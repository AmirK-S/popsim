# a42. Preenregistrement, le plancher de bruit de cellule et la rarete stable

**Ecrit le 8 septembre 2026 a 15:42:15 CEST, soit 2026-09-08T13:42:15Z.**
**Aucun calcul n'a ete lance avant cette ecriture. Ce fichier n'est plus modifie ensuite.**

Ce document est la famille d'hypotheses, les seuils et les planchers de a42. Il repond au
verrou 2 de `MODELE-DU-MONDE.md` section 6 et a la premiere des trois objections de la
section 7 : *« le resultat des rares est du bruit de petites cellules, controle a moitie
par un plancher circulaire dans un rapport non preenregistre »*.

a34 avait deux defauts nommes par son propre auteur en section 9 point 2 :
il n'existait dans ce rapport *« pas de partition qui soit a la fois non circulaire pour
le plancher et non tautologique pour la regression »*, et la famille avait ete ecrite
apres une lecture descriptive. a42 traite les deux.

---

## 0. Etat de connaissance au moment de l'ecriture

Ce qui est deja lu, et qui doit etre declare parce que cela conditionne les predictions :
les tableaux de a34 (rappels par tercile de deductibilite, planchers, contrastes), ceux de
a29 (rappel, precision, F1 minoritaires, correlation par personne), et la lecture 01 sur
Rennard et Xypolopoulos. **Rien de ce qui suit n'a ete calcule.** Les trois partitions de
a42, la stabilite en vague 2, la division de recensement et la partition aleatoire, n'ont
jamais ete construites ni regardees, sur aucune de leurs marges. Les quantites de a42 sont
donc nouvelles ; les predictions ci dessous sont des predictions au sens strict.

---

## 1. Perimetre, seuil, donnees

**Donnees.** GSS Stanford, jeu OSF t6g7k, 1 052 personnes, 149 items, deux vagues a deux
semaines d'ecart. Lecture seule sur `data/`. Zero appel de modele de langage. Quatre
coeurs. Aucun script existant n'est modifie ; `a34_commun`, `a31_commun`, `a29_commun`,
`a28_commun`, `a25_*`, `a8_commun`, `a2_commun`, `a2_baselines_gss`, `a35_commun` sont
importes tels quels, memes graines, memes plis, memes blocs, memes personnes.

**Perimetre.** Le perimetre naturel de chaque methode : 1 052 personnes pour les methodes
qui les couvrent, 150 personnes du run local pour `C2` et `C3`, avec la reference de
minorite recalculee sur ces 150, comme a28, a29, a31 et a34.

**Seuil de minorite.** 10 pour cent, definition de a8 section 6 importee sans retouche.
Le seuil de 20 pour cent est une robustesse hors famille.

**Methodes testees, treize.** Les six conditions de Stanford (`agents composite`,
`agents entretien (v3)`, `agents enquete`, `agents demographiques (v6)`, `agents v7`,
`agents v8`), `B2 argmax`, `B3 foret`, `PMM k=5`, `PMM k=10`, `IM m=10 mode des m`, plus
`C2` et `C3` sur le perimetre 150. Les trois methodes d'imputation de a35 sont relues du
cache `/tmp/a35-methodes.pkl`, produites par `a35_commun.imputations_regression` sans
modification. Si ce cache s'avere illisible, elles sont declarees non importables et le
fait est ecrit dans le rapport ; la famille est alors reduite d'autant et la reduction est
annoncee.

**Comparateur declare.** `B1 argmax`, comme en a34, et pour la meme raison : von der Heyde
oppose un modele de langage a une regression multinomiale sur exactement les memes
variables que l'invite.

**References hors test.** `B0 tirage`, temoin de lecture ; `humains vague 2`, plafond de
bruit humain. `B0 mode` est decrit et non teste : il ne predit jamais de modalite
minoritaire, sa precision n'est pas definie.

---

## 2. Les trois partitions, et pourquoi elles ne sont ni circulaires ni tautologiques

### 2.1 P_A, la stabilite en vague 2 : la partition qui repond a l'adversaire

Pour une cellule (personne, item) dont la reponse de vague 1 est une modalite minoritaire
et dont la reponse de vague 2 est observee :

- **rarete STABLE** : la personne a redonne **exactement la meme modalite** deux semaines
  plus tard ;
- **rarete INSTABLE** : elle a donne autre chose.

Les cellules sans reponse de vague 2 sont exclues de cette partition, et le taux de
couverture est rapporte.

