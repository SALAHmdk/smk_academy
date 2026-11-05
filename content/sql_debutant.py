"""Contenu de la formation « SQL pour débutants » (SMK Academy).

Source de vérité du contenu pédagogique. `scripts/build_seed.py --content sql_debutant`
le transforme en migration SQL idempotente.

Toutes les requêtes s'appliquent à la même petite base « SMK » (étudiants, formations,
inscriptions), donnée en entier dans la leçon 1. Chaque résultat affiché a été vérifié
en exécutant la requête (voir scripts/check_sql_course.py).

Markdown : blocs ```sql pour les requêtes, ```text pour les résultats,
```solution-sql pour les corrections (affichées repliées).
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("sql_debutant_m3_m5", _Path(__file__).with_name("sql_debutant_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "sql-debutant",
    "title": "SQL pour débutants",
    "subtitle": "Interrogez une base de données avec confiance.",
    "description": (
        "Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, "
        "SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première "
        "requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose "
        "des exercices corrigés et chaque module se termine par un quiz noté sur 20."
    ),
    "category": "Bases de données",
    "category_slug": "bases-de-donnees",
    "topic": "SQL",
    "cover_label": "SQL",
    "level": "debutant",
    "duration_minutes": 480,
    "objectives": [
        "Comprendre l'organisation d'une base de données relationnelle",
        "Extraire, filtrer et trier des données avec SELECT",
        "Calculer des statistiques avec GROUP BY et les fonctions d'agrégation",
        "Croiser plusieurs tables avec les jointures",
        "Créer des tables et modifier des données en toute sécurité",
    ],
    "prerequisites": [
        "Savoir utiliser un ordinateur et un navigateur",
        "Aucune connaissance préalable en programmation ou en base de données",
    ],
    "status": "published",
    "is_premium": False,
    "position": 2,
}

# ---------------------------------------------------------------------------
# Module 1 — Découvrir SQL
# ---------------------------------------------------------------------------
M1_L1 = r"""
## À quoi sert une base de données ?

Une application garde en mémoire des milliers d'informations : comptes, commandes, notes, messages… Ces informations sont rangées dans une **base de données**, gérée par un logiciel spécialisé appelé **SGBD** (système de gestion de bases de données) : PostgreSQL, MySQL, SQLite, Oracle ou SQL Server.

La plupart de ces bases sont **relationnelles** : les données y sont rangées dans des **tables**, comme dans un tableur.

- Une **table** regroupe des informations d'un même type (les étudiants, les formations…).
- Chaque **colonne** décrit une caractéristique (le prénom, la ville…).
- Chaque **ligne** (on dit aussi *enregistrement*) correspond à un élément précis : un étudiant, une formation.

## Le langage SQL

**SQL** (*Structured Query Language*) est le langage qui permet de dialoguer avec une base relationnelle. On écrit une **requête**, le SGBD l'exécute et renvoie un résultat, lui aussi présenté sous forme de tableau.

```sql
SELECT prenom, ville FROM etudiants;
```

Cette requête se lit presque comme une phrase : « sélectionne le prénom et la ville dans la table des étudiants ». SQL est un langage **déclaratif** : vous décrivez *ce que vous voulez obtenir*, et le SGBD décide lui-même *comment* aller le chercher.

> SQL est normalisé : les requêtes de cette formation fonctionnent sur PostgreSQL, MySQL et SQLite. Lorsque la syntaxe varie d'un SGBD à l'autre, c'est signalé.

## La base de la formation

Toute la formation utilise la même petite base, celle d'un organisme de formation. Elle contient trois tables.

**etudiants**

| id | prenom | nom | ville | date_naissance | email |
|---|---|---|---|---|---|
| 1 | Amina | Benali | Paris | 2001-03-14 | amina@exemple.fr |
| 2 | Lucas | Martin | Lyon | 1999-11-02 | lucas@exemple.fr |
| 3 | Sofia | Rossi | Paris | 2003-06-25 | *(vide)* |
| 4 | Karim | Haddad | Marseille | 2000-01-30 | karim@exemple.fr |
| 5 | Emma | Dubois | Lille | 2002-09-08 | emma@exemple.fr |
| 6 | Yanis | Morel | Lyon | 1998-04-17 | yanis@exemple.fr |

**formations**

| id | titre | categorie | duree_heures | prix |
|---|---|---|---|---|
| 1 | Python pour débutants | Programmation | 11 | 0 |
| 2 | SQL pour débutants | Bases de données | 8 | 0 |
| 3 | Excel avancé | Business Intelligence | 6 | 49 |
| 4 | Machine Learning | Data Science | 20 | 99 |
| 5 | Anglais professionnel | Langues | 8 | 29 |
| 6 | Docker | Cloud et DevOps | 10 | 39 |

**inscriptions** : qui suit quelle formation, et avec quelle note sur 20.

| id | etudiant_id | formation_id | date_inscription | note |
|---|---|---|---|---|
| 1 | 1 | 1 | 2026-09-01 | 16 |
| 2 | 1 | 2 | 2026-09-15 | 14 |
| 3 | 2 | 1 | 2026-09-03 | 9 |
| 4 | 3 | 4 | 2026-10-01 | 18 |
| 5 | 4 | 2 | 2026-10-05 | *(vide)* |
| 6 | 5 | 3 | 2026-10-10 | 12 |
| 7 | 2 | 5 | 2026-10-12 | 11 |
| 8 | 1 | 4 | 2026-10-20 | *(vide)* |

Remarquez trois choses importantes :

1. Chaque table possède une colonne `id` dont la valeur est **unique** : c'est la **clé primaire**. Elle identifie une ligne sans ambiguïté, même si deux étudiants portent le même nom.
2. La table `inscriptions` ne recopie ni le nom de l'étudiant ni le titre de la formation : elle contient seulement leurs identifiants (`etudiant_id`, `formation_id`). C'est ce lien entre tables qui rend la base **relationnelle**. Vous apprendrez à exploiter ces liens au module 4.
3. Certaines cases sont vides : Sofia n'a pas donné d'email et deux inscriptions n'ont pas encore de note. En SQL, une case vide contient la valeur spéciale **NULL**, qui signifie « inconnu ».

