"""Python pour débutants — modules 3 à 5 (leçons et quiz).

Importé par content/python_debutant.py. Mêmes conventions Markdown :
```python pour les exemples, ```text pour les sorties, ```solution pour les corrections.
"""

M3_L1 = r"""
## Ranger plusieurs valeurs ensemble

Jusqu'ici, une variable contenait une seule valeur. Pour stocker les notes d'une classe, les étapes d'une recette ou les produits d'un panier, on utilise une **liste** : une suite ordonnée de valeurs, écrite entre crochets et séparée par des virgules.

```python
notes = [12, 15.5, 9, 17]
prenoms = ["Amina", "Yanis", "Lina"]
vide = []
print(notes)        # [12, 15.5, 9, 17]
print(len(notes))   # 4 : len() donne le nombre d'éléments
```

Une liste peut contenir des valeurs de types différents, mais en pratique on y range des éléments de même nature.

## Accéder à un élément : l'indice

Chaque élément a une position appelée **indice**. Attention : on commence à compter à **0**.

```python
prenoms = ["Amina", "Yanis", "Lina"]
print(prenoms[0])    # Amina   (premier élément)
print(prenoms[2])    # Lina    (troisième élément)
print(prenoms[-1])   # Lina    (indice négatif : on part de la fin)
```

Demander un indice qui n'existe pas provoque une erreur :

```python
print(prenoms[3])
# IndexError: list index out of range
```

Pour une liste de longueur `n`, les indices valides vont de `0` à `n - 1`.

## Extraire une partie : les tranches

La syntaxe `liste[debut:fin]` renvoie une nouvelle liste, de `debut` inclus à `fin` **exclu** (comme `range`).

```python
lettres = ["a", "b", "c", "d", "e"]
print(lettres[1:3])   # ['b', 'c']
print(lettres[:2])    # ['a', 'b']        depuis le début
print(lettres[3:])    # ['d', 'e']        jusqu'à la fin
```

## Modifier une liste

Contrairement à une chaîne de caractères, une liste est **modifiable** (on dit *mutable*) :

```python
courses = ["pain", "lait"]
courses[1] = "beurre"        # remplace l'élément d'indice 1
courses.append("œufs")       # ajoute à la fin
courses.insert(0, "café")    # insère à l'indice 0
print(courses)               # ['café', 'pain', 'beurre', 'œufs']

courses.remove("pain")       # retire la première occurrence de "pain"
dernier = courses.pop()      # retire et renvoie le dernier élément
print(dernier)               # œufs
print(courses)               # ['café', 'beurre']
```

`append`, `insert`, `remove` et `pop` sont des **méthodes** : des fonctions attachées à la liste, appelées avec un point.

## Parcourir et tester

La boucle `for` parcourt une liste élément par élément, et `in` teste l'appartenance :

```python
notes = [12, 15.5, 9, 17]
total = 0
for note in notes:
    total += note
print(f"Moyenne : {total / len(notes):.2f}")   # Moyenne : 13.38

if 9 in notes:
    print("Au moins une note sous la moyenne")
```

Python fournit aussi des fonctions toutes prêtes : `sum(notes)`, `min(notes)`, `max(notes)`, et `sorted(notes)` qui renvoie une copie triée.

```python
print(sum(notes) / len(notes))   # 13.375
print(max(notes))                # 17
print(sorted(notes))             # [9, 12, 15.5, 17]
```

## À retenir

- Une liste s'écrit `[a, b, c]` ; `len()` donne sa longueur.
- Les indices commencent à 0 ; `-1` désigne le dernier élément.
- `liste[debut:fin]` extrait une tranche, `fin` exclue.
- `append`, `insert`, `remove`, `pop` modifient la liste ; `sum`, `min`, `max`, `sorted` l'analysent.

## Exercices

### Exercice 1 — Statistiques d'une classe

À partir de `notes = [14, 8, 17.5, 11, 9.5, 16]`, affichez le nombre de notes, la moyenne (2 décimales), la meilleure et la moins bonne note.

```solution
notes = [14, 8, 17.5, 11, 9.5, 16]

print("Nombre de notes :", len(notes))
print(f"Moyenne : {sum(notes) / len(notes):.2f}")
print("Meilleure note :", max(notes))
print("Moins bonne note :", min(notes))
```

### Exercice 2 — Liste de tâches

Créez une liste vide `taches`. Demandez trois tâches à l'utilisateur et ajoutez-les avec `append`. Retirez ensuite la première tâche (elle est terminée) et affichez les tâches restantes, une par ligne.

```solution
taches = []
for i in range(3):
    tache = input(f"Tâche {i + 1} : ")
    taches.append(tache)

taches.pop(0)   # pop accepte un indice : retire la première tâche

for tache in taches:
    print("-", tache)
```
"""

