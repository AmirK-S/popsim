# C7-résidu-trajectoire, résultats : le résidu tombe de 10× à 2,5×, et son amplitude reste indécidable

statut: courant
fait_foi: resultats/c7-residu-trajectoire.csv
mandat: trancher si le residu de ~10x de la trajectoire 2023->2025, a nombre d'items apparie, est reel ou un artefact
agent: mesures : residu de trajectoire, 13/09
ecriture: analyses/c7_residu_trajectoire.py, resultats/c7-residu-trajectoire-preenregistrement.md, resultats/c7-residu-trajectoire-resultats.md, resultats/c7-residu-trajectoire.csv
lecture_seule: tout le reste, en particulier analyses/c7_temoins_relecture.py (agent parallele)
interdits: appel d'API payant, reseau, recherche web, arriere-plan, fusion sur master
cout_reel_usd: 0.00

Préenregistré dans `resultats/c7-residu-trajectoire-preenregistrement.md` **avant toute
mesure d'attaque nouvelle** ; calculé par `analyses/c7_residu_trajectoire.py` (graine
20260913, `.venv/bin/python`, aucun appel réseau, aucune dépense). Sortie :
`resultats/c7-residu-trajectoire.csv` (102 lignes).
Étude de risque de vie privée sur deux jeux déjà publics (Twin-2K-500 ; Argyle et al.
2023, Harvard Dataverse `doi:10.7910/DVN/JPV20K`, CC0). Aucun identifiant, aucun
appariement individuel n'est imprimé ni écrit.

**Verdict en une ligne : le résidu n'est pas nul, mais il est quatre fois plus petit
qu'annoncé et son amplitude n'est pas estimable.** À information effective appariée, le
contraste 2023 → 2025 tombe de ≈ 10× à **2,5×** ; rapporté à ce qu'un simple plus proche
voisin obtient avec les mêmes items, il tombe à **1,3×**. Le bout gauche échoue son
propre contrôle d'interprétabilité, le bout droit ne le passe que sur trois des cinq
sous-ensembles d'items appariés. **La trajectoire garde un sens, pas un chiffre.**

---

## 1. Confrontation à la prédiction préenregistrée

| grandeur à M2 (n_eff = 4,31) | prédiction | intervalle prédit | observé | |
|---|---|---|---|---|
| top-1 jumeau `JSON Persona - GPT4.1` | 0,55 % | [0,25 ; 1,20] | **0,3412 %** | dans l'intervalle |
| top-1 `Demographics Only` | 0,20 % | [0,08 ; 0,45] | **0,1349 %** | dans l'intervalle |
| rapport à la baseline | 2,7 | [1,3 ; 5,0] | **2,53** | dans l'intervalle |
| rapport à la baseline à M3 | 3,2 | [1,6 ; 5,5] | **4,65** | dans l'intervalle |
| invariance au bassin (A2), côté Twin | ± 20 % | — | 2,42 / 2,61 / 2,39 | vérifiée |
| **contrôle d'interprétabilité à M2** | **ÉCHEC attendu** | — | **PASSE en agrégé, 3/5 sous-ensembles** | **prédiction réfutée** |

**Ma prédiction centrale est réfutée** : je m'attendais à ce que le jumeau Twin cesse de
battre sa propre baseline une fois l'information effective ramenée au niveau d'Argyle.
Il la bat encore (0,3412 % [0,2853 ; 0,3983] contre 0,1349 % [0,1081 ; 0,1629], IC
disjoints). La règle R1(a) n'est donc **pas** déclenchée, et je ne peux pas écrire que le
résidu est un pur artefact d'information effective. Les cinq autres grandeurs sont dans
leurs intervalles prédits, ce qui n'est pas un mérite : elles étaient larges.

Réfutation secondaire, dans l'autre sens : je n'avais pas prévu que le contrôle
échouerait sur **2 des 5** sous-ensembles appariés pris un par un. Le « PASSE » agrégé
masque une fragilité que le préenregistrement ne demandait pas de mesurer et que je
rapporte quand même.

## 2. Les entrées d'appariement, recalculées ici (humains seuls)

