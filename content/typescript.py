"""Contenu de la formation « TypeScript » (SMK Academy).

Blocs ```ts pour le code, ```text pour la sortie de la console (ou le message exact de tsc),
```solution-ts pour les corrections. scripts/check_code_blocks.py compile chaque bloc ```ts avec
`tsc --strict` puis l'exécute avec Node.js ; un bloc ```text qui suit un exemple d'erreur volontaire
contient le message produit par tsc (sans le nom de fichier ni la position, qui dépendent de l'éditeur).
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("typescript_m3_m5", _Path(__file__).with_name("typescript_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "typescript",
    "title": "TypeScript",
    "subtitle": "Ajouter des types sûrs à JavaScript.",
    "description": (
        "TypeScript ajoute à JavaScript un système de types vérifié avant l'exécution : de nombreuses erreurs "
        "sont détectées dès l'écriture du code, et l'éditeur devient un véritable assistant. Cette formation "
        "part de JavaScript que vous connaissez déjà pour typer variables, fonctions et objets, utiliser unions, "
        "interfaces, classes et génériques, puis configurer un vrai projet avec tsconfig.json. Chaque leçon "
        "propose des exemples compilés et exécutés, des erreurs de typage commentées et des exercices corrigés ; "
        "un mini-projet typé conclut la formation."
    ),
    "category": "Programmation",
    "category_slug": "programmation",
    "topic": "TypeScript",
    "cover_label": "TS",
    "level": "intermediaire",
    "duration_minutes": 480,
    "objectives": [
        "Typer variables, fonctions et objets",
        "Utiliser interfaces et génériques",
        "Configurer un projet TypeScript",
    ],
    "prerequisites": ["JavaScript pour débutants"],
    "status": "published",
    "is_premium": False,
    "position": 13,
}

# ---------------------------------------------------------------------------
# Module 1 — Pourquoi TypeScript et types de base
# ---------------------------------------------------------------------------
M1_L1 = r"""
## JavaScript… avec des types

**TypeScript** est un langage créé par Microsoft qui **étend JavaScript** : tout programme JavaScript valide est (presque toujours) un programme TypeScript valide, auquel on ajoute des **annotations de type**.

```ts
const prixHt: number = 50;
const tva: number = 0.2;
console.log(prixHt * (1 + tva));
```

```text
60
```

Le `: number` après le nom de la variable est une **annotation** : elle indique que la variable contient un nombre. Retirez les annotations et vous retrouvez exactement le JavaScript du cours précédent.

> On dit que TypeScript est un **sur-ensemble** (*superset*) de JavaScript : il ne remplace pas JavaScript, il s'ajoute par-dessus.

## Pourquoi ajouter des types ?

En JavaScript, beaucoup d'erreurs ne se révèlent **qu'à l'exécution**, parfois chez l'utilisateur :

```js
function prixTtc(prixHt) {
  return prixHt * 1.2;
}
console.log(prixTtc("50 €"));
```

```text
NaN
```

Le programme ne plante même pas : il affiche `NaN` et l'erreur passe inaperçue. En TypeScript, on précise que le paramètre est un nombre :

```ts
function prixTtc(prixHt: number): number {
  return prixHt * 1.2;
}
console.log(prixTtc("50 €"));
```

