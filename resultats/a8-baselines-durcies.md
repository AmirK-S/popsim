# a8 : les baselines de a2, durcies

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 7 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Recalcul :
`analyses/a19_a8_correlation.py`, tableau `resultats/a19-a8-correlation-blocs.csv`, lecture
seule de `a8-twin-par-item.csv`. Aucun script existant n'a ete modifie, aucun appel de modele.

### E1. Sections 1 et 3.2 : le regime "famille retiree" n'est applique qu'a B2. La comparaison n'est pas appariee et la conclusion ne tient pas en l'etat. Objection a17 4.1.

**Phrase d'origine, section 1.** "Quand on retire la famille entiere, les agents de Stanford
battent B2. Le test existentiel A4 se retourne du bon cote pour le projet."

**Phrase d'origine, section 3.2.** "Reponse directe a la question posee : oui, quand on retire
toute la famille, les agents de Stanford battent B2 [MESURE]. Sur les 58 items reunis, l'agent
composite passe de 1,8 point derriere B2 a 1,5 point devant, et l'agent enquete de 2,5 points
derriere a 0,9 point devant."

**Le protocole de B2 est correct, ce n'est pas lui qui est en cause.** La ligne
`contexte = np.setdiff1d(np.arange(m), cols)` de `a8_familles.py` retire bien toute la famille
du contexte de B2, pour tous les items de la famille. Le decoupage fait ce que la section 3.1
annonce. [VERIFIE par lecture du code]

**Correction : les conditions d'agents ne sont pas replacees dans le meme regime.** Les agents
enquete et composite de l'archive ont recu, dans leur invite, l'ensemble des reponses de la
personne au GSS **moins le seul item predit**. a14 section 3.1 cite la regle des auteurs :
"we ensure that the question we are predicting on is not in the input for the agents"
[CONFIRME, materiel supplementaire p. PDF 38]. Quand on predit `abany`, l'agent composite
dispose donc encore de `abdefect`, `abnomore`, `abhlth`, `abpoor`, `abrape` et `absingle`.
B2 famille retiree, elle, en est privee. **Le tableau de la section 3.2 compare une baseline
amputee de ses six cousins a un agent qui les a gardes.** La comparaison n'est pas appariee et
elle est defavorable a B2.

**La condition appariee existe, elle est publiee par le papier, et elle suffit a renverser le
sens du resultat.** Le materiel supplementaire evalue les Survey Agents sous les deux
strategies de retrait, sur un sous echantillon de 100 agents [CONFIRME, a14 section 3.4,
Tableau 6 p. PDF 76 a 77] :

| strategie de retrait pour les Survey Agents | score normalise |
|---|---|
| retrait du seul item predit, c'est le regime de nos tableaux | **0,82** |
| retrait du bloc entier du GSS auquel appartient l'item, c'est le regime de B2 | **0,77** |

Cinq points de score normalise, soit environ **4,0 points d'exactitude brute** au denominateur
de 79,53 pour cent. Appliques aux 0,6711 de l'agent enquete sur les 58 items, ils donnent
environ **0,631, sous les 0,6621 de B2 famille retiree**. L'agent composite, a 0,6775, passerait
lui aussi sous B2 ou a sa hauteur. [PROBABLE, voir la reserve ci dessous.]

**Reserve, et elle est reelle.** Le 0,77 contre 0,82 est mesure sur 100 agents et sur
l'ensemble des items du GSS ; le transposer aux 58 items de familles thematiques, ou
l'autocorrelation intra famille est par construction plus forte que la moyenne, n'est pas une
mesure. L'ordre de grandeur est defendable, la valeur exacte non. Un fichier de la condition
"retrait par bloc" n'a pas ete cherche dans le paquet OSF ; si un tel fichier existe, il
tranche en une heure.

**Ce qu'il faut ecrire a la place, et ou est le test propre.** "Le regime famille retiree n'est
applique qu'a B2 ; les agents de Stanford conservent les items cousins dans leur invite, et la
comparaison leur est favorable d'environ quatre points d'exactitude brute selon la condition
appariee que le papier publie lui meme. En l'etat, la phrase les agents de Stanford battent B2
n'est pas etablie. **Le test propre est la condition C3F de a5**, ou nos propres agents perdent
la famille thematique entiere de leur contexte : elle se compare a la ligne B2 famille retiree
de `resultats/a8-familles-gss.csv`, et a rien d'autre. a5 section 4.5 la declare ecrite,
testee a la resolution du protocole, et non lancee."

**Consequence sur la section 7.3 et sur l'entree du JOURNAL de 22:50.** Le test existentiel A4
n'est pas retourne. Il reste ouvert, et son cout est desormais chiffre : une nuit de calcul
pour C3F.

### E2. Section 5.3 : la correlation de 0,80 est portee par un seul bloc, et son p traite 108 items dependants comme independants. Objection a17 4.3.

**Phrase d'origine, sections 1 et 5.3.** "La correlation de rang entre l'avantage du modele par
item et la stabilite test retest de l'item vaut **0,80** [MESURE, p < 0,0001, 108 items]."

**Correction, recalcul sur `a8-twin-par-item.csv`.** [MESURE,
`analyses/a19_a8_correlation.py`, `resultats/a19-a8-correlation-blocs.csv`]

| perimetre | n | Spearman avantage contre retest, GPT-4.1-mini persona texte | p |
|---|---|---|---|
| 108 items, comme publie | 108 | **+0,797** | 5,4 x 10^-25 |
| **hors les 40 items du bloc `Product Preferences - Pricing`** | 68 | **+0,561** | 6,7 x 10^-7 |
| moyennes par bloc, unite d'observation le bloc | 33 | **+0,479** | 4,8 x 10^-3 |
| moyennes par bloc, blocs a plus d'un item seulement | 7 | +0,857 | 1,4 x 10^-2 |

Le meme profil se retrouve sur les autres configurations : 0,786 puis 0,516 pour GPT-4.1
persona JSON, 0,795 puis 0,530 pour Gemini.

**Trois choses a dire, et la troisieme est la plus genante.** D'abord, 40 des 108 items
appartiennent a un seul bloc, celui des preferences de prix, et c'est lui qui porte tout
l'avantage du modele : avantage moyen **+0,103 dans ce bloc, -0,056 hors de ce bloc**. La
correlation de 0,80 est en grande partie la separation entre ce bloc et le reste. Ensuite, le
p inferieur a 0,0001 traite 108 items d'une meme batterie comme 108 observations
independantes ; le nombre de blocs est de **33, dont 26 a un seul item**. Enfin, la meme table
contient une colonne `spearman_avantage_exactitude_B0` a **0,428**, non mentionnee par le
rapport : l'avantage du modele suit aussi la facilite de l'item. Ce controle la, la correlation
le passe, la correlation partielle a B0 mode fixe valant 0,757 ; le controle par bloc, non.

