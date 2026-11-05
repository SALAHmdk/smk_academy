"""Modules 3 à 5 de « React » (importé par content/react.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Listes, formulaires et composition
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Afficher sous condition

Un composant est une fonction JavaScript : pour afficher un contenu différent selon une condition, on dispose de tous les outils du langage. Trois formes reviennent constamment.

### `if` et `return` anticipé

Quand le rendu change **entièrement** selon la situation, un `if` avant le `return` principal est le plus lisible :

```jsx
export default function Accueil({ utilisateur }) {
  if (!utilisateur) {
    return <p>Veuillez vous connecter.</p>;
  }
  return <h1>Bonjour {utilisateur.prenom} !</h1>;
}
```

### Le ternaire `condition ? a : b`

Pour choisir entre **deux** variantes à l'intérieur du JSX :

```jsx
export default function Statut({ enLigne }) {
  return (
    <p className={enLigne ? "statut statut-ok" : "statut"}>
      {enLigne ? "En ligne" : "Hors ligne"}
    </p>
  );
}
```

### L'opérateur `&&`

Pour afficher un élément **ou rien** : `condition && <Element />`. Si la condition est fausse, l'expression vaut `false`, et React n'affiche rien pour `false`, `null`, `undefined` ni `true`.

```jsx
export default function Messagerie({ nonLus }) {
  return (
    <header>
      <h2>Messagerie</h2>
      {nonLus > 0 && <span className="badge">{nonLus} non lu(s)</span>}
    </header>
  );
}
```

> **Piège classique** : n'écrivez pas `{nonLus && <span>…</span>}`. Quand `nonLus` vaut `0`, l'expression vaut `0`… et React **affiche les nombres**, donc un « 0 » apparaît à l'écran. Utilisez une vraie comparaison : `nonLus > 0 &&`.

Un composant peut aussi renvoyer `null` pour ne **rien** afficher du tout :

```jsx
export default function Alerte({ message }) {
  if (!message) return null;
  return <div role="alert">{message}</div>;
}
```

## Afficher une liste avec `map`

Le JSX accepte un **tableau d'éléments** entre accolades. Pour afficher une liste, on transforme donc un tableau de données en tableau de JSX avec `map` :

```jsx
const villes = [
  { id: "par", nom: "Paris", habitants: 2100000 },
  { id: "lyo", nom: "Lyon", habitants: 520000 },
  { id: "lil", nom: "Lille", habitants: 236000 },
];

export default function ListeVilles() {
  return (
    <ul>
      {villes.map((ville) => (
        <li key={ville.id}>
          {ville.nom} — {ville.habitants.toLocaleString("fr-FR")} habitants
        </li>
      ))}
    </ul>
  );
}
```

> Les nombres d'habitants de cet exemple sont des valeurs arrondies données à titre d'illustration.

## Les clés (`key`)

Chaque élément d'une liste doit recevoir un attribut **`key`** : une valeur qui l'identifie **de façon unique parmi ses frères** et **stable** dans le temps. Quand la liste change (ajout, suppression, tri), React s'appuie sur les clés pour savoir quel élément est lequel, et donc quel élément du DOM et quel état conserver.

Sans clé, React affiche un avertissement dans la console et identifie les éléments par leur position : après une suppression ou un tri, l'état d'un élément (case cochée, texte saisi) peut se retrouver associé au mauvais élément.

| Source de la clé | Verdict |
|---|---|
| identifiant venant des données (`id` d'une base, code unique) | à privilégier |
| identifiant créé **une fois** à l'ajout (`crypto.randomUUID()`, compteur) | correct |
| position dans le tableau (`index`) | seulement pour une liste **fixe**, jamais triée ni filtrée |
| `Math.random()` dans le rendu | à proscrire : la clé change à chaque rendu |

Quelques précisions :

- la clé se place sur l'élément **renvoyé directement par `map`** (ici le `<li>`), pas sur un élément à l'intérieur ;
- les clés doivent être uniques entre frères, pas dans toute l'application ;
- `key` n'est pas transmise au composant comme prop : si l'enfant a besoin de l'identifiant, passez-le aussi dans une autre prop (`id={produit.id}`).

```jsx
function LigneProduit({ id, nom }) {
  return (
    <li>
      {nom} <small>(réf. {id})</small>
    </li>
  );
}

export default function ListeProduits({ produits }) {
  return (
    <ul>
      {produits.map((p) => (
        <LigneProduit key={p.id} id={p.id} nom={p.nom} />
      ))}
    </ul>
  );
}
```

Si chaque élément doit produire **plusieurs** balises sans enveloppe, utilisez `Fragment` avec une clé (la syntaxe courte `<>` n'accepte pas d'attribut) :

```jsx
import { Fragment } from "react";

export default function Glossaire({ termes }) {
  return (
    <dl>
      {termes.map((t) => (
        <Fragment key={t.id}>
          <dt>{t.mot}</dt>
          <dd>{t.definition}</dd>
        </Fragment>
      ))}
    </dl>
  );
}
```

## Filtrer et trier avant d'afficher

On prépare les données **avant** le `map`, avec des fonctions JavaScript ordinaires. Les écrire sous forme de fonctions pures permet de les tester sans React :

```js
const produits = [
  { id: 1, nom: "Clavier", prix: 45, stock: 12 },
  { id: 2, nom: "Souris", prix: 20, stock: 0 },
  { id: 3, nom: "Écran", prix: 180, stock: 3 },
  { id: 4, nom: "Casque", prix: 59, stock: 7 },
];

function disponiblesParPrix(liste) {
  return liste
    .filter((p) => p.stock > 0)
    .toSorted((a, b) => a.prix - b.prix);
}

console.log(disponiblesParPrix(produits).map((p) => `${p.nom} : ${p.prix} €`));
console.log(produits.length);
```

```text
[ 'Clavier : 45 €', 'Casque : 59 €', 'Écran : 180 €' ]
4
```

`toSorted` renvoie une **copie** triée (comme `[...liste].sort()`), sans modifier le tableau d'origine — indispensable quand ce tableau provient des props ou de l'état. Si vous devez prendre en charge d'anciens navigateurs, préférez `[...liste].sort(...)`, qui produit le même résultat.

Dans le composant :

```jsx
export default function Vitrine({ produits }) {
  const visibles = produits.filter((p) => p.stock > 0);

  if (visibles.length === 0) {
    return <p>Aucun produit disponible pour le moment.</p>;
  }

  return (
    <ul>
      {visibles.map((p) => (
        <li key={p.id}>
          {p.nom} — {p.prix} €{p.stock < 5 && <em> (plus que {p.stock})</em>}
        </li>
      ))}
    </ul>
  );
}
```

> Prévoyez toujours l'**état vide** d'une liste (aucun résultat, aucune donnée) : un message clair vaut mieux qu'un écran blanc.

## À retenir

- `if` + `return` anticipé pour un rendu entièrement différent ; ternaire pour deux variantes ; `&&` pour « ceci ou rien ».
- `{n > 0 && …}` et non `{n && …}`, sinon un `0` s'affiche.
- Une liste s'affiche avec `map` ; chaque élément renvoyé reçoit une `key` unique et stable.
- Les clés viennent des données ; l'index seulement pour une liste figée ; jamais `Math.random()`.
- Filtrez et triez avant le `map`, sans modifier le tableau d'origine.

## Exercices

### Exercice 1 — Liste de tâches

Écrivez un composant `ListeTaches` qui reçoit une prop `taches` (tableau d'objets `{ id, titre, faite }`) et affiche une liste à puces ; les tâches faites sont précédées de `✓`. Si la liste est vide, affichez `Rien à faire !`.

```solution-jsx
export default function ListeTaches({ taches }) {
  if (taches.length === 0) {
    return <p>Rien à faire !</p>;
  }
  return (
    <ul>
      {taches.map((t) => (
        <li key={t.id}>
          {t.faite && "✓ "}
          {t.titre}
        </li>
      ))}
    </ul>
  );
}
```

### Exercice 2 — Préparer les données

Écrivez une fonction pure `meilleursEleves(eleves, seuil)` qui renvoie les noms des élèves dont la note est supérieure ou égale au seuil, triés par note décroissante.

```solution-js
const eleves = [
  { id: 1, nom: "Amina", note: 15 },
  { id: 2, nom: "Lucas", note: 9 },
  { id: 3, nom: "Sofia", note: 18 },
  { id: 4, nom: "Karim", note: 12 },
];

function meilleursEleves(liste, seuil) {
  return liste
    .filter((e) => e.note >= seuil)
    .toSorted((a, b) => b.note - a.note)
    .map((e) => e.nom);
}

console.log(meilleursEleves(eleves, 12));
```

```text
[ 'Sofia', 'Amina', 'Karim' ]
```

### Exercice 3 — Corrigez les clés

Ce code fonctionne mais pose deux problèmes. Lesquels ?

```jsx
{commentaires.map((c) => (
  <div>
    <Commentaire key={Math.random()} texte={c.texte} />
  </div>
))}
```

```solution-text
1. La clé n'est pas sur l'élément renvoyé par map (le <div>), mais sur un enfant : React signale
   toujours une clé manquante.
2. Math.random() produit une nouvelle clé à chaque rendu : React recrée tous les éléments et perd
   leur état. Il faut une clé stable issue des données :

{commentaires.map((c) => (
  <div key={c.id}>
    <Commentaire texte={c.texte} />
  </div>
))}
```
"""

