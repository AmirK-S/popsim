# R3, resultats. La vraie ablation de l'etiquette, a un seul facteur

Rapport du 9 septembre 2026, ecrit apres le run et apres l'evaluation. Il execute le
**verrou 1** de `MODELE-DU-MONDE.md` section 11.5 et l'**objection bloquante numero 1** de
`resultats/a45-relecture-adverse-2.md`. Il rend compte contre la page de plan
`resultats/r3-preenregistrement.md`, **horodatee du 8 septembre 2026 a 22:30:01 CEST**,
ecrite avant le moindre appel de modele de langage de R3 et non modifiee depuis. En cas de
divergence, la page de plan fait foi contre ce rapport.

Aucun fichier existant n'a ete modifie pour ecrire ce rapport. Les mesures viennent de
`analyses/r3_evaluer.py`, deja joue a 08:00 (`data/traces/r3-evaluation.log`), et d'un
script complementaire nouveau, `analyses/r3b_appariement.py`, qui n'ecrit que des fichiers
`r3b-*` et qui repare un defaut de perimetre d'items decrit en section 3. Zero appel de
modele de langage dans les deux. Figure : `analyses/r3b_figure.py`.

Convention de marquage : **[MESURE]** une valeur produite par un calcul fait ici ou lue dans
un tableau produit cette nuit, **[CONFIRME]** un fait verifie sur un fichier ou une commande,
**[PROBABLE]** une lecture argumentee sans recalcul, **[HYPOTHESE]** le reste.

