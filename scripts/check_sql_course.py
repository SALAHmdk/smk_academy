"""Exécute chaque bloc ```sql / ```solution-sql de la formation SQL sur la base d'exemple (SQLite).

Usage : python3 scripts/check_sql_course.py
Chaque bloc s'exécute sur une base neuve : les exemples INSERT/UPDATE/DELETE ne s'influencent pas.
Les blocs volontairement erronés ou propres à un SGBD sont listés dans EXPECTED_FAILURES.
"""
import importlib.util
import re
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("sql_course", ROOT / "content" / "sql_debutant.py")
course = importlib.util.module_from_spec(spec)
spec.loader.exec_module(course)

SETUP = re.search(r"```sql\n(CREATE TABLE etudiants.*?)```", course.M1_L1, re.S).group(1)

# Fragments identifiant les blocs dont l'échec est attendu (exemples d'erreurs ou syntaxe d'un autre SGBD).
EXPECTED_FAILURES = [
    "GENERATED ALWAYS AS IDENTITY",        # syntaxes d'identifiants propres à chaque SGBD
    "VALUES (9, 42, 1",                    # violation de clé étrangère (démonstration)
    "WHERE MAX(note) > 15",                # agrégation dans WHERE (démonstration)
    "SELECT ville, prenom, COUNT(*) FROM etudiants GROUP BY ville",  # refusé par PostgreSQL ; SQLite tolère
    "SELECT prenom, COUNT(*) FROM etudiants;",                         # idem
    "FROM table",                          # gabarits de syntaxe (SELECT colonnes FROM table)
    "valeur_par_defaut",                   # gabarit de CASE
    "DROP TABLE avis",                     # suppose la table avis créée dans l'exemple précédent
]


def blocks():
    for name in dir(course):
        if re.fullmatch(r"M\d_L\d", name):
            yield name, getattr(course, name)
    for name in dir(course._m35):
        if re.fullmatch(r"M\d_L\d", name):
            yield name, getattr(course._m35, name)


def main() -> int:
    ok = failed = expected = 0
    for lesson, md in sorted(blocks()):
        for lang, code in re.findall(r"```(sql|solution-sql)\n(.*?)```", md, re.S):
            if code.startswith("CREATE TABLE etudiants"):
                continue
            con = sqlite3.connect(":memory:")
            con.execute("PRAGMA foreign_keys = ON")
            con.executescript(SETUP)
            sql = code
            if "BEGIN;" in sql:
                sql = sql.replace("BEGIN;", "BEGIN TRANSACTION;")
            try:
                con.executescript(sql) if sql.count(";") > 1 else con.execute(sql).fetchall()
                ok += 1
            except sqlite3.Error as e:
                if any(f in code for f in EXPECTED_FAILURES):
                    expected += 1
                else:
                    failed += 1
                    print(f"ÉCHEC {lesson} [{lang}] : {e}\n{code}\n")
    print(f"{ok} blocs exécutés, {expected} échecs attendus, {failed} échecs inattendus")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