**Pourquoi c'est la partition qui repond a l'adversaire.** Elle n'emploie ni la confiance
de `B1`, ni aucune frequence de segment, ni aucun attribut demographique : c'est une
mesure prise sur la personne elle meme, a deux semaines. **Une rarete stable est de la
vraie heterogeneite individuelle ; une rarete instable est indistinguable du bruit humain
de reponse.** Si l'avantage des conditions a modele de langage sur la statistique ne tient
que sur les instables, il porte sur du bruit et la these tombe.

**Identite a declarer d'avance.** Sur cette partition, `humains vague 2` a un rappel de
1,000 sur les stables et de 0,000 sur les instables **par construction** : la partition
est cette ligne. Elle est imprimee comme identite et **elle n'entre dans aucun test**. Le
troisieme plancher, `humains vague 2`, est pour la meme raison degenere sur P_A : il n'y
est pas lu.

**Effet attendu et deja anticipe.** Les cellules stables sont plus faciles pour tout le
monde, y compris pour les planchers : une modalite qu'une personne redonne a deux semaines
est plausiblement une modalite un peu moins rare. **C'est pourquoi le rappel brut par
classe ne prouve rien et c'est l'EXCES SUR PLANCHER qui porte la conclusion.**

### 2.2 P_B, la division de recensement : la partition tierce de deductibilite

Frequence de la modalite dans la **division de recensement** de la personne
(`census_division`, neuf niveaux dans `demographic_summary.csv`), calculee sur les humains
de la vague 1 **en laissant de cote la personne elle meme**. Terciles aux 33,3e et 66,7e
percentiles du score sur les cellules minoritaires reelles du perimetre. T1 = le moins
deductible.

**Ce qu'elle repare, et ce qu'elle ne repare pas, ecrit d'avance.** Elle n'est **ni** la
confiance de `B1` (partition D_logit de a34, tautologique : 100 pour cent des raretes
osees par la regression y tombent dans le tercile deductible), **ni** la frequence dans le
segment ideologie x genre x age (partition D_seg de a34, qui est le meme calcul que le
plancher, donc circulaire). L'exces sur le plancher de segment y est donc lisible.
**Mais `census_division` fait partie des onze attributs que `B1`, `B3 foret` et les
personas demographiques recoivent : la partition n'est pas independante de la famille des
predicteurs, elle est seulement independante du plancher et de la regle de decision de
`B1`.** Ce defaut residuel est declare ici et sera repete dans le rapport. La seule
partition du dossier qui soit independante de tout est P_A.

**Controle arithmetique declare d'avance** : la part des raretes osees par `B1 argmax` qui
tombe dans chacun des trois terciles de P_B est mesuree et publiee. Si elle vaut 100 pour
cent dans T3, P_B a le meme defaut que D_logit et **elle est declaree non interpretable**
plutot que publiee comme arbitrage.

### 2.3 P_C, la partition aleatoire fixee : le placebo

Les 1 052 personnes sont reparties en **neuf groupes aleatoires de tailles egales**,
graine 20260908 fixee ici, avant tout calcul. Le score est la frequence de la modalite
dans le groupe aleatoire de la personne, sans la personne, et les terciles sont pris comme
en P_B.

**Ce placebo n'est pas un ornement, c'est l'etalon du bruit de petites cellules.** Un
groupe aleatoire ne porte aucune information sur la personne : l'esperance de son score
est la marginale de l'item. Tout gradient de rappel observe le long de P_C est donc
**entierement du bruit d'echantillonnage de petites cellules**. Il donne la taille de
l'artefact que Rennard et Xypolopoulos decrivent, mesuree chez nous. **Le gradient de P_B
n'est interpretable que dans la mesure ou il depasse celui de P_C.**

---

## 3. Les trois planchers

Tous les trois sont calcules **sur les memes cellules** que le rappel qu'ils servent a
juger, et retranches cellule par cellule avant agregation par personne.

1. **Plancher d'item** : rappel attendu sous un tirage dans la marginale de l'item, sans
   la personne. C'est l'esperance de `B0 tirage`. Il ne sait rien de la personne.
2. **Plancher de segment** : rappel attendu sous un tirage dans la marginale du segment
   ideologie x genre x age de la personne, sans la personne. C'est le plancher de bruit de
   cellule demande par la lecture 01 section (d) point 5. Le segment est celui de a34,
   importe : trois axes, 98 cases possibles, minimum de cinq autres repondants
   exploitables sur l'item, sinon la cellule n'entre pas dans le plancher.
