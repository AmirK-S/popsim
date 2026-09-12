# C7 monde ouvert, intervalles de confiance : le défaut d'A3 (attaque naïve)

Calculé par `analyses/c7_monde_ouvert_ic.py`, qui importe `analyses/c7_monde_ouvert.py` et
`analyses/c7_reidentification.py` **tels quels** (aucune modification). Données :
`resultats/c7-monde-ouvert-ic.csv`. Aucun identifiant ni appariement individuel imprimé.

## 0. Préenregistrement (écrit avant tout calcul de bootstrap, repris du script)

**Périmètre.** A3 cite deux familles de chiffres : (a) l'attaque **naïve** (accord de Hamming),
calculée par `c7_monde_ouvert.py` — 3,04 % / 20,39 % à FPR = 1 %, 0,93 % / 8,47 % à FPR = 0,1 %,
plafond humain 54,5 % / 90,7 % ; (b) l'attaque **forte** (A-LLR hors pli, `c7_attaquant_fort.py`)
— **60,17 %**, 44,37 %, 4,28 %, 1,01 %. La consigne de ce script restreint les imports à
`c7_monde_ouvert.py` et `c7_reidentification.py` : **le 60,17 % est donc hors périmètre ici**,
il appartient à l'agent qui a la main sur `c7_attaquant_fort.py`. Ce rapport ne calcule l'IC que
pour la famille (a).

**Attente 1 (largeur).** À FPR = 1 %, l'échantillon (1 052 à 2 058 personnes) devrait donner un
IC raisonnable (quelques points). À FPR = 0,1 %, le seuil est calé sur environ 1 à 3 personnes :
l'IC devrait être très large, potentiellement un facteur 3 à 10 entre bornes, et pourrait toucher
zéro en bas.

**Attente 2 (rejeu du seuil).** Le seuil est choisi **après** avoir vu les données (interpolation
sur la courbe ROC du même échantillon que celui où le TPR est lu). Un bootstrap qui fixerait ce
seuil une fois pour toutes sous-estimerait la variabilité, surtout à 0,1 %. Attente : l'IC avec
seuil rejoué à chaque tirage est plus large que l'IC à seuil fixe, l'écart étant plus marqué à
0,1 % qu'à 1 %.

**Méthode.** Bootstrap non paramétrique sur les personnes attaquées, 2 000 tirages, graine fixée
(`[20260912, 99, ...]`). Le pool de candidats (référence) n'est **pas** rééchantillonné — seules
les lignes (personnes attaquées, avec remise) le sont ; cela évite qu'une personne dupliquée comme
candidat ne fausse sa propre marge de confiance. `marges_deux_regimes` et `roc_et_taux`
(importées sans modification) sont rappelées à neuf sur chaque tirage : le seuil est donc rejoué
par construction dans la colonne recommandée. Une seconde colonne, à seuil fixé sur le seul
échantillon observé, est calculée en parallèle pour chiffrer l'écart annoncé en attente 2.
Déviation documentée : le nombre de tirages de départage des ex-æquo de marge est réduit de 5
(valeur de `c7_monde_ouvert.py`) à 1 dans le bootstrap seulement, pour tenir le calcul en temps
raisonnable ; l'estimation ponctuelle garde n_tirages = 5, identique au rapport publié (les
valeurs ponctuelles retrouvées ci-dessous, 20,62 % / 0,93 % / 3,04 % Twin et 65,68 % / 8,47 % /
20,39 % Stanford, collent au dixième de point près à `c7-monde-ouvert-resultats.md`, sanity check
réussi).

## 1. Résultats

IC à 95 %, percentile, 2000 tirages. « FP absolus » = nombre attendu de faux positifs (en
personnes) qui définissent le seuil à ce FPR sur l'échantillon observé (= FPR cible × n).

| jeu | prédicteur | n | top-1 monde fermé [IC] | TPR@FPR=0,1 % [IC seuil rejoué] | FP absolus @0,1 % | TPR@FPR=1 % [IC seuil rejoué] | FP absolus @1 % |
|---|---|---|---|---|---|---|---|
| Twin | **Meilleur jumeau (JSON Persona GPT4.1)** | 2058 | 20,62 % [18,95 ; 22,40] | **0,93 % [0,23 ; 1,56]** | **≈2** | **3,04 % [2,01 ; 3,99]** | ≈21 |
| Twin | Demographics Only | 2058 | 2,08 % [1,55 ; 2,82] | 0,10 % [0,00 ; 0,29] | ≈2 | 0,20 % [0,05 ; 0,40] | ≈21 |
| Twin | PMM k=10 | 2058 | 0,07 % [0,00 ; 0,19] | 0,00 % [0,00 ; 0,00] | ≈2 | 0,00 % [0,00 ; 0,00] | ≈21 |
| Twin | Retest humain (plafond) | 2058 | 81,66 % [79,88 ; 83,24] | 36,86 % [13,56 ; 42,62] | ≈2 | 54,49 % [50,76 ; 57,55] | ≈21 |
| Stanford | **Meilleur agent (composite)** | 1052 | 65,68 % [62,83 ; 68,44] | **8,47 % [2,45 ; 16,20]** | **≈1** | **20,39 % [15,67 ; 24,49]** | ≈11 |
| Stanford | démographique | 1052 | 2,28 % [1,43 ; 3,14] | 0,00 % [0,00 ; 0,00] | ≈1 | 0,00 % [0,00 ; 0,00] | ≈11 |
| Stanford | PMM k=10 | 1052 | 0,53 % [0,10 ; 1,05] | 0,00 % [0,00 ; 0,00] | ≈1 | 0,00 % [0,00 ; 0,00] | ≈11 |
| Stanford | Retest humain (plafond) | 1052 | 96,75 % [95,63 ; 97,81] | 63,53 % [19,90 ; 87,88] | ≈1 | 90,69 % [88,18 ; 93,35] | ≈11 |

