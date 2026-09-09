# a29. Les minorites gardees sont elles les bonnes personnes ?

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 8 point 1 et revendication 6 : « une ablation propre » devient « un contraste de conditionnement ». Objection a45 numero 1, contradiction D1.

**Phrases d'origine.** Section 8 point 1 : « C2 contre C3 est **une ablation propre**, mais
sur un seul modele, un seul run, 150 personnes ». Revendication 6 : « A modele, personnes,
questions et traces constants, donner l'etiquette demographique fait passer la correlation
par personne de 0,410 a 0,194 [...] [MESURE, **ablation** C3 contre C2, la mesure la plus
propre du rapport] ».

**Correction.** Ecrire « un **contraste de conditionnement** dont les deux facteurs sont
confondus : C2 recoit onze attributs et aucune reponse de la personne, C3 recoit 119
reponses de la personne et aucune etiquette ». Le renversement 0,410 contre 0,194 est un
fait ; son attribution a l'etiquette seule ne l'est pas. Le chiffre reste, la cause devient
indeterminee entre les deux facteurs.

**Ce que les deux invites contiennent, mesure sur le code.**
[CONFIRME, `analyses/a5_agents_locaux_gss.py`, `systeme_c2` lignes 164 a 177 et `systeme_c3`
lignes 180 a 196]

| | contenu de l'invite systeme | etiquette ideologique | reponses de la personne |
|---|---|---|---|
| C2 | les **onze attributs** de `demographic_summary.csv`, et rien d'autre | oui, ligne `Political ideology` | **aucune** |
| C3 | les **environ 119 items de contexte**, question et reponse en clair | **non** | oui, toutes |

C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette : **ils echangent
integralement leur entree**. Le contraste melange deux changements, le retrait de l'etiquette
et le remplacement de la personne par onze attributs ; ses deux facteurs sont confondus et
aucun des textes du dossier ne les separe.

**Ce que le second facteur vaut a lui seul.** `B1 argmax` est une regression sur les memes
onze attributs, `B2 argmax` un plus proche voisin sur les memes 119 items **sans aucune
demographie** [CONFIRME, `a2_baselines_gss.py` lignes 178 et 188 : `enc.transform` n'alimente
que `B1`, `B2` ne voit que `codes[:, contexte]`]. A moteur statistique constant et sans
aucune ablation d'etiquette, le passage de l'un a l'autre deplace la chute sous permutation
de **0,175 a 0,357 du plancher humain**, un facteur 2,0 ; le passage de C2 a C3 vaut un
facteur 6,2 [MESURE, `a47-chute-deux-segmentations.csv`, segmentation `S_ideo`].

**L'ablation propre n'est pas dans ce dossier.** Elle est le run R3 de la nuit du 8 au
9 septembre : C3 plus etiquette contre C3, et C2 prive de la seule ligne `Political
ideology` contre C2. Tant qu'il n'a pas rendu, aucun texte ne doit ecrire « ablation de
l'etiquette » ni « seule l'etiquette bouge ».

---

Rapport du 8 septembre 2026. Il execute le premier travail demande apres l'arbitrage :
verifier la FIN de la phrase a defendre, « les methodes classiques simulent une societe
sans minorites ; les modeles de langage en gardent la moitie, mais pas les bonnes
personnes, et ils se trompent la ou les gens se surveillent » (`ARBITRAGE.md`). Le debut
de la phrase est etabli par `a8-baselines-durcies.md` section 6 et par
`a28-trois-tests-decisifs.md` section 3.4. La fin ne l'etait pas.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a29_commun.py`, `a29_mesures.py`, `a29_profils.py`, plus
`a29_figure.py`. **Aucun script existant n'a ete modifie** ; `a2_commun`,
`a2_baselines_gss`, `a5_evaluer`, `a5_agents_locaux_gss`, `a8_commun`, `a25_commun`,
`a25_mesures`, `a28_commun` et `a28_figures` sont importes tels quels, memes graines,
memes plis, memes 149 items, memes personnes. La foret aleatoire `B3 foret` est relue du
cache de a28, elle n'est pas redefinie.

Controle de protocole avant toute lecture : sur le perimetre 150 et au seuil de 10 pour
cent, les lignes de a28 se reproduisent au chiffre pres. `agents composite` 0,2544 de
rappel et 0,2554 de precision contre 0,254 et 0,255 en a28 ; `C3` 0,2195 et 0,1315 contre
0,220 et 0,132 ; `B3 foret` 0,0080 et 0,2069 contre 0,008 et 0,207 [MESURE]. Rien n'a
bouge dans la chaine.

Sorties : `a29-minorites-global.csv`, `a29-correlation-personne.csv`, `a29-par-item.csv`,
`a29-masse-item.csv`, `a29-items-sensibles.csv`, `a29-sensibles-bootstrap-items.csv`,
`a29-contrastes.csv`, `a29-contraste-de-groupe.csv`, `a29-profils-niveaux.csv`,
`a29-profils-correlation.csv`, `a29-profils-quintiles.csv`, `a29-profils-fidelite.csv`,
`a29-figure-minorites.png` et `.svg`.

---

## Reponse en une ligne

**La fin de la phrase tient EN PARTIE, et la partie qui tombe est celle qui la rendait
postable.** Les agents riches de Stanford ne distribuent pas la rarete au hasard : la
correlation par personne entre nombre de reponses rares reelles et nombre de reponses
rares predites vaut **0,531 [0,485 ; 0,575] pour `agents composite`, soit 73 pour cent du
plafond humain de 0,732**, quand le temoin qui met la bonne masse aux mauvais endroits,
`B0 tirage`, est a **moins 0,019 [moins 0,078 ; 0,041]**, c'est a dire zero
[MESURE, `a29-correlation-personne.csv`]. **Ecrire « pas les bonnes personnes » sans
qualificatif est faux pour les deux conditions riches.** Ce qui reste vrai, et qui est le
resultat a defendre : **la bonne personne recoit la mauvaise minorite**. Quand
`agents composite` ose une modalite minoritaire, **61,6 pour cent du temps la personne a
en fait donne une reponse majoritaire sur cet item**, contre 41,4 pour cent pour les memes
humains reinterroges ; sa precision est 0,323 contre 0,531, difference moins 0,207
[moins 0,226 ; moins 0,189], p ajuste par Holm 0,013 sur une famille de 26 tests declaree
avant execution [MESURE, `a29-contrastes.csv`]. Et **la fin de la phrase est fausse pour
nos propres agents dans l'autre sens que celui qu'on croyait** : C2, avec etiquette, est a
0,194 de correlation, 30 pour cent du plafond, quand C3, sans aucune etiquette, est a
0,410, 63 pour cent du plafond. **L'etiquette demographique degrade l'attribution des
rares aux bonnes personnes.**