M3_L2 = r"""
## Le tuple : une séquence qui ne change pas

Un **tuple** ressemble à une liste, mais s'écrit entre parenthèses et **ne peut pas être modifié** après sa création (*immuable*). On l'utilise pour des données qui vont ensemble et ne doivent pas changer : des coordonnées, une date, une couleur RVB.

```python
point = (3, 7)
date = (14, "juillet", 1789)
print(point[0])      # 3   : même accès par indice qu'une liste
print(len(date))     # 3

point[0] = 5
# TypeError: 'tuple' object does not support item assignment
```

Un tuple d'un seul élément s'écrit avec une virgule : `(5,)`. Sans virgule, `(5)` est simplement le nombre 5 entre parenthèses.

## Le déballage

On peut répartir les éléments d'un tuple (ou d'une liste) dans plusieurs variables en une seule ligne :

```python
point = (3, 7)
x, y = point
print(x, y)          # 3 7

jour, mois, annee = (14, "juillet", 1789)
print(mois)          # juillet
```

C'est ce mécanisme qui permet l'échange de valeurs `a, b = b, a` vu au module 1 : à droite, Python crée le tuple `(b, a)`, puis le déballe dans `a` et `b`.

Une fonction peut aussi renvoyer plusieurs valeurs sous forme de tuple ; vous le verrez au module 4.

## Parcourir avec l'indice : enumerate()

Quand on a besoin à la fois de la position et de la valeur, `enumerate()` fournit des paires `(indice, élément)` :

```python
podium = ["Lina", "Yanis", "Amina"]
for position, prenom in enumerate(podium, start=1):
    print(f"{position}. {prenom}")
```

```text
1. Lina
2. Yanis
3. Amina
```

C'est plus lisible et plus sûr que de gérer un compteur à la main.

## Parcourir deux listes ensemble : zip()

`zip()` associe les éléments de même position de plusieurs séquences :

```python
eleves = ["Lina", "Yanis", "Amina"]
notes = [16, 11, 14]

for eleve, note in zip(eleves, notes):
    print(f"{eleve} : {note}/20")
```

```text
Lina : 16/20
Yanis : 11/20
Amina : 14/20
```

Si les séquences n'ont pas la même longueur, `zip()` s'arrête à la plus courte.

## Les chaînes sont aussi des séquences

Une chaîne se comporte comme un tuple de caractères : indices, tranches, `len()`, `in` et `for` fonctionnent, et elle est immuable.

```python
mot = "Python"
print(mot[0], mot[-1])   # P n
print(mot[1:4])          # yth
```

Deux méthodes très utiles relient chaînes et listes :

```python
phrase = "apprendre coder progresser"
mots = phrase.split()        # découpe sur les espaces
print(mots)                  # ['apprendre', 'coder', 'progresser']

print(" - ".join(mots))      # apprendre - coder - progresser
```

`split(";")` découpe sur un autre séparateur, ce qui servira pour lire des fichiers au module 5.

## Liste ou tuple ?

- **Liste** : une collection qui évolue (ajouts, suppressions, tri).
- **Tuple** : un petit groupe de valeurs fixes qui décrivent une même chose.

## À retenir

- Un tuple `(a, b)` s'utilise comme une liste mais ne se modifie pas.
- Le déballage `x, y = point` répartit les valeurs dans des variables.
- `enumerate()` donne indice et valeur ; `zip()` parcourt plusieurs séquences en parallèle.
- `split()` transforme une chaîne en liste, `join()` fait l'inverse.

## Exercices

### Exercice 1 — Bulletin

Avec `matieres = ["Maths", "Français", "Anglais"]` et `notes = [15, 12, 17]`, affichez chaque matière avec sa note, puis la matière où la note est la plus haute.

```solution
matieres = ["Maths", "Français", "Anglais"]
notes = [15, 12, 17]

for matiere, note in zip(matieres, notes):
    print(f"{matiere} : {note}/20")

meilleure = max(notes)
indice = notes.index(meilleure)   # position de la meilleure note
print("Meilleure matière :", matieres[indice])
```

### Exercice 2 — Compter les mots

Demandez une phrase, puis affichez le nombre de mots et le mot le plus long.

```solution
phrase = input("Votre phrase : ")
mots = phrase.split()

print("Nombre de mots :", len(mots))

plus_long = ""
for mot in mots:
    if len(mot) > len(plus_long):
        plus_long = mot
print("Mot le plus long :", plus_long)
```
"""

M3_L3 = r"""
## Retrouver une valeur par son nom

Une liste range des valeurs par position. Mais pour un annuaire, on veut retrouver un numéro à partir d'un **nom**, pas d'un indice. C'est le rôle du **dictionnaire** : un ensemble de paires **clé : valeur**, écrit entre accolades.

```python
etudiant = {
    "nom": "Amina",
    "age": 21,
    "formation": "Python",
}
print(etudiant["nom"])        # Amina
print(len(etudiant))          # 3 paires
```

Les clés sont le plus souvent des chaînes ; elles doivent être **uniques**. Les valeurs peuvent être de n'importe quel type, y compris des listes.

## Ajouter, modifier, supprimer

```python
stock = {"pommes": 12, "poires": 5}

stock["bananes"] = 8      # nouvelle clé : ajout
stock["pommes"] = 10      # clé existante : modification
del stock["poires"]       # suppression

print(stock)              # {'pommes': 10, 'bananes': 8}
```

Lire une clé absente provoque une erreur :

```python
print(stock["kiwis"])
# KeyError: 'kiwis'
```

Deux façons de s'en protéger :

```python
if "kiwis" in stock:              # in teste les clés
    print(stock["kiwis"])

print(stock.get("kiwis", 0))      # get renvoie 0 si la clé n'existe pas
```

## Parcourir un dictionnaire

```python
notes = {"Lina": 16, "Yanis": 11, "Amina": 14}

for prenom in notes:                     # parcourt les clés
    print(prenom)

for prenom, note in notes.items():       # paires (clé, valeur)
    print(f"{prenom} : {note}/20")

print(list(notes.values()))              # [16, 11, 14]
print(sum(notes.values()) / len(notes))  # 13.666...
```

`items()` est la méthode la plus utile : elle renvoie des tuples `(clé, valeur)` que l'on déballe directement dans la boucle.

## Compter avec un dictionnaire

Un usage classique : compter des occurrences. La clé est l'élément compté, la valeur son nombre d'apparitions.

```python
votes = ["Python", "SQL", "Python", "Anglais", "Python", "SQL"]
compte = {}
for choix in votes:
    compte[choix] = compte.get(choix, 0) + 1
print(compte)    # {'Python': 3, 'SQL': 2, 'Anglais': 1}
```

## Combiner listes et dictionnaires

Les données réelles mélangent souvent les deux : une liste de dictionnaires, chacun décrivant un élément.

```python
classe = [
    {"nom": "Lina", "notes": [16, 18]},
    {"nom": "Yanis", "notes": [11, 9]},
]
for eleve in classe:
    moyenne = sum(eleve["notes"]) / len(eleve["notes"])
    print(f"{eleve['nom']} : {moyenne:.1f}")
```

Remarquez les guillemets simples `'nom'` à l'intérieur de la f-string délimitée par des guillemets doubles.

## À retenir

- Un dictionnaire associe des clés uniques à des valeurs : `{"cle": valeur}`.
- `d[cle] = valeur` ajoute ou modifie ; `del d[cle]` supprime.
- `in` teste une clé ; `get(cle, defaut)` évite la `KeyError`.
- `items()` parcourt les paires, `values()` les valeurs.

## Exercices

### Exercice 1 — Mini-annuaire

Créez un dictionnaire de trois contacts (prénom → numéro). Demandez un prénom et affichez son numéro, ou le message `Contact inconnu`.

```solution
annuaire = {
    "Lina": "06 12 34 56 78",
    "Yanis": "07 98 76 54 32",
    "Amina": "06 11 22 33 44",
}

prenom = input("Prénom : ")
print(annuaire.get(prenom, "Contact inconnu"))
```

### Exercice 2 — Fréquence des lettres

Demandez un mot et affichez combien de fois apparaît chaque lettre, au format `p : 1`.

```solution
mot = input("Votre mot : ").lower()
frequences = {}
for lettre in mot:
    frequences[lettre] = frequences.get(lettre, 0) + 1

for lettre, nombre in frequences.items():
    print(f"{lettre} : {nombre}")
```
"""

