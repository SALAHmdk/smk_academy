"""Contenu de la formation « JavaScript pour débutants » (SMK Academy).

Blocs ```js pour le code, ```text pour la sortie de la console, ```solution-js pour les corrections.
Chaque bloc ```js ou ```solution-js sans manipulation du DOM est exécuté par
scripts/check_js_course.mjs, qui compare sa sortie au bloc ```text qui le suit.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("javascript_debutant_m3_m5", _Path(__file__).with_name("javascript_debutant_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "javascript-debutant",
    "title": "JavaScript pour débutants",
    "subtitle": "Le langage du web, pas à pas.",
    "description": (
        "JavaScript est le langage qui rend les pages web interactives. Cette formation part de zéro : "
        "variables, conditions, boucles, fonctions, tableaux et objets, puis manipulation d'une page web "
        "(DOM, événements, formulaires) et programmation asynchrone avec fetch. Chaque leçon propose des "
        "exemples exécutables et des exercices corrigés ; chaque module se termine par un quiz noté sur 20."
    ),
    "category": "Programmation",
    "category_slug": "programmation",
    "topic": "JavaScript",
    "cover_label": "JS",
    "level": "debutant",
    "duration_minutes": 720,
    "objectives": [
        "Maîtriser variables, conditions, boucles et fonctions",
        "Manipuler tableaux et objets",
        "Modifier une page web et réagir aux actions de l'utilisateur",
        "Comprendre l'asynchrone et récupérer des données avec fetch",
    ],
    "prerequisites": ["Savoir utiliser un navigateur web", "Notions de HTML conseillées"],
    "status": "published",
    "is_premium": False,
    "position": 12,
}

# ---------------------------------------------------------------------------
# Module 1 — Premiers pas
# ---------------------------------------------------------------------------
M1_L1 = r"""
## Qu'est-ce que JavaScript ?

Une page web repose sur trois langages complémentaires :

- **HTML** décrit le contenu (titres, paragraphes, boutons) ;
- **CSS** définit l'apparence (couleurs, mise en page) ;
- **JavaScript** ajoute le **comportement** : réagir à un clic, vérifier un formulaire, charger des données sans recharger la page.

JavaScript est exécuté directement par le navigateur : aucune installation n'est nécessaire pour commencer. Il fonctionne aussi en dehors du navigateur, grâce à **Node.js**, pour écrire des serveurs ou des outils.

> Malgré son nom, JavaScript n'a presque rien à voir avec Java. Ce sont deux langages distincts.

## Votre premier programme

Ouvrez la **console** de votre navigateur : touche `F12` (ou clic droit → *Inspecter*), puis onglet **Console**. Tapez :

```js
console.log("Bonjour, SMK Academy !");
```

```text
Bonjour, SMK Academy !
```

`console.log()` affiche une valeur dans la console. C'est l'outil n°1 pour comprendre ce que fait un programme : vous l'utiliserez tout au long de la formation.

## Où écrire du JavaScript ?

Pour des programmes de plus d'une ligne, on écrit le code dans un fichier `.js` relié à une page HTML :

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <title>Ma page</title>
  </head>
  <body>
    <h1>Bonjour</h1>
    <script src="app.js"></script>
  </body>
</html>
```

La balise `<script src="app.js">` charge le fichier `app.js`. On la place **à la fin du `<body>`** pour que la page soit construite avant que le script ne s'exécute.

Pour vous entraîner sans rien installer, vous pouvez aussi utiliser un éditeur en ligne comme **CodePen** ou **JSFiddle**, ou exécuter vos fichiers avec Node.js : `node app.js`.

## Les règles d'écriture

- Une **instruction** se termine par un point-virgule `;`. Il est techniquement facultatif dans la plupart des cas, mais nous l'écrirons toujours, par clarté.
- JavaScript **distingue les majuscules et les minuscules** : `console.log` fonctionne, `Console.Log` provoque une erreur.
- Les **commentaires** ne sont pas exécutés :

```js
// Commentaire sur une ligne
/* Commentaire
   sur plusieurs lignes */
