# C7-Argyle, résultats : le contrôle d'interprétabilité arrête l'analyse

Préenregistré dans `resultats/c7-argyle-preenregistrement.md` **avant toute mesure
d'attaque** ; calculé par `analyses/c7_argyle.py` (graine 20260912, `.venv/bin/python`,
aucun appel réseau, aucune dépense). Sortie : `resultats/c7-argyle.csv`.
Étude de risque de vie privée sur un jeu déjà public (Argyle et al. 2023, Harvard
Dataverse `doi:10.7910/DVN/JPV20K`, **CC0 1.0**). Aucun identifiant ANES, aucun appariement
individuel n'est imprimé ni écrit.

**Verdict en une ligne : réplication IMPOSSIBLE sur ce jeu.** Les trois jumeaux GPT-3
publiés par l'équipe de BYU échouent au contrôle d'interprétabilité — ils ne réidentifient
pas mieux que la démographie seule. Conformément à la règle de décision n°1, l'analyse
s'arrête là et aucun contraste n'est interprété.

---

## 1. Appariement : confirmé, par lecture directe

`data/argyle-2023/anesgpt3_task3.csv`, 4 270 lignes, **12 items appariés sur la même ligne**,
donc la même personne. Identifiant réel : **`V160001_orig`** (identifiant de cas ANES 2016),
**unique sur les 4 270 lignes**.

| item | colonne **réelle** | colonne **jumelle** |
|---|---|---|
| gender | `V161342` | `gender_gpt3` |
| race | `V161310x` | `race_gpt3` |
| age | `V161267` | `age_gpt3` |
| education | `V161270` | `education_gpt3` |
| church_goer | `V161244` | `church_goer_gpt3` |
| patriotism | `V162125x` | `patriotism_gpt3` |
| discuss_politics | `V162174` | `discuss_politics_gpt3` |
| political_interest | `V162256` | `political_interest_gpt3` |
| ideology | `V161126` | `ideology_gpt3` |
| pid7 | `V161158x` | `pid7_gpt3` |
| voted_2016 | `V162031x` | `voted_2016_gpt3` |
| votechoice_2016 | `V162062x` | `votechoice_2016_gpt3` |

Les deux fichiers de robustesse en température portent la **même suite de `V160001_orig`,
dans le même ordre** (comparaison exacte des vecteurs) : trois jumeaux GPT-3 indépendants
des **mêmes** personnes. `V161155` (pid3) n'a pas de jumelle et est exclue.

Crosswalk vérifié dans le code de génération des auteurs
(`GPT3_OtherModels_DataGenerationCode.pdf` §1.10) : les clés du champ `vals` sont les codes
ANES et c'est cette clé qui est écrite dans la colonne `_gpt3`. Deux recodages explicites :
**education** (les 4 bandes des auteurs ; `strcompare` ne peut produire que 9/12/13/16) et
**votechoice** (ANES 3/4/5 → code 42 « someone else »).

