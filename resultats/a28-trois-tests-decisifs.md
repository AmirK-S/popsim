# a28. Les trois tests decisifs, avant la seance

> **Erratum du 9 septembre 2026, sur un point qui n'est pas couvert par l'errata E1 ci dessous.** « Seule l'ablation C2 contre C3 est defendable » et « son ablation la plus propre, C3 contre C2 » nomment mal ce couple : C2 recoit onze attributs demographiques, C3 les 119 reponses de la personne sans demographie (`a45` section 0, `a47` D1).
> C'est un contraste de conditionnement a deux facteurs confondus. L'ablation propre, a un seul facteur, est le run R3 : `resultats/r3-resultats.md`.

## Errata du 9 septembre 2026

Correction apportee a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md` section 12.1, contradiction D8, signalee par
`resultats/a47-errata-2.md` section 4. **Le corps du rapport n'est pas reecrit** ; l'errata
cite la phrase d'origine, donne la correction et donne la preuve. Aucun recalcul, aucun
appel de modele de langage : les chiffres cites sont ceux de `a38` tels que publies.

### E1. Test 1, rang 1 : la these « la simulation devie la ou les humains se surveillent » est tombee. Objection a45 numero 12.1, contradiction D8.

**Phrase d'origine.** « **Test 1, rang 1.** *La simulation devie la ou les humains se
surveillent.* **Le motif tient au niveau du groupe de methodes et tombe au niveau de chaque
methode prise seule :** les huit conditions a modele de langage ont un contraste moyen de
plus 0,0503 de distance sur les items sensibles, les cinq predicteurs statistiques de moins
0,0001, difference plus 0,0504 avec un `p` de permutation sur les etiquettes de methode de
0,0008. »

**Correction, trois lignes.**

1. **Le motif de groupe ne survit pas a la version continue.**
   `resultats/a38-mode-continu-et-camp.md` section 2 remplace le decoupage binaire de NORC
   par l'ampleur mesuree item par item sur six sources : **aucun `p` brut ne descend sous
   0,18**, les intervalles bootstrap contiennent tous zero, et sur la dispersion le meilleur
   `p` vaut 0,119, **de signe oppose a la prediction** [MESURE, `a38-continu.csv`]. Le
   contraste de groupe de ce rapport ne doit plus etre cite comme un motif etabli.
2. **Ce qui reste du contraste est une affaire d'attitudes, pas de surveillance.** a38
   section 3.2 : le contraste vaut plus 0,062 a plus 0,093 sur les items d'attitude et se
   tient entre moins 0,031 et plus 0,045 sur les comportements verifiables, la ou la
   litterature sur la desirabilite sociale attendait l'effet le plus fort
   [MESURE, `a38-comportement.csv`].
3. **La reserve deja portee par ce rapport devient la conclusion :** aucune condition prise
   individuellement ne passe la famille de 52 tests, meilleur `p` de Holm **0,144**
   [MESURE, `a28-t1-corrections.csv`] ; et le seul effet distinguable trouve par `a25`, C2 a
   moins 0,207 [moins 0,331 ; moins 0,092], est **une condition sur treize dans une famille
   non corrigee**.

**Ce que le rapport garde.** Le protocole ecrit avant les resultats, la foret aleatoire
`B3 foret` et ses 0,6340 d'exactitude, les tests 2 et 3 et l'ensemble des tableaux
`a28-t1-*`, `a28-t2-*` et `a28-t3-*` restent valides. C'est la lecture du test 1 en tete de
rapport qui est retiree.

---

Rapport du 8 septembre 2026. Il execute les tests decisifs des idees de rang 1, 2 et 3 de
`CORPUS-SYNTHESE.md` section 4, pour que la seance de reflexion se tienne sur des chiffres
et non sur des impressions. Chaque test durcit une revendication existante ; deux des
trois la font tomber en partie.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre scripts nouveaux,
`analyses/a28_commun.py`, `a28_test1_mode.py`, `a28_test2_ecrasement.py`,
`a28_test3_stereotype.py`, plus `a28_figures.py`. Aucun script existant n'a ete modifie ;
`a2_commun`, `a2_baselines_gss`, `a5_evaluer`, `a5_agents_locaux_gss`, `a8_commun`,
`a25_commun` et `a25_mesures` sont importes tels quels, memes graines, memes plis, memes
149 items et memes personnes que a2, a23 et a25.

Une methode est nouvelle et une seule : la foret aleatoire sur demographies, notee
`B3 foret`, scikit-learn, 300 arbres, feuilles d'au moins 5 observations, memes cinq plis
et meme encodage indicatrice que `B1 argmax`. C'est l'adversaire nomme par Ku 2026,
replante chez nous. Elle obtient 0,6340 d'exactitude sur le GSS, entre `B1 argmax` a
0,6209 et `B2 argmax` a 0,6717 [MESURE]. `B1 argmax` retombe a 0,6209 exactement comme en
a2 : le protocole n'a pas bouge.

Sorties : `a28-t1-*.csv` (7 tableaux), `a28-t2-*.csv` (4 tableaux), `a28-t3-*.csv`
(3 tableaux), `a28-figure-test1`, `a28-figure-test2`, `a28-figure-test3`, en `.png` et
`.svg`.

---

## Les trois reponses en une ligne

**Test 1, rang 1.** *La simulation devie la ou les humains se surveillent.* **Le motif tient
au niveau du groupe de methodes et tombe au niveau de chaque methode prise seule :** les
huit conditions a modele de langage ont un contraste moyen de plus 0,0503 de distance sur
les items sensibles, les cinq predicteurs statistiques de moins 0,0001, difference
plus 0,0504 avec un p de permutation sur les etiquettes de methode de 0,0008 ; mais une
fois corrigee sur la famille de 52 tests declaree avant les resultats, **aucune condition
prise individuellement ne passe**, le meilleur p ajuste par Holm valant 0,144 et par
Benjamini Hochberg 0,055 [MESURE, `a28-t1-corrections.csv`].

**Test 2, rang 2.** *La statistique ecrase uniformement, le modele de langage ecrase
selectivement.* **La prediction ne tient pas, et le signe est inverse :** ce sont les
predicteurs statistiques qui montrent l'ecrasement le plus selectif, `B2 argmax` a 0,285 de
correlation et la foret aleatoire a 0,186, quand les huit conditions a modele de langage
s'etalent de 0,003 a 0,185 et qu'aucune ne passe la correction de Holm
[MESURE, `a28-t2-selectivite.csv`]. Le controle a demi echantillon, qui elimine l'artefact
de denominateur partage, ne laisse debout que `B2 argmax` a 0,333 et la foret a 0,247, et
met les huit conditions a modele de langage dans le bruit. L'objection de Ku 2026 sort
renforcee de ce test, pas affaiblie.

**Test 3, rang 3.** *Le modele efface par le stereotype et non par la moyenne.* **La
prediction tient dans son ordre et se vide de sa portee par son plancher :** les huit
conditions a modele de langage se trompent vers le stereotype de segment dans 0,371 a
0,715 des cas contre 0,100 pour `B0 mode`, et C3 sans etiquette se place bien sous C2 avec
etiquette, moins 0,129 [moins 0,160 ; moins 0,099] ; mais les memes humains reinterroges
sont a 0,537, et `B1 argmax` a 0,552 sur le meme perimetre et 0,653 sur les 1 052 : **se
tromper vers le stereotype de son segment n'est pas propre au langage, c'est propre au fait
de disposer de l'etiquette** [MESURE, `a28-t3-profil-erreur.csv`]. Le resultat qui reste
est ailleurs, sur le rappel des cellules minoritaires, ou l'ordre s'inverse et ou la foret
aleatoire est derniere de treize.

---

## 0. Le protocole, ecrit avant les resultats

C'est la dette ouverte depuis a17 et rappelee par a25 : tant que la famille d'hypotheses
n'est pas fixee, aucun p du projet n'est defendable. Elle est fixee ici, en clair, dans
l'entete de chaque script, et recopiee ci dessous sans retouche. Elle a ete ecrite avant
l'execution ; le journal de session le montre, et la seule verification possible pour un
tiers est la lecture des docstrings, qui n'ont pas ete modifies apres coup.

### 0.1 La famille du test 1, 52 tests

| | enonce | nombre de tests |
|---|---|---|
| **H1** primaire, distance | pour chacune des 13 methodes non humaines, la distance a la population humaine est plus grande sur les 12 items sensibles de NORC que sur ses 65 temoins, perimetre 150 | 13 |
| **H2** primaire, dispersion | pour chacune des 13 methodes, le rapport d'entropie agent sur humain est plus bas sur les items sensibles | 13 |
| **H3** secondaire, continu | pour chacune des 13 methodes, la correlation de rang entre le score de sensibilite par item et la distance par item est positive, score NORC ordinal | 13 |
| **H4** secondaire, sens | pour chacune des 13 methodes, le deplacement vers le pole desirable est plus grand sur les items sensibles | 13 |

**Correction principale : Holm sur les 52.** Elle controle le taux d'erreur par famille
sans hypothese sur la dependance, ce qui est necessaire : les 13 contrastes portent sur
les memes items et les memes gens, ils sont fortement correles. **Correction secondaire
rapportee a cote : Benjamini Hochberg sur les 52**, qui controle le taux de fausses
decouvertes mais suppose une dependance positive au sens PRDS, hypothese plausible et non
verifiee ici. Les corrections par sous famille de 13 sont aussi donnees, pour le lecteur
qui juge que seule H1 meritait d'etre pre enregistree.

**N'entrent pas dans la famille**, et sont rapportes comme des descriptions : la ligne
`humains vague 2`, qui est un temoin negatif et non une hypothese ; les analyses de
robustesse et de stratification, conditionnelles a H1 ; les scores de sensibilite S2 et S3 ;
le perimetre 1 052, qui est un echantillon emboite et non un test independant ; et le
contraste de groupe de la section 1.5, ajoute apres coup et signale comme tel.

### 0.2 Les familles des tests 2 et 3

| | enonce | nombre |
|---|---|---|
| **H5** | pour chacune des 13 methodes non humaines, la correlation de rang entre le rapport de dispersion intra par item et la part de variance humaine expliquee par la segmentation est positive, profil croise, perimetre 150 | 13 |
| **H6** | l'ecart type du rapport intra entre items est plus grand chez les 8 conditions a modele de langage que chez les 5 predicteurs statistiques | 1 |
| **H7** | pour chacune des 8 conditions a modele de langage, la part stereotype est plus haute que celle de `B0 mode`, axe ideologie, perimetre 150 | 8 |
| **H8** | la part stereotype de C3, sans etiquette, est plus basse que celle de C2, avec etiquette | 1 |

Holm et Benjamini Hochberg sont appliques sur H5 union H6 d'un cote, 14 tests, et sur
H7 union H8 de l'autre, 9 tests.

### 0.3 Ce qui est partage avec a2, a23 et a25

Memes 1 052 participants et memes 149 items ; meme liste d'exclusion de Stanford ; memes
cinq plis sur les personnes et memes cinq blocs d'items, graine 20260903 ; memes 150
personnes du run local pour C2 et C3 ; memes traces completes du 8 septembre. Graine
d'analyse 20260908 partout. Les baselines sont recalculees a partir de `a2_baselines_gss`
sans modification : `B1 argmax` retombe a 0,6209, comme en a2.

---

## 1. Test 1. La simulation devie t elle la ou les humains se surveillent ?

Figure : `a28-figure-test1.png` et `.svg`.

### 1.1 Ce que la correction pour tests multiples fait au resultat de a25

[MESURE, `a28-t1-contrastes.csv` et `a28-t1-corrections.csv`, perimetre 150]

| condition | sensibles | temoins | difference | IC 95 % items | p brut | Holm 13 | BH 13 | Holm 52 | BH 52 |
|---|---|---|---|---|---|---|---|---|---|
| agents entretien (v3) | 0,1653 | 0,0911 | **+0,0743** | [+0,011 ; +0,149] | **0,0028** | **0,037** | **0,037** | 0,144 | 0,055 |
| agents v8 | 0,1764 | 0,1175 | +0,0589 | [-0,010 ; +0,135] | 0,0517 | 0,517 | 0,168 | 1,000 | 0,315 |
| agents composite | 0,1299 | 0,0746 | **+0,0553** | [+0,003 ; +0,119] | **0,0112** | 0,135 | 0,072 | 0,528 | 0,097 |
| agents enquete | 0,1448 | 0,0948 | **+0,0500** | [+0,002 ; +0,111] | **0,0167** | 0,183 | 0,072 | 0,766 | 0,124 |
| agents demographiques (v6) | 0,1963 | 0,1513 | +0,0450 | [-0,023 ; +0,119] | 0,1700 | 1,000 | 0,413 | 1,000 | 0,450 |
| C3 | 0,2548 | 0,2103 | +0,0445 | [-0,048 ; +0,148] | 0,3993 | 1,000 | 0,686 | 1,000 | 0,794 |
| agents v7 | 0,2037 | 0,1653 | +0,0384 | [-0,026 ; +0,109] | 0,1908 | 1,000 | 0,413 | 1,000 | 0,473 |
| C2 | 0,2462 | 0,2101 | +0,0361 | [-0,051 ; +0,133] | 0,4583 | 1,000 | 0,686 | 1,000 | 0,810 |
| B2 argmax | 0,1494 | 0,1357 | +0,0137 | [-0,036 ; +0,074] | 0,5805 | 1,000 | 0,686 | 1,000 | 0,839 |
| B1 argmax | 0,1147 | 0,1043 | +0,0104 | [-0,028 ; +0,058] | 0,5361 | 1,000 | 0,686 | 1,000 | 0,820 |
| **B3 foret** | 0,1616 | 0,1588 | +0,0027 | [-0,050 ; +0,062] | 0,9139 | 1,000 | 0,914 | 1,000 | 0,954 |
| B0 tirage | 0,0384 | 0,0455 | -0,0071 | [-0,022 ; +0,009] | 0,4797 | 1,000 | 0,686 | 1,000 | 0,810 |
| B0 mode | 0,2641 | 0,2840 | -0,0200 | [-0,087 ; +0,045] | 0,6394 | 1,000 | 0,693 | 1,000 | 0,853 |
| *humains vague 2* | 0,0221 | 0,0267 | -0,0046 | [-0,014 ; +0,006] | 0,4184 | hors famille | | | |

**Le chiffre desagreable, et il est central.** Sur la famille complete de 52 tests declarees
avant les resultats, **aucune condition ne passe le seuil de 5 pour cent**, ni par Holm,
0,144 au mieux, ni par Benjamini Hochberg, 0,055 au mieux, et ce meilleur p appartient a
H2 et non a H1. Meme reduit a la seule sous famille de 13 tests de H1, une seule condition
passe, `agents entretien (v3)` a 0,037, et elle passe de justesse. a25 ecrivait, dans son
paragraphe interdit numero 4, que « le resultat de la section 3 est a la limite de ce que
la correction laisserait passer ». **La correction est faite : il est au dessous.**

**La nouveaute favorable a la these** est que le seul predicteur statistique manquant,
la foret aleatoire de Ku 2026, se range exactement la ou les autres : plus 0,0027,
p = 0,914, l'avant derniere valeur du tableau. Les cinq predicteurs statistiques
s'etendent de moins 0,020 a plus 0,014 ; les huit conditions a modele de langage, de
plus 0,036 a plus 0,074, sans exception et sans chevauchement des deux plages.

### 1.2 (e) Le contraste sur la dispersion, mesure nouvelle

Rapport d'entropie de la population simulee sur la population humaine, item par item,
entropie corrigee par Miller Madow, puis contraste sensibles moins temoins. Un rapport de 1
signifie autant de variete que chez les humains. La question posee est : **la simulation
efface t elle plus de variete sur les items sensibles ?** [MESURE, `a28-t1-contrastes.csv`]

| condition | sensibles | temoins | difference | IC 95 % items | p brut | Holm 13 | BH 13 |
|---|---|---|---|---|---|---|---|
| agents entretien (v3) | 0,606 | 0,885 | **-0,2787** | [-0,500 ; -0,068] | **0,0010** | **0,014** | **0,014** |
| agents v8 | 0,547 | 0,820 | **-0,2727** | [-0,506 ; -0,048] | **0,0109** | 0,120 | **0,047** |
| agents enquete | 0,655 | 0,887 | **-0,2321** | [-0,402 ; -0,091] | **0,0041** | **0,049** | **0,027** |
| agents demographiques (v6) | 0,448 | 0,594 | -0,1469 | [-0,343 ; +0,048] | 0,1546 | 1,000 | 0,335 |
| agents v7 | 0,468 | 0,608 | -0,1395 | [-0,302 ; +0,015] | 0,0899 | 0,809 | 0,234 |
| B1 argmax | 0,672 | 0,689 | -0,0170 | [-0,193 ; +0,141] | 0,8314 | 1,000 | 0,929 |
| B2 argmax | 0,557 | 0,565 | -0,0079 | [-0,189 ; +0,165] | 0,9293 | 1,000 | 0,929 |
| B0 tirage | 0,967 | 0,982 | -0,0151 | [-0,062 ; +0,035] | 0,6378 | 1,000 | 0,829 |
| agents composite | 0,928 | 0,918 | +0,0100 | [-0,208 ; +0,284] | 0,8824 | 1,000 | 0,929 |
| **B3 foret** | 0,505 | 0,456 | +0,0495 | [-0,148 ; +0,242] | 0,6211 | 1,000 | 0,829 |
| B0 mode | 0,085 | 0,018 | +0,0665 | [-0,030 ; +0,192] | 0,0790 | 0,790 | 0,234 |
| **C3** | 0,837 | 0,693 | **+0,1437** | [-0,146 ; +0,556] | 0,3044 | 1,000 | 0,495 |
| **C2** | 0,819 | 0,653 | **+0,1655** | [-0,184 ; +0,637] | 0,2323 | 1,000 | 0,431 |
| *humains vague 2* | 0,981 | 1,004 | -0,0228 | [-0,052 ; +0,006] | 0,2851 | hors famille | |

**Deux enseignements, l'un pour la these et l'autre contre.**

**Pour.** Les trois conditions riches de Stanford effacent nettement plus de variete sur les
items sensibles, de 23 a 28 points de rapport d'entropie, et les trois p bruts sont sous
0,05 ; deux passent encore la correction de Holm dans la sous famille et trois passent
Benjamini Hochberg. C'est le resultat le plus net du test 1, et c'est une mesure nouvelle :
a25 ne regardait que la distance. **Aucun des cinq predicteurs statistiques ne montre rien**,
de moins 0,017 a plus 0,066.

**Contre.** **C2 et C3 vont dans l'autre sens**, plus 0,166 et plus 0,144 : nos agents
locaux conservent PLUS de variete sur les items sensibles que sur les temoins. Et
`agents composite`, la condition la plus riche du paquet de Stanford, est a plus 0,010,
c'est a dire a rien. **Le motif « les huit conditions vont dans le meme sens », qui etait
l'argument de vente de a25 sur la distance, ne se reproduit pas sur la dispersion : cinq
conditions sur huit vont dans un sens et trois dans l'autre.**

### 1.3 (c) Robustesse : le retrait des quatre items nominaux

a25 avait identifie quatre items nominaux charges comme porteurs de l'effet : `spkrac/y`,
`polabuse/y`, `polattak/y` et `vote16`. Ils sont retires un a un puis tous les quatre.
[MESURE, `a28-t1-robustesse.csv`, metrique de distance, perimetre 150]

| condition | aucun retrait | sans `spkrac/y` | sans `polabuse/y` | sans `polattak/y` | sans `vote16` | **sans les quatre** |
|---|---|---|---|---|---|---|
| agents composite | +0,0553 | +0,0665 | +0,0544 | +0,0296 | +0,0623 | **+0,0436** |
| agents entretien (v3) | +0,0743 | +0,0517 | +0,0838 | +0,0535 | +0,0810 | **+0,0372** |
| agents enquete | +0,0500 | +0,0413 | +0,0601 | +0,0268 | +0,0528 | **+0,0240** |
| agents demographiques (v6) | +0,0450 | +0,0235 | +0,0586 | +0,0265 | +0,0569 | **+0,0249** |
| agents v7 | +0,0384 | +0,0182 | +0,0521 | +0,0206 | +0,0412 | **+0,0086** |
| agents v8 | +0,0589 | +0,0350 | +0,0695 | +0,0392 | +0,0531 | **+0,0055** |
| **C2** | +0,0361 | +0,0185 | +0,0209 | +0,0361 | +0,0052 | **-0,0516** |
| **C3** | +0,0445 | +0,0532 | +0,0428 | +0,0283 | +0,0077 | **-0,0189** |
| B1 argmax | +0,0104 | +0,0154 | +0,0154 | -0,0071 | +0,0123 | +0,0027 |
| B2 argmax | +0,0137 | +0,0164 | +0,0218 | -0,0036 | -0,0036 | -0,0191 |
| B3 foret | +0,0027 | -0,0008 | +0,0120 | -0,0165 | +0,0011 | -0,0182 |
| B0 mode | -0,0200 | -0,0359 | -0,0014 | -0,0323 | -0,0293 | -0,0462 |
| *humains vague 2* | -0,0046 | -0,0032 | -0,0032 | -0,0087 | -0,0032 | -0,0044 |

**Aucun retrait unique ne detruit l'effet pour les six conditions de Stanford**, et c'est ce
que a25 disait deja. **Le retrait des quatre ensemble change le signe pour C2 et C3**, a
moins 0,052 et moins 0,019, et il ramene `agents v8` a plus 0,006 et `agents v7` a
plus 0,009, c'est a dire a rien. Les trois conditions riches de Stanford survivent, a
0,024 a 0,044, mais avec 8 items sensibles au lieu de 12 : le test n'a plus la puissance de
conclure, comme le montre la section suivante.

**Enseignement direct** : **le contraste de nos deux conditions locales n'existe pas en
dehors de ces quatre items.** Toute phrase du papier qui dit « nos agents aussi » doit
nommer les quatre items ou disparaitre.

### 1.4 (d) Stratification par type d'item

Trois strates : items a deux modalites, ou la distance de Wasserstein et la distance de
variation totale coincident ; items nominaux a trois modalites et plus ; items ordinaux a
trois modalites et plus. Les 12 items sensibles se repartissent en **3 binaires**
(`spkrac/y`, `polabuse/y`, `polattak/y`), **1 nominal** (`vote16`) et **8 ordinaux**.
[MESURE, `a28-t1-strates.csv`, perimetre 150]

| condition | binaire (3 items sensibles) | nominal 3 et plus (1 item) | ordinal 3 et plus (8 items) |
|---|---|---|---|
| agents composite | +0,1299 | -0,0550 | +0,0365 |
| agents entretien (v3) | +0,2069 | -0,0212 | +0,0343 |
| agents enquete | +0,1546 | -0,0461 | +0,0171 |
| agents demographiques (v6) | +0,1537 | -0,1600 | +0,0296 |
| agents v7 | +0,1267 | -0,0405 | +0,0181 |
| agents v8 | +0,2187 | -0,0400 | +0,0059 |
| C2 | +0,1323 | +0,2022 | -0,0030 |
| C3 | +0,0390 | +0,3856 | +0,0215 |
| B1 argmax | +0,0278 | -0,0656 | +0,0198 |
| B2 argmax | +0,0248 | +0,1122 | +0,0065 |
| B3 foret | +0,0431 | -0,0867 | +0,0076 |
| B0 mode | +0,0331 | -0,2544 | +0,0007 |
| *humains vague 2* | +0,0011 | -0,0367 | -0,0023 |

**Le contraste de distance est un phenomene d'items binaires.** Sur la strate binaire il
vaut 0,127 a 0,219 pour les six conditions de Stanford et moins 0,002 a plus 0,043 pour les
predicteurs statistiques. Sur la strate ordinale il tombe a 0,006 a 0,037 pour les conditions de
Stanford, contre moins 0,003 a plus 0,020 pour les predicteurs statistiques : les deux
plages se recouvrent, le motif disparait. La colonne nominale ne porte qu'un item, `vote16`, et
n'autorise aucun intervalle.

**Le contraste de dispersion se comporte mieux.** Sur la meme stratification
[MESURE, `a28-t1-strates.csv`, metrique de rapport d'entropie] : sur les 8 items ordinaux,
`agents entretien (v3)` vaut moins 0,150, `agents enquete` moins 0,142, `composite`
moins 0,109, `v8` moins 0,081, quand `B1 argmax` vaut moins 0,012, `B2 argmax` plus 0,048,
`B3 foret` plus 0,069, `B0 mode` plus 0,114 et les humains plus 0,002. **La mesure de dispersion, elle, garde une
separation sur les items ordinaux.** C'est le point le plus solide du test 1.

### 1.5 (b) La version continue

a25 declarait ce point non testable faute d'ampleurs par item chez NORC. Il l'est, a
condition de construire le score et d'en assumer la construction. Trois scores, declares en
clair dans `a28_test1_mode.py` et exportes item par item dans `a28-t1-scores-items.csv`.

**S1, classes ordonnees de NORC** : temoin 0, a investiguer 1, sensible 2. Couverture
**90 items sur 149**. C'est la seule version pre enregistree, celle de H3.

**S2, ampleur publiee**, en points de pourcentage d'ecart entre ce qui est declare et ce
qui est cache ou observe, une valeur par domaine, chacune tiree d'une mesure de
`corpus/04`. Couverture **60 items sur 149**, dont seulement **5 des 12 items sensibles**.
Regle stricte : quand la litterature n'a pas mesure le domaine, la valeur est absente et
non zero ; zero est reserve aux domaines ou elle a cherche et n'a rien trouve, ce qui est
un resultat. Les valeurs qui portent le score :

| domaine | points | niveau | source |
|---|---|---|---|
| vote declare (`vote16`) | 15,8 | [CONFIRME] | Ansolabehere et Hersh 2012, corpus 04-20 : 84,3 declare contre 68,5 valide |
| attitude raciale (`spkrac/y`, `natrace/y`, `racdif*`, `colrac`, `librac/y`...) | 13,5 | [CONFIRME] | Berinsky 1999, corpus 04-19 |
| discrimination percue (`discaff*`) | 13,0 | [HYPOTHESE] | Pew 2015, corpus 04-15, transfert vers la discrimination inverse |
| immigration (`letin1a`) | 10,0 | [CONFIRME] | Bursztyn, Egorov et Fiorin 2020, corpus 04-27 |
| religion (`attend`, `pray`, `reborn`, `savesoul`, `bible`, `postlife`) | 10,0 | [PROBABLE] | Presser et Stinson 1998, corpus 04-13 |
| hostilite envers les gays (`homosex`, `spkhomo/y`, `colhomo`, `libhomo/y`) | 10,0 | [PROBABLE] | Coffman, Coffman et Ericson 2017, corpus 04-21, conversion en points faite par nous |
| revenu et statut (`income`, `incom16`, `finrela`, `class`) | 8,0 | [PROBABLE] | Tourangeau et Yan 2007 corpus 04-03 ; Kreuter, Presser et Tourangeau 2008 corpus 04-11 |
| conduite sexuelle (`xmarsex`, `xmovie`, `pillok`, `sexeduc`, `pornlaw`) | 6,0 | [PROBABLE] | Gnambs et Kaspar 2015, corpus 04-14, Omega = 1,29 |
| satisfaction et bien etre (`happy`, `satfin`, `satjob`, `health`, `life`...) | 5,5 | [PROBABLE] | Pew 2015, corpus 04-15, ecart moyen sur 60 questions |
| chomage passe (`unemp`), punition corporelle (`spanking`) | 5,0 | [HYPOTHESE] | transposition, aucune ampleur publiee |
| tolerance politique (`spkath/y`, `colath`, `spkcom/y`...), roles de genre (`fefam`...) | 4,0 | [HYPOTHESE] | Tourangeau et Yan 2007, aucune ampleur par item |
| drogues, opinion (`grass`) | 2,0 | [HYPOTHESE] | Gnambs et Kaspar mesurent le comportement, pas l'opinion |
| mariage entre personnes de meme sexe (`marhomo`) | **0,0** | [CONFIRME] | Lax, Phillips et Stollwerk 2016, corpus 04-22 : aucune preuve. Zero mesure |
| choix de candidat (`pres16`, `if16who`) | **0,0** | [CONFIRME] | Coppock 2017 corpus 04-30, AAPOR 2021 corpus 04-31 : aucun electeur cache. Zero mesure |

**S3, composite** : moyenne des rangs normalises de S1 et de S2, sur les 40 items ou les
deux existent.

Correlations de rang avec la distance par item [MESURE, `a28-t1-continu.csv`, perimetre 150] :

| condition | S1 NORC (90 items) | p | S2 ampleur (60 items) | S3 composite (40 items) |
|---|---|---|---|---|
| agents enquete | +0,186 | 0,080 | +0,241 | +0,300 |
| agents composite | +0,159 | 0,138 | +0,192 | +0,174 |
| agents entretien (v3) | +0,152 | 0,152 | +0,137 | +0,173 |
| agents v7 | +0,144 | 0,173 | +0,221 | **+0,370** |
| C3 | +0,117 | 0,277 | **+0,306** | **+0,460** |
| agents v8 | +0,097 | 0,358 | +0,158 | +0,050 |
| agents demographiques (v6) | +0,071 | 0,500 | **+0,281** | +0,277 |
| C2 | +0,013 | 0,909 | +0,165 | +0,080 |
| B0 mode | +0,061 | 0,559 | -0,055 | +0,101 |
| B2 argmax | +0,006 | 0,954 | **-0,292** | -0,142 |
| B3 foret | -0,016 | 0,878 | **-0,225** | +0,057 |
| B1 argmax | -0,070 | 0,515 | -0,197 | -0,099 |
| B0 tirage | -0,202 | 0,055 | +0,056 | +0,097 |
| *humains vague 2* | -0,199 | 0,059 | -0,129 | -0,232 |

**La version continue ne sauve pas le resultat au niveau de chaque condition** : sur S1, le
score pre enregistre, aucune correlation ne se distingue de zero, la plus forte valant
0,186 avec p = 0,080 avant toute correction. **Elle produit en revanche le motif le plus net
du rapport au niveau du groupe** : sur S2, les huit conditions a modele de langage sont
toutes positives, de +0,137 a +0,306, et les trois predicteurs qui recoivent de
l'information sur la personne sont tous negatifs, `B1` a -0,197, `B2` a -0,292, `B3 foret`
a -0,225.

### 1.6 Le contraste de groupe, post hoc, et pourquoi il est le vrai resultat

Ce contraste **n'est pas dans la famille declaree**. Il est ajoute apres coup, parce que la
revendication de a25 ne portait pas sur une condition mais sur un motif : huit conditions a
modele de langage d'un cote, predicteurs statistiques de l'autre. Tester le motif demande
une permutation des etiquettes de **methode** et non d'item. 20 000 tirages.
[MESURE, `a28-t1-contraste-de-groupe.csv`, perimetre 150]

| quantite | moyenne des 8 conditions a modele de langage | moyenne des 5 predicteurs statistiques | difference | p |
|---|---|---|---|---|
| **H1, distance** | +0,0503 | -0,0001 | **+0,0504** | **0,0008** |
| **H3 continu, S2 ampleur publiee** | +0,2127 | -0,1428 | **+0,3555** | **0,0009** |
| **H3 continu, S1 NORC ordinal** | +0,1176 | -0,0443 | **+0,1618** | **0,0016** |
| **H3 continu, S3 composite** | +0,2355 | +0,0028 | **+0,2327** | **0,0147** |
| H4, sens de l'ecart | -0,0648 | -0,0028 | -0,0621 | 0,0698 |
| H2, dispersion | -0,0938 | +0,0152 | -0,1090 | 0,2070 |

**Voila ce qui reste du rang 1, une fois tout corrige.** Ce n'est pas « telle condition
s'ecarte davantage sur les items sensibles » : cette phrase ne survit a aucune correction.
C'est **« les methodes qui emploient un modele de langage se comportent en bloc autrement
que les methodes qui n'en emploient pas, sur les items que NORC a mesures sensibles au mode,
et le signe est celui que la these predit »**, avec un p de 0,0008 sur la distance et de
0,0009 sur la version continue.

**La limite de ce test, ecrite en clair.** Il traite les 13 methodes comme 13 unites
echangeables, ce qu'elles ne sont pas : elles partagent les memes items et les memes gens,
et l'etiquette « modele de langage » n'est pas tiree au sort. Le p est donc a lire comme
la probabilite qu'un decoupage au hasard de 13 methodes en 8 et 5 produise un ecart aussi
grand, et rien de plus. Il ne remplace pas une replication.

### 1.7 Les controles qui restent negatifs

- **La classe adjacente ne montre toujours rien.** Sur les 13 items que NORC classe « a
  investiguer » contre les memes 65 temoins, aucune condition ne se distingue : agents v7
  +0,034 (p = 0,200), agents enquete +0,014 (p = 0,443), C3 +0,012 (p = 0,813), composite
  -0,007, C2 -0,061 [MESURE]. C'est le meme constat genant qu'en a25 et il n'est pas leve.
- **Le perimetre 1 052 reproduit le motif sans le renforcer** : agents entretien +0,0695
  (p = 0,0042), composite +0,0588 (p = 0,0113), enquete +0,0392 (p = 0,0423),
  `B1 argmax` -0,0007 (p = 0,963), `B2 argmax` +0,0034 (p = 0,873), **`B3 foret` +0,0039
  (p = 0,871)**, humains vague 2 +0,0004 (p = 0,919) [MESURE]. Sur la dispersion, meme
  perimetre : entretien -0,3046 (p = 0,0006), enquete -0,2066 (p = 0,0071), v8 -0,2771
  (p = 0,0100).
- **Le sens de l'ecart tombe toujours.** Une seule condition se distingue de zero, C2 a
  -0,207 [-0,328 ; -0,092], p brut 0,0043, et elle va **contre** le pole desirable. Apres
  correction sur la famille de 52, son p ajuste vaut 0,209 par Holm et 0,055 par
  Benjamini Hochberg [MESURE]. La conclusion de a25 est inchangee et elle est maintenant
  corrigee : **la prediction dirigee est morte.**

---

## 2. Test 2. L'ecrasement est il uniforme ou selectif ?

Figure : `a28-figure-test2.png` et `.svg`.

C'est la reponse mesuree a Ku 2026. Leur objection : une foret aleatoire supervisee ecrase
la dispersion autant qu'un modele de langage, rapport de 0,72 contre 0,67 a 0,85, donc
l'ecrasement est une propriete de la tache et non du langage [CONFIRME, corpus/01]. Ce test
ne conteste pas l'amplitude, il conteste la **forme**. Prediction de la these : la
statistique ecrase uniformement, le modele de langage ecrase selectivement, la ou
l'etiquette n'explique rien.

### 2.1 Le niveau, d'abord : Ku a raison sur l'amplitude

Rapport de dispersion intra groupe, indice de Gini Simpson, estimateur sans biais,
segmentation par le profil croise genre x race x bloc d'ideologie de a1, mediane sur les
146 items dont la dispersion intra humaine depasse 0,05.
[MESURE, `a28-t2-uniformite.csv`, perimetre 150]

| condition | rapport median | rapport moyen | ecart type | ecart interquartile | coefficient de variation | q10 | q90 |
|---|---|---|---|---|---|---|---|
| agents composite | 0,903 | 0,872 | 0,287 | 0,225 | 0,329 | 0,627 | 1,085 |
| agents enquete | 0,853 | 0,860 | 0,741 | 0,279 | 0,862 | 0,418 | 1,069 |
| agents entretien (v3) | 0,817 | 0,767 | 0,302 | 0,314 | 0,394 | 0,316 | 1,045 |
| C3 | 0,745 | 0,713 | 0,466 | 0,545 | 0,652 | 0,066 | 1,154 |
| agents demographiques (v6) | 0,660 | 0,598 | 0,357 | 0,553 | 0,597 | 0,025 | 1,001 |
| agents v7 | 0,585 | 0,605 | 0,308 | 0,455 | 0,509 | 0,180 | 0,970 |
| agents v8 | 0,491 | 0,504 | 0,253 | 0,293 | 0,502 | 0,211 | 0,794 |
| C2 | 0,408 | 0,470 | 0,666 | 0,388 | 1,416 | 0,000 | 0,808 |
| B0 tirage | 1,038 | 1,046 | 0,214 | 0,125 | 0,204 | 0,890 | 1,242 |
| B1 argmax | 0,604 | 0,557 | 0,245 | 0,331 | 0,439 | 0,190 | 0,844 |
| B2 argmax | 0,568 | 0,501 | 0,297 | 0,503 | 0,593 | 0,014 | 0,867 |
| **B3 foret** | **0,330** | 0,337 | 0,262 | 0,503 | 0,777 | 0,000 | 0,703 |
| B0 mode | 0,000 | 0,034 | 0,143 | 0,000 | 4,236 | 0,000 | 0,000 |
| *humains vague 2* | 1,001 | 1,010 | 0,108 | 0,109 | 0,107 | 0,898 | 1,100 |

**La foret aleatoire ecrase davantage que les huit conditions a modele de langage**,
0,330 de rapport median contre 0,408 a 0,903. Elle ecrase aussi davantage que `B1 argmax`
et `B2 argmax`, ce qui est attendu d'un modele plus flexible : mieux il ajuste l'etiquette,
moins il laisse de variete a l'interieur du segment. Le controle humain est a 1,001, comme
il doit.

### 2.2 La selectivite : la prediction de la these est fausse, et de signe inverse

Correlation de rang entre le rapport intra par item et la part de variance humaine
expliquee par la segmentation, D_inter sur D_total, 146 items, intervalle bootstrap sur les
items, p par permutation des items, correction sur la famille de 14 tests.
[MESURE, `a28-t2-selectivite.csv`, perimetre 150, profil croise]

| condition | rho de Spearman | IC 95 % items | p brut | Holm 14 | BH 14 |
|---|---|---|---|---|---|
| **B0 tirage** | **+0,560** | [+0,423 ; +0,675] | **0,0001** | **0,0013** | **0,0013** |
| **B2 argmax** | **+0,285** | [+0,114 ; +0,439] | **0,0006** | **0,0072** | **0,0039** |
| **B3 foret** | **+0,186** | [+0,034 ; +0,338] | **0,0240** | 0,264 | 0,078 |
| agents demographiques (v6) | +0,185 | [+0,020 ; +0,355] | 0,0269 | 0,269 | 0,078 |
| agents composite | +0,179 | [-0,004 ; +0,343] | 0,0300 | 0,270 | 0,078 |
| B0 mode | +0,164 | [+0,015 ; +0,281] | 0,0467 | 0,374 | 0,101 |
| agents entretien (v3) | +0,123 | [-0,036 ; +0,273] | 0,1415 | 0,990 | 0,257 |
| B1 argmax | +0,120 | [-0,046 ; +0,285] | 0,1582 | 0,990 | 0,257 |
| agents enquete | +0,092 | [-0,094 ; +0,262] | 0,2712 | 1,000 | 0,392 |
| agents v7 | +0,082 | [-0,084 ; +0,248] | 0,3245 | 1,000 | 0,417 |
| C3 | +0,079 | [-0,083 ; +0,231] | 0,3533 | 1,000 | 0,417 |
| C2 | +0,007 | [-0,170 ; +0,175] | 0,9331 | 1,000 | 0,973 |
| agents v8 | +0,003 | [-0,158 ; +0,169] | 0,9728 | 1,000 | 0,973 |
| *humains vague 2* | +0,130 | [-0,051 ; +0,310] | 0,1229 | hors famille | |

**Reponse a la question posee : non, la prediction de la these ne tient pas.** Les trois
seules methodes dont la correlation se distingue de zero apres correction sont **des
predicteurs statistiques**. Les huit conditions a modele de langage s'etalent de +0,003 a
+0,185 et **aucune ne passe**. Le motif attendu, du positif en rouge et du nul en bleu, est
exactement inverse dans son extremite haute.

**Sur le perimetre 1 052**, plus puissant pour les conditions de Stanford, le renversement
est plus net encore [MESURE] : `B0 tirage` +0,767, `B2 argmax` +0,140, `B3 foret` +0,018,
contre `agents entretien (v3)` **-0,173** [-0,334 ; -0,005], `agents composite` -0,090,
`B1 argmax` -0,113. **Les conditions riches de Stanford deviennent negatives** : elles
ecrasent legerement plus la ou l'etiquette explique le PLUS, ce qui est l'inverse strict de
la prediction.

### 2.3 Deux artefacts qu'il faut nommer avant de lire ce tableau

**Premier artefact, arithmetique et exact.** `B0 tirage` echantillonne dans la marginale de
la population, donc sa dispersion a l'interieur d'un segment vaut la dispersion TOTALE de
la population. Son rapport intra vaut donc mecaniquement D_total sur D_intra, c'est a dire
1 / (1 moins la part expliquee). **Sa correlation de 0,560 n'est pas un resultat, c'est une
identite.** Elle sert de borne haute de lecture : aucune methode ne peut etre plus
selective que cela sans que quelque chose cloche.

**Second artefact, statistique.** La part expliquee vaut 1 moins D_intra(humain) sur
D_total(humain), et le rapport intra vaut D_intra(methode) sur D_intra(humain). Les deux
quantites portent **le meme** D_intra(humain). Toute erreur d'echantillonnage sur ce terme
cree une correlation positive sans qu'aucune methode n'ait rien fait de selectif.
Le controle est ecrit dans `a28_test2_ecrasement.dispersions_demi_echantillon` : les
personnes sont coupees en deux moities, la part expliquee est estimee sur la moitie A et le
rapport intra sur la moitie B, de sorte que les deux ne partagent plus aucune cellule.
[MESURE, `a28-t2-demi-echantillon.csv`]

| condition | rho, perimetre 150 | IC 95 % | rho, perimetre 1 052 | IC 95 % |
|---|---|---|---|---|
| **B2 argmax** | **+0,333** | [+0,169 ; +0,480] | +0,135 | [-0,035 ; +0,309] |
| **B3 foret** | **+0,247** | [+0,096 ; +0,391] | +0,033 | [-0,135 ; +0,185] |
| agents demographiques (v6) | +0,145 | [-0,025 ; +0,309] | +0,124 | [-0,052 ; +0,281] |
| B0 tirage | +0,121 | [-0,060 ; +0,297] | **+0,574** | [+0,418 ; +0,695] |
| agents enquete | +0,115 | [-0,055 ; +0,280] | +0,084 | [-0,078 ; +0,235] |
| C3 | +0,080 | [-0,094 ; +0,240] | non applicable | |
| B1 argmax | +0,068 | [-0,096 ; +0,231] | -0,101 | [-0,260 ; +0,056] |
| C2 | +0,031 | [-0,134 ; +0,199] | non applicable | |
| agents entretien (v3) | +0,028 | [-0,145 ; +0,192] | -0,096 | [-0,261 ; +0,066] |
| agents composite | +0,024 | [-0,156 ; +0,197] | +0,027 | [-0,136 ; +0,179] |
| B0 mode | +0,039 | [-0,087 ; +0,167] | +0,114 | [-0,038 ; +0,254] |
| agents v8 | -0,043 | [-0,192 ; +0,111] | +0,004 | [-0,173 ; +0,172] |
| agents v7 | -0,056 | [-0,224 ; +0,139] | +0,039 | [-0,135 ; +0,208] |
| *humains vague 2* | -0,208 | [-0,371 ; -0,036] | +0,075 | [-0,092 ; +0,238] |

**Le controle confirme le renversement au lieu de le corriger.** Une fois les deux
estimations rendues independantes, les seules correlations dont l'intervalle exclut zero
sont celles de `B2 argmax`, +0,333, et de `B3 foret`, +0,247. **Les huit conditions a
modele de langage sont toutes dans le bruit.** Et la ligne humaine, a -0,208 sur les 150,
donne l'ampleur du bruit residuel : c'est du meme ordre que la plupart des valeurs
mesurees.

### 2.4 L'uniformite : le seul point qui reste favorable, et il ne resiste pas au controle

H6, ecart type du rapport intra entre items, 8 conditions a modele de langage contre 5
predicteurs statistiques, permutation des etiquettes de methode
[MESURE, `a28-t2-uniformite.csv`] :

- ecart type moyen : **0,4224** pour les modeles de langage contre **0,2320** pour les
  predicteurs statistiques, difference **+0,1903**, **p = 0,0378**. La prediction tient.
- **controle sans echelle**, coefficient de variation, parce que l'ecart type depend du
  niveau du rapport et que les methodes ne sont pas au meme niveau : 0,658 contre 1,250,
  difference **-0,592**, p = 0,451 ; le signe s'inverse, mais `B0 mode` seul explique le
  renversement, son coefficient valant 4,236 pour un rapport moyen de 0,034.
- **meme controle sans `B0 mode`** : 0,658 contre 0,503, difference **+0,154**, p = 0,485.

**Enseignement.** Une fois l'echelle controlee, la difference d'uniformite tombe a un ecart
de 0,15 sur un coefficient de variation, non distinguable de zero sur 8 methodes contre 4.
**H6 ne survit pas a son propre controle.**

### 2.5 Le controle par axe

La correlation de selectivite, calculee sur chacun des six axes de segmentation
[MESURE, `a28-t2-selectivite.csv`, perimetre 150] :

| condition | age | education | genre | ideologie | profil croise | race |
|---|---|---|---|---|---|---|
| agents composite | +0,174 | +0,146 | +0,002 | -0,048 | +0,179 | +0,054 |
| agents entretien (v3) | +0,190 | +0,170 | +0,089 | **-0,133** | +0,123 | +0,003 |
| agents enquete | +0,078 | -0,004 | +0,009 | +0,080 | +0,092 | -0,035 |
| agents demographiques (v6) | +0,156 | +0,200 | -0,125 | +0,112 | +0,185 | +0,051 |
| agents v7 | +0,214 | +0,191 | +0,108 | -0,054 | +0,082 | +0,013 |
| agents v8 | -0,112 | -0,112 | +0,070 | -0,017 | +0,003 | -0,148 |
| C2 | +0,045 | -0,046 | +0,167 | **-0,204** | +0,007 | +0,058 |
| C3 | +0,035 | +0,081 | -0,074 | +0,139 | +0,079 | +0,033 |
| B0 tirage | +0,451 | +0,338 | +0,169 | +0,408 | +0,560 | +0,253 |
| B1 argmax | +0,090 | +0,150 | +0,205 | -0,094 | +0,120 | +0,179 |
| B2 argmax | +0,028 | +0,102 | -0,019 | **+0,307** | +0,285 | +0,106 |
| B3 foret | +0,081 | +0,120 | +0,135 | +0,061 | +0,186 | +0,142 |
| *humains vague 2* | +0,305 | +0,206 | +0,082 | +0,099 | +0,130 | +0,089 |

**Sur l'axe ideologique, celui dont tout le dossier dit qu'il porte l'effet, les signes sont
melanges et C2 est a -0,204.** Aucun axe ne donne le motif predit.

---

## 3. Test 3. Moyenne ou stereotype ?

Figure : `a28-figure-test3.png` et `.svg`.

### 3.1 Le protocole, et ce qu'il exclut

Pour chaque cellule (personne, item), deux modalites de reference calculees sur les humains
de la vague 1 **en laissant de cote la personne elle meme** : `m_pop`, la modalite
majoritaire de la population, et `m_seg`, la modalite majoritaire du segment de la
personne. Sans cette precaution, une personne contribuerait a definir le stereotype auquel
on compare sa propre prediction.

Les cellules ou les deux coincident sont **exclues** : elles ne separent rien. Sur les
150 personnes et l'axe ideologique, il reste **4 317 cellules sur 22 350**, soit 19,3 pour
cent. Parmi elles, on ne garde que les erreurs, et on les repartit en erreur vers la
moyenne (`m_pop`), erreur vers le stereotype (`m_seg`), et erreur ailleurs.

**Deux lignes sont tautologiques et ne sont pas des resultats.** `B0 mode` predit `m_pop`
par construction : sa part stereotype ne peut etre que proche de zero, et elle vaut 0,100.
`B1 argmax` maximise la probabilite conditionnelle a l'etiquette : elle predit tres souvent
`m_seg`. Ces deux lignes sont des ancres de lecture. Les comparaisons informatives sont
entre conditions a modele de langage, et entre elles et `B2 argmax`, qui ne voit aucune
demographie, `B3 foret`, qui ne voit que cela, et les humains reinterroges.

### 3.2 Le profil d'erreur, axe ideologie politique

[MESURE, `a28-t3-profil-erreur.csv`, perimetre 150, 5 000 tirages bootstrap sur les personnes]

| condition | cellules separantes | erreurs | vers stereotype | vers moyenne | **part stereotype** | IC 95 % | part des erreurs expliquees |
|---|---|---|---|---|---|---|---|
| agents v8 | 4 314 | 2 340 | 1 208 | 481 | **0,715** | [0,683 ; 0,745] | 0,722 |
| C2 | 4 317 | 2 488 | 1 052 | 672 | **0,610** | [0,582 ; 0,639] | 0,693 |
| agents entretien (v3) | 4 301 | 1 841 | 760 | 532 | 0,588 | [0,551 ; 0,625] | 0,702 |
| agents composite | 4 314 | 1 693 | 686 | 509 | 0,574 | [0,542 ; 0,606] | 0,706 |
| agents enquete | 4 308 | 1 867 | 755 | 569 | 0,570 | [0,538 ; 0,602] | 0,709 |
| **B1 argmax** | 4 317 | 2 064 | 945 | 768 | **0,552** | [0,518 ; 0,585] | 0,830 |
| ***humains vague 2*** | 4 317 | 1 078 | 403 | 348 | ***0,537*** | [0,498 ; 0,576] | 0,697 |
| C3 | 4 317 | 2 158 | 672 | 724 | **0,481** | [0,452 ; 0,511] | 0,647 |
| **B3 foret** | 4 317 | 2 028 | 852 | 975 | 0,466 | [0,433 ; 0,499] | 0,901 |
| **B2 argmax** | 4 317 | 1 816 | 692 | 847 | 0,450 | [0,413 ; 0,487] | 0,847 |
| agents v7 | 4 307 | 2 384 | 754 | 1 075 | 0,412 | [0,372 ; 0,453] | 0,767 |
| B0 tirage | 4 317 | 2 744 | 737 | 1 237 | 0,373 | [0,348 ; 0,399] | 0,719 |
| agents demographiques (v6) | 4 308 | 2 342 | 667 | 1 132 | 0,371 | [0,340 ; 0,402] | 0,768 |
| B0 mode | 4 317 | 2 540 | 243 | 2 189 | 0,100 | [0,086 ; 0,116] | 0,957 |

**H7 passe, et ne dit presque rien.** Les huit conditions a modele de langage sont toutes
au dessus de `B0 mode` de 0,271 a 0,615, p de bootstrap 0,0002 et p ajuste par Holm 0,0018
dans les huit cas [MESURE, `a28-t3-contrastes.csv`]. Mais la comparaison etait gagnee
d'avance : `B0 mode` predit la moyenne par definition.

**H8 passe, et dit quelque chose.** **C3, qui ne recoit aucune etiquette, est a 0,481 et C2,
qui recoit onze attributs demographiques, est a 0,610 : difference moins 0,129
[moins 0,160 ; moins 0,099], p ajuste 0,0018.** Meme modele, memes personnes, memes
questions, memes traces ; la seule chose qui change est l'etiquette, et elle deplace le
profil d'erreur de treize points vers le stereotype de segment. C'est la mesure la plus
propre du rapport, parce qu'elle est une ablation et non une comparaison entre familles de
methodes.

**Le chiffre qui vide la prediction de sa portee.** **Les memes humains reinterroges sont a
0,537.** Un humain qui change d'avis en deux semaines se trompe vers la modalite
majoritaire de son segment ideologique dans 54 pour cent des cas. Deux conditions sur huit
sont a moins de 4 points de ce plancher, trois sont dessous, et **`B1 argmax`, une regression
logistique, est a 0,552, c'est a dire au niveau des agents riches de Stanford et au dessus
du plancher humain**. Sur le perimetre 1 052, `B1 argmax` monte a **0,653** et `B3 foret` a
**0,599**, contre 0,553 pour `agents composite` et 0,530 pour `agents enquete` [MESURE].

**Conclusion du test 3, sans adoucissement : se tromper vers le stereotype de son segment
n'est pas une propriete du langage, c'est une propriete du fait de disposer de l'etiquette.**
Une regression logistique sur onze attributs demographiques le fait autant, et sur le grand
perimetre elle le fait davantage.

### 3.3 Le profil d'erreur par axe

[MESURE, `a28-t3-profil-erreur.csv`, perimetre 150]

| condition | ideologie | genre | age | education | profil croise |
|---|---|---|---|---|---|
| agents v8 | **0,715** | 0,563 | 0,564 | 0,539 | 0,588 |
| C2 | 0,610 | 0,636 | 0,554 | **0,652** | 0,559 |
| agents entretien (v3) | 0,588 | 0,517 | 0,500 | 0,576 | 0,512 |
| agents composite | 0,574 | 0,528 | 0,504 | 0,585 | 0,509 |
| agents enquete | 0,570 | 0,574 | 0,515 | 0,587 | 0,514 |
| B1 argmax | 0,552 | 0,492 | 0,485 | 0,531 | 0,484 |
| *humains vague 2* | *0,537* | *0,564* | *0,538* | *0,563* | *0,516* |
| C3 | 0,481 | 0,527 | 0,463 | 0,557 | 0,430 |
| B3 foret | 0,466 | 0,440 | 0,382 | 0,460 | 0,389 |
| B2 argmax | 0,450 | 0,414 | 0,392 | 0,406 | 0,371 |
| agents v7 | 0,412 | 0,529 | 0,482 | 0,538 | 0,384 |
| B0 tirage | 0,373 | 0,471 | 0,440 | 0,444 | 0,392 |
| agents demographiques (v6) | 0,371 | 0,451 | 0,437 | 0,570 | 0,370 |
| B0 mode | 0,100 | 0,186 | 0,136 | 0,205 | 0,077 |

**L'axe ideologique est le seul ou une condition se detache franchement du plancher humain**,
`agents v8` a 0,715 contre 0,537. Sur le genre, l'age et l'education, presque toutes les
conditions sont a moins de 5 points des humains. **C'est une nouvelle confirmation, par une
mesure independante, que l'ideologie est le seul axe qui porte quelque chose** dans ce
dossier, ce que a1 et a23 disaient deja par une autre voie.

### 3.4 Le rappel des cellules minoritaires : l'ordre s'inverse

Definition de a8 section 6, memes lignes, memes 150 personnes. Une modalite est minoritaire
si moins de 10 pour cent, puis moins de 20 pour cent, des repondants de l'item l'ont
choisie. [MESURE, `a28-t3-minorites.csv`]

| condition | rappel, seuil 10 % | precision | masse predite | rappel, seuil 20 % |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,474*** | 0,448 | 0,035 | ***0,582*** |
| agents entretien (v3) | **0,256** | 0,233 | 0,037 | 0,345 |
| agents composite | **0,254** | 0,255 | 0,033 | 0,352 |
| **C3** | **0,220** | 0,132 | 0,056 | 0,278 |
| agents enquete | 0,191 | 0,179 | 0,036 | 0,259 |
| agents v8 | 0,142 | 0,118 | 0,040 | 0,197 |
| agents demographiques (v6) | 0,137 | 0,280 | 0,016 | 0,173 |
| **C2** | 0,129 | 0,099 | 0,043 | 0,204 |
| B0 tirage | 0,082 | 0,073 | 0,037 | 0,115 |
| agents v7 | 0,059 | 0,096 | 0,021 | 0,121 |
| B1 argmax | 0,046 | 0,158 | 0,010 | 0,131 |
| B2 argmax | 0,027 | 0,455 | 0,002 | 0,100 |
| **B3 foret** | **0,008** | 0,207 | 0,001 | 0,054 |
| B0 mode | 0,000 | sans objet | 0,000 | 0,000 |
| *masse humaine de reference* | | | *0,033* | *0,108* |

**C'est le resultat le plus net des trois tests, et il n'etait pas demande.** Sur les
cellules ou la vraie reponse est minoritaire, **l'ordre des methodes s'inverse par rapport
a l'exactitude moyenne.** `B2 argmax`, la methode la plus exacte du dossier a 0,6717,
retrouve **2,7 pour cent** des reponses minoritaires. `B3 foret`, l'adversaire de Ku 2026 a
0,6340 d'exactitude, en retrouve **0,8 pour cent**, la derniere place de treize. Les deux
conditions riches de Stanford en retrouvent 25 pour cent, cinq fois plus que `B1 argmax` et
trente deux fois plus que la foret. **C3, notre agent local prive de toute etiquette et
battu par tout le monde sur l'exactitude, en retrouve 22 pour cent**, trois a vingt sept fois plus
que les predicteurs statistiques.

**La masse minoritaire predite le dit autrement.** Les humains attribuent une reponse
minoritaire a 3,3 pour cent des cellules. Les conditions de Stanford et nos deux conditions
en produisent 1,6 a 5,6 pour cent, du bon ordre de grandeur. `B1 argmax` en produit 1,0,
`B2 argmax` 0,2 et `B3 foret` 0,1 pour cent. **Les predicteurs statistiques ne se trompent
pas sur les minorites, ils ne les produisent pas du tout.**

C'est la reponse la plus directe a Ku 2026 que ce rapport contienne, et elle n'est pas dans
le terme de dispersion, elle est dans la queue de distribution.

---

## 4. Ce que ces resultats changent au classement des cinq idees

Le classement de `CORPUS-SYNTHESE.md` section 4 etait etabli sur des tests decisifs non
executes. Ils le sont. Voici le classement revise, avec ce qui monte et ce qui tombe.

### Ce qui tombe : le rang 2 sort du classement

**Le rang 2, « la simulation efface ce qui n'est pas deductible de l'etiquette », tombe de
la deuxieme a la derniere place, et il faut le dire.** Son test decisif etait ecrit noir sur
blanc : « si la statistique ecrase uniformement et le modele selectivement, la these tient ».
**Elle ne tient pas.** Les seules methodes dont l'ecrasement est selectif sont statistiques,
`B2 argmax` a +0,333 et `B3 foret` a +0,247 sur le controle a demi echantillon, quand les
huit conditions a modele de langage sont dans le bruit et que deux d'entre elles sont
negatives sur le grand perimetre. L'uniformite, seul point favorable, ne survit pas a son
propre controle d'echelle. **Ku 2026 sort de ce test renforce et non affaibli.**

Ce qui reste du rang 2 est ailleurs et n'a pas ete teste ici : l'effet de l'etiquette sur
le **gonflement des ecarts entre groupes**, facteur 25 chez nous sur deux echantillons
independants, reste etabli et sans equivalent publie. Mais ce n'est pas « ce que la
simulation efface », c'est ce qu'elle exagere. **Les deux enonces ne doivent plus etre
vendus ensemble.**

### Ce qui monte : le rang 3 devient le rang 1, par sa moitie minoritaire

**Le rang 3 monte, mais pas par la porte qu'on croyait.** Sa moitie « stereotype » est
mesurable, elle passe son test et elle ne prouve presque rien : `B1 argmax` fait aussi bien
que les agents riches, le plancher humain est a 0,537, et sur le grand perimetre la
regression logistique depasse tout le monde a 0,653. **Se tromper par stereotype de segment
n'est pas propre au langage.**

**Sa moitie « part minoritaire » est le resultat le plus fort de ce rapport.** Sur les
cellules a reponse minoritaire, l'ordre des methodes s'inverse : les agents de Stanford
retrouvent 25,6 pour cent des reponses minoritaires, C3 en retrouve 22,0, `B1 argmax` 4,6,
`B2 argmax` 2,7 et **la foret aleatoire 0,8**, contre 47 pour cent pour les memes humains
reinterroges. Le rapport de masse minoritaire predite le confirme : les predicteurs
statistiques n'en produisent presque aucune. **C'est le seul endroit du dossier ou un modele
de langage bat une methode statistique d'un facteur trente sur une quantite qu'un institut
achete.** Et c'est une reponse a Ku 2026 dans une metrique qu'ils ne mesurent pas.

Reformulation proposee du rang, en un enonce : **« La simulation par modele de langage garde
les minorites d'opinion que la statistique detruit, et elle les garde mal ; la statistique
ne les produit pas du tout. »** Le second membre est une critique du domaine tout entier, le
premier est la contribution.

### Ce qui reste, diminue : le rang 1 descend au deuxieme rang

**Le rang 1 tient au niveau du groupe de methodes et tombe au niveau de chaque methode.**
Il faut choisir laquelle des deux phrases on porte.

- La phrase forte, **« la condition X s'ecarte davantage des humains sur les items
  sensibles »**, est morte : elle ne survit ni a Holm ni a Benjamini Hochberg sur la famille
  de 52 tests, et elle est portee par 3 items binaires sur 12.
- La phrase moyenne, **« les methodes a modele de langage se comportent en bloc autrement
  que les predicteurs statistiques sur les items que NORC a mesures sensibles au mode »**,
  tient a p = 0,0008 sur la distance et p = 0,0009 sur la version continue, avec un test de
  permutation sur les etiquettes de methode dont les limites sont ecrites en 1.6.
- La mesure nouvelle qui la soutient le mieux est la **dispersion** et non la distance : sur
  les 8 items ordinaux, les conditions riches de Stanford effacent 8 a 15 points de variete
  de plus sur les items sensibles, quand les trois predicteurs statistiques informes sont
  entre moins 1 et plus 7 points.

Il descend d'un rang parce que sa mesure la plus vendable, la distance, s'effondre sur les
items ordinaux, et parce que C2 et C3 ne le portent pas : elles changent de signe des qu'on
retire les quatre items nominaux.

### Les rangs 4 et 5 ne sont pas touches

Ni le rang 4, « marges justes, structure fausse », ni le rang 5, « la part effacee est la
part incoherente », n'ont ete testes ici. Leur position relative change neanmoins par
consequence : **le rang 4 remonte mecaniquement**, puisque son test decisif, le classifieur
synthetique contre reel sur nos huit conditions, coute quinze lignes de code et n'a
toujours pas ete fait, et que le rang 2 lui a libere une place. Son defaut reste le meme :
c'est l'idee la plus deja dite du lot.

### Le classement revise

| rang | idee | etat apres a28 |
|---|---|---|
| **1** | **La simulation garde les minorites d'opinion que la statistique detruit** | monte de la 3e place, moitie minoritaire seulement, facteur 30 sur la foret aleatoire, mesure et non teste ailleurs |
| **2** | La simulation devie la ou les humains se surveillent | descend de la 1re, tient en bloc a p = 0,0008, tombe methode par methode apres correction |
| **3** | Marges justes, structure fausse | inchangee, remonte par defaut, test decisif toujours pas fait |
| **4** | La part effacee est la part incoherente | inchangee, non testee, adversaire serieux |
| **5** | La simulation efface ce qui n'est pas deductible de l'etiquette | **tombe de la 2e a la derniere**, test decisif execute et resultat de signe inverse |

---

## 5. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. Que la famille d'hypotheses du projet est desormais fixee et ecrite, 52 tests pour le
   test 1, 14 pour le test 2, 9 pour le test 3, et que les corrections de Holm et de
   Benjamini Hochberg sont appliquees et publiees ligne a ligne
   [MESURE, `a28-t1-corrections.csv`, `a28-t2-selectivite.csv`, `a28-t3-contrastes.csv`].
2. Que l'effet de a25 **ne survit pas** a cette correction condition par condition, le
   meilleur p ajuste par Holm valant 0,144 sur 52 tests et 0,037 sur les 13 de la seule
   sous famille primaire [MESURE].
3. Que le motif de groupe survit : huit conditions a modele de langage contre cinq
   predicteurs statistiques, difference de +0,0504 de contraste de distance, p de 0,0008 par
   permutation des etiquettes de methode ; +0,3555 sur la version continue construite a
   partir des ampleurs de `corpus/04`, p de 0,0009 [MESURE].
4. Qu'une foret aleatoire sur demographies, replantee chez nous avec le protocole de a2,
   obtient 0,6340 d'exactitude, un rapport de dispersion intra median de 0,330, le plus bas
   des treize methodes hors `B0 mode`, et **ne montre aucun contraste sur les items
   sensibles**, +0,0027, p = 0,914 [MESURE].
5. Que l'ecrasement selectif, tel qu'il est defini par la correlation entre rapport intra et
   part expliquee, est une propriete des **predicteurs statistiques** et non des modeles de
   langage, et que ce resultat survit au controle a demi echantillon qui elimine l'artefact
   de denominateur partage [MESURE, `a28-t2-demi-echantillon.csv`].
6. Que l'etiquette demographique deplace le profil d'erreur de 12,9 points vers le
   stereotype de segment, a modele, personnes, questions et temperature constants, C3 a
   0,481 contre C2 a 0,610, intervalle [-0,160 ; -0,099] [MESURE].
7. Que sur les cellules a reponse minoritaire, le rappel va de 0,008 pour la foret aleatoire
   a 0,256 pour les agents entretien, contre 0,474 pour les memes humains reinterroges, et
   que les trois predicteurs statistiques informes ne produisent qu'entre 0,1 et 1,0 pour
   cent de masse minoritaire quand les humains en produisent 3,3 [MESURE].
8. Que la mesure de dispersion, rapport d'entropie par item, separe les conditions riches de
   Stanford des predicteurs statistiques **y compris sur les seuls items ordinaux**, la ou
   la mesure de distance ne le fait plus [MESURE].

### Interdit

1. **Ecrire qu'une condition donnee s'ecarte davantage des humains sur les items sensibles.**
   Aucune ne passe la correction sur la famille declaree. La seule formulation defendable
   porte sur le groupe de methodes, avec la limite de la section 1.6.
2. **Ecrire que nos agents locaux montrent le contraste.** C2 et C3 changent de signe des
   qu'on retire les quatre items nominaux, a moins 0,052 et moins 0,019, et leur contraste
   de dispersion va dans le sens oppose a celui des conditions de Stanford.
3. **Ecrire que le modele de langage ecrase selectivement et la statistique uniformement.**
   La mesure dit l'inverse. Toute phrase de ce type doit etre retiree du dossier et de
   `CORPUS-SYNTHESE.md` section 4 rang 2.
4. **Ecrire que le modele se trompe par stereotype la ou la statistique se trompe par la
   moyenne.** `B1 argmax` est a 0,552 sur le perimetre 150 et 0,653 sur 1 052, au dessus de
   cinq des six conditions de Stanford. Seule l'ablation C2 contre C3 est defendable, et
   elle parle de l'etiquette, pas du langage.
5. **Citer la part stereotype sans citer le plancher humain de 0,537.** Un humain
   reinterroge fait la meme chose une fois sur deux.
6. **Presenter le contraste de groupe de la section 1.6 comme un test pre enregistre.** Il
   ne l'est pas, il est ajoute apres avoir vu que les tests par condition tombaient.
7. **Presenter les scores S2 et S3 comme des mesures.** Sur les 12 items sensibles, 5
   seulement ont une ampleur publiee, et 6 des 16 valeurs de domaine sont marquees
   [HYPOTHESE]. Le score est une construction defendable ligne a ligne, pas une donnee.
8. **Citer `B0 tirage` comme un cas d'ecrasement selectif.** Sa correlation de 0,560 est une
   identite arithmetique, pas un resultat.
9. **Ecrire que la foret aleatoire echoue partout.** Elle bat `B1 argmax` en exactitude,
   0,6340 contre 0,6209, et elle est la methode la plus selective apres `B2` sur le controle
   a demi echantillon. Elle n'echoue que sur les minorites, et la elle echoue completement.

---

## 6. Ce que je n'ai pas pu verifier

1. **Le pre enregistrement n'est pas verifiable par un tiers.** Les familles d'hypotheses
   sont ecrites dans les docstrings des trois scripts et je certifie qu'elles ont ete
   ecrites avant l'execution, mais rien dans les fichiers ne l'horodate. Un depot public
   avec un tag avant execution serait la seule preuve. Ce n'est pas fait.
2. **Les p de permutation sur les etiquettes de methode reposent sur 13 unites** dont
   plusieurs sont des variantes du meme systeme, les six conditions de Stanford venant du
   meme paquet et nos deux conditions du meme modele. Le nombre effectif d'unites
   independantes est probablement plus proche de 4 ou 5 que de 13, et je n'ai pas de moyen
   de le chiffrer.
3. **La foret aleatoire n'a pas ete reglee.** 300 arbres, feuilles d'au moins 5
   observations, aucun balayage d'hyperparametres. Une foret mieux reglee ecraserait
   probablement moins ou plus, et je ne sais pas dans quel sens. Ku 2026 ne publie pas ses
   reglages non plus.
4. **La segmentation par profil croise est fragile sur 150 personnes.** Elle produit
   jusqu'a 18 segments pour 150 individus, soit huit personnes par segment en moyenne.
   L'estimateur sans biais de Simpson exige deux observations par segment et les segments
   vides sont ecartes, mais la variance d'echantillonnage reste elevee, et c'est
   probablement ce qui explique que le perimetre 1 052 donne des signes differents.
5. **Le rapport d'entropie est instable sur les items a faible entropie humaine.** Aucun
   seuil n'a ete impose sur cette mesure, contrairement au rapport de dispersion intra ou le
   seuil de 0,05 ecarte 3 items sur 149. Les valeurs de C2 et C3 sur les items sensibles,
   qui vont dans le sens oppose aux conditions de Stanford, peuvent en partie venir de la.
6. **La correspondance entre `m_seg` et « stereotype » est une convention.** Predire la
   modalite majoritaire du segment d'une personne n'est pas necessairement un stereotype :
   c'est aussi ce que fait un estimateur bayesien correct en l'absence d'autre information.
   Le mot est celui de `CORPUS-SYNTHESE.md`, la mesure est ce qu'elle est.
7. **Aucun test n'a ete fait sur Twin-2K-500 ni sur le WVS.** Les trois tests sont sur le
   GSS et sur lui seul, avec un croisement NORC qui n'existe que pour le GSS.
8. **Les invites de C2 et C3 n'ont toujours pas ete comparees a celles de Stanford.** Limite
   ouverte depuis a17, a23 et a25, et elle pese ici sur toute lecture de C2 et C3, qui sont
   precisement les deux conditions qui se comportent differemment des six autres.
9. **Le mode de collecte de la verite terrain de Stanford n'est toujours pas documente.**
   Si les vagues 1 et 2 ont ete administrees en ligne sans enqueteur, la population de
   reference est deja du cote non observe, ce qui change l'interpretation du signe partout
   dans le test 1. La verification est une lecture d'arXiv 2411.10109 et elle n'est pas
   faite.
10. **Le seuil de minorite est descriptif et calcule sur la population observee.** Il ne
    fuit dans aucune prediction, mais il n'est pas independant de l'echantillon, et le
    rappel minoritaire des humains vague 2 est mecaniquement avantage par le fait que les
    memes personnes sont des deux cotes.

---

## 7. Questions ouvertes pour Simon

1. **Faut il porter le rang 1 sur son contraste de groupe, sachant qu'aucune condition
   individuelle ne survit a la correction ?** Le p de 0,0008 est reel et le motif est net,
   mais l'unite de test devient la methode et il n'y en a que treize dont plusieurs sont
   parentes. C'est un enonce sur une population de methodes, ce qui n'est pas la facon dont
   ce domaine ecrit ses resultats. Est ce publiable ou est ce un artifice ?
2. **Le rang 2 doit il sortir du dossier ou changer de formulation ?** Son test decisif a
   ete execute et il donne le signe inverse. Il reste l'effet de l'etiquette sur le
   gonflement, facteur 25, qui est solide mais qui n'est pas « ce que la simulation efface ».
   Faut il scinder le dossier en deux revendications, l'une sur ce qui est efface, l'autre
   sur ce qui est exagere, ou abandonner la seconde ?
3. **Le resultat sur les minorites merite t il d'etre le resultat principal ?** Un facteur
   trente entre les agents de Stanford et une foret aleatoire sur une quantite qu'un institut
   achete est le chiffre le plus vendable du dossier, et il n'etait dans aucune des cinq
   idees. Il a pourtant deux defauts : il vient de a8 et il est donc a moitie deja mesure
   chez nous, et le plancher humain a 0,474 rappelle que meme la meilleure condition est a
   la moitie de ce qu'un humain reproduit de lui meme.
4. **Que faire du plancher humain a 0,537 sur la part stereotype ?** Il est le chiffre le
   plus honnete du rapport et il tue la moitie de la these du rang 3. Faut il le publier au
   milieu du tableau, comme ici, ou en faire une section a part qui pose la question de ce
   qu'un modele devrait imiter ?
5. **La nuit de calcul sur gpt-oss-20b doit elle rejouer les trois tests ou seulement a25 ?**
   Le test 1 depend de C2 et C3 dans ses lignes les plus fragiles ; le test 3 depend d'elles
   pour son ablation la plus propre, C3 contre C2. Rejouer les trois demande une seule
   commande de plus, `a28_*.py` etant ecrits pour lire les traces sans rien recalculer.
6. **Faut il un pre enregistrement horodate avant la prochaine campagne ?** La dette de
   a17 est soldee sur le papier, elle ne l'est pas sur la preuve. Un depot public avec un
   tag date coute dix minutes et retire la principale objection qu'un relecteur peut faire
   a tout ce rapport.
7. **Le mot « stereotype » est il tenable ?** Predire la modalite majoritaire du segment
   d'une personne est aussi ce que fait un estimateur correct. Si le mot ne tient pas, la
   moitie de la formulation du rang 3 ne tient pas non plus, et c'est une question de
   vocabulaire qui se tranche avec un psychologue et non avec un calcul.

---

## Rejouer

```
.venv/bin/python analyses/a28_test1_mode.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 50000
.venv/bin/python analyses/a28_test2_ecrasement.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 20000
.venv/bin/python analyses/a28_test3_stereotype.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 5000
.venv/bin/python analyses/a28_figures.py
```

Sans les deux caches, le premier script recalcule les baselines de a2, environ trois
minutes, et entraine la foret aleatoire, environ deux minutes sur quatre coeurs ; avec les
caches, quinze secondes. Durees mesurees : test 1, 64 secondes ; test 2, environ vingt
minutes, le cout etant dans les permutations de correlation ; test 3, trois minutes ;
figures, quatre secondes. Graine 20260908 partout, graine de protocole 20260903 heritee de
a2. Aucun appel de modele, aucune ecriture dans `data/`.
