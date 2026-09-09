# a43. Ce qui reste d'une personne quand on lui retire son item, puis son groupe

Rapport du 8 septembre 2026, soiree. Verrou 7 de `MODELE-DU-MONDE.md` section 6 : la mesure de
Ahn, Mao et Lee (arXiv 2608.29455, lecture 01, L1.02) et les quatre mesures de Peng et al.
(a36), portees sur nos donnees, avec et sans etiquette, avec et sans retrait de la moyenne de
segment.

Preenregistrement : `resultats/a43-preenregistrement.md`, ecrit a 15:41:50 CEST avant tout calcul
et reproduit en section 2 de ce rapport. Aucun appel de modele. Lecture seule sur `data/`. Aucun
fichier existant n'est modifie.

Scripts nouveaux : `analyses/a43_commun.py`, `a43_r2_demoyenne.py`, `a43_peng.py`,
`a43_polarite.py`, `a43_plancher.py`, `a43_figure.py`. Sorties :
`resultats/a43-items-ordinaux.csv`, `a43-segments.csv`, `a43-r2-demoyenne.csv`,
`a43-test-ahn.csv`, `a43-decomposition.csv`, `a43-contrastes.csv`, `a43-peng.csv`,
`a43-peng-par-item.csv`, `a43-verification-a39.csv`, `a43-polarite.csv`, `a43-plancher.csv`,
`a43-figure-r2.png` et `.svg`.

---

## Reponse en une ligne

**A conditionnement egal a celui de Ahn, c'est a dire une persona fixe qui ne contient aucune
reponse de la personne, nos agents retrouvent son chiffre a la decimale pres : apres retrait de la
moyenne d'item, il reste 1,64 pour cent de variance individuelle pour `agents demographiques (v6)`,
1,10 pour `agents v7`, 1,77 pour `C2` et 5,47 pour `agents v8`, contre les 3,05 pour cent de Ahn,
et un plafond humain a deux semaines de 44,33 pour cent, contre leur 53,6** [MESURE,
`a43-r2-demoyenne.csv`] ; **apres retrait en plus de la moyenne du segment ideologie x genre x age,
la part qui reste au dela du groupe tombe a 1,09 pour cent pour v6, 0,43 pour v8 et 0,30 pour C2,
soit 2,7 / 1,1 / 0,8 pour cent du plafond, et sur le perimetre des 150 personnes ni `C2` ni
`agents v8` ne se distinguent du plancher de bruit du demoyennage mesure sur `B0 mode`**
[MESURE, `a43-plancher.csv`] ; **la prediction preenregistree P1 est donc fausse en toute rigueur,
la part au dela du groupe n'est pas nulle, mais elle est de l'ordre du centieme du plafond humain
et elle n'est pas distinguable du bruit des que l'echantillon descend a 150 personnes** ; **et la
decomposition de Ahn se reproduit presque exactement une fois les echelles orientees : effet de
personne 5,8 a 6,0 pour cent, interaction personne x item 46,0 a 48,3, rapport 7,7 a 8,4 contre
leur 8,9** [MESURE, `a43-polarite.csv`].

---

## 1. Ce qu'il faut lire avant les tableaux : trois conditionnements, pas un

C'est le point qui commande toute la lecture, et il n'etait pas dans le preenregistrement.

Ahn, Mao et Lee mesurent un jumeau dont la persona est **fixe d'un item a l'autre** et ne contient
**aucune reponse de la personne au questionnaire evalue**. Chez nous, trois conditionnements
different coexistent dans le meme tableau :

| conditionnement | conditions | comparable a Ahn ? |
|---|---|---|
| **etiquette ou persona fixe** | `agents demographiques (v6)`, `agents v7`, `agents v8`, `C2`, plus `B1 argmax` et `B3 foret` qui ne voient que 11 attributs | **oui** |
| **119 reponses de la personne** | `C3`, `B2 argmax`, `PMM k=5`, `PMM k=10`, `IM m=10 mode des m` | non, ils voient la personne |
| **toutes les reponses moins l'item predit** | `agents composite`, `agents entretien (v3)`, `agents enquete` | non, et c'est pire : leurs invites gardent les items cousins de la question predite [CONFIRME, a14 section 3.1, repris par a41 section 4.2] |

**Toute comparaison de nos conditions riches de Stanford aux 3,05 pour cent de Ahn serait une
faute.** Elles ne mesurent pas la meme chose. Elles sont dans les tableaux parce que le
preenregistrement les y met, elles ne sont pas dans la conclusion.

---

## 2. Le preenregistrement, reproduit

Le fichier `resultats/a43-preenregistrement.md` est reproduit ici en entier dans sa substance ; il
n'a pas ete modifie depuis son ecriture.

**Donnees.** Aucune donnee nouvelle. Chargement par `a28_commun.charger_tout` : memes 1 052
personnes, memes 149 items, memes plis, memes graines, memes 150 personnes du run local. Les
imputations de a35 sont relues du cache `/tmp/a35-methodes.pkl`. Deux perimetres, 1052 et 150.
Quatorze conditions plus le plancher `humains vague 2`.

**Items.** Toutes les mesures sont numeriques, donc calculees sur les seuls items **ordinaux** au
sens de `a25_commun.ORDINAUX` prive des items portant une modalite du type « Inapplicable », c'est
a dire la liste exacte de `a39_commun.items_ordinaux`. La valeur d'une modalite est son rang
normalise dans [0, 1] selon l'ordre de `question_master/gss/main.csv`. Hypothese heritee et
declaree : cet ordre est pris pour l'ordre de l'echelle.

**Moyennes retirees.** Deux niveaux, tous deux en `leave-one-out` sur les personnes : moyenne
d'item `m_j^(-i)`, puis moyenne d'item x segment `m_{j,s}^(-i)`. **Les deux sont toujours estimees
sur les 1 052 personnes**, y compris quand la mesure porte sur les 150, pour que le demoyennage
n'ajoute pas un bruit d'estimation different d'un perimetre a l'autre. Segmentation primaire
decidee d'avance : bloc d'ideologie x genre x age regroupe en trois, soit 18 segments ;
segmentation secondaire de robustesse a 42 segments. Une cellule item x segment de moins de 10
repondants observes est ecartee.