**Phrase de remplacement.** "La correlation de rang entre l'avantage du modele par item et la
stabilite test retest de l'item vaut 0,80 sur les 108 items, 0,56 une fois retires les 40 items
du bloc de preferences de prix, et 0,48 lorsque l'unite d'observation est le bloc et non l'item
[MESURE, 33 blocs, p = 0,005]. Le lien survit aux trois perimetres, mais son ampleur est
divisee par 1,7 des qu'on tient compte de la dependance entre items d'une meme batterie."

**Ce que cela ne change pas.** Le sens du resultat tient : le predicteur de l'avantage du
modele reste la stabilite de la personne avec elle meme, et il reste plus fort que le lien avec
le R2 des demographies, 0,39. L'hypothese de remplacement de la section 5.3 n'est pas
invalidee, elle est seulement moins fortement soutenue qu'annonce.

### E3. Section 7.1 : la phrase de a2 declaree "non contredite" est contredite par a2 lui meme. Objection a17 2.1, contradiction C5.

**Phrase d'origine.** "La conclusion generale de a2 sur le GSS, cinq des six conditions d'agents
de Stanford sont battues par du scikit-learn sur les 149 items, n'est pas contredite : rien
dans ce rapport ne recalcule ce chiffre la sur les 149 items."

**Correction.** C'est exact au sens ou a8 ne recalcule pas ce chiffre. Mais la phrase de a2 est
contredite par la limite 2 de a2 lui meme, qui declare que "la comparaison B2 contre agents
demographiques n'a pas de sens". Trois des cinq conditions comptees comme battues, `v6`, `v7`
et `v8`, sont exactement celles la. Declarer la phrase "non contredite" la valide une seconde
fois. Voir l'errata E3 de `a2-baselines.md`, rendu le meme jour.

**Phrase de remplacement.** "La conclusion de a2 sur le GSS n'est pas recalculee ici. Elle doit
etre reduite, pour la raison que a2 donne lui meme en limite 2, aux deux conditions comparables
a B2, entretien et enquete."

### E4. Perimetre des 149 items : `income` y figure et `gss_v6` le recopie a 99,4 pour cent. Objection a17 2.2 et 6.3, contradiction C6.

Les 149 items employes par `a8_commun.py` sont ceux de `a2_baselines_gss.py`, donc ils
contiennent `income`. La condition `gss_v6` recopie cet item a **99,4 pour cent**, contre
63,4 pour cent pour le retest humain et 51,6 pour cent pour la modalite majoritaire ; son score
sur les 149 items est gonfle de **0,28 point**. [MESURE, errata E2 de `a2-baselines.md`,
`resultats/a19-income-baselines.csv`]

Effet sur ce rapport : les lignes `v6` des tableaux des sections 3.2 et 4.2 sont surestimees
d'environ 0,3 point. Aucune conclusion de a8 ne repose sur `v6`, qui est battue par toutes les
baselines dans tous les regimes, donc aucun chiffre publie ici ne change de sens. La note doit
neanmoins figurer, parce que le meme perimetre sert a a7 et a a12.

### E5. Ce que ces errata ne changent pas

Le k de B2 par validation interne, la copule gaussienne et son avantage sur les 70 items
ordinaux, la decomposition bloc par bloc de Twin, le rappel des minorites et les treize
configurations ne sont pas touches. Le point favorable non revendique de la section 4.4 reste
vrai : la copule gagne avec 56 items de contexte contre 119 pour B2.

---

Rapport du 7 septembre 2026. Il ferme cinq limites declarees du rapport `a2-baselines.md`
avant qu'un relecteur ne les ouvre, et il mesure ou le modele de langage gagne vraiment.
Aucun appel de modele de langage n'a ete fait pour produire ces chiffres : les simulations
utilisees sont celles publiees par les auteurs de Twin-2K-500 et par l'archive OSF.

Protocole repris a l'identique de a2, sans modification d'aucun script existant : graine
20260903, cinq plis sur les personnes, cinq blocs d'items sur le GSS, decoupage temporel
fourni sur Twin-2K-500, memes metriques importees de `analyses/a2_commun.py`.

Scripts : `analyses/a8_commun.py`, `a8_telecharger_twin_llm.py`, `a8_k_validation.py`,
`a8_familles.py`, `a8_copule.py`, `a8_twin_items.py`, `a8_minorites.py`, `a8_figures.py`.
Tableaux : `resultats/a8-*.csv`. Figure : `resultats/a8-figure-familles.png` et `.svg`.

Rejouable en six commandes, environ douze minutes en tout, quatre coeurs.

```
.venv/bin/python analyses/a8_telecharger_twin_llm.py
.venv/bin/python analyses/a8_k_validation.py
.venv/bin/python analyses/a8_familles.py
.venv/bin/python analyses/a8_copule.py
.venv/bin/python analyses/a8_twin_items.py
.venv/bin/python analyses/a8_minorites.py && .venv/bin/python analyses/a8_figures.py
```

---

## 1. Ce qu'il faut retenir

**Quand on retire la famille entiere, les agents de Stanford battent B2. Le test existentiel
A4 se retourne du bon cote pour le projet.** [MESURE] Sur les 58 items du GSS qui
appartiennent a une famille thematique fermee, B2 passe de 0,6956 avec le decoupage
aleatoire de a2 a 0,6621 quand la famille est retiree du contexte et predite. Les agents
composite (0,6775) et les agents enquete (0,6711) passent devant. Famille par famille,
l'agent composite bat B2 dans cinq familles sur six et l'agent enquete dans quatre sur six.
Le seul terrain ou B2 tient encore est celui des depenses publiques `nat*`, 17 items, ou
elle fait 0,6170 contre 0,5911 pour le meilleur agent.

