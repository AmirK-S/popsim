# d4. La diversite politique d'un camp, chez les humains : une quantite sur trois survit au controle de la position, et ce n'est pas celle qu'Amir croyait

Seance du 9 septembre 2026. **Preenregistrement : `resultats/d4-preenregistrement.md`, horodate
du 9 septembre a 12:05 CEST, ecrit avant le premier calcul et non modifie ensuite.** Le calcul a
tourne de 12:08:55 a 12:10:18, soit **1 minute 23 secondes** sur quatre coeurs.

**Zero appel de modele de langage. Aucun serveur d'inference. Lecture seule sur `data/`. Aucune
microdonnee ecrite. Aucun fichier existant modifie ; tous les fichiers produits sont prefixes
`d4`.** `a30_commun`, `a30_structure`, `a37_commun`, `a44_commun`, `a2_baselines_gss`,
`a25_commun`, `a9_commun`, `a12_retest_delai` et `i1_commun` sont importes tels quels, sans une
ligne recopiee.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans une
source verifiee, **[PROBABLE]** interpretation etayee mais non demontree, **[HYPOTHESE]**
proposition a tester.

---

## Reponse en une ligne

**H_Amir n'est pas etablie, et le pari du dossier n'est pas gagne non plus.** [MESURE] Sur les
trois quantites preenregistrees, **une seule** passe les quatre conditions de la section 7 du
preenregistrement, la ou H_Amir en exigeait deux : la dispersion residuelle apres controle de
position (Q1) ne montre **aucune** asymetrie, contraste **+0,0003 [-0,0124 ; +0,0160]**, p 0,971 ;
la dimension effective de la structure de correlation (Q3) montre une asymetrie de **+0,0332
[0,0310 ; 0,0353]** mais elle est **plus forte sur les items non politiques** (+0,0526) et elle
**s'inverse sur Twin** (-0,1710), donc elle tombe sur deux criteres a la fois ; et le nombre de
profils distincts en exces du nul de gabarit (Q2) donne **+12,41 [11,96 ; 12,86]**, p de Holm
0,003, **onze fois** le plancher de reinterrogation, robuste a l'appariement
demographique exact, au changement d'ancrage sur `partyid`, aux trois tailles d'echantillon
testees, et **replique dans les cinq replications** : Twin-2K-500 et les quatre panels NORC, sur
onze mille personnes de plus et quinze annees. **Sur cette quantite la, l'asymetrie existe et elle
n'est pas de la position.** [MESURE] Le controle qui la specifie est le plus net du rapport : sur
les items **non politiques** du meme questionnaire, l'ecart tombe a +0,71 sur le GSS et **change
de signe** sur Twin et sur les quatre panels.

**Mais la quantite qui survit ne dit pas ce qu'Amir en attend.** [MESURE] Le camp du centre est
au meme niveau que la droite sur Q2, -14,88 contre -13,22, et **la depasse** sur Q3, 0,5110 contre
0,4565. L'enonce que les donnees soutiennent n'est pas « la droite est plus diverse », c'est
**« la gauche est le camp le plus contraint des trois »**, ce qui est exactement l'enonce que
Cely publie sur l'ESS en 2025 et que `a30` mesurait deja par un autre chemin, correlation entre
axe economique et axe social 0,447 a gauche contre 0,311 a droite.

**Et le mecanisme de `a37` est confirme une seconde fois, plus profondement.** [MESURE] Q1 ne vaut
zero en moyenne que parce qu'elle est la **somme de deux effets opposes** : sur les 34 items ou la
majorite penche a gauche, c'est **la gauche** qui a le plus de dispersion residuelle, contraste
-0,0192 [-0,0306 ; -0,0085] ; sur les 12 items ou la majorite penche a droite, c'est **la droite**,
+0,0555 [0,0260 ; 0,0877]. Le residu de position n'est pas une propriete du camp non plus : il
change de signe avec la polarite de l'item, pente +0,158, R2 0,248.

---

## 0. Ce qui a ete mesure, et sur quoi

| jeu | personnes | items `P1` politiques | items `P0` de controle | camps, bloc de trois | `n_egal` |
|---|---|---|---|---|---|
| **GSS de Stanford**, vagues 1 et 2 | 1 052, memes personnes | **79** orientes (Q1 sur les **46** a plus de deux modalites) | 51 non orientables (Q1 sur 32) | gauche 417, centre 303, droite 332 | **303** |
| **Twin-2K-500**, vagues 1 a 3 et 4 | 2 058 | **10** items du bloc `attitudes` | 275 items de personnalite (Q1 sur 261) | gauche 909, centre 582, droite 567 | **567** |
| **panel NORC 2006-2010** | 2 000 | 76 orientes (Q1 sur 43) | 42 (Q1 sur 30) | gauche 533, centre 731, droite 667 | 533 |
| **panel NORC 2008-2012** | 2 023 | idem | idem | gauche 530, centre 740, droite 663 | 530 |
| **panel NORC 2010-2014** | 2 044 | idem | idem | gauche 567, centre 746, droite 660 | 567 |
| **panel NORC 2016-2020** | 5 215 | idem | idem | gauche 796, centre 1 032, droite 928 | 796 |