M3_L2 = r"""
## Les champs contrôlés

Dans un formulaire HTML classique, c'est le navigateur qui mémorise ce que l'utilisateur tape. En React, on préfère que la valeur du champ soit **stockée dans l'état** : on parle de **champ contrôlé** (*controlled input*).

```jsx
import { useState } from "react";

export default function ChampPrenom() {
  const [prenom, setPrenom] = useState("");

  return (
    <div>
      <label htmlFor="prenom">Prénom</label>
      <input id="prenom" value={prenom} onChange={(e) => setPrenom(e.target.value)} />
      <p>Aperçu : {prenom || "(vide)"}</p>
    </div>
  );
}
```

Le fonctionnement repose sur deux attributs :

1. `value={prenom}` : le champ affiche **toujours** la valeur de l'état ;
2. `onChange` : à chaque frappe, on enregistre la nouvelle valeur dans l'état, ce qui provoque un rendu qui met le champ à jour.

L'état devient l'**unique source de vérité** : vous pouvez afficher la saisie ailleurs, la transformer, la valider pendant la frappe ou vider le champ en appelant `setPrenom("")`.

> En React, `onChange` se déclenche **à chaque modification** de la valeur (comme l'événement `input` du DOM), et non seulement quand le champ perd le focus.

Si vous écrivez `value={prenom}` **sans** `onChange`, le champ devient impossible à modifier et React affiche un avertissement dans la console. Pour un champ volontairement non modifiable, ajoutez `readOnly`.

## Transformer la saisie

Comme vous contrôlez la valeur, vous pouvez la transformer avant de l'enregistrer :

```jsx
import { useState } from "react";

export default function CodePostal() {
  const [code, setCode] = useState("");

  function gererSaisie(e) {
    const chiffres = e.target.value.replace(/\D/g, "").slice(0, 5); // chiffres uniquement, 5 maximum
    setCode(chiffres);
  }

  return (
    <label>
      Code postal <input inputMode="numeric" value={code} onChange={gererSaisie} />
    </label>
  );
}
```

## Les autres types de champs

| Champ | Attribut lié à l'état | Valeur lue dans `onChange` |
|---|---|---|
| `<input>`, `<textarea>` | `value` | `e.target.value` (toujours une **chaîne**) |
| `<input type="checkbox">` | `checked` | `e.target.checked` (booléen) |
| `<input type="radio">` | `checked={choix === "x"}` | `e.target.value` |
| `<select>` | `value` | `e.target.value` |

En JSX, `<textarea>` et `<select>` reçoivent eux aussi un attribut `value` (en HTML, on écrirait le texte entre les balises ou l'attribut `selected` sur une option).

```jsx
import { useState } from "react";

export default function Preferences() {
  const [frequence, setFrequence] = useState("hebdo");
  const [accepte, setAccepte] = useState(false);
  const [format, setFormat] = useState("html");

  return (
    <fieldset>
      <legend>Newsletter</legend>

      <label>
        Fréquence{" "}
        <select value={frequence} onChange={(e) => setFrequence(e.target.value)}>
          <option value="quotidien">Quotidienne</option>
          <option value="hebdo">Hebdomadaire</option>
          <option value="mensuel">Mensuelle</option>
        </select>
      </label>

      <label>
        <input type="radio" name="format" value="html" checked={format === "html"} onChange={(e) => setFormat(e.target.value)} />
        HTML
      </label>
      <label>
        <input type="radio" name="format" value="texte" checked={format === "texte"} onChange={(e) => setFormat(e.target.value)} />
        Texte
      </label>

      <label>
        <input type="checkbox" checked={accepte} onChange={(e) => setAccepte(e.target.checked)} />
        J'accepte de recevoir la newsletter
      </label>
    </fieldset>
  );
}
```

> Les valeurs d'un champ texte sont **toujours des chaînes**, même avec `type="number"`. Convertissez-les avec `Number()` avant de calculer.

## Un seul état pour tout le formulaire

Quand un formulaire comporte beaucoup de champs, on peut les regrouper dans **un objet** et utiliser un **gestionnaire unique** qui s'appuie sur l'attribut `name` de chaque champ. L'écriture `[nom]: valeur` (propriété **calculée**) crée une propriété dont le nom est contenu dans une variable :

```js
const formulaire = { nom: "", email: "" };

function mettreAJour(etat, nom, valeur) {
  return { ...etat, [nom]: valeur };
}

const etape1 = mettreAJour(formulaire, "nom", "Rossi");
const etape2 = mettreAJour(etape1, "email", "rossi@exemple.fr");
console.log(etape2);
console.log(formulaire);
```

```text
{ nom: 'Rossi', email: 'rossi@exemple.fr' }
{ nom: '', email: '' }
```

## Valider et envoyer

La validation s'écrit elle aussi comme une **fonction pure** : elle reçoit les valeurs et renvoie un objet d'erreurs (vide si tout va bien).

```js
function valider({ nom, email, age }) {
  const erreurs = {};
  if (nom.trim() === "") erreurs.nom = "Le nom est obligatoire.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) erreurs.email = "Adresse email invalide.";
  const ageNombre = Number(age);
  if (!Number.isInteger(ageNombre) || ageNombre < 16) erreurs.age = "Vous devez avoir au moins 16 ans.";
  return erreurs;
}

console.log(valider({ nom: "", email: "sofia@exemple", age: "15" }));
console.log(valider({ nom: "Sofia", email: "sofia@exemple.fr", age: "27" }));
```

```text
{
  nom: 'Le nom est obligatoire.',
  email: 'Adresse email invalide.',
  age: 'Vous devez avoir au moins 16 ans.'
}
{}
```

Le composant assemble l'état, le gestionnaire unique, la validation et l'envoi :

```jsx
import { useState } from "react";

const VIDE = { nom: "", email: "", age: "" };

function valider({ nom, email, age }) {
  const erreurs = {};
  if (nom.trim() === "") erreurs.nom = "Le nom est obligatoire.";
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) erreurs.email = "Adresse email invalide.";
  const ageNombre = Number(age);
  if (!Number.isInteger(ageNombre) || ageNombre < 16) erreurs.age = "Vous devez avoir au moins 16 ans.";
  return erreurs;
}

export default function Inscription() {
  const [valeurs, setValeurs] = useState(VIDE);
  const [erreurs, setErreurs] = useState({});
  const [message, setMessage] = useState("");

  function gererChangement(e) {
    const { name, value } = e.target;
    setValeurs((v) => ({ ...v, [name]: value }));
  }

  function gererEnvoi(e) {
    e.preventDefault();
    const trouvees = valider(valeurs);
    setErreurs(trouvees);
    if (Object.keys(trouvees).length > 0) return;
    setMessage(`Merci ${valeurs.nom}, votre inscription est enregistrée.`);
    setValeurs(VIDE);
  }

  return (
    <form onSubmit={gererEnvoi} noValidate>
      <label htmlFor="nom">Nom</label>
      <input id="nom" name="nom" value={valeurs.nom} onChange={gererChangement} />
      {erreurs.nom && <p className="erreur">{erreurs.nom}</p>}

      <label htmlFor="email">Email</label>
      <input id="email" name="email" type="email" value={valeurs.email} onChange={gererChangement} />
      {erreurs.email && <p className="erreur">{erreurs.email}</p>}

      <label htmlFor="age">Âge</label>
      <input id="age" name="age" type="number" value={valeurs.age} onChange={gererChangement} />
      {erreurs.age && <p className="erreur">{erreurs.age}</p>}

      <button type="submit">S'inscrire</button>
      {message && <p role="status">{message}</p>}
    </form>
  );
}
```

- `e.preventDefault()` empêche le rechargement de la page ;
- `noValidate` désactive les bulles de validation du navigateur, pour afficher nos propres messages ;
- chaque `<label htmlFor>` est relié à son champ : c'est indispensable pour l'accessibilité.

> La validation dans le navigateur améliore le confort de l'utilisateur, mais elle se contourne facilement : le **serveur doit toujours revérifier** les données reçues.

## Champs non contrôlés

Il existe une alternative : laisser le navigateur gérer la valeur (`defaultValue` pour la valeur initiale) et la lire seulement à l'envoi, par exemple avec `new FormData(e.target)`. C'est suffisant pour un formulaire très simple ; les champs contrôlés restent préférables dès que l'interface doit réagir pendant la saisie.

## À retenir

- Champ contrôlé : `value={etat}` + `onChange={(e) => setEtat(e.target.value)}`.
- Case à cocher : `checked` et `e.target.checked` ; `select` et `textarea` utilisent `value`.
- Les valeurs saisies sont des **chaînes** : convertissez avec `Number()`.
- Un objet d'état + `name` + `[name]: value` pour un gestionnaire unique.
- `onSubmit` sur le `<form>`, `e.preventDefault()`, validation par une fonction pure ; le serveur revérifie toujours.

## Exercices

### Exercice 1 — Fonction de validation

Écrivez une fonction pure `validerMotDePasse(mdp)` qui renvoie un tableau de messages : au moins 12 caractères, au moins un chiffre, au moins une majuscule. Testez-la avec `"secret"` et `"MotDePasse2025!"`.

```solution-js
function validerMotDePasse(mdp) {
  const problemes = [];
  if (mdp.length < 12) problemes.push("Au moins 12 caractères.");
  if (!/\d/.test(mdp)) problemes.push("Au moins un chiffre.");
  if (!/[A-Z]/.test(mdp)) problemes.push("Au moins une majuscule.");
  return problemes;
}

console.log(validerMotDePasse("secret"));
console.log(validerMotDePasse("MotDePasse2025!"));
```

```text
[
  'Au moins 12 caractères.',
  'Au moins un chiffre.',
  'Au moins une majuscule.'
]
[]
```

### Exercice 2 — Compteur de caractères

Écrivez un composant `Avis` avec une zone de texte contrôlée limitée à 200 caractères, qui affiche `n / 200` sous le champ et désactive le bouton « Publier » tant que le texte est vide.

```solution-jsx
import { useState } from "react";

const MAX = 200;

export default function Avis() {
  const [texte, setTexte] = useState("");

  return (
    <form onSubmit={(e) => e.preventDefault()}>
      <label htmlFor="avis">Votre avis</label>
      <textarea id="avis" value={texte} maxLength={MAX} onChange={(e) => setTexte(e.target.value)} />
      <p>
        {texte.length} / {MAX}
      </p>
      <button type="submit" disabled={texte.trim() === ""}>
        Publier
      </button>
    </form>
  );
}
```

### Exercice 3 — Champ bloqué

Un développeur écrit `<input value={ville} />` et ne parvient plus à taper dans le champ. Expliquez pourquoi et proposez deux corrections selon le besoin.

```solution-text
Le champ est contrôlé (value lié à l'état) mais rien ne met l'état à jour : à chaque frappe,
React réaffiche la valeur de ville, qui n'a pas changé.

- Si le champ doit être modifiable : ajouter onChange={(e) => setVille(e.target.value)}.
- Si le champ doit seulement afficher la valeur : ajouter readOnly (ou utiliser defaultValue
  pour un champ non contrôlé avec une valeur de départ).
```
"""

M3_L3 = r"""
## Quand deux composants ont besoin de la même donnée

Imaginez une page de recherche composée de deux composants frères : une `BarreRecherche` où l'on tape un texte, et une `ListeResultats` qui doit afficher les éléments correspondants. Si le texte est stocké dans l'état de `BarreRecherche`, la liste n'y a pas accès : l'état est **local** à son composant.

La solution s'appelle **remonter l'état** (*lifting state up*) :

1. on déplace l'état dans le **plus proche parent commun** des deux composants ;
2. le parent transmet la **valeur** aux enfants par les props ;
3. le parent transmet aussi une **fonction** qui permet à l'enfant de demander une modification.

```jsx
import { useState } from "react";

const LIVRES = [
  { id: 1, titre: "Le Jardin des étoiles", auteur: "Claire Morel" },
  { id: 2, titre: "Rivières de sel", auteur: "Hugo Bernard" },
  { id: 3, titre: "Le Dernier Phare", auteur: "Nadia Benali" },
];

function BarreRecherche({ texte, onTexteChange }) {
  return (
    <input
      type="search"
      placeholder="Titre ou auteur…"
      value={texte}
      onChange={(e) => onTexteChange(e.target.value)}
    />
  );
}

function ListeResultats({ livres }) {
  if (livres.length === 0) return <p>Aucun livre trouvé.</p>;
  return (
    <ul>
      {livres.map((l) => (
        <li key={l.id}>
          {l.titre} — {l.auteur}
        </li>
      ))}
    </ul>
  );
}

export default function Bibliotheque() {
  const [texte, setTexte] = useState("");
  const recherche = texte.trim().toLowerCase();
  const resultats = LIVRES.filter(
    (l) => l.titre.toLowerCase().includes(recherche) || l.auteur.toLowerCase().includes(recherche)
  );

  return (
    <>
      <BarreRecherche texte={texte} onTexteChange={setTexte} />
      <ListeResultats livres={resultats} />
    </>
  );
}
```

Les livres et leurs auteurs sont fictifs. `BarreRecherche` est maintenant un composant **contrôlé par son parent** : il n'a plus d'état propre, il affiche ce qu'on lui donne et signale les changements. Cette organisation illustre le **flux de données à sens unique** : les données descendent, les demandes de modification remontent.

## Les données dérivées

Remarquez que `resultats` n'est **pas** un état : c'est une **donnée dérivée**, recalculée à chaque rendu à partir de l'état (`texte`) et des données (`LIVRES`). Stocker `resultats` dans un second `useState` serait une erreur fréquente :

- il faudrait penser à le mettre à jour à chaque changement de `texte` ;
- les deux états pourraient se **désynchroniser** et afficher des informations contradictoires.

> Règle d'or : **si une valeur peut se calculer à partir des props ou de l'état existants, ne la stockez pas — calculez-la pendant le rendu.**

Ces calculs gagnent à être écrits dans des fonctions pures, testables séparément :

```js
function statistiquesPanier(lignes) {
  const articles = lignes.reduce((total, l) => total + l.quantite, 0);
  const montant = lignes.reduce((total, l) => total + l.quantite * l.prixUnitaire, 0);
  return { articles, montant: Math.round(montant * 100) / 100, vide: lignes.length === 0 };
}

const panier = [
  { id: "a1", nom: "Cahier", quantite: 3, prixUnitaire: 2.5 },
  { id: "b7", nom: "Stylo", quantite: 10, prixUnitaire: 0.9 },
];

console.log(statistiquesPanier(panier));
console.log(statistiquesPanier([]));
```

```text
{ articles: 13, montant: 16.5, vide: false }
{ articles: 0, montant: 0, vide: true }
```

Le composant n'a besoin que de l'état `lignes` : nombre d'articles, montant et panier vide s'en déduisent.

> Un calcul dérivé très coûteux (des milliers d'éléments, des calculs lourds) peut être mis en cache avec le hook `useMemo`. Pour des listes de taille ordinaire, le calcul direct suffit : n'optimisez qu'après avoir constaté une lenteur.

## Un seul élément ouvert à la fois

Autre cas typique : un accordéon (*accordion*) dont un seul panneau peut être ouvert. Si chaque panneau gérait son propre état `ouvert`, plusieurs pourraient l'être en même temps. On remonte donc l'information « quel panneau est ouvert » dans le parent, sous forme d'**identifiant** :

```jsx
import { useState } from "react";

function Panneau({ titre, ouvert, onOuvrir, children }) {
  return (
    <section>
      <h3>
        <button aria-expanded={ouvert} onClick={onOuvrir}>
          {titre}
        </button>
      </h3>
      {ouvert && <div>{children}</div>}
    </section>
  );
}

export default function Faq() {
  const [ouvertId, setOuvertId] = useState("livraison");

  return (
    <>
      <Panneau titre="Livraison" ouvert={ouvertId === "livraison"} onOuvrir={() => setOuvertId("livraison")}>
        <p>Les commandes sont expédiées sous 48 h ouvrées.</p>
      </Panneau>
      <Panneau titre="Retours" ouvert={ouvertId === "retours"} onOuvrir={() => setOuvertId("retours")}>
        <p>Vous disposez de 30 jours pour nous retourner un article.</p>
      </Panneau>
    </>
  );
}
```

Les délais affichés sont ceux d'une boutique fictive.

## Penser une interface en composants

Face à une maquette, cette démarche en cinq étapes aide à structurer une application React :

1. **Découper** la maquette en composants (un composant = une responsabilité) et dessiner leur arbre.
2. Écrire une **version statique** qui affiche des données d'exemple avec des props, sans état.
3. Identifier l'**état minimal** : ce qui change au fil du temps, n'est pas transmis par le parent et ne peut pas se calculer.
4. Décider **où placer** chaque état : dans le plus proche parent commun de tous les composants qui l'utilisent.
5. Ajouter le **flux inverse** : des fonctions passées en props pour que les enfants demandent des modifications.

Pour la page de recherche : la liste des livres est une donnée fixe (pas un état), le texte saisi est un état, la liste filtrée est dérivée.

## Composer plutôt que transmettre en cascade

Quand une donnée doit traverser de nombreux niveaux de composants qui ne l'utilisent pas, on parle de **passage de props en cascade** (*prop drilling*). Deux remèdes :

- la **composition** : passer directement des éléments JSX via `children` (ou d'autres props), pour que le composant intermédiaire n'ait pas à connaître la donnée ;
- le **contexte**, présenté au module 4, pour les données utiles à toute une partie de l'application (thème, utilisateur connecté, langue).

```jsx
function Mise({ entete, children }) {
  return (
    <div className="mise">
      <header>{entete}</header>
      <main>{children}</main>
    </div>
  );
}

export default function Page({ utilisateur }) {
  // Mise ne reçoit pas « utilisateur » : on lui passe directement l'élément prêt à afficher.
  return (
    <Mise entete={<p>Connecté : {utilisateur.prenom}</p>}>
      <p>Contenu de la page</p>
    </Mise>
  );
}
```

## À retenir

- Deux composants partagent une donnée → l'état remonte dans leur plus proche parent commun.
- Le parent passe la valeur et une fonction de modification (`onXChange`) en props.
- Les **données dérivées** se calculent pendant le rendu ; on ne les stocke pas dans l'état.
- Pour « un seul élément sélectionné », on stocke son **identifiant** dans le parent.
- Démarche : découper, version statique, état minimal, emplacement de l'état, flux inverse.

## Exercices

### Exercice 1 — Identifier l'état minimal

Une page affiche une liste de produits (venant des props), un champ de recherche, une case « en stock uniquement », le nombre de produits affichés et le produit sélectionné. Quels éléments sont des états ?

```solution-text
États : le texte de recherche, la case « en stock uniquement » et l'identifiant du produit sélectionné.
Pas des états : la liste de produits (reçue en props) et le nombre de produits affichés
(dérivé : on le calcule en filtrant la liste avec la recherche et la case).
```

### Exercice 2 — Onglets

Écrivez un composant `Onglets` qui affiche trois boutons (« Description », « Avis », « Livraison ») et le contenu de l'onglet actif. Le bouton actif reçoit la classe `actif`.

```solution-jsx
import { useState } from "react";

const ONGLETS = [
  { id: "description", titre: "Description", contenu: "Un sac léger et robuste." },
  { id: "avis", titre: "Avis", contenu: "Aucun avis pour le moment." },
  { id: "livraison", titre: "Livraison", contenu: "Expédition sous 48 h ouvrées." },
];

export default function Onglets() {
  const [actif, setActif] = useState("description");
  const courant = ONGLETS.find((o) => o.id === actif);

  return (
    <div>
      {ONGLETS.map((o) => (
        <button key={o.id} className={o.id === actif ? "actif" : ""} onClick={() => setActif(o.id)}>
          {o.titre}
        </button>
      ))}
      <p>{courant.contenu}</p>
    </div>
  );
}
```

### Exercice 3 — Une donnée dérivée

Écrivez une fonction pure `resumeTaches(taches)` qui renvoie le texte `x terminée(s) sur y (z %)`, le pourcentage étant arrondi à l'entier.

```solution-js
function resumeTaches(taches) {
  const total = taches.length;
  const faites = taches.filter((t) => t.faite).length;
  const pourcentage = total === 0 ? 0 : Math.round((faites / total) * 100);
  return `${faites} terminée(s) sur ${total} (${pourcentage} %)`;
}

console.log(resumeTaches([{ faite: true }, { faite: false }, { faite: true }]));
console.log(resumeTaches([]));
```

```text
2 terminée(s) sur 3 (67 %)
0 terminée(s) sur 0 (0 %)
```
"""

