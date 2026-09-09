# i3. Detecter et quantifier une population synthetique dans un flux de reponses fermees, sans etiquette ni supervision

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 2 et reponse en une ligne : les trois constantes humaines du detecteur ne se transportent pas. Objection a45 numero 5, contradiction D12.

**Phrase d'origine.** « **Mais il est detectable en bilateral des 6,4 pour cent**, parce que
de vraies personnes ne sont pas non plus libres : les humains ont un deficit de patrons de
moins 6,9 pour cent et un exces de correlation de 0,042, et un flux qui s'en approche de zero
est aussi anormal qu'un flux qui s'en eloigne [MESURE]. »

**Correction.** Les trois statistiques de reference ne sont pas des constantes humaines : ce
sont des fonctions du questionnaire **et** de l'effectif. Mesurees sur Twin-2K-500, une
population entierement humaine, **a effectif egal de 1 052 personnes**, elles valent de 1,9 a
2,5 fois moins que sur le GSS, soit **14 a 25 ecarts types `s_0` de la reference de i3**,
tres au dela du seuil bilateral de 3,22 que le rapport fixe. **Cale comme i3 le cale, le
detecteur classerait 100 pour cent d'une population humaine reelle comme synthetique.**

**Preuve.** [MESURE, `i3b-twin-reference.csv` et `i3-reference-humaine.csv`, lus par
`analyses/a47_verifications.py` ; i3b ecrit deux heures apres i3]

| statistique | GSS, 1 052 personnes | Twin, 1 052 personnes | rapport | ecart en `s_0` de i3 |
|---|---|---|---|---|
| **A**, deficit de patrons | moins 0,0686 | **moins 0,0278** | 2,5 | **14** |
| **B**, exces de correlation | plus 0,0422 | **plus 0,0227** | 1,9 | **23** |
| **C**, concentration | plus 0,0272 | **plus 0,0115** | 2,4 | **25** |

La meme instabilite existe en effectif, sur le GSS seul : A vaut moins 0,037 a N = 300,
moins 0,050 a 500, moins 0,060 a 750 et moins 0,068 a 1 052, un facteur 1,8
[MESURE, `i3b-reference-par-taille.csv`].

**Ce qu'il faut ecrire en tete du rapport.** « Les trois statistiques varient d'un facteur
1,9 a 2,5 entre le GSS et Twin a effectif egal, et de 1,8 entre N = 300 et N = 1 052 sur le
GSS ; **aucun seuil de ce rapport ne se transporte**, la reference doit etre recalculee sur
la population et l'effectif audites. » i3b l'ecrit deja, « la bande est une forme, pas une
valeur » ; i3 ne le portait pas, et sa section 11 point 3 se contentait de dire que Twin
n'avait pas ete teste. La consequence sur la portee est bloquante ; le dispositif de i3, sa
puissance et sa borne restent valides sur le jeu et l'effectif ou ils sont calibres.

### E2. Section 11 point 10 : le facteur 1,62 attribue a `v8` est celui de C2. Objection a45 numero 11.2, contradiction D10.

**Phrase d'origine.** « Les deux vont dans le meme sens pour v8, **facteur 1,76 ici contre
1,62 en a38**, mais ce ne sont pas les memes nombres et il ne faut pas les confondre. »

**Correction.** Le facteur d'amplification de a38 pour `v8` vaut **3,167 au perimetre 150 et
3,091 au perimetre 1 052** ; **1,62 est celui de C2**, une autre condition. La phrase compare
la polarisation de `v8` mesuree par i3 a l'amplification de C2 mesuree par a38.

**Preuve.** [MESURE, `a47-a38-invariance-facteur.csv` : `agents v8` 3,091378 a 1 052 et
3,167249 a 150 ; `C2` 1,616674 a 150.]

**Ce qu'il faut ecrire.** « 1,76 a 50 pour cent de contamination par `v8`, contre un facteur
d'amplification de 3,09 pour une population de `v8` pure en a38 ; les deux quantites ne sont
pas comparables directement. » S'y ajoute que le facteur de a38 est une quantite de gabarit,
exactement invariante sous permutation des personnes a l'interieur de leur camp, alors que la
polarisation de i3 est mesuree sur les rangs de la population entiere : la comparaison entre
les deux ne peut pas etre une confirmation mutuelle.

---

Jour 4 de la premiere semaine du brainstorm d'impact, idee I3, avec I4 en corollaire.
Zero appel de modele de langage, lecture seule sur `data/`, quatre coeurs, 1 480 secondes de
calcul. Aucun fichier existant n'est modifie.

**Preenregistrement : `resultats/i3-preenregistrement.md`, ecrit le 8 septembre 2026 a
19 h 12 CEST, avant l'ecriture des scripts et avant tout calcul, non modifie depuis.** Les
sources, la regle de melange, les cinq taux, les trois statistiques, le mode de
reechantillonnage, la formule de puissance, la famille de tests et sept predictions y sont
figes. Cinq ecarts sont declares en section 0, et trois des sept predictions sont fausses ou
a moitie fausses, ce qui est la preuve que le texte a bien ete ecrit avant.

---

## Reponse en une ligne

**Oui, on detecte, mais le seuil depend entierement du fabricant, et l'auditeur qui ignore
lequel sous evalue la quantite d'un facteur 2,4 a 10, ou rend zero.** Sur un flux de 1 052 reponses a
149 items fermes, avec la seule ideologie declaree et aucune etiquette de provenance, un test
bilateral a 5 pour cent corrige par Holm sur la famille preenregistree de 27 tests signale
**des 5 pour cent de contamination** un agent a etiquette ideologique, `agents v8`
(`p` de Holm 1,7e-4 sur le deficit de patrons, 3,9e-4 sur l'exces de correlation et 1,1e-8 sur
la concentration) et notre agent local a etiquette `C2` (1,7e-5 sur le deficit et 3,4e-11 sur
la concentration)
[MESURE, `i3-puissance.csv`]. **Le plus petit taux detectable a puissance 80 pour cent** vaut
**1,9 pour cent pour `agents v8`** et **3,6 pour cent pour `C2`** ; il monte a **6,6 pour cent
pour l'agent a demographies `v6`**, a **11,5 pour cent pour l'agent riche `composite`**, et a
**21,9 pour cent pour `PMM k=10`** et **24,6 pour cent pour la regression stochastique
`E2`**, c'est a dire les deux adversaires par tirage [MESURE, seuil de Holm, `alpha` corrige
0,05 / 27]. Sur un flux de vraies personnes reinterrogees deux semaines plus tard, le
detecteur ne se declenche pas avant 95 pour cent de melange : **il ne prend pas de vrais
humains pour des faux**.

**La borne adverse est publiee, et elle n'est pas celle que le brainstorm annoncait.**
L'adversaire nul, un faux repondant dont chaque reponse est tiree dans la marginale de son
segment ideologique, est bien invisible a un test unilateral cale sur les agents : il deplace
le deficit de patrons **vers le haut**, de moins 6,86 a moins 2,36 pour cent a 50 pour cent de
contamination, et l'exces de correlation **vers le bas**, de 0,0422 a 0,0163, c'est a dire
dans la direction exactement opposee. **Mais il est detectable en bilateral des 6,4 pour
cent**, parce que de vraies personnes ne sont pas non plus libres : les humains ont un deficit
de patrons de moins 6,9 pour cent et un exces de correlation de 0,042, et un flux qui s'en
approche de zero est aussi anormal qu'un flux qui s'en eloigne [MESURE]. **Le detecteur ne
protege donc pas contre le tirage dans le segment ; il le voit, mais il faut l'avoir prevu
dans les deux sens, et un test unilateral construit sur nos agents le laisse passer
integralement.**

