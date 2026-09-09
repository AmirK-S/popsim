# P1. L'experience de lecture : ce que lire un assistant dit de l'autre camp fait aux croyances de second ordre

Preenregistrement, redige le 9 septembre 2026, destine a etre depose sur OSF tel quel, sous le
gabarit **OSF Preregistration** version 2, dont les cinq pages et les vingt-cinq champs sont
repris ici dans l'ordre [CONFIRME,
https://raw.githubusercontent.com/CenterForOpenScience/osf.io/develop/website/project/metadata/osf-preregistration.json].

Ce document execute le **mois 6 du programme A** de `MOONSHOTS.md`, section 3, et la moitie
causale de M3 dans `brainstorm/01-democratie-basculements.md` et
`brainstorm/04-science-esprit-societes.md`. Le premier terme, ce que les modeles disent des
camps, est mesure par `resultats/r1-resultats.md`. Le second terme, ce que les humains croient
des camps, est etabli par `resultats/a46-second-ordre-ahler-sood.md`. Ce protocole produit le
**troisieme**, l'effet causal de la lecture.

**Aucune donnee n'a ete collectee. Aucun appel de modele de langage n'a ete passe pour ecrire
ce document. Aucun fichier existant du depot n'a ete modifie.** Le seul calcul est un calcul de
puissance sans donnees, `protocoles/p1-puissance.py`.

Conventions de certitude : **[MESURE]** calcule sur nos donnees, **[CONFIRME]** lu dans une
source verifiee avec son adresse, **[PROBABLE]** interpretation etayee non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Avant tout : les quatre decisions de conception, et pourquoi

Quatre questions ne se tranchent pas dans un tableau et commandent tout le reste. Elles sont
tranchees ici, avant les champs du gabarit, avec leur cout.

### Decision 1. Le bras « modele » est decline par modele, il n'est pas tire au hasard

`MOONSHOTS.md` ecrit « trois bras, description du modele, distribution vraie, rien ». Ce plan
supposait que « la description du modele » soit une chose. R1 mesure qu'elle n'en est pas une.

Sur l'ecart entre camps, les trois modeles rendent des facteurs de **0,245, 0,618 et 1,268**,
dont les intervalles de confiance **excluent le plancher humain dans des directions opposees**
[MESURE, r1 section 1.2]. L'ecart entre le facteur le plus bas et le plus haut vaut **5,2** sur
les 79 items orientes, et la dispersion entre modeles **depasse l'erreur de chacun** [MESURE, r1
section 5.1].

Consequence directe pour un plan d'experience. Si l'on tire un modele au hasard par
participant, l'estimateur du bras « modele » est la **moyenne d'effets dont la theorie predit
les signes opposes** : Qwen3-4B ecrase l'ecart entre camps et devrait donc reduire la
polarisation percue, Qwen3-30B-A3B l'exagere et devrait l'augmenter. Un zero mesure sur ce bras
serait **indistinguable** de deux issues contraires, « lire un modele ne fait rien » et « les
modeles font des choses opposees qui s'annulent ». Ce n'est pas une perte de puissance, c'est
une perte d'identification : la quantite estimee n'aurait pas d'interpretation.

**Donc : trois bras modele, un par modele, plus le bras distribution vraie, plus le temoin.
Cinq bras, et six avec la decision 4.** Le cout est de deux bras de plus a financer, chiffre en q14. Le gain
est triple : trois tests diriges au lieu d'un, une **prediction d'ordonnancement** entre les
trois bras que rien d'autre dans le champ ne sait formuler (section Hypotheses, H4), et un test
groupe conserve en secondaire sur la seule mesure ou les trois modeles concordent.

Le tirage au hasard reste disponible comme variante, et il est **ecarte avec sa raison**, ce qui
est le format que `PROTOCOLES-DE-RECHERCHE.md` section 2.8 demande.

**Ce que l'errata E3 de `MOONSHOTS.md` demande en plus, et ce qui est fait.** L'errata du
9 septembre, ecrit apres R1, demande des bras « indexes par modele **et par identite du
demandeur** », plus un **bras de taux de base**, plus la mesure de la variete percue a cote de
l'ecart percu. Trois demandes, deux tenues et une reportee. La variete percue devient une mesure
principale, `HOM_out`, et elle porte H3. Le bras de taux de base est ajoute, section Decision 4.
L'indexation par identite du demandeur **ne tient pas dans 1 500 a 2 000 personnes** : elle
porterait le plan a neuf bras et exigerait 2 528 analyses, chiffre en q14 ; elle est
declaree en extension E1 avec son cout, et c'est la premiere chose a financer si le budget monte.
Le protocole ne peut pas faire semblant de tenir les trois.

### Decision 2. Le texte lu est presente comme une reponse d'assistant, sans tromperie sur la source

Deux variantes existaient. Ne pas dire d'ou vient le texte mesure l'effet du texte nu ; le dire
mesure l'effet de **la situation reelle**, un citoyen qui demande a un assistant ce que pense
l'autre camp. La quantite que le programme A veut porter devant un regulateur est la seconde :
c'est celle qui est produite des centaines de millions de fois par jour. Elle a en outre
l'avantage decisif de **supprimer la tromperie sur la source**, ce qui allege le passage en
comite et rend le debriefing simple.

**Donc : dans les trois bras modele, la consigne dit que le texte est la reponse d'un assistant
conversationnel a la question posee.** La variante non etiquetee est declaree en extension E2 et
n'est pas financee ici.

### Decision 3. L'ancrage des camps est le parti pour les compositions, l'ideologie pour les opinions

C'est la reponse a la question ouverte 3 de `a46`. Ahler et Sood interrogent le **parti** ; R1
interroge l'**ideologie**. Melanger les deux dans un indice unique fabriquerait une quantite qui
n'a de referent nulle part.

**Donc : le bloc composition emploie le parti, au mot pres d'Ahler et Sood, et le bloc opinion
emploie l'ideologie, au mot pres de R1. Chaque participant est classe sur les deux axes. Les
deux blocs ont chacun leur mesure principale et ne sont jamais additionnes.** Le cout est ecrit :
il n'y aura pas de nombre unique resumant l'experience, et il faut le dire au partenaire avant
qu'il ne le demande.


### Decision 4. Un sixieme bras, les taux de base, parce que c'est la ou la litterature predit l'inverse du bon sens

Ahler et Sood testent quatre explications alternatives a la mauvaise perception de la composition
des partis, dont l'ignorance des taux de base de la population. Leur condition **Base Rates**
fournit au repondant la part de chaque groupe dans la population americaine avant de lui demander
sa part dans le parti. Le resultat est contre intuitif et il est net : **fournir les taux de base
augmente la perception au lieu de la reduire**, de sept a neuf points sur les huit dyades
[CONFIRME, tableau 2 du papier, n de 91 a 98 par condition] :

| dyade | condition standard | condition taux de base | ecart | d de Cohen reconstruit |
|---|---|---|---|---|
| `dem_black` | 36,2 | 43,2 | +7,0 | 0,297 |
| `dem_lgb` | 27,0 | 35,9 | +8,9 | 0,308 |
| `rep_rich` | 31,5 | 39,2 | +7,7 | 0,276 |
| `rep_evang` | 46,6 | 56,0 | +9,4 | 0,349 |
| `rep_old` | 44,7 | 53,1 | +8,4 | 0,398 |

[CONFIRME pour les moyennes et intervalles ; MESURE pour les d, reconstruits des intervalles et
des effectifs publies]

