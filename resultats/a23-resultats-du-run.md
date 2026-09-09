# a23. Ce que le premier run d'agents locaux etablit, et ce qu'il detruit

Rapport du 8 septembre 2026, ecrit apres la fin du run a5 et apres les deux evaluations du
matin. Il porte sur les traces **completes** de C2 et C3, 22 350 appels chacune, 150 personnes,
149 items.

Sources primaires : `data/traces/a5-run.log`, `data/traces/evaluation-matin.log` (a5_evaluer
puis a18_decomposition_traces, lances a 05:02:13 et 05:02:32, code de retour 0 tous les deux),
`resultats/a5-familles.csv` et `resultats/a5_resultats.json` (horodates 05:02:32),
`resultats/a18-*.csv` et `resultats/a18-figure-c2-c3.png` (horodates 05:03:10 a 05:03:12).
Horodatages verifies, ils sont bien posterieurs a la ligne `RUN TERMINE 2026-09-08 05:01:21`.

Deux scripts nouveaux ont ete ecrits pour ce rapport, aucun script existant n'a ete modifie :
`analyses/a23_regime_de_validite.py` (exactitude par item, ecarts apparies, concentration) et
`analyses/a23_axes_ic.py` (intervalles bootstrap par axe, absents de a18). Sorties :
`resultats/a23-par-item.csv`, `a23-ecarts-apparies.csv`, `a23-concentration.csv`,
`a23-axes-ic.csv`.

---

## Reponse en une ligne

**Le run detruit la revendication d'exactitude et il en fabrique une autre : nos deux agents
locaux sont domines sur les deux axes a la fois, exactitude et diversite conservee, par une
regression logistique sur les seules demographies, C3 a 0,5817 et 67,4 pour cent de diversite
contre B1 a 0,6281 et 73,1 pour cent [MESURE, `evaluation-matin.log`, bloc a5_evaluer] ; mais
il etablit le contraste que la litterature n'avait pas fait, a savoir que la meme machine, meme
modele, meme temperature, memes personnes et memes items, gonfle les ecarts entre segments
ideologiques d'un facteur 8,16 [5,43 ; 15,55] quand l'etiquette ideologique est dans l'invite,
et les ecrase a 0,73 [0,47 ; 0,99] quand elle n'y est pas** [MESURE, `a23-axes-ic.csv`, mesure
entropie], **le controle de la vague 2 passant desormais sur cet axe a 1,11 [0,93 ; 1,41]**.

---

## 0. Etat du run, verifie avant toute lecture

| verification | resultat | source |
|---|---|---|
| fin du run | `RUN TERMINE 2026-09-08 05:01:21` | `a5-run.log` |
| C2 passe 1 | 22 350 appels en 101,5 min, 13 217 appels/h, **0 rejet** | `a5-run.log` |
| C3 passe 1 | 22 350 appels en 274,5 min, 4 886 appels/h, **30 rejets** | `a5-run.log` |
| lignes de trace | 22 350 et 22 350 | `wc -l` sur les deux JSONL |
| controle de degenerescence a18 | `CONTROLE PASSE`, ecart 0,000e+00 | `evaluation-matin.log` |
| controle argmax du tenseur contre trace | coincide sur toutes les cellules | idem |
| cellules exploitables par toutes les conditions | 22 147 sur 22 350, soit 99,09 pour cent | idem |
| plafond humain test retest de ces 150 personnes | **0,7915 [0,7763 ; 0,8056]** | idem, bloc a5_evaluer |

**Les 30 rejets de C3 ne sont pas repartis au hasard : 25 portent sur `income`, 3 sur
`dwelown16`, 2 sur `mobile16`, sur 27 personnes distinctes, avec une masse sur les lettres
descendant a 0,0991** [MESURE, relecture directe de `a5-C3-p1.jsonl`]. `income` a douze
modalites, donc treize lettres declarees. L'evaluateur ne filtre pas ces cellules : elles sont
scorees sur une distribution renormalisee qui ne capte qu'un dixieme a un cinquieme de la masse.
L'effet sur le chiffre global est negligeable, 30 cellules sur 22 350, mais la regle de scoring
par lettre unique n'est pas robuste au dela de sept ou huit modalites, et cela doit etre ecrit.
C2 n'a aucun rejet et aucune modalite absente du top 40 [MESURE].

**C3F et l'extension de C2 ne sont pas dans ce rapport.** C3F a demarre a 05:01:59 avec une fin
dure a 06:20 et tourne a 2 556 appels/h ; a 05:17 elle porte 638 appels sur les 8 700 attendus,
11 personnes completes [MESURE, `a5-familles.log` et `a5-C3F-p1.jsonl`]. A ce debit elle
couvrira environ 3 300 appels, soit 57 personnes sur 150, et l'extension de C2 ne tournera pas.
Toute ligne C3F apparaissant dans les sorties de ce matin est calculee sur une trace partielle
de onze personnes et ne doit pas etre lue.

---

## 1. Le regime de validite : ou C3 bat il quelque chose ?

### 1.1 Globalement, sur les 149 items, il ne bat rien qui compte

Ecarts apparies sur les memes 150 personnes, bootstrap 2 000 tirages sur les personnes
[MESURE, `a23-ecarts-apparies.csv`, perimetre "149 items"] :

| comparaison | ecart en points | IC 95 % | en points de score normalise |
|---|---|---|---|
| C3 moins B0 mode | **-1,39** | [-2,42 ; -0,31] | -1,76 |
| C3 moins B1 argmax | **-4,64** | [-5,71 ; -3,60] | -5,86 |
| C3 moins B2 argmax | **-8,81** | [-9,76 ; -7,84] | -11,12 |
| C3 moins agents enquete | **-6,41** | [-7,32 ; -5,49] | -8,10 |
| C3 moins agents composite | -10,08 | [-11,13 ; -9,12] | -12,73 |
| C3 moins agents v8 | **+1,66** | [+0,42 ; +2,89] | +2,10 |
| C3 moins agents v7 | **+1,36** | [+0,18 ; +2,57] | +1,72 |
| C3 moins agents demographiques (v6) | -0,70 | [-1,70 ; +0,32] | -0,88 |
| C3 moins C2 | +5,54 | [+4,60 ; +6,58] | +7,00 |
| C2 moins B2 argmax | -14,34 | [-15,54 ; -13,12] | -18,12 |