## 2. Le point délicat : FPR = 0,1 % repose sur une poignée de personnes

À FPR = 0,1 %, le seuil est calé sur **≈ 2 personnes sur 2 058** (Twin) et **≈ 1 personne sur
1 052** (Stanford) — dans les deux cas **sous la barre de 10** fixée par la mission. C'est une
estimation très instable : le TPR à 0,1 % ne doit pas être présenté comme un point ponctuel fiable.
Cela se voit directement dans les IC : Twin meilleur jumeau **0,93 % [0,23 ; 1,56]** (facteur ~7
entre bornes), Stanford meilleur agent **8,47 % [2,45 ; 16,20]** (facteur ~7 aussi, et l'IC bas
touche presque zéro pour Twin). Le plafond humain est encore plus instable à ce FPR : Stanford
**63,5 % [19,9 ; 87,9]** — l'IC couvre presque toute la plage possible. À FPR = 1 %, le nombre de
faux positifs (~21 et ~11) est plus grand et les IC nettement plus resserrés, sans être étroits
pour autant (Stanford composite : 15,7–24,5 points, soit ±4,5 points autour de 20,4 %).

## 3. Le seuil est choisi après avoir vu les données — et le rejeu change le résultat

`roc_et_taux` obtient le seuil à FPR cible par interpolation sur la courbe ROC calculée sur le
**même** échantillon que celui où le TPR est ensuite lu : c'est un choix de seuil **a posteriori**,
pas préenregistré à une valeur de marge fixée à l'avance. L'IC doit donc rejouer ce choix dans
chaque tirage bootstrap, sous peine d'être trop étroit.

C'est confirmé, et l'effet est important, surtout à 0,1 % :

| | FPR=0,1 % : largeur seuil rejoué | largeur seuil fixe | ratio | FPR=1 % : largeur seuil rejoué | largeur seuil fixe | ratio |
|---|---|---|---|---|---|---|
| Twin, meilleur jumeau | 1,33 pt | 0,83 pt | ×1,6 | 1,98 pt | 1,51 pt | ×1,3 |
| Stanford, meilleur agent | 13,76 pt | 3,33 pt | **×4,1** | 8,83 pt | 4,94 pt | ×1,8 |
| Twin, plafond humain | 29,06 pt | 4,18 pt | **×7,0** | 6,79 pt | 4,47 pt | ×1,5 |
| Stanford, plafond humain | 67,98 pt | 5,70 pt | **×11,9** | 5,16 pt | 3,61 pt | ×1,4 |

Un bootstrap à seuil fixé (ne rejouant que le TPR, pas le seuil) aurait donné, pour Stanford à
FPR = 0,1 %, un IC **quatre fois trop étroit** : le rejeu n'est pas un raffinement cosmétique,
c'est la différence entre un IC honnête et un IC qui masque l'instabilité du seuil. L'écart croît
avec l'instabilité du seuil (le plus petit nombre de faux positifs, Stanford, montre le plus grand
écart), conforme à l'attente 2.

## 4. Formulation exacte à écrire dans le manuscrit (attaque naïve)

> À un taux de fausses accusations de 1 %, le meilleur jumeau retrouve la bonne personne
> **3,04 % [IC 95 % 2,0 ; 4,0]** du temps sur Twin-2K-500 et **20,39 % [15,7 ; 24,5]** sur
> l'archive Park, sous bootstrap sur les personnes (2000 tirages, seuil recalculé dans chaque
> tirage). À FPR = 0,1 %, ces taux tombent à **0,93 % [0,2 ; 1,6]** et **8,47 % [2,5 ; 16,2]** —
> des intervalles larges car ce seuil n'est défini que par environ 2 et 1 faux positifs
> respectivement (sur 2 058 et 1 052 personnes) : un chiffre à traiter comme une estimation très
> instable, pas comme un taux mesuré avec précision. Les comparateurs (Demographics Only, PMM
> k=10) restent indiscernables du bruit aux deux FPR (IC touchant ou incluant zéro). Le plafond
> humain (retest), à FPR = 1 %, est de 54,5 % [50,8 ; 57,5] (Twin) et 90,7 % [88,2 ; 93,3]
> (Stanford) ; à FPR = 0,1 % il est trop instable pour être cité sans son IC (Stanford :
> 63,5 % [19,9 ; 87,9]).

**Ce que le manuscrit ne doit pas faire** : citer 0,93 % ou 8,47 % (ou tout chiffre à FPR = 0,1 %)
sans mentionner que le seuil sous-jacent repose sur moins de 10 faux positifs absolus — c'est
précisément ce qu'un relecteur PoPETs/USENIX vérifiera. Le 60,17 % (attaque forte) n'est pas
couvert par ce calcul et ne doit pas être présenté avec les IC ci-dessus : son IC relève de
l'agent en charge de `c7_attaquant_fort.py`.
