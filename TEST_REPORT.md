# Rapport de tests — jalons 1 et 2 (04/11/2026)

Légende : ✅ exécuté et réussi · 🟡 préparé, pas encore exécuté · ❌ non couvert

## Base de données (exécutés sur `smk-academy-dev`, transaction annulée)

`supabase/tests/security_and_grading.sql` — **24/24 réussis** :

| Vérification | Résultat |
|---|---|
| Profil créé automatiquement avec le rôle `student` | ✅ |
| Corrigés (`private.quiz_answer_keys`) inaccessibles à un étudiant | ✅ |
| Impossible de se donner le rôle `admin` | ✅ |
| Impossible de s'attribuer l'offre Premium | ✅ |
| Modification de son nom autorisée | ✅ |
| Insertion directe d'une note 20/20 refusée | ✅ |
| Options du quiz lisibles (36) | ✅ |
| Toutes bonnes réponses → 20/20, validé | ✅ |
| Moitié juste → 10/20, validé (seuil 10) | ✅ |
| Copie vide → 0/20, non validé | ✅ |
| Cocher toutes les options d'un QCM → 0/20 | ✅ |
| Réponses forgées (identifiants inventés ou d'une autre question) ignorées | ✅ |
| Format de réponses invalide rejeté | ✅ |
| Correction détaillée (10 questions + explications) | ✅ |
| Leçon terminée enregistrée, idempotente | ✅ |
| Inscription + dernière leçon mémorisées | ✅ |
| Historique des tentatives | ✅ |
| Un étudiant B ne voit ni les notes, ni la progression, ni le profil de A | ✅ ✅ ✅ |
| Visiteur : catalogue et plan visibles, leçons et quiz refusés | ✅ ✅ ✅ ✅ |

Intégrité du contenu : empreintes MD5 des **15 leçons** identiques entre le dépôt et la base ✅.
Contenu : 5 modules publiés × 3 leçons, 5 quiz × 10 questions, 50 corrigés en base ✅.
Notation des 5 quiz avec toutes les bonnes réponses : 20/20 pour chacun ✅.
Code pédagogique des modules 3 à 5 : les **75 blocs** (exemples + corrections) exécutés avec Python 3 sans erreur inattendue ✅ (saisies simulées ; les blocs qui illustrent volontairement une erreur la produisent bien).
Advisor sécurité Supabase : seules alertes = les 4 RPC volontairement ouvertes aux connectés + `rls_auto_enable` (déclencheur d'événement Supabase, non appelable via l'API).

## Application

| Vérification | Résultat |
|---|---|
| `tsc --noEmit` (TypeScript strict, client Supabase typé) | ✅ |
| ESLint | ✅ |
| Vitest — 14 tests (formatage, moyenne, ordre des leçons, validation Zod, anti-redirection ouverte, rendu Markdown, blocage du HTML brut) | ✅ |
| `next build` production (17 routes + proxy) | ✅ |
| Redirection vers /connexion : tableau de bord, leçons, résultats | ✅ |
| 404 personnalisée | ✅ |
| En-têtes de sécurité | ✅ |
| Captures Chrome headless 393 px et 1366 px, clair et sombre : accueil, catalogue, formation, inscription, connexion — **aucun débordement horizontal** | ✅ (API Supabase simulée localement avec le vrai contenu) |
| Pages connectées (tableau de bord, formation, leçon, quiz, résultat, compte) en 393 px et 1366 px, clair et sombre, avec une session simulée | ✅ aucun débordement ; barre d'onglets et barre de validation du quiz vérifiées |
| Flou « Liquid Glass » effectivement appliqué (style calculé `backdrop-filter`) | ✅ après correction de l'ordre des déclarations |

## Parcours étudiant complet en production (exécuté le 04/11/2026, 20:55)

Site : https://smk-academy.netlify.app (déploiement `fa4c477`), Supabase `smk-academy-dev`, navigateur Chrome réel.
Compte de test dédié : `e2e@smktech.test` (email confirmé créé directement en base, mot de passe non versionné).

| Scénario | Résultat |
|---|---|
| Accès au tableau de bord sans session → redirection vers /connexion | ✅ |
| Connexion (mot de passe) → tableau de bord vide, profil créé automatiquement | ✅ |
| Page formation : 5 modules ouverts sur 5, durée 11 h | ✅ |
| « Commencer la formation » → inscription + ouverture de la leçon 1 | ✅ |
| Lecture de la leçon, correction d'exercice repliable | ✅ |
| « Terminer et continuer » → leçon 1 cochée, leçon 2 ouverte | ✅ |
| Quiz module 1 : aucun corrigé présent dans le HTML avant soumission | ✅ |
| 9 bonnes réponses sur 10 → **18/20**, « Module validé » | ✅ |
| Correction détaillée : Q9 à 0/2 avec explication, les 9 autres à 2/2 | ✅ |
| Fraude via l'API avec la session de l'étudiant : insérer un 20/20, modifier ou supprimer sa note, devenir admin, passer Premium | ✅ toutes refusées (403) |
| Lecture des corrigés via l'API | ✅ table inexistante côté API (404) |
| Un étudiant ne voit que ses propres tentatives | ✅ |
| Thème sombre puis automatique depuis « Mon compte » | ✅ |
| Déconnexion → espace privé de nouveau inaccessible | ✅ |
| Reconnexion → moyenne 18/20, 1 leçon terminée, 1/15, « Prochaine étape : Variables et types de base », historique daté (heure de Paris) | ✅ |

## Catalogue et administration (04/11/2026, soir)

| Test | Type | Résultat |
|---|---|---|
| `supabase/tests/security_and_grading.sql` après migrations catalogue | exécuté (SQL, transaction annulée) | ✅ 24/24 |
| `supabase/tests/admin_security.sql` : étudiant refusé, admin en aal1 refusé, admin aal2 autorisé, formation/module vides non publiables, question sans corrigé bloquée, validation des corrigés, journal d'audit, brouillons invisibles des étudiants et visiteurs | exécuté (SQL, transaction annulée) | ✅ 18/18 |
| Typecheck, lint, 16 tests unitaires (dont filtres du catalogue), build | exécuté | ✅ |
| Écrans `/admin`, fiche formation, nouvelle formation, éditeur de quiz (desktop, API simulée) | exécuté (captures locales) | ✅ aucun débordement |
| Enrôlement TOTP réel avec Google/Microsoft Authenticator puis accès `/admin` en production | préparé | 🟡 à faire par le propriétaire (rôle admin à attribuer) |

## Offres, codes promo, accès offerts, paiements (04/11/2026, 22 h)

| Test | Type | Résultat |
|---|---|---|
| `supabase/tests/premium_security.sql` : prix en lecture seule hors admin aal2, auto-attribution Premium / faux abonnement / création de code refusés, leçons Premium invisibles en Free, codes personnels réservés, usage unique, cumul des mois, blocage après 10 échecs, accès illimité puis révocation, webhook : faux jeton refusé, idempotence, paiement réel refusé, paiements d'autrui invisibles | exécuté (SQL, transaction annulée) | ✅ 34/34 |
| Non-régression `security_and_grading.sql` après contrôle Premium | exécuté | ✅ 24/24 |
| Bug détecté par les tests : journal d'audit des offres (identifiant texte) → migration `20261104221000_fix_plans_audit.sql` | exécuté | ✅ corrigé |
| Vérification de signature Stripe (valide, contenu modifié, autre clé, rejeu > 5 min, en-tête absent, rotation), refus des clés `sk_live_`, encodage Stripe, formats de prix | exécuté (Vitest) | ✅ 27/27 au total |
| Écrans Tarifs, Abonnement, admin Offres / Codes promo / Accès / Paiements (mobile, desktop, sombre, API simulée) | exécuté (captures) | ✅ aucun débordement |
| Paiement Stripe Checkout réel en mode test (carte 4242…), webhook reçu, Premium activé, résiliation via le portail | préparé | 🟡 après configuration des clés de test |

## Formation « SQL pour débutants » (05/11/2026)

| Test | Type | Résultat |
|---|---|---|
| `scripts/check_sql_course.py` : exécution des 110 blocs SQL des leçons et corrections sur la base d'exemple (SQLite) | exécuté | ✅ 103 exécutés, 7 échecs attendus (exemples d'erreurs, syntaxes propres à un SGBD), 0 inattendu |
| Résultats affichés dans les leçons recalculés par exécution réelle des requêtes | exécuté | ✅ |
| Contenu en base identique à la source : empreintes MD5 des leçons, résumés, questions, options, explications et positions des bonnes réponses, 5 modules | exécuté | ✅ 30/30 |
| Notation des 5 quiz : bonnes réponses → 20/20, copie vide → 0/20 ; 15 leçons lisibles après inscription | exécuté (SQL, transaction annulée) | ✅ |
| Parcours complet dans le navigateur sur le site Netlify | préparé | 🟡 |

