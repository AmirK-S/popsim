# R2, resultats. La comparaison appariee sur les gens rares, en regime severe

Rapport du 9 septembre 2026, ecrit apres le run et apres l'evaluation. Il execute le
**verrou 1** de `MODELE-DU-MONDE.md` section 10.5 et il rend compte contre la page de plan
`resultats/r2-preenregistrement.md`, **horodatee du 8 septembre 2026 a 22:05:00 CEST**,
ecrite avant le moindre appel de modele de langage et non modifiee depuis. En cas de
divergence, la page de plan fait foi contre ce rapport.

Aucun fichier existant n'a ete modifie pour ecrire ce rapport. Les mesures viennent de
`analyses/r2_evaluer.py`, rejoue sur les traces definitives sous le suffixe `-def`, et d'un
script complementaire nouveau, `analyses/r2b_puissance.py`, qui n'ecrit que des fichiers
`r2b-*`. Zero appel de modele de langage dans les deux.

---

## Reponse en une ligne

**Le verrou 1 se ferme dans le sens negatif : sur les memes personnes et les memes cellules,
la famille thematique entiere retiree des deux cotes, un jumeau de langage de 20 milliards de
parametres ne retrouve pas les gens rares reels mieux qu'un tirage au sort dans le segment de
la personne, et il est derriere l'appariement sur moyenne predite.** L'exces de rappel de
`C3F gpt-oss-20b` sur le plancher de segment, sur les 106 cellules rares stables des 58 items
de famille, vaut **plus 0,0315 [moins 0,0355 ; plus 0,1015]**, p de bootstrap apparie 0,3405,
p ajuste par Holm sur la famille primaire **1,0000** : **H1a echoue**, et c'est le critere de
chute numero 1 de la page de plan, issue 3 de sa section 6 [MESURE, `r2-contrastes-def.csv`,
150 personnes completes, 8 700 appels, zero rejet].

**H1b echoue contre cinq des six methodes du regime severe, et le seul contraste qui passe
est celui contre le plus faible adversaire du jeu.** `C3F gpt-oss` moins
`B2 famille retiree (argmax)` vaut plus 0,1509 [plus 0,0575 ; plus 0,2362], Holm 0,0175 ;
contre `PMM k=10 famille retiree` la difference est **negative**, moins 0,0943
[moins 0,1729 ; moins 0,0099], intervalle non ajuste entierement negatif, Holm 0,2400 ;
contre `IM m=10 mode` moins 0,0094 et contre `E2 famille retiree (tirage)` moins 0,0472
[MESURE]. Dans l'ordre du rappel des raretes stables, le jumeau est **quatrieme sur sept** :
PMM 0,2830, E2 tirage 0,2358, IM mode 0,1981, **jumeau 0,1887**, plancher de segment 0,1644,
E1 argmax 0,1509, B2 tirage 0,1415, B2 argmax 0,0377.

**Sur la precision il est dernier des sept, et decidablement derriere les six, et derriere le
hasard.** 0,0542 contre 0,2190 pour PMM et 0,3478 pour E1 ; les six contrastes H2b passent
Holm dans le sens defavorable, de moins 0,0432 a moins 0,3458 ; et **H2a est le contraste le
plus severe du rapport** : sur les cellules ou le jumeau ose une modalite minoritaire, un
tirage au sort dans le segment de la personne serait juste 0,5796 fois sur une, et le jumeau
l'est 0,0542 fois, exces **moins 0,5254 [moins 0,5671 ; moins 0,4770]**, Holm 0,0018 [MESURE].
Il ose 369 raretes pour en placer 20 justes, quand PMM en ose 137 pour en placer 30.

**Ni l'exactitude ni la structure ne le sauvent, et le passage a 20 milliards de parametres
ne change rien.** Les six contrastes d'exactitude sont negatifs, moins 0,0467 a moins 0,1362,
Holm 0,0015 ; le jumeau conserve 0,4438 de la diversite humaine contre 0,9828 a PMM, six
contrastes de structure a Holm 0,0015 dans le sens defavorable ; il fait **moins bien que la
modalite modale de la population**, 0,5328 contre 0,6205 pour `B0 mode`. Sur les 60 personnes
communes avec la trace Qwen3-4B, **le modele de 20 milliards n'a reduit aucun ecart** : il
perd 0,9 point d'exactitude de plus que le modele de 4 milliards face aux six methodes
(ecart median moins 0,1138 contre moins 0,1046), retrouve 9,7 points de moins de raretes
stables (0,1613 contre 0,2581) et conserve moins de dispersion (0,4340 contre 0,5898), aucune
de ces trois differences n'etant decidable [MESURE, `r2b-pont-modeles.csv`, `r2-croises-def.csv`].

**Ce qui produisait l'avantage est identifie, et ce sont les items cousins.** La meme trace
en condition `C3`, cousins conserves dans l'invite, sur 105 personnes, fait tout ce que la
these annonce : exces sur le plancher plus 0,3491 [plus 0,2368 ; plus 0,4665], Holm 0,0018, et
les **six** contrastes H1b positifs et retenus par Holm, PMM compris, plus 0,1724, Holm 0,0080.
Sur les 105 personnes communes, retirer la famille coute au modele de 20 milliards
**moins 0,0627 d'exactitude** [moins 0,0783 ; moins 0,0473] et **moins 0,2299 de rappel des
raretes stables** [moins 0,3333 ; moins 0,1316], les deux a p 0,00025 [MESURE,
`r2-croises-def.csv`]. Le cout d'exactitude est celui que a33 mesure sur Qwen3-4B, moins
0,0624 : **6,3 points a 20 milliards contre 6,2 a 4 milliards.**

---

## 0. Ce qui a tourne, et ce qui a ete rejoue

| | |
|---|---|
| Modele | **gpt-oss-20b**, GGUF MXFP4, gabarit harmony, coupure **publiee** juin 2024. Le repli `Qwen3-30B-A3B` n'a pas ete employe |
| Sonde de gabarit | variante `answer` 0,9622, variante `brut` 0,9995 ; **`answer` retenue**, comme la page de plan le prescrit des qu'elle atteint 0,90, pour rester comparable a la trace a5 [MESURE, `r2-run.log`] |
| Smoke test | masse mediane 0,9539, minimale 0,9344, modalites absentes 0,00 : **passe**, critere de chute 6 non declenche [MESURE] |
| `C3F gpt-oss-20b` | **150 personnes completes sur 150**, 58 items, **8 700 appels**, **zero rejet**, 1 932 appels par heure, trace close a 03:47 |
| `C3 gpt-oss-20b` | **105 personnes completes**, **6 090 appels**, **zero rejet**, 2 742 appels par heure |
| `C3F Qwen3-4B` | trace a5 existante, 60 personnes completes et une partielle, 3 498 appels |
| Correction | Holm et Benjamini Hochberg **par famille**, sur la definition de rarete du **perimetre** ; la definition sur population est publiee sans correction, comme sensibilite. 26 contrastes corriges par condition, 78 en tout [MESURE, `r2-controles-def.csv`] |

**L'arret n'a pas ete propre, et il faut le dire.** Le SIGINT envoye par la file de nuit a
05:45 n'a pas arrete le processus, qui a continue jusqu'a **06:01**, ou l'orchestrateur l'a
tue et a tue son serveur ; le code de sortie est 137 et `r2-run.log` **ne contient pas** la
ligne `RUN TERMINE`. Consequence pratique : la premiere evaluation, lancee a 05:47, a lu une
trace `C3` encore en ecriture et a compte **95** personnes. **Ce rapport ne repose pas
dessus.** L'evaluation a ete rejouee a 06:02 sur les traces definitives, et publiee sous le
suffixe `-def` pour ne reecrire aucun fichier existant.

**Ce que le rejeu change, et ce qu'il ne change pas** [MESURE] :

- **`C3F gpt-oss` : rien du tout.** Les 26 contrastes de la condition primaire sont
  **identiques a la derniere decimale** entre l'evaluation de 05:47 et celle de 06:02, ecart
  maximal 0,0 sur les differences comme sur les p ajustes. La trace C3F etait close depuis
  03:47 et le verrou 1 n'a jamais dependu de l'arret.
- **`C3` : 95 personnes deviennent 105**, 5 510 appels deviennent 6 090, et les 71 cellules
  rares stables deviennent 87. Toutes les valeurs de C3 citees ici sont celles de 105
  personnes.
