# Architecture — SMK Academy

## Vue d'ensemble

```
Navigateur ──► Netlify (Next.js 16, OpenNext)
                 ├─ src/proxy.ts           rafraîchit la session, protège les espaces privés
                 ├─ Server Components      lecture des données (RLS appliquée avec le JWT de l'étudiant)
                 └─ Server Actions         écritures via fonctions Postgres (RPC)
                          │
                          ▼
               Supabase (projet smk-academy-dev, eu-west-2)
                 ├─ Auth                   comptes, emails de confirmation
                 ├─ public.*               catalogue + données étudiant, RLS partout
                 └─ private.*              corrigés des quiz, fonctions internes (non exposés)
```

Aucune clé secrète n'est utilisée par l'application : seule la clé **publishable** est déployée, et toutes les règles d'accès vivent dans Postgres.

## Arborescence

```
src/
  proxy.ts                         session Supabase + redirection vers /connexion
  app/
    page.tsx                       accueil
    formations/                    catalogue, page formation, leçon, quiz
      [slug]/[module]/[lesson]/    lecteur de leçon (Markdown)
      [slug]/[module]/quiz/        quiz (énoncés uniquement)
    resultats/[attemptId]/         note /20 + correction détaillée
    tableau-de-bord/               progression, moyenne, historique
    inscription | connexion | mot-de-passe-oublie | compte/nouveau-mot-de-passe
    auth/confirm/route.ts          liens email (PKCE ?code= et token_hash)
    actions/auth.ts                inscription, connexion, déconnexion, mots de passe
    actions/learning.ts            inscription à une formation, leçon terminée, quiz
  components/                      en-tête, Markdown, formulaire de quiz, icônes
  lib/
    learning.ts                    types, calculs purs, validation Zod (testés)
    queries.ts                     lectures Supabase côté serveur
    database.types.ts              types générés du schéma
    supabase/server.ts             client serveur + getCurrentUser (getClaims)
content/python_debutant.py         source du contenu pédagogique
scripts/build_seed.py              contenu → migration SQL idempotente (UUID v5)
scripts/build_icons.py             logo → favicon, icônes PWA
supabase/migrations/               schéma, contenu, durcissement
supabase/tests/                    tests SQL de sécurité et de notation
e2e/                               parcours étudiant Playwright
```

## Modèle de données

| Table | Rôle | Accès API |
|---|---|---|
| `profiles` | nom, rôle (`student`/`admin`), offre (`free`/`premium`) | lecture de son profil ; mise à jour de `full_name` uniquement |
| `courses`, `modules` | catalogue et plan | lecture publique (publié / à venir) |
| `lessons`, `quizzes`, `quiz_questions`, `quiz_options` | contenu | lecture si connecté et module publié |
| `private.quiz_answer_keys` | bonnes réponses + explications | **aucun** |
| `enrollments` | inscriptions + dernière leçon ouverte | lecture des siennes |
| `lesson_progress` | leçons terminées | lecture des siennes |
| `quiz_attempts` | notes, corrections | lecture des siennes |

Les écritures étudiantes passent exclusivement par des fonctions `SECURITY DEFINER` (`search_path = ''`, contrôle de `auth.uid()`) :

- `enroll_in_course(course_id)`
- `touch_lesson(lesson_id)` — mémorise la position (bouton « Reprendre »)
- `complete_lesson(lesson_id)` — idempotent
- `submit_quiz(quiz_id, answers jsonb)` — calcule la note sur 20 **en base**, enregistre la tentative et la correction, limite à 10 tentatives/minute

## Notation

Une question rapporte tous ses points si l'ensemble des options cochées est exactement l'ensemble des bonnes réponses, sinon 0. Note = points / total × 20, arrondie à 2 décimales. Seuil de validation par quiz (`pass_mark`, 10 par défaut). Les identifiants inconnus ou appartenant à une autre question sont ignorés.

## Sécurité

- RLS activée sur toutes les tables ; politiques avec `(select auth.uid())`.
- Privilèges : `revoke all` puis grants minimaux (aucun `TRUNCATE`/`INSERT` direct pour les rôles API) ; privilèges par défaut révoqués pour les futures tables.
- Les corrigés ne quittent jamais la base avant soumission.
- Rôle et offre non modifiables par l'étudiant (privilège de colonne).
- Identité vérifiée côté serveur avec `auth.getClaims()` (signature du JWT).
- Redirections internes uniquement (`safeNextPath`), validation Zod de toutes les entrées.
- En-têtes : `X-Frame-Options: DENY`, `nosniff`, `Referrer-Policy`, `Permissions-Policy`.
- Markdown rendu sans HTML brut (`skipHtml`).

## Design system

Couleurs issues du logo SMKTECH : bleu `#0B4BD6` réservé aux éléments interactifs, vert `#00A87E` réservé aux réussites (leçon terminée, quiz validé). Police système Apple (SF) avec Inter en repli. Boutons capsules ≥ 44 px, barre de navigation flottante translucide, mode sombre sur fond noir. Jetons dans `src/app/globals.css` (`@layer components`).
