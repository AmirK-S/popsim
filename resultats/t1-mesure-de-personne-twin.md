# t1. La mesure de personne repliquee sur Twin-2K-500 : un autre pipeline, treize configurations

Rapport du 9 septembre 2026, nuit. Il execute le verrou 3 de `MODELE-DU-MONDE.md` 10.5,
« rejouer la chute sous permutation sur Twin, zero appel », et il repond au point 10 de la
section des limites de `resultats/a45-relecture-adverse-2.md` : « la replication sur Twin de
la chute sous permutation n'existe pas, et c'est ce qu'un relecteur demandera en premier
apres avoir lu la section 1.1 : si le chiffre depend de la segmentation sur le GSS, il faut
savoir s'il depend aussi du jeu ».

**Le preenregistrement est `resultats/t1-preenregistrement.md`, ecrit le 9 septembre 2026 a
01 h 08 CEST (8 septembre, 23 h 08 UTC), avant l'ecriture du premier script et avant tout
calcul de resultat.** Depot a `d536169dc5361c38edcd723d48816e2ddd06dc4f`. Sa section 1 liste
ce qui avait ete inspecte avant de l'ecrire, et ce n'etait que de la structure : nombre
d'items, nombre de sujets, modalites et effectifs des six variables demographiques
candidates, largeur du codage indicatrice, et un banc de temps sur matrices aleatoires.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. **Aucun script
existant n'a ete modifie** ; `a44_commun`, `a44_mesures`, `a1_double_distorsion`,
`a6_double_distorsion_hors_gss`, `i3b_twin`, `i3b_commun`, `i3_commun` et `a2_commun` sont
importes tels quels, memes graines, memes definitions, memes 108 items, memes 2 058
personnes. Le `llama-server` de R2 n'a pas ete touche.

Cinq scripts nouveaux, `analyses/t1_commun.py`, `t1_baselines.py`, `t1_mesures.py`,
`t1_nul.py`, `t1_verdict.py`, `t1_placebo.py`, plus `t1_figure.py`.

---

## Reponse en une ligne

**La mesure de personne se transporte, et elle donne sur Twin un resultat inverse de celui
du GSS : les treize configurations sont toutes du cote du porteur de personne, 42 a 71 pour
cent du plancher humain, et les trois seuls gabarits du tableau sont les trois predicteurs
statistiques, `B1 argmax` 10,1 pour cent, `B2 argmax` 11,6 et `PMM k=10` 13,6**
[MESURE, `t1-chute-segmentations.csv`, 200 permutations, IC par sous echantillonnage
pivote sur les personnes]. **Le plancher humain de Twin, les memes 2 058 personnes
reinterrogees a la vague 4, perd 45,6 pour cent de son exactitude quand on melange qui est
qui a l'interieur de son segment, et les deux temoins aveugles a la personne perdent
0,05 a 0,10 pour cent, c'est a dire zero.** Les seize conditions de la famille primaire ont une
chute strictement superieure a celle du temoin `B0 tirage`, **`p` de Holm 0,008 pour les
seize, sur 2 000 sous echantillons dont 100 pour cent sont du meme signe** [MESURE,
`t1-holm-contre-b0.csv`].

**Le second resultat est le plus utile au dossier, et c'etait la prediction la plus risquee
du preenregistrement : la sensibilite a la segmentation que `a47` E2 a trouvee sur le GSS
ne se produit pas sur Twin.** Sur le GSS, passer de l'ideologie seule a genre x ethnicite x
age multiplie la chute de `agents v8` par **3,72** et celle de `C2` par **2,56**, les deux
seules conditions qui recoivent l'etiquette ideologique en clair, quand les quinze autres
tiennent entre 0,96 et 1,45. Sur Twin, **le facteur maximal sur les treize configurations
vaut 1,064** et le minimum 1,006 [MESURE, `t1-chute-segmentations.csv`]. **Le chiffre ne
depend pas du jeu ; il depend de ce que la condition a recu en entree**, et l'ablation
propre le montre : `B1 argmax` refait sans les deux seules colonnes politiques du bloc
Demographics voit son facteur passer de **1,212 a 0,575** et sa chute sous l'ideologie
**monter** de 0,0835 a 0,0942 alors que son exactitude **baisse** de 0,5183 a 0,5134
[MESURE, `t1-placebo-etiquette.csv`].

**Le troisieme resultat replique `a44` sans nuance : la double distorsion de `a6` sur Twin
est une quantite de gabarit.** Sur l'axe ideologie, le generateur nul conditionnellement
independant reproduit le ratio inter des treize configurations a **102,4 a 106,9 pour
cent** et le ratio intra a **98,9 a 99,7 pour cent** ; il reproduit meme le retest humain a
127,1 et 99,4 pour cent [MESURE, `t1-generateur-nul.csv`, 200 replicats]. Et les deux
ratios sont **exactement** invariants sous permutation des personnes intra segment, ecart
`0,000e+00` sur dix neuf conditions et quatre segmentations : c'est le fait arithmetique de
`a44` 3.1, verifie et non suppose.

**Le quatrieme resultat va contre `a45` objection 1.3, et il faut l'ecrire.** Sur le GSS la
chute et l'exactitude brute partagent 82 pour cent de leur variance, ce qui rendait la
mesure de personne presque redondante. **Sur Twin, a perimetre de conditions comparable,
elles n'en partagent que 28 pour cent**, Pearson 0,529 contre 0,828 [MESURE,
`t1-correlation-chute-exactitude.csv`]. La version partialisee separe encore mieux que la
brute : les residus de la regression de la chute sur l'exactitude sont **negatifs pour les
trois predicteurs statistiques et positifs pour les treize configurations, sans une
exception** [MESURE, `t1-correlation-residus.csv`].

**Ce qui ne se transporte pas.** La condition « demographies seules » du GSS, `agents v6` a
0,236 et `agents v8` a 0,267 du plancher, correspond sur Twin a `Demographics Only` qui vaut
**0,556**, soit un facteur 2,1 a 2,4. La condition « persona complete » se transporte au
contraire au chiffre : `agents composite` du GSS vaut 0,696 et `JSON Persona - GPT4.1` de
Twin vaut 0,708.

---

## 1. Le preenregistrement, le score des huit predictions, et les ecarts

### 1.1 Les huit predictions, ecrites avant tout calcul [MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | les deux temoins ont une chute inferieure a 0,5 pour cent sous les quatre segmentations | **tenue.** `B0 mode` et `B0 tirage` : chute relative de moins 0,048 a moins 0,097 pour cent sur les huit couples, et l'IC de la chute de `B0 tirage` contient zero |
| **P2** | `Demographics Only` a la plus petite part du plancher des treize, et elle est sous 0,30 | **fausse sur ses deux moities.** Elle vaut **0,556**, et deux configurations sont plus basses, `Finetuning 500` a 0,420 et `Summary + JSON` a 0,533 |
| **P3** | `Text Persona` et `JSON Persona` sont au dessus de 0,40 du plancher | **tenue**, 0,579 a 0,708 ; mais elle ne separe rien, **les treize le sont** |
| **P4** | la part du plancher change moins entre `S_ideo` et `S_gra` sur Twin que sur le GSS | **tenue, et c'est le resultat du rapport.** Facteur maximal 1,064 sur Twin contre 3,72 sur le GSS |
| **P5** | le ratio inter est reproduit a plus de 95 pour cent par le nul pour les treize, et l'IC de `d` contient zero pour au moins dix | **tenue sur la premiere moitie, fausse sur la seconde.** Part reproduite 102,4 a 106,9 pour cent ; **aucun** IC de `d` ne contient zero, `z` de moins 2,4 a moins 5,6 |
| **P6** | la correlation de Pearson entre chute et exactitude est superieure a 0,80 sur Twin | **fausse, et c'est une bonne nouvelle pour la mesure.** 0,512 a 0,529 sur les seize conditions de la famille |
| **P7** | `Finetuning 500` est du cote du gabarit, part sous 0,15 | **fausse.** 0,420, du cote du porteur de personne, alors que `i3b` en fait le generateur le plus degenere du dossier |
| **P8** | Spearman entre la part du plancher et le `tau*` de `i3b` superieur a 0,5 | **tenue de justesse**, 0,528 a 0,582 selon la segmentation |

**Trois predictions fausses sur huit, dont deux fausses sur les deux moities.** C'est la
seule preuve interne que le preenregistrement a bien ete ecrit avant le calcul.

### 1.2 Les ecarts au preenregistrement, tous declares

