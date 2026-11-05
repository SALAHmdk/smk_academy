"""Modules 3 à 5 de « SQL pour débutants » (importé par content/sql_debutant.py)."""

# ---------------------------------------------------------------------------
# Module 3 — Agréger les données
# ---------------------------------------------------------------------------
M3_L1 = r"""
## Résumer plusieurs lignes en une seule valeur

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
```
"""

M3_L2 = r"""
## Une statistique par groupe

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
```
"""

M3_L3 = r"""
## Filtrer après le regroupement : HAVING

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
```
"""

# ---------------------------------------------------------------------------
# Module 4 — Joindre des tables
# ---------------------------------------------------------------------------
M4_L1 = r"""
## Pourquoi plusieurs tables ?

La table `inscriptions` ne contient que des identifiants : `etudiant_id = 1`, `formation_id = 4`. Pour savoir qu'il s'agit d'*Amina* inscrite en *Machine Learning*, il faut aller chercher l'information dans les tables `etudiants` et `formations`.

Pourquoi ne pas tout ranger dans une seule grande table ? Parce qu'Amina apparaîtrait trois fois, avec trois copies de son email. Le jour où elle change d'adresse, il faudrait modifier trois lignes, et l'oubli d'une seule rendrait les données incohérentes. En stockant chaque information **une seule fois** et en la référençant par son identifiant, la base reste fiable. Ce principe s'appelle la **normalisation**.

## Clé primaire et clé étrangère

- `etudiants.id` est la **clé primaire** de la table des étudiants.
- `inscriptions.etudiant_id` est une **clé étrangère** : elle *fait référence* à `etudiants.id`. La base refuse une inscription qui pointerait vers un étudiant inexistant.

Une **jointure** reconstitue l'information en associant chaque ligne d'une table aux lignes correspondantes d'une autre.

## INNER JOIN

```sql
SELECT etudiants.prenom, inscriptions.formation_id, inscriptions.note
FROM inscriptions
INNER JOIN etudiants ON etudiants.id = inscriptions.etudiant_id;
```

- `INNER JOIN etudiants` ajoute la table des étudiants ;
- `ON …` donne la **condition de jointure** : une ligne d'inscription est associée à l'étudiant dont l'`id` est égal à son `etudiant_id`.

Le mot `INNER` est facultatif : `JOIN` seul signifie `INNER JOIN`.

## Les alias de tables

Répéter `inscriptions.` et `etudiants.` alourdit la requête. On donne un **alias** court à chaque table, juste après son nom :

```sql
SELECT e.prenom, e.nom, i.formation_id, i.note
FROM inscriptions i
JOIN etudiants e ON e.id = i.etudiant_id;
```

Préfixer les colonnes devient **obligatoire** dès qu'un nom existe dans les deux tables : `id` existe à la fois dans `inscriptions` et dans `etudiants`. Écrire simplement `id` serait **ambigu** et provoquerait une erreur.

## Joindre trois tables

Chaque `JOIN` ajoute une table. Pour afficher en clair qui suit quelle formation :

```sql
SELECT e.prenom, f.titre, i.note
FROM inscriptions i
JOIN etudiants e  ON e.id = i.etudiant_id
JOIN formations f ON f.id = i.formation_id
ORDER BY e.prenom, f.titre;
```

```text
prenom | titre                 | note
-------+-----------------------+-----
Amina  | Machine Learning      | NULL
Amina  | Python pour débutants | 16
Amina  | SQL pour débutants    | 14
Emma   | Excel avancé          | 12
Karim  | SQL pour débutants    | NULL
Lucas  | Anglais professionnel | 11
Lucas  | Python pour débutants | 9
Sofia  | Machine Learning      | 18
```

Ce résultat contient **une ligne par inscription** (8 lignes). Yanis n'apparaît pas : il n'a aucune inscription, et `INNER JOIN` ne garde que les lignes qui ont une correspondance des deux côtés. Docker non plus, pour la même raison.

## Filtrer après une jointure

`WHERE` s'utilise normalement, sur n'importe quelle colonne des tables jointes :

```sql
SELECT e.prenom, e.nom
FROM inscriptions i
JOIN etudiants e  ON e.id = i.etudiant_id
JOIN formations f ON f.id = i.formation_id
WHERE f.titre = 'Python pour débutants';
-- Amina Benali, Lucas Martin
```

## Le piège : oublier la condition ON

Sans condition de jointure (ou avec une condition fausse), chaque ligne de la première table est associée à **chaque** ligne de la seconde : 8 inscriptions × 6 étudiants = 48 lignes absurdes. C'est le **produit cartésien**. Si un résultat contient soudain beaucoup trop de lignes, vérifiez vos `ON`.

## À retenir

- Une **clé étrangère** référence la clé primaire d'une autre table.
- `JOIN … ON …` associe les lignes qui vérifient la condition de jointure.
- `INNER JOIN` ne garde que les lignes ayant une correspondance des deux côtés.
- Des alias courts (`e`, `f`, `i`) rendent la requête lisible ; préfixez les colonnes ambiguës.
- Un nombre de lignes inattendu signale souvent une condition `ON` manquante ou fausse.

## Exercices

### Exercice 1 — Notes en clair

Affichez le titre de la formation et la note de chaque inscription notée, de la meilleure à la moins bonne.

```solution-sql
SELECT f.titre, i.note
FROM inscriptions i
JOIN formations f ON f.id = i.formation_id
WHERE i.note IS NOT NULL
ORDER BY i.note DESC;
-- Machine Learning 18, Python 16, SQL 14, Excel 12, Anglais 11, Python 9
```

### Exercice 2 — Les Lyonnais

Affichez le prénom et le titre des formations suivies par les étudiants habitant à Lyon.

```solution-sql
SELECT e.prenom, f.titre
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id
JOIN formations f   ON f.id = i.formation_id
WHERE e.ville = 'Lyon';
-- Lucas : Python pour débutants, Anglais professionnel (Yanis n'a aucune inscription)
```
"""

