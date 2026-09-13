# C7, équité du risque : la moyenne cache une minorité identifiée à coup sûr (13 septembre 2026) — UNE AFFIRMATION AMENDÉE le 13 septembre 2026

statut: provisoire
amende_par: resultats/audit-predictibilite-2026-09-13.md
fait_foi: resultats/audit-predictibilite-2026-09-13.md
mandat: Mesurer si le risque de ré-identification est réparti uniformément entre les personnes ou concentré sur une minorité, caractériser les plus exposés, et déterminer si la défense D4 (mélange intra-segment) réduit l'inégalité ou seulement le taux moyen. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_equite_risque.py, resultats/c7-equite-risque-preenregistrement.md, resultats/c7-equite-risque-resultats.md, resultats/c7-equite-risque.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_defense.py, analyses/c7_controle_interpretabilite.py, analyses/c7_stanford.py
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, réimplémentation de l'attaque, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00

Préenregistré dans `resultats/c7-equite-risque-preenregistrement.md`, écrit **avant** le
premier calcul. Script `analyses/c7_equite_risque.py`, données `c7-equite-risque.csv`.
Durée totale 69 s, aucune réduction de calcul n'a été nécessaire. Aucun identifiant,
aucune réponse, aucun segment nommé, aucun groupe de moins de 20 personnes.

**Contrôle d'interprétabilité passé avant toute lecture** (`controle_avant_interpretation`,
bassin exactement attaqué, baseline recalculée dessus) : `JSON Persona - GPT4.1`,
top-1 **20,69 % [19,00 ; 22,40]** contre baseline Demographics Only **2,15 %
[1,59 ; 2,79]** sur les 2 058 personnes. Le jumeau porte bien une personne ; ce qui suit
est interprétable.

---

## 0 bis. Une affirmation de ce rapport est AMENDÉE — et elle n'est PAS retirée

Rien n'est effacé. Une seule des affirmations de ce rapport change de statut, et il faut
dire exactement laquelle, parce que la nuance a déjà été déformée une fois dans le sens
du retrait.

**État : AMENDÉ — « affaiblie et renommée », pas retirée.** Fait foi :
`resultats/audit-predictibilite-2026-09-13.md`, §1 et §7, dont le verdict est mot pour
mot : « l'affirmation ne doit pas être retirée, elle doit être affaiblie et renommée ».

**Ce qui est interdit :** la phrase **« la fuite suit la prédictibilité, non la rareté »**
(§3 et §7 ci-dessous). L'audit établit qu'elle **oppose deux choses qui ne sont pas
opposables** : sous un modèle de population, « prédictible » et « typique » sont la même
variable (ρ = −0,702 entre prédictibilité hors pli et rareté moyenne,
`c7-audit-predictibilite.csv`). L'opposition est mal posée, donc la phrase doit
disparaître.

**Ce qui TIENT, et qui a résisté au test le plus dangereux — la moitié « rareté ».** Le
signe négatif de la corrélation risque ↔ atypicité survit :

- à une autre définition de la rareté (ρ = −0,213 avec la rareté moyenne `−log q_j`,
  `c7-audit-predictibilite.csv`) ;
- **au changement d'attaquant pour A-LLR pondéré par la rareté**, c'est-à-dire à
  l'attaquant construit pour exploiter la rareté : ρ = −0,185 [−0,228 ; −0,138] sur
  l'atypicité, et **plus fort encore** sur la rareté moyenne, −0,237 [−0,275 ; −0,198].
  La prédiction P6 de l'auditeur, qui annonçait l'inversion du signe, est **réfutée**.

Autrement dit : le contre-intuitif tient — les plus exposés ne sont pas les plus
atypiques — et c'est la seconde moitié, celle qui revendiquait la « prédictibilité »
contre la « rareté », qui tombe. Toute note qui présenterait cette affirmation comme
*retirée* est fausse et doit être corrigée vers ce paragraphe.

**La formulation de remplacement** est celle du §8 de l'audit, à reprendre in extenso.

