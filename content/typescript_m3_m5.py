"""Modules 3 à 5 de « TypeScript » (importé par content/typescript.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Interfaces, types et classes
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Déclarer une interface

Une **interface** décrit la **forme** d'un objet, comme un alias `type` d'objet. Elle se lit comme un **contrat** : « tout objet de ce type possède ces propriétés ».

```ts
interface Formation {
  titre: string;
  dureeHeures: number;
  niveau: "debutant" | "intermediaire" | "avance";
  description?: string;
}

const ts: Formation = { titre: "TypeScript", dureeHeures: 8, niveau: "intermediaire" };
console.log(`${ts.titre} — ${ts.dureeHeures} h (${ts.niveau})`);
```

```text
TypeScript — 8 h (intermediaire)
```

On y retrouve tout ce que vous connaissez : propriétés optionnelles `?`, `readonly`, unions, types littéraux.

## Méthodes dans une interface

Une interface peut décrire des **méthodes**, c'est-à-dire des fonctions attachées à l'objet :

```ts
interface Compteur {
  valeur: number;
  incrementer(pas?: number): void;
  reinitialiser(): void;
}

const visites: Compteur = {
  valeur: 0,
  incrementer(pas = 1) {
    this.valeur += pas;
  },
  reinitialiser() {
    this.valeur = 0;
  },
};

visites.incrementer();
visites.incrementer(5);
console.log(visites.valeur);
visites.reinitialiser();
console.log(visites.valeur);
```

```text
6
0
```

Si l'objet oublie une méthode promise par l'interface, l'erreur est immédiate :

```ts
interface Compteur {
  valeur: number;
  incrementer(): void;
}
const c: Compteur = { valeur: 0 };
```

```text
error TS2741: Property 'incrementer' is missing in type '{ valeur: number; }' but required in type 'Compteur'.
```

## Étendre une interface

Le mot-clé `extends` crée une interface **à partir d'une autre**, en ajoutant des propriétés :

```ts
interface Personne {
  prenom: string;
  nom: string;
}

interface Formateur extends Personne {
  specialites: string[];
}

const claire: Formateur = { prenom: "Claire", nom: "Roux", specialites: ["TypeScript", "React"] };
console.log(`${claire.prenom} ${claire.nom} : ${claire.specialites.join(", ")}`);
```

```text
Claire Roux : TypeScript, React
```

Une interface peut étendre **plusieurs** interfaces : `interface Tuteur extends Personne, Disponible { … }`.

## Composer avec l'intersection `&`

Avec les alias `type`, on obtient le même résultat grâce à l'**intersection** `A & B` : un objet qui possède **à la fois** les propriétés de A et celles de B.

```ts
type Horodatage = { creeLe: string; modifieLe: string };
type Article = { titre: string; contenu: string };
type ArticleStocke = Article & Horodatage & { id: number };

const a: ArticleStocke = {
  id: 7,
  titre: "Bien débuter",
  contenu: "…",
  creeLe: "2026-01-10",
  modifieLe: "2026-02-03",
};
console.log(`#${a.id} ${a.titre} (modifié le ${a.modifieLe})`);
```

```text
#7 Bien débuter (modifié le 2026-02-03)
```

> Ne confondez pas : l'**union** `A | B` est « l'un ou l'autre » (moins de propriétés garanties), l'**intersection** `A & B` est « les deux à la fois » (plus de propriétés exigées).

## `interface` ou `type` ?

Pour décrire un objet, les deux conviennent et se comportent presque pareil. Les différences pratiques :

| | `interface` | `type` |
|---|---|---|
| Décrire un objet | oui | oui |
| Union, littéraux, tuples, types de fonctions | non | oui |
| Étendre | `extends` | intersection `&` |
| Déclarer deux fois le même nom | les déclarations **fusionnent** | erreur |
| Messages d'erreur | affichent le nom de l'interface | affichent souvent le nom de l'alias |

La **fusion de déclarations** (*declaration merging*) signifie que deux `interface Config { … }` du même nom s'additionnent. C'est utile pour compléter les types d'une bibliothèque, mais surprenant par accident.

> Règle simple et répandue : **`interface` pour les formes d'objets** que l'on étend ou que d'autres implémentent (classes), **`type` pour tout le reste** (unions, littéraux, fonctions, combinaisons). Surtout, soyez cohérent dans un même projet.

## Le typage structurel

TypeScript compare les types par leur **structure**, pas par leur nom. Un objet est accepté s'il possède **au moins** les propriétés demandées, avec les bons types :

```ts
interface Nommable {
  nom: string;
}

function etiquette(x: Nommable): string {
  return `<${x.nom}>`;
}

const ville = { nom: "Lille", habitants: 236000 };
console.log(etiquette(ville));
```

```text
<Lille>
```

`ville` n'a jamais été déclarée comme `Nommable`, mais elle en a la forme : elle est acceptée. On parle parfois de « typage canard » (*duck typing*) : si ça a la forme d'un canard, c'est un canard. La vérification des propriétés **en trop** vue au module 2 ne s'applique qu'aux littéraux d'objets écrits directement à l'endroit de l'affectation ou de l'appel.

## Types de fonctions et signatures d'index dans une interface

Une interface peut aussi décrire un dictionnaire :

```ts
interface Traductions {
  [cle: string]: string;
}

const fr: Traductions = { bonjour: "Bonjour", merci: "Merci" };
fr["auRevoir"] = "Au revoir";
console.log(Object.keys(fr).length, fr.merci);
```

```text
3 Merci
```

## À retenir

- `interface Nom { … }` décrit la forme d'un objet, méthodes comprises.
- `extends` étend une interface ; `&` combine des alias de type.
- Union `|` = l'un ou l'autre ; intersection `&` = les deux à la fois.
- `interface` pour les objets extensibles, `type` pour unions et combinaisons ; restez cohérent.
- Typage structurel : seule la forme compte, pas le nom du type.

## Exercices

### Exercice 1 — Interface Salle

Déclarez une interface `Salle` (nom, capacite, equipements : tableau de chaînes, `etage` optionnel) et une fonction `peutAccueillir(s: Salle, participants: number): boolean`. Testez avec une salle de 20 places pour 25 participants.

```solution-ts
interface Salle {
  nom: string;
  capacite: number;
  equipements: string[];
  etage?: number;
}

function peutAccueillir(s: Salle, participants: number): boolean {
  return participants <= s.capacite;
}

const b204: Salle = { nom: "B204", capacite: 20, equipements: ["vidéoprojecteur"] };
console.log(peutAccueillir(b204, 25));
```

```text
false
```

### Exercice 2 — Étendre

Créez `interface Vehicule { marque: string; roues: number }` puis `interface Camion extends Vehicule { chargeMaxKg: number }`. Créez un camion et affichez une phrase le décrivant.

```solution-ts
interface Vehicule {
  marque: string;
  roues: number;
}

interface Camion extends Vehicule {
  chargeMaxKg: number;
}

const porteur: Camion = { marque: "Transalpe", roues: 6, chargeMaxKg: 12000 };
console.log(`${porteur.marque} : ${porteur.roues} roues, ${porteur.chargeMaxKg} kg`);
```

```text
Transalpe : 6 roues, 12000 kg
```

### Exercice 3 — Union ou intersection ?

Avec `type A = { x: number }` et `type B = { y: number }`, quelles propriétés peut-on lire sans test sur une valeur de type `A | B` ? Et sur `A & B` ?

```solution-text
A | B : aucune des deux sans test, car la valeur peut n'avoir que x ou que y
(il faut rétrécir, par exemple avec "x" in v).
A & B : x et y, car la valeur possède les deux propriétés à la fois.
```
"""

