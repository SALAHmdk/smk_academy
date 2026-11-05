-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose des exercices corrigés et chaque module se termine par un quiz noté sur 20.$smk$, (select id from public.categories where slug = $smk$bases-de-donnees$smk$), $smk$SQL$smk$, $smk$SQL$smk$, $smk$debutant$smk$, 480, array[$smk$Comprendre l'organisation d'une base de données relationnelle$smk$, $smk$Extraire, filtrer et trier des données avec SELECT$smk$, $smk$Calculer des statistiques avec GROUP BY et les fonctions d'agrégation$smk$, $smk$Croiser plusieurs tables avec les jointures$smk$, $smk$Créer des tables et modifier des données en toute sécurité$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance préalable en programmation ou en base de données$smk$]::text[], 'coming_soon', false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category_id = excluded.category_id, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('a9a348a1-30ab-5d6f-9af0-222d483965cc', '458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$Joindre des tables$smk$, $smk$Croiser les informations de plusieurs tables grâce aux clés étrangères.$smk$, 4, 'draft')
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('34297120-76f9-5bfb-b68f-4f85c95a507c', 'a9a348a1-30ab-5d6f-9af0-222d483965cc', $smk$inner-join$smk$, $smk$Relier deux tables avec JOIN$smk$, $smk$Clés étrangères, INNER JOIN, alias de tables.$smk$, $smk$## Pourquoi plusieurs tables ?

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
```$smk$, 30, 1),
('2dc3314b-ff08-5ca5-b230-1bd53da1c3d0', 'a9a348a1-30ab-5d6f-9af0-222d483965cc', $smk$left-join$smk$, $smk$Garder toutes les lignes avec LEFT JOIN$smk$, $smk$Jointure externe, lignes sans correspondance, trouver les absents.$smk$, $smk$## Le problème des lignes sans correspondance

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
```$smk$, 25, 2),
('109bdb5c-44d2-57dc-92c6-2fb625afab43', 'a9a348a1-30ab-5d6f-9af0-222d483965cc', $smk$jointures-et-agregations$smk$, $smk$Jointures multiples et agrégations$smk$, $smk$Trois tables à la fois, statistiques par étudiant et par formation.$smk$, $smk$## Combiner jointures et agrégations

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
```$smk$, 30, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 'a9a348a1-30ab-5d6f-9af0-222d483965cc', $smk$Quiz — Joindre des tables$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 1, $smk$single$smk$, $smk$Qu'est-ce qu'une clé étrangère ?$smk$, null, 2),
('ffcf2c6c-f161-5247-821d-462ca62ba69f', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 2, $smk$single$smk$, $smk$Combien de lignes renvoie cette jointure ?$smk$, $smk$SELECT e.prenom, i.formation_id
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id;$smk$, 2),
('1936c6e9-b702-5950-b1da-a22a1c90721c', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 3, $smk$single$smk$, $smk$Même question avec un LEFT JOIN : combien de lignes ?$smk$, $smk$SELECT e.prenom, i.formation_id
FROM etudiants e
LEFT JOIN inscriptions i ON i.etudiant_id = e.id;$smk$, 2),
('d936402e-c12c-5194-ac5e-98fddfd9ac35', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 4, $smk$single$smk$, $smk$Que se passe-t-il si l'on oublie la condition de jointure entre 8 inscriptions et 6 étudiants (CROSS JOIN) ?$smk$, null, 2),
('7fa3f4fc-8eb9-568f-abba-801b8928f359', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 5, $smk$single$smk$, $smk$Pourquoi écrire COUNT(i.id) plutôt que COUNT(*) après un LEFT JOIN ?$smk$, null, 2),
('93e17e25-bc61-5822-83c5-d1befecc401b', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 6, $smk$single$smk$, $smk$Quelle requête trouve les formations sans aucun inscrit ?$smk$, null, 2),
('135fe239-edb1-567d-826f-1443b306f7d5', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 7, $smk$true_false$smk$, $smk$Dans « A LEFT JOIN B », toutes les lignes de B sont conservées.$smk$, null, 2),
('d8923c96-14f2-5316-a510-7e1a3146c991', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 8, $smk$single$smk$, $smk$Pourquoi cette requête renvoie-t-elle une erreur « colonne ambiguë » ?$smk$, $smk$SELECT id, prenom, note
FROM etudiants e
JOIN inscriptions i ON i.etudiant_id = e.id;$smk$, 2),
('767c961b-1789-53a8-9789-03daa6cb9169', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 9, $smk$multiple$smk$, $smk$Quelles affirmations sur la normalisation sont exactes ?$smk$, null, 2),
('30403a64-9246-5eaf-aaf6-5c9eca543166', '60ad1ac3-b85c-5da6-a3bf-8bcc342f0544', 10, $smk$single$smk$, $smk$Avec un LEFT JOIN etudiants → inscriptions, où placer la condition « note >= 10 » pour garder aussi les étudiants sans note ?$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('b9fe9d72-21ee-5246-8956-cb602575a97a', 'a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', 1, $smk$Une colonne qui fait référence à la clé primaire d'une autre table$smk$),
('95629ba3-0488-55da-ae09-cb148678fb84', 'a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', 2, $smk$Une clé de chiffrement externe$smk$),
('815e9267-a930-5e39-9d50-37aada2f098b', 'a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', 3, $smk$La clé primaire d'une table importée$smk$),
('19b913c6-ed97-5702-9bc3-ea3c0958d681', 'a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', 4, $smk$Une colonne qui accepte les doublons$smk$),
('50312de4-b96c-56e2-8994-dbc8866a2d08', 'ffcf2c6c-f161-5247-821d-462ca62ba69f', 1, $smk$6$smk$),
('158b76a7-0186-564c-8e0b-50af2578af99', 'ffcf2c6c-f161-5247-821d-462ca62ba69f', 2, $smk$8$smk$),
('b695f942-1a79-5cf0-ab85-7c745b341ef8', 'ffcf2c6c-f161-5247-821d-462ca62ba69f', 3, $smk$48$smk$),
('c1358d94-f06e-5cae-8f5b-cd3f308dbfc0', 'ffcf2c6c-f161-5247-821d-462ca62ba69f', 4, $smk$9$smk$),
('bee90a1c-29a4-5c43-9f9b-a69ba102c466', '1936c6e9-b702-5950-b1da-a22a1c90721c', 1, $smk$6$smk$),
('e2d0e0bb-bb0f-5ec2-bbbb-5beed370850e', '1936c6e9-b702-5950-b1da-a22a1c90721c', 2, $smk$8$smk$),
('0b1d8a5c-cc58-5216-8c70-2f52c5201ea2', '1936c6e9-b702-5950-b1da-a22a1c90721c', 3, $smk$9$smk$),
('a2396272-b921-5199-b009-517281331ce0', '1936c6e9-b702-5950-b1da-a22a1c90721c', 4, $smk$14$smk$),
('f971959a-da3c-5a2f-b06f-754baf84c10e', 'd936402e-c12c-5194-ac5e-98fddfd9ac35', 1, $smk$Une erreur systématique$smk$),
('6655a8de-fcd5-5a3c-bbf0-410d0f975257', 'd936402e-c12c-5194-ac5e-98fddfd9ac35', 2, $smk$8 lignes$smk$),
('1477e4fd-9857-5dba-916b-246ab73dfd50', 'd936402e-c12c-5194-ac5e-98fddfd9ac35', 3, $smk$48 lignes : chaque inscription est associée à chaque étudiant$smk$),
('c6cd80a7-a012-584f-9773-8f629ab04b08', 'd936402e-c12c-5194-ac5e-98fddfd9ac35', 4, $smk$6 lignes$smk$),
('e9d316fa-cbe9-51cf-b682-87b5fcad9ee9', '7fa3f4fc-8eb9-568f-abba-801b8928f359', 1, $smk$COUNT(*) est plus lent$smk$),
('dc4a7237-c03e-5268-845f-4a4e8496cae1', '7fa3f4fc-8eb9-568f-abba-801b8928f359', 2, $smk$Pour compter 0 et non 1 pour les lignes sans correspondance$smk$),
('4ce8c555-6541-5e36-a4ec-8544b034272a', '7fa3f4fc-8eb9-568f-abba-801b8928f359', 3, $smk$COUNT(*) est interdit avec LEFT JOIN$smk$),
('33bb0f16-c7f7-5044-9b9e-95b0d311937b', '7fa3f4fc-8eb9-568f-abba-801b8928f359', 4, $smk$Il n'y a aucune différence$smk$),
('0ccfe0c3-39a2-5bf9-8dfc-a7a848f3e05f', '93e17e25-bc61-5822-83c5-d1befecc401b', 1, $smk$SELECT f.titre FROM formations f JOIN inscriptions i ON i.formation_id = f.id WHERE i.id IS NULL;$smk$),
('f932f3b5-1dda-5aa6-b59c-4f2b700983dc', '93e17e25-bc61-5822-83c5-d1befecc401b', 2, $smk$SELECT f.titre FROM formations f LEFT JOIN inscriptions i ON i.formation_id = f.id WHERE i.id IS NULL;$smk$),
('be985cd0-260d-57e5-8c8f-7a92213ec4e5', '93e17e25-bc61-5822-83c5-d1befecc401b', 3, $smk$SELECT f.titre FROM inscriptions i LEFT JOIN formations f ON f.id = i.formation_id WHERE f.id IS NULL;$smk$),
('8eb5809a-c646-5aab-bb5c-5376c12ea10c', '93e17e25-bc61-5822-83c5-d1befecc401b', 4, $smk$SELECT f.titre FROM formations f LEFT JOIN inscriptions i ON i.formation_id = f.id WHERE i.id = NULL;$smk$),
('af3f06db-8955-5220-835c-a97948b13ab5', '135fe239-edb1-567d-826f-1443b306f7d5', 1, $smk$Vrai$smk$),
('53d4fd0d-28a2-5d78-8641-eb1147a7b954', '135fe239-edb1-567d-826f-1443b306f7d5', 2, $smk$Faux$smk$),
('8cfe20bf-535b-5d88-b403-056504a120ac', 'd8923c96-14f2-5316-a510-7e1a3146c991', 1, $smk$prenom existe dans les deux tables$smk$),
('b572c5ec-43b5-5337-9b30-021c9cd74ebe', 'd8923c96-14f2-5316-a510-7e1a3146c991', 2, $smk$id existe dans les deux tables$smk$),
('4a0fcb5d-036f-525b-855a-29a05e2698e4', 'd8923c96-14f2-5316-a510-7e1a3146c991', 3, $smk$note est NULL pour certaines lignes$smk$),
('a2c90e93-a198-5d92-b3e9-2b3bc42fac95', 'd8923c96-14f2-5316-a510-7e1a3146c991', 4, $smk$Il manque INNER$smk$),
('b7f4ec40-5f8b-5aca-8fb8-86a347118f0f', '767c961b-1789-53a8-9789-03daa6cb9169', 1, $smk$Chaque information est stockée une seule fois$smk$),
('327e4f0e-96dd-52d1-8ec5-bad391316d8f', '767c961b-1789-53a8-9789-03daa6cb9169', 2, $smk$Elle impose de tout mettre dans une seule table$smk$),
('23d93498-bfe8-5099-8551-2973dcdf74c5', '767c961b-1789-53a8-9789-03daa6cb9169', 3, $smk$Elle évite les incohérences lors des modifications$smk$),
('1955ffe1-6cc4-5e0b-9dbf-a8a154eeb03e', '767c961b-1789-53a8-9789-03daa6cb9169', 4, $smk$Elle s'appuie sur des identifiants qui relient les tables$smk$),
('5810f950-66ba-53b3-894e-8f1e3e87ffba', '30403a64-9246-5eaf-aaf6-5c9eca543166', 1, $smk$Dans le WHERE$smk$),
('f861c1b1-32ee-59d0-a49b-d06ce9c1c6e3', '30403a64-9246-5eaf-aaf6-5c9eca543166', 2, $smk$Dans le ON de la jointure$smk$),
('eb1f0032-3ba4-50c0-ba22-e62779a7e64c', '30403a64-9246-5eaf-aaf6-5c9eca543166', 3, $smk$Dans le GROUP BY$smk$),
('92de1c6f-1a78-5ef5-82d7-29974c5b9b5f', '30403a64-9246-5eaf-aaf6-5c9eca543166', 4, $smk$Dans le SELECT$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('a9b2d72d-993a-5a7f-9de9-ed6dbb218f6d', array['b9fe9d72-21ee-5246-8956-cb602575a97a']::uuid[], $smk$inscriptions.etudiant_id est une clé étrangère : elle référence etudiants.id, et la base refuse une valeur qui n'y existe pas.$smk$),
('ffcf2c6c-f161-5247-821d-462ca62ba69f', array['158b76a7-0186-564c-8e0b-50af2578af99']::uuid[], $smk$INNER JOIN produit une ligne par inscription ayant un étudiant correspondant : 8 lignes. Yanis, sans inscription, n'apparaît pas.$smk$),
('1936c6e9-b702-5950-b1da-a22a1c90721c', array['0b1d8a5c-cc58-5216-8c70-2f52c5201ea2']::uuid[], $smk$Les 8 inscriptions donnent 8 lignes, et LEFT JOIN ajoute une ligne pour Yanis, qui n'a aucune correspondance (formation_id NULL) : 9 lignes.$smk$),
('d936402e-c12c-5194-ac5e-98fddfd9ac35', array['1477e4fd-9857-5dba-916b-246ab73dfd50']::uuid[], $smk$Sans condition, chaque ligne de la première table est associée à chaque ligne de la seconde : 8 × 6 = 48. C'est le produit cartésien.$smk$),
('7fa3f4fc-8eb9-568f-abba-801b8928f359', array['dc4a7237-c03e-5268-845f-4a4e8496cae1']::uuid[], $smk$La ligne d'un étudiant sans inscription existe (avec des NULL à droite) : COUNT(*) la compte, COUNT(i.id) ignore le NULL et donne 0.$smk$),
('93e17e25-bc61-5822-83c5-d1befecc401b', array['f932f3b5-1dda-5aa6-b59c-4f2b700983dc']::uuid[], $smk$Il faut conserver toutes les formations (LEFT JOIN depuis formations) puis garder celles sans correspondance (i.id IS NULL). Un INNER JOIN les exclut d'emblée ; = NULL n'est jamais vrai.$smk$),
('135fe239-edb1-567d-826f-1443b306f7d5', array['53d4fd0d-28a2-5d78-8641-eb1147a7b954']::uuid[], $smk$C'est la table de gauche, A, qui est conservée en entier. Les lignes de B n'apparaissent que si elles correspondent à une ligne de A.$smk$),
('d8923c96-14f2-5316-a510-7e1a3146c991', array['b572c5ec-43b5-5337-9b30-021c9cd74ebe']::uuid[], $smk$etudiants et inscriptions ont toutes deux une colonne id : il faut préciser e.id ou i.id. INNER est facultatif.$smk$),
('767c961b-1789-53a8-9789-03daa6cb9169', array['b7f4ec40-5f8b-5aca-8fb8-86a347118f0f', '23d93498-bfe8-5099-8551-2973dcdf74c5', '1955ffe1-6cc4-5e0b-9dbf-a8a154eeb03e']::uuid[], $smk$Normaliser, c'est répartir les données en tables reliées par des clés, pour stocker chaque information une fois et éviter les copies divergentes. C'est l'inverse d'une table unique.$smk$),
('30403a64-9246-5eaf-aaf6-5c9eca543166', array['f861c1b1-32ee-59d0-a49b-d06ce9c1c6e3']::uuid[], $smk$Dans le WHERE, la condition élimine les lignes où note est NULL, y compris celles des étudiants sans inscription : le LEFT JOIN devient un INNER JOIN. Dans le ON, elle filtre seulement les correspondances.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

update public.modules set status = $smk$published$smk$ where id = 'a9a348a1-30ab-5d6f-9af0-222d483965cc';
