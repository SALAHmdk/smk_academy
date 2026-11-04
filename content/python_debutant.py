"""Contenu de la formation « Python pour débutants » (SMK Academy).

Source de vérité du contenu pédagogique. `scripts/build_seed.py` transforme ce
fichier en migration SQL idempotente.

Convention Markdown des leçons :
- blocs ```python pour les exemples ;
- blocs ```solution pour les corrections d'exercices (affichées repliées).
"""

COURSE = {
    "slug": "python-debutant",
    "title": "Python pour débutants",
    "subtitle": "Écrivez vos premiers programmes, pas à pas.",
    "description": (
        "Une formation progressive pour apprendre à programmer avec Python, "
        "même sans aucune expérience. Chaque leçon combine explications, "
        "exemples de code commentés et exercices corrigés, puis un quiz noté "
        "sur 20 valide chaque module."
    ),
    "category": "Programmation",
    "level": "debutant",
    "duration_minutes": 660,
    "objectives": [
        "Écrire et exécuter un programme Python",
        "Manipuler variables, types et conversions",
        "Contrôler le déroulement d'un programme avec conditions et boucles",
        "Organiser son code avec des fonctions",
        "Lire et écrire des fichiers, gérer les erreurs",
    ],
    "prerequisites": [
        "Savoir utiliser un ordinateur et un navigateur",
        "Aucune connaissance en programmation n'est nécessaire",
    ],
    "status": "published",
    "is_premium": False,
    "position": 1,
}

OTHER_COURSES = [
    {
        "slug": "sql-debutant",
        "title": "SQL pour débutants",
        "subtitle": "Interrogez une base de données avec confiance.",
        "description": "SELECT, filtres, tris, jointures et agrégations sur des données réelles.",
        "category": "Bases de données",
        "level": "debutant",
        "duration_minutes": 480,
        "objectives": ["Écrire des requêtes SELECT", "Filtrer et trier", "Joindre des tables", "Agréger des données"],
        "prerequisites": ["Aucun"],
        "status": "coming_soon",
        "is_premium": False,
        "position": 2,
    },
    {
        "slug": "anglais-professionnel-debutant",
        "title": "Anglais professionnel — débutant",
        "subtitle": "Les bases pour communiquer au travail.",
        "description": "Se présenter, écrire un email simple, participer à une réunion.",
        "category": "Langues",
        "level": "debutant",
        "duration_minutes": 480,
        "objectives": ["Se présenter", "Écrire un email professionnel", "Comprendre une réunion simple"],
        "prerequisites": ["Niveau A1 conseillé"],
        "status": "coming_soon",
        "is_premium": False,
        "position": 3,
    },
]

