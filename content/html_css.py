"""Contenu de la formation « HTML et CSS » (SMK Academy).

Blocs ```html / ```css pour le code, ```solution-html / ```solution-css pour les corrections.
scripts/check_web_course.mjs vérifie l'équilibre des balises HTML et la syntaxe des blocs CSS.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("html_css_m3_m5", _Path(__file__).with_name("html_css_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "html-css",
    "title": "HTML et CSS",
    "subtitle": "Construire et mettre en forme vos premières pages.",
    "description": (
        "Apprenez à construire des pages web propres, accessibles et adaptées au mobile. HTML pour "
        "structurer le contenu (texte, liens, images, tableaux, formulaires), CSS pour la mise en forme "
        "(couleurs, typographie, modèle de boîte), puis Flexbox, Grid et le responsive design. "
        "La formation se termine par la réalisation d'une page de présentation complète. Chaque module "
        "se termine par un quiz noté sur 20."
    ),
    "category": "Développement web",
    "category_slug": "developpement-web",
    "topic": "HTML/CSS",
    "cover_label": "HTML",
    "level": "debutant",
    "duration_minutes": 600,
    "objectives": [
        "Structurer une page en HTML sémantique et accessible",
        "Créer des tableaux et des formulaires",
        "Mettre en forme avec CSS et maîtriser le modèle de boîte",
        "Construire des mises en page avec Flexbox et Grid",
        "Créer un site adapté au mobile",
    ],
    "prerequisites": ["Aucun prérequis", "Un éditeur de texte (Visual Studio Code conseillé) et un navigateur"],
    "status": "published",
    "is_premium": False,
    "position": 21,
}

M1_L1 = r"""
## Comment fonctionne une page web

