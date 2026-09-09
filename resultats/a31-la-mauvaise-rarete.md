# a31. Pourquoi la bonne personne recoit elle la mauvaise rarete ?

> **Erratum du 9 septembre 2026, sur un point qui n'est pas couvert par les errata ci dessous.** Partout ou ce rapport ecrit « l'ablation C2 contre C3 » ou « l'ablation est propre », il nomme mal un contraste de conditionnement : C2 recoit onze attributs demographiques, C3 les 119 reponses de la personne sans demographie (`a45` section 0, `a47` D1).
> Les valeurs restent, 4,45 avec etiquette contre 0,44 sans et l'effet direct de plus 0,0338 ; leur attribution a la seule etiquette tombe. L'ablation propre, a un seul facteur, est le run R3 : `resultats/r3-resultats.md`.

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Reponse en une ligne : le rapport groupe sur personne des conditions a etiquette est une quantite de gabarit. Objection a45 numero 6.1, contradiction D7.

**Phrase d'origine.** « Les humains placent leurs fausses raretes davantage par la personne
que par le groupe, rapport 0,56 ; les neuf methodes du perimetre 1 052 dont le rapport est
defini font toutes l'inverse, de 1,09 pour `agents demographiques (v6)` a **8,18 pour la
foret aleatoire** et 7,37 pour `agents v8`. »

**Correction.** Le 7,37 de `v8` est reproduit a **7,32** par le generateur nul
conditionnellement independant de a44, ses deux composantes a 99 et 98 pour cent, et le
rappel des rares a 91 pour cent [a44 section 6]. Ces lifts de segment et ce rapport sont
donc des **quantites de gabarit** au sens de Yuan : ils disent que les marginales par
segment de la condition different de celles des humains, et rien de plus sur les personnes.
La phrase doit porter la mention « quantite de gabarit, reproduite par un generateur sans
structure individuelle ».

**Ce qui reste debout, et qu'il faut ecrire avec.** Le nul echoue completement du cote de la
personne chez les humains et chez les conditions riches, 0,241 contre 0,001 et 0,212 contre
0,047 [a44 section 6] : **la moitie « rarete de personne » de a31 tient**, c'est la moitie
« rarete de groupe » qui perd son statut de preuve.

**Preuve.** a44 section 6 et `a44-quantites.csv` ; convention de lecture etablie par
`a47-errata-2.md` section 3.

---