| grandeur | Twin-2K-500 | Argyle 2023 |
|---|---|---|
| bassin attaqué | 2 058 | 2 148 |
| items | 60 | 12 |
| **items effectifs** (V̄ de Cramér) | **10,13** (V̄ = 0,0834) | **4,31** (V̄ = 0,1620) |
| entropie humaine totale | 80,91 bits | 21,30 bits |
| entropie moyenne par item | 1,349 bit | 1,775 bit |
| **bits effectifs** (n_eff × H̄) | **13,66** | **7,66** |
| manquants sur les items utilisés | **0,0000 %** | 0,0000 % |
| lignes écartées pour construire le bassin | **0 %** | **49,70 %** |
| modalités par item (médiane / max) | 2 / 7 | 4 / 73 |
| accord test-retest humain | **74,47 %** | **non mesurable** |

Tous les chiffres déjà publiés ailleurs sont retrouvés à la décimale (4,31 ; 10,13 ;
21,30 bits ; 20,694 % à 60 items). Deux faits **nouveaux** et non anodins apparaissent
ici :

- **Le bassin Argyle écarte 49,7 % des lignes** pour au moins un item manquant, là où le
  bassin Twin n'en écarte aucune. Le bout gauche de la trajectoire est donc mesuré sur
  une sous-population « qui répond à tout », auto-sélectionnée ; le bout droit non.
  Ce n'est pas un artefact de **non-réponse résiduelle** (A5 est bien à 0 % des deux
  côtés sur les items utilisés), c'est un artefact de **sélection du bassin**, que la
  mission ne listait pas et que je ne peux pas neutraliser (on ne peut pas attaquer des
  lignes incomplètes sans rouvrir le motif de manquants comme empreinte).
- **Un des 12 items d'Argyle (`voted_2016`) n'a qu'une seule modalité** sur ce bassin :
  il transporte exactement zéro bit. Le bout gauche a donc 11 items informatifs, pas 12,
  ce qui aggrave encore le défaut de l'appariement « 12 contre 12 ».

## 3. La courbe : le nombre d'items gonfle **tout ce qui attaque**, pas seulement le jumeau