3. **Plancher des humains de la vague 2** : le rappel des memes personnes reinterrogees
   deux semaines plus tard, sur les memes cellules. C'est en pratique un **plafond** et
   non un plancher ; l'exces sur lui sera negatif pour toutes les methodes et se lit comme
   une part du plafond humain. Il est **degenere sur P_A** et n'y est pas lu.

**Exces** = rappel moins plancher, sur les cellules ou le plancher est defini, avec
intervalle de confiance a 95 pour cent par bootstrap apparie **sur les personnes**.

---

## 4. La famille d'hypotheses

Notation : « stable » et « instable » designent les deux classes de P_A ; « T1 » et « T3 »
les terciles extremes de P_B.

| | enonce | direction | nombre de tests |
|---|---|---|---|
| **H1** primaire | pour chacune des 13 methodes testees, l'avantage de rappel sur `B1 argmax` **sur les raretes STABLES** est strictement positif | dirige | 13 |
| **H2** primaire | pour chacune des 14 methodes (13 plus `B1 argmax`), l'exces de rappel sur le **plancher de segment**, **sur les raretes STABLES**, est strictement positif | dirige | 14 |
| **H3** secondaire | pour chacune des 13 methodes, l'avantage sur `B1 argmax` sur les STABLES differe de celui sur les INSTABLES | bilateral | 13 |
| **H4** secondaire | pour chacune des 14 methodes, l'exces sur le plancher de segment differe entre T3 et T1 de **P_B**, la partition tierce | bilateral | 14 |
| **H5** tertiaire | pour chacune des 13 methodes, l'avantage sur `B1 argmax` sur les raretes STABLES reste strictement positif **apres retrait des cellules dont la modalite est portee par moins de 20 personnes** (controle de Rennard, le plus severe des trois) | dirige | 13 |

**Famille primaire : H1 union H2, 27 tests. Famille secondaire : H3 union H4, 27 tests.
Famille tertiaire : H5, 13 tests.** Chaque famille est corrigee **separement par Holm**,
valide sans hypothese sur la dependance, ce qui est necessaire puisque les contrastes
portent sur les memes personnes et les memes items. **Benjamini Hochberg** est rapporte a
cote. Tous les p sont des p de **bootstrap apparie sur les personnes, 4 000 tirages**, lus
sur la position de zero dans la distribution ; ils ne descendent jamais sous 1/4 000. Le
meme tirage sert a toutes les methodes.

### 4.1 Les criteres de chute, ecrits avant de voir un chiffre

**Le resultat de a29, a31 et a34 sur les rares tombe si l'une des trois conditions
suivantes se realise.**

1. **H1 echoue pour les conditions riches de Stanford.** Si `agents composite` et
   `agents entretien (v3)` n'ont pas un avantage strictement positif sur `B1 argmax` dans
   les raretes STABLES apres Holm, alors l'avantage mesure depuis a28 porte sur du bruit
   humain et non sur de l'heterogeneite, et la these tombe.
2. **H2 echoue pour ces memes conditions.** Si leur exces sur le plancher de segment n'est
   pas strictement positif sur les STABLES, le resultat est du bruit de petites cellules
   au sens exact de Rennard, et la these tombe.
3. **H3 est fortement negatif pour ces memes conditions**, c'est a dire un avantage
   significativement plus grand sur les INSTABLES que sur les STABLES. La these ne tombe
   pas mecaniquement, mais sa formulation devient « les agents retrouvent surtout les
   raretes que la personne ne reproduit pas », ce qui est **l'objection de l'adversaire
   confirmee**, et il faudra l'ecrire ainsi.

**Predictions ecrites d'avance, pour qu'on puisse me prendre en defaut.**
(a) H1 passe pour les six conditions de Stanford et pour `C3`, et je ne sais pas pour
`C2`, `agents v7` et les trois methodes d'imputation de a35. (b) H2 passe pour les
conditions riches et **echoue pour `B1 argmax`, `B3 foret`, `PMM` et `IM`**, dont l'exces
sera negatif : c'est la reconduction du resultat le plus dur de a34 sur une partition non
circulaire. (c) H3 : je predis une difference **non significative** pour la majorite des
conditions, c'est a dire un avantage qui tient des deux cotes. (d) P_C, le placebo, montre
un gradient de rappel **non nul** le long de terciles pourtant vides d'information : c'est
la mesure directe de l'artefact de Rennard.

### 4.2 N'entrent dans aucune famille, et sont des descriptions