M4_L1 = r"""
## Pourquoi des fonctions ?

Vous utilisez déjà des fonctions : `print()`, `len()`, `input()`. Une **fonction** est un bloc de code nommé que l'on peut appeler autant de fois que nécessaire. Écrire ses propres fonctions permet :

- d'éviter de copier-coller le même code ;
- de découper un programme en petites étapes faciles à comprendre ;
- de corriger un problème à un seul endroit.

## Définir et appeler une fonction

On définit une fonction avec le mot-clé `def`, un nom, des parenthèses et deux-points. Le corps est indenté.

```python
def saluer():
    print("Bonjour et bienvenue sur SMK Academy !")

saluer()     # appel : le code de la fonction s'exécute
saluer()     # on peut l'appeler plusieurs fois
```

Définir une fonction n'exécute rien : son code ne s'exécute qu'au moment de l'**appel**. La définition doit apparaître avant le premier appel.

## Les paramètres

Un **paramètre** est une variable qui reçoit une valeur au moment de l'appel. La valeur transmise s'appelle un **argument**.

```python
def saluer(prenom):
    print(f"Bonjour {prenom} !")

saluer("Lina")     # Bonjour Lina !
saluer("Yanis")    # Bonjour Yanis !
```

Une fonction peut avoir plusieurs paramètres, séparés par des virgules ; les arguments sont associés dans l'ordre :

```python
def presenter(prenom, age):
    print(f"{prenom} a {age} ans.")

presenter("Amina", 21)
```

## Renvoyer un résultat : return

`print()` affiche une valeur à l'écran, mais le programme ne peut pas la réutiliser. Pour qu'une fonction **produise** un résultat utilisable, on utilise `return` :

```python
def carre(n):
    return n * n

resultat = carre(5)
print(resultat)            # 25
print(carre(3) + carre(4)) # 25
```

`return` arrête immédiatement la fonction et renvoie la valeur à l'endroit de l'appel. Une fonction sans `return` renvoie la valeur spéciale `None` :

```python
def afficher_carre(n):
    print(n * n)

x = afficher_carre(4)   # affiche 16
print(x)                # None : rien n'a été renvoyé
```

C'est une source d'erreur fréquente : dans la plupart des cas, une fonction de calcul doit **renvoyer** son résultat plutôt que l'afficher.

## Plusieurs return

Une fonction peut contenir plusieurs `return`, par exemple dans des conditions :

```python
def mention(note):
    if note >= 16:
        return "Très bien"
    if note >= 14:
        return "Bien"
    if note >= 10:
        return "Passable"
    return "Non validé"

print(mention(15))   # Bien
```

Comme `return` quitte la fonction, les `elif` ne sont pas nécessaires ici.

## Renvoyer plusieurs valeurs

En séparant les valeurs par des virgules, une fonction renvoie un tuple, que l'on peut déballer :

```python
def min_max(valeurs):
    return min(valeurs), max(valeurs)

plus_petit, plus_grand = min_max([12, 7, 19])
print(plus_petit, plus_grand)   # 7 19
```

## À retenir

- `def nom(parametres):` définit une fonction ; elle ne s'exécute qu'à l'appel `nom(arguments)`.
- `return` renvoie un résultat et termine la fonction.
- Sans `return`, une fonction renvoie `None`.
- Préférez renvoyer un résultat plutôt que l'afficher dans la fonction.

## Exercices

### Exercice 1 — Prix TTC

Écrivez une fonction `prix_ttc(prix_ht)` qui renvoie le prix avec 20 % de TVA. Testez-la avec 50 et 19.99.

```solution
def prix_ttc(prix_ht):
    return prix_ht * 1.2

print(prix_ttc(50))                # 60.0
print(f"{prix_ttc(19.99):.2f}")    # 23.99
```

### Exercice 2 — Est-ce un nombre pair ?

Écrivez une fonction `est_pair(n)` qui renvoie `True` si `n` est pair et `False` sinon, puis utilisez-la pour afficher les nombres pairs de 1 à 10.

```solution
def est_pair(n):
    return n % 2 == 0

for i in range(1, 11):
    if est_pair(i):
        print(i)
```
"""

