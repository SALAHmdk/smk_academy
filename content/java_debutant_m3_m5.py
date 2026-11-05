"""Modules 3 à 5 de « Java pour débutants » (importé par content/java_debutant.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Programmation orientée objet
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Penser en objets

Jusqu'ici, vos programmes manipulaient des valeurs isolées : un prix, un nom, un tableau de notes. Dès qu'un programme grandit, il devient naturel de **regrouper** les données qui vont ensemble avec les opérations qui les concernent. C'est l'idée de la **programmation orientée objet** (POO).

- Une **classe** est un **plan** : elle décrit ce qu'est un compte bancaire (un titulaire, un solde) et ce qu'il sait faire (déposer, retirer).
- Un **objet** est un exemplaire concret construit à partir de ce plan : le compte d'Amina, le compte de Lucas. On dit aussi une **instance** de la classe.

| Notion | Rôle | Exemple pour un compte |
|---|---|---|
| **Attribut** (*field*) | une donnée de l'objet | `titulaire`, `solde` |
| **Méthode** | une action de l'objet | `deposer(montant)` |
| **Constructeur** | initialise un nouvel objet | `new Compte("Amina", 100)` |

## Une première classe

```java
class Compte {
    String titulaire;
    double solde;

    void deposer(double montant) {
        solde = solde + montant;
    }

    void afficher() {
        System.out.println(titulaire + " : " + solde + " EUR");
    }
}

public class Banque {
    public static void main(String[] args) {
        Compte c1 = new Compte();
        c1.titulaire = "Amina";
        c1.deposer(150);

        Compte c2 = new Compte();
        c2.titulaire = "Lucas";
        c2.deposer(40);
        c2.deposer(10);

        c1.afficher();
        c2.afficher();
    }
}
```

```text
Amina : 150.0 EUR
Lucas : 50.0 EUR
```

- `new Compte()` **crée** un objet ; la variable `c1` contient une **référence** vers lui.
- Chaque objet a **ses propres** attributs : déposer sur `c1` ne change pas `c2`.
- On accède à un attribut ou à une méthode avec le **point** : `c1.titulaire`, `c2.deposer(40)`.
- Les méthodes ne sont plus `static` : elles s'appliquent **à un objet précis**, celui placé avant le point.
- Un attribut non initialisé reçoit une valeur par défaut : `0` pour les nombres, `false` pour un `boolean`, `null` pour un objet.

> Dans cet exemple, les deux classes sont dans le même fichier `Banque.java` pour simplifier. Dans un vrai projet, chaque classe a **son propre fichier** (`Compte.java`, `Banque.java`).

## Le constructeur

Remplir les attributs un par un après `new` est fastidieux et risqué (on peut en oublier). Un **constructeur** est une méthode spéciale, **du même nom que la classe** et **sans type de retour**, appelée automatiquement par `new` :

```java
class Livre {
    String titre;
    String auteur;
    int pages;

    Livre(String titre, String auteur, int pages) {
        this.titre = titre;
        this.auteur = auteur;
        this.pages = pages;
    }

    Livre(String titre, String auteur) {
        this(titre, auteur, 0);  // appelle l'autre constructeur
    }

    String resume() {
        return titre + " (" + auteur + ", " + pages + " p.)";
    }
}

public class Constructeurs {
    public static void main(String[] args) {
        Livre a = new Livre("Le Petit Prince", "Saint-Exupéry", 96);
        Livre b = new Livre("Carnet de notes", "Anonyme");
        System.out.println(a.resume());
        System.out.println(b.resume());
    }
}
```

```text
Le Petit Prince (Saint-Exupéry, 96 p.)
Carnet de notes (Anonyme, 0 p.)
```

- Le mot clé `this` désigne **l'objet en cours**. `this.titre = titre;` signifie : « l'attribut `titre` de cet objet reçoit le paramètre `titre` ». Sans `this`, le paramètre masquerait l'attribut.
- Une classe peut avoir **plusieurs constructeurs** (surcharge) ; `this(…)` en appelle un autre, en première instruction.
- Si vous n'écrivez aucun constructeur, Java en fournit un **par défaut**, sans paramètre. Dès que vous en écrivez un, ce constructeur par défaut disparaît.

## toString : un affichage lisible

Afficher directement un objet avec `println` donne par défaut quelque chose comme `Livre@1b6d3586` : le nom de la classe suivi d'un code peu parlant. En écrivant une méthode `toString()`, vous choisissez ce qui s'affiche :

```java
class Point {
    int x;
    int y;

    Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    void deplacer(int dx, int dy) {
        x += dx;
        y += dy;
    }

    @Override
    public String toString() {
        return "(" + x + ", " + y + ")";
    }
}

public class Points {
    public static void main(String[] args) {
        Point p = new Point(2, 3);
        System.out.println(p);
        p.deplacer(1, -1);
        System.out.println("Après déplacement : " + p);
    }
}
```

```text
(2, 3)
Après déplacement : (3, 2)
```

`println` et la concaténation avec `+` appellent automatiquement `toString()`. L'annotation `@Override` sera expliquée avec l'héritage : elle indique que l'on **redéfinit** une méthode existante.

## Références et null

Une variable de type objet ne contient pas l'objet lui-même, mais une **référence** (une sorte d'adresse). Copier la variable copie la référence : les deux variables désignent alors **le même objet**.

```java
class Compteur {
    int valeur;
}

public class References {
    public static void main(String[] args) {
        Compteur a = new Compteur();
        Compteur b = a;          // même objet, deux noms
        b.valeur = 10;
        System.out.println(a.valeur);

        Compteur c = new Compteur();
        System.out.println(a == b);   // même objet ?
        System.out.println(a == c);

        Compteur vide = null;    // aucune référence
        System.out.println(vide == null);
    }
}
```

```text
10
true
false
true
```

`null` signifie « aucun objet ». Appeler une méthode sur une variable `null` provoque une `NullPointerException` à l'exécution : vérifiez avec `!= null` quand une valeur peut être absente.

## À retenir

- Une **classe** est un plan (attributs + méthodes) ; un **objet** est une instance créée avec `new`.
- Le **constructeur** porte le nom de la classe, n'a pas de type de retour et initialise l'objet ; `this` désigne l'objet en cours.
- Chaque objet a ses propres valeurs d'attributs ; les méthodes non `static` agissent sur l'objet avant le point.
- Redéfinissez `toString()` pour obtenir un affichage lisible.
- Une variable objet contient une **référence** ; `==` compare des références ; `null` = aucun objet.

## Exercices

### Exercice 1 — Rectangle

Écrivez une classe `Rectangle` (largeur, hauteur) avec un constructeur, les méthodes `aire()` et `perimetre()`, et un `toString()`. Testez avec un rectangle 4 × 2,5.

```solution-java
class Rectangle {
    double largeur;
    double hauteur;

    Rectangle(double largeur, double hauteur) {
        this.largeur = largeur;
        this.hauteur = hauteur;
    }

    double aire() {
        return largeur * hauteur;
    }

    double perimetre() {
        return 2 * (largeur + hauteur);
    }

    @Override
    public String toString() {
        return "Rectangle " + largeur + " x " + hauteur;
    }
}

public class TestRectangle {
    public static void main(String[] args) {
        Rectangle r = new Rectangle(4, 2.5);
        System.out.println(r);
        System.out.println("Aire : " + r.aire());
        System.out.println("Périmètre : " + r.perimetre());
    }
}
```

```text
Rectangle 4.0 x 2.5
Aire : 10.0
Périmètre : 13.0
```

### Exercice 2 — Prévoir l'affichage

Qu'affiche ce code, avec la classe `Point` de la leçon ?

```text
Point p1 = new Point(0, 0);
Point p2 = p1;
p2.deplacer(5, 5);
Point p3 = new Point(5, 5);
System.out.println(p1 + " " + (p1 == p2) + " " + (p1 == p3));
```

```solution-text
(5, 5) true false
p1 et p2 désignent le même objet : le déplacement via p2 se voit sur p1, et p1 == p2 est vrai.
p3 est un autre objet, même avec les mêmes coordonnées : p1 == p3 est faux.
```

### Exercice 3 — Thermostat

Créez une classe `Thermostat` avec un attribut `temperature` (initialisé par le constructeur) et les méthodes `augmenter()` et `baisser()` qui modifient la température de 0,5 degré. Partez de 19, augmentez trois fois, baissez une fois.

```solution-java
class Thermostat {
    double temperature;

    Thermostat(double temperature) {
        this.temperature = temperature;
    }

    void augmenter() {
        temperature += 0.5;
    }

    void baisser() {
        temperature -= 0.5;
    }
}

public class TestThermostat {
    public static void main(String[] args) {
        Thermostat t = new Thermostat(19);
        t.augmenter();
        t.augmenter();
        t.augmenter();
        t.baisser();
        System.out.println("Température : " + t.temperature + " °C");
    }
}
```

```text
Température : 20.0 °C
```
"""

