"""Contenu de la formation « Java pour débutants » (SMK Academy).

Blocs ```java pour le code, ```text pour la sortie de la console, ```solution-java pour les corrections.
Chaque bloc ```java ou ```solution-java suivi d'un bloc ```text est compilé (javac) et exécuté (java) par
scripts/check_code_blocks.py, qui compare la sortie réelle au bloc ```text.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("java_debutant_m3_m5", _Path(__file__).with_name("java_debutant_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "java-debutant",
    "title": "Java pour débutants",
    "subtitle": "Les bases de la programmation orientée objet.",
    "description": (
        "Java est un langage très répandu en entreprise, dans les applications serveur et dans l'enseignement. "
        "Cette formation part de zéro : installation du JDK, compilation, variables, conditions, boucles et méthodes, "
        "puis programmation orientée objet (classes, encapsulation, héritage, interfaces, polymorphisme). "
        "Vous manipulerez ensuite les collections, les exceptions et les records, avant de réaliser un mini-projet : "
        "la gestion d'une bibliothèque en console. Chaque leçon propose des exemples exécutés et des exercices corrigés ; "
        "chaque module se termine par un quiz noté sur 20."
    ),
    "category": "Programmation",
    "category_slug": "programmation",
    "topic": "Java",
    "cover_label": "Jv",
    "level": "debutant",
    "duration_minutes": 900,
    "objectives": [
        "Écrire et compiler un programme Java",
        "Utiliser classes, objets et héritage",
        "Manipuler les collections",
    ],
    "prerequisites": ["Aucun prérequis"],
    "status": "published",
    "is_premium": False,
    "position": 11,
}

# ---------------------------------------------------------------------------
# Module 1 — Premiers pas en Java
# ---------------------------------------------------------------------------
M1_L1 = r"""
## Qu'est-ce que Java ?

**Java** est un langage de programmation généraliste, apparu au milieu des années 1990. On le retrouve dans les applications d'entreprise, les serveurs web, les outils de traitement de données, et il est historiquement lié au développement Android. Il est aussi très utilisé pour enseigner la programmation orientée objet.

Trois idées résument Java :

- **Typage statique** : chaque variable a un type connu dès l'écriture du programme (nombre entier, texte…). Beaucoup d'erreurs sont détectées **avant** l'exécution.
- **Orienté objet** : un programme Java est organisé en **classes**, qui décrivent des objets (un client, un livre, un compte bancaire).
- **Portable** : le code est compilé en un format intermédiaire, le **bytecode**, exécuté par une **machine virtuelle** (la JVM). Le même fichier compilé fonctionne sur Windows, macOS ou Linux.

> Malgré la ressemblance des noms, Java et JavaScript sont deux langages différents.

## JDK, JVM : de quoi a-t-on besoin ?

| Sigle | Signification | Rôle |
|---|---|---|
| **JVM** | *Java Virtual Machine* | Exécute le bytecode (fichiers `.class`). |
| **JDK** | *Java Development Kit* | Kit du développeur : contient le compilateur `javac`, la commande `java` et la bibliothèque standard. |

Pour programmer, installez un **JDK** récent. Plusieurs distributions gratuites existent (par exemple OpenJDK, Eclipse Temurin). Choisissez de préférence une version dite **LTS** (*Long-Term Support*, support à long terme) : cette formation utilise du Java moderne, compatible avec Java 17 et les versions suivantes.

Vérifiez l'installation dans un terminal :

```bash
javac -version
java -version
```

Chaque commande affiche un numéro de version. Si le terminal répond « commande introuvable », le JDK n'est pas installé ou n'est pas dans le `PATH` (la liste des dossiers où le système cherche les programmes).

## Votre premier programme

Créez un fichier nommé **exactement** `Bonjour.java` :

```java
public class Bonjour {
    public static void main(String[] args) {
        System.out.println("Bonjour, SMK Academy !");
    }
}
```

```text
Bonjour, SMK Academy !
```

Décortiquons-le :

- `public class Bonjour { … }` déclare une **classe** nommée `Bonjour`. Tout code Java vit dans une classe. Une classe `public` doit se trouver dans un fichier qui porte **son nom** : `Bonjour.java`.
- `public static void main(String[] args)` est la **méthode principale** : le point d'entrée du programme. La JVM commence toujours par elle. Vous comprendrez chaque mot clé au fil de la formation ; pour l'instant, recopiez cette ligne telle quelle.
- `System.out.println(…)` affiche une ligne dans la console (*print line*).
- Chaque **instruction** se termine par un point-virgule `;`. Les accolades `{ }` délimitent des **blocs**.

## Compiler puis exécuter

Le travail se fait en deux étapes :

```bash
javac Bonjour.java   # compile : produit Bonjour.class (le bytecode)
java Bonjour         # exécute la classe Bonjour (sans extension)
```

1. `javac` (le **compilateur**) vérifie le code et le traduit en bytecode dans `Bonjour.class`. S'il trouve une erreur, il l'affiche et ne produit rien.
2. `java` démarre la JVM, qui charge la classe et appelle sa méthode `main`.

Depuis Java 11, on peut aussi lancer directement un programme tenant en un seul fichier : `java Bonjour.java` compile en mémoire puis exécute. C'est pratique pour s'entraîner ; pour un vrai projet, on utilise `javac` ou un outil de construction (Maven, Gradle) via un environnement de développement comme IntelliJ IDEA, Eclipse ou VS Code.

## print, println et commentaires

```java
public class Affichage {
    public static void main(String[] args) {
        // Commentaire sur une ligne : ignoré par le compilateur
        System.out.print("Java ");      // print ne passe pas à la ligne
        System.out.print("est ");
        System.out.println("compilé.");  // println passe à la ligne
        /* Commentaire
           sur plusieurs lignes */
        System.out.println(2 + 3);
        System.out.println("2 + 3 = " + (2 + 3));
    }
}
```

```text
Java est compilé.
5
2 + 3 = 5
```

L'opérateur `+` appliqué à un texte **concatène** (met bout à bout). Les parenthèses autour de `2 + 3` forcent le calcul avant la concaténation.

## Lire une erreur de compilation

Java distingue les majuscules et les minuscules, et le compilateur est exigeant. Voici un programme avec une faute de frappe (`system` au lieu de `System`) :

```java
public class Erreur {
    public static void main(String[] args) {
        system.out.println("Oups");
    }
}
```

```text
Erreur.java:3: error: package system does not exist
        system.out.println("Oups");
              ^
1 error
```

Le message indique **le fichier et la ligne** (`Erreur.java:3`), **la nature du problème**, et un accent circonflexe `^` montre l'endroit repéré. Le message ne désigne pas toujours la cause exacte (ici, il croit à un *package* inconnu), mais la ligne indiquée est le bon point de départ. Corrigez **la première erreur** d'abord : les suivantes en découlent souvent.

> Les messages du compilateur sont généralement en anglais. Lisez-les en entier : *cannot find symbol* (nom inconnu, souvent une faute de frappe), *';' expected* (point-virgule manquant), *incompatible types* (mauvais type de valeur).

## À retenir

- Le **JDK** fournit `javac` (compilateur) et `java` (lanceur de la JVM).
- `javac Fichier.java` produit un `.class` ; `java Fichier` l'exécute ; `java Fichier.java` fait les deux pour un fichier unique.
- Une classe `public` se place dans un fichier du même nom ; le programme démarre dans `public static void main(String[] args)`.
- `System.out.println` affiche une ligne, `System.out.print` n'ajoute pas de retour à la ligne.
- Java distingue les majuscules ; chaque instruction se termine par `;` ; commentaires `//` et `/* */`.