console.log(2 + 3); // affiche 5
```

```text
5
```

## Lire un message d'erreur

```js
console.lg("test");
```

La console affiche `TypeError: console.lg is not a function`. Une erreur indique **son type**, **un message** et la **ligne** concernée : lisez-la toujours en entier, elle désigne le plus souvent le problème exact (ici, une faute de frappe).

## À retenir

- HTML = contenu, CSS = apparence, JavaScript = comportement.
- `console.log()` affiche une valeur dans la console (`F12`).
- Un script se relie à une page avec `<script src="app.js"></script>` à la fin du `<body>`.
- JavaScript distingue les majuscules ; `//` et `/* */` pour les commentaires.

## Exercices

### Exercice 1 — Affichages

Écrivez un programme qui affiche votre prénom, puis le résultat de `12 * 4`.

```solution-js
console.log("Amina");
console.log(12 * 4);
```

```text
Amina
48
```

### Exercice 2 — Trouvez les erreurs

Ce code contient deux erreurs : `Console.log("Bonjour")` et `console.log("Au revoir)`. Lesquelles ?

```solution-text
1. « Console » prend une minuscule : console.log, car JavaScript distingue les majuscules.
2. Le texte "Au revoir n'est pas fermé : il manque le guillemet final → console.log("Au revoir");
```
"""

M1_L2 = r"""
## Stocker une valeur : les variables

Une **variable** est une boîte nommée qui contient une valeur. On la déclare avec `let` ou `const` :

```js
let age = 25;
const prenom = "Sofia";
console.log(prenom, age);
```

```text
Sofia 25
```

- `const` déclare une variable qui **ne sera pas réaffectée** ;
- `let` déclare une variable dont la valeur **peut changer**.

```js
let score = 10;
score = 15;          // autorisé avec let
console.log(score);
```

```text
15
```

Avec `const`, `prenom = "Lucas"` provoquerait l'erreur `TypeError: Assignment to constant variable.`

> Règle pratique : utilisez **`const` par défaut**, et `let` seulement si la valeur doit changer. Vous rencontrerez aussi `var` dans d'anciens codes : il a des comportements surprenants, ne l'utilisez plus.

## Nommer ses variables

- Lettres, chiffres, `_` et `$`, sans commencer par un chiffre ;
- par convention, le **camelCase** : `prixTotal`, `nombreEtudiants` ;
- des noms **explicites** : `prixTtc` plutôt que `p2`.

## Les types de valeurs

| Type | Exemples | Rôle |
|---|---|---|
| `number` | `42`, `3.14`, `-7` | nombres entiers ou décimaux |
| `string` | `"Bonjour"`, `'Paris'` | texte |
| `boolean` | `true`, `false` | vrai ou faux |
| `undefined` | `undefined` | variable déclarée sans valeur |
| `null` | `null` | absence volontaire de valeur |

L'opérateur `typeof` indique le type d'une valeur :

```js
console.log(typeof 42);
console.log(typeof "42");
console.log(typeof true);
```

```text
number
string
boolean
```

Attention : `42` (nombre) et `"42"` (texte) sont deux valeurs différentes.

## Les opérateurs arithmétiques

```js
console.log(7 + 2);
console.log(7 - 2);
console.log(7 * 2);
console.log(7 / 2);
console.log(7 % 2);
console.log(2 ** 3);
```

```text
9
5
14
3.5
1
8
```

`%` donne le **reste** de la division (7 = 2 × 3 + 1), `**` la puissance. La division `/` donne toujours un résultat décimal.

Raccourcis : `score += 5` équivaut à `score = score + 5` ; `compteur++` ajoute 1.

## Le piège des nombres décimaux

```js
console.log(0.1 + 0.2);
```

```text
0.30000000000000004
```

Comme dans la plupart des langages, les décimaux sont stockés de façon approchée. Pour afficher un montant, on arrondit : `(0.1 + 0.2).toFixed(2)` donne le texte `"0.30"`.

## À retenir

- `const` par défaut, `let` si la valeur change, jamais `var`.
- Types de base : `number`, `string`, `boolean`, `undefined`, `null`.
- `typeof` donne le type ; `42` et `"42"` sont différents.
- `%` = reste, `**` = puissance ; arrondir les montants avec `toFixed`.

## Exercices

