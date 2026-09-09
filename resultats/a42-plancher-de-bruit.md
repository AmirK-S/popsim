# a42. Le plancher de bruit de cellule, ferme : la rarete stable contre la rarete instable

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 6 et resume : « l'ablation de l'etiquette » devient « le contraste de conditionnement ». Objection a45 numero 1, contradiction D1.

**Phrases d'origine.** « **Le cinquieme est l'ablation de l'etiquette, quatrieme mesure
independante.** Sur les raretes stables du run local, `C3`, prive de toute etiquette, a un
exces de plus 0,1616 [0,1086 ; 0,2106] sur le plancher de son propre segment ; **`C2`, le
meme modele avec onze attributs demographiques**, est a plus 0,0327 [moins 0,0054 ; 0,0749] »
(section 2, reprise en section 6, « L'ablation de l'etiquette sur la rarete stable »).

**Correction.** La formule « le meme modele **avec** onze attributs demographiques » dit
litteralement que C2 est C3 plus l'etiquette, ce que le code refute en trois lignes : C2 a
les onze attributs **et n'a pas** les 119 reponses de la personne. Ecrire « le meme modele
conditionne sur onze attributs au lieu des 119 reponses de la personne » et remplacer le
titre de la section 6 par « le contraste de conditionnement sur la rarete stable ». Les deux
chiffres, plus 0,1616 et plus 0,0327, ne changent pas ; c'est leur attribution a l'etiquette
seule qui tombe.

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

Rapport du 8 septembre 2026. Il execute le **verrou 2** de `MODELE-DU-MONDE.md` section 6
et repond a la premiere des trois objections de la section 7 : *« le resultat des rares est
du bruit de petites cellules, controle a moitie par un plancher circulaire dans un rapport
non preenregistre »*.