## Formations Anglais professionnel, JavaScript, HTML/CSS et import automatique (05/11/2026)

| Test | Type | Résultat |
|---|---|---|
| `check_js_course.mjs` : 81 exemples JavaScript exécutés avec Node, sortie identique à la leçon ; 26 blocs DOM/réseau vérifiés en syntaxe | exécuté | ✅ (2 erreurs réelles trouvées puis corrigées : identifiants `Date.now()` en double, format d'affichage) |
| `check_web_course.mjs` : 79 blocs HTML (imbrication) et CSS (Lightning CSS + accolades) ; détection d'erreurs vérifiée sur un exemple cassé | exécuté | ✅ |
| Anglais professionnel : relecture des exemples et des corrigés | relu | ✅ |
| RPC `content_import_if_changed` : faux jeton refusé, import sans session (rôle anon) avec publication et corrigés, second import ignoré (« inchangée ») | exécuté (SQL, transaction annulée) | ✅ |
| Import réel au build Netlify | préparé | 🟡 en attente de la variable `CONTENT_IMPORT_TOKEN` |

## Restant à tester

| Scénario | État |
|---|---|
| Inscription par le formulaire + clic sur l'email de confirmation | 🟡 à faire avec une vraie boîte mail (liens désormais construits depuis l'origine du site) |
| Mot de passe oublié (email) | 🟡 idem |
| Affichage téléphone en production | 🟡 vérifié en local (Chrome 393 px) ✅ ; fenêtre du navigateur réel non redimensionnable pendant le test |
| Administration, Premium, paiements | ❌ jalons suivants |
