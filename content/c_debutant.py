"""Contenu de la formation « Langage C » (SMK Academy).

Blocs ```c pour le code, ```text pour la sortie du programme, ```solution-c pour les corrections,
```bash pour les commandes du terminal et ```h pour les fichiers d'en-tête.
Chaque bloc ```c ou ```solution-c suivi d'un bloc ```text est compilé (gcc -std=c17 -Wall), exécuté
et comparé à ce bloc par scripts/check_code_blocks.py.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("c_debutant_m3_m5", _Path(__file__).with_name("c_debutant_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "c-debutant",
    "title": "Langage C",
    "subtitle": "Comprendre la mémoire et les pointeurs.",
    "description": (
        "Le C est le langage des systèmes d'exploitation, de l'embarqué et de nombreux outils que vous utilisez "
        "chaque jour. Cette formation part de zéro : compilation avec gcc, variables, conditions, boucles et "
        "fonctions, puis tableaux, chaînes et pointeurs, mémoire dynamique, structures et fichiers. Une attention "
        "particulière est portée à la sûreté mémoire (comportements indéfinis, dépassements, fuites) et aux outils "
        "qui les détectent. Chaque leçon propose des programmes complets et des exercices corrigés ; chaque module "
        "se termine par un quiz noté sur 20."
    ),
    "category": "Programmation",
    "category_slug": "programmation",
    "topic": "C",
    "cover_label": "C",
    "level": "debutant",
    "duration_minutes": 840,
    "objectives": [
        "Écrire et compiler un programme C",
        "Utiliser pointeurs et tableaux",
        "Gérer la mémoire dynamique",
    ],
    "prerequisites": ["Aucun prérequis"],
    "status": "published",
    "is_premium": False,
    "position": 14,
}

# ---------------------------------------------------------------------------
# Module 1 — Compilation et bases
# ---------------------------------------------------------------------------
M1_L1 = r"""
## Qu'est-ce que le langage C ?

Le **C** a été créé au début des années 1970 aux laboratoires Bell, pour écrire le système Unix. Plus de cinquante ans plus tard, il reste partout :

- dans les **systèmes d'exploitation** (le noyau Linux est écrit essentiellement en C) ;
- dans l'**embarqué** : microcontrôleurs, objets connectés, automobile ;
- dans les **outils et bibliothèques** de base : l'interpréteur Python officiel (CPython), de nombreuses bases de données, des compilateurs.

Apprendre le C, c'est comprendre **ce qui se passe sous le capot** : comment les données sont rangées en mémoire, ce qu'est une adresse, pourquoi un programme peut planter. Ces notions vous serviront ensuite dans n'importe quel langage.

> Le C vous donne beaucoup de pouvoir et peu de garde-fous : le compilateur fait ce que vous écrivez, même si c'est une erreur. Tout au long de cette formation, nous insisterons sur les **bonnes pratiques de sûreté**.

## Un langage compilé

En Python ou en JavaScript, un programme est lu et exécuté par un interpréteur. En C, le code source doit d'abord être **compilé** : un programme appelé **compilateur** le traduit en **exécutable**, un fichier en langage machine que le processeur exécute directement.

La compilation se déroule en trois grandes étapes :

| Étape | Rôle |
|---|---|
| Préprocesseur | traite les lignes commençant par `#` (inclusion de fichiers, constantes) |
| Compilation | traduit le C en code machine (fichier objet) |
| Édition des liens (*linking*) | assemble votre code et les bibliothèques en un exécutable |

Nous utiliserons **gcc** (*GNU Compiler Collection*), le compilateur libre le plus répandu. **clang** est une alternative très proche, avec les mêmes options de base.

## Installer un compilateur

- **Linux** (Debian, Ubuntu) : `sudo apt install build-essential` installe gcc et les outils associés.
- **macOS** : `xcode-select --install` installe les outils en ligne de commande ; la commande `gcc` y lance en réalité clang, ce qui convient parfaitement pour cette formation.
- **Windows** : le plus simple est d'utiliser **WSL** (un Linux intégré à Windows) puis la commande Linux ci-dessus, ou l'environnement **MSYS2**.

Vérifiez l'installation dans un terminal avec `gcc --version`. Un simple éditeur de texte suffit ensuite ; un éditeur comme VS Code apporte la coloration et l'autocomplétion.

## Votre premier programme

Créez un fichier `bonjour.c` :

```c
#include <stdio.h>

int main(void)
{
    printf("Bonjour, SMK Academy !\n");
    return 0;
}
```

```text
Bonjour, SMK Academy !
```

Ligne par ligne :

- `#include <stdio.h>` demande au préprocesseur d'inclure la déclaration des fonctions d'entrée-sortie standard (*standard input/output*), dont `printf` ;
- `int main(void)` est la **fonction principale** : l'exécution commence toujours ici. `int` indique qu'elle renvoie un entier, `void` qu'elle ne reçoit aucun paramètre ;
- les **accolades** `{ }` délimitent le corps de la fonction ;
- `printf(...)` affiche du texte ; `\n` est le **retour à la ligne** ;
- `return 0;` termine le programme en signalant au système que tout s'est bien passé (une valeur différente de 0 signale une erreur).

Chaque instruction se termine par un **point-virgule**.

## Compiler et exécuter

Dans le terminal, placez-vous dans le dossier du fichier et tapez :

```bash
gcc -std=c17 -Wall -Wextra -o bonjour bonjour.c
./bonjour
```

| Option | Signification |
|---|---|
| `-std=c17` | utiliser la norme C17 du langage |
| `-Wall -Wextra` | activer les principaux **avertissements** (*warnings*) |
| `-o bonjour` | nommer l'exécutable `bonjour` (sinon il s'appelle `a.out`) |

`./bonjour` lance l'exécutable situé dans le dossier courant (sous Windows natif, il s'appelle `bonjour.exe`).

> Le C a connu plusieurs versions normalisées : C89, C99, C11, C17 et plus récemment C23. Nous utilisons C17, bien pris en charge par tous les compilateurs actuels.

## Lire une erreur de compilation

Oublions le point-virgule après `printf(...)`. gcc refuse de compiler et affiche :

```text
bonjour.c: In function 'main':
bonjour.c:5:39: error: expected ';' before 'return'
    5 |     printf("Bonjour, SMK Academy !\n")
      |                                       ^
      |                                       ;
```

Le message indique le **fichier**, la **ligne** (5) et la **colonne** (39), puis la nature du problème. Lisez toujours la **première** erreur en premier : les suivantes en sont souvent la conséquence.

## Ne jamais ignorer un avertissement

Un **avertissement** n'empêche pas la compilation, mais il signale très souvent un vrai bogue. Sans `#include <stdio.h>`, gcc 13 affiche par exemple :

```text
noinc.c:3:5: warning: implicit declaration of function 'printf' [-Wimplicit-function-declaration]
```

Selon la version du compilateur, ce cas est un simple avertissement ou une erreur. Prenez l'habitude de compiler **toujours** avec `-Wall -Wextra` et de corriger chaque avertissement : un programme qui compile « avec des warnings » n'est pas terminé.

## Les commentaires

