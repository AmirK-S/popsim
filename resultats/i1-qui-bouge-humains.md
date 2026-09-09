# I1, jour 1. Qui change d'avis dans les panels GSS, et est ce previsible

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Reponse en une ligne et section 4 : « integralement une consequence comptable » est un non rejet a 1,35 ecart type. Objection a45 numero 10.2.

**Phrase d'origine.** « [...] un generateur nul qui conserve exactement les deux marginales,
la derive et le taux de changement, et qui detruit seulement le lien entre qui part et ou il
va, produit **11,1 points**, c'est a dire un peu plus. **L'exces de changement monotone est
integralement une consequence comptable de la derive agregee ; il ne contient aucune
information sur les personnes.** [MESURE] »

**Correction.** Le nul donne 11,07 points d'exces monotone avec un ecart type de **0,50 sur
50 replicats**, contre 10,4 points mesures. L'ecart vaut **1,35 ecart type** : c'est un non
rejet, pas une egalite demontree. Le mot « integralement » et la phrase « il ne contient
aucune information sur les personnes » depassent la mesure. La formulation juste est
« indistinguable du nul, ecart 0,7 point pour un ecart type de 0,5 ». Le sens de la
conclusion ne change pas ; sa force, si.

**Preuve.** [MESURE, `i1-nul-remelange.csv`, temoin « remelange des destinations, derive et
taux conserves », 50 replicats : exces monotone moyen 11,070 points, ecart type 0,498 ; le
temoin « remelange complet » donne 5,077 points, ecart type 0,019.]

### E2. Section 4.3 : l'artefact hors pli isole sur T1 n'est pas borne sur les autres predicteurs. Objection a45 numero 10.1, [PROBABLE].

**Ce que le rapport etablit.** Le temoin de segment a une chute **negative**, moins 0,0385,
parce que son score varie a l'interieur d'un segment uniquement du fait de l'estimation hors
pli, la personne etant exclue de son propre estimateur [CONFIRME,
`i1_previsibilite.scores_hors_pli`, lignes 126 a 133].

**Ce que le rapport ne tire pas.** La meme anticorrelation existe dans la composante de
groupe de tous les autres predicteurs, eux aussi ajustes hors pli et encodant des moyennes de
segment (`L1`, `L2` par les indicatrices demographiques, `F` par les splits de la foret).
L'ampleur mesuree sur T1, 0,0385, vaut **28 pour cent de la chute de la foret (0,1368) et 43
pour cent de celle du predicteur primaire (0,0905)**. Tant que cette part n'est pas bornee,
la phrase « cette avance ne vient pas du groupe » repose sur une mesure dont on sait qu'elle
est biaisee vers le haut d'une quantite du meme ordre.

**Correction.** Porter la reserve dans la section 4.3, et refaire la chute de `L2` et de `F`
avec des moyennes de segment estimees en laissant la personne dehors mais son pli dedans, ou
publier la chute corrigee de celle de T1 comme correctif de premier ordre. Cette version
corrigee **n'a pas ete construite** ici ; l'objection porte sur le mecanisme et sur l'ordre
de grandeur, pas sur un chiffre de rechange. [PROBABLE]

---

Rapport du 8 septembre 2026, soiree. Il execute le **jour 1** de la premiere semaine de
`BRAINSTORM-IMPACT.md`, section 3 : « sur les quatre panels GSS, la part de changement
monotone par item, sa predictibilite par regression sur la vague 1, la chute sous
permutation de cette prediction, et le nul avec derive ; c'est le resultat humain d'I1, et
il dit si le signal existe avant tout appel ». Il porte aussi le volet humain d'I2, les
cross pressures.

**Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Aucun script
existant n'a ete modifie** ; `a12_retest_delai.py`, `a2_commun.py`, `a44_commun.py`,
`a30_commun.py`, `a25_commun.py` et `a28_figures.py` sont importes tels quels, memes items,
memes graines, memes definitions. Cinq scripts nouveaux : `analyses/i1_commun.py`,
`i1_changement.py`, `i1_previsibilite.py`, `i1_profils.py` et `i1_figure.py`.

