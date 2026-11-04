# Feuille de route — SMK Academy

| Jalon | Contenu | État |
|---|---|---|
| 1 | Architecture, Supabase, authentification, parcours étudiant Python (leçon → quiz /20 → progression) | ✅ code + tests SQL ; 🟡 test de bout en bout après déploiement |
| 2 | Python modules 3 à 5 (9 leçons, 3 quiz) | ✅ ; examen final ⏳ |
| 3 | Profil (modification, suppression de compte RGPD), favoris | ⏳ |
| 4 | Administration : rôles, CRUD formations / modules / leçons / quiz depuis l'interface, statistiques réelles | ⏳ |
| 5 | Formations SQL et Anglais professionnel (5 modules × 3 leçons chacune) | ⏳ |
| 6 | Offres Free / Premium configurables, accès Premium vérifié côté serveur | ⏳ |
| 7 | Stripe (mode test) : Checkout, Billing, webhooks signés et idempotents ; puis PayPal | ⏳ |
| 8 | Design Apple / Liquid Glass, thème, barre d'onglets mobile | ✅ ; PWA hors ligne, attestations PDF ⏳ |
| 9 | Audit sécurité, tests d'autorisation admin, pages légales (à valider juridiquement) | ⏳ |
| 10 | Production : SMTP, domaine, monitoring, documentation finale | ⏳ |

## Prochaines actions immédiates

1. Créer le site Netlify relié au dépôt (avec l'accord de SMKTECH) et définir les 3 variables d'environnement.
2. Renseigner Site URL / Redirect URLs dans Supabase Auth.
3. Exécuter `npm run e2e` contre le site déployé et compléter TEST_REPORT.md.
4. Examen final Python, puis profil complet (suppression de compte RGPD) et administration.
