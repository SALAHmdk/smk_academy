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

## Parcours étudiant complet contre Supabase réel

L'environnement de développement de Claude ne peut pas joindre `*.supabase.co` (liste d'accès réseau). Le parcours est donc prêt mais doit être exécuté sur le site déployé :

| Scénario | État |
|---|---|
| Création de compte + email de confirmation | 🟡 |
| Connexion / déconnexion / reconnexion | 🟡 `e2e/parcours-etudiant.spec.ts` |
| Lecture d'une leçon, correction repliable | 🟡 |
| Quiz → note /20 → correction | 🟡 (logique ✅ en SQL) |
| Récupération de la progression après reconnexion | 🟡 (logique ✅ en SQL) |
| Affichage mobile des pages connectées sur le site déployé | 🟡 (vérifié localement ✅) |
| Administration, Premium, paiements | ❌ jalons suivants |
