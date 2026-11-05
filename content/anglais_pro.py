"""Contenu de la formation « Anglais professionnel — débutant » (SMK Academy).

Explications en français, exemples en anglais. Niveau visé : A2 → B1 en contexte professionnel.
Blocs ```text pour les dialogues et les emails, ```solution-text pour les corrections.
`scripts/build_seed.py --content anglais_pro --json` produit content/build/anglais-professionnel-debutant.json.
"""

import importlib.util as _ilu
from pathlib import Path as _Path

_spec = _ilu.spec_from_file_location("anglais_pro_m3_m5", _Path(__file__).with_name("anglais_pro_m3_m5.py"))
_m35 = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_m35)

COURSE = {
    "slug": "anglais-professionnel-debutant",
    "title": "Anglais professionnel — débutant",
    "subtitle": "Les bases pour communiquer au travail.",
    "description": (
        "Gagnez en aisance dans les situations professionnelles les plus courantes : vous présenter, "
        "présenter votre entreprise, écrire des emails clairs et polis, téléphoner, participer à une "
        "réunion ou à une visioconférence et rendre compte de votre activité. Chaque leçon réunit le "
        "vocabulaire utile, les points de grammaire indispensables, des modèles prêts à l'emploi et des "
        "exercices corrigés ; chaque module se termine par un quiz noté sur 20."
    ),
    "category": "Langues",
    "category_slug": "langues",
    "topic": "Anglais",
    "cover_label": "EN",
    "level": "debutant",
    "duration_minutes": 480,
    "objectives": [
        "Se présenter et présenter son entreprise",
        "Écrire un email professionnel clair et poli",
        "Téléphoner et participer à une visioconférence",
        "Prendre part à une réunion et en résumer les décisions",
        "Rendre compte de son activité et présenter des chiffres",
    ],
    "prerequisites": ["Niveau A1 conseillé (bases de l'anglais courant)"],
    "status": "published",
    "is_premium": False,
    "position": 3,
}

# ---------------------------------------------------------------------------
# Module 1 — Se présenter et présenter son entreprise
# ---------------------------------------------------------------------------
M1_L1 = r"""
## Pourquoi cette formation ?

Au travail, l'anglais sert surtout dans des situations prévisibles : se présenter, écrire un email, appeler un fournisseur, participer à une réunion. Bonne nouvelle : ces situations reposent sur un nombre limité d'expressions. Cette formation vous les donne, avec juste ce qu'il faut de grammaire pour les utiliser correctement.

> Conseil : lisez chaque exemple **à voix haute**. Parler, même seul, est le moyen le plus rapide de gagner en aisance.

## Saluer : formel ou informel ?

| Situation | Formel | Plus détendu |
|---|---|---|
| Arriver | *Good morning* (jusqu'à midi), *Good afternoon* | *Hi*, *Hello* |
| Première rencontre | *Pleased to meet you.* / *Nice to meet you.* | *Nice to meet you.* |
| Demander des nouvelles | *How are you?* | *How's it going?* |
| Répondre | *Very well, thank you. And you?* | *Fine, thanks. You?* |
| Partir | *Goodbye. It was a pleasure.* | *Bye! See you soon.* |

*How do you do?* existe encore, mais il est devenu très formel et rare. *Good evening* sert pour saluer le soir ; pour prendre congé le soir, on dit *Have a good evening*. *Good night* signifie « bonne nuit », au moment d'aller dormir.

## Se présenter

```text
Hello, I'm Amina Benali. I'm a project manager at SMKTECH.
Nice to meet you, Amina. I'm David Clark, from the sales team.
```

Les structures essentielles :

- *I'm* + prénom et nom : **I'm** Amina Benali. (*My name is…* est correct mais plus solennel.)
- *I'm a / an* + métier : I'm **a** developer, I'm **an** engineer. En anglais, l'article est **obligatoire** devant un métier : on ne dit jamais *I'm developer*.
- *I work for / at* + entreprise : I work **for** SMKTECH. / I work **at** SMKTECH.
- *I work in* + service ou secteur : I work **in** marketing, **in** finance, **in** the IT department.

`a` devient `an` devant un **son** voyelle : *an engineer*, *an assistant*, *an hour* (le h ne se prononce pas), mais *a university* (prononcé « you »).

## Le verbe *to be* au présent

| Forme pleine | Contraction | Négation | Question |
|---|---|---|---|
| I am | I'm | I'm not | Am I…? |
| you are | you're | you aren't | Are you…? |
| he / she / it is | he's / she's / it's | he isn't | Is she…? |
| we / they are | we're / they're | we aren't | Are they…? |

À l'oral et dans les emails courants, on utilise les **contractions**. Les formes pleines restent normales dans un écrit très formel.

## Présenter quelqu'un

```text
David, this is Sofia Rossi, our new data analyst.
Sofia, this is David Clark. He's in charge of our UK clients.
```

On présente avec **this is** (et non *he is*) : *This is my colleague, Karim.*

## À retenir

- *Nice to meet you* à la première rencontre ; *Good morning / afternoon* pour un contexte formel.
- *I'm a / an* + métier : l'article est obligatoire.
- *work for / at* une entreprise, *work in* un service ou un secteur.
- *This is…* pour présenter une personne.

## Exercices

### Exercice 1 — Corrigez les erreurs

Chaque phrase contient une erreur. Corrigez-la : (a) *I am engineer.* (b) *I work in Google.* (c) *He is my colleague, Karim* (pour le présenter à quelqu'un). (d) *I'm a assistant.*

```solution-text
(a) I'm an engineer.         → article obligatoire, « an » devant un son voyelle
(b) I work for / at Google.  → « in » s'emploie pour un service ou un secteur
(c) This is my colleague, Karim.
(d) I'm an assistant.
```

### Exercice 2 — Votre présentation

Écrivez trois phrases pour vous présenter : votre nom, votre métier, votre entreprise ou votre service.

```solution-text
Exemple de réponse :
Hello, I'm Lucas Martin. I'm an accountant. I work for a small consulting firm in Lyon, in the finance department.
Vérifiez : contraction « I'm », article devant le métier, bonne préposition (for / at / in).
```
"""

