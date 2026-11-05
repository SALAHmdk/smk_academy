"""Modules 3 à 5 de « HTML et CSS » (importé par content/html_css.py)."""

M3_L1 = r"""
## Relier une feuille de style

Le CSS (*Cascading Style Sheets*) s'écrit dans un fichier séparé, relié dans le `<head>` :

```html
<link rel="stylesheet" href="style.css">
```

Un seul fichier CSS peut mettre en forme toutes les pages d'un site : changer une couleur dans ce fichier la change partout.

## Anatomie d'une règle

```css
h1 {
  color: #0B4BD6;
  font-size: 2rem;
}
```

- `h1` est le **sélecteur** : il désigne les éléments concernés ;
- entre accolades, des **déclarations** `propriété: valeur;`.

## Les sélecteurs essentiels

```css
p { line-height: 1.6; }                 /* tous les <p> */
.alerte { color: #B42318; }             /* les éléments class="alerte" */
#inscription { max-width: 30rem; }      /* l'élément id="inscription" */
nav a { text-decoration: none; }        /* les <a> situés dans une <nav> */
h1, h2, h3 { font-weight: 700; }        /* plusieurs sélecteurs */
a:hover { text-decoration: underline; } /* au survol */
button:focus-visible { outline: 3px solid #0B4BD6; } /* focus clavier */
```

| Sélecteur | Cible |
|---|---|
| `p` | une balise |
| `.classe` | une classe (réutilisable sur plusieurs éléments) |
| `#id` | un identifiant (unique dans la page) |
| `parent enfant` | un descendant |
| `:hover`, `:focus-visible` | un état (pseudo-classe) |

> Bonne pratique : stylez surtout avec des **classes**. Les identifiants sont trop prioritaires (leçon suivante) et ne sont pas réutilisables.

Une classe s'ajoute dans le HTML ; un élément peut en avoir plusieurs :

```html
<p class="carte carte--mise-en-avant">Offre Premium</p>
```

## Les couleurs

```css
.exemples {
  color: #0B4BD6;                 /* hexadécimal */
  background-color: rgb(0 179 134); /* rouge vert bleu */
  border-color: rgb(0 0 0 / 0.1); /* avec transparence */
  outline-color: royalblue;       /* nom de couleur */
}
```

Le code hexadécimal `#RRGGBB` est le plus utilisé ; `rgb(… / opacité)` permet la transparence.

Vérifiez toujours le **contraste** entre le texte et son fond : au moins 4,5:1 pour le texte courant. Les outils de développement de Chrome l'affichent dans le sélecteur de couleur.

## Les commentaires

```css
/* Les commentaires CSS s'écrivent ainsi */
```

## À retenir

- `<link rel="stylesheet" href="style.css">` dans le `<head>`.
- `sélecteur { propriété: valeur; }`.
- Sélecteurs : balise, `.classe`, `#id`, descendant, `:hover`, `:focus-visible`.
- Préférer les classes ; vérifier les contrastes.

## Exercices

### Exercice 1 — Premiers styles

Écrivez le CSS qui met tous les paragraphes en gris foncé (`#333333`) et les liens en bleu `#0B4BD6`, soulignés seulement au survol.

```solution-css
p {
  color: #333333;
}
a {
  color: #0B4BD6;
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
}
```

### Exercice 2 — Une classe réutilisable

Créez une classe `.badge` (fond vert `#00B386`, texte blanc) et appliquez-la à un `<span>` « Nouveau ».

```solution-css
.badge {
  background-color: #00B386;
  color: #ffffff;
}
```

```solution-html
<span class="badge">Nouveau</span>
```
"""

M3_L2 = r"""
## La typographie

```css
body {
  font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
  color: #1d1d1f;
}
h1 {
  font-size: 2.5rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}
.intro {
  font-size: 1.25rem;
  font-style: italic;
  text-align: center;
}
```

- `font-family` : liste de polices, de la préférée à la plus générique (`sans-serif`, `serif`, `monospace`) ;
- `font-size`, `font-weight` (400 = normal, 700 = gras), `line-height` (interligne, sans unité) ;
- `text-align`, `text-transform`, `letter-spacing`.

Pour une police personnalisée, on utilise un service comme Google Fonts ou la règle `@font-face`.

## Les unités

| Unité | Relative à | Usage typique |
|---|---|---|
| `px` | pixel de référence | bordures fines, ombres |
| `rem` | taille de police de la racine (souvent 16 px) | tailles de texte, espacements |
| `em` | taille de police de l'élément | espacements proportionnels au texte |
| `%` | élément parent | largeurs |
| `vw` / `vh` | 1 % de la largeur / hauteur de la fenêtre | sections plein écran |

> Utilisez `rem` pour les tailles de texte : si l'utilisateur agrandit la police de son navigateur, toute la page suit. Des tailles en `px` ignorent ce réglage.

## L'héritage

Certaines propriétés, surtout celles du texte (`color`, `font-family`, `line-height`), se **transmettent** aux éléments enfants. C'est pourquoi on définit la police une seule fois sur `body`. Les propriétés de boîte (`margin`, `border`, `background`) ne s'héritent pas.

## La cascade et la spécificité

Quand plusieurs règles ciblent le même élément, laquelle s'applique ? Le navigateur compare la **spécificité** des sélecteurs :

| Sélecteur | Poids |
|---|---|
| `style="…"` dans le HTML | le plus fort |
| `#id` | fort |
| `.classe`, `:hover`, `[attribut]` | moyen |
| `p`, `h1` (balise) | faible |

À spécificité égale, **la dernière règle écrite l'emporte**.

```css
p { color: black; }
.note { color: green; }
p { color: gray; }
```

```html
<p class="note">Quelle couleur ?</p>
```

Ce paragraphe est **vert** : `.note` (une classe) est plus spécifique que `p` (une balise), quel que soit l'ordre. Un `<p>` sans classe serait **gris** : entre les deux règles `p`, la dernière l'emporte.

`!important` force une déclaration, mais rend le CSS très difficile à maintenir : réservez-le aux cas exceptionnels.

## À retenir

- `font-family` avec une police de secours, `line-height` sans unité.
- `rem` pour le texte et les espacements.
- Les propriétés de texte s'héritent.
- Spécificité : style en ligne > `#id` > `.classe` > balise ; à égalité, la dernière règle gagne.

## Exercices

### Exercice 1 — Prédisez la couleur

Avec `#titre { color: red; }` puis `.grand { color: blue; }`, de quelle couleur est `<h1 id="titre" class="grand">` ?

```solution-text
Rouge : un identifiant (#titre) est plus spécifique qu'une classe (.grand), même si la règle .grand est écrite après.
```

### Exercice 2 — Une base typographique

Écrivez des règles pour : texte de base en `system-ui` à 1 rem avec un interligne de 1,6 ; titres `h2` à 1,75 rem en gras.

```solution-css
body {
  font-family: system-ui, sans-serif;
  font-size: 1rem;
  line-height: 1.6;
}
h2 {
  font-size: 1.75rem;
  font-weight: 700;
}
```
"""

