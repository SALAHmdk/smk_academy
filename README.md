# SMK Academy by SMKTECH

**Learn. Practice. Succeed.**

Plateforme de formation en ligne de SMKTECH : comptes étudiants, catalogue, leçons avec exercices corrigés, quiz notés sur 20 et progression enregistrée.

## État actuel — jalon 1

| Fonctionnalité | État |
|---|---|
| Page d'accueil responsive (clair / sombre) | ✅ |
| Inscription, confirmation d'email, connexion, déconnexion | ✅ |
| Mot de passe oublié / nouveau mot de passe | ✅ |
| Catalogue (disponibles / à venir) | ✅ |
| Formation Python : modules 1 et 2 publiés (6 leçons, 12 exercices corrigés, 2 quiz) | ✅ |
| Modules 3 à 5 de Python | ⏳ affichés « En préparation » |
| Quiz noté sur 20, correction détaillée, historique | ✅ (note calculée en base) |
| Progression et reprise (« Reprendre ma formation ») | ✅ |
| Tableau de bord étudiant | ✅ |
| Administration, Premium, paiements | ❌ jalons suivants |

Voir [ROADMAP.md](ROADMAP.md) et [TEST_REPORT.md](TEST_REPORT.md).

## Stack

Next.js 16 (App Router, TypeScript strict) · Tailwind CSS 4 · Supabase (Auth, Postgres, RLS) · Zod · Vitest · Playwright · Netlify.

## Démarrer en local

```bash
npm ci
cp .env.example .env.local   # renseigner l'URL et la clé publishable Supabase
npm run dev                  # http://localhost:3000
```

Commandes utiles :

```bash
npm run typecheck   # TypeScript
npm run lint        # ESLint
npm test            # tests unitaires (Vitest)
npm run build       # build de production
npm run e2e         # parcours étudiant (Playwright, voir e2e/)
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — structure, données, sécurité
- [DEPLOYMENT.md](DEPLOYMENT.md) — Supabase + Netlify
- [CONTENT_GUIDELINES.md](CONTENT_GUIDELINES.md) — écrire une formation
- [CLAUDE.md](CLAUDE.md) — conventions et reprise du projet

© SMKTECH. Les attestations SMK Academy sont des attestations internes et ne constituent pas des diplômes reconnus par l'État.