Twin-2K-500, jumeau `JSON Persona - GPT4.1`, 2 058 personnes, 30 tirages d'items par k.
IC 95 % en **double bootstrap** (personnes × tirages d'items) : c'est la différence
avec le témoin de `relecture-fond` §D3, dont l'IC n'incluait pas la variance du tirage
d'items — et à faible k cette variance domine.

| k | n_eff mesuré | bits eff. | jumeau % [IC] | `Demographics Only` % | rapport [IC] | plafond humain % | classe ex æquo médiane |
|---|---|---|---|---|---|---|---|
| 4 | 3,20 | 4,27 | 0,182 [0,163 ; 0,203] | 0,097 | 1,87 [1,68 ; 2,10] | 0,69 | 68,5 |
| 5 | 3,75 | 5,03 | 0,247 [0,214 ; 0,282] | 0,121 | 2,05 [1,72 ; 2,39] | 1,23 | 29,8 |
| **6** | **4,25** | 5,83 | **0,325** [0,268 ; 0,384] | 0,127 | **2,56** [2,07 ; 3,12] | 2,20 | 11,5 |
| 7 | 4,65 | 6,38 | 0,472 [0,397 ; 0,552] | 0,174 | 2,71 [2,18 ; 3,41] | 3,31 | 6,5 |
| 8 | 5,05 | 6,71 | 0,670 [0,537 ; 0,819] | 0,192 | 3,49 [2,75 ; 4,49] | 4,73 | 4,1 |
| 10 | 5,74 | 7,74 | 0,958 [0,774 ; 1,137] | 0,263 | 3,64 [2,87 ; 4,60] | 8,11 | 2,9 |
| **12** | **6,28** | 8,71 | **1,160** [0,938 ; 1,399] | 0,245 | **4,73** [3,71 ; 6,37] | 11,88 | 2,0 |
| 16 | 7,12 | 9,37 | 2,391 [2,022 ; 2,791] | 0,422 | 5,67 [4,52 ; 7,04] | 21,46 | 2,0 |
| 20 | 7,74 | 10,41 | 3,280 [2,732 ; 3,871] | 0,502 | 6,53 [5,10 ; 8,41] | 30,69 | 2,0 |
| 30 | 8,78 | 11,93 | 6,454 [5,713 ; 7,291] | 0,880 | 7,33 [5,87 ; 9,31] | 52,10 | 1,0 |
| 40 | 9,41 | 12,74 | 10,548 [9,439 ; 11,745] | 1,223 | 8,63 [6,96 ; 11,06] | 66,81 | 1,0 |
| **60** | **10,13** | 13,66 | **20,694** [19,020 ; 22,359] | 2,145 | **9,65** [7,48 ; 13,10] | 81,60 | 1,0 |

Trois lectures, dont deux nouvelles :

1. **Le point de raccord est bon.** 20,694 % à k = 60 reproduit exactement le chiffre
   publié, et 1,160 % à k = 12 est compatible avec le 1,2193 % [1,1118 ; 1,3301] mesuré
   indépendamment sur la branche `agent/mesures/temoins-relecture` (mon IC est plus
   large parce qu'il inclut la variance du tirage d'items, le leur non). Les deux
   mesures ne se contredisent pas.
2. **La baseline démographique gagne elle aussi un facteur ≈ 8,7 entre 12 et 60 items**
   (0,245 % → 2,145 %), contre ≈ 17,8 pour le jumeau. Le nombre d'items gonfle
   **n'importe quel attaquant**, y compris celui qui ne connaît que quatre variables
   démographiques. Ce point, signalé par l'agent des témoins, est confirmé ici :
   il est fatal à toute lecture du contraste brut comme « progrès des modèles ».
3. **Le rapport à la baseline gonfle aussi**, de 4,73 à 9,65 entre 12 et 60 items.
   Autrement dit, **normaliser par la baseline ne suffit pas** à neutraliser le nombre
   d'items : la normalisation absorbe la moitié du facteur, pas la totalité. C'est
   exactement pourquoi l'appariement doit porter sur l'information effective, pas sur
   le nombre brut.

## 4. Les quatre régimes appariés : le résidu, artefact par artefact

30 sous-ensembles d'items par régime, tirés **par rejet** sur la grandeur d'appariement
**mesurée** (et non choisis par un k a priori). Tous à bassin 2 058, même attaque, même
jumeau, même baseline recalculée sur les mêmes items.

| régime | n_eff mesuré | k effectif | jumeau % [IC] | baseline % | **rapport** [IC] | contrôle |
|---|---|---|---|---|---|---|
| **M1** items bruts = 12 | 6,31 | 12 | 1,298 [1,045 ; 1,588] | 0,276 | **4,70** [3,75 ; 5,95] | PASSE (5/5) |
| **M2** items effectifs = 4,31 | **4,30** | 6–7 | **0,341** [0,285 ; 0,398] | 0,135 | **2,53** [2,02 ; 3,14] | PASSE (**3/5**) |
| **M3** bits effectifs = 7,66 | 5,77 | 7–20 | 1,540 [0,856 ; 2,439] | 0,331 | **4,65** [3,42 ; 5,91] | PASSE (5/5) |
| **M4** entropie brute = 21,3 bits | 7,14 | 13–19 | 2,447 [1,920 ; 3,018] | 0,441 | **5,55** [4,52 ; 6,94] | PASSE (5/5) |
| *Argyle 2023, 12 items* | *4,31* | *12* | *0,137 [0,042 ; 0,258]* | *0,095* | ***1,44–1,48*** | **ÉCHEC** |

### Ce que devient le résidu, artefact par artefact

| artefact neutralisé | contraste brut Twin/Argyle | contraste en rapport à la baseline |
|---|---|---|
| rien (chiffres publiés, 60 vs 12 items) | ≈ 150× | 9,65 / 1,48 = **6,5×** |
| **A1a** nombre d'items **brut** apparié (M1) | 1,298 / 0,135 = **9,6×** | 4,70 / 1,48 = **3,2×** |
| **A1b** items **effectifs** appariés (M2) | 0,341 / 0,135 = **2,5×** | 2,53 / 1,48 = **1,7×** |
| **A4** information effective en **bits** appariée (M3) | 1,540 / 0,135 = 11,4× | 4,65 / 1,48 = 3,1× |
| **A3'** en plus, normalisé au **B-oracle** (§6) | — | 1,26 / 0,96 = **1,3×** |

**A1 (items effectifs) est, de loin, le plus gros artefact restant : il divise le résidu
par 3,8** (de 9,6× à 2,5×). Apparier le nombre brut d'items, comme le faisait le témoin
de `relecture-fond`, laisse au bout droit un excédent de 46 % d'information indépendante
(6,31 items effectifs contre 4,31) ; c'est cet excédent qui fabriquait l'essentiel du
« résidu ».

**M3 va dans l'autre sens et je le signale sans l'écarter.** Apparier les *bits*
effectifs plutôt que les *items* effectifs laisse le résidu à 11,4× — plus haut qu'à
M1. La raison est mécanique : les items ANES sont individuellement plus riches
(1,775 bit contre 1,349), donc apparier en bits oblige à donner **plus** d'items à Twin
(7 à 20, moyenne 5,77 items effectifs). Les deux appariements ne peuvent pas être
satisfaits en même temps : **aucun sous-ensemble de Twin n'a simultanément 4,31 items
effectifs et 7,66 bits effectifs**, parce que Twin n'a tout simplement pas d'items aussi
riches que l'âge à l'année exacte. C'est une limite de l'appariement, pas un choix : je
retiens M2 comme régime de verdict (c'est l'appariement demandé par la mission et le
seul qui égalise l'information *indépendante*), et je publie M3 et M4 pour que la
fourchette soit visible. **Selon le critère d'appariement retenu, le résidu vaut entre
1,3× et 11,4×.** C'est en soi le résultat le plus honnête de ce rapport.

## 5. A2 — taille du bassin : neutralisée côté Twin, et elle révèle que le bout gauche n'est pas estimable

Sous-échantillonnage sans remise, 5 tirages, baseline **recalculée dans chaque
sous-bassin**.

| N | Twin à M2 : jumeau / baseline → rapport | Argyle 12 items : jumeau / baseline → rapport |
|---|---|---|
| 2 058 | 0,397 % / 0,164 % → **2,42** | 0,143 % / 0,043 % → **3,33** |
| 1 500 | 0,578 % / 0,221 % → **2,61** | 0,154 % / 0,067 % → **2,29** |
| 1 052 | 0,774 % / 0,324 % → **2,39** | 0,223 % / 0,061 % → **3,65** |

- **Côté Twin, le rapport est stable** (2,39 à 2,61, ±5 %) alors que les niveaux
  absolus doublent : A2 est neutralisé, et la règle R1(c) n'est pas déclenchée. Un
  bassin plus petit gonfle le top-1, exactement comme `c7-anomalie-park` l'avait établi,
  mais il gonfle le jumeau et la baseline dans la même proportion.
- **Côté Argyle, le rapport erre entre 2,29 et 3,65** sur trois sous-bassins du même
  jeu, quand la valeur publiée sur le bassin complet est 1,44–1,48. Ce n'est pas une
  dépendance au bassin : c'est l'absence d'estimateur. **Le « 1,5 » du bout gauche
  n'est pas une mesure, c'est une réalisation** — trois hits de plus ou de moins sur
  2 148 personnes le déplacent d'un facteur 2,5. Aucun contraste construit sur ce
  dénominateur n'a d'amplitude définie.

## 6. A3 — le plafond : ce qu'on peut mesurer, et ce qu'on ne peut pas

**Ce qui n'est pas mesurable, et je ne le contourne pas.** L'ANES 2016 ne remesure pas
les mêmes items sur les mêmes personnes : **il n'y a pas de test-retest côté Argyle**.
Le plafond de fiabilité humaine du bout gauche est inconnu et le restera sans une
ressource que nous n'avons pas. Je note seulement que, s'il était **plus haut** que
celui de Twin (74,47 %, mesuré ici), il prédirait **plus** de fuite côté Argyle, pas
moins — comme H4 de `c7-anomalie-park`. L'artefact irait donc dans le sens qui rend le
résidu plus difficile à expliquer, pas plus facile.

**Le substitut, mesurable des deux côtés : B-oracle**, l'imputeur au plus proche voisin
laisse-un-item-dehors qui dispose exactement des mêmes items que le jumeau. Il fixe ce
qu'un attaquant **sans modèle de langage** obtient avec la même information — un plafond
d'information, à défaut d'un plafond de fiabilité. Mesuré sur **exactement les mêmes
sous-ensembles d'items** que le jumeau et sous la même convention d'ex æquo.

| régime | jumeau % | B-oracle % | plafond retest humain % | **jumeau / oracle** | jumeau / plafond |
|---|---|---|---|---|---|
| M1 (12 items bruts) | 1,716 | 0,881 | 12,807 | **1,95** | 0,13 |
| **M2 (items effectifs appariés)** | **0,397** | **0,315** | 2,383 | **1,26** | 0,17 |
| M3 (bits effectifs appariés) | 2,120 | 0,725 | 12,852 | 2,92 | 0,16 |
| M4 (entropie brute appariée) | 2,474 | 1,152 | 22,014 | 2,15 | 0,11 |
| *Argyle 2023, 12 items* | *0,135* | *0,140* | *non mesurable* | ***0,96*** | *—* |

**C'est la mesure la plus dure pour la trajectoire.** À information effective appariée,
le jumeau de 2025 n'apporte que **26 %** de plus qu'un plus proche voisin classique
disposant des mêmes items ; celui de 2023 n'apporte rien (0,96, il est *sous* l'oracle).
Le résidu, exprimé dans cette normalisation-là, vaut **1,3×** — et l'IC du bout gauche
(0,042 ; 0,258) contient largement 1,26. **Sur ce critère, le résidu n'est pas
distinguable de zéro.**

Le jumeau ne dépasse jamais 17 % du plafond humain de test-retest, à aucun régime.

## 7. La convention d'ex æquo : à information appariée, le bout DROIT dégénère aussi

Défaut D9 de `relecture-fond` : sous 1 %, le top-1 est une convention de départage. Il
était établi pour Argyle (plage de facteur 13). Il vaut **aussi**, et bien plus fort,
pour Twin une fois l'information appariée.

| régime | ex æquo **favorable** | espérance (publié) | ex æquo **défavorable** | plage |
|---|---|---|---|---|
| M1 (12 items) | 3,766 % | 1,298 % | 0,580 % | ×6,5 |
| **M2 (items effectifs appariés)** | **4,193 %** | **0,341 %** | **0,032 %** | **×130** |
| M3 | 4,104 % | 1,540 % | 0,802 % | ×5,1 |
| M4 | 4,992 % | 2,447 % | 1,446 % | ×3,5 |

À M2, la classe d'ex æquo de tête compte **11,5 candidats en médiane** (contre 1 à 60
items) : le chiffre de 0,341 % est un point à l'intérieur d'une plage de **facteur 130**
fixée par convention. Le *rapport* à la baseline, lui, résiste mieux (2,54 sous la
convention favorable, 3,33 sous la défavorable, 2,53 en espérance) parce que la
convention frappe le jumeau et la baseline ensemble — raison supplémentaire de publier
le rapport plutôt que le taux. **Mais la comparaison de deux taux bruts entre les deux
bouts de la trajectoire, à information appariée, n'a plus de sens :** des deux côtés, le
chiffre dépend d'une convention.

