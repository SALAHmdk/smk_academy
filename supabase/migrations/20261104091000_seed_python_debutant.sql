-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$python-debutant$smk$, $smk$Python pour débutants$smk$, $smk$Écrivez vos premiers programmes, pas à pas.$smk$, $smk$Une formation progressive pour apprendre à programmer avec Python, même sans aucune expérience. Chaque leçon combine explications, exemples de code commentés et exercices corrigés, puis un quiz noté sur 20 valide chaque module.$smk$, $smk$Programmation$smk$, $smk$debutant$smk$, 600, array[$smk$Écrire et exécuter un programme Python$smk$, $smk$Manipuler variables, types et conversions$smk$, $smk$Contrôler le déroulement d'un programme avec conditions et boucles$smk$, $smk$Organiser son code avec des fonctions$smk$, $smk$Lire et écrire des fichiers, gérer les erreurs$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance en programmation n'est nécessaire$smk$]::text[], $smk$published$smk$, false, 1)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$SELECT, filtres, tris, jointures et agrégations sur des données réelles.$smk$, $smk$Bases de données$smk$, $smk$debutant$smk$, 480, array[$smk$Écrire des requêtes SELECT$smk$, $smk$Filtrer et trier$smk$, $smk$Joindre des tables$smk$, $smk$Agréger des données$smk$]::text[], array[$smk$Aucun$smk$]::text[], $smk$coming_soon$smk$, false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.courses (id, slug, title, subtitle, description, category, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('56364fc8-3462-511e-a2df-d7bb067b3f03', $smk$anglais-professionnel-debutant$smk$, $smk$Anglais professionnel — débutant$smk$, $smk$Les bases pour communiquer au travail.$smk$, $smk$Se présenter, écrire un email simple, participer à une réunion.$smk$, $smk$Langues$smk$, $smk$debutant$smk$, 480, array[$smk$Se présenter$smk$, $smk$Écrire un email professionnel$smk$, $smk$Comprendre une réunion simple$smk$]::text[], array[$smk$Niveau A1 conseillé$smk$]::text[], $smk$coming_soon$smk$, false, 3)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category = excluded.category, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, status = excluded.status, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('e1d20424-2dff-5ca2-9e45-9c8a022c80e3', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Premiers pas avec Python$smk$, $smk$Écrire et exécuter un programme, utiliser variables, types et opérations.$smk$, 1, $smk$published$smk$),
('57ce5744-5413-5d8f-af77-74bf2787f572', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Conditions et boucles$smk$, $smk$Prendre des décisions et répéter des actions.$smk$, 2, $smk$published$smk$),
('5d72ac2e-9373-5e71-8aa4-20a924c02949', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Listes, tuples et dictionnaires$smk$, $smk$Stocker et manipuler des collections de données.$smk$, 3, $smk$coming_soon$smk$),
('277b3ca7-00f1-5d59-892d-04756c6489a7', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Les fonctions$smk$, $smk$Découper un programme en blocs réutilisables.$smk$, 4, $smk$coming_soon$smk$),
('6592e04c-ad44-5dad-b0db-e530cff2fa4b', '70e1705f-341c-5c47-9fa2-bddb767d9e42', $smk$Fichiers, erreurs et mini-projet$smk$, $smk$Lire et écrire des fichiers, gérer les exceptions, réaliser un projet complet.$smk$, 5, $smk$coming_soon$smk$)
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position, status = excluded.status;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('32ccfaee-b4c9-537b-ae27-01b54d7c1d0e', 'e1d20424-2dff-5ca2-9e45-9c8a022c80e3', $smk$decouvrir-python$smk$, $smk$Découvrir Python et écrire son premier programme$smk$, $smk$print(), commentaires et lecture des messages d'erreur.$smk$, $smk$## Pourquoi Python ?

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
```$smk$, 20, 1),
('f6b4b5e5-3d39-5ac8-bfeb-5aeceb467c69', 'e1d20424-2dff-5ca2-9e45-9c8a022c80e3', $smk$variables-et-types$smk$, $smk$Variables et types de base$smk$, $smk$Stocker des valeurs, bien les nommer, connaître int, float, str et bool.$smk$, $smk$## Qu'est-ce qu'une variable ?

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
```$smk$, 25, 2),
('6298a8c4-3b27-5772-b528-3b4307a17ff0', 'e1d20424-2dff-5ca2-9e45-9c8a022c80e3', $smk$saisie-conversions-operations$smk$, $smk$Saisie, conversions et opérations$smk$, $smk$input(), conversions de types, opérateurs arithmétiques et f-strings.$smk$, $smk$## Demander une information : input()

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
```$smk$, 30, 3),
('fab41434-f860-568b-acec-c7ca3bc91dde', '57ce5744-5413-5d8f-af77-74bf2787f572', $smk$conditions$smk$, $smk$Les conditions : if, elif, else$smk$, $smk$Comparaisons, opérateurs logiques et choix multiples.$smk$, $smk$## Prendre des décisions

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
```$smk$, 25, 1),
('7b8ec9b8-7f7c-58e1-82da-97ee9597bed0', '57ce5744-5413-5d8f-af77-74bf2787f572', $smk$boucle-while$smk$, $smk$La boucle while$smk$, $smk$Répéter tant qu'une condition est vraie, valider une saisie, accumuler.$smk$, $smk$## Répéter tant qu'une condition est vraie

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
```$smk$, 25, 2),
('6cde5a2f-105f-5a5d-9da0-6e6612d3eb4e', '57ce5744-5413-5d8f-af77-74bf2787f572', $smk$boucle-for$smk$, $smk$La boucle for et range()$smk$, $smk$Parcourir une séquence, compter, break et continue.$smk$, $smk$## Parcourir une séquence

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

> L'opérateur `in` teste si un caractère appartient à une chaîne : `"a" in "aeiouy"` vaut `True`.$smk$, 30, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('5e138572-4d1c-5200-b7bc-b707fe41a1a3', 'e1d20424-2dff-5ca2-9e45-9c8a022c80e3', $smk$Quiz — Premiers pas avec Python$smk$, 10),
('3b906e23-94ee-537b-9f81-4235a08fe91b', '57ce5744-5413-5d8f-af77-74bf2787f572', $smk$Quiz — Conditions et boucles$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('4d482a46-cdc9-5a2d-af30-f6697f046f49', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 1, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$print("2" + "3")$smk$, 2),
('84bce527-d31c-58d8-8c06-e2106a366e4b', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 2, $smk$single$smk$, $smk$Quel est le type de la valeur renvoyée par input() ?$smk$, null, 2),
('b2342927-e8d0-5694-a98a-59d86fb89606', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 3, $smk$single$smk$, $smk$Combien vaut l'expression 17 // 5 ?$smk$, null, 2),
('39b987c0-e2cf-53e9-8892-1e0da70434fe', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 4, $smk$single$smk$, $smk$Combien vaut l'expression 17 % 5 ?$smk$, null, 2),
('94ea164c-9487-5604-8aaa-3fefb3640b95', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 5, $smk$multiple$smk$, $smk$Parmi ces noms de variables, lesquels sont valides en Python ?$smk$, null, 2),
('6ac0a729-65f1-512b-8a99-c6041523efca', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 6, $smk$true_false$smk$, $smk$Python ignore tout ce qui suit le symbole # sur une ligne.$smk$, null, 2),
('74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 7, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$note = 15.456
print(f"{note:.1f}")$smk$, 2),
('66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 8, $smk$multiple$smk$, $smk$Quelles expressions produisent une erreur ?$smk$, null, 2),
('aab6556c-0f23-5873-a234-d55bf787daec', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 9, $smk$true_false$smk$, $smk$L'expression 8 / 2 renvoie l'entier 4.$smk$, null, 2),
('5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', '5e138572-4d1c-5200-b7bc-b707fe41a1a3', 10, $smk$single$smk$, $smk$Après ces instructions, que vaut score ?$smk$, $smk$score = 10
score = score + 5
score = score * 2$smk$, 2),
('48fcadb4-133a-5d91-b152-2a9dfabd0d89', '3b906e23-94ee-537b-9f81-4235a08fe91b', 1, $smk$single$smk$, $smk$Quel opérateur teste l'égalité de deux valeurs ?$smk$, null, 2),
('bcd94236-4942-5270-98a3-969878598671', '3b906e23-94ee-537b-9f81-4235a08fe91b', 2, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$note = 15
if note >= 12:
    print("A")
elif note >= 14:
    print("B")
else:
    print("C")$smk$, 2),
('8fd1c9f1-4662-5e85-8f14-59d86ff55641', '3b906e23-94ee-537b-9f81-4235a08fe91b', 3, $smk$single$smk$, $smk$Quels nombres produit range(2, 8, 2) ?$smk$, null, 2),
('ee72c5fb-d492-5865-8c2a-d35d178f2161', '3b906e23-94ee-537b-9f81-4235a08fe91b', 4, $smk$true_false$smk$, $smk$Une boucle while dont la condition ne devient jamais fausse s'exécute indéfiniment.$smk$, null, 2),
('12f0d6ee-6824-56d3-9522-7f873199838b', '3b906e23-94ee-537b-9f81-4235a08fe91b', 5, $smk$multiple$smk$, $smk$Quelles conditions sont vraies lorsque age = 20 ?$smk$, null, 2),
('c3aa61c0-f216-5103-8e31-5a7e3b751eb4', '3b906e23-94ee-537b-9f81-4235a08fe91b', 6, $smk$single$smk$, $smk$Combien de fois le mot « SMK » est-il affiché ?$smk$, $smk$for i in range(3):
    for j in range(2):
        print("SMK")$smk$, 2),
('249c71a3-eded-5d8f-b524-2f1cded2be75', '3b906e23-94ee-537b-9f81-4235a08fe91b', 7, $smk$single$smk$, $smk$Qu'affiche ce programme ?$smk$, $smk$for n in range(1, 6):
    if n == 3:
        continue
    print(n, end=' ')$smk$, 2),
('d091b533-2e82-5fd9-979c-b5f294c881eb', '3b906e23-94ee-537b-9f81-4235a08fe91b', 8, $smk$true_false$smk$, $smk$En Python, l'indentation du bloc qui suit un if est facultative.$smk$, null, 2),
('20c96769-cb43-505d-a99e-78bc9eb77e7b', '3b906e23-94ee-537b-9f81-4235a08fe91b', 9, $smk$single$smk$, $smk$Après cette boucle, que vaut total ?$smk$, $smk$total = 0
n = 1
while n <= 4:
    total += n
    n += 1$smk$, 2),
('9f96009c-a355-515b-ba8e-26f0028d468d', '3b906e23-94ee-537b-9f81-4235a08fe91b', 10, $smk$multiple$smk$, $smk$Dans quelles situations une boucle while est-elle plus adaptée qu'une boucle for ?$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('69a6177c-7d2b-5855-aa10-c7f9b128d95c', '4d482a46-cdc9-5a2d-af30-f6697f046f49', 1, $smk$5$smk$),
('0c58d56f-7000-559d-ab48-8f3c1d7b1530', '4d482a46-cdc9-5a2d-af30-f6697f046f49', 2, $smk$23$smk$),
('24eaedd0-9ffb-51bb-9c99-a73131f940f6', '4d482a46-cdc9-5a2d-af30-f6697f046f49', 3, $smk$Une erreur$smk$),
('e09c10ba-b4ab-591f-8ba6-7f24075a9986', '4d482a46-cdc9-5a2d-af30-f6697f046f49', 4, $smk$2 3$smk$),
('ed39b66b-0e34-5c22-8ba2-a56c38bd1b63', '84bce527-d31c-58d8-8c06-e2106a366e4b', 1, $smk$int$smk$),
('452e8d04-72e4-5f26-826a-117753a3fa8f', '84bce527-d31c-58d8-8c06-e2106a366e4b', 2, $smk$float$smk$),
('d5f150b7-7786-5026-9de5-5b827b4a940c', '84bce527-d31c-58d8-8c06-e2106a366e4b', 3, $smk$str$smk$),
('9bb07491-ae91-578e-bd76-1458096cd2fb', '84bce527-d31c-58d8-8c06-e2106a366e4b', 4, $smk$Cela dépend de ce que tape l'utilisateur$smk$),
('2e7ba0b9-77f4-53f1-9f32-c35db1aa38e8', 'b2342927-e8d0-5694-a98a-59d86fb89606', 1, $smk$3.4$smk$),
('3ff9c563-efcd-5c55-9991-87d79f0e9913', 'b2342927-e8d0-5694-a98a-59d86fb89606', 2, $smk$3$smk$),
('b3925a47-5ed6-5795-b271-2cbd1518dd8a', 'b2342927-e8d0-5694-a98a-59d86fb89606', 3, $smk$2$smk$),
('47e21922-68bc-53d6-9306-c003497bc2e1', 'b2342927-e8d0-5694-a98a-59d86fb89606', 4, $smk$4$smk$),
('366b596e-0c25-513f-b46b-d6767cd1ed6c', '39b987c0-e2cf-53e9-8892-1e0da70434fe', 1, $smk$2$smk$),
('64c6b4fe-f361-5858-84ab-c0af22d57ee2', '39b987c0-e2cf-53e9-8892-1e0da70434fe', 2, $smk$3$smk$),
('cbdd6b98-a9a0-5796-8fb4-c9bb5f74574e', '39b987c0-e2cf-53e9-8892-1e0da70434fe', 3, $smk$3.4$smk$),
('e90c9bad-77cf-58c0-ac3b-3fa097c359dd', '39b987c0-e2cf-53e9-8892-1e0da70434fe', 4, $smk$0$smk$),
('71119cc8-fd2c-5d92-8a3c-b15cf1330e1f', '94ea164c-9487-5604-8aaa-3fefb3640b95', 1, $smk$prix_total$smk$),
('7678a795-0909-58a4-9557-a95e504dd38f', '94ea164c-9487-5604-8aaa-3fefb3640b95', 2, $smk$2eme_note$smk$),
('0440dec5-1e94-5d45-807d-115da044366c', '94ea164c-9487-5604-8aaa-3fefb3640b95', 3, $smk$_compteur$smk$),
('36f325b0-5a6b-5bec-bbe1-cb9a95e20331', '94ea164c-9487-5604-8aaa-3fefb3640b95', 4, $smk$nombre-eleves$smk$),
('8ea4a39e-1df8-513f-a895-7c8b858ce877', '6ac0a729-65f1-512b-8a99-c6041523efca', 1, $smk$Vrai$smk$),
('53732d4f-404c-5c17-ac12-fa1ceda7fe8a', '6ac0a729-65f1-512b-8a99-c6041523efca', 2, $smk$Faux$smk$),
('d79f0846-c8cd-50c3-8653-3341985615e0', '74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', 1, $smk$15.4$smk$),
('7fe1a606-283f-57ac-b2ec-839d2e2f154c', '74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', 2, $smk$15.5$smk$),
('834b34c1-5a44-5972-b289-b0ab3f9244a7', '74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', 3, $smk$15.456$smk$),
('d093161f-3449-548a-ad5d-1fa3275c4b28', '74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', 4, $smk${note:.1f}$smk$),
('632c0767-5dfe-57d0-a33c-e7a89c86437e', '66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', 1, $smk$"Âge : " + 25$smk$),
('5b0eceb7-5f6d-5182-a767-57aadd03c203', '66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', 2, $smk$int("vingt")$smk$),
('e4706bf0-1912-595c-8b7b-a2062b0332e6', '66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', 3, $smk$int("20") + 1$smk$),
('3116aec2-9ce5-5ea5-855b-011101262705', '66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', 4, $smk$str(25) + " ans"$smk$),
('8ab67941-a82c-535e-b463-a3cc9ab4688a', 'aab6556c-0f23-5873-a234-d55bf787daec', 1, $smk$Vrai$smk$),
('9cf9a111-f3b6-576a-bf3e-121bb57e9729', 'aab6556c-0f23-5873-a234-d55bf787daec', 2, $smk$Faux$smk$),
('fb075fcd-5c17-5506-b210-258b2b1c25dd', '5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', 1, $smk$10$smk$),
('647b1afd-af68-54f6-ae8b-ae7398f0c382', '5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', 2, $smk$15$smk$),
('c6124ca0-4f90-5e8e-b8ac-c6dadd03f2cb', '5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', 3, $smk$20$smk$),
('0b281b3f-7db7-54b8-88c3-58870f6ba398', '5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', 4, $smk$30$smk$),
('edeb25f6-16e8-5558-ae00-61066d7036fa', '48fcadb4-133a-5d91-b152-2a9dfabd0d89', 1, $smk$=$smk$),
('5fbdd16c-dc3e-51eb-8914-e19c35cdfe2e', '48fcadb4-133a-5d91-b152-2a9dfabd0d89', 2, $smk$==$smk$),
('043157ad-da95-56a4-bc6a-9d3844040e1a', '48fcadb4-133a-5d91-b152-2a9dfabd0d89', 3, $smk$===$smk$),
('787c9c54-c26f-595d-812b-b2f044e544f3', '48fcadb4-133a-5d91-b152-2a9dfabd0d89', 4, $smk$equals$smk$),
('23df9471-386f-5e18-a825-019d03152b6e', 'bcd94236-4942-5270-98a3-969878598671', 1, $smk$A$smk$),
('a44b5656-2b83-5592-9a1a-fd4f59d08f16', 'bcd94236-4942-5270-98a3-969878598671', 2, $smk$B$smk$),
('7ee7cdcc-7bd9-59f9-aa7a-6f56aa7038ab', 'bcd94236-4942-5270-98a3-969878598671', 3, $smk$A puis B$smk$),
('9c30621f-4cb3-53f7-8bd2-1432683fd81d', 'bcd94236-4942-5270-98a3-969878598671', 4, $smk$C$smk$),
('39451af8-fea9-5a82-b136-07b58a6ba538', '8fd1c9f1-4662-5e85-8f14-59d86ff55641', 1, $smk$2, 4, 6, 8$smk$),
('44807d95-99c2-5abf-87a4-92766cc838f1', '8fd1c9f1-4662-5e85-8f14-59d86ff55641', 2, $smk$2, 4, 6$smk$),
('379c1af3-fedc-5cfa-8d1e-c10715fcfda3', '8fd1c9f1-4662-5e85-8f14-59d86ff55641', 3, $smk$2, 3, 4, 5, 6, 7$smk$),
('e96c84b5-2eb2-515c-9737-a06d03c9d588', '8fd1c9f1-4662-5e85-8f14-59d86ff55641', 4, $smk$4, 6, 8$smk$),
('ed73c00d-44b7-5f46-8a73-ea8380340b35', 'ee72c5fb-d492-5865-8c2a-d35d178f2161', 1, $smk$Vrai$smk$),
('dfee922f-1e47-5178-bd84-c27d0f17e4d7', 'ee72c5fb-d492-5865-8c2a-d35d178f2161', 2, $smk$Faux$smk$),
('3cce3a43-1e49-50d5-b36c-f96732049961', '12f0d6ee-6824-56d3-9522-7f873199838b', 1, $smk$age >= 18 and age < 25$smk$),
('d7213cac-db42-5a27-9822-0f6805a156ac', '12f0d6ee-6824-56d3-9522-7f873199838b', 2, $smk$age < 18 or age > 65$smk$),
('7b95ca9b-4e63-5166-a72c-900cc219ecff', '12f0d6ee-6824-56d3-9522-7f873199838b', 3, $smk$not age == 20$smk$),
('2c47a190-ff69-5ab7-b4c8-6caabaa772bd', '12f0d6ee-6824-56d3-9522-7f873199838b', 4, $smk$18 <= age <= 30$smk$),
('67137ff4-3dd6-554a-9b13-0af50eb5a9e8', 'c3aa61c0-f216-5103-8e31-5a7e3b751eb4', 1, $smk$2$smk$),
('bd434c6e-ca10-528c-b638-8b72a77764a4', 'c3aa61c0-f216-5103-8e31-5a7e3b751eb4', 2, $smk$3$smk$),
('e612e23a-c742-5a89-803c-1abbe45a580c', 'c3aa61c0-f216-5103-8e31-5a7e3b751eb4', 3, $smk$5$smk$),
('9adeff69-2eca-5450-9560-842679cf73c3', 'c3aa61c0-f216-5103-8e31-5a7e3b751eb4', 4, $smk$6$smk$),
('fc28b2ef-898f-532f-bec6-7ce32fdb39c5', '249c71a3-eded-5d8f-b524-2f1cded2be75', 1, $smk$1 2$smk$),
('ccd5d5c4-8ca2-5872-93b1-3bf8d9978999', '249c71a3-eded-5d8f-b524-2f1cded2be75', 2, $smk$1 2 3 4 5$smk$),
('fb99a110-abf9-52c7-a0d0-706334e7cbac', '249c71a3-eded-5d8f-b524-2f1cded2be75', 3, $smk$1 2 4 5$smk$),
('2babf15f-d89f-5c44-936e-5b56d2864359', '249c71a3-eded-5d8f-b524-2f1cded2be75', 4, $smk$3$smk$),
('b506e12a-064f-5336-bd7d-ff40f944ab1d', 'd091b533-2e82-5fd9-979c-b5f294c881eb', 1, $smk$Vrai$smk$),
('aa149748-b0e2-5eba-9a27-8077ac81b954', 'd091b533-2e82-5fd9-979c-b5f294c881eb', 2, $smk$Faux$smk$),
('0a0d1f13-f8b7-5d3b-99fb-058ee361e822', '20c96769-cb43-505d-a99e-78bc9eb77e7b', 1, $smk$4$smk$),
('086d264c-2952-51e8-81bc-b187a3c8e26c', '20c96769-cb43-505d-a99e-78bc9eb77e7b', 2, $smk$6$smk$),
('392cd43b-9b08-55d6-8f76-0ffde453c8c0', '20c96769-cb43-505d-a99e-78bc9eb77e7b', 3, $smk$10$smk$),
('c4339600-078f-5205-a66b-9e1b383581dd', '20c96769-cb43-505d-a99e-78bc9eb77e7b', 4, $smk$15$smk$),
('7f43fb99-d7c2-5ba4-922b-b449a2238ac2', '9f96009c-a355-515b-ba8e-26f0028d468d', 1, $smk$Redemander une saisie tant qu'elle est invalide$smk$),
('c2bfb43d-9dd0-5777-b6e6-502e518d5577', '9f96009c-a355-515b-ba8e-26f0028d468d', 2, $smk$Afficher les nombres de 1 à 100$smk$),
('279fcdec-3e70-5264-acfa-ba4fa6b78361', '9f96009c-a355-515b-ba8e-26f0028d468d', 3, $smk$Faire jouer l'utilisateur jusqu'à ce qu'il trouve le nombre secret$smk$),
('5865c492-969b-5503-a84c-a6eab195f19d', '9f96009c-a355-515b-ba8e-26f0028d468d', 4, $smk$Parcourir chaque lettre d'un mot$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('4d482a46-cdc9-5a2d-af30-f6697f046f49', array['0c58d56f-7000-559d-ab48-8f3c1d7b1530']::uuid[], $smk$Les guillemets font de "2" et "3" des chaînes : + les met bout à bout (concaténation) et produit "23".$smk$),
('84bce527-d31c-58d8-8c06-e2106a366e4b', array['d5f150b7-7786-5026-9de5-5b827b4a940c']::uuid[], $smk$input() renvoie toujours une chaîne (str). Il faut la convertir avec int() ou float() pour calculer.$smk$),
('b2342927-e8d0-5694-a98a-59d86fb89606', array['3ff9c563-efcd-5c55-9991-87d79f0e9913']::uuid[], $smk$// est la division entière : 17 = 5 × 3 + 2, le quotient entier est 3.$smk$),
('39b987c0-e2cf-53e9-8892-1e0da70434fe', array['366b596e-0c25-513f-b46b-d6767cd1ed6c']::uuid[], $smk$% donne le reste de la division entière : 17 = 5 × 3 + 2, le reste est 2.$smk$),
('94ea164c-9487-5604-8aaa-3fefb3640b95', array['71119cc8-fd2c-5d92-8a3c-b15cf1330e1f', '0440dec5-1e94-5d45-807d-115da044366c']::uuid[], $smk$Un nom contient lettres, chiffres et _ et ne commence pas par un chiffre. 2eme_note commence par un chiffre ; nombre-eleves contient un tiret, interprété comme une soustraction.$smk$),
('6ac0a729-65f1-512b-8a99-c6041523efca', array['8ea4a39e-1df8-513f-a895-7c8b858ce877']::uuid[], $smk$# introduit un commentaire : il sert aux humains et n'est jamais exécuté.$smk$),
('74729a9e-85a1-5d6e-8c22-ddf5bdebd9e9', array['7fe1a606-283f-57ac-b2ec-839d2e2f154c']::uuid[], $smk$Le format :.1f arrondit à une décimale : 15.456 devient 15.5.$smk$),
('66743abd-4a5e-56ee-acf2-5cfb4d66eeb7', array['632c0767-5dfe-57d0-a33c-e7a89c86437e', '5b0eceb7-5f6d-5182-a767-57aadd03c203']::uuid[], $smk$On ne peut pas additionner un str et un int (TypeError), et "vingt" ne peut pas être converti en entier (ValueError). Les deux autres expressions sont correctes.$smk$),
('aab6556c-0f23-5873-a234-d55bf787daec', array['9cf9a111-f3b6-576a-bf3e-121bb57e9729']::uuid[], $smk$L'opérateur / renvoie toujours un float : 8 / 2 vaut 4.0. Pour un entier, utilisez 8 // 2.$smk$),
('5c8b194b-c3a9-5170-96d1-5e8d4e5b3165', array['0b281b3f-7db7-54b8-88c3-58870f6ba398']::uuid[], $smk$score vaut d'abord 10, puis 10 + 5 = 15, puis 15 × 2 = 30. Chaque affectation remplace l'ancienne valeur.$smk$),
('48fcadb4-133a-5d91-b152-2a9dfabd0d89', array['5fbdd16c-dc3e-51eb-8914-e19c35cdfe2e']::uuid[], $smk$== compare deux valeurs. Un seul = est l'opérateur d'affectation.$smk$),
('bcd94236-4942-5270-98a3-969878598671', array['23df9471-386f-5e18-a825-019d03152b6e']::uuid[], $smk$Python exécute seulement le premier bloc dont la condition est vraie. note >= 12 est vrai, donc il affiche A et ignore la suite, même si note >= 14 est aussi vrai.$smk$),
('8fd1c9f1-4662-5e85-8f14-59d86ff55641', array['44807d95-99c2-5abf-87a4-92766cc838f1']::uuid[], $smk$range part de 2, avance de 2 en 2 et s'arrête avant 8 (borne exclue) : 2, 4, 6.$smk$),
('ee72c5fb-d492-5865-8c2a-d35d178f2161', array['ed73c00d-44b7-5f46-8a73-ea8380340b35']::uuid[], $smk$C'est une boucle infinie. Il faut s'assurer que le bloc modifie ce que teste la condition (ou utiliser break).$smk$),
('12f0d6ee-6824-56d3-9522-7f873199838b', array['3cce3a43-1e49-50d5-b36c-f96732049961', '2c47a190-ff69-5ab7-b4c8-6caabaa772bd']::uuid[], $smk$20 est bien entre 18 et 25, et entre 18 et 30. Il n'est ni < 18 ni > 65, et not (age == 20) vaut False.$smk$),
('c3aa61c0-f216-5103-8e31-5a7e3b751eb4', array['9adeff69-2eca-5450-9560-842679cf73c3']::uuid[], $smk$La boucle intérieure (2 tours) s'exécute entièrement à chacun des 3 tours de la boucle extérieure : 3 × 2 = 6.$smk$),
('249c71a3-eded-5d8f-b524-2f1cded2be75', array['fb99a110-abf9-52c7-a0d0-706334e7cbac']::uuid[], $smk$continue saute la suite du bloc pour n = 3 et passe au tour suivant : 3 n'est pas affiché.$smk$),
('d091b533-2e82-5fd9-979c-b5f294c881eb', array['aa149748-b0e2-5eba-9a27-8077ac81b954']::uuid[], $smk$L'indentation est obligatoire : c'est elle qui délimite le bloc. Sans elle, Python lève une IndentationError.$smk$),
('20c96769-cb43-505d-a99e-78bc9eb77e7b', array['392cd43b-9b08-55d6-8f76-0ffde453c8c0']::uuid[], $smk$La boucle ajoute 1, 2, 3 puis 4 : total = 1 + 2 + 3 + 4 = 10.$smk$),
('9f96009c-a355-515b-ba8e-26f0028d468d', array['7f43fb99-d7c2-5ba4-922b-b449a2238ac2', '279fcdec-3e70-5264-acfa-ba4fa6b78361']::uuid[], $smk$while convient quand le nombre de tours dépend d'une condition imprévisible. Pour un nombre connu de tours ou une séquence, for est plus simple.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