M4_L2 = r'''
## Des valeurs par défaut

Un paramètre peut recevoir une **valeur par défaut**, utilisée si l'argument n'est pas fourni :

```python
def saluer(prenom, formule="Bonjour"):
    print(f"{formule} {prenom} !")

saluer("Lina")               # Bonjour Lina !
saluer("Yanis", "Bonsoir")   # Bonsoir Yanis !
```

Les paramètres avec valeur par défaut se placent **après** les paramètres obligatoires.

## Les arguments nommés

À l'appel, on peut préciser le nom du paramètre. L'ordre n'a alors plus d'importance et l'appel devient plus lisible :

```python
def creer_compte(email, pseudo, newsletter=False):
    print(email, pseudo, newsletter)

creer_compte("lina@exemple.fr", "lina", newsletter=True)
creer_compte(pseudo="yanis", email="yanis@exemple.fr")
```

Vous connaissez déjà ce mécanisme : `print("a", "b", sep="-")` ou `print(x, end="")` utilisent des arguments nommés.

## La portée des variables

Une variable créée **dans** une fonction est **locale** : elle n'existe que pendant l'exécution de la fonction.

```python
def calculer():
    resultat = 42
    return resultat

calculer()
print(resultat)
# NameError: name 'resultat' is not defined
```

Pour récupérer une valeur calculée dans une fonction, on la **renvoie** avec `return` et on la stocke à l'appel : `resultat = calculer()`.

Une fonction peut **lire** une variable définie en dehors (variable **globale**), mais si elle lui affecte une valeur, Python crée une nouvelle variable locale du même nom :

```python
taux = 20

def appliquer_tva(prix):
    return prix * (1 + taux / 100)   # lecture de la variable globale : autorisé

print(appliquer_tva(100))   # 120.0
```

Bonne pratique : faites passer les informations par les **paramètres** et les résultats par **return**. Une fonction qui ne dépend que de ses paramètres est plus facile à comprendre et à tester.

## Les paramètres et les listes

Quand on passe une liste à une fonction, la fonction reçoit **la même liste**, pas une copie. Si elle la modifie, la modification est visible à l'extérieur :

```python
def ajouter_bonus(notes):
    for i in range(len(notes)):
        notes[i] = min(20, notes[i] + 1)

mes_notes = [12, 19, 20]
ajouter_bonus(mes_notes)
print(mes_notes)   # [13, 20, 20]
```

Pour ne pas modifier l'original, on renvoie une nouvelle liste :

```python
def avec_bonus(notes):
    resultat = []
    for note in notes:
        resultat.append(min(20, note + 1))
    return resultat
```

## Documenter une fonction

Une **docstring** est une chaîne placée juste sous la ligne `def`. Elle explique ce que fait la fonction, et l'aide de Python l'affiche avec `help()` :

```python
def moyenne(valeurs):
    """Renvoie la moyenne d'une liste de nombres non vide."""
    return sum(valeurs) / len(valeurs)

help(moyenne)
```

## À retenir

- `param=valeur` donne une valeur par défaut ; ces paramètres viennent en dernier.
- Les arguments nommés rendent les appels explicites et indépendants de l'ordre.
- Les variables d'une fonction sont locales : récupérez les résultats avec `return`.
- Une liste passée en argument peut être modifiée par la fonction.

## Exercices

### Exercice 1 — Puissance

Écrivez une fonction `puissance(base, exposant=2)` qui renvoie `base` élevé à `exposant`. Testez `puissance(5)`, `puissance(2, 10)` et `puissance(exposant=3, base=2)`.

```solution
def puissance(base, exposant=2):
    return base ** exposant

print(puissance(5))                    # 25
print(puissance(2, 10))                # 1024
print(puissance(exposant=3, base=2))   # 8
```

### Exercice 2 — Filtrer les notes

Écrivez une fonction `notes_reussies(notes, seuil=10)` qui renvoie une **nouvelle** liste contenant uniquement les notes supérieures ou égales au seuil, sans modifier la liste d'origine.

```solution
def notes_reussies(notes, seuil=10):
    reussies = []
    for note in notes:
        if note >= seuil:
            reussies.append(note)
    return reussies

toutes = [8, 12, 15, 9, 10]
print(notes_reussies(toutes))       # [12, 15, 10]
print(notes_reussies(toutes, 14))   # [15]
print(toutes)                       # inchangée : [8, 12, 15, 9, 10]
```
'''

M4_L3 = r'''
## Réutiliser le travail des autres : les modules

Python est livré avec une **bibliothèque standard** : des centaines de fonctions prêtes à l'emploi, rangées dans des **modules**. On les charge avec `import`.

```python
import math

print(math.sqrt(16))     # 4.0   racine carrée
print(math.pi)           # 3.141592653589793
print(math.ceil(2.1))    # 3     arrondi à l'entier supérieur
```

On peut aussi importer uniquement ce dont on a besoin :

```python
from math import sqrt, floor

print(sqrt(25))    # 5.0
print(floor(2.9))  # 2
```

## Le module random

```python
import random

print(random.randint(1, 6))                 # entier entre 1 et 6 inclus
print(random.choice(["pile", "face"]))      # élément au hasard
cartes = [1, 2, 3, 4, 5]
random.shuffle(cartes)                      # mélange la liste sur place
print(cartes)
```

## Découper un problème en fonctions

Face à un programme plus long, la bonne méthode est de le découper en petites fonctions qui font chacune **une seule chose**, puis de les assembler. Prenons un jeu « devinez le nombre ».

```python
import random


def tirer_nombre(maximum):
    """Choisit le nombre secret."""
    return random.randint(1, maximum)


def demander_essai(maximum):
    """Redemande tant que la saisie n'est pas un entier dans les bornes."""
    while True:
        saisie = input(f"Votre proposition (1-{maximum}) : ")
        if saisie.isdigit() and 1 <= int(saisie) <= maximum:
            return int(saisie)
        print("Saisie invalide.")


def indice(essai, secret):
    """Renvoie le message à afficher après un essai."""
    if essai < secret:
        return "C'est plus."
    if essai > secret:
        return "C'est moins."
    return "Gagné !"


def jouer(maximum=100):
    secret = tirer_nombre(maximum)
    essais = 0
    while True:
        essai = demander_essai(maximum)
        essais += 1
        message = indice(essai, secret)
        print(message)
        if essai == secret:
            print(f"Trouvé en {essais} essais.")
            return essais


jouer(20)
```

Chaque fonction a un nom qui dit ce qu'elle fait. La fonction `jouer` se lit presque comme une description du jeu. Et si l'on veut changer le texte des indices, on sait immédiatement où intervenir.

La méthode `isdigit()` renvoie `True` si la chaîne ne contient que des chiffres : elle évite ici l'erreur qu'aurait provoquée `int("abc")`. Au module 5, vous verrez une approche plus générale avec `try`.

## Tester ses fonctions

Une fonction qui renvoie une valeur se teste facilement avec `assert`, qui lève une erreur si la condition est fausse :

```python
assert indice(5, 10) == "C'est plus."
assert indice(15, 10) == "C'est moins."
assert indice(10, 10) == "Gagné !"
print("Tous les tests passent.")
```

C'est l'une des grandes raisons de préférer `return` à `print` : une valeur renvoyée se vérifie automatiquement.

## Conventions de style

- Noms de fonctions en *snake_case*, sous forme de verbe : `calculer_moyenne`, `afficher_menu`.
- Deux lignes vides entre les fonctions.
- Les `import` en haut du fichier.
- Une fonction courte (moins de 20 lignes) qui fait une seule chose.

## À retenir

- `import module` puis `module.fonction()`, ou `from module import fonction`.
- `math` pour les calculs, `random` pour le hasard.
- Découpez un programme en fonctions courtes, une responsabilité chacune.
- `assert condition` vérifie automatiquement le résultat d'une fonction.

## Exercices

### Exercice 1 — Lancer de dés

Écrivez une fonction `lancer_des(nombre)` qui simule `nombre` lancers d'un dé à six faces et renvoie la liste des résultats. Affichez la liste et la somme pour 5 lancers.

```solution
import random


def lancer_des(nombre):
    resultats = []
    for _ in range(nombre):
        resultats.append(random.randint(1, 6))
    return resultats


lancers = lancer_des(5)
print(lancers, "somme :", sum(lancers))
```

> Le nom de variable `_` indique par convention que la valeur n'est pas utilisée.

### Exercice 2 — Aire d'un disque, testée

Écrivez `aire_disque(rayon)` avec le module `math`, puis vérifiez avec `assert` que l'aire d'un disque de rayon 1 est bien `math.pi` et que celle de rayon 0 vaut 0.

```solution
import math


def aire_disque(rayon):
    """Renvoie l'aire d'un disque."""
    return math.pi * rayon ** 2


assert aire_disque(1) == math.pi
assert aire_disque(0) == 0
print(f"Aire pour un rayon de 3 : {aire_disque(3):.2f}")   # 28.27
```
'''

