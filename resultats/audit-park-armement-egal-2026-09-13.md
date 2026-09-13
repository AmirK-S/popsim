# Audit — Park à armement égal : que reste-t-il au jumeau quand le comparateur démographique porte la même arme ?

statut: courant
mandat: Reproduire independamment les 85,17 % et 29,09 % du volet T1a §1g, produire le tableau a armement egal (jumeau et comparateur demographique, attaque naive et A-LLR, monde ferme et monde ouvert, Park et Twin, bassin strictement constant), trancher ce qui reste au jumeau sur Park, tester l'explication par le nombre d'items, et nommer ce que le comparateur demographique exploite reellement.
agent: audit / Park armement egal, 13/09
ecriture: analyses/c7_park_armement_egal.py, resultats/audit-park-armement-egal-2026-09-13.md, resultats/c7-park-armement-egal.csv
lecture_seule: tout le reste du depot
interdits: appel de modele paye, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, toute ecriture dans article/manuscrit.md et resultats/article-synthese.md
cecite: Aucune verification reseau. Les valeurs 85,17 % / 29,09 % / 90,40 % / 60,17 % annoncees par la branche agent/mesures/t1a-complements ne servent qu'a la verification de raccordement ; aucune n'est recopiee dans un calcul.
cout_reel_usd: 0.00

---

> ## AVERTISSEMENT — POST HOC, NON PRÉENREGISTRÉ AU SENS DE C7
>
> Cet audit est déclenché **après** une mesure de révision (T1a §1g), elle-même post-hoc.
> Le §0 ci-dessous fixe prédictions et critères de réfutation **avant le premier calcul**,
> mais pour une question **choisie après coup**. Il ne compte dans aucun dénominateur de
> multiplicité préenregistré et ne peut réfuter aucune prédiction préenregistrée d'origine.

---

## 0. PRÉENREGISTREMENT — écrit et commité avant le premier calcul

### 0.1 Conventions fixées d'avance

**Départage des ex æquo.** Dans ce projet, cette seule convention fait varier un taux d'un
facteur 130. Elle est donc fixée ici, avant tout calcul, et vaut pour **toutes** les
cellules du tableau, cible comme comparateur, naïf comme A-LLR, Park comme Twin :

- **Convention publiée, retenue pour tous les chiffres de tête** : espérance sous départage
  uniforme dans la classe d'ex æquo de tête, `1/|classe|` si la vraie personne est dans la
  classe de tête, 0 sinon. Calcul **exact et déterministe** (tolérance `1e-12`), pas une
  moyenne de tirages.
- **Deux bornes encadrantes publiées à côté, pour chaque cellule** : `en_faveur` (compte
  dès que rien n'est strictement meilleur) et `contre` (compte seulement si la classe de
  tête est un singleton).
- La variante à 20 tirages aléatoires de `rangs_depuis_accord` est calculée **en plus**,
  pour le seul raccordement à la chaîne publiée.

**Bassin.** Un chargement par jeu, un seul, partagé par la cible et par le comparateur :
mêmes personnes attaquées, même pool, mêmes colonnes d'items. Conformité au chargeur
canonique `c7_fort_monde_ouvert_ic` vérifiée par assertion, arrêt si écart.

**Monde ouvert.** Marge top1−top2 en deux régimes, TPR en escalier exact aux FPR cibles
0,1 % et 1 %, valeur `np.interp` publiée à côté. Protocole `c7_monde_ouvert` repris sans
modification.

**Intervalles.** Bootstrap 2 000 sur les **personnes**, graine `20260913` dérivée du nom de
la mesure. Pour les rapports cible/comparateur : bootstrap **apparié** (les mêmes personnes
rééchantillonnées simultanément pour les deux conditions), 2 000 tirages.

**Baseline.** Tout taux sort avec la baseline recalculée dans **exactement** la même
condition (même bassin, mêmes items, même attaque, même convention de départage).

**Contrôle d'interprétabilité** : `analyses/c7_controle_interpretabilite.py`, règle
inchangée — le candidat passe seulement si la borne basse de son IC est **strictement**
supérieure à la borne haute de l'IC du comparateur, les deux sous la **même** attaque et
le **même** bassin. Appliqué avant toute interprétation.

**Aucune donnée individuelle** n'est calculée, imprimée ni écrite : ni identifiant, ni
appariement, ni cellule démographique d'une personne. Seuls des agrégats sortent.