M1_L2 = r"""
## Parler de son travail au présent simple

Pour décrire ce que l'on fait habituellement, l'anglais utilise le **présent simple** :

```text
I manage a team of five people.
I prepare the monthly reports.
She works in the London office.
```

La seule difficulté : à la **3e personne du singulier** (*he, she, it*), on ajoute **-s** au verbe.

| Sujet | Verbe |
|---|---|
| I / you / we / they | work, manage, deal with |
| he / she / it | work**s**, manage**s**, deal**s** with |

Cas particuliers : *go → goes*, *do → does*, *have → has*, *watch → watches*, *study → studies*.

## Négation et questions : *do* / *does*

```text
I don't work on Fridays.          She doesn't speak German.
Do you travel a lot?              Does he work from home?
— Yes, I do. / No, I don't.       — Yes, he does. / No, he doesn't.
```

Après *does* ou *doesn't*, le verbe reprend sa forme de base : *Does she **work**…?* (et non *works*).

## Décrire ses responsabilités

Ces expressions sont incontournables :

- *I'm in charge of* + nom ou verbe en -ing : I'm in charge **of** recruitment. / …of **organising** events.
- *I'm responsible for* + nom ou verbe en -ing : I'm responsible **for** the budget.
- *I deal with* + nom : I deal **with** customer complaints.
- *I report to* + personne : I report **to** the Head of Sales.
- *My job involves* + verbe en -ing : My job involves **travelling** a lot.

```text
What do you do?
— I'm a sales assistant. I deal with orders and I answer customer emails.
  I report to the sales manager.
```

*What do you do?* signifie « Quel est votre métier ? » ; *What are you doing?* signifie « Que faites-vous en ce moment ? ».

## Dire à quelle fréquence

Les adverbes de fréquence se placent **avant le verbe**, mais **après** *to be* :

| Adverbe | Sens |
|---|---|
| always | toujours |
| usually | d'habitude |
| often | souvent |
| sometimes | parfois |
| rarely | rarement |
| never | jamais |

```text
I usually start at 9 a.m.
We often have meetings on Monday.
She is always on time.
```

Pour une fréquence précise : *every day*, *twice a week*, *once a month*, en fin de phrase.

## À retenir

- Présent simple pour les habitudes et les tâches régulières.
- **-s** à la 3e personne : *she manages*, *he goes*.
- *do / does* pour les questions et les négations ; verbe de base ensuite.
- *in charge of*, *responsible for*, *deal with*, *report to*.
- Adverbe de fréquence avant le verbe, après *be*.

## Exercices

### Exercice 1 — Conjuguez

Mettez le verbe au présent simple : (a) She ___ (manage) the IT team. (b) ___ he ___ (work) on Saturdays? (c) We ___ (not / use) this software. (d) My manager ___ (go) to London twice a month.

```solution-text
(a) She manages the IT team.
(b) Does he work on Saturdays?
(c) We don't use this software.
(d) My manager goes to London twice a month.
```

### Exercice 2 — Placez l'adverbe

Remettez dans l'ordre : (a) *late / I / am / never* (b) *answer / usually / emails / I / in the morning* (c) *works / sometimes / she / from home*

```solution-text
(a) I am never late.                       → après « be »
(b) I usually answer emails in the morning. → avant le verbe
(c) She sometimes works from home.
```

### Exercice 3 — Votre poste

Décrivez votre poste en trois phrases en utilisant *in charge of*, *deal with* et *report to*.

```solution-text
Exemple : I'm in charge of the company website. I deal with requests from the marketing team. I report to the IT manager.
```
"""

