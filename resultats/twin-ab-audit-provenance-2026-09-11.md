# Tournoi A vers B sur Twin-2K-500 : audit de provenance et comptes de faisabilité

Rapport du 11 septembre 2026. Il fait les deux vérifications que `resultats/prochaine-validation-externe-2026-09-11.md`, section « Ce que je n'ai pas pu vérifier », déclare non faites : la provenance des treize configurations (a-t-on pu voir une réponse humaine de vague 4 autrement que par l'historique de retest des vagues 1 à 3 ?) et les dénombrements de structure qui disent si trois blocs B de 36 items sont constructibles.

Lecture seule sur `data/`, aucun appel réseau, aucun appel de modèle, aucun script existant modifié. Les comptes ont été faits par des scripts jetables hors dépôt, qui importent `analyses/i3b_twin.charger_twin_commun` tel quel pour les matrices de codes. **Aucune exactitude, perte, chute ou corrélation n'est calculée ici.** Les seules comparaisons de valeurs entre fichiers servent à identifier la source d'un objet (vague 1 à 3 ou vague 4), jamais à noter une configuration.

Étiquettes : [MESURE] compté sur les fichiers locaux ; [CONFIRMÉ] lu dans un fichier du paquet ou du dossier ; [INFÉRÉ] déduit de la structure, sans document qui le dise ; [NON VÉRIFIABLE] hors de portée des fichiers locaux.

---

## 1. Réponse courte

1. **Trois configurations sur treize sont à exclure** : les deux `JSON Persona (Predicted Output)`, par la règle de masque déjà écrite dans le document de référence et parce que le contenu passé comme « sortie prédite » est inconnu, et `LLM Finetuning (500 training samples)`, dont les poids ont été ajustés sur des réponses humaines dont la vague et les items ne sont pas documentés localement.
2. **Deux sont suspectes** : `Persona Summary` et `Persona Summary - JSON Persona`. Le seul champ `persona_summary` que décrit le README est rangé dans le dossier `full_persona`, où les réponses de vague 4 remplacent celles des vagues 1 à 3 pour les questions répétées. Le paquet `wave_split` ne contient aucun résumé.
3. **Huit sont admissibles sous réserve** : aucune invite n'est observable localement, mais l'objet de contexte que le README désigne pour l'évaluation, `wave1_3_persona_*`, ne contient aucun des 75 QID répétés sur les 294 personnes présentes localement.
4. **Une partition en trois blocs de 36 items existe arithmétiquement**, mais « stratifiée par famille » est presque vide de sens : 26 familles sur 33 ont un seul item, une famille en a 40. Et on ne peut pas à la fois stratifier par famille et par type de réponse et garder entiers les QID matrice et les expériences inter sujets.
5. **Aucun item ne disparaît à l'intersection des masques**, quel que soit l'ensemble retenu. Ce qui se contracte, ce sont les personnes : 2 058, 1 558, 1 000 ou 500 selon qu'on garde `JSON Persona - GPT4.1-mini` et `Finetuning`.

---

## 2. Audit de provenance

### 2.1 Ce que contient localement le paquet

- **Les treize fichiers de sortie existent en double, sans quatorzième configuration.** Empreintes MD5 [MESURE] : chaque `llm/spec_*.csv` est identique octet pour octet à un fichier de `llm_specs/`. `llm/default_gpt41mini_llm.csv` est `Text Persona - GPT4.1-mini`, `llm/default_gpt41mini_wave4.csv` est `humains_wave4.csv`, `llm/demo_only_gpt41mini_llm.csv` est `Demographics Only`. Les alias du dossier se lisent `predout` = *Predicted Output*, `finetune500` = *LLM Finetuning (500 training samples)*, `resume` = *Persona Summary*, `texte_repetition` = *Repeating Questions*. La correspondance nom distant vers nom local est dans `analyses/a8_telecharger_twin_llm.py` : chaque fichier est le `responses_llm_imputed_formatted.csv` du dossier de spécification Hugging Face du même nom [CONFIRMÉ].
- **Aucune invite, aucun message système, aucun fichier d'entraînement.** Ni `llm/` ni `llm_specs/` ne contiennent autre chose que les réponses formatées [MESURE].
- **Le dossier `full_persona` est absent localement.** Le seul objet de contexte présent est `wave_persona_chunk_001.parquet`, configuration `wave_split`, **294 personnes sur 2 058** (pid 2 à 2 056), colonnes `pid`, `wave1_3_persona_text`, `wave1_3_persona_json`, `wave4_Q_wave1_3_A`, `wave4_Q_wave4_A` [MESURE].
- **Le README décrit deux familles d'objets persona en amont** [CONFIRMÉ, `data/twin2k500/README.md`] : `full_persona`, dont `persona_text` et `persona_json` utilisent les réponses de vague 4 pour les questions posées dans les deux périodes, et qui porte aussi `persona_summary` ; `wave_split`, désigné pour « testing and evaluating different LLM persona creation methodologies ».