M1_L1 = r"""
## Pourquoi Python ?

Python est un langage de programmation conçu pour être **lisible**. Son code ressemble presque à de l'anglais, ce qui en fait le langage idéal pour débuter. Il est pourtant utilisé par des professionnels partout : sites web, analyse de données, intelligence artificielle, automatisation de tâches, scripts d'administration…

Un **programme** est une suite d'instructions que l'ordinateur exécute dans l'ordre, de haut en bas. Le rôle de Python est de traduire ces instructions, écrites par un humain, en actions que la machine sait réaliser. On dit que Python est un langage **interprété** : vous écrivez le code, l'interpréteur Python le lit et l'exécute immédiatement, ligne après ligne.

## Où écrire du Python ?

Trois options s'offrent à vous :

1. **En ligne**, sans rien installer : des sites comme *Python Tutor* ou *Replit* exécutent votre code dans le navigateur. C'est parfait pour ce cours.
2. **Sur votre ordinateur** : téléchargez Python depuis `python.org` (version 3.12 ou plus récente), puis lancez `python` (ou `python3` sur macOS/Linux) dans un terminal.
3. **Dans un éditeur** comme VS Code, qui colore le code et signale les erreurs.

> Assurez-vous d'utiliser **Python 3**. Python 2 n'est plus maintenu depuis 2020.

## Votre premier programme

La fonction `print()` affiche du texte à l'écran. Le texte à afficher est placé entre guillemets : on appelle cela une **chaîne de caractères**.

```python
print("Bonjour, SMK Academy !")
```

Résultat :

```text
Bonjour, SMK Academy !
```

Vous pouvez afficher plusieurs éléments en les séparant par des virgules. Python insère alors un espace entre eux :

```python
print("J'apprends", "Python", "depuis", 1, "jour")
# Affiche : J'apprends Python depuis 1 jour
```

Chaque appel à `print()` passe à la ligne suivante :

```python
print("Ligne 1")
print("Ligne 2")
```

## Les commentaires

Tout ce qui suit le symbole `#` sur une ligne est un **commentaire** : Python l'ignore. Les commentaires servent à expliquer votre code aux humains, y compris à vous-même dans trois mois.

```python
# Ce programme salue l'utilisateur
print("Salut !")  # un commentaire peut aussi suivre une instruction
```

## Lire un message d'erreur

Faire des erreurs est normal : c'est même ainsi qu'on apprend. Si vous oubliez un guillemet, Python s'arrête et affiche un message :

```python
print("Bonjour)
```

```text
SyntaxError: unterminated string literal (detected at line 1)
```

Prenez l'habitude de **lire la dernière ligne** du message : elle indique le type d'erreur (`SyntaxError`, erreur de syntaxe) et souvent la ligne concernée. Ici, Python signale une chaîne de caractères qui n'a jamais été fermée.

Autre erreur fréquente : les majuscules. Python est **sensible à la casse** : `Print` et `print` sont deux noms différents.

```python
Print("Bonjour")
# NameError: name 'Print' is not defined
```

## À retenir

- Un programme est une suite d'instructions exécutées de haut en bas.
- `print()` affiche des valeurs ; le texte s'écrit entre guillemets.
- `#` introduit un commentaire ignoré par Python.
- Lisez la dernière ligne d'un message d'erreur : elle donne le type et la cause du problème.

## Exercices

### Exercice 1 — Carte de visite

Écrivez un programme qui affiche sur trois lignes votre prénom, la ville où vous habitez et la phrase `J'apprends Python avec SMK Academy`.

```solution
print("Prénom : Salah")
print("Ville : Paris")
print("J'apprends Python avec SMK Academy")
```

### Exercice 2 — Chasse aux erreurs

Le programme suivant contient trois erreurs. Trouvez-les et corrigez-les.

```python
print("Début du programme)
Print("Python est lisible")
print("Fin du programme"
```

```solution
print("Début du programme")   # guillemet fermant manquant
print("Python est lisible")   # print s'écrit en minuscules
print("Fin du programme")     # parenthèse fermante manquante
```
"""

M1_L2 = r"""
## Qu'est-ce qu'une variable ?

Une **variable** est un nom qui désigne une valeur stockée en mémoire. Imaginez une étiquette collée sur une boîte : l'étiquette est le nom, le contenu de la boîte est la valeur.

On crée une variable avec le signe `=`, appelé **opérateur d'affectation** :

```python
age = 25
prenom = "Amina"
print(prenom, "a", age, "ans")
# Affiche : Amina a 25 ans
```

Attention : en Python, `=` ne signifie pas « est égal à » comme en mathématiques. Il signifie « **range la valeur de droite dans le nom de gauche** ». C'est pourquoi on peut écrire :

```python
score = 10
score = score + 5   # on calcule score + 5, puis on range le résultat dans score
print(score)        # 15
```

Une variable peut changer de valeur au cours du programme : c'est pour cela qu'on l'appelle *variable*.

## Bien nommer ses variables

Règles obligatoires :

- un nom contient des lettres, des chiffres et le caractère `_` ;
- il ne commence **pas** par un chiffre ;
- il ne peut pas être un mot réservé de Python (`if`, `for`, `class`…).

Conventions recommandées :

- écrivez en minuscules et séparez les mots par `_` : `prix_total`, `nombre_eleves` (style *snake_case*) ;
- choisissez des noms **explicites** : `prix_ttc` est bien plus clair que `p` ou `x2`.

```python
nombre_de_lecons = 15    # correct et lisible
2eme_essai = 3           # SyntaxError : commence par un chiffre
```

## Les quatre types de base

Chaque valeur a un **type**, qui détermine ce qu'on peut faire avec elle.

| Type | Nom | Exemples |
|------|-----|----------|
| `int` | nombre entier | `42`, `-7`, `0` |
| `float` | nombre décimal | `3.14`, `-0.5`, `2.0` |
| `str` | chaîne de caractères | `"Python"`, `'Bonjour'` |
| `bool` | booléen | `True`, `False` |

Notez que les nombres décimaux s'écrivent avec un **point**, pas une virgule : `3.14` et non `3,14`.

La fonction `type()` indique le type d'une valeur :

```python
print(type(42))        # <class 'int'>
print(type(3.14))      # <class 'float'>
print(type("42"))      # <class 'str'>  — entre guillemets, c'est du texte !
print(type(True))      # <class 'bool'>
```

`42` et `"42"` sont deux valeurs très différentes : la première est un nombre, la seconde un texte composé des caractères `4` et `2`.

## Le type détermine les opérations possibles

```python
print(10 + 5)          # 15     : addition de nombres
print("10" + "5")      # 105    : concaténation (mise bout à bout) de textes
print("ha" * 3)        # hahaha : répétition d'un texte
```

Mélanger un texte et un nombre dans une addition provoque une erreur :

```python
print("Âge : " + 25)
# TypeError: can only concatenate str (not "int") to str
```

Nous verrons à la leçon suivante comment convertir une valeur d'un type à l'autre pour résoudre ce problème.

## Les booléens

Un booléen ne peut valoir que `True` (vrai) ou `False` (faux), avec une majuscule. Ils servent à représenter une réponse oui/non et seront essentiels pour les conditions du module 2.

```python
est_connecte = True
a_reussi_quiz = False
print(est_connecte)    # True
```

## À retenir

- `nom = valeur` range une valeur dans une variable ; la valeur peut changer ensuite.
- Noms en *snake_case*, explicites, sans chiffre au début.
- Quatre types de base : `int`, `float`, `str`, `bool`.
- `type()` révèle le type ; `"42"` (texte) n'est pas `42` (nombre).

## Exercices

### Exercice 1 — Fiche étudiant

Créez les variables `nom` (texte), `annee_naissance` (entier), `moyenne` (décimal) et `est_inscrit` (booléen), puis affichez chacune avec son type.

```solution
nom = "Yanis"
annee_naissance = 2003
moyenne = 14.5
est_inscrit = True

print(nom, type(nom))
print(annee_naissance, type(annee_naissance))
print(moyenne, type(moyenne))
print(est_inscrit, type(est_inscrit))
```

### Exercice 2 — Échanger deux valeurs

On a `a = 3` et `b = 8`. Écrivez le code qui échange leurs valeurs pour obtenir `a = 8` et `b = 3`, d'abord avec une variable intermédiaire, puis avec la syntaxe Python `a, b = b, a`.

```solution
a = 3
b = 8

# Méthode 1 : variable intermédiaire
temp = a
a = b
b = temp
print(a, b)   # 8 3

# Méthode 2 : affectation multiple (propre à Python)
a, b = b, a
print(a, b)   # 3 8 (on a ré-échangé)
```
"""