# ---------------------------------------------------------------------------
# Module 4 — Effets, réducteurs et contexte
# ---------------------------------------------------------------------------
M4_L1 = r"""
## À quoi sert un effet ?

Le rendu d'un composant doit rester **pur** : calculer du JSX à partir des props et de l'état, sans rien modifier à l'extérieur. Pourtant, une application doit parfois **se synchroniser avec un système extérieur à React** :

- modifier le titre de l'onglet (`document.title`) ;
- démarrer un minuteur (`setInterval`) ;
- écouter un événement de la fenêtre (redimensionnement, connexion réseau) ;
- charger des données depuis un serveur (module 5).

Ces opérations s'appellent des **effets de bord** (*side effects*). React fournit le hook **`useEffect`** pour les exécuter **après** l'affichage du composant.

```jsx
import { useEffect, useState } from "react";

export default function CompteurTitre() {
  const [compteur, setCompteur] = useState(0);

  useEffect(() => {
    document.title = `${compteur} clic(s)`;
  }, [compteur]);

  return <button onClick={() => setCompteur((c) => c + 1)}>Cliquer</button>;
}
```

`useEffect` reçoit deux arguments :

1. une **fonction** contenant l'effet ;
2. un **tableau de dépendances** : les valeurs utilisées par l'effet qui, lorsqu'elles changent, doivent le relancer.

## Le tableau de dépendances

| Écriture | Quand l'effet s'exécute-t-il ? |
|---|---|
| `useEffect(fn)` | après **chaque** rendu |
| `useEffect(fn, [])` | après le **premier** affichage seulement |
| `useEffect(fn, [a, b])` | après le premier affichage, puis quand `a` ou `b` a changé depuis le rendu précédent |

React compare chaque dépendance avec sa valeur précédente (avec `Object.is`, comme pour l'état).

> Le tableau de dépendances n'est pas un choix : il doit contenir **toutes** les props, variables d'état et fonctions du composant utilisées dans l'effet. La règle ESLint `react-hooks/exhaustive-deps` vous signale les oublis. Si une dépendance vous gêne, c'est souvent le signe que le code doit être réorganisé, pas qu'il faut la retirer.

## Le nettoyage

Un effet qui **démarre** quelque chose doit aussi savoir l'**arrêter**. Pour cela, la fonction d'effet peut renvoyer une **fonction de nettoyage** (*cleanup*). React l'appelle :

- avant de relancer l'effet (quand une dépendance a changé) ;
- quand le composant disparaît de l'écran (on dit qu'il est **démonté**).

```jsx
import { useEffect, useState } from "react";

export default function Horloge() {
  const [maintenant, setMaintenant] = useState(() => new Date());

  useEffect(() => {
    const id = setInterval(() => setMaintenant(new Date()), 1000);
    return () => clearInterval(id); // nettoyage : on arrête le minuteur
  }, []);

  return <p>Il est {maintenant.toLocaleTimeString("fr-FR")}</p>;
}
```

Sans `clearInterval`, chaque affichage de `Horloge` laisserait un minuteur tourner indéfiniment, même après la disparition du composant.

Même principe pour un écouteur d'événement :

```jsx
import { useEffect, useState } from "react";

export default function LargeurFenetre() {
  const [largeur, setLargeur] = useState(window.innerWidth);

  useEffect(() => {
    function gererRedimensionnement() {
      setLargeur(window.innerWidth);
    }
    window.addEventListener("resize", gererRedimensionnement);
    return () => window.removeEventListener("resize", gererRedimensionnement);
  }, []);

  return <p>Largeur de la fenêtre : {largeur} px</p>;
}
```

> En développement, le **mode strict** monte chaque composant, le démonte puis le remonte immédiatement : votre effet s'exécute donc deux fois, avec un nettoyage entre les deux. C'est volontaire : si l'application se comporte mal (deux minuteurs, deux abonnements), c'est qu'il manque un nettoyage. Ce double appel n'a pas lieu en production.

## Un effet qui dépend d'une prop

```jsx
import { useEffect, useState } from "react";

export default function Minuteur({ secondes }) {
  const [restant, setRestant] = useState(secondes);

  useEffect(() => {
    setRestant(secondes);
    const id = setInterval(() => {
      setRestant((r) => (r > 0 ? r - 1 : 0));
    }, 1000);
    return () => clearInterval(id);
  }, [secondes]);

  return <p>{restant > 0 ? `${restant} s` : "Terminé !"}</p>;
}
```

Si le parent change `secondes`, React nettoie l'ancien minuteur puis relance l'effet avec la nouvelle valeur. Notez la **fonction de mise à jour** `setRestant((r) => …)` : grâce à elle, l'effet n'a pas besoin de lire `restant`, qui n'est donc pas une dépendance.

## Les pièges classiques

**La boucle infinie** : un effet sans tableau de dépendances qui modifie l'état provoque un rendu, qui relance l'effet, qui modifie l'état…

```jsx
// À ne pas faire : boucle infinie
useEffect(() => {
  setCompteur(compteur + 1);
});
```

**La valeur figée** (*stale closure*) : un effet qui utilise une valeur sans la déclarer en dépendance continue de voir sa valeur au moment où il a été créé.

**Les objets créés pendant le rendu** : un objet ou une fonction déclaré dans le composant est **nouveau à chaque rendu** ; placé en dépendance, il relance l'effet à chaque fois. Déclarez-le à l'intérieur de l'effet, ou en dehors du composant s'il ne dépend de rien.

## Vous n'avez peut-être pas besoin d'un effet

Un effet sert à se synchroniser avec **l'extérieur**. Deux usages sont donc inutiles, et même nuisibles :

- **calculer une donnée dérivée** : `const total = prix * quantite;` pendant le rendu, et non un état `total` mis à jour dans un effet (ce qui provoque un rendu supplémentaire avec une valeur périmée entre les deux) ;
- **réagir à une action de l'utilisateur** : le code à exécuter après un clic ou un envoi de formulaire se place dans le **gestionnaire d'événement**, où l'on sait exactement ce qui s'est passé.

```jsx
// Inutile
const [total, setTotal] = useState(0);
useEffect(() => {
  setTotal(prix * quantite);
}, [prix, quantite]);

// Préférable
const total = prix * quantite;
```

## À retenir

- `useEffect(fn, deps)` exécute un effet **après** l'affichage, pour se synchroniser avec l'extérieur.
- `[]` : au premier affichage ; `[a, b]` : quand `a` ou `b` change ; pas de tableau : après chaque rendu.
- Toutes les valeurs du composant utilisées dans l'effet figurent dans les dépendances.
- Ce qui est démarré (minuteur, écouteur, abonnement) est arrêté dans la **fonction de nettoyage**.
- Pas d'effet pour une donnée dérivée ni pour réagir à un clic : calcul pendant le rendu ou gestionnaire d'événement.

## Exercices

### Exercice 1 — Titre de la page

Écrivez un composant `Messages` qui reçoit une prop `nonLus` et affiche `(3) Messagerie` dans le titre de l'onglet quand il y a des messages non lus, et `Messagerie` sinon.

```solution-jsx
import { useEffect } from "react";

export default function Messages({ nonLus }) {
  useEffect(() => {
    document.title = nonLus > 0 ? `(${nonLus}) Messagerie` : "Messagerie";
  }, [nonLus]);

  return <h1>Messagerie</h1>;
}
```

### Exercice 2 — Chronomètre

Écrivez un composant `Chrono` avec un bouton « Démarrer / Arrêter » et l'affichage des secondes écoulées. Le minuteur ne doit tourner que lorsque le chronomètre est démarré.

```solution-jsx
import { useEffect, useState } from "react";

export default function Chrono() {
  const [secondes, setSecondes] = useState(0);
  const [actif, setActif] = useState(false);

  useEffect(() => {
    if (!actif) return;
    const id = setInterval(() => setSecondes((s) => s + 1), 1000);
    return () => clearInterval(id);
  }, [actif]);

  return (
    <div>
      <p>{secondes} s</p>
      <button onClick={() => setActif((a) => !a)}>{actif ? "Arrêter" : "Démarrer"}</button>
      <button onClick={() => setSecondes(0)}>Remettre à zéro</button>
    </div>
  );
}
```

### Exercice 3 — Effet inutile

Simplifiez ce composant.

```jsx
function NomComplet({ prenom, nom }) {
  const [complet, setComplet] = useState("");
  useEffect(() => {
    setComplet(`${prenom} ${nom}`);
  }, [prenom, nom]);
  return <p>{complet}</p>;
}
```

```solution-jsx
function NomComplet({ prenom, nom }) {
  const complet = `${prenom} ${nom}`; // donnée dérivée : calculée pendant le rendu
  return <p>{complet}</p>;
}

export default NomComplet;
```
"""

