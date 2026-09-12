# C7 monde ouvert, intervalles de confiance : le 60,17 % (attaquant fort A-LLR)

Calculé par `analyses/c7_fort_monde_ouvert_ic.py`, qui importe `analyses/c7_attaquant_fort.py`,
`analyses/c7_monde_ouvert.py` et `analyses/c7_reidentification.py` **tels quels** (aucune
modification, aucune ligne recopiée). Données : `resultats/c7-fort-monde-ouvert-ic.csv`. Aucun
identifiant ni appariement individuel imprimé ou écrit.

## 0. Préenregistrement (écrit avant tout calcul de bootstrap, repris du script)

**Défaut visé.** A3 cite comme chiffre de tête, en monde ouvert à FPR = 1 %, **60,17 %** sur
l'archive Park (et **4,28 %** sur Twin ; **44,37 %** / **1,01 %** à FPR = 0,1 %). Ces quatre
chiffres viennent de l'attaquant **fort** A-LLR, paramètres estimés **hors pli** en 5 plis
(`c7_attaquant_fort.py`, fonction `scores_hors_pli`). Ils sont publiés sans IC.
`resultats/c7-monde-ouvert-ic-2026-09-12.md` a déjà traité l'IC de l'attaque **naïve** pour les
mêmes FPR ; ce script ne refait pas ce travail, il relit son CSV pour la comparaison du point 4.

**Attente 1 (largeur).** Mêmes ordres de grandeur qu'en naïf : large sur Twin (TPR bas, seuil
calé sur une poignée de personnes), plus étroit en relatif sur Park à FPR = 1 % (TPR déjà haut,
60 %, donc davantage de faux positifs absolus derrière le seuil qu'à 20 %).

**Attente 2 (rejeu du seuil).** Identique au rapport naïf : le seuil est choisi *a posteriori* sur
le même échantillon ; un IC à seuil fixe serait trop étroit, surtout à FPR = 0,1 %.

**Attente 3 (le piège propre à l'attaquant fort — point central de ce script).** Les paramètres
a_j (fiabilité du jumeau par item) et q_j (rareté des modalités) sont estimés **hors pli**, sur 4
plis sur 5, avant d'attaquer le 5e. Un bootstrap qui se contente de rééchantillonner les lignes
d'une matrice de score **déjà calculée** traite a_j, q_j comme connus et fixes : il ne capture que
la variabilité de « qui dépasse le seuil », pas celle de l'estimation des paramètres eux-mêmes —
c'est optimiste. Attente : un bootstrap qui **ré-estime** a_j, q_j à chaque tirage (en respectant
la structure en plis) donne un IC au moins aussi large, probablement plus large.

**Piège explicite à éviter.** Si l'on rééchantillonne les personnes attaquées avec remise puis
qu'on relance une répartition en plis **naïve** (permutation de 0..n-1 sur l'échantillon
bootstrap), une même personne originale dupliquée peut atterrir à la fois dans un pli
d'entraînement (sa vraie réponse alimente a_j/q_j) et dans le pli de test (sa copie est attaquée) :
fuite de la personne sur elle-même, qui gonflerait son propre score dans ce tirage. Parade
retenue : l'appartenance aux 5 plis est assignée par **identité originale** (l'indice de la
personne avant rééchantillonnage) — toutes les copies d'une même personne, dans un tirage donné,
vont nécessairement dans le même pli.

## 1. Méthode : deux bootstraps rapportés côte à côte

**(A) « Paramètres figés ».** La matrice de score A-LLR hors pli est calculée **une fois**,
exactement comme dans `c7_attaquant_fort.py` (mêmes étiquettes de graine `"twin|llr"` /
`"stan|llr"`, mêmes fonctions importées telles quelles — sanity check : le script retrouve
60,17 % / 44,37 % / 4,28 % / 1,01 % à la décimale près en relisant cette matrice avant tout
bootstrap). Le bootstrap rééchantillonne ensuite seulement les **lignes** (personnes attaquées) de
cette matrice figée, avec remise ; le pool de candidats n'est **pas** rééchantillonné (même
raison qu'en naïf). Le seuil est **rejoué** à chaque tirage (`marges_deux_regimes` et
`roc_et_taux`, importées sans modification). **2000 tirages**, graine fixée. **Cet IC est
optimiste** (voir attente 3) : il ne couvre pas l'incertitude d'estimation de a_j, q_j.

**(B) « Paramètres ré-estimés, plis bloqués par identité ».** À chaque tirage, les personnes
attaquées sont rééchantillonnées avec remise (mêmes tirages que (A)) ; les 5 plis sont assignés
par identité originale (voir piège ci-dessus) ; pour chaque pli, `parametres` et `score_llr`
(importées de `c7_attaquant_fort.py` **sans modification**) sont rappelées sur les positions
d'entraînement du tirage, et notent le pli de test contre le pool complet, non rééchantillonné. Le
seuil est rejoué comme en (A). **C'est le bootstrap qui respecte honnêtement la structure hors
pli.**