[MESURE] Les quatre panels NORC sont des **echantillons probabilistes disjoints** : d'un panel a
l'autre, aucune personne n'est commune. Ils apportent 11 282 personnes, quinze annees et un mode
de recrutement qui n'est ni Prolific ni un panel en ligne, ce qui est le controle externe le plus
fort du rapport. 19 items du GSS de Stanford portent une modalite « inapplicable » et sont exclus
de tout : la position n'y a pas de sens.

---

## 1. Les trois quantites, et ce que le nul en dit

Rappel du preenregistrement, section 3. Le **critere O** : une quantite de diversite est
admissible si elle est **modifiee** quand on remplace le camp par une population fictive de memes
marginales item par item et sans aucune structure ; et la quantite publiee est l'**ecart** a cette
reference. Le nul est celui de `a44_commun`, tirage multinomial independant dans la loi de l'item
**a l'interieur du camp**. Il a donc, item par item, exactement la meme position que le camp reel.

`d4-nuls.csv`, GSS de Stanford, `P1`, vague 1, 303 personnes par camp.

| camp | Q2 patrons observes | Q2 patrons du nul | **Q2 exces** | Q3 dimension observee | Q3 dimension du nul | **Q3 normalisee** |
|---|---|---|---|---|---|---|
| **gauche** | 195,44 | 221,07 | **-25,63** | 26,59 | 62,80 | **0,4233** |
| centre | 250,38 | 265,26 | -14,88 | 32,10 | 62,83 | 0,5110 |
| **droite** | 261,22 | 274,44 | **-13,22** | 28,68 | 62,82 | **0,4565** |

[MESURE] **La colonne « patrons du nul » est la preuve que le controle etait necessaire.** Sur dix
items et 303 personnes, le camp de gauche ne peut produire que 221 combinaisons distinctes meme en
tirant ses items independamment, contre 274 pour la droite : c'est un pur effet de position, ses
marginales sont plus concentrees. **Comparer les 195 aux 261 serait comparer deux positions ; ce
que ce rapport compare, ce sont les 25,6 aux 13,2.**

[MESURE] **Controle bloquant numero 1, le nul contre le nul.** L'ecart entre deux replicats du
generateur nul vaut **+0,03 en moyenne pour Q2** (ecart type 6,8 par tirage, 4 000 tirages) et
**1,0000 pour Q3** (ecart type 0,007). Les deux quantites ont donc une reference stable, et les
ecarts publies, 12,41 et 0,0332, ne sont pas du bruit de generateur.

[MESURE] Une lecture relative, descriptive et non preenregistree, pour ceux qui trouveront le
« -25,6 contre -13,2 » difficile a lire : la gauche perd **11,6 pour cent** des combinaisons que
ses propres marginales autorisent, la droite **4,8 pour cent**, le centre **5,6 pour cent**.

---

## 2. Q1, la dispersion residuelle : rien en moyenne, et deux effets opposes en dessous

`d4-contrastes.csv`, `d4-q1-par-item.csv`, `d4-polarite.csv`. Contraste apparie item par item,
1 000 tirages de bootstrap, test d'inversion de signe de `a30_structure.apparie`.

| condition | residu gauche | residu droite | contraste | intervalle | p | p Holm |
|---|---|---|---|---|---|---|
| **GSS `P1` vague 1, 46 items** | -0,0317 | -0,0314 | **+0,0003** | [-0,0124 ; +0,0160] | 0,971 | 0,971 |
| GSS `P1` vague 2, plancher | -0,0332 | -0,0292 | +0,0039 | [-0,0125 ; +0,0227] | 0,693 | |
| GSS `P0` vague 1, 32 items | -0,0730 | -0,0837 | -0,0107 | [-0,0356 ; +0,0086] | 0,359 | |
| GSS `P1` appariement demographique | -0,0315 | -0,0325 | -0,0010 | [-0,0163 ; +0,0144] | 0,883 | |
| GSS `P1` ancrage `partyid` | -0,0331 | -0,0357 | -0,0026 | [-0,0158 ; +0,0111] | 0,725 | |
| Twin `P1`, 10 items | -0,0013 | -0,0153 | -0,0140 | [-0,0265 ; -0,0009] | 0,096 | 0,096 |
| panel 2006-2010 | -0,0383 | -0,0429 | -0,0046 | [-0,0181 ; +0,0078] | 0,520 | |
| panel 2008-2012 | -0,0448 | -0,0546 | -0,0098 | [-0,0270 ; +0,0098] | 0,348 | |
| panel 2010-2014 | -0,0386 | -0,0460 | -0,0074 | [-0,0203 ; +0,0072] | 0,329 | |
| panel 2016-2020 | -0,0399 | -0,0497 | -0,0098 | [-0,0270 ; +0,0086] | 0,294 | |