M4_L2 = r"""
## Quand `useState` devient difficile à suivre

Dans un composant riche (panier, éditeur, jeu), les mises à jour de l'état se multiplient et se dispersent dans de nombreux gestionnaires. Il devient difficile de savoir **comment** l'état peut évoluer. Le hook **`useReducer`** propose de **centraliser** toute cette logique dans une seule fonction.

## Le principe du réducteur

Un **réducteur** (*reducer*) est une fonction **pure** qui reçoit l'état actuel et une **action** décrivant ce qui s'est passé, et qui renvoie le **nouvel état** :

```text
(étatActuel, action) => nouvelÉtat
```

Par convention, une action est un objet avec une propriété `type` et, si besoin, des données :

```js
function panierReducer(etat, action) {
  switch (action.type) {
    case "ajouter": {
      const existe = etat.find((l) => l.id === action.produit.id);
      if (existe) {
        return etat.map((l) => (l.id === action.produit.id ? { ...l, quantite: l.quantite + 1 } : l));
      }
      return [...etat, { ...action.produit, quantite: 1 }];
    }
    case "retirer":
      return etat.filter((l) => l.id !== action.id);
    case "vider":
      return [];
    default:
      throw new Error(`Action inconnue : ${action.type}`);
  }
}

const actions = [
  { type: "ajouter", produit: { id: "p1", nom: "Cahier" } },
  { type: "ajouter", produit: { id: "p2", nom: "Stylo" } },
  { type: "ajouter", produit: { id: "p1", nom: "Cahier" } },
  { type: "retirer", id: "p2" },
];

const etatFinal = actions.reduce(panierReducer, []);
console.log(etatFinal);

try {
  panierReducer([], { type: "payer" });
} catch (e) {
  console.log(e.message);
}
```

```text
[ { id: 'p1', nom: 'Cahier', quantite: 2 } ]
Action inconnue : payer
```

Le nom vient de là : appliquer une suite d'actions à un état initial revient exactement à appeler `reduce` sur un tableau d'actions. Comme le réducteur est une fonction pure, on peut le **tester sans React**, simplement avec des données.

Les règles d'un réducteur sont celles de l'état : **ne jamais muter** `etat`, toujours renvoyer une nouvelle valeur, et ne rien faire d'autre (pas d'appel réseau, pas de minuteur). Lever une erreur pour une action inconnue aide à repérer les fautes de frappe.

## Utiliser `useReducer`

```jsx
import { useReducer } from "react";

function panierReducer(etat, action) {
  switch (action.type) {
    case "ajouter": {
      const existe = etat.find((l) => l.id === action.produit.id);
      if (existe) {
        return etat.map((l) => (l.id === action.produit.id ? { ...l, quantite: l.quantite + 1 } : l));
      }
      return [...etat, { ...action.produit, quantite: 1 }];
    }
    case "retirer":
      return etat.filter((l) => l.id !== action.id);
    case "vider":
      return [];
    default:
      throw new Error(`Action inconnue : ${action.type}`);
  }
}

const PRODUITS = [
  { id: "p1", nom: "Cahier" },
  { id: "p2", nom: "Stylo" },
];

export default function Panier() {
  const [lignes, dispatch] = useReducer(panierReducer, []);

  return (
    <div>
      {PRODUITS.map((p) => (
        <button key={p.id} onClick={() => dispatch({ type: "ajouter", produit: p })}>
          Ajouter {p.nom}
        </button>
      ))}
      <ul>
        {lignes.map((l) => (
          <li key={l.id}>
            {l.nom} × {l.quantite}{" "}
            <button onClick={() => dispatch({ type: "retirer", id: l.id })}>Retirer</button>
          </li>
        ))}
      </ul>
      {lignes.length > 0 && <button onClick={() => dispatch({ type: "vider" })}>Vider le panier</button>}
    </div>
  );
}
```

- `useReducer(reducteur, etatInitial)` renvoie l'état actuel et une fonction **`dispatch`** ;
- `dispatch(action)` envoie une action : React appelle le réducteur et effectue un nouveau rendu avec l'état obtenu ;
- les gestionnaires décrivent **ce qui s'est passé** (« ajouter tel produit ») ; le réducteur décide **comment** l'état change.

| | `useState` | `useReducer` |
|---|---|---|
| Idéal pour | valeurs simples et indépendantes | état structuré, nombreuses façons de le modifier |
| Logique de mise à jour | dans chaque gestionnaire | centralisée dans le réducteur |
| Tests | via le composant | réducteur testable seul |

Les deux se valent pour React : choisissez celui qui rend le code le plus lisible.

## `useRef` : mémoriser sans provoquer de rendu

Le hook **`useRef`** renvoie un objet `{ current: valeurInitiale }` que React **conserve** d'un rendu à l'autre. Contrairement à l'état, **modifier `ref.current` ne déclenche pas de rendu**. On l'utilise pour deux besoins.

### 1. Garder une valeur technique

Par exemple, l'identifiant d'un minuteur, nécessaire pour l'arrêter mais inutile à l'affichage :

```jsx
import { useRef, useState } from "react";

export default function Chronometre() {
  const [secondes, setSecondes] = useState(0);
  const idRef = useRef(null);

  function demarrer() {
    if (idRef.current !== null) return; // déjà démarré
    idRef.current = setInterval(() => setSecondes((s) => s + 1), 1000);
  }

  function arreter() {
    clearInterval(idRef.current);
    idRef.current = null;
  }

  return (
    <div>
      <p>{secondes} s</p>
      <button onClick={demarrer}>Démarrer</button>
      <button onClick={arreter}>Arrêter</button>
    </div>
  );
}
```

### 2. Accéder à un élément du DOM

En passant une ref à l'attribut `ref` d'une balise, React place l'élément du DOM correspondant dans `ref.current` une fois l'élément affiché. Utile pour donner le focus à un champ, faire défiler la page ou mesurer un élément :

```jsx
import { useRef } from "react";

export default function RechercheRapide() {
  const champRef = useRef(null);

  return (
    <div>
      <input ref={champRef} placeholder="Rechercher…" />
      <button onClick={() => champRef.current.focus()}>Aller à la recherche</button>
    </div>
  );
}
```

> Ne lisez pas et n'écrivez pas `ref.current` **pendant le rendu** (dans le corps du composant, hors initialisation) : le résultat serait imprévisible, puisque React n'est pas prévenu des changements. Utilisez les refs dans les gestionnaires d'événements et les effets. Si une valeur doit apparaître à l'écran, c'est un **état**.

| | État (`useState`) | Ref (`useRef`) |
|---|---|---|
| Conservé entre les rendus | oui | oui |
| Modification → nouveau rendu | oui | non |
| Lecture pendant le rendu | oui | à éviter |
| Usage | ce qui s'affiche | identifiants techniques, éléments du DOM |

## À retenir

- Un réducteur est une fonction pure `(etat, action) => nouvelEtat`, souvent écrite avec `switch`.
- `const [etat, dispatch] = useReducer(reducteur, initial)` ; `dispatch({ type, ... })` envoie une action.
- Le réducteur centralise la logique et se teste sans React.
- `useRef` conserve une valeur sans déclencher de rendu ; `ref={maRef}` donne accès à un élément du DOM.
- Ce qui s'affiche va dans l'état ; ce qui est purement technique peut aller dans une ref.

## Exercices

### Exercice 1 — Réducteur de compteur

Écrivez un réducteur `compteurReducer` gérant les actions `incrementer`, `decrementer` (sans descendre sous 0) et `definir` (avec une propriété `valeur`). Testez-le en appliquant une suite d'actions avec `reduce`.

```solution-js
function compteurReducer(etat, action) {
  switch (action.type) {
    case "incrementer":
      return { valeur: etat.valeur + 1 };
    case "decrementer":
      return { valeur: Math.max(0, etat.valeur - 1) };
    case "definir":
      return { valeur: action.valeur };
    default:
      throw new Error(`Action inconnue : ${action.type}`);
  }
}

const suite = [
  { type: "incrementer" },
  { type: "incrementer" },
  { type: "decrementer" },
  { type: "decrementer" },
  { type: "decrementer" },
  { type: "definir", valeur: 10 },
  { type: "incrementer" },
];
console.log(suite.reduce(compteurReducer, { valeur: 0 }));
```

```text
{ valeur: 11 }
```

### Exercice 2 — Focus après envoi

Écrivez un composant `AjoutRapide` avec un champ contrôlé et un bouton « Ajouter ». Après chaque ajout, le champ est vidé et reprend le focus ; les éléments ajoutés s'affichent dans une liste.

```solution-jsx
import { useRef, useState } from "react";

export default function AjoutRapide() {
  const [texte, setTexte] = useState("");
  const [elements, setElements] = useState([]);
  const champRef = useRef(null);

  function gererEnvoi(e) {
    e.preventDefault();
    if (texte.trim() === "") return;
    setElements((liste) => [...liste, { id: crypto.randomUUID(), texte: texte.trim() }]);
    setTexte("");
    champRef.current.focus();
  }

  return (
    <form onSubmit={gererEnvoi}>
      <input ref={champRef} value={texte} onChange={(e) => setTexte(e.target.value)} />
      <button type="submit">Ajouter</button>
      <ul>
        {elements.map((el) => (
          <li key={el.id}>{el.texte}</li>
        ))}
      </ul>
    </form>
  );
}
```

`crypto.randomUUID()` est appelé **une seule fois**, au moment de l'ajout : la clé reste donc stable ensuite (rien à voir avec `Math.random()` dans le rendu).

### Exercice 3 — État ou ref ?

Pour chaque valeur, choisissez état ou ref : (a) le texte d'un champ de recherche affiché ; (b) l'identifiant d'un `setTimeout` à annuler ; (c) le nombre de clics affiché à l'écran ; (d) l'élément `<video>` à mettre en pause.

```solution-text
(a) état : la valeur s'affiche dans le champ.
(b) ref : valeur technique, inutile à l'affichage.
(c) état : la valeur s'affiche, sa modification doit déclencher un rendu.
(d) ref : on accède à l'élément du DOM pour appeler sa méthode pause().
```
"""

