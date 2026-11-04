# CLAUDE.md — reprise du projet SMK Academy

Plateforme e-learning de SMKTECH. Dépôt unique : `SALAHmdk/smk_academy` (ne jamais créer d'autre dépôt). Supabase : projet `smk-academy-dev` (`xebdrfqotzfitbtxeohp`). Hébergement : Netlify uniquement (jamais Vercel). Paiements : Stripe en mode test puis PayPal — **pas avant** que la plateforme pédagogique soit validée.

## Règles

- Demander l'accord du propriétaire avant toute action irréversible ou touchant un service existant (sites Netlify existants, projets Supabase, paiements).
- Ne jamais commiter de secret ; seule la clé Supabase **publishable** est utilisée côté application.
- Interface et contenus en français, vouvoiement.
- Ne jamais présenter une formation ou un module vide comme complet.
- Distinguer dans TEST_REPORT.md les tests exécutés de ceux seulement préparés.

## Conventions techniques

- Next.js 16 App Router : `params`/`searchParams` sont des Promises ; le middleware s'appelle `src/proxy.ts` (export `proxy`).
- `cacheComponents: false` (rendu dynamique, pages dépendantes de la session).
- Identité : `getCurrentUser()` (`src/lib/supabase/server.ts`, basé sur `auth.getClaims()`), jamais `getSession()` côté serveur.
- Écritures étudiantes : uniquement via RPC Postgres (`enroll_in_course`, `touch_lesson`, `complete_lesson`, `submit_quiz`). Aucune note n'est calculée dans Next.js.
- Nouvelle table : RLS + `revoke all` + grants explicites (les privilèges par défaut sont révoqués). Politiques avec `(select auth.uid())`, index sur les colonnes filtrées.
- Après une migration : régénérer `src/lib/database.types.ts`, lancer l'advisor sécurité Supabase et `supabase/tests/security_and_grading.sql`.
- CSS : jetons et classes de composants dans `@layer components` de `globals.css` (sinon ils écrasent les utilitaires Tailwind). Bleu = interactif, vert = réussite uniquement.
- Lightning CSS ne garde que la dernière déclaration d'une paire préfixée : écrire `-webkit-backdrop-filter` AVANT `backdrop-filter`.
- Thème : cookie `smk-theme` (light/dark) → `<html data-theme>` ; absent = système.
- Nouveau contenu : `python3 scripts/build_seed.py --modules N` génère une migration ne contenant que ce module ; ne jamais réécrire une migration déjà appliquée.
- Contenu : `content/*.py` → `scripts/build_seed.py` (UUID v5 déterministes, upserts idempotents).
- Dépendances : n'installer que des versions publiées depuis au moins une semaine (`npm install --before=<date>`). Le registre utilisé par Netlify n'avait pas encore les versions de la veille (échec ETARGET du 04/11 sur is-core-module@2.18.0). Chaque entrée du package-lock.json doit avoir `resolved` et `integrity`.
- Vérifier avant de livrer : `npm run typecheck && npm run lint && npm test && npm run build`.

## Environnement Claude

- Le bac à sable ne joint pas `*.supabase.co` : passer par le connecteur Supabase (MCP) pour le SQL ; tester le parcours complet sur le site Netlify.
- Chrome est disponible (`/usr/bin/google-chrome`) pour des captures Playwright (`executablePath`).
- Si `next build` échoue avec « Bus error », le binaire SWC est tronqué : `rm -rf node_modules && npm ci`.

## État et suite

Voir ROADMAP.md (jalons 1 et 2 livrés : parcours étudiant + formation Python complète, design Apple) et TEST_REPORT.md.
Prochaine étape : site Netlify (création via API refusée en 429 le 04/11 : import manuel depuis l'interface) + configuration Auth Supabase, puis test de bout en bout, puis examen final Python et administration.

Captures locales : `python3 mock_supabase.py <repo>` (API simulée) + `next dev` avec `NEXT_PUBLIC_SUPABASE_URL=http://127.0.0.1:54321`, session simulée par un cookie `sb-127-auth-token` contenant un JWT HS256 factice (voir l'historique de session).
