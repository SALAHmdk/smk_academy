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

## Restant à tester

| Scénario | État |
|---|---|
| Inscription par le formulaire + clic sur l'email de confirmation | 🟡 à faire avec une vraie boîte mail (liens désormais construits depuis l'origine du site) |
| Mot de passe oublié (email) | 🟡 idem |
| Affichage téléphone en production | 🟡 vérifié en local (Chrome 393 px) ✅ ; fenêtre du navigateur réel non redimensionnable pendant le test |
| Administration, Premium, paiements | ❌ jalons suivants |