M4_L3 = r"""
## Le problème du passage en cascade

Certaines informations intéressent de **nombreux** composants à des profondeurs différentes : le thème (clair ou sombre), la langue, l'utilisateur connecté. Les transmettre par les props oblige chaque composant intermédiaire à recevoir et retransmettre des données qu'il n'utilise pas : c'est le **passage de props en cascade** (*prop drilling*).

```text
App (theme)
└── Page (theme)            ← n'utilise pas theme, le transmet
    └── Barre (theme)       ← n'utilise pas theme, le transmet
        └── Bouton (theme)  ← l'utilise enfin
```

Le **contexte** permet à un composant de fournir une valeur à **tous ses descendants**, quelle que soit leur profondeur, sans passer par les composants intermédiaires.

## Les trois étapes

### 1. Créer le contexte

```jsx
// src/ThemeContext.js
import { createContext } from "react";

export const ThemeContext = createContext("clair");
```

L'argument de `createContext` est la **valeur par défaut**, utilisée seulement si un composant lit le contexte sans qu'aucun fournisseur ne soit présent au-dessus de lui.

### 2. Fournir une valeur

On entoure une partie de l'arbre avec le **fournisseur** (*Provider*) du contexte :

```jsx
import { useState } from "react";
import { ThemeContext } from "./ThemeContext.js";
import Page from "./Page.jsx";

export default function App() {
  const [theme, setTheme] = useState("clair");

  return (
    <ThemeContext.Provider value={theme}>
      <button onClick={() => setTheme((t) => (t === "clair" ? "sombre" : "clair"))}>Changer de thème</button>
      <Page />
    </ThemeContext.Provider>
  );
}
```

### 3. Lire la valeur avec `useContext`

N'importe quel descendant lit la valeur, sans prop :

```jsx
import { useContext } from "react";
import { ThemeContext } from "./ThemeContext.js";

export default function Bouton({ children }) {
  const theme = useContext(ThemeContext);
  return <button className={`bouton bouton-${theme}`}>{children}</button>;
}
```

Quand la `value` du fournisseur change, **tous les composants qui lisent ce contexte** sont affichés à nouveau avec la nouvelle valeur. Un composant lit la valeur du fournisseur **le plus proche** au-dessus de lui : on peut donc imbriquer plusieurs fournisseurs du même contexte pour remplacer la valeur dans une partie de l'arbre.

## Partager une valeur et une fonction

Pour que les descendants puissent aussi **modifier** la valeur, on fournit un objet contenant l'état et sa fonction de mise à jour. Une bonne pratique consiste à regrouper le fournisseur et un **hook d'accès** dans un même fichier :

```jsx
// src/auth.jsx
import { createContext, useContext, useState } from "react";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [utilisateur, setUtilisateur] = useState(null);

  function connecter(prenom) {
    setUtilisateur({ prenom });
  }

  function deconnecter() {
    setUtilisateur(null);
  }

  return (
    <AuthContext.Provider value={{ utilisateur, connecter, deconnecter }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const valeur = useContext(AuthContext);
  if (valeur === null) {
    throw new Error("useAuth doit être utilisé à l'intérieur de <AuthProvider>.");
  }
  return valeur;
}
```

```jsx
// src/App.jsx
import { AuthProvider, useAuth } from "./auth.jsx";

function BarreCompte() {
  const { utilisateur, connecter, deconnecter } = useAuth();

  if (!utilisateur) {
    return <button onClick={() => connecter("Sofia")}>Se connecter</button>;
  }
  return (
    <p>
      Bonjour {utilisateur.prenom} <button onClick={deconnecter}>Se déconnecter</button>
    </p>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <header>
        <BarreCompte />
      </header>
    </AuthProvider>
  );
}
```

- `useAuth` est un **hook personnalisé** (module 5) : il cache le détail du contexte et produit une erreur claire si l'on oublie le fournisseur ;
- les composants n'importent que `useAuth`, jamais `AuthContext` directement.

> Cet exemple simule une connexion pour illustrer le contexte. Une vraie authentification passe par un serveur ; on ne stocke jamais de mot de passe dans l'état ni dans le navigateur.

## Contexte et réducteur

Le contexte se combine très bien avec `useReducer` : le fournisseur détient l'état et `dispatch`, et n'importe quel composant peut lire l'état ou envoyer une action. C'est une manière simple de gérer l'**état global** d'une application de taille moyenne (panier, préférences), sans bibliothèque supplémentaire.

```jsx
import { createContext, useContext, useReducer } from "react";

const PanierContext = createContext(null);

function panierReducer(etat, action) {
  switch (action.type) {
    case "ajouter":
      return [...etat, action.article];
    case "vider":
      return [];
    default:
      throw new Error(`Action inconnue : ${action.type}`);
  }
}

export function PanierProvider({ children }) {
  const [articles, dispatch] = useReducer(panierReducer, []);
  return <PanierContext.Provider value={{ articles, dispatch }}>{children}</PanierContext.Provider>;
}

export function usePanier() {
  const valeur = useContext(PanierContext);
  if (valeur === null) throw new Error("usePanier doit être utilisé dans <PanierProvider>.");
  return valeur;
}
```

## Quand utiliser le contexte ?

Le contexte est pratique, mais il rend les dépendances entre composants **moins visibles** que les props. Avant d'y recourir :

1. **commencez par les props** : transmettre une donnée sur deux ou trois niveaux est normal et rend le flux explicite ;
2. **essayez la composition** (`children`) pour éviter de traverser des composants intermédiaires ;
3. utilisez le contexte pour les données **réellement transversales** : thème, langue, utilisateur, panier.

> Tous les composants qui lisent un contexte sont affichés à nouveau quand sa valeur change. Pour des données qui changent très souvent (position de la souris, saisie à chaque frappe), préférez un état local, ou découpez en plusieurs contextes plus petits.

## À retenir

- Le contexte transmet une valeur à tous les descendants sans passer par les props.
- `createContext(defaut)` → `<MonContexte.Provider value={…}>` → `useContext(MonContexte)`.
- Un composant lit le fournisseur **le plus proche** ; la valeur par défaut ne sert qu'en l'absence de fournisseur.
- Bonne pratique : un fichier qui exporte le fournisseur et un hook `useX()` vérifiant sa présence.
- Props d'abord, composition ensuite, contexte pour les données vraiment transversales.

## Exercices

### Exercice 1 — Contexte de langue

Créez un contexte `LangueContext` (valeur par défaut `"fr"`), un composant `App` qui fournit la langue choisie par un bouton bascule `fr` / `en`, et un composant `Salut` qui affiche `Bonjour` ou `Hello` selon la langue.

```solution-jsx
import { createContext, useContext, useState } from "react";

const LangueContext = createContext("fr");

function Salut() {
  const langue = useContext(LangueContext);
  return <p>{langue === "fr" ? "Bonjour" : "Hello"}</p>;
}

export default function App() {
  const [langue, setLangue] = useState("fr");
  return (
    <LangueContext.Provider value={langue}>
      <button onClick={() => setLangue((l) => (l === "fr" ? "en" : "fr"))}>{langue === "fr" ? "English" : "Français"}</button>
      <Salut />
    </LangueContext.Provider>
  );
}
```

### Exercice 2 — Quelle valeur ?

Avec `const Ctx = createContext("A")`, qu'affichent les trois composants `<Lecteur />` de cet arbre, `Lecteur` affichant `useContext(Ctx)` ?

```jsx
<>
  <Lecteur />
  <Ctx.Provider value="B">
    <Lecteur />
    <Ctx.Provider value="C">
      <Lecteur />
    </Ctx.Provider>
  </Ctx.Provider>
</>
```

```solution-text
A, B, C.
Le premier Lecteur n'a aucun fournisseur au-dessus de lui : il reçoit la valeur par défaut "A".
Le deuxième lit le fournisseur le plus proche ("B"), le troisième le fournisseur imbriqué ("C").
```

### Exercice 3 — Utiliser le panier partagé

À l'aide de `PanierProvider` et `usePanier` présentés dans la leçon, écrivez un composant `CompteurPanier` qui affiche `Panier (n)` et un composant `BoutonVider` qui vide le panier.

```solution-jsx
import { usePanier } from "./panier.jsx";

export function CompteurPanier() {
  const { articles } = usePanier();
  return <span>Panier ({articles.length})</span>;
}

export function BoutonVider() {
  const { articles, dispatch } = usePanier();
  return (
    <button disabled={articles.length === 0} onClick={() => dispatch({ type: "vider" })}>
      Vider
    </button>
  );
}
```
"""

# ---------------------------------------------------------------------------
# Module 5 — Données distantes et hooks personnalisés
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Rappel : `fetch` et `async`/`await`

Dans la formation JavaScript, vous avez récupéré des données avec `fetch`. Retenez trois points essentiels :

- `fetch(url)` renvoie une **promesse** de réponse HTTP ;
- `fetch` ne rejette sa promesse qu'en cas d'**échec réseau** : une réponse 404 ou 500 arrive normalement, il faut tester **`reponse.ok`** ;
- `await reponse.json()` convertit le corps de la réponse en objet JavaScript.

Regroupons ces règles dans une fonction utilitaire. Pour pouvoir l'exécuter sans réseau, elle reçoit la fonction `fetch` en paramètre : on lui passe ici une **fausse** implémentation qui imite les réponses d'un serveur.

```js
async function chargerJson(url, fetchFn = fetch) {
  const reponse = await fetchFn(url);
  if (!reponse.ok) {
    throw new Error(`Erreur HTTP ${reponse.status}`);
  }
  return reponse.json();
}

// Faux serveur, pour l'exemple
async function fauxFetch(url) {
  if (url === "/api/utilisateurs") {
    return { ok: true, status: 200, json: async () => [{ id: 1, nom: "Amina" }] };
  }
  return { ok: false, status: 404, json: async () => ({}) };
}

console.log(await chargerJson("/api/utilisateurs", fauxFetch));
try {
  await chargerJson("/api/inconnu", fauxFetch);
} catch (erreur) {
  console.log(erreur.message);
}
```

```text
[ { id: 1, nom: 'Amina' } ]
Erreur HTTP 404
```

> Dans un navigateur, vous appellerez simplement `chargerJson(url)`, qui utilisera le vrai `fetch`.

## Charger des données au montage d'un composant

Charger des données, c'est se **synchroniser** avec un serveur : c'est donc un **effet**. Un affichage de données distantes comporte toujours **trois situations** à prévoir :

| Situation | Ce que voit l'utilisateur |
|---|---|
| chargement en cours | un indicateur (« Chargement… ») |
| erreur | un message compréhensible, éventuellement un bouton « Réessayer » |
| succès | les données (ou un message si la liste est vide) |

```jsx
import { useEffect, useState } from "react";

export default function ListeUtilisateurs() {
  const [utilisateurs, setUtilisateurs] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const controleur = new AbortController();

    async function charger() {
      try {
        const reponse = await fetch("https://jsonplaceholder.typicode.com/users", {
          signal: controleur.signal,
        });
        if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
        setUtilisateurs(await reponse.json());
      } catch (e) {
        if (e.name !== "AbortError") setErreur(e.message);
      } finally {
        if (!controleur.signal.aborted) setChargement(false);
      }
    }

    charger();
    return () => controleur.abort();
  }, []);

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p role="alert">Impossible de charger les utilisateurs : {erreur}</p>;

  return (
    <ul>
      {utilisateurs.map((u) => (
        <li key={u.id}>
          {u.name} — {u.email}
        </li>
      ))}
    </ul>
  );
}
```

`https://jsonplaceholder.typicode.com` est un service public gratuit qui renvoie des données **fictives**, très utilisé pour s'entraîner. Les noms des propriétés (`name`, `email`) sont ceux de cette API.

Points importants :

- la fonction passée à `useEffect` ne peut **pas** être `async` (elle doit renvoyer rien ou une fonction de nettoyage, pas une promesse) : on déclare une fonction `async` **à l'intérieur** et on l'appelle ;
- `try` / `catch` / `finally` traite les trois situations ;
- la clé de chaque `<li>` est l'identifiant fourni par l'API.

## Annuler une requête : `AbortController`

Que se passe-t-il si le composant disparaît (l'utilisateur change de page) avant la réponse ? Ou si une requête plus ancienne arrive **après** une plus récente ? Sans précaution, on risque d'afficher des données **périmées**.

`AbortController` permet d'**annuler** une requête : on transmet son `signal` à `fetch`, et l'appel à `controleur.abort()` interrompt la requête, dont la promesse est alors rejetée avec une erreur nommée `"AbortError"`. On l'appelle dans la **fonction de nettoyage** de l'effet ; l'erreur d'annulation est ignorée dans le `catch`, car ce n'est pas une vraie erreur.

## Recharger quand un paramètre change

Quand la requête dépend d'une prop ou d'un état, ce paramètre devient une **dépendance** de l'effet. À chaque changement, React nettoie l'effet précédent (annulant la requête en cours) puis en lance un nouveau : c'est exactement ce qui évite les réponses qui arrivent dans le désordre.

```jsx
import { useEffect, useState } from "react";

export default function DetailUtilisateur({ id }) {
  const [utilisateur, setUtilisateur] = useState(null);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const controleur = new AbortController();
    setUtilisateur(null);
    setErreur(null);

    fetch(`https://jsonplaceholder.typicode.com/users/${id}`, { signal: controleur.signal })
      .then((reponse) => {
        if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
        return reponse.json();
      })
      .then(setUtilisateur)
      .catch((e) => {
        if (e.name !== "AbortError") setErreur(e.message);
      });

    return () => controleur.abort();
  }, [id]);

  if (erreur) return <p role="alert">{erreur}</p>;
  if (!utilisateur) return <p>Chargement…</p>;
  return (
    <article>
      <h2>{utilisateur.name}</h2>
      <p>{utilisateur.address.city}</p>
    </article>
  );
}
```

## Les requêtes déclenchées par l'utilisateur

Toutes les requêtes ne vont pas dans un effet. Un **envoi** de données (création, modification, suppression) répond à une **action** de l'utilisateur : il se place dans le **gestionnaire d'événement**.

```jsx
import { useState } from "react";

export default function NouveauMessage() {
  const [texte, setTexte] = useState("");
  const [statut, setStatut] = useState("repos"); // repos | envoi | envoye | erreur

  async function gererEnvoi(e) {
    e.preventDefault();
    setStatut("envoi");
    try {
      const reponse = await fetch("https://jsonplaceholder.typicode.com/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: "Message", body: texte, userId: 1 }),
      });
      if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
      setTexte("");
      setStatut("envoye");
    } catch {
      setStatut("erreur");
    }
  }

  return (
    <form onSubmit={gererEnvoi}>
      <textarea value={texte} onChange={(e) => setTexte(e.target.value)} />
      <button type="submit" disabled={statut === "envoi" || texte.trim() === ""}>
        {statut === "envoi" ? "Envoi…" : "Envoyer"}
      </button>
      {statut === "envoye" && <p role="status">Message envoyé.</p>}
      {statut === "erreur" && <p role="alert">L'envoi a échoué, réessayez.</p>}
    </form>
  );
}
```

Désactiver le bouton pendant l'envoi évite les **doubles envois**. (JSONPlaceholder simule l'enregistrement : la donnée n'est pas réellement conservée.)

## Sécurité et bonnes pratiques

- Tout le code React est **envoyé au navigateur** : n'y placez **jamais** de clé secrète ou de mot de passe. Avec Vite, seules les variables d'environnement préfixées par `VITE_` sont exposées au code (`import.meta.env.VITE_API_URL`) — et elles deviennent alors **publiques**.
- Les appels nécessitant un secret passent par **votre serveur**, qui seul détient la clé.
- Des bibliothèques spécialisées (par exemple TanStack Query ou SWR) ajoutent mise en cache et nouvelles tentatives ; les principes restent les mêmes.

## À retenir

- Charger des données au montage = un effet ; un envoi déclenché par l'utilisateur = un gestionnaire d'événement.
- Trois situations à afficher : chargement, erreur, succès (et liste vide).
- Tester `reponse.ok` : `fetch` ne rejette pas sur une erreur HTTP.
- Fonction `async` déclarée **dans** l'effet ; `AbortController` + `abort()` dans le nettoyage.
- Pas de secret dans le code front : les appels nécessitant une clé passent par votre serveur.

## Exercices

### Exercice 1 — Liste d'articles

Écrivez un composant `Articles` qui charge `https://jsonplaceholder.typicode.com/posts?_limit=5` et affiche les titres (`title`), avec les états de chargement et d'erreur, et l'annulation au démontage.

