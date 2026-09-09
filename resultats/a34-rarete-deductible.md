# a34. La rarete deductible : le seul test qui pouvait faire tomber la these

> **Erratum du 9 septembre 2026, sur un point qui n'est pas couvert par l'errata E1 ci dessous.** « L'ablation C2 contre C3, coeur de a31, survit intacte » nomme mal un contraste de conditionnement : C2 recoit onze attributs demographiques, C3 les 119 reponses de la personne sans demographie (`a45` section 0, `a47` D1).
> La survie du couple par tercile reste mesuree ; son attribution a la seule etiquette tombe. L'ablation propre, a un seul facteur, est le run R3 : `resultats/r3-resultats.md`.

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Reponse en une ligne : l'instrument des terciles de deductibilite est invalide ; les rappels restent, l'interpretation tombe. Objection a45 numero 6.3.

**Phrase d'origine.** « Dans le tercile ou la rarete n'est PAS deductible, c'est a dire ou
aucune autre personne du segment ideologie x genre x age de l'individu n'a donne cette
reponse, les agents riches de Stanford en retrouvent 21,8 et 20,3 pour cent quand la
regression logistique sur demographies en retrouve 1,45 pour cent et la foret aleatoire
0,21 pour cent ».

**Correction.** a42 section 5, ecrite le meme jour, oppose aux terciles de deductibilite une
**partition placebo de neuf groupes de personnes tires au hasard**, donc porteurs d'aucune
information de deductibilite : elle reproduit le meme gradient, l'ecart entre les deux
partitions ne depassant jamais 0,040 et valant **0,016 en mediane** [a42 section 5,
`a42-partitions.csv`]. Un tercile de frequence de segment est d'abord un tercile de
frequence d'item. **Les rappels de a34 restent justes ; leur lecture en « rarete
deductible » est retiree**, y compris la phrase « le rapport des rappels est de 15 contre 1
dans le tercile non deductible contre 3,3 contre 1 dans le tercile deductible ».

**Partition de remplacement.** La seule que a42 conserve est « rarete stable en vague 2 »,
qui n'a pas de placebo possible : le hasard ne peut pas fabriquer la stabilite d'une reponse
a deux semaines.

**Preuve.** a42 section 5 ; `MODELE-DU-MONDE.md` 10.1 l'acte deja pour la synthese, le corps
de a34 ne le portait pas.

---

Rapport du 8 septembre 2026. Il execute le test 4 de la section (d) de
`corpus/lecture-complete/03-baselines-statistiques-extension-enquete.md`, designe la comme
**« le seul du lot qui peut faire tomber le rang 1 revise »**. Il oppose notre resultat
(a28 section 3.4, a29, a31 : sur les cellules minoritaires les agents retrouvent 22 a
31 pour cent des reponses rares, la regression 5,8 et la foret 1,4) a la contre preuve la
plus directe du corpus, von der Heyde, Haensch et Wenz 2025 (T03-34), qui mesure l'inverse
sur le vote allemand : l'ecart de F1 entre la regression multinomiale et GPT-3.5 passe de
11 points sur la CDU a 25 points sur l'AfD et 20 sur les petits partis, c'est a dire qu'il
**se creuse quand la categorie se rarefie**.