**Ce que cela dit sans ambiguite.** Les seules conditions que C3 bat de facon distinguable sont
les deux invites les plus pauvres du paquet de Stanford, `v8` et `v7`, de 1,4 a 1,7 point. Il
egale `v6`. Il perd contre la modalite majoritaire, contre la regression logistique, contre les
30 plus proches voisins et contre les trois conditions riches de Stanford. **C2 n'est devant que B0
tirage : il est derriere les dix autres methodes non humaines sur le chiffre global**
[MESURE, `evaluation-matin.log`, bloc a5_evaluer].

### 1.2 Par famille thematique, une famille sort

Tableau par famille, exactitude sur les memes 150 personnes [MESURE, `a5-familles.csv`] :

| famille | items | plafond humain | **C3** | B2 argmax | B1 argmax | B0 mode | ag. enquete | ag. composite | **C2** |
|---|---|---|---|---|---|---|---|---|---|
| depenses publiques (nat*) | 17 | 0,7310 | 0,4871 | **0,6333** | 0,5902 | 0,5675 | 0,5776 | 0,5753 | 0,4369 |
| confiance institutions (con*) | 13 | 0,7128 | 0,5477 | **0,5954** | 0,5482 | 0,5164 | 0,5744 | 0,6000 | 0,4841 |
| avortement (ab*) | 7 | 0,9162 | 0,8076 | **0,8705** | 0,8190 | 0,7486 | 0,8648 | 0,8848 | 0,7771 |
| **libertes civiles (spk/col/lib)** | 11 | 0,8303 | **0,8018** | 0,7921 | 0,7448 | 0,7558 | 0,7879 | 0,7861 | 0,7352 |
| fin de vie (suicide/letdie) | 5 | 0,8840 | 0,7773 | **0,8507** | 0,7480 | 0,7360 | 0,7960 | 0,7867 | 0,6893 |
| roles de genre (fe*) | 5 | 0,6707 | 0,4973 | **0,5253** | 0,4640 | 0,4787 | 0,4853 | 0,5213 | 0,4227 |

**Sur les libertes civiles, C3 est en tete des douze methodes non humaines** [MESURE]. Les
ecarts apparies sur cette famille [MESURE, `a23-ecarts-apparies.csv`] :

| comparaison, famille libertes civiles | ecart | IC 95 % |
|---|---|---|
| C3 moins B1 argmax | **+5,70** | [+2,67 ; +8,85] |
| C3 moins B0 mode | **+4,61** | [+1,82 ; +7,39] |
| C3 moins C2 | **+6,67** | [+4,00 ; +9,45] |
| C3 moins B2 argmax | +0,97 | [-1,45 ; +3,39] |
| C3 moins agents enquete | +1,39 | [-1,21 ; +4,00] |
| C3 moins agents composite | +1,58 | [-1,03 ; +4,30] |

Lecture stricte : **C3 est nominalement premier, distinguablement au dessus de la regression
logistique et de la modalite majoritaire, et indistinguable de B2 et des deux conditions
riches de Stanford.** Aucune correction pour tests multiples n'est appliquee, et il y a 36
comparaisons dans ce bloc : a 5 pour cent nominal on attend environ deux intervalles excluant
zero par pur hasard, et il y en a douze, mais la selection de la famille s'est faite apres avoir
vu les chiffres. C'est un resultat a repliquer, pas un resultat a annoncer [PROBABLE].

Dans les cinq autres familles, C3 est battu par B2 de facon distinguable dans quatre
(depenses -14,63 ; confiance -4,77 ; avortement -6,29 ; fin de vie -7,33) et non distinguable
dans la cinquieme, roles de genre, -2,80 [-6,67 ; +1,20] [MESURE, `a23-ecarts-apparies.csv`].

### 1.3 Par item, douze items sur 149

Comptes item par item, memes 150 personnes [MESURE, `a23-par-item.csv`] :

| comparaison | items ou C3 devance | egalites | ecart moyen par item |
|---|---|---|---|
| C3 contre B0 mode | 74 sur 149 | 14 | -0,0139 |
| C3 contre B1 argmax | 66 sur 149 | 4 | -0,0464 |
| C3 contre B2 argmax | 35 sur 149 | 8 | -0,0881 |
| C3 contre agents enquete | 43 sur 149 | 5 | -0,0641 |
| C3 contre agents v8 | 89 sur 149 | 4 | +0,0166 |
| C2 contre B2 argmax | 5 sur 149 | 12 | -0,1434 |

**C3 est strictement en tete des dix methodes non humaines sur 12 items sur 149. C2 sur zero.**
Les douze : `spkath/y` 0,900, `spkhomo/y` 0,947, `spkcom/y` 0,860, `colath` 0,847 (libertes
civiles), `conjudge` 0,540, `conlegis` 0,600, `coneduc` 0,607 (confiance), `natheal/y` 0,680,
`jew` 0,880, `savesoul` 0,840, `jobfind` 0,673, `discaffm` 0,487 [MESURE, `a23-par-item.csv`].
Le motif est lisible : questions de tolerance, de liberte d'expression et de religion, la ou un
modele de langage a une representation dense et ou la reponse est peu predictible par la
demographie.

### 1.4 Le chiffre desagreable : l'avantage n'existe que dans les familles

Exactitude separee sur les 58 items des six familles et sur les 91 autres [MESURE,
`a23-ecarts-apparies.csv`, perimetres "familles reunies" et "hors famille"] :

| methode | 58 items de famille | 91 autres items |
|---|---|---|
| humains vague 2 | 0,7761 | 0,8013 |
| B2 argmax | **0,6930** | 0,6549 |
| agents composite | 0,6717 | **0,6893** |
| agents enquete | 0,6623 | 0,6353 |
| B1 argmax | 0,6405 | 0,6202 |
| **C3** | 0,6249 | **0,5541** |
| B0 mode | 0,6205 | 0,5798 |
| **C2** | 0,5656 | 0,5012 |

**Hors des six familles, C3 tombe sous la modalite majoritaire.** Le deficit y est concentre :
les dix pires items expliquent 61 pour cent de l'ecart moyen a B1 et 193 pour cent de l'ecart a
B0 mode, c'est a dire que **sans ces dix items C3 passerait au dessus de B0 mode**, +0,0139 par
item au lieu de -0,0139 [MESURE, calcul sur `a23-par-item.csv`].

Ces dix items ne sont pas des accidents, ce sont des inversions de population :