**La cause de la victoire du modele sur Twin-2K-500 n'est pas celle qu'annonce a2, et
l'hypothese de la section 5 est fausse.** [MESURE] a2 supposait que le modele gagnait sur
les experiences d'heuristiques et de biais, ou la reponse depend de la structure du probleme
plus que de la personne. Mesure bloc par bloc, c'est l'inverse : sur les blocs
d'heuristiques et de biais, le modele perd contre la modalite majoritaire, jusqu'a 14 points
sur Linda-conjunction. Tout son avantage vient d'un seul bloc, les preferences de prix sur
40 produits, ou GPT-4.1 persona JSON fait 0,7166 contre 0,5623 pour B2. Ce bloc est aussi
celui ou la personne est la plus stable avec elle meme, 0,8389 de fidelite test retest. La
correlation de rang entre l'avantage du modele par item et la stabilite test retest de
l'item vaut **0,80** [MESURE, p < 0,0001, 108 items]. Le modele gagne la ou il y a une
personne a retrouver, pas la ou il n'y en a pas.

**Le classement modele contre baseline ne tient pas pour toutes les configurations.**
[MESURE] Sur les treize configurations publiees par les auteurs, huit battent B2 et cinq
perdent. La meilleure est GPT-4.1 persona JSON a 0,5738. La pire est le modele affine sur
500 exemples, 0,4619, en dessous de la modalite majoritaire et de nos six baselines a
l'exception de B0 tirage.

**Une copule gaussienne bat tout le monde sur les items ordinaux du GSS.** [MESURE] Sur les
70 items ordinaux, elle atteint 0,5840 contre 0,5655 pour B2, 0,5142 pour B1, et **0,5596
pour l'agent composite**, qui etait la seule condition de Stanford que a2 laissait invaincue.
Sur ce sous ensemble, aucune des six conditions d'agents ne resiste.

**Sur les minorites d'opinion, l'ecart se renverse completement, et c'est le resultat le plus
vendable du lot.** [MESURE] Sur le GSS, quand la vraie reponse est une modalite choisie par
moins de 10 pour cent des repondants, B2, championne de a2 a 0,6717 en moyenne, n'en
retrouve que **3,6 pour cent**, et ne produit que 7 pour cent de la masse minoritaire
humaine. L'agent composite en retrouve **30,7 pour cent** et reproduit 95 pour cent de la
masse. B0 mode en retrouve zero, par construction. Un institut qui achete des queues de
distribution n'achete aucune de nos baselines.

**Le k de B2 choisi sur le pli de test coutait moins que ce que a2 craignait sur le GSS, et
coutait dans l'autre sens sur Twin.** [MESURE] Choisi par validation interne au pli
d'entrainement, k vaut 25 sur le GSS aux cinq plis et l'exactitude passe de 0,6717 a 0,6711,
soit 0,06 point d'optimisme au lieu des 0,2 annonces. Sur Twin, la validation interne choisit
k = 100 aux cinq plis et l'exactitude **monte** de 0,5301 a 0,5345 : a2 sous estimait sa
propre baseline de 0,44 point.

---

## 2. Le k de B2 par validation interne, limite 1 de a2

Protocole : a l'interieur de chaque pli d'entrainement, validation croisee a trois plis
internes, balayage de k sur `[1, 3, 5, 10, 15, 20, 25, 30, 40, 60, 100, 150]`, choix du k
qui maximise l'exactitude interne, puis application au pli de test sans retouche. Le pli de
test n'est jamais regarde. Le score final est recalcule avec `b2_voisins` de a2, sans
modification.

| jeu | k retenu, cinq plis | exactitude | IC 95 % | a2, k = 30 | ecart |
|---|---|---|---|---|---|
| GSS | 25, 25, 25, 25, 25 | 0,6711 | [0,6673 ; 0,6750] | 0,6717 | -0,06 point |
| Twin-2K-500 | 100, 100, 100, 100, 100 | 0,5345 | [0,5306 ; 0,5386] | 0,5301 | +0,44 point |

Detail par pli dans `resultats/a8-k-validation-plis.csv`, resume dans
`resultats/a8-k-validation.csv`.

Lecture. Le k choisi est stable d'un pli a l'autre sur les deux jeux [MESURE], ce qui est
attendu vu la platitude de la courbe decrite en a2. Sur le GSS l'optimisme existe mais il est
de six centiemes de point : il ne change aucune conclusion et il faut le dire pour couper
court. Sur Twin la situation est inverse et plus interessante : le voisinage optimal est trois
fois plus large, ce qui est la signature d'un signal individuel faible et bruite, et a2 se
penalisait elle meme. Avec k = 100, l'ecart entre GPT-4.1-mini persona complet (0,5530) et
B2 tombe de 2,3 a **1,85 point** [MESURE]. Le sens de la conclusion de a2 ne change pas, son
amplitude oui.

---

## 3. Le decoupage par famille, limite 7 de a2, et le test existentiel A4

### 3.1 Ce qui est mesure

Pour chaque famille du GSS, la famille entiere sort du contexte **et** sert de cible. B2 ne
dispose plus des cousins de l'item, seulement des 149 moins n items du reste du questionnaire.
C'est le regime "la question n'a jamais ete posee a personne dans ce domaine" du point de vue
statistique. B0, B1 et les agents de Stanford sont recalcules sur exactement les memes items,
sans quoi l'ecart viendrait du denominateur.

Figure : `resultats/a8-figure-familles.png`, panneau du haut. Tableau complet, avec
intervalles de confiance, diversite conservee et accord par paires :
`resultats/a8-familles-gss.csv`.

### 3.2 Le tableau qui repond a la question

| famille | items | B0 mode | B1 argmax | B2 aleatoire (a2) | **B2 famille retiree** | composite | enquete | entretien v3 | v6 | v7 | v8 | humains |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| depenses publiques `nat*` | 17 | 0,5733 | 0,5900 | 0,6372 | **0,6170** | 0,5911 | 0,5828 | 0,5639 | 0,4880 | 0,4855 | 0,4700 | 0,7468 |
| confiance `con*` | 13 | 0,5027 | 0,5471 | 0,5951 | **0,5690** | 0,5901 | 0,5836 | 0,5622 | 0,4998 | 0,4952 | 0,5074 | 0,7209 |
| avortement `ab*` | 7 | 0,7436 | 0,8053 | 0,8779 | **0,8278** | 0,8914 | 0,8810 | 0,8373 | 0,7572 | 0,7541 | 0,7879 | 0,9172 |
| libertes civiles | 11 | 0,7497 | 0,7406 | 0,7883 | **0,7566** | 0,7855 | 0,7973 | 0,7139 | 0,7023 | 0,7152 | 0,6597 | 0,8380 |
| fin de vie | 5 | 0,7283 | 0,7266 | 0,8376 | **0,7582** | 0,8044 | 0,8207 | 0,7367 | 0,7011 | 0,7230 | 0,6903 | 0,8833 |
| roles de genre `fe*` | 5 | 0,4751 | 0,4783 | 0,5540 | **0,5217** | 0,5348 | 0,4778 | 0,4911 | 0,4544 | 0,4629 | 0,4549 | 0,6886 |
| **toutes familles reunies** | **58** | **0,6164** | **0,6371** | **0,6956** | **0,6621** | **0,6775** | **0,6711** | **0,6336** | **0,5792** | **0,5822** | **0,5704** | **0,7856** |

