# A12. Le delai de retest n'est pas controle par la litterature

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md` et de la
lecture integrale du papier de reference `a14-lecture-2411-10109-v3.md`. Le corps du rapport
n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 7 septembre. Recalculs :
`analyses/a19_denominateurs.py`, tableaux `resultats/a19-test-retest-par-jeu.csv` et
`a19-income-baselines.csv`. Aucun appel de modele, aucun script existant modifie.

### E1. Section 3 : le champ des auteurs porte sur 150 items, pas sur 177. Objection a17 6.1, contradiction C9.

**Phrase d'origine.** "appliquee aux deux vagues humaines de l'archive elle donne 0,795002 sur
les 149 items contre 0,795253 pour le champ `p_wave1__p_wave2__accuracy` calcule par les auteurs
sur les **177 items**."

**Correction.** Le champ des auteurs porte sur **150 items**. La consistance test retest
humaine recalculee sur les quatre jeux d'items le montre sans ambiguite : 177 items 81,2491 ;
169 items 81,0072 ; **150 items 79,5253** ; 149 items 79,5002. La valeur publiee 79,5253 est
reproduite exactement sur les 150 items et sur aucun autre jeu. [MESURE,
`a19-test-retest-par-jeu.csv`]

Le controle de definition reste valide, il change seulement de denominateur de reference : notre
0,795002 sur 149 items et le 0,795253 des auteurs sur 150 items different d'un item, pas d'une
definition.

### E2. Section 4.2 : le 0,860 ne valide pas la chaine de calcul. Objection a17 6.2, contradiction C10.

**Phrase d'origine.** "Le 0,860 reproduit le 86 pour cent publie par Stanford pour la condition
composite, ce qui valide la chaine de calcul."

**Correction.** Notre 0,860 est un rapport de moyennes ; la definition des auteurs est une
normalisation individuelle puis moyenne, qui donne **0,865** [a14 section 2.3]. Deux estimateurs
differents qui arrondissent au meme 0,86 ne se valident pas l'un l'autre. La phrase de validation
est retiree. Le tableau 4.2 est inchange, seule sa lecture l'est : il faut lire "notre estimateur
donne 0,860 la ou l'estimateur des auteurs donne 0,865, ecart 0,005".

### E3. Sections 4.1 et 4.2 : `income` figure dans les items et `gss_v6` le recopie. Objection a17 2.2 et 6.3, contradiction C6.

**Correction.** `income` figure dans les 149 items comme dans les 118 items du noyau commun, et
la generation `gss_v6` le recopie a **0,994**, contre 0,634 de consistance test retest humaine
sur le meme item. C'est une fuite de meme nature que `polviews`, que a1 avait ecartee pour ce
motif. L'effet mesure sur le GSS est de **0,28 point** sur le score brut de `v6`, qui passe de
0,5818 a 0,5790 sur 148 items ; B1 et B2 ne bougent pas, 0,6209 vers 0,6216 et 0,6717 vers
0,6719. [MESURE, `a19-income-baselines.csv`]

Consequence pour ce rapport : toutes les lignes `gss_v6` des tableaux 4.1 et 4.2 sont
surestimees d'environ 0,3 point de score brut, donc d'environ 0,4 point de score normalise.
**Aucune conclusion de a12 ne repose sur `v6`** : le rapport porte sur le denominateur, qui est
identique pour toutes les conditions, et les gains de 8,4 a 14,8 points sont inchanges.

### E4. Ce que ces errata ne changent pas

Les trois denominateurs, 77,79 pour cent a deux semaines, 69,53 a deux ans et 67,45 a quatre ans
sur les 118 items du noyau commun ; le franchissement de 1,008 a quatre ans sur les 149 items ;
la non uniformite du delai par famille d'items ; la sensibilite au traitement des non reponses ;
et les six points de la section "Autorise" ne sont pas touches.

**Un point de la section "Ce que je n'ai pas pu verifier" est leve.** Le point 5, "le texte
integral du papier de Stanford", est verifie : la version 3 integrale, 86 pages, annexes
comprises, ne discute nulle part le choix du delai de deux semaines, ne le compare a aucun autre
denominateur et ne conduit aucune analyse de sensibilite dessus. L'angle A8 conserve sa nouveaute
[a14 section 1].

---

Mesure du denominateur de normalisation a trois delais : deux semaines, deux ans, quatre ans.
Ecrit le 7 septembre 2026. Scripts `analyses/a12_telecharger_panel.py`,
`analyses/a12_retest_delai.py`, `analyses/a12_sensibilite_dk.py`. Aucun appel de modele de
langage. Tableaux dans `resultats/a12-*.csv`.

---

## Reponse en une ligne

**Sur exactement les memes 118 items du GSS et avec exactement la definition de Stanford, la
consistance test retest des memes personnes vaut 77,79 pour cent a deux semaines, 69,53 pour
cent a deux ans et 67,45 pour cent a quatre ans ; changer de denominateur deplace le score
normalise de l'agent composite de 0,844 a 0,944 puis a 0,973, soit dix a treize points de
score normalise gagnes sans qu'aucun agent ne s'ameliore.** [MESURE]

Sur les 149 items de a2 et le denominateur publie de 79,53 pour cent, l'ecart est encore plus
large : 0,860 a deux semaines contre 0,978 a deux ans et **1,008 a quatre ans**, c'est a dire
que l'agent composite devient nominalement plus fidele a la personne que la personne ne l'est
a elle meme. [MESURE]

---

## 1. Acces aux donnees, ce qui a ete verifie

**Le panel GSS se telecharge sans compte, en une commande.** [CONFIRME]
Page d'index : https://gss.norc.org/us/en/gss/get-the-data/stata.html
Quatre archives, toutes en HTTP 200 avec `content-type: application/zip`, sans jeton, sans
formulaire, sans acceptation de licence prealable :

| panel | URL (prefixe `https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/`) | octets | vagues |
|---|---|---|---|
| 2006-2010 | `GSS_2006_Panel_Stata.zip` | 2 810 743 | 2006, 2008, 2010 |
| 2008-2012 | `GSS_2008_Panel_stata.zip` | 2 366 403 | 2008, 2010, 2012 |
| 2010-2014 | `GSS_2010_Panel_stata.zip` | 2 226 711 | 2010, 2012, 2014 |
| 2016-2020 | `GSS_2020_panel_stata_1a.zip` | 11 847 819 | 2016 ou 2018, puis 2020 |

Total 19,3 Mo compresses, 65,2 Mo decompresses, codebook du panel 2016-2020 inclus. Aucun
telechargement de plusieurs gigaoctets n'a ete necessaire. Empreintes SHA-256 dans
`data/gss-panel/PROVENANCE.md`.

**La licence.** Conditions generales de NORC, https://gss.norc.org/us/en/gss/terms-and-conditions.html :
*"No part of the contents of NORC websites may be reproduced, stored, or transmitted in any
form or by any means, electronic or mechanical, in whole or in any part, without the express
written consent of NORC."* [CONFIRME]
Lecture operationnelle : le telechargement et l'analyse locale ne demandent aucune demarche,
**la redistribution est interdite**. Consequence appliquee ici : les fichiers restent dans
`data/gss-panel/`, qui est dans le `.gitignore` ; tous les fichiers produits par a12 sont des
agregats par item, par famille ou par centile, aucun ne contient de ligne individuelle.
Le point deja note dans `exploration/07-ethique-conformite.md`, "compte requis sur le Data
Explorer", vaut pour l'outil d'exploration en ligne, **pas pour les fichiers de donnees eux
memes**, qui sont en telechargement direct. C'est une correction a apporter au tableau
section 1.A de ce rapport. [CONFIRME]

**Structure des panels, verifiee dans les fichiers.** [MESURE]
Les panels 2006, 2008 et 2010 sont a trois vagues sur les memes personnes, a deux ans
d'intervalle : ils fournissent donc deux paires a deux ans et une paire a quatre ans chacun.
Le panel 2016-2020 n'est pas de meme nature : les champs `year_1a` et `year_1b` sont
mutuellement exclusifs. La cohorte 2016 (2 867 personnes) est reinterrogee en 2020 seulement,
soit quatre ans ; la cohorte 2018 (2 348 personnes) est reinterrogee en 2020, soit deux ans.
Personne n'est interroge en 2016 puis en 2018. Onze paires de vagues au total.

---

## 2. Appariement des items, et ce qui ne s'apparie pas

Cible : les **149 items** de `analyses/a2_baselines_gss.py`, c'est a dire les 177 colonnes de
l'archive OSF moins la liste d'exclusion de Stanford moins `polviews`. La liste d'exclusion
est recopiee a l'identique, pas reinterpretee.

Deux conventions de nommage de l'archive ont ete traduites, elles sont documentees dans
`figure2/data/question_master/gss/main.csv` :

- le suffixe `/y` designe un item pose en deux versions de ballot, par exemple `NATSPAC` et
  `NATSPACY`, que Stanford fusionne en une seule cible. Cote panel, les deux variables
  existent et sont fusionnees dans le meme ordre : la premiere renseignee gagne. [MESURE]
- l'asterisque final (`spdeg*`, `relig16*`, `compuse*`, `usewww*`, `uscitzn*`, `jew16*`) est
  un marqueur de l'archive, pas un joker : il est retire.

**Controle de la fusion de ballot.** La part de personnes qui changent de version de ballot
entre deux vagues est **exactement 0 pour cent dans les trois panels de 2006 a 2014** et
**3,9 a 4,4 pour cent dans le panel 2016-2020**. [MESURE] L'appariement ne cree donc
pratiquement pas de faux desaccords dus a une reformulation de la question.

**Ce qui ne s'apparie pas.** Trois items n'existent dans aucun panel : `divorced`,
`wrkgovt1`, `wrkgovt2`. Les deux derniers sont les versions renumerotees de `WRKGOVT` apres
la refonte de 2021 et n'ont pas ete apparies volontairement : le panel contient `wrkgovt`
sans suffixe, et decider que `wrkgovt1` et `wrkgovt2` designent tous deux `wrkgovt` aurait
compte deux fois la meme variable. `divorced` n'a pas d'equivalent evident, `divorce` du GSS
posant une question differente. [MESURE]

Le reste depend du panel, parce que le GSS a ajoute des items au fil des annees :

| panel | items apparies sur 149 | manquants |
|---|---|---|
| 2016-2020 | 146 | les trois ci dessus |
| 2010-2014 | 137 | `dwelown16`, `hunt1`, `if16who`, `mnthsusa`, `pres16`, `union1`, `vote16`, `wksub1`, `wksup1` |
| 2008-2012 | 133 | les precedents plus `compuse*`, `natenrgy`, `usewww*`, `webmob` |
| 2006-2010 | 132 | les precedents plus `wlthhsps` |

Les items d'elections 2016 (`vote16`, `pres16`, `if16who`) et d'usage numerique (`compuse*`,
`usewww*`, `webmob`) n'existent evidemment pas dans les panels anterieurs. [MESURE]

---

## 3. Les trois denominateurs

Definition employee des deux cotes, celle de Stanford : **egalite exacte de la modalite**
entre les deux passations, moyennee d'abord sur les items renseignes chez une personne, puis
sur les personnes. Controle de la definition : appliquee aux deux vagues humaines de
l'archive elle donne 0,795002 sur les 149 items contre 0,795253 pour le champ
`p_wave1__p_wave2__accuracy` calcule par les auteurs sur les 177 items. [MESURE]

### 3.1 Sur le noyau commun, la seule comparaison honnete

Une part de l'ecart pourrait venir de la liste d'items et non du delai, puisque les panels
n'apparient pas les 149. Le **noyau commun** est l'ensemble des items mesures dans les onze
paires de vagues a la fois, soit **118 items**. Les trois denominateurs sont recalcules sur
ces 118 items exactement, des deux cotes.

| denominateur | delai | n personnes evaluees | consistance | IC 95 pour cent |
|---|---|---|---|---|
| Stanford, archive OSF | 2 semaines | 1 052 | **0,7779** | [0,7723 ; 0,7831] |
| panels GSS, mise en commun | 2 ans | 9 556 | **0,6953** | [0,6936 ; 0,6969] |
| panels GSS, mise en commun | 4 ans | 4 683 | **0,6745** | [0,6721 ; 0,6769] |

Bootstrap sur les personnes, 2 000 tirages, `bootstrap_personnes` de `a2_commun.py`.
Les intervalles ne se recouvrent pas, de loin. [MESURE]
Fichiers : `a12-noyau-commun.csv`, `a12-denominateurs-ic.csv`.

**8,26 points de consistance separent deux semaines de deux ans, 10,34 points separent deux
semaines de quatre ans.** Le passage de deux a quatre ans ne coute que 2,08 points de plus :
l'essentiel de la perte est deja consomme au bout de deux ans. [MESURE]

### 3.2 Sur les items propres a chaque panel, pour controle

| panel | paire | delai | n | consistance |
|---|---|---|---|---|
| Stanford | vague 1 contre vague 2, 149 items | 2 semaines | 1 052 | 0,7950 |
| 2006-2010 | 2006 contre 2008 | 2 ans | 1 536 | 0,6903 |
| 2006-2010 | 2008 contre 2010 | 2 ans | 1 276 | 0,7054 |
| 2008-2012 | 2008 contre 2010 | 2 ans | 1 581 | 0,6931 |
| 2008-2012 | 2010 contre 2012 | 2 ans | 1 294 | 0,7096 |
| 2010-2014 | 2010 contre 2012 | 2 ans | 1 551 | 0,6949 |
| 2010-2014 | 2012 contre 2014 | 2 ans | 1 304 | 0,7094 |
| 2016-2020 | 2018 contre 2020 | 2 ans | 1 014 | 0,6937 |
| **mise en commun** | | **2 ans** | **9 556** | **0,6991** |
| 2006-2010 | 2006 contre 2010 | 4 ans | 1 276 | 0,6715 |
| 2008-2012 | 2008 contre 2012 | 4 ans | 1 294 | 0,6829 |
| 2010-2014 | 2010 contre 2014 | 4 ans | 1 304 | 0,6807 |
| 2016-2020 | 2016 contre 2020 | 4 ans | 809 | 0,6786 |
| **mise en commun** | | **4 ans** | **4 683** | **0,6784** |

Les sept estimations a deux ans tiennent dans une fourchette de 1,9 point, les quatre
estimations a quatre ans dans une fourchette de 1,1 point, sur quatre cohortes distinctes
couvrant 2006 a 2020 et deux modes de collecte. **Le resultat n'est pas un artefact de
periode.** [MESURE] Fichier : `a12-synthese-delais.csv`.

### 3.3 La distribution par individu, pas seulement la moyenne

Meme lecture que la section 6 de `a1-double-distorsion.md`, transposee aux longs delais.

| source | delai | moyenne | ecart type | p10 | mediane | p90 | part sous 70 pour cent |
|---|---|---|---|---|---|---|---|
| Stanford | 2 semaines | 0,7950 | 0,0867 | 0,698 | 0,812 | 0,886 | **10,6 pour cent** |
| 2016-2020 | 2 ans | 0,6937 | 0,0820 | 0,588 | 0,700 | 0,794 | **49,5 pour cent** |
| 2016-2020 | 4 ans | 0,6786 | 0,0775 | 0,577 | 0,688 | 0,771 | **57,6 pour cent** |
| 2006-2010 | 4 ans | 0,6715 | 0,0829 | 0,561 | 0,678 | 0,771 | **60,8 pour cent** |

L'ecart type individuel est **le meme** aux trois delais, environ 8 points. Le delai deplace
toute la distribution vers le bas sans l'elargir. Un point qui compte pour a1 : la
correlation entre fidelite de l'agent et stabilite propre de la personne, r = 0,684, a ete
mesuree sur un plancher a deux semaines. Rien ici ne dit ce qu'elle deviendrait sur un
plancher a deux ans, et la question se pose puisque le classement des personnes n'est pas le
meme. [HYPOTHESE]

### 3.4 Sensibilite : le "ne sait pas" gonfle le chiffre du panel

Dans l'archive de Stanford il n'y a **aucune cellule manquante** : 1 052 x 177 reponses,
toutes remplies. [MESURE] Dans le GSS de terrain il y a des "ne sait pas", des refus et des
"passe sur le web". Le calcul principal les traite en manquants, ce qui retire du calcul les
reponses les plus fragiles et tire la consistance du panel **vers le haut**.

`a12_sensibilite_dk.py` refait le calcul en comptant "ne sait pas", "pas de reponse", "refus"
et "passe sur le web" comme une modalite unique. Les codes `i` (question non posee), `x`,
`y` et `c` restent des manquants dans les deux variantes.

| variante | 2 ans | 4 ans |
|---|---|---|
| non reponse traitee en manquant, calcul principal | 0,6991 | 0,6784 |
| non reponse comptee comme modalite | **0,6741** | **0,6541** |

[MESURE] Le chiffre du panel retenu dans ce rapport est donc **un majorant**. Le retenir rend
la conclusion conservatrice : le vrai ecart entre deux semaines et deux ans est plus grand
que celui que ce rapport publie. Ce script reproduit par ailleurs a la sixieme decimale les
onze valeurs du calcul principal dans sa variante basse, ce qui vaut controle croise de deux
lectures independantes des fichiers Stata. [MESURE]

---

## 4. Le chiffre du papier : les scores normalises recalcules

Les scores bruts des quatre conditions d'agents sont recalcules sur les memes items que le
denominateur, avec `exactitude_par_personne` de `a2_commun.py`.

### 4.1 Noyau commun, 118 items, la version defendable

| condition | score brut | normalise, 2 semaines | normalise, 2 ans | normalise, 4 ans | gain 2 ans | gain 4 ans |
|---|---|---|---|---|---|---|
| agents composite | 0,6563 | **0,844** | **0,944** | **0,973** | **+10,0 pts** | **+12,9 pts** |
| agents enquete | 0,6334 | 0,814 | 0,911 | 0,939 | +9,7 pts | +12,5 pts |
| agents entretien (v3) | 0,6252 | 0,804 | 0,899 | 0,927 | +9,6 pts | +12,3 pts |
| agents demographiques (v6) | 0,5501 | 0,707 | 0,791 | 0,816 | +8,4 pts | +10,8 pts |

[MESURE] Fichier `a12-normalisation-noyau.csv`.

### 4.2 Les 149 items de a2 contre le denominateur publie de 79,53 pour cent

| condition | score brut | normalise, 2 semaines | normalise, 2 ans | normalise, 4 ans | gain 2 ans | gain 4 ans |
|---|---|---|---|---|---|---|
| agents composite | 0,6839 | 0,860 | 0,978 | **1,008** | **+11,8 pts** | **+14,8 pts** |
| agents entretien (v3) | 0,6565 | 0,826 | 0,939 | 0,968 | +11,3 pts | +14,2 pts |
| agents enquete | 0,6510 | 0,819 | 0,931 | 0,960 | +11,2 pts | +14,1 pts |
| agents demographiques (v6) | 0,5818 | 0,732 | 0,832 | 0,858 | +10,0 pts | +12,6 pts |

[MESURE] Fichier `a12-normalisation.csv`. Le 0,860 reproduit le 86 pour cent publie par
Stanford pour la condition composite, ce qui valide la chaine de calcul.

**Ce qu'il faut retenir du tableau.** Le meme agent, sur les memes reponses, sans qu'aucune
ligne de code du systeme simule ne change, passe de 86 a 98 pour cent de la performance
humaine si l'on choisit un denominateur a deux ans, et **franchit 100 pour cent a quatre
ans**. Un franchissement de 100 pour cent est une propriete du denominateur, pas une
propriete de l'agent : il signifie seulement que l'agent est plus proche de la vague 1 que ne
l'est la meme personne quatre ans plus tard. Un lecteur qui compare deux scores normalises
issus de deux protocoles de retest differents compare deux quantites qui ne sont pas la meme.

**L'ecart de rendement.** Le gain est plus grand pour les conditions riches en information
(+10,0 points pour le composite) que pour l'agent demographique (+8,4 points). Changer de
denominateur n'est donc pas une translation : cela **etire aussi l'echelle**, et cela ecarte
les conditions les unes des autres. L'ecart entre agent composite et agent demographique
passe de 13,7 points de score normalise a deux semaines a 15,3 points a deux ans. [MESURE]

---

## 5. Item par item : le delai n'est pas uniforme

137 items sont mesures aux deux delais. Correlation de Pearson entre consistance a deux
semaines et consistance a deux ans : **0,866**, correlation de rang 0,861. Perte moyenne
7,73 points, ecart type 6,82 points, de -10,7 a +33,0 points. [MESURE]
Fichier `a12-items-stables-instables.csv`.

### 5.1 Les items qui perdent le plus

| item | libelle abrege | 2 semaines | 2 ans | perte |
|---|---|---|---|---|
| `if16who` | pour qui vous seriez vous prononce en 2016 | 0,907 | 0,577 | **33,0 pts** |
| `attend` | frequence de frequentation religieuse | 0,747 | 0,434 | **31,3 pts** |
| `marhomo` | le mariage homosexuel doit il etre reconnu | 0,766 | 0,526 | 24,0 pts |
| `joblose` | probabilite de perdre son emploi | 0,779 | 0,583 | 19,6 pts |
| `letin1a` | nombre d'immigrants a admettre | 0,688 | 0,498 | 19,0 pts |
| `finalter` | situation financiere en amelioration ou non | 0,706 | 0,522 | 18,4 pts |
| `health` | etat de sante declare | 0,799 | 0,617 | 18,3 pts |
| `pray` | frequence de priere | 0,724 | 0,545 | 17,9 pts |
| `pillok` | contraception pour les adolescents | 0,656 | 0,480 | 17,6 pts |
| `spanking` | fessee dans l'education | 0,740 | 0,570 | 17,0 pts |

Trois logiques distinctes se lisent dans cette liste, et une seule est de l'instabilite
d'opinion. `if16who` et `joblose` et `finalter` et `health` sont des **items dont le referent
change** : la question ne porte plus sur le meme monde deux ans plus tard. `marhomo` et
`pillok` sont des items sur lesquels l'opinion americaine s'est deplacee en bloc pendant la
periode. `attend` et `pray` sont des echelles de frequence a nombreuses modalites, ou une
petite derive de comportement suffit a changer de case. [PROBABLE]

### 5.2 Les items qui ne perdent rien, ou qui gagnent

Onze items ont une consistance **plus haute** a deux ans qu'a deux semaines chez Stanford :
`granborn` (+10,7 pts), `income` (+9,2), `wksub1` (+8,6), `polattak/y` (+8,0), `xmarsex`
(+7,8), `reborn` (+4,1), `trust` (+3,4), `partfull` (+3,2), `spfund` (+3,1), `relig16*`
(+2,3). [MESURE] Ce ne peut pas etre un effet du delai. Ce sont des items ou l'echantillon
Bovitz en ligne est simplement moins consistant que le panel NORC en face a face, ou bien ou
la modalite proposee differe entre les deux instruments. C'est le controle negatif du
resultat : il montre que la comparaison mesure aussi une difference d'echantillon, et pas
seulement une difference de delai. Ce point est repris en section 6.

### 5.3 Par famille thematique

Familles reprises telles quelles de `FAMILLES` dans `a2_baselines_gss.py`.

| famille | n | 2 sem. | 2 ans | 4 ans | perte a 2 ans | perte a 4 ans |
|---|---|---|---|---|---|---|
| confiance dans les institutions (`con*`) | 13 | 0,721 | 0,614 | 0,582 | **10,7 pts** | 13,9 pts |
| roles de genre (`fe*`) | 5 | 0,689 | 0,586 | 0,575 | **10,3 pts** | 11,4 pts |
| depenses publiques (`nat*`) | 17 | 0,747 | 0,650 | 0,622 | 9,7 pts | 12,5 pts |
| hors famille | 79 | 0,791 | 0,718 | 0,695 | 7,4 pts | 9,2 pts |
| avortement (`ab*`) | 7 | 0,917 | 0,848 | 0,842 | 6,9 pts | 7,5 pts |
| libertes civiles (`spk`/`col`/`lib`) | 11 | 0,838 | 0,785 | 0,777 | 5,3 pts | 6,1 pts |
| fin de vie (`suicide`/`letdie`) | 5 | 0,883 | 0,853 | 0,844 | **3,1 pts** | 4,0 pts |

[MESURE] Fichier `a12-familles.csv`.

**Le delai frappe donc de facon tres inegale, dans un rapport de 3,5 entre la famille la plus
touchee et la moins touchee.** Les items de position morale stable (avortement, fin de vie,
libertes civiles) resistent ; les items d'evaluation conjoncturelle (confiance dans les
institutions, depenses publiques souhaitees) s'effondrent. La famille `con*` est justement
celle ou la mesure de confiance a bouge le plus dans la periode : la part declarant "hardly
any" confiance dans les institutions financieres passe de 15 pour cent en 2006 a 42 pour cent
en 2010, chiffre publie par NORC lui meme. [CONFIRME]
https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR119.pdf

**Consequence pour la normalisation.** Un denominateur a long delai n'avantage pas les agents
de facon uniforme : il les avantage **le plus sur les items d'opinion conjoncturelle**, qui
sont precisement ceux qu'un simulateur de population est cense predire et ceux ou il est le
moins bon. Un jeu d'evaluation riche en `con*` et `nat*` normalise a deux ans est le
protocole le plus flatteur qu'on puisse construire sans tricher. [MESURE] pour la mesure. Aucune intention n'est pretee a qui que ce soit, ce protocole n'existe dans aucun papier lu.

### 5.4 Ce qui ne cause pas l'ecart

Trois explications alternatives ont ete testees et ecartees. [MESURE]

- **Le nombre de modalites.** Correlation entre la perte a deux ans et le nombre de modalites
  observees dans le panel : 0,146. Faible.
- **Le desaccord de hasard.** L'accord attendu sous independance, indice de Simpson de la
  marginale, est presque identique des deux cotes : correlation 0,803 entre les deux sources,
  ecart moyen -0,0067. Les deux instruments proposent donc bien les memes modalites avec des
  distributions comparables, l'appariement ne cree pas d'artefact d'echelle.
- **Un effet de plafond.** La regression de la perte sur la consistance a deux semaines donne
  une pente de -0,133 et une correlation de -0,199. Les items deja instables a deux semaines
  perdent un peu moins, mais tres peu : l'effet du delai n'est pas la simple compression d'un
  plafond.

---

## 6. Bovitz en ligne contre NORC en face a face

Le point faible du resultat, ecrit en clair : les deux mesures ne portent pas sur le meme
echantillon, ni sur le meme mode de collecte, ni sur la meme annee.

Test tente : caler sur chaque item une droite en logarithme du delai, a partir des deux
points a deux et quatre ans, puis extrapoler a deux semaines et comparer a ce que Stanford
observe. Le modele est le plus pauvre qui reste defendable, la perte de consistance ralentit
avec le temps. L'extrapolation porte sur deux ordres de grandeur, ce qui est enorme.

Resultat sur 134 items : moyenne extrapolee a deux semaines **0,818** (apres bornage a 1,
sept items depassaient 1), moyenne observee chez Stanford **0,786**. Residu moyen
**-0,032**, mediane -0,030 ; Stanford est au dessus de l'extrapolation pour seulement 35,8
pour cent des items. [MESURE] Fichier `a12-extrapolation.csv`.

Deux lectures, et je ne peux pas trancher entre elles avec ces donnees. [HYPOTHESE]

1. **L'echantillon Bovitz en ligne est un peu moins stable que le panel NORC en face a face.**
   Trois points de moins a delai equivalent. Ce serait attendu : administration sans
   enqueteur, moindre engagement, panel commercial.
2. **La decroissance n'est pas logarithmique.** Une part de l'incoherence est du bruit de
   mesure present des la seconde passation et qui ne decroit pas avec le delai. Un modele qui
   ajoute une constante de bruit predirait moins de 0,818 a deux semaines et reconcilierait
   les deux mesures sans invoquer de difference d'echantillon.

La lecture 2 est la plus probable au vu de la section 3.1 : la perte entre deux et quatre ans
n'est que de 2,08 points quand la perte entre deux semaines et deux ans est de 8,26 points.
La courbe est deja tres plate a deux ans, donc l'extrapolation lineaire en logarithme
surestime mecaniquement le point a deux semaines. **Cela renforce le resultat principal
plutot qu'il ne l'affaiblit** : si l'essentiel de la chute a lieu tres tot, alors le choix du
denominateur entre deux semaines et deux ans est encore plus determinant qu'une lecture
naive ne le suggere.

**Ce qui, en revanche, ne s'explique pas par le delai** : les onze items ou Stanford est
strictement moins consistant a deux semaines que le panel a deux ans, section 5.2. Sur
`confed`, `jobfind`, `wksub1`, `xmarsex`, `income`, `news`, `spfund`, `partfull`, le residu
depasse 18 points. Il existe donc bien une composante "echantillon et instrument" en plus de
la composante "delai", et ce rapport ne sait pas la separer proprement. [MESURE]

---

## 7. Ce que la litterature dit deja, et ce qu'elle ne dit pas

**Stanford ne cache rien, il ne compare pas.** Le papier dit explicitement que le
denominateur est la consistance test retest a deux semaines. [CONFIRME]
https://arxiv.org/abs/2411.10109v3 : *"agent accuracy reached 83% (interview only), 82%
(surveys only), and 86% (combined) of participants' two-week test-retest consistency"*.
Ce rapport ne reproche donc pas une dissimulation. Il constate qu'aucune comparaison a un
autre delai n'est fournie, et que le lecteur n'a aucun moyen de savoir que le chiffre bougerait
de dix points avec un autre protocole de retest.

**Le travail de reference sur la fiabilite du GSS existe et separe deux choses que ce rapport
melange.** Hout, M. et Hastings, O. P., *Reliability and Stability Estimates for the GSS Core
Items from the Three-wave Panels, 2006-2010*, GSS Methodological Report 119, NORC, juin 2012,
version corrigee aout 2014. [CONFIRME]
https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR119.pdf
Sur les memes panels que ceux utilises ici, avec le modele de Heise 1969 et Wiley 1970 dans
l'implementation d'Alwin 2007, les auteurs decomposent le desaccord entre vagues en **erreur
de mesure** (la fiabilite) et **changement reel de la position** (l'instabilite). Fiabilite
mediane par type d'item, table 2 :

| type d'item | fiabilite mediane | n |
|---|---|---|
| faits demographiques | 0,958 | 22 |
| faits religieux | 0,964 | 21 |
| croyances, sexualite | 0,839 | 16 |
| croyances, libertes civiles | 0,709 | 20 |
| croyances, genre et famille | 0,622 | 12 |
| croyances, racial | 0,490 | 16 |
| attitudes, toutes | 0,658 | 63 |
| attitudes, institutionnelles | 0,600 | 14 |
| attitudes, impots et depenses | 0,681 | 29 |

**Le classement est le meme que le mien.** Les familles ou MR119 trouve la plus faible
fiabilite (institutionnelles 0,600, genre et famille 0,622, impots et depenses 0,681) sont
exactement celles ou je mesure la plus grosse perte entre deux semaines et deux ans (`con*`
10,7 pts, `fe*` 10,3 pts, `nat*` 9,7 pts) ; celles ou MR119 trouve la plus forte fiabilite
(sexualite 0,839, libertes civiles 0,709) sont celles qui perdent le moins (`ab*` 6,9 pts,
`spk`/`col`/`lib` 5,3 pts). [MESURE]

Cette convergence est importante et elle coupe dans les deux sens. Elle valide la mesure. Mais
elle affaiblit l'interpretation "c'est le delai" : si les items qui perdent le plus a deux ans
sont ceux que MR119 juge les moins **fiables**, alors une partie de la perte est de l'erreur de
mesure, pas du changement d'opinion. Et l'erreur de mesure devrait etre presente a deux
semaines aussi. La resolution la plus vraisemblable est que l'echantillon Stanford, en ligne,
en deux passations rapprochees, avec un questionnaire force sans "ne sait pas", produit
mecaniquement moins d'erreur de mesure que le GSS de terrain. **Auquel cas l'ecart de dix
points melange trois choses : le delai, le mode de collecte et le traitement des non
reponses, et ce rapport ne les separe pas.** [PROBABLE]

**Ce que je n'ai trouve nulle part** : un travail qui normalise des scores d'agents de langage
par une consistance test retest mesuree sur le panel GSS, ni un travail qui signale
l'incomparabilite des scores normalises entre protocoles de retest. Twin-2K-500 normalise par
son propre retest et annonce 0,88 normalise, sans que le delai de ce retest soit compare a
celui de Stanford. [PROBABLE, recherche non exhaustive, quatre requetes]

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.**

1. Que la consistance test retest des memes personnes sur les items du GSS de Stanford vaut
   77,79 pour cent a deux semaines, 69,53 pour cent a deux ans et 67,45 pour cent a quatre
   ans, mesuree sur 118 items identiques et avec la definition des auteurs. [MESURE]
2. Que le score normalise d'une meme condition d'agent, sur les memes reponses, se deplace de
   dix points (deux ans) a treize points (quatre ans) selon le seul choix du denominateur, et
   franchit 100 pour cent a quatre ans sur les 149 items. [MESURE]
3. Que **deux scores normalises issus de deux protocoles de retest differents ne sont pas
   comparables**, et que le delai de retest doit etre declare au meme titre que le score.
   C'est la contribution de A8 et elle tient.
4. Que le choix du denominateur n'est pas une translation : il etire l'echelle et separe
   davantage les conditions riches des conditions pauvres, ce qui rend aussi incomparables les
   *ecarts* entre conditions. [MESURE]
5. Que le delai frappe dans un rapport de 3,5 selon la famille d'items, et le plus fort sur
   les items d'evaluation conjoncturelle. [MESURE]
6. Que le panel GSS se telecharge sans compte, que sa licence interdit la redistribution, et
   que la mention "compte requis" du rapport 07 doit etre corrigee. [CONFIRME]

**Interdit.**

1. **Ecrire que Stanford a choisi un denominateur flatteur.** C'est le contraire : deux
   semaines est le denominateur le plus severe des trois. La critique porte sur
   l'incomparabilite entre protocoles, pas sur un biais des auteurs.
2. **Ecrire que 8,26 points de l'ecart sont "du delai".** Ils melangent le delai, le mode de
   collecte (en ligne contre face a face), la population (panel commercial contre echantillon
   probabiliste), l'annee, et le traitement des non reponses. Ce rapport n'a pas de design qui
   separe ces facteurs. La formulation defendable est : "le denominateur mesure sur le panel
   GSS a deux ans vaut 69,5 pour cent, contre 77,8 pour cent pour le retest a deux semaines de
   Stanford, et ces deux quantites servent l'une et l'autre de denominateur dans la
   litterature".
3. **Publier le chiffre de 79,53 pour cent contre 69,91 pour cent** sans preciser que le
   premier porte sur 149 items et le second sur 124 a 131 : c'est le chiffre le plus
   spectaculaire du dossier et c'est le moins propre. Le couple a publier est **77,79 contre
   69,53 sur 118 items identiques**.
4. **Ecrire que les agents de Stanford depassent le plafond humain.** Le 1,008 est une
   propriete du denominateur a quatre ans, pas une performance. Le dire autrement serait
   exactement la faute que ce rapport denonce.
5. **Traiter le panel GSS comme un instrument identique.** Il comporte des non reponses que
   l'instrument de Stanford n'a pas, et les exclure gonfle son chiffre de 2,5 points.

---

## Ce que je n'ai pas pu verifier

1. **Le mode de collecte du retest de Stanford.** Je sais que la vague 2 a lieu environ deux
   semaines apres et reprend tous les instruments sauf l'entretien. Je ne sais pas si elle est
   administree exactement dans les memes conditions que la vague 1, ni si le questionnaire
   force la reponse. La totale absence de cellule vide dans l'archive suggere une reponse
   forcee, mais c'est une inference, pas une lecture du protocole. [HYPOTHESE]
2. **La date des deux vagues de Stanford.** L'archive OSF ne date pas les vagues. Impossible
   donc de verifier que les deux semaines sont bien deux semaines, ni de savoir si un evenement
   d'actualite est tombe entre les deux.
3. **La separation delai / mode / echantillon.** Il faudrait un retest court sur le meme panel
   NORC, ou un retest long sur le meme panel Bovitz. Ni l'un ni l'autre n'existe dans les
   donnees publiques que je connais.
4. **Le codebook du panel 2016-2020.** Telecharge, 14 Mo, non lu. Les chiffres d'effectifs
   (2 867 en 2016, 2 348 en 2018, 1 823 reinterroges en 2020) viennent de mon comptage direct
   dans le fichier, pas du codebook.
5. **Le texte integral du papier de Stanford.** Je n'ai lu que le resume en ligne et le
   materiel de replication. Il est possible que la version 3 discute deja le delai de retest
   quelque part dans les annexes. **A verifier avant toute soumission** : si les auteurs le
   signalent, l'angle A8 perd sa nouveaute, mais la mesure garde sa valeur.
6. **L'exhaustivite de la revue.** Quatre requetes web, aucun acces a une base bibliographique.
   L'affirmation "personne ne le signale" est un [PROBABLE] et pas davantage.
7. **Les items multi modalites fines.** `attend` et `pray` ont beaucoup de modalites ordonnees
   ou une derive d'un cran compte comme un desaccord total. La definition de Stanford, egalite
   exacte, est la bonne pour reproduire son chiffre, mais elle est severe pour ces items, aux
   deux delais.

---

## Questions ouvertes pour Simon

1. **Le papier A8 doit il porter sur la mesure ou sur la norme ?** La mesure est faite et elle
   tient en trois tableaux. La contribution plus ambitieuse serait de proposer une convention :
   tout score normalise declare son delai de retest, son mode de collecte et son traitement
   des non reponses, comme un intervalle de confiance declare son niveau. Est ce que ce genre
   de proposition de norme se publie, et ou ?
2. **Faut il aller chercher la separation delai / mode ?** Le seul design propre serait un
   retest court sur un echantillon probabiliste, ou un retest long sur un panel en ligne. Le
   LISS neerlandais et l'Understanding America Study ont des mesures repetees a delais
   variables sur le meme panel. Cela couterait une semaine et un formulaire d'acces. Est ce
   que ce controle est indispensable au papier, ou est ce qu'une limite honnete suffit ?
3. **Ce que MR119 propose est plus fin que ce que je fais.** Le modele de Heise separe l'erreur
   de mesure du changement reel. Applique aux deux vagues de Stanford il est inutilisable, il
   faut trois vagues. Mais applique au panel il donne un plafond humain **corrige de l'erreur
   de mesure**, qui serait le denominateur theoriquement correct pour normaliser un simulateur.
   Est ce une piste, ou est ce que cela sort du champ d'un papier sur les agents de langage ?
4. **Le lien avec a1.** La correlation de 0,684 entre fidelite de l'agent et stabilite propre
   de la personne a ete mesuree a deux semaines. A deux ans, la stabilite d'une personne mesure
   surtout la stabilite de sa vie et non de ses reponses. Est ce que cela change
   l'interpretation psychologique de la section 6 de a1 ?
5. **Est ce que A8 est un papier, ou une section d'un papier ?** Trois tableaux et une prise de
   position sur la comparabilite, ce n'est pas gros. Cela pourrait etre une note methodologique
   courte, ou la section 2 d'un papier sur la mesure dont la section 1 serait la double
   distorsion. Ton avis oriente le reste du calendrier.

---

## Reproduction

```
.venv/bin/python -m pip install pyreadstat
.venv/bin/python analyses/a12_telecharger_panel.py     # 19 Mo, ecrit data/gss-panel/PROVENANCE.md
.venv/bin/python analyses/a12_retest_delai.py          # environ 20 secondes
.venv/bin/python analyses/a12_sensibilite_dk.py        # environ 30 secondes
```

Tableaux produits : `a12-appariement-items.csv`, `a12-retest-item.csv`,
`a12-retest-individu.csv`, `a12-synthese-delais.csv`, `a12-normalisation.csv`,
`a12-normalisation-noyau.csv`, `a12-noyau-commun.csv`, `a12-denominateurs-ic.csv`,
`a12-items-stables-instables.csv`, `a12-familles.csv`, `a12-extrapolation.csv`,
`a12-sensibilite-dk.csv`.

Aucun fichier existant n'a ete modifie. `analyses/a2_commun.py` est importe et utilise tel
quel pour `est_manquant`, `exactitude_par_personne` et `bootstrap_personnes` ;
`analyses/a2_baselines_gss.py` est importe pour la liste `FAMILLES` et pour rien d'autre.