Une phrase de rechange, defendable telle quelle : **« la statistique ne produit pas de
minorites ; les modeles de langage en produisent au bon taux, et ils visent les bonnes
personnes a trois quarts du plafond humain, mais ils leur attribuent la mauvaise opinion
minoritaire trois fois sur cinq »**.

---

## 0. Le protocole, ecrit avant les resultats

La famille est recopiee sans retouche de l'entete de `analyses/a29_mesures.py`, ou elle a
ete ecrite avant l'execution. La seule verification possible pour un tiers est la lecture
de la docstring, qui n'a pas ete modifiee apres coup.

**Perimetre declare** : le perimetre naturel de chaque methode, soit les 1 052 personnes
pour les onze methodes qui les couvrent, et les 150 personnes du run local pour C2 et C3,
avec la reference de minorite calculee sur ces 150 personnes. **Seuil declare** : 10 pour
cent.

| | enonce | nombre de tests |
|---|---|---|
| **H1** primaire | pour chacune des 13 methodes non humaines, la precision sur les cellules minoritaires est inferieure a celle des memes humains reinterroges | 13 |
| **H2** primaire | pour chacune des 13 methodes, la correlation par personne entre taux de rares reelles et taux de rares predites est inferieure a celle des memes humains reinterroges | 13 |
| **H3** secondaire | pour chacune des 13 methodes, cette correlation par personne est strictement positive | 13 |
| **H4** secondaire | pour chacune des 13 methodes, le rappel minoritaire sur les 12 items sensibles au mode de NORC differe de celui des 65 temoins, bilateral | 13 |

**Famille primaire : H1 union H2, 26 tests. Famille secondaire : H3 union H4, 26 tests.**
Correction principale sur chaque famille : **Holm**, valide sans hypothese sur la
dependance, ce qui est necessaire puisque les contrastes portent sur les memes personnes
et les memes items. Correction secondaire rapportee a cote : **Benjamini Hochberg**.
Tous les p sont des p de bootstrap apparie sur les personnes, 2 000 tirages, lus sur la
position de zero dans la distribution ; ils ne descendent jamais sous 1/2 000 = 0,0005.

**N'entrent pas dans les familles**, et sont rapportes comme des descriptions : le seuil
de 20 pour cent, robustesse ; le perimetre 150 pour les onze methodes qui disposent du
1 052, echantillon emboite ; le F1, le taux de fausses minorites et la masse predite, qui
se deduisent des quantites testees ; la correlation par item entre masse humaine et masse
predite ; les contrastes de groupe entre les huit conditions a modele de langage et les
cinq predicteurs statistiques, ajoutes apres coup et signales comme tels ; le bootstrap
sur les items de la section 4, ajoute apres avoir vu que le bootstrap sur les personnes
etait insuffisant ; toute la section 3, descriptive de bout en bout.

**Deux tests de la famille primaire sont non evaluables** et recoivent p = 1 : `B0 mode`
ne predit jamais une modalite minoritaire, sa precision et sa correlation ne sont pas
definies. Le choix de p = 1 est conservateur : il ne peut pas creer de fausse decouverte
et il n'allege pas la correction appliquee aux douze autres methodes.

**Definitions.** Une modalite est minoritaire si moins de 10 pour cent, puis moins de 20
pour cent, des repondants observes de l'item l'ont choisie ; c'est la definition de a8
section 6, importee et non recopiee. **Rappel** : part des cellules a reponse minoritaire
reelle qui sont bien predites. **Precision** : part des cellules justes parmi celles ou la
methode predit une modalite minoritaire. **Taux de fausses minorites** : part, parmi les
cellules ou la methode predit une modalite minoritaire, de celles ou la personne a en
realite donne une modalite **majoritaire**. **Taux de mauvaise minorite** : meme
denominateur, cellules ou la personne a bien donne une reponse rare, mais une autre. Les
trois font 1 par construction. Une cellule est evaluable des que la vraie reponse de la
vague 1 est observee ; une prediction refusee compte comme non minoritaire, convention la
plus severe, et le taux de refus est rapporte, au plus 0,20 pour cent.

Au seuil de 10 pour cent, **70 items sur 149 portent au moins une modalite minoritaire**,
5 709 cellules sur 156 748 sur le perimetre 1 052, masse humaine 3,64 pour cent.

---

## 1. Rappel et precision : garder la masse ne dit pas viser juste

[MESURE, `a29-minorites-global.csv`, perimetre 1 052, seuil 10 pour cent, 2 000 tirages
bootstrap sur les personnes]