**La quantification marche seulement si l'on connait le fabricant.** Calibree sur la bonne
source, l'inversion de la courbe de melange estime le taux a moins de 1,5 point pres pour
toutes les conditions a modele de langage, et a 2,8 a 9,7 points pour PMM. En calibration
croisee entre familles, elle se trompe de 15 a 78 points. Avec la calibration agnostique, la
courbe moyenne des agents appliquee a tout, un flux contamine a 50 pour cent par PMM est
estime a 4,9 a 11,0 pour cent, et un flux contamine a 50 pour cent par `E2` ou par le tirage
dans le segment est estime a **zero** [MESURE, `i3-quantification.csv`]. **Un institut qui
publierait « 5 pour cent de synthetique detectes » sans dire de quel type publierait un
plancher, jamais une part.**

**I4, en corollaire, contredit la formulation du brainstorm et donne une variable plus
propre.** L'ecart gauche droite mesure ne se separe pas en gabarit contre tirage : il se
separe selon que le fabricant a recu **l'etiquette ideologique** ou non. A 50 pour cent de
contamination, `agents v8` porte la polarisation mesuree a 1,76 fois sa valeur humaine et
`agents composite` a 1,21, tandis que `agents v6`, qui recoit des demographies sans ideologie,
la ramene a **0,78** ; les imputations par tirage ne bougent presque pas, 0,97 pour `E2` et
1,08 pour `PMM`, et le tirage dans le segment donne 0,99 [MESURE, `i3-polarisation.csv`].
**Le signe du biais de polarisation est fixe par le groupe nomme, exactement comme
`MODELE-DU-MONDE.md` section 4 le predit, et pas par le mode de fabrication.**

---

## 0. Le preenregistrement, les cinq ecarts, et le score des sept predictions

### 0.1 Les ecarts, tous declares

| | ecart | pourquoi |
|---|---|---|
| **E1** | **Le mode de reechantillonnage de la statistique B a change.** Le preenregistrement, section 5, reservait le bootstrap avec remise a B, en supposant que seules A et C etaient sensibles aux doublons. La reference de B est finalement prise par **sous echantillonnage sans remise** a `m = 526`, comme A et C. | Mesure : le bootstrap avec remise donne `B = 0,04782` contre 0,04222, biais **+0,00561**, soit 13,3 pour cent de la valeur [MESURE, `i3-controles.csv`]. Une ligne dupliquee est une co-variation parfaite entre tous les items, que le generateur nul detruit ; le bootstrap fabrique donc de l'exces de correlation. Le defaut que a44 section 0 signalait sur Q3 vaut aussi sur Q5, ce que a44 n'ecrivait pas. La valeur biaisee et son biais sont publies a cote. |
| **E2** | **Le pivot de l'intervalle sous echantillonne est la moyenne des tirages, pas la valeur de reference.** | Sans ce correctif, les intervalles ne contenaient pas leur propre estimation ponctuelle, la loi a `m = 526` etant decalee : le nombre de patrons distincts et la concentration dependent de l'effectif. C'est le meme defaut que a44 section 11 point 8 decrit sur ses IC de Q5, corrige ici. |
| **E3** | **Une source descriptive ajoutee, `humains vague 2`**, les memes personnes reinterrogees deux semaines plus tard, melangees aux cinq taux comme si elles etaient un fabricant. Elle n'entre dans aucune famille de tests. | Ajoutee avant lecture des resultats, apres avoir constate que le controle negatif preenregistre, les humains melanges a eux memes, est trivialement nul et ne mesure aucune fausse alarme. Celle ci mesure une vraie fausse alarme : de vraies personnes, un autre jour. |
| **E4** | **`B0 segment` est regenere a chaque tirage de melange** et non tire une fois pour toutes. | C'est la lecture fidele de sa definition, un faux repondant est un tirage independant, mais le preenregistrement ne le disait pas explicitement. |
| **E5** | **La correction de Benjamini Hochberg a l'interieur de chaque source**, annoncee en section 6 du preenregistrement pour les taux au dela de 5 pour cent, est calculee dans ce rapport a partir des `p` du tableau et non ecrite dans le CSV. | Cout d'ecriture nul, mais il faut le dire : la colonne `p_holm` de `i3-puissance.csv` ne porte que la famille primaire des 27 tests a 5 pour cent. Les valeurs BH sont dans la section 5.3 de ce rapport. |

### 0.2 Le score des sept predictions [MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | les trois statistiques separent `agents v8` a 25 et a 50 pour cent, avec Holm | **tenue.** `z` de 28,2 a 168,3 selon la statistique et le taux, `p` de BH nuls a la precision machine |
| **P2** | `tau*` de la meilleure des trois est inferieur a 10 pour cent pour v8 et superieur a 25 pour cent pour composite | **a moitie tenue, a moitie fausse.** v8 : 1,9 pour cent, tenue et largement. Composite : **11,5 pour cent**, donc fausse ; l'agent riche est bien plus detectable que je ne le predisais |
| **P3** | `PMM k=10` n'est pas detectable en dessous de 25 pour cent par la concentration | **tenue.** `tau*` de C pour PMM vaut 52,6 pour cent sous Holm et 34,3 pour cent au seuil nominal |
| **P4** | PMM est detectable par le deficit de patrons a un taux plus bas que par la concentration | **tenue**, 36,0 contre 52,6 pour cent. Non predit : c'est l'exces de correlation qui fait le mieux, 21,9 pour cent |
| **P5** | `B0 segment` deplace A et B dans la direction opposee, et n'est visible en bilateral qu'au dela de 25 pour cent | **tenue sur la direction, fausse sur le seuil.** A monte de moins 0,0686 a moins 0,0236 et B descend de 0,0422 a 0,0163 a 50 pour cent, comme predit ; mais `tau*` vaut **6,4 pour cent** sur B, quatre fois plus bas que ma prediction |
| **P6** | erreur superieure a 15 points en calibration croisee entre familles ; inferieure a 5 points en calibration propre au dela de 10 pour cent | **tenue sur la premiere moitie**, 15 a 78 points selon le couple. **A moitie fausse sur la seconde** : vraie pour les conditions a modele de langage, 0,4 a 2,2 points, fausse pour PMM sur A et sur C, 7,1 et 9,7 points a 50 pour cent |
| **P7** | l'ecart gauche droite croit avec v8 et C2 et decroit avec PMM, E2 et B0 segment | **fausse.** Il croit avec v8, composite, C2, **et aussi avec PMM et IM**, faiblement ; il decroit avec **v6** fortement, avec C3 et avec E2 faiblement. La variable qui separe n'est pas gabarit contre tirage, c'est l'etiquette ideologique recue ou non |

Trois predictions tenues, une fausse, trois a moitie fausses. **Aucune reecriture n'a ete
faite ; les predictions fausses sont les plus informatives du rapport**, en particulier P7,
qui remplace la formulation d'I4 par une variable plus propre.

