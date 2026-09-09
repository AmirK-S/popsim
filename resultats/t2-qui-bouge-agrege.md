# T2. Qui bouge, version agregee. Le signal de groupe sur les panels GSS, et le nul a derive transporte de C1

Rapport du 9 septembre 2026. Il execute la version agregee du programme C de
`MOONSHOTS.md`, « combien bougent et dans quel groupe », et transporte sur les panels GSS
le resultat neuf de `c1-anticipations-sce.md` section 6.3, « le nul a derive fait bouger les
menages deux fois trop ».

**Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Aucun fichier
existant, script ou tableau, n'a ete modifie** ; `i1_commun.py`, `a12_retest_delai.py`,
`a2_commun.py`, `a2_baselines_gss.py`, `a30_commun.py` et `a44_commun.py` (par i1) sont
importes tels quels, memes items, memes seuils, memes definitions. Le `llama-server` de R2
n'a pas ete sollicite. Cinq scripts nouveaux : `analyses/t2_commun.py`, `t2_agrege.py`,
`t2_amplitude.py`, `t2_camps.py` et `t2_figure.py`.

**Le preenregistrement est `resultats/t2-preenregistrement.md`, ecrit le 9 septembre 2026 a
01 h 05 CEST (8 septembre a 23 h 05 UTC), depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant l'ecriture du premier script de T2 et
avant tout calcul.** Les quatre volets, les groupes, les deux cibles de deplacement, les six
modeles, le dispositif en demi echantillons, six predictions, cinq controles bloquants et
trois regles de decision y sont figes. Il n'a pas ete modifie depuis.

Sorties : `t2-controles-volet1.csv`, `t2-controles-volet2.csv`, `t2-controles-volet3.csv`,
`t2-groupes.csv`, `t2-modeles.csv`, `t2-contrastes.csv`, `t2-variance-inter-groupes.csv`,
`t2-plafond.csv`, `t2-permutation-groupes.csv`, `t2-erreur-par-item.csv`,
`t2-par-groupe-item.csv`, `t2-amplitude.csv`, `t2-amplitude-par-famille.csv`,
`t2-ordinaux.csv`, `t2-camps.csv`, `t2-changeurs-deciles.csv`,
`t2-figure-qui-bouge-agrege.png` et `.svg`. **Aucune microdonnee.**

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee non demontree, **[HYPOTHESE]**
proposition a tester.

---

## Reponse en une ligne

**Le signal de groupe existe, il est fort, et il porte sur qui change et jamais sur le sens
du changement.** Sur les quatre panels GSS a quatre ans, 4 683 personnes, 118 items et 53
groupes, le profil de taux de changement d'un groupe se reproduit d'une moitie de
l'echantillon a l'autre avec une correlation de **0,596** en moyenne, **0,603 pour les camps
ideologiques**, contre une bande de permutation d'etiquette qui plafonne a 0,12 au 95e
centile, `p` de permutation nul sur les quatre axes apres Holm ; et un modele qui ne connait
que la vague 1 et les demographies ramene l'erreur du nul a derive de **3,74 a 2,78 points**,
soit un gain de **0,96 point** et une part de variance inter groupes expliquee de **0,447**
pour un plafond de bruit de **0,638**, c'est a dire **70 pour cent de ce qui est
atteignable**. [MESURE]

**Sur le sens du deplacement, il n'y a rien a vendre.** Le meme test donne une correlation
inter moities de **0,118 pour les camps**, a l'interieur de la bande de permutation
(`p = 0,064`, `p` de Holm **0,192**, non retenu), 0,063 pour l'education et 0,159 pour le
genre ; **seul l'axe d'age sort**, 0,383, `p` de Holm nul. Et aucun modele ne bat le nul a
derive : le meilleur, l'additif item plus groupe, gagne **0,0025 point** d'erreur absolue
pour `p = 0,57`. **Sur un meme item, les camps ne bougent pas dans des sens differents au
dela de la derive globale ; les generations, si.** [MESURE]

**Le « bouge deux fois trop » de C1 se transporte en direction mais pas en valeur.** Le nul a
derive qui conserve les deux marginales et detruit l'appariement des personnes fait changer
les repondants du GSS sur **51,9 pour cent** de leurs items contre **32,4** reellement,
rapport **0,625** [0,621 ; 0,629] ; sur la distance de changement des items ordinaux,
rapport **0,598** [0,594 ; 0,604]. C'est **1,6 fois trop**, pas deux, la ou le SCE donnait
**2,3 fois trop** (rapport 0,43 a 0,55). Le rapport n'est pas une constante : par famille
d'items il va de **0,389** sur l'avortement a **0,735** sur la confiance dans les
institutions. **L'enonce qui survit est : une population sans personnes bouge toujours trop,
d'un facteur 1,4 a 2,6 selon le sujet.** [MESURE]

**Et le camp le moins varie de a30 est bien celui qui bouge le moins, mais cela ne survit pas
au changement d'ancrage.** La gauche change sur 31,47 pour cent de ses items, la droite
32,38, le centre 33,00, ecart maximal **1,53 point** ; avec l'ancrage partisan, plus fiable,
l'ordre gauche droite s'inverse. **Ce qui survit aux deux ancrages, c'est que le centre bouge
le plus** : les changeurs du decile superieur sont sur representes de **1,40** [1,19 ; 1,60]
chez les independants sans preference, et les gens les plus stables sont a gauche,
sur representation de **1,60** [1,46 ; 1,75] dans le decile inferieur. [MESURE]

---

## 1. Les controles bloquants, executes avant toute lecture

[MESURE, `t2-controles-volet1.csv`, `t2-controles-volet2.csv`]

| controle | attendu | obtenu | passe |
|---|---|---|---|
| **C1** consistance a deux ans, noyau commun, valeur de a12 | 0,695267 | **0,695267** | oui |
| **C1** consistance a quatre ans, noyau commun, valeur de a12 | 0,674471 | **0,674471** | oui |
| **C2** items du noyau commun | 118 | **118** | oui |
| **C2** personnes, perimetre a quatre ans | 4 683 | **4 683** | oui |
| **C3** marginale d'arrivee conservee par le nul, quatre variantes | ecart 0 | **0,0 exactement** | oui |
| **C4** items marques ordinaux par le `question_master`, retenus | publie | 63 marques, **63 retenus** | oui |
| **C5** coupures 50 / 50 disjointes | oui | **oui** | oui |
| **C5** effectif minimal d'une cellule retenue, cote A | au moins 50 | **50** | oui |
| groupes retenus au seuil de 200 personnes | publie | **53** | oui |

