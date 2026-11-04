-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$python-debutant$smk$, $smk$Python pour débutants$smk$, $smk$Écrivez vos premiers programmes, pas à pas.$smk$, $smk$Une formation progressive pour apprendre à programmer avec Python, même sans aucune expérience. Chaque leçon combine explications, exemples de code commentés et exercices corrigés, puis un quiz noté sur 20 valide chaque module.$smk$, $smk$Programmation$smk$, $smk$debutant$smk$, 660, array[$smk$Écrire et exécuter un programme Python$smk$, $smk$Manipuler variables, types et conversions$smk$, $smk$Contrôler le déroulement d'un programme avec conditions et boucles$smk$, $smk$Organiser son code avec des fonctions$smk$, $smk$Lire et écrire des fichiers, gérer les erreurs$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance en programmation n'est nécessaire$smk$]::text[], $smk$published$smk$, false, 1)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('277b3ca7-00f1-5d59-892d-04756c6489a7', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Les fonctions$smk$, $smk$Découper un programme en blocs réutilisables.$smk$, 4, $smk$published$smk$)
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position, status = excluded.status;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('c4913467-ab83-5ae5-b151-e61f5e78452a', '277b3ca7-00f1-5d59-892d-04756c6489a7', $smk$definir-une-fonction$smk$, $smk$Définir et appeler une fonction$smk$, $smk$def, paramètres et return.$smk$, $smk$## Pourquoi des fonctions ?

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
```$smk$, 25, 1),
('dd185f43-8d4a-55e2-8a4a-b76716e74b03', '277b3ca7-00f1-5d59-892d-04756c6489a7', $smk$parametres-et-portee$smk$, $smk$Paramètres, portée et documentation$smk$, $smk$Valeurs par défaut, arguments nommés, variables locales, docstrings.$smk$, $smk$## Des valeurs par défaut

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
```$smk$, 25, 2),
('c0963e30-21f8-539e-8a60-a22578746807', '277b3ca7-00f1-5d59-892d-04756c6489a7', $smk$modules-et-decomposition$smk$, $smk$Modules et découpage d'un programme$smk$, $smk$import, math, random, fonctions courtes et tests avec assert.$smk$, $smk$## Réutiliser le travail des autres : les modules

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
```$smk$, 30, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('801c1334-e625-5d7e-ba4f-1a9962dac1bc', '277b3ca7-00f1-5d59-892d-04756c6489a7', $smk$Quiz — Les fonctions$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('85ed2f87-07c2-5f02-9298-28463c4c51ce', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 1, $smk$single$smk$, $smk$Quel mot-clé permet de définir une fonction en Python ?$smk$, null, 2),
('c40b6525-2201-5d69-9218-8b3c7d08d343', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 2, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$def carre(n):
    return n * n

print(carre(3) + 1)$smk$, 2),
('7dbb011b-4f34-50bd-ab2f-639273afd704', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 3, $smk$single$smk$, $smk$Que vaut x après ce code ?$smk$, $smk$def afficher(n):
    print(n * 2)

x = afficher(4)$smk$, 2),
('c3e9d998-bec7-5c9c-b96f-1111ceadc8dc', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 4, $smk$true_false$smk$, $smk$Définir une fonction avec def exécute immédiatement son code.$smk$, null, 2),
('3d72ee6c-4e80-57d5-b2a4-1772062d91d5', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 5, $smk$single$smk$, $smk$Avec def saluer(prenom, formule="Bonjour"), qu'affiche saluer("Lina") si la fonction fait print(formule, prenom) ?$smk$, null, 2),
('5ea6262f-3057-5ed9-8bcc-e3a460370489', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 6, $smk$multiple$smk$, $smk$Quels appels sont valides pour def creer(email, pseudo, newsletter=False) ?$smk$, null, 2),
('8acdfd0c-3b29-531c-aa56-596d73b2c96b', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 7, $smk$single$smk$, $smk$Que se passe-t-il à la dernière ligne ?$smk$, $smk$def calculer():
    resultat = 42

calculer()
print(resultat)$smk$, 2),
('ed5dbb3c-e601-5080-b148-982cc24caa32', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 8, $smk$single$smk$, $smk$Quelle instruction importe uniquement la fonction sqrt du module math ?$smk$, null, 2),
('1e9156ee-eace-5243-a0b2-f01fd86a4223', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 9, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$def bonus(notes):
    notes.append(20)

mes_notes = [12]
bonus(mes_notes)
print(mes_notes)$smk$, 2),
('17df09e3-d80f-534d-9e35-f872f7c51106', '801c1334-e625-5d7e-ba4f-1a9962dac1bc', 10, $smk$true_false$smk$, $smk$Une fonction peut renvoyer plusieurs valeurs, par exemple return a, b.$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('04f53e3a-27f8-50c0-8119-edd4e445ea93', '85ed2f87-07c2-5f02-9298-28463c4c51ce', 1, $smk$function$smk$),
('45d1b2cf-ffef-5c66-beaf-6934cf57332d', '85ed2f87-07c2-5f02-9298-28463c4c51ce', 2, $smk$def$smk$),
('86708b35-7a09-515b-8290-fa2bd8473a9b', '85ed2f87-07c2-5f02-9298-28463c4c51ce', 3, $smk$func$smk$),
('7b587ba2-92d0-5606-b700-b5c425a5ff51', '85ed2f87-07c2-5f02-9298-28463c4c51ce', 4, $smk$define$smk$),
('30b9c6bf-dcf4-5205-86d2-a280b18679ee', 'c40b6525-2201-5d69-9218-8b3c7d08d343', 1, $smk$9$smk$),
('9d22422e-ba72-5249-8857-3bc6a248658b', 'c40b6525-2201-5d69-9218-8b3c7d08d343', 2, $smk$10$smk$),
('b6adc55a-90c5-50a9-95a9-f64756a6d6dc', 'c40b6525-2201-5d69-9218-8b3c7d08d343', 3, $smk$31$smk$),
('b9f63197-f07c-565e-a41c-f3079a770496', 'c40b6525-2201-5d69-9218-8b3c7d08d343', 4, $smk$Une erreur$smk$),
('8d04ffda-1deb-53c7-937d-73e59a88a62a', '7dbb011b-4f34-50bd-ab2f-639273afd704', 1, $smk$8$smk$),
('362b4e7a-0ef5-5fa5-947c-a576fa60027d', '7dbb011b-4f34-50bd-ab2f-639273afd704', 2, $smk$4$smk$),
('d20590a4-6d4e-5a6c-8fa7-e037bc069154', '7dbb011b-4f34-50bd-ab2f-639273afd704', 3, $smk$None$smk$),
('78abfe20-05eb-566f-96cf-3053775f8b62', '7dbb011b-4f34-50bd-ab2f-639273afd704', 4, $smk$Une erreur$smk$),
('4ffd9686-2545-5333-948a-3bc4ea31a7c2', 'c3e9d998-bec7-5c9c-b96f-1111ceadc8dc', 1, $smk$Vrai$smk$),
('3e077769-c8a3-5eb1-bb19-3cc6a8d25476', 'c3e9d998-bec7-5c9c-b96f-1111ceadc8dc', 2, $smk$Faux$smk$),
('7d0f7e40-be4d-5e6f-ba06-69148da51e8a', '3d72ee6c-4e80-57d5-b2a4-1772062d91d5', 1, $smk$Lina$smk$),
('000899e0-339d-53b0-9081-992fd394ccc8', '3d72ee6c-4e80-57d5-b2a4-1772062d91d5', 2, $smk$Bonjour Lina$smk$),
('60915596-5b9f-57f9-b356-ab1c59aad0de', '3d72ee6c-4e80-57d5-b2a4-1772062d91d5', 3, $smk$Lina Bonjour$smk$),
('8f0bd79d-ea92-5dcd-bd88-ffc40f49915f', '3d72ee6c-4e80-57d5-b2a4-1772062d91d5', 4, $smk$Une erreur : il manque un argument$smk$),
('0efc8c06-8313-5d42-9e54-1b323be18749', '5ea6262f-3057-5ed9-8bcc-e3a460370489', 1, $smk$creer("a@b.fr", "ana")$smk$),
('bf1d4d16-6a0a-575f-9200-ebc9972c403b', '5ea6262f-3057-5ed9-8bcc-e3a460370489', 2, $smk$creer(pseudo="ana", email="a@b.fr")$smk$),
('3c50c472-265b-5cb7-aa1d-fd89817d7051', '5ea6262f-3057-5ed9-8bcc-e3a460370489', 3, $smk$creer("a@b.fr")$smk$),
('f6c98a45-33f1-56c3-ace1-735809728214', '5ea6262f-3057-5ed9-8bcc-e3a460370489', 4, $smk$creer("a@b.fr", "ana", newsletter=True)$smk$),
('11af1a6a-9c95-5be5-8fd6-a4ba3b5a64b6', '8acdfd0c-3b29-531c-aa56-596d73b2c96b', 1, $smk$Affiche 42$smk$),
('0d7bdd92-a14c-5d40-823c-d63162b05e9a', '8acdfd0c-3b29-531c-aa56-596d73b2c96b', 2, $smk$Affiche None$smk$),
('3597a124-c2c1-5a4b-9299-bbe1472c175d', '8acdfd0c-3b29-531c-aa56-596d73b2c96b', 3, $smk$NameError : resultat n'est pas défini$smk$),
('78d79564-2132-585e-8127-d8f806c120b8', '8acdfd0c-3b29-531c-aa56-596d73b2c96b', 4, $smk$Affiche 0$smk$),
('d783809b-a650-5d3c-904d-a25c3e686af0', 'ed5dbb3c-e601-5080-b148-982cc24caa32', 1, $smk$import sqrt$smk$),
('1a8ae91b-6a49-5591-ae4f-cf874ba9350f', 'ed5dbb3c-e601-5080-b148-982cc24caa32', 2, $smk$from math import sqrt$smk$),
('1a71c338-9582-529a-8fc9-b55fd1e64e19', 'ed5dbb3c-e601-5080-b148-982cc24caa32', 3, $smk$import math.sqrt()$smk$),
('821039a5-c578-5fa8-bdbe-307f7dddde11', 'ed5dbb3c-e601-5080-b148-982cc24caa32', 4, $smk$include math$smk$),
('2abca4a1-4a61-57e3-a4ae-6a9ebc26ad0a', '1e9156ee-eace-5243-a0b2-f01fd86a4223', 1, $smk$[12]$smk$),
('92531ea4-c36d-520e-826f-f0dc000f7d16', '1e9156ee-eace-5243-a0b2-f01fd86a4223', 2, $smk$[12, 20]$smk$),
('353a93d7-57e9-5588-ad47-e321dea0d621', '1e9156ee-eace-5243-a0b2-f01fd86a4223', 3, $smk$[20]$smk$),
('61383e48-0688-599a-aedb-20ba1d391eab', '1e9156ee-eace-5243-a0b2-f01fd86a4223', 4, $smk$None$smk$),
('328cc0ff-0e7c-5e08-a2f8-f229b39b10d7', '17df09e3-d80f-534d-9e35-f872f7c51106', 1, $smk$Vrai$smk$),
('d5558bb6-fcb1-51e6-889f-03f0ceef6888', '17df09e3-d80f-534d-9e35-f872f7c51106', 2, $smk$Faux$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('85ed2f87-07c2-5f02-9298-28463c4c51ce', array['45d1b2cf-ffef-5c66-beaf-6934cf57332d']::uuid[], $smk$Une fonction se définit avec def, suivi de son nom, de parenthèses et de deux-points.$smk$),
('c40b6525-2201-5d69-9218-8b3c7d08d343', array['9d22422e-ba72-5249-8857-3bc6a248658b']::uuid[], $smk$carre(3) renvoie 9, auquel on ajoute 1 : le programme affiche 10.$smk$),
('7dbb011b-4f34-50bd-ab2f-639273afd704', array['d20590a4-6d4e-5a6c-8fa7-e037bc069154']::uuid[], $smk$La fonction affiche 8 mais ne contient pas de return : elle renvoie None, qui est stocké dans x.$smk$),
('c3e9d998-bec7-5c9c-b96f-1111ceadc8dc', array['3e077769-c8a3-5eb1-bb19-3cc6a8d25476']::uuid[], $smk$La définition enregistre seulement la fonction. Son code s'exécute à chaque appel.$smk$),
('3d72ee6c-4e80-57d5-b2a4-1772062d91d5', array['000899e0-339d-53b0-9081-992fd394ccc8']::uuid[], $smk$Le paramètre formule a une valeur par défaut, utilisée quand l'argument n'est pas fourni.$smk$),
('5ea6262f-3057-5ed9-8bcc-e3a460370489', array['0efc8c06-8313-5d42-9e54-1b323be18749', 'bf1d4d16-6a0a-575f-9200-ebc9972c403b', 'f6c98a45-33f1-56c3-ace1-735809728214']::uuid[], $smk$email et pseudo sont obligatoires, dans l'ordre ou nommés. creer("a@b.fr") oublie pseudo et provoque une TypeError.$smk$),
('8acdfd0c-3b29-531c-aa56-596d73b2c96b', array['3597a124-c2c1-5a4b-9299-bbe1472c175d']::uuid[], $smk$resultat est une variable locale à la fonction : elle n'existe plus après l'appel. Il fallait la renvoyer avec return.$smk$),
('ed5dbb3c-e601-5080-b148-982cc24caa32', array['1a8ae91b-6a49-5591-ae4f-cf874ba9350f']::uuid[], $smk$from module import fonction importe un élément précis, utilisable ensuite sans préfixe : sqrt(16).$smk$),
('1e9156ee-eace-5243-a0b2-f01fd86a4223', array['92531ea4-c36d-520e-826f-f0dc000f7d16']::uuid[], $smk$La fonction reçoit la même liste, pas une copie : l'ajout est visible à l'extérieur.$smk$),
('17df09e3-d80f-534d-9e35-f872f7c51106', array['328cc0ff-0e7c-5e08-a2f8-f229b39b10d7']::uuid[], $smk$return a, b renvoie un tuple (a, b), que l'on peut déballer à l'appel : x, y = f().$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

