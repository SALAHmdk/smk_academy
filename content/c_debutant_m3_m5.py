"""Modules 3 à 5 de « Langage C » (importé par content/c_debutant.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Tableaux, chaînes et pointeurs
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Ranger plusieurs valeurs : le tableau

Un **tableau** est une suite de valeurs du **même type**, rangées les unes à la suite des autres en mémoire. Sa taille est fixée à la déclaration.

```c
#include <stdio.h>

int main(void)
{
    int notes[5] = {12, 8, 15, 19, 10};

    printf("Première note : %d\n", notes[0]);
    printf("Dernière note : %d\n", notes[4]);
    notes[1] = 9;   /* modification de la deuxième case */
    printf("Deuxième note corrigée : %d\n", notes[1]);
    return 0;
}
```

```text
Première note : 12
Dernière note : 10
Deuxième note corrigée : 9
```

- les cases sont numérotées **à partir de 0** : un tableau de 5 cases va de `notes[0]` à `notes[4]` ;
- le numéro entre crochets s'appelle l'**indice** (*index*).

Si l'on fournit moins de valeurs que de cases, les cases restantes valent 0. `int compteurs[26] = {0};` crée ainsi 26 compteurs à zéro. En revanche, un tableau local déclaré **sans** initialisation (`int t[5];`) contient des valeurs imprévisibles.

## Parcourir un tableau

On parcourt un tableau avec une boucle `for` dont l'indice va de 0 à la taille moins 1. Pour connaître le nombre de cases, on divise la taille totale du tableau par celle d'une case :

```c
#include <stdio.h>

int main(void)
{
    int notes[] = {12, 8, 15, 19, 10, 6};
    size_t n = sizeof notes / sizeof notes[0];
    int somme = 0;
    int meilleure = notes[0];

    for (size_t i = 0; i < n; i++) {
        somme += notes[i];
        if (notes[i] > meilleure) {
            meilleure = notes[i];
        }
    }
    printf("%zu notes, moyenne %.2f, meilleure %d\n", n, (double) somme / n, meilleure);
    return 0;
}
```

```text
6 notes, moyenne 11.67, meilleure 19
```

Avec `int notes[] = {…}`, le compilateur compte lui-même les cases. Le type `size_t` est le type naturel d'une taille ou d'un indice (entier non signé, affiché avec `%zu`).

## Le danger n°1 : sortir du tableau

Le C **ne vérifie pas** les indices. Écrire `notes[6]` dans un tableau de 6 cases ne provoque aucune erreur de compilation : le programme lit ou écrit dans la mémoire **située après** le tableau, qui appartient peut-être à une autre variable. C'est un **comportement indéfini** : le programme peut sembler marcher, corrompre silencieusement d'autres données ou planter.

Ces **dépassements de tampon** (*buffer overflows*) sont historiquement l'une des principales causes de failles de sécurité : un attaquant qui contrôle les données écrites hors du tableau peut parfois prendre le contrôle du programme.

> Règles de sûreté : boucle `i < n` (jamais `i <= n`), indice toujours vérifié avant usage s'il vient de l'extérieur (saisie, fichier), et taille du tableau toujours transmise avec lui. Au module 4, vous verrez des outils (*sanitizers*) qui détectent ces erreurs à l'exécution.

## Passer un tableau à une fonction

Quand on passe un tableau à une fonction, celle-ci ne reçoit **que l'adresse de sa première case**, pas une copie, et elle ne connaît **pas sa taille**. Il faut donc toujours transmettre la taille en paramètre :

```c
#include <stdio.h>

void afficher(const int t[], size_t n)
{
    for (size_t i = 0; i < n; i++) {
        printf("%d ", t[i]);
    }
    printf("\n");
}

void doubler_tout(int t[], size_t n)
{
    for (size_t i = 0; i < n; i++) {
        t[i] *= 2;
    }
}

int main(void)
{
    int valeurs[] = {1, 2, 3, 4};
    size_t n = sizeof valeurs / sizeof valeurs[0];
    afficher(valeurs, n);
    doubler_tout(valeurs, n);
    afficher(valeurs, n);
    return 0;
}
```

```text
1 2 3 4
2 4 6 8
```

Deux remarques importantes :

- contrairement aux variables simples, la fonction **modifie le tableau d'origine** : elle travaille sur la même mémoire ;
- `const` dans `afficher` promet que la fonction ne modifiera pas le tableau ; le compilateur refusera toute écriture. Utilisez-le pour toute fonction en lecture seule.

Dans une fonction, `sizeof t` ne donne **pas** la taille du tableau mais celle d'une adresse (gcc vous avertit d'ailleurs avec `-Wall`) : l'astuce `sizeof t / sizeof t[0]` ne fonctionne qu'à l'endroit où le tableau est déclaré.

## Rechercher dans un tableau

Une **recherche linéaire** parcourt le tableau jusqu'à trouver la valeur. Par convention, on renvoie l'indice trouvé, ou -1 si la valeur est absente :

```c
#include <stdio.h>

int chercher(const int t[], int n, int valeur)
{
    for (int i = 0; i < n; i++) {
        if (t[i] == valeur) {
            return i;
        }
    }
    return -1;
}

int main(void)
{
    int codes[] = {40, 12, 77, 5};
    printf("77 est à l'indice %d\n", chercher(codes, 4, 77));
    printf("99 est à l'indice %d\n", chercher(codes, 4, 99));
    return 0;
}
```

```text
77 est à l'indice 2
99 est à l'indice -1
```

## Les tableaux à deux dimensions

Un tableau peut avoir plusieurs dimensions, par exemple des lignes et des colonnes :

```c
#include <stdio.h>

int main(void)
{
    int ventes[2][3] = {
        {10, 20, 30},
        {5, 15, 25},
    };
    for (int magasin = 0; magasin < 2; magasin++) {
        int total = 0;
        for (int mois = 0; mois < 3; mois++) {
            total += ventes[magasin][mois];
        }
        printf("Magasin %d : %d ventes\n", magasin + 1, total);
    }
    return 0;
}
```

```text
Magasin 1 : 60 ventes
Magasin 2 : 45 ventes
```

`ventes[1][2]` désigne la ligne 1, colonne 2 (en comptant à partir de 0), soit 25. En mémoire, les lignes sont rangées les unes après les autres.

## À retenir

- `int t[5]` : 5 cases, de `t[0]` à `t[4]` ; `{0}` initialise tout à zéro.
- Nombre de cases : `sizeof t / sizeof t[0]`, uniquement là où le tableau est déclaré.
- Le C ne vérifie pas les indices : sortir du tableau est un **comportement indéfini**, source de failles.
- Une fonction reçoit l'adresse du tableau : passez toujours la **taille**, et `const` si elle ne modifie rien.
- Recherche linéaire : renvoyer l'indice, ou -1 si absent.

## Exercices

### Exercice 1 — Inverser un tableau

Écrivez `void inverser(int t[], size_t n)` qui inverse l'ordre des éléments sur place, et testez-la sur `{1, 2, 3, 4, 5}`.

```solution-c
#include <stdio.h>

void inverser(int t[], size_t n)
{
    for (size_t i = 0; i < n / 2; i++) {
        int tmp = t[i];
        t[i] = t[n - 1 - i];
        t[n - 1 - i] = tmp;
    }
}

int main(void)
{
    int t[] = {1, 2, 3, 4, 5};
    size_t n = sizeof t / sizeof t[0];
    inverser(t, n);
    for (size_t i = 0; i < n; i++) {
        printf("%d ", t[i]);
    }
    printf("\n");
    return 0;
}
```

```text
5 4 3 2 1
```

On échange la première et la dernière case, puis la deuxième et l'avant-dernière, etc. : `n / 2` échanges suffisent.

### Exercice 2 — Au-dessus de la moyenne

Avec les températures `{18, 22, 25, 19, 30, 27}`, affichez la moyenne puis le nombre de valeurs strictement supérieures à cette moyenne.

```solution-c
#include <stdio.h>

int main(void)
{
    int temp[] = {18, 22, 25, 19, 30, 27};
    size_t n = sizeof temp / sizeof temp[0];
    int somme = 0;
    for (size_t i = 0; i < n; i++) {
        somme += temp[i];
    }
    double moyenne = (double) somme / n;
    int au_dessus = 0;
    for (size_t i = 0; i < n; i++) {
        if (temp[i] > moyenne) {
            au_dessus++;
        }
    }
    printf("Moyenne : %.2f\n", moyenne);
    printf("Au-dessus : %d\n", au_dessus);
    return 0;
}
```

```text
Moyenne : 23.50
Au-dessus : 3
```

### Exercice 3 — Trouvez le bogue

Ce code doit additionner les 4 cases du tableau. Quel est le problème ?

```text
int t[4] = {1, 2, 3, 4};
int somme = 0;
for (int i = 1; i <= 4; i++) {
    somme += t[i];
}
```

```solution-text
Les indices vont de 0 à 3. La boucle commence à 1 (elle oublie t[0]) et va jusqu'à 4 :
t[4] est hors du tableau, ce qui est un comportement indéfini.
Correction : for (int i = 0; i < 4; i++)
```
"""

