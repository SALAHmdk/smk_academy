// Vérifie les exemples d'une formation HTML/CSS :
//  - blocs ```html / ```solution-html : balises correctement ouvertes, fermées et imbriquées ;
//  - blocs ```css / ```solution-css : analysés par Lightning CSS (erreur = échec), avertissements signalés.
// Usage : node scripts/check_web_course.mjs content/build/html-css.json
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const { transform } = require("lightningcss");
const file = process.argv[2] ?? "content/build/html-css.json";
const data = JSON.parse(readFileSync(file, "utf8"));

const VOID = new Set(["area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"]);
// Éléments dont la fermeture est facultative en HTML : tolérés s'ils ne sont pas fermés.
const OPTIONAL_CLOSE = new Set(["li", "option", "p", "td", "th", "tr"]);

function checkHtml(code) {
  const stack = [];
  const src = code.replace(/<!--[\s\S]*?-->/g, "").replace(/<!DOCTYPE[^>]*>/i, "");
  for (const [, closing, name] of src.matchAll(/<(\/?)([a-zA-Z][a-zA-Z0-9-]*)\b[^>]*>/g)) {
    const tag = name.toLowerCase();
    if (VOID.has(tag)) continue;
    if (!closing) {
      stack.push(tag);
      continue;
    }
    while (stack.length && stack.at(-1) !== tag && OPTIONAL_CLOSE.has(stack.at(-1))) stack.pop();
    if (stack.at(-1) !== tag) return `</${tag}> inattendu (ouvert : ${stack.at(-1) ?? "aucun"})`;
    stack.pop();
  }
  const left = stack.filter((t) => !OPTIONAL_CLOSE.has(t));
  return left.length ? `non fermé : ${left.join(", ")}` : null;
}

function checkCss(code) {
  const sansCommentaires = code.replace(/\/\*[\s\S]*?\*\//g, "");
  const ouvrantes = (sansCommentaires.match(/{/g) ?? []).length;
  const fermantes = (sansCommentaires.match(/}/g) ?? []).length;
  if (ouvrantes !== fermantes) throw new Error(`accolades déséquilibrées (${ouvrantes} « { » pour ${fermantes} « } »)`);
  const warnings = [];
  transform({
    filename: "exemple.css",
    code: Buffer.from(code),
    errorRecovery: false,
    onWarning: (w) => warnings.push(w.message),
  });
  return warnings;
}

let ok = 0, failed = 0, warned = 0;
for (const m of data.modules) {
  for (const l of m.lessons) {
    for (const [, lang, code] of l.content_md.matchAll(/```(html|solution-html|css|solution-css)\n([\s\S]*?)```/g)) {
      try {
        if (lang.endsWith("html")) {
          const err = checkHtml(code);
          if (err) throw new Error(err);
        } else {
          const w = checkCss(code);
          if (w.length) {
            warned++;
            console.warn(`AVERTISSEMENT ${l.slug} : ${w.join(" ; ")}`);
          }
        }
        ok++;
      } catch (e) {
        failed++;
        console.error(`ÉCHEC ${l.slug} [${lang}] : ${e.message}\n${code}`);
      }
    }
  }
}
console.log(`${ok} blocs valides, ${warned} avertissement(s), ${failed} échec(s)`);
process.exit(failed ? 1 : 0);