M4_L2 = r"""
## Le problème des lignes sans correspondance

Combien de formations suit chaque étudiant, **y compris ceux qui n'en suivent aucune** ? Avec un `INNER JOIN`, Yanis disparaît du résultat, puisqu'il n'a aucune inscription. Il faut une jointure qui conserve toutes les lignes d'une table : la **jointure externe**.

## LEFT JOIN

`LEFT JOIN` garde **toutes les lignes de la table de gauche** (celle écrite avant le `JOIN`), même lorsqu'elles n'ont aucune correspondance à droite. Les colonnes de la table de droite sont alors remplies de `NULL`.

```sql
SELECT e.prenom, i.formation_id
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id
ORDER BY e.prenom;
```

Cette fois, Yanis figure dans le résultat, avec `NULL` comme `formation_id`.

## Compter avec un LEFT JOIN

```sql
SELECT e.prenom, COUNT(i.id) AS nb_inscriptions
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id
GROUP BY e.id, e.prenom
ORDER BY nb_inscriptions DESC, e.prenom;
```

```text
prenom | nb_inscriptions
-------+----------------
Amina  | 3
Lucas  | 2
Emma   | 1
Karim  | 1
Sofia  | 1
Yanis  | 0
```

Le détail qui compte : on écrit `COUNT(i.id)` et **non** `COUNT(*)`. La ligne de Yanis existe bien (avec des `NULL` à droite), donc `COUNT(*)` vaudrait 1. `COUNT(i.id)` ne compte que les valeurs non NULL : 0.

On groupe aussi sur `e.id` et pas seulement sur le prénom : deux étudiants pourraient porter le même prénom.

## Trouver les absents

Le motif « `LEFT JOIN` + `IS NULL` » répond aux questions du type « qui n'a jamais… ? » :

```sql
-- Étudiants sans aucune inscription
SELECT e.prenom, e.nom
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id
WHERE i.id IS NULL;
-- Yanis Morel
```

```sql
-- Formations sans aucun inscrit
SELECT f.titre
FROM formations f
LEFT JOIN inscriptions i ON i.formation_id = f.id
WHERE i.id IS NULL;
-- Docker
```

## L'ordre des tables compte

`A LEFT JOIN B` conserve toutes les lignes de **A**. Inverser les tables change le sens de la requête : `inscriptions LEFT JOIN etudiants` conserverait toutes les inscriptions, et Yanis n'apparaîtrait pas.

Il existe aussi `RIGHT JOIN` (conserve la table de droite) et `FULL OUTER JOIN` (conserve les deux). En pratique, on réécrit presque toujours un `RIGHT JOIN` en `LEFT JOIN` en inversant les tables : c'est plus lisible.

## Piège : un filtre qui annule le LEFT JOIN

```sql
-- Yanis disparaît : la condition du WHERE élimine les lignes où i.note est NULL
SELECT e.prenom, i.note
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id
WHERE i.note >= 10;
```

Une condition sur la table de droite placée dans le `WHERE` élimine les lignes sans correspondance, et le `LEFT JOIN` se comporte alors comme un `INNER JOIN`. Pour filtrer la table de droite tout en gardant toutes les lignes de gauche, placez la condition dans le `ON` :

```sql
SELECT e.prenom, COUNT(i.id) AS formations_validees
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id AND i.note >= 10
GROUP BY e.id, e.prenom
ORDER BY e.prenom;
-- Amina 2, Emma 1, Karim 0, Lucas 1, Sofia 1, Yanis 0
```

## À retenir

- `LEFT JOIN` garde toutes les lignes de la table de gauche ; les colonnes de droite valent `NULL` sans correspondance.
- Avec un `LEFT JOIN`, comptez avec `COUNT(colonne_de_droite)`, pas `COUNT(*)`.
- `LEFT JOIN … WHERE droite.id IS NULL` trouve les lignes sans correspondance.
- Une condition sur la table de droite se place dans le `ON` pour ne pas perdre de lignes.

## Exercices

### Exercice 1 — Inscrits par formation

Affichez chaque formation avec son nombre d'inscrits, y compris celles qui n'en ont aucun.

```solution-sql
SELECT f.titre, COUNT(i.id) AS inscrits
FROM formations f
LEFT JOIN inscriptions i ON i.formation_id = f.id
GROUP BY f.id, f.titre
ORDER BY inscrits DESC, f.titre;
-- Machine Learning, Python, SQL : 2 ; Anglais, Excel : 1 ; Docker : 0
```

### Exercice 2 — Jamais noté

Affichez les étudiants qui n'ont encore reçu aucune note (aucune inscription, ou seulement des inscriptions non notées).

```solution-sql
SELECT e.prenom
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id AND i.note IS NOT NULL
WHERE i.id IS NULL;
-- Karim (inscrit mais pas encore noté) et Yanis (aucune inscription)
```
"""

