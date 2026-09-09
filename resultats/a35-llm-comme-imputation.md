# a35. Le modele de langage comme methode d'imputation

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 6 : le regime « severe » donne PLUS de contexte que le regime « facile ». Objection a45 numero 7, contradiction D5.

**Phrase d'origine.** « Le cout du retrait de la famille est deux fois plus lourd pour la
regression que pour les voisins [MESURE] : `E1` perd 6,55 points (0,7304 vers 0,6649),
`IM mode` 6,32, `PMM k=10` 6,62, quand a8 mesurait moins 3,4 points pour `B2`. »

**Correction.** Les deux regimes n'ont pas la meme taille de contexte. Le regime facile
retire un bloc de validation croisee de 30 items et laisse **119 items** de contexte ; le
regime severe retire une famille de 5 a 17 items et laisse **132 a 144 items**. Le regime
dit severe est donc plus riche de 13 a 25 items que le regime dit facile, et le « cout du
retrait » de 6,55 points melange deux changements de signe oppose : le retrait de la famille
de cousins, et l'ajout de 13 a 25 items de contexte. **Le cout propre du retrait de famille
est plus grand que 6,55 points, et l'exactitude severe de `E1`, 0,6649, est optimiste.**

**Preuve.** [MESURE, `a47-contexte-regimes.csv`, produit par `analyses/a47_verifications.py`
a partir de `a2_baselines_gss.FAMILLES` et de `a35_familles.imputer_par_famille` ligne 64,
`ctx = np.setdiff1d(np.arange(m), cols)`]

| famille retiree | items retires | items de contexte |
|---|---|---|
| depenses publiques (`nat*`) | 17 | **132** |
| confiance dans les institutions (`con*`) | 13 | 136 |
| libertes civiles (`spk/col/lib`) | 11 | 138 |
| avortement (`ab*`) | 7 | 142 |
| fin de vie (`suicide/letdie`) | 5 | **144** |
| roles de genre (`fe*`) | 5 | **144** |
| *bloc de validation croisee, regime facile* | *30* | ***119*** |

**Ce qu'il faut ecrire a la place.** « Le cout mesure de 6,55 points est une **borne basse**,
le contexte du regime severe comptant 13 a 25 items de plus que celui du regime facile ; la
comparaison facile contre severe n'est pas une mesure propre du cout de l'ablation. » La
mesure propre est le couple C3 contre C3F de a33, seul contraste du dossier ou une seule
chose change.

---

Rapport du 8 septembre 2026. Il execute le test D.5 de
`corpus/lecture-complete/02-homogeneite-variance-correctifs.md` : « construire trois
predicteurs statistiques sur nos donnees, la moyenne de cellule, la regression logistique et
l'appariement sur moyenne predite, puis publier pour chacun le ratio intra et le ratio inter,
dans le meme tableau que les agents. Si nos agents se placent entre les deux, la these
devient une these de position et non une these d'accusation. »

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Quatre scripts
nouveaux, `analyses/a35_commun.py`, `a35_imputation.py`, `a35_familles.py`, `a35_figure.py`.
**Aucun script existant n'a ete modifie** ; `a2_commun`, `a2_baselines_gss`, `a8_commun`,
`a8_copule`, `a8_familles`, `a25_commun`, `a25_mesures`, `a28_commun`, `a29_commun`,
`a31_commun` et `a31_mecanismes` sont importes tels quels, memes graines, memes plis, memes
149 items, memes personnes. Les matrices de `B1 tirage` et `B2 tirage` sont relues du cache de
a2 et non recalculees ; la foret aleatoire est relue du cache de a28 ; la copule est rejouee
par appel des fonctions de `a8_copule`, avec le retrecissement 0,20 que a8 a retenu aux cinq
plis.

**Controle de protocole avant toute lecture** [MESURE]. Les lignes deja publiees se
reproduisent au chiffre pres sur les memes cellules. Exactitude : `agents composite` 0,6839,
`B2 argmax` 0,6717, `B1 argmax` 0,6209, `B0 mode` 0,5934, humains 0,7950, identiques a a2
section 4. Copule sur ses 70 items ordinaux : 0,5840 en argmax et 0,4533 en tirage,
identiques a a8 section 4.2. Minorites au seuil de 10 pour cent : `agents composite` 0,3069 de
rappel et 0,3232 de precision, `B2 argmax` 0,0357 et 0,4892, `B3 foret` 0,0144 et 0,3961,
humains 0,5483 et 0,5306, identiques a a29 section 1. Rapport groupe sur personne :
`agents composite` 1,6219, `B1 argmax` 5,2807, `B3 foret` 8,1789, `C2` 4,4463, `C3` 0,4362,
identiques a `a31-leviers-personne-segment.csv`. Regime severe : `B2 argmax` 0,6956 et
`agents composite` 0,6775 sur les 58 items de famille, identiques a a8 section 3.2. Rien n'a
bouge dans la chaine.

Sorties : `a35-tableau-quatre-cases.csv`, `a35-couples-regime.csv`, `a35-position-llm.csv`,
`a35-contrastes-descriptifs.csv`, `a35-ordinaux-copule.csv`, `a35-familles-regime-severe.csv`,
`a35-rubin-marginales.csv`, `a35-front-pareto.csv`, `a35-groupe-sur-personne.csv`,
`a35-verification-dispersion.csv`, `a35-choix-penalite.csv`, `a35-figure-imputation.png` et
`.svg`.

---

## Reponse en une ligne

**Le theoreme d'imputation de van Buuren se verifie integralement sur nos cellules, et il
ecrase la these de position : sur huit conditions a modele de langage, une seule se place
entre l'imputation par esperance et l'imputation par tirage ; les sept autres ecrasent la
dispersion intra PLUS que l'imputation par esperance de reference.** Les douze contrastes de
regime passent la correction de Holm et onze portent le signe ecrit avant execution : passer
de l'argmax au tirage, a modele constant, coute 7,8 a 10,2 points d'exactitude et remonte le
ratio intra de 0,20 a 1,01 ; sur les trois modeles qui conditionnent sur quelque chose, il
fait aussi tomber le ratio inter de 0,58 a 1,48 [MESURE, `a35-couples-regime.csv`]. Sur le ratio intra, `agents composite` est a 0,843, soit au dessus
de l'imputation par esperance `E1` a 0,797, difference +0,047 [+0,040 ; +0,054], et en dessous
de l'imputation par tirage `E2` a 1,000, difference moins 0,157 [moins 0,166 ; moins 0,148],
p ajuste par Holm 0,04 sur une famille de 16 tests declaree avant execution [MESURE,
`a35-position-llm.csv`]. **C'est la seule des huit conditions dont la position soit celle que
la these annonce.** `agents enquete` est indistinguable de `E1` (p = 0,21, le seul test de la
famille qui ne passe pas la correction) et les six autres sont sous `E1`, jusqu'a moins 0,43
pour `C2`.