[MESURE] **Q1 est nulle partout, et quand elle penche, elle penche du mauvais cote pour H_Amir.**
Aucun des dix contrastes n'a un intervalle qui exclut zero du cote de la droite ; sept des dix sont
negatifs, c'est a dire en faveur de la gauche. **Sur les 46 items du GSS, le residu de droite ne
depasse celui de gauche que dans 16 cas sur 46.** [MESURE] **La conclusion de `a37` section 4 tient
donc, et se durcit : une fois la position de l'item otee, la dispersion interne d'un camp ne
distingue plus les camps.**

### 2.1 Le controle de polarite, et le resultat qui n'etait pas prevu

`d4-polarite.csv`. Le preenregistrement demandait de verifier que le residu ne depend plus de la
polarite de l'item. **Il en depend encore, et le motif est exactement celui de Brandt et Sleegers.**

| sous ensemble | items | derive moyenne | contraste Q1 droite moins gauche | intervalle | p |
|---|---|---|---|---|---|
| **derive negative**, la majorite penche a gauche | **34** | -0,160 | **-0,0192** | [-0,0306 ; -0,0085] | **0,003** |
| **derive positive**, la majorite penche a droite | **12** | +0,165 | **+0,0555** | [0,0260 ; 0,0877] | **0,005** |
| ensemble | 46 | -0,075 | +0,0003 | [-0,0124 ; 0,0160] | 0,971 |

[MESURE] Regression du contraste sur la derive et sur sa valeur absolue : **pente +0,158 sur la
derive, R2 0,248**. Le residu de position n'est pas orthogonal a la polarite ; il en depend au
second ordre, et il change de signe avec elle.

[PROBABLE] **La lecture defendable.** Le temoin de position de `a37` retire l'effet de premier
ordre, la moyenne du camp sur l'echelle. Ce qui reste n'est pas une propriete du camp : c'est un
effet de second ordre, de meme nature. Le camp qui se trouve **du cote oppose au consensus** garde
plus de dispersion residuelle, quel que soit le camp. **Q1 mesure donc bien quelque chose, mais ce
quelque chose est encore de la position, et son bilan agrege est nul parce que les 34 items a
derive de gauche et les 12 items a derive de droite se compensent presque exactement.** C'est la
version residuelle du test T1 de `corpus/05`, et elle donne la meme reponse que `a37`.

---

## 3. Q2, les profils distincts en exces du nul : la seule asymetrie qui survit a tout

`d4-contrastes.csv`. 200 sous ensembles de dix items, 20 tirages de personnes par sous ensemble,
soit 4 000 comparaisons appariees, 50 replicats du generateur nul, effectifs egalises.

