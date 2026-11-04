"""Génère la migration SQL du catalogue (formations annoncées « Bientôt disponible »).

Usage : python3 scripts/build_catalog.py > supabase/migrations/<horodatage>_catalog_courses.sql

Idempotent : UUID v5 déterministes. Une formation déjà publiée n'est jamais repassée
en « Bientôt disponible » (le statut n'est écrit qu'à la création).
"""

import importlib.util
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAMESPACE = uuid.UUID("5d0c9a3e-8b1f-4c6e-9a27-3f1e5b7c2d40")


def load():
    spec = importlib.util.spec_from_file_location("catalogue", ROOT / "content" / "catalogue.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def lit(v) -> str:
    text = str(v)
    assert "$smk$" not in text
    return f"$smk${text}$smk$"


def arr(values) -> str:
    return "array[" + ", ".join(lit(v) for v in values) + "]::text[]"


def main() -> None:
    cat = load()
    rows = []
    position = 10
    for category_slug, courses in cat.CATALOGUE.items():
        for slug, title, subtitle, topic, cover, level, minutes, objectives, prereq in courses:
            position += 1
            cid = uuid.uuid5(NAMESPACE, f"course/{slug}")
            rows.append(
                f"('{cid}', {lit(slug)}, {lit(title)}, {lit(subtitle)}, {lit(subtitle)}, "
                f"(select id from public.categories where slug = {lit(category_slug)}), {lit(topic)}, {lit(cover)}, "
                f"{lit(level)}, {minutes}, {arr(objectives)}, {arr(prereq)}, 'coming_soon', false, {position})"
            )
    out = [
        "-- Généré par scripts/build_catalog.py — ne pas modifier à la main.",
        "insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level,",
        "  duration_minutes, objectives, prerequisites, status, is_premium, position) values",
        ",\n".join(rows),
        "on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle,",
        "  category_id = excluded.category_id, topic = excluded.topic, cover_label = excluded.cover_label,",
        "  level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives,",
        "  prerequisites = excluded.prerequisites, position = excluded.position;",
        "",
    ]
    for slug, (category_slug, topic, cover, position) in cat.EXISTING.items():
        out.append(
            f"update public.courses set category_id = (select id from public.categories where slug = {lit(category_slug)}), "
            f"topic = {lit(topic)}, cover_label = {lit(cover)}, position = {position} where slug = {lit(slug)};"
        )
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