```solution-jsx
import { useEffect, useState } from "react";

export default function Articles() {
  const [articles, setArticles] = useState([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState(null);

  useEffect(() => {
    const controleur = new AbortController();
    fetch("https://jsonplaceholder.typicode.com/posts?_limit=5", { signal: controleur.signal })
      .then((r) => {
        if (!r.ok) throw new Error(`Erreur HTTP ${r.status}`);
        return r.json();
      })
      .then((donnees) => {
        setArticles(donnees);
        setChargement(false);
      })
      .catch((e) => {
        if (e.name === "AbortError") return;
        setErreur(e.message);
        setChargement(false);
      });
    return () => controleur.abort();
  }, []);

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p role="alert">{erreur}</p>;
  return (
    <ol>
      {articles.map((a) => (
        <li key={a.id}>{a.title}</li>
      ))}
    </ol>
  );
}
```

### Exercice 2 — Plusieurs requêtes en parallèle

Écrivez une fonction `chargerTout(urls, fetchFn)` qui charge plusieurs URL **en parallèle** avec `Promise.all` et renvoie le tableau des résultats. Testez-la avec un faux `fetch`.

```solution-js
async function chargerJson(url, fetchFn) {
  const reponse = await fetchFn(url);
  if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
  return reponse.json();
}

async function chargerTout(urls, fetchFn) {
  return Promise.all(urls.map((url) => chargerJson(url, fetchFn)));
}

async function fauxFetch(url) {
  const donnees = { "/api/a": { nom: "A" }, "/api/b": { nom: "B" } };
  return { ok: url in donnees, status: url in donnees ? 200 : 404, json: async () => donnees[url] };
}

console.log(await chargerTout(["/api/a", "/api/b"], fauxFetch));
try {
  await chargerTout(["/api/a", "/api/z"], fauxFetch);
} catch (e) {
  console.log(e.message);
}
```

```text
[ { nom: 'A' }, { nom: 'B' } ]
Erreur HTTP 404
```

`Promise.all` échoue dès qu'une seule requête échoue.

### Exercice 3 — Trouvez les erreurs

Ce code contient trois problèmes. Lesquels ?

```jsx
useEffect(async () => {
  const reponse = await fetch(`/api/produits/${id}`);
  setProduit(await reponse.json());
}, []);
```

```solution-text
1. La fonction de l'effet est async : elle renvoie une promesse au lieu de rien ou d'une fonction
   de nettoyage. Il faut déclarer une fonction async à l'intérieur de l'effet et l'appeler.
2. id est utilisé mais absent des dépendances : le produit ne sera pas rechargé quand id change.
   Il faut écrire [id].
3. Aucun contrôle de reponse.ok ni gestion d'erreur, et pas d'annulation : une ancienne réponse
   peut écraser la nouvelle. Ajouter try/catch, un AbortController et controleur.abort() dans le nettoyage.
```
"""

M5_L2 = r"""
## Pourquoi créer ses propres hooks ?

En écrivant les leçons précédentes, vous avez sans doute remarqué des **répétitions** : chaque chargement de données réclame trois états, un effet et un `AbortController` ; chaque bascule un `useState(false)` et une fonction d'inversion. Un **hook personnalisé** (*custom hook*) permet de **factoriser cette logique avec état** dans une fonction réutilisable.

Un hook personnalisé est simplement une fonction :

- dont le nom **commence par `use`** suivi d'une majuscule (`useBascule`, `useFetch`) — c'est ce qui permet à React et à ESLint d'appliquer les règles des hooks ;
- qui **appelle d'autres hooks** (`useState`, `useEffect`, `useContext`…) ;
- qui renvoie ce dont le composant a besoin (une valeur, un tableau, un objet).

## Un premier hook : `useBascule`

```jsx
import { useState } from "react";

export function useBascule(initial = false) {
  const [actif, setActif] = useState(initial);
  const basculer = () => setActif((a) => !a);
  return [actif, basculer];
}
```

```jsx
import { useBascule } from "./useBascule.js";

export default function Menu() {
  const [ouvert, basculerMenu] = useBascule();
  const [sombre, basculerTheme] = useBascule(true);

  return (
    <nav className={sombre ? "sombre" : "clair"}>
      <button onClick={basculerMenu} aria-expanded={ouvert}>
        Menu
      </button>
      <button onClick={basculerTheme}>Thème</button>
      {ouvert && (
        <ul>
          <li>Accueil</li>
          <li>Formations</li>
        </ul>
      )}
    </nav>
  );
}
```

Point essentiel : **chaque appel** d'un hook personnalisé crée un état **indépendant**. Les hooks partagent de la **logique**, pas des données : ici `ouvert` et `sombre` n'ont rien en commun. Pour partager des données entre composants, on remonte l'état ou on utilise un contexte.

## `useLocalStorage` : un état qui survit au rechargement

`localStorage` conserve du **texte** dans le navigateur, propre au site. Le hook suivant se comporte comme `useState`, mais enregistre chaque changement.

La partie délicate — lire une valeur éventuellement absente ou corrompue — s'isole dans une **fonction pure**, testable sans navigateur :

```js
function lireJson(texte, valeurParDefaut) {
  if (texte === null) return valeurParDefaut;
  try {
    return JSON.parse(texte);
  } catch {
    return valeurParDefaut;
  }
}

console.log(lireJson(null, []));
console.log(lireJson('["react","vite"]', []));
console.log(lireJson("{pas du json", { theme: "clair" }));
```

```text
[]
[ 'react', 'vite' ]
{ theme: 'clair' }
```

```jsx
import { useEffect, useState } from "react";

function lireJson(texte, valeurParDefaut) {
  if (texte === null) return valeurParDefaut;
  try {
    return JSON.parse(texte);
  } catch {
    return valeurParDefaut;
  }
}

export function useLocalStorage(cle, valeurInitiale) {
  const [valeur, setValeur] = useState(() => lireJson(localStorage.getItem(cle), valeurInitiale));

  useEffect(() => {
    localStorage.setItem(cle, JSON.stringify(valeur));
  }, [cle, valeur]);

  return [valeur, setValeur];
}
```

- l'**initialisation paresseuse** `useState(() => …)` ne lit le stockage qu'au premier rendu ;
- l'**effet** synchronise le stockage (système extérieur) avec l'état ;
- le hook renvoie la même paire que `useState` : il s'utilise de la même façon.

```jsx
import { useLocalStorage } from "./useLocalStorage.js";

export default function Bloc() {
  const [note, setNote] = useLocalStorage("note-du-jour", "");
  return <textarea value={note} onChange={(e) => setNote(e.target.value)} placeholder="Votre note…" />;
}
```

> `localStorage` est lisible par tout script exécuté sur la page : n'y stockez jamais de mot de passe ni de jeton sensible. Il convient pour des préférences ou des brouillons.

## `useFetch` : charger des données en une ligne

Le modèle de chargement de la leçon précédente devient un hook réutilisable :

```jsx
import { useEffect, useState } from "react";

export function useFetch(url) {
  const [etat, setEtat] = useState({ donnees: null, chargement: true, erreur: null });

  useEffect(() => {
    const controleur = new AbortController();
    setEtat({ donnees: null, chargement: true, erreur: null });

    async function charger() {
      try {
        const reponse = await fetch(url, { signal: controleur.signal });
        if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
        const donnees = await reponse.json();
        setEtat({ donnees, chargement: false, erreur: null });
      } catch (e) {
        if (e.name !== "AbortError") {
          setEtat({ donnees: null, chargement: false, erreur: e.message });
        }
      }
    }

    charger();
    return () => controleur.abort();
  }, [url]);

  return etat;
}
```

```jsx
import { useFetch } from "./useFetch.js";

export default function Albums() {
  const { donnees, chargement, erreur } = useFetch("https://jsonplaceholder.typicode.com/albums?_limit=5");

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p role="alert">{erreur}</p>;
  return (
    <ul>
      {donnees.map((a) => (
        <li key={a.id}>{a.title}</li>
      ))}
    </ul>
  );
}
```

Un seul objet d'état garantit que `donnees`, `chargement` et `erreur` restent **cohérents** entre eux (impossible d'être à la fois en chargement et en erreur). Comme `url` est une dépendance, changer l'URL relance le chargement et annule la requête précédente.

## `useDebounce` : attendre la fin de la frappe

Lancer une requête à **chaque** frappe dans un champ de recherche est inutile et coûteux. Le **debounce** (anti-rebond) consiste à attendre que la valeur soit restée **stable** pendant un délai avant de l'utiliser :

```jsx
import { useEffect, useState } from "react";

export function useDebounce(valeur, delai = 300) {
  const [valeurStable, setValeurStable] = useState(valeur);

  useEffect(() => {
    const id = setTimeout(() => setValeurStable(valeur), delai);
    return () => clearTimeout(id); // une nouvelle frappe annule le minuteur précédent
  }, [valeur, delai]);

  return valeurStable;
}
```

À chaque changement de `valeur`, le nettoyage annule le minuteur précédent : seule la **dernière** valeur, restée inchangée pendant `delai` millisecondes, est retenue. Le même principe en JavaScript pur, avec une simulation :

```js
function creerDebounce(fn, delai) {
  let id = null;
  return (...args) => {
    clearTimeout(id);
    id = setTimeout(() => fn(...args), delai);
  };
}

const rechercher = creerDebounce((texte) => console.log(`Recherche : ${texte}`), 50);
rechercher("r");
rechercher("re");
rechercher("rea");
setTimeout(() => rechercher("react"), 100);
```

```text
Recherche : rea
Recherche : react
```

Les trois premiers appels, rapprochés, ne produisent qu'une recherche ; l'appel isolé en produit une seconde.

## Bonnes pratiques

- Un hook personnalisé porte un nom qui dit **à quoi il sert** (`useEnLigne`, `useFetch`), pas comment il fonctionne.
- Les **règles des hooks** s'appliquent à l'intérieur comme à l'extérieur : appels au premier niveau, jamais dans une condition.
- Isolez la logique sans React (analyse, calcul, validation) dans des **fonctions pures** : elles se testent facilement.
- N'en créez pas pour une seule ligne de code : un hook est utile quand il encapsule une logique **avec état ou effet** réutilisée.

## À retenir

- Un hook personnalisé est une fonction `useXxx` qui appelle d'autres hooks.
- Chaque appel crée un état indépendant : on partage de la logique, pas des données.
- `useLocalStorage` : initialisation paresseuse + effet de synchronisation.
- `useFetch(url)` : chargement, erreur, données dans un seul état ; annulation au nettoyage.
- `useDebounce` : un minuteur annulé à chaque changement ne retient que la dernière valeur stable.

## Exercices

### Exercice 1 — `useCompteur`

Écrivez un hook `useCompteur(initial = 0, pas = 1)` qui renvoie `{ valeur, incrementer, decrementer, reinitialiser }`, puis un composant qui l'utilise avec un pas de 5.

```solution-jsx
import { useState } from "react";

export function useCompteur(initial = 0, pas = 1) {
  const [valeur, setValeur] = useState(initial);
  return {
    valeur,
    incrementer: () => setValeur((v) => v + pas),
    decrementer: () => setValeur((v) => v - pas),
    reinitialiser: () => setValeur(initial),
  };
}

export default function Score() {
  const { valeur, incrementer, decrementer, reinitialiser } = useCompteur(0, 5);
  return (
    <div>
      <p>Score : {valeur}</p>
      <button onClick={decrementer}>-5</button>
      <button onClick={incrementer}>+5</button>
      <button onClick={reinitialiser}>Remettre à zéro</button>
    </div>
  );
}
```

### Exercice 2 — `useEnLigne`

Écrivez un hook `useEnLigne()` qui renvoie `true` si le navigateur est connecté, en s'appuyant sur `navigator.onLine` et sur les événements `online` et `offline` de `window`.

```solution-jsx
import { useEffect, useState } from "react";

export function useEnLigne() {
  const [enLigne, setEnLigne] = useState(navigator.onLine);

  useEffect(() => {
    const surOnline = () => setEnLigne(true);
    const surOffline = () => setEnLigne(false);
    window.addEventListener("online", surOnline);
    window.addEventListener("offline", surOffline);
    return () => {
      window.removeEventListener("online", surOnline);
      window.removeEventListener("offline", surOffline);
    };
  }, []);

  return enLigne;
}

export default function Bandeau() {
  const enLigne = useEnLigne();
  return enLigne ? null : <p role="status">Vous êtes hors ligne.</p>;
}
```

### Exercice 3 — Valeur avec repli

Écrivez une fonction pure `lirePreferences(texte)` qui fusionne les préférences enregistrées (JSON) avec des valeurs par défaut `{ theme: "clair", taille: 16 }` ; un texte absent ou invalide donne les valeurs par défaut.