M3_L2 = r"""
## Une classe typée

Les **classes** de JavaScript fonctionnent en TypeScript, avec en plus la déclaration du type de chaque **propriété** :

```ts
class CompteBancaire {
  titulaire: string;
  solde: number;

  constructor(titulaire: string, soldeInitial: number) {
    this.titulaire = titulaire;
    this.solde = soldeInitial;
  }

  deposer(montant: number): void {
    this.solde += montant;
  }

  resume(): string {
    return `${this.titulaire} : ${this.solde.toFixed(2)} €`;
  }
}

const compte = new CompteBancaire("Inès Morel", 100);
compte.deposer(50);
console.log(compte.resume());
```

```text
Inès Morel : 150.00 €
```

En mode strict, chaque propriété doit être **initialisée** dans sa déclaration ou dans le constructeur. Un oubli est signalé :

```ts
class Produit {
  nom: string;
  prix: number;
  constructor(nom: string) {
    this.nom = nom;
  }
}
```

```text
error TS2564: Property 'prix' has no initializer and is not definitely assigned in the constructor.
```

## Visibilité : `public`, `private`, `protected`

TypeScript ajoute des **modificateurs d'accès** :

| Modificateur | Accessible depuis |
|---|---|
| `public` (par défaut) | partout |
| `protected` | la classe et ses sous-classes |
| `private` | la classe uniquement |

```ts
class CompteBancaire {
  private solde = 0;

  deposer(montant: number): void {
    if (montant <= 0) {
      throw new Error("Le montant doit être positif");
    }
    this.solde += montant;
  }

  consulter(): number {
    return this.solde;
  }
}

const compte = new CompteBancaire();
compte.deposer(80);
console.log(compte.consulter());
```

```text
80
```

Accéder directement au solde depuis l'extérieur est refusé :

```ts
class CompteBancaire {
  private solde = 0;
}
const compte = new CompteBancaire();
compte.solde = 1000000;
```

```text
error TS2341: Property 'solde' is private and only accessible within class 'CompteBancaire'.
```

C'est l'**encapsulation** : on oblige à passer par `deposer`, qui contrôle les montants.

> `private` est vérifié **à la compilation seulement**. JavaScript propose ses propres champs privés, écrits avec un dièse (`#solde`), réellement inaccessibles à l'exécution. Les deux existent ; `#` offre la garantie la plus forte, `private` est très répandu dans le code existant.

## `readonly` et les propriétés de paramètres

Une propriété `readonly` ne peut être affectée que dans sa déclaration ou dans le constructeur. TypeScript propose aussi un raccourci : un modificateur placé **devant un paramètre du constructeur** déclare et initialise la propriété en une fois.

```ts
class Etudiant {
  constructor(
    public readonly matricule: string,
    public prenom: string,
    private notes: number[] = [],
  ) {}

  ajouterNote(note: number): void {
    this.notes.push(note);
  }

  moyenne(): number {
    if (this.notes.length === 0) return 0;
    return this.notes.reduce((s, n) => s + n, 0) / this.notes.length;
  }
}

const e = new Etudiant("E-2026-001", "Yanis");
e.ajouterNote(14);
e.ajouterNote(17);
console.log(`${e.prenom} (${e.matricule}) : ${e.moyenne()}`);
```

```text
Yanis (E-2026-001) : 15.5
```

Ces **propriétés de paramètres** (*parameter properties*) sont très courantes dans le code TypeScript existant. Comme les `enum`, elles génèrent du code (les affectations `this.matricule = matricule`) : les outils qui se contentent d'effacer les types ne les acceptent pas (module 5). La forme longue reste toujours possible.

## Accesseurs `get` et `set`

Un **accesseur** ressemble à une propriété mais exécute une fonction : idéal pour une valeur calculée ou une modification contrôlée.

```ts
class Temperature {
  #celsius = 0;

  get celsius(): number {
    return this.#celsius;
  }

  set celsius(valeur: number) {
    if (valeur < -273.15) {
      throw new Error("Température impossible");
    }
    this.#celsius = valeur;
  }

  get fahrenheit(): number {
    return this.#celsius * 9 / 5 + 32;
  }
}

const t = new Temperature();
t.celsius = 25;
console.log(t.celsius, t.fahrenheit);
try {
  t.celsius = -300;
} catch (e) {
  console.log(e instanceof Error ? e.message : e);
}
```

```text
25 77
Température impossible
```

Un `get` sans `set` correspondant donne une propriété en **lecture seule** : `t.fahrenheit = 100` serait refusé par TypeScript.

## Membres statiques

Un membre `static` appartient à la **classe elle-même**, pas à chaque objet : compteur partagé, constantes, fonctions de fabrication.

```ts
class Ticket {
  static prochainNumero = 1;
  readonly numero: number;

  constructor(public sujet: string) {
    this.numero = Ticket.prochainNumero;
    Ticket.prochainNumero++;
  }

  static depuisTexte(texte: string): Ticket {
    return new Ticket(texte.trim());
  }
}

const t1 = new Ticket("Connexion impossible");
const t2 = Ticket.depuisTexte("  Facture en double  ");
console.log(t1.numero, t1.sujet);
console.log(t2.numero, t2.sujet);
```

```text
1 Connexion impossible
2 Facture en double
```

## Une classe est aussi un type

Le nom d'une classe s'utilise directement comme type : `function afficher(t: Ticket)`. Rappelez-vous que le typage est **structurel** : un objet littéral ayant les mêmes membres publics serait aussi accepté… sauf si la classe contient des membres `private` ou `#`, qui rendent ses instances uniques.

## À retenir

- Les propriétés d'une classe se déclarent avec leur type et doivent être initialisées.
- `public` (défaut), `protected`, `private` : vérifiés à la compilation ; `#champ` : privé réel à l'exécution.
- `constructor(public readonly id: string)` déclare et initialise une propriété en une ligne.
- `get` / `set` pour les valeurs calculées ou contrôlées ; `static` pour ce qui appartient à la classe.

## Exercices

### Exercice 1 — Panier

Écrivez une classe `Panier` avec une propriété privée `articles` (tableau de `{ nom: string; prix: number }`), une méthode `ajouter(nom, prix)` et un accesseur `total`. Ajoutez deux articles et affichez le total.

```solution-ts
class Panier {
  private articles: { nom: string; prix: number }[] = [];

  ajouter(nom: string, prix: number): void {
    this.articles.push({ nom, prix });
  }

  get total(): number {
    return this.articles.reduce((s, a) => s + a.prix, 0);
  }
}

const panier = new Panier();
panier.ajouter("Clavier", 39.9);
panier.ajouter("Souris", 19.9);
console.log(panier.total.toFixed(2));
```

```text
59.80
```

### Exercice 2 — Version courte

Réécrivez cette classe avec des propriétés de paramètres : `class Point { x: number; y: number; constructor(x: number, y: number) { this.x = x; this.y = y; } }`. Ajoutez une méthode `distanceOrigine()`.

```solution-ts
class Point {
  constructor(public x: number, public y: number) {}

  distanceOrigine(): number {
    return Math.hypot(this.x, this.y);
  }
}

console.log(new Point(3, 4).distanceOrigine());
```

```text
5
```

### Exercice 3 — Quel message ?

Quelle erreur `tsc` produit-il pour `class A { private secret = 1 } console.log(new A().secret);` ?

```solution-text
error TS2341: Property 'secret' is private and only accessible within class 'A'.
La propriété est privée : seule la classe A peut la lire. Il faudrait ajouter une méthode
publique (ou un accesseur get) qui renvoie la valeur.
```
"""

M3_L3 = r"""
## Implémenter une interface : `implements`

Une classe peut s'engager à respecter une interface avec `implements`. TypeScript vérifie alors que **tous les membres promis** sont présents.

```ts
interface Notifiable {
  envoyer(message: string): string;
}

class NotificationEmail implements Notifiable {
  constructor(private adresse: string) {}

  envoyer(message: string): string {
    return `Email à ${this.adresse} : ${message}`;
  }
}

class NotificationSms implements Notifiable {
  constructor(private numero: string) {}

  envoyer(message: string): string {
    return `SMS au ${this.numero} : ${message.slice(0, 20)}`;
  }
}

const canaux: Notifiable[] = [
  new NotificationEmail("lea@exemple.fr"),
  new NotificationSms("0601020304"),
];
for (const canal of canaux) {
  console.log(canal.envoyer("Votre formation commence demain à 9 h"));
}
```

```text
Email à lea@exemple.fr : Votre formation commence demain à 9 h
SMS au 0601020304 : Votre formation comm
```

Le tableau `canaux` contient des objets de classes différentes, tous manipulés à travers l'interface `Notifiable` : c'est le **polymorphisme**. Le code qui envoie les messages n'a pas besoin de connaître chaque classe.

Si une méthode manque, l'erreur désigne la classe fautive :

```ts
interface Notifiable {
  envoyer(message: string): string;
}
class NotificationPush implements Notifiable {}
```

```text
error TS2420: Class 'NotificationPush' incorrectly implements interface 'Notifiable'.
```

Une classe peut implémenter plusieurs interfaces : `class A implements B, C { … }`.

## Hériter d'une classe : `extends`

L'**héritage** crée une classe à partir d'une autre : la sous-classe reçoit les propriétés et méthodes de la classe parente et peut en ajouter ou en **redéfinir**.

```ts
class Employe {
  constructor(public nom: string, protected salaireMensuel: number) {}

  salaireAnnuel(): number {
    return this.salaireMensuel * 12;
  }

  presentation(): string {
    return `${this.nom}, ${this.salaireAnnuel()} € par an`;
  }
}

class Manager extends Employe {
  constructor(nom: string, salaireMensuel: number, private prime: number) {
    super(nom, salaireMensuel);
  }

  override salaireAnnuel(): number {
    return super.salaireAnnuel() + this.prime;
  }
}

const equipe: Employe[] = [new Employe("Hugo", 2500), new Manager("Nadia", 3500, 6000)];
for (const personne of equipe) {
  console.log(personne.presentation());
}
```

```text
Hugo, 30000 € par an
Nadia, 48000 € par an
```

Points clés :

- `super(...)` appelle le constructeur parent ; il doit précéder toute utilisation de `this` ;
- `super.salaireAnnuel()` appelle la version parente de la méthode ;
- `protected salaireMensuel` est accessible dans `Manager`, mais pas depuis l'extérieur ;
- `override` indique explicitement que la méthode **redéfinit** celle du parent.

> Le mot-clé `override` est facultatif par défaut. Avec l'option `noImplicitOverride` (module 5), il devient obligatoire : si la méthode parente est renommée, TypeScript signale alors toutes les redéfinitions devenues orphelines, au lieu de les laisser créer silencieusement une nouvelle méthode.

Une faute de frappe dans une méthode marquée `override` est détectée :

```ts
class Employe {
  salaireAnnuel(): number {
    return 30000;
  }
}
class Stagiaire extends Employe {
  override salaireAnuel(): number {
    return 6000;
  }
}
```

```text
error TS4117: This member cannot have an 'override' modifier because it is not declared in the base class 'Employe'. Did you mean 'salaireAnnuel'?
```

## Les classes abstraites

Une classe **abstraite** (`abstract`) sert uniquement de **modèle** : on ne peut pas l'instancier, et elle peut déclarer des méthodes abstraites, sans corps, que chaque sous-classe **doit** fournir.

```ts
abstract class Forme {
  constructor(public readonly nom: string) {}

  abstract aire(): number;

  description(): string {
    return `${this.nom} d'aire ${this.aire().toFixed(2)}`;
  }
}

class Disque extends Forme {
  constructor(private rayon: number) {
    super("Disque");
  }
  aire(): number {
    return Math.PI * this.rayon ** 2;
  }
}

class Rectangle extends Forme {
  constructor(private largeur: number, private hauteur: number) {
    super("Rectangle");
  }
  aire(): number {
    return this.largeur * this.hauteur;
  }
}

const formes: Forme[] = [new Disque(2), new Rectangle(3, 4.5)];
for (const f of formes) {
  console.log(f.description());
}
```

```text
Disque d'aire 12.57
Rectangle d'aire 13.50
```

`description()` est écrite **une seule fois** dans la classe abstraite et appelle `aire()`, dont chaque sous-classe fournit sa version. Instancier la classe abstraite est refusé :

```ts
abstract class Forme {
  abstract aire(): number;
}
const f = new Forme();
```

```text
error TS2511: Cannot create an instance of an abstract class.
```

## Interface, classe abstraite ou union ?

| Besoin | Outil |
|---|---|
| Décrire un contrat, sans code commun | `interface` + `implements` |
| Partager du code commun et imposer certaines méthodes | `abstract class` + `extends` |
| Ensemble **fermé** de variantes connues à l'avance | union discriminée (module 2) |

> Préférez la **composition** à l'héritage profond : au-delà de deux niveaux d'héritage, le code devient difficile à suivre. Un objet qui *contient* un autre objet (un `Notifiable` passé au constructeur, par exemple) est souvent plus souple qu'un objet qui en *hérite*.

## Composition : injecter une dépendance

```ts
interface Journal {
  ecrire(ligne: string): void;
}

class JournalConsole implements Journal {
  ecrire(ligne: string): void {
    console.log(`[log] ${ligne}`);
  }
}

class ServiceInscription {
  constructor(private journal: Journal) {}

  inscrire(prenom: string, formation: string): void {
    this.journal.ecrire(`${prenom} inscrit(e) à ${formation}`);
  }
}

const service = new ServiceInscription(new JournalConsole());
service.inscrire("Maëlle", "TypeScript");
```

```text
[log] Maëlle inscrit(e) à TypeScript
```

`ServiceInscription` ne dépend que de l'interface `Journal` : on peut lui fournir un journal en fichier, ou un faux journal pendant les tests, sans modifier sa classe.

## À retenir

- `implements` vérifie qu'une classe respecte une interface ; on manipule ensuite les objets via l'interface.
- `extends` hérite d'une classe ; `super(...)` appelle le constructeur parent.
- `override` signale une redéfinition (obligatoire avec `noImplicitOverride`).
- `abstract class` : non instanciable, impose des méthodes abstraites aux sous-classes.
- Préférez la composition (dépendances passées au constructeur) à l'héritage profond.

## Exercices

### Exercice 1 — Implémenter

Écrivez `interface Convertisseur { convertir(montant: number): number }` et deux classes `EnDollars` (taux passé au constructeur) et `SansConversion`. Appliquez-les à 100.

```solution-ts
interface Convertisseur {
  convertir(montant: number): number;
}

class EnDollars implements Convertisseur {
  constructor(private taux: number) {}
  convertir(montant: number): number {
    return montant * this.taux;
  }
}

class SansConversion implements Convertisseur {
  convertir(montant: number): number {
    return montant;
  }
}

const convertisseurs: Convertisseur[] = [new EnDollars(1.5), new SansConversion()];
for (const c of convertisseurs) {
  console.log(c.convertir(100));
}
```

```text
150
100
```

Le taux 1,5 est fictif : un vrai taux de change varie en permanence.

### Exercice 2 — Classe abstraite

Créez `abstract class Abonnement` avec une méthode abstraite `prixMensuel(): number` et une méthode `prixAnnuel()` qui renvoie 12 fois le prix mensuel. Créez `AbonnementEtudiant` (9 € par mois) et affichez son prix annuel.

```solution-ts
abstract class Abonnement {
  abstract prixMensuel(): number;

  prixAnnuel(): number {
    return this.prixMensuel() * 12;
  }
}

class AbonnementEtudiant extends Abonnement {
  prixMensuel(): number {
    return 9;
  }
}

console.log(new AbonnementEtudiant().prixAnnuel());
```

```text
108
```

### Exercice 3 — Héritage ou union ?

Une application gère trois types de paiements fixes (carte, virement, espèces) avec des données différentes, et aucun code partagé. Que choisir ?

```solution-text
Une union discriminée (type Paiement = { mode: "carte"; … } | { mode: "virement"; … } | { mode: "especes" }) :
l'ensemble est fermé et connu, il n'y a pas de code commun à partager, et le switch sur mode
avec vérification d'exhaustivité (never) garantit qu'aucun cas n'est oublié.
```
"""