---

## 1. Les controles, executes et lus avant toute lecture de resultat

[MESURE, `i3-controles.csv`, 38 lignes, **les 38 passent**]

1. **Part de cellules renseignees mais hors nomenclature** : 0,000 pour cent chez les humains
   des deux vagues, chez C2, C3, PMM, E2 et IM ; au pire **0,070 pour cent** pour
   `agents v8`. Seuil declare 0,5 pour cent, passe partout.
2. **Cellules perdues par l'intersection des masques**, lues sur les seules lignes ou la
   source existe : **0,000 pour cent** pour C2, C3, PMM, E2, IM et la vague 2 ; **0,171 pour
   cent** pour v8, **0,244** pour v6, **0,043** pour composite. Seuil declare 0,5 pour cent.
   Le masque du flux est donc a moins d'un quart de pour cent celui des humains, a tous les
   taux, et la statistique de concentration est comparable d'une source a l'autre.
3. **Taux de repli du generateur nul sous `S_ideo`** : **0,0 pour cent**, sept segments,
   1 043 couples item x segment. Le nul conditionne reellement partout, ce qui est la
   condition que a44 section 1 point 6 pose.
4. **Le flux a taux 0 egale la population humaine**, ecart **0 cellule**.
5. **Controle negatif preenregistre**, les humains melanges a eux memes aux cinq taux, ecart
   **0 cellule** : le dispositif de melange ne fabrique aucune difference.
6. **Validite de la mise a l'echelle du sous echantillonnage**, `K = 60` populations
   independantes tirees du generateur nul humain, taille 1 052. Rapport entre l'ecart type de
   sous echantillonnage remis a l'echelle et l'ecart type inter population directement
   mesure : **0,935 pour A, 1,053 pour B, 0,892 pour C**. Seuil declare, entre 0,7 et 1,4.
   **Les intervalles de la section 3 sont donc corrects a moins de 11 pour cent pres, et
   plutot legerement conservateurs.**
7. **Reproduction de a44 sur les sources pures**, taux 100 pour cent, six conditions
   communes : ecart maximal **0,0021** sur le deficit de patrons du tableau 3 de a44
   (`agents demographiques (v6)`, moins 22,79 pour cent ici contre moins 23,0 publie) et
   **0,00044** sur l'exces de correlation du tableau 4 (`C2`, 0,0463 ici contre 0,0467
   publie). Seuil declare 0,005. **La chaine de mesure de i3 est celle de a44, sans une ligne
   modifiee, et elle redonne ses chiffres.**

---

## 2. Protocole

### 2.1 Le flux

**Remplacement en place, effectif constant.** Le flux compte toujours `N = 1 052` lignes et
149 items. Au taux `tau`, `round(tau x N)` personnes sont tirees sans remise et leur ligne de
reponses humaine est remplacee par celle que la source synthetique produit **pour cette meme
personne**. La colonne des demographies declarees n'est jamais touchee, donc la composition
par segment est strictement invariante et aucun signal ne peut venir d'un desequilibre
demographique. Le masque de la cellule est l'intersection du masque humain et du masque de la
source, controle 1.2. `D = 20` tirages de melange par couple (source, taux), graines fonction
de la source, du taux et du numero de tirage, jamais de l'ordre d'execution.

`C2` et `C3` n'existent que sur les 150 personnes du run local, donc le taux maximal
atteignable sans dupliquer de ligne vaut `150 / 1052 = 14,3 pour cent` : **elles ne sont
melangees qu'a 5 et 10 pour cent**, comme le preenregistrement l'ecrit, et leurs `tau*` sont
des extrapolations sur trois points seulement. Il faut le lire ainsi et pas autrement.

### 2.2 Les trois statistiques, et ce que l'auditeur a besoin de connaitre

| | statistique | ce que l'auditeur doit avoir | valeur de reference chez les humains |
|---|---|---|---|
| **A** | deficit relatif de patrons de reponses distincts par rapport au **generateur nul du flux lui meme** ; vingt sous ensembles de dix items, ceux de a44, graine identique | la matrice de reponses et l'ideologie declaree | **moins 6,86 pour cent** |
| **B** | exces de correlation moyenne `|rho|` de Spearman entre items **apres retrait du rang moyen du segment**, 11 026 paires, moins le meme exces sur le nul du flux | idem | **+0,04222** |
| **C** | concentration par segment : part des personnes d'un segment qui donnent le patron modal du segment, sur les memes vingt sous ensembles, moyenne ponderee par l'effectif complet | idem | **0,02723** |

**Aucune des trois n'exige la verite terrain par personne.** C'est le point de tout le
rapport : la mesure qui separe le mieux dans a44, la chute d'exactitude sous permutation intra
segment, exige de connaitre la vraie reponse de chaque personne, ce qu'un auditeur de sondage
n'a jamais. Elle n'entre pas dans le detecteur et n'est pas mesuree ici.

Le generateur nul est la transposition categorielle de l'equation (2) de Yuan reprise de
`a44_commun` sans une ligne modifiee, `X_ij ~ Multinomiale(p_{j, g(i)})`, parametree sur **le
flux lui meme** et non sur les humains, masque conserve. `R = 40` replicats nuls par flux ;
l'ecart type inter replicat est publie dans `i3-melanges.csv`.

### 2.3 Le test, la correction, la puissance

Test **bilateral**, seuil nominal 5 pour cent. Le choix du bilateral est preenregistre et il
est le bon : la section 7 montre que deux des neuf sources deplacent A et B dans la direction
opposee a celle des agents, et un test unilateral cale sur les agents les laisserait passer
entierement.

Famille primaire : `3 statistiques x 9 sources = 27` tests, chacun etant « la statistique du
flux a `tau = 5` pour cent differe de la reference humaine », **correction de Holm**. Les
couples au dela de 5 pour cent sont corriges par Benjamini Hochberg a l'interieur de leur
source, section 5.3.

Le plus petit taux detectable `tau*` est la plus petite racine positive de
`|E[T(tau)] - T(0)| = (z + 0,8416) x s_0`, ou la courbe `E[T(tau)] - T(0)` est ajustee par une
regression de degre 2 sans terme constant, `R^2` de 0,9948 a 1,0000 sur les trente courbes
[MESURE], et `s_0` l'ecart type de reference de la section 3. Deux versions : `z = 1,960`,
seuil nominal, et `z = 3,113`, seuil de Holm pour la famille de 27. **C'est la seconde qu'il
faut citer.**

---

## 3. La reference humaine et son bruit

[MESURE, `i3-reference-humaine.csv`, 1 000 tirages, sous echantillonnage sans remise a
`m = 526` remis a l'echelle par `racine(m / N) = 0,7071`, validite du facteur verifiee au
controle 1.6]

| statistique | valeur sur le flux pur | IC a 95 pour cent | `s_0` | dont bruit du nul interieur |
|---|---|---|---|---|
| **A**, deficit de patrons | **-0,06856** | [-0,07427 ; -0,06300] | 0,002919 | 0,000294 |
| **B**, exces de correlation | **+0,042216** | [0,040593 ; 0,043856] | 0,000861 | 0,000013 |
| **C**, concentration par segment | **0,027234** | [0,026027 ; 0,028381] | 0,000632 | 0 |
| *P*, polarisation, pour I4 | *0,45045* | *[0,42360 ; 0,47735]* | *sans objet* | *sans objet* |