### 0.2 Prédictions et critères de réfutation

| # | Prédiction (avant calcul) | Ce qui la réfute |
|---|---|---|
| **P1** | Je reproduis, indépendamment de `c7_t1a_complements`, le top-1 monde fermé du comparateur démographique armé sur Park à **85,17 % ± 0,50 pt** et son TPR@1 % à **29,09 % ± 1,00 pt**. | Un écart au-delà de ces tolérances. **Si P1 est réfutée, je m'arrête là et le livrable est cette non-reproduction** — je ne conclus rien d'autre. |
| **P2** | À armement égal sur **Park**, en monde fermé, le rapport cible/comparateur est **≤ 1,15×** et les IC à 95 % des deux top-1 **se recouvrent**. | Rapport ≥ 1,30× avec IC disjoints. Alors un écart survit et je le publie avec son intervalle. |
| **P3** | Le top-1 A-LLR du **comparateur démographique** sur Park **croît de façon monotone** avec le nombre d'items retenus (20, 40, 60, 100, 177), à bassin constant, et le rapport cible/comparateur **décroît** sur la même grille. | Courbe plate (étendue < 5 pts entre k=20 et k=177) ou non monotone. Alors l'explication par le nombre d'items est fausse et il faut chercher ailleurs. |
| **P4** | Le comparateur démographique identifie parce que les **cellules démographiques de Park sont quasi uniques** : je prédis que **plus de 30 %** des personnes du pool Park sont **seules** dans leur cellule exacte (genre × race × âge × éducation). | Moins de 10 % de personnes isolées. Alors l'unicité de cellule n'est pas le mécanisme, et il faut l'attribuer à des items fortement déterminés par la démographie. |
| **P5** | Le top-1 armé du comparateur (85 %) **dépasse largement** le plafond que donnerait la seule cellule démographique, `moyenne(1/|cellule|)` — c'est-à-dire que A-LLR extrait plus que l'appartenance de cellule. | Le top-1 armé est **inférieur ou égal** à ce plafond : alors le comparateur ne fait que relire la cellule, et il n'y a rien de plus. |

### 0.3 Règle d'arrêt

Si P1 est réfutée, l'audit s'arrête au §1 et ne produit ni tableau ni interprétation.
**Aucune conclusion en faveur de l'article par défaut** : si le rapport sur Park est
proche de 1 avec IC recouvrants, la phrase du manuscrit sur Park doit être retirée ou
requalifiée, et le rapport le dit explicitement.

---

## 1. P1 — La reproduction est confirmée, au chiffre près

Chemin de mesure réécrit (`analyses/c7_park_armement_egal.py`), sans importer
`c7_t1a_complements`. Les briques canoniques (`c7_stanford`, `c7_attaquant_fort`,
`c7_monde_ouvert`) sont reprises telles quelles ; le chargeur canonique
`c7_fort_monde_ouvert_ic` sert d'**assertion** de conformité du bassin (arrêt si écart —
il n'y en a pas eu).

| valeur | publié T1a §1g | reproduit ici | écart |
|---|---|---|---|
| comparateur démographique, Park, A-LLR, monde fermé | 85,1711 % | **85,1711 %** | 0,0000 pt |
| comparateur démographique, Park, A-LLR, TPR @ 1 % FPR (escalier) | 29,0875 % | **29,0875 %** | 0,0000 pt |
| comparateur démographique, Park, naïf, monde fermé | 2,2433 % | 2,2497 % | 0,0064 pt |
| cible, Park, A-LLR, monde fermé | 90,3992 % | **90,3992 %** | 0,0000 pt |
| cible, Park, A-LLR, TPR @ 1 % FPR | 60,1711 % | **60,1711 %** | 0,0000 pt |
| cible, Twin, A-LLR, monde fermé | 23,2264 % | **23,2264 %** | 0,0000 pt |
| comparateur démographique, Twin, A-LLR, monde fermé | 0,7775 % | **0,7775 %** | 0,0000 pt |

**P1 confirmée.** L'écart de 0,0064 pt sur le comparateur naïf vient du départage exact
des ex æquo (convention 0.1) là où T1a moyennait 20 tirages ; c'est du bruit de
Monte-Carlo, pas un désaccord. L'audit continue.

