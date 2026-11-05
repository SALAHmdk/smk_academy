"""Contrôle de structure d'une formation exportée (content/build/<slug>.json) avant publication.

Usage : python3 scripts/validate_course.py content/build/<slug>.json [...]
Vérifie : 5 modules × 3 leçons, 10 questions par quiz, métadonnées conformes au catalogue,
longueur des leçons, sections « À retenir » et « Exercices », blocs de code fermés, réponses valides,
explications présentes, absence de marqueurs de brouillon.
"""

import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("catalogue", ROOT / "content" / "catalogue.py")
cat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cat)
CATALOGUE = {item[0]: (slug_cat, item) for slug_cat, items in cat.CATALOGUE.items() for item in items}
DRAFT = re.compile(r"\b(TODO|FIXME|XXX|lorem ipsum|à compléter)\b", re.I)


def check(path: Path) -> list[str]:
    d = json.loads(path.read_text(encoding="utf-8"))
    c, mods = d["course"], d["modules"]
    errs: list[str] = []
    entry = CATALOGUE.get(c["slug"])
    if entry:
        category, (slug, title, _sub, topic, cover, level, duration, *_rest) = entry
        for key, want in (("title", title), ("level", level), ("category_slug", category), ("cover_label", cover)):
            if c[key] != want:
                errs.append(f"métadonnée {key} = {c[key]!r}, catalogue = {want!r}")
    if c["status"] != "published" or c["is_premium"]:
        errs.append("statut attendu : published, is_premium False")
    if len(mods) != 5:
        errs.append(f"{len(mods)} modules au lieu de 5")
    slugs = set()
    total = 0
    for m in mods:
        if len(m["lessons"]) != 3:
            errs.append(f"module {m['position']} : {len(m['lessons'])} leçons")
        for lesson in m["lessons"]:
            md = lesson["content_md"]
            total += lesson["duration_minutes"]
            where = f"M{m['position']} {lesson['slug']}"
            if lesson["slug"] in slugs:
                errs.append(f"{where} : slug en double")
            slugs.add(lesson["slug"])
            if not 2500 <= len(md) <= 16000:
                errs.append(f"{where} : {len(md)} caractères")
            if md.count("```") % 2:
                errs.append(f"{where} : bloc de code non fermé")
            if "## À retenir" not in md:
                errs.append(f"{where} : section « À retenir » absente")
            if "## Exercices" not in md and not (m["position"] == 5 and lesson["position"] == 3):
                errs.append(f"{where} : section « Exercices » absente")
            if "```solution" not in md and not (m["position"] == 5 and lesson["position"] == 3):
                errs.append(f"{where} : aucune correction")
            if DRAFT.search(md):
                errs.append(f"{where} : marqueur de brouillon « {DRAFT.search(md).group(0)} »")
        q = m.get("quiz") or {}
        questions = q.get("questions", [])
        if len(questions) != 10:
            errs.append(f"module {m['position']} : {len(questions)} questions")
        kinds = {x["kind"] for x in questions}
        if questions and "multiple" not in kinds:
            errs.append(f"module {m['position']} : aucune question à choix multiples")
        positions = []
        for x in questions:
            if not x["explanation"] or len(x["explanation"]) < 30:
                errs.append(f"module {m['position']} Q{x['position']} : explication trop courte")
            if len(x["options"]) < 2 or len({o['label'] for o in x['options']}) != len(x["options"]):
                errs.append(f"module {m['position']} Q{x['position']} : options invalides ou en double")
            if x["kind"] == "true_false" and [o["label"] for o in x["options"]] != ["Vrai", "Faux"]:
                errs.append(f"module {m['position']} Q{x['position']} : vrai/faux mal formé")
            ids = [o["id"] for o in x["options"]]
            positions += [ids.index(i) for i in x["correct"]]
        if positions and len(set(positions)) == 1 and len(positions) >= 8:
            errs.append(f"module {m['position']} : la bonne réponse est toujours à la même position")
    if entry and not 0.6 * entry[1][6] <= total <= 1.4 * entry[1][6]:
        errs.append(f"durée cumulée des leçons {total} min, annoncée {entry[1][6]} min")
    return errs


def main() -> int:
    bad = 0
    for p in sys.argv[1:]:
        errs = check(Path(p))
        print(f"{'OK ' if not errs else 'KO '} {p}" + "".join(f"\n   - {e}" for e in errs))
        bad += bool(errs)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