```c
#include <stdio.h>

/* Commentaire
   sur plusieurs lignes */
int main(void)
{
    // Commentaire sur une ligne
    printf("%d\n", 2 + 3); // affiche 5
    return 0;
}
```

```text
5
```

`%d` est un **indicateur de format** : il est remplacé par la valeur entière qui suit. Nous y reviendrons en détail.

## À retenir

- Le C est **compilé** : code source `.c` → compilateur → exécutable.
- Tout programme commence par `int main(void)` et se termine par `return 0;` en cas de succès.
- `#include <stdio.h>` est nécessaire pour utiliser `printf`.
- Compilez avec `gcc -std=c17 -Wall -Wextra -o prog prog.c` et corrigez **chaque** avertissement.
- Lisez la première erreur en premier : fichier, ligne, colonne, message.

## Exercices

### Exercice 1 — Carte de visite

Écrivez un programme qui affiche votre prénom sur une ligne, puis `Formation : Langage C` sur la ligne suivante.

```solution-c
#include <stdio.h>

int main(void)
{
    printf("Amina\n");
    printf("Formation : Langage C\n");
    return 0;
}
```

```text
Amina
Formation : Langage C
```

### Exercice 2 — Trouvez les erreurs

Ce programme ne compile pas. Trouvez les trois erreurs.

```text
#include <stdio.h>

int Main(void)
{
    printf("Bonjour\n")
    return 0;
```

```solution-text
1. Le C distingue majuscules et minuscules : la fonction principale s'appelle main, pas Main.
2. Il manque le point-virgule après printf("Bonjour\n").
3. L'accolade fermante } de la fonction est absente.
```

### Exercice 3 — Un calcul

Affichez le résultat de `12 * 4` à l'aide de `printf` et de `%d`.

```solution-c
#include <stdio.h>

int main(void)
{
    printf("12 x 4 = %d\n", 12 * 4);
    return 0;
}
```

```text
12 x 4 = 48
```
"""

M1_L2 = r"""
## Les variables

Une **variable** est une zone de la mémoire, désignée par un nom, qui contient une valeur. En C, chaque variable a un **type** fixé à sa déclaration : le compilateur sait ainsi combien d'octets réserver et comment interpréter leur contenu.

```c
#include <stdio.h>

int main(void)
{
    int age = 25;
    double taille = 1.72;
    char initiale = 'S';

    printf("Âge : %d ans\n", age);
    printf("Taille : %.2f m\n", taille);
    printf("Initiale : %c\n", initiale);
    return 0;
}
```

```text
Âge : 25 ans
Taille : 1.72 m
Initiale : S
```

On peut modifier une variable après sa déclaration : `age = 26;`. En revanche, on ne peut pas changer son type.

Règles de nommage : lettres non accentuées, chiffres et `_`, sans commencer par un chiffre. Le C distingue les majuscules (`total` et `Total` sont deux variables). Par convention, on écrit souvent les noms en minuscules avec des `_` : `prix_total`, `nb_etudiants`.

## Les types de base

| Type | Contenu | Format `printf` |
|---|---|---|
| `int` | entier (positif ou négatif) | `%d` |
| `unsigned int` | entier positif ou nul | `%u` |
| `long long` | grand entier | `%lld` |
| `double` | nombre à virgule (double précision) | `%f` |
| `float` | nombre à virgule (simple précision) | `%f` |
| `char` | un caractère (petit entier) | `%c` |

Dans le code, le séparateur décimal est le **point** : `1.72`, pas `1,72`. Préférez `double` à `float` : il est plus précis et c'est le type des constantes décimales comme `1.72`.

## La taille des types : `sizeof`

L'opérateur `sizeof` donne la taille d'un type ou d'une variable, en **octets**. Son résultat est de type `size_t`, qui s'affiche avec `%zu`.

```c
#include <stdio.h>

int main(void)
{
    printf("char   : %zu octet(s)\n", sizeof(char));
    printf("int    : %zu octet(s)\n", sizeof(int));
    printf("double : %zu octet(s)\n", sizeof(double));
    return 0;
}
```

```text
char   : 1 octet(s)
int    : 4 octet(s)
double : 8 octet(s)
```

`sizeof(char)` vaut **toujours** 1. Les autres tailles dépendent de la machine et du compilateur : les valeurs ci-dessus sont celles d'un ordinateur 64 bits courant. Un `int` de 4 octets (32 bits) va de -2 147 483 648 à 2 147 483 647.

## Les caractères sont des nombres

Un `char` contient en réalité un **code numérique**. Les caractères s'écrivent entre **apostrophes** `'A'`, alors que les textes (chaînes) s'écrivent entre **guillemets** `"Bonjour"`.

```c
#include <stdio.h>

int main(void)
{
    char lettre = 'A';
    printf("%c a pour code %d\n", lettre, lettre);
    printf("La lettre suivante est %c\n", lettre + 1);
    return 0;
}
```

```text
A a pour code 65
La lettre suivante est B
```

## La division entière

Entre deux entiers, `/` effectue une **division entière** : la partie décimale est perdue. `%` donne le **reste**.

```c
#include <stdio.h>

int main(void)
{
    printf("%d\n", 7 / 2);
    printf("%d\n", 7 % 2);
    printf("%f\n", 7.0 / 2);
    printf("%.1f\n", (double) 7 / 2);
    return 0;
}
```

```text
3
1
3.500000
3.5
```

Il suffit qu'un des deux opérandes soit décimal pour obtenir une division décimale. `(double) 7` est une **conversion explicite** (*cast*) : elle transforme l'entier 7 en `double`. Par défaut, `%f` affiche 6 décimales ; `%.1f` en affiche une.

## Constantes

Une valeur qui ne doit pas changer se déclare avec `const`. Le préprocesseur permet aussi de définir des constantes avec `#define` (sans `=` ni point-virgule) :

```c
#include <stdio.h>

#define TAUX_TVA 0.20

int main(void)
{
    const double prix_ht = 50.0;
    printf("Prix TTC : %.2f euros\n", prix_ht * (1 + TAUX_TVA));
    return 0;
}
```

```text
Prix TTC : 60.00 euros
```

Une tentative de modification (`prix_ht = 40;`) est refusée par le compilateur.

## Deux pièges de sûreté

**1. Une variable non initialisée contient n'importe quoi.** `int total;` réserve la mémoire sans la remettre à zéro. Lire `total` avant de lui donner une valeur produit une valeur imprévisible : c'est un bogue, que `-Wall` signale souvent. **Initialisez toujours vos variables** : `int total = 0;`.

**2. Le dépassement de capacité.** Un type a des limites, définies dans `<limits.h>` :

```c
#include <stdio.h>
#include <limits.h>

int main(void)
{
    printf("INT_MAX = %d\n", INT_MAX);
    unsigned int u = 0;
    u = u - 1;
    printf("0 - 1 en unsigned = %u\n", u);
    return 0;
}
```

```text
INT_MAX = 2147483647
0 - 1 en unsigned = 4294967295
```

Pour un type **non signé**, le résultat « fait le tour » : c'est un comportement défini, mais rarement celui qu'on veut. Pour un `int` **signé**, dépasser `INT_MAX` (par exemple `INT_MAX + 1`) est un **comportement indéfini** (*undefined behavior*, UB).

