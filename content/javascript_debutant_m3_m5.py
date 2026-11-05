"""Modules 3 à 5 de « JavaScript pour débutants » (importé par content/javascript_debutant.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Fonctions, tableaux et objets
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Pourquoi des fonctions ?

Une **fonction** regroupe des instructions sous un nom, pour les réutiliser autant de fois que nécessaire. Elle évite de copier-coller du code et rend le programme plus lisible.

```js
function direBonjour(prenom) {
  console.log(`Bonjour ${prenom} !`);
}

direBonjour("Amina");
direBonjour("Lucas");
```

```text
Bonjour Amina !
Bonjour Lucas !
```

- `function direBonjour(prenom)` **déclare** la fonction ; `prenom` est un **paramètre** ;
- `direBonjour("Amina")` **appelle** la fonction ; `"Amina"` est l'**argument**.

## Renvoyer un résultat : `return`

Une fonction peut **calculer** une valeur et la renvoyer avec `return`. L'appel est alors remplacé par cette valeur :

```js
function prixTtc(prixHt, taux) {
  return prixHt * (1 + taux);
}

const total = prixTtc(100, 0.2);
console.log(total);
console.log(prixTtc(50, 0.055));
```

```text
120
52.75
```

`return` **arrête** immédiatement la fonction. Une fonction sans `return` renvoie `undefined`.

> Distinguez bien **afficher** (`console.log`) et **renvoyer** (`return`) : une fonction qui renvoie un résultat est réutilisable dans d'autres calculs ; une fonction qui se contente d'afficher ne l'est pas.

## Paramètres par défaut

```js
function saluer(prenom = "visiteur") {
  return `Bienvenue, ${prenom}`;
}
console.log(saluer());
console.log(saluer("Sofia"));
```

```text
Bienvenue, visiteur
Bienvenue, Sofia
```

## Les fonctions fléchées

La syntaxe **fléchée** (*arrow function*) est plus courte, très utilisée avec les tableaux :

```js
const carre = (n) => n * n;
const additionner = (a, b) => a + b;
console.log(carre(4));
console.log(additionner(2, 3));
```

```text
16
5
```

Quand le corps tient en une expression, le `return` est implicite. Pour plusieurs instructions, on utilise des accolades et un `return` explicite :

```js
const mention = (note) => {
  if (note >= 16) return "Très bien";
  if (note >= 10) return "Validé";
  return "À retravailler";
};
console.log(mention(13));
```

```text
Validé
```

## La portée des variables

Une variable déclarée **dans** une fonction n'existe qu'à l'intérieur de celle-ci :

```js
function calculer() {
  const resultat = 42;
  return resultat;
}
console.log(calculer());
```

```text
42
```

Écrire `console.log(resultat)` en dehors de la fonction provoquerait `ReferenceError: resultat is not defined`. De même, une variable déclarée dans un bloc `{ }` (`if`, `for`) avec `let` ou `const` n'existe que dans ce bloc.

## À retenir

- `function nom(parametres) { … }` déclare ; `nom(arguments)` appelle.
- `return` renvoie une valeur et arrête la fonction.
- Fonctions fléchées : `const f = (x) => x * 2;`
- Les variables d'une fonction ou d'un bloc n'existent qu'à l'intérieur.

## Exercices

### Exercice 1 — Moyenne de deux notes

Écrivez une fonction `moyenne(a, b)` qui renvoie la moyenne de deux nombres, puis affichez `moyenne(12, 17)`.

```solution-js
function moyenne(a, b) {
  return (a + b) / 2;
}
console.log(moyenne(12, 17));
```

```text
14.5
```

### Exercice 2 — Version fléchée

Réécrivez en fonction fléchée : `function estMajeur(age) { return age >= 18; }`, puis testez avec 16 et 30.

```solution-js
const estMajeur = (age) => age >= 18;
console.log(estMajeur(16));
console.log(estMajeur(30));
```

```text
false
true
```

### Exercice 3 — Prix soldé

Écrivez `prixSolde(prix, remise = 10)` qui renvoie le prix après une remise en pourcentage (10 % par défaut). Testez avec 80 puis avec 80 et 25.

```solution-js
function prixSolde(prix, remise = 10) {
  return prix * (1 - remise / 100);
}
console.log(prixSolde(80));
console.log(prixSolde(80, 25));
```

```text
72
60
```
"""

