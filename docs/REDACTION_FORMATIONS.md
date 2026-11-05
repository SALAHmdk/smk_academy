# Rédiger une formation SMK Academy — consignes pour les rédacteurs (humains ou agents)

Ce document est la référence pour écrire une formation complète. Modèles à imiter (lisez-en au moins un en entier
avant d'écrire) : `content/sql_debutant.py` + `content/sql_debutant_m3_m5.py`, `content/javascript_debutant.py`
+ `content/javascript_debutant_m3_m5.py`, `content/anglais_pro.py` + `content/anglais_pro_m3_m5.py`.

## Ce que vous livrez

1. `content/<nom>.py` : `COURSE`, quiz des modules 1–2, `MODULES` (5 modules) ; il importe
   `content/<nom>_m3_m5.py` (leçons M3_L1…M5_L3 et QUIZ_M3…QUIZ_M5), exactement comme les modèles.
2. L'export : `python3 scripts/build_seed.py --content <nom> --json` → `content/build/<slug>.json`.
3. `content/reports/<slug>.md` : rapport court et honnête (voir plus bas).

**Ne touchez à AUCUN autre fichier.** Pas de commit, pas de push, pas de migration, pas d'appel à Supabase ou Netlify,
pas d'installation de paquets. Le coordinateur relit, vérifie et publie.

## Structure imposée

- `COURSE` : reprendre tels quels `slug`, `title`, `subtitle`, `level`, `duration_minutes`, `position`,
  `category_slug`, `topic`, `cover_label`, `objectives`, `prerequisites` fournis dans votre mission
  (vous pouvez préciser les objectifs et prérequis, sans changer leur sens). `category` = nom lisible,
  `status: "published"`, `is_premium: False`, `description` de 3–4 phrases.
- **5 modules**, chacun : `position`, `title`, `description`, `status: "published"`, **3 leçons**, **1 quiz**.
- Leçon : `(slug, titre, résumé d'une ligne, contenu_markdown, durée_minutes)`. Slugs en minuscules et tirets,
  uniques dans la formation. Durées réalistes (20–45 min) dont la somme approche `duration_minutes`.
- Quiz : **10 questions**, tuples `(kind, prompt, code_ou_None, [options], [indices corrects], explication)` ;
  `kind` ∈ `single` (1 bonne réponse), `multiple` (≥ 1), `true_false` (options `["Vrai", "Faux"]`).
  4 options en général. Chaque explication dit **pourquoi** la bonne réponse est juste. Variez la position
  de la bonne réponse. Au moins 1 `multiple` par quiz ; pas de question piège sur un détail sans intérêt.
- Contenu des leçons dans des chaînes `r"""…"""` ; ne jamais utiliser la séquence `$smk$`.

## Contenu d'une leçon (Markdown)

Ordre habituel : `## sections` d'explication avec exemples → `## À retenir` (4–6 puces) → `## Exercices`
(2–3 exercices `### Exercice n — titre`, chacun suivi de sa correction).

- Français, vouvoiement, ton clair et bienveillant ; termes techniques anglais expliqués à la première occurrence.
- Progression du simple au complexe ; une notion par section ; un exemple concret pour chaque notion.
- Tableaux Markdown bienvenus pour comparer ; citations `>` pour les conseils et pièges.
- La leçon 3 du module 5 est un **mini-projet** qui mobilise toute la formation.
- Longueur : 6 000 à 11 000 caractères par leçon.
- Blocs de code : ```` ```<langage> ```` (python, js, ts, java, c, cpp, go, rust, php, sql, html, css, bash,
  kotlin, swift, dart, yaml, json, text…). Sortie de programme : bloc ```` ```text ```` **juste après** le code.
- Corrections : ```` ```solution-<langage> ```` (ou ```` ```solution-text ```` pour une réponse rédigée) ; elles
  s'affichent repliées sous « Voir la correction ».

## Exactitude : non négociable

- **Aucun fait inventé.** Pas de chiffres, dates, versions, prix, citations ou fonctionnalités dont vous n'êtes pas sûr.
  Pour les services qui évoluent (AWS, Azure, GCP, Power BI, Tableau, LLM…), décrivez les **concepts durables**
  et dites que l'interface ou les tarifs peuvent changer ; jamais de prix précis.
- **Tout code exécutable ici doit être exécuté.** Langages disponibles : Python 3 (avec numpy, pandas, scipy,
  scikit-learn), Node.js, TypeScript (`tsc`), Java, C (`gcc`), C++ (`g++`), Go, Rust, PHP, Git.
  Non disponibles (relecture attentive obligatoire, à signaler dans le rapport) : C#, R, Kotlin, Swift, Dart/Flutter,
  MySQL, MongoDB, Oracle, Kubernetes, clouds. Docker : n'exécutez pas de conteneurs.
- Chaque bloc suivi d'un ```` ```text ```` est comparé à sa sortie réelle par
  `python3 scripts/check_code_blocks.py content/build/<slug>.json` : **0 échec exigé**. Examinez chaque
  avertissement (un fragment non autonome est acceptable, une vraie erreur non).
  Pour SQL : `scripts/check_sql_course.py` est spécifique au cours SQL ; pour PostgreSQL vous pouvez écrire des
  exemples compatibles et les relire soigneusement.
- Sorties : copiez la **vraie** sortie (y compris le format exact de `print`, des tableaux, des flottants).
- Pas de contenu sous droit d'auteur reproduit (textes de documentation, paroles, extraits de livres) ;
  écrivez vos propres exemples. Données d'exemple fictives (noms, entreprises, emails en `@exemple.fr`).
- Sécurité : jamais de secret réel ; signaler les bonnes pratiques (requêtes paramétrées, pas de mot de passe en clair…).

## Langues (anglais, espagnol, allemand)

Explications en français, exemples dans la langue étudiée, niveau CECRL respecté (A1 : présent, vocabulaire
du quotidien ; C1 : nuances, registres, argumentation). Grammaire exacte, exemples naturels et actuels.
Pas d'audio disponible : donnez des repères de prononciation simples en français quand c'est utile.

## Avant de rendre

```bash
python3 scripts/build_seed.py --content <nom> --json
python3 scripts/check_code_blocks.py content/build/<slug>.json
node scripts/check_web_course.mjs content/build/<slug>.json   # si la formation contient du HTML/CSS
python3 -c "import json;d=json.load(open('content/build/<slug>.json'));print(len(d['modules']),[len(m['lessons']) for m in d['modules']],[len(m['quiz']['questions']) for m in d['modules']])"
```

Attendu : `5 [3, 3, 3, 3, 3] [10, 10, 10, 10, 10]` et 0 échec.

## Rapport `content/reports/<slug>.md`

```markdown
# <Titre> — rapport de rédaction
- Modules / leçons / questions : 5 / 15 / 50
- Code exécuté : N blocs vérifiés, A avertissements (expliquer chacun en une ligne), 0 échec
- Non exécutable ici : (langages / blocs relus à la main)
- Points d'attention pour la relecture : (ce dont vous n'êtes pas totalement sûr)
```