Le témoin de permutation est reproduit lui aussi : comparateur démographique armé,
**0,0951 %**, soit exactement le hasard (1/1 052). Le signal est une correspondance
personne-à-personne **réelle**, pas un défaut de câblage.

---

## 2. Le tableau à armement égal, sur les deux jeux

Bassin strictement constant (un chargement par jeu, partagé par toutes les conditions),
convention de départage **uniforme exacte** pour les chiffres de tête, TPR **en escalier
exact**, IC 95 % bootstrap sur 2 000 rééchantillonnages de personnes.

### 2.1 Park (archive Park et al., bloc GSS) — 1 052 personnes, 177 items

| condition | attaque | top-1 monde fermé (IC 95 %) | bornes de départage (contre / en faveur) | AUC | TPR @ 1 % FPR | TPR @ 0,1 % FPR |
|---|---|---|---|---|---|---|
| **cible** meilleur agent (composite) | naïve | 65,5973 % [62,70 ; 68,35] | 63,88 / 67,59 | 0,5527 | 20,1521 % | 8,3650 % |
| **cible** meilleur agent (composite) | **A-LLR** | **90,3992 %** [88,59 ; 92,11] | 90,40 / 90,40 | 0,8479 | **60,1711 %** | 50,1901 % |
| **comparateur démographique** | naïve | 2,2497 % [1,42 ; 3,16] | 1,90 / 2,76 | 0,0127 | **0,0000 %** | **0,0000 %** |
| **comparateur démographique** | **A-LLR** | **85,1711 %** [82,89 ; 87,26] | 85,17 / 85,17 | 0,7394 | **29,0875 %** | 17,0152 % |
| PMM k=10 | naïve | 0,5703 % [0,19 ; 1,05] | — | 0,0022 | 0,0000 % | 0,0000 % |
| PMM k=10 | **A-LLR** | 1,0456 % [0,48 ; 1,71] | — | 0,0052 | 0,0000 % | 0,0000 % |

### 2.2 Twin-2K-500 — 2 058 personnes, 60 items

| condition | attaque | top-1 monde fermé (IC 95 %) | bornes de départage | AUC | TPR @ 1 % FPR | TPR @ 0,1 % FPR |
|---|---|---|---|---|---|---|
| **cible** JSON Persona - GPT4.1 | naïve | 20,6940 % [19,11 ; 22,41] | 18,32 / 24,10 | 0,1494 | 2,9640 % | 0,9232 % |
| **cible** JSON Persona - GPT4.1 | **A-LLR** | **23,2264 %** [21,38 ; 25,12] | 23,23 / 23,23 | 0,1769 | **4,2760 %** | 1,2634 % |
| **comparateur démographique** | naïve | 2,1453 % [1,56 ; 2,77] | 1,80 / 2,67 | 0,0128 | 0,1944 % | 0,0972 % |
| **comparateur démographique** | **A-LLR** | **0,7775 %** [0,44 ; 1,17] | 0,78 / 0,78 | 0,0051 | **0,0486 %** (1 personne) | **0,0000 %** |
| PMM k=10 | naïve | 0,0891 % [0,00 ; 0,21] | — | 0,0002 | 0,0000 % | 0,0000 % |
| PMM k=10 | **A-LLR** | 0,2430 % [0,05 ; 0,49] | — | 0,0013 | 0,0000 % | 0,0000 % |

**La convention de départage est déclarée, et elle compte.** Sous A-LLR les scores sont
continus : les trois conventions coïncident au douzième chiffre (aucun ex æquo). Sous
l'attaque **naïve** de Hamming, elles s'écartent : Twin 18,32 % contre 24,10 %, soit un
facteur **1,32×** sur la seule convention ; Park 63,88 % contre 67,59 %. Toute comparaison
naïf → A-LLR faite sans fixer cette convention est donc partiellement un artefact de
convention. Elle est fixée ici, identiquement pour toutes les cellules.

---

## 3. La question qui décide : ce qui reste au jumeau sur Park

| jeu | attaque | rapport cible / comparateur (monde fermé) | IC 95 % apparié | écart en points | contrôle d'interprétabilité |
|---|---|---|---|---|---|
| **Park** | naïve | **29,16×** | [20,67 ; 46,25] | +63,35 pt [+60,52 ; +66,21] | **PASSE** |
| **Park** | **A-LLR** | **1,061×** | **[1,030 ; 1,097]** | **+5,23 pt [+2,66 ; +8,08]** | **PASSE, de justesse** |
| **Twin** | naïve | 9,65× | [7,39 ; 13,43] | +18,55 pt | PASSE |
| **Twin** | **A-LLR** | **29,88×** | [19,37 ; 55,23] | +22,45 pt | PASSE |