M1_L3 = r"""
## Présenter son entreprise

Lors d'un premier contact, on vous demandera souvent : *What does your company do?* Voici une présentation type :

```text
SMKTECH is a software company. We are based in Paris and we have offices in Lyon and Montreal.
We develop e-learning platforms for schools and businesses.
We employ around 80 people and our main clients are universities.
```

## Les expressions clés

| Pour dire… | En anglais |
|---|---|
| le secteur | *We're a* software / consulting / logistics *company.* — *We work in* the energy sector. |
| l'activité | *We develop / sell / provide / manufacture* … |
| le lieu | *We're based in* Paris. — *Our head office is in* Lyon. |
| la taille | *We employ* 80 people. — *We have* a team of 80. |
| les clients | *Our clients are mainly* banks. — *We work with* … |
| l'histoire | *The company was founded in* 2015. |

*Provide* signifie « fournir » un service : *We provide training*. *Manufacture* : fabriquer en usine.

## *There is* / *There are*

Pour dire « il y a » :

```text
There is a canteen on the ground floor.
There are three meeting rooms on this floor.
Is there a car park? — Yes, there is. / No, there isn't.
How many employees are there? — There are about 200.
```

*There is* devant un singulier, *there are* devant un pluriel.

## Les grands nombres

| Nombre | Lecture |
|---|---|
| 150 | one hundred **and** fifty (britannique) |
| 2,500 | two thousand five hundred |
| 1,000,000 | one million |
| 3.5 million | three point five million |

Attention aux différences avec le français :

- l'anglais sépare les milliers par une **virgule** (2,500) et les décimales par un **point** (3.5) ;
- *hundred*, *thousand*, *million* ne prennent **pas de -s** après un nombre : *two hundred people* ;
- *billion* = **milliard** (et non « billion » français).

## L'organisation : les services

| Français | Anglais |
|---|---|
| ressources humaines | Human Resources (HR) |
| comptabilité / finance | Accounting / Finance |
| service commercial | Sales |
| service informatique | IT department |
| recherche et développement | R&D |
| service client | Customer Service |
| siège social | head office / headquarters (HQ) |
| directeur général | CEO, Managing Director |

## À retenir

- *We're a … company. We're based in … We employ …*
- *There is* + singulier, *there are* + pluriel.
- Virgule pour les milliers, point pour les décimales ; *two hundred*, sans -s.
- *billion* = milliard.

## Exercices

### Exercice 1 — There is / there are

Complétez : (a) ___ a printer in the office. (b) ___ 25 people in our team. (c) ___ any parking spaces? (d) ___ only one coffee machine.

```solution-text
(a) There is a printer in the office.
(b) There are 25 people in our team.
(c) Are there any parking spaces?
(d) There is only one coffee machine.
```

### Exercice 2 — Lisez les nombres

Écrivez en toutes lettres : (a) 340 (b) 7,200 (c) 1.8 million (d) 4 billion euros.

```solution-text
(a) three hundred and forty (britannique) / three hundred forty (américain)
(b) seven thousand two hundred
(c) one point eight million
(d) four billion euros  → quatre milliards d'euros
```

### Exercice 3 — Présentez une entreprise

Présentez en quatre phrases une entreprise que vous connaissez : secteur, lieu, activité, taille.

```solution-text
Exemple : Dubois Logistics is a transport company. We're based in Lille. We deliver goods to supermarkets in the north of France. We employ about 120 people.
```
"""