Deux lectures a faire ici et pas ailleurs.

**Le bruit du generateur nul interieur est negligeable devant le bruit d'echantillonnage**,
0,000294 contre 0,002904 sur A, soit un dixieme, et un soixantieme sur B. `R = 40` replicats
suffisent largement ; monter a 200 ne changerait pas le troisieme chiffre de `s_0`.

**Le bootstrap avec remise est inutilisable pour ces trois statistiques.** Sur B il donne
0,04782 contre 0,04222, biais **+0,00561**, soit **6,5 ecarts types de reference**. Ce n'est
pas une subtilite : un detecteur calibre sur ce bootstrap aurait une bande deportee de six
ecarts types et **ne detecterait plus rien du tout du cote haut**. a44 avait vu le probleme
sur le comptage de patrons ; il est aussi grave sur la correlation, et c'est l'ecart E1.

---

## 4. Les courbes de melange

[MESURE, `i3-melanges.csv` et `i3-puissance.csv`, moyenne sur 20 tirages par cellule ; la
ligne `tau = 0` est la reference de la section 3, commune a toutes les sources]

### 4.1 Tableau 1 : les valeurs pures, taux 100 pour cent

Ce que chaque fabricant vaut sans melange, sur son propre perimetre [MESURE,
`i3-sources-pures.csv`].

| source | famille | `N` | A | B | C |
|---|---|---|---|---|---|
| humains vague 1, reference | humain | 1 052 | **-0,0686** | **+0,0422** | **0,0272** |
| `agents v8` | etiquette ideologique | 1 052 | **-0,3199** | 0,0942 | **0,2587** |
| `agents demographiques (v6)` | demographies | 1 052 | -0,2279 | 0,0926 | 0,1216 |
| `agents composite` | riche | 1 052 | -0,1819 | 0,0839 | 0,0584 |
| `IM m=10 mode des m` | imputation par esperance | 1 052 | -0,1208 | 0,0571 | 0,0508 |
| `PMM k=10` | imputation par tirage | 1 052 | -0,0984 | 0,0558 | 0,0314 |
| **`E2 regression contexte tirage`** | imputation par tirage | 1 052 | **-0,0376** | **0,0275** | **0,0240** |
| **`B0 segment`, adversaire nul** | tirage dans le segment | 1 052 | **+0,0014** | **-0,0003** | **0,0229** |
| `C2` | etiquette, local | 150 | -0,1615 | 0,0463 | 0,3690 |
| `C3` | sans etiquette, local | 150 | -0,1378 | 0,0547 | 0,1537 |

**Deux fabricants sont au dessus des humains et non en dessous.** `B0 segment` est exactement
son propre nul, A = +0,0014 et B = -0,0003, ce qui est le controle negatif du dispositif
transpose ici. Et **`E2`, la regression stochastique sur les 119 items de contexte, est plus
libre qu'une vraie population** : A = -0,0376 contre -0,0686, B = 0,0275 contre 0,0422.
**Une imputation par tirage sur un modele riche produit moins de structure residuelle que de
vraies personnes**, ce qui est la lecture de a44 tableau 4 point 3 sur `B3 foret` etendue au
regime de tirage [MESURE]. Cela fixe le signe de sa courbe de melange, section 7.

### 4.2 Tableau 2 : la statistique A, deficit de patrons, contre le taux

Reference humaine **-0,0686**, IC [-0,0743 ; -0,0630].

| source | 5 % | 10 % | 25 % | 50 % | `z` a 5 % | puissance empirique a 5 % |
|---|---|---|---|---|---|---|
| `agents v8` | **-0,0817** | **-0,0985** | -0,1508 | -0,2258 | **-4,5** | **1,00** |
| `agents demographiques (v6)` | -0,0750 | -0,0830 | -0,1098 | -0,1501 | -2,2 | 0,75 |
| `agents composite` | -0,0724 | -0,0758 | -0,0916 | -0,1202 | -1,3 | 0,05 |
| `IM m=10 mode des m` | -0,0724 | -0,0766 | -0,0868 | -0,1024 | -1,3 | 0,05 |
| `PMM k=10` | -0,0707 | -0,0721 | -0,0770 | -0,0835 | -0,7 | 0,00 |
| `E2 regression contexte tirage` | -0,0677 | -0,0660 | -0,0610 | -0,0536 | +0,3 | 0,00 |
| **`B0 segment`** | **-0,0638** | **-0,0583** | **-0,0435** | **-0,0236** | **+1,6** | 0,25 |
| `C2` | -0,0830 | -0,1026 | sans objet | sans objet | -5,0 | 1,00 |
| `C3` | -0,0758 | -0,0886 | sans objet | sans objet | -2,5 | 0,90 |
| *`humains vague 2`, controle* | *-0,0699* | *-0,0699* | *-0,0717* | *-0,0744* | *-0,5* | *0,00* |

### 4.3 Tableau 3 : la statistique B, exces de correlation, contre le taux

Reference humaine **+0,04222**, IC [0,04059 ; 0,04386].

| source | 5 % | 10 % | 25 % | 50 % | `z` a 5 % | puissance empirique a 5 % |
|---|---|---|---|---|---|---|
| `agents v8` | **0,0459** | **0,0504** | 0,0667 | 0,0900 | **+4,3** | **1,00** |
| `agents demographiques (v6)` | 0,0443 | 0,0466 | 0,0571 | 0,0735 | +2,4 | 0,80 |
| `agents composite` | 0,0435 | 0,0449 | 0,0505 | 0,0605 | +1,5 | 0,15 |
| `IM m=10 mode des m` | 0,0429 | 0,0437 | 0,0460 | 0,0499 | +0,8 | 0,00 |
| `PMM k=10` | 0,0430 | 0,0438 | 0,0461 | 0,0494 | +0,9 | 0,00 |
| **`E2 regression contexte tirage`** | **0,0415** | **0,0410** | **0,0387** | **0,0352** | **-0,8** | 0,00 |
| **`B0 segment`** | **0,0395** | **0,0369** | **0,0290** | **0,0163** | **-3,2** | **1,00** |
| `C2` | 0,0443 | 0,0489 | sans objet | sans objet | +2,5 | 0,85 |
| `C3` | 0,0443 | 0,0493 | sans objet | sans objet | +2,4 | 0,85 |
| *`humains vague 2`, controle* | *0,0423* | *0,0424* | *0,0429* | *0,0434* | *+0,1* | *0,00* |

**C'est la statistique la plus utile des trois pour un auditeur aveugle** : c'est elle qui a
le `tau*` le plus bas sur six des neuf sources, et c'est la seule qui attrape l'adversaire nul
des 5 pour cent, puissance empirique 1,00, `z = -3,2`.

### 4.4 Tableau 4 : la statistique C, concentration par segment, contre le taux

Reference humaine **0,02723**, IC [0,02603 ; 0,02838].

