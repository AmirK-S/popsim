# a33. La fausse rarete vient elle d'un contexte insuffisant ? La condition C3F, enfin exploitee

Rapport du 8 septembre 2026. Il execute le travail que a31 designe lui meme comme la
mesure manquante, section 10 point 3 et question 3 pour Simon : « il faudrait une
condition dont le contexte varie a personne constante ; `C3F`, qui ampute la famille
thematique entiere, est exactement cela et n'a pas ete exploitee ici ». Sa trace existe
depuis 06:20 ce matin, 1,9 Mo, et elle n'etait ni dans a25, ni dans a28, ni dans a29, ni
dans a31.

a31 laisse H5, le contexte insuffisant, dans un etat inconfortable : le test declare est
confondu par construction, `B0 tirage` le passe alors qu'il est aveugle, et les deux
mesures de contexte disponibles, la rarete du contexte de H5 et la rarete de la personne
de H1b, sont numeriquement presque la meme quantite, 0,0439 contre 0,0436 pour
`agents composite`. Aucune des deux n'isole « le contexte vu » de « la personne ». C3F
separe les deux : meme modele, memes personnes, memes items, meme chaine de scoring que
C3, et un contexte ampute.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a33_commun.py`, `a33_contexte_rarete.py`, `a33_figure.py`. **Aucun
script existant n'a ete modifie** ; `a31_commun`, `a31_mecanismes`, `a29_commun`,
`a28_commun`, `a25_commun`, `a25_mesures`, `a8_commun`, `a2_commun`, `a2_baselines_gss`,
`a5_evaluer` et `a5_agents_locaux_gss` sont importes tels quels, memes graines, memes
plis, memes blocs, memes 149 items, memes personnes. Le temoin aveugle a la personne, le
bootstrap apparie sur les personnes et les covariables de cellule sont ceux de a31, sans
une ligne recopiee.

Sorties : `a33-mesures.csv`, `a33-contrastes.csv`, `a33-leviers-personne-segment.csv`,
`a33-par-famille.csv`, `a33-contexte.csv`, `a33-quintiles.csv`, `a33-confiance.csv`,
`a33-sensibilites.csv`, `a33-cousins.csv`, `a33-controles.csv`, `a33-figure-c3f.png` et
`.svg`.

---

## Reponse en une ligne

**Non. Amputer le contexte a personne constante coute six points d'exactitude et ne rend
pas la fausse rarete plus frequente parmi les raretes osees ni plus « de groupe » : la
rarete de groupe des fausses raretes BAISSE au lieu de monter, moins 0,0135
[moins 0,0207 ; moins 0,0064], p ajuste par Holm 0,00175 sur une famille de 7 tests
declaree avant execution.** [MESURE, `a33-contrastes.csv`, 60 personnes, 58 items,
3 480 cellules, IC bootstrap sur les personnes, 4 000 tirages]

Le detail, dans l'ordre des sept contrastes declares. **P1, l'exactitude tombe de 0,6195 a
0,5572, moins 0,0624 [moins 0,0828 ; moins 0,0422], p ajuste 0,00175** : l'ablation mord,
elle n'est pas cosmetique. **P2, le taux de fausses raretes ne bouge pas de facon
decidable**, 0,826 pour C3 contre 0,867 pour C3F, plus 0,041 [moins 0,009 ; plus 0,087], p
ajuste 0,59. **P3 et P4, le rappel et la precision des cellules minoritaires ne
bougent pas de facon decidable non plus.** **P5, la rarete du cote de la personne ne bouge pas**, moins 0,0027
[moins 0,0076 ; plus 0,0023], p ajuste 0,91. **P6, la rarete du cote du groupe baisse**,
et c'est le seul contraste, avec l'exactitude, qui passe la correction. **P7, le choix de
la modalite rare n'est pas evaluable sur ce perimetre** : sur les 58 items de famille, 21
portent une modalite minoritaire et **aucun n'en porte deux**, si bien que oser une rarete
c'est y oser LA rarete et que la question du choix ne se pose pas.

**La prediction de H5 est donc refusee sur ses deux termes.** Elle annoncait plus de
fausses raretes et un rapport groupe sur personne plus eleve. Le taux ne monte pas de
facon decidable, et la quantite testee du cote du groupe descend. **La prediction de H2
seule est celle qui survit** : seule l'exactitude baisse.

**Trois faits mesures encadrent cette lecture et l'empechent d'etre lue trop largement.**

1. **L'amputation de C3F n'est pas une reduction de volume.** C3 voit 119,2 items en
   moyenne, les 149 moins son bloc secret, dont **8,72 cousins de la famille de l'item** ;
   C3F en voit **137,3**, les 149 moins la famille, et **zero cousin**. C3F voit donc PLUS
   d'items que C3. Ce qui est retire est l'information la plus proche de la question, pas
   la quantite d'information [MESURE, `a33-contexte.csv`, `a33-cousins.csv`].
2. **Le nombre de fausses raretes augmente en valeur absolue, parce que le modele ose
   davantage, pas parce qu'il vise plus mal.** 124 fausses raretes contre 95, soit
   plus 0,0083 par cellule [plus 0,0032 ; plus 0,0135], quand les raretes osees montent de
   plus 0,0081 par cellule [plus 0,0026 ; plus 0,0138]. Les deux montent du meme montant :
   **la proportion, elle, ne bouge pas**, ce qui est exactement ce que dit P2. Ces deux
   mesures sont **post hoc**, hors des deux familles declarees, et signalees comme telles
   partout [MESURE].
3. **Le rapport groupe sur personne n'est pas identifiable sur 60 personnes.** Il vaut
   1,22 pour C3 et 1,17 pour C3F, mais son intervalle bootstrap est [0,22 ; 8,30] pour C3
   et [moins 9,17 ; 10,78] pour C3F. **Aucune conclusion ne peut etre tiree de ce rapport
   sur ce perimetre**, et le rapport n'est de toute facon jamais teste, a31 section 8
   point 6 l'interdit [MESURE, `a33-mesures.csv`].

---

## 0. Le protocole, ecrit avant les resultats

La famille est recopiee sans retouche de l'entete de
`analyses/a33_contexte_rarete.py`, ou elle a ete ecrite avant l'execution. La seule
verification possible pour un tiers est la lecture de la docstring, qui n'a pas ete
modifiee apres coup.

**Perimetre declare** : les **60 personnes completes** de la trace C3F et les **58 items**
des six familles thematiques de `a2_baselines_gss`, soit **3 480 cellules**, restreintes
aux cellules dont la reponse de la vague 1 est observee ET que C3 et C3F predisent toutes
les deux. Toutes les conditions sont evaluees sur ces cellules la et sur aucune autre. En
pratique les 3 480 cellules sont retenues : aucune reponse de vague 1 ne manque et aucune
des deux conditions ne refuse [MESURE, `a33-controles.csv`].

**Seuil declare** : 10 pour cent. **Reference de minorite declaree** : la population des
**1 052 personnes** du perimetre GSS, et non les 60 du perimetre. Motif ecrit avant
execution : sur 60 personnes, un seuil de 10 pour cent porte sur six repondants et la
rarete d'un segment ideologique serait estimee sur huit personnes en moyenne. **C'est un
ecart assume a la convention de a29 et a31**, qui calculent la reference sur le perimetre ;
les variantes « reference sur les 150 » et « seuil 20 pour cent » sont rapportees comme
sensibilites dans `a33-sensibilites.csv`.

**Unite d'analyse declaree** : la **fausse rarete**, memes definitions que a29 et a31, une
cellule ou la methode predit une modalite minoritaire et ou la personne a en realite donne
une modalite majoritaire.

**Les deux predictions concurrentes, ecrites avant l'execution.**

> **Si H5 est vraie** : C3F pose PLUS de fausses raretes que C3 sur les memes cellules, et
> son rapport groupe sur personne est PLUS ELEVE, parce qu'un modele prive de
> l'information propre a la personne retombe sur la regularite de groupe meme sans
> etiquette demographique.
>
> **Si H2 seule est vraie** : le taux de fausses raretes et le rapport groupe sur personne
> ne bougent pas, et seule l'exactitude baisse.

**Les sept contrastes declares, tous C3F moins C3, memes cellules, memes personnes.**

| | mesure | nombre de tests |
|---|---|---|
| **P1** | exactitude argmax | 1 |
| **P2** | taux de fausses raretes, part des raretes osees posees sur une personne majoritaire | 1 |
| **P3** | rappel des cellules minoritaires | 1 |
| **P4** | precision des cellules minoritaires | 1 |
| **P5** | H1b, rarete reelle de la PERSONNE, moyenne sur les fausses raretes | 1 |
| **P6** | H2b, rarete reelle du SEGMENT ideologique sur cet item, moyenne sur les fausses raretes | 1 |
| **P7** | H2a, part des fausses raretes egales a la modalite rare modale du segment | 1 |

**Famille primaire declaree : P1 a P7, 7 tests, Holm.** **Famille secondaire declaree** :
l'exces contre le **temoin aveugle a la personne** de a31, pour chacune des deux conditions
et chacun des deux cotes, **4 tests, Holm separement**. Benjamini Hochberg est rapporte a
cote des deux. Tous les p sont des p de bootstrap apparie sur les 60 personnes, 4 000
tirages, lus sur la position de zero dans la distribution ; ils ne descendent jamais sous
1/4 000 = 0,00025, donc le plancher de Holm vaut **0,00175** sur la famille primaire et
**0,001** sur la secondaire.

**N'entrent dans aucune famille**, et sont des descriptions : le rapport groupe sur
personne et les lifts, qui sont des rapports a un temoin et non des quantites testees ; le
seuil de 20 pour cent ; la reference de minorite calculee sur les 150 ; le detail par
famille thematique ; la taille et la rarete du contexte reellement vu ; les quintiles ; la
confiance et l'entropie des distributions ; le controle B2 famille retiree ; les deux
mesures par cellule ajoutees apres coup, signalees post hoc ; et toutes les lignes des
conditions autres que C3 et C3F, qui sont des points de repere sur les memes cellules.

### 0.1 Cinq controles executes avant toute lecture

[MESURE, `a33-controles.csv`]

1. **La trace C3F porte 3 498 appels, 61 personnes, 58 items.** Une personne n'a que 18
   appels, le run s'est arrete sur la fin dure au milieu d'elle ; **elle est ecartee**. Il
   reste **60 personnes completes a 58 items**, soit 3 480 appels exactement. Les 58 items
   de la trace sont exactement les 58 items des six familles de `a2_baselines_gss`.
2. **C3 restreinte aux 58 items et aux 150 personnes du run redonne 0,6249**, c'est a dire
   au dix millieme le chiffre de a23 cite par l'addendum 06:25 de
   `SYNTHESE-NUIT-2026-09-08.md`. La chaine de lecture des traces n'a pas bouge.
3. **`B2 famille retiree` recalculee ici redonne 0,662105 sur les 1 052 personnes**, avec
   un ecart de **0,000000** a la valeur publiee dans `a8-familles-gss.csv`. Voir la
   section 7 pour ce que cela implique sur la reutilisation de a8.
4. **La reference de minorite du perimetre**, calculee sur les 1 052 : **21 des 58 items
   portent au moins une modalite minoritaire, et aucun n'en porte deux**. Le test P7 est
   donc **non evaluable** ; il recoit p = 1 par la convention conservatrice de a31, ce qui
   ne peut pas creer de fausse decouverte et n'allege pas la correction des six autres.
5. **Les 60 personnes de C3F viennent des plis 0 et 1 uniquement**, 30 par pli. Le run est
   ordonne personne par personne et s'est arrete avant les plis 2, 3 et 4. La comparaison
   appariee C3 contre C3F n'en souffre pas, ce sont les memes personnes des deux cotes ;
   la generalisation aux 1 052 en souffre, et c'est porte en section 11.

### 0.2 Deux ecarts a l'addendum 06:25, verifies et expliques

[MESURE, `a33-controles.csv`]

L'addendum de `SYNTHESE-NUIT-2026-09-08.md` donne C3F a **0,5617** et une diversite
conservee de **56,6 pour cent**. Les deux chiffres sont reproduits ici a l'identique en
refaisant le calcul comme `a5_evaluer` le fait, et les deux ecarts avec le present rapport
sont mecaniques.

- **0,5617 contre 0,5572.** `a5_evaluer` retient toute personne portant au moins une
  prediction, donc **61 personnes**, y compris celle qui n'a que 18 items. Ce rapport
  garde les **60 completes**. Les 0,5572 sont la valeur sur les 60.
- **56,6 pour cent contre 59,0 pour cent.** `a5_evaluer` compare l'entropie des
  predictions de 60 personnes a l'entropie des reponses de **150** humains, parce que sa
  population de reference est l'union des traces. Sur les **memes 60 personnes des deux
  cotes**, la diversite conservee de C3F vaut **0,5898**. C'est la valeur a employer
  desormais pour comparer C3F a C3, qui vaut **0,6582** sur ce meme perimetre.

**Ce n'est pas une erreur de l'addendum**, qui signalait lui meme sa comparaison comme
indicative ; c'est la meme quantite mesuree sur deux denominateurs.

---

## 1. Ce que C3F ampute exactement, et ce qu'il n'ampute pas

[MESURE, `a33-contexte.csv` et `a33-cousins.csv`]

| condition | contexte du prompt systeme | items de contexte, moyenne | cousins de famille vus, moyenne | rarete moyenne du contexte |
|---|---|---|---|---|
| **C3** | 149 items moins le bloc secret | **119,2** | **8,72** | 0,0359 |
| **C3F** | 149 items moins la famille entiere | **137,3** | **0,00** | 0,0364 |

**Il faut lire ce tableau avant tout le reste, parce qu'il contredit l'intuition portee
par le mot « ampute ».** Le decoupage du run a5 retire du contexte de C3 le **bloc secret
entier**, 29 ou 30 items tires au hasard ; le decoupage de C3F retire la **famille
entiere**, 5 a 17 items selon la famille. **C3F voit donc dix huit items de plus que C3 en
moyenne.** La rarete moyenne du contexte, qui est la covariable de H5 dans a31, est meme
imperceptiblement plus haute pour C3F, 0,0364 contre 0,0359.

**Ce qui est retire n'est pas de la quantite, c'est de la proximite.** C3 voit en moyenne
8,72 cousins thematiques de la question posee, de 3,20 pour la famille « fin de vie » a
13,06 pour la famille « depenses publiques ». C3F en voit zero, par construction, et le
controle de a5 section 4.5 avait deja verifie sur 116 prompts que ni l'item cible ni aucun
de ses cousins n'apparait dans le texte du prompt systeme.

**Consequence de methode, et elle est importante pour la suite.** C3F ne teste donc pas
« moins de contexte », il teste « le contexte le plus informatif retire ». C'est un test
plus severe et plus interessant que la version quantitative de H5, mais **ce n'est pas
exactement la version de H5 que a31 a declaree**, qui portait sur la richesse en raretes
du contexte. Le present rapport tranche la version qualitative ; la version quantitative
reste sans condition experimentale dediee.

---

## 2. Le resultat principal : les sept contrastes declares

[MESURE, `a33-contrastes.csv`, famille primaire, 7 tests, Holm, bootstrap apparie sur les
60 personnes, 4 000 tirages]

| test | C3 | C3F | **C3F moins C3** | IC 95 % | p brut | **p Holm** | p BH |
|---|---|---|---|---|---|---|---|
| **P1 exactitude** | **0,6195** | **0,5572** | **moins 0,0624** | **[moins 0,0828 ; moins 0,0422]** | 0,00025 | **0,00175** | 0,00088 |
| P2 taux de fausses raretes | 0,8261 | 0,8671 | plus 0,0411 | [moins 0,0090 ; plus 0,0865] | 0,119 | 0,593 | 0,207 |
| P3 rappel des minorites | 0,2151 | 0,2043 | moins 0,0108 | [moins 0,0656 ; plus 0,0516] | 0,857 | 1,000 | 0,999 |
| P4 precision des minorites | 0,1739 | 0,1329 | moins 0,0411 | [moins 0,0865 ; plus 0,0090] | 0,119 | 0,593 | 0,207 |
| P5 H1b rarete de la personne | 0,0414 | 0,0387 | moins 0,0027 | [moins 0,0076 ; plus 0,0023] | 0,303 | 0,908 | 0,424 |
| **P6 H2b rarete du segment** | **0,0714** | **0,0580** | **moins 0,0135** | **[moins 0,0207 ; moins 0,0064]** | 0,00025 | **0,00175** | 0,00088 |
| P7 H2a modale rare du segment | non evaluable | non evaluable | sans objet | sans objet | 1,000 | 1,000 | 1,000 |

**Ce que le tableau dit, dans l'ordre.**

1. **L'ablation mord sur l'exactitude, et c'est le resultat le plus solide du rapport.**
   Six points et quart, intervalle entierement negatif, p au plancher de la correction.
   C3F passe **sous la modalite majoritaire**, `B0 mode` a 0,6376 sur les memes cellules,
   et loin sous `B2 argmax` a 0,7086 et sous `B2 famille retiree` a 0,6822. Le regime
   « question jamais posee dans ce domaine » n'est pas un terrain ou notre agent local de
   4 milliards de parametres gagne, ce que l'addendum 06:25 disait deja et que ce rapport
   confirme sur des cellules appariees [MESURE, `a33-mesures.csv`].
2. **P2 et P4 sont le meme test au signe pres, et il faut le dire.** Sur ce perimetre
   aucun item ne porte deux modalites minoritaires, donc le compte « mauvaise modalite
   rare » vaut **zero pour toutes les conditions**, et par consequent
   `precision = 1 moins taux de fausses raretes` exactement. Les deux lignes ne portent
   qu'une seule information. **La correction de Holm sur 7 tests dont deux sont
   parfaitement redondants et un est non evaluable est conservatrice** ; elle ne peut pas
   avoir masque un effet, elle a seulement rendu la decision plus exigeante.
3. **Le taux de fausses raretes ne se decide pas.** Le point estime va dans le sens de H5,
   plus 4,1 points, mais l'intervalle contient zero et le p ajuste vaut 0,59. Avec 115 et
   143 raretes osees, la puissance est faible : ce n'est pas « H5 est refutee sur ce
   point », c'est **« ce perimetre ne tranche pas ce point »**, et la section 11 le porte.
4. **Le rappel ne bouge pas du tout.** 0,215 contre 0,204, intervalle large et centre sur
   zero. Retirer la famille du contexte ne fait pas perdre les minorites que le modele
   trouvait : il en trouve 19 au lieu de 20 sur 93.

---

## 3. La rarete de groupe baisse au lieu de monter

### 3.1 Le contraste declare, P6

[MESURE, `a33-contrastes.csv` et `a33-mesures.csv`]

La mesure est celle de a31 section 2.2 : la rarete reelle du segment ideologique de la
personne **sur cet item la**, calculee sur les humains de la vague 1 sans la personne elle
meme, moyennee sur les fausses raretes.

| condition | fausses raretes | rarete du segment aux fausses raretes | IC 95 % | temoin aveugle | **lift groupe** | IC du lift |
|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***30*** | ***0,1033*** | ***[0,075 ; 0,135]*** | ***0,0702*** | ***plus 0,47*** | ***[plus 0,14 ; plus 0,83]*** |
| **C3, contexte complet** | **95** | **0,0714** | **[0,058 ; 0,088]** | **0,0597** | **plus 0,20** | **[plus 0,06 ; plus 0,33]** |
| **C3F, famille retiree** | **124** | **0,0580** | **[0,045 ; 0,073]** | **0,0528** | **plus 0,10** | **[moins 0,04 ; plus 0,24]** |
| C2, etiquette demographique | 87 | 0,1681 | [0,111 ; 0,206] | 0,0648 | plus 1,59 | [plus 0,95 ; plus 2,10] |
| B2 famille retiree | 3 | 0,1752 | [0,151 ; 0,210] | 0,0764 | plus 1,29 | [plus 0,70 ; plus 2,26] |

**Priver le modele de la famille ne le fait pas retomber sur le groupe, cela l'en
eloigne.** La quantite testee baisse de 0,0135, intervalle entierement negatif, p ajuste
0,00175. Le lift de groupe passe de plus 0,20 a plus 0,10, et l'intervalle du lift de C3F
recouvre zero alors que celui de C3 ne le recouvre pas.

**La famille secondaire declaree le dit une seconde fois, contre un temoin different**
[MESURE, 4 tests, Holm separement] :

| condition | cote | exces sur le temoin aveugle a la personne | IC 95 % | p brut | p Holm |
|---|---|---|---|---|---|
| **C3** | **groupe, H2b** | **plus 0,0117** | **[plus 0,0033 ; plus 0,0215]** | 0,0040 | **0,016** |
| C3 | personne, H1b | plus 0,0057 | [plus 0,0004 ; plus 0,0108] | 0,027 | 0,081 |
| C3F | groupe, H2b | plus 0,0052 | [moins 0,0021 ; plus 0,0137] | 0,172 | 0,343 |
| C3F | personne, H1b | plus 0,0030 | [moins 0,0014 ; plus 0,0075] | 0,202 | 0,343 |

**C3, avec sa famille dans le contexte, place ses fausses raretes sur des cellules ou le
groupe est reellement plus souvent rare, et cela passe la correction. C3F ne le fait
plus.** Les deux cotes de C3F sont indecidables.

### 3.2 Comment lire ce signe, sans le sur interpreter

Le sens le plus simple est arithmetique et il faut le donner en premier. **C3F pose 29
fausses raretes de plus que C3, et il les pose ailleurs** : 83 de ses 124 fausses raretes
tombent sur la famille des depenses publiques `nat*`, contre 59 sur 95 pour C3
[MESURE, `a33-par-famille.csv`]. Le temoin aveugle a la personne, qui est apparie item par
item sur la composition en items, baisse lui aussi, de 0,0597 a 0,0528. **Une partie de la
baisse du lift est donc un deplacement du poids vers des items ou la rarete de segment est
plus faible, pas un changement de comportement du modele a item constant.** C'est la
limite principale de la section 3 et elle est portee en section 11.

Ce qui reste vrai apres cette reserve, parce que le test porte sur la valeur et non sur le
lift : **la quantite declaree baisse, et la prediction de H5 annoncait qu'elle monterait.**
Sur ce point la, H5 n'est pas seulement indecidable, elle est prise a contre pied.

---

## 4. Le rapport groupe sur personne n'est pas identifiable sur 60 personnes

[MESURE, `a33-leviers-personne-segment.csv` et `a33-mesures.csv`, IC bootstrap sur les
personnes]

C'est la mesure que a31 propose comme quantite du papier et comme critere de reussite de
la nuit de calcul. Sur le perimetre apparie, elle ne dit rien.

| condition | lift PERSONNE | IC | lift GROUPE | IC | **rapport groupe sur personne** | **IC du rapport** |
|---|---|---|---|---|---|---|
| ***humains vague 2*** | ***plus 0,55*** | ***[0,17 ; 0,88]*** | ***plus 0,47*** | ***[0,14 ; 0,83]*** | ***0,86*** | ***[0,22 ; 2,74]*** |
| **C3** | **plus 0,16** | **[0,01 ; 0,29]** | **plus 0,20** | **[0,06 ; 0,33]** | **1,22** | **[0,22 ; 8,30]** |
| **C3F** | **plus 0,08** | **[moins 0,04 ; 0,21]** | **plus 0,10** | **[moins 0,04 ; 0,24]** | **1,17** | **[moins 9,17 ; 10,78]** |
| C2 | plus 0,21 | [moins 0,21 ; 0,70] | plus 1,59 | [0,95 ; 2,10] | 7,44 | [moins 63 ; 78] |
| agents composite | plus 0,42 | [0,07 ; 0,75] | plus 0,76 | [0,42 ; 1,10] | 1,80 | [0,67 ; 8,92] |
| B2 famille retiree | moins 0,18 | [moins 0,63 ; 0,24] | plus 1,29 | [0,70 ; 2,26] | sans objet | sans objet |

**Trois lectures, et la troisieme est la seule qui compte.**

1. Le classement qualitatif de a31 se retrouve : C2, qui recoit l'etiquette, est tres haut
   du cote du groupe, plus 1,59, et les humains sont la seule ligne sous 1. **C'est un
   accord et non une replication** : le perimetre, le denominateur et la reference de
   minorite ne sont pas ceux de a31.
2. Sur ce perimetre, **C3 est a 1,22 et non a 0,44 comme dans a31**. La difference n'est
   pas un desaccord, c'est un changement de perimetre : 58 items au lieu de 149, 60
   personnes au lieu de 150, reference de minorite sur les 1 052 au lieu des 150. **Les
   deux chiffres ne doivent pas etre compares.**
3. **Les intervalles rendent le rapport inutilisable ici.** Celui de C3F contient zero et
   des valeurs des deux signes. La prediction « si H5, le rapport monte » **ne peut donc
   pas etre testee sur ce perimetre**, et c'est la reponse honnete a cette moitie de la
   question : elle est tranchee par P6, la quantite testee, et pas par le rapport.

---

## 5. Ce que l'amputation fait au modele : il hesite plus et il converge plus

[MESURE, `a33-confiance.csv` et `a33-mesures.csv`, distributions completes lues dans les
traces]

| condition | type de cellule | n | p max moyen | part a p max > 0,99 | entropie moyenne, bits |
|---|---|---|---|---|---|
| C3 | cellule ou aucune rarete n'est osee | 3 365 | 0,9781 | **0,8449** | 0,0781 |
| C3 | rarete juste | 20 | 0,9895 | 0,8500 | 0,0556 |
| C3 | fausse rarete | 95 | 0,9317 | 0,6842 | 0,2239 |
| **C3F** | cellule ou aucune rarete n'est osee | 3 337 | 0,9457 | **0,6503** | 0,1875 |
| **C3F** | rarete juste | 19 | 0,9384 | 0,4211 | 0,2640 |
| **C3F** | fausse rarete | 124 | 0,9022 | **0,3871** | 0,3507 |

**Trois faits.**

1. **Retirer la famille fait plus que doubler l'entropie moyenne du modele**, de 0,082 a
   0,194 bits sur l'ensemble des cellules, et fait tomber la part de cellules quasi
   certaines de 0,845 a 0,650 sur les cellules ou il n'ose aucune rarete. Le modele
   **hesite**, et c'est ce qui explique qu'il ose 143 raretes au lieu de 115.
2. **La hierarchie de H4 se reproduit une troisieme fois, avec le meme signe inverse.**
   Dans les deux conditions, la part de cellules quasi certaines decroit des cellules sans
   rarete vers les raretes justes puis vers les fausses raretes. a31 section 4 avait
   etabli ce signe sur C2 et C3 ; C3F, qui n'etait pas dans a31, le refait :
   0,650 puis 0,421 puis 0,387. **La fausse rarete vient toujours du regime ou le modele
   est le moins sur.**
3. **Et pourtant la population simulee devient MOINS variee, pas plus.** La part de
   diversite humaine conservee passe de **0,6582 pour C3 a 0,5898 pour C3F**, et l'accord
   par paires monte de 0,6923 a 0,7119 sur les memes cellules et les memes 60 personnes
   [MESURE]. **Le modele hesite davantage appel par appel et rend des reponses plus
   semblables d'une personne a l'autre.** Les deux faits ne se contredisent pas :
   l'entropie de la distribution rendue et la dispersion des argmax entre les personnes
   sont deux quantites differentes, et c'est exactement la distinction que a0 et a5
   portent depuis le debut du projet. Pour la these du projet, c'est le point le plus
   utile de cette section : **priver le modele de l'information la plus proche de la
   personne ecrase la variance de la population au lieu de la liberer.**

---

## 6. Famille par famille

[MESURE, `a33-par-famille.csv`, memes 60 personnes, memes cellules]

| famille | items | cousins vus par C3 | C3 | C3F | **baisse, points** | B2 famille retiree | B0 mode | humains vague 2 |
|---|---|---|---|---|---|---|---|---|
| avortement `ab*` | 7 | 4,86 | 0,8286 | 0,7071 | **moins 12,1** | 0,8690 | 0,7976 | 0,9143 |
| depenses publiques `nat*` | 17 | 13,06 | 0,5196 | 0,4255 | **moins 9,4** | 0,6431 | 0,5824 | 0,7373 |
| fin de vie | 5 | 3,20 | 0,7667 | 0,6867 | moins 8,0 | 0,7633 | 0,7200 | 0,8800 |
| libertes civiles | 11 | 8,18 | 0,8106 | 0,7545 | moins 5,6 | 0,7955 | 0,7864 | 0,8455 |
| roles de genre `fe*` | 5 | 3,60 | 0,4733 | 0,4533 | moins 2,0 | 0,4900 | 0,4767 | 0,6567 |
| confiance `con*` | 13 | 9,69 | 0,4756 | 0,4718 | moins 0,4 | 0,5795 | 0,5282 | 0,7051 |

**La baisse est presente dans les six familles**, ce que l'addendum 06:25 disait deja sur
un perimetre non apparie, moins 4,7 a moins 10 points ; sur les cellules appariees
l'amplitude va de moins 0,4 a moins 12,1 points.

**Elle n'est pas expliquee par le nombre de cousins retires**, correlation de rang entre
le nombre de cousins vus par C3 et la baisse : **moins 0,03 sur six familles** [MESURE,
hors famille, six points, aucun test]. La famille qui perd le plus, l'avortement, est
celle ou C3 voyait le MOINS de cousins apres la fin de vie ; celle qui ne perd rien, la
confiance dans les institutions, est celle ou C3 en voyait presque dix. **Ce que le
contexte thematique apporte depend du contenu de la famille et pas de sa taille**, ce qui
est [PROBABLE] et non mesure : six familles ne permettent pas de trancher.

**C3F ne passe au dessus de `B0 mode`, la modalite majoritaire, dans AUCUNE des six
familles**, la ou C3 y passe dans trois, l'avortement, la fin de vie et les libertes
civiles [MESURE]. La lecture de l'addendum tient et se durcit : « le regime question
jamais posee dans ce domaine n'est pas un terrain ou l'agent local de 4 milliards gagne,
il y perd contre la modalite majoritaire », et sur des cellules appariees il y perd
partout.

---

## 7. Le controle B2 famille retiree, et ce que le script de a8 permet

**Le script `analyses/a8_familles.py` ne permet PAS de restreindre son calcul a un sous
ensemble de personnes sans modification.** Sa fonction `gss()` rend des lignes d'agregats
deja calculees sur les 1 052 personnes et ne rend aucune matrice de prediction ; son
argument de perimetre n'existe pas. **Conformement a la consigne, je le dis plutot que de
le modifier.**

**Ce qui a ete fait a la place, et pourquoi c'est licite.** La prediction
`B2 famille retiree (argmax)` a ete **reconstruite** dans `a33_commun.b2_famille_retiree`
a partir des memes primitives importees telles quelles, `a2_commun.en_codes`,
`distance_hamming` et `b2_voisins`, avec les memes plis, le meme K de 30 et la meme graine
que `a8_commun`. Le point de methode qui rend la reconstruction exacte est le suivant :
**`b2_voisins` en mode argmax ne consomme pas le generateur aleatoire**, la matrice
obtenue ne depend donc pas de l'ordre des tirages de a8, qui differe du notre puisque nous
ne recalculons ni B0 ni B1.

**Le controle le verifie et il est au zero.** L'exactitude de la matrice reconstruite sur
les 1 052 personnes et les 58 items vaut **0,662105**, contre **0,662105** publie dans
`a8-familles-gss.csv`, **ecart 0,000000** [MESURE, `a33-controles.csv`].

**Ce que ce controle apporte au rapport.** Sur les memes 60 personnes et les memes
cellules, `B2 famille retiree` est a **0,6822**, contre 0,5572 pour C3F, soit
**12,5 points au dessus**. La cible de 0,6621 citee par l'addendum etait celle des 1 052
personnes ; sur les 60 personnes du perimetre la cible est plus haute encore. **Un plus
proches voisins prive lui aussi de la famille bat notre agent local de langage prive de la
famille, largement.** L'objection 1 de a17 sur a8 se referme dans le sens defavorable au
modele de langage, pour ce modele, et cette fois sur des cellules appariees.

**Un fait a ne pas sur interpreter** : `B2 famille retiree` n'ose presque jamais une
rarete, 4 raretes osees sur 3 480 cellules contre 143 pour C3F. Sa bonne exactitude est
achetee par l'abstention, ce que a29 et l'arbitrage disent deja de toutes les methodes
statistiques. **Le classement en exactitude et le classement en minorites restent opposes**
[MESURE, `a33-mesures.csv`].

---

## 8. Verdict sur H5, et ce que cela permet de corriger

| | prediction de H5 | mesure | verdict |
|---|---|---|---|
| plus de fausses raretes parmi les raretes osees | oui | plus 0,041 [moins 0,009 ; plus 0,087], p ajuste 0,59 | **indecidable, et le point estime seul ne suffit pas** |
| rapport groupe sur personne plus eleve | oui | 1,22 vers 1,17, IC [moins 9,17 ; 10,78] | **non identifiable sur 60 personnes** |
| quantite de groupe, H2b, plus haute | oui | **moins 0,0135 [moins 0,0207 ; moins 0,0064], p ajuste 0,00175** | **CONTREDITE, signe inverse** |
| quantite de personne, H1b, inchangee ou plus basse | oui | moins 0,0027 [moins 0,0076 ; plus 0,0023] | compatible, indecidable |
| exactitude en baisse | prediction commune aux deux | **moins 0,0624, p ajuste 0,00175** | **CONFIRMEE** |

**Verdict : H5 CONTREDITE dans sa forme testable, et pour la premiere fois par une
condition qui fait varier le contexte a personne constante.** a31 la declarait
« contredite dans sa forme quantitative, indecidable par le test declare ». Le present
rapport remplace « indecidable » par une mesure : l'ablation de contexte la plus severe
dont nous disposons **degrade l'exactitude sans deplacer la fausse rarete vers le groupe**.

**Ce que cela permet de corriger, en une phrase : enrichir le contexte n'est toujours pas
un correctif de la fausse rarete, et appauvrir le contexte n'en est pas la cause.** Le
seul levier mesure du dossier reste le retrait de l'etiquette, mesure en a31 section 6.2.

**Ce que cela interdit d'ecrire.**

1. **Interdit d'ecrire que la fausse rarete vient du manque d'information sur la
   personne.** [MESURE] A personne constante, retirer la famille thematique entiere du
   contexte ne deplace pas la fausse rarete vers la rarete de groupe ; la quantite testee
   va dans l'autre sens.
2. **Interdit d'ecrire que C3F est une condition a contexte plus pauvre.** [MESURE] C3F
   voit 137,3 items contre 119,2 pour C3. Ce qu'il perd, ce sont les 8,72 cousins
   thematiques.
3. **Interdit d'employer le rapport groupe sur personne sur ce perimetre.** [MESURE] Son
   intervalle bootstrap couvre les deux signes pour C3F.
4. **Interdit de conclure que le taux de fausses raretes est inchange.** [MESURE] Il n'est
   pas mesure comme inchange, il est **indecidable** avec 115 et 143 raretes osees. La
   distinction compte pour un relecteur adverse.

---

## 9. La figure

`a33-figure-c3f.png` et `.svg`, quatre panneaux, produits par `a33_figure.py` qui ne
recalcule rien et lit les tableaux.

- **Panneau 1** : l'exactitude famille par famille, la fleche allant du contexte complet
  au contexte ampute, avec le nombre moyen de cousins que C3 voyait a droite. La fleche
  pointe vers la gauche dans les six familles, et sa longueur ne suit pas le nombre de
  cousins.
- **Panneau 2** : les sept contrastes declares et les deux descriptions post hoc, avec
  leur intervalle bootstrap. Deux seulement s'ecartent de zero apres Holm, l'exactitude et
  la rarete de groupe, et les deux vont vers la gauche.
- **Panneau 3** : le depart entre H1 et H2, lift du cote de la personne contre lift du
  cote du groupe, avec les deux intervalles. C2 et `B2 famille retiree` sont en haut a
  gauche, les humains sur la diagonale, C3 et C3F au centre avec des intervalles qui se
  recouvrent : c'est le panneau qui montre que le rapport n'est pas identifiable ici.
- **Panneau 4** : le taux de fausses raretes par quintile de rarete du contexte
  reellement vu, hors du bloc secret pour C3 et hors de la famille pour C3F, avec le
  nombre de raretes osees sous chaque point. Le taux est plat sur les quatre premiers
  quintiles pour les deux conditions et ne baisse qu'au cinquieme, exactement comme en a31
  section 5 sur un tout autre decoupage.

---

## 10. Ce que cela change a `ARBITRAGE.md`

**Rien de la phrase a defendre, et c'est le resultat utile.** L'option A et la phrase de
la section « Mon avis » reposent sur le mecanisme H2, la substitution du groupe a la
personne par l'etiquette. Ce rapport a cherche l'explication concurrente, le manque de
contexte, avec la seule condition capable de la tester, **et ne l'a pas trouvee**. La
phrase resiste a une tentative serieuse de refutation, ce qu'elle ne pouvait pas encore
dire ce matin.

**Une ligne peut etre ajoutee a la liste « ce qui est tombe aujourd'hui, pour ne plus le
dire »** :

> « La fausse rarete vient d'un contexte trop pauvre. » Faux, teste a personne constante :
> retirer du prompt la famille thematique entiere de la question coute six points
> d'exactitude et fait baisser, pas monter, la part de rarete de groupe des fausses
> raretes.

**Et une precision est a apporter au second travail, « si un modele plus gros ou non
aligne fait la meme substitution ».** a31 proposait de surveiller le rapport groupe sur
personne pendant la nuit de calcul. **Ce rapport montre que ce rapport n'est pas mesurable
sur 60 personnes**, intervalle [moins 9,17 ; 10,78], et de justesse sur 150. La quantite a
surveiller doit etre **la valeur H2b et son exces sur le temoin aveugle**, qui est testee
directement et qui separe deja C3 de C3F, et non le rapport de deux lifts. C'est une
correction de protocole a porter avant de lancer la nuit de calcul, pas apres.

---

## 11. Ce que je n'ai pas pu verifier

1. **Soixante personnes, et elles ne sont pas un echantillon des 150.** Le run C3F s'est
   arrete sur la fin dure et n'a couvert que les plis 0 et 1, 30 personnes chacun. La
   comparaison appariee C3 contre C3F n'en souffre pas, mais **toute generalisation aux
   1 052 personnes en souffre**, et les puissances s'en ressentent : P2 aurait besoin
   d'environ quatre fois plus de raretes osees pour trancher un ecart de quatre points.
   La suite est ecrite et chiffree dans l'addendum 06:25 : environ 2 h 10 de calcul, seul
   sur la machine, pour finir les 90 personnes manquantes.
2. **Une seule passe.** C3F n'a que la passe 1, l'ordre de nomenclature. C3 aussi sur ce
   perimetre, la comparaison est donc equitable, mais **le biais de position n'est neutre
   dans aucune des deux** et la passe 2 n'a jamais tourne pour aucune des deux.
3. **Le deplacement du poids d'item entre les deux conditions.** Le temoin aveugle est
   apparie item par item, mais C3F pose 83 de ses 124 fausses raretes sur la famille
   `nat*` contre 59 sur 95 pour C3. Une partie de la baisse du lift de groupe est donc un
   effet de composition et non un changement de comportement a item constant. Le test P6
   porte sur la valeur et non sur le lift, ce qui le protege en partie seulement.
4. **P7 n'a pas pu etre teste.** Aucun des 58 items de famille ne porte deux modalites
   minoritaires au seuil de 10 pour cent sur les 1 052. Les 19 items multimodalites de a31
   sont tous hors des six familles, `income`, `wrkstat`, `attend`, `jew`, `hunt1`,
   `union1`. **Le choix de la modalite rare est donc structurellement hors d'atteinte de
   C3F**, quelle que soit la taille de l'echantillon.
5. **La version quantitative de H5 reste sans condition dediee.** C3F retire la proximite
   thematique, pas la quantite d'information : il voit meme dix huit items de plus que C3.
   Une condition qui retirerait N items tires au hasard, N variant, testerait le volume ;
   elle n'existe pas et couterait une nuit de calcul.
6. **Une reference de minorite differente de a29 et a31.** Elle est calculee sur les 1 052
   et non sur le perimetre. Les deux sensibilites de `a33-sensibilites.csv` montrent que
   les conclusions qualitatives tiennent au seuil de 20 pour cent et avec la reference sur
   les 150, mais **les valeurs bougent beaucoup**, et le rapport groupe sur personne de
   C3F va de 0,07 a 1,17 selon la variante. Une raison de plus de ne pas s'en servir.
7. **Un seul axe pour la rarete de groupe.** L'ideologie politique, comme en a31, pour la
   meme raison et avec la meme limite.
8. **Un seul modele, un seul run, 4 milliards de parametres, une seule formulation
   d'invite.** La limite ouverte de a23 sur la formulation vaut mot pour mot, et rien ici
   ne permet de conclure sur les modeles en general.
9. **La longueur du prompt n'est pas controlee.** Le prompt de C3F est plus long que celui
   de C3, environ 5 280 tokens contre 4 600, parce qu'il contient plus d'items. Les deux
   tiennent dans les 8 192 tokens du slot, mais **je n'ai pas mesure si la degradation
   d'exactitude tient a l'absence des cousins ou a la longueur**. Le controle propre
   serait une condition a longueur egale et famille presente.
10. **Twin-2K-500.** Toute l'analyse porte sur le GSS, comme a29 et a31.

---

## 12. Questions ouvertes pour Simon

1. **Faut il finir C3F sur les 150 personnes avant de publier quoi que ce soit de cette
   section ?** Deux heures dix de calcul selon l'addendum. Le gain porte sur P2, le taux
   de fausses raretes, qui est le seul point ou le rapport dit « indecidable » la ou un
   relecteur adverse voudra lire « refute ». Les autres conclusions ne bougeront pas.
2. **La quantite a surveiller pendant la nuit de calcul doit elle changer ?** a31
   proposait le rapport groupe sur personne. Ce rapport montre qu'il n'est pas mesurable
   a ces tailles d'echantillon. Je propose l'exces H2b sur le temoin aveugle, teste
   directement, avec son intervalle. Faut il acter ce changement dans le protocole de la
   nuit ?
3. **Le fait le plus vendeur du rapport n'est pas celui qui etait demande.** Priver le
   modele de l'information la plus proche le fait **hesiter davantage appel par appel**,
   entropie de 0,082 a 0,194 bits, **et rendre une population MOINS variee**, diversite
   conservee de 0,658 a 0,590, accord par paires de 0,692 a 0,712. C'est un enonce
   directement utile a la these « ce que la simulation efface ». Faut il lui donner une
   sous section dans le papier, ou reste t il un resultat de service ?
4. **Faut il ecrire quelque part que C3F voit PLUS d'items que C3 ?** C'est contre
   intuitif, c'est une consequence du decoupage en blocs de a2, et un relecteur qui ne le
   sait pas lira « contexte ampute » comme « contexte plus pauvre ». Je l'ai mis en
   section 1 ; faut il aussi corriger l'addendum 06:25, qui ne le dit pas ?
5. **Que faire de la comparaison C3F contre `B2 famille retiree` ?** Douze points et demi
   d'ecart en faveur du plus proches voisins sur les memes cellules, avec 4 raretes osees
   contre 143. C'est l'illustration la plus nette du compromis exactitude contre minorites
   de tout le dossier. Merite t elle une figure a elle, ou est ce deja dit par a29 ?
6. **L'addendum 06:25 doit il etre corrige sur les deux chiffres de la section 0.2 ?**
   0,5617 vient de 61 personnes dont une incomplete, et la diversite de 56,6 pour cent
   compare 60 personnes simulees a 150 humains. Les valeurs appariees sont 0,5572 et
   0,5898. Ce sont des ecarts petits mais ce sont des ecarts.

---

## Rejouer

```
.venv/bin/python analyses/a33_contexte_rarete.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 4000
.venv/bin/python analyses/a33_figure.py
```

Les deux caches sont ceux de a25 et de a28, les memes que a28, a29 et a31. S'ils manquent,
ils sont reconstruits. Duree totale : environ 5 secondes pour `a33_contexte_rarete`,
reconstruction de `B2 famille retiree` comprise, et 3 secondes pour la figure, sur quatre
coeurs. Graine d'analyse 20260908 partout, graine de grille 20260903, celle du run
a5.