M3_L2 = r"""
## Le problème : des attributs modifiables par tous

Avec la classe `Compte` de la leçon précédente, rien n'empêche d'écrire `c1.solde = -5000;` n'importe où dans le programme. L'objet ne peut pas protéger sa propre cohérence. L'**encapsulation** consiste à **cacher** les données d'un objet et à n'autoriser leur modification que **par ses méthodes**, qui vérifient les règles.

## Les modificateurs d'accès

| Modificateur | Visible depuis… |
|---|---|
| `private` | la classe elle-même uniquement |
| *(aucun)* | les classes du même *package* (dossier de classes) |
| `protected` | le même package et les sous-classes |
| `public` | partout |

La règle d'or : **attributs `private`**, méthodes `public` pour ce que l'objet propose au reste du programme.

## Accesseurs et validation

On donne accès aux données par des méthodes appelées **accesseurs** : un *getter* (`getSolde()`) pour lire, éventuellement un *setter* (`setX(…)`) pour modifier. Mais on ne crée pas de setter systématiquement : pour un compte, on préfère des méthodes **métier** (`deposer`, `retirer`) qui contrôlent chaque opération.

```java
class Compte {
    private final String titulaire;
    private double solde;

    public Compte(String titulaire, double soldeInitial) {
        if (soldeInitial < 0) {
            throw new IllegalArgumentException("Solde initial négatif");
        }
        this.titulaire = titulaire;
        this.solde = soldeInitial;
    }

    public String getTitulaire() {
        return titulaire;
    }

    public double getSolde() {
        return solde;
    }

    public void deposer(double montant) {
        if (montant <= 0) {
            throw new IllegalArgumentException("Montant invalide : " + montant);
        }
        solde += montant;
    }

    public boolean retirer(double montant) {
        if (montant <= 0 || montant > solde) {
            return false;   // opération refusée, le solde ne bouge pas
        }
        solde -= montant;
        return true;
    }
}

public class Encapsulation {
    public static void main(String[] args) {
        Compte c = new Compte("Amina", 100);
        c.deposer(50);
        System.out.println("Retrait de 500 : " + c.retirer(500));
        System.out.println("Retrait de 30 : " + c.retirer(30));
        System.out.println(c.getTitulaire() + " : " + c.getSolde());
    }
}
```

```text
Retrait de 500 : false
Retrait de 30 : true
Amina : 120.0
```

- `private double solde` : depuis `main`, écrire `c.solde = -5000;` provoque maintenant une **erreur de compilation** (*solde has private access in Compte*).
- `private final String titulaire` : le titulaire est fixé par le constructeur et ne peut plus changer. Il n'a qu'un getter.
- `throw new IllegalArgumentException(…)` **signale une erreur** quand on passe un argument invalide : le programme s'arrête à cet endroit (sauf si l'erreur est interceptée, voir le module 5). Ainsi, un objet `Compte` est **toujours dans un état valide**.

> Bénéfice majeur : si la règle change (découvert autorisé de 200 €, par exemple), vous ne modifiez **qu'une méthode**, et non tous les endroits du programme qui touchaient au solde.

## Démonstration : un argument refusé

```java
class Produit {
    private final String nom;
    private double prix;

    Produit(String nom, double prix) {
        this.nom = nom;
        setPrix(prix);
    }

    public void setPrix(double prix) {
        if (prix < 0) {
            throw new IllegalArgumentException("Le prix ne peut pas être négatif");
        }
        this.prix = prix;
    }

    public double getPrix() {
        return prix;
    }
}

public class Validation {
    public static void main(String[] args) {
        Produit p = new Produit("Lampe", 25);
        System.out.println("Prix : " + p.getPrix());
        p.setPrix(-3);
        System.out.println("Cette ligne n'est jamais atteinte");
    }
}
```

```text
Prix : 25.0
Exception in thread "main" java.lang.IllegalArgumentException: Le prix ne peut pas être négatif
	at Produit.setPrix(Validation.java:12)
	at Validation.main(Validation.java:26)
```

Le message d'erreur (la **pile d'appels**, *stack trace*) se lit de haut en bas : le type d'exception, votre message, puis la méthode où l'erreur a été levée et celles qui l'ont appelée, avec les numéros de ligne. Le constructeur réutilise `setPrix`, ce qui évite de dupliquer la vérification.

## Les membres static

Un attribut `static` appartient **à la classe** et non à chaque objet : il est **partagé** par toutes les instances. Une méthode `static` s'appelle sur la classe (`Math.sqrt`, `Integer.parseInt`) et n'a pas accès à `this`.

```java
class Ticket {
    private static int compteur = 0;   // partagé par tous les tickets
    public static final String PREFIXE = "T-";

    private final int numero;

    Ticket() {
        compteur++;
        numero = compteur;
    }

    public String getCode() {
        return PREFIXE + numero;
    }

    public static int getNombreCrees() {
        return compteur;
    }
}

public class Tickets {
    public static void main(String[] args) {
        Ticket a = new Ticket();
        Ticket b = new Ticket();
        Ticket c = new Ticket();
        System.out.println(a.getCode() + " " + b.getCode() + " " + c.getCode());
        System.out.println("Tickets créés : " + Ticket.getNombreCrees());
    }
}
```

```text
T-1 T-2 T-3
Tickets créés : 3
```

`public static final` est la façon habituelle de déclarer une **constante** de classe, comme `Math.PI`.

## Conventions de nommage

| Élément | Convention | Exemple |
|---|---|---|
| Classe | PascalCase, nom | `CompteBancaire` |
| Méthode | camelCase, verbe | `calculerTotal()` |
| Attribut, variable | camelCase | `dateCreation` |
| Constante | MAJUSCULES_ET_TIRETS_BAS | `TAUX_MAX` |
| Getter / setter | `getX()`, `setX(…)`, `isX()` pour un booléen | `isActif()` |

## À retenir

- Encapsuler : attributs `private`, accès par des méthodes `public` qui vérifient les règles.
- Getters pour lire ; setters seulement si la modification a du sens, sinon des méthodes métier.
- `final` sur un attribut : valeur fixée une fois pour toutes (en général dans le constructeur).
- `throw new IllegalArgumentException("…")` refuse un argument invalide ; l'objet reste cohérent.
- `static` : membre partagé par la classe entière ; `public static final` pour les constantes.

## Exercices

### Exercice 1 — Note encadrée

Écrivez une classe `Note` avec un attribut privé `valeur` (entre 0 et 20) : constructeur, getter, et une méthode `ajouterBonus(double points)` qui plafonne la note à 20. Testez avec 18 puis un bonus de 3.

```solution-java
class Note {
    private double valeur;

    Note(double valeur) {
        if (valeur < 0 || valeur > 20) {
            throw new IllegalArgumentException("Note hors de [0, 20] : " + valeur);
        }
        this.valeur = valeur;
    }

    public double getValeur() {
        return valeur;
    }

    public void ajouterBonus(double points) {
        valeur = Math.min(20, valeur + points);
    }
}

public class TestNote {
    public static void main(String[] args) {
        Note n = new Note(18);
        n.ajouterBonus(3);
        System.out.println("Note finale : " + n.getValeur());
    }
}
```

```text
Note finale : 20.0
```

### Exercice 2 — Identifiants automatiques

Créez une classe `Membre` dont chaque instance reçoit automatiquement un identifiant `M001`, `M002`… (attribut `static` + `String.format("M%03d", n)`). Créez trois membres et affichez leurs identifiants et leurs noms.

```solution-java
class Membre {
    private static int dernierNumero = 0;
    private final String id;
    private final String nom;

    Membre(String nom) {
        dernierNumero++;
        this.id = String.format("M%03d", dernierNumero);
        this.nom = nom;
    }

    @Override
    public String toString() {
        return id + " " + nom;
    }
}

public class TestMembres {
    public static void main(String[] args) {
        System.out.println(new Membre("Inès"));
        System.out.println(new Membre("Hugo"));
        System.out.println(new Membre("Yanis"));
    }
}
```

```text
M001 Inès
M002 Hugo
M003 Yanis
```

`%03d` affiche un entier sur 3 chiffres, complété par des zéros à gauche.

### Exercice 3 — Pourquoi pas de setSolde ?

Expliquez en deux phrases pourquoi la classe `Compte` propose `deposer` et `retirer` plutôt qu'un `setSolde(double)` public.

```solution-text
Un setSolde public permettrait de fixer n'importe quel solde (négatif, par exemple) sans aucun contrôle,
ce qui casserait la cohérence de l'objet. Les méthodes métier deposer et retirer expriment les seules
opérations autorisées et vérifient chacune leurs règles (montant positif, solde suffisant).
```
"""

M3_L3 = r"""
## Réutiliser avec l'héritage

Dans une application de ressources humaines, un **salarié** et un **stagiaire** partagent beaucoup de choses (un nom, une méthode de présentation), mais diffèrent sur d'autres (calcul de la rémunération). Plutôt que de dupliquer le code commun, on le place dans une classe **mère** (ou *superclasse*), dont héritent des classes **filles** (ou *sous-classes*).

L'héritage exprime une relation « **est un** » : un stagiaire **est une** personne. Si la phrase sonne faux (« une voiture est un moteur »), l'héritage n'est pas le bon outil : on utilise plutôt un attribut (« une voiture **a un** moteur »).

## extends et super

```java
class Personne {
    protected String nom;

    Personne(String nom) {
        this.nom = nom;
    }

    String sePresenter() {
        return "Je m'appelle " + nom;
    }
}

class Salarie extends Personne {
    private double salaireMensuel;

    Salarie(String nom, double salaireMensuel) {
        super(nom);   // appelle le constructeur de Personne
        this.salaireMensuel = salaireMensuel;
    }

    double salaireAnnuel() {
        return salaireMensuel * 12;
    }
}

public class Heritage {
    public static void main(String[] args) {
        Salarie s = new Salarie("Nadia", 2500);
        System.out.println(s.sePresenter());   // méthode héritée
        System.out.println("Salaire annuel : " + s.salaireAnnuel());
    }
}
```

```text
Je m'appelle Nadia
Salaire annuel : 30000.0
```

- `class Salarie extends Personne` : `Salarie` **hérite** des attributs et méthodes de `Personne`.
- `super(nom)` appelle le constructeur de la classe mère ; c'est obligatoirement la **première instruction** du constructeur.
- `protected` rend `nom` accessible aux sous-classes (tout en le cachant au reste du programme, hors package).
- En Java, une classe n'hérite que d'**une seule** classe mère (héritage simple).

## Redéfinir une méthode : @Override

Une sous-classe peut **redéfinir** (*override*) une méthode héritée pour l'adapter. L'annotation `@Override` demande au compilateur de vérifier qu'une méthode de même signature existe bien dans la classe mère : une faute de frappe dans le nom devient alors une erreur de compilation au lieu d'un bug silencieux.

```java
class Personne {
    protected String nom;

    Personne(String nom) {
        this.nom = nom;
    }

    String sePresenter() {
        return "Je m'appelle " + nom;
    }
}

class Stagiaire extends Personne {
    private String ecole;

    Stagiaire(String nom, String ecole) {
        super(nom);
        this.ecole = ecole;
    }

    @Override
    String sePresenter() {
        return super.sePresenter() + ", stagiaire de " + ecole;
    }
}

public class Redefinition {
    public static void main(String[] args) {
        Personne p = new Personne("Marc");
        Stagiaire st = new Stagiaire("Zoé", "l'IUT de Nantes");
        System.out.println(p.sePresenter());
        System.out.println(st.sePresenter());
    }
}
```

```text
Je m'appelle Marc
Je m'appelle Zoé, stagiaire de l'IUT de Nantes
```

`super.sePresenter()` appelle la version de la classe mère : on **complète** le comportement au lieu de le réécrire entièrement.

| À ne pas confondre | Surcharge (*overloading*) | Redéfinition (*overriding*) |
|---|---|---|
| Où ? | dans une même classe | dans une sous-classe |
| Signature | même nom, paramètres **différents** | même nom, **mêmes** paramètres |
| But | plusieurs variantes d'une opération | adapter un comportement hérité |

## Une variable de type mère

Une variable de type `Personne` peut contenir **n'importe quelle sous-classe** de `Personne`. Au moment de l'appel, c'est la méthode de **l'objet réel** qui s'exécute :

```java
class Animal {
    String cri() {
        return "...";
    }
}

class Chien extends Animal {
    @Override
    String cri() {
        return "Wouf";
    }
}

class Chat extends Animal {
    @Override
    String cri() {
        return "Miaou";
    }

    void ronronner() {
        System.out.println("Rrrr");
    }
}

public class TypeMere {
    public static void main(String[] args) {
        Animal[] animaux = {new Chien(), new Chat(), new Animal()};
        for (Animal a : animaux) {
            System.out.println(a.getClass().getSimpleName() + " : " + a.cri());
        }
        Animal x = new Chat();
        if (x instanceof Chat c) {
            c.ronronner();
        }
    }
}
```

```text
Chien : Wouf
Chat : Miaou
Animal : ...
Rrrr
```

- La boucle traite tous les animaux de la même façon, et chacun répond avec **son** cri : c'est le **polymorphisme**, approfondi au module 4.
- Avec une variable de type `Animal`, on ne peut appeler que les méthodes déclarées dans `Animal`. Pour utiliser `ronronner()`, on teste le type réel avec `instanceof` ; la forme `x instanceof Chat c` (Java moderne) déclare en même temps une variable `c` de type `Chat`.

## La classe Object et final

Toute classe hérite, directement ou non, de la classe **`Object`**. C'est d'elle que viennent `toString()`, `equals(…)` et `getClass()` : voilà pourquoi on écrit `@Override` devant `toString()`.

Le mot clé `final` a deux usages liés à l'héritage :

- `final class Monnaie` : la classe ne peut pas avoir de sous-classe (c'est le cas de `String`) ;
- `final` sur une méthode : elle ne peut pas être redéfinie.

> Conseil : l'héritage crée un lien fort entre classes. Utilisez-le pour de vraies relations « est un » ; pour partager seulement un comportement, les **interfaces** (module 4) sont souvent plus souples.

## À retenir

- `class Fille extends Mere` : la fille hérite des attributs et méthodes ; une seule classe mère en Java.
- `super(…)` appelle le constructeur parent (première instruction) ; `super.methode()` sa version d'une méthode.
- `@Override` redéfinit une méthode héritée et fait vérifier la signature par le compilateur.
- Une variable de type mère peut référencer un objet fille ; la méthode exécutée est celle de l'objet réel.
- Toutes les classes héritent d'`Object` ; `final` empêche l'héritage ou la redéfinition.

## Exercices

### Exercice 1 — Véhicules

Créez une classe `Vehicule` (marque, méthode `description()`) et une sous-classe `Voiture` avec un nombre de portes, qui redéfinit `description()` en réutilisant celle de la mère. Affichez la description d'une Renault 5 portes.

```solution-java
class Vehicule {
    protected String marque;

    Vehicule(String marque) {
        this.marque = marque;
    }

    String description() {
        return "Véhicule " + marque;
    }
}

class Voiture extends Vehicule {
    private int portes;

    Voiture(String marque, int portes) {
        super(marque);
        this.portes = portes;
    }

    @Override
    String description() {
        return super.description() + ", " + portes + " portes";
    }
}

public class TestVehicules {
    public static void main(String[] args) {
        Vehicule v = new Voiture("Renault", 5);
        System.out.println(v.description());
    }
}
```

```text
Véhicule Renault, 5 portes
```

### Exercice 2 — Compte épargne

À partir d'une classe `Compte` (solde, `deposer`), créez `CompteEpargne` avec un taux d'intérêt et une méthode `appliquerInterets()` qui dépose les intérêts. Testez avec 1 000 € à 3 %.

```solution-java
class Compte {
    protected double solde;

    void deposer(double montant) {
        solde += montant;
    }

    double getSolde() {
        return solde;
    }
}

class CompteEpargne extends Compte {
    private final double taux;

    CompteEpargne(double taux) {
        this.taux = taux;
    }

    void appliquerInterets() {
        deposer(solde * taux);
    }
}

public class TestEpargne {
    public static void main(String[] args) {
        CompteEpargne ce = new CompteEpargne(0.03);
        ce.deposer(1000);
        ce.appliquerInterets();
        System.out.println("Solde : " + ce.getSolde());
    }
}
```

```text
Solde : 1030.0
```

`CompteEpargne` n'a pas besoin d'appeler `super(…)` explicitement : `Compte` n'a que le constructeur par défaut, appelé automatiquement.

### Exercice 3 — Héritage ou attribut ?

Pour chaque couple, indiquez s'il faut utiliser l'héritage ou un attribut : (a) `Livre` / `Auteur` ; (b) `Directeur` / `Salarie` ; (c) `Commande` / `Client`.

```solution-text
(a) Attribut : un livre « a un » auteur, il n'« est » pas un auteur.
(b) Héritage : un directeur « est un » salarié → class Directeur extends Salarie.
(c) Attribut : une commande « a un » client.
```
"""

