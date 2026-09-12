# C7, tautologie : résultats (12 septembre 2026)

Préenregistré dans `c7-tautologie-preenregistrement.md` (et son avenant du même jour),
calculé par `analyses/c7_tautologie.py`. **Reproductibilité : vérifiée empiriquement.**
Le script a été exécuté deux fois de bout en bout (2058 personnes, 5 réplicats, 20 tirages
de départage, bootstrap 2000) ; `diff` entre les deux `c7-tautologie.csv` obtenus est
vide — **identique bit à bit**, toutes colonnes (top-1, top-10, rang médian, bits, IC)
comprises. Les deux exécutions ont pris 159 s et 164 s.

## 0. Le garde-fou (bloquant) : vérifié

Après construction des quatre prédicteurs, le script recalcule l'exactitude réalisée par
personne (nombre de cellules où le prédicteur égale la vérité, sur les 60 items) dans
chaque condition et vérifie l'égalité bit à bit avec `k_i` (emprunté au jumeau réel), puis
l'égalité bit à bit entre les quatre vecteurs d'exactitude réalisée eux-mêmes. Log
effectif :

> `GARDE-FOU VERIFIE : exactitude par personne identique au bit pres entre les quatre
> conditions (et egale a k_i emprunte a JSON Persona - GPT4.1).`

Aucune des deux assertions (`np.array_equal`) n'a échoué ; le script ne s'est donc pas
arrêté prématurément. **Les quatre conditions ont, par construction et par vérification,
exactement le même nombre d'items exacts par personne** (moyenne 0,5904, médiane 0,600,
de 4 à 51 sur 60).

## 1. Où `y_ref` (la vraie réponse) intervient dans chaque condition — le point sur lequel
ce rapport est jugé

**Réponse directe et sans détour : les quatre conditions (a)-(d) copient toutes `y_ref`
sur exactement `k_i` positions par personne. C'est vrai des quatre, de façon identique.**
Ce n'est pas un vice caché découvert après coup : c'est écrit dans le préenregistrement
(section 1) et dans le docstring de `construire_predicteur`, AVANT le calcul. La question
n'est pas « est-ce que ça copie la cible » (oui, nécessairement) mais « est-ce que cela
invalide la mesure » — non, et voici pourquoi, condition par condition :

- **(a) hasard** : sur un sous-ensemble de `k_i` positions tiré au hasard et
  indépendamment par personne, `query = pool` (= `y_ref`). Sur les `60-k_i` autres,
  `query` vient de `valeurs_fausses`, tirée dans la marginale de population de l'item,
  jamais de la valeur de cette personne.