| condition | exces gauche | exces droite | contraste | intervalle | p | p Holm |
|---|---|---|---|---|---|---|
| **GSS `P1` vague 1** | **-25,63** | **-13,22** | **+12,41** | **[11,96 ; 12,86]** | **0,001** | **0,003** |
| GSS `P1` vague 2, plancher | -28,01 | -14,50 | +13,51 | [13,07 ; 13,97] | 0,001 | 0,003 |
| **GSS `P0` vague 1, controle** | **-7,31** | **-6,61** | **+0,71** | [0,42 ; 0,97] | 0,001 | 0,003 |
| GSS `P1` appariement demographique, 281 par camp | -22,22 | -11,18 | +11,04 | [10,48 ; 11,61] | 0,001 | |
| GSS `P1` ancrage `partyid` | -29,22 | -16,48 | +12,74 | [11,95 ; 13,42] | 0,001 | |
| GSS `P1` `n_egal` 166 | -14,10 | -5,06 | +9,04 | [8,47 ; 9,66] | 0,001 | |
| GSS `P1` `n_egal` 249 | -21,23 | -9,31 | +11,92 | [11,13 ; 12,69] | 0,001 | |
| GSS `P1` `n_egal` 332 | -27,75 | -14,22 | +13,53 | [12,54 ; 14,45] | 0,001 | |
| **Twin `P1`, 10 items** | -75,19 | -19,80 | **+55,39** | [55,06 ; 55,71] | 0,001 | 0,003 |
| Twin `P0`, 275 items de personnalite | -4,18 | -6,40 | **-2,22** | [-2,50 ; -1,94] | 0,001 | 0,003 |
| **panel 2006-2010** | -7,10 | -2,79 | **+4,31** | [3,06 ; 5,63] | 0,001 | 0,003 |
| panel 2006-2010 `P0` | -0,80 | -1,45 | **-0,65** | [-1,16 ; -0,15] | 0,010 | 0,020 |
| **panel 2008-2012** | -8,36 | -3,46 | **+4,90** | [3,76 ; 6,14] | 0,001 | 0,003 |
| panel 2008-2012 `P0` | -0,66 | -1,13 | **-0,47** | [-0,83 ; -0,15] | 0,016 | 0,032 |
| **panel 2010-2014** | -6,85 | -3,62 | **+3,23** | [2,09 ; 4,43] | 0,001 | 0,003 |
| panel 2010-2014 `P0` | -0,90 | -1,07 | -0,17 | [-0,72 ; 0,37] | 0,548 | 1,000 |
| **panel 2016-2020** | -11,20 | -5,54 | **+5,66** | [4,09 ; 7,21] | 0,001 | 0,003 |
| panel 2016-2020 `P0` | -1,47 | -2,39 | **-0,92** | [-1,66 ; -0,14] | 0,027 | 0,054 |

[MESURE] **Les quatre conditions du preenregistrement sont satisfaites, les quatre.**

1. **Signe, intervalle et Holm.** +12,41 [11,96 ; 12,86], p de Holm 0,003 dans la famille de trois.
2. **Au dessus du plancher.** La reinterrogation des memes 1 052 personnes deux semaines plus tard
   donne +13,51 : le plancher vaut **1,10**, et le contraste est **onze fois** ce plancher.
3. **Replication.** Cinq replications independantes, toutes du meme signe, toutes avec un
   intervalle excluant zero : Twin +55,39 et les quatre panels NORC de +3,23 a +5,66.
4. **Specificite politique.** Sur les items **non politiques du meme questionnaire**, l'ecart tombe
   a +0,71 sur le GSS, soit **6 pour cent** de sa valeur politique, et il **change de signe** sur
   Twin (-2,22) et sur les quatre panels (-0,17 a -0,92). **Sur les items qui ne sont pas
   politiques, c'est la droite qui est legerement la plus contrainte.**

[MESURE] **Une reserve d'echelle, obligatoire.** Le contraste croit avec `n_egal` : +9,04 a 166
personnes par camp, +11,92 a 249, +13,53 a 332. **La valeur numerique de Q2 n'est pas comparable
d'un jeu a l'autre ni d'une taille a l'autre** ; seuls le signe et l'ordre des camps le sont. C'est
la raison pour laquelle le +55,39 de Twin ne doit jamais etre cite a cote du +12,41 du GSS.

[MESURE] **Une reserve de perimetre, propre a Twin.** Le bloc `attitudes` de Twin ne compte que
**dix** items, et les sous ensembles en comptent dix : **il n'y a qu'un seul sous ensemble
possible**. L'intervalle [55,06 ; 55,71] ne porte donc que sur le tirage des personnes, jamais sur
le tirage des items, et il est artificiellement etroit. La replication de Twin compte pour son
signe, pas pour son intervalle.

---

## 4. Q3, la dimension effective : elle passe Holm et elle tombe sur deux controles

| condition | Q3 gauche | Q3 droite | contraste | intervalle | p Holm |
|---|---|---|---|---|---|
| **GSS `P1` vague 1** | 0,4233 | 0,4565 | **+0,0332** | [0,0310 ; 0,0353] | **0,003** |
| GSS `P1` vague 2, plancher | 0,4021 | 0,4365 | +0,0344 | [0,0325 ; 0,0363] | 0,003 |
| **GSS `P0` vague 1, controle** | 0,6412 | 0,6938 | **+0,0526** | [0,0507 ; 0,0544] | **0,003** |
| GSS `P1` appariement demographique | 0,4366 | 0,4583 | +0,0218 | [0,0211 ; 0,0224] | |
| GSS `P1` ancrage `partyid` | 0,4200 | 0,4594 | +0,0394 | [0,0373 ; 0,0414] | |
| **Twin `P1`** | 0,6451 | 0,4741 | **-0,1710** | [-0,1740 ; -0,1678] | 0,003 |
| Twin `P0` personnalite | 0,1793 | 0,1924 | +0,0132 | [0,0122 ; 0,0141] | 0,003 |
| panel 2006-2010 `P1` / `P0` | 0,4728 / 0,7041 | 0,5404 / 0,7211 | **+0,0676** / +0,0170 | | 0,003 |
| panel 2008-2012 `P1` / `P0` | 0,5266 / 0,6720 | 0,5666 / 0,6960 | **+0,0400** / +0,0240 | | 0,003 |
| panel 2010-2014 `P1` / `P0` | 0,4714 / 0,6571 | 0,5208 / 0,6878 | **+0,0495** / +0,0307 | | 0,003 |
| panel 2016-2020 `P1` / `P0` | 0,4338 / 0,6392 | 0,5557 / 0,7145 | **+0,1219** / +0,0752 | | 0,003 |