Reponse directe a la question posee : **oui, quand on retire toute la famille, les agents de
Stanford battent B2** [MESURE]. Sur les 58 items reunis, l'agent composite passe de 1,8 point
derriere B2 a 1,5 point devant, et l'agent enquete de 2,5 points derriere a 0,9 point devant.
L'agent entretien reste derriere, de 2,9 points.

Compte des victoires, famille par famille [MESURE] : l'agent composite bat B2 famille retiree
dans **cinq familles sur six**, l'agent enquete dans **quatre sur six**, l'agent entretien
dans **une sur six**. Les trois conditions faibles, v6, v7 et v8, ne battent B2 dans aucune
famille.

### 3.3 Ce que le retrait coute, et ou

| famille | B2 aleatoire | B2 famille retiree | cout du retrait |
|---|---|---|---|
| fin de vie | 0,8376 | 0,7582 | -7,9 points |
| avortement `ab*` | 0,8779 | 0,8278 | -5,0 points |
| roles de genre `fe*` | 0,5540 | 0,5217 | -3,2 points |
| libertes civiles | 0,7883 | 0,7566 | -3,2 points |
| confiance `con*` | 0,5951 | 0,5690 | -2,6 points |
| depenses publiques `nat*` | 0,6372 | 0,6170 | -2,0 points |
| toutes familles reunies | 0,6956 | 0,6621 | **-3,4 points** |

Le cout est le plus eleve la ou la famille est petite et fortement auto correlee, fin de vie
et avortement [MESURE]. C'est coherent : cinq items de fin de vie tres correles entre eux
donnent au decoupage aleatoire quatre cousins gratuits pour predire le cinquieme. La limite 7
de a2 etait donc bien reelle et son ordre de grandeur, "un B2 plus bas", est confirme et
chiffre a 3,4 points sur ces items.

**Le point qui compte pour la these du projet.** [MESURE] A 0,6621, B2 famille retiree
conserve 58,0 pour cent de la diversite humaine et affiche un accord par paires de 72,1 pour
cent, contre 49,1 pour cent chez les humains. L'agent composite, a 0,6775 sur les memes
items, conserve **94,8 pour cent** de la diversite. Sur ce regime, les agents de langage
dominent donc les deux axes a la fois, exactitude et dispersion. C'est la premiere fois dans
ce projet qu'une condition d'agent domine une baseline sur les deux dimensions simultanement.

### 3.4 Twin-2K-500 : le regime severe etait deja en place, sans que a2 le dise

Fait verifie et non anticipe [MESURE] : le contexte des vagues 1 a 3 utilise par a2 ne
contient **aucun** item appartenant a un bloc de la vague 4. Les quatre blocs de contexte sont
Personality (255 colonnes), Economic preferences (176), Cognitive tests (49) et Demographics
(14) ; l'intersection avec les blocs cibles est vide. La raison est mecanique : a2 retire du
contexte toutes les colonnes reposees en vague 4, et ces blocs sont reposes en entier. Il n'y
a donc pas de famille a retirer sur Twin, elle est deja absente. Les chiffres Twin de a2 sont
**deja** des chiffres de regime "famille retiree", ce que a2 ne dit pas.

Faute de famille a retirer, on retire les blocs de contexte un a un.
`resultats/a8-familles-contexte-twin.csv` :

| contexte donne a B2 | colonnes | exactitude, 108 items |
|---|---|---|
| complet, comme a2 | 494 | 0,5301 |
| sans Economic preferences | 318 | 0,5314 |
| sans Cognitive tests | 445 | 0,5291 |
| sans Personality | 239 | 0,5169 |
| demographies seules | 14 | 0,5192 |

Lecture [MESURE] : tout ce que B2 gagne au dessus des demographies seules sur Twin vient du
bloc Personality, et rien du tout des 176 items de preferences economiques ni des 49 tests
cognitifs. Retirer les preferences economiques **ameliore** B2 de 0,13 point, ce qui est du
bruit mais certainement pas un apport. C'est une information utile pour le projet : sur ce
jeu, 225 des 494 colonnes de contexte ne servent a rien.

---

## 4. La copule gaussienne, limite 8 de a2

### 4.1 Ce qui est construit

Chaque item ordinal est traite comme la discretisation d'une variable latente normale. Les
seuils viennent de la marginale estimee sur le pli d'entrainement, la matrice de correlation
latente est estimee sur les scores normaux du meme pli, le retrecissement `(1 - lam) R + lam I`
est choisi par validation interne au pli d'entrainement, et la prediction est la loi
conditionnelle du latent cible sachant les latents des items de contexte, avec le meme
decoupage en cinq blocs que B2.

Perimetre [MESURE] : les items nominaux n'ont pas d'ordre, donc pas de seuil. Le repere est
`figure2/data/question_master/gss/groups/categorical.csv`, colonne `Categorical` : `N`
designe un item ordinal, `Y` un item nominal. Sur les 149 items cibles, **70 sont ordinaux**
et les 79 autres sont nominaux. La copule porte donc sur 70 items et non sur les 75 attendus,
et toutes les methodes comparees ci dessous sont recalculees sur ces 70 items. Le
retrecissement retenu est 0,20 aux cinq plis.

### 4.2 Resultats, 70 items ordinaux du GSS

| methode | exactitude | IC 95 % | diversite conservee | accord paires |
|---|---|---|---|---|
| humains reinterroges | 0,7144 | [0,7081 ; 0,7212] | 100,1 % | 38,5 % |
| **copule gaussienne (argmax)** | **0,5840** | [0,5791 ; 0,5885] | 57,3 % | 62,6 % |
| B2 argmax | 0,5655 | [0,5605 ; 0,5705] | 61,2 % | 60,5 % |
| agents composite | 0,5596 | [0,5544 ; 0,5652] | 89,4 % | 44,0 % |
| agents entretien (v3) | 0,5273 | [0,5223 ; 0,5323] | 89,7 % | 44,5 % |
| agents enquete | 0,5206 | [0,5155 ; 0,5259] | 86,0 % | 46,1 % |
| B1 argmax | 0,5142 | [0,5091 ; 0,5192] | 76,4 % | 52,4 % |
| B0 mode | 0,4908 | [0,4854 ; 0,4960] | 4,4 % | 96,8 % |
| B2 tirage | 0,4586 | [0,4542 ; 0,4630] | 96,3 % | 40,5 % |
| agents demographiques (v6) | 0,4511 | [0,4459 ; 0,4563] | 62,4 % | 61,0 % |
| copule gaussienne (tirage) | 0,4533 | [0,4490 ; 0,4574] | 99,4 % | 38,8 % |
| agents v7 | 0,4397 | | 64,3 % | 60,4 % |
| agents v8 | 0,4377 | | 83,5 % | 47,7 % |
| B1 tirage | 0,4318 | | 99,9 % | 38,6 % |
| B0 tirage | 0,3846 | | 99,9 % | 38,5 % |

