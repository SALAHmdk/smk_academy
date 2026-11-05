# Feuille de route — SMK Academy

| Jalon | Contenu | État |
|---|---|---|
| 1 | Architecture, Supabase, authentification, parcours étudiant Python (leçon → quiz /20 → progression) | ✅ code + tests SQL ; 🟡 test de bout en bout après déploiement |
| 2 | Python modules 3 à 5 (9 leçons, 3 quiz) | ✅ ; examen final ⏳ |
| 3 | Profil (modification, suppression de compte RGPD), favoris | ⏳ |
| 4 | Administration : rôles, CRUD formations / modules / leçons / quiz depuis l'interface, statistiques réelles, MFA TOTP obligatoire (aal2) | ✅ code + tests SQL ; 🟡 test TOTP réel en production |
| 4b | Catalogue : 10 catégories, 55 formations (1 publiée, 54 « Bientôt disponible »), recherche et filtres | ✅ |
| 5 | Formations SQL et Anglais professionnel (5 modules × 3 leçons chacune), puis JavaScript, HTML/CSS, Java… | ✅ SQL publiée ; ✅ Anglais professionnel, JavaScript, HTML/CSS rédigés et vérifiés (import automatique au prochain build) ; ⏳ Java, puis les autres |
| 6 | Offres Free / Premium configurables (0 €, 1 €/mois, 10 €/an), accès Premium vérifié en base, codes promo, accès offerts | ✅ |
| 7 | Stripe (mode test) : Checkout, portail client, webhooks signés et idempotents ; puis PayPal | ✅ code + tests ; 🟡 clés de test à configurer |
| 8 | Design Apple / Liquid Glass, thème, barre d'onglets mobile | ✅ ; PWA hors ligne, attestations PDF ⏳ |
| 9 | Audit sécurité, tests d'autorisation admin, pages légales (à valider juridiquement) | ⏳ |
| 10 | Production : SMTP, domaine, monitoring, documentation finale | ⏳ |

## Prochaines actions immédiates

1. Propriétaire : `select private.set_role('<email>', 'admin');` dans l'éditeur SQL Supabase, puis activer la double authentification sur `/compte/securite`.
2. Propriétaire : activer « Leaked password protection » dans Supabase Auth.
3. Formation SQL complète (5 modules), puis Anglais professionnel.
4. Mission sécurité : audit défensif, en-têtes CSP/HSTS, CAPTCHA, limitation de débit, documents SECURITY*.md.