M3_L3 = r"""
## Tout est une boîte

Chaque élément affiché est une **boîte** composée de quatre zones, de l'intérieur vers l'extérieur :

1. le **contenu** (*content*) : texte, image ;
2. la **marge intérieure** (*padding*) : l'espace entre le contenu et la bordure ;
3. la **bordure** (*border*) ;
4. la **marge extérieure** (*margin*) : l'espace avec les autres éléments.

```css
.carte {
  width: 300px;
  padding: 1.5rem;
  border: 1px solid #d2d2d7;
  border-radius: 12px;
  margin: 1rem auto;
  background-color: #ffffff;
}
```

## Les raccourcis

```css
.exemple {
  margin: 10px;                 /* les 4 côtés */
  margin: 10px 20px;            /* haut-bas | gauche-droite */
  margin: 10px 20px 30px 40px;  /* haut | droite | bas | gauche (sens des aiguilles d'une montre) */
  margin-top: 2rem;             /* un seul côté */
  margin-inline: auto;          /* gauche et droite automatiques : centre un bloc de largeur définie */
}
```

## Le piège de la largeur : `box-sizing`

Par défaut, `width` ne s'applique qu'au **contenu** : padding et bordure s'ajoutent. Notre `.carte` de 300 px occupe en réalité 300 + 2 × 24 (padding) + 2 × 1 (bordure) = **350 px**.

La règle `box-sizing: border-box` intègre padding et bordure dans la largeur : la carte mesure alors exactement 300 px. On l'applique à toute la page, en tête de feuille de style :

```css
*, *::before, *::after {
  box-sizing: border-box;
}
```

## Bordures, coins et ombres

```css
.bouton {
  border: 2px solid #0B4BD6;
  border-radius: 999px;   /* forme de pilule */
  box-shadow: 0 4px 12px rgb(0 0 0 / 0.08);
}
.avatar {
  border-radius: 50%;      /* cercle (pour une image carrée) */
}
```

## Largeurs maximales

Pour un texte lisible, une ligne ne devrait pas dépasser 60 à 75 caractères. `max-width` limite la largeur sans empêcher l'élément de rétrécir sur un petit écran :

```css
.article {
  max-width: 65ch;     /* environ 65 caractères */
  margin-inline: auto; /* centré */
  padding-inline: 1rem;
}
```

## Observer les boîtes

Dans les outils de développement (**Inspecter**), l'onglet *Calculé* (*Computed*) dessine le modèle de boîte de l'élément sélectionné avec ses dimensions exactes : c'est l'outil idéal pour comprendre un espacement inattendu.

## À retenir

- Contenu → padding → border → margin.
- Raccourcis : 1, 2 ou 4 valeurs (haut, droite, bas, gauche).
- `box-sizing: border-box` pour que `width` inclue padding et bordure.
- `max-width` + `margin-inline: auto` pour centrer un bloc lisible.

## Exercices

### Exercice 1 — Calculez la largeur

Sans `box-sizing: border-box`, quelle est la largeur totale (hors margin) de `width: 200px; padding: 20px; border: 5px solid;` ? Et avec ?

```solution-text
Sans border-box : 200 + 2 × 20 + 2 × 5 = 250 px.
Avec border-box : 200 px (le padding et la bordure sont inclus dans les 200 px).
```

### Exercice 2 — Une carte

Écrivez une classe `.carte` : 1,5 rem d'espace intérieur, bordure grise de 1 px, coins arrondis de 16 px, ombre légère, largeur maximale de 24 rem, centrée.

```solution-css
.carte {
  max-width: 24rem;
  margin-inline: auto;
  padding: 1.5rem;
  border: 1px solid #d2d2d7;
  border-radius: 16px;
  box-shadow: 0 2px 8px rgb(0 0 0 / 0.08);
}
```
"""