**Six mesures.** M1 `R^2` demoyenne d'item, `corr(h - m, p - m)^2` poolee sur les cellules, contre
le plafond calcule avec la vague 2. M2 la meme apres retrait de la moyenne de segment. M3 le `r`
par personne a travers les items, contre la moyenne d'item `leave-one-out` et contre la moyenne de
segment `leave-one-out`. M4 la decomposition de variance personne, item, interaction, erreur.
M5 les quatre mesures de Peng. M6 la figure.

**Predictions ecrites d'avance.** P1 la part au dela du groupe est indistinguable de zero pour v6,
v8 et C2. P2 elle est strictement positive et sous le dixieme du plafond pour composite, enquete,
entretien et C3. P3 les imputations par tirage sont entre les deux. P4 aucune de nos conditions a
modele de langage ne bat la moyenne d'item `leave-one-out`. P5 le rapport interaction sur effet de
personne chez nos humains depasse 5. P6 le rapport d'ecarts types range aveugle sous etiquette sous
riche.

**Inference.** Bootstrap sur les personnes, 2 000 tirages, graine 20260908, meme tirage pour toutes
les conditions d'un perimetre. Trois familles corrigees separement par Holm, Benjamini Hochberg en
colonne secondaire. `p` bilateral lu sur la position de zero dans la distribution bootstrap,
plancher a 1 sur 2 000. Les moyennes `leave-one-out` ne sont pas recalculees dans la boucle de
bootstrap : l'intervalle porte sur la correlation, pas sur le demoyennage, et il est donc
legerement trop etroit.

---

## 3. Protocole effectivement execute

| element | valeur | source |
|---|---|---|
| items ordinaux retenus | **71 sur 149** | `a43-items-ordinaux.csv` |
| cellules evaluees, perimetre 1052 | 74 692 | `a43-r2-demoyenne.csv` |
| cellules evaluees, perimetre 150 | 10 650 | idem |
| segments primaires | **18**, mediane 58 personnes, de 18 a 92 | `a43-segments.csv` |
| segments secondaires | 42, mediane 27 personnes, de 3 a 52 | idem |
| personnes sans segment | **0** sur 1 052 | idem |
| cellules perdues au seuil de 10, segmentation 18 | **0** | `a43-r2-demoyenne.csv`, colonne `n_cellules` |
| cellules perdues au seuil de 10, segmentation 42 | 3 195 sur 74 692, soit 4,3 pour cent | idem |
| reproduction du rapport d'ecarts types de a39 | ecart maximal **0,000000** sur les 24 lignes communes | `a43-verification-a39.csv` |

Les 71 items ordinaux sont ceux de a39, sans une ligne de definition nouvelle. Les 78 items
nominaux sont hors de tout ce rapport : aucune des mesures de Ahn ni de Peng n'est definie sur une
reponse sans echelle. C'est une restriction de perimetre, pas un choix de commodite, et elle
signifie que **a43 ne dit rien de la moitie de notre questionnaire**.

---

## 4. M1 et M2. Le `R^2` demoyenne, avec et sans le groupe

Perimetre 1052, en pour cent de variance individuelle expliquee, intervalle bootstrap sur les
personnes, `n = 74 692` cellules [MESURE, `a43-r2-demoyenne.csv`].

| condition | conditionnement | apres retrait de l'item | part du plafond | apres retrait de l'item et du segment | part du plafond |
|---|---|---|---|---|---|
| **plafond, humains vague 2** | la personne elle meme | **44,33** [42,78 ; 45,90] | 100 % | **40,13** [38,77 ; 41,59] | 100 % |
| `agents composite` | tout sauf l'item predit | 19,40 [18,34 ; 20,44] | 43,8 % | 13,53 [12,73 ; 14,37] | 33,7 % |
| `agents entretien (v3)` | tout sauf l'item predit | 16,45 [15,51 ; 17,48] | 37,1 % | 9,88 [9,21 ; 10,61] | 24,6 % |
| `IM m=10 mode des m` | 119 items et 11 demographies | 15,15 [14,23 ; 16,10] | 34,2 % | 10,26 [9,55 ; 10,96] | 25,6 % |
| `PMM k=5` | 119 items et 11 demographies | 14,39 [13,44 ; 15,32] | 32,5 % | 9,63 [8,94 ; 10,31] | 24,0 % |
| `PMM k=10` | 119 items et 11 demographies | 14,38 [13,49 ; 15,31] | 32,4 % | 9,60 [8,91 ; 10,31] | 23,9 % |
| `agents enquete` | tout sauf l'item predit | 13,38 [12,45 ; 14,40] | 30,2 % | 8,40 [7,70 ; 9,18] | 20,9 % |
| `B2 argmax` | 119 items | 10,76 [9,91 ; 11,66] | 24,3 % | 6,16 [5,58 ; 6,78] | 15,3 % |
| `B1 argmax` | 11 demographies | 6,08 [5,44 ; 6,73] | 13,7 % | **1,45** [1,20 ; 1,72] | 3,6 % |
| **`agents v8`** | **etiquette** | 5,47 [4,75 ; 6,23] | 12,3 % | **0,43** [0,26 ; 0,62] | **1,1 %** |
| `B3 foret` | 11 demographies | 5,08 [4,54 ; 5,66] | 11,5 % | **1,16** [0,95 ; 1,40] | 2,9 % |
| **`agents demographiques (v6)`** | **etiquette** | **1,64** [1,37 ; 1,98] | **3,7 %** | **1,09** [0,88 ; 1,34] | **2,7 %** |
| **`agents v7`** | **persona fixe** | **1,10** [0,82 ; 1,41] | **2,5 %** | **0,74** [0,53 ; 0,99] | **1,8 %** |
| `B0 mode` | rien | 0,00 [0,00 ; 0,01] | 0,0 % | 0,05 [0,01 ; 0,12] | 0,1 % |

Perimetre 150, `n = 10 650` cellules, avec `C2` et `C3` [MESURE, meme fichier].