# ---------------------------------------------------------------------------
# Module 2 — Les emails professionnels
# ---------------------------------------------------------------------------
M2_L1 = r"""
## La structure d'un email professionnel

Un email efficace est **court**, **poli** et va **droit au but**. Il suit presque toujours la même structure :

```text
Subject: Meeting on Thursday 14 November

Dear Ms Clark,

I am writing to confirm our meeting on Thursday 14 November at 10 a.m.
Please find attached the agenda.

I look forward to seeing you.

Best regards,
Amina Benali
Project Manager, SMKTECH
```

1. **Objet** (*subject*) : précis et court.
2. **Salutation** (*greeting*).
3. **Ouverture** : la raison de l'email.
4. **Corps** : l'information ou la demande.
5. **Clôture** : la suite attendue.
6. **Formule finale** (*sign-off*) et signature.

## Les salutations

| Situation | Salutation | Formule finale |
|---|---|---|
| Destinataire inconnu | *Dear Sir or Madam,* | *Yours faithfully,* (britannique) |
| Nom connu, ton formel | *Dear Mr Clark, / Dear Ms Rossi,* | *Yours sincerely,* / *Kind regards,* |
| Ton neutre (le plus courant) | *Dear David,* | *Best regards,* / *Kind regards,* |
| Collègue proche | *Hi David,* | *Thanks,* / *Best,* |

*Ms* (prononcé « miz ») est la forme neutre pour une femme, que l'on soit mariée ou non : c'est le choix par défaut. *Mrs* désigne une femme mariée, *Miss* une jeune fille : à éviter sauf demande explicite.

> Contrairement au français, on ne recopie pas de longues formules de politesse : « Je vous prie d'agréer… » n'a pas d'équivalent. *Best regards* suffit.

## Ouvrir l'email

- *I am writing to* + verbe : *I am writing to confirm / to ask about / to inform you that…*
- *I am writing regarding* + nom : *…regarding your order no. 4521.*
- *Thank you for your email.* / *Thanks for getting back to me.*
- *Further to our phone call,* … (« Suite à notre appel… »)

## Conclure l'email

- *I look forward to hearing from you.* (« Dans l'attente de votre réponse. »)
- *I look forward to seeing you.* / *…to working with you.*
- *Please let me know if you have any questions.*
- *Please do not hesitate to contact me.*

Attention : *look forward to* est suivi d'un verbe en **-ing** : *I look forward to **hearing** from you* (et non *to hear*).

## Écrire un bon objet

| À éviter | Mieux |
|---|---|
| *Question* | *Question about invoice no. 4521* |
| *Meeting* | *Meeting on Thursday 14 Nov – agenda* |
| *Urgent!!!* | *Action needed by Friday: contract signature* |

## À retenir

- Objet précis, salutation, raison de l'email, demande, clôture, signature.
- *Dear* + nom est toujours correct ; *Hi* avec les collègues proches.
- *Ms* par défaut pour une femme.
- *I am writing to…* pour ouvrir, *I look forward to hearing from you* pour conclure.

## Exercices

### Exercice 1 — Choisissez la formule

Quelle salutation et quelle formule finale pour : (a) une candidature à une entreprise dont vous ignorez le contact ; (b) un email à une cliente, Sarah Jones, que vous ne connaissez pas encore ; (c) un message à votre collègue Tom.

```solution-text
(a) Dear Sir or Madam, … Yours faithfully,
(b) Dear Ms Jones, … Kind regards, (ou Yours sincerely,)
(c) Hi Tom, … Thanks, / Best,
```

### Exercice 2 — Corrigez

Corrigez cet email : *Dear Mrs Jones, I write for confirm the meeting. I look forward to see you. Regards.*

```solution-text
Dear Ms Jones,
I am writing to confirm the meeting.
I look forward to seeing you.
Best regards,
[Prénom Nom]

→ « Ms » par défaut ; « I am writing to » + verbe ; « look forward to » + -ing ; formule finale suivie d'une virgule et de la signature.
```
"""