- Une consequence operationnelle, resolue depuis : le `llama-server` de PID 4996 a survecu
  au SIGTERM et a bloque la file jusqu'a 06:01. **La note de 05:50 du journal de nuit, qui
  annonce R3 demarre a 05:47, est fausse** : la file a ecrit `FILE TERMINEE` a 06:02 et
  **R3 a reellement demarre a 06:02**, avec son propre serveur, et ecrit
  `data/traces/r3-C3E-qwen4.jsonl` [MESURE, `file-nuit-3.log`, `r3-run.pid`]. Dix sept
  minutes de machine ont ete perdues entre la fin dure annoncee de R2 et le depart de R3.

**Deux ecarts a la page de plan, tous deux dans le decompte des tests, aucun sur le sens
d'une conclusion** [MESURE, lecture de `r2_evaluer.py`] :

1. **F4 annonce 8 tests, quatre methodes a tirage fois deux quantites ; il en compte 6.**
   Le regime severe ne contient que **trois** methodes a tirage, `E2 famille retiree`,
   `PMM k=10 famille retiree` et `B2 famille retiree (tirage)` ; la quatrieme que la page de
   plan comptait, `B0 tirage`, n'est pas une methode du regime severe mais un repere. Holm
   sur 6 est moins exigeant que sur 8 ; les six p de F4 sont au plancher, 0,0015, et la
   conclusion ne peut pas en dependre.
2. **F3 annonce 7 tests ; six sont corriges par Holm et le septieme, H3b, est calcule dans
   `r2-croises-def.csv` sans correction.** H3b vaut moins 0,0092 [moins 0,0270 ; plus 0,0089],
   p 0,317 : non decidable, donc l'absence de correction ne cree aucune decouverte.

Un troisieme ecart, du meme genre et dans le sens conservateur : **F1 et F2 sont declarees
diriges et sont testees avec un p de bootstrap bilateral**, celui de `a34_commun.p_contre_zero`
importe par toute la chaine. Un test dirige serait deux fois plus facile a passer. **Aucun
verdict n'en depend** : le p brut de H1a vaut 0,3405 bilateral, soit environ 0,17 unilateral,
et sept fois 0,17 depasse encore 1 apres Holm [MESURE].

**Les criteres de couverture de la page de plan sont tenus.** Critere 5, « au moins 60
personnes » : C3F en couvre 150 sur 150. Critere 6, smoke test : passe. **Le verrou 1 peut
donc etre conclu**, et il l'est.

---

## 1. Le protocole, rappele

| | |
|---|---|
| Personnes | les 150 de `data/traces/a5-personnes.csv`, 30 par pli, graine 20260907, ecrites avant le premier appel de a5 |
| Items | les **58 items** des six familles thematiques de `FAMILLES` dans `a2_baselines_gss.py`, perimetre exact de a8, a35 section 6 et a41 |
| Condition primaire | **C3F**, contexte egal aux 149 items **moins toute la famille** de l'item cible, aucune demographie, aucune etiquette. C3F voit 137,3 items en moyenne et **zero cousin** (a33) : ce qui est retire est l'information la plus proche, pas la quantite |
| Condition secondaire | **C3**, contexte egal aux 119 items du bloc de a2, **cousins compris**, memes 58 items cibles |
| Cellules jugees | les cellules **minoritaires reelles** au seuil de 10 pour cent que la personne **redonne a l'identique en vague 2**, partition P_A de a42, importee de `a42_commun.classes_stabilite` |
| Plancher | tirage dans la marginale du segment **ideologie x genre x age**, sans la personne, `a34_commun.frequence_segment`, 98 cases [MESURE, controle] |
| Adversaires | les **six** methodes du regime severe de a41, importees et non recopiees : `E1 famille retiree (argmax)`, `E2 famille retiree (tirage)`, `PMM k=10 famille retiree`, `IM m=10 mode, famille retiree`, `B2 famille retiree (argmax)`, `B2 famille retiree (tirage)` |
| Statistique | tous les p sont des p de bootstrap **apparie sur les personnes**, memes 4 000 tirages pour toutes les methodes, plancher du p a 1 sur 4 000 ; contraste a denominateur vide a p = 1 |

**Ce qui rend la comparaison appariee, et c'est tout l'objet de R2.** Les six methodes
statistiques perdent la famille thematique entiere de leur contexte ; le jumeau la perd de son
invite ; les personnes et les cellules sont les memes des deux cotes. Les six conditions
d'agents de Stanford **ne sont ni testees ni affichees comme adversaires** : elles gardent les
items cousins dans leur invite (a8 errata E1, a41 section 0.2) et les replacer en regime
severe demanderait de relancer leur pipeline [MESURE, controle publie]. Interdiction 4 de a41
section 7 : R2 mesure **nos** agents, pas les leurs.

---

## 2. Les quatre familles, avec verdict selon les criteres preenregistres

### 2.0 Le tableau de reference

[MESURE, `r2-tableau-def.csv`, `C3F gpt-oss-20b`, 150 personnes, 58 items, definition de
rarete sur le perimetre, **106 cellules rares stables**]

| methode | exactitude | raretes osees | rappel stables | precision stables | F1 stables | exces sur plancher | diversite conservee | ratio intra |
|---|---|---|---|---|---|---|---|---|
| *humains vague 2* | *0,7761* | *106* | *1,0000* | *1,0000* | *1,0000* | *plus 0,8356* | *0,9920* | *0,9838* |
| `PMM k=10 famille retiree` | 0,6302 | 137 | **0,2830** | 0,2190 | **0,2469** | **plus 0,1242** | 0,9828 | 0,9616 |
| `E2 famille retiree (tirage)` | 0,6010 | 166 | 0,2358 | 0,1506 | 0,1838 | plus 0,0624 | **0,9950** | 0,9989 |
| `IM m=10 mode, famille retiree` | 0,6518 | 70 | 0,1981 | 0,3000 | 0,2386 | plus 0,0212 | 0,8537 | 0,8211 |
| **`C3F gpt-oss-20b`** | **0,5328** | **369** | **0,1887** | **0,0542** | **0,0842** | **plus 0,0315** | **0,4438** | **0,4280** |
| *plancher de segment* | | | *0,1644* | | | *zero par definition* | | |
| `E1 famille retiree (argmax)` | 0,6690 | 46 | 0,1509 | 0,3478 | 0,2105 | moins 0,0304 | 0,7957 | 0,7419 |
| `B2 famille retiree (tirage)` | 0,5795 | 154 | 0,1415 | 0,0974 | 0,1154 | moins 0,0304 | 0,9551 | 0,9573 |
| `B2 famille retiree (argmax)` | 0,6597 | 10 | 0,0377 | **0,4000** | 0,0690 | moins 0,1438 | 0,5897 | 0,5056 |
| *reperes hors regime severe* | | | | | | | | |
| `B1 argmax` | 0,6405 | 57 | 0,1132 | 0,2105 | 0,1472 | moins 0,0407 | 0,7060 | 0,5545 |
| `B0 tirage` | 0,5164 | 184 | 0,0943 | 0,0543 | 0,0690 | moins 0,0716 | 0,9854 | 1,0440 |
| `B0 mode` | 0,6205 | 0 | 0,0000 | sans objet | 0,0000 | moins 0,1644 | 0,0479 | 0,0545 |
| `B3 foret` | 0,6483 | 9 | 0,0189 | 0,2222 | 0,0348 | moins 0,1541 | 0,4673 | 0,3224 |

**Quatre lectures directes, avant tout test.**

1. **Le jumeau est quatrieme sur sept en rappel et dernier sur sept en precision**, dans un
   jeu ou il est le seul a avoir vu 137 reponses reelles de la personne.
2. **Son F1 sur les raretes stables, 0,0842, est le plus bas du regime severe apres
   `B2 argmax`.** La question ouverte 2 du rapport de lancement, « le rappel est il la bonne
   quantite, ou faut il passer au F1 », se resout ici sans avoir besoin d'etre tranchee :
   les deux quantites disent la meme chose.
3. **Son exactitude, 0,5328, est sous celle de la modalite modale de la population**,
   `B0 mode` a 0,6205. Le seul repere qu'il depasse est le tirage aveugle, `B0 tirage` a
   0,5164.