M4_L3 = r"""
## Combiner jointures et agrégations

Les jointures prennent toute leur puissance associées à `GROUP BY`. La méthode est toujours la même :

1. **joindre** les tables pour disposer de toutes les colonnes utiles ;
2. **filtrer** les lignes avec `WHERE` ;
3. **grouper** et **agréger** ;
4. **trier** et **limiter**.

## Statistiques par formation

```sql
SELECT f.titre,
       COUNT(i.id)           AS inscrits,
       ROUND(AVG(i.note), 1) AS moyenne
FROM formations f
LEFT JOIN inscriptions i ON i.formation_id = f.id
GROUP BY f.id, f.titre
ORDER BY inscrits DESC, f.titre;
```

```text
titre                 | inscrits | moyenne
----------------------+----------+--------
Machine Learning      | 2        | 18.0
Python pour débutants | 2        | 12.5
SQL pour débutants    | 2        | 14.0
Anglais professionnel | 1        | 11.0
Excel avancé          | 1        | 12.0
Docker                | 0        | NULL
```

Docker n'a ni inscrit ni moyenne : `AVG` sur un groupe sans aucune note renvoie `NULL`.

## Statistiques par catégorie

On peut grouper sur une colonne de n'importe quelle table jointe :

```sql
SELECT f.categorie, COUNT(i.id) AS inscrits
FROM formations f
LEFT JOIN inscriptions i ON i.formation_id = f.id
GROUP BY f.categorie
ORDER BY inscrits DESC, f.categorie;
-- Bases de données, Data Science, Programmation : 2 ; Business Intelligence, Langues : 1 ; Cloud et DevOps : 0
```

## Trois tables et un calcul

Combien chaque étudiant a-t-il dépensé en formations ?

```sql
SELECT e.prenom, SUM(f.prix) AS depense
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id
JOIN formations f   ON f.id = i.formation_id
GROUP BY e.id, e.prenom
ORDER BY depense DESC, e.prenom;
```

```text
prenom | depense
-------+--------
Amina  | 99
Sofia  | 99
Emma   | 49
Lucas  | 29
Karim  | 0
```

Amina a suivi Python (0), SQL (0) et Machine Learning (99) : 99 € au total. Yanis n'apparaît pas (aucune inscription, `INNER JOIN`).

## Moyenne par ville

```sql
SELECT e.ville, ROUND(AVG(i.note), 1) AS moyenne
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id
WHERE i.note IS NOT NULL
GROUP BY e.ville
ORDER BY moyenne DESC;
```

```text
ville | moyenne
------+--------
Paris | 16.0
Lille | 12.0
Lyon  | 10.0
```

Paris : (16 + 14 + 18) / 3 = 16. Marseille est absente, car la seule inscription de Karim n'est pas notée.

## Vérifier ses résultats

Une requête qui ne renvoie pas d'erreur n'est pas forcément juste. Prenez l'habitude de vérifier :

- **le nombre de lignes** : est-il plausible ? Un nombre trop élevé signale souvent une jointure mal écrite ;
- **un cas à la main** : recalculez une ligne du résultat à partir des tables, comme ci-dessus pour Amina ;
- **les NULL** : les lignes sans correspondance ou les valeurs manquantes sont-elles traitées comme vous le souhaitez ?

## À retenir

- Méthode : joindre → filtrer → grouper et agréger → trier.
- Le `GROUP BY` peut porter sur n'importe quelle colonne des tables jointes.
- `INNER JOIN` ou `LEFT JOIN` selon que les lignes sans correspondance doivent apparaître ou non.
- Vérifiez toujours le nombre de lignes et recalculez un cas à la main.

## Exercices

### Exercice 1 — Heures de formation par étudiant

Affichez, pour chaque étudiant inscrit, le nombre total d'heures de formation qu'il suit.

```solution-sql
SELECT e.prenom, SUM(f.duree_heures) AS heures
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id
JOIN formations f   ON f.id = i.formation_id
GROUP BY e.id, e.prenom
ORDER BY heures DESC;
-- Amina 39 (11 + 8 + 20), Sofia 20, Lucas 19 (11 + 8), Karim 8, Emma 6
```

### Exercice 2 — Catégories qui réussissent

Affichez les catégories dont la moyenne des notes est d'au moins 12, avec cette moyenne arrondie à une décimale.

```solution-sql
SELECT f.categorie, ROUND(AVG(i.note), 1) AS moyenne
FROM formations f
JOIN inscriptions i ON i.formation_id = f.id
GROUP BY f.categorie
HAVING AVG(i.note) >= 12
ORDER BY moyenne DESC;
-- Data Science 18.0, Bases de données 14.0, Programmation 12.5, Business Intelligence 12.0
```
"""