La precision et le F1 par classe et par tercile ; le seuil de 20 pour cent ; la partition
aleatoire P_C dans son entier, qui est un placebo et non une hypothese ; les planchers
d'item et de vague 2, qui sont des lectures et non des tests ; le controle de Rennard a
n = 5 et n = 10, seul n = 20 etant teste ; le perimetre 150 pour les methodes qui
disposent du 1 052 ; la ligne `humains vague 2` partout ; la ligne `B0 tirage` partout ;
les contrastes de groupe entre familles de methodes ; la couverture de la vague 2 et la
description des partitions.

---

## 5. Definitions de mesure, y compris les cas penibles

**Rappel** par classe : part des cellules minoritaires reelles **de cette classe** que la
methode retrouve. **Precision** par classe : part des cellules justes parmi celles ou la
methode **ose** une modalite minoritaire **et qui appartiennent a cette classe**.
**F1** : moyenne harmonique des deux.

**Comment une cellule osee est classee, et c'est un ecart avec a34 qu'il faut declarer.**
Sur P_A, la classe d'une cellule est une propriete de la **personne sur cet item** : la
stabilite de SA reponse de vague 1, definie que la reponse soit rare ou non. Elle
s'applique donc identiquement au numerateur et au denominateur du rappel et de la
precision. a34 classait au contraire les cellules osees par la deductibilite de la
modalite **predite** ; ce choix n'a pas de sens ici, puisque la stabilite est une propriete
de la personne et non de la modalite. Sur P_B et P_C, ou le score est bien une propriete de
la modalite, la convention de a34 est reprise telle quelle : la classe d'une cellule osee
est celle de la modalite predite.

**Convention de masque**, reprise de a8 section 6, a29, a31 et a34 sans changement : une
cellule est evaluable des que la vraie reponse de la vague 1 est observee ; une prediction
refusee compte comme non minoritaire.

**Controle de Rennard.** Pour une cellule dont la vraie modalite est `m` sur l'item `j`,
le support de `m` est le nombre de personnes du perimetre qui ont donne `m` sur `j` en
vague 1. Le controle retire les cellules de support strictement inferieur a n, pour
n = 5, 10 et 20, et recalcule rappel, plancher et exces. **Seul n = 20 est teste (H5).**

**Bootstrap.** 4 000 tirages avec remise sur les **personnes** du perimetre, jamais sur
les cellules : deux reponses d'une meme personne ne sont pas independantes. Graine
d'analyse 20260908, graine de protocole 20260903 heritee de a2. Toutes les quantites sont
des rapports de sommes reduits a un numerateur et un denominateur par personne, comme en
a31 et a34, ce qui rend les contrastes apparies.

**Contraste non evaluable** : un contraste dont l'un des deux denominateurs est vide recoit
p = 1, choix conservateur repris de a29 et a31 ; il ne peut pas creer de fausse decouverte
et il n'allege pas la correction appliquee aux autres.

---

## 6. Ecarts declares par rapport a a34

1. **Les partitions.** a34 employait D_seg (circulaire avec le plancher) et D_logit
   (tautologique pour `B1`). a42 emploie trois partitions tierces : stabilite en vague 2,
   division de recensement, partition aleatoire placebo. D_seg et D_logit ne sont pas
   recalculees ici.
2. **Le preenregistrement.** a34 declarait explicitement ne pas l'avoir ; a42 l'a, ce
   fichier en est la trace horodatee, et il n'est pas modifie ensuite.
3. **Les methodes.** `PMM k=5`, `PMM k=10` et `IM m=10 mode des m` de a35 entrent, sous
   reserve de lisibilite du cache. `B0 mode` sort des tests.
4. **Les planchers.** Trois au lieu de deux ; les humains de la vague 2 deviennent un
   plancher explicite, avec l'avertissement qu'ils sont en pratique un plafond.
5. **Le controle de Rennard sur le support de modalite** (n = 5, 10, 20) n'existait pas
   dans a34.
6. **La classification des cellules osees sur P_A** est une propriete de la personne et
   non de la modalite predite ; voir section 5.
7. **Trois familles de correction** au lieu de deux.

---

## 7. Sorties prevues

`analyses/a42_commun.py`, `a42_plancher.py`, `a42_figure.py`.
`resultats/a42-partitions.csv`, `a42-stabilite.csv`, `a42-partitions-tierces.csv`,
`a42-contrastes.csv`, `a42-rennard.csv`, `a42-controles.csv`,
`a42-figure-plancher.png` et `.svg`, `a42-plancher-de-bruit.md`.

Aucun fichier existant n'est modifie. Aucune microdonnee n'est ecrite.