4. **Il ose 369 raretes sur 8 700 cellules, deux fois et demie plus que PMM**, et sa
   diversite conservee, 0,4438, est la plus basse du regime severe apres `B3 foret`. Les deux
   faits ne se contredisent pas : il ose beaucoup de modalites minoritaires, mais toujours les
   memes, ce que le ratio intra a 0,4280 dit deja.

### 2.1 F1 primaire, le rappel des raretes stables. 7 tests, Holm par famille

[MESURE, `r2-contrastes-def.csv`, definition de rarete sur le perimetre]

| | adversaire | difference | IC 95 % apparie | p brut | **p Holm** | p BH | signe attendu | **verdict** |
|---|---|---|---|---|---|---|---|---|
| **H1a** | plancher de segment | **plus 0,0315** | [moins 0,0355 ; plus 0,1015] | 0,3405 | **1,0000** | 0,4767 | positif | **echoue** |
| H1b | `E1 famille retiree (argmax)` | plus 0,0377 | [moins 0,0510 ; plus 0,1260] | 0,4550 | 1,0000 | 0,5308 | positif | echoue |
| H1b | `E2 famille retiree (tirage)` | moins 0,0472 | [moins 0,1343 ; plus 0,0342] | 0,3020 | 1,0000 | 0,4767 | positif | echoue, **signe inverse** |
| H1b | **`PMM k=10 famille retiree`** | **moins 0,0943** | **[moins 0,1729 ; moins 0,0099]** | 0,0400 | 0,2400 | 0,1400 | positif | echoue, **signe inverse** |
| H1b | `IM m=10 mode, famille retiree` | moins 0,0094 | [moins 0,0870 ; plus 0,0660] | 0,8830 | 1,0000 | 0,8830 | positif | echoue, **signe inverse** |
| H1b | `B2 famille retiree (argmax)` | **plus 0,1509** | [plus 0,0575 ; plus 0,2362] | 0,0025 | **0,0175** | 0,0175 | positif | **passe** |
| H1b | `B2 famille retiree (tirage)` | plus 0,0472 | [moins 0,0342 ; plus 0,1226] | 0,2800 | 1,0000 | 0,4767 | positif | echoue |

**Verdict de F1 : un test sur sept passe, et c'est celui contre l'adversaire le plus faible
du jeu.** `B2 famille retiree (argmax)`, ce sont les voisins de Hamming pris a l'argmax, une
methode qui n'ose que **dix** raretes sur 8 700 cellules ; battre son rappel n'est pas un
resultat, c'est une identite de comportement.

**Trois precisions qui ne doivent pas etre confondues.**

- **H1a n'est pas « le jumeau fait comme le hasard ».** Le point estime est positif,
  plus 0,0315, et l'intervalle contient zero. La formulation juste est : **on ne peut pas
  distinguer son rappel d'un tirage au sort dans le segment de la personne**, et l'intervalle
  **exclut** un exces aussi grand que plus 0,102. Il exclut donc, sur ce perimetre, l'exces
  de plus 0,1616 que a42 mesure pour C3 hors regime severe, et l'exces de plus 0,289 de
  `agents composite`.
- **Contre PMM, le point estime et l'intervalle non ajuste sont entierement contre le
  jumeau.** C'est un fait a rapporter tel quel : moins 0,0943 [moins 0,1729 ; moins 0,0099],
  p brut 0,0400. Sous Holm, dans une famille de sept, il ne decide pas. **Ce que R2 etablit
  est donc « le jumeau ne bat pas PMM », et non « PMM bat le jumeau ».** La difference
  compte, et la section 3 dit ce qu'il faudrait pour trancher la seconde.
- **La sensibilite a la definition de rarete ne sauve rien.** Avec la definition de a41,
  seuil applique aux 1 052 personnes, 96 cellules au lieu de 106 : H1a vaut plus 0,0424
  [moins 0,0303 ; plus 0,1208], p 0,262 ; contre PMM moins 0,0938 ; contre E2 exactement zero
  [MESURE, publie sans correction, comme sensibilite].

### 2.2 F2 secondaire, la precision. 7 tests

[MESURE, `r2-contrastes-def.csv`]

| | adversaire | difference | IC 95 % apparie | **p Holm** | **verdict** |
|---|---|---|---|---|---|
| **H2a** | plancher de segment sur les cellules **osees** | **moins 0,5254** | [moins 0,5671 ; moins 0,4770] | **0,0018** | **echoue, decidablement inverse** |
| H2b | `E1 famille retiree (argmax)` | moins 0,2936 | [moins 0,4259 ; moins 0,1558] | 0,0018 | echoue, decidablement inverse |
| H2b | `IM m=10 mode, famille retiree` | moins 0,2458 | [moins 0,3581 ; moins 0,1362] | 0,0018 | echoue, decidablement inverse |
| H2b | `PMM k=10 famille retiree` | moins 0,1648 | [moins 0,2440 ; moins 0,0898] | 0,0018 | echoue, decidablement inverse |
| H2b | `E2 famille retiree (tirage)` | moins 0,0964 | [moins 0,1471 ; moins 0,0489] | 0,0018 | echoue, decidablement inverse |
| H2b | `B2 famille retiree (argmax)` | moins 0,3458 | [moins 0,6837 ; moins 0,0356] | 0,0405 | echoue, decidablement inverse |
| H2b | `B2 famille retiree (tirage)` | moins 0,0432 | [moins 0,0833 ; moins 0,0082] | 0,0280 | echoue, decidablement inverse |

**Verdict de F2 : zero test sur sept, et les sept sont decidables dans le sens defavorable.**

**H2a merite d'etre lu lentement, parce que c'est le contraste le plus severe du rapport.**
Le plancher n'est pas ici « la precision d'une methode qui tire au hasard partout » : c'est la
probabilite qu'un tirage dans la marginale du segment de la personne tombe juste **sur les
cellules exactes ou le jumeau a ose une minorite**. Elle vaut **0,5796**, parce que sur ces
cellules la vraie reponse est le plus souvent la modalite majoritaire. Le jumeau, lui, y est
juste 0,0542 fois sur une. **Sur les cellules ou il ose, oser lui coute 52,5 points par
rapport a ne pas oser** [MESURE]. La lecture defensive du dossier, « le jumeau paie en
precision ce qu'il gagne en rappel », suppose un gain de rappel : il n'y en a pas.

### 2.3 F3 tertiaire, l'exactitude globale. 6 tests corriges plus H3b

[MESURE, `r2-contrastes-def.csv` et `r2-croises-def.csv`]

| | adversaire | difference | IC 95 % apparie | **p Holm** |
|---|---|---|---|---|
| H3a | `E1 famille retiree (argmax)` | **moins 0,1362** | [moins 0,1509 ; moins 0,1217] | 0,0015 |
| H3a | `B2 famille retiree (argmax)` | moins 0,1268 | [moins 0,1407 ; moins 0,1130] | 0,0015 |
| H3a | `IM m=10 mode, famille retiree` | moins 0,1189 | [moins 0,1328 ; moins 0,1051] | 0,0015 |
| H3a | `PMM k=10 famille retiree` | moins 0,0973 | [moins 0,1124 ; moins 0,0825] | 0,0015 |
| H3a | `E2 famille retiree (tirage)` | moins 0,0681 | [moins 0,0828 ; moins 0,0534] | 0,0015 |
| H3a | `B2 famille retiree (tirage)` | **moins 0,0467** | [moins 0,0613 ; moins 0,0326] | 0,0015 |
| H3b | `C3F Qwen3-4B`, 60 personnes communes | moins 0,0092 | [moins 0,0270 ; plus 0,0089] | non corrige, p 0,317 |

**Verdict de F3 : entierement negatif, comme la page de plan l'annoncait.** Les six
intervalles sont disjoints de zero et Holm est au plancher. C'est le critere de chute 4 :
**la phrase du dossier reste « le rappel des rares, et lui seul », sauf que le rappel des
rares vient lui aussi de tomber.**

**H3b est le premier des deux chiffres du pont avec le petit modele** : sur les 60 personnes
communes, le modele de 20 milliards et celui de 4 milliards ne sont pas distinguables en
exactitude, et le point estime est **en faveur du petit**.

### 2.4 F4 quaternaire, la structure. 6 tests, plus H4c descriptif

[MESURE, `r2-contrastes-def.csv`]