# ---------------------------------------------------------------------------
# Module 5 — Créer et modifier des données
# ---------------------------------------------------------------------------
M5_L1 = r"""
## Le langage de définition des données

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
```
"""

M5_L2 = r"""
## Ajouter des lignes : INSERT

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
```
"""

M5_L3 = r"""
## Une requête dans une requête

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
- Toute question métier se décompose : quelles tables, quelles lignes, quels groupes, quel ordre.
"""

# ---------------------------------------------------------------------------
# Quiz
# ---------------------------------------------------------------------------
QUIZ_M3 = [
    ("single", "Que renvoie COUNT(note) sur la table inscriptions, qui compte 8 lignes dont 2 sans note ?", None,
     ["8", "6", "2", "NULL"], [1],
     "COUNT(colonne) ne compte que les valeurs non NULL : 6. COUNT(*) compterait les 8 lignes."),
    ("single", "Les notes sont 16, 14, 9, 18, 12, 11, NULL et NULL. Que vaut AVG(note) ?", None,
     ["10", "13,3 environ", "NULL", "80"], [1],
     "AVG ignore les NULL : 80 / 6 ≈ 13,3. Pour compter les absences comme des zéros, il faudrait AVG(COALESCE(note, 0)) = 10."),
    ("single", "Combien de lignes renvoie cette requête ?", "SELECT ville, COUNT(*)\nFROM etudiants\nGROUP BY ville;",
     ["1", "4", "6", "Une erreur"], [1],
     "GROUP BY produit une ligne par groupe. Il y a 4 villes différentes : Paris, Lyon, Marseille et Lille."),
    ("single", "Pourquoi cette requête est-elle refusée par PostgreSQL ?", "SELECT ville, prenom, COUNT(*)\nFROM etudiants\nGROUP BY ville;",
     ["COUNT(*) est interdit avec GROUP BY", "prenom n'est ni groupé ni agrégé",
      "ville doit être agrégée", "Il manque un ORDER BY"], [1],
     "Chaque colonne du SELECT doit être dans le GROUP BY ou dans une agrégation. Un groupe « Paris » contient deux prénoms : SQL ne peut pas choisir lequel afficher."),
    ("single", "Quelle clause permet de ne garder que les groupes ayant au moins 2 lignes ?", None,
     ["WHERE COUNT(*) >= 2", "HAVING COUNT(*) >= 2", "GROUP BY COUNT(*) >= 2", "LIMIT 2"], [1],
     "HAVING filtre les groupes après le regroupement et accepte les agrégations. WHERE agit avant le regroupement et ne peut pas utiliser COUNT."),
    ("single", "Dans quel ordre logique le SGBD exécute-t-il ces clauses ?", None,
     ["SELECT, FROM, WHERE, GROUP BY, HAVING", "FROM, WHERE, GROUP BY, HAVING, SELECT",
      "FROM, GROUP BY, WHERE, SELECT, HAVING", "WHERE, FROM, SELECT, GROUP BY, HAVING"], [1],
     "Ordre logique : FROM, WHERE, GROUP BY, HAVING, SELECT, puis ORDER BY et LIMIT. C'est pourquoi un alias du SELECT n'est pas utilisable dans WHERE."),
    ("true_false", "COUNT(DISTINCT etudiant_id) compte une seule fois un étudiant inscrit à plusieurs formations.", None,
     ["Vrai", "Faux"], [0],
     "DISTINCT élimine les doublons avant de compter : Amina, inscrite trois fois, n'est comptée qu'une fois."),
    ("multiple", "Quelles conditions peuvent figurer dans un WHERE ?", None,
     ["note >= 10", "COUNT(*) > 1", "ville IN ('Paris', 'Lyon')", "AVG(note) > 12"], [0, 2],
     "WHERE accepte les conditions sur les lignes. Les agrégations (COUNT, AVG…) ne sont autorisées que dans HAVING, SELECT et ORDER BY."),
    ("single", "Que calcule cette expression ?", "SUM(CASE WHEN note >= 10 THEN 1 ELSE 0 END)",
     ["La somme des notes supérieures ou égales à 10", "Le nombre de notes supérieures ou égales à 10",
      "La moyenne des notes", "Le nombre total de lignes"], [1],
     "Le CASE vaut 1 pour chaque note ≥ 10 et 0 sinon : la somme de ces 1 compte les notes ≥ 10."),
    ("single", "Que renvoie MAX(note) pour un groupe dont toutes les notes sont NULL ?", None,
     ["0", "NULL", "Une erreur", "20"], [1],
     "Les agrégations ignorent les NULL ; s'il ne reste aucune valeur, le résultat est NULL. Seul COUNT renvoie 0 dans ce cas."),
]