[MESURE] **Q3 echoue au controle numero 4, et sur les cinq jeux, pas seulement sur un.** Le
preenregistrement exigeait que le contraste sur les items non politiques soit inferieur a la
moitie du contraste politique. Sur le GSS de Stanford il lui est **superieur**, 0,0526 contre
0,0332 ; sur trois des quatre panels il depasse la moitie (0,0240 contre 0,0400 ; 0,0307 contre
0,0495 ; 0,0752 contre 0,1219). **La droite a une matrice de correlation plus proche de
l'independance que la gauche sur les items politiques, mais aussi sur l'equipement, la sante, la
pratique religieuse et le bien etre.** Ce n'est donc pas une propriete de son systeme de croyances,
c'est un fait de style de reponse.

[MESURE] **Q3 declenche en outre le critere de refutation numero 3, l'inversion de signe.** Sur les
dix items d'attitudes de Twin, le contraste vaut **-0,1710 [-0,1740 ; -0,1678]** contre **+0,0332
[0,0310 ; 0,0353]** sur le GSS : deux intervalles disjoints, deux signes opposes. C'est exactement
le motif que Brandt et ses coauteurs rencontrent entre l'ESS et l'Eurobarometre [CONFIRME,
corpus/05, 05-56], et le preenregistrement l'avait ecrit comme refutation de l'universalite.

[MESURE] Le plancher de Q3 est minuscule, 0,0012 entre les deux vagues des memes personnes, et il
ne sauve rien : le probleme de Q3 n'est pas sa precision, c'est sa specificite.

---

## 5. Le centre, qui decide du sens de la phrase

`d4-nuls.csv`, GSS de Stanford, `P1`, vague 1.

| quantite | gauche | centre | droite | centre moins gauche | droite moins gauche | droite moins centre |
|---|---|---|---|---|---|---|
| **Q1** | -0,0317 | -0,0449 | -0,0314 | **-0,0132** [-0,0251 ; -0,0002] | +0,0003 | +0,0135 |
| **Q2** | -25,63 | -14,88 | -13,22 | **+10,75** [10,33 ; 11,17] | **+12,41** | **+1,66** |
| **Q3** | 0,4233 | 0,5110 | 0,4565 | **+0,0876** [0,0855 ; 0,0897] | +0,0332 | **-0,0545** |

[MESURE] **Sur Q2, le centre capte 87 pour cent de l'avantage de la droite** (10,75 contre 12,41).
**Sur Q3, le centre depasse la droite** de 0,0545. La quantite mesuree n'est donc pas « etre de
droite », c'est **« ne pas etre de gauche »**, avec un supplement faible et non teste pour la
droite sur Q2.

[MESURE] C'est le meme motif que `a30` avait deja mesure sur la dispersion, ou le centre etait
indistinguable de la droite, 0,989 contre 1,000. **Il se reproduit sur une quantite entierement
differente, qui ne partage avec la premiere ni sa formule ni sa sensibilite a la position.**

[MESURE] Le contraste droite moins centre est une **difference de moyennes publiees, sans
intervalle de bootstrap** : il n'etait pas dans les familles de tests et il n'a pas ete estime.
Il ne doit pas etre cite comme un resultat teste.

---

## 6. Le tableau des verdicts, applique mot pour mot

`d4-verdicts.csv`. Les quatre conditions de la section 7 du preenregistrement, cochees ou non.

| quantite | contraste GSS `P1` | p Holm | plancher | contraste `P0` | C1 signe et Holm | C2 au dessus du plancher | C3 replication meme signe | C4 `P0` ne reproduit pas | **les quatre** |
|---|---|---|---|---|---|---|---|---|---|
| **Q1** | +0,0003 | 0,971 | 0,0036 | -0,0107 | non | non | non (1 inversion) | non | **non** |
| **Q2** | **+12,41** | **0,003** | **1,10** | **+0,71** | **oui** | **oui** | **oui, 5 sur 5** | **oui** | **OUI** |
| **Q3** | +0,0332 | 0,003 | 0,0012 | **+0,0526** | oui | oui | oui, 4 sur 5 | **non** | **non** |