| | ecart | pourquoi |
|---|---|---|
| **E1** | **Deux conditions ajoutees a la famille descriptive** : `B0 mode` et `B0 tirage` etaient prevus au preenregistrement section 3, ils y sont ; rien n'est ajoute. **En revanche `t1_placebo.py` n'etait pas prevu.** | Ecrit apres avoir vu que P4 etait tenue et que le dossier n'avait toujours aucune ablation propre d'etiquette, `a44` E1 le reclamant. Il porte une prediction ecrite en tete de son propre fichier, avant son execution, et il est signale post hoc partout. |
| **E2** | **Le nombre de permutations a l'interieur d'un sous echantillon n'etait pas fixe** ; il vaut **30**. | Le preenregistrement fixe `P = 200` permutations pour l'estimation ponctuelle, ce qui a ete fait, et `S = 200` sous echantillons, ce qui a ete fait ; il ne dit rien du nombre de permutations dans chaque sous echantillon. Trente suffisent parce que la moyenne de la chute sur 200 sous echantillons moyenne aussi ce bruit la. |
| **E3** | **Le test de verdict a du etre refait avec `S = 2 000` sous echantillons**, dans `t1_verdict.py`. | Avec `S = 200`, la plus petite valeur de `p` atteignable vaut `1 / 200 = 0,005`, et Holm sur seize tests exige `p <= 0,003125`. Le verdict etait arithmetiquement hors d'atteinte quelle que soit la force du signal. **Ce n'etait pas un resultat, c'etait une resolution insuffisante**, et le premier passage l'a produite : `p` de Holm 0,08 pour les seize. Avec 2 000 sous echantillons le plancher tombe a 0,0005 et les seize passent a 0,008. La valeur declaree au preenregistrement etait mal dimensionnee, et c'est ecrit ici plutot que corrige en silence. |
| **E4** | **Q4 est estime avec 10 permutations d'etiquettes de segment par replicat nul et 30 pour la population**, ce qui etait declare ; **Q5, les six axes, tourne sur 50 replicats et non 200**, ce qui l'etait aussi. | Rien de neuf, rappele pour memoire. |
| **E5** | **La segmentation `S_parti` a ete ajoutee au preenregistrement, pas au plan de `a44`.** | Twin a le parti, `QID20`, que le GSS de `a44` n'avait pas. Elle est descriptive et n'entre dans aucune famille. |

---

## 2. Protocole

### 2.1 Le materiau

2 058 personnes, **108 colonnes categorielles de la vague 4** sur 126, type `MC` ou `Matrix`
au catalogue, decoupage identique a celui de `a6` et de `a2`. Taux de cellules vides
**24,07 pour cent**, identique pour les quinze tables parce que plusieurs experiences sont
inter sujets : le masque est le meme partout et la comparaison est appariee.

Les quinze tables, treize configurations plus les deux references humaines, sont chargees
par **`i3b_twin.charger_twin_commun` appelee telle quelle**, qui les met dans une
nomenclature commune et les aligne sur les 2 058 sujets ; elle appelle elle meme
`a6.charger_twin` et `a6.lire_formatte`. `a6.charger_twin` est appelee une seconde fois par
`t1_commun.charger` pour recuperer `est_ordinal` et les six axes de `a6` sans les
reconstruire. **L'ordre des 108 items de `a6` et de `i3b` est verifie identique par
assertion a chaque execution** [CONFIRME].

**La verite est la vague 4** ; **le plancher humain est le retest, les vagues 1 a 3 des
memes personnes.** C'est la convention de `a6` et non celle de `i3b`, qui inverse les deux ;
elle est reprise ici parce que la question posee est celle de `a44`, ou la verite est la
vague 1 du GSS et le plancher la vague 2.

**Trois configurations ne couvrent pas les 2 058 sujets** : `JSON Persona - GPT4.1-mini`
1 000, `LLM Finetuning (500 training samples)` 1 558, `JSON Persona (Predicted Output) -
GPT4.1` 2 050. Chacune est mesuree sur son perimetre, **avec le plancher humain recalcule
sur les memes personnes**, et aucune valeur absolue n'est comparee d'un perimetre a l'autre.
Le plancher varie peu, 0,4444 a 0,4619 de chute relative selon le perimetre et la
segmentation, mais il varie, et la colonne « part du plancher humain » est la seule
comparable.

### 2.2 Les quatre segmentations

| nom | definition | cellules | contient l'ideologie |
|---|---|---|---|
| `S_ideo` | `QID22`, ideologie a cinq niveaux | **5** | oui |
| `S_fin` | bloc d'ideologie x genre x age | **24** | oui |
| `S_gra` | genre x ethnicite x age | **40** | **non** |
| `S_parti` | `QID20`, parti a quatre niveaux | **4** | non, mais l'axe politique oui |

Aucune personne hors cellule sur les quatre : les six variables demographiques employees
sont completes sur les 2 058 sujets [MESURE]. La segmentation du verdict est **`S_gra`**,
declaree avant calcul, conformement a `a47` E2 qui fait de la segmentation sans ideologie la
lecture principale sur le GSS.

**Reponse a la question de la mission : Twin a l'ideologie et il a le parti.** Le repli sur
genre x age x education n'a donc pas lieu d'etre, et `S_ideo` est l'analogue exact du
`S_ideo` du GSS.

### 2.3 Les cinq predicteurs sans modele de langage, construits ici

`B0 mode`, `B0 tirage`, `B1 argmax` et `B2 argmax` emploient `a2_commun` sans une ligne
modifiee et le decoupage en cinq plis de personnes de `a2_baselines_twin`. `B1` recoit les
**quatorze questions du bloc Demographics** ; `B2` les **494 items categoriels des vagues 1
a 3 qui ne sont pas reposes en vague 4**, `k = 30` voisins, distance de Hamming.

**`PMM k=10` est une transposition et non un import, et c'est declare au preenregistrement
section 10 point 3.** `a35` impute un item du GSS a partir des autres items de la meme
vague, par blocs a retirer du contexte. Sur Twin le contexte est temporel et disjoint par
construction, vagues 1 a 3 contre vague 4, donc il n'y a aucun bloc a retirer. La recette de
tirage chez un donneur, distance euclidienne entre vecteurs de probabilites predites,
`k = 10` donneurs, est celle de `a35_commun.imputations_regression`, ligne pour ligne.

### 2.4 Les intervalles, et pourquoi il y en a deux sortes

Regle declaree au preenregistrement section 7, tiree du controle de `i3b` sur le biais du
tirage avec remise.

- **L'exactitude** est une moyenne par personne : **bootstrap avec remise**, 1 000 tirages.
- **La chute et le gain hongrois** : **sous echantillonnage pivote**, `m = N / 2`, 200 sous
  echantillons, mise a l'echelle par `racine(m / N)`, correction de population finie
  `1 / racine(1 - m / N)`, pivot sur la moyenne des sous echantillons, par
  `i3b_commun.ic_pivote` et `i3b_commun.correction_population_finie` importees telles
  quelles. **Raison : dupliquer une personne dans un segment permet a la permutation de lui
  reassigner ses propres reponses, ce qui gonfle l'exactitude permutee et ecrase la chute.**
  Le tirage avec remise est inadmissible pour cette quantite.
- **Les ratios** : bande des 200 replicats nuls pour l'incertitude du nul, et sous
  echantillonnage pivote **avec le nul retire dans chaque sous echantillon** pour
  l'incertitude d'echantillon. C'est la correction que `a44` limite 8 signalait ne pas avoir
  faite.

### 2.5 La famille de tests et Holm

Famille primaire, **seize conditions** : les treize configurations plus `B1 argmax`,
`B2 argmax` et `PMM k=10`. Test declare : « la chute de la condition est elle superieure a
celle du temoin `B0 tirage`, sur le meme perimetre et sous `S_gra` ». La statistique est la
difference des deux chutes calculee sur le **meme** sous echantillon, donc appariee.
**Correction de Holm sur seize.**

---

## 3. Les controles, executes avant toute lecture

[MESURE, `t1-controles.csv`, 113 lignes]

1. **Bloquant 1, l'invariance.** Le ratio inter et le ratio intra sont **exactement**
   invariants sous permutation des personnes a l'interieur de leur segment, quand la mesure
   et la permutation partagent la segmentation : ecart maximal sur dix neuf conditions et
   quatre segmentations, **`0,000e+00`**, seuil declare `1e-12`. **Passe.** C'est le fait
   arithmetique de `a44` 3.1, retrouve sur un autre jeu d'items et une autre nomenclature.
2. **Bloquant 2, les marginales du nul.** Le generateur nul redonne les marginales par item
   et par segment de la condition qui le parametre : ecart moyen **0,00734** sur les couples
   non replies, 100 replicats, seuil declare 0,01. **Passe.** Il est plus grand que le
   0,00386 de `a44` parce que Twin a cinq segments et non sept et des nomenclatures plus
   courtes, ce qui rend chaque marginale plus concentree.
3. **Le temoin.** `B0 mode` et `B0 tirage` ont une chute relative comprise entre **moins
   0,048 et moins 0,097 pour cent** sur les huit couples condition x segmentation, en valeur
   absolue toujours sous 0,5 pour cent, et l'intervalle de la chute de `B0 tirage` sous
   `S_gra` contient zero. La valeur est negative parce que la moyenne des 200 permutations
   contient la permutation identite avec probabilite nulle et du bruit avec probabilite un.
   **La mesure ne fabrique pas de chute.** C'est le controle qui autorise a lire toutes les
   autres lignes.