| item | mode humain sur les 150 | argmax de C3, comptage sur 150 | C3 | B1 argmax |
|---|---|---|---|---|
| `dwelown16` | "own or is buying", 110 | **"Other", 133** | 0,053 | 0,760 |
| `nataid/y` | "too much", 103 | **"Too little", 128** | 0,133 | 0,667 |
| `divlaw` | "stay as is", 79 | **"More difficult", 139** | 0,193 | 0,487 |
| `income` | 12 modalites | eparpille, 25 rejets | 0,093 | 0,500 |

[MESURE, comptage direct sur `a5-C3-p1.jsonl` et `a23-par-item.csv`] Sur ces items, le modele
n'echoue pas au niveau de la personne, il substitue **sa** modalite a celle de la population.

---

## 2. La comparaison a modele egal d'information

Les deux couples apparies, sur les memes 150 personnes et les memes 149 items. C2 porte les
onze attributs de `demographic_summary.csv`, ideologie et parti compris : son homologue est
`gss_v8` et non `gss_v6` [CONFIRME, a17 objection 3, a19 section 1]. C3 porte les 119 reponses
d'enquete du bloc et aucune demographie : son homologue est la condition agents enquete.

| | **C2 contre `gss_v8`** | **C3 contre agents enquete** |
|---|---|---|
| notre modele | Qwen3-4B-Instruct-2507 Q4_K_M, temperature 0, un appel, `n_probs` 40 (a5 section 2) | idem |
| leur modele | GPT-4o, temperature 0,7 en dur, un seul appel (a16, `gpt_structure.py` ligne 74) | idem |
| exactitude | 0,5263 contre 0,5651 | 0,5817 contre 0,6458 |
| **ecart apparie** | **-3,87 points [-4,74 ; -2,95]** | **-6,41 points [-7,32 ; -5,49]** |
| **en part du plafond 0,7915** | **-4,90 points de score normalise**, 66,5 contre 71,4 pour cent | **-8,10 points**, 73,5 contre 81,6 pour cent |
| ratio intra (entropie) | 0,556 [0,527 ; 0,584] contre 0,674 [0,648 ; 0,697] | 0,672 [0,657 ; 0,687] contre 0,831 [0,814 ; 0,847] |
| ratio de dispersion totale | 0,653 contre 0,785 | 0,671 contre 0,852 |
| diversite conservee | 65,4 contre 78,9 pour cent | 67,4 contre 85,6 pour cent |
| ratio inter, axe ideologie | **8,16 [5,43 ; 15,55] contre 8,95 [6,00 ; 16,80]** | **0,73 [0,47 ; 0,99] contre 2,43 [1,82 ; 3,72]** |

[MESURE, `evaluation-matin.log`, `a18-decomposition.csv`, `a18-recapitulatif.csv`,
`a23-ecarts-apparies.csv`, `a23-axes-ic.csv`]

**L'effet du modele, quantifie.** A information strictement egale, passer de GPT-4o a 0,7 a
Qwen3-4B en 4 bits a temperature 0 coute **3,9 point d'exactitude dans le regime demographique
et 6,4 points dans le regime questionnaire**, soit **4,9 et 8,1 points de score normalise**,
c'est a dire de 6 a 10 pour cent du plafond humain. Il coute aussi de 0,12 a 0,16 de ratio
intra et de 0,13 a 0,18 de ratio de dispersion totale : **le petit modele en local est plus
faux et plus homogene, les deux ensemble.**

**Mais l'effet n'est pas le meme sur le terme inter, et c'est le resultat.** Dans le regime
demographique, notre modele reproduit le gonflement de GPT-4o presque exactement, 8,16 contre
8,95, intervalles largement recouvrants. Dans le regime questionnaire, il fait **l'inverse** de
GPT-4o : leurs agents enquete gonflent l'axe ideologique de 2,43 [1,82 ; 3,72], les notres
l'ecrasent a 0,73 [0,47 ; 0,99], intervalle excluant 1 des deux cotes et les deux intervalles
disjoints. **Le gonflement du regime questionnaire n'est donc pas une propriete des modeles de
langage, c'est une propriete de ce modele la, ou de sa taille, ou de sa temperature** [MESURE
pour le fait, [HYPOTHESE] pour la cause, une seule paire de modeles].

Reserve obligatoire, deja portee par a5 limite 4 : **le prompt de C2 n'a pas ete compare a celui
de `v8`, ni celui de C3 a celui des agents enquete.** Une part de ces ecarts peut venir de la
formulation. C'est la limite la plus serieuse de toute cette section.

---

## 3. Les cinq contrastes de a15, sur les traces completes

### 3.1 Le juge : le controle de la vague 2 passe-t-il a 150 personnes ?

a18 publiait les ratios par axe **sans intervalle**, son bootstrap ne portant que sur l'agregat
des six axes. `analyses/a23_axes_ic.py` reprend sa preparation de banc telle quelle et
bootstrappe axe par axe, memes 50 permutations, memes 1 000 tirages recentres, meme graine.

Controle de la vague 2 par axe, ratio inter, les memes personnes reinterrogees deux semaines
plus tard [MESURE, `a23-axes-ic.csv`] :

| axe | denominateur humain, bits | entropie | Gini Simpson | verdict |
|---|---|---|---|---|
| **ideologie politique** | 7,12 | **1,11 [0,93 ; 1,41]** | **1,01 [0,86 ; 1,20]** | **passe sur les deux mesures** |
| profil croise | 9,22 | 0,97 [0,70 ; 1,19] | 0,90 [0,59 ; 1,07] | passe |
| age | 4,50 | 1,10 [0,83 ; 1,66] | 1,02 [0,77 ; 1,44] | passe, intervalle large |
| education | 1,96 | 1,06 [-0,92 ; 3,77] | 1,17 [-1,82 ; 4,09] | **ininterpretable** |
| genre | 1,70 | 0,83 [0,44 ; 1,32] | 0,78 [0,24 ; 1,29] | limite, intervalle de largeur 0,9 |
| race | 0,84 | 1,46 [-5,71 ; 7,87] | 1,27 [-1,76 ; 4,75] | **ininterpretable** |

Au niveau agrege, le controle passe aussi, ce qui n'etait pas le cas a 55 personnes :
**1,046 [0,912 ; 1,237]** en entropie et **0,983 [0,856 ; 1,117]** en Gini Simpson, contre
1,167 avec un intervalle debordant des deux cotes sur la trace partielle [MESURE,
`a18-decomposition.csv` contre a18 tableau 1].