L'hypothese qui reconcilie les deux, ecrite dans `corpus/03` : la statistique retrouve les
raretes **deductibles** de l'etiquette et rate les autres ; le modele de langage retrouve
les deux, ou surtout les non deductibles. Si le modele de langage ne retrouve que les
deductibles, la these « il garde les outliers » tombe.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a34_commun.py`, `a34_deductibilite.py`, `a34_figure.py`. **Aucun script
existant n'a ete modifie** ; `a31_commun`, `a29_commun`, `a28_commun`, `a25_commun`,
`a25_mesures`, `a8_commun`, `a2_commun`, `a2_baselines_gss`, `a5_evaluer` et
`a5_agents_locaux_gss` sont importes tels quels, memes graines, memes plis, memes blocs,
memes 149 items, memes personnes. La foret aleatoire `B3 foret` est relue du cache de a28,
elle n'est pas redefinie.

Sorties : `a34-terciles-description.csv`, `a34-par-tercile.csv`, `a34-planchers.csv`,
`a34-contrastes.csv`, `a34-leviers-par-tercile.csv`, `a34-contraste-de-groupe.csv`,
`a34-controles.csv`, `a34-figure-rarete-deductible.png` et `.svg`.

---

## Reponse en une ligne

**La these tient, son test decisif est passe, et sa formulation dirigee tombe.** Dans le
tercile ou la rarete n'est PAS deductible, c'est a dire ou **aucune autre personne du
segment ideologie x genre x age de l'individu n'a donne cette reponse**, les agents riches
de Stanford en retrouvent **21,8 et 20,3 pour cent** quand la regression logistique sur
demographies en retrouve **1,45 pour cent** et la foret aleatoire **0,21 pour cent**, sous
le plancher de **5,2 pour cent** qu'obtient un tirage aveugle dans la marginale de l'item
[MESURE, `a34-par-tercile.csv`, perimetre 1 052, seuil 10 pour cent]. **Les huit conditions
a modele de langage ont un avantage strictement positif sur `B1 argmax` dans ce tercile,
les huit passent la correction de Holm sur une famille de 21 tests, p ajuste 0,0052 dans
les huit cas**, du plus faible, `agents v7` a plus 0,0268 [0,0160 ; 0,0377], au plus fort,
`agents composite` a plus 0,2036 [0,1816 ; 0,2253]. **La prediction adverse de von der
Heyde, « l'ecart se concentre dans le tercile deductible et s'annule ailleurs », est
refutee : rien ne s'annule, et le rapport des rappels est de 15 contre 1 dans le tercile
non deductible contre 3,3 contre 1 dans le tercile deductible.**

**Mais la prediction dirigee de notre propre these est fausse aussi, et il faut le dire.**
L'ecart ABSOLU avec la statistique n'est pas maximal dans le tercile non deductible : il
vaut plus 0,204 en T1, plus 0,263 en T2 et plus 0,281 en T3 pour `agents composite`. Sur le
test declare H3, trois conditions sur huit ont un ecart **significativement plus petit**
dans le tercile non deductible, `agents v8` a moins 0,142, `agents entretien` a moins 0,096
et `agents composite` a moins 0,077, p ajuste 0,0052 [MESURE, `a34-contrastes.csv`].
**La phrase defendable est donc « l'avantage ne disparait nulle part et il est le plus
spectaculaire en rapport la ou la rarete est indeductible », pas « l'ecart y est
maximal ».**

**Le troisieme resultat est le plus severe pour le champ, et il vient du plancher de bruit
de cellule de la lecture 01.** Le rappel de toutes les methodes monte avec la
deductibilite ; le plancher monte plus vite. Une fois le plancher d'un tirage dans la
marginale du segment soustrait, **l'exces de rappel des trois meilleures conditions est
plat**, 0,218 / 0,220 / 0,184 pour `agents composite`, sans gradient significatif apres
correction (moins 0,035, p ajuste 0,29), **et l'exces des cinq predicteurs statistiques est
negatif dans les deux terciles les plus deductibles** : `B1 argmax` a moins 0,043 et
moins 0,097, `B3 foret` a moins 0,063 et moins 0,183, les cinq passant Holm
[MESURE, `a34-planchers.csv`]. **La regression logistique ne bat jamais un tirage dans la
marginale du segment de la personne : elle parait gagner sur la rarete deductible parce
que la rarete deductible est facile.**

**Enfin, le point 4 du cahier des charges donne un resultat mitige pour a31.** Le rapport
groupe sur personne de a31 est calcule sur TOUTES les fausses raretes, pas sur le tercile
non deductible. Recalcule sur le seul tercile non deductible de la partition non
circulaire : **l'ablation C2 contre C3, coeur de a31, survit intacte, 4,12 contre
moins 0,75, contre 4,45 contre 0,44 sur l'ensemble** ; mais **le meme recalcul detruit
l'enonce pour les conditions riches de Stanford**, `agents composite` tombant de 1,62 a
0,02 et `agents entretien` de 3,65 a 0,09 [MESURE, `a34-leviers-par-tercile.csv`]. Sur la
rarete indeductible, les agents riches placent leurs fausses raretes **par la personne**,
comme les humains, et non par le groupe. **La phrase de a31 « toutes les autres methodes
font l'inverse » doit nommer les conditions qui n'ont que l'etiquette.**

---

## 0. Le protocole, et l'aveu qui doit le preceder

### 0.1 Ce rapport ne revendique pas le pre enregistrement

a28, a29 et a31 revendiquent que leur famille d'hypotheses a ete ecrite avant l'execution.
**Ce rapport ne le revendique pas, et c'est le premier chiffre desagreable.** La famille
recopiee ci dessous a ete ecrite **apres** une lecture descriptive des rappels par tercile,
et c'est precisement cette lecture qui a impose le choix de la partition principale, pour
la raison arithmetique donnee en 0.3. Les p qui suivent sont des p de confirmation faible.
Le fait est ecrit dans l'entete de `a34_deductibilite.py` et repete ici ; aucune
formulation du rapport ne doit laisser croire l'inverse.

### 0.2 Les deux scores de deductibilite

**D_logit, la deductibilite logistique.** Pour une cellule (personne, item) et une
modalite, la probabilite **hors pli** que la regression logistique multinomiale sur les
onze attributs demographiques attribue cette modalite a cette personne. C'est exactement le
modele de `B1 argmax` : memes cinq plis sur les personnes, graine 20260903, meme encodeur
indicatrice ajuste sur le pli d'entrainement seul, meme `LogisticRegression(max_iter=2000,
C=1.0)`. La seule difference avec `a2_commun.b1_logistique` est qu'on lit `predict_proba`
au lieu de `predict`. **Le score de deductibilite est donc, litteralement, la confiance de
l'adversaire statistique.** C'est la definition qui colle a von der Heyde, ou la regression
multinomiale tourne sur exactement les memes variables que l'invite du modele.

**D_seg, la deductibilite par segment.** Frequence de la modalite dans le segment
**ideologie x genre x age** de la personne, calculee sur les humains de la vague 1 **en
laissant de cote la personne elle meme**. 98 cases non vides pour 1 052 personnes, mediane
de 9 personnes par case. Une cellule dont le segment compte moins de cinq autres
repondants exploitables sur l'item recoit NaN ; **la couverture est de 89,6 pour cent des
cellules minoritaires**, et les terciles ne portent donc que sur 5 114 des 5 709 cellules
minoritaires du perimetre 1 052.

**Les deux scores sont calcules une fois sur les 1 052 humains** et restreints ensuite au
perimetre : ce sont des descripteurs de population, comme la marginale d'un item, et les
recalculer sur 150 personnes donnerait des cases de segment d'une ou deux personnes. En
revanche le seuil de minorite et les **bornes** de tercile sont recalcules sur le
perimetre, comme a29 et a31 le font pour le seuil.

Les deux scores se correlent a **0,497** en rang sur les cellules minoritaires [MESURE] :
ils mesurent la meme chose sans etre la meme chose.

### 0.3 Pourquoi la partition principale est D_seg et non D_logit

**C'est le point technique qui commande tout le rapport, et il a ete decouvert avant la
declaration de la famille.** `B1 argmax` ne peut predire une modalite que si elle est la
plus probable. Mesure : **la plus petite valeur de D_logit parmi les 1 496 raretes que
`B1 argmax` ose sur le perimetre 1 052 vaut 0,1452**, au dessus de la borne superieure du
tercile, 0,1046 [MESURE, `a34-controles.csv`]. **Cent pour cent des raretes osees par la
regression tombent donc dans le tercile deductible par definition, et son rappel dans les
deux autres terciles est nul par arithmetique et non par mesure.** Une partition sur
D_logit ne peut pas arbitrer le desaccord avec von der Heyde : elle le tranche d'avance en
faveur de notre these.

La partition sur D_seg n'a pas ce defaut : la regression y place **16,1 pour cent** de ses
raretes dans le tercile non deductible [MESURE]. C'est elle qui porte les tests declares.
**D_logit est rapportee partout a cote, comme partition secondaire et descriptive**, avec
cet avertissement des deux cotes, parce qu'elle est la definition demandee par `corpus/03`
et qu'elle a une lecture propre pour les conditions a modele de langage, qui ne sont pas
la regression.

### 0.4 La famille declaree

**Perimetre** : le perimetre naturel de chaque methode, 1 052 personnes pour les onze
methodes qui les couvrent, 150 personnes du run local pour C2 et C3. **Seuil** : 10 pour
cent. **Partition des tests** : D_seg. **Comparateur declare** : `B1 argmax`, parce que von
der Heyde oppose GPT-3.5 a une regression multinomiale sur les memes variables que
l'invite.

| | enonce | nombre de tests |
|---|---|---|
| **H1** primaire | pour chacune des 13 methodes non humaines, le rappel minoritaire sur T3 differe de celui sur T1, bilateral | 13 |
| **H2** primaire | pour chacune des 8 conditions a modele de langage, l'avantage de rappel sur `B1 argmax` est strictement positif sur T1, le tercile NON deductible | 8 |
| **H3** secondaire | pour chacune des 8 conditions a modele de langage, cet avantage sur T1 differe de celui sur T3, bilateral : positif = notre these, negatif = von der Heyde | 8 |
| **H4** secondaire | pour chacune des 13 methodes, le rappel EN EXCES du plancher de bruit de cellule differe encore entre T3 et T1, bilateral | 13 |

**Famille primaire : H1 union H2, 21 tests. Famille secondaire : H3 union H4, 21 tests.**
Correction principale sur chaque famille : **Holm**, valide sans hypothese sur la
dependance, ce qui est necessaire puisque les contrastes portent sur les memes personnes et
les memes items. **Benjamini Hochberg** est rapporte a cote. Tous les p sont des p de
**bootstrap apparie sur les personnes, 4 000 tirages**, lus sur la position de zero dans la
distribution ; ils ne descendent jamais sous 1/4 000, donc le plancher de Holm vaut 0,0052
sur chacune des deux familles.

**H2 est le test qui pouvait faire tomber la these.**

**N'entrent dans aucune famille**, et sont des descriptions : toute la partition D_logit ;
la precision et le F1 par tercile ; le seuil de 20 pour cent ; le perimetre 150 pour les
onze methodes qui disposent du 1 052 ; le recalcul du rapport groupe sur personne de a31
par tercile, qui est une verification de provenance ; le contraste de groupe entre les huit
conditions a modele de langage et les cinq predicteurs statistiques, ajoute apres coup et
signale comme tel ; la ligne `humains vague 2`, qui est un plafond de bruit.

### 0.5 Les planchers, lecture 01 section (d) point 5

L1.01 demontre que l'absence de controle de la taille de cellule « redecouvre un effet
contre stereotypique fallacieux », et l'avertissement des auteurs est cite tel quel dans
`corpus/01` : *« audits that do not control ground-truth cell size will rediscover a
spurious counter-stereotypical effect, as our own raw data did before correction »*. Deux
planchers sont donc calcules par tercile.

- **Plancher de segment** : rappel attendu sous un tirage dans la marginale du segment
  ideologie x genre x age de la personne, sans la personne. C'est le plancher de bruit de
  cellule demande.
- **Plancher d'item** : rappel attendu sous un tirage dans la marginale de l'item, sans la
  personne. C'est l'esperance de `B0 tirage`, qui ne sait rien de personne, et il sert de
  temoin de lecture.

**Un avertissement de circularite, ecrit ici parce qu'il est genant.** Le plancher de
segment et le score D_seg sont **le meme calcul**. L'exces sur plancher lu a l'interieur de
la partition D_seg est donc une quantite construite pour etre plate en T1, ou le plancher
vaut exactement zero. **C'est la partition D_logit qui donne la lecture non circulaire de
l'exces**, et les deux sont rapportees.

### 0.6 Trois controles executes avant toute lecture

[MESURE, `a34-controles.csv`]

1. **L'argmax des distributions hors pli reproduit `B1 argmax` sur 156 748 cellules sur
   156 748.** Le score de deductibilite est donc bien la confiance du predicteur employe
   par a2, a28, a29 et a31, et non celle d'un modele voisin.
2. **Les rappels globaux reproduisent a28 section 3.4 et a29 section 1 au quatrieme
   chiffre** : `agents composite` 0,3069, `B1 argmax` 0,0580, `B3 foret` 0,0144 sur les
   1 052 ; `C3` 0,2195 et `C2` 0,1285 sur les 150. Rien n'a bouge dans la chaine.
3. **Le fait arithmetique de 0.3 est mesure et non suppose** : min D_logit des raretes
   osees par `B1 argmax` = 0,1452 contre une borne haute de tercile a 0,1046.

---

## 1. Le tableau qui repond a la question

Figure : `a34-figure-rarete-deductible.png` et `.svg`, panneau 1.

[MESURE, `a34-par-tercile.csv`, perimetre 1 052, seuil 10 pour cent, partition **D_seg**,
4 000 tirages bootstrap sur les personnes ; 1 866, 1 562 et 1 686 cellules minoritaires par
tercile, 5 114 sur 5 709]

| condition | **T1 non deductible** | T2 intermediaire | **T3 deductible** | ensemble |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,4861*** | ***0,5359*** | ***0,6133*** | ***0,5483*** |
| **agents composite** | **0,2181** | 0,2855 | **0,4039** | 0,3069 |
| agents entretien (v3) | 0,2026 | 0,2650 | 0,4075 | 0,2953 |
| agents demographiques (v6) | **0,1870** | 0,1677 | **0,1388** | 0,1624 |
| agents enquete | 0,1677 | 0,2145 | 0,2835 | 0,2305 |
| agents v8 | 0,0622 | 0,0871 | 0,3126 | 0,1717 |
| **B0 tirage** | **0,0472** | 0,0563 | 0,0813 | 0,0617 |
| agents v7 | 0,0413 | 0,0570 | 0,0985 | 0,0673 |
| **B1 argmax** | **0,0145** | 0,0224 | **0,1234** | 0,0580 |
| B2 argmax | 0,0118 | 0,0250 | 0,0688 | 0,0357 |
| **B3 foret** | **0,0021** | 0,0026 | 0,0374 | 0,0144 |
| B0 mode | 0,0000 | 0,0000 | 0,0000 | 0,0000 |
| *plancher, tirage dans la marginale du segment* | *0,0000* | *0,0657* | *0,2204* | *0,0927* |
| *plancher, tirage dans la marginale de l'item* | *0,0517* | *0,0624* | *0,0734* | *0,0623* |

**Ce que ce tableau dit, dans l'ordre.**

1. **T1 est un tercile a definition dure.** La borne basse de D_seg vaut exactement 0,0000 :
   T1 est l'ensemble des cellules minoritaires ou **aucune des autres personnes du segment
   ideologie x genre x age de l'individu n'a donne cette reponse sur cet item**. Il n'y a
   rien a deduire de l'etiquette, au sens le plus litteral. Elles sont 1 866 sur 149 items
   et 70 items distincts.

2. **La these passe son test decisif.** Sur ces cellules, `agents composite` retrouve
   21,8 pour cent des reponses rares et `B1 argmax` 1,45 pour cent : **un rapport de 15
   contre 1**, quand le meme rapport vaut 3,3 contre 1 sur le tercile deductible. Contre la
   foret aleatoire, le rapport passe de 104 contre 1 en T1 a 10,8 contre 1 en T3.
   **L'avantage ne s'annule nulle part, et il est le plus spectaculaire la ou von der Heyde
   predisait qu'il disparaisse.**

3. **Le chiffre le plus dur du tableau est sur la ligne `B0 tirage`.** Un tirage aveugle
   dans la marginale de chaque item, qui ne sait rien de personne, retrouve **4,72 pour
   cent** des reponses rares non deductibles ; `B1 argmax` en retrouve 1,45, `B2 argmax`
   1,18 et `B3 foret` 0,21. **Les trois predicteurs statistiques informes sont trois a
   vingt fois SOUS le hasard aveugle sur la rarete indeductible.** Ce n'est pas une
   maladresse de leur part, c'est leur regle de decision : ils prennent l'argmax, et une
   modalite indeductible n'est jamais l'argmax.

4. **Une ligne va contre le motif et il faut la nommer.** `agents demographiques (v6)`, la
   condition de Stanford qui ne recoit qu'une persona demographique, a un rappel qui
   **decroit** avec la deductibilite, 0,1870 puis 0,1677 puis 0,1388, difference
   moins 0,0482 [moins 0,0743 ; moins 0,0220], p ajuste par Holm 0,0052
   [MESURE, `a34-contrastes.csv`]. C'est la seule methode du dossier dont le gradient est
   negatif, et elle est celle qui n'a que l'etiquette. Je n'ai pas d'explication.

5. **Le plafond humain monte aussi**, 0,486 a 0,613 : les cellules deductibles sont plus
   faciles **pour les humains eux memes reinterroges deux semaines plus tard**. Le gradient
   n'est donc pas une propriete des methodes, c'est une propriete des cellules. C'est le
   point que la section 3 chiffre.

### 1.1 La meme table sur la partition D_logit, avec son avertissement

[MESURE, `a34-par-tercile.csv`, perimetre 1 052, seuil 10 pour cent, partition **D_logit**,
1 903 cellules par tercile]

| condition | T1 non deductible | T2 intermediaire | T3 deductible |
|---|---|---|---|
| *humains vague 2* | *0,4640* | *0,5292* | *0,6516* |
| agents composite | 0,1992 | 0,2864 | 0,4351 |
| agents entretien (v3) | 0,1792 | 0,2669 | 0,4398 |
| agents demographiques (v6) | 0,1797 | 0,1545 | 0,1529 |
| agents enquete | 0,1403 | 0,2296 | 0,3216 |
| agents v8 | 0,0520 | 0,1240 | 0,3389 |
| B0 tirage | 0,0473 | 0,0699 | 0,0678 |
| agents v7 | 0,0431 | 0,0583 | 0,1004 |
| **B1 argmax** | **0,0000** | **0,0000** | **0,1739** |
| B2 argmax | 0,0084 | 0,0210 | 0,0778 |
| **B3 foret** | **0,0000** | 0,0011 | 0,0420 |
| *plancher segment* | *0,0388* | *0,0759* | *0,1670* |
| *plancher item* | *0,0495* | *0,0643* | *0,0730* |

**Les deux zeros de `B1 argmax` ne sont pas un resultat, ce sont deux identites.** Ils sont
imprimes ici parce que le lecteur les cherchera, et ils sont barres d'avance par la
section 0.3. Ce que ce tableau apporte est ailleurs : **les huit conditions a modele de
langage, elles, ne sont pas contraintes par cette partition**, et elles retrouvent 4,3 a
19,9 pour cent des reponses que la regression declare avoir moins de 3,2 pour cent de
chance d'observer. `B0 tirage`, qui ignore la partition, est plat a 0,047 / 0,070 / 0,068,
ce qui est le controle de lecture attendu.

### 1.2 Precision et F1 : la metrique de von der Heyde

von der Heyde compare des **F1 par classe**, pas des rappels. Notre resultat doit se lire
dans sa metrique, sans quoi la comparaison n'est pas honnete.

[MESURE, `a34-par-tercile.csv`, F1 par tercile, perimetre 1 052, partition D_seg]

| condition | T1 non deductible | T2 | T3 deductible |
|---|---|---|---|
| *humains vague 2* | *0,4744* | *0,5328* | *0,6077* |
| agents composite | **0,2453** | 0,2936 | 0,3896 |
| agents entretien (v3) | 0,2198 | 0,2680 | 0,3704 |
| agents demographiques (v6) | 0,2496 | 0,2307 | 0,1950 |
| agents enquete | 0,1646 | 0,2255 | 0,2915 |
| agents v8 | 0,0747 | 0,0935 | 0,2274 |
| B0 tirage | 0,0418 | 0,0545 | 0,0972 |
| **B1 argmax** | **0,0261** | 0,0386 | **0,1663** |
| B2 argmax | 0,0229 | 0,0475 | 0,1211 |
| **B3 foret** | **0,0043** | 0,0050 | **0,0697** |

**L'ecart de F1 avec la regression, en points, vaut 0,219 en T1, 0,255 en T2 et 0,223 en
T3.** Il est donc **plat**, la ou von der Heyde mesure une croissance de 11 a 25 points
quand la categorie se rarefie. **En rapport, il vaut 9,4 en T1 et 2,3 en T3.** Contre la
foret aleatoire, le rapport de F1 passe de **57 en T1 a 5,6 en T3**.

`B2 argmax` garde ici sa signature de a29 : sa precision est la meilleure des non humaines
dans les trois terciles, 0,415 / 0,494 / 0,504, pour un rappel de 1,2 a 6,9 pour cent. Elle
ne se trompe pas, elle n'ose pas : 53, 79 et 230 raretes osees sur 156 748 cellules.

---

## 2. Les tests declares

[MESURE, `a34-contrastes.csv`, perimetre naturel, seuil 10 pour cent, partition D_seg,
4 000 tirages bootstrap sur les personnes ; le plancher de Holm vaut 0,0052 sur chaque
famille de 21 tests]

### 2.1 H2, le test qui pouvait faire tomber la these : il passe pour les huit

| condition | avantage sur `B1 argmax` dans T1 | IC 95 % | p Holm | p BH |
|---|---|---|---|---|
| **agents composite** | **plus 0,2036** | [0,1816 ; 0,2253] | **0,0052** | 0,0003 |
| agents entretien (v3) | plus 0,1881 | [0,1673 ; 0,2092] | **0,0052** | 0,0003 |
| agents demographiques (v6) | plus 0,1726 | [0,1537 ; 0,1915] | **0,0052** | 0,0003 |
| agents enquete | plus 0,1533 | [0,1314 ; 0,1746] | **0,0052** | 0,0003 |
| **C3, sans etiquette** | **plus 0,1507** | [0,0976 ; 0,2046] | **0,0052** | 0,0003 |
| **C2, avec etiquette** | **plus 0,0882** | [0,0545 ; 0,1250] | **0,0052** | 0,0003 |
| agents v8 | plus 0,0477 | [0,0349 ; 0,0613] | **0,0052** | 0,0003 |
| agents v7 | plus 0,0268 | [0,0160 ; 0,0377] | **0,0052** | 0,0003 |

**Huit sur huit, intervalles entierement au dessus de zero, y compris les deux conditions
les plus pauvres du dossier et y compris notre agent local de 4 milliards de parametres.**
C'est la reponse la plus directe que le projet ait a la contradiction 2 de `corpus/03`.

### 2.2 H1, le gradient de rappel : douze sur treize, et une exception nommee

| condition | T3 moins T1 | IC 95 % | p Holm |
|---|---|---|---|
| agents v8 | plus 0,2504 | [0,2174 ; 0,2819] | 0,0052 |
| agents entretien (v3) | plus 0,2049 | [0,1708 ; 0,2384] | 0,0052 |
| agents composite | plus 0,1858 | [0,1511 ; 0,2206] | 0,0052 |
| C3 | plus 0,1510 | [0,0677 ; 0,2338] | 0,0052 |
| agents enquete | plus 0,1158 | [0,0811 ; 0,1507] | 0,0052 |
| B1 argmax | plus 0,1089 | [0,0915 ; 0,1259] | 0,0052 |
| C2 | plus 0,0761 | [0,0114 ; 0,1361] | 0,0370 |
| agents v7 | plus 0,0572 | [0,0369 ; 0,0788] | 0,0052 |
| B2 argmax | plus 0,0570 | [0,0403 ; 0,0746] | 0,0052 |
| B3 foret | plus 0,0352 | [0,0265 ; 0,0444] | 0,0052 |
| B0 tirage | plus 0,0341 | [0,0176 ; 0,0502] | 0,0052 |
| **agents demographiques (v6)** | **moins 0,0482** | [moins 0,0743 ; moins 0,0220] | **0,0052** |
| B0 mode | 0,0000 | sans objet | 1,0000 |

**Le gradient existe pour tout le monde, y compris pour un tirage aveugle**, `B0 tirage` a
plus 0,034, ce qui est deja l'annonce de la section 3 : une partie du gradient est une
propriete des cellules et non des methodes.

### 2.3 H3, la direction de l'ecart : notre these dirigee tombe

| condition | avantage T1 moins avantage T3 | IC 95 % | p Holm | lecture |
|---|---|---|---|---|
| agents demographiques (v6) | plus 0,1571 | [0,1261 ; 0,1877] | **0,0052** | sens de notre these |
| agents v7 | plus 0,0517 | [0,0274 ; 0,0763] | **0,0052** | sens de notre these |
| C2 | plus 0,0219 | [moins 0,0343 ; 0,0779] | 1,000 | rien |
| agents enquete | moins 0,0069 | [moins 0,0449 ; 0,0298] | 1,000 | rien |
| C3 | moins 0,0531 | [moins 0,1405 ; 0,0364] | 0,912 | rien |
| **agents composite** | **moins 0,0769** | [moins 0,1140 ; moins 0,0419] | **0,0052** | **sens de von der Heyde** |
| **agents entretien (v3)** | **moins 0,0960** | [moins 0,1325 ; moins 0,0608] | **0,0052** | **sens de von der Heyde** |
| **agents v8** | **moins 0,1415** | [moins 0,1736 ; moins 0,1092] | **0,0052** | **sens de von der Heyde** |

**Trois conditions vont dans le sens de von der Heyde, deux dans le notre, trois ne disent
rien.** Et les trois qui vont dans son sens sont **les deux meilleures conditions du dossier
et celle qui a la plus forte masse rare**. **La prediction « l'ecart avec la statistique est
maximal dans le tercile non deductible » est donc fausse en ecart absolu pour nos meilleures
conditions, et il faut cesser de l'ecrire.** Ce qui reste vrai, et qui est le resultat, est
en 2.1 : l'ecart ne s'annule nulle part, et en rapport il est cinq fois plus grand en T1.

### 2.4 Le contraste de groupe, post hoc

Permutation des etiquettes de methode, 20 000 tirages, huit conditions a modele de langage
contre cinq predicteurs statistiques. **Hors famille declaree**, avec la meme limite qu'en
a28 section 1.6 : treize unites dont plusieurs sont parentes.

[MESURE, `a34-contraste-de-groupe.csv`, seuil 10 pour cent, partition D_seg]

| perimetre | tercile | moyenne modeles de langage | moyenne predicteurs statistiques | difference | p |
|---|---|---|---|---|---|
| 1 052 | T1 non deductible | 0,1465 | 0,0151 | **plus 0,1314** | **0,0102** |
| 1 052 | T2 intermediaire | 0,1795 | 0,0213 | **plus 0,1582** | **0,0078** |
| 1 052 | T3 deductible | 0,2741 | 0,0622 | **plus 0,2120** | **0,0152** |
| 150 | T1 non deductible | 0,1268 | 0,0154 | **plus 0,1114** | **0,0044** |
| 150 | T3 deductible | 0,2376 | 0,0597 | **plus 0,1778** | **0,0113** |

**Le motif de groupe tient dans les trois terciles et sur les deux perimetres.** Rien ne
s'annule.

---

## 3. Le plancher de bruit de cellule, et ce qu'il fait au resultat

C'est la contre expertise obligatoire demandee par `corpus/01` section (d) point 5.

### 3.1 Le rappel en exces du plancher

[MESURE, `a34-planchers.csv`, perimetre 1 052, seuil 10 pour cent, **partition D_logit**,
qui est la lecture non circulaire]

| condition | T1 | T2 | T3 | ensemble |
|---|---|---|---|---|
| *plancher de segment* | *0,0388* | *0,0759* | *0,1670* | *0,0927* |
| ***humains vague 2***, exces | ***plus 0,4211*** | ***plus 0,4516*** | ***plus 0,4803*** | ***plus 0,4505*** |
| agents composite, exces | plus 0,1588 | plus 0,2058 | plus 0,2597 | plus 0,2072 |
| agents entretien (v3), exces | plus 0,1381 | plus 0,1902 | plus 0,2645 | plus 0,1965 |
| agents demographiques (v6), exces | plus 0,1421 | plus 0,0791 | **moins 0,0076** | plus 0,0725 |
| agents enquete, exces | plus 0,1018 | plus 0,1468 | plus 0,1342 | plus 0,1275 |
| agents v8, exces | plus 0,0055 | plus 0,0334 | plus 0,1439 | plus 0,0596 |
| agents v7, exces | plus 0,0050 | **moins 0,0233** | **moins 0,0670** | moins 0,0278 |
| **B1 argmax**, exces | **moins 0,0388** | **moins 0,0759** | **moins 0,0034** | **moins 0,0399** |
| **B2 argmax**, exces | **moins 0,0302** | **moins 0,0556** | **moins 0,0900** | **moins 0,0581** |
| **B3 foret**, exces | **moins 0,0388** | **moins 0,0753** | **moins 0,1246** | **moins 0,0788** |
| B0 tirage, exces | plus 0,0078 | moins 0,0059 | moins 0,0997 | moins 0,0315 |

**Trois lectures, et la troisieme est une critique du champ.**

1. **Aucun predicteur statistique ne bat le plancher, dans aucun tercile.** `B1 argmax`,
   `B2 argmax` et `B3 foret` ont un exces negatif partout, jusqu'a moins 0,125 pour la
   foret sur le tercile deductible. **Sur les cellules minoritaires, un tirage dans la
   marginale du segment ideologie x genre x age de la personne bat les trois predicteurs
   statistiques du dossier**, y compris celui que Ku 2026 nous oppose.

2. **Les deux meilleures conditions de Stanford et C3 gardent un exces positif partout**,
   de plus 0,10 a plus 0,26. C'est ce qui reste de l'avantage une fois le bruit de cellule
   paye.

3. **Le gradient de rappel est en grande partie un artefact de plancher, exactement comme
   L1.01 le prevoyait.** Sur la partition D_seg, ou le plancher est le score lui meme,
   l'exces de `agents composite` vaut 0,2181 / 0,2198 / 0,1836 : **plat, et le test H4
   ne le distingue pas de zero apres correction, moins 0,0346, p ajuste par Holm 0,2905**
   [MESURE, `a34-contrastes.csv`]. Il en va de meme pour `agents entretien`, moins 0,0155,
   p ajuste 1,000, pour C3, moins 0,0515, p ajuste 0,910, et pour `agents v8`, plus 0,0301,
   p ajuste 0,300. **Les quatre conditions qui produisent reellement des minorites n'ont
   plus de gradient de deductibilite une fois le plancher soustrait.** Les cinq predicteurs
   statistiques, eux, ont un gradient d'exces fortement negatif, de moins 0,111 pour `B1`
   a moins 0,185 pour `B3 foret`, les cinq a p ajuste 0,0052.

**L'enonce qui sort de cette section, et qui est le plus vendable du rapport** : *« sur les
reponses que moins d'une personne sur dix donne, une regression logistique et une foret
aleatoire sur demographies font moins bien qu'un tirage au sort dans le segment
demographique de la personne, dans les trois terciles de deductibilite ; une population
simulee par modele de langage fait mieux que ce tirage partout »*.

### 3.2 L'ablation C2 contre C3 par tercile, perimetre 150

[MESURE, `a34-par-tercile.csv` et `a34-planchers.csv`, perimetre 150, partition D_seg]

| condition | T1 rappel | T3 rappel | T1 exces | T3 exces |
|---|---|---|---|---|
| *humains vague 2* | *0,4154* | *0,5355* | *plus 0,4154* | *plus 0,3330* |
| agents composite | 0,1838 | 0,3270 | plus 0,1838 | plus 0,1245 |
| **C3, sans etiquette** | **0,1618** | **0,3128** | **plus 0,1618** | **plus 0,1103** |
| **C2, avec etiquette** | **0,0993** | **0,1754** | **plus 0,0993** | **moins 0,0272** |
| B1 argmax | 0,0110 | 0,1090 | plus 0,0110 | moins 0,0935 |

**C3, prive de toute etiquette, retrouve 16,2 pour cent des raretes indeductibles, contre
9,9 pour cent pour le meme modele avec onze attributs demographiques.** Et sur le tercile
deductible, **C2 tombe sous le plancher, moins 0,027, la ou C3 reste a plus 0,110**.
L'etiquette ne fait pas seulement basculer l'agent vers le stereotype de segment comme a28
et a31 le mesuraient : **elle le fait descendre au niveau d'un tirage dans ce segment.**
C'est une quatrieme mesure independante du meme phenomene, apres la deviance de a23, la
correlation par personne de a29 et le lift de groupe de a31.

---

## 4. Point 4 du cahier des charges : le rapport groupe sur personne de a31 est il calcule sur le bon tercile ?

**Reponse : non.** a31 section 2.3 calcule le lift du cote de la personne (H1b) et le lift
du cote du groupe (H2b) sur **toutes** les fausses raretes de chaque methode, sans
partition. Sur le tercile deductible, « la bonne rarete » et « la rarete de groupe »
coincident presque par construction : une modalite frequente dans le segment est, par
definition, une modalite que le segment donne souvent. **Le rapport de a31 est donc une
moyenne dominee par le tercile ou il ne peut pas etre faux.** Il fallait le recalculer sur
le tercile non deductible ; c'est fait.

### 4.1 Le recalcul, partition D_logit, qui est la lecture non circulaire

[MESURE, `a34-leviers-par-tercile.csv` ; meme definition qu'en a31, meme temoin aveugle a
la personne apparie par item, meme segment ideologique de a1, memes 4 000 tirages]

| condition | rapport groupe sur personne, **T1 non deductible** | T2 | T3 deductible | **ensemble, valeur de a31** |
|---|---|---|---|---|
| ***humains vague 2***, 1 052 | ***moins 0,32*** | ***0,39*** | ***1,84*** | ***0,56*** |
| **agents composite** | **0,02** | 1,37 | 2,75 | **1,62** |
| **agents entretien (v3)** | **0,09** | 2,40 | 5,07 | **3,65** |
| **agents enquete** | **0,31** | 1,32 | 3,09 | **1,90** |
| agents demographiques (v6) | moins 1,67 | 0,55 | 3,29 | 1,09 |
| agents v7 | moins 1,94 | non defini | 47,6 | 2,87 |
| **agents v8** | **8,27** | 6,63 | 7,39 | **7,37** |
| **C2, avec etiquette**, 150 | **4,12** | 5,07 | 4,37 | **4,45** |
| **C3, sans etiquette**, 150 | **moins 0,75** | 0,45 | 2,30 | **0,44** |
| *humains vague 2*, 150 | *moins 0,05* | *0,18* | *1,01* | *0,40* |
| B1 argmax | non evaluable, 0 cellule | 0 cellule | 5,28 | 5,28 |

**Deux verdicts opposes, et ils sont tous les deux importants.**

**Ce qui survit, et c'est le coeur de a31.** **L'ablation C2 contre C3 est intacte sur le
tercile non deductible : 4,12 contre moins 0,75, contre 4,45 contre 0,44 sur l'ensemble.**
`agents v8`, l'autre condition du dossier qui n'a que l'etiquette, est a 8,27 en T1 contre
7,37 sur l'ensemble : plat aussi. **Chez les deux conditions qui ne recoivent que
l'etiquette, la substitution de la personne par le groupe n'a rien a voir avec la
deductibilite de la rarete : elle est la partout.** Le mecanisme de a31 est donc bien un
mecanisme, pas un artefact de composition de l'echantillon de cellules.

**Ce qui tombe, et a31 ne le dit pas.** **Chez les trois conditions riches de Stanford, le
rapport s'effondre sur le tercile non deductible** : `agents composite` de 1,62 a **0,02**,
`agents entretien` de 3,65 a **0,09**, `agents enquete` de 1,90 a **0,31**. Toutes les trois
passent **sous 1**, c'est a dire du cote humain, et deux d'entre elles passent sous la
valeur humaine elle meme, moins 0,32. **Sur la rarete indeductible, les agents riches
placent leurs fausses raretes par la personne et non par le groupe, comme les humains
reinterroges.** La phrase de a31 section 2.3, *« toutes les autres methodes font
l'inverse »*, est vraie sur l'ensemble des fausses raretes et **fausse sur les fausses
raretes indeductibles pour les trois meilleures conditions du dossier**.

**Le recalcul sur la partition D_seg est donne dans `a34-leviers-par-tercile.csv` et il ne
doit pas etre lu comme un test.** Il fait tomber tout le monde, C2 comprise, a 0,96 en T1,
mais la restriction a T1 y retire par construction une partie de ce que le lift de groupe
mesure. **C'est de la circularite, et elle est signalee plutot que publiee.**

### 4.2 Ce que ce point 4 impose a la formulation de a31

Le tableau de a31 section 2.3 doit garder ses chiffres et gagner une ligne de restriction :
le rapport groupe sur personne est mesure sur toutes les fausses raretes, et il est porte
par les cellules ou la modalite rare est frequente dans le segment. **Restreint aux
cellules ou elle ne l'est pas, il ne survit que chez les conditions qui n'ont que
l'etiquette.**

---

## 5. Robustesse au seuil de 20 pour cent

[MESURE, `a34-par-tercile.csv`, hors famille, perimetre 1 052, partition D_seg, 18 411
cellules minoritaires]

| condition | T1 non deductible | T2 | T3 deductible |
|---|---|---|---|
| *humains vague 2* | *0,5314* | *0,5993* | *0,6811* |
| agents composite | 0,2789 | 0,3416 | 0,4384 |
| agents entretien (v3) | 0,2541 | 0,3363 | 0,4573 |
| agents enquete | 0,2148 | 0,2724 | 0,3374 |
| agents demographiques (v6) | 0,1800 | 0,1854 | 0,1980 |
| B0 tirage | 0,0886 | 0,1354 | 0,1541 |
| **B1 argmax** | **0,0317** | 0,0966 | 0,2480 |
| **B3 foret** | **0,0058** | 0,0242 | 0,1098 |

**Meme ordre, meme lecture, ecarts resserres comme en a29.** L'avantage de
`agents composite` sur `B1 argmax` dans le tercile non deductible passe de plus 0,204 a
plus 0,247, et le rapport de 15 a 8,8. Le gradient negatif de `agents demographiques (v6)`
disparait a ce seuil, plus 0,018 : **c'etait un effet du seuil de 10 pour cent et il ne
faut pas le porter.**

---

## 6. La figure

`a34-figure-rarete-deductible.png` et `.svg`, trois panneaux, produits par `a34_figure.py`
qui ne recalcule rien et lit les tableaux.

- **Panneau 1**, rappel par tercile de la partition principale D_seg, perimetre 1 052, une
  courbe par methode, rouge pour les conditions a modele de langage, bleu pour les
  predicteurs statistiques, vert pour les humains reinterroges. Les deux planchers sont en
  pointille, le tirage dans la marginale du segment en trait noir tirete et le tirage dans
  la marginale de l'item en pointille gris. On y voit d'un coup d'oeil le resultat : le
  faisceau rouge part de 0,17 a 0,22 quand le faisceau bleu part de 0,00 a 0,05, sous le
  pointille gris.
- **Panneau 2**, la meme chose sur la partition D_logit, avec l'avertissement inscrit dans
  le sous titre : la courbe de `B1 argmax` y est plate a zero sur T1 et T2 par arithmetique.
- **Panneau 3**, perimetre 150, avec C2 et C3, ou l'ecart entre les deux se lit dans les
  trois terciles.

---

## 7. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. « Sur les reponses rares qu'aucune autre personne du meme segment demographique n'a
   donnees, une population simulee par modele de langage en retrouve 21,8 pour cent et une
   regression logistique sur les memes attributs 1,45 pour cent, soit un rapport de 15
   contre 1 ; sur les reponses rares que le segment donne souvent, le rapport tombe a 3,3
   contre 1. » [MESURE]
2. « Les huit conditions a modele de langage du dossier ont un avantage strictement positif
   sur la regression logistique dans le tercile de rarete non deductible, les huit passant
   la correction de Holm sur une famille de 21 tests. » [MESURE]
3. « La contradiction relevee par von der Heyde ne se reproduit pas chez nous : l'ecart
   entre le modele de langage et la statistique ne se concentre pas sur la rarete
   deductible, il existe dans les trois terciles, p de permutation des etiquettes de
   methode entre 0,0044 et 0,0152. » [MESURE, post hoc]
4. « Une regression logistique et une foret aleatoire sur demographies font moins bien
   qu'un tirage au sort dans le segment ideologie x genre x age de la personne, dans les
   trois terciles de deductibilite : leur exces sur ce plancher va de moins 0,003 a
   moins 0,125. » [MESURE, c'est le chiffre le plus dur du rapport]
5. « Sur la rarete non deductible, la regression logistique retrouve 1,45 pour cent des
   reponses rares et un tirage aveugle dans la marginale de l'item en retrouve 4,72 : les
   predicteurs informes sont sous le hasard non informe. » [MESURE]
6. « Une fois soustrait le plancher de bruit de cellule, le gradient de deductibilite
   disparait chez les quatre conditions qui produisent reellement des minorites et il reste
   fortement negatif chez les cinq predicteurs statistiques. » [MESURE]
7. « A modele, personnes, questions et traces constants, donner l'etiquette demographique
   fait passer le rappel de la rarete non deductible de 16,2 a 9,9 pour cent, et fait
   passer l'agent sous le plancher de tirage dans son propre segment sur la rarete
   deductible. » [MESURE, ablation C3 contre C2]

### Interdit

1. **Interdit d'ecrire que l'ecart avec la statistique est maximal sur la rarete non
   deductible.** [MESURE] En ecart absolu il y est le plus PETIT pour `agents composite`,
   `agents entretien` et `agents v8`, les trois passant Holm sur H3. Seul le rapport, et
   non la difference, va dans le sens annonce.
2. **Interdit de citer le tableau de la partition D_logit comme un arbitrage.** [MESURE]
   Cent pour cent des raretes osees par `B1 argmax` y tombent dans le tercile deductible
   par definition. Toute lecture de cette partition doit porter l'avertissement.
3. **Interdit de citer un rappel par tercile sans le plancher du meme tercile.** [MESURE]
   Le plancher de segment passe de 0,000 a 0,220 entre T1 et T3 : la moitie du gradient
   apparent est un gradient de facilite des cellules.
4. **Interdit de reprendre le rapport groupe sur personne de a31 comme s'il valait sur la
   rarete indeductible.** [MESURE] Il tombe de 1,62 a 0,02 pour `agents composite` et de
   3,65 a 0,09 pour `agents entretien`. Il ne survit que chez `C2` et `agents v8`, les deux
   conditions qui n'ont que l'etiquette.
5. **Interdit de presenter ce rapport comme pre enregistre.** La famille a ete ecrite apres
   une lecture descriptive des rappels par tercile. a28, a29 et a31 peuvent revendiquer le
   contraire, pas celui ci.
6. **Interdit de porter le gradient negatif de `agents demographiques (v6)`.** [MESURE]
   Il vaut moins 0,048 au seuil de 10 pour cent et plus 0,018 au seuil de 20 pour cent :
   c'est un effet de seuil.
7. **Interdit d'ecrire que la statistique se trompe sur la rarete deductible.** [MESURE]
   Elle y fait son meilleur score, `B1 argmax` a 0,124 de rappel et 0,255 de precision, et
   c'est bien la lecture de von der Heyde. Ce qui est faux chez lui, chez nous, est le
   corollaire : que le modele de langage y perde son avantage.

---

## 8. Ce que cela change a `ARBITRAGE.md`

**L'option A survit a son test le plus dangereux, et sa phrase gagne une precision qui la
rend plus dure a attaquer.**

`ARBITRAGE.md` porte, dans son option A, l'enonce : « toute methode qui predit des reponses
efface les gens rares ; la statistique les efface presque tous, l'IA en garde la moitie ».
La lecture de `corpus/03` opposait a cet enonce la mesure de von der Heyde et annoncait un
test qui pouvait le faire tomber. **Le test est execute et l'enonce tient.** Trois
consequences pour la page d'arbitrage.

1. **Une phrase a ajouter, parce qu'elle repond a l'objection avant qu'on la pose** :
   *« et cela ne vient pas de ce que le modele de langage devinerait mieux les raretes
   previsibles : sur les reponses rares qu'aucune autre personne du meme segment n'a
   donnees, il en retrouve une sur cinq quand la regression en retrouve une sur soixante
   dix »*.
2. **Une phrase a retirer du stock d'arguments avant qu'elle soit ecrite** : « l'ecart est
   maximal la ou l'etiquette ne dit rien ». C'est faux en ecart absolu et le test H3 le
   dit.
3. **Une restriction a porter sur le mecanisme de la derniere ligne de la page.**
   `ARBITRAGE.md` ecrit : « le mecanisme est mesure (a31) : les fausses raretes sont les
   raretes typiques du segment, pas celles de la personne, rapport 4,45 avec etiquette
   contre 0,44 sans ». Ce couple de chiffres est celui de C2 contre C3 et **il survit sur
   la rarete non deductible, 4,12 contre moins 0,75**. La phrase peut rester telle quelle.
   Mais si quelqu'un la generalise aux conditions de Stanford, elle devient fausse : leur
   rapport tombe a 0,02 a 0,31 sur ce meme tercile. **Le mecanisme « le groupe remplace la
   personne » est un mecanisme de l'etiquette, pas un mecanisme du langage**, et c'est la
   quatrieme mesure independante qui le dit.

**Une derniere consequence, pour la these et non pour l'arbitrage.** Le resultat de la
section 3, « aucun predicteur statistique ne bat un tirage au sort dans le segment de la
personne sur les cellules minoritaires », n'etait dans aucune des cinq idees et il est plus
vendable que le facteur 11 sur le F1 : il ne compare pas une IA a une statistique, il
compare une statistique a un tirage au sort, et il perd.

---

## 9. Ce que je n'ai pas pu verifier

1. **Le pre enregistrement, et ici il est absent et non simplement inverifiable.** La
   famille de 42 tests a ete ecrite apres une lecture descriptive des rappels par tercile.
   Le choix de la partition principale en decoule directement. Un tiers doit lire ce
   rapport comme une analyse exploratoire corrigee pour tests multiples, pas comme une
   confirmation.
2. **La circularite du plancher de segment sur la partition D_seg n'est pas levee, elle est
   contournee.** Les deux quantites sont le meme calcul ; j'ai reporte la lecture de
   l'exces sur la partition D_logit, qui a son propre defaut. **Il n'existe pas, dans ce
   rapport, de partition qui soit a la fois non circulaire pour le plancher et non
   tautologique pour la regression.** Une troisieme partition, construite sur un
   predicteur tiers qui ne serait ni B1 ni une frequence de segment, la donnerait ; je ne
   l'ai pas construite.
3. **Le segment ideologie x genre x age est fin et je n'ai pas mesure la sensibilite du
   classement a ce choix.** 98 cases pour 1 052 personnes, mediane de 9 personnes par case,
   10,4 pour cent des cellules minoritaires sans score faute de cinq autres repondants.
   Une segmentation plus grossiere deplacerait les bornes de tercile et je ne sais pas de
   combien.
4. **La comparaison a von der Heyde reste une comparaison entre deux jeux et deux
   instruments.** Chez eux, la categorie rare est un vote de parti, une variable a une
   seule dimension, et leur regression semble evaluee en echantillon, sans validation
   croisee, ce qui gonfle mecaniquement ses F1 sur les classes rares. Cette faille, notee
   dans `corpus/03`, **n'est pas levee par ce rapport** : je montre que chez nous l'effet
   n'existe pas, pas que le leur est un artefact.
5. **Le tercile T1 de la partition D_seg est defini par une frequence nulle**, donc par une
   absence dans un echantillon de neuf personnes en mediane. Une partie de ce que j'appelle
   « indeductible » est un zero d'echantillonnage et non un zero structurel, au sens de
   Garrido et al. 2020 (L03-06). Le taux de change entre les deux n'est pas mesure ici.
6. **Aucun test n'a ete fait sur Twin-2K-500 ni sur le WVS.** Comme a28, a29 et a31, tout
   est sur le GSS.
7. **La comparabilite des six conditions de Stanford entre elles n'est pas verifiee**, et
   la limite ouverte depuis a17 et a23 sur la formulation des invites de C2 et C3 pese ici
   sur toute la section 3.2.
8. **Je n'ai pas mesure la sensibilite du resultat au choix du comparateur.** `B1 argmax`
   est declare parce que c'est l'adversaire de von der Heyde ; avec `B2 argmax`, qui voit
   les items de contexte et non les demographies, les avantages seraient plus grands en
   rappel et plus petits en precision, et je n'ai pas fait tourner la famille sur ce
   comparateur.

---

## 10. Questions ouvertes pour Simon

1. **Le resultat de la section 3 doit il devenir le resultat principal du papier ?**
   « Une regression logistique et une foret aleatoire sur demographies font moins bien
   qu'un tirage au sort dans le segment demographique de la personne, sur les reponses que
   moins d'une personne sur dix donne » ne parle pas d'IA du tout. C'est une critique de la
   pratique statistique du champ, elle se comprend sans connaitre le dossier, et elle est
   plus difficile a attaquer que toute comparaison entre familles de methodes. Mais elle
   deplace le papier : il ne parle plus de ce que la simulation efface, il parle de ce que
   la statistique n'a jamais produit.
2. **Faut il porter le rapport de 15 contre 1, ou l'ecart absolu de 0,204 ?** Le rapport est
   le chiffre qui se poste et il est vrai ; l'ecart absolu est le chiffre qu'un relecteur
   demandera, et il est plus petit en T1 qu'en T3, ce qui contredit la formulation
   naturelle de la these. Les deux sont dans le rapport. Lequel va dans le titre ?
3. **La partition doit elle etre refaite sur un predicteur tiers ?** Le probleme de la
   section 0.3 est reel : notre score de deductibilite principal est la confiance de notre
   adversaire, et l'autre est notre propre plancher. Un troisieme score, par exemple la
   probabilite d'un modele de melange ajuste sur les seuls items de contexte, coute une
   soiree et retirerait l'objection la plus serieuse qu'un relecteur peut faire a ce
   rapport. Est ce que cela vaut la soiree ?
4. **Que fait on de a31 ?** Son tableau central reste vrai et son ablation survit, mais son
   enonce general « toutes les autres methodes font l'inverse des humains » ne survit pas
   sur la rarete indeductible pour les trois meilleures conditions. Faut il corriger a31 en
   place, ou porter la restriction dans le papier et laisser le rapport tel quel ?
5. **Le tercile non deductible est il un zero d'echantillonnage ou un zero structurel ?**
   Garrido et al. distinguent les deux et publient leur taux de change ; nous n'avons que
   le premier. Sur neuf personnes par case, « personne n'a donne cette reponse » veut
   souvent dire « personne parmi neuf ». Faut il refaire la partition sur un segment plus
   large, quitte a perdre la finesse, ou publier le taux de change comme Garrido ?
6. **Faut il ecrire a von der Heyde ?** Leur mesure est la contre preuve la plus directe du
   corpus, ce rapport la teste sur nos donnees et trouve le signe inverse, et la variable
   explicative proposee, la nature de la rarete, est testable chez eux avec les donnees
   qu'ils ont deja. C'est le genre d'echange qui produit une note commune ou une
   replication, et c'est aussi le genre d'echange ou l'on decouvre que l'un des deux s'est
   trompe.
7. **Le rapport doit il porter le F1 par tercile plutot que le rappel par tercile ?** von
   der Heyde publie des F1 et la comparaison n'est honnete que dans sa metrique. Sur le F1,
   notre ecart est plat, 0,219 / 0,255 / 0,223 : c'est un resultat plus faible que le
   rapport de rappels, et plus difficile a contester.

---

## Rejouer

```
.venv/bin/python analyses/a34_deductibilite.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-deduct /tmp/a34-deductibilite.pkl \
    --tirages 4000
.venv/bin/python analyses/a34_figure.py
```

Les deux premiers caches sont ceux de a25 et de a28. Le troisieme est propre a a34 : il
contient les distributions hors pli de la regression logistique, 149 items fois cinq plis,
et sa reconstruction coute **4 secondes** sur quatre coeurs. Durees mesurees : **13
secondes** pour `a34_deductibilite` avec les trois caches, 4 000 tirages bootstrap et
20 000 permutations, **16 secondes** depuis un cache froid, **3 secondes** pour la figure. Graine d'analyse 20260908 partout, graine de
protocole 20260903 heritee de a2. Aucun appel de modele, aucune ecriture dans `data/`.
