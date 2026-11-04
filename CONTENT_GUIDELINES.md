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
- Correction d'exercice : bloc ` ```solution ` (affiché replié, coloré comme du Python).
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