# ---------------------------------------------------------------------------
# Module 4 — Abstraction et collections
# ---------------------------------------------------------------------------
M4_L1 = r"""
## Les classes abstraites

Dans une application de dessin, « une forme » en général n'a pas de sens concret : on dessine des **cercles**, des **rectangles**… On veut pourtant garantir que **toute** forme sait calculer son aire. Une **classe abstraite** sert exactement à cela :

```java
abstract class Forme {
    private final String nom;

    Forme(String nom) {
        this.nom = nom;
    }

    abstract double aire();   // pas de corps : chaque sous-classe doit l'écrire

    String decrire() {
        return String.format("%s d'aire %.2f", nom, aire());
    }
}

class Cercle extends Forme {
    private final double rayon;

    Cercle(double rayon) {
        super("Cercle");
        this.rayon = rayon;
    }

    @Override
    double aire() {
        return Math.PI * rayon * rayon;
    }
}

class Rectangle extends Forme {
    private final double largeur;
    private final double hauteur;

    Rectangle(double largeur, double hauteur) {
        super("Rectangle");
        this.largeur = largeur;
        this.hauteur = hauteur;
    }

    @Override
    double aire() {
        return largeur * hauteur;
    }
}

public class Formes {
    public static void main(String[] args) {
        Forme[] formes = {new Cercle(1), new Rectangle(3, 4), new Cercle(2.5)};
        double total = 0;
        for (Forme f : formes) {
            System.out.println(f.decrire());
            total += f.aire();
        }
        System.out.printf("Aire totale : %.2f%n", total);
    }
}
```

```text
Cercle d'aire 3.14
Rectangle d'aire 12.00
Cercle d'aire 19.63
Aire totale : 34.78
```

- `abstract class Forme` : on **ne peut pas** écrire `new Forme(…)` ; la classe sert de modèle commun.
- `abstract double aire();` : une **méthode abstraite**, sans corps. Toute sous-classe concrète **doit** la redéfinir, sinon le code ne compile pas.
- Une classe abstraite peut contenir des attributs, un constructeur et des méthodes complètes (`decrire`), qui peuvent appeler les méthodes abstraites.

## Les interfaces

Une **interface** décrit une **capacité** : une liste de méthodes qu'une classe s'engage à fournir, sans dire comment. Une classe l'adopte avec `implements`.

```java
interface Payable {
    double montantDu();

    default String libelle() {          // méthode par défaut, avec un corps
        return String.format("%.2f EUR à payer", montantDu());
    }
}

class Facture implements Payable {
    private final double montantHT;

    Facture(double montantHT) {
        this.montantHT = montantHT;
    }

    @Override
    public double montantDu() {
        return montantHT * 1.2;
    }
}

class Abonnement implements Payable {
    private final double mensualite;
    private final int mois;

    Abonnement(double mensualite, int mois) {
        this.mensualite = mensualite;
        this.mois = mois;
    }

    @Override
    public double montantDu() {
        return mensualite * mois;
    }

    @Override
    public String libelle() {
        return mois + " mois d'abonnement : " + Payable.super.libelle();
    }
}

public class Paiements {
    public static void main(String[] args) {
        Payable[] aPayer = {new Facture(100), new Abonnement(9.99, 3)};
        for (Payable p : aPayer) {
            System.out.println(p.libelle());
        }
    }
}
```

```text
120.00 EUR à payer
3 mois d'abonnement : 29.97 EUR à payer
```

- Les méthodes d'une interface sont implicitement `public` : leur implémentation doit donc être déclarée `public`.
- Une méthode `default` fournit un comportement par défaut, que les classes peuvent garder ou redéfinir.
- Une classe peut **implémenter plusieurs interfaces** (`class A implements X, Y`), alors qu'elle n'hérite que d'une seule classe.

## Classe abstraite ou interface ?

| | Classe abstraite | Interface |
|---|---|---|
| Relation | « est un » (famille d'objets) | « sait faire » (capacité) |
| Attributs d'instance | oui | non (seulement des constantes) |
| Constructeur | oui | non |
| Combien par classe ? | une seule (`extends`) | plusieurs (`implements`) |
| Exemple | `Forme`, `Animal` | `Payable`, `Comparable`, `Imprimable` |

En cas de doute, commencez par une **interface** : elle impose moins de contraintes.

## Le polymorphisme

Le **polymorphisme** (« plusieurs formes ») est la capacité de traiter des objets de classes différentes **à travers un type commun**, chacun réagissant à sa manière. Dans les deux exemples ci-dessus, les boucles ne savent pas si elles manipulent un cercle ou un rectangle, une facture ou un abonnement : elles appellent `aire()` ou `libelle()`, et Java exécute la bonne version selon l'objet réel.

Conséquence très pratique : pour ajouter un nouveau type (un `Triangle`, un `Don`), on écrit **une nouvelle classe**, sans toucher au code qui les utilise.

```java
interface Notification {
    void envoyer(String message);
}

class Email implements Notification {
    private final String adresse;

    Email(String adresse) {
        this.adresse = adresse;
    }

    @Override
    public void envoyer(String message) {
        System.out.println("[email " + adresse + "] " + message);
    }
}

class Sms implements Notification {
    private final String numero;

    Sms(String numero) {
        this.numero = numero;
    }

    @Override
    public void envoyer(String message) {
        String court = message.length() > 20 ? message.substring(0, 20) + "…" : message;
        System.out.println("[sms " + numero + "] " + court);
    }
}

public class Notifications {
    static void prevenirTous(Notification[] canaux, String message) {
        for (Notification n : canaux) {
            n.envoyer(message);
        }
    }

    public static void main(String[] args) {
        Notification[] canaux = {new Email("lea@exemple.fr"), new Sms("06 00 00 00 00")};
        prevenirTous(canaux, "Votre commande a été expédiée");
    }
}
```

```text
[email lea@exemple.fr] Votre commande a été expédiée
[sms 06 00 00 00 00] Votre commande a été…
```

La méthode `prevenirTous` dépend seulement de l'interface `Notification` : on pourra demain ajouter une notification par messagerie instantanée sans la modifier.

## Une interface de la bibliothèque standard : Comparable

Java fournit de nombreuses interfaces prêtes à l'emploi. `Comparable<T>` définit un **ordre naturel** grâce à la méthode `compareTo` (négatif si « avant », 0 si égal, positif si « après »). Les méthodes de tri l'utilisent automatiquement :

```java
import java.util.Arrays;

class Joueur implements Comparable<Joueur> {
    final String nom;
    final int score;

    Joueur(String nom, int score) {
        this.nom = nom;
        this.score = score;
    }

    @Override
    public int compareTo(Joueur autre) {
        return Integer.compare(autre.score, this.score);  // score décroissant
    }

    @Override
    public String toString() {
        return nom + "=" + score;
    }
}

public class Classement {
    public static void main(String[] args) {
        Joueur[] joueurs = {new Joueur("Ana", 120), new Joueur("Bilal", 340), new Joueur("Chloé", 210)};
        Arrays.sort(joueurs);
        System.out.println(Arrays.toString(joueurs));
    }
}
```

```text
[Bilal=340, Chloé=210, Ana=120]
```

`<Joueur>` précise le type comparé : c'est un **type générique**, notion que vous retrouverez avec les collections.

## À retenir

- Une classe `abstract` ne s'instancie pas ; ses méthodes `abstract` doivent être redéfinies par les sous-classes.
- Une `interface` décrit une capacité ; une classe peut en implémenter plusieurs avec `implements`.
- Les méthodes d'interface sont publiques ; une méthode `default` a un corps par défaut.
- Polymorphisme : un même appel, sur un type commun, exécute la version de l'objet réel.
- `Comparable` définit l'ordre naturel utilisé par `Arrays.sort`.

## Exercices

### Exercice 1 — Triangle

Ajoutez une classe `Triangle` (base, hauteur) à la hiérarchie `Forme` et affichez sa description pour une base 6 et une hauteur 2.

```solution-java
abstract class Forme {
    private final String nom;

    Forme(String nom) {
        this.nom = nom;
    }

    abstract double aire();

    String decrire() {
        return String.format("%s d'aire %.2f", nom, aire());
    }
}

class Triangle extends Forme {
    private final double base;
    private final double hauteur;

    Triangle(double base, double hauteur) {
        super("Triangle");
        this.base = base;
        this.hauteur = hauteur;
    }

    @Override
    double aire() {
        return base * hauteur / 2;
    }
}

public class TestTriangle {
    public static void main(String[] args) {
        Forme t = new Triangle(6, 2);
        System.out.println(t.decrire());
    }
}
```

```text
Triangle d'aire 6.00
```

### Exercice 2 — Interface Imprimable

Créez une interface `Imprimable` avec une méthode `String imprimer()`, implémentée par `Etudiant` (nom, promotion) et `Salle` (numéro, places). Affichez un tableau contenant un objet de chaque.

```solution-java
interface Imprimable {
    String imprimer();
}

class Etudiant implements Imprimable {
    private final String nom;
    private final int promotion;

    Etudiant(String nom, int promotion) {
        this.nom = nom;
        this.promotion = promotion;
    }

    @Override
    public String imprimer() {
        return "Étudiant " + nom + " (promo " + promotion + ")";
    }
}

class Salle implements Imprimable {
    private final String numero;
    private final int places;

    Salle(String numero, int places) {
        this.numero = numero;
        this.places = places;
    }

    @Override
    public String imprimer() {
        return "Salle " + numero + " : " + places + " places";
    }
}

public class TestImprimable {
    public static void main(String[] args) {
        Imprimable[] elements = {new Etudiant("Sami", 2025), new Salle("B204", 30)};
        for (Imprimable e : elements) {
            System.out.println(e.imprimer());
        }
    }
}
```

```text
Étudiant Sami (promo 2025)
Salle B204 : 30 places
```

### Exercice 3 — Vrai ou faux ?

(a) On peut écrire `new Forme("x")` si `Forme` est abstraite. (b) Une classe peut implémenter deux interfaces. (c) Une interface peut avoir des attributs d'instance.

```solution-text
(a) Faux : une classe abstraite ne peut pas être instanciée directement.
(b) Vrai : class A implements X, Y est autorisé.
(c) Faux : une interface ne contient que des constantes (static final), pas d'état propre à chaque objet.
```
"""