**Reponse a la question posee : oui, le controle passe a 150 personnes sur l'axe ideologie, et
sur cet axe seulement de facon confortable.** Les ratios inter du run sont donc publiables sur
l'ideologie, le profil croise et l'age. Ils ne le sont pas sur la race ni sur l'education, ou le
denominateur humain vaut 0,84 et 1,96 bit sur 149 items et ou l'intervalle du controle contient
des valeurs negatives. Le genre est un cas intermediaire a ne pas publier seul.

Ce point retire la limite transversale de SYNTHESE-NUIT qui disait "150 personnes ne suffisent
probablement pas a estimer le terme inter" : elles suffisent sur l'axe qui porte l'effet
principal, elles ne suffisent pas sur les axes a faible denominateur. La premiere des trois
issues de a18 question 1 est donc retenue, mais dans une version restreinte a l'axe.

### 3.2 Contraste 1 : ratio inter par axe, C2 contre C3

Mesure entropie, intervalles bootstrap [MESURE, `a23-axes-ic.csv`] :

| condition | genre | race | **ideologie** | age | education | profil croise |
|---|---|---|---|---|---|---|
| *denominateur humain, bits* | *1,70* | *0,84* | *7,12* | *4,50* | *1,96* | *9,22* |
| humains vague 2 | 0,83 | 1,46 | **1,11 [0,93 ; 1,41]** | 1,10 | 1,06 | 0,97 |
| **C2 argmax** | 0,07 | 4,84 | **8,16 [5,43 ; 15,55]** | **1,87 [1,09 ; 4,11]** | 2,60 | **4,88 [2,89 ; 16,01]** |
| **C3 argmax** | 0,66 | -0,09 | **0,73 [0,47 ; 0,99]** | 0,43 [-0,08 ; 0,75] | 0,97 | **0,57 [0,16 ; 0,82]** |
| agents enquete | 0,89 | 1,17 | **2,43 [1,82 ; 3,72]** | 0,99 | 1,21 | **1,90 [1,33 ; 4,72]** |
| agents composite | 0,95 | 1,49 | **2,20 [1,69 ; 3,36]** | 1,26 | 1,28 | **1,63 [1,21 ; 3,47]** |
| agents v8 | 0,13 | 5,17 | **8,95 [6,00 ; 16,80]** | **3,07 [1,87 ; 7,24]** | 0,96 | **5,95 [3,47 ; 19,00]** |
| agents v6 | 0,91 | 3,90 | **0,24 [-0,25 ; 0,66]** | 0,99 | 2,66 | 0,69 |

**Aucune des trois issues ecrites par a15 section 8 ne decrit ce tableau, et la sortie du script
le dit en ces termes** [MESURE, `evaluation-matin.log`, bloc `VERDICT SUR LES TROIS ISSUES DE
a15`]. Le detail :

- **Issue A**, l'axe commande, C2 gonfle l'ideologie et reste au voisinage de 1 sur genre et
  age, C3 pareil en moins fort. **Fausse pour C3** : C3 ne gonfle rien, il ecrase l'ideologie a
  0,73 avec un intervalle excluant 1.
- **Issue B**, l'etiquette commande, C2 gonfle uniformement et C3 sur aucun axe. **Vraie pour la
  moitie C3, fausse pour la moitie C2** : C2 ne gonfle pas uniformement, il effondre le genre a
  0,07 alors que l'etiquette de genre est dans son invite au meme titre que l'ideologie.
- **Issue C**, les deux gonflent l'ideologie a un niveau comparable, ce qui aurait signifie que
  le modele reconstruit l'ideologie a partir des reponses. **Fausse, et fausse dans les grandes
  largeurs** : 8,16 contre 0,73, intervalles disjoints. Le controle propose par a15, la
  correlation entre ideologie reconstruite et ideologie declaree, se lit deja dans la mesure a
  la Chen : `delta eta carre` de C3 vaut **-0,0225** sur l'axe ideologie a sept niveaux et
  **-0,0104** en trois blocs [MESURE, `a18-chen.csv`], c'est a dire que les reponses de C3
  portent **moins** de structure ideologique que celles des humains. **C3 ne reconstruit pas
  l'ideologie.**

**Ce qui est reellement observe est une quatrieme issue, et il faut l'ecrire telle quelle :
l'etiquette commande le signe, l'axe commande la repartition a l'interieur de la condition
etiquetee.** Sans etiquette, aucun gonflement sur aucun axe, y compris l'ideologie. Avec
etiquette, gonflement massif sur l'ideologie, sur le profil croise et sur l'age, et effondrement
sur le genre, alors que l'etiquette de genre est presente et recopiee. La phrase de synthese de
a15 section 7.1 doit etre rouverte : les deux mecanismes ne sont pas exclusifs, ils sont
emboites.

### 3.3 Contraste 2 : argmax contre distribution

[MESURE, `a18-decomposition.csv` et `a18-chen.csv`]

| condition | inter, argmax | inter, distribution | intra, argmax | intra, distribution | `delta eta carre`, 3 blocs |
|---|---|---|---|---|---|
| C2 | 4,769 | 4,579 | 0,556 | 0,575 | +0,2960 puis +0,2760 |
| C3 | 0,607 | 0,630 | 0,672 | 0,693 | -0,0104 puis -0,0111 |

**Le signe ne change jamais, ni sur l'inter, ni sur l'intra, ni sur la mesure de Chen.** Ce que
la trace partielle annoncait tient : chez nous le mode distributionnel gonfle **legerement
moins** pour C2, 4,579 contre 4,769, la ou Chen trouve l'inverse pour Sonnet, +0,104 contre
+0,081. Pour C3 il ecrase legerement moins, 0,630 contre 0,607, c'est a dire qu'il rapproche de
1 dans les deux cas. L'ecart est de 4 pour cent sur C2 et de 4 pour cent sur C3 : a temperature
0 et avec 77 a 79 pour cent des cellules au dessus de 0,99 de confiance, les deux versions ne
peuvent pas beaucoup differer, ce que a5 annoncait d'avance [PROBABLE pour la cause].

### 3.4 Contraste 3 : la mesure a la Chen