**Verdict, dans les termes du preenregistrement.**

- **H_Amir, telle qu'elle est ecrite, n'est pas etablie.** Elle exigeait **au moins deux** des trois
  quantites satisfaisant les quatre conditions. **Une seule** les satisfait.
- **Le critere de refutation numero 3 est declenche pour Q3** : signe inverse entre le GSS de
  Stanford et Twin, intervalles disjoints. Q3 est retiree comme mesure d'asymetrie politique.
- **Q1 refute H_Amir sur son terrain propre**, celui de la dispersion : rien, sur cinq jeux de
  donnees et 13 386 personnes.
- **Mais le pari du dossier est perdu sur Q2.** Le pari ecrit etait : *« il n'y a pas d'asymetrie
  droite gauche robuste au controle de la position des items »*. **Q2 est exactement une telle
  asymetrie** : elle est construite pour etre inchangee sous remplacement du camp par ses propres
  marginales, elle survit a l'appariement demographique, au changement d'ancrage, a trois tailles
  d'echantillon, elle est onze fois son plancher de bruit, elle se replique cinq fois sur cinq, et
  son controle de specificite politique est net.
- **Le resultat global est donc mixte, et c'est le resultat.** Il n'est ni « asymetrie etablie » ni
  « asymetrie refutee » au sens de la section 7 : deux quantites passent Holm mais une seule passe
  les quatre conditions. Le preenregistrement appelle ce cas **« asymetrie non concluante »**, et
  ce rapport l'ecrit ainsi, en nommant la quantite qui tient et celles qui tombent.

---

## 7. Ce que ce resultat dit a Amir

Sans menagement et sans jugement, en langage courant.

**1. Ta phrase, telle que tu la dis, ne tient pas.** « La droite a plus de diversite politique que
la gauche » suppose qu'on mesure de la diversite. Les deux facons naturelles de mesurer la
diversite d'un camp, la variete des reponses a chaque question et la richesse de la structure de
ses opinions, ne te donnent pas raison. La premiere, une fois qu'on a enleve l'effet mecanique de
la position des questions, ne separe plus les camps du tout : +0,0003, autant dire rien, et c'est
pareil sur cinq jeux de donnees differents et treize mille personnes. La seconde te donne raison
sur le GSS, mais elle te la donne aussi sur les questions qui n'ont rien de politique, et elle
s'inverse sur Twin. Une mesure qui dit la meme chose de l'avortement et de « avez vous un
ordinateur » ne mesure pas de la politique.

**2. Il reste une chose, et elle est solide.** Quand on demande combien de combinaisons de reponses
differentes un camp produit reellement, comparees a celles que ses propres opinions moyennes
autorisent, la gauche en perd **deux fois et demie plus** que la droite : elle laisse tomber 11,6
pour cent des combinaisons possibles, la droite 4,8 pour cent. Autrement dit : **savoir ce qu'un
electeur de gauche pense de l'avortement te dit beaucoup plus sur ce qu'il pense du reste, que la
meme information pour un electeur de droite.** Ce resultat resiste a tout ce qu'on lui a oppose, y
compris au controle qui avait tue le fameux 1,12. Il se replique sur les quatre panels de l'enquete
officielle americaine, sur quinze ans, avec des gens qui n'ont rien a voir les uns avec les autres.

**3. Mais ce n'est pas « la droite est diverse », c'est « la gauche est serree ».** Le camp du
centre est au meme niveau que la droite, et il la depasse meme sur l'autre mesure. Ce que les
donnees separent, c'est la gauche du reste du monde, pas la droite du reste du monde. Si tu veux
une phrase vraie, c'est celle la : **la gauche americaine est le camp dont les opinions sont les
plus liees entre elles.** Elle est moins flatteuse pour la droite qu'elle n'en a l'air, et elle est
deja publiee : Cely le mesure en 2025 sur 131 partis dans 15 pays europeens, et le dossier l'avait
deja sous une autre forme, la correlation entre l'axe economique et l'axe social qui vaut 0,447 a
gauche et 0,311 a droite.

**4. Ce que ca te coute, et ce que ca te rapporte.** Ca te coute la version forte de ta croyance,
celle qui parle de « diversite de pensee » et qui suggere une qualite cognitive : rien dans ces
donnees ne la soutient, et le papier que tu as vu passer sur Reddit dit lui meme le contraire de la
legende qu'on lui a collee. Ca te rapporte une quantite propre, orthogonale a la position, qui
n'existait pas dans le dossier ce matin, qui repond a la question que `a37` posait a Simon, et qui
est exactement ce que tu voulais : une prediction qui pouvait couter, qui a couvert une partie de
la mise.