**Déviation documentée (réduction du nombre de tirages, comme demandé).** Chaque tirage de (B)
rappelle l'estimation complète des paramètres et le score de vraisemblance sur tout le pool :
mesuré en amont à environ 0,45–0,5 s par tirage. (A) garde ses **2000 tirages** (rapide : 60,1 s
Twin, 17,0 s Stanford, car aucune ré-estimation). Pour (B) seul, le nombre de tirages est réduit
de 2000 à **300** — c'est le nombre réellement utilisé, imprimé dans les logs et écrit dans le CSV
(colonne `n_boot_reestime`) ; temps mesuré : 205,1 s (Twin) et 187,8 s (Stanford). Calcul total du
script : 7 min 57 s, entièrement en avant-plan, aucune tâche laissée en arrière-plan.

## 2. Résultats

IC à 95 %, percentile. « FP absolus » = nombre attendu de faux positifs (personnes) qui
définissent le seuil à ce FPR sur l'échantillon observé (= FPR cible × n).

| jeu | prédicteur (A-LLR hors pli) | n | TPR@FPR=1 % | FP abs. @1 % | IC (A) figé | IC (B) ré-estimé | TPR@FPR=0,1 % | FP abs. @0,1 % | IC (A) figé | IC (B) ré-estimé |
|---|---|---|---|---|---|---|---|---|---|---|
| Twin | Meilleur jumeau (JSON Persona GPT4.1) | 2058 | **4,28 %** | **≈21** | [3,35 ; 5,39] | [3,29 ; 5,64] | **1,01 %** | **≈2** | [0,00 ; 2,67] | [0,05 ; 2,82] |
| Park (Stanford GSS) | Meilleur agent (composite) | 1052 | **60,17 %** | **≈11** | [54,02 ; 64,26] | [54,52 ; 64,41] | **44,37 %** | **≈1** | [24,40 ; 53,72] | [23,34 ; 53,76] |

Top-1 monde fermé (même bootstrap, pour référence) : Twin 23,23 % [(A) 21,5 ; 25,1] [(B) 21,0 ;
25,0] ; Park 90,40 % [(A) 88,5 ; 92,1] [(B) 88,4 ; 92,0].

**Le piège a-t-il changé le résultat ?** Modestement, et dans le sens attendu (élargissement),
mais pas de façon spectaculaire : à FPR = 1 %, la largeur passe de 2,04 pt (A) à 2,35 pt (B) sur
Twin, et de 10,24 pt (A) à 9,89 pt (B) sur Park (ici quasi identique, légèrement plus étroit — le
bruit de rééchantillonnage domine). À FPR = 0,1 %, où le seuil est le plus instable, l'effet est
plus net : 2,67 pt (A) → 2,77 pt (B) sur Twin, et 29,31 pt (A) → 30,43 pt (B) sur Park. Conclusion
honnête : l'incertitude de ré-estimation des paramètres A-LLR existe et va dans le sens prédit,
mais sur ces deux jeux elle est **secondaire** face à l'instabilité déjà énorme du seuil à FPR
rare — elle n'aurait pas suffi, à elle seule, à faire une différence qualitative. **L'IC (B) est
celui à citer** ; (A) est rapporté pour montrer que l'écart entre les deux méthodes reste faible
ici (contrairement à l'écart seuil-rejoué/seuil-fixe, qui lui était le facteur dominant, cf.
rapport naïf).

## 3. Faux positifs absolus : la même fragilité qu'en naïf à FPR = 0,1 %

À FPR = 0,1 %, le seuil repose sur **≈ 2 personnes sur 2 058** (Twin) et **≈ 1 personne sur 1 052**
(Park) — **sous la barre de 10** fixée par la mission dans les deux cas. Le TPR à 0,1 % ne doit
pas être cité comme un point ponctuel fiable : Twin 1,01 % [0,05 ; 2,82] (facteur ~56 entre bornes
non nulles, borne basse quasi nulle), Park 44,37 % [23,34 ; 53,76] (facteur ~2,3, un intervalle de
30 points). À FPR = 1 %, le nombre de faux positifs (~21 Twin, ~11 Park) reste modeste mais plus
grand : les IC sont plus resserrés sans être étroits (Park : 54,5–64,4 points, soit ±5 points
autour de 60,17 %).

## 4. L'attaquant fort bat-il l'attaque naïve, une fois les IC posés ?