M3_L2 = r"""
## Créer un tableau

Un **tableau** (*array*) est une liste ordonnée de valeurs, écrite entre crochets :

```js
const fruits = ["pomme", "banane", "kiwi"];
console.log(fruits.length);
console.log(fruits[0]);
console.log(fruits[fruits.length - 1]);
```

```text
3
pomme
kiwi
```

Comme pour les chaînes, les positions (**indices**) commencent à 0 ; le dernier élément est à l'indice `length - 1`.

## Modifier un tableau

```js
const taches = ["Lire", "Coder"];
taches.push("Tester");       // ajoute à la fin
taches.unshift("Planifier"); // ajoute au début
console.log(taches);
const derniere = taches.pop(); // retire et renvoie le dernier
console.log(derniere, taches);
taches[0] = "Organiser";       // remplace un élément
console.log(taches);
```

```text
[ 'Planifier', 'Lire', 'Coder', 'Tester' ]
Tester [ 'Planifier', 'Lire', 'Coder' ]
[ 'Organiser', 'Lire', 'Coder' ]
```

Un tableau déclaré avec `const` peut être **modifié** : `const` empêche seulement de remplacer le tableau entier par un autre.

## Rechercher

```js
const villes = ["Paris", "Lyon", "Lille"];
console.log(villes.includes("Lyon"));
console.log(villes.indexOf("Lille"));
console.log(villes.indexOf("Nice"));
```

```text
true
2
-1
```

`indexOf` renvoie `-1` quand l'élément est absent.

## Les méthodes essentielles : `map`, `filter`, `find`, `reduce`

Ces méthodes prennent une **fonction** en argument et l'appliquent à chaque élément. Elles ne modifient pas le tableau d'origine.

```js
const prix = [10, 25, 8, 40];

const prixTtc = prix.map((p) => p * 1.2);          // transforme chaque élément
const chers = prix.filter((p) => p > 15);          // garde ceux qui vérifient la condition
const premierPetit = prix.find((p) => p < 10);     // premier élément qui vérifie la condition
const total = prix.reduce((somme, p) => somme + p, 0); // combine tout en une valeur

console.log(prixTtc);
console.log(chers);
console.log(premierPetit);
console.log(total);
```

```text
[ 12, 30, 9.6, 48 ]
[ 25, 40 ]
8
83
```

| Méthode | Renvoie |
|---|---|
| `map` | un nouveau tableau de **même longueur**, éléments transformés |
| `filter` | un nouveau tableau avec **certains** éléments |
| `find` | le **premier** élément trouvé, ou `undefined` |
| `reduce` | **une seule valeur** (somme, maximum…) |

`reduce((acc, element) => …, valeurInitiale)` : `acc` (l'accumulateur) part de la valeur initiale et reçoit, à chaque tour, ce que renvoie la fonction.

## Trier

```js
const notes = [12, 5, 18, 9];
const triees = [...notes].sort((a, b) => a - b);
console.log(triees);
console.log(notes);
```

```text
[ 5, 9, 12, 18 ]
[ 12, 5, 18, 9 ]
```

Deux pièges : `sort()` **modifie** le tableau (d'où la copie `[...notes]`), et sans fonction de comparaison il trie **comme du texte** (`[10, 9, 1].sort()` donne `[1, 10, 9]`). `(a, b) => a - b` trie les nombres par ordre croissant.

## À retenir

- `[a, b, c]`, indices à partir de 0, `length`.
- `push` / `pop` à la fin, `unshift` au début, `includes`, `indexOf`.
- `map` transforme, `filter` sélectionne, `find` cherche, `reduce` combine.
- `sort((a, b) => a - b)` pour trier des nombres, sur une copie.

## Exercices

### Exercice 1 — Doubler

Avec `const nombres = [1, 2, 3, 4]`, créez un tableau contenant le double de chaque nombre.

```solution-js
const nombres = [1, 2, 3, 4];
const doubles = nombres.map((n) => n * 2);
console.log(doubles);
```

```text
[ 2, 4, 6, 8 ]
```

### Exercice 2 — Notes validées

Avec `const notes = [8, 14, 11, 6, 17]`, affichez les notes supérieures ou égales à 10, puis leur nombre.

```solution-js
const notes = [8, 14, 11, 6, 17];
const validees = notes.filter((n) => n >= 10);
console.log(validees);
console.log(validees.length);
```

```text
[ 14, 11, 17 ]
3
```

### Exercice 3 — Maximum avec reduce

Trouvez la plus grande valeur de `[4, 19, 7, 12]` avec `reduce`.

```solution-js
const valeurs = [4, 19, 7, 12];
const max = valeurs.reduce((m, v) => (v > m ? v : m), valeurs[0]);
console.log(max);
// Plus simple : Math.max(...valeurs)
```

```text
19
```
"""

M3_L3 = r"""
## Décrire une chose : l'objet

Un **objet** regroupe des informations sous forme de paires **clé : valeur** (appelées *propriétés*) :

```js
const etudiant = {
  prenom: "Sofia",
  age: 23,
  ville: "Paris",
  inscrite: true,
};
console.log(etudiant.prenom);
console.log(etudiant["ville"]);
```

```text
Sofia
Paris
```

On lit une propriété avec le **point** (`etudiant.prenom`) ou les **crochets** (`etudiant["ville"]`). Les crochets sont nécessaires quand le nom de la propriété est dans une variable :

```js
const etudiant = { prenom: "Sofia", ville: "Paris" };
const champ = "ville";
console.log(etudiant[champ]);
console.log(etudiant.telephone);
```

```text
Paris
undefined
```

Une propriété absente vaut `undefined`.

## Modifier un objet

```js
const produit = { nom: "Clavier", prix: 49 };
produit.prix = 39;          // modifier
produit.stock = 12;         // ajouter
delete produit.stock;       // supprimer
console.log(produit);
```

```text
{ nom: 'Clavier', prix: 39 }
```

## Les méthodes

Une propriété peut contenir une **fonction** : on parle alors de **méthode**. À l'intérieur, `this` désigne l'objet lui-même.

```js
const compte = {
  titulaire: "Karim",
  solde: 100,
  deposer(montant) {
    this.solde += montant;
    return this.solde;
  },
};
console.log(compte.deposer(50));
```

```text
150
```

## Les tableaux d'objets

C'est la structure la plus courante dans une application : une liste d'éléments décrits par des objets.

```js
const formations = [
  { titre: "Python", heures: 11, gratuite: true },
  { titre: "SQL", heures: 8, gratuite: true },
  { titre: "Machine Learning", heures: 20, gratuite: false },
];

const gratuites = formations.filter((f) => f.gratuite).map((f) => f.titre);
const totalHeures = formations.reduce((t, f) => t + f.heures, 0);
console.log(gratuites);
console.log(totalHeures);
```

```text
[ 'Python', 'SQL' ]
39
```

Les méthodes s'enchaînent : `filter` puis `map`.

## Parcourir un objet

```js
const scores = { Amina: 16, Lucas: 12, Emma: 18 };
for (const [nom, score] of Object.entries(scores)) {
  console.log(`${nom} : ${score}`);
}
console.log(Object.keys(scores));
```

```text
Amina : 16
Lucas : 12
Emma : 18
[ 'Amina', 'Lucas', 'Emma' ]
```

## JSON : échanger des données

**JSON** (*JavaScript Object Notation*) est le format texte utilisé pour échanger des données avec un serveur. Il ressemble aux objets JavaScript, avec des clés **entre guillemets doubles**.

```js
const utilisateur = { nom: "Emma", age: 24 };
const texte = JSON.stringify(utilisateur);
console.log(texte);
const objet = JSON.parse('{"nom":"Lucas","age":27}');
console.log(objet.age);
```

```text
{"nom":"Emma","age":24}
27
```

`JSON.stringify` transforme un objet en texte ; `JSON.parse` fait l'inverse.

## À retenir

- `{ cle: valeur }` ; accès par `objet.cle` ou `objet["cle"]`.
- Propriété absente → `undefined`.
- Méthode = fonction dans un objet ; `this` désigne l'objet.
- Tableaux d'objets + `filter` / `map` / `reduce` : la base des applications.
- `JSON.stringify` / `JSON.parse` pour convertir en texte et inversement.

## Exercices

### Exercice 1 — Fiche livre

Créez un objet `livre` (titre, auteur, pages), puis affichez `« Le Petit Prince » de Saint-Exupéry, 96 pages`.

```solution-js
const livre = { titre: "Le Petit Prince", auteur: "Saint-Exupéry", pages: 96 };
console.log(`« ${livre.titre} » de ${livre.auteur}, ${livre.pages} pages`);
```

```text
« Le Petit Prince » de Saint-Exupéry, 96 pages
```

### Exercice 2 — Panier

Avec le panier ci-dessous, calculez le total (prix × quantité).

```solution-js
const panier = [
  { produit: "Stylo", prix: 2, quantite: 5 },
  { produit: "Cahier", prix: 4, quantite: 3 },
];
const total = panier.reduce((t, ligne) => t + ligne.prix * ligne.quantite, 0);
console.log(total);
```

```text
22
```

### Exercice 3 — Trouver un étudiant

Dans `[{ nom: "Amina", note: 16 }, { nom: "Lucas", note: 9 }]`, trouvez l'objet de Lucas avec `find` et affichez sa note.

```solution-js
const etudiants = [{ nom: "Amina", note: 16 }, { nom: "Lucas", note: 9 }];
const lucas = etudiants.find((e) => e.nom === "Lucas");
console.log(lucas.note);
```

```text
9
```
"""