### Exercice 1 — Calcul de prix

Déclarez une constante `prixHt` valant 50 et une constante `tva` valant 0.2. Affichez le prix TTC.

```solution-js
const prixHt = 50;
const tva = 0.2;
console.log(prixHt * (1 + tva));
```

```text
60
```

### Exercice 2 — let ou const ?

Un compteur de visites démarre à 0 et augmente de 1 à chaque visite. Écrivez le code pour trois visites, puis affichez le compteur.

```solution-js
let visites = 0;   // let : la valeur change
visites++;
visites++;
visites++;
console.log(visites);
```

```text
3
```

### Exercice 3 — Pair ou impair ?

Affichez le reste de la division de 17 par 2. Que vous indique ce résultat ?

```solution-js
console.log(17 % 2);
```

```text
1
```
"""

M1_L3 = r"""
## Manipuler du texte

Une chaîne de caractères (*string*) s'écrit entre guillemets doubles `"…"`, simples `'…'` ou **accents graves** `` `…` ``.

```js
const prenom = "Karim";
console.log(prenom.length);
console.log(prenom.toUpperCase());
console.log(prenom[0]);
```

```text
5
KARIM
K
```

- `.length` donne le nombre de caractères ;
- `toUpperCase()` / `toLowerCase()` changent la casse ;
- `chaine[0]` donne le premier caractère (on compte **à partir de 0**).

## Assembler des textes

L'opérateur `+` **concatène** (met bout à bout) deux chaînes :

```js
const ville = "Lyon";
console.log("J'habite à " + ville + ".");
```

```text
J'habite à Lyon.
```

Les **gabarits** (*template literals*), entre accents graves, sont plus lisibles : on insère une valeur avec `${…}`.

```js
const nom = "Emma";
const age = 24;
console.log(`${nom} a ${age} ans.`);
console.log(`Dans 5 ans, ${nom} aura ${age + 5} ans.`);
```

```text
Emma a 24 ans.
Dans 5 ans, Emma aura 29 ans.
```

On peut placer n'importe quelle expression dans `${…}`, y compris un calcul.

## Méthodes utiles

```js
const phrase = "  Apprendre JavaScript  ";
console.log(phrase.trim());
console.log(phrase.includes("Java"));
console.log("a,b,c".split(","));
console.log("SMK".padStart(6, "*"));
```

```text
Apprendre JavaScript
true
[ 'a', 'b', 'c' ]
***SMK
```

`trim()` supprime les espaces aux extrémités, `includes()` teste la présence d'un texte, `split()` découpe en tableau (module 3).

## Le piège de `+` avec du texte

Si l'un des deux côtés est une chaîne, `+` **concatène** au lieu d'additionner :

```js
console.log(2 + 3);
console.log("2" + 3);
console.log("2" * 3);
```

```text
5
23
6
```

Les valeurs saisies dans un formulaire sont **toujours des chaînes**. Pour calculer, convertissez-les avec `Number()` :

```js
const saisie = "42";
console.log(Number(saisie) + 8);
console.log(Number("abc"));
```

```text
50
NaN
```

`NaN` (*Not a Number*) signale une conversion impossible. On le teste avec `Number.isNaN(valeur)`.

## À retenir

- `.length`, `toUpperCase()`, `trim()`, `includes()`, `split()`.
- Les positions commencent à **0**.
- Gabarits : `` `Bonjour ${prenom}` `` pour insérer des valeurs.
- `"2" + 3` donne `"23"` : convertissez avec `Number()` avant de calculer.

## Exercices

### Exercice 1 — Message de bienvenue

Avec `const prenom = "Lucas"` et `const formation = "JavaScript"`, affichez `Bienvenue Lucas dans la formation JavaScript !` à l'aide d'un gabarit.

```solution-js
const prenom = "Lucas";
const formation = "JavaScript";
console.log(`Bienvenue ${prenom} dans la formation ${formation} !`);
```

```text
Bienvenue Lucas dans la formation JavaScript !
```

### Exercice 2 — Initiales

Avec `const prenom = "sofia"` et `const nom = "rossi"`, affichez les initiales en majuscules : `SR`.

