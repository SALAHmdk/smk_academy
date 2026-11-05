# React — rapport de rédaction

- Modules / leçons / questions : 5 / 15 / 50 (durée cumulée des leçons : 660 min pour 720 annoncées)
- Code exécuté : 31 blocs `js` / `solution-js` vérifiés par `check_code_blocks.py`, 0 avertissement, 0 échec.
  `validate_course.py` : OK.
- Non exécutable par le contrôle automatique : 102 blocs `jsx` / `solution-jsx` (composants), plus des blocs `bash`
  (commandes Vite/npm), `css`, `html` et `text`. Les blocs JSX ont été vérifiés pendant la rédaction, hors dépôt :
  - ESLint avec `eslint-plugin-react-hooks` (rules-of-hooks, exhaustive-deps) et `eslint-plugin-react` (jsx-key,
    jsx-no-undef) + `no-undef` : aucun problème dans les composants complets. Les seuls signalements portent sur
    des fragments volontaires (extraits de 2 à 5 lignes, deux fichiers juxtaposés, exemples de bugs à corriger
    dans les exercices : clé manquante, `useEffect(async …)`, boucle infinie, JSX sans racine).
  - Transpilation `tsc --jsx react-jsx` puis rendu `react-dom/server` (React 19.3 du dépôt) des 67 composants
    autonomes : 64 rendus sans erreur ni avertissement de clé ; les 3 autres sont attendus (bloc de bug volontaire,
    deux composants rendus sans leurs props obligatoires). Le HTML affiché dans « Composants et props » est
    identique au rendu réel ; le piège `{0 && …}` qui affiche « 0 » a été confirmé.
  - Les effets, gestionnaires et appels réseau n'ont pas été exécutés dans un navigateur (pas de DOM ici).
- Points d'attention pour la relecture :
  - Commande `npm create vite@latest mon-app -- --template react`, port 5173 « le plus souvent » et structure du
    projet : présentés comme susceptibles d'évoluer avec Vite (dit explicitement dans la leçon).
  - Le contexte est fourni avec `<Ctx.Provider value>`, forme valable dans toutes les versions récentes ; la
    syntaxe plus courte des versions récentes n'est volontairement pas présentée.
  - `toSorted` (ES2023) est utilisé dans deux leçons, avec la mention de l'alternative `[...t].sort()`.
  - L'API publique JSONPlaceholder (`jsonplaceholder.typicode.com`, données fictives) est utilisée pour les
    exemples réseau et le mini-projet ; si elle devenait indisponible, l'état d'erreur du projet s'afficherait.
  - Longueur : M5_L1 (11 185 caractères) et le mini-projet M5_L3 (13 246) dépassent légèrement la cible de
    11 000 caractères (le validateur accepte jusqu'à 16 000) ; le mini-projet contient tout le code de l'application.
  - Les nombres d'habitants (leçon sur les listes) sont signalés comme arrondis et illustratifs ; noms de livres,
    auteurs, délais de livraison et personnes sont fictifs.