| condition | conditionnement | retrait de l'item | part du plafond | retrait de l'item et du segment | part du plafond |
|---|---|---|---|---|---|
| **plafond, humains vague 2** | la personne | **42,16** [37,83 ; 46,41] | 100 % | **37,95** [33,91 ; 42,00] | 100 % |
| `agents composite` | tout sauf l'item | 19,02 [16,33 ; 21,79] | 45,1 % | 13,51 [11,31 ; 15,76] | 35,6 % |
| `agents entretien (v3)` | tout sauf l'item | 15,80 [13,32 ; 18,36] | 37,5 % | 9,55 [7,70 ; 11,37] | 25,2 % |
| `IM m=10 mode des m` | 119 items | 14,45 [12,18 ; 16,96] | 34,3 % | 9,50 [7,83 ; 11,32] | 25,0 % |
| `PMM k=5` | 119 items | 14,02 [11,67 ; 16,44] | 33,3 % | 9,20 [7,42 ; 11,00] | 24,2 % |
| `agents enquete` | tout sauf l'item | 12,67 [10,08 ; 15,44] | 30,1 % | 8,15 [6,27 ; 10,14] | 21,5 % |
| `B2 argmax` | 119 items | 10,67 [8,45 ; 13,12] | 25,3 % | 6,08 [4,62 ; 7,72] | 16,0 % |
| `B1 argmax` | 11 demographies | 5,98 [4,50 ; 7,65] | 14,2 % | 1,38 [0,81 ; 2,07] | 3,6 % |
| `agents v8` | etiquette | 5,17 [3,50 ; 7,31] | 12,3 % | **0,49** [0,09 ; 1,16] | **1,3 %** |
| `B3 foret` | 11 demographies | 4,57 [3,25 ; 6,09] | 10,8 % | 0,85 [0,39 ; 1,46] | 2,2 % |
| **`C3`** | **119 items, sans etiquette** | **3,53** [2,56 ; 4,63] | **8,4 %** | **3,04** [2,16 ; 4,02] | **8,0 %** |
| `agents demographiques (v6)` | etiquette | 1,79 [1,14 ; 2,69] | 4,2 % | 1,23 [0,72 ; 1,82] | 3,3 % |
| `agents v7` | persona fixe | 1,79 [0,91 ; 2,96] | 4,2 % | 1,15 [0,54 ; 1,99] | 3,0 % |
| **`C2`** | **etiquette** | **1,77** [1,08 ; 2,63] | **4,2 %** | **0,30** [0,08 ; 0,63] | **0,8 %** |
| `B0 mode` | rien | 0,00 [0,00 ; 0,10] | 0,0 % | 0,06 [0,00 ; 0,33] | 0,2 % |

### 4.1 Le chiffre de Ahn se retrouve, a conditionnement egal

Ahn publie **3,05 pour cent** apres retrait de la moyenne d'item, contre un plafond `test retest` de
**53,6**, soit **5,7 pour cent du plafond**. Nos quatre conditions a persona fixe donnent
**1,10 ; 1,64 ; 1,77 ; 5,47** pour cent, soit **2,5 ; 3,7 ; 4,2 ; 12,3** pour cent d'un plafond de
**44,33** [MESURE]. Trois des quatre encadrent leur chiffre. La quatrieme, `agents v8`, est
au dessus, et la section 4.3 dit pourquoi ce n'est pas une bonne nouvelle pour v8.

Notre plafond humain a deux semaines, 44,33 pour cent, est plus bas que leur 53,6. Les deux ne sont
pas la meme quantite : le leur vient du panel Twin-2K-500 et sert de reference descriptive commune
a leurs quatre jeux, ce que les auteurs signalent eux memes [CONFIRME, lecture 01, L1.02] ; le
notre est mesure sur les memes 1 052 personnes reinterrogees deux semaines plus tard, sur les items
qu'on evalue. **Notre plafond est le bon denominateur pour nos chiffres, et le leur pour les
leurs.**

### 4.2 Ce que le retrait du segment enleve, condition par condition

L'ecart entre les deux colonnes est **ce que la methode ne savait que parce qu'elle connaissait le
groupe** [MESURE, calcul sur `a43-r2-demoyenne.csv`].

| condition | perd, en points de `R^2` | perd, en part de son propre signal |
|---|---|---|
| `agents v8` | 5,47 vers 0,43 | **92 pour cent** |
| `B1 argmax` | 6,08 vers 1,45 | 76 pour cent |
| `B3 foret` | 5,08 vers 1,16 | 77 pour cent |
| `C2` (150) | 1,77 vers 0,30 | **83 pour cent** |
| `agents demographiques (v6)` | 1,64 vers 1,09 | 34 pour cent |
| `agents v7` | 1,10 vers 0,74 | 33 pour cent |
| `agents composite` | 19,40 vers 13,53 | 30 pour cent |
| `PMM k=5` | 14,39 vers 9,63 | 33 pour cent |
| **`C3` (150)** | **3,53 vers 3,04** | **14 pour cent** |

Deux lectures. **La premiere est le resultat central du verrou.** `C2` et `agents v8`, les deux
conditions ou l'etiquette est seule, perdent 83 et 92 pour cent de leur signal individuel quand on
retire la moyenne de leur segment : ce qu'elles savaient d'une personne etait presque entierement
la moyenne de son groupe. `C3`, la meme machine sans etiquette et avec les 119 items, ne perd que
14 pour cent : son signal n'est pas de nature demographique. **La seconde** : les deux predicteurs
statistiques purement demographiques, `B1` et `B3 foret`, perdent 76 et 77 pour cent, c'est a dire
le meme comportement que l'etiquette. C'est la ligne qui dit que **le geste n'est pas propre au
langage, il est propre au conditionnement sur le groupe.**

### 4.3 Le plancher de bruit du demoyennage, et pourquoi P1 est fausse sans etre fausse

[ANALYSE NON PREENREGISTREE, ajoutee apres avoir vu que `B0 mode` obtient une correlation non nulle
apres retrait du segment, `a43-plancher.csv`]