**Le reste de ce rapport n'est pas touché** : la forme quasi binaire du risque, la
concentration, le Gini, l'effet de D4 et la réplication sur Park sont hors du périmètre
de cet audit.

---

## 0. La mesure, et le piège du bassin

Le top-1 est binaire par personne : il n'a pas de déciles. Et il dépend mécaniquement de
la taille du bassin (2,13 % à 2 058, 13,29 % à 120 pour la même baseline). Comparer des
sous-groupes de tailles différentes par leur top-1 intra-groupe mesurerait la taille du
groupe, pas l'exposition.

La mesure retenue, préenregistrée §2, est le **risque individuel à bassin constant**
`p_i(B) = C(M − c_i, B − 1) / C(M, B − 1)` — la probabilité que la personne `i` soit
classée première dans un bassin tiré au hasard de taille `B` qui la contient, où
`c_i = R_i − 1` est le nombre d'imposteurs qui la battent dans l'attaque inchangée
(`c7_reidentification.rangs_attaque`). C'est une **transformation déterministe et monotone
du rang**, pas une nouvelle attaque : elle est continue, elle est définie au **même `B`
pour tout le monde**, et elle vaut le top-1 quand `B = N`.

**Limite déclarée.** `c_i` est réel (rang moyen sur les 20 tirages de départage d'ex
aequo), donc la transformation interpole entre deux entiers là où l'attaque produit des
ex aequo. Contrôle de cohérence : `p_i(B = N)` moyen = **18,40 %** contre top-1 observé
**20,68 %**. L'écart de 2,3 points est ce lissage ; il **sous-estime** le risque, il ne le
gonfle pas. Toutes les conclusions de concentration ci-dessous sont donc conservatrices.

## 1. La forme : le risque n'est pas réparti, il est binaire

Au bassin publié (`B = N = 2 058`, `JSON Persona - GPT4.1` contre les humains vague 4) :

| | risque individuel |
|---|---|
| moyenne | 18,4 % (top-1 publié 20,7 %) |
| **médiane** | **0,0 %** |
| décile 1 à 5 | 0,0 % |
| décile 9 | 84,6 % |
| **décile 10** | **100,0 %** |
| personnes sous 1 % de risque | **79,8 %** |
| personnes au-dessus de 90 % de risque | **18,3 %** |

**La moyenne de 20,7 % ne décrit personne.** Elle est la moyenne d'une distribution
quasi binaire : environ une personne sur cinq est retrouvée avec une quasi-certitude, et
quatre sur cinq ne le sont essentiellement jamais. La moitié de l'échantillon a un risque
exactement nul ; le décile le plus exposé a un risque de 1,00.

À bassin réduit, la même asymétrie persiste : à `B = 100`, moyenne 45,4 %, médiane 38,5 %,
31,9 % des personnes sous 1 % et 46,8 % au-dessus de 50 %. À `B = 1 000` : moyenne 24,8 %,
médiane 0,0 %.

## 2. La concentration, chiffrée

| bassin | Gini du risque | part du décile le plus exposé | part du centile le plus exposé |
|---|---|---|---|
| `B = 100` | **0,516 [0,498 ; 0,535]** | **22,0 % [21,2 ; 23,0]** | 2,2 % |
| `B = 1 000` | 0,739 [0,722 ; 0,756] | 40,4 % [38,0 ; 43,2] | 4,1 % |
| **`B = N = 2 058`** | **0,816 [0,799 ; 0,832]** | **54,4 % [49,6 ; 60,3]** | 5,5 % |

*(IC 95 % par bootstrap sur les personnes, 1 000 tirages, la statistique d'inégalité étant
**ré-estimée dans chaque tirage** — poser un IC autour d'un Gini déjà calculé n'aurait pas
de sens. Graine 20260911.)*

Au bassin publié, **les 10 % les plus exposés portent 54 % de toutes les identifications
réussies**, et les 1 % les plus exposés en portent 5,5 %.