| condition | rappel | precision | **F1** | fausses minorites | mauvaise minorite | masse predite |
|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***0,5483*** | ***0,5306*** | ***0,5393*** | ***0,414*** | ***0,055*** | ***3,76 %*** |
| agents composite | 0,3069 | 0,3232 | **0,3149** | 0,616 | 0,061 | 3,46 % |
| agents entretien (v3) | 0,2953 | 0,2903 | 0,2928 | 0,652 | 0,058 | 3,71 % |
| agents enquete | 0,2305 | 0,2333 | 0,2319 | 0,703 | 0,064 | 3,60 % |
| agents demographiques (v6) | 0,1624 | 0,3592 | 0,2236 | 0,576 | 0,065 | 1,65 % |
| agents v8 | 0,1717 | 0,1483 | 0,1591 | 0,827 | 0,025 | 4,22 % |
| **B1 argmax** | 0,0580 | 0,2213 | 0,0919 | 0,683 | 0,096 | 0,95 % |
| agents v7 | 0,0673 | 0,1307 | 0,0888 | 0,814 | 0,056 | 1,87 % |
| **B0 tirage** | 0,0617 | 0,0618 | 0,0617 | **0,885** | 0,053 | **3,64 %** |
| **B2 argmax** | 0,0357 | **0,4892** | 0,0666 | **0,365** | 0,146 | 0,27 % |
| **B3 foret** | 0,0144 | 0,3961 | 0,0277 | 0,459 | 0,145 | 0,13 % |
| B0 mode | 0,0000 | sans objet | 0,0000 | sans objet | sans objet | 0,00 % |

Sur les 150 personnes du run local, memes references restreintes, la meme table donne
`C2` a 0,1285 de rappel et 0,0994 de precision, `C3` a 0,2195 et 0,1315, contre 0,4739 et
0,4481 pour les memes humains reinterroges [MESURE].

**Ce que la colonne precision ajoute au rappel de a28.**

1. **Le classement change de tete selon la colonne** [MESURE]. Sur le rappel, `B2 argmax`
   est douzieme de treize ; sur la precision, elle est **premiere des non humaines, a
   0,4892, a 4,1 points du plafond humain, le seul contraste de H1 qui ne passe pas la
   correction**, p ajuste par Holm 0,351 [MESURE, `a29-contrastes.csv`]. La foret
   aleatoire, derniere de treize sur le rappel a 0,0144, est **quatrieme sur la
   precision a 0,3961**. La signature de l'ecrasement, vue des queues, n'est pas de se
   tromper : c'est de ne presque jamais oser.
2. **Le F1 remet l'ordre de a28 en place et le rend defendable** [MESURE]. Il combine les
   deux colonnes et il n'est pas gagnable par l'abstention : `agents composite` 0,3149,
   `B1 argmax` 0,0919, `B2 argmax` 0,0666, `B3 foret` 0,0277. **Le facteur 32 de a28 sur
   le rappel devient un facteur 11,4 sur le F1 entre la meilleure condition a modele de
   langage et la foret**, et un facteur 3,4 contre `B1 argmax`. Le fait tient, l'ampleur
   se degonfle nettement. C'est le premier chiffre desagreable de ce rapport.
3. **Le taux de fausses minorites est la mesure la plus lisible du defaut** [MESURE].
   Quand `agents composite` ose une modalite rare, **61,6 pour cent du temps la personne
   est en fait majoritaire sur l'item** ; les humains reinterroges sont a 41,4 pour cent,
   `B0 tirage` a 88,5 pour cent, `B2 argmax` a 36,5 pour cent. Les agents sont a mi chemin
   entre le hasard et l'humain, et **au dessus du niveau de la regression logistique**,
   qui est a 68,3 pour cent mais qui n'ose presque jamais.
4. **Se tromper de minorite est rare partout** [MESURE]. Le taux de mauvaise minorite est
   de 2,5 a 9,6 pour cent chez les conditions a modele de langage et chez `B0`, `B1`. Il
   monte a 14,6 et 14,5 pour cent chez `B2 argmax` et la foret, ce qui est coherent avec
   leur precision haute et leur masse minuscule. **L'erreur type n'est pas « la mauvaise
   opinion rare », c'est « la bonne opinion rare a la mauvaise personne ».**
5. **Robustesse au seuil de 20 pour cent** [MESURE, hors famille]. Meme ordre, meme
   lecture, ecarts resserres : `agents composite` 0,3554 de rappel et 0,4078 de precision,
   F1 0,3798 ; humains 0,6058, 0,6023 et 0,6040 ; `B3 foret` F1 0,0879. Le rapport de F1
   entre la meilleure condition et la foret passe de 11,4 a 4,3.

**H1 : onze des treize contrastes passent Holm** a p ajuste 0,013. Les deux qui echouent
sont `B0 mode`, non evaluable, et **`B2 argmax`, a p ajuste 0,351 : rien ne permet de dire
que sa precision est sous celle des humains** [MESURE, `a29-contrastes.csv`]. C'est le seul
echec informatif de la famille primaire.

---

## 2. Le niveau population contre le niveau personne

C'est le coeur du rapport. Les deux niveaux se contredisent, et le temoin le montre sans
discussion.

### 2.1 Au niveau de la population, item par item, presque tout le monde est bon

[MESURE, `a29-masse-item.csv`, perimetre 1 052, seuil 10 pour cent, 149 items]

| condition | correlation de rang entre masse humaine et masse predite, par item | rapport de masse totale | items a masse predite nulle sur 149 |
|---|---|---|---|
| **B0 tirage** | **0,9966** | 0,998 | 79 |
| humains vague 2 | 0,9951 | 1,033 | 79 |
| B1 argmax | 0,9543 | 0,262 | 85 |
| agents entretien (v3) | 0,9241 | 1,017 | 80 |
| agents composite | 0,9106 | 0,949 | 80 |
| agents enquete | 0,8804 | 0,988 | 82 |
| agents v7 | 0,8747 | 0,515 | 83 |
| agents v8 | 0,8089 | 1,158 | 91 |
| agents demographiques (v6) | 0,7726 | 0,452 | 98 |
| B2 argmax | 0,5795 | 0,073 | 124 |
| **B3 foret** | **0,4119** | **0,036** | **137** |

**La ligne qui interdit de conclure au niveau population** : `B0 tirage`, qui tire dans la
marginale de chaque item sans rien savoir de personne, obtient **0,9966**, la meilleure
correlation par item du tableau, humains compris, et reproduit **99,8 pour cent** de la
masse minoritaire. Cette methode ne sait pas qui est qui. **Une bonne correlation de masse
par item ne dit strictement rien sur les personnes**, et c'est exactement le piege signale
dans a8 section 6.3 point 4, ici mesure au lieu d'etre annonce.