# ---------------------------------------------------------------------------
# Module 4 — Génériques et types utilitaires
# ---------------------------------------------------------------------------
M4_L1 = r"""
## Le problème : réutiliser sans perdre le type

Écrivons une fonction qui renvoie le premier élément d'un tableau. Avec `any`, elle accepte tout… mais le résultat perd son type :

```ts
function premierAny(liste: any[]): any {
  return liste[0];
}
const p = premierAny(["Paris", "Lyon"]);
console.log(p.toFixed(2));
```

```text
TypeError: p.toFixed is not a function
```

Ce code compile, puis plante à l'exécution : TypeScript ne sait plus que `p` est une chaîne. Écrire une version par type (`premierTexte`, `premierNombre`…) serait absurde.

## Les génériques

Un **générique** est une fonction (ou un type) **paramétrée par un type**. On déclare un **paramètre de type**, noté par convention `T`, entre chevrons :

```ts
function premier<T>(liste: T[]): T | undefined {
  return liste[0];
}

const ville = premier(["Paris", "Lyon"]);
const note = premier([12, 18]);
console.log(ville?.toUpperCase(), note?.toFixed(1));
```

```text
PARIS 12.0
```

Lisez `premier<T>(liste: T[]): T | undefined` ainsi : « pour un type `T` quelconque, la fonction reçoit un tableau de `T` et renvoie un `T` ou `undefined` ». À chaque appel, TypeScript **infère** `T` à partir de l'argument : `string` pour le premier, `number` pour le second. Le lien entre l'entrée et la sortie est conservé.

Le type de retour inclut `undefined` car un tableau vide n'a pas de premier élément. TypeScript nous l'impose ensuite, d'où les `?.`.

On peut aussi préciser `T` explicitement, rarement utile :

```ts
function premier<T>(liste: T[]): T | undefined {
  return liste[0];
}
const vide = premier<string>([]);
console.log(vide ?? "aucun élément");
```

```text
aucun élément
```

## Plusieurs paramètres de type

```ts
function paire<A, B>(a: A, b: B): [A, B] {
  return [a, b];
}

function inverser<A, B>(p: [A, B]): [B, A] {
  return [p[1], p[0]];
}

const p = paire("Emma", 16);
const inversee = inverser(p);
console.log(p, inversee);
```

```text
[ 'Emma', 16 ] [ 16, 'Emma' ]
```

`p` est de type `[string, number]`, `inversee` de type `[number, string]` : tout est déduit.

## Les contraintes : `extends`

Parfois, la fonction a besoin que `T` possède certaines propriétés. Une **contrainte** `T extends …` restreint les types acceptés :

```ts
function plusLong<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(plusLong("chat", "éléphant"));
console.log(plusLong([1, 2, 3], [4]));
```

```text
éléphant
[ 1, 2, 3 ]
```

Chaînes et tableaux ont une propriété `length` : ils sont acceptés. Un nombre ne l'est pas :

```ts
function plusLong<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}
console.log(plusLong(10, 20));
```

```text
error TS2345: Argument of type 'number' is not assignable to parameter of type '{ length: number; }'.
```

> Ici, `extends` ne veut pas dire « hériter » : il signifie « doit être compatible avec ».

## `keyof` : les clés d'un type

L'opérateur `keyof` produit l'union des **noms de propriétés** d'un type :

```ts
type Livre = { titre: string; auteur: string; annee: number };
type CleLivre = keyof Livre; // "titre" | "auteur" | "annee"

const tri: CleLivre = "annee";
console.log(tri);
```

```text
annee
```

Combiné aux génériques, il permet d'écrire des fonctions qui manipulent des propriétés **sans faute de frappe possible**. `T[K]` désigne le type de la propriété `K` de `T` (*type d'accès indexé*) :

```ts
function lire<T, K extends keyof T>(objet: T, cle: K): T[K] {
  return objet[cle];
}

const livre = { titre: "Le Code clair", auteur: "Paul Nadal", annee: 2019 };
const annee = lire(livre, "annee");
console.log(annee + 1);
console.log(lire(livre, "titre").toUpperCase());
```

```text
2020
LE CODE CLAIR
```

`lire(livre, "annee")` est de type `number`, `lire(livre, "titre")` de type `string`. Et une clé inexistante est refusée :

```ts
function lire<T, K extends keyof T>(objet: T, cle: K): T[K] {
  return objet[cle];
}
const livre = { titre: "Le Code clair", annee: 2019 };
lire(livre, "editeur");
```

```text
error TS2345: Argument of type '"editeur"' is not assignable to parameter of type '"annee" | "titre"'.
```

## Un exemple utile : trier par propriété

```ts
function trierPar<T, K extends keyof T>(liste: T[], cle: K): T[] {
  return [...liste].sort((a, b) => (a[cle] < b[cle] ? -1 : a[cle] > b[cle] ? 1 : 0));
}

const stagiaires = [
  { prenom: "Zoé", age: 23 },
  { prenom: "Adam", age: 31 },
  { prenom: "Lina", age: 19 },
];

console.log(trierPar(stagiaires, "age").map((s) => s.prenom));
console.log(trierPar(stagiaires, "prenom").map((s) => s.prenom));
```

```text
[ 'Lina', 'Zoé', 'Adam' ]
[ 'Adam', 'Lina', 'Zoé' ]
```

`[...liste]` copie le tableau, car `sort` modifie le tableau sur place. Le même code trie n'importe quel tableau d'objets, par n'importe quelle propriété existante.

## À retenir

- `function f<T>(x: T): T` : un paramètre de type, inféré à chaque appel.
- Les génériques conservent le lien entre types d'entrée et de sortie, contrairement à `any`.
- `T extends Contrainte` exige que `T` possède certaines propriétés.
- `keyof T` = union des clés ; `T[K]` = type de la propriété `K`.
- `<T, K extends keyof T>` : accès à une propriété vérifié et typé.

## Exercices

### Exercice 1 — dernier

Écrivez `dernier<T>(liste: T[]): T | undefined` et testez-la avec `[3, 7, 9]` et `[]`.

```solution-ts
function dernier<T>(liste: T[]): T | undefined {
  return liste[liste.length - 1];
}
console.log(dernier([3, 7, 9]));
console.log(dernier([]));
```

```text
9
undefined
```

### Exercice 2 — Extraire une colonne

Écrivez `colonne<T, K extends keyof T>(liste: T[], cle: K): T[K][]` qui renvoie les valeurs d'une propriété pour chaque objet. Testez avec une liste de produits et la clé `"prix"`.

```solution-ts
function colonne<T, K extends keyof T>(liste: T[], cle: K): T[K][] {
  return liste.map((element) => element[cle]);
}

const produits = [
  { nom: "Stylo", prix: 1.5 },
  { nom: "Cahier", prix: 3 },
];
const prix = colonne(produits, "prix");
console.log(prix, prix.reduce((s, p) => s + p, 0));
```

```text
[ 1.5, 3 ] 4.5
```

### Exercice 3 — Contrainte

Écrivez `afficherNom<T extends { nom: string }>(x: T): string` qui renvoie `Nom : …`. Pourquoi l'appel `afficherNom({ titre: "A" })` est-il refusé ?

```solution-ts
function afficherNom<T extends { nom: string }>(x: T): string {
  return `Nom : ${x.nom}`;
}
console.log(afficherNom({ nom: "Atelier Leroy", ville: "Brest" }));
// afficherNom({ titre: "A" }) est refusé : l'objet n'a pas de propriété nom de type string,
// il ne respecte donc pas la contrainte { nom: string }.
```

```text
Nom : Atelier Leroy
```
"""