Reserve de forme, valable pour tout le dossier : popsim n'est pas sous suivi de version. Les
horodatages sont ceux de la machine et rien d'autre ne les atteste [CONFIRME, `git ls-files
resultats/` ne rend rien].

---

## Reponse en une ligne

**A information de la personne constante, l'etiquette demographique est la cause mesuree de
la caricature entre groupes et de l'exces de rarete de groupe, et elle n'est pas la cause de
la perte de la personne : ajoutee aux 119 reponses de C3, elle multiplie par 2,9 l'ecart
entre segments ideologiques (ratio inter 0,796 vers 2,344) et par 3,0 le lift de rarete de
segment (0,239 vers 0,728, Holm 0,0020), sans rien retirer du cote de la personne (lift de
personne plus 0,025, p 0,645) et sans changer d'un point ce qui se perd a permuter les
personnes a l'interieur de leur segment (0,455 contre 0,448 du plancher humain sous S_ideo,
0,511 contre 0,564 sous S_gra, p de Holm 0,950 et 0,988)** [MESURE, `r3-contrastes.csv`,
`r3b-contrastes-rarete.csv`, `r3b-plancher-humain.csv`, 94 personnes communes, 58 items].

**Dans le regime pauvre le meme geste fait tout : retirer les deux lignes politiques de C2
fait tomber le ratio inter sur l'axe ideologie de 10,077 a 0,038, Holm 0,0025, a exactitude
inchangee (0,5655 contre 0,5580, p 0,2125)** [MESURE, 130 personnes]. C'est l'analogue exact
de v6 contre v8 chez Stanford, et il est verifie : le critere de chute numero 2 de la page de
plan n'est pas declenche.

**Trois enonces du dossier ne survivent pas tels quels.** Un, « l'etiquette transforme un
agent en gabarit » : elle ne le fait pas quand les reponses de la personne sont la, et C3E
reste du cote « porteur de personne » au sens de a44 7.2, a 45 pour cent du plancher humain
comme C3. Deux, « la rarete de groupe remplace la rarete de la personne » : sur une ablation
propre, l'etiquette **ajoute** de la rarete de groupe et n'en retire pas du cote de la
personne, ce qui est le mecanisme de a31 2.3 et non une substitution. Trois, la lecture
causale de a42 section 6 se retourne : sur les raretes stables des 58 items et a perimetre
d'items apparie, **ajouter l'etiquette ameliore** l'exces sur le plancher de segment, de
plus 0,429 a plus 0,527 dans le regime riche (effet plus 0,098 [0,018 ; 0,175]) et de moins
0,148 a plus 0,047 dans le regime pauvre (effet plus 0,195 [0,075 ; 0,316]) [MESURE,
`r3b-contrastes-rarete.csv`].

**Un defaut de mesure a ete trouve dans l'evaluation de 08:00 et il est repare ici.** Quatre
lignes de `r3-contrastes.csv` comparent un bras mesure sur 58 items a un bras mesure sur 149.
La plus visible, « rappel des rares », publie une chute de 0,2485 a 0,1403 pour H1 ; a
perimetre d'items apparie l'effet change de signe et vaut **plus 0,0160 [0,0000 ; 0,0319]**,
p 0,073. Section 3.

**H3 n'est pas testee.** C3ES n'a pas tourne, la fin dure de 08:00 etant atteinte. L'effet H1
est donc celui du **bloc demographique entier**, onze attributs, et non celui des deux lignes
politiques. Le mot « etiquette » n'est exact, dans ce rapport, que pour H2.

---

## 0. Ce qui a tourne

| | |
|---|---|
| Modele | **Qwen3-4B-Instruct-2507**, GGUF **Q4_K_M**, le meme fichier que C2 et C3 de a5, gabarit `qwen`, variante de fin `answer`, `version_prompt` `r3-p1-qwen4-answer`, coupure de connaissances **non publiee** [CONFIRME, `r3-couverture.csv`, registre relu dans la trace] |
| Smoke test | masse mediane **0,99999**, masse minimale **0,99906**, part de modalites absentes **0,00** : passe, critere de chute numero 4 non declenche [MESURE, `r3-resume-qwen4.json`] |
| `C3E` | **94 personnes completes** sur 150, 1 partielle, **5 491 appels**, **0 rejet**, 3 274 appels/h, trace tronquee a 07:43 par la fin intermediaire |
| `C2S` | **130 personnes completes**, 1 partielle, **7 564 appels**, **0 rejet**, 26 872 appels/h, arret propre a 07:59 |
| `C3ES` | **non lancee**, fin dure atteinte avant son tour. `RUN TERMINE 2026-09-09 08:00:00` [CONFIRME, `r3-run.log`] |
| `C3` et `C2` | traces existantes `a5-C3-p1.jsonl` et `a5-C2-p1.jsonl`, 150 personnes, 149 items, non reecrites |
| Perimetre | **58 items** des six familles de `a2_baselines_gss`, repartis 10/12/14/10/12 sur les cinq blocs, les memes que R2 |
| Correction | **Holm par famille preenregistree**, F1 (5 tests), F2 (5 tests), F3 (1 test, non teste). Benjamini Hochberg publie a cote. IC bootstrap **apparie sur les personnes**, 2 000 tirages ; 200 tirages et 20 permutations pour la chute sous permutation, 200 permutations pour l'estimation ponctuelle [MESURE, `r3-controles.csv`] |

**Le debit projete etait faux dans les deux sens et cela n'a pas coute le run.** La page de
plan projetait 2,9 h pour C3E sur 150 personnes ; la sonde du matin a projete 1,89 h ; le
debit reel a ete de 3 274 appels/h contre 4 591 projetes, soit **29 pour cent en dessous**,
et C3E s'est arretee a 94 personnes au lieu des 75 a 90 annoncees [MESURE]. C2S a tourne a
26 872 appels/h contre 35 541 projetes. La regle de partage a fonctionne : H2 a eu son temps.

**La troncature n'est pas aleatoire, elle est par pli.** C3E couvre les plis 0, 1 et 2
entiers et 4 personnes du pli 3 ; C2S couvre les plis 0 a 3 entiers et 10 personnes du pli 4
[MESURE]. Les distributions restent proches de celles des 150 : ideologie, part de
« moderate » 0,287 contre 0,300 et de « liberal » 0,266 contre 0,240 ; genre, 0,585 de
femmes contre 0,560. Un ecart est a signaler : la part de repondants noirs tombe de **0,147
a 0,096** sur les 94 personnes de C3E [MESURE]. Aucune mesure de ce rapport n'est ponderee.

---

## 1. H1 : ajouter les onze attributs a C3, 94 personnes, 58 items

Convention de signe, celle du script : **effet = avec l'etiquette moins sans**. Toutes les
valeurs sur les memes personnes et les memes cellules.

### 1.1 Le tableau, mesure par mesure, avec le verdict preenregistre

| mesure | sens predit | C3 | C3E | effet | IC 95 % | p | p Holm F1 | verdict preenregistre |
|---|---|---|---|---|---|---|---|---|
| **chute sous permutation, S_ideo** | baisse | 0,0760 | 0,0755 | **moins 0,0005** | [moins 0,0065 ; 0,0070] | 0,475 | **0,950** | **non verifiee** |
| **chute sous permutation, S_gra** | baisse | 0,0695 | 0,0774 | **plus 0,0079** | [0,0004 ; 0,0107] | 0,988 | **0,988** | **non verifiee, effet contraire decidable** |
| ratio inter, S_ideo | hausse | 0,796 | **2,344** | plus 1,548 | *IC non lisible* | **0,0005** | hors F1 | **verifiee** |
| **ratio inter, S_gra** | hausse | 0,0507 | **0,3769** | plus 0,3262 | *IC non lisible* | 0,0015 | **0,0075** | **verifiee** |
| ratio intra, S_ideo | aucun | 0,663 | 0,672 | plus 0,0089 | [moins 0,0165 ; 0,0348] | 0,463 | hors F1 | conforme |
| ratio intra, S_gra | aucun | 0,693 | 0,796 | plus 0,1037 | [0,0585 ; 0,1445] | 0,0005 | hors F1 | **non conforme** |
| **groupe sur personne** | hausse | 0,819 | **3,233** | plus 2,414 | [0,910 ; 7,550] | 0,0020 | **0,0080** | **verifiee** |
| rappel des rares | aucun | 0,2485 | 0,1403 | moins 0,1082 | [moins 0,1445 ; moins 0,0760] | 0,0005 | hors F1 | **artefact, section 3** |
| **exactitude par personne** | hausse | 0,6205 | 0,6255 | plus 0,0050 | [moins 0,0029 ; 0,0128] | 0,1005 | **0,3015** | **verifiee au sens faible** |

[MESURE, `r3-contrastes.csv`, `r3-tableau.csv`]

**Lecture de l'IC du ratio inter.** L'effet ponctuel du ratio inter S_ideo vaut plus 1,548 et
l'intervalle percentile rendu par le bootstrap est [0,557 ; 1,126], qui **ne contient pas
l'effet**. Le meme defaut est signale par la page de plan section 9 point 4 sur le contraste
de reference. Ce n'est pas une erreur de code : c'est une propriete du ratio de sommes de
dispersion sous re echantillonnage des personnes, les segments se vidant et le seuil
`N_MIN_ITEM` de 30 changeant l'estimand d'un tirage a l'autre. **Le p unilateral reste
lisible comme test de signe, l'intervalle non**, et il n'est pas publie comme une borne. Un
bootstrap pivotal ou BCa reglerait le point, il n'est pas ecrit.

### 1.2 La chute sous permutation : elle ne bouge pas, et c'est contre H1a

C'est la mesure primaire de la page de plan, et **la prediction H1a attendait une baisse**.
Elle n'a pas lieu.

| | C3 | C3E | plancher humain, memes personnes, memes items | part du plancher, C3 | part du plancher, C3E |
|---|---|---|---|---|---|
| chute relative, **S_ideo** | 0,1225 | 0,1208 | **0,2693** | **0,455** | **0,448** |
| chute relative, **S_gra** | 0,1120 | 0,1237 | **0,2194** | **0,511** | **0,564** |

[MESURE, `r3b-plancher-humain.csv`, humains vague 2 sur les memes 94 personnes et les memes
58 items, 200 permutations]

Trois choses a en tirer, dans l'ordre.

1. **La prediction H1a est fausse, sous les deux segmentations.** Sous S_ideo l'effet est
   moins 0,0005, c'est a dire zero a la resolution du dispositif, p de Holm 0,950. Sous S_gra
   l'effet est **plus 0,0079 avec un IC qui exclut zero** [0,0004 ; 0,0107] : ajouter
   l'etiquette **augmente** legerement ce qui se perd a permuter les personnes. Il faut
   l'ecrire ainsi, et non « non significatif » : l'intervalle est du bon cote de zero, dans
   le sens **contraire** a la these.
2. **Le critere de chute de la page de plan n'est pas declenche.** Il exige que H1a soit
   rejetee dans le sens contraire **sous les deux segmentations**. Elle l'est sous une seule.
   La these de l'etiquette comme fabrique de gabarit ne tombe donc pas ; elle se retrecit,
   section 4.
3. **C3E reste du cote de la personne.** Le seuil de lecture de a44 7.2, gabarit sous 15 pour
   cent du plancher humain, porteur de personne au dessus de 40, classe C3 et C3E dans la
   meme case, 45 et 45 pour cent sous S_ideo, 51 et 56 sous S_gra. **Onze lignes de
   demographie, ideologie et parti compris, ne convertissent pas un agent riche en gabarit.**

Reserve de puissance a lire avec ces chiffres : sur les 94 personnes, la segmentation S_gra
compte **30 cases non vides et une seule de dix personnes ou plus** ; les autres comptent de
une a sept personnes, ou permuter est proche de l'identite [MESURE, `r3b-segments.csv`]. La
quantite reste definie au sens du repli de la page de plan, qui n'exige qu'une case a dix,
mais elle est portee par de petites cases et son intervalle est large. S_ideo compte 7 cases
dont 4 a dix personnes ou plus.

### 1.3 Le ratio inter : c'est la que l'etiquette agit, et de facon decidable

De 0,796 a **2,344** sur l'axe ideologie, de 0,051 a **0,377** sur genre x race x age. Le
signe est le meme sous les deux segmentations, ce que la page de plan exige. Le plancher est
1,000, la dispersion des humains de la vague 1 sur les memes items.

**Trois lectures.** Un, C3 **ecrase** l'ecart entre camps, 0,796, et C3E le **depasse**,
2,344 : l'etiquette ne deplace pas seulement la quantite, elle la fait changer de cote par
rapport aux humains. Deux, la meme chose se produit sur un axe que l'invite ne contient pas,
genre x race x age, 0,051 vers 0,377, ce qui interdit de lire l'effet comme une simple
recopie de la ligne `Political ideology`. Trois, le ratio **intra** bouge aussi sous S_gra,
plus 0,104 [0,0585 ; 0,1445], alors que la page de plan predisait « aucun » : l'etiquette
n'ecrase pas seulement entre les groupes, elle **elargit** aussi la dispersion a l'interieur
des cases de genre x race x age. Ce dernier point est **contre la these**, il est publie
ici, et il n'entre dans aucune famille corrigee.

### 1.4 La rarete : elle s'ajoute, elle ne se substitue pas

Perimetre d'items apparie, section 3, bootstrap apparie sur les personnes, 2 000 tirages.
La famille de reparation n'est **pas** preenregistree, son Holm est signale comme tel.

| mesure | C3 | C3E | effet | IC 95 % | p | p Holm, famille de reparation | humains vague 2 |
|---|---|---|---|---|---|---|---|
| **lift de rarete de segment** | 0,239 | **0,728** | plus 0,489 | [0,324 ; 0,667] | 0,0005 | **0,0020** | 0,452 |
| **lift de rarete de personne** | 0,200 | 0,225 | plus 0,025 | [moins 0,076 ; 0,133] | 0,645 | 0,645 | **0,797** |
| **groupe sur personne** | 1,193 | **3,233** | plus 2,039 | [0,607 ; 6,042] | 0,0125 | 0,0376 | **0,568** |
| rappel des rares | 0,124 | 0,140 | plus 0,016 | [0,000 ; 0,032] | 0,073 | 0,146 | 0,142 |
| raretes osees | 267 | 292 | plus 25 | [moins 1 ; 53] | 0,074 | | 146 |

[MESURE, `r3b-contrastes-rarete.csv`, 94 personnes, 58 items]

**C'est le resultat de mecanisme le plus net du run, et il ne dit pas ce que le dossier
attendait.** Ajouter l'etiquette **multiplie par 3,0 le lift de rarete de segment** et
**ne retire rien** du lift de rarete de personne. Le rapport groupe sur personne monte parce
que son numerateur monte, pas parce que son denominateur baisse. C'est mot pour mot le
mecanisme que a31 section 2.3 avait lu sur le contraste confondu C2 contre C3, « donner
l'etiquette ajoute de la rarete de groupe et n'ajoute rien du cote de la personne », et
**c'est la seule des six mesures anterieures qui traverse l'ablation propre sans changer
d'enonce**.

Sur les **raretes stables** de la partition P_A de a42, seuil 0,10, 71 cellules sur les 58
items, secondaires et sous puissantes par declaration de la page de plan [MESURE,
`r3-rarete.csv` et `r3b-contrastes-rarete.csv`] :

| | C3 | C3E | effet | IC 95 % | p |
|---|---|---|---|---|---|
| rappel des raretes stables | 0,535 | **0,634** | plus 0,099 | [0,027 ; 0,173] | 0,012 |
| exces sur le plancher de segment | 0,429 | **0,527** | plus 0,098 | [0,018 ; 0,175] | 0,030 |
| exces sur le plancher d'item | 0,454 | **0,552** | plus 0,099 | [0,027 ; 0,173] | 0,012 |
| precision sur les raretes stables | 0,193 | 0,217 | plus 0,025 | [moins 0,000 ; 0,052] | 0,056 |

**Ajouter l'etiquette ne fait pas perdre les gens rares reels : elle en fait retrouver dix
points de plus**, sur les seules raretes que la personne redonne deux semaines plus tard.
Le plancher humain de cette ligne vaut 1,000 **par construction**, la stabilite etant definie
par l'accord avec la vague 2 : ce n'est pas une reference exploitable et la figure le trace
en pointille.

### 1.5 L'exactitude : egale

Plus 0,0050 [moins 0,0029 ; 0,0128], p 0,1005, Holm 0,3015. **H1d est verifiee au sens
faible** : ajouter de l'information vraie ne nuit pas. Elle n'est pas verifiee au sens fort,
l'intervalle contenant zero. Deux consequences. Un, tout ce qui precede se lit **a exactitude
constante** : l'etiquette ne s'achete ni ne se paie en justesse, elle deplace la forme de la
population. Deux, l'objection de a47 E5, la chute sous permutation partage 82 pour cent de sa
variance avec l'exactitude brute, ne mord pas ici : l'exactitude ne bouge pas et la chute non
plus, les deux sont coherentes.

### 1.6 Score des predictions H1

| | enonce | direction | issue |
|---|---|---|---|
| **H1a** | la chute sous permutation **diminue** de C3 a C3E | en faveur | **fausse**. Nulle sous S_ideo (Holm 0,950), **de signe contraire et decidable** sous S_gra (IC [0,0004 ; 0,0107]) |
| **H1b** | le ratio inter **augmente** | en faveur | **tenue**, sous les deux segmentations, S_gra Holm 0,0075 |
| **H1c** | la rarete de groupe sur personne **augmente** | en faveur | **tenue**, Holm 0,0080 ; tenue aussi a perimetre apparie, plus 2,04 |
| **H1d** | l'exactitude de C3E est **superieure ou egale** | neutre | **tenue au sens faible**, plus 0,0050, IC contenant zero |

**Une sur quatre est fausse, et c'est la primaire.** Deux mesures publiees hors famille vont
egalement contre l'enonce du dossier : le ratio intra sous S_gra augmente au lieu de rester
stable, et le rappel des raretes stables augmente au lieu de baisser.

---

## 2. H2 : retirer l'ideologie et le parti de C2, 130 personnes, 58 items

| mesure | sens predit | C2S | C2 | effet | IC 95 % | p | p Holm F2 | verdict |
|---|---|---|---|---|---|---|---|---|
| **ratio inter, S_ideo** | hausse | **0,0385** | **10,077** | plus 10,038 | *IC non lisible* | 0,0005 | **0,0025** | **verifiee** |
| chute sous permutation, S_ideo | baisse | 0,0041 | moins 0,0025 | moins 0,0066 | [moins 0,0128 ; moins 0,0001] | 0,020 | **0,080** | non retenue |
| chute sous permutation, S_gra | baisse | 0,0020 | 0,0283 | plus 0,0263 | [0,0119 ; 0,0318] | 1,000 | **1,000** | **non verifiee** |
| groupe sur personne | hausse | **non defini** | 3,144 | non defini | [moins 34,2 ; 26,7] | 0,297 | 0,6375 | **non testable** |
| exactitude par personne | bilaterale | 0,5580 | 0,5655 | plus 0,0076 | [moins 0,0109 ; 0,0251] | 0,2125 | 0,6375 | **egale** |
| ratio inter, S_gra | hausse | 1,308 | 0,564 | moins 0,745 | *IC non lisible* | 0,046 | hors F2 | contraire |
| ratio intra, S_ideo | aucun | 0,258 | 0,251 | moins 0,0066 | [moins 0,066 ; 0,048] | 0,766 | hors F2 | conforme |
| ratio intra, S_gra | aucun | 0,201 | 0,687 | plus 0,486 | [0,381 ; 0,609] | 0,0005 | hors F2 | non conforme |
| rappel des rares | aucun | 0,0015 | 0,1191 | plus 0,1176 | [0,086 ; 0,152] | 0,0005 | hors F2 | voir section 3 |

[MESURE, `r3-contrastes.csv`]

### 2.1 Le ratio inter sur l'ideologie : de 10,1 a 0,04

**C'est le resultat le plus fort du run.** Deux lignes de texte retirees d'une invite de 591
caracteres, et l'ecart entre camps ideologiques passe de **dix fois** celui des humains a
**un vingt sixieme** de celui des humains, a exactitude egale a un demi point pres. C2S ne
distingue plus les camps du tout : sa dispersion inter est trente fois plus petite que celle
des vrais repondants.

Le critere de chute numero 2 de la page de plan, « la lecture v6 contre v8 », exigeait pour
tomber que H2a ne soit pas verifiee. **Elle l'est, largement.** L'analogie entre nos
conditions et le couple v6 / v8 de Stanford tient, et elle tient maintenant sur une ablation
a un facteur et non sur un contraste de conditionnement.

Reserve : cette mesure est une **quantite de gabarit** au sens de a44 section 3.1, exactement
invariante sous permutation des personnes a l'interieur d'un segment et reproductible par un
generateur qui tire dans la marginale de segment. Elle dit que les marginales par camp de C2
different de celles des humains, et rien de plus sur les personnes. C'est vrai avant comme
apres l'ablation ; ce que R3 ajoute est la **cause** de cette difference de marginales, et
elle est bien l'etiquette.

### 2.2 La chute sous permutation : nulle dans les deux, et le signe change d'une segmentation a l'autre

Part du plancher humain, memes 130 personnes, memes 58 items [MESURE,
`r3b-plancher-humain.csv`, plancher humain 0,2834 sous S_ideo et 0,2337 sous S_gra] :

| | C2S | C2 |
|---|---|---|
| part du plancher humain, **S_ideo** | 0,026 | **moins 0,016** |
| part du plancher humain, **S_gra** | 0,016 | **0,214** |

**C2 est un gabarit avec ou sans l'ideologie.** Sous S_ideo les deux sont a deux pour cent ou
moins du plancher humain, du cote des temoins aveugles a la personne de a44 ; permuter les
personnes a l'interieur de leur camp coute a C2 une exactitude **negative**, c'est a dire
rien. Retirer l'etiquette ne rend pas la personne, parce qu'il n'y a aucune personne a
rendre : neuf attributs demographiques ne sont pas une personne.

Sous S_gra le signe s'inverse et H2b echoue franchement, p unilateral 1,000. La lecture est
mecanique et elle merite d'etre ecrite parce qu'elle borne l'instrument : sous une
segmentation genre x race x age, la ligne `Political ideology` est **elle meme** une variable
discriminante a l'interieur de la case, puisque l'ideologie varie a genre, race et age fixes.
La chute de C2 sous S_gra, 21 pour cent du plancher humain, ne mesure donc pas que C2 porte
la personne : elle mesure que C2 porte **l'etiquette**, qui n'est pas dans la segmentation.
La retirer fait tomber la chute a 1,6 pour cent. **C'est le symetrique exact de l'objection 2
de a45**, qui reprochait a S_ideo de permuter a l'interieur de la variable que l'invite
contient ; ici c'est S_gra qui laisse dehors une variable que l'invite contient. Aucune des
deux segmentations n'est neutre pour une condition a etiquette, et la mesure de personne
n'est propre que pour une condition dont l'invite ne contient aucune des variables de la
segmentation, ce qui est le cas de C3 et de C3E sous S_gra, et d'aucune condition sous
S_ideo.

### 2.3 Pourquoi le rapport groupe sur personne n'est pas defini pour C2S

La page de plan predisait sa baisse (H2c). Il n'est pas defini, et la raison n'est pas
« plus aucune rarete de groupe osee » [MESURE, `r3b-rarete-appariee.csv`, perimetre apparie].

| | C2 | C2S | humains vague 2 |
|---|---|---|---|
| modalites rares **osees** sur 7 540 cellules | **254** | **20** | 185 |
| fausses raretes | 219 | 19 | 97 |
| lift de rarete de **personne** | plus 0,288 | **moins 0,016** | plus 0,654 |
| lift de rarete de **segment** | plus 1,405 | plus 0,162 | plus 0,295 |
| rapport groupe sur personne | 4,885 | **non defini** | 0,451 |

La definition de a31 section 2.3, reprise sans retouche par `a44_commun.groupe_sur_personne`,
rend `NaN` des que le **denominateur** est negatif ou nul. C'est le cas : le lift de personne
de C2S vaut moins 0,016. Et la cause est en amont : **C2S n'ose presque plus aucune modalite
minoritaire du tout**, 20 cellules sur 7 540, soit 0,27 pour cent, contre 3,4 pour cent pour
C2 et 2,5 pour cent chez les vrais repondants reinterroges. Prive de ses deux lignes
politiques, l'agent se replie sur la modalite majoritaire. Ses dix neuf fausses raretes ne
suffisent pas a faire monter le lift de personne au dessus de son temoin aveugle a la
personne, et le rapport devient un zero sur zero.

**Ce qu'il faut ecrire, et ne pas ecrire.** Ne pas ecrire « la rarete de groupe disparait » :
le lift de segment de C2S reste positif, plus 0,162. Ecrire : **retirer l'ideologie et le
parti fait passer le nombre de raretes osees de 254 a 20, et le rapport groupe sur personne
cesse d'etre defini faute de denominateur**. H2c est **non testable sur cette definition**,
pas « non verifiee ». Le contraste bootstrap publie pour elle, p 0,297, Holm 0,6375, porte
sur une difference de `NaN` et n'a aucun contenu ; il ne doit pas etre cite.

### 2.4 Score des predictions H2

| | enonce | direction | issue |
|---|---|---|---|
| **H2a** | le ratio inter sur l'ideologie **tombe** de C2 a C2S | en faveur | **tenue**, 10,077 vers 0,038, Holm 0,0025 |
| **H2b** | la chute sous permutation **augmente** sous S_ideo | en faveur | **non retenue**. Le signe est le bon, p 0,020, mais Holm 0,080 ; et le signe s'inverse sous S_gra, ou la page de plan ne prevoyait rien mais ou la chute s'effondre |
| **H2c** | le rapport groupe sur personne **diminue** | en faveur | **non testable**, denominateur non defini |
| **H2d** | exactitude, bilaterale | neutre | **egale**, plus 0,0076, p 0,2125 |

### 2.5 H3, non testee

C3ES n'a pas tourne. Les deux contrastes H3a (C3E contre C3ES) et H3b (C3ES contre C3) sont
declares **non testes**, jamais « non rejetes » [CONFIRME, `r3-contrastes-couverture.csv`].
Consequence de fond : **R3 ne separe pas, dans le regime riche, l'etiquette ideologique des
neuf autres attributs**. L'effet H1 est celui des onze lignes ensemble. Le mot « ablation de
l'etiquette » n'est exact que pour H2.

Reprise, une heure de machine, aucun serveur ne devant tourner :

```bash
.venv/bin/python analyses/r3_ablation_etiquette.py --conditions C3ES --fin 12:00 \
    >> data/traces/r3-run.log 2>&1