**Preenregistre.** La famille d'hypotheses, les seuils, les planchers et les criteres de
chute sont ecrits dans `resultats/a42-preenregistrement.md`, **horodate du 8 septembre 2026
a 15:42:15 CEST**, avant le moindre calcul, et ce fichier n'a pas ete modifie ensuite. Il
est reproduit en section 1. C'est le premier ecart avec a34, qui declarait explicitement ne
pas revendiquer le pre enregistrement.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a42_commun.py`, `a42_plancher.py`, `a42_figure.py`. **Aucun script
existant n'a ete modifie** ; `a34_commun`, `a31_commun`, `a29_commun`, `a28_commun`,
`a25_commun`, `a25_mesures`, `a8_commun`, `a2_commun`, `a2_baselines_gss`, `a5_evaluer` et
`a5_agents_locaux_gss` sont importes tels quels, memes graines, memes plis, memes blocs,
memes 149 items, memes personnes. `PMM k=5`, `PMM k=10` et `IM m=10 mode des m` sont relues
du cache de a35, produites par `a35_commun.imputations_regression` : **elles etaient
importables, les trois**.

Sorties : `a42-partitions.csv`, `a42-stabilite.csv`, `a42-partitions-tierces.csv`,
`a42-contrastes.csv`, `a42-rennard.csv`, `a42-controles.csv`,
`a42-figure-plancher.png` et `.svg`.

---

## Reponse en une ligne

**L'objection tombe, et l'instrument qui servait a la formuler tombe avec elle.** Sur les
raretes que la personne **redonne** deux semaines plus tard, c'est a dire la vraie
heterogeneite individuelle et non le bruit humain de reponse, `agents composite` retrouve
**40,8 pour cent** des reponses rares quand la regression logistique en retrouve **8,0** et
la foret aleatoire **2,2**, pour un plancher de **10,9 pour cent** qu'obtient un tirage au
sort dans le segment ideologie x genre x age de la personne : **exces plus 0,2891
[0,2673 ; 0,3113]** pour les agents, **moins 0,0353** pour la regression et **moins 0,0878**
pour la foret [MESURE, `a42-stabilite.csv`, perimetre 1 052, seuil 10 pour cent]. **Dix des
treize methodes testees passent H1 et neuf des quatorze passent H2, correction de Holm sur
27 tests, p ajuste 0,0068.** Le critere de chute ecrit d'avance est donc franchi dans le bon
sens.

**Et l'avantage est PLUS GRAND sur les raretes stables que sur les instables, pas
l'inverse.** H3 : plus 0,1739 [0,1494 ; 0,2004] pour `agents composite`, plus 0,1210 pour
`agents entretien`, plus 0,0707 pour `agents enquete`, les trois a p ajuste 0,0068
[MESURE, `a42-contrastes.csv`]. **La lecture adverse, « les agents retrouvent surtout du
bruit humain », est mesuree et refutee dans sa propre direction.**

**Le troisieme resultat est le plus severe, et il porte contre nous.** La partition
placebo, neuf groupes de personnes tires **au hasard** et donc porteurs d'aucune
information, **reproduit trait pour trait le gradient de deductibilite** mesure sur la
division de recensement : gradient de l'exces entre tercile deductible et tercile non
deductible, plus 0,072 contre plus 0,053 pour `agents composite`, plus 0,104 contre plus
0,099 pour `PMM k=5`, moins 0,057 contre moins 0,057 pour la foret ; **l'ecart entre les
deux partitions ne depasse jamais 0,040 et vaut 0,019 en mediane**
[MESURE, `a42-partitions-tierces.csv`]. **Un tercile de « deductibilite » construit sur une
frequence de segment est d'abord un tercile de frequence d'item, et le hasard le fabrique
aussi bien qu'une vraie demographie.** C'est l'artefact de Rennard et Xypolopoulos mesure
chez nous, et il invalide comme instrument tout le dispositif de terciles de a34, y compris
son H4.

**Le quatrieme resultat corrige a34 sur son chiffre le plus vendable.** a34 ecrivait
qu'*« une regression logistique et une foret aleatoire sur demographies font moins bien
qu'un tirage au sort dans le segment de la personne »*. C'est confirme, et cela vaut aussi
pour `B2 argmax` et pour le tirage aveugle. **Mais l'appariement sur moyenne predite de a35
bat ce plancher largement : `PMM k=5` a plus 0,1505 d'exces sur les raretes stables, plus
que quatre des six conditions de Stanford** [MESURE]. La phrase « aucun predicteur
statistique ne bat le plancher » est fausse ; la phrase juste nomme les predicteurs par
l'esperance sur demographies.

**Le cinquieme est l'ablation de l'etiquette, quatrieme mesure independante.** Sur les
raretes stables du run local, `C3`, prive de toute etiquette, a un exces de **plus 0,1616
[0,1086 ; 0,2106]** sur le plancher de son propre segment ; `C2`, le meme modele avec onze
attributs demographiques, est a **plus 0,0327 [moins 0,0054 ; 0,0749]**, p ajuste 0,199 :
**il n'est pas distinguable d'un tirage au sort dans le segment de la personne**
[MESURE].

**Le controle de Rennard sur le support de modalite ne mord pas, et il faut dire pourquoi.**
Retirer les cellules dont la modalite est portee par moins de 20 personnes ne retire que
**72 cellules sur 3 130**, et l'avantage de `agents composite` passe de plus 0,3275 a plus
0,3277 [MESURE, `a42-rennard.csv`]. **Nos cellules ne sont pas les cellules de Rennard** :
les siennes sont des croisements demographiques a `n >= 20`, les notres sont des couples
item x modalite ou une modalite « rare » est encore portee par 75 personnes en mediane. Le
petit effectif est ailleurs, dans le segment de la personne, mediane de neuf, et c'est
exactement ce que le plancher de segment paie.

---

## 1. Le preenregistrement, reproduit

Reproduction integrale de `resultats/a42-preenregistrement.md`, fichier ecrit le
**8 septembre 2026 a 15:42:15 CEST**, avant tout calcul, et non modifie depuis.

### 1.1 Etat de connaissance declare au moment de l'ecriture

Les tableaux de a34, de a29 et la lecture 01 etaient lus. **Les trois partitions de a42, la
stabilite en vague 2, la division de recensement et la partition aleatoire, n'avaient jamais
ete construites ni regardees, sur aucune de leurs marges.** Les predictions de la section
1.4 sont donc des predictions au sens strict.

### 1.2 Les trois partitions tierces

- **P_A, la stabilite en vague 2.** Une cellule minoritaire est **stable** si la personne a
  redonne exactement la meme modalite deux semaines plus tard, **instable** sinon. Elle
  n'emploie ni la confiance d'un predicteur, ni une frequence de segment, ni un attribut
  demographique. Une rarete stable est de la vraie heterogeneite individuelle ; une rarete
  instable est indistinguable du bruit humain de reponse. **C'est la partition qui repond a
  l'adversaire.** Identite declaree d'avance : `humains vague 2` y vaut 1 sur les stables et
  0 sur les instables par construction, elle n'entre dans aucun test, et le troisieme
  plancher y est degenere.
- **P_B, la division de recensement.** Frequence de la modalite dans la division de
  recensement de la personne, sans la personne, en terciles. Ni la confiance de `B1`, ni le
  segment du plancher. **Defaut residuel declare d'avance** : `census_division` fait partie
  des onze attributs que `B1`, `B3 foret` et les personas demographiques recoivent ; la
  partition est independante du plancher et de la regle de decision de `B1`, pas de la
  famille des predicteurs.
- **P_C, la partition aleatoire fixee.** Neuf groupes tires au hasard, graine 20260908
  ecrite dans le preenregistrement. **Placebo** : tout gradient le long de P_C est du bruit
  d'echantillonnage de petites cellules et rien d'autre.

### 1.3 Les trois planchers

Tirage dans la marginale de l'item, sans la personne ; tirage dans la marginale du segment
ideologie x genre x age, sans la personne, qui est le plancher de bruit de cellule de la
lecture 01 importe de a34 ; et les memes humains reinterroges a deux semaines, **plancher
qui est en pratique un plafond** et qui est degenere sur P_A. Exces = rappel moins plancher
sur les memes cellules, intervalle par bootstrap apparie sur les personnes.

### 1.4 La famille declaree

| | enonce | direction | tests |
|---|---|---|---|
| **H1** primaire | pour chacune des 13 methodes testees, l'avantage de rappel sur `B1 argmax` **sur les raretes STABLES** est strictement positif | dirige | 13 |
| **H2** primaire | pour chacune des 14 methodes, l'exces de rappel sur le **plancher de segment**, **sur les raretes STABLES**, est strictement positif | dirige | 14 |
| **H3** secondaire | cet avantage differe t il entre STABLES et INSTABLES | bilateral | 13 |
| **H4** secondaire | l'exces sur plancher differe t il entre T3 et T1 de **P_B** | bilateral | 14 |
| **H5** tertiaire | H1 survit il au retrait des modalites portees par moins de 20 personnes | dirige | 13 |

**Famille primaire 27 tests, secondaire 27, tertiaire 13, corrigees separement par Holm**,
Benjamini Hochberg a cote, p de bootstrap apparie sur les personnes, 4 000 tirages,
plancher a 1 sur 4 000. Un contraste a denominateur vide recoit p = 1.

**Criteres de chute ecrits d'avance.** (1) Si H1 echoue pour `agents composite` et
`agents entretien`, la these tombe. (2) Si H2 echoue pour ces memes conditions, le resultat
est du bruit de petites cellules et la these tombe. (3) Si H3 est fortement negatif pour
elles, il faudra ecrire « les agents retrouvent surtout les raretes que la personne ne
reproduit pas », c'est a dire donner raison a l'adversaire.

**Predictions ecrites d'avance.** (a) H1 passe pour les six conditions de Stanford et pour
`C3`, incertain pour `C2`, `agents v7` et les trois methodes d'imputation. (b) H2 passe pour
les conditions riches et **echoue pour `B1`, `B3 foret`, `PMM` et `IM`**. (c) H3 est **non
significatif** pour la majorite. (d) P_C montre un gradient **non nul**.

**Bilan des predictions, apres coup** [MESURE] : (a) juste, sauf que `agents v7` echoue et
que les trois methodes d'imputation passent ; (b) **fausse sur `PMM` et `IM`, qui passent
H2** ; (c) **fausse : H3 est significativement positif pour six methodes sur treize**, donc
l'avantage est plus grand sur les stables ; (d) juste, et beaucoup plus fort que prevu.

---

## 2. La partition, et ce qu'elle contient

[MESURE, `a42-partitions.csv`, perimetre 1 052, seuil 10 pour cent]

| | cellules minoritaires | items | plancher item | plancher segment | support median |
|---|---|---|---|---|---|
| **rarete stable** | **3 130** | 70 | 0,0642 | 0,1094 | 75 |
| **rarete instable** | **2 579** | 69 | 0,0600 | 0,0728 | 71 |
| hors partition, vague 2 absente | **0** | 0 | | | |
| ensemble | 5 709 | 70 | 0,0623 | 0,0927 | 73 |

**Trois remarques avant le premier tableau de resultats.**

1. **La couverture de la vague 2 est de 100 pour cent des cellules minoritaires** : aucune
   cellule ne sort de la partition [MESURE, `a42-controles.csv`]. C'est le meilleur cas
   possible pour cette partition, et il n'etait pas garanti.
2. **54,8 pour cent des reponses rares sont stables.** Le chiffre n'est pas nouveau, c'est
   une identite : le rappel de `humains vague 2` sur les cellules minoritaires, 0,5483
   publie par a29 section 1, **est exactement la part de raretes stables**. La partition ne
   fait que rendre lisible ce que ce nombre disait deja.
3. **Les cellules stables sont plus faciles, et les planchers le disent avant les methodes**
   : le plancher de segment vaut 0,1094 sur les stables contre 0,0728 sur les instables. Le
   rappel brut ne prouve donc rien, et c'est pourquoi tout le rapport lit **l'exces**.

---

## 3. Le tableau qui repond a l'adversaire

Figure `a42-figure-plancher.png`, panneau 1.

[MESURE, `a42-stabilite.csv`, perimetre 1 052, seuil 10 pour cent, 4 000 tirages bootstrap
sur les personnes ; 3 130 cellules stables, 2 579 instables]

| condition | rappel stables | precision stables | **F1 stables** | **exces sur plancher de segment, stables** | exces, instables |
|---|---|---|---|---|---|
| ***humains vague 2*** | ***1,0000*** | ***1,0000*** | ***1,0000*** | ***identite, non teste*** | ***identite*** |
| **agents composite** | **0,4077** | 0,3343 | **0,3674** | **plus 0,2891** [0,2673 ; 0,3113] | plus 0,1100 |
| agents entretien (v3) | 0,3722 | 0,2876 | 0,3245 | plus 0,2577 [0,2363 ; 0,2786] | plus 0,1237 |
| agents enquete | 0,2847 | 0,2139 | 0,2442 | plus 0,1649 [0,1423 ; 0,1876] | plus 0,0830 |
| **PMM k=5** | **0,2677** | 0,2888 | **0,2779** | **plus 0,1505** [0,1310 ; 0,1706] | plus 0,0646 |
| **PMM k=10** | 0,2668 | 0,2925 | 0,2790 | plus 0,1494 [0,1308 ; 0,1693] | plus 0,0650 |
| agents v8 | 0,2077 | 0,1330 | 0,1622 | plus 0,0756 [0,0577 ; 0,0947] | plus 0,0406 |
| agents demographiques (v6) | 0,1687 | 0,3021 | 0,2165 | plus 0,0634 [0,0445 ; 0,0832] | plus 0,0834 |
| **IM m=10 mode des m** | 0,1709 | 0,3880 | 0,2373 | plus 0,0518 [0,0368 ; 0,0676] | moins 0,0035 |
| agents v7 | 0,0863 | 0,1199 | 0,1003 | **moins 0,0266** [moins 0,0402 ; moins 0,0129] | moins 0,0292 |
| **B1 argmax** | **0,0802** | 0,2337 | 0,1194 | **moins 0,0353** [moins 0,0446 ; moins 0,0261] | moins 0,0454 |
| B0 tirage | 0,0604 | 0,0437 | 0,0507 | moins 0,0482 | moins 0,0116 |
| **B2 argmax** | 0,0518 | **0,5329** | 0,0944 | **moins 0,0590** [moins 0,0702 ; moins 0,0475] | moins 0,0570 |
| **B3 foret** | **0,0224** | 0,5109 | 0,0429 | **moins 0,0878** [moins 0,0942 ; moins 0,0813] | moins 0,0681 |
| B0 mode | 0,0000 | sans objet | 0,0000 | moins 0,1094 | moins 0,0728 |
| *plancher, tirage dans la marginale du segment* | *0,1094* | | | *par definition zero* | |
| *plancher, tirage dans la marginale de l'item* | *0,0642* | | | | |

**Ce que ce tableau dit, dans l'ordre.**

1. **Le critere de chute numero 1 est franchi.** L'avantage de `agents composite` sur la
   regression logistique, sur les seules raretes que la personne reproduit, vaut **plus
   0,3275 [0,3058 ; 0,3502]**, p ajuste par Holm 0,0068 sur une famille de 27 tests
   [MESURE, `a42-contrastes.csv`]. **Dix des treize methodes testees passent H1** ; les
   trois echecs sont `agents v7`, plus 0,0061 [moins 0,0093 ; 0,0220], p ajuste 0,485, et
   `B2 argmax` et `B3 foret`, dont l'avantage est **negatif**, moins 0,0284 et moins 0,0578,
   significativement.
2. **Le critere de chute numero 2 est franchi.** **Neuf des quatorze methodes** ont un
   exces strictement positif sur le plancher de bruit de cellule, sur les raretes stables.
   Les cinq qui ne passent pas : `agents v7`, `B1 argmax`, `B2 argmax` et `B3 foret`, dont
   l'exces est significativement **negatif**, et `C2`, non distinguable de zero.
3. **En rapport, l'avantage est un peu plus grand sur les instables ; en difference, il est
   beaucoup plus grand sur les stables.** Rapport `agents composite` sur `B1 argmax` :
   **5,1 contre 1 sur les stables, 6,0 contre 1 sur les instables**. Difference : plus
   0,3275 contre plus 0,1536. **Les deux sont vraies et il faut porter la seconde**, parce
   que c'est celle qui repond a l'objection : la masse d'avantage est sur la vraie
   heterogeneite.
4. **La signature de a29 se reproduit intacte.** `B2 argmax` et `B3 foret` ont la meilleure
   precision du tableau sur les raretes stables, 0,533 et 0,511, pour un rappel de 5,2 et
   2,2 pour cent. **Elles ne se trompent pas, elles n'osent pas** : 304 et 137 raretes osees
   sur 156 748 cellules.
5. **`B0 tirage` est le temoin de lecture attendu** : son exces sur le plancher d'ITEM vaut
   moins 0,0038, c'est a dire zero. Un tirage dans la marginale de l'item obtient bien le
   plancher d'item, ce qui verifie la chaine.

---

## 4. H3 : l'avantage tient il sur les raretes stables ? Il y est plus grand

C'est la question posee par la mission, et la reponse est directionnelle.

[MESURE, `a42-contrastes.csv`, famille secondaire, 27 tests, Holm]

| condition | avantage stables moins avantage instables | IC 95 % | p Holm | lecture |
|---|---|---|---|---|
| **agents composite** | **plus 0,1739** | [0,1494 ; 0,2004] | **0,0068** | **l'avantage est sur la vraie heterogeneite** |
| **agents entretien (v3)** | **plus 0,1210** | [0,0962 ; 0,1460] | **0,0068** | idem |
| agents enquete | plus 0,0707 | [0,0451 ; 0,0970] | **0,0068** | idem |
| PMM k=10 | plus 0,0706 | [0,0480 ; 0,0940] | **0,0068** | idem |
| PMM k=5 | plus 0,0704 | [0,0466 ; 0,0946] | **0,0068** | idem |
| IM m=10 mode des m | plus 0,0477 | [0,0287 ; 0,0661] | **0,0068** | idem |
| agents v8 | plus 0,0305 | [0,0085 ; 0,0534] | 0,0520 | ne passe pas |
| C3 | plus 0,0075 | [moins 0,0660 ; 0,0766] | 1,000 | rien |
| agents v7 | moins 0,0071 | [moins 0,0250 ; 0,0104] | 1,000 | rien |
| B2 argmax | moins 0,0137 | [moins 0,0280 ; 0,0006] | 0,4305 | rien |
| C2 | moins 0,0235 | [moins 0,0793 ; 0,0317] | 1,000 | rien |
| **B3 foret** | **moins 0,0315** | [moins 0,0434 ; moins 0,0200] | **0,0068** | avantage sur les instables |
| **agents demographiques (v6)** | **moins 0,0352** | [moins 0,0579 ; moins 0,0113] | **0,0450** | avantage sur les instables |

**Six methodes sur treize ont un avantage significativement plus grand sur les raretes
STABLES, et ce sont les meilleures du dossier plus les deux PMM. Deux ont l'inverse, la
foret aleatoire et la condition de Stanford qui n'a qu'une persona demographique. Cinq ne
disent rien.**

**C'est la refutation la plus directe que le projet ait de l'objection.** L'adversaire
suppose que l'avantage vient du bruit ; la mesure dit que l'avantage grandit quand on
retire le bruit. La seule methode a modele de langage qui va dans le sens de l'adversaire
est **`agents demographiques (v6)`, celle qui ne recoit que l'etiquette**, ce qui est
coherent avec a29, a31, a34 et la section 6 de ce rapport : l'etiquette est ce qui deplace
une methode vers le regime statistique.

---

## 5. Le placebo, et ce qu'il detruit

C'est le resultat le plus severe du rapport, et il porte contre l'outillage du dossier, pas
contre sa these.

[MESURE, `a42-partitions-tierces.csv`, perimetre 1 052, seuil 10 pour cent. Gradient =
exces sur le plancher de segment dans le tercile deductible, moins le meme exces dans le
tercile non deductible]

| condition | **P_B, division de recensement** | **P_C, partition ALEATOIRE** | ecart |
|---|---|---|---|
| humains vague 2 | plus 0,0015 | plus 0,0058 | moins 0,0044 |
| agents composite | plus 0,0720 | plus 0,0529 | plus 0,0191 |
| agents entretien (v3) | plus 0,1227 | plus 0,0860 | plus 0,0368 |
| agents enquete | plus 0,0551 | plus 0,0303 | plus 0,0247 |
| agents demographiques (v6) | moins 0,1611 | moins 0,1884 | plus 0,0272 |
| agents v7 | moins 0,0296 | moins 0,0458 | plus 0,0162 |
| agents v8 | plus 0,0523 | plus 0,0646 | moins 0,0122 |
| PMM k=5 | plus 0,1036 | plus 0,0989 | plus 0,0047 |
| PMM k=10 | plus 0,1229 | plus 0,1039 | plus 0,0190 |
| IM m=10 mode des m | plus 0,0813 | plus 0,0535 | plus 0,0278 |
| B2 argmax | moins 0,0144 | moins 0,0180 | plus 0,0036 |
| B1 argmax | plus 0,0228 | moins 0,0172 | plus 0,0400 |
| B3 foret | moins 0,0565 | moins 0,0566 | **0,0000** |
| B0 tirage | moins 0,0252 | moins 0,0351 | plus 0,0099 |

**L'ecart entre les deux colonnes ne depasse jamais 0,040 et vaut 0,016 en mediane, quand
les gradients eux memes vont de moins 0,19 a plus 0,12** [MESURE]. La partition aleatoire
reproduit meme le seul gradient negatif fort du dossier, celui de
`agents demographiques (v6)`, a 0,027 pres.

**Le mecanisme est visible dans la description des terciles.** Le plancher d'ITEM vaut
0,040 / 0,068 / 0,079 sur les terciles de P_B et 0,039 / 0,069 / 0,081 sur ceux de P_C
[MESURE, `a42-partitions.csv`]. **Un tercile de frequence dans un segment est d'abord un
tercile de frequence dans l'item**, parce que la frequence dans un groupe de taille finie
estime la marginale de l'item, avec du bruit. Un groupe aleatoire l'estime sans biais ; un
groupe demographique l'estime avec une information marginale en plus. **La quantite qu'on
appelait « deductibilite » est donc, pour l'essentiel, la frequence de la modalite.**

**Ce que cela invalide.** H4 est declare et il passe pour onze methodes sur quatorze
[MESURE, `a42-contrastes.csv`] ; **il ne doit pas etre lu comme un resultat sur la
deductibilite**, puisque le placebo produit le meme. Par transitivite, **la partition en
terciles de a34, D_seg comme D_logit, ne mesure pas ce que son nom dit**, et son H4
n'aurait pas du etre interprete. La partition qui reste debout est P_A, la stabilite, et
c'est la seule qui n'a pas de placebo possible : le hasard ne peut pas fabriquer la
question « la personne a t elle redonne la meme reponse ».

**Ce que cela n'invalide pas.** Les rappels par tercile de a34 restent des mesures justes ;
c'est leur interpretation en termes de deductibilite qui tombe. Et le resultat central de
a34, l'exces sur le plancher de segment, est reproduit ici sur une partition qui n'a pas ce
defaut : voir la section 3.

---

## 6. L'ablation de l'etiquette sur la rarete stable

[MESURE, `a42-stabilite.csv`, perimetre 150, seuil 10 pour cent, 354 raretes stables]

| condition | rappel stables | exces sur plancher de segment | IC 95 % |
|---|---|---|---|
| *humains vague 2* | *1,0000* | *identite* | |
| agents composite | 0,3418 | plus 0,2308 | [0,1715 ; 0,2909] |
| agents entretien (v3) | 0,3249 | plus 0,2214 | [0,1624 ; 0,2810] |
| PMM k=10 | 0,3023 | plus 0,2025 | [0,1475 ; 0,2557] |
| PMM k=5 | 0,2768 | plus 0,1742 | [0,1224 ; 0,2227] |
| **C3, sans etiquette** | **0,2486** | **plus 0,1616** | **[0,1086 ; 0,2106]** |
| agents enquete | 0,2345 | plus 0,1428 | [0,0846 ; 0,2008] |
| agents v8 | 0,1723 | plus 0,0641 | [0,0167 ; 0,1134] |
| IM m=10 mode des m | 0,1554 | plus 0,0516 | [0,0104 ; 0,0917] |
| agents demographiques (v6) | 0,1384 | plus 0,0421 | [moins 0,0091 ; 0,0957] |
| **C2, avec etiquette** | **0,1412** | **plus 0,0327** | **[moins 0,0054 ; 0,0749]** |
| B0 tirage | 0,0847 | moins 0,0176 | [moins 0,0573 ; 0,0252] |
| B1 argmax | 0,0706 | moins 0,0239 | [moins 0,0523 ; 0,0077] |
| B2 argmax | 0,0480 | moins 0,0522 | [moins 0,0770 ; moins 0,0259] |
| B3 foret | 0,0141 | moins 0,0868 | [moins 0,1165 ; moins 0,0591] |

**A modele, temperature, personnes, questions et traces constants, donner l'etiquette
demographique fait passer l'exces sur le plancher de segment de plus 0,1616 a plus 0,0327,
c'est a dire d'un resultat a une valeur non distinguable d'un tirage au sort dans le
segment de la personne**, p ajuste par Holm 0,199 [MESURE]. `C3` passe H1 et H2 ;
**`C2` passe H1, plus 0,0706 [0,0275 ; 0,1145], et echoue H2.**

C'est la cinquieme mesure independante du meme phenomene, apres la deviance de a23, la
correlation par personne de a29, le lift de groupe de a31 et le rappel par tercile de a34.
**Et c'est la premiere qui le montre sur les seules raretes que la personne reproduit**,
donc sur de l'heterogeneite verifiee et non sur du bruit.

---

## 7. Le controle de Rennard, et pourquoi il ne mord pas ici

[MESURE, `a42-rennard.csv`, perimetre 1 052, raretes stables, seuil 10 pour cent]

| support minimal de la modalite | cellules restantes | rappel `agents composite` | exces sur plancher | avantage sur `B1 argmax` |
|---|---|---|---|---|
| aucun | 3 130 | 0,4077 | plus 0,2891 | plus 0,3275 [0,3058 ; 0,3502] |
| >= 5 personnes | 3 122 | 0,4078 | plus 0,2888 | plus 0,3274 |
| >= 10 personnes | 3 109 | 0,4078 | plus 0,2883 | plus 0,3271 |
| **>= 20 personnes** | **3 058** | **0,4097** | **plus 0,2883** | **plus 0,3277** [0,3062 ; 0,3505] |

**H5 passe pour huit des treize methodes**, les memes que H1 hormis `C2` et `C3`, p ajuste
par Holm 0,0032 sur une famille de 13 tests [MESURE, `a42-contrastes.csv`]. `agents v7`
echoue, `B2 argmax` et `B3 foret` restent negatives, et **`C2` et `C3` sont non evaluables
par arithmetique** : sur 150 personnes, une modalite minoritaire
au seuil de 10 pour cent est portee par 14 personnes au plus, donc le filtre a 20 vide
l'ensemble. Elles recoivent p = 1, convention conservatrice declaree. Au filtre effectif de
ce perimetre, **n >= 10, 181 cellules sur 354, `C3` garde un exces de plus 0,1858
[0,1173 ; 0,2534] et `C2` de plus 0,0253 [moins 0,0255 ; 0,0789]** : l'ablation survit
[MESURE, hors famille].

**Pourquoi le controle ne mord pas, et c'est une information et non une deception.** Le
support median d'une modalite minoritaire stable est de **75 personnes** sur 1 052 : nos
cellules ne sont pas les cellules de Rennard et Xypolopoulos, qui travaillent sur des
croisements demographiques a `n >= 20` et dont le bruit vient du petit effectif de la
cellule de verite terrain. **Chez nous le petit effectif est ailleurs** : dans le segment
ideologie x genre x age, 98 cases pour 1 052 personnes, mediane de neuf. **C'est
precisement ce que le plancher de segment paie, et c'est pourquoi il est le bon controle et
le filtre de support le mauvais.** L'avertissement de la lecture 01 s'applique a notre
dossier par le plancher, pas par le filtre.

---

## 8. Robustesse au seuil de 20 pour cent

[MESURE, `a42-stabilite.csv`, hors famille, perimetre 1 052, 11 153 raretes stables et
7 258 instables]

| condition | rappel stables | exces sur plancher de segment, stables | exces, instables |
|---|---|---|---|
| agents composite | 0,4507 | plus 0,2659 | plus 0,0704 |
| agents entretien (v3) | 0,4257 | plus 0,2398 | plus 0,0988 |
| PMM k=5 | 0,3893 | plus 0,2043 | plus 0,0978 |
| agents enquete | 0,3265 | plus 0,1412 | plus 0,0648 |
| IM m=10 mode des m | 0,3094 | plus 0,1223 | plus 0,0342 |
| agents v8 | 0,2557 | plus 0,0586 | plus 0,0234 |
| agents demographiques (v6) | 0,1996 | plus 0,0223 | plus 0,0293 |
| agents v7 | 0,1537 | moins 0,0276 | moins 0,0368 |
| **B1 argmax** | 0,1605 | **moins 0,0288** | moins 0,0592 |
| **B2 argmax** | 0,1273 | **moins 0,0595** | moins 0,0954 |
| **B3 foret** | 0,0650 | **moins 0,1205** | moins 0,1142 |

**Meme ordre, meme lecture, meme signe partout.** L'ecart stables contre instables se
maintient pour les conditions riches et pour PMM ; le plancher monte de 0,109 a 0,179 et
les trois predicteurs par l'esperance restent dessous.

---

## 9. Ce que cela change a `MODELE-DU-MONDE.md` section 7

**Le verrou 2 de la section 6 est ferme.** Sa formulation disait : *« la these des rares
survit a sa contre expertise ou tombe avant qu'un relecteur la fasse tomber »*. Elle
survit, et la contre expertise a coute une soiree et zero appel.

### 9.1 La phrase de l'adversaire, a reecrire

La section 7 ecrit aujourd'hui : *« Le resultat des rares est du bruit de petites cellules,
controle a moitie par un plancher circulaire dans un rapport non preenregistre. »* **Les
trois griefs sont leves separement** [MESURE].

1. **« du bruit de petites cellules »** : sur les seules raretes que la personne reproduit
   a deux semaines, l'avantage est plus grand que sur les instables, plus 0,174 pour la
   meilleure condition, et il survit au retrait des modalites portees par moins de vingt
   personnes.
2. **« un plancher circulaire »** : le plancher est le meme qu'en a34, mais il est
   desormais lu sur une partition qui ne le contient pas, la stabilite en vague 2, laquelle
   n'emploie ni predicteur ni demographie.
3. **« un rapport non preenregistre »** : `a42-preenregistrement.md` est horodate du
   8 septembre 2026 a 15:42:15 CEST, ses predictions sont ecrites, et **deux d'entre elles
   sont fausses**, ce qui est la seule preuve utile qu'il a bien ete ecrit avant.

### 9.2 Quatre phrases a changer dans le texte de la these

1. **A ajouter, et c'est la phrase la plus forte du rapport** : *« sur les reponses rares
   que la personne redonne a l'identique deux semaines plus tard, donc sur de
   l'heterogeneite verifiee et non sur du bruit de reponse, une population simulee retrouve
   40,8 pour cent des reponses rares quand une regression logistique sur les memes attributs
   en retrouve 8,0, pour un plancher de 10,9 qu'obtient un tirage au sort dans le segment
   demographique de la personne ; l'avantage est plus grand sur ces raretes la que sur les
   raretes instables, plus 0,17 de difference »*. [MESURE]
2. **A corriger.** La section 7 ecrit *« la ou tout predicteur par l'esperance fait moins
   bien qu'un tirage au sort dans le segment de la personne »*. **Le mot « tout » est
   faux** : `PMM k=5` et `PMM k=10`, appariement sur moyenne predite sur le contexte, ont un
   exces de plus 0,15 sur ce plancher, et `IM m=10` de plus 0,05. La phrase juste est
   *« la ou les predicteurs par l'esperance sur demographies, regression logistique et foret
   aleatoire, font moins bien qu'un tirage au sort dans le segment de la personne »*.
   [MESURE] C'est aussi une correction de l'enonce numero 4 de a34 section 7.
3. **A retirer du stock d'arguments.** Toute formulation en terciles de deductibilite. Le
   placebo montre qu'une partition aleatoire produit le meme gradient : **la deductibilite
   ainsi mesuree n'est pas une variable, c'est une frequence d'item deguisee.** [MESURE]
4. **A renforcer.** *« une sur cinq retrouvee contre une sur soixante dix pour la
   regression »* peut devenir, sur la partition qui compte, **« deux sur cinq contre une
   sur douze »** : 0,4077 contre 0,0802 sur les raretes stables. [MESURE]

### 9.3 Ce qui reste ouvert dans la section 7

La deuxieme objection, *« l'avantage du langage dans le regime severe est une estimation
ponctuelle sans intervalle »*, n'est pas traitee ici : c'est le verrou 1, et a41 s'en
occupe. La troisieme, le renommage de Peng, Xie et Rennard, n'est pas affectee. **La
section 8, « ce que je ne sais pas », perd une ligne** : *« je ne sais pas si le tercile
indeductible de a34 est un zero structurel ou un zero d'echantillonnage »* devient sans
objet, puisque la partition en terciles est retiree comme instrument ; la question de
Garrido et al. reste posee mais elle ne porte plus sur un resultat publie.

---

## 10. Ce que je n'ai pas pu verifier

1. **La division de recensement compte dix niveaux, pas neuf.** Le preenregistrement en
   annonce neuf ; la mesure en trouve dix, le dixieme etant `foreign`
   [MESURE, `a42-controles.csv`]. L'ecart est sans consequence sur les terciles, mais il est
   ecrit ici parce qu'un preenregistrement se juge aussi sur ses erreurs.
2. **P_B n'est pas independante des predicteurs, et je l'ai declare avant de la
   construire.** `census_division` fait partie des onze attributs de `B1`, `B3 foret` et des
   personas demographiques. Le controle arithmetique declare est passe, la regression y
   place 11,0 pour cent de ses raretes dans le tercile non deductible et 59,4 dans le
   deductible, donc la partition n'est pas tautologique comme D_logit ; **mais elle n'est
   pas tierce au sens fort.** Vu la section 5, cela n'a plus grande importance : elle ne
   mesure de toute facon pas ce qu'on croyait.
3. **La stabilite en vague 2 n'est pas une mesure pure d'heterogeneite.** Une personne peut
   redonner une reponse rare par memoire de sa premiere reponse plutot que par conviction,
   et deux semaines est un delai court. Le sens de la partition, « vraie heterogeneite
   contre bruit », est donc une interpretation defendable et non une mesure directe
   [PROBABLE]. Le delai de a12 est le seul dont nous disposons.
4. **La classe d'une cellule sur P_A depend de la seule reponse de vague 2**, sans modele de
   mesure. Une modelisation classe latente donnerait une probabilite de stabilite au lieu
   d'une dichotomie et deplacerait les frontieres ; je ne l'ai pas faite, et le
   preenregistrement ne la prevoyait pas.
5. **Le filtre de support de Rennard est calcule sur le perimetre**, comme le
   preenregistrement le dit, ce qui rend H5 non evaluable pour `C2` et `C3` par
   arithmetique. Un support calcule sur les 1 052 aurait rendu le test evaluable sur les
   150 ; ce choix n'a pas ete fait apres coup, il est reste tel qu'ecrit.
6. **`E1 regression contexte argmax` et la copule gaussienne de a35 ne sont pas dans la
   famille.** Le preenregistrement ne nomme que `PMM` et `IM`, et je ne les ai pas ajoutees
   apres avoir vu que `PMM` passait H2. La comparaison complete avec les vingt methodes
   d'imputation de a35 sur cette partition reste a faire.
7. **Aucun test sur Twin-2K-500 ni sur le WVS.** Comme a28, a29, a31 et a34, tout est sur le
   GSS, et la vague 2 est ce qui rend a42 possible : le protocole ne se transporte pas a un
   jeu sans reinterrogation.
8. **La comparabilite des invites de `C2` et `C3` avec celles de Stanford**, ouverte depuis
   a17 et a23, pese ici sur toute la section 6, exactement comme sur a34 section 3.2.
9. **Je n'ai pas mesure la sensibilite au comparateur.** `B1 argmax` est declare parce que
   c'est l'adversaire de von der Heyde ; avec `PMM k=10` comme comparateur, quatre des six
   conditions de Stanford perdraient leur avantage sur les raretes stables. **Le fait est
   lisible dans le tableau de la section 3 et il n'est pas teste.**

---

## 11. Questions ouvertes pour Simon

1. **Le placebo doit il entrer dans le papier, ou seulement dans le dossier ?** « Une
   partition aleatoire reproduit le gradient de deductibilite trait pour trait » est une
   critique methodologique qui vaut pour von der Heyde, pour a34 et pour tout audit qui
   decoupe des cellules par frequence. Elle est courte, elle se comprend seule, et elle
   demontre l'avertissement de Rennard sur nos donnees au lieu de le citer. Mais elle
   affaiblit un tableau que nous avons publie il y a six heures.
2. **La partition stable contre instable doit elle devenir la partition principale du
   papier ?** Elle a trois avantages sur les terciles : elle n'a pas de placebo possible,
   elle ne depend d'aucun predicteur, et elle a une lecture en un mot pour un lecteur non
   technique, « la personne l'a t elle redit ». Son cout est qu'elle exige une vague 2, ce
   qu'un relecteur pourra reprocher au protocole plutot qu'a la mesure.
3. **Que fait on de PMM ?** C'est le vrai adversaire du dossier, pas la regression. Sur les
   raretes stables il bat quatre des six conditions de Stanford et il coute zero appel de
   modele. Faut il le mettre dans le titre du tableau comparatif, au risque que le papier
   reponde a la question « le langage est il utile » par « pas plus que l'appariement sur
   moyenne predite, sauf dans le regime severe » ?
4. **`agents demographiques (v6)` est la seule condition a modele de langage dont l'avantage
   est plus grand sur les raretes INSTABLES.** C'est aussi celle qui n'a que l'etiquette.
   Est ce le meme fait que a29 point 5, a31 et a34 section 4, ou une coincidence de plus ?
   Trois mesures sur quatre le disent maintenant.
5. **Faut il un second delai de retest ?** Deux semaines separent nos vagues. Si la
   stabilite a quatre mois donnait le meme classement, la lecture « vraie heterogeneite »
   deviendrait tres difficile a attaquer ; si elle le renversait, elle dirait que nous
   mesurons de la memoire de reponse. Le GSS panel de a12 a t il un troisieme point ?
6. **La lecture 01 nous demandait un plancher, nous en avons trois.** Le plancher des
   humains de la vague 2 est degenere sur la partition qui compte. Faut il un quatrieme
   plancher, par demi echantillons de la meme cellule comme Rennard le fait, pour avoir un
   chiffre comparable ligne a ligne avec L1.01b, qui publie 0,079 / 0,120 / 0,147 ?
7. **Faut il corriger a34 en place ?** Son enonce numero 4 est faux depuis a42, `PMM` bat le
   plancher, et son H4 n'est pas interpretable depuis le placebo. Corriger en place ou
   porter la restriction dans le papier, comme la question 4 de a34 le demandait deja pour
   a31 ?

---

## Rejouer

```
.venv/bin/python analyses/a42_plancher.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl --tirages 4000
.venv/bin/python analyses/a42_figure.py
```

Les trois caches sont ceux de a25, de a28 et de a35 ; les deux premiers se reconstruisent
seuls s'ils manquent, le troisieme est produit par `a35_imputation.py` et **n'est jamais
reecrit par a42**. Duree mesuree : **15 secondes** pour `a42_plancher` avec 4 000 tirages
bootstrap sur deux perimetres et deux seuils, **4 secondes** pour la figure, sur quatre
coeurs. Graine d'analyse 20260908, graine de la partition placebo 20260908 fixee dans le
preenregistrement, graine de protocole 20260903 heritee de a2. Aucun appel de modele,
aucune ecriture dans `data/`, aucun fichier existant modifie.
