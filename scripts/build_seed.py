"""Génère la migration SQL du contenu pédagogique à partir de content/*.py.

Usage : python3 scripts/build_seed.py > supabase/migrations/<horodatage>_seed_python.sql

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
    spec = importlib.util.spec_from_file_location("content", ROOT / "content" / "python_debutant.py")
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


def course_sql(c) -> str:
    cid = uid("course", c["slug"])
    return (
        "insert into public.courses (id, slug, title, subtitle, description, category, level, "
        "duration_minutes, objectives, prerequisites, status, is_premium, position) values ("
        f"'{cid}', {lit(c['slug'])}, {lit(c['title'])}, {lit(c['subtitle'])}, {lit(c['description'])}, "
        f"{lit(c['category'])}, {lit(c['level'])}, {c['duration_minutes']}, {arr(c['objectives'])}, "
        f"{arr(c['prerequisites'])}, {lit(c['status'])}, {lit(c['is_premium'])}, {c['position']})\n"
        "on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, "
        "description = excluded.description, category = excluded.category, level = excluded.level, "
        "duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, "
        "prerequisites = excluded.prerequisites, status = excluded.status, "
        "is_premium = excluded.is_premium, position = excluded.position;\n"
    )


TABLES = {
    "modules": ("public.modules", "id, course_id, title, description, position, status", "id",
                "title = excluded.title, description = excluded.description, position = excluded.position, status = excluded.status"),
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
    content = load_content()
    out = ["-- Généré par scripts/build_seed.py — ne pas modifier à la main."]
    rows = {k: [] for k in TABLES}

    for c in [content.COURSE, *content.OTHER_COURSES]:
        out.append(course_sql(c))

    slug = content.COURSE["slug"]
    cid = uid("course", slug)
    for m in content.MODULES:
        mid = uid("module", slug, m["position"])
        rows["modules"].append(f"'{mid}', '{cid}', {lit(m['title'])}, {lit(m['description'])}, {m['position']}, {lit(m['status'])}")
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
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