M1_L3 = r"""
## Demander une information : input()

`input()` affiche un message, attend que l'utilisateur tape quelque chose puis appuie sur Entrée, et **renvoie le texte saisi**.

```python
prenom = input("Comment vous appelez-vous ? ")
print("Enchanté,", prenom)
```

Point essentiel : `input()` renvoie **toujours une chaîne de caractères** (`str`), même si l'utilisateur tape un nombre.

```python
age = input("Votre âge ? ")   # l'utilisateur tape 20
print(type(age))              # <class 'str'>
print(age + 1)                # TypeError !
```

## Convertir entre les types

Pour transformer une valeur, on utilise le nom du type comme une fonction :

| Fonction | Convertit en | Exemple | Résultat |
|----------|--------------|---------|----------|
| `int()` | entier | `int("20")` | `20` |
| `float()` | décimal | `float("3.5")` | `3.5` |
| `str()` | texte | `str(42)` | `"42"` |

```python
age = int(input("Votre âge ? "))   # on convertit directement la saisie
print("L'an prochain, vous aurez", age + 1, "ans")
```

Si la conversion est impossible, Python lève une erreur :

```python
int("vingt")
# ValueError: invalid literal for int() with base 10: 'vingt'
```

`int()` appliqué à un décimal **tronque** (supprime la partie décimale) sans arrondir : `int(7.9)` vaut `7`.

## Les opérateurs arithmétiques

| Opérateur | Rôle | Exemple | Résultat |
|-----------|------|---------|----------|
| `+` | addition | `7 + 2` | `9` |
| `-` | soustraction | `7 - 2` | `5` |
| `*` | multiplication | `7 * 2` | `14` |
| `/` | division | `7 / 2` | `3.5` |
| `//` | division entière | `7 // 2` | `3` |
| `%` | reste (modulo) | `7 % 2` | `1` |
| `**` | puissance | `7 ** 2` | `49` |

Quelques remarques :

- `/` renvoie **toujours** un `float` : `8 / 2` vaut `4.0`.
- `//` et `%` vont ensemble : 7 = 2 × **3** + **1**.
- `%` est très utile pour savoir si un nombre est pair : `n % 2` vaut `0` pour un nombre pair.
- Les priorités sont celles des mathématiques ; utilisez des parenthèses en cas de doute : `(2 + 3) * 4` vaut `20`.

```python
minutes_totales = 135
heures = minutes_totales // 60    # 2
minutes = minutes_totales % 60    # 15
print(heures, "h", minutes, "min")
```

## Mettre en forme avec les f-strings

Une **f-string** est une chaîne précédée de la lettre `f`. Tout ce qui est entre accolades `{}` est remplacé par sa valeur :

```python
prenom = "Lina"
note = 15.456
print(f"{prenom} a obtenu {note} sur 20")
# Lina a obtenu 15.456 sur 20

print(f"Note arrondie : {note:.1f}/20")
# Note arrondie : 15.5/20
```

Le format `:.1f` affiche le nombre avec une décimale, `:.2f` avec deux. Les f-strings évitent les conversions manuelles avec `str()` et rendent le code bien plus lisible.

## Un programme complet

```python
# Calcul du prix TTC
prix_ht = float(input("Prix HT (€) : "))
taux_tva = 20

tva = prix_ht * taux_tva / 100
prix_ttc = prix_ht + tva

print(f"TVA : {tva:.2f} €")
print(f"Prix TTC : {prix_ttc:.2f} €")
```

## À retenir

- `input()` renvoie toujours du texte : convertissez avec `int()` ou `float()`.
- `/` donne un décimal, `//` le quotient entier, `%` le reste.
- Les f-strings `f"... {valeur} ..."` insèrent des valeurs dans un texte ; `:.2f` fixe le nombre de décimales.

## Exercices

### Exercice 1 — Convertisseur de durée

Demandez un nombre de secondes à l'utilisateur et affichez l'équivalent en heures, minutes et secondes. Exemple : `3725` → `1 h 2 min 5 s`.

```solution
total = int(input("Nombre de secondes : "))

heures = total // 3600
reste = total % 3600
minutes = reste // 60
secondes = reste % 60

print(f"{heures} h {minutes} min {secondes} s")
```

### Exercice 2 — Moyenne de trois notes

Demandez trois notes sur 20 (elles peuvent être décimales) et affichez la moyenne avec deux décimales.

```solution
note1 = float(input("Note 1 : "))
note2 = float(input("Note 2 : "))
note3 = float(input("Note 3 : "))

moyenne = (note1 + note2 + note3) / 3
print(f"Moyenne : {moyenne:.2f}/20")
```
"""