4. **Le masque.** Deux configurations sur treize perdent plus de 0,5 pour cent des cellules
   ou la reponse humaine existe : **`JSON Persona (Predicted Output) - GPT4.1-mini`,
   9,918 pour cent**, et **`JSON Persona (Predicted Output) - GPT4.1`, 0,508 pour cent**.
   Ce sont **exactement** les deux configurations et **exactement** les deux chiffres de
   l'ecart E4 de `i3b`, retrouves par un chargeur different et un decompte different
   [MESURE, reproduction independante]. Les deux lignes sont conservees et signalees.
5. **Le repli du generateur nul.** Un couple sur les 76 depasse le seuil declare de 30 pour
   cent : `JSON Persona - GPT4.1-mini` sous `S_gra`, **32,96 pour cent**, 1 000 sujets pour
   40 cellules. Le nul n'est lu que sous `S_ideo`, ou le repli vaut **0,0 pour cent pour les
   dix neuf conditions sans exception**, cinq segments de 137 a 582 personnes etant tous au
   dessus du seuil de cinq repondants sur tous les items ;
   donc **aucune ligne du generateur nul n'est affectee** ; la permutation intra segment,
   elle, n'emploie pas le nul, ce que `a44` E7 precise deja.
6. **La reproduction de `a6`.** Sur l'axe ideologie et en entropie, le ratio inter et le
   ratio intra de t1 redonnent `a6-ratios-par-axe.csv` a **0,30 pour cent** au pire sur les
   quatorze conditions communes, seuil declare 2 pour cent. **Passe.** Sur les six axes
   agreges, la reproduction du tableau principal de `a6` section 2 est meilleure encore :
   `Demographics Only` 1,5802 contre 1,570 publie, `Text Persona - GPT4.1-mini` 3,6717
   contre 3,655, `JSON Persona - GPT4.1` 3,7635 contre 3,733, `Text Persona - Gemini` 3,0356
   contre 3,015, retest humain 1,0074 contre 1,0043 ; et les ratios intra au millieme,
   0,5016 contre 0,502, 0,5578 contre 0,558, 0,7499 contre 0,750, 1,0090 contre 1,0090
   [MESURE, `t1-generateur-nul-six-axes.csv`]. **`a6` est reproduit par un autre chemin de
   chargement.**
7. **L'exactitude.** L'exactitude sur codes entiers egale celle de
   `a2_commun.exactitude_par_personne` sur les chaines, ecart **`0,0`**, seuil `1e-12`.

---

## 4. Tableau 1 : la chute sous permutation des personnes intra segment

[MESURE, `t1-chute-segmentations.csv`, 200 permutations, IC par sous echantillonnage pivote,
segmentation du verdict `S_gra` en gras]

| condition | n | exactitude | chute sous `S_gra` | IC de la chute | **part du plancher, `S_gra`** | `S_ideo` | `S_fin` | `S_parti` | lecture |
|---|---|---|---|---|---|---|---|---|---|
| **humains vagues 1-3, retest** | 2 058 | **0,7119** | **0,3248** | [0,3216 ; 0,3280] | **1,000** | 1,000 | 1,000 | 1,000 | plancher |
| `JSON Persona - GPT4.1` | 2 058 | 0,5738 | 0,1853 | [0,1824 ; 0,1883] | **0,708** | 0,677 | 0,686 | 0,687 | porteur de personne |
| *`JSON Persona (PredOut) - GPT4.1`* | 2 050 | 0,5646 | 0,1822 | [0,1796 ; 0,1850] | **0,707** | 0,671 | 0,682 | 0,684 | porteur de personne |
| `Text Persona - Gemini-Flash2.5` | 2 058 | 0,5505 | 0,1752 | [0,1725 ; 0,1781] | **0,698** | 0,656 | 0,658 | 0,668 | porteur de personne |
| `JSON Persona - GPT4.1-mini` | 1 000 | 0,5439 | 0,1639 | [0,1600 ; 0,1676] | **0,675** | 0,647 | 0,652 | 0,655 | porteur de personne |
| `Text Persona (Reasoning)` | 2 058 | 0,5435 | 0,1625 | [0,1597 ; 0,1655] | **0,655** | 0,620 | 0,628 | 0,631 | porteur de personne |
| `Text Persona (Repeating Questions)` | 2 058 | 0,5489 | 0,1594 | [0,1568 ; 0,1619] | **0,637** | 0,604 | 0,609 | 0,614 | porteur de personne |
| *`JSON Persona (PredOut) - GPT4.1-mini`* | 2 058 | 0,4625 | 0,1335 | [0,1310 ; 0,1361] | **0,633** | 0,606 | 0,608 | 0,611 | porteur de personne |
| `Text Persona - GPT4.1-mini` | 2 058 | 0,5530 | 0,1573 | [0,1549 ; 0,1597] | **0,623** | 0,590 | 0,596 | 0,600 | porteur de personne |
| `Persona Summary - GPT4.1-mini` | 2 058 | 0,5209 | 0,1473 | [0,1442 ; 0,1502] | **0,620** | 0,604 | 0,604 | 0,605 | porteur de personne |
| `Text Persona (Default Temperature)` | 2 058 | 0,5478 | 0,1533 | [0,1511 ; 0,1561] | **0,614** | 0,579 | 0,585 | 0,589 | porteur de personne |
| **`Demographics Only - GPT4.1-mini`** | 2 058 | 0,4996 | 0,1267 | [0,1239 ; 0,1291] | **0,556** | 0,552 | 0,547 | 0,551 | porteur de personne |
| `Persona Summary - JSON Persona` | 2 058 | 0,4742 | 0,1154 | [0,1125 ; 0,1184] | **0,533** | 0,508 | 0,509 | 0,515 | porteur de personne |
| **`LLM Finetuning (500 exemples)`** | 1 558 | 0,4619 | 0,0881 | [0,0837 ; 0,0927] | **0,420** | 0,417 | 0,424 | 0,420 | porteur de personne |
| **`PMM k=10`** | 2 058 | 0,4910 | 0,0305 | [0,0282 ; 0,0327] | **0,136** | 0,122 | 0,116 | 0,135 | **gabarit de groupe** |
| **`B2 argmax`** | 2 058 | 0,5305 | 0,0282 | [0,0255 ; 0,0307] | **0,116** | 0,117 | 0,114 | 0,121 | **gabarit de groupe** |
| **`B1 argmax`** | 2 058 | 0,5183 | 0,0240 | [0,0212 ; 0,0263] | **0,101** | 0,083 | 0,069 | 0,112 | **gabarit de groupe** |
| *`B0 mode`, temoin* | 2 058 | *0,5216* | *moins 0,00025* | *[-0,0005 ; -0,0001]* | *moins 0,001* | *moins 0,001* | *moins 0,001* | *moins 0,001* | *temoin* |
| *`B0 tirage`, temoin* | 2 058 | *0,4430* | *moins 0,00028* | *[-0,0024 ; 0,0020]* | *moins 0,001* | *moins 0,002* | *moins 0,002* | *moins 0,001* | *temoin* |

Les deux lignes en italique en tete sont celles dont le controle de masque echoue.

**Cinq lectures.**

1. **Le controle passe et il passe partout.** Les deux temoins aveugles a la personne
   perdent entre 0,048 et 0,097 pour cent de leur exactitude, en negatif, sous les quatre
   segmentations. L'IC de `B0 tirage` contient zero. La mesure ne fabrique rien.
2. **Le plancher humain de Twin est plus haut que celui du GSS**, 45,6 pour cent de chute
   relative contre 34,7. Et **la reassignation optimale ne gagne rien chez les humains de
   Twin non plus**, rapport **1,0005** sous `S_gra` et 1,0008 sous `S_ideo` : le controle qui
   leve la reserve du preenregistrement de `a44` sur le sur ajustement de l'appariement
   hongrois se reproduit a l'identique sur un autre jeu.
3. **Les seuils declares avant calcul ne separent pas les treize configurations, et il faut
   l'ecrire.** « Gabarit » sous 0,15, « porteur de personne » au dessus de 0,40 : les treize
   sont au dessus de 0,40. Le classement de `a44` section 7.2 avait quatre gabarits sur
   douze ; ici il n'y en a aucun parmi les agents. **Le seuil n'est pas mauvais, c'est le jeu
   qui est different** : aucune configuration de Twin ne recoit d'etiquette ideologique en
   clair, selon la lecture de `i3b` section 4.4.
4. **Les trois gabarits sont les trois predicteurs statistiques.** C'est l'inverse du GSS, ou
   `PMM k=10` etait a 62,5 pour cent du plancher, devant `C3`, et ou seuls `B1` et
   `B3 foret` etaient du cote du gabarit. La raison est de plan et non de methode : sur le
   GSS les predicteurs recoivent 119 items de contexte de la **meme** passation que la cible,
   sur Twin ils recoivent des items d'une vague **anterieure**, et la cible est une vague
   posterieure de plusieurs semaines. **Comparer `PMM` du GSS a `PMM` de Twin est une faute
   de plan, et le rapport ne la commet pas.**
