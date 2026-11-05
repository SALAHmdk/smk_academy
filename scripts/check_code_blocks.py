"""Vérifie les exemples de code d'une formation (content/build/<slug>.json).

Règle : un bloc de code (```<langage> ou ```solution-<langage>) immédiatement suivi d'un bloc ```text
est EXÉCUTÉ et sa sortie doit être identique au bloc ```text. Les autres blocs exécutables sont
compilés ou exécutés à titre indicatif : un échec est signalé en avertissement (fragments, entrées clavier…).

Langages exécutés : python, js, ts, java, c, cpp, go, rust, php.
Usage : python3 scripts/check_code_blocks.py content/build/java-debutant.json [--strict]
  --strict : les avertissements comptent comme des échecs.
"""

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TIMEOUT = 20
BLOCK = re.compile(r"```(solution-)?([a-z+#]+)\n(.*?)```(?:\s*```text\n(.*?)```)?", re.S)
ALIASES = {"python": "python", "py": "python", "solution": "python", "js": "js", "javascript": "js", "ts": "ts",
           "typescript": "ts", "java": "java", "c": "c", "cpp": "cpp", "c++": "cpp", "go": "go", "rust": "rust",
           "rs": "rust", "php": "php"}


def run(lang: str, code: str, tmp: Path) -> tuple[bool, str]:
    def sh(cmd, cwd=tmp):
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT)
        return p.returncode == 0, p.stdout if p.returncode == 0 else (p.stdout + p.stderr)

    if lang == "python":
        (tmp / "m.py").write_text(code)
        return sh([sys.executable, "-I", "m.py"])
    if lang == "js":
        (tmp / "m.mjs").write_text(code)
        return sh(["node", "m.mjs"])
    if lang == "ts":
        (tmp / "m.ts").write_text(code)
        ok, out = sh(["tsc", "--strict", "--target", "es2022", "--module", "es2022", "--outDir", "out", "m.ts"])
        if not ok:
            return ok, out
        (tmp / "out" / "package.json").write_text('{"type":"module"}')
        return sh(["node", "out/m.js"])
    if lang == "java":
        m = re.search(r"public\s+(?:final\s+)?class\s+(\w+)", code)
        name = m.group(1) if m else "Main"
        (tmp / f"{name}.java").write_text(code)
        ok, out = sh(["javac", f"{name}.java"])
        if not ok or "static void main" not in code:
            return ok, out
        return sh(["java", "-cp", ".", name])
    if lang in ("c", "cpp"):
        src = "m.c" if lang == "c" else "m.cpp"
        (tmp / src).write_text(code)
        cc = ["gcc", "-std=c17"] if lang == "c" else ["g++", "-std=c++20"]
        ok, out = sh(cc + ["-Wall", "-o", "m", src, "-lm"])
        if not ok or "main(" not in code:
            return ok, out
        return sh(["./m"])
    if lang == "go":
        (tmp / "m.go").write_text(code)
        if "package main" not in code:
            return sh(["gofmt", "-e", "m.go"])
        return sh(["go", "run", "m.go"])
    if lang == "rust":
        (tmp / "m.rs").write_text(code)
        if "fn main" not in code:
            return sh(["rustc", "--edition", "2021", "--crate-type", "lib", "m.rs"])
        ok, out = sh(["rustc", "--edition", "2021", "-o", "m", "m.rs"])
        return sh(["./m"]) if ok else (ok, out)
    if lang == "php":
        (tmp / "m.php").write_text(code)
        return sh(["php", "m.php"])
    raise ValueError(lang)


def main() -> int:
    path = Path(sys.argv[1])
    strict = "--strict" in sys.argv
    data = json.loads(path.read_text(encoding="utf-8"))
    checked = warned = failed = 0
    for m in data["modules"]:
        for lesson in m["lessons"]:
            for sol, raw, code, expected in BLOCK.findall(lesson["content_md"]):
                lang = ALIASES.get(raw if not sol else raw)
                if raw == "solution" and not sol:
                    lang = "python"
                if lang is None:
                    continue
                tmp = Path(tempfile.mkdtemp())
                try:
                    ok, out = run(lang, code, tmp)
                except subprocess.TimeoutExpired:
                    ok, out = False, "délai dépassé"
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)
                where = f"{lesson['slug']} [{sol}{raw}]"
                norm = lambda t: "\n".join(line.rstrip() for line in t.strip("\n").splitlines())
                # Exemple d'erreur volontaire : la dernière ligne attendue (message d'erreur) figure dans la sortie.
                error_demo = expected and not ok and expected.strip().splitlines()[-1].strip() in out
                if expected and not error_demo:
                    if not ok or norm(out) != norm(expected):
                        failed += 1
                        print(f"ÉCHEC {where}\n--- code\n{code}--- attendu\n{expected}--- obtenu\n{out}\n")
                    else:
                        checked += 1
                elif error_demo:
                    checked += 1
                elif not ok:
                    warned += 1
                    print(f"AVERTISSEMENT {where} (non exécutable seul ?)\n{out[:600]}\n")
                else:
                    checked += 1
    print(f"{checked} blocs vérifiés, {warned} avertissement(s), {failed} échec(s)")
    return 1 if failed or (strict and warned) else 0


if __name__ == "__main__":
    sys.exit(main())