Pourquoi ce bras compte ici plus qu'ailleurs. R1 mesure que le defaut des modeles **est** un
defaut de taux de base : une modalite reellement sous 1 pour cent recoit 11,9 pour cent en
moyenne, le point fixe est vers un tiers, et la deformation est monotone sur 8 718 modalites
[MESURE, r1 section 3.3]. Si l'on ne teste pas le bras taux de base, un effet des bras modele sera
attribue a la representation des camps alors qu'il pourrait n'etre qu'un effet d'ancrage
numerique, deja documente chez les humains et **de signe oppose a l'intuition corrective**. Le
bras F est donc le seul controle qui separe « le modele deforme le portrait du camp » de « un
nombre est apparu a l'ecran ».

**Donc : six bras.** L'effet attendu y est grand, d de 0,28 a 0,40, ce qui permet de lui allouer
moins de participants qu'aux bras modele : voir l'allocation inegale en q13.

---

# Page 1. Study Information

## q1. Titre

Ce que lire un assistant dit de l'autre camp fait aux croyances de second ordre : une experience
randomisee a six bras avec la description de trois modeles, la distribution vraie, les taux de base
et un temoin.

## q2. Auteurs

A completer au depot. Champ obligatoire du gabarit. Le protocole exige un partenaire de science
politique co-signataire, sans lequel il n'est pas deposable : voir `resultats/p1-protocoles.md`,
section « ce qui manque ».

## q3. Description

Les Americains se trompent lourdement sur la composition de leurs partis. Ahler et Sood
etablissent, sur un echantillon YouGov de 1 000 personnes et trois echantillons MTurk, que les
gens croient que **32 pour cent des democrates sont gais, lesbiennes ou bisexuels contre 6 en
realite, et que 38 pour cent des republicains gagnent plus de 250 000 dollars par an contre 2**
[CONFIRME, resume du papier, http://gsood.com/research/papers/partisanComposition.pdf ; recalcul
independant dans `resultats/a46-ahler-sood-items.csv`, ecart maximal de 1,6 x 10^-6 point contre
les fichiers des auteurs]. Ils montrent en outre, par experience randomisee, que **corriger cette
croyance rend l'autre camp moins extreme aux yeux du repondant et reduit l'animosite**
[CONFIRME, meme source].

Une source nouvelle de croyances de second ordre est apparue depuis : les assistants
conversationnels, a qui des centaines de millions de personnes demandent ce que pense l'autre
camp. Le run R1 mesure ce que trois modeles ouverts repondent a cette question sur 149 items du
GSS a distribution par camp connue, contre la realite et contre un plancher de reinterrogation
humaine. Trois faits en sortent, et ils fixent la question de cette experience :

1. **Les trois modeles decrivent tous les camps comme plus varies qu'ils ne sont**, rapport de
   1,01 a 1,18 sur dix-huit cellules sur dix-huit, contre un plancher humain de 1,00 [MESURE, r1
   section 1.1]. C'est l'inverse de ce que le programme supposait.
2. **Ils se contredisent sur l'ecart entre camps**, facteurs 0,245, 0,618 et 1,268, intervalles
   disjoints du plancher dans des directions opposees [MESURE, r1 section 1.2].
3. **Ils gonflent les modalites rares et rabotent les modalites massives**, point fixe vers un
   tiers : une modalite a moins de 1 pour cent de realite recoit 11,9 pour cent en moyenne
   [MESURE, r1 section 3.3, 8 718 modalites].

La question est donc : **lire ce qu'un assistant dit de l'autre camp change t il ce que les gens
croient de l'autre camp, dans quel sens, et de combien, par rapport a lire la distribution vraie
ou a ne rien lire ?** Elle se pose maintenant parce que le premier terme est mesure, parce que le
second terme et son instrument existent chez Ahler et Sood, et parce que la reponse decide de ce
que le programme A peut ecrire pour un regulateur : une norme d'audit avec un volet causal, ou
une norme d'audit sans.

Trois issues sont possibles et **les trois se publient**. La lecture depolarise, parce que les
modeles sur dispersent les camps et rabotent les modalites massives ; alors l'assistant est un
correcteur, et c'est l'issue la plus consequente pour une plateforme. La lecture polarise, au
moins pour le modele qui exagere l'ecart ; alors la fidelite de representation devient une
quantite de risque systemique. La lecture ne fait rien ; alors la norme se publie sans son volet
causal, exactement comme `MOONSHOTS.md` section 3 le prevoit deja comme point d'arret.

## q4. Hypotheses

Sept hypotheses, chacune declaree **dirigee** ou **non dirigee**, avec sa source. Les hypotheses
dirigees sont testees en bilateral quand meme ; la direction est enregistree pour que le score
final compte les predictions tenues, comme `c1` le fait sur ses six predictions.

### Famille P, deux tests, la validation de l'instrument et l'effet groupe

**H1, dirigee.** Le bras **distribution vraie** reduit l'erreur absolue moyenne des estimations
de second ordre sur le camp adverse, par rapport au temoin. Source : la verification de
manipulation d'Ahler et Sood, ou l'erreur absolue moyenne passe de **27,7 a 6,1 points, chute de
21,6 points, IC 95 pour cent [-23,6 ; -19,5]** [CONFIRME]. Effet attendu chez nous : grand, c'est
une verification de manipulation autant qu'une hypothese. **Si H1 echoue, rien n'est conclu du
reste** : voir les criteres de chute.

**H2, dirigee.** Le bras **distribution vraie** reduit la part de placements du sympathisant
typique du camp adverse a l'extremite des echelles de politique publique, par rapport au temoin.
Source : l'effet mesure par Ahler et Sood, **moins 6,6 points, IC [-0,11 ; -0,02]**, soit un d de
Cohen de **0,219** apres reconstruction de l'ecart type implique [CONFIRME pour la difference et
l'intervalle, MESURE pour la conversion, `protocoles/p1-puissance.py` section 3].

### Famille M, trois tests, un par modele, la question du programme

**H3, dirigee, sur les trois bras modele a la fois.** Chacun des trois bras modele **reduit
l'homogeneite percue du camp adverse** par rapport au temoin. Source : R1 section 1.1, dix-huit
cellules sur dix-huit au dessus de 1, quinze significatives apres Holm, sur les trois modeles et
les trois camps. C'est la seule prediction que le dossier autorise sur les trois modeles a la
fois, et **elle contredit l'enonce d'origine du programme A**, « la reponse est plus unanime que
la realite ». Elle est ecrite ici dans le sens que la mesure impose, pas dans le sens que le
programme esperait.

**H4, prediction d'ordonnancement, dirigee.** Sur l'**ecart percu entre les deux camps**, les
trois bras modele se classent dans l'ordre de leurs facteurs mesures en R1 : Qwen3-4B (0,245) au
plus bas, gpt-oss-20b (0,618) au milieu, Qwen3-30B-A3B (1,268) au plus haut ; et le bras
Qwen3-30B-A3B depasse le temoin quand le bras Qwen3-4B lui est inferieur. Test :
correlation de rang de Spearman entre le rang des trois bras sur la mesure humaine et le rang de
leurs facteurs R1, plus le contraste lineaire preenregistre. **C'est l'hypothese la plus forte du
protocole** : elle predit non pas qu'un effet existe, mais qu'une quantite mesuree sur la machine
a une nuit de calcul **ordonne des effets sur des lecteurs humains**. Si elle tient, la quantite
d'audit de R1 est validee comme predicteur d'un effet reel, ce qui est exactement ce qu'un
regulateur demande d'une norme. Si elle tombe, la quantite reste auditable mais perd sa
justification causale, et il faut l'ecrire.

