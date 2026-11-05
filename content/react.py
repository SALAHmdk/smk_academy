"""Contenu de la formation « React » (SMK Academy).

Blocs ```jsx pour les composants (non exécutés par le contrôle automatique : relus, analysés avec ESLint
— règles des hooks, clés de listes, variables non définies — et rendus avec react-dom/server pendant la rédaction).
Blocs ```js pour les fonctions pures (reducers, filtres, utilitaires) : exécutés par
scripts/check_code_blocks.py, qui compare leur sortie au bloc ```text qui suit.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("react_m3_m5", _Path(__file__).with_name("react_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "react",
    "title": "React",
    "subtitle": "Construire des interfaces avec des composants.",
    "description": (
        "React est une bibliothèque JavaScript qui permet de construire des interfaces à partir de composants "
        "réutilisables. Cette formation part de la création d'un projet avec Vite pour aborder le JSX, les props, "
        "l'état, les événements, les listes et les formulaires contrôlés, puis les effets, le contexte, les hooks "
        "personnalisés et les appels réseau. Elle se termine par un mini-projet complet : un annuaire filtrable "
        "alimenté par une API ; chaque module se conclut par un quiz noté sur 20."
    ),
    "category": "Développement web",
    "category_slug": "developpement-web",
    "topic": "React",
    "cover_label": "Re",
    "level": "intermediaire",
    "duration_minutes": 720,
    "objectives": [
        "Créer des composants et gérer l'état",
        "Utiliser les hooks (useState, useEffect, useReducer, useRef, useContext et hooks personnalisés)",
        "Consommer une API avec fetch en gérant chargement et erreurs",
    ],
    "prerequisites": [
        "JavaScript pour débutants (fonctions, tableaux, objets, fetch et async/await)",
        "Notions de HTML et de CSS",
    ],
    "status": "published",
    "is_premium": False,
    "position": 22,
}

# ---------------------------------------------------------------------------
# Module 1 — Premiers pas avec React
# ---------------------------------------------------------------------------
M1_L1 = r"""
## Qu'est-ce que React ?

**React** est une **bibliothèque** JavaScript, créée par Meta (anciennement Facebook) et distribuée en open source, qui sert à construire des **interfaces utilisateur**. Une interface React est découpée en **composants** : des morceaux d'écran autonomes et réutilisables (un bouton, une carte produit, un formulaire, une page entière).

> On parle de **bibliothèque** et non de *framework* (cadre complet) : React s'occupe de l'affichage. Le routage, l'accès aux données ou la mise en forme sont confiés à d'autres outils, que vous choisissez.

## Impératif ou déclaratif

Dans la formation JavaScript, vous avez modifié la page **pas à pas** : sélectionner un élément, changer son texte, ajouter une classe. C'est l'approche **impérative** : vous décrivez *comment* passer d'un état de l'écran au suivant.

```jsx
// Approche impérative (JavaScript sans React)
const bouton = document.querySelector("#bouton");
const texte = document.querySelector("#texte");
let compteur = 0;
bouton.addEventListener("click", () => {
  compteur++;
  texte.textContent = `Vous avez cliqué ${compteur} fois`;
});
```

Avec React, vous adoptez une approche **déclarative** : vous décrivez *à quoi doit ressembler* l'écran pour des données précises, et React se charge de mettre la page à jour quand ces données changent. On résume souvent l'idée par une formule : **l'interface est une fonction des données**.

Cette idée se comprend très bien avec une simple fonction JavaScript :

```js
function afficherCompteur(compteur) {
  return `<p>Vous avez cliqué ${compteur} fois</p>`;
}

console.log(afficherCompteur(0));
console.log(afficherCompteur(3));
```

```text
<p>Vous avez cliqué 0 fois</p>
<p>Vous avez cliqué 3 fois</p>
```

Un composant React fonctionne sur ce principe : il reçoit des données et renvoie la description de l'interface correspondante. Quand les données changent, React rappelle le composant, compare la nouvelle description à l'ancienne et ne modifie dans la page que ce qui a réellement changé.

## Ce que vous allez construire

| Notion | Rôle | Module |
|---|---|---|
| JSX | décrire l'interface avec une syntaxe proche du HTML | 1 |
| Composants et props | découper l'écran et transmettre des données | 1 |
| État et événements | réagir aux actions de l'utilisateur | 2 |
| Listes et formulaires | afficher des collections, saisir des données | 3 |
| Effets, réducteurs, contexte | se synchroniser avec l'extérieur, organiser l'état | 4 |
| Appels réseau, hooks personnalisés | charger des données depuis une API | 5 |

## Les rappels JavaScript indispensables

React utilise beaucoup de syntaxes modernes de JavaScript. Vérifiez que vous êtes à l'aise avec chacune d'elles : elles reviendront dans presque tous les exemples.

### Fonctions fléchées

```js
const doubler = (n) => n * 2;
const saluer = (prenom) => `Bonjour ${prenom}`;
console.log(doubler(21));
console.log(saluer("Inès"));
```

```text
42
Bonjour Inès
```

### Déstructuration

La **déstructuration** extrait des valeurs d'un objet ou d'un tableau dans des variables. React l'utilise pour lire les **props** (objet) et l'**état** (tableau de deux éléments).

```js
const utilisateur = { nom: "Rossi", ville: "Lyon", age: 31 };
const { nom, ville } = utilisateur;
console.log(nom, ville);

const paire = ["valeur", "modifier"];
const [premier, second] = paire;
console.log(premier, second);

function presenter({ nom, ville = "inconnue" }) {
  return `${nom} (${ville})`;
}
console.log(presenter({ nom: "Diallo" }));
```

```text
Rossi Lyon
valeur modifier
Diallo (inconnue)
```

La dernière fonction déstructure directement son paramètre et prévoit une **valeur par défaut** pour `ville`.

### L'opérateur de décomposition (*spread*)

`...` recopie le contenu d'un tableau ou d'un objet dans un **nouveau** tableau ou objet. C'est l'outil de base pour modifier des données sans toucher à l'original, ce que React exige.

```js
const fruits = ["pomme", "poire"];
const plusDeFruits = [...fruits, "kiwi"];
console.log(fruits);
console.log(plusDeFruits);

const profil = { nom: "Emma", theme: "clair" };
const profilModifie = { ...profil, theme: "sombre" };
console.log(profil.theme, profilModifie.theme);
```

```text
[ 'pomme', 'poire' ]
[ 'pomme', 'poire', 'kiwi' ]
clair sombre
```

Les propriétés écrites **après** `...profil` remplacent celles de l'original.

### `map`, `filter` et les expressions conditionnelles

```js
const produits = [
  { nom: "Clavier", prix: 45 },
  { nom: "Souris", prix: 20 },
  { nom: "Écran", prix: 180 },
];
const abordables = produits.filter((p) => p.prix < 50);
const noms = abordables.map((p) => p.nom.toUpperCase());
console.log(noms);

const stock = 0;
console.log(stock > 0 ? "Disponible" : "Épuisé");
console.log(stock > 0 && "Disponible");
```

```text
[ 'CLAVIER', 'SOURIS' ]
Épuisé
false
```

`map` servira à afficher des listes, `filter` à les filtrer, le ternaire et `&&` à afficher un élément sous condition.

### Les modules : `import` et `export`

Un projet React est découpé en fichiers. Chaque fichier **exporte** ce qu'il partage et **importe** ce dont il a besoin :

```jsx
// fichier prix.js
export const TVA = 0.2;
export function prixTtc(ht) {
  return ht * (1 + TVA);
}
export default function formaterEuros(montant) {
  return `${montant.toFixed(2)} €`;
}

// fichier App.jsx
import formaterEuros, { prixTtc } from "./prix.js";
console.log(formaterEuros(prixTtc(10))); // 12.00 €
```