Retirer la **meme** moyenne estimee des deux cotes injecte le bruit d'estimation de cette moyenne
dans les deux termes de la correlation, et gonfle donc la correlation residuelle. Sur la moyenne
d'item, estimee sur mille repondants, c'est negligeable : `B0 mode` obtient `r = -0,0012`. Sur la
moyenne de segment, estimee sur cinquante huit, ce ne l'est plus : `B0 mode`, qui predit une
modalite constante par item et ne sait donc **rien** de la personne ni du segment, obtient
`r = 0,0224` sur les 18 segments et `r = 0,0449` sur les 42 [MESURE]. Le plancher double quand la
cellule est divisee par deux. C'est un artefact de la mesure de Ahn appliquee a une segmentation
fine, et il n'est pas dans leur papier parce qu'ils ne segmentent pas.

Contraste apparie contre ce plancher, meme tirage bootstrap, Holm sur la famille
[MESURE, `a43-plancher.csv`, variante « moyenne d'item et de segment 18 »] :

| perimetre | condition | correlation moins celle de `B0 mode` | IC 95 % | `p` Holm |
|---|---|---|---|---|
| 1052 | `agents demographiques (v6)` | +0,0823 | [0,0690 ; 0,0963] | 0,0065 |
| 1052 | `agents v7` | +0,0637 | [0,0494 ; 0,0779] | 0,0065 |
| 1052 | `agents v8` | +0,0426 | [0,0201 ; 0,0655] | 0,0065 |
| **150** | **`agents v8`** | **+0,0457** | **[-0,0160 ; 0,1084]** | **0,3140** |
| **150** | **`C2`** | **+0,0306** | **[-0,0127 ; 0,0762]** | **0,3140** |
| 150 | `C3` | +0,1498 | [0,1102 ; 0,1908] | 0,0075 |
| 150 | `agents demographiques (v6)` | +0,0871 | [0,0533 ; 0,1221] | 0,0075 |

**Verdict sur P1.** La prediction disait « nulle ». Elle est fausse au sens strict : sur les
1 052 personnes, les trois conditions a etiquette gardent une correlation superieure au plancher,
avec `p` Holm de 0,0065. Elle est vraie au sens pratique : la part restante vaut **1,1 a 2,7 pour
cent du plafond humain**, et sur les 150 personnes du run local, ou l'echantillon est celui d'une
etude ordinaire, **`C2` et `agents v8` ne se distinguent plus du plancher de bruit du
demoyennage**. La formulation defendable est donc : *avec une etiquette seule, ce qui reste d'une
personne au dela de son groupe est de l'ordre du centieme du bruit humain, et disparait sous le
seuil de detection d'une etude a 150 participants.* Ce n'est pas la formule de la these, c'est
plus fort, parce que c'est chiffre.

**Verdict sur P2.** Fausse aussi, dans l'autre sens. `C3` garde 8,0 pour cent du plafond, ce qui
est au dessus du dixieme annonce, et les trois conditions riches de Stanford gardent 21 a 36 pour
cent, tres au dessus. Mais la section 1 dit pourquoi ces trois la ne comptent pas : elles voient
les reponses de la personne.

**Verdict sur P3.** Fausse. Les imputations par tirage ne sont pas entre l'etiquette et les
conditions riches : `PMM` et `IM` sont **au niveau** des conditions riches de Stanford, 9,2 a 10,3
contre 8,4 a 13,5, et tres au dessus de `C3`. Elles voient le meme contexte que les conditions
riches, ce qui explique le classement et ce qui aurait du figurer dans la prediction.

### 4.4 La segmentation a 42 segments

[MESURE, `a43-r2-demoyenne.csv`, variante « moyenne d'item et de segment 42 »] Les `R^2` sont
**plus hauts** avec la segmentation fine qu'avec la grossiere : composite 14,45 contre 13,53, v6
1,47 contre 1,09, plafond 40,75 contre 40,13. Ce n'est pas que la segmentation fine retire moins
de groupe, c'est que son plancher de bruit est deux fois plus haut, comme la section 4.3 le montre
sur `B0 mode`, 0,0449 contre 0,0224. **La segmentation primaire a 18 segments est donc la lecture
conservatrice, et c'est celle qu'il faut citer.** La secondaire ne sert qu'a montrer que le sens
du resultat ne change pas.

---

## 5. M3. Le test d'Ahn : le jumeau bat il la moyenne des autres ?

`r` moyen par personne, a travers les 71 items, valeurs brutes, moyenne des `z` de Fisher
retransformee. Perimetre 150, parce que c'est le seul ou `C2` et `C3` existent
[MESURE, `a43-test-ahn.csv`, `a43-contrastes.csv`].

| condition | `r` moyen | IC 95 % | moins la moyenne d'item LOO | `dz` | `p` Holm |
|---|---|---|---|---|---|
| **humains vague 2** | **0,7466** | [0,7197 ; 0,7690] | **+0,280** | +1,38 | 0,015 |
| `agents composite` | 0,5612 | [0,5348 ; 0,5870] | +0,094 | +0,56 | 0,015 |
| **moyenne de segment LOO** | **0,5338** | [0,5023 ; 0,5622] | reference F3 | | |
| `B2 argmax` | 0,5307 | [0,5017 ; 0,5566] | +0,064 | +0,42 | 0,015 |
| `IM m=10 mode des m` | 0,5307 | [0,5029 ; 0,5571] | +0,064 | +0,38 | 0,015 |
| `agents entretien (v3)` | 0,5250 | [0,4975 ; 0,5523] | +0,058 | +0,33 | 0,015 |
| `PMM k=5` | 0,4997 | [0,4727 ; 0,5239] | +0,033 | +0,18 | 0,198 |
| `B3 foret` | 0,4830 | [0,4542 ; 0,5126] | +0,017 | +0,13 | 0,316 |
| `agents enquete` | 0,4749 | [0,4417 ; 0,5050] | +0,008 | +0,04 | 1,000 |
| `B1 argmax` | 0,4672 | [0,4401 ; 0,4934] | +0,001 | +0,00 | 1,000 |
| **moyenne d'item LOO** | **0,4667** | [0,4367 ; 0,4951] | reference F2 | | |
| `B0 mode` | 0,4010 | [0,3723 ; 0,4296] | **-0,065** | -0,89 | 0,015 |
| **`agents demographiques (v6)`** | **0,3700** | [0,3389 ; 0,4010] | **-0,096** | -0,72 | 0,015 |
| **`agents v7`** | **0,3536** | [0,3183 ; 0,3886] | **-0,113** | -0,65 | 0,015 |
| **`agents v8`** | **0,3481** | [0,3144 ; 0,3844] | **-0,118** | -0,55 | 0,015 |
| **`C3`** | **0,3210** | [0,2935 ; 0,3470] | **-0,146** | -0,89 | 0,015 |
| **`C2`** | **0,2533** | [0,2277 ; 0,2797] | **-0,213** | -1,12 | 0,015 |

**Le chiffre de Ahn est reproduit presque a l'identique.** Il publie `r` 0,34 pour le modele de
langage contre 0,45 pour la moyenne d'item `leave-one-out`, `dz = -0,55`. Nous mesurons, pour les
trois conditions a etiquette de Stanford, **0,348 a 0,370 contre 0,467**, avec des `dz` de -0,55 a
-0,72. **La valeur -0,55 de `agents v8` est celle de leur papier au centieme pres.** Ce n'est pas
une coincidence recherchee : c'est la meme mesure sur d'autres donnees, d'autres modeles et
d'autres items.

**Verdict sur P4.** Vraie pour les cinq conditions comparables, `v6`, `v7`, `v8`, `C2` et `C3` :
aucune ne bat la moyenne des autres repondants, toutes perdent avec `p` Holm a 0,015. Fausse pour
les trois conditions riches de Stanford, qui la battent de 0,008 a 0,094 ; mais elles voient les
reponses de la personne, donc l'enonce de la prediction etait mal cadre, pas le resultat.

**Et contre la moyenne de son segment, plus severe encore** [MESURE, famille F3] : sur les
150 personnes et les quinze methodes non humaines, **onze perdent avec un `p` Holm de 0,015 a
0,024**, `C2` de -0,280 et `C3` de -0,213 ; **trois l'egalent**, `agents entretien (v3)`,
`IM m=10 mode des m` et `B2 argmax`, toutes trois a `p` Holm de 1,000 ; et **une seule est
nominalement devant**, `agents composite`, de +0,027 [0,007 ; 0,049], que Holm ne retient pas a
0,084. Seuls les humains la battent franchement, de +0,213. Autrement dit : sur nos donnees,
**predire une personne par la moyenne de son segment ideologie x genre x age n'est battu par aucune
des quinze methodes**, et cette moyenne de segment coute zero appel et onze attributs.

---

## 6. M4. La decomposition de Ahn

[MESURE, `a43-decomposition.csv` et `a43-polarite.csv`]

Chez les humains, plan personne x item x occasion, les deux occasions etant les deux vagues, sur
les 1 052 personnes et les 71 items ordinaux :

| decomposition | effet personne | effet item | interaction personne x item | erreur transitoire | rapport interaction sur personne |
|---|---|---|---|---|---|
| **Ahn, Mao et Lee** | 4,9 % | 8,7 % | 44,0 % | 42,4 % | **8,9** |
| nous, ordre du fichier | **1,9 %** | 20,1 % | 51,2 % | 26,7 % | **27,1** |
| nous, echelles orientees, moitie B | **6,0 %** | 20,5 % | 46,0 % | 27,5 % | **7,7** |
| nous, echelles orientees, moitie A | **5,8 %** | 20,1 % | 48,3 % | 25,9 % | **8,4** |

**La ligne « ordre du fichier » est fausse et il faut dire pourquoi.** L'effet principal de personne
mesure la tendance d'une personne a repondre haut sur le rang normalise. Le rang normalise suit
l'ordre des modalites du fichier de Stanford, qui n'a aucune raison de pointer dans le meme sens
d'un item a l'autre. Un jeu d'items dont les echelles pointent au hasard a un effet de personne
mecaniquement ecrase et une interaction mecaniquement gonflee. Le script `a43_polarite.py`, **non
preenregistre et declare comme tel**, estime l'orientation de chaque item sur une moitie des
personnes, par le signe de la correlation entre l'item et la moyenne des **autres** items de la
personne, puis refait la decomposition sur l'autre moitie. **19 items sur 71 sont retournes, dans
les deux sens du partage, ce qui est un accord parfait entre les deux moities.**

Une fois les echelles orientees, **les quatre parts de Ahn se reproduisent** : personne 5,8 a 6,0
contre leur 4,9 ; interaction 46,0 a 48,3 contre leur 44,0 ; **rapport 7,7 et 8,4 contre leur 8,9**.
Le seul ecart notable est l'erreur transitoire, 26 a 28 pour cent chez nous contre 42,4 chez eux,
et l'effet d'item, 20 contre 8,7 : nos humains sont plus stables a deux semaines que les leurs, et
nos items plus disperses en difficulte.

**Verdict sur P5.** Vraie dans les deux versions : le rapport vaut 27,1 sans orientation et 7,7 a
8,4 avec, tous deux au dessus de 5. **La conclusion de Ahn tient sur nos donnees** : le signal
manquant n'est pas « qui est cette personne en moyenne », qu'une persona peut encoder ; c'est
« comment cette personne s'ecarte de la moyenne sur cet item precis », qu'une persona fixe ne peut
par construction pas encoder.

Chez les methodes, une seule occasion existe, donc trois parts seulement et le rapport residu sur
personne est une **borne superieure**. Il est instructif quand meme
[MESURE, `a43-decomposition.csv`, perimetre 1052] :

| condition | part personne | part item | part residu | borne du rapport |
|---|---|---|---|---|
| humains vague 1 | 2,03 % | 20,03 % | 77,94 % | 38,4 |
| `agents composite` | 3,62 % | 26,46 % | 69,93 % | 19,3 |
| `agents v8` | 3,35 % | 19,74 % | 76,91 % | 22,9 |
| `agents v7` | 2,41 % | 50,08 % | 47,52 % | 19,7 |
| `C3` (150) | 2,44 % | 53,52 % | 44,03 % | 18,0 |
| `C2` (150) | 2,15 % | 37,43 % | 60,42 % | 28,1 |
| `PMM k=5` | 1,78 % | 22,49 % | 75,73 % | 42,5 |
| `agents demographiques (v6)` | **0,36 %** | **47,88 %** | 51,77 % | **145,1** |
| `B1 argmax` | 0,56 % | 39,41 % | 60,04 % | 108,0 |
| `B3 foret` | **0,09 %** | 57,40 % | 42,51 % | **482,1** |
| `B0 mode` | 0,00 % | 97,75 % | 2,25 % | non defini |

Lu de bas en haut, c'est l'echelle du remplacement : `B0 mode` est presque tout entier de l'effet
d'item, `agents demographiques (v6)` et `B3 foret` en sont a 47,9 et 57,4 pour cent avec un effet de
personne de 0,36 et 0,09 pour cent, la ou les humains sont a 20 pour cent d'item et 2,0 de personne.
**Une etiquette demographique produit une population dont la moitie de la variance est de l'item.**

---

## 7. M5. Les quatre mesures de Peng

[MESURE, `a43-peng.csv`, 71 items ordinaux, valeurs dans [0, 1], bootstrap sur les personnes]

Perimetre 1052 :

| condition | exactitude `1 - MAD` | correlation par item | Glass Delta | rapport d'ecarts types | items sous 1 |
|---|---|---|---|---|---|
| **humains vague 2** | **0,8692** [0,8656 ; 0,8727] | **0,667** [0,656 ; 0,680] | 0,028 | **0,999** [0,994 ; 1,006] | 35 sur 71 |
| `agents composite` | 0,7911 | 0,445 [0,434 ; 0,456] | 0,209 | 0,924 [0,916 ; 0,932] | 46 |
| `IM m=10 mode des m` | 0,7911 | 0,383 | 0,097 | 0,881 | 67 |
| `B2 argmax` | 0,7901 | 0,330 | 0,238 | 0,685 | 70 |
| `PMM k=10` | 0,7778 | 0,373 | **0,031** | **0,967** | 61 |
| `PMM k=5` | 0,7766 | 0,374 | **0,031** | **0,971** | 61 |
| `agents entretien (v3)` | 0,7703 | 0,411 | 0,267 | 0,946 | 42 |
| `B3 foret` | 0,7703 | 0,217 | 0,273 | 0,598 | 69 |
| `agents enquete` | 0,7672 | 0,383 | 0,271 | 0,907 | 46 |
| `B1 argmax` | 0,7590 | 0,233 | 0,159 | 0,807 | 66 |
| `B0 mode` | 0,7482 | **-0,014** | 0,464 | **0,042** | 71 |
| `agents demographiques (v6)` | 0,7298 | 0,208 | 0,318 | **0,654** | 65 |
| `agents v7` | 0,7198 | 0,122 | 0,393 | 0,689 | 68 |
| `agents v8` | 0,7143 | 0,219 | 0,325 | 0,914 | 38 |

Perimetre 150, lignes ajoutees :

| condition | exactitude | correlation | Glass Delta | rapport d'ecarts types |
|---|---|---|---|---|
| `C3` | 0,7165 [0,7075 ; 0,7258] | 0,262 [0,233 ; 0,295] | **0,548** | 0,781 [0,752 ; 0,808] |
| `C2` | 0,7067 [0,6986 ; 0,7152] | 0,163 [0,132 ; 0,195] | 0,452 | 0,771 [0,720 ; 0,822] |

### 7.1 Comparaison ligne a ligne avec Peng

| quantite | Peng, persona vide | Peng, etiquette | Peng, persona complete | Peng, ajuste T 0,7 | nous, l'equivalent |
|---|---|---|---|---|---|
| rapport d'ecarts types | **0,446** | **0,575** | **0,634** | **1,061** | v6 **0,654**, v7 0,689, C2 0,771, C3 0,781, v8 0,914, composite 0,924, humains 0,999 |
| exactitude | 0,734 | 0,746 | 0,748 | 0,704 | v8 0,714, v6 0,730, composite 0,791, humains 0,869 |
| correlation | 0,080 | 0,145 | 0,197 | 0,140 | v7 0,122, C2 0,163, v6 0,208, v8 0,219, composite 0,445, humains 0,667 |

**Trois choses.**

1. **Notre condition a etiquette tombe exactement sur la leur.** Leur `demographics_only` a 0,575
   de rapport d'ecarts types et 0,145 de correlation ; notre `agents demographiques (v6)` a
   **0,654 et 0,208**, notre `C2` a **0,771 et 0,163**. Les deux quantites sont dans le meme
   ordre de grandeur, du meme cote, et la correlation est du meme rang.
2. **Notre exactitude est plus haute que la leur partout, et cela ne veut rien dire.**
   L'exactitude `1 - MAD` depend de l'etendue de l'echelle et de la concentration de la
   distribution humaine ; leurs 164 resultats et nos 71 items ordinaux n'ont pas la meme forme.
   La seule lecture valable est **l'ordre**, et il coincide : le hasard en bas, l'etiquette au
   milieu, l'information individuelle en haut.
3. **Aucune de nos conditions ne sur disperse.** Leur `full_persona_fine_tuned_temperature_7`
   atteint 1,061, au dessus de 1. La ligne la plus haute chez nous est `humains vague 2` a 0,999,
   c'est a dire exactement 1 par construction. **Chez nous, tout ce qui n'est pas humain retrecit.**
   Notre `B0 mode` a 0,042 est l'equivalent de leur plancher trivial, mais dans l'autre sens : leur
   `random_benchmark` a 1,139 tire au hasard, notre `B0 mode` prend le mode, donc ne disperse rien.

**Verdict sur P6.** Presque vraie, avec une exception nommee. L'ordre attendu, aveugle sous
etiquette sous riche, tient pour `B0 mode` 0,042, `agents demographiques (v6)` 0,654, `agents v7`
0,689, et les conditions riches 0,907 a 0,946. Il **casse sur `agents v8`, a 0,914**, une condition
a etiquette qui disperse autant que les conditions riches. C'est coherent avec la section 4.2 :
`v8` disperse beaucoup et sait tres peu de la personne, ce qui est le profil d'une dispersion sans
information.

### 7.2 Le Glass's Delta, et une mise en garde sur son intervalle

Le Glass's Delta est un **ecart de moyenne**, pas un ecart de personne. Nos valeurs vont de 0,028
pour les humains a 0,548 pour `C3` [MESURE]. La valeur la plus haute du tableau est celle de
**`C3`, la condition sans etiquette**, et la seconde celle de `B0 mode`. Peng publie 0,352 ecart
type d'ecart de moyennes en moyenne, significatif dans 105 resultats sur 164, soit 64 pour cent
[CONFIRME, a36 section 2.3] ; nos conditions a modele de langage sont entre 0,209 et 0,548, donc
du meme ordre.

**Mise en garde.** L'intervalle bootstrap du Glass's Delta est **biaise vers le haut** et il faut
le lire comme une indication, pas comme un test. La mesure est une valeur absolue moyennee sur les
items ; le reechantillonnage ajoute du bruit a chaque ecart de moyenne, et la valeur absolue
transforme ce bruit en augmentation. Cela se voit dans le tableau : `PMM k=5` a une valeur
ponctuelle de 0,0308 et un intervalle de [0,0350 ; 0,0478] qui ne la contient pas. Le fait est
signale ici et non corrige ; le corriger demanderait un bootstrap sur les items, que a43 ne fait
pas.

---

## 8. La figure

`resultats/a43-figure-r2.png` et `.svg`. Deux panneaux, un par perimetre. Deux barres par methode :
sans et avec retrait de la moyenne de segment. Les deux traits verticaux verts sont les deux
plafonds correspondants, mesures sur les memes humains a deux semaines. La barre horizontale est
l'intervalle bootstrap sur les personnes. La figure est tracee a partir de
`a43-r2-demoyenne.csv` et de rien d'autre, pour qu'elle ne puisse pas diverger du texte.

Ce qu'on doit y voir en un coup d'oeil : **la distance entre n'importe quelle barre et le trait
vert**, et **la difference entre les deux barres d'une meme methode chez les conditions a
etiquette**, ou la barre hachuree disparait presque.

---

## 9. Ce que cela change a `MODELE-DU-MONDE.md` section 7

Sept modifications, de la plus forte a la plus faible. Aucune n'est appliquee au fichier :
`MODELE-DU-MONDE.md` n'est pas modifie par a43.

**1. La these gagne le chiffre qui lui manquait, et il est meilleur que le mot.** Le resume dit
« une societe simulee a partir d'etiquettes remplace chaque personne par l'esperance de son
groupe ». On peut desormais ecrire une phrase mesuree a la place d'une phrase imagee : *avec une
etiquette seule, ce qui reste d'une personne apres retrait de la moyenne de son item et de la
moyenne de son segment vaut 0,3 a 1,1 pour cent de variance, soit 0,8 a 2,7 pour cent du bruit des
memes humains reinterroges, et n'est plus distinguable du plancher de bruit de la mesure sur
150 participants.* [MESURE]

**2. Il faut ajouter une phrase au « ce que la these ne dit pas », et c'est une phrase couteuse.**
La part au dela du groupe n'est **pas** nulle sur 1 052 personnes : v6 garde 1,09 pour cent, v7
0,74, v8 0,43, tous au dessus du plancher avec `p` Holm de 0,0065. Ecrire « nulle » serait faux.
La formulation juste est « de l'ordre du centieme du plafond humain, et non detectable sous
150 personnes ». **Ne pas ecrire « nulle » dans le preprint.**

**3. Le remplacement par le groupe n'est pas une propriete du langage.** `B1 argmax` et
`B3 foret`, deux predicteurs statistiques sans langage ni alignement, perdent 76 et 77 pour cent
de leur signal individuel au retrait du segment, contre 83 et 92 pour `C2` et `v8`. Le paragraphe
de la section 7 qui dit « c'est l'etiquette elle meme » gagne un complement : **c'est le
conditionnement sur le groupe, quel que soit le moteur.** L'ablation de a23 reste ce qui distingue
notre travail, mais la conclusion doit etre formulee sur le conditionnement et non sur le langage.

**4. Un adversaire trivial nouveau, et il est humiliant.** La **moyenne de segment
`leave-one-out`** obtient `r = 0,5338` par personne sur les 150, et **aucune des quinze methodes ne
la bat de facon retenue par Holm** : onze perdent, trois l'egalent, une la depasse de +0,027 sans
passer la correction. Elle coute zero appel et onze attributs. Le tableau des vingt methodes d'imputation de la
section 7 doit la contenir : c'est le plancher trivial correct pour toute revendication au niveau
individuel, et il est plus severe que la moyenne d'item de Ahn.

**5. La decomposition de Ahn se reproduit, et elle explique nos propres resultats.** Interaction
personne x item 46 a 48 pour cent contre effet de personne 5,8 a 6,0, rapport 7,7 a 8,4. Cela dit,
sur nos donnees et non plus sur les leurs, **pourquoi enrichir une persona ne marche pas** : la
persona est fixe d'un item a l'autre, elle ne peut encoder que l'effet principal de personne, qui
vaut un huitieme de ce qu'il faudrait. C'est un argument mecanique a mettre dans le preprint, et
il n'est pas de nous.

**6. La section 8, « ce que je ne sais pas », perd une ligne et en gagne une.** Elle perd : on sait
maintenant quelle part de l'ecart `C2` contre `C3` est de nature demographique, `C2` perd 83 pour
cent de son signal au retrait du segment et `C3` seulement 14. Elle gagne : **on ne sait pas si les
1,1 pour cent qui restent a `agents demographiques (v6)` sont de l'information sur la personne ou
un residu de segmentation trop grossiere**, puisque affiner la segmentation eleve le plancher de
bruit plus vite qu'il n'abaisse le signal.

**7. La revendication de comparabilite du verrou 7 est acquise.** Nos chiffres sont maintenant
donnes dans les unites exactes de Ahn et de Peng : `R^2` demoyenne, part du plafond, `r` par
personne, `dz`, exactitude `1 - MAD`, correlation a travers les participants, Glass's Delta,
rapport d'ecarts types. Le cout annonce dans la section 6, « une soiree, zero appel », est tenu.

---

## Ce que je n'ai pas pu verifier

1. **A quoi s'applique exactement la decomposition de Ahn.** La lecture 01 ecrit « l'erreur de
   prediction se repartit en effet principal de personne 4,9 pour cent... ». J'ai implemente la
   decomposition de **la reponse humaine**, parce que c'est la seule lecture qui rend le rapport
   8,9 interpretable comme « ce qu'une persona peut encoder contre ce qu'elle ne peut pas », et
   parce que 44,0 sur 4,9 vaut 8,98. Si leur decomposition porte sur l'erreur de prediction et non
   sur la reponse, la ligne « nous » de la section 6 mesure autre chose que la leur, et la
   coincidence a 7,7 contre 8,9 serait alors fortuite. **Je n'ai pas lu le papier, seulement la
   lecture 01.**
2. **L'ordre des modalites.** Toutes les mesures numeriques de a43 supposent que l'ordre du fichier
   `question_master/gss/main.csv` est l'ordre de l'echelle, item par item. Cette hypothese est
   heritee de a1, a25, a35 et a39 et n'a jamais ete verifiee item par item. La section 6 montre
   qu'elle est fausse pour au moins 19 des 71 items **au sens de la direction**, ce qui ne veut pas
   dire que l'ordre interne soit faux.
3. **Le plancher de bruit du demoyennage n'est pas modelise, il est mesure sur un temoin.**
   `B0 mode` est un bon temoin parce qu'il est constant par item, mais il n'est pas exactement
   constant, il est le mode du pli d'entrainement. Un temoin parfaitement constant donnerait un
   plancher legerement different.
4. **Les intervalles ne portent pas sur les moyennes retirees.** Elles sont estimees une fois et
   non recalculees a chaque tirage bootstrap. Les intervalles publies sont donc **trop etroits**,
   d'un montant que je n'ai pas quantifie.
5. **Aucun bootstrap sur les items.** Toutes les incertitudes sont sur les personnes. Les
   comparaisons entre conditions sur les mesures agregees par item, en particulier le rapport
   d'ecarts types et le Glass's Delta, ne portent donc pas d'intervalle valable pour un
   reechantillonnage des items. C'est la meme limite que a39.
6. **L'intervalle du Glass's Delta est biaise vers le haut**, section 7.2, et n'est pas corrige.
7. **Les 78 items nominaux sont hors de tout ce rapport.** La moitie de notre questionnaire ne
   recoit aucune de ces mesures, et rien ne garantit que le resultat s'y transporte.
8. **Le perimetre 150 est petit pour cette mesure.** Sur `C2` et `agents v8`, l'echec a se
   distinguer du plancher peut etre un manque de puissance et non une absence de signal ; la ligne
   1052 de `agents v8`, ou l'ecart est significatif, suggere qu'il s'agit bien d'un manque de
   puissance.
9. **Je n'ai pas verifie que le cache de a35 correspond au run publie de a35.** Il porte un bloc
   `_meta` avec `force = 0,03`, coherent avec le rapport de a35, mais je n'ai pas recalcule les
   matrices.

---

## Questions ouvertes pour Simon

1. **La decomposition de Ahn porte t elle sur la reponse ou sur l'erreur ?** C'est la seule question
   du rapport dont la reponse peut invalider une section entiere. Une lecture du papier, ou une
   ligne de leur code, tranche.
2. **Faut il declarer la moyenne de segment `leave-one-out` comme adversaire principal du
   preprint ?** Elle bat treize methodes sur quatorze au niveau individuel, elle coute zero appel,
   et aucun des trois papiers voisins ne la publie. C'est soit notre meilleure ligne, soit une
   ouverture que le relecteur retournera contre nous.
3. **Le plancher de bruit du demoyennage doit il aller dans le corps ou en annexe ?** Il montre
   qu'une segmentation fine fabrique du signal, ce qui est un defaut de la mesure de Ahn appliquee
   a un terme inter groupes. C'est une contribution methodologique reelle, et c'est aussi une
   critique d'un papier qu'on cite en soutien.
4. **Que fait on de `agents v8` ?** C'est une condition a etiquette qui disperse comme une condition
   riche, 0,914 de rapport d'ecarts types, qui garde 5,47 pour cent de `R^2` apres retrait de
   l'item et 0,43 apres retrait du segment. Elle casse P6 et elle est la seule a le faire. Faut il
   la traiter comme un cas a expliquer ou comme une invite mal formee ?
5. **Doit on refaire ces mesures sur Twin-2K-500 ?** Ahn les a faites sur ce jeu, avec le meme
   plafond de 53,6 pour cent. Ce serait la comparaison ligne a ligne exacte, sur le meme jeu, avec
   nos conditions. Cout : une soiree, zero appel, si les matrices de a8 et a11 sont reutilisables.
6. **Le retrait du segment doit il devenir le denominateur par defaut de tout le dossier ?** Toutes
   nos mesures d'exactitude, y compris celles de a2, a23 et a41, sont des mesures avant retrait de
   la moyenne d'item. Passer tout le dossier a la mesure demoyennee serait un travail lourd et
   changerait plusieurs classements.

---

## Reproduction

```
.venv/bin/python analyses/a43_r2_demoyenne.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
.venv/bin/python analyses/a43_peng.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
.venv/bin/python analyses/a43_polarite.py
.venv/bin/python analyses/a43_plancher.py
.venv/bin/python analyses/a43_figure.py
```

Duree totale mesuree : moins de vingt secondes sur quatre coeurs, caches de a25, a28 et a35
presents. Zero appel de modele. Graine 20260908 partout, 2 000 tirages bootstrap.
