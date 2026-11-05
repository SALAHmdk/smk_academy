-- Généré par scripts/build_seed.py — ne pas modifier à la main.
insert into public.courses (id, slug, title, subtitle, description, category_id, topic, cover_label, level, duration_minutes, objectives, prerequisites, status, is_premium, position) values ('458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$sql-debutant$smk$, $smk$SQL pour débutants$smk$, $smk$Interrogez une base de données avec confiance.$smk$, $smk$Apprenez à lire et à modifier des données avec SQL, le langage commun à PostgreSQL, MySQL, SQLite, Oracle et SQL Server. Une seule base d'exemple vous accompagne de la première requête SELECT jusqu'aux jointures, agrégations et sous-requêtes. Chaque leçon propose des exercices corrigés et chaque module se termine par un quiz noté sur 20.$smk$, (select id from public.categories where slug = $smk$bases-de-donnees$smk$), $smk$SQL$smk$, $smk$SQL$smk$, $smk$debutant$smk$, 480, array[$smk$Comprendre l'organisation d'une base de données relationnelle$smk$, $smk$Extraire, filtrer et trier des données avec SELECT$smk$, $smk$Calculer des statistiques avec GROUP BY et les fonctions d'agrégation$smk$, $smk$Croiser plusieurs tables avec les jointures$smk$, $smk$Créer des tables et modifier des données en toute sécurité$smk$]::text[], array[$smk$Savoir utiliser un ordinateur et un navigateur$smk$, $smk$Aucune connaissance préalable en programmation ou en base de données$smk$]::text[], 'coming_soon', false, 2)
on conflict (slug) do update set title = excluded.title, subtitle = excluded.subtitle, description = excluded.description, category_id = excluded.category_id, level = excluded.level, duration_minutes = excluded.duration_minutes, objectives = excluded.objectives, prerequisites = excluded.prerequisites, is_premium = excluded.is_premium, position = excluded.position;

insert into public.modules (id, course_id, title, description, position, status) values
('1c537041-9ffb-57a1-ba64-ffae2d99cc2b', '458089cd-7c63-54a4-8e5d-dda50ea92fd3', $smk$Trier, limiter et transformer$smk$, $smk$Ordonner les résultats, paginer, utiliser les fonctions et CASE.$smk$, 2, 'draft')
on conflict (id) do update set title = excluded.title, description = excluded.description, position = excluded.position;