Axe ideologie en trois blocs, 62 items ordinaux, seuil de 8 personnes par segment
[MESURE, `a18-chen.csv`] :

| condition | rapport d'ecart | `delta eta carre` |
|---|---|---|
| agents v8 | 2,715 | **+0,5178** |
| **C2 argmax** | 1,736 | **+0,2960** |
| agents entretien (v3) | 1,787 | +0,0961 |
| agents enquete | 1,235 | +0,0575 |
| agents composite | 1,455 | +0,0460 |
| humains vague 2, controle | 1,000 | +0,0047 |
| **C3 argmax** | **0,489** | **-0,0104** |
| agents v7 | 0,429 | -0,0155 |
| agents demographiques (v6) | 0,443 | -0,0226 |

Le contrat de a18 section 10 est tenu : `delta eta carre` reste **positif pour C2** et
**negatif pour `v6` et `v7`**. Il devient negatif pour C3, ce qui est nouveau et coherent avec
la section 3.2. Le controle humain vague 2 est a +0,0047, rapport d'ecart 1,000. **Seuls le
signe et le classement sont comparables a Chen, jamais les valeurs absolues** : nos segments
sont plus grossiers et notre echantillon est cent fois plus petit que le sien [CONFIRME, a18
section 5].

### 3.5 Contraste 4 : le terme intra a temperature 0

Bande des six conditions de Stanford sur ces 150 personnes : **0,620 (`v6`) a 0,872
(composite)** [MESURE, `a18-decomposition.csv`, entropie].

- **C2 est a 0,556 [0,527 ; 0,584], sous toute la bande, et son inter est dans la bande,
  4,769 contre 5,481 pour `v8`.** C'est exactement le profil que a15 decrivait comme isolant la
  temperature en levier purement intra.
- **C3 est a 0,672 [0,657 ; 0,687], dans la bande, et son inter est sous la bande, 0,607.** Le
  profil inverse.

**La conclusion de a15 sur ce contraste ne tient donc que pour C2 et elle est confondue.** Nos
agents different de ceux de Stanford par la temperature, mais aussi par le modele, la
quantification et l'invite. Rien dans ce run n'isole la temperature. Le dire, et ne pas ecrire
que la temperature est un levier purement intra tant qu'un balayage de temperature a modele
constant n'a pas ete fait [HYPOTHESE non testee].

### 3.6 Contraste 5 : la dispersion totale, la question 3 de a7

[MESURE, `a18-dispersion-totale.csv`]

| condition | version | dispersion totale, bits | ratio | entropie individuelle moyenne | tau |
|---|---|---|---|---|---|
| humains vague 1 | reference | 187,36 | 1,000 | 0 | |
| C2 | 1 argmax | 122,61 | **0,654** | 0 | |
| C2 | 2 tirage, esperance | 125,25 | **0,668** | 0,1165 bit | 1,00 |
| C2 | 3 borne en temperature | 187,36 | 1,000 | 1,0071 bit | **6,29** |
| C3 | 1 argmax | 126,20 | **0,674** | 0 | |
| C3 | 2 tirage, esperance | 129,81 | **0,693** | 0,1396 bit | 1,00 |
| C3 | 3 borne en temperature | 187,36 | 1,000 | 1,0027 bit | **6,27** |

**Le resultat de la trace partielle est confirme et legerement aggrave.** Lire la distribution
complete au lieu de durcir par argmax rend **1,4 point sur les 34,6 qui manquent pour C2**
(0,654 vers 0,668) et **1,9 point sur les 32,6 pour C3** (0,674 vers 0,693), soit 4,1 et 5,9
pour cent du deficit. La temperature necessaire pour combler le reste est de **6,29 et 6,27**,
et non 5,71 comme sur la trace partielle ; elle porterait l'entropie individuelle de 0,117 a
1,007 bit, soit un facteur 8,6. **Le deficit de dispersion totale n'est pas dans le decodage.
La famille A de `exploration/09` est fermee par une mesure, sur deux regimes d'invite et
44 700 appels, et non plus sur 8 116 cellules d'une seule condition.**

### 3.7 Le critere A6 en version positive, un chiffre qui derange

Correlation entre la deviance au mode de segment de l'agent et celle de la vraie personne, axe
ideologie, mode calcule hors soi [MESURE, `a18-critere-a6.csv`] :

| condition | r | deviance agent | deviance humaine |
|---|---|---|---|
| humains vague 2, controle | **0,895** | 0,398 | 0,396 |
| agents composite | 0,773 | 0,374 | 0,396 |
| agents enquete | 0,743 | 0,377 | 0,396 |
| **C3** | **0,673** | **0,429** | 0,396 |
| agents entretien (v3) | 0,585 | 0,372 | 0,396 |
| agents v6 | 0,510 | 0,350 | 0,396 |
| **C2** | **0,246** | **0,409** | 0,396 |
| agents v7 | 0,298 | 0,350 | 0,396 |
| agents v8 | 0,186 | 0,336 | 0,396 |

**C2 et C3 sont les deux seules conditions dont la deviance moyenne depasse celle des humains**,
0,409 et 0,429 contre 0,396, et **C2 a la deuxieme plus mauvaise correlation du tableau**, 0,246.
Toutes les conditions de Stanford sont sous la deviance humaine, profil attendu d'un ecrasement.
Nos agents s'ecartent du stereotype de groupe **plus souvent que les vraies personnes, et pas
pour les memes personnes** : c'est du bruit, pas de l'heterogeneite. Le chiffre de la trace
partielle, C2 a r = 0,638, n'a pas tenu : sur 150 personnes il tombe a 0,246 [MESURE].

---

## 4. La calibration et l'entropie individuelle, sur 44 700 appels

[MESURE, `evaluation-matin.log`, bloc "mesures distributionnelles", et `a18-calibration.csv`]

| | **C2**, 22 350 appels | **C3**, 22 350 appels |
|---|---|---|
| exactitude argmax | 0,5263 | 0,5817 |
| **exactitude esperee** | **0,5258** | **0,5814** |
| ecart argmax moins esperee | **0,0005** | **0,0003** |
| entropie moyenne par appel | 0,1167 bit sur 1,5984 possible, soit **7,3 pour cent** | 0,1411 bit, soit **8,8 pour cent** |
| mediane de l'entropie individuelle | 0,000 bit | 0,000 bit |
| q75, q90 de l'entropie individuelle | 0,036 ; 0,487 | 0,060 ; 0,612 |
| part des appels a p max > 0,99 | **79,3 pour cent** | **76,8 pour cent** |
| **ECE** | **0,4410** | **0,3787** |
| decile 0,9 a 1,0 | n = 20 101, confiance 0,9950, **exactitude 0,5450** | n = 19 674, confiance 0,9943, **exactitude 0,6132** |