M2_L1 = r"""
## Prendre des décisions

Jusqu'ici, nos programmes exécutaient toutes leurs instructions, dans l'ordre. Une **condition** permet d'exécuter un bloc de code **seulement si** une affirmation est vraie.

```python
note = 14
if note >= 10:
    print("Module validé !")
print("Fin du programme")
```

Deux éléments de syntaxe sont indispensables :

1. les **deux-points** `:` à la fin de la ligne `if` ;
2. l'**indentation** (4 espaces) des instructions qui dépendent de la condition.

L'indentation n'est pas décorative en Python : c'est elle qui délimite le bloc. Une indentation incorrecte provoque une `IndentationError`.

## Les opérateurs de comparaison

Une comparaison produit un booléen, `True` ou `False` :

| Opérateur | Signification | Exemple | Résultat |
|-----------|---------------|---------|----------|
| `==` | égal à | `5 == 5` | `True` |
| `!=` | différent de | `5 != 3` | `True` |
| `<` | strictement inférieur | `3 < 5` | `True` |
| `<=` | inférieur ou égal | `5 <= 5` | `True` |
| `>` | strictement supérieur | `3 > 5` | `False` |
| `>=` | supérieur ou égal | `3 >= 5` | `False` |

Ne confondez pas `=` (affectation) et `==` (comparaison) : c'est l'erreur la plus fréquente des débutants.

## if, elif, else

`else` (« sinon ») s'exécute quand la condition est fausse. `elif` (contraction de *else if*) teste une nouvelle condition si les précédentes étaient fausses.

```python
note = float(input("Votre note sur 20 : "))

if note >= 16:
    mention = "Très bien"
elif note >= 14:
    mention = "Bien"
elif note >= 12:
    mention = "Assez bien"
elif note >= 10:
    mention = "Passable"
else:
    mention = "Non validé"

print(f"Résultat : {mention}")
```

Python teste les conditions **de haut en bas** et n'exécute que le **premier** bloc dont la condition est vraie. Avec une note de 15, seul le bloc `"Bien"` s'exécute, même si `note >= 12` est aussi vrai. L'ordre des `elif` est donc important.

## Combiner des conditions : and, or, not

- `a and b` est vrai si **les deux** sont vrais ;
- `a or b` est vrai si **au moins un** est vrai ;
- `not a` inverse la valeur.

```python
age = 20
a_un_compte = True

if age >= 18 and a_un_compte:
    print("Accès autorisé")

jour = "samedi"
if jour == "samedi" or jour == "dimanche":
    print("C'est le week-end")

if not a_un_compte:
    print("Créez un compte pour continuer")
```

Python permet aussi d'enchaîner les comparaisons, comme en mathématiques :

```python
note = 12
if 0 <= note <= 20:
    print("Note valide")
```

## Comparer des textes

Les comparaisons fonctionnent aussi sur les chaînes, en tenant compte des majuscules :

```python
reponse = input("Voulez-vous continuer ? (oui/non) ")
if reponse.lower() == "oui":
    print("C'est parti !")
```

La méthode `.lower()` convertit le texte en minuscules : ainsi `"OUI"`, `"Oui"` et `"oui"` sont acceptés.

## À retenir

- `if condition:` suivi d'un bloc indenté de 4 espaces.
- `elif` et `else` traitent les autres cas ; seul le premier bloc vrai s'exécute.
- `==` compare, `=` affecte.
- `and`, `or`, `not` combinent des conditions.

## Exercices

### Exercice 1 — Pair ou impair

Demandez un entier et affichez s'il est pair ou impair.

```solution
n = int(input("Entrez un entier : "))
if n % 2 == 0:
    print(f"{n} est pair")
else:
    print(f"{n} est impair")
```

### Exercice 2 — Tarif de cinéma

Le billet coûte 12 €. Les moins de 14 ans paient 6 €, les 14-25 ans et les plus de 65 ans paient 8 €. Demandez l'âge et affichez le tarif.

```solution
age = int(input("Votre âge : "))

if age < 14:
    prix = 6
elif age <= 25 or age > 65:
    prix = 8
else:
    prix = 12

print(f"Tarif : {prix} €")
```
"""