# ---------------------------------------------------------------------------
# Module 4 — Manipuler une page web
# ---------------------------------------------------------------------------
M4_L1 = r"""
## Le DOM

Quand le navigateur charge une page HTML, il la transforme en un arbre d'objets : le **DOM** (*Document Object Model*). Chaque balise devient un objet que JavaScript peut lire et modifier. Modifier le DOM modifie **immédiatement** ce qui est affiché.

Pour cette leçon, partons de cette page :

```html
<h1 id="titre">Mes tâches</h1>
<p class="info">Aucune tâche pour l'instant.</p>
<ul id="liste">
  <li>Lire la leçon</li>
  <li>Faire les exercices</li>
</ul>
```

## Sélectionner des éléments

```js
const titre = document.querySelector("#titre");       // par identifiant
const info = document.querySelector(".info");         // premier élément de la classe
const items = document.querySelectorAll("#liste li"); // tous les éléments correspondants
console.log(items.length); // 2
```

`querySelector` et `querySelectorAll` utilisent les **sélecteurs CSS** : `#id`, `.classe`, `balise`, `parent enfant`. `querySelector` renvoie le premier élément trouvé, ou `null` s'il n'y en a aucun.

## Modifier le contenu

```js
titre.textContent = "Ma liste du jour";
info.textContent = `Vous avez ${items.length} tâches.`;
```

`textContent` remplace le texte d'un élément.

> Il existe aussi `innerHTML`, qui interprète le texte comme du HTML. **Ne l'utilisez jamais avec une donnée saisie par un utilisateur** : un texte malveillant pourrait injecter du code dans la page (faille XSS). `textContent` est sûr.

## Modifier les classes et les styles

La bonne pratique consiste à définir l'apparence en CSS et à **ajouter ou retirer des classes** en JavaScript :

```css
.termine { text-decoration: line-through; color: gray; }
.cache { display: none; }
```

```js
items[0].classList.add("termine");
info.classList.toggle("cache");      // ajoute la classe si absente, la retire sinon
console.log(items[0].classList.contains("termine")); // true
```

On peut aussi modifier un style directement, pour un cas ponctuel :

```js
titre.style.color = "#0B4BD6";
```

## Les attributs

```js
const lien = document.querySelector("a");
lien.setAttribute("href", "https://smk-academy.netlify.app");
console.log(lien.getAttribute("href"));
const image = document.querySelector("img");
image.alt = "Logo SMK Academy";
```

## À retenir

- Le DOM est la représentation de la page en objets JavaScript.
- `document.querySelector(selecteurCss)` et `querySelectorAll(…)`.
- `textContent` pour le texte ; jamais `innerHTML` avec une saisie utilisateur.
- `classList.add / remove / toggle / contains` pour l'apparence.

## Exercices

### Exercice 1 — Changer le titre

Avec la page de la leçon, écrivez le code qui remplace le texte du `<h1>` par « Planning » et lui ajoute la classe `important`.

```solution-js
const titre = document.querySelector("#titre");
titre.textContent = "Planning";
titre.classList.add("important");
```

### Exercice 2 — Compter et afficher

Affichez dans le paragraphe `.info` le nombre d'éléments `<li>` de la liste, sous la forme « 2 tâche(s) ».

```solution-js
const items = document.querySelectorAll("#liste li");
document.querySelector(".info").textContent = `${items.length} tâche(s)`;
```

### Exercice 3 — Pourquoi pas innerHTML ?

Un développeur écrit `zone.innerHTML = saisieUtilisateur;`. Quel est le risque, et quelle est la correction ?

```solution-text
Si l'utilisateur saisit du HTML contenant du script (par exemple une balise <img> avec un attribut onerror),
le navigateur l'exécute : c'est une faille XSS, qui peut voler la session d'autres utilisateurs.
Correction : zone.textContent = saisieUtilisateur;  (le texte est affiché tel quel, jamais interprété)
```
"""