**5. Ce que ca te coute aussi, cote dossier.** Le dossier avait ecrit qu'il n'y avait pas
d'asymetrie robuste au controle des items. C'est faux sur une quantite, et c'est ecrit ici. La
phrase publique du dossier doit etre restreinte : *la dispersion interne d'un camp n'est pas une
propriete du camp*, oui, et c'est demontre deux fois maintenant ; mais *la contrainte entre items a
l'interieur d'un camp*, elle, en est une.

---

## 8. Ce que cela change au dossier

**A `a37`.** La question 1 de sa section 10, « y a t il une mesure de consensus intra camp qui soit
orthogonale a la position ? », recoit une reponse : **oui, une sur trois candidates**, et c'est le
comptage de profils distincts en exces du nul de gabarit. Sa conclusion de section 4 n'est pas
contredite : elle porte sur la dispersion marginale item par item, et Q1 la confirme sur cinq jeux
au lieu d'un. **Proposition de restriction, a valider par Amir :** ecrire desormais « la dispersion
interne d'un camp sur un item n'est pas une propriete du camp, c'est une consequence de sa
position », **et ne jamais generaliser cette phrase a la structure entre items**, ou l'asymetrie
existe et vaut 12,41 [11,96 ; 12,86] sur le GSS.

**A `a30`.** Son interdiction numero 1, « interdit d'ecrire que la droite est plus heterogene que
la gauche sans nommer le domaine », est confirmee par le controle `P0` : le domaine est le seul
endroit ou l'effet vit. **Proposition d'ajout, a valider par Amir :** *interdit de citer une
asymetrie de diversite entre camps sans dire si elle est une asymetrie de dispersion, qui n'existe
pas apres controle de position, ou une asymetrie de contrainte, qui existe et se replique.*

**A `a32`.** Le papier de Lüders desavoue explicitement la glose de Reddit et attribue l'asymetrie
au symbolique. Nos trois quantites vont dans le meme sens : la seule qui tient mesure de la
contrainte entre croyances, pas de la tolerance ni de l'ouverture, et elle place le centre au meme
niveau que la droite. **Rien ici ne soutient la glose ; une partie soutient le papier.**

**A `BRAINSTORM-DECISIONS` D4.** Le test T1 a zero cout que D4 prevoyait est fait, et il est fait
sur une quantite residuelle et non sur le rapport brut : section 2.1. Le critere de chute de D4,
« si un generateur nul reproduit toute l'asymetrie a partir des seules marges, la quantite est un
artefact de taux de base », est teste et **n'est pas atteint pour Q2** : le nul contre nul vaut
+0,03 contre +12,41.

---

## 9. Ce que je n'ai pas pu verifier

1. **Q2 depend de la taille de l'echantillon, et je n'ai pas de forme normalisee preenregistree.**
   Le contraste passe de +9,04 a +13,53 quand `n_egal` passe de 166 a 332. La lecture relative de
   la section 1, 11,6 pour cent contre 4,8 pour cent, est descriptive et n'a pas ete preenregistree,
   donc elle ne porte aucun test. Une version normalisee proprement construite manque.
2. **Le contraste droite moins centre n'a pas d'intervalle.** Il n'etait pas dans les familles de
   tests, et il n'a pas ete estime par bootstrap. C'est pourtant lui qui decide entre « la droite »
   et « ne pas etre de gauche », et il est publie comme une simple difference de moyennes.
3. **Le perimetre `P1` de Twin ne compte que dix items**, et les sous ensembles de Q2 en comptent
   dix : il n'existe qu'un seul sous ensemble, donc l'intervalle de Twin ne porte que sur les
   personnes. La replication de Twin vaut pour son signe et pas pour sa precision.
4. **Le controle `P0` compare le politique au non politique du meme questionnaire.** Un style de
   reponse propre aux items d'opinion, mais non politique, passerait ce controle sans etre detecte.
   Le dossier n'a pas de troisieme perimetre d'items d'opinion non politiques.
5. **Q1 n'est pas orthogonale a la polarite**, et le rapport le mesure au lieu de le supposer :
   pente +0,158, R2 0,248. Le critere O du preenregistrement n'a donc ete satisfait pleinement que
   par Q2 et Q3 ; pour Q1, le residu porte encore un effet de position du second ordre, et son
   bilan agrege nul est une compensation, pas une absence.