M2_L2 = r"""
## Répéter tant qu'une condition est vraie

Une **boucle** répète un bloc d'instructions. La boucle `while` (« tant que ») répète son bloc **tant que** sa condition est vraie.

```python
compteur = 1
while compteur <= 5:
    print("Tour", compteur)
    compteur = compteur + 1
print("Terminé")
```

```text
Tour 1
Tour 2
Tour 3
Tour 4
Tour 5
Terminé
```

Le déroulement est le suivant : Python teste la condition ; si elle est vraie, il exécute le bloc puis **revient tester** la condition ; dès qu'elle est fausse, il passe à la suite du programme.

## L'écriture raccourcie +=

Augmenter une variable est si courant que Python propose un raccourci :

```python
compteur += 1     # équivaut à compteur = compteur + 1
total -= 5        # total = total - 5
prix *= 2         # prix = prix * 2
```

## Attention aux boucles infinies

Si la condition ne devient jamais fausse, la boucle ne s'arrête jamais :

```python
compteur = 1
while compteur <= 5:
    print(compteur)
    # oubli de compteur += 1 : la boucle tourne indéfiniment !
```

Si cela vous arrive, interrompez le programme avec **Ctrl + C** dans le terminal. Avant d'écrire un `while`, demandez-vous toujours : *qu'est-ce qui fera devenir la condition fausse ?*

## Cas d'usage typique : valider une saisie

`while` est idéal quand on ne sait pas à l'avance combien de répétitions seront nécessaires, par exemple pour redemander une saisie tant qu'elle est incorrecte :

```python
note = float(input("Note sur 20 : "))
while note < 0 or note > 20:
    print("La note doit être comprise entre 0 et 20.")
    note = float(input("Note sur 20 : "))
print(f"Note enregistrée : {note}")
```

## Accumuler un résultat

Une boucle sert souvent à construire un résultat petit à petit dans une variable appelée **accumulateur** :

```python
# Somme des entiers de 1 à 100
somme = 0
n = 1
while n <= 100:
    somme += n
    n += 1
print(somme)   # 5050
```

## Interrompre une boucle : break

L'instruction `break` quitte immédiatement la boucle. Combinée à `while True` (une condition toujours vraie), elle permet d'écrire des boucles dont la sortie se décide à l'intérieur :

```python
secret = 7
while True:
    essai = int(input("Devinez le nombre (1-10) : "))
    if essai == secret:
        print("Bravo !")
        break
    print("Raté, réessayez.")
```

## À retenir

- `while condition:` répète le bloc tant que la condition est vraie.
- Vérifiez que la condition finira par devenir fausse, sinon la boucle est infinie (Ctrl + C pour l'arrêter).
- `+=`, `-=`, `*=` modifient une variable de façon concise.
- `break` sort immédiatement de la boucle.

## Exercices

### Exercice 1 — Compte à rebours

Affichez un compte à rebours de 10 à 1, puis le message `Décollage !`.

```solution
n = 10
while n >= 1:
    print(n)
    n -= 1
print("Décollage !")
```

### Exercice 2 — Moyenne d'une série de notes

Demandez des notes jusqu'à ce que l'utilisateur tape `-1`. Affichez ensuite le nombre de notes saisies et leur moyenne (si au moins une note a été saisie).

```solution
somme = 0
nombre = 0

note = float(input("Note (-1 pour terminer) : "))
while note != -1:
    somme += note
    nombre += 1
    note = float(input("Note (-1 pour terminer) : "))

if nombre > 0:
    print(f"{nombre} notes, moyenne : {somme / nombre:.2f}/20")
else:
    print("Aucune note saisie.")
```
"""