5. **Les quatre variantes de `Text Persona` en GPT-4.1-mini, qui ne different que par la
   temperature, le raisonnement et la repetition des questions, s'etalent de 0,614 a 0,655**,
   un facteur 1,07, et le passage a Gemini-Flash-2.5 sur la meme invite donne 0,698. **Le
   reglage compte, mais beaucoup moins que sur la detectabilite de `i3b`**, ou les memes
   quatre variantes s'etalaient de 6,1 a 12,9 pour cent de contamination, un facteur 2,1.

---

## 5. Tableau 2 : la reassignation optimale et son plancher

[MESURE, `t1-reassignation.csv`, `S_ideo`, appariement hongrois intra segment]

`a47` E4 interdit de publier le rapport `(hongrois moins permutee) / (vraie moins permutee)`
sans son plancher, parce qu'il explose quand le denominateur tend vers zero. Le plancher est
le **gain hongrois absolu d'une population sans aucun signal individuel**, `B0 tirage`.

| condition | gain hongrois absolu | plancher `B0 tirage` | au dessus | chute | rapport publie |
|---|---|---|---|---|---|
| *`B0 mode`, temoin* | *0,0045* | *0,1423* | *non* | *moins 0,0003* | *moins 16,9* |
| **`B2 argmax`** | **0,1309** | 0,1423 | **non** | 0,0282 | **4,64** |
| *`B0 tirage`, plancher* | *0,1423* | *0,1423* | *reference* | *moins 0,0004* | *moins 330* |
| **`B1 argmax`** | **0,1440** | 0,1423 | oui, de 1,2 pour cent | 0,0197 | **7,31** |
| **`PMM k=10`** | **0,1561** | 0,1423 | oui, de 9,7 pour cent | 0,0273 | **5,72** |
| `JSON PredOut mini` | 0,1538 | 0,1423 | oui | 0,1280 | 1,20 |
| `Finetuning 500` | 0,1548 | 0,1423 | oui | 0,0881 | 1,76 |
| `Demographics Only` | 0,1592 | 0,1423 | oui | 0,1259 | 1,26 |
| `Text Persona - GPT4.1-mini` | 0,1668 | 0,1423 | oui | 0,1490 | 1,12 |
| `Text Persona - Gemini` | 0,1823 | 0,1423 | oui | 0,1650 | 1,11 |
| `JSON Persona - GPT4.1` | 0,1914 | 0,1423 | oui | 0,1774 | 1,08 |
| **humains vagues 1-3** | **0,3256** | 0,1423 | oui, de 129 pour cent | 0,3253 | **1,001** |

**Le piege de `a47` E4 se reproduit sur Twin, et il frappe cette fois les predicteurs
statistiques.** `B1 argmax` a un rapport publie de **7,31**, plus eleve que le 4,91 de
`agents v8` sur le GSS, et son gain hongrois absolu, 0,1440, est a **1,2 pour cent** de
celui d'une population sans aucune structure individuelle. `B2 argmax`, rapport 4,64, est
**en dessous** du plancher. **Le rapport de reassignation ne mesure pas que la vraie
assignation est arbitraire ; il mesure que le denominateur est petit.** Il ne doit jamais
etre publie seul, et le gain absolu doit l'accompagner, sur ce jeu comme sur le GSS.

**Les deux criteres concordent tout de meme.** Les treize configurations ont un rapport
entre 1,03 et 1,76 et un gain absolu de 8 a 35 pour cent au dessus du plancher ; les trois
predicteurs statistiques ont un rapport entre 3,8 et 7,3 et un gain absolu a moins de 10
pour cent du plancher. **Le depart est le meme que sur le GSS, il tombe simplement sur
d'autres conditions.**

---

## 6. Tableau 3 : le generateur nul, et la double distorsion de `a6`

[MESURE, `t1-generateur-nul.csv`, axe ideologie, entropie de Miller Madow, 200 replicats,
IC de `d` par sous echantillonnage pivote avec le nul retire dans chaque sous echantillon]

### 6.1 Le ratio inter

| condition | mesure | son nul | bande du nul | part reproduite | `d` | IC de `d` | `z` |
|---|---|---|---|---|---|---|---|
| humains vagues 1-3 | 0,950 | 1,208 | [1,150 ; 1,261] | **127,1 %** | -0,258 | [-0,334 ; -0,196] | -8,6 |
| `Finetuning 500` | 1,360 | 1,541 | [1,456 ; 1,631] | **113,3 %** | -0,180 | [-0,248 ; -0,119] | -4,0 |
| **`Demographics Only`** | **1,867** | **1,981** | **[1,910 ; 2,049]** | **106,1 %** | -0,113 | [-0,148 ; -0,079] | -3,2 |
| `Summary + JSON` | 2,451 | 2,621 | [2,535 ; 2,692] | 106,9 % | -0,170 | [-0,212 ; -0,125] | -4,3 |
| `Persona Summary` | 2,891 | 3,027 | [2,953 ; 3,108] | 104,7 % | -0,135 | [-0,176 ; -0,101] | -3,4 |
| `JSON PredOut mini` | 3,293 | 3,406 | [3,337 ; 3,483] | 103,5 % | -0,114 | [-0,151 ; -0,084] | -3,0 |
| `JSON Persona mini` | 3,781 | 4,075 | [3,950 ; 4,218] | 107,8 % | -0,294 | [-0,383 ; -0,188] | -4,4 |
| `Text Persona Gemini` | 4,158 | 4,367 | [4,290 ; 4,436] | 105,0 % | -0,210 | [-0,261 ; -0,159] | -5,6 |
| `Text raisonnement` | 4,173 | 4,322 | [4,226 ; 4,407] | 103,6 % | -0,149 | [-0,186 ; -0,112] | -3,3 |
| `Text temp. defaut` | 4,425 | 4,575 | [4,491 ; 4,668] | 103,4 % | -0,150 | [-0,188 ; -0,112] | -3,2 |
| `Text repetition` | 4,716 | 4,871 | [4,786 ; 4,960] | 103,3 % | -0,156 | [-0,203 ; -0,113] | -3,3 |
| **`Text Persona mini`** | **4,981** | **5,100** | **[5,009 ; 5,196]** | **102,4 %** | -0,119 | [-0,158 ; -0,078] | -2,4 |
| `JSON Persona - GPT4.1` | 5,153 | 5,309 | [5,210 ; 5,402] | 103,0 % | -0,156 | [-0,200 ; -0,115] | -2,9 |
| `JSON PredOut 4.1` | 5,334 | 5,461 | [5,378 ; 5,559] | 102,4 % | -0,127 | [-0,167 ; -0,094] | -2,6 |
| `B1 argmax` | 3,885 | 4,015 | [3,949 ; 4,097] | 103,3 % | -0,130 | [-0,169 ; -0,102] | -3,7 |
| `B2 argmax` | 0,317 | 0,410 | [0,379 ; 0,439] | 129,5 % | -0,093 | [-0,116 ; -0,073] | -5,6 |
| `PMM k=10` | 0,916 | 1,046 | [1,004 ; 1,091] | 114,2 % | -0,130 | [-0,161 ; -0,099] | -5,9 |
| *`B0 mode`, temoin* | *0,0003* | *0,0015* | *[-0,0002 ; 0,0041]* | *sans objet* | *-0,0012* | *[-0,0026 ; 0,0001]* | *-1,1* |
| *`B0 tirage`, temoin* | *0,0017* | *0,1454* | *[0,127 ; 0,167]* | *sans objet* | *-0,144* | *[-0,173 ; -0,114]* | *-13,9* |

### 6.2 Le ratio intra

| condition | mesure | son nul | part reproduite | `d` | `z` |
|---|---|---|---|---|---|
| `JSON PredOut mini` | 0,4184 | 0,4153 | **99,27 %** | 0,0031 | 2,4 |
| `Demographics Only` | 0,4852 | 0,4825 | **99,43 %** | 0,0028 | 2,2 |
| `Text Persona mini` | 0,5017 | 0,4986 | **99,37 %** | 0,0031 | 2,3 |
| `Finetuning 500` | 0,5413 | 0,5367 | **99,14 %** | 0,0046 | 2,6 |
| `Persona Summary` | 0,5564 | 0,5531 | **99,40 %** | 0,0033 | 2,7 |
| `JSON Persona mini` | 0,5661 | 0,5598 | **98,90 %** | 0,0063 | 3,6 |
| `JSON Persona - GPT4.1` | 0,5747 | 0,5707 | **99,31 %** | 0,0039 | 2,8 |
| `Text Persona Gemini` | 0,7062 | 0,7010 | **99,26 %** | 0,0052 | 3,6 |
| `B1 argmax` | 0,7030 | 0,6999 | 99,55 % | 0,0031 | 2,3 |
| `PMM k=10` | 0,9001 | 0,8969 | 99,65 % | 0,0032 | 3,1 |
| **humains vagues 1-3** | **1,0101** | **1,0039** | **99,38 %** | 0,0062 | 4,4 |
| *`B0 mode`, temoin* | *0,0163* | *0,0162* | *99,85 %* | *0,0000* | *0,1* |