M5_L1 = r"""
## Quand le programme rencontre un problème

Une saisie inattendue, un fichier absent, une division par zéro : ces situations provoquent des **exceptions**. Sans précaution, le programme s'arrête avec un message d'erreur.

```python
age = int(input("Votre âge : "))   # l'utilisateur tape « vingt »
# ValueError: invalid literal for int() with base 10: 'vingt'
```

Les exceptions les plus fréquentes :

| Exception | Cause typique |
|-----------|---------------|
| `ValueError` | conversion impossible : `int("abc")` |
| `ZeroDivisionError` | division par zéro |
| `IndexError` | indice hors de la liste |
| `KeyError` | clé absente d'un dictionnaire |
| `TypeError` | opération entre types incompatibles |
| `FileNotFoundError` | fichier introuvable |

## Intercepter une exception : try / except

Le bloc `try` contient le code qui peut échouer ; le bloc `except` indique quoi faire si l'exception survient. Le programme continue ensuite normalement.

```python
try:
    age = int(input("Votre âge : "))
    print(f"L'an prochain, vous aurez {age + 1} ans.")
except ValueError:
    print("Merci de saisir un nombre entier.")
print("Suite du programme")
```

Si la conversion réussit, le bloc `except` est ignoré. Si elle échoue, Python saute directement dans `except` : la ligne `print(f"L'an prochain…")` n'est pas exécutée.

## Redemander jusqu'à obtenir une saisie valide

En combinant `while True`, `try` et `break`, on obtient une saisie robuste :

```python
def demander_entier(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print("Ce n'est pas un nombre entier, réessayez.")


nombre = demander_entier("Combien de leçons par semaine ? ")
```

## Plusieurs cas d'erreur

On peut prévoir un `except` par type d'exception :

```python
def moyenne(total, nombre):
    try:
        return total / nombre
    except ZeroDivisionError:
        print("Aucune note : moyenne impossible.")
        return None
    except TypeError:
        print("Le total et le nombre doivent être des nombres.")
        return None
```

Évitez d'écrire un `except:` seul, sans type : il intercepterait toutes les erreurs, y compris vos propres fautes de frappe, et rendrait les problèmes très difficiles à trouver. Précisez toujours l'exception attendue.

## else et finally

- `else` s'exécute seulement si **aucune** exception n'a eu lieu ;
- `finally` s'exécute **toujours**, qu'il y ait eu une erreur ou non (utile pour libérer une ressource).

```python
try:
    valeur = int(input("Un nombre : "))
except ValueError:
    print("Saisie invalide.")
else:
    print(f"Le double vaut {valeur * 2}.")
finally:
    print("Fin de la saisie.")
```

## Lever une exception soi-même : raise

Une fonction peut signaler qu'on l'utilise mal en levant une exception avec `raise` :

```python
def verifier_note(note):
    if not 0 <= note <= 20:
        raise ValueError("La note doit être comprise entre 0 et 20.")
    return note


try:
    verifier_note(25)
except ValueError as erreur:
    print("Erreur :", erreur)   # Erreur : La note doit être comprise entre 0 et 20.
```

`as erreur` donne accès au message de l'exception.

## À retenir

- Une exception interrompt le programme si elle n'est pas interceptée.
- `try` / `except NomDeLException:` traite l'erreur et permet de continuer.
- Précisez toujours le type d'exception ; évitez `except:` seul.
- `else` : aucune erreur ; `finally` : toujours ; `raise` : signaler une erreur.

## Exercices

### Exercice 1 — Division sécurisée

Demandez deux nombres et affichez leur quotient. Gérez la saisie non numérique (`ValueError`) et la division par zéro avec deux messages différents.

```solution
try:
    a = float(input("Premier nombre : "))
    b = float(input("Second nombre : "))
    print(f"Résultat : {a / b:.2f}")
except ValueError:
    print("Veuillez saisir des nombres.")
except ZeroDivisionError:
    print("Division par zéro impossible.")
```

### Exercice 2 — Note validée

Écrivez une fonction `saisir_note()` qui redemande une note jusqu'à obtenir un nombre entre 0 et 20, en gérant aussi les saisies non numériques. Elle renvoie la note.

```solution
def saisir_note():
    while True:
        try:
            note = float(input("Note sur 20 : "))
        except ValueError:
            print("Ce n'est pas un nombre.")
            continue
        if 0 <= note <= 20:
            return note
        print("La note doit être entre 0 et 20.")


note = saisir_note()
print("Note enregistrée :", note)
```
"""