M4_L2 = r"""
## Les limites des tableaux

Un tableau a une **taille fixe** : impossible d'y ajouter un 11ᵉ élément s'il a été créé avec 10 cases. Pour une liste qui grandit ou rétrécit (un panier, des inscrits, des messages), Java propose les **collections**, dans le package `java.util`. La plus utilisée est **`ArrayList`**, une liste ordonnée de taille variable.

## Créer et remplir une ArrayList

```java
import java.util.ArrayList;
import java.util.List;

public class Listes {
    public static void main(String[] args) {
        List<String> courses = new ArrayList<>();
        courses.add("pain");
        courses.add("lait");
        courses.add("pommes");
        courses.add(1, "beurre");        // insère à l'indice 1

        System.out.println(courses);
        System.out.println("Taille : " + courses.size());
        System.out.println("Premier : " + courses.get(0));
        courses.set(2, "lait d'avoine"); // remplace l'élément d'indice 2
        courses.remove("pain");          // retire par valeur
        System.out.println(courses);
        System.out.println(courses.contains("pommes") + " " + courses.indexOf("pommes"));
        System.out.println("Vide ? " + courses.isEmpty());
    }
}
```

```text
[pain, beurre, lait, pommes]
Taille : 4
Premier : pain
[beurre, lait d'avoine, pommes]
true 2
Vide ? false
```

- `List<String>` : le type entre chevrons `< >` est un **paramètre générique** : cette liste ne contient **que** des `String`. Le compilateur refuse `courses.add(42)`.
- On déclare généralement la variable avec l'**interface** `List` et on crée l'objet avec la classe `ArrayList` : le reste du code ne dépend que de `List`. Les chevrons vides `<>` (*diamond*) laissent Java déduire le type.
- Contrairement aux tableaux : `size()` au lieu de `length`, `get(i)` au lieu de `[i]`.

| Méthode | Effet |
|---|---|
| `add(e)` / `add(i, e)` | ajoute à la fin / à la position `i` |
| `get(i)` / `set(i, e)` | lit / remplace l'élément d'indice `i` |
| `remove(i)` / `remove(objet)` | retire par position / par valeur |
| `size()`, `isEmpty()`, `clear()` | taille, test de vide, vidage |
| `contains(e)`, `indexOf(e)` | recherche (avec `equals`) |

## Les types enveloppes

Une collection ne contient que des **objets**, jamais des types primitifs. Pour stocker des nombres, on utilise les **classes enveloppes** (*wrappers*) : `Integer` pour `int`, `Double` pour `double`, `Boolean`, `Character`… Java convertit automatiquement dans les deux sens (*autoboxing*) :

```java
import java.util.ArrayList;
import java.util.List;

public class Enveloppes {
    public static void main(String[] args) {
        List<Integer> notes = new ArrayList<>();
        notes.add(14);   // int → Integer automatiquement
        notes.add(9);
        notes.add(17);
        int somme = 0;
        for (int n : notes) {   // Integer → int automatiquement
            somme += n;
        }
        System.out.println("Somme : " + somme);

        notes.remove(Integer.valueOf(9));  // retire la valeur 9
        notes.remove(0);                   // retire l'élément d'indice 0
        System.out.println(notes);
    }
}
```

```text
Somme : 40
[17]
```

> Piège : avec une `List<Integer>`, `remove(0)` retire l'élément **d'indice** 0. Pour retirer la **valeur** 9, écrivez `remove(Integer.valueOf(9))`.

## Parcourir une liste

```java
import java.util.ArrayList;
import java.util.List;

public class Parcourir {
    public static void main(String[] args) {
        List<String> inscrits = new ArrayList<>(List.of("Léa", "Omar", "Jade", "Tom"));

        for (String nom : inscrits) {                   // for-each
            System.out.print(nom + " ");
        }
        System.out.println();

        for (int i = 0; i < inscrits.size(); i++) {    // avec l'indice
            System.out.println((i + 1) + ". " + inscrits.get(i));
        }

        inscrits.removeIf(nom -> nom.length() <= 3);    // supprime selon une condition
        System.out.println(inscrits);
    }
}
```

```text
Léa Omar Jade Tom
1. Léa
2. Omar
3. Jade
4. Tom
[Omar, Jade]
```

- `List.of(…)` crée une liste **non modifiable** ; on la copie dans une `ArrayList` pour pouvoir la modifier ensuite. Appeler `add` sur le résultat de `List.of` provoque une `UnsupportedOperationException`.
- `nom -> nom.length() <= 3` est une **lambda** : une petite fonction anonyme (paramètre `nom`, résultat après la flèche). `removeIf` l'applique à chaque élément et retire ceux pour lesquels elle vaut `true`.

> Ne retirez pas d'éléments **pendant** une boucle for-each sur la même liste : Java lève une `ConcurrentModificationException`. Utilisez `removeIf`.

## Trier une liste

```java
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

class Produit {
    final String nom;
    final double prix;

    Produit(String nom, double prix) {
        this.nom = nom;
        this.prix = prix;
    }

    @Override
    public String toString() {
        return nom + " (" + prix + ")";
    }
}

public class Tri {
    public static void main(String[] args) {
        List<Integer> nombres = new ArrayList<>(List.of(42, 7, 19, 3));
        Collections.sort(nombres);                     // ordre naturel
        System.out.println(nombres);

        List<Produit> catalogue = new ArrayList<>();
        catalogue.add(new Produit("Souris", 19.9));
        catalogue.add(new Produit("Écran", 149.0));
        catalogue.add(new Produit("Câble", 7.5));

        catalogue.sort(Comparator.comparingDouble(p -> p.prix));
        System.out.println(catalogue);
        catalogue.sort(Comparator.comparing((Produit p) -> p.nom).reversed());
        System.out.println(catalogue);
    }
}
```

```text
[3, 7, 19, 42]
[Câble (7.5), Souris (19.9), Écran (149.0)]
[Écran (149.0), Souris (19.9), Câble (7.5)]
```

- `Collections.sort` trie selon l'**ordre naturel** (nombres croissants, texte alphabétique), défini par `Comparable`.
- `liste.sort(comparateur)` trie selon un critère choisi ; `Comparator.comparing…` fabrique ce critère à partir d'une lambda, `reversed()` inverse l'ordre.
- Le tri des chaînes compare les **codes des caractères** : les lettres accentuées comme `É` sont classées après les lettres sans accent. Pour un ordre alphabétique adapté au français, Java propose la classe `java.text.Collator`.

## À retenir

- `List<Type> liste = new ArrayList<>();` crée une liste de taille variable, d'un seul type d'éléments.
- `add`, `get`, `set`, `remove`, `size`, `contains`, `indexOf` sont les méthodes de base.
- Les collections contiennent des objets : `Integer`, `Double`… avec conversion automatique.
- Parcours par for-each ou par indice ; suppression conditionnelle avec `removeIf`.
- Tri : `Collections.sort` (ordre naturel) ou `liste.sort(Comparator.comparing(…))`.

## Exercices

### Exercice 1 — Liste de notes

Créez une `List<Double>` avec 12.5, 8, 15 et 17.5, ajoutez 10, puis affichez la moyenne et la liste triée.

```solution-java
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Notes {
    public static void main(String[] args) {
        List<Double> notes = new ArrayList<>(List.of(12.5, 8.0, 15.0, 17.5));
        notes.add(10.0);
        double somme = 0;
        for (double n : notes) {
            somme += n;
        }
        System.out.println("Moyenne : " + somme / notes.size());
        Collections.sort(notes);
        System.out.println("Triées : " + notes);
    }
}
```

```text
Moyenne : 12.6
Triées : [8.0, 10.0, 12.5, 15.0, 17.5]
```

Avec une `List<Double>`, écrivez `8.0` et non `8` : le littéral `8` est un `int`, qui ne peut pas être converti automatiquement en `Double`.

### Exercice 2 — Filtrer des mots

À partir de `"java est un langage robuste et portable"`, construisez une liste des mots de plus de 4 lettres, en majuscules.

```solution-java
import java.util.ArrayList;
import java.util.List;

public class FiltreMots {
    public static void main(String[] args) {
        String phrase = "java est un langage robuste et portable";
        List<String> longs = new ArrayList<>();
        for (String mot : phrase.split(" ")) {
            if (mot.length() > 4) {
                longs.add(mot.toUpperCase());
            }
        }
        System.out.println(longs);
    }
}
```

```text
[LANGAGE, ROBUSTE, PORTABLE]
```

`split(" ")` découpe une chaîne en un tableau de morceaux, selon le séparateur indiqué.

### Exercice 3 — Classement de produits

Avec la classe `Produit` de la leçon, triez une liste de trois produits du plus cher au moins cher et affichez seulement le nom du plus cher.

```solution-java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

class Produit {
    final String nom;
    final double prix;

    Produit(String nom, double prix) {
        this.nom = nom;
        this.prix = prix;
    }
}

public class PlusCher {
    public static void main(String[] args) {
        List<Produit> produits = new ArrayList<>();
        produits.add(new Produit("Casque", 59.0));
        produits.add(new Produit("Clavier", 89.0));
        produits.add(new Produit("Tapis", 12.0));
        produits.sort(Comparator.comparingDouble((Produit p) -> p.prix).reversed());
        System.out.println("Le plus cher : " + produits.get(0).nom);
    }
}
```

```text
Le plus cher : Clavier
```
"""