C1 passe **a la sixieme decimale**, en repassant par `a12_retest_delai.consistance` et non par
ses tableaux. Tout ce qui suit porte donc sur exactement les memes personnes, les memes items
et les memes conventions de manquants que `a12-delai-de-retest.md` et que
`i1-qui-bouge-humains.md`.

**Un controle de plus, non demande, et il vaut validation du generateur nul.** Pour des items
categoriels, le taux de changement attendu du nul N1 a une **forme close** : c'est
`1 - somme_m p1(m) p2(m)`, ou `p1` et `p2` sont les deux marginales de l'item dans le panel.
Calculee analytiquement elle donne **0,519329** ; les 50 replicats de permutation donnent
**0,519338**. L'ecart vaut neuf millioniemes. [MESURE] **Consequence pratique : sur des items
categoriels, le nul a derive ne demande aucun tirage, il se calcule au crayon depuis les deux
marginales.**

---

## 2. Protocole, en clair

**Les items et les perimetres.** Le noyau commun de 118 items de a12, recalcule par appel de
ses fonctions. Perimetre primaire : les quatre paires a quatre ans, 4 683 personnes disjointes
d'un panel a l'autre. Perimetre secondaire : les quatre paires a deux ans, 5 682 personnes.
Manquants exclus comme en a12 : les taux publies sont des **minorants**.

**Les groupes.** Camp ideologique (`polviews` en trois blocs), age, education (`degree`),
genre, et leurs six croisements, tous construits sur la **vague de depart seulement** avec les
fonctions de `i1_commun`. Un groupe entre au dessus de 200 personnes, une cellule (groupe,
item) au dessus de 50 personnes **de chaque cote** de la coupure. **53 groupes** retenus, du
plus gros (`education = bas`, 2 838 personnes) au plus petit. Le camp partisan n'entre qu'au
volet 3, comme controle d'ancrage.

**Les deux quantites a predire.** Pour un groupe `g` et un item `j` :

- **`tau(g, j)`, le taux de changement**, en points ;
- **`pi(g, j)`, le deplacement projete sur la derive**, en points : la variation de part de
  chaque modalite dans le groupe, projetee sur la direction de la derive globale de l'item.
  Elle est definie pour les 118 items, ne suppose aucune ordinalite, et **son signe dit si le
  groupe bouge avec ou contre la derive globale** ;
- **`mu(g, j)`, le deplacement ordinal**, en points d'echelle, pour les 63 items marques
  ordinaux par le `question_master` de Stanford, sur le code numerique brut du GSS.

**Le dispositif.** Cinq coupures 50 / 50 des personnes, stratifiees par panel. Les modeles
sont ajustes sur la moitie A, la cible est **observee sur la moitie B**. Aucune personne des
deux cotes. Ce dispositif est ce qui rend la comparaison honnete : la cible est elle meme une
estimation, et un modele qui aurait appris le bruit d'une cellule serait puni.

**Les six modeles.** M0, le **nul a derive**, connait la derive agregee de l'item et rien des
groupes. M1, **segment seul**, connait le groupe et rien de l'item. M2, **additif item plus
groupe**. M3, **`P` agrege** : la matrice de transition par modalite de vague 1 estimee sur A
sans regarder les groupes, appliquee aux reponses de vague 1 des personnes de B et moyennee
dans la cellule ; c'est le predicteur `P` de I1 transporte a l'agrege, et il connait le groupe
**uniquement par sa composition**. M4, **`P` agrege plus decalage de groupe**, le modele « qui
connait la vague 1 et les demographies » du cahier des charges. M5, **oracle empirique de
cellule** : la valeur observee de la meme cellule dans l'autre moitie.

---

## 3. Volet 1. La version agregee de « qui bouge »

### 3.1 Le tableau

[MESURE, `t2-modeles.csv` et `t2-contrastes.csv`, 6 175 cellules (groupe, item) retenues pour
`tau` et `pi`, 3 320 pour `mu`, moyenne sur cinq coupures, bootstrap sur les personnes de la
moitie d'evaluation, 400 tirages]

| cible | modele | erreur absolue moyenne | ecart type bootstrap | **gain sur le nul** | `p` de Holm | **part de variance inter groupes expliquee** |
|---|---|---|---|---|---|---|
| **`tau`** taux de changement, points | M0, nul a derive | **3,744** | 0,034 | reference | | 0,000 |
| | M1, segment seul | 12,009 | 0,049 | -8,265 | 0,0125 | -7,258 |
| | M2, additif item + groupe | 3,347 | 0,031 | **+0,397** | **0,0125** | 0,197 |
| | M5, oracle empirique de cellule | 3,341 | 0,027 | **+0,403** | **0,0125** | 0,195 |
| | M3, `P` agrege | 3,100 | 0,032 | **+0,644** | **0,0125** | 0,311 |
| | **M4, `P` agrege + decalage** | **2,782** | 0,029 | **+0,962** | **0,0125** | **0,447** |
| | *plafond de bruit* | | | | | *0,638* |
| **`pi`** deplacement projete, points | M0, nul a derive | **3,640** | 0,038 | reference | | 0,000 |
| | M2, additif item + groupe | 3,638 | 0,038 | +0,0025 | **0,570** | 0,003 |
| | M1, segment seul | 4,211 | 0,042 | -0,570 | 0,0125 | -0,273 |
| | M5, oracle empirique de cellule | 4,529 | 0,038 | -0,889 | 0,0125 | -0,583 |
| | M4, `P` agrege + decalage | 4,627 | 0,043 | -0,986 | 0,0125 | -0,670 |
| | M3, `P` agrege | 4,666 | 0,044 | -1,026 | 0,0125 | -0,689 |
| | *plafond de bruit* | | | | | *0,308* |
| **`mu`** deplacement ordinal, points d'echelle | M0, nul a derive | **0,0508** | 0,0007 | reference | | 0,000 |
| | M2, additif item + groupe | 0,0510 | 0,0007 | -0,0002 | **0,180** | -0,005 |
| | M5, oracle empirique de cellule | 0,0610 | 0,0007 | -0,0103 | 0,0125 | -0,466 |
| | M4, `P` agrege + decalage | 0,0706 | 0,0008 | -0,0199 | 0,0125 | -0,881 |
| | M3, `P` agrege | 0,0712 | 0,0008 | -0,0204 | 0,0125 | -0,909 |
| | *plafond de bruit* | | | | | *0,369* |

Le `p` de bootstrap est plancher a `1 / 401 = 0,002494` ; Holm sur les cinq contrastes d'une
cible donne `0,01247`, donc la correction est **satisfiable ici**, contrairement a ce qui
s'etait produit dans I1 ecart E4.

**Sur l'usage des intervalles.** Les intervalles de bootstrap d'une **erreur absolue moyenne**
sont deplaces vers le haut, parce que reechantillonner les personnes ajoute du bruit a la
cible et gonfle mecaniquement l'erreur : la moyenne de bootstrap de M0 vaut 4,44 pour une
valeur ponctuelle de 3,74. Les colonnes d'intervalle percentile et pivotal sont publiees dans
`t2-modeles.csv` et `t2-contrastes.csv`, mais **ce qui se lit est l'ecart type de bootstrap et
le signe du contraste apparie**, ou le deplacement s'annule en grande partie. Le verdict de la
section repose sur le test de permutation de la section 3.3, qui n'a pas ce defaut. Ecart E2.

### 3.2 Ce que le tableau dit, en quatre lignes

**Un.** **Il existe un signal de groupe sur qui change, et il est loin d'etre negligeable.**
Le nul a derive se trompe de 3,74 points sur le taux de changement d'une cellule (groupe,
item) ; un modele qui ne voit que la vague 1 et les demographies se trompe de 2,78, soit **26
pour cent d'erreur en moins**. Il est meilleur que le nul sur **107 des 118 items**.