**Deux chiffres desagreables, et ce sont les principaux resultats du rapport.** Premier : sur
les 149 items et les 1 052 personnes, **une regression logistique multinomiale regularisee sur
le contexte et les demographies obtient 0,7059 d'exactitude, soit 2,19 points de plus que la
meilleure des six conditions de Stanford** [MESURE, contraste apparie +0,0219
[+0,0191 ; +0,0251], p bootstrap 0,0025]. Elle bat donc les six, et non cinq comme a2
l'ecrivait pour `B2`. Second : **le coin du plan que a2 section 8 declarait occupe par le seul
modele de langage ne l'est plus.** `IM m=10 mode des m`, la modalite modale de dix imputations
multiples, fait 0,6876 d'exactitude contre 0,6839, avec un ratio intra indistinguable de celui
de `agents composite`, difference moins 0,004 [moins 0,011 ; +0,003], p = 0,275, et un
gonflement inter deux fois moindre, 1,372 contre 2,156 [MESURE,
`a35-contrastes-descriptifs.csv`]. `PMM k=10` conserve 96,3 pour cent de la diversite humaine
contre 89,6, pour 1,55 point d'exactitude en moins.

**Ce qui sauve le dossier, et il faut le dire aussi nettement : tout cela ne vaut que dans le
regime facile.** Quand la famille thematique entiere sort du contexte, protocole de a8 section
3, la regression perd 6,6 points, deux fois ce que `B2` perdait, et **repasse derriere
`agents composite` et `agents enquete`** : 0,6649 contre 0,6775 et 0,6711, avec 80,5 pour cent
de diversite conservee contre 94,8 pour cent [MESURE, `a35-familles-regime-severe.csv`]. Sur
une question reellement nouvelle, l'agent de langage domine l'imputation par regression sur
l'exactitude ET sur la dispersion.

Phrase de rechange, defendable telle quelle : **« un agent de langage est une methode
d'imputation par esperance, pas une methode de tirage : sur huit conditions, une seule laisse
les gens d'un meme groupe aussi differents qu'une regression stochastique le ferait, et sept
les rendent plus semblables qu'une simple regression logistique. Son avantage propre n'est pas
la dispersion, c'est de tenir quand la question n'a jamais ete posee. »**

---

## 0. La famille d'hypotheses, ecrite avant les resultats

Recopiee sans retouche de l'entete de `analyses/a35_imputation.py`, ou elle a ete ecrite avant
l'execution. La seule verification possible pour un tiers est la lecture de la docstring, qui
n'a pas ete modifiee apres coup.

**Perimetre declare** : les 1 052 personnes et les 149 items de a2, decoupage identique, cinq
plis sur les personnes et cinq blocs d'items, chaque couple (personne, item) predit exactement
une fois, contexte egal aux 119 autres items et aux 11 attributs demographiques. Pour `C2` et
`C3`, qui n'existent que sur 150 personnes, le perimetre naturel est ces 150 personnes, et
toutes les methodes auxquelles elles sont comparees y sont restreintes. **Mesure de dispersion
declaree** : indice de Gini Simpson, estimateur sans biais de a1, segmentation principale
l'ideologie politique, segmentation secondaire le profil croise genre x race x bloc
d'ideologie. **Seuil de minorite declare** : 10 pour cent.

| | enonce | nombre de tests |
|---|---|---|
| **H1** primaire | pour chacun des quatre couples « meme modele, deux regimes » (marginale, regression sur demographies, regression sur contexte, hot deck k = 30) et chacune des trois quantites (exactitude, ratio intra, ratio inter), la valeur en mode tirage differe de la valeur en mode argmax, bilateral | 12 |
| **H2** secondaire | pour chacune des huit conditions a modele de langage, son ratio intra differe (a) de celui de `E1 regression contexte argmax`, (b) de celui de `E2 regression contexte tirage`, bilateral | 16 |

**Signes attendus, ecrits avant execution.** Pour H1, d'apres van Buuren : exactitude plus
basse en tirage, ratio intra plus haut en tirage, ratio inter plus bas en tirage. Un signe
inverse est un resultat contre la prediction et il est signale comme tel. Le cas de la
marginale est declare a part : elle ne conditionne sur rien, son terme inter est nul dans les
deux regimes, et la prediction sur le ratio inter n'a pas de sens pour elle ; le test est
quand meme execute et compte dans la famille. Pour H2 : ratio intra superieur a celui de `E1`
et inferieur a celui de `E2`, c'est a dire strictement entre les deux.

**Famille primaire : H1, 12 tests. Famille secondaire : H2, 16 tests.** Correction principale
sur chaque famille : **Holm**, valide sans hypothese sur la dependance, ce qui est necessaire
puisque tous les contrastes portent sur les memes personnes et les memes items. Correction
secondaire rapportee a cote : **Benjamini Hochberg**. Tous les p sont des p de bootstrap
**apparie sur les personnes**, lus sur la position de zero dans la distribution ; ils ne
descendent jamais sous 1 divise par le nombre de tirages.

**N'entrent dans aucune famille**, et sont rapportes comme des descriptions : la copule
gaussienne et son couple de regimes, qui ne portent que sur 70 items ordinaux et n'ont donc
pas le meme denominateur ; le ratio de dispersion totale ; la diversite conservee et l'accord
par paires ; le rappel, la precision et le F1 minoritaires ; le rapport groupe sur personne de
a31 ; les regles de Rubin sur les marginales ; le front de Pareto ; la segmentation par profil
croise ; le perimetre 150 pour les methodes qui disposent du perimetre 1 052 ; le regime
severe par retrait de famille, qui est une verification de robustesse ; les contrastes
descriptifs autour du front, ajoutes **apres** avoir lu le front et signales comme tels ; et
la comparaison des methodes qui ne recoivent pas le meme conditionnement, signalee partout ou
elle apparait.

---

## 1. Le protocole, methode par methode, avec sa source

Le decoupage est celui de a2 et il n'a pas bouge : 5 plis sur les personnes, 5 blocs d'items,
un bloc secret et quatre blocs de contexte a chaque tour, chaque cellule predite une fois et
une seule. Le tableau ci dessous dit, pour chaque methode, d'ou elle vient et sur quoi elle
conditionne. **La colonne conditionnement est la plus importante du rapport** : opposer une
methode qui voit 11 attributs a une methode qui voit 119 reponses n'a pas de sens, et le
tableau le signale au lieu de le cacher.