**Bassin retenu** : les **2 148** personnes valides sur les 12 items (garde-fou de
`c7_reidentification.items_communs` : aucun motif de manquants ne peut servir d'empreinte).
À 4 % de l'ancre Twin (2 058) : **aucune extrapolation en taille de bassin**.

## 2. Les trois vagues demandées n'existent pas dans ce format

Le seul fichier à items multiples appariés (`anesgpt3_task3.csv`) est **exclusivement ANES
2016**. Les fichiers 2012/2016/2020 (`full_results_*_2.tab`, 5 914 / 4 270 / 5 441 lignes)
ne portent qu'**une** sortie GPT-3 : une paire de probabilités de vote ; toutes leurs autres
colonnes sont les **entrées** ANES de la mise en récit. **Un item par personne : l'attaque
n'y est pas définissable.** Substitut déclaré au préenregistrement : les **trois versions de
jumeaux** (température principale, 0,01, 1,0) des mêmes 2016, traitées séparément. Variation
de décodage, pas d'époque — ce n'est pas la réplication à trois vagues demandée.

## 3. Le confondu de format, identifié avant la mesure

`build_interview(..., human_readable_omit=X)` construit, pour chaque item X, un entretien
contenant les **onze vraies réponses de la personne** aux autres items, puis demande à
GPT-3 (`davinci`) la douzième. Chaque colonne `_gpt3` est donc une prédiction **réellement
tenue à l'écart** de sa cible — aucune tautologie — mais **conditionnée sur onze réponses
vraies**, là où nos jumeaux Twin et Park le sont sur un persona. Ce jumeau devrait donc être
**plus** fidèle que les nôtres, pas moins. Il l'est moins.

## 4. Contrôle d'interprétabilité : **ÉCHEC pour les trois jumeaux**

Règle reprise à l'identique de `c7_controle_interpretabilite` : IC bootstrap 95 %
(2 000 tirages, sur les personnes) du candidat **strictement au-dessus** de celui de la
baseline démographique. Garde-fou préservé : `controle_avant_interpretation` n'accepte
**aucun** argument de baseline — il reçoit le bassin et **recalcule la baseline sur ces
lignes-là**. Aucune constante reprise d'ailleurs.

| candidat (bassin = 2 148, 12 items) | top-1 | IC 95 % | verdict |
|---|---|---|---|
| GPT-3 davinci (temp. principale) | **0,14 %** | [0,05 ; 0,27] | **ÉCHEC** |
| GPT-3 davinci (temp. 0,01) | **0,11 %** | [0,04 ; 0,20] | **ÉCHEC** |
| GPT-3 davinci (temp. 1,0) | **0,09 %** | [0,02 ; 0,22] | **ÉCHEC** |
| **B-demo** (démographies seules, ce bassin) | 0,10 % | [0,02 ; 0,23] | baseline |
| hasard (1/2 148) | 0,047 % | — | — |

Les IC des trois jumeaux **chevauchent** celui de la baseline de leur propre bassin. Aucun
ne passe. **L'analyse s'arrête ici.** Les 20 tirages au bassin d'ancre N = 1 052 n'ont pas
été calculés : ils n'auraient interprété que du bruit.

**Sensibilité déclarée** (l'échec tient-il à l'âge, 73 modalités appariées à l'année
exacte ?) : **non**. Sans l'âge (11 items) : 0,08–0,13 %, échec. Sur les 8 items d'attitude
seuls : 0,09–0,11 %, échec. Le verdict ne dépend d'aucun choix d'items.

## 5. Pourquoi : le jumeau est moins exact que la modalité modale

Accord exact par item, jumeau contre humain, sur les 2 148 personnes :

| item | GPT-3 | B-demo | B-oracle | modale |
|---|---|---|---|---|
| gender | 48,6 % | 49,0 % | 54,6 % | 51,8 % |
| race | 80,7 % | 82,6 % | 82,6 % | 82,6 % |
| age (année exacte) | 1,8 % | 1,7 % | 1,6 % | 2,8 % |
| education (4 bandes) | 30,6 % | 28,3 % | 34,8 % | 33,0 % |
| church_goer | 52,7 % | 60,4 % | 65,0 % | 61,1 % |
| patriotism | 47,6 % | 55,4 % | 58,4 % | 56,8 % |
| discuss_politics | 83,2 % | 88,9 % | 88,9 % | 88,9 % |
| political_interest | 35,1 % | 48,5 % | 49,7 % | 51,5 % |
| ideology | 22,9 % | 21,7 % | 43,2 % | 23,7 % |
| pid7 | 29,3 % | 23,0 % | 44,6 % | 23,1 % |
| voted_2016 | 87,0 % | 100 % | 100 % | 100 % |
| votechoice_2016 | 47,3 % | 58,1 % | 84,1 % | 47,1 % |
| **moyenne** | **47,2 %** | **51,5 %** | **59,0 %** | — |

Le jumeau GPT-3 n'est au-dessus de la modale que sur **deux** items (`pid7`, `ideology`), et
sous la modale sur neuf. Sur l'âge il rajeunit systématiquement : **médiane 33 ans contre 53**
chez les humains, écart absolu médian **21 ans**, 7,3 % de prédictions à ±2 ans.

Ni B-demo ni B-oracle ne reçoivent jamais la vraie valeur d'un item sur lequel ils sont
notés (`_imputer_loo` retire l'item cible du contexte), exactement comme GPT-3 ne voyait
jamais la réponse demandée. Aucune tautologie des deux côtés.

## 6. Bits d'identité : il n'y a presque rien à transporter

Plafond d'identification log2(2 148) = **11,07 bits** ; entropie humaine des 12 items =
**21,30 bits**.

| candidat | bits [IC 95 %] | bits normalisés |
|---|---|---|
| GPT-3 (temp. 0,01), le meilleur des trois | **0,094** [0,074 ; 0,118] | **0,0044** |
| GPT-3 (temp. principale) | 0,047 [0,033 ; 0,066] | 0,0022 |
| GPT-3 (temp. 1,0) | 0,030 [0,020 ; 0,045] | 0,0014 |
| B-demo (démographies seules) | 0,014 [0,007 ; 0,026] | 0,0007 |
| **B-oracle** (mêmes 11 vraies réponses) | **0,342** [0,301 ; 0,389] | 0,0161 |

Pour mémoire (`c7-bits.csv`) : Twin JSON Persona GPT4.1 = 3,55 bits ; Twin *Demographics
Only* = 0,82 bit ; le plus faible prédicteur statistique de Twin (B2 argmax) = 0,079 bit.
**Le meilleur jumeau GPT-3 d'Argyle (0,094 bit) est au niveau du plus faible comparateur
statistique de Twin, et neuf fois sous le jumeau démographique de Twin.**

**B-oracle identifie 3,6 fois mieux que le meilleur jumeau GPT-3** (0,342 contre 0,094 bit ;
sans l'âge, top-1 0,38 % contre 0,13 %, IC disjoints). Un plus proche voisin classique
disposant exactement de la même information fait nettement mieux que GPT-3 davinci.

## 7. Confrontation à la prédiction préenregistrée

| grandeur | prédiction | observé | |
|---|---|---|---|
| top-1, bassin complet | 2,5 % — intervalle [1,0 ; 6,0] | **0,14 %** | hors intervalle, ×18 en dessous |
| bits normalisés | [0,020 ; 0,070] | **0,0044** | hors intervalle, ×4,5 en dessous |
| contrôle (B-demo) | passe nettement | **échoue, les trois** | attente démentie |
| B-oracle ≥ GPT-3 | attendu | **confirmé**, ×3,6 | attente vérifiée |

**Notre loi d'échelle n'est ni confirmée ni réfutée : elle n'est pas testable ici.** Elle
prédit la fuite d'un jumeau qui porte une personne ; le contrôle établit que ces jumeaux-là
n'en portent pas de démontrable. Compter un top-1 de 0,14 % comme une réfutation de la loi
serait commettre, à l'envers, l'erreur exacte que ce contrôle existe pour empêcher — conclure
d'une mesure prise sur du bruit. **Je ne peux pas distinguer « notre loi surestime la fuite à
faible nombre d'items effectifs » de « ce jumeau est au niveau du bruit », et je ne prétends
pas le faire.** Ce qui est tranché, en revanche, c'est que le jumeau est au niveau du bruit :
0,094 bit sur un plafond de 11,07, et une exactitude par item inférieure à la modale.

La prédiction en bits normalisés est **manquée du même coup**, et pour la même raison : la
conclusion P2 de `c7-bits-resultats.md` (« la mesure voyage, le taux non ») présuppose elle
aussi un jumeau qui transporte de l'information individuelle. Sur un jumeau qui n'en
transporte pas, le rapport bits/entropie n'a rien à faire voyager. **P2 n'est donc pas
réfutée ici non plus — elle est hors domaine.** Le dire autrement serait s'accorder une
victoire ou s'infliger une défaite qu'aucune de ces données ne permet.

## 8. Structure des items, pour mémoire

V de Cramér moyen = **0,1620** (55 paires) → **items effectifs = 4,31** pour 12 items bruts.
Pour comparaison : Twin 60 items → 10,13 ; Park/Stanford 177 → 9,05. Ce troisième jeu porte
**43 % de l'information effective de Twin**, et ses 12 questions ANES sont sensiblement plus
redondantes entre elles (V̄ 0,162 contre 0,083 et 0,106).

## 9. Limites et honnêteté envers les auteurs

- **Ce résultat ne contredit pas l'article d'Argyle et al.** Leur étude 3 est intitulée
  « Second Order Correlations » et sa Figure 4 compare des **matrices de V de Cramér** entre
  variables, c'est-à-dire la structure d'association de l'échantillon — pas l'exactitude
  individuelle. Un jumeau peut reproduire une structure de corrélations sans identifier
  personne. Nos mesures et les leurs ne portent pas sur la même quantité.
- **Un seul modèle, une seule époque.** GPT-3 `davinci`, requêté en 2022, `max_tokens` ≤ 5,
  réponse recodée par simple correspondance de préfixe (`strcompare`). C'est un jumeau de
  première génération ; rien ici ne se transporte aux jumeaux 2025-2026 de Twin ou de Park.
- **Le confondu de format joue contre nous, pas pour nous** (§3) : ces jumeaux disposaient de
  onze vraies réponses par prédiction, un avantage que nos jumeaux persona n'ont pas. Qu'ils
  échouent quand même rend le constat plus fort, pas plus faible.
- **Réserve de redistribution** : la clause propre à l'ANES pour les variables publiques
  utilisées n'a pas été vérifiée à la source (reprise de `chasse-jeux-apparies-2026-09-12.md`).
  Le jeu Dataverse lui-même est public et CC0. Rien n'est redistribué ici : `data/` n'est pas
  versionné.

## En clair

Le troisième jeu existe, il est bien apparié personne par personne, et nous avons pu
l'attaquer proprement. Mais les jumeaux GPT-3 qu'il contient ne reconnaissent pratiquement
personne : ils retrouvent la bonne personne dans 0,14 % des cas là où le hasard en donne
0,047 % et où la seule démographie en donne 0,10 % — et un simple appariement au plus proche
voisin, avec exactement les mêmes informations, fait trois fois mieux qu'eux. Ils sont même,
question par question, moins exacts que de répondre systématiquement la réponse la plus
fréquente. Il n'y a donc rien à répliquer ici : notre loi d'échelle ne peut pas être mise à
l'épreuve sur des jumeaux qui ne portent aucune personne. Ce n'est pas un échec de la chasse
— c'est un résultat en soi sur ce que valaient les jumeaux numériques de première
génération, et c'est exactement la situation que le contrôle préalable devait détecter avant
qu'on en tire des conclusions.
