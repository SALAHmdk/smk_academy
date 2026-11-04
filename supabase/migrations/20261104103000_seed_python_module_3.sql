-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$python-debutant$smk$, $smk$Python pour débutants$smk$, $smk$Écrivez vos premiers programmes, pas à pas.$smk$, $smk$Une formation progressive pour apprendre à programmer avec Python, même sans aucune expérience. Chaque leçon combine explications, exemples de code commentés et exercices corrigés, puis un quiz noté sur 20 valide chaque module.$smk$, $smk$Programmation$smk$, $smk$debutant$smk$, 660, array[$smk$Écrire et exécuter un programme Python$smk$, $smk$Manipuler variables, types et conversions$smk$, $smk$Contrôler le déroulement d'un programme avec conditions et boucles$smk$, $smk$Organiser son code avec des fonctions$smk$, $smk$Lire et écrire des fichiers, gérer les erreurs$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance en programmation n'est nécessaire$smk$]::text[], $smk$published$smk$, false, 1)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('5d72ac2e-9373-5e71-8aa4-20a924c02949', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Listes, tuples et dictionnaires$smk$, $smk$Stocker et manipuler des collections de données.$smk$, 3, $smk$published$smk$)
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position, status = excluded.status;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('6c3a4309-e98a-5e84-b7ff-c6fe4f73ffc6', '5d72ac2e-9373-5e71-8aa4-20a924c02949', $smk$listes$smk$, $smk$Les listes$smk$, $smk$Créer, lire, modifier et parcourir une liste.$smk$, $smk$## Ranger plusieurs valeurs ensemble

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
```$smk$, 25, 1),
('705455fb-0812-5b9c-a2ee-05feb61a34d2', '5d72ac2e-9373-5e71-8aa4-20a924c02949', $smk$tuples-et-sequences$smk$, $smk$Tuples et parcours de séquences$smk$, $smk$Tuples, déballage, enumerate(), zip(), split() et join().$smk$, $smk$## Le tuple : une séquence qui ne change pas

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
```$smk$, 25, 2),
('d13300d0-1365-561c-bd78-294ee85602d1', '5d72ac2e-9373-5e71-8aa4-20a924c02949', $smk$dictionnaires$smk$, $smk$Les dictionnaires$smk$, $smk$Associer des clés à des valeurs, compter, combiner.$smk$, $smk$## Retrouver une valeur par son nom

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
```$smk$, 25, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('e6d3b879-97ba-5067-994c-cb1feeeae44a', '5d72ac2e-9373-5e71-8aa4-20a924c02949', $smk$Quiz — Listes, tuples et dictionnaires$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('6181d0cf-1d25-525a-be25-4f642fd4cdaa', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 1, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$prenoms = ["Amina", "Yanis", "Lina"]
print(prenoms[1])$smk$, 2),
('6d8eebee-cafc-54c4-970f-08854f4e6238', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 2, $smk$single$smk$, $smk$Que vaut lettres[1:3] si lettres = ['a', 'b', 'c', 'd'] ?$smk$, null, 2),
('c1b3780a-0fc1-5efa-be64-01a9e7e06538', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 3, $smk$single$smk$, $smk$Quelle instruction ajoute "thé" à la fin de la liste boissons ?$smk$, null, 2),
('7b36f906-38e0-5b8c-9c9c-a64a1d484ac6', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 4, $smk$true_false$smk$, $smk$Un tuple peut être modifié après sa création.$smk$, null, 2),
('8aac58bd-a4ea-5ca0-85fd-f2f950552f52', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 5, $smk$single$smk$, $smk$Après x, y = (4, 9), que vaut y ?$smk$, null, 2),
('2f293889-5cbc-5b44-b44f-40173333a7bb', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 6, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$stock = {"pommes": 12}
stock["pommes"] = 10
stock["poires"] = 3
print(len(stock))$smk$, 2),
('d7c81df6-e96b-5c92-bd12-d57836dd13f4', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 7, $smk$multiple$smk$, $smk$Quelles instructions évitent une KeyError si la clé "kiwis" n'existe pas dans stock ?$smk$, null, 2),
('82d85587-5774-5a1d-94ec-d84840b6b233', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 8, $smk$single$smk$, $smk$Que renvoie "a b c".split() ?$smk$, null, 2),
('f2b4af5f-21c6-580e-a97b-28a0a5808e0f', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 9, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$for i, x in enumerate(["a", "b"], start=1):
    print(i, x)$smk$, 2),
('b44cd899-8dda-5eb6-bdc4-37ed66251665', 'e6d3b879-97ba-5067-994c-cb1feeeae44a', 10, $smk$true_false$smk$, $smk$Pour une liste de longueur 5, l'indice 5 désigne le dernier élément.$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('e7bd459f-490d-5aed-9ac2-229a21fe04e0', '6181d0cf-1d25-525a-be25-4f642fd4cdaa', 1, $smk$Amina$smk$),
('245affe9-04d6-5940-8671-1cb4b8a03546', '6181d0cf-1d25-525a-be25-4f642fd4cdaa', 2, $smk$Yanis$smk$),
('46317fe7-cfbe-5550-a664-7c709d076cf9', '6181d0cf-1d25-525a-be25-4f642fd4cdaa', 3, $smk$Lina$smk$),
('d7a51a4c-1f53-5369-a5ec-b75e74f39176', '6181d0cf-1d25-525a-be25-4f642fd4cdaa', 4, $smk$Une erreur$smk$),
('1a7764b7-083f-5203-909b-2944a512f54a', '6d8eebee-cafc-54c4-970f-08854f4e6238', 1, $smk$['a', 'b', 'c']$smk$),
('0a016889-fbfb-5e87-9157-f93940c863e8', '6d8eebee-cafc-54c4-970f-08854f4e6238', 2, $smk$['b', 'c']$smk$),
('3a403e6f-91a9-54da-8e77-2e8becb88aa8', '6d8eebee-cafc-54c4-970f-08854f4e6238', 3, $smk$['b', 'c', 'd']$smk$),
('b4676c0a-afeb-5ae6-bf85-9c14c6268e65', '6d8eebee-cafc-54c4-970f-08854f4e6238', 4, $smk$['a', 'b']$smk$),
('0dc89ad8-0096-5537-9af4-d18a91e5f388', 'c1b3780a-0fc1-5efa-be64-01a9e7e06538', 1, $smk$boissons.append("thé")$smk$),
('22ae5e4a-5546-5f67-885c-7796644ed458', 'c1b3780a-0fc1-5efa-be64-01a9e7e06538', 2, $smk$boissons.add("thé")$smk$),
('9011ee45-f52a-5171-932e-0d23d81b92e6', 'c1b3780a-0fc1-5efa-be64-01a9e7e06538', 3, $smk$boissons + "thé"$smk$),
('71e1ebb9-4cef-5eb1-ae1c-39c396c8fd85', 'c1b3780a-0fc1-5efa-be64-01a9e7e06538', 4, $smk$boissons.insert("thé")$smk$),
('4932a820-763c-5f26-8992-ef95f9f600b8', '7b36f906-38e0-5b8c-9c9c-a64a1d484ac6', 1, $smk$Vrai$smk$),
('4b62db65-22e1-5095-8a60-2b76fe7be7b9', '7b36f906-38e0-5b8c-9c9c-a64a1d484ac6', 2, $smk$Faux$smk$),
('1c21cff6-4307-55ae-add7-e160ad303f40', '8aac58bd-a4ea-5ca0-85fd-f2f950552f52', 1, $smk$4$smk$),
('aaaaf30e-f674-5809-827f-254267b223cc', '8aac58bd-a4ea-5ca0-85fd-f2f950552f52', 2, $smk$9$smk$),
('dd7a7653-acce-574a-96e7-07fb284224d3', '8aac58bd-a4ea-5ca0-85fd-f2f950552f52', 3, $smk$(4, 9)$smk$),
('696c4f11-0e7b-5875-895e-69960dc8003c', '8aac58bd-a4ea-5ca0-85fd-f2f950552f52', 4, $smk$Une erreur$smk$),
('24c52f9d-45d1-51ee-a110-904cd2394060', '2f293889-5cbc-5b44-b44f-40173333a7bb', 1, $smk$1$smk$),
('e9dc7c88-7c83-52e0-b34b-fb9135dc8db8', '2f293889-5cbc-5b44-b44f-40173333a7bb', 2, $smk$2$smk$),
('3b64f643-70be-5e00-b62f-d1868e61400c', '2f293889-5cbc-5b44-b44f-40173333a7bb', 3, $smk$3$smk$),
('c00f3883-d4e1-56de-b4f0-010dcbad4fa0', '2f293889-5cbc-5b44-b44f-40173333a7bb', 4, $smk$25$smk$),
('1ba735ab-f76f-53c4-91de-2902405d1b1e', 'd7c81df6-e96b-5c92-bd12-d57836dd13f4', 1, $smk$stock.get("kiwis", 0)$smk$),
('10812160-b253-5c33-873a-cc3d04b07e6f', 'd7c81df6-e96b-5c92-bd12-d57836dd13f4', 2, $smk$stock["kiwis"]$smk$),
('91f5a0cc-d0cc-523c-bc4b-8da5d3dee23b', 'd7c81df6-e96b-5c92-bd12-d57836dd13f4', 3, $smk$if "kiwis" in stock: print(stock["kiwis"])$smk$),
('1226c1b5-5f24-5b05-8e63-4178242bf93c', 'd7c81df6-e96b-5c92-bd12-d57836dd13f4', 4, $smk$del stock["kiwis"]$smk$),
('b0d633d5-3b97-52e9-822b-b4acef0f65c5', '82d85587-5774-5a1d-94ec-d84840b6b233', 1, $smk$'abc'$smk$),
('6fbb517c-4143-5c45-af1b-e3c0698945b2', '82d85587-5774-5a1d-94ec-d84840b6b233', 2, $smk$['a', 'b', 'c']$smk$),
('36a2f4be-e97f-58ed-bc6c-d13322f67324', '82d85587-5774-5a1d-94ec-d84840b6b233', 3, $smk$('a', 'b', 'c')$smk$),
('97550a50-9f79-5178-b9df-700a3417b716', '82d85587-5774-5a1d-94ec-d84840b6b233', 4, $smk$['a b c']$smk$),
('632d14ce-c81c-53bd-85fe-a4cc5a1707d1', 'f2b4af5f-21c6-580e-a97b-28a0a5808e0f', 1, $smk$0 a puis 1 b$smk$),
('3d255987-00ee-5378-bdc1-9d8e7e84b4e2', 'f2b4af5f-21c6-580e-a97b-28a0a5808e0f', 2, $smk$1 a puis 2 b$smk$),
('62de11d7-4a73-5d3f-bbcc-898ec6070d2a', 'f2b4af5f-21c6-580e-a97b-28a0a5808e0f', 3, $smk$a 1 puis b 2$smk$),
('a9313e30-5334-5f72-b365-675a4067458e', 'f2b4af5f-21c6-580e-a97b-28a0a5808e0f', 4, $smk$Une erreur$smk$),
('5df3650e-6ec8-51ba-a023-e8682df1ec71', 'b44cd899-8dda-5eb6-bdc4-37ed66251665', 1, $smk$Vrai$smk$),
('479909e9-e364-5fd3-80cc-4009c49138b5', 'b44cd899-8dda-5eb6-bdc4-37ed66251665', 2, $smk$Faux$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('6181d0cf-1d25-525a-be25-4f642fd4cdaa', array['245affe9-04d6-5940-8671-1cb4b8a03546']::uuid[], $smk$Les indices commencent à 0 : prenoms[0] vaut "Amina", prenoms[1] vaut "Yanis".$smk$),
('6d8eebee-cafc-54c4-970f-08854f4e6238', array['0a016889-fbfb-5e87-9157-f93940c863e8']::uuid[], $smk$Une tranche va de l'indice de début inclus à l'indice de fin exclu : indices 1 et 2, soit 'b' et 'c'.$smk$),
('c1b3780a-0fc1-5efa-be64-01a9e7e06538', array['0dc89ad8-0096-5537-9af4-d18a91e5f388']::uuid[], $smk$append() ajoute un élément à la fin. add() n'existe pas pour les listes, et insert() demande aussi un indice.$smk$),
('7b36f906-38e0-5b8c-9c9c-a64a1d484ac6', array['4b62db65-22e1-5095-8a60-2b76fe7be7b9']::uuid[], $smk$Un tuple est immuable : point[0] = 5 provoque une TypeError. Pour une collection modifiable, utilisez une liste.$smk$),
('8aac58bd-a4ea-5ca0-85fd-f2f950552f52', array['aaaaf30e-f674-5809-827f-254267b223cc']::uuid[], $smk$Le déballage répartit les éléments dans l'ordre : x reçoit 4 et y reçoit 9.$smk$),
('2f293889-5cbc-5b44-b44f-40173333a7bb', array['e9dc7c88-7c83-52e0-b34b-fb9135dc8db8']::uuid[], $smk$La première affectation modifie une clé existante, la seconde ajoute une nouvelle clé : le dictionnaire contient 2 paires.$smk$),
('d7c81df6-e96b-5c92-bd12-d57836dd13f4', array['1ba735ab-f76f-53c4-91de-2902405d1b1e', '91f5a0cc-d0cc-523c-bc4b-8da5d3dee23b']::uuid[], $smk$get() renvoie une valeur par défaut, et le test in vérifie la présence de la clé avant de la lire. Lire ou supprimer directement une clé absente lève une KeyError.$smk$),
('82d85587-5774-5a1d-94ec-d84840b6b233', array['6fbb517c-4143-5c45-af1b-e3c0698945b2']::uuid[], $smk$split() découpe la chaîne sur les espaces et renvoie une liste de chaînes.$smk$),
('f2b4af5f-21c6-580e-a97b-28a0a5808e0f', array['3d255987-00ee-5378-bdc1-9d8e7e84b4e2']::uuid[], $smk$enumerate() fournit des paires (indice, élément) ; start=1 fait commencer la numérotation à 1.$smk$),
('b44cd899-8dda-5eb6-bdc4-37ed66251665', array['479909e9-e364-5fd3-80cc-4009c49138b5']::uuid[], $smk$Les indices valides vont de 0 à 4. Le dernier élément est liste[4] ou liste[-1] ; liste[5] provoque une IndexError.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