M4_L2 = r"""
## Des types génériques

Les alias de type et les interfaces peuvent eux aussi avoir des paramètres de type. Un exemple très utile : un **résultat** qui est soit un succès avec une valeur, soit un échec avec un message.

```ts
type Resultat<T> =
  | { ok: true; valeur: T }
  | { ok: false; erreur: string };

function convertirAge(saisie: string): Resultat<number> {
  const age = Number(saisie);
  if (!Number.isInteger(age) || age < 0) {
    return { ok: false, erreur: `« ${saisie} » n'est pas un âge valide` };
  }
  return { ok: true, valeur: age };
}

for (const saisie of ["34", "trente"]) {
  const r = convertirAge(saisie);
  if (r.ok) {
    console.log(`Âge : ${r.valeur}`);
  } else {
    console.log(`Erreur : ${r.erreur}`);
  }
}
```

```text
Âge : 34
Erreur : « trente » n'est pas un âge valide
```

`Resultat<T>` est une **union discriminée générique** (discriminant : `ok`) : le même type sert pour un `Resultat<number>`, un `Resultat<Utilisateur>`… Ce motif oblige l'appelant à traiter l'échec, sans passer par des exceptions.

## Interfaces génériques

```ts
interface Page<T> {
  elements: T[];
  page: number;
  totalPages: number;
}

type Cours = { titre: string };

const page1: Page<Cours> = {
  elements: [{ titre: "TypeScript" }, { titre: "React" }],
  page: 1,
  totalPages: 3,
};
console.log(`Page ${page1.page}/${page1.totalPages} : ${page1.elements.map((c) => c.titre).join(", ")}`);
```

```text
Page 1/3 : TypeScript, React
```

Vous utilisez déjà des types génériques : `Array<T>`, `Record<K, V>`, `Map<K, V>`, `Set<T>`, `Promise<T>`.

```ts
const inscrits = new Map<string, number>();
inscrits.set("typescript", 42);
inscrits.set("react", 17);
console.log(inscrits.get("typescript"), inscrits.get("go"));

const tags = new Set<string>(["web", "typage", "web"]);
console.log(tags.size);
```

```text
42 undefined
2
```

`inscrits.get(...)` est typé `number | undefined` : la clé peut être absente.

## Valeur par défaut d'un paramètre de type

```ts
interface Reponse<T = string> {
  statut: number;
  corps: T;
}

const texte: Reponse = { statut: 200, corps: "OK" };
const json: Reponse<{ id: number }> = { statut: 201, corps: { id: 9 } };
console.log(texte.corps, json.corps.id);
```

```text
OK 9
```

## Classes génériques

```ts
class Pile<T> {
  private elements: T[] = [];

  empiler(element: T): void {
    this.elements.push(element);
  }

  depiler(): T | undefined {
    return this.elements.pop();
  }

  get taille(): number {
    return this.elements.length;
  }
}

const historique = new Pile<string>();
historique.empiler("/accueil");
historique.empiler("/formations");
historique.empiler("/formations/typescript");
console.log(historique.depiler());
console.log(historique.taille);
```

```text
/formations/typescript
2
```

Une `Pile<string>` refuse tout ce qui n'est pas une chaîne :

```ts
class Pile<T> {
  private elements: T[] = [];
  empiler(element: T): void {
    this.elements.push(element);
  }
}
const historique = new Pile<string>();
historique.empiler(404);
```

```text
error TS2345: Argument of type 'number' is not assignable to parameter of type 'string'.
```

## Le code asynchrone : `Promise<T>`

Une fonction `async` renvoie toujours une **promesse**. Son type de retour s'écrit `Promise<T>`, où `T` est le type de la valeur obtenue avec `await`.

```ts
type Utilisateur = { id: number; prenom: string };

function attendre(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function chargerUtilisateur(id: number): Promise<Utilisateur> {
  await attendre(50); // simule un appel réseau
  if (id <= 0) {
    throw new Error(`Utilisateur ${id} introuvable`);
  }
  return { id, prenom: "Aya" };
}

async function principal(): Promise<void> {
  const u = await chargerUtilisateur(3);
  console.log(`${u.id} : ${u.prenom}`);
  try {
    await chargerUtilisateur(0);
  } catch (e) {
    console.log(e instanceof Error ? e.message : "Erreur inconnue");
  }
}

principal();
```

```text
3 : Aya
Utilisateur 0 introuvable
```

Après `await`, `u` est de type `Utilisateur` : l'autocomplétion fonctionne. Oublier le `await` est une erreur classique que TypeScript attrape souvent :

```ts
type Utilisateur = { id: number; prenom: string };
async function chargerUtilisateur(id: number): Promise<Utilisateur> {
  return { id, prenom: "Aya" };
}
async function principal(): Promise<void> {
  const u = chargerUtilisateur(3);
  console.log(u.prenom);
}
```

```text
error TS2339: Property 'prenom' does not exist on type 'Promise<Utilisateur>'.
```

## Typer une réponse `fetch`

`reponse.json()` renvoie `Promise<any>` : TypeScript ne peut pas connaître la forme des données envoyées par un serveur. Plutôt que d'écrire `as Utilisateur` (une affirmation **non vérifiée**), récupérez la valeur en `unknown` et validez-la avec un prédicat de type (module 2) :

```ts
type Utilisateur = { id: number; prenom: string };

function estUtilisateur(v: unknown): v is Utilisateur {
  return typeof v === "object" && v !== null
    && "id" in v && typeof v.id === "number"
    && "prenom" in v && typeof v.prenom === "string";
}

async function chargerDepuisApi(url: string): Promise<Utilisateur> {
  const reponse = await fetch(url);
  if (!reponse.ok) {
    throw new Error(`Erreur HTTP ${reponse.status}`);
  }
  const donnees: unknown = await reponse.json();
  if (!estUtilisateur(donnees)) {
    throw new Error("Réponse inattendue du serveur");
  }
  return donnees;
}
```

> L'opérateur `as` (*assertion de type*) dit à TypeScript « fais-moi confiance ». Il ne convertit rien et ne vérifie rien à l'exécution. Réservez-le aux cas où vous en savez réellement plus que le compilateur.

## À retenir

- `type Resultat<T> = …`, `interface Page<T>`, `class Pile<T>` : types paramétrés.
- `Array<T>`, `Map<K, V>`, `Set<T>`, `Promise<T>` sont des types génériques standards.
- Un paramètre de type peut avoir une valeur par défaut : `<T = string>`.
- Une fonction `async` renvoie `Promise<T>` ; `await` donne un `T`.
- Données d'API : `unknown` + validation, plutôt que `as`.

## Exercices

### Exercice 1 — File d'attente

Écrivez une classe générique `File<T>` avec `ajouter(e: T)`, `retirer(): T | undefined` (premier arrivé, premier servi) et un accesseur `vide`. Testez avec des numéros de ticket.

```solution-ts
class FileAttente<T> {
  private elements: T[] = [];

  ajouter(e: T): void {
    this.elements.push(e);
  }

  retirer(): T | undefined {
    return this.elements.shift();
  }

  get vide(): boolean {
    return this.elements.length === 0;
  }
}

const tickets = new FileAttente<number>();
tickets.ajouter(101);
tickets.ajouter(102);
console.log(tickets.retirer(), tickets.vide);
console.log(tickets.retirer(), tickets.vide);
```

```text
101 false
102 true
```

La classe est nommée `FileAttente` : dans un fichier sans `import` ni `export`, le nom `File` entrerait en conflit avec le type `File` déjà défini par le navigateur.

### Exercice 2 — Resultat générique

Avec `type Resultat<T> = { ok: true; valeur: T } | { ok: false; erreur: string }`, écrivez `diviser(a: number, b: number): Resultat<number>`, puis affichez le résultat de `diviser(9, 3)` et `diviser(1, 0)`.

```solution-ts
type Resultat<T> = { ok: true; valeur: T } | { ok: false; erreur: string };

function diviser(a: number, b: number): Resultat<number> {
  if (b === 0) return { ok: false, erreur: "division par zéro" };
  return { ok: true, valeur: a / b };
}

for (const r of [diviser(9, 3), diviser(1, 0)]) {
  console.log(r.ok ? `= ${r.valeur}` : `Erreur : ${r.erreur}`);
}
```

```text
= 3
Erreur : division par zéro
```

### Exercice 3 — Promesse typée

Écrivez `async function doubleApres(n: number, ms: number): Promise<number>` qui attend `ms` millisecondes puis renvoie `n * 2`. Affichez le résultat pour `21`.

```solution-ts
function attendre(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function doubleApres(n: number, ms: number): Promise<number> {
  await attendre(ms);
  return n * 2;
}

doubleApres(21, 30).then((resultat) => console.log(resultat));
```

```text
42
```
"""