M4_L2 = r"""
## Réagir aux actions de l'utilisateur

Un **événement** est un signal envoyé par le navigateur : clic, saisie au clavier, envoi d'un formulaire, chargement… On l'écoute avec `addEventListener` :

```html
<button id="bouton">Cliquez-moi</button>
<p id="compteur">0 clic</p>
```

```js
const bouton = document.querySelector("#bouton");
const compteur = document.querySelector("#compteur");
let clics = 0;

bouton.addEventListener("click", () => {
  clics++;
  compteur.textContent = `${clics} clic${clics > 1 ? "s" : ""}`;
});
```

`addEventListener(type, fonction)` : la fonction (appelée **gestionnaire**) s'exécute **à chaque fois** que l'événement se produit, et non au moment où le code est lu.

## Les événements courants

| Événement | Déclenché quand… |
|---|---|
| `click` | on clique sur l'élément |
| `input` | la valeur d'un champ change (à chaque frappe) |
| `change` | la valeur d'un champ est validée (case cochée, liste choisie) |
| `submit` | un formulaire est envoyé |
| `keydown` | une touche est enfoncée |
| `DOMContentLoaded` | la page HTML est entièrement chargée |

## L'objet événement

Le gestionnaire reçoit un objet décrivant l'événement :

```js
const champ = document.querySelector("#recherche");
const apercu = document.querySelector("#apercu");

champ.addEventListener("input", (event) => {
  apercu.textContent = `Vous cherchez : ${event.target.value}`;
});
```

`event.target` désigne l'élément concerné ; `.value` contient le texte saisi dans un champ.

```js
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    console.log("Fermeture de la fenêtre");
  }
});
```

## Créer et supprimer des éléments

```js
const liste = document.querySelector("#liste");

const nouvel = document.createElement("li");   // crée l'élément
nouvel.textContent = "Réviser le quiz";        // lui donne un texte (sûr)
liste.append(nouvel);                          // l'ajoute à la fin de la liste

nouvel.remove();                               // le retire de la page
```

## La délégation d'événements

Pour réagir aux clics sur des éléments **créés dynamiquement**, on écoute leur parent une seule fois :

```js
liste.addEventListener("click", (event) => {
  if (event.target.tagName === "LI") {
    event.target.classList.toggle("termine");
  }
});
```

Tous les `<li>`, présents ou futurs, réagissent au clic, sans ajouter un écouteur à chacun.

## À retenir

- `element.addEventListener("click", fonction)` ; la fonction s'exécute à chaque événement.
- `click`, `input`, `change`, `submit`, `keydown`.
- `event.target` désigne l'élément ; `.value` sa valeur.
- `createElement`, `textContent`, `append`, `remove`.
- Délégation : un écouteur sur le parent pour tous les enfants.

## Exercices

### Exercice 1 — Afficher / masquer

Un bouton `#toggle` doit afficher ou masquer le paragraphe `#details` à chaque clic (classe CSS `cache`).

```solution-js
const toggle = document.querySelector("#toggle");
const details = document.querySelector("#details");
toggle.addEventListener("click", () => {
  details.classList.toggle("cache");
});
```

### Exercice 2 — Compteur de caractères

Sous une zone `<textarea id="message">`, affichez dans `#reste` le nombre de caractères restants sur 280, à chaque frappe.

```solution-js
const message = document.querySelector("#message");
const reste = document.querySelector("#reste");
message.addEventListener("input", () => {
  reste.textContent = `${280 - message.value.length} caractères restants`;
});
```

### Exercice 3 — Ajouter un élément

Au clic sur `#ajouter`, ajoutez à `#liste` un `<li>` contenant le texte du champ `#tache`, puis videz le champ (ignorez un champ vide).

```solution-js
const champ = document.querySelector("#tache");
const liste = document.querySelector("#liste");
document.querySelector("#ajouter").addEventListener("click", () => {
  const texte = champ.value.trim();
  if (!texte) return;
  const li = document.createElement("li");
  li.textContent = texte;
  liste.append(li);
  champ.value = "";
});
```
"""

M4_L3 = r"""
## Intercepter l'envoi d'un formulaire

Par défaut, envoyer un formulaire recharge la page. Pour traiter les données en JavaScript, on écoute l'événement `submit` et on **empêche le comportement par défaut** :

```html
<form id="inscription" novalidate>
  <label for="email">Email</label>
  <input id="email" name="email" type="email" required>
  <label for="age">Âge</label>
  <input id="age" name="age" type="number">
  <button type="submit">S'inscrire</button>
  <p id="erreur" role="alert"></p>
</form>
```

```js
const form = document.querySelector("#inscription");
form.addEventListener("submit", (event) => {
  event.preventDefault();               // pas de rechargement
  const donnees = new FormData(form);
  const email = donnees.get("email").trim();
  const age = Number(donnees.get("age"));
  console.log(email, age);
});
```

`FormData` lit tous les champs d'un formulaire par leur attribut `name`. Rappel : les valeurs sont des **chaînes**, d'où `Number()`.

## Valider les données

La validation consiste à vérifier les données **avant** de les utiliser, et à expliquer clairement les erreurs :

```js
function valider(email, age) {
  const erreurs = [];
  if (!email.includes("@")) erreurs.push("L'adresse email n'est pas valide.");
  if (!Number.isInteger(age) || age < 16) erreurs.push("Vous devez avoir au moins 16 ans.");
  return erreurs;
}
console.log(valider("amina@exemple.fr", 22));
console.log(valider("amina", 12));
```

```text
[]
[
  "L'adresse email n'est pas valide.",
  'Vous devez avoir au moins 16 ans.'
]
```

(Node.js et la console affichent un tableau sur plusieurs lignes quand il est long.)

Séparer la validation dans une fonction qui **renvoie** la liste des erreurs permet de la tester facilement.

## Afficher les erreurs

```js
form.addEventListener("submit", (event) => {
  event.preventDefault();
  const donnees = new FormData(form);
  const erreurs = valider(donnees.get("email").trim(), Number(donnees.get("age")));
  const zone = document.querySelector("#erreur");
  if (erreurs.length > 0) {
    zone.textContent = erreurs.join(" ");
    return;
  }
  zone.textContent = "";
  form.reset();
  alert("Inscription enregistrée !");
});
```

L'attribut `role="alert"` fait lire le message par les lecteurs d'écran : l'erreur est **accessible** à tous.

## La validation intégrée au HTML

Les attributs `required`, `type="email"`, `min`, `max`, `minlength`, `pattern` déclenchent une validation par le navigateur, sans JavaScript. On peut l'interroger :

```js
const champEmail = document.querySelector("#email");
console.log(champEmail.checkValidity());      // true ou false
console.log(champEmail.validationMessage);    // message du navigateur
```

L'attribut `novalidate` sur le formulaire désactive les bulles du navigateur pour afficher vos propres messages.

## La règle de sécurité fondamentale

La validation en JavaScript améliore le **confort** de l'utilisateur, mais elle **ne protège rien** : n'importe qui peut la contourner (outils de développement, requête directe au serveur). **Le serveur doit toujours revérifier les données.** C'est exactement ce que fait SMK Academy : les notes de vos quiz sont calculées par la base de données, jamais par le navigateur.

## À retenir

- `submit` + `event.preventDefault()` pour traiter le formulaire en JavaScript.
- `new FormData(form).get("name")` ; les valeurs sont des chaînes.
- Une fonction de validation qui renvoie la liste des erreurs.
- Messages d'erreur clairs et accessibles (`role="alert"`).
- La validation côté navigateur ne remplace jamais celle du serveur.

## Exercices

### Exercice 1 — Fonction de validation

Écrivez `validerMotDePasse(mdp)` qui renvoie la liste des erreurs : au moins 8 caractères, au moins un chiffre. Testez avec `"abc"` puis `"securite2026"`.

```solution-js
function validerMotDePasse(mdp) {
  const erreurs = [];
  if (mdp.length < 8) erreurs.push("8 caractères minimum");
  if (!/[0-9]/.test(mdp)) erreurs.push("au moins un chiffre");
  return erreurs;
}
console.log(validerMotDePasse("abc"));
console.log(validerMotDePasse("securite2026"));
```

```text
[ '8 caractères minimum', 'au moins un chiffre' ]
[]
```

### Exercice 2 — Vrai ou faux ?

« Puisque mon formulaire vérifie l'email en JavaScript, mon serveur peut faire confiance aux emails reçus. »

```solution-text
Faux. La validation côté navigateur se contourne facilement (désactivation du script, outils de
développement, envoi direct d'une requête). Le serveur doit toujours revérifier toutes les données reçues.
```
"""