### 2.2 Au niveau de la personne, le classement se separe en trois

[MESURE, `a29-correlation-personne.csv`, correlation de rang de Spearman entre le taux de
reponses rares reelles et le taux de reponses rares predites, une valeur par personne,
2 000 tirages bootstrap sur les personnes, perimetre 1 052, seuil 10 pour cent]

| condition | rho | IC 95 % | part du plafond humain | temoin de permutation |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,7320*** | ***[0,696 ; 0,763]*** | ***1,00*** | ***moins 0,000*** |
| agents composite | **0,5313** | [0,485 ; 0,575] | **0,73** | moins 0,002 |
| agents enquete | 0,5041 | [0,455 ; 0,552] | 0,69 | moins 0,002 |
| agents entretien (v3) | 0,3908 | [0,335 ; 0,446] | 0,53 | 0,001 |
| agents demographiques (v6) | 0,3355 | [0,281 ; 0,387] | 0,46 | 0,000 |
| **B2 argmax** | **0,3003** | [0,243 ; 0,355] | **0,41** | 0,002 |
| **B1 argmax** | 0,2198 | [0,162 ; 0,279] | 0,30 | 0,002 |
| agents v8 | 0,2130 | [0,154 ; 0,274] | 0,29 | moins 0,003 |
| **B3 foret** | 0,1050 | [0,051 ; 0,162] | 0,14 | 0,003 |
| agents v7 | 0,0872 | [0,023 ; 0,146] | 0,12 | 0,003 |
| **B0 tirage** | **moins 0,0191** | **[moins 0,078 ; 0,041]** | **moins 0,03** | moins 0,000 |
| B0 mode | non definie | | | |

Sur les 150 personnes du run local, memes references restreintes : humains 0,6541
[0,529 ; 0,762], `agents composite` 0,5231 [0,394 ; 0,640], **`C3` 0,4098
[0,260 ; 0,541]**, **`C2` 0,1938 [0,047 ; 0,348]**, `B2 argmax` 0,2442 [0,082 ; 0,394],
`B3 foret` 0,0428 [moins 0,121 ; 0,213] [MESURE].

Le **contraste de groupe post hoc**, hors famille declaree, ne tranche pas : 0,344 de
correlation moyenne pour les six conditions a modele de langage du perimetre 1 052 contre
0,152 pour les cinq predicteurs statistiques, difference 0,192, p de permutation des
etiquettes de methode 0,111 ; sur les 150 personnes, 0,311 contre 0,137, p 0,070
[MESURE, `a29-contraste-de-groupe.csv`]. **La separation nette est entre conditions riches
et conditions pauvres, pas entre langage et statistique** : `B2 argmax` a 0,300 depasse
`agents v8` a 0,213 et `agents v7` a 0,087.

Le **temoin de permutation** permute, item par item, les predictions entre les personnes
evaluables, 200 permutations. Il conserve exactement la masse minoritaire de chaque item
et detruit l'appariement personne par personne. Il vaut zero a trois millemes pres pour
les treize conditions, avec un 97,5e percentile compris entre 0,050 et 0,068 sur les
1 052, et entre 0,140 et 0,198 sur les 150. **Toute valeur au dessus de ces bornes est de
l'appariement individuel, pas de la structure d'items.**

**Ce que ce tableau etablit.**

1. **La phrase « pas les bonnes personnes » est fausse pour les conditions riches**
   [MESURE]. `agents composite` et `agents enquete` sont a 73 et 69 pour cent du plafond
   humain, intervalles nettement au dessus du temoin. Un institut d'etudes qui achete une
   segmentation par propension a l'opinion minoritaire obtiendrait avec eux les trois
   quarts du signal qu'un panel de reinterrogation lui donnerait.
2. **Elle est vraie pour les conditions pauvres et pour nos agents locaux avec etiquette**
   [MESURE]. `agents v7` a 0,087 et `C2` a 0,194 sont a un et trois deciles du plafond, et
   l'intervalle de `C2`, [0,047 ; 0,348], descend sous le 97,5e percentile du temoin de
   permutation du meme perimetre, 0,177.
3. **H2 passe pour douze methodes sur treize**, p ajuste par Holm 0,013 pour onze et 0,020
   pour C3, `B0 mode` non evaluable. **Aucune methode n'atteint le plafond humain**, ce qui
   est le seul enonce que la famille primaire autorise sans reserve [MESURE].
4. **H3 : neuf methodes sur treize ont une correlation strictement positive apres Holm**
   [MESURE]. Les quatre qui echouent sont `B0 mode`, non evaluable, `B0 tirage`, p 0,570,
   et, de peu, `agents v7` a p ajuste 0,091 et `C2` a 0,120. **Les methodes dont on ne peut
   pas dire qu'elles distribuent la rarete autrement qu'au hasard entre les gens sont un
   tirage aveugle et notre propre agent a etiquette.**
5. **Le chiffre le plus desagreable du rapport** [MESURE]. **`C2`, notre agent avec onze
   attributs demographiques, est a 0,194 ; `C3`, le meme modele sans aucune etiquette, est
   a 0,410.** Meme modele, memes personnes, memes questions, memes traces. L'ecart va dans
   le sens inverse de l'intuition et **il rejoint le r de 0,246 contre 0,673 de la deviance
   au mode de segment mesuree en a23 section 3.7 sur les memes deux conditions**. Deux
   mesures independantes, la deviance et la rarete, disent la meme chose : **donner
   l'etiquette a ce modele detruit l'appariement individuel.**

### 2.3 La calibration par personne, en cinq classes

[MESURE, `a29-profils-quintiles.csv`, perimetre 1 052, quintiles des 1 052 personnes par
taux de reponses rares reelles, taux moyens]