M2_L2 = r"""
## Demander poliment

En anglais professionnel, une demande trop directe paraît impolie. *Send me the report* sonne comme un ordre. On adoucit avec des **modaux** et des formules :

| Niveau | Formule |
|---|---|
| Neutre | *Could you send me the report, please?* |
| Plus poli | *Would you mind sending me the report?* (+ -ing) |
| Très formel | *I would be grateful if you could send me the report.* |
| Demander une permission | *Could I / May I ask you a question?* |

*Can you…?* est acceptable entre collègues, mais *Could you…?* est plus sûr dans un email.

## Répondre à une demande

```text
Of course. I'll send it to you this afternoon.
I'm afraid I can't attend the meeting on Monday. Would Tuesday suit you?
Unfortunately, the product is out of stock.
```

- *I'm afraid…* (« Je crains que… ») adoucit une mauvaise nouvelle.
- *Unfortunately,…* : malheureusement.
- *Would … suit you?* / *Would … work for you?* : propose une alternative.

## Relancer sans être insistant

```text
Hi David,

I'm just following up on my email of 4 November about the invoice.
Could you let me know when the payment will be made?

Thanks in advance,
Amina
```

Formules utiles :

- *I'm just following up on…* : « Je reviens vers vous au sujet de… ».
- *Just a quick reminder that…* : petit rappel.
- *I'm writing to check whether…* : pour vérifier si…
- *Could you give me an update on…?* : où en est…?

## Remercier et s'excuser

| Pour… | Formule |
|---|---|
| remercier | *Thank you for your quick reply.* / *Thanks for your help.* / *Many thanks.* |
| s'excuser d'un retard | *Sorry for the late reply.* / *Apologies for the delay.* |
| s'excuser formellement | *We apologise for any inconvenience.* |

*Thank you for* est suivi d'un nom ou d'un verbe en **-ing** : *Thank you for **sending** the documents.*

## À retenir

- *Could you…?*, *Would you mind + -ing?*, *I would be grateful if you could…*
- *I'm afraid* / *Unfortunately* pour annoncer un refus ou un problème.
- *I'm just following up on…* pour relancer.
- *Thank you for* + nom ou -ing.

## Exercices

### Exercice 1 — Rendez polies ces demandes

(a) *Send me the price list.* (b) *Call me tomorrow.* (c) *Change the date of the meeting.*

```solution-text
(a) Could you send me the price list, please?
(b) Would you mind calling me tomorrow?
(c) I would be grateful if you could change the date of the meeting.
(Plusieurs formules sont possibles : l'essentiel est d'éviter l'impératif seul.)
```

### Exercice 2 — Écrivez une relance

Vous avez envoyé un devis (*quote*) à M. Brown le 2 novembre, sans réponse. Écrivez une relance de trois phrases.

```solution-text
Dear Mr Brown,

I'm just following up on the quote I sent you on 2 November.
Could you let me know if you have any questions or if you need more information?

Kind regards,
[Prénom Nom]
```

### Exercice 3 — Refusez poliment

Un client propose une réunion lundi à 9 h ; vous êtes indisponible. Proposez mardi à 14 h.

```solution-text
I'm afraid I'm not available on Monday at 9 a.m. Would Tuesday at 2 p.m. suit you?
```
"""