```solution-js
const DEFAUT = { theme: "clair", taille: 16 };

function lirePreferences(texte) {
  if (texte === null) return { ...DEFAUT };
  try {
    return { ...DEFAUT, ...JSON.parse(texte) };
  } catch {
    return { ...DEFAUT };
  }
}

console.log(lirePreferences('{"theme":"sombre"}'));
console.log(lirePreferences("oups"));
console.log(lirePreferences(null));
```

```text
{ theme: 'sombre', taille: 16 }
{ theme: 'clair', taille: 16 }
{ theme: 'clair', taille: 16 }
```
"""

M5_L3 = r"""
## Le projet

Vous allez construire un **annuaire filtrable** qui mobilise toute la formation :

- charger une liste de personnes depuis une API avec `fetch` (chargement, erreur, nouvelle tentative) ;
- filtrer par texte (nom, email, entreprise) et par ville, sans tenir compte des accents ni des majuscules ;
- trier par nom ou par ville ;
- marquer des **favoris**, conservés après un rechargement de la page ;
- afficher le nombre de résultats et un message quand aucun ne correspond.

L'API utilisée est `https://jsonplaceholder.typicode.com/users`, qui renvoie dix utilisateurs **fictifs**. Chaque utilisateur possède notamment `id`, `name`, `email`, `address.city` et `company.name`.

Architecture visée :

```text
src/
├── App.jsx                     état des filtres, assemblage
├── filtres.js                  fonctions pures : normaliser, filtrer, trier, villes
├── hooks/
│   ├── useFetch.js             chargement des données (module 5)
│   └── useLocalStorage.js      favoris persistants (module 5)
└── components/
    ├── BarreFiltres.jsx        champs contrôlés
    ├── ListePersonnes.jsx      liste + état vide
    └── CartePersonne.jsx       une personne + bouton favori
```

## Étape 1 — Créer le projet

```bash
npm create vite@latest annuaire -- --template react
cd annuaire
npm install
npm run dev
```

Videz `src/App.jsx` et `src/App.css`, puis créez les dossiers `hooks` et `components`.

## Étape 2 — La logique pure (`src/filtres.js`)

Toute la logique de filtrage est écrite **sans React**, sous forme de fonctions pures. Testons-la avec des données d'exemple de même forme que celles de l'API :

```js
export function normaliser(texte) {
  return texte.normalize("NFD").replace(/[̀-ͯ]/g, "").toLowerCase().trim();
}

export function filtrerPersonnes(personnes, { texte = "", ville = "", favorisSeuls = false }, favoris = []) {
  const recherche = normaliser(texte);
  return personnes.filter((p) => {
    const cible = normaliser(`${p.name} ${p.email} ${p.company.name}`);
    if (recherche && !cible.includes(recherche)) return false;
    if (ville && p.address.city !== ville) return false;
    if (favorisSeuls && !favoris.includes(p.id)) return false;
    return true;
  });
}

export function trierPersonnes(personnes, critere) {
  const cle = critere === "ville" ? (p) => p.address.city : (p) => p.name;
  return personnes.toSorted((a, b) => cle(a).localeCompare(cle(b), "fr"));
}

export function listeVilles(personnes) {
  return [...new Set(personnes.map((p) => p.address.city))].sort((a, b) => a.localeCompare(b, "fr"));
}

// Tests avec des données fictives
const personnes = [
  { id: 1, name: "Élodie Martin", email: "elodie@exemple.fr", address: { city: "Nantes" }, company: { name: "Atelier Bleu" } },
  { id: 2, name: "Karim Haddad", email: "karim@exemple.fr", address: { city: "Lyon" }, company: { name: "Studio Nord" } },
  { id: 3, name: "Sofia Rossi", email: "sofia@exemple.fr", address: { city: "Nantes" }, company: { name: "Studio Sud" } },
  { id: 4, name: "Amina Diallo", email: "amina@exemple.fr", address: { city: "Brest" }, company: { name: "Atelier Vert" } },
];

const noms = (liste) => liste.map((p) => p.name);
console.log(normaliser("  Élodie "));
console.log(noms(filtrerPersonnes(personnes, { texte: "elodie" })));
console.log(noms(filtrerPersonnes(personnes, { texte: "studio" })));
console.log(noms(filtrerPersonnes(personnes, { ville: "Nantes" })));
console.log(noms(filtrerPersonnes(personnes, { favorisSeuls: true }, [2, 4])));
console.log(noms(trierPersonnes(personnes, "nom")));
console.log(noms(trierPersonnes(personnes, "ville")));
console.log(listeVilles(personnes));
```

```text
elodie
[ 'Élodie Martin' ]
[ 'Karim Haddad', 'Sofia Rossi' ]
[ 'Élodie Martin', 'Sofia Rossi' ]
[ 'Karim Haddad', 'Amina Diallo' ]
[ 'Amina Diallo', 'Élodie Martin', 'Karim Haddad', 'Sofia Rossi' ]
[ 'Amina Diallo', 'Karim Haddad', 'Élodie Martin', 'Sofia Rossi' ]
[ 'Brest', 'Lyon', 'Nantes' ]
```

Quelques remarques :

- `normalize("NFD")` sépare chaque lettre accentuée en lettre + accent ; l'expression régulière supprime ensuite les accents : « Élodie » devient « elodie » ;
- `localeCompare(…, "fr")` trie selon l'ordre alphabétique français (« É » est rangé avec les « E ») ;
- `toSorted` ne modifie pas le tableau reçu ; `new Set` supprime les doublons de villes ;
- le tri par ville conserve l'ordre d'origine des personnes d'une même ville (Élodie avant Sofia).

Dans le projet, supprimez la partie « Tests » du fichier, ou déplacez-la dans un fichier de test séparé.

## Étape 3 — Les hooks

Reprenez **tels quels** `useFetch` et `useLocalStorage` de la leçon précédente, dans `src/hooks/useFetch.js` et `src/hooks/useLocalStorage.js` (chacun avec ses imports depuis `react`). Ils fournissent respectivement `{ donnees, chargement, erreur }` et une paire `[valeur, setValeur]` persistante.

Pour permettre un bouton « Réessayer », ajoutons à `useFetch` un compteur de tentatives, qui fait partie des dépendances de l'effet :

```jsx
import { useEffect, useState } from "react";

export function useFetch(url) {
  const [etat, setEtat] = useState({ donnees: null, chargement: true, erreur: null });
  const [tentative, setTentative] = useState(0);

  useEffect(() => {
    const controleur = new AbortController();
    setEtat({ donnees: null, chargement: true, erreur: null });

    async function charger() {
      try {
        const reponse = await fetch(url, { signal: controleur.signal });
        if (!reponse.ok) throw new Error(`Erreur HTTP ${reponse.status}`);
        const donnees = await reponse.json();
        setEtat({ donnees, chargement: false, erreur: null });
      } catch (e) {
        if (e.name !== "AbortError") {
          setEtat({ donnees: null, chargement: false, erreur: e.message });
        }
      }
    }

    charger();
    return () => controleur.abort();
  }, [url, tentative]);

  const reessayer = () => setTentative((t) => t + 1);
  return { ...etat, reessayer };
}
```

## Étape 4 — Les composants d'affichage

`src/components/BarreFiltres.jsx` : des champs **contrôlés par le parent**. Le composant ne possède aucun état ; il reçoit les filtres et une fonction `onChange` qui renvoie un objet de filtres mis à jour.

```jsx
export default function BarreFiltres({ filtres, villes, onChange }) {
  function modifier(e) {
    const { name, value, type, checked } = e.target;
    onChange({ ...filtres, [name]: type === "checkbox" ? checked : value });
  }

  return (
    <form className="filtres" role="search" onSubmit={(e) => e.preventDefault()}>
      <label>
        Recherche
        <input type="search" name="texte" value={filtres.texte} onChange={modifier} placeholder="Nom, email, entreprise…" />
      </label>

      <label>
        Ville
        <select name="ville" value={filtres.ville} onChange={modifier}>
          <option value="">Toutes</option>
          {villes.map((v) => (
            <option key={v} value={v}>
              {v}
            </option>
          ))}
        </select>
      </label>

      <label>
        Tri
        <select name="tri" value={filtres.tri} onChange={modifier}>
          <option value="nom">Nom</option>
          <option value="ville">Ville</option>
        </select>
      </label>

      <label>
        <input type="checkbox" name="favorisSeuls" checked={filtres.favorisSeuls} onChange={modifier} />
        Favoris uniquement
      </label>
    </form>
  );
}
```

`src/components/CartePersonne.jsx` :

```jsx
export default function CartePersonne({ personne, favori, onBasculerFavori }) {
  return (
    <li className="carte">
      <div>
        <h2>{personne.name}</h2>
        <p>
          {personne.company.name} — {personne.address.city}
        </p>
        <a href={`mailto:${personne.email}`}>{personne.email}</a>
      </div>
      <button
        onClick={() => onBasculerFavori(personne.id)}
        aria-pressed={favori}
        aria-label={favori ? `Retirer ${personne.name} des favoris` : `Ajouter ${personne.name} aux favoris`}
      >
        {favori ? "★" : "☆"}
      </button>
    </li>
  );
}
```

`src/components/ListePersonnes.jsx` : la liste, avec sa **clé** (l'identifiant de l'API) et son **état vide** :

```jsx
import CartePersonne from "./CartePersonne.jsx";

export default function ListePersonnes({ personnes, favoris, onBasculerFavori }) {
  if (personnes.length === 0) {
    return <p className="vide">Aucune personne ne correspond à ces critères.</p>;
  }
  return (
    <ul className="liste">
      {personnes.map((p) => (
        <CartePersonne key={p.id} personne={p} favori={favoris.includes(p.id)} onBasculerFavori={onBasculerFavori} />
      ))}
    </ul>
  );
}
```

## Étape 5 — L'assemblage (`src/App.jsx`)

`App` détient l'état des filtres et des favoris ; tout le reste est **dérivé** pendant le rendu.

```jsx
import { useState } from "react";
import { useFetch } from "./hooks/useFetch.js";
import { useLocalStorage } from "./hooks/useLocalStorage.js";
import { filtrerPersonnes, listeVilles, trierPersonnes } from "./filtres.js";
import BarreFiltres from "./components/BarreFiltres.jsx";
import ListePersonnes from "./components/ListePersonnes.jsx";
import "./App.css";

const URL_API = "https://jsonplaceholder.typicode.com/users";
const FILTRES_INITIAUX = { texte: "", ville: "", tri: "nom", favorisSeuls: false };

export default function App() {
  const { donnees, chargement, erreur, reessayer } = useFetch(URL_API);
  const [filtres, setFiltres] = useState(FILTRES_INITIAUX);
  const [favoris, setFavoris] = useLocalStorage("annuaire-favoris", []);

  function basculerFavori(id) {
    setFavoris((liste) => (liste.includes(id) ? liste.filter((f) => f !== id) : [...liste, id]));
  }

  if (chargement) return <p className="info">Chargement de l'annuaire…</p>;
  if (erreur) {
    return (
      <div role="alert" className="info">
        <p>Impossible de charger l'annuaire ({erreur}).</p>
        <button onClick={reessayer}>Réessayer</button>
      </div>
    );
  }

  // Données dérivées : recalculées à chaque rendu, jamais stockées dans l'état
  const villes = listeVilles(donnees);
  const visibles = trierPersonnes(filtrerPersonnes(donnees, filtres, favoris), filtres.tri);

  return (
    <main className="annuaire">
      <h1>Annuaire</h1>
      <BarreFiltres filtres={filtres} villes={villes} onChange={setFiltres} />
      <p aria-live="polite">
        {visibles.length} résultat(s) sur {donnees.length} — {favoris.length} favori(s)
      </p>
      {(filtres.texte || filtres.ville || filtres.favorisSeuls) && (
        <button onClick={() => setFiltres(FILTRES_INITIAUX)}>Effacer les filtres</button>
      )}
      <ListePersonnes personnes={visibles} favoris={favoris} onBasculerFavori={basculerFavori} />
    </main>
  );
}
```

Vérifiez les règles des hooks : les trois hooks (`useFetch`, `useState`, `useLocalStorage`) sont appelés **avant** les `return` anticipés, toujours dans le même ordre.

## Étape 6 — Un peu de style (`src/App.css`)

```css
.annuaire { max-width: 48rem; margin: 2rem auto; padding: 0 1rem; font-family: system-ui, sans-serif; }
.filtres { display: flex; flex-wrap: wrap; gap: 1rem; align-items: end; margin-bottom: 1rem; }
.filtres label { display: flex; flex-direction: column; gap: .25rem; }
.liste { list-style: none; padding: 0; display: grid; gap: .75rem; }
.carte { display: flex; justify-content: space-between; align-items: start; padding: 1rem; border: 1px solid #ddd; border-radius: .75rem; }
.carte h2 { margin: 0 0 .25rem; font-size: 1.1rem; }
.carte button { font-size: 1.5rem; background: none; border: none; cursor: pointer; }
.vide, .info { color: #555; }
```

## Vérifier votre travail

Testez chaque point :