M5_L2 = r"""
## Conserver des données après la fin du programme

Les variables disparaissent quand le programme se termine. Pour garder des informations (notes, scores, paramètres), on les enregistre dans un **fichier**.

## Ouvrir un fichier avec with

La fonction `open()` ouvre un fichier ; le mot-clé `with` garantit qu'il sera **refermé automatiquement**, même en cas d'erreur.

```python
with open("notes.txt", "w", encoding="utf-8") as fichier:
    fichier.write("Lina;16\n")
    fichier.write("Yanis;11\n")
```

Le deuxième argument est le **mode** :

| Mode | Rôle |
|------|------|
| `"r"` | lecture (par défaut) ; erreur si le fichier n'existe pas |
| `"w"` | écriture ; crée le fichier ou **efface** son contenu |
| `"a"` | ajout à la fin ; crée le fichier s'il n'existe pas |

Précisez toujours `encoding="utf-8"` pour que les accents soient correctement enregistrés sur tous les systèmes.

`write()` n'ajoute pas de retour à la ligne : écrivez `\n` vous-même.

## Lire un fichier

```python
with open("notes.txt", "r", encoding="utf-8") as fichier:
    contenu = fichier.read()       # tout le fichier dans une chaîne
print(contenu)
```

Le plus souvent, on lit **ligne par ligne** avec une boucle `for` :

```python
with open("notes.txt", encoding="utf-8") as fichier:
    for ligne in fichier:
        ligne = ligne.strip()      # retire le \n final et les espaces
        print(ligne)
```

`strip()` est indispensable : chaque ligne lue se termine par `\n`.

## Exploiter des données structurées

Le format `nom;note` est une version simple du format **CSV** (valeurs séparées). Avec `split(";")`, on récupère chaque champ :

```python
notes = {}
with open("notes.txt", encoding="utf-8") as fichier:
    for ligne in fichier:
        nom, note = ligne.strip().split(";")
        notes[nom] = float(note)

print(notes)                                  # {'Lina': 16.0, 'Yanis': 11.0}
print(sum(notes.values()) / len(notes))       # 13.5
```

Pour des fichiers CSV réels (guillemets, virgules dans les valeurs), le module standard `csv` gère tous les cas particuliers.

## Ajouter sans effacer

```python
def enregistrer_score(nom, score):
    with open("scores.txt", "a", encoding="utf-8") as fichier:
        fichier.write(f"{nom};{score}\n")


enregistrer_score("Amina", 18)
enregistrer_score("Lina", 15)
```

Chaque appel ajoute une ligne : les scores précédents sont conservés.

## Gérer un fichier absent

À la première exécution, le fichier n'existe peut-être pas encore. On combine lecture et gestion d'exception :

```python
def charger_scores():
    scores = []
    try:
        with open("scores.txt", encoding="utf-8") as fichier:
            for ligne in fichier:
                nom, score = ligne.strip().split(";")
                scores.append((nom, int(score)))
    except FileNotFoundError:
        pass   # pas encore de fichier : on renvoie une liste vide
    return scores
```

`pass` est une instruction qui ne fait rien ; elle sert quand la syntaxe exige un bloc.

## Où est créé le fichier ?

Un nom simple comme `"notes.txt"` désigne un fichier dans le **dossier courant**, en général celui depuis lequel vous lancez le programme. Si Python ne trouve pas un fichier que vous voyez pourtant, vérifiez d'abord ce dossier.

## À retenir

- `with open(nom, mode, encoding="utf-8") as f:` ouvre et referme automatiquement.
- `"r"` lit, `"w"` écrase, `"a"` ajoute à la fin.
- Lisez ligne par ligne avec `for ligne in f`, puis `strip()` et `split()`.
- Interceptez `FileNotFoundError` quand le fichier peut ne pas exister.

## Exercices

### Exercice 1 — Journal d'apprentissage

Écrivez un programme qui demande ce que vous avez appris aujourd'hui et l'ajoute comme nouvelle ligne dans `journal.txt`, puis affiche tout le journal avec un numéro devant chaque ligne.

```solution
entree = input("Qu'avez-vous appris aujourd'hui ? ")

with open("journal.txt", "a", encoding="utf-8") as fichier:
    fichier.write(entree + "\n")

with open("journal.txt", encoding="utf-8") as fichier:
    for numero, ligne in enumerate(fichier, start=1):
        print(f"{numero}. {ligne.strip()}")
```

### Exercice 2 — Meilleur score

En réutilisant `charger_scores()`, affichez le meilleur score et son auteur, ou `Aucun score enregistré` si la liste est vide.

```solution
scores = charger_scores()

if not scores:
    print("Aucun score enregistré")
else:
    meilleur_nom, meilleur_score = scores[0]
    for nom, score in scores:
        if score > meilleur_score:
            meilleur_nom, meilleur_score = nom, score
    print(f"Meilleur score : {meilleur_score} ({meilleur_nom})")
```
"""

M5_L3 = r"""
## Le projet : un carnet de notes en ligne de commande

Pour terminer la formation, vous allez assembler tout ce que vous avez appris dans un programme complet. Le **carnet de notes** permet de :

1. ajouter une note pour une matière ;
2. afficher toutes les notes et la moyenne par matière ;
3. afficher la moyenne générale ;
4. enregistrer les notes dans un fichier et les recharger au démarrage.

Vous mobiliserez : variables et conversions (module 1), conditions et boucles (module 2), dictionnaires et listes (module 3), fonctions (module 4), fichiers et exceptions (module 5).

## Étape 1 — Choisir la structure de données

Un dictionnaire dont les clés sont les matières et les valeurs des listes de notes :

```python
carnet = {
    "Maths": [14, 16.5],
    "Anglais": [12],
}
```

Ajouter une note revient à faire `carnet.setdefault(matiere, []).append(note)` : `setdefault` crée la liste vide si la matière n'existe pas encore, puis la renvoie.

## Étape 2 — Charger et enregistrer

Format du fichier `carnet.txt` : une ligne par note, `matiere;note`.

```python
FICHIER = "carnet.txt"


def charger():
    carnet = {}
    try:
        with open(FICHIER, encoding="utf-8") as f:
            for ligne in f:
                matiere, note = ligne.strip().split(";")
                carnet.setdefault(matiere, []).append(float(note))
    except FileNotFoundError:
        pass
    return carnet


def enregistrer(carnet):
    with open(FICHIER, "w", encoding="utf-8") as f:
        for matiere, notes in carnet.items():
            for note in notes:
                f.write(f"{matiere};{note}\n")
```

Une variable écrite en majuscules (`FICHIER`) est, par convention, une **constante** : une valeur qui ne change pas pendant l'exécution.

## Étape 3 — Les calculs

```python
def moyenne(notes):
    return sum(notes) / len(notes)


def moyenne_generale(carnet):
    moyennes = [moyenne(notes) for notes in carnet.values() if notes]
    if not moyennes:
        return None
    return moyenne(moyennes)
```

La ligne `[moyenne(notes) for notes in carnet.values() if notes]` est une **liste en compréhension** : une écriture compacte de la boucle « pour chaque liste non vide, ajouter sa moyenne ». Elle équivaut à :

```python
moyennes = []
for notes in carnet.values():
    if notes:
        moyennes.append(moyenne(notes))
```

## Étape 4 — Les saisies

```python
def saisir_note():
    while True:
        try:
            note = float(input("Note sur 20 : ").replace(",", "."))
        except ValueError:
            print("Ce n'est pas un nombre.")
            continue
        if 0 <= note <= 20:
            return note
        print("La note doit être entre 0 et 20.")
```

`replace(",", ".")` accepte aussi la virgule française : `12,5` devient `12.5`.

## Étape 5 — Le menu principal

```python
def afficher(carnet):
    if not carnet:
        print("Le carnet est vide.")
        return
    for matiere, notes in sorted(carnet.items()):
        liste = ", ".join(str(n) for n in notes)
        print(f"{matiere} : {liste}  (moyenne {moyenne(notes):.2f})")


def main():
    carnet = charger()
    while True:
        print("\n1. Ajouter une note  2. Afficher  3. Moyenne générale  4. Quitter")
        choix = input("Votre choix : ")
        if choix == "1":
            matiere = input("Matière : ").strip().capitalize()
            carnet.setdefault(matiere, []).append(saisir_note())
            enregistrer(carnet)
            print("Note enregistrée.")
        elif choix == "2":
            afficher(carnet)
        elif choix == "3":
            generale = moyenne_generale(carnet)
            if generale is None:
                print("Aucune note pour l'instant.")
            else:
                print(f"Moyenne générale : {generale:.2f}/20")
        elif choix == "4":
            print("À bientôt !")
            break
        else:
            print("Choix invalide.")


main()
```

Exemple d'exécution :

```text
1. Ajouter une note  2. Afficher  3. Moyenne générale  4. Quitter
Votre choix : 1
Matière : maths
Note sur 20 : 15,5
Note enregistrée.

1. Ajouter une note  2. Afficher  3. Moyenne générale  4. Quitter
Votre choix : 2
Maths : 15.5  (moyenne 15.50)
```

## Pour aller plus loin

Une fois le carnet fonctionnel, améliorez-le :

- supprimer la dernière note d'une matière ;
- afficher la meilleure et la moins bonne matière ;
- refuser une matière vide ;
- afficher une mention à côté de chaque moyenne, avec la fonction `mention()` du module 4.

## À retenir

- Un projet se construit par étapes : données, fichiers, calculs, saisies, menu.
- Chaque étape correspond à des fonctions courtes et testables.
- `setdefault` crée une entrée de dictionnaire si nécessaire.
- Les listes en compréhension condensent une boucle qui construit une liste.

## Exercices

### Exercice 1 — Meilleure matière

Ajoutez une fonction `meilleure_matiere(carnet)` qui renvoie le nom de la matière ayant la meilleure moyenne (ou `None` si le carnet est vide), et une option de menu pour l'afficher.

```solution
def meilleure_matiere(carnet):
    meilleure = None
    meilleure_moyenne = -1
    for matiere, notes in carnet.items():
        if notes and moyenne(notes) > meilleure_moyenne:
            meilleure, meilleure_moyenne = matiere, moyenne(notes)
    return meilleure


# Dans main(), ajouter par exemple :
# elif choix == "5":
#     print("Meilleure matière :", meilleure_matiere(carnet) or "aucune")
```

### Exercice 2 — Tests automatiques

Écrivez trois `assert` qui vérifient `moyenne`, `moyenne_generale` sur un carnet de test, et `moyenne_generale` sur un carnet vide.

```solution
test = {"Maths": [10, 20], "Anglais": [12]}

assert moyenne([10, 20]) == 15
assert moyenne_generale(test) == 13.5     # moyenne de 15 et 12
assert moyenne_generale({}) is None
print("Tous les tests passent.")
```
"""