M3_L2 = r"""
## La mémoire et les adresses

La mémoire de l'ordinateur est une immense suite d'**octets**, chacun repéré par un numéro : son **adresse**. Chaque variable occupe un ou plusieurs octets consécutifs ; son adresse est celle de son premier octet.

L'opérateur `&` donne l'adresse d'une variable. On l'affiche avec `%p`, après une conversion en `void *` (le type « adresse de n'importe quoi ») :

```c
#include <stdio.h>

int main(void)
{
    int age = 25;
    printf("Valeur : %d\n", age);
    printf("Adresse : %p\n", (void *) &age);
    printf("Taille : %zu octets\n", sizeof age);
    return 0;
}
```

Exemple d'affichage (les adresses changent d'une machine et d'une exécution à l'autre) :

```text
Valeur : 25
Adresse : 0x7ffd5e8a3b4c
Taille : 4 octets
```

## Qu'est-ce qu'un pointeur ?

Un **pointeur** est une variable qui contient une **adresse**. Son type indique ce qui se trouve à cette adresse : `int *` est un « pointeur vers un `int` ».

```c
#include <stdio.h>

int main(void)
{
    int age = 25;
    int *p = &age;      /* p contient l'adresse de age */

    printf("*p vaut %d\n", *p);
    *p = 30;            /* on écrit à l'adresse contenue dans p */
    printf("age vaut maintenant %d\n", age);
    return 0;
}
```

```text
*p vaut 25
age vaut maintenant 30
```

| Écriture | Signification |
|---|---|
| `int *p;` | déclare un pointeur vers un `int` |
| `p = &age;` | `p` reçoit l'adresse de `age` |
| `*p` | la valeur **pointée** (on dit qu'on **déréférence** `p`) |
| `*p = 30;` | modifie la variable pointée |

Le symbole `*` a donc deux rôles : dans une **déclaration**, il indique un type pointeur ; dans une **expression**, il accède à la valeur pointée.

## Le pointeur nul et les pointeurs non initialisés

Un pointeur qui ne pointe sur rien de valide doit valoir **`NULL`** (défini notamment dans `<stdio.h>` et `<stdlib.h>`). Avant de déréférencer un pointeur qui peut être nul, on le teste :

```c
#include <stdio.h>

void afficher_valeur(const int *p)
{
    if (p == NULL) {
        printf("Aucune valeur\n");
        return;
    }
    printf("Valeur : %d\n", *p);
}

int main(void)
{
    int x = 7;
    afficher_valeur(&x);
    afficher_valeur(NULL);
    return 0;
}
```

```text
Valeur : 7
Aucune valeur
```

> Trois erreurs graves, toutes des **comportements indéfinis** : déréférencer `NULL` (en pratique, le programme plante souvent avec une *segmentation fault*), utiliser un pointeur **non initialisé** (`int *p; *p = 3;` écrit à une adresse aléatoire), et utiliser l'adresse d'une variable qui **n'existe plus** (variable locale d'une fonction terminée). Initialisez toujours un pointeur : avec une adresse valide ou avec `NULL`.

## Modifier une variable depuis une fonction

Au module 2, une fonction ne pouvait pas modifier la variable de l'appelant, car elle en recevait une copie. En lui passant l'**adresse** de la variable, elle le peut : c'est le **passage par adresse**.

```c
#include <stdio.h>

void echanger(int *a, int *b)
{
    int tmp = *a;
    *a = *b;
    *b = tmp;
}

int main(void)
{
    int x = 3, y = 8;
    echanger(&x, &y);
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
```

```text
x = 8, y = 3
```

C'est exactement ce que fait `scanf("%d", &age)` : il reçoit l'adresse de `age` pour pouvoir y écrire.

Le passage par adresse sert aussi à **renvoyer plusieurs résultats**. La valeur de retour indique souvent si l'opération a réussi, et les résultats sont écrits via des pointeurs :

```c
#include <stdio.h>
#include <stdbool.h>

bool diviser(int a, int b, int *quotient, int *reste)
{
    if (b == 0) {
        return false;
    }
    *quotient = a / b;
    *reste = a % b;
    return true;
}

int main(void)
{
    int q = 0, r = 0;
    if (diviser(17, 5, &q, &r)) {
        printf("17 = 5 x %d + %d\n", q, r);
    }
    if (!diviser(4, 0, &q, &r)) {
        printf("Division par zéro refusée\n");
    }
    return 0;
}
```

```text
17 = 5 x 3 + 2
Division par zéro refusée
```

## Pointeurs et tableaux

Le nom d'un tableau, utilisé dans une expression, est converti en **l'adresse de sa première case** : `t` équivaut à `&t[0]`. On peut alors **ajouter un entier** à un pointeur : `p + 1` désigne la case **suivante** (le compilateur avance de `sizeof(int)` octets pour un `int *`, pas d'un seul octet).

```c
#include <stdio.h>

int main(void)
{
    int t[] = {10, 20, 30, 40};
    int *p = t;          /* équivaut à &t[0] */

    printf("%d\n", *p);
    printf("%d\n", *(p + 2));
    printf("%d\n", p[3]);
    p++;
    printf("%d\n", *p);
    return 0;
}
```

```text
10
30
40
20
```

`t[i]` et `*(t + i)` sont strictement équivalents : la notation avec crochets n'est qu'une écriture plus lisible. C'est pourquoi une fonction qui reçoit un tableau peut s'écrire indifféremment `void f(int t[], size_t n)` ou `void f(int *t, size_t n)`.

L'arithmétique des pointeurs n'est valable **qu'à l'intérieur d'un même tableau** (ou juste après sa dernière case, sans la déréférencer). Calculer ou lire une adresse au-delà est un comportement indéfini, comme un indice hors limites.

## `const` et pointeurs

`const int *p` signifie « pointeur vers un `int` qu'on ne modifiera pas par ce pointeur ». C'est la façon idiomatique de dire qu'une fonction **lit** une donnée sans la modifier, comme `afficher_valeur` plus haut. Le compilateur refuse alors `*p = 5;`.

## À retenir

- `&x` donne l'adresse de `x` ; un pointeur `int *p` contient une adresse ; `*p` est la valeur pointée.
- Initialisez toujours un pointeur (adresse valide ou `NULL`) et testez `NULL` avant de déréférencer.
- Passer `&x` à une fonction lui permet de modifier `x` ou de renvoyer plusieurs résultats.
- `t[i]` équivaut à `*(t + i)` ; `p + 1` avance d'un élément, pas d'un octet.
- Restez dans les limites du tableau ; `const` pour les données en lecture seule.

## Exercices

### Exercice 1 — Prédire l'affichage

Qu'affiche ce programme ?

```solution-c
#include <stdio.h>

int main(void)
{
    int a = 5;
    int b = 10;
    int *p = &a;
    *p = *p + 1;
    p = &b;
    *p = *p * 2;
    printf("a = %d, b = %d\n", a, b);
    return 0;
}
```

```text
a = 6, b = 20
```

`p` pointe d'abord sur `a` (qui passe à 6), puis sur `b` (qui passe à 20).

### Exercice 2 — Minimum et maximum

Écrivez `void min_max(const int *t, size_t n, int *min, int *max)` (avec `n` au moins égal à 1) et testez-la sur `{7, 2, 9, 4}`.

```solution-c
#include <stdio.h>

void min_max(const int *t, size_t n, int *min, int *max)
{
    *min = t[0];
    *max = t[0];
    for (size_t i = 1; i < n; i++) {
        if (t[i] < *min) {
            *min = t[i];
        }
        if (t[i] > *max) {
            *max = t[i];
        }
    }
}

int main(void)
{
    int t[] = {7, 2, 9, 4};
    int mini = 0, maxi = 0;
    min_max(t, 4, &mini, &maxi);
    printf("min = %d, max = %d\n", mini, maxi);
    return 0;
}
```

```text
min = 2, max = 9
```

### Exercice 3 — Somme avec un pointeur

Calculez la somme du tableau `{3, 6, 9, 12}` en le parcourant **uniquement avec un pointeur** (sans crochets).

```solution-c
#include <stdio.h>

int main(void)
{
    int t[] = {3, 6, 9, 12};
    int somme = 0;
    for (const int *p = t; p < t + 4; p++) {
        somme += *p;
    }
    printf("Somme : %d\n", somme);
    return 0;
}
```

```text
Somme : 30
```

`t + 4` est l'adresse juste après la dernière case : on a le droit de la calculer et de la comparer, mais pas de la déréférencer.
"""

M3_L3 = r"""
## Une chaîne, c'est un tableau de `char`

Le C n'a pas de type « chaîne » à proprement parler. Une **chaîne de caractères** est un tableau de `char` terminé par le **caractère nul** `'\0'` (l'octet de valeur 0), qui marque la fin du texte.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char mot[] = "Bonjour";
    printf("Texte : %s\n", mot);
    printf("strlen : %zu\n", strlen(mot));
    printf("sizeof : %zu\n", sizeof mot);
    return 0;
}
```

```text
Texte : Bonjour
strlen : 7
sizeof : 8
```

`strlen` compte les caractères **avant** le `'\0'` ; le tableau, lui, occupe une case de plus pour stocker ce `'\0'`. Retenez-le : **une chaîne de N caractères a besoin de N + 1 octets**.

Toutes les fonctions de chaînes parcourent la mémoire **jusqu'au `'\0'`**. Une chaîne sans `'\0'` les fait lire au-delà du tableau : comportement indéfini.

## Parcourir une chaîne

```c
#include <stdio.h>

int main(void)
{
    const char *texte = "langage C";
    int espaces = 0;
    for (int i = 0; texte[i] != '\0'; i++) {
        if (texte[i] == ' ') {
            espaces++;
        }
    }
    printf("%d espace(s)\n", espaces);
    return 0;
}
```

```text
1 espace(s)
```

## Littéraux et tableaux modifiables

- `char mot[] = "Bonjour";` crée un **tableau** initialisé avec une copie du texte : on peut le modifier (`mot[0] = 'b';`).
- `const char *texte = "langage C";` crée un **pointeur** vers un texte constant, stocké dans une zone en lecture seule. Le modifier est un comportement indéfini : déclarez ces pointeurs `const`, le compilateur vous protégera.

## Les fonctions de `<string.h>`

| Fonction | Rôle |
|---|---|
| `strlen(s)` | longueur (sans le `'\0'`) |
| `strcmp(a, b)` | compare : 0 si égales, négatif si `a` avant `b`, positif sinon |
| `strcpy(dest, src)` | copie `src` dans `dest` (**sans vérifier la place**) |
| `strcat(dest, src)` | ajoute `src` à la fin de `dest` (**sans vérifier la place**) |
| `strchr(s, c)` | adresse de la première occurrence de `c`, ou `NULL` |
| `strstr(s, motif)` | adresse de la première occurrence de `motif`, ou `NULL` |

**Comparer deux chaînes** : `a == b` compare deux **adresses**, pas les textes ! Utilisez `strcmp` :

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char saisie[] = "admin";
    if (strcmp(saisie, "admin") == 0) {
        printf("Identiques\n");
    }
    printf("%d\n", strcmp("abricot", "banane") < 0);
    return 0;
}
```

```text
Identiques
1
```

## Copier sans déborder

`strcpy` et `strcat` écrivent sans vérifier la taille du tableau de destination : si le texte est trop long, ils débordent. C'est la cause de nombreuses failles. Préférez **`snprintf`**, qui reçoit la taille de la destination, **coupe** si nécessaire et ajoute toujours le `'\0'` :

```c
#include <stdio.h>

int main(void)
{
    char court[8];
    int n = snprintf(court, sizeof court, "%s", "Bonjour tout le monde");
    printf("Copié : \"%s\"\n", court);
    if (n >= (int) sizeof court) {
        printf("Texte tronqué (%d caractères nécessaires)\n", n);
    }

    char message[40];
    snprintf(message, sizeof message, "%s a %d ans", "Lina", 22);
    printf("%s\n", message);
    return 0;
}
```

```text
Copié : "Bonjour"
Texte tronqué (21 caractères nécessaires)
Lina a 22 ans
```

`snprintf` renvoie la longueur qu'**aurait** eue le texte complet : si elle est supérieure ou égale à la taille, le texte a été coupé. Ici, seuls les 7 premiers caractères tiennent : le huitième octet est réservé au `'\0'`. Lorsque les textes sont connus dès la compilation, comme ici, gcc peut même signaler la troncature par un avertissement `-Wformat-truncation` : dans cet exemple, elle est volontaire.

> `strncpy` semble être la version sûre de `strcpy`, mais elle **n'ajoute pas** le `'\0'` si le texte est trop long. Elle est donc piégeuse : `snprintf` est plus simple à utiliser correctement.

## Lire une ligne au clavier avec `fgets`

`fgets(tampon, taille, stdin)` lit une ligne en écrivant **au plus** `taille - 1` caractères, puis le `'\0'` : elle ne peut pas déborder. Elle conserve le retour à la ligne `'\n'` final s'il y a la place ; on le retire avec `strcspn`, qui donne la position du premier `'\n'`.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    char nom[32];
    printf("Votre nom : ");
    if (fgets(nom, sizeof nom, stdin) == NULL) {
        printf("\nAucune saisie.\n");
        return 0;
    }
    nom[strcspn(nom, "\n")] = '\0';
    printf("Bonjour %s !\n", nom);
    return 0;
}
```

`fgets` renvoie `NULL` si rien n'a pu être lu (fin de l'entrée ou erreur). N'utilisez jamais `gets`, qui ne connaît pas la taille du tampon : elle a d'ailleurs été retirée du langage en C11.

## Transformer des caractères : `<ctype.h>`

`toupper`, `tolower`, `isdigit`, `isalpha`, `isspace` travaillent sur un caractère. Passez-leur un `unsigned char` converti, car leur argument doit être positif (ou `EOF`) :

```c
#include <stdio.h>
#include <ctype.h>

int main(void)
{
    char code[] = "ab12cd";
    int chiffres = 0;
    for (int i = 0; code[i] != '\0'; i++) {
        unsigned char c = (unsigned char) code[i];
        if (isdigit(c)) {
            chiffres++;
        }
        code[i] = (char) toupper(c);
    }
    printf("%s (%d chiffres)\n", code, chiffres);
    return 0;
}
```

```text
AB12CD (2 chiffres)
```

Ces fonctions traitent les caractères **un octet à la fois** : les lettres accentuées en UTF-8, qui occupent plusieurs octets, ne sont pas converties correctement.

## À retenir

- Une chaîne = tableau de `char` terminé par `'\0'` ; N caractères demandent N + 1 octets.
- `strlen` compte sans le `'\0'` ; `strcmp(a, b) == 0` pour tester l'égalité, jamais `a == b`.
- Un littéral pointé par `const char *` ne se modifie pas.
- `strcpy`, `strcat` et `gets` peuvent déborder : préférez `snprintf` et `fgets`, qui reçoivent la taille.
- `<ctype.h>` : passez un `unsigned char`.

## Exercices

### Exercice 1 — Votre propre `strlen`

Écrivez `size_t longueur(const char *s)` sans utiliser `<string.h>`, et testez-la sur `"pointeur"`.

```solution-c
#include <stdio.h>

size_t longueur(const char *s)
{
    size_t n = 0;
    while (s[n] != '\0') {
        n++;
    }
    return n;
}

int main(void)
{
    printf("%zu\n", longueur("pointeur"));
    printf("%zu\n", longueur(""));
    return 0;
}
```

```text
8
0
```

### Exercice 2 — Compter une lettre

Comptez le nombre de `'e'` dans `"excellente semaine"`.

```solution-c
#include <stdio.h>

int main(void)
{
    const char *texte = "excellente semaine";
    int n = 0;
    for (const char *p = texte; *p != '\0'; p++) {
        if (*p == 'e') {
            n++;
        }
    }
    printf("%d\n", n);
    return 0;
}
```

```text
6
```

### Exercice 3 — Identifiant sûr

Construisez dans un tableau `char id[12]` le texte `prenom-annee` à partir de `"Alexandre"` et `2025`, sans jamais déborder, et indiquez si le texte a été tronqué.

```solution-c
#include <stdio.h>

int main(void)
{
    char id[12];
    int n = snprintf(id, sizeof id, "%s-%d", "Alexandre", 2025);
    printf("%s\n", id);
    printf("%s\n", n >= (int) sizeof id ? "tronqué" : "complet");
    return 0;
}
```

```text
Alexandre-2
tronqué
```

Le texte complet `Alexandre-2025` compte 14 caractères : seuls les 11 premiers tiennent avec le `'\0'`.
"""