M4_L3 = r"""
## Associer une clé à une valeur

Une liste range des éléments **par position**. Souvent, on veut plutôt retrouver une information **par un identifiant** : le prix d'un produit à partir de sa référence, le numéro de téléphone d'un contact à partir de son nom. C'est le rôle d'une **Map** (dictionnaire, ou table d'association) : chaque **clé** unique est associée à une **valeur**.

L'implémentation la plus courante est **`HashMap`**, très rapide pour retrouver une valeur à partir de sa clé.

```java
import java.util.HashMap;
import java.util.Map;

public class Annuaire {
    public static void main(String[] args) {
        Map<String, String> telephones = new HashMap<>();
        telephones.put("Amina", "06 11 22 33 44");
        telephones.put("Lucas", "07 55 66 77 88");
        telephones.put("Amina", "06 99 99 99 99");   // même clé : la valeur est remplacée

        System.out.println(telephones.get("Amina"));
        System.out.println(telephones.get("Zoé"));            // clé absente
        System.out.println(telephones.containsKey("Lucas"));
        System.out.println(telephones.getOrDefault("Zoé", "inconnu"));
        System.out.println("Taille : " + telephones.size());
        telephones.remove("Lucas");
        System.out.println("Après suppression : " + telephones.size());
    }
}
```

```text
06 99 99 99 99
null
true
inconnu
Taille : 2
Après suppression : 1
```

- `Map<String, String>` : deux paramètres génériques, le type des **clés** puis celui des **valeurs**.
- `put` ajoute ou **remplace** : une clé ne peut apparaître qu'une fois.
- `get` renvoie `null` si la clé est absente ; `getOrDefault` permet de fournir une valeur de repli.

| Méthode | Effet |
|---|---|
| `put(k, v)` | associe `v` à la clé `k` (remplace l'ancienne valeur) |
| `get(k)`, `getOrDefault(k, d)` | lit la valeur (ou `null` / `d` si absente) |
| `containsKey(k)`, `containsValue(v)` | teste la présence |
| `remove(k)` | supprime l'association |
| `size()`, `isEmpty()` | taille, test de vide |
| `keySet()`, `values()`, `entrySet()` | clés, valeurs, couples clé-valeur |

## Compter des occurrences

Un usage très fréquent : compter combien de fois apparaît chaque élément. La méthode `merge` simplifie ce travail :

```java
import java.util.HashMap;
import java.util.Map;
import java.util.TreeMap;

public class Comptage {
    public static void main(String[] args) {
        String texte = "le chat et le chien et le poisson";
        Map<String, Integer> compteur = new HashMap<>();
        for (String mot : texte.split(" ")) {
            compteur.merge(mot, 1, Integer::sum);
        }
        System.out.println(compteur.get("le") + " " + compteur.get("et") + " " + compteur.get("chat"));
        System.out.println(new TreeMap<>(compteur));
    }
}
```

```text
3 2 1
{chat=1, chien=1, et=2, le=3, poisson=1}
```

- `compteur.merge(mot, 1, Integer::sum)` : si `mot` est absent, on lui associe `1` ; sinon on **additionne** `1` à la valeur existante. `Integer::sum` est une **référence de méthode**, une écriture compacte de la lambda `(a, b) -> a + b`.
- Une écriture équivalente, plus longue : `compteur.put(mot, compteur.getOrDefault(mot, 0) + 1);`.

## L'ordre des clés

Une `HashMap` **ne garantit aucun ordre** de parcours : l'ordre d'affichage peut sembler aléatoire et changer quand on ajoute des éléments. Choisissez l'implémentation selon votre besoin :

| Implémentation | Ordre de parcours |
|---|---|
| `HashMap` | aucun ordre garanti (la plus utilisée) |
| `LinkedHashMap` | ordre d'insertion |
| `TreeMap` | clés triées (ordre naturel) |

C'est pourquoi l'exemple précédent copie la map dans une `TreeMap` avant de l'afficher : le résultat est trié par ordre alphabétique des clés, donc prévisible.

## Parcourir une Map

```java
import java.util.LinkedHashMap;
import java.util.Map;

public class Stock {
    public static void main(String[] args) {
        Map<String, Integer> stock = new LinkedHashMap<>();
        stock.put("stylos", 120);
        stock.put("cahiers", 8);
        stock.put("classeurs", 35);

        for (Map.Entry<String, Integer> e : stock.entrySet()) {
            String alerte = e.getValue() < 10 ? "  <- à commander" : "";
            System.out.println(e.getKey() + " : " + e.getValue() + alerte);
        }

        int total = 0;
        for (int quantite : stock.values()) {
            total += quantite;
        }
        System.out.println("Articles en stock : " + total);
        System.out.println("Références : " + stock.keySet());
    }
}
```

```text
stylos : 120
cahiers : 8  <- à commander
classeurs : 35
Articles en stock : 163
Références : [stylos, cahiers, classeurs]
```

- `entrySet()` donne les couples ; chaque `Map.Entry` offre `getKey()` et `getValue()`.
- `keySet()` donne les clés, `values()` les valeurs.

## Des objets comme valeurs

Les valeurs d'une map peuvent être n'importe quels objets, y compris des listes. Exemple : regrouper des élèves par classe.

```java
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

public class Groupes {
    public static void main(String[] args) {
        String[][] eleves = {{"Inès", "6A"}, {"Noah", "6B"}, {"Lina", "6A"}, {"Adam", "6B"}, {"Maël", "6C"}};
        Map<String, List<String>> parClasse = new TreeMap<>();
        for (String[] eleve : eleves) {
            String nom = eleve[0];
            String classe = eleve[1];
            parClasse.computeIfAbsent(classe, c -> new ArrayList<>()).add(nom);
        }
        for (String classe : parClasse.keySet()) {
            List<String> noms = parClasse.get(classe);
            System.out.println(classe + " (" + noms.size() + ") : " + noms);
        }
    }
}
```

```text
6A (2) : [Inès, Lina]
6B (2) : [Noah, Adam]
6C (1) : [Maël]
```

`computeIfAbsent(classe, c -> new ArrayList<>())` renvoie la liste associée à `classe`, en la **créant** d'abord si elle n'existe pas encore : une seule ligne pour « ajouter l'élève dans le bon groupe ».

> Une clé de map doit avoir des méthodes `equals` et `hashCode` cohérentes. `String`, `Integer` et les records (module 5) les fournissent ; pour vos propres classes utilisées comme clés, il faudrait les redéfinir.

## À retenir

- `Map<K, V> m = new HashMap<>();` associe des clés uniques à des valeurs.
- `put` ajoute ou remplace ; `get` renvoie `null` si la clé manque ; `getOrDefault` fournit une valeur de repli.
- `merge(cle, 1, Integer::sum)` compte des occurrences ; `computeIfAbsent` crée une valeur à la demande.
- `HashMap` : pas d'ordre ; `LinkedHashMap` : ordre d'insertion ; `TreeMap` : clés triées.
- Parcours avec `entrySet()`, `keySet()` ou `values()`.

## Exercices

### Exercice 1 — Prix des produits

Créez une map référence → prix avec trois produits, augmentez de 10 % le prix de `"REF-2"`, puis affichez toutes les références triées avec leur prix sur deux décimales.

```solution-java
import java.util.Map;
import java.util.TreeMap;

public class Prix {
    public static void main(String[] args) {
        Map<String, Double> prix = new TreeMap<>();
        prix.put("REF-3", 4.0);
        prix.put("REF-1", 12.5);
        prix.put("REF-2", 20.0);
        prix.put("REF-2", prix.get("REF-2") * 1.1);
        for (Map.Entry<String, Double> e : prix.entrySet()) {
            System.out.printf("%s : %.2f%n", e.getKey(), e.getValue());
        }
    }
}
```

```text
REF-1 : 12.50
REF-2 : 22.00
REF-3 : 4.00
```

### Exercice 2 — Fréquence des lettres

Comptez les lettres du mot `"bibliotheque"` avec une `TreeMap<Character, Integer>` et affichez le résultat.

```solution-java
import java.util.Map;
import java.util.TreeMap;

public class Lettres {
    public static void main(String[] args) {
        String mot = "bibliotheque";
        Map<Character, Integer> frequences = new TreeMap<>();
        for (char c : mot.toCharArray()) {
            frequences.merge(c, 1, Integer::sum);
        }
        System.out.println(frequences);
    }
}
```

```text
{b=2, e=2, h=1, i=2, l=1, o=1, q=1, t=1, u=1}
```

`toCharArray()` transforme une chaîne en tableau de caractères, parcourable avec for-each.

### Exercice 3 — Quelle implémentation ?

Quelle Map choisir pour : (a) un cache de recherche rapide où l'ordre n'importe pas ; (b) un historique où l'on veut garder l'ordre d'ajout ; (c) un index alphabétique ?

```solution-text
(a) HashMap : la plus simple et rapide, sans ordre garanti.
(b) LinkedHashMap : conserve l'ordre d'insertion.
(c) TreeMap : maintient les clés triées.
```
"""

# ---------------------------------------------------------------------------
# Module 5 — Exceptions, records et projet
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Qu'est-ce qu'une exception ?

Une **exception** est un objet qui signale un problème survenu **pendant l'exécution** : division par zéro, texte qui n'est pas un nombre, indice hors d'un tableau, fichier introuvable… Quand une exception est **levée** et que personne ne la traite, le programme s'arrête et affiche la pile d'appels :

```java
public class Plantage {
    public static void main(String[] args) {
        int[] notes = {12, 15, 9};
        System.out.println("Début");
        System.out.println(notes[3]);
        System.out.println("Fin");
    }
}
```

```text
Début
Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 3 out of bounds for length 3
	at Plantage.main(Plantage.java:5)
```

« Fin » ne s'affiche jamais. Pour qu'un programme résiste aux erreurs prévisibles (une saisie invalide, par exemple), on **intercepte** les exceptions.

## try / catch

On place le code risqué dans un bloc `try`, et le traitement de l'erreur dans un bloc `catch` qui précise **quel type** d'exception il intercepte :

```java
public class Conversion {
    static int lireEntier(String texte) {
        try {
            return Integer.parseInt(texte);
        } catch (NumberFormatException e) {
            System.out.println("« " + texte + " » n'est pas un nombre (" + e.getMessage() + ")");
            return 0;
        }
    }

    public static void main(String[] args) {
        System.out.println(lireEntier("42"));
        System.out.println(lireEntier("quarante"));
        System.out.println("Le programme continue.");
    }
}
```

```text
42
« quarante » n'est pas un nombre (For input string: "quarante")
0
Le programme continue.
```

- Si aucune exception ne survient, le `catch` est ignoré.
- Si une exception survient dans le `try`, l'exécution **saute** immédiatement au `catch` correspondant ; le reste du `try` n'est pas exécuté.
- La variable `e` est l'objet exception : `e.getMessage()` donne son message.

## Plusieurs catch et finally

```java
public class Plusieurs {
    static void traiter(String[] valeurs, int indice) {
        try {
            int n = Integer.parseInt(valeurs[indice]);
            System.out.println("100 / " + n + " = " + (100 / n));
        } catch (NumberFormatException e) {
            System.out.println("Valeur non numérique");
        } catch (ArithmeticException | ArrayIndexOutOfBoundsException e) {
            System.out.println("Calcul impossible : " + e.getMessage());
        } finally {
            System.out.println("-- fin du traitement " + indice);
        }
    }

    public static void main(String[] args) {
        String[] valeurs = {"4", "abc", "0"};
        for (int i = 0; i <= 3; i++) {
            traiter(valeurs, i);
        }
    }
}
```

```text
100 / 4 = 25
-- fin du traitement 0
Valeur non numérique
-- fin du traitement 1
Calcul impossible : / by zero
-- fin du traitement 2
Calcul impossible : Index 3 out of bounds for length 3
-- fin du traitement 3
```

- Les `catch` sont testés dans l'ordre ; le premier qui correspond est exécuté.
- `catch (A | B e)` intercepte plusieurs types avec le même traitement.
- Le bloc `finally` s'exécute **dans tous les cas**, erreur ou non : on y place le nettoyage (fermer une ressource, afficher un bilan).

> N'interceptez pas une exception pour l'ignorer silencieusement (`catch (Exception e) {}`) : l'erreur disparaît mais le problème reste, et il devient très difficile à trouver.

## Lever une exception : throw

Votre code peut lui aussi **signaler** une situation anormale avec `throw`. C'est ce que vous avez fait pour valider des arguments au module 3 :

```java
public class Retrait {
    static double retirer(double solde, double montant) {
        if (montant <= 0) {
            throw new IllegalArgumentException("Le montant doit être positif");
        }
        if (montant > solde) {
            throw new IllegalStateException("Solde insuffisant : " + solde);
        }
        return solde - montant;
    }

    public static void main(String[] args) {
        double[] demandes = {30, -5, 500};
        double solde = 100;
        for (double d : demandes) {
            try {
                solde = retirer(solde, d);
                System.out.println("Retrait de " + d + " OK, solde : " + solde);
            } catch (IllegalArgumentException | IllegalStateException e) {
                System.out.println("Refusé : " + e.getMessage());
            }
        }
    }
}
```

```text
Retrait de 30.0 OK, solde : 70.0
Refusé : Le montant doit être positif
Refusé : Solde insuffisant : 70.0
```

## Exceptions vérifiées et non vérifiées

Java distingue deux familles :

| Famille | Hérite de | Le compilateur oblige-t-il à la traiter ? | Exemples |
|---|---|---|---|
| **Non vérifiées** (*unchecked*) | `RuntimeException` | non | `NullPointerException`, `IllegalArgumentException`, `ArithmeticException` |
| **Vérifiées** (*checked*) | `Exception` (hors `RuntimeException`) | **oui** | `IOException` (lecture de fichier), exceptions métier |

Une méthode susceptible de lever une exception vérifiée doit soit la **traiter** (`try/catch`), soit l'**annoncer** dans sa signature avec `throws`, pour que l'appelant s'en charge. Les exceptions non vérifiées signalent plutôt des **erreurs de programmation** (à corriger dans le code) ; les vérifiées, des situations **prévisibles** que l'appelant doit gérer.

## Créer sa propre exception

Pour exprimer une erreur métier, on crée une classe qui hérite d'`Exception` (vérifiée) ou de `RuntimeException` (non vérifiée) :

```java
class StockInsuffisantException extends Exception {
    StockInsuffisantException(String message) {
        super(message);
    }
}

class Entrepot {
    private int stock = 5;

    void sortir(int quantite) throws StockInsuffisantException {
        if (quantite > stock) {
            throw new StockInsuffisantException("Demande " + quantite + ", disponible " + stock);
        }
        stock -= quantite;
    }

    int getStock() {
        return stock;
    }
}

public class Commandes {
    public static void main(String[] args) {
        Entrepot entrepot = new Entrepot();
        int[] commandes = {2, 4, 3};
        for (int q : commandes) {
            try {
                entrepot.sortir(q);
                System.out.println("Commande de " + q + " expédiée, reste " + entrepot.getStock());
            } catch (StockInsuffisantException e) {
                System.out.println("Commande de " + q + " en attente : " + e.getMessage());
            }
        }
    }
}
```

```text
Commande de 2 expédiée, reste 3
Commande de 4 en attente : Demande 4, disponible 3
Commande de 3 expédiée, reste 0
```

