-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose des exercices corrigés et chaque module se termine par un quiz noté sur 20.$smk$, (select id from public.categories where slug = $smk$bases-de-donnees$smk$), $smk$SQL$smk$, $smk$SQL$smk$, $smk$debutant$smk$, 480, array[$smk$Comprendre l'organisation d'une base de données relationnelle$smk$, $smk$Extraire, filtrer et trier des données avec SELECT$smk$, $smk$Calculer des statistiques avec GROUP BY et les fonctions d'agrégation$smk$, $smk$Croiser plusieurs tables avec les jointures$smk$, $smk$Créer des tables et modifier des données en toute sécurité$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance préalable en programmation ou en base de données$smk$]::text[], 'coming_soon', false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category_id = excluded.category_id, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('c36831c7-6d45-5ec3-9364-da2c32439368', '458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$Agréger les données$smk$, $smk$Compter, additionner, faire des moyennes et des statistiques par groupe.$smk$, 3, 'draft')
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('ac3e2b8c-575a-5ba8-8054-8d38bf87604d', 'c36831c7-6d45-5ec3-9364-da2c32439368', $smk$fonctions-agregation$smk$, $smk$Les fonctions d'agrégation$smk$, $smk$COUNT, SUM, AVG, MIN, MAX et leur comportement avec NULL.$smk$, $smk$## Résumer plusieurs lignes en une seule valeur

Jusqu'ici, chaque ligne du résultat correspondait à une ligne de la table. Les **fonctions d'agrégation** font l'inverse : elles résument un ensemble de lignes en **une seule valeur**. Combien d'inscriptions ? Quelle note moyenne ? Quel est le prix le plus élevé ?

| Fonction | Rôle |
|---|---|
| `COUNT(*)` | nombre de lignes |
| `COUNT(colonne)` | nombre de valeurs **non NULL** de la colonne |
| `SUM(colonne)` | somme |
| `AVG(colonne)` | moyenne |
| `MIN(colonne)` | plus petite valeur |
| `MAX(colonne)` | plus grande valeur |

## Un tableau de bord en une requête

```sql
SELECT COUNT(*)            AS nb_inscriptions,
       COUNT(note)         AS nb_notes,
       ROUND(AVG(note), 1) AS moyenne,
       MIN(note)           AS note_min,
       MAX(note)           AS note_max
FROM inscriptions;
```

```text
nb_inscriptions | nb_notes | moyenne | note_min | note_max
----------------+----------+---------+----------+---------
8               | 6        | 13.3    | 9        | 18
```

Le résultat ne contient qu'**une seule ligne**, qui résume les huit inscriptions.

## Les agrégations ignorent NULL

Observez la différence entre `COUNT(*)` (8) et `COUNT(note)` (6) : deux inscriptions n'ont pas de note. Toutes les fonctions d'agrégation, sauf `COUNT(*)`, **ignorent les valeurs NULL**.

La moyenne vaut donc (16 + 14 + 9 + 18 + 12 + 11) / 6 = 80 / 6 ≈ 13,3 : les deux inscriptions non notées ne comptent pas comme des zéros. C'est généralement ce que l'on souhaite. Si vous voulez au contraire compter les absences comme des zéros, écrivez `AVG(COALESCE(note, 0))`, qui vaudrait 80 / 8 = 10.

## Agréger une partie des lignes

`WHERE` filtre les lignes **avant** le calcul :

```sql
SELECT SUM(prix) AS total_catalogue_payant, COUNT(*) AS nb_formations
FROM formations
WHERE prix > 0;
-- total_catalogue_payant : 216, nb_formations : 4
```

## Compter des valeurs distinctes

`COUNT(DISTINCT colonne)` compte les valeurs différentes. Combien d'étudiants différents se sont inscrits au moins une fois ?

```sql
SELECT COUNT(DISTINCT etudiant_id) AS etudiants_inscrits
FROM inscriptions;
-- 5 (Amina compte une seule fois malgré ses trois inscriptions ; Yanis n'est inscrit nulle part)
```

## Compter selon une condition

En combinant `SUM` et `CASE`, on compte plusieurs catégories dans la même requête :

```sql
SELECT SUM(CASE WHEN note >= 10 THEN 1 ELSE 0 END) AS validees,
       SUM(CASE WHEN note < 10 THEN 1 ELSE 0 END)  AS non_validees
FROM inscriptions;
-- validees : 5, non_validees : 1
```

## Le piège : mélanger lignes et agrégats

Cette requête est **refusée** par PostgreSQL :

```sql
SELECT prenom, COUNT(*) FROM etudiants;
```

Elle demande à la fois une valeur par étudiant (`prenom`) et une valeur unique pour toute la table (`COUNT(*)`) : SQL ne sait pas quel prénom afficher sur la ligne unique du résultat. Pour obtenir un calcul **par groupe**, il faut `GROUP BY`, objet de la leçon suivante.

> SQLite et certaines configurations de MySQL acceptent cette requête et affichent un prénom choisi arbitrairement : le résultat n'a pas de sens. Ne vous y fiez pas.

## À retenir

- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX` résument plusieurs lignes en une valeur.
- `COUNT(*)` compte les lignes ; `COUNT(colonne)` compte les valeurs non NULL.
- Les agrégations ignorent `NULL` ; `COALESCE` permet de le remplacer.
- `COUNT(DISTINCT …)` compte les valeurs différentes ; `SUM(CASE …)` compte selon une condition.
- On ne mélange pas une colonne « par ligne » et une agrégation sans `GROUP BY`.

## Exercices

### Exercice 1 — Le catalogue en chiffres

Affichez le nombre de formations, leur durée totale en heures et le prix moyen.

```solution-sql
SELECT COUNT(*) AS nb_formations,
       SUM(duree_heures) AS heures_totales,
       AVG(prix) AS prix_moyen
FROM formations;
-- 6 formations, 63 heures, prix moyen 36
```

### Exercice 2 — Les notes d'Amina

Affichez la meilleure note et la note moyenne d'Amina (identifiant 1).

```solution-sql
SELECT MAX(note) AS meilleure_note, AVG(note) AS moyenne
FROM inscriptions
WHERE etudiant_id = 1;
-- 16 et 15 : l'inscription non notée (Machine Learning) est ignorée.
```

### Exercice 3 — Taux de réussite

Calculez le nombre d'inscriptions notées et le nombre d'inscriptions validées (note ≥ 10) dans la même requête.

```solution-sql
SELECT COUNT(note) AS notees,
       SUM(CASE WHEN note >= 10 THEN 1 ELSE 0 END) AS validees
FROM inscriptions;
-- 6 notées, 5 validées
```$smk$, 25, 1),
('b9562a8b-6625-5c0c-a92c-7342ad263ad4', 'c36831c7-6d45-5ec3-9364-da2c32439368', $smk$group-by$smk$, $smk$Regrouper avec GROUP BY$smk$, $smk$Calculer une statistique pour chaque groupe de lignes.$smk$, $smk$## Une statistique par groupe

Combien d'étudiants habitent dans **chaque** ville ? Il faut découper la table en groupes (un par ville), puis calculer un `COUNT` dans chaque groupe. C'est le rôle de `GROUP BY` :

```sql
SELECT ville, COUNT(*) AS nb_etudiants
FROM etudiants
GROUP BY ville
ORDER BY nb_etudiants DESC, ville;
```

```text
ville     | nb_etudiants
----------+-------------
Lyon      | 2
Paris     | 2
Lille     | 1
Marseille | 1
```

Le SGBD procède en trois temps :

1. il lit les lignes de `etudiants` ;
2. il range ensemble les lignes qui ont la même valeur de `ville` ;
3. il produit **une ligne de résultat par groupe**, avec la valeur commune (`ville`) et le résultat de l'agrégation.

## La règle d'or du GROUP BY

Dans une requête avec `GROUP BY`, chaque colonne du `SELECT` doit être :

- soit **dans le GROUP BY** (elle a la même valeur pour tout le groupe) ;
- soit **à l'intérieur d'une fonction d'agrégation**.

```sql
-- Refusé : prenom n'est ni groupé ni agrégé (quel prénom afficher pour Paris ?)
SELECT ville, prenom, COUNT(*) FROM etudiants GROUP BY ville;
```

## Plusieurs statistiques par groupe

```sql
SELECT formation_id,
       COUNT(*) AS inscrits,
       ROUND(AVG(note), 1) AS moyenne
FROM inscriptions
GROUP BY formation_id
ORDER BY formation_id;
```

```text
formation_id | inscrits | moyenne
-------------+----------+--------
1            | 2        | 12.5
2            | 2        | 14.0
3            | 1        | 12.0
4            | 2        | 18.0
5            | 1        | 11.0
```

La formation 2 compte deux inscrits mais une seule note (14) : la moyenne ignore la note manquante. Il en va de même pour la formation 4. La formation 6 (Docker) n'apparaît pas, car aucune inscription ne la concerne : on verra au module 4 comment l'afficher avec zéro inscrit.

## Grouper sur plusieurs colonnes

On peut grouper selon plusieurs critères : un groupe correspond alors à chaque **combinaison** de valeurs.

```sql
SELECT ville, date_naissance >= '2000-01-01' AS ne_apres_2000, COUNT(*) AS nb
FROM etudiants
GROUP BY ville, date_naissance >= '2000-01-01'
ORDER BY ville;
-- Lyon apparaît une fois (Lucas et Yanis sont nés avant 2000) ; chaque autre ville aussi.
```

En pratique, on groupe le plus souvent sur une ou deux colonnes « catégories » : ville, catégorie, mois, statut…

## Trier les groupes

`ORDER BY` s'applique au résultat final : on peut trier sur la colonne de groupe ou sur l'agrégat, via son alias.

```sql
SELECT categorie, SUM(duree_heures) AS heures
FROM formations
GROUP BY categorie
ORDER BY heures DESC
LIMIT 3;
-- Data Science (20), Programmation (11), Cloud et DevOps (10)
```

## À retenir

- `GROUP BY` découpe les lignes en groupes et produit une ligne de résultat par groupe.
- Toute colonne du `SELECT` est soit groupée, soit agrégée.
- Les groupes sans aucune ligne n'apparaissent pas.
- `ORDER BY` et `LIMIT` s'appliquent après le regroupement.

## Exercices

### Exercice 1 — Inscriptions par étudiant

Affichez, pour chaque `etudiant_id` présent dans les inscriptions, le nombre d'inscriptions, du plus grand au plus petit.

```solution-sql
SELECT etudiant_id, COUNT(*) AS nb
FROM inscriptions
GROUP BY etudiant_id
ORDER BY nb DESC, etudiant_id;
-- 1 : 3, 2 : 2, puis 3, 4 et 5 : 1
```

### Exercice 2 — Prix moyen par tranche

Affichez le nombre de formations gratuites et payantes, avec leur durée moyenne. Indice : groupez sur une expression `CASE`.

```solution-sql
SELECT CASE WHEN prix = 0 THEN 'Gratuite' ELSE 'Payante' END AS acces,
       COUNT(*) AS nb,
       AVG(duree_heures) AS duree_moyenne
FROM formations
GROUP BY CASE WHEN prix = 0 THEN 'Gratuite' ELSE 'Payante' END;
-- Gratuite : 2 formations, 9.5 h ; Payante : 4 formations, 11 h
```$smk$, 25, 2),
('d6133057-013d-571c-bf8d-9ac8933aeebd', 'c36831c7-6d45-5ec3-9364-da2c32439368', $smk$having$smk$, $smk$Filtrer les groupes avec HAVING$smk$, $smk$HAVING, différence avec WHERE et ordre d'exécution d'une requête.$smk$, $smk$## Filtrer après le regroupement : HAVING

Quels étudiants sont inscrits à **au moins deux** formations ? La condition porte sur un résultat d'agrégation (`COUNT(*)`), qui n'existe qu'**après** le regroupement. `WHERE` ne peut donc pas l'utiliser : il faut `HAVING`.

```sql
SELECT etudiant_id, COUNT(*) AS nb
FROM inscriptions
GROUP BY etudiant_id
HAVING COUNT(*) >= 2;
```

```text
etudiant_id | nb
------------+---
1           | 3
2           | 2
```

## WHERE ou HAVING ?

| | `WHERE` | `HAVING` |
|---|---|---|
| Filtre… | les **lignes** | les **groupes** |
| Moment | avant le `GROUP BY` | après le `GROUP BY` |
| Peut utiliser une agrégation ? | non | oui |

Les deux se combinent très bien. Quelles formations ont une moyenne d'au moins 12, en ne tenant compte que des inscriptions notées ?

```sql
SELECT formation_id, ROUND(AVG(note), 1) AS moyenne
FROM inscriptions
WHERE note IS NOT NULL
GROUP BY formation_id
HAVING AVG(note) >= 12
ORDER BY moyenne DESC;
```

```text
formation_id | moyenne
-------------+--------
4            | 18.0
2            | 14.0
1            | 12.5
3            | 12.0
```

La formation 5 (moyenne 11) est éliminée par le `HAVING`.

> Règle pratique : si la condition peut s'écrire dans le `WHERE`, mettez-la dans le `WHERE`. Les lignes inutiles sont écartées plus tôt et la requête est plus rapide.

## L'ordre d'exécution d'une requête

Une requête ne s'exécute pas dans l'ordre où elle s'écrit. Le SGBD suit cet ordre **logique** :

1. `FROM` : choisir la table (et les jointures) ;
2. `WHERE` : filtrer les lignes ;
3. `GROUP BY` : former les groupes ;
4. `HAVING` : filtrer les groupes ;
5. `SELECT` : calculer les colonnes et les alias ;
6. `ORDER BY` : trier ;
7. `LIMIT` / `OFFSET` : garder une partie du résultat.

Cet ordre explique plusieurs règles déjà rencontrées :

- un alias défini dans le `SELECT` est utilisable dans `ORDER BY` (étape 6) mais **pas dans `WHERE`** (étape 2, quand l'alias n'existe pas encore) ;
- une agrégation ne peut pas apparaître dans `WHERE` : les groupes n'existent pas encore.

```sql
-- Erreur (PostgreSQL, Oracle, SQL Server) : l'alias minutes n'existe pas encore à l'étape WHERE
SELECT titre, duree_heures * 60 AS minutes FROM formations WHERE minutes > 500;

-- Correct : on répète l'expression
SELECT titre, duree_heures * 60 AS minutes FROM formations WHERE duree_heures * 60 > 500;
```

## À retenir

- `HAVING` filtre les groupes, après le `GROUP BY` ; il accepte les agrégations.
- `WHERE` filtre les lignes avant le regroupement ; préférez-le quand c'est possible.
- Ordre logique : `FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT`.
- Un alias du `SELECT` n'est pas visible dans `WHERE`.

## Exercices

### Exercice 1 — Villes représentées

Affichez les villes qui comptent au moins deux étudiants.

```solution-sql
SELECT ville, COUNT(*) AS nb
FROM etudiants
GROUP BY ville
HAVING COUNT(*) >= 2;
-- Paris et Lyon
```

### Exercice 2 — Corriger la requête

Cette requête renvoie une erreur. Expliquez pourquoi, puis corrigez-la pour obtenir les formations dont la meilleure note dépasse 15.

```sql
SELECT formation_id, MAX(note) AS meilleure
FROM inscriptions
WHERE MAX(note) > 15
GROUP BY formation_id;
```

```solution-sql
-- Une agrégation ne peut pas figurer dans WHERE : les groupes n'existent pas encore.
SELECT formation_id, MAX(note) AS meilleure
FROM inscriptions
GROUP BY formation_id
HAVING MAX(note) > 15;
-- Formations 1 (16) et 4 (18)
```

### Exercice 3 — Catégories actives

Parmi les formations de plus de 6 heures, affichez les catégories dont la durée totale atteint au moins 10 heures.

```solution-sql
SELECT categorie, SUM(duree_heures) AS heures
FROM formations
WHERE duree_heures > 6
GROUP BY categorie
HAVING SUM(duree_heures) >= 10;
-- Cloud et DevOps (10), Data Science (20), Programmation (11)
```$smk$, 25, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('4de55be0-9840-539b-a1c4-ab628176f210', 'c36831c7-6d45-5ec3-9364-da2c32439368', $smk$Quiz — Agréger les données$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('c986f89a-e0ae-56b4-b768-9f3106b3f151', '4de55be0-9840-539b-a1c4-ab628176f210', 1, $smk$single$smk$, $smk$Que renvoie COUNT(note) sur la table inscriptions, qui compte 8 lignes dont 2 sans note ?$smk$, null, 2),
('d75d8d43-6937-5e65-8018-12a460820b80', '4de55be0-9840-539b-a1c4-ab628176f210', 2, $smk$single$smk$, $smk$Les notes sont 16, 14, 9, 18, 12, 11, NULL et NULL. Que vaut AVG(note) ?$smk$, null, 2),
('61729b78-59cc-52b3-8ba6-77f75523b7cc', '4de55be0-9840-539b-a1c4-ab628176f210', 3, $smk$single$smk$, $smk$Combien de lignes renvoie cette requête ?$smk$, $smk$SELECT ville, COUNT(*)
FROM etudiants
GROUP BY ville;$smk$, 2),
('0051047a-a583-5681-8761-aa146d6b4f3f', '4de55be0-9840-539b-a1c4-ab628176f210', 4, $smk$single$smk$, $smk$Pourquoi cette requête est-elle refusée par PostgreSQL ?$smk$, $smk$SELECT ville, prenom, COUNT(*)
FROM etudiants
GROUP BY ville;$smk$, 2),
('ecd01baa-2d13-51ca-b29b-7e649ae8690d', '4de55be0-9840-539b-a1c4-ab628176f210', 5, $smk$single$smk$, $smk$Quelle clause permet de ne garder que les groupes ayant au moins 2 lignes ?$smk$, null, 2),
('5b4b303c-eaab-5fda-b101-fdc1dae103e9', '4de55be0-9840-539b-a1c4-ab628176f210', 6, $smk$single$smk$, $smk$Dans quel ordre logique le SGBD exécute-t-il ces clauses ?$smk$, null, 2),
('24498b3f-0b23-5f5d-a3e7-7af422862e38', '4de55be0-9840-539b-a1c4-ab628176f210', 7, $smk$true_false$smk$, $smk$COUNT(DISTINCT etudiant_id) compte une seule fois un étudiant inscrit à plusieurs formations.$smk$, null, 2),
('3e55efa5-8788-5247-86a8-cbac54717b80', '4de55be0-9840-539b-a1c4-ab628176f210', 8, $smk$multiple$smk$, $smk$Quelles conditions peuvent figurer dans un WHERE ?$smk$, null, 2),
('2c6d2ed0-f491-511b-851a-bb2c22c9aecd', '4de55be0-9840-539b-a1c4-ab628176f210', 9, $smk$single$smk$, $smk$Que calcule cette expression ?$smk$, $smk$SUM(CASE WHEN note >= 10 THEN 1 ELSE 0 END)$smk$, 2),
('42ac6186-9ae2-5eaa-b039-9e5d293b0e96', '4de55be0-9840-539b-a1c4-ab628176f210', 10, $smk$single$smk$, $smk$Que renvoie MAX(note) pour un groupe dont toutes les notes sont NULL ?$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('0f6cb594-62a1-5a3e-b40d-3fa33f54d69f', 'c986f89a-e0ae-56b4-b768-9f3106b3f151', 1, $smk$8$smk$),
('5c413f19-b165-52a2-b82c-864019590c20', 'c986f89a-e0ae-56b4-b768-9f3106b3f151', 2, $smk$6$smk$),
('b4d1427c-98f7-53af-aad2-27d17b392e47', 'c986f89a-e0ae-56b4-b768-9f3106b3f151', 3, $smk$2$smk$),
('8b89e0f0-2309-529f-bc23-3a140f71983a', 'c986f89a-e0ae-56b4-b768-9f3106b3f151', 4, $smk$NULL$smk$),
('69c599a6-84a5-583c-b279-689d393b7834', 'd75d8d43-6937-5e65-8018-12a460820b80', 1, $smk$10$smk$),
('38241e5c-c54c-5ec6-a4b2-e373069565fa', 'd75d8d43-6937-5e65-8018-12a460820b80', 2, $smk$13,3 environ$smk$),
('d55e330a-a3d1-5857-a3dd-ea260d1e3711', 'd75d8d43-6937-5e65-8018-12a460820b80', 3, $smk$NULL$smk$),
('d1d4f448-e6b6-5fbf-91cb-3b4cfe7a8903', 'd75d8d43-6937-5e65-8018-12a460820b80', 4, $smk$80$smk$),
('d9dcafe5-9657-5a3b-9749-35771297b961', '61729b78-59cc-52b3-8ba6-77f75523b7cc', 1, $smk$1$smk$),
('7e9fcb08-4045-580e-a5ef-e0548dc8ab64', '61729b78-59cc-52b3-8ba6-77f75523b7cc', 2, $smk$4$smk$),
('a5f52ae6-a342-59ba-ac67-f8c92c31fb85', '61729b78-59cc-52b3-8ba6-77f75523b7cc', 3, $smk$6$smk$),
('baa17680-b523-533c-93f5-0d8c81ab4c4c', '61729b78-59cc-52b3-8ba6-77f75523b7cc', 4, $smk$Une erreur$smk$),
('fa41b26e-b948-5d44-a281-ed7c47b0890c', '0051047a-a583-5681-8761-aa146d6b4f3f', 1, $smk$COUNT(*) est interdit avec GROUP BY$smk$),
('9a93822b-82d5-5535-94a2-39bf0cc04b0d', '0051047a-a583-5681-8761-aa146d6b4f3f', 2, $smk$prenom n'est ni groupé ni agrégé$smk$),
('10bbc0da-c21a-5f3f-9c92-426a7dee5c94', '0051047a-a583-5681-8761-aa146d6b4f3f', 3, $smk$ville doit être agrégée$smk$),
('e9ea6f67-2ef3-51b8-965a-d8ced7ada989', '0051047a-a583-5681-8761-aa146d6b4f3f', 4, $smk$Il manque un ORDER BY$smk$),
('a35bc567-a2a3-5262-bec2-4678bef373ca', 'ecd01baa-2d13-51ca-b29b-7e649ae8690d', 1, $smk$WHERE COUNT(*) >= 2$smk$),
('e7130356-cfa7-5100-b675-be81a03db7c0', 'ecd01baa-2d13-51ca-b29b-7e649ae8690d', 2, $smk$HAVING COUNT(*) >= 2$smk$),
('a5a5c706-2e93-5edf-b316-1027f3eea191', 'ecd01baa-2d13-51ca-b29b-7e649ae8690d', 3, $smk$GROUP BY COUNT(*) >= 2$smk$),
('3d20da1e-f0be-5533-ba4e-95ba9f5853d7', 'ecd01baa-2d13-51ca-b29b-7e649ae8690d', 4, $smk$LIMIT 2$smk$),
('3816ca89-3170-52f6-b014-8c78cfcde37e', '5b4b303c-eaab-5fda-b101-fdc1dae103e9', 1, $smk$SELECT, FROM, WHERE, GROUP BY, HAVING$smk$),
('77a3b5d7-bb7f-5be9-927b-2a1fa245940b', '5b4b303c-eaab-5fda-b101-fdc1dae103e9', 2, $smk$FROM, WHERE, GROUP BY, HAVING, SELECT$smk$),
('885d0684-e8e8-52f5-8e93-88808a50e4da', '5b4b303c-eaab-5fda-b101-fdc1dae103e9', 3, $smk$FROM, GROUP BY, WHERE, SELECT, HAVING$smk$),
('9a5c8633-8701-52f6-a636-8224e6db47c7', '5b4b303c-eaab-5fda-b101-fdc1dae103e9', 4, $smk$WHERE, FROM, SELECT, GROUP BY, HAVING$smk$),
('f917226a-f7ac-570f-9413-097fda6df813', '24498b3f-0b23-5f5d-a3e7-7af422862e38', 1, $smk$Vrai$smk$),
('93f72195-888d-5617-a9ee-34c752e514e6', '24498b3f-0b23-5f5d-a3e7-7af422862e38', 2, $smk$Faux$smk$),
('7462b8ad-071f-5fc0-a72c-97a20367cd09', '3e55efa5-8788-5247-86a8-cbac54717b80', 1, $smk$note >= 10$smk$),
('fc627f37-ecc3-5bfc-9680-a2f8c8094ac0', '3e55efa5-8788-5247-86a8-cbac54717b80', 2, $smk$COUNT(*) > 1$smk$),
('1ea8cb96-5685-5589-8406-7085971aaf0a', '3e55efa5-8788-5247-86a8-cbac54717b80', 3, $smk$ville IN ('Paris', 'Lyon')$smk$),
('2ec25a99-32d8-589c-b52d-7b220819f681', '3e55efa5-8788-5247-86a8-cbac54717b80', 4, $smk$AVG(note) > 12$smk$),
('f5a03a03-9dcf-57a4-bae2-5ec3501772e1', '2c6d2ed0-f491-511b-851a-bb2c22c9aecd', 1, $smk$La somme des notes supérieures ou égales à 10$smk$),
('84b54b33-cb89-5776-9a14-e7cacf26edef', '2c6d2ed0-f491-511b-851a-bb2c22c9aecd', 2, $smk$Le nombre de notes supérieures ou égales à 10$smk$),
('0bc75bf3-168d-5d95-9bb1-90942e8254af', '2c6d2ed0-f491-511b-851a-bb2c22c9aecd', 3, $smk$La moyenne des notes$smk$),
('7853f02e-550d-50e6-83d0-8932506818ae', '2c6d2ed0-f491-511b-851a-bb2c22c9aecd', 4, $smk$Le nombre total de lignes$smk$),
('01665784-6f8f-5417-b320-64c72e9db0d5', '42ac6186-9ae2-5eaa-b039-9e5d293b0e96', 1, $smk$0$smk$),
('05ae03bf-9c3f-50a7-9f2f-9b5e1b740fa1', '42ac6186-9ae2-5eaa-b039-9e5d293b0e96', 2, $smk$NULL$smk$),
('8e996cc7-b84c-550b-a36c-7c1daf3237c8', '42ac6186-9ae2-5eaa-b039-9e5d293b0e96', 3, $smk$Une erreur$smk$),
('1fee9a97-7844-5086-b3db-bed95b435e7f', '42ac6186-9ae2-5eaa-b039-9e5d293b0e96', 4, $smk$20$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('c986f89a-e0ae-56b4-b768-9f3106b3f151', array['5c413f19-b165-52a2-b82c-864019590c20']::uuid[], $smk$COUNT(colonne) ne compte que les valeurs non NULL : 6. COUNT(*) compterait les 8 lignes.$smk$),
('d75d8d43-6937-5e65-8018-12a460820b80', array['38241e5c-c54c-5ec6-a4b2-e373069565fa']::uuid[], $smk$AVG ignore les NULL : 80 / 6 ≈ 13,3. Pour compter les absences comme des zéros, il faudrait AVG(COALESCE(note, 0)) = 10.$smk$),
('61729b78-59cc-52b3-8ba6-77f75523b7cc', array['7e9fcb08-4045-580e-a5ef-e0548dc8ab64']::uuid[], $smk$GROUP BY produit une ligne par groupe. Il y a 4 villes différentes : Paris, Lyon, Marseille et Lille.$smk$),
('0051047a-a583-5681-8761-aa146d6b4f3f', array['9a93822b-82d5-5535-94a2-39bf0cc04b0d']::uuid[], $smk$Chaque colonne du SELECT doit être dans le GROUP BY ou dans une agrégation. Un groupe « Paris » contient deux prénoms : SQL ne peut pas choisir lequel afficher.$smk$),
('ecd01baa-2d13-51ca-b29b-7e649ae8690d', array['e7130356-cfa7-5100-b675-be81a03db7c0']::uuid[], $smk$HAVING filtre les groupes après le regroupement et accepte les agrégations. WHERE agit avant le regroupement et ne peut pas utiliser COUNT.$smk$),
('5b4b303c-eaab-5fda-b101-fdc1dae103e9', array['77a3b5d7-bb7f-5be9-927b-2a1fa245940b']::uuid[], $smk$Ordre logique : FROM, WHERE, GROUP BY, HAVING, SELECT, puis ORDER BY et LIMIT. C'est pourquoi un alias du SELECT n'est pas utilisable dans WHERE.$smk$),
('24498b3f-0b23-5f5d-a3e7-7af422862e38', array['f917226a-f7ac-570f-9413-097fda6df813']::uuid[], $smk$DISTINCT élimine les doublons avant de compter : Amina, inscrite trois fois, n'est comptée qu'une fois.$smk$),
('3e55efa5-8788-5247-86a8-cbac54717b80', array['7462b8ad-071f-5fc0-a72c-97a20367cd09', '1ea8cb96-5685-5589-8406-7085971aaf0a']::uuid[], $smk$WHERE accepte les conditions sur les lignes. Les agrégations (COUNT, AVG…) ne sont autorisées que dans HAVING, SELECT et ORDER BY.$smk$),
('2c6d2ed0-f491-511b-851a-bb2c22c9aecd', array['84b54b33-cb89-5776-9a14-e7cacf26edef']::uuid[], $smk$Le CASE vaut 1 pour chaque note ≥ 10 et 0 sinon : la somme de ces 1 compte les notes ≥ 10.$smk$),
('42ac6186-9ae2-5eaa-b039-9e5d293b0e96', array['05ae03bf-9c3f-50a7-9f2f-9b5e1b740fa1']::uuid[], $smk$Les agrégations ignorent les NULL ; s'il ne reste aucune valeur, le résultat est NULL. Seul COUNT renvoie 0 dans ce cas.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

update public.modules set status = $smk$published$smk$ where id = 'c36831c7-6d45-5ec3-9364-da2c32439368';