Rapport des TPR à 1 % de FPR, à armement égal sous A-LLR : **Park 2,07×** (60,17 % contre
29,09 %), **Twin 88,0×** (4,2760 % contre 0,0486 %).

**Le contrôle d'interprétabilité** (`c7_controle_interpretabilite`, règle inchangée : IC
disjoints, borne basse du candidat strictement au-dessus de la borne haute du
comparateur) **passe sur Park** : 88,59 % contre 87,26 %, **1,33 point de marge**. Le
bootstrap apparié — le test le plus puissant, puisqu'il rééchantillonne les mêmes
personnes des deux côtés — confirme : l'écart de +5,23 pt a un IC qui **exclut zéro**
[+2,66 ; +8,08] et le rapport un IC qui **exclut 1** [1,030 ; 1,097].

**Verdict sur P2 : ma prédiction est à moitié réfutée.** J'avais prédit un rapport
≤ 1,15× **et** des IC recouvrants. Le rapport tient (1,061 ≤ 1,15) ; **les IC ne se
recouvrent pas**. Un écart survit donc sur Park, et il est statistiquement résolu. Mais
il est **de 5,2 points, pas de 88 points** : il ne peut plus porter la phrase actuelle du
manuscrit. Le critère de réfutation que j'avais posé (≥ 1,30× avec IC disjoints) n'est pas
atteint non plus : la démonstration sur Park n'est ni sauvée ni entièrement détruite —
elle est **réduite d'un facteur 27**.

---

## 4. P3 — Pourquoi la baseline monte : confirmé, et plus fort que prévu

Comparateur et cible, sous **A-LLR** et sous l'attaque naïve, en fonction du nombre
d'items retenus. Bassin, pool et personnes attaquées strictement constants ; seules les
colonnes changent. **Réduction déclarée** : 8 tirages d'items par valeur de *k* au lieu des
20 de la convention `c7_stanford.N_TIRAGES_ITEMS`, pour la durée. *k* = 177 est le jeu
entier (un seul « tirage »).

| items | **comparateur armé (A-LLR)** | comparateur naïf | cible armée | cible naïve | rapport cible/comparateur (A-LLR) |
|---|---|---|---|---|---|
| 20 | **3,84 %** | 1,06 % | 19,29 % | 11,07 % | **5,02×** |
| 40 | **16,44 %** | 1,16 % | 48,27 % | 25,03 % | **2,93×** |
| 60 | **22,74 %** | 1,36 % | 53,87 % | 32,17 % | **2,37×** |
| 100 | **61,03 %** | 2,39 % | 79,28 % | 51,38 % | **1,30×** |
| 177 | **85,17 %** | 2,25 % | 90,40 % | 65,60 % | **1,06×** |

**P3 est confirmée, sans réserve.** La baseline armée croît de façon strictement monotone
sur toute la grille, de 3,84 % à 85,17 % — 81 points d'amplitude. Le rapport
cible/comparateur décroît de façon strictement monotone, 5,02× → 1,06×. Et la
décomposition est nette : **c'est l'interaction entre l'armement et le nombre d'items**,
pas l'un ou l'autre. Le comparateur **naïf** ne bouge quasiment pas sur la même grille
(1,06 % → 2,25 %) ; c'est A-LLR qui convertit le nombre d'items en identification, et il
le fait **plus vite pour le comparateur que pour la cible**.

Cela rejoint les trois autres mesures de la nuit : **plus d'items gonflent tout attaquant,
et gonflent le comparateur plus que la cible.** Sur Twin, 60 items ne suffisent pas :
c'est l'unique raison pour laquelle la phrase du manuscrit y survit.

**Une réserve à publier.** L'étendue sur les tirages d'items est énorme : à *k* = 100, le
comparateur armé va de **7,70 % à 91,06 %** selon les items tirés. Le nombre d'items ne
détermine donc le taux qu'en moyenne ; **quels** items sont retenus compte autant. Les
bornes min/max sont dans le CSV (`ic_bas`/`ic_haut` du volet `4 courbe items`) et ne sont
**pas** des intervalles de confiance : le CSV le dit en toutes lettres.

