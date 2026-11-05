// Import des formations du dépôt (content/build/*.json) dans Supabase, exécuté à la fin du build Netlify.
// Protégé par CONTENT_IMPORT_TOKEN (variable Netlify, jamais exposée au navigateur).
// Sans jeton (build local, aperçu), l'import est simplement ignoré.
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY;
const token = process.env.CONTENT_IMPORT_TOKEN;
const dir = path.join(process.cwd(), "content", "build");

if (!token || !url || !key) {
  console.log("[contenu] CONTENT_IMPORT_TOKEN absent : import des formations ignoré.");
  process.exit(0);
}
if (process.env.CONTEXT && process.env.CONTEXT !== "production") {
  console.log(`[contenu] contexte ${process.env.CONTEXT} : import réservé à la production.`);
  process.exit(0);
}

const files = (await readdir(dir)).filter((f) => f.endsWith(".json")).sort();
let failed = 0;
for (const file of files) {
  const payload = JSON.parse(await readFile(path.join(dir, file), "utf8"));
  const res = await fetch(`${url}/rest/v1/rpc/content_import_if_changed`, {
    method: "POST",
    headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({ p_token: token, p_payload: payload }),
  });
  const body = await res.text();
  if (res.ok) {
    console.log(`[contenu] ${JSON.parse(body)}`);
  } else {
    failed++;
    console.error(`[contenu] ÉCHEC ${file} (${res.status}) : ${body.slice(0, 500)}`);
  }
}
if (failed) {
  console.error(`[contenu] ${failed} formation(s) non importée(s).`);
  process.exit(1);
}