| methode | regime | ce que c'est, et d'ou elle vient | conditionnement |
|---|---|---|---|
| `B0 mode` | esperance | modalite majoritaire de la marginale d'entrainement, a2_commun | rien |
| `B0 tirage` | tirage | tirage dans la marginale d'entrainement, a2_commun | rien |
| `B1 argmax` | esperance | multinomiale sur les 11 demographies, a2_commun | 11 demographies |
| `B1 tirage` | tirage | la meme, tirage dans la loi predite, a2_commun | 11 demographies |
| `B3 foret` | esperance | foret aleatoire sur demographies, a28_commun, adversaire de Ku 2026 | 11 demographies |
| **`E1 regression contexte argmax`** | esperance | **nouveau.** Multinomiale regularisee de l'item sur les 119 items de contexte en indicatrices plus les 11 demographies, modalite la plus probable. C'est la « regression imputation » de van Buuren | 119 items et 11 demographies |
| **`E2 regression contexte tirage`** | tirage | **nouveau.** Le meme modele, tirage dans la loi predite. C'est la « stochastic regression imputation » de van Buuren, son correctif | 119 items et 11 demographies |
| **`PMM k=5`, `PMM k=10`** | tirage | **nouveau.** Appariement sur moyenne predite : le meme modele, puis la valeur OBSERVEE d'un donneur tire parmi les k plus proches | 119 items et 11 demographies |
| **`IM m=10 mode des m`** | esperance | **nouveau.** Dix imputations stochastiques independantes, puis la modalite modale des dix | 119 items et 11 demographies |
| **`hot deck k=5 tirage`, `k=10`** | tirage | **nouveau.** Hot deck par plus proche voisin, tirage parmi les k voisins, meme distance de Hamming que `B2` | 119 items |
| `B2 argmax` | esperance | plus proches voisins k = 30, vote majoritaire, a2_commun : c'est le hot deck en mode esperance | 119 items |
| `B2 tirage` | tirage | les memes voisins, tirage : c'est le hot deck classique | 119 items |
| `copule argmax`, `copule tirage` | les deux | copule gaussienne de a8, 70 items ordinaux seulement | les autres items ordinaux |
| six conditions de Stanford | modele de langage | matrices publiees, archive OSF t6g7k, recalculees sur les memes 149 items | variable, voir a1 section 7 |
| `C2`, `C3` | modele de langage | run local de a5, 150 personnes | etiquette, ou 119 items sans etiquette |
| `humains vague 2` | plafond | les memes personnes reinterrogees deux semaines plus tard | la personne elle meme |

**Trois choix de methode a documenter, parce qu'ils sont contestables.**

1. **La consigne appelait la regression sur contexte « B2 ou une version regularisee ». Ce
   n'en est pas une** [CONFIRME par lecture du code]. `B2` est un estimateur a noyau non
   parametrique, les k plus proches voisins au sens de Hamming. `E1` est une multinomiale
   parametrique sur les indicatrices du contexte. Elles ne recoivent pas la meme information
   sous la meme forme et elles ne donnent pas le meme resultat : 0,7059 contre 0,6717, ecart
   +0,0341 [+0,0317 ; +0,0368] [MESURE]. La designer comme une variante de `B2` aurait masque
   le principal chiffre nouveau du rapport.
2. **La penalite de `E1` a ete choisie par validation interne au pli d'entrainement du pli 0**,
   sur 30 items tires au hasard, jamais sur un pli de test. Grille 0,003 a 1,0 ; l'optimum est
   interieur, C = 0,03, et la courbe est plate entre 0,01 et 0,03 (0,6942 et 0,6943)
   [MESURE, `a35-choix-penalite.csv`]. C'est un protocole plus propre que le choix du k de
   `B2` dans a2, qui avait ete fait sur un pli de test.
3. **PMM est generalise, et la generalisation est declaree.** L'appariement sur moyenne predite
   classique compare des moyennes predites scalaires, ce qui suppose une reponse numerique. Sur
   un item a plus de deux modalites nominales, la moyenne predite n'existe pas. La regle
   retenue apparie sur le **vecteur des probabilites predites**, au sens euclidien. Pour un
   item binaire, elle coincide exactement avec la regle classique, la distance etant une
   fonction monotone de l'ecart des moyennes predites. Aucun paquet n'a ete installe :
   `scikit-learn` et `scipy` suffisaient.

**Le bootstrap.** 2 000 tirages sur les personnes pour l'exactitude, 400 pour les quantites de
dispersion, les seconds etant les 400 premiers des premiers, le meme tirage servant a toutes
les methodes pour que les contrastes soient apparies. Le plancher de p est donc 1/400 =
0,0025, et apres Holm sur 12 tests il vaut 0,03, apres Holm sur 16 tests 0,04. **La famille
reste decidable, mais aucun p ne peut descendre plus bas, et c'est une limite du rapport.**

**Une optimisation de calcul, et sa verification.** La decomposition de dispersion est
calculee par `a28_commun.dispersion_item`, l'estimateur de a1, pour toutes les valeurs
publiees. Dans la boucle de bootstrap seulement, une version vectorisee equivalente est
employee, sans quoi 400 tirages sur 25 methodes seraient hors de portee. Les deux
implementations sont comparees sur l'echantillon complet, deux axes, quatre matrices : **l'ecart
maximal est de 5,7e-14**, soit la precision machine [MESURE,
`a35-verification-dispersion.csv`].

---

## 2. H1. Le theoreme d'imputation se verifie sur nos cellules

[MESURE, `a35-couples-regime.csv`, perimetre 1 052, axe ideologie, 400 tirages bootstrap sur
les personnes, famille primaire de 12 tests corrigee par Holm]

Passer de l'argmax au tirage, **a modele constant**, c'est a dire sans changer une ligne de ce
que la methode sait de la personne :

| couple | exactitude | ratio intra | ratio inter |
|---|---|---|---|
| marginale, `B0 mode` vers `B0 tirage` | **moins 0,1016** [moins 0,105 ; moins 0,098] | **+1,011** [+1,001 ; +1,022] | +0,092 [+0,075 ; +0,110] |
| regression sur demographies, `B1` | **moins 0,0783** [moins 0,081 ; moins 0,075] | **+0,363** [+0,355 ; +0,372] | **moins 1,477** [moins 1,614 ; moins 1,344] |
| regression sur contexte, `E1` vers `E2` | **moins 0,0855** [moins 0,088 ; moins 0,083] | **+0,204** [+0,197 ; +0,211] | **moins 0,576** [moins 0,618 ; moins 0,535] |
| hot deck k = 30, `B2` | **moins 0,0964** [moins 0,099 ; moins 0,094] | **+0,427** [+0,417 ; +0,437] | **moins 0,977** [moins 1,031 ; moins 0,917] |