## Exercices

### Exercice 1 — Carte de visite

Écrivez une classe `Carte` qui affiche, sur trois lignes, un prénom, une ville et le résultat de `12 * 4`.

```solution-java
public class Carte {
    public static void main(String[] args) {
        System.out.println("Amina");
        System.out.println("Lyon");
        System.out.println(12 * 4);
    }
}
```

```text
Amina
Lyon
48
```

### Exercice 2 — Trouvez les erreurs

Ce programme, enregistré dans `Salut.java`, ne compile pas. Trouvez les trois erreurs.

```text
public class salut {
    public static void main(String[] args) {
        System.out.println("Salut")
        System.out.Println("à tous");
    }
}
```

```solution-text
1. La classe publique doit porter le nom du fichier : public class Salut (S majuscule).
2. Il manque le point-virgule après System.out.println("Salut").
3. Println n'existe pas : Java distingue les majuscules, la méthode s'écrit println.
```

### Exercice 3 — Les deux commandes

Vous avez écrit `Calcul.java`. Quelles commandes tapez-vous pour le compiler puis l'exécuter, et quel fichier apparaît après la première ?

```solution-text
javac Calcul.java   → crée Calcul.class (le bytecode)
java Calcul         → exécute la classe (sans l'extension .class)
Variante pour un programme en un seul fichier : java Calcul.java
```
"""

M1_L2 = r"""
## Déclarer une variable

Une **variable** est un emplacement nommé qui contient une valeur. En Java, on indique son **type** lors de la déclaration :

```java
public class Variables {
    public static void main(String[] args) {
        int age = 25;
        double taille = 1.68;
        String prenom = "Sofia";
        boolean inscrit = true;

        System.out.println(prenom + " a " + age + " ans.");
        age = age + 1;  // réaffectation : même type obligatoire
        System.out.println("Un an plus tard : " + age + " ans.");
        System.out.println("Taille : " + taille + " m, inscrite : " + inscrit);
    }
}
```

```text
Sofia a 25 ans.
Un an plus tard : 26 ans.
Taille : 1.68 m, inscrite : true
```

Règles de nommage : une lettre au début, puis lettres, chiffres ou `_` ; pas d'espace ni de mot réservé (`class`, `int`…). Par convention, on écrit les variables en **camelCase** : `prixTotal`, `nombreDeLivres`.

## Les types primitifs

Java propose huit **types primitifs** (des valeurs simples, stockées directement). Les plus utilisés :

| Type | Contenu | Exemple |
|---|---|---|
| `int` | entier (environ ± 2,1 milliards) | `int stock = 42;` |
| `long` | grand entier (suffixe `L`) | `long population = 8_000_000_000L;` |
| `double` | nombre à virgule (point décimal) | `double prix = 19.99;` |
| `boolean` | `true` ou `false` | `boolean actif = false;` |
| `char` | un caractère, entre apostrophes | `char note = 'A';` |

Les autres (`byte`, `short`, `float`) servent dans des cas particuliers. Le tiret bas `_` dans `8_000_000_000L` améliore seulement la lisibilité.

`String` (le texte) n'est **pas** un type primitif mais une **classe** : d'où sa majuscule. Une chaîne s'écrit entre guillemets doubles `"…"`, un `char` entre apostrophes `'…'`.

## Le typage statique en action

Une variable ne peut pas changer de type. Le compilateur refuse ce programme :

```java
public class TypeIncorrect {
    public static void main(String[] args) {
        int age = "vingt";
    }
}
```

```text
TypeIncorrect.java:3: error: incompatible types: String cannot be converted to int
        int age = "vingt";
                  ^
1 error
```

L'erreur est détectée **avant** toute exécution : c'est l'un des grands atouts de Java.

## var et final

- `var` laisse le compilateur **déduire** le type à partir de la valeur (pour les variables locales). Le type reste fixe : `var n = 10;` fait de `n` un `int` pour toujours.
- `final` interdit la réaffectation : on l'utilise pour les **constantes**, écrites par convention en MAJUSCULES.

```java
public class VarFinal {
    public static void main(String[] args) {
        var quantite = 3;          // int déduit
        var libelle = "Cahier";    // String déduit
        final double TVA = 0.20;
        double prixHT = 5.0;
        System.out.println(quantite + " x " + libelle);
        System.out.println("Prix TTC unitaire : " + prixHT * (1 + TVA));
    }
}
```

```text
3 x Cahier
Prix TTC unitaire : 6.0
```

Écrire `TVA = 0.10;` plus loin provoquerait une erreur de compilation : *cannot assign a value to final variable TVA*.

## Les opérateurs arithmétiques

| Opérateur | Sens | Exemple | Résultat |
|---|---|---|---|
| `+` `-` `*` | addition, soustraction, multiplication | `7 * 3` | `21` |
| `/` | division | `7 / 2` | `3` (entre entiers !) |
| `%` | reste de la division (modulo) | `7 % 2` | `1` |

**Piège classique** : la division de deux `int` donne un `int`, la partie décimale est **tronquée**. Pour obtenir un résultat décimal, au moins un des opérandes doit être un `double` :

```java
public class Division {
    public static void main(String[] args) {
        int a = 7;
        int b = 2;
        System.out.println(a / b);
        System.out.println(a % b);
        System.out.println(a / 2.0);
        System.out.println((double) a / b);
        System.out.println(0.1 + 0.2);
    }
}
```

```text
3
1
3.5
3.5
0.30000000000000004
```

- `(double) a` est une **conversion explicite** (*cast*) : on demande de traiter `a` comme un `double`.
- La dernière ligne montre que les `double` sont des **approximations** binaires. Pour de l'argent, les professionnels utilisent la classe `BigDecimal` ou comptent en centimes avec des entiers.

## Conversions et raccourcis

Java convertit automatiquement vers un type « plus large » (`int` → `double`), mais exige un *cast* dans l'autre sens, car on peut perdre de l'information :

```java
public class Conversions {
    public static void main(String[] args) {
        double moyenne = 14.8;
        int arrondiInf = (int) moyenne;           // tronque : 14
        long arrondi = Math.round(moyenne);       // arrondit : 15
        int compteur = 10;
        compteur += 5;   // compteur = compteur + 5
        compteur++;      // compteur = compteur + 1
        compteur *= 2;   // compteur = compteur * 2
        System.out.println(arrondiInf + " " + arrondi + " " + compteur);
        System.out.println(Math.max(3, 9) + " " + Math.sqrt(16) + " " + Math.pow(2, 10));
        System.out.println(Integer.MAX_VALUE + 1);
    }
}
```

```text
14 15 32
9 4.0 1024.0
-2147483648
```

La dernière ligne illustre le **dépassement de capacité** : au-delà de sa valeur maximale, un `int` « repart » du côté négatif, sans erreur. Si vos nombres peuvent devenir très grands, utilisez `long`.

## À retenir

- Une variable se déclare avec un type : `int`, `double`, `boolean`, `char`, `String`… et ne change jamais de type.
- `var` déduit le type ; `final` crée une constante (en MAJUSCULES par convention).
- La division de deux entiers est entière : `7 / 2` vaut `3` ; `%` donne le reste.
- `(double)` ou `(int)` convertissent explicitement ; `Math.round`, `Math.max`, `Math.sqrt`, `Math.pow` sont prêts à l'emploi.
- Les `double` sont des approximations ; un `int` peut dépasser sa capacité.