.venv/bin/python analyses/r3_evaluer.py --tirages 2000 --tirages-permutation 200 \
    --permutations 200 --suffixe=-avec-c3es
```

---

## 3. Un defaut de perimetre d'items dans l'evaluation de 08:00, et sa reparation

**Ce que le code fait** [CONFIRME, lecture de `analyses/r3_evaluer.py`, fonction `mesurer`
lignes 344 a 383]. L'exactitude, les deux ratios de dispersion et la chute sous permutation
sont restreints aux 58 items de famille, par `pred[:, colonnes]` ou par le parametre
`colonnes` passe a `C44.ratios`. La famille de mesures de rarete de a29 et a31 ne l'est pas :
`C44.groupe_sur_personne(pred, ctx["cv"]["S_ideo"])` recoit la matrice **149 colonnes**
entiere, et son denominateur, le nombre de cellules rares vraies, court sur les 149 items.

**Pourquoi cela cree un ecart.** Les traces de R3 ne couvrent que les 58 items de famille ;
les traces de a5 en couvrent 149 [MESURE, `r3b-couverture-items.csv`, 58 items couverts pour
C3E et C2S, 149 pour C3 et C2, dont 91 hors des familles]. Les quatre quantites
`lift personne`, `lift segment`, `groupe sur personne` et `rappel des rares` de
`r3-contrastes.csv` comparent donc **un bras mesure sur 58 items a un bras mesure sur 149**.
Le controle de placebo de la page de plan, la meme trace lue deux fois, ne pouvait pas le
voir, les deux bras y ayant le meme perimetre.

**L'ampleur, mesuree.** `analyses/r3b_appariement.py` recalcule les memes quantites avec les
memes fonctions, apres avoir masque les predictions des deux bras hors des 58 items.

| contraste | mesure | effet publie a 08:00 | effet a perimetre d'items **apparie** |
|---|---|---|---|
| H1 | **rappel des rares** | **moins 0,1082** | **plus 0,0160** [0,0000 ; 0,0319] |
| H1 | groupe sur personne | plus 2,414 | plus 2,039 [0,607 ; 6,042] |
| H1 | lift de segment | *non publie* | plus 0,489 [0,324 ; 0,667] |
| H1 | lift de personne | *non publie* | plus 0,025 [moins 0,076 ; 0,133] |
| H2 | rappel des rares | plus 0,1176 | plus 0,0519 [0,027 ; 0,080] |
| H2 | groupe sur personne | non defini | non defini, C2 passe de 3,144 a 4,885 |

[MESURE, `r3b-contrastes-rarete.csv`]

**Ce qui change et ce qui ne change pas.** Le seul renversement est le **rappel des rares de
H1** : la « chute de 0,25 a 0,14 » est un artefact de couverture d'items, et sur les memes
cellules l'effet est positif et non decidable. Les autres directions tiennent : le rapport
groupe sur personne monte toujours, de facon decidable, dans les deux lectures. Le tableau
`r3-rarete.csv`, qui porte les raretes stables, **n'est pas touche** : ses masques passent
par `restreindre(..., colonnes)` des deux cotes, numerateur et denominateur [CONFIRME,
lecture de `r3_evaluer.mesures_rares`].

**Statut de la reparation.** Elle n'est **pas preenregistree**. Son Holm est calcule sur une
famille de quatre tests declaree ici, jamais substituee a F1 et F2. Les tableaux de 08:00 ne
sont pas reecrits ; les deux lectures sont publiees cote a cote, et c'est la lecture
appariee qui doit etre citee pour toute quantite de rarete.

---

## 4. La lecture d'ensemble : ce que l'etiquette fait, et ce qu'elle ne fait pas

### 4.1 Ce qu'elle fait, a exactitude constante

1. **Elle fabrique la caricature entre groupes.** Regime riche, ratio inter S_ideo 0,796 vers
   2,344, facteur 2,9, et l'ecart passe **au dessus** des humains apres avoir ete en dessous.
   Regime pauvre, 0,038 vers 10,077, et l'ecart passe de rien a dix fois les humains. Sur un
   axe que l'invite ne contient pas, genre x race x age, le meme geste fait 0,051 vers 0,377.
   [MESURE]
2. **Elle ajoute de la rarete de groupe.** Lift de segment 0,239 vers 0,728 dans le regime
   riche, 0,162 vers 1,405 dans le regime pauvre, les deux a Holm 0,0020 sur la famille de
   reparation. Chez les humains reinterroges il vaut 0,452 et 0,295 : **C3E et C2 depassent
   les humains sur la rarete de groupe**, C3 et C2S sont en dessous. [MESURE]
3. **Elle fait oser des modalites minoritaires.** 267 vers 292 dans le regime riche, **20 vers
   254** dans le regime pauvre. Sans elle, C2S se replie sur la modalite majoritaire.
4. **Elle ne coute pas d'exactitude et n'en rapporte pas**, plus 0,0050 et plus 0,0076, les
   deux intervalles contenant zero. C'est ce qui rend l'effet interessant : il est invisible a
   l'instrument que la litterature emploie.

### 4.2 Ce qu'elle ne fait pas

1. **Elle ne retire pas la personne quand ses 119 reponses sont donnees.** La chute sous
   permutation ne bouge pas, 0,455 contre 0,448 du plancher humain sous S_ideo, et elle
   **augmente** un peu sous S_gra, 0,511 contre 0,564. Ce qui porte la personne dans C3 est
   le conditionnement sur ses reponses ; l'etiquette se pose a cote sans le detruire.
2. **Elle ne remplace pas la rarete de la personne par celle du groupe.** Le lift de personne
   ne baisse pas, plus 0,025 [moins 0,076 ; 0,133] et plus 0,303 [moins 0,107 ; 0,712]. Le
   rapport groupe sur personne monte **par son numerateur**. Le mot juste est **addition**,
   pas substitution.
3. **Elle ne fait pas perdre les gens rares reels.** Sur les raretes stables des 58 items,
   perimetre apparie, l'ajouter fait gagner plus 0,099 de rappel dans le regime riche et
   plus 0,227 dans le regime pauvre. La chute mesuree par a42 entre C3 et C2 est le facteur
   d'information, pas le facteur d'etiquette.

### 4.3 Les six mesures anterieures, une par une

Aucune des six n'etait une ablation propre. Voici ce que R3 en fait.

| mesure | ce qu'elle disait | ce que R3 en fait |
|---|---|---|
| **a19** : ajouter l'etiquette ideologique a un agent demographique multiplie par 25 le gonflement, 0,34 vers 8,51, sans changer l'exactitude d'un point (v6 contre v8, Stanford) | contraste a un facteur, mais chez Stanford | **confirmee sur nos conditions**, avec un facteur plus grand : 0,038 vers 10,077 a exactitude egale a 0,8 point pres. Notre C2S est un analogue plus propre de v6 que v6 lui meme, qui recopie ses items d'etat civil (a47 E6) |
| **a23** : ratio inter 8,16 [5,43 ; 15,55] avec l'etiquette, 0,73 [0,47 ; 0,99] sans | **a reformuler**. Le « sans » etait C3, qui n'est pas C2 sans etiquette. Le vrai « sans » est C2S, a **0,038**, vingt fois plus bas encore. Le chiffre de a23 **sous estimait** l'effet de l'etiquette et lui donnait le mauvais comparateur | ecrire « 10,1 avec l'etiquette contre 0,04 sans, a conditionnement constant », et garder 8,16 contre 0,73 comme contraste de conditionnement |
| **a30** : le camp de gauche de C2 est litteralement unanime | quantite de gabarit (a30 E1), et non rejouee sous ablation | **non tranchee par R3**. L'effondrement du ratio inter de C2S la rend probable, elle n'est pas mesuree. Elle se rejoue sur la trace C2S sans un seul appel [PROBABLE] |
| **a31** : donner l'etiquette ajoute de la rarete de groupe (plus 0,034, Holm 0,0012) et n'ajoute rien du cote de la personne (moins 0,001, p 0,554) | contraste confondu | **confirmee telle quelle, dans les deux regimes**. C'est la seule des six qui traverse l'ablation propre sans changer d'enonce. Son rapport 7,37 reste une quantite de gabarit (a31 E1) ; ce que R3 ajoute est sa **cause** |
| **a38** : facteur d'amplification de l'ecart entre camps 1,62 pour C2 contre 0,52 pour C3, « l'etiquette produit la caricature » | quantite de gabarit (a47 E3), contraste confondu (a38 E1) | **direction confirmee par un instrument voisin**, le ratio inter, dans les deux regimes. Le facteur d'amplification lui meme n'a **pas** ete recalcule sous C3E et C2S ; il se recalcule sans appel. Ecrire « l'etiquette produit la caricature **entre groupes** », jamais « seule l'etiquette change » sans dire que R3 le mesure sur onze attributs et non sur la seule ligne ideologique |
| **a42** : donner l'etiquette fait passer l'exces sur le plancher de segment de plus 0,162 a plus 0,033 sur les raretes stables | contraste confondu (a42 E1) | **retournee**. A perimetre apparie, ajouter l'etiquette **augmente** l'exces, plus 0,429 vers plus 0,527 dans le regime riche et moins 0,148 vers plus 0,047 dans le regime pauvre. L'ecart mesure par a42 est le facteur d'information |

**Bilan : une confirmee telle quelle (a31), deux confirmees avec une valeur differente et un
comparateur a corriger (a19, a23), une retournee (a42), une confirmee en direction seulement
et sur un autre instrument (a38), une non tranchee (a30).**

---

## 5. Ce que cela change au dossier

### 5.1 `MODELE-DU-MONDE.md` section 10.4

**Phrase d'origine.** « L'etiquette ideologique est ce qui transforme un agent en gabarit : le
meme modele, les memes personnes et les memes questions donnent 7 pour cent du plancher avec
l'etiquette et 45 pour cent sans. »

**Phrase de remplacement proposee.** « L'etiquette demographique est la cause mesuree de la
caricature entre groupes et de l'exces de rarete de groupe, et elle n'est pas la cause de la
perte de la personne. A information de la personne constante, l'ajouter aux 119 reponses de
C3 multiplie par 2,9 l'ecart entre segments ideologiques et par 3,0 le lift de rarete de
segment, sans retirer de rarete de personne et sans changer la part du plancher humain perdue
sous permutation, 0,455 contre 0,448 sous la segmentation ideologique et 0,511 contre 0,564
sous genre x race x age. A conditionnement constant, retirer l'ideologie et le parti des onze
attributs de C2 fait tomber le ratio inter sur l'axe ideologie de 10,077 a 0,038, a exactitude
egale, et fait passer le nombre de modalites minoritaires osees de 254 a 20. Le sept pour cent
contre quarante cinq est le facteur d'information, pas le facteur d'etiquette. »

**Ou se range l'issue dans le tableau de la page de plan section 8.** Aucune des six lignes ne
convient exactement. La plus proche est « H1a nulle, H2a verifiee », qui donne « l'etiquette
n'agit que dans le regime pauvre » ; elle est **trop forte**, parce que H1b et H1c sont
verifiees et que l'etiquette agit donc aussi dans le regime riche, sur le gonflement et sur la
rarete de groupe. L'issue reelle est une septieme : **l'etiquette agit dans les deux regimes,
mais sur des quantites de gabarit, et sur aucune quantite de personne.**

### 5.2 `MODELE-DU-MONDE.md` section 11

- 11.2, « L'ablation propre est R3, en cours [EN ATTENTE] » : remplacer par les deux resultats.
  La phrase « la substitution de la personne par le groupe est propre au conditionnement, pas
  au moteur » **tient et se renforce** : R3 montre que ce n'est pas non plus l'etiquette.
- 11.2, la mesure de personne depend de la segmentation : **le point s'aggrave et se
  symetrise**. Sous S_gra, la chute de C2 mesure ce que porte l'etiquette et non ce que porte
  la personne, section 2.2. Ecrire : « la chute sous permutation n'est une mesure de personne
  que pour une condition dont l'invite ne contient aucune variable de la segmentation ».
- 11.4, phrase une : la clause « la part propre a l'etiquette est celle que R3 mesure [EN
  ATTENTE] » se ferme, dans le sens : la part propre a l'etiquette sur la **chute** est nulle,
  la part propre a l'etiquette sur le **gonflement** est la totalite dans le regime pauvre et
  un facteur 2,9 dans le regime riche.
- 11.5, verrou un : **ferme pour H1 et H2, ouvert pour H3.** Le placebo d'etiquette, etiquette
  permutee entre personnes, reste a faire ; il est maintenant moins urgent que C3ES, qui
  separerait les deux lignes politiques des neuf autres attributs pour une heure de machine.

### 5.3 `ARBITRAGE.md` point 2

**Phrase d'origine.** « A modele, personnes et questions constants, la seule presence de
l'etiquette fait la difference. Six mesures independantes le disent. »

**Remplacement.** « A modele, personnes, questions et traces constants, et sur une ablation a
un seul facteur, la presence de l'etiquette fait la difference sur l'ecart entre groupes et
sur la rarete de groupe, a exactitude egale ; elle ne la fait pas sur ce qui reste de la
personne quand ses reponses sont donnees. Des six mesures dites independantes, une est
confirmee telle quelle, deux avec un comparateur corrige, une est retournee, une n'est
confirmee qu'en direction, une n'est pas tranchee. »

### 5.4 `MOONSHOTS.md`, programmes A et B

**Programme A, la fidelite de representation des camps.** R3 lui donne son levier causal, et
c'est un argument de regulation et non de laboratoire : **une ligne de texte dans l'invite
systeme deplace l'ecart entre camps d'un facteur 2,9 a 260 sans deplacer l'exactitude d'un
demi point.** La quantite auditee est manipulable par le fournisseur du prompt, invisible a
l'instrument que le champ emploie, et le registre des versions doit donc consigner **si
l'invite porte une etiquette politique**, au meme rang que le modele et le protocole. Cela
renforce la conclusion de r1 section 5.2, « fixer un protocole et un registre avant de fixer
un seuil », en lui ajoutant un troisieme axe, le contenu de l'invite.

**Programme B, la bande humaine.** R3 fournit le plancher humain des quatre quantites sur les
memes personnes et les memes items, et il montre que ce plancher **n'est pas le meme sous deux
segmentations de finesse comparable**, 0,269 sous S_ideo et 0,219 sous S_gra sur 94 personnes,
0,283 et 0,234 sur 130 [MESURE, `r3b-plancher-humain.csv`]. La regle de la section 11.4 gagne
un mot : aucune quantite ne se publie sans le plancher de sa population, de son effectif, de
son delai, de son protocole **et de sa segmentation**.

### 5.5 La these finale, en trois phrases, R2 etant negatif

1. Une etiquette demographique, l'ideologie et le parti en tete, est la cause mesuree de la
   caricature entre groupes et de l'exces de rarete de groupe : a modele, personnes,
   questions, traces et exactitude constants, l'ajouter multiplie par 2,9 l'ecart entre camps
   quand les 119 reponses de la personne sont deja la, et le fait passer de 0,04 a 10,1 fois
   l'ecart humain quand elles n'y sont pas, en faisant passer de 20 a 254 le nombre de
   modalites minoritaires osees.
2. Elle n'est pas la cause de la perte de la personne : quand les reponses sont donnees,
   l'ajouter ne change pas ce qui se perd a permuter les personnes a l'interieur de leur
   segment, 45 pour cent du plancher humain avant comme apres ; ce qui porte la personne est
   le conditionnement sur ses reponses, et une regression sur les memes onze attributs perd
   autant de signal individuel que l'agent de langage.
3. Et ce que ce conditionnement achete ne survit pas au regime severe : sur un modele de 20
   milliards de parametres, la famille thematique retiree des deux cotes, le jumeau ne
   retrouve pas les gens rares reels mieux qu'un tirage au sort dans le segment de la personne
   et il est derriere l'imputation par appariement predictif (R2) ; le dossier tient donc un
   diagnostic sur ce que l'etiquette fabrique, et aucun avantage a defendre.

---

## 6. La figure

`resultats/r3b-figure-ablation-etiquette.png` et `.svg`, produites par
`analyses/r3b_figure.py`, qui ne recalcule rien et lit `r3b-plancher-humain.csv` et
`r3b-rarete-appariee.csv`.

Quatre panneaux, les memes quatre conditions dans le meme ordre sur chacun, dans le sens de
l'ajout : **C3 vers C3E**, puis **C2S vers C2**. Une fleche marque le geste. Le trait vert est
le plancher humain, la vague 2 sur les **memes** personnes et les **memes** 58 items : il y en
a deux par panneau, un par perimetre, 94 personnes pour H1 et 130 pour H2, parce que confondre
les deux serait une faute de denominateur.

1. La chute sous permutation en part du plancher humain, barres pour S_ideo et losanges pour
   S_gra. Les deux paires sont plates : c'est le resultat negatif.
2. Le ratio inter sur l'axe ideologie, plancher a 1,000. Les deux paires montent, la seconde
   d'un facteur 260.
3. Le rapport de rarete groupe sur personne, perimetre d'items apparie. C2S y est marque
   **non defini**, et non zero.
4. Le rappel des raretes stables sur les 58 items, perimetre apparie. Les deux paires montent.
   Le plancher humain y vaut 1,000 par construction et le trait est en pointille pour le dire.

---

## 7. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

- « A modele, quantification, temperature, personnes, questions et traces constants, et en ne
  changeant qu'un bloc de texte de 90 caracteres dans l'invite systeme, retirer les lignes
  `Political ideology` et `Political party` fait passer l'ecart entre camps ideologiques de
  10,1 a 0,04 fois celui des vrais repondants, a exactitude egale. » [MESURE, 130 personnes,
  58 items, Qwen3-4B Q4_K_M, argmax]
- « Ajoutee a une invite qui contient deja 119 reponses de la personne, l'etiquette
  demographique multiplie par 2,9 le meme ecart et par 3,0 le lift de rarete de segment, sans
  retirer de rarete de personne et sans changer l'exactitude. » [MESURE, 94 personnes]
- « L'etiquette ne retire pas la personne : la chute d'exactitude sous permutation intra
  segment de C3 vaut 45 pour cent du plancher humain avec et sans les onze attributs. »
  [MESURE, sous les deux segmentations, le signe des deux effets etant oppose et les deux
  intervalles voisins de zero]
- « Donner l'etiquette **ajoute** de la rarete de groupe sans en retirer du cote de la
  personne » : c'est le mecanisme de a31 2.3, replique sur une ablation propre dans les deux
  regimes d'information.
- « Le contraste C2 contre C3 du dossier melange deux facteurs, et la part imputable a
  l'etiquette est mesuree : elle est la totalite du gonflement dans le regime pauvre et
  aucune part de la chute sous permutation dans le regime riche. »
- « Le nombre de modalites minoritaires osees par un agent demographique passe de 254 a 20 sur
  7 540 cellules quand on lui retire ses deux lignes politiques, contre 185 chez les vrais
  repondants reinterroges. »

### Interdit

- **« L'etiquette transforme un agent en gabarit. »** Faux dans le regime riche : C3E reste a
  45 pour cent du plancher humain. Vrai seulement au sens ou C2 est deja un gabarit avant
  l'ablation, et le reste apres.
- **« Sept pour cent du plancher avec l'etiquette et quarante cinq sans. »** Ce contraste est
  celui de l'information, pas celui de l'etiquette. R3 le montre en tenant l'information
  constante des deux cotes.
- **« La rarete de groupe remplace la rarete de la personne. »** Le lift de personne ne baisse
  pas, p 0,645 et p 0,127. Ecrire « s'ajoute a ».
- **« L'etiquette fait perdre les gens rares reels. »** L'inverse est mesure sur les raretes
  stables a perimetre apparie, dans les deux regimes.
- **« Le rappel des rares tombe de 0,25 a 0,14 quand on ajoute l'etiquette. »** Artefact de
  couverture d'items, section 3. L'effet apparie vaut plus 0,016.
- **« R3 est l'ablation de l'etiquette ideologique. »** Pour H1, R3 ajoute **onze** attributs.
  Seul H2 isole les deux lignes politiques. C3ES n'a pas tourne.
- **« Le rapport groupe sur personne de C2S est nul. »** Il n'est **pas defini**. Le p de
  0,297 publie pour ce contraste porte sur une difference de `NaN`.
- Toute generalisation a un autre modele, une autre taille, un autre jeu, un autre regime de
  decodage ou un autre ordre de modalites.

---

## 8. Ce que je n'ai pas pu verifier

1. **H3 n'existe pas.** C3ES n'a pas tourne. Rien ne separe, dans le regime riche, l'effet des
   deux lignes politiques de celui des neuf autres attributs. Non teste, jamais non rejete.
2. **Le perimetre de C3E n'est pas aleatoire.** 94 personnes sur 150, prises dans l'ordre des
   plis. La part de repondants noirs y tombe de 0,147 a 0,096. Aucune mesure n'est ponderee et
   aucun test de sensibilite au perimetre n'a ete fait ; la comparaison C3E contre C3 est
   appariee sur les personnes, ce qui protege le contraste et non la representativite.
3. **L'IC du ratio inter n'est pas lisible.** Sur l'effet ponctuel plus 1,548, le percentile
   rend [0,557 ; 1,126], qui ne contient pas l'effet. Le p unilateral est publie comme test de
   signe ; l'intervalle ne l'est pas. Un bootstrap pivotal ou BCa reglerait le point, il n'est
   pas ecrit.
4. **La chute sous permutation est estimee au rabais dans le bootstrap.** 200 tirages et 20
   permutations par tirage, contre 200 permutations pour l'estimation ponctuelle. Ses
   intervalles sont grossiers. Sur 94 personnes, S_gra n'a qu'une case de dix personnes ou
   plus sur 30 cases non vides.
5. **La famille de reparation de la section 3 n'est pas preenregistree.** Ses p de Holm sont
   calcules sur une famille declaree apres avoir vu les chiffres de 08:00. Ils sont publies
   comme reparation d'un perimetre, jamais comme verdict.
6. **Le facteur d'amplification de a38, l'unanimite de a30 et la pente de a37 n'ont pas ete
   recalcules sous C3E et C2S.** Ils coutent zero appel et ils fermeraient les deux lignes
   « non tranchee » et « direction seulement » du tableau 4.3.
7. **La passe 2 n'existe pas pour R3.** Le biais de position des modalites n'est pas
   neutralise ; il est constant entre les conditions comparees, ce qui suffit pour un
   contraste et pas pour un niveau.
8. **Aucune condition n'est evaluee en tirage.** Argmax partout, objection 8 de a45. Les
   distributions sont dans la trace, un tirage se reconstruira sans appel.
9. **Un seul modele, 4 milliards de parametres, quantifie en 4 bits, un jeu, un pays, une
   invite.** Rien ici ne dit ce que l'etiquette fait a un modele plus gros, dont la capacite a
   exploiter 119 reponses est plus grande et qui sature peut etre moins vite.
10. **Le plancher humain de la ligne « raretes stables » vaut 1,000 par construction.** La
    stabilite est definie par l'accord avec la vague 2 ; ce n'est pas une reference
    exploitable, et je n'ai pas construit de plancher alternatif pour cette ligne.
11. **Rien de tout ceci n'est sous suivi de version**, ni la page de plan, ni les scripts, ni
    les traces. C'est l'objection ouverte de a45 et R3 ne la corrige pas.

---

## 9. Questions ouvertes pour Simon

1. **C3ES vaut il une heure de machine avant tout le reste ?** C'est le seul chiffre qui
   permettrait d'ecrire « l'etiquette **ideologique** » plutot que « le bloc demographique »
   dans le regime riche, et c'est la formulation que huit textes du dossier emploient. Une
   heure, aucun serveur ne devant tourner, la commande est en section 2.5.
2. **Quelle segmentation porte la these, maintenant que les deux sont piegees ?** S_ideo
   permute a l'interieur d'une variable que l'invite de C2 contient ; S_gra laisse dehors une
   variable que l'invite de C2 contient. Pour C3 et C3E, S_gra est propre. Pour C2 et C2S,
   aucune des deux ne l'est. Faut il construire une segmentation par les **reponses** et non
   par les attributs, ou renoncer a la chute sous permutation pour les conditions a etiquette
   seule ?
3. **Le retournement de a42 change t il la these deux ?** La derniere clause de la phrase deux
   de la section 11.4, l'avantage sur les gens rares, est deja detruite par R2 sur gpt-oss-20b.
   R3 y ajoute que l'etiquette **aide** sur les raretes stables au lieu de nuire. Faut il
   abandonner entierement l'etage « avantage » et n'ecrire qu'un dossier de diagnostic ?
4. **Le resultat H2 est il publiable seul ?** « Deux lignes de texte, un facteur 260 sur
   l'ecart entre camps, zero effet sur l'exactitude » est un enonce court, replicable a cout
   nul par n'importe qui, et il est exactement l'analogue de v6 contre v8 avec le controle que
   Stanford n'a pas fait. Faut il en faire une note separee plutot qu'une section d'un dossier
   dont la these principale est negative ?
5. **Faut il refaire le meme protocole sur un modele serieux avant de publier ?** Un relecteur
   dira que l'effet de l'etiquette depend de la capacite du modele a exploiter 119 reponses.
   Le meme protocole sur gpt-oss-20b coute une nuit ; il donnerait aussi la seule chose qui
   manque a la these une, la generalite.
6. **Que fait on des huit textes ?** a45 proposait de remplacer partout « ablation de
   l'etiquette » par « contraste de conditionnement ». R3 permet maintenant d'ecrire les deux :
   le contraste de conditionnement **et** l'ablation. Faut il reecrire les huit, ou ajouter une
   ligne d'erratum a chacun qui renvoie ici ?

---

## 10. Rejouer

Rien ne demande de serveur. Quatre coeurs, lecture seule sur `data/traces/`.

```bash
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# l'evaluation preenregistree, deja jouee a 08:00
.venv/bin/python analyses/r3_evaluer.py --tirages 2000 \
    --tirages-permutation 200 --permutations 200