**Les douze tests passent Holm a p ajuste 0,03**, qui est le plancher de la correction. **Onze
sur douze portent le signe ecrit avant execution.** Le douzieme est le ratio inter de la
marginale, dont il avait ete ecrit avant execution qu'il n'avait pas de sens : `B0 mode` a un
terme inter de moins 0,0003 et `B0 tirage` de moins 0,0085, tous deux nuls a l'estimateur
pres, et la difference de +0,092 est une difference entre deux zeros negatifs. Elle est
rapportee, elle compte dans la famille, elle ne s'interprete pas.

**Hors famille, la copule gaussienne donne le meme resultat sur ses 70 items ordinaux**
[MESURE] : moins 0,131 d'exactitude, +0,457 de ratio intra, moins 1,004 de ratio inter. Cinq
familles de modeles, cinq fois le meme comportement.

**Ce que cela etablit.** La double distorsion de a1 n'est pas une propriete des modeles de
langage : c'est la signature d'un predicteur ponctuel employe comme generateur, et elle
s'obtient chez nous avec du `scikit-learn`, dans les deux termes a la fois, avec le correctif
que la statistique d'enquete enseigne depuis Little et Rubin. **La revendication « nous avons
mesure les deux distorsions » est morte deux fois : une equipe l'a fait en avril
(`ARBITRAGE.md`), et un manuel d'imputation le predisait avant.**

---

## 3. Le tableau a quatre cases

[MESURE, `a35-tableau-quatre-cases.csv`, perimetre 1 052, 149 items, axe ideologie pour les
ratios, seuil 10 pour cent pour les minorites]

| methode | regime | exactitude | normalisee | intra | inter | total | diversite | accord paires | F1 minoritaire | groupe / personne |
|---|---|---|---|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***plafond*** | ***0,7950*** | ***100 %*** | ***1,003*** | ***1,019*** | ***1,003*** | ***100,4 %*** | ***49,1 %*** | ***0,539*** | ***0,56*** |
| **`E1` regression contexte** | esperance | **0,7059** | 88,8 % | 0,797 | 1,552 | 0,834 | 81,4 % | 57,7 % | 0,184 | 1,12 |
| `IM m=10 mode des m` | esperance | 0,6876 | 86,5 % | 0,839 | 1,372 | 0,866 | 84,9 % | 56,1 % | 0,187 | 1,10 |
| **`agents composite`** | langage | **0,6839** | 86,0 % | 0,843 | 2,156 | 0,909 | **89,6 %** | 53,9 % | **0,315** | 1,62 |
| `B2 argmax` | esperance | 0,6717 | 84,5 % | 0,538 | 1,830 | 0,602 | 58,5 % | 69,4 % | 0,067 | 1,12 |
| `PMM k=10` | tirage | 0,6684 | 84,1 % | **0,955** | 1,354 | 0,975 | **96,3 %** | 50,5 % | 0,247 | 1,25 |
| `PMM k=5` | tirage | 0,6674 | 84,0 % | **0,958** | 1,344 | 0,977 | **96,5 %** | 50,4 % | 0,247 | 1,25 |
| `agents entretien (v3)` | langage | 0,6565 | 82,6 % | 0,764 | 2,826 | 0,867 | 87,1 % | 55,9 % | 0,293 | 3,65 |
| `agents enquete` | langage | 0,6510 | 81,9 % | 0,792 | 2,519 | 0,878 | 86,1 % | 55,4 % | 0,232 | 1,90 |
| `B3 foret` | esperance | 0,6340 | 79,7 % | 0,394 | 2,781 | 0,513 | 49,4 % | 74,0 % | 0,028 | 8,18 |
| `B1 argmax` | esperance | 0,6209 | 78,1 % | 0,638 | 2,673 | 0,739 | 74,0 % | 62,5 % | 0,092 | 5,28 |
| `E2` regression contexte | tirage | 0,6204 | 78,0 % | **1,000** | 0,892 | 0,995 | 99,3 % | 49,5 % | 0,165 | 1,49 |
| `hot deck k=5 tirage` | tirage | 0,5941 | 74,7 % | 0,957 | 0,851 | 0,952 | 95,3 % | 51,7 % | 0,143 | 2,85 |
| `B0 mode` | esperance | 0,5934 | 74,6 % | 0,040 | 0,000 | 0,038 | 3,3 % | 98,1 % | 0,000 | sans objet |
| `hot deck k=10 tirage` | tirage | 0,5857 | 73,7 % | 0,963 | 0,799 | 0,955 | 95,5 % | 51,5 % | 0,128 | 4,32 |
| `agents demographiques (v6)` | langage | 0,5818 | 73,2 % | 0,652 | 0,312 | 0,635 | 63,9 % | 67,7 % | 0,224 | 1,09 |
| `B2 tirage` | tirage | 0,5752 | 72,4 % | 0,965 | 0,700 | 0,952 | 95,4 % | 51,7 % | 0,118 | 4,33 |
| `agents v7` | langage | 0,5640 | 70,9 % | 0,648 | 0,163 | 0,623 | 64,2 % | 68,3 % | 0,089 | 2,87 |
| `agents v8` | langage | 0,5591 | 70,3 % | 0,442 | **8,130** | 0,826 | 80,6 % | 58,0 % | 0,159 | 7,37 |
| `B1 tirage` | tirage | 0,5426 | 68,2 % | **1,001** | **1,001** | 1,001 | 100,0 % | 49,2 % | 0,111 | sans objet |
| `B0 tirage` | tirage | 0,4918 | 61,9 % | 1,052 | moins 0,009 | 0,999 | 99,9 % | 49,3 % | 0,062 | sans objet |

Sur les 150 personnes du run local, memes references restreintes : `C2` 0,5263 d'exactitude,
0,365 de ratio intra, 6,894 de ratio inter ; `C3` 0,5817, 0,681 et 0,724 ; `E1` 0,7027, 0,794
et 1,544 ; humains 0,7915, 0,999 et 0,998 [MESURE].

**Cinq lectures.**