M4_L3 = r"""
## Transformer des types existants

Les **types utilitaires** (*utility types*) sont des types génériques fournis par TypeScript pour **dériver** un type d'un autre, au lieu de le réécrire. Partons d'un modèle :

```ts
interface Utilisateur {
  id: number;
  email: string;
  prenom: string;
  motDePasseHache: string;
  creeLe: string;
}
```

## `Partial<T>` et `Required<T>`

`Partial<T>` rend **toutes** les propriétés optionnelles : parfait pour une mise à jour partielle.

```ts
interface Utilisateur {
  id: number;
  email: string;
  prenom: string;
}

function mettreAJour(u: Utilisateur, modifs: Partial<Utilisateur>): Utilisateur {
  return { ...u, ...modifs };
}

const avant: Utilisateur = { id: 1, email: "nina@exemple.fr", prenom: "Nina" };
const apres = mettreAJour(avant, { prenom: "Nina-Rose" });
console.log(apres);
```

```text
{ id: 1, email: 'nina@exemple.fr', prenom: 'Nina-Rose' }
```

`Required<T>` fait l'inverse : toutes les propriétés deviennent obligatoires.

## `Readonly<T>`

`Readonly<T>` rend toutes les propriétés en lecture seule :

```ts
type Config = { theme: string; langue: string };
const config: Readonly<Config> = { theme: "sombre", langue: "fr" };
config.langue = "en";
```

```text
error TS2540: Cannot assign to 'langue' because it is a read-only property.
```

## `Pick<T, K>` et `Omit<T, K>`

`Pick` **garde** certaines propriétés, `Omit` en **retire** :

```ts
interface Utilisateur {
  id: number;
  email: string;
  prenom: string;
  motDePasseHache: string;
}

type ProfilPublic = Pick<Utilisateur, "id" | "prenom">;
type NouvelUtilisateur = Omit<Utilisateur, "id" | "motDePasseHache"> & { motDePasse: string };

function profilPublic(u: Utilisateur): ProfilPublic {
  return { id: u.id, prenom: u.prenom };
}

const u: Utilisateur = { id: 7, email: "omar@exemple.fr", prenom: "Omar", motDePasseHache: "(empreinte)" };
console.log(profilPublic(u));

const formulaire: NouvelUtilisateur = { email: "jade@exemple.fr", prenom: "Jade", motDePasse: "(saisie)" };
console.log(Object.keys(formulaire));
```

```text
{ id: 7, prenom: 'Omar' }
[ 'email', 'prenom', 'motDePasse' ]
```

Ce découpage a un intérêt de **sécurité** : en typant la réponse d'une API `ProfilPublic`, vous rendez visible toute tentative d'y ajouter l'empreinte du mot de passe. Rappel : les types ne filtrent rien à l'exécution ; c'est la fonction `profilPublic`, qui construit un nouvel objet, qui retire réellement les champs sensibles. Et un mot de passe ne se stocke jamais en clair : seule une empreinte calculée par un algorithme de hachage adapté est conservée.

## `Record<K, V>` avec des clés fermées

Vous connaissez `Record<string, number>`. Avec une union de littéraux comme clés, TypeScript exige **chaque** clé :

```ts
type Niveau = "debutant" | "intermediaire" | "avance";

const libelles: Record<Niveau, string> = {
  debutant: "Débutant",
  intermediaire: "Intermédiaire",
  avance: "Avancé",
};
console.log(libelles.intermediaire);
```

```text
Intermédiaire
```

Si l'on ajoute `"expert"` à `Niveau`, chaque `Record<Niveau, …>` incomplet devient une erreur : impossible d'oublier un libellé.

## `Exclude`, `Extract` et `NonNullable`

Ces utilitaires agissent sur des **unions** :

```ts
type Statut = "brouillon" | "publie" | "archive" | "supprime";

type StatutVisible = Exclude<Statut, "archive" | "supprime">; // "brouillon" | "publie"
type StatutFinal = Extract<Statut, "archive" | "supprime">;   // "archive" | "supprime"
type Valeur = NonNullable<string | null | undefined>;          // string

const s: StatutVisible = "publie";
const f: StatutFinal = "archive";
const v: Valeur = "ok";
console.log(s, f, v);
```

```text
publie archive ok
```

## `ReturnType` et `Parameters`

Ces deux utilitaires extraient les types d'une **fonction** existante :

```ts
function creerSession(utilisateurId: number, dureeMinutes: number) {
  return { utilisateurId, expireDans: dureeMinutes * 60, jeton: "(jeton factice)" };
}

type Session = ReturnType<typeof creerSession>;
type ArgsSession = Parameters<typeof creerSession>; // [utilisateurId: number, dureeMinutes: number]

const args: ArgsSession = [12, 30];
const s: Session = creerSession(...args);
console.log(s.expireDans);
```

```text
1800
```

Notez `typeof creerSession` : en position de type, **`typeof` donne le type d'une valeur** existante (ici, le type de la fonction). C'est une autre utilisation que le `typeof` de JavaScript, qui renvoie une chaîne à l'exécution.

## `typeof` + `keyof` sur un objet constant

Combinés avec `as const`, ils permettent de dériver un type d'une **valeur unique de référence** :

```ts
const ROLES = {
  admin: "Administrateur",
  formateur: "Formateur",
  etudiant: "Étudiant",
} as const;

type Role = keyof typeof ROLES; // "admin" | "formateur" | "etudiant"

function libelleRole(r: Role): string {
  return ROLES[r];
}
console.log(libelleRole("formateur"));
```

```text
Formateur
```

Ajouter un rôle dans l'objet met automatiquement le type `Role` à jour : une seule source de vérité.

## L'opérateur `satisfies`

Annoter une variable remplace son type inféré par le type annoté, ce qui fait parfois perdre de la précision. `satisfies` **vérifie** qu'une valeur respecte un type **sans** changer le type inféré :

```ts
type Couleur = string | [number, number, number];

const palette = {
  primaire: "#0071e3",
  succes: [52, 199, 89],
} satisfies Record<string, Couleur>;

console.log(palette.primaire.toUpperCase());
console.log(palette.succes.join(", "));
```

```text
#0071E3
52, 199, 89
```

Avec `const palette: Record<string, Couleur> = …`, `palette.primaire` serait de type `Couleur` (chaîne **ou** tuple) et `toUpperCase()` serait refusé. Avec `satisfies`, TypeScript vérifie la conformité **et** garde les types précis : `string` pour `primaire`, tuple pour `succes`. Une couleur mal formée est signalée :

```ts
type Couleur = string | [number, number, number];
const palette = {
  alerte: [255, 59],
} satisfies Record<string, Couleur>;
```

```text
error TS2322: Type '[number, number]' is not assignable to type 'Couleur'.
```

## Récapitulatif

| Utilitaire | Effet |
|---|---|
| `Partial<T>` / `Required<T>` | tout optionnel / tout obligatoire |
| `Readonly<T>` | tout en lecture seule |
| `Pick<T, K>` / `Omit<T, K>` | garder / retirer des propriétés |
| `Record<K, V>` | objet aux clés `K` et valeurs `V` |
| `Exclude<U, X>` / `Extract<U, X>` | retirer / garder des membres d'une union |
| `NonNullable<T>` | retirer `null` et `undefined` |
| `ReturnType<F>` / `Parameters<F>` | type de retour / tuple des paramètres |

## À retenir

- Dérivez les types au lieu de les recopier : une modification du modèle se propage partout.
- `Pick` / `Omit` pour des vues partielles (formulaires, réponses d'API).
- `typeof valeur` en position de type, `keyof typeof OBJET` pour une liste de clés.
- `satisfies` vérifie sans élargir le type inféré.

## Exercices

### Exercice 1 — Brouillon

Avec `interface Article { id: number; titre: string; contenu: string; publieLe: string }`, définissez `Brouillon` = un article sans `id` ni `publieLe`, dont toutes les propriétés sont optionnelles. Créez un brouillon avec seulement un titre.

```solution-ts
interface Article {
  id: number;
  titre: string;
  contenu: string;
  publieLe: string;
}

type Brouillon = Partial<Omit<Article, "id" | "publieLe">>;

const b: Brouillon = { titre: "Pourquoi typer ?" };
console.log(b);
```

```text
{ titre: 'Pourquoi typer ?' }
```

### Exercice 2 — Tarifs complets

Avec `type Formule = "mensuelle" | "annuelle"`, déclarez `const tarifs: Record<Formule, number>` (12 et 120) et affichez l'économie annuelle par rapport à 12 mois de formule mensuelle.

```solution-ts
type Formule = "mensuelle" | "annuelle";

const tarifs: Record<Formule, number> = { mensuelle: 12, annuelle: 120 };
console.log(tarifs.mensuelle * 12 - tarifs.annuelle);
```

```text
24
```

Les tarifs sont fictifs ; si l'on oubliait la clé `annuelle`, `tsc` refuserait l'objet.

### Exercice 3 — Dériver d'une constante

À partir de `const MODES = ["carte", "virement", "especes"] as const;`, définissez le type `Mode` correspondant à l'une des valeurs, puis vérifiez qu'une saisie est un `Mode` valide avec une fonction `estMode(v: string): v is Mode`.

```solution-ts
const MODES = ["carte", "virement", "especes"] as const;
type Mode = (typeof MODES)[number]; // "carte" | "virement" | "especes"

function estMode(v: string): v is Mode {
  return (MODES as readonly string[]).includes(v);
}

console.log(estMode("virement"), estMode("chèque"));
```

```text
true false
```

`(typeof MODES)[number]` signifie « le type d'un élément quelconque du tableau ». La conversion `as readonly string[]` est nécessaire car `includes` sur un tableau de littéraux n'accepte que ces littéraux.
"""

# ---------------------------------------------------------------------------
# Module 5 — Configurer un projet TypeScript
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Le fichier `tsconfig.json`

Jusqu'ici, on compilait un fichier à la fois. Un vrai projet contient de nombreux fichiers et un fichier de configuration, **`tsconfig.json`**, placé à la racine : il indique à `tsc` **quels fichiers** compiler et **comment**.

```bash
mkdir mon-projet && cd mon-projet
npm init -y
npm install --save-dev typescript
npx tsc --init        # crée un tsconfig.json commenté
```

`tsc --init` génère un fichier abondamment commenté, dont le contenu exact dépend de la version de TypeScript : lisez-le, puis gardez les options dont vous avez besoin. Voici une configuration claire pour un projet Node.js, que nous allons expliquer :

```json
{
  "compilerOptions": {
    "target": "es2022",
    "module": "nodenext",
    "rootDir": "src",
    "outDir": "dist",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "noEmitOnError": true,
    "sourceMap": true,
    "skipLibCheck": true
  },
  "include": ["src"]
}
```

Une fois ce fichier en place, la commande `npx tsc`, **sans nom de fichier**, compile tout le projet. On l'ajoute souvent aux scripts de `package.json` :

```json
{
  "type": "module",
  "scripts": {
    "build": "tsc",
    "typecheck": "tsc --noEmit",
    "start": "node dist/index.js"
  }
}
```

`tsc --noEmit` vérifie les types **sans produire** de fichiers : pratique en intégration continue ou quand un autre outil se charge de produire le JavaScript.

## Où sont les fichiers : `include`, `rootDir`, `outDir`

| Option | Rôle |
|---|---|
| `include` | les fichiers à compiler (ici tout le dossier `src`) |
| `rootDir` | la racine des sources ; la structure des dossiers est reproduite dans `outDir` |
| `outDir` | le dossier où sont écrits les `.js` (souvent `dist` ou `build`) |

Avec cette configuration, `src/index.ts` devient `dist/index.js`, et `src/modeles/cours.ts` devient `dist/modeles/cours.js`. Le dossier `dist` est généré : on ne le modifie jamais à la main et on l'ajoute au `.gitignore`.

## Quel JavaScript produire : `target` et `module`

- **`target`** : la version de JavaScript produite. Une version récente (`es2022` ou plus) convient à Node.js et aux navigateurs actuels. Avec une cible ancienne, `tsc` réécrit certaines syntaxes modernes.
- **`module`** : le système de modules produit. Pour Node.js, `nodenext` suit les règles de Node (modules ES ou CommonJS selon le champ `type` du `package.json`). Pour une application web assemblée par un outil comme Vite, on rencontre plutôt `"module": "esnext"` avec `"moduleResolution": "bundler"`.
- **`lib`** : les définitions de types disponibles (`"dom"` pour le navigateur, par exemple). Elle découle de `target` si on ne la précise pas.