## Exercices

### Exercice 1 — Moyenne de trois notes

Déclarez trois notes entières `12`, `15` et `16`, puis affichez leur moyenne **avec** sa partie décimale.

```solution-java
public class Moyenne {
    public static void main(String[] args) {
        int n1 = 12;
        int n2 = 15;
        int n3 = 16;
        double moyenne = (n1 + n2 + n3) / 3.0;
        System.out.println("Moyenne : " + moyenne);
    }
}
```

```text
Moyenne : 14.333333333333334
```

Avec `/ 3` au lieu de `/ 3.0`, vous obtiendriez `14` : division entière.

### Exercice 2 — Heures et minutes

Convertissez `135` minutes en heures et minutes avec `/` et `%`.

```solution-java
public class Duree {
    public static void main(String[] args) {
        int total = 135;
        int heures = total / 60;
        int minutes = total % 60;
        System.out.println(total + " min = " + heures + " h " + minutes + " min");
    }
}
```

```text
135 min = 2 h 15 min
```

### Exercice 3 — Quel type ?

Quel type choisiriez-vous pour : un nombre d'élèves, un prix, une réponse oui/non, une initiale, le nombre d'habitants de la Terre ?

```solution-text
Nombre d'élèves : int
Prix : double (ou BigDecimal en contexte bancaire)
Réponse oui/non : boolean
Initiale : char
Habitants de la Terre : long (dépasse la capacité d'un int)
```
"""

M1_L3 = r"""
## Les chaînes de caractères

Une `String` est une suite de caractères. C'est un **objet** : on lui applique des **méthodes** avec un point.

```java
public class Chaines {
    public static void main(String[] args) {
        String ville = "Marseille";
        System.out.println(ville.length());          // nombre de caractères
        System.out.println(ville.toUpperCase());
        System.out.println(ville.charAt(0));          // premier caractère
        System.out.println(ville.substring(0, 4));    // de 0 inclus à 4 exclu
        System.out.println(ville.indexOf("se"));      // position de "se"
        System.out.println(ville.contains("eill"));
        System.out.println("  espaces  ".trim() + "|");
        System.out.println(ville.replace("e", "E"));
    }
}
```

```text
9
MARSEILLE
M
Mars
3
true
espaces|
MarsEillE
```

Les positions commencent à **0** : le premier caractère est à l'indice 0, le dernier à l'indice `length() - 1`.

> Les chaînes sont **immuables** : `toUpperCase()` ne modifie pas `ville`, elle renvoie une **nouvelle** chaîne. Pour garder le résultat : `ville = ville.toUpperCase();`.

## Comparer deux chaînes : equals, pas ==

Pour comparer le **contenu** de deux chaînes, utilisez toujours `equals` (ou `equalsIgnoreCase` pour ignorer les majuscules). L'opérateur `==` compare si ce sont **le même objet** en mémoire, ce qui peut être faux même pour un texte identique :

```java
public class Comparer {
    public static void main(String[] args) {
        String a = "java";
        String b = new String("java");
        System.out.println(a.equals(b));
        System.out.println(a == b);
        System.out.println("JAVA".equalsIgnoreCase(a));
        System.out.println("abc".compareTo("abd") < 0);  // ordre alphabétique
    }
}
```

```text
true
false
true
true
```

`compareTo` renvoie un nombre négatif si la première chaîne vient avant dans l'ordre, zéro si elles sont égales, un nombre positif sinon.

## Mettre en forme : String.format et printf

Concaténer avec `+` devient vite illisible. `String.format` (et son équivalent `System.out.printf`) insère des valeurs dans un **gabarit** :

| Code | Insère | Exemple |
|---|---|---|
| `%s` | du texte (ou n'importe quelle valeur) | `"Bonjour %s"` |
| `%d` | un entier | `"%d articles"` |
| `%.2f` | un décimal avec 2 chiffres après la virgule | `"%.2f €"` |
| `%n` | un retour à la ligne | — |

```java
public class Format {
    public static void main(String[] args) {
        String produit = "Clavier";
        int quantite = 3;
        double prix = 24.9;
        String ligne = String.format("%s x%d : %.2f EUR", produit, quantite, quantite * prix);
        System.out.println(ligne);
        System.out.printf("Total arrondi : %.1f%n", 74.75);
        System.out.printf("|%-8s|%5d|%n", "Stylo", 12);  // largeurs fixes
    }
}
```

```text
Clavier x3 : 74.70 EUR
Total arrondi : 74.8
|Stylo   |   12|
```

`%-8s` réserve 8 caractères alignés à gauche ; `%5d` réserve 5 caractères alignés à droite : pratique pour des tableaux en console.

> Le séparateur décimal de `%f` dépend de la **langue du système** : sur un ordinateur configuré en français, vous pourriez voir `74,70` au lieu de `74.70`.

## Convertir du texte en nombre

Une saisie au clavier ou une ligne de fichier arrive sous forme de texte. Pour calculer, il faut la convertir :

```java
public class Conversion {
    public static void main(String[] args) {
        int annee = Integer.parseInt("2024");
        double note = Double.parseDouble("15.5");
        String texte = String.valueOf(42);   // nombre → texte
        System.out.println(annee + 1);
        System.out.println(note * 2);
        System.out.println(texte + "1");
    }
}
```

```text
2025
31.0
421
```

Si le texte n'est pas un nombre valide, `Integer.parseInt("abc")` provoque une **exception** `NumberFormatException` (une erreur à l'exécution). Vous apprendrez à les intercepter au module 5.

## Lire le clavier avec Scanner

La classe `Scanner` lit ce que tape l'utilisateur. Elle se trouve dans le *package* (bibliothèque) `java.util`, qu'il faut **importer** en haut du fichier :

```java
import java.util.Scanner;

public class Saisie {
    public static void main(String[] args) {
        Scanner clavier = new Scanner(System.in);
        System.out.print("Votre prénom : ");
        String prenom = clavier.nextLine();
        System.out.print("Votre âge : ");
        int age = clavier.nextInt();
        System.out.println("Bonjour " + prenom + ", dans 10 ans vous aurez " + (age + 10) + " ans.");
        clavier.close();
    }
}
```

Exemple d'exécution, où l'utilisateur tape `Lina` puis `31` (chaque saisie est validée par la touche Entrée) :

```text
Votre prénom : Lina
Votre âge : 31
Bonjour Lina, dans 10 ans vous aurez 41 ans.
```

Les méthodes principales :