Si vous supprimez le `try/catch` dans `main`, le code **ne compile plus** (*unreported exception StockInsuffisantException*) : le compilateur vous oblige à prévoir ce cas.

## try-with-resources

Certaines ressources (fichiers, connexions, `Scanner`) doivent être **fermées** après usage. La forme `try (…)` les ferme automatiquement, même en cas d'exception :

```java
import java.util.Scanner;

public class Ressources {
    public static void main(String[] args) {
        try (Scanner sc = new Scanner("10 20 x 30")) {
            int somme = 0;
            while (sc.hasNext()) {
                if (sc.hasNextInt()) {
                    somme += sc.nextInt();
                } else {
                    System.out.println("Ignoré : " + sc.next());
                }
            }
            System.out.println("Somme : " + somme);
        }   // sc.close() est appelé automatiquement ici
    }
}
```

```text
Ignoré : x
Somme : 60
```

Remarquez `hasNextInt()` : tester **avant** de lire évite l'exception, ce qui est souvent préférable à un `try/catch` pour une erreur prévisible.

## À retenir

- Une exception non traitée arrête le programme et affiche la pile d'appels.
- `try { … } catch (Type e) { … }` intercepte ; plusieurs `catch` ou `catch (A | B e)` ; `finally` s'exécute toujours.
- `throw new …Exception("message")` signale une erreur ; `e.getMessage()` la décrit.
- Exceptions **vérifiées** : à traiter ou à déclarer avec `throws` ; **non vérifiées** (`RuntimeException`) : erreurs de programmation.
- `try (ressource) { … }` ferme automatiquement la ressource ; ne jamais ignorer silencieusement une exception.

## Exercices

### Exercice 1 — Division sécurisée

Écrivez `diviser(String a, String b)` qui convertit les deux textes et affiche le quotient entier, ou un message clair si la conversion échoue ou si le diviseur est nul. Testez avec `("20", "4")`, `("20", "zéro")` et `("20", "0")`.

```solution-java
public class DivisionSure {
    static void diviser(String a, String b) {
        try {
            int x = Integer.parseInt(a);
            int y = Integer.parseInt(b);
            System.out.println(x + " / " + y + " = " + (x / y));
        } catch (NumberFormatException e) {
            System.out.println("Saisie invalide : " + a + ", " + b);
        } catch (ArithmeticException e) {
            System.out.println("Division par zéro impossible");
        }
    }

    public static void main(String[] args) {
        diviser("20", "4");
        diviser("20", "zéro");
        diviser("20", "0");
    }
}
```

```text
20 / 4 = 5
Saisie invalide : 20, zéro
Division par zéro impossible
```

### Exercice 2 — Âge valide

Écrivez `verifierAge(int age)` qui lève une `IllegalArgumentException` si l'âge est hors de [0, 130], puis testez-la avec 25 et 150 en interceptant l'erreur.

```solution-java
public class Age {
    static int verifierAge(int age) {
        if (age < 0 || age > 130) {
            throw new IllegalArgumentException("Âge invalide : " + age);
        }
        return age;
    }

    public static void main(String[] args) {
        int[] ages = {25, 150};
        for (int a : ages) {
            try {
                System.out.println("Âge accepté : " + verifierAge(a));
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
        }
    }
}
```

```text
Âge accepté : 25
Âge invalide : 150
```

### Exercice 3 — Vérifiée ou non ?

Classez : (a) `NullPointerException` ; (b) une `IOException` levée à la lecture d'un fichier ; (c) votre `StockInsuffisantException extends Exception` ; (d) `NumberFormatException`.

```solution-text
(a) Non vérifiée : hérite de RuntimeException (erreur de programmation).
(b) Vérifiée : le compilateur oblige à la traiter ou à la déclarer avec throws.
(c) Vérifiée : elle hérite directement d'Exception.
(d) Non vérifiée : elle hérite (indirectement) de RuntimeException.
```
"""

M5_L2 = r"""
## Des classes qui ne font que porter des données

Beaucoup de classes servent uniquement à **transporter des données** : un point (x, y), une adresse, une ligne de commande. Écrites « à la main », elles demandent beaucoup de code répétitif : attributs `private final`, constructeur, getters, `toString`, `equals`, `hashCode`. Le **record**, introduit dans le Java moderne (disponible en Java 17), génère tout cela en une ligne.

```java
record Point(int x, int y) { }

public class Records {
    public static void main(String[] args) {
        Point p = new Point(3, 4);
        System.out.println(p);
        System.out.println(p.x() + " " + p.y());

        Point q = new Point(3, 4);
        System.out.println(p.equals(q));
        System.out.println(p == q);
    }
}
```

```text
Point[x=3, y=4]
3 4
true
false
```

La déclaration `record Point(int x, int y)` fournit automatiquement :

- deux attributs `private final` : `x` et `y` ;
- un **constructeur** qui prend `x` et `y` ;
- des **accesseurs** `x()` et `y()` (sans le préfixe `get`) ;
- un `toString()` lisible, ainsi que `equals` et `hashCode` basés sur **les valeurs** : deux records aux composantes égales sont égaux (`equals` vaut `true`), même s'ils sont deux objets distincts (`==` vaut `false`).

## Les records sont immuables

Les composantes d'un record sont `final` : impossible de les modifier après la création. Pour « changer » une valeur, on crée un **nouveau** record :

```java
record Prix(String produit, double montant) {
    Prix avecRemise(double pourcentage) {
        return new Prix(produit, montant * (1 - pourcentage / 100));
    }
}

public class Immuable {
    public static void main(String[] args) {
        Prix original = new Prix("Chaise", 80);
        Prix solde = original.avecRemise(25);
        System.out.println(original);
        System.out.println(solde);
    }
}
```

```text
Prix[produit=Chaise, montant=80.0]
Prix[produit=Chaise, montant=60.0]
```

Un objet **immuable** est plus simple à comprendre : personne ne peut le modifier « dans votre dos », on peut le partager sans risque. Un record peut contenir des méthodes (comme `avecRemise`) et des méthodes `static`, mais pas d'attributs d'instance supplémentaires.

## Valider dans un constructeur compact

Pour vérifier les valeurs à la création, on écrit un **constructeur compact** : sans liste de paramètres, il s'exécute avant l'affectation des composantes.

```java
record Email(String adresse) {
    Email {
        if (adresse == null || !adresse.contains("@")) {
            throw new IllegalArgumentException("Adresse invalide : " + adresse);
        }
        adresse = adresse.trim().toLowerCase();   // normalisation
    }
}

public class Validation {
    public static void main(String[] args) {
        System.out.println(new Email("  Lea.Martin@Exemple.fr "));
        try {
            new Email("pas-une-adresse");
        } catch (IllegalArgumentException e) {
            System.out.println("Refusé : " + e.getMessage());
        }
    }
}
```

```text
Email[adresse=lea.martin@exemple.fr]
Refusé : Adresse invalide : pas-une-adresse
```

Dans le constructeur compact, `adresse` désigne le **paramètre** ; on peut le réaffecter (ici pour le normaliser) avant qu'il ne soit rangé dans le record.

## Records et collections

Grâce à leurs `equals` et `hashCode`, les records s'utilisent naturellement dans les listes et comme **clés de map** :

```java
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

record Vente(String vendeur, String produit, int quantite) { }

record Case(int ligne, int colonne) { }

public class Collections2 {
    public static void main(String[] args) {
        List<Vente> ventes = new ArrayList<>(List.of(
            new Vente("Nora", "clavier", 3),
            new Vente("Paul", "souris", 10),
            new Vente("Nora", "écran", 1)
        ));
        ventes.sort(Comparator.comparingInt(Vente::quantite).reversed());
        for (Vente v : ventes) {
            System.out.println(v.vendeur() + " : " + v.quantite() + " " + v.produit());
        }

        Map<Case, String> plateau = new HashMap<>();
        plateau.put(new Case(0, 0), "X");
        plateau.put(new Case(1, 1), "O");
        System.out.println(plateau.get(new Case(1, 1)));   // nouvel objet, même valeur
        System.out.println(plateau.containsKey(new Case(2, 2)));
    }
}
```

```text
Paul : 10 souris
Nora : 3 clavier
Nora : 1 écran
O
false
```

`plateau.get(new Case(1, 1))` fonctionne avec un **autre objet** que celui utilisé pour `put` : la map compare les clés avec `equals`, que le record définit d'après les valeurs. Avec une classe ordinaire sans `equals` redéfini, ce `get` renverrait `null`.

`Vente::quantite` est une référence de méthode équivalente à la lambda `v -> v.quantite()`.

## Bonus : les énumérations

Pour une valeur qui ne peut prendre qu'un **ensemble fixe** de possibilités (jours, statuts, niveaux), on utilise une **énumération** (`enum`). Elle se marie bien avec les records et le `switch` :

```java
enum Statut { EN_ATTENTE, EXPEDIEE, LIVREE }

record Commande(int numero, Statut statut) { }

public class Enums {
    public static void main(String[] args) {
        Commande c = new Commande(1042, Statut.EXPEDIEE);
        String message = switch (c.statut()) {
            case EN_ATTENTE -> "en préparation";
            case EXPEDIEE -> "en route";
            case LIVREE -> "livrée";
        };
        System.out.println("Commande " + c.numero() + " : " + message);
        System.out.println(Statut.values().length + " statuts possibles");
    }
}
```

```text
Commande 1042 : en route
3 statuts possibles
```

Ici, le `switch` n'a pas besoin de `default` : tous les cas de l'énumération sont couverts, et le compilateur le vérifie.

## Record ou classe ?

| Choisissez un **record** si… | Choisissez une **classe** si… |
|---|---|
| l'objet représente une **valeur** (point, prix, adresse) | l'objet a un **état qui évolue** (compte, livre emprunté ou non) |
| ses données ne changent pas après création | il faut modifier ses attributs |
| l'égalité dépend des valeurs | l'identité compte (deux comptes identiques restent deux comptes) |

## À retenir

- `record Nom(type a, type b) { }` génère attributs `final`, constructeur, accesseurs `a()`, `toString`, `equals` et `hashCode`.
- Un record est **immuable** : pour changer une valeur, on crée un nouveau record.
- Le **constructeur compact** valide ou normalise les valeurs à la création.
- Deux records aux mêmes valeurs sont `equals` : idéal comme clé de map ou élément de liste.
- `enum` représente un ensemble fixe de valeurs, compatible avec un `switch` exhaustif.

## Exercices

### Exercice 1 — Record Personne

Déclarez `record Personne(String nom, int age)` avec une méthode `estMajeure()`, puis affichez une personne de 17 ans et le résultat de la méthode.

```solution-java
record Personne(String nom, int age) {
    boolean estMajeure() {
        return age >= 18;
    }
}

public class TestPersonne {
    public static void main(String[] args) {
        Personne p = new Personne("Elio", 17);
        System.out.println(p + " majeure ? " + p.estMajeure());
    }
}
```

```text
Personne[nom=Elio, age=17] majeure ? false
```

### Exercice 2 — Intervalle validé

Déclarez `record Intervalle(int debut, int fin)` dont le constructeur compact refuse `debut > fin`, et une méthode `longueur()`. Testez avec (2, 9) puis (5, 1).

```solution-java
record Intervalle(int debut, int fin) {
    Intervalle {
        if (debut > fin) {
            throw new IllegalArgumentException("debut > fin : " + debut + " > " + fin);
        }
    }

    int longueur() {
        return fin - debut;
    }
}

public class TestIntervalle {
    public static void main(String[] args) {
        Intervalle i = new Intervalle(2, 9);
        System.out.println(i + " longueur " + i.longueur());
        try {
            new Intervalle(5, 1);
        } catch (IllegalArgumentException e) {
            System.out.println("Erreur : " + e.getMessage());
        }
    }
}
```

```text
Intervalle[debut=2, fin=9] longueur 7
Erreur : debut > fin : 5 > 1
```

### Exercice 3 — Total par vendeur

Avec le record `Vente` de la leçon et les trois ventes données, calculez la quantité totale vendue par vendeur dans une `TreeMap`.