> Les valeurs par défaut et les options disponibles évoluent selon les versions de TypeScript : certaines options anciennes ont été dépréciées puis retirées (`tsc` l'indique alors clairement). En cas de doute, consultez `npx tsc --help --all` et la documentation de votre version, et vérifiez votre version avec `npx tsc --version`.

## Le mode strict

`"strict": true` active d'un coup une **famille** d'options de vérification. Les plus importantes :

| Option incluse dans `strict` | Effet |
|---|---|
| `strictNullChecks` | `null` et `undefined` sont des types à part (module 1) |
| `noImplicitAny` | refuse les `any` implicites (paramètres non typés) |
| `strictPropertyInitialization` | propriétés de classe obligatoirement initialisées |
| `strictFunctionTypes` | vérification plus stricte des types de fonctions |
| `useUnknownInCatchVariables` | `catch (e)` donne un `e` de type `unknown` |
| `alwaysStrict` | produit du JavaScript en mode strict (`"use strict"`) |

Les versions récentes de TypeScript activent `strict` par défaut, mais **écrivez-le explicitement** : votre configuration reste claire et ne dépend pas de la version installée. Voici ce que `noImplicitAny` refuse :

```ts
function doubler(x) {
  return x * 2;
}
console.log(doubler(4));
```

```text
error TS7006: Parameter 'x' implicitly has an 'any' type.
```

> Sur un nouveau projet, activez `strict` dès le premier jour : ajouter la rigueur plus tard oblige à corriger des centaines d'erreurs d'un coup. Sur un ancien projet JavaScript, on peut migrer progressivement (option `allowJs`, puis fichier par fichier).

## Aller plus loin que `strict`

Certaines options utiles ne font **pas** partie de `strict` :

- **`noUncheckedIndexedAccess`** : `tableau[i]` et `dictionnaire[cle]` sont typés `T | undefined`, car l'élément peut ne pas exister ;
- **`noImplicitOverride`** : `override` obligatoire pour redéfinir une méthode (module 3) ;
- **`noFallthroughCasesInSwitch`** : signale un `case` non vide qui « tombe » dans le suivant faute de `break` ou `return` ;
- **`noUnusedLocals`** / **`noUnusedParameters`** : signalent variables et paramètres inutilisés ;
- **`exactOptionalPropertyTypes`** : distingue « propriété absente » et « propriété présente valant `undefined` ».

Exemple avec `noUncheckedIndexedAccess`. Sans l'option, ce code compile, alors que `notes[5]` vaut `undefined` à l'exécution :

```ts
const notes = [12, 15];
const n = notes[5];
console.log(n);
```

```text
undefined
```

Avec l'option activée, `n` est de type `number | undefined` et `n.toFixed(1)` serait refusé avec `'n' is possibly 'undefined'.` : la vérification devient obligatoire.

## Produire ou bloquer : `noEmitOnError`, `sourceMap`, `declaration`

- **`noEmitOnError`** : aucun `.js` n'est produit tant qu'il reste une erreur de type ;
- **`sourceMap`** : génère des fichiers `.js.map` pour que le débogueur et les messages d'erreur pointent vers le **code TypeScript** d'origine ;
- **`declaration`** : génère des fichiers `.d.ts` décrivant les types exportés, indispensable si vous publiez une bibliothèque (leçon suivante) ;
- **`skipLibCheck`** : ne revérifie pas les fichiers `.d.ts` des dépendances, ce qui accélère la compilation.

## Le mode surveillance

```bash
npx tsc --watch
```

`tsc --watch` (ou `-w`) recompile automatiquement à chaque enregistrement et affiche les erreurs au fil de l'eau. Votre éditeur effectue de son côté la même vérification en continu, en s'appuyant sur le même `tsconfig.json`.

## À retenir

- `tsconfig.json` à la racine ; `npx tsc` compile tout le projet, `tsc --noEmit` vérifie seulement.
- `include`, `rootDir`, `outDir` : où sont les sources, où va le JavaScript.
- `target` = version de JavaScript produite ; `module` = système de modules (`nodenext` pour Node.js).
- `"strict": true` toujours, explicitement ; ajoutez `noUncheckedIndexedAccess` pour les accès indexés.
- `noEmitOnError`, `sourceMap`, `declaration` contrôlent ce qui est produit.

## Exercices

### Exercice 1 — Lire une configuration

Avec `"rootDir": "src"`, `"outDir": "build"` et `"include": ["src"]`, où sera produit le fichier compilé de `src/services/paiement.ts` ?

```solution-text
build/services/paiement.js : la structure sous rootDir (src) est reproduite dans outDir (build).
```

### Exercice 2 — Quelle option ?

Associez chaque besoin à une option : (a) ne jamais livrer de JavaScript tant qu'il reste une erreur ; (b) obliger à traiter le cas où `liste[i]` n'existe pas ; (c) déboguer en voyant le code TypeScript ; (d) vérifier les types dans la CI sans produire de fichiers.

```solution-text
(a) "noEmitOnError": true
(b) "noUncheckedIndexedAccess": true
(c) "sourceMap": true
(d) la commande tsc --noEmit (ou l'option "noEmit": true)
```

### Exercice 3 — Corriger pour le mode strict

Corrigez ce code pour qu'il compile en mode strict : `function total(prix, quantite) { return prix * quantite; }`, puis affichez `total(2.5, 4)`.

```solution-ts
function total(prix: number, quantite: number): number {
  return prix * quantite;
}
console.log(total(2.5, 4));
```

```text
10
```
"""

M5_L2 = r"""
## Les modules : un fichier, une responsabilité

Dans un projet, le code est réparti en **modules** : chaque fichier qui contient `import` ou `export` est un module, avec sa propre portée. On **exporte** ce qui doit être utilisé ailleurs, et on l'**importe** là où on en a besoin.

Fichier `src/modeles.ts` :

```ts
export interface Cours {
  slug: string;
  titre: string;
  dureeMinutes: number;
}

export type Niveau = "debutant" | "intermediaire" | "avance";

export function dureeLisible(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;
  return m === 0 ? `${h} h` : `${h} h ${m}`;
}
```

Fichier `src/index.ts` :

```ts
import { dureeLisible } from "./modeles.js";
import type { Cours } from "./modeles.js";

const cours: Cours = { slug: "typescript", titre: "TypeScript", dureeMinutes: 480 };
console.log(`${cours.titre} : ${dureeLisible(cours.dureeMinutes)}`);
```

Après `npx tsc` puis `node dist/index.js` :

```text
TypeScript : 8 h
```

Trois points méritent attention :

1. **L'extension `.js` dans l'import.** Avec `"module": "nodenext"` et des modules ES, on écrit le chemin du fichier **tel qu'il existera après compilation** : `./modeles.js`, même si le fichier source est `modeles.ts`. TypeScript le comprend et retrouve `modeles.ts`. Sans extension, `tsc` signale une erreur, car Node.js lui-même refuserait l'import.
2. **`import type`** importe uniquement un type : l'import est **entièrement effacé** à la compilation. L'option `verbatimModuleSyntax` impose cette distinction, ce qui rend le JavaScript produit prévisible.
3. **`export`** peut précéder toute déclaration : fonction, constante, classe, interface, type.

> Les deux blocs ci-dessus forment un projet de deux fichiers : ils ne peuvent pas être exécutés séparément. Pour les essayer, créez-les dans `src/` avec la configuration de la leçon précédente.

## Export par défaut et exports nommés

```ts
export default class Catalogue {
  private titres: string[] = [];
  ajouter(titre: string): void {
    this.titres.push(titre);
  }
}
```

Un module peut avoir **un** export par défaut, importé sans accolades et sous le nom de votre choix : `import Catalogue from "./catalogue.js";`. Beaucoup d'équipes préfèrent les **exports nommés**, plus faciles à rechercher et à renommer de façon cohérente.

## Modules ES et CommonJS

Node.js connaît deux systèmes de modules :

| | Modules ES (ESM) | CommonJS (CJS) |
|---|---|---|
| Syntaxe | `import` / `export` | `require()` / `module.exports` |
| Activation | `"type": "module"` dans `package.json`, ou fichiers `.mjs` | par défaut, ou fichiers `.cjs` |
| Statut | standard du langage | historique, encore très répandu |

En TypeScript, on écrit **toujours** `import` / `export`. Avec `"module": "nodenext"`, `tsc` lit le `package.json` et produit le format attendu par Node.js. Pour un nouveau projet, choisissez les modules ES (`"type": "module"`).

## Les fichiers de déclaration `.d.ts`

Un fichier `.d.ts` contient **uniquement des types**, sans code exécutable. Il décrit les types d'un code JavaScript existant. Par exemple, pour une petite bibliothèque JavaScript `calcul-tva.js` :

```ts
export declare function prixTtc(prixHt: number, taux?: number): number;
export declare const TAUX_NORMAL: number;
```

Le mot-clé `declare` signifie « cela existe ailleurs, à l'exécution ; voici son type ». Avec l'option `declaration`, `tsc` génère automatiquement ces fichiers pour votre propre code.

## Les types des bibliothèques : `@types`

Quand vous installez une bibliothèque npm, trois cas se présentent :

1. elle **fournit ses types** (fichiers `.d.ts` inclus) : rien à faire ;
2. ses types sont publiés à part, par la communauté, dans le projet **DefinitelyTyped**, sous le nom `@types/<nom>` : on les installe en dépendance de développement, par exemple `npm install --save-dev @types/node` pour les API de Node.js (`process`, `fs`…) ;
3. aucun type n'existe : on écrit un petit `.d.ts`, ou l'on accepte un typage minimal.

> Les paquets `@types` sont maintenus par la communauté et peuvent avoir un léger retard sur la bibliothèque. Vérifiez que leur version correspond à celle de la bibliothèque installée.

## Exécuter du TypeScript

| Méthode | Vérifie les types ? | Usage |
|---|---|---|
| `tsc` puis `node dist/index.js` | oui | production, bibliothèques |
| un outil de **bundling** (Vite, esbuild…) | non (effacement seul) | applications web |
| un exécuteur comme `tsx` | non | développement, scripts |
| `node fichier.ts` dans les versions récentes de Node.js | non (effacement seul) | scripts, développement |

Les outils rapides se contentent d'**effacer** les types sans les vérifier. Ils ne savent donc pas traiter les syntaxes qui génèrent du code, comme les `enum` ou les propriétés de paramètres (module 3) ; l'option `erasableSyntaxOnly` de `tsc` signale ces syntaxes pour garder un code compatible. Et dans tous les cas, **gardez `tsc --noEmit` dans votre chaîne** (script `typecheck`, intégration continue) : c'est lui qui vérifie les types.

## Typer l'environnement : variables et configuration

Les variables d'environnement (`process.env.X`) sont typées `string | undefined` par `@types/node` : TypeScript vous oblige à gérer leur absence. Un module de configuration centralise ces vérifications :

```ts
type Environnement = Record<string, string | undefined>;

function lireVariable(env: Environnement, nom: string): string {
  const valeur = env[nom];
  if (valeur === undefined || valeur === "") {
    throw new Error(`Variable d'environnement manquante : ${nom}`);
  }
  return valeur;
}

const envDeTest: Environnement = { URL_API: "https://api.exemple.fr" };
console.log(lireVariable(envDeTest, "URL_API"));
try {
  lireVariable(envDeTest, "CLE_API");
} catch (e) {
  console.log(e instanceof Error ? e.message : e);
}
```

```text
https://api.exemple.fr
Variable d'environnement manquante : CLE_API
```

Dans un vrai projet, on passerait `process.env`. Ne versionnez jamais une vraie clé : les secrets restent dans l'environnement ou un gestionnaire de secrets, et le message d'erreur ne doit afficher que le **nom** de la variable, jamais sa valeur.

## À retenir

- `export` / `import` entre fichiers ; `import type` pour les imports de types seulement.
- Avec `nodenext` et les modules ES, écrivez l'extension `.js` dans les imports relatifs.
- `.d.ts` = types seuls (`declare`) ; `@types/<nom>` pour les bibliothèques sans types.
- Les exécuteurs rapides effacent les types sans les vérifier : gardez `tsc --noEmit`.

## Exercices

### Exercice 1 — Corriger un import

Dans un projet `"module": "nodenext"` avec `"type": "module"`, l'import `import { calculer } from "./outils";` est refusé. Pourquoi, et comment le corriger ?

```solution-text
Avec les modules ES de Node.js, les chemins relatifs doivent indiquer l'extension du fichier
qui existera à l'exécution. On écrit donc : import { calculer } from "./outils.js";
(TypeScript retrouve le fichier source outils.ts).
```

### Exercice 2 — Choisir l'import

`src/types.ts` exporte `interface Commande` et `src/prix.ts` exporte la fonction `totalCommande`. Écrivez les imports de `src/index.ts`.

```solution-text
import type { Commande } from "./types.js";
import { totalCommande } from "./prix.js";
Commande n'est qu'un type : import type garantit que l'import disparaît à la compilation.
```

### Exercice 3 — Déclarer une bibliothèque

Une bibliothèque JavaScript sans types exporte `slugifier(texte)`, qui renvoie une chaîne, et `SEPARATEUR`, une chaîne. Écrivez son fichier de déclaration.

```solution-ts
export declare function slugifier(texte: string): string;
export declare const SEPARATEUR: string;
```
"""

M5_L3 = r"""
## Le projet

Vous allez écrire le cœur typé d'un service d'**inscriptions à des formations**, en mobilisant toute la formation :

- des **modèles** (interfaces, unions de littéraux, `readonly`) ;
- la **validation** de données reçues en `unknown` avec un prédicat de type ;
- un **résultat générique** `Resultat<T>` plutôt que des exceptions ;
- une **classe** de dépôt générique avec des membres privés ;
- une **union discriminée** d'événements traitée avec vérification d'exhaustivité ;
- des **types utilitaires** (`Omit`, `Record`, `Pick`).

Dans un vrai projet, ce code serait réparti en modules (`modeles.ts`, `validation.ts`, `depot.ts`, `index.ts`) avec la configuration de la leçon 1. Ici, il tient dans un seul fichier pour être exécuté d'un bloc.

## Démarche

1. **Modèles** : formation, apprenant, inscription et statuts ; `NouvelleInscription` est dérivée avec `Omit`, car l'identifiant et le statut sont fixés par le service.
2. **Validation** : les demandes arrivent en `unknown` ; le prédicat `estDemande` vérifie la forme et `valider` renvoie un `Resultat<…>`.
3. **Dépôt générique** : `Depot<T extends { id: string }>` stocke tout objet possédant un `id`, derrière une `Map` privée.
4. **Service et événements** : règles métier (formation existante, places, doublons) ; chaque action produit un `Evenement` traduit par un `switch` exhaustif.

## Le programme complet

```ts
// ---------- Modèles ----------
type Niveau = "debutant" | "intermediaire" | "avance";
type StatutInscription = "confirmee" | "liste-attente" | "annulee";