| quintile | taux reel | humains vague 2 | composite | enquete | v8 | B1 | B2 | B3 foret | B0 tirage |
|---|---|---|---|---|---|---|---|---|---|
| 1, les moins rares | 0,0101 | 0,0171 | 0,0172 | 0,0192 | 0,0303 | 0,0064 | 0,0008 | 0,0008 | 0,0371 |
| 2 | 0,0201 | 0,0252 | 0,0234 | 0,0257 | 0,0302 | 0,0071 | 0,0011 | 0,0009 | 0,0356 |
| 3 | 0,0298 | 0,0310 | 0,0305 | 0,0305 | 0,0396 | 0,0092 | 0,0020 | 0,0014 | 0,0367 |
| 4 | 0,0434 | 0,0429 | 0,0373 | 0,0383 | 0,0486 | 0,0112 | 0,0022 | 0,0017 | 0,0355 |
| 5, les plus rares | 0,0717 | 0,0668 | 0,0595 | 0,0619 | 0,0578 | 0,0129 | 0,0065 | 0,0016 | 0,0366 |
| rapport 5 sur 1 | **7,1** | **3,9** | **3,5** | **3,2** | **1,9** | **2,0** | **8,5** | **2,0** | **0,99** |

`B0 tirage` est plat, 0,036 partout : c'est la lecture directe du temoin. `B3 foret` est
plate aussi, a 0,001. **Les agents riches suivent la pente reelle mais l'ecrasent : le
quintile le plus rare recoit 0,0595 au lieu de 0,0717, et le moins rare 0,0172 au lieu de
0,0101.** Les humains reinterroges ecrasent deja la pente de 7,1 a 3,9, ce qui rappelle
qu'une part de la pente reelle est du bruit de mesure.

---

## 3. Qui sont les personnes minoritaires, et qui chaque methode designe

**Section entierement descriptive.** Aucun p, aucune correction : les comparaisons
possibles se comptent en centaines, six axes fois quatorze conditions, et aucune n'a ete
declaree avant de voir les chiffres. Les intervalles sont des bootstraps sur les
personnes, ils bornent une moyenne, ils ne testent rien.

### 3.1 La vraie personne minoritaire est un homme d'extreme droite, jeune, peu diplome

[MESURE, `a29-profils-niveaux.csv`, perimetre 1 052, taux de reponses rares reelles]

| axe | niveau le plus rare | taux | niveau le moins rare | taux | rapport |
|---|---|---|---|---|---|
| ideologie | extremement conservateur (61 pers.) | 0,0608 [0,054 ; 0,069] | liberal (200) | 0,0313 [0,028 ; 0,034] | **1,94** |
| profil croise | homme, autre, droite (13) | 0,0609 [0,047 ; 0,074] | femme, autre, centre (22) | 0,0238 | **2,56** |
| education | moins que le secondaire (24) | 0,0422 [0,036 ; 0,049] | secondaire (409) | 0,0351 | 1,20 |
| age | 25 a 34 ans (146) | 0,0407 [0,037 ; 0,045] | 75 ans et plus (30) | 0,0313 | 1,30 |
| genre | homme (459) | 0,0394 [0,037 ; 0,042] | femme (593) | 0,0341 | 1,16 |
| race | noir (150) | 0,0384 [0,035 ; 0,042] | blanc (799) | 0,0360 | 1,07 |

**Un seul axe porte quelque chose, et c'est encore l'ideologie** [MESURE]. Sur les cinq
autres, l'ecart est inferieur a 1,3 et les intervalles se chevauchent presque tous. C'est
la troisieme confirmation independante, apres a1 et a23, que **l'ideologie est le seul axe
du dossier qui separe**, et c'est aussi une limite : cet axe est une attitude declaree,
pas une donnee demographique.

**La personne qui donne beaucoup de reponses rares est moins fidele a elle meme.** La
correlation de rang entre le taux de reponses rares et la fidelite test retest a deux
semaines vaut **moins 0,321** sur les 1 052 personnes, et les memes humains reinterroges
la reproduisent a **moins 0,348** [MESURE, `a29-profils-fidelite.csv`]. La fidelite passe
de 0,825 dans le quintile le moins rare a 0,750 dans le plus rare. **Une partie de ce
qu'on appelle une minorite d'opinion est de l'instabilite de reponse**, et il faut le dire
avant qu'un relecteur le dise. Aucune methode ne reproduit ce lien : `agents composite`
est a moins 0,103, `B2 argmax` a plus 0,041, `B3 foret` a plus 0,002 [MESURE].

### 3.2 Toutes les methodes exagerent le stereotype ideologique, et les statistiques le plus

[MESURE, `a29-profils-correlation.csv`, perimetre 1 052, axe ideologie, sept niveaux]

| condition | rapport entre le niveau le plus rare et le moins rare | correlation de rang avec le profil reel | niveau designe comme le plus rare |
|---|---|---|---|
| *reel, vague 1* | *1,94* | *1,00* | *extremement conservateur* |
| humains vague 2 | 1,90 | 0,893 | extremement conservateur |
| agents demographiques (v6) | 1,55 | 0,857 | extremement conservateur |
| agents v7 | 1,68 | moins 0,036 | extremement conservateur |
| agents enquete | 3,69 | 0,821 | extremement conservateur |
| agents entretien (v3) | 4,07 | 0,821 | extremement conservateur |
| agents composite | **4,18** | 0,893 | extremement conservateur |
| **B1 argmax** | 4,85 | 0,571 | extremement conservateur |
| **B2 argmax** | **9,34** | 0,786 | extremement conservateur |
| **B3 foret** | **12,84** | 0,000 | extremement conservateur |
| agents v8 | **14,82** | 0,607 | extremement conservateur |
| B0 tirage | 1,09 | 0,500 | legerement conservateur |