### 2.2 Vérifications faites sur les objets locaux

1. **Le persona des vagues 1 à 3 ne contient aucun item répété**, et donc ni la réponse de vague 4 ni même la réponse antérieure. Sur les 294 personnes, `wave1_3_persona_json` contient **0** question dont le QID fait partie des 75 QID des 108 items, et **0** question d'une des 33 familles de vague 4. Ses blocs sont `Cognitive tests`, `Demographics`, `Economic preferences`, `Economic preferences - intro`, `Forward Flow`, `Personality`. Dans `wave1_3_persona_text`, **0** personne sur 294 ne cite un nom de famille de vague 4 [MESURE]. `a2-baselines.md` avait fait le même constat sur 25 personas ; il est étendu ici à tout le fragment local.
2. **Les deux objets de vague 4 portent bien la source que leur nom annonce.** Sur les 294 personnes, pour les items MC répétés où la réponse des vagues 1 à 3 diffère de celle de la vague 4, **3 448 cellules** : `wave4_Q_wave1_3_A` égale la valeur des vagues 1 à 3 dans 3 448 cas et celle de la vague 4 dans 0 ; `wave4_Q_wave4_A` égale la vague 4 dans 3 448 cas et les vagues 1 à 3 dans 0. Les 12 134 autres cellules ne discriminent pas [MESURE]. **L'historique de retest autorisé existe donc localement sous une forme propre, `wave4_Q_wave1_3_A`, distincte du persona.**
3. **Les fichiers de sortie sont construits sur le gabarit humain de vague 4.** Pour les treize, les colonnes `StartDate`, `EndDate`, `Duration (in seconds)` et `RecordedDate` sont identiques ligne à ligne à celles de `humains_wave4.csv`, de même que les treize colonnes d'ordre de randomisation (`base_rate`, `Allais`, `matching`, ...) [MESURE]. Cela ne prouve pas une fuite : l'affectation aux bras inter sujets est **la même aux vagues 1 à 3 et à la vague 4**, le statut vide ou renseigné des 108 items diffère sur **0** cellule entre les deux fichiers humains [MESURE]. L'information « quel bras cette personne a vu » n'est donc pas propre à la vague 4.
4. **Aucune configuration ne répond hors du bras vu par la personne.** Pour les trois fichiers dont le masque diffère du masque humain, les écarts vont tous dans le même sens : cellule humaine renseignée, cellule du modèle vide. **0** cellule remplie par le modèle là où l'humain de vague 4 n'a pas vu la question [MESURE].

### 2.3 Périmètres et masques, par configuration