## 8. Tableau des artefacts : ce qui est neutralisé, ce qui ne l'est pas

| # | artefact | neutralisé ? | ce qu'il reste du résidu après |
|---|---|---|---|
| **A1** | items effectifs | **oui** (appariement par rejet à n_eff = 4,31) | **2,5× brut, 1,7× à la baseline** (contre 9,6× / 3,2× à items bruts) |
| **A2** | taille du bassin | **oui** côté Twin (rapport stable 2,39–2,61 de N = 2 058 à 1 052) | inchangé côté Twin ; côté Argyle, révèle que le dénominateur n'est pas estimable (2,29–3,65) |
| **A3** | plafond de fiabilité humaine | **non** côté ANES (pas de remesure) ; substitut B-oracle mesuré des deux côtés | **1,3×**, et l'IC du bout gauche contient cette valeur |
| **A4** | nature des items (modalités, entropie) | **partiellement** (M3, M4) ; les deux appariements sont **incompatibles** | entre 1,3× et 11,4× selon le critère retenu |
| **A5** | non-réponse | **oui**, 0 % des deux côtés sur les items utilisés | inchangé — mais voir la **sélection du bassin** ci-dessous |
| **A5'** | **sélection du bassin** (nouveau, non listé dans la mission) | **non** : Argyle écarte 49,7 % des lignes, Twin 0 % | non chiffrable ; direction inconnue |
| **A6** | population et époque (ANES 2016 vs Twin 2025) | **non**, irréductible | non chiffrable |
| **A7** | **convention d'ex æquo** (nouveau) | **non**, mais bornée | plage de facteur 130 sur le taux à M2 ; le rapport, lui, tient (2,54–3,33) |