- un **export nommé** s'importe entre accolades, avec le même nom ;
- un fichier a au plus un **export par défaut**, importé sans accolades et sous le nom de votre choix.

## À retenir

- React est une bibliothèque d'interfaces fondée sur des **composants** réutilisables.
- Approche **déclarative** : on décrit l'écran pour des données ; React met la page à jour.
- La déstructuration et le *spread* (`...`) sont omniprésents en React.
- `map` et `filter` produisent de **nouveaux** tableaux sans modifier l'original.
- `export` / `import` organisent le code en modules ; un seul export par défaut par fichier.

## Exercices

### Exercice 1 — Déstructuration

Avec `const film = { titre: "Le Voyage", annee: 2019, duree: 112 }`, extrayez `titre` et `duree` par déstructuration, puis affichez `Le Voyage dure 112 minutes`.

```solution-js
const film = { titre: "Le Voyage", annee: 2019, duree: 112 };
const { titre, duree } = film;
console.log(`${titre} dure ${duree} minutes`);
```

```text
Le Voyage dure 112 minutes
```

### Exercice 2 — Modifier sans muter

À partir de `const tache = { id: 1, titre: "Réviser", terminee: false }`, créez un **nouvel** objet `tacheFaite` où `terminee` vaut `true`, sans modifier `tache`. Affichez les deux valeurs de `terminee`.

```solution-js
const tache = { id: 1, titre: "Réviser", terminee: false };
const tacheFaite = { ...tache, terminee: true };
console.log(tache.terminee, tacheFaite.terminee);
```

```text
false true
```

### Exercice 3 — Préparer une liste

Avec `const notes = [12, 7, 15, 9, 18]`, construisez un tableau de textes `"Note : 12"`… ne contenant que les notes supérieures ou égales à 10.

```solution-js
const notes = [12, 7, 15, 9, 18];
const lignes = notes.filter((n) => n >= 10).map((n) => `Note : ${n}`);
console.log(lignes);
```

```text
[ 'Note : 12', 'Note : 15', 'Note : 18' ]
```
"""

M1_L2 = r"""
## Préparer son poste

Pour développer avec React, vous avez besoin de :

- **Node.js** (de préférence une version LTS, c'est-à-dire maintenue à long terme), qui fournit aussi **npm**, le gestionnaire de paquets ;
- un **éditeur de code** (par exemple Visual Studio Code) ;
- un **terminal** et un navigateur récent.

Vérifiez l'installation dans un terminal :

```bash
node --version
npm --version
```

Chaque commande doit afficher un numéro de version.

## Créer un projet avec Vite

**Vite** est un outil de construction (*build tool*) : il lance un serveur de développement qui recharge la page dès que vous enregistrez un fichier, puis prépare une version optimisée pour la mise en ligne. Créez un projet :

```bash
npm create vite@latest mon-app -- --template react
cd mon-app
npm install
npm run dev
```

- `npm create vite@latest mon-app` crée le dossier `mon-app` ; l'option `--template react` choisit le modèle React en JavaScript (sans elle, l'outil vous pose les questions une à une) ;
- `npm install` télécharge les dépendances (dossier `node_modules`) ;
- `npm run dev` démarre le serveur de développement. Ouvrez l'adresse affichée dans le terminal (le plus souvent `http://localhost:5173`).

> Les questions posées et le contenu exact des fichiers générés évoluent avec les versions de Vite. Les principes décrits ici restent valables : un fichier `index.html`, un point d'entrée `src/main.jsx` et un composant `src/App.jsx`.

## La structure du projet

```text
mon-app/
├── index.html          la seule page HTML, avec <div id="root">
├── package.json        dépendances et scripts (dev, build, preview)
├── vite.config.js      configuration de Vite
├── public/             fichiers copiés tels quels (icônes…)
└── src/
    ├── main.jsx        point d'entrée : monte l'application
    ├── App.jsx         composant principal
    └── index.css       styles globaux
```

Le point d'entrée `src/main.jsx` relie React à la page :

```jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <App />
  </StrictMode>
);
```

- `createRoot` prend le contrôle de l'élément `#root` de `index.html` ;
- `render` y affiche le composant `App` ;
- `StrictMode` (mode strict) active en développement des vérifications supplémentaires qui aident à repérer les erreurs ; il n'a aucun effet sur la version de production.

Remplacez le contenu de `src/App.jsx` par :

```jsx
export default function App() {
  return (
    <main>
      <h1>Bonjour React !</h1>
      <p>Ma première application.</p>
    </main>
  );
}
```

Enregistrez : la page se met à jour **immédiatement**, sans rechargement manuel.

## Le JSX

Le code qui ressemble à du HTML dans un fichier `.jsx` s'appelle du **JSX** (*JavaScript XML*). Ce n'est pas du HTML : l'outil de construction le **transforme en appels de fonctions JavaScript** qui décrivent les éléments à afficher. Le JSX est donc une **expression** : on peut le stocker dans une variable, le renvoyer depuis une fonction ou le passer en argument.

### Les règles du JSX

1. **Un seul élément racine** par expression. Pour regrouper plusieurs éléments sans ajouter de balise inutile, utilisez un **fragment** `<>…</>`.
2. **Toutes les balises se ferment**, y compris les balises vides : `<img />`, `<br />`, `<input />`.
3. Les attributs s'écrivent en **camelCase** : `onClick`, `tabIndex`, `maxLength`.
4. Deux attributs changent de nom : `class` devient **`className`**, `for` devient **`htmlFor`**.
5. L'attribut `style` reçoit un **objet**, avec des propriétés en camelCase : `style={{ fontSize: 18 }}`.

| HTML | JSX |
|---|---|
| `<div class="carte">` | `<div className="carte">` |
| `<label for="email">` | `<label htmlFor="email">` |
| `<input type="text">` | `<input type="text" />` |
| `<p style="color: red">` | `<p style={{ color: "red" }}>` |
| `<!-- commentaire -->` | `{/* commentaire */}` |

```jsx
export default function Inscription() {
  return (
    <>
      <h2 className="titre">Inscription</h2>
      <label htmlFor="email">Email</label>
      <input id="email" type="email" maxLength={80} />
      <p style={{ color: "gray", fontSize: 14 }}>Nous ne partageons jamais votre adresse.</p>
    </>
  );
}
```

## Insérer du JavaScript avec les accolades

Entre accolades `{ }`, vous pouvez placer **n'importe quelle expression** JavaScript : une variable, un calcul, un appel de fonction, un ternaire.

```jsx
const utilisateur = { prenom: "Karim", points: 1250 };

function formaterPoints(n) {
  return n.toLocaleString("fr-FR");
}

export default function Profil() {
  const estExpert = utilisateur.points >= 1000;
  return (
    <section>
      <h2>Bonjour {utilisateur.prenom} !</h2>
      <p>Vous avez {formaterPoints(utilisateur.points)} points.</p>
      <p>Niveau : {estExpert ? "Expert" : "Débutant"}</p>
      <img src="/avatar.png" alt={`Avatar de ${utilisateur.prenom}`} />
    </section>
  );
}
```

On ne peut en revanche pas y écrire d'**instructions** (`if`, `for`, déclarations de variables) : préparez les valeurs avant le `return`, ou utilisez un ternaire.

> Les doubles accolades de `style={{ color: "red" }}` ne sont pas une syntaxe spéciale : les accolades extérieures ouvrent une expression JavaScript, les intérieures délimitent l'objet.

## JSX et sécurité