```solution-js
const prenom = "sofia";
const nom = "rossi";
console.log((prenom[0] + nom[0]).toUpperCase());
```

```text
SR
```

### Exercice 3 — Corrigez le calcul

Ce code affiche `1005` au lieu de `105`. Corrigez-le : `const quantite = "100"; console.log(quantite + 5);`

```solution-js
const quantite = "100";
console.log(Number(quantite) + 5);
```

```text
105
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Conditions et boucles
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Prendre une décision : `if`

```js
const note = 14;
if (note >= 10) {
  console.log("Module validé");
} else {
  console.log("Module à repasser");
}
```

```text
Module validé
```

La condition est écrite **entre parenthèses** ; le bloc à exécuter **entre accolades**. Le `else` est facultatif.

Plusieurs cas s'enchaînent avec `else if` ; le premier cas vrai l'emporte :

```js
const note = 17;
if (note >= 16) {
  console.log("Très bien");
} else if (note >= 10) {
  console.log("Validé");
} else {
  console.log("À retravailler");
}
```

```text
Très bien
```

## Les comparaisons

| Opérateur | Signification |
|---|---|
| `===` | strictement égal (même valeur **et** même type) |
| `!==` | strictement différent |
| `<`, `<=`, `>`, `>=` | comparaisons |

```js
console.log(5 === 5);
console.log(5 === "5");
console.log(5 == "5");
```

```text
true
false
true
```

`==` convertit les types avant de comparer, ce qui produit des résultats surprenants (`0 == ""` vaut `true`). **Utilisez toujours `===` et `!==`.**

## Combiner des conditions

- `&&` (ET) : les deux conditions doivent être vraies ;
- `||` (OU) : au moins une ;
- `!` (NON) : inverse.

```js
const age = 20;
const aUnBillet = true;
if (age >= 18 && aUnBillet) {
  console.log("Entrée autorisée");
}
```

```text
Entrée autorisée
```

## Valeurs « vraies » et « fausses »

Dans une condition, toute valeur est convertie en booléen. Sont considérées comme **fausses** (*falsy*) : `false`, `0`, `""` (chaîne vide), `null`, `undefined` et `NaN`. Toutes les autres sont **vraies** (*truthy*), y compris `"0"` et `" "`.

```js
const email = "";
if (!email) {
  console.log("Veuillez saisir un email");
}
```

```text
Veuillez saisir un email
```

## L'opérateur ternaire

Pour choisir entre deux valeurs, la forme courte `condition ? siVrai : siFaux` est pratique :

```js
const stock = 0;
const message = stock > 0 ? "En stock" : "Rupture de stock";
console.log(message);
```

```text
Rupture de stock
```

## À retenir

- `if (condition) { … } else if (…) { … } else { … }`.
- Toujours `===` et `!==`, jamais `==`.
- `&&` (et), `||` (ou), `!` (non).
- Valeurs fausses : `false`, `0`, `""`, `null`, `undefined`, `NaN`.
- `condition ? a : b` pour choisir une valeur.

## Exercices

### Exercice 1 — Tarif

Un billet coûte 12 €, 8 € pour les moins de 18 ans et les plus de 65 ans. Avec `const age = 70`, affichez le prix.

```solution-js
const age = 70;
let prix;
if (age < 18 || age > 65) {
  prix = 8;
} else {
  prix = 12;
}
console.log(`Prix : ${prix} €`);
```

```text
Prix : 8 €
```

### Exercice 2 — Prédisez

Qu'affiche ce code ? `console.log(0 === false); console.log("10" === 10); console.log(Boolean("0"));`

```solution-js
console.log(0 === false);
console.log("10" === 10);
console.log(Boolean("0"));
```

```text
false
false
true
```

### Exercice 3 — Ternaire

Avec `const heure = 15`, affichez `Bonjour` avant 18 h et `Bonsoir` ensuite, en une seule ligne.

```solution-js
const heure = 15;
console.log(heure < 18 ? "Bonjour" : "Bonsoir");
```

```text
Bonjour
```
"""

M2_L2 = r"""
## Répéter : la boucle `for`

Une **boucle** répète un bloc d'instructions. La boucle `for` est idéale quand on connaît le nombre de répétitions :

```js
for (let i = 1; i <= 3; i++) {
  console.log(`Tour ${i}`);
}
```

```text
Tour 1
Tour 2
Tour 3
```

Les trois parties entre parenthèses :

1. `let i = 1` : **initialisation**, exécutée une fois au début ;
2. `i <= 3` : **condition**, testée avant chaque tour ;
3. `i++` : **incrémentation**, exécutée après chaque tour.

## Calculer avec une boucle

```js
let total = 0;
for (let i = 1; i <= 10; i++) {
  total += i;
}
console.log(total);
```

```text
55
```

Le schéma « variable à 0, puis ajout à chaque tour » s'appelle un **accumulateur**.

## La boucle `while`

`while` répète **tant que** la condition est vraie, sans nombre de tours fixé à l'avance :

```js
let capital = 1000;
let annees = 0;
while (capital < 1500) {
  capital = capital * 1.1;
  annees++;
}
console.log(`${annees} ans`);
```

```text
5 ans
```

> Attention à la **boucle infinie** : si la condition ne devient jamais fausse, le programme ne s'arrête pas (et l'onglet du navigateur se fige). Vérifiez toujours que la boucle fait évoluer sa condition.

## Parcourir un texte ou un tableau : `for…of`

```js
const villes = ["Paris", "Lyon", "Lille"];
for (const ville of villes) {
  console.log(ville);
}
```

```text
Paris
Lyon
Lille
```

`for…of` parcourt chaque élément, sans gérer d'indice. C'est la forme la plus lisible pour parcourir une liste (module 3).

## Interrompre une boucle

- `break` sort immédiatement de la boucle ;
- `continue` passe directement au tour suivant.

```js
for (let i = 1; i <= 10; i++) {
  if (i % 2 === 0) continue;   // on saute les nombres pairs
  if (i > 7) break;            // on s'arrête après 7
  console.log(i);
}
```

```text
1
3
5
7
```

## À retenir

- `for (let i = 0; i < n; i++)` pour un nombre de tours connu.
- `while (condition)` tant qu'une condition est vraie ; attention aux boucles infinies.
- `for (const element of liste)` pour parcourir une liste.
- `break` sort de la boucle, `continue` passe au tour suivant.

## Exercices

### Exercice 1 — Table de multiplication

Affichez la table de 7, de `7 x 1 = 7` à `7 x 5 = 35`.

```solution-js
for (let i = 1; i <= 5; i++) {
  console.log(`7 x ${i} = ${7 * i}`);
}
```

```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
```

### Exercice 2 — Compte à rebours

Avec une boucle `while`, affichez 3, 2, 1, puis `Décollage !`.

```solution-js
let n = 3;
while (n > 0) {
  console.log(n);
  n--;
}
console.log("Décollage !");
```

```text
3
2
1
Décollage !
```

### Exercice 3 — Compter les voyelles

Comptez les voyelles (a, e, i, o, u, y) du mot `"javascript"` avec `for…of`.

```solution-js
let voyelles = 0;
for (const lettre of "javascript") {
  if ("aeiouy".includes(lettre)) {
    voyelles++;
  }
}
console.log(voyelles);
```

```text
3
```
"""

M2_L3 = r"""
## Choisir parmi plusieurs valeurs : `switch`

Quand une même variable est comparée à plusieurs valeurs précises, `switch` est plus lisible qu'une suite de `else if` :

```js
const jour = "samedi";
switch (jour) {
  case "samedi":
  case "dimanche":
    console.log("Week-end");
    break;
  case "mercredi":
    console.log("Milieu de semaine");
    break;
  default:
    console.log("Jour ouvré");
}
```

```text
Week-end
```

- `switch` compare avec `===` ;
- chaque `case` se termine par `break`, sinon l'exécution **continue** dans le cas suivant ;
- deux `case` consécutifs sans instruction partagent le même bloc (ici samedi et dimanche) ;
- `default` traite tous les autres cas.

## Mettre en pratique : un petit programme complet

Combinons variables, conditions et boucles pour analyser une liste de notes.

```js
const notes = [12, 8, 15, 19, 10, 6];
let somme = 0;
let validees = 0;
let meilleure = notes[0];