**Quatre lectures.**

1. **Le nul reproduit tout le monde, et il sur reproduit systematiquement.** La part
   reproduite du ratio inter vaut 102,4 a 106,9 pour cent pour les treize configurations,
   113 a 130 pour cent pour les conditions dont le ratio est petit, et 127 pour cent pour le
   retest humain. **Le `d` est un montant additif a peu pres constant**, moins 0,11 a moins
   0,29, exactement comme sur le GSS : `p_chapeau` est estime sur le segment puis retire dans
   le meme segment, ce qui ajoute une couche de bruit multinomial que le terme inter compte.
   **La part reproduite ne doit donc pas etre lue comme un classement de proximite.**
2. **Contrairement au GSS, aucun IC de `d` ne contient zero.** `a44` avait onze intervalles
   sur onze contenant zero sur 1 052 personnes ; ici les dix sept sont a `z` de moins 2,4 a
   moins 5,9. La difference vient de l'intervalle et non du fait : `a44` employait un
   bootstrap avec remise dont la limite 8 dit qu'il n'est pas centre, t1 emploie un sous
   echantillonnage pivote qui retire le nul dans chaque sous echantillon. **La conclusion ne
   change pas d'un iota : un ecart de 2 a 7 pour cent sur un ratio de 5 reste un ecart de
   2 a 7 pour cent.**
3. **Le ratio intra est reproduit a 98,9 a 99,7 pour cent pour les dix neuf conditions sans
   exception**, exactement comme les 99,3 pour cent du GSS. **L'ecrasement de dispersion
   interne de `a6` est une quantite de gabarit sur Twin comme sur le GSS.**
4. **La lecture secondaire sur les six axes agreges, avec un nul qui ne connait que
   l'ideologie, est declaree d'avance comme une borne inferieure, et elle se comporte comme
   telle** [MESURE, `t1-generateur-nul-six-axes.csv`, 50 replicats] : la part reproduite vaut
   86 a 99 pour cent pour les treize configurations, mais seulement **48 a 49 pour cent pour
   `B1 argmax` et `B2 argmax`**, dont la structure vit sur les axes que ce nul detruit. Le
   ratio intra, lui, est reproduit a 100 pour cent meme sur les six axes.

**Conclusion de la section, ecrite telle quelle : les deux ratios que `a6` publie sur Twin
sont des fonctionnelles de la table de contingence (segment, modalite), exactement
invariants sous permutation des personnes intra segment, et reproduits a 2 a 7 pour cent
pres sur l'inter et a moins de 1,1 pour cent pres sur l'intra par un generateur qui ne sait
rien de la personne. Le critere de Yuan s'applique mot pour mot sur ce jeu aussi.**

---

## 7. Tableau 4 : la chute et l'exactitude brute, et la version partialisee

[MESURE, `t1-correlation-chute-exactitude.csv` et `t1-correlation-residus.csv`]

### 7.1 La correlation brute

| jeu | perimetre | segmentation | Pearson | Spearman | variance partagee |
|---|---|---|---|---|---|
| **GSS**, `a47` | 13 conditions, humains vague 2 comprise | `S_ideo` | **0,906** | 0,874 | **82 %** |
| **GSS**, recalcul a perimetre apparie | 12 conditions, aucun humain, aucun temoin | `S_ideo` | **0,804** | 0,804 | **65 %** |
| **GSS**, idem | idem | `S_gra` | 0,828 | 0,797 | 69 % |
| **Twin**, t1 | **16 conditions de la famille primaire** | `S_ideo` | **0,512** | 0,803 | **26 %** |
| **Twin**, t1 | idem | `S_gra` | **0,529** | 0,791 | **28 %** |
| **Twin**, t1 | 17, plancher humain compris | `S_gra` | 0,769 | 0,826 | 59 % |
| **Twin**, t1 | 19, temoins compris | `S_gra` | 0,757 | 0,816 | 57 % |

**A perimetre apparie, la variance partagee tombe de 65 a 69 pour cent sur le GSS a 26 a 28
pour cent sur Twin.** L'objection 1.3 de `a45` reste vraie sur le GSS et **ne se transporte
pas**. Sur Twin, la chute apporte quelque chose que l'exactitude ne voit pas. La correlation
de rang reste haute, 0,79 a 0,80, donc **le classement des conditions est en grande partie
celui de l'exactitude ; ce sont les ecarts au classement qui portent l'information**, et
c'est exactement ce que la version partialisee mesure.

### 7.2 La version partialisee, proposee au preenregistrement et calculee

Regression lineaire de la chute sur l'exactitude a travers les seize conditions de la
famille, sous `S_gra`, puis residus [MESURE] :

| condition | exactitude | chute | chute predite par l'exactitude | **residu** |
|---|---|---|---|---|
| **`B2 argmax`** | 0,5305 | 0,0282 | 0,1322 | **moins 0,1041** |
| **`B1 argmax`** | 0,5183 | 0,0240 | 0,1224 | **moins 0,0984** |
| **`PMM k=10`** | 0,4910 | 0,0305 | 0,1002 | **moins 0,0697** |
| `Text Persona - GPT4.1-mini` | 0,5530 | 0,1573 | 0,1505 | plus 0,0068 |
| `Text temp. defaut` | 0,5478 | 0,1533 | 0,1463 | plus 0,0071 |
| `Finetuning 500` | 0,4619 | 0,0881 | 0,0767 | plus 0,0114 |
| `Text repetition` | 0,5489 | 0,1594 | 0,1472 | plus 0,0122 |
| `JSON Persona - GPT4.1` | 0,5738 | 0,1853 | 0,1674 | plus 0,0179 |
| `Demographics Only` | 0,4996 | 0,1267 | 0,1072 | plus 0,0195 |
| `Text raisonnement` | 0,5435 | 0,1625 | 0,1428 | plus 0,0197 |
| `JSON Persona mini` | 0,5439 | 0,1639 | 0,1431 | plus 0,0208 |
| `JSON PredOut 4.1` | 0,5646 | 0,1822 | 0,1600 | plus 0,0222 |
| `Persona Summary` | 0,5209 | 0,1473 | 0,1245 | plus 0,0228 |
| `Text Persona Gemini` | 0,5505 | 0,1752 | 0,1485 | plus 0,0267 |
| `Summary + JSON` | 0,4742 | 0,1154 | 0,0866 | plus 0,0287 |
| `JSON PredOut mini` | 0,4625 | 0,1335 | 0,0771 | **plus 0,0564** |

**La partialisation separe mieux que la brute et elle separe parfaitement : les trois
predicteurs statistiques sont les trois seuls residus negatifs, et les treize configurations
sont les treize seuls residus positifs.** Le plus gros residu positif, `JSON Persona
(Predicted Output) - GPT4.1-mini`, plus 0,056, est aussi la configuration a l'exactitude la
plus faible du bloc : elle porte beaucoup plus de personne que son exactitude ne le laisse
croire. **C'est la version de la mesure que le rapport recommande de publier quand la
correlation avec l'exactitude est haute**, et elle est utile meme quand elle ne l'est pas.

---

## 8. Le verdict preenregistre

[MESURE, `t1-holm-contre-b0.csv`, 2 000 sous echantillons, ecart E3]

Test declare : « la chute de la condition est superieure a celle du temoin `B0 tirage` sur
le meme perimetre », sous `S_gra`, difference calculee sur le meme sous echantillon donc
appariee, **Holm sur seize**.

**Les seize conditions passent, `p` de Holm 0,008 pour les seize, et la part des sous
echantillons ou la difference est positive vaut 1,000 pour les seize.** Les differences
moyennes vont de **0,0238** pour `B1 argmax` a **0,1822** pour `JSON Persona - GPT4.1`, avec
des intervalles a 95 pour cent larges de deux a six millemes.

**Ce verdict separe moins que le classement descriptif**, puisque tout le monde le passe. Sa
valeur est negative et elle est reelle : **elle etablit que meme les trois predicteurs
statistiques portent une quantite non nulle de personne**, ce que le classement par seuil,
qui les range en « gabarit de groupe », ne dit pas. Un gabarit au sens operationnel n'est pas
un objet a chute nulle, c'est un objet a chute petite ; les temoins `B0` sont les seuls a
chute nulle.

**La lecon de methode, et elle est genante.** Le preenregistrement fixait `S = 200`, ce qui
plafonnait `p` a 0,005 et rendait Holm sur seize inatteignable a 0,05. **Le verdict etait
impossible avant d'etre calcule, et il a fallu un second run pour le rendre possible.** Un
preenregistrement doit fixer la resolution de son test, pas seulement son seuil.

---

## 9. Le placebo d'etiquette, hors preenregistrement, et ce qu'il tranche