| | adversaire | quantite | difference | IC 95 % apparie | **p Holm** |
|---|---|---|---|---|---|
| H4a | `E2 famille retiree (tirage)` | diversite conservee | **moins 0,5523** | [moins 0,5845 ; moins 0,5191] | 0,0015 |
| H4a | `PMM k=10 famille retiree` | diversite conservee | moins 0,5398 | [moins 0,5686 ; moins 0,5101] | 0,0015 |
| H4a | `B2 famille retiree (tirage)` | diversite conservee | moins 0,5118 | [moins 0,5477 ; moins 0,4747] | 0,0015 |
| H4b | `E2 famille retiree (tirage)` | ecart absolu a 1 du ratio intra | **plus 0,5587** | [plus 0,5162 ; plus 0,5952] | 0,0015 |
| H4b | `PMM k=10 famille retiree` | ecart absolu a 1 du ratio intra | plus 0,5330 | [plus 0,4992 ; plus 0,5656] | 0,0015 |
| H4b | `B2 famille retiree (tirage)` | ecart absolu a 1 du ratio intra | plus 0,5288 | [plus 0,4843 ; plus 0,5733] | 0,0015 |

**Verdict de F4 : les six contrastes sont decidables et tous defavorables**, avec des
amplitudes qui sont les plus grandes du rapport. Le jumeau conserve **0,4438** de la
diversite humaine quand les trois methodes a tirage en conservent 0,9551 a 0,9950, et il est
plus loin de 1 sur le ratio intra de plus de la moitie d'un point de ratio. C'est le fait de
a41 section 7 reproduit sur un modele cinq fois plus gros, et **aggrave** : `C3F Qwen3-4B`
conservait 0,5898.

**H4c, la chute sous permutation, descriptif et hors famille** [MESURE,
`r2-permutation-def.csv`, 200 permutations].

`S_fin`, le bloc ideologie x genre x age, est **declare non calculable**, comme la page de
plan l'ecrivait d'avance : sur 150 personnes le plus gros groupe compte **8** individus et
aucun camp n'est exploitable. Les deux autres segmentations sont calculables. Sur `S_camp`,
trois camps, le plus gros a 63 personnes :

| methode | exactitude | permutee | chute | **part du plancher humain** |
|---|---|---|---|---|
| *humains vague 2, plancher* | *0,7761* | *0,5453* | ***0,2308*** | *100 %* |
| `PMM k=10 famille retiree` | 0,6302 | 0,5474 | 0,0828 | **35,9 %** |
| `E1 famille retiree (argmax)` | 0,6690 | 0,5873 | 0,0817 | 35,4 % |
| `IM m=10 mode, famille retiree` | 0,6518 | 0,5733 | 0,0785 | 34,0 % |
| `E2 famille retiree (tirage)` | 0,6010 | 0,5406 | 0,0604 | 26,2 % |
| `B2 famille retiree (argmax)` | 0,6597 | 0,6125 | 0,0471 | 20,4 % |
| `B2 famille retiree (tirage)` | 0,5795 | 0,5493 | 0,0302 | 13,1 % |
| **`C3F gpt-oss-20b`** | 0,5328 | 0,5079 | **0,0249** | **10,8 %** |

Sur `S_ideo`, six niveaux exploitables, l'ordre est le meme et le jumeau est encore dernier,
**10,1 %** du plancher humain [MESURE].

**Le jumeau prive de sa famille est dernier des huit, sous toutes les methodes statistiques,
sous les deux segmentations.** Et le contraste avec `C3` est net : la meme trace, cousins
conserves, remonte a **36,7 %** du plancher humain sur `S_camp`, 105 personnes, au niveau de
PMM a 39,2 % et de E1 a 36,3 %. **Ce n'est pas le modele qui porte la personne, ce sont les
items cousins de son invite.**

*Reserve de lecture, la meme que celle du rapport de lancement.* a44 section 5 mesure sur 149
items et 1 052 personnes ; ici, 58 items, 150 personnes et la famille retiree. La comparaison
directe des pourcentages entre les deux rapports n'est pas legitime. Ce qui est lisible est
l'ordre a l'interieur de ce tableau, ou toutes les methodes subissent exactement la meme
privation.

### 2.5 Score des cinq predictions signees

Elles sont dans la page de plan section 5 et dans `resultats/bilan-predictions.md` section 4,
recopiees ici sans etre reecrites. [MESURE pour les verdicts]

| | enonce, direction | verdict | ce qui est mesure |
|---|---|---|---|
| **a** | H1a passe pour `C3F gpt-oss` (*en faveur*) | **FAUSSE** | plus 0,0315 [moins 0,0355 ; plus 0,1015], Holm 1,0000 |
| **b** | H1b passe contre `B2 argmax`, `E1` et `IM m=10` ; incertain contre `PMM` et `E2 tirage` (*en faveur*) | **A MOITIE, et du mauvais cote** | un seul des trois annonces passe, `B2 argmax` ; `E1` echoue et `IM` echoue **avec le signe inverse** ; les deux « incertains » se resolvent **contre** le jumeau |
| **c** | H2 echoue au moins contre `PMM` (*contre*) | **TENUE, et au dela** | H2 echoue contre les **six**, et contre le plancher, les sept a Holm decidable |
| **d** | H3a reste entierement negatif, mais l'ecart median passe sous les 9,8 points de Qwen3-4B contre PMM (*contre*) | **A MOITIE** | premiere moitie tenue, six contrastes negatifs a Holm 0,0015. Seconde moitie **non tenue** : ecart median moins 0,1081, soit 10,8 points, au dessus de 9,8 ; et sur les 60 personnes communes, moins 0,1138 contre moins 0,1046 pour le petit modele |
| **e** | H4a place `C3F gpt-oss` sous 80 pour cent de diversite conservee (*en faveur*) | **TENUE** | 0,4438, tres en dessous de 80, et en dessous des 0,5898 du modele de 4 milliards |

**Ce que ce score dit du preenregistrement.** Trois predictions etaient ecrites **en faveur**
de la these, deux **contre** elle. **Les deux qui sont contre sont tenues, et deux des trois
qui sont en faveur sont fausses ou a moitie.** C'est le motif d'une page de plan reellement
ecrite avant les chiffres, et il est publie comme tel, sans etre presente comme une vertu.

---

## 3. La puissance : ce qui est decide, ce qui ne l'est pas, et ce qu'il faudrait

### 3.1 Le compte des cellules : mieux que prevu, et cela ne suffit pas

[MESURE, `r2b-cellules-par-personne.csv`]

| | valeur |
|---|---|
| cellules rares stables attendues sur 150 personnes, ecrites d'avance | **78** (a42, extrapolation des 31 cellules de 60 personnes) |
| cellules rares stables **mesurees** sur 150 personnes | **106** |
| personnes qui ne portent **aucune** cellule rare stable | **98 sur 150** |
| mediane de cellules par personne | **0** |
| moyenne | 0,71 |
| maximum | 9 |

**La puissance annoncee etait pessimiste de 36 pour cent, et cela ne change pas la
conclusion.** La raison est ecrite dans la troisieme ligne : **le bootstrap porte sur les
personnes, et 98 personnes sur 150 n'apportent aucune information a la famille primaire.**
L'effectif effectif de F1 n'est pas 150, c'est **52**, et 106 cellules reparties de facon tres
inegale, jusqu'a neuf chez une seule personne. C'est pourquoi l'ecart type de bootstrap des
contrastes H1b reste a 0,040 environ malgre le doublement du perimetre par rapport a a41.

### 3.2 Les contrastes sont ils decidables ?

[MESURE et ESTIMATION, `r2b-puissance.csv`. L'effectif exige est une **estimation** : il
suppose l'effet constant et met l'ecart type a l'echelle en 1 sur racine de n, ce qui est
l'hypothese usuelle et n'est pas verifiee ici. Le z exige est celui de Holm pour le test le
plus severe d'une famille de sept, alpha sur sept unilateral, soit **2,450**. C'est la barre
la plus exigeante de la famille, un contraste classe deuxieme n'ayant besoin que de alpha sur
six : les effectifs publies sont donc conservateurs de ce cote la]