- **(b) concentré sur les items fréquents** : mêmes règles, mais l'ensemble des `k_i`
  positions où `query = y_ref` est choisi par un critère de POPULATION (rang d'entropie
  de l'item), identique pour tout le monde à `k_i` fixé — pas par un critère qui regarde
  la valeur de la personne.
- **(c) concentré sur les items rares** : symétrique de (b), même mécanique.
- **(d) corrélé entre personnes** : même mécanique, ordre fixe tiré une fois, indépendant
  de l'entropie et de toute personne particulière.

**Pourquoi ce n'est pas la faute relevée sur `c7_disjoint.construire_nul`.** Ce n'est pas
que la lecture de `y_ref` soit interdite en soi — c'est *inévitable* : « cette personne a
exactement `k_i` items exacts » est une phrase qui, par définition, exige que sur `k_i`
positions la valeur écrite soit la vraie valeur. Aucune construction ne peut fixer une
exactitude PAR PERSONNE, choisie à l'avance, sans à un moment lire la vérité de cette
personne pour savoir où la recopier. Le jumeau LLM réel, sur les items qu'il devine juste,
fait exactement la même chose : sa sortie égale la vérité. Ce n'est donc pas un défaut de
conception propre à nos quatre témoins ; **c'est la définition même de « exactitude
positive »**, vraie pour tout prédicteur, réel ou synthétique. La variable manipulée ici
n'est JAMAIS « lire ou non `y_ref` » (les quatre le font, identiquement) — c'est
uniquement la RÈGLE qui choisit QUELLES positions sont recopiées.

**Ce qui, lui, ne lit `y_ref` d'aucune personne pour construire sa PROPRE ligne** :
le témoin ajouté après l'alerte, `temoin_mode_global` (voir §3) — la modalité modale de
chaque item sur toute la population (`c7_bits.mode_item`), UN SEUL vecteur, identique
pour tout le monde. Il ne dépend de la personne i qu'à hauteur de sa contribution de
1/2058e à une statistique de population (convention déjà utilisée sans réserve dans ce
dépôt pour B0/B0 mode) — jamais de sa réponse individuelle pour écrire SA ligne à elle.
Son exactitude n'est pas calée sur `k_i` ; elle tombe où elle tombe (0,499).

**Conséquence honnête pour la portée de l'expérience** : parce que les quatre conditions
lisent toutes `y_ref` de la même façon, cette expérience ne teste PAS « un prédicteur
peut-il fuir sans jamais rien savoir de la vraie réponse » (question déjà tranchée
ailleurs, par PMM/B2, voir §4) — elle teste, à lecture de `y_ref` égale et à exactitude
égale, si la RÈGLE DE CHOIX des positions recopiées change la fuite. C'est exactement la
question préenregistrée en section 0 du préenregistrement, formulée pour pouvoir être
fausse. Elle ne peut pas répondre, et ne prétend pas répondre, à une question différente
(« la fuite existe-t-elle sans aucune lecture individuelle ») — pour celle-là, voir le
témoin (e) et PMM/B2 au §4.

## 2. Résultats mesurés

| condition | exactitude | top-1 [IC 95 %] | top-10 | rang médian | bits [IC 95 %] |
|---|---|---|---|---|---|
| (a) hasard | 0,5904 | **31,90 %** [30,18 ; 33,68] | 54,64 % | 7,5 / 2058 | 4,64 [4,46 ; 4,81] |
| (b) concentré fréquents (exact = rare) | 0,5904 | **27,66 %** [25,81 ; 29,57] | 50,69 % | 9,9 / 2058 | 4,30 [4,13 ; 4,47] |
| (c) concentré rares (exact = fréquent) | 0,5904 | **31,58 %** [29,71 ; 33,36] | 52,32 % | 8,9 / 2058 | 4,42 [4,25 ; 4,61] |
| (d) corrélé entre personnes | 0,5904 | **32,14 %** [30,32 ; 34,02] | 54,40 % | 7,3 / 2058 | 4,64 [4,45 ; 4,82] |
| hasard pur (repère) | — | 0,049 % | 0,49 % | ~1029 | — |

Toutes IC par bootstrap sur les personnes (2000 tirages) ; bits = borne dyadique +
Miller-Madow (`c7_bits.bits_et_ic`, IC bootstrap 2000 intégré).

## 3. Témoin supplémentaire, ajouté après l'alerte : aucune lecture individuelle

`temoin_mode_global` (modalité modale de population, un seul vecteur pour tout le monde,
exactitude naturelle non calée = 0,499) : **top-1 = 0,063 % [0,015 ; 0,129], top-10 =
0,47 %, bits = −0,004** (indiscernable de zéro — validation attendue d'un prédicteur
sans aucune information individuelle). Comparé à (a)-(d) : **entre 440 et 510 fois moins
de top-1**, malgré une exactitude proche (0,499 contre 0,590). C'est la mesure la plus
propre de ce que « aucune fuite individuelle » donne dans ce pipeline exact.

## 4. Repères externes (déjà publiés, non recalculés ici)

| repère | exactitude | top-1 | source |
|---|---|---|---|
| JSON Persona GPT4.1 (jumeau réel, celui qui fournit k_i ici) | 0,590 | 20,7 % | `c7-contre-examen-2026-09-11.md` |
| PMM k=10 (contexte, jamais l'item cible) | 0,475 | 0,23 % | idem |
| B2 argmax (contexte, jamais l'item cible) | 0,511 | 0,07 % | idem |
| retest humain (plafond) | 0,745 | 81,6 % | idem |

## 5. Verdict, règle de décision préenregistrée (section 4)

Pivot demandé : (b) contre (d). **top-1(b) = 27,66 % [25,81;29,57], top-1(d) = 32,14 %
[30,32;34,02], ratio b/d = 0,86.** Ce n'est ni le facteur ≥ 3 avec IC disjoints qui
confirmerait « l'exactitude n'explique pas tout », ni le recouvrement total qui validerait
la tautologie sans réserve : (b) est en fait **légèrement plus bas** que (d), pas plus
haut — l'inverse de ce qui était prédit — et l'écart global sur les quatre conditions
(max/min = 32,14/27,66 = **1,16**) est réel (les IC de (b) ne recouvrent pas ceux de (a),
(c), (d), qui se recouvrent entre eux) mais **petit** au regard des écarts déjà connus
dans ce dossier (jumeau réel contre PMM : facteur ~90 à exactitude comparable ; ici,
facteur 1,16 à exactitude RIGOUREUSEMENT identique). **Verdict : mixte, tel que prévu par
la règle pour ce cas** — la structure des erreurs a un effet réel mais faible (~16 %), pas
nul, pas dominant.

**Résultat le plus important, non anticipé par la règle de décision** : les quatre
conditions (a)-(d), à exactitude 0,590, fuient TOUTES davantage (27,7 à 32,1 %) que le
jumeau réel à la même exactitude (20,7 %). Un témoin construit en recopiant la vérité sur
un sous-ensemble d'items — choisi au hasard, ou par n'importe laquelle des trois règles
structurées testées — **dépasse déjà** la fuite du jumeau LLM réel. Le jumeau réel
n'exploite donc PAS la structure la plus favorable à la fuite qui soit compatible avec son
exactitude : sa fuite mesurée est, si quoi que ce soit, un MINORANT de ce qu'une exactitude
de 0,59 permettrait, pas un signe d'individualisation allant au-delà de l'exactitude.

## 6. Ma prédiction préenregistrée était-elle réfutée ? Oui, sur l'essentiel.

Prédit (section 3 du préenregistrement) : top-1(b) le plus haut (rare = distinctif),
top-1(c) le plus bas, proche de PMM/B2 (0,05-1 %). **Observé : c'est l'inverse — (b) est
le PLUS BAS des quatre (27,7 %), (c) est proche du haut (31,6 %), et aucun des deux n'est
proche de PMM/B2.** Raison, identifiable après coup et déjà présente dans ce dépôt avant
ce script (`c7-bits-resultats.md`, section « avenant ») : l'entropie brute d'un item
n'est PAS un proxy fiable de son pouvoir d'identification sur Twin — le signe est
INVERSÉ (r = −0,81) : les items d'achat (basse entropie, ~0,99 bit) portent l'essentiel
du pouvoir d'identification (δ médian 0,209), les items d'opinion (haute entropie, ~2,1
bits) n'en portent presque pas (δ médian 0,029). En classant « rare » par entropie
brute, (b) a préférentiellement gardé exacts les items d'opinion (peu identifiants) et
mis faux les items d'achat (très identifiants) — l'exact opposé de l'effet recherché.
Cette erreur de préenregistrement (utiliser l'entropie plutôt que l'information mutuelle
conditionnelle comme proxy de rareté « utile ») était évitable : le fichier qui la
contredit avait déjà été lu avant d'écrire la prédiction. Elle est rapportée ici telle
quelle, sans être maquillée. La prédiction sur (a) vs (d) (proches, IC recouvrants) est,
elle, confirmée : 31,9 % contre 32,1 %, aucun effet détectable d'un ordre partagé entre
personnes tant qu'il n'est pas corrélé à un contenu identifiant.

## 7. Ce que l'article peut désormais écrire, et ce qu'il doit cesser d'écrire

**À écrire** : « à exactitude par personne strictement égale (identique au bit près,
pas seulement en espérance), la fuite varie peu selon la structure des erreurs — de 27,7 %
à 32,1 % de top-1 sur quatre témoins synthétiques construits pour isoler cette question —
et ce que nous mesurons chez le jumeau LLM réel (20,7 %) reste EN DESSOUS de ce qu'un
simple hasard calé sur la même exactitude produit déjà. L'exactitude par personne, une
fois qu'elle inclut nécessairement de recopier la vérité sur les items devinés justes,
suffit à elle seule à produire une fuite du même ordre de grandeur — voire supérieure — à
celle du jumeau réel. » Corollaire pour la section A1/O1 de `article-synthese.md` (à
réviser par qui en a la charge, pas par ce script) : ce résultat AJOUTE au verdict déjà
écrit après le nul de marge de `c7-disjoint-resultats.md` (« le couplage ne démontre
aucune spécificité individuelle ») un second témoin, plus strict (exactitude appariée au
bit près et non plus en espérance), qui pointe dans le MÊME sens défavorable.

**À cesser d'écrire** : toute affirmation selon laquelle le jumeau LLM « fuit plus qu'un
simple effet d'exactitude ne le laisserait attendre » — c'est l'inverse qui est mesuré
ici. Également à ne plus écrire : « les items rares sont ce qui identifie » sans la
réserve du sens inversé sur Twin (c'est l'information CONDITIONNELLE au contexte, pas
l'entropie brute, qui identifie — déjà établi par `c7-bits-resultats.md`, confirmé ici par
une expérience causale et non plus seulement corrélationnelle).

**Ce qui reste vrai et non touché par ce script** : l'écart à PMM/B2 (prédicteurs réels
qui n'ont jamais accès à `y_ref` de la personne sur l'item cible, seulement au contexte)
reste énorme — 0,07-0,3 % contre les 27,7-32,1 % des témoins appariés ici, et contre 20,7 %
pour le jumeau réel — deux à trois ordres de grandeur. Ce contraste-là, entre lire ou non
la vérité de la cible, reste le plus solide de tout le dossier C7 ; ce que ce script
retire, c'est l'idée que le jumeau LLM ferait, à exactitude égale et à lecture de cible
égale, mieux qu'un simple hasard.
