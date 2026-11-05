-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose des exercices corrigés et chaque module se termine par un quiz noté sur 20.$smk$, (select id from public.categories where slug = $smk$bases-de-donnees$smk$), $smk$SQL$smk$, $smk$SQL$smk$, $smk$debutant$smk$, 480, array[$smk$Comprendre l'organisation d'une base de données relationnelle$smk$, $smk$Extraire, filtrer et trier des données avec SELECT$smk$, $smk$Calculer des statistiques avec GROUP BY et les fonctions d'agrégation$smk$, $smk$Croiser plusieurs tables avec les jointures$smk$, $smk$Créer des tables et modifier des données en toute sécurité$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance préalable en programmation ou en base de données$smk$]::text[], 'coming_soon', false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category_id = excluded.category_id, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('bbdfa414-fd52-589e-89d6-6e9c7ec18e98', '458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$Découvrir SQL$smk$, $smk$Comprendre une base relationnelle, lire des tables avec SELECT et filtrer avec WHERE.$smk$, 1, 'draft')
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('734599d2-ddc3-53a0-8633-c110992fbfc5', 'bbdfa414-fd52-589e-89d6-6e9c7ec18e98', $smk$bases-de-donnees-relationnelles$smk$, $smk$Bases de données relationnelles et SQL$smk$, $smk$Tables, lignes, colonnes, clé primaire, NULL et la base de la formation.$smk$, $smk$## À quoi sert une base de données ?

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
```$smk$, 20, 1),
('4a88590b-8364-5494-a470-b19ec386c23f', 'bbdfa414-fd52-589e-89d6-6e9c7ec18e98', $smk$select$smk$, $smk$Lire des données avec SELECT$smk$, $smk$Choisir des colonnes, calculer, renommer avec AS, supprimer les doublons.$smk$, $smk$## La requête SELECT

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
```$smk$, 25, 2),
('a6df48bb-b85d-5766-94bb-03406eba0115', 'bbdfa414-fd52-589e-89d6-6e9c7ec18e98', $smk$where$smk$, $smk$Filtrer avec WHERE$smk$, $smk$Comparaisons, AND/OR/NOT, IN, BETWEEN, LIKE et IS NULL.$smk$, $smk$## Filtrer les lignes avec WHERE

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
```$smk$, 30, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 'bbdfa414-fd52-589e-89d6-6e9c7ec18e98', $smk$Quiz — Découvrir SQL$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('6d088157-78fe-5f8f-b496-fa89fd016a84', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 1, $smk$single$smk$, $smk$Dans une table, que représente une ligne ?$smk$, null, 2),
('baf4bd3b-495d-51a5-9b6c-71a51727cb0a', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 2, $smk$single$smk$, $smk$À quoi sert la clé primaire d'une table ?$smk$, null, 2),
('2d6c3b83-fb02-59a3-85f5-6767d9dca156', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 3, $smk$single$smk$, $smk$Que renvoie cette requête ?$smk$, $smk$SELECT DISTINCT ville FROM etudiants;$smk$, 2),
('168154b9-2f03-5e31-9f12-3edc1fe59dcb', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 4, $smk$single$smk$, $smk$Quelle requête affiche uniquement les étudiants habitant à Lyon ?$smk$, null, 2),
('7459fab3-0b71-5ee6-9c98-441054479b80', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 5, $smk$multiple$smk$, $smk$Quelles conditions sélectionnent Sofia, qui n'a pas d'email ?$smk$, null, 2),
('c515b66b-0d67-5765-90cd-3992f69c8466', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 6, $smk$single$smk$, $smk$Combien de lignes renvoie cette requête ?$smk$, $smk$SELECT titre FROM formations
WHERE duree_heures BETWEEN 8 AND 10;$smk$, 2),
('fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 7, $smk$single$smk$, $smk$Quel motif trouve tous les noms qui se terminent par « i » ?$smk$, null, 2),
('9924d8ef-c691-50bc-8866-bc0c1064b0aa', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 8, $smk$single$smk$, $smk$Que renvoie cette requête ?$smk$, $smk$SELECT prenom FROM etudiants
WHERE ville = 'Paris' OR ville = 'Lyon' AND date_naissance < '2000-01-01';$smk$, 2),
('9f72a4dd-96a6-51e8-b556-f46bb37f48f3', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 9, $smk$true_false$smk$, $smk$Une requête SELECT peut modifier les données d'une table.$smk$, null, 2),
('10687aba-d553-5566-a929-e3409609c502', '08ea9688-ce2b-592b-82ed-c6e1716bf5ab', 10, $smk$single$smk$, $smk$Qu'affiche cette requête ?$smk$, $smk$SELECT prenom nom FROM etudiants;$smk$, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('bb15148c-f8d7-5bbd-9531-804d79265cb2', '6d088157-78fe-5f8f-b496-fa89fd016a84', 1, $smk$Une caractéristique commune à tous les éléments$smk$),
('61f56313-df6a-5ebf-9f19-a8d7c2c0f3cb', '6d088157-78fe-5f8f-b496-fa89fd016a84', 2, $smk$Un élément précis, par exemple un étudiant$smk$),
('21a6c07b-1b2f-543e-b99d-d01fc3f77be5', '6d088157-78fe-5f8f-b496-fa89fd016a84', 3, $smk$Le type de données d'une colonne$smk$),
('42c3e027-21ba-53da-a687-7bac98b15cc7', '6d088157-78fe-5f8f-b496-fa89fd016a84', 4, $smk$Une requête enregistrée$smk$),
('971101c3-3a36-5ca0-9076-f38942ae8403', 'baf4bd3b-495d-51a5-9b6c-71a51727cb0a', 1, $smk$À trier automatiquement les lignes$smk$),
('6bc115f0-3ace-5447-880e-fd74c0ecf5e4', 'baf4bd3b-495d-51a5-9b6c-71a51727cb0a', 2, $smk$À identifier chaque ligne de manière unique$smk$),
('bcf4638a-c1fb-524d-982e-41b3c19dddcf', 'baf4bd3b-495d-51a5-9b6c-71a51727cb0a', 3, $smk$À chiffrer les données$smk$),
('dd23b450-e3d0-532c-b1ce-292932609f94', 'baf4bd3b-495d-51a5-9b6c-71a51727cb0a', 4, $smk$À relier la table à Internet$smk$),
('be3d2983-d06c-5d71-91e9-4876d15dfd70', '2d6c3b83-fb02-59a3-85f5-6767d9dca156', 1, $smk$6 lignes, une par étudiant$smk$),
('bd81729b-ca5a-5e61-acbe-743ddd8c3cf0', '2d6c3b83-fb02-59a3-85f5-6767d9dca156', 2, $smk$4 lignes, une par ville différente$smk$),
('5dc3498e-74a0-58f4-b6b0-3c2865c34dd0', '2d6c3b83-fb02-59a3-85f5-6767d9dca156', 3, $smk$1 ligne : le nombre de villes$smk$),
('3cac7b7d-ac15-5ba1-823d-b26e7d73f1f7', '2d6c3b83-fb02-59a3-85f5-6767d9dca156', 4, $smk$Une erreur$smk$),
('2b37ea6b-e6e1-52a9-bb93-1fbfaf0717ab', '168154b9-2f03-5e31-9f12-3edc1fe59dcb', 1, $smk$SELECT * FROM etudiants WHERE ville = "Lyon";$smk$),
('49b3a3f0-178f-513b-acd8-f5750a2bac8e', '168154b9-2f03-5e31-9f12-3edc1fe59dcb', 2, $smk$SELECT * FROM etudiants WHERE ville == 'Lyon';$smk$),
('6924e66f-21d0-57f5-99fd-588c573674e2', '168154b9-2f03-5e31-9f12-3edc1fe59dcb', 3, $smk$SELECT * FROM etudiants WHERE ville = 'Lyon';$smk$),
('242b367c-f555-5f22-a927-4873dfdce974', '168154b9-2f03-5e31-9f12-3edc1fe59dcb', 4, $smk$SELECT * WHERE ville = 'Lyon' FROM etudiants;$smk$),
('e8bd8eec-2df2-50f8-99fb-3f5cf8ff4316', '7459fab3-0b71-5ee6-9c98-441054479b80', 1, $smk$WHERE email IS NULL$smk$),
('b895574a-ac22-5131-834b-aa96b7c6be21', '7459fab3-0b71-5ee6-9c98-441054479b80', 2, $smk$WHERE email = NULL$smk$),
('2de62ab4-b50f-5565-91ea-59a79fb79ba7', '7459fab3-0b71-5ee6-9c98-441054479b80', 3, $smk$WHERE email IS NOT NULL$smk$),
('1db1199e-239d-501e-a294-8f105a0d968d', '7459fab3-0b71-5ee6-9c98-441054479b80', 4, $smk$WHERE prenom = 'Sofia'$smk$),
('9561ffcf-0631-570f-8938-7719ec06ea62', 'c515b66b-0d67-5765-90cd-3992f69c8466', 1, $smk$1$smk$),
('a4287b4a-f7cb-5b85-a258-dfb69d17c5e8', 'c515b66b-0d67-5765-90cd-3992f69c8466', 2, $smk$2$smk$),
('6aefded1-e19b-57f9-ba2e-3373cb5a1b24', 'c515b66b-0d67-5765-90cd-3992f69c8466', 3, $smk$3$smk$),
('036c3588-42f9-537d-b53e-b3ca2c2c36e7', 'c515b66b-0d67-5765-90cd-3992f69c8466', 4, $smk$4$smk$),
('4e7d8a6a-671f-5924-b7cd-03544c87558f', 'fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', 1, $smk$LIKE 'i%'$smk$),
('ca60cc4e-5f9b-55ad-8e7a-da70c9551585', 'fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', 2, $smk$LIKE '%i'$smk$),
('9571ea57-4964-5137-a2a9-d50483326876', 'fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', 3, $smk$LIKE '_i'$smk$),
('31c88ae9-22ba-5648-805b-a44adb957606', 'fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', 4, $smk$LIKE '%i%'$smk$),
('dd2966ba-f4ac-5115-9241-be775602ddf0', '9924d8ef-c691-50bc-8866-bc0c1064b0aa', 1, $smk$Lucas et Yanis$smk$),
('d3d8bd34-611d-5948-bf95-0c50cc7a977e', '9924d8ef-c691-50bc-8866-bc0c1064b0aa', 2, $smk$Amina, Sofia, Lucas et Yanis$smk$),
('53683a0a-cc88-5d52-9240-bdbba029453d', '9924d8ef-c691-50bc-8866-bc0c1064b0aa', 3, $smk$Amina et Sofia$smk$),
('c1bc290f-985c-50ba-95ad-fcef9df6e070', '9924d8ef-c691-50bc-8866-bc0c1064b0aa', 4, $smk$Aucune ligne$smk$),
('2a9350ea-6788-5831-8cfa-d92a89da6778', '9f72a4dd-96a6-51e8-b556-f46bb37f48f3', 1, $smk$Vrai$smk$),
('82a33ad0-1143-5357-84db-90dd4bb0356b', '9f72a4dd-96a6-51e8-b556-f46bb37f48f3', 2, $smk$Faux$smk$),
('e558184c-af0c-5a39-b931-76203845905f', '10687aba-d553-5566-a929-e3409609c502', 1, $smk$Les prénoms et les noms$smk$),
('67bdd8fa-971d-5646-b7fa-c9a77c7d3d08', '10687aba-d553-5566-a929-e3409609c502', 2, $smk$Une erreur de syntaxe$smk$),
('e764feeb-afb9-57c0-929a-86e69ef5d30c', '10687aba-d553-5566-a929-e3409609c502', 3, $smk$Les prénoms, dans une colonne intitulée « nom »$smk$),
('900654ab-b581-55c9-8851-bf763714a9cc', '10687aba-d553-5566-a929-e3409609c502', 4, $smk$Les noms seulement$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('6d088157-78fe-5f8f-b496-fa89fd016a84', array['61f56313-df6a-5ebf-9f19-a8d7c2c0f3cb']::uuid[], $smk$Une ligne (ou enregistrement) décrit un élément précis ; les colonnes décrivent les caractéristiques communes à tous les éléments.$smk$),
('baf4bd3b-495d-51a5-9b6c-71a51727cb0a', array['6bc115f0-3ace-5447-880e-fd74c0ecf5e4']::uuid[], $smk$La clé primaire (souvent id) prend une valeur différente pour chaque ligne : elle permet de désigner une ligne sans ambiguïté, même si deux étudiants ont le même nom.$smk$),
('2d6c3b83-fb02-59a3-85f5-6767d9dca156', array['bd81729b-ca5a-5e61-acbe-743ddd8c3cf0']::uuid[], $smk$DISTINCT supprime les doublons : Paris et Lyon apparaissent deux fois dans la table mais une seule fois dans le résultat, soit 4 villes.$smk$),
('168154b9-2f03-5e31-9f12-3edc1fe59dcb', array['6924e66f-21d0-57f5-99fd-588c573674e2']::uuid[], $smk$En SQL, l'égalité s'écrit avec un seul = et les valeurs texte entre apostrophes. Les guillemets doubles désignent un nom de colonne, == n'existe pas et WHERE se place après FROM.$smk$),
('7459fab3-0b71-5ee6-9c98-441054479b80', array['e8bd8eec-2df2-50f8-99fb-3f5cf8ff4316', '1db1199e-239d-501e-a294-8f105a0d968d']::uuid[], $smk$NULL ne se compare jamais avec = : email = NULL n'est vrai pour aucune ligne. IS NULL fonctionne, tout comme un filtre sur le prénom. IS NOT NULL sélectionne au contraire les cinq autres.$smk$),
('c515b66b-0d67-5765-90cd-3992f69c8466', array['6aefded1-e19b-57f9-ba2e-3373cb5a1b24']::uuid[], $smk$BETWEEN inclut ses bornes : SQL (8 h), Anglais professionnel (8 h) et Docker (10 h) sont retenues, soit 3 lignes. Python (11 h) est exclue.$smk$),
('fed387e5-63eb-5c62-9b9e-4f6bac65bd6e', array['ca60cc4e-5f9b-55ad-8e7a-da70c9551585']::uuid[], $smk$% remplace n'importe quelle suite de caractères. '%i' signifie « n'importe quoi puis un i final ». 'i%' cherche un i au début, '_i' exactement deux caractères, '%i%' un i n'importe où.$smk$),
('9924d8ef-c691-50bc-8866-bc0c1064b0aa', array['d3d8bd34-611d-5948-bf95-0c50cc7a977e']::uuid[], $smk$AND est évalué avant OR : la condition se lit « Paris, OU (Lyon ET né avant 2000) ». Amina et Sofia (Paris) sont donc retenues, ainsi que Lucas et Yanis. Des parenthèses autour du OR auraient donné seulement Lucas et Yanis.$smk$),
('9f72a4dd-96a6-51e8-b556-f46bb37f48f3', array['82a33ad0-1143-5357-84db-90dd4bb0356b']::uuid[], $smk$SELECT ne fait que lire. Un calcul comme prix * 10 produit une colonne dans le résultat, sans toucher à la table. Les modifications se font avec INSERT, UPDATE et DELETE.$smk$),
('10687aba-d553-5566-a929-e3409609c502', array['e764feeb-afb9-57c0-929a-86e69ef5d30c']::uuid[], $smk$Sans virgule, le second mot est interprété comme un alias (le mot AS est facultatif). La requête affiche donc la colonne prenom renommée en nom : un piège classique.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

update public.modules set status = $smk$published$smk$ where id = 'bbdfa414-fd52-589e-89d6-6e9c7ec18e98';