1. pendant le chargement, le message « Chargement de l'annuaire… » apparaît ;
2. en coupant le réseau (outils de développement, onglet *Réseau*, mode *Hors connexion*) puis en rechargeant, le message d'erreur et le bouton « Réessayer » s'affichent ;
3. la recherche ignore les accents et les majuscules ; le compteur de résultats se met à jour ;
4. un filtre sans résultat affiche le message d'état vide ;
5. les favoris restent marqués après un rechargement de la page ;
6. la console ne signale aucun avertissement de clé manquante.

## Pour aller plus loin

- Retarder la recherche avec le hook `useDebounce` : `const texteStable = useDebounce(filtres.texte, 300);`, puis filtrer avec `{ ...filtres, texte: texteStable }`.
- Afficher le détail d'une personne au clic, en mémorisant l'**identifiant** sélectionné dans l'état de `App`.
- Remplacer l'état des filtres par un `useReducer` (actions `modifier`, `effacer`).
- Construire la version de production avec `npm run build` et la déposer chez un hébergeur de sites statiques.

## À retenir

- La logique métier (filtrer, trier, normaliser) vit dans des **fonctions pures**, testées sans React.
- Les données distantes passent par un **hook** qui gère chargement, erreur, annulation et nouvelle tentative.
- Un état **minimal** (filtres, favoris) ; tout le reste (villes, liste visible, compteurs) est **dérivé**.
- Les composants d'affichage sont **contrôlés par le parent** et reçoivent des fonctions `onX`.
- Chaque élément de liste a une **clé stable** ; chaque liste prévoit son **état vide**.
"""

# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------
QUIZ_M3 = [
    ("single", "Qu'affiche ce composant quand nonLus vaut 0 ?", "return <div>{nonLus && <span>{nonLus} message(s)</span>}</div>;",
     ["Rien dans la div", "Une erreur", "« 0 message(s) »", "Le chiffre 0"], [3],
     "0 && … vaut 0, et React affiche les nombres : un « 0 » apparaît. Il faut écrire nonLus > 0 && …"),
    ("single", "Quel est le meilleur choix de clé pour une liste de produits venant d'une API ?", None,
     ["L'index du tableau", "Math.random()", "L'identifiant du produit fourni par l'API", "Le nom du composant"], [2],
     "Une clé doit être unique parmi les frères et stable dans le temps : l'identifiant issu des données remplit ces deux conditions."),
    ("single", "Où placer l'attribut key dans une liste ?", None,
     ["Sur l'élément renvoyé directement par map", "Sur la balise <ul>", "Sur le premier enfant de chaque élément", "Dans le composant enfant, via props.key"], [0],
     "La clé se place sur l'élément de plus haut niveau renvoyé par la fonction passée à map ; elle n'est pas transmise comme prop."),
    ("multiple", "Quelles affirmations sur les clés sont exactes ?", None,
     ["Elles doivent être uniques parmi les éléments frères.", "Elles doivent être uniques dans toute l'application.", "Une clé qui change à chaque rendu fait perdre l'état des éléments.", "L'index convient à une liste fixe, jamais triée ni filtrée."], [0, 2, 3],
     "L'unicité n'est exigée qu'entre frères. Une clé instable force React à recréer les éléments ; l'index n'est acceptable que pour une liste figée."),
    ("single", "Qu'est-ce qu'un champ contrôlé ?", None,
     ["Un champ validé par le serveur", "Un champ dont la valeur est stockée dans l'état et mise à jour par onChange", "Un champ en lecture seule", "Un champ avec l'attribut required"], [1],
     "Avec value={etat} et onChange, l'état React est l'unique source de vérité de la valeur affichée."),
    ("single", "Quelle propriété lire dans onChange pour une case à cocher ?", None,
     ["e.target.checked", "e.target.value", "e.checked", "e.target.selected"], [0],
     "Pour une case à cocher, l'état coché est un booléen disponible dans e.target.checked."),
    ("true_false", "La valeur lue dans un <input type=\"number\"> est un nombre.", None,
     ["Vrai", "Faux"], [1],
     "e.target.value est toujours une chaîne, même avec type=\"number\" : il faut la convertir avec Number() avant de calculer."),
    ("single", "Deux composants frères ont besoin du même texte de recherche. Que faire ?", None,
     ["Dupliquer l'état dans les deux composants", "Utiliser une variable globale", "Remonter l'état dans leur plus proche parent commun et le transmettre par les props", "Stocker le texte dans le DOM"], [2],
     "Remonter l'état dans le parent commun crée une source de vérité unique ; le parent transmet la valeur et une fonction de modification."),
    ("single", "Une liste filtrée se calcule à partir de l'état texte et des données. Où la placer ?", None,
     ["Dans un second useState mis à jour à chaque frappe", "Dans une ref", "Dans localStorage", "Dans une variable calculée pendant le rendu"], [3],
     "C'est une donnée dérivée : la calculer pendant le rendu évite les doublons et les désynchronisations."),
    ("single", "Que fait e.preventDefault() dans le gestionnaire onSubmit d'un formulaire ?", None,
     ["Il empêche l'envoi classique et le rechargement de la page", "Il vide les champs", "Il valide les champs", "Il désactive le bouton"], [0],
     "Le comportement par défaut d'un formulaire est d'envoyer les données et de recharger la page ; preventDefault laisse React traiter l'envoi."),
]

QUIZ_M4 = [
    ("single", "À quoi sert useEffect ?", None,
     ["À calculer des données dérivées", "À remplacer les props", "À créer un état", "À synchroniser le composant avec un système extérieur à React"], [3],
     "Un effet s'exécute après l'affichage pour se synchroniser avec l'extérieur : titre de la page, minuteur, abonnement, réseau."),
    ("single", "Quand s'exécute useEffect(fn, []) ?", None,
     ["Après chaque rendu", "Jamais", "Après le premier affichage seulement", "Avant le premier affichage"], [2],
     "Un tableau de dépendances vide signifie que l'effet ne dépend d'aucune valeur : il s'exécute après le premier affichage (en production)."),
    ("single", "Quand React appelle-t-il la fonction de nettoyage d'un effet ?", None,
     ["Avant de relancer l'effet et quand le composant est démonté", "Uniquement au premier affichage", "À chaque clic", "Jamais automatiquement"], [0],
     "Le nettoyage arrête ce que l'effet a démarré : avant une nouvelle exécution (dépendance modifiée) et au démontage."),
    ("single", "Que provoque ce code ?", "useEffect(() => {\n  setN(n + 1);\n});",
     ["Une seule mise à jour", "Une boucle infinie de rendus", "Une erreur de syntaxe", "Rien"], [1],
     "Sans tableau de dépendances, l'effet s'exécute après chaque rendu ; il modifie l'état, ce qui provoque un nouveau rendu, et ainsi de suite."),
    ("multiple", "Dans quels cas un effet est-il inutile ?", None,
     ["Calculer un total à partir de l'état", "Démarrer un setInterval", "Réagir au clic sur un bouton « Envoyer »", "Écouter l'événement resize de la fenêtre"], [0, 2],
     "Une donnée dérivée se calcule pendant le rendu, et une action de l'utilisateur se traite dans le gestionnaire d'événement. Minuteurs et écouteurs de la fenêtre sont de vrais effets."),
    ("single", "Que doit renvoyer un réducteur ?", None,
     ["Rien, il modifie l'état directement", "Une action", "Le nouvel état, sans muter l'ancien", "Une promesse"], [2],
     "Un réducteur est une fonction pure (etat, action) => nouvelEtat ; comme pour useState, l'ancien état n'est jamais modifié."),
    ("single", "Que renvoie useReducer(reducteur, initial) ?", None,
     ["[etat, dispatch]", "[etat, setEtat]", "{ state, actions }", "Le réducteur"], [0],
     "useReducer renvoie l'état courant et la fonction dispatch, qui envoie des actions au réducteur."),
    ("true_false", "Modifier maRef.current provoque un nouveau rendu du composant.", None,
     ["Vrai", "Faux"], [1],
     "Une ref conserve une valeur entre les rendus sans en déclencher : c'est sa différence essentielle avec l'état."),
    ("single", "Quelle valeur reçoit useContext(Ctx) si aucun <Ctx.Provider> n'entoure le composant ?", None,
     ["undefined dans tous les cas", "La valeur par défaut passée à createContext", "Une erreur est toujours levée", "La valeur du fournisseur le plus récent dans l'application"], [1],
     "Sans fournisseur au-dessus du composant, useContext renvoie la valeur par défaut donnée à createContext."),
    ("single", "Quel est le meilleur usage du contexte ?", None,
     ["Remplacer toutes les props", "Remplacer useState", "Stocker la saisie de chaque champ de formulaire", "Partager des données transversales comme le thème, la langue ou l'utilisateur connecté"], [3],
     "Le contexte évite le passage en cascade pour des données utilisées dans tout l'arbre ; pour le reste, les props restent plus explicites."),
]

QUIZ_M5 = [
    ("single", "Pourquoi ne peut-on pas écrire useEffect(async () => { … }) ?", None,
     ["Parce que fetch est interdit dans un effet", "Parce que await est interdit en React", "Parce qu'une fonction async renvoie une promesse, alors que l'effet doit renvoyer rien ou une fonction de nettoyage", "Parce que les effets doivent être synchrones pour Vite"], [2],
     "On déclare une fonction async à l'intérieur de l'effet et on l'appelle : l'effet lui-même reste libre de renvoyer sa fonction de nettoyage."),
    ("true_false", "fetch rejette sa promesse lorsque le serveur répond avec le statut 404.", None,
     ["Vrai", "Faux"], [1],
     "fetch ne rejette qu'en cas d'échec réseau (ou d'annulation) ; pour un 404 ou un 500, il faut tester reponse.ok."),
    ("multiple", "Quelles situations un composant qui charge des données doit-il prévoir ?", None,
     ["Le chargement en cours", "L'erreur", "Le succès avec une liste vide", "Le rechargement complet de la page"], [0, 1, 2],
     "Un affichage de données distantes gère le chargement, l'erreur et le succès, y compris le cas d'une liste vide ; aucun rechargement de page n'est nécessaire."),
    ("single", "À quoi sert AbortController dans un effet de chargement ?", None,
     ["À accélérer la requête", "À mettre la réponse en cache", "À relancer automatiquement la requête", "À annuler la requête au nettoyage, pour éviter d'afficher une réponse périmée"], [3],
     "abort() dans le nettoyage interrompt la requête quand le composant est démonté ou quand une dépendance change."),
    ("single", "Où placer l'appel fetch qui enregistre un formulaire envoyé par l'utilisateur ?", None,
     ["Dans le gestionnaire onSubmit", "Dans un useEffect sans dépendances", "Dans le corps du composant", "Dans le réducteur"], [0],
     "Un envoi répond à une action précise de l'utilisateur : il se place dans le gestionnaire d'événement, pas dans un effet."),
    ("single", "Quelle affirmation sur les clés d'API dans une application React est exacte ?", None,
     ["Une variable VITE_ reste secrète", "Il suffit de minifier le code", "Tout le code est envoyé au navigateur : aucune clé secrète ne doit y figurer", "Le contexte protège les secrets"], [2],
     "Le code front est public. Les variables préfixées VITE_ sont intégrées au code envoyé au navigateur ; les secrets restent sur le serveur."),
    ("single", "Quelle condition un hook personnalisé doit-il respecter ?", None,
     ["Être déclaré dans le même fichier que le composant", "Ne jamais appeler useState", "Renvoyer obligatoirement du JSX", "Avoir un nom qui commence par use et respecter les règles des hooks"], [3],
     "Le préfixe use permet à React et à ESLint de vérifier les règles des hooks ; un hook personnalisé appelle d'autres hooks et renvoie ce que l'on veut."),
    ("single", "Deux composants appellent useBascule(). Partagent-ils le même état ?", None,
     ["Oui, toujours", "Non : chaque appel crée un état indépendant", "Oui, s'ils sont dans le même fichier", "Seulement en production"], [1],
     "Les hooks personnalisés partagent de la logique, pas des données ; pour partager un état, on le remonte ou on utilise un contexte."),
    ("single", "Quel est le rôle de useDebounce(valeur, 300) ?", None,
     ["Renvoyer la valeur seulement après qu'elle est restée stable 300 ms", "Renvoyer la valeur avec 300 ms d'avance", "Limiter la valeur à 300 caractères", "Répéter la valeur toutes les 300 ms"], [0],
     "Chaque changement annule le minuteur précédent : seule la dernière valeur, restée inchangée pendant le délai, est retenue."),
    ("single", "Dans le mini-projet, pourquoi la liste des villes n'est-elle pas un état ?", None,
     ["Parce que les villes ne s'affichent pas", "Parce qu'elle se déduit des données chargées : c'est une donnée dérivée", "Parce que useState n'accepte pas les tableaux", "Parce qu'elle est stockée dans localStorage"], [1],
     "listeVilles(donnees) se recalcule à chaque rendu ; la stocker dans un état créerait un doublon susceptible de se désynchroniser."),
]