Trois lectures desagreables.

1. **La copule est la meilleure methode non humaine du tableau** [MESURE], 1,85 point devant
   B2 et 2,44 points devant l'agent composite. La phrase de a2 "seul l'agent composite tient
   encore" tombe sur les items ordinaux : sur ce sous ensemble, **les six conditions d'agents
   sont battues**, et deux fois plutot qu'une.
2. **La copule en mode tirage conserve 99,4 pour cent de la diversite humaine et un accord par
   paires de 38,8 pour cent contre 38,5 pour cent chez les humains** [MESURE]. C'est le seul
   simulateur de ce projet, LLM compris, dont l'accord par paires colle a celui des humains a
   0,3 point pres. Il paye ce realisme d'une exactitude individuelle de 0,4533, mais pour un
   usage de restitution de distribution, c'est la reference a battre.
3. L'ecart entre les deux modes de la copule, 13,1 points d'exactitude contre 42,1 points de
   diversite, est le meme compromis que celui decrit en section 8 de a2. La copule ne le
   resout pas, elle le deplace.

Note de methode assumee : la correlation latente est estimee par la correlation de Pearson des
scores normaux, qui approche la correlation polychorique sans l'estimer par maximum de
vraisemblance [CONFIRME, choix documente dans le script]. Cette approximation sous estime
legerement les correlations fortes, donc le chiffre de 0,5840 est un plancher pour cette
famille de methodes, pas un plafond.

---

## 5. Twin-2K-500 item par item, section 5 et limite 5 de a2

### 5.1 Toutes les configurations publiees, pas deux

Les treize configurations du dossier `LLM_simulation_results/llm_simulations_all_specifications`
sont evaluees sur exactement les memes 108 items, dans le meme codage, contre les memes
baselines. Alignement verifie avant toute comparaison [MESURE] : le fichier humain formate,
trie par `TWIN_ID` croissant, a la meme liste de `pid` dans le meme ordre que le catalogue, et
les valeurs coincident sur les 108 items, accord 1,0000, memes cellules manquantes.

Trois configurations sur treize ne couvrent pas les 2 058 personnes et leur couverture est
rapportee avec leur score : le modele affine exclut ses 500 exemples d'entrainement (1 558
personnes), une variante JSON s'arrete a 1 000 personnes, une autre en perd huit.

| configuration | exactitude, 108 items | diversite conservee | bat B2 a 0,5301 ? |
|---|---|---|---|
| GPT-4.1, persona JSON | 0,5738 | 66,0 % | oui |
| GPT-4.1, persona JSON, sortie predite | 0,5646 | 60,3 % | oui |
| GPT-4.1-mini, persona texte | 0,5530 | 58,6 % | oui |
| Gemini-Flash-2.5, persona texte | 0,5505 | 77,1 % | oui |
| GPT-4.1-mini, persona texte, questions repetees | 0,5489 | 65,8 % | oui |
| GPT-4.1-mini, persona texte, temperature par defaut | 0,5478 | 64,6 % | oui |
| GPT-4.1-mini, persona JSON (1 000 personnes) | 0,5439 | 62,6 % | oui |
| GPT-4.1-mini, persona texte, raisonnement | 0,5435 | 67,9 % | oui |
| **B2 argmax, k = 30** | **0,5301** | 53,5 % | reference |
| GPT-4.1-mini, resume de persona | 0,5209 | 60,0 % | non |
| **B0 mode** | **0,5216** | 1,1 % | reference |
| GPT-4.1-mini, demographies seules | 0,4996 | 51,1 % | non |
| GPT-4.1-mini, resume plus persona JSON | 0,4742 | 59,3 % | non |
| GPT-4.1-mini, persona JSON, sortie predite | 0,4625 | 47,3 % | non |
| GPT-4.1-mini, affine sur 500 exemples (1 558 personnes) | 0,4619 | 55,6 % | non |

Reponse a la question de a2, limite 5 : **le classement ne tient pas pour tous les modeles**
[MESURE]. Huit configurations sur treize battent B2, cinq perdent, et ces cinq passent aussi sous la
modalite majoritaire. Le fait le plus desagreable est que **l'affinage sur 500 exemples est la
pire des treize** : donner au modele 500 vrais repondants degrade sa fidelite individuelle de
9,1 points par rapport au meme modele en persona texte. Un affinage sur des humains reels ne
s'achete donc pas la fidelite individuelle, du moins pas a cette echelle et avec cette recette.

### 5.2 Ou le modele gagne, bloc par bloc

`resultats/a8-twin-par-bloc.csv`. Figure : `resultats/a8-figure-familles.png`, panneau du bas.

| bloc | items | retest humain | B0 mode | B1 | B2 | GPT-4.1-mini texte | GPT-4.1-mini demo | GPT-4.1 JSON | Gemini | affine 500 |
|---|---|---|---|---|---|---|---|---|---|---|
| Product Preferences - Pricing | 40 | 0,8389 | 0,5590 | 0,5557 | 0,5623 | **0,6687** | 0,5884 | **0,7166** | 0,6694 | 0,5175 |
| Probability matching, probleme 1 | 10 | 0,7336 | 0,7722 | 0,7569 | 0,7712 | 0,7722 | 0,7723 | 0,7722 | 0,7694 | 0,7687 |
| Probability matching, probleme 2 | 6 | 0,7617 | 0,7549 | 0,7355 | 0,7550 | 0,7549 | 0,7549 | 0,7549 | 0,7545 | 0,7572 |
| autres experiences, blocs a 1 ou 2 items | 26 | 0,5836 | **0,5110** | 0,4828 | **0,5131** | 0,4506 | 0,4000 | 0,4293 | 0,4248 | 0,3917 |
| False consensus | 10 | 0,6161 | 0,3973 | **0,4481** | 0,4415 | 0,3686 | 0,3528 | 0,3795 | 0,3828 | 0,3184 |
| Non-experimental heuristics and biases | 10 | 0,4962 | 0,3607 | 0,3531 | **0,3729** | 0,3056 | 0,2589 | 0,2965 | 0,2970 | 0,2969 |
| Linda -no conjunction | 3 | 0,4030 | 0,3618 | 0,3343 | **0,3661** | 0,2899 | 0,2711 | 0,2896 | 0,2818 | 0,1894 |
| Linda-conjunction | 3 | 0,3767 | **0,3709** | 0,3262 | 0,3524 | 0,2310 | 0,2650 | 0,2410 | 0,2465 | 0,2186 |
| **tous les items** | **108** | **0,6861** | 0,5216 | 0,5184 | 0,5301 | 0,5530 | 0,4996 | **0,5738** | 0,5505 | 0,4619 |