6. **Les items des panels NORC ne sont pas exactement ceux du GSS de Stanford** : 76 orientes sur
   118 au lieu de 79 sur 149, et le codage ordinal est reconstruit depuis les codes numeriques des
   fichiers `.dta`. Les valeurs numeriques des deux perimetres GSS ne se comparent pas chiffre a
   chiffre ; seuls leurs signes se comparent.
7. **Le plancher de reinterrogation du GSS de Stanford est a deux semaines**, donc le plus favorable
   de tous. [MESURE, `a12`] La fidelite humaine tombe de 77,79 a 67,45 pour cent entre deux semaines
   et quatre ans. Les panels donnent un plancher a deux et quatre ans, mais seulement pour Q1 : je
   n'ai pas recalcule Q2 et Q3 sur leurs vagues tardives.
8. **Aucune des trois quantites n'a d'homologue publie**, donc aucune valeur de reference exterieure
   ne peut confirmer que mes chiffres sont dans le bon ordre de grandeur.
9. **Le nombre de lignes completes n'est pas rapporte camp par camp dans le texte.** Il est dans
   `d4-nuls.csv` par construction, puisque le masque du camp est conserve a l'identique par le
   generateur nul, mais je n'ai pas verifie item par item que le taux de non reponse ne differe pas
   entre camps d'une facon qui interagirait avec le comptage de patrons.
10. **Aucune figure n'a ete produite.** Les sept tableaux `d4-*.csv` portent tout ce qui est cite.

---

## 10. Questions ouvertes pour Simon

1. **La quantite qui survit a t elle un nom ?** « Nombre de profils de reponses distincts d'un
   groupe, en exces du nombre qu'un tirage independant dans les marginales de ce meme groupe
   produirait » : est ce une redescription de la contrainte ideologique de Converse, une entropie
   conjointe deguisee, ou un objet que l'ecologie ou la genetique des populations appelle
   autrement ? Si le nom existe, il faut le prendre plutot que d'en inventer un.
2. **Pourquoi Q2 et Q3 divergent elles ?** Les deux mesurent la contrainte entre items, l'une par le
   comptage de combinaisons, l'autre par le spectre de la matrice de correlation. Q2 est
   politiquement specifique et se replique cinq fois sur cinq ; Q3 ne l'est pas et s'inverse sur
   Twin. Est ce que le comptage de patrons capte des dependances d'ordre superieur que la matrice de
   correlation par paires ne voit pas, ou est ce que Q3 est simplement contaminee par le style de
   reponse et Q2 protegee par sa discretisation ?
3. **L'inversion de Twin est elle un fait de population ou un fait d'items ?** Twin est le seul jeu
   ou Q3 s'inverse et c'est aussi le seul dont le perimetre politique compte dix items au lieu de
   soixante seize. Faut il refaire Q3 sur le GSS restreint a dix items pour separer les deux
   explications, ou est ce que dix items ne suffisent tout simplement pas a estimer une dimension
   effective ?
4. **Le controle `P0` est il le bon controle ?** Il oppose le politique au non politique a
   l'interieur du meme questionnaire. Existe t il, dans le GSS ou dans l'ESS, une batterie d'items
   d'opinion non politiques assez longue pour servir de troisieme perimetre ?
5. **La question qui interesse le projet, et qui n'est pas testee ici.** Q2 est une quantite
   orthogonale a la position, elle a une valeur humaine de reference et un plancher de bruit.
   **Que font les populations simulees de cette quantite ?** `a37` a montre que la simulation
   exagere la loi de consensus ; si elle exagere aussi la contrainte, alors le dossier tient une
   seconde loi humaine deformee par la machine, mesuree le meme jour sur les memes personnes. Est ce
   la quantite qu'il faut porter aux agents en priorite, ou est ce que le comptage de patrons est
   trop sensible au taux de reponses hors echelle des modeles pour servir d'instrument d'audit ?

---

## 11. Reproduction

```
.venv/bin/python analyses/d4_asymetrie_humains.py
```

Graine unique **20260909**, declaree dans le preenregistrement section 9 et dans
`d4_asymetrie_humains.GRAINE`. Duree mesuree, quatre coeurs : **1 minute 23 secondes**, panels
NORC compris. `--rapide` reduit tout d'un facteur cinquante pour un essai en dix secondes ;
`--sans-panels` saute la famille C.

**Fichiers produits.** Preenregistrement : `resultats/d4-preenregistrement.md`. Script :
`analyses/d4_asymetrie_humains.py`. Tableaux : `resultats/d4-contrastes.csv`,
`d4-nuls.csv`, `d4-q1-par-item.csv`, `d4-polarite.csv`, `d4-planchers.csv`, `d4-controles.csv`,
`d4-verdicts.csv`. Rapport : `resultats/d4-resultats.md`. **Aucun fichier existant n'a ete
modifie.**