# ---------------------------------------------------------------------------
# Module 5 — L'asynchrone et fetch
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Le problème de l'attente

Certaines opérations prennent du temps : télécharger des données, attendre une réponse d'un serveur, lire un fichier. Si JavaScript attendait sans rien faire, la page entière serait **figée** pendant ce temps. JavaScript lance donc ces opérations et **continue** son travail : c'est la programmation **asynchrone**.

## `setTimeout` : exécuter plus tard

```js
console.log("Début");
setTimeout(() => {
  console.log("Deux secondes plus tard");
}, 2000);
console.log("Fin");
```

```text
Début
Fin
Deux secondes plus tard
```

« Fin » s'affiche **avant** le message différé : `setTimeout` programme la fonction, puis le programme continue immédiatement.

Même avec un délai de 0, la fonction attend que le code en cours soit terminé :

```js
setTimeout(() => console.log("B"), 0);
console.log("A");
```

```text
A
B
```

JavaScript exécute **une seule chose à la fois**. Les fonctions différées sont placées dans une **file d'attente** et exécutées quand le code en cours est terminé.

## Les promesses

Une **promesse** (*Promise*) représente un résultat qui arrivera plus tard. Elle est d'abord **en attente**, puis soit **tenue** (*fulfilled*, avec une valeur), soit **rompue** (*rejected*, avec une erreur).

```js
function attendre(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

attendre(500).then(() => {
  console.log("500 ms écoulées");
});
```

```text
500 ms écoulées
```

- `.then(fonction)` s'exécute quand la promesse est tenue ;
- `.catch(fonction)` s'exécute en cas d'erreur.

```js
function diviser(a, b) {
  return new Promise((resolve, reject) => {
    if (b === 0) reject(new Error("Division par zéro"));
    else resolve(a / b);
  });
}

diviser(10, 2).then((r) => console.log(r));
diviser(1, 0).catch((e) => console.log(`Erreur : ${e.message}`));
```

```text
5
Erreur : Division par zéro
```

Vous écrirez rarement `new Promise` vous-même : les fonctions du navigateur (comme `fetch`) **renvoient** déjà des promesses. L'essentiel est de savoir les **utiliser**, ce que la leçon suivante simplifie avec `async` / `await`.

## À retenir

- Asynchrone : une opération longue est lancée, le programme continue.
- `setTimeout(fonction, ms)` exécute plus tard ; le code suivant s'exécute d'abord.
- Une promesse est en attente, puis tenue (`.then`) ou rompue (`.catch`).

## Exercices

### Exercice 1 — Prédisez l'ordre

Dans quel ordre s'affichent les lettres ?

```solution-js
console.log("1");
setTimeout(() => console.log("2"), 0);
console.log("3");
```

```text
1
3
2
```

### Exercice 2 — Promesse de vérification

Écrivez une fonction `verifierAge(age)` qui renvoie une promesse tenue avec `"Accès autorisé"` si l'âge est supérieur ou égal à 18, rompue avec l'erreur `"Accès refusé"` sinon. Testez avec 20 et 15.

```solution-js
function verifierAge(age) {
  return new Promise((resolve, reject) => {
    if (age >= 18) resolve("Accès autorisé");
    else reject(new Error("Accès refusé"));
  });
}
verifierAge(20).then((m) => console.log(m));
verifierAge(15).catch((e) => console.log(e.message));
```

```text
Accès autorisé
Accès refusé
```
"""

M5_L2 = r"""
## `async` et `await`

`async` / `await` permet d'écrire du code asynchrone **comme s'il était séquentiel**, sans enchaîner les `.then` :

```js
const attendre = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function demo() {
  console.log("Étape 1");
  await attendre(300);
  console.log("Étape 2, après 300 ms");
}
demo();
```

```text
Étape 1
Étape 2, après 300 ms
```

- `async` devant une fonction indique qu'elle contient des opérations asynchrones ; elle renvoie toujours une promesse ;
- `await` **attend** le résultat d'une promesse avant de passer à la ligne suivante, sans figer la page.