Rapport du 8 septembre 2026. Il execute le travail demande apres a29 : comprendre le
MECANISME de la phrase a defendre. a29 a etabli que les agents riches savent qui sont les
personnes a reponses rares, correlation par personne 0,531 contre 0,732 chez les memes
humains reinterroges, et qu'ils leur pretent souvent la mauvaise rarete, 61,6 pour cent de
fausses minorites contre 41,4 pour cent chez les humains, l'etiquette aggravant le point,
C2 a 0,194 contre C3 a 0,410. Ce rapport cherche ce qui distingue les cellules ou une
methode pose une fausse rarete.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a31_commun.py`, `a31_mecanismes.py`, `a31_figure.py`. **Aucun script
existant n'a ete modifie** ; `a29_commun`, `a28_commun`, `a25_commun`, `a25_mesures`,
`a8_commun`, `a2_commun`, `a2_baselines_gss`, `a5_evaluer` et `a5_agents_locaux_gss` sont
importes tels quels, memes graines, memes plis, memes blocs, memes 149 items, memes
personnes. La foret aleatoire `B3 foret` est relue du cache de a28, elle n'est pas
redefinie.

Sorties : `a31-mecanismes.csv`, `a31-contrastes.csv`, `a31-h2-par-axe.csv`,
`a31-h3-positions.csv`, `a31-h4-confiance.csv`, `a31-h5-quintiles.csv`,
`a31-synthese-mecanismes.csv`, `a31-leviers-personne-segment.csv`,
`a31-leviers-seuil-confiance.csv`, `a31-controles.csv`, `a31-figure-rarete.png` et `.svg`.

---

## Reponse en une ligne

**Le mecanisme est H2, la rarete de groupe, et il est identifie par une mesure qui separe
proprement les deux moities de la question.** Quand une methode pose une fausse rarete,
elle la pose sur une personne dont la rarete reelle est un peu au dessus du hasard, lift
**plus 0,21** pour `agents composite` contre **plus 0,24** chez les memes humains
reinterroges, et sur un segment ideologique dont la rarete reelle est tres au dessus du
hasard, lift **plus 0,34** contre **plus 0,14** chez les humains
[MESURE, `a31-leviers-personne-segment.csv`, IC bootstrap sur les personnes, p ajuste par
Holm 0,0065 sur une famille de 26 tests declaree avant execution]. **Les humains placent
leurs fausses raretes davantage par la personne que par le groupe, rapport 0,56 ; les neuf
methodes du perimetre 1 052 dont le rapport est defini font toutes l'inverse**, de 1,09 pour
`agents demographiques (v6)` a **8,18 pour la foret aleatoire** et 7,37 pour `agents v8`. **Et c'est exactement la que se joue le
renversement C2 contre C3 de a29 : C2, avec etiquette, est a un rapport de 4,45 ; C3, sans
etiquette, est a 0,44, c'est a dire du cote humain.** L'ablation directe donne, sur le lift
de groupe, **plus 0,0338 [0,0250 ; 0,0430], p ajuste 0,0012**, quand le lift du cote de la
personne ne bouge pas, moins 0,0012 [moins 0,0046 ; 0,0024] [MESURE, post hoc, signale
comme tel].

**Les quatre autres hypotheses tombent, et deux tombent a l'envers.** Le deplacement de
rarete (H1) existe, lift plus 0,59 pour `agents composite`, mais il existe autant chez les
humains, plus 0,67, et aucune condition a modele de langage ne s'en distingue apres
correction. La rarete de position (H3) est nulle partout, lift plus 0,01 : les fausses
raretes sont en bout d'echelle sept fois sur dix, mais les vraies raretes humaines des
memes items le sont tout autant. La sur confiance (H4) a le signe inverse : les fausses
raretes de C3 viennent des cellules ou le modele est le MOINS sur, 48,8 pour cent au dessus
de p max 0,99 contre 66,5 pour cent pour les raretes justes et 78,4 pour cent pour les
cellules ou il n'ose aucune rarete, difference moins 0,177 [moins 0,258 ; moins 0,091], p
ajuste 0,0135. Le contexte pauvre (H5) ne produit pas plus de fausses raretes : le taux est
plat sur les cinq quintiles de rarete du contexte, 0,616, 0,658, 0,636, 0,653 et 0,570 pour
`agents composite`, et le test declare est confondu par construction, ce que `B0 tirage`,
aveugle, demontre en le passant lui aussi.

**Ce que cela permet de corriger, en une phrase : le seul levier mesure est le retrait de
l'etiquette, et il est deja mesure. La calibration ne marche pas**, un seuil de confiance a
0,999 sur C3 fait passer la precision de 0,132 a 0,206 mais le rappel de 0,220 a 0,122, le
F1 de 0,164 a 0,153, et **le taux de fausses raretes de 0,805 a 0,791, c'est a dire pas**
[MESURE, `a31-leviers-seuil-confiance.csv`].

---

## 0. Le protocole, ecrit avant les resultats

La famille est recopiee sans retouche de l'entete de `analyses/a31_mecanismes.py`, ou elle
a ete ecrite avant l'execution. La seule verification possible pour un tiers est la lecture
de la docstring, qui n'a pas ete modifiee apres coup.

**Perimetre declare** : le perimetre naturel de chaque methode, soit les 1 052 personnes
pour les onze methodes qui les couvrent, et les 150 personnes du run local pour C2 et C3,
avec la reference de minorite calculee sur ces 150 personnes. **Seuil declare** : 10 pour
cent. **Unite d'analyse declaree** : la **fausse rarete**, c'est a dire une cellule ou la
methode predit une modalite minoritaire et ou la personne a en realite donne une modalite
majoritaire. C'est la quantite que a29 chiffre a 61,6 pour cent des raretes osees.

| | mecanisme | mesure | contre quoi | nombre de tests |
|---|---|---|---|---|
| **H1a** | deplacement de rarete | part des fausses raretes dont la personne est rare sur un AUTRE item de la meme famille thematique | les memes humains reinterroges | 13 |
| **H2a** | rarete de groupe, choix de la modalite | part des fausses raretes egales a la modalite rare modale du segment ideologique, sur les 19 items a deux modalites rares ou plus | les memes humains reinterroges | 13 |
| **H3** | rarete de position | part des fausses raretes en premiere ou derniere position de la nomenclature | les VRAIES raretes humaines, appariees item par item | 13 |
| **H5** | contexte insuffisant | rarete moyenne du contexte de la personne, hors du bloc secret | les raretes JUSTES de la meme methode | 13 |
| **H4** | sur confiance | part des cellules a p max superieur a 0,99 | les raretes JUSTES de la meme methode | 2 |

**Famille primaire declaree : H1a union H2a union H3 union H5 union H4, 54 tests.**

| | mesure complementaire | contre quoi | nombre de tests |
|---|---|---|---|
| **H1b** | rarete reelle de la personne, moyenne sur les fausses raretes | le temoin aveugle a la personne, apparie item par item | 13 |
| **H2b** | rarete reelle du segment ideologique sur cet item, moyenne sur les fausses raretes | le meme temoin aveugle | 13 |

**Famille secondaire declaree : H1b union H2b, 26 tests.** Les deux familles sont corrigees
**separement** par **Holm**, valide sans hypothese sur la dependance, ce qui est necessaire
puisque les contrastes portent sur les memes personnes et les memes items ; **Benjamini
Hochberg** est rapporte a cote. Tous les p sont des p de **bootstrap apparie sur les
personnes, 4 000 tirages**, lus sur la position de zero dans la distribution ; ils ne
descendent jamais sous 1/4 000 = 0,00025, donc le plancher de Holm vaut 0,0135 sur la
famille primaire et 0,0065 sur la secondaire.

**Le temoin aveugle a la personne**, qui est l'outil central du rapport, place exactement le
meme nombre de fausses raretes sur exactement les memes items, mais chez des personnes
tirees au hasard parmi les repondants de l'item. Le **lift** est la valeur mesuree divisee
par ce temoin, moins un. Zero veut dire que le mecanisme n'explique rien de plus qu'un
placement au hasard ; plus 0,50 veut dire la moitie de plus que ce hasard. Le lift est sans
unite, c'est ce qui permet de comparer cinq mecanismes de natures differentes.

**N'entrent dans aucune famille**, et sont des descriptions : le seuil de 20 pour cent ; le
perimetre 150 pour les onze methodes qui disposent du 1 052, echantillon emboite ; les cinq
axes autres que l'ideologie ; la version population de H2a ; le decoupage de H3 en premiere
et derniere position ; la calibration de C2 et C3 ; les quintiles de contexte ; **l'ablation
C2 contre C3, ajoutee apres avoir vu que H2b separait les deux, corrigee separement sur ses
cinq tests et signalee post hoc partout** ; les lifts eux memes, qui sont des rapports de
deux quantites dont une seule est testee ; et l'ordre d'importance des mecanismes, qui est
une lecture et non un test.

### 0.1 Trois controles executes avant toute lecture

[MESURE, `a31-controles.csv`]

1. Le decoupage en blocs recalcule par `a2_baselines_gss.grille` coincide avec le numero de
   bloc ecrit dans chaque ligne de trace du run a5, **149 items sur 149**. La covariable de
   contexte de H5 est donc bien le contexte reellement vu par C3.
2. L'argmax de la distribution relue dans la trace coincide avec la matrice de prediction
   employee par a25, a28 et a29, **22 350 cellules sur 22 350 pour C2 et autant pour C3**.
   C'est l'erreur que a18 section 2.3 a trouvee dans sa premiere version, elle n'est pas
   refaite.
3. Les taux de fausses minorites de a29 se reproduisent au chiffre pres :
   `agents composite` **0,6157** contre 0,616, `humains vague 2` **0,4140** contre 0,414,
   `B0 tirage` **0,8849** contre 0,885, `B2 argmax` **0,3645** contre 0,365, `B3 foret`
   **0,4589** contre 0,459 [MESURE, `a31-mecanismes.csv`]. Rien n'a bouge dans la chaine.

### 0.2 Le fait de structure qu'il faut lire avant tout le reste

[MESURE, perimetre 1 052, seuil 10 pour cent]

156 748 cellules evaluables, 5 709 minoritaires, masse humaine 3,64 pour cent.
**70 items sur 149 portent au moins une modalite minoritaire, mais 19 seulement en portent
au moins DEUX.** Sur les 51 autres, predire une rarete c'est predire LA rarete de l'item :
l'erreur ne peut pas etre « la mauvaise modalite rare », elle est necessairement « la
mauvaise personne ». C'est la raison arithmetique du taux de mauvaise minorite tres bas
mesure en a29 section 1 point 4, et c'est aussi un **plafond pose sur deux des cinq
hypotheses** : H2a et H3, qui portent sur le choix de la modalite, ne peuvent agir que sur
les fausses raretes des 19 items multimodalites, soit **715 des 3 337 fausses raretes de
`agents composite`, 21,4 pour cent**, contre 921 des 2 442 chez les humains, 37,7 pour
cent. Les 118 modalites minoritaires du perimetre se repartissent en 25 en premiere
position, 38 en derniere et 55 au milieu. 58 items appartiennent aux six familles
thematiques de a2, dont **21 portent une modalite minoritaire** : c'est le perimetre
d'evaluation de H1a, 21 040 cellules valides.

---

## 1. H1, deplacement de rarete : le mecanisme existe, il n'explique pas l'ecart

[MESURE, `a31-mecanismes.csv`, perimetre 1 052, seuil 10 pour cent, 4 000 tirages bootstrap
sur les personnes ; contrastes dans `a31-contrastes.csv`]

| condition | fausses raretes evaluables | part rare ailleurs dans la famille | IC 95 % | temoin aveugle | **lift** | difference aux humains | p Holm |
|---|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***732*** | ***0,4208*** | ***[0,375 ; 0,469]*** | ***0,2526*** | ***plus 0,67*** | ref | ref |
| agents enquete | 1 409 | 0,4684 | [0,425 ; 0,510] | 0,2761 | plus 0,70 | plus 0,048 | 1,000 |
| agents composite | 1 584 | 0,4899 | [0,442 ; 0,534] | 0,3089 | plus 0,59 | plus 0,069 | 0,137 |
| agents entretien (v3) | 1 904 | 0,4375 | [0,395 ; 0,480] | 0,3155 | plus 0,39 | plus 0,017 | 1,000 |
| agents v8 | 3 165 | 0,3795 | [0,340 ; 0,418] | 0,3059 | plus 0,24 | moins 0,041 | 1,000 |
| **B2 argmax** | 50 | 0,6400 | [0,508 ; 0,764] | 0,2510 | **plus 1,55** | plus 0,219 | 0,080 |
| B3 foret | 32 | 0,2500 | [0,105 ; 0,444] | 0,1218 | plus 1,05 | moins 0,171 | 1,000 |
| B1 argmax | 276 | 0,3877 | [0,320 ; 0,459] | 0,2647 | plus 0,46 | moins 0,033 | 1,000 |
| agents v7 | 692 | 0,3353 | [0,280 ; 0,391] | 0,3364 | moins 0,00 | moins 0,086 | 0,333 |
| **agents demographiques (v6)** | 277 | 0,2383 | [0,181 ; 0,301] | 0,2461 | **moins 0,03** | **moins 0,183** | **0,0135** |
| **B0 tirage** | 1 396 | 0,2600 | [0,230 ; 0,291] | 0,2685 | **moins 0,03** | **moins 0,161** | **0,0135** |

Sur les 150 personnes : `C2` 0,4779 sur 226 cellules, lift plus 0,61 ; `C3` 0,3710 sur 248,
lift plus 0,32 ; humains 0,4904 sur 104, lift plus 0,88 ; aucune des deux differences ne
passe la correction [MESURE].

**Ce que le tableau dit.**

1. **Le deplacement est reel** [MESURE]. Les trois conditions riches de Stanford placent
   leurs fausses raretes sur des personnes qui sont rares ailleurs dans la meme famille thematique 39 a
   70 pour cent plus souvent qu'un placement aveugle a la personne, intervalles au dessus du
   temoin. La fausse rarete n'est donc pas posee n'importe ou : **elle vise une personne
   qui, dans ce domaine, est effectivement une personne a reponses rares.**
2. **Il n'explique rien de l'ecart aux humains** [MESURE]. Les humains reinterroges font
   exactement la meme chose, lift plus 0,67. **Aucune methode ne se distingue d'eux au dessus
   apres Holm** : le meilleur candidat, `agents composite`, est a plus 0,069 avec un p brut
   de 0,0035 et un p ajuste de 0,137. **Les deux seules methodes qui se distinguent,
   `agents demographiques (v6)` a moins 0,183 et `B0 tirage` a moins 0,161, se distinguent
   en dessous** : ce sont les deux methodes qui ne deplacent rien du tout.
3. **Et l'ordre n'est pas stable au seuil de 20 pour cent** [MESURE, hors famille]. A ce
   seuil, `agents composite` est a un lift de plus 0,41 et les humains a plus 0,22 :
   l'ordre s'inverse. Un mecanisme dont le classement bascule avec le seuil ne porte pas
   une these.

**Verdict H1 : SOUTENUE comme description, CONTREDITE comme explication.** Le deplacement
de rarete est une propriete du fait de repondre rarement, pas une signature de la
simulation.

---

## 2. H2, rarete de groupe : c'est le mecanisme

### 2.1 Le choix de la modalite, H2a : rien chez les conditions riches, tout chez celles qui ont l'etiquette

[MESURE, `a31-mecanismes.csv` et `a31-h2-par-axe.csv`, axe ideologie, 19 items,
perimetre 1 052]

| condition | cellules | part egale a la modalite rare modale du segment | IC 95 % | temoin | **lift** | difference aux humains | p Holm |
|---|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***913*** | ***0,5433*** | ***[0,511 ; 0,576]*** | ***0,5291*** | ***plus 0,03*** | ref | ref |
| **B2 argmax** | 64 | **0,8438** | [0,750 ; 0,927] | 0,4219 | **plus 1,00** | **plus 0,301** | **0,0135** |
| **B1 argmax** | 489 | **0,6871** | [0,646 ; 0,726] | 0,5266 | **plus 0,30** | **plus 0,144** | **0,0135** |
| **agents v8** | 1 194 | **0,6843** | [0,656 ; 0,712] | 0,5753 | **plus 0,19** | **plus 0,141** | **0,0135** |
| agents v7 | 861 | 0,6074 | [0,575 ; 0,640] | 0,5007 | plus 0,21 | plus 0,064 | 0,216 |
| agents demographiques (v6) | 694 | 0,5951 | [0,560 ; 0,631] | 0,5205 | plus 0,14 | plus 0,052 | 1,000 |
| agents entretien (v3) | 864 | 0,5405 | [0,509 ; 0,574] | 0,4782 | plus 0,13 | moins 0,003 | 1,000 |
| agents composite | 714 | 0,5182 | [0,484 ; 0,555] | 0,4663 | plus 0,11 | moins 0,025 | 1,000 |
| agents enquete | 1 119 | 0,5049 | [0,474 ; 0,534] | 0,3757 | plus 0,34 | moins 0,038 | 1,000 |
| B3 foret | 37 | 0,4595 | [0,313 ; 0,615] | 0,3603 | plus 0,28 | moins 0,084 | 1,000 |
| B0 tirage | 2 094 | 0,4962 | [0,476 ; 0,517] | 0,5279 | moins 0,06 | moins 0,047 | 0,448 |

Sur les 150 personnes : `C2` 0,5000 sur 314 cellules pour un temoin de 0,2379, lift **plus
1,10** ; `C3` 0,4397 sur 282 pour un temoin de 0,3608, lift plus 0,22 ; humains 0,4850 pour
un temoin de 0,3126, lift plus 0,17. **Aucune des deux differences aux humains ne passe la
correction**, +0,015 pour C2 et moins 0,045 pour C3 [MESURE] : sur ce test la, l'ecart de
lift vient des temoins et non des valeurs, et il ne faut donc pas le lire comme un
resultat teste. C'est [PROBABLE] et pas davantage.

**Trois lectures** [MESURE].

1. **Les trois methodes qui passent la correction sont celles qui n'ont que l'etiquette ou
   que le voisinage** : une regression logistique sur onze attributs demographiques, une
   foret de voisins sur les items de contexte, et `agents v8`. **Aucune condition riche de
   Stanford ne passe.** C'est le meme verdict qu'en a28 test 3 et qu'en a29 section 3.2 :
   quand une methode se trompe vers le stereotype, c'est parce qu'elle dispose de
   l'etiquette, pas parce qu'elle parle.
2. **Le plafond arithmetique borne cette lecture** : le test ne porte que sur 19 items,
   c'est a dire 21,4 pour cent des fausses raretes de `agents composite`. Meme si H2a etait
   maximal, il ne pourrait expliquer qu'un cinquieme du phenomene.
3. **Par axe**, le classement ne bouge pas beaucoup : sur les six axes, `agents v8` va de
   0,555 sur l'education a 0,689 sur le profil croise, `agents composite` de 0,478 sur la
   race a 0,543 sur l'education, et la
   version « population entiere », qui remplace le segment par la population, donne des
   valeurs voisines pour toutes les conditions sauf `agents enquete`, 0,425 contre 0,505 sur
   l'ideologie [MESURE, `a31-h2-par-axe.csv`, hors famille]. **La modalite rare modale du
   segment et celle de la population sont trop souvent la meme pour que ce test les
   separe.** C'est la limite principale de H2a.

### 2.2 Le placement, H2b : c'est ici que tout se joue

[MESURE, `a31-mecanismes.csv` et `a31-contrastes.csv`, famille secondaire, 26 tests]

Mesure : la rarete reelle du segment ideologique de la personne SUR CET ITEM LA, calculee
sur les humains de la vague 1 sans la personne elle meme, moyennee sur les fausses raretes,
contre le temoin aveugle apparie par item. Elle est definie sur les 149 items et sur toutes
les fausses raretes, donc elle n'a pas le plafond de H2a.

| condition | rarete du segment aux fausses raretes | IC 95 % | temoin | **lift groupe** | p Holm |
|---|---|---|---|---|---|
| ***humains vague 2*** | ***0,1123*** | ***[0,108 ; 0,117]*** | ***0,0989*** | ***plus 0,14*** | ref |
| **B3 foret** | 0,2891 | [0,263 ; 0,315] | 0,1596 | **plus 0,81** | **0,0065** |
| **agents v8** | 0,1496 | [0,145 ; 0,154] | 0,0859 | **plus 0,74** | **0,0065** |
| **B2 argmax** | 0,2264 | [0,205 ; 0,247] | 0,1403 | **plus 0,61** | **0,0065** |
| **B1 argmax** | 0,1906 | [0,182 ; 0,199] | 0,1268 | **plus 0,50** | **0,0065** |
| **agents entretien (v3)** | 0,1277 | [0,123 ; 0,133] | 0,0920 | **plus 0,39** | **0,0065** |
| **agents enquete** | 0,1178 | [0,113 ; 0,123] | 0,0855 | **plus 0,38** | **0,0065** |
| **agents composite** | 0,1289 | [0,124 ; 0,134] | 0,0960 | **plus 0,34** | **0,0065** |
| agents demographiques (v6) | 0,1206 | [0,116 ; 0,125] | 0,1131 | plus 0,07 | 0,0165 |
| agents v7 | 0,1022 | [0,097 ; 0,107] | 0,0960 | plus 0,06 | 0,086 |
| B0 tirage | 0,1070 | [0,104 ; 0,110] | 0,1091 | moins 0,02 | 0,483 |

Sur les 150 personnes : **`C2` 0,1303 pour un temoin de 0,0988, lift plus 0,32, p ajuste
0,0065 ; `C3` 0,0965 pour un temoin de 0,0922, lift plus 0,05, IC [moins 0,0011 ; 0,0097],
p ajuste 0,726, c'est a dire rien** ; humains 0,1174 pour 0,1055, lift plus 0,11 [MESURE].

### 2.3 Le depart entre H1 et H2, sur une seule ligne par methode

[MESURE, `a31-leviers-personne-segment.csv`, perimetre naturel, seuil 10 pour cent]

Les deux lifts cote a cote : celui du cote de la personne, H1b, et celui du cote du groupe,
H2b. Leur rapport dit par quoi la fausse rarete est guidee.

| condition | lift PERSONNE | lift GROUPE | **rapport groupe sur personne** |
|---|---|---|---|
| ***humains vague 2, 1 052*** | ***plus 0,241*** | ***plus 0,135*** | ***0,56*** |
| ***humains vague 2, 150*** | ***plus 0,283*** | ***plus 0,112*** | ***0,40*** |
| **C3, sans etiquette** | **plus 0,105** | **plus 0,046** | **0,44** |
| agents demographiques (v6) | plus 0,061 | plus 0,066 | 1,09 |
| B2 argmax | plus 0,549 | plus 0,614 | 1,12 |
| agents composite | plus 0,212 | plus 0,343 | 1,62 |
| agents enquete | plus 0,199 | plus 0,378 | 1,90 |
| agents v7 | plus 0,022 | plus 0,064 | 2,87 |
| agents entretien (v3) | plus 0,106 | plus 0,388 | 3,65 |
| **C2, avec etiquette** | **plus 0,072** | **plus 0,319** | **4,45** |
| B1 argmax | plus 0,095 | plus 0,503 | 5,28 |
| **agents v8** | plus 0,101 | plus 0,743 | **7,37** |
| **B3 foret** | plus 0,099 | plus 0,811 | **8,18** |
| B0 tirage | moins 0,021 | moins 0,019 | sans objet |

**C'est le tableau du rapport.** Les humains reinterroges sont la seule ligne, avec C3, dont
le rapport est inferieur a 1 : **quand un humain se trompe en donnant une reponse rare, il
se trompe surtout parce que la personne est du genre a repondre rarement, et accessoirement
parce que son groupe l'est.** Toutes les autres methodes font l'inverse, et les deux
extremes sont une foret aleatoire et `agents v8`, les deux methodes du dossier qui n'ont
strictement que l'etiquette.

**L'ablation, post hoc, signalee comme telle** [MESURE, `a31-contrastes.csv`, famille
« post hoc, ablation », cinq tests corriges separement] :

| mesure | C2 moins C3 | IC 95 % | p Holm |
|---|---|---|---|
| **H2b, lift du cote du groupe** | **plus 0,0338** | **[0,0250 ; 0,0430]** | **0,0012** |
| H1b, lift du cote de la personne | moins 0,0012 | [moins 0,0046 ; 0,0024] | 0,554 |
| H3, position extreme | moins 0,1494 | [moins 0,2141 ; moins 0,0926] | 0,0012 |
| H2a, modalite rare modale du segment | plus 0,0603 | [moins 0,0118 ; 0,1329] | 0,285 |
| H1a, deplacement dans la famille | plus 0,1069 | [moins 0,0211 ; 0,2373] | 0,285 |

**Meme modele, memes personnes, memes questions, memes traces. Donner l'etiquette
demographique ajoute de la rarete de groupe et n'ajoute rien du cote de la personne.**
C'est le mecanisme du renversement de a29, ou C2 est a 0,194 de correlation par personne et
C3 a 0,410, et c'est le mecanisme du deplacement de treize points vers le stereotype de
segment mesure en a28 test 3. Trois mesures independantes, la deviance, la rarete et
maintenant le placement des fausses raretes, disent la meme chose.

**Robustesse au seuil de 20 pour cent** [MESURE, hors famille] : le lift de groupe de C2
passe de 0,319 a 0,144 et celui de C3 de 0,046 a 0,014, le rapport de 10 a 1 se maintient ;
`agents composite` passe de 0,343 a 0,175 et les humains de 0,135 a 0,055, le rapport de
2,5 a 1 se maintient aussi. **L'ordre des methodes ne bouge pas.**

**Verdict H2 : SOUTENUE, et c'est le mecanisme dominant.**

---

## 3. H3, rarete de position : rien

[MESURE, `a31-mecanismes.csv` et `a31-h3-positions.csv`, perimetre 1 052]

| condition | part des fausses raretes en position extreme | temoin, vraies raretes humaines des memes items | **lift** | difference | p Holm |
|---|---|---|---|---|---|
| agents entretien (v3) | 0,7815 | 0,7751 | plus 0,01 | plus 0,006 | 1,000 |
| agents v8 | 0,7800 | 0,7820 | moins 0,00 | moins 0,002 | 1,000 |
| agents composite | 0,7770 | 0,7702 | plus 0,01 | plus 0,007 | 1,000 |
| B3 foret | 0,7579 | 0,6879 | plus 0,10 | plus 0,070 | 1,000 |
| agents enquete | 0,6737 | 0,6945 | moins 0,03 | moins 0,021 | 1,000 |
| *humains vague 2* | *0,5971* | *0,6134* | *moins 0,03* | ref | ref |
| B0 tirage | 0,5909 | 0,5901 | plus 0,00 | plus 0,001 | 1,000 |
| B2 argmax | 0,5658 | 0,6257 | moins 0,10 | moins 0,060 | 1,000 |
| B1 argmax | 0,5553 | 0,5627 | moins 0,01 | moins 0,007 | 1,000 |
| agents v7 | 0,5573 | 0,5934 | moins 0,06 | moins 0,036 | 1,000 |
| agents demographiques (v6) | 0,3183 | 0,3638 | moins 0,13 | moins 0,046 | 0,429 |

**Aucun des treize contrastes ne passe la correction, et aucun ne l'approche.** Le detail
premiere contre derniere position ne dit rien de plus : `agents composite` met 62,7 pour
cent de ses fausses raretes en derniere position et 15,0 pour cent en premiere, quand les
vraies raretes humaines des memes items y sont a 60,9 et 16,1 pour cent
[MESURE, `a31-h3-positions.csv`].

**Il faut lire ce resultat correctement, parce qu'il est contre intuitif.** Oui, les fausses
raretes sont massivement en bout d'echelle, jusqu'a 78 pour cent. **Non, ce n'est pas un
biais de la methode : c'est que les modalites rares du GSS sont elles memes en bout
d'echelle**, 63 des 118 modalites minoritaires du perimetre. Le temoin approprie n'est pas
« une modalite au hasard », c'est « une modalite rare au hasard », et sur ce temoin la il
ne reste rien.

**Verdict H3 : CONTREDITE.** Consequence directe pour le plan de travail : **la passe 2,
qui permute l'ordre de presentation des modalites, n'est pas justifiee par ce rapport comme
correctif de la fausse rarete.** Elle peut rester utile pour le biais de position sur
l'exactitude, qui n'est pas mesure ici.

---

## 4. H4, sur confiance : le signe est l'inverse

[MESURE, `a31-h4-confiance.csv`, C2 et C3, 150 personnes, distributions completes lues dans
`data/traces/a5-C2-p1.jsonl` et `a5-C3-p1.jsonl`]

| condition | type de cellule | n | p max moyen | p max median | part a p max > 0,99 | entropie moyenne, bits |
|---|---|---|---|---|---|---|
| **C2** | cellule ou aucune rarete n'est osee | 21 384 | 0,9697 | 1,0000 | **0,8034** | 0,1084 |
| C2 | rarete juste | 96 | 0,9331 | 0,9992 | 0,7188 | 0,2136 |
| **C2** | **fausse rarete** | 808 | 0,9147 | 0,9961 | **0,5569** | 0,3023 |
| C2 | mauvaise modalite rare | 62 | 0,9015 | 0,9874 | 0,4677 | 0,4197 |
| **C3** | cellule ou aucune rarete n'est osee | 21 103 | 0,9646 | 1,0000 | **0,7841** | 0,1254 |
| C3 | rarete juste | 164 | 0,9457 | 0,9996 | 0,6646 | 0,2117 |
| **C3** | **fausse rarete** | 1 004 | 0,8936 | 0,9890 | **0,4880** | 0,3848 |
| C3 | mauvaise modalite rare | 79 | 0,7307 | 0,7906 | 0,1013 | 1,0762 |

Contrastes declares, fausses raretes contre raretes justes : **C3 moins 0,177
[moins 0,258 ; moins 0,091], p ajuste par Holm 0,0135** ; C2 moins 0,162
[moins 0,260 ; moins 0,058], p ajuste 0,171, ne passe pas [MESURE].

**L'hypothese predisait le contraire.** a23 section 1.4 montre que sur dix items le modele
substitue sa modalite a celle de la population, et a23 section 4 que quand il dit 0,995 il a
raison une fois sur deux. On pouvait en deduire que la fausse rarete est une certitude mal
placee. **Elle ne l'est pas.** Le regime de certitude du modele, ce sont les cellules ou il
n'ose aucune rarete : 78 a 80 pour cent d'entre elles sont au dessus de p max 0,99. Quand il
ose une rarete il hesite deja, et quand il se trompe il hesite davantage. La hierarchie est
monotone dans les deux conditions et sur les quatre types de cellules.

**Verdict H4 : CONTREDITE, de signe inverse.** Ce qui ne contredit pas a23 : le modele reste
grossierement sur confiant EN MOYENNE, ECE 0,441 pour C2 et 0,379 pour C3. Les deux faits
tiennent ensemble, et c'est precisement pour cela que la calibration ne repare pas la
fausse rarete, voir la section 6.

---

## 5. H5, contexte insuffisant : le test declare est confondu, et la mesure non confondue est plate

[MESURE, `a31-mecanismes.csv` et `a31-h5-quintiles.csv`]

Le test declare compare la rarete du contexte des fausses raretes a celle des raretes
justes. Il passe la correction pour huit methodes sur treize, `agents composite` a moins
0,0056 [moins 0,0079 ; moins 0,0033], p ajuste 0,0135.

**Il ne faut pas le lire, et le controle qui l'interdit est dans le tableau.** **`B0 tirage`
le passe aussi**, moins 0,0113 [moins 0,0151 ; moins 0,0076], p ajuste 0,0135. Or `B0
tirage` tire dans la marginale de chaque item sans rien savoir de personne. Le contraste est
donc confondu par construction : une rarete JUSTE exige que la personne soit reellement rare
sur cet item, donc elle tombe mecaniquement sur des personnes plus rares partout ailleurs.
Toute methode, meme aveugle, produit ce signe la.

**La mesure non confondue est le taux de fausses raretes par quintile de rarete du
contexte** [MESURE, `a31-h5-quintiles.csv`, hors famille].

| quintile de rarete du contexte | 1, le plus pauvre | 2 | 3 | 4 | 5, le plus riche |
|---|---|---|---|---|---|
| rarete moyenne du contexte | 0,0097 | 0,0199 | 0,0280 | 0,0399 | 0,0753 |
| **agents composite**, taux de fausses raretes | 0,616 | 0,658 | 0,636 | 0,653 | **0,570** |
| *humains vague 2* | *0,395* | *0,423* | *0,439* | *0,403* | *0,415* |
| **C2**, 150 personnes | 0,857 | 0,884 | 0,886 | 0,858 | 0,741 |
| **C3**, 150 personnes | 0,847 | 0,848 | 0,820 | 0,834 | 0,721 |

**Le taux est plat sur les quatre premiers quintiles et ne baisse qu'au cinquieme**, de 4,6
points pour `agents composite`, 11,6 pour C2, 12,6 pour C3. Un contexte pauvre en reponses
rares ne produit pas plus de fausses raretes ; un contexte tres riche en produit un peu
moins. Et l'autre cote de la mesure, le lift du cote de la personne, dit que les fausses
raretes tombent quand meme sur des personnes plus rares que le hasard, plus 0,21 pour
`agents composite`.

**Verdict H5 : CONTREDITE dans sa forme quantitative, INDECIDABLE par le test declare.**
Le rapport ne soutient pas « enrichir le contexte » comme correctif.

---

## 6. L'ordre d'importance, et ce que cela permet de corriger

### 6.1 L'ordre

Les cinq mecanismes ne sont pas sur la meme echelle, le lift les rend comparables mais ne
les rend pas equivalents ; ce classement est une lecture et non un test, et il est
[PROBABLE] et non [MESURE].

| rang | mecanisme | verdict | ce qui le porte | ce qui le limite |
|---|---|---|---|---|
| **1** | **H2, rarete de groupe, placement** | **soutenue** | lift plus 0,34 a plus 0,81 pour huit methodes, p ajuste 0,0065 ; humains a plus 0,14 ; separe C2 de C3 par une ablation, plus 0,0338, p ajuste 0,0012 ; stable au seuil de 20 pour cent | un seul axe teste, l'ideologie ; le segment ideologique est une attitude declaree, pas une demographie |
| **2** | **H1, deplacement de rarete** | **soutenue mais non distinctive** | lift plus 0,39 a plus 0,70 pour les conditions riches | les humains font autant, plus 0,67 ; aucun contraste ne passe Holm ; l'ordre s'inverse au seuil de 20 pour cent |
| **3** | **H2a, rarete de groupe, choix de la modalite** | **soutenue pour trois methodes seulement** | `B2 argmax`, `B1 argmax` et `agents v8` passent Holm | ne concerne que 19 items, 21 pour cent des fausses raretes ; la modale du segment et celle de la population se confondent trop souvent |
| **4** | **H5, contexte insuffisant** | **contredite** | rien | le test declare est confondu, `B0 tirage` le passe ; le taux est plat par quintile |
| **5** | **H4, sur confiance** | **contredite, signe inverse** | rien | la fausse rarete vient des cellules les moins sures, moins 0,177, p ajuste 0,0135 |
| **5 ex aequo** | **H3, rarete de position** | **contredite** | rien | aucun des treize contrastes ne passe ni n'approche la correction |

### 6.2 Ce que cela permet de corriger

**H2 domine, donc le correctif est le retrait de l'etiquette, et il est deja mesure.**
[MESURE] C3, sans aucune etiquette, a un lift de groupe de plus 0,046, intervalle
[moins 0,0011 ; 0,0097] qui ne s'ecarte pas de zero, et un rapport groupe sur personne de
0,44, c'est a dire du cote humain, 0,40 sur le meme perimetre. C2, avec onze attributs, est
a plus 0,319 et 4,45. L'ablation coute 0,0338 de lift de groupe et **ne rend rien du cote de
la personne**. Ce que a29 avait mesure comme un effet, ce rapport le mesure comme un
mecanisme.

**La calibration ne marche pas, et c'est mesure, pas suppose.**
[MESURE, `a31-leviers-seuil-confiance.csv`, 150 personnes, seuil 10 pour cent] N'oser une
modalite rare qu'au dessus d'un seuil de p max :

| condition | seuil p max | raretes osees | rappel | precision | F1 | **taux de fausses raretes** |
|---|---|---|---|---|---|---|
| C3 | aucun | 1 247 | 0,2195 | 0,1315 | 0,1645 | **0,8051** |
| C3 | 0,90 | 861 | 0,1834 | 0,1591 | **0,1704** | 0,8095 |
| C3 | 0,99 | 607 | 0,1459 | 0,1796 | 0,1610 | 0,8072 |
| C3 | 0,999 | 441 | 0,1218 | **0,2063** | 0,1532 | **0,7914** |
| C2 | aucun | 966 | 0,1285 | 0,0994 | 0,1121 | **0,8364** |
| C2 | 0,999 | 382 | 0,0643 | 0,1257 | 0,0850 | **0,8534** |

**Le seuil de confiance achete de la precision en detruisant le rappel, le F1 ne bouge
pratiquement pas, et le taux de fausses raretes ne bouge pas du tout**, 0,805 vers 0,791
pour C3, et il empire pour C2. La raison est dans la section 4 : les fausses raretes sont
deja dans la queue peu sure, un seuil les coupe en meme temps que les raretes justes.

**Permuter les modalites, la passe 2, n'est pas justifiee par ce rapport** comme correctif
de la fausse rarete, puisque H3 est nul. **Enrichir le contexte n'est pas justifie** non
plus, puisque H5 est plat.

---

## 7. La figure

`a31-figure-rarete.png` et `.svg`, six panneaux, produits par `a31_figure.py` qui ne
recalcule rien et lit les tableaux.

- **Panneaux 1 a 4** : un mecanisme chacun, H1a, H2a, H2b et H3, une ligne par condition,
  le lift sur le temoin aveugle a la personne et son intervalle bootstrap sur les personnes.
  Deux lignes vertes donnent le niveau des memes humains reinterroges, en tirets sur les
  1 052 personnes et en pointilles sur les 150. C2 et C3 sont les deux points cernes de
  noir. On voit d'un coup d'oeil que le panneau 3, H2b, est le seul ou toutes les conditions
  se detachent nettement de zero et du niveau humain.
- **Panneau 5** : H4, la part des cellules a p max superieur a 0,99 par type de cellule pour
  C2 et C3. La decroissance de gauche a droite est le refus de l'hypothese.
- **Panneau 6** : le depart, lift du cote de la personne en abscisse contre lift du cote du
  groupe en ordonnee, diagonale en fond. Les humains et C3 sont sous la diagonale, tout le
  reste est dessus, et `B3 foret` et `agents v8` sont au plafond.

---

## 8. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. « Quand une population simulee attribue par erreur une opinion minoritaire, elle vise une
   personne dont le GROUPE est effectivement souvent minoritaire sur cette question, 34 pour
   cent plus souvent qu'un placement au hasard pour la meilleure condition, contre 14 pour
   cent chez les memes humains reinterroges. » [MESURE]
2. « Les humains qui changent d'avis en deux semaines placent leurs fausses raretes
   davantage par la personne que par le groupe, rapport 0,56. Les treize methodes du dossier
   font l'inverse, de 1,09 a 8,18, et les deux extremes sont une foret aleatoire et un agent
   qui ne recoit qu'une etiquette demographique. » [MESURE]
3. « A modele, personnes, questions et traces constants, donner l'etiquette demographique
   ajoute 0,034 de rarete de groupe aux fausses raretes [0,025 ; 0,043] et n'ajoute rien du
   cote de la personne, moins 0,001 [moins 0,005 ; 0,002]. » [MESURE, ablation C2 contre C3,
   post hoc, la mesure la plus propre du rapport]
4. « Les fausses raretes sont en bout d'echelle sept fois sur dix, mais les vraies reponses
   rares des memes questions le sont tout autant : ce n'est pas un biais de position, c'est
   la forme des questions. » [MESURE]
5. « Une population simulee ne se trompe pas parce qu'elle est trop sure d'elle : les
   fausses raretes de notre agent viennent des cellules ou il est le moins sur, 49 pour cent
   au dessus de p max 0,99 contre 78 pour cent la ou il n'ose aucune rarete. » [MESURE]
6. « Filtrer les reponses rares par un seuil de confiance ameliore la precision de moitie et
   detruit le rappel d'autant : le taux de fausses raretes passe de 0,805 a 0,791, c'est a
   dire ne bouge pas. » [MESURE]
7. « Attribuer la rarete a la bonne personne sur le mauvais item existe, et c'est une
   propriete du fait de repondre rarement, pas de la simulation : les humains reinterroges
   le font autant que les meilleurs agents. » [MESURE]

### Interdit

1. **Interdit d'ecrire que la mauvaise rarete est un probleme de choix de modalite.**
   [MESURE] Sur 70 items porteurs d'une modalite minoritaire, **51 n'en portent qu'une** :
   sur ceux la, oser une rarete c'est oser LA rarete, et l'erreur ne peut etre que la
   personne. Le choix de modalite ne concerne que 21 pour cent des fausses raretes.
2. **Interdit d'ecrire que la position ou l'ordre des modalites explique quoi que ce soit
   de la fausse rarete.** [MESURE] Aucun des treize contrastes de H3 n'approche la
   correction, et la passe 2 ne repare pas ce defaut la.
3. **Interdit de proposer la calibration comme correctif de la fausse rarete.** [MESURE] Le
   signe de H4 est l'inverse de l'hypothese, et le levier de seuil est mesure : il ne change
   pas le taux de fausses raretes.
4. **Interdit d'ecrire que la fausse rarete tombe sur les personnes mal renseignees.**
   [MESURE] Le taux de fausses raretes est plat sur les quatre premiers quintiles de rarete
   du contexte, et le contraste declare est confondu par construction, ce que `B0 tirage`
   demontre en le passant.
5. **Interdit d'attribuer la rarete de groupe au langage.** [MESURE] Les deux lifts de
   groupe les plus forts sont une foret aleatoire, plus 0,81, et `agents v8`, plus 0,74 ;
   la regression logistique est a plus 0,50. C'est le meme verdict qu'en a28 test 3 et a29
   section 3.2 : c'est une propriete de l'etiquette.
6. **Interdit d'employer les lifts comme s'ils etaient testes.** Les tests declares portent
   sur les valeurs, pas sur les rapports a un temoin ; les lifts sont des descriptions
   commodes, et le cas de H2a sur les 150 personnes montre qu'un lift peut separer la ou le
   test declare ne separe pas.
7. **Interdit d'employer la comparaison C2 contre C3 pour conclure sur les modeles en
   general.** Un modele ouvert de 4 milliards de parametres, un seul run, 150 personnes, et
   la limite ouverte de a23 sur la formulation des invites reste entiere.

---

## 9. Ce que cela change a `ARBITRAGE.md`

**La derniere phrase de l'option A gagne son mecanisme et perd son ambiguite.** Elle disait
« ils leur pretent souvent la mauvaise rarete, et l'etiquette demographique aggrave cela »
sans dire pourquoi. Le pourquoi est mesure : **la fausse rarete suit le groupe et non la
personne, et l'etiquette est ce qui fait basculer une methode du regime humain, ou la
personne pese plus que le groupe, au regime statistique, ou le groupe pese jusqu'a huit fois
plus.** La formulation proposee, en remplacement de la phrase actuelle :

> « Les methodes classiques simulent une societe sans minorites. Les modeles de langage en
> gardent la moitie et visent les bonnes personnes aux trois quarts du plafond humain, mais
> quand ils se trompent, ils attribuent la rarete du groupe et non celle de la personne, et
> l'etiquette demographique est exactement ce qui produit cette substitution. »

**Le premier travail apres l'arbitrage est fait.** Le second, « si un modele plus gros ou
non aligne fait mieux », devient plus precis : la quantite a surveiller sur la nuit de
calcul n'est plus seulement la correlation par personne, c'est **le rapport groupe sur
personne** du tableau 2.3. Si un modele de 20 ou 30 milliards de parametres avec etiquette
passe sous 1, la lecture change entierement ; s'il reste au dessus de 4, l'etiquette est
condamnee quelle que soit la taille.

---

## 10. Ce que je n'ai pas pu verifier

1. **Un seul axe teste pour la rarete de groupe.** H2a et H2b sont testes sur l'ideologie
   politique parce que c'est le seul axe dont a1, a23, a28 et a29 disent tous les quatre
   qu'il separe. Les cinq autres axes sont rapportes sans test pour H2a et pas du tout pour
   H2b. Un lift de groupe calcule sur le profil croise, ou sur l'ensemble des onze attributs
   comme le fait B1, pourrait donner un autre classement.
2. **La causalite du renversement C2 contre C3.** L'ablation est propre, mais sur un seul
   modele, un seul run, 150 personnes, et deux regimes d'invite dont la formulation n'a
   jamais ete comparee a celle de Stanford. La limite de a23 vaut mot pour mot.
3. **La separation entre H1b et H5.** Le contexte de H5 retire le bloc secret entier, 30
   items, mais la rarete du reste du questionnaire reste presque la meme quantite que la
   rarete generale de la personne : `agents composite` est a 0,0439 pour H5 et 0,0436 pour
   H1b. Aucune de mes deux mesures n'isole vraiment « le contexte vu » de « la personne ».
   Il faudrait une condition dont le contexte varie a personne constante ; `C3F`, qui ampute
   la famille thematique entiere, est exactement cela et n'a pas ete exploitee ici.
4. **Le temoin aveugle et le bootstrap.** Les poids d'item du temoin sont ceux de
   l'echantillon observe et ne sont pas retires a chaque tirage. Le bootstrap porte sur les
   personnes, jamais sur les items ; l'incertitude liee au tirage des 149 items n'est donc
   pas dans les intervalles, exactement comme dans a29 section 4 avant le bootstrap sur les
   items.
5. **Les 19 items multimodalites.** Tout H2a repose sur eux, et ils sont particuliers :
   `income`, `wrkstat`, `attend`, `jew`, `hunt1`, `union1`. Ce sont des items a nomenclature
   longue ou a categories fines, pas un echantillon des 149.
6. **Twin-2K-500.** Toute l'analyse porte sur le GSS. La replication hors GSS n'est pas
   faite, et c'est la verification la plus utile qui manque, comme deja dit en a29.
7. **Les egalites dans la modale rare du segment.** En cas d'egalite, la modalite la plus
   haute dans l'ordre de la nomenclature est retenue. Le choix est deterministe et
   documente, sa sensibilite n'est pas mesuree.
8. **La convention sur les refus.** Reprise de a8 et a29 sans changement : une prediction
   refusee compte comme non minoritaire. Le taux de refus est au plus 0,20 pour cent, la
   convention inverse n'est pas testee.

---

## 11. Questions ouvertes pour Simon

1. **Le rapport groupe sur personne est il la bonne mesure du papier ?** Il tient sur une
   ligne, il separe les humains de toutes les methodes, il separe C2 de C3, et il donne un
   critere de reussite pour la nuit de calcul. Mais c'est un rapport de deux lifts, dont
   aucun n'est teste directement ; les deux numerateurs le sont. Faut il le publier tel
   quel, ou construire un estimateur unique avec son intervalle ?
2. **Faut il refaire H2 sur les onze attributs et pas sur le seul axe ideologique ?** B1
   argmax voit onze attributs et je le teste sur un seul. C'est conservateur pour B1 et
   peut etre injuste pour les agents, dont la persona contient plus que l'ideologie.
3. **C3F est la condition qui manque.** Elle ampute le contexte de la famille thematique
   entiere, a personne constante. Sa trace existe, 1,9 Mo, et elle n'est ni dans a25, ni
   dans a28, ni dans a29, ni ici. C'est la seule facon de trancher H5 proprement, et de
   verifier H1 : si le deplacement dans la famille survit au retrait de la famille du
   contexte, il ne vient pas du contexte. Faut il l'ajouter au dossier ?
4. **Que faire du plafond arithmetique ?** Sur 51 des 70 items porteurs de minorite, il n'y
   a qu'une modalite rare. Une part du « la mauvaise rarete » du titre est donc un
   malentendu de vocabulaire : c'est presque toujours « la bonne rarete a la mauvaise
   personne ». Faut il changer la formule de l'arbitrage, quitte a perdre la symetrie ?
5. **La calibration est morte, faut il le dire dans le papier ?** C'est un resultat negatif
   utile pour un praticien : le reflexe de seuiller les sorties d'un modele pour ne garder
   que les reponses sures ne repare pas les minorites, il les supprime. Cela vaut il une
   sous section, ou une note de bas de page ?
6. **Le vieux excentrique et le rapport groupe sur personne.** a29 question 4 laissait
   ouverte l'inversion du profil d'age. Le lift de groupe donne un moyen de la tester
   proprement, sur l'axe age, avec une famille declaree. Est ce que cela vaut une mesure
   dediee ou est ce toujours a laisser tomber ?

---

## Rejouer

```
.venv/bin/python analyses/a31_mecanismes.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 4000
.venv/bin/python analyses/a31_figure.py
```

Les deux caches sont ceux de a25 et de a28, les memes que a28 et a29. S'ils manquent, ils
sont reconstruits, ce qui coute environ deux minutes et demie pour la foret aleatoire.
Duree totale ensuite : 8 secondes pour `a31_mecanismes`, 3 pour la figure, sur quatre
coeurs. Graine d'analyse 20260908 partout, graine de grille 20260903, celle du run a5.