> **Comportement indéfini** : la norme du C n'impose rien. Le programme peut sembler fonctionner, donner un résultat faux ou planter, et ce comportement peut changer d'une compilation à l'autre. C'est la principale source de bogues et de failles de sécurité en C : tout au long de la formation, nous apprendrons à les éviter.

## À retenir

- Chaque variable a un **type** : `int`, `double`, `char`… et se déclare avant usage.
- `sizeof` donne une taille en octets (`%zu`) ; seule `sizeof(char) == 1` est garantie.
- `7 / 2` vaut 3 entre entiers ; utilisez un `double` ou un *cast* pour une division décimale.
- `'A'` est un caractère (un nombre), `"A"` une chaîne.
- Initialisez toujours vos variables ; le dépassement d'un entier signé est un comportement indéfini.

## Exercices

### Exercice 1 — Moyenne

Avec trois notes entières 12, 15 et 16, affichez la moyenne avec deux décimales.

```solution-c
#include <stdio.h>

int main(void)
{
    int n1 = 12, n2 = 15, n3 = 16;
    double moyenne = (n1 + n2 + n3) / 3.0;
    printf("Moyenne : %.2f\n", moyenne);
    return 0;
}
```

```text
Moyenne : 14.33
```

Diviser par `3.0` (et non `3`) force une division décimale.

### Exercice 2 — Heures et minutes

Convertissez 135 minutes en heures et minutes avec `/` et `%`.

```solution-c
#include <stdio.h>

int main(void)
{
    int minutes = 135;
    printf("%d h %d min\n", minutes / 60, minutes % 60);
    return 0;
}
```

```text
2 h 15 min
```

### Exercice 3 — Code d'un caractère

Affichez le code numérique de `'a'` et le caractère dont le code vaut `'a' + 25`.

```solution-c
#include <stdio.h>

int main(void)
{
    printf("%d\n", 'a');
    printf("%c\n", 'a' + 25);
    return 0;
}
```

```text
97
z
```
"""

M1_L3 = r"""
## Les opérateurs arithmétiques et d'affectation

| Opérateur | Rôle | Exemple |
|---|---|---|
| `+ - * /` | opérations de base | `a * 2` |
| `%` | reste de la division entière | `17 % 5` vaut 2 |
| `+=`, `-=`, `*=`, `/=` | opération et affectation | `total += prix;` |
| `++`, `--` | ajouter ou retirer 1 | `compteur++;` |

La multiplication et la division sont prioritaires sur l'addition, comme en mathématiques. Dans le doute, ajoutez des **parenthèses** : elles rendent aussi le code plus lisible.

```c
#include <stdio.h>

int main(void)
{
    int a = 2 + 3 * 4;
    int b = (2 + 3) * 4;
    int compteur = 10;
    compteur += 5;
    compteur++;
    printf("a = %d, b = %d, compteur = %d\n", a, b, compteur);
    return 0;
}
```

```text
a = 14, b = 20, compteur = 16
```

> Évitez d'utiliser `++` sur une variable qui apparaît plusieurs fois dans la même expression (`i = i++ + 1;`) : c'est un comportement indéfini. Gardez `compteur++;` seul sur sa ligne.

## Bien utiliser `printf`

`printf` (*print formatted*) remplace chaque **indicateur de format** par l'argument correspondant, dans l'ordre.

| Indicateur | Type affiché |
|---|---|
| `%d` | `int` |
| `%u` | `unsigned int` |
| `%lld` | `long long` |
| `%f`, `%.2f` | `double` (6 ou 2 décimales) |
| `%c` | `char` |
| `%s` | chaîne de caractères |
| `%zu` | `size_t` (résultat de `sizeof`) |
| `%p` | adresse mémoire (module 3) |
| `%%` | le caractère `%` lui-même |

On peut aussi fixer une **largeur** pour aligner des colonnes : `%5d` occupe au moins 5 caractères alignés à droite, `%-10s` au moins 10 caractères alignés à gauche.

```c
#include <stdio.h>

int main(void)
{
    printf("%-10s|%5d|\n", "Stylos", 12);
    printf("%-10s|%5d|\n", "Cahiers", 140);
    printf("Remise : %d%%\n", 15);
    printf("Pi vaut environ %.3f\n", 3.14159);
    return 0;
}
```

```text
Stylos    |   12|
Cahiers   |  140|
Remise : 15%
Pi vaut environ 3.142
```

> Le type de l'argument **doit** correspondre à l'indicateur. `printf("%d", 3.5)` est un comportement indéfini et affiche n'importe quoi. Avec `-Wall`, gcc vérifie la plupart de ces correspondances et vous avertit.

## Les fonctions mathématiques