**Validation non circulaire (P3).** Le classement par risque est estimé contre les humains
**vague 4** ; le succès est ensuite compté contre une **cible différente**, les humains
**vagues 1-3 (retest)**. Le décile le plus exposé selon v4 capte **25,1 %
[22,1 ; 28,7]** des top-1 réussis contre v1-3 (uniformité = 10 %), et le quartile le plus
exposé en capte **58,4 %**. La concentration n'est donc pas un artefact de la statistique
qui la définit : l'exposition est une propriété stable de la personne, qui se transporte
d'une vague de mesure à l'autre.

**Comparateur.** La baseline Demographics Only est encore plus concentrée (Gini 0,842,
part du décile 68,5 % à `B = 100`) pour un risque moyen six fois plus faible. Le jumeau LLM
ne fait donc pas que déplacer le risque : il **élargit** la population exposée tout en
gardant une forte concentration.

## 3. Qui sont les plus exposés — et ma prédiction est réfutée dans sa direction

Corrélations de Spearman entre le risque individuel `p_i(100)` et des caractéristiques
observables, IC 95 % par bootstrap sur les personnes :

| caractéristique | ρ | IC 95 % |
|---|---|---|
| **cohérence interne test-retest** (accord v4 / v1-3 de la personne) | **+0,256** | [+0,213 ; +0,293] |
| **atypicité des réponses** (distance au mode de la population) | **−0,181** | [−0,225 ; −0,135] |
| atypicité du **jumeau** (distance au mode des jumeaux) | +0,146 | [+0,099 ; +0,191] |
| nombre de réponses non manquantes (108 items) | +0,033 | [−0,008 ; +0,075] (traverse 0) |

**Le préenregistrement P4 prédisait ρ ≥ +0,20 avec l'atypicité. Le signe observé est
négatif, et l'IC exclut zéro : la prédiction est réfutée, et réfutée dans sa direction.**
Réplication indépendante sur l'archive Park et al. : **ρ = −0,154 [−0,211 ; −0,094]**,
même signe, même ordre de grandeur.

Ce ne sont donc **pas** les réponses atypiques qui exposent. Le corrélat dominant est la
**cohérence interne** : les personnes les plus exposées sont celles qui se répondent à
elles-mêmes de la même façon d'une vague à l'autre, et dont les réponses sont plutôt
**proches** du mode. L'attaque ne réussit pas parce que la personne est singulière, mais
parce que le jumeau la **prédit bien** — et un modèle de langage prédit mieux les
personnes stables et centrales que les personnes erratiques ou marginales. La fuite suit
la prédictibilité, pas la rareté.

**Prudence, et ce qu'il ne faut pas en conclure.** Ce résultat est le contraire de
l'intuition de la k-anonymité (où l'atypique est le vulnérable) parce que le mécanisme
est différent : ici l'attaquant ne cherche pas une combinaison rare dans une table, il
compare une **prédiction** à une personne. Il ne dit pas que les personnes atypiques sont
protégées dans l'absolu — seulement que ce jumeau-ci ne les retrouve pas. Un attaquant
équipé d'un meilleur générateur pourrait renverser le signe.