**Oui, les distributions sont toujours quasi degenerees, et le smoke test etait optimiste.** Le
smoke test de a5 mesurait 0,66 d'exactitude dans le decile de confiance maximale sur 80
cellules ; sur 20 101 cellules c'est **0,545** pour C2 et 0,613 pour C3. **Quand ce modele dit
0,995, il a raison une fois sur deux.** L'exactitude esperee est a cinq dix millemes de
l'exactitude argmax : il n'hesite jamais.

**La version population du meme fait, qui est nouvelle** [MESURE, `a23-concentration.csv`] :
part mediane de la modalite la plus predite, par item, sur les 150 personnes.

| methode | part mediane | items ou une seule modalite couvre plus de 90 pour cent des personnes |
|---|---|---|
| B0 mode | 1,000 | 141 sur 149 |
| agents v7 | 0,813 | 44 |
| B2 argmax | 0,793 | 53 |
| **C2** | **0,773** | **46** |
| **C3** | **0,760** | **43** |
| B1 argmax | 0,740 | 33 |
| agents enquete | 0,660 | 16 |
| agents composite | 0,627 | 13 |
| **humains vague 1** | **0,573** | **13** |

**Ce que cela dit du deficit de dispersion.** Le deficit n'est pas une hesitation mal decodee,
c'est une certitude mal placee : le modele choisit une modalite pour les trois quarts de la
population sur la moitie des items, et il en est certain. Les 34,6 points de dispersion totale
manquants se logent la, pas dans le durcissement par argmax. Cela confirme, avec deux mesures
independantes et sur deux regimes d'invite, l'orientation vers la famille B, le conditionnement.

---

## 5. Le test existentiel, refait avec nos agents

Le plan exactitude contre diversite conservee, memes 150 personnes, memes 149 items [MESURE,
`evaluation-matin.log`, bloc a5_evaluer, et `a5_resultats.json`] :

| methode | exactitude | normalise | diversite conservee | accord par paires |
|---|---|---|---|---|
| humains vague 2 | 0,7915 | 100,0 % | 99,9 % | 49,3 % |
| agents composite | 0,6825 | 86,2 % | 89,2 % | 53,9 % |
| B2 argmax | 0,6698 | 84,6 % | 58,7 % | 69,2 % |
| agents entretien (v3) | 0,6542 | 82,7 % | 86,7 % | 56,1 % |
| agents enquete | 0,6458 | 81,6 % | 85,6 % | 55,5 % |
| **B1 argmax** | **0,6281** | **79,4 %** | **73,1 %** | 63,0 % |
| B0 mode | 0,5956 | 75,3 % | 3,4 % | 98,1 % |
| agents demographiques (v6) | 0,5887 | 74,4 % | 63,1 % | 67,9 % |
| **C3** | **0,5817** | **73,5 %** | **67,4 %** | 65,3 % |
| agents v7 | 0,5681 | 71,8 % | 64,1 % | 68,4 % |
| agents v8 | 0,5651 | 71,4 % | 78,9 % | 59,2 % |
| **C2** | **0,5263** | **66,5 %** | **65,4 %** | 66,4 % |
| B0 tirage | 0,4940 | 62,4 % | 99,4 % | 49,6 % |

**Front de Pareto de ce plan, humains exclus : deux points seulement, agents composite et
B0 tirage** [MESURE, calcul direct sur `a5_resultats.json`]. Tout le reste est domine.

- **C3 est domine par B1 argmax, agents enquete, agents entretien et agents composite**, c'est
  a dire qu'il existe quatre methodes plus exactes **et** plus diverses.
- **C2 est domine par six methodes**, dont C3, `v8` et B1.

**Reponse au test existentiel, telle qu'elle est.** Sur le GSS, dans nos deux regimes, le modele
de langage local ne se justifie **ni par l'exactitude, ni par le couple exactitude et
diversite**. La phrase de a2 section 8, "le seul avantage clair des modeles de langage dans nos
mesures est ce couple", reste vraie **pour les agents composite de Stanford, GPT-4o**, et
uniquement pour eux : elle ne se transfere pas a un modele local de 4 milliards de parametres en
4 bits. Le seul endroit ou nos agents tiennent est la famille des libertes civiles, section 1.2,
et il faudra le repliquer avant d'en faire quoi que ce soit.

---

## 6. Ce que cela implique pour la these et pour la suite

### 6.1 Ce qui tient dans SYNTHESE-NUIT

1. **Le point 3, le deficit n'est pas dans le decodage.** Renforce et etendu : mesure sur les
   deux conditions completes, 0,654 vers 0,668 et 0,674 vers 0,693, temperature necessaire 6,29
   et 6,27. La mention "trace partielle, a confirmer au matin" est levee. [CONFIRME]
2. **La revendication (b) 9**, l'imputation du deficit total, tient et change de chiffre : 1,4
   point sur 34,6 pour C2, 1,9 sur 32,6 pour C3, temperature 6,29. [CONFIRME]
3. **Le point 10, le pipeline reproduit la mesure fondatrice a un point pres.** Accord par
   paires de C2 sur ces 150 personnes 66,4 pour cent contre 49,3 chez les memes humains
   reinterroges [MESURE, `evaluation-matin.log`], a rapprocher des 66,4 contre 49,5 de a0 sur
   les agents demographiques de Stanford et 1 052 personnes. La coincidence est desormais a
   **zero point** sur le premier terme. [CONFIRME]
4. **Le point 5 et l'errata a19, l'etiquette ideologique est de premier ordre.** Reproduit sur
   notre pipeline, un autre modele, une autre invite : 8,16 avec etiquette contre 0,73 sans,
   intervalles disjoints. [CONFIRME]
5. **La limite "150 personnes ne suffisent probablement pas a estimer le terme inter" tombe en
   partie** : le controle passe a 150 sur l'agregat, sur l'ideologie, sur le profil croise et
   sur l'age. Il ne passe pas sur la race ni sur l'education. [MESURE]

### 6.2 Ce qui tombe