QUIZ_M4 = [
    ("single", "Qu'est-ce qu'une clé étrangère ?", None,
     ["Une colonne qui fait référence à la clé primaire d'une autre table", "Une clé de chiffrement externe",
      "La clé primaire d'une table importée", "Une colonne qui accepte les doublons"], [0],
     "inscriptions.etudiant_id est une clé étrangère : elle référence etudiants.id, et la base refuse une valeur qui n'y existe pas."),
    ("single", "Combien de lignes renvoie cette jointure ?", "SELECT e.prenom, i.formation_id\nFROM etudiants e\nJOIN inscriptions i ON i.etudiant_id = e.id;",
     ["6", "8", "48", "9"], [1],
     "INNER JOIN produit une ligne par inscription ayant un étudiant correspondant : 8 lignes. Yanis, sans inscription, n'apparaît pas."),
    ("single", "Même question avec un LEFT JOIN : combien de lignes ?", "SELECT e.prenom, i.formation_id\nFROM etudiants e\nLEFT JOIN inscriptions i ON i.etudiant_id = e.id;",
     ["6", "8", "9", "14"], [2],
     "Les 8 inscriptions donnent 8 lignes, et LEFT JOIN ajoute une ligne pour Yanis, qui n'a aucune correspondance (formation_id NULL) : 9 lignes."),
    ("single", "Que se passe-t-il si l'on oublie la condition de jointure entre 8 inscriptions et 6 étudiants (CROSS JOIN) ?", None,
     ["Une erreur systématique", "8 lignes", "48 lignes : chaque inscription est associée à chaque étudiant", "6 lignes"], [2],
     "Sans condition, chaque ligne de la première table est associée à chaque ligne de la seconde : 8 × 6 = 48. C'est le produit cartésien."),
    ("single", "Pourquoi écrire COUNT(i.id) plutôt que COUNT(*) après un LEFT JOIN ?", None,
     ["COUNT(*) est plus lent", "Pour compter 0 et non 1 pour les lignes sans correspondance",
      "COUNT(*) est interdit avec LEFT JOIN", "Il n'y a aucune différence"], [1],
     "La ligne d'un étudiant sans inscription existe (avec des NULL à droite) : COUNT(*) la compte, COUNT(i.id) ignore le NULL et donne 0."),
    ("single", "Quelle requête trouve les formations sans aucun inscrit ?", None,
     ["SELECT f.titre FROM formations f JOIN inscriptions i ON i.formation_id = f.id WHERE i.id IS NULL;",
      "SELECT f.titre FROM formations f LEFT JOIN inscriptions i ON i.formation_id = f.id WHERE i.id IS NULL;",
      "SELECT f.titre FROM inscriptions i LEFT JOIN formations f ON f.id = i.formation_id WHERE f.id IS NULL;",
      "SELECT f.titre FROM formations f LEFT JOIN inscriptions i ON i.formation_id = f.id WHERE i.id = NULL;"], [1],
     "Il faut conserver toutes les formations (LEFT JOIN depuis formations) puis garder celles sans correspondance (i.id IS NULL). Un INNER JOIN les exclut d'emblée ; = NULL n'est jamais vrai."),
    ("true_false", "Dans « A LEFT JOIN B », toutes les lignes de B sont conservées.", None,
     ["Vrai", "Faux"], [1],
     "C'est la table de gauche, A, qui est conservée en entier. Les lignes de B n'apparaissent que si elles correspondent à une ligne de A."),
    ("single", "Pourquoi cette requête renvoie-t-elle une erreur « colonne ambiguë » ?", "SELECT id, prenom, note\nFROM etudiants e\nJOIN inscriptions i ON i.etudiant_id = e.id;",
     ["prenom existe dans les deux tables", "id existe dans les deux tables", "note est NULL pour certaines lignes", "Il manque INNER"], [1],
     "etudiants et inscriptions ont toutes deux une colonne id : il faut préciser e.id ou i.id. INNER est facultatif."),
    ("multiple", "Quelles affirmations sur la normalisation sont exactes ?", None,
     ["Chaque information est stockée une seule fois", "Elle impose de tout mettre dans une seule table",
      "Elle évite les incohérences lors des modifications", "Elle s'appuie sur des identifiants qui relient les tables"], [0, 2, 3],
     "Normaliser, c'est répartir les données en tables reliées par des clés, pour stocker chaque information une fois et éviter les copies divergentes. C'est l'inverse d'une table unique."),
    ("single", "Avec un LEFT JOIN etudiants → inscriptions, où placer la condition « note >= 10 » pour garder aussi les étudiants sans note ?", None,
     ["Dans le WHERE", "Dans le ON de la jointure", "Dans le GROUP BY", "Dans le SELECT"], [1],
     "Dans le WHERE, la condition élimine les lignes où note est NULL, y compris celles des étudiants sans inscription : le LEFT JOIN devient un INNER JOIN. Dans le ON, elle filtre seulement les correspondances."),
]