# ---------------------------------------------------------------------------
# Module 4 — Mémoire dynamique et structures
# ---------------------------------------------------------------------------
M4_L1 = r"""
## La pile et le tas

Jusqu'ici, toutes nos variables étaient **automatiques** : déclarées dans une fonction, elles sont rangées dans une zone appelée la **pile** (*stack*) et disparaissent automatiquement à la fin de la fonction. Cette mémoire a deux limites :

- sa **taille doit être connue** à la compilation (un `int t[100]`) ;
- sa **durée de vie** est celle de la fonction.

Pour un nombre d'éléments connu seulement à l'exécution (un fichier de taille inconnue, une liste qui grandit), on utilise le **tas** (*heap*) : une zone où le programme **demande** de la mémoire quand il en a besoin, et la **rend** quand il a fini. C'est l'**allocation dynamique**, déclarée dans `<stdlib.h>`.

| | Pile (variables locales) | Tas (allocation dynamique) |
|---|---|---|
| Réservation | automatique | `malloc`, `calloc`, `realloc` |
| Libération | automatique, en fin de bloc | **manuelle**, avec `free` |
| Taille | fixée à la compilation | choisie à l'exécution |
| Durée de vie | celle de la fonction | jusqu'au `free` |

## `malloc` et `free`

`malloc(taille)` réserve `taille` octets et renvoie l'adresse du début de la zone, ou **`NULL`** si la mémoire manque. `free(p)` rend la mémoire.

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t n = 5;
    int *carres = malloc(n * sizeof *carres);
    if (carres == NULL) {
        printf("Mémoire insuffisante\n");
        return 1;
    }
    for (size_t i = 0; i < n; i++) {
        carres[i] = (int) (i * i);
    }
    for (size_t i = 0; i < n; i++) {
        printf("%d ", carres[i]);
    }
    printf("\n");
    free(carres);
    carres = NULL;
    return 0;
}
```

```text
0 1 4 9 16
```

Les quatre gestes à répéter **à chaque allocation** :

1. calculer la taille avec `sizeof` : `n * sizeof *carres` (la taille d'un élément pointé, qui reste juste même si l'on change le type) ;
2. **tester `NULL`** avant toute utilisation ;
3. utiliser la zone comme un tableau, **sans dépasser** les `n` éléments ;
4. **libérer** avec `free` une fois terminé, puis mettre le pointeur à `NULL`.

La zone renvoyée par `malloc` n'est **pas initialisée** : elle contient des valeurs imprévisibles tant que vous n'y avez pas écrit.

## `calloc` : une zone remise à zéro

`calloc(nombre, taille_element)` réserve `nombre` éléments et les met tous à zéro :

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int *compteurs = calloc(4, sizeof *compteurs);
    if (compteurs == NULL) {
        return 1;
    }
    compteurs[2] += 3;
    for (int i = 0; i < 4; i++) {
        printf("%d ", compteurs[i]);
    }
    printf("\n");
    free(compteurs);
    return 0;
}
```

```text
0 0 3 0
```

## `realloc` : agrandir une zone

`realloc(p, nouvelle_taille)` agrandit (ou réduit) une zone. Elle peut **déplacer** les données ailleurs en mémoire et renvoie alors une nouvelle adresse ; en cas d'échec, elle renvoie `NULL` **sans libérer** l'ancienne zone. D'où le schéma sûr, avec un pointeur temporaire :

```c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t capacite = 2;
    int *t = malloc(capacite * sizeof *t);
    if (t == NULL) {
        return 1;
    }
    t[0] = 10;
    t[1] = 20;

    size_t nouvelle = capacite * 2;
    int *tmp = realloc(t, nouvelle * sizeof *t);
    if (tmp == NULL) {
        free(t);              /* l'ancienne zone est toujours valide : on la libère */
        return 1;
    }
    t = tmp;
    capacite = nouvelle;
    t[2] = 30;
    t[3] = 40;

    for (size_t i = 0; i < capacite; i++) {
        printf("%d ", t[i]);
    }
    printf("(capacité %zu)\n", capacite);
    free(t);
    return 0;
}
```

```text
10 20 30 40 (capacité 4)
```

Écrire directement `t = realloc(t, …)` est une erreur classique : en cas d'échec, `t` devient `NULL` et l'adresse de l'ancienne zone est perdue, donc impossible à libérer.

## Une fonction qui alloue

Une fonction peut renvoyer une zone allouée sur le tas : elle survit à la fin de la fonction. **L'appelant devient alors responsable de la libérer**, ce qu'il faut indiquer clairement dans un commentaire.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Renvoie une copie de s allouée sur le tas (à libérer avec free), ou NULL. */
char *dupliquer(const char *s)
{
    size_t taille = strlen(s) + 1;          /* + 1 pour le '\0' */
    char *copie = malloc(taille);
    if (copie == NULL) {
        return NULL;
    }
    memcpy(copie, s, taille);
    return copie;
}

int main(void)
{
    char *nom = dupliquer("Camille");
    if (nom == NULL) {
        return 1;
    }
    nom[0] = 'K';
    printf("%s\n", nom);
    free(nom);
    return 0;
}
```

```text
Kamille
```

Oublier le `+ 1` du `'\0'` est une erreur fréquente : la copie déborderait d'un octet.

## Les erreurs mémoire à connaître

| Erreur | Description | Conséquence |
|---|---|---|
| Fuite de mémoire (*memory leak*) | oublier `free` | la mémoire du programme grossit sans cesse |
| Utilisation après libération (*use after free*) | utiliser un pointeur après `free` | comportement indéfini, faille possible |
| Double libération (*double free*) | appeler `free` deux fois sur la même zone | comportement indéfini, souvent un plantage |
| Libération invalide | `free` sur une adresse non allouée par `malloc` | comportement indéfini |
| Dépassement (*overflow*) | écrire au-delà de la taille allouée | corruption de la mémoire |

Après `free(p)`, `p` contient toujours l'ancienne adresse : on parle de **pointeur pendant** (*dangling pointer*). Le mettre à `NULL` juste après le `free` rend une utilisation accidentelle plus facile à détecter, et `free(NULL)` ne fait rien, ce qui protège d'une double libération par ce même pointeur.

## Détecter une fuite avec Valgrind

**Valgrind** (outil libre, disponible sous Linux) exécute votre programme en surveillant chaque accès mémoire. Prenons un programme qui alloue 10 `int` et oublie le `free` :

```bash
gcc -std=c17 -Wall -Wextra -g -o fuite fuite.c
valgrind --leak-check=full ./fuite
```

Extrait de la sortie (le nombre entre `==` est l'identifiant du processus, il change à chaque fois) :

```text
==12345== HEAP SUMMARY:
==12345==     in use at exit: 40 bytes in 1 blocks
==12345== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
==12345==    at 0x4846828: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==12345==    by 0x10917E: main (fuite.c:6)
==12345== LEAK SUMMARY:
==12345==    definitely lost: 40 bytes in 1 blocks
```

Valgrind indique **40 octets perdus** (10 `int` de 4 octets) et la **ligne de l'allocation** (`fuite.c:6`), grâce à l'option `-g` qui ajoute les informations de débogage. Un programme correct doit afficher `All heap blocks were freed`.

## À retenir

- Le tas sert aux données de taille ou de durée de vie inconnues à la compilation.
- `malloc(n * sizeof *p)`, **tester `NULL`**, utiliser sans dépasser, `free(p)`, puis `p = NULL`.
- `calloc` met la zone à zéro ; `realloc` s'utilise avec un pointeur temporaire.
- Chaque `malloc` doit avoir exactement un `free` ; documentez qui libère.
- Fuite, *use after free*, *double free*, dépassement : Valgrind les détecte.

## Exercices

### Exercice 1 — Tableau de taille choisie

Allouez dynamiquement un tableau de `n = 6` `double`, remplissez-le avec `i * 0.5`, affichez la somme, puis libérez-le.

```solution-c
#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    size_t n = 6;
    double *t = malloc(n * sizeof *t);
    if (t == NULL) {
        return 1;
    }
    double somme = 0.0;
    for (size_t i = 0; i < n; i++) {
        t[i] = i * 0.5;
        somme += t[i];
    }
    printf("Somme : %.1f\n", somme);
    free(t);
    return 0;
}
```

```text
Somme : 7.5
```

### Exercice 2 — Concaténer en allouant

Écrivez `char *concatener(const char *a, const char *b)` qui renvoie une nouvelle chaîne allouée contenant `a` puis `b`. Testez avec `"pointeur"` et `"s"`.

```solution-c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Résultat à libérer avec free ; NULL si la mémoire manque. */
char *concatener(const char *a, const char *b)
{
    size_t la = strlen(a), lb = strlen(b);
    char *r = malloc(la + lb + 1);
    if (r == NULL) {
        return NULL;
    }
    memcpy(r, a, la);
    memcpy(r + la, b, lb + 1);   /* copie aussi le '\0' de b */
    return r;
}

int main(void)
{
    char *mot = concatener("pointeur", "s");
    if (mot == NULL) {
        return 1;
    }
    printf("%s (%zu caractères)\n", mot, strlen(mot));
    free(mot);
    return 0;
}
```

```text
pointeurs (9 caractères)
```

### Exercice 3 — Trouvez les erreurs

Relevez les trois problèmes de ce code.

```text
int *t = malloc(3 * sizeof(int));
t[0] = 1; t[1] = 2; t[2] = 3; t[3] = 4;
free(t);
printf("%d\n", t[0]);
```

```solution-text
1. Le résultat de malloc n'est pas testé : si t vaut NULL, t[0] = 1 est un comportement indéfini.
2. t[3] = 4 écrit au-delà des 3 cases allouées (dépassement de tas).
3. t[0] est lu après free(t) : utilisation après libération.
```
"""