1. **"Le contraste C2 contre C3 est le plan qui manque a la litterature et il valide la these de
   a15."** Le plan existe maintenant et **aucune des trois issues prevues n'est observee**. La
   phrase de synthese de a15 section 7.1, l'axe de segmentation separe les camps, ne suffit pas :
   dans la condition sans etiquette, aucun axe ne gonfle, ideologie comprise.
2. **"La temperature est isolable comme levier purement intra."** Vrai pour C2, faux pour C3, et
   confondu dans les deux cas avec le modele, la quantification et l'invite. Ne pas l'ecrire.
3. **Toute phrase suggerant que nos agents locaux valident la double distorsion comme propriete
   des modeles de langage.** C3 est dans le quadrant **inferieur gauche** de la figure
   `a18-figure-c2-c3.png`, avec `v6` et `v7` : les deux termes ecrases, pas de gonflement. Seul
   C2 est dans le quadrant de la double distorsion, avec `v8`. **Deux de nos deux conditions ne
   font pas la meme chose, et une seule soutient la these.** [MESURE]
4. **Le chiffre de a18 sur le critere A6, C2 a r = 0,638.** Il tombe a 0,246 sur 150 personnes.
   Tout chiffre de la trace partielle repris ailleurs doit etre reverifie.
5. **L'espoir que C3F retourne l'objection 1 de a17.** Arithmetiquement : C3F retire du contexte
   la famille entiere de l'item cible, donc **C3F est necessairement inferieur ou egal a C3 sur
   ces memes 58 items**, ou C3 vaut **0,6249** sur nos 150 personnes [MESURE,
   `a23-ecarts-apparies.csv`]. La cible est **0,6621**, la ligne "B2 famille retiree (argmax)"
   toutes familles reunies de `a8-familles-gss.csv`. **C3F ne peut pas atteindre 0,6621**, sauf
   effet de sous echantillon d'environ quatre points. La phrase "les agents battent B2" sort du
   dossier, sous reserve du chiffre reel. [PROBABLE, sur une inegalite qui ne peut jouer que
   dans un sens]

### 6.3 Les experiences qui deviennent prioritaires, dans l'ordre

| rang | experience | ce qu'elle tranche | cout machine | source du chiffrage |
|---|---|---|---|---|
| 1 | **Un modele plus gros en local, gpt-oss-20b ou Qwen3-30B-A3B, sur C2 et C3** | si la quasi degenerescence, l'ECE de 0,44 et surtout l'absence de gonflement de C3 sont des proprietes de Qwen3-4B Q4 ou du regime sans etiquette | **11 h 48 sur gpt-oss-20b, 13 h 36 sur Qwen3-30B-A3B** pour les deux conditions, une nuit pour C2 seule | a3 tableau 4.2 : 9 569 et 8 340 appels/h contre 18 060 pour Qwen3-4B, applique aux debits reels de a5, 13 217 et 4 886 [ESTIMATION] |
| 2 | **La temperature, balayage a modele constant sur C2** | isole le levier temperature sur l'intra, seul moyen de sauver le contraste 4 de a15 | quelques heures, la distribution est deja lue, seule la relecture change | a18 section 6, la version 3 se calcule sans un appel |
| 3 | **La fin de C3F** | la seule reponse propre a l'objection 1 de a17 ; le chiffre attendu est sous 0,6249 | **3 h 24** au debit mesure de 2 556 appels/h, resumable | `a5-familles.log`, ligne 05:16:06 |
| 4 | **La passe 2 de C3** | l'ampleur du biais de position, inconnue, sur des items ou le modele colle a une modalite dans 43 items sur 149 | une nuit sur le GSS | a5 section 6 |
| 5 | **L'extension de C2 a 300 personnes** | elle perd son urgence : le controle passe deja a 150 sur les axes qui portent l'effet | 2 h 03 | a21 |

**Le rang 2 monte et le rang 5 descend par rapport a SYNTHESE-NUIT.** La question de la taille
d'echantillon est partiellement reglee par le controle ; la question du modele et de la
temperature ne l'est pas, et elle porte desormais le resultat principal.

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. **Que le deficit de dispersion totale n'est pas un artefact de decodage**, mesure sur
   44 700 appels et deux regimes d'invite : 0,654 vers 0,668 et 0,674 vers 0,693, temperature
   necessaire 6,29 et 6,27.
2. **Que l'etiquette ideologique dans l'invite est de premier ordre sur le terme inter**, avec
   intervalles : 8,16 [5,43 ; 15,55] pour C2, 0,73 [0,47 ; 0,99] pour C3, sur les memes
   personnes, les memes items, le meme modele et la meme temperature. C'est la replication
   interne du fait que a19 a etabli sur l'archive.
3. **Que le terme inter est estimable a 150 personnes sur l'axe ideologie**, controle vague 2 a
   1,11 [0,93 ; 1,41] en entropie et 1,01 [0,86 ; 1,20] en Gini Simpson.
4. **Que le modele est certain et faux**, avec la version appel et la version population :
   ECE 0,441, exactitude 0,545 dans le decile a 0,995 de confiance, et une modalite couvrant plus
   de 90 pour cent de la population sur 46 items sur 149 pour C2 et 43 pour C3, contre 13
   chez les humains.
5. **Qu'un modele local de 4 milliards de parametres en 4 bits ne se justifie pas sur le couple
   exactitude et diversite** : il est domine sur les deux axes par une regression logistique.
6. **Que la version distributionnelle de la decomposition est une generalisation exacte de la
   version ponctuelle**, controle a 0,000e+00 sur 150 personnes.

### Interdit

1. **Ecrire que nos agents valident la double distorsion.** Une de nos deux conditions la
   valide, l'autre la contredit. Toute phrase globale sur "nos agents" est fausse.
2. **Lire les colonnes race et education des tableaux par axe.** Le controle de la vague 2 y a
   un intervalle contenant des valeurs negatives. Le genre est a ne pas publier seul.
3. **Presenter C2 comme une replication de l'agent demographique de Stanford.** Son homologue est
   `v8`, pas `v6`. [CONFIRME, a17 objection 3]
4. **Comparer les valeurs absolues de `delta eta carre` a celles de Chen.** Signe et classement
   seulement.
5. **Annoncer la famille des libertes civiles comme un regime ou le modele de langage local
   gagne.** Elle a ete choisie apres avoir vu les chiffres, sur 36 comparaisons sans correction,
   et C3 n'y est distinguable ni de B2 ni des agents de Stanford.