| source | 5 % | 10 % | 25 % | 50 % | `z` a 5 % | puissance empirique a 5 % |
|---|---|---|---|---|---|---|
| `agents v8` | **0,0312** | **0,0395** | **0,0724** | **0,1337** | **+6,2** | **1,00** |
| `agents demographiques (v6)` | 0,0280 | 0,0299 | 0,0411 | 0,0667 | +1,2 | 0,15 |
| `agents composite` | 0,0277 | 0,0283 | 0,0311 | 0,0391 | +0,7 | 0,00 |
| `IM m=10 mode des m` | 0,0283 | 0,0296 | 0,0328 | 0,0386 | +1,7 | 0,45 |
| `PMM k=10` | 0,0276 | 0,0277 | 0,0286 | 0,0296 | +0,6 | 0,00 |
| `E2 regression contexte tirage` | 0,0270 | 0,0270 | 0,0263 | 0,0255 | -0,4 | 0,00 |
| `B0 segment` | 0,0269 | 0,0267 | 0,0257 | 0,0243 | -0,5 | 0,00 |
| `C2` | **0,0317** | **0,0432** | sans objet | sans objet | **+7,1** | **1,00** |
| `C3` | 0,0269 | 0,0282 | sans objet | sans objet | -0,5 | 0,00 |
| *`humains vague 2`, controle* | *0,0272* | *0,0272* | *0,0271* | *0,0269* | *-0,0* | *0,00* |

**C est la statistique la plus specifique et la moins sensible.** Elle est de tres loin la
meilleure sur les deux conditions a etiquette ideologique, `z = 6,2` pour v8 et `7,1` pour C2
des 5 pour cent, et elle ne voit presque rien d'autre : `z = 0,6` pour PMM, `-0,4` pour E2,
`-0,5` pour l'adversaire nul et `-0,5` pour C3, l'agent sans etiquette. **C'est la definition
operationnelle du gabarit : la concentration par segment ne mesure que la fabrication qui
conditionne sur le groupe nomme.** La variante a cinq items, declaree au preenregistrement,
donne la meme lecture avec des effectifs modaux plus grands : de 0,1036 chez les humains a
0,2489 pour v8 a 50 pour cent, contre 0,1112 pour PMM [MESURE, `i3-melanges.csv`, colonne
`C5`].

---

## 5. Le plus petit taux detectable

### 5.1 Tableau 5 : `tau*`, puissance 80 pour cent

[MESURE, `i3-puissance.csv`. En gras la meilleure des trois statistiques pour chaque source.
La colonne de droite est celle a citer.]

| source | famille | A | B | C | **meilleure, Holm** | meilleure, seuil nominal |
|---|---|---|---|---|---|---|
| `agents v8` | etiquette | 0,036 | 0,037 | **0,019** | **1,9 %** | 1,4 % |
| `C2` | etiquette, local | 0,041 | 0,067 | **0,036** | **3,6 %** | 2,9 % |
| **`B0 segment`** | adversaire nul | 0,111 | **0,064** | 0,427 | **6,4 %** | 4,5 % |
| `agents demographiques (v6)` | demographies | 0,074 | **0,066** | 0,076 | **6,6 %** | 4,7 % |
| `C3` | sans etiquette, local | 0,070 | **0,067** | 0,130 | **6,7 %** | 5,5 % |
| `IM m=10 mode des m` | imputation esperance | 0,152 | 0,229 | **0,111** | **11,1 %** | 7,9 % |
| `agents composite` | riche | 0,138 | **0,115** | 0,185 | **11,5 %** | 8,3 % |
| `PMM k=10` | imputation tirage | 0,360 | **0,219** | 0,526 | **21,9 %** | 15,3 % |
| `E2 regression contexte tirage` | imputation tirage | 0,390 | **0,246** | 0,738 | **24,6 %** | 17,5 % |
| *`humains vague 2`, controle* | *humain* | *sans objet* | *jamais* | *jamais* | *jamais* | *95,5 % sur A* |

`R^2` de l'ajustement quadratique : 0,9948 a 1,0000 sur les trente courbes, donc l'inversion
n'est pas le maillon faible [MESURE].

### 5.2 La famille primaire : qui est signale a 5 pour cent

[MESURE, `p` bilateral et `p` de Holm sur les 27 tests preenregistres, `i3-puissance.csv`]

Trois couples seulement passent la correction :

| source | statistique | `p` bilateral | `p` de Holm |
|---|---|---|---|
| `agents v8` | C | 4,3e-10 | **1,1e-8** |
| `C2` | C | 1,3e-12 | **3,4e-11** |
| `C2` | A | 6,9e-7 | **1,7e-5** |
| `agents v8` | A | 7,1e-6 | **1,7e-4** |
| `agents v8` | B | 1,7e-5 | **3,9e-4** |
| **`B0 segment`** | **B** | 0,00156 | **0,0343** |
| `agents demographiques (v6)` | B | 0,0179 | 0,337, non retenu |
| `C3` | A | 0,0133 | 0,280, non retenu |
| toutes les autres | | > 0,02 | non retenu |

**A 5 pour cent de contamination et sous une correction honnete, le detecteur signale les deux
agents a etiquette ideologique et l'adversaire nul, et rien d'autre.** L'agent riche, l'agent
a demographies, les trois imputations et l'agent local sans etiquette passent.

### 5.3 Au dela de 5 pour cent, correction de Benjamini Hochberg dans la source

[MESURE, ecart E5, 12 tests par source, `p` bilateral recorrige]

**A 10 pour cent**, sont signalees : `agents v8`, `agents demographiques (v6)`, `C2`, `C3`,
`agents composite` (`p` BH 0,019 sur A et 0,0033 sur B), `IM m=10` (0,0091 sur A et 0,00041
sur C) et `B0 segment` (0,00077 sur A, moins de 1e-5 sur B). **Ne le sont pas : `PMM k=10`
(0,107 au mieux) et `E2` (0,253 au mieux).**

**A 25 pour cent**, les neuf sources sont signalees sans exception, `p` BH au plus 0,0219.
**A 50 pour cent** aussi, `p` BH au plus 0,0213.

**Le controle de fausse alarme.** `humains vague 2` n'est jamais signale a 5, 10 ni 25 pour
cent, sur aucune des trois statistiques ; a 50 pour cent la puissance empirique de A vaut
0,65, en dessous du seuil de 80 pour cent, et `tau*` vaut 95,5 pour cent. **Melanger a parts
egales deux vagues d'un panel humain reel ne declenche pas le detecteur** [MESURE].

---

## 6. Quantification, et l'aveugle

### 6.1 Calibration propre : le cas favorable, qui n'existe pas en audit

[MESURE, `i3-quantification.csv`, erreur absolue mediane sur 20 tirages, en points de taux]

| source evaluee | statistique | 5 % | 10 % | 25 % | 50 % |
|---|---|---|---|---|---|
| `agents v8` | A | 0,009 | 0,008 | 0,011 | 0,010 |
| `agents v8` | C | 0,020 | 0,014 | 0,011 | **0,004** |
| `agents composite` | B | 0,008 | 0,013 | 0,016 | 0,011 |
| `agents demographiques (v6)` | A | 0,010 | 0,009 | 0,013 | 0,010 |
| `PMM k=10` | B | 0,008 | 0,010 | 0,010 | **0,028** |
| `PMM k=10` | A | 0,025 | 0,043 | 0,038 | **0,071** |
| `PMM k=10` | C | 0,033 | 0,070 | 0,054 | **0,097** |
| `E2 regression contexte tirage` | B | 0,009 | 0,016 | 0,015 | 0,021 |
| `B0 segment` | B | 0,003 | 0,006 | 0,006 | 0,008 |