M4_L1 = r"""
## La propriété `display`

`display` détermine comment un élément se place :

| Valeur | Comportement |
|---|---|
| `block` | nouvelle ligne, toute la largeur |
| `inline` | dans le texte ; `width` et `height` sont ignorés |
| `inline-block` | dans le texte, mais dimensions respectées |
| `none` | l'élément n'est pas affiché (ni lu par les lecteurs d'écran) |
| `flex` | conteneur Flexbox |
| `grid` | conteneur Grid |

## Flexbox : aligner sur un axe

**Flexbox** dispose les enfants d'un conteneur sur **une ligne** (ou une colonne) et gère leur alignement et leur répartition. C'est l'outil idéal pour une barre de navigation, une rangée de boutons ou une carte.

```html
<nav class="menu">
  <a href="/">Accueil</a>
  <a href="/formations">Formations</a>
  <a href="/tarifs">Tarifs</a>
</nav>
```

```css
.menu {
  display: flex;
  gap: 1rem;
  justify-content: center;
  align-items: center;
}
```

- `display: flex` sur le **parent** : ses enfants directs deviennent des éléments flexibles ;
- `gap` : espace entre les éléments ;
- `justify-content` : répartition sur l'**axe principal** (horizontal par défaut) ;
- `align-items` : alignement sur l'**axe secondaire** (vertical par défaut).

## Les valeurs de répartition

| `justify-content` | Effet |
|---|---|
| `flex-start` | groupés au début |
| `center` | centrés |
| `flex-end` | groupés à la fin |
| `space-between` | premier et dernier aux extrémités, espace égal entre eux |
| `space-around` / `space-evenly` | espaces répartis autour |

L'en-tête classique « logo à gauche, menu à droite » :

```css
.entete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}
```

## Changer d'axe et passer à la ligne

```css
.colonne {
  display: flex;
  flex-direction: column; /* empile verticalement */
  gap: .5rem;
}
.galerie {
  display: flex;
  flex-wrap: wrap;        /* passe à la ligne s'il manque de place */
  gap: 1rem;
}
```

Avec `flex-direction: column`, les axes s'inversent : `justify-content` agit verticalement, `align-items` horizontalement.

## Faire grandir les éléments

```css
.recherche {
  display: flex;
  gap: .5rem;
}
.recherche input {
  flex: 1;   /* prend toute la place restante */
}
```

`flex: 1` dit à l'élément d'occuper l'espace disponible. Si trois éléments ont `flex: 1`, ils se partagent la largeur à parts égales.

## Centrer parfaitement

```css
.centre {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

## À retenir

- `display: flex` sur le parent ; `gap` pour les espaces.
- `justify-content` (axe principal), `align-items` (axe secondaire).
- `flex-direction: column`, `flex-wrap: wrap`.
- `flex: 1` pour occuper l'espace restant.

## Exercices

### Exercice 1 — Barre d'en-tête

Écrivez le CSS d'un `<header class="entete">` contenant un logo et une `<nav>` : logo à gauche, navigation à droite, alignés verticalement.

```solution-css
.entete {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.5rem;
}
```

### Exercice 2 — Trois cartes égales

Trois `.carte` dans un `.rangee` doivent occuper chacune un tiers de la largeur, avec 1,5 rem entre elles, et passer à la ligne sur un écran étroit.

```solution-css
.rangee {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}
.carte {
  flex: 1 1 15rem; /* grandit, rétrécit, base de 15rem : passe à la ligne sous ~15rem */
}
```
"""

M4_L2 = r"""
## Grid : deux dimensions

Flexbox gère **un axe** ; **CSS Grid** gère les **lignes et les colonnes à la fois**. C'est l'outil idéal pour une grille de cartes ou la structure générale d'une page.

```css
.grille {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1.5rem;
}
```

- `grid-template-columns` définit les colonnes ;
- `fr` (*fraction*) partage l'espace disponible : `1fr 1fr 1fr` = trois colonnes égales, `2fr 1fr` = deux tiers / un tiers ;
- `gap` espace lignes et colonnes.

`repeat(3, 1fr)` est un raccourci pour `1fr 1fr 1fr`.

## La grille responsive en une ligne

```css
.catalogue {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1.5rem;
}
```

Cette ligne crée **autant de colonnes que possible**, chacune d'au moins 16 rem : 1 colonne sur un téléphone, 2 sur une tablette, 3 ou 4 sur un ordinateur, sans aucune media query. C'est la technique utilisée pour le catalogue de SMK Academy.

## Placer des éléments

Un élément peut s'étendre sur plusieurs cellules :

```css
.mise-en-avant {
  grid-column: span 2;   /* occupe deux colonnes */
}
.bandeau {
  grid-column: 1 / -1;   /* de la première à la dernière ligne de colonne : toute la largeur */
}
```

## Les zones nommées

Pour la structure d'une page, les **zones nommées** rendent le CSS très lisible :

```css
.page {
  display: grid;
  grid-template-columns: 14rem 1fr;
  grid-template-areas:
    "entete entete"
    "menu   contenu"
    "pied   pied";
  min-height: 100vh;
  gap: 1rem;
}
.page > header { grid-area: entete; }
.page > nav    { grid-area: menu; }
.page > main   { grid-area: contenu; }
.page > footer { grid-area: pied; }
```

## Flexbox ou Grid ?

| Besoin | Outil |
|---|---|
| Aligner des éléments sur une ligne (menu, boutons) | Flexbox |
| Contenu dont la taille dicte la disposition | Flexbox |
| Grille régulière (cartes, galerie) | Grid |
| Structure de page en lignes et colonnes | Grid |

Les deux se combinent : une grille de cartes (Grid) dont chaque carte aligne son contenu (Flexbox).

## À retenir

- `display: grid` + `grid-template-columns` + `gap`.
- `fr` partage l'espace ; `repeat(3, 1fr)`.
- `repeat(auto-fill, minmax(16rem, 1fr))` : grille responsive sans media query.
- `grid-column: span 2`, `grid-column: 1 / -1`, zones nommées.
- Flexbox pour une dimension, Grid pour deux.

## Exercices

### Exercice 1 — Galerie

Créez une galerie `.galerie` de 4 colonnes égales avec 1 rem d'écart.

```solution-css
.galerie {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
}
```

### Exercice 2 — Grille automatique

Modifiez la galerie pour qu'elle s'adapte seule à la largeur de l'écran, avec des images d'au moins 12 rem.

```solution-css
.galerie {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(12rem, 1fr));
  gap: 1rem;
}
```

### Exercice 3 — Le bon outil

Pour (a) une rangée de trois boutons centrés et (b) un tableau de bord avec un menu latéral et une zone principale, choisissez Flexbox ou Grid.

```solution-text
(a) Flexbox : une seule dimension (une rangée), justify-content: center.
(b) Grid : une structure en colonnes (menu + contenu) et en lignes (en-tête, pied).
```
"""