6. **Attribuer a la temperature l'ecrasement intra de C2.** Trois variables changent en meme
   temps.
7. **Reprendre un chiffre de la trace partielle de a18.** Le critere A6 de C2 passe de 0,638 a
   0,246, le controle inter de 1,167 a 1,046, la temperature de 5,71 a 6,29.

---

## Ce que je n'ai pas pu verifier

1. **C3F n'a pas tourne.** Onze personnes completes a 05:17, projection de 57 sur 150 a l'heure
   dure de 06:20. La ligne C3F qui apparait dans les sorties de `a23_regime_de_validite.py`,
   0,5701 sur les 58 items, est calculee sur ces onze personnes et n'a aucune valeur. **La
   comparaison stricte C3F contre "B2 famille retiree" a 0,6621 reste a faire.**
2. **L'extension de C2 a 300 personnes n'a pas tourne.** La question "le controle se resserre t
   il en passant de 150 a 300" n'est donc pas testee ; elle est seulement devenue moins urgente.
3. **Le biais de position n'est pas mesure.** La passe 2 de C3 n'existe pas. Sur des items ou une
   seule modalite est predite pour plus de 90 pour cent des personnes dans 43 cas sur 149, ce
   biais peut etre important et il est inconnu.
4. **Les prompts de C2 et C3 n'ont pas ete compares a ceux de `v8` et des agents enquete.** Toute
   la section 2 attribue au modele un ecart qui peut venir de la formulation. C'est la limite la
   plus serieuse de ce rapport.
5. **Un seul modele.** Qwen3-4B-Instruct-2507 en Q4_K_M. L'absence de gonflement de C3, qui est
   le resultat le plus interessant, peut etre une incapacite du modele plutot qu'une propriete du
   regime sans etiquette. Rien ne separe les deux tant qu'un second modele n'a pas tourne.
6. **Aucune correction pour tests multiples nulle part.** 36 comparaisons par famille, 12 axes
   fois conditions par mesure, 2 mesures. La famille d'hypotheses n'est toujours pas fixee.
7. **Les intervalles par axe sont recentres, comme dans a1 et a18.** C'est un intervalle de
   percentile translate sur l'estimation ponctuelle, pas un bootstrap de base. Le point de a19
   errata E3 vaut ici aussi.
8. **Le seuil d'occupation de Miller Madow reste un degre de liberte** sur la voie
   distributionnelle en entropie : inter 132,30 au seuil 1 contre 82,78 au seuil 0 pour C2, et
   33,41 contre -9,91 pour C3 [MESURE, `evaluation-matin.log`]. Gini Simpson y est insensible et
   donne le meme signe et le meme classement, ce qui est le controle attendu, mais le choix n'est
   pas source.
9. **Les 30 rejets de C3 n'ont pas ete retires de l'evaluation.** Effet estime negligeable, non
   mesure.
10. **La selection de la famille des libertes civiles est post hoc.** Aucune preinscription,
    aucune replication.

---

## Questions ouvertes pour Simon

1. **C3 ne gonfle rien. Est ce un resultat ou une incapacite ?** C'est la question la plus
   importante du rapport. Si un modele plus gros dans le meme regime sans etiquette gonfle comme
   les agents enquete de Stanford, alors l'essentialisme identitaire est une propriete qui
   apparait avec la capacite, ce qui est un resultat fort et publiable. S'il ne gonfle pas non
   plus, alors le gonflement du regime questionnaire est une propriete de la chaine de Stanford,
   invite comprise, et le papier change de cible. Une nuit de calcul tranche. Laquelle des deux
   hypotheses le projet doit il chercher a falsifier en premier ?
2. **Les trois issues de a15 sont fausses toutes les trois. Faut il republier la question ou
   publier la quatrieme issue ?** Ce qui est observe est un emboitement : l'etiquette commande le
   signe, l'axe commande la repartition a l'interieur de la condition etiquetee. C'est plus vrai
   et moins vendeur que "l'axe de segmentation separe les camps".
3. **Nos agents sont domines par une regression logistique sur les deux axes du plan. Que fait on
   de ce chiffre dans le papier ?** Le cacher est impossible, un relecteur le refera. Le publier
   affaiblit toute revendication de simulation. La position defendable est que le papier ne porte
   pas sur la performance mais sur la mesure de structure, et que nos agents servent de banc a
   information controlee, pas de proposition de simulation. Est ce tenable ?
4. **Faut il garder la famille des libertes civiles dans le dossier ?** Elle est le seul endroit
   ou notre agent est en tete, elle a ete trouvee apres coup, et elle n'est distinguable ni de B2
   ni des agents de Stanford. La garder demande une replication preinscrite sur un autre
   decoupage ; la retirer laisse le rapport sans aucun regime favorable.
5. **Les 25 rejets sur `income` posent une question de protocole.** La regle de scoring par
   lettre unique perd sa masse au dela de sept ou huit modalites. Faut il retirer `income` des
   149 items, comme a19 le suggerait deja pour une autre raison, ou changer de regle de scoring
   pour les items a plus de huit modalites, ce qui casse la comparabilite avec a2 ?
6. **La deviance de C2 et de C3 depasse celle des humains, 0,409 et 0,429 contre 0,396, et leurs
   correlations sont les plus basses du tableau.** Aucune condition de Stanford ne fait cela. Un
   agent qui s'ecarte du mode de son groupe plus que les vraies personnes, et pas pour les memes
   personnes, n'est pas decrit par la litterature, qui ne parle que d'ecrasement. Est ce une
   propriete du petit modele, un artefact des items ou le modele impose sa propre modalite
   (`nataid/y`, `dwelown16`, `divlaw`), ou un phenomene a nommer ?

---

## Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# les deux sorties du matin, deja produites, journal complet dans data/traces/evaluation-matin.log
.venv/bin/python analyses/a5_evaluer.py
.venv/bin/python analyses/a18_decomposition_traces.py

# les deux ajouts de ce rapport
.venv/bin/python analyses/a23_regime_de_validite.py
.venv/bin/python analyses/a23_axes_ic.py
```

Aucun appel de modele de langage, traces ouvertes en lecture seule, aucune microdonnee hors de
`data/`. Les fichiers `a23-*.csv` sont exclus par `.gitignore` comme les autres CSV : les
chiffres qui comptent sont recopies ci dessus.