**Les treize methodes designent le meme profil que la realite, et toutes l'exagerent**
[MESURE]. Les humains reinterroges reproduisent le rapport reel a 2 pour cent pres, 1,90
contre 1,94. Les agents riches le doublent, 3,7 a 4,2. **La regression logistique le
multiplie par 2,5, la foret aleatoire par 6,6 et `agents v8` par 7,6.** En clair,
`agents v8` attribue une reponse rare a 13,5 pour cent des cellules des extremement
conservateurs et a 0,9 pour cent de celles des legerement liberaux, la ou la realite dit
6,1 et 3,3 pour cent.

**Conclusion, et elle est desagreable pour la these** : le stereotype de la personne
marginale existe, il est reel dans sa direction et faux dans son amplitude, et **ce n'est
pas une propriete du langage**. Les deux methodes qui l'exagerent le plus sont une foret
aleatoire et une regression logistique, exactement comme en a28 section 3.2 pour le
stereotype de segment. **C'est une propriete du fait de disposer de l'etiquette
ideologique**, pas du modele de langage.

**Sur l'axe age, en revanche, les conditions a modele de langage inversent le profil**
[MESURE]. La rarete reelle decroit avec l'age, de 0,0384 chez les 18 a 24 ans a 0,0313
chez les 75 ans et plus ; les humains reinterroges reproduisent la decroissance,
correlation de rang plus 0,893. `agents composite` est a moins 0,357, `agents entretien` a
moins 0,857 et `agents v8` a moins 0,964 : ils font **croitre** la rarete avec l'age,
jusqu'a 0,0492 chez les 75 ans et plus pour `agents v8`. **Le vieux excentrique est un
stereotype de modele de langage, et il n'est pas dans les donnees.** L'avertissement
d'usage vaut : sept niveaux, une correlation de rang sur sept points, aucun test declare.

---

## 4. Les minorites sur les items ou les gens se surveillent

Douze items sur 149 sont classes « likely mode sensitive » par NORC, 65 sont des temoins,
memes listes et meme correspondance que a25 et a28. Au seuil de 10 pour cent, les items
sensibles portent **724 cellules minoritaires sur 12 624, masse humaine 5,74 pour cent**,
contre **2 153 sur 68 380, masse humaine 3,15 pour cent** pour les temoins [MESURE]. **La
masse minoritaire est presque deux fois plus forte sur les items sensibles**, ce qui est
en soi un resultat descriptif interessant et un piege de comparaison.

Le plafond humain, lui, ne differe pas : rappel 0,5483 sur les sensibles contre 0,5574 sur
les temoins, difference moins 0,009 [MESURE]. **Le contraste n'est donc pas un artefact de
difficulte du jeu d'items du cote humain.**

[MESURE, `a29-items-sensibles.csv` et `a29-contrastes.csv`, perimetre 1 052, seuil 10 %]

| condition | rappel sensibles | rappel temoins | difference | IC personnes | p Holm | IC items |
|---|---|---|---|---|---|---|
| humains vague 2 | 0,5483 | 0,5574 | moins 0,009 | | hors famille | [moins 0,130 ; 0,069] |
| agents composite | 0,3715 | 0,3929 | moins 0,021 | [moins 0,058 ; 0,017] | 1,000 | [moins 0,234 ; 0,198] |
| agents entretien (v3) | 0,3398 | 0,3771 | moins 0,037 | [moins 0,075 ; moins 0,000] | 0,506 | [moins 0,287 ; 0,196] |
| **agents enquete** | 0,1699 | 0,2712 | **moins 0,101** | [moins 0,131 ; moins 0,073] | **0,013** | [moins 0,247 ; 0,049] |
| agents demographiques (v6) | 0,0884 | 0,0697 | plus 0,019 | [moins 0,005 ; 0,042] | 1,000 | [moins 0,100 ; 0,095] |
| agents v7 | 0,0898 | 0,0841 | plus 0,006 | [moins 0,016 ; 0,028] | 1,000 | [moins 0,077 ; 0,117] |
| agents v8 | 0,2044 | 0,1918 | plus 0,013 | [moins 0,017 ; 0,042] | 1,000 | [moins 0,168 ; 0,254] |
| **B1 argmax** | 0,1008 | 0,0474 | **plus 0,054** | [0,031 ; 0,076] | **0,013** | [moins 0,040 ; 0,208] |
| **B2 argmax** | 0,0856 | 0,0362 | **plus 0,049** | [0,028 ; 0,072] | **0,013** | [moins 0,036 ; 0,108] |
| **B3 foret** | 0,0552 | 0,0056 | **plus 0,050** | [0,033 ; 0,067] | **0,013** | [moins 0,013 ; 0,206] |
| B0 tirage | 0,0677 | 0,0641 | plus 0,004 | [moins 0,017 ; 0,024] | 1,000 | [moins 0,016 ; 0,027] |

Sur les 150 personnes, `C2` est a moins 0,032 et `C3` a moins 0,071, ni l'un ni l'autre ne
passant la correction [MESURE].

**Trois lectures, dont la derniere annule les deux premieres.**

1. **Lu au bootstrap sur les personnes, le signe est l'inverse de la these** [MESURE].
   Les trois predicteurs statistiques informes, `B1 argmax`, `B2 argmax` et `B3 foret`,
   retrouvent **mieux** les minorites sur les items sensibles, plus 0,049 a plus 0,054, les
   trois passant Holm sur la famille secondaire ; `B0 tirage`, qui est aveugle, ne bouge
   pas, plus 0,004. **Aucune condition a modele de langage n'est meilleure sur les
   items sensibles**, et une, `agents enquete`, est nettement pire, moins 0,101, p ajuste
   0,013. Le contraste de groupe post hoc va dans le meme sens : moins 0,021 en moyenne
   pour les six conditions a modele de langage contre plus 0,031 pour les cinq predicteurs
   statistiques, difference moins 0,052, p de permutation des etiquettes de methode 0,047
   [MESURE, `a29-contraste-de-groupe.csv`, hors famille].