1. **La colonne « total » est le piege que a1 avait deja signale, et il vaut pour la
   statistique aussi** [MESURE]. `E1` affiche 0,834 de dispersion totale, ce qu'un relecteur
   lirait comme « compression de 17 pour cent ». La decomposition dit au meme moment moins 20
   pour cent a l'interieur des groupes et **plus 55 pour cent entre eux**. `B1 tirage` affiche
   1,001, 1,001 et 1,001 : c'est la seule methode du tableau qui ne distorde ni l'un ni
   l'autre, et elle est avant derniere sur l'exactitude.
2. **Le ratio inter separe les methodes bien mieux que le ratio intra** [MESURE]. Sur l'axe
   ideologie il va de 0,163 pour `agents v7` a 8,130 pour `agents v8`, un facteur 50 entre deux
   conditions du meme papier. Toutes les methodes qui conditionnent sur du contexte riche et
   rendent un point, `E1`, `B2 argmax`, `IM`, se tiennent entre 1,37 et 1,83 ; les trois
   conditions riches de Stanford entre 2,16 et 2,83. **A conditionnement comparable, l'agent de
   langage gonfle davantage l'ecart entre camps politiques que la regression.**
3. **La segmentation par profil croise donne le meme classement** [MESURE, hors famille]. Pour
   `agents composite`, 0,847 d'intra et 1,992 d'inter contre 0,843 et 2,156 sur l'ideologie ;
   pour `E1`, 0,795 et 1,523 contre 0,797 et 1,552. La lecture ne depend pas de l'axe.
4. **Le rapport groupe sur personne de a31 dissocie deux defauts qu'on confondait** [MESURE,
   hors famille]. `E1` ecrase l'intra plus que `agents composite` (0,797 contre 0,843) mais
   **substitue beaucoup moins la personne par son groupe** (1,12 contre 1,62). `B3 foret`
   ecrase le plus (0,394) et substitue le plus (8,18) ; `IM` et `B2 argmax` sont a 1,10 et 1,12.
   Ecraser la dispersion interne et poser ses fausses raretes sur le stereotype du segment sont
   deux choses differentes, et le tableau les separe.
5. **Le F1 minoritaire reste le seul terrain ou les conditions riches de Stanford dominent
   nettement toute methode statistique** [MESURE, hors famille] : 0,315 pour `agents composite`
   contre 0,247 pour `PMM k=10`, 0,187 pour `IM`, 0,184 pour `E1`, 0,067 pour `B2 argmax`. Mais
   le facteur s'est reduit : a29 opposait 0,315 a 0,092 pour `B1 argmax`, facteur 3,4 ; contre
   `PMM k=10` le facteur tombe a **1,27**. **L'appariement sur moyenne predite reprend les deux
   tiers de l'ecart minoritaire que a29 attribuait au langage.**

---

## 4. H2. Ou se place le modele de langage

[MESURE, `a35-position-llm.csv`, famille secondaire de 16 tests corrigee par Holm, perimetre
naturel de chaque condition]

Difference de ratio intra entre chaque condition et les deux references d'imputation :

| condition | intra | contre `E1` (0,797) | contre `E2` (1,000) | position |
|---|---|---|---|---|
| `agents composite` | 0,843 | **+0,047** [+0,040 ; +0,054] | moins 0,157 [moins 0,166 ; moins 0,148] | **entre les deux** |
| `agents enquete` | 0,792 | moins 0,004 [moins 0,011 ; +0,003], p = 0,21 | moins 0,208 | indistinguable de `E1` |
| `agents entretien (v3)` | 0,764 | moins 0,032 [moins 0,042 ; moins 0,023] | moins 0,236 | sous `E1` |
| `C3` (150) | 0,681 | moins 0,114 [moins 0,130 ; moins 0,093] | moins 0,314 | sous `E1` |
| `agents demographiques (v6)` | 0,652 | moins 0,145 | moins 0,348 | sous `E1` |
| `agents v7` | 0,648 | moins 0,150 | moins 0,353 | sous `E1` |
| `agents v8` | 0,442 | moins 0,354 | moins 0,557 | sous `E1` |
| `C2` (150) | 0,365 | moins 0,429 [moins 0,457 ; moins 0,399] | moins 0,630 | sous `E1` |

**Quinze des seize tests passent Holm a p ajuste 0,04**, le plancher de la correction. Le
seizieme, `agents enquete` contre `E1`, est a p ajuste 0,21 : rien ne permet de dire que ces
deux methodes different sur le ratio intra.

**Ce que cela dit, et ce qui tombe.** La these de position, telle que la lecture de corpus la
formulait (« si nos agents se placent entre les deux, la these devient une these de position »),
**est vraie pour une condition sur huit** [MESURE]. La formulation correcte est : un agent de
langage est une methode d'esperance. Sa place dans le plan est celle d'un predicteur ponctuel,
et pour sept conditions sur huit c'est un predicteur ponctuel **plus ecrasant** que la
regression multinomiale de reference, alors meme que celle ci est la methode que van Buuren
cite comme le cas d'ecole de l'ecrasement.

Deux precisions qui empechent de conclure trop vite.

- **`agents composite` et `agents enquete` ne recoivent pas le meme conditionnement que `E1`.**
  Elles recoivent un entretien ou un questionnaire hors de notre decoupage en blocs, `E1`
  recoit exactement 119 items et 11 attributs. Les deux informations ne sont pas de meme
  nature. La comparaison est declaree, elle n'est pas propre.
- **Le contraste le plus propre du tableau est `C2` contre `C3`**, meme modele, memes
  personnes, memes items, meme run, seule l'etiquette change : 0,365 avec etiquette contre
  0,681 sans, soit un ecrasement presque double [MESURE]. Il reproduit sur le terme intra ce
  que a29 avait trouve sur l'attribution des raretes et a31 sur la substitution du groupe.

---

## 5. Le front de Pareto, et le coin que a2 croyait reserve

[MESURE, `a35-front-pareto.csv`, hors famille. Trois criteres a maximiser : l'exactitude, la
proximite de 1 du ratio intra, la proximite de 1 du ratio inter. Une methode est dominee si
une autre fait au moins aussi bien sur les trois et strictement mieux sur au moins un.]

Sept methodes sur vingt et une sont non dominees : `E1`, `IM m=10 mode des m`,
`agents composite`, `PMM k=5`, `PMM k=10`, `E2`, `B1 tirage`. **Une seule condition a modele de
langage y figure, et six n'y figurent pas.** `agents composite` s'y maintient par son ratio
intra, et par 0,004 seulement.