M4_L3 = r"""
## La propriété `position`

Par défaut, les éléments suivent le **flux normal** (`position: static`) : ils s'empilent les uns après les autres. `position` permet de sortir de ce flux pour des besoins précis.

| Valeur | Comportement | Usage typique |
|---|---|---|
| `static` | flux normal (défaut) | |
| `relative` | reste dans le flux, peut être décalé ; sert de **référence** aux enfants absolus | conteneur d'un badge |
| `absolute` | sort du flux, placé par rapport au plus proche ancêtre positionné | badge, icône sur une image |
| `fixed` | placé par rapport à la fenêtre, ne défile pas | bouton flottant, bannière |
| `sticky` | normal, puis « collé » quand on atteint un seuil au défilement | en-tête, barre de navigation |

On place l'élément avec `top`, `right`, `bottom`, `left` (ou `inset`).

## Un badge sur une carte

```html
<article class="carte">
  <span class="badge">Nouveau</span>
  <h3>Formation SQL</h3>
</article>
```

```css
.carte {
  position: relative;      /* référence pour le badge */
}
.badge {
  position: absolute;
  top: .75rem;
  right: .75rem;
}
```

Sans `position: relative` sur la carte, le badge se placerait par rapport à la page entière.

## Un en-tête collant

```css
.entete {
  position: sticky;
  top: 0;
  z-index: 10;
  background-color: rgb(255 255 255 / 0.85);
  -webkit-backdrop-filter: blur(12px);
  backdrop-filter: blur(12px);
}
```

L'en-tête défile normalement, puis reste en haut de l'écran. `backdrop-filter` floute ce qui passe en dessous (effet « verre dépoli ») ; le préfixe `-webkit-` est nécessaire pour Safari.

## La superposition : `z-index`

Quand des éléments positionnés se chevauchent, `z-index` décide lequel passe au-dessus : la valeur la plus grande l'emporte. Il ne fonctionne que sur les éléments positionnés (ou les enfants d'un conteneur flex ou grid).

Conseil : utilisez une petite échelle cohérente (1, 10, 100) plutôt que des valeurs comme 99999.

## Masquer un élément… intelligemment

| Technique | Visible | Lu par un lecteur d'écran |
|---|---|---|
| `display: none` | non | non |
| `visibility: hidden` | non (la place reste réservée) | non |
| classe « visuellement masquée » | non | **oui** |

La dernière technique sert à donner une information aux lecteurs d'écran sans l'afficher :

```css
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  overflow: hidden;
  clip-path: inset(50%);
  white-space: nowrap;
}
```

## À retenir

- `relative` sur le parent, `absolute` sur l'enfant pour placer un élément dans un autre.
- `sticky` + `top: 0` pour un en-tête collant ; `fixed` pour un élément fixe.
- `z-index` sur des éléments positionnés, avec une échelle simple.
- `.sr-only` pour un texte réservé aux lecteurs d'écran.

## Exercices

### Exercice 1 — Bouton flottant

Placez un bouton `.aide` en bas à droite de l'écran, à 1,5 rem des bords, qui reste visible pendant le défilement.

```solution-css
.aide {
  position: fixed;
  right: 1.5rem;
  bottom: 1.5rem;
  z-index: 10;
}
```

### Exercice 2 — Pourquoi ça ne marche pas ?

Un `.prix` en `position: absolute; top: 0; right: 0;` se retrouve en haut à droite de la page au lieu de sa carte. Pourquoi ?

```solution-text
Aucun ancêtre n'est positionné : l'élément absolu se place alors par rapport à la page.
Il faut ajouter position: relative; sur la carte qui le contient.
```
"""