**L'hypothese de la section 5 de a2 est fausse.** [MESURE] a2 ecrivait : "la cible de la vague
4 est faite d'experiences d'heuristiques et de biais, ou la reponse depend de la structure du
probleme bien plus que de qui repond [...] un modele de langage dispose d'un savoir sur la
tache elle meme. A verifier item par item avant d'en faire un argument de papier." Verification
faite : sur **tous** les blocs d'heuristiques et de biais, le modele de langage perd contre la
modalite majoritaire, de 5,5 points sur les heuristiques non experimentales, de 7,2 points sur
Linda sans conjonction, de 14,0 points sur Linda avec conjonction, de 2,9 points sur le faux
consensus. Il ne dispose d'aucun avantage sur la tache. Il en a un handicap.

Tout l'avantage vient d'un seul bloc, **les preferences de prix sur 40 produits**, 37 pour cent
des items : +10,6 points pour GPT-4.1-mini et **+15,4 points pour GPT-4.1** contre B2 [MESURE].
Retire ce bloc, et la meilleure configuration passe sous nos baselines.

### 5.3 Pourquoi la, et l'hypothese qui remplace celle de a2

`resultats/a8-twin-correlations.csv`. Trois correlations de rang de Spearman entre l'avantage
du modele par item, defini comme son exactitude moins le meilleur de B1 et B2, et trois
descripteurs de l'item, sur les 108 items.

| descripteur de l'item | GPT-4.1-mini texte | GPT-4.1 JSON | Gemini | affine 500 |
|---|---|---|---|---|
| stabilite test retest humaine | **+0,797** *** | **+0,786** *** | **+0,795** *** | +0,201 * |
| R2 de McFadden des demographies | +0,388 *** | +0,404 *** | +0,411 *** | +0,043 ns |
| R2 de McFadden des voisins | -0,092 ns | -0,058 ns | -0,050 ns | +0,007 ns |

`***` p < 0,001, `*` p < 0,05, `ns` non significatif.

Lecture. **Le predicteur de l'avantage du modele est la stabilite de la personne avec elle
meme, pas l'absence de correlat statistique** [MESURE]. La correlation est de 0,80, elle est
la meme pour les trois familles de modeles, et elle est deux fois plus forte que celle avec
les demographies.

Hypothese de remplacement, etiquetee comme telle [HYPOTHESE] : le modele de langage gagne la
ou il existe un signal individuel stable **et** ou ce signal n'est pas lineairement lisible
dans les reponses passees, ce qui est exactement le cas des preferences de prix, un domaine ou
il sait ce qu'est un produit. Il perd la ou la reponse humaine est proche du bruit, parce qu'il
repond alors la reponse normative ou la reponse modale de son corpus, la ou le vrai humain
oscille. Cette hypothese predit que le modele devrait aussi gagner sur les items de
consommation, de marque et de choix de produit du GSS ou d'autres enquetes. Test le moins
cher : reprendre l'exercice sur un jeu contenant des items de consommation ; nous n'en avons
pas sous la main.

Deux avertissements sur ces correlations [CONFIRME] :

- le R2 de McFadden hors echantillon des demographies est **negatif en moyenne**, -0,0305 sur
  les 108 items, autrement dit la regression logistique fait pire que la marginale en
  vraisemblance sur ce jeu. La correlation de +0,39 est donc calculee sur une plage etroite et
  proche du bruit, et elle est bien plus faible que celle avec le retest. Ne pas la
  surinterpreter ;
- l'avantage moyen par item de GPT-4.1-mini persona texte est de +0,003 seulement, et le
  modele ne bat les baselines que sur **46 items sur 108**. Son avantage global de 2,3 points
  vient d'une minorite d'items ou il gagne beaucoup, pas d'une superiorite diffuse.

---

## 6. Les minorites d'opinion, fiche B4 du BRAINSTORM

Definition [CONFIRME] : pour chaque item, une modalite est minoritaire si moins de 10 pour cent,
puis moins de 20 pour cent, des repondants observes l'ont choisie. Le seuil est descriptif,
calcule sur la population et jamais employe dans une prediction. Trois quantites : le rappel,
part des cellules a reponse minoritaire correctement predites ; la precision, part des cellules
justes parmi celles ou la methode predit une modalite minoritaire ; la masse minoritaire
predite au niveau population, a comparer a la masse humaine.

### 6.1 GSS, seuil 10 pour cent, 5 709 cellules minoritaires sur 156 748, masse humaine 3,64 %

| methode | exactitude globale | rappel minoritaire | precision | masse predite | masse reproduite |
|---|---|---|---|---|---|
| humains reinterroges | 0,7950 | 0,5483 | 0,5306 | 3,76 % | 103 % |
| agents composite | 0,6839 | **0,3069** | 0,3232 | 3,46 % | **95 %** |
| agents entretien (v3) | 0,6565 | 0,2953 | 0,2903 | 3,71 % | 102 % |
| agents enquete | 0,6510 | 0,2305 | 0,2333 | 3,60 % | 99 % |
| agents v8 | 0,5591 | 0,1717 | 0,1483 | 4,22 % | 116 % |
| agents demographiques (v6) | 0,5818 | 0,1624 | 0,3592 | 1,65 % | 45 % |
| B1 tirage | 0,5426 | 0,1118 | 0,1110 | 3,67 % | 101 % |
| B2 tirage | 0,5752 | 0,1093 | 0,1286 | 3,09 % | 85 % |
| agents v7 | 0,5640 | 0,0673 | 0,1307 | 1,88 % | 52 % |
| B0 tirage | 0,4918 | 0,0617 | 0,0618 | 3,64 % | 100 % |
| B1 argmax | 0,6209 | 0,0580 | 0,2213 | 0,95 % | 26 % |
| **B2 argmax** | **0,6717** | **0,0357** | 0,4892 | **0,27 %** | **7 %** |
| B0 mode | 0,5934 | 0,0000 | sans objet | 0,00 % | 0 % |