Quand vous insérez une valeur texte avec `{ }`, React **échappe** automatiquement les caractères spéciaux : un texte contenant `<script>` s'affiche tel quel, sans être exécuté. C'est une protection importante contre les injections de code (failles XSS). La seule manière d'insérer du HTML brut porte un nom volontairement inquiétant, `dangerouslySetInnerHTML` : ne l'utilisez jamais avec un contenu saisi par un utilisateur.

## Construire pour la production

```bash
npm run build
npm run preview
```

`npm run build` crée un dossier `dist/` contenant des fichiers HTML, CSS et JavaScript optimisés, prêts à être déposés chez un hébergeur de sites statiques. `npm run preview` permet de tester localement cette version.

## À retenir

- `npm create vite@latest mon-app -- --template react`, puis `npm install` et `npm run dev`.
- `src/main.jsx` monte le composant `App` dans `<div id="root">` avec `createRoot`.
- JSX : un seul élément racine (ou un fragment `<>…</>`), balises toujours fermées, `className`, `htmlFor`, attributs en camelCase.
- `{ }` insère une **expression** JavaScript ; les valeurs texte sont échappées automatiquement.
- `npm run build` produit la version de production dans `dist/`.

## Exercices

### Exercice 1 — Du HTML au JSX

Convertissez ce HTML en un composant `Contact` : `<div class="contact"><label for="nom">Nom</label><input id="nom" type="text"><br><button class="principal">Envoyer</button></div>`.

```solution-jsx
export default function Contact() {
  return (
    <div className="contact">
      <label htmlFor="nom">Nom</label>
      <input id="nom" type="text" />
      <br />
      <button className="principal">Envoyer</button>
    </div>
  );
}
```

### Exercice 2 — Trouvez les erreurs

Ce composant contient trois erreurs. Lesquelles ?

```jsx
export default function Carte() {
  return (
    <h2 class="titre">Offre</h2>
    <img src="offre.png">
  );
}
```

```solution-text
1. Deux éléments sont renvoyés côte à côte : il faut un élément racine unique, par exemple un fragment <>…</>.
2. class doit s'écrire className en JSX.
3. La balise img doit être fermée : <img src="offre.png" />. Ajoutez aussi un attribut alt pour l'accessibilité.
```

### Exercice 3 — Expressions dans le JSX

Créez un composant `Panier` qui, à partir de `const articles = 3` et `const total = 47.5`, affiche `3 articles — total : 47.50 €`, et le texte `Livraison offerte` si le total dépasse 40, `Livraison : 4.90 €` sinon.

```solution-jsx
const articles = 3;
const total = 47.5;

export default function Panier() {
  return (
    <div>
      <p>
        {articles} articles — total : {total.toFixed(2)} €
      </p>
      <p>{total > 40 ? "Livraison offerte" : "Livraison : 4.90 €"}</p>
    </div>
  );
}
```
"""

M1_L3 = r"""
## Qu'est-ce qu'un composant ?

Un **composant** est une **fonction JavaScript qui renvoie du JSX**. Il représente un morceau d'interface que l'on peut réutiliser autant de fois que nécessaire, comme une balise HTML que vous auriez inventée.

```jsx
function Entete() {
  return (
    <header>
      <h1>SMK Boutique</h1>
    </header>
  );
}

function PiedDePage() {
  return <footer>Contact : boutique@exemple.fr</footer>;
}

export default function App() {
  return (
    <>
      <Entete />
      <main>Bienvenue !</main>
      <PiedDePage />
    </>
  );
}
```

Deux règles à respecter :

- le nom d'un composant commence par une **majuscule** : `<Entete />` est un composant, `<header>` une balise HTML. React s'appuie sur cette majuscule pour les distinguer ;
- un composant se déclare au **premier niveau** du fichier, jamais à l'intérieur d'un autre composant.

Un composant peut en utiliser d'autres : c'est la **composition**. Une application React est un **arbre de composants** dont `App` est la racine.

## Transmettre des données : les props

Un composant devient vraiment utile quand on peut le **paramétrer**. Les **props** (abréviation de *properties*) sont les attributs que l'on passe à un composant ; il les reçoit sous la forme d'un **objet**, en premier paramètre.

```jsx
function CarteProduit({ nom, prix, enPromo }) {
  return (
    <article className="carte">
      <h2>{nom}</h2>
      <p>{prix.toFixed(2)} €</p>
      {enPromo && <span className="badge">Promo</span>}
    </article>
  );
}

export default function Catalogue() {
  return (
    <section>
      <CarteProduit nom="Clavier" prix={45} enPromo />
      <CarteProduit nom="Souris" prix={19.9} enPromo={false} />
    </section>
  );
}
```

Le HTML produit est le suivant :

```html
<section><article class="carte"><h2>Clavier</h2><p>45.00 €</p><span class="badge">Promo</span></article><article class="carte"><h2>Souris</h2><p>19.90 €</p></article></section>
```

Observez la façon de passer chaque type de valeur :

| Écriture | Valeur reçue |
|---|---|
| `nom="Clavier"` | la chaîne `"Clavier"` |
| `prix={45}` | le nombre `45` (accolades obligatoires) |
| `enPromo` | `true` (attribut sans valeur) |
| `enPromo={false}` | `false` |
| `options={{ taille: "M" }}` | un objet |
| `onAchat={acheter}` | une fonction (module 2) |

La déstructuration `({ nom, prix, enPromo })` est la forme la plus courante. Elle équivaut à recevoir `props` puis à lire `props.nom`, `props.prix`…

### Valeurs par défaut

```jsx
function Bouton({ texte = "Valider", variante = "principal" }) {
  return <button className={`bouton bouton-${variante}`}>{texte}</button>;
}

export default function Actions() {
  return (
    <div>
      <Bouton />
      <Bouton texte="Annuler" variante="secondaire" />
    </div>
  );
}
```

Une prop absente vaut `undefined` : la valeur par défaut de la déstructuration s'applique alors.

## Les props sont en lecture seule

Un composant ne doit **jamais modifier ses props**. Elles appartiennent au composant parent, qui peut en fournir de nouvelles à chaque affichage. Pour qu'une valeur change au fil du temps, on utilisera l'**état** (module 2).

Plus largement, un composant doit se comporter comme une **fonction pure** : pour les mêmes props, il renvoie toujours le même JSX, sans modifier de variable extérieure pendant l'affichage. Comparez ces deux fonctions :

```js
let total = 0;

function ajouterImpure(prix) {
  total += prix;            // modifie une variable extérieure
  return total;
}

function ajouterPure(totalActuel, prix) {
  return totalActuel + prix; // ne dépend que de ses paramètres
}

console.log(ajouterImpure(10), ajouterImpure(10));
console.log(ajouterPure(0, 10), ajouterPure(0, 10));
```

```text
10 20
10 10
```

