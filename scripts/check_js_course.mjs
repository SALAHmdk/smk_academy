// Vérifie les exemples d'une formation JavaScript : chaque bloc ```js / ```solution-js sans DOM ni réseau
// est exécuté avec Node ; s'il est suivi d'un bloc ```text, la sortie doit être identique.
// Usage : node scripts/check_js_course.mjs content/build/javascript-debutant.json
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";

const file = process.argv[2] ?? "content/build/javascript-debutant.json";
const data = JSON.parse(readFileSync(file, "utf8"));
const SKIP = /document\.|window\.|localStorage|fetch\(|alert\(|addEventListener|classList|\.textContent|\.style\./;
let ok = 0, skipped = 0, failed = 0;

for (const m of data.modules) {
  for (const l of m.lessons) {
    const re = /```(js|solution-js)\n([\s\S]*?)```(?:\s*```text\n([\s\S]*?)```)?/g;
    for (const [, , code, expected] of l.content_md.matchAll(re)) {
      if (SKIP.test(code) || code.includes("console.lg")) {
        // Non exécuté (DOM, réseau) : on vérifie au moins la syntaxe.
        try {
          new Function(code);
        } catch (e) {
          failed++;
          console.error(`ÉCHEC ${l.slug} : syntaxe (${e.message})\n${code}`);
          continue;
        }
        skipped++;
        continue;
      }
      let out = "";
      try {
        out = execFileSync(process.execPath, ["--input-type=module", "-e", code], { timeout: 5000, encoding: "utf8" });
      } catch (e) {
        failed++;
        console.error(`ÉCHEC ${l.slug} : exécution\n${code}\n${e.stderr || e.message}`);
        continue;
      }
      if (expected !== undefined && out.trimEnd() !== expected.trimEnd()) {
        failed++;
        console.error(`ÉCHEC ${l.slug} : sortie différente\n--- code\n${code}--- attendu\n${expected}--- obtenu\n${out}`);
        continue;
      }
      ok++;
    }
  }
}
console.log(`${ok} blocs vérifiés, ${skipped} vérifiés en syntaxe seulement (DOM, réseau), ${failed} échecs`);
process.exit(failed ? 1 : 0);