```solution-java
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

record Vente(String vendeur, String produit, int quantite) { }

public class TotalVendeurs {
    public static void main(String[] args) {
        List<Vente> ventes = List.of(
            new Vente("Nora", "clavier", 3),
            new Vente("Paul", "souris", 10),
            new Vente("Nora", "écran", 1)
        );
        Map<String, Integer> totaux = new TreeMap<>();
        for (Vente v : ventes) {
            totaux.merge(v.vendeur(), v.quantite(), Integer::sum);
        }
        System.out.println(totaux);
    }
}
```

```text
{Nora=4, Paul=10}
```
"""

M5_L3 = r"""
## Le projet

Vous allez réaliser une application console de **gestion de bibliothèque**. Elle mobilise toute la formation : classes et encapsulation, héritage d'exception, records, `ArrayList`, `HashMap`, `switch`, boucles, méthodes et gestion des erreurs.

Fonctionnalités attendues :

1. ajouter des livres au catalogue (ISBN, titre, auteur, année) ;
2. afficher le catalogue trié par titre, avec la disponibilité de chaque livre ;
3. rechercher des livres par mot-clé (titre ou auteur, sans tenir compte des majuscules) ;
4. emprunter et rendre un livre, en refusant les opérations impossibles avec un message clair ;
5. afficher des statistiques : nombre de livres par auteur et emprunts en cours.

L'application lit des **commandes texte** (`liste`, `chercher java`, `emprunter <isbn> <membre>`, `rendre <isbn>`, `stats`). Pour que le programme soit testable sans clavier, la méthode `main` exécute une **liste de commandes** préparée ; vous la brancherez ensuite sur le clavier.

## La conception

| Élément | Type | Pourquoi |
|---|---|---|
| `Livre` | classe | son état **évolue** (disponible ou emprunté) : attributs privés, méthodes `emprunter` / `rendre` |
| `Emprunt` | record | une **valeur** immuable : quel livre, quel membre, quelle date |
| `BibliothequeException` | exception vérifiée | les erreurs métier (livre inconnu, déjà emprunté) doivent être traitées par l'appelant |
| `Bibliotheque` | classe | gère le catalogue (`Map` ISBN → livre) et les emprunts (`List`) |
| `GestionBibliotheque` | classe principale | interprète les commandes et affiche les résultats |

Le catalogue est une `HashMap<String, Livre>` : retrouver un livre par son ISBN est immédiat. Pour l'affichage, on copie les livres dans une liste triée par titre.

> Dans un vrai projet, chaque classe serait dans son propre fichier. Ici, tout tient dans `GestionBibliotheque.java` pour pouvoir le compiler et l'exécuter d'un coup.

## Le programme complet

```java
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

class BibliothequeException extends Exception {
    BibliothequeException(String message) {
        super(message);
    }
}

class Livre {
    private final String isbn;
    private final String titre;
    private final String auteur;
    private final int annee;
    private boolean disponible = true;

    Livre(String isbn, String titre, String auteur, int annee) {
        if (isbn.isBlank() || titre.isBlank()) {
            throw new IllegalArgumentException("ISBN et titre obligatoires");
        }
        this.isbn = isbn;
        this.titre = titre;
        this.auteur = auteur;
        this.annee = annee;
    }

    String getIsbn() { return isbn; }
    String getTitre() { return titre; }
    String getAuteur() { return auteur; }
    boolean isDisponible() { return disponible; }

    void emprunter() throws BibliothequeException {
        if (!disponible) {
            throw new BibliothequeException("« " + titre + " » est déjà emprunté");
        }
        disponible = false;
    }

    void rendre() throws BibliothequeException {
        if (disponible) {
            throw new BibliothequeException("« " + titre + " » n'était pas emprunté");
        }
        disponible = true;
    }

    boolean correspond(String motCle) {
        String m = motCle.toLowerCase();
        return titre.toLowerCase().contains(m) || auteur.toLowerCase().contains(m);
    }

    @Override
    public String toString() {
        return String.format("%-6s %-28s %-18s %d  %s", isbn, titre, auteur, annee,
                disponible ? "disponible" : "emprunté");
    }
}

record Emprunt(String isbn, String membre, LocalDate date) { }

class Bibliotheque {
    private final Map<String, Livre> catalogue = new HashMap<>();
    private final List<Emprunt> emprunts = new ArrayList<>();

    void ajouter(Livre livre) {
        catalogue.put(livre.getIsbn(), livre);
    }

    Livre trouver(String isbn) throws BibliothequeException {
        Livre livre = catalogue.get(isbn);
        if (livre == null) {
            throw new BibliothequeException("Aucun livre avec l'ISBN " + isbn);
        }
        return livre;
    }

    List<Livre> livresTries() {
        List<Livre> liste = new ArrayList<>(catalogue.values());
        liste.sort(Comparator.comparing(Livre::getTitre));
        return liste;
    }

    List<Livre> rechercher(String motCle) {
        List<Livre> resultats = new ArrayList<>();
        for (Livre l : livresTries()) {
            if (l.correspond(motCle)) {
                resultats.add(l);
            }
        }
        return resultats;
    }

    void emprunter(String isbn, String membre, LocalDate date) throws BibliothequeException {
        Livre livre = trouver(isbn);
        livre.emprunter();
        emprunts.add(new Emprunt(isbn, membre, date));
    }

    void rendre(String isbn) throws BibliothequeException {
        Livre livre = trouver(isbn);
        livre.rendre();
        emprunts.removeIf(e -> e.isbn().equals(isbn));
    }

    Map<String, Integer> livresParAuteur() {
        Map<String, Integer> stats = new TreeMap<>();
        for (Livre l : catalogue.values()) {
            stats.merge(l.getAuteur(), 1, Integer::sum);
        }
        return stats;
    }

    List<Emprunt> getEmprunts() {
        return List.copyOf(emprunts);   // copie non modifiable : encapsulation
    }
}

public class GestionBibliotheque {
    private final Bibliotheque biblio = new Bibliotheque();
    private LocalDate aujourdhui = LocalDate.of(2025, 3, 10);

    void executer(String ligne) {
        System.out.println("> " + ligne);
        String[] mots = ligne.trim().split(" ");
        try {
            switch (mots[0]) {
                case "liste" -> biblio.livresTries().forEach(System.out::println);
                case "chercher" -> {
                    List<Livre> res = biblio.rechercher(mots[1]);
                    if (res.isEmpty()) {
                        System.out.println("Aucun résultat");
                    }
                    res.forEach(System.out::println);
                }
                case "emprunter" -> {
                    biblio.emprunter(mots[1], mots[2], aujourdhui);
                    System.out.println("Emprunt enregistré pour " + mots[2]);
                }
                case "rendre" -> {
                    biblio.rendre(mots[1]);
                    System.out.println("Retour enregistré");
                }
                case "stats" -> {
                    System.out.println("Livres par auteur : " + biblio.livresParAuteur());
                    for (Emprunt e : biblio.getEmprunts()) {
                        System.out.println("En cours : " + e.isbn() + " par " + e.membre() + " depuis le " + e.date());
                    }
                }
                default -> System.out.println("Commande inconnue : " + mots[0]);
            }
        } catch (BibliothequeException e) {
            System.out.println("Erreur : " + e.getMessage());
        } catch (ArrayIndexOutOfBoundsException e) {
            System.out.println("Erreur : paramètre manquant pour « " + mots[0] + " »");
        }
    }

    void chargerCatalogue() {
        biblio.ajouter(new Livre("B001", "Apprendre Java pas à pas", "C. Martin", 2021));
        biblio.ajouter(new Livre("B002", "Les algorithmes en douceur", "A. Benali", 2019));
        biblio.ajouter(new Livre("B003", "Java et les collections", "C. Martin", 2023));
        biblio.ajouter(new Livre("B004", "Bases de données", "L. Nguyen", 2020));
    }

    public static void main(String[] args) {
        GestionBibliotheque app = new GestionBibliotheque();
        app.chargerCatalogue();
        String[] commandes = {
            "liste",
            "chercher java",
            "emprunter B003 Amina",
            "emprunter B003 Lucas",
            "emprunter B999 Lucas",
            "emprunter B002",
            "rendre B004",
            "stats",
            "rendre B003",
            "aide"
        };
        for (String c : commandes) {
            app.executer(c);
        }
    }
}
```

```text
> liste
B001   Apprendre Java pas à pas     C. Martin          2021  disponible
B004   Bases de données             L. Nguyen          2020  disponible
B003   Java et les collections      C. Martin          2023  disponible
B002   Les algorithmes en douceur   A. Benali          2019  disponible
> chercher java
B001   Apprendre Java pas à pas     C. Martin          2021  disponible
B003   Java et les collections      C. Martin          2023  disponible
> emprunter B003 Amina
Emprunt enregistré pour Amina
> emprunter B003 Lucas
Erreur : « Java et les collections » est déjà emprunté
> emprunter B999 Lucas
Erreur : Aucun livre avec l'ISBN B999
> emprunter B002
Erreur : paramètre manquant pour « emprunter »
> rendre B004
Erreur : « Bases de données » n'était pas emprunté
> stats
Livres par auteur : {A. Benali=1, C. Martin=2, L. Nguyen=1}
En cours : B003 par Amina depuis le 2025-03-10
> rendre B003
Retour enregistré
> aide
Commande inconnue : aide
```

## Comprendre le code

- **Encapsulation** : `Livre` garde `disponible` privé ; seules `emprunter()` et `rendre()` le modifient, et elles refusent les transitions impossibles. `getEmprunts()` renvoie une **copie non modifiable** (`List.copyOf`) : l'extérieur ne peut pas altérer la liste interne.
- **Exception métier vérifiée** : `BibliothequeException` est déclarée avec `throws` jusqu'à `executer`, qui la traite en un seul endroit et affiche un message clair. Le programme ne s'arrête jamais sur une erreur d'utilisateur.
- **Exception non vérifiée** : une commande incomplète (`emprunter B002`) provoque un `ArrayIndexOutOfBoundsException` sur `mots[2]`, intercepté pour afficher un message utile. Une validation explicite du nombre de mots serait encore plus propre (voir les améliorations).
- **Collections** : `HashMap` pour retrouver un livre par ISBN, `ArrayList` triée avec `Comparator.comparing(Livre::getTitre)` pour l'affichage, `TreeMap` + `merge` pour les statistiques, `removeIf` pour clore un emprunt.
- **Record** : `Emprunt` est une valeur immuable ; `LocalDate` (package `java.time`) représente une date sans heure et s'affiche au format `AAAA-MM-JJ`. Une date fixe est utilisée ici pour que la sortie soit reproductible ; dans une vraie application, on écrirait `LocalDate.now()`.
- **switch moderne** et **références de méthodes** : `System.out::println` équivaut à la lambda `l -> System.out.println(l)`.
- **Tri des titres** : « Bases de données » apparaît avant « Java… » car le tri compare les caractères un à un, et `B` vient avant `J`.

## Brancher le clavier

Pour une utilisation interactive, remplacez le tableau de commandes de `main` par une lecture au clavier (ajoutez `import java.util.Scanner;` en haut du fichier) :

```java
public static void main(String[] args) {
    GestionBibliotheque app = new GestionBibliotheque();
    app.chargerCatalogue();
    try (Scanner clavier = new Scanner(System.in)) {
        System.out.println("Commandes : liste, chercher <mot>, emprunter <isbn> <membre>, rendre <isbn>, stats, quitter");
        while (clavier.hasNextLine()) {
            String ligne = clavier.nextLine();
            if (ligne.equals("quitter")) {
                break;
            }
            if (!ligne.isBlank()) {
                app.executer(ligne);
            }
        }
    }
}
```

Grâce à la méthode `executer`, la logique ne change pas : seule la **source** des commandes est différente. Séparer ainsi la lecture des entrées et le traitement rend le programme facile à tester.

## Pistes d'amélioration

Une fois le programme compris et exécuté, enrichissez-le :

1. **Validation des commandes** : vérifiez le nombre de mots avant d'accéder à `mots[1]` ou `mots[2]`, et affichez la syntaxe attendue.
2. **Limite d'emprunts** : refusez un emprunt si le membre a déjà 3 livres en cours (comptez dans `emprunts` ceux dont `membre()` correspond).
3. **Retards** : ajoutez une commande `retards` qui liste les emprunts de plus de 21 jours, avec `e.date().plusDays(21).isBefore(aujourdhui)`.
4. **Types de documents** : créez une classe abstraite `Document` dont héritent `Livre` et `Magazine`, chacun avec sa propre durée d'emprunt (polymorphisme).
5. **Commande ajouter** : `ajouter <isbn> <année> <titre…>`, en utilisant `split(" ", 4)` pour garder le titre en un seul morceau, et en interceptant la `NumberFormatException` sur l'année.