```text
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

L'erreur est signalée **avant** l'exécution, par le compilateur et directement dans l'éditeur (soulignement rouge). Les bénéfices :

| Bénéfice | Concrètement |
|---|---|
| Détection précoce | fautes de frappe, arguments inversés, valeurs `undefined` oubliées |
| Autocomplétion | l'éditeur connaît les propriétés de chaque objet |
| Documentation vivante | la signature d'une fonction dit ce qu'elle attend et renvoie |
| Refactorisation sûre | renommer une propriété signale tous les endroits à corriger |

## Comment ça marche : la compilation

Les navigateurs et Node.js exécutent du **JavaScript**. Le compilateur TypeScript, la commande `tsc`, fait deux choses :

1. il **vérifie les types** et affiche les erreurs ;
2. il **produit un fichier `.js`** en retirant les annotations (on parle d'**effacement des types**, *type erasure*).

```bash
npm install --save-dev typescript   # installe tsc dans le projet
npx tsc --version                   # affiche la version installée
npx tsc bonjour.ts                  # vérifie et produit bonjour.js
node bonjour.js                     # exécute le JavaScript produit
```

Le fichier `bonjour.ts` suivant…

```ts
const prenom: string = "Amina";
const message: string = `Bonjour ${prenom} !`;
console.log(message);
```

```text
Bonjour Amina !
```

… devient, après compilation, du JavaScript ordinaire : `const prenom = "Amina";` et ainsi de suite, sans les `: string`.

> Conséquence importante : **les types n'existent plus à l'exécution**. Ils servent uniquement à la vérification. Une donnée reçue d'un serveur ou saisie par l'utilisateur doit donc toujours être contrôlée par du vrai code JavaScript (module 2).

## Lire un message d'erreur de tsc

Un message de `tsc` ressemble à ceci :

```text
bonjour.ts(2,7): error TS2322: Type 'number' is not assignable to type 'string'.
```

- `bonjour.ts(2,7)` : le **fichier**, la **ligne** et la **colonne** ;
- `TS2322` : le **code** de l'erreur, utile pour chercher de l'aide ;
- la fin est le **message**, en anglais : « le type `number` ne peut pas être affecté au type `string` ».

Dans cette formation, nous reproduisons le message exact de `tsc` à partir de `error TS…` ; le nom du fichier et la position dépendent de votre projet. Voici le code qui produit l'erreur ci-dessus :

```ts
let ville: string = "Lyon";
ville = 69;
```

```text
error TS2322: Type 'number' is not assignable to type 'string'.
```

Vocabulaire utile pour lire les messages : *assignable* (affectable), *type* (type), *property* (propriété), *does not exist on type* (n'existe pas sur le type), *possibly 'undefined'* (peut-être `undefined`).

> Par défaut, `tsc` produit quand même le fichier `.js` malgré les erreurs de type. Une erreur de type n'est donc pas un « plantage » : c'est un **avertissement sérieux** qu'il faut corriger. L'option `noEmitOnError` (module 5) bloque la production du `.js` tant qu'il reste des erreurs.

## Où pratiquer ?

- Le **TypeScript Playground**, sur le site officiel de TypeScript : on tape du code à gauche, on voit le JavaScript produit et les erreurs, sans rien installer.
- Un éditeur comme **Visual Studio Code**, qui comprend TypeScript nativement.
- En ligne de commande avec Node.js et `tsc`, comme ci-dessus.

## À retenir

- TypeScript = JavaScript + annotations de type vérifiées **avant** l'exécution.
- `tsc` vérifie les types puis produit du JavaScript en effaçant les annotations.
- Les types n'existent plus à l'exécution : les données externes doivent toujours être vérifiées.
- Un message `fichier.ts(ligne,colonne): error TSxxxx: …` se lit en entier : il désigne le problème exact.

## Exercices

### Exercice 1 — Annoter

Réécrivez ce code JavaScript en ajoutant les annotations de type : `const quantite = 3; const prixUnitaire = 4.5; console.log(quantite * prixUnitaire);`

```solution-ts
const quantite: number = 3;
const prixUnitaire: number = 4.5;
console.log(quantite * prixUnitaire);
```

```text
13.5
```

### Exercice 2 — Lire une erreur

Que signifie `app.ts(8,3): error TS2322: Type 'boolean' is not assignable to type 'number'.` ?

```solution-text
Dans le fichier app.ts, ligne 8, colonne 3, on essaie de placer une valeur booléenne (true ou false)
dans une variable ou une propriété déclarée de type number. Il faut soit corriger la valeur,
soit revoir le type déclaré.
```

### Exercice 3 — Vrai ou faux ?

« Comme mon code TypeScript compile sans erreur, une valeur reçue d'une API aura forcément le type que j'ai déclaré. »

```solution-text
Faux. Les types sont effacés à la compilation : à l'exécution, rien ne vérifie automatiquement
qu'une réponse d'API respecte le type déclaré. Il faut la contrôler avec du code (typeof, tests de
propriétés…), comme nous le verrons au module 2.
```
"""

M1_L2 = r"""
## Les types primitifs

Les trois types les plus utilisés correspondent aux valeurs de base de JavaScript :

| Type | Exemples |
|---|---|
| `string` | `"Bonjour"`, `'Paris'`, `` `Total : ${n}` `` |
| `number` | `42`, `3.14`, `-7` (entiers et décimaux) |
| `boolean` | `true`, `false` |

```ts
const formation: string = "TypeScript";
const dureeHeures: number = 8;
const estPubliee: boolean = true;
console.log(formation, dureeHeures, estPubliee);
```

```text
TypeScript 8 true
```

> Les noms de types s'écrivent en **minuscules** : `string`, `number`, `boolean`. Les versions avec majuscule (`String`, `Number`) désignent des objets enveloppes qu'il ne faut pas utiliser comme types.

## L'inférence : TypeScript devine le type

Il est rarement nécessaire d'annoter une variable initialisée : TypeScript **infère** (déduit) son type à partir de la valeur.

```ts
let compteur = 0;      // inféré : number
compteur = compteur + 1;
console.log(compteur);
```

```text
1
```

L'inférence est aussi stricte qu'une annotation :

```ts
let compteur = 0;
compteur = "un";
```

```text
error TS2322: Type 'string' is not assignable to type 'number'.
```

Avec `const`, le type inféré est encore plus précis : `const ville = "Lyon"` a pour type le **littéral** `"Lyon"` (la valeur ne peut pas changer). Nous y reviendrons à la leçon suivante.

> Bonne pratique : laissez l'inférence travailler pour les variables locales, et **annotez les paramètres et les valeurs de retour des fonctions** (module 2). C'est là que les annotations apportent le plus.

## Déclarer sans initialiser

Une variable déclarée sans valeur doit être annotée. TypeScript vérifie ensuite qu'elle est **affectée avant d'être lue** :

```ts
let mention: string;
const note = 14;
if (note >= 10) {
  mention = "Validé";
} else {
  mention = "À repasser";
}
console.log(mention);
```

```text
Validé
```

Si l'une des branches oubliait d'affecter `mention`, `tsc` signalerait `Variable 'mention' is used before being assigned.`

## `null` et `undefined`

En mode strict (activé dans cette formation et recommandé partout), `null` et `undefined` sont des types à part : une variable `string` ne peut **pas** contenir `undefined`.

```ts
let surnom: string = "Kiki";
surnom = undefined;
```

```text
error TS2322: Type 'undefined' is not assignable to type 'string'.
```

Pour autoriser l'absence de valeur, on l'écrit explicitement avec une **union** (`|` se lit « ou ») :

```ts
let surnom: string | undefined = undefined;
console.log(surnom);
surnom = "Kiki";
console.log(surnom.toUpperCase());
```

```text
undefined
KIKI
```

Ici TypeScript sait qu'au moment du `toUpperCase()`, `surnom` vient de recevoir une chaîne : l'appel est autorisé. Cette capacité à suivre le type au fil du code s'appelle le **rétrécissement** (*narrowing*), détaillé au module 2.

## Des opérations vérifiées

TypeScript vérifie aussi les **opérations** : les calculs arithmétiques (`*`, `-`, `/`, `%`) n'acceptent que des nombres. Le piège de JavaScript où `"3" * 2` donne silencieusement `6` est signalé :

```ts
const quantite = "3";
console.log(quantite * 2);
```

```text
error TS2362: The left-hand side of an arithmetic operation must be of type 'any', 'number', 'bigint' or an enum type.
```

Le message dit que la partie gauche (*left-hand side*) d'une opération arithmétique doit être un nombre. La correction consiste à **convertir explicitement** la valeur :

```ts
const quantite = "3";
const n = Number(quantite);
console.log(n * 2, Number.isNaN(Number("trois")));
```

```text
6 true
```

En revanche, `+` entre un texte et un nombre reste autorisé, car c'est une concaténation parfaitement valide en JavaScript : `"Total : " + 12` donne `"Total : 12"`. Restez donc attentif aux valeurs saisies dans un formulaire, qui sont toujours des chaînes.

## `any` : désactiver la vérification

Le type `any` accepte **tout** et autorise **tout** : TypeScript cesse de vérifier.

```ts
let donnee: any = "texte";
console.log(donnee.toFixed(2));
```

```text
TypeError: donnee.toFixed is not a function
```

Ce code compile sans erreur… puis plante à l'exécution avec l'erreur ci-dessus, car une chaîne n'a pas de méthode `toFixed`. `any` fait perdre tout l'intérêt de TypeScript.

> En mode strict, un paramètre sans type et dont le type ne peut pas être deviné est une erreur (`implicitly has an 'any' type`) : TypeScript refuse les `any` cachés. Réservez `any` aux migrations progressives d'anciens codes.

## `unknown` : l'alternative sûre

`unknown` accepte lui aussi n'importe quelle valeur, mais **interdit de l'utiliser** tant qu'on n'a pas vérifié son type :

```ts
const valeur: unknown = "42";
console.log(valeur.length);
```

```text
error TS18046: 'valeur' is of type 'unknown'.
```

Après une vérification avec `typeof`, l'utilisation devient possible :

```ts
const valeur: unknown = "42";
if (typeof valeur === "string") {
  console.log(valeur.length);
}
```

```text
2
```

| | `any` | `unknown` |
|---|---|---|
| Accepte toute valeur | oui | oui |
| Utilisable sans vérification | oui (dangereux) | non |
| Usage | migration d'ancien code | données externes (JSON, saisies) |

## À retenir

- Types primitifs : `string`, `number`, `boolean`, en minuscules.
- L'inférence déduit le type d'une variable initialisée ; annotez surtout les fonctions.
- En mode strict, `null` et `undefined` doivent être autorisés explicitement : `string | undefined`.
- `any` désactive la vérification ; préférez `unknown`, qui oblige à vérifier avant d'utiliser.

## Exercices

### Exercice 1 — Inférence

Quel type TypeScript infère-t-il pour chaque variable ? `let a = 3.5; let b = "3.5"; let c = a > 2;`

```solution-text
a : number (3.5 est un nombre)
b : string (entre guillemets, c'est du texte)
c : boolean (le résultat d'une comparaison est true ou false)
```

### Exercice 2 — Corrigez

Ce code ne compile pas : `let telephone: string = undefined;`. Le numéro de téléphone est facultatif. Corrigez la déclaration, puis affectez `"0102030405"` et affichez la valeur.

```solution-ts
let telephone: string | undefined = undefined;
telephone = "0102030405";
console.log(telephone);
```

```text
0102030405
```

### Exercice 3 — unknown

Avec `const saisie: unknown = 12;`, affichez le double de la valeur seulement si c'est un nombre, sinon affichez `Valeur invalide`.

```solution-ts
const saisie: unknown = 12;
if (typeof saisie === "number") {
  console.log(saisie * 2);
} else {
  console.log("Valeur invalide");
}
```

```text
24
```
"""

M1_L3 = r"""
## Typer un tableau

Un tableau se type en ajoutant `[]` après le type de ses éléments :

```ts
const notes: number[] = [12, 15, 9];
notes.push(18);
console.log(notes);
```

```text
[ 12, 15, 9, 18 ]
```

TypeScript vérifie chaque ajout :

```ts
const notes: number[] = [12, 15, 9];
notes.push("dix-huit");
```

```text
error TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.
```

La notation `Array<number>` est équivalente à `number[]` ; elle utilise la syntaxe des **génériques** (module 4). Pour un tableau qui mélange deux types, on utilise une union entre parenthèses : `(string | number)[]`.

Les méthodes de tableau conservent les types : `map`, `filter`, `find` produisent des résultats correctement typés.

```ts
const prix = [10, 25, 40];
const prixTtc = prix.map((p) => p * 1.2);
const chers = prix.filter((p) => p > 20);
console.log(prixTtc, chers);
```

```text
[ 12, 30, 48 ] [ 25, 40 ]
```

Dans `p => p * 1.2`, vous n'avez pas besoin d'annoter `p` : TypeScript sait que les éléments de `prix` sont des `number`. On parle d'**inférence contextuelle**.

## `find` peut ne rien trouver

```ts
const villes = ["Paris", "Lyon", "Lille"];
const trouvee = villes.find((v) => v.startsWith("M"));
console.log(trouvee.length);
```

```text
error TS18048: 'trouvee' is possibly 'undefined'.
```

`find` renvoie `string | undefined` : TypeScript vous oblige à traiter le cas « aucun résultat », source fréquente de bugs en JavaScript.

```ts
const villes = ["Paris", "Lyon", "Lille"];
const trouvee = villes.find((v) => v.startsWith("M"));
if (trouvee !== undefined) {
  console.log(trouvee.length);
} else {
  console.log("Aucune ville trouvée");
}
```

```text
Aucune ville trouvée
```

## Les tuples : des tableaux de forme fixe

Un **tuple** est un tableau dont la **longueur** et le **type de chaque position** sont fixés :

```ts
const point: [number, number] = [48.85, 2.35];
const entree: [string, number] = ["Emma", 16];
console.log(`${entree[0]} a obtenu ${entree[1]}/20`);
console.log(`Latitude ${point[0]}, longitude ${point[1]}`);
```

```text
Emma a obtenu 16/20
Latitude 48.85, longitude 2.35
```

TypeScript connaît le type de chaque case et refuse une position inexistante :

```ts
const entree: [string, number] = ["Emma", 16];
console.log(entree[2]);
```

```text
error TS2493: Tuple type '[string, number]' of length '2' has no element at index '2'.
```

> Les tuples conviennent aux petites paires de valeurs (coordonnées, clé et valeur). Au-delà de deux ou trois éléments, préférez un objet avec des propriétés nommées : `{ nom: "Emma", note: 16 }` est plus lisible que `["Emma", 16]`.

## Les types littéraux

Un **type littéral** n'accepte qu'**une valeur précise**. Combiné à une union, il décrit une liste fermée de valeurs autorisées :

```ts
let niveau: "debutant" | "intermediaire" | "avance";
niveau = "intermediaire";
console.log(niveau);
```

```text
intermediaire
```

Une faute de frappe est détectée immédiatement (dans ses messages, `tsc` peut lister les membres de l'union dans un autre ordre que celui de votre déclaration) :

```ts
let niveau: "debutant" | "intermediaire" | "avance";
niveau = "expert";
```

```text
error TS2322: Type '"expert"' is not assignable to type '"avance" | "debutant" | "intermediaire"'.
```

C'est l'un des outils les plus utiles de TypeScript : statuts de commande, rôles d'utilisateur, thèmes `"clair" | "sombre"`… Les nombres et booléens littéraux existent aussi : `1 | 2 | 3`.

## `const` et `as const`

Avec `let`, le type inféré est élargi (`let theme = "clair"` donne `string`) ; avec `const`, il reste littéral (`"clair"`). Pour un tableau ou un objet, `as const` fige toutes les valeurs : le contenu devient en **lecture seule** et chaque valeur garde son type littéral.

```ts
const JOURS_OUVRES = ["lundi", "mardi", "mercredi", "jeudi", "vendredi"] as const;
console.log(JOURS_OUVRES.length, JOURS_OUVRES[0]);
```

```text
5 lundi
```

Le type de `JOURS_OUVRES` est `readonly ["lundi", "mardi", "mercredi", "jeudi", "vendredi"]` : un `push` serait refusé.

## Et les `enum` ?

TypeScript propose aussi des **énumérations** :

```ts
enum Statut {
  Brouillon,
  Publie,
  Archive,
}
const s: Statut = Statut.Publie;
console.log(s, Statut[s]);
```

```text
1 Publie
```

Un `enum` est l'une des rares fonctionnalités de TypeScript qui **génère du code** à l'exécution (un objet `Statut`) : ce n'est pas un simple type effacé. Beaucoup d'équipes lui préfèrent aujourd'hui une union de littéraux (`"brouillon" | "publie" | "archive"`), plus simple et sans code généré ; certains outils qui se contentent d'effacer les types ne savent d'ailleurs pas traiter les `enum` (module 5). Vous rencontrerez les deux.

## À retenir

- `number[]` (ou `Array<number>`) pour un tableau ; `(string | number)[]` pour un mélange.
- `find` renvoie `T | undefined` : traitez le cas où rien n'est trouvé.
- Tuple `[string, number]` : longueur et types fixés par position.
- Types littéraux + union = liste fermée de valeurs autorisées : `"clair" | "sombre"`.
- `as const` fige un tableau ou un objet en lecture seule avec des types littéraux.

## Exercices

### Exercice 1 — Moyenne typée

Déclarez `const notes: number[] = [14, 9, 17, 12]` et affichez la moyenne avec `reduce`.

```solution-ts
const notes: number[] = [14, 9, 17, 12];
const somme = notes.reduce((total, n) => total + n, 0);
console.log(somme / notes.length);
```

```text
13
```

### Exercice 2 — Liste fermée

Déclarez une variable `taille` qui n'accepte que `"S"`, `"M"` ou `"L"`, affectez-lui `"M"` et affichez-la. Que se passerait-il avec `"XL"` ?

```solution-ts
let taille: "S" | "M" | "L";
taille = "M";
console.log(taille);
// taille = "XL"; serait refusé : Type '"XL"' is not assignable to type '"S" | "M" | "L"'.
```

```text
M
```

### Exercice 3 — Recherche sûre

Avec `const emails = ["amina@exemple.fr", "lucas@exemple.fr"]`, cherchez l'email qui commence par `"lucas"` et affichez-le en majuscules, ou `Introuvable`.

```solution-ts
const emails = ["amina@exemple.fr", "lucas@exemple.fr"];
const email = emails.find((e) => e.startsWith("lucas"));
console.log(email !== undefined ? email.toUpperCase() : "Introuvable");
```

```text
LUCAS@EXEMPLE.FR
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Fonctions, objets, unions et narrowing
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Typer les paramètres et le retour

On annote chaque **paramètre**, puis le **type de retour** après les parenthèses :

```ts
function moyenne(a: number, b: number): number {
  return (a + b) / 2;
}
console.log(moyenne(12, 15));
```

```text
13.5
```

TypeScript vérifie alors **chaque appel** : nombre d'arguments, type de chacun.

```ts
function moyenne(a: number, b: number): number {
  return (a + b) / 2;
}
console.log(moyenne(12));
```

```text
error TS2554: Expected 2 arguments, but got 1.
```

Le type de retour peut être inféré, mais l'écrire est une bonne habitude : si le corps de la fonction renvoie par erreur autre chose, l'erreur est signalée **dans la fonction** et non chez ceux qui l'appellent.

```ts
function initiale(nom: string): string {
  return nom.length;
}
```

```text
error TS2322: Type 'number' is not assignable to type 'string'.
```

Le développeur voulait renvoyer la première lettre (`nom[0]`) mais a écrit `nom.length`, un nombre, alors que la fonction promet un `string` : l'annotation de retour a joué son rôle de garde-fou, et l'erreur est signalée sur la ligne fautive.

## Paramètres optionnels et valeurs par défaut

Un `?` après le nom rend un paramètre **optionnel** ; son type devient alors `T | undefined` :

```ts
function saluer(prenom: string, titre?: string): string {
  if (titre) {
    return `Bonjour ${titre} ${prenom}`;
  }
  return `Bonjour ${prenom}`;
}
console.log(saluer("Martin"));
console.log(saluer("Martin", "Dr"));
```

```text
Bonjour Martin
Bonjour Dr Martin
```

Une **valeur par défaut** rend aussi le paramètre optionnel, et son type est inféré :

```ts
function prixTtc(prixHt: number, taux = 0.2): number {
  return Math.round(prixHt * (1 + taux) * 100) / 100;
}
console.log(prixTtc(100));
console.log(prixTtc(100, 0.055));
```

```text
120
105.5
```

> Les paramètres optionnels se placent **après** les paramètres obligatoires.

## Paramètres du reste

Pour accepter un nombre variable d'arguments, on type le **paramètre du reste** (*rest parameter*) comme un tableau :

```ts
function somme(...valeurs: number[]): number {
  return valeurs.reduce((total, v) => total + v, 0);
}
console.log(somme(1, 2, 3, 4));
```

```text
10
```

## Déstructurer un objet en paramètre

Quand une fonction reçoit beaucoup d'options, on lui passe souvent **un objet**, que l'on déstructure directement dans la signature. Le type s'écrit après le motif de déstructuration :

```ts
function creerCompte({ email, role = "etudiant" }: { email: string; role?: string }): string {
  return `${email} (${role})`;
}
console.log(creerCompte({ email: "ines@exemple.fr" }));
console.log(creerCompte({ email: "marc@exemple.fr", role: "formateur" }));
```

```text
ines@exemple.fr (etudiant)
marc@exemple.fr (formateur)
```

L'appel est lisible (chaque valeur est nommée) et l'ordre des propriétés n'a plus d'importance. Une propriété mal nommée est signalée, avec une suggestion :

```ts
function creerCompte({ email, role = "etudiant" }: { email: string; role?: string }): string {
  return `${email} (${role})`;
}
creerCompte({ mail: "x@exemple.fr" });
```

```text
error TS2561: Object literal may only specify known properties, but 'mail' does not exist in type '{ email: string; role?: string | undefined; }'. Did you mean to write 'email'?
```

Notez que TypeScript affiche `role?: string | undefined` : une propriété optionnelle peut valoir `undefined`. Au module suivant, nous donnerons un nom à ce type d'objet pour ne pas le répéter.

## `void` : ne rien renvoyer

Une fonction qui ne renvoie rien a pour type de retour `void` :

```ts
function journaliser(message: string): void {
  console.log(`[journal] ${message}`);
}
journaliser("Démarrage");
```

```text
[journal] Démarrage
```

## Fonctions fléchées et types de fonctions

Les fonctions fléchées s'annotent de la même façon :

```ts
const carre = (n: number): number => n * n;
console.log(carre(7));
```

```text
49
```

Une fonction est aussi une valeur : on peut décrire son **type** avec la syntaxe `(paramètres) => retour`. C'est indispensable pour typer un paramètre qui est lui-même une fonction (un *callback*) :

```ts
function appliquer(valeurs: number[], operation: (n: number) => number): number[] {
  const resultat: number[] = [];
  for (const v of valeurs) {
    resultat.push(operation(v));
  }
  return resultat;
}
console.log(appliquer([1, 2, 3], (n) => n * 10));
```

```text
[ 10, 20, 30 ]
```

Le callback `(n) => n * 10` n'a pas besoin d'annotation : son type est déduit de celui du paramètre `operation`.

## `never` : une fonction qui ne se termine jamais normalement

Une fonction qui **lève toujours une exception** ne renvoie jamais : son type de retour est `never`.

```ts
function echec(message: string): never {
  throw new Error(message);
}

function diviser(a: number, b: number): number {
  if (b === 0) {
    echec("Division par zéro");
  }
  return a / b;
}

try {
  console.log(diviser(10, 4));
  console.log(diviser(1, 0));
} catch (e) {
  if (e instanceof Error) {
    console.log(`Erreur : ${e.message}`);
  }
}
```

```text
2.5
Erreur : Division par zéro
```

Remarquez le `catch (e)` : en mode strict, `e` est de type `unknown`, car on peut lever n'importe quoi en JavaScript. Le test `e instanceof Error` permet ensuite de lire `e.message` en toute sécurité. Le type `never` sert aussi à vérifier qu'aucun cas n'a été oublié (leçon 3).

## À retenir

- `function f(a: number, b: string): boolean { … }` : paramètres et retour annotés.
- `?` rend un paramètre optionnel (`T | undefined`) ; une valeur par défaut aussi.
- `...valeurs: number[]` pour un nombre variable d'arguments.
- `void` : ne renvoie rien ; `never` : ne se termine jamais normalement.
- Type de fonction : `(n: number) => number`, utile pour les callbacks.

## Exercices

### Exercice 1 — Fonction typée

Écrivez `estMajeur(age: number): boolean` puis affichez le résultat pour 17 et 18.

```solution-ts
function estMajeur(age: number): boolean {
  return age >= 18;
}
console.log(estMajeur(17));
console.log(estMajeur(18));
```

```text
false
true
```

### Exercice 2 — Paramètre optionnel

Écrivez `formaterPrix(montant: number, devise?: string): string` qui renvoie le montant avec deux décimales suivi de la devise, `€` par défaut. Testez avec `12.5` puis `(8, "$")`.

```solution-ts
function formaterPrix(montant: number, devise?: string): string {
  return `${montant.toFixed(2)} ${devise ?? "€"}`;
}
console.log(formaterPrix(12.5));
console.log(formaterPrix(8, "$"));
```

```text
12.50 €
8.00 $
```

L'opérateur `??` (*nullish coalescing*) renvoie la valeur de droite quand celle de gauche est `null` ou `undefined`. Une valeur par défaut `devise = "€"` serait tout aussi correcte.

### Exercice 3 — Callback typé

Écrivez `compter(mots: string[], test: (mot: string) => boolean): number` qui compte les mots validant le test. Comptez les mots de plus de 4 lettres dans `["chat", "éléphant", "souris", "rat"]`.

```solution-ts
function compter(mots: string[], test: (mot: string) => boolean): number {
  let total = 0;
  for (const mot of mots) {
    if (test(mot)) total++;
  }
  return total;
}
console.log(compter(["chat", "éléphant", "souris", "rat"], (m) => m.length > 4));
```

```text
2
```
"""

M2_L2 = r"""
## Le type d'un objet

Un objet se type en listant ses propriétés et leur type :

```ts
const etudiant: { prenom: string; age: number } = {
  prenom: "Sofia",
  age: 22,
};
console.log(`${etudiant.prenom}, ${etudiant.age} ans`);
```

```text
Sofia, 22 ans
```

TypeScript vérifie alors que les propriétés existent et ont le bon type. Une faute de frappe dans un nom de propriété, l'une des erreurs les plus courantes en JavaScript, est détectée immédiatement :

```ts
const etudiant = { prenom: "Sofia", age: 22 };
console.log(etudiant.prenon);
```

```text
error TS2551: Property 'prenon' does not exist on type '{ prenom: string; age: number; }'. Did you mean 'prenom'?
```

## Nommer un type avec `type`

Répéter `{ prenom: string; age: number }` partout serait pénible. Un **alias de type** donne un nom à un type :

```ts
type Etudiant = {
  prenom: string;
  age: number;
};

function presenter(e: Etudiant): string {
  return `${e.prenom} (${e.age} ans)`;
}

const lucas: Etudiant = { prenom: "Lucas", age: 25 };
console.log(presenter(lucas));
```

```text
Lucas (25 ans)
```

> Par convention, les noms de types commencent par une **majuscule** (*PascalCase*) : `Etudiant`, `Commande`, `LigneDeFacture`.

Un alias peut nommer n'importe quel type, pas seulement un objet : `type Identifiant = string | number;`, `type Theme = "clair" | "sombre";`.

## Propriétés manquantes ou en trop

Un objet déclaré avec un type doit avoir **toutes** les propriétés obligatoires :

```ts
type Etudiant = { prenom: string; age: number };
const amina: Etudiant = { prenom: "Amina" };
```

```text
error TS2741: Property 'age' is missing in type '{ prenom: string; }' but required in type 'Etudiant'.
```

Et un objet écrit directement (*littéral d'objet*) ne doit pas contenir de propriété inconnue, ce qui attrape les fautes de frappe :

```ts
type Etudiant = { prenom: string; age: number };
const amina: Etudiant = { prenom: "Amina", age: 20, emial: "amina@exemple.fr" };
```

```text
error TS2353: Object literal may only specify known properties, and 'emial' does not exist in type 'Etudiant'.
```

## Propriétés optionnelles et en lecture seule

- `?` rend une propriété **optionnelle** ;
- `readonly` interdit de la **modifier** après la création.

```ts
type Produit = {
  readonly reference: string;
  nom: string;
  prix: number;
  description?: string;
};

const stylo: Produit = { reference: "ST-001", nom: "Stylo", prix: 1.5 };
stylo.prix = 1.8;
console.log(stylo);
console.log(stylo.description ?? "(pas de description)");
```

```text
{ reference: 'ST-001', nom: 'Stylo', prix: 1.8 }
(pas de description)
```

Modifier la référence est refusé :

```ts
type Produit = { readonly reference: string; nom: string };
const stylo: Produit = { reference: "ST-001", nom: "Stylo" };
stylo.reference = "ST-002";
```

```text
error TS2540: Cannot assign to 'reference' because it is a read-only property.
```

> `readonly` est une vérification de TypeScript uniquement : à l'exécution, l'objet reste modifiable par du code JavaScript non vérifié. Pour un tableau, on écrit `readonly string[]` : `push`, `pop` et l'affectation d'une case sont alors interdits.

## Le chaînage optionnel `?.`

Quand une propriété peut être absente, l'opérateur `?.` renvoie `undefined` au lieu de planter :

```ts
type Adresse = { ville: string; codePostal: string };
type Client = { nom: string; adresse?: Adresse };

const c1: Client = { nom: "Durand", adresse: { ville: "Nantes", codePostal: "44000" } };
const c2: Client = { nom: "Petit" };

console.log(c1.adresse?.ville);
console.log(c2.adresse?.ville);
console.log(c2.adresse?.ville ?? "Ville inconnue");
```

```text
Nantes
undefined
Ville inconnue
```

Sans le `?.`, écrire `c2.adresse.ville` serait refusé : `error TS18048: 'c2.adresse' is possibly 'undefined'.`

## Objets imbriqués et tableaux d'objets

Les types se combinent librement :

```ts
type Ligne = { produit: string; quantite: number; prixUnitaire: number };
type Commande = { numero: number; client: string; lignes: Ligne[] };

const commande: Commande = {
  numero: 1042,
  client: "Atelier Leroy",
  lignes: [
    { produit: "Cahier", quantite: 3, prixUnitaire: 2.5 },
    { produit: "Classeur", quantite: 2, prixUnitaire: 4 },
  ],
};

function total(c: Commande): number {
  return c.lignes.reduce((s, l) => s + l.quantite * l.prixUnitaire, 0);
}
console.log(`Commande ${commande.numero} : ${total(commande)} €`);
```

```text
Commande 1042 : 15.5 €
```

## Objets « dictionnaires » : `Record`

Pour un objet dont les **clés ne sont pas connues à l'avance** (stock par référence, traductions…), on utilise `Record<Clé, Valeur>` :

```ts
const stock: Record<string, number> = { "ST-001": 120, "CA-010": 35 };
stock["CL-020"] = 12;
for (const [reference, quantite] of Object.entries(stock)) {
  console.log(`${reference} : ${quantite}`);
}
```

```text
ST-001 : 120
CA-010 : 35
CL-020 : 12
```

On rencontre aussi l'écriture équivalente `{ [reference: string]: number }`, appelée **signature d'index**.

> Attention : par défaut, `stock["XYZ"]` est typé `number` alors que la clé n'existe pas (la valeur réelle est `undefined`). L'option `noUncheckedIndexedAccess` (module 5) corrige ce point en typant l'accès `number | undefined`.

## À retenir

- `type Nom = { prop: type; … }` nomme un type d'objet (PascalCase).
- TypeScript signale propriétés manquantes, inconnues ou mal orthographiées.
- `prop?: T` : optionnelle ; `readonly prop: T` : non modifiable (vérification à la compilation).
- `?.` et `??` gèrent proprement les valeurs absentes.
- `Record<string, number>` pour un dictionnaire aux clés libres.

## Exercices

### Exercice 1 — Type Livre

Créez un type `Livre` (titre, auteur, annee, disponible) et une fonction `fiche(l: Livre): string`. Affichez la fiche d'un livre fictif.

```solution-ts
type Livre = {
  titre: string;
  auteur: string;
  annee: number;
  disponible: boolean;
};

function fiche(l: Livre): string {
  const etat = l.disponible ? "disponible" : "emprunté";
  return `${l.titre} — ${l.auteur} (${l.annee}) : ${etat}`;
}

console.log(fiche({ titre: "Les Algorithmes du jardin", auteur: "Claire Roux", annee: 2021, disponible: false }));
```

```text
Les Algorithmes du jardin — Claire Roux (2021) : emprunté
```

### Exercice 2 — Repérez les erreurs

Avec `type Salle = { readonly nom: string; capacite: number; projecteur?: boolean }`, lesquelles de ces lignes sont refusées ? `const a: Salle = { nom: "A1", capacite: 30 };` — `a.capacite = 32;` — `a.nom = "B2";` — `const b: Salle = { nom: "B1" };`

```solution-text
1. Acceptée : projecteur est optionnel.
2. Acceptée : capacite n'est pas en lecture seule.
3. Refusée : nom est readonly (TS2540).
4. Refusée : la propriété obligatoire capacite manque (TS2741).
```

### Exercice 3 — Panier

Avec `const panier: Record<string, number> = { pommes: 3, poires: 2 }` (quantités), écrivez une boucle qui affiche le nombre total d'articles.

```solution-ts
const panier: Record<string, number> = { pommes: 3, poires: 2 };
let totalArticles = 0;
for (const quantite of Object.values(panier)) {
  totalArticles += quantite;
}
console.log(totalArticles);
```

```text
5
```
"""

M2_L3 = r"""
## Les unions

Une **union** `A | B` décrit une valeur qui est **soit** de type A, **soit** de type B :

```ts
function afficherIdentifiant(id: string | number): void {
  console.log(`Identifiant : ${id}`);
}
afficherIdentifiant(42);
afficherIdentifiant("u-42");
```

```text
Identifiant : 42
Identifiant : u-42
```

Sur une union, on ne peut utiliser **que ce qui est commun** à tous les membres :

```ts
function majuscules(id: string | number): string {
  return id.toUpperCase();
}
```

```text
error TS2339: Property 'toUpperCase' does not exist on type 'string | number'.
```

`toUpperCase` existe pour `string`, pas pour `number`. Il faut d'abord **déterminer** de quel membre il s'agit.

## Le rétrécissement (*narrowing*)

TypeScript analyse les tests que vous écrivez et **rétrécit** le type dans chaque branche :

```ts
function formater(id: string | number): string {
  if (typeof id === "string") {
    return id.toUpperCase();      // ici, id est un string
  }
  return id.toString().padStart(5, "0"); // ici, id est un number
}
console.log(formater("u-42"));
console.log(formater(42));
```

```text
U-42
00042
```

Les principaux tests reconnus :

| Test | Exemple | Pour |
|---|---|---|
| `typeof` | `typeof x === "string"` | types primitifs |
| égalité | `x === null`, `x !== undefined` | valeurs précises |
| véracité | `if (x)` | écarter `null`, `undefined`, `""`, `0` |
| `in` | `"email" in contact` | présence d'une propriété |
| `instanceof` | `e instanceof Error` | instances de classes |
| `Array.isArray` | `Array.isArray(x)` | tableaux |

## Écarter `null` et `undefined`

C'est le cas le plus fréquent :

```ts
function longueur(texte: string | null): number {
  if (texte === null) {
    return 0;
  }
  return texte.length;
}
console.log(longueur("Bonjour"));
console.log(longueur(null));
```

```text
7
0
```

> Le test de véracité `if (texte)` écarte aussi `null`, mais il écarte également la chaîne vide `""` (et `0` pour un nombre). Quand `""` ou `0` sont des valeurs valides, testez explicitement `!== null` ou `!== undefined`.

## L'opérateur `in`

Pour distinguer deux types d'objets, on peut tester la présence d'une propriété :

```ts
type ContactEmail = { email: string };
type ContactTelephone = { telephone: string };

function joindre(c: ContactEmail | ContactTelephone): string {
  if ("email" in c) {
    return `Envoyer un message à ${c.email}`;
  }
  return `Appeler le ${c.telephone}`;
}
console.log(joindre({ email: "lea@exemple.fr" }));
console.log(joindre({ telephone: "0102030405" }));
```

```text
Envoyer un message à lea@exemple.fr
Appeler le 0102030405
```

## Les unions discriminées

Le motif le plus puissant consiste à donner à chaque membre d'une union une propriété commune avec une **valeur littérale différente**, le **discriminant** (souvent `type` ou `kind`) :

```ts
type Cercle = { forme: "cercle"; rayon: number };
type Rectangle = { forme: "rectangle"; largeur: number; hauteur: number };
type Figure = Cercle | Rectangle;

function aire(f: Figure): number {
  switch (f.forme) {
    case "cercle":
      return Math.PI * f.rayon ** 2;
    case "rectangle":
      return f.largeur * f.hauteur;
  }
}

console.log(aire({ forme: "rectangle", largeur: 4, hauteur: 2.5 }));
console.log(aire({ forme: "cercle", rayon: 1 }).toFixed(2));
```

```text
10
3.14
```

Dans le `case "cercle"`, TypeScript sait que `f` est un `Cercle` : `f.rayon` est accessible, `f.largeur` serait refusé. Ce motif modélise très bien les états d'une application : `{ etat: "chargement" } | { etat: "succes"; donnees: … } | { etat: "erreur"; message: string }`.

## Vérifier l'exhaustivité avec `never`

Que se passe-t-il si l'on ajoute une forme `Triangle` sans mettre à jour `aire` ? On peut demander à TypeScript de le signaler. Dans le `default`, toutes les formes ont été traitées : le type restant est `never`. Si une forme a été oubliée, l'affectation à `never` échoue :

```ts
type Cercle = { forme: "cercle"; rayon: number };
type Carre = { forme: "carre"; cote: number };
type Triangle = { forme: "triangle"; base: number; hauteur: number };
type Figure = Cercle | Carre | Triangle;

function aire(f: Figure): number {
  switch (f.forme) {
    case "cercle":
      return Math.PI * f.rayon ** 2;
    case "carre":
      return f.cote ** 2;
    default: {
      const oubli: never = f;
      throw new Error(`Forme non gérée : ${JSON.stringify(oubli)}`);
    }
  }
}
```

```text
error TS2322: Type 'Triangle' is not assignable to type 'never'.
```

Le message désigne précisément le cas oublié. Ajoutez `case "triangle": return (f.base * f.hauteur) / 2;` et l'erreur disparaît.

## Les prédicats de type

Pour réutiliser un test, on écrit une fonction dont le type de retour est un **prédicat** `parametre is Type` :

```ts
type Utilisateur = { nom: string; email: string };

function estUtilisateur(valeur: unknown): valeur is Utilisateur {
  return (
    typeof valeur === "object" &&
    valeur !== null &&
    "nom" in valeur && typeof valeur.nom === "string" &&
    "email" in valeur && typeof valeur.email === "string"
  );
}

const recu: unknown = JSON.parse('{"nom": "Karim", "email": "karim@exemple.fr"}');
if (estUtilisateur(recu)) {
  console.log(`Bienvenue ${recu.nom}`);
} else {
  console.log("Données invalides");
}
console.log(estUtilisateur({ nom: "Lina" }));
```

```text
Bienvenue Karim
false
```

C'est ainsi que l'on **valide des données externes** (réponse d'API, fichier JSON) : `JSON.parse` renvoie `any`, que l'on range dans une variable `unknown`, puis un prédicat vérifie réellement la forme avant utilisation.

> TypeScript fait confiance à votre prédicat : s'il renvoie `true` à tort, le typage sera faux. Testez-le soigneusement. Dans les projets réels, des bibliothèques de validation de schémas automatisent ce travail.

## À retenir

- `A | B` : soit l'un, soit l'autre ; seules les propriétés communes sont utilisables directement.
- `typeof`, `===`, `in`, `instanceof`, `Array.isArray` rétrécissent le type.
- Union discriminée : une propriété littérale commune (`forme`, `type`, `etat`) + `switch`.
- `const oubli: never = x` dans le `default` vérifie que tous les cas sont traités.
- `valeur is Type` crée un test réutilisable, idéal pour valider des données `unknown`.

## Exercices

### Exercice 1 — Normaliser

Écrivez `enNombre(v: string | number): number` qui convertit une chaîne avec `Number()` et renvoie un nombre tel quel. Testez avec `"12.5"` et `7`.

```solution-ts
function enNombre(v: string | number): number {
  if (typeof v === "string") {
    return Number(v);
  }
  return v;
}
console.log(enNombre("12.5") + enNombre(7));
```

```text
19.5
```

### Exercice 2 — Paiement

Modélisez `Paiement = { mode: "carte"; derniersChiffres: string } | { mode: "virement"; iban: string } | { mode: "especes" }` et écrivez `decrire(p: Paiement): string` avec un `switch`. Testez les trois modes.

```solution-ts
type Paiement =
  | { mode: "carte"; derniersChiffres: string }
  | { mode: "virement"; iban: string }
  | { mode: "especes" };

function decrire(p: Paiement): string {
  switch (p.mode) {
    case "carte":
      return `Carte se terminant par ${p.derniersChiffres}`;
    case "virement":
      return `Virement depuis ${p.iban.slice(0, 4)}…`;
    case "especes":
      return "Paiement en espèces";
  }
}

console.log(decrire({ mode: "carte", derniersChiffres: "4242" }));
console.log(decrire({ mode: "virement", iban: "FR7630006000011234567890189" }));
console.log(decrire({ mode: "especes" }));
```

```text
Carte se terminant par 4242
Virement depuis FR76…
Paiement en espèces
```

### Exercice 3 — Pourquoi l'erreur ?

Pourquoi `function f(x: string | undefined) { return x.trim(); }` est-il refusé, et comment le corriger ?

```solution-text
x peut valoir undefined, qui n'a pas de méthode trim : tsc signale « 'x' is possibly 'undefined' » (TS18048).
Corrections possibles : tester avant (if (x === undefined) return ""; return x.trim();),
utiliser le chaînage optionnel (return x?.trim();, qui renvoie alors string | undefined)
ou fournir une valeur par défaut (return (x ?? "").trim();).
```
"""

QUIZ_M1 = [
    ("single", "Que fait la commande tsc ?", None,
     ["Elle exécute directement le TypeScript dans le navigateur", "Elle vérifie les types puis produit du JavaScript", "Elle installe Node.js", "Elle minifie le CSS"], [1],
     "tsc est le compilateur : il vérifie les types et émet des fichiers .js en effaçant les annotations."),
    ("true_false", "Les annotations de type TypeScript sont vérifiées pendant l'exécution du programme.", None,
     ["Vrai", "Faux"], [1],
     "Les types sont effacés à la compilation : ils n'existent plus à l'exécution. Les données externes doivent être vérifiées par du code."),
    ("single", "Quel type TypeScript infère-t-il pour let total = 0 ?", None,
     ["any", "0", "number", "unknown"], [2],
     "Avec let, le type inféré est élargi au type primitif : number. Avec const, il serait le littéral 0."),
    ("single", "Qu'affiche tsc pour ce code ?", "let ville: string = \"Lyon\";\nville = 69;",
     ["Rien, le code est valide", "error TS2322: Type 'number' is not assignable to type 'string'.", "error TS2304: Cannot find name 'ville'.", "Une erreur seulement à l'exécution"], [1],
     "ville est déclarée string : lui affecter un nombre est refusé avec l'erreur TS2322."),
    ("single", "En mode strict, comment déclarer une variable texte qui peut aussi être absente ?", None,
     ["let s: string = undefined;", "let s: string | undefined;", "let s: any;", "let s?: string;"], [1],
     "L'union string | undefined autorise explicitement l'absence de valeur. La syntaxe ? est réservée aux propriétés et paramètres."),
    ("multiple", "Quelles affirmations sur any et unknown sont exactes ?", None,
     ["Les deux acceptent n'importe quelle valeur.", "unknown oblige à vérifier le type avant d'utiliser la valeur.", "any conserve toutes les vérifications de TypeScript.", "unknown est préférable pour des données reçues de l'extérieur."], [0, 1, 3],
     "any désactive la vérification ; unknown accepte tout mais impose un test (typeof…) avant usage, ce qui le rend sûr pour les données externes."),
    ("single", "Quel est le type de retour de [\"a\", \"b\"].find(...) ?", None,
     ["string", "string[]", "string | undefined", "boolean"], [2],
     "find peut ne rien trouver : TypeScript type le résultat string | undefined et oblige à traiter ce cas."),
    ("single", "Quel type décrit une paire « nom, note » de longueur fixe ?", None,
     ["string | number", "[string, number]", "(string | number)[]", "Array<string>"], [1],
     "Un tuple [string, number] fixe la longueur et le type de chaque position."),
    ("single", "Que permet le type \"clair\" | \"sombre\" ?", None,
     ["N'importe quelle chaîne", "Uniquement les valeurs \"clair\" ou \"sombre\"", "Un booléen", "Un tableau de deux chaînes"], [1],
     "C'est une union de types littéraux : seules ces deux valeurs précises sont acceptées."),
    ("multiple", "Que fait as const appliqué à un tableau littéral ?", None,
     ["Il rend le tableau en lecture seule pour TypeScript.", "Il conserve le type littéral de chaque valeur.", "Il copie le tableau en profondeur à l'exécution.", "Il convertit les valeurs en chaînes."], [0, 1],
     "as const produit un type readonly avec des littéraux ; il n'a aucun effet à l'exécution (pas de copie ni de conversion)."),
]

QUIZ_M2 = [
    ("single", "Que signale tsc pour moyenne(12) si moyenne attend deux paramètres number ?", None,
     ["Rien", "error TS2554: Expected 2 arguments, but got 1.", "Une erreur seulement à l'exécution", "error TS2322"], [1],
     "TypeScript vérifie le nombre d'arguments de chaque appel : il en manque un."),
    ("single", "Quel est le type du paramètre titre dans function f(titre?: string) ?", None,
     ["string", "string | undefined", "any", "string | null"], [1],
     "Un paramètre optionnel peut être omis : sa valeur est alors undefined, d'où le type string | undefined."),
    ("single", "Quel type de retour pour une fonction qui lève toujours une exception ?", None,
     ["void", "undefined", "never", "unknown"], [2],
     "never signifie que la fonction ne se termine jamais normalement. void s'utilise pour une fonction qui se termine sans renvoyer de valeur."),
    ("single", "Comment typer un paramètre « fonction qui reçoit un nombre et renvoie un booléen » ?", None,
     ["test: Function", "test: (n: number) => boolean", "test: boolean(number)", "test: number => boolean"], [1],
     "La syntaxe d'un type de fonction est (paramètres) => typeDeRetour, avec des paramètres nommés."),
    ("multiple", "Avec type Produit = { readonly ref: string; prix: number; note?: number }, quelles affirmations sont exactes ?", None,
     ["{ ref: \"A\", prix: 2 } est un Produit valide.", "On peut modifier p.prix.", "On peut modifier p.ref.", "note est obligatoire."], [0, 1],
     "note est optionnelle (?) et seule ref est en lecture seule : prix reste modifiable."),
    ("single", "Que vaut client.adresse?.ville si adresse est absente ?", None,
     ["Une erreur TypeError", "undefined", "null", "\"\""], [1],
     "Le chaînage optionnel ?. s'arrête et renvoie undefined dès que la valeur à gauche est null ou undefined."),
    ("single", "Pourquoi ce code est-il refusé ?", "function f(id: string | number) {\n  return id.toUpperCase();\n}",
     ["toUpperCase n'existe pas en JavaScript", "toUpperCase n'existe pas sur number, donc pas sur l'union", "Il manque le type de retour", "Les unions sont interdites en paramètre"], [1],
     "Sur une union, seules les propriétés communes sont utilisables ; il faut d'abord rétrécir avec typeof."),
    ("multiple", "Quels tests rétrécissent le type d'une valeur ?", None,
     ["typeof x === \"string\"", "x instanceof Error", "\"email\" in x", "console.log(x)"], [0, 1, 2],
     "typeof, instanceof et in sont analysés par TypeScript ; un simple affichage ne donne aucune information sur le type."),
    ("single", "Dans une union discriminée, à quoi sert le discriminant ?", None,
     ["À trier les objets", "À identifier le membre de l'union grâce à une valeur littérale propre à chacun", "À rendre les propriétés optionnelles", "À convertir l'objet en JSON"], [1],
     "Chaque membre porte une valeur littérale différente (forme: \"cercle\"…) : tester cette propriété suffit à connaître le type exact."),
    ("true_false", "Dans le default d'un switch, const oubli: never = f; provoque une erreur de compilation si un cas de l'union n'a pas été traité.", None,
     ["Vrai", "Faux"], [0],
     "Si un membre n'est pas traité, il reste dans le type de f au default, et il n'est pas affectable à never : tsc le signale."),
]

MODULES = [
    {
        "position": 1,
        "title": "Pourquoi TypeScript et types de base",
        "description": "Comprendre la compilation, lire une erreur de tsc et utiliser les types de base, les tableaux, tuples et littéraux.",
        "status": "published",
        "lessons": [
            ("decouvrir-typescript", "Découvrir TypeScript",
             "Ce que TypeScript ajoute à JavaScript, la compilation avec tsc et la lecture des erreurs.", M1_L1, 25),
            ("types-de-base", "Types de base et inférence",
             "string, number, boolean, inférence, null et undefined, any et unknown.", M1_L2, 35),
            ("tableaux-tuples-litteraux", "Tableaux, tuples et types littéraux",
             "Typer des listes, des paires de valeurs et des ensembles fermés de valeurs.", M1_L3, 30),
        ],
        "quiz": ("Quiz — Pourquoi TypeScript et types de base", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Fonctions, objets, unions et narrowing",
        "description": "Typer les fonctions et les objets, combiner des types avec les unions et laisser TypeScript rétrécir les types.",
        "status": "published",
        "lessons": [
            ("fonctions-typees", "Fonctions typées",
             "Paramètres, retour, optionnels, reste, void, never et types de fonctions.", M2_L1, 30),
            ("objets-et-alias", "Objets et alias de type",
             "Types d'objets, propriétés optionnelles et readonly, chaînage optionnel, Record.", M2_L2, 30),
            ("unions-narrowing", "Unions et rétrécissement",
             "typeof, in, unions discriminées, exhaustivité et prédicats de type.", M2_L3, 35),
        ],
        "quiz": ("Quiz — Fonctions, objets, unions et narrowing", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Interfaces, types et classes",
        "description": "Décrire des contrats avec les interfaces, composer des types et écrire des classes typées.",
        "status": "published",
        "lessons": [
            ("interfaces", "Les interfaces",
             "Déclarer, étendre et composer des contrats ; interface ou type ?", _m35.M3_L1, 30),
            ("classes", "Les classes typées",
             "Propriétés, constructeur, visibilité, readonly, accesseurs et membres statiques.", _m35.M3_L2, 35),
            ("heritage-abstraction", "Héritage, implements et classes abstraites",
             "Réutiliser et spécialiser du code, typage structurel.", _m35.M3_L3, 30),
        ],
        "quiz": ("Quiz — Interfaces, types et classes", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Génériques et types utilitaires",
        "description": "Écrire du code réutilisable sans perdre la précision des types, et transformer des types existants.",
        "status": "published",
        "lessons": [
            ("generiques", "Les génériques",
             "Fonctions génériques, inférence, contraintes et keyof.", _m35.M4_L1, 35),
            ("types-generiques-asynchrone", "Types génériques et code asynchrone",
             "Interfaces et classes génériques, Promise<T> et async typé.", _m35.M4_L2, 30),
            ("types-utilitaires", "Les types utilitaires",
             "Partial, Pick, Omit, Record, ReturnType, typeof, keyof et satisfies.", _m35.M4_L3, 35),
        ],
        "quiz": ("Quiz — Génériques et types utilitaires", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Configurer un projet TypeScript",
        "description": "tsconfig.json, mode strict, modules et outillage, puis un mini-projet entièrement typé.",
        "status": "published",
        "lessons": [
            ("tsconfig-strict", "tsconfig.json et le mode strict",
             "Créer et comprendre la configuration d'un projet, options de rigueur.", _m35.M5_L1, 30),
            ("modules-outillage", "Modules, déclarations et outillage",
             "import et export, import type, fichiers .d.ts, @types et exécution.", _m35.M5_L2, 30),
            ("mini-projet", "Mini-projet : gestion des inscriptions",
             "Une application typée de bout en bout : modèles, validation, génériques et rapport.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Configurer un projet TypeScript", _m35.QUIZ_M5),
    },
]