Au seuil de 20 pour cent, meme ordre : agents composite 0,3554 de rappel, agents entretien
0,3532, B2 argmax 0,0940, B1 argmax 0,1299, B0 mode 0,0000. Tableau complet dans
`resultats/a8-minorites-gss.csv`.

### 6.2 Twin-2K-500, seuil 10 pour cent, 6 971 cellules minoritaires sur 168 768, masse humaine 4,13 %

| methode | exactitude globale | rappel minoritaire | masse predite | masse reproduite |
|---|---|---|---|---|
| humains retest vagues 1 a 3 | 0,7119 | 0,3867 | 4,45 % | 108 % |
| Gemini-Flash-2.5, persona texte | 0,5505 | **0,1823** | 5,57 % | 135 % |
| GPT-4.1, persona JSON | 0,5738 | 0,1317 | 4,29 % | 104 % |
| GPT-4.1-mini, persona texte | 0,5530 | 0,1218 | 3,10 % | 75 % |
| B1 tirage | 0,4620 | 0,1109 | 4,15 % | 100 % |
| B2 tirage | 0,4620 | 0,0855 | 3,73 % | 90 % |
| B1 argmax | 0,5184 | 0,0821 | 1,72 % | 42 % |
| GPT-4.1-mini, demographies seules | 0,4996 | 0,0567 | 2,55 % | 62 % |
| **B2 argmax** | **0,5301** | **0,0139** | **0,20 %** | **5 %** |
| B0 mode | 0,5216 | 0,0000 | 0,00 % | 0 % |

Tableau complet, vingt methodes et deux seuils : `resultats/a8-minorites-twin.csv`.

### 6.3 Ce que ces trois tableaux etablissent

1. **La hierarchie de a2 s'inverse integralement sur les minorites** [MESURE]. B2, meilleure
   baseline de a2 sur les deux jeux, est **derniere ou avant derniere** sur le rappel
   minoritaire, derriere le tirage marginal aveugle. Sur le GSS, B0 tirage, qui ne sait rien
   de personne, retrouve 6,2 pour cent des minorites contre 3,6 pour cent pour B2 argmax.
2. **La precision de B2 argmax est pourtant la plus haute de toutes, 0,4892** [MESURE] : quand
   elle ose une modalite minoritaire, elle a raison une fois sur deux. Elle n'ose presque
   jamais. C'est la signature exacte de l'ecrasement de variance, vue du cote des queues.
3. **Les agents de langage sont les seuls a tenir le rappel et la masse ensemble** [MESURE].
   L'agent composite reproduit 95 pour cent de la masse minoritaire humaine avec un rappel de
   30,7 pour cent, soit **8,6 fois celui de B2**. Aucune baseline ne s'en approche.
4. **Attention au piege de la masse seule** [CONFIRME]. B0 tirage et B1 tirage reproduisent
   100 pour cent de la masse minoritaire avec un rappel de 6 a 11 pour cent : ils mettent des
   minorites au bon taux mais aux mauvais endroits. La masse ne se lit qu'avec le rappel, et
   c'est pour cela que les deux sont rapportes cote a cote.

---

## 7. Ce que ces resultats changent a a2

### 7.1 Chiffres de a2 qui restent vrais, verifies en les rejouant

- GSS, tableau de la section 4 [CONFIRME] : B2 argmax 0,6717 reproduit a l'identique,
  B1 argmax 0,6209, B0 mode 0,5934, agents composite 0,6839, plancher humain 0,7950.
- Twin, tableau de la section 5 [CONFIRME] : B2 argmax 0,5301, B0 mode 0,5216, B1 argmax
  0,5184, GPT-4.1-mini persona complet 0,5530, demographies seules 0,4996, plancher humain
  0,7119. Tous reproduits au quatrieme chiffre.
- Section 7, planchers par famille [CONFIRME] : les plafonds "modalite majoritaire" annonces
  par a2 se retrouvent a moins d'un demi point pres dans notre B0 mode hors echantillon, par
  exemple 57,7 contre 57,33 pour `nat*`, 74,4 contre 74,36 pour `ab*`.
- La conclusion generale de a2 sur le GSS, "cinq des six conditions d'agents de Stanford sont
  battues par du scikit-learn sur les 149 items", n'est pas contredite : rien dans ce rapport
  ne recalcule ce chiffre la sur les 149 items.

### 7.2 Chiffres et phrases de a2 qui bougent

| element de a2 | ce que a8 mesure |
|---|---|
| Limite 1, "l'optimisme induit par le k est d'au plus 0,2 point" | 0,06 point sur le GSS. Sur Twin, le biais est **inverse** : la validation interne choisit k = 100 et gagne 0,44 point |
| Section 5, "B2 argmax 0,5301" sur Twin | avec le k choisi proprement, **0,5345** ; l'ecart avec GPT-4.1-mini passe de 2,3 a 1,85 point |
| Section 4, "seul l'agent composite tient encore" | faux sur les 70 items ordinaux : la copule gaussienne fait 0,5840 contre 0,5596, **toutes** les conditions d'agents sont battues sur ce sous ensemble |
| Section 8, "aucune de nos baselines n'atteint ce coin du plan" | la copule en mode tirage atteint un accord par paires de 38,8 % contre 38,5 % chez les humains sur les items ordinaux, ce qu'aucun agent n'egale |
| Limite 7, "un decoupage par famille donnerait un B2 plus bas" | chiffre : **-3,4 points** sur les 58 items concernes, et cela suffit a faire passer composite et enquete **devant** B2 |
| Section 10, point 1, "la baseline non LLM obligatoire, c'est B2 k = 30" | insuffisant. Il faut B2 **et** la copule sur les items ordinaux, et B2 doit etre evaluee en decoupage par famille, pas en blocs aleatoires |
| Section 5, hypothese "la vague 4 est faite d'heuristiques et de biais ou le modele a un savoir sur la tache" | **fausse** [MESURE]. Le modele perd sur tous les blocs d'heuristiques et de biais. Son avantage vient des 40 items de preferences de prix |
| Limite 5, "le classement pourrait bouger avec un autre modele" | il bouge : 8 configurations sur 13 battent B2, 5 perdent, l'affinage sur 500 exemples est la pire des treize a 0,4619 |
| Section 3.2, description du contexte Twin | a completer : le contexte ne contient **aucun** item des blocs de la vague 4, donc les chiffres Twin de a2 sont deja en regime "famille retiree" |
| Section 8, "le seul avantage clair des LLM est le couple exactitude et diversite" | il y en a un second, plus net et plus vendable : le **rappel des minorites**, 8,6 fois celui de B2 sur le GSS |