M5_L1 = r"""
## Un site, tous les écrans

Plus de la moitié des visites se font sur mobile. Un site **responsive** s'adapte à toutes les largeurs d'écran, du téléphone au grand moniteur.

Première condition, déjà vue au module 1 : la balise viewport dans le `<head>`.

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Sans elle, le téléphone affiche la page comme sur un ordinateur, en tout petit.

## Mobile first

La méthode recommandée consiste à écrire d'abord le CSS **pour le mobile** (une colonne, simple), puis à **ajouter** des règles pour les écrans plus larges :

```css
.cartes {
  display: grid;
  gap: 1rem;                     /* mobile : une colonne */
}

@media (min-width: 48rem) {      /* à partir de 768 px environ */
  .cartes {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 64rem) {      /* à partir de 1024 px environ */
  .cartes {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

Une **media query** `@media (condition) { … }` n'applique ses règles que si la condition est vraie. Avec `min-width`, on part du petit écran et on enrichit progressivement.

## Des tailles fluides

- Largeurs en `%` ou `max-width` plutôt qu'en `px` fixes ;
- `clamp(min, idéal, max)` pour une taille qui varie entre deux bornes :

```css
h1 {
  font-size: clamp(2rem, 1.2rem + 4vw, 4rem);
}
```

Le titre mesure au moins 2 rem, au plus 4 rem, et grandit avec la largeur de l'écran entre les deux.

## Des images qui s'adaptent

```css
img {
  max-width: 100%;
  height: auto;
}
```

Ces deux lignes empêchent une image de déborder de son conteneur. Pour envoyer une image plus légère aux petits écrans, HTML propose `srcset` :

```html
<img src="photo-800.jpg"
     srcset="photo-400.jpg 400w, photo-800.jpg 800w, photo-1600.jpg 1600w"
     sizes="(min-width: 64rem) 50vw, 100vw"
     alt="Salle de formation SMK Academy" width="800" height="533" loading="lazy">
```

`loading="lazy"` ne charge l'image que lorsqu'elle approche de l'écran.

## Les zones tactiles

Sur mobile, on vise avec le doigt : les boutons et liens doivent mesurer au moins **44 × 44 px** et être suffisamment espacés.

## Tester

Les outils de développement proposent un **mode appareil** (icône téléphone, ou `Ctrl+Maj+M`) pour simuler différentes largeurs. Testez aussi sur un vrai téléphone : rien ne remplace le doigt.

## À retenir

- Balise viewport obligatoire.
- Mobile first : CSS de base pour le mobile, `@media (min-width: …)` pour les grands écrans.
- `max-width`, `%`, `clamp()` pour des tailles fluides.
- `img { max-width: 100%; height: auto; }`, `srcset`, `loading="lazy"`.
- Zones tactiles d'au moins 44 px.

## Exercices

### Exercice 1 — Navigation responsive

Sur mobile, les liens de `.menu` sont empilés ; à partir de 48 rem, ils sont alignés sur une ligne avec 2 rem d'écart. Écrivez le CSS en mobile first.

```solution-css
.menu {
  display: flex;
  flex-direction: column;
  gap: .5rem;
}

@media (min-width: 48rem) {
  .menu {
    flex-direction: row;
    gap: 2rem;
  }
}
```

### Exercice 2 — Titre fluide

Écrivez une taille de `h1` qui varie entre 1,75 rem et 3,5 rem selon la largeur de l'écran.

```solution-css
h1 {
  font-size: clamp(1.75rem, 1rem + 4vw, 3.5rem);
}
```
"""

M5_L2 = r"""
## Les variables CSS

Les **propriétés personnalisées** (variables CSS) évitent de répéter les mêmes valeurs et rendent un thème facile à modifier :

```css
:root {
  --couleur-principale: #0B4BD6;
  --couleur-succes: #00B386;
  --texte: #1d1d1f;
  --fond: #ffffff;
  --rayon: 14px;
  --espace: 1rem;
}

.bouton {
  background-color: var(--couleur-principale);
  color: #ffffff;
  border-radius: var(--rayon);
  padding: calc(var(--espace) * .75) var(--espace);
}
```

- on les déclare avec `--nom` (souvent sur `:root`, la racine de la page) ;
- on les utilise avec `var(--nom)` ;
- `calc()` permet de calculer à partir d'elles.

Changer `--couleur-principale` met à jour tous les éléments qui l'utilisent.

## Un thème sombre automatique

La media query `prefers-color-scheme` détecte le réglage du système de l'utilisateur. Avec des variables, le thème sombre tient en quelques lignes :

```css
@media (prefers-color-scheme: dark) {
  :root {
    --texte: #f5f5f7;
    --fond: #000000;
    --couleur-principale: #4C8DFF;
  }
}

body {
  color: var(--texte);
  background-color: var(--fond);
}
```

En thème sombre, une couleur vive est souvent éclaircie pour garder un bon contraste sur fond noir.

## Les transitions

Une **transition** anime le passage d'une valeur à une autre, par exemple au survol :

```css
.carte {
  transition: transform 200ms ease, box-shadow 200ms ease;
}
.carte:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgb(0 0 0 / 0.12);
}
```

- on indique les **propriétés** animées, la **durée** et la **courbe** (`ease`, `ease-out`, `linear`) ;
- `transform` (déplacement, échelle, rotation) et `opacity` sont les propriétés les plus performantes à animer.

## Respecter les préférences de mouvement

Certaines personnes souffrent de nausées face aux animations. Leur système peut le signaler ; respectez ce choix :

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}
```

C'est l'un des rares usages légitimes de `!important`.

## À retenir

- `:root { --nom: valeur; }` puis `var(--nom)` ; `calc()` pour calculer.
- `prefers-color-scheme: dark` + variables = thème sombre.
- `transition: propriété durée courbe` ; animer de préférence `transform` et `opacity`.
- Respecter `prefers-reduced-motion`.

## Exercices

### Exercice 1 — Un thème en variables

Déclarez trois variables (couleur d'accent, couleur de texte, rayon de 12 px) et utilisez-les dans une classe `.bouton`.

```solution-css
:root {
  --accent: #0B4BD6;
  --texte-inverse: #ffffff;
  --rayon: 12px;
}
.bouton {
  background-color: var(--accent);
  color: var(--texte-inverse);
  border-radius: var(--rayon);
}
```

### Exercice 2 — Survol animé

Faites légèrement grossir (`scale(1.03)`) un `.bouton` au survol, en 150 ms.

```solution-css
.bouton {
  transition: transform 150ms ease-out;
}
.bouton:hover {
  transform: scale(1.03);
}
```
"""