M4_L2 = r"""
## Regrouper des données : `struct`

Une **structure** regroupe plusieurs variables, appelées **champs** (ou membres), éventuellement de types différents, sous un même nom. Elle permet de représenter un objet du monde réel : un étudiant, un produit, un point.

```c
#include <stdio.h>

struct etudiant {
    char nom[32];
    int age;
    double moyenne;
};

int main(void)
{
    struct etudiant e = {"Amina", 21, 14.5};
    printf("%s, %d ans, moyenne %.1f\n", e.nom, e.age, e.moyenne);
    e.age = 22;
    printf("Nouvel âge : %d\n", e.age);
    return 0;
}
```

```text
Amina, 21 ans, moyenne 14.5
Nouvel âge : 22
```

- la définition `struct etudiant { … };` crée un **nouveau type** (n'oubliez pas le point-virgule final) ;
- on accède à un champ avec le **point** : `e.age`.

## `typedef` et initialisation nommée

`typedef` donne un nom plus court à un type. Les **initialiseurs désignés** (`.champ = valeur`) rendent l'initialisation lisible et indépendante de l'ordre des champs ; les champs non cités valent 0.

```c
#include <stdio.h>

typedef struct {
    char nom[32];
    int quantite;
    double prix;
} Produit;

int main(void)
{
    Produit p = {.nom = "Clavier", .prix = 29.90, .quantite = 3};
    Produit vide = {0};
    printf("%s : %d x %.2f = %.2f\n", p.nom, p.quantite, p.prix, p.quantite * p.prix);
    printf("Quantité du produit vide : %d\n", vide.quantite);
    return 0;
}
```

```text
Clavier : 3 x 29.90 = 89.70
Quantité du produit vide : 0
```

## Structures et fonctions : la flèche `->`

Passer une structure **par valeur** copie tous ses champs : la fonction ne modifie que sa copie, et la copie coûte cher pour une grosse structure. On passe donc généralement un **pointeur**. Pour accéder à un champ via un pointeur, on utilise la **flèche** : `p->prix` est une abréviation de `(*p).prix`.

```c
#include <stdio.h>

typedef struct {
    char nom[32];
    double prix;
} Produit;

void appliquer_remise(Produit *p, double pourcentage)
{
    p->prix = p->prix * (1.0 - pourcentage / 100.0);
}

void afficher(const Produit *p)
{
    printf("%s : %.2f euros\n", p->nom, p->prix);
}

int main(void)
{
    Produit souris = {.nom = "Souris", .prix = 20.0};
    afficher(&souris);
    appliquer_remise(&souris, 15.0);
    afficher(&souris);
    return 0;
}
```

```text
Souris : 20.00 euros
Souris : 17.00 euros
```

Le `const` de `afficher` garantit que la fonction ne modifie pas le produit.

## Tableaux de structures

```c
#include <stdio.h>

typedef struct {
    char nom[32];
    double moyenne;
} Etudiant;

int main(void)
{
    Etudiant classe[] = {
        {"Amina", 14.5},
        {"Lucas", 11.0},
        {"Sofia", 16.25},
    };
    size_t n = sizeof classe / sizeof classe[0];
    size_t meilleur = 0;
    for (size_t i = 1; i < n; i++) {
        if (classe[i].moyenne > classe[meilleur].moyenne) {
            meilleur = i;
        }
    }
    printf("Meilleure moyenne : %s (%.2f)\n", classe[meilleur].nom, classe[meilleur].moyenne);
    return 0;
}
```

```text
Meilleure moyenne : Sofia (16.25)
```

## Copier une structure

L'affectation `b = a;` copie **tous les champs**, y compris les tableaux qu'elle contient. Attention cependant : si un champ est un **pointeur**, seule l'adresse est copiée, pas la zone pointée. Les deux structures partagent alors la même mémoire, et libérer cette zone deux fois (une fois par structure) serait une double libération.

## Allouer une structure sur le tas

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char nom[32];
    int points;
} Joueur;

int main(void)
{
    Joueur *j = malloc(sizeof *j);
    if (j == NULL) {
        return 1;
    }
    snprintf(j->nom, sizeof j->nom, "%s", "Nora");
    j->points = 120;
    j->points += 30;
    printf("%s a %d points\n", j->nom, j->points);
    free(j);
    return 0;
}
```

```text
Nora a 150 points
```

Pour remplir un champ texte, utilisez `snprintf` avec `sizeof j->nom` : aucun risque de débordement.

## Les énumérations : `enum`

Une **énumération** donne des noms à une liste de constantes entières. Elle rend le code plus lisible qu'une série de nombres « magiques » :

```c
#include <stdio.h>

typedef enum { EN_ATTENTE, PAYEE, EXPEDIEE } Statut;

const char *statut_texte(Statut s)
{
    switch (s) {
    case EN_ATTENTE:
        return "en attente";
    case PAYEE:
        return "payée";
    case EXPEDIEE:
        return "expédiée";
    }
    return "inconnu";
}

int main(void)
{
    Statut commande = PAYEE;
    printf("Commande %s (code %d)\n", statut_texte(commande), commande);
    return 0;
}
```

```text
Commande payée (code 1)
```

Par défaut, les valeurs commencent à 0 et augmentent de 1. Avec `-Wall`, gcc signale un `switch` sur une énumération qui oublie l'une des valeurs.

## La taille d'une structure

La taille d'une structure peut dépasser la somme de ses champs : le compilateur ajoute parfois des octets de **remplissage** (*padding*) pour aligner les champs en mémoire. Utilisez donc toujours `sizeof(Produit)` (ou `sizeof *p`), jamais une somme calculée à la main.

## À retenir

- `typedef struct { … } Nom;` crée un type ; `.champ` pour une variable, `->champ` pour un pointeur.
- Initialisation nommée : `{.nom = "…", .prix = 9.5}` ; `{0}` met tout à zéro.
- Passez les structures par pointeur (`const` si lecture seule).
- La copie d'une structure ne copie pas la mémoire pointée par ses champs pointeurs.
- `enum` pour nommer des constantes ; `sizeof` pour la taille d'une structure.

## Exercices

### Exercice 1 — Rectangle

Définissez `Rectangle` (largeur et hauteur en `double`) et deux fonctions `aire` et `perimetre` qui reçoivent un `const Rectangle *`. Testez avec 4 x 2,5.

```solution-c
#include <stdio.h>

typedef struct {
    double largeur;
    double hauteur;
} Rectangle;

double aire(const Rectangle *r)
{
    return r->largeur * r->hauteur;
}

double perimetre(const Rectangle *r)
{
    return 2.0 * (r->largeur + r->hauteur);
}

int main(void)
{
    Rectangle r = {.largeur = 4.0, .hauteur = 2.5};
    printf("Aire : %.2f\n", aire(&r));
    printf("Périmètre : %.2f\n", perimetre(&r));
    return 0;
}
```

```text
Aire : 10.00
Périmètre : 13.00
```

### Exercice 2 — Stock total

Avec un tableau de trois `Produit` (nom, quantité, prix) — Stylo 10 x 1.20, Cahier 4 x 3.50, Règle 2 x 2.00 — affichez la valeur totale du stock.

```solution-c
#include <stdio.h>

typedef struct {
    char nom[32];
    int quantite;
    double prix;
} Produit;

double valeur_stock(const Produit *t, size_t n)
{
    double total = 0.0;
    for (size_t i = 0; i < n; i++) {
        total += t[i].quantite * t[i].prix;
    }
    return total;
}

int main(void)
{
    Produit stock[] = {
        {"Stylo", 10, 1.20},
        {"Cahier", 4, 3.50},
        {"Règle", 2, 2.00},
    };
    printf("Valeur du stock : %.2f euros\n", valeur_stock(stock, 3));
    return 0;
}
```

```text
Valeur du stock : 30.00 euros
```

### Exercice 3 — Point milieu

Définissez `Point` (x, y en `double`) et une fonction `Point milieu(Point a, Point b)` qui renvoie le milieu du segment. Testez avec (0, 0) et (4, 6).

```solution-c
#include <stdio.h>

typedef struct {
    double x;
    double y;
} Point;

Point milieu(Point a, Point b)
{
    Point m = {(a.x + b.x) / 2.0, (a.y + b.y) / 2.0};
    return m;
}

int main(void)
{
    Point a = {0.0, 0.0};
    Point b = {4.0, 6.0};
    Point m = milieu(a, b);
    printf("Milieu : (%.1f, %.1f)\n", m.x, m.y);
    return 0;
}
```

```text
Milieu : (2.0, 3.0)
```

Pour une petite structure comme `Point`, le passage et le retour par valeur sont simples et sans danger.
"""