for (const note of notes) {
  somme += note;
  if (note >= 10) validees++;
  if (note > meilleure) meilleure = note;
}

const moyenne = somme / notes.length;
console.log(`Moyenne : ${moyenne.toFixed(1)}`);
console.log(`Notes validées : ${validees} sur ${notes.length}`);
console.log(`Meilleure note : ${meilleure}`);
```

```text
Moyenne : 11.7
Notes validées : 4 sur 6
Meilleure note : 19
```

Ce programme suit une démarche que vous réutiliserez souvent :

1. **préparer** les variables (accumulateurs, valeur de référence) ;
2. **parcourir** les données une fois ;
3. **calculer et afficher** le résultat.

## Déboguer une boucle

Quand une boucle ne donne pas le résultat attendu, affichez l'état des variables à chaque tour :

```js
let total = 0;
for (let i = 1; i <= 3; i++) {
  total += i;
  console.log(`i = ${i}, total = ${total}`);
}
```

```text
i = 1, total = 1
i = 2, total = 3
i = 3, total = 6
```

Les **outils de développement** du navigateur proposent aussi un débogueur : en ajoutant l'instruction `debugger;` dans le code, l'exécution s'arrête à cet endroit et vous pouvez examiner chaque variable (onglet *Sources*).

## Erreurs fréquentes

- `if (note = 10)` : un seul `=` **affecte** la valeur au lieu de comparer. Écrivez `===`.
- Oublier les accolades : sans `{ }`, seule la première instruction dépend du `if`.
- Boucle décalée d'un tour : `i < notes.length` parcourt toutes les positions de `0` à `length - 1` ; `i <= notes.length` va une case trop loin.

## À retenir

- `switch` pour comparer une valeur à plusieurs cas ; `break` à la fin de chaque cas.
- Démarche : préparer → parcourir → calculer.
- Afficher les variables dans la boucle, ou utiliser `debugger;`.
- `=` affecte, `===` compare.

## Exercices

### Exercice 1 — Nom du mois

Écrivez un `switch` qui affiche le nom du mois à partir de son numéro (1, 2 ou 3), et `Autre mois` pour toute autre valeur. Testez avec `const mois = 2`.

```solution-js
const mois = 2;
switch (mois) {
  case 1:
    console.log("Janvier");
    break;
  case 2:
    console.log("Février");
    break;
  case 3:
    console.log("Mars");
    break;
  default:
    console.log("Autre mois");
}
```

```text
Février
```

### Exercice 2 — Statistiques de températures

Avec `const temperatures = [18, 22, 25, 19, 30, 27]`, affichez la température minimale et le nombre de jours à 25 °C ou plus.

```solution-js
const temperatures = [18, 22, 25, 19, 30, 27];
let minimum = temperatures[0];
let joursChauds = 0;
for (const t of temperatures) {
  if (t < minimum) minimum = t;
  if (t >= 25) joursChauds++;
}
console.log(`Minimum : ${minimum}`);
console.log(`Jours chauds : ${joursChauds}`);
```

```text
Minimum : 18
Jours chauds : 3
```
"""

QUIZ_M1 = [
    ("single", "Quel rôle joue JavaScript dans une page web ?", None,
     ["Décrire le contenu", "Définir les couleurs et la mise en page", "Ajouter le comportement et l'interactivité", "Héberger le site"], [2],
     "HTML décrit le contenu, CSS l'apparence, JavaScript le comportement (réagir aux actions, charger des données…)."),
    ("single", "Que fait console.log(\"Bonjour\") ?", None,
     ["Affiche une fenêtre d'alerte", "Affiche « Bonjour » dans la console", "Écrit dans la page HTML", "Enregistre un fichier"], [1],
     "console.log affiche une valeur dans la console des outils de développement."),
    ("single", "Quelle déclaration choisir pour une valeur qui ne sera jamais réaffectée ?", None,
     ["var", "let", "const", "static"], [2],
     "const déclare une variable qui ne peut pas être réaffectée. On l'utilise par défaut."),
    ("single", "Que vaut typeof \"42\" ?", None,
     ["\"number\"", "\"string\"", "\"boolean\"", "\"undefined\""], [1],
     "Les guillemets font de 42 une chaîne de caractères : typeof renvoie \"string\"."),
    ("single", "Que vaut 17 % 5 ?", None,
     ["3.4", "2", "3", "12"], [1],
     "% donne le reste de la division : 17 = 5 × 3 + 2."),
    ("single", "Qu'affiche console.log(\"2\" + 3) ?", None,
     ["5", "\"23\" (la chaîne 23)", "NaN", "Une erreur"], [1],
     "Si l'un des opérandes est une chaîne, + concatène : \"2\" + 3 donne \"23\"."),
    ("single", "Qu'affiche ce code ?", "const nom = \"Emma\";\nconsole.log(`Bonjour ${nom} !`);",
     ["Bonjour ${nom} !", "Bonjour Emma !", "Bonjour nom !", "Une erreur"], [1],
     "Entre accents graves, ${…} insère la valeur de l'expression : Bonjour Emma !"),
    ("single", "Que vaut \"JavaScript\"[0] ?", None,
     ["\"J\"", "\"a\"", "undefined", "\"JavaScript\""], [0],
     "Les positions commencent à 0 : le premier caractère est \"J\"."),
    ("multiple", "Quelles affirmations sont exactes ?", None,
     ["JavaScript distingue les majuscules et les minuscules.", "Number(\"abc\") renvoie NaN.", "let et const sont équivalents en tout point.", "// commence un commentaire sur une ligne."], [0, 1, 3],
     "let permet la réaffectation, contrairement à const : ils ne sont pas équivalents. Les trois autres affirmations sont exactes."),
    ("true_false", "Java et JavaScript sont deux noms du même langage.", None,
     ["Vrai", "Faux"], [1],
     "Ce sont deux langages différents, malgré la ressemblance des noms."),
]

QUIZ_M2 = [
    ("single", "Que vaut 5 === \"5\" ?", None,
     ["true", "false", "undefined", "Une erreur"], [1],
     "=== compare la valeur et le type : un nombre n'est pas strictement égal à une chaîne."),
    ("single", "Pourquoi préférer === à == ?", None,
     ["=== est plus rapide à écrire", "== convertit les types avant de comparer, ce qui produit des résultats surprenants", "== n'existe pas en JavaScript", "=== fonctionne seulement avec les nombres"], [1],
     "== convertit les types (0 == \"\" vaut true) ; === compare sans conversion, de façon prévisible."),
    ("multiple", "Quelles valeurs sont « fausses » (falsy) dans une condition ?", None,
     ["0", "\"\" (chaîne vide)", "\"0\"", "null"], [0, 1, 3],
     "0, \"\", null, undefined, NaN et false sont falsy. La chaîne \"0\" n'est pas vide : elle est truthy."),
    ("single", "Qu'affiche ce code ?", "const a = 4;\nconsole.log(a > 5 ? \"grand\" : \"petit\");",
     ["grand", "petit", "true", "false"], [1],
     "4 > 5 est faux : l'opérateur ternaire renvoie la seconde valeur, \"petit\"."),
    ("single", "Combien de fois cette boucle affiche-t-elle un message ?", "for (let i = 0; i < 4; i++) {\n  console.log(i);\n}",
     ["3", "4", "5", "Infiniment"], [1],
     "i prend les valeurs 0, 1, 2 et 3 : 4 affichages. La boucle s'arrête quand i vaut 4."),
    ("single", "Que vaut total à la fin ?", "let total = 0;\nfor (let i = 1; i <= 4; i++) {\n  total += i;\n}",
     ["4", "6", "10", "24"], [2],
     "1 + 2 + 3 + 4 = 10."),
    ("single", "Que fait l'instruction break dans une boucle ?", None,
     ["Passe au tour suivant", "Sort immédiatement de la boucle", "Recommence la boucle", "Provoque une erreur"], [1],
     "break interrompt la boucle ; continue passe au tour suivant."),
    ("single", "Quel est le risque de ce code ?", "let n = 1;\nwhile (n > 0) {\n  n++;\n}",
     ["Aucun", "Une boucle infinie", "Une erreur de syntaxe", "La boucle ne s'exécute jamais"], [1],
     "n augmente sans cesse et reste supérieur à 0 : la condition ne devient jamais fausse."),
    ("single", "Dans un switch, que se passe-t-il si l'on oublie break à la fin d'un case ?", None,
     ["Une erreur est levée", "L'exécution continue dans le case suivant", "Le switch s'arrête", "Le default est ignoré"], [1],
     "Sans break, l'exécution « tombe » dans le cas suivant. C'est voulu seulement quand plusieurs cas partagent un même bloc."),
    ("single", "Quelle condition est correcte pour tester si note vaut 10 ?", None,
     ["if (note = 10)", "if (note === 10)", "if note === 10", "if (note => 10)"], [1],
     "Un seul = affecte la valeur ; il faut === entre parenthèses. => sert à écrire des fonctions fléchées."),
]

MODULES = [
    {
        "position": 1,
        "title": "Premiers pas",
        "description": "Exécuter du JavaScript, utiliser variables, types, opérateurs et chaînes de caractères.",
        "status": "published",
        "lessons": [
            ("decouvrir-javascript", "Découvrir JavaScript",
             "Le rôle de JavaScript, la console, relier un script à une page.", M1_L1, 20),
            ("variables-types", "Variables et types",
             "let, const, nombres, chaînes, booléens et opérateurs.", M1_L2, 30),
            ("chaines", "Travailler avec le texte",
             "Méthodes des chaînes, gabarits et conversions.", M1_L3, 30),
        ],
        "quiz": ("Quiz — Premiers pas", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Conditions et boucles",
        "description": "Prendre des décisions, répéter des instructions et structurer un programme.",
        "status": "published",
        "lessons": [
            ("conditions", "Les conditions",
             "if, else, comparaisons strictes, opérateurs logiques et ternaire.", M2_L1, 30),
            ("boucles", "Les boucles",
             "for, while, for…of, break et continue.", M2_L2, 30),
            ("switch-et-programme", "switch et premier programme complet",
             "Choisir parmi plusieurs cas, analyser des données, déboguer.", M2_L3, 30),
        ],
        "quiz": ("Quiz — Conditions et boucles", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Fonctions, tableaux et objets",
        "description": "Écrire des fonctions réutilisables et organiser les données.",
        "status": "published",
        "lessons": [
            ("fonctions", "Les fonctions",
             "Déclarer, appeler, paramètres, valeur de retour et fonctions fléchées.", _m35.M3_L1, 35),
            ("tableaux", "Les tableaux",
             "Créer, modifier et parcourir une liste ; map, filter, find, reduce.", _m35.M3_L2, 35),
            ("objets", "Les objets",
             "Propriétés, méthodes, tableaux d'objets et JSON.", _m35.M3_L3, 35),
        ],
        "quiz": ("Quiz — Fonctions, tableaux et objets", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Manipuler une page web",
        "description": "Lire et modifier le DOM, réagir aux événements, gérer un formulaire.",
        "status": "published",
        "lessons": [
            ("dom", "Le DOM",
             "Sélectionner des éléments, modifier texte, classes et styles.", _m35.M4_L1, 30),
            ("evenements", "Les événements",
             "addEventListener, clic, saisie, création d'éléments.", _m35.M4_L2, 30),
            ("formulaires", "Les formulaires",
             "Lire les champs, valider, empêcher l'envoi, afficher les erreurs.", _m35.M4_L3, 35),
        ],
        "quiz": ("Quiz — Manipuler une page web", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "L'asynchrone et fetch",
        "description": "Comprendre l'asynchrone, utiliser les promesses, async/await et fetch, puis mini-projet.",
        "status": "published",
        "lessons": [
            ("asynchrone", "Comprendre l'asynchrone",
             "setTimeout, file d'attente et promesses.", _m35.M5_L1, 30),
            ("async-await-fetch", "async/await et fetch",
             "Récupérer des données JSON et gérer les erreurs.", _m35.M5_L2, 35),
            ("mini-projet", "Mini-projet : liste de tâches",
             "Une application complète : DOM, événements, tableaux et stockage local.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — L'asynchrone et fetch", _m35.QUIZ_M5),
    },
]