---

## 5. Ce que le comparateur démographique exploite — et c'est le vrai résultat

### 5.1 La cellule à quatre axes n'explique rien (P4 réfutée à la lettre)

Cellule genre × race × âge × éducation, telle que je l'avais préenregistrée et telle que
l'emploie le comparateur PMM du dépôt :

- **146 cellules** pour 1 052 personnes (2×3×7×5 modalités) ;
- **25 personnes (2,38 %)** seules dans leur cellule — j'avais prédit **> 30 %** ;
- taille médiane 15, maximum 46 ; plafond d'une attaque qui ne lirait que la cellule :
  `moyenne(1/|cellule|)` = **13,88 %**.

**P4 est réfutée telle que je l'avais écrite** (2,38 % < 10 %). Et le succès du
comparateur armé **ne dépend pas** de la rareté de la cellule : 92,0 % pour les 25
personnes seules, **84,9 % pour les 674 personnes en cellule de 11 et plus** ;
Spearman(taille de cellule, top-1 armé) = **−0,020, p = 0,51**. Le comparateur retrouve
les gens **à l'intérieur** de leur cellule démographique grossière.

### 5.2 Le bloc réellement fourni à l'agent en compte onze, et il est quasi unique

**Déclaré post-hoc** : en cherchant le mécanisme, j'ai lu
`data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv`. L'agent « demographique »
(`gss_v6`) de l'archive Park n'est pas conditionné sur quatre attributs mais sur **onze** :
`age`, `census_division`, `political_ideology`, `political_party`, `education`, `race`,
`ethnicity`, `gender`, `income`, `neighborhood`, `sexual_orientation`.