**Quand on sait ce qu'on cherche, l'inversion de la courbe est excellente** : moins de 1,5
point pour toutes les conditions a modele de langage, et le taux estime median est a moins
d'un point du vrai, par exemple 0,500 pour un vrai 50 pour cent de v8 sur A. **Mais le cas
favorable n'existe pas** : un auditeur qui saurait deja quel modele a fabrique le flux n'aurait
pas besoin du detecteur.

### 6.2 Calibration croisee : ce qui se passe reellement

[MESURE, erreur absolue mediane moyennee sur les quatre taux, en points de taux]

| courbe de calibration | flux evalue | A | B | C |
|---|---|---|---|---|
| `agents v8` | `PMM k=10` | 0,203 | 0,189 | 0,216 |
| `PMM k=10` | `agents v8` | **0,631** | **0,481** | **0,775** |
| `agents v8` | `agents composite` | 0,158 | 0,143 | 0,194 |
| `agents composite` | `agents v8` | 0,324 | 0,277 | 0,465 |
| `agents v8` | `C2` | **0,006** | 0,027 | 0,012 |
| `agents demographiques (v6)` | `C3` | 0,016 | 0,022 | 0,059 |
| `PMM k=10` | `C2` | 0,659 | 0,223 | 0,925 |
| `B0 segment` | n'importe quelle source a modele | 0,225 | 0,225 | 0,225 |

**A l'interieur d'une famille, la calibration croisee marche** : la courbe de v8 estime le taux
de C2 a 0,6 point pres sur A, et celle de v6 estime C3 a 1,6 point. **Entre familles, elle
echoue completement** : 15 a 78 points d'erreur. Prediction P6, tenue.

### 6.3 L'aveugle : la calibration agnostique

C'est ce qu'un institut ferait : appliquer a tout la courbe moyenne des conditions a modele de
langage, faute de savoir laquelle. [MESURE, taux estime median]

| flux evalue, vrai taux 50 pour cent | A | B | C |
|---|---|---|---|
| `agents v8` | 0,432 | 0,379 | **0,476** |
| `agents demographiques (v6)` | 0,276 | 0,292 | 0,276 |
| `agents composite` | 0,197 | 0,207 | 0,136 |
| `IM m=10 mode des m` | 0,144 | 0,117 | 0,133 |
| `PMM k=10` | **0,071** | **0,110** | **0,049** |
| `E2 regression contexte tirage` | **0,000** | **0,000** | **0,000** |
| `B0 segment` | **0,000** | **0,000** | **0,000** |
| *`humains vague 2`, controle* | *0,032* | *0,024* | *0,000* |

**L'estimateur aveugle est un plancher, jamais une part.** Il retrouve son propre type a 2 a 12
points pres, il sous estime l'agent riche d'un facteur 2,5, l'imputation par appariement d'un
facteur 5 a 10, et il rend **exactement zero** pour les deux fabricants qui sont plus libres
que les humains. Une phrase de rapport d'audit ne peut donc pas s'ecrire « le flux contient
`x` pour cent de synthetique » ; elle peut s'ecrire « le flux contient au moins `x` pour cent
de synthetique **de type gabarit**, et cette borne ne dit rien du synthetique par tirage ».

Note utile pour un institut : sur le controle de vraies personnes, `humains vague 2`,
l'estimateur agnostique rend 0,0 a 3,2 pour cent quel que soit le taux de melange. **Le
plancher publie n'est pas gonfle par du bruit humain** [MESURE].

---

## 7. Les deux adversaires, et la borne

### 7.1 L'imputation par tirage

`PMM k=10` et `E2 regression contexte tirage` sont les adversaires competents de a35 : ils
recopient ou tirent des reponses reelles conditionnellement a 119 items de contexte, et a44
mesure qu'ils portent la personne, PMM a 59,6 pour cent du plancher humain sous permutation
intra segment contre 7 pour cent pour v8.

**La statistique de gabarit ne les voit pas**, ce qui etait la prediction P3 et elle tient :
`tau*` de la concentration vaut 52,6 pour cent pour PMM et 73,8 pour cent pour E2, sous Holm.
A 50 pour cent de contamination, la concentration passe de 0,02723 a 0,02958 pour PMM, soit
3,8 ecarts types, et **descend** a 0,0255 pour E2.

**Ce qui reste detectable est l'exces de correlation**, `tau*` de 21,9 pour cent pour PMM et
24,6 pour cent pour E2 sous Holm, 15,3 et 17,5 pour cent au seuil nominal, **et il l'est dans
deux directions opposees** : PMM tire l'exces vers le haut, 0,0422 a 0,0494, et E2 vers le bas,
0,0422 a 0,0352. **Le deficit de patrons vient en second**, 36,0 et 39,0 pour cent.

**Reponse a la question du brainstorm** : ce qui reste, c'est l'exces de correlation, pas le
deficit de patrons ; et la reponse a « le detecteur ne verrait que la fraude paresseuse » est
**oui a 5 pour cent, non a 25 pour cent**. A un quart du flux, les neuf fabricants sont
signales, l'imputation par tirage comprise.

### 7.2 L'adversaire nul : le faux repondant tire dans les marginales de son segment

C'est l'adversaire qui ne coute rien : il ne demande ni modele, ni appel, ni donnee au dela des
marges publiees d'un vrai sondage. Il a par construction les marginales exactes de chaque
segment.

**Il est invisible a un test unilateral cale sur les agents, et c'est le resultat de la
section.** A 50 pour cent de contamination, le deficit de patrons passe de moins 6,86 a
**moins 2,36 pour cent**, c'est a dire **vers zero**, et l'exces de correlation de 0,0422 a
**0,0163**, c'est a dire **vers le plancher de bruit**. Un detecteur qui n'alerte que quand le
flux est plus pauvre et plus couple que des humains ne le voit **jamais, a aucun taux**.

**En bilateral il est le troisieme fabricant le plus detectable des neuf**, `tau*` de
**6,4 pour cent** sur l'exces de correlation, devant l'agent a demographies et devant l'agent
riche, et il est l'une des trois lignes qui passent Holm a 5 pour cent [MESURE].

**La raison est le fait de a44 que ce rapport transforme en instrument** : de vraies personnes
ne sont pas libres. Elles ont **moins** de patrons distincts que leur propre nul, moins
6,9 pour cent, et **plus** de correlation residuelle, 0,042. Une population sans structure
individuelle a exactement zero sur les deux. **La signature humaine est une bande, pas un
demi axe**, et c'est la seule facon de detecter a la fois le gabarit et le tirage.

### 7.3 La borne, ecrite en clair

1. **Un flux fabrique par tirage dans les marginales de segment est detecte, mais seulement
   par un test bilateral, et le detecteur doit avoir ete construit pour cela.**