## Où pratiquer ?

Pour exécuter les requêtes de la formation, il suffit d'un navigateur :

1. Ouvrez un outil en ligne gratuit comme **DB Fiddle** (choisissez PostgreSQL) ou **SQLite Online**.
2. Copiez le script de création ci-dessous et exécutez-le une fois : il crée les trois tables et leurs données.
3. Écrivez ensuite vos requêtes à la suite.

```sql
CREATE TABLE etudiants (
  id INTEGER PRIMARY KEY,
  prenom TEXT NOT NULL,
  nom TEXT NOT NULL,
  ville TEXT,
  date_naissance DATE,
  email TEXT UNIQUE
);
CREATE TABLE formations (
  id INTEGER PRIMARY KEY,
  titre TEXT NOT NULL,
  categorie TEXT NOT NULL,
  duree_heures INTEGER NOT NULL,
  prix NUMERIC NOT NULL DEFAULT 0
);
CREATE TABLE inscriptions (
  id INTEGER PRIMARY KEY,
  etudiant_id INTEGER NOT NULL REFERENCES etudiants (id),
  formation_id INTEGER NOT NULL REFERENCES formations (id),
  date_inscription DATE NOT NULL,
  note NUMERIC
);
INSERT INTO etudiants VALUES
  (1, 'Amina', 'Benali', 'Paris', '2001-03-14', 'amina@exemple.fr'),
  (2, 'Lucas', 'Martin', 'Lyon', '1999-11-02', 'lucas@exemple.fr'),
  (3, 'Sofia', 'Rossi', 'Paris', '2003-06-25', NULL),
  (4, 'Karim', 'Haddad', 'Marseille', '2000-01-30', 'karim@exemple.fr'),
  (5, 'Emma', 'Dubois', 'Lille', '2002-09-08', 'emma@exemple.fr'),
  (6, 'Yanis', 'Morel', 'Lyon', '1998-04-17', 'yanis@exemple.fr');
INSERT INTO formations VALUES
  (1, 'Python pour débutants', 'Programmation', 11, 0),
  (2, 'SQL pour débutants', 'Bases de données', 8, 0),
  (3, 'Excel avancé', 'Business Intelligence', 6, 49),
  (4, 'Machine Learning', 'Data Science', 20, 99),
  (5, 'Anglais professionnel', 'Langues', 8, 29),
  (6, 'Docker', 'Cloud et DevOps', 10, 39);
INSERT INTO inscriptions VALUES
  (1, 1, 1, '2026-09-01', 16),
  (2, 1, 2, '2026-09-15', 14),
  (3, 2, 1, '2026-09-03', 9),
  (4, 3, 4, '2026-10-01', 18),
  (5, 4, 2, '2026-10-05', NULL),
  (6, 5, 3, '2026-10-10', 12),
  (7, 2, 5, '2026-10-12', 11),
  (8, 1, 4, '2026-10-20', NULL);
```

Ne cherchez pas encore à comprendre chaque mot de ce script : `CREATE TABLE` et `INSERT` sont expliqués au module 5.

## À retenir

- Une base relationnelle range les données dans des **tables** faites de **colonnes** et de **lignes**.
- **SQL** est le langage qui interroge et modifie ces tables ; il est commun à tous les grands SGBD.
- La **clé primaire** (`id`) identifie chaque ligne de façon unique.
- Les tables sont reliées entre elles par des identifiants (`etudiant_id`, `formation_id`).
- **NULL** représente une valeur inconnue ou absente.

## Exercices

### Exercice 1 — Lire une table

En vous aidant uniquement des tableaux ci-dessus, répondez : combien de formations sont gratuites ? Dans quelle ville habite l'étudiant n° 4 ? Quelle note a obtenue l'étudiant n° 2 à la formation n° 5 ?

```solution-text
- Deux formations sont gratuites (prix = 0) : « Python pour débutants » et « SQL pour débutants ».
- L'étudiant n° 4, Karim Haddad, habite à Marseille.
- L'inscription n° 7 relie l'étudiant 2 (Lucas) à la formation 5 (Anglais professionnel) : sa note est 11.
```

### Exercice 2 — Suivre les identifiants

Amina (id 1) est inscrite à plusieurs formations. Lesquelles, et lesquelles ne sont pas encore notées ?

```solution-text
La table inscriptions contient trois lignes avec etudiant_id = 1 :
- formation 1 « Python pour débutants » : note 16 ;
- formation 2 « SQL pour débutants » : note 14 ;
- formation 4 « Machine Learning » : note NULL, donc pas encore notée.
```
"""

M1_L2 = r"""
## La requête SELECT

`SELECT` est l'instruction la plus utilisée en SQL : elle **lit** des données sans jamais les modifier. Sa forme minimale comporte deux mots-clés :

```sql
SELECT colonnes
FROM table;
```

- `SELECT` liste les colonnes à afficher, séparées par des virgules ;
- `FROM` indique la table à lire ;
- le point-virgule `;` termine la requête.

```sql
SELECT prenom, nom, ville
FROM etudiants;
```

```text
prenom | nom    | ville
-------+--------+----------
Amina  | Benali | Paris
Lucas  | Martin | Lyon
Sofia  | Rossi  | Paris
Karim  | Haddad | Marseille
Emma   | Dubois | Lille
Yanis  | Morel  | Lyon
```

Les colonnes apparaissent dans l'ordre où vous les avez écrites, pas dans l'ordre de la table.

> Les mots-clés SQL ne sont pas sensibles à la casse : `select`, `SELECT` et `Select` sont équivalents. L'usage est d'écrire les mots-clés en MAJUSCULES et les noms de tables et de colonnes en minuscules, pour une lecture plus facile. Les retours à la ligne sont libres.

## Toutes les colonnes : l'étoile