| | adversaire | effet | ecart type | z observe | plus petit effet detectable, Holm | **personnes exigees, Holm** |
|---|---|---|---|---|---|---|
| H1a | plancher de segment | plus 0,0315 | 0,0347 | 0,91 | 0,0851 | **1 097** |
| H1b | `E1 famille retiree` | plus 0,0377 | 0,0446 | 0,85 | 0,1093 | 1 258 |
| H1b | `E2 famille retiree (tirage)` | moins 0,0472 | 0,0428 | moins 1,10 | 0,1049 | 742 |
| H1b | **`PMM k=10 famille retiree`** | **moins 0,0943** | 0,0417 | **moins 2,26** | 0,1021 | **176** |
| H1b | `IM m=10 mode` | moins 0,0094 | 0,0397 | moins 0,24 | 0,0972 | 15 914 |
| H1b | `B2 famille retiree (argmax)` | plus 0,1509 | 0,0449 | 3,36 | 0,1101 | **80, deja atteint** |
| H1b | `B2 famille retiree (tirage)` | plus 0,0472 | 0,0396 | 1,19 | 0,0970 | 635 |

**Trois lectures, et elles ne disent pas la meme chose.**

1. **Ce qui est decide l'est.** Le seul contraste de F1 dont le signe soit favorable et
   l'amplitude grande, `B2 argmax`, est decide a 150 personnes et le serait a 80. Les six
   familles F2, F3 et F4 sont decidees a Holm 0,0015 a 0,0405. **R2 n'est pas un rapport sans
   puissance : il est un rapport ou tout ce qui est grand est decide, et ou ce qui n'est pas
   decide est petit.**
2. **H1a n'est pas indecidable par manque de personnes, il est indecidable parce que l'effet
   est petit.** Le plus petit exces detectable a 150 personnes est **0,0851**. L'exces mesure
   est 0,0315, soit un tiers de cette barre. Pour le decider a son amplitude actuelle il
   faudrait **environ 1 100 personnes**, c'est a dire **la totalite du panel de 1 052**, et
   encore de justesse. **Autrement dit : meme en depensant tout le jeu de donnees, on ne
   ferait probablement pas passer H1a.** C'est la mesure la plus utile de la section, et elle
   ferme la question plutot qu'elle ne l'ouvre.
3. **Le seul contraste qui vaudrait la peine d'etre depense est celui contre PMM, et il irait
   contre nous.** Il exige **environ 176 personnes** sous Holm, 113 sous un intervalle a 95
   pour cent sans correction : c'est **26 personnes de plus** que ce que R2 a couvert, soit
   moins de deux heures de la machine au debit mesure de 1 932 appels par heure. **Si le
   dossier depense cette nuit la, l'issue probable n'est pas « le jumeau bat PMM », c'est
   « PMM bat le jumeau, decidablement ».** [ESTIMATION]

### 3.3 Ce qui n'est pas decidable et ne le sera pas ici

- **`IM m=10 mode`** : la difference est moins 0,0094, quinze mille personnes seraient
  necessaires. **La lecture juste est « le jumeau et l'imputation multiple font la meme chose
  sur les gens rares »**, et c'est une egalite, pas une indecision.
- **H3b, le gros modele contre le petit** : moins 0,0092 en exactitude, p 0,317, sur 60
  personnes communes. Ce contraste ne demande pas plus de personnes, il demande **plus de
  personnes communes** : la trace Qwen3-4B n'en a que 60, issues des plis 0 et 1 seulement
  (a33 section 0.1). Completer C3F Qwen3-4B aux 150 personnes coute une nuit courte a 2 688
  appels par heure et rendrait ce contraste decidable ou definitivement nul.
- **Le rappel des raretes stables entre les deux modeles** : moins 0,0968
  [moins 0,2693 ; plus 0,0370], p 0,247, 31 cellules seulement. Meme remede.

---

## 4. Le pont avec le petit modele, et le cout du retrait de la famille

### 4.1 Le modele de 20 milliards ne reduit pas l'ecart avec la statistique. Il l'augmente

[MESURE, `r2b-pont-modeles.csv` et `r2b-ecarts-a-la-statistique.csv`, **60 personnes
communes** aux deux traces C3F, memes 58 items, memes 31 cellules rares stables, memes six
methodes restreintes aux memes personnes]

| | **`C3F gpt-oss-20b`** | **`C3F Qwen3-4B`** | ce que dit la comparaison |
|---|---|---|---|
| exactitude | 0,5480 | **0,5572** | le petit modele est devant |
| ecart median aux six methodes severes, exactitude | **moins 0,1138** | moins 0,1046 | **le gros creuse l'ecart de 0,9 point** |
| ecart extreme, contre `E1` | moins 0,1437 | moins 0,1345 | idem sur les six, un a un |
| rappel des raretes stables | 0,1613 | **0,2581** | le petit modele est devant de 9,7 points |
| ecart median aux six, rappel | plus 0,0484 | **plus 0,1452** | **le gros perd 9,7 points d'avance** |
| precision sur les raretes stables | 0,0331 | **0,0727** | le petit modele est devant |
| exces sur le plancher de segment | plus 0,0412 | **plus 0,1245** | ni l'un ni l'autre decidable sur 60 personnes |
| raretes osees | 151 | 110 | le gros ose 37 pour cent de plus |
| diversite conservee | **0,4340** | 0,5898 | **le gros ecrase plus la dispersion** |
| ratio intra | **0,4456** | 0,6407 | idem |

**La reponse a la question posee est donc : non, et de combien se mesure.** Sur les memes 60
personnes, passer de 4 a 20 milliards de parametres **augmente** l'ecart median d'exactitude
aux methodes statistiques de **0,9 point**, **reduit** le rappel des raretes stables de
**9,7 points**, et **abaisse** la diversite conservee de **15,6 points**.

**Aucune de ces trois differences n'est decidable** [MESURE, `r2-croises-def.csv`] :
exactitude moins 0,0092 [moins 0,0270 ; plus 0,0089], p 0,317 ; rappel moins 0,0968
[moins 0,2693 ; plus 0,0370], p 0,247. **La formulation autorisee est donc « le passage a 20
milliards de parametres ne reduit aucun des trois ecarts, et son point estime va dans l'autre
sens dans les trois cas »**, jamais « le gros modele est pire ».

**Ce que cela retire au dossier.** La derniere ligne de defense disponible etait « C3F est un
modele local de 4 milliards de parametres, ce n'est pas Stanford » (a41 interdiction 4). Elle
reste vraie pour Stanford. Elle n'est plus disponible comme explication de l'echec : le
modele a ete multiplie par cinq, sur les memes personnes, et rien n'a bouge dans le bon sens.

### 4.2 Le cout du retrait de la famille : 6,3 points a 20 milliards, 6,2 a 4 milliards

[MESURE, `r2-croises-def.csv` et `r2b-pont-regimes.csv`, **105 personnes communes** aux
traces C3F et C3 gpt-oss, memes 58 items, 87 cellules rares stables]

| quantite | `C3F gpt-oss` | `C3 gpt-oss` | **C3F moins C3** | IC 95 % apparie | p |
|---|---|---|---|---|---|
| exactitude | 0,5435 | 0,6062 | **moins 0,0627** | [moins 0,0783 ; moins 0,0473] | 0,00025 |
| rappel des raretes stables | 0,2529 | 0,4828 | **moins 0,2299** | [moins 0,3333 ; moins 0,1316] | 0,00025 |
| precision sur les raretes stables | 0,0794 | 0,2211 | moins 0,1417 | | |
| exces sur le plancher de segment | plus 0,0825 [moins 0,0075 ; plus 0,1682] | plus 0,3491 [plus 0,2315 ; plus 0,4671] | | | |
| raretes osees | 277 | 190 | plus 87 | | |
| chute sous permutation, part du plancher humain, `S_camp` | 10,8 % (sur 150) | **36,7 %** | | | |

**Comparaison avec le modele de 4 milliards** [MESURE, a33 section 2, 60 personnes, memes 58
items] : `C3F moins C3` vaut **moins 0,0624** [moins 0,0828 ; moins 0,0422] en exactitude,
p ajuste 0,00175.

**Le cout du retrait de la famille est le meme a 4 et a 20 milliards de parametres : 6,2 et
6,3 points d'exactitude, intervalles largement recouvrants.** [MESURE] Ce n'est pas un
resultat de puissance, c'est un resultat de forme : **la dependance aux items cousins ne
diminue pas avec la taille du modele.** a33 ne pouvait pas mesurer l'effet sur le rappel des
raretes, faute de cellules ; R2 le mesure, et il est enorme : **moins 23 points**, soit **la
moitie du rappel de C3**.