2. **Ce serait un joli resultat inverse. Il ne survit pas au bootstrap sur les items**
   [MESURE, `a29-sensibles-bootstrap-items.csv`, hors famille, ajoute apres coup]. Le
   contraste oppose deux ensembles d'items differents, l'un de douze et l'autre de
   soixante cinq ; son incertitude porte donc aussi sur le tirage des items, que le
   bootstrap sur les personnes ne voit pas. **Une fois les items reechantillonnes, aucun
   des onze contrastes du perimetre 1 052 n'exclut zero**, et les p vont de 0,149 a 0,943.
   L'intervalle de `agents enquete` devient [moins 0,247 ; 0,049], celui de `B1 argmax`
   [moins 0,040 ; 0,208].
3. **Conclusion, sans adoucissement : sur les cellules minoritaires, la question des items
   sensibles n'est pas tranchable avec douze items.** Le resultat de la lecture 1 est un
   effet d'items, pas un effet de classe d'items. **La derniere partie de la phrase de
   `ARBITRAGE.md`, « et ils se trompent la ou les gens se surveillent », n'est pas
   soutenue par les minorites**, et elle ne l'etait deja pas methode par methode en a28
   test 1. Elle reste un indice de groupe et rien de plus.

---

## 5. La figure

`a29-figure-minorites.png` et `.svg`, trois panneaux, produits par `a29_figure.py` qui ne
recalcule rien et lit les tableaux.

- **Panneau 1**, rappel en abscisse contre precision en ordonnee, perimetre 1 052, seuil
  10 pour cent, courbes d'iso F1 en fond, barres d'intervalle bootstrap sur les personnes
  dans les deux directions, humains vague 2 en point vert cercle noir. Il montre d'un coup
  d'oeil les deux familles : les predicteurs statistiques collent a l'axe des ordonnees,
  precision correcte et rappel nul ; les conditions a modele de langage occupent la
  diagonale basse ; le point humain est seul en haut a droite.
- **Panneau 2**, le meme sur les 150 personnes du run local, avec `C2` et `C3`.
- **Panneau 3**, la correlation par personne avec son intervalle, plafond humain en
  pointille vert, zero en trait plein, qui est aussi la valeur du temoin de permutation.

---

## 6. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. « Sur les reponses que moins d'une personne sur dix donne, une regression logistique et
   une foret aleatoire n'en produisent presque aucune : 0,95 et 0,13 pour cent des
   cellules, contre 3,64 pour cent chez les humains. Les populations simulees par modele de
   langage en produisent 1,65 a 4,22 pour cent, au bon ordre de grandeur. » [MESURE]