M2_L3 = r"""
## Parcourir une séquence

La boucle `for` parcourt les éléments d'une séquence, un par un. Une chaîne de caractères est une séquence de caractères :

```python
for lettre in "SMK":
    print(lettre)
```

```text
S
M
K
```

À chaque tour, la variable `lettre` prend la valeur de l'élément suivant. La boucle s'arrête d'elle-même à la fin de la séquence : pas de risque de boucle infinie.

## range() : générer des nombres

`range()` produit une suite d'entiers, ce qui permet de répéter une action un nombre précis de fois.

| Appel | Nombres produits |
|-------|------------------|
| `range(5)` | 0, 1, 2, 3, 4 |
| `range(1, 6)` | 1, 2, 3, 4, 5 |
| `range(0, 11, 2)` | 0, 2, 4, 6, 8, 10 |
| `range(5, 0, -1)` | 5, 4, 3, 2, 1 |

La borne de fin est toujours **exclue** : `range(1, 6)` s'arrête à 5.

```python
for i in range(1, 4):
    print(f"Leçon {i}")
```

## for ou while ?

- **`for`** quand on connaît le nombre de répétitions ou qu'on parcourt une séquence ;
- **`while`** quand la répétition dépend d'une condition imprévisible (saisie de l'utilisateur, jeu…).

Comparez la somme de 1 à 100, beaucoup plus concise avec `for` :

```python
somme = 0
for n in range(1, 101):
    somme += n
print(somme)   # 5050
```

## break et continue

- `break` quitte la boucle immédiatement ;
- `continue` passe directement au tour suivant.

```python
# Afficher les nombres de 1 à 10 sauf les multiples de 3
for n in range(1, 11):
    if n % 3 == 0:
        continue
    print(n)
```

```python
# Trouver le premier multiple de 7 supérieur à 50
for n in range(51, 100):
    if n % 7 == 0:
        print(n)   # 56
        break
```

## Boucles imbriquées

Une boucle peut en contenir une autre. La boucle intérieure s'exécute entièrement à chaque tour de la boucle extérieure :

```python
for ligne in range(1, 4):
    for colonne in range(1, 4):
        print(ligne * colonne, end="\t")
    print()
```

```text
1	2	3
2	4	6
3	6	9
```

Le paramètre `end="\t"` remplace le retour à la ligne de `print()` par une tabulation ; le `print()` vide final passe à la ligne.

## À retenir

- `for element in sequence:` parcourt chaque élément.
- `range(debut, fin, pas)` génère des entiers ; `fin` est exclue.
- `for` pour un nombre connu de tours, `while` pour une condition.
- `continue` saute au tour suivant, `break` sort de la boucle.

## Exercices

### Exercice 1 — Table de multiplication

Demandez un nombre et affichez sa table de multiplication de 1 à 10, au format `7 x 3 = 21`.

```solution
n = int(input("Quelle table ? "))
for i in range(1, 11):
    print(f"{n} x {i} = {n * i}")
```

### Exercice 2 — Compter les voyelles

Demandez une phrase et affichez le nombre de voyelles (a, e, i, o, u, y) qu'elle contient, sans tenir compte des majuscules.

```solution
phrase = input("Votre phrase : ")
voyelles = 0
for caractere in phrase.lower():
    if caractere in "aeiouy":
        voyelles += 1
print(f"Nombre de voyelles : {voyelles}")
```

> L'opérateur `in` teste si un caractère appartient à une chaîne : `"a" in "aeiouy"` vaut `True`.
"""