insert into public.lessons (id, module_id, slug, title, summary, content_md, duration_minutes, position) values
('a421ad6d-2ea7-56a8-82a2-29a3815b7cdb', '1c537041-9ffb-57a1-ba64-ffae2d99cc2b', $smk$order-by-limit$smk$, $smk$Trier et limiter les résultats$smk$, $smk$ORDER BY, ASC/DESC, plusieurs critères, LIMIT et OFFSET.$smk$, $smk$## Trier avec ORDER BY

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
```$smk$, 20, 1),
('6b065d94-4734-5e54-b60a-ab3fb42e7e4b', '1c537041-9ffb-57a1-ba64-ffae2d99cc2b', $smk$fonctions$smk$, $smk$Fonctions sur le texte, les nombres et NULL$smk$, $smk$UPPER, LENGTH, SUBSTR, ||, ROUND, COALESCE et les dates.$smk$, $smk$## Les fonctions SQL

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
```$smk$, 25, 2),
('9b324705-271c-5e86-8cc2-983fff836cd1', '1c537041-9ffb-57a1-ba64-ffae2d99cc2b', $smk$case-when$smk$, $smk$Conditions avec CASE$smk$, $smk$Produire une valeur selon des conditions, ligne par ligne.$smk$, $smk$## Choisir une valeur selon une condition : CASE

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
```$smk$, 20, 3)
on conflict (id) do update set slug = excluded.slug, title = excluded.title, summary = excluded.summary, content_md = excluded.content_md, duration_minutes = excluded.duration_minutes, position = excluded.position;

insert into public.quizzes (id, module_id, title, pass_mark) values
('7538fe6d-cfae-51db-8f59-02fb635b94de', '1c537041-9ffb-57a1-ba64-ffae2d99cc2b', $smk$Quiz — Trier, limiter et transformer$smk$, 10)
on conflict (id) do update set title = excluded.title, pass_mark = excluded.pass_mark;

insert into public.quiz_questions (id, quiz_id, position, kind, prompt, code, points) values
('9cb75b59-fb10-5151-b955-075f2330339d', '7538fe6d-cfae-51db-8f59-02fb635b94de', 1, $smk$single$smk$, $smk$Quelle clause trie les formations de la plus chère à la moins chère ?$smk$, null, 2),
('588a249f-4c2b-5539-919b-a93e1017a660', '7538fe6d-cfae-51db-8f59-02fb635b94de', 2, $smk$true_false$smk$, $smk$Sans ORDER BY, les lignes sont toujours renvoyées dans l'ordre de leur insertion.$smk$, null, 2),
('e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', '7538fe6d-cfae-51db-8f59-02fb635b94de', 3, $smk$single$smk$, $smk$Quelle requête affiche la page 3 d'une liste, à raison de 10 étudiants par page ?$smk$, null, 2),
('327adab5-17d5-52cb-9434-48d090c9a640', '7538fe6d-cfae-51db-8f59-02fb635b94de', 4, $smk$single$smk$, $smk$Quel est l'ordre correct des clauses ?$smk$, null, 2),
('9764e1fd-4e0c-5465-89d4-778d6381ef8e', '7538fe6d-cfae-51db-8f59-02fb635b94de', 5, $smk$single$smk$, $smk$Que vaut l'expression suivante ?$smk$, $smk$COALESCE(NULL, NULL, 'Lyon', 'Paris')$smk$, 2),
('4958f982-34b1-5588-940f-ddf468a2d400', '7538fe6d-cfae-51db-8f59-02fb635b94de', 6, $smk$single$smk$, $smk$Que vaut NULL + 5 ?$smk$, null, 2),
('89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', '7538fe6d-cfae-51db-8f59-02fb635b94de', 7, $smk$single$smk$, $smk$Que renvoie UPPER(SUBSTR('benali', 1, 3)) ?$smk$, null, 2),
('0d7f9851-c287-5a99-acfb-e9f3ad180bc4', '7538fe6d-cfae-51db-8f59-02fb635b94de', 8, $smk$single$smk$, $smk$Quelle mention reçoit une note de 18 avec ce CASE ?$smk$, $smk$CASE
  WHEN note >= 10 THEN 'Validé'
  WHEN note >= 16 THEN 'Très bien'
  ELSE 'Non validé'
END$smk$, 2),
('8f81633f-3d4d-5518-83e7-4bb82b4d1585', '7538fe6d-cfae-51db-8f59-02fb635b94de', 9, $smk$true_false$smk$, $smk$Un CASE sans ELSE renvoie NULL pour les lignes qui ne vérifient aucune condition.$smk$, null, 2),
('3d411f86-9427-5237-a112-9db86fe58169', '7538fe6d-cfae-51db-8f59-02fb635b94de', 10, $smk$multiple$smk$, $smk$Quelles requêtes affichent les 2 formations les plus courtes ?$smk$, null, 2)
on conflict (id) do update set position = excluded.position, kind = excluded.kind, prompt = excluded.prompt, code = excluded.code, points = excluded.points;

insert into public.quiz_options (id, question_id, position, label) values
('5e018c4b-f684-5b10-9996-94c20dcbad09', '9cb75b59-fb10-5151-b955-075f2330339d', 1, $smk$ORDER BY prix$smk$),
('eada8002-65be-5d37-8643-713858bb0ed7', '9cb75b59-fb10-5151-b955-075f2330339d', 2, $smk$ORDER BY prix DESC$smk$),
('548008e4-17ab-56f8-859b-265e4241dc49', '9cb75b59-fb10-5151-b955-075f2330339d', 3, $smk$SORT BY prix DESC$smk$),
('3ed1a7bc-3472-5e34-8a22-7dd157e62147', '9cb75b59-fb10-5151-b955-075f2330339d', 4, $smk$ORDER prix DESC$smk$),
('7cddb1ce-99e0-5c35-8f76-3e93a4ce79ed', '588a249f-4c2b-5539-919b-a93e1017a660', 1, $smk$Vrai$smk$),
('e510de46-738c-5432-8e17-bfff2f58fbd0', '588a249f-4c2b-5539-919b-a93e1017a660', 2, $smk$Faux$smk$),
('2451f0b8-6f15-5efe-8ef1-fc33859a052f', 'e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', 1, $smk$... LIMIT 10 OFFSET 30$smk$),
('8622ef76-6fd6-5994-91f0-36c360e28d26', 'e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', 2, $smk$... LIMIT 10 OFFSET 20$smk$),
('9a5238e6-1e0b-5ffc-a65b-fc7bf7d65d50', 'e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', 3, $smk$... LIMIT 30 OFFSET 10$smk$),
('f6dff124-9101-520a-b717-0421acafebca', 'e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', 4, $smk$... LIMIT 3 OFFSET 10$smk$),
('15494324-9def-5971-9df5-b7eb5a9c58b2', '327adab5-17d5-52cb-9434-48d090c9a640', 1, $smk$SELECT, FROM, ORDER BY, WHERE, LIMIT$smk$),
('3bf8eddc-2139-510c-9fa2-48932b28ef42', '327adab5-17d5-52cb-9434-48d090c9a640', 2, $smk$SELECT, WHERE, FROM, ORDER BY, LIMIT$smk$),
('a7f09cab-c426-5ef1-8836-e567d99b7544', '327adab5-17d5-52cb-9434-48d090c9a640', 3, $smk$SELECT, FROM, WHERE, ORDER BY, LIMIT$smk$),
('14924535-e54f-5344-910d-5f65e374fe52', '327adab5-17d5-52cb-9434-48d090c9a640', 4, $smk$FROM, SELECT, WHERE, LIMIT, ORDER BY$smk$),
('87dd1f30-a709-5ac6-b127-7eff551ea3ef', '9764e1fd-4e0c-5465-89d4-778d6381ef8e', 1, $smk$NULL$smk$),
('31a16fc2-df6b-5a2c-89ea-a2be115ce079', '9764e1fd-4e0c-5465-89d4-778d6381ef8e', 2, $smk$'Lyon'$smk$),
('6786e51e-44fc-5be2-8c71-4391ccfa2e48', '9764e1fd-4e0c-5465-89d4-778d6381ef8e', 3, $smk$'Paris'$smk$),
('8aa61c8b-db2c-5960-a990-4af5d55be911', '9764e1fd-4e0c-5465-89d4-778d6381ef8e', 4, $smk$Une erreur$smk$),
('39f71cc3-e4d9-560c-a4b3-f0603a2fcd63', '4958f982-34b1-5588-940f-ddf468a2d400', 1, $smk$5$smk$),
('d68478f0-d109-50e8-a149-f27846448fe0', '4958f982-34b1-5588-940f-ddf468a2d400', 2, $smk$0$smk$),
('a26b7029-f6fc-56b1-b30d-c8805a038313', '4958f982-34b1-5588-940f-ddf468a2d400', 3, $smk$NULL$smk$),
('bbb51c8d-9720-55ce-853e-69a1f1d7123f', '4958f982-34b1-5588-940f-ddf468a2d400', 4, $smk$Une erreur$smk$),
('e94400fb-0dbe-5c14-8eb1-7ab3b6200478', '89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', 1, $smk$'BENALI'$smk$),
('8cb33d81-0e58-5a63-839e-24367b3916d3', '89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', 2, $smk$'BEN'$smk$),
('78ba9269-2faf-565a-a597-108734970657', '89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', 3, $smk$'ben'$smk$),
('98ea7e3b-43e3-5fdc-800e-4fcb6251631f', '89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', 4, $smk$'ALI'$smk$),
('bc357bf0-02d3-5f73-8348-9201aa661925', '0d7f9851-c287-5a99-acfb-e9f3ad180bc4', 1, $smk$Validé$smk$),
('932ac528-c7db-5c08-a973-611cd33709eb', '0d7f9851-c287-5a99-acfb-e9f3ad180bc4', 2, $smk$Très bien$smk$),
('27c22fb8-edca-5b60-8d43-e34a2d2e0dee', '0d7f9851-c287-5a99-acfb-e9f3ad180bc4', 3, $smk$Non validé$smk$),
('cb1c432a-2bc8-5100-8e3f-e8124bb19984', '0d7f9851-c287-5a99-acfb-e9f3ad180bc4', 4, $smk$NULL$smk$),
('b0772ae5-74c3-55fa-b401-db81fea3728e', '8f81633f-3d4d-5518-83e7-4bb82b4d1585', 1, $smk$Vrai$smk$),
('73dc83f1-7b7f-52cb-96eb-72a04c0b4c19', '8f81633f-3d4d-5518-83e7-4bb82b4d1585', 2, $smk$Faux$smk$),
('3d198aa9-e6e9-53cb-b07a-c3411472c608', '3d411f86-9427-5237-a112-9db86fe58169', 1, $smk$SELECT titre FROM formations ORDER BY duree_heures LIMIT 2;$smk$),
('68ca6205-1bc9-5710-96ee-15636e48b237', '3d411f86-9427-5237-a112-9db86fe58169', 2, $smk$SELECT titre FROM formations ORDER BY duree_heures ASC LIMIT 2;$smk$),
('ab033f39-3bea-5526-9aeb-088434d0278f', '3d411f86-9427-5237-a112-9db86fe58169', 3, $smk$SELECT titre FROM formations LIMIT 2;$smk$),
('2d3e9018-2326-562a-b692-b2a4388fd973', '3d411f86-9427-5237-a112-9db86fe58169', 4, $smk$SELECT titre FROM formations ORDER BY duree_heures DESC LIMIT 2;$smk$)
on conflict (id) do update set position = excluded.position, label = excluded.label;

insert into private.quiz_answer_keys (question_id, correct_option_ids, explanation) values
('9cb75b59-fb10-5151-b955-075f2330339d', array['eada8002-65be-5d37-8643-713858bb0ed7']::uuid[], $smk$ORDER BY trie et DESC impose l'ordre décroissant. Sans DESC, le tri est croissant (ASC). SORT BY n'existe pas en SQL standard.$smk$),
('588a249f-4c2b-5539-919b-a93e1017a660', array['e510de46-738c-5432-8e17-bfff2f58fbd0']::uuid[], $smk$L'ordre n'est garanti que par ORDER BY. Le SGBD peut renvoyer les lignes dans n'importe quel ordre, qui peut changer d'une exécution à l'autre.$smk$),
('e54b6aba-9a97-5f8a-a632-0238a5b0f8c7', array['8622ef76-6fd6-5994-91f0-36c360e28d26']::uuid[], $smk$Pour la page p avec n lignes par page : LIMIT n OFFSET (p − 1) × n. Page 3 : on saute les 20 premières lignes et on en garde 10.$smk$),
('327adab5-17d5-52cb-9434-48d090c9a640', array['a7f09cab-c426-5ef1-8836-e567d99b7544']::uuid[], $smk$Les clauses s'écrivent toujours SELECT … FROM … WHERE … ORDER BY … LIMIT. Tout autre ordre provoque une erreur de syntaxe.$smk$),
('9764e1fd-4e0c-5465-89d4-778d6381ef8e', array['31a16fc2-df6b-5a2c-89ea-a2be115ce079']::uuid[], $smk$COALESCE renvoie la première valeur non NULL de la liste, en partant de la gauche : 'Lyon'.$smk$),
('4958f982-34b1-5588-940f-ddf468a2d400', array['a26b7029-f6fc-56b1-b30d-c8805a038313']::uuid[], $smk$Toute opération arithmétique avec NULL donne NULL : une valeur inconnue plus 5 reste inconnue. COALESCE(note, 0) + 5 vaudrait 5.$smk$),
('89a2a53a-f4f2-5917-b0ad-2ecaccef7fe6', array['8cb33d81-0e58-5a63-839e-24367b3916d3']::uuid[], $smk$SUBSTR extrait 3 caractères à partir du premier : 'ben'. UPPER les met ensuite en majuscules : 'BEN'.$smk$),
('0d7f9851-c287-5a99-acfb-e9f3ad180bc4', array['bc357bf0-02d3-5f73-8348-9201aa661925']::uuid[], $smk$La première condition vraie l'emporte : 18 >= 10, donc « Validé », et la suite n'est pas testée. Il faudrait tester >= 16 en premier.$smk$),
('8f81633f-3d4d-5518-83e7-4bb82b4d1585', array['b0772ae5-74c3-55fa-b401-db81fea3728e']::uuid[], $smk$C'est le comportement standard : sans ELSE, la valeur par défaut est NULL. Pensez à prévoir un ELSE ou à traiter explicitement les cas restants.$smk$),
('3d411f86-9427-5237-a112-9db86fe58169', array['3d198aa9-e6e9-53cb-b07a-c3411472c608', '68ca6205-1bc9-5710-96ee-15636e48b237']::uuid[], $smk$Le tri croissant (ASC est la valeur par défaut) met les plus courtes en premier. Sans ORDER BY, LIMIT renvoie deux lignes quelconques ; avec DESC, on obtiendrait les plus longues.$smk$)
on conflict (question_id) do update set correct_option_ids = excluded.correct_option_ids, explanation = excluded.explanation;

update public.modules set status = $smk$published$smk$ where id = '1c537041-9ffb-57a1-ba64-ffae2d99cc2b';
