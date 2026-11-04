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
- Contenu : `content/*.py` → `scripts/build_seed.py` (UUID v5 déterministes, upserts idempotents).
- Vérifier avant de livrer : `npm run typecheck && npm run lint && npm test && npm run build`.

## Environnement Claude

- Le bac à sable ne joint pas `*.supabase.co` : passer par le connecteur Supabase (MCP) pour le SQL ; tester le parcours complet sur le site Netlify.
- Chrome est disponible (`/usr/bin/google-chrome`) pour des captures Playwright (`executablePath`).
- Si `next build` échoue avec « Bus error », le binaire SWC est tronqué : `rm -rf node_modules && npm ci`.

## État et suite

Voir ROADMAP.md (jalon 1 livré) et TEST_REPORT.md. Prochaine étape : site Netlify + configuration Auth Supabase, puis test de bout en bout, puis modules 3 à 5 de Python.