QUIZ_M3 = [
    ("single", "Qu'affiche ce programme ?", 'prenoms = ["Amina", "Yanis", "Lina"]\nprint(prenoms[1])',
     ["Amina", "Yanis", "Lina", "Une erreur"], [1],
     "Les indices commencent à 0 : prenoms[0] vaut \"Amina\", prenoms[1] vaut \"Yanis\"."),
    ("single", "Que vaut lettres[1:3] si lettres = ['a', 'b', 'c', 'd'] ?", None,
     ["['a', 'b', 'c']", "['b', 'c']", "['b', 'c', 'd']", "['a', 'b']"], [1],
     "Une tranche va de l'indice de début inclus à l'indice de fin exclu : indices 1 et 2, soit 'b' et 'c'."),
    ("single", "Quelle instruction ajoute \"thé\" à la fin de la liste boissons ?", None,
     ['boissons.append("thé")', 'boissons.add("thé")', 'boissons + "thé"', 'boissons.insert("thé")'], [0],
     "append() ajoute un élément à la fin. add() n'existe pas pour les listes, et insert() demande aussi un indice."),
    ("true_false", "Un tuple peut être modifié après sa création.", None,
     ["Vrai", "Faux"], [1],
     "Un tuple est immuable : point[0] = 5 provoque une TypeError. Pour une collection modifiable, utilisez une liste."),
    ("single", "Après x, y = (4, 9), que vaut y ?", None,
     ["4", "9", "(4, 9)", "Une erreur"], [1],
     "Le déballage répartit les éléments dans l'ordre : x reçoit 4 et y reçoit 9."),
    ("single", "Qu'affiche ce programme ?", 'stock = {"pommes": 12}\nstock["pommes"] = 10\nstock["poires"] = 3\nprint(len(stock))',
     ["1", "2", "3", "25"], [1],
     "La première affectation modifie une clé existante, la seconde ajoute une nouvelle clé : le dictionnaire contient 2 paires."),
    ("multiple", "Quelles instructions évitent une KeyError si la clé \"kiwis\" n'existe pas dans stock ?", None,
     ['stock.get("kiwis", 0)', 'stock["kiwis"]', 'if "kiwis" in stock: print(stock["kiwis"])', 'del stock["kiwis"]'], [0, 2],
     "get() renvoie une valeur par défaut, et le test in vérifie la présence de la clé avant de la lire. Lire ou supprimer directement une clé absente lève une KeyError."),
    ("single", "Que renvoie \"a b c\".split() ?", None,
     ["'abc'", "['a', 'b', 'c']", "('a', 'b', 'c')", "['a b c']"], [1],
     "split() découpe la chaîne sur les espaces et renvoie une liste de chaînes."),
    ("single", "Qu'affiche ce programme ?", 'for i, x in enumerate(["a", "b"], start=1):\n    print(i, x)',
     ["0 a puis 1 b", "1 a puis 2 b", "a 1 puis b 2", "Une erreur"], [1],
     "enumerate() fournit des paires (indice, élément) ; start=1 fait commencer la numérotation à 1."),
    ("true_false", "Pour une liste de longueur 5, l'indice 5 désigne le dernier élément.", None,
     ["Vrai", "Faux"], [1],
     "Les indices valides vont de 0 à 4. Le dernier élément est liste[4] ou liste[-1] ; liste[5] provoque une IndexError."),
]