**Segments démographiques**, à bassin constant `B = 100`, niveaux de moins de 20 personnes
écartés, niveaux **jamais nommés** (ordre d'exposition seulement) :

| axe | niveaux retenus | rapport max / min du risque moyen |
|---|---|---|
| ethnicité | 5 | 1,36 |
| idéologie politique | 5 | 1,23 |
| âge | 4 | 1,18 |
| éducation | 5 | 1,10 |
| genre | 2 | 1,08 |

Les écarts démographiques sont **faibles** — au plus 1,36 entre le niveau le plus et le
moins exposé — face à un rapport de **plus de 4** entre le décile supérieur et le décile
médian et de l'infini entre décile 10 et médiane au bassin complet. **L'inégalité
d'exposition est massivement intra-groupe, pas inter-groupe.** Et une corrélation avec un
segment ne dirait pas que ce segment est visé : elle dirait que ses réponses sont plus
prédictibles dans ce jeu, ce qui peut tenir à sa taille dans l'échantillon, au contenu du
questionnaire ou au recrutement. Aucune formulation causale n'est écrite ici.

## 4. La défense : elle divise, elle n'égalise pas — et elle déplace

D4 = permutation des réponses entre personnes du même segment `S_gra`, item par item,
appliquée aux 40 items d'achat seulement, attaque toujours sur les 60 items
(`c7_defense.defense_d4`, mêmes graines).

| | avant D4 | après D4 |
|---|---|---|
| risque moyen, `B = 100` | 45,4 % | **2,2 %** |
| risque moyen, `B = N` | 18,4 % | **0,098 %** |
| personnes sous 1 % de risque (`B = N`) | 79,8 % | **99,85 %** |
| **rapport décile le plus exposé (avant) / 90 % restants** | **2,54** | **2,59** |
| réduction relative du risque, décile le plus exposé | — | **95,05 %** |
| réduction relative du risque, 90 % restants | — | **95,14 %** |

**Le test décisif préenregistré (§5) tombe entre les deux seuils.** Le rapport
exposés / reste passe de 2,54 à 2,59 : il ne monte pas au-dessus de 3 (D4 n'abandonne
donc **pas** les plus vulnérables), mais il ne descend pas sous 1,5 (D4 n'**égalise** pas
non plus). La réduction est **proportionnelle et quasi identique** pour les deux groupes
(95,05 % contre 95,14 %). D4 divise le risque de tout le monde par vingt en laissant
la structure d'inégalité intacte.

**Le Gini monte de 0,516 à 0,958, et ce chiffre ne doit pas être lu comme une aggravation.**
Il est en grande partie mécanique : un Gini calculé sur une distribution écrasée vers zéro
monte même quand la réduction est strictement proportionnelle. C'est pourquoi le
préenregistrement avait désigné le rapport exposés / reste, et non le Gini, comme test
décisif. La prédiction P5 (« le Gini ne baisse pas de plus de 0,10 ») est donc
techniquement vérifiée, mais pour une raison que je n'avais pas anticipée.

**Ce que la défense fait vraiment : elle déplace.** Le recouvrement entre le décile le
plus exposé **avant** D4 et le décile le plus exposé **après** D4 est de **22,8 %**
(hasard = 10 %). Plus des trois quarts des personnes qui portent le risque résiduel
n'étaient pas les plus exposées avant la défense. D4 ne protège donc pas spécifiquement
ceux qui étaient menacés : elle rebat les cartes en abaissant le niveau général. Le risque
résiduel reste extrêmement concentré (99,7 % dans un seul décile à `B = 100`), et une
fraction de l'ordre de 0,1 % des personnes reste au-dessus de 90 % de risque au bassin
complet malgré la défense.

## 5. Réplication sur Park et al. — et un renversement de forme

| | Twin-2K-500 (`B = N`) | Park et al. GSS (`B = N = 1 052`) |
|---|---|---|
| top-1 | 20,7 % | 65,6 % |
| Gini du risque | **0,816** | **0,360** |
| part du décile le plus exposé | 54,4 % | 15,6 % |
| personnes au-dessus de 90 % de risque | 18,3 % | 63,9 % |
| ρ(risque, atypicité) | −0,181 | −0,154 |

**Le régime n'est pas le même.** Sur Twin le risque est **concentré** : peu de gens, très
exposés. Sur Park il est **généralisé** : à `B = 100`, le Gini tombe à **0,135** et la part
du décile supérieur à **11,7 %** — c'est-à-dire que **le critère préenregistré
d'uniformité est satisfait sur Park**, non parce que le risque y est faible mais parce
qu'il y est presque universellement élevé (88,5 % des personnes au-dessus de 50 % de
risque). Il n'y a pas de minorité exposée sur Park : il y a une majorité exposée.

La direction du corrélat d'atypicité, elle, réplique : dans les deux jeux, les plus
exposés sont les plus proches du mode, pas les plus singuliers.