2. « Retrouver la masse minoritaire ne prouve rien sur les personnes : un tirage aveugle
   dans la marginale de chaque question reproduit 99,8 pour cent de la masse et obtient la
   meilleure correlation par item du tableau, 0,9966, pour une correlation par personne de
   moins 0,019. » [MESURE, c'est le temoin de tout le rapport]
3. « Les deux conditions riches de Stanford visent les bonnes personnes a 69 et 73 pour
   cent du plafond que donnent les memes humains reinterroges deux semaines plus tard,
   0,504 et 0,531 contre 0,732. » [MESURE]
4. « Quand une population simulee ose une opinion minoritaire, elle la donne trois fois sur
   cinq a une personne qui, sur cette question, repond comme la majorite : 61,6 pour cent
   pour la meilleure condition, contre 41,4 pour cent chez les humains reinterroges. »
   [MESURE]
5. « Le F1 sur les cellules minoritaires separe les methodes d'un facteur 11 entre la
   meilleure population simulee et la foret aleatoire, 0,3149 contre 0,0277, et d'un
   facteur 3,4 contre la regression logistique. » [MESURE]
6. « A modele, personnes, questions et traces constants, donner l'etiquette demographique
   fait passer la correlation par personne de 0,410 a 0,194, soit de 63 a 30 pour cent du
   plafond humain. » [MESURE, ablation C3 contre C2, la mesure la plus propre du rapport]
7. « Les personnes qui donnent beaucoup de reponses rares sont moins fideles a elles memes
   d'une vague a l'autre, correlation moins 0,32, et aucune methode ne reproduit ce lien. »
   [MESURE]
8. « Toutes les methodes, statistiques comprises, exagerent le lien entre extremisme
   ideologique declare et rarete des reponses : le rapport reel est de 1,94, les humains
   reinterroges donnent 1,90, les agents riches 3,7 a 4,2, la regression 4,9, la foret
   12,8. » [MESURE]

### Interdit

1. **Interdit d'ecrire « les modeles de langage gardent les minorites mais pas les bonnes
   personnes » sans qualificatif.** [MESURE] C'est faux pour les deux conditions riches, a
   73 et 69 pour cent du plafond, et vrai pour `agents v7`, `C2`, et pour tout ce qui n'a
   que l'etiquette. La phrase doit nommer la condition ou dire « aux trois quarts des
   bonnes personnes ».
2. **Interdit de reprendre le facteur 32 de a28 comme le chiffre du dossier sur les
   minorites.** [MESURE] Il est vrai sur le rappel seul, sur 150 personnes. Sur les 1 052
   et sur le F1, qui n'est pas gagnable par l'abstention, il vaut 11,4 contre la foret et
   3,4 contre la regression logistique.
3. **Interdit d'ecrire que la statistique se trompe sur les minorites.** [MESURE] Sa
   precision est la meilleure du tableau, 0,4892 pour `B2 argmax`, et c'est le seul
   contraste de precision de la famille primaire qui ne passe pas la correction. Elle ne
   se trompe pas, elle s'abstient : 0,27 pour cent de masse predite et 124 items sur 149 a
   masse nulle.
4. **Interdit d'ecrire que le stereotype de la personne marginale est un defaut des
   modeles de langage.** [MESURE] La foret aleatoire exagere le rapport ideologique par
   6,6 et `B2 argmax` par 4,8, davantage que les agents riches. Le meme verdict qu'en a28
   test 3 : c'est une propriete de l'etiquette, pas du langage.
5. **Interdit d'ecrire que les modeles se trompent davantage sur les minorites des sujets
   sensibles.** [MESURE] Le signe mesure est l'inverse, et il ne survit pas au
   reechantillonnage des douze items.
6. **Interdit de presenter la propension aux reponses rares comme une propriete purement
   attitudinale.** [MESURE] Elle est correlee a moins 0,32 avec la fidelite test retest de
   la personne, et une part inconnue en est du bruit de reponse.
7. **Interdit d'employer la comparaison C2 contre C3 pour conclure sur les modeles en
   general.** Un modele ouvert de 4 milliards de parametres, un seul run, et la limite
   ouverte de a23 sur la formulation des invites reste entiere.

---

## 7. Ce que cela change a `ARBITRAGE.md`

**L'option A survit mais sa phrase doit etre recrite : la moitie des minorites est bien
gardee et elle va aux trois quarts aux bonnes personnes, ce qui n'est pas le risque annonce
en note de bas de page ; le vrai defaut mesurable est que la bonne personne recoit la
mauvaise opinion rare trois fois sur cinq, et la troisieme partie de la phrase, sur les
sujets ou les gens se surveillent, doit sortir.**

---

## 8. Ce que je n'ai pas pu verifier

1. **La causalite de l'effet d'etiquette sur l'attribution individuelle.** C2 contre C3 est
   une ablation propre, mais sur un seul modele, un seul run, 150 personnes, et deux
   regimes d'invite dont la formulation n'a jamais ete comparee a celle de Stanford. La
   limite ouverte de a23 vaut mot pour mot ici.
2. **Le sens du seuil de minorite.** Il est calcule sur le perimetre observe, donc sur
   150 personnes pour C2 et C3 et sur 1 052 ailleurs. Les deux tableaux ne sont pas
   comparables ligne a ligne entre perimetres, et je n'ai pas mesure la sensibilite du
   classement a ce choix au dela des deux seuils de 10 et 20 pour cent.
3. **La part de bruit dans la propension individuelle a la rarete.** La correlation de
   moins 0,32 avec la fidelite test retest dit qu'il y en a. Je n'ai pas construit
   l'estimateur corrige de l'attenuation, qui demanderait une fidelite par personne
   estimee sur un jeu d'items disjoint de celui qui sert a la mesure.
4. **La comparabilite des conditions de Stanford entre elles.** Six conditions, deux
   generations d'agents demographiques, des tailles d'invite tres differentes. Le rapport
   les met dans le meme tableau parce que a1, a2, a25 et a28 le font deja, pas parce que
   j'ai verifie qu'elles sont comparables.
5. **Twin-2K-500.** Toute l'analyse porte sur le GSS. a8 section 6.2 donne les rappels sur
   Twin, mais ni la precision par personne, ni la correlation par personne, ni les
   profils. La replication hors GSS n'est pas faite, et c'est la verification la plus
   utile qui manque.
6. **L'unicite de la mesure d'appariement.** La correlation de rang sur le taux de rares
   par personne est une mesure parmi d'autres. Une aire sous la courbe par personne, ou un
   modele a effets aleatoires, pourraient donner un autre classement. Je n'ai pas mesure
   cette sensibilite.
7. **Les refus.** Ils sont comptes comme des reponses non minoritaires, convention severe.
   Leur taux est au plus 0,20 pour cent et je n'ai pas mesure ce que change la convention
   inverse.

---

## 9. Questions ouvertes pour Simon

1. **La phrase du papier.** Faut il ecrire « aux trois quarts des bonnes personnes » et
   perdre la formule choc, ou restreindre l'enonce aux conditions pauvres et a nos agents,
   ou l'abandonner ? Le chiffre 0,531 contre 0,732 n'est pas une refutation, c'est une
   nuance, et une nuance ne se poste pas.
2. **Le renversement C2 contre C3.** Deux mesures independantes disent que l'etiquette
   demographique degrade l'appariement individuel de notre agent, la deviance en a23 et la
   rarete ici. Est ce le resultat qui porte le papier, plutot que le gonflement des ecarts
   entre groupes ? Il a l'avantage d'etre une ablation et non une comparaison entre
   familles de methodes.
3. **La nuit de calcul.** La question ouverte numero un de `FAITS-ETABLIS.md` est de savoir
   si l'absence de gonflement sans etiquette tient a un modele de 4 milliards de
   parametres. La mesure de ce rapport ajoute une raison de la trancher : si un modele de
   20 ou 30 milliards de parametres avec etiquette remonte au dessus de C3 sur la
   correlation par personne, la lecture change entierement.
4. **Le vieux excentrique.** Les conditions a modele de langage inversent le profil d'age
   de la rarete, la ou les humains reinterroges le reproduisent. Cela vaut il une mesure
   dediee, avec une famille declaree, ou est ce une correlation de rang sur sept points
   qu'il faut laisser tomber ?
5. **Les douze items sensibles.** Trois rapports successifs, a25, a28 et a29, butent sur le
   meme mur : douze items ne suffisent pas. Faut il abandonner l'axe « la simulation devie
   la ou les gens se surveillent », ou aller chercher une source de classification qui
   donne plus d'items, quitte a perdre l'autorite de NORC ?
6. **Ce qu'un institut achete.** Le rapport suppose qu'un acheteur veut la propension
   individuelle a l'opinion minoritaire. S'il ne veut que le taux par question, la
   correlation par item de 0,91 a 0,92 des agents riches suffit, et `B0 tirage` a 0,9966
   suffit encore mieux pour rien du tout. Quelle est la bonne cible ?

---

## Rejouer

```
.venv/bin/python analyses/a29_mesures.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 2000 --permutations 200
.venv/bin/python analyses/a29_profils.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 2000
.venv/bin/python analyses/a29_figure.py
```

Les deux caches sont ceux de a25 et de a28. S'ils manquent, ils sont reconstruits, ce qui
coute environ deux minutes et demie pour la foret aleatoire. Duree totale ensuite :
24 secondes pour `a29_mesures`, 18 pour `a29_profils`, 3 pour la figure, sur quatre
coeurs. Graine d'analyse 20260908 partout.