2. **Un fabricant qui viserait la valeur humaine des trois statistiques ne serait pas detecte
   du tout.** Rien dans ce rapport ne l'interdit, et il est constructible : il suffit de
   melanger un generateur trop pauvre et un generateur trop libre dans la proportion qui
   ramene A a moins 0,069 et B a 0,042. **C'est la limite theorique du dispositif et elle est
   atteignable par un adversaire qui a lu ce rapport.**
3. **En dessous de 5 pour cent, rien n'est detectable, pour aucun fabricant**, sur 1 052
   personnes et 149 items. Le meilleur `tau*` du tableau 5 vaut 1,9 pour cent, et il ne vaut
   que pour l'agent a etiquette ideologique.

---

## 8. I4, la polarisation mesuree contre le taux de contamination

[MESURE, `i3-polarisation.csv`. Definition preenregistree : ecart standardise des rangs entre
le bloc gauche et le bloc droite, moyenne sur les 149 items, signe aligne sur les humains purs.
Reference humaine 0,4505, IC bootstrap [0,4236 ; 0,4773], 400 tirages.]

| source | 5 % | 10 % | 25 % | 50 % | facteur a 50 % |
|---|---|---|---|---|---|
| **`agents v8`**, etiquette ideologique | 0,4860 | 0,5170 | 0,6204 | **0,7930** | **1,760** |
| `agents composite`, riche | 0,4598 | 0,4694 | 0,4970 | 0,5454 | 1,211 |
| `PMM k=10`, tirage | 0,4544 | 0,4582 | 0,4704 | 0,4884 | 1,084 |
| `IM m=10`, esperance | 0,4535 | 0,4558 | 0,4681 | 0,4864 | 1,080 |
| `B0 segment`, adversaire nul | 0,4490 | 0,4504 | 0,4513 | 0,4478 | 0,994 |
| `E2 regression`, tirage | 0,4489 | 0,4473 | 0,4430 | 0,4373 | 0,971 |
| **`agents demographiques (v6)`**, sans ideologie | 0,4392 | 0,4294 | 0,3986 | **0,3514** | **0,780** |
| `C2`, etiquette, local | 0,4612 | 0,4709 | sans objet | sans objet | 1,045 a 10 % |
| `C3`, sans etiquette, local | 0,4402 | 0,4298 | sans objet | sans objet | 0,954 a 10 % |
| *`humains vague 2`, controle* | *0,4506* | *0,4498* | *0,4492* | *0,4494* | *0,998* |

**La prediction P7 est fausse et sa correction est le resultat.** Le signe ne se lit pas sur
gabarit contre tirage : les deux imputations par tirage donnent 1,08 et 0,97, l'adversaire nul
donne 0,99, tous a l'interieur ou au bord de la bande humaine. **Le signe se lit sur
l'etiquette ideologique recue ou non.** Les deux conditions qui l'ont recue gonflent,
`agents v8` a 1,76 et `C2` a 1,045 des 10 pour cent ; les deux qui ne l'ont pas recue mais
recoivent quand meme un profil aplatissent, `agents v6` a 0,78 et `C3` a 0,954 ;
`agents composite`, qui recoit un entretien complet dont l'ideologie fait partie, gonfle
moderement, 1,21.

**C'est mot pour mot ce que `MODELE-DU-MONDE.md` section 4 pose comme variable
reconciliatrice**, « la variable qui reconcilie gonflement et aplatissement est le groupe nomme
ou non », et c'est la premiere fois qu'elle est mesuree **en fonction d'un taux de
contamination** et non entre conditions pures [MESURE ; l'accord avec a38 est une lecture,
PROBABLE].

**Ce que I4 autorise a ecrire.** Une contamination de 10 pour cent par un agent a etiquette
ideologique deplace la polarisation mesuree de 14,8 pour cent, ce qui est de l'ordre de
grandeur des hausses publiees sur une decennie. **Ce que I4 n'autorise pas a ecrire.** Que la
polarisation mesuree apres 2023 est gonflee : le mode de contamination reel, un humain qui
colle la question dans un assistant sans son identite, ressemble a `v6` ou a `C3`, donc au mode
**aplatissant**, et nous n'avons aucun echantillon reellement contamine. **La courbe est une
simulation, pas une mesure.**

---

## 9. La figure

`resultats/i3-figure-detecteur.png` et `.svg`, quatre panneaux, la meme liste de dix sources
dans le meme ordre sur les quatre. A, B, C : les trois statistiques contre le taux, avec le
trait tirete de la reference humaine et la bande grise de son IC a 95 pour cent. D : I4.

Ce que la figure montre et que les tableaux disent moins bien : **le faisceau rouge des agents
et le faisceau bleu des imputations se separent, et la ligne grise de l'adversaire nul part de
l'autre cote de la bande sur les deux premiers panneaux.** Sur le panneau C, une seule courbe
decolle vraiment, celle de l'agent a etiquette ideologique, et c'est la lecture visuelle du
mot « gabarit ». Sur le panneau D, deux courbes rouges partent en sens contraires, v8 vers le
haut et v6 vers le bas, ce qui est le resultat d'I4 en une image.

---

## 10. Ce que cela vaut pour un institut

**Mode d'emploi, une phrase.** Calculer sur le fichier livre les trois statistiques avec le
generateur nul du fichier lui meme, les comparer **en bilateral** a la bande d'un echantillon
humain de reference de meme taille et de meme questionnaire, et signaler le fichier des qu'une
des trois sort de la bande : sur nos donnees, cela attrape un agent a etiquette a partir de
2 pour cent, un agent riche a partir de 11 pour cent et une imputation par tirage a partir de
22 pour cent, sans jamais se declencher sur un panel humain reel melange a une autre vague.

**Limite, une phrase.** Le chiffre que le detecteur produit est un **plancher de contamination
de type gabarit** et non une part : sans connaitre le fabricant, l'estimateur sous evalue d'un
facteur 2,5 a 10 et rend zero pour les deux fabricants qui sont plus libres qu'une vraie
population, si bien qu'un « zero detecte » ne doit jamais etre lu comme « fichier propre ».

---

## 11. Ce que je n'ai pas pu verifier

1. **Aucun jeu reel a contamination documentee.** Toutes les courbes de ce rapport sont des
   simulations de contamination. Nous n'avons aucun fichier de sondage reellement contamine,
   ni son taux vrai. C'est la limite qui rend le rapport publiable comme methode et pas comme
   mesure.
2. **Une seule population humaine de reference, et c'est elle qui sert de fond.** Les 1 052
   personnes de la vague 1 du GSS sont a la fois le fond du flux, la reference du detecteur et
   la source des marginales de l'adversaire nul. Un institut aurait une reference externe,
   pas la meme population, et son `s_0` serait plus grand. **Tous les `tau*` de la section 5
   sont donc optimistes d'une quantite non mesuree.**
3. **Un seul questionnaire, une seule segmentation.** 149 items d'attitudes du GSS, ideologie
   politique a sept niveaux. Rien sur Twin-2K-500, rien sur les jeux de a6, aucune
   segmentation fine : a44 montre que `S_fin` vide le nul de son conditionnement sur ce
   perimetre, donc `S_ideo` est le seul choix defendable ici, mais la sensibilite du detecteur
   a la segmentation n'est pas mesuree.
4. **`C2` et `C3` ne vont pas au dela de 10 pour cent** et leurs `tau*` sont extrapoles sur
   trois points. Leur place dans le tableau 5 est indicative.