**Et c'est la que se trouve toute l'explication du dossier depuis a42.** `C3 gpt-oss`, cousins
conserves, passe H1a et **les six** H1b sous Holm, PMM compris. `C3F gpt-oss`, cousins retires
comme ils le sont du contexte des methodes statistiques, n'en passe aucun sauf contre
`B2 argmax`. **La comparaison qui donnait raison au jumeau etait la comparaison ou lui seul
gardait les items voisins de la question.**

**Une reserve qui doit accompagner cette lecture partout.** `C3` **n'est pas** une condition
appariee : son contexte contient les cousins que les six methodes statistiques n'ont pas.
Ses sept succes en F1 ne sont donc pas un resultat de superiorite, ce sont exactement le biais
que R2 existe pour mesurer. Et ce biais est fragile a la definition de la rarete : sous la
definition de a41, sur la population, **l'avantage de C3 sur PMM tombe a plus 0,0769,
p 0,4085, non decidable** [MESURE, sensibilite non corrigee].

---

## 5. Ce que cela change

### 5.1 Au verrou 1 de `MODELE-DU-MONDE.md` section 10.5

Le verrou 1 demandait « la comparaison appariee du rappel des minorites, restreinte aux
raretes stables : un run en regime severe sur gpt-oss-20b, famille retiree de l'invite [...]
avec la chute sous permutation comme seconde quantite ; une nuit ».

**Il est execute, en entier, et il se ferme dans le sens negatif.** [ETABLI] Les 150
personnes sont couvertes, la seconde quantite est mesuree sous deux segmentations, et la case
« raretes stables x 58 items de famille x regime severe », qui n'existait dans aucun fichier
de `resultats/`, existe maintenant. **Ce verrou ne se rouvre pas sans element nouveau**, et
la section 3.2 dit lequel serait necessaire : environ 176 personnes pour decider le contraste
contre PMM, dans un sens qui serait defavorable, et environ 1 100 pour esperer decider H1a a
son amplitude actuelle.

**La phrase de la section 10.4, « son seul avantage mesure tient sur les gens rares reels
[...] et il attend sa comparaison appariee », doit etre remplacee, pas amendee.** La
restriction que la page de plan avait prevue, « hors du regime ou l'information la plus proche
manque », est trop faible : elle laisserait croire qu'il existe un regime ou l'avantage est
mesure en apparie. Il n'y en a pas. La formulation que R2 autorise est :

> Sur les reponses rares que la personne redonne deux semaines plus tard, l'avantage du
> jumeau de langage sur l'imputation statistique **n'existe que lorsque le jumeau garde dans
> son invite les items voisins de la question et que la statistique en est privee**. Compare
> a information egale, sur les memes personnes et les memes cellules, il ne se distingue pas
> d'un tirage au sort dans le segment demographique de la personne, et il est derriere
> l'appariement sur moyenne predite.

### 5.2 Aux trois phrases revendicables de la section 11.4

- **Phrase une**, la substitution qui suit le conditionnement : **non touchee par R2.** Elle
  attend R3, qui n'a pas encore demarre.
- **Phrase deux.** Sa derniere clause, « son seul avantage mesure [...] est mesure contre le
  comparateur le plus faible et attend R2 sur gpt-oss-20b, famille retiree de l'invite
  [EN ATTENTE, arret 05:45] », doit etre **retiree et remplacee**. La phrase deux devient
  entierement negative : *« Compare equitablement a vingt methodes d'imputation, un jumeau de
  langage est une imputation par l'esperance, dominee par les imputations par tirage sur la
  structure et par la regression sur l'exactitude dans les deux regimes mesures, il ne bat pas
  la moyenne du segment de la personne calculee sans elle, et **il ne bat pas non plus
  l'imputation par tirage sur les gens rares que la personne redonne deux semaines plus tard,
  des lors que les deux cotes perdent la meme information** ».* [ETABLI]
- **Phrase trois**, la regle du plancher : **renforcee.** R2 est le rapport ou le plancher
  fait tout le travail. Sans le plancher de segment, le rappel brut de 0,1887 serait lisible
  comme un succes ; avec lui, il n'est pas distinguable du hasard. Et le plancher humain de
  la chute sous permutation, 0,2308, est ce qui rend lisible le 0,0249 du jumeau. **La regle
  « aucune quantite ne se publie sans le plancher de sa population, de son effectif, de son
  delai et de son protocole » recoit ici sa demonstration la plus nette.**

### 5.3 A `ARBITRAGE.md`

**La phrase du point 4, « Cet avantage attend encore sa comparaison appariee », ne peut plus
etre ecrite.** [ETABLI] L'attente est levee et la reponse est negative. Elle apparait trois
fois dans le fichier, aux lignes 72, 158 et dans le point 4 de la liste des revendications,
et elle doit etre remplacee partout par le meme enonce, pas par une variante :

> Cet avantage a recu sa comparaison appariee, sur un modele de 20 milliards de parametres et
> 150 personnes, et il ne survit pas : a information egale, le jumeau ne se distingue pas d'un
> tirage dans le segment de la personne sur les gens rares stables, et il est derriere
> l'appariement sur moyenne predite.

**Consequence sur les trois options.** L'option A, « la ou l'etiquette remplace la personne »,
gardait comme unique note positive « ils sont domines sauf sur les gens rares reels ». **Cette
exception tombe.** L'option A ne devient pas indefendable : elle devient **entierement
negative**, ce qui est un papier different et, selon le quatrieme critere du jugement, pas un
papier moins bon. Ce qui change est la promesse commerciale, pas la valeur scientifique.
L'ordre des nuits recommande par `ARBITRAGE.md`, « d'abord la comparaison appariee sur les
gens rares », etait le bon : c'est la nuit qui a le plus change le dossier.

### 5.4 A `MOONSHOTS.md`

**C'est l'issue 3 de la page de plan section 6, celle qui renforce le programme B et affaiblit
tout le reste.** [ETABLI, la page de plan l'ecrit d'avance]

- **Programme B, la bande humaine.** Il gagne, et il gagne deux fois. Une, sa these ne depend
  pas de la superiorite du langage mais de la **detectabilite d'un flux**, et R2 ne la touche
  pas. Deux, R2 lui fournit **une seconde quantite de personne** a cote de la chute sous
  permutation de a44 : le rappel des raretes stables en regime severe, avec son plancher de
  segment et son plafond humain a 1,0000, mesures ici sur 106 cellules. Sa section « ce qui
  ne se leve pas » reclamait exactement ce type de statistique de reserve, prise sur la
  personne et non sur les marges.
- **Moonshot 9, l'audit des simulateurs vendus (E1, E2, E5).** Il perd son argument
  commercial, et la phrase a ecrire est celle que la mission demande, sans adoucissement :
  **si un jumeau de 20 milliards de parametres ne bat pas une imputation a tirage sur les
  gens rares en comparaison appariee, alors la valeur d'un panel synthetique est celle de
  l'imputation.** [ETABLI sur nos agents ; **non etabli sur les simulateurs vendus**, qui
  n'ont pas ete mesures ici] La reponse a l'acheteur devient « achetez le modele tabulaire »,
  ce que le jugement anticipait deja pour le programme E3. Le critere d'achat que l'issue 1
  aurait donne, « un simulateur qui ne retrouve pas les rares stables d'un panel tenu cache ne
  vaut pas son prix », reste utilisable comme **test**, mais il ne peut plus etre presente
  comme un test que les jumeaux passent et les tables ratent.
- **Programme A, l'oracle des camps : non touche.** Il porte sur le mode description, pas sur
  l'imputation. R1 l'alimente, R2 non.

### 5.5 La these devient elle un resultat negatif complet sur les jumeaux ?

**Oui, sur la valeur predictive des jumeaux de langage, et le rapport ne doit pas l'adoucir.**
[ETABLI] Des quatre avantages que le dossier a successivement revendiques, les quatre sont
tombes : l'exactitude en regime apparie (a41 sections 4 et 5), la structure contre les
imputations a tirage (a41 section 7), le gonflement et l'ecrasement comme quantites de
personne (a44, a47, errata E3), et maintenant le rappel des gens rares en comparaison
appariee (R2). **Il ne reste aucune quantite sur laquelle un jumeau de langage batte une
methode d'imputation de manuel a information egale.**

