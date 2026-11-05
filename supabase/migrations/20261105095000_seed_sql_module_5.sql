-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose des exercices corrigés et chaque module se termine par un quiz noté sur 20.$smk$, (select id from public.categories where slug = $smk$bases-de-donnees$smk$), $smk$SQL$smk$, $smk$SQL$smk$, $smk$debutant$smk$, 480, array[$smk$Comprendre l'organisation d'une base de données relationnelle$smk$, $smk$Extraire, filtrer et trier des données avec SELECT$smk$, $smk$Calculer des statistiques avec GROUP BY et les fonctions d'agrégation$smk$, $smk$Croiser plusieurs tables avec les jointures$smk$, $smk$Créer des tables et modifier des données en toute sécurité$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance préalable en programmation ou en base de données$smk$]::text[], 'coming_soon', false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category_id = excluded.category_id, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('7a7e647a-f423-5667-9475-4147f4bae379', '458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$Créer et modifier des données$smk$, $smk$Créer des tables, insérer, mettre à jour, supprimer et utiliser des sous-requêtes.$smk$, 5, 'draft')
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('742a9eaf-c0ed-569e-ab60-ad6ad68657c6', '7a7e647a-f423-5667-9475-4147f4bae379', $smk$create-table$smk$, $smk$Créer une table et ses contraintes$smk$, $smk$CREATE TABLE, types, PRIMARY KEY, NOT NULL, UNIQUE, CHECK, FOREIGN KEY.$smk$, $smk$## Le langage de définition des données

Jusqu'ici, vous avez **lu** des données. SQL permet aussi de **définir** la structure de la base : créer, modifier et supprimer des tables. Ces instructions forment le *DDL* (*Data Definition Language*).

## CREATE TABLE

```sql
CREATE TABLE avis (
  id            INTEGER PRIMARY KEY,
  inscription_id INTEGER NOT NULL REFERENCES inscriptions (id),
  etoiles       INTEGER NOT NULL CHECK (etoiles BETWEEN 1 AND 5),
  commentaire   TEXT,
  publie_le     DATE NOT NULL DEFAULT CURRENT_DATE
);
```

Chaque colonne est déclarée avec un **nom**, un **type** et, éventuellement, des **contraintes**.

## Les types de données courants

| Type | Contenu | Exemple |
|---|---|---|
| `INTEGER` | nombre entier | `42` |
| `NUMERIC(p, s)` | nombre décimal exact (montants) | `49.90` |
| `TEXT` / `VARCHAR(n)` | texte (limité à `n` caractères pour `VARCHAR`) | `'Lyon'` |
| `BOOLEAN` | vrai ou faux | `TRUE` |
| `DATE` | date | `'2026-11-05'` |
| `TIMESTAMP` | date et heure | `'2026-11-05 09:30:00'` |

> Pour de l'argent, utilisez `NUMERIC` et jamais un type à virgule flottante (`REAL`, `FLOAT`) : ces derniers produisent des erreurs d'arrondi (0,1 + 0,2 ≠ 0,3).

## Les contraintes : la base vérifie pour vous

Les contraintes refusent les données incohérentes, quelle que soit l'application qui les envoie :

- `PRIMARY KEY` : valeur unique et obligatoire, identifiant de la ligne ;
- `NOT NULL` : la colonne doit être renseignée ;
- `UNIQUE` : deux lignes ne peuvent pas avoir la même valeur (par exemple l'email) ;
- `CHECK (condition)` : la valeur doit vérifier la condition (`etoiles BETWEEN 1 AND 5`) ;
- `REFERENCES table (colonne)` : **clé étrangère**, la valeur doit exister dans l'autre table ;
- `DEFAULT valeur` : valeur utilisée si rien n'est fourni.

Une tentative d'insertion qui viole une contrainte est **rejetée avec une erreur** : la base ne contient jamais de note de 7 étoiles ni d'avis rattaché à une inscription inexistante.

## Les identifiants automatiques

Plutôt que de choisir soi-même les `id`, on laisse généralement la base les générer :

```sql
-- PostgreSQL (norme SQL)
id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
-- MySQL
id INT AUTO_INCREMENT PRIMARY KEY
-- SQLite : une colonne INTEGER PRIMARY KEY est numérotée automatiquement
```

## Modifier ou supprimer une table

```sql
ALTER TABLE etudiants ADD COLUMN telephone TEXT;   -- ajouter une colonne
ALTER TABLE etudiants DROP COLUMN telephone;       -- la supprimer
DROP TABLE avis;                                   -- supprimer la table ET toutes ses données
```

> `DROP TABLE` est **irréversible** : la table et toutes ses lignes disparaissent. Sur une vraie base, on ne l'exécute qu'après avoir vérifié qu'une sauvegarde existe.

## À retenir

- `CREATE TABLE` déclare chaque colonne avec un type et des contraintes.
- `NUMERIC` pour les montants, `DATE`/`TIMESTAMP` pour le temps, `TEXT` pour le texte.
- Les contraintes (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `CHECK`, `REFERENCES`) protègent la cohérence des données.
- `ALTER TABLE` modifie une table ; `DROP TABLE` la supprime définitivement.

## Exercices

### Exercice 1 — Table des formateurs

Créez une table `formateurs` avec un identifiant, un prénom et un nom obligatoires, un email unique et un taux horaire positif.

```solution-sql
CREATE TABLE formateurs (
  id          INTEGER PRIMARY KEY,
  prenom      TEXT NOT NULL,
  nom         TEXT NOT NULL,
  email       TEXT UNIQUE,
  taux_horaire NUMERIC(6, 2) NOT NULL CHECK (taux_horaire > 0)
);
```

### Exercice 2 — Quelle contrainte ?

Pour chaque règle, indiquez la contrainte adaptée : (a) deux étudiants ne peuvent pas avoir le même email ; (b) une note est comprise entre 0 et 20 ; (c) une inscription doit concerner une formation existante ; (d) le prénom est obligatoire.

```solution-text
(a) UNIQUE sur la colonne email
(b) CHECK (note BETWEEN 0 AND 20)
(c) une clé étrangère : formation_id INTEGER REFERENCES formations (id)
(d) NOT NULL sur la colonne prenom
```$smk$, 25, 1),
('90109a06-9b26-51c2-9664-e211e7bddf23', '7a7e647a-f423-5667-9475-4147f4bae379', $smk$insert-update-delete$smk$, $smk$Insérer, modifier et supprimer$smk$, $smk$INSERT, UPDATE, DELETE, transactions et bonnes pratiques de sécurité.$smk$, $smk$## Ajouter des lignes : INSERT

```sql
INSERT INTO etudiants (id, prenom, nom, ville, date_naissance, email)
VALUES (7, 'Lina', 'Fontaine', 'Nantes', '2004-02-11', 'lina@exemple.fr');
```

- On liste les colonnes à remplir, puis les valeurs **dans le même ordre**.
- Les colonnes omises reçoivent leur valeur par défaut (`DEFAULT`) ou `NULL`.
- Plusieurs lignes peuvent être insérées d'un coup :

```sql
INSERT INTO formations (id, titre, categorie, duree_heures, prix)
VALUES (7, 'HTML et CSS', 'Développement web', 10, 0),
       (8, 'React', 'Développement web', 14, 39);
```

> Écrivez toujours la liste des colonnes. `INSERT INTO etudiants VALUES (…)` dépend de l'ordre des colonnes de la table et se casse le jour où une colonne est ajoutée.

## Modifier des lignes : UPDATE

```sql
UPDATE inscriptions
SET note = 13
WHERE id = 5;
```

`SET` indique les nouvelles valeurs ; `WHERE` désigne les lignes concernées. On peut modifier plusieurs colonnes et utiliser la valeur actuelle :

```sql
UPDATE formations
SET prix = prix + 10, duree_heures = duree_heures + 1
WHERE categorie = 'Data Science';
```

## Supprimer des lignes : DELETE

```sql
DELETE FROM inscriptions
WHERE id = 8;
```

## La règle de sécurité absolue : le WHERE

**Sans `WHERE`, `UPDATE` et `DELETE` s'appliquent à toutes les lignes de la table.**

```sql
UPDATE formations SET prix = 0;      -- toutes les formations deviennent gratuites
DELETE FROM inscriptions;            -- toutes les inscriptions sont effacées
```

Ces requêtes sont parfaitement valides : la base les exécute sans demander de confirmation. Adoptez ce réflexe :

1. écrivez d'abord un `SELECT` avec le `WHERE` prévu ;
2. vérifiez que les lignes renvoyées sont exactement celles à modifier ;
3. remplacez ensuite `SELECT …` par `UPDATE … SET …` ou `DELETE`, **sans toucher au `WHERE`**.

```sql
SELECT * FROM inscriptions WHERE note IS NULL;      -- 1. vérifier : lignes 5 et 8
DELETE FROM inscriptions WHERE note IS NULL;        -- 2. puis supprimer
```

## Les transactions

Une **transaction** regroupe plusieurs modifications qui doivent réussir **toutes ensemble ou pas du tout**. Exemple : transférer un étudiant d'une formation à une autre.

```sql
BEGIN;
UPDATE inscriptions SET formation_id = 2 WHERE id = 3;
UPDATE etudiants SET ville = 'Paris' WHERE id = 2;
COMMIT;
```

- `BEGIN` ouvre la transaction ;
- `COMMIT` valide définitivement toutes les modifications ;
- `ROLLBACK` les annule toutes, comme si rien ne s'était passé.

En cas d'erreur au milieu (contrainte violée, coupure…), le SGBD annule la transaction : la base ne reste jamais dans un état à moitié modifié. Avant une modification délicate, vous pouvez aussi ouvrir une transaction, exécuter votre `UPDATE`, vérifier avec un `SELECT`, puis choisir `COMMIT` ou `ROLLBACK`.

## Les contraintes en action

```sql
INSERT INTO inscriptions (id, etudiant_id, formation_id, date_inscription)
VALUES (9, 42, 1, '2026-11-05');
-- Erreur : l'étudiant 42 n'existe pas (violation de la clé étrangère)

DELETE FROM etudiants WHERE id = 1;
-- Erreur : des inscriptions font encore référence à Amina
```

La clé étrangère empêche à la fois de créer une inscription « orpheline » et de supprimer un étudiant qui a encore des inscriptions.

> Dans une application, les valeurs saisies par les utilisateurs ne sont **jamais** collées directement dans le texte d'une requête : on utilise des **requêtes paramétrées**, fournies par tous les langages. Sinon, un texte malveillant peut modifier la requête elle-même : c'est l'**injection SQL**, l'une des failles de sécurité les plus courantes.

## À retenir

- `INSERT INTO table (colonnes) VALUES (…)` ajoute des lignes ; listez toujours les colonnes.
- `UPDATE table SET … WHERE …` modifie ; `DELETE FROM table WHERE …` supprime.
- Sans `WHERE`, toute la table est concernée : vérifiez d'abord avec un `SELECT`.
- `BEGIN … COMMIT` / `ROLLBACK` : tout ou rien.
- Requêtes paramétrées dans le code, toujours.

## Exercices

### Exercice 1 — Nouvelle inscription

Inscrivez Yanis (id 6) à la formation Docker (id 6) le 5 novembre 2026, avec l'identifiant 9, sans note.

```solution-sql
INSERT INTO inscriptions (id, etudiant_id, formation_id, date_inscription)
VALUES (9, 6, 6, '2026-11-05');
-- La colonne note, omise, vaut NULL.
```

### Exercice 2 — Promotion

Baissez de 20 % le prix de toutes les formations payantes de plus de 8 heures. Écrivez d'abord la requête de vérification.

```solution-sql
SELECT id, titre, prix FROM formations WHERE prix > 0 AND duree_heures > 8;
-- Machine Learning (99) et Docker (39)
UPDATE formations
SET prix = prix * 0.8
WHERE prix > 0 AND duree_heures > 8;
-- Machine Learning : 79.2, Docker : 31.2
```

### Exercice 3 — Trouver l'erreur

Un collègue veut supprimer l'inscription n° 8 et a exécuté `DELETE FROM inscriptions;`. Que s'est-il passé, et comment l'éviter ?

```solution-text
Sans WHERE, la requête a supprimé TOUTES les inscriptions, pas seulement la n° 8.
La bonne requête est : DELETE FROM inscriptions WHERE id = 8;
Pour l'éviter : vérifier d'abord avec SELECT * FROM inscriptions WHERE id = 8;
et travailler dans une transaction (BEGIN … puis COMMIT seulement si le nombre de lignes supprimées est correct).
```$smk$, 30, 2),
('e6beda58-4576-520f-9365-bb5b01423afc', '7a7e647a-f423-5667-9475-4147f4bae379', $smk$sous-requetes-mini-projet$smk$, $smk$Sous-requêtes et mini-projet$smk$, $smk$Requêtes imbriquées, puis un tableau de bord complet de l'organisme.$smk$, $smk$## Une requête dans une requête

Une **sous-requête** est un `SELECT` écrit entre parenthèses à l'intérieur d'une autre requête. Elle permet de répondre en une fois à une question en deux temps.

Quelles formations sont plus chères que la moyenne ? Il faut d'abord calculer la moyenne (36 €), puis comparer chaque prix :

```sql
SELECT titre, prix
FROM formations
WHERE prix > (SELECT AVG(prix) FROM formations);
```

```text
titre            | prix
-----------------+-----
Excel avancé     | 49
Machine Learning | 99
Docker           | 39
```

La sous-requête renvoie **une seule valeur** : on peut donc la comparer avec `>`.

## Sous-requête avec IN

Lorsque la sous-requête renvoie **une liste** de valeurs, on utilise `IN` :

```sql
-- Étudiants ayant obtenu au moins une note supérieure ou égale à 15
SELECT prenom, nom
FROM etudiants
WHERE id IN (SELECT etudiant_id FROM inscriptions WHERE note >= 15);
-- Amina Benali, Sofia Rossi
```

`NOT IN` donne l'inverse. Attention : si la sous-requête peut renvoyer `NULL`, `NOT IN` ne renvoie plus aucune ligne. Le motif `LEFT JOIN … IS NULL` ou `NOT EXISTS` est plus sûr dans ce cas.

## EXISTS

`EXISTS (sous-requête)` est vrai si la sous-requête renvoie au moins une ligne. Elle peut faire référence à la requête principale :

```sql
-- Formations ayant au moins une inscription notée
SELECT f.titre
FROM formations f
WHERE EXISTS (
  SELECT 1 FROM inscriptions i
  WHERE i.formation_id = f.id AND i.note IS NOT NULL
);
-- Python, SQL, Excel, Machine Learning, Anglais (pas Docker)
```

## Retrouver la ligne du maximum

« Qui a obtenu la meilleure note, et dans quelle formation ? » :

```sql
SELECT e.prenom, f.titre, i.note
FROM inscriptions i
JOIN etudiants e  ON e.id = i.etudiant_id
JOIN formations f ON f.id = i.formation_id
WHERE i.note = (SELECT MAX(note) FROM inscriptions);
-- Sofia, Machine Learning, 18
```

## Mini-projet : le tableau de bord de l'organisme

La direction vous demande quatre indicateurs. Écrivez chaque requête, exécutez-la, puis comparez avec la correction. Ce projet mobilise toute la formation.

### Indicateur 1 — Vue d'ensemble

Une seule ligne : nombre d'étudiants, nombre de formations, nombre d'inscriptions et moyenne générale arrondie à une décimale.

```solution-sql
SELECT (SELECT COUNT(*) FROM etudiants)    AS etudiants,
       (SELECT COUNT(*) FROM formations)   AS formations,
       (SELECT COUNT(*) FROM inscriptions) AS inscriptions,
       (SELECT ROUND(AVG(note), 1) FROM inscriptions) AS moyenne_generale;
-- 6 | 6 | 8 | 13.3
```

### Indicateur 2 — Classement des formations

Pour chaque formation : titre, nombre d'inscrits, moyenne (ou « — » si aucune note) et chiffre d'affaires (prix × inscrits). Les formations sans inscrit doivent apparaître. Triez par chiffre d'affaires décroissant.

```solution-sql
SELECT f.titre,
       COUNT(i.id) AS inscrits,
       COALESCE(CAST(ROUND(AVG(i.note), 1) AS TEXT), '—') AS moyenne,
       f.prix * COUNT(i.id) AS chiffre_affaires
FROM formations f
LEFT JOIN inscriptions i ON i.formation_id = f.id
GROUP BY f.id, f.titre, f.prix
ORDER BY chiffre_affaires DESC, f.titre;
-- Machine Learning 2 | 18.0 | 198 ; Excel avancé 1 | 12.0 | 49 ; Anglais 1 | 11.0 | 29 ;
-- Docker 0 | — | 0 ; Python 2 | 12.5 | 0 ; SQL 2 | 14.0 | 0
```

### Indicateur 3 — Étudiants à relancer

Les étudiants sans aucune inscription, avec leur email (ou « email manquant »), pour une campagne de relance.

```solution-sql
SELECT e.prenom, e.nom, COALESCE(e.email, 'email manquant') AS contact
FROM etudiants e
WHERE NOT EXISTS (SELECT 1 FROM inscriptions i WHERE i.etudiant_id = e.id);
-- Yanis Morel, yanis@exemple.fr
```

### Indicateur 4 — Mentions

Le nombre d'inscriptions par mention : « Très bien » (≥ 16), « Validé » (≥ 10), « À retravailler » (< 10) et « En cours » (pas de note).

```solution-sql
SELECT CASE
         WHEN note >= 16 THEN 'Très bien'
         WHEN note >= 10 THEN 'Validé'
         WHEN note IS NULL THEN 'En cours'
         ELSE 'À retravailler'
       END AS mention,
       COUNT(*) AS nb
FROM inscriptions
GROUP BY 1
ORDER BY nb DESC;
-- Validé 3, Très bien 2, En cours 2, À retravailler 1
-- (GROUP BY 1 regroupe sur la première colonne du SELECT.)
```

## Et après ?

Vous savez désormais lire, analyser et modifier une base relationnelle. Pour aller plus loin : les **index** (accélérer les recherches), les **vues** (enregistrer une requête), les **fonctions de fenêtrage** (classements, cumuls) et la conception d'un schéma complet. Ces notions sont au programme des formations PostgreSQL et MySQL de SMK Academy.

## À retenir

- Une sous-requête est un `SELECT` entre parenthèses dans une autre requête.
- Une valeur unique se compare avec `=`, `>`, etc. ; une liste s'utilise avec `IN`.
- `EXISTS` teste la présence d'au moins une ligne ; préférez `NOT EXISTS` à `NOT IN` quand des `NULL` sont possibles.
- Toute question métier se décompose : quelles tables, quelles lignes, quels groupes, quel ordre.$smk$, 40, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('0d3158b9-b186-50c6-a4ba-21012acb0ab2', '7a7e647a-f423-5667-9475-4147f4bae379', $smk$Quiz — Créer et modifier des données$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('27864bac-3815-5c14-902c-251be6a77854', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 1, $smk$single$smk$, $smk$Que fait cette requête ?$smk$, $smk$UPDATE formations SET prix = 0;$smk$, 2),
('4519395d-1ca0-5aab-b0d1-800258ea143d', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 2, $smk$single$smk$, $smk$Quelle contrainte garantit qu'une note est comprise entre 0 et 20 ?$smk$, null, 2),
('5d50c9e9-3e5b-5697-96f5-3a886a27af9f', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 3, $smk$single$smk$, $smk$Quel type choisir pour stocker un prix ?$smk$, null, 2),
('6c770df5-c861-5aec-b0aa-78055ed0d2f5', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 4, $smk$single$smk$, $smk$Quelle est la meilleure pratique avant un DELETE délicat ?$smk$, null, 2),
('f60c1b8b-6225-587d-823b-e18e24af180f', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 5, $smk$true_false$smk$, $smk$ROLLBACK annule toutes les modifications effectuées depuis le BEGIN de la transaction.$smk$, null, 2),
('785d9396-ccfc-57a6-bc9f-121964ab9a9f', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 6, $smk$single$smk$, $smk$Pourquoi cette insertion échoue-t-elle ?$smk$, $smk$INSERT INTO inscriptions (id, etudiant_id, formation_id, date_inscription)
VALUES (9, 42, 1, '2026-11-05');$smk$, 2),
('2a35a556-43df-5a77-89d9-8f7b76934050', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 7, $smk$single$smk$, $smk$Que renvoie cette requête ?$smk$, $smk$SELECT titre FROM formations
WHERE prix > (SELECT AVG(prix) FROM formations);$smk$, 2),
('0fdd2366-5d1f-514d-9bac-691a4890deec', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 8, $smk$multiple$smk$, $smk$Quelles instructions modifient les données ou la structure de la base ?$smk$, null, 2),
('166797e5-a098-5d3d-bd2b-df90096e7627', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 9, $smk$single$smk$, $smk$Comment une application doit-elle transmettre la saisie d'un utilisateur à une requête SQL ?$smk$, null, 2),
('7722b9d5-8d18-59de-96c7-85843fabffb3', '0d3158b9-b186-50c6-a4ba-21012acb0ab2', 10, $smk$single$smk$, $smk$Quand préférer NOT EXISTS à NOT IN ?$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('db9874c8-6b57-560b-98bf-902734f4122c', '27864bac-3815-5c14-902c-251be6a77854', 1, $smk$Elle provoque une erreur car il manque WHERE$smk$),
('839d5235-c37c-5938-9898-9d344bbafb3e', '27864bac-3815-5c14-902c-251be6a77854', 2, $smk$Elle rend gratuite la première formation$smk$),
('95313a1f-d18b-58cb-8709-f4ff58048d52', '27864bac-3815-5c14-902c-251be6a77854', 3, $smk$Elle rend gratuites toutes les formations$smk$),
('bf646bf4-c115-5753-91b4-9f1b275609ee', '27864bac-3815-5c14-902c-251be6a77854', 4, $smk$Elle ne fait rien sans COMMIT$smk$),
('c80db567-d5fd-5434-aed4-57fa0f235d14', '4519395d-1ca0-5aab-b0d1-800258ea143d', 1, $smk$UNIQUE$smk$),
('7a359355-c473-5946-9adc-f0916c688e2b', '4519395d-1ca0-5aab-b0d1-800258ea143d', 2, $smk$NOT NULL$smk$),
('cec07819-8728-547f-8bb1-be6197dfb833', '4519395d-1ca0-5aab-b0d1-800258ea143d', 3, $smk$CHECK (note BETWEEN 0 AND 20)$smk$),
('1090cd50-4460-5248-9169-615d2a28c2b7', '4519395d-1ca0-5aab-b0d1-800258ea143d', 4, $smk$DEFAULT 0$smk$),
('5eb7ceed-2ad5-5beb-9744-29fe71da6e36', '5d50c9e9-3e5b-5697-96f5-3a886a27af9f', 1, $smk$FLOAT$smk$),
('da24d839-d144-57ce-88a6-45d3d148fb1f', '5d50c9e9-3e5b-5697-96f5-3a886a27af9f', 2, $smk$REAL$smk$),
('03bc705e-ec4c-5096-b013-f2216ba5de3e', '5d50c9e9-3e5b-5697-96f5-3a886a27af9f', 3, $smk$NUMERIC(8, 2)$smk$),
('6f77070e-922c-561e-8298-bcf4789e051a', '5d50c9e9-3e5b-5697-96f5-3a886a27af9f', 4, $smk$TEXT$smk$),
('50e16a92-1d3b-5565-ad1e-71c39156f75d', '6c770df5-c861-5aec-b0aa-78055ed0d2f5', 1, $smk$Exécuter d'abord un SELECT avec le même WHERE pour vérifier les lignes$smk$),
('1a4eec4e-1c39-50c3-862d-008e87806c6c', '6c770df5-c861-5aec-b0aa-78055ed0d2f5', 2, $smk$Supprimer puis recréer les lignes manquantes$smk$),
('76344f0c-a18e-52d4-9b5c-47d1a44e434f', '6c770df5-c861-5aec-b0aa-78055ed0d2f5', 3, $smk$Retirer le WHERE pour aller plus vite$smk$),
('10e776c3-83ee-577c-95a9-04d58fa9c1aa', '6c770df5-c861-5aec-b0aa-78055ed0d2f5', 4, $smk$Désactiver les clés étrangères$smk$),
('b523ed43-52d9-503f-a514-c0998c758f4b', 'f60c1b8b-6225-587d-823b-e18e24af180f', 1, $smk$Vrai$smk$),
('dca216b9-cc82-5e91-a134-c61248e9e13b', 'f60c1b8b-6225-587d-823b-e18e24af180f', 2, $smk$Faux$smk$),
('7177b0b0-b2f2-5dc0-b129-edccb39711a7', '785d9396-ccfc-57a6-bc9f-121964ab9a9f', 1, $smk$La date est mal écrite$smk$),
('c6287b7f-4911-56ce-8cfb-eed26d47b05d', '785d9396-ccfc-57a6-bc9f-121964ab9a9f', 2, $smk$L'étudiant 42 n'existe pas : la clé étrangère est violée$smk$),
('17b87982-72eb-5316-9cd5-51a059e1ee3e', '785d9396-ccfc-57a6-bc9f-121964ab9a9f', 3, $smk$La note est obligatoire$smk$),
('a26df1f1-8eba-5b5f-9ee5-2033880fedfb', '785d9396-ccfc-57a6-bc9f-121964ab9a9f', 4, $smk$L'identifiant 9 est déjà pris$smk$),
('4e7aec56-5eed-5523-968e-ded523cdd598', '2a35a556-43df-5a77-89d9-8f7b76934050', 1, $smk$Les formations gratuites$smk$),
('118b6e66-3fe0-5380-b55b-3497dfb10b1c', '2a35a556-43df-5a77-89d9-8f7b76934050', 2, $smk$Les formations plus chères que le prix moyen (36 €)$smk$),
('288663b5-a346-5bc7-878f-52ff6d24f012', '2a35a556-43df-5a77-89d9-8f7b76934050', 3, $smk$La formation la plus chère$smk$),
('9602e65e-7dfb-586b-acea-a501655562f5', '2a35a556-43df-5a77-89d9-8f7b76934050', 4, $smk$Une erreur : une sous-requête est interdite dans WHERE$smk$),
('78cdabff-13f3-56ab-b4e4-9963d9d4d789', '0fdd2366-5d1f-514d-9bac-691a4890deec', 1, $smk$SELECT$smk$),
('f75ec796-2076-5fd6-b1d5-c6300a82236a', '0fdd2366-5d1f-514d-9bac-691a4890deec', 2, $smk$INSERT$smk$),
('26db1179-7b8e-540a-99e9-18c9a7e67a99', '0fdd2366-5d1f-514d-9bac-691a4890deec', 3, $smk$DELETE$smk$),
('dd3ad4ae-7f25-5d87-befc-a84f877998f7', '0fdd2366-5d1f-514d-9bac-691a4890deec', 4, $smk$ALTER TABLE$smk$),
('7a7152ea-af6a-540d-bcd9-116464a11340', '166797e5-a098-5d3d-bd2b-df90096e7627', 1, $smk$En la collant directement dans le texte de la requête$smk$),
('2e2acdfd-30bc-53c3-ac16-8a4c762ce7d7', '166797e5-a098-5d3d-bd2b-df90096e7627', 2, $smk$Avec une requête paramétrée$smk$),
('58be7817-9cfd-5f9c-bc58-f448aa47425d', '166797e5-a098-5d3d-bd2b-df90096e7627', 3, $smk$En la mettant en majuscules$smk$),
('6083305f-1224-550d-a6c2-2246c64a92d6', '166797e5-a098-5d3d-bd2b-df90096e7627', 4, $smk$En supprimant les espaces$smk$),
('566f7c1c-7cda-5ec9-abaa-b24799219a80', '7722b9d5-8d18-59de-96c7-85843fabffb3', 1, $smk$Jamais, ils sont toujours équivalents$smk$),
('61b02680-f049-5ebd-857b-1d4195ec6710', '7722b9d5-8d18-59de-96c7-85843fabffb3', 2, $smk$Quand la sous-requête peut renvoyer des NULL$smk$),
('2f524066-3202-559f-a872-06d0b7e828f8', '7722b9d5-8d18-59de-96c7-85843fabffb3', 3, $smk$Quand la table est vide$smk$),
('1e6c8604-e088-5fca-80b9-6b5779bfd40b', '7722b9d5-8d18-59de-96c7-85843fabffb3', 4, $smk$Uniquement en MySQL$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('27864bac-3815-5c14-902c-251be6a77854', array['95313a1f-d18b-58cb-8709-f4ff58048d52']::uuid[], $smk$Sans WHERE, UPDATE s'applique à toutes les lignes. La requête est valide et s'exécute immédiatement (hors transaction ouverte).$smk$),
('4519395d-1ca0-5aab-b0d1-800258ea143d', array['cec07819-8728-547f-8bb1-be6197dfb833']::uuid[], $smk$CHECK impose une condition à chaque valeur. UNIQUE interdit les doublons, NOT NULL impose une valeur, DEFAULT fournit une valeur par défaut.$smk$),
('5d50c9e9-3e5b-5697-96f5-3a886a27af9f', array['03bc705e-ec4c-5096-b013-f2216ba5de3e']::uuid[], $smk$NUMERIC stocke les décimaux de façon exacte. Les types à virgule flottante (FLOAT, REAL) introduisent des erreurs d'arrondi inacceptables pour de l'argent.$smk$),
('6c770df5-c861-5aec-b0aa-78055ed0d2f5', array['50e16a92-1d3b-5565-ad1e-71c39156f75d']::uuid[], $smk$Le SELECT avec le même WHERE montre exactement les lignes qui seront supprimées. On peut en plus travailler dans une transaction pour pouvoir annuler.$smk$),
('f60c1b8b-6225-587d-823b-e18e24af180f', array['b523ed43-52d9-503f-a514-c0998c758f4b']::uuid[], $smk$Une transaction est « tout ou rien » : COMMIT valide l'ensemble, ROLLBACK l'annule entièrement.$smk$),
('785d9396-ccfc-57a6-bc9f-121964ab9a9f', array['c6287b7f-4911-56ce-8cfb-eed26d47b05d']::uuid[], $smk$etudiant_id référence etudiants(id). Aucun étudiant n'a l'identifiant 42 : la base refuse cette inscription orpheline. La note, elle, peut être NULL.$smk$),
('2a35a556-43df-5a77-89d9-8f7b76934050', array['118b6e66-3fe0-5380-b55b-3497dfb10b1c']::uuid[], $smk$La sous-requête calcule le prix moyen (36 €) ; la requête principale garde les formations plus chères : Excel avancé, Machine Learning et Docker.$smk$),
('0fdd2366-5d1f-514d-9bac-691a4890deec', array['f75ec796-2076-5fd6-b1d5-c6300a82236a', '26db1179-7b8e-540a-99e9-18c9a7e67a99', 'dd3ad4ae-7f25-5d87-befc-a84f877998f7']::uuid[], $smk$INSERT ajoute des lignes, DELETE en supprime, ALTER TABLE modifie la structure. SELECT se contente de lire.$smk$),
('166797e5-a098-5d3d-bd2b-df90096e7627', array['2e2acdfd-30bc-53c3-ac16-8a4c762ce7d7']::uuid[], $smk$Les requêtes paramétrées séparent le code SQL des données : un texte malveillant ne peut pas modifier la requête. C'est la protection standard contre l'injection SQL.$smk$),
('7722b9d5-8d18-59de-96c7-85843fabffb3', array['61b02680-f049-5ebd-857b-1d4195ec6710']::uuid[], $smk$Si la liste de NOT IN contient un NULL, la condition n'est jamais vraie et la requête ne renvoie rien. NOT EXISTS n'a pas ce piège.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

update public.modules set status = $smk$published$smk$ where id = '7a7e647a-f423-5667-9475-4147f4bae379';
update public.courses set status = $smk$published$smk$ where slug = $smk$sql-debutant$smk$;
