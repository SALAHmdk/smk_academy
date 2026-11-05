# Rédiger une formation SMK Academy

## Structure

Une formation = 5 modules ; un module = 3 leçons + 1 quiz ; une formation se termine par un examen final. Une formation n'est publiée (`status = 'published'`) que si elle est réellement complète ; un module non rédigé reste `coming_soon` et s'affiche « En préparation ».

## Leçon

- 20 à 30 minutes de lecture, une notion principale.
- Progression : pourquoi → notion → exemples → pièges fréquents → « À retenir » → exercices.
- Chaque exemple de code doit être **exécutable tel quel** et donner le résultat annoncé.
- Phrases courtes, vocabulaire défini à sa première apparition, tutoiement interdit (vouvoiement).
- Au moins 2 exercices par leçon, chacun avec sa correction.

### Markdown

- Titres de section : `##` ; exercices : `###`.
- Code : blocs ` ```python ` ; sortie console : ` ```text `.
- Correction d'exercice : bloc ` ```solution ` (Python), ` ```solution-sql ` ou ` ```solution-text ` (affichés repliés).
- Formation SQL : chaque requête est vérifiée par `python3 scripts/check_sql_course.py`.
- Si le connecteur Supabase demande une confirmation pour un contenu contenant DELETE/DROP/UPDATE, appliquer la migration avec ces mots masqués puis restaurés (voir l'historique du 05/11).
- Encadré : `> texte`.
- Pas d'HTML brut ni d'image pour l'instant (ignorés à l'affichage).

## Quiz

- 10 questions de 2 points (total 20), seuil de validation 10/20.
- Types : `single`, `multiple`, `true_false`.
- Chaque question a une **explication** qui dit pourquoi la bonne réponse est juste et pourquoi les pièges sont faux.
- Les distracteurs reprennent des erreurs réelles de débutants (confusion `=`/`==`, borne de `range` incluse…).
- Une question à choix multiples n'est juste que si toutes les bonnes options et seulement elles sont cochées : l'indiquer dans l'énoncé (« lesquels… »).

## Publier

1. Modifier `content/<formation>.py`.
2. `python3 scripts/build_seed.py > supabase/migrations/<horodatage>_seed_<formation>.sql`
3. Appliquer la migration sur Supabase, puis vérifier dans l'application.

(L'interface d'administration du jalon 4 remplacera cette procédure.)

## Publier une formation (depuis le 05/11/2026)

1. Rédiger `content/<nom>.py` (COURSE + MODULES ; 5 modules × 3 leçons, un quiz de 10 questions par module).
2. `python3 scripts/build_seed.py --content <nom> --json` → `content/build/<slug>.json`.
3. Vérifier : `npm run check:content` (requêtes SQL exécutées, exemples JavaScript exécutés et comparés à leur sortie,
   HTML équilibré et CSS analysé par Lightning CSS).
4. Commit + push : le build Netlify appelle `scripts/import_content.mjs`, qui charge en base les formations dont le
   contenu a changé (RPC `content_import_if_changed`, protégée par `CONTENT_IMPORT_TOKEN`). Aucune suppression.
5. Les retouches faites dans l'administration sur une formation gérée par le dépôt sont écrasées au prochain
   changement de son fichier source : modifier le fichier plutôt que l'administration pour ces formations.

Blocs de correction : ```solution (Python), ```solution-sql, ```solution-js, ```solution-html, ```solution-css, ```solution-text.