M5_L3 = r"""
## Le projet

Vous allez réaliser la **page de présentation d'un formateur indépendant** : responsive, accessible, avec un thème sombre automatique. Elle mobilise toute la formation.

Contenu attendu :

1. un en-tête avec le nom et une navigation vers les sections ;
2. une section d'accroche avec un titre et un bouton d'action ;
3. une grille de trois formations proposées ;
4. un formulaire de contact ;
5. un pied de page.

## Étape 1 — Le HTML

```html
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Sofia Rossi – Formatrice data</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header class="entete">
      <a class="logo" href="#">Sofia Rossi</a>
      <nav aria-label="Navigation principale">
        <ul class="menu">
          <li><a href="#formations">Formations</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
      </nav>
    </header>

    <main>
      <section class="accroche">
        <h1>Apprenez la data, simplement.</h1>
        <p>Des formations courtes et concrètes en SQL, Excel et Power BI.</p>
        <a class="bouton" href="#contact">Me contacter</a>
      </section>

      <section id="formations" aria-labelledby="titre-formations">
        <h2 id="titre-formations">Formations</h2>
        <div class="grille">
          <article class="carte">
            <h3>SQL pour débutants</h3>
            <p>Interroger une base de données en une journée.</p>
          </article>
          <article class="carte">
            <h3>Excel avancé</h3>
            <p>Tableaux croisés dynamiques et formules utiles.</p>
          </article>
          <article class="carte">
            <h3>Power BI</h3>
            <p>Créer un tableau de bord clair et interactif.</p>
          </article>
        </div>
      </section>

      <section id="contact" aria-labelledby="titre-contact">
        <h2 id="titre-contact">Contact</h2>
        <form class="formulaire" action="https://formspree.io/f/votre-identifiant" method="post">
          <label for="nom">Nom</label>
          <input id="nom" name="nom" autocomplete="name" required>
          <label for="email">Email</label>
          <input id="email" name="email" type="email" autocomplete="email" required>
          <label for="message">Message</label>
          <textarea id="message" name="message" rows="5" required></textarea>
          <button class="bouton" type="submit">Envoyer</button>
        </form>
      </section>
    </main>

    <footer class="pied">
      <p>© 2026 Sofia Rossi</p>
    </footer>
  </body>
</html>
```

## Étape 2 — Le CSS

```css
*, *::before, *::after { box-sizing: border-box; }

:root {
  --accent: #0B4BD6;
  --texte: #1d1d1f;
  --texte-2: #515154;
  --fond: #ffffff;
  --fond-2: #f5f5f7;
  --rayon: 16px;
}

@media (prefers-color-scheme: dark) {
  :root {
    --accent: #4C8DFF;
    --texte: #f5f5f7;
    --texte-2: #a1a1a6;
    --fond: #000000;
    --fond-2: #1c1c1e;
  }
}

body {
  margin: 0;
  font-family: system-ui, sans-serif;
  line-height: 1.6;
  color: var(--texte);
  background-color: var(--fond);
}

main > section {
  max-width: 64rem;
  margin-inline: auto;
  padding: 3rem 1.25rem;
}

.entete {
  position: sticky;
  top: 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: .75rem 1.25rem;
  background-color: var(--fond);
  border-bottom: 1px solid var(--fond-2);
}
.logo { font-weight: 700; color: var(--texte); text-decoration: none; }
.menu { display: flex; gap: 1.25rem; margin: 0; padding: 0; list-style: none; }
.menu a { color: var(--texte-2); text-decoration: none; }
.menu a:hover { color: var(--accent); }

.accroche { text-align: center; }
.accroche h1 { font-size: clamp(2rem, 1.2rem + 4vw, 3.5rem); line-height: 1.1; margin-bottom: .5rem; }
.accroche p { color: var(--texte-2); font-size: 1.15rem; }

.bouton {
  display: inline-block;
  min-height: 44px;
  padding: .7rem 1.4rem;
  border: 0;
  border-radius: 999px;
  background-color: var(--accent);
  color: #ffffff;
  font: inherit;
  font-weight: 600;
  text-decoration: none;
  cursor: pointer;
  transition: transform 150ms ease-out;
}
.bouton:hover { transform: scale(1.03); }
.bouton:focus-visible { outline: 3px solid var(--accent); outline-offset: 3px; }

.grille {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(16rem, 1fr));
  gap: 1.25rem;
}
.carte {
  padding: 1.5rem;
  border-radius: var(--rayon);
  background-color: var(--fond-2);
}
.carte h3 { margin-top: 0; }

.formulaire { display: grid; gap: .5rem; max-width: 32rem; }
.formulaire input, .formulaire textarea {
  font: inherit;
  padding: .7rem;
  border: 1px solid var(--texte-2);
  border-radius: 10px;
  background-color: var(--fond);
  color: var(--texte);
}
.formulaire button { justify-self: start; margin-top: .5rem; }

.pied { text-align: center; padding: 2rem; color: var(--texte-2); }

@media (prefers-reduced-motion: reduce) {
  .bouton { transition: none; }
}
```

## Étape 3 — Vérifier

Avant de publier, passez cette liste :

- [ ] le validateur HTML du W3C ne signale aucune erreur ;
- [ ] la page est utilisable au clavier, et le focus est toujours visible ;
- [ ] l'audit Lighthouse (*Accessibility*) dépasse 90 ;
- [ ] la page s'affiche correctement de 320 px à 1 440 px de large ;
- [ ] le thème sombre reste lisible (contrastes).

## Étape 4 — Publier gratuitement

Un site statique (HTML + CSS) se publie gratuitement en quelques minutes : déposez le dossier sur **Netlify Drop** (glisser-déposer), ou publiez-le avec **GitHub Pages** depuis un dépôt GitHub. Vous obtenez une adresse publique à partager.

Le formulaire de cet exemple utilise un service tiers (Formspree) pour recevoir les messages par email ; remplacez `votre-identifiant` par celui fourni lors de votre inscription, ou retirez l'attribut `action` pour un simple exercice.

## À retenir

- Partir d'un HTML sémantique, puis le mettre en forme avec des variables CSS.
- Grid pour la grille, Flexbox pour l'en-tête, `clamp()` pour le titre.
- Vérifier : validateur, clavier, Lighthouse, tailles d'écran, thème sombre.
- Un site statique se publie gratuitement (Netlify, GitHub Pages).
"""