# Modules 3 à 5 : contenu dans un fichier séparé pour rester lisible.
import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("python_debutant_m3_m5", _Path(__file__).with_name("python_debutant_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

# Quiz : (kind, prompt, code, [options], [indices des bonnes réponses], explication)
QUIZ_M1 = [
    ("single", "Qu'affiche ce programme ?", 'print("2" + "3")',
     ["5", "23", "Une erreur", "2 3"], [1],
     "Les guillemets font de \"2\" et \"3\" des chaînes : + les met bout à bout (concaténation) et produit \"23\"."),
    ("single", "Quel est le type de la valeur renvoyée par input() ?", None,
     ["int", "float", "str", "Cela dépend de ce que tape l'utilisateur"], [2],
     "input() renvoie toujours une chaîne (str). Il faut la convertir avec int() ou float() pour calculer."),
    ("single", "Combien vaut l'expression 17 // 5 ?", None,
     ["3.4", "3", "2", "4"], [1],
     "// est la division entière : 17 = 5 × 3 + 2, le quotient entier est 3."),
    ("single", "Combien vaut l'expression 17 % 5 ?", None,
     ["2", "3", "3.4", "0"], [0],
     "% donne le reste de la division entière : 17 = 5 × 3 + 2, le reste est 2."),
    ("multiple", "Parmi ces noms de variables, lesquels sont valides en Python ?", None,
     ["prix_total", "2eme_note", "_compteur", "nombre-eleves"], [0, 2],
     "Un nom contient lettres, chiffres et _ et ne commence pas par un chiffre. 2eme_note commence par un chiffre ; nombre-eleves contient un tiret, interprété comme une soustraction."),
    ("true_false", "Python ignore tout ce qui suit le symbole # sur une ligne.", None,
     ["Vrai", "Faux"], [0],
     "# introduit un commentaire : il sert aux humains et n'est jamais exécuté."),
    ("single", "Qu'affiche ce programme ?", 'note = 15.456\nprint(f"{note:.1f}")',
     ["15.4", "15.5", "15.456", "{note:.1f}"], [1],
     "Le format :.1f arrondit à une décimale : 15.456 devient 15.5."),
    ("multiple", "Quelles expressions produisent une erreur ?", None,
     ['"Âge : " + 25', 'int("vingt")', 'int("20") + 1', 'str(25) + " ans"'], [0, 1],
     "On ne peut pas additionner un str et un int (TypeError), et \"vingt\" ne peut pas être converti en entier (ValueError). Les deux autres expressions sont correctes."),
    ("true_false", "L'expression 8 / 2 renvoie l'entier 4.", None,
     ["Vrai", "Faux"], [1],
     "L'opérateur / renvoie toujours un float : 8 / 2 vaut 4.0. Pour un entier, utilisez 8 // 2."),
    ("single", "Après ces instructions, que vaut score ?", "score = 10\nscore = score + 5\nscore = score * 2",
     ["10", "15", "20", "30"], [3],
     "score vaut d'abord 10, puis 10 + 5 = 15, puis 15 × 2 = 30. Chaque affectation remplace l'ancienne valeur."),
]

QUIZ_M2 = [
    ("single", "Quel opérateur teste l'égalité de deux valeurs ?", None,
     ["=", "==", "===", "equals"], [1],
     "== compare deux valeurs. Un seul = est l'opérateur d'affectation."),
    ("single", "Qu'affiche ce programme ?", 'note = 15\nif note >= 12:\n    print("A")\nelif note >= 14:\n    print("B")\nelse:\n    print("C")',
     ["A", "B", "A puis B", "C"], [0],
     "Python exécute seulement le premier bloc dont la condition est vraie. note >= 12 est vrai, donc il affiche A et ignore la suite, même si note >= 14 est aussi vrai."),
    ("single", "Quels nombres produit range(2, 8, 2) ?", None,
     ["2, 4, 6, 8", "2, 4, 6", "2, 3, 4, 5, 6, 7", "4, 6, 8"], [1],
     "range part de 2, avance de 2 en 2 et s'arrête avant 8 (borne exclue) : 2, 4, 6."),
    ("true_false", "Une boucle while dont la condition ne devient jamais fausse s'exécute indéfiniment.", None,
     ["Vrai", "Faux"], [0],
     "C'est une boucle infinie. Il faut s'assurer que le bloc modifie ce que teste la condition (ou utiliser break)."),
    ("multiple", "Quelles conditions sont vraies lorsque age = 20 ?", None,
     ["age >= 18 and age < 25", "age < 18 or age > 65", "not age == 20", "18 <= age <= 30"], [0, 3],
     "20 est bien entre 18 et 25, et entre 18 et 30. Il n'est ni < 18 ni > 65, et not (age == 20) vaut False."),
    ("single", "Combien de fois le mot « SMK » est-il affiché ?", 'for i in range(3):\n    for j in range(2):\n        print("SMK")',
     ["2", "3", "5", "6"], [3],
     "La boucle intérieure (2 tours) s'exécute entièrement à chacun des 3 tours de la boucle extérieure : 3 × 2 = 6."),
    ("single", "Qu'affiche ce programme ?", "for n in range(1, 6):\n    if n == 3:\n        continue\n    print(n, end=' ')",
     ["1 2", "1 2 3 4 5", "1 2 4 5", "3"], [2],
     "continue saute la suite du bloc pour n = 3 et passe au tour suivant : 3 n'est pas affiché."),
    ("true_false", "En Python, l'indentation du bloc qui suit un if est facultative.", None,
     ["Vrai", "Faux"], [1],
     "L'indentation est obligatoire : c'est elle qui délimite le bloc. Sans elle, Python lève une IndentationError."),
    ("single", "Après cette boucle, que vaut total ?", "total = 0\nn = 1\nwhile n <= 4:\n    total += n\n    n += 1",
     ["4", "6", "10", "15"], [2],
     "La boucle ajoute 1, 2, 3 puis 4 : total = 1 + 2 + 3 + 4 = 10."),
    ("multiple", "Dans quelles situations une boucle while est-elle plus adaptée qu'une boucle for ?", None,
     ["Redemander une saisie tant qu'elle est invalide",
      "Afficher les nombres de 1 à 100",
      "Faire jouer l'utilisateur jusqu'à ce qu'il trouve le nombre secret",
      "Parcourir chaque lettre d'un mot"], [0, 2],
     "while convient quand le nombre de tours dépend d'une condition imprévisible. Pour un nombre connu de tours ou une séquence, for est plus simple."),
]

MODULES = [
    {
        "position": 1,
        "title": "Premiers pas avec Python",
        "description": "Écrire et exécuter un programme, utiliser variables, types et opérations.",
        "status": "published",
        "lessons": [
            ("decouvrir-python", "Découvrir Python et écrire son premier programme",
             "print(), commentaires et lecture des messages d'erreur.", M1_L1, 20),
            ("variables-et-types", "Variables et types de base",
             "Stocker des valeurs, bien les nommer, connaître int, float, str et bool.", M1_L2, 25),
            ("saisie-conversions-operations", "Saisie, conversions et opérations",
             "input(), conversions de types, opérateurs arithmétiques et f-strings.", M1_L3, 30),
        ],
        "quiz": ("Quiz — Premiers pas avec Python", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Conditions et boucles",
        "description": "Prendre des décisions et répéter des actions.",
        "status": "published",
        "lessons": [
            ("conditions", "Les conditions : if, elif, else",
             "Comparaisons, opérateurs logiques et choix multiples.", M2_L1, 25),
            ("boucle-while", "La boucle while",
             "Répéter tant qu'une condition est vraie, valider une saisie, accumuler.", M2_L2, 25),
            ("boucle-for", "La boucle for et range()",
             "Parcourir une séquence, compter, break et continue.", M2_L3, 30),
        ],
        "quiz": ("Quiz — Conditions et boucles", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Listes, tuples et dictionnaires",
        "description": "Stocker et manipuler des collections de données.",
        "status": "published",
        "lessons": [
            ("listes", "Les listes", "Créer, lire, modifier et parcourir une liste.", _m35.M3_L1, 25),
            ("tuples-et-sequences", "Tuples et parcours de séquences",
             "Tuples, déballage, enumerate(), zip(), split() et join().", _m35.M3_L2, 25),
            ("dictionnaires", "Les dictionnaires", "Associer des clés à des valeurs, compter, combiner.", _m35.M3_L3, 25),
        ],
        "quiz": ("Quiz — Listes, tuples et dictionnaires", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Les fonctions",
        "description": "Découper un programme en blocs réutilisables.",
        "status": "published",
        "lessons": [
            ("definir-une-fonction", "Définir et appeler une fonction", "def, paramètres et return.", _m35.M4_L1, 25),
            ("parametres-et-portee", "Paramètres, portée et documentation",
             "Valeurs par défaut, arguments nommés, variables locales, docstrings.", _m35.M4_L2, 25),
            ("modules-et-decomposition", "Modules et découpage d'un programme",
             "import, math, random, fonctions courtes et tests avec assert.", _m35.M4_L3, 30),
        ],
        "quiz": ("Quiz — Les fonctions", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Fichiers, erreurs et mini-projet",
        "description": "Lire et écrire des fichiers, gérer les exceptions, réaliser un projet complet.",
        "status": "published",
        "lessons": [
            ("gerer-les-erreurs", "Gérer les erreurs", "try, except, else, finally et raise.", _m35.M5_L1, 25),
            ("lire-et-ecrire-des-fichiers", "Lire et écrire des fichiers",
             "open, with, modes r/w/a, lecture ligne par ligne.", _m35.M5_L2, 25),
            ("mini-projet-carnet-de-notes", "Mini-projet : un carnet de notes",
             "Assembler toute la formation dans un programme complet.", _m35.M5_L3, 45),
        ],
        "quiz": ("Quiz — Fichiers et erreurs", _m35.QUIZ_M5),
    },
]
