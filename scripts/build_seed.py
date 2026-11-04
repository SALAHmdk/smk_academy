"""Génère la migration SQL du contenu pédagogique à partir de content/*.py.

Usage : python3 scripts/build_seed.py [--content python_debutant] [--modules 1,2] > supabase/migrations/<horodatage>_seed_x.sql

Les identifiants sont déterministes (UUID v5 dérivés des slugs) : relancer la
migration met à jour le contenu sans casser la progression des étudiants.
"""

import importlib.util
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMESPACE = uuid.UUID("5d0c9a3e-8b1f-4c6e-9a27-3f1e5b7c2d40")  # espace de noms SMK Academy
POINTS_PER_QUESTION = 2


def load_content():
    """--content NOM charge content/NOM.py (par défaut python_debutant)."""
    name = sys.argv[sys.argv.index("--content") + 1] if "--content" in sys.argv else "python_debutant"
    spec = importlib.util.spec_from_file_location("content", ROOT / "content" / f"{name}.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def uid(*parts: object) -> str:
    return str(uuid.uuid5(NAMESPACE, "/".join(str(p) for p in parts)))


def lit(value) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    text = str(value)
    tag = "$smk$"
    assert tag not in text, "délimiteur présent dans le contenu"
    return f"{tag}{text}{tag}"


def arr(values) -> str:
    return "array[" + ", ".join(lit(v) for v in values) + "]::text[]" if values else "'{}'::text[]"


CATEGORY_SLUGS = {
    "Programmation": "programmation",
    "Bases de données": "bases-de-donnees",
    "Langues": "langues",
}


def course_sql(c) -> str:
    """Insère ou met à jour une formation SANS toucher à son statut (géré à la fin, après les modules)."""
    cid = uid("course", c["slug"])
    category = c.get("category_slug") or CATEGORY_SLUGS[c["category"]]
    return (
        "insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, "
        "duration_minutes, objectives, prerequisites, status, is_premium, position) values ("
        f"'{cid}', {lit(c['slug'])}, {lit(c['title'])}, {lit(c['subtitle'])}, {lit(c['description'])}, "
        f"(select id from public.categories where slug = {lit(category)}), {lit(c.get('topic', ''))}, "
        f"{lit(c.get('cover_label', ''))}, {lit(c['level'])}, {c['duration_minutes']}, {arr(c['objectives'])}, "
        f"{arr(c['prerequisites'])}, 'coming_soon', {lit(c['is_premium'])}, {c['position']})\n"
        "on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, "
        "description = excluded.description, category_id = excluded.category_id, level = excluded.level, "
        "duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, "
        "prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;\n"
    )


TABLES = {
    "modules": ("public.modules", "id, course_id, title, description, position, status", "id",
                "title = excluded.title, description = excluded.description, position = excluded.position"),
    "lessons": ("public.lessons", "id, module_id, slug, title, summary, content_md, duration_minutes, position", "id",
                "slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, "
                "duration_minutes = excluded.duration_minutes, position = excluded.position"),
    "quizzes": ("public.quizzes", "id, module_id, title, pass_mark", "id",
                "title = excluded.title, pass_mark = excluded.pass_mark"),
    "questions": ("public.quiz_questions", "id, quiz_id, position, kind, prompt, code, points", "id",
                  "position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points"),
    "options": ("public.quiz_options", "id, question_id, position, label", "id",
                "position = excluded.position, label = excluded.label"),
    "keys": ("private.quiz_answer_keys", "question_id, correct_option_ids, explanation", "question_id",
             "correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation"),
}


def emit(out, rows):
    for key, (table, cols, pk, updates) in TABLES.items():
        if rows[key]:
            values = ",\n".join("(" + r + ")" for r in rows[key])
            out.append(f"insert into {table} ({cols}) values\n{values}\non conflict ({pk}) do update set {updates};\n")


def main() -> None:
    # Option : --modules 3,4,5 pour ne générer que certains modules (sans les cours).
    only = None
    if "--modules" in sys.argv:
        only = {int(x) for x in sys.argv[sys.argv.index("--modules") + 1].split(",")}
    content = load_content()
    out = ["-- Généré par scripts/build_seed.py — ne pas modifier à la main."]
    rows = {k: [] for k in TABLES}
    statuses = []

    out.append(course_sql(content.COURSE))

    slug = content.COURSE["slug"]
    cid = uid("course", slug)
    for m in content.MODULES:
        if only is not None and m["position"] not in only:
            continue
        mid = uid("module", slug, m["position"])
        rows["modules"].append(f"'{mid}', '{cid}', {lit(m['title'])}, {lit(m['description'])}, {m['position']}, 'draft'")
        statuses.append((mid, m["status"]))
        for pos, (lslug, title, summary, md, minutes) in enumerate(m["lessons"], start=1):
            lid = uid("lesson", slug, m["position"], lslug)
            rows["lessons"].append(f"'{lid}', '{mid}', {lit(lslug)}, {lit(title)}, {lit(summary)}, {lit(md.strip())}, {minutes}, {pos}")
        if m["quiz"]:
            qtitle, questions = m["quiz"]
            qid = uid("quiz", slug, m["position"])
            rows["quizzes"].append(f"'{qid}', '{mid}', {lit(qtitle)}, 10")
            for qpos, (kind, prompt, code, options, correct, explanation) in enumerate(questions, start=1):
                assert correct and all(0 <= i < len(options) for i in correct), prompt
                if kind != "multiple":
                    assert len(correct) == 1, prompt
                qqid = uid("question", slug, m["position"], qpos)
                rows["questions"].append(f"'{qqid}', '{qid}', {qpos}, {lit(kind)}, {lit(prompt)}, {lit(code)}, {POINTS_PER_QUESTION}")
                option_ids = []
                for opos, label in enumerate(options, start=1):
                    oid = uid("option", slug, m["position"], qpos, opos)
                    option_ids.append(oid)
                    rows["options"].append(f"'{oid}', '{qqid}', {opos}, {lit(label)}")
                correct_ids = ", ".join(f"'{option_ids[i]}'" for i in correct)
                rows["keys"].append(f"'{qqid}', array[{correct_ids}]::uuid[], {lit(explanation)}")

    emit(out, rows)
    # Statuts appliqués en dernier : les garde-fous en base vérifient que chaque module publié est complet.
    for mid, status in statuses:
        out.append(f"update public.modules set status = {lit(status)} where id = '{mid}';")
    c = content.COURSE
    out.append(f"update public.courses set status = {lit(c['status'])} where slug = {lit(c['slug'])};")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