L'astérisque `*` signifie « toutes les colonnes » :

```sql
SELECT * FROM formations;
```

C'est pratique pour découvrir une table. Dans une application, préférez lister les colonnes utiles : la requête reste lisible et ne renvoie pas de données superflues.

## Calculer dans un SELECT

Une colonne du résultat peut être une **expression** : un calcul effectué pour chaque ligne. Les opérateurs arithmétiques habituels sont disponibles : `+`, `-`, `*`, `/`.

```sql
SELECT titre, duree_heures * 60 AS duree_minutes
FROM formations;
```

```text
titre                 | duree_minutes
----------------------+--------------
Python pour débutants | 660
SQL pour débutants    | 480
Excel avancé          | 360
Machine Learning      | 1200
Anglais professionnel | 480
Docker                | 600
```

Le calcul ne modifie pas la table : il produit seulement une colonne dans le résultat.

## Renommer une colonne avec AS

Le mot-clé `AS` donne un nom (un **alias**) à une colonne du résultat. Sans alias, le SGBD invente un nom peu lisible comme `?column?` ou `duree_heures * 60`.

```sql
SELECT prenom AS "Prénom", ville AS "Ville de résidence"
FROM etudiants;
```

Les **guillemets doubles** permettent un alias avec majuscules, accents ou espaces. Les **apostrophes** (guillemets simples), elles, servent aux **valeurs texte** : `'Paris'`. Ne les confondez pas.

## Supprimer les doublons avec DISTINCT

Plusieurs étudiants habitent la même ville. Pour obtenir chaque ville **une seule fois**, ajoutez `DISTINCT` juste après `SELECT` :

```sql
SELECT DISTINCT ville
FROM etudiants;
```

```text
ville
---------
Paris
Lyon
Marseille
Lille
```

Sans `DISTINCT`, la requête renverrait six lignes, dont Paris et Lyon en double. L'ordre des lignes n'est pas garanti tant que vous ne le demandez pas explicitement (leçon « Trier et limiter »).

## Pièges fréquents

- Oublier la virgule entre deux colonnes : `SELECT prenom nom FROM etudiants` ne provoque pas d'erreur, mais affiche la colonne `prenom` **renommée** en `nom` !
- Mettre une virgule après la dernière colonne : `SELECT prenom, nom, FROM etudiants` est une erreur de syntaxe.
- Écrire une valeur texte entre guillemets doubles : en PostgreSQL, `"Paris"` désigne une colonne nommée Paris, pas le texte Paris.

## À retenir

- `SELECT colonnes FROM table;` lit des données sans les modifier.
- `*` sélectionne toutes les colonnes.
- On peut calculer des expressions et les nommer avec `AS`.
- `DISTINCT` supprime les lignes en double du résultat.
- Apostrophes pour les valeurs texte, guillemets doubles pour les noms.

## Exercices

### Exercice 1 — Catalogue

Affichez le titre et le prix de chaque formation, en nommant les colonnes « Formation » et « Prix (€) ».

```solution-sql
SELECT titre AS "Formation", prix AS "Prix (€)"
FROM formations;
```

### Exercice 2 — Catégories

Affichez la liste des catégories de formation, chacune une seule fois.

```solution-sql
SELECT DISTINCT categorie
FROM formations;
-- 6 lignes : chaque formation a ici sa propre catégorie.
```

### Exercice 3 — Prix pour un groupe

Un groupe de 10 personnes s'inscrit à chaque formation. Affichez le titre et le montant total pour le groupe dans une colonne `prix_groupe`.

```solution-sql
SELECT titre, prix * 10 AS prix_groupe
FROM formations;
-- Machine Learning : 990, Excel avancé : 490, Docker : 390…
```
"""

M1_L3 = r"""
## Filtrer les lignes avec WHERE

`SELECT` choisit les **colonnes** ; `WHERE` choisit les **lignes**. Seules les lignes pour lesquelles la condition est vraie apparaissent dans le résultat.

```sql
SELECT prenom, nom
FROM etudiants
WHERE ville = 'Paris';
```

```text
prenom | nom
-------+-------
Amina  | Benali
Sofia  | Rossi
```

`WHERE` se place toujours **après** `FROM`. En SQL, l'égalité s'écrit avec un seul signe `=` (contrairement à Python).

## Les opérateurs de comparaison

| Opérateur | Signification |
|---|---|
| `=` | égal à |
| `<>` (ou `!=`) | différent de |
| `<`, `<=` | inférieur, inférieur ou égal |
| `>`, `>=` | supérieur, supérieur ou égal |

Ils fonctionnent avec les nombres, les textes (ordre alphabétique) et les dates (ordre chronologique) :

```sql
SELECT prenom, date_naissance
FROM etudiants
WHERE date_naissance >= '2002-01-01';
-- Sofia (2003-06-25) et Emma (2002-09-08)
```

## Combiner des conditions : AND, OR, NOT

- `AND` : les deux conditions doivent être vraies ;
- `OR` : au moins une des deux ;
- `NOT` : inverse une condition.

```sql
SELECT titre, prix
FROM formations
WHERE prix > 0 AND duree_heures <= 10;
```

```text
titre                 | prix
----------------------+-----
Excel avancé          | 49
Anglais professionnel | 29
Docker                | 39
```

`AND` est évalué **avant** `OR`, comme la multiplication avant l'addition. En cas de doute, utilisez des parenthèses :

```sql
SELECT prenom, ville
FROM etudiants
WHERE (ville = 'Paris' OR ville = 'Lyon') AND date_naissance < '2000-01-01';
-- Lucas (Lyon, 1999) et Yanis (Lyon, 1998)
```

Sans les parenthèses, la requête signifierait « Paris, ou bien (Lyon et né avant 2000) » : Amina et Sofia apparaîtraient aussi.

## Raccourcis utiles

**IN** teste l'appartenance à une liste :

```sql
SELECT titre
FROM formations
WHERE categorie IN ('Langues', 'Data Science');
-- Machine Learning, Anglais professionnel
```