M2_L3 = r"""
## Joindre un document

```text
Please find attached the contract.
I have attached the presentation from yesterday's meeting.
I'm sending you the file as a PDF.
```

*Please find attached…* est la formule la plus courante. Un oubli arrive à tout le monde : *Sorry, I forgot to attach the file. Here it is.*

## Fixer un rendez-vous

```text
Are you available on Thursday morning?
Would 3 p.m. on Friday work for you?
I can do Wednesday at 11. Does that suit you?
Let's say Monday at 10, then. I'll send you an invitation.
```

## Les dates et les heures

**Dates.** Le britannique écrit *14 November 2026* (lu « the fourteenth of November ») ; l'américain écrit *November 14, 2026* (lu « November fourteenth »). Attention à l'écriture numérique : *04/11/2026* signifie 4 novembre au Royaume-Uni mais **11 avril** aux États-Unis. Dans un email international, écrivez le mois **en lettres**.

**Heures.** Le système sur 12 heures domine à l'oral et à l'écrit courant : *9 a.m.* (matin), *3 p.m.* (après-midi). *Noon* = midi, *midnight* = minuit.

**Prépositions de temps** :

| Préposition | Usage | Exemples |
|---|---|---|
| *at* | une heure précise | at 10 a.m., at noon |
| *on* | un jour, une date | on Monday, on 14 November |
| *in* | un mois, une année, une partie de la journée | in May, in 2026, in the morning |

## Les faux amis du bureau

Certains mots anglais ressemblent au français mais n'ont **pas le même sens** :

| Anglais | Signifie | « Faux ami » français | En anglais |
|---|---|---|---|
| *actually* | en fait | actuellement | *currently* |
| *eventually* | finalement, au bout du compte | éventuellement | *possibly* |
| *to assist* | aider | assister (à une réunion) | *to attend* |
| *a library* | une bibliothèque | une librairie | *a bookshop* |
| *sensible* | raisonnable | sensible | *sensitive* |
| *to propose* | proposer (souvent : demander en mariage) | proposer une idée | *to suggest* |
| *a formation* | une formation… militaire ou géologique | une formation professionnelle | *training* |

> *I attended a training course* = « J'ai suivi une formation ». *I assisted the trainer* = « J'ai aidé le formateur ».

## À retenir

- *Please find attached…* pour une pièce jointe.
- *Are you available on…? / Would … work for you?* pour un rendez-vous.
- Mois en lettres dans les emails internationaux ; *at* une heure, *on* un jour, *in* un mois.
- Attention à *actually*, *eventually*, *assist*, *formation*.

## Exercices

### Exercice 1 — Prépositions

Complétez avec *at*, *on* ou *in* : (a) The meeting is ___ Tuesday ___ 2 p.m. (b) We launched the product ___ 2024. (c) I'm free ___ the afternoon. (d) The deadline is ___ 30 June.

```solution-text
(a) on Tuesday at 2 p.m.
(b) in 2024
(c) in the afternoon
(d) on 30 June
```

### Exercice 2 — Faux amis

Traduisez : (a) Actuellement, je travaille sur un nouveau projet. (b) J'ai assisté à la réunion. (c) Je cherche une formation en anglais.

```solution-text
(a) I'm currently working on a new project.   (et non « actually »)
(b) I attended the meeting.                    (et non « assisted »)
(c) I'm looking for an English training course. (et non « formation »)
```

### Exercice 3 — Email complet

Écrivez à Mme Lee pour lui envoyer le rapport mensuel en pièce jointe et lui proposer un appel jeudi à 15 h.

```solution-text
Subject: Monthly report and call on Thursday

Dear Ms Lee,

Please find attached the monthly report.
Would you be available for a short call on Thursday at 3 p.m. to discuss it?

I look forward to hearing from you.

Best regards,
[Prénom Nom]
```
"""