# la reparation du perimetre d'items, le plancher humain et les tailles de segments
.venv/bin/python analyses/r3b_appariement.py --tirages 2000 --permutations 200

# la figure
.venv/bin/python analyses/r3b_figure.py
```

## 11. Fichiers

**Produits par ce rapport** : `analyses/r3b_appariement.py`, `analyses/r3b_figure.py`,
`resultats/r3b-couverture-items.csv`, `r3b-rarete-appariee.csv`,
`r3b-contrastes-rarete.csv`, `r3b-plancher-humain.csv`, `r3b-segments.csv`,
`r3b-figure-ablation-etiquette.png` et `.svg`, et ce fichier.

**Lus, non modifies** : `resultats/r3-preenregistrement.md`, `r3-ablation-etiquette.md`,
`r3-couverture.csv`, `r3-contrastes-couverture.csv`, `r3-tableau.csv`, `r3-contrastes.csv`,
`r3-permutation.csv`, `r3-rarete.csv`, `r3-controles.csv` ;
`data/traces/r3-C3E-qwen4.jsonl`, `r3-C2S-qwen4.jsonl`, `r3-evaluation.log`, `r3-run.log`,
`r3-resume-qwen4.json`, `a5-C3-p1.jsonl`, `a5-C2-p1.jsonl`, `a5-personnes.csv` ;
`analyses/r3_evaluer.py`, `a44_commun.py`, `a42_commun.py`.