[MESURE, reproduit à l'identique `t1-controles.csv` et `i3b-twin-controles.csv`]

| configuration | personnes | pid absents | cellules perdues où l'humain de v4 répond |
|---|---|---|---|
| dix configurations | 2 058 | aucun | 0 |
| `JSON Persona - GPT4.1-mini` | 1 000 | **1 001 à 2 058** | 153, **0,187 %** |
| `LLM Finetuning (500 training samples) - GPT4.1-mini` | 1 558 | **exactement 1 à 500** | 0 |
| `JSON Persona (Predicted Output) - GPT4.1` | 2 050 | 443, 1 399, 1 411, 1 472, 1 489, 1 504, 1 512, 1 519 | 854, **0,508 %** |
| `JSON Persona (Predicted Output) - GPT4.1-mini` | 2 058 | aucun | 16 738, **9,918 %** |

**Où tombent les pertes.**
- `PredOut mini`, 91 items touchés sur 108. Les plus atteints : `Q159_1` à `Q159_3` (*Linda -no conjunction*) 56,07 %, `Q160_1` à `Q160_3` (*Linda-conjunction*) 31,88 %, `Denominator neglect` 30,61 %, prix 33 à 40 environ 17 %. Par famille : prix 10 131 cellules, heuristiques non expérimentales 2 074, Linda sans conjonction 1 731, Linda conjonction 984, appariement de probabilités P1 930, P2 402.
- `PredOut 4.1`, 44 items touchés. Les plus atteints : `Q161` (*Outcome bias - success*) 6,21 %, `Q162` (*failure*) 2,49 %, prix 1 à 9 à 0,93 %.
- `JSON Persona mini`, 153 cellules : prix 100, Linda conjonction 33, *Outcome bias* 13, divers 7.

**Anomalie propre à `PredOut mini`** : son fichier a **181 colonnes contre 168** pour les douze autres et pour le gabarit humain. Les treize colonnes en plus sont `QID183_TEXT` et `QID194_1` à `QID194_12`, renseignées sur une à trois lignes seulement. Au catalogue, `QID183` est *Absolute vs. relative - calculator* et `QID194` *Myside Ford*, deux questions MC sans sous colonnes. Le tableau des QID dupliqués du catalogue (`QID268` à `QID279`) ne les explique pas [MESURE, CONFIRMÉ]. Il y a eu une sortie mal structurée pour quelques personnes. Rien ne dit localement pourquoi.

**Structure des périmètres** [MESURE] : les 500 personnes absentes de `Finetuning` (pid 1 à 500) sont toutes incluses dans les 1 000 de `JSON Persona mini` (pid 1 à 1 000). L'intersection des deux vaut donc **exactement 500 personnes, pid 501 à 1 000**.

### 2.4 Classement des treize configurations

Réserves communes :
- **R1** : l'invite réellement envoyée n'est pas observable localement.
- **R2** : deux objets persona existent en amont, `wave_split`, vérifié propre sur 294 personnes, et `full_persona`, qui contient les réponses de vague 4 aux questions répétées. Le fichier de sortie ne dit pas lequel a servi. Le README désigne `wave_split` pour l'évaluation.
- **R3** : le sens exact de la variante n'est pas documenté localement.

| # | configuration | fichier `llm_specs/` | pers. | masque | classement | motif |
|---|---|---|---|---|---|---|
| 1 | Demographics Only - GPT4.1-mini | `demographics_only__gpt41_mini.csv` | 2 058 | passe | **ADMISSIBLE** sous R1 | Aucune question de vague 4 n'appartient au bloc Demographics (`a6` §1.4 point 3). Ensemble d'information distinct des configurations riches. |
| 2 | JSON Persona (Predicted Output) - GPT4.1 | `json_persona_predicted_output__gpt41.csv` | 2 050 | **échoue**, 0,508 % | **À EXCLURE** | Masque : règle du document de référence, écart E4 de `i3b`. Provenance **SUSPECTE** : le contenu passé comme sortie prédite est inconnu (voir ci-dessous). |
| 3 | JSON Persona (Predicted Output) - GPT4.1-mini | `json_persona_predicted_output__gpt41_mini.csv` | 2 058 | **échoue**, 9,918 % | **À EXCLURE** | Masque, 13 colonnes hors gabarit. Provenance **SUSPECTE**, même motif que 2. |
| 4 | JSON Persona - GPT4.1 | `json_persona__gpt41.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2 | |
| 5 | JSON Persona - GPT4.1-mini | `json_persona__gpt41_mini.csv` | 1 000 | passe, 0,187 % | **ADMISSIBLE** sous R1, R2 | Pas de motif de fuite. Contrainte de périmètre : pid 1 à 1 000 seulement. |
| 6 | LLM Finetuning (500 training samples) - GPT4.1-mini | `llm_finetuning_500_training_samples__gpt41_mini.csv` | 1 558 | passe | **À EXCLURE** | Exposition par entraînement : poids ajustés sur des réponses humaines de 500 personnes, dont on infère qu'elles sont les pid 1 à 500 [INFÉRÉ]. Cible, vague et items non documentés. Dans le meilleur cas, ce sont les réponses d'autres personnes aux mêmes items B. Dans le cas le plus naturel pour un dossier « LLM simulation results » noté contre la vague 4, ce sont leurs réponses de vague 4. Ce n'est pas l'historique de retest de la personne prédite. |
| 7 | Persona Summary - GPT4.1-mini | `persona_summary__gpt41_mini.csv` | 2 058 | passe | **SUSPECTE** | Le seul `persona_summary` documenté est dans `full_persona`, dont le texte source porte les réponses de vague 4 aux questions répétées. `wave_split` n'a aucun résumé. Le README ne dit pas à partir de quel texte le résumé est produit. |
| 8 | Persona Summary - JSON Persona - GPT4.1-mini | `persona_summary__json_persona__gpt41_mini.csv` | 2 058 | passe | **SUSPECTE** | Même motif que 7, plus R2 pour la partie JSON. |
| 9 | Text Persona (Default Temperature) - GPT4.1-mini | `text_persona_default_temperature__gpt41_mini.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2 | |
| 10 | Text Persona (Reasoning) - GPT4.1-mini | `text_persona_reasoning__gpt41_mini.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2 | |
| 11 | Text Persona (Repeating Questions) - GPT4.1-mini | `text_persona_repeating_questions__gpt41_mini.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2, R3 | Si « repeating questions » signifie que les questions de vague 4 ont été présentées avec les réponses des vagues 1 à 3, c'est l'historique de retest autorisé. Mais c'est alors un ensemble d'information plus riche que celui des autres configurations, dont le persona ne contient aucun item répété (2.2 point 1). |
| 12 | Text Persona - GPT4.1-mini | `text_persona__gpt41_mini.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2 | Aussi `llm/default_gpt41mini_llm.csv`. |
| 13 | Text Persona - Gemini-Flash2.5 | `text_persona__gemini_flash25.csv` | 2 058 | passe | **ADMISSIBLE** sous R1, R2 | |

**Bilan** : 8 admissibles sous réserve, 2 suspectes, 3 à exclure. Parmi les 8 admissibles, **7 configurations riches** (4, 5, 9 à 13) et **1 seule configuration à démographies seules** (1).

**Sur « Predicted Output ».** D'après la documentation publique d'OpenAI, non consultée pour ce rapport faute d'accès réseau, *Predicted Outputs* est une option d'accélération du décodage où l'appelant fournit un texte attendu. Deux lectures sont compatibles avec les fichiers locaux :
- le texte attendu est la structure JSON des questions sans réponse, et il n'y a pas de fuite ;
- il est construit à partir d'un JSON portant les réponses, par exemple `wave4_Q_wave4_A`, et la fuite est directe.

Rien dans le paquet local ne tranche. Indice faible, lu et non recalculé : `t1-mesure-de-personne-twin.md` publie pour ces deux sorties une exactitude de 0,4625 et 0,5646, sous `JSON Persona - GPT4.1` à 0,5738. C'est peu compatible avec une copie systématique de la réponse de vague 4, et compatible avec une contamination partielle. Ce n'est pas une preuve.

**Sur R2.** Même indice faible et même source : aucune configuration riche ne dépasse 0,5738 d'exactitude, contre 0,7119 pour le retest humain. C'est peu compatible avec un persona `full_persona` contenant la réponse de vague 4 à chaque item cible. Ce n'est pas non plus une preuve.

---

## 3. Comptes de faisabilité

### 3.1 Les 108 items

[MESURE, `question_catalog.json` et `wave4_formatted_to_catalog_mapping.json`]

- Le mapping compte 126 colonnes de questions : MC 68, Matrix 40, Slider 12, TE 6. **Les 108 items catégoriels sont les 68 MC et les 40 lignes de Matrix**, portés par **75 QID distincts**.
- **Type de réponse** : MC `SAVR` 53, MC `SAHR` 15, Matrix `Likert/SingleAnswer` 40. Nombre d'options des MC : 2 options pour 49 items, 4 pour 1, 5 pour 6, 6 pour 7, 7 pour 2, 10 pour 3.
- **Sept QID matrice** portent les 40 lignes : `QID287` 10 (*False consensus*), `QID198` 10 (*Probability matching P1*), `QID203` 6 (*P2*), `QID288` 4 et `QID289` 4 (*Non-experimental heuristics and biases*), `QID159` 3 (*Linda -no conjunction*), `QID160` 3 (*Linda-conjunction*).

**Familles (`BlockName`) : 33, dont 26 à un seul item.**

| famille | items | type | renseignement humain v4 |
|---|---|---|---|
| Product Preferences - Pricing | **40** | MC, 40 QID | 100 % |
| False consensus | 10 | Matrix, un QID | 100 % |
| Non-experimental heuristics and biases | 10 | 8 Matrix + 2 MC | 100 % |
| Probability matching vs. maximizing - Problem 1 | 10 | Matrix, un QID | 50,1 % |
| Probability matching vs. maximizing - Problem 2 | 6 | Matrix, un QID | 49,9 % |
| Linda-conjunction | 3 | Matrix, un QID | 50,0 % |
| Linda -no conjunction | 3 | Matrix, un QID | 50,0 % |
| 26 familles à un item | 26 | MC | 31,6 à 51,3 % |

**Structure inter sujets** [MESURE, masques de `wave4_response.csv`] : **60 items complets** (prix 40, False consensus 10, heuristiques non expérimentales 10) et **48 items partiels** répartis en **11 expériences** à bras mutuellement exclusifs, dont l'union couvre toujours 100 % des personnes.

| expérience | bras (items, effectif humain) |
|---|---|
| Disease | loss (1, 1 055) / gain (1, 1 003) |
| Linda | conjunction (3, 1 029) / no conjunction (3, 1 029) |
| Outcome bias | failure (1, 1 006) / success (1, 1 052) |
| Anchoring African | low (1, 1 002) / high (1, 1 056) |
| Anchoring redwood | low (1, 1 049) / high (1, 1 009) |
| Less is More + Proportion dominance | A (3, 735) / B (3, 672) / C (3, 651) |
| Absolute vs. relative | calculator (1, 1 031) / jacket (1, 1 027) |
| WTA/WTP Thaler | WTP certainty (1, 712) / WTA certainty (1, 673) / WTP noncertainty (1, 673) |
| Allais | Form 1 (1, 1 051) / Form 2 (1, 1 007) |
| Myside | Ford (1, 1 015) / German (1, 1 043) |
| Probability matching | Problem 1 (10, 1 032) / Problem 2 (6, 1 026) |

Chaque personne a donc **84 cellules** renseignées (1 032 personnes, bras P1) ou **80** (1 026 personnes, bras P2), soit 168 768 cellules sur 222 264, et 24,07 % de vides [MESURE].

### 3.2 Intersection des masques

Cellules où l'humain de vague 4 répond **et** où toutes les configurations de l'ensemble répondent [MESURE].

| ensemble | configs | personnes | cellules | couverture par item, min / médiane / max | items perdus |
|---|---|---|---|---|---|
| les treize | 13 | **500** (pid 501-1000) | 36 194 | **104** / 399 / 500 | 0 |
| sans les deux PredOut | 11 | 500 | 40 906 | 159 / 497 / 500 | 0 |
| **les 8 admissibles** (= sans PredOut ni Finetuning ; les deux Summary ne perdent aucune cellule) | 8 à 10 | **1 000** (pid 1-1000) | **81 879** | 311 / 997 / 1 000 | 0 |
| les 7 admissibles sans JSON Persona mini | 7 à 9 | **2 058** | **168 768** | 651 / 2 058 / 2 058 | 0 |
| sans PredOut ni JSON mini, Finetuning gardé | 10 | 1 558 (pid 501-2058) | 127 780 | 502 / 1 558 / 1 558 | 0 |

**Aucun item ne disparaît dans aucun ensemble.** Le plus bas est `Q159_1` à `Q159_3` : 104 personnes quand les treize sont gardées, ce qui vient de `PredOut mini`. Sur le périmètre des 8 admissibles, les 153 cellules perdues par `JSON Persona mini` sont les seules pertes : l'humain a 82 032 cellules sur les pid 1 à 1 000.

### 3.3 Existence d'une partition en trois blocs de 36

Bornes « plancher / plafond » d'une stratification exacte par bloc : 22 à 23 MC et 13 à 14 Matrix, et pour chaque famille de `n` items, `floor(n/3)` à `ceil(n/3)` items. Deux jeux de contraintes ont été testés par recherche constructive. **Les solutions trouvées sont des témoins d'existence, pas des propositions.**

- **S1, stratification famille et type au sens plancher / plafond, blocs de 36** : **réalisable**, témoin trouvé au premier essai. Mais ce témoin **coupe les 7 QID matrice sur 7** entre blocs et **répartit les bras de 10 expériences inter sujets sur 11** dans des blocs différents. Pour les 26 familles à un item, la contrainte est vide : chacune tombe entière dans un seul bloc.
- **S2, QID matrice entier et expérience inter sujets entière (56 unités indivisibles), blocs de 36** : **réalisable en taille**, mais **incompatible avec la stratification par type**. La meilleure répartition possible des 40 lignes Matrix est **16 / 14 / 10**, parce que l'expérience *Probability matching* forme à elle seule une unité de 16 lignes. La borne 13 à 14 est inatteignable. Le témoin S2 viole la borne plancher / plafond sur 17 couples famille × bloc, avec des prix répartis 13 / 13 / 14.

**Ce qui est incompatible par construction** [MESURE] : *False consensus*, *Probability matching P1*, *P2*, *Linda-conjunction* et *Linda -no conjunction* sont chacune un seul QID matrice. Les stratifier par famille oblige à couper la matrice. La garder entière oblige à renoncer à la stratification de cette famille.

### 3.4 Couverture de chaque bloc, sur les deux témoins

Format : cellules disponibles / couverture minimale d'un item / cellules minimales d'une personne / personnes à moins de 10 cellules [MESURE].

| périmètre | témoin | B1 | B2 | B3 |
|---|---|---|---|---|
| 7 admissibles, 2 058 | S1 | 56 592 / 651 / 25 / 0 | 55 941 / 651 / 24 / 0 | 56 235 / 651 / 24 / 0 |
| 7 admissibles, 2 058 | S2 | 63 798 / 673 / 31 / 0 | 53 508 / 651 / 26 / 0 | 51 462 / 1 002 / 23 / 0 |
| 8 admissibles, 1 000 | S1 | 27 427 / 311 / 12 / 0 | 27 108 / 311 / 13 / 0 | 27 344 / 311 / 14 / 0 |
| 8 admissibles, 1 000 | S2 | 30 955 / 319 / 17 / 0 | 25 928 / 311 / 13 / 0 | 24 996 / 472 / 9 / 1 |
| avec Finetuning, 1 558 | S1 | 42 875 / 502 / 25 / 0 | 42 347 / 502 / 24 / 0 | 42 558 / 502 / 24 / 0 |
| 11 configs, 500 | S1 | 13 715 / 162 / 12 / 0 | 13 520 / 159 / 13 / 0 | 13 671 / 162 / 14 / 0 |
| 13 configs, 500 | S1 | 11 973 / 104 / 4 / 26 | 12 117 / 104 / 5 / 24 | 12 104 / 104 / 5 / 27 |
| 13 configs, 500 | S2 | 14 252 / 148 / 11 / 0 | 10 905 / 104 / 4 / 37 | 11 037 / 216 / 1 / 40 |

Le document de référence annonce « environ 74 000 réponses potentielles » par bloc B. C'est le rectangle 36 × 2 058 = 74 088. **Les cellules humaines réellement renseignées sont d'environ 56 000 par bloc** sur 2 058 personnes (témoin S1), à cause des 24,07 % de vides inter sujets. **Aucun seuil de couverture n'est déclaré** dans le document de référence (« selon un seuil fixé avant lecture ») : ce rapport ne dit donc pas si ces nombres suffisent.

### 3.5 Taille des cellules de `S_gra` sur chaque périmètre

Le diagnostic prévu est la chute sous permutation intra `S_gra`, genre × ethnicité × âge, règle de `t1_commun.segmentations` [MESURE].

| périmètre | cellules occupées | singletons | cellules < 5 (personnes) | cellules < 10 | médiane | max |
|---|---|---|---|---|---|---|
| 2 058 | 40 | 1 | 5 (12) | 6 | 23 | 259 |
| 1 558 (pid 501-2058) | 40 | 2 | 6 (14) | 9 | 19 | 185 |
| 1 000 (pid 1-1000) | 39 | 2 | 8 (21) | 16 | 13 | 145 |
| 500 (pid 501-1000) | 39 | 4 | 14 (30) | 25 | 7 | 61 |

Une personne seule dans sa cellule ne peut pas être permutée. Sur le périmètre de 500 personnes, 25 cellules sur 39 ont moins de 10 personnes.

---

## 4. Ce que les rapports et CSV `t1` et `i3b` contraignent déjà

1. **Les deux sorties dont le contrôle de masque échoue sont identifiées sans ambiguïté** : `JSON Persona (Predicted Output) - GPT4.1-mini`, **0,09917756920743269** de cellules perdues, et `JSON Persona (Predicted Output) - GPT4.1`, **0,005079946702198535**, pour un seuil de 0,005. Sources : `t1-controles.csv` lignes « masque, ... », `i3b-twin-controles.csv` (0,099178 et 0,00508), écart E4 de `i3b-abaque-et-borne.md`, constante `MASQUE_DOUTEUX` de `analyses/t1_commun.py` lignes 105 à 107, colonne `masque_douteux` de `t1-classement.csv`. Recalculées ici, 9,9178 % et 0,5080 % [MESURE].
2. **Aucun item n'est écarté par `t1`** : les 108 items sont gardés (`paq["garder"]` vaut vrai partout). Les 18 colonnes Slider et TE sont écartées en amont par `a6.charger_twin`.
3. **Quatre segmentations déclarées au préenregistrement `t1`** : `S_ideo` (5 cellules), `S_fin` (24), `S_gra` (40, segmentation du verdict), `S_parti` (4). Le contrôle 5 de `t1` signale déjà un repli du générateur nul de **32,96 %** pour `JSON Persona - GPT4.1-mini` sous `S_gra`, au dessus du seuil de 30 %. La permutation n'emploie pas le nul (voir 3.5 pour les tailles de cellules).
4. **Les prédicteurs statistiques de `t1` apprennent sur des réponses de vague 4 d'autres personnes.** Dans `analyses/t1_baselines.py`, la cible est `y = paq["codes"][C.REF]`, c'est-à-dire les humains de vague 4, apprise en validation croisée à 5 plis sur les personnes (`KFold`, graine 20260909). `B0 mode`, `B0 tirage`, `B1 argmax`, `B2 argmax` et `PMM k=10` sont ajustés, item par item, sur les réponses de vague 4 des quatre plis d'entraînement, **y compris pour les items qui seraient en B**. Leurs entrées sont les 14 démographies (`B1`, dont `QID22` et `QID20`), les 494 items de contexte non répétés des vagues 1 à 3 (`B2`), ou les deux (`PMM`). C'est le même type d'exposition que celui qui motive l'exclusion de `Finetuning`, réponses d'autres personnes aux items cibles. Le fait est rapporté, pas jugé.
5. **La version résidualisée de `t1-correlation-residus.csv` est ajustée sur 16 conditions**, les 13 configurations plus `B1`, `B2` et `PMM`. Sur les seules configurations admissibles, la régression aurait 8 points, ou 7 sans `JSON Persona mini`.
6. **`QID290` n'est pas un des 108 items.** Au catalogue c'est un Slider du bloc *Non-experimental heuristics and biases* (10 énoncés « False cons. others »), écarté comme les autres curseurs. **`QID287` est une matrice de 10 lignes comprise dans les 108.** Le geler hors du tournoi laisse **98** items, ce qui n'est pas compatible avec trois blocs de 36.
7. **Périmètres** : `t1` recalcule le plancher humain sur chaque périmètre et interdit de comparer des valeurs absolues entre périmètres (préenregistrement `t1` §3). Les ensembles de 3.2 ont des périmètres de 2 058, 1 558, 1 000 ou 500 personnes.
8. **Sous tournoi « démographies seules »** : parmi les configurations admissibles, il n'y en a qu'une, `Demographics Only - GPT4.1-mini`.

---

## 5. Ce que je n'ai pas pu vérifier

1. **Aucune invite n'a été lue.** Le paquet local ne contient ni message système, ni gabarit d'invite, ni code de génération. Le README renvoie au dépôt GitHub `tianyipeng-lab/Digital-Twin-Simulation` et à sa documentation, non consultés faute d'accès réseau. **Tout le classement « admissible » repose sur des noms de configuration, sur le README et sur l'examen de l'objet de contexte, pas sur l'entrée réellement envoyée.**
2. **Quel objet persona a servi à chaque configuration.** `full_persona`, qui contient les réponses de vague 4 aux questions répétées, est absent localement. Je n'ai pas pu établir qu'aucune configuration ne l'a employé.
3. **La propreté du persona `wave_split` est vérifiée sur 294 personnes sur 2 058** : les autres fragments du parquet ne sont pas dans `data/`. Pour les 1 764 autres personnes, elle est supposée.
4. **Le contenu passé comme « sortie prédite »** aux deux configurations `Predicted Output` n'est pas documenté localement, et ce que fait l'option n'a pas été relu dans la documentation d'OpenAI.
5. **Le protocole d'affinage de `Finetuning`** : cible (vague 4 ou vagues 1 à 3), items, format, époques. L'identité des 500 personnes d'entraînement (pid 1 à 500) est **inférée** de leur absence exacte du fichier de sortie, et `a6` l'avait déjà inférée ainsi. Aucun document local ne l'établit.
6. **Le contenu des résumés `Persona Summary`** et le texte à partir duquel ils ont été produits.
7. **Le sens de « Repeating Questions », « Reasoning » et « Default Temperature »** au delà de leur nom.
8. **L'origine des 13 colonnes hors gabarit de `PredOut mini`**, des 8 personnes absentes de `PredOut 4.1`, et du choix des pid 1 à 1 000 pour `JSON Persona mini`.
9. **La mémorisation par pré entraînement.** Twin-2K-500 est public depuis mai 2025 et `exploration/05-datasets-publics.md` classe ce risque « moyen à élevé ». Je n'ai pas vérifié les dates de génération des sorties par rapport aux coupures des modèles, et ce risque, s'il existe, ne se voit pas dans les fichiers.
10. **La notion de « stratifié » n'est pas définie** par le document de référence : ni tolérance par bloc, ni règle sur les lignes de matrice, ni règle sur les bras inter sujets. S1 et S2 sont deux formalisations que j'ai choisies pour rendre la question dénombrable. D'autres sont possibles, par exemple regrouper les 26 familles singletons en catégories plus larges, et elles n'ont pas été testées.
11. **Les témoins S1 et S2 viennent d'une recherche constructive, pas d'une optimisation exhaustive.** Seul l'optimum de répartition des lignes Matrix sous S2 (16 / 14 / 10) est exhaustif, sur les 3^5 affectations des cinq unités matricielles. Les couvertures du tableau 3.4 sont celles des témoins, pas des bornes sur toutes les partitions possibles.
12. **Les scripts de comptage ne sont pas versionnés** : ils ont été écrits hors dépôt comme l'exigeait la consigne. Les règles de comptage sont décrites ici pour être refaites. Les chargements passent par `i3b_twin.charger_twin_commun`, et les pertes de masque reproduisent au chiffre `t1-controles.csv`.