| bloc | cellules | personnes seules dans leur cellule | plafond `moyenne(1/|cellule|)` |
|---|---|---|---|
| 4 axes (celui que j'avais préenregistré) | 146 | 25 / 1 052 — **2,38 %** | 13,88 % |
| **11 attributs (celui réellement fourni)** | **1 046** | **1 040 / 1 052 — 98,86 %** | **99,43 %** |

**Voilà le mécanisme, et il a un nom : ce n'est pas une baseline démographique, c'est un
bloc de quasi-identifiants.** Le « comparateur démographique » de Park reçoit un profil
qui rend **98,86 % des répondants uniques dans leur propre échantillon**. Ce n'est plus
une baseline au sens du manuscrit — c'est un identifiant.

**Aucun attribut ne porte seul cette unicité.** Laisse-un-de-côté, part de personnes
seules : sans `census_division` 92,87 % (−5,99 pt), sans `education` 96,29 % (−2,57 pt),
sans `political_ideology` 97,05 % (−1,81 pt), sans `political_party` 97,15 % (−1,71 pt),
sans `race` ou `ethnicity` **98,86 % (−0,00 pt)**. C'est la **conjonction** des onze qui
identifie — le mécanisme classique du quasi-identifiant, jamais un attribut vedette.

Et les items ne sont **pas** fortement déterminés par la démographie prise attribut par
attribut : part de la modalité majoritaire dans les groupes d'un attribut, contre des
groupes aléatoires de même taille, écart maximal **+4,91 pt** (`sexual_orientation`),
puis +3,09 pt (`political_ideology`), +2,62 pt (`political_party`) ; tous les autres sous
+1,6 pt. **Chaque item ne dit presque rien ; 177 items pondérés par la rareté disent
tout.**

### 5.3 P5 réfutée : A-LLR ne fait pas plus que relire la cellule, il la relit mal

J'avais prédit que les 85,17 % **dépasseraient** le plafond de la cellule. Ils sont
**au-dessous** : 85,17 % contre un plafond de **99,43 %**. Un attaquant qui saurait
décoder parfaitement le bloc de onze attributs depuis les 177 réponses ferait **mieux**
que A-LLR. **P5 est réfutée**, et sa réfutation est une bonne nouvelle pour la clarté :
il n'y a **rien à expliquer au-delà des quasi-identifiants**. A-LLR ne découvre pas une
fuite mystérieuse ; il décode, imparfaitement, un bloc qui était déjà identifiant avant
tout modèle de langage.

---

## 6. Ce que l'article doit écrire

### 6.1 Verdict sur mes cinq prédictions

| | verdict |
|---|---|
| **P1** reproduction | **confirmée**, au chiffre près |
| **P2** rapport ≤ 1,15× et IC recouvrants | **à moitié réfutée** : rapport 1,061× mais IC **disjoints** ; écart réel +5,23 pt [+2,66 ; +8,08] |
| **P3** croissance monotone avec les items | **confirmée**, 3,84 % → 85,17 %, rapport 5,02× → 1,06× |
| **P4** > 30 % de personnes seules dans leur cellule | **réfutée à la lettre** (2,38 % sur 4 axes) — **et confirmée au-delà** sur le bloc réel : **98,86 %** |
| **P5** A-LLR dépasse le plafond de cellule | **réfutée** : 85,17 % < 99,43 % |

### 6.2 La phrase exacte à écrire sur Park

Le manuscrit ne peut pas garder, sur Park, une phrase qui oppose 90,40 % à une baseline
désarmée. Proposition, à insérer avec la mention post-hoc :

> On the Park corpus, the 90.40 % closed-world top-1 and 60.17 % TPR at 1 % FPR of the
> best agent are **not evidence that the LLM twin leaks beyond demographics**. Armed with
> the same rarity-weighted likelihood attacker on the same basin, the demographics-only
> comparator reaches 85.17 % [82.89 ; 87.26] closed-world and 29.09 % TPR at 1 % FPR: a
> target-to-comparator ratio of **1.06×** [1.030 ; 1.097] closed-world (a paired gap of
> **+5.2 points** [+2.7 ; +8.1], statistically resolved but 27× smaller than the 29×
> obtained under the naive attack) and **2.07×** at 1 % FPR. The reason is that the Park
> "demographics-only" condition is conditioned on **eleven** attributes that leave
> **98.86 %** of the 1 052 respondents unique in their own sample — a quasi-identifier
> block, not a demographic baseline — and that a rarity-weighted attacker converts 177
> items into identity: the same comparator reaches only 3.84 % at 20 items and 22.74 % at
> 60. **Twin-2K-500, with 60 items and no such block, is the dataset that carries the
> claim** (23.23 % vs 0.78 %, 29.9×; 4.28 % vs 0.05 % at 1 % FPR, 88×).
>
> *(Post-hoc, not preregistered; audit of 13 September 2026.)*

### 6.3 Trois gestes de rédaction

1. **Ne pas retirer Park, le requalifier.** Park cesse d'être une démonstration que le
   jumeau fuit ; il devient une démonstration que **le risque de liaison existe sans
   jumeau LLM**, dès qu'un bloc de quasi-identifiants et assez d'items sont publiés
   ensemble. C'est un résultat plus fort et plus général que celui qu'on perd, et il est
   dans la ligne de la thèse de l'article.
2. **Le chiffre de tête de l'article doit venir de Twin, pas de Park.** Sur Twin le
   rapport à armement égal **s'améliore** (9,65× → 29,88× en monde fermé, 88× à 1 % de
   FPR). C'est le jeu qui porte le résultat.
3. **Publier la dépendance au nombre d'items comme une limite**, avec son étendue par
   tirage : un taux de ré-identification sur ce type de corpus n'est pas comparable d'une
   étude à l'autre sans déclarer le nombre **et** l'identité des items, ni la convention
   de départage des ex æquo.

---

## 7. Traçabilité

- Script : `analyses/c7_park_armement_egal.py` — graine `20260913`, aucun appel de
  modèle, aucun réseau, lecture seule sur `data/`, aucun script existant modifié.
- Données : `resultats/c7-park-armement-egal.csv`, 333 lignes, colonnes
  (`volet`, `jeu`, `condition`, `attaque`, `mesure`, `valeur`, `ic_bas`, `ic_haut`).
  Volets : `2 armement egal`, `3 rapport et controle`, `4 courbe items`,
  `5 structure demographique`, `5bis bloc demographique reel`.
- Aucune donnée individuelle n'est calculée, imprimée ni écrite : ni identifiant, ni
  appariement, ni cellule d'une personne. Seuls des taux et des distributions agrégées.
- Réductions déclarées : 8 tirages d'items par *k* (au lieu de 20) ; 5 tirages du témoin
  de permutation. Aucune autre.
- Écarts de raccordement : **aucun**.