# ---------------------------------------------------------------------------
# Quiz : (kind, prompt, code, [options], [indices corrects], explication)
# ---------------------------------------------------------------------------
QUIZ_M1 = [
    ("single", "Quelle phrase est correcte pour indiquer votre métier ?", None,
     ["I'm engineer.", "I'm an engineer.", "I'm a engineer.", "I'm the engineer of."], [1],
     "L'article est obligatoire devant un métier, et « a » devient « an » devant un son voyelle : I'm an engineer."),
    ("single", "Vous rencontrez un client pour la première fois. Que dites-vous ?", None,
     ["Nice to meet you.", "Good night.", "See you soon.", "How do you do it?"], [0],
     "« Nice to meet you » (ou « Pleased to meet you ») se dit à la première rencontre. « Good night » signifie « bonne nuit »."),
    ("single", "Complétez : « I work ___ the marketing department. »", None,
     ["for", "at", "in", "on"], [2],
     "On travaille « in » un service ou un secteur (in marketing, in finance) et « for / at » une entreprise."),
    ("single", "Comment présenter votre collègue Karim à un client ?", None,
     ["He is Karim.", "This is Karim, my colleague.", "It's Karim my colleague.", "Here Karim."], [1],
     "On présente une personne avec « This is… »."),
    ("single", "Complétez : « She ___ the sales team. »", None,
     ["manage", "manages", "is manage", "managing"], [1],
     "Au présent simple, la 3e personne du singulier prend un -s : she manages."),
    ("single", "Quelle question est correcte ?", None,
     ["Does he works in London?", "Do he work in London?", "Does he work in London?", "Is he work in London?"], [2],
     "Avec he / she / it, la question se forme avec « does », suivi du verbe à la forme de base : Does he work…?"),
    ("single", "Où placer « always » ? « I ___ check ___ my emails ___ in the morning. »", None,
     ["Avant « check »", "Après « check »", "Après « emails »", "En fin de phrase"], [0],
     "Un adverbe de fréquence se place avant le verbe principal : I always check my emails in the morning."),
    ("multiple", "Quelles expressions permettent de décrire vos responsabilités ?", None,
     ["I'm in charge of the budget.", "I'm responsible for the budget.", "I'm charged the budget.", "I deal with the budget."], [0, 1, 3],
     "« in charge of », « responsible for » et « deal with » décrivent des responsabilités. « I'm charged the budget » n'a pas de sens."),
    ("single", "Comment lit-on 3,500 en anglais ?", None,
     ["three point five hundred", "three thousand five hundred", "three thousands five hundreds", "thirty-five thousand"], [1],
     "La virgule sépare les milliers : 3,500 = three thousand five hundred, sans -s à thousand et hundred."),
    ("true_false", "« One billion » signifie « un milliard ».", None,
     ["Vrai", "Faux"], [0],
     "En anglais actuel, billion = 1 000 000 000, soit un milliard. Le « billion » français vaut mille fois plus."),
]

QUIZ_M2 = [
    ("single", "Vous écrivez à une femme dont vous connaissez le nom, Sarah Jones. Quelle salutation choisir par défaut ?", None,
     ["Dear Mrs Jones,", "Dear Ms Jones,", "Dear Miss Jones,", "Dear Sarah Jones Madam,"], [1],
     "« Ms » est la forme neutre, indépendante de la situation familiale : c'est le choix par défaut."),
    ("single", "Quelle phrase est correcte ?", None,
     ["I look forward to hear from you.", "I look forward to hearing from you.", "I look forward hearing you.", "I look forward for hearing from you."], [1],
     "« look forward to » est suivi d'un verbe en -ing : I look forward to hearing from you."),
    ("single", "Quelle ouverture convient pour expliquer la raison d'un email ?", None,
     ["I write for asking…", "I am writing to ask…", "I am write to ask…", "I writing to ask…"], [1],
     "La formule standard est « I am writing to » + verbe."),
    ("single", "Quelle demande est la plus polie ?", None,
     ["Send me the file.", "You send me the file.", "Could you send me the file, please?", "I want the file."], [2],
     "« Could you…, please? » adoucit la demande. L'impératif seul paraît brusque en anglais professionnel."),
    ("single", "Complétez : « Would you mind ___ the meeting? »", None,
     ["to move", "move", "moving", "moved"], [2],
     "« Would you mind » est suivi d'un verbe en -ing : Would you mind moving the meeting?"),
    ("single", "Que signifie « I'm just following up on my email » ?", None,
     ["Je vais bientôt vous écrire.", "Je reviens vers vous au sujet de mon email.", "Je supprime mon email.", "Je transfère mon email."], [1],
     "« follow up on » sert à relancer poliment un message resté sans réponse."),
    ("single", "Comment annoncer poliment que vous ne pourrez pas venir ?", None,
     ["I'm afraid I can't attend the meeting.", "I don't come.", "No meeting for me.", "I am fear I can't come."], [0],
     "« I'm afraid… » (« je crains que… ») adoucit une réponse négative."),
    ("single", "Quelle phrase traduit « Actuellement, je travaille à Lyon » ?", None,
     ["Actually, I work in Lyon.", "Currently, I work in Lyon.", "Eventually, I work in Lyon.", "Actual, I work in Lyon."], [1],
     "« actually » signifie « en fait ». « Actuellement » se traduit par « currently » ou « at the moment »."),
    ("single", "Complétez : « The meeting is ___ Monday ___ 10 a.m. »", None,
     ["in … at", "on … at", "at … on", "on … in"], [1],
     "« on » devant un jour, « at » devant une heure précise."),
    ("multiple", "Quelles phrases annoncent correctement une pièce jointe ?", None,
     ["Please find attached the contract.", "I have attached the contract.", "Please find enclosed in attachment the contract joined.", "The contract is attached."], [0, 1, 3],
     "« Please find attached… », « I have attached… » et « … is attached » sont naturels. La troisième phrase est une traduction mot à mot incorrecte."),
]

