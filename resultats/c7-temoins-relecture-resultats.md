# C7 — Témoins de relecture : mes chiffres, mes intervalles, mes écarts — UN CHIFFRE BORNÉ le 13 septembre 2026

statut: provisoire
borne_par: resultats/c7-residu-trajectoire-resultats.md
fait_foi: resultats/c7-temoins-relecture.csv (pour les chiffres de ce rapport) ; resultats/c7-residu-trajectoire-resultats.md (pour le contraste 2023 -> aujourd'hui, desormais interdit de publication chiffree)


mandat: T1a : reimplementer independamment les deux temoins de la relecture hostile du 13/09 (items apparies sur Twin, attaquant fort sur Argyle), appliquer le controle d'interpretabilite, rapporter mes propres chiffres avec IC bootstrap sur les personnes, et les declarer post-hoc et non preenregistres
agent: mesures / temoins de relecture (T1a), 13/09
ecriture: analyses/c7_temoins_relecture.py, resultats/c7-temoins-relecture-preenregistrement.md, resultats/c7-temoins-relecture-resultats.md, resultats/c7-temoins-relecture.csv
lecture_seule: tout le reste
interdits: appel payant, reseau, recherche web, commit sur master, fusion, ecriture hors des quatre fichiers du mandat
cout_reel_usd: 0.00

> ## BORNÉ, le 13/09/2026 — le contraste « 8,9× » ne doit plus être publié comme un facteur
>
> **État : BORNÉ** (le fait tient dans un périmètre plus étroit, et le périmètre est nommé).
> Fait foi : `resultats/c7-residu-trajectoire-resultats.md`, §9 et §10.
>
> Le tableau du §« Le rapport à la baseline, à nombre d'items apparié » publie
> **8,9×** (`c7-temoins-relecture.csv`, ligne `synthese`, colonne
> `contraste_twin_sur_argyle` = 8,878207) comme contraste 2023 → aujourd'hui à items
> appariés, et conclut qu'« il ne s'annule pas ».
>
> Ce qui est établi ensuite, et qui borne ce chiffre : **apparier le nombre brut d'items
> n'apparie rien.** À nombre d'items égal, les douze items Twin portent encore 46 %
> d'information indépendante de plus que les douze items ANES. Une fois cet excédent
> retiré, le contraste tombe de 9,6× à **2,53×** (`c7-residu-trajectoire.csv`, régime
> `M2 items effectifs = 4.31`, `rapport jumeau/demo` = 2,5293) — et son dénominateur
> (0,135 %, Argyle) **échoue son propre contrôle d'interprétabilité** et n'est pas
> estimable, ce qui rend le rapport indéfini, pas seulement petit.
>
> **Interdit à partir d'ici :** toute formulation portant un **facteur chiffré** entre les
> deux époques — « 150× », « 15× », « 10× », « 8,9× », et **y compris le 2,5×** du rapport
> qui borne celui-ci. Ce qui peut être publié est une **direction, pas une amplitude** :
> la formulation exacte est celle du §10 de `c7-residu-trajectoire-resultats.md`.
>
> **Ce qui tient sans réserve dans ce rapport** : les taux et intervalles du témoin T1
> (1,2193 % [1,1118 ; 1,3301] à k = 12), le témoin T2 sur Argyle, le contrôle
> d'interprétabilité, et surtout le constat que **le nombre d'items gonfle tout ce qui
> attaque**, baseline démographique comprise (facteur 7,41 de 12 à 60 items,
> `c7-temoins-relecture.csv`, `facteur_12_vers_60_items`) — constat repris et confirmé
> indépendamment par le rapport qui borne celui-ci.

> **POST HOC, NON PRÉENREGISTRÉ.** Les deux témoins de ce fichier ont été conçus après
> avoir vu les résultats qu'ils mesurent, en réponse à la relecture hostile du
> 13 septembre 2026. Ils ne comptent dans aucun dénominateur de multiplicité
> préenregistré et ne réfutent aucune prédiction préenregistrée. Cette mention doit
> suivre ces chiffres partout, manuscrit compris. Voir
> `resultats/c7-temoins-relecture-preenregistrement.md`, qui documente franchement une
> analyse déjà faite.

**Source qui fait foi : `resultats/c7-temoins-relecture.csv`**, produit en une exécution
par `analyses/c7_temoins_relecture.py` (graines fixées dans le code, aucun appel payant,
aucun réseau, lecture seule sur `data/`). Chaque nombre de ce fichier a sa ligne dans ce
CSV. Aucun chiffre n'est recopié du rapport de relecture : les tableaux de comparaison
ci-dessous mettent en regard **ses** valeurs, citées depuis
`resultats/relecture-fond-2026-09-13.md`, et **les miennes**, issues du CSV.

**Dérivation indépendante.** Les scripts du relecteur (`temoin_trajectoire.py`,
`temoin_argyle_fort.py`) sont restés dans son scratchpad hors dépôt ; aucune de leurs
lignes n'a été lue. Seule la description de ses deux témoins (défauts D2 et D3) a servi
de cahier des charges. Là où nos chiffres diffèrent, **ils ne sont pas alignés** : un
écart est une information.

---

## Les deux témoins tirent en sens opposés, et les deux sont rapportés

| témoin | effet sur la thèse | verdict de ma mesure |
|---|---|---|
| **T1 — nombre d'items apparié** (en premier) | **affaiblit** | confirmé, et un peu plus fort : facteur **17,0**, pas 15,6 |
| **T2 — attaquant fort sur Argyle** (ensuite) | **renforce** | confirmé : même armé, le point 2023 échoue au contrôle |

T1, l'affaiblissant, passe **en premier** — décision du plan de révision (R1), pour que
la rédaction ne puisse pas mettre en avant le témoin qui arrange. Aucun des deux n'est
retenu au détriment de l'autre, ni ici ni dans le CSV.

---

# T1 — Témoin à nombre d'items apparié (Twin-2K-500)

Un seul jeu, une seule équipe, un seul modèle (`JSON Persona - GPT4.1`), une seule
attaque (Hamming naïf), les mêmes 2 058 personnes, le même pool. **La seule chose qui
change d'un point à l'autre est le nombre d'items.** k < 60 : 30 tirages d'items
indépendants sans remise parmi les 60 items toujours renseignés ; k = 60 : l'ensemble
entier.

## Ma courbe

| k items | top-1 jumeau (IC 95 % bootstrap **sur les personnes**) | étendue **entre les 30 tirages d'items** | top-1 `Demographics Only` | rapport |
|---|---|---|---|---|
| **12** | **1,2193 %** [1,1118 ; 1,3301] | 0,3401 – 3,0126 % | 0,2864 % [0,2413 ; 0,3346] | **4,26** |
| 20 | 3,2611 % [2,9726 ; 3,5650] | 1,5549 – 6,0544 % | 0,5565 % [0,4661 ; 0,6443] | 5,86 |
| 30 | 7,3353 % [6,7582 ; 7,9322] | 3,5374 – 11,3217 % | 0,8931 % [0,7337 ; 1,0629] | 8,21 |
| 40 | 11,0295 % [10,1140 ; 11,9322] | 4,7425 – 16,5015 % | 1,2514 % [1,0010 ; 1,5329] | 8,81 |
| **60** | **20,7191 %** [19,0402 ; 22,3837] | — (un seul tirage possible) | 2,1210 % [1,5524 ; 2,7309] | 9,77 |

**Raccordement vérifié.** À k = 60 je retrouve **20,7191 %** contre **20,694 %** publiés
et recalculés par le relecteur — troisième décimale près, écart imputable au tirage de
départage des ex æquo. Le portage est donc bon ; la règle d'arrêt §5 du préenregistrement
est satisfaite.

**Deux incertitudes, jamais confondues.** L'IC bootstrap sur les personnes et l'étendue
entre tirages d'items sont dans des colonnes distinctes du CSV et ne portent pas le même
nom. À k = 12 ils diffèrent d'un facteur 40 en largeur : [1,11 ; 1,33] contre
0,34 – 3,01. C'est exactement le défaut D6 que la relecture reproche au §5.9 de
l'article, et il ne sera pas reproduit ici.

## Ce que devient le facteur 15,6

| grandeur | relecteur | **moi** |
|---|---|---|
| top-1 jumeau, k = 12 | 1,323 % | **1,2193 %** [1,1118 ; 1,3301] |
| top-1 jumeau, k = 60 | 20,694 % | **20,7191 %** [19,0402 ; 22,3837] |
| **facteur 12 → 60 items, jumeau** | **15,6** | **17,0** |
| facteur 12 → 60 items, baseline démographique | non donné | **7,41** (0,2864 → 2,1210 %) |

**Le facteur 15,6 devient 17,0 dans ma mesure**, parce que mon k = 12 est plus bas
(1,22 % contre 1,32 %) alors que nos k = 60 coïncident. Je ne corrige pas cet écart. Son
origine la plus plausible : nos 30 tirages d'items ne sont pas les mêmes, et l'étendue
entre tirages à k = 12 couvre un facteur ~9 (0,34 – 3,01 %). Deux jeux de 30 tirages
peuvent parfaitement produire des moyennes à 8 % l'une de l'autre. **La conclusion est la
même et elle est même légèrement renforcée : le seul nombre d'items couvre plus d'un
ordre de grandeur de l'amplitude de la trajectoire.**

Chiffre nouveau, que le relecteur ne donne pas : **la baseline démographique gagne elle
aussi un facteur 7,4 entre 12 et 60 items.** Le nombre d'items ne gonfle donc pas
seulement le jumeau ; il gonfle tout ce qui attaque. C'est pourquoi le **rapport à la
baseline**, et non le taux nu, est la grandeur à publier.

## Le rapport à la baseline, à nombre d'items apparié

| | relecteur | **moi** |
|---|---|---|
| Twin 2025, 12 items, rapport à sa baseline | 4,3 | **4,26** |
| Argyle 2023, 12 items, rapport à sa baseline | 1,5 | **1,79** |
| contraste 2023 → aujourd'hui, à items appariés | ~10× | **8,9×** |

Sur le rapport Twin, nous sommes d'accord à la deuxième décimale. Sur Argyle je trouve
**1,79 et non 1,5**, parce que ma baseline B-demo sort à **0,0768 %** là où il annonce
0,0913 % (défaut D1) ou 0,1024 % (défaut D2) — **il donne lui-même deux valeurs
différentes pour cette baseline dans le même rapport**. À ce niveau, la baseline repose
sur **1 à 2 succès absolus sur 2 148** : les trois valeurs sont indiscernables et le
rapport 1,5 / 1,79 n'a pas de contenu. La conclusion qualitative tient quel que soit le
chiffre retenu : **à 12 items appariés, les jumeaux de 2025 battent nettement leur
baseline (4,26×) là où ceux de 2023 ne la battent pas de façon démontrable** (IC
largement chevauchants, voir T2 et le contrôle ci-dessous).

Le contraste 2023 → aujourd'hui tombe à **8,9×** chez moi, ~10× chez lui — même ordre,
et dans les deux cas **il ne s'annule pas**.

---

# T2 — L'attaquant fort appliqué à Argyle 2023

2 148 personnes complètes, 12 items, trois jumeaux GPT-3 publiés par l'équipe Argyle plus
la baseline démographique recalculée sur **ce** bassin. Les fonctions employées sont
exactement celles qui ont produit les chiffres de tête du manuscrit :
`c7_attaquant_fort.scores_hors_pli` (A-LLR, paramètres estimés hors pli),
`c7_monde_ouvert.marges_deux_regimes` et `roc_et_taux`. Rien n'est réimplémenté : c'est
l'intérêt du témoin, la métrique du bout **droit** appliquée au bout **gauche**.

## Monde fermé et monde ouvert

| jumeau Argyle | top-1 naïf (IC 95 % personnes) | top-1 **A-LLR** (IC 95 % personnes) | AUC ouvert (A-LLR) | TPR @ 1 % FPR |
|---|---|---|---|---|
| GPT-3 (temp. principale) | 0,1373 % [0,0466 ; 0,2700] | **0,2328 %** [0,0466 ; 0,4655] | **0,0013** | **0,0466 %** |
| GPT-3 (temp. 0,01) | 0,1047 % [0,0396 ; 0,1839] | 0,0140 % [0,0000 ; 0,0419] | 0,0000 | 0,0000 % |
| GPT-3 (temp. 1,0) | 0,1001 % [0,0116 ; 0,2281] | 0,1397 % [0,0000 ; 0,3259] | 0,0004 | 0,0000 % |
| **B-demo (baseline)** | 0,0768 % [0,0093 ; 0,1909] | 0,0931 % [0,0000 ; 0,2328] | 0,0004 | 0,0000 % |

Hasard = 1 / 2 148 = 0,0466 %. TPR @ 0,1 % de FPR = **0,0000 %** pour les quatre, sous
les deux attaques.

## Les trois enseignements, et mes écarts avec le relecteur

**1. L'attaquant fort ne sauve pas le point 2023.** 0,1373 → 0,2328 % (+69 % relatifs),
contre une baseline qui passe elle aussi de 0,0768 à 0,0931 % sous la même attaque. Le
jumeau reste au niveau de la baseline : ses IC [0,0466 ; 0,4655] et [0,0000 ; 0,2328] se
chevauchent largement. **Sur le fond, je confirme le relecteur.** Sur les chiffres, je
diverge :

| | relecteur | **moi** |
|---|---|---|
| top-1 naïf, temp. principale | 0,1490 % | **0,1373 %** |
| top-1 A-LLR, temp. principale | 0,1862 % | **0,2328 %** |
| top-1 A-LLR, B-demo | 0,0931 % | **0,0931 %** (identique) |
| TPR @ 1 % FPR, temp. principale | 0,0000 % | **0,0466 %** |

Ces écarts portent sur **1 à 5 personnes retrouvées sur 2 148**. 0,1373 % = 2,95
personnes, 0,2328 % = 5 personnes, 0,0466 % = **1 seule personne**. Le départage
aléatoire des ex æquo suffit à les produire : à 12 items, la classe d'ex æquo au rang 1
compte plusieurs candidats (défaut D9 de la relecture), et le tirage décide. Je ne les
corrige pas et je ne prétends pas trancher : **aucune de ces valeurs n'est identifiée par
les données**, et c'est cela le résultat.

**2. Dans la métrique de l'accroche, le bout gauche est nul ou quasi nul.** Je trouve
**0,0466 % de TPR à 1 % de FPR** pour le meilleur jumeau de 2023 — une personne —, là où
le relecteur trouve 0,0000 %. L'écart est d'une personne ; la conclusion est la même. La
trajectoire honnête dans une métrique unique est donc « ~0 % → 60,17 % », **plus forte**
que ce qu'écrit l'article.

**3. Mais cette métrique dégénère à 12 items, et je le confirme.** L'AUC en monde ouvert
vaut **0,0013** pour le meilleur jumeau (le relecteur annonce 0,001), et **0,0000** pour
le jumeau à température 0,01. Une AUC quasi nulle, pas 0,5 : les marges top1 − top2 sont
massivement ex æquo et la courbe ROC n'a pas de forme exploitable. **Le bout gauche
n'existe pas dans la métrique du bout droit.** Ce n'est pas un résultat faible, c'est la
raison pour laquelle on lit deux métriques différentes dans une seule phrase de
l'abstract, et il faut l'écrire ainsi plutôt que de changer de métrique en silence.

---

# Le contrôle d'interprétabilité, appliqué avant toute interprétation

Règle de décision inchangée (`c7_controle_interpretabilite`) : le candidat passe si la
borne basse de son IC 95 % est **strictement** supérieure à la borne haute de l'IC de la
baseline démographique **recalculée sur le même bassin et les mêmes items**. Test
conservateur, parce que le sinistre qu'il prévient est un faux positif.

## Sur T1 (Twin), à chaque k — fonction canonique du dépôt

`c7_controle_interpretabilite.controle_avant_interpretation` est appelée **telle
quelle**. Elle n'accepte aucune valeur de baseline en argument : elle la recalcule
elle-même sur les mêmes personnes et les mêmes items. k = 12 porte la conclusion « la
trajectoire survit au témoin » et l'étendue entre tirages d'items y couvre un facteur 9 :
le contrôle y est donc rejoué sur **5 tirages d'items indépendants**, pas un seul.

| k | tirage | top-1 candidat (`JSON Persona - GPT4.1`) | baseline recalculée sur les mêmes items | verdict |
|---|---|---|---|---|
| **12** | 0 | 2,4636 % [1,9242 ; 3,0248] | 0,8066 % [0,5029 ; 1,1419] | **PASSE** |
| **12** | 1 | 1,8610 % [1,3946 ; 2,3519] | 0,5369 % [0,2891 ; 0,8115] | **PASSE** |
| **12** | 2 | 0,3353 % [0,1506 ; 0,5564] | 0,1020 % [0,0219 ; 0,2332] | **ÉCHEC** |
| **12** | 3 | 1,1492 % [0,7847 ; 1,5185] | 0,2357 % [0,0948 ; 0,4082] | **PASSE** |
| **12** | 4 | 1,5792 % [1,1758 ; 2,0262] | 0,6948 % [0,4252 ; 1,0108] | **PASSE** |
| 20 | 0 | 2,9786 % [2,3615 ; 3,6129] | 0,5466 % [0,3037 ; 0,8285] | PASSE |
| 30 | 0 | 6,2123 % [5,2793 ; 7,2085] | 0,5005 % [0,2453 ; 0,7799] | PASSE |
| 40 | 0 | 7,7089 % [6,6569 ; 8,8146] | 0,8576 % [0,5101 ; 1,2391] | PASSE |
| 60 | 0 | 20,6827 % [19,0330 ; 22,3690] | 2,1526 % [1,5865 ; 2,7892] | PASSE |

**À k = 12 : 4 tirages d'items sur 5 passent.** Je rapporte l'échec plutôt que de
m'arrêter au premier tirage favorable. Le tirage 2 est un sous-ensemble d'items pauvre
(top-1 candidat 0,34 %, soit le bas de l'étendue 0,34 – 3,01 % mesurée plus haut) : le
candidat y bat pourtant sa baseline d'un facteur 3,3, mais les IC se chevauchent et le
test — délibérément conservateur — refuse de laisser interpréter. C'est le comportement
attendu, et c'est la raison d'être du test.

**Sur la courbe agrégée (30 tirages d'items), le contrôle passe nettement à k = 12** :
[1,1118 ; 1,3301] contre [0,2413 ; 0,3346], IC disjoints. Cette application-là de la
règle est la mienne, appliquée aux indicatrices moyennées de la courbe, et non un appel
de la fonction canonique — qui ne prend qu'un jeu d'items à la fois. Les deux lectures
concordent ; la seconde est la plus prudente et la plus informative.

## Sur T2 (Argyle), sous les deux attaques

`c7_argyle.controle_avant_interpretation` reprend la règle à l'identique pour un jeu qui
n'est pas Twin ; la variante A-LLR applique la même règle avec candidat **et** baseline
tous deux sous l'attaquant fort.

| jumeau Argyle | attaque | top-1 candidat | baseline B-demo, même bassin, même attaque | verdict |
|---|---|---|---|---|
| GPT-3 (temp. principale) | naïve | 0,1443 % [0,0512 ; 0,2677] | 0,1001 % [0,0163 ; 0,2258] | **ÉCHEC** |
| GPT-3 (temp. 0,01) | naïve | 0,1094 % [0,0372 ; 0,2048] | 0,1001 % [0,0163 ; 0,2258] | **ÉCHEC** |
| GPT-3 (temp. 1,0) | naïve | 0,0931 % [0,0163 ; 0,2165] | 0,1001 % [0,0163 ; 0,2258] | **ÉCHEC** (sous la baseline) |
| GPT-3 (temp. principale) | **A-LLR** | 0,2328 % [0,0466 ; 0,4655] | 0,0931 % [0,0000 ; 0,2328] | **ÉCHEC** |
| GPT-3 (temp. 0,01) | **A-LLR** | 0,0140 % [0,0000 ; 0,0419] | 0,0931 % [0,0000 ; 0,2328] | **ÉCHEC** (sous la baseline) |
| GPT-3 (temp. 1,0) | **A-LLR** | 0,1397 % [0,0000 ; 0,3259] | 0,0931 % [0,0000 ; 0,2328] | **ÉCHEC** |

Les top-1 de ce tableau diffèrent de quelques centièmes de point de ceux du tableau de
mesure (0,1443 contre 0,1373 % par exemple) : c'est la même grandeur, calculée par la
fonction de contrôle avec ses propres graines de départage. L'écart vaut **0,15
personne** sur 2 148 et n'a aucun contenu.

**Verdict : aucun jumeau Argyle ne passe le contrôle, ni sous l'attaque naïve, ni sous
l'attaquant fort.** C'est le résultat le plus important de T2 et il n'avait jamais été
mesuré : le contrôle d'interprétabilité, qui est une contribution du manuscrit, **résiste
à l'armement de l'attaquant**. On ne pouvait pas l'affirmer avant ce témoin.

**Lecture croisée, qui est la substance de la révision R1.** À **12 items**, sur le même
nombre d'items, sous la même attaque naïve :

- le jumeau **Twin 2025** passe le contrôle — sur la courbe agrégée à 30 tirages
  d'items, et sur 4 tirages d'items sur 5 pris isolément ;
- le jumeau **Argyle 2023** ne le passe **jamais** — ni sous l'attaque naïve, ni sous
  l'attaquant fort, sur aucun des trois jumeaux publiés.

C'est ce qui reste de la trajectoire une fois le nombre d'items neutralisé. Ce n'est pas
un facteur 150, c'est la différence entre « au-dessus de sa baseline de façon
démontrable » et « indiscernable de sa baseline ». **Elle est réelle, et elle est quinze
à dix-sept fois plus petite que la phrase qui la porte dans l'abstract.**

---

# Récapitulatif des écarts avec le relecteur, sans alignement

| grandeur | relecteur | moi | écart | mon hypothèse |
|---|---|---|---|---|
| T1 top-1 k = 12 | 1,323 % | 1,2193 % | −8 % rel. | 30 tirages d'items différents ; étendue entre tirages = facteur 9 |
| T1 top-1 k = 60 | 20,694 % | 20,7191 % | +0,1 % rel. | départage des ex æquo ; **raccordement validé** |
| T1 facteur 12 → 60 | 15,6 | **17,0** | +9 % | conséquence directe de la ligne 1 |
| T1 rapport à la baseline, k = 12 | 4,3 | 4,26 | négligeable | — |
| T2 top-1 naïf, temp. principale | 0,1490 % | 0,1373 % | −0,25 personne | départage des ex æquo |
| T2 top-1 A-LLR, temp. principale | 0,1862 % | 0,2328 % | +1 personne | départage + plis de l'estimation hors pli |
| T2 top-1 A-LLR, B-demo | 0,0931 % | 0,0931 % | nul | — |
| T2 TPR @ 1 % FPR, temp. principale | 0,0000 % | 0,0466 % | +1 personne | interpolation sur un axe FPR massivement ex æquo |
| T2 AUC ouvert | 0,001 | 0,0013 | négligeable | — |
| rapport à la baseline Argyle, 12 items | 1,5 | 1,79 | +0,3 | sa baseline vaut 0,0913 % (D1) **ou** 0,1024 % (D2) selon l'endroit de son rapport ; la mienne 0,0768 % ; 1 à 2 succès absolus |

**Aucun de ces écarts n'a été corrigé.** Aucun ne renverse un sens : le facteur items
reste supérieur à 15, aucun jumeau Argyle ne passe le contrôle, le point k = 60 se
raccorde. La règle d'arrêt du préenregistrement (§5) n'a jamais été déclenchée.

**Ce que ces écarts enseignent, et qui vaut plus que les écarts eux-mêmes :** tout ce qui
se mesure à 12 items, des deux côtés, repose sur une poignée de personnes et sur une
convention de départage. Deux dérivations indépendantes, avec des graines différentes,
donnent des taux qui bougent d'une personne à l'autre. **Les chiffres du bout gauche de
la trajectoire ne doivent jamais être publiés sans leur nombre de succès absolus.**

---

# Ce que ce fichier ne contient pas

Les cinq autres mesures de la tâche T1a du plan de révision ne sont **pas** faites ici et
ne sont pas approchées : §1c (classes d'ex æquo, Clopper-Pearson, différence appariée,
top-1 de B-oracle), §1d (FPR = 0,1 % en escalier sur Park et Twin), §1e (Spearman
bootstrap sur les paires), §1f (bootstrap en grappes du 36,4 %), §1g (baseline
démographique en monde ouvert sous A-LLR). Elles sortent du périmètre confié.

Le plan de révision nomme le livrable `resultats/c7-temoins-relecture.md` ; le mandat
d'écriture de cet agent le scinde en
`c7-temoins-relecture-preenregistrement.md` + `c7-temoins-relecture-resultats.md`. Les
renvois du plan pointent donc vers ces deux fichiers et vers le CSV.