**H5, dirigee.** Sur les items dont la modalite vraie est rare, part reelle sous 10 pour cent,
les trois bras modele **augmentent** l'estimation que les participants donnent de cette part,
par rapport au temoin. Source : la courbe d'etalonnage de R1, section 3.3, ou une modalite sous
1 pour cent recoit 11,9 pour cent en moyenne et une modalite entre 5 et 10 pour cent en recoit
18,7. Cette hypothese porte le sous entendu politique le plus lourd du dossier : si elle tient,
l'assistant **installe la meme erreur que celle qu'Ahler et Sood documentent chez les humains**,
et sur les memes groupes rares.

**H6, dirigee, bras F.** Le bras **taux de base** **augmente** l'erreur des estimations de second
ordre par rapport au temoin, au lieu de la reduire. Source : la condition Base Rates d'Ahler et
Sood, plus sept a neuf points sur les huit dyades, d reconstruit de **0,276 a 0,398** [CONFIRME
pour les moyennes, MESURE pour les d]. C'est la seule hypothese du protocole dont la direction
contredit le bon sens correctif, et c'est celle qui distingue un effet de representation d'un
effet d'ancrage numerique.

### Famille S, secondaires, non confirmatoires

**H7, dirigee.** Le bras distribution vraie reduit l'animosite envers le camp adverse, mesuree
par le thermometre de sentiment et par l'indice de distance sociale. Source : Ahler et Sood,
**6,4 points sur 100 au thermometre, IC [-0,10 ; -0,03] en echelle 0 a 1, soit d = 0,273**, et
**2,5 points de distance sociale, IC [-0,05 ; 0,00], soit d = 0,168** [CONFIRME pour les
differences, MESURE pour les conversions].

**H8, non dirigee.** Les bras modele deplacent l'animosite. **Aucune direction n'est predite**,
et cette absence est un resultat de R1 : la mesure de direction du deplacement selon l'identite
du demandeur est **nulle sur les six cellules apres Holm** [MESURE, r1 section 1.3], donc le
dossier n'autorise aucune prediction de sens sur l'affect. Toute phrase de la forme « le modele
caricature le camp adverse » est interdite dans ce protocole comme elle l'est dans r1.

---

# Page 2. Design Plan

## q5. Type d'etude

Experience. Des participants sont assignes au hasard a des traitements et une mesure est prise
apres.

## q6 et q7. Aveuglement

**Participants** : aveugles a l'existence des autres bras et a l'hypothese. La question de
composition est presentee, comme chez Ahler et Sood, a l'interieur d'une enquete plus large de
connaissance politique, precisement pour limiter la demande experimentale [CONFIRME, « To deter
demand effects, we couched the composition questions as part of a broader political knowledge
survey »].

**Analystes** : les bras arrivent au script d'analyse sous les etiquettes A, B, C, D, E, dont la
table de correspondance est scellee et deposee sur OSF au moment du preenregistrement, ouverte
apres le gel du script. C'est la version praticable du jeu tenu secret de
`PROTOCOLES-DE-RECHERCHE.md` section 2.4.

**Generation des textes** : les textes des bras modele sont produits **avant** le
preenregistrement, geles, hachages SHA-256 deposes avec le protocole. Personne ne les choisit
apres avoir vu un chiffre.

## q8. Plan d'experience

Plan entre sujets a **six bras**, une seule seance, environ vingt minutes, **a allocation
inegale** : le temoin recoit `sqrt(5)` fois l'effectif d'un bras traite, ce qui est l'allocation
optimale quand cinq traitements sont compares a un meme temoin.

| bras | part de l'echantillon | ce que le participant lit | role |
|---|---|---|---|
| **A. Temoin** | 558 | un texte non politique de longueur appariee | plancher, comparateur commun, egalisation du temps de lecture |
| **B. Distribution vraie** | 250 | la distribution reelle par camp, mise en page comme une reponse d'assistant | reproduction d'Ahler et Sood, validation de l'instrument |
| **C. Modele 1, Qwen3-4B-Instruct-2507** | 250 | la reponse du modele a la meme question | facteur R1 = 0,245, ecrase l'ecart |
| **D. Modele 2, gpt-oss-20b** | 250 | idem | facteur R1 = 0,618, ecrase moins |
| **E. Modele 3, Qwen3-30B-A3B-Instruct-2507** | 250 | idem | facteur R1 = 1,268, exagere |
| **F. Taux de base** | 250 | la part de chaque groupe dans la population americaine, sans aucune information par camp | separe l'ancrage numerique de la representation des camps ; effet attendu **positif** |

**Deroule.** Consentement ; demographies et double classement partisan et ideologique ; bloc de
connaissance politique servant de couverture et de covariable ; **mesure avant sur une moitie des
items, tiree au hasard par participant** ; texte du bras ; **mesure apres sur les seize items** ;
echelles d'extremite percue ; thermometre et distance sociale ; sonde de suspicion ; debriefing
complet avec les vraies valeurs.

**Pourquoi la mesure avant ne porte que sur une moitie des items.** Ahler et Sood mesurent que le
simple fait de demander des nombres depolarise deja : leur condition **ask** deplace l'extremite
percue de **moins 0,03, IC [-0,08 ; 0,01]**, soit environ la moitie de l'effet de la correction,
juste sous le seuil [CONFIRME]. Une mesure avant sur tous les items traiterait donc **tous les
bras** avant le traitement, ecraserait la marge du bras B et biaiserait tout vers le pole
corrige. La moitie tiree au hasard resout les deux problemes a la fois : la mesure principale est
faite **apres seulement, sur les items non pre mesures**, donc non contaminee ; la mesure avant
de l'autre moitie sert de **covariable** dans l'ANCOVA, ce qui rend une partie du gain de
precision ; et la comparaison, a l'interieur du bras temoin, entre items pre mesures et items non
pre mesures **estime l'effet ask lui meme**, qui devient une quantite secondaire du protocole.
Cette derniere quantite a une valeur propre : si demander des nombres depolarise la moitie autant
que dire la verite, la correction la moins chere qu'une plateforme puisse deployer est un champ
de saisie, pas un encart de correction.

## q9. Randomisation

Assignation au bras par tirage aleatoire simple, **stratifiee par identification partisane en
trois classes**, democrate avec les proches, republicain avec les proches, independant pur, les
independants purs etant assignes au hasard a un camp adverse comme chez Ahler et Sood [CONFIRME,
note de bas de page du papier]. Sequence produite par la plateforme d'enquete avec une graine
fixee et journalisee. Ordre des items randomise a l'interieur de chaque batterie ; ordre des deux
batteries partisanes randomise ; ces randomisations sont celles d'Ahler et Sood, reprises pour
comparabilite [CONFIRME].

---

# Page 3. Sampling Plan

## q10 et q11. Donnees existantes

Aucune. Les donnees n'existent pas au moment du depot. Les jeux **deja detenus** et utilises pour
construire le materiel, jamais comme donnees d'analyse, sont : `data/ahler-sood-pcomp/`
(Harvard Dataverse, `doi:10.7910/DVN/CLMQ8E`, CC0 1.0), le jeu GSS de Stanford et les
distributions par camp de `a30`, et les traces de R1 dans `data/traces/`.

## q12. Procedures de collecte

Panel en ligne, adultes americains, quotas sur l'age, le sexe, la region et l'identification
partisane. Plateforme principale : **Prolific**. Criteres de filtrage : residence aux Etats Unis,
langue premiere anglais, taux d'approbation superieur a 95 pour cent, aucune participation a une
etude anterieure du meme projet, liste d'exclusion tenue par identifiant.