**Deux.** **Ce signal est previsible, et presque completement.** Le plafond de bruit dit que
seulement 63,8 pour cent de la variance inter groupes observee dans une moitie fraiche est du
signal, le reste etant du bruit d'echantillonnage. M4 en capte 0,447, soit **70 pour cent de
ce qui est atteignable**. C'est un resultat different de celui de I1 : au niveau individuel,
la foret ne battait le predicteur a une ligne que de 0,039 point d'AUC ; **au niveau agrege,
ajouter l'etiquette de groupe a la seule composition en vague 1 rapporte encore 0,318 point
d'erreur absolue** (2,782 contre 3,100) **et 0,136 point de variance inter groupes expliquee**
(0,447 contre 0,311). Le groupe ajoute quelque chose que sa composition ne dit pas.

**Trois.** **La composition en vague 1 fait deja la moitie du travail.** M3, qui ne connait
aucune etiquette de groupe et se contente d'appliquer une matrice de transition par modalite,
obtient 0,311 de variance expliquee. Autrement dit, **une bonne part de ce qui distingue le
taux de changement d'un camp de celui d'un autre est simplement que les deux camps ne tiennent
pas les memes reponses en vague 1**, et que certaines reponses sont plus instables que
d'autres. C'est le resultat central de I1, « ce qui est previsible, c'est l'instabilite de la
cellule », qui remonte intact d'un etage.

**Quatre.** **M5 n'est pas un plafond, et le preenregistrement avait tort de le presenter
ainsi.** L'oracle empirique de cellule est **sans biais mais bruite** : il porte tout le bruit
d'echantillonnage de la moitie A. Il bat le nul, ce qui prouve l'existence du signal, mais il
se fait battre par M4, qui est un estimateur lisse. Le vrai plafond est le rapport signal sur
bruit, publie dans `t2-plafond.csv`. Ecart E1.

### 3.3 Le test qui porte le verdict : les groupes different ils de facon reproductible ?

C'est la question de la mission dans sa forme la plus directe, et elle se pose sans aucun
modele. Pour chaque cellule (groupe, item), on calcule l'ecart du groupe a la moyenne de
l'item **dans chaque moitie separement**, puis la correlation de ces deux ecarts sur toutes
les cellules. Sous un decoupage sans contenu elle vaut zero en esperance. La bande de
comparaison est produite en permutant l'etiquette de groupe entre les personnes du meme
panel, **1 000 permutations** (200 par coupure, cinq coupures).

[MESURE, `t2-permutation-groupes.csv`, panneau C de la figure]

| axe | cible | **correlation entre les deux moities** | 95e centile de la permutation | `p` de permutation | `p` de Holm sur les douze |
|---|---|---|---|---|---|
| **camp** | **qui change** | **0,603** | 0,117 | < 0,001 | **0,000** |
| age | qui change | **0,717** | 0,123 | < 0,001 | **0,000** |
| education | qui change | **0,750** | 0,122 | < 0,001 | **0,000** |
| genre | qui change | **0,567** | 0,176 | < 0,001 | **0,000** |
| **camp** | **sens du deplacement** | **0,118** | 0,129 | 0,064 | **0,192, non retenu** |
| age | sens du deplacement | **0,383** | 0,127 | < 0,001 | **0,000** |
| education | sens du deplacement | 0,063 | 0,140 | 0,249 | 0,320, non retenu |
| genre | sens du deplacement | 0,159 | 0,179 | 0,073 | 0,192, non retenu |
| **camp** | deplacement ordinal | 0,294 | 0,205 | 0,010 | **0,060, non retenu** |
| age | deplacement ordinal | **0,548** | 0,200 | < 0,001 | **0,000** |
| education | deplacement ordinal | 0,159 | 0,210 | 0,099 | 0,320, non retenu |
| genre | deplacement ordinal | 0,234 | 0,268 | 0,078 | 0,320, non retenu |

**Lu en clair.** Sur **qui change**, les quatre axes sortent massivement de la bande, et le
camp ideologique sort a 0,603 pour une bande a 0,117. **Les camps changent effectivement a des
taux differents sur un meme item, et cette difference se reproduit.** Sur **le sens du
deplacement**, un seul axe sort : **l'age**. Le camp est a 0,118 pour une bande a 0,129 ; il
est litteralement dans le bruit. L'education n'y est meme pas, le genre est a la limite.