5. **La taille de flux n'est pas variee.** Tous les resultats sont a `N = 1 052`. Les trois
   statistiques dependent de l'effectif, `s_0` decroit en `racine(N)` et le nombre de patrons
   distincts sature ; **un flux de 300 personnes ou de 10 000 n'a pas les memes `tau*` et le
   rapport ne dit pas lesquels.** C'est le complement le moins cher a faire.
6. **Le taux de contamination est uniforme sur les segments.** Une fraude reelle serait
   concentree, par exemple tous les faux repondants d'un meme camp, ce qui rendrait le
   detecteur plus sensible sur un segment et aveugle ailleurs. Non teste.
7. **Le fabricant qui vise la valeur humaine n'a pas ete construit.** La section 7.3 point 2
   affirme qu'il est constructible ; c'est un raisonnement, pas une mesure [HYPOTHESE].
8. **La correction de Holm porte sur la famille a 5 pour cent seulement.** Les taux
   superieurs sont corriges par Benjamini Hochberg a l'interieur de leur source, une famille
   plus permissive ; aucun verdict du rapport ne repose sur eux seuls.
9. **`R = 40` replicats nuls par flux**, contre 200 pour la reference. Le controle 3 montre que
   le bruit du nul interieur vaut un dixieme du bruit d'echantillonnage, donc l'effet sur
   `s_0` est de l'ordre du demi pour cent, mais chaque point des courbes des sections 4 et 5
   porte cette incertitude et pas d'intervalle propre au dela de l'ecart type inter tirages
   publie dans `i3-melanges.csv`.
10. **La mesure de polarisation d'I4 est notre definition, pas celle de a38.** a38 emploie des
    scores de desirabilite sur 29 items a pole d'endogroupe declare ; i3 emploie un ecart
    standardise de rang sur les 149 items, signe aligne sur les humains. Les deux vont dans le
    meme sens pour v8, facteur 1,76 ici contre 1,62 en a38, mais **ce ne sont pas les memes
    nombres et il ne faut pas les confondre** [MESURE pour i3, la concordance etant une
    lecture, PROBABLE].
11. **Rien sur le texte libre.** L'etat de l'art de la detection de reponses generees passe par
    le texte ; ce rapport ne le compare pas au detecteur structurel et ne peut pas dire lequel
    est le meilleur, ni si les deux se combinent.

---

## 12. Questions ouvertes pour Simon

1. **Est ce que la bonne these d'I3 n'est pas la bande plutot que le seuil ?** Le resultat que
   je trouve le plus solide n'est pas « on detecte a 5 pour cent », qui depend du fabricant, du
   questionnaire et de l'effectif ; c'est que **la signature humaine est un intervalle a deux
   bords** : de vraies personnes ne sont ni aussi libres qu'un tirage sans structure, ni aussi
   pauvres qu'un agent. Deux fabricants sur neuf tombent du cote « trop libre », et un
   detecteur unilateral, qui est ce que tout le monde construirait apres a44, les rate
   integralement. Est ce que ce n'est pas cela, le titre ?
2. **Faut il publier `E2` comme le vrai adversaire, et non PMM ?** `E2`, la regression
   stochastique sur le contexte, a un deficit de patrons de moins 3,8 pour cent et un exces de
   correlation de 0,0275, c'est a dire **moins de structure que de vraies personnes**. C'est le
   fabricant le plus difficile des neuf, `tau*` de 24,6 pour cent, et c'est celui qui coute le
   moins cher a produire. PMM est plus connu mais moins dangereux.
3. **Que fait on du fait que le detecteur ne se declenche jamais sur `humains vague 2` ?**
   C'est une bonne nouvelle et une mauvaise : bonne parce que la specificite est excellente,
   mauvaise parce que cela veut dire que **les trois statistiques ne bougent pas avec le temps
   ni avec l'occasion de mesure**, donc qu'elles ne captent rien de ce qui fait la variabilite
   humaine reelle. Est ce un argument de robustesse ou l'aveu que le detecteur mesure une
   seule chose ?
4. **La quantification vaut elle la peine d'etre publiee ?** Elle est excellente en calibration
   propre, inutilisable en aveugle, et l'honnetete oblige a publier surtout la seconde. Un
   relecteur peut lire cela comme « l'estimateur ne marche pas ». Ma preference est de le
   presenter comme un **plancher borne**, avec le tableau 6.3 comme resultat principal et pas
   comme limite, mais c'est un choix de cadrage et il t'appartient.
5. **I4 devient il une section a lui seul, maintenant que la variable est l'etiquette et pas le
   mode de fabrication ?** Le fait mesure est plus fort que celui du brainstorm : une meme
   famille de fabricants deplace la polarisation dans les deux sens selon qu'on lui a nomme le
   camp, facteur 1,76 contre 0,78 a 50 pour cent. Cela relie I3, I4 et la section 4 de
   `MODELE-DU-MONDE.md` en un seul enonce.
6. **Le complement le moins cher est la variation d'effectif**, `N` de 300 a 5 000 par sous
   echantillonnage et par duplication de la population synthetique, pour donner a un institut
   l'abaque `tau*(N)` dont il a reellement besoin. Zero appel, environ une heure de calcul.
   Faut il le faire avant de montrer quoi que ce soit a un institut ?

---

## 13. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python analyses/i3_melanges.py
.venv/bin/python analyses/i3_figure.py
```

Duree mesuree : **1 480 secondes** pour `i3_melanges.py` sur quatre coeurs, dont 1 216 pour les
720 flux melanges, quelques secondes pour la figure. Les caches `/tmp/a25-matrices.pkl`,
`/tmp/a28-foret.npy` et `/tmp/a35-methodes.pkl` doivent exister ; ils sont produits par a25,
a28 et a35 et ne sont pas recalcules ici. Graine unique `20260909` partout. Un passage rapide
de verification est disponible par `--smoke`.

---

## 14. Fichiers produits

| fichier | contenu |
|---|---|
| `resultats/i3-preenregistrement.md` | le preenregistrement, horodate avant tout calcul, non modifie |
| `resultats/i3-controles.csv` | les cinq controles bloquants et les taux hors nomenclature, 38 lignes, toutes passees |
| `resultats/i3-reference-humaine.csv` | les trois statistiques sur le flux pur avec IC et `s_0`, 3 lignes |
| `resultats/i3-sources-pures.csv` | les neuf sources a taux 100 pour cent, controle de reproduction de a44, 9 lignes |
| `resultats/i3-melanges.csv` | les 720 flux, source x taux x tirage, toutes quantites, 721 lignes |
| `resultats/i3-puissance.csv` | `z`, `p`, `p` de Holm, puissance empirique et `tau*`, 108 lignes |
| `resultats/i3-quantification.csv` | l'estimateur du taux, calibrations propre, croisee et agnostique, 1 188 lignes |
| `resultats/i3-polarisation.csv` | I4, l'ecart gauche droite contre le taux, 37 lignes |
| `resultats/i3-figure-detecteur.png` et `.svg` | la figure a quatre panneaux |
| `analyses/i3_commun.py` | flux melanges, les trois statistiques, reechantillonnage, polarisation |
| `analyses/i3_melanges.py` | le run principal |
| `analyses/i3_figure.py` | la figure |