QUIZ_M3 = [
    ("single", "Comment relier une feuille de style style.css à une page ?", None,
     ["<style src=\"style.css\">", "<link rel=\"stylesheet\" href=\"style.css\">", "<css>style.css</css>", "<script src=\"style.css\">"], [1],
     "La balise <link rel=\"stylesheet\" href=\"…\"> se place dans le <head>."),
    ("single", "Quel sélecteur cible les éléments ayant la classe « alerte » ?", None,
     ["#alerte", ".alerte", "alerte", "*alerte"], [1],
     "Le point désigne une classe ; le dièse désigne un identifiant."),
    ("single", "Avec « p { color: black; } » puis « .note { color: green; } », de quelle couleur est <p class=\"note\"> ?", None,
     ["Noir", "Vert", "Ça dépend du navigateur", "Aucune couleur"], [1],
     "Une classe est plus spécifique qu'une balise : la règle .note l'emporte."),
    ("single", "À spécificité égale, quelle règle s'applique ?", None,
     ["La première écrite", "La dernière écrite", "La plus courte", "Aucune"], [1],
     "C'est le principe de la cascade : à égalité, la dernière règle l'emporte."),
    ("single", "Quelle unité respecte la taille de police choisie par l'utilisateur dans son navigateur ?", None,
     ["px", "rem", "cm", "pt"], [1],
     "rem dépend de la taille de police de la racine, que l'utilisateur peut modifier."),
    ("single", "Dans quel ordre se trouvent les zones du modèle de boîte, de l'intérieur vers l'extérieur ?", None,
     ["margin, border, padding, contenu", "contenu, padding, border, margin", "contenu, margin, border, padding", "padding, contenu, border, margin"], [1],
     "Contenu, puis marge intérieure (padding), bordure, et marge extérieure (margin)."),
    ("single", "Sans box-sizing: border-box, quelle est la largeur totale de width: 100px; padding: 10px; border: 2px solid ?", None,
     ["100 px", "112 px", "124 px", "120 px"], [2],
     "100 + 2 × 10 + 2 × 2 = 124 px. Avec border-box, l'élément mesurerait 100 px."),
    ("single", "Que fait margin: 10px 20px; ?", None,
     ["10 px en haut, 20 px en bas", "10 px en haut et en bas, 20 px à gauche et à droite", "10 px à gauche, 20 px à droite", "10 px partout sauf 20 px en haut"], [1],
     "Avec deux valeurs : la première pour haut et bas, la seconde pour gauche et droite."),
    ("multiple", "Quelles propriétés s'héritent des parents par défaut ?", None,
     ["color", "font-family", "margin", "border"], [0, 1],
     "Les propriétés de texte (color, font-family, line-height…) s'héritent ; les propriétés de boîte non."),
    ("single", "Quel sélecteur cible un bouton qui a reçu le focus au clavier ?", None,
     ["button:hover", "button:focus-visible", "button:active", "button::before"], [1],
     ":focus-visible cible le focus clavier : indispensable pour l'accessibilité."),
]