QUIZ_M5 = [
    ("single", "Que fait cette requête ?", "UPDATE formations SET prix = 0;",
     ["Elle provoque une erreur car il manque WHERE", "Elle rend gratuite la première formation",
      "Elle rend gratuites toutes les formations", "Elle ne fait rien sans COMMIT"], [2],
     "Sans WHERE, UPDATE s'applique à toutes les lignes. La requête est valide et s'exécute immédiatement (hors transaction ouverte)."),
    ("single", "Quelle contrainte garantit qu'une note est comprise entre 0 et 20 ?", None,
     ["UNIQUE", "NOT NULL", "CHECK (note BETWEEN 0 AND 20)", "DEFAULT 0"], [2],
     "CHECK impose une condition à chaque valeur. UNIQUE interdit les doublons, NOT NULL impose une valeur, DEFAULT fournit une valeur par défaut."),
    ("single", "Quel type choisir pour stocker un prix ?", None,
     ["FLOAT", "REAL", "NUMERIC(8, 2)", "TEXT"], [2],
     "NUMERIC stocke les décimaux de façon exacte. Les types à virgule flottante (FLOAT, REAL) introduisent des erreurs d'arrondi inacceptables pour de l'argent."),
    ("single", "Quelle est la meilleure pratique avant un DELETE délicat ?", None,
     ["Exécuter d'abord un SELECT avec le même WHERE pour vérifier les lignes",
      "Supprimer puis recréer les lignes manquantes", "Retirer le WHERE pour aller plus vite", "Désactiver les clés étrangères"], [0],
     "Le SELECT avec le même WHERE montre exactement les lignes qui seront supprimées. On peut en plus travailler dans une transaction pour pouvoir annuler."),
    ("true_false", "ROLLBACK annule toutes les modifications effectuées depuis le BEGIN de la transaction.", None,
     ["Vrai", "Faux"], [0],
     "Une transaction est « tout ou rien » : COMMIT valide l'ensemble, ROLLBACK l'annule entièrement."),
    ("single", "Pourquoi cette insertion échoue-t-elle ?", "INSERT INTO inscriptions (id, etudiant_id, formation_id, date_inscription)\nVALUES (9, 42, 1, '2026-11-05');",
     ["La date est mal écrite", "L'étudiant 42 n'existe pas : la clé étrangère est violée",
      "La note est obligatoire", "L'identifiant 9 est déjà pris"], [1],
     "etudiant_id référence etudiants(id). Aucun étudiant n'a l'identifiant 42 : la base refuse cette inscription orpheline. La note, elle, peut être NULL."),
    ("single", "Que renvoie cette requête ?", "SELECT titre FROM formations\nWHERE prix > (SELECT AVG(prix) FROM formations);",
     ["Les formations gratuites", "Les formations plus chères que le prix moyen (36 €)",
      "La formation la plus chère", "Une erreur : une sous-requête est interdite dans WHERE"], [1],
     "La sous-requête calcule le prix moyen (36 €) ; la requête principale garde les formations plus chères : Excel avancé, Machine Learning et Docker."),
    ("multiple", "Quelles instructions modifient les données ou la structure de la base ?", None,
     ["SELECT", "INSERT", "DELETE", "ALTER TABLE"], [1, 2, 3],
     "INSERT ajoute des lignes, DELETE en supprime, ALTER TABLE modifie la structure. SELECT se contente de lire."),
    ("single", "Comment une application doit-elle transmettre la saisie d'un utilisateur à une requête SQL ?", None,
     ["En la collant directement dans le texte de la requête", "Avec une requête paramétrée",
      "En la mettant en majuscules", "En supprimant les espaces"], [1],
     "Les requêtes paramétrées séparent le code SQL des données : un texte malveillant ne peut pas modifier la requête. C'est la protection standard contre l'injection SQL."),
    ("single", "Quand préférer NOT EXISTS à NOT IN ?", None,
     ["Jamais, ils sont toujours équivalents", "Quand la sous-requête peut renvoyer des NULL",
      "Quand la table est vide", "Uniquement en MySQL"], [1],
     "Si la liste de NOT IN contient un NULL, la condition n'est jamais vraie et la requête ne renvoie rien. NOT EXISTS n'a pas ce piège."),
]