M4_L3 = r"""
## Les comportements indéfinis : récapitulatif

Vous avez rencontré plusieurs **comportements indéfinis** (*undefined behavior*). Rappelons ce que cela signifie : la norme du C n'impose **aucun** résultat. Le programme peut fonctionner sur votre machine, échouer chez un client, ou changer de comportement avec une autre option d'optimisation, car le compilateur a le droit de supposer qu'ils n'arrivent jamais.

| Comportement indéfini | Exemple | Prévention |
|---|---|---|
| Indice hors limites | `t[n]` dans un tableau de `n` cases | boucles `i < n`, vérifier les indices externes |
| Variable non initialisée | `int total; total += 5;` | initialiser à la déclaration |
| Déréférencement de `NULL` | `*p` avec `p == NULL` | tester `NULL` (résultat de `malloc`, `fopen`…) |
| Utilisation après `free` | lire `p[0]` après `free(p)` | `p = NULL` après `free` |
| Double `free` | `free(p); free(p);` | un seul propriétaire par zone |
| Dépassement d'entier signé | `INT_MAX + 1` | vérifier les bornes, types plus grands |
| Division entière par zéro | `a / 0` | tester le diviseur |
| Chaîne sans `'\0'` | `strlen` sur un tableau non terminé | `snprintf`, `fgets` |
| Mauvais format `printf` | `printf("%d", 2.5)` | compiler avec `-Wall` |

Dans un programme exposé à des données extérieures (réseau, fichiers), ces erreurs deviennent des **failles de sécurité** : un dépassement de tampon peut permettre à un attaquant de lire des données secrètes ou d'exécuter son propre code.

## Première ligne de défense : le compilateur

Compilez toujours avec les avertissements, et faites-en des erreurs pendant le développement :

```bash
gcc -std=c17 -Wall -Wextra -Werror -g -o prog prog.c
```

`-Werror` transforme chaque avertissement en erreur : impossible de l'ignorer. gcc repère ainsi de nombreuses fautes, par exemple une utilisation après `free` évidente :

```text
uaf.c:12:5: warning: pointer 'p' used after 'free' [-Wuse-after-free]
   12 |     printf("%d\n", *p);   /* erreur : utilisation après libération */
      |     ^~~~~~~~~~~~~~~~~~
```

Mais le compilateur ne voit pas tout : la plupart des erreurs mémoire dépendent des données et n'apparaissent qu'à l'**exécution**.

## Deuxième ligne de défense : les *sanitizers*

Les **sanitizers** sont des options de gcc et de clang qui ajoutent des vérifications au programme compilé. Le programme est plus lent : on les active pendant le développement et les tests, pas en production.

| Option | Détecte |
|---|---|
| `-fsanitize=address` (ASan) | dépassements (tas, pile, globales), *use after free*, *double free*, fuites (sous Linux) |
| `-fsanitize=undefined` (UBSan) | dépassement d'entier signé, division par zéro, décalages invalides… |

Les deux se combinent : `-fsanitize=address,undefined`. Ajoutez `-g` pour obtenir les numéros de ligne.

**Exemple 1 — un dépassement sur le tas.** Ce programme alloue 5 `int`, mais sa boucle `for (int i = 0; i <= 5; i++)` écrit 6 cases :

```bash
gcc -std=c17 -Wall -Wextra -g -fsanitize=address -o debord debord.c
./debord
```

Extrait du rapport (les adresses varient) :

```text
==7235==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x503000000054 at pc 0x55ca2d9122c9 bp 0x7ffedd9899b0 sp 0x7ffedd9899a0
WRITE of size 4 at 0x503000000054 thread T0
    #0 0x55ca2d9122c8 in main /tmp/cwork/debord.c:11

0x503000000054 is located 0 bytes after 20-byte region [0x503000000040,0x503000000054)
SUMMARY: AddressSanitizer: heap-buffer-overflow /tmp/cwork/debord.c:11 in main
```

Le rapport se lit ainsi : une **écriture de 4 octets** (`WRITE of size 4`, un `int`) a eu lieu **juste après** (`0 bytes after`) une zone de **20 octets** (5 `int`), à la **ligne 11** de `debord.c`. Sans ASan, ce même programme s'exécute souvent sans aucun message : le bogue resterait caché.

**Exemple 2 — un dépassement d'entier.** Avec `-fsanitize=undefined`, l'instruction `x = x + 1;` sur un `int` valant `INT_MAX` produit :

```text
ub.c:7:7: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
```

## Troisième outil : Valgrind

**Valgrind** (vu à la leçon précédente) n'exige pas de recompiler avec une option spéciale : il exécute le programme dans une machine virtuelle qui surveille la mémoire. Il est plus lent qu'ASan mais pratique pour vérifier les fuites :

```bash
valgrind --leak-check=full ./prog
```

N'utilisez pas Valgrind sur un programme compilé avec `-fsanitize=address` : les deux outils sont incompatibles. Valgrind est disponible principalement sous Linux ; ASan fonctionne aussi sous macOS avec clang.

> Aucun outil ne prouve qu'un programme est correct : ils ne détectent que les erreurs **survenues pendant l'exécution testée**. Testez donc aussi les cas limites : tableau vide, un seul élément, texte très long, fichier absent.

## Mettre en pratique : un tableau dynamique sûr

Assemblons tout ce que vous savez dans une petite bibliothèque de **tableau dynamique** : une structure qui garde l'adresse des données, le nombre d'éléments et la capacité, et qui double sa capacité quand elle est pleine.

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int *donnees;
    size_t taille;     /* nombre d'éléments utilisés */
    size_t capacite;   /* nombre d'éléments alloués */
} Tableau;

void tab_init(Tableau *t)
{
    t->donnees = NULL;
    t->taille = 0;
    t->capacite = 0;
}

bool tab_ajouter(Tableau *t, int valeur)
{
    if (t->taille == t->capacite) {
        size_t nouvelle = t->capacite == 0 ? 4 : t->capacite * 2;
        int *tmp = realloc(t->donnees, nouvelle * sizeof *tmp);
        if (tmp == NULL) {
            return false;            /* l'ancien contenu reste intact */
        }
        t->donnees = tmp;
        t->capacite = nouvelle;
    }
    t->donnees[t->taille] = valeur;
    t->taille++;
    return true;
}

bool tab_lire(const Tableau *t, size_t i, int *valeur)
{
    if (i >= t->taille) {
        return false;                /* indice refusé au lieu d'un dépassement */
    }
    *valeur = t->donnees[i];
    return true;
}

void tab_liberer(Tableau *t)
{
    free(t->donnees);
    tab_init(t);                     /* plus de pointeur pendant */
}

int main(void)
{
    Tableau t;
    tab_init(&t);
    for (int i = 1; i <= 10; i++) {
        if (!tab_ajouter(&t, i * 10)) {
            tab_liberer(&t);
            return 1;
        }
    }
    printf("Taille %zu, capacité %zu\n", t.taille, t.capacite);

    int v = 0;
    if (tab_lire(&t, 9, &v)) {
        printf("Élément 9 : %d\n", v);
    }
    if (!tab_lire(&t, 10, &v)) {
        printf("Indice 10 refusé\n");
    }
    tab_liberer(&t);
    printf("Après libération : taille %zu\n", t.taille);
    return 0;
}
```

```text
Taille 10, capacité 16
Élément 9 : 100
Indice 10 refusé
Après libération : taille 0
```

Les choix de sûreté de ce code :

- `realloc(NULL, …)` se comporte comme `malloc` : le premier ajout fonctionne sans cas particulier ;
- un échec d'allocation est **signalé** (`false`) au lieu de faire planter le programme ;
- `tab_lire` **vérifie l'indice** : l'accès hors limites devient une erreur gérée ;
- `tab_liberer` remet la structure dans un état vide et cohérent : un second appel ne provoque pas de double libération, car `free(NULL)` ne fait rien.

Compilé avec `-fsanitize=address,undefined` ou exécuté sous Valgrind, ce programme ne signale aucune erreur ni fuite.

## À retenir

- Un comportement indéfini peut rester invisible longtemps : il faut le **prévenir** et le **chercher**.
- Développez avec `-Wall -Wextra -Werror -g`.
- Testez avec `-fsanitize=address,undefined` ; vérifiez les fuites avec ASan ou `valgrind --leak-check=full`.
- Les outils ne voient que les chemins exécutés : testez les cas limites.
- Encapsulez la mémoire dans des fonctions (`init`, `ajouter`, `liberer`) qui vérifient tout.

## Exercices

### Exercice 1 — Somme d'un tableau dynamique

Ajoutez au tableau dynamique une fonction `long long tab_somme(const Tableau *t)` et vérifiez-la avec les valeurs 5, 15 et 25.

```solution-c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct {
    int *donnees;
    size_t taille;
    size_t capacite;
} Tableau;

bool tab_ajouter(Tableau *t, int valeur)
{
    if (t->taille == t->capacite) {
        size_t nouvelle = t->capacite == 0 ? 4 : t->capacite * 2;
        int *tmp = realloc(t->donnees, nouvelle * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        t->donnees = tmp;
        t->capacite = nouvelle;
    }
    t->donnees[t->taille++] = valeur;
    return true;
}

long long tab_somme(const Tableau *t)
{
    long long somme = 0;
    for (size_t i = 0; i < t->taille; i++) {
        somme += t->donnees[i];
    }
    return somme;
}

int main(void)
{
    Tableau t = {NULL, 0, 0};
    int valeurs[] = {5, 15, 25};
    for (size_t i = 0; i < 3; i++) {
        if (!tab_ajouter(&t, valeurs[i])) {
            free(t.donnees);
            return 1;
        }
    }
    printf("Somme : %lld\n", tab_somme(&t));
    free(t.donnees);
    return 0;
}
```

```text
Somme : 45
```

`long long` évite un dépassement si la somme de nombreux `int` devient grande.

### Exercice 2 — Quel outil ?

Pour chaque situation, indiquez l'outil le plus adapté : (a) savoir si un programme déjà compilé libère toute sa mémoire, sans le recompiler ; (b) détecter un dépassement d'entier signé ; (c) repérer `if (x = 3)` avant même d'exécuter.

```solution-text
(a) Valgrind : valgrind --leak-check=full ./prog (aucune recompilation nécessaire, même si -g aide à lire le rapport).
(b) UndefinedBehaviorSanitizer : compiler avec -fsanitize=undefined.
(c) Les avertissements du compilateur : -Wall (option -Wparentheses), idéalement avec -Werror.
```

### Exercice 3 — Corriger une fuite

Ce programme fuit : `char *a = dupliquer("x"); a = dupliquer("y"); free(a);`. Expliquez pourquoi et corrigez-le.

```solution-text
La première zone (copie de "x") n'est jamais libérée : son adresse est écrasée par la
seconde affectation, elle est donc perdue. Il faut libérer avant de réaffecter :
char *a = dupliquer("x");
free(a);
a = dupliquer("y");
free(a);
```
"""

# ---------------------------------------------------------------------------
# Module 5 — Fichiers et mini-projet
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Pourquoi des fichiers ?

Les variables disparaissent quand le programme s'arrête. Pour **conserver** des données (scores, réglages, inventaire), on les écrit dans un **fichier**. La bibliothèque `<stdio.h>` fournit tout le nécessaire, à travers le type `FILE *` : un pointeur vers une structure qui représente un fichier ouvert (on parle de **flux**, *stream*).