QUIZ_M4 = [
    ("single", "Sur quel élément applique-t-on display: flex ?", None,
     ["Sur chaque enfant", "Sur le conteneur parent", "Sur le <body> uniquement", "Sur le <head>"], [1],
     "display: flex s'applique au parent ; ses enfants directs deviennent des éléments flexibles."),
    ("single", "Quelle propriété répartit les éléments sur l'axe principal d'un conteneur flex ?", None,
     ["align-items", "justify-content", "flex-wrap", "text-align"], [1],
     "justify-content agit sur l'axe principal ; align-items sur l'axe secondaire."),
    ("single", "Quelle valeur place un logo à gauche et un menu à droite ?", None,
     ["justify-content: center", "justify-content: space-between", "align-items: stretch", "flex-direction: column"], [1],
     "space-between place le premier élément au début, le dernier à la fin."),
    ("single", "Que fait flex: 1 sur un élément flexible ?", None,
     ["Il le masque", "Il occupe l'espace restant disponible", "Il le place en premier", "Il fixe sa largeur à 1 px"], [1],
     "flex: 1 permet à l'élément de grandir pour occuper l'espace disponible."),
    ("single", "Que signifie grid-template-columns: 2fr 1fr ?", None,
     ["Deux colonnes de 2 px et 1 px", "Deux colonnes : deux tiers et un tiers de l'espace", "Trois colonnes égales", "Une colonne de 21 fractions"], [1],
     "fr partage l'espace disponible : 2fr + 1fr = 3 parts, soit 2/3 et 1/3."),
    ("single", "Que permet repeat(auto-fill, minmax(16rem, 1fr)) ?", None,
     ["Une seule colonne fixe", "Autant de colonnes que possible, d'au moins 16 rem chacune", "16 colonnes", "Une grille qui ne change jamais"], [1],
     "La grille crée automatiquement le nombre de colonnes adapté à la largeur disponible."),
    ("single", "Que fait grid-column: 1 / -1 ?", None,
     ["Masque l'élément", "L'étend sur toute la largeur de la grille", "Le place dans la dernière colonne", "Inverse les colonnes"], [1],
     "De la première à la dernière ligne de colonne : l'élément occupe toute la largeur."),
    ("single", "Pour placer un badge dans le coin d'une carte, quelle combinaison utiliser ?", None,
     ["position: absolute sur la carte, relative sur le badge", "position: relative sur la carte, absolute sur le badge", "position: fixed sur les deux", "float: right sur le badge"], [1],
     "Le badge absolu se place par rapport au plus proche ancêtre positionné : la carte en relative."),
    ("single", "Quelle valeur garde un en-tête visible en haut de l'écran pendant le défilement, après sa position normale ?", None,
     ["position: static", "position: sticky; top: 0", "position: absolute", "display: block"], [1],
     "sticky laisse l'élément dans le flux, puis le colle en haut une fois le seuil atteint."),
    ("multiple", "Quels cas se prêtent bien à Flexbox ?", None,
     ["Une barre de navigation horizontale", "Une rangée de boutons centrés", "Une structure de page en lignes et colonnes avec zones nommées", "Aligner l'icône et le texte d'un bouton"], [0, 1, 3],
     "Flexbox gère une dimension ; une structure de page en deux dimensions relève plutôt de Grid."),
]

QUIZ_M5 = [
    ("single", "Que permet la balise <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"> ?", None,
     ["D'accélérer le chargement", "D'adapter l'affichage à la largeur de l'écran mobile", "D'activer le thème sombre", "D'améliorer le référencement uniquement"], [1],
     "Sans elle, les téléphones affichent la page comme sur un ordinateur, en réduction."),
    ("single", "Dans une démarche mobile first, quelle media query utilise-t-on surtout ?", None,
     ["@media (max-width: …)", "@media (min-width: …)", "@media print", "@media (orientation: portrait) uniquement"], [1],
     "On écrit d'abord le CSS mobile, puis on enrichit avec min-width pour les écrans plus larges."),
    ("single", "Que fait font-size: clamp(2rem, 1rem + 4vw, 4rem) ?", None,
     ["Une taille fixe de 2 rem", "Une taille qui varie avec l'écran, entre 2 rem et 4 rem", "Une taille de 4 rem sur mobile", "Une erreur"], [1],
     "clamp(min, idéal, max) borne une valeur fluide entre un minimum et un maximum."),
    ("single", "Quelles règles empêchent une image de déborder de son conteneur ?", None,
     ["width: 100vw", "max-width: 100%; height: auto;", "overflow: scroll", "display: none"], [1],
     "max-width: 100% limite la largeur ; height: auto conserve les proportions."),
    ("single", "Que fait loading=\"lazy\" sur une image ?", None,
     ["Elle est chargée en basse qualité", "Elle n'est chargée que lorsqu'elle approche de l'écran", "Elle est chargée après 5 secondes", "Elle est masquée"], [1],
     "Le chargement différé économise de la bande passante pour les images hors de l'écran."),
    ("single", "Comment utilise-t-on une variable CSS déclarée avec --accent: #0B4BD6 ?", None,
     ["color: $accent;", "color: var(--accent);", "color: --accent;", "color: @accent;"], [1],
     "Les propriétés personnalisées se lisent avec var(--nom)."),
    ("single", "Quelle media query détecte le thème sombre du système ?", None,
     ["@media (theme: dark)", "@media (prefers-color-scheme: dark)", "@media (dark-mode)", "@media (color: black)"], [1],
     "prefers-color-scheme reflète le réglage clair ou sombre de l'utilisateur."),
    ("single", "Quelles propriétés sont les plus performantes à animer ?", None,
     ["width et height", "transform et opacity", "margin et padding", "top et left"], [1],
     "transform et opacity sont gérées efficacement par le navigateur, sans recalcul de mise en page."),
    ("single", "Quelle est la taille minimale recommandée d'une zone tactile ?", None,
     ["16 × 16 px", "24 × 24 px", "44 × 44 px", "100 × 100 px"], [2],
     "Environ 44 × 44 px permettent de viser facilement avec le doigt."),
    ("true_false", "Il faut respecter prefers-reduced-motion en réduisant ou supprimant les animations.", None,
     ["Vrai", "Faux"], [0],
     "Certaines personnes sont gênées par les animations : leur réglage système doit être respecté."),
]