| | exactitude | intra | inter | diversite conservee |
|---|---|---|---|---|
| `E1` | 0,7059 | 0,797 | 1,552 | 81,4 % |
| `IM m=10 mode des m` | 0,6876 | 0,839 | 1,372 | 84,9 % |
| `agents composite` | 0,6839 | 0,843 | 2,156 | 89,6 % |
| `PMM k=10` | 0,6684 | 0,955 | 1,354 | 96,3 % |

**Contrastes descriptifs, ajoutes apres avoir lu le front et signales comme tels** [MESURE,
`a35-contrastes-descriptifs.csv`] :

- `E1` moins `agents composite` : exactitude **+0,0219** [+0,0191 ; +0,0251], intra moins 0,047,
  inter **moins 0,544** [moins 0,626 ; moins 0,458].
- `IM m=10 mode des m` moins `agents composite` : exactitude **+0,0037** [+0,0005 ; +0,0070],
  p = 0,020 ; intra moins 0,004 [moins 0,011 ; +0,003], **p = 0,275** ; inter **moins 0,703**
  [moins 0,786 ; moins 0,614].
- `PMM k=10` moins `agents composite` : exactitude moins 0,0155, intra **+0,111**
  [+0,105 ; +0,118], inter **moins 0,706**.

**La phrase de a2 section 8, « le seul avantage clair des modeles de langage dans nos mesures
est ce couple exactitude et diversite, aucune de nos baselines n'atteint ce coin du plan »,
doit etre recrite** [MESURE]. Sur le couple exactitude et diversite conservee, `agents composite`
n'est toujours pas domine, mais il n'est plus seul dans le coin : `PMM k=10` a 4,7 points de
plus de diversite et 1,55 point de moins d'exactitude, `IM mode` a 0,4 point de plus
d'exactitude et 4,7 points de moins de diversite. **Et sur le ratio intra, qui est la quantite
structurelle que a1 mesure, `IM mode des 10` est indistinguable de `agents composite` tout en
etant plus exact et en gonflant l'ecart entre camps deux fois moins.**

**Y a t il un point du plan que seul le modele de langage occupe ?** Sur ces trois criteres,
non pour sept conditions sur huit ; et pour la huitieme, par une marge de 0,004 de ratio intra
qui ne survit pas au bootstrap. La reponse mesuree est **non**, sur le regime facile.

---

## 6. Le regime severe renverse la lecture