La fonction impure donne un résultat différent à chaque appel avec le même argument. Or React peut appeler un composant plusieurs fois (le mode strict le fait même exprès en développement, pour révéler ce type d'erreur) : un composant impur afficherait alors des résultats incohérents.

## La prop `children`

Ce que vous placez **entre** la balise ouvrante et la balise fermante d'un composant lui est transmis dans une prop spéciale, **`children`**. C'est idéal pour les composants « conteneurs » : cadres, cartes, fenêtres modales.

```jsx
function Encadre({ titre, children }) {
  return (
    <div className="encadre">
      <h3>{titre}</h3>
      <div className="encadre-contenu">{children}</div>
    </div>
  );
}

export default function Page() {
  return (
    <Encadre titre="Conseil">
      <p>Enregistrez souvent votre travail.</p>
      <p>Relisez les messages d'erreur en entier.</p>
    </Encadre>
  );
}
```

## Organiser les fichiers

Dans un vrai projet, on place en général **un composant par fichier**, dans un dossier `src/components/` :

```jsx
// src/components/CarteProduit.jsx
export default function CarteProduit({ nom, prix }) {
  return (
    <article className="carte">
      <h2>{nom}</h2>
      <p>{prix.toFixed(2)} €</p>
    </article>
  );
}
```

```jsx
// src/App.jsx
import CarteProduit from "./components/CarteProduit.jsx";

export default function App() {
  return <CarteProduit nom="Casque" prix={59} />;
}
```

> Pour les styles, Vite permet d'importer un fichier CSS directement depuis un composant : `import "./CarteProduit.css";`. Les classes restent globales : choisissez des noms précis (`carte-produit`) pour éviter les collisions.

## À retenir

- Un composant est une fonction dont le nom commence par une **majuscule** et qui renvoie du JSX.
- Les **props** sont reçues sous forme d'objet, généralement déstructuré ; chaînes entre guillemets, autres valeurs entre accolades.
- On prévoit des **valeurs par défaut** dans la déstructuration.
- Les props sont en **lecture seule** ; un composant doit rester **pur**.
- `children` contient ce qui est placé entre les balises du composant.

## Exercices

### Exercice 1 — Un badge paramétrable

Écrivez un composant `Badge` qui reçoit `texte` et `couleur` (par défaut `"bleu"`) et affiche `<span className="badge badge-bleu">…</span>`. Utilisez-le deux fois dans un composant `App`, dont une fois avec la couleur `"vert"`.

```solution-jsx
function Badge({ texte, couleur = "bleu" }) {
  return <span className={`badge badge-${couleur}`}>{texte}</span>;
}

export default function App() {
  return (
    <p>
      <Badge texte="Nouveau" />
      <Badge texte="Validé" couleur="vert" />
    </p>
  );
}
```

### Exercice 2 — Une carte avec `children`

Écrivez un composant `Carte` qui affiche un titre (prop `titre`) dans un `<h2>`, puis son contenu (`children`). Utilisez-le pour afficher une carte « Horaires » contenant deux paragraphes.

```solution-jsx
function Carte({ titre, children }) {
  return (
    <section className="carte">
      <h2>{titre}</h2>
      {children}
    </section>
  );
}

export default function App() {
  return (
    <Carte titre="Horaires">
      <p>Du lundi au vendredi : 9 h – 18 h</p>
      <p>Le samedi : 10 h – 13 h</p>
    </Carte>
  );
}
```

### Exercice 3 — Trouvez le problème

Que reprochez-vous à ce composant ?

```jsx
function Salutation(props) {
  props.prenom = props.prenom.toUpperCase();
  return <p>Bonjour {props.prenom}</p>;
}
```

```solution-text
Il modifie une prop : les props sont en lecture seule et appartiennent au composant parent.
Il faut calculer une nouvelle valeur sans toucher à props :

function Salutation({ prenom }) {
  return <p>Bonjour {prenom.toUpperCase()}</p>;
}
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Interactivité : événements et état
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Attacher un gestionnaire d'événement

En React, on n'utilise pas `addEventListener` : on passe une **fonction** à un attribut d'événement directement dans le JSX. Ces attributs s'écrivent en camelCase : `onClick`, `onChange`, `onSubmit`, `onMouseEnter`, `onKeyDown`…

```jsx
export default function BoutonBonjour() {
  function gererClic() {
    alert("Bonjour !");
  }

  return <button onClick={gererClic}>Dire bonjour</button>;
}
```

La fonction `gererClic` est appelée **à chaque clic**. On la déclare en général dans le composant, ce qui lui donne accès aux props et aux variables de celui-ci.

> Par convention, on nomme les gestionnaires `gererX` (ou `handleX` dans les projets en anglais) et les props qui reçoivent un gestionnaire `onX`.

## Le piège des parenthèses

```jsx
<button onClick={gererClic}>OK</button>     {/* correct : on passe la fonction */}
<button onClick={gererClic()}>OK</button>   {/* erreur : on l'appelle pendant l'affichage */}
```

Avec des parenthèses, `gererClic()` est **exécutée immédiatement**, à chaque affichage du composant, et c'est son résultat (souvent `undefined`) qui est passé à `onClick`. Il faut transmettre la fonction **elle-même**.

Pour passer un **argument**, enveloppez l'appel dans une fonction fléchée :

```jsx
function Notation() {
  function noter(etoiles) {
    alert(`Vous avez donné ${etoiles} étoile(s)`);
  }

  return (
    <div>
      <button onClick={() => noter(1)}>1</button>
      <button onClick={() => noter(2)}>2</button>
      <button onClick={() => noter(3)}>3</button>
    </div>
  );
}

export default Notation;
```

`() => noter(2)` est une nouvelle fonction qui, **lorsqu'on cliquera**, appellera `noter(2)`.

## L'objet événement

Le gestionnaire reçoit un **objet événement** en paramètre. Ses propriétés les plus utiles :

| Propriété ou méthode | Usage |
|---|---|
| `e.target` | l'élément concerné (champ, bouton…) |
| `e.target.value` | la valeur d'un champ de saisie |
| `e.key` | la touche pressée (`"Enter"`, `"Escape"`…) |
| `e.preventDefault()` | empêche le comportement par défaut (envoi d'un formulaire, suivi d'un lien) |
| `e.stopPropagation()` | empêche l'événement de remonter vers les éléments parents |

```jsx
export default function Recherche() {
  function gererTouche(e) {
    if (e.key === "Enter") {
      console.log("Recherche :", e.target.value);
    }
  }

  function gererEnvoi(e) {
    e.preventDefault(); // pas de rechargement de la page
    console.log("Formulaire envoyé");
  }

  return (
    <form onSubmit={gererEnvoi}>
      <input onKeyDown={gererTouche} placeholder="Rechercher…" />
      <button type="submit">OK</button>
    </form>
  );
}
```

> Dans un formulaire, `onSubmit` se place sur la balise `<form>` et non sur le bouton : il se déclenche aussi bien au clic sur le bouton qu'en appuyant sur Entrée.

## Transmettre un gestionnaire par les props

Un composant réutilisable ne sait pas toujours ce qu'il doit faire quand on clique : c'est son **parent** qui le décide. Le parent passe alors une fonction en prop.

```jsx
function BoutonAction({ texte, onAction }) {
  return (
    <button className="bouton" onClick={onAction}>
      {texte}
    </button>
  );
}

export default function BarreOutils() {
  return (
    <div>
      <BoutonAction texte="Imprimer" onAction={() => window.print()} />
      <BoutonAction texte="Aide" onAction={() => alert("Consultez la FAQ.")} />
    </div>
  );
}
```

C'est le principe du **flux de données à sens unique** de React : les données **descendent** du parent vers l'enfant par les props ; les actions **remontent** de l'enfant vers le parent par des fonctions passées en props.

## Propagation des événements

Un événement se produit d'abord sur l'élément cliqué, puis **remonte** vers ses parents (on parle de propagation, ou *bubbling*). Si un bouton est placé dans une carte cliquable, un clic sur le bouton déclenche les deux gestionnaires, sauf si le bouton appelle `e.stopPropagation()`.

```jsx
export default function CarteCliquable() {
  return (
    <div className="carte" onClick={() => console.log("Ouvrir la carte")}>
      <h3>Article</h3>
      <button
        onClick={(e) => {
          e.stopPropagation();
          console.log("Ajouter aux favoris");
        }}
      >
        ☆
      </button>
    </div>
  );
}
```

## Pourquoi une simple variable ne suffit pas

Essayons d'écrire un compteur avec une variable ordinaire :

```jsx
export default function CompteurCasse() {
  let compteur = 0;

  function incrementer() {
    compteur = compteur + 1;
    console.log(compteur); // la valeur augmente dans la console…
  }

  return <button onClick={incrementer}>Cliqué {compteur} fois</button>; // …mais l'écran affiche toujours 0
}
```

Deux problèmes :

1. modifier une variable locale **ne demande pas** à React d'afficher à nouveau le composant ;
2. même si React l'affichait à nouveau, la fonction serait réexécutée et `compteur` repartirait de `0`.

Il faut une valeur que React **conserve** entre deux affichages et dont la modification **déclenche** un nouvel affichage : c'est l'**état**, objet de la leçon suivante.

## À retenir

- On attache un événement avec `onClick={fonction}`, sans parenthèses d'appel.
- Pour passer un argument : `onClick={() => faire(id)}`.
- Le gestionnaire reçoit l'objet événement : `e.target.value`, `e.key`, `e.preventDefault()`.
- Un parent transmet ses gestionnaires aux enfants par des props nommées `onX`.
- Modifier une variable locale ne met pas l'écran à jour : il faut l'état.

## Exercices

### Exercice 1 — Bouton de salutation

Écrivez un composant `BoutonSalut` qui reçoit une prop `prenom` et affiche une alerte `Bonjour <prenom> !` au clic.

```solution-jsx
export default function BoutonSalut({ prenom }) {
  return <button onClick={() => alert(`Bonjour ${prenom} !`)}>Saluer {prenom}</button>;
}
```

### Exercice 2 — Un lecteur et ses commandes

Écrivez un composant `Commandes` qui reçoit deux props `onLecture` et `onPause` et affiche deux boutons « Lecture » et « Pause ». Écrivez ensuite un composant `Lecteur` qui l'utilise et affiche dans la console `Lecture` ou `Pause`.

```solution-jsx
function Commandes({ onLecture, onPause }) {
  return (
    <div>
      <button onClick={onLecture}>Lecture</button>
      <button onClick={onPause}>Pause</button>
    </div>
  );
}

export default function Lecteur() {
  return <Commandes onLecture={() => console.log("Lecture")} onPause={() => console.log("Pause")} />;
}
```

### Exercice 3 — Expliquez le bug

Ce composant supprime l'article dès l'affichage de la liste, sans qu'on ait cliqué. Pourquoi ? Corrigez la ligne.

```jsx
<button onClick={supprimer(article.id)}>Supprimer</button>
```

```solution-text
supprimer(article.id) est un appel de fonction : il s'exécute pendant l'affichage, et c'est son
résultat qui est passé à onClick. Il faut transmettre une fonction qui fera l'appel plus tard :

<button onClick={() => supprimer(article.id)}>Supprimer</button>
```
"""

M2_L2 = r"""
## Le hook `useState`

L'**état** (*state*) est la mémoire d'un composant : une valeur que React conserve entre deux affichages et dont la modification provoque un nouvel affichage. On le crée avec la fonction **`useState`**, importée depuis `react` :

```jsx
import { useState } from "react";

export default function Compteur() {
  const [compteur, setCompteur] = useState(0);

  return (
    <button onClick={() => setCompteur(compteur + 1)}>
      Cliqué {compteur} fois
    </button>
  );
}
```

`useState(0)` renvoie un **tableau de deux éléments**, que l'on déstructure :

- `compteur` : la **valeur actuelle** de l'état (`0` au premier affichage) ;
- `setCompteur` : la **fonction de mise à jour**. L'appeler enregistre la nouvelle valeur **et** demande à React d'afficher à nouveau le composant.

Les noms sont libres ; la convention est `[quelqueChose, setQuelqueChose]`.

## Le cycle d'affichage

Quand l'utilisateur clique :

1. `setCompteur(1)` est appelé : React note la nouvelle valeur ;
2. React **rappelle** la fonction `Compteur` ; cette fois, `useState` renvoie `1` ;
3. le composant renvoie un nouveau JSX (`Cliqué 1 fois`) ;
4. React compare avec le JSX précédent et ne modifie dans la page que le texte du bouton.

Ce mécanisme s'appelle un nouveau **rendu** (*re-render*). Le mot « rendu » désigne l'appel de votre composant par React, pas une modification systématique de la page.

## Chaque composant a son propre état

```jsx
import { useState } from "react";

function Compteur({ libelle }) {
  const [valeur, setValeur] = useState(0);
  return (
    <p>
      {libelle} : {valeur}{" "}
      <button onClick={() => setValeur(valeur + 1)}>+1</button>
    </p>
  );
}

export default function Tableau() {
  return (
    <>
      <Compteur libelle="Visiteurs" />
      <Compteur libelle="Inscriptions" />
    </>
  );
}
```

Les deux compteurs sont **indépendants** : chaque instance d'un composant possède son propre état. `{" "}` insère un espace explicite entre le texte et le bouton.

## Plusieurs variables d'état

Un composant peut appeler `useState` plusieurs fois, une par information indépendante :

```jsx
import { useState } from "react";

export default function Reglages() {
  const [volume, setVolume] = useState(50);
  const [muet, setMuet] = useState(false);

  return (
    <div>
      <p>Volume : {muet ? "coupé" : volume}</p>
      <button onClick={() => setVolume(Math.max(0, volume - 10))}>-</button>
      <button onClick={() => setVolume(Math.min(100, volume + 10))}>+</button>
      <button onClick={() => setMuet(!muet)}>{muet ? "Rétablir" : "Couper"}</button>
    </div>
  );
}
```

`setMuet(!muet)` inverse un booléen : c'est le schéma classique d'une **bascule** (*toggle*).

## L'état est une photographie

Dans un rendu donné, la variable d'état est une **constante** : appeler `setCompteur` ne la modifie pas immédiatement, cela **programme** un nouveau rendu avec une nouvelle valeur. Conséquence surprenante :

```jsx
function gererClic() {
  setCompteur(compteur + 1);
  setCompteur(compteur + 1);
  setCompteur(compteur + 1);
  console.log(compteur); // affiche encore l'ancienne valeur
}
```

Si `compteur` vaut 0, les trois appels demandent tous « mets 1 » : après le clic, le compteur vaut **1**, pas 3.

Lorsque la nouvelle valeur dépend de la précédente, passez une **fonction de mise à jour** : React l'appellera avec la valeur la plus récente.

```jsx
function gererClic() {
  setCompteur((c) => c + 1);
  setCompteur((c) => c + 1);
  setCompteur((c) => c + 1); // le compteur augmente bien de 3
}
```

React place les mises à jour dans une **file d'attente** qu'il traite au rendu suivant. Cette petite simulation reproduit son raisonnement :

```js
function traiterFile(etatInitial, file) {
  return file.reduce(
    (etat, miseAJour) => (typeof miseAJour === "function" ? miseAJour(etat) : miseAJour),
    etatInitial
  );
}

const compteur = 0;
console.log(traiterFile(compteur, [compteur + 1, compteur + 1, compteur + 1]));
console.log(traiterFile(compteur, [(c) => c + 1, (c) => c + 1, (c) => c + 1]));
console.log(traiterFile(compteur, [compteur + 5, (c) => c + 1]));
```

```text
1
3
6
```

- une **valeur** remplace l'état, quelle que soit la valeur précédente ;
- une **fonction** reçoit l'état le plus récent et calcule le suivant.

> Règle pratique : dès que la nouvelle valeur se calcule à partir de l'ancienne, utilisez la forme `setX((ancien) => …)`.

## Les règles des hooks

Les fonctions dont le nom commence par `use` (`useState`, `useEffect`…) s'appellent des **hooks**. React les identifie par leur **ordre d'appel** à chaque rendu ; d'où deux règles impératives :

1. appelez les hooks **au premier niveau** du composant : jamais dans une condition, une boucle, une fonction imbriquée ou après un `return` anticipé ;
2. appelez-les **uniquement** dans un composant ou dans un hook personnalisé (module 5), jamais dans une fonction JavaScript ordinaire.

```jsx
import { useState } from "react";

export default function Formulaire({ avance }) {
  // Interdit : if (avance) { const [niveau, setNiveau] = useState(1); }
  const [niveau, setNiveau] = useState(1); // toujours appelé, dans le même ordre
  if (!avance) {
    return <p>Mode simple</p>;
  }
  return <button onClick={() => setNiveau(niveau + 1)}>Niveau {niveau}</button>;
}
```

Le plugin ESLint `eslint-plugin-react-hooks`, souvent inclus dans les modèles de projet, signale automatiquement ces erreurs.

## Valeur initiale coûteuse

La valeur passée à `useState` n'est utilisée qu'au **premier** rendu. Si son calcul est coûteux (lecture du stockage local, gros calcul), passez une **fonction** : React ne l'appellera qu'une fois.

```jsx
const [notes, setNotes] = useState(() => JSON.parse(localStorage.getItem("notes") ?? "[]"));
```

## À retenir

- `const [valeur, setValeur] = useState(initiale)` crée un état ; `setValeur` déclenche un nouveau rendu.
- Chaque instance d'un composant a son propre état.
- Dans un rendu, l'état est une photographie : `setX` ne le modifie pas immédiatement.
- Si la nouvelle valeur dépend de l'ancienne : `setX((ancien) => nouveau)`.
- Hooks au premier niveau, jamais dans une condition ni une boucle.

## Exercices

### Exercice 1 — Bouton « J'aime »

Écrivez un composant `BoutonJaime` qui affiche `♡ J'aime` puis, après un clic, `♥ Vous aimez`. Un nouveau clic revient à l'état initial.

```solution-jsx
import { useState } from "react";

export default function BoutonJaime() {
  const [aime, setAime] = useState(false);
  return (
    <button onClick={() => setAime((a) => !a)} aria-pressed={aime}>
      {aime ? "♥ Vous aimez" : "♡ J'aime"}
    </button>
  );
}
```

### Exercice 2 — Compteur borné

Écrivez un composant `Quantite` avec les boutons `-`, `+` et `Réinitialiser`. La quantité démarre à 1 et ne descend jamais sous 1 ni ne dépasse 10.

```solution-jsx
import { useState } from "react";

export default function Quantite() {
  const [quantite, setQuantite] = useState(1);
  return (
    <div>
      <button onClick={() => setQuantite((q) => Math.max(1, q - 1))}>-</button>
      <span> {quantite} </span>
      <button onClick={() => setQuantite((q) => Math.min(10, q + 1))}>+</button>
      <button onClick={() => setQuantite(1)}>Réinitialiser</button>
    </div>
  );
}
```

### Exercice 3 — Prédisez

`n` vaut 0. Que vaut-il après l'exécution de ce gestionnaire ? Vérifiez avec la fonction `traiterFile` de la leçon.

```jsx
function gererClic() {
  setN((x) => x + 2);
  setN(n + 10);
  setN((x) => x * 2);
}
```

```solution-js
function traiterFile(etatInitial, file) {
  return file.reduce(
    (etat, miseAJour) => (typeof miseAJour === "function" ? miseAJour(etat) : miseAJour),
    etatInitial
  );
}

const n = 0;
console.log(traiterFile(n, [(x) => x + 2, n + 10, (x) => x * 2]));
```

```text
20
```
"""

M2_L3 = r"""
## L'état doit être remplacé, jamais modifié

Pour décider s'il doit afficher à nouveau un composant, React compare l'ancienne et la nouvelle valeur de l'état avec `Object.is`, qui se comporte comme `===` pour les objets : il vérifie qu'il s'agit **du même objet en mémoire**, pas que le contenu est identique.

```js
const avant = { prenom: "Emma", age: 24 };

const modifie = avant;
modifie.age = 25;                     // mutation de l'objet existant
console.log(Object.is(modifie, avant));

const copie = { ...avant, age: 26 };  // nouvel objet
console.log(Object.is(copie, avant));
console.log(avant.age, copie.age);
```

```text
true
false
25 26
```

Si vous **modifiez** (on dit aussi **muter**) un objet ou un tableau de l'état puis passez ce même objet à `setX`, React voit la même référence et peut ignorer la mise à jour : l'écran ne change pas. La règle est donc simple : **traitez l'état comme s'il était en lecture seule** et créez toujours une **nouvelle** valeur.

## Mettre à jour un objet

```jsx
import { useState } from "react";

export default function Profil() {
  const [profil, setProfil] = useState({ prenom: "Emma", ville: "Nantes", newsletter: false });

  function demenager() {
    setProfil({ ...profil, ville: "Bordeaux" }); // copie + propriété remplacée
  }

  function basculerNewsletter() {
    setProfil((p) => ({ ...p, newsletter: !p.newsletter }));
  }

  return (
    <div>
      <p>
        {profil.prenom} habite à {profil.ville}. Newsletter : {profil.newsletter ? "oui" : "non"}
      </p>
      <button onClick={demenager}>Déménager</button>
      <button onClick={basculerNewsletter}>Newsletter</button>
    </div>
  );
}
```

> Attention aux parenthèses dans `(p) => ({ ...p })` : sans elles, les accolades seraient comprises comme le corps de la fonction et non comme un objet.

Pour un objet **imbriqué**, il faut copier chaque niveau modifié :

```js
const client = { nom: "Diallo", adresse: { ville: "Lille", codePostal: "59000" } };

const demenage = {
  ...client,
  adresse: { ...client.adresse, ville: "Roubaix", codePostal: "59100" },
};

console.log(client.adresse.ville);
console.log(demenage.adresse.ville, demenage.nom);
```

```text
Lille
Roubaix Diallo
```

## Mettre à jour un tableau

Certaines méthodes des tableaux **modifient** le tableau d'origine ; d'autres **renvoient un nouveau tableau**. Avec l'état, n'utilisez que les secondes.

| Opération | À éviter (mutation) | À utiliser (nouveau tableau) |
|---|---|---|
| ajouter | `push`, `unshift` | `[...t, element]`, `[element, ...t]` |
| supprimer | `splice`, `pop` | `t.filter(...)` |
| modifier | `t[i] = x` | `t.map(...)` |
| trier | `sort`, `reverse` | `[...t].sort(...)` |

Ces opérations s'écrivent comme de petites fonctions pures, faciles à tester :

```js
const ajouter = (taches, titre, id) => [...taches, { id, titre, faite: false }];
const supprimer = (taches, id) => taches.filter((t) => t.id !== id);
const basculer = (taches, id) =>
  taches.map((t) => (t.id === id ? { ...t, faite: !t.faite } : t));

let taches = [{ id: 1, titre: "Lire", faite: false }];
taches = ajouter(taches, "Coder", 2);
taches = ajouter(taches, "Tester", 3);
taches = basculer(taches, 2);
taches = supprimer(taches, 1);
console.log(taches);

const nombres = [3, 1, 2];
const tries = [...nombres].sort((a, b) => a - b);
console.log(nombres, tries);
```

```text
[
  { id: 2, titre: 'Coder', faite: true },
  { id: 3, titre: 'Tester', faite: false }
]
[ 3, 1, 2 ] [ 1, 2, 3 ]
```

`[...nombres]` crée une copie avant le tri : `nombres` reste intact.

## Une liste de courses

Assemblons tout cela dans un composant. (Les attributs `key` et l'affichage des listes sont détaillés au module 3.)

```jsx
import { useState } from "react";

const articlesInitiaux = [
  { id: 1, nom: "Pain", achete: false },
  { id: 2, nom: "Lait", achete: true },
];

export default function ListeCourses() {
  const [articles, setArticles] = useState(articlesInitiaux);
  const [prochainId, setProchainId] = useState(3);

  function ajouter() {
    setArticles([...articles, { id: prochainId, nom: `Article ${prochainId}`, achete: false }]);
    setProchainId(prochainId + 1);
  }

  function basculer(id) {
    setArticles(articles.map((a) => (a.id === id ? { ...a, achete: !a.achete } : a)));
  }

  function supprimer(id) {
    setArticles(articles.filter((a) => a.id !== id));
  }

  return (
    <div>
      <ul>
        {articles.map((a) => (
          <li key={a.id}>
            <label>
              <input type="checkbox" checked={a.achete} onChange={() => basculer(a.id)} />
              {a.nom}
            </label>
            <button onClick={() => supprimer(a.id)}>Retirer</button>
          </li>
        ))}
      </ul>
      <button onClick={ajouter}>Ajouter un article</button>
    </div>
  );
}
```

## Choisir la forme de son état

Quelques principes pour garder un état simple :

- **regroupez** les valeurs qui changent toujours ensemble (une position `{ x, y }` plutôt que deux états) ;
- **évitez les doublons** : ne stockez pas à la fois une liste et « l'élément sélectionné » complet ; stockez plutôt l'**identifiant** sélectionné ;
- **ne stockez pas ce qui se calcule** : le nombre d'articles achetés se déduit de la liste à chaque rendu (`articles.filter((a) => a.achete).length`). Le module 3 revient sur ces **données dérivées**.

## À retenir

- React compare les états par **référence** : une mutation peut passer inaperçue.
- Objet : `{ ...ancien, propriete: nouvelleValeur }` ; copier chaque niveau imbriqué modifié.
- Tableau : `[...t, x]` pour ajouter, `filter` pour supprimer, `map` pour modifier, `[...t].sort()` pour trier.
- Écrire les transformations comme des fonctions pures les rend faciles à tester.
- Un état minimal : pas de doublon, pas de valeur calculable.

## Exercices

### Exercice 1 — Renommer un élément

Écrivez une fonction pure `renommer(taches, id, titre)` qui renvoie un nouveau tableau où la tâche d'identifiant `id` porte le nouveau titre. Testez-la et vérifiez que le tableau d'origine n'a pas changé.

```solution-js
const renommer = (taches, id, titre) => taches.map((t) => (t.id === id ? { ...t, titre } : t));

const taches = [
  { id: 1, titre: "Lire" },
  { id: 2, titre: "Coder" },
];
const resultat = renommer(taches, 2, "Coder en React");
console.log(resultat[1].titre);
console.log(taches[1].titre);
```

```text
Coder en React
Coder
```

### Exercice 2 — Objet imbriqué

Avec `const reglages = { theme: "clair", notifications: { email: true, sms: false } }`, créez un nouvel objet où `sms` vaut `true`, sans modifier l'original. Affichez les deux valeurs de `sms`.

```solution-js
const reglages = { theme: "clair", notifications: { email: true, sms: false } };
const nouveaux = {
  ...reglages,
  notifications: { ...reglages.notifications, sms: true },
};
console.log(reglages.notifications.sms, nouveaux.notifications.sms);
```

```text
false true
```

### Exercice 3 — Tout cocher

Ajoutez au composant `ListeCourses` une fonction `toutCocher` qui marque tous les articles comme achetés, et un bouton pour l'appeler.

```solution-jsx
function toutCocher() {
  setArticles((liste) => liste.map((a) => ({ ...a, achete: true })));
}

// dans le JSX, sous la liste :
<button onClick={toutCocher}>Tout cocher</button>
```
"""

QUIZ_M1 = [
    ("single", "Que signifie l'approche « déclarative » de React ?", None,
     ["On modifie la page élément par élément avec querySelector", "On déclare toutes les variables avec const", "On écrit directement du HTML dans index.html", "On décrit l'interface attendue pour des données, et React met la page à jour"], [3],
     "Avec React, on décrit à quoi doit ressembler l'écran pour un état donné ; React calcule et applique les changements nécessaires dans la page."),
    ("single", "Quelle commande crée un nouveau projet React avec Vite ?", None,
     ["npm create vite@latest mon-app -- --template react", "npm install react", "npx react new mon-app", "node vite mon-app"], [0],
     "npm create vite@latest lance l'outil de création de Vite ; l'option --template react choisit le modèle React."),
    ("single", "Quel attribut JSX remplace l'attribut HTML class ?", None,
     ["class", "cssClass", "className", "styleName"], [2],
     "class est un mot réservé de JavaScript : en JSX, on écrit className (et htmlFor au lieu de for)."),
    ("single", "Pourquoi ce code JSX est-il invalide ?", "return (\n  <h1>Titre</h1>\n  <p>Texte</p>\n);",
     ["Il manque un élément racine unique (ou un fragment)", "<p> n'est pas autorisé en JSX", "Il faut écrire <H1>", "Le return doit être sur une seule ligne"], [0],
     "Une expression JSX doit avoir un seul élément racine ; on regroupe les deux éléments dans un fragment <>…</> ou une balise."),
    ("single", "Comment passer le nombre 42 dans une prop quantite ?", None,
     ["quantite=\"42\"", "quantite:{42}", "quantite=42", "quantite={42}"], [3],
     "Les accolades insèrent une expression JavaScript : {42} transmet un nombre, alors que \"42\" transmettrait une chaîne."),
    ("single", "Pourquoi le nom d'un composant doit-il commencer par une majuscule ?", None,
     ["C'est une simple convention sans effet", "React traite les noms en minuscules comme des balises HTML", "Les minuscules sont interdites en JSX", "Pour que Vite trouve le fichier"], [1],
     "En JSX, <carte /> serait interprété comme une balise HTML inconnue ; <Carte /> désigne le composant."),
    ("single", "Que contient la prop children de <Encadre><p>Texte</p></Encadre> ?", None,
     ["undefined", "La chaîne \"Encadre\"", "L'élément <p>Texte</p> placé entre les balises", "Les autres props du composant"], [2],
     "children reçoit ce qui est placé entre la balise ouvrante et la balise fermante du composant."),
    ("multiple", "Quelles affirmations sur les props sont exactes ?", None,
     ["Un composant reçoit ses props sous la forme d'un objet.", "Un composant peut modifier ses props pour changer l'affichage.", "On peut prévoir une valeur par défaut dans la déstructuration.", "Une fonction peut être passée en prop."], [0, 2, 3],
     "Les props sont en lecture seule : pour qu'une valeur change, on utilise l'état. Les trois autres affirmations sont exactes."),
    ("true_false", "Insérer {saisie} dans du JSX peut exécuter un script contenu dans la saisie.", None,
     ["Vrai", "Faux"], [1],
     "React échappe automatiquement les valeurs texte insérées avec { } : le contenu s'affiche tel quel. Seul dangerouslySetInnerHTML insère du HTML brut."),
    ("single", "Que vaut fruits après ce code ?", "const fruits = [\"pomme\"];\nconst autres = [...fruits, \"kiwi\"];",
     ["[\"pomme\", \"kiwi\"]", "[\"kiwi\"]", "[\"pomme\"]", "Une erreur"], [2],
     "Le spread crée un nouveau tableau autres ; fruits n'est pas modifié et contient toujours [\"pomme\"]."),
]

QUIZ_M2 = [
    ("single", "Quelle écriture déclenche alerte() seulement au clic ?", None,
     ["onClick={alerte()}", "onClick={alerte}", "onclick=\"alerte()\"", "onClick=alerte"], [1],
     "On passe la fonction elle-même ; avec des parenthèses, elle serait exécutée pendant l'affichage."),
    ("single", "Comment appeler supprimer(id) au clic sur un bouton ?", None,
     ["onClick={supprimer(id)}", "onClick=\"supprimer(id)\"", "onClick={supprimer, id}", "onClick={() => supprimer(id)}"], [3],
     "La fonction fléchée crée une fonction qui appellera supprimer(id) au moment du clic."),
    ("single", "Que renvoie useState(0) ?", None,
     ["Un tableau [valeur, fonction de mise à jour]", "Le nombre 0", "Un objet { state, setState }", "Une promesse"], [0],
     "useState renvoie un tableau de deux éléments que l'on déstructure : la valeur actuelle et la fonction qui la modifie."),
    ("single", "Pourquoi l'écran ne change-t-il pas quand on modifie une variable locale avec let ?", None,
     ["Parce que let est interdit dans un composant", "Parce qu'il faut recharger la page", "Parce que modifier une variable locale ne déclenche pas de nouveau rendu, et qu'elle est réinitialisée à chaque rendu", "Parce que React ne lit que les constantes"], [2],
     "Seul l'appel à la fonction de mise à jour de l'état demande un nouveau rendu ; une variable locale repart de sa valeur initiale à chaque appel du composant."),
    ("single", "compteur vaut 0. Que vaut-il après ce gestionnaire ?", "setCompteur(compteur + 1);\nsetCompteur(compteur + 1);",
     ["0", "Une erreur", "2", "1"], [3],
     "Dans ce rendu, compteur vaut 0 : les deux appels demandent la valeur 1. Avec setCompteur((c) => c + 1), on obtiendrait 2."),
    ("single", "compteur vaut 0. Que vaut-il après ce gestionnaire ?", "setCompteur((c) => c + 1);\nsetCompteur((c) => c + 1);",
     ["2", "1", "0", "Une erreur"], [0],
     "Chaque fonction de mise à jour reçoit la valeur la plus récente de la file : 0 → 1 → 2."),
    ("multiple", "Quelles utilisations de useState respectent les règles des hooks ?", None,
     ["L'appeler au premier niveau du composant", "L'appeler dans un if", "L'appeler dans une boucle for", "L'appeler dans un hook personnalisé dont le nom commence par use"], [0, 3],
     "Les hooks s'appellent au premier niveau d'un composant ou d'un hook personnalisé, toujours dans le même ordre : jamais dans une condition ni une boucle."),
    ("single", "Quelle mise à jour de l'état items ajoute correctement un élément ?", None,
     ["items.push(x); setItems(items);", "setItems(items.push(x));", "setItems([...items, x]);", "items[items.length] = x;"], [2],
     "[...items, x] crée un nouveau tableau ; push modifie le tableau existant (et renvoie sa longueur), ce que React peut ne pas détecter."),
    ("single", "Comment passer la propriété ville de l'objet d'état profil à \"Lyon\" ?", None,
     ["profil.ville = \"Lyon\";", "setProfil({ ville: \"Lyon\" });", "setProfil({ ...profil, ville: \"Lyon\" });", "setProfil(profil, \"Lyon\");"], [2],
     "On copie l'objet avec le spread puis on remplace ville. setProfil({ ville: \"Lyon\" }) ferait perdre toutes les autres propriétés."),
    ("true_false", "React compare l'ancien et le nouvel état par référence : muter un objet puis le repasser à setX peut ne pas mettre l'écran à jour.", None,
     ["Vrai", "Faux"], [0],
     "Object.is compare les références : le même objet modifié est vu comme inchangé. Il faut toujours créer un nouvel objet ou tableau."),
]

MODULES = [
    {
        "position": 1,
        "title": "Premiers pas avec React",
        "description": "Comprendre l'approche de React, créer un projet avec Vite, écrire du JSX et des composants avec props.",
        "status": "published",
        "lessons": [
            ("decouvrir-react", "Découvrir React",
             "L'approche déclarative et les rappels JavaScript indispensables.", M1_L1, 40),
            ("vite-et-jsx", "Créer un projet avec Vite et écrire du JSX",
             "Installer, structurer un projet, règles du JSX et expressions.", M1_L2, 45),
            ("composants-props", "Composants et props",
             "Découper l'interface, transmettre des données, children.", M1_L3, 45),
        ],
        "quiz": ("Quiz — Premiers pas avec React", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Interactivité : événements et état",
        "description": "Réagir aux actions de l'utilisateur et mémoriser des valeurs avec useState.",
        "status": "published",
        "lessons": [
            ("evenements", "Réagir aux événements",
             "onClick, objet événement, gestionnaires passés en props.", M2_L1, 40),
            ("usestate", "L'état avec useState",
             "Créer un état, cycle de rendu, fonction de mise à jour, règles des hooks.", M2_L2, 45),
            ("etat-objets-tableaux", "Mettre à jour objets et tableaux",
             "Immutabilité, spread, map, filter et forme de l'état.", M2_L3, 45),
        ],
        "quiz": ("Quiz — Événements et état", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Listes, formulaires et composition",
        "description": "Afficher des listes avec des clés, gérer des formulaires contrôlés et partager l'état entre composants.",
        "status": "published",
        "lessons": [
            ("conditions-et-listes", "Affichage conditionnel et listes",
             "Ternaire, &&, map et clés stables.", _m35.M3_L1, 45),
            ("formulaires-controles", "Formulaires contrôlés",
             "Champs liés à l'état, cases à cocher, listes, validation.", _m35.M3_L2, 45),
            ("partager-etat", "Partager l'état entre composants",
             "Remonter l'état, données dérivées, penser en composants.", _m35.M3_L3, 45),
        ],
        "quiz": ("Quiz — Listes, formulaires et composition", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Effets, réducteurs et contexte",
        "description": "Se synchroniser avec l'extérieur, organiser un état complexe et partager des données dans l'arbre.",
        "status": "published",
        "lessons": [
            ("useeffect", "Les effets avec useEffect",
             "Dépendances, nettoyage et cas où un effet est inutile.", _m35.M4_L1, 45),
            ("usereducer-useref", "useReducer et useRef",
             "Centraliser les mises à jour, mémoriser sans rendu, accéder au DOM.", _m35.M4_L2, 45),
            ("contexte", "Le contexte",
             "createContext, Provider et useContext contre le passage de props en cascade.", _m35.M4_L3, 40),
        ],
        "quiz": ("Quiz — Effets, réducteurs et contexte", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Données distantes et hooks personnalisés",
        "description": "Charger des données avec fetch, factoriser la logique dans des hooks, puis mini-projet.",
        "status": "published",
        "lessons": [
            ("appels-reseau", "Appels réseau avec fetch",
             "Chargement, erreurs, annulation et requêtes déclenchées par l'utilisateur.", _m35.M5_L1, 45),
            ("hooks-personnalises", "Les hooks personnalisés",
             "useBascule, useLocalStorage, useFetch, useDebounce.", _m35.M5_L2, 45),
            ("mini-projet", "Mini-projet : annuaire filtrable",
             "Une application complète : fetch, filtres, tri et favoris.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Données distantes et hooks personnalisés", _m35.QUIZ_M5),
    },
]