Vous utilisez déjà trois flux ouverts automatiquement : `stdin` (le clavier), `stdout` (l'écran) et `stderr` (l'écran, réservé aux messages d'erreur).

## Ouvrir et fermer : `fopen` et `fclose`

`fopen(chemin, mode)` ouvre un fichier et renvoie un `FILE *`, ou **`NULL`** en cas d'échec (fichier absent, droits insuffisants, dossier inexistant…).

| Mode | Effet | Si le fichier n'existe pas |
|---|---|---|
| `"r"` | lecture | échec (`NULL`) |
| `"w"` | écriture, **efface** le contenu existant | il est créé |
| `"a"` | ajout à la fin (*append*) | il est créé |
| `"r+"` | lecture et écriture | échec |
| `"rb"`, `"wb"`… | même chose en mode **binaire** | (voir leçon suivante) |

Chaque `fopen` réussi doit être suivi d'un **`fclose`** : il vide les données encore en attente dans la mémoire tampon vers le disque et libère les ressources. Un fichier non fermé est une **fuite**, comme un `malloc` sans `free`.

## Écrire dans un fichier : `fprintf`

`fprintf` fonctionne comme `printf`, avec un premier argument supplémentaire : le fichier.

```c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("notes.txt", "w");
    if (f == NULL) {
        perror("notes.txt");
        return 1;
    }
    fprintf(f, "Amina 15\n");
    fprintf(f, "Lucas 12\n");
    fprintf(f, "Sofia 17\n");
    if (fclose(f) != 0) {
        perror("fclose");
        return 1;
    }
    printf("Fichier écrit.\n");
    return 0;
}
```

```text
Fichier écrit.
```

`perror` affiche sur `stderr` le texte fourni suivi de la cause de la dernière erreur système, par exemple `notes.txt: Permission denied`. `fclose` peut lui-même échouer (disque plein) : pour un fichier écrit, tester son retour est une bonne habitude.

## Lire ligne par ligne : `fgets`

La façon la plus sûre de lire un fichier texte est `fgets`, qui lit **une ligne à la fois** dans un tampon de taille connue, sans jamais déborder. Elle renvoie `NULL` à la fin du fichier.

```c
#include <stdio.h>
#include <string.h>

int main(void)
{
    FILE *f = fopen("courses.txt", "w");
    if (f == NULL) {
        perror("courses.txt");
        return 1;
    }
    fprintf(f, "pain\nlait\npommes\n");
    fclose(f);

    f = fopen("courses.txt", "r");
    if (f == NULL) {
        perror("courses.txt");
        return 1;
    }
    char ligne[128];
    int numero = 1;
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        ligne[strcspn(ligne, "\n")] = '\0';
        printf("%d. %s\n", numero, ligne);
        numero++;
    }
    fclose(f);
    return 0;
}
```

```text
1. pain
2. lait
3. pommes
```

> Si une ligne dépasse la taille du tampon, `fgets` la lit en plusieurs morceaux : le morceau lu ne se termine alors pas par `'\n'`. Choisissez une taille confortable et, pour un programme robuste, détectez ce cas.

## Lire caractère par caractère : `fgetc`

`fgetc(f)` renvoie le caractère suivant, ou la constante **`EOF`** (*end of file*) à la fin. Son résultat est un **`int`**, pas un `char` : `EOF` est une valeur négative distincte de tous les caractères, et la stocker dans un `char` empêcherait de la reconnaître de façon fiable.

```c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("texte.txt", "w");
    if (f == NULL) {
        return 1;
    }
    fprintf(f, "Le C\nest un langage\ncompilé.\n");
    fclose(f);

    f = fopen("texte.txt", "r");
    if (f == NULL) {
        return 1;
    }
    int c;
    int lignes = 0, caracteres = 0;
    while ((c = fgetc(f)) != EOF) {
        caracteres++;
        if (c == '\n') {
            lignes++;
        }
    }
    fclose(f);
    printf("%d lignes, %d octets\n", lignes, caracteres);
    return 0;
}
```

```text
3 lignes, 30 octets
```

Le décompte est en **octets** : le `é` de « compilé » en occupe deux en UTF-8.

## Gérer un fichier absent

Avant d'ouvrir un fichier en lecture, on ne peut pas savoir s'il existe : il faut **toujours** tester le résultat de `fopen`. La variable `errno` (déclarée dans `<errno.h>`) contient alors le code de l'erreur, que `strerror` traduit en texte :

```c
#include <stdio.h>
#include <string.h>
#include <errno.h>

int main(void)
{
    FILE *f = fopen("inexistant.txt", "r");
    if (f == NULL) {
        printf("Impossible d'ouvrir le fichier : %s\n", strerror(errno));
        return 0;
    }
    fclose(f);
    return 0;
}
```

```text
Impossible d'ouvrir le fichier : No such file or directory
```

Le texte du message dépend du système et de sa langue. Sous Linux et macOS, `fopen` renseigne `errno` ; la norme du C ne l'exige pas, d'où l'intérêt de `perror` et `strerror` plutôt que de codes écrits en dur.

## Ajouter à la fin : le mode `"a"`

Le mode `"a"` est idéal pour un **journal** (*log*) : chaque exécution ajoute ses lignes sans effacer les précédentes.

```c
#include <stdio.h>

int journaliser(const char *message)
{
    FILE *f = fopen("journal.txt", "a");
    if (f == NULL) {
        return -1;
    }
    fprintf(f, "%s\n", message);
    return fclose(f);
}

int main(void)
{
    journaliser("Démarrage");
    journaliser("Traitement terminé");

    FILE *f = fopen("journal.txt", "r");
    if (f == NULL) {
        return 1;
    }
    char ligne[100];
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        printf("> %s", ligne);
    }
    fclose(f);
    return 0;
}
```

```text
> Démarrage
> Traitement terminé
```

## À retenir

- `FILE *f = fopen(chemin, mode)` puis **tester `NULL`** ; toujours `fclose(f)`.
- `"w"` efface, `"a"` ajoute, `"r"` lit et échoue si le fichier n'existe pas.
- Écrire : `fprintf` ; lire une ligne : `fgets` dans un tampon de taille connue.
- `fgetc` renvoie un `int` à comparer à `EOF`.
- `perror` et `strerror(errno)` expliquent la cause d'un échec.

## Exercices

### Exercice 1 — Table dans un fichier

Écrivez la table de 9 (de 1 à 5) dans `table9.txt`, puis relisez le fichier et affichez son contenu.

```solution-c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("table9.txt", "w");
    if (f == NULL) {
        perror("table9.txt");
        return 1;
    }
    for (int i = 1; i <= 5; i++) {
        fprintf(f, "9 x %d = %d\n", i, 9 * i);
    }
    fclose(f);

    f = fopen("table9.txt", "r");
    if (f == NULL) {
        perror("table9.txt");
        return 1;
    }
    char ligne[64];
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        printf("%s", ligne);
    }
    fclose(f);
    return 0;
}
```

```text
9 x 1 = 9
9 x 2 = 18
9 x 3 = 27
9 x 4 = 36
9 x 5 = 45
```

### Exercice 2 — Copier un fichier

Écrivez `int copier(const char *source, const char *destination)` qui copie un fichier caractère par caractère et renvoie 0 en cas de succès, -1 sinon. Testez-la.

```solution-c
#include <stdio.h>

int copier(const char *source, const char *destination)
{
    FILE *in = fopen(source, "r");
    if (in == NULL) {
        return -1;
    }
    FILE *out = fopen(destination, "w");
    if (out == NULL) {
        fclose(in);              /* ne pas oublier le premier fichier */
        return -1;
    }
    int c;
    while ((c = fgetc(in)) != EOF) {
        fputc(c, out);
    }
    fclose(in);
    return fclose(out) == 0 ? 0 : -1;
}

int main(void)
{
    FILE *f = fopen("original.txt", "w");
    if (f == NULL) {
        return 1;
    }
    fprintf(f, "Bonjour\n");
    fclose(f);

    printf("Copie : %d\n", copier("original.txt", "copie.txt"));
    printf("Source absente : %d\n", copier("absent.txt", "copie2.txt"));
    return 0;
}
```

```text
Copie : 0
Source absente : -1
```

Remarquez le `fclose(in)` dans le cas d'échec : chaque chemin de sortie de la fonction doit fermer ce qui a été ouvert.
"""

M5_L2 = r"""
## Des données structurées dans un fichier texte

Un format très courant pour échanger des données est le **CSV** (*comma-separated values*) : une ligne par enregistrement, des champs séparés par un caractère (souvent `,` ou `;`). Par exemple, un fichier `ventes.csv` :

```text
Stylo;10;1.20
Cahier;4;3.50
Règle;2;2.00
```

Pour le lire, on combine `fgets` (une ligne à la fois) et `sscanf` (analyser la ligne).

## Analyser une ligne avec `sscanf`

```c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("ventes.csv", "w");
    if (f == NULL) {
        return 1;
    }
    fprintf(f, "Stylo;10;1.20\nCahier;4;3.50\nligne invalide\nRègle;2;2.00\n");
    fclose(f);

    f = fopen("ventes.csv", "r");
    if (f == NULL) {
        perror("ventes.csv");
        return 1;
    }
    char ligne[128];
    char nom[32];
    int quantite;
    double prix;
    double total = 0.0;
    int numero = 0;
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        numero++;
        if (sscanf(ligne, "%31[^;];%d;%lf", nom, &quantite, &prix) != 3) {
            printf("Ligne %d ignorée\n", numero);
            continue;
        }
        printf("%-8s %3d x %5.2f\n", nom, quantite, prix);
        total += quantite * prix;
    }
    fclose(f);
    printf("Total : %.2f\n", total);
    return 0;
}
```

```text
Stylo     10 x  1.20
Cahier     4 x  3.50
Ligne 3 ignorée
Règle     2 x  2.00
Total : 30.00
```

Le format `%31[^;]` signifie : « lire au plus **31** caractères différents de `;` ». Deux points essentiels :

- **la largeur 31** protège le tableau `nom[32]` (31 caractères + `'\0'`). Un `%s` ou `%[^;]` sans largeur déborderait sur une ligne trop longue : c'est une faille classique ;
- le **retour de `sscanf`** (3 valeurs attendues) permet d'ignorer proprement une ligne mal formée au lieu d'utiliser des variables non remplies.

L'alignement de `Règle` est décalé d'un espace : `é` occupe deux octets en UTF-8 et `%-8s` compte des octets.

## Convertir un texte en nombre avec contrôle : `strtol`

`sscanf("12abc", "%d", &n)` accepte `12` et ignore la suite sans le signaler. Pour une **validation stricte**, on utilise `strtol` (*string to long*) de `<stdlib.h>`, qui indique où la conversion s'est arrêtée :

```c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include <limits.h>

bool lire_entier(const char *texte, int *resultat)
{
    char *fin = NULL;
    errno = 0;
    long valeur = strtol(texte, &fin, 10);
    if (fin == texte || *fin != '\0') {
        return false;                 /* rien lu, ou caractères en trop */
    }
    if (errno == ERANGE || valeur < INT_MIN || valeur > INT_MAX) {
        return false;                 /* nombre trop grand */
    }
    *resultat = (int) valeur;
    return true;
}

int main(void)
{
    const char *essais[] = {"42", "-7", "12abc", "", "99999999999999999999"};
    for (int i = 0; i < 5; i++) {
        int n = 0;
        if (lire_entier(essais[i], &n)) {
            printf("\"%s\" -> %d\n", essais[i], n);
        } else {
            printf("\"%s\" -> invalide\n", essais[i]);
        }
    }
    return 0;
}
```

```text
"42" -> 42
"-7" -> -7
"12abc" -> invalide
"" -> invalide
"99999999999999999999" -> invalide
```

- `fin` reçoit l'adresse du premier caractère **non converti** : s'il ne pointe pas sur le `'\0'` final, il reste des caractères en trop ;
- si le nombre dépasse la capacité d'un `long`, `strtol` met `errno` à `ERANGE` ;
- le dernier argument, `10`, est la base (décimale).

> Toute donnée venant de l'extérieur (fichier, saisie, réseau) doit être **validée** avant d'être utilisée, surtout si elle sert d'indice de tableau ou de taille d'allocation.

## Les fichiers binaires : `fwrite` et `fread`

Un fichier **binaire** contient directement les octets de la mémoire, sans conversion en texte. On l'ouvre avec `"wb"` ou `"rb"` et on utilise `fwrite(adresse, taille_element, nombre, f)` et `fread(...)`, qui renvoient le **nombre d'éléments** réellement écrits ou lus.

```c
#include <stdio.h>

typedef struct {
    int id;
    double solde;
} Compte;

int main(void)
{
    Compte comptes[3] = {{1, 120.5}, {2, 0.0}, {3, 87.25}};
    FILE *f = fopen("comptes.bin", "wb");
    if (f == NULL) {
        return 1;
    }
    size_t ecrits = fwrite(comptes, sizeof comptes[0], 3, f);
    fclose(f);
    printf("%zu comptes écrits\n", ecrits);

    Compte relus[3];
    f = fopen("comptes.bin", "rb");
    if (f == NULL) {
        return 1;
    }
    size_t lus = fread(relus, sizeof relus[0], 3, f);
    fclose(f);
    for (size_t i = 0; i < lus; i++) {
        printf("Compte %d : %.2f\n", relus[i].id, relus[i].solde);
    }
    return 0;
}
```

```text
3 comptes écrits
Compte 1 : 120.50
Compte 2 : 0.00
Compte 3 : 87.25
```

| | Fichier texte | Fichier binaire |
|---|---|---|
| Lisible par un humain | oui | non |
| Taille | souvent plus grande | compacte |
| Portabilité entre machines | bonne | **fragile** : tailles des types, remplissage des structures et ordre des octets peuvent différer |
| Usage typique | configuration, export, échange | cache local, données volumineuses |

Pour des données échangées entre programmes ou machines, préférez un **format texte** bien défini.

## Codes de retour du programme

`<stdlib.h>` définit `EXIT_SUCCESS` et `EXIT_FAILURE`, plus explicites que `0` et `1`. Le code de retour de `main` est récupérable par le terminal (`echo $?` sous Linux et macOS) : les scripts s'en servent pour savoir si un programme a réussi.

## À retenir

- Lire un fichier structuré : `fgets` + `sscanf`, en testant le nombre de valeurs lues.
- Toujours une **largeur** pour lire du texte : `%31s`, `%31[^;]` pour un tableau de 32 octets.
- `strtol` + contrôle de `fin` et `errno` pour valider strictement un nombre.
- `fwrite` / `fread` en mode `"wb"` / `"rb"` ; vérifiez le nombre d'éléments traités.
- Le binaire est compact mais peu portable ; le texte est préférable pour l'échange.

## Exercices

### Exercice 1 — Moyenne d'un fichier de notes

Créez un fichier `notes.txt` contenant une note entière par ligne (12, 15, 9, 18), relisez-le avec `fgets` et `sscanf`, et affichez la moyenne.

```solution-c
#include <stdio.h>

int main(void)
{
    FILE *f = fopen("notes.txt", "w");
    if (f == NULL) {
        return 1;
    }
    fprintf(f, "12\n15\n9\n18\n");
    fclose(f);

    f = fopen("notes.txt", "r");
    if (f == NULL) {
        return 1;
    }
    char ligne[32];
    int somme = 0, nb = 0, note;
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        if (sscanf(ligne, "%d", &note) == 1) {
            somme += note;
            nb++;
        }
    }
    fclose(f);
    if (nb > 0) {
        printf("Moyenne de %d notes : %.2f\n", nb, (double) somme / nb);
    }
    return 0;
}
```

```text
Moyenne de 4 notes : 13.50
```

Le test `nb > 0` évite une division par zéro si le fichier est vide.

### Exercice 2 — Valider un âge

Avec la fonction `lire_entier` de la leçon, écrivez `bool lire_age(const char *texte, int *age)` qui n'accepte que les entiers de 0 à 130. Testez `"34"`, `"-2"` et `"trente"`.

```solution-c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <errno.h>
#include <limits.h>

bool lire_entier(const char *texte, int *resultat)
{
    char *fin = NULL;
    errno = 0;
    long valeur = strtol(texte, &fin, 10);
    if (fin == texte || *fin != '\0' || errno == ERANGE || valeur < INT_MIN || valeur > INT_MAX) {
        return false;
    }
    *resultat = (int) valeur;
    return true;
}

bool lire_age(const char *texte, int *age)
{
    int n = 0;
    if (!lire_entier(texte, &n) || n < 0 || n > 130) {
        return false;
    }
    *age = n;
    return true;
}

int main(void)
{
    const char *essais[] = {"34", "-2", "trente"};
    for (int i = 0; i < 3; i++) {
        int age = 0;
        printf("%s : %s\n", essais[i], lire_age(essais[i], &age) ? "valide" : "refusé");
    }
    return 0;
}
```

```text
34 : valide
-2 : refusé
trente : refusé
```
"""

M5_L3 = r"""
## Le projet

Pour terminer, vous allez réaliser un **gestionnaire d'inventaire** en ligne de commande, qui mobilise toute la formation :

- une **structure** `Article` (nom, quantité, prix) ;
- un **tableau dynamique** d'articles qui grandit avec `realloc` ;
- des **fonctions** avec passage par pointeur et `const` ;
- des **chaînes** copiées sans débordement avec `snprintf` ;
- la **sauvegarde** dans un fichier CSV et le **rechargement** avec `fgets` et `sscanf` ;
- une **libération** complète de la mémoire, vérifiable avec les sanitizers.

## Étape 1 — Les types

```h
typedef struct {
    char nom[32];
    int quantite;
    double prix;
} Article;

typedef struct {
    Article *articles;   /* zone allouée sur le tas */
    size_t taille;       /* nombre d'articles utilisés */
    size_t capacite;     /* nombre d'articles alloués */
} Inventaire;
```

C'est le même principe que le tableau dynamique du module 4, appliqué à des structures.

## Étape 2 — Le programme complet

Lisez attentivement chaque fonction : chacune vérifie ses entrées et signale ses échecs.

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

typedef struct {
    char nom[32];
    int quantite;
    double prix;
} Article;

typedef struct {
    Article *articles;
    size_t taille;
    size_t capacite;
} Inventaire;

void inv_init(Inventaire *inv)
{
    inv->articles = NULL;
    inv->taille = 0;
    inv->capacite = 0;
}

void inv_liberer(Inventaire *inv)
{
    free(inv->articles);
    inv_init(inv);
}

/* Renvoie l'indice de l'article, ou -1 s'il est absent. */
long inv_trouver(const Inventaire *inv, const char *nom)
{
    for (size_t i = 0; i < inv->taille; i++) {
        if (strcmp(inv->articles[i].nom, nom) == 0) {
            return (long) i;
        }
    }
    return -1;
}

/* Ajoute un article, ou augmente sa quantité s'il existe déjà. */
bool inv_ajouter(Inventaire *inv, const char *nom, int quantite, double prix)
{
    if (quantite < 0 || prix < 0.0 || strlen(nom) >= sizeof inv->articles[0].nom) {
        return false;                       /* données refusées */
    }
    long i = inv_trouver(inv, nom);
    if (i >= 0) {
        inv->articles[i].quantite += quantite;
        inv->articles[i].prix = prix;
        return true;
    }
    if (inv->taille == inv->capacite) {
        size_t nouvelle = inv->capacite == 0 ? 2 : inv->capacite * 2;
        Article *tmp = realloc(inv->articles, nouvelle * sizeof *tmp);
        if (tmp == NULL) {
            return false;
        }
        inv->articles = tmp;
        inv->capacite = nouvelle;
    }
    Article *a = &inv->articles[inv->taille];
    snprintf(a->nom, sizeof a->nom, "%s", nom);
    a->quantite = quantite;
    a->prix = prix;
    inv->taille++;
    return true;
}

bool inv_retirer(Inventaire *inv, const char *nom, int quantite)
{
    long i = inv_trouver(inv, nom);
    if (i < 0 || quantite < 0 || inv->articles[i].quantite < quantite) {
        return false;
    }
    inv->articles[i].quantite -= quantite;
    return true;
}

double inv_valeur(const Inventaire *inv)
{
    double total = 0.0;
    for (size_t i = 0; i < inv->taille; i++) {
        total += inv->articles[i].quantite * inv->articles[i].prix;
    }
    return total;
}

void inv_afficher(const Inventaire *inv)
{
    printf("%-12s %8s %8s\n", "Article", "Quantité", "Prix");
    for (size_t i = 0; i < inv->taille; i++) {
        const Article *a = &inv->articles[i];
        printf("%-12s %8d %8.2f\n", a->nom, a->quantite, a->prix);
    }
    printf("Valeur totale : %.2f euros\n", inv_valeur(inv));
}

bool inv_sauvegarder(const Inventaire *inv, const char *chemin)
{
    FILE *f = fopen(chemin, "w");
    if (f == NULL) {
        return false;
    }
    for (size_t i = 0; i < inv->taille; i++) {
        const Article *a = &inv->articles[i];
        fprintf(f, "%s;%d;%.2f\n", a->nom, a->quantite, a->prix);
    }
    return fclose(f) == 0;
}

/* Ajoute à inv les articles du fichier ; renvoie le nombre de lignes ignorées, ou -1. */
int inv_charger(Inventaire *inv, const char *chemin)
{
    FILE *f = fopen(chemin, "r");
    if (f == NULL) {
        return -1;
    }
    char ligne[128];
    char nom[32];
    int quantite;
    double prix;
    int ignorees = 0;
    while (fgets(ligne, sizeof ligne, f) != NULL) {
        if (sscanf(ligne, "%31[^;];%d;%lf", nom, &quantite, &prix) != 3
            || !inv_ajouter(inv, nom, quantite, prix)) {
            ignorees++;
        }
    }
    fclose(f);
    return ignorees;
}

int main(void)
{
    Inventaire inv;
    inv_init(&inv);

    inv_ajouter(&inv, "Clavier", 5, 29.90);
    inv_ajouter(&inv, "Souris", 12, 14.50);
    inv_ajouter(&inv, "Ecran", 3, 189.00);
    inv_ajouter(&inv, "Souris", 3, 14.50);   /* article existant : quantité cumulée */
    if (!inv_retirer(&inv, "Ecran", 5)) {
        printf("Retrait impossible : stock insuffisant\n");
    }
    inv_retirer(&inv, "Clavier", 2);
    inv_afficher(&inv);

    if (!inv_sauvegarder(&inv, "inventaire.csv")) {
        printf("Échec de la sauvegarde\n");
        inv_liberer(&inv);
        return EXIT_FAILURE;
    }
    inv_liberer(&inv);

    /* Rechargement dans un inventaire neuf */
    FILE *f = fopen("inventaire.csv", "a");
    if (f != NULL) {
        fprintf(f, "ligne abîmée\n");        /* simulons une ligne corrompue */
        fclose(f);
    }
    Inventaire copie;
    inv_init(&copie);
    int ignorees = inv_charger(&copie, "inventaire.csv");
    printf("\nRechargé : %zu articles, %d ligne(s) ignorée(s)\n", copie.taille, ignorees);
    printf("Valeur totale : %.2f euros\n", inv_valeur(&copie));
    inv_liberer(&copie);
    return EXIT_SUCCESS;
}
```

```text
Retrait impossible : stock insuffisant
Article      Quantité     Prix
Clavier             3    29.90
Souris             15    14.50
Ecran               3   189.00
Valeur totale : 874.20 euros

Rechargé : 3 articles, 1 ligne(s) ignorée(s)
Valeur totale : 874.20 euros
```

L'en-tête `Quantité` paraît décalé d'un espace pour la même raison que précédemment : `%8s` compte les octets, et `é` en occupe deux.

## Étape 3 — Comprendre les choix de conception

| Fonction | Garantie de sûreté |
|---|---|
| `inv_ajouter` | refuse les quantités et prix négatifs et les noms trop longs ; `realloc` via un pointeur temporaire ; copie du nom avec `snprintf` |
| `inv_retirer` | refuse un article absent ou un stock insuffisant au lieu de passer en négatif |
| `inv_trouver` | renvoie -1 plutôt qu'un indice invalide |
| `inv_charger` | largeur `%31` dans `sscanf`, ligne mal formée ignorée et comptée |
| `inv_sauvegarder` | teste `fopen` et `fclose` |
| `inv_liberer` | libère et remet la structure à zéro : aucun pointeur pendant |

Chaque `fopen` a son `fclose`, chaque allocation est libérée par `inv_liberer`, sur **tous** les chemins de sortie de `main`, y compris celui d'erreur.

## Étape 4 — Vérifier avec les outils

Compilez avec tous les avertissements et les sanitizers, puis exécutez :

```bash
gcc -std=c17 -Wall -Wextra -Werror -g -fsanitize=address,undefined -o inventaire inventaire.c
./inventaire
```

Le programme doit afficher le même résultat **sans aucun rapport** d'ASan ou d'UBSan. Faites ensuite l'expérience : supprimez l'appel `inv_liberer(&copie);` à la fin de `main`, recompilez et relancez. Sous Linux, LeakSanitizer signale alors une fuite (`detected memory leaks`) et indique la ligne du `realloc` responsable. Remettez l'appel en place.

Vous pouvez aussi vérifier une version compilée **sans** sanitizer avec `valgrind --leak-check=full ./inventaire`.

## Étape 5 — Pour aller plus loin

Quelques améliorations à réaliser seul, dans l'ordre de difficulté :

1. **Supprimer un article** : décaler les articles suivants d'une case vers la gauche, puis décrémenter `taille`.
2. **Trier** l'inventaire par valeur décroissante avec la fonction standard `qsort` de `<stdlib.h>`.
3. **Menu interactif** : lire des commandes au clavier avec `fgets` (`ajouter Clavier 2 29.90`, `afficher`, `quitter`) et les analyser avec `sscanf`, en validant chaque saisie.
4. **Plusieurs fichiers** : déplacer les types et prototypes dans `inventaire.h`, les fonctions dans `inventaire.c`, et garder `main` dans `main.c`.

Voici deux pistes corrigées, sur un tableau simple d'articles pour rester court.

**Suppression par décalage** :

```c
#include <stdio.h>
#include <string.h>

typedef struct {
    char nom[32];
    int quantite;
} Article;

/* Supprime l'article d'indice i ; renvoie la nouvelle taille. */
size_t supprimer(Article *t, size_t n, size_t i)
{
    if (i >= n) {
        return n;                      /* indice invalide : rien à faire */
    }
    memmove(&t[i], &t[i + 1], (n - i - 1) * sizeof t[0]);
    return n - 1;
}

int main(void)
{
    Article t[] = {{"Clavier", 3}, {"Souris", 15}, {"Ecran", 3}};
    size_t n = supprimer(t, 3, 1);
    for (size_t i = 0; i < n; i++) {
        printf("%s (%d)\n", t[i].nom, t[i].quantite);
    }
    return 0;
}
```

```text
Clavier (3)
Ecran (3)
```

`memmove` copie un bloc d'octets en gérant correctement le cas où source et destination se chevauchent (ce que `memcpy` ne garantit pas).

**Tri avec `qsort`** : `qsort` reçoit le tableau, le nombre d'éléments, la taille d'un élément et une **fonction de comparaison** qui renvoie un nombre négatif, nul ou positif.

```c
#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char nom[32];
    int quantite;
    double prix;
} Article;