[MESURE, `a35-familles-regime-severe.csv`, protocole de a8 section 3 repris sans retouche :
les six familles thematiques de a2, 58 items, la famille entiere retiree du contexte ET
predite. Hors famille d'hypotheses, verification de robustesse declaree.]

| methode | exactitude | normalisee | diversite | intra | inter |
|---|---|---|---|---|---|
| ***humains vague 2*** | ***0,7856*** | ***100 %*** | ***100,5 %*** | ***1,004*** | ***1,023*** |
| `E1` blocs aleatoires | 0,7304 | 93,0 % | 85,1 % | 0,812 | 1,437 |
| `IM mode` blocs aleatoires | 0,7133 | 90,8 % | 88,5 % | 0,857 | 1,341 |
| `B2 argmax` blocs aleatoires | 0,6956 | 88,5 % | 62,9 % | 0,548 | 1,728 |
| `PMM k=10` blocs aleatoires | 0,6942 | 88,4 % | 98,0 % | 0,958 | 1,339 |
| **`agents composite`** | **0,6775** | 86,2 % | **94,8 %** | 0,858 | 2,322 |
| **`agents enquete`** | **0,6711** | 85,4 % | 90,0 % | 0,795 | 2,461 |
| **`E1` famille retiree** | **0,6649** | 84,6 % | 80,5 % | 0,751 | 1,518 |
| `IM mode` famille retiree | 0,6501 | 82,8 % | 85,3 % | 0,816 | 1,353 |
| `agents entretien (v3)` | 0,6336 | 80,6 % | 88,6 % | 0,710 | 3,267 |
| `PMM k=10` famille retiree | 0,6280 | 79,9 % | 98,0 % | 0,958 | 1,356 |
| `E2` famille retiree | 0,5937 | 75,6 % | 99,3 % | 1,006 | 0,821 |

**Le cout du retrait de la famille est deux fois plus lourd pour la regression que pour les
voisins** [MESURE] : `E1` perd 6,55 points (0,7304 vers 0,6649), `IM mode` 6,32, `PMM k=10`
6,62, quand a8 mesurait moins 3,4 points pour `B2`. **Consequence directe : les deux conditions
riches de Stanford repassent devant.** `agents composite` a 0,6775 et `agents enquete` a 0,6711
battent `E1 famille retiree` a 0,6649, et `agents composite` la domine aussi sur la diversite
conservee, 94,8 contre 80,5 pour cent, et sur le ratio intra, 0,858 contre 0,751. Le seul axe
sur lequel `E1 famille retiree` reste devant est le ratio inter, 1,518 contre 2,322.

**Pourquoi.** Une regression parametrique sur 119 indicatrices exploite intensivement les
cousins thematiques d'un item ; prives d'eux, ses coefficients n'ont plus grand chose a lire.
Un agent de langage a lu ailleurs ce que le questionnaire ne lui dit pas. C'est exactement le
mecanisme que a8 section 3 avait identifie pour `B2`, en plus marque. [PROBABLE pour
l'explication, MESURE pour l'ecart.]

---

## 7. Les regles de Rubin, ou ce que coute un fichier complete

[MESURE, `a35-rubin-marginales.csv`, hors famille. Estimand : pour chaque item et chaque
modalite, la proportion de la population qui la choisit ; 486 couples (item, modalite).
Couverture : part des couples dont l'intervalle a 95 pour cent contient la vraie proportion
humaine.]

| protocole | couverture | demi largeur moyenne | biais absolu moyen |
|---|---|---|---|
| esperance, une imputation | **17,7 %** | 0,019 | 0,0544 |
| tirage, une imputation | **96,3 %** | 0,022 | 0,0079 |
| Rubin, m = 10 imputations | **100,0 %** | 0,031 | 0,0035 |

**Un analyste qui remplit un fichier par la modalite la plus probable et calcule ensuite ses
intervalles comme si les donnees etaient observees se trompe cinq fois sur six** [MESURE]. Le
biais absolu moyen sur la marginale est de 5,4 points, contre 0,8 point pour une seule
imputation stochastique. C'est le chiffre qu'un institut d'etudes comprend immediatement, et il
transporte l'argument de methodologue vers un prix.

**Deux reserves qu'il faut porter avec ce tableau.** [MESURE] La couverture de 100 pour cent
des regles de Rubin est une **sur couverture** : l'intervalle est 40 pour cent plus large que
celui d'une imputation unique. Elle vient du regime, qui n'est pas celui pour lequel Rubin a
ecrit ses regles : ici **100 pour cent des cellules sont imputees**, aucune n'est observee,
donc la variance entre imputations domine. Dans un usage reel, ou une partie des reponses est
observee, la sur couverture serait moindre. Et le protocole compare des intervalles de
couverture sans comparer leur pouvoir : un intervalle infiniment large couvre toujours.

---

## 8. Les 70 items ordinaux, avec la copule

[MESURE, `a35-ordinaux-copule.csv`, hors famille : le denominateur n'est pas celui des tableaux
precedents. Toutes les methodes recalculees sur les memes 70 colonnes.]

| methode | exactitude | diversite | intra | inter |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,7144*** | ***100,1 %*** | ***0,999*** | ***1,033*** |
| **`E1` regression contexte** | **0,5912** | 82,2 % | 0,808 | 1,766 |
| `copule argmax` (a8) | 0,5840 | 57,3 % | 0,563 | 1,607 |
| `IM m=10 mode des m` | 0,5687 | 86,6 % | 0,864 | 1,516 |
| `B2 argmax` | 0,5655 | 61,2 % | 0,565 | 2,347 |
| `agents composite` | 0,5596 | 89,4 % | 0,835 | 2,571 |
| `PMM k=10` | 0,5467 | 96,4 % | 0,957 | 1,423 |
| `copule tirage` (a8) | 0,4533 | 99,4 % | 1,021 | 0,420 |

**La phrase de a8 section 4.2, « la copule est la meilleure methode non humaine du tableau »,
tombe** [MESURE] : `E1` la depasse de 0,72 point d'exactitude et conserve 82,2 pour cent de la
diversite humaine contre 57,3 pour cent. La copule reste la seule methode dont l'accord par
paires colle a celui des humains, 38,8 contre 38,5 pour cent en mode tirage, et cela reste vrai.

---

## 9. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. « La double distorsion est un theoreme d'imputation. Sur les memes 1 052 personnes et les
   memes 149 items, passer d'une prediction ponctuelle a un tirage dans la meme loi predite
   coute 7,8 a 10,2 points d'exactitude et remonte la dispersion intra de 0,20 a 1,01 ; sur les
   trois modeles qui conditionnent sur quelque chose, il fait aussi tomber le gonflement entre
   groupes de 0,58 a 1,48. Les douze contrastes passent la correction de Holm sur une famille declaree avant execution. » [MESURE]
2. « Sur huit populations simulees par modele de langage, une seule laisse les gens d'un meme
   camp politique aussi differents qu'une imputation stochastique le ferait. Les sept autres
   les rendent plus semblables qu'une simple regression logistique sur les memes donnees. »
   [MESURE]
3. « Une regression logistique multinomiale sur les questions deja posees bat les six
   conditions d'agents du papier de Stanford sur l'exactitude individuelle, 0,7059 contre
   0,6839 pour la meilleure, sur exactement les memes cellules. » [MESURE, avec le
   conditionnement en note]
4. « L'appariement sur moyenne predite, methode standard de la statistique d'enquete,
   atteint 0,668 d'exactitude en conservant 96,3 pour cent de la diversite humaine et un
   ratio de dispersion intra de 0,955. Aucune population simulee par modele de langage
   n'approche cette combinaison. » [MESURE]
5. « Remplir un fichier d'enquete par la reponse la plus probable donne une marginale dont
   l'intervalle a 95 pour cent rate la verite cinq fois sur six ; la meme regression en mode
   tirage la rate une fois sur vingt sept. » [MESURE]
6. « Quand la question n'a jamais ete posee dans son domaine, la hierarchie s'inverse : la
   regression perd 6,6 points, deux fois ce que perdent les plus proches voisins, et les deux
   conditions riches de Stanford repassent devant, en dominant aussi sur la diversite conservee,
   94,8 contre 80,5 pour cent. » [MESURE]
7. « Ecraser la dispersion interne et remplacer la personne par son groupe sont deux defauts
   distincts : la regression sur contexte ecrase plus que l'agent composite (0,797 contre 0,843)
   et substitue deux fois moins (1,12 contre 1,62). » [MESURE]

### Interdit

1. **Interdit d'ecrire que nos agents se placent entre l'imputation par esperance et
   l'imputation par tirage.** [MESURE] C'est vrai d'une condition sur huit, `agents composite`,
   et par +0,047 de ratio intra. Sept conditions sont sous la reference d'esperance, dont nos
   deux.
2. **Interdit de reprendre la phrase de a2 section 8 sur le coin du plan.** [MESURE]
   `IM m=10 mode des m` est indistinguable de `agents composite` sur le ratio intra, plus exact
   et deux fois moins gonflant sur l'inter ; `PMM k=10` conserve plus de diversite.
3. **Interdit d'ecrire « cinq des six conditions de Stanford sont battues par du
   scikit-learn ».** [MESURE] Le chiffre correct sur ce protocole est **six sur six**, et il
   faut immediatement ajouter que la phrase s'inverse dans le regime severe.
4. **Interdit de presenter l'ecrasement de la variance comme une propriete du langage ou de
   l'alignement.** [MESURE] Une multinomiale de 1959 le produit, une foret aleatoire le produit
   davantage (0,394), la copule gaussienne le produit (0,563). Le langage n'y ajoute rien de
   qualitatif ; il y ajoute, sur le terme inter, une amplitude.
5. **Interdit de conclure de ce rapport que la simulation par langage ne sert a rien.**
   [MESURE] Deux terrains lui restent : le F1 minoritaire, ou `agents composite` fait 0,315
   contre 0,247 pour la meilleure methode statistique, et surtout le regime des questions
   jamais posees, ou elle domine sur les deux axes a la fois.
6. **Interdit de comparer `E1` et les agents de Stanford sans nommer le conditionnement.**
   [CONFIRME] `E1` recoit 119 reponses de la personne, les agents recoivent un entretien ou un
   questionnaire construits autrement. Ce sont deux informations differentes sur la meme
   personne, pas la meme information.
7. **Interdit d'employer les p de ce rapport comme des p continus.** [MESURE] Le bootstrap de
   dispersion porte 400 tirages : le plancher est 0,0025 avant correction, 0,03 et 0,04 apres.
   Vingt sept des vingt huit tests de la famille sont exactement au plancher.

---

## 10. Ce que cela change a `ARBITRAGE.md`

**L'option A survit, mais son adversaire a change de camp et sa phrase doit se restreindre au
regime severe.** `ARBITRAGE.md` oppose « la statistique fabrique une societe sans minorites,
l'IA en garde la moitie » ; le present rapport montre que la statistique dont il parle,
regression sur demographies et foret aleatoire, n'est pas la statistique d'enquete. Avec un
appariement sur moyenne predite, la statistique garde 96 pour cent de la dispersion, obtient un
F1 minoritaire de 0,247 contre 0,315, et reproduit la marginale mieux que n'importe quelle
population simulee. **Le facteur 11 contre la foret devient un facteur 1,27 contre PMM.**

Ce qui reste, et c'est desormais la phrase la plus solide du dossier :
**« aucune methode statistique, y compris les correctifs concus pour cela, ne tient quand la
question n'a jamais ete posee ; c'est la seule chose que la simulation par langage achete, et
elle l'achete en exagerant les ecarts entre camps politiques d'un facteur deux. »**

La question ouverte que `ARBITRAGE.md` place en fin de page, socle contre aligne, n'est pas
touchee par ce rapport. Celle qui s'y ajoute est ailleurs : la comparaison qui decide n'est
plus « langage contre statistique », c'est **« langage contre statistique d'enquete
correctement outillee, sur des questions nouvelles »**.

---

## 11. Ce que je n'ai pas pu verifier

1. **Le regime severe n'a pas de famille d'hypotheses ni d'intervalles.** Les chiffres de la
   section 6 sont des estimations ponctuelles sur 58 items et 1 052 personnes, sans bootstrap
   et sans correction. L'ecart de 1,3 point entre `agents composite` et `E1 famille retiree`
   n'est pas teste, et il pourrait ne pas survivre a un reechantillonnage des items. **C'est la
   verification la plus utile qui manque, et le rapport s'appuie pourtant sur ce resultat pour
   sauver la these.**
2. **La generalisation de PMM au vecteur de probabilites n'est pas validee contre PMM
   classique.** Elle coincide avec lui sur les items binaires et rien ne dit ce qu'elle fait
   sur un item a sept modalites nominales. Je n'ai pas implemente la version scalaire sur les
   items ordinaux pour comparer, faute de temps.
3. **La sur couverture des regles de Rubin n'est pas diagnostiquee.** Elle est attribuee au
   regime a 100 pour cent de cellules imputees, ce qui est plausible mais non teste : il aurait
   fallu refaire le calcul en n'imputant qu'une part des cellules.
4. **Aucune des methodes nouvelles n'est mesuree sur Twin-2K-500.** Tout le rapport porte sur le
   GSS. La replication hors GSS n'est pas faite.
5. **Le contraste de conditionnement n'est pas controle.** `E1` recoit 119 items, les agents de
   Stanford recoivent autre chose. Le rapport le declare partout mais ne construit aucune
   condition qui rende les deux informations comparables, ce qui demanderait de reconstruire
   les invites de Stanford a partir de nos 119 items.
6. **Le plancher de p.** 400 tirages sur les quantites de dispersion, choisis pour tenir dans
   le budget de calcul. Un bootstrap plus long donnerait des p plus fins, sans changer les
   signes ni les intervalles, qui sont deja stables.
7. **Le choix de la penalite de `E1` porte sur 30 items du pli 0.** Il est propre au sens ou il
   ne regarde aucun pli de test, mais il n'est pas refait pli par pli, et l'optimum pourrait
   differer sur un autre pli.
8. **La convention de codage des refus.** Une prediction hors nomenclature est traitee comme
   une cellule vide dans les mesures de dispersion et comme une reponse non minoritaire dans
   les mesures de minorite, conventions de a1 et de a29 reprises telles quelles. Je n'ai pas
   mesure ce que change la convention inverse.
9. **Le nombre de conditions comparees.** Vingt et une methodes dans un meme tableau, dont six
   conditions de Stanford dont a1 section 7 dit qu'elles ne sont pas comparables entre elles.
   Le rapport les met ensemble parce que a1, a2, a25, a28 et a29 le font deja, pas parce que
   j'ai verifie qu'elles sont comparables.

---

## 12. Questions ouvertes pour Simon

1. **Le chiffre a mettre en tete.** Deux candidats s'excluent. « Une regression bat les six
   agents de Stanford » est le plus frappant et le plus fragile : il tombe dans le regime
   severe. « Quand la question est nouvelle, l'agent domine la regression sur les deux axes »
   est le plus solide et le moins postable. Lequel porte le papier ?
2. **Faut il faire de PMM l'adversaire officiel du projet ?** `B1` et `B3 foret` sont des
   adversaires de complaisance au regard de la statistique d'enquete : personne dans un institut
   n'impute par argmax d'une multinomiale sur demographies. Passer a PMM et a l'imputation
   multiple durcit tout le dossier, et coute la moitie des ecarts publies dans a28 et a29.
3. **Le regime severe merite t il sa propre famille d'hypotheses et sa nuit de calcul ?** Il
   porte maintenant l'essentiel de la these et il est le moins bien mesure du rapport.
4. **Ou situer le terme inter dans l'argumentaire ?** C'est la seule dimension ou les
   conditions riches de Stanford sont nettement pires que toute methode d'imputation a
   conditionnement comparable, facteur 1,4 a 1,8 sur l'ideologie. Est ce l'argument principal,
   plutot que l'ecrasement intra que sept conditions sur huit partagent avec la regression ?
5. **Le couple `C2` contre `C3`.** Il donne ici le contraste le plus propre du rapport, 0,365
   contre 0,681 de ratio intra, meme modele et meme run. Trois rapports successifs, a29, a31 et
   a35, convergent sur l'etiquette comme mecanisme. Faut il en faire le sujet du papier plutot
   que la comparaison entre familles de methodes ?
6. **Ce qu'un institut achete, suite.** a29 posait la question pour les minorites, elle revient
   pour la variance : si l'acheteur veut une marginale, les regles de Rubin sur une imputation
   stochastique lui donnent 0,0035 de biais absolu pour zero appel de modele. Que reste t il a
   vendre a cote de cela ?

---

## Rejouer

```
.venv/bin/python analyses/a35_imputation.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl \
    --tirages 2000 --tirages-dispersion 400
.venv/bin/python analyses/a35_familles.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
.venv/bin/python analyses/a35_figure.py
```

Les caches sont ceux de a25 et de a28 ; s'ils manquent ils sont reconstruits. Duree : 68
secondes pour `a35_imputation` dont 35 de construction des methodes nouvelles, 14 secondes pour
`a35_familles`, 3 pour la figure, sur quatre coeurs. Graine d'analyse 20260908, graine de
protocole 20260903 heritee de a2.