La bibliothèque `<math.h>` fournit `sqrt` (racine carrée), `pow` (puissance), `fabs` (valeur absolue d'un décimal), `round`, `floor`, `ceil`… Sous Linux, il faut ajouter l'option `-lm` à la fin de la commande de compilation pour lier la bibliothèque mathématique.

```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    printf("%.3f\n", sqrt(2.0));
    printf("%.0f\n", pow(2.0, 10.0));
    printf("%.1f\n", round(2.6));
    return 0;
}
```

```text
1.414
1024
3.0
```

```bash
gcc -std=c17 -Wall -Wextra -o maths maths.c -lm
```

## Lire une saisie au clavier : `scanf`

`scanf` lit des valeurs tapées au clavier selon des indicateurs de format proches de ceux de `printf`. Remarquez le `&` devant la variable : il transmet son **adresse**, pour que `scanf` puisse y écrire (les adresses sont expliquées au module 3).

```c
#include <stdio.h>

int main(void)
{
    int age = 0;
    printf("Votre âge : ");
    if (scanf("%d", &age) != 1) {
        printf("Saisie invalide.\n");
        return 1;
    }
    printf("Dans 10 ans, vous aurez %d ans.\n", age + 10);
    return 0;
}
```

Exemple d'exécution, si vous tapez `30` :

```text
Votre âge : 30
Dans 10 ans, vous aurez 40 ans.
```

`scanf` renvoie le **nombre de valeurs lues avec succès**. Si l'utilisateur tape `abc`, il renvoie 0 et `age` n'est pas modifié. **Testez toujours cette valeur de retour** : utiliser une variable que `scanf` n'a pas remplie est une source classique de bogues.

> Pour lire du texte, n'utilisez jamais `scanf("%s", ...)` sans limite de taille : une saisie trop longue déborde de la mémoire prévue. Nous verrons au module 3 la fonction `fgets`, plus sûre.

## Convertir un texte en nombre : `sscanf`

`sscanf` fonctionne comme `scanf`, mais lit dans une **chaîne** au lieu du clavier. C'est pratique pour analyser une ligne déjà lue, et pour tester sans clavier :

```c
#include <stdio.h>

int main(void)
{
    const char *ligne = "42 3.5";
    int quantite = 0;
    double prix = 0.0;
    int lus = sscanf(ligne, "%d %lf", &quantite, &prix);
    printf("Valeurs lues : %d\n", lus);
    printf("Total : %.2f\n", quantite * prix);
    return 0;
}
```

```text
Valeurs lues : 2
Total : 147.00
```

Attention : pour **lire** un `double`, `scanf` et `sscanf` utilisent `%lf`, alors que `printf` utilise `%f`.

## À retenir

- Priorités habituelles (`*` et `/` avant `+` et `-`) ; ajoutez des parenthèses en cas de doute.
- `printf` : un indicateur par argument, du **bon type** (`%d`, `%f`, `%c`, `%s`, `%zu`, `%%`).
- `<math.h>` demande l'option `-lm` sous Linux.
- `scanf("%d", &x)` : n'oubliez pas le `&` et **testez la valeur de retour**.
- Pour lire un `double` : `%lf` ; pour l'afficher : `%f`.

## Exercices

### Exercice 1 — Facture alignée

Affichez cette facture, avec le nom aligné à gauche sur 8 caractères et le prix aligné à droite sur 8 caractères avec 2 décimales : Café 2.5, Croissant 1.2.

```solution-c
#include <stdio.h>

int main(void)
{
    printf("%-8s%8.2f\n", "Café", 2.5);
    printf("%-8s%8.2f\n", "Croissant", 1.2);
    return 0;
}
```

```text
Café       2.50
Croissant    1.20
```

Remarquez deux détails. `Croissant` (9 caractères) dépasse la largeur de 8 : `printf` ne coupe jamais, il écrit tout. Et `é` occupe **deux octets** en UTF-8 : `printf` compte des octets, pas des caractères affichés, d'où un décalage d'un espace.

### Exercice 2 — Hypoténuse

Calculez l'hypoténuse d'un triangle rectangle de côtés 3 et 4 avec `sqrt`.

```solution-c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double a = 3.0, b = 4.0;
    printf("Hypoténuse : %.1f\n", sqrt(a * a + b * b));
    return 0;
}
```

```text
Hypoténuse : 5.0
```

### Exercice 3 — Analyser une date

Avec `sscanf`, extrayez le jour, le mois et l'année de la chaîne `"14/07/2025"`, puis affichez-les au format `2025-07-14`.

```solution-c
#include <stdio.h>

int main(void)
{
    int jour = 0, mois = 0, annee = 0;
    if (sscanf("14/07/2025", "%d/%d/%d", &jour, &mois, &annee) == 3) {
        printf("%d-%02d-%02d\n", annee, mois, jour);
    }
    return 0;
}
```

```text
2025-07-14
```

`%02d` complète l'affichage par des zéros à gauche, sur 2 chiffres.
"""

# ---------------------------------------------------------------------------
# Module 2 — Contrôle et fonctions
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Prendre une décision : `if`

```c
#include <stdio.h>

int main(void)
{
    int note = 14;
    if (note >= 10) {
        printf("Module validé\n");
    } else {
        printf("Module à repasser\n");
    }
    return 0;
}
```

```text
Module validé
```

La condition s'écrit **entre parenthèses**, le bloc **entre accolades**. Plusieurs cas s'enchaînent avec `else if` : le premier cas vrai l'emporte, les suivants ne sont pas testés.

```c
#include <stdio.h>

int main(void)
{
    int note = 17;
    if (note >= 16) {
        printf("Très bien\n");
    } else if (note >= 10) {
        printf("Validé\n");
    } else {
        printf("À retravailler\n");
    }
    return 0;
}
```

```text
Très bien
```

> Écrivez **toujours** les accolades, même pour une seule instruction. Sans elles, seule la première instruction dépend du `if` : ajouter une ligne plus tard crée un bogue invisible à la lecture.

## Comparaisons et vérité en C

| Opérateur | Signification |
|---|---|
| `==` | égal |
| `!=` | différent |
| `<`, `<=`, `>`, `>=` | comparaisons |

En C, une comparaison produit un **entier** : 1 si elle est vraie, 0 si elle est fausse. Dans une condition, **0 est faux et toute autre valeur est vraie**.

```c
#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    printf("%d\n", 5 > 3);
    printf("%d\n", 5 == 3);
    bool majeur = true;
    if (majeur) {
        printf("Accès autorisé\n");
    }
    return 0;
}
```

```text
1
0
Accès autorisé
```

L'en-tête `<stdbool.h>` fournit le type `bool` et les valeurs `true` (1) et `false` (0), plus lisibles qu'un `int`.

## Le piège `=` au lieu de `==`

`=` **affecte** une valeur ; `==` **compare**. Écrire `if (note = 10)` met 10 dans `note`, puis teste 10, toujours vrai. Ce code compile, mais `-Wall` le signale :

```text
egal.c:6:9: warning: suggest parentheses around assignment used as truth value [-Wparentheses]
    6 |     if (note = 10) {
      |         ^~~~
```

C'est une excellente raison de ne jamais compiler sans avertissements.

## Combiner des conditions

- `&&` (ET) : vrai si les deux conditions sont vraies ;
- `||` (OU) : vrai si au moins une est vraie ;
- `!` (NON) : inverse la condition.

Ces opérateurs sont **paresseux** (*short-circuit*) : si la première partie suffit à décider, la seconde n'est pas évaluée. On s'en sert pour protéger un calcul :

```c
#include <stdio.h>

int main(void)
{
    int total = 50;
    int nb = 0;
    if (nb != 0 && total / nb > 10) {
        printf("Moyenne élevée\n");
    } else {
        printf("Pas de moyenne calculable ou moyenne faible\n");
    }
    return 0;
}
```

```text
Pas de moyenne calculable ou moyenne faible
```

Comme `nb != 0` est faux, la division `total / nb` n'est jamais exécutée. Une **division entière par zéro** est un comportement indéfini (en pratique, le programme plante souvent).

## Choisir parmi plusieurs valeurs : `switch`

`switch` compare une valeur **entière** (ou un caractère) à des constantes :

```c
#include <stdio.h>

int main(void)
{
    char choix = 'b';
    switch (choix) {
    case 'a':
        printf("Ajouter\n");
        break;
    case 'b':
    case 'B':
        printf("Supprimer\n");
        break;
    default:
        printf("Choix inconnu\n");
    }
    return 0;
}
```

```text
Supprimer
```

- chaque `case` se termine par `break`, sinon l'exécution **continue** dans le cas suivant ;
- deux `case` consécutifs partagent le même bloc (`'b'` et `'B'`) ;
- `default` traite toutes les autres valeurs.

`switch` ne fonctionne pas avec des chaînes de caractères ni des décimaux.

## Comparer des nombres décimaux

Les `double` sont stockés de façon **approchée** : `0.1 + 0.2` ne vaut pas exactement `0.3`. Une comparaison avec `==` entre décimaux calculés est donc risquée ; on compare plutôt l'écart à une petite tolérance :

```c
#include <stdio.h>
#include <math.h>

int main(void)
{
    double a = 0.1 + 0.2;
    printf("%d\n", a == 0.3);
    printf("%d\n", fabs(a - 0.3) < 1e-9);
    return 0;
}
```

```text
0
1
```

`fabs` (de `<math.h>`) donne la valeur absolue ; `1e-9` s'écrit en notation scientifique et vaut 0,000000001. Pour des montants d'argent, une autre solution courante consiste à compter en **centimes** avec des entiers.

## L'opérateur ternaire

`condition ? valeur_si_vrai : valeur_si_faux` choisit entre deux valeurs :

```c
#include <stdio.h>

int main(void)
{
    int stock = 0;
    printf("%s\n", stock > 0 ? "En stock" : "Rupture de stock");
    return 0;
}
```

```text
Rupture de stock
```

## À retenir

- `if (…) { … } else if (…) { … } else { … }`, toujours avec accolades.
- En C, 0 est faux, toute autre valeur est vraie ; `<stdbool.h>` apporte `bool`, `true`, `false`.
- `=` affecte, `==` compare : `-Wall` vous prévient de la confusion.
- `&&` et `||` s'arrêtent dès que le résultat est connu : utile pour éviter une division par zéro.
- `switch` sur des entiers ou caractères, avec `break` à la fin de chaque `case`.

## Exercices

### Exercice 1 — Tarif

Un billet coûte 12 euros, 8 euros pour les moins de 18 ans et les plus de 65 ans. Avec `int age = 70;`, affichez le prix.

```solution-c
#include <stdio.h>

int main(void)
{
    int age = 70;
    int prix = 12;
    if (age < 18 || age > 65) {
        prix = 8;
    }
    printf("Prix : %d euros\n", prix);
    return 0;
}
```

```text
Prix : 8 euros
```

### Exercice 2 — Année bissextile

Une année est bissextile si elle est divisible par 4 mais pas par 100, ou si elle est divisible par 400. Testez 1900, 2000 et 2024.

```solution-c
#include <stdio.h>
#include <stdbool.h>

int main(void)
{
    int annees[] = {1900, 2000, 2024};
    for (int i = 0; i < 3; i++) {
        int a = annees[i];
        bool bissextile = (a % 4 == 0 && a % 100 != 0) || a % 400 == 0;
        printf("%d : %s\n", a, bissextile ? "bissextile" : "non bissextile");
    }
    return 0;
}
```

```text
1900 : non bissextile
2000 : bissextile
2024 : bissextile
```

La boucle `for` et le tableau `annees` sont présentés dans les leçons suivantes ; ils évitent ici de répéter trois fois le même test.

### Exercice 3 — Menu

Avec `int jour = 3;`, affichez `Lundi`, `Mardi` ou `Mercredi` pour 1, 2 ou 3, et `Autre jour` sinon, à l'aide d'un `switch`.

```solution-c
#include <stdio.h>

int main(void)
{
    int jour = 3;
    switch (jour) {
    case 1:
        printf("Lundi\n");
        break;
    case 2:
        printf("Mardi\n");
        break;
    case 3:
        printf("Mercredi\n");
        break;
    default:
        printf("Autre jour\n");
    }
    return 0;
}
```

```text
Mercredi
```
"""

M2_L2 = r"""
## La boucle `for`

Une **boucle** répète un bloc d'instructions. La boucle `for` convient quand on connaît le nombre de tours :

```c
#include <stdio.h>

int main(void)
{
    for (int i = 1; i <= 3; i++) {
        printf("Tour %d\n", i);
    }
    return 0;
}
```

```text
Tour 1
Tour 2
Tour 3
```

Les trois parties entre parenthèses :

1. `int i = 1` : **initialisation**, exécutée une seule fois ;
2. `i <= 3` : **condition**, testée avant chaque tour ;
3. `i++` : **incrémentation**, exécutée après chaque tour.

La variable `i`, déclarée dans le `for`, n'existe qu'à l'intérieur de la boucle.

## Accumuler un résultat

```c
#include <stdio.h>

int main(void)
{
    int total = 0;
    for (int i = 1; i <= 100; i++) {
        total += i;
    }
    printf("Somme de 1 à 100 : %d\n", total);
    return 0;
}
```

```text
Somme de 1 à 100 : 5050
```

Le schéma « variable initialisée à 0, puis ajout à chaque tour » s'appelle un **accumulateur**. Sans `= 0`, `total` partirait d'une valeur imprévisible.

## La boucle `while`

`while` répète **tant que** la condition est vraie. On l'utilise quand le nombre de tours n'est pas connu à l'avance :

```c
#include <stdio.h>

int main(void)
{
    double capital = 1000.0;
    int annees = 0;
    while (capital < 1500.0) {
        capital = capital * 1.05;
        annees++;
    }
    printf("%d ans, capital : %.2f\n", annees, capital);
    return 0;
}
```

```text
9 ans, capital : 1551.33
```

> Vérifiez qu'une boucle `while` fait **évoluer sa condition**. Sinon, c'est une **boucle infinie** : le programme ne s'arrête jamais (interrompez-le avec `Ctrl + C` dans le terminal).

## La boucle `do … while`

`do … while` teste la condition **après** le bloc : celui-ci est donc exécuté **au moins une fois**. C'est utile pour un menu ou une saisie à répéter.

```c
#include <stdio.h>

int main(void)
{
    int n = 10;
    do {
        printf("n = %d\n", n);
        n++;
    } while (n < 3);
    return 0;
}
```

```text
n = 10
```

Bien que `n < 3` soit faux dès le départ, le bloc s'exécute une fois. Notez le **point-virgule** après `while (…)`.

## `break` et `continue`

- `break` sort immédiatement de la boucle ;
- `continue` passe directement au tour suivant.

```c
#include <stdio.h>

int main(void)
{
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;   /* on saute les nombres pairs */
        }
        if (i > 7) {
            break;      /* on s'arrête après 7 */
        }
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
```

```text
1 3 5 7
```

## Boucles imbriquées

Une boucle peut en contenir une autre : pour chaque tour de la boucle extérieure, la boucle intérieure fait tous ses tours.

```c
#include <stdio.h>

int main(void)
{
    for (int ligne = 1; ligne <= 3; ligne++) {
        for (int col = 1; col <= 4; col++) {
            printf("%4d", ligne * col);
        }
        printf("\n");
    }
    return 0;
}
```

```text
   1   2   3   4
   2   4   6   8
   3   6   9  12
```

## Choisir la bonne boucle

| Situation | Boucle conseillée |
|---|---|
| nombre de tours connu (parcourir 10 éléments) | `for` |
| répéter jusqu'à un événement (capital atteint, fin de fichier) | `while` |
| exécuter au moins une fois (afficher un menu, puis demander un choix) | `do … while` |

Les trois boucles sont interchangeables en théorie : choisissez celle qui exprime le plus clairement votre intention. Une boucle volontairement infinie s'écrit `for (;;)` ou `while (1)`, avec un `break` à l'intérieur pour en sortir.

## L'erreur « décalée d'un » (*off-by-one*)

C'est l'erreur de boucle la plus fréquente : un tour de trop ou de moins.

| Boucle | Valeurs de `i` | Nombre de tours |
|---|---|---|
| `for (i = 0; i < 5; i++)` | 0, 1, 2, 3, 4 | 5 |
| `for (i = 1; i <= 5; i++)` | 1, 2, 3, 4, 5 | 5 |
| `for (i = 0; i <= 5; i++)` | 0 à 5 | **6** |

Pour parcourir N éléments numérotés à partir de 0 (le cas des tableaux, module 3), la forme standard est `for (int i = 0; i < N; i++)`. En C, un tour de trop sur un tableau ne provoque pas d'erreur claire : il lit ou écrit **hors du tableau**, ce qui est un comportement indéfini.

## Déboguer une boucle

Quand une boucle ne donne pas le résultat attendu, affichez l'état des variables à chaque tour :

```c
#include <stdio.h>

int main(void)
{
    int total = 0;
    for (int i = 1; i <= 3; i++) {
        total += i;
        printf("i = %d, total = %d\n", i, total);
    }
    return 0;
}
```

```text
i = 1, total = 1
i = 2, total = 3
i = 3, total = 6
```

Pour aller plus loin, le débogueur **gdb** permet d'exécuter un programme pas à pas et d'examiner les variables (compilez alors avec l'option `-g`).

## À retenir

- `for (int i = 0; i < n; i++)` pour un nombre de tours connu.
- `while (condition)` tant qu'une condition est vraie ; `do … while` s'exécute au moins une fois.
- `break` sort de la boucle, `continue` passe au tour suivant.
- Initialisez les accumulateurs ; vérifiez les bornes (`<` ou `<=`) pour éviter les erreurs décalées d'un.

## Exercices

### Exercice 1 — Table de multiplication

Affichez la table de 7, de `7 x 1 = 7` à `7 x 5 = 35`.

```solution-c
#include <stdio.h>

int main(void)
{
    for (int i = 1; i <= 5; i++) {
        printf("7 x %d = %d\n", i, 7 * i);
    }
    return 0;
}
```

```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
```

### Exercice 2 — Somme des chiffres

Avec une boucle `while`, calculez la somme des chiffres de 4072 (indice : `n % 10` donne le dernier chiffre, `n / 10` le retire).

```solution-c
#include <stdio.h>

int main(void)
{
    int n = 4072;
    int somme = 0;
    while (n > 0) {
        somme += n % 10;
        n /= 10;
    }
    printf("Somme des chiffres : %d\n", somme);
    return 0;
}
```

```text
Somme des chiffres : 13
```

### Exercice 3 — Triangle d'étoiles

Affichez un triangle de 4 lignes : 1 étoile, puis 2, 3 et 4.

```solution-c
#include <stdio.h>

int main(void)
{
    for (int ligne = 1; ligne <= 4; ligne++) {
        for (int k = 0; k < ligne; k++) {
            printf("*");
        }
        printf("\n");
    }
    return 0;
}
```

```text
*
**
***
****
```
"""

M2_L3 = r"""
## Pourquoi des fonctions ?

Une **fonction** regroupe des instructions sous un nom, pour les réutiliser et rendre le programme lisible. Vous en utilisez déjà : `main`, `printf`, `sqrt`.

```c
#include <stdio.h>

double prix_ttc(double prix_ht, double taux)
{
    return prix_ht * (1.0 + taux);
}

int main(void)
{
    printf("%.2f\n", prix_ttc(100.0, 0.20));
    printf("%.2f\n", prix_ttc(50.0, 0.055));
    return 0;
}
```

```text
120.00
52.75
```

Une définition de fonction indique :

- le **type de retour** (`double`) : le type de la valeur renvoyée par `return` ;
- le **nom** (`prix_ttc`) ;
- les **paramètres**, chacun avec son type (`double prix_ht, double taux`) ;
- le **corps**, entre accolades.

Une fonction qui ne renvoie rien a le type de retour `void`. Une fonction sans paramètre s'écrit `f(void)`.

## Déclarer avant d'utiliser : le prototype

Le compilateur lit le fichier de haut en bas : une fonction doit être **connue** avant d'être appelée. Si on préfère écrire `main` en premier, on place avant elle un **prototype** (la première ligne de la fonction suivie d'un point-virgule) :

```c
#include <stdio.h>

void afficher_ligne(int longueur);   /* prototype */

int main(void)
{
    afficher_ligne(5);
    afficher_ligne(10);
    return 0;
}

void afficher_ligne(int longueur)
{
    for (int i = 0; i < longueur; i++) {
        printf("-");
    }
    printf("\n");
}
```

```text
-----
----------
```

## Le passage par valeur

En C, les arguments sont **copiés** dans les paramètres. Modifier un paramètre ne modifie donc **pas** la variable de l'appelant :

```c
#include <stdio.h>

void doubler(int x)
{
    x = x * 2;
    printf("Dans la fonction : %d\n", x);
}

int main(void)
{
    int n = 5;
    doubler(n);
    printf("Après l'appel : %d\n", n);
    return 0;
}
```

```text
Dans la fonction : 10
Après l'appel : 5
```

Deux solutions : **renvoyer** la nouvelle valeur (`n = doubler(n);` avec une fonction qui fait `return x * 2;`), ou transmettre l'**adresse** de la variable grâce à un pointeur. C'est l'objet du module 3, et c'est ce que fait `scanf("%d", &age)`.

## Portée des variables

Une variable déclarée dans une fonction (ou dans un bloc `{ }`) est **locale** : elle n'existe que pendant l'exécution de ce bloc et disparaît ensuite. Deux fonctions peuvent donc avoir chacune leur variable `i` sans conflit.

Une variable déclarée en dehors de toute fonction est **globale** : visible partout dans le fichier. Évitez-les autant que possible : n'importe quelle fonction peut les modifier, ce qui rend les bogues difficiles à trouver.

Le mot-clé `static` devant une variable locale la fait **survivre** entre deux appels :

```c
#include <stdio.h>

int prochain_numero(void)
{
    static int compteur = 0;   /* initialisée une seule fois */
    compteur++;
    return compteur;
}

int main(void)
{
    printf("%d\n", prochain_numero());
    printf("%d\n", prochain_numero());
    printf("%d\n", prochain_numero());
    return 0;
}
```

```text
1
2
3
```

> Une fonction ne doit **jamais renvoyer l'adresse d'une de ses variables locales** (non `static`) : la variable n'existe plus après le `return`, et l'utiliser est un comportement indéfini. Nous y reviendrons avec les pointeurs.

## La récursivité

Une fonction **récursive** s'appelle elle-même. Il lui faut un **cas de base** qui arrête les appels :

```c
#include <stdio.h>

unsigned long long factorielle(unsigned int n)
{
    if (n <= 1) {
        return 1;                       /* cas de base */
    }
    return n * factorielle(n - 1);      /* appel récursif */
}

int main(void)
{
    printf("5! = %llu\n", factorielle(5));
    printf("20! = %llu\n", factorielle(20));
    return 0;
}
```

```text
5! = 120
20! = 2432902008176640000
```

`%llu` affiche un `unsigned long long`. 21! dépasse la capacité de ce type (64 bits) : le résultat serait faux. Sans cas de base, les appels s'empilent jusqu'à épuiser la **pile** (*stack overflow*) et le programme plante.

## Organiser un programme en plusieurs fichiers

Pour un projet plus grand, on range les fonctions dans plusieurs fichiers. On sépare :

- un **fichier d'en-tête** `calcul.h`, qui contient les prototypes ;
- un **fichier source** `calcul.c`, qui contient les définitions ;
- le programme principal `main.c`, qui inclut l'en-tête.

```h
/* calcul.h */
#ifndef CALCUL_H
#define CALCUL_H

int carre(int x);

#endif
```

```c
/* calcul.c */
#include "calcul.h"

int carre(int x)
{
    return x * x;
}
```

```c
/* main.c */
#include <stdio.h>
#include "calcul.h"

int main(void)
{
    printf("%d\n", carre(7));
    return 0;
}
```

```bash
gcc -std=c17 -Wall -Wextra -o programme main.c calcul.c
./programme
```

Les guillemets `"calcul.h"` désignent un en-tête de votre projet, les chevrons `<stdio.h>` un en-tête du système. Les lignes `#ifndef … #define … #endif` (*include guard*) empêchent d'inclure deux fois le même en-tête. Le programme affiche `49`.

## À retenir

- `type_retour nom(type param, …) { … return valeur; }` ; `void` si rien n'est renvoyé.
- Une fonction doit être déclarée avant d'être appelée : sinon, ajoutez un **prototype**.
- Les arguments sont **copiés** : modifier un paramètre ne change pas la variable de l'appelant.
- Variables locales de préférence ; `static` conserve une valeur entre deux appels.
- Une fonction récursive a toujours un cas de base.
- Projet en plusieurs fichiers : prototypes dans le `.h`, définitions dans le `.c`.

## Exercices

### Exercice 1 — Maximum

Écrivez une fonction `int max2(int a, int b)` qui renvoie le plus grand des deux nombres, et testez-la avec (3, 8) et (12, 5).

```solution-c
#include <stdio.h>

int max2(int a, int b)
{
    return a > b ? a : b;
}

int main(void)
{
    printf("%d\n", max2(3, 8));
    printf("%d\n", max2(12, 5));
    return 0;
}
```

```text
8
12
```

### Exercice 2 — Nombre premier

Écrivez `bool est_premier(int n)` (vrai si `n` n'a que deux diviseurs, 1 et lui-même) et affichez les nombres premiers inférieurs à 30.

```solution-c
#include <stdio.h>
#include <stdbool.h>

bool est_premier(int n)
{
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

int main(void)
{
    for (int i = 1; i < 30; i++) {
        if (est_premier(i)) {
            printf("%d ", i);
        }
    }
    printf("\n");
    return 0;
}
```

```text
2 3 5 7 11 13 17 19 23 29
```

Il suffit de tester les diviseurs jusqu'à la racine carrée de `n` (`d * d <= n`).

### Exercice 3 — Puissance récursive

Écrivez une fonction récursive `long long puissance(int base, int exposant)` (exposant positif ou nul) et calculez 2 puissance 10 et 3 puissance 4.

```solution-c
#include <stdio.h>

long long puissance(int base, int exposant)
{
    if (exposant == 0) {
        return 1;
    }
    return base * puissance(base, exposant - 1);
}

int main(void)
{
    printf("%lld\n", puissance(2, 10));
    printf("%lld\n", puissance(3, 4));
    return 0;
}
```

```text
1024
81
```
"""

QUIZ_M1 = [
    ("single", "Que produit la commande gcc -std=c17 -Wall -o bonjour bonjour.c ?", None,
     ["Elle exécute directement bonjour.c", "Elle compile bonjour.c en un exécutable nommé bonjour", "Elle crée le fichier bonjour.c", "Elle affiche le code source"], [1],
     "gcc compile le fichier source ; l'option -o fixe le nom de l'exécutable produit, qu'on lance ensuite avec ./bonjour."),
    ("single", "Par quelle fonction commence l'exécution d'un programme C ?", None,
     ["start", "printf", "main", "init"], [2],
     "L'exécution commence toujours par la fonction main, quel que soit l'ordre des fonctions dans le fichier."),
    ("single", "Que vaut l'expression 7 / 2 lorsque 7 et 2 sont des int ?", None,
     ["3.5", "3", "4", "1"], [1],
     "Entre deux entiers, / effectue une division entière : la partie décimale est perdue, le résultat vaut 3."),
    ("single", "Quel indicateur de format affiche un double avec deux décimales ?", None,
     ["%d", "%2d", "%lf2", "%.2f"], [3],
     "%f affiche un double ; la précision .2 limite l'affichage à deux décimales."),
    ("single", "Qu'affiche ce programme ?", "#include <stdio.h>\n\nint main(void)\n{\n    char c = 'A';\n    printf(\"%c\\n\", c + 2);\n    return 0;\n}",
     ["A2", "C", "67", "B"], [1],
     "Un char est un nombre : 'A' vaut 65, 'A' + 2 vaut 67, que %c affiche comme le caractère C."),
    ("multiple", "Quelles affirmations sur sizeof sont exactes ?", None,
     ["sizeof(char) vaut toujours 1", "sizeof(int) vaut 4 sur toutes les machines", "Le résultat de sizeof s'affiche avec %zu", "sizeof donne une taille en octets"], [0, 2, 3],
     "Seule la taille de char est fixée par la norme ; celle d'un int dépend de la plateforme (souvent 4 octets). sizeof renvoie un size_t, exprimé en octets, affiché avec %zu."),
    ("single", "Que renvoie scanf(\"%d\", &age) si l'utilisateur tape « abc » ?", None,
     ["0, et age n'est pas modifié", "1", "La valeur 0 est placée dans age", "Le programme s'arrête avec une erreur de compilation"], [0],
     "scanf renvoie le nombre de valeurs lues avec succès : ici aucune. age garde sa valeur précédente, d'où l'importance de tester ce retour."),
    ("true_false", "Dépasser la valeur maximale d'un int signé (INT_MAX + 1) est un comportement indéfini en C.", None,
     ["Vrai", "Faux"], [0],
     "Le dépassement d'un entier signé est un comportement indéfini : la norme n'impose aucun résultat. Seuls les types non signés « font le tour » de façon définie."),
    ("single", "Pourquoi compiler avec -Wall -Wextra ?", None,
     ["Pour rendre le programme plus rapide", "Pour activer des avertissements qui signalent des erreurs probables", "Pour inclure automatiquement stdio.h", "Pour produire un exécutable Windows"], [1],
     "Ces options activent les principaux avertissements : ils repèrent des bogues fréquents (confusion = / ==, format printf incorrect, variable non initialisée…)."),
    ("single", "Quel format faut-il utiliser pour lire un double avec scanf ?", None,
     ["%f", "%d", "%lf", "%lld"], [2],
     "Pour la lecture, scanf distingue float (%f) et double (%lf). printf, lui, affiche un double avec %f."),
]

QUIZ_M2 = [
    ("single", "Qu'affiche ce programme ?", "#include <stdio.h>\n\nint main(void)\n{\n    int x = 0;\n    if (x) {\n        printf(\"oui\\n\");\n    } else {\n        printf(\"non\\n\");\n    }\n    return 0;\n}",
     ["oui", "non", "0", "Rien"], [1],
     "En C, 0 est faux et toute autre valeur est vraie : la condition est fausse, le bloc else s'exécute."),
    ("single", "Quel est le problème de if (note = 10) ?", None,
     ["Aucun, c'est une comparaison", "Il affecte 10 à note, et la condition est toujours vraie", "Il provoque une erreur de compilation", "Il compare l'adresse de note à 10"], [1],
     "Un seul = affecte la valeur : note prend la valeur 10, qui est non nulle donc vraie. Il faut écrire ==. -Wall le signale."),
    ("single", "Combien de fois ce code affiche-t-il un message ?", "for (int i = 0; i <= 5; i++) {\n    printf(\"x\\n\");\n}",
     ["6", "5", "4", "Une infinité"], [0],
     "i prend les valeurs 0, 1, 2, 3, 4 et 5 : six tours. C'est un exemple d'erreur « décalée d'un » si l'on voulait 5 tours."),
    ("single", "Quelle boucle exécute son bloc au moins une fois ?", None,
     ["for", "while", "Aucune", "do … while"], [3],
     "do … while teste la condition après le bloc : celui-ci s'exécute donc toujours une première fois."),
    ("single", "Dans un switch, que se passe-t-il si l'on oublie break à la fin d'un case ?", None,
     ["L'exécution continue dans le case suivant", "Une erreur de compilation", "Le switch recommence", "Le default est exécuté immédiatement"], [0],
     "Sans break, l'exécution « tombe » dans le cas suivant. C'est voulu seulement quand plusieurs cas partagent un même bloc."),
    ("single", "Qu'affiche ce programme ?", "#include <stdio.h>\n\nvoid ajouter_un(int n)\n{\n    n = n + 1;\n}\n\nint main(void)\n{\n    int a = 4;\n    ajouter_un(a);\n    printf(\"%d\\n\", a);\n    return 0;\n}",
     ["5", "4", "0", "Un comportement indéfini"], [1],
     "Les arguments sont passés par valeur : la fonction modifie une copie, a vaut toujours 4."),
    ("multiple", "Quelles affirmations sur les fonctions sont exactes ?", None,
     ["Une fonction qui ne renvoie rien a le type de retour void", "Un prototype permet d'appeler une fonction définie plus bas dans le fichier", "Une fonction récursive a besoin d'un cas de base", "Une fonction peut renvoyer sans risque l'adresse de sa variable locale"], [0, 1, 2],
     "Une variable locale disparaît à la fin de la fonction : utiliser son adresse ensuite est un comportement indéfini. Les trois autres affirmations sont exactes."),
    ("single", "Que permet le mot-clé static devant une variable locale ?", None,
     ["De la rendre constante", "De la rendre visible dans tous les fichiers", "De l'allouer dans le tas", "De conserver sa valeur entre deux appels de la fonction"], [3],
     "Une variable locale static est initialisée une seule fois et survit entre les appels, tout en restant visible seulement dans la fonction."),
    ("true_false", "Dans if (b != 0 && a / b > 2), la division n'est pas effectuée lorsque b vaut 0.", None,
     ["Vrai", "Faux"], [0],
     "&& est évalué de gauche à droite et s'arrête dès que la première partie est fausse : la division par zéro est évitée."),
    ("single", "Que contient habituellement un fichier d'en-tête .h ?", None,
     ["Le code de la fonction main", "Le programme compilé", "Les prototypes des fonctions et des définitions partagées", "Les options de compilation"], [2],
     "Le .h déclare ce qu'un module offre (prototypes, constantes, types) ; les définitions sont dans le .c correspondant."),
]

MODULES = [
    {
        "position": 1,
        "title": "Compilation et bases",
        "description": "Compiler avec gcc, comprendre les types, les opérateurs, printf et la saisie.",
        "status": "published",
        "lessons": [
            ("premier-programme-c", "Premier programme et compilation",
             "Le rôle du C, gcc, les étapes de compilation, erreurs et avertissements.", M1_L1, 35),
            ("variables-et-types", "Variables et types",
             "int, double, char, sizeof, division entière, constantes et dépassements.", M1_L2, 40),
            ("operateurs-printf-scanf", "Opérateurs, affichage et saisie",
             "Priorités, formats de printf, math.h, scanf et sscanf.", M1_L3, 40),
        ],
        "quiz": ("Quiz — Compilation et bases", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Contrôle et fonctions",
        "description": "Conditions, boucles et fonctions pour structurer un programme C.",
        "status": "published",
        "lessons": [
            ("conditions-c", "Les conditions",
             "if, else, opérateurs logiques, switch et ternaire.", M2_L1, 40),
            ("boucles-c", "Les boucles",
             "for, while, do … while, break, continue et erreurs décalées d'un.", M2_L2, 40),
            ("fonctions-c", "Les fonctions",
             "Paramètres, retour, prototypes, portée, récursivité et fichiers d'en-tête.", M2_L3, 45),
        ],
        "quiz": ("Quiz — Contrôle et fonctions", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Tableaux, chaînes et pointeurs",
        "description": "Ranger des séries de valeurs, manipuler du texte et comprendre les adresses mémoire.",
        "status": "published",
        "lessons": [
            ("tableaux-c", "Les tableaux",
             "Déclarer, parcourir, passer à une fonction ; dépassements et tableaux 2D.", _m35.M3_L1, 45),
            ("pointeurs", "Les pointeurs",
             "Adresses, déréférencement, passage par adresse et arithmétique des pointeurs.", _m35.M3_L2, 45),
            ("chaines-c", "Les chaînes de caractères",
             "Le caractère nul, string.h, copies sûres et lecture avec fgets.", _m35.M3_L3, 45),
        ],
        "quiz": ("Quiz — Tableaux, chaînes et pointeurs", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Mémoire dynamique et structures",
        "description": "Allouer et libérer la mémoire, regrouper des données et traquer les erreurs mémoire.",
        "status": "published",
        "lessons": [
            ("memoire-dynamique", "Allocation dynamique",
             "Pile et tas, malloc, calloc, realloc et free ; fuites et pointeurs pendants.", _m35.M4_L1, 45),
            ("structures", "Les structures",
             "struct, typedef, accès avec . et ->, tableaux de structures, enum.", _m35.M4_L2, 45),
            ("surete-memoire", "Sûreté mémoire et outils",
             "Comportements indéfinis, sanitizers, Valgrind et tableau dynamique.", _m35.M4_L3, 45),
        ],
        "quiz": ("Quiz — Mémoire dynamique et structures", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Fichiers et mini-projet",
        "description": "Lire et écrire des fichiers, gérer les erreurs, puis réaliser un programme complet.",
        "status": "published",
        "lessons": [
            ("fichiers-texte", "Fichiers texte",
             "fopen, fprintf, fgets, fclose et gestion des erreurs.", _m35.M5_L1, 40),
            ("fichiers-donnees", "Analyser et enregistrer des données",
             "Lire un fichier ligne par ligne, sscanf, strtol et fichiers binaires.", _m35.M5_L2, 45),
            ("mini-projet-c", "Mini-projet : gestionnaire d'inventaire",
             "Structures, tableau dynamique, fichiers et libération de la mémoire.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Fichiers et mini-projet", _m35.QUIZ_M5),
    },
]