`await` ne s'utilise qu'à l'intérieur d'une fonction `async` (ou au premier niveau d'un module JavaScript).

## Gérer les erreurs : `try` / `catch`

```js
async function charger() {
  try {
    await Promise.reject(new Error("Serveur indisponible"));
    console.log("Jamais affiché");
  } catch (erreur) {
    console.log(`Problème : ${erreur.message}`);
  }
}
charger();
```

```text
Problème : Serveur indisponible
```

Si une promesse attendue avec `await` est rompue, l'exécution saute directement dans le bloc `catch`.

## Récupérer des données avec `fetch`

`fetch(url)` envoie une requête HTTP et renvoie une promesse de **réponse**. Le schéma standard :

```js
async function chargerUtilisateurs() {
  try {
    const reponse = await fetch("https://jsonplaceholder.typicode.com/users");
    if (!reponse.ok) {
      throw new Error(`Erreur HTTP ${reponse.status}`);
    }
    const utilisateurs = await reponse.json();
    console.log(`${utilisateurs.length} utilisateurs reçus`);
    console.log(utilisateurs[0].name);
  } catch (erreur) {
    console.log(`Impossible de charger les données : ${erreur.message}`);
  }
}
chargerUtilisateurs();
```

Trois étapes, trois points d'attention :

1. `await fetch(url)` : attend la réponse du serveur ;
2. `reponse.ok` : **`fetch` ne lève pas d'erreur pour un code 404 ou 500**, il faut vérifier le statut soi-même ;
3. `await reponse.json()` : lit le corps de la réponse et le convertit en objet JavaScript.

*JSONPlaceholder* est un service public de démonstration : la requête ci-dessus fonctionne depuis votre navigateur et renvoie dix utilisateurs fictifs.

## Envoyer des données

```js
async function creerTache(titre) {
  const reponse = await fetch("https://jsonplaceholder.typicode.com/todos", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title: titre, completed: false }),
  });
  return reponse.json();
}
```

`method` choisit le type de requête, `headers` décrit le format, `body` contient les données en JSON.

## Afficher les données dans la page

```js
async function afficherUtilisateurs() {
  const liste = document.querySelector("#utilisateurs");
  liste.textContent = "Chargement…";
  try {
    const reponse = await fetch("https://jsonplaceholder.typicode.com/users");
    if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
    const utilisateurs = await reponse.json();
    liste.textContent = "";
    for (const u of utilisateurs) {
      const li = document.createElement("li");
      li.textContent = `${u.name} (${u.email})`;
      liste.append(li);
    }
  } catch (erreur) {
    liste.textContent = "Le chargement a échoué. Réessayez plus tard.";
  }
}
```

Prévoyez toujours trois états : **chargement**, **succès**, **erreur**.

## À retenir

- `async function` + `await promesse` pour un code lisible.
- `try` / `catch` pour gérer les erreurs.
- `fetch(url)` → vérifier `reponse.ok` → `await reponse.json()`.
- `POST` : `method`, `headers`, `body: JSON.stringify(…)`.
- Afficher les états chargement, succès et erreur.

## Exercices

### Exercice 1 — Réécrire avec async/await

Réécrivez avec `async` / `await` : `attendre(200).then(() => console.log("Prêt"));` (avec la fonction `attendre` de la leçon).

```solution-js
const attendre = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
async function main() {
  await attendre(200);
  console.log("Prêt");
}
main();
```

```text
Prêt
```

### Exercice 2 — Trouvez l'oubli

Ce code n'affiche aucune erreur quand l'URL n'existe pas (404). Pourquoi, et comment le corriger ?

```solution-text
fetch ne rejette sa promesse qu'en cas d'échec réseau ; une réponse 404 ou 500 est considérée comme « reçue ».
Il faut tester le statut : if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
avant d'appeler reponse.json().
```

### Exercice 3 — Charger une tâche

Écrivez une fonction `async` qui charge `https://jsonplaceholder.typicode.com/todos/1` et affiche son titre, avec gestion des erreurs.

```solution-js
async function chargerTache() {
  try {
    const reponse = await fetch("https://jsonplaceholder.typicode.com/todos/1");
    if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
    const tache = await reponse.json();
    console.log(tache.title);
  } catch (erreur) {
    console.log(`Échec : ${erreur.message}`);
  }
}
chargerTache();
```
"""

M5_L3 = r"""
## Le projet

Vous allez construire une **liste de tâches** complète qui mobilise toute la formation :

- ajouter une tâche depuis un formulaire ;
- cocher une tâche terminée ;
- supprimer une tâche ;
- afficher le nombre de tâches restantes ;
- **conserver les tâches** après un rechargement de la page.

Créez trois fichiers dans un même dossier : `index.html`, `style.css` et `app.js`, puis ouvrez `index.html` dans votre navigateur.

## Étape 1 — La page HTML

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mes tâches</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <main>
      <h1>Mes tâches</h1>
      <form id="formulaire">
        <label for="champ">Nouvelle tâche</label>
        <input id="champ" name="titre" maxlength="100" required>
        <button type="submit">Ajouter</button>
      </form>
      <ul id="liste"></ul>
      <p id="resume" aria-live="polite"></p>
    </main>
    <script src="app.js"></script>
  </body>
</html>
```

## Étape 2 — Un peu de style

```css
body { font-family: system-ui, sans-serif; max-width: 32rem; margin: 2rem auto; padding: 0 1rem; }
form { display: flex; gap: .5rem; flex-wrap: wrap; }
input { flex: 1; padding: .5rem; }
li { display: flex; align-items: center; gap: .5rem; padding: .4rem 0; }
li.terminee span { text-decoration: line-through; color: gray; }
```

## Étape 3 — Les données et la logique

La règle d'or : les **données** (un tableau d'objets) sont la source de vérité ; l'affichage est **recalculé** à partir d'elles à chaque changement.

```js
let taches = [];
let prochainId = 1;

function ajouter(titre) {
  taches.push({ id: prochainId++, titre, terminee: false });
}

function basculer(id) {
  taches = taches.map((t) => (t.id === id ? { ...t, terminee: !t.terminee } : t));
}

function supprimer(id) {
  taches = taches.filter((t) => t.id !== id);
}

function restantes() {
  return taches.filter((t) => !t.terminee).length;
}

ajouter("Lire la leçon");
ajouter("Faire le quiz");
basculer(taches[0].id);
console.log(taches.map((t) => `${t.titre} : ${t.terminee ? "faite" : "à faire"}`));
console.log(restantes());
```

```text
[ 'Lire la leçon : faite', 'Faire le quiz : à faire' ]
1
```

`{ ...t, terminee: !t.terminee }` crée une **copie** de l'objet en inversant `terminee`.

Chaque tâche reçoit un identifiant unique grâce au compteur `prochainId`.

> Piège classique : utiliser `Date.now()` comme identifiant. Deux tâches créées dans la même milliseconde (comme ici, l'une après l'autre) reçoivent alors le **même** identifiant, et cocher l'une coche aussi l'autre. Dans une vraie application, utilisez `crypto.randomUUID()`, disponible dans tous les navigateurs récents.

## Étape 4 — L'affichage

```js
const liste = document.querySelector("#liste");
const resume = document.querySelector("#resume");

function afficher() {
  liste.textContent = "";
  for (const tache of taches) {
    const li = document.createElement("li");
    li.dataset.id = tache.id;
    li.classList.toggle("terminee", tache.terminee);

    const caseACocher = document.createElement("input");
    caseACocher.type = "checkbox";
    caseACocher.checked = tache.terminee;
    caseACocher.setAttribute("aria-label", `Marquer « ${tache.titre} » comme terminée`);

    const texte = document.createElement("span");
    texte.textContent = tache.titre;

    const bouton = document.createElement("button");
    bouton.textContent = "Supprimer";

    li.append(caseACocher, texte, bouton);
    liste.append(li);
  }
  const n = restantes();
  resume.textContent = n === 0 ? "Tout est fait !" : `${n} tâche(s) restante(s)`;
}
```

## Étape 5 — Les événements

```js
document.querySelector("#formulaire").addEventListener("submit", (event) => {
  event.preventDefault();
  const champ = document.querySelector("#champ");
  const titre = champ.value.trim();
  if (!titre) return;
  ajouter(titre);
  champ.value = "";
  enregistrer();
  afficher();
});

liste.addEventListener("click", (event) => {
  const li = event.target.closest("li");
  if (!li) return;
  const id = Number(li.dataset.id);
  if (event.target.type === "checkbox") basculer(id);
  else if (event.target.tagName === "BUTTON") supprimer(id);
  else return;
  enregistrer();
  afficher();
});
```

`closest("li")` remonte jusqu'au `<li>` qui contient l'élément cliqué : c'est la **délégation d'événements**.

## Étape 6 — Conserver les tâches : `localStorage`

`localStorage` stocke du **texte** dans le navigateur, de façon durable, pour ce site uniquement. On y enregistre le tableau en JSON :

```js
function enregistrer() {
  localStorage.setItem("taches", JSON.stringify(taches));
}

function charger() {
  try {
    taches = JSON.parse(localStorage.getItem("taches")) ?? [];
  } catch {
    taches = [];
  }
  prochainId = Math.max(0, ...taches.map((t) => t.id)) + 1;
}

charger();
afficher();
```

`??` fournit une valeur par défaut quand la valeur de gauche est `null` ou `undefined` (aucune donnée enregistrée). Le `try` / `catch` protège contre des données corrompues.

> `localStorage` est visible et modifiable par l'utilisateur, et par tout script exécuté sur la page : n'y stockez **jamais** de mot de passe ni de donnée sensible.

## Pour aller plus loin

- ajouter un filtre « Toutes / À faire / Terminées » ;
- permettre de modifier une tâche par double-clic ;
- synchroniser les tâches avec un serveur grâce à `fetch` (leçon précédente).

## À retenir

- Les données sont la source de vérité ; l'affichage est recalculé à chaque changement.
- `createElement` + `textContent` pour un affichage sûr.
- Délégation d'événements avec `closest`.
- `localStorage` + `JSON.stringify` / `JSON.parse` pour conserver des données non sensibles.
"""

# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------
QUIZ_M3 = [
    ("single", "Que renvoie une fonction qui ne contient aucun return ?", None,
     ["0", "null", "undefined", "Une erreur"], [2],
     "Sans return, une fonction renvoie undefined."),
    ("single", "Qu'affiche ce code ?", "const double = (n) => n * 2;\nconsole.log(double(7));",
     ["7", "14", "undefined", "n * 2"], [1],
     "Avec une fonction fléchée sur une ligne, le return est implicite : double(7) vaut 14."),
    ("single", "Quelle est la différence entre console.log et return dans une fonction ?", None,
     ["Aucune", "console.log affiche, return renvoie une valeur utilisable par le reste du programme", "return affiche dans la console", "console.log arrête la fonction"], [1],
     "console.log se contente d'afficher ; return transmet le résultat à l'appelant, qui peut le réutiliser."),
    ("single", "Quelle méthode ajoute un élément à la fin d'un tableau ?", None,
     ["pop", "push", "shift", "unshift"], [1],
     "push ajoute à la fin, pop retire le dernier, unshift ajoute au début."),
    ("single", "Que renvoie [1, 2, 3, 4].filter((n) => n % 2 === 0) ?", None,
     ["[1, 3]", "[2, 4]", "2", "[false, true, false, true]"], [1],
     "filter garde les éléments qui vérifient la condition : les nombres pairs 2 et 4."),
    ("single", "Que renvoie [1, 2, 3].map((n) => n * 10) ?", None,
     ["[10, 20, 30]", "60", "[1, 2, 3]", "30"], [0],
     "map applique la fonction à chaque élément et renvoie un nouveau tableau de même longueur."),
    ("single", "Que vaut [5, 10, 15].reduce((s, n) => s + n, 0) ?", None,
     ["15", "30", "[5, 15, 30]", "0"], [1],
     "reduce part de 0 et ajoute chaque élément : 0 + 5 + 10 + 15 = 30."),
    ("multiple", "Quelles méthodes renvoient un NOUVEAU tableau sans modifier l'original ?", None,
     ["map", "filter", "push", "sort"], [0, 1],
     "map et filter créent un nouveau tableau. push et sort modifient le tableau existant : d'où la copie [...tableau] avant un tri."),
    ("single", "Avec const user = { nom: \"Emma\" }, que vaut user.age ?", None,
     ["0", "null", "undefined", "Une erreur"], [2],
     "Une propriété absente d'un objet vaut undefined (aucune erreur n'est levée)."),
    ("single", "Que fait JSON.stringify({ a: 1 }) ?", None,
     ["Il renvoie le texte '{\"a\":1}'", "Il renvoie l'objet { a: 1 }", "Il affiche l'objet", "Il lève une erreur"], [0],
     "JSON.stringify convertit un objet en texte au format JSON ; JSON.parse fait l'inverse."),
]

QUIZ_M4 = [
    ("single", "Qu'est-ce que le DOM ?", None,
     ["Un langage de style", "La représentation de la page HTML sous forme d'objets manipulables par JavaScript", "Un serveur web", "Une base de données du navigateur"], [1],
     "Le DOM (Document Object Model) est l'arbre d'objets construit par le navigateur à partir du HTML."),
    ("single", "Quelle instruction sélectionne l'élément dont l'identifiant est « menu » ?", None,
     ["document.querySelector(\".menu\")", "document.querySelector(\"#menu\")", "document.querySelector(\"menu\")", "document.getElement(\"menu\")"], [1],
     "querySelector utilise les sélecteurs CSS : # pour un identifiant, . pour une classe."),
    ("single", "Pourquoi utiliser textContent plutôt qu'innerHTML pour afficher une saisie utilisateur ?", None,
     ["textContent est plus rapide à écrire", "innerHTML interprète le HTML et peut exécuter du code injecté (faille XSS)", "innerHTML ne fonctionne pas dans les listes", "Il n'y a aucune différence"], [1],
     "textContent affiche le texte tel quel ; innerHTML l'interprète, ce qui ouvre la porte aux injections."),
    ("single", "Que fait element.classList.toggle(\"actif\") ?", None,
     ["Ajoute toujours la classe", "Retire toujours la classe", "Ajoute la classe si elle est absente, la retire sinon", "Vérifie si la classe existe"], [2],
     "toggle bascule la présence de la classe ; contains vérifie sa présence."),
    ("single", "Quand la fonction passée à addEventListener(\"click\", f) s'exécute-t-elle ?", None,
     ["Immédiatement", "À chaque clic sur l'élément", "Une seule fois, au premier clic", "Au chargement de la page"], [1],
     "Le gestionnaire est exécuté à chaque fois que l'événement se produit."),
    ("single", "Dans un gestionnaire d'événement, que désigne event.target ?", None,
     ["La page entière", "L'élément sur lequel l'événement s'est produit", "La fonction gestionnaire", "Le formulaire"], [1],
     "event.target est l'élément concerné par l'événement (bouton cliqué, champ modifié…)."),
    ("single", "Quel événement se déclenche à chaque frappe dans un champ de texte ?", None,
     ["click", "submit", "input", "load"], [2],
     "input se déclenche à chaque modification de la valeur ; change seulement à la validation."),
    ("single", "À quoi sert event.preventDefault() dans un gestionnaire submit ?", None,
     ["À vider le formulaire", "À empêcher l'envoi et le rechargement par défaut de la page", "À valider les champs", "À supprimer le formulaire"], [1],
     "preventDefault empêche le comportement par défaut (envoi et rechargement) pour traiter les données en JavaScript."),
    ("multiple", "Quelles affirmations sur la validation des formulaires sont exactes ?", None,
     ["La validation en JavaScript améliore le confort de l'utilisateur.", "La validation en JavaScript suffit à protéger le serveur.", "Le serveur doit toujours revérifier les données.", "Les valeurs lues dans un formulaire sont des chaînes de caractères."], [0, 2, 3],
     "La validation côté navigateur se contourne : seul le serveur peut garantir la validité des données."),
    ("single", "Quel est l'avantage de la délégation d'événements ?", None,
     ["Elle accélère le chargement des images", "Un seul écouteur sur le parent gère aussi les éléments ajoutés plus tard", "Elle remplace le CSS", "Elle empêche les clics"], [1],
     "En écoutant le parent, on gère tous les enfants, y compris ceux créés dynamiquement."),
]

QUIZ_M5 = [
    ("single", "Dans quel ordre s'affichent les messages ?", "console.log(\"A\");\nsetTimeout(() => console.log(\"B\"), 0);\nconsole.log(\"C\");",
     ["A, B, C", "A, C, B", "B, A, C", "C, B, A"], [1],
     "Même avec un délai de 0, la fonction différée attend la fin du code en cours : A, C, puis B."),
    ("single", "Que représente une promesse (Promise) ?", None,
     ["Une variable constante", "Un résultat qui sera disponible plus tard, ou une erreur", "Une boucle infinie", "Un événement de clic"], [1],
     "Une promesse est d'abord en attente, puis tenue (avec une valeur) ou rompue (avec une erreur)."),
    ("single", "Quelle méthode s'exécute quand une promesse est rompue ?", None,
     [".then()", ".catch()", ".finally() uniquement", ".resolve()"], [1],
     ".catch() traite les erreurs ; .then() le résultat d'une promesse tenue."),
    ("single", "Où peut-on utiliser await ?", None,
     ["Partout", "Dans une fonction déclarée async (ou au premier niveau d'un module)", "Uniquement dans une boucle", "Uniquement avec setTimeout"], [1],
     "await n'est autorisé que dans une fonction async ou au premier niveau d'un module JavaScript."),
    ("single", "Que renvoie fetch(url) ?", None,
     ["Directement les données JSON", "Une promesse de réponse HTTP", "Le code HTML de la page", "Un tableau"], [1],
     "fetch renvoie une promesse qui se résout en un objet Response ; il faut ensuite appeler reponse.json()."),
    ("true_false", "fetch rejette automatiquement sa promesse quand le serveur répond 404.", None,
     ["Vrai", "Faux"], [1],
     "fetch ne rejette qu'en cas d'échec réseau. Pour un 404 ou un 500, il faut tester reponse.ok soi-même."),
    ("single", "Comment lire le corps JSON d'une réponse fetch ?", None,
     ["reponse.body", "await reponse.json()", "JSON.parse(reponse)", "reponse.text"], [1],
     "reponse.json() renvoie une promesse du contenu converti en objet ; on l'attend avec await."),
    ("single", "Quel bloc intercepte une erreur levée pendant un await ?", None,
     ["if / else", "try / catch", "switch", "for"], [1],
     "Avec async/await, les erreurs se gèrent avec try / catch."),
    ("single", "Que stocke localStorage ?", None,
     ["Des objets JavaScript directement", "Du texte, propre au site, conservé après rechargement", "Des fichiers sur le serveur", "Des mots de passe chiffrés"], [1],
     "localStorage stocke des chaînes ; on convertit les objets avec JSON.stringify et JSON.parse."),
    ("multiple", "Quelles données NE doivent PAS être stockées dans localStorage ?", None,
     ["Un mot de passe", "La liste de tâches d'un exercice", "Un jeton d'accès sensible", "Le thème clair ou sombre choisi"], [0, 2],
     "localStorage est lisible par tout script de la page : jamais de mot de passe ni de secret. Des préférences ou des données d'exercice conviennent."),
]