**Quatre choses restent, et elles ne sont pas des consolations.**

1. **La mesure.** La grille de comparaison est le vrai produit : vingt methodes d'imputation,
   six methodes de regime severe, trois planchers dont un obtenu en reinterrogeant les memes
   personnes, la partition stable contre instable, et un bootstrap apparie sur les personnes.
   **C'est ce dispositif qui a permis de faire tomber quatre revendications en huit jours, y
   compris les notres**, et c'est lui qui se publie.
2. **La cause par l'etiquette.** Elle reste ouverte et elle est mesurable : R3 est en attente
   et decide si l'etiquette a un effet propre ou si tout est du conditionnement. **R2 n'y
   touche pas** : ses deux conditions, C3 et C3F, n'ont **aucune** etiquette ni aucune
   demographie. Ce que R2 ajoute a ce chantier est un fait de forme utile : le retrait des
   cousins coute la meme chose a 4 et a 20 milliards de parametres, donc les effets de
   conditionnement mesures sur Qwen3-4B ne sont pas des artefacts de petit modele.
3. **Le plancher humain.** Il est ce qui a rendu R2 lisible, et c'est la revendication de
   nouveaute la plus solide du dossier. Ici il donne les deux nombres qui font le rapport :
   0,1644 pour le tirage dans le segment et 0,2308 pour la chute des memes humains
   reinterroges.
4. **La grille comme norme d'audit**, c'est a dire le programme B. C'est le seul programme que
   ce resultat negatif renforce, et c'est celui ou le dossier detient deja la mesure.

**Ce que le resultat negatif ne dit pas.** Il ne dit rien des agents de Stanford, qui n'ont
pas ete replaces dans le regime severe et ne peuvent pas l'etre sans relancer leur pipeline.
Il ne dit rien des 1 052 personnes. Il ne dit rien de la contamination. Et il ne dit pas que
les jumeaux de langage sont inutiles : il dit qu'ils ne sont pas de meilleurs **imputateurs**
que l'imputation.

---

## 6. La figure

`resultats/r2b-figure-rares.png` et `.svg` [MESURE, produites par `analyses/r2b_puissance.py`]

Deux panneaux, memes 150 personnes, memes 58 items, memes 106 cellules rares stables. A
gauche le **rappel des raretes stables**, `C3F gpt-oss-20b` en tete de tableau et les six
methodes du regime severe dessous, avec le **plancher de segment en pointille vert a 0,164**.
A droite la **precision sur les raretes osees**, memes methodes, meme ordre. Les barres
d'erreur sont les intervalles a 95 pour cent du bootstrap apparie sur les personnes, 4 000
tirages partages. Le rouge est notre jumeau, le bleu les imputations par tirage, le gris les
imputations par esperance, pour que la lecture ne repose pas sur la couleur seule : le libelle
porte deja la marque.

**Ce que la figure montre en une seconde, et c'est pourquoi elle est faite ainsi.** A gauche,
la barre rouge touche le pointille et trois barres bleues et grises le depassent nettement.
A droite, la barre rouge est la plus courte du panneau, d'un facteur quatre a sept. **Le
jumeau ose le plus et touche le moins.** Le plancher ne figure que sur le panneau de gauche :
le plancher de precision depend des cellules que chaque methode ose, et differe donc d'une
methode a l'autre, ce qui interdit une ligne unique. Sa valeur pour le jumeau, 0,5796, est
dans la section 2.2.

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. **« Quand la famille thematique entiere de la question est retiree de l'invite du jumeau
   comme du contexte de la statistique, un jumeau de langage de 20 milliards de parametres ne
   retrouve pas les reponses rares que la personne redonne deux semaines plus tard mieux qu'un
   tirage au sort dans son segment demographique : plus 0,0315 [moins 0,0355 ; plus 0,1015]
   sur 150 personnes et 106 cellules. »** [MESURE]
2. **« Il est derriere l'appariement sur moyenne predite sur cette meme quantite, moins 0,0943,
   intervalle non ajuste entierement negatif, et le seul adversaire qu'il batte est celui qui
   n'ose que dix raretes sur 8 700 cellules. »** [MESURE] La seconde moitie de la phrase est
   obligatoire : sans elle, « il en bat un sur six » serait trompeur.
3. **« Sur les cellules ou il ose une modalite minoritaire, il est juste 0,0542 fois sur une
   la ou un tirage dans le segment le serait 0,5796 fois : oser lui coute 52,5 points, avec un
   intervalle disjoint de zero. »** [MESURE]