Quand vous ouvrez un site, votre navigateur télécharge un fichier **HTML** (le contenu et sa structure), des fichiers **CSS** (l'apparence) et souvent du **JavaScript** (le comportement). Il assemble le tout et affiche la page.

HTML (*HyperText Markup Language*) n'est pas un langage de programmation : c'est un **langage de balisage**. On entoure chaque contenu de **balises** qui indiquent sa nature.

```html
<p>Ceci est un paragraphe.</p>
```

- `<p>` est la balise **ouvrante**, `</p>` la balise **fermante** ;
- l'ensemble forme un **élément** ;
- certains éléments n'ont pas de contenu et pas de balise fermante, comme `<br>` (retour à la ligne) ou `<img>`.

## Préparer son poste de travail

1. Installez un éditeur de code : **Visual Studio Code** est gratuit et très répandu.
2. Créez un dossier `mon-site`, puis un fichier `index.html`.
3. Ouvrez ce fichier dans votre navigateur (double-clic). Après chaque modification, enregistrez et rechargez la page (`F5`).

## La structure minimale d'une page

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Ma première page</title>
  </head>
  <body>
    <h1>Bonjour !</h1>
    <p>Bienvenue sur ma première page web.</p>
  </body>
</html>
```

| Élément | Rôle |
|---|---|
| `<!DOCTYPE html>` | indique au navigateur qu'il s'agit de HTML moderne |
| `<html lang="fr">` | racine de la page ; `lang` aide les lecteurs d'écran et les moteurs de recherche |
| `<head>` | informations sur la page, non affichées dans la page elle-même |
| `<meta charset="utf-8">` | encodage : indispensable pour les accents |
| `<meta name="viewport" …>` | adapte l'affichage aux écrans mobiles |
| `<title>` | titre affiché dans l'onglet et dans les résultats de recherche |
| `<body>` | tout le contenu visible |

## Les attributs

Une balise ouvrante peut porter des **attributs**, qui précisent l'élément. Ils s'écrivent `nom="valeur"` :

```html
<a href="https://www.example.com" target="_blank">Visiter le site</a>
```

## Imbrication et indentation

Les éléments s'emboîtent comme des poupées russes ; un élément ouvert à l'intérieur d'un autre doit être fermé **avant** lui.

```html
<p>Un mot <strong>important</strong> dans la phrase.</p>
```

`<p><strong>…</p></strong>` serait incorrect. Indentez votre code (2 espaces par niveau) pour visualiser cette imbrication.

## Les commentaires et les outils du navigateur

```html
<!-- Ce commentaire n'est pas affiché -->
```

Clic droit sur un élément → **Inspecter** : les outils de développement montrent le HTML réellement interprété. C'est le meilleur moyen de comprendre une page.

## À retenir

- HTML structure le contenu à l'aide de balises : `<p>…</p>`.
- Squelette : `<!DOCTYPE html>`, `<html lang>`, `<head>` (charset, viewport, title), `<body>`.
- Les attributs précisent un élément : `href="…"`.
- Les éléments s'emboîtent sans se chevaucher.

## Exercices

### Exercice 1 — Votre première page

Créez une page dont le titre d'onglet est « Mon CV », qui affiche votre nom en grand titre et une phrase de présentation.

```solution-html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Mon CV</title>
  </head>
  <body>
    <h1>Amina Benali</h1>
    <p>Développeuse web junior, passionnée par l'accessibilité.</p>
  </body>
</html>
```

### Exercice 2 — Trouvez l'erreur

Ce code est mal imbriqué : `<p>Bonjour <em>tout le monde</p></em>`. Corrigez-le.

```solution-html
<p>Bonjour <em>tout le monde</em></p>
```
"""

M1_L2 = r"""
## Les titres

HTML propose six niveaux de titres, de `<h1>` (le plus important) à `<h6>` :

```html
<h1>Recettes de saison</h1>
<h2>Entrées</h2>
<h3>Velouté de potiron</h3>
<h2>Desserts</h2>
```

Règles essentielles :

- **un seul `<h1>`** par page, qui décrit son sujet ;
- **ne pas sauter de niveau** (pas de `<h4>` directement sous un `<h2>`) ;
- choisir un titre pour son **rôle**, jamais pour sa taille : la taille se règle en CSS.

Les lecteurs d'écran utilisent cette hiérarchie pour naviguer, comme une table des matières.

## Paragraphes et mise en valeur

```html
<p>Le <strong>délai d'inscription</strong> est fixé au 30 juin.</p>
<p>Ce module est <em>facultatif</em>.<br>Il compte pour 10 % de la note.</p>
```

- `<strong>` : importance forte (affiché en gras) ;
- `<em>` : emphase (affichée en italique) ;
- `<br>` : retour à la ligne à l'intérieur d'un paragraphe (à utiliser avec parcimonie).

## Les listes

```html
<ul>
  <li>HTML</li>
  <li>CSS</li>
  <li>JavaScript</li>
</ul>

<ol>
  <li>Préchauffer le four.</li>
  <li>Mélanger les ingrédients.</li>
  <li>Enfourner 30 minutes.</li>
</ol>
```

`<ul>` (*unordered list*) pour une liste à puces, `<ol>` (*ordered list*) pour une liste numérotée ; chaque élément dans un `<li>`.

## Les liens

```html
<a href="https://developer.mozilla.org">Documentation MDN</a>
<a href="contact.html">Nous contacter</a>
<a href="#tarifs">Voir les tarifs</a>
<a href="mailto:contact@exemple.fr">Écrire un email</a>
```

- une **URL absolue** pointe vers un autre site ;
- un **chemin relatif** (`contact.html`) pointe vers une page de votre site ;
- `#tarifs` pointe vers l'élément de la page qui porte `id="tarifs"`.

Le texte du lien doit être **explicite** : « Télécharger le programme (PDF) » plutôt que « cliquez ici ».

## Les images

```html
<img src="images/equipe.jpg" alt="L'équipe SMKTECH réunie devant les bureaux de Paris" width="800" height="533">
```

- `src` : chemin de l'image ;
- `alt` : **texte alternatif**, lu par les lecteurs d'écran et affiché si l'image ne charge pas. Il est obligatoire ; pour une image purement décorative, on écrit `alt=""` ;
- `width` et `height` réservent la place de l'image et évitent que la page « saute » pendant le chargement.

Formats : **JPEG** ou **WebP** pour les photos, **PNG** pour les images avec transparence, **SVG** pour les logos et icônes.

## À retenir

- Un seul `<h1>`, une hiérarchie de titres sans saut.
- `<p>`, `<strong>`, `<em>`, `<br>`.
- `<ul>` / `<ol>` + `<li>`.
- `<a href>` avec un texte explicite ; `#id` pour un lien interne.
- `<img>` avec un `alt` pertinent, `width` et `height`.

## Exercices

### Exercice 1 — Corrigez la hiérarchie

Cette page utilise deux `<h1>` et saute un niveau : `<h1>Blog</h1> <h1>Article</h1> <h4>Introduction</h4>`. Proposez une hiérarchie correcte.

```solution-html
<h1>Blog</h1>
<h2>Article</h2>
<h3>Introduction</h3>
```

### Exercice 2 — Une liste de liens

Créez une liste à puces de trois liens : la page d'accueil (`index.html`), la page contact (`contact.html`) et la section `#faq` de la page actuelle.

```solution-html
<ul>
  <li><a href="index.html">Accueil</a></li>
  <li><a href="contact.html">Contact</a></li>
  <li><a href="#faq">Questions fréquentes</a></li>
</ul>
```

### Exercice 3 — Texte alternatif

Rédigez un attribut `alt` pour : (a) le logo de l'entreprise SMKTECH, cliquable vers l'accueil ; (b) une simple ligne décorative.

```solution-text
(a) alt="SMKTECH – retour à l'accueil"   → décrit la fonction du lien, pas l'apparence du logo
(b) alt=""                                → image décorative : texte vide, ignorée par les lecteurs d'écran
```
"""

M1_L3 = r"""
## Le HTML sémantique

Une page peut être entièrement construite avec des `<div>` (blocs sans signification). Mais HTML propose des éléments qui décrivent le **rôle** de chaque zone : on parle de HTML **sémantique**.

```html
<body>
  <header>
    <a href="/">SMK Academy</a>
    <nav aria-label="Navigation principale">
      <ul>
        <li><a href="/formations">Formations</a></li>
        <li><a href="/tarifs">Tarifs</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <article>
      <h1>Apprendre le HTML en 2026</h1>
      <p>Publié le <time datetime="2026-11-05">5 novembre 2026</time></p>
      <section>
        <h2>Pourquoi le HTML reste essentiel</h2>
        <p>…</p>
      </section>
    </article>
    <aside>
      <h2>À lire aussi</h2>
      <p>…</p>
    </aside>
  </main>

  <footer>
    <p>© 2026 SMKTECH</p>
  </footer>
</body>
```

| Élément | Rôle |
|---|---|
| `<header>` | en-tête (logo, navigation) |
| `<nav>` | bloc de navigation principal |
| `<main>` | contenu principal, **un seul par page** |
| `<article>` | contenu autonome (article, fiche produit, carte) |
| `<section>` | partie thématique, généralement avec un titre |
| `<aside>` | contenu complémentaire (encadré, liens connexes) |
| `<footer>` | pied de page |
| `<time>` | date ou heure lisible par les machines |

## Pourquoi c'est important

1. **Accessibilité** : les lecteurs d'écran permettent de sauter directement au `<main>` ou à la `<nav>`.
2. **Référencement** : les moteurs de recherche comprennent mieux la structure.
3. **Lisibilité du code** : `<nav>` est plus parlant que `<div class="menu">`.

`<div>` (bloc) et `<span>` (en ligne) restent utiles, mais uniquement quand aucun élément sémantique ne convient, typiquement pour la mise en page en CSS.

## Éléments de type bloc et en ligne

- Les éléments **bloc** (`<p>`, `<h1>`, `<ul>`, `<div>`, `<section>`) occupent toute la largeur disponible et commencent sur une nouvelle ligne.
- Les éléments **en ligne** (`<a>`, `<strong>`, `<em>`, `<span>`, `<img>`) s'insèrent dans le texte.

Ce comportement par défaut pourra être modifié en CSS (module 4).

## Valider son code

Un navigateur affiche presque toujours quelque chose, même avec un HTML incorrect : les erreurs passent donc inaperçues. Le validateur officiel du W3C (validator.w3.org) signale les balises mal fermées, les attributs manquants et les imbrications interdites. Prenez l'habitude de l'utiliser.

## À retenir

- `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`.
- Un seul `<main>` par page.
- Sémantique = accessibilité + référencement + lisibilité.
- `<div>` et `<span>` seulement à défaut d'élément plus précis.
- Bloc : nouvelle ligne, toute la largeur ; en ligne : dans le texte.

## Exercices

### Exercice 1 — Structurez la page

Écrivez la structure sémantique d'une page de blog : un en-tête avec le nom du blog et une navigation, un article principal avec un titre, et un pied de page.

```solution-html
<body>
  <header>
    <p>Le blog de Lucas</p>
    <nav aria-label="Navigation principale">
      <ul>
        <li><a href="index.html">Accueil</a></li>
        <li><a href="archives.html">Archives</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <article>
      <h1>Mon premier article</h1>
      <p>Bienvenue sur mon blog.</p>
    </article>
  </main>
  <footer>
    <p>© 2026 Lucas Martin</p>
  </footer>
</body>
```

### Exercice 2 — Bloc ou en ligne ?

Classez : `<p>`, `<a>`, `<section>`, `<strong>`, `<ul>`, `<span>`.

```solution-text
Bloc : <p>, <section>, <ul>
En ligne : <a>, <strong>, <span>
```
"""

M2_L1 = r"""
## Quand utiliser un tableau ?

Un tableau HTML sert à présenter des **données tabulaires** : horaires, tarifs, résultats, comparatifs. Il ne doit **jamais** servir à mettre en page un site (on utilise CSS pour cela).

## Structure d'un tableau

```html
<table>
  <caption>Résultats du trimestre</caption>
  <thead>
    <tr>
      <th scope="col">Module</th>
      <th scope="col">Note</th>
      <th scope="col">Statut</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Python</th>
      <td>16/20</td>
      <td>Validé</td>
    </tr>
    <tr>
      <th scope="row">SQL</th>
      <td>9/20</td>
      <td>À repasser</td>
    </tr>
  </tbody>
</table>
```

| Élément | Rôle |
|---|---|
| `<table>` | le tableau |
| `<caption>` | titre du tableau (important pour l'accessibilité) |
| `<thead>`, `<tbody>`, `<tfoot>` | en-tête, corps, pied |
| `<tr>` | une ligne (*table row*) |
| `<th>` | une cellule d'en-tête ; `scope="col"` ou `scope="row"` précise si elle titre une colonne ou une ligne |
| `<td>` | une cellule de données |

Les attributs `scope` permettent aux lecteurs d'écran d'annoncer, pour chaque cellule, l'en-tête correspondant (« Note : 16/20 »).

## Fusionner des cellules

```html
<table>
  <tr>
    <th scope="col">Jour</th>
    <th scope="col">Matin</th>
    <th scope="col">Après-midi</th>
  </tr>
  <tr>
    <th scope="row">Lundi</th>
    <td colspan="2">Formation toute la journée</td>
  </tr>
</table>
```

`colspan="2"` étend une cellule sur deux colonnes ; `rowspan` sur plusieurs lignes. À utiliser avec modération : les tableaux complexes sont difficiles à lire, surtout sur mobile.

## À retenir

- Tableaux pour les données, jamais pour la mise en page.
- `<caption>`, `<thead>`, `<tbody>`, `<tr>`, `<th scope>`, `<td>`.
- `colspan` / `rowspan` pour fusionner, avec modération.

## Exercices

### Exercice 1 — Tableau des tarifs

Créez un tableau avec une légende « Nos offres », deux colonnes (Offre, Prix) et deux lignes : Free à 0 €, Premium à 1 € par mois.

```solution-html
<table>
  <caption>Nos offres</caption>
  <thead>
    <tr>
      <th scope="col">Offre</th>
      <th scope="col">Prix</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Free</th>
      <td>0 €</td>
    </tr>
    <tr>
      <th scope="row">Premium</th>
      <td>1 € par mois</td>
    </tr>
  </tbody>
</table>
```

### Exercice 2 — Bon usage ?

Un développeur utilise un tableau à deux colonnes pour placer un menu à gauche et le contenu à droite. Est-ce une bonne pratique ?

```solution-text
Non. Un tableau doit contenir des données tabulaires. Pour la mise en page, on utilise des éléments
sémantiques (<nav>, <main>) disposés avec CSS (Flexbox ou Grid). Un tableau de mise en page perturbe
les lecteurs d'écran et s'adapte mal aux mobiles.
```
"""

M2_L2 = r"""
## Le formulaire

Un formulaire recueille des informations : inscription, contact, recherche, paiement.

```html
<form action="/inscription" method="post">
  <label for="prenom">Prénom</label>
  <input id="prenom" name="prenom" type="text" autocomplete="given-name" required>

  <label for="email">Adresse email</label>
  <input id="email" name="email" type="email" autocomplete="email" required>

  <button type="submit">Créer mon compte</button>
</form>
```

- `action` : adresse qui reçoit les données ; `method` : `get` (recherche, données visibles dans l'URL) ou `post` (envoi de données) ;
- `name` : nom sous lequel la valeur est envoyée ;
- `<button type="submit">` envoie le formulaire.

## Le label : indispensable

Chaque champ doit avoir un `<label>` relié par `for` = `id` du champ :

- le lecteur d'écran annonce le label quand le champ reçoit le focus ;
- cliquer sur le label place le curseur dans le champ (plus grande zone cliquable, utile sur mobile).

> Un texte d'exemple (`placeholder`) **ne remplace pas** un label : il disparaît dès que l'on commence à écrire et il est souvent trop pâle pour être lu.

## Les types de champs

| Type | Usage | Bénéfice |
|---|---|---|
| `text` | texte court | |
| `email` | adresse email | clavier avec @ sur mobile, vérification du format |
| `password` | mot de passe | caractères masqués |
| `tel` | téléphone | clavier numérique sur mobile |
| `number` | nombre | flèches, `min`, `max`, `step` |
| `date` | date | sélecteur de date |
| `checkbox` | case à cocher | choix multiples |
| `radio` | bouton radio | un seul choix parmi plusieurs (même `name`) |

```html
<fieldset>
  <legend>Niveau souhaité</legend>
  <input id="niv-deb" type="radio" name="niveau" value="debutant" checked>
  <label for="niv-deb">Débutant</label>
  <input id="niv-int" type="radio" name="niveau" value="intermediaire">
  <label for="niv-int">Intermédiaire</label>
</fieldset>

<label for="pays">Pays</label>
<select id="pays" name="pays">
  <option value="fr">France</option>
  <option value="be">Belgique</option>
</select>

<label for="message">Message</label>
<textarea id="message" name="message" rows="5"></textarea>

<input id="cgu" type="checkbox" name="cgu" required>
<label for="cgu">J'accepte les conditions d'utilisation</label>
```

`<fieldset>` et `<legend>` regroupent des champs liés, comme des boutons radio.

## La validation intégrée

Le navigateur vérifie automatiquement certains attributs avant l'envoi :

- `required` : champ obligatoire ;
- `minlength` / `maxlength` : longueur du texte ;
- `min` / `max` : bornes d'un nombre ou d'une date ;
- `pattern` : expression régulière (par exemple un code postal à 5 chiffres : `pattern="[0-9]{5}"`).

Cette validation améliore l'expérience, mais **le serveur doit toujours revérifier** : n'importe qui peut la contourner.

## `autocomplete` : faire gagner du temps

`autocomplete="email"`, `"given-name"`, `"family-name"`, `"tel"`, `"postal-code"`, `"new-password"` permettent au navigateur et aux gestionnaires de mots de passe de remplir les champs correctement.

## À retenir

- Chaque champ a un `<label for>` relié à son `id` ; le placeholder ne remplace pas le label.
- Choisir le bon `type` (email, tel, number, date…).
- Radios d'un même groupe : même `name`, regroupés dans un `<fieldset>` avec `<legend>`.
- `required`, `minlength`, `min`, `pattern` ; le serveur revérifie toujours.

## Exercices

### Exercice 1 — Formulaire de contact

Créez un formulaire de contact : nom (obligatoire), email (obligatoire), message (zone de texte, 20 caractères minimum) et un bouton « Envoyer ».

```solution-html
<form action="/contact" method="post">
  <label for="nom">Nom</label>
  <input id="nom" name="nom" type="text" autocomplete="name" required>

  <label for="email">Adresse email</label>
  <input id="email" name="email" type="email" autocomplete="email" required>

  <label for="message">Message</label>
  <textarea id="message" name="message" rows="6" minlength="20" required></textarea>

  <button type="submit">Envoyer</button>
</form>
```

### Exercice 2 — Choix unique

Ajoutez un choix « Vous êtes : Étudiant / Professionnel » avec des boutons radio correctement regroupés.

```solution-html
<fieldset>
  <legend>Vous êtes</legend>
  <input id="statut-etu" type="radio" name="statut" value="etudiant">
  <label for="statut-etu">Étudiant</label>
  <input id="statut-pro" type="radio" name="statut" value="professionnel">
  <label for="statut-pro">Professionnel</label>
</fieldset>
```
"""

M2_L3 = r"""
## Une page pour tout le monde

L'**accessibilité** (souvent abrégée *a11y*) consiste à rendre un site utilisable par tous : personnes aveugles ou malvoyantes (lecteurs d'écran, zoom), personnes qui naviguent au clavier, personnes daltoniennes, mais aussi quelqu'un qui consulte son téléphone en plein soleil. En France, elle est encadrée par le **RGAA** ; à l'international, par les **WCAG**.

Bonne nouvelle : la plupart des règles reposent sur un HTML **correct et sémantique**.

## Les règles essentielles

1. **Langue** : `<html lang="fr">`.
2. **Titres** hiérarchisés, un seul `<h1>`.
3. **Images** : un `alt` pertinent, ou `alt=""` si décorative.
4. **Liens** explicites hors contexte : « Lire l'article sur Flexbox » plutôt que « Lire la suite ».
5. **Formulaires** : un `<label>` pour chaque champ, des messages d'erreur clairs.
6. **Clavier** : tout doit être utilisable avec `Tab`, `Entrée` et `Espace`. Utilisez de vrais `<button>` et `<a>`, jamais un `<div>` cliquable.
7. **Contraste** suffisant entre le texte et le fond (au moins 4,5:1 pour le texte courant).
8. **Ne pas transmettre une information par la couleur seule** : un champ en erreur est rouge **et** accompagné d'un message.

## Bouton ou lien ?

| Élément | Quand l'utiliser |
|---|---|
| `<a href="…">` | pour **aller** quelque part (une autre page, une section) |
| `<button>` | pour **agir** (envoyer, ouvrir un menu, supprimer) |

```html
<!-- À éviter : invisible au clavier et aux lecteurs d'écran -->
<div class="bouton" onclick="ouvrirMenu()">Menu</div>

<!-- Correct -->
<button type="button" aria-expanded="false" aria-controls="menu">Menu</button>
```

## Les attributs ARIA, avec parcimonie

Les attributs **ARIA** (`aria-label`, `aria-expanded`, `aria-live`…) complètent l'information transmise aux technologies d'assistance, quand le HTML seul ne suffit pas :

```html
<button type="button" aria-label="Fermer la fenêtre">×</button>
<p role="alert">Le mot de passe est incorrect.</p>
```

Première règle d'ARIA : **si un élément HTML natif fait l'affaire, utilisez-le**. Un `<button>` vaut mieux qu'un `<div role="button">`.

## Tester simplement

- Parcourez la page uniquement au **clavier** (`Tab`, `Maj+Tab`) : voyez-vous toujours où se trouve le focus ?
- Zoomez à **200 %** : la page reste-t-elle lisible ?
- Lancez l'audit **Lighthouse** des outils de développement de Chrome (onglet *Lighthouse* → *Accessibility*).

## À retenir

- Accessibilité = HTML sémantique + alternatives textuelles + clavier + contrastes.
- `<a>` pour naviguer, `<button>` pour agir ; jamais de `<div>` cliquable.
- ARIA en complément, jamais à la place d'un élément natif.
- Testez au clavier, au zoom et avec Lighthouse.

## Exercices

### Exercice 1 — Corrigez

Repérez et corrigez les problèmes : `<img src="graphique.png">` puis `<div onclick="envoyer()">Envoyer</div>` puis `<a href="cours.html">Cliquez ici</a>`.

```solution-html
<img src="graphique.png" alt="Ventes 2026 : hausse de 30 % entre janvier et juin">
<button type="submit">Envoyer</button>
<a href="cours.html">Voir le programme du cours</a>
```

### Exercice 2 — Un message d'erreur accessible

Un champ email en erreur est seulement entouré de rouge. Pourquoi est-ce insuffisant, et que faut-il ajouter ?

```solution-text
La couleur seule n'est pas perçue par les personnes daltoniennes ni annoncée par les lecteurs d'écran.
Il faut ajouter un message texte explicite (par exemple « L'adresse email doit contenir @ »), placé près
du champ et annoncé, par exemple avec role="alert" ou relié au champ par aria-describedby.
```
"""

QUIZ_M1 = [
    ("single", "Quel est le rôle de HTML ?", None,
     ["Mettre en forme la page", "Structurer le contenu de la page", "Rendre la page interactive", "Héberger le site"], [1],
     "HTML structure le contenu ; CSS gère l'apparence et JavaScript le comportement."),
    ("single", "Que contient l'élément <head> ?", None,
     ["Le contenu visible de la page", "Les informations sur la page (titre, encodage…)", "Le pied de page", "Le menu de navigation"], [1],
     "<head> regroupe les métadonnées (charset, viewport, title…) ; le contenu visible est dans <body>."),
    ("single", "Pourquoi écrire <meta charset=\"utf-8\"> ?", None,
     ["Pour accélérer la page", "Pour afficher correctement les accents et caractères spéciaux", "Pour le référencement uniquement", "Pour activer JavaScript"], [1],
     "L'encodage UTF-8 garantit l'affichage correct des caractères accentués et spéciaux."),
    ("single", "Combien de <h1> une page devrait-elle contenir ?", None,
     ["Aucun", "Un seul", "Un par section", "Autant que nécessaire"], [1],
     "Un seul <h1>, qui décrit le sujet de la page ; les sous-parties utilisent <h2>, <h3>…"),
    ("single", "Quelle balise crée une liste numérotée ?", None,
     ["<ul>", "<ol>", "<li>", "<list>"], [1],
     "<ol> (ordered list) crée une liste numérotée ; <ul> une liste à puces ; <li> un élément de liste."),
    ("single", "À quoi sert l'attribut alt d'une image ?", None,
     ["À donner un titre au survol", "À fournir un texte alternatif lu par les lecteurs d'écran et affiché si l'image ne charge pas", "À redimensionner l'image", "À créer un lien"], [1],
     "alt est indispensable pour l'accessibilité ; il vaut \"\" pour une image décorative."),
    ("single", "Quelle imbrication est correcte ?", None,
     ["<p><em>texte</p></em>", "<p><em>texte</em></p>", "<em><p>texte</em></p>", "<p>texte<em></p>"], [1],
     "Le dernier élément ouvert doit être le premier fermé."),
    ("single", "Que fait le lien <a href=\"#tarifs\">Tarifs</a> ?", None,
     ["Ouvre la page tarifs.html", "Fait défiler jusqu'à l'élément id=\"tarifs\" de la page", "Envoie un email", "Rien"], [1],
     "#tarifs cible l'élément de la page dont l'identifiant est « tarifs »."),
    ("multiple", "Quels éléments sont sémantiques ?", None,
     ["<header>", "<div>", "<nav>", "<article>"], [0, 2, 3],
     "<header>, <nav> et <article> décrivent un rôle ; <div> est un bloc générique sans signification."),
    ("single", "Combien d'éléments <main> une page devrait-elle contenir ?", None,
     ["Un seul", "Deux", "Un par article", "Aucun"], [0],
     "<main> désigne le contenu principal : il est unique dans la page."),
]

QUIZ_M2 = [
    ("single", "Dans un tableau, quelle balise crée une cellule d'en-tête ?", None,
     ["<td>", "<th>", "<tr>", "<thead>"], [1],
     "<th> crée une cellule d'en-tête ; <td> une cellule de données ; <tr> une ligne."),
    ("single", "À quoi sert scope=\"col\" sur un <th> ?", None,
     ["À fusionner des colonnes", "À indiquer que la cellule est l'en-tête d'une colonne", "À centrer le texte", "À trier la colonne"], [1],
     "scope permet aux lecteurs d'écran d'associer chaque donnée à son en-tête de colonne ou de ligne."),
    ("true_false", "Un tableau HTML est une bonne solution pour mettre en page un site (menu à gauche, contenu à droite).", None,
     ["Vrai", "Faux"], [1],
     "Les tableaux sont réservés aux données tabulaires ; la mise en page se fait en CSS."),
    ("single", "Comment relier un <label> à son champ ?", None,
     ["Avec l'attribut name", "Avec for sur le label égal à l'id du champ", "Avec la même classe", "En plaçant le label après le champ"], [1],
     "for=\"email\" sur le label et id=\"email\" sur le champ les relient."),
    ("single", "Pourquoi un placeholder ne remplace-t-il pas un label ?", None,
     ["Il est trop long", "Il disparaît dès la saisie et il est souvent peu lisible", "Il n'est pas envoyé au serveur", "Il est interdit en HTML5"], [1],
     "Le placeholder disparaît quand on écrit et a un faible contraste : un label visible reste indispensable."),
    ("single", "Quel type de champ affiche un clavier numérique adapté sur mobile pour un numéro de téléphone ?", None,
     ["text", "number", "tel", "phone"], [2],
     "type=\"tel\" affiche le pavé téléphonique ; number est destiné aux quantités."),
    ("single", "Comment permettre un seul choix parmi plusieurs boutons radio ?", None,
     ["Leur donner le même id", "Leur donner le même name", "Les placer dans une liste", "Ajouter required"], [1],
     "Les boutons radio d'un même groupe partagent le même name ; l'id, lui, reste unique."),
    ("single", "Quel attribut rend un champ obligatoire ?", None,
     ["mandatory", "required", "needed", "validate"], [1],
     "required empêche l'envoi tant que le champ est vide."),
    ("single", "Pour une action comme « Ouvrir le menu », quel élément utiliser ?", None,
     ["<div onclick>", "<a href=\"#\">", "<button type=\"button\">", "<span>"], [2],
     "Un <button> est utilisable au clavier et annoncé correctement ; <a> sert à naviguer."),
    ("multiple", "Quelles pratiques améliorent l'accessibilité ?", None,
     ["Indiquer une erreur uniquement par la couleur rouge", "Un label pour chaque champ", "Des liens au texte explicite", "Un contraste suffisant"], [1, 2, 3],
     "La couleur seule ne suffit pas : il faut aussi un message texte."),
]

MODULES = [
    {
        "position": 1,
        "title": "Les bases du HTML",
        "description": "Structure d'une page, texte, listes, liens, images et HTML sémantique.",
        "status": "published",
        "lessons": [
            ("premiere-page", "Votre première page",
             "Balises, structure minimale d'une page, attributs et outils du navigateur.", M1_L1, 25),
            ("texte-liens-images", "Texte, listes, liens et images",
             "Titres, paragraphes, listes, liens et images accessibles.", M1_L2, 30),
            ("html-semantique", "Le HTML sémantique",
             "header, nav, main, article, section, footer ; bloc et en ligne.", M1_L3, 25),
        ],
        "quiz": ("Quiz — Les bases du HTML", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Tableaux, formulaires et accessibilité",
        "description": "Présenter des données, recueillir des informations et rendre la page utilisable par tous.",
        "status": "published",
        "lessons": [
            ("tableaux", "Les tableaux",
             "Structure, en-têtes, légende et fusion de cellules.", M2_L1, 20),
            ("formulaires", "Les formulaires",
             "Labels, types de champs, validation intégrée et autocomplétion.", M2_L2, 35),
            ("accessibilite", "L'accessibilité",
             "Règles essentielles, boutons et liens, ARIA et tests.", M2_L3, 30),
        ],
        "quiz": ("Quiz — Tableaux, formulaires et accessibilité", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Les bases du CSS",
        "description": "Sélecteurs, couleurs, typographie, cascade et modèle de boîte.",
        "status": "published",
        "lessons": [
            ("premiers-styles", "Premiers styles",
             "Relier une feuille de style, règles, sélecteurs et couleurs.", _m35.M3_L1, 30),
            ("typographie-cascade", "Typographie, cascade et spécificité",
             "Polices, tailles, unités, héritage et priorité des règles.", _m35.M3_L2, 30),
            ("modele-de-boite", "Le modèle de boîte",
             "Contenu, padding, border, margin et box-sizing.", _m35.M3_L3, 30),
        ],
        "quiz": ("Quiz — Les bases du CSS", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "La mise en page",
        "description": "display, Flexbox, Grid et positionnement.",
        "status": "published",
        "lessons": [
            ("flexbox", "Flexbox",
             "Aligner et répartir des éléments sur une ligne ou une colonne.", _m35.M4_L1, 35),
            ("grid", "CSS Grid",
             "Construire des grilles en deux dimensions.", _m35.M4_L2, 35),
            ("position", "Positionnement et superposition",
             "position relative, absolute, fixed, sticky et z-index.", _m35.M4_L3, 25),
        ],
        "quiz": ("Quiz — La mise en page", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Responsive design et projet",
        "description": "Adapter la page à tous les écrans, variables, transitions et mini-projet.",
        "status": "published",
        "lessons": [
            ("responsive", "Le responsive design",
             "Mobile first, media queries, images et unités fluides.", _m35.M5_L1, 30),
            ("variables-transitions", "Variables CSS, thème sombre et transitions",
             "Custom properties, prefers-color-scheme et animations sobres.", _m35.M5_L2, 25),
            ("mini-projet", "Mini-projet : une page de présentation",
             "Construire et publier une page complète, accessible et responsive.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Responsive design et projet", _m35.QUIZ_M5),
    },
]