## À retenir

- Choisir le bon outil : une **classe** pour un état qui évolue, un **record** pour une valeur, une **exception vérifiée** pour une erreur métier, une **Map** pour un accès par identifiant.
- Encapsuler l'état et faire respecter les règles **dans** les méthodes de l'objet concerné.
- Centraliser la gestion des erreurs à un seul endroit (`executer`) et afficher des messages compréhensibles.
- Séparer la **source des entrées** (tableau de test, clavier) du **traitement** : le code devient testable.
- Félicitations : vous savez écrire, compiler et structurer un programme Java orienté objet complet !
"""

QUIZ_M3 = [
    ("single", "Quelle est la différence entre une classe et un objet ?", None,
     ["La classe est un plan, l'objet est une instance créée à partir de ce plan.", "Il n'y en a aucune.", "L'objet est un plan, la classe en est une copie.", "Une classe ne contient que des méthodes."], [0],
     "La classe décrit attributs et méthodes ; chaque appel à new crée un objet (une instance) qui possède ses propres valeurs."),
    ("single", "Quelle affirmation sur un constructeur est exacte ?", None,
     ["Il a pour type de retour void.", "Il doit s'appeler init.", "Une classe ne peut en avoir qu'un seul.", "Il porte le nom de la classe et n'a pas de type de retour."], [3],
     "Un constructeur porte exactement le nom de la classe, sans type de retour ; il peut être surchargé (plusieurs constructeurs)."),
    ("single", "Dans un constructeur, que signifie this.nom = nom; ?", None,
     ["Le paramètre nom reçoit la valeur de l'attribut.", "L'attribut nom de l'objet en cours reçoit la valeur du paramètre nom.", "On crée une nouvelle variable locale nom.", "On appelle la classe mère."], [1],
     "this désigne l'objet en cours : this.nom est l'attribut, nom seul est le paramètre qui le masquerait sans this."),
    ("single", "Qu'affiche ce code ?", "Compteur a = new Compteur();\nCompteur b = a;\nb.valeur = 7;\nSystem.out.println(a.valeur);",
     ["0", "null", "7", "Erreur de compilation"], [2],
     "b = a copie la référence : a et b désignent le même objet. Modifier b.valeur modifie donc ce que l'on lit avec a.valeur."),
    ("multiple", "Quelles pratiques relèvent d'une bonne encapsulation ?", None,
     ["Déclarer les attributs private.", "Fournir systématiquement un setter public pour chaque attribut.", "Vérifier les règles métier dans les méthodes qui modifient l'état.", "Déclarer final un attribut qui ne doit plus changer après la construction."], [0, 2, 3],
     "Encapsuler, c'est cacher les données et contrôler leur modification. Des setters publics systématiques rouvriraient l'accès sans contrôle."),
    ("single", "Que signifie static devant un attribut ?", None,
     ["L'attribut ne peut pas changer de valeur.", "L'attribut est privé.", "L'attribut est recalculé à chaque appel.", "L'attribut est partagé par toutes les instances de la classe."], [3],
     "Un attribut static appartient à la classe et non à chaque objet : toutes les instances partagent la même valeur. C'est final qui empêche la modification."),
    ("single", "Comment déclarer que Chat hérite d'Animal ?", None,
     ["class Chat extends Animal", "class Chat implements Animal", "class Chat inherits Animal", "class Chat : Animal"], [0],
     "extends exprime l'héritage d'une classe ; implements sert pour les interfaces."),
    ("single", "Que fait super(nom) dans le constructeur d'une sous-classe ?", None,
     ["Il appelle une méthode nommée super.", "Il appelle le constructeur de la classe mère avec l'argument nom.", "Il crée un nouvel objet de la classe mère.", "Il rend l'attribut nom public."], [1],
     "super(…) appelle le constructeur parent, obligatoirement en première instruction, pour initialiser la partie héritée de l'objet."),
    ("single", "À quoi sert l'annotation @Override ?", None,
     ["À rendre une méthode privée.", "À surcharger une méthode avec d'autres paramètres.", "À demander au compilateur de vérifier qu'on redéfinit bien une méthode héritée.", "À empêcher toute redéfinition."], [2],
     "@Override signale une redéfinition : si aucune méthode de même signature n'existe dans la classe mère (faute de frappe, par exemple), la compilation échoue."),
    ("true_false", "En Java, une classe peut hériter directement de deux classes.", None,
     ["Vrai", "Faux"], [1],
     "Java n'autorise qu'une seule classe mère (héritage simple). En revanche, une classe peut implémenter plusieurs interfaces."),
]

QUIZ_M4 = [
    ("single", "Que se passe-t-il si l'on écrit new Forme() alors que Forme est déclarée abstract ?", None,
     ["Erreur de compilation : une classe abstraite ne s'instancie pas.", "Un objet Forme vide est créé.", "Une exception est levée à l'exécution.", "Java crée automatiquement une sous-classe."], [0],
     "Une classe abstraite sert de modèle : on ne peut créer que des objets de ses sous-classes concrètes."),
    ("multiple", "Quelles affirmations sur les interfaces sont exactes ?", None,
     ["Une classe peut implémenter plusieurs interfaces.", "Une méthode default possède un corps.", "Une interface possède un constructeur.", "Les méthodes implémentées d'une interface doivent être public."], [0, 1, 3],
     "Une interface n'a pas de constructeur ni d'attributs d'instance. Les trois autres affirmations sont exactes."),
    ("single", "Qu'est-ce que le polymorphisme ?", None,
     ["Le fait d'avoir plusieurs constructeurs.", "Copier une classe sous un autre nom.", "Convertir un int en double.", "Traiter des objets de classes différentes via un type commun, chacun exécutant sa propre version des méthodes."], [3],
     "Avec une variable de type commun (classe mère ou interface), l'appel exécute la méthode de l'objet réel : un même code traite des objets différents."),
    ("single", "Comment déclarer une liste de chaînes de taille variable ?", None,
     ["String[] liste = new String[];", "List<String> liste = new ArrayList<>();", "ArrayList liste = String[];", "List<string> liste = new List();"], [1],
     "On déclare avec l'interface List, paramétrée par le type des éléments, et on crée l'objet avec ArrayList (les <> vides laissent Java déduire le type)."),
    ("single", "Quelle méthode donne le nombre d'éléments d'une ArrayList ?", None,
     ["length", "length()", "size()", "count()"], [2],
     "Les collections utilisent size(). length (sans parenthèses) est réservé aux tableaux, length() aux chaînes."),
    ("single", "Pourquoi écrit-on List<Integer> et non List<int> ?", None,
     ["Integer est plus rapide.", "Les collections ne contiennent que des objets : on utilise la classe enveloppe Integer.", "int n'existe pas en Java.", "C'est une simple convention de style."], [1],
     "Les génériques n'acceptent pas les types primitifs ; Java convertit automatiquement entre int et Integer (autoboxing)."),
    ("single", "Que renvoie map.get(cle) si la clé est absente d'une HashMap ?", None,
     ["0", "Une chaîne vide", "null", "Une exception"], [2],
     "get renvoie null pour une clé absente. getOrDefault(cle, valeur) permet de fournir une valeur de repli."),
    ("single", "Que fait compteur.merge(mot, 1, Integer::sum) ?", None,
     ["Remplace toujours la valeur par 1.", "Associe 1 si le mot est absent, sinon ajoute 1 à la valeur existante.", "Supprime le mot s'il existe.", "Fusionne deux maps."], [1],
     "merge insère la valeur donnée si la clé manque, sinon combine l'ancienne et la nouvelle avec la fonction fournie (ici l'addition)."),
    ("single", "Quelle Map garde les clés triées ?", None,
     ["HashMap", "LinkedHashMap", "TreeMap", "ArrayList"], [2],
     "TreeMap maintient ses clés dans l'ordre naturel ; LinkedHashMap conserve l'ordre d'insertion ; HashMap ne garantit aucun ordre."),
    ("true_false", "Dans une HashMap, deux associations peuvent avoir la même clé.", None,
     ["Vrai", "Faux"], [1],
     "Les clés sont uniques : un put avec une clé existante remplace l'ancienne valeur."),
]

QUIZ_M5 = [
    ("single", "Que se passe-t-il quand une exception est levée et que personne ne l'intercepte ?", None,
     ["Elle est ignorée.", "Le compilateur la corrige.", "La ligne est exécutée une seconde fois.", "Le programme s'arrête et affiche la pile d'appels."], [3],
     "Une exception non traitée remonte jusqu'à main puis arrête le programme, en affichant son type, son message et la pile d'appels."),
    ("single", "Quand le bloc finally s'exécute-t-il ?", None,
     ["Uniquement si aucune exception ne survient.", "Uniquement si une exception survient.", "Dans tous les cas, après le try et l'éventuel catch.", "Jamais si un catch a été exécuté."], [2],
     "finally s'exécute toujours, erreur ou non : on y place le nettoyage."),
    ("single", "Quel mot clé permet de lever une exception ?", None,
     ["throws", "throw", "catch", "raise"], [1],
     "throw lève une exception (throw new …). throws, dans une signature, annonce qu'une méthode peut en lever."),
    ("multiple", "Lesquelles sont des exceptions non vérifiées (héritant de RuntimeException) ?", None,
     ["NullPointerException", "IllegalArgumentException", "IOException", "ArithmeticException"], [0, 1, 3],
     "IOException est vérifiée : le compilateur oblige à la traiter ou à la déclarer. Les trois autres héritent de RuntimeException."),
    ("single", "Votre classe StockException extends Exception est levée dans une méthode. Que faut-il faire ?", None,
     ["Rien de particulier.", "La traiter avec try/catch ou la déclarer avec throws dans la signature.", "La transformer en int.", "Remplacer extends par implements."], [1],
     "Une classe qui hérite d'Exception (hors RuntimeException) est vérifiée : le compilateur exige qu'elle soit traitée ou déclarée."),
    ("single", "Qu'affiche ce code ?", "record Point(int x, int y) { }\n\nPoint a = new Point(1, 2);\nPoint b = new Point(1, 2);\nSystem.out.println(a.equals(b) + \" \" + (a == b));",
     ["true true", "false false", "true false", "false true"], [2],
     "Un record définit equals d'après ses valeurs : a.equals(b) est vrai. Mais ce sont deux objets distincts : a == b est faux."),
    ("single", "Comment lit-on la composante nom d'un record Personne(String nom, int age) p ?", None,
     ["p.nom()", "p.getNom()", "p.nom", "Personne.nom(p)"], [0],
     "Les accesseurs générés par un record portent le nom de la composante, sans préfixe get : p.nom()."),
    ("single", "Pourquoi la classe Livre du mini-projet n'est-elle pas un record ?", None,
     ["Les records ne peuvent pas contenir de String.", "Son état (disponible ou non) doit évoluer, alors qu'un record est immuable.", "Un record ne peut pas avoir de méthode.", "Un record ne peut pas être stocké dans une Map."], [1],
     "Un record est immuable ; un livre passe de disponible à emprunté, donc une classe avec un attribut modifiable et encapsulé convient mieux."),
    ("single", "Dans le mini-projet, pourquoi getEmprunts() renvoie-t-il List.copyOf(emprunts) ?", None,
     ["Pour trier la liste.", "Parce que ArrayList ne peut pas être renvoyée.", "Pour accélérer le programme.", "Pour que l'extérieur ne puisse pas modifier la liste interne de la bibliothèque."], [3],
     "List.copyOf renvoie une copie non modifiable : c'est de l'encapsulation, la bibliothèque reste seule maîtresse de ses emprunts."),
    ("true_false", "Écrire catch (Exception e) { } pour faire disparaître toutes les erreurs est une bonne pratique.", None,
     ["Vrai", "Faux"], [1],
     "Ignorer silencieusement une exception masque le problème sans le résoudre et rend les bugs très difficiles à trouver."),
]