4. **« Passer de 4 a 20 milliards de parametres, sur les memes 60 personnes, ne reduit aucun
   des trois ecarts a la statistique, et le point estime va dans l'autre sens dans les trois
   cas. »** [MESURE, aucune des trois differences n'etant decidable]
5. **« Retirer les items cousins coute 6,2 points d'exactitude a un modele de 4 milliards et
   6,3 a un modele de 20 milliards, et 23 points de rappel des raretes stables au second. »**
   [MESURE, a33 pour le premier, R2 pour le second]
6. **« Prive de sa famille thematique, le jumeau porte la personne moins que n'importe quelle
   methode statistique soumise a la meme privation : 10,8 pour cent du plancher humain contre
   13,1 a 35,9 pour cent. Avec les cousins, il remonte a 36,7. »** [MESURE, descriptif, hors
   famille d'hypotheses, `S_camp`]
7. **« Le dossier ne detient plus aucune quantite sur laquelle un jumeau de langage batte une
   methode d'imputation de manuel a information egale. »** [ETABLI]
8. **« La valeur d'un panel synthetique, sur les gens rares, est celle de l'imputation. »**
   [ETABLI sur nos agents ; a ne jamais ecrire sans cette restriction]

### Interdit

1. **Interdit d'ecrire « le jumeau fait comme le hasard sur les gens rares ».** [MESURE]
   Le point estime est positif et l'intervalle contient zero. La formulation est « on ne peut
   pas l'en distinguer », et elle s'accompagne de la borne haute, plus 0,102, qui est ce que
   la mesure exclut.
2. **Interdit d'ecrire « PMM bat le jumeau sur les gens rares ».** [MESURE] Sous Holm, dans
   la famille de sept declaree, le contraste ne decide pas, p ajuste 0,2400. Ce qui est
   etabli est « le jumeau ne bat pas PMM ». La difference entre les deux enonces est la seule
   chose qui separe ce rapport d'un rapport qui ferait ce que a8 avait fait.
3. **Interdit de presenter R2 comme une refutation des agents de Stanford.** [CONFIRME]
   Ils gardent les items cousins dans leur invite et ne peuvent pas etre replaces en regime
   severe sans relancer leur pipeline. R2 mesure nos agents. Interdiction 4 de a41 section 7,
   maintenue mot pour mot.
4. **Interdit de citer les sept succes de `C3` comme un resultat de superiorite.** [MESURE]
   C3 garde les cousins que les six methodes statistiques n'ont pas. Ses sept succes sont la
   mesure du biais, pas la mesure d'un avantage. Et ils sont fragiles : sous la definition de
   rarete sur population, l'avantage de C3 sur PMM tombe a p 0,4085.
5. **Interdit d'attribuer l'echec a la taille du modele.** [MESURE] Le modele a ete multiplie
   par cinq sur les memes personnes et rien n'a bouge dans le bon sens.
6. **Interdit de lire le rappel sans la precision, ou la precision sans le rappel.** [MESURE]
   Le jumeau a le quatrieme rappel et la derniere precision ; `B2 argmax` a la meilleure
   precision, 0,4000, et le dernier rappel, 0,0377. Les deux lignes ensemble, ou rien.
7. **Interdit de comparer le 10,8 pour cent de chute sous permutation de R2 aux 45 pour cent
   de C3 dans a44.** [CONFIRME] Le perimetre change sur trois dimensions a la fois, items,
   personnes et regime. Seul l'ordre a l'interieur du tableau de R2 est lisible.
8. **Interdit de conclure quoi que ce soit sur les 1 052 personnes.** [CONFIRME] Les 150 sont
   un sous echantillon stratifie sur les cinq plis ; les 60 de la trace Qwen3-4B viennent des
   plis 0 et 1 seulement. La comparaison appariee n'en souffre pas, la generalisation si.

---

## Ce que je n'ai pas pu verifier

1. **Que la seconde passe ne changerait rien.** [NON VERIFIE] L'ordre inverse des modalites
   n'a pas ete fait, le budget de la nuit ne le permettait pas. **Le biais de position est
   donc non controle dans R2.** Il est le meme pour C3F et pour C3, donc il ne biaise pas leur
   comparaison ; il peut biaiser la comparaison avec les six methodes statistiques, qui n'ont
   pas de biais de position. C'est la limite la plus serieuse du rapport, et elle joue
   potentiellement **contre** le jumeau.
2. **Que la variante de fin de prompt retenue soit la meilleure.** [MESURE, et arbitrage
   assume] La sonde a mesure `answer` a 0,9622 et `brut` a **0,9995**. La page de plan
   prescrivait de garder `answer` des qu'elle atteint 0,90, pour rester comparable a la trace
   a5, et c'est ce qui a ete fait. **3,7 points de masse ont donc ete cedes a la
   comparabilite.** Je ne sais pas ce que `brut` aurait donne, et un lecteur adverse peut
   demander la meme nuit sous `brut`.
3. **La contamination.** [NON VERIFIE] La coupure de juin 2024 est publiee par OpenAI, pas
   auditee. R2 n'en tire aucune conclusion, ni dans un sens ni dans l'autre, et le sens du
   resultat rend la question moins pressante qu'elle ne l'aurait ete en cas de succes.
4. **L'effectif exige de la section 3.2.** [ESTIMATION] Il suppose l'effet constant et met
   l'ecart type a l'echelle en 1 sur racine de n. Sur une quantite dont 98 personnes sur 150
   ne portent aucune cellule, cette mise a l'echelle est optimiste : ajouter des personnes
   ajoute surtout des zeros. Les nombres publies sont donc des **bornes basses** de l'effectif
   necessaire.
5. **Que le plancher de precision de H2a soit la bonne reference.** [NON VERIFIE comme choix]
   `a42_commun.mesure_sur` ne fournit pas de precision de reference, parce que a42 ne teste
   que le rappel ; elle est construite dans `r2_evaluer` avec les memes briques. Le choix,
   « la probabilite qu'un tirage dans le segment tombe juste sur exactement les cellules
   osees », est defendable et il est declare ; il n'a pas ete valide contre une autre
   definition.
6. **Ce que vaut `C3F` sur les 90 personnes manquantes de la trace Qwen3-4B.** [NON VERIFIE]
   Le pont entre modeles repose sur 60 personnes et 31 cellules. Le verrou 1 de la section
   10.5 demandait aussi « les 90 personnes manquantes de C3F » ; elles ne sont toujours pas
   la, et c'est la depense la moins chere qui reste ouverte.
7. **La chute sous permutation sur `S_fin`.** [CONFIRME comme non calculable] Zero camp
   exploitable sur 150 personnes, groupe maximal a 8 individus. Declare d'avance.
8. **Que la nuit perdue entre 05:45 et 06:02 n'ait rien coute a R3.** [PARTIELLEMENT VERIFIE]
   R3 a demarre a 06:02 et non a 05:45 comme la file le prevoyait, parce que le serveur de R2
   a survecu au SIGTERM ; sa fin dure reste 08:00. Je n'ai pas touche a la machine et je ne
   sais pas combien de personnes ces dix sept minutes lui coutent.

---

## Questions ouvertes pour Simon

1. **Faut il depenser les 176 personnes qui rendraient decidable le contraste contre PMM ?**
   C'est moins de deux heures de machine, et l'issue probable est **defavorable au dossier** :
   « PMM bat le jumeau sur les gens rares, decidablement ». Un preenregistrement honnete doit
   se decider avant de savoir, et nous savons deja le signe. Ma lecture : **oui**, parce que
   la difference entre « ne bat pas » et « est battu » sera la premiere chose qu'un rapporteur
   demandera, et parce qu'un dossier qui depense une nuit pour se contredire lui meme est plus
   credible qu'un dossier qui s'arrete a l'indecision favorable. Mais c'est un arbitrage, pas
   une mesure.
2. **La question ouverte 4 du rapport de lancement demandait une regle ecrite d'avance pour le
   cas « H1a passe et H1b echoue contre PMM seulement ». Le cas ne s'est pas produit, mais un
   voisin s'est produit : H1b echoue contre PMM **avec le signe inverse**, et la page de plan
   n'avait pas prevu ce cas la.** Le critere de chute 1 s'applique par H1a et suffit ; faut il
   neanmoins ajouter d'avance, pour les prochains runs, une regle disant quoi faire d'un
   contraste dirige dont le signe s'inverse ?
3. **La definition de la rarete, perimetre ou population.** R2 corrige celle du perimetre,
   qui est la definition declaree, et publie l'autre en sensibilite. Les deux donnent la meme
   conclusion pour C3F, 106 cellules contre 96. **Elles ne la donnent pas pour C3** : sous la
   definition de population, l'avantage de C3 sur PMM tombe a p 0,4085. Faut il faire de la
   definition sur population la definition officielle du dossier, puisque c'est la seule qui
   ne bouge pas quand le perimetre bouge ?
4. **`S_camp` comme quantite de verdict.** R2 confirme ce que le rapport de lancement
   anticipait : `S_fin` est vide sous 150 personnes, `S_ideo` donne six camps, `S_camp` en
   donne trois et les trois ordres sont identiques. Faut il adopter `S_camp` comme
   segmentation de verdict du dossier, ce qui rendrait a44, a47 et R2 comparables, au prix
   d'un groupe plus grossier ? R2 est le premier rapport ou les deux segmentations donnent le
   meme classement, ce qui est un argument nouveau en sa faveur.
5. **Le repli sur la seconde passe.** La limite 1 de la section precedente joue contre le
   jumeau, pas pour lui. Faut il faire une nuit courte de passe 2 sur C3F gpt-oss avant de
   publier un resultat negatif, pour retirer a un rapporteur l'objection « votre jumeau etait
   handicape par l'ordre des modalites » ? Elle coute 8 700 appels, soit 4,5 heures au debit
   mesure.
6. **Que faire de `C3` maintenant ?** Ses 105 personnes, cousins conserves, sont la meilleure
   demonstration du dossier que la comparaison non appariee fabrique un avantage : sept
   succes sous Holm d'un cote, zero de l'autre, meme modele, memes personnes, memes items,
   une seule difference dans l'invite. Faut il en faire une **figure a part** dans le papier,
   plutot qu'une ligne de tableau ?

---

## Rejouer

```bash
# 1. l'evaluation, zero appel de modele, lecture seule sur data/traces/
.venv/bin/python analyses/r2_evaluer.py --tirages 4000 --permutations 200 --suffixe=-def

# 2. la puissance, les deux ponts et la figure, zero appel
.venv/bin/python analyses/r2b_puissance.py --tirages 4000

# 3. le controle qui valide la chaine de mesure, sur la trace a5 seule
.venv/bin/python analyses/r2_evaluer.py --essai-sur-a5 --tirages 4000 --permutations 200

# 4. completer C3, si la machine se libere et si la decision de la question 1 est oui
.venv/bin/python analyses/r2_rares_apparie.py --conditions C3 --fin 23:00
```

**Fichiers.** Page de plan `resultats/r2-preenregistrement.md` (22:05:00, non modifiee).
Rapport de lancement `resultats/r2-rares-apparie.md`. Mesures definitives
`resultats/r2-couverture-def.csv`, `r2-tableau-def.csv`, `r2-contrastes-def.csv`,
`r2-permutation-def.csv`, `r2-croises-def.csv`, `r2-controles-def.csv`. Complements
`resultats/r2b-puissance.csv`, `r2b-cellules-par-personne.csv`, `r2b-pont-modeles.csv`,
`r2b-ecarts-a-la-statistique.csv`, `r2b-pont-regimes.csv`. Figure
`resultats/r2b-figure-rares.png` et `.svg`. Traces `data/traces/r2-C3F-gptoss.jsonl`
(md5 97ed4603f8f0214485b732d43d589e2b) et `r2-C3-gptoss.jsonl`
(md5 42df59251588f4ffc8e314c6a899b855), journal `data/traces/r2-run.log`, evaluation
`data/traces/r2-evaluation.log`.