**BETWEEN** teste un intervalle, **bornes comprises** :

```sql
SELECT titre, duree_heures
FROM formations
WHERE duree_heures BETWEEN 8 AND 11;
-- Python (11), SQL (8), Anglais (8), Docker (10)
```

**LIKE** recherche un motif dans un texte : `%` remplace n'importe quelle suite de caractères (même vide), `_` remplace exactement un caractère.

```sql
SELECT prenom, nom
FROM etudiants
WHERE nom LIKE 'M%';
-- Lucas Martin, Yanis Morel
```

> En PostgreSQL, `LIKE` distingue majuscules et minuscules (`'m%'` ne trouverait rien) ; utilisez `ILIKE` pour l'ignorer. En MySQL et SQLite, `LIKE` ignore la casse par défaut.

## Le cas particulier de NULL

`NULL` signifie « valeur inconnue ». On ne peut donc pas le comparer avec `=` : `email = NULL` n'est jamais vrai, pas même pour Sofia. Il faut utiliser `IS NULL` ou `IS NOT NULL` :

```sql
SELECT prenom
FROM etudiants
WHERE email IS NULL;
-- Sofia
```

C'est l'une des erreurs les plus fréquentes en SQL : retenez-la dès maintenant.

## À retenir

- `WHERE` filtre les lignes ; il se place après `FROM`.
- Comparaisons : `=`, `<>`, `<`, `<=`, `>`, `>=`.
- `AND` passe avant `OR` : mettez des parenthèses dès que vous mélangez les deux.
- `IN` (liste), `BETWEEN` (intervalle, bornes incluses), `LIKE` (motif avec `%` et `_`).
- `NULL` se teste uniquement avec `IS NULL` / `IS NOT NULL`.

## Exercices

### Exercice 1 — Formations longues

Affichez le titre et la durée des formations de plus de 10 heures.

```solution-sql
SELECT titre, duree_heures
FROM formations
WHERE duree_heures > 10;
-- Python pour débutants (11), Machine Learning (20)
```

### Exercice 2 — Inscriptions à noter

Affichez l'identifiant des inscriptions qui n'ont pas encore de note.

```solution-sql
SELECT id
FROM inscriptions
WHERE note IS NULL;
-- 5 et 8. Attention : WHERE note = NULL ne renverrait aucune ligne.
```

### Exercice 3 — Recherche dans le catalogue

Affichez les formations payantes dont le titre contient la lettre « e » minuscule, en excluant la catégorie « Data Science ».

```solution-sql
SELECT titre, prix
FROM formations
WHERE prix > 0
  AND titre LIKE '%e%'
  AND categorie <> 'Data Science';
-- Excel avancé, Anglais professionnel, Docker
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Trier, limiter et transformer
# ---------------------------------------------------------------------------
M2_L1 = r"""
## Trier avec ORDER BY

Sans instruction de tri, l'ordre des lignes renvoyées par une requête **n'est pas garanti** : il peut changer d'une exécution à l'autre. Pour un ordre précis, ajoutez `ORDER BY` à la fin de la requête.

```sql
SELECT titre, prix
FROM formations
ORDER BY prix;
```

Le tri est **croissant** par défaut (`ASC`, *ascending*). Pour un ordre **décroissant**, ajoutez `DESC` :

```sql
SELECT titre, prix
FROM formations
ORDER BY prix DESC;
```

## Trier sur plusieurs colonnes

Deux formations sont gratuites : laquelle afficher en premier ? Ajoutez un second critère, utilisé seulement en cas d'égalité sur le premier :

```sql
SELECT titre, prix
FROM formations
ORDER BY prix DESC, titre;
```

```text
titre                 | prix
----------------------+-----
Machine Learning      | 99
Excel avancé          | 49
Docker                | 39
Anglais professionnel | 29
Python pour débutants | 0
SQL pour débutants    | 0
```

Chaque critère a son propre sens de tri : ici `prix` est décroissant et `titre` croissant (alphabétique).

On peut aussi trier sur un alias défini dans le `SELECT` :

```sql
SELECT titre, duree_heures * 60 AS minutes
FROM formations
ORDER BY minutes DESC;
```

## Limiter le nombre de lignes

`LIMIT n` ne garde que les `n` premières lignes du résultat. Combiné à `ORDER BY`, il répond aux questions du type « les 3 plus… » :

```sql
SELECT prenom, date_naissance
FROM etudiants
ORDER BY date_naissance
LIMIT 3;
```

```text
prenom | date_naissance
-------+---------------
Yanis  | 1998-04-17
Lucas  | 1999-11-02
Karim  | 2000-01-30
```

Les trois étudiants les plus âgés sont ceux dont la date de naissance est la plus ancienne.

> `LIMIT` sans `ORDER BY` renvoie des lignes au hasard de l'organisation interne de la table : combinez-les toujours. `LIMIT` est accepté par PostgreSQL, MySQL et SQLite ; la norme SQL écrit aussi `FETCH FIRST 3 ROWS ONLY` (PostgreSQL, Oracle, SQL Server).

## Paginer avec OFFSET

`OFFSET n` saute les `n` premières lignes. C'est le principe de la **pagination** d'un site (« page suivante ») :

```sql
-- Page 2, avec 2 étudiants par page
SELECT prenom, date_naissance
FROM etudiants
ORDER BY date_naissance
LIMIT 2 OFFSET 2;
-- Karim (2000-01-30), Amina (2001-03-14)
```

Pour la page `p` avec `n` lignes par page : `LIMIT n OFFSET (p - 1) × n`.

## L'ordre d'écriture des clauses

Les clauses s'écrivent toujours dans cet ordre :

```sql
SELECT colonnes
FROM table
WHERE condition
ORDER BY tri
LIMIT nombre OFFSET décalage;
```

Écrire `ORDER BY` avant `WHERE` provoque une erreur de syntaxe.

## À retenir

- Sans `ORDER BY`, l'ordre du résultat n'est pas garanti.
- `ASC` (par défaut) pour croissant, `DESC` pour décroissant, critère par critère.
- `LIMIT` garde les premières lignes ; `OFFSET` en saute.
- Ordre des clauses : `SELECT … FROM … WHERE … ORDER BY … LIMIT … OFFSET …`.

## Exercices

### Exercice 1 — Le plus long

Affichez le titre de la formation la plus longue.

```solution-sql
SELECT titre
FROM formations
ORDER BY duree_heures DESC
LIMIT 1;
-- Machine Learning (20 heures)
```

### Exercice 2 — Classement des notes

Affichez les inscriptions notées (identifiant et note), de la meilleure à la moins bonne note.

```solution-sql
SELECT id, note
FROM inscriptions
WHERE note IS NOT NULL
ORDER BY note DESC;
-- 4 (18), 1 (16), 2 (14), 6 (12), 7 (11), 3 (9)
```

### Exercice 3 — Annuaire alphabétique

Affichez nom et prénom des étudiants triés par ville, puis par nom dans chaque ville. N'affichez que les 4 premiers.

```solution-sql
SELECT ville, nom, prenom
FROM etudiants
ORDER BY ville, nom
LIMIT 4;
-- Lille Dubois, Lyon Martin, Lyon Morel, Marseille Haddad
```
"""

M2_L2 = r"""
## Les fonctions SQL

Une **fonction** prend une ou plusieurs valeurs et renvoie un résultat. Elle s'applique ligne par ligne, dans le `SELECT` comme dans le `WHERE`. Les plus courantes sont communes à tous les SGBD.

## Fonctions sur le texte

| Fonction | Rôle | Exemple | Résultat |
|---|---|---|---|
| `UPPER(t)` | met en majuscules | `UPPER('Lyon')` | `LYON` |
| `LOWER(t)` | met en minuscules | `LOWER('SQL')` | `sql` |
| `LENGTH(t)` | nombre de caractères | `LENGTH('Emma')` | `4` |
| `SUBSTR(t, début, n)` | extrait `n` caractères | `SUBSTR('Benali', 1, 3)` | `Ben` |
| `TRIM(t)` | supprime les espaces au début et à la fin | `TRIM('  SQL ')` | `SQL` |

L'opérateur `||` **concatène** (met bout à bout) deux textes :

```sql
SELECT UPPER(nom) AS nom,
       prenom || ' ' || nom AS nom_complet,
       LENGTH(prenom) AS lettres