C'est la reponse a la question decisive de la mission, et elle est en deux temps :
**les camps bougent differemment, mais differemment en quantite, pas en direction.**

### 3.4 A quoi cela ressemble, item par item

[MESURE, `t2-par-groupe-item.csv`, premiere coupure, taux de changement observe dans la moitie
d'evaluation, en points]

| item | libelle abrege | gauche | centre | droite | ecart |
|---|---|---|---|---|---|
| `xmarsex` | relations extraconjugales | **32,7** | 23,9 | **15,7** | **17,0** |
| `nateduc/y` | depenses d'education | 20,1 | 23,0 | **33,7** | 13,6 |
| `natenvir/y` | depenses pour l'environnement | 27,6 | 32,6 | **40,1** | 12,5 |
| `conpress` | confiance dans la presse | **47,5** | 40,8 | 35,5 | 12,0 |
| `colcom/y` | un communiste peut il enseigner | 25,5 | 37,3 | 33,7 | 11,8 |
| `confed` | confiance dans l'executif federal | **58,4** | 47,7 | 52,5 | 10,7 |

L'ecart droite moins gauche, item par item, **se reproduit d'une moitie a l'autre a
`r = 0,737`** pour le taux de changement, contre `r = 0,321` pour le deplacement projete et
`r = 0,422` pour le deplacement ordinal. [MESURE]

Les items ou le predicteur de groupe gagne le plus sont `income` (erreur du nul 8,57 points,
erreur de M4 1,80), `spkcom/y`, `xmarsex`, `spkath/y`, `libcom/y`, `news` et `wrkstat`.
**La reserve de I1 section 4.4 s'applique ici sans attenuation** : `income` et `wrkstat` ne
sont pas des opinions, ce sont des trajectoires de vie, et une part du gain de M4 sur eux est
un effet de bord de l'echelle et de la composition demographique des groupes, pas une
propriete de l'opinion.

### 3.5 Ou le nul a derive reste imbattable

Sur le **deplacement projete**, M4 bat M0 sur seulement **30 items sur 118** ; sur le
deplacement ordinal, **11 sur 63**. Le seul modele qui ne perd pas est l'additif item plus
groupe, et il gagne 0,0025 point sur 3,64, ce qui est indistinguable de zero (`p = 0,57`).

Ce resultat est le prolongement exact, a l'etage du groupe, de ce que I1 avait etabli a
l'etage de la personne et C1 a l'etage du menage : **la direction d'un mouvement d'opinion est
une propriete de l'item, pas de qui le porte.** I1 : « l'exces de changement monotone est
reproduit a 106 pour cent par un nul sans structure individuelle ». C1 : « sur les neuf
variables l'exces va de -7,6 a +5,1 points, ce qui est un tirage a pile ou face ». T2 ajoute
la marche du milieu : **meme en agregeant a des groupes de plusieurs centaines de personnes,
et meme en donnant au modele la composition complete de la vague 1, on ne sait pas dire dans
quel sens un camp va se deplacer sur un item au dela de la derive de tout le monde.**

**La seule exception mesuree est l'age**, correlation inter moities 0,383 sur le sens, `p` de
Holm nul. C'est le seul endroit du rapport ou une population synthetique aurait quelque chose
a rendre sur la direction, et c'est celui ou la lecture substantielle est la plus banale :
les generations ne se deplacent pas comme les autres, ce qui est la definition d'un effet de
cohorte. [MESURE]

---

## 4. Volet 2. Le nul a derive de C1 transporte sur le GSS

### 4.1 Le rapport

[MESURE, `t2-amplitude.csv`, 50 replicats, bootstrap sur les personnes, 400 tirages, panneau B
de la figure. N1 remelange la vague d'arrivee dans le panel ; N2 la remelange dans le segment
`ideologie x age x education`, pendant exact de la cohorte de C1]

| perimetre | generateur | quantite | **reel** | **nul** | **rapport** | IC 95 pour cent |
|---|---|---|---|---|---|---|
| quatre ans | N1, panel | nombre d'items changes | 0,3244 | 0,5193 | **0,625** | [0,621 ; 0,629] |
| quatre ans | N1, panel | distance ordinale | 0,5057 | 0,8450 | **0,598** | [0,594 ; 0,603] |
| quatre ans | N2, segment | nombre d'items changes | 0,3244 | 0,4906 | **0,661** | [0,657 ; 0,665] |
| quatre ans | N2, segment | distance ordinale | 0,5057 | 0,7965 | **0,635** | [0,630 ; 0,640] |
| deux ans | N1, panel | nombre d'items changes | 0,3103 | 0,5206 | **0,596** | [0,593 ; 0,600] |
| deux ans | N1, panel | distance ordinale | 0,4790 | 0,8460 | **0,566** | [0,562 ; 0,570] |
| deux ans | N2, segment | nombre d'items changes | 0,3103 | 0,4915 | **0,631** | [0,628 ; 0,635] |
| deux ans | N2, segment | distance ordinale | 0,4790 | 0,7962 | **0,602** | [0,598 ; 0,606] |

Par panel, le rapport a quatre ans sous N1 va de **0,615** (2008-2012) a **0,637**
(2006-2010) ; a deux ans, de 0,585 a 0,613. La dispersion entre panels est de trois points,
donc le fait est stable d'un echantillon a l'autre.

### 4.2 Ce que cela dit du resultat de C1

**Le phenomene se transporte, sa valeur non.** C1 avait mesure sur neuf variables du SCE un
rapport de **0,427 a 0,554**, soit un nul qui fait bouger les menages **deux fois trop**. Sur
le GSS, le meme nul fait bouger les repondants **1,6 fois trop**, rapport 0,625, et 1,5 fois
trop sur la distance de changement ordinale, rapport 0,598.

**La prediction P1 est donc fausse d'un cheveu** : elle annoncait le rapport entre 0,35 et
0,60, il vaut 0,625. La regle de decision 3 du preenregistrement s'applique a la lettre : **la
quantite de C1 ne se transporte pas telle quelle et ne doit pas etre publiee comme une
constante**. Ce qui doit etre publie, c'est l'enonce plus faible et plus solide : **une
population dont chaque personne est retiree dans la loi de son groupe bouge systematiquement
trop, et le facteur mesure sur deux jeux de donnees, deux instruments et deux natures de
variable va de 1,4 a 2,6.**

**Le detail par famille montre pourquoi une constante etait une mauvaise idee.**

[MESURE, `t2-amplitude-par-famille.csv`, quatre ans, generateur N1]

| famille d'items | n items | reel | nul | **rapport** | IC 95 pour cent |
|---|---|---|---|---|---|
| avortement (`ab*`) | 7 | 0,158 | 0,406 | **0,389** | [0,371 ; 0,408] |
| fin de vie (`suicide`, `letdie`) | 5 | 0,154 | 0,311 | **0,495** | [0,472 ; 0,518] |
| libertes civiles (`spk`, `col`, `lib`) | 11 | 0,222 | 0,376 | **0,591** | [0,574 ; 0,608] |
| depenses publiques (`nat*`) | 16 | 0,377 | 0,564 | **0,668** | [0,661 ; 0,675] |
| roles de genre (`fe*`) | 5 | 0,416 | 0,585 | **0,711** | [0,696 ; 0,726] |
| confiance dans les institutions (`con*`) | 13 | 0,419 | 0,570 | **0,735** | [0,724 ; 0,746] |

**La lecture est nette et elle est la meme que celle de a12 section 5.3 et de I1 section 3.6.**
La ou les gens tiennent une position morale, l'avortement et la fin de vie, l'appariement des
personnes est fort et un nul qui le detruit bouge deux fois et demie trop. La ou ils repondent
a une conjoncture, la confiance dans les institutions et les depenses publiques, l'appariement
est faible, les gens sont eux memes proches de leur propre marginale, et le nul ne se trompe
que d'un tiers. **Le rapport reel sur nul est une mesure de combien une opinion appartient a
la personne plutot qu'a la periode**, et les neuf variables du SCE, qui sont des anticipations
macroeconomiques, tombent dans la zone des positions morales. C'est un fait a expliquer et
non un fait explique. [PROBABLE]

**La prediction P2 est tenue** : le rapport est plus grand a quatre ans qu'a deux ans, 0,625
contre 0,596 sous N1, 0,661 contre 0,631 sous N2, 0,598 contre 0,566 sur la distance
ordinale. Le nul ne depend presque pas du delai, 0,519 a quatre ans et 0,521 a deux ans, ce
qui est attendu puisqu'il ne depend que des marginales ; c'est le reel qui monte avec le
delai. **Le nul est donc d'autant moins faux qu'on lui donne une fenetre longue** : a delai
infini, une population sans personnes et une population reelle deviennent indistinguables sur
cette mesure.

---

## 5. Volet 3. Le lien avec les camps

### 5.1 Le camp le moins varie est bien celui qui bouge le moins, et cela ne survit pas au changement d'ancrage

[MESURE, `t2-camps.csv`, perimetre a quatre ans, bootstrap sur les personnes, 400 tirages]

| ancrage | camp | n | **taux de changement** | IC 95 pour cent | distance ordinale | **rapport reel sur nul** |
|---|---|---|---|---|---|---|
| ideologie declaree | **gauche** | 1 334 | **0,3147** | [0,3095 ; 0,3196] | 0,499 | **0,609** |
| ideologie declaree | droite | 1 494 | 0,3238 | [0,3199 ; 0,3276] | 0,501 | 0,619 |
| ideologie declaree | **centre** | 1 718 | **0,3300** | [0,3266 ; 0,3340] | 0,510 | 0,640 |
| parti | **droite** | 1 519 | **0,3197** | [0,3162 ; 0,3237] | 0,493 | 0,615 |
| parti | gauche | 2 261 | 0,3230 | [0,3192 ; 0,3263] | 0,504 | 0,624 |
| parti | **centre** | 767 | **0,3414** | [0,3358 ; 0,3472] | 0,537 | 0,653 |

a30 etablit que **la gauche est le camp le moins varie des trois** sur les 149 items du GSS
transversal. T2 mesure que **la gauche est aussi le camp qui change le moins** sur les panels,
0,3147 contre 0,3238 a droite, un ecart de 0,91 point dont les intervalles ne se recouvrent
pas. **La prediction P5 est donc fausse dans sa premiere moitie**, elle annoncait le
contraire ; et tenue dans la seconde, l'ecart maximal entre camps vaut **1,53 point**, sous la
borne de deux points annoncee.

**Mais le controle d'ancrage refuse le resultat, et a30 avait pose la regle.** « Une
difference qui ne survit pas au changement d'ancrage n'est pas une difference entre camps,
c'est une difference d'echelle » [a30 section 1, sur le parti dont la fiabilite vaut 0,84
contre 0,66 pour l'ideologie declaree]. Avec l'ancrage partisan, c'est **la droite** qui
change le moins, 0,3197, et l'ecart gauche droite change de signe. **Le lien entre variete
interne et propension a changer n'est donc pas etabli** : il tient sur un ancrage et pas sur
l'autre, et l'ancrage sur lequel il tient est le moins fiable des deux. [MESURE]

**Ce qui survit aux deux ancrages, c'est le centre.** Il change le plus dans les deux
decoupages, 0,3300 et 0,3414, et son rapport reel sur nul est le plus haut, 0,640 et 0,653,
c'est a dire que **le centre est le groupe dont les personnes sont le moins appariees a elles
memes**.

### 5.2 Les changeurs se recrutent au centre, et les stables a gauche

[MESURE, `t2-changeurs-deciles.csv`, deciles du taux de changement individuel, perimetre a
quatre ans]

| ancrage | camp | part de la population | **sur representation dans le decile qui bouge le plus** | IC 95 pour cent | **sur representation dans le decile qui bouge le moins** | IC 95 pour cent |
|---|---|---|---|---|---|---|
| ideologie | centre | 0,367 | 1,029 | [0,918 ; 1,154] | 0,690 | [0,579 ; 0,788] |
| ideologie | droite | 0,319 | **0,828** | [0,713 ; 0,934] | 0,853 | [0,730 ; 0,982] |
| ideologie | gauche | 0,285 | 1,045 | [0,907 ; 1,184] | **1,600** | [1,459 ; 1,754] |
| **parti** | **centre** | 0,164 | **1,395** | [1,190 ; 1,602] | 0,670 | [0,505 ; 0,824] |
| parti | droite | 0,324 | **0,763** | [0,656 ; 0,872] | 0,865 | [0,753 ; 0,972] |
| parti | gauche | 0,483 | 1,033 | [0,946 ; 1,129] | **1,158** | [1,070 ; 1,242] |

**La reponse a la question « les changeurs se recrutent ils dans les camps ou dans le centre »
depend de l'ancrage, et l'ancrage fiable dit le centre.** Chez les independants sans
preference partisane, les gens du decile qui bouge le plus sont sur representes de **1,40**,
intervalle qui exclut 1 largement ; chez les moderes de l'ideologie declaree, la
sur representation vaut 1,03 et n'est pas distinguable de 1. Les deux ancrages s'accordent en
revanche pour dire que **la droite est sous representee parmi les changeurs**, 0,83 et 0,76,
et que **la gauche est sur representee parmi les stables**, 1,60 et 1,16.

Il faut lire ce tableau a cote de la section 5.1 de I1 : **le decile qui bouge le plus est
d'abord fait de gens qui tiennent des modalites rares et qui sont loin du patron modal de leur
segment**, et une part indeterminee de cette position est de l'erreur de mesure sur une
cellule rare, mesuree a 54,8 pour cent de fidelite a deux semaines par a42. **La
sur representation du centre parmi les changeurs peut donc etre, pour partie, une
sur representation du centre parmi les repondants imprecis.** C'est une reserve, pas une
refutation ; elle n'est pas levee ici. [PROBABLE]

---

## 6. La figure

`resultats/t2-figure-qui-bouge-agrege.png` et `.svg`, trois panneaux.

**A.** Un item, un point : erreur absolue du predicteur de groupe M4 contre celle du nul a
derive M0, en bleu pour le taux de changement et en rouge pour le deplacement projete. Le
nuage bleu est **sous** la diagonale, 107 items sur 118 ; le nuage rouge est **au dessus**,
88 items sur 118. C'est la figure de tout le rapport en une image.

**B.** Rapport reel sur nul par panel et par delai, avec la valeur d'ensemble du GSS a quatre
ans (0,625), celle du SCE mesuree par C1 (0,43) et la ligne d'egalite. Les seize points sont
groupes entre 0,56 et 0,64, tous tres loin de 1 et tous au dessus de la valeur du SCE.

**C.** Correlation des profils de groupe entre deux moities de l'echantillon, par axe et par
cible, avec le 95e centile de la permutation d'etiquette de groupe en trait noir. Les barres
bleues, qui change, dominent partout ; les barres rouges, sens du deplacement, ne depassent le
trait noir que sur l'axe d'age.

---

## 7. Le score des six predictions ecrites avant le calcul

[MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | rapport reel sur nul du nombre d'items changes entre 0,35 et 0,60 a quatre ans | **fausse**, 0,625 [0,621 ; 0,629], juste au dessus de la borne |
| **P2** | rapport plus grand a quatre ans qu'a deux ans | **tenue**, 0,625 contre 0,596, et sous les quatre combinaisons de generateur et de quantite |
| **P3** | M5 bat M0 d'au moins 0,3 point sur le taux de changement, retenu par Holm | **tenue**, +0,403 point, `p` de Holm 0,0125 |
| **P4** | part de variance inter groupes expliquee par le meilleur modele inferieure a 0,25 | **fausse**, M4 donne **0,447**, pour un plafond de 0,638 |
| **P5** | la gauche n'est pas le camp qui change le moins, et l'ecart entre camps est inferieur a 2 points | **moitie fausse, moitie tenue** : la gauche **est** le camp qui change le moins sous l'ancrage ideologique, 0,3147 ; l'ecart vaut 1,53 point |
| **P6** | aucun modele ne bat M0 sur le deplacement projete apres Holm | **tenue**, le meilleur gagne 0,0025 point pour `p = 0,570` |

Trois tenues, deux fausses, une a moitie. **P1 et P4 sont fausses dans deux sens opposes** :
le nul a derive est moins mauvais que je ne l'attendais sur l'amplitude, et le signal de
groupe est plus previsible que je ne l'attendais. Une famille de predictions qui se trompe
dans les deux sens est la seule preuve interne qu'elle a bien ete ecrite avant.

---

## 8. Les ecarts au preenregistrement

| | ecart | pourquoi |
|---|---|---|
| **E1** | **M5 avait ete declare comme un plafond, il n'en est pas un.** L'oracle empirique de cellule est sans biais mais porte tout le bruit d'echantillonnage de la moitie A ; il se fait battre par un estimateur lisse. Deux quantites nouvelles sont ajoutees : le **plafond de bruit**, `1 - variance de bruit / variance inter groupes totale`, et la **correlation des profils de groupe entre les deux moities**, avec son test de permutation. | Decouvert au premier calcul, avant toute lecture d'un contraste de modele : M4 battait M5, ce qui est impossible si M5 est un plafond. La regle de decision 1 du preenregistrement reste appliquee telle qu'elle est ecrite, M5 bat M0 et elle ne se declenche pas ; les deux quantites ajoutees ne servent qu'a mesurer ce que M5 ne pouvait pas mesurer. |
| **E2** | **Les intervalles de bootstrap sur les niveaux d'erreur absolue sont deplaces vers le haut** et ne sont pas lus. Trois colonnes sont publiees a la place d'une : percentile, pivotal et ecart type de bootstrap. | Reechantillonner les personnes ajoute du bruit a la cible, ce qui gonfle mecaniquement une erreur absolue. Le deplacement vaut 0,70 point pour un ecart type de 0,034, donc vingt ecarts types : ni l'intervalle percentile ni l'intervalle pivotal ne sont valides sur un niveau. Ils le sont beaucoup mieux sur le contraste apparie, et le verdict repose sur le test de permutation, qui n'a pas ce defaut. |
| **E3** | **Le test de permutation d'etiquette de groupe compte 1 000 tirages et non 200.** | Les 200 permutations declarees sont faites **par coupure**, et il y a cinq coupures ; les mille tirages sont mis en commun. Ecart favorable, il abaisse le plancher du `p` empirique de 1/201 a 1/1001 et rend Holm satisfiable. |
| **E4** | **Le test de permutation ne porte que sur les quatre axes simples**, pas sur les six croisements. | Cout de calcul, et les croisements sont deja couverts par la part de variance expliquee de `t2-variance-inter-groupes.csv`. |
| **E5** | **Le rapport par famille d'items n'est publie que sous le generateur N1 et sur le seul nombre d'items changes.** | Cout de calcul. La distance ordinale par famille aurait demande une seconde execution complete du nul. |
| **E6** | **Le volet 1 ne tourne que sur le perimetre a quatre ans.** Le perimetre a deux ans passe aux volets 2 et 3 seulement. | Cout de calcul, une seconde execution complete. C'est exactement l'ecart E6 de I1, non resorbe. La question « la previsibilite du signal de groupe depend elle du delai » reste ouverte. |
| **E7** | **`c1_commun` n'est pas importe, bien qu'il le soit sans effet de bord** (verifie). Le generateur nul est reecrit dans `t2_commun.nul_amplitude` en suivant la definition de `c1-anticipations-sce.md` section 6.3 mot a mot. | La fonction de C1 opere sur des variables continues de menages winsorisees ; elle n'a pas de sens sur des modalites categorielles. Ce qui est transporte est la **definition** du temoin, pas son code. Le preenregistrement prevoyait ce cas et demandait de le declarer. |

---

## 9. Ce que cela change a MOONSHOTS programme C

`MOONSHOTS.md` section 3 conclut sur le programme C, le banc des basculements : « C est
solide, necessaire, et pas assez gros en 2026 : son premier resultat existe et il dit que le
sol manque ; sa forme honnete est un plafond, et un plafond ne se vend pas a un ministre ». Le
« sol manque » venait de I1, qui avait montre que la quantite individuelle a predire est
presque entierement dans la reponse precedente. **T2 change trois choses a ce diagnostic, deux
dans un sens et une dans l'autre.**

**Un. L'etage agrege a un sol, et il est chiffre.** Contrairement a l'etage individuel, le
niveau du groupe porte un signal reproductible et previsible : correlation inter moities 0,596
sur qui change, 0,603 pour les camps ; variance inter groupes expliquee 0,447 pour un plafond
de 0,638. **La phrase « il n'y a rien a predire » est fausse au niveau agrege.** Un institut
qui vend « quelle part de tel groupe va changer d'avis sur tel item » vend quelque chose de
mesurable, et T2 donne la barre.

**Deux. La barre pour un jumeau, a declarer avant le run du jour 5, dans sa version
agregee.**

> Une population simulee construite sur la vague 1 du panel 2016-2020 doit, sur les 118 items
> du noyau commun et les 53 groupes de `t2-groupes.csv`, produire un taux de changement par
> cellule (groupe, item) dont **l'erreur absolue moyenne est inferieure a 2,78 points** et
> dont la **part de variance inter groupes expliquee depasse 0,447**, mesurees dans le meme
> dispositif en demi echantillons. En dessous de **3,10 points** et de **0,311**, elle ne fait
> pas mieux qu'un modele qui ignore les etiquettes de groupe et ne connait que la composition
> en vague 1. En dessous de **3,74 points** et de **0,000**, elle ne fait pas mieux qu'un nul
> qui ne connait que la derive de l'item. Et elle ne doit **jamais** etre notee sur le sens du
> deplacement d'un groupe, sur lequel le nul a derive est imbattable, sauf sur l'axe d'age.

**Trois. La promesse « qui bascule » reste interdite, et T2 la restreint encore.** Le
programme C promettait de dire qui bascule ; I1 avait retire l'individu, T2 retire la
direction au niveau du groupe. Ce qui reste vendable est exactement : **la part de tel groupe
qui va changer d'avis sur tel item**, sans savoir qui, et sans savoir dans quel sens au dela
de la derive de tout le monde. C'est une promesse plus petite que celle du programme C
d'origine, et elle a le merite d'etre soutenue par une mesure.

**Quatre, pour le point d'arret du mois 1.** `MOONSHOTS` ecrit : « si le run C3 ne bat pas la
modalite de vague 1 sur qui bouge, la branche jumeaux ferme ». T2 precise ce que « la modalite
de vague 1 » devient a l'agrege : c'est **M3**, la matrice de transition par modalite agregee
a la cellule, erreur 3,10 points et variance expliquee 0,311. C'est un adversaire plus dur que
le nul a derive et il coute zero appel.

**Cinq, une entree de plus a la liste des quantites de gabarit de `MODELE-DU-MONDE`.** Le
**rapport reel sur nul de l'amplitude** rejoint la liste, avec deux precisions que C1 seul ne
pouvait pas donner : il vaut 0,43 a 0,55 sur les anticipations de menages et 0,60 a 0,66 sur
les attitudes du GSS, donc ce n'est pas une constante ; et il se calcule **en forme close**
sur des items categoriels, `1 - somme p1(m) p2(m)`, sans aucun tirage.

---

## 10. Ce que je n'ai pas pu verifier

1. **Que le signal de groupe sur qui change soit un signal d'opinion.** Les items ou le
   predicteur de groupe gagne le plus sont `income`, `wrkstat` et `news`, qui ne sont pas des
   opinions mais des faits biographiques ou des comportements. La reserve de I1 section 4.4
   vaut ici sans attenuation, et T2 n'a **pas** refait la mesure sur le sous ensemble des
   seuls items d'attitude. C'est le premier calcul a faire et il ne coute rien.
2. **Que le plafond de bruit de la section 3.1 soit exact.** Il repose sur l'hypothese que la
   vraie valeur d'une cellule est la meme dans les deux moities et que le bruit y a la meme
   variance. Les deux moities ont le meme effectif, ce qui rend la seconde hypothese
   raisonnable, mais l'estimateur n'est pas borne et ses deux versions, le plafond et la
   correlation inter moities, s'accordent sur le taux de changement (0,638 et 0,596) et
   divergent sur le deplacement projete (0,308 et 0,133). **Sur le sens, le plafond est
   probablement surestime**, et c'est la correlation, qui a un test de permutation, qui porte
   le verdict. [PROBABLE]
3. **Que l'ecart droite moins gauche sur le sens du deplacement soit vraiment nul.** Le test
   preenregistre ne retient pas le camp sur `pi`, `p` de Holm 0,192. Mais un contraste
   **non preenregistre**, l'ecart droite moins gauche item par item sur la premiere coupure
   seulement, se reproduit a `r = 0,321` entre les deux moities. Ce contraste ne pointe que
   deux camps la ou le test preenregistre en compare trois a la moyenne d'item, dont un centre
   tres bruite. **Il est possible que le test declare manque de puissance sur la bonne
   quantite.** Ce n'est pas verifie et ce n'est pas publie comme un resultat. [PROBABLE]
4. **Que la sur representation du centre parmi les changeurs ne soit pas une
   sur representation des repondants imprecis.** Le centre partisan, « independent
   (neither) », est le groupe le plus petit, 767 personnes, et celui dont on attend le plus de
   reponses peu fiables. a42 mesure 54,8 pour cent de fidelite sur les modalites rares. La
   correction n'a pas ete faite.
5. **Que le codage ordinal soit fidele a l'echelle du questionnaire.** Les 63 items ordinaux
   emploient le **code numerique brut du GSS**, jamais un recodage de notre invention, et il
   est publie item par item dans `t2-ordinaux.csv`. Rien ne garantit que pour chacun d'eux le
   code numerique soit monotone dans l'echelle. Une inversion locale gonflerait la distance
   des deux cotes, reel et nul, donc le rapport de la section 4 est robuste ; la cible `mu` de
   la section 3, elle, ne l'est pas.
6. **La ponderation de panel.** Comme dans I1, les quatre panels sont mis en commun sans
   redressement ; `wtpannr123` et `wtssall` existent et ne sont pas utilises. Les quantites
   publiees sont des quantites d'echantillon, pas des quantites de population americaine.
   **C'est une reserve serieuse pour un volet dont l'objet est precisement le groupe.**
7. **La stabilite sous un autre decoupage de groupe.** Les blocs d'age, d'education et
   d'ideologie sont ceux de a1 et de a44, repris sans discussion. Le bloc `education = bas`
   reunit 2 838 personnes sur 4 683 parce que la regle de `i1_commun.bloc_education` range le
   diplome de fin d'etudes secondaires avec les non diplomes. Un decoupage plus fin donnerait
   d'autres cellules et n'a pas ete essaye.
8. **Le perimetre a deux ans pour le volet 1**, ecart E6, et la variante « non reponse comptee
   comme modalite » de `a12_sensibilite_dk.py`, qui n'a ete refaite ni par I1 ni ici.
9. **L'anteriorite.** La decomposition d'un changement de panel entre une part attribuable aux
   marginales et une part attribuable a l'appariement est classique en analyse de tables de
   mobilite, et je n'ai pas fait de recherche d'anteriorite sur la forme close de la
   section 1 ni sur le rapport reel sur nul.

---

## 11. Questions ouvertes pour Simon

1. **Refait on le volet 1 sur les seuls items d'attitude ?** C'est la question numero 1 de I1,
   restee sans reponse, et T2 la rend plus urgente : la ou le predicteur de groupe gagne le
   plus, il gagne sur `income` et `wrkstat`. Le calcul coute vingt minutes et zero appel. **Ma
   preference est de le declarer avant, de le publier comme perimetre primaire, et de garder
   les 118 items a cote.** Si le signal de groupe tient sur les seuls items d'attitude, la
   barre du jour 5 est defendable devant un institut ; s'il s'effondre, c'est un resultat
   negatif propre et il faut l'ecrire.

2. **Le rapport reel sur nul entre il au dossier comme quantite de verdict, sachant qu'il
   n'est pas une constante ?** Il vaut 0,43 a 0,55 sur le SCE et 0,60 a 0,66 sur le GSS, et de
   0,39 a 0,74 selon la famille d'items. C1 proposait d'en faire une quantite de verdict ; T2
   montre qu'elle depend du sujet autant que de la population. **Deux options** : le publier
   comme un profil par famille, ce qui est plus riche et moins vendable, ou fixer un
   perimetre de reference une fois pour toutes. Je n'ai pas tranche.

3. **Que fait on de l'axe d'age, seul endroit ou le sens du deplacement porte un signal de
   groupe ?** Correlation inter moities 0,383 sur `pi` et 0,548 sur `mu`, `p` de Holm nul dans
   les deux cas. C'est le seul point du dossier ou une population synthetique pourrait etre
   notee sur une direction. **Cela vaut il un volet a part, « les cohortes se deplacent
   differemment et cela se mesure », ou est ce trop banal pour etre publie ?**

4. **Le contraste droite moins gauche sur le sens merite il un test dedie ?** Le test
   preenregistre ne retient pas le camp sur la direction ; un contraste a deux camps, non
   preenregistre et calcule sur une seule coupure, se reproduit a 0,321. **Si Simon veut le
   savoir, il faut le preenregistrer separement et le refaire sur les cinq coupures.** Je
   refuse de le publier comme un resultat en l'etat.

5. **Le plafond de bruit doit il devenir une convention du dossier ?** T2 en a eu besoin parce
   que l'oracle empirique n'etait pas un plafond, et il change la lecture : dire « M4 explique
   0,447 de la variance inter groupes » est tiede, dire « M4 capte 70 pour cent de ce qui est
   atteignable » est un enonce. La meme quantite manque a a43, a a44 et a I1, ou toutes les
   parts de variance sont publiees contre une variance totale qui contient du bruit
   d'echantillonnage non mesure. **Faut il la retro appliquer, ou la reserver aux mesures a
   venir ?**

6. **La ponderation de panel.** Un volet dont l'objet est le groupe et qui ne redresse pas est
   attaquable par n'importe quel statisticien d'institut. Les poids existent dans les fichiers.
   **Est ce le moment de payer cette dette, sachant qu'elle s'applique aussi retroactivement a
   I1 et a a12 ?**

7. **La forme close du nul a derive change t elle la facon dont le dossier ecrit ses
   temoins ?** Sur des items categoriels, `1 - somme p1(m) p2(m)` donne le taux de changement
   du nul a neuf millioniemes pres, sans un seul tirage. Plusieurs temoins du dossier, dans
   a44 comme ici, sont calcules par permutation la ou une esperance existe. **Cela ne change
   aucun resultat, mais cela change ce qu'on peut demander a un relecteur de verifier au
   crayon**, et c'est peut etre l'argument le plus simple a mettre devant un ministre : la
   population sans personnes n'est pas une simulation, c'est une soustraction.