Deux artefacts que la mission ne listait pas se sont ajoutés en cours de mesure (A5'
sélection du bassin, A7 convention d'ex æquo) et **aucun des deux n'est neutralisable**.

## 9. Verdict, selon la règle de décision préenregistrée

- **R1 (artefact) n'est pas déclenchée** : le jumeau Twin passe le contrôle à M2 en
  agrégé (a), l'IC de son rapport [2,02 ; 3,14] ne contient pas 1,5 (b), et le rapport
  est stable sous variation du bassin (c).
- **R2 (réel) n'est pas satisfaite non plus** : elle exige que le contrôle passe à M2
  *et* à M3. Il passe en agrégé, mais **seulement sur 3 des 5 sous-ensembles appariés
  de M2** pris un par un. Un résultat qui dépend du tirage d'items dans 40 % des cas
  n'est pas un résultat robuste.
- **R3 s'applique, et elle est inconditionnelle** : le dénominateur du contraste
  (0,135 %, Argyle) échoue son propre contrôle d'interprétabilité — sous l'attaque naïve
  comme sous l'attaquant fort (`relecture-fond` §D2), sur les trois versions de jumeaux
  (`c7-argyle-resultats` §4) — et le §5 ci-dessus montre qu'il n'est même pas estimable.
  **Aucun chiffre calculé ici ne peut rendre défini un rapport dont le dénominateur est
  du bruit.**
- **R4 s'applique** : A3 côté ANES, A5' et A6 ne sont pas neutralisables.

### **Le résidu est INDÉCIDABLE en amplitude, et sa borne haute honnête est 2,5×, pas 10×.**

Ce qui est établi, et qui ne dépend d'aucune convention :

1. **Le nombre d'items brut n'apparie rien.** À nombre d'items apparié, le bout droit
   garde 46 % d'information indépendante en plus. Une fois cet excédent retiré, le
   contraste passe de 9,6× à **2,5×** : **l'appariement sur l'information effective
   absorbe les trois quarts du résidu qui restait.**
2. **Le nombre d'items gonfle tout ce qui attaque**, baseline démographique comprise
   (×8,7 de 12 à 60 items), et gonfle même le *rapport* à la baseline (de 4,7 à 9,7).
   Normaliser par la baseline ne suffit donc pas à retirer ce confondu.
3. **À information effective appariée, le jumeau de 2025 n'apporte que 26 % de plus
   qu'un plus proche voisin sans modèle de langage**, et celui de 2023 n'apporte rien.
   La différence entre 1,26 et 0,96 n'est pas séparable du bruit.
4. **Une asymétrie qualitative survit, et c'est tout ce qui survit** : sur les mêmes
   items effectifs, le même bassin et la même attaque, le jumeau de 2025 dépasse sa
   baseline démographique (IC disjoints, sur 3 sous-ensembles d'items sur 5) là où
   aucun des trois jumeaux de 2023 ne dépasse la sienne (IC chevauchants, sur toutes
   les mesures, naïves et fortes). C'est une différence de **direction**, pas de
   **facteur**.

## 10. La phrase que l'article a le droit d'écrire

Une seule, et elle remplace l'accroche de trajectoire dans le titre, l'abstract, §1.1,
§1.3 (1) et §5.8.

> At matched **effective** information — 4.3 independent items on both sides, the same
> pool size, the same attack and the same tie-breaking convention — the twins of 2025
> exceed their own demographic baseline (0.34 % [0.29 ; 0.40] against 0.13 %
> [0.11 ; 0.16]) while none of the three twins of 2023 exceeds theirs. Matching on the
> raw number of items is not enough: twelve Twin items still carry 46 % more independent
> information than the twelve ANES items, and the number of items inflates every
> attacker, the demographic baseline included, by a factor of 8.7 between 12 and 60
> items. We therefore report a **direction, not a magnitude**: the 2023 endpoint fails
> our interpretability control and is not estimable (its ratio to baseline wanders
> between 1.4 and 3.7 across subsamples of its own pool), and relative to a
> nearest-neighbour attacker holding the same items the 2025 twin gains only 1.26 where
> the 2023 twin gains 0.96 — a difference we cannot separate from noise.

Et la phrase qu'il **n'a pas** le droit d'écrire : toute formulation portant un facteur
chiffré entre les deux époques — « 150× », « 15× », « 10× », et **y compris le 2,5×
mesuré ici**. Le 2,5× est une borne haute honnête sur ce que le résidu peut valoir, pas
une estimation : son dénominateur n'a pas d'estimateur.

## 11. Limites, réductions et honnêteté

- **Réductions déclarées** (mission : tout en avant-plan, toute réduction annoncée). Les
  étapes lourdes (contrôle officiel sous-ensemble par sous-ensemble, B-oracle,
  sous-échantillonnage de bassin) tournent sur **5** sous-ensembles appariés par régime
  au lieu de 30, et sur **5** tirages de bassin au lieu de 20 : à 30 sous-ensembles
  elles dépassaient l'heure. Les sous-ensembles retenus sont les cinq **premiers du
  tirage**, sans sélection. Les étapes 1 à 4, qui portent le verdict, ne sont pas
  réduites (30 sous-ensembles, 2 000 tirages de double bootstrap).
- **Le « 3/5 » du contrôle à M2 est mesuré sur 5 sous-ensembles** : c'est peu, et je ne
  prétends pas que la vraie fraction soit 60 %. Ce que la mesure établit est plus
  modeste : **il existe des sous-ensembles d'items appariés sur lesquels le contrôle
  échoue**, donc le résultat dépend du tirage. Une mesure sur 30 sous-ensembles
  (≈ 25 minutes) donnerait la fraction ; elle n'a pas été faite.
- **Un seul jumeau Twin testé** (`JSON Persona - GPT4.1`), choisi pour la comparabilité
  directe avec le témoin de `relecture-fond` §D3. Rien ici ne dit ce que donneraient les
  autres configurations, dont certaines fuient trois fois plus.
- **M2 et M3 sont incompatibles** (§4) : aucun sous-ensemble de Twin n'apparie
  simultanément les items effectifs et les bits effectifs d'Argyle. Le choix de M2 comme
  régime de verdict est un choix, argumenté, pas une nécessité.
- **A3 côté ANES, A5' et A6 restent ouverts** et ne sont pas contournables avec les
  données sur disque. Si l'un d'eux suffit à expliquer le résidu, ce rapport ne peut pas
  le savoir.
- **Ce résultat ne contredit pas Argyle et al.** Leur étude 3 porte sur des matrices de
  corrélations entre variables, pas sur l'exactitude individuelle ; un jumeau peut
  reproduire une structure d'association sans identifier personne. Réserve reprise de
  `c7-argyle-resultats.md` §9.

## En clair

L'article annonçait une trajectoire : le hasard en 2023, 60 % aujourd'hui. Une première
relecture avait montré que le nombre de questions posées expliquait déjà un facteur
quinze de cet écart, et qu'il restait un facteur dix. Ce rapport montre que le facteur
dix vient, pour l'essentiel, de la même cause mal comptée : douze questions de Twin ne
valent pas douze questions de l'ANES, parce qu'elles sont moins redondantes entre elles
et portent presque moitié plus d'information indépendante. Une fois les deux jeux
ramenés à la même quantité d'information réellement indépendante, l'écart tombe de dix
à deux et demi — et si l'on demande en plus ce que le jumeau apporte par rapport à un
simple appariement statistique qui ne coûte rien, il tombe à 1,3, c'est-à-dire à rien de
démontrable. Il reste une différence de nature, pas de degré : le jumeau d'aujourd'hui
fait mieux que la démographie seule, celui de 2023 ne le faisait pas. C'est vrai, c'est
mesuré, et c'est tout ce que l'article peut écrire. Le chiffre, lui, doit partir : le
point de départ de la trajectoire est trop bruité pour qu'on puisse diviser quoi que ce
soit par lui.
