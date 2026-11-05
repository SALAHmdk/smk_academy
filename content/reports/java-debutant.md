# Java pour débutants — rapport de rédaction

- Modules / leçons / questions : 5 / 15 / 50 (quiz : 10 questions par module, au moins une `multiple` chacun)
- Fichiers : `content/java_debutant.py` (COURSE, M1–M2, quiz M1–M2, MODULES), `content/java_debutant_m3_m5.py` (M3–M5, quiz M3–M5), export `content/build/java-debutant.json`
- Code exécuté (OpenJDK 21, `javac` + `java`) : `check_code_blocks.py` → **95 blocs vérifiés, 2 avertissements, 0 échec**
  - Avertissement 1 — `texte-et-saisie`, programme `Saisie` : il lit le clavier (`Scanner(System.in)`) ; pendant la vérification l'entrée standard est vide, d'où une `NoSuchElementException`. Le programme compile ; l'exemple de session est volontairement séparé du code par une phrase.
  - Avertissement 2 — `mini-projet-bibliotheque`, bloc « Brancher le clavier » : fragment (méthode `main` de remplacement) non compilable seul, par construction.
- Tous les blocs de sortie (```text) collés après le code sont des sorties réelles, y compris les erreurs de compilation (`javac`) et les piles d'appels d'exceptions (comparaison sur la dernière ligne).
- `validate_course.py` : OK. Structure `5 [3, 3, 3, 3, 3] [10, 10, 10, 10, 10]`.
- Non exécutable ici : rien (seules les commandes `bash` d'installation/compilation ne sont pas exécutées par le contrôle, elles sont standard).

## Points d'attention pour la relecture

- Durée cumulée des leçons : 660 min pour 900 min annoncées (les leçons sont plafonnées à 45 min par la consigne ; le reste correspond aux quiz et à la pratique). Dans la tolérance de `validate_course.py`.
- Longueur : la leçon mini-projet fait environ 13 200 caractères (au-delà des 11 000 conseillés, sous la limite de 16 000 du validateur) car elle contient le programme complet (~6 000 caractères).
- Affirmations de version volontairement limitées : lancement direct `java Fichier.java` « depuis Java 11 », records « disponibles en Java 17 », Java 17 cité comme LTS ; le reste est présenté comme « Java moderne (17+) ». `instanceof` avec variable (`x instanceof Chat c`) et `switch` avec flèches sont standard en Java 17.
- Les sorties de `printf("%.2f")` dépendent de la locale : vérifiées en `en_US` (point décimal) ; une note dans la leçon M1 L3 prévient qu'un système en français peut afficher une virgule.
- Le numéro de ligne d'une pile d'appels (`Validation.java:26`, `Plantage.java:5`) correspond au bloc tel qu'écrit : toute modification du code de ces exemples impose de mettre à jour la sortie.
- Tri des titres du mini-projet et des produits (M4 L2) : ordre par code de caractère (`É` après les lettres non accentuées), explicitement signalé dans la leçon avec mention de `java.text.Collator`.
