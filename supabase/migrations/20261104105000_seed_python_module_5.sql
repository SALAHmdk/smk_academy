-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$python-debutant$smk$, $smk$Python pour débutants$smk$, $smk$Écrivez vos premiers programmes, pas à pas.$smk$, $smk$Une formation progressive pour apprendre à programmer avec Python, même sans aucune expérience. Chaque leçon combine explications, exemples de code commentés et exercices corrigés, puis un quiz noté sur 20 valide chaque module.$smk$, $smk$Programmation$smk$, $smk$debutant$smk$, 660, array[$smk$Écrire et exécuter un programme Python$smk$, $smk$Manipuler variables, types et conversions$smk$, $smk$Contrôler le déroulement d'un programme avec conditions et boucles$smk$, $smk$Organiser son code avec des fonctions$smk$, $smk$Lire et écrire des fichiers, gérer les erreurs$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance en programmation n'est nécessaire$smk$]::text[], $smk$published$smk$, false, 1)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('6592e04c-ad44-5dad-b0db-e530cff2fa4b', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Fichiers, erreurs et mini-projet$smk$, $smk$Lire et écrire des fichiers, gérer les exceptions, réaliser un projet complet.$smk$, 5, $smk$published$smk$)
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position, status = excluded.status;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('d58b23f3-e702-509c-bf8b-c5edcbacd9d6', '6592e04c-ad44-5dad-b0db-e530cff2fa4b', $smk$gerer-les-erreurs$smk$, $smk$Gérer les erreurs$smk$, $smk$try, except, else, finally et raise.$smk$, $smk$## Quand le programme rencontre un problème

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
```$smk$, 25, 1),
('fc32046f-2674-5522-ba27-ac9fe690d163', '6592e04c-ad44-5dad-b0db-e530cff2fa4b', $smk$lire-et-ecrire-des-fichiers$smk$, $smk$Lire et écrire des fichiers$smk$, $smk$open, with, modes r/w/a, lecture ligne par ligne.$smk$, $smk$## Conserver des données après la fin du programme

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
```$smk$, 25, 2),
('5be5235a-cce4-5bf9-8760-813ab5023b70', '6592e04c-ad44-5dad-b0db-e530cff2fa4b', $smk$mini-projet-carnet-de-notes$smk$, $smk$Mini-projet : un carnet de notes$smk$, $smk$Assembler toute la formation dans un programme complet.$smk$, $smk$## Le projet : un carnet de notes en ligne de commande

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
```$smk$, 45, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', '6592e04c-ad44-5dad-b0db-e530cff2fa4b', $smk$Quiz — Fichiers et erreurs$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 1, $smk$single$smk$, $smk$Quelle exception provoque int("vingt") ?$smk$, null, 2),
('ca09ef59-f8c3-5637-a225-c98859d50694', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 2, $smk$single$smk$, $smk$Qu'affiche ce programme si l'utilisateur tape « abc » ?$smk$, $smk$try:
    n = int(input())
    print("OK")
except ValueError:
    print("Erreur")
print("Fin")$smk$, 2),
('427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 3, $smk$single$smk$, $smk$Dans quel cas le bloc finally s'exécute-t-il ?$smk$, null, 2),
('e9d94ed1-e30d-5a4a-ada2-b8c3a3aed576', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 4, $smk$true_false$smk$, $smk$Il est recommandé d'écrire except: sans préciser de type d'exception.$smk$, null, 2),
('9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 5, $smk$single$smk$, $smk$Quel mode d'ouverture ajoute du texte à la fin d'un fichier sans effacer son contenu ?$smk$, null, 2),
('4306e90e-ff68-595e-9eee-01d6125cfb22', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 6, $smk$single$smk$, $smk$Pourquoi utilise-t-on with open(...) as f: ?$smk$, null, 2),
('c6190bc8-7767-5966-99d1-ac80b81a0680', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 7, $smk$single$smk$, $smk$Que renvoie "Lina;16\n".strip().split(";") ?$smk$, null, 2),
('57d8211d-d12d-5c6b-975e-25f475fd3e27', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 8, $smk$multiple$smk$, $smk$Quelles affirmations sur l'ouverture en mode "w" sont exactes ?$smk$, null, 2),
('bdd7d973-aa49-5004-a5ef-e5a808cd62e6', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 9, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$def verifier(note):
    if note > 20:
        raise ValueError("trop grand")
    return note

try:
    verifier(25)
except ValueError as e:
    print(e)$smk$, 2),
('1ba357e0-e86b-5ebe-b879-4e7f898e456c', '362ab9db-63e9-5e3d-9ebb-a92a6baa0aa5', 10, $smk$true_false$smk$, $smk$write() ajoute automatiquement un retour à la ligne après le texte écrit.$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('631fabb5-d4cf-52da-a561-3cada71d19b8', 'b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', 1, $smk$TypeError$smk$),
('087458cb-d9a3-525c-b8f5-27fff55ca731', 'b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', 2, $smk$ValueError$smk$),
('9e53da04-1774-548a-9fdc-30d6e09bff23', 'b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', 3, $smk$ZeroDivisionError$smk$),
('b1ceaa5c-4b69-5c34-8a99-e82b52aba08e', 'b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', 4, $smk$KeyError$smk$),
('6a4deb62-7ef4-5284-be97-3c6fc6513fcb', 'ca09ef59-f8c3-5637-a225-c98859d50694', 1, $smk$OK puis Fin$smk$),
('e2a68271-26ee-59f5-a19f-c6b41328e33e', 'ca09ef59-f8c3-5637-a225-c98859d50694', 2, $smk$Erreur puis Fin$smk$),
('a62e16ea-a151-55c4-879e-1bfc0311bb3a', 'ca09ef59-f8c3-5637-a225-c98859d50694', 3, $smk$Erreur seulement$smk$),
('996ff019-611d-576b-adb1-227c041402c7', 'ca09ef59-f8c3-5637-a225-c98859d50694', 4, $smk$Le programme s'arrête avec une ValueError$smk$),
('76c6ae40-8254-5a8a-b23f-e0a424e808bb', '427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', 1, $smk$Seulement si une exception a eu lieu$smk$),
('7ffba145-4642-518c-85ac-cff64de26c8c', '427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', 2, $smk$Seulement si aucune exception n'a eu lieu$smk$),
('54b1264b-c021-589f-a4d3-2122cc4c1be2', '427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', 3, $smk$Toujours$smk$),
('2577c22d-0076-5e73-8bda-dda8674fa812', '427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', 4, $smk$Jamais si le bloc try contient return$smk$),
('dea67d2a-67b1-549a-99d4-9cfd5d9cd160', 'e9d94ed1-e30d-5a4a-ada2-b8c3a3aed576', 1, $smk$Vrai$smk$),
('f736ff80-edb8-5ac8-9824-96c7fefabc7e', 'e9d94ed1-e30d-5a4a-ada2-b8c3a3aed576', 2, $smk$Faux$smk$),
('b5f8da29-62a6-5b79-bb89-5e751b8d1d87', '9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', 1, $smk$"r"$smk$),
('ccd21ec3-515c-5ac7-bf16-1c78631abe96', '9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', 2, $smk$"w"$smk$),
('e8dbb611-61ee-53c1-a7ec-ce2563e0640f', '9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', 3, $smk$"a"$smk$),
('0a15a232-9397-5c7b-9895-6fe3699b21e5', '9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', 4, $smk$"x"$smk$),
('ddfa3d7a-cfea-5399-9cfe-829aff9c8989', '4306e90e-ff68-595e-9eee-01d6125cfb22', 1, $smk$Pour lire plus vite$smk$),
('a38a087d-5f35-59c7-b70e-42acc5994e01', '4306e90e-ff68-595e-9eee-01d6125cfb22', 2, $smk$Pour que le fichier soit refermé automatiquement$smk$),
('cf16d378-6a5c-53de-94e6-0b55d83b6404', '4306e90e-ff68-595e-9eee-01d6125cfb22', 3, $smk$Pour créer un dossier$smk$),
('66703801-05b5-5084-b0ff-5371794d249a', '4306e90e-ff68-595e-9eee-01d6125cfb22', 4, $smk$C'est la seule façon d'ouvrir un fichier$smk$),
('592eed9e-5763-5761-8cfa-7c615ced165b', 'c6190bc8-7767-5966-99d1-ac80b81a0680', 1, $smk$['Lina;16']$smk$),
('4da037f4-188e-52e8-b9cb-f8f64a1c62db', 'c6190bc8-7767-5966-99d1-ac80b81a0680', 2, $smk$['Lina', '16']$smk$),
('c9042d0e-8855-53ed-9510-9a6aeb2bd213', 'c6190bc8-7767-5966-99d1-ac80b81a0680', 3, $smk$['Lina', 16]$smk$),
('85417421-1f7a-5c30-8f86-5c89cb703122', 'c6190bc8-7767-5966-99d1-ac80b81a0680', 4, $smk$('Lina', '16')$smk$),
('1bb3451d-79fa-5479-8210-762feb632183', '57d8211d-d12d-5c6b-975e-25f475fd3e27', 1, $smk$Elle crée le fichier s'il n'existe pas$smk$),
('5cba339c-be41-5697-89e5-68ef808eb48e', '57d8211d-d12d-5c6b-975e-25f475fd3e27', 2, $smk$Elle efface le contenu existant$smk$),
('2fd17234-bdbd-5f87-96f5-e9115d46ff9a', '57d8211d-d12d-5c6b-975e-25f475fd3e27', 3, $smk$Elle lève FileNotFoundError si le fichier n'existe pas$smk$),
('80f00081-269c-5f0d-ac2e-9ca1e93541e2', '57d8211d-d12d-5c6b-975e-25f475fd3e27', 4, $smk$Elle ajoute toujours à la fin$smk$),
('2ec9289d-2149-59ba-8f45-2c0be71b4ac5', 'bdd7d973-aa49-5004-a5ef-e5a808cd62e6', 1, $smk$25$smk$),
('ca3344f3-e8f1-5c5f-839b-70d29a589595', 'bdd7d973-aa49-5004-a5ef-e5a808cd62e6', 2, $smk$trop grand$smk$),
('1ca1a8ab-7193-5135-94e2-eebbeacae6c5', 'bdd7d973-aa49-5004-a5ef-e5a808cd62e6', 3, $smk$ValueError$smk$),
('29ac0efc-95c2-5a97-b5d6-31dabb87d370', 'bdd7d973-aa49-5004-a5ef-e5a808cd62e6', 4, $smk$Rien$smk$),
('05033c9c-7e02-59ae-b7ab-fda5ebcf61f2', '1ba357e0-e86b-5ebe-b879-4e7f898e456c', 1, $smk$Vrai$smk$),
('64cb48f5-b67a-5910-b276-2435eb3706e3', '1ba357e0-e86b-5ebe-b879-4e7f898e456c', 2, $smk$Faux$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('b6c9a266-2b0f-5ab9-ae8c-bac95bcdf0ee', array['087458cb-d9a3-525c-b8f5-27fff55ca731']::uuid[], $smk$La chaîne ne représente pas un entier : la conversion échoue avec une ValueError.$smk$),
('ca09ef59-f8c3-5637-a225-c98859d50694', array['e2a68271-26ee-59f5-a19f-c6b41328e33e']::uuid[], $smk$La conversion échoue : Python saute dans except (Erreur) sans exécuter print("OK"), puis le programme continue (Fin).$smk$),
('427cf9cb-286f-5a5d-9ac4-70ce7aa08a7d', array['54b1264b-c021-589f-a4d3-2122cc4c1be2']::uuid[], $smk$finally s'exécute dans tous les cas, ce qui le rend utile pour libérer une ressource.$smk$),
('e9d94ed1-e30d-5a4a-ada2-b8c3a3aed576', array['f736ff80-edb8-5ac8-9824-96c7fefabc7e']::uuid[], $smk$Un except sans type intercepte toutes les erreurs, y compris les fautes de programmation, et masque les vrais problèmes. Précisez l'exception attendue.$smk$),
('9f0dd409-54c1-5ab9-9a33-b7a96ebf529c', array['e8dbb611-61ee-53c1-a7ec-ce2563e0640f']::uuid[], $smk$"a" (append) ajoute à la fin. "w" efface le contenu existant, "r" ouvre en lecture seule.$smk$),
('4306e90e-ff68-595e-9eee-01d6125cfb22', array['a38a087d-5f35-59c7-b70e-42acc5994e01']::uuid[], $smk$with garantit la fermeture du fichier à la fin du bloc, même si une erreur survient.$smk$),
('c6190bc8-7767-5966-99d1-ac80b81a0680', array['4da037f4-188e-52e8-b9cb-f8f64a1c62db']::uuid[], $smk$strip() retire le retour à la ligne, puis split(";") découpe sur le point-virgule. Les éléments restent des chaînes : il faut convertir 16 avec int() ou float().$smk$),
('57d8211d-d12d-5c6b-975e-25f475fd3e27', array['1bb3451d-79fa-5479-8210-762feb632183', '5cba339c-be41-5697-89e5-68ef808eb48e']::uuid[], $smk$Le mode "w" crée le fichier si besoin et remplace son contenu. C'est le mode "r" qui lève FileNotFoundError pour un fichier absent.$smk$),
('bdd7d973-aa49-5004-a5ef-e5a808cd62e6', array['ca3344f3-e8f1-5c5f-839b-70d29a589595']::uuid[], $smk$raise lève l'exception avec son message ; except ValueError as e l'intercepte et print(e) affiche le message.$smk$),
('1ba357e0-e86b-5ebe-b879-4e7f898e456c', array['64cb48f5-b67a-5910-b276-2435eb3706e3']::uuid[], $smk$write() écrit exactement le texte fourni. Pour passer à la ligne, ajoutez "\n" vous-même.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