### 7.3 Consequence sur le test existentiel

Le test existentiel A4 du BRAINSTORM etait pose ainsi : existe t il un regime ou le modele de
langage bat une baseline statistique ? La reponse de a2 etait "partagee". La reponse de a8 est
plus precise et plus utilisable [MESURE] :

1. **Sur les questions dont la famille entiere est absente du corpus**, oui, sur le GSS, et
   avec en plus une diversite preservee de 94,8 pour cent contre 58,0 pour cent. C'est le
   premier regime ou une condition d'agent domine sur les deux axes.
2. **Sur les minorites d'opinion**, oui, largement, sur les deux jeux et pour toutes les
   conditions d'agents sauf v7.
3. **Sur les items ordinaux d'un questionnaire dense**, non, et c'est pire qu'en a2 : la
   copule bat les six conditions.
4. **Sur les experiences d'heuristiques et de biais**, non, et le modele perd meme contre la
   modalite majoritaire.

---

## 8. Ce que je n'ai pas pu verifier

1. **La copule n'existe que sur le GSS et sur ses 70 items ordinaux.** [CONFIRME] Les 79 items
   nominaux n'ont pas d'ordre exploitable et une copule gaussienne ne les couvre pas sans une
   extension a variables latentes multinomiales, qui n'est pas construite ici. Aucune copule
   n'a ete construite sur Twin-2K-500.
2. **La correlation latente est approchee par la correlation de Pearson des scores normaux**,
   pas estimee par maximum de vraisemblance polychorique. Le chiffre de 0,5840 est donc un
   plancher pour cette famille de methodes.
3. **La courbe de croisement de la section 6 de a2 n'a pas ete refaite** avec le k choisi par
   validation interne ni avec la copule. Les seuils de 145, 180 et 250 repondants qui y sont
   annonces ne sont ni confirmes ni infirmes ici.
4. **Le decoupage par famille n'a pas ete etendu a la totalite des 149 items du GSS**, seulement
   aux 58 qui appartiennent a une famille thematique fermee et verifiable au libelle. Un
   decoupage par famille couvrant tout le questionnaire demanderait une taxonomie complete des
   149 items, qui n'existe pas dans l'archive.
5. **Aucune analyse de variance intra contre inter groupes** n'est faite ici. Ce rapport parle
   d'exactitude, de diversite globale et de queues, pas de double distorsion. Les chiffres de
   diversite ne se substituent pas au travail de a1.
6. **La stabilite test retest des items de Twin est mesuree entre vagues 1 a 3 et vague 4**,
   soit un delai variable de deux a quatre semaines selon la vague d'origine, la ou le retest
   du GSS est a deux semaines fixes. La correlation de 0,80 de la section 5.3 est donc calculee
   contre une quantite dont le delai n'est pas constant.
7. **Les variantes `tirage` reposent toujours sur un tirage aleatoire unique a graine fixee**,
   limite 6 de a2, non levee ici.
8. **Les trois configurations a couverture partielle** (1 000, 1 558 et 2 050 personnes) sont
   comparees aux baselines calculees sur 2 058 personnes. Le denominateur des cellules differe,
   et la couverture est rapportee, mais la comparaison n'est pas strictement appariee.
9. **Aucune verification n'a ete faite sur la contamination** : les 40 produits du bloc de
   preferences de prix pourraient figurer dans les corpus d'entrainement des modeles evalues.
   C'est l'objection la plus evidente contre le resultat central de la section 5.2 et elle
   n'est pas traitee.

---

## 9. Questions ouvertes pour Simon

1. **Le resultat des minorites est il publiable seul ?** Un banc d'essai qui montre que la
   meilleure baseline statistique retrouve 3,6 pour cent des opinions minoritaires quand un
   agent de langage en retrouve 30,7 pour cent est une mesure que personne ne publie, et elle
   renverse la lecture habituelle "les LLM ecrasent la diversite". Est ce un papier de
   methodologie, une section d'un papier plus large, ou une figure de vente ?
2. **La correlation de 0,80 entre l'avantage du modele et la stabilite test retest de l'item
   correspond elle a un construit connu ?** Elle dit que le modele ne gagne que la ou l'humain
   est fiable avec lui meme. Existe t il en psychometrie un nom pour ce plafond, et une
   litterature qui l'a deja formule pour les predicteurs non humains ?
3. **Faut il retirer le bloc de preferences de prix des analyses de Twin ?** Il porte 37 pour
   cent des items et 100 pour cent de l'avantage du modele. Le garder rend le jeu favorable au
   modele pour une raison qui est peut etre de la connaissance produit et peut etre de la
   contamination. Le retirer rend Twin-2K-500 inutile comme jeu porteur.
4. **La copule doit elle devenir la baseline officielle du projet a la place de B2 ?** Elle est
   meilleure sur les items ordinaux, elle restitue une dispersion realiste, et elle est
   l'adversaire cite dans la litterature. Le cout est qu'elle ne couvre pas les items nominaux,
   qui sont la majorite du GSS.
5. **L'affinage sur 500 exemples degrade la fidelite individuelle de 9,1 points.** Est ce un
   resultat attendu de son point de vue, un artefact de la recette des auteurs, ou un signal
   exploitable contre la these du "il suffit d'affiner sur des vraies personnes" ?
6. **Le regime "famille retiree" doit il devenir le protocole par defaut du projet ?** Il est
   plus severe, il est plus proche du cas d'usage reel d'un institut, et c'est le seul ou une
   condition d'agent domine nos baselines sur les deux axes. Il coute 3,4 points a B2 et il
   demande une taxonomie d'items que personne ne publie.

---

Chiffres desagreables de ce rapport, rassembles pour qu'ils ne se perdent pas : la copule bat
les six conditions d'agents de Stanford sur les items ordinaux ; le modele de langage perd
contre la modalite majoritaire sur tous les blocs d'heuristiques et de biais de Twin ;
l'affinage sur 500 humains reels est la pire des treize configurations ; et l'hypothese
explicative de la section 5 de a2 est fausse.