**Le preenregistrement est `resultats/i1-preenregistrement.md`, ecrit le 8 septembre 2026 a
18 h 30 CEST (16 h 30 UTC), depot a `d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant
l'ecriture du premier script et avant tout calcul.** Les trois questions, les perimetres,
la definition du changement monotone, les quatre predicteurs, les trois temoins, la
quantite de verdict, six predictions et quatre controles bloquants y sont figes. Il n'a pas
ete modifie depuis.

Sorties : `i1-controles.csv`, `i1-changement-par-item.csv`,
`i1-changement-par-item-detail.csv`, `i1-changement-par-personne.csv`,
`i1-nul-remelange.csv`, `i1-trois-vagues.csv`, `i1-synthese-changement.csv`,
`i1-auc-par-item.csv`, `i1-auc-synthese.csv`, `i1-bande-nulle.csv`,
`i1-auc-par-item-mono.csv`, `i1-auc-synthese-mono.csv`, `i1-bande-nulle-mono.csv`,
`i1-cross-pressions.csv`,
`i1-profil-changeurs.csv`, `i1-position-initiale.csv`, `i1-deciles-cross-pression.csv`,
`i1-bruit-propre.csv`, `i1-figure-qui-bouge.png` et `.svg`. Aucune microdonnee.

---

## Reponse en une ligne

**Le signal individuel de changement existe et il est mesurable.** Predire qui changera
d'avis sur un item du GSS entre deux vagues distantes de quatre ans donne une AUC de
**0,670** pour une foret et de **0,610** pour la logistique complete declaree comme
predicteur primaire, contre 0,545 pour un temoin qui ne connait que le segment
ideologie x age x education et 0,500 pour un nul avec derive ; et cette avance ne vient pas
du groupe, puisque permuter les personnes a l'interieur de leur segment fait chuter l'AUC de
**0,1368** [0,1321 ; 0,1386] pour la foret et de **0,0905** [0,0863 ; 0,0928] pour la
logistique, sur 111 et 97 items sur 118 retenus apres correction de Holm. [MESURE]

**Mais ce signal individuel est fait pour les trois quarts d'une seule chose, la modalite
que la personne a donnee en vague 1.** Un predicteur qui ne connait que cela, la
probabilite de changement des gens qui ont donne la meme reponse, obtient une chute de
**0,0974**, c'est a dire **plus que le predicteur primaire** et 71 pour cent de celle de la
foret. Le reste du profil de 117 items, les demographies, les axes et les voisins n'ajoutent
que 0,039 point d'AUC de chute. **Ce qui est previsible, ce n'est pas qui va changer d'avis,
c'est quelle reponse est instable et qui la tient.** [MESURE]

**Et la direction du changement n'est pas individuelle du tout.** Sur les 4 683 personnes,
41,6 pour cent des changements vont dans le sens de la derive agregee de la periode et 31,2
pour cent a contresens, soit un exces monotone de 10,4 points ; un generateur nul qui
conserve exactement les deux marginales, la derive et le taux de changement, et qui detruit
seulement le lien entre qui part et ou il va, produit **11,1 points**, c'est a dire un peu
plus. **L'exces de changement monotone est integralement une consequence comptable de la
derive agregee ; il ne contient aucune information sur les personnes.** [MESURE]

**Enfin, la cross pression n'est pas la persuadabilite.** Les personnes dont l'axe
economique et l'axe social se contredisent changent 0,75 point de plus que les congruentes,
un ecart qu'une permutation des etiquettes de quadrant a l'interieur du segment reproduit
(`p = 0,17`), et la version continue de la variable est **decroissante**. Ce qui predit le
changement n'est pas la contradiction entre deux axes, c'est **la distance de la personne au
patron modal de son propre segment**, `rho = 0,366`, dont les quatre cinquiemes survivent a
la permutation. [MESURE]
## 1. Les controles bloquants, executes avant toute lecture

[MESURE, `i1-controles.csv`]

| controle | attendu | obtenu | passe |
|---|---|---|---|
| nombre de paires de vagues | 11 | 11 | oui |
| taille du noyau commun | 118 items | 118 | oui |
| consistance a deux ans, noyau commun, valeur de a12 | 0,6953 | **0,695267** | oui |
| consistance a quatre ans, noyau commun, valeur de a12 | 0,6745 | **0,674471** | oui |

La chaine de lecture des quatre fichiers Stata reproduit les deux denominateurs de a12 a
la quatrieme decimale, en repassant par ses fonctions et non par ses tableaux. Tout ce qui
suit est donc calcule sur exactement les memes personnes, les memes items et les memes
conventions de manquants que `a12-delai-de-retest.md`.

**Le controle 2 du preenregistrement est vide, et il faut l'ecrire.** Il demandait
d'inverser l'ordre des deux vagues item par item et de verifier que la part de changement
monotone tombe a la part de changement contraire. Elle n'y tombe pas : elle ne bouge pas
d'un milliardieme, `0,416240` avant et apres. Ce n'est pas une anomalie, c'est une symetrie
exacte de la regle. En inversant les vagues, la variation d'effectif `D` change de signe et
la personne parcourt son chemin a l'envers ; les deux conditions « la modalite prise gagne »
et « la modalite quittee perd » s'echangent terme a terme et l'ensemble des changements
monotones est identique. Le controle ne pouvait donc rien detecter. Il est remplace par le
nul avec derive de la section 3, qui est le temoin qu'il aurait fallu ecrire. [MESURE]

**Le controle 3 passe dans sa version stricte.** Le temoin `T0b`, qui donne a chaque
personne le taux de changement de l'item calcule sur tout le perimetre, a une AUC de
**0,500000** exactement et une chute sous permutation de **0,000000** exactement. Le temoin
`T0` du preenregistrement, qui estime ce taux sur le pli d'entrainement, n'est pas
rigoureusement constant : sa valeur change d'un pli a l'autre, ce qui lui donne une AUC de
0,48 et une chute negative. Les deux sont publies ; c'est `T0b` qui verifie
l'implementation de la permutation.

**Le controle 4 ne retire aucun item.** Sur le perimetre a quatre ans, les 118 items ont
tous au moins 100 personnes evaluees et au moins 30 changeurs.

---

## 2. Protocole, en clair

**Les items.** Le **noyau commun de 118 items** de a12 : les items apparies dans les onze
paires de vagues a la fois, avec le seuil de cent personnes par item et par paire. Ils sont
recalcules ici par appel de `a12_retest_delai.items_stanford`, `noms_gss`, `charger_panel`
et `consistance`, sans une ligne recopiee. Consequence a connaitre : **`marhomo`, le mariage
homosexuel, n'est pas dans le noyau** ; il est mesure dans neuf paires sur onze et absent du
panel 2016-2020, donc exclu par la regle. `grass`, la legalisation de la marijuana, y est.
Des deux items a mouvement documente que `BRAINSTORM-IMPACT` cite pour I1, un seul survit
au noyau commun. [MESURE, `a12-retest-item.csv`]

**Les perimetres.** Primaire : les **quatre paires a quatre ans**, 2006-2010, 2008-2012,
2010-2014 et la cohorte 2016 du panel 2016-2020, soit **4 683 personnes**. Les quatre
echantillons de depart sont des tirages distincts du GSS, les personnes sont disjointes d'un
panel a l'autre, ce qui autorise la mise en commun et le bootstrap sur les personnes sans
correction de grappe. Secondaire : quatre paires a deux ans disjointes, 5 682 personnes.
Trois vagues : les trois panels de 2006 a 2014, 3 874 personnes.

**Le changement.** Egalite exacte de la modalite entre les deux passations, la definition de
Stanford et de a12. Les « ne sait pas », refus et non poses arrivent en NaN par pyreadstat
et sont exclus, comme dans le calcul principal de a12 ; la variante de
`a12_sensibilite_dk.py`, qui les compte comme une modalite et fait baisser la consistance de
2,5 points, n'est pas refaite ici. Les taux de changement publies sont donc, comme ceux de
a12, des **minorants**.

**Le changement monotone, et la regle en laisse un dehors.** Pour l'item `j` et la paire de
vagues, `D_j(m)` est la variation d'effectif de la modalite `m` entre les deux passations,
sur les personnes evaluables. Une personne qui passe de `a` a `b` est classee **monotone**
si, **une fois elle meme retiree du calcul de la derive**, la modalite prise gagne du terrain
et la modalite quittee en perd, c'est a dire `D_j(b) - 1 > 0` et `D_j(a) + 1 < 0` ;
**contraire** si les deux inegalites sont inversees ; **indeterminee** sinon. Le retrait de
la personne est le point technique du protocole : sans lui, tout changement de `a` vers `b`
pousserait mecaniquement `D(b)` vers le haut et se classerait monotone tout seul. La regle
ne suppose aucune ordinalite et vaut donc pour les items nominaux comme pour les echelles ;
aucune version ordinale n'est publiee.

**La derive nette.** `TV_j`, distance en variation totale entre les deux marginales de
l'item, c'est a dire la part minimale de la population qui a du bouger pour produire la
marginale d'arrivee. **La part dirigee** est `TV_j` divisee par le taux de changement brut :
c'est la fraction du mouvement observe qui n'est pas de l'agitation.

**Les deux planchers de bruit.** Le plancher de Stanford, `1 - consistance a deux semaines`
item par item, relu de `a12-items-stables-instables.csv`. Et un plancher interne qui ne
depend d'aucun echantillon exterieur : sur les trois panels a trois vagues, un **aller
retour**, `y1 = y3` et `y2` different des deux, est du bruit par construction.

---

## 3. Q-A. Un tiers des reponses change, et ce changement est presque tout de l'agitation

### 3.1 Combien de personnes changent, sur combien d'items

[MESURE, `i1-synthese-changement.csv`, `i1-changement-par-personne.csv`]

| perimetre | n personnes | taux de changement moyen par personne | IC 95 pour cent | p10 | mediane | p90 | personnes a zero changement |
|---|---|---|---|---|---|---|---|
| quatre ans | 4 683 | **0,3255** | [0,3232 ; 0,3279] | 0,2250 | 0,3205 | 0,4337 | **0 pour cent** |
| deux ans | 5 682 | **0,3115** | [0,3095 ; 0,3136] | 0,2099 | 0,3049 | 0,4179 | **0 pour cent** |

Bootstrap sur les personnes, 1 000 tirages, `bootstrap_personnes` de `a2_commun`. C'est le
complement a un des 0,6745 et 0,6953 de a12, donc rien de neuf ; ce qui est neuf est la
distribution. **Aucune des 4 683 personnes ne traverse quatre ans sans changer une seule
reponse** ; la personne mediane change sur 32 pour cent de ses 82 items, celle du dixieme
decile sur 43 pour cent. Le « tiers qui bouge » du brainstorm n'est pas un tiers de
personnes, c'est un tiers de cellules reparti sur tout le monde. [MESURE]

### 3.2 La part dirigee : 14 pour cent du mouvement, 86 pour cent d'agitation

[MESURE, `i1-changement-par-item.csv`]

Sur les 118 items du perimetre a quatre ans, le taux de changement brut moyen pondere vaut
**0,3244** et la derive nette moyenne ponderee **0,0448**. La **part dirigee** vaut donc
**0,139** en moyenne ponderee et **0,131** en mediane : **sept huitiemes du changement
individuel observe entre deux vagues ne deplacent pas la marginale.** [MESURE]
La prediction P2 du preenregistrement, « part dirigee mediane inferieure a 0,25 », est
**tenue**.

Soixante items sur 118 ont une derive nette d'au moins quatre points, treize d'au moins huit
points. La question ouverte de `BRAINSTORM-IMPACT` section 5, « combien d'items bougent de
plus de huit points dans une fenetre de quatre ans », a donc une reponse : **treize sur
118**, et elle vaut aussi pour I8. [MESURE]

### 3.3 Le plancher de bruit de Stanford

[MESURE, panneau A de la figure]

**110 items sur 118, soit 93,2 pour cent, changent davantage a quatre ans qu'a deux
semaines** ; le surcroit median vaut **9,9 points** et le surcroit moyen pondere 10,1 points.
La prediction P1, « plus de 90 pour cent des items », est **tenue**. Huit items changent
moins a quatre ans dans le panel NORC qu'a deux semaines chez Bovitz : ce sont les memes
que la section 5.2 de a12 identifiait, et **la reserve de a12 section 6 s'applique
integralement ici** : les deux mesures ne portent pas sur le meme echantillon ni sur le meme
mode de collecte, et une part inconnue du surcroit est une difference d'instrument, pas de
delai. Le plancher de Stanford est donc lu comme un ordre de grandeur, jamais comme une
soustraction exacte.

### 3.4 Le plancher interne : l'aller retour, mesure sans Stanford

[MESURE, `i1-trois-vagues.csv`, 3 874 personnes, 118 items, trois panels]

| classe sur trois vagues | part des cellules renseignees aux trois passations |
|---|---|
| stable, `y1 = y2 = y3` | **0,5608** |
| aller retour, `y1 = y3`, `y2` different | **0,1172** [0,1163 ; 0,1191] |
| changement persistant, `y1` different de `y3`, `y2` dans `{y1, y3}` | **0,2812** |
| erratique, trois modalites distinctes | 0,0407 |
| dont **monotone persistant** | **0,1176** |

La prediction P3, « le taux d'aller retour depasse le taux de changement persistant », est
**fausse**, et largement : 11,7 pour cent contre 28,1. Elle etait ecrite dans l'idee que le
changement de panel serait majoritairement du bruit ; il ne l'est pas au sens ou une
majorite des changements ne revient pas en arriere.

Ce que ce tableau donne, et que le plancher de Stanford ne pouvait pas donner, est un
**estimateur du bruit de reponse interne au panel** : sous un modele de bruit symetrique,
une passation bruitee produit autant d'allers que de retours, donc le taux de changement
attribuable au bruit dans une paire vaut environ deux fois le taux d'aller retour, soit
**0,2345** contre un taux de changement observe de 0,3244. **Environ 72 pour cent du
changement observe a quatre ans est compatible avec du bruit de reponse mesure sur les
panels eux memes**, sans passer par l'echantillon de Stanford. [PROBABLE, le modele de
bruit symetrique a deux etats est une hypothese, pas une mesure ; il ignore que le bruit
d'une echelle a cinq modalites n'a pas de raison d'etre symetrique.]

### 3.5 Le changement monotone est exactement ce que la derive impose

C'est le resultat de la section, et il est negatif au sens fort.

[MESURE, `i1-synthese-changement.csv`, `i1-nul-remelange.csv`, 50 replicats, panneau B]

| | part monotone du changement | part contraire | exces monotone | taux de changement |
|---|---|---|---|---|
| **observe, quatre ans** | **0,4162** | 0,3120 | **+0,1042** | 0,3255 |
| **nul avec derive, destinations remelangees** | **0,4201** | 0,3094 | **+0,1107** | 0,3167 |
| nul avec derive, remelange complet | 0,4050 | 0,3542 | +0,0508 | non conserve |
| observe, deux ans | 0,4094 | 0,3290 | +0,0804 | 0,3115 |

Le temoin de la deuxieme ligne est le **nul avec derive** demande par `BRAINSTORM-IMPACT`,
transpose a la classification : pour chaque item, les **destinations sont remelangees entre
les seuls changeurs**, sans qu'aucun changeur ne recoive sa propre modalite de depart. Les
origines et les destinations restent les memes multiensembles, donc **les deux marginales,
la derive agregee et le taux de changement brut sont conserves** ; ce qui est detruit est le
lien entre qui part et ou il va.

**L'exces de changement monotone observe, plus 10,4 points, est integralement reproduit par
ce nul, plus 11,1 points, et il lui est meme legerement inferieur.** Item par item, les deux
quantites correlent a **0,858**, et l'exces observe depasse celui du nul sur seulement
**67 items sur 118**, ce qui est ce qu'un tirage a pile ou face donnerait. [MESURE]

Lu en clair : **la direction du changement individuel n'est pas une propriete des personnes,
c'est la comptabilite de la derive agregee vue de pres.** Quand une modalite gagne cinq
points, il faut bien que des gens y entrent et que d'autres quittent les modalites qui
perdent ; la part de mouvements qui se trouve alors « dans le sens de la derive » est fixee
par les deux marginales, et savoir qui exactement a fait ce mouvement n'ajoute rien. Le
troisieme temoin, le remelange complet, le confirme par l'autre bout : il detruit aussi le
taux de changement, gonfle le denominateur et fait tomber l'exces a plus 5,1 points ; il ne
sert qu'a montrer qu'un nul mal construit change la reponse, ce qui est la raison d'etre du
nul a taux conserve.

### 3.6 Item par item, ou la derive est reelle

[MESURE, `i1-changement-par-item.csv` et `i1-changement-par-item-detail.csv`]

Les dix items de plus forte derive nette sur le perimetre a quatre ans :

| item | libelle abrege | n | taux de changement | derive nette | part dirigee | part monotone du changement |
|---|---|---|---|---|---|---|
| `confinan` | confiance dans les institutions financieres | 3 135 | 0,475 | **0,174** | 0,367 | 0,523 |
| `jobfind` | facilite a retrouver un emploi | 1 503 | 0,454 | 0,132 | 0,290 | 0,458 |
| `attend` | frequence de frequentation religieuse | 4 615 | 0,609 | 0,112 | 0,185 | 0,350 |
| `natheal/y` | depenses de sante | 4 511 | 0,378 | 0,107 | 0,284 | 0,534 |
| `colcom/y` | un communiste peut il enseigner | 2 871 | 0,339 | 0,106 | 0,313 | 0,627 |
| `joblose` | probabilite de perdre son emploi | 1 509 | 0,445 | 0,099 | 0,223 | 0,506 |
| `conlegis` | confiance dans le Congres | 3 107 | 0,405 | 0,098 | 0,242 | 0,535 |
| `natenvir/y` | depenses pour l'environnement | 2 211 | 0,339 | 0,090 | 0,267 | 0,463 |
| `natarms/y` | depenses de defense | 4 460 | 0,442 | 0,085 | 0,192 | 0,434 |
| `finalter` | situation financiere en amelioration | 4 661 | 0,531 | 0,083 | 0,157 | 0,420 |

La liste est celle de la crise de 2008 et de sa sortie, plus la secularisation. Elle
recoupe exactement la lecture de a12 section 5.3 : la famille `con*` et la famille `nat*`
sont celles qui bougent, les positions morales ne bougent pas.

`grass`, la legalisation de la marijuana, est le cas d'ecole du mouvement lent et
regulier : sa part dirigee monte de **0,306** dans le panel 2006-2010 a **0,483** dans le
panel 2016-2020, et sa part de changement monotone de 0,653 a 0,742, pour un taux de
changement brut qui, lui, ne bouge pas, 0,196 puis 0,167. [MESURE] **C'est l'image exacte de
ce que la section 3.5 dit : ce n'est pas que les gens changent plus, c'est qu'a taux de
changement constant la comptabilite de la derive oriente une part croissante des
mouvements.**

---

## 4. Q-B. La previsibilite : un signal individuel reel, presque entierement fait de la reponse elle meme

### 4.1 Le dispositif

Cible primaire `Y_chg`, le changement brut entre les deux vagues, item par item, sur le
perimetre a quatre ans. **Cinq predicteurs et trois temoins**, tous ajustes **par item** et
**par pli**, decoupe en cinq plis **sur les personnes** ; les scores hors pli sont
concatenes. Ce que le predicteur voit est la **vague de depart seulement** : les 118
reponses de la personne, dont la sienne a l'item predit, ses demographies, et l'indicatrice
de panel. Jamais la vague d'arrivee, jamais la derive de l'item.

- **P, position initiale seule** : le taux de changement des personnes qui donnent la meme
  modalite que la personne a cet item, estime sur le pli d'entrainement. Pendant exact du
  temoin de segment, avec la reponse propre a la place du groupe. Ajoute apres le
  preenregistrement, ecart E2.
- **L1, logistique resumee** : demographies, reponse propre a l'item, et six resumes du
  profil, scores economique et social, cross pression, distance au patron modal du segment,
  part de modalites rares, part de manquants.
- **L2, logistique complete**, **le predicteur primaire declare** : demographies plus le
  profil complet de 118 items en indicatrices, 643 colonnes, penalisation L2.
- **V, voisins k = 25** : distance de Hamming de `a2_commun` sur le profil de vague de
  depart **prive de l'item predit**, probabilite egale a la part de voisins ayant change.
- **F, foret** : 200 arbres sur les codes du profil et les demographies.
- **T0** : le taux de changement de l'item, estime sur le pli d'entrainement.
  **T0b** : le meme, estime sur tout le perimetre, donc rigoureusement constant.
  **T1** : le taux de changement du segment `ideologie x age x education`, estime sur le pli
  d'entrainement, replie sur la marginale sous dix personnes. **40 segments observes,
  effectif median 82.**

**La quantite de verdict declaree est la chute de l'AUC sous permutation des personnes a
l'interieur du segment**, `a44_commun.permuter_intra` reutilise sans retouche, 200
permutations par item et par predicteur. Elle vaut zero si le predicteur ne porte que du
groupe, et elle est positive s'il porte de l'individu.

### 4.2 Le tableau

[MESURE, `i1-auc-synthese.csv` et `i1-auc-par-item.csv`, 118 items, taux de base moyen
0,3244, IC par bootstrap sur les personnes, 1 000 tirages]

| predicteur | AUC | IC 95 pour cent | AUC apres permutation | **chute** | IC 95 pour cent | rappel des changeurs | items retenus, Holm |
|---|---|---|---|---|---|---|---|
| **F, foret** | **0,6698** | [0,6675 ; 0,6719] | 0,5330 | **0,1368** | [0,1321 ; 0,1386] | 0,478 | **111 / 118** |
| L1, logistique resumee | 0,6346 | [0,6321 ; 0,6370] | 0,5284 | 0,1062 | [0,1022 ; 0,1083] | 0,456 | 105 / 118 |
| **L2, logistique complete (primaire)** | **0,6100** | [0,6077 ; 0,6123] | 0,5195 | **0,0905** | [0,0863 ; 0,0928] | 0,425 | **97 / 118** |
| **P, position initiale seule** | 0,6060 | [0,6034 ; 0,6086] | 0,5085 | **0,0974** | [0,0930 ; 0,0999] | 0,452 | 99 / 118 |
| V, voisins k = 25 | 0,5694 | [0,5670 ; 0,5720] | 0,5177 | 0,0517 | [0,0481 ; 0,0545] | 0,378 | 54 / 118 |
| T1, temoin de segment | 0,5449 | [0,5420 ; 0,5477] | 0,5834 | **-0,0385** | [-0,0392 ; -0,0367] | 0,354 | **0 / 118** |
| T0, nul avec derive | 0,4798 | [0,4775 ; 0,4818] | 0,4996 | -0,0197 | [-0,0226 ; -0,0169] | 0,309 | 0 / 118 |
| T0b, nul a taux commun | **0,5000** | [0,5000 ; 0,5000] | 0,5000 | **0,0000** | [0,0000 ; 0,0000] | 0,327 | 0 / 118 |

La **bande d'echantillonnage de l'AUC en l'absence totale de signal**, un score tire au
hasard note contre les vraies etiquettes a l'effectif reel de chaque item, va en moyenne de
**0,4764 a 0,5231**. C'est elle, et non la valeur 0,5, qui dit ce qui est distinguable de
rien. Les cinq predicteurs et le temoin de segment en sortent ; les deux nuls y sont.

**Correction pour tests multiples.** Le `p` empirique de permutation est plancher a
`1 / 201 = 0,004975` ; sur 118 items, Holm exige moins de `0,000424`. **Le
preenregistrement a donc demande une correction que son propre nombre de permutations
interdisait de satisfaire**, et le `p` empirique retient zero item pour tout le monde. Le
`p` par approximation normale de la loi de permutation, publie a cote, redonne la
resolution : c'est lui qui porte la colonne « items retenus ». Benjamini-Hochberg sur le `p`
empirique donne les memes ordres, 114, 108, 103, 102, 88 et zero pour les trois temoins.
Ecart E4.

### 4.3 Ce que le tableau dit, en trois lignes

**Un.** Il existe un signal individuel de changement, il n'est pas dans la bande nulle, et
il n'est pas du groupe : la chute sous permutation intra segment vaut 0,1368 pour la foret
et 0,0905 pour le predicteur primaire, avec des intervalles qui ne touchent pas zero et 111
et 97 items retenus apres Holm. **La reponse a la question decisive de la mission est oui.**

**Deux.** Ce signal est presque entierement fait de la reponse elle meme. **P, qui ne
connait que la modalite donnee a l'item en vague 1, obtient une chute de 0,0974, superieure
a celle du predicteur primaire et egale a 71 pour cent de celle de la foret.** Ajouter les
117 autres reponses, les demographies, les axes de a30 et les voisins ne rapporte que
`0,1368 - 0,0974 = 0,039` point d'AUC de chute, et seule la foret, donc la non linearite et
les interactions, va chercher cette part. Une logistique complete a 643 colonnes fait
**moins bien que la seule modalite de depart**. **Ce qui est previsible, ce n'est pas la
personne, c'est l'instabilite de la cellule.**

**Trois.** Le temoin de segment est un cas d'ecole a lire a l'envers. Son AUC vaut 0,5449,
donc le segment porte un peu d'information ; mais **sa chute est negative, moins 0,0385**.
Permuter les personnes dans le segment **ameliore** son AUC. Ce n'est pas une anomalie :
son score varie a l'interieur d'un segment uniquement parce qu'il est estime hors pli, et
cette variation est negativement correlee a la cible par construction ; la permutation
efface cette correlation parasite. La lecon de methode est directe et vaut pour tout usage
futur de cette mesure : **la chute sous permutation d'un predicteur dont le score est
constant par segment doit etre lue comme nulle, meme quand la validation croisee la rend
legerement negative.** Le temoin `T0b`, seul score rigoureusement constant du tableau, donne
exactement 0,500000 et 0,000000, ce qui verifie l'implementation.

### 4.4 Ou le signal est fort, et pourquoi cela doit rendre prudent

[MESURE, `i1-auc-par-item.csv`]

Les cinq items de plus forte chute pour le predicteur primaire :

| item | libelle abrege | n | taux de base | AUC | AUC permutee | chute |
|---|---|---|---|---|---|---|
| `income` | tranche de revenu declaree | 3 920 | 0,290 | 0,866 | 0,578 | **0,289** |
| `evwork` | avez vous deja travaille un an | 1 225 | 0,047 | 0,878 | 0,621 | 0,258 |
| `racdif2` | les ecarts raciaux viennent ils de l'education | 3 008 | 0,103 | 0,804 | 0,559 | 0,245 |
| `spkhomo/y` | un homosexuel peut il prendre la parole | 3 012 | 0,118 | 0,804 | 0,565 | 0,239 |
| `wrkstat` | statut d'activite | 4 678 | 0,385 | 0,749 | 0,524 | 0,225 |

**Trois des cinq ne sont pas des opinions.** `income`, `evwork` et `wrkstat` sont des faits
biographiques, ranges « hors axe » par `a30_commun.CLASSEMENT_RESTANTS`, et ce qui est
predit chez eux est une trajectoire de vie et un effet de bord des bornes de l'echelle : qui
est dans la tranche haute de revenu ne peut pas monter, qui a deja travaille un an ne peut
pas revenir en arriere. Les deux autres, `racdif2` et `spkhomo/y`, sont des items a
modalites tres desequilibrees, taux de base 10 et 12 pour cent, ou l'essentiel de la
prediction est le retour a la mode de la section 5.1. **La ou le signal individuel est le
plus fort, il est le moins interessant.** C'est la reserve principale a poser sur le chiffre
de la section 4.2 avant de s'en servir comme barre pour un jumeau.

### 4.5 La cible secondaire, le changement monotone, et pourquoi son chiffre trompe

[MESURE, `i1-auc-synthese-mono.csv`, 118 items, taux de base 0,1350, bootstrap sur les
personnes, 300 tirages, ecart E5]

| predicteur | AUC | IC 95 pour cent | AUC apres permutation | chute | IC 95 pour cent | items retenus, Holm |
|---|---|---|---|---|---|---|
| L1, logistique resumee | 0,7410 | [0,7383 ; 0,7438] | 0,5171 | **0,2239** | [0,2181 ; 0,2263] | 113 / 118 |
| F, foret | 0,7345 | [0,7315 ; 0,7371] | 0,5241 | 0,2103 | [0,2044 ; 0,2122] | 114 / 118 |
| L2, logistique complete | 0,7049 | [0,7022 ; 0,7078] | 0,5133 | 0,1917 | [0,1866 ; 0,1938] | 109 / 118 |
| **P, position initiale seule** | 0,6825 | [0,6790 ; 0,6856] | 0,5057 | **0,1768** | [0,1706 ; 0,1789] | 103 / 118 |
| V, voisins k = 25 | 0,5563 | [0,5533 ; 0,5598] | 0,5122 | 0,0442 | [0,0400 ; 0,0484] | 43 / 118 |
| T1, temoin de segment | 0,5308 | [0,5273 ; 0,5340] | 0,5902 | -0,0594 | [-0,0603 ; -0,0567] | 0 / 118 |
| T0b, nul a taux commun | 0,5000 | [0,5000 ; 0,5000] | 0,5000 | 0,0000 | [0,0000 ; 0,0000] | 0 / 118 |

Les chiffres sont plus beaux et **il ne faut pas s'en servir**. La cible `Y_mono` vaut un
quand la personne change **et** quitte une modalite qui perd du terrain pour une modalite qui
en gagne. Or quelles modalites perdent et lesquelles gagnent est une propriete de l'item, et
**quelle modalite la personne tient est justement ce que le predicteur a le droit de voir**.
Une part importante de ces AUC est donc la derive agregee qui rentre par la definition de
l'etiquette, et non de la connaissance des personnes. La signature en est visible : `P`, qui
ne connait que la modalite de depart, passe de 0,606 sur `Y_chg` a 0,682 sur `Y_mono` et sa
chute de 0,097 a 0,177. **Sur la cible monotone, le predicteur a une ligne gagne encore plus
que les autres**, ce qui est exactement ce qu'on attend si le gain vient de la definition de
la cible. Le tableau est publie pour completude ; **le verdict d'I1 repose sur `Y_chg`**,
comme declare.

---

## 5. Q-C. Qui bouge : l'incoherence oui, la cross pression non

### 5.1 La position initiale, item par item

[MESURE, `i1-position-initiale.csv`, perimetre a quatre ans, moyennes ponderees par les
effectifs]

| position en vague de depart | n items | changement des porteurs | changement des autres | monotone des porteurs | monotone des autres |
|---|---|---|---|---|---|
| modalite **majoritaire** de l'item | 118 | **0,2626** | 0,4503 | 0,1114 | 0,1890 |
| modalite **rare**, moins de 10 pour cent | 47 | **0,7185** | 0,3320 | 0,2340 | 0,1280 |

**Qui tient une position rare a la vague de depart change dans 72 pour cent des cas, contre
33 pour cent pour les autres ; qui tient la modalite majoritaire change dans 26 pour cent
des cas.** C'est l'ecart le plus grand du rapport, et c'est aussi le plus banal : il est
pour une part indeterminee du **retour a la mode**, c'est a dire l'autre nom de l'erreur de
mesure sur une cellule rare. a42 a mesure que 54,8 pour cent seulement des reponses rares
sont redonnees a l'identique deux semaines plus tard ; sur quatre ans, en retrouver 28 pour
cent n'est pas surprenant. **Ce fait n'est donc pas un fait sur qui change d'avis, c'est
d'abord un fait sur la fiabilite des cellules rares**, et il faut le dire avant de
l'utiliser. Il reste vrai que le monotone suit : les porteurs de rarete changent monotone
deux fois plus que les autres, 0,234 contre 0,128.

### 5.2 L'incoherence initiale, personne par personne

[MESURE, `i1-profil-changeurs.csv`, correlations de Spearman sur 4 683 personnes, IC
bootstrap sur les personnes, 400 tirages, `p` de permutation intra segment sur 200
permutations, correction de Holm sur la famille de dix variables]

Cible : le taux de changement brut de la personne sur ses items evaluables.

| variable de vague de depart | rho | IC 95 pour cent | rho sous permutation intra segment | chute | p Holm |
|---|---|---|---|---|---|
| **distance de Hamming au patron modal de son propre segment** | **0,366** | [0,338 ; 0,392] | 0,083 | **0,283** | 0,0498 |
| part de modalites rares tenues | 0,338 | [0,313 ; 0,362] | 0,067 | 0,270 | 0,0498 |
| part de modalites majoritaires tenues | -0,265 | [-0,289 ; -0,235] | -0,026 | -0,239 | 0,0498 |
| annees d'etudes | -0,302 | [-0,330 ; -0,278] | -0,222 | -0,081 | 0,0498 |
| age | -0,194 | [-0,223 ; -0,168] | -0,178 | -0,016 | 0,0498 |
| part de cellules manquantes | 0,175 | [0,148 ; 0,203] | 0,030 | 0,145 | 0,0498 |
| score social z | 0,169 | [0,144 ; 0,197] | 0,070 | 0,099 | 0,0498 |
| **cross pression, `|z_eco - z_soc|`** | **-0,088** | [-0,116 ; -0,062] | -0,002 | -0,086 | 0,0498 |
| distance de l'ideologie au centre | -0,082 | [-0,110 ; -0,052] | -0,063 | -0,019 | 0,0498 |
| score economique z | 0,006 | [-0,023 ; 0,032] | 0,003 | 0,002 | **0,652, non retenu** |

Les memes correlations sur le changement **monotone** sont de meme signe et environ moitie
plus faibles : distance au patron modal 0,208, part de rares 0,154, cross pression -0,055.

Deux lectures. **L'incoherence predit le changement, et ce n'est pas du segment** : la
distance au patron modal de son propre segment tombe de 0,366 a 0,083 quand on permute les
personnes a l'interieur du segment, c'est a dire que les quatre cinquiemes de cette
correlation sont de l'individuel. **L'age et l'education, eux, sont du segment** : leurs
correlations ne perdent presque rien sous permutation, 0,194 vers 0,178 et 0,302 vers 0,222,
ce qui est attendu puisque l'age et l'education entrent dans la definition du segment.
La chute sous permutation separe donc bien les deux familles de variables, ce qui vaut
controle de la mesure.

### 5.3 Les cross pressures, le volet humain d'I2

[MESURE, `i1-cross-pressions.csv` et `i1-deciles-cross-pression.csv`]

Axes de `a30_commun` transposes aux codes du panel, premiere composante principale de chaque
bloc estimee sur le perimetre entier, orientation fixee par `polviews` : **17 items
economiques et 24 items sociaux** presents dans le noyau commun. **2 121 personnes hors
quadrant, 2 562 congruentes.**

| cible | hors quadrant | congruent | ecart | IC 95 pour cent | ecart sous permutation intra segment | p de permutation | p Holm |
|---|---|---|---|---|---|---|---|
| changement brut | 0,3296 | 0,3221 | **+0,0075** | [+0,0029 ; +0,0124] | +0,0055 [+0,0009 ; +0,0099] | **0,174** | 0,249 |
| changement monotone | 0,1371 | 0,1339 | **+0,0032** | [+0,0005 ; +0,0060] | +0,0016 [-0,0014 ; +0,0043] | **0,124** | 0,249 |

**Les personnes sous cross pression changent plus, de 0,75 point de pourcentage, et cet
ecart n'est pas distinguable de ce qu'une permutation des etiquettes de quadrant a
l'interieur du segment produit.** La prediction P6 avait deux moitiees : la premiere, « les
hors quadrant changent plus », est tenue ; la seconde, « l'ecart survit a la permutation
intra segment », est **fausse**.

Le tableau par deciles est plus net encore, et il va dans l'autre sens :

| decile de cross pression | 1 | 5 | 10 |
|---|---|---|---|
| taux de changement | 0,3335 | 0,3198 | **0,3161** |
| taux de changement monotone | 0,1359 | 0,1349 | **0,1296** |

**La relation est plate et, si elle penche, elle penche a la baisse** : plus l'ecart entre
l'axe economique et l'axe social d'une personne est grand, moins elle change. Le contraste
binaire hors quadrant contre congruent est positif, la variable continue est negative :
c'est la signature d'un effet de proximite du zero et non d'un effet de cross pression.
Pour comparaison, sur la meme figure, le decile de distance au patron modal du segment va
de 0,267 a 0,383 de facon monotone. [MESURE, panneau D]

**Verdict pour I2, cote humain.** Sur ces donnees, **la theorie de la persuadabilite par
cross pression ne se verifie pas** au sens ou l'entend `BRAINSTORM-IMPACT` I2 : les cross
presses de vague 1 ne bougent pas davantage a vague 3 une fois le segment tenu. L'objection
fatale ecrite dans I2 est donc levee par la negative : « il faut que les cross presses de
vague 1 bougent davantage a vague 3 chez les humains, sinon la theorie de la persuadabilite
ne tient pas sur nos donnees ». Elle ne tient pas sur nos donnees. **Ce qui bouge, c'est
l'incoherence par rapport a son propre groupe, pas la contradiction entre deux axes.**
Deux reserves qui comptent : l'axe economique de a30 est ampute des items `eqwlth`,
`helppoor`, `helpsick`, `helpblk` et `helpnot`, absents du sous ensemble de Stanford, et il
se reduit a la batterie de depenses publiques plus `tax` ; et sa correlation avec le
changement est nulle, 0,006, ce qui laisse ouverte l'hypothese que l'axe lui meme est mal
mesure plutot que la theorie fausse.

### 5.4 Le bruit propre de la personne

[MESURE, `i1-bruit-propre.csv`, trois panels a trois vagues, 3 874 personnes]

Le taux d'aller retour d'une personne, mesure sur une moitie tiree au hasard des 118 items,
correle a **0,148** [0,127 ; 0,169] avec son taux de changement sur **l'autre moitie**, et a
**0,074** [0,052 ; 0,098] avec son taux de changement monotone. Le croisement des moities est
ce qui rend la mesure non circulaire.

Lu en clair : **une part du signal individuel de changement est un trait de repondant, pas
un trait d'opinion.** Les gens qui font des allers retours sur la moitie A font aussi plus
de changements sur la moitie B. C'est faible, 0,148, mais c'est du meme ordre que plusieurs
des correlations de la section 5.2, et c'est la variable qu'un jumeau ne peut pas
reproduire puisqu'elle n'est pas une opinion. Elle rejoint la mesure de a29, propension aux
reponses rares correlee a moins 0,32 avec la fidelite.

---

## 6. Le score des six predictions ecrites avant le calcul

[MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | plus de 90 pour cent des items changent plus a quatre ans qu'a deux semaines | **tenue**, 93,2 pour cent, 110 items sur 118 |
| **P2** | part dirigee mediane inferieure a 0,25 | **tenue**, 0,131 en mediane, 0,139 en moyenne ponderee |
| **P3** | le taux d'aller retour depasse le taux de changement persistant | **fausse**, 0,1172 contre 0,2812 |
| **P4** | AUC du predicteur primaire entre 0,55 et 0,65 | **tenue**, 0,6100 [0,6077 ; 0,6123] |
| **P5** | chute du predicteur primaire positive et inferieure a 0,03 point d'AUC | **fausse** : positive, mais **0,0905**, trois fois la borne annoncee |
| **P6** | les hors quadrant changent plus, et l'ecart survit a la permutation intra segment | **moitie tenue, moitie fausse** : ils changent plus, `+0,0075`, et l'ecart ne survit pas, `p = 0,174` |

Trois tenues, deux fausses, une a moitie. **P5 et P3 sont fausses dans le sens qui compte** :
le signal individuel est plus grand que je ne l'attendais, et le changement de panel est
moins reversible que je ne l'attendais. Une famille de predictions qui se trompe dans les
deux sens est la seule preuve interne qu'elle a bien ete ecrite avant.

---

## 7. Les ecarts au preenregistrement

| | ecart | pourquoi |
|---|---|---|
| **E1** | **Le controle bloquant 2 est vide et il est remplace.** L'inversion de l'ordre des vagues item par item laisse la part de changement monotone strictement inchangee, `0,416240` avant et apres : c'est une symetrie exacte de la regle de direction, pas une propriete des donnees. Il est remplace par le nul avec derive a taux de changement conserve, section 3.5. | Decouvert au premier calcul, avant toute lecture d'un resultat de prediction. Le controle ecrit ne pouvait rien detecter ; le remplacer par un temoin qui, lui, peut echouer est le seul choix honnete. L'ancien controle est publie avec sa demonstration. |
| **E2** | **Un cinquieme predicteur, `P`, position initiale seule**, non prevu : la probabilite de changement des personnes qui donnent la meme modalite que la personne a l'item, estimee sur le pli d'entrainement. Ajoute avant le calcul complet, apres le premier essai a trois items. | Sans lui, la chute des quatre predicteurs declares n'etait pas decomposable : on aurait su qu'il existe un signal individuel sans savoir qu'il est fait presque entierement de l'instabilite de la reponse elle meme. C'est le pendant exact du temoin de segment `T1`, avec la reponse propre a la place du groupe. |
| **E3** | **Un temoin `T0b`, nul a taux commun**, ajoute pour verifier le controle 3. | Le `T0` declare estime le taux sur le pli d'entrainement, donc il n'est pas constant et son AUC n'est pas exactement 0,5 ; il ne pouvait pas servir de verification d'implementation de la permutation. `T0b` la fournit, a 0,500000 et 0,000000. |
| **E4** | **Un `p` de permutation par approximation normale**, publie a cote du `p` empirique, et c'est lui qui porte la correction de Holm. | Le `p` empirique sur 200 permutations est plancher a `1 / 201 = 0,004975`. Sur 118 items, Holm exige moins de `0,05 / 118 = 0,000424`. **Le plancher rend donc Holm structurellement incapable de retenir un seul item, quel que soit le resultat** ; le preenregistrement a demande une correction que son propre nombre de permutations interdisait. L'approximation normale de la loi de permutation de l'AUC redonne la resolution. Les deux `p` et les deux corrections sont publies dans `i1-auc-par-item.csv`. |
| **E5** | **Le bootstrap de la cible secondaire `Y_mono` porte sur 300 tirages et non 1 000.** | Cout de calcul. Les colonnes du tableau principal, cible `Y_chg`, sont bien a 1 000 tirages comme declare. |
| **E6** | **Le perimetre secondaire a deux ans n'est passe qu'a la partie Q-A**, pas a la partie Q-B. | Cout de calcul, une seconde execution complete. La question de savoir si la previsibilite du changement depend du delai reste ouverte. |

Deux points du preenregistrement n'ont pas ete executes et ne sont pas remplaces : la
variante « non reponse comptee comme modalite » de `a12_sensibilite_dk.py`, et la version
ordinale de la regle de direction, qui n'etait deja publiee que comme controle facultatif.


---

## 8. Ce que cela dit pour I1 et pour I2

### 8.1 I1 n'est pas mort, et la barre est chiffree

La regle de decision 1 du preenregistrement disait : si la chute du predicteur primaire
n'est pas distinguable de zero apres correction, I1 est mort avant tout appel de modele.
**Elle ne s'applique pas** : la chute vaut 0,0905 [0,0863 ; 0,0928] pour le predicteur
primaire, 0,1368 pour la foret, sur 97 et 111 items sur 118 retenus. Il y a bien, chez les
humains, une couche de changement qui appartient a la personne et pas a son groupe. La
regle 2 s'applique donc, et elle donne **la barre du run du jour 5**, a declarer avant le
run :

> Un jumeau construit sur la vague 1 du panel 2016-2020, evalue en regime C3, doit atteindre
> une **AUC hors pli superieure a 0,670** sur le changement a quatre ans et surtout une
> **chute sous permutation intra segment superieure a 0,137**, mesurees sur les memes items,
> la meme segmentation `ideologie x age x education` et la meme correction. En dessous de
> **0,097**, il ne fait pas mieux qu'un predicteur qui ne connait que la modalite donnee en
> vague 1 ; en dessous de **0,000**, il ne fait pas mieux qu'un gabarit de groupe.

Trois consequences que le jour 1 impose au jour 5.

**Un, le nul avec derive est deja gagnant sur la direction, il ne faut donc pas evaluer le
jumeau sur le sens du changement.** La section 3.5 montre que l'exces de changement monotone
est reproduit a 106 pour cent par un nul sans structure individuelle. L'objection fatale
ecrite dans I1 se verifie **chez les humains**, avant tout appel : « si ce nul fait aussi
bien que le jumeau, le jumeau ne sait que la tendance de groupe ». Le nul fait deja aussi
bien que **les humains eux memes**. La cible du jumeau doit donc etre **qui change**, jamais
**dans quel sens**, sauf a mesurer la memorisation de la marginale.

**Deux, le temoin a battre n'est pas la persistance, c'est P.** La litterature evalue au
retest ; le brainstorm proposait la persistance et la regression. Le jour 1 dit que le vrai
adversaire est plus petit et plus dur a battre : **la probabilite de changement des gens qui
ont donne la meme reponse**, qui coute zero appel, zero demographie et une ligne de code, et
qui capte 71 pour cent du signal individuel de la foret. Un jumeau qui bat la persistance
mais pas P n'a rien montre. C'est le pendant, pour le changement, de ce que a43 a etabli
pour l'etat : la moyenne du segment de la personne, calculee sans elle, `r = 0,534`, n'est
battue par aucune des quinze methodes de facon retenue par Holm.

**Trois, la puissance existe.** La question ouverte de `BRAINSTORM-IMPACT` section 5, « je ne
sais pas si les panels GSS ont assez de changeurs monotones par item pour qu'I1 ait de la
puissance », a une reponse : **aucun des 118 items n'est sous le seuil de 100 personnes ni
sous celui de 30 changeurs**, le taux de base moyen est de 32 pour cent et les intervalles
de confiance sur la chute agregee ont une largeur de 0,006 point d'AUC. La puissance n'est
pas le probleme d'I1. Le probleme d'I1 est que **la quantite qui a de la puissance,
l'instabilite d'une cellule, n'est pas celle qu'un ministre achete.**

### 8.2 I2, cote humain, tombe dans sa version publiee et se releve dans une autre

L'objection fatale d'I2 posait deux conditions. La premiere : « que les cross presses de
vague 1 bougent davantage a vague 3 chez les humains, sinon la theorie de la persuadabilite
ne tient pas sur nos donnees ». **Elle n'est pas remplie.** L'ecart hors quadrant contre
congruent vaut 0,75 point de pourcentage, il est reproduit par une permutation des
etiquettes a l'interieur du segment, et la version continue de la cross pression est
**decroissante**. Sur ces 118 items, ces 4 683 personnes et ces axes, **les cross presses ne
sont pas les persuadables**.

I2 n'est pas mort pour autant, il change d'objet. **La variable qui fait ce que la cross
pression devait faire est la distance de la personne au patron modal de son propre
segment** : `rho = 0,366` avec le changement brut, dont 0,283 survit a la permutation intra
segment. C'est une quantite qui a exactement la forme dont I2 a besoin, et elle est **deja
mesurable sur les populations simulees sans un appel de plus** : a44 a montre que les agents
a etiquette ont moins de patrons de reponses distincts que leur propre generateur nul, moins
22 a moins 47 pour cent, et que leurs items sont couples deux fois plus fort qu'entre vraies
personnes. **Un agent a etiquette est, par construction, proche du patron modal de son
segment.** La prediction que le jour 2 doit tester devient donc :

> La distribution de la distance au patron modal du segment est plus concentree vers le bas
> chez les agents que chez les humains, et la queue haute de cette distribution, les gens
> qui bougent, est manquante. Cette mesure ne demande aucun appel, elle se calcule sur les
> six conditions de Stanford, C2, C3 et les predicteurs statistiques avec le meme code que
> `i1_commun.profils`.

C'est une reformulation d'I2 qui garde son enjeu, un message optimise sur une population
sans les gens qui bougent est optimise contre des convaincus, et qui remplace une theorie
importee, Hillygus et Shields, par une quantite mesuree ici.

### 8.3 Ce qui remonte au dossier

Trois phrases qui peuvent entrer dans `MODELE-DU-MONDE` si elles sont relues.

1. **Un tiers des reponses change en quatre ans, aucune personne ne traverse quatre ans sans
   changer, et sept huitiemes de ce changement ne deplacent pas la marginale.** [MESURE]
2. **La direction du changement individuel est une quantite de gabarit au sens de a44** : un
   generateur qui conserve les deux marginales et detruit l'appariement des personnes
   reproduit 106 pour cent de l'exces de changement monotone. La liste des « quantites de
   gabarit » du dossier s'allonge d'une entree, et celle ci est mesuree **chez les humains**,
   ce qui la rend plus forte : elle ne dit pas qu'un simulateur triche, elle dit qu'il n'y a
   rien a savoir. [MESURE]
3. **La chute sous permutation intra segment se transporte de l'etat au changement.** a44
   l'avait definie sur l'exactitude, elle fonctionne sur l'AUC, elle donne zero exactement
   sur un temoin constant, elle donne une valeur negative interpretable sur un temoin de
   segment estime hors pli, et elle separe les variables de personne des variables de
   segment sur des donnees purement humaines. C'est un argument de plus pour le verrou trois
   de `MODELE-DU-MONDE` 10.5, « faire de la chute sous permutation une quantite de verdict
   preenregistree ». [MESURE]

---

## 9. Ce que je n'ai pas pu verifier

1. **Que le surcroit de changement sur le plancher de Stanford soit un effet de delai.** Les
   deux mesures viennent de deux echantillons, Bovitz en ligne et NORC en face a face, avec
   deux instruments. a12 section 6 avait deja ecrit cette reserve ; elle vaut ici sans
   attenuation, et le plancher interne de la section 3.4 existe justement pour ne pas
   dependre d'elle.
2. **Que le modele de bruit symetrique a deux etats de la section 3.4 tienne.** Sur une
   echelle a cinq modalites, il n'y a aucune raison qu'un bruit produise autant d'allers que
   de retours ; le chiffre « 72 pour cent du changement est compatible avec du bruit » est un
   ordre de grandeur, pas une decomposition.
3. **Que l'axe economique de a30 mesure l'axe economique.** Ampute de `eqwlth`, `helppoor`,
   `helpsick`, `helpblk` et `helpnot`, absents du sous ensemble de Stanford, il se reduit a
   la batterie de depenses publiques et a l'impot, et sa correlation avec le changement est
   nulle. Le verdict negatif sur les cross pressures peut etre un verdict sur l'instrument.
4. **`marhomo`**, l'item que `BRAINSTORM-IMPACT` designe comme le mouvement documente de la
   fenetre 2006-2010, n'est pas dans le noyau commun : il manque au panel 2016-2020. Il n'a
   donc pas ete mesure ici, alors que c'est un des deux items sur lesquels I1 et I8 comptent.
5. **Le taux de non reponse.** Le calcul principal exclut les « ne sait pas » et les refus,
   comme a12 ; les taux de changement publies sont des minorants d'une ampleur non mesuree
   ici.
6. **La stabilite du resultat sous un autre segment.** Toute la mesure de personne repose sur
   la segmentation `ideologie x age x education` a 27 cellules plus les non renseignes, soit
   40 segments observes d'effectif median 82. a44 a montre que l'exces de correlation entre
   items etait stable de sept a quatre vingts cellules de conditionnement ; rien ne dit que
   la chute de l'AUC le soit.
7. **La ponderation de panel.** Les quatre panels sont mis en commun sans ponderation de
   redressement ; les champs `wtpannr123` et `wtssall` existent et ne sont pas utilises. Les
   quantites publiees sont des quantites d'echantillon, pas des quantites de population
   americaine.
8. **Le regime a trois vagues pour le panel 2016-2020**, qui n'en a que deux par cohorte : la
   decomposition aller retour contre persistant ne porte que sur 2006 a 2014 et sur 3 874
   personnes.

---

## 10. Questions ouvertes pour Simon

1. **La question qui commande le jour 5 : quelle cible donne t on au jumeau ?** Le jour 1
   ferme la cible « sens du changement », qu'un nul sans structure individuelle reproduit
   deja chez les humains. Il ouvre la cible « qui change », sur laquelle un signal individuel
   existe. Mais il montre aussi que ce signal est a 71 pour cent celui d'un predicteur a une
   ligne, `P`, et que la ou il est le plus fort il porte sur `income`, `wrkstat` et `evwork`,
   c'est a dire sur des faits biographiques. **Faut il evaluer le jumeau sur les 118 items,
   ou sur le sous ensemble des items d'attitude, ou il n'y a presque rien a gagner et ou le
   resultat sera probablement nul ?** Le premier choix est flatteur pour tout le monde, le
   second est le seul qui reponde a la question du ministre. Ma preference est le second,
   declare avant le run, avec le premier publie a cote.

2. **Faut il depenser la seconde execution pour le perimetre a deux ans ?** Elle coute une
   heure de calcul et zero appel. Elle repond a « la previsibilite du changement depend elle
   du delai », qui est le prolongement direct de a12 et le seul endroit ou a12 et I1 se
   parlent. Je ne l'ai pas faite, ecart E6.

3. **Le predicteur `P` doit il devenir un plancher officiel du dossier, au meme titre que la
   moyenne de segment de a43 ?** Il en a toutes les proprietes : zero appel, une ligne, et il
   bat le predicteur primaire sur la quantite de verdict. Si oui, il faut le passer aussi sur
   Twin et sur les conditions de Stanford, ce qui est le verrou cinq de `MODELE-DU-MONDE`
   10.5 transpose au changement.

4. **Que fait on du fait que la chute sous permutation d'un temoin de segment estime hors pli
   est negative ?** Elle vaut moins 0,0385 ici, et elle est parfaitement explicable. Mais si
   la mesure devient une quantite de verdict preenregistree, comme le demande le verrou trois,
   il faut fixer d'avance la convention : la lit on brute, ou la centre t on sur la valeur du
   temoin de segment ? La seconde option rendrait la quantite comparable d'un dispositif a
   l'autre, la premiere garde la definition de a44. Je n'ai pas tranche.

5. **L'axe economique de a30 est il assez bon pour porter un verdict negatif sur I2 ?** Il
   est ampute de cinq items, il se reduit a la batterie de depenses publiques et a l'impot,
   et sa correlation avec le changement est de 0,006. Le verdict « les cross presses ne sont
   pas les persuadables » peut etre un verdict sur l'instrument. Le panel GSS contient
   `eqwlth`, `helppoor`, `helpsick` et `helpnot` hors du sous ensemble de Stanford ; les
   reconstruire pour les seuls humains coute une demi journee et rendrait le verdict
   defendable, au prix de ne plus pouvoir comparer aux agents sur les memes items.

6. **`marhomo` manque au noyau commun.** C'est l'item que `BRAINSTORM-IMPACT` designe pour I1
   et pour I8. Accepte t on un second perimetre, les trois panels de 2006 a 2014 seulement,
   pour les items a mouvement documente qui n'existent pas dans le panel 2016-2020 ? Cela
   ferait un tableau de plus et une exception de perimetre a declarer.

7. **Le resultat de la section 3.5 vaut il un enonce a part dans le papier ?** « La direction
   du changement d'opinion individuel est une consequence comptable de la derive agregee »
   est un enonce sur les humains, verifiable par n'importe qui avec un panel, et il rend
   caduque toute evaluation d'un simulateur sur le sens du changement. Il n'est pas dans le
   dossier, il ne coute rien, et il est peut etre plus solide que tout ce qui porte sur les
   agents. Je ne sais pas s'il est nouveau : la decomposition brut contre net du changement
   est classique en demographie et en analyse de panel, et je n'ai pas fait de recherche
   d'anteriorite.