[MESURE, `t1-placebo-etiquette.csv`, `analyses/t1_placebo.py`, **ecart E1, post hoc**]

`a47` E2 montre sur le GSS que la chute change d'un facteur 2,6 a 3,7 selon que le segment
contient ou non l'ideologie, et **seulement** pour `agents v8` et `C2`, les deux conditions
qui recoivent l'etiquette ideologique en clair. La lecture causale proposee est : permuter a
l'interieur de la variable que la condition a recue mesure ce qu'elle sait **au dela** de ce
qu'on vient de fixer, donc rabote sa chute. **Cette lecture n'avait aucune ablation pour la
soutenir, `a44` E1 le dit explicitement.**

Sur Twin, aucune configuration d'agent ne recoit d'etiquette ideologique explicite selon la
lecture de `i3b` 4.4 [PROBABLE, lecture d'un rapport, non verifiee sur `data/`]. Mais
`B1 argmax` de t1, lui, recoit les quatorze questions du bloc Demographics, dont `QID22`
opinions politiques et `QID20` parti. **Son entree est ecrite dans `t1_baselines.py`, elle
est donc entierement controlee.** L'ablation retire ces deux colonnes et rien d'autre : meme
moteur, memes plis, meme graine, meme protocole.

| version | exactitude | part du plancher, `S_ideo` | part, `S_gra` | part, `S_parti` | **facteur `S_gra / S_ideo`** |
|---|---|---|---|---|---|
| `B1 argmax`, **quatorze** demographies | 0,5183 | **0,0835** | 0,1012 | 0,1123 | **1,212** |
| `B1 argmax`, **sans ideologie ni parti** | 0,5134 | **0,0942** | 0,0542 | 0,1009 | **0,575** |

**La prediction ecrite en tete de `t1_placebo.py` avant son execution etait : le facteur doit
baisser et la chute sous `S_ideo` doit monter. Les deux sont arrivees.** La chute sous
l'ideologie **monte** de 12,8 pour cent alors que le modele est **plus pauvre**, son
exactitude baissant de 0,0049. Le facteur passe de 1,212 a 0,575, un facteur 2,1 vers le bas.

**Ce que cela autorise a dire** [MESURE] : la sensibilite de la chute a la segmentation est
causee par le **recouvrement entre la variable de segmentation et l'entree de la condition**,
et non par une propriete du jeu de donnees ni par la finesse du segment. **La lecture causale
de `a47` E2 est correcte, et elle est maintenant appuyee par une ablation propre.**

**Ce que cela n'autorise pas a dire.** L'ablation retire deux colonnes en meme temps,
l'ideologie et le parti, et elle change donc a la fois le recouvrement avec le segment et
l'information totale du modele. **La quantite diagnostique est le rapport entre
segmentations, concu pour annuler le niveau general**, et c'est lui qui bouge d'un facteur
2,1 ; les deux chutes prises separement melangent les deux effets. Sous `S_parti`, qui
contient l'autre variable retiree, le facteur bouge peu, 0,1123 contre 0,1009, ce que le
rapport ne sait pas expliquer.

---

## 10. La coherence avec `i3b`, et l'exactitude comme rivale

[MESURE, `t1-coherence-i3b.csv` et `t1-classement.csv` ; `i3b-twin-sources-pures.csv` et
`i3b-twin-abaque.csv` sont **lus, jamais recalcules**]

Correlations de rang sur les treize configurations :

| paire | `S_ideo` | `S_fin` | `S_gra` | `S_parti` |
|---|---|---|---|---|
| part du plancher humain contre `tau*` de `i3b`, Holm(39), N = 2 058 | **0,528** | 0,571 | **0,582** | 0,571 |
| part du plancher humain contre `A`, deficit de patrons de `i3b` | **0,028** | 0,050 | **0,055** | 0,050 |
| part du plancher humain contre exactitude brute | 0,687 | 0,725 | **0,758** | 0,725 |
| exactitude brute contre `tau*` de `i3b` | 0,577 | 0,577 | **0,577** | 0,577 |

**Trois faits.**

1. **La prediction P8 est tenue de justesse.** Plus une configuration porte la personne, plus
   il faut la contaminer pour que le detecteur de `i3` la signale, Spearman 0,53 a 0,58.
   C'est un lien reel et modeste. **Mais l'exactitude brute predit `tau*` presque aussi bien,
   0,577.** La mesure de personne n'apporte, sur cette question, qu'un tres petit supplement
   a une quantite gratuite.
2. **Le deficit de patrons `A` de `i3b` et la mesure de personne sont orthogonaux**,
   Spearman 0,03 a 0,06. Ce sont deux choses differentes, et c'est le meilleur argument
   mesure pour les publier ensemble. `LLM Finetuning (500 exemples)` en est l'illustration
   extreme : **le generateur le plus degenere de tout le dossier sur `A`, moins 79,3 pour
   cent, detecte a 0,43 pour cent de contamination, est du cote du porteur de personne sur la
   mesure de t1, 42 pour cent du plancher humain.** Une population peut etre a la fois
   pauvre en combinaisons et fidele aux personnes.
3. **La prediction P7 tombe pour cette raison**, et c'est l'echec le plus instructif du lot :
   « degenere » au sens du deficit de patrons et « gabarit » au sens de la permutation ne
   sont pas la meme chose, et le preenregistrement les confondait.

---

## 11. GSS contre Twin : ce qui se transporte

[MESURE, `t1-gss-contre-twin.csv` ; les chiffres du GSS sont **lus** dans
`a47-chute-deux-segmentations.csv`, rien n'est recalcule]

### 11.1 Les conditions analogues

| famille | GSS | part du plancher, `S_gra` | Twin | part du plancher, `S_gra` | transport |
|---|---|---|---|---|---|
| **demographies seules** | `agents demographiques (v6)` | **0,236** | `Demographics Only - GPT4.1-mini` | **0,556** | **non**, facteur 2,4 |
| **etiquette ideologique seule** | `agents v8` | 0,267 | *aucun equivalent* | *sans objet* | *non testable* |
| **persona complete** | `agents composite` | **0,696** | `JSON Persona - GPT4.1` | **0,708** | **oui, au chiffre** |
| **persona complete** | `agents entretien (v3)` | 0,613 | `Text Persona - Gemini` | 0,698 | oui, ordre de grandeur |
| **persona complete** | `agents enquete` | 0,618 | `Text Persona - GPT4.1-mini` | 0,623 | **oui, au chiffre** |
| **imputation statistique** | `PMM k=10` | **0,625** | `PMM k=10` | **0,136** | **non**, facteur 4,6 |
| **regression sur demographies** | `B1 argmax` | 0,228 | `B1 argmax` | 0,101 | non, facteur 2,3 |
| **plus proches voisins** | `B2 argmax` | 0,424 | `B2 argmax` | 0,116 | non, facteur 3,7 |
| **plancher humain, chute relative** | humains vague 2 | 34,7 % | humains vagues 1-3 | 45,6 % | ordre de grandeur |

**Ce qui se transporte, ce sont les personas completes**, a un ou deux points pres, sur
d'autres personnes, d'autres items, d'autres auteurs et d'autres modeles. C'est le resultat
le plus reutilisable du rapport [MESURE].

**Ce qui ne se transporte pas a deux causes distinctes, et il faut les separer.**

- **Les predicteurs statistiques chutent d'un facteur 2,3 a 4,6 sur Twin, et c'est un effet
  de plan et non de methode.** Sur le GSS, `PMM` et `B2` recoivent 119 items de contexte de
  la **meme** passation que la cible ; sur Twin ils recoivent des items d'une vague
  **anterieure** et la cible est posee des semaines plus tard. Le contexte de Twin est plus
  loin de sa cible. **Toute comparaison directe des lignes statistiques entre les deux jeux
  est une faute de plan.**
- **`Demographics Only` de Twin porte deux fois plus de personne que `agents v6` du GSS.**
  Le rapport ne sait pas si la cause est le contenu de l'invite, les demographies de Twin
  etant peut etre plus riches que les onze attributs de Stanford, ou le modele,
  GPT-4.1-mini contre les modeles de Stanford, ou le questionnaire, des items de
  psychologie experimentale contre des attitudes politiques. **Les trois sont confondues et
  aucune n'est isolable dans ce dossier.**

### 11.2 La sensibilite a la segmentation, les deux jeux cote a cote

Facteur `part sous S_gra / part sous S_ideo` [MESURE] :

| jeu | conditions dont l'entree contient l'ideologie nommee | facteur | autres conditions | facteur |
|---|---|---|---|---|
| **GSS** | `agents v8`, `C2` | **3,72 et 2,56** | les quinze autres | 0,96 a 1,45 |
| **Twin** | `B1 argmax`, qui recoit `QID22` et `QID20` | **1,21** | les treize configurations | **1,006 a 1,064** |
| **Twin, ablation** | `B1 argmax` sans les deux colonnes politiques | **0,58** | | |

**La reponse a `a45` point 10 est donc : le chiffre ne depend pas du jeu, il depend de ce que
la condition a recu.** Sur le GSS, `a47` E2 avait raison de retirer la formule « des gabarits
de groupe a 93 pour cent interchangeables », qui etait le complement a 1 du seul chiffre
`S_ideo` ; mais la generalisation « le chiffre est fragile » est fausse. **Le chiffre est
stable partout ou le segment ne recouvre pas l'entree, et il ne bouge que la ou il recouvre.**

---

## 12. La figure

`resultats/t1-figure-personne-twin.png` et `.svg`. Trois panneaux, memes conditions dans le
meme ordre sur les deux premiers, ordre croissant de la part du plancher humain sous `S_gra`.

**Panneau A.** La chute en part du plancher humain, deux points par condition : le cercle est
`S_ideo`, le point plein est `S_gra`. **Les traits sont courts pour les dix neuf
conditions** : c'est le resultat P4 sous sa forme la plus directe, et il faut le lire a cote
du panneau C, qui montre les memes traits sur le GSS.

**Panneau B.** Le ratio inter sur l'axe ideologie, echelle logarithmique, valeur mesuree
contre valeur du generateur nul, avec la bande des 200 replicats. **Les traits sont courts
partout** : le nul tombe sur la mesure. Les deux temoins `B0` en sont retires, leur ratio
vrai etant nul par construction.

**Panneau C.** Le facteur de changement de la chute quand on retire l'ideologie du segment,
les deux jeux l'un au dessus de l'autre. **Deux points seulement sortent, `agents v8` a 3,72
et `C2` a 2,56, et ce sont les deux conditions du dossier qui recoivent l'etiquette
ideologique en clair.**

**Ce que la figure ne montre pas et qu'il faut lire au tableau 4** : la version partialisee,
qui est la seule quantite du rapport qui separe les treize configurations des trois
predicteurs statistiques sans exception.

---

## 13. Ce que cela change a `MODELE-DU-MONDE.md` section 10

### 13.1 Le verrou 3 de la section 10.5 est ferme sur sa moitie Twin

Il demandait : « passer a28 test 3, a29 et a33 au generateur nul, faire de la chute sous
permutation une quantite de verdict preenregistree, et la rejouer sur Twin ; zero appel ».
**Les deux dernieres sont faites, la premiere ne l'est pas.** La chute est desormais une
quantite de verdict preenregistree, avec sa famille, sa correction de Holm et son
comparateur ; et elle est rejouee sur Twin.

### 13.2 La question ouverte de la fin de la section 10 recoit sa reponse

Le texte dit : « ce que je ne sais plus, ou pas encore : [...] si la chute sous permutation,
mesure preenregistree mais classement post hoc, tiendra ses seuils sur Twin ».

**Reponse : elle ne les tient pas, et la raison est instructive.** Les seuils de 0,15 et 0,40
du plancher humain, redeclares avant calcul ici, rangent **les treize configurations de Twin
du cote du porteur de personne et les trois predicteurs statistiques du cote du gabarit**.
Sur le GSS ils rangeaient quatre conditions sur douze en gabarit. **Ce ne sont pas les seuils
qui echouent, c'est le jeu qui ne contient pas la condition qui produit le gabarit** : aucune
configuration de Twin ne recoit l'etiquette ideologique en clair. Le seuil doit donc etre
publie comme un seuil **relatif au plancher humain du jeu**, ce qu'il est deja, et jamais
comme une constante d'audit, ce que `i3b` 11.1 dit deja des constantes de `i3`.

### 13.3 Ce que la section 10.3 peut ecrire en plus, et ce qu'elle doit corriger

**En plus** [MESURE] :

1. « Les deux ratios sont des quantites de gabarit **sur les deux jeux**. Sur Twin, un
   generateur qui tire chaque reponse independamment dans la marginale de son segment
   reproduit le ratio inter des treize configurations a 102 a 107 pour cent et le ratio intra
   a 99 pour cent. L'invariance exacte sous permutation intra segment est `0,000e+00` sur dix
   neuf conditions et quatre segmentations. »
2. « Le controle humain de l'appariement hongrois se reproduit : rapport 1,0005 sur les
   2 058 personnes de Twin reinterrogees, contre 1,001 sur le GSS. »
3. « Le rapport de reassignation n'a de sens qu'a cote de son gain absolu : sur Twin il vaut
   **7,31 pour `B1 argmax`**, dont le gain absolu est a 1,2 pour cent d'une population sans
   structure, et **4,64 pour `B2 argmax`**, dont le gain absolu est **en dessous** de cette
   population. » C'est la generalisation de `a47` E4.

**A corriger** :

1. La phrase de 10.3 « c'est le conditionnement, pas le langage » reste vraie mais elle doit
   cesser d'etre illustree par « la foret et la regression sur demographies sont du cote du
   gabarit ». **Sur Twin, la regression, les voisins et l'appariement sur moyenne predite sont
   tous les trois du cote du gabarit, et les treize configurations a modele de langage sont
   toutes du cote de la personne.** La phrase juste est : **c'est le recouvrement entre ce
   que la condition recoit et ce que la permutation fixe, et le contexte que la condition
   recoit.**
2. La phrase de 10.4 « les mesures de gonflement [...] doivent etre publiees a cote de la
   chute sous permutation et du plancher humain, jamais seules » gagne un jeu de plus et
   n'appelle aucune retouche.
3. **L'affirmation implicite que la chute sous permutation est presque redondante avec
   l'exactitude, qui vient de `a45` 1.3, doit etre indexee sur le jeu.** Elle est vraie sur
   le GSS, 65 a 82 pour cent de variance partagee, et **fausse sur Twin, 26 a 28 pour cent a
   perimetre apparie**. La version partialisee, residus de la chute apres regression sur
   l'exactitude, doit devenir la forme publiee par defaut : elle separe parfaitement sur
   Twin et elle ne coute rien.

### 13.4 Le verrou 2, le placebo d'etiquette, est entame

`MODELE-DU-MONDE.md` 10.5 verrou 2 dit : « le placebo d'etiquette et le test d'ordre de Yuan
sur C2 et C3 [...] a44 fournit le nul, pas le placebo ». **t1 fournit un placebo, sur
`B1 argmax` de Twin plutot que sur C2** : meme moteur, meme run, memes plis, deux colonnes
retirees. Il confirme la lecture causale de `a47` E2. Il ne remplace pas le placebo sur un
agent, qui reste a faire, et il ne dit rien du test d'ordre de Yuan.

### 13.5 Le verrou 8, le deficit de combinaison sur Twin, n'est pas ferme

`i3b` l'a mesure sur Twin, statistique `A`, moins 8 a moins 79 pour cent selon la
configuration. **t1 ajoute seulement qu'il est orthogonal a la mesure de personne**, Spearman
0,03 a 0,06. Le deficit de combinaison reste un resultat a part, et c'est desormais mesure et
non suppose.

---

## 14. Ce que je n'ai pas pu verifier

1. **Ce que contient reellement l'invite de `Demographics Only - GPT4.1-mini`.** Le paquet
   telecharge dans `data/twin2k500` contient les reponses des configurations et le texte des
   personas, pas les invites systeme par configuration. **Je ne peux donc pas verifier si
   cette condition recoit `QID22`, l'ideologie politique.** Toute la lecture de la section 11
   repose sur la phrase de `i3b` 4.4, « Twin ne contient aucune configuration qui recoive une
   etiquette ideologique explicite », que je prends pour exacte sans l'avoir verifiee
   [PROBABLE]. Si elle est fausse, la prediction P4 reste tenue en mesure mais son
   explication tombe.
2. **La perturbation d'ordre des items de Yuan.** Elle demande des appels de modele et n'a
   pas ete faite, pas plus qu'en `a44`.
3. **Le deficit de patrons et l'exces de correlation ne sont pas recalcules ici.** Les valeurs
   `A` et `B` employees en section 10 sont lues dans `i3b-twin-sources-pures.csv`. Je n'ai
   donc pas de controle croise sur elles.
4. **`PMM k=10` de Twin n'est pas `PMM k=10` du GSS.** La recette de tirage est la meme, le
   plan ne l'est pas : contexte de la meme vague sur le GSS, contexte d'une vague anterieure
   sur Twin. **Les deux lignes ne se comparent pas et le rapport le dit trois fois.**
5. **L'ablation de la section 9 retire deux colonnes en meme temps.** Une ablation qui ne
   retirerait que `QID22` n'a pas ete construite ; elle coute quinze secondes et elle
   trancherait la ligne `S_parti` que je ne sais pas expliquer.
6. **La resolution du test de verdict a du etre changee apres le premier run**, ecart E3. Le
   fait que la correction ait ete faite dans le sens qui rend le verdict atteignable est
   declare, et un relecteur a le droit de le trouver suspect. Ce qui le limite : les seize
   `p` bruts sont **tous** au plancher de leur resolution dans les deux runs, avec
   100 pour cent des sous echantillons du meme signe ; aucune ligne ne change de cote.
7. **Aucun calcul de puissance des non rejets.** Il n'y a pas de non rejet dans ce rapport, ce
   qui rend le point moins grave qu'en `a44`, mais l'affirmation « les seuils ne separent
   rien sur Twin » est une affirmation d'absence et elle n'est pas bornee.
8. **Les intervalles du generateur nul ne portent pas l'incertitude du plancher humain.** Le
   denominateur des ratios, le retest de la vague 4, est traite comme fixe dans chaque sous
   echantillon alors qu'il y est aussi reestime ; l'effet est du second ordre et il n'est pas
   chiffre.
9. **La ligne `JSON Persona - GPT4.1-mini` sous `S_gra` a 32,96 pour cent de repli du nul.**
   Elle n'est pas lue pour le generateur nul, qui ne tourne que sous `S_ideo`, mais sa chute
   sous `S_gra`, 0,676 du plancher, est publiee. La permutation n'emploie pas le nul, donc
   elle est valide ; c'est une precision de lecture, comme `a44` E7.
10. **Rien de nouveau sur le GSS.** Aucun chiffre du GSS n'est recalcule ici ; ils sont lus
    dans `a47-chute-deux-segmentations.csv` et `a47-correlation-chute-exactitude.csv`. Le seul
    calcul nouveau cote GSS est la correlation a perimetre apparie de la section 7.1, faite
    sur le fichier de `a47` sans le regenerer.
11. **Le sous echantillonnage pivote n'est pas valide ici.** `i3b` publie un controle de
    validite de la mise a l'echelle sur ses trois statistiques ; t1 ne le refait pas sur la
    chute. La mise a l'echelle en `racine(m / N)` avec correction de population finie est
    supposee, pas verifiee.
12. **L'horodatage du preenregistrement repose sur un repertoire synchronise par iCloud**,
    limite deja ecrite par `a45` point 11. Aucun depot tiers.

---

## 15. Questions ouvertes pour Simon

1. **La question qui commande le reste : que fait on d'un jeu ou aucune configuration n'est un
   gabarit ?** Twin contient treize pipelines produits par une equipe qui cherchait la
   fidelite individuelle, et les treize portent la personne au sens de notre mesure, 42 a 71
   pour cent du plancher humain. Le GSS contient deux conditions a etiquette seule qui sont
   des gabarits a 7 pour cent. **Trois lectures possibles.** (a) Le gabarit est un artefact du
   materiau de Stanford, et notre these porte sur une famille de pipelines qui n'est plus
   celle qu'on construit en 2026. (b) Le gabarit est produit par l'etiquette nommee, Twin n'en
   a pas, donc rien n'est contredit et t1 est une confirmation par l'absence. (c) La mesure de
   personne est trop indulgente sur un questionnaire de psychologie experimentale, ou une
   grande part des items est quasi determinee par des heuristiques stables. **Je penche pour
   (b) et je ne sais pas exclure (c) sans une decomposition par bloc d'items.** C'est un run
   d'une demi heure a zero appel.
2. **Faut il adopter la version partialisee comme forme publiee ?** Elle separe parfaitement
   sur Twin, elle ne coute rien, et elle repond a l'objection 1.3 de `a45` sans discuter. Le
   prix est qu'elle est definie **relativement au jeu de conditions publie** : ajouter une
   condition change tous les residus. Faut il la publier a cote de la brute, ou fixer une
   droite de reference une fois pour toutes sur les conditions du GSS ?
3. **`Demographics Only` de Twin est a 0,556 du plancher, `agents v6` du GSS a 0,236.** Si les
   deux recoivent bien des demographies sans etiquette ideologique nommee, c'est un facteur
   2,4 entre deux conditions de meme famille, et le dossier ne sait pas le decomposer entre
   l'invite, le modele et le questionnaire. **Est ce une limite acceptable pour un papier, ou
   faut il un run qui refasse `Demographics Only` sur les items du GSS ?**
4. **Le rapport de reassignation doit il disparaitre ?** Sur Twin il donne 7,31 a `B1 argmax`,
   plus que le 4,91 de `agents v8` sur le GSS, et son gain absolu est a 1,2 pour cent du
   plancher sans structure. `a47` E4 avait deja demande de le publier avec son gain absolu. **A
   ce stade je propose de le retirer des tableaux et de ne garder que le gain absolu rapporte
   au plancher `B0 tirage`**, qui dit la meme chose sans exploser.
5. **`LLM Finetuning (500 exemples)` est le generateur le plus degenere du dossier sur le
   deficit de patrons, moins 79,3 pour cent, detecte a 0,43 pour cent de contamination, et il
   est du cote du porteur de personne, 42 pour cent du plancher.** Les deux mesures sont
   orthogonales, Spearman 0,03. **Est ce un resultat a publier comme tel, « detectabilite et
   fidelite individuelle sont deux axes independants » ?** C'est la meilleure justification
   possible du test bilateral statistique par statistique de `i3b`, et elle vient d'un
   instrument different.
6. **Le placebo de la section 9 doit il etre refait sur un agent ?** Il est propre sur
   `B1 argmax` parce que j'ecris son entree. Sur C2 il coute une nuit courte d'appels et il
   fermerait le verrou 2 pour de bon. **La question est de savoir si un placebo sur une
   regression suffit a un relecteur pour accepter la lecture causale sur un agent.** Je pense
   que non, et je pense que le run R3 de la nuit du 8 au 9 le fournira.
7. **Le plancher humain de Twin est a 45,6 pour cent et celui du GSS a 34,7.** L'ecart va dans
   le sens attendu, le retest de Twin porte sur plusieurs semaines et pas deux, mais il n'a pas
   ete explique. **Faut il un tableau des planchers humains par jeu et par delai avant de
   parler de « part du plancher humain » dans un papier ?**

---

## 16. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python analyses/t1_baselines.py
.venv/bin/python analyses/t1_mesures.py --permutations 200 --sous 200
.venv/bin/python analyses/t1_nul.py --replicats 200 --replicats-six-axes 50 \
    --sous 100 --replicats-sous 20
.venv/bin/python analyses/t1_verdict.py --sous 2000
.venv/bin/python analyses/t1_placebo.py
.venv/bin/python analyses/t1_figure.py
```

Durees mesurees, quatre coeurs : **363 s** pour `t1_baselines.py`, **308 s** pour
`t1_mesures.py`, **896 s** pour `t1_nul.py`, **523 s** pour `t1_verdict.py`, **20 s** pour
`t1_placebo.py`, quelques secondes pour la figure. Total environ **35 minutes**. Aucun cache
externe n'est necessaire, le seul cache produit est `/tmp/t1-baselines.pkl`. Graine unique
`20260909` partout. Les scripts s'arretent sur assertion si l'ordre des items ou celui des
personnes differe entre `a2`, `a6` et `i3b`.

---

## 17. Fichiers produits

| fichier | contenu |
|---|---|
| `resultats/t1-preenregistrement.md` | le preenregistrement, horodate avant tout calcul |
| `resultats/t1-controles.csv` | les sept controles, 113 lignes, trois echecs declares |
| `resultats/t1-chute-segmentations.csv` | la chute, quatre segmentations, 76 lignes |
| `resultats/t1-reassignation.csv` | le gain hongrois absolu et son plancher, 76 lignes |
| `resultats/t1-generateur-nul.csv` | les ratios inter et intra contre leur nul, 38 lignes |
| `resultats/t1-generateur-nul-six-axes.csv` | la lecture secondaire, borne inferieure, 38 lignes |
| `resultats/t1-correlation-chute-exactitude.csv` | Q6 brute, 12 lignes |
| `resultats/t1-correlation-residus.csv` | Q6 partialisee, 64 lignes |
| `resultats/t1-classement.csv` | le verdict par configuration et `i3b`, 76 lignes |
| `resultats/t1-coherence-i3b.csv` | les correlations de rang avec `i3b`, 4 lignes |
| `resultats/t1-holm-contre-b0.csv` | le test preenregistre, 2 000 sous echantillons, 16 lignes |
| `resultats/t1-placebo-etiquette.csv` | l'ablation d'etiquette sur `B1`, 8 lignes |
| `resultats/t1-gss-contre-twin.csv` | les conditions analogues des deux jeux, 111 lignes |
| `resultats/t1-figure-personne-twin.png` et `.svg` | la figure, trois panneaux |
| `analyses/t1_commun.py` | chargement, segmentations, chaine de `a1`, intervalles |
| `analyses/t1_baselines.py` | `B0`, `B1`, `B2`, `PMM k=10` sur Twin |
| `analyses/t1_mesures.py` | controles, chute, reassignation, correlations, classement |
| `analyses/t1_nul.py` | le generateur nul sur les ratios de `a6` |
| `analyses/t1_verdict.py` | le test preenregistre a la bonne resolution |
| `analyses/t1_placebo.py` | l'ablation d'etiquette, hors preenregistrement |
| `analyses/t1_figure.py` | la figure |