MODULES = [
    {
        "position": 1,
        "title": "Se présenter et présenter son entreprise",
        "description": "Saluer, parler de son poste et de son entreprise, utiliser le présent simple.",
        "status": "published",
        "lessons": [
            ("se-presenter", "Saluer et se présenter",
             "Salutations formelles et informelles, « to be », métiers et présentations.", M1_L1, 25),
            ("son-poste", "Parler de son poste",
             "Présent simple, responsabilités et adverbes de fréquence.", M1_L2, 30),
            ("son-entreprise", "Présenter son entreprise",
             "Secteur, activité, taille, « there is / there are » et grands nombres.", M1_L3, 25),
        ],
        "quiz": ("Quiz — Se présenter et présenter son entreprise", QUIZ_M1),
    },
    {
        "position": 2,
        "title": "Les emails professionnels",
        "description": "Structurer un email, demander, relancer, remercier et éviter les faux amis.",
        "status": "published",
        "lessons": [
            ("structure-email", "La structure d'un email",
             "Objet, salutations, ouverture, clôture et formules finales.", M2_L1, 30),
            ("demander-relancer", "Demander, relancer, remercier",
             "Formules polies, refus diplomatiques et relances.", M2_L2, 30),
            ("pieces-jointes-rendez-vous", "Pièces jointes, rendez-vous et faux amis",
             "Dates, heures, prépositions de temps et pièges de traduction.", M2_L3, 30),
        ],
        "quiz": ("Quiz — Les emails professionnels", QUIZ_M2),
    },
    {
        "position": 3,
        "title": "Téléphone et visioconférence",
        "description": "Passer et recevoir un appel, prendre un message, gérer une visioconférence.",
        "status": "published",
        "lessons": [
            ("telephoner", "Passer et recevoir un appel",
             "Se présenter au téléphone, demander quelqu'un, faire patienter.", _m35.M3_L1, 25),
            ("prendre-un-message", "Prendre un message et épeler",
             "L'alphabet, épeler un nom ou une adresse email, noter un numéro.", _m35.M3_L2, 30),
            ("visioconference", "Réussir une visioconférence",
             "Problèmes techniques, prise de parole et demandes de répétition.", _m35.M3_L3, 25),
        ],
        "quiz": ("Quiz — Téléphone et visioconférence", _m35.QUIZ_M3),
    },
    {
        "position": 4,
        "title": "Participer à une réunion",
        "description": "Organiser une réunion, donner son avis, résumer et répartir les actions.",
        "status": "published",
        "lessons": [
            ("organiser-reunion", "Organiser une réunion",
             "Proposer un créneau, envoyer un ordre du jour, ouvrir la réunion.", _m35.M4_L1, 25),
            ("donner-son-avis", "Donner son avis",
             "Exprimer son opinion, être d'accord ou non avec diplomatie.", _m35.M4_L2, 30),
            ("conclure-reunion", "Conclure et répartir les actions",
             "Résumer, « will » et « going to », échéances et prochaines étapes.", _m35.M4_L3, 30),
        ],
        "quiz": ("Quiz — Participer à une réunion", _m35.QUIZ_M4),
    },
    {
        "position": 5,
        "title": "Rendre compte de son activité",
        "description": "Raconter au passé, présenter des chiffres, accueillir un visiteur et mini-projet.",
        "status": "published",
        "lessons": [
            ("parler-du-passe", "Raconter ce qui s'est passé",
             "Prétérit, verbes irréguliers courants et marqueurs de temps.", _m35.M5_L1, 30),
            ("presenter-des-chiffres", "Présenter des chiffres et des résultats",
             "Hausses, baisses, pourcentages et present perfect.", _m35.M5_L2, 30),
            ("accueil-mini-projet", "Accueillir un visiteur et mini-projet",
             "Small talk, puis une journée complète en anglais : email, appel, réunion.", _m35.M5_L3, 40),
        ],
        "quiz": ("Quiz — Rendre compte de son activité", _m35.QUIZ_M5),
    },
]