## q13. Taille d'echantillon

**1 806 participants analyses, repartis en allocation inegale : 558 au temoin et 250 a chacun des
cinq bras traites, pour 2 080 recrutes.** Le detail est en q14.

**Pourquoi l'allocation est inegale.** Cinq bras sont compares au meme temoin. La variance d'un
contraste vaut `sigma^2 (1/n_traite + 1/n_temoin)` ; a effectif total fixe, elle est minimale
quand le temoin recoit `sqrt(5) = 2,24` fois l'effectif d'un bras traite. Avec 250 par bras traite
et 558 au temoin, `1/250 + 1/558 = 0,005789`, contre `2/345 = 0,005797` pour un plan equilibre a
345 par bras : **le contraste a la meme precision qu'un plan equilibre a 345 par bras, pour
1 806 personnes au lieu de 2 070** [MESURE, `p1-puissance.py`]. L'allocation inegale paye
exactement le sixieme bras.

## q14. Justification de la taille, calcul de puissance

Script : `protocoles/p1-puissance.py`, execute avec `.venv/bin/python`, sans aucune donnee.

**Effet attendu, tire de la litterature de correction.** Les trois effets d'Ahler et Sood,
convertis en d de Cohen a partir de leurs differences publiees, de leurs intervalles de confiance
et de leurs effectifs par bras, valent :

| quantite | difference publiee | IC 95 pour cent | n par bras | ecart type implique | **d** |
|---|---|---|---|---|---|
| part de placements a l'extreme | 0,066 | [0,02 ; 0,11] | 345 | 0,302 | **0,219** |
| thermometre, echelle 0 a 1 | 0,064 | [0,03 ; 0,10] | 345 | 0,235 | **0,273** |
| distance sociale | 0,025 | [0,00 ; 0,05] | 274 | 0,149 | **0,168** |

[CONFIRME pour les differences et intervalles ; MESURE pour les conversions,
`p1-puissance.py` section 3]

Un quatrieme ancrage, plus recent et sur un autre canal : le rerangement par modele de langage de
l'animosite partisane dans un fil d'actualite deplace le thermometre de **deux points sur cent**
en dix jours sur 1 256 participants [CONFIRME, arXiv 2411.14652, publie dans *Science* 390(6776),
27 novembre 2025]. Deux points sur cent avec un ecart type de thermometre de l'ordre de 25 points
correspond a un d de **0,08**, c'est a dire un effet **hors de portee** d'une seance unique a
notre budget. C'est une information de conception, pas une objection : notre mesure principale
n'est pas l'affect mais la croyance, ou les effets de correction sont trois fois plus grands.

**L'effet retenu pour le calcul est d = 0,22**, la valeur de la mesure de croyance d'Ahler et
Sood, la plus proche de notre mesure principale. Elle est **conservatrice pour le bras B**, dont
la verification de manipulation chez eux vaut 21,6 points d'erreur absolue, un effet enorme ; elle
est **le pari du protocole pour les bras modele**, pour lesquels aucun ancrage n'existe.

**Parametres.** Test bilateral de difference de deux moyennes independantes. Puissance 0,80.
Correction de Holm a l'interieur de chaque famille, seuil au cas le plus defavorable :
**0,0250** pour la famille P (deux tests), **0,0167** pour la famille M (trois tests). Ajustement
de covariable de depart par le facteur `sqrt(1 - r^2)`, avec **r = 0,45** en hypothese de travail,
valeur volontairement basse puisque la covariable est la mesure avant portant sur **l'autre
moitie** des items et non sur les memes.

| d | famille | r | n par bras, plan equilibre | cinq bras equilibres, pour memoire | recrutes a +15 pour cent |
|---|---|---|---|---|---|
| 0,22 | M, alpha 0,0167 | 0,00 | 433 | 2 163 | 2 487 |
| 0,22 | M, alpha 0,0167 | 0,30 | 394 | 1 968 | 2 264 |
| **0,22** | **M, alpha 0,0167** | **0,45** | **345** | **1 725** | **1 984** |
| 0,22 | M, alpha 0,0167 | 0,60 | 277 | 1 384 | 1 592 |
| 0,22 | P, alpha 0,0250 | 0,45 | 313 | 1 566 | 1 801 |
| 0,20 | M, alpha 0,0167 | 0,60 | 335 | 1 675 | 1 926 |
| 0,25 | M, alpha 0,0167 | 0,60 | 214 | 1 072 | 1 233 |

[MESURE, `p1-puissance.py` section 1 et section 4]

**La ligne retenue est la troisieme**, 345 par bras en plan equilibre, transposee en allocation
inegale a six bras selon q13 : **250 par bras traite, 558 au temoin, 1 806 analyses,
2 080 recrutes**. Elle tient dans la fourchette de 1 500 a 2 000 personnes de `MOONSHOTS.md`, en
lisant cette fourchette comme un nombre d'analyses. Le taux de perte de 15 pour cent est justifie
en q22.

**Le bras F est amplement dote.** A d = 0,30, un plan equilibre demande 186 par bras ; a d = 0,34,
144 [MESURE, `p1-puissance.py`]. Les 250 du bras F couvrent l'effet de taux de base d'Ahler et
Sood avec une marge de moitie.

**Effet minimal detectable, a taille fixee**, ce qui est la lecture honnete a donner au partenaire
qui financera :

| total analyse | plan | r | EMD en d | equivalent en points de thermometre, ecart type 25 |
|---|---|---|---|---|
| **1 806** | **250 par bras traite et 558 au temoin, six bras** | **0,45** | **0,220** | **5,5** |
| 1 500 | 250 par bras traite et 500 au temoin, cinq bras | 0,45 | 0,224 | 5,6 |
| 2 070 | 345, six bras equilibres | 0,45 | 0,220 | 5,5 |
| 2 400 | 400 par bras traite et 400 au temoin, six bras | 0,45 | 0,204 | 5,1 |

Toutes les lignes sont au seuil de Holm le plus defavorable, 0,0167, qui est celui des deux
familles confirmatoires.

[MESURE, `p1-puissance.py` section 2]

**Le cout de l'indexation par identite du demandeur, chiffre.** Ajouter la seconde identite de R1
porte les bras modele de trois a six et le plan de six a neuf bras. A la meme precision de
contraste, l'allocation optimale a huit traitements donne **233 par bras traite et 660 au temoin,
soit 2 528 analyses et 2 908 recrutes**, c'est a dire **40 pour cent de budget en plus**
[MESURE, `p1-puissance.py` section 5]. C'est pourquoi
l'extension E1 est declaree et non financee ici. Si le budget est fixe et qu'il faut choisir, le
bras a sacrifier est **D, gpt-oss-20b**, dont le facteur R1 (0,618) est intermediaire : les deux
extremes, 0,245 et 1,268, portent seuls le contraste de H4, et le milieu ne fait que le rendre
plus joli.

**Ce que cette taille ne permet pas, et qu'il faut dire au partenaire avant et non apres.** Elle
ne permet pas de detecter l'effet de deux points de thermometre de l'experience de rerangement,
d = 0,08, qui exigerait environ 2 600 participants par bras. Elle ne permet pas d'estimer avec
precision la variation de l'effet selon la croyance de depart : Ahler et Sood ecrivent eux memes
« we lack the power to estimate variation in treatment effects by prior beliefs about partisan
composition with precision » avec des effectifs du meme ordre [CONFIRME]. Cette moderation est
donc declaree secondaire et exploratoire, jamais confirmatoire.

## q15. Regle d'arret