interface Formation {
  readonly id: string;
  titre: string;
  niveau: Niveau;
  places: number;
}

interface Apprenant {
  readonly id: string;
  prenom: string;
  email: string;
}

interface Inscription {
  readonly id: string;
  formationId: string;
  apprenantId: string;
  statut: StatutInscription;
}

type NouvelleInscription = Omit<Inscription, "id" | "statut">;

type Resultat<T> = { ok: true; valeur: T } | { ok: false; erreur: string };

type Evenement =
  | { type: "inscrit"; apprenant: string; formation: string }
  | { type: "attente"; apprenant: string; formation: string; rang: number }
  | { type: "refuse"; motif: string };

// ---------- Validation d'une entrée inconnue ----------
function estDemande(v: unknown): v is NouvelleInscription {
  return typeof v === "object" && v !== null
    && "formationId" in v && typeof v.formationId === "string"
    && "apprenantId" in v && typeof v.apprenantId === "string";
}

function valider(v: unknown): Resultat<NouvelleInscription> {
  if (!estDemande(v)) {
    return { ok: false, erreur: "demande mal formée" };
  }
  return { ok: true, valeur: v };
}

// ---------- Dépôt générique ----------
class Depot<T extends { id: string }> {
  private elements = new Map<string, T>();

  ajouter(element: T): void {
    this.elements.set(element.id, element);
  }

  trouver(id: string): T | undefined {
    return this.elements.get(id);
  }

  lister(filtre: (element: T) => boolean = () => true): T[] {
    return [...this.elements.values()].filter(filtre);
  }
}

// ---------- Service ----------
class ServiceInscriptions {
  private compteur = 0;

  constructor(
    private formations: Depot<Formation>,
    private apprenants: Depot<Apprenant>,
    private inscriptions: Depot<Inscription>,
  ) {}

  inscrire(entree: unknown): Evenement {
    const demande = valider(entree);
    if (!demande.ok) {
      return { type: "refuse", motif: demande.erreur };
    }
    const { formationId, apprenantId } = demande.valeur;
    const formation = this.formations.trouver(formationId);
    const apprenant = this.apprenants.trouver(apprenantId);
    if (formation === undefined || apprenant === undefined) {
      return { type: "refuse", motif: "formation ou apprenant inconnu" };
    }
    const existantes = this.inscriptions.lister((i) => i.formationId === formationId && i.statut !== "annulee");
    if (existantes.some((i) => i.apprenantId === apprenantId)) {
      return { type: "refuse", motif: `${apprenant.prenom} est déjà inscrit(e)` };
    }
    const confirmees = existantes.filter((i) => i.statut === "confirmee").length;
    const statut: StatutInscription = confirmees < formation.places ? "confirmee" : "liste-attente";
    this.compteur++;
    this.inscriptions.ajouter({ id: `INS-${this.compteur}`, formationId, apprenantId, statut });
    if (statut === "confirmee") {
      return { type: "inscrit", apprenant: apprenant.prenom, formation: formation.titre };
    }
    const rang = existantes.length - confirmees + 1;
    return { type: "attente", apprenant: apprenant.prenom, formation: formation.titre, rang };
  }

  bilan(): Record<StatutInscription, number> {
    const totaux: Record<StatutInscription, number> = { "confirmee": 0, "liste-attente": 0, "annulee": 0 };
    for (const i of this.inscriptions.lister()) {
      totaux[i.statut]++;
    }
    return totaux;
  }
}

function decrire(e: Evenement): string {
  switch (e.type) {
    case "inscrit":
      return `✔ ${e.apprenant} est inscrit(e) à « ${e.formation} »`;
    case "attente":
      return `… ${e.apprenant} est en liste d'attente pour « ${e.formation} » (rang ${e.rang})`;
    case "refuse":
      return `✘ Refusé : ${e.motif}`;
    default: {
      const oubli: never = e;
      return oubli;
    }
  }
}

// ---------- Démonstration ----------
const formations = new Depot<Formation>();
formations.ajouter({ id: "ts", titre: "TypeScript", niveau: "intermediaire", places: 2 });

const apprenants = new Depot<Apprenant>();
for (const [id, prenom] of [["a1", "Amina"], ["a2", "Lucas"], ["a3", "Sofia"]]) {
  apprenants.ajouter({ id, prenom, email: `${prenom.toLowerCase()}@exemple.fr` });
}

const service = new ServiceInscriptions(formations, apprenants, new Depot<Inscription>());
const demandes: unknown[] = [
  { formationId: "ts", apprenantId: "a1" },
  { formationId: "ts", apprenantId: "a2" },
  { formationId: "ts", apprenantId: "a3" },
  { formationId: "ts", apprenantId: "a1" },
  { formationId: "go", apprenantId: "a2" },
  { formation: "ts" },
];

for (const d of demandes) {
  console.log(decrire(service.inscrire(d)));
}
console.log(service.bilan());

type Annuaire = Pick<Apprenant, "prenom" | "email">[];
const annuaire: Annuaire = apprenants.lister().map(({ prenom, email }) => ({ prenom, email }));
console.log(annuaire.map((a) => a.email).join(" ; "));
```

```text
✔ Amina est inscrit(e) à « TypeScript »
✔ Lucas est inscrit(e) à « TypeScript »
… Sofia est en liste d'attente pour « TypeScript » (rang 1)
✘ Refusé : Amina est déjà inscrit(e)
✘ Refusé : formation ou apprenant inconnu
✘ Refusé : demande mal formée
{ confirmee: 2, 'liste-attente': 1, annulee: 0 }
amina@exemple.fr ; lucas@exemple.fr ; sofia@exemple.fr
```

## Ce que TypeScript garantit ici

- **Une demande mal formée ne passe jamais** : `inscrire` reçoit un `unknown` et n'accède aux champs qu'après `valider`. Supprimez l'appel à `valider` et `tsc` refuse `demande.valeur`.
- **Aucun statut inventé** : `statut` ne peut valoir que trois littéraux, et `bilan` doit tous les compter, sinon le `Record` est incomplet.
- **Aucun événement oublié** : ajoutez `{ type: "annule"; … }` à `Evenement` et la ligne `const oubli: never = e;` devient une erreur tant que `decrire` ne le traite pas.
- **Le dépôt reste cohérent** : `Depot<Formation>` refuse d'enregistrer un apprenant, et la `Map` interne est inaccessible de l'extérieur.

> Limite à garder en tête : ces garanties portent sur **votre** code. Les données qui entrent (formulaire, API, base de données) doivent toujours être validées à l'exécution, ce que fait `estDemande`. Et dans une vraie application, ces règles (places disponibles, doublons) seraient aussi vérifiées côté serveur ou base de données.

## Pour aller plus loin

1. Répartissez le code en quatre modules avec `export` / `import` (et `import type` pour les types), un `tsconfig.json` strict et un script `typecheck`.
2. Remplacez le `Depot` en mémoire par une implémentation réelle (fichier JSON, base de données) sans changer le service, puis ajoutez des tests automatisés.

## À retenir

- Modélisez d'abord les données (interfaces, unions de littéraux), puis dérivez les variantes (`Omit`, `Pick`).
- Toute entrée externe est `unknown` jusqu'à sa validation par un prédicat de type.
- `Resultat<T>` et les unions discriminées rendent les erreurs et les cas explicites.
- Les génériques contraints (`T extends { id: string }`) donnent des composants réutilisables et sûrs.

## Exercices

### Exercice 1 — Annuler une inscription

On ajoute à `Evenement` le membre `{ type: "annule"; apprenant: string }`. Que se passe-t-il à la compilation si l'on ne modifie pas `decrire`, et comment corriger ?

```solution-text
La ligne const oubli: never = e; devient une erreur : tsc indique que le type
{ type: "annule"; apprenant: string; } n'est pas affectable à never (TS2322).
Il suffit d'ajouter le cas correspondant dans decrire :
case "annule": return `↺ ${e.apprenant} a annulé son inscription`;
```

### Exercice 2 — Places restantes

Écrivez une fonction `placesRestantes(formation: Pick<Formation, "places">, confirmees: number): number` qui ne renvoie jamais un nombre négatif. Testez-la avec 2 places et 3 inscriptions confirmées, puis 10 places et 4.

```solution-ts
interface Formation {
  readonly id: string;
  titre: string;
  places: number;
}

function placesRestantes(formation: Pick<Formation, "places">, confirmees: number): number {
  return Math.max(0, formation.places - confirmees);
}

console.log(placesRestantes({ places: 2 }, 3));
console.log(placesRestantes({ places: 10 }, 4));
```

```text
0
6
```

Grâce à `Pick`, la fonction n'exige que la propriété dont elle a besoin : elle est plus facile à tester.

### Exercice 3 — Valider un email

Ajoutez une validation : une demande contenant un champ `email` doit avoir un `@`. Écrivez `emailValide(v: unknown): Resultat<string>` et testez-la avec `"lea@exemple.fr"`, `"lea.exemple.fr"` et `42`.

```solution-ts
type Resultat<T> = { ok: true; valeur: T } | { ok: false; erreur: string };

function emailValide(v: unknown): Resultat<string> {
  if (typeof v !== "string") {
    return { ok: false, erreur: "l'email doit être un texte" };
  }
  const email = v.trim().toLowerCase();
  if (!email.includes("@") || email.startsWith("@") || email.endsWith("@")) {
    return { ok: false, erreur: `« ${v} » n'est pas un email valide` };
  }
  return { ok: true, valeur: email };
}