| jeu | FPR | naïf (IC) | fort (IC, (B) ré-estimé) | chevauchement ? |
|---|---|---|---|---|
| Twin | 1 % | 3,04 % [2,01 ; 3,99] | 4,28 % [3,29 ; 5,64] | **oui** (zone commune ≈ 3,29–3,99) |
| Twin | 0,1 % | 0,93 % [0,23 ; 1,56] | 1,01 % [0,05 ; 2,82] | **oui**, largement (le naïf est presque inclus dans le fort) |
| Park | 1 % | 20,39 % [15,67 ; 24,49] | 60,17 % [54,52 ; 64,41] | **non** — écart net de plus de 30 points, aucun recouvrement |
| Park | 0,1 % | 8,47 % [2,45 ; 16,20] | 44,37 % [23,34 ; 53,76] | **non** — écart net, aucun recouvrement (borne basse fort 23,3 % > borne haute naïf 16,2 %) |

**Conclusion à écrire sans arrondir les angles.** Sur **Park**, le renforcement de l'attaque est un
gain réel et statistiquement net aux deux FPR : les IC ne se chevauchent pas, l'écart de plusieurs
dizaines de points survit à l'incertitude d'échantillonnage et à celle de la ré-estimation des
paramètres. Sur **Twin**, en revanche, **le gain apparent (3,04 %→4,28 % à 1 %, 0,93 %→1,01 % à
0,1 %) ne survit PAS aux IC** : les intervalles se chevauchent largement aux deux FPR. On ne peut
donc pas affirmer, avec les données actuelles, que l'attaquant fort identifie mieux que l'attaque
naïve sur Twin à ces FPR précis — seul le point estimé est plus haut, ce qui est cohérent avec ce
que dit déjà `article-synthese.md` (« sur Twin, l'écart est faible »), mais « faible » doit
désormais se lire comme **statistiquement indiscernable à FPR fixé**, pas seulement comme un petit
écart numérique. Le gain qualitatif majeur de l'attaquant fort décrit par ailleurs (top-1 monde
fermé, 65,51 %→90,40 % sur Park) reste, lui, hors du périmètre de ce calcul (ce n'est pas un TPR à
FPR fixé) et n'est pas remis en cause ici.

## 5. Ce que le manuscrit ne doit pas faire

Ne pas citer 60,17 % ou 44,37 % (ni 4,28 %, ni 1,01 %) sans IC. Ne pas dire que l'attaquant fort
« améliore » le taux de ré-identification en monde ouvert **sur Twin** aux FPR testés sans
préciser que l'écart avec l'attaque naïve n'est pas significatif à ces FPR (IC chevauchants). Ne
pas citer le TPR à FPR = 0,1 % (sur l'un ou l'autre jeu) sans mentionner qu'il repose sur environ 1
à 2 faux positifs absolus.

## 6. Formulation exacte à écrire dans le manuscrit

> En monde ouvert, à un taux de fausses accusations de 1 %, l'attaquant fort (vraisemblance
> pondérée par la rareté, A-LLR, paramètres estimés hors échantillon en 5 plis) retrouve la bonne
> personne **60,17 % [IC 95 % 54,5 ; 64,4]** du temps sur l'archive Park et **4,28 % [IC 95 % 3,3 ;
> 5,6]** sur Twin-2K-500, sous un bootstrap sur les personnes qui ré-estime les paramètres a_j, q_j
> dans chaque tirage en respectant la structure en plis (2000 tirages pour la version à paramètres
> figés, 300 pour la version qui ré-estime — les deux méthodes donnant des IC proches ici). À
> FPR = 0,1 %, ces taux tombent à **44,37 % [IC 95 % 23,3 ; 53,8]** (Park) et **1,01 % [IC 95 % 0,05
> ; 2,82]** (Twin) — des intervalles très larges car ce seuil n'est défini que par environ 1 et 2
> faux positifs absolus respectivement (sur 1 052 et 2 058 personnes) : des chiffres à traiter comme
> des estimations très instables. Comparé à l'attaque naïve par accord de Hamming aux mêmes FPR
> (20,39 % [15,7 ; 24,5] et 8,47 % [2,5 ; 16,2] sur Park ; 3,04 % [2,0 ; 4,0] et 0,93 % [0,2 ; 1,6]
> sur Twin), le renforcement de l'attaque produit un gain net et statistiquement significatif sur
> Park (aucun chevauchement des IC aux deux FPR), mais un gain qui **ne survit pas** aux IC sur
> Twin (chevauchement large aux deux FPR) : le 60,17 % est donc un résultat robuste au
> renforcement de l'attaquant, le gain relatif sur Twin ne l'est pas et ne doit pas être présenté
> comme établi.

## 7. Reproductibilité

`.venv/bin/python analyses/c7_fort_monde_ouvert_ic.py`. Graine dédiée `GRAINE_IC = [20260912,
199]`, distincte de `[20260912, 99]` du script naïf. Aucun fichier existant modifié ; seules les
fonctions `scores_hors_pli`, `parametres`, `score_llr` (de `c7_attaquant_fort.py`),
`marges_deux_regimes`, `roc_et_taux`, `compte_au_moins`, `graine_nom` (de `c7_monde_ouvert.py`) et
`items_communs`, `REF_V4`, `REF_V13` (de `c7_reidentification.py`) sont importées et appelées.