**Aucune analyse intermediaire. Aucun arret optionnel.** La collecte s'arrete au premier des deux
evenements : 2 080 questionnaires complets, ou quatorze jours calendaires apres l'ouverture. Si
2 080 n'est pas atteint en quatorze jours, l'analyse est faite sur l'effectif obtenu et la
puissance reelle est recalculee et publiee. Aucune donnee n'est regardee, pas meme descriptive,
avant la fermeture. La regle est ecrite avant, comme
`PROTOCOLES-DE-RECHERCHE.md` section 2.8 l'exige.

---

# Page 4. Variables

## q16. Variables manipulees

Une seule : **le texte lu**, six modalites, decrites en q8.

### Comment les textes sont produits, et le controle qui conditionne tout

**Bras C, D, E.** Un run de generation `P1-G`, passe **avant le depot**, reprend l'invite `r1-d1`
de R1 dans une **variante en prose** : meme consigne systeme, meme identite de demandeur
(journaliste neutre, l'identite la moins chargee des deux de R1), temperature 0, `top_k` 1,
gabarit de conversation propre a chaque famille, meme fichier de poids et meme quantification que
R1 [CONFIRME, r1 section « Protocole rappele »]. Registre de version depose : nom du fichier,
quantification, hachage SHA-256, date, parametres du serveur.

**Le controle qui conditionne tout.** R1 lit des pourcentages ecrits en clair ; l'experience fait
lire de la prose. Rien ne garantit qu'un modele mette en prose la distribution qu'il ecrit en
chiffres. Donc : pour chaque texte, la distribution impliquee par la prose est extraite par deux
codeurs independants, aveugles au bras et au modele, et comparee a la cellule R1 correspondante.
**Critere : distance de variation totale inferieure a 0,05 entre la distribution de la prose et
celle de R1, sur chaque item retenu.** Un item qui echoue est remplace par l'item suivant de la
liste de reserve, fixee d'avance. Si plus de trois items sur seize echouent pour un modele, ce
modele **ne porte pas** la quantite mesuree en R1, son bras est retire du protocole et le fait est
publie : ce serait un resultat sur la relation entre les deux modes de lecture d'un modele, pas un
echec de l'experience.

**Bras B.** Meme mise en page, meme longueur a 10 pour cent pres, meme nombre de chiffres, texte
produit par un gabarit rempli avec les valeurs reelles. Le choix de la base de realite est fige
ici et repond a la question ouverte 2 de `a46` : **pour le bloc composition, la base principale
est l'estimation contemporaine la plus recente disponible chez le partenaire, et a defaut la
composition par camp du jeu de Stanford recalculee sur les effectifs de camp, `a46-composition-gss-2024.csv`, l'ANES 2012 d'Ahler et Sood etant publiee a cote comme seconde
colonne et jamais substituee** ; pour le bloc opinion, la base est `a30`, les distributions par
camp du GSS employees par R1. La raison est simple : le bras B doit dire la verite sur la
population dont on interroge les camps, et c'est celle la.

**Bras F.** Meme mise en page, meme longueur, meme nombre de chiffres, mais les chiffres sont les
parts de chaque groupe **dans la population americaine adulte**, jamais dans un camp. La source de
chaque part est nommee dans le texte. C'est la transposition litterale de la condition Base Rates
d'Ahler et Sood [CONFIRME, annexe OA 2.2, figure OA 2.1 panneau c].

**Bras A.** Texte non politique, longueur appariee, sans chiffre de composition, sur un sujet sans
valence partisane. Sa fonction est d'egaliser le temps passe et l'effort de lecture, que le temoin
sans lecture d'Ahler et Sood n'egalise pas.

## q17. Variables mesurees

### Bloc composition, ancrage parti, huit couples groupe et parti, au mot pres d'Ahler et Sood

`dem_black`, `dem_union`, `dem_aa`, `dem_lgb`, `rep_evang`, `rep_rich`, `rep_old`, `rep_south`.
Formulation : le repondant tape son estimation, obligatoirement entre 0 et 100, dans une case a
cote de chaque groupe ; ordre des groupes et ordre des deux batteries randomises [CONFIRME, texte
du papier, section « People Overestimate the Share of Party-Stereotypical Groups »]. Les valeurs
de reference humaines pour la comparaison sont dans `resultats/a46-ahler-sood-items.csv`, verifiees
au millionieme contre les fichiers des auteurs [MESURE].

### Bloc opinion, ancrage ideologie, huit items du GSS

Regle de selection, **fixee avant toute generation de texte et aveugle a l'erreur des modeles** :
parmi les 79 items orientes de `a37`, on retient les items dont la distance de variation totale
entre le camp de gauche et le camp de droite dans la realite vaut au moins 0,10, on exclut les
cinq items concernes par les cellules rejetees de R1 [MESURE, r1 section 4.1], puis on prend les
quatre premiers par ordre alphabetique du nom de variable parmi les items a deux modalites et les
quatre premiers parmi les items a trois ou quatre modalites. La stratification par nombre de
modalites est necessaire parce que l'erreur des modeles croit avec ce nombre, correlation de rang
de +0,40 a +0,58 selon le modele [MESURE, r1 section 3.2], et qu'un tirage libre chargerait
l'experience sur les items ou le modele est le plus faux pour une raison structurelle et non
politique. La liste des seize items et sa liste de reserve sont deposees avec le protocole.

Formulation de second ordre : « Sur 100 Americains qui se disent [de gauche / de droite], combien
selon vous repondent [modalite] a la question suivante ? », suivie du libelle GSS au mot pres.

### Mesures de sortie reprises d'Ahler et Sood, au mot pres

**Extremite percue.** Les quatre echelles semantiques de politique publique, impots, avortement,
droits des homosexuels, politique raciale, avec leurs cinq ou six modalites et leurs bornes
volontairement hors du courant dominant. Formulation exacte disponible : « Which of the following
statements do you think comes closest to what the average Republican Party supporter believes
about taxes? », sous question « How about the average Democratic Party supporter? », modalite
extreme cote gauche « To address inequality, establish a national maximum income by taxing all
income over a certain amount at 100 % » [CONFIRME, annexe OA 4.5 du papier].

**Animosite.** Thermometre de sentiment envers le camp adverse, 101 points, recode a l'envers et
ramene sur 0 a 1 [CONFIRME]. Indice de distance sociale de Bogardus, quatre situations, moyenne
des quatre, alpha de Cronbach 0,71 chez les auteurs [CONFIRME].

**Placebo.** Les memes mesures sur le **camp du participant**, jamais corrige dans aucun bras. Chez
Ahler et Sood, l'ecart tell contre temoin sur l'extremite du camp propre vaut 0,01, IC
[-0,03 ; 0,04], et sur le thermometre du camp propre l'intervalle est [-0,04 ; 0,03] [CONFIRME].
C'est le controle de demande experimentale le plus economique du dispositif.

**Verification de manipulation et conformite.** Les items de composition sont redemandes en fin
de questionnaire dans le bras B, comme chez Ahler et Sood. Est declare conforme le participant
qui donne au moins une des quatre estimations a moins de cinq points de la verite ; chez eux
**74,2 pour cent** l'etaient, et cette definition liberale rend un effet de conformite
conservateur [CONFIRME]. L'effet moyen causal sur les conformes est estime par assignation
comme instrument.

**Sonde de suspicion et de nouveaute.** Le participant declare s'il pense que le texte etait
produit par une machine, s'il l'a trouve credible, et si l'information lui semblait nouvelle.

### Covariables preenregistrees

Force de l'identification partisane, score du bloc de connaissance politique, education, age,
sexe, region, temps passe sur la page du texte, et la mesure avant de la moitie d'items non
utilisee dans la sortie.

## q18. Indices

- **`MAE_out`**, mesure principale du bloc composition et du bloc opinion, separement : moyenne
  sur les items de `|estimation - verite|`, en points de pourcentage. C'est la quantite « en
  points » d'Ahler et Sood, bornee et lisible.
- **`ERR_rel`**, quantite secondaire : moyenne sur les items de `(estimation - verite) / verite`,
  la quantite non bornee du code de replication des auteurs, lignes 160 a 172 du fichier `.do`
  [CONFIRME], celle qui rend le resultat spectaculaire sur les groupes rares. **Les deux
  quantites sont publiees ensemble et jamais l'une a la place de l'autre**, parce qu'elles ne
  disent pas la meme chose : `a46` le releve deja.
- **`HOM_out`**, homogeneite percue du camp adverse : sur les items d'opinion a modalites
  ordonnees, la dispersion implicite de la distribution que le participant attribue au camp,
  mesuree par l'indice de Gini et Simpson a biais corrige, la meme fonctionnelle que `a1` et
  `a44` emploient. C'est la mesure de H3.
- **`GAP_out`**, ecart percu entre camps : distance de variation totale entre la distribution
  attribuee au camp de gauche et celle attribuee au camp de droite, moyennee sur les items. C'est
  la mesure de H4, et c'est la transposition humaine exacte du facteur H2b de R1.
- **`EXT_out`**, part de placements du sympathisant typique du camp adverse a l'extremite,
  moyennee sur les quatre echelles. Mesure principale d'Ahler et Sood.
- **`AFF_out`**, thermometre recode a l'envers sur 0 a 1 ; **`SOC_out`**, indice de distance
  sociale.

---

# Page 5. Analysis Plan

## q19. Modeles statistiques

**Comparaison principale, pour chaque mesure et chaque bras contre le temoin** : moindres carres
ordinaires de la mesure apres sur des indicatrices de bras, avec les covariables preenregistrees
de q17, sans interaction. Pour les mesures calculees au niveau de l'item, `MAE_out`, `ERR_rel`,
`HOM_out`, `GAP_out`, `EXT_out`, l'unite d'analyse est le couple participant et item, avec
**effets fixes d'item** et **erreurs types groupees par participant**, exactement le traitement
d'Ahler et Sood sur leur mesure d'extremite [CONFIRME, « we stacked the data so that the unit of
analysis is respondent-policy-question. To account for correlation of errors within respondents,
we clustered the standard errors by respondent »].

**H4, ordonnancement** : contraste lineaire preenregistre sur les trois bras modele avec les
poids donnes par les facteurs R1 centres, `(0,245 ; 0,618 ; 1,268)`, plus la correlation de rang
de Spearman entre l'ordre des trois moyennes de bras et l'ordre des trois facteurs. Le contraste
lineaire porte le verdict ; le rho est publie a cote.

**Familles et correction.** Trois familles arretees ici et jamais elargies apres coup :
**P** (H1, H2, H6), trois tests, Holm ; **M** (H3, H4, H5), trois tests, Holm ; **S** (H7, H8 et
tout le reste), Benjamini et Hochberg a 0,05, etiquetee secondaire. H6 rejoint la famille P et non
la famille M parce que le bras F ne porte aucune information par camp : ce n'est pas un test sur
la representation des camps, c'est un test sur l'ancrage numerique, du meme genre que la
validation d'instrument. Le seuil de Holm au cas le plus defavorable devient donc **0,0167 dans
les deux familles**, ce qui ne change aucune taille, la table de q14 etant deja calculee a ce
seuil. Un test qui n'est pas dans cette liste est un test exploratoire, rendu sans valeur p, comme
`PROTOCOLES-DE-RECHERCHE.md` section 4 point 6 l'exige.

**Grille multivers publiee entiere**, non pas la ligne la plus favorable, selon la section 2.5 du
meme document. Les axes de la grille sont fixes ici : avec et sans les exclusions de q22 ; `MAE`
et `ERR_rel` ; ancrage parti et ancrage ideologie la ou les deux existent ; base de realite
contemporaine et base ANES 2012 pour le bloc composition ; items pre mesures et items non pre
mesures. Cela fait 32 lignes par mesure, toutes publiees, la ligne principale designee ici.

## q20. Transformations

Le thermometre est recode a l'envers et ramene sur 0 a 1, comme chez les auteurs. Les estimations
de composition sont bornees a l'intervalle 0 a 100 par construction du champ de saisie. Aucune
winsorisation, aucune transformation logarithmique sur les mesures principales. `ERR_rel` n'est
pas transformee et son intervalle est obtenu par bootstrap sur les participants, 2 000 tirages,
parce que sa distribution est fortement asymetrique.

## q21. Criteres d'inference

Tests bilateraux, seuil nominal 0,05 par famille, corrige par Holm a l'interieur de la famille.
Les intervalles publies sont a 95 pour cent, obtenus par bootstrap sur les participants,
2 000 tirages, pour toute quantite qui n'est pas une moyenne simple. Les hypotheses dirigees sont
comptees tenues ou fausses selon un tableau de score publie avec les resultats, sur le modele des
six predictions de `c1` section 9.

**Ce qui est declare d'avance comme non concluant.** Un intervalle qui contient zero et dont les
bornes sont a l'interieur de plus ou moins 0,10 d est declare **nul en pratique** ; un intervalle
qui contient zero et dont une borne depasse 0,20 d est declare **non concluant**, pas nul. Cette
distinction est faite avant, parce que r1 a montre qu'on la reclame apres.

## q22. Exclusion de donnees

Regles arretees ici, toutes appliquees avant l'ouverture de la table de correspondance des bras :

1. echec aux deux controles d'attention places dans le bloc de couverture ;
2. duree totale inferieure a 40 pour cent de la mediane du pilote ;
3. duree sur la page du texte inferieure a 30 pour cent du temps de lecture attendu au debit de
   200 mots par minute, ce qui atteste que le traitement n'a pas ete recu ;
4. valeur identique sur les huit items de la batterie de composition ;
5. identifiant en double, ou participant present dans la liste d'exclusion du projet.

Taux de perte attendu : **10 a 15 pour cent**, d'ou le recrutement de 2 080 pour 1 806 analyses.
L'analyse principale est faite **avec** ces exclusions ; la meme analyse **sans aucune exclusion**
est publiee dans la grille multivers, systematiquement.

## q23. Donnees manquantes

Le questionnaire force la reponse sur les items principaux, donc les manquantes ne peuvent venir
que d'un abandon. Un abandon avant la lecture du texte est retire ; un abandon apres est conserve
et analyse en intention de traiter sur les mesures qu'il porte, la mesure manquante restant
manquante, sans imputation. Le taux d'abandon par bras est publie, et un ecart de plus de cinq
points entre deux bras est declare comme un risque d'attrition differentielle et discute.

## q24. Analyses exploratoires

Rendues a part, sous le titre exploration, sans valeur p : moderation par la croyance de depart ;
moderation par la force partisane ; effet de la sonde de suspicion ; comportement item par item ;
lien entre l'ampleur de l'effet sur un item et l'`alpha` de retrecissement de ce modele sur cet
item, mesure en R1 section 3.3 ; et l'effet **ask** estime dans le bras temoin par la comparaison
des items pre mesures et non pre mesures, qui est la seule exploration dont le protocole annonce
d'avance qu'il aimerait qu'elle devienne confirmatoire dans une seconde etude.

---

# Page 6. Other

## q25a. Budget, par plateforme, avec ses sources

**Prolific.** Recompense recommandee **9,00 livres sterling ou 12,00 dollars par heure**, minimum
absolu autorise **6,00 livres ou 8,00 dollars par heure** ; frais de plateforme **33,3 pour cent
des recompenses pour un compte academique ou a but non lucratif**, **42,8 pour cent pour un compte
commercial** [CONFIRME, https://www.prolific.com/pricing et
https://researcher-help.prolific.com/en/article/9cd998, consultes le 9 septembre 2026].

Duree estimee du questionnaire : **20 minutes**, estimation a valider sur le pilote, qui la
corrigera dans un sens ou dans l'autre.

| poste | effectif | duree | taux | frais | recompenses | frais | **total** |
|---|---|---|---|---|---|---|---|
| pilote | 150 | 20 min | 9,00 GBP/h | academique | 450,00 | 149,85 | **599,85 GBP** |
| etude principale | 2 080 | 20 min | 9,00 GBP/h | academique | 6 240,00 | 2 077,92 | **8 317,92 GBP** |
| **ensemble** | 2 230 | 20 min | 9,00 GBP/h | academique | 6 690,00 | 2 227,77 | **8 917,77 GBP** |
| ensemble, compte commercial | 2 230 | 20 min | 9,00 GBP/h | commercial | 6 690,00 | 2 863,32 | **9 553,32 GBP** |
| ensemble, questionnaire ramene a 15 min | 2 230 | 15 min | 9,00 GBP/h | academique | 5 017,50 | 1 670,83 | **6 688,33 GBP** |
| ensemble, au minimum autorise, a ne pas faire | 2 230 | 20 min | 6,00 GBP/h | academique | 4 460,00 | 1 485,18 | **5 945,18 GBP** |
| extension E1, neuf bras, pour memoire | 3 060 | 20 min | 9,00 GBP/h | academique | 9 180,00 | 3 056,94 | **12 236,94 GBP** |

[MESURE, arithmetique sur les taux confirmes ci dessus]

La derniere ligne est ecrite pour etre refusee : payer 6,00 livres de l'heure est autorise par la
plateforme et deconseille par elle, et un comite d'ethique le lira comme tel.

**Conversion en euros.** Le taux de change du jour n'a pas ete verifie dans cette session. A un
taux de 1,15 euro pour une livre, l'ensemble academique vaut environ **10 250 euros** [HYPOTHESE,
taux non verifie].

**CloudResearch.** Aucun tarif public. Les pages Connect, MTurk Toolkit et Prime Panels renvoient
a des calculateurs interactifs et a une demande de devis, et n'affichent ni frais par participant
ni minimum de remuneration ; la seule information chiffree publiee est la gratuite des frais
pendant dix jours pour un compte academique nouveau sur Connect [CONFIRME comme absence,
https://www.cloudresearch.com/pricing/ et https://www.cloudresearch.com/products/prime-panels/,
consultes le 9 septembre 2026]. **Le budget CloudResearch ne peut donc pas etre chiffre ici**, et
c'est une des trois choses a demander au partenaire.

**Panel probabiliste.** Les 15 000 a 30 000 euros de `MOONSHOTS.md` correspondent a un panel
probabiliste de type AmeriSpeak ou YouGov, pas a Prolific. Aucun tarif public n'a ete verifie
pour ces fournisseurs [HYPOTHESE]. La difference est un choix de fond et pas de commodite : Ahler
et Sood ont fait leur etude descriptive sur YouGov, **echantillon apparie avec poids**, et leurs
quatre experiences sur **MTurk**, en argumentant explicitement la generalisation [CONFIRME,
note 9 du papier : perceptions MTurk proches des perceptions YouGov, effets de traitement ne
variant ni par education ni par partisanerie, annexes OA 2.5 et OA 2.6]. **Ce protocole suit leur
choix** : experience sur panel en ligne, avec la meme defense, et une extension sur panel
probabiliste si le partenaire l'apporte.

**Autres postes.** Plateforme d'enquete, Qualtrics ou LimeSurvey, de zero a 500 euros selon la
licence du partenaire. Double codage des textes, deux fois quatre heures. Frais de comite
d'ethique, de zero a quelques centaines d'euros selon l'etablissement. **Le calcul de machine est
nul** : les textes des bras modele tournent sur la machine locale, moins d'une heure au debit
mesure en R1.

**Total a inscrire dans une demande** : **10 000 a 12 000 euros** pour la version Prolific
complete, pilote compris, hors salaire. C'est **la moitie basse** de la fourchette de
`MOONSHOTS.md`, et l'ecart s'explique entierement par le type de panel.

## q25b. Duree

| etape | duree |
|---|---|
| generation et gel des textes, double codage, controle de prose contre R1 | 1 semaine |
| depot du protocole sur OSF et passage en comite | 4 a 8 semaines, hors de notre controle |
| pilote de 150 personnes, correction de la duree et des consignes | 1 semaine |
| collecte principale | 3 a 14 jours |
| analyse, script gele avant l'ouverture des etiquettes de bras | 1 semaine |
| ecriture | 2 semaines |

**Le chemin critique est le comite, pas la collecte.** La collecte tient dans une semaine.

## q25c. Ethique

**Consentement.** Formulaire preliminaire indiquant la duree, la remuneration, le caractere
politique des questions, le droit de retrait a tout moment sans justification et sans perte de
remuneration pour la part effectuee, et l'absence de collecte de donnee directement identifiante.

**Absence de tromperie sur la source.** Decision 2 ci dessus : les participants des bras C, D et
E sont informes que le texte est la reponse d'un assistant conversationnel. Il n'y a donc pas de
tromperie sur l'origine du materiel. Il reste une **omission**, l'objet de l'etude, qui est
standard et couverte par le debriefing.

**Le point ethique reel, et sa reponse.** Les textes des bras modele sont **mesurablement faux** :
sur les 149 items, l'erreur des trois modeles vaut de **0,199 a 0,306** de distance de variation
totale contre la realite, soit **sept a onze fois** le bruit de reinterrogation d'un panel humain
[MESURE, r1 section 3.1]. Exposer des gens a une information fausse sur un groupe social exige
une reparation, et elle est integrale :

1. **Tout participant, dans les six bras sans exception**, recoit en fin de questionnaire un
   tableau des vraies valeurs sur les seize items, avec la source de chaque valeur.
2. **Les participants des bras C, D et E** recoivent en plus, item par item, l'ecart entre ce que
   le texte disait et la realite, dans la forme meme qu'Ahler et Sood emploient dans leur
   condition **tell** : « The percentage of Democrats (Republicans) who are g is smaller than you
   think. Only x % are g. » [CONFIRME, annexe OA 4.2 du papier].
3. Le debriefing dit explicitement que le texte lu venait d'un modele de langage, qu'il n'a pas
   ete choisi pour etre faux, qu'il est la sortie brute d'un protocole reproductible, et il donne
   l'adresse du preenregistrement et du jeu de donnees a venir.
4. Une adresse de contact est fournie, et le participant peut demander le retrait de ses reponses
   pendant trente jours.

**Comite.** Un passage en comite est requis avant toute collecte, et il n'est pas negociable. Deux
voies selon le partenaire : un comite d'ethique de la recherche d'universite francaise, ou un
*institutional review board* americain. Precedent utile a citer dans la demande : les etudes
d'Ahler et Sood ont ete « deemed exempt by Stanford University and the University of California,
Berkeley », et menees « in compliance with relevant laws and the ethical standards contained in
the 1964 Declaration of Helsinki and its later amendments » [CONFIRME, note de bas de page 1 du
papier].

**Donnees personnelles.** Les opinions politiques sont une categorie particuliere de donnees au
sens de l'article 9 du reglement general sur la protection des donnees. La base legale, la
minimisation, la duree de conservation et l'analyse d'impact doivent etre nommees dans le dossier
de comite. Les identifiants de plateforme sont pseudonymes, conserves separement de la table
d'analyse, detruits a la publication, et jamais joints a quoi que ce soit d'autre.

## q25d. Risques, et ce qui les couvre

| risque | pourquoi il est reel ici | ce qui le couvre |
|---|---|---|
| **demande experimentale** | le participant devine que l'etude porte sur la polarisation et repond au sens du dispositif | couverture en enquete de connaissance politique, exactement comme Ahler et Sood ; **placebo sur le camp propre**, dont l'effet doit rester dans [-0,04 ; 0,04] comme chez eux ; sonde de suspicion analysee |
| **effet de plafond, et effet de plancher** | les estimations humaines sont deja tres hautes, de 28 a 43 pour cent sur les huit dyades [MESURE, a46] ; un bras qui pousse vers le haut a peu de place | H5 est dirigee vers le haut sur les **modalites rares**, ou la place est maximale ; diagnostic de plafond publie par item, part des reponses a 0 et a 100 ; `ERR_rel`, non bornee, publiee a cote de `MAE` |
| **contamination entre bras** | les participants de Prolific echangent sur des forums | plan entre sujets, seance unique, collecte courte, liste d'exclusion, question finale sur la connaissance prealable de l'etude, analyse de sensibilite sans les participants qui declarent en avoir entendu parler |
| **contamination de la mesure avant** | demander des nombres depolarise deja, effet **ask** d'Ahler et Sood, moitie de l'effet de la correction | mesure avant sur une moitie d'items tiree au hasard, mesure principale sur les items non pre mesures |
| **perissabilite par version** | la quantite est propre a un modele et a une version | textes geles, hachages deposes, registre de version, protocole rejouable ; c'est ce qu'une norme est, pas une objection |
| **la prose ne porte pas la distribution des chiffres** | R1 lit des pourcentages, l'experience fait lire de la prose | controle de prose contre R1 a 0,05 de distance de variation totale, liste de reserve, retrait du bras si plus de trois items sur seize echouent |
| **le modele est une archive fidele** | objection fatale du programme A | affaiblie et non levee par R1 : trois archives seraient d'accord entre elles et ne le sont pas, et l'erreur vaut sept a onze fois le plancher humain ; **elle ne concerne pas ce protocole**, qui mesure un effet de lecture et non l'exactitude du modele |

## q25e. Ce qui ferait tomber l'idee

Ces criteres sont ecrits avant, et ils commandent sans debat.

1. **La verification de manipulation echoue.** Si le bras B ne reduit pas l'erreur absolue moyenne
   d'au moins **10 points**, la ou Ahler et Sood en obtiennent 21,6, l'instrument ne fonctionne
   pas dans notre echantillon et **rien n'est conclu des bras modele**. Le rapport publie l'echec
   de reproduction et s'arrete la.
2. **Le placebo bouge.** Si l'ecart entre un bras et le temoin sur les mesures du **camp propre**
   sort de l'intervalle [-0,04 ; 0,04] qu'Ahler et Sood observent, la demande experimentale n'est
   pas maitrisee et les mesures principales ne sont pas interpretables.
3. **La prose ne porte pas les chiffres.** Plus de trois items sur seize hors du seuil de 0,05
   pour un modele : ce bras sort.
4. **Les trois bras modele ne se distinguent ni du temoin ni entre eux**, avec des intervalles
   entierement contenus dans plus ou moins 0,10 d. Alors l'etage causal du programme A est nul, et
   **la norme d'audit se publie sans volet causal**, ce que `MOONSHOTS.md` prevoit deja comme
   point d'arret du mois 6. Ce n'est pas un echec de l'idee : c'est l'issue rassurante, et elle
   vaut d'etre publiee parce que personne ne l'a mesuree.
5. **H4 tombe et H3 tombe ensemble.** Si l'ordonnancement des trois bras ne suit pas les facteurs
   R1 **et** si l'homogeneite percue ne bouge pas, alors les quantites d'audit de R1 ne predisent
   rien de ce que la lecture fait a un lecteur. La norme reste une norme de description, et il
   faut ecrire noir sur blanc que sa valeur causale n'est pas etablie.
6. **Ce qui ne fait pas tomber l'idee, et qu'il ne faut pas confondre.** Un effet nul sur
   l'affect, thermometre et distance sociale, ne fait rien tomber : l'ancrage le plus recent, deux
   points de thermometre sur 1 256 personnes en dix jours, dit que cette mesure est hors de portee
   d'une seance unique a cette taille. L'affect est secondaire ici, et il est declare tel avant.

## q25f. Extensions declarees, non financees dans ce protocole

**E1, l'identite du demandeur.** R1 mesure que le portrait qu'un modele fait d'un camp depend de
qui demande, de **2,74 a 4,23 fois** le plancher humain, sur les six cellules, au p minimal que
20 000 permutations autorisent : c'est le **seul** resultat ou les trois modeles concordent en
niveau [MESURE, r1 section 1.3]. La version lecture de ce fait, faire lire a un participant la
reponse produite pour un journaliste ou celle produite pour un membre du camp adverse, double le
nombre de bras modele et coute environ 1 000 participants de plus. C'est l'extension a financer
en premier si le budget monte.

**E2, texte non etiquete.** Meme plan sans dire que le texte vient d'une machine. Mesure l'effet
du texte nu et exige un traitement de la tromperie en comite.

**E3, seconde langue et second pays.** Barometre CEVIPOF, dix-sept vagues, CC BY 4.0, deja
identifie dans `exploration/05`. La fausse polarisation n'est pas une propriete americaine, et le
protocole est transposable ; les items d'Ahler et Sood ne le sont pas tels quels.

**E4, l'IGS Poll.** Ahler et Sood detiennent le seul jeu connu portant une croyance humaine de
second ordre sur des **opinions** avec le referent de la meme enquete, et le fichier
`pcomp_igspoll.dta` **manque de l'archive Dataverse** [CONFIRME, `readme.txt` de l'archive contre
son contenu]. **Fait nouveau de cette session** : les **vingt-cinq enonces de politique publique**
de cette enquete sont imprimes en clair dans l'annexe OA 3.2.1 du papier [CONFIRME,
http://gsood.com/research/papers/partisanComposition.pdf]. Les libelles sont donc recuperables
sans le fichier, ce qui rend l'extension realisable meme si Gaurav Sood ne repond pas ; ce qui
manque alors est la **distribution reelle** des camps sur ces enonces, qu'une vague de calibrage
de mille personnes produirait pour environ 1 400 livres sterling au tarif ci dessus.

---

## Rejouer le calcul de puissance

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python protocoles/p1-puissance.py
```

Aucune donnee n'est lue. La sortie contient les quatre sections citees en q14.

## Fichiers a deposer avec ce protocole

| fichier | contenu |
|---|---|
| `protocoles/01-experience-de-lecture.md` | ce document |
| `protocoles/p1-puissance.py` | le calcul de puissance, sans donnees |
| la liste des seize items et sa liste de reserve | a produire par la regle de q17, avant la generation |
| les cinq textes par item et par camp, avec leurs hachages | run `P1-G`, a passer avant le depot |
| le registre des versions de modeles | nom de fichier, quantification, hachage, date, parametres |
| la table de correspondance scellee des bras A a E | ouverte apres le gel du script d'analyse |