| Méthode | Lit |
|---|---|
| `nextLine()` | toute la ligne, jusqu'à Entrée |
| `next()` | un mot (jusqu'au prochain espace) |
| `nextInt()`, `nextDouble()` | un nombre |
| `hasNextInt()` | vérifie, sans lire, que la prochaine saisie est un entier |

> **Piège** : `nextInt()` lit le nombre mais laisse le retour à la ligne dans le tampon. Un `nextLine()` appelé juste après renvoie alors une chaîne vide. Solution simple : lire toutes les saisies avec `nextLine()` puis convertir avec `Integer.parseInt(…)`.

Un `Scanner` peut aussi lire une **chaîne** au lieu du clavier, ce qui est pratique pour tester un traitement sans rien taper :

```java
import java.util.Scanner;

public class ScannerTexte {
    public static void main(String[] args) {
        Scanner sc = new Scanner("Lina 31 1.62");
        String prenom = sc.next();
        int age = sc.nextInt();
        double taille = sc.nextDouble();
        System.out.println(prenom + " / " + age + " / " + taille);
    }
}
```

```text
Lina / 31 / 1.62
```

## À retenir

- Les méthodes de `String` : `length`, `charAt`, `substring`, `indexOf`, `contains`, `toUpperCase`, `trim`, `replace`… Les positions commencent à 0.
- Les chaînes sont immuables ; comparez-les avec `equals`, jamais avec `==`.
- `String.format` et `printf` construisent un texte à partir d'un gabarit (`%s`, `%d`, `%.2f`, `%n`).
- `Integer.parseInt` et `Double.parseDouble` convertissent du texte en nombre.
- `Scanner` (à importer depuis `java.util`) lit le clavier avec `nextLine`, `nextInt`…

## Exercices

### Exercice 1 — Initiales

À partir de `String prenom = "marie";` et `String nom = "curie";`, affichez `M.C.` puis `Marie CURIE`.

```solution-java
public class Initiales {
    public static void main(String[] args) {
        String prenom = "marie";
        String nom = "curie";
        String initiales = Character.toUpperCase(prenom.charAt(0)) + "." + Character.toUpperCase(nom.charAt(0)) + ".";
        String complet = prenom.substring(0, 1).toUpperCase() + prenom.substring(1) + " " + nom.toUpperCase();
        System.out.println(initiales);
        System.out.println(complet);
    }
}
```

```text
M.C.
Marie CURIE
```

`Character.toUpperCase` met un `char` en majuscule ; concaténé avec `"."`, le résultat devient une `String`.

### Exercice 2 — Ticket de caisse

Avec `printf`, affichez une ligne `Café        2 x  1.80 =  3.60` : nom sur 10 caractères aligné à gauche, quantité sur 2, prix unitaire et total sur 5 avec deux décimales.

```solution-java
public class Ticket {
    public static void main(String[] args) {
        String article = "Café";
        int quantite = 2;
        double prix = 1.8;
        System.out.printf("%-10s %2d x %5.2f = %5.2f%n", article, quantite, prix, quantite * prix);
    }
}
```

```text
Café        2 x  1.80 =  3.60
```

### Exercice 3 — Saisie robuste

Pourquoi ce programme affiche-t-il un nom vide si l'utilisateur tape `30`, Entrée, puis `Paul`, Entrée ? Comment le corriger ?

```text
int age = clavier.nextInt();
String nom = clavier.nextLine();
```

```solution-text
nextInt() lit « 30 » mais laisse le retour à la ligne dans le tampon ; nextLine() lit ce
reste de ligne vide et renvoie "". Correction : lire chaque saisie avec nextLine(), puis convertir :
int age = Integer.parseInt(clavier.nextLine());
String nom = clavier.nextLine();
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Contrôler l'exécution
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Comparer des valeurs

Une condition est une expression de type `boolean`, qui vaut `true` ou `false`. On la construit avec des **opérateurs de comparaison** :

| Opérateur | Sens | Exemple (avec `x = 7`) |
|---|---|---|
| `==` | égal à | `x == 7` → `true` |
| `!=` | différent de | `x != 7` → `false` |
| `<`, `<=` | inférieur (ou égal) | `x < 10` → `true` |
| `>`, `>=` | supérieur (ou égal) | `x >= 8` → `false` |

> `=` **affecte** une valeur, `==` **compare** deux valeurs primitives. Pour les chaînes, utilisez `equals`.

## if, else if, else

```java
public class Mention {
    public static void main(String[] args) {
        double moyenne = 13.5;
        if (moyenne >= 16) {
            System.out.println("Mention très bien");
        } else if (moyenne >= 14) {
            System.out.println("Mention bien");
        } else if (moyenne >= 12) {
            System.out.println("Mention assez bien");
        } else if (moyenne >= 10) {
            System.out.println("Admis");
        } else {
            System.out.println("Non admis");
        }
    }
}
```

```text
Mention assez bien
```

Les conditions sont testées **dans l'ordre** ; seul le premier bloc dont la condition est vraie s'exécute. La condition se place toujours entre **parenthèses**. Mettez toujours des accolades, même pour une seule instruction : c'est plus sûr quand on ajoute une ligne plus tard.

## Combiner des conditions

| Opérateur | Nom | Vrai si… |
|---|---|---|
| `&&` | ET | les deux conditions sont vraies |
| `\|\|` | OU | au moins une est vraie |
| `!` | NON | la condition est fausse |

```java
public class Acces {
    public static void main(String[] args) {
        int age = 17;
        boolean accompagne = true;
        boolean estMembre = false;

        if (age >= 18 || accompagne) {
            System.out.println("Entrée autorisée");
        }
        if (age >= 18 && !estMembre) {
            System.out.println("Tarif adulte");
        } else {
            System.out.println("Tarif réduit ou membre");
        }
        boolean adolescent = age >= 13 && age <= 19;
        System.out.println("Adolescent : " + adolescent);
    }
}
```

```text
Entrée autorisée
Tarif réduit ou membre
Adolescent : true
```

`&&` et `||` sont **paresseux** (*short-circuit*) : si la première partie suffit à décider, la seconde n'est pas évaluée. On en profite pour écrire `texte != null && texte.length() > 3` sans risque d'erreur si `texte` est `null` (absence d'objet).

## L'opérateur ternaire

Pour choisir entre **deux valeurs**, l'opérateur ternaire `condition ? valeurSiVrai : valeurSiFaux` est plus compact qu'un `if` :

```java
public class Ternaire {
    public static void main(String[] args) {
        int stock = 0;
        String etat = stock > 0 ? "disponible" : "en rupture";
        System.out.println("Article " + etat);
        int articles = 1;
        System.out.println(articles + " article" + (articles > 1 ? "s" : ""));
    }
}
```

```text
Article en rupture
1 article
```

Réservez-le aux choix simples ; au-delà, un `if` reste plus lisible.

## switch : choisir parmi plusieurs cas

Quand on compare **une même valeur** à plusieurs constantes, `switch` est plus clair qu'une suite de `else if`. Java moderne propose une syntaxe avec des flèches `->`, sans risque d'« oublier un `break` » :

```java
public class Jours {
    public static void main(String[] args) {
        String jour = "samedi";
        switch (jour) {
            case "samedi", "dimanche" -> System.out.println("Week-end");
            case "mercredi" -> System.out.println("Milieu de semaine");
            default -> System.out.println("Jour ouvré");
        }

        int numeroMois = 4;
        int nbJours = switch (numeroMois) {
            case 2 -> 28;
            case 4, 6, 9, 11 -> 30;
            default -> 31;
        };
        System.out.println("Mois " + numeroMois + " : " + nbJours + " jours");
    }
}
```

```text
Week-end
Mois 4 : 30 jours
```

- Plusieurs valeurs peuvent partager une branche : `case 4, 6, 9, 11`.
- `default` traite tous les autres cas.
- La seconde forme est une **expression `switch`** : elle **produit une valeur** que l'on range dans `nbJours` (notez le `;` final). Le compilateur exige alors que tous les cas soient couverts, d'où le `default`.

> Vous rencontrerez aussi l'ancienne syntaxe `case 1: … break;`. Sans `break`, l'exécution « tombe » dans le cas suivant, une source fréquente de bugs : préférez les flèches.

## Imbriquer avec modération

Une condition peut en contenir une autre, mais au-delà de deux niveaux le code devient difficile à lire. Souvent, combiner les conditions avec `&&` ou tester d'abord les cas d'erreur suffit :

```java
public class Livraison {
    public static void main(String[] args) {
        double montant = 42.0;
        boolean premium = false;
        double frais;
        if (montant <= 0) {
            System.out.println("Panier vide");
            return;  // quitte main immédiatement
        }
        if (premium || montant >= 50) {
            frais = 0;
        } else {
            frais = 4.99;
        }
        System.out.println("Frais de livraison : " + frais);
    }
}
```

```text
Frais de livraison : 4.99
```

Traiter le cas particulier d'abord, puis sortir avec `return`, évite d'imbriquer tout le reste dans un `else`.

## À retenir

- Comparaisons : `==`, `!=`, `<`, `<=`, `>`, `>=` ; chaînes avec `equals`.
- `if` / `else if` / `else` : la première condition vraie l'emporte ; toujours des accolades.
- `&&` (ET), `||` (OU), `!` (NON) ; `&&` et `||` n'évaluent la seconde partie que si nécessaire.
- Ternaire `cond ? a : b` pour choisir entre deux valeurs.
- `switch` avec `->` : plusieurs valeurs par `case`, `default`, et forme expression qui renvoie une valeur.

## Exercices

### Exercice 1 — Pair ou impair, positif ou négatif

Pour `int n = -7;`, affichez `-7 est impair et négatif`.

```solution-java
public class Parite {
    public static void main(String[] args) {
        int n = -7;
        String parite = n % 2 == 0 ? "pair" : "impair";
        String signe;
        if (n > 0) {
            signe = "positif";
        } else if (n < 0) {
            signe = "négatif";
        } else {
            signe = "nul";
        }
        System.out.println(n + " est " + parite + " et " + signe);
    }
}
```

```text
-7 est impair et négatif
```

Remarque : `-7 % 2` vaut `-1` en Java, d'où le test `== 0` plutôt que `== 1`.

### Exercice 2 — Tarif de cinéma

Plein tarif 11 €, moins de 14 ans 6 €, étudiant ou plus de 65 ans 8 €. Affichez le tarif pour `age = 22` et `etudiant = true`.

```solution-java
public class Cinema {
    public static void main(String[] args) {
        int age = 22;
        boolean etudiant = true;
        int tarif;
        if (age < 14) {
            tarif = 6;
        } else if (etudiant || age > 65) {
            tarif = 8;
        } else {
            tarif = 11;
        }
        System.out.println("Tarif : " + tarif + " EUR");
    }
}
```

```text
Tarif : 8 EUR
```

### Exercice 3 — Saison

Avec une expression `switch`, associez un numéro de mois (1 à 12) à une saison (hiver : 12, 1, 2 ; printemps : 3, 4, 5 ; été : 6, 7, 8 ; automne : 9, 10, 11) et affichez celle du mois 10.

```solution-java
public class Saison {
    public static void main(String[] args) {
        int mois = 10;
        String saison = switch (mois) {
            case 12, 1, 2 -> "hiver";
            case 3, 4, 5 -> "printemps";
            case 6, 7, 8 -> "été";
            case 9, 10, 11 -> "automne";
            default -> "mois invalide";
        };
        System.out.println("Mois " + mois + " : " + saison);
    }
}
```

```text
Mois 10 : automne
```
"""

M2_L2 = r"""
## Pourquoi des boucles ?

Une **boucle** répète un bloc d'instructions. Plutôt que d'écrire dix fois `System.out.println`, on écrit une boucle qui tourne dix fois. Java en propose quatre formes.

## La boucle while

`while` répète **tant que** la condition est vraie. Elle convient quand on ne sait pas à l'avance combien de tours seront nécessaires :

```java
public class Epargne {
    public static void main(String[] args) {
        double capital = 1000;
        int annees = 0;
        while (capital < 1200) {
            capital = capital * 1.05;   // +5 % par an
            annees++;
        }
        System.out.printf("Objectif atteint en %d ans (%.2f)%n", annees, capital);
    }
}
```

```text
Objectif atteint en 4 ans (1215.51)
```

> Si la condition ne devient jamais fausse, la boucle est **infinie** : le programme ne s'arrête pas (interrompez-le avec `Ctrl + C`). Vérifiez toujours que quelque chose, dans le corps de la boucle, rapproche de la sortie.

`do { … } while (condition);` est une variante qui exécute le corps **au moins une fois** avant de tester ; elle sert surtout à redemander une saisie jusqu'à ce qu'elle soit valide.

## La boucle for

`for` regroupe sur une ligne **l'initialisation**, **la condition** et **la mise à jour**. C'est la boucle idéale pour compter :

```java
public class Table {
    public static void main(String[] args) {
        for (int i = 1; i <= 5; i++) {
            System.out.println("7 x " + i + " = " + (7 * i));
        }
        for (int i = 10; i > 0; i -= 3) {
            System.out.print(i + " ");
        }
        System.out.println();
    }
}
```

```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
10 7 4 1
```

Lecture de `for (int i = 1; i <= 5; i++)` : « commencer avec `i = 1` ; tant que `i <= 5`, exécuter le bloc puis ajouter 1 à `i` ». La variable `i` n'existe qu'à l'intérieur de la boucle.

## Les tableaux

Un **tableau** (*array*) range plusieurs valeurs **du même type** sous un seul nom. Sa taille est fixée à la création :

```java
public class Tableaux {
    public static void main(String[] args) {
        int[] notes = {12, 15, 9, 17};
        String[] jours = new String[3];   // 3 cases, vides (null) au départ
        jours[0] = "lundi";
        jours[1] = "mardi";
        jours[2] = "mercredi";

        System.out.println(notes.length);   // taille : un attribut, sans parenthèses
        System.out.println(notes[0]);       // premier élément
        System.out.println(notes[notes.length - 1]);
        notes[2] = 10;                      // modification
        System.out.println(java.util.Arrays.toString(notes));
        System.out.println(jours[1]);
    }
}
```

```text
4
12
17
[12, 15, 10, 17]
mardi
```

- Les indices vont de `0` à `length - 1`. Accéder à `notes[4]` provoque une erreur à l'exécution (`ArrayIndexOutOfBoundsException`).
- `Arrays.toString` (classe `java.util.Arrays`) produit un affichage lisible ; `System.out.println(notes)` seul afficherait une référence peu parlante.
- Pour une liste dont la taille **varie**, on utilisera plutôt `ArrayList` (module 4).

## Parcourir un tableau : for et for-each

```java
public class Parcours {
    public static void main(String[] args) {
        double[] prix = {4.5, 12.0, 7.25};
        double total = 0;
        for (double p : prix) {          // « pour chaque p dans prix »
            total += p;
        }
        System.out.println("Total : " + total);

        for (int i = 0; i < prix.length; i++) {   // quand l'indice est utile
            System.out.println("Article " + (i + 1) + " : " + prix[i]);
        }
    }
}
```

```text
Total : 23.75
Article 1 : 4.5
Article 2 : 12.0
Article 3 : 7.25
```

La boucle **for-each** (`for (type element : tableau)`) est la plus lisible pour lire chaque élément. Utilisez le `for` classique quand vous avez besoin de la position ou que vous modifiez le tableau.

## break et continue

- `break` **sort** immédiatement de la boucle.
- `continue` **passe** directement au tour suivant.

```java
public class Recherche {
    public static void main(String[] args) {
        int[] valeurs = {3, -1, 8, 0, 42, 5};
        for (int v : valeurs) {
            if (v <= 0) {
                continue;          // ignore les valeurs nulles ou négatives
            }
            if (v > 40) {
                System.out.println("Trop grand : arrêt sur " + v);
                break;             // sort de la boucle
            }
            System.out.println("Valeur traitée : " + v);
        }
    }
}
```

```text
Valeur traitée : 3
Valeur traitée : 8
Trop grand : arrêt sur 42
```

## Boucles imbriquées

Une boucle peut en contenir une autre : pour chaque tour de la boucle extérieure, la boucle intérieure fait tous ses tours.

```java
public class Grille {
    public static void main(String[] args) {
        for (int ligne = 1; ligne <= 3; ligne++) {
            for (int col = 1; col <= ligne; col++) {
                System.out.print("* ");
            }
            System.out.println();
        }
    }
}
```

```text
*
* *
* * *
```

## À retenir

- `while` répète tant qu'une condition est vraie ; `do … while` au moins une fois.
- `for (init; condition; mise à jour)` est idéal pour compter.
- Un tableau a une taille fixe : `int[] t = {1, 2};`, `new String[3]`, indices de `0` à `length - 1`.
- `for (type x : tableau)` parcourt chaque élément ; `Arrays.toString` affiche un tableau.
- `break` sort de la boucle, `continue` passe au tour suivant.

## Exercices

### Exercice 1 — Somme et maximum

Pour `int[] ventes = {120, 340, 90, 410, 205};`, calculez la somme, la moyenne et la plus grande valeur.

```solution-java
public class Ventes {
    public static void main(String[] args) {
        int[] ventes = {120, 340, 90, 410, 205};
        int somme = 0;
        int max = ventes[0];
        for (int v : ventes) {
            somme += v;
            if (v > max) {
                max = v;
            }
        }
        double moyenne = (double) somme / ventes.length;
        System.out.println("Somme : " + somme);
        System.out.println("Moyenne : " + moyenne);
        System.out.println("Maximum : " + max);
    }
}
```

```text
Somme : 1165
Moyenne : 233.0
Maximum : 410
```

On initialise `max` avec le premier élément, et non avec `0`, pour que le calcul reste juste si toutes les valeurs sont négatives.

### Exercice 2 — FizzBuzz

Affichez les nombres de 1 à 15 sur une ligne, en remplaçant les multiples de 3 par `Fizz`, ceux de 5 par `Buzz` et ceux de 15 par `FizzBuzz`.

```solution-java
public class FizzBuzz {
    public static void main(String[] args) {
        for (int i = 1; i <= 15; i++) {
            if (i % 15 == 0) {
                System.out.print("FizzBuzz ");
            } else if (i % 3 == 0) {
                System.out.print("Fizz ");
            } else if (i % 5 == 0) {
                System.out.print("Buzz ");
            } else {
                System.out.print(i + " ");
            }
        }
        System.out.println();
    }
}
```

```text
1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz
```

Le test sur 15 doit venir **en premier**, sinon les multiples de 15 seraient capturés par le test sur 3.

### Exercice 3 — Compte à rebours

Avec une boucle `while`, affichez `5 4 3 2 1 Décollage !`.

```solution-java
public class Rebours {
    public static void main(String[] args) {
        int n = 5;
        while (n > 0) {
            System.out.print(n + " ");
            n--;
        }
        System.out.println("Décollage !");
    }
}
```

```text
5 4 3 2 1 Décollage !
```
"""

M2_L3 = r"""
## Pourquoi des méthodes ?

Une **méthode** regroupe des instructions sous un nom pour pouvoir les réutiliser. Vous en utilisez déjà : `println`, `length`, `Math.max`… Écrire vos propres méthodes permet de **découper** un problème en petites étapes, d'éviter le copier-coller et de tester chaque partie séparément.

Dans ce module, nos méthodes sont déclarées `static` : elles appartiennent à la classe et s'appellent directement, comme `main`. Le module 3 présentera les méthodes liées aux objets.

## Déclarer et appeler une méthode

```java
public class Salutations {
    static void saluer(String prenom) {
        System.out.println("Bonjour " + prenom + " !");
    }

    public static void main(String[] args) {
        saluer("Amina");
        saluer("Lucas");
    }
}
```

```text
Bonjour Amina !
Bonjour Lucas !
```

La **signature** `static void saluer(String prenom)` indique :

- `void` : la méthode ne **renvoie** rien, elle agit (ici, elle affiche) ;
- `saluer` : son nom, en camelCase et de préférence un **verbe** ;
- `(String prenom)` : un **paramètre** de type `String`. À l'appel, la valeur fournie (l'**argument**) est copiée dans `prenom`.

## Renvoyer une valeur avec return

Une méthode peut **calculer** un résultat et le renvoyer avec `return`. Son type de retour remplace alors `void` :

```java
public class Calculs {
    static double prixTTC(double prixHT, double taux) {
        return prixHT * (1 + taux);
    }

    static boolean estPair(int n) {
        return n % 2 == 0;
    }

    static int maximum(int[] valeurs) {
        int max = valeurs[0];
        for (int v : valeurs) {
            if (v > max) {
                max = v;
            }
        }
        return max;
    }

    public static void main(String[] args) {
        double ttc = prixTTC(50, 0.2);
        System.out.println("TTC : " + ttc);
        System.out.println("8 pair ? " + estPair(8));
        System.out.println("Max : " + maximum(new int[] {4, 19, 7}));
    }
}
```

```text
TTC : 60.0
8 pair ? true
Max : 19
```

- `return` **termine** la méthode immédiatement.
- Le compilateur vérifie que la valeur renvoyée a le bon type, et que **tous les chemins** se terminent par un `return`.
- Une méthode qui renvoie une valeur ne l'affiche pas : c'est l'appelant qui décide quoi en faire. Séparer **calcul** et **affichage** rend le code réutilisable.

## Plusieurs paramètres et surcharge

Une méthode peut recevoir plusieurs paramètres, séparés par des virgules. Java autorise aussi la **surcharge** (*overloading*) : plusieurs méthodes de même nom, à condition que leurs paramètres diffèrent (en nombre ou en type).

```java
public class Surcharge {
    static int aire(int cote) {
        return cote * cote;
    }

    static int aire(int longueur, int largeur) {
        return longueur * largeur;
    }

    static double aire(double rayon) {
        return Math.PI * rayon * rayon;
    }

    public static void main(String[] args) {
        System.out.println(aire(4));
        System.out.println(aire(4, 3));
        System.out.printf("%.2f%n", aire(1.5));
    }
}
```

```text
16
12
7.07
```

Le compilateur choisit la bonne version selon les arguments : `aire(4)` → un `int`, `aire(1.5)` → un `double`.

## Portée des variables et passage par valeur

Une variable déclarée dans une méthode (ou dans un bloc `{ }`) n'existe **que là** : c'est sa **portée**. Deux méthodes peuvent donc utiliser le même nom de variable sans conflit.

Java transmet les arguments **par valeur** : la méthode reçoit une **copie**. Modifier un paramètre de type primitif n'a aucun effet chez l'appelant. En revanche, pour un tableau (ou un objet), la copie porte sur la **référence** : la méthode accède au **même** tableau et peut modifier son contenu.

```java
import java.util.Arrays;

public class Passage {
    static void doubler(int n) {
        n = n * 2;  // modifie la copie locale seulement
    }

    static void doublerTout(int[] t) {
        for (int i = 0; i < t.length; i++) {
            t[i] = t[i] * 2;  // modifie le tableau partagé
        }
    }

    public static void main(String[] args) {
        int x = 5;
        doubler(x);
        System.out.println(x);

        int[] valeurs = {1, 2, 3};
        doublerTout(valeurs);
        System.out.println(Arrays.toString(valeurs));
    }
}
```

```text
5
[2, 4, 6]
```

Cette distinction entre **valeur primitive** et **référence** est essentielle en Java ; elle reviendra avec les objets.

## Découper un programme

Voici un petit programme d'analyse de notes, découpé en méthodes courtes qui font chacune **une seule chose** :

```java
public class Bulletin {
    static double moyenne(double[] notes) {
        double somme = 0;
        for (double n : notes) {
            somme += n;
        }
        return somme / notes.length;
    }

    static String appreciation(double moy) {
        if (moy >= 14) {
            return "Très bon travail";
        } else if (moy >= 10) {
            return "Résultats corrects";
        }
        return "Des efforts sont nécessaires";
    }

    static void afficherBulletin(String nom, double[] notes) {
        double moy = moyenne(notes);
        System.out.printf("%s : %.2f — %s%n", nom, moy, appreciation(moy));
    }

    public static void main(String[] args) {
        afficherBulletin("Inès", new double[] {15, 13.5, 17});
        afficherBulletin("Hugo", new double[] {9, 11, 8.5});
    }
}
```

```text
Inès : 15.17 — Très bon travail
Hugo : 9.50 — Des efforts sont nécessaires
```

Chaque méthode est courte, nommée par ce qu'elle fait, et peut être testée seule : c'est la clé d'un code lisible.

## À retenir

- Une méthode : `static typeRetour nom(type param, …) { … }` ; `void` si elle ne renvoie rien.
- `return valeur;` renvoie un résultat et termine la méthode.
- La surcharge permet plusieurs méthodes de même nom avec des paramètres différents.
- Les variables locales n'existent que dans leur bloc ; les arguments sont passés par valeur (copie de la valeur ou de la référence).
- Découpez : une méthode = une tâche, un nom explicite ; séparez calcul et affichage.

## Exercices

### Exercice 1 — Conversion de température

Écrivez `celsiusVersFahrenheit(double c)` (formule `c * 9 / 5 + 32`) et affichez le résultat pour 0, 37 et 100.

```solution-java
public class Temperature {
    static double celsiusVersFahrenheit(double c) {
        return c * 9 / 5 + 32;
    }

    public static void main(String[] args) {
        double[] valeurs = {0, 37, 100};
        for (double c : valeurs) {
            System.out.println(c + " °C = " + celsiusVersFahrenheit(c) + " °F");
        }
    }
}
```

```text
0.0 °C = 32.0 °F
37.0 °C = 98.6 °F
100.0 °C = 212.0 °F
```

### Exercice 2 — Compter les voyelles

Écrivez `compterVoyelles(String texte)` qui renvoie le nombre de voyelles (a, e, i, o, u, y), sans tenir compte des majuscules.

```solution-java
public class Voyelles {
    static int compterVoyelles(String texte) {
        int compte = 0;
        String minuscules = texte.toLowerCase();
        for (int i = 0; i < minuscules.length(); i++) {
            char c = minuscules.charAt(i);
            if ("aeiouy".indexOf(c) >= 0) {
                compte++;
            }
        }
        return compte;
    }

    public static void main(String[] args) {
        System.out.println(compterVoyelles("Programmation Java"));
    }
}
```

```text
7
```

`"aeiouy".indexOf(c)` renvoie `-1` si le caractère n'est pas une voyelle : une astuce simple pour tester l'appartenance à une liste de caractères.

### Exercice 3 — Nombre premier

Écrivez `estPremier(int n)` (un nombre premier a exactement deux diviseurs : 1 et lui-même), puis affichez les nombres premiers inférieurs à 30.

```solution-java
public class Premiers {
    static boolean estPremier(int n) {
        if (n < 2) {
            return false;
        }
        for (int d = 2; d * d <= n; d++) {
            if (n % d == 0) {
                return false;
            }
        }
        return true;
    }

    public static void main(String[] args) {
        for (int i = 1; i < 30; i++) {
            if (estPremier(i)) {
                System.out.print(i + " ");
            }
        }
        System.out.println();
    }
}
```

```text
2 3 5 7 11 13 17 19 23 29
```

Il suffit de tester les diviseurs jusqu'à la racine carrée de `n` (`d * d <= n`) : si `n` avait un diviseur plus grand, il en aurait aussi un plus petit.
"""

QUIZ_M1 = [
    ("single", "Quel outil du JDK transforme un fichier .java en bytecode (.class) ?", None,
     ["java", "javac", "jar", "la JVM"], [1],
     "javac est le compilateur : il vérifie le code source et produit le fichier .class. La commande java lance ensuite la JVM qui l'exécute."),
    ("single", "Votre fichier contient public class Facture. Comment doit-il s'appeler ?", None,
     ["facture.java", "Facture.class", "Facture.java", "N'importe quel nom se terminant par .java"], [2],
     "Une classe publique doit être enregistrée dans un fichier portant exactement son nom, majuscules comprises, avec l'extension .java."),
    ("single", "Qu'affiche ce programme ?", "System.out.println(7 / 2);\nSystem.out.println(7 % 2);",
     ["3.5 puis 1", "3 puis 1", "3 puis 0.5", "3.5 puis 0"], [1],
     "7 et 2 sont des int : la division est entière (3) et % donne le reste de la division (1)."),
    ("single", "Quelle déclaration est refusée par le compilateur ?", None,
     ["double prix = 10;", "long n = 5;", "int age = \"vingt\";", "var nom = \"Léa\";"], [2],
     "Une chaîne ne peut pas être rangée dans un int : erreur « incompatible types ». Les autres déclarations sont valides (int vers double ou long est une conversion automatique)."),
    ("multiple", "Quelles affirmations sur String sont exactes ?", None,
     ["String est une classe, pas un type primitif.", "Pour comparer le contenu de deux chaînes, on utilise equals.", "toUpperCase() modifie la chaîne d'origine.", "Le premier caractère d'une chaîne est à l'indice 0."], [0, 1, 3],
     "Les chaînes sont immuables : toUpperCase() renvoie une nouvelle chaîne sans modifier l'originale. Les trois autres affirmations sont exactes."),
    ("single", "Que vaut \"Bonjour\".substring(0, 3) ?", None,
     ["\"Bon\"", "\"Bonj\"", "\"onj\"", "\"Bo\""], [0],
     "substring(début, fin) prend les caractères de l'indice 0 inclus à l'indice 3 exclu : B, o, n."),
    ("single", "Que produit String.format(\"%.2f\", 3.14159) sur un système configuré en anglais ?", None,
     ["3.14159", "3.1", "3.14", "3"], [2],
     "%.2f affiche un nombre décimal avec deux chiffres après la virgule. Sur un système en français, le séparateur pourrait être une virgule."),
    ("single", "Que faut-il écrire en haut du fichier pour utiliser Scanner ?", None,
     ["include java.util.Scanner;", "import java.util.Scanner;", "using Scanner;", "Rien, Scanner est toujours disponible"], [1],
     "Scanner appartient au package java.util, qu'il faut importer avec import java.util.Scanner;."),
    ("single", "Que vaut l'expression (int) 9.99 ?", None,
     ["10", "9", "9.99", "Une erreur de compilation"], [1],
     "Le cast (int) tronque la partie décimale sans arrondir : on obtient 9. Pour arrondir, on utilise Math.round."),
    ("true_false", "Une variable déclarée avec var peut recevoir plus tard une valeur d'un autre type.", None,
     ["Vrai", "Faux"], [1],
     "var laisse seulement le compilateur déduire le type à la déclaration ; ce type reste ensuite fixe, comme pour toute variable Java."),
]

QUIZ_M2 = [
    ("single", "Qu'affiche ce code ?", "int note = 12;\nif (note >= 14) {\n    System.out.println(\"Bien\");\n} else if (note >= 10) {\n    System.out.println(\"Passable\");\n} else {\n    System.out.println(\"Insuffisant\");\n}",
     ["Bien", "Insuffisant", "Passable puis Insuffisant", "Passable"], [3],
     "12 n'est pas ≥ 14, mais il est ≥ 10 : seule la première branche vraie s'exécute, donc « Passable »."),
    ("single", "Que vaut (5 > 3) && !(2 == 2) ?", None,
     ["true", "false", "Erreur de compilation", "null"], [1],
     "5 > 3 est vrai, 2 == 2 est vrai donc !(2 == 2) est faux ; vrai ET faux donne false."),
    ("multiple", "Quelles affirmations sur le switch avec flèches (->) sont exactes ?", None,
     ["Un case peut regrouper plusieurs valeurs : case 4, 6 ->", "Il faut un break à la fin de chaque branche.", "Une expression switch peut renvoyer une valeur rangée dans une variable.", "default traite les valeurs non listées."], [0, 2, 3],
     "Avec les flèches, il n'y a pas de « chute » d'un cas au suivant : aucun break n'est nécessaire. Les trois autres affirmations sont exactes."),
    ("single", "Combien de fois ce code affiche-t-il « Java » ?", "for (int i = 0; i < 4; i++) {\n    System.out.println(\"Java\");\n}",
     ["3", "4", "5", "Une infinité"], [1],
     "i prend les valeurs 0, 1, 2 et 3 ; à 4, la condition i < 4 devient fausse. La boucle fait donc 4 tours."),
    ("single", "Quel est l'indice du dernier élément d'un tableau t ?", None,
     ["t.length", "t.length - 1", "t.length()", "t.size() - 1"], [1],
     "Les indices commencent à 0, donc le dernier est t.length - 1. Pour un tableau, length est un attribut sans parenthèses."),
    ("single", "Que fait l'instruction continue dans une boucle ?", None,
     ["Elle passe directement au tour suivant.", "Elle sort de la boucle.", "Elle recommence la boucle depuis le début.", "Elle arrête le programme."], [0],
     "continue saute la fin du tour en cours et passe au suivant ; c'est break qui sort de la boucle."),
    ("single", "Quelle boucle exécute toujours son corps au moins une fois ?", None,
     ["while", "for", "do … while", "for-each"], [2],
     "do … while teste la condition après avoir exécuté le corps, qui s'exécute donc au moins une fois."),
    ("single", "Quelle est la bonne signature pour une méthode qui reçoit deux entiers et renvoie leur moyenne décimale ?", None,
     ["static void moyenne(int a, int b)", "static int moyenne(double a, b)", "static double moyenne(int a, int b)", "static moyenne(int a, int b) double"], [2],
     "Le type de retour (double) précède le nom, et chaque paramètre a son propre type. void signifierait que la méthode ne renvoie rien."),
    ("single", "Qu'affiche ce programme ?", "static void ajouter(int n) {\n    n = n + 10;\n}\n\npublic static void main(String[] args) {\n    int x = 1;\n    ajouter(x);\n    System.out.println(x);\n}",
     ["11", "10", "Erreur de compilation", "1"], [3],
     "Java passe les arguments par valeur : la méthode modifie une copie de x. La variable x de main vaut toujours 1."),
    ("true_false", "Deux méthodes d'une même classe peuvent porter le même nom si leurs paramètres diffèrent.", None,
     ["Vrai", "Faux"], [0],
     "C'est la surcharge : le compilateur choisit la version adaptée selon le nombre et le type des arguments."),
]

MODULES = [
    {
        "position": 1,
        "title": "Premiers pas en Java",
        "description": "Installer le JDK, compiler et exécuter un programme, utiliser variables, types, opérateurs, chaînes et saisie au clavier.",
        "status": "published",
        "lessons": [
            ("jdk-et-premier-programme", "Le JDK et votre premier programme",
             "JDK, JVM, javac et java : écrire, compiler et exécuter une classe.", M1_L1, 40),
            ("variables-types-operateurs", "Variables, types et opérateurs",
             "Types primitifs, var, final, calculs, division entière et conversions.", M1_L2, 45),
            ("texte-et-saisie", "Le texte et la saisie au clavier",
             "Méthodes de String, equals, String.format, conversions et Scanner.", M1_L3, 45),
        ],
        "quiz": ("Quiz — Premiers pas en Java", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Contrôler l'exécution",
        "description": "Prendre des décisions, répéter des instructions, utiliser des tableaux et découper un programme en méthodes.",
        "status": "published",
        "lessons": [
            ("conditions-et-switch", "Conditions et switch",
             "if, else, opérateurs logiques, ternaire et switch moderne.", M2_L1, 40),
            ("boucles-et-tableaux", "Boucles et tableaux",
             "while, for, for-each, tableaux, break et continue.", M2_L2, 45),
            ("methodes", "Les méthodes",
             "Paramètres, valeur de retour, surcharge, portée et passage par valeur.", M2_L3, 45),
        ],
        "quiz": ("Quiz — Contrôler l'exécution", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Programmation orientée objet",
        "description": "Créer des classes et des objets, protéger leurs données par l'encapsulation et réutiliser du code par l'héritage.",
        "status": "published",
        "lessons": [
            ("classes-et-objets", "Classes, objets et constructeurs",
             "Attributs, méthodes, constructeurs, this, toString et références.", _m35.M3_L1, 45),
            ("encapsulation", "L'encapsulation",
             "private, accesseurs, validation, membres static et constantes.", _m35.M3_L2, 45),
            ("heritage", "L'héritage",
             "extends, super, redéfinition avec @Override et la classe Object.", _m35.M3_L3, 45),
        ],
        "quiz": ("Quiz — Programmation orientée objet", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Abstraction et collections",
        "description": "Classes abstraites, interfaces et polymorphisme, puis listes dynamiques et dictionnaires avec ArrayList et HashMap.",
        "status": "published",
        "lessons": [
            ("interfaces-et-polymorphisme", "Classes abstraites, interfaces et polymorphisme",
             "abstract, interface, implements et traitement uniforme d'objets différents.", _m35.M4_L1, 45),
            ("arraylist", "Les listes avec ArrayList",
             "Ajouter, retirer, parcourir et trier une liste dynamique.", _m35.M4_L2, 45),
            ("hashmap", "Les dictionnaires avec HashMap",
             "Associer des clés à des valeurs, compter, regrouper et parcourir.", _m35.M4_L3, 45),
        ],
        "quiz": ("Quiz — Abstraction et collections", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Exceptions, records et projet",
        "description": "Gérer les erreurs avec les exceptions, modéliser des données avec les records, puis réaliser une gestion de bibliothèque en console.",
        "status": "published",
        "lessons": [
            ("exceptions", "Les exceptions",
             "try, catch, finally, throw, exceptions vérifiées et personnalisées.", _m35.M5_L1, 45),
            ("records", "Les records et les données immuables",
             "Déclarer un record, equals, validation et records dans les collections.", _m35.M5_L2, 40),
            ("mini-projet-bibliotheque", "Mini-projet : gestion d'une bibliothèque",
             "Une application console complète : classes, collections, exceptions et records.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Exceptions, records et projet", _m35.QUIZ_M5),
    },
]