## 6. Verdict contre le préenregistrement

| prédiction | résultat |
|---|---|
| **P1** forme asymétrique, médiane < moyenne | **confirmée** (médiane 0,0 % vs moyenne 18,4 % à `B = N`) ; le rapport D10/D5 ≥ 10 est vérifié à `B = N` (infini) mais **pas** à `B = 100` (4,4) |
| **P2** Gini ≥ 0,50 et décile supérieur ≥ 35 % | **à moitié** : Gini 0,516 ✓ à `B = 100`, mais part du décile 22,0 % ✗ (le seuil n'est atteint qu'à `B ≥ 1 000`) |
| **P3** décile v4 capte ≥ 25 % des top-1 v1-3 | **confirmée** de justesse : 25,1 % [22,1 ; 28,7] |
| **P4** ρ(atypicité) ≥ +0,20 | **RÉFUTÉE, signe inversé** : −0,181 [−0,225 ; −0,135], répliqué sur Park |
| **P5** D4 ne réduit pas l'inégalité | **confirmée**, mais par un mécanisme non prévu (réduction proportionnelle + déplacement des exposés) |
| **critère d'uniformité** (Gini < 0,20 et part ∈ [10 ; 16] %) | **non atteint sur Twin** (0,516 / 22,0 %) ; **atteint sur Park à `B = 100`** (0,135 / 11,7 %) |

La question d'équité ne tombe pas sur Twin. Elle tombe sur Park, pour la raison inverse de
celle envisagée.

## 7. La phrase que l'article peut écrire

> Le taux moyen de ré-identification décrit mal le risque individuel : sur Twin-2K-500,
> la médiane du risque est nulle, 79,8 % des personnes ont moins de 1 % de chance d'être
> retrouvées et 18,3 % en ont plus de 90 %, les 10 % les plus exposés concentrant 54 % des
> identifications réussies (Gini 0,816 [0,799 ; 0,832]) — une concentration qui se
> transporte à une vague de mesure différente (25,1 % [22,1 ; 28,7] des succès contre le
> retest, pour 10 % attendus sous uniformité). Contre l'intuition de la k-anonymité, les
> plus exposés ne sont pas les plus atypiques : le risque décroît avec la distance au mode
> (ρ = −0,181 [−0,225 ; −0,135] sur Twin, −0,154 [−0,211 ; −0,094] sur Park) et croît avec
> la cohérence interne test-retest (ρ = +0,256 [+0,213 ; +0,293]) ; la fuite suit la
> prédictibilité, non la rareté, et les écarts entre segments démographiques (rapport
> max/min ≤ 1,36 à bassin constant) sont d'un ordre de grandeur inférieurs à l'inégalité
> intra-groupe. Le mélange intra-segment divise le risque de chacun par vingt sans
> modifier cette structure (rapport exposés / reste 2,54 → 2,59) et déplace la population
> résiduellement exposée plutôt qu'il ne la protège (recouvrement des déciles les plus
> exposés avant / après : 22,8 %).

## 8. Ce que ce travail ne montre pas

1. **Un seul attaquant.** Tout est mesuré avec l'attaque naïve par accord de Hamming de
   `c7_reidentification`. L'attaquant fort (A-LLR) change les taux de 20,7 % à 23,2 % sur
   Twin et de 65,5 % à 90,4 % sur Park ; il pourrait changer aussi **qui** est exposé, et
   donc le signe du corrélat d'atypicité. Non mesuré ici.
2. **Monde fermé.** Les chiffres publiés en monde ouvert (60,17 % TPR à 1 % de fausses
   accusations sur Park) reposent sur un régime de décision différent ; la distribution du
   risque en monde ouvert n'est pas mesurée ici.
3. **La causalité.** Les corrélats sont des associations sur deux jeux. Rien n'établit que
   rendre une personne moins cohérente la protégerait.
4. **Une seule défense.** D4 seulement ; D1, D2, D3 ne sont pas décomposées par décile.
