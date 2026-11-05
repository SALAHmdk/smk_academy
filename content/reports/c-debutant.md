# Langage C — rapport de rédaction

- Modules / leçons / questions : 5 / 15 / 50 (10 par quiz, au moins 1 `multiple` par quiz, positions des bonnes réponses variées)
- Fichiers : `content/c_debutant.py`, `content/c_debutant_m3_m5.py`, export `content/build/c-debutant.json`
- Durée cumulée des leçons : 640 min pour 840 min annoncées (quiz et exercices en plus ; dans la plage acceptée par `validate_course.py`)
- Longueur des leçons : 6 139 à 10 795 caractères

## Contrôles exécutés

- `python3 scripts/check_code_blocks.py content/build/c-debutant.json` : **104 blocs vérifiés, 4 avertissements, 0 échec** (gcc 13.3, `-std=c17 -Wall`).
- `python3 scripts/validate_course.py content/build/c-debutant.json` : **OK**.
- Contrôle complémentaire (hors script) : les 106 programmes complets ont été recompilés avec `-Wall -Wextra -g -fsanitize=address,undefined` et exécutés (entrée standard vide) : aucun rapport ASan/UBSan, aucun avertissement sauf les deux troncatures `snprintf` volontaires (leçon chaînes, signalées dans le texte).
- L'exemple multi-fichiers (`calcul.h`, `calcul.c`, `main.c`) a été compilé et exécuté à part : il affiche `49`, comme indiqué.
- Les sorties de gcc (erreur de point-virgule, `-Wparentheses`, `-Wimplicit-function-declaration`, `-Wuse-after-free`), de Valgrind 3.22 et d'ASan/UBSan citées dans les leçons sont de vrais extraits obtenus ici (adresses et PID variables, signalé au lecteur).

## Avertissements du vérificateur (attendus)

1. `operateurs-printf-scanf` — programme `scanf` : lit le clavier (délai dépassé si l'entrée standard reste ouverte ; renvoie 1 si l'entrée est vide).
2. `chaines-c` — programme `fgets(…, stdin)` : lit le clavier (même raison).
3. et 4. `fonctions-c` — `calcul.c` et `main.c` : fragments d'un projet multi-fichiers, non compilables seuls (testés ensemble à part).

## Non exécutable ici

- Rien : seules les commandes `bash` (compilation, `valgrind`) et les blocs `text` ne sont pas exécutés par le script ; elles ont été lancées à la main.

## Points d'attention pour la relecture

- Tailles (`sizeof(int)` = 4, `double` = 8) et `INT_MAX` correspondent à un ordinateur 64 bits courant ; le texte précise qu'elles dépendent de la plateforme.
- Le message `strerror` (`No such file or directory`) dépend de la langue du système (précisé dans la leçon).
- Le rendu `solution-c` n'a pas d'alias de coloration dans `src/components/markdown.tsx` (seuls python, sql, text, js, html, css en ont) : les corrections C s'affichent sans coloration. Fichier non modifié (hors périmètre).
- Les blocs `h` (fichier d'en-tête) reposent sur l'alias `h` du langage C de highlight.js.
- Faits historiques volontairement généraux : création au début des années 1970 aux laboratoires Bell, noyau Linux et CPython écrits en C, `gets` retirée en C11, normes C89 à C23.