FROM etudiants
WHERE ville = 'Lyon';
```

```text
nom    | nom_complet  | lettres
-------+--------------+--------
MARTIN | Lucas Martin | 5
MOREL  | Yanis Morel  | 5
```

> MySQL n'accepte pas `||` pour concaténer par défaut : utilisez `CONCAT(prenom, ' ', nom)`, qui fonctionne aussi en PostgreSQL.

Les fonctions servent aussi à filtrer sans se soucier de la casse :

```sql
SELECT prenom FROM etudiants WHERE LOWER(ville) = 'paris';
```

## Fonctions numériques

- `ROUND(x, n)` arrondit à `n` décimales : `ROUND(13.333, 1)` donne `13.3` ;
- `ABS(x)` renvoie la valeur absolue ;
- les opérateurs `+ - * /` et `%` (reste de la division, `MOD` en Oracle).

Attention à la **division entière** : en PostgreSQL et SQLite, `7 / 2` vaut `3` lorsque les deux nombres sont des entiers. Écrivez `7 / 2.0` pour obtenir `3.5`.

## Remplacer NULL avec COALESCE

`COALESCE(a, b, …)` renvoie la première valeur **non NULL** de la liste. C'est le moyen standard d'afficher une valeur par défaut :

```sql
SELECT prenom, COALESCE(email, 'non renseigné') AS email
FROM etudiants;
```

```text
prenom | email
-------+-----------------
Amina  | amina@exemple.fr
Lucas  | lucas@exemple.fr
Sofia  | non renseigné
Karim  | karim@exemple.fr
Emma   | emma@exemple.fr
Yanis  | yanis@exemple.fr
```

Pourquoi est-ce important ? Parce que **toute opération avec NULL donne NULL** : `NULL + 1` vaut `NULL`, `'Bonjour ' || NULL` vaut `NULL` (sauf en Oracle). `COALESCE` évite ces « trous » dans les résultats.

## Les dates

Les dates s'écrivent au format international `'AAAA-MM-JJ'` et se comparent naturellement. `CURRENT_DATE` renvoie la date du jour :

```sql
SELECT id, date_inscription
FROM inscriptions
WHERE date_inscription < CURRENT_DATE;
```

Les fonctions de calcul sur les dates (ajouter un mois, extraire l'année…) varient beaucoup d'un SGBD à l'autre : `EXTRACT(YEAR FROM d)` en PostgreSQL et MySQL, `strftime('%Y', d)` en SQLite. Consultez la documentation de votre SGBD le moment venu.

## À retenir

- Les fonctions s'appliquent ligne par ligne, dans `SELECT` et `WHERE`.
- Texte : `UPPER`, `LOWER`, `LENGTH`, `SUBSTR`, `TRIM`, concaténation `||` (ou `CONCAT`).
- Nombres : `ROUND`, `ABS` ; attention à la division entière.
- Toute opération avec `NULL` donne `NULL` ; `COALESCE` fournit une valeur de remplacement.
- Dates au format `'AAAA-MM-JJ'`, date du jour avec `CURRENT_DATE`.

## Exercices

### Exercice 1 — Initiales

Affichez pour chaque étudiant ses initiales (première lettre du prénom et du nom), par exemple `AB` pour Amina Benali.

```solution-sql
SELECT prenom, nom, SUBSTR(prenom, 1, 1) || SUBSTR(nom, 1, 1) AS initiales
FROM etudiants;
-- AB, LM, SR, KH, ED, YM
```

### Exercice 2 — Notes affichables

Affichez l'identifiant de chaque inscription et sa note, en remplaçant les notes manquantes par 0 dans une colonne `note_affichee`.

```solution-sql
SELECT id, COALESCE(note, 0) AS note_affichee
FROM inscriptions;
-- Les inscriptions 5 et 8 affichent 0.
```

### Exercice 3 — Prix horaire

Affichez le titre des formations payantes et leur prix par heure, arrondi à deux décimales.

```solution-sql
SELECT titre, ROUND(prix / duree_heures, 2) AS prix_horaire
FROM formations
WHERE prix > 0;
-- Excel avancé 8.17, Machine Learning 4.95, Anglais professionnel 3.63, Docker 3.9
-- (prix est de type NUMERIC : la division n'est pas entière.)
```
"""

M2_L3 = r"""
## Choisir une valeur selon une condition : CASE

`CASE` est l'équivalent SQL du « si… sinon… ». Il produit une valeur différente selon les conditions, pour chaque ligne :

```sql
CASE
  WHEN condition1 THEN valeur1
  WHEN condition2 THEN valeur2
  ELSE valeur_par_defaut
END
```

Les conditions sont testées **dans l'ordre** ; la première vraie l'emporte et les suivantes sont ignorées. Si aucune n'est vraie et qu'il n'y a pas de `ELSE`, le résultat est `NULL`.

## Un premier exemple

```sql
SELECT titre,
       CASE WHEN prix = 0 THEN 'Gratuite' ELSE 'Payante' END AS acces
FROM formations;
```

```text
titre                 | acces
----------------------+---------
Python pour débutants | Gratuite
SQL pour débutants    | Gratuite
Excel avancé          | Payante
Machine Learning      | Payante
Anglais professionnel | Payante
Docker                | Payante
```

## Plusieurs cas : attribuer une mention

```sql
SELECT id, note,
       CASE
         WHEN note >= 16 THEN 'Très bien'
         WHEN note >= 10 THEN 'Validé'
         WHEN note IS NULL THEN 'En cours'
         ELSE 'À retravailler'
       END AS mention
FROM inscriptions;
```

```text
id | note | mention
---+------+---------------
1  | 16   | Très bien
2  | 14   | Validé
3  | 9    | À retravailler
4  | 18   | Très bien
5  | NULL | En cours
6  | 12   | Validé
7  | 11   | Validé
8  | NULL | En cours
```

L'**ordre des conditions** compte : la note 18 vérifie à la fois `>= 16` et `>= 10`, mais c'est la première condition vraie (`Très bien`) qui est retenue. Si l'on testait `>= 10` en premier, aucune note n'obtiendrait jamais « Très bien ».

Notez aussi le traitement de `NULL` : sans la ligne `WHEN note IS NULL`, les inscriptions non notées tomberaient dans le `ELSE` et recevraient « À retravailler », ce qui serait faux.

## CASE ailleurs que dans SELECT

`CASE` peut servir dans `ORDER BY` pour imposer un ordre personnalisé :

```sql
SELECT prenom, ville
FROM etudiants
ORDER BY CASE WHEN ville = 'Paris' THEN 0 ELSE 1 END, prenom;
-- Les Parisiennes d'abord (Amina, Sofia), puis les autres par ordre alphabétique.
```

Il servira aussi au module 3 pour compter selon une condition, à l'intérieur d'une agrégation.

## À retenir

- `CASE WHEN … THEN … ELSE … END` choisit une valeur ligne par ligne.
- La première condition vraie l'emporte : écrivez les cas du plus précis au plus général.
- Sans `ELSE`, une ligne qui ne vérifie aucune condition reçoit `NULL`.
- Pensez à traiter `NULL` explicitement avec `IS NULL`.
- `CASE` s'utilise dans `SELECT`, `WHERE`, `ORDER BY` et dans les agrégations.

## Exercices

### Exercice 1 — Format des formations

Affichez le titre de chaque formation et une colonne `format` valant « Courte » (moins de 8 heures), « Standard » (de 8 à 12 heures) ou « Longue » (plus de 12 heures).

```solution-sql
SELECT titre,
       CASE
         WHEN duree_heures < 8 THEN 'Courte'
         WHEN duree_heures <= 12 THEN 'Standard'
         ELSE 'Longue'
       END AS format
FROM formations;
-- Excel avancé : Courte ; Machine Learning : Longue ; toutes les autres : Standard.
```

### Exercice 2 — Repérer les erreurs

Pourquoi cette requête n'affiche-t-elle jamais « Excellent » ? Corrigez-la.

```sql
SELECT id,
       CASE
         WHEN note >= 10 THEN 'Admis'
         WHEN note >= 16 THEN 'Excellent'
         ELSE 'Non admis'
       END AS resultat
FROM inscriptions;
```

```solution-sql
-- Toute note >= 16 est aussi >= 10 : la première condition l'emporte toujours.
-- Il faut tester le cas le plus exigeant en premier, et traiter NULL.
SELECT id,
       CASE
         WHEN note >= 16 THEN 'Excellent'
         WHEN note >= 10 THEN 'Admis'
         WHEN note IS NULL THEN 'Non noté'
         ELSE 'Non admis'
       END AS resultat
FROM inscriptions;
```
"""

# ---------------------------------------------------------------------------
# Quiz : (kind, prompt, code, [options], [indices des bonnes réponses], explication)
# ---------------------------------------------------------------------------
QUIZ_M1 = [
    ("single", "Dans une table, que représente une ligne ?", None,
     ["Une caractéristique commune à tous les éléments", "Un élément précis, par exemple un étudiant",
      "Le type de données d'une colonne", "Une requête enregistrée"], [1],
     "Une ligne (ou enregistrement) décrit un élément précis ; les colonnes décrivent les caractéristiques communes à tous les éléments."),
    ("single", "À quoi sert la clé primaire d'une table ?", None,
     ["À trier automatiquement les lignes", "À identifier chaque ligne de manière unique",
      "À chiffrer les données", "À relier la table à Internet"], [1],
     "La clé primaire (souvent id) prend une valeur différente pour chaque ligne : elle permet de désigner une ligne sans ambiguïté, même si deux étudiants ont le même nom."),
    ("single", "Que renvoie cette requête ?", "SELECT DISTINCT ville FROM etudiants;",
     ["6 lignes, une par étudiant", "4 lignes, une par ville différente", "1 ligne : le nombre de villes", "Une erreur"], [1],
     "DISTINCT supprime les doublons : Paris et Lyon apparaissent deux fois dans la table mais une seule fois dans le résultat, soit 4 villes."),
    ("single", "Quelle requête affiche uniquement les étudiants habitant à Lyon ?", None,
     ["SELECT * FROM etudiants WHERE ville = \"Lyon\";", "SELECT * FROM etudiants WHERE ville == 'Lyon';",
      "SELECT * FROM etudiants WHERE ville = 'Lyon';", "SELECT * WHERE ville = 'Lyon' FROM etudiants;"], [2],
     "En SQL, l'égalité s'écrit avec un seul = et les valeurs texte entre apostrophes. Les guillemets doubles désignent un nom de colonne, == n'existe pas et WHERE se place après FROM."),
    ("multiple", "Quelles conditions sélectionnent Sofia, qui n'a pas d'email ?", None,
     ["WHERE email IS NULL", "WHERE email = NULL", "WHERE email IS NOT NULL", "WHERE prenom = 'Sofia'"], [0, 3],
     "NULL ne se compare jamais avec = : email = NULL n'est vrai pour aucune ligne. IS NULL fonctionne, tout comme un filtre sur le prénom. IS NOT NULL sélectionne au contraire les cinq autres."),
    ("single", "Combien de lignes renvoie cette requête ?", "SELECT titre FROM formations\nWHERE duree_heures BETWEEN 8 AND 10;",
     ["1", "2", "3", "4"], [2],
     "BETWEEN inclut ses bornes : SQL (8 h), Anglais professionnel (8 h) et Docker (10 h) sont retenues, soit 3 lignes. Python (11 h) est exclue."),
    ("single", "Quel motif trouve tous les noms qui se terminent par « i » ?", None,
     ["LIKE 'i%'", "LIKE '%i'", "LIKE '_i'", "LIKE '%i%'"], [1],
     "% remplace n'importe quelle suite de caractères. '%i' signifie « n'importe quoi puis un i final ». 'i%' cherche un i au début, '_i' exactement deux caractères, '%i%' un i n'importe où."),
    ("single", "Que renvoie cette requête ?", "SELECT prenom FROM etudiants\nWHERE ville = 'Paris' OR ville = 'Lyon' AND date_naissance < '2000-01-01';",
     ["Lucas et Yanis", "Amina, Sofia, Lucas et Yanis", "Amina et Sofia", "Aucune ligne"], [1],
     "AND est évalué avant OR : la condition se lit « Paris, OU (Lyon ET né avant 2000) ». Amina et Sofia (Paris) sont donc retenues, ainsi que Lucas et Yanis. Des parenthèses autour du OR auraient donné seulement Lucas et Yanis."),
    ("true_false", "Une requête SELECT peut modifier les données d'une table.", None,
     ["Vrai", "Faux"], [1],
     "SELECT ne fait que lire. Un calcul comme prix * 10 produit une colonne dans le résultat, sans toucher à la table. Les modifications se font avec INSERT, UPDATE et DELETE."),
    ("single", "Qu'affiche cette requête ?", "SELECT prenom nom FROM etudiants;",
     ["Les prénoms et les noms", "Une erreur de syntaxe", "Les prénoms, dans une colonne intitulée « nom »", "Les noms seulement"], [2],
     "Sans virgule, le second mot est interprété comme un alias (le mot AS est facultatif). La requête affiche donc la colonne prenom renommée en nom : un piège classique."),
]

QUIZ_M2 = [
    ("single", "Quelle clause trie les formations de la plus chère à la moins chère ?", None,
     ["ORDER BY prix", "ORDER BY prix DESC", "SORT BY prix DESC", "ORDER prix DESC"], [1],
     "ORDER BY trie et DESC impose l'ordre décroissant. Sans DESC, le tri est croissant (ASC). SORT BY n'existe pas en SQL standard."),
    ("true_false", "Sans ORDER BY, les lignes sont toujours renvoyées dans l'ordre de leur insertion.", None,
     ["Vrai", "Faux"], [1],
     "L'ordre n'est garanti que par ORDER BY. Le SGBD peut renvoyer les lignes dans n'importe quel ordre, qui peut changer d'une exécution à l'autre."),
    ("single", "Quelle requête affiche la page 3 d'une liste, à raison de 10 étudiants par page ?", None,
     ["... LIMIT 10 OFFSET 30", "... LIMIT 10 OFFSET 20", "... LIMIT 30 OFFSET 10", "... LIMIT 3 OFFSET 10"], [1],
     "Pour la page p avec n lignes par page : LIMIT n OFFSET (p − 1) × n. Page 3 : on saute les 20 premières lignes et on en garde 10."),
    ("single", "Quel est l'ordre correct des clauses ?", None,
     ["SELECT, FROM, ORDER BY, WHERE, LIMIT", "SELECT, WHERE, FROM, ORDER BY, LIMIT",
      "SELECT, FROM, WHERE, ORDER BY, LIMIT", "FROM, SELECT, WHERE, LIMIT, ORDER BY"], [2],
     "Les clauses s'écrivent toujours SELECT … FROM … WHERE … ORDER BY … LIMIT. Tout autre ordre provoque une erreur de syntaxe."),
    ("single", "Que vaut l'expression suivante ?", "COALESCE(NULL, NULL, 'Lyon', 'Paris')",
     ["NULL", "'Lyon'", "'Paris'", "Une erreur"], [1],
     "COALESCE renvoie la première valeur non NULL de la liste, en partant de la gauche : 'Lyon'."),
    ("single", "Que vaut NULL + 5 ?", None,
     ["5", "0", "NULL", "Une erreur"], [2],
     "Toute opération arithmétique avec NULL donne NULL : une valeur inconnue plus 5 reste inconnue. COALESCE(note, 0) + 5 vaudrait 5."),
    ("single", "Que renvoie UPPER(SUBSTR('benali', 1, 3)) ?", None,
     ["'BENALI'", "'BEN'", "'ben'", "'ALI'"], [1],
     "SUBSTR extrait 3 caractères à partir du premier : 'ben'. UPPER les met ensuite en majuscules : 'BEN'."),
    ("single", "Quelle mention reçoit une note de 18 avec ce CASE ?", "CASE\n  WHEN note >= 10 THEN 'Validé'\n  WHEN note >= 16 THEN 'Très bien'\n  ELSE 'Non validé'\nEND",
     ["Validé", "Très bien", "Non validé", "NULL"], [0],
     "La première condition vraie l'emporte : 18 >= 10, donc « Validé », et la suite n'est pas testée. Il faudrait tester >= 16 en premier."),
    ("true_false", "Un CASE sans ELSE renvoie NULL pour les lignes qui ne vérifient aucune condition.", None,
     ["Vrai", "Faux"], [0],
     "C'est le comportement standard : sans ELSE, la valeur par défaut est NULL. Pensez à prévoir un ELSE ou à traiter explicitement les cas restants."),
    ("multiple", "Quelles requêtes affichent les 2 formations les plus courtes ?", None,
     ["SELECT titre FROM formations ORDER BY duree_heures LIMIT 2;",
      "SELECT titre FROM formations ORDER BY duree_heures ASC LIMIT 2;",
      "SELECT titre FROM formations LIMIT 2;",
      "SELECT titre FROM formations ORDER BY duree_heures DESC LIMIT 2;"], [0, 1],
     "Le tri croissant (ASC est la valeur par défaut) met les plus courtes en premier. Sans ORDER BY, LIMIT renvoie deux lignes quelconques ; avec DESC, on obtiendrait les plus longues."),
]

MODULES = [
    {
        "position": 1,
        "title": "Découvrir SQL",
        "description": "Comprendre une base relationnelle, lire des tables avec SELECT et filtrer avec WHERE.",
        "status": "published",
        "lessons": [
            ("bases-de-donnees-relationnelles", "Bases de données relationnelles et SQL",
             "Tables, lignes, colonnes, clé primaire, NULL et la base de la formation.", M1_L1, 20),
            ("select", "Lire des données avec SELECT",
             "Choisir des colonnes, calculer, renommer avec AS, supprimer les doublons.", M1_L2, 25),
            ("where", "Filtrer avec WHERE",
             "Comparaisons, AND/OR/NOT, IN, BETWEEN, LIKE et IS NULL.", M1_L3, 30),
        ],
        "quiz": ("Quiz — Découvrir SQL", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Trier, limiter et transformer",
        "description": "Ordonner les résultats, paginer, utiliser les fonctions et CASE.",
        "status": "published",
        "lessons": [
            ("order-by-limit", "Trier et limiter les résultats",
             "ORDER BY, ASC/DESC, plusieurs critères, LIMIT et OFFSET.", M2_L1, 20),
            ("fonctions", "Fonctions sur le texte, les nombres et NULL",
             "UPPER, LENGTH, SUBSTR, ||, ROUND, COALESCE et les dates.", M2_L2, 25),
            ("case-when", "Conditions avec CASE",
             "Produire une valeur selon des conditions, ligne par ligne.", M2_L3, 20),
        ],
        "quiz": ("Quiz — Trier, limiter et transformer", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Agréger les données",
        "description": "Compter, additionner, faire des moyennes et des statistiques par groupe.",
        "status": "published",
        "lessons": [
            ("fonctions-agregation", "Les fonctions d'agrégation",
             "COUNT, SUM, AVG, MIN, MAX et leur comportement avec NULL.", _m35.M3_L1, 25),
            ("group-by", "Regrouper avec GROUP BY",
             "Calculer une statistique pour chaque groupe de lignes.", _m35.M3_L2, 25),
            ("having", "Filtrer les groupes avec HAVING",
             "HAVING, différence avec WHERE et ordre d'exécution d'une requête.", _m35.M3_L3, 25),
        ],
        "quiz": ("Quiz — Agréger les données", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Joindre des tables",
        "description": "Croiser les informations de plusieurs tables grâce aux clés étrangères.",
        "status": "published",
        "lessons": [
            ("inner-join", "Relier deux tables avec JOIN",
             "Clés étrangères, INNER JOIN, alias de tables.", _m35.M4_L1, 30),
            ("left-join", "Garder toutes les lignes avec LEFT JOIN",
             "Jointure externe, lignes sans correspondance, trouver les absents.", _m35.M4_L2, 25),
            ("jointures-et-agregations", "Jointures multiples et agrégations",
             "Trois tables à la fois, statistiques par étudiant et par formation.", _m35.M4_L3, 30),
        ],
        "quiz": ("Quiz — Joindre des tables", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Créer et modifier des données",
        "description": "Créer des tables, insérer, mettre à jour, supprimer et utiliser des sous-requêtes.",
        "status": "published",
        "lessons": [
            ("create-table", "Créer une table et ses contraintes",
             "CREATE TABLE, types, PRIMARY KEY, NOT NULL, UNIQUE, CHECK, FOREIGN KEY.", _m35.M5_L1, 25),
            ("insert-update-delete", "Insérer, modifier et supprimer",
             "INSERT, UPDATE, DELETE, transactions et bonnes pratiques de sécurité.", _m35.M5_L2, 30),
            ("sous-requetes-mini-projet", "Sous-requêtes et mini-projet",
             "Requêtes imbriquées, puis un tableau de bord complet de l'organisme.", _m35.M5_L3, 40),
        ],
        "quiz": ("Quiz — Créer et modifier des données", _m35.QUIZ_M5),
    },
]