QUIZ_M4 = [
    ("single", "Quel mot-clé permet de définir une fonction en Python ?", None,
     ["function", "def", "func", "define"], [1],
     "Une fonction se définit avec def, suivi de son nom, de parenthèses et de deux-points."),
    ("single", "Qu'affiche ce programme ?", "def carre(n):\n    return n * n\n\nprint(carre(3) + 1)",
     ["9", "10", "31", "Une erreur"], [1],
     "carre(3) renvoie 9, auquel on ajoute 1 : le programme affiche 10."),
    ("single", "Que vaut x après ce code ?", "def afficher(n):\n    print(n * 2)\n\nx = afficher(4)",
     ["8", "4", "None", "Une erreur"], [2],
     "La fonction affiche 8 mais ne contient pas de return : elle renvoie None, qui est stocké dans x."),
    ("true_false", "Définir une fonction avec def exécute immédiatement son code.", None,
     ["Vrai", "Faux"], [1],
     "La définition enregistre seulement la fonction. Son code s'exécute à chaque appel."),
    ("single", "Avec def saluer(prenom, formule=\"Bonjour\"), qu'affiche saluer(\"Lina\") si la fonction fait print(formule, prenom) ?", None,
     ["Lina", "Bonjour Lina", "Lina Bonjour", "Une erreur : il manque un argument"], [1],
     "Le paramètre formule a une valeur par défaut, utilisée quand l'argument n'est pas fourni."),
    ("multiple", "Quels appels sont valides pour def creer(email, pseudo, newsletter=False) ?", None,
     ['creer("a@b.fr", "ana")', 'creer(pseudo="ana", email="a@b.fr")', 'creer("a@b.fr")', 'creer("a@b.fr", "ana", newsletter=True)'], [0, 1, 3],
     "email et pseudo sont obligatoires, dans l'ordre ou nommés. creer(\"a@b.fr\") oublie pseudo et provoque une TypeError."),
    ("single", "Que se passe-t-il à la dernière ligne ?", "def calculer():\n    resultat = 42\n\ncalculer()\nprint(resultat)",
     ["Affiche 42", "Affiche None", "NameError : resultat n'est pas défini", "Affiche 0"], [2],
     "resultat est une variable locale à la fonction : elle n'existe plus après l'appel. Il fallait la renvoyer avec return."),
    ("single", "Quelle instruction importe uniquement la fonction sqrt du module math ?", None,
     ["import sqrt", "from math import sqrt", "import math.sqrt()", "include math"], [1],
     "from module import fonction importe un élément précis, utilisable ensuite sans préfixe : sqrt(16)."),
    ("single", "Qu'affiche ce programme ?", "def bonus(notes):\n    notes.append(20)\n\nmes_notes = [12]\nbonus(mes_notes)\nprint(mes_notes)",
     ["[12]", "[12, 20]", "[20]", "None"], [1],
     "La fonction reçoit la même liste, pas une copie : l'ajout est visible à l'extérieur."),
    ("true_false", "Une fonction peut renvoyer plusieurs valeurs, par exemple return a, b.", None,
     ["Vrai", "Faux"], [0],
     "return a, b renvoie un tuple (a, b), que l'on peut déballer à l'appel : x, y = f()."),
]

QUIZ_M5 = [
    ("single", "Quelle exception provoque int(\"vingt\") ?", None,
     ["TypeError", "ValueError", "ZeroDivisionError", "KeyError"], [1],
     "La chaîne ne représente pas un entier : la conversion échoue avec une ValueError."),
    ("single", "Qu'affiche ce programme si l'utilisateur tape « abc » ?", 'try:\n    n = int(input())\n    print("OK")\nexcept ValueError:\n    print("Erreur")\nprint("Fin")',
     ["OK puis Fin", "Erreur puis Fin", "Erreur seulement", "Le programme s'arrête avec une ValueError"], [1],
     "La conversion échoue : Python saute dans except (Erreur) sans exécuter print(\"OK\"), puis le programme continue (Fin)."),
    ("single", "Dans quel cas le bloc finally s'exécute-t-il ?", None,
     ["Seulement si une exception a eu lieu", "Seulement si aucune exception n'a eu lieu", "Toujours", "Jamais si le bloc try contient return"], [2],
     "finally s'exécute dans tous les cas, ce qui le rend utile pour libérer une ressource."),
    ("true_false", "Il est recommandé d'écrire except: sans préciser de type d'exception.", None,
     ["Vrai", "Faux"], [1],
     "Un except sans type intercepte toutes les erreurs, y compris les fautes de programmation, et masque les vrais problèmes. Précisez l'exception attendue."),
    ("single", "Quel mode d'ouverture ajoute du texte à la fin d'un fichier sans effacer son contenu ?", None,
     ['"r"', '"w"', '"a"', '"x"'], [2],
     "\"a\" (append) ajoute à la fin. \"w\" efface le contenu existant, \"r\" ouvre en lecture seule."),
    ("single", "Pourquoi utilise-t-on with open(...) as f: ?", None,
     ["Pour lire plus vite", "Pour que le fichier soit refermé automatiquement", "Pour créer un dossier", "C'est la seule façon d'ouvrir un fichier"], [1],
     "with garantit la fermeture du fichier à la fin du bloc, même si une erreur survient."),
    ("single", "Que renvoie \"Lina;16\\n\".strip().split(\";\") ?", None,
     ["['Lina;16']", "['Lina', '16']", "['Lina', 16]", "('Lina', '16')"], [1],
     "strip() retire le retour à la ligne, puis split(\";\") découpe sur le point-virgule. Les éléments restent des chaînes : il faut convertir 16 avec int() ou float()."),
    ("multiple", "Quelles affirmations sur l'ouverture en mode \"w\" sont exactes ?", None,
     ["Elle crée le fichier s'il n'existe pas", "Elle efface le contenu existant", "Elle lève FileNotFoundError si le fichier n'existe pas", "Elle ajoute toujours à la fin"], [0, 1],
     "Le mode \"w\" crée le fichier si besoin et remplace son contenu. C'est le mode \"r\" qui lève FileNotFoundError pour un fichier absent."),
    ("single", "Qu'affiche ce programme ?", 'def verifier(note):\n    if note > 20:\n        raise ValueError("trop grand")\n    return note\n\ntry:\n    verifier(25)\nexcept ValueError as e:\n    print(e)',
     ["25", "trop grand", "ValueError", "Rien"], [1],
     "raise lève l'exception avec son message ; except ValueError as e l'intercepte et print(e) affiche le message."),
    ("true_false", "write() ajoute automatiquement un retour à la ligne après le texte écrit.", None,
     ["Vrai", "Faux"], [1],
     "write() écrit exactement le texte fourni. Pour passer à la ligne, ajoutez \"\\n\" vous-même."),
]
