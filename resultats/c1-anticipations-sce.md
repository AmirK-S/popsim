# C1. Les anticipations des menages americains : la dispersion, le plancher de reinterrogation, et la personne au dela de la cohorte

Rapport du 8 septembre 2026, nuit. Il execute le **mois 1 du programme C, version menages**
(`MOONSHOTS.md` section 3, programme C ; `brainstorm/03-economie-entreprises.md` M4), cote
humain, sur les microdonnees du Survey of Consumer Expectations de la Federal Reserve Bank
of New York.

**Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Aucun script
existant n'a ete modifie** ; `a44_commun.py` (permutation des personnes a l'interieur du
segment, Holm, Benjamini-Hochberg, dispersion Gini-Simpson a biais corrige), `a2_commun.py`
(regle de bootstrap sur les unites) et `i1_commun.py` (AUC de Mann-Whitney) sont importes
tels quels. Sept scripts nouveaux : `analyses/c1_commun.py`, `c1_decrire.py`,
`c1_dispersion.py`, `c1_stabilite.py`, `c1_previsibilite.py`, `c1_cibles.py`,
`c1_figures.py`.

**Le preenregistrement est `resultats/c1-preenregistrement.md`, ecrit le 8 septembre 2026 a
22 h 30 CEST (20 h 30 UTC), depot a `d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant
l'ecriture du premier script d'analyse et avant tout calcul statistique.** Sa section 0 dit
exactement ce qui avait ete regarde avant de l'ecrire : la ligne d'entete des fichiers, le
questionnaire du module central, et trois lignes brutes. Aucune statistique. Les douze
variables, les cohortes, les quatre quantites, les six predictions et les quatre controles
bloquants y sont figes.

**Une modification d'environnement, declaree** : `openpyxl` 3.1.5 a ete installe dans le
`.venv` pour lire les fichiers `.xlsx` de la Fed de New York. C'est la seule.

**Pour refaire le calcul**, dans cet ordre : `c1_decrire.py`, `c1_dispersion.py`,
`c1_stabilite.py`, `c1_previsibilite.py`, `c1_cibles.py`, `c1_figures.py`. Le troisieme et le
quatrieme durent une vingtaine de minutes chacun ; `c1_previsibilite.py` accepte une liste de
variables en argument et met en cache ses lignes par variable, puis `c1_previsibilite.py
assembler` recompose les tableaux et applique la correction pour tests multiples. La lecture
des fichiers Excel est mise en cache hors du depot, dans le repertoire temporaire, jamais dans
`data/` ni dans `resultats/`.

Sorties : `c1-controles.csv`, `c1-recouvrement-identifiants.csv`, `c1-structure-panel.csv`,
`c1-duree-participation.csv`, `c1-variables.csv`, `c1-demographies.csv`, `c1-cohortes.csv`,
`c1-couverture-mensuelle.csv`, `c1-dispersion-mensuelle.csv`, `c1-choc-2025.csv`,
`c1-avant-apres-choc.csv`, `c1-avant-apres-choc-detail.csv`, `c1-dispersion-ordinales.csv`,
`c1-dispersion-cohortes-alternatives.csv`, `c1-retest-par-delai.csv`, `c1-part-stable.csv`,
`c1-previsibilite-synthese.csv`, `c1-previsibilite-par-variable.csv`,
`c1-qui-bouge-choc.csv`, `c1-nul-a-derive.csv`, `c1-cibles-jumeau.csv`,
`c1-figure-dispersion-mensuelle.png` et `.svg`, `c1-figure-chute-permutation.png` et
`.svg`. Aucune microdonnee n'est ecrite.

Mention de source imposee par la licence FRBNY : *Source: Survey of Consumer Expectations,
(c) 2013-26 Federal Reserve Bank of New York (FRBNY). The SCE data are available without
charge at www.newyorkfed.org and may be used subject to license terms posted there. FRBNY
disclaims any responsibility or legal liability for this analysis and interpretation of
Survey of Consumer Expectations data.*

---

## Reponse en une ligne

**Le desaccord des menages americains sur l'inflation est presque entierement a l'interieur
des cohortes, et il appartient aux personnes.** Sur 70 mois, 82 535 observations et 10 974
menages, la part de la dispersion des anticipations d'inflation a un an qui separe les
cohortes age x diplome x revenu vaut **0,019 en mediane mensuelle, et ne depasse jamais
0,048** ; les 98 pour cent restants sont a l'interieur des cellules. [MESURE] Un gabarit qui
reproduit les moyennes de cohorte rend donc a une banque centrale la seule chose qu'elle a
deja et perd la totalite de ce qu'elle cherche.

**Et ce qui reste dans la cellule n'est pas du bruit.** Un menage reinterroge un mois plus
tard redonne une anticipation correlee a **0,659** a la sienne, moyennes de mois retirees, et
la part stable de la dispersion inter menages, estimee sans biais par analyse de variance,
vaut **0,525** [0,510 ; 0,539]. **La moitie du desaccord est de la vraie heterogeneite de
menage.** [MESURE]

**La personne bat la cohorte de deux ordres de grandeur, et elle est presque entierement
faite de sa propre reponse precedente.** Predire l'anticipation d'inflation du mois suivant
donne un Spearman de 0,681 pour l'historique du menage contre 0,077 pour les demographies
seules ; la chute sous permutation des menages a l'interieur du couple (mois, cohorte),
quantite de verdict preenregistree, vaut **0,639** pour l'historique et **0,003** pour les
demographies. Mais la persistance seule, `x(i, t)`, une ligne de code et zero appel, obtient
**0,615**, soit **96 pour cent** de ce que la foret va chercher. [MESURE] **C'est le resultat
de i1, transporte du changement d'opinion aux anticipations macroeconomiques et amplifie :
ce qui est previsible n'est pas la personne, c'est sa reponse precedente.**

**Au choc de 2025, l'ampleur de la revision est previsible, sa direction ne l'est pas au dela
du retour a la moyenne, et le nul a derive de i1 tient.** Qui revise fortement son
anticipation se predit a partir de son historique, AUC 0,809, chute 0,287, dont la moitie par
la seule volatilite passee du menage, chute 0,140 ; les demographies donnent **moins 0,032**,
c'est a dire rien. La direction, elle, est captee integralement par le niveau d'avant le
choc, chute 0,150 contre 0,124 pour l'historique complet : **c'est du retour a la moyenne,
pas de la connaissance des personnes.** Et la part de revisions qui vont dans le sens de la
derive agregee, 0,562, est reproduite a 1,6 point pres par un nul qui conserve les deux
distributions marginales et la derive par cohorte et detruit l'appariement des menages,
0,546. [MESURE]

**Le fait le plus utile a un jumeau est ailleurs, et il est simple** : ce meme nul a derive
produit des revisions **deux fois trop grandes**. Les menages reels bougent en moyenne de
2,37 points, les menages remelanges de 5,50, soit un rapport de **0,43**. [MESURE] Une
population simulee qui reproduit la moyenne et la dispersion par cohorte mais pas
l'appariement des personnes fera bouger ses menages deux fois trop.

---

## 1. Les controles bloquants, executes avant toute lecture

[MESURE, `c1-controles.csv`]

| controle | attendu | obtenu | passe |
|---|---|---|---|
| C1, observations 2020-2024 | 71 976 | **71 976** | oui |
| C1, `userid` distincts 2020-2024 | 9 751 | **9 751** | oui |
| C1, doublons `(date, userid)` 2020-2024 | 0 | **0** | oui |
| C1, observations 2025 | 10 559 | **10 559** | oui |
| C1, `userid` distincts 2025 | 2 159 | **2 159** | oui |
| C1, doublons 2025 | 0 | 0 | oui |
| C1, observations 2017-2019 | 47 681 | **47 681** | oui |
| C1, `userid` distincts 2017-2019 | 7 379 | **7 379** | oui |
| C1, doublons 2017-2019 | 0 | 0 | oui |
| C3, chute du temoin `T0b` | 0 exactement | **0,000000 sur les neuf variables** | oui |
| C4, cent menages par mois et par variable | tous les mois | **tous, sur les sept primaires** | oui |
| C4, trois cents menages des deux cotes du choc | oui | **640 a 1 049 selon la variable** | oui |
| C5, le signe est deja porte par la colonne d'amplitude | 1,0 / 1,0 | **1,0000 / 1,0000 sur les cinq variables** | oui |
| C6, permutation identique a `a44_commun` | identique | **identique, 200, 5 000 et 60 000 lignes** | oui |

La chaine de lecture reproduit a l'unite les quatre comptes que la session D1 avait mesures
en lisant directement le XML des feuilles, sans openpyxl et sans passer par les memes
fonctions. C'est le controle qui autorise tout le reste.

**Le controle C2 n'avait pas de seuil et il rapporte un fait neuf.** Il demandait si les
identifiants de menage sont stables d'un fichier a l'autre, ce que `PROVENANCE.md` et la
lettre `demandes/02-frbny-sce.md` listaient comme non verifie. Reponse :

[MESURE, `c1-recouvrement-identifiants.csv`]

| paire de fichiers | menages du premier | du second | communs | part du second |
|---|---|---|---|---|
| 2017-2019 et 2020-2024 | 7 379 | 9 751 | **1 212** | 0,124 |
| 2020-2024 et 2025 | 9 751 | 2 159 | **936** | **0,434** |
| 2017-2019 et 2025 | 7 379 | 2 159 | **0** | 0,000 |

Sur les 936 menages recoupes au raccord de decembre 2024 et janvier 2025, **la categorie
d'age et la categorie de diplome coincident dans 100,0 pour cent des cas**. [MESURE]
**Les identifiants sont donc stables d'un fichier a l'autre**, et le zero de la troisieme
ligne n'est pas une incoherence : il est ce que la regle du panel impose, un menage ne reste
pas douze mois dans la SCE et six ans dans le fichier. La lettre 02 peut retirer sa question
de jointure ; elle garde ses autres points.

**Deux controles ont ete ajoutes apres le preenregistrement, C5 et C6.** C5 est une
correction de fait, expliquee en section 10 : le questionnaire decrit une direction et une
amplitude positive, mais **le fichier public livre l'amplitude deja signee**. La suivre
aveuglement aurait retourne le signe de cinq variables sur douze. C6 verifie que
l'implementation rapide de la permutation tire exactement la meme permutation que
`a44_commun.permuter_intra` a graine egale, ce qui autorise a l'utiliser sans changer la
definition.

---

## 2. Protocole, en clair

**Les donnees.** `frbny-sce-public-microdata-20-24.xlsx` et
`frbny-sce-public-microdata-latest.xlsx`, soit **janvier 2020 a octobre 2025, 70 mois,
82 535 observations, 10 974 menages**. Le fichier 2017-2019 est ouvert en descriptif
seulement, pour la trajectoire d'avant 2020 et pour le controle C2. Le fichier 2013-2016
n'est pas ouvert.

**L'unite.** Le menage, `userid`. **Tous les intervalles de confiance publies sont des
bootstrap sur les menages**, jamais sur les couples menage-mois, selon la regle de
`a2_commun.bootstrap_personnes`.

**Les cohortes.** `_AGE_CAT` x `_EDU_CAT` x `_HH_INC_CAT`, les trois variables que la mission
nomme, telles que la FRBNY les code, avec une cellule « non renseigne » tenue a part et
jamais fusionnee. **48 cohortes observees, dont 27 pleines**, qui portent 98,6 pour cent des
observations ; **36 cohortes en moyenne par mois**, effectif median d'une cellule mois par
cohorte **24 menages**. Sous cinq menages, une cellule est repliee sur une cohorte
residuelle, seuil `N_MIN_SEGMENT` de `a44_commun`.

**Les valeurs extremes.** Les mesures robustes, ecart interquartile et ecart median absolu,
sont calculees sur les valeurs brutes. La variance et toutes les regressions passent par une
winsorisation **aux 2e et 98e centiles de la distribution mise en commun sur les 70 mois**,
bornes calculees une fois par variable et appliquees a l'identique a tous les mois, publiees
dans `c1-variables.csv`. Les probabilites subjectives, bornees a 0 et 100 par construction,
ne sont pas winsorisees. La regle etait figee avant de voir une distribution ; elle n'etait
pas superflue, `revenu` monte a 10 000 pour cent et descend a moins 400.

**La decomposition inter et intra cohorte.** Pour une variable continue et un mois, l'intra
est la variance intra ponderee sans biais, l'inter est la variance ponderee des moyennes de
cohorte **moins le terme que l'echantillonnage fini ajoute mecaniquement**,
`somme_g w_g (1 - w_g) s_g^2 / n_g`. C'est la transposition au continu de la logique des
estimateurs Gini-Simpson a biais corrige de a1 et a35. **Sans cette correction, une cohorte
de vingt-quatre menages fabrique de la difference entre cohortes qui n'existe pas.** La
correction peut rendre la part inter negative ; elle est alors publiee negative et lue comme
nulle. Pour les deux variables ordinales, c'est `a44_commun.dispersion`, le Gini-Simpson,
qui est appele, sans une ligne reimplementee.

**La quantite de verdict.** La chute sous permutation des menages **a l'interieur du couple
(mois cible, cohorte)**, 200 permutations par variable et par predicteur. Ce qui est conserve
est le mois et la cohorte ; ce qui est detruit est ce qui distingue un menage d'un autre dans
la meme cohorte le meme mois. **Le mois est donne a tous les predicteurs**, sous son index et
sa moyenne : la tendance agregee est offerte a chacun, exactement comme le nul a derive la
donne a tout le monde, et seule la prediction a l'interieur du mois et de la cohorte est
notee.

**La correction pour tests multiples.** Le `p` de permutation par approximation normale de la
loi de permutation porte la correction de Holm sur la famille des variables fois predicteurs ;
Benjamini-Hochberg et le `p` empirique sont publies a cote. **La lecon E4 de i1 a ete
appliquee d'avance** : avec 200 permutations le `p` empirique est plancher a 1/201, ce qui
rend Holm structurellement incapable de retenir quoi que ce soit sur une grande famille.

---

## 3. Q1. Ce qu'est ce panel, et ce qu'il n'a pas

### 3.1 La structure

[MESURE, `c1-structure-panel.csv`, `c1-duree-participation.csv`]

| perimetre | observations | menages | mois | periode | vagues par menage | menages par mois | `tenure` |
|---|---|---|---|---|---|---|---|
| 2017-2019, descriptif | 47 681 | 7 379 | 36 | 2017-01 a 2019-12 | 6,46 | 1 324 | 1 a 12 |
| 2020-2024 | 71 976 | 9 751 | 60 | 2020-01 a 2024-12 | 7,38 | 1 200 | 1 a **16** |
| 2025 | 10 559 | 2 159 | 10 | 2025-01 a 2025-10 | 4,89 | 1 056 | 1 a 13 |
| **primaire 2020-2025** | **82 535** | **10 974** | **70** | 2020-01 a 2025-10 | **7,52** | **1 179** | 1 a 16 |

La duree de participation n'est pas uniforme et sa forme compte pour tout ce qui suit :

| mois de participation | 1 | 2 a 5 | 6 a 11 | **12** | 13 | 14 |
|---|---|---|---|---|---|---|
| menages | **1 662** | 2 616 | 2 894 | **3 119** | 614 | 69 |
| part | 15,1 % | 23,8 % | 26,4 % | **28,4 %** | 5,6 % | 0,6 % |

**Le panel est bimodal** : un menage sur sept ne repond qu'une fois, plus d'un sur quatre
fait les douze mois complets. La mediane est de neuf mois. **Les 683 menages a treize ou
quatorze mois, et les valeurs de `tenure` jusqu'a 16, sont un fait a signaler** : le
protocole annonce douze mois, le fichier en contient davantage pour une minorite, sans que la
page de la SCE le documente. Cela ne change aucun resultat, tout est calcule sur des couples
observes.

### 3.2 Les variables d'anticipation retenues

[MESURE, `c1-variables.csv`, perimetre primaire]

| cle | source | ce que c'est | observations | part renseignee | mediane | bornes de winsorisation |
|---|---|---|---|---|---|---|
| `infl1` | `Q9_mean` | inflation a un an, moyenne de la densite subjective | 81 183 | 0,984 | 3,57 | [-4,91 ; 25,00] |
| `infl3` | `Q9c_mean` | inflation a trois ans, moyenne de la densite | 81 178 | 0,984 | 3,00 | [-7,10 ; 25,00] |
| `revenu` | `Q25v2part2` | croissance attendue du revenu du menage, en pour cent | 82 349 | 0,998 | 3,00 | [-30,0 ; 50,0] |
| `depense` | `Q26v2part2` | croissance attendue de la depense du menage | 82 392 | 0,998 | 5,00 | [-30,0 ; 50,0] |
| `logement` | `Q31v2part2` | variation attendue du prix du logement au niveau national | 82 372 | 0,998 | 5,00 | [-20,0 ; 44,0] |
| `perte_emploi` | `Q13new` | probabilite subjective de perdre son emploi principal | **50 530** | **0,612** | 5,00 | [0 ; 100] |
| `chomage` | `Q4new` | probabilite subjective que le chomage augmente | 82 482 | 0,999 | 40,00 | [0 ; 100] |
| `infl1_var` | `Q9_var` | incertitude individuelle, variance de la densite | 81 183 | 0,984 | 4,86 | [0,33 ; 133,7] |
| `infl1_iqr` | `Q9_iqr` | incertitude individuelle, IQR de la densite | 81 183 | 0,984 | 3,26 | [0,84 ; 18,36] |
| `infl1_point` | `Q8v2part2` | prevision ponctuelle d'inflation a un an | 82 239 | 0,996 | 5,00 | [-20,0 ; 50,0] |
| `fin_avant` | `Q1` | ordinale a 5 points, situation financiere depuis douze mois | 82 467 | 0,999 | 3 | ordinale |
| `fin_apres` | `Q2` | ordinale a 5 points, situation financiere attendue | 82 477 | 0,999 | 3 | ordinale |

Deux remarques que le tableau impose. **Un**, la couverture est presque parfaite pour tout
sauf `perte_emploi`, qui n'est posee qu'aux salaries non independants ayant un emploi : 61
pour cent des observations, 7 258 menages sur 10 974, et **ce sous ensemble est conditionne
sur une variable qui bouge avec le cycle**. Toute lecture de `perte_emploi` est une lecture
conditionnelle a l'emploi. **Deux**, la SCE publie **la distribution subjective complete par
personne et par mois**, dix bacs de probabilite, trois quartiles, variance et ecart
interquartile, a un an, a trois ans et a cinq ans. C'est ce qui rend le jeu superieur au
Michigan pour le programme C : on ne mesure pas seulement le desaccord entre menages, on
mesure aussi l'incertitude a l'interieur de la tete de chaque menage, `infl1_var`, et ce sont
deux quantites differentes qui bougent differemment.

Le module publie aussi ce qui n'est pas retenu ici et existe : depense de consommation par
poste, taxes, acces au credit, probabilite de defaut sur une dette, prix du logement en
distribution complete `C1_*` pour les repondants repetes, mobilite residentielle, recherche
d'emploi, taux d'interet et prix des actions, et une batterie de numeratie.

### 3.3 Les demographies, et ce qui manque

[MESURE, `c1-demographies.csv`]

| variable | niveaux | couverture |
|---|---|---|
| `_AGE_CAT` | 3 : moins de 40, 40 a 60, plus de 60 | toutes les observations |
| `_EDU_CAT` | 3 : lycee, quelques annees d'universite, diplome | toutes |
| `_HH_INC_CAT` | 3 : moins de 50 k, 50 a 100 k, plus de 100 k | toutes |
| `_REGION_CAT` | 4 : Midwest, Northeast, South, West | toutes |
| `_NUM_CAT` | 2 : numeratie haute, basse | toutes |
| `_STATE` | 52 | presque toutes |
| `tenure`, `weight` | rang de vague, poids de redressement | toutes |
| `Q33`, sexe | 2 | **9 754 menages sur 10 974**, poses aux nouveaux repondants |
| `Q36`, diplome detaille | 9 | 9 759 menages |
| `Q47`, revenu detaille | 11 | 9 698 menages |

**Le module central de la SCE ne contient ni parti, ni ideologie, ni intention de vote.** Le
questionnaire a ete lu en entier ; il n'y a pas une question politique. C'est une difference
de nature avec le GSS et l'ANES, sur lesquels tout le reste du dossier repose : **la
segmentation par camp, qui porte a1, a30, a37, a38, i1 et i3, est impossible ici**. La
cohorte de la SCE est economique et demographique, jamais politique. Ce n'est pas une lacune
de notre traitement, c'est une propriete de l'instrument, et elle ferme d'avance toute
tentative de transporter ici la lecture par camps.

Le sexe existe mais au niveau du menage et pour 89 pour cent d'entre eux seulement, parce que
`Q33` n'est pose qu'aux nouveaux repondants ; les repondants repetes ne le redonnent pas. Il
n'entre donc pas dans la cohorte primaire.

---

## 4. Q2. La dispersion : quatre-vingt-dix-huit pour cent du desaccord est a l'interieur des cohortes

### 4.1 Le resultat central

[MESURE, `c1-dispersion-mensuelle.csv`, `c1-cibles-jumeau.csv`, panneau B de la figure 1]

Part de la dispersion inter menages qui separe les cohortes age x diplome x revenu, variance
corrigee du biais d'echantillonnage fini, sur les 70 mois du perimetre :

| variable | part inter, mediane | minimum | maximum | dispersion totale, IQR median |
|---|---|---|---|---|
| **`infl1`, inflation a un an** | **0,0193** | -0,0017 | **0,0480** | 4,79 points |
| `infl3`, inflation a trois ans | 0,0106 | -0,0117 | 0,0374 | 5,31 |
| `revenu` | 0,0196 | -0,0024 | 0,0525 | 5,00 |
| `depense` | 0,0056 | -0,0192 | 0,0309 | 8,00 |
| `logement` | 0,0369 | 0,0053 | 0,1125 | 9,00 |
| `perte_emploi` | 0,0103 | -0,0167 | 0,0506 | 14,00 |
| `chomage` | 0,0160 | -0,0044 | 0,0874 | 35,00 |
| `infl1_var`, incertitude individuelle | **0,1188** | 0,0546 | **0,1982** | 17,49 |
| `infl1_point` | 0,0537 | 0,0128 | 0,1328 | 6,00 |
| `fin_avant` et `fin_apres`, ordinales, Gini-Simpson | 0,0136 | 0,0025 | 0,0276 | -- |

**La prediction P1 est tenue et de loin** : elle demandait moins de 0,15 a tous les mois pour
`infl1`, le maximum sur 70 mois vaut 0,048. **Sur les sept variables primaires, le maximum
atteint sur les 70 mois vaut 0,113, une seule fois, sur le prix du logement.**

Ce n'est pas un effet du choix de cohorte. [MESURE, `c1-dispersion-cohortes-alternatives.csv`]

| segmentation | cohortes | part inter mediane de `infl1` | plage sur les sept primaires |
|---|---|---|---|
| age x diplome x revenu, primaire | 26 | 0,0193 | 0,006 a 0,037 |
| age seul | 3 | 0,0029 | -0,001 a 0,017 |
| diplome x revenu | 11 | 0,0133 | 0,002 a 0,038 |
| region | 4 | 0,0004 | -0,000 a 0,003 |

**Plus la segmentation est fine, plus la part inter monte, et elle plafonne a 4 pour cent.**
C'est le comportement attendu si la difference entre cohortes est faible et si l'estimateur
est correctement debiaise : ajouter des cellules ne fabrique pas de difference.

**La seule variable ou la cohorte dit quelque chose est l'incertitude individuelle**,
`infl1_var`, part inter 0,119 en mediane et 0,198 au maximum, en hausse continue depuis 2020.
[MESURE, panneau B] Autrement dit : les cohortes ne different pas sur **ce qu'elles
anticipent**, elles different sur **a quel point elles en sont sures**, et cet ecart grandit.
C'est le seul endroit du rapport ou un gabarit de cohorte aurait quelque chose a rendre.

### 4.2 La trajectoire 2020-2025

[MESURE, panneau A de la figure 1]

La dispersion de `infl1`, ecart interquartile entre menages, part de **2,37 points en janvier
2020**, saute a 5,91 en avril 2020, monte jusqu'a **6,72 en septembre 2022**, redescend a 3,93
en fevrier 2024, et remonte a **5,77 en avril 2025**. La moyenne suit le meme profil avec un
retard : 3,23 en fevrier 2020, **7,50 en juin 2022**, 3,68 en octobre 2024, **5,36 en avril
2025**. La mediane des ecarts interquartiles a l'interieur des cohortes suit la dispersion
totale de tres pres, ecart relatif median de plus 2,2 pour cent et compris entre moins 15 et
plus 24 pour cent selon le mois ; l'ecart interquartile des medianes de cohorte, lui, reste
entre **0,26 et 2,13 points**, c'est a dire au plus le tiers de la dispersion totale, et le
plus souvent le cinquieme.

Sur la fenetre descriptive 2017-2019, la meme mesure vaut 2,4 a 3,5 points et sa part inter
cohortes n'est pas mesurable ici, faute d'avoir recalcule les cohortes sur cette periode avec
les memes bornes de winsorisation issues du perimetre primaire ; le panneau A l'affiche en
grise et rien n'en est conclu.

### 4.3 Le choc de 2025 : la regle preenregistree designe un mois, la regle secondaire en designe un autre

[MESURE, `c1-choc-2025.csv`]

La regle primaire, ecrite avant tout calcul, etait : le mois de janvier a octobre 2025 qui
maximise la valeur absolue du saut de la moyenne de `infl1`. La regle secondaire : le mois
qui maximise la valeur absolue du saut de l'ecart interquartile.

| mois 2025 | 01 | 02 | 03 | **04** | 05 | **06** | 07 | 08 | 09 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| moyenne | 4,36 | 4,79 | 4,93 | **5,36** | 5,11 | **4,49** | 4,67 | 4,77 | 4,65 | 4,53 |
| saut de moyenne | +0,17 | +0,43 | +0,15 | **+0,43** | -0,25 | **-0,62** | +0,18 | +0,10 | -0,12 | -0,12 |
| IQR | 5,46 | 5,13 | 5,06 | **5,77** | 5,49 | 4,81 | 4,55 | 4,66 | 4,26 | 4,53 |
| saut d'IQR | +0,26 | -0,34 | -0,07 | **+0,72** | -0,28 | -0,68 | -0,26 | +0,11 | -0,40 | +0,27 |

**La regle primaire designe juin 2025, la regle secondaire designe avril 2025.** La
prediction P2 disait avril ou mai : **elle est fausse pour la regle qui porte le verdict, et
juste pour la regle secondaire.**

Il faut dire pourquoi, parce que c'est une lecon de methode. La regle primaire prenait une
valeur absolue ; le plus grand mouvement mensuel de la fenetre n'est pas la montee mais **le
retournement**, moins 0,62 point en juin. La montee, elle, s'est faite en trois mois, de
+0,17 en janvier a +0,43 en avril, pour un total de **plus 1,17 point depuis decembre 2024**,
et aucun mois pris isolement ne bat le retournement de juin. **Une regle de saut mensuel
maximal ne trouve pas un episode qui dure un trimestre ; elle trouve sa fin.** Le
preenregistrement n'a pas ete modifie : **tout ce qui suit est publie sous les deux regles**,
la primaire porte le verdict, la secondaire est publiee entierement a cote et jamais
substituee.

### 4.4 Ce que le choc fait a la dispersion

[MESURE, `c1-avant-apres-choc.csv`, panneau C de la figure 1. Fenetre avant : les trois mois
qui precedent ; fenetre apres : le mois du choc et les deux suivants]

| variable | regle primaire, choc 2025-06 | | regle secondaire, choc 2025-04 | |
|---|---|---|---|---|
| | delta moyenne | rapport d'IQR | delta moyenne | rapport d'IQR |
| `infl1` | -0,50 | **0,858** | +0,29 | 1,017 |
| `infl3` | -0,47 | 0,959 | +0,20 | 0,929 |
| `revenu` | +0,43 | 1,000 | -0,56 | 1,000 |
| `depense` | -0,29 | 1,000 | -0,09 | 1,000 |
| `logement` | -0,26 | 1,125 | -0,16 | 1,125 |
| `perte_emploi` | -1,43 | 1,056 | +0,45 | 0,947 |
| `chomage` | -3,94 | 0,920 | +2,98 | **1,163** |
| `infl1_var` | -2,12 | 0,778 | -0,86 | 0,907 |
| `infl1_point` | -0,57 | 0,750 | +1,53 | **1,333** |

**La prediction P3 est fausse.** Elle annoncait une hausse d'au moins 10 pour cent de l'ecart
interquartile de `infl1` entre les deux fenetres. Sous la regle primaire il **baisse** de
14 pour cent, ce qui est coherent puisque la regle a designe le retournement ; sous la regle
secondaire il monte de 1,7 pour cent seulement. La seconde moitie de P3, « la dispersion
monte plus que la part inter cohortes », n'est donc pas evaluable dans le sens ou elle etait
ecrite.

Deux choses meritent d'etre notees quand meme. **Un**, sous la regle secondaire, ce qui monte
franchement est la **prevision ponctuelle**, plus 33 pour cent d'IQR, et la **probabilite de
hausse du chomage**, plus 16 pour cent, pendant que la moyenne de la densite, `infl1`, ne
bouge presque pas. La question ponctuelle et la question de densite ne reagissent pas de la
meme facon au meme evenement, et un jumeau qui n'en simulerait qu'une le manquerait. **Deux**,
`revenu` et `depense` affichent un rapport d'IQR exactement egal a 1,000 : leurs ecarts
interquartiles valent 4 et 8 points dans les deux fenetres, parce que les repondants donnent
des nombres ronds et que l'IQR d'une variable a forte granularite est un mauvais instrument
de variation fine. Pour ces deux variables, c'est la variance qui bouge, de 0,92 et 0,90
respectivement, et c'est elle qu'il faut lire.

---

## 5. Q3. Le plancher de reinterrogation : la moitie du desaccord est stable

### 5.1 La courbe de retest, onze delais

[MESURE, `c1-retest-par-delai.csv`, panneau C de la figure 2. Correlation de Spearman entre
`x(i, t)` et `x(i, t + k)`, **moyennes de mois retirees de chaque cote** pour que la derive
agregee n'alimente pas la correlation. Bootstrap sur les menages, 200 tirages.]

| delai, mois | 1 | 2 | 3 | 6 | 9 | 11 | couples a un mois |
|---|---|---|---|---|---|---|---|
| `infl1` | **0,659** | 0,612 | 0,575 | 0,488 | 0,370 | **0,280** | 66 292 |
| `infl3` | 0,615 | 0,579 | 0,547 | 0,469 | 0,360 | 0,290 | 66 301 |
| `revenu` | 0,608 | 0,554 | 0,523 | 0,439 | 0,385 | 0,376 | 67 667 |
| `depense` | 0,514 | 0,476 | 0,445 | 0,382 | 0,316 | 0,264 | 67 718 |
| `logement` | 0,594 | 0,543 | 0,498 | 0,414 | 0,336 | 0,299 | 67 698 |
| `perte_emploi` | **0,729** | 0,693 | 0,667 | 0,608 | 0,547 | **0,513** | 40 037 |
| `chomage` | 0,599 | 0,549 | 0,512 | 0,429 | 0,326 | 0,241 | 67 826 |
| `infl1_var` | 0,691 | 0,654 | 0,624 | 0,541 | 0,448 | 0,358 | 66 292 |
| `infl1_point` | 0,633 | 0,586 | 0,542 | 0,462 | 0,359 | 0,292 | 67 529 |

C'est le plancher de reinterrogation que le dossier reclamait, gratuit, sur les memes
menages, a onze delais au lieu des trois de a12. **Il ne plafonne pas.** La correlation decroit
regulierement du premier au onzieme mois, sans palier visible : `infl1` passe de 0,659 a
0,280. **Une part de ce qui ressemble a un trait de menage est donc une composante lente qui
s'efface, pas une propriete fixe.** Une seule variable a un palier net, `perte_emploi`, qui
tient 0,51 a onze mois ; c'est aussi la seule qui porte sur la situation propre du repondant
et non sur l'economie.

### 5.2 La part stable

[MESURE, `c1-part-stable.csv`. Decomposition d'analyse de variance a un facteur aleatoire sur
les valeurs centrees par mois, menages a trois observations ou plus, estimateur sans biais.
Bootstrap sur les menages, 200 tirages.]

| variable | menages | `sigma2` entre | `sigma2` intra | **part stable** | IC 95 pour cent | verification pairs / impairs ramenee |
|---|---|---|---|---|---|---|
| `infl1` | 8 337 | 16,51 | 14,92 | **0,525** | [0,510 ; 0,539] | 0,485 |
| `infl3` | 8 336 | 15,77 | 16,06 | 0,495 | [0,477 ; 0,514] | 0,445 |
| `revenu` | 8 392 | 72,76 | 84,68 | 0,462 | [0,444 ; 0,483] | 0,407 |
| `depense` | 8 395 | 54,81 | 97,16 | **0,361** | [0,344 ; 0,381] | 0,329 |
| `logement` | 8 396 | 58,06 | 62,30 | 0,482 | [0,465 ; 0,499] | 0,428 |
| `perte_emploi` | 5 396 | 193,75 | 152,84 | **0,559** | [0,541 ; 0,580] | 0,517 |
| `chomage` | 8 398 | 287,76 | 316,05 | 0,477 | [0,464 ; 0,487] | 0,453 |
| `infl1_var` | 8 337 | 524,40 | 326,72 | **0,616** | [0,600 ; 0,630] | 0,449 |
| `infl1_point` | 8 391 | 60,52 | 69,51 | 0,465 | [0,447 ; 0,483] | 0,407 |

**La prediction P4 est tenue** : elle annoncait la part stable de `infl1` entre 0,25 et 0,55,
elle vaut 0,525, dans la fourchette et pres de sa borne haute.

**Lu en clair : entre 36 et 62 pour cent de la dispersion inter menages est de la vraie
heterogeneite de menage, le reste est de la revision et du bruit de mesure.** C'est la reponse
directe a la question de la mission, et c'est le nombre qui decide si le programme C a un
objet : si la part stable avait ete sous 0,10, il n'y aurait aucune personne a reproduire et
le run simule aurait ete annule par la regle de decision 2. Elle est cinq fois au dessus.

La verification non circulaire, la correlation entre la moyenne du menage sur ses mois
impairs et sa moyenne sur ses mois pairs, donne 0,70 a 0,83 brute. Ramenee a une observation
isolee par la formule de Spearman et Brown, avec `k` proche de 4,7 mois par demi-echantillon,
elle donne les valeurs de la derniere colonne : **elles concordent avec l'analyse de variance
a moins de 0,06 pres pour huit variables sur neuf**. La neuvieme, `infl1_var`, s'ecarte de
0,17 ; son estimateur d'analyse de variance est probablement gonfle par sa forte asymetrie.
Le preenregistrement demandait de signaler tout ecart superieur a 0,10 : c'est fait, et il
n'y en a qu'un.

**Une reserve qui compte.** La decomposition d'analyse de variance suppose que le residu est
echangeable dans le temps ; la courbe de retest de la section 5.1 montre qu'il ne l'est pas,
puisqu'elle decroit. **La part stable de 0,525 est donc a lire comme une borne haute de la
composante permanente et une borne basse de ce qui est stable a un mois.** Les deux bornes
honnetes sont ecrites dans le tableau des cibles : le retest a un mois, 0,659, et le retest a
onze mois, 0,280.

---

## 6. Q4. La personne au dela de la cohorte

### 6.1 Predire l'anticipation du mois suivant

[MESURE, `c1-previsibilite-synthese.csv`, `c1-previsibilite-par-variable.csv`, panneaux A et
B de la figure 2. Neuf variables, 40 037 a 67 826 couples menage-mois consecutifs, cinq plis
sur les menages, scores hors pli, 200 permutations, bootstrap 400 tirages sur les menages.]

| predicteur | Spearman moyen | **chute moyenne** | chute min | chute max | variables retenues, Holm |
|---|---|---|---|---|---|
| **H, historique du menage** | 0,653 | **0,5960** | 0,520 | 0,707 | **9 / 9** |
| F, foret sur historique et demographies | 0,655 | 0,5923 | 0,526 | 0,695 | 9 / 9 |
| **P, persistance seule, `x(i, t)`** | 0,629 | **0,5770** | 0,489 | 0,689 | **9 / 9** |
| HD, historique et demographies | 0,645 | 0,5752 | 0,514 | 0,701 | 9 / 9 |
| **D, demographies seules** | 0,134 | **0,0336** | -0,006 | 0,076 | 9 / 9 |
| T0b, cohorte a plein echantillon | 0,205 | **0,0000** | 0,000 | 0,000 | 0 / 9 |
| T1, temoin de cohorte hors pli | 0,084 | **-0,0907** | -0,119 | -0,053 | 0 / 9 |

Trois lectures, dans l'ordre.

**Un. Il y a une personne, et elle ecrase la cohorte.** La chute sous permutation vaut 0,596
pour l'historique du menage contre 0,034 pour les demographies seules, sur les neuf
variables, avec des intervalles bootstrap qui ne se touchent pas. **La prediction P5, premiere
moitie, est tenue** : elle demandait un ecart d'au moins 0,05 point, il vaut 0,56.

**Deux. Cette personne est presque entierement sa reponse precedente.** `P`, qui ne connait
que `x(i, t)` et rien d'autre, obtient une chute de 0,577, soit **96,4 pour cent** de celle de
la foret. Variable par variable, le rapport va de 0,930 pour `depense` a 1,041 pour
`infl1_var`, ou la persistance **bat** la foret. **La prediction P5, seconde moitie, est tenue
et largement** : elle demandait 70 pour cent au moins. Ajouter la valeur du mois d'avant, la
moyenne et l'ecart type de l'historique, les cinq demographies et une foret de 200 arbres
rapporte **moins de deux centiemes de point** de chute, 0,0153 exactement.

C'est exactement le resultat de i1, en plus net. i1 disait, sur le changement d'opinion du
GSS entre deux vagues distantes de quatre ans : la chute de la foret vaut 0,1368, celle de la
position initiale seule 0,0974, soit 71 pour cent. **Ici, sur des anticipations
macroeconomiques a un mois d'intervalle, la proportion monte a 96 pour cent.** Le dossier
tient donc le meme fait sur deux jeux qui n'ont ni les memes personnes, ni le meme pays de
mesure, ni le meme format de reponse, ni la meme echelle de temps : **ce qui est previsible
chez une personne, c'est ce qu'elle a repondu la fois d'avant.**

**Trois. Le temoin de cohorte a une chute negative, et c'est la meme lecon de methode qu'en
i1.** `T1`, la moyenne de la cohorte au mois cible estimee hors pli, a une chute de -0,091 :
permuter les menages a l'interieur de leur cohorte **ameliore** son Spearman. Son score ne
varie a l'interieur d'une cohorte que parce qu'il est estime hors pli, et cette variation est
negativement correlee a la cible par construction. `T0b`, la meme moyenne estimee sur tout le
perimetre, donc rigoureusement constante dans le groupe de permutation, donne **0,000000 sur
les neuf variables** et verifie l'implementation. **La convention a retenir, deja formulee en
i1 section 4.3, est confirmee : la chute d'un predicteur constant par cohorte se lit comme
nulle, meme quand la validation croisee la rend negative.**

### 6.2 Qui bouge au choc

[MESURE, `c1-qui-bouge-choc.csv`, panneau D de la figure 2. Menages presents dans les trois
mois avant et les trois mois a partir du choc ; 640 a 1 049 selon la variable. Revision
`R(i)` = moyenne apres moins moyenne avant. `Y_rev` = 1 si `|R|` depasse sa mediane ; `Y_dir`
= 1 si `R > 0`. Foret hors pli, AUC de `i1_commun.auc`, 200 permutations intra cohorte,
bootstrap 400 tirages, Holm sur la famille entiere.]

**Ampleur de la revision, `Y_rev`, `infl1`, regle primaire, 1 037 menages, taux de base
0,4995 :**

| predicteur | AUC | AUC permutee | **chute** | IC 95 pour cent | Holm |
|---|---|---|---|---|---|
| **H, historique du menage** | **0,809** | 0,522 | **0,2867** | [0,238 ; 0,325] | retenu |
| HD, historique et demographies | 0,803 | 0,535 | 0,2680 | [0,228 ; 0,305] | retenu |
| **V, volatilite passee du menage seule** | 0,664 | 0,524 | **0,1401** | [0,093 ; 0,183] | retenu |
| N, ecart au niveau moyen | 0,568 | 0,515 | 0,0534 | [0,005 ; 0,101] | retenu |
| **D, demographies seules** | 0,553 | 0,585 | **-0,0322** | [-0,058 ; -0,010] | a lire comme nul |
| L, niveau d'avant, signe | 0,335 | 0,493 | -0,1580 | [-0,205 ; -0,097] | inverse, cf. ci dessous |
| T0b, temoin constant | 0,500 | 0,500 | 0,0000 | [0,000 ; 0,000] | -- |

Sur les neuf variables, la chute de `H` va de 0,164 a 0,374 et celle de `V` de 0,061 a 0,176,
soit **entre 37 et 66 pour cent de `H`, la moitie en mediane**. Les demographies seules
donnent une chute **negative sur sept variables sur neuf**, et inferieure a 0,02 sur les deux
autres.

**Lu en clair : qui revise fortement son anticipation au choc se predit, et la moitie de cette
prediction est la seule volatilite passee du menage.** C'est le transport exact du resultat
central de i1, « ce qui est previsible, c'est l'instabilite d'une reponse, pas la personne »,
a une variable continue et a un choc macroeconomique. **La cohorte, elle, ne dit rien du tout
sur qui revise.**

**Direction de la revision, `Y_dir`, `infl1`, regle primaire :**

| predicteur | AUC | chute | IC 95 pour cent |
|---|---|---|---|
| **L, niveau d'avant le choc, seul, signe** | 0,652 | **0,1500** | [0,095 ; 0,195] |
| H, historique du menage | 0,630 | 0,1238 | [0,075 ; 0,175] |
| V, volatilite passee seule | 0,488 | -0,0189 | [-0,070 ; 0,027] |
| D, demographies seules | 0,538 | -0,0257 | [-0,060 ; 0,011] |

**La prediction P6, premiere moitie, est fausse** : elle annoncait une chute non distinguable
de zero sur la direction, et la chute de `H` vaut 0,124, retenue par Holm sur les neuf
variables. Mais la lecture honnete est la deuxieme colonne : **le niveau d'avant le choc, tout
seul, atteint la chute de l'historique complet a moins de 0,027 pres sur les neuf variables,
et la depasse sur six d'entre elles** (0,150 contre 0,124 pour `infl1`, 0,173 contre 0,154
pour `infl3`, 0,198 contre 0,180 pour `revenu`). Le signe est celui du retour a la moyenne : qui anticipait haut revise vers le
bas. **La direction de la revision est donc previsible, et elle l'est integralement par le
retour a la moyenne sur sa propre valeur precedente, pas par une connaissance de la
personne.** La volatilite passee, qui explique la moitie de l'ampleur, n'explique rien de la
direction, chute -0,019.

### 6.3 Le nul a derive

[MESURE, `c1-nul-a-derive.csv`. Temoin : les valeurs de la fenetre apres sont remelangees
entre menages de la meme cohorte. Les deux distributions marginales, avant et apres, et la
derive par cohorte sont donc conservees ; seul l'appariement des menages est detruit. 50
replicats.]

| variable, regle primaire | derive agregee | part dans le sens de la derive, **observee** | **nul a derive** | exces | ampleur moyenne observee | **ampleur du nul** | **rapport** |
|---|---|---|---|---|---|---|---|
| `infl1` | -0,60 | 0,5622 | 0,5464 | **+0,016** | 2,37 | 5,50 | **0,431** |
| `infl3` | -0,51 | 0,5472 | 0,5312 | +0,016 | 2,35 | 5,50 | 0,427 |
| `revenu` | +0,41 | 0,4145 | 0,4903 | -0,076 | 5,23 | 10,96 | 0,477 |
| `depense` | -1,15 | 0,5248 | 0,5271 | -0,002 | 6,36 | 11,49 | 0,554 |
| `logement` | -0,69 | 0,5038 | 0,5156 | -0,012 | 4,94 | 9,80 | 0,504 |
| `perte_emploi` | -0,88 | 0,4875 | 0,4986 | -0,011 | 8,76 | 17,14 | 0,511 |
| `chomage` | -6,01 | 0,6187 | 0,5676 | +0,051 | 12,75 | 28,55 | 0,447 |
| `infl1_var` | -3,81 | 0,6162 | 0,5828 | +0,033 | 9,78 | 22,66 | 0,432 |
| `infl1_point` | -1,28 | 0,5368 | 0,5291 | +0,008 | 4,54 | 10,46 | 0,434 |

**La prediction P6, seconde moitie, est tenue pour `infl1`** : l'ecart entre la part observee
et la part du nul vaut 1,6 point, sous la borne de trois points annoncee. Sur les neuf
variables l'exces va de -7,6 a +5,1 points, positif cinq fois et negatif quatre fois, ce qui
est un tirage a pile ou face. **Le resultat de i1 se transporte : la part de mouvements qui
vont dans le sens de la derive agregee est ce qu'un nul sans structure individuelle produit
deja.**

**Mais la derniere colonne est le vrai resultat de cette section, et il est neuf.** Le nul a
derive conserve les deux marginales et detruit l'appariement des personnes ; il produit alors
des revisions **deux fois trop grandes**, 5,50 contre 2,37 points pour `infl1`, rapport 0,431.
Sur les neuf variables le rapport va de 0,427 a 0,554. **Autrement dit : ce qui distingue une
vraie population d'une population correctement calibree sur ses marges n'est pas la direction
du mouvement, c'est son ampleur.** Une population dont chaque menage est tire dans la loi de
sa cohorte a chaque mois bougerait deux fois trop entre deux mois. C'est une quantite de
verdict simple, elle ne demande aucun appel de modele, et elle est mesuree ici chez les
humains.

---

## 7. Q5. Ce que devrait battre une population simulee de menages

[MESURE, `c1-cibles-jumeau.csv`. Perimetre primaire, cohorte age x diplome x revenu, choc sous
la regle primaire.]

### 7.1 A reproduire

| variable | IQR median mensuel | **part inter cohortes** | **part stable** | retest 1 mois | retest 11 mois | rapport d'IQR au choc |
|---|---|---|---|---|---|---|
| `infl1` | 4,79 | **0,019** | **0,525** | 0,659 | 0,280 | 0,858 |
| `infl3` | 5,31 | 0,011 | 0,495 | 0,615 | 0,290 | 0,959 |
| `revenu` | 5,00 | 0,020 | 0,462 | 0,608 | 0,376 | 1,000 |
| `depense` | 8,00 | 0,006 | 0,361 | 0,514 | 0,264 | 1,000 |
| `logement` | 9,00 | 0,037 | 0,482 | 0,594 | 0,299 | 1,125 |
| `perte_emploi` | 14,00 | 0,010 | 0,559 | 0,729 | 0,513 | 1,056 |
| `chomage` | 35,00 | 0,016 | 0,477 | 0,599 | 0,241 | 0,920 |
| `infl1_var` | 17,49 | **0,119** | 0,616 | 0,691 | 0,358 | 0,778 |
| `infl1_point` | 6,00 | 0,054 | 0,465 | 0,633 | 0,292 | 0,750 |

Un gabarit de cohorte reproduit la premiere colonne sans effort, echoue sur la deuxieme **par
exces** puisqu'il met toute sa dispersion entre les cohortes, et echoue sur la troisieme **par
defaut** puisqu'il retire un menage neuf a chaque mois. Les deux colonnes de retest sont les
bornes honnetes de la troisieme, pour la raison ecrite en 5.2.

### 7.2 A depasser

| variable | **chute de `H`** | IC bas | **chute de `P`, le vrai adversaire** | chute de `F` | part de `F` captee par `P` |
|---|---|---|---|---|---|
| `infl1` | **0,639** | 0,633 | **0,615** | 0,638 | 0,964 |
| `infl3` | 0,614 | 0,606 | 0,582 | 0,616 | 0,944 |
| `revenu` | 0,569 | 0,561 | 0,559 | 0,562 | 0,996 |
| `depense` | 0,520 | 0,512 | 0,489 | 0,526 | 0,930 |
| `logement` | 0,555 | 0,547 | 0,534 | 0,550 | 0,971 |
| `perte_emploi` | 0,707 | 0,698 | 0,689 | 0,695 | 0,991 |
| `chomage` | 0,594 | 0,586 | 0,553 | 0,588 | 0,940 |
| `infl1_var` | 0,603 | 0,594 | 0,614 | 0,589 | 1,041 |
| `infl1_point` | 0,564 | 0,556 | 0,560 | 0,567 | 0,986 |

Et, sur le choc :

| variable | chute sur **qui revise**, `H` | dont **volatilite passee seule** | chute sur **la direction**, `H` | dont **niveau d'avant seul** |
|---|---|---|---|---|
| `infl1` | 0,287 | 0,140 | 0,124 | **0,150** |
| `infl3` | 0,238 | 0,120 | 0,154 | 0,173 |
| `revenu` | 0,280 | 0,174 | 0,180 | 0,198 |
| `depense` | 0,266 | 0,119 | 0,212 | 0,207 |
| `logement` | 0,240 | 0,110 | 0,232 | 0,237 |
| `perte_emploi` | 0,266 | 0,176 | 0,108 | 0,115 |
| `chomage` | 0,164 | 0,061 | 0,136 | 0,135 |
| `infl1_var` | 0,374 | 0,171 | 0,104 | 0,097 |
| `infl1_point` | 0,284 | 0,139 | 0,214 | 0,219 |

### 7.3 Les planchers

| plancher | valeur | comment le lire |
|---|---|---|
| **`T0b`, cohorte a plein echantillon** | **0,000000** sur les neuf variables | verification d'implementation ; une chute non nulle signale un bug, pas un resultat |
| **`T1`, cohorte hors pli** | -0,053 a -0,119 | **a lire comme nul**, jamais comme negatif ; c'est l'artefact de la validation croisee decrit en 6.1 |
| **`D`, demographies seules** | -0,006 a 0,076, moyenne **0,034** | ce qu'un gabarit de cohorte peut esperer sur l'anticipation du mois suivant |
| **`D` sur qui revise au choc** | -0,069 a 0,020 | ce qu'un gabarit de cohorte peut esperer sur qui bouge : **rien** |
| **le nul a derive, rapport d'ampleur** | 0,427 a 0,554 | une population sans appariement des personnes fait bouger ses menages **deux fois trop** |

**La barre du run simule, ecrite ici et a declarer avant le run :**

> Une population simulee de menages, evaluee sur les memes mois, les memes cohortes et la
> meme permutation, doit atteindre sur `infl1` une **chute superieure a 0,639** pour egaler
> l'historique du menage, et une **chute superieure a 0,615** pour battre la persistance
> seule, qui coute zero appel et une ligne de code. En dessous de **0,034**, elle ne fait pas
> mieux que les cinq demographies. En dessous de **0,000**, elle ne fait pas mieux qu'un
> gabarit de cohorte. Elle doit par ailleurs reproduire une part inter cohortes de **0,019**
> et non de 1, une part stable de **0,525** et non de 0, et un rapport entre l'ampleur de ses
> propres revisions au choc et celle de son propre nul a derive de **0,43**, comme les
> humains, et non de 1,00, qui est la valeur d'une population sans appariement des personnes.

---

## 8. Les figures

**`c1-figure-dispersion-mensuelle`**, trois panneaux. A, la dispersion de `infl1` mois par
mois de 2017 a 2025, totale, a l'interieur des cohortes et entre cohortes, avec la moyenne
pour situer et les deux mois de choc marques. B, la part inter cohortes des neuf variables sur
les 70 mois, avec la borne de la prediction P1. C, ce que le choc fait a l'ecart interquartile
de chaque variable, sous les deux regles.

Le panneau A porte le resultat central a l'oeil : la courbe de dispersion a l'interieur des
cohortes est colee a la courbe de dispersion totale, la courbe entre cohortes rampe au bas du
graphique. Une reserve de lecture : la mediane des ecarts interquartiles intra cohorte passe
parfois **au dessus** de l'ecart interquartile total. Ce n'est pas une incoherence, c'est du
bruit d'echantillonnage : un IQR estime sur une cellule de vingt-quatre menages est une
statistique tres dispersee, et la mediane de trente-six d'entre elles n'a aucune raison
d'etre bornee par l'IQR global. La decomposition de variance du panneau B, elle, est corrigee
du biais et ne souffre pas de ce defaut ; c'est elle qui porte le verdict.

**`c1-figure-chute-permutation`**, quatre panneaux. A, pour chaque predicteur, le Spearman
observe et le Spearman apres permutation ; la longueur du trait est la quantite de verdict.
B, la meme chute variable par variable pour `H`, `P` et `D`, avec les intervalles bootstrap.
C, la courbe de retest a onze delais et la part stable en pointilles. D, qui revise au choc,
ampleur contre direction.

---

## 9. Le score des six predictions ecrites avant le calcul

[MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | part inter cohortes de `infl1` sous 0,15 a tous les mois | **tenue**, maximum 0,048 sur 70 mois |
| **P2** | le mois du choc tombe en avril ou mai 2025 | **fausse pour la regle primaire**, qui designe juin 2025 ; **juste pour la regle secondaire**, qui designe avril |
| **P3** | l'IQR de `infl1` monte d'au moins 10 pour cent au choc | **fausse**, il baisse de 14 pour cent sous la regle primaire et monte de 1,7 pour cent sous la secondaire |
| **P4** | part stable de `infl1` entre 0,25 et 0,55 | **tenue**, 0,525 [0,510 ; 0,539] |
| **P5** | chute de `H` superieure a celle de `D` d'au moins 0,05, et `P` capte au moins 70 pour cent de `F` | **tenue deux fois**, ecart de 0,56 et 96,4 pour cent |
| **P6** | chute nulle sur la direction de la revision, et part dans le sens de la derive reproduite par le nul a 3 points pres | **moitie fausse, moitie tenue** : la chute vaut 0,124 et n'est pas nulle, mais elle est entierement portee par le niveau d'avant ; l'ecart au nul vaut 1,6 point |

Trois tenues, deux fausses, une a moitie. **Les deux fausses le sont dans le sens qui compte :
la regle de detection du choc a trouve la fin d'un episode plutot que son debut, et la
direction de la revision est plus previsible que je ne l'attendais, pour une raison qui la
rend inutile.** Une famille de predictions qui se trompe dans les deux sens est la seule
preuve interne qu'elle a bien ete ecrite avant.

---

## 10. Les ecarts au preenregistrement

| | ecart | pourquoi |
|---|---|---|
| **E1** | **Les cinq variables signees ne sont pas reconstruites, elles sont prises telles quelles.** Le preenregistrement, section 2.1, deduisait du questionnaire qu'il fallait multiplier l'amplitude par moins un pour la direction « decrease ». La verification sur les donnees montre que **la colonne `part2` du fichier public est deja signee** : pour la direction 1, 100,0 pour cent des valeurs sont positives ou nulles ; pour la direction 3 ou 2, de 85 a 99 pour cent sont strictement negatives et le reste vaut exactement zero. | Appliquer la regle ecrite aurait retourne le signe de cinq variables sur douze et rendu tout le rapport faux. L'accord entre direction declaree et signe observe est publie comme controle bloquant **C5**, et il passe a 1,0000 sur les cinq. |
| **E2** | **Deux controles bloquants ajoutes, C5 et C6.** C5 est ci dessus. C6 verifie que l'extraction rapide des groupes de permutation tire **exactement la meme permutation** que `a44_commun.permuter_intra` a graine egale, sur 200, 5 000 et 60 000 lignes. | `a44_commun.permuter_intra` balaie tout le vecteur pour chaque groupe. Avec trois mille groupes (mois x cohorte) et soixante mille lignes, une permutation coutait cent fois plus que le calcul qu'elle sert, et le calcul complet demandait trois heures. La definition n'est pas touchee ; seule l'extraction des groupes est faite une fois au lieu de trois mille. |
| **E3** | **Le temoin `T0b` est la moyenne de la cohorte au mois cible a plein echantillon, et non la moyenne du mois.** | Le preenregistrement declarait un temoin constant **par mois**. Le score de verdict etant une correlation de Spearman calculee **a l'interieur du mois**, un score constant par mois y est indefini et ne peut rien verifier. Le temoin doit varier a l'interieur du mois pour etre notable, et etre constant a l'interieur du **groupe de permutation** pour que sa chute soit exactement nulle. La version publiee remplit les deux conditions et donne 0,000000 sur les neuf variables. |
| **E4** | **Le mois est donne aux predicteurs sous deux colonnes, son index et sa moyenne, et non en soixante-neuf indicatrices.** | La foret mettait quatre minutes par variable avec les indicatrices et vingt secondes avec la moyenne. L'information portee est la meme, elle est constante par mois dans les deux cas. Le principe declare, « la tendance agregee est offerte a chacun », est respecte a la lettre. |
| **E5** | **Le bootstrap de la section 6.1 porte sur 400 tirages et non 1 000 ; celui de la section 5 sur 200.** | Cout de calcul, meme raison que l'ecart E5 de i1. Les intervalles publies ont une largeur de six a dix millimes de point de Spearman ; passer a mille tirages ne changerait aucune conclusion. |
| **E6** | **Le choc est publie sous les deux regles et non sous la seule regle primaire.** | La regle primaire designe juin 2025, la secondaire avril 2025. La primaire porte le verdict comme declare et n'a pas ete modifiee ; publier la secondaire a cote est le seul moyen de ne pas laisser croire que le mois de juin est le mois de l'evenement. |
| **E7** | **Un predicteur `L`, niveau d'avant le choc, seul et signe, ajoute a la section 6.2.** | Sans lui, la chute non nulle sur la direction de la revision aurait ete lue comme un signal de personne. `L` montre qu'elle est du retour a la moyenne. C'est le pendant exact de l'ecart E2 de i1, qui avait ajoute le predicteur `P` pour la meme raison. |

Un point du preenregistrement n'a pas ete execute et n'est pas remplace : **la version robuste
de la decomposition n'a pas ete reprise sur les cohortes alternatives**, seule la part inter
en variance l'a ete.

---

## Ce que cela vaut pour une banque centrale

Le desaccord des menages sur l'inflation, qui est la quantite que la politique monetaire
surveille au dela de la moyenne, se joue a **98 pour cent a l'interieur des cohortes d'age, de
diplome et de revenu**, et une population simulee qui reproduit les moyennes de cohorte rend
donc exactement ce que l'enquete donne deja et perd la totalite de ce qui est cherche.
La moitie de ce desaccord interne est une **vraie heterogeneite de menage**, part stable 0,525
sur l'inflation a un an, ce qui veut dire qu'il y a bien quelque chose a simuler, et non du
bruit de mesure. Mais la contrepartie est severe : **ce qui est previsible d'un menage tient a
96 pour cent dans ce qu'il a repondu le mois precedent**, de sorte qu'un simulateur qui ne
recoit pas les reponses anterieures des menages n'a aucune chance de battre une ligne de code,
et qu'un simulateur qui les recoit devra prouver qu'il apporte autre chose que de la
persistance.

---

## Ce que le run simule devra montrer

Le protocole de la nuit suivante, a declarer dans un preenregistrement avant tout appel.

**Les cohortes.** Les six cohortes pleines les plus peuplees du perimetre, qui portent a elles
seules **48 pour cent** des observations : `40 a 60 x diplome x plus de 100 k`, `moins de 40 x
diplome x plus de 100 k`, `moins de 40 x diplome x 50 a 100 k`, `40 a 60 x diplome x 50 a
100 k`, `plus de 60 x quelques annees x moins de 50 k`, `plus de 60 x diplome x 50 a 100 k`.
Cent menages tires par cohorte, soit six cents agents, chacun avec son historique reel.

**Les mois.** Deux fenetres de trois mois. La fenetre de contexte, **decembre 2024 a fevrier
2025**, entierement anterieure au choc, sert d'historique donne a l'agent. La fenetre notee,
**mars a juin 2025**, contient la montee et le retournement, donc les deux regles de choc.

**Les deux regimes, comme M4 les declare.** **C2**, l'agent recoit l'etiquette de cohorte,
age, diplome, revenu, region, numeratie, et rien d'autre. **C3**, l'agent recoit en plus **ses
propres anticipations des trois mois de contexte**, en clair, et le mois courant. Aucun agent
ne recoit la moyenne du mois cible ni la marginale de sa cohorte au mois cible.

**Les quatre adversaires, tous a zero appel.** `P`, la persistance ; `D`, les demographies
seules ; `T1`, la moyenne de cohorte ; et la voie **description**, dans laquelle le modele
n'incarne personne mais decrit la distribution de la cohorte, qui est l'adversaire bon marche
de a27 et que M4 designe explicitement.

**Le modele et sa coupure.** Un modele local a coupure documentee et anterieure au choc, le
20 milliards de a5 et a11, coupure juin 2024 selon lecture 07. **La coupure doit etre
anterieure a mars 2025**, sinon le test n'a aucune valeur ; c'est la seule contrainte qui ne
se negocie pas. Le registre de version et le compte infini-gram des chiffres publies de la SCE
sont a joindre comme variable de controle.

**Les cinq nombres a rendre.** La chute sous permutation intra cohorte sur l'anticipation du
mois suivant, a comparer a 0,639 et a 0,615 ; la part inter cohortes de la population simulee,
a comparer a 0,019 ; sa part stable d'un mois a l'autre, a comparer a 0,525 ; le rapport entre l'ampleur de
ses revisions au choc et celle de son propre nul a derive, a comparer a **0,43** chez les
humains, sachant qu'une population sans appariement des personnes rendrait 1,00 ; et la
chute sur qui revise, a comparer a 0,287 et a 0,140.

**Les points d'arret.** Si C3 ne bat pas `P` sur la chute, la branche jumeaux du programme C
version menages ferme et le banc devient un banc de statistique, comme MOONSHOTS l'ecrit. Si
C2 fait aussi bien que C3, le regime a etiquette suffit et le dossier a trouve un contre
exemple a a44, ce qui vaudrait d'etre publie tel quel.

---

## Ce que je n'ai pas pu verifier

1. **Que le choc de 2025 soit le choc tarifaire.** Le mois est defini depuis les donnees par
   une regle ecrite d'avance, et **aucune donnee externe n'a ete consultee** : ni serie
   officielle d'inflation, ni indice de prix, ni chronologie d'evenements. Que la montee de
   janvier a avril 2025 soit l'effet des annonces tarifaires est une **hypothese**, pas une
   mesure de ce rapport. [HYPOTHESE]
2. **Que la part stable de 0,525 soit une composante permanente.** L'estimateur d'analyse de
   variance suppose un residu echangeable dans le temps ; la courbe de retest decroit de 0,659
   a 0,280, donc il ne l'est pas. Le vrai nombre est entre les deux et ce rapport ne le
   separe pas. [PROBABLE]
3. **Que le sous ensemble de `perte_emploi` soit exogene.** La question n'est posee qu'aux
   salaries non independants ayant un emploi ; qui perd son emploi sort du perimetre. Toutes
   les mesures sur cette variable sont conditionnelles a l'emploi, et sa part stable elevee,
   0,559, peut en etre un artefact.
4. **La ponderation.** Les champs `weight` existent et ne sont **pas** utilises. Toutes les
   quantites publiees sont des quantites d'echantillon, jamais des quantites de population
   americaine. Meme convention et meme reserve qu'en i1 section 9.7.
5. **L'attrition.** Le panel est tournant, un menage qui disparait n'est pas remplace par son
   semblable, et les mesures de stabilite portent mecaniquement sur les menages qui restent.
   Un menage sur sept ne repond qu'une fois et n'entre dans aucune mesure de retest.
6. **Les valeurs de `tenure` superieures a douze.** 683 menages ont treize ou quatorze mois de
   participation, et `tenure` monte a 16, alors que le protocole publie annonce douze mois.
   L'explication n'est pas documentee sur la page de la SCE et n'a pas ete cherchee ailleurs.
7. **L'effet de la winsorisation sur la part inter cohortes.** Les bornes sont globales et
   declarees, mais la part inter n'a pas ete recalculee sans winsorisation ni avec d'autres
   centiles. Les mesures robustes, publiees a cote, vont dans le meme sens, ce qui rassure
   sans prouver.
8. **Que la mediane des IQR intra cohorte soit un bon estimateur.** Elle passe parfois au
   dessus de l'IQR total, ce qui est du bruit d'echantillonnage sur des cellules de vingt-quatre
   menages. Aucune correction de biais n'a ete faite sur la version robuste, contrairement a
   la version en variance.
9. **La comparaison a la litterature.** Aucune recherche d'anteriorite n'a ete faite. La
   decomposition inter et intra cohorte du desaccord d'inflation est un classique de la
   litterature sur les anticipations, Mankiw, Reis et Wolfers 2003 est cite par
   `brainstorm/03` sans avoir ete lu ici, et il est possible que la part de 2 pour cent soit
   deja publiee. Ce qui est probablement neuf est **la mise en regard de cette part avec la
   part stable et avec la chute sous permutation**, c'est a dire la lecture en termes de
   jumeau.

---

## Questions ouvertes pour Simon

1. **La question qui commande le run : contre quel adversaire note-t-on le jumeau ?** La
   persistance capte 96 pour cent de ce que la foret va chercher. Un jumeau qui recoit
   l'historique du menage et qui bat la persistance de deux centiemes aura battu la
   persistance, et cela ne voudra rien dire. **Ma preference est de noter le jumeau sur la
   partie residuelle : ce qu'il ajoute a `P`, et non ce qu'il fait tout seul**, avec la
   chute complete publiee a cote. Il faut trancher avant le run, parce que les deux chiffres
   racontent des histoires opposees.
2. **Faut il changer la regle de detection du choc pour les prochains jeux ?** Une regle de
   saut mensuel maximal en valeur absolue a designe le retournement plutot que la montee. Une
   regle de **plus grand ecart entre deux fenetres de trois mois glissantes** aurait designe
   avril. Elle est aussi mecanique, aussi preenregistrable, et elle voit les episodes qui
   durent un trimestre. Je ne l'ai pas substituee ici parce que le preenregistrement etait
   ecrit ; je propose de l'ecrire pour les panels europeens.
3. **Le rapport d'ampleur du nul a derive doit il devenir une quantite de verdict du
   dossier ?** Il vaut 0,43 a 0,55 chez les humains, il coute zero appel, il se calcule sur
   n'importe quelle population simulee avec le meme code, et il dit quelque chose qu'aucune
   des quantites existantes ne dit : une population sans appariement des personnes **bouge
   deux fois trop**. Si oui, il faut le passer sur Twin, sur les six conditions de Stanford et
   sur les panels GSS, ce qui est le verrou cinq de `MODELE-DU-MONDE` 10.5 transpose au
   mouvement.
4. **Que fait on de l'incertitude individuelle ?** `infl1_var` est la seule variable dont la
   cohorte explique une part non negligeable, 0,119 et en hausse continue depuis 2020, et sa
   part stable est la plus haute des neuf, 0,616. C'est aussi la seule ou la persistance bat
   la foret. Elle se comporte comme un **trait de menage** plus que comme une anticipation.
   Faut il en faire une variable a part, et la traiter comme a29 traite la propension aux
   reponses rares ?
5. **La SCE n'a ni parti ni ideologie. Est ce un probleme ou une chance ?** Tout le dossier
   segmente par camp. Ici c'est impossible, et pourtant la part inter cohortes est encore plus
   basse que ce que a1 mesure sur le GSS avec l'ideologie dans le segment. Cela suggere que le
   resultat « le gabarit ecrase l'interieur » ne depend pas de la nature du segment. Faut il en
   faire un argument, ou une reserve ?
6. **Faut il ouvrir le fichier 2013-2016 ?** Il coute cinquante mega-octets de lecture et
   ajoute quarante-trois mois et 8 735 menages. Il ne sert a rien pour le choc de 2025, mais il
   donnerait une trajectoire de dispersion sur douze ans et il contient l'episode de 2015-2016,
   qui est le seul autre point de comparaison hors crise. Je ne l'ai pas ouvert.
7. **La question de jointure de la lettre 02 est resolue et il faut le lui dire.** Les
   identifiants sont stables d'un fichier a l'autre, 936 menages recoupes au raccord de
   janvier 2025 avec 100 pour cent d'accord sur les demographies fixes. La lettre garde ses
   autres points, notamment la vague tenue cachee, mais son point de blocage technique tombe.