for (const saisie of ["lea@exemple.fr", "lea.exemple.fr", 42]) {
  const r = emailValide(saisie);
  console.log(r.ok ? `OK : ${r.valeur}` : `Erreur : ${r.erreur}`);
}
```

```text
OK : lea@exemple.fr
Erreur : « lea.exemple.fr » n'est pas un email valide
Erreur : l'email doit être un texte
```

Cette vérification reste volontairement simple : elle sert à guider l'utilisateur. La seule preuve qu'une adresse est valide reste l'envoi d'un email de confirmation.
"""

QUIZ_M3 = [
    ("single", "Que décrit une interface TypeScript ?", None,
     ["Le code exécuté par une classe", "La forme (propriétés et méthodes) qu'un objet doit avoir", "Une base de données", "Un fichier de configuration"], [1],
     "Une interface est un contrat de forme : elle liste les propriétés et méthodes attendues, sans code exécutable."),
    ("single", "Quelle différence entre A | B et A & B ?", None,
     ["Aucune", "A | B : l'un ou l'autre ; A & B : les deux à la fois", "A | B : les deux à la fois ; A & B : l'un ou l'autre", "& ne fonctionne qu'avec des nombres"], [1],
     "L'union accepte une valeur de l'un des types ; l'intersection exige toutes les propriétés des deux types."),
    ("multiple", "Que permet un alias type mais PAS une interface ?", None,
     ["Décrire une union comme \"clair\" | \"sombre\"", "Décrire un tuple [number, number]", "Décrire un objet avec des propriétés", "Nommer un type de fonction (x: number) => number"], [0, 1, 3],
     "Les deux décrivent des objets ; seuls les alias type peuvent nommer directement des unions, des tuples ou des types de fonctions."),
    ("true_false", "Un objet peut être passé à une fonction attendant une interface même s'il n'a jamais été déclaré avec ce type, à condition d'en avoir la forme.", None,
     ["Vrai", "Faux"], [0],
     "TypeScript utilise un typage structurel : seule la forme compte, pas le nom du type."),
    ("single", "Que vérifie le mot-clé implements ?", None,
     ["Que la classe hérite du code de l'interface", "Que la classe possède tous les membres promis par l'interface", "Que la classe est abstraite", "Que la classe est exportée"], [1],
     "implements ne fournit aucun code : il vérifie que la classe respecte le contrat de l'interface."),
    ("single", "Depuis où un membre protected est-il accessible ?", None,
     ["Partout", "Uniquement depuis la classe qui le déclare", "Depuis la classe et ses sous-classes", "Uniquement depuis les instances"], [2],
     "protected est accessible dans la classe et dans les classes qui en héritent, mais pas depuis l'extérieur."),
    ("single", "Que fait constructor(public readonly id: string) {} ?", None,
     ["Rien, c'est une erreur", "Déclare une propriété publique en lecture seule id et l'initialise avec l'argument", "Crée une méthode id", "Rend la classe abstraite"], [1],
     "C'est une propriété de paramètre : déclaration et affectation en une seule écriture."),
    ("single", "Que signifie l'erreur TS2511 « Cannot create an instance of an abstract class » ?", None,
     ["La classe n'a pas de constructeur", "On a utilisé new sur une classe abstraite", "La classe est privée", "Il manque un import"], [1],
     "Une classe abstraite sert de modèle : on instancie seulement ses sous-classes concrètes."),
    ("multiple", "Quelles affirmations sur private et # sont exactes ?", None,
     ["private est vérifié par TypeScript à la compilation.", "#champ est privé y compris à l'exécution.", "private chiffre la valeur en mémoire.", "Les deux empêchent l'accès depuis l'extérieur dans du code TypeScript vérifié."], [0, 1, 3],
     "private est une vérification de compilation ; # est un vrai champ privé JavaScript. Aucun ne chiffre quoi que ce soit."),
    ("single", "À quoi sert override sur une méthode ?", None,
     ["À rendre la méthode privée", "À indiquer qu'elle redéfinit une méthode de la classe parente, ce que TypeScript vérifie", "À appeler la méthode parente automatiquement", "À empêcher toute redéfinition"], [1],
     "override signale une redéfinition ; si la méthode n'existe pas chez le parent (faute de frappe, renommage), tsc signale l'erreur."),
]

QUIZ_M4 = [
    ("single", "Quel avantage d'un générique function premier<T>(l: T[]): T | undefined sur une version avec any ?", None,
     ["Il est plus rapide à l'exécution", "Le type du résultat reste lié au type des éléments reçus", "Il accepte moins de tableaux", "Il évite d'écrire return"], [1],
     "Avec T, premier([\"a\"]) est de type string | undefined ; avec any, toute information de type est perdue."),
    ("single", "Dans function f<T extends { length: number }>(x: T), que signifie extends ?", None,
     ["T hérite d'une classe", "T doit posséder une propriété length de type number", "T est forcément un tableau", "T est optionnel"], [1],
     "Dans un générique, extends exprime une contrainte de compatibilité, pas un héritage."),
    ("single", "Que vaut keyof { titre: string; annee: number } ?", None,
     ["string | number", "\"titre\" | \"annee\"", "[\"titre\", \"annee\"]", "object"], [1],
     "keyof produit l'union des noms de propriétés sous forme de littéraux."),
    ("single", "Quel est le type de lire(livre, \"annee\") avec lire<T, K extends keyof T>(o: T, k: K): T[K] et livre.annee: number ?", None,
     ["any", "string", "number", "keyof T"], [2],
     "T[K] est le type de la propriété demandée : ici annee, de type number."),
    ("single", "Quel est le type de retour d'une fonction async qui renvoie un Utilisateur ?", None,
     ["Utilisateur", "Promise<Utilisateur>", "async Utilisateur", "void"], [1],
     "Une fonction async renvoie toujours une promesse ; await permet ensuite d'obtenir l'Utilisateur."),
    ("multiple", "Lesquels sont des types génériques fournis par TypeScript ou JavaScript ?", None,
     ["Array<T>", "Map<K, V>", "Promise<T>", "Number<T>"], [0, 1, 2],
     "Array, Map, Set et Promise sont paramétrés par des types ; Number n'accepte pas de paramètre de type."),
    ("single", "Quel utilitaire rend toutes les propriétés d'un type optionnelles ?", None,
     ["Required<T>", "Readonly<T>", "Partial<T>", "Pick<T, K>"], [2],
     "Partial<T> ajoute ? à chaque propriété : utile pour les mises à jour partielles."),
    ("single", "Que produit Omit<Utilisateur, \"motDePasseHache\"> ?", None,
     ["Un objet sans mot de passe à l'exécution", "Un type identique à Utilisateur sans la propriété motDePasseHache", "Une erreur", "Un type contenant uniquement motDePasseHache"], [1],
     "Omit agit sur les types seulement ; pour retirer réellement un champ d'un objet, il faut construire un nouvel objet."),
    ("true_false", "satisfies vérifie qu'une valeur respecte un type tout en conservant le type précis inféré pour cette valeur.", None,
     ["Vrai", "Faux"], [0],
     "Contrairement à une annotation, satisfies ne remplace pas le type inféré : on garde les types précis de chaque propriété."),
    ("multiple", "Pour des données reçues d'une API, quelles pratiques sont recommandées ?", None,
     ["Les typer unknown puis les valider avec un prédicat de type", "Écrire as MonType sans vérification", "Vérifier reponse.ok avant de lire le corps", "Faire confiance au type déclaré car TypeScript vérifie à l'exécution"], [0, 2],
     "as ne vérifie rien et les types n'existent pas à l'exécution : il faut contrôler le statut HTTP et valider la forme des données."),
]

QUIZ_M5 = [
    ("single", "Que fait npx tsc lancé sans nom de fichier dans un dossier contenant tsconfig.json ?", None,
     ["Il affiche l'aide", "Il compile tout le projet selon tsconfig.json", "Il crée un nouveau projet", "Il exécute le projet"], [1],
     "Sans argument, tsc lit le tsconfig.json et compile tous les fichiers inclus."),
    ("single", "Que fait tsc --noEmit ?", None,
     ["Il compile sans vérifier les types", "Il vérifie les types sans produire de fichiers", "Il supprime le dossier dist", "Il désactive le mode strict"], [1],
     "--noEmit est idéal en intégration continue ou quand un autre outil produit le JavaScript."),
    ("single", "Avec \"rootDir\": \"src\" et \"outDir\": \"dist\", où est produit src/api/client.ts ?", None,
     ["dist/client.js", "dist/api/client.js", "src/api/client.js", "dist/src/api/client.js"], [1],
     "La structure des dossiers sous rootDir est reproduite dans outDir."),
    ("multiple", "Quelles options font partie de la famille activée par \"strict\": true ?", None,
     ["strictNullChecks", "noImplicitAny", "noUncheckedIndexedAccess", "strictPropertyInitialization"], [0, 1, 3],
     "noUncheckedIndexedAccess n'est pas incluse dans strict : il faut l'activer séparément."),
    ("single", "Avec noUncheckedIndexedAccess, quel est le type de notes[0] si notes: number[] ?", None,
     ["number", "number | undefined", "any", "never"], [1],
     "L'option tient compte du fait qu'un indice peut ne pas exister : l'accès est typé number | undefined."),
    ("single", "Avec \"module\": \"nodenext\" et des modules ES, comment importer src/outils.ts depuis src/index.ts ?", None,
     ["import { f } from \"./outils\";", "import { f } from \"./outils.ts\";", "import { f } from \"./outils.js\";", "require(\"./outils\")"], [2],
     "On écrit le chemin du fichier tel qu'il existera après compilation (.js) ; TypeScript retrouve le fichier source .ts."),
    ("single", "Que garantit import type { Cours } from \"./modeles.js\" ?", None,
     ["Que Cours est une classe", "Que l'import est entièrement effacé à la compilation", "Que le module est chargé deux fois", "Que Cours devient readonly"], [1],
     "import type n'importe que des types : il ne laisse aucune trace dans le JavaScript produit."),
    ("single", "Que contient un fichier .d.ts ?", None,
     ["Du code JavaScript minifié", "Uniquement des déclarations de types", "Les tests du projet", "La configuration de tsc"], [1],
     "Un fichier de déclaration décrit des types (avec declare) sans code exécutable."),
    ("single", "Comment obtenir les types des API de Node.js (process, fs…) ?", None,
     ["Ils sont toujours inclus sans rien faire", "En installant @types/node en dépendance de développement", "En écrivant any partout", "En activant sourceMap"], [1],
     "Les types de Node.js sont publiés dans le paquet @types/node, issu du projet DefinitelyTyped."),
    ("multiple", "Quelles affirmations sur les exécuteurs rapides (effacement des types) sont exactes ?", None,
     ["Ils ne vérifient pas les types.", "Ils remplacent complètement tsc --noEmit.", "Ils peuvent refuser les enum, qui génèrent du code.", "Il faut garder une vérification tsc dans la chaîne (script ou CI)."], [0, 2, 3],
     "Ils se contentent d'effacer les annotations : la vérification des types reste le rôle de tsc, à garder en script ou en intégration continue."),
]