int comparer_valeur_desc(const void *a, const void *b)
{
    const Article *x = a;
    const Article *y = b;
    double vx = x->quantite * x->prix;
    double vy = y->quantite * y->prix;
    return (vx < vy) - (vx > vy);      /* ordre décroissant */
}

int main(void)
{
    Article t[] = {
        {"Clavier", 3, 29.90},
        {"Souris", 15, 14.50},
        {"Ecran", 3, 189.00},
    };
    size_t n = sizeof t / sizeof t[0];
    qsort(t, n, sizeof t[0], comparer_valeur_desc);
    for (size_t i = 0; i < n; i++) {
        printf("%-8s %7.2f\n", t[i].nom, t[i].quantite * t[i].prix);
    }
    return 0;
}
```

```text
Ecran     567.00
Souris    217.50
Clavier    89.70
```

L'expression `(vx < vy) - (vx > vy)` donne 1, 0 ou -1 sans risque de dépassement, contrairement à une soustraction convertie en `int`.

## À retenir

- Un programme C solide se construit avec des **fonctions courtes** qui vérifient leurs entrées et **signalent** leurs échecs.
- Chaque ressource (mémoire, fichier) a un propriétaire et est libérée sur tous les chemins.
- Les entrées externes (fichiers, saisies) sont lues avec des **largeurs** et **validées**.
- `-Wall -Wextra -Werror` et `-fsanitize=address,undefined` font partie du développement, pas d'une étape facultative.
- Bravo : vous savez maintenant écrire, compiler, déboguer et sécuriser un programme C complet.
"""

QUIZ_M3 = [
    ("single", "Un tableau déclaré int t[8] possède des cases d'indices…", None,
     ["1 à 8", "0 à 8", "0 à 7", "1 à 7"], [2],
     "Les indices commencent à 0 : un tableau de 8 cases va de t[0] à t[7]. t[8] est hors du tableau."),
    ("single", "Que se passe-t-il si un programme écrit dans t[10] alors que t ne compte que 5 cases ?", None,
     ["Le compilateur refuse de compiler", "Le tableau s'agrandit automatiquement", "Un comportement indéfini : corruption possible ou plantage", "L'écriture est ignorée"], [2],
     "Le C ne vérifie pas les indices : l'écriture touche la mémoire voisine. C'est un comportement indéfini, source de failles de sécurité."),
    ("single", "Qu'affiche ce programme ?", "#include <stdio.h>\n\nint main(void)\n{\n    int x = 4;\n    int *p = &x;\n    *p = *p * 3;\n    printf(\"%d\\n\", x);\n    return 0;\n}",
     ["4", "12", "L'adresse de x", "7"], [1],
     "p contient l'adresse de x : *p = *p * 3 modifie directement x, qui vaut 12."),
    ("multiple", "Quelles expressions désignent la même valeur que t[2] pour un tableau int t[5] ?", None,
     ["*(t + 2)", "*t + 2", "2[t]", "&t[2]"], [0, 2],
     "t[i] est défini comme *(t + i), donc aussi *(i + t), ce qui rend 2[t] valide (mais à éviter). *t + 2 ajoute 2 à t[0], et &t[2] est une adresse."),
    ("single", "Pourquoi une fonction qui reçoit un tableau doit-elle aussi recevoir sa taille ?", None,
     ["Parce qu'elle ne reçoit que l'adresse de la première case", "Parce que sizeof y est interdit", "Parce que les tableaux sont copiés", "Ce n'est pas nécessaire"], [0],
     "Le tableau est converti en pointeur vers sa première case : la fonction ne peut pas connaître le nombre d'éléments, sizeof y donne la taille d'une adresse."),
    ("single", "Combien d'octets faut-il pour stocker la chaîne \"Paris\" ?", None,
     ["5", "4", "6", "7"], [2],
     "5 caractères plus le caractère nul '\\0' qui termine la chaîne : 6 octets."),
    ("single", "Comment tester correctement si deux chaînes a et b ont le même contenu ?", None,
     ["a == b", "strcmp(a, b) == 0", "strlen(a) == strlen(b)", "*a == *b"], [1],
     "a == b compare deux adresses ; strlen ne compare que les longueurs et *a == *b le premier caractère. strcmp compare le contenu et renvoie 0 si les chaînes sont égales."),
    ("true_false", "snprintf(dest, sizeof dest, \"%s\", src) ne peut pas écrire au-delà du tableau dest et le termine toujours par '\\0'.", None,
     ["Vrai", "Faux"], [0],
     "snprintf reçoit la taille de la destination, tronque si nécessaire et ajoute le '\\0' (pour une taille non nulle). C'est la façon sûre de copier ou composer une chaîne."),
    ("single", "Que vaut un pointeur après la déclaration int *p; à l'intérieur d'une fonction ?", None,
     ["NULL", "L'adresse d'une variable libre", "Une valeur indéterminée : l'utiliser est un comportement indéfini", "0x0 garanti"], [2],
     "Une variable locale non initialisée, pointeur compris, contient une valeur imprévisible. Il faut l'initialiser avec une adresse valide ou NULL."),
    ("single", "Quelle fonction lire pour obtenir une ligne au clavier sans risque de débordement ?", None,
     ["gets", "fgets", "scanf(\"%s\", …)", "strcpy"], [1],
     "fgets reçoit la taille du tampon et n'écrit jamais au-delà. gets a été retirée du langage, scanf(\"%s\") sans largeur peut déborder."),
]

QUIZ_M4 = [
    ("single", "Que faut-il faire juste après un appel à malloc ?", None,
     ["Appeler free", "Appeler realloc", "Rien de particulier", "Tester si le résultat vaut NULL"], [3],
     "malloc renvoie NULL si la mémoire manque ; utiliser ce pointeur serait un comportement indéfini. On teste donc toujours le résultat."),
    ("single", "Quelle est la différence entre malloc et calloc ?", None,
     ["calloc met la zone allouée à zéro", "malloc alloue sur la pile", "calloc ne nécessite pas de free", "Aucune"], [0],
     "calloc(n, taille) alloue n éléments et les initialise à zéro ; malloc laisse un contenu indéterminé. Les deux nécessitent free."),
    ("single", "Pourquoi éviter t = realloc(t, nouvelle_taille); ?", None,
     ["realloc ne peut pas agrandir", "En cas d'échec, t devient NULL et l'ancienne zone est perdue (fuite)", "realloc libère toujours t", "Cela provoque une erreur de compilation"], [1],
     "Si realloc échoue, elle renvoie NULL sans libérer l'ancienne zone. Avec un pointeur temporaire, on garde l'adresse pour la libérer ou continuer."),
    ("multiple", "Lesquelles de ces situations sont des comportements indéfinis ?", None,
     ["Lire une zone après l'avoir libérée avec free", "Appeler free deux fois sur la même adresse", "Appeler free(NULL)", "Écrire une case après la fin d'une zone allouée"], [0, 1, 3],
     "free(NULL) est explicitement autorisé et ne fait rien. Les trois autres sont des comportements indéfinis : use after free, double free et dépassement."),
    ("single", "Comment accéder au champ prix d'une structure à partir d'un pointeur p vers cette structure ?", None,
     ["p.prix", "*p.prix", "p->prix", "&p.prix"], [2],
     "p->prix est l'abréviation de (*p).prix. *p.prix est interprété comme *(p.prix), ce qui est incorrect."),
    ("single", "Qu'est-ce qu'une fuite de mémoire ?", None,
     ["Une zone allouée jamais libérée et dont l'adresse est perdue", "Une écriture hors d'un tableau", "Un pointeur NULL", "Une variable non initialisée"], [0],
     "Une fuite survient quand une zone allouée n'est jamais rendue avec free ; la mémoire utilisée par le programme grossit inutilement."),
    ("single", "Quel outil s'active en ajoutant une option à la compilation pour détecter dépassements et use after free ?", None,
     ["Valgrind", "gdb", "-fsanitize=address", "-O2"], [2],
     "AddressSanitizer s'active avec -fsanitize=address. Valgrind s'utilise sans recompiler, gdb est un débogueur et -O2 une option d'optimisation."),
    ("true_false", "Copier une structure avec b = a; copie aussi la mémoire pointée par ses champs pointeurs.", None,
     ["Vrai", "Faux"], [1],
     "Seule l'adresse contenue dans un champ pointeur est copiée : a et b partagent alors la même zone, qu'il ne faut libérer qu'une fois."),
    ("single", "Pourquoi utiliser sizeof(struct …) plutôt que la somme des tailles des champs ?", None,
     ["Parce que sizeof est plus rapide", "Parce que les champs n'ont pas de taille", "Parce que le compilateur peut ajouter des octets de remplissage (padding)", "Il n'y a aucune différence possible"], [2],
     "Pour aligner les champs, le compilateur peut insérer du remplissage : la taille réelle peut dépasser la somme des champs. sizeof donne toujours la bonne valeur."),
    ("single", "Un programme passe tous ses tests sous AddressSanitizer sans rapport. Que peut-on en conclure ?", None,
     ["Qu'il ne contient aucune erreur mémoire", "Qu'aucune erreur détectable n'est survenue sur les chemins exécutés par ces tests", "Qu'il peut être compilé sans -Wall", "Qu'il ne contient aucun comportement indéfini"], [1],
     "Les sanitizers ne contrôlent que ce qui est réellement exécuté. D'autres entrées peuvent révéler des erreurs : il faut tester aussi les cas limites."),
]

QUIZ_M5 = [
    ("single", "Que renvoie fopen si le fichier ne peut pas être ouvert ?", None,
     ["0", "EOF", "NULL", "-1"], [2],
     "fopen renvoie un FILE * ; en cas d'échec, c'est NULL, qu'il faut tester avant toute lecture ou écriture."),
    ("single", "Quel mode d'ouverture ajoute des lignes à la fin d'un fichier sans effacer son contenu ?", None,
     ["\"w\"", "\"r\"", "\"r+\"", "\"a\""], [3],
     "Le mode \"a\" (append) écrit à la fin et crée le fichier s'il n'existe pas ; \"w\" efface le contenu existant."),
    ("single", "Pourquoi le résultat de fgetc doit-il être stocké dans un int plutôt qu'un char ?", None,
     ["Pour gagner de la mémoire", "Pour pouvoir distinguer EOF de tous les caractères valides", "Parce que fgetc renvoie un pointeur", "Ce n'est pas nécessaire"], [1],
     "fgetc renvoie soit un caractère (comme unsigned char converti en int), soit EOF, une valeur négative. Un char ne permet pas de les distinguer de façon fiable."),
    ("multiple", "Quelles pratiques sont correctes pour lire le fichier CSV « nom;quantité » dans char nom[32] ?", None,
     ["Lire chaque ligne avec fgets", "Analyser avec sscanf(ligne, \"%31[^;];%d\", nom, &q)", "Analyser avec sscanf(ligne, \"%[^;];%d\", nom, &q)", "Vérifier que sscanf renvoie 2"], [0, 1, 3],
     "Sans largeur, %[^;] peut déborder du tableau nom. fgets, la largeur 31 et le test du nombre de valeurs lues rendent la lecture sûre."),
    ("single", "Que fait fclose ?", None,
     ["Vide le tampon vers le disque et libère les ressources du flux", "Supprime le fichier", "Remet le fichier à zéro", "Ferme le programme"], [0],
     "fclose écrit les données encore en attente et libère le flux. Oublier fclose est une fuite de ressource."),
    ("single", "Avec strtol(texte, &fin, 10), comment savoir qu'il reste des caractères non numériques après le nombre ?", None,
     ["errno vaut ERANGE", "fin pointe sur un caractère différent de '\\0'", "strtol renvoie -1", "fin vaut NULL"], [1],
     "fin reçoit l'adresse du premier caractère non converti. S'il n'est pas le '\\0' final, le texte contenait autre chose qu'un nombre. ERANGE signale un dépassement."),
    ("true_false", "Un fichier binaire écrit avec fwrite à partir d'un tableau de structures est parfaitement portable entre toutes les machines.", None,
     ["Vrai", "Faux"], [1],
     "La taille des types, le remplissage des structures et l'ordre des octets peuvent varier : un format texte bien défini est préférable pour l'échange."),
    ("single", "Que renvoie fread ?", None,
     ["Le nombre d'octets du fichier", "Toujours 0 en cas de succès", "Un pointeur vers les données", "Le nombre d'éléments effectivement lus"], [3],
     "fread renvoie le nombre d'éléments complets lus, qui peut être inférieur à celui demandé (fin de fichier ou erreur) : il faut le vérifier."),
    ("single", "Dans une fonction qui ouvre deux fichiers, que faire si le second fopen échoue ?", None,
     ["Rien, le système fermera tout", "Appeler free sur le second pointeur", "Fermer le premier fichier avant de renvoyer une erreur", "Relancer fopen en boucle"], [2],
     "Le premier fichier est ouvert : chaque chemin de sortie doit libérer ce qui a été acquis, sinon la ressource fuit."),
    ("single", "Pourquoi memmove plutôt que memcpy pour décaler les éléments d'un tableau vers la gauche ?", None,
     ["memmove est la seule à copier des structures", "La source et la destination se chevauchent, cas que memcpy ne gère pas", "memcpy ne fonctionne que sur des chaînes", "memmove libère la mémoire"], [1],
     "Lors d'un décalage, les zones source et destination se recouvrent. memmove gère ce cas ; avec memcpy, le résultat serait un comportement indéfini."),
]
