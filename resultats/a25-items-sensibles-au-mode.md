# a25. Ce que la simulation efface, premier test sur les items sensibles au mode

## Errata du 9 septembre 2026

Correction apportee a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md` section 12.1, contradiction D8, signalee par
`resultats/a47-errata-2.md` section 4. **Le corps du rapport n'est pas reecrit** ; l'errata
cite la phrase d'origine, donne la correction et donne la preuve. Aucun recalcul, aucun
appel de modele de langage : les chiffres cites sont ceux de `a38` et de `a28` tels que
publies.

### E1. Reponse en une ligne : la these « la simulation devie la ou les humains se surveillent » est tombee, et le seul effet distinguable etait une condition sur treize dans une famille non corrigee. Objection a45 numero 12.1, contradiction D8.

**Phrase d'origine.** « **La moitie de la prediction tient et l'autre tombe : les huit
conditions d'agents testees, les six de Stanford et nos deux, s'ecartent plus de la
distribution humaine sur les 12 items que NORC classe sensibles au mode que sur ses 65
temoins negatifs [...] et il n'est distinguable de zero que pour une seule condition, C2,
ou il vaut moins 0,207 [moins 0,331 ; moins 0,092] point de score de desirabilite.** »

**Correction, trois lignes.**

1. **La these est tombee.** `resultats/a38-mode-continu-et-camp.md` section 2 remplace le
   decoupage binaire de NORC par l'ampleur mesuree item par item sur six sources : **aucun
   `p` brut ne descend sous 0,18**, les intervalles bootstrap contiennent tous zero, et sur
   la dispersion le meilleur `p` vaut 0,119 pour `agents entretien (v3)`, **de signe oppose
   a la prediction** [MESURE, `a38-continu.csv`].
2. **Ce qui reste du contraste est un phenomene d'attitudes, pas de surveillance.** a38
   section 3.2 le localise : plus 0,062 a plus 0,093 sur les items d'attitude contre moins
   0,031 a plus 0,045 sur les comportements verifiables, c'est a dire exactement la ou la
   litterature sur la desirabilite sociale n'attend pas l'effet
   [MESURE, `a38-comportement.csv`].
3. **Le moins 0,207 de C2 est une condition sur treize dans une famille de 52 tests non
   corrigee**, ce qui est ce qu'on attend d'une famille de treize tests bruts ; `a28`
   section 0.1 fixe cette famille et `a28-t1-corrections.csv` etablit qu'aucune condition
   prise individuellement ne passe, meilleur `p` ajuste par Holm **0,144**.

**Ce que le rapport garde.** Le croisement avec la note de mode de NORC, le depouillement
des 163 variables, la liste des 119 temoins negatifs et les tableaux par item restent
valides et reutilisables. C'est leur lecture en reponse d'une ligne qui est retiree : aucune
synthese ne doit plus ecrire « le motif tient » a partir de ce rapport.

---

Rapport du 8 septembre 2026. Premier test de la these de `corpus/04`, section "Ce que
personne n'a fait", point 4 : si une population simulee est "presentable", alors l'ecart
entre agents et humains doit etre plus grand sur les items du GSS ou les humains eux memes
repondent differemment selon qu'ils sont observes ou non, et le sens de l'ecart doit aller
vers la reponse socialement desirable.

Zero appel de modele de langage. Lecture seule sur `data/`. Trois scripts nouveaux,
`analyses/a25_commun.py`, `a25_mesures.py`, `a25_contrastes.py`, `a25_figure.py`. Aucun
script existant n'a ete modifie ; `a2_commun`, `a2_baselines_gss`, `a5_evaluer` et
`a5_agents_locaux_gss` sont importes tels quels, memes graines, memes plis, memes 149
items que a2 et a23.

Sorties : `resultats/a25-croisement.csv`, `a25-par-item-condition.csv`,
`a25-bootstrap-personnes.csv`, `a25-contrastes.csv`, `a25-contrastes-controles.csv`,
`a25-figure-mode.png` et `.svg`.

---

## Reponse en une ligne

**La moitie de la prediction tient et l'autre tombe : les huit conditions d'agents testees,
les six de Stanford et nos deux, s'ecartent plus de la distribution humaine sur les 12
items que NORC classe sensibles au mode que sur ses 65 temoins negatifs, alors que les
quatre baselines statistiques et les memes humains reinterroges ne montrent aucun ecart de
ce type ; mais le sens de l'ecart ne va pas vers la reponse socialement desirable, il va
contre elle, et il n'est distinguable de zero que pour une seule condition, C2, ou il vaut
moins 0,207 [moins 0,331 ; moins 0,092] point de score de desirabilite** [MESURE,
`a25-contrastes.csv`, perimetre 150].

---

## 1. Le croisement

### 1.1 La source

NORC (2023), *2022 GSS Cross-section, Mode Sensitivity in the 2022 GSS, Release 1*, PDF
officiel telecharge le 8 septembre 2026 sur `gss.norc.org`, chemin
`/content/dam/gss/get-documentation/pdf/other/2022 GSS Mode Sensitivity Note v1.pdf`. La
note examine 163 variables du GSS 2022 par regression logistique multivariee sur les
variables de ponderation plus la condition experimentale et le mode, ponderee `WTSSNR`,
avec correction de Bonferroni. Elle produit trois classes : **23** variables "Likely mode
sensitive", **21** "Requires further investigation", **119** entrees "Less likely to be
mode sensitive" [CONFIRME, lu dans le texte du PDF].

Trois precisions que la fiche `corpus/04-18` ne portait pas et que la lecture du PDF
etablit :

- la liste complete des temoins negatifs existe et elle est longue. `corpus/04` n'en citait
  que la partie deduite ; les 119 entrees sont recopiees dans `analyses/a25_commun.py`
  [CONFIRME].
- `RELPERSN` figure **deux fois**, en "Requires further investigation" et en "Less likely".
  C'est une incoherence de la source. L'item est de toute facon exclu par la liste
  d'exclusion de Stanford [CONFIRME].
- NORC ecrit lui meme que ce ne sont pas de vrais effets de mode, le mode de completion
  etant endogene, et que les poids ne soutiennent pas l'analyse par mode [CONFIRME].

### 1.2 Le croisement avec nos 149 items

[MESURE, `a25-croisement.csv`]

| classe NORC | items de nos 149 | dont pole de desirabilite defini |
|---|---|---|
| sensible ("likely mode sensitive") | **12** | 10 |
| a investiguer ("requires further investigation") | **13** | 7 |
| temoin negatif ("less likely to be mode sensitive") | **65** | 46 |
| mixte, les deux formes de la question ne sont pas dans la meme classe | 4 | 4 |
| non teste par NORC | 55 | 9 |

**Les 12 items sensibles** : `attend`, `coneduc`, `conlegis`, `conmedic`, `natchld`,
`natrace/y`, `natroad`, `polabuse/y`, `polattak/y`, `spkrac/y`, `vote16`, `xmarsex`.

**Les 13 items a investiguer** : `abany`, `abpoor`, `abrape`, `conarmy`, `fefam`,
`fepresch`, `if16who`, `news`, `pillok`, `pray`, `reborn`, `savesoul`, `suicide1`.

**Les 4 items mixtes**, ecartes des deux bras : `natspac/y`, `natheal/y`, `natcity/y`,
`natfare/y`. Stanford fusionne sous un seul nom de colonne la forme historique et la forme
reformulee 2021 d'une meme question, et NORC classe les deux formes differemment. Exemple :
`NATFARE` est temoin, `NATFAREY` est sensible. Les garder aurait fait entrer un item
ambigu dans un bras ou dans l'autre.

**Ce qui manque.** Neuf des 23 variables sensibles de NORC ne sont pas dans nos 149 :
`CHLDIDEL`, `IF20WHO`, `MARBLK`, `MEOVRWRK`, `PARTYID`, `POLMURDR`, `SOCBAR`, `VOTE20`,
`WORDSUM`. Une seule de ces absences vient de nous, `PARTYID`, retire par la liste
d'exclusion de Stanford parce que l'information est deja dans la persona ; les huit autres
ne sont pas dans les 177 items de l'archive [MESURE]. Cinq des 21 variables a investiguer
manquent de la meme facon : `ADULTS`, `FAMDIF16`, `FEJOBAFF`, `NATCRIMY`, `RELPERSN`.

**Le croisement n'est pas trop pauvre** : 12 items sensibles contre 65 temoins suffisent a
un test de permutation. Un second decoupage, celui des domaines sensibles de Tourangeau et
Yan 2007 repris dans la synthese de `corpus/04` (religion, sexualite, drogues, revenu,
vote, race), a quand meme ete construit comme controle de robustesse, 39 items contre 110.
Son resultat figure en section 5.

---

## 2. Le protocole

### 2.1 Les conditions comparees

Onze methodes non humaines plus un plancher humain, sur les memes 149 items et la meme
verite terrain que a2 et a23.

- **Six conditions d'agents de Stanford**, 1 052 personnes : agents composite, agents
  entretien (v3), agents enquete, agents demographiques (v6), agents v7, agents v8.
- **Nos deux conditions locales**, 150 personnes : C2 (persona demographique, 11 attributs)
  et C3 (119 reponses d'enquete, aucune demographie), Qwen3-4B a temperature 0, traces
  completes du run du 8 septembre.
- **Quatre baselines sans modele de langage**, 1 052 personnes : `B0 mode`, `B0 tirage`,
  `B1 argmax` (regression logistique multinomiale sur les seules demographies),
  `B2 argmax` (30 plus proches voisins sur les items de contexte). Elles sont le controle
  decisif : ce sont des predicteurs sans langage, sans presentation de soi et sans notion
  de ce qui est dicible.
- **Humains vague 2**, les memes personnes reinterrogees a deux semaines. C'est le plancher
  de bruit humain.

Deux perimetres. Le perimetre **1 052** porte les conditions de Stanford et les baselines.
Le perimetre **150** restreint tout le monde aux personnes de notre run et ajoute C2 et C3.
**Toute comparaison impliquant C2 ou C3 se lit sur le perimetre 150 et sur lui seul.**

### 2.2 Les trois mesures, par couple condition et item

1. **Exactitude** au niveau de la cellule, egalite exacte de chaine apres normalisation de
   casse, meme definition que `a2_commun.exactitude_par_personne`.
2. **Ecart de distribution** entre la population simulee et la population humaine de la
   vague 1 sur les memes personnes : distance de Wasserstein d'ordre 1 sur les rangs
   ramenes a [0, 1] pour les items ordinaux, distance de variation totale pour les items
   nominaux. Les deux sont dans [0, 1] et coincident quand l'item est binaire. Un item
   portant une modalite "Inapplicable" n'est jamais traite comme ordinal.
3. **Sens de l'ecart** : score moyen de desirabilite de la population simulee moins celui
   de la population humaine. Positif veut dire que la masse simulee s'est deplacee vers le
   pole socialement desirable. Le score est renormalise sur les seules modalites qui en
   portent un, de sorte qu'une condition qui repond souvent "Inapplicable" ne soit pas
   penalisee pour cette seule raison.

Une cellule dont la prediction est vide est exclue des trois mesures des deux cotes. Cela
ne concerne que quatre conditions de Stanford et au plus six cellules sur 150 pour un item,
`agents demographiques (v6)` etant la plus touchee avec 149,72 cellules par item en moyenne
[MESURE, `a25-par-item-condition.csv`]. C2, C3, les baselines et les humains couvrent les
150 cellules de chaque item.

### 2.3 La definition du pole desirable, item par item

C'est la partie contestable du protocole. Elle est ecrite en clair dans
`analyses/a25_commun.py`, table `DESIRABILITE`, et exportee item par item dans
`a25-croisement.csv` avec sa source et son niveau de confiance. Trois niveaux :

- **[CONFIRME]**, la direction est donnee explicitement par NORC dans la note de mode ;
- **[PROBABLE]**, la direction est etablie par une mesure publiee sur le meme item ou le
  meme domaine ;
- **[HYPOTHESE]**, la direction est deduite d'une norme sociale sans mesure directe.

Les decisions qui portent le resultat :

| item ou famille | pole desirable retenu | niveau | source |
|---|---|---|---|
| `attend` | pratique religieuse plus forte | [CONFIRME] | NORC : ATTEND chute nettement sur le web ; Presser et Stinson 1998, `corpus 04-13` |
| `pray`, `reborn`, `savesoul` | pratique et croyance plus fortes | [CONFIRME] | NORC, meme phrase |
| `coneduc`, `conlegis`, `conmedic` | "a great deal" | [CONFIRME] | NORC : la confiance passe de "a great deal" en face a face a "only some" sur le web |
| les 13 autres `con*` | "a great deal" | [HYPOTHESE] | meme echelle, meme pole, appliquee uniformement aux temoins |
| les 17 items `nat*` | "too little" | [HYPOTHESE] | regle uniforme, le pole genereux ; NORC ne donne pas la direction item par item |
| `vote16` | "voted" | [PROBABLE] | Ansolabehere et Hersh 2012, `corpus 04-20` : 15,8 points d'ecart au registre |
| `xmarsex` | "always wrong" | [PROBABLE] | Tourangeau et Yan 2007, `corpus 04-03` |
| `homosex`, `marhomo`, items de tolerance | pole tolerant | [PROBABLE] | Coffman, Coffman et Ericson 2017, `corpus 04-21` |
| `racdif1` a `racdif4` | pole racialement liberal | [PROBABLE] et [HYPOTHESE] | Berinsky 1999, `corpus 04-19` |
| `letin1a` | pole pro immigration | [PROBABLE] | Bursztyn, Egorov et Fiorin 2020, `corpus 04-27` |
| `happy`, `satfin`, `satjob`, `health`, `life` | pole positif | [PROBABLE] | Pew 2015, `corpus 04-15` : 14 a 18 points d'ecart de mode sur les items de satisfaction |
| `polabuse/y`, `polhitok/y` | "no" | [HYPOTHESE] | approuver un coup porte a un citoyen est le pole stigmatise |

**Cinq items sensibles ou aucun pole n'est retenu, et c'est assume.** `spkrac/y`, `colrac`
et `librac/y` opposent deux normes, la liberte d'expression et l'antiracisme, et rien dans
la litterature ne tranche laquelle domine en presence d'un enqueteur. `polattak/y` decrit
un citoyen qui attaque le policier, ou approuver est une reponse socialement acceptable.
`pres16` et `if16who` sont des choix de candidat, et deux enquetes post electorales,
`corpus 04-30` et `04-31`, ecartent l'electeur qui se cache. Tous les items d'avortement
sont egalement laisses sans pole. Ces items entrent dans les mesures d'exactitude et
d'ecart de distribution, jamais dans la mesure de sens.

**Une contradiction a signaler et non a masquer.** Pour `vote16` le pole desirable retenu
est "voted", d'apres la validation par registre. Or NORC mesure sur le GSS 2022 un vote
declare **plus eleve sur le web**, donc en l'absence d'enqueteur, ce qui est l'inverse du
sens attendu. Le pole retenu suit la litterature de validation externe et non la direction
de mode de NORC. Ce choix est defavorable a notre these, puisqu'il rend les agents
"non presentables" sur cet item.

### 2.4 Les tests

- **Bootstrap sur les items**, 10 000 tirages, reechantillonnage separe dans chaque groupe.
  Il repond a : verrait on le meme contraste avec d'autres items ?
- **Bootstrap sur les personnes**, 1 000 tirages, memes personnes tirees des deux cotes de
  facon appariee. Il repond a : verrait on le meme contraste avec d'autres gens ?
- **Test de permutation** des etiquettes sensible et temoin, 10 000 tirages, p bilateral.
  C'est le test decisif, il ne suppose rien sur la forme de la distribution.
- **Quatre controles** : items ordinaux seulement ; stratification par le couple type et
  nombre de modalites ; residualisation par le bruit humain test retest item par item ;
  decoupage alternatif de la litterature.

---

## 3. Resultat 1, l'ecart de distribution : la prediction tient

Perimetre 150, les 12 items sensibles contre les 65 temoins [MESURE, `a25-contrastes.csv`
et `a25-bootstrap-personnes.csv`]. Figure : `a25-figure-mode.png`.

| condition | sensibles | temoins | difference | IC 95 % items | IC 95 % personnes | p permutation |
|---|---|---|---|---|---|---|
| agents entretien (v3) | 0,1653 | 0,0911 | **+0,0743** | [+0,011 ; +0,148] | [+0,055 ; +0,088] | **0,004** |
| agents v8 | 0,1764 | 0,1175 | **+0,0589** | [-0,009 ; +0,136] | [+0,039 ; +0,071] | 0,051 |
| agents composite | 0,1299 | 0,0746 | **+0,0553** | [+0,003 ; +0,121] | [+0,037 ; +0,073] | **0,013** |
| agents enquete | 0,1448 | 0,0948 | **+0,0500** | [+0,001 ; +0,110] | [+0,033 ; +0,065] | **0,018** |
| agents demographiques (v6) | 0,1963 | 0,1513 | +0,0450 | [-0,023 ; +0,119] | [+0,026 ; +0,064] | 0,176 |
| **C3** | 0,2548 | 0,2103 | +0,0445 | [-0,049 ; +0,151] | [+0,026 ; +0,064] | 0,403 |
| agents v7 | 0,2037 | 0,1653 | +0,0384 | [-0,027 ; +0,110] | [+0,015 ; +0,057] | 0,194 |
| **C2** | 0,2462 | 0,2101 | +0,0361 | [-0,052 ; +0,133] | [+0,018 ; +0,056] | 0,457 |
| B2 argmax | 0,1494 | 0,1357 | +0,0137 | [-0,037 ; +0,073] | [-0,007 ; +0,032] | 0,593 |
| B1 argmax | 0,1147 | 0,1043 | +0,0104 | [-0,029 ; +0,058] | [-0,010 ; +0,030] | 0,530 |
| **humains vague 2** | 0,0221 | 0,0267 | **-0,0046** | [-0,014 ; +0,006] | [-0,015 ; +0,008] | 0,414 |
| B0 tirage | 0,0384 | 0,0455 | -0,0071 | [-0,022 ; +0,010] | [-0,025 ; +0,011] | 0,484 |
| B0 mode | 0,2641 | 0,2840 | -0,0200 | [-0,087 ; +0,045] | [-0,040 ; -0,001] | 0,637 |

**Le motif est net et il va dans le sens de la these.** Les huit conditions qui emploient un
modele de langage ont toutes une difference positive, de +0,036 a +0,074, et leur intervalle
sur les personnes exclut zero dans les huit cas. Les quatre baselines statistiques ont une
difference comprise entre -0,020 et +0,014, et leur intervalle sur les personnes contient
zero dans trois cas sur quatre ; le quatrieme, `B0 mode`, est **negatif**. Les memes humains
reinterrogees ont une difference de -0,005.

**Le point decisif demande par le cahier des charges a donc une reponse.** La presentabilite
mesuree ici **n'est pas un effet de predicteur**. `B1` et `B2` ne montrent pas le meme
contraste. `B2 argmax` est pourtant la methode la plus exacte du tableau et `B0 mode` la
plus concentree : ni l'exactitude ni la concentration ne produisent ce motif. Cela distingue
notre resultat de Ku et al. (`corpus/01`), dont la conclusion est qu'une part des effets
attribues aux modeles de langage se retrouve chez un predicteur statistique.

**Sur le perimetre 1 052**, plus puissant pour les conditions de Stanford [MESURE] : agents
entretien (v3) +0,0695 [+0,009 ; +0,140], p = 0,004 ; agents composite +0,0588
[-0,001 ; +0,142], p = 0,011 ; agents enquete +0,0392 [-0,005 ; +0,092], p = 0,041 ;
`B1 argmax` -0,0007, p = 0,963 ; `B2 argmax` +0,0034, p = 0,869 ; humains vague 2 +0,0004,
p = 0,919.

### 3.1 Ce qui pourrait le detruire, et qui ne le detruit pas

**Un item unique.** En retirant tour a tour chacun des 12 items sensibles, la difference
reste positive pour les huit conditions a modele de langage : le minimum sur les 12 retraits
vaut +0,030 pour les agents composite (sans `polattak/y`), +0,052 pour les agents entretien,
+0,027 pour les agents enquete, +0,005 pour C2 et +0,008 pour C3 (sans `vote16` dans les
deux cas). Pour `B1` et `B2`, le meme exercice fait **changer de signe** la difference,
-0,007 et -0,004 [MESURE, calcul sur `a25-par-item-condition.csv`].

**La composition des groupes.** Les deux groupes n'ont ni le meme nombre de modalites ni la
meme proportion d'items ordinaux. Deux corrections [MESURE,
`a25-contrastes-controles.csv`, perimetre 150] :

| condition | brut | items ordinaux seulement (8 items) | stratifie par type et nombre de modalites (10 items) |
|---|---|---|---|
| agents entretien (v3) | +0,074 | +0,034 (p = 0,113) | **+0,089** |
| agents v8 | +0,059 | +0,006 (p = 0,831) | **+0,080** |
| agents composite | +0,055 | +0,037 (p = 0,035) | **+0,068** |
| agents enquete | +0,050 | +0,017 (p = 0,393) | **+0,058** |
| C3 | +0,045 | +0,022 (p = 0,673) | +0,027 |
| C2 | +0,036 | -0,003 (p = 0,929) | +0,042 |
| B1 argmax | +0,010 | +0,020 (p = 0,189) | +0,011 |
| B2 argmax | +0,014 | +0,007 (p = 0,679) | +0,007 |
| humains vague 2 | -0,005 | -0,002 (p = 0,624) | -0,003 |

La stratification conserve l'effet, et meme l'amplifie pour les conditions riches. La
restriction aux seuls items ordinaux le divise par deux et ne laisse qu'un p sous 0,05, pour
les agents composite. **La partie du contraste portee par les items nominaux, c'est a dire
`spkrac/y`, `polabuse/y`, `polattak/y` et `vote16`, est donc essentielle.** Ce n'est pas
disqualifiant, ce sont quatre des items les plus charges du GSS, mais il faut l'ecrire : sur
les seuls items ordinaux et avec 8 items, le test n'a pas la puissance de conclure.

**Le bruit humain.** Residualisation item par item par l'ecart des memes humains reinterroges
[MESURE] : agents entretien +0,079 [+0,018 ; +0,148], p = 0,002 ; agents composite +0,060
[+0,012 ; +0,116], p = 0,003 ; agents enquete +0,055 [+0,009 ; +0,109], p = 0,009 ;
`B1 argmax` +0,015, p = 0,352 ; `B2 argmax` +0,018, p = 0,461. La correction ne change rien,
ce qui etait attendu puisque le contraste chez les humains vague 2 est deja nul.

---

## 4. Resultat 2, le sens de l'ecart : la prediction tombe

Perimetre 150, meme decoupage, metrique du deplacement vers le pole desirable [MESURE,
`a25-contrastes.csv`]. Positif veut dire "plus presentable que les humains".

| condition | sensibles | temoins | difference | IC 95 % items | p permutation |
|---|---|---|---|---|---|
| B2 argmax | +0,063 | +0,033 | +0,030 | [-0,057 ; +0,120] | 0,496 |
| humains vague 2 | +0,000 | -0,005 | +0,005 | [-0,008 ; +0,018] | 0,580 |
| agents entretien (v3) | -0,038 | -0,040 | +0,002 | [-0,071 ; +0,075] | 0,948 |
| B1 argmax | +0,020 | +0,028 | -0,007 | [-0,077 ; +0,054] | 0,826 |
| agents enquete | -0,003 | +0,008 | -0,012 | [-0,068 ; +0,044] | 0,730 |
| B0 mode | +0,047 | +0,068 | -0,021 | [-0,169 ; +0,123] | 0,783 |
| agents composite | -0,044 | -0,023 | -0,022 | [-0,079 ; +0,044] | 0,433 |
| agents demographiques (v6) | +0,010 | +0,033 | -0,022 | [-0,116 ; +0,073] | 0,661 |
| agents v8 | -0,032 | +0,023 | -0,054 | [-0,129 ; +0,028] | 0,158 |
| agents v7 | +0,028 | +0,100 | -0,072 | [-0,171 ; +0,034] | 0,126 |
| **C3** | -0,088 | +0,043 | **-0,131** | [-0,304 ; +0,037] | 0,134 |
| **C2** | -0,155 | +0,052 | **-0,207** | [-0,331 ; -0,092] | **0,004** |

**La prediction dirigee echoue, et il faut le dire sans adoucir.** Aucune condition ne
deplace la masse vers le pole desirable plus sur les items sensibles que sur les temoins.
Onze differences sur douze sont negatives ou nulles. La seule qui se distingue de zero, C2,
est **negative** : nos agents locaux sont, sur les items sensibles, **moins presentables**
que les humains qu'ils simulent, de 0,207 point de score de desirabilite.

Le detail par item explique d'ou vient le signe [MESURE, comptages directs sur les traces et
sur l'archive, 150 personnes] :

| item | humains vague 1 | C2 | C3 | agents composite |
|---|---|---|---|---|
| `vote16`, "voted" | 95 sur 150 | **25** | **14** | 94 |
| `polabuse/y`, "yes" (approuve le coup) | 9 sur 150 | **71** | **50** | 30 |
| `conmedic`, "a great deal" | 72 sur 150 | 27 | 18 | 37 |
| `xmarsex`, "always wrong" | 80 sur 150 | 43 | 54 | **129** |
| `attend`, "never" | 67 sur 150 | 31 | 89 | 77 |

Deux enseignements distincts.

**Nos agents locaux vont contre la norme, pas avec elle.** Ils declarent que 90 pour cent des
personnes n'ont pas vote quand 63 pour cent des humains declarent avoir vote, et ils font
approuver la violence policiere a un tiers puis a une moitie des personnes quand 6 pour cent
des humains l'approuvent. Ce n'est pas une simulation qui rend le monde presentable, c'est une simulation
qui produit une population plus dure et plus abstentionniste que la population reelle.

**Les agents riches de Stanford, eux, sont plus presentables sur l'item de moeurs et pas
ailleurs.** Sur `xmarsex`, la condition composite met 129 personnes sur 150 dans "always
wrong" contre 80 chez les humains, ce qui est exactement la presentabilite attendue. Sur
`conmedic` et `attend` elle va dans l'autre sens. La direction n'est donc pas une propriete
de la condition, elle depend de l'item, et la moyenne sur 10 items ne la voit pas.

**Interpretation la plus economique** [HYPOTHESE] : sur les items ou l'humain se surveille,
le modele ne reproduit pas la surveillance, il produit sa propre reponse. Cette reponse est
parfois plus normative que celle des humains, `xmarsex` chez les agents composite, parfois
beaucoup moins, `vote16` et `polabuse/y` chez nos agents locaux. Ce qui est commun aux huit
conditions n'est pas la direction, c'est **l'amplitude** de l'ecart. C'est la formulation de
`corpus/04` sur le regime de reponse substitue, et elle survit au test ; la formulation
"la simulation efface ce que les gens cachent" n'y survit pas.

---

## 5. Les trois controles qui limitent la portee

### 5.1 La classe "a investiguer" ne montre rien

Le meme test sur les 13 items que NORC classe "requires further investigation" contre les
memes 65 temoins [MESURE, `a25-contrastes.csv`, perimetre 150] : agents v7 +0,034
(p = 0,196), agents enquete +0,014 (p = 0,436), C3 +0,012 (p = 0,813), agents composite
-0,007 (p = 0,668), C2 -0,061 (p = 0,178). **Aucune condition ne se distingue.** Le groupe
reuni sensible plus a investiguer, 25 items, ne donne qu'un seul p sous 0,05, agents enquete
+0,031 (p = 0,047).

C'est le resultat le plus genant du rapport. Si l'effet etait un effet de "sensibilite au
mode" au sens large, on l'attendrait attenue mais present dans la classe adjacente. Il est
absent. Deux lectures possibles, non departageables ici : soit NORC a bien separe, et la
classe 1 est reellement differente de la classe 2 ; soit l'effet mesure sur 12 items tient a
la composition particuliere de ces 12 items et non a leur sensibilite au mode [HYPOTHESE].

### 5.2 Le decoupage de la litterature ne donne rien du tout

Avec les domaines de Tourangeau et Yan a la place de la liste NORC, 39 items sensibles contre
110 temoins, **aucune condition ne montre de contraste** : agents composite -0,004
(p = 0,770), agents entretien -0,004 (p = 0,804), C2 -0,022 (p = 0,473), C3 -0,001
(p = 0,974), `B1` -0,012, `B2` -0,005 [MESURE, `a25-contrastes-controles.csv`].

Enseignement direct pour la redaction : **l'effet n'est pas un effet de "sujet sensible"**.
Les items dont la litterature dit qu'ils portent de la desirabilite sociale, religion,
sexualite, race, revenu, ne produisent aucun ecart particulier. Seule la liste construite par
mesure de mode sur le GSS 2022 en produit un. C'est un argument pour le protocole, et c'est
aussi un avertissement : un relecteur pourra dire que 12 items choisis par un tiers ont
produit un resultat que 39 items choisis par la theorie ne produisent pas.

### 5.3 L'exactitude ne separe rien

Sur la metrique d'exactitude, **toutes** les methodes sont moins bonnes sur les items
sensibles que sur les temoins, y compris les baselines et y compris les humains vague 2
[MESURE, perimetre 150] : humains vague 2 -0,018, `B1 argmax` -0,047, `B2 argmax` -0,050,
agents composite -0,083, C2 -0,091. Le contraste sur l'exactitude est donc une propriete des
items, pas des methodes, et il ne teste rien. C'est ce qui justifie d'avoir construit le test
sur l'ecart de distribution et non sur l'exactitude.

---

## 6. Le controle demande sur les humains vague 2

L'instabilite test retest **n'est pas plus grande sur les items sensibles**. Sur les 1 052
personnes, l'ecart de distribution entre vague 2 et vague 1 vaut 0,0139 sur les items
sensibles et 0,0136 sur les temoins, difference +0,0004 [-0,005 ; +0,006], p = 0,919
[MESURE]. Sur les 150 personnes, -0,0046, p = 0,414. Aucune normalisation n'est donc
necessaire, et la residualisation par ce plancher ne change aucune conclusion, section 3.1.

Une exception a signaler : sur les 13 items de la classe "a investiguer", les humains sont
**plus stables** que sur les temoins, -0,0103 [-0,017 ; -0,004], p = 0,048 [MESURE]. Le fait
est note, il n'est pas explique.

---

## 7. La figure

`resultats/a25-figure-mode.png` et `.svg`, perimetre 150. Panneau de gauche : pour chaque
methode, l'ecart moyen de distribution aux humains sur les 12 items sensibles et sur les 65
temoins, avec intervalle bootstrap sur les personnes. Panneau de droite : la difference des
deux, avec l'intervalle sur les personnes en trait epais, l'intervalle sur les items en trait
fin, et le p du test de permutation.

La lecture voulue est celle du panneau de droite : les huit lignes de modeles de langage sont
a droite du zero, les quatre baselines statistiques et la ligne humaine sont dessus.

**Avertissement de lecture sur les intervalles.** L'intervalle sur les personnes est etroit
parce qu'il conditionne sur le jeu d'items ; l'intervalle sur les items est large parce qu'il
n'a que 12 items d'un cote. Les deux repondent a deux questions differentes et il ne faut pas
lire le premier comme une confirmation du second. Le p de permutation, qui reechantillonne
les etiquettes d'items, est la statistique conservatrice du rapport.

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. Que le croisement entre la liste NORC des items sensibles au mode et une mesure d'ecart
   agent contre humain **est fait**, sur 12 items sensibles, 13 en zone grise et 65 temoins
   negatifs, et qu'il n'existait pas au 8 septembre 2026 selon la verification de
   `corpus/04` [MESURE et CONFIRME].
2. Que les huit conditions d'agents testees s'ecartent plus de la distribution humaine sur
   les items sensibles que sur les temoins, +0,036 a +0,074 de distance, intervalle sur les
   personnes excluant zero dans les huit cas, p de permutation sous 0,05 pour trois des six
   conditions de Stanford sur le perimetre 150 [MESURE].
3. Que **ce n'est pas un effet de predicteur** : une regression logistique sur les
   demographies et 30 plus proches voisins ne montrent pas ce contraste, et le retrait d'un
   seul item leur fait changer de signe [MESURE]. C'est le point qui distingue ce resultat
   de Ku et al.
4. Que ce n'est pas du bruit humain : les memes personnes reinterrogees a deux semaines ne
   sont pas plus instables sur les items sensibles [MESURE].
5. Que la prediction dirigee de `corpus/04`, point 4, **echoue sur nos donnees** : le sens de
   l'ecart ne va pas vers la reponse socialement desirable, et la seule condition ou il se
   distingue de zero va contre [MESURE].
6. Que, sur `vote16`, nos agents locaux predisent 25 et 14 votants sur 150 la ou les humains
   en declarent 95, et que sur `polabuse/y` ils font approuver la violence policiere par 71
   et 50 personnes sur 150 la ou 9 humains l'approuvent [MESURE].

### Interdit

1. Ecrire "la simulation efface ce que les gens cachent". La direction mesuree ne le soutient
   pas. La formulation qui survit est : **la simulation s'ecarte davantage des humains la ou
   les humains se surveillent, et elle ne s'en ecarte pas dans la direction de la
   surveillance.**
2. Ecrire que l'effet vaut pour "les sujets sensibles". Le decoupage de la litterature ne
   donne rien, section 5.2. L'effet est attache a la liste NORC et a elle seule.
3. Ecrire que l'effet est etabli hors des items nominaux. Sur les 8 items ordinaux, un seul p
   passe sous 0,05, section 3.1.
4. Presenter le p de permutation comme corrige. `a25-contrastes.csv` porte 216 lignes de contraste, dont 117 sur le
   perimetre 150 ; aucune correction pour tests multiples n'est appliquee,
   comme partout ailleurs dans le projet. A 5 pour cent nominal, sur les 39 tests du seul
   bloc "distance, perimetre 150", on attend deux p sous 0,05 par hasard et il y en a trois.
   **Le resultat de la section 3 est a la limite de ce que la correction laisserait passer.**
5. Citer les chiffres de C2 et C3 comme "nos agents" sans nommer le modele. Qwen3-4B a
   temperature 0, et la question ouverte de a23 sur la capacite du modele reste ouverte ici :
   rien ne dit que le contraste mesure sur C2 et C3 tiendrait sur un modele plus gros.
6. Dire que les agents de Stanford sont "presentables". Sur `xmarsex` oui, sur `conmedic` et
   `attend` non, et la moyenne est nulle.

---

## Ce que je n'ai pas pu verifier

1. **NORC ne publie pas d'ampleur par item.** La note donne trois classes et des directions
   qualitatives par famille, jamais un ecart chiffre variable par variable. Le point 4 de
   `corpus/04`, "l'ecart agent contre humain doit etre correle a l'ecart de mode humain,
   item par item", **n'est donc pas testable en l'etat** : il n'y a pas de variable continue
   a correler. Ce rapport teste la version categorielle de la prediction, sensible contre
   temoin, qui est plus faible. Obtenir la version continue demande de recalculer les ecarts
   de mode sur les microdonnees du GSS 2022, ce qui est faisable et n'a pas ete fait ici.
2. **Le mode de collecte de la verite terrain de Stanford n'est pas documente dans
   l'archive.** Ni `FIGURE2_PIPELINE.md` ni `PROVENANCE.md` ne disent si les vagues 1 et 2
   ont ete administrees en ligne sans enqueteur. Si elles l'ont ete, et c'est le plus
   probable, alors la population de reference est deja du cote "non observe", ce qui change
   l'interpretation du signe : un agent moins presentable que ces humains est encore plus
   loin du pole observe. Cette verification est a faire dans le papier de reference, arXiv
   2411.10109, et elle n'a pas ete faite ici.
3. **La correspondance `divorced` vers `DIVORCE`** est deduite du libelle de la question et
   non d'un dictionnaire de variables. L'item est un temoin parmi 65, l'effet d'une erreur
   serait negligeable, mais la deduction est signalee dans `a25_commun.py`.
4. **Les poles de desirabilite marques [HYPOTHESE] portent le resultat de la section 4.**
   Sur les 10 items sensibles pourvus d'un pole, 4 sont [CONFIRME] par NORC, 2 [PROBABLE],
   4 [HYPOTHESE]. Un relecteur qui conteste la regle uniforme sur les items `nat*` conteste
   3 des 12 items. Aucune analyse de sensibilite au choix des poles n'a ete faite.
5. **Aucun test n'a ete fait sur Twin-2K-500 ni sur le WVS.** Le croisement NORC n'existe que
   pour le GSS.
6. **Les prompts de C2 et C3 n'ont toujours pas ete compares a ceux de l'archive de
   Stanford**, limite ouverte depuis a17 et a23. Une part de l'ecart attribue au modele peut
   venir de la formulation, et cela vaut ici comme ailleurs.
7. **Le p de permutation sur `agents v8`, 0,051, est a la frontiere** et bascule d'un cote ou
   de l'autre selon la graine. Il est rapporte tel quel, graine 20260908.

---

## Questions ouvertes pour Simon

1. **Le resultat de la section 3 vaut il d'etre porte, sachant que la section 4 tombe ?**
   La these vendable etait "la simulation rend presentable". Ce qui est mesure est "la
   simulation derape la ou l'humain se surveille, sans direction commune". C'est plus faible
   et c'est plus vrai. Est ce publiable en l'etat ou faut il d'abord la version continue de
   la prediction, point 1 de la section precedente ?
2. **Faut il recalculer les ecarts de mode sur les microdonnees du GSS 2022 ?** C'est ce qui
   transformerait un test a 12 items contre 65 en une correlation sur 149 items, avec une
   puissance sans commune mesure. Le GSS 2022 est en libre acces, le calcul est celui de
   NORC, et cela ouvre le point 2 de "Ce que personne n'a fait" : disposer simultanement
   d'une mesure du cache cote humain et de l'ecart cote agent.
3. **La direction negative est elle un resultat ou un defaut de nos agents ?** Sur `vote16`
   et `polabuse/y`, C2 et C3 produisent des populations que rien ne justifie. Faut il y voir
   une propriete des modeles de langage simulant des individus, ou un defaut de Qwen3-4B qui
   disparaitrait sur gpt-oss-20b ? La nuit de calcul deja prevue par a23 repond aussi a
   cette question, a condition de rejouer a25 dessus.
4. **La famille des items nominaux charges, `spkrac/y`, `polabuse/y`, `polattak/y`,
   `vote16`, doit elle etre isolee comme resultat a part ?** C'est la ou tout se joue. Le
   risque est le meme que celui de la famille des libertes civiles dans a23 : une famille
   choisie apres avoir vu les chiffres.
5. **Faut il fixer maintenant la famille d'hypotheses pour la correction des tests
   multiples ?** La dette est ouverte depuis a17 et ce rapport ajoute 117 tests. Tant qu'elle
   n'est pas fixee, aucun p du projet n'est defendable.
6. **Les poles de desirabilite doivent ils etre valides par un tiers ?** Ils sont ecrits en
   clair et contestables ligne a ligne dans `a25_commun.py`. Une validation par deux codeurs
   independants coute une heure et retire la principale objection a la section 4.

---

## Rejouer

```
.venv/bin/python analyses/a25_mesures.py --cache /tmp/a25-matrices.pkl --bootstrap 1000
.venv/bin/python analyses/a25_contrastes.py --tirages 10000
.venv/bin/python analyses/a25_figure.py --perimetre 150
```

Sans le cache, `a25_mesures.py` recalcule les baselines de a2, environ trois minutes ; avec
le cache, six secondes. `a25_contrastes.py` prend neuf secondes, la figure deux. Graine
20260908 partout. Aucun appel de modele, aucune ecriture dans `data/`.
