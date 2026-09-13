# Audit hostile : « la DP coûte plus cher que D4 » — verdict

statut: courant
mandat: Détruire, si elle est destructible, l'affirmation selon laquelle à protection comparable (eps=3 et eps=10) la confidentialité différentielle coûte plus cher que D4 sur les trois composantes d'utilité
agent: Claude Opus 5, sous-agent audit comparaison DP
ecriture: resultats/audit-comparaison-dp-2026-09-13.md uniquement (aucune modification de analyses/c7_dp.py, voir §9)
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, arrière-plan
cout_reel_usd: 0.00
branche: agent/audit/comparaison-dp (poussée, non fusionnée)

---

## Verdict

**À retirer.** L'affirmation est fausse sur ses deux moitiés : la « protection comparable »
n'en est pas une, et le « coût de la DP » n'est pas un coût de la DP. Huit failles, dont
cinq indépendamment fatales. Une formulation de repli défendable est donnée au §8 ; elle ne
revendique aucune supériorité de D4 sur la confidentialité différentielle.

Toutes les mesures ci-dessous ont été recalculées dans un arbre isolé sur les mêmes données
(`data/twin2k500`, 2 058 personnes, 60 items communs, 40 achat / 20 opinion), avec les
fonctions du dépôt reprises telles quelles (`c7_defense.mesurer_utilite`,
`c7_reidentification.rangs_attaque`, `c7_dp.marginales_bruitees`). Aucun appel de modèle.

---

## F1 — Fatale. Les deux « 0,0 » de D4 SONT la fuite, pas un avantage d'utilité

`c7_defense.defense_d4` permute chaque item **indépendamment** à l'intérieur de chaque
segment (`xd[membres, j] = x40[rng.permutation(membres), j]`, une permutation neuve par
item `j`). Conséquence vérifiée par calcul : pour les 40 segments × 40 items,
le multi-ensemble des réponses à l'item `j` dans le segment `g` est **conservé à
l'identique** (test d'égalité des vecteurs triés : `True` sur les 1 600 couples).

D4 republie donc, **exactement et sans bruit**, l'histogramme de chaque item à l'intérieur
de chaque segment. C'est précisément ce que la DP interdit : un adversaire informé qui
connaît les réponses des |g|−1 autres membres d'un segment reconstitue par différence les
40 réponses de la cible, avec certitude ; deux publications D4 d'un même segment avec et
sans une personne donnent la même chose. Le modèle de l'adversaire informé est le modèle
dans lequel la DP est définie ; D4 y a un epsilon formel infini.

Or `erreur_distribution = 0,0` et `erreur_groupes = 0,0` **sont la formulation en langage
d'utilité de ce même fait**. La comparaison « 0,0 / 0,0 contre 3,1 / 2,3 » note un
mécanisme qui publie une statistique exactement contre un mécanisme qui la protège, sur
l'exactitude de cette statistique. Elle est circulaire. À elle seule, cette faille
suffit : un relecteur de vie privée la verra en une lecture et ce sera le rejet.

## F2 — Fatale. Le bruit de confidentialité ne contribue à rien du coût mesuré

Le même générateur, **à eps = ∞, c'est-à-dire sans aucune confidentialité**, coûte autant
que sous DP. Moyennes sur 5 graines, reproduites ici (le fichier livré
`c7-dp-resultats.csv` contient déjà sa propre ligne eps=infini qui le montre) :

| eps | distribution | groupes | corrélations | moyenne |
|---|---|---|---|---|
| 3 | 3,563 | 2,789 | 4,591 | 3,65 |
| 10 | 3,191 | 2,471 | 4,501 | 3,39 |
| 100 | 3,346 | 2,708 | 4,487 | 3,51 |
| **∞ (aucune DP)** | **3,232** | **2,382** | **4,523** | **3,38** |

Le témoin non privé est indiscernable d'eps=10 et **meilleur** qu'eps=3. Dans le CSV livré,
le témoin eps=infini a même une moyenne (3,522) **pire** qu'eps=10 (3,380). La contribution
marginale du budget de confidentialité est donc de **0,0 point à eps=10 et ≈0,3 point à
eps=3**, non de 3,1-3,2 / 2,3-2,4 / 4,47-4,59. Ce qui est mesuré est le coût de
l'architecture (marginales d'item indépendantes, PrivBayes degré 0) et du désappariement de
référence (F3) — pas celui de la confidentialité différentielle. Le titre du résultat
attribue à la DP un coût dont elle est responsable à 0 %.

## F3 — Fatale. La DP est entraînée sur les humains et notée contre le jumeau

`c7_dp.py` ligne 148 ajuste le générateur sur `pool_v4` (les 2 058 **humains**), ligne 152
mesure son utilité contre `twin_x40`, le **jumeau** : `mesurer_utilite(x_synth[:, i_achat],
twin_x40, hum40, ...)`. D4, lui, est le jumeau permuté, noté contre le jumeau
(`c7_defense.py` ligne 235). La DP se voit donc facturer l'écart humains↔jumeau, qui vaut
**3,118 points** (`c7-defense-resultats.csv`, ligne `aucune`, colonne
`erreur_distribution_hum`) — soit exactement le « coût » publié de 3,1-3,2.

Preuve directe : le même générateur ajusté sur le jumeau (le même objet que D4 protège)
tombe de 3,19 → **0,919** à eps=10 et de 3,56 → **1,709** à eps=3 sur la distribution.
La colonne `erreur_distribution_hum` déjà présente dans `c7-dp-resultats.csv` le disait :
0,95 à eps=10, 1,60 à eps=3, 0,90 à eps=infini.

## F4 — Grave. L'implémentation DP est un homme de paille sur trois points standard

Laplace, composition **séquentielle basique** (eps/60 par item), sensibilité bornée 2. Un
praticien compétent compose sous zCDP avec le mécanisme gaussien : à eps=3, δ=1e-6,
ρ=0,147, **σ = 20,2** contre un écart-type Laplace effectif de 56,6 — **2,8× moins de
bruit au même eps** (2,9× à eps=1, 2,5× à eps=10). La DP non bornée (ajout/retrait,
sensibilité 1) le diviserait encore par deux. Rien de tout cela n'est exotique.

Corrigé (gaussienne zCDP **et** entraînement sur le jumeau, 5 graines) :

| eps | distribution | groupes | corrélations |
|---|---|---|---|
| 1 | 1,754 | 2,627 | 4,506 |
| **3** | **0,997** | 2,932 | 4,549 |
| **10** | **0,923** | 2,673 | 4,603 |

**Le chiffre publié de 3,11 / 3,21 sur la distribution devient 1,00 / 0,92**, soit une
division par 3,3. Et sur ces 0,92, la part imputable à la confidentialité est de 0,09 point
seulement : le même générateur non privé sur le jumeau coûte déjà 0,837.

Une piste testée et écartée honnêtement : les marginales **par segment** (composition
parallèle, gratuite en epsilon puisque les segments partitionnent la population) devraient
annuler l'erreur de groupes. Elles l'aggravent — 17,6 à eps=10 et 22,3 à eps=3 — parce que
`S_gra` a 40 segments de taille médiane 24. C'est une vraie limite de la DP ici, pas un
défaut d'implémentation (voir §7).

## F5 — Fatale. Un attaquant adaptatif renverse l'ordre des deux mécanismes

Le top-1 publié mesure **un** attaquant, contraint d'utiliser les 60 items. Laissons-le
choisir ses colonnes — la forme la plus faible d'adaptativité qui soit, bien en deçà de
l'adversaire informé de F1 :

| objet publié | attaque 60 items | 20 items d'opinion seuls | 40 items d'achat seuls |
|---|---|---|---|
| jumeau non protégé | 20,656 % | 0,260 % | **33,073 %** |
| **D4** | 0,131 % [0,007 ; 0,292] | **0,243 % [0,068 ; 0,459]** | 0,049 % |
| DP eps=3 | 0,085 % | 0,049 % | — |
| DP eps=10 | 0,075 % | 0,041 % | — |

D4 ne touche pas les 20 items d'opinion : ils sortent authentiques, personne par personne.
Un attaquant qui écarte le bloc qu'il sait brouillé porte la fuite de D4 de 0,131 % à
**0,243 %**. La publication DP n'a aucun item intact : son maximum sur les mêmes attaques
est 0,085 %. **L'ordre s'inverse : le meilleur attaquant donne D4 ≈ 3× plus fuyant que la
DP à eps=3**, là où l'article présente D4 comme le plus protecteur des deux. « À protection
comparable » est faux, et faux dans le sens défavorable à D4.

## F6 — Grave. Les taux comparés sont des effectifs de 0 à 3 personnes

D4 0,126 % = **2,6 personnes** sur 2 058 ; DP eps=3 0,158 % = **3,2 personnes** ; DP eps=10
0,000 % = **0 personne** ; DP eps=∞, **sans aucune confidentialité**, 0,024 % = 0,5
personne. La suite en epsilon est non monotone (0,012 % → 0,080 % → 0,158 % → 0 %) et tous
les IC se recouvrent. Le « 0 % à eps=10 » est zéro succès, pas une protection démontrée ;
et puisque le témoin sans DP est lui aussi à ~0, ce top-1 mesure l'architecture du
générateur, pas le budget. Aucun classement des deux mécanismes n'est soutenable sur ces
nombres, dans aucun sens.

## F7 — Grave. Aucun réplicat ni intervalle du côté de l'utilité

Le risque reçoit un bootstrap de 2 000 tirages ; les trois composantes d'utilité sont un
tirage unique, sans intervalle. Sur 10 graines, `erreur_correlations` de D4 vaut
**4,373 ± 0,058**, étendue [4,254 ; 4,433] ; côté DP l'écart-type inter-graines est de
0,05-0,09. L'argument « même sur les corrélations, 4,47-4,59 contre 4,40 » compare un écart
de 0,07 à 0,19 point entre deux quantités dont la dispersion de graine à graine est de
±0,06 à ±0,09. Il n'est pas mesurable. La valeur publiée 4,400 est un tirage du haut de
l'étendue de D4.

## F8 — Fatale pour la composante corrélations. Les deux mécanismes la détruisent à 100 %

|corr| moyenne sur les 780 paires des 40 items d'achat du jumeau = **4,317 points**. C'est
la note qu'obtient, par définition, tout mécanisme qui détruit toute corrélation. Or :
D4 = **4,373** (10 graines) — **au-dessus** de 4,317, donc D4 n'en préserve rien et ajoute
du bruit autour de zéro ; un tirage indépendant des marginales exactes du jumeau =
**4,531 ± 0,090** ; DP = 4,49-4,60. Les trois sont le même nombre : « tout est détruit ».
La différence 4,40 vs 4,47-4,59 est la variance d'échantillonnage de deux estimations de
zéro. **Il n'existe aucun avantage de D4 sur les corrélations**, et l'article ne peut pas
présenter cet écart comme un résultat.

---

## §7 — Ce qui survit à la correction, et l'objection résiduelle

Une seule chose : **les écarts entre segments**. Corrigée de F3 et F4, la DP coûte encore
2,7-2,9 points là où D4 coûte 0,0. Avec 2 058 personnes, 40 segments de taille médiane 24 et
un écart-type inter-segments réel de 14,0 points, aucun mécanisme DP à eps ≤ 10 ne
reproduit ces écarts — les marginales par segment, pourtant gratuites en epsilon, font pire
(§F4). C'est un coût authentique de la confidentialité différentielle à cette taille
d'échantillon.

**Objection résiduelle d'un relecteur** : « vous concédez donc que la DP coûte les
comparaisons de groupe, et D4 non. » **Réponse** : (a) le 0,0 de D4 est l'exacte
republication de l'histogramme intra-segment, c'est-à-dire la fuite de F1 — ce n'est pas
une utilité gagnée mais une protection non fournie ; (b) `erreur_groupes` compare
|écart-type − écart-type| : à taille de segment 24, le seul bruit d'échantillonnage d'un
générateur i.i.d. fabrique un écart-type inter-segments d'environ 10-11 points, noté comme
presque juste, sans qu'aucun segment ne diffère dans le bon sens. La métrique ne vérifie pas
la direction des écarts ; elle est une preuve faible dans les deux sens.

## §8 — Formulation exacte que l'article doit employer

> Nous n'avons pas comparé le coût de la confidentialité différentielle à celui de D4. Sur
> ces 2 058 personnes, un générateur synthétique à marginales d'item indépendantes coûte
> 0,9 à 1,0 point d'erreur de distribution et 2,7 à 2,9 points sur les écarts entre
> segments, qu'il soit bruité à eps = 3, à eps = 10, ou **pas bruité du tout** : le coût
> mesuré est celui de l'hypothèse d'indépendance entre items, et la contribution marginale
> du budget de confidentialité est de 0,1 à 0,3 point à eps = 3. Sur les corrélations, D4
> (4,37) et le générateur DP (4,50-4,55) détruisent l'un comme l'autre la totalité de la
> structure, dont l'amplitude vaut 4,32 : ni l'un ni l'autre n'en préserve quoi que ce soit.
> D4 n'offre aucune garantie formelle : il republie exactement l'histogramme de chaque item
> à l'intérieur de chaque segment, de sorte qu'un adversaire connaissant les autres membres
> du segment reconstitue les 40 réponses de la cible ; ses erreurs de distribution et de
> groupe nulles sont cette republication exacte, non un avantage. Enfin notre top-1 mesure
> un attaquant fixé : un attaquant qui écarte le bloc brouillé porte la fuite de D4 de
> 0,13 % à 0,24 %, au-dessus du générateur DP à eps = 3 (0,09 %), et ces taux correspondent
> à 0 à 3 personnes sur 2 058. **Nous ne revendiquons aucune supériorité de D4 sur la
> confidentialité différentielle**, seulement un compromis différent, sans garantie, contre
> l'attaque particulière que nous avons construite.

Sont à retirer en conséquence : la phrase comparative du §5 de
`resultats/cout-defense-synthese-2026-09-13.md` (« D4 domine la DP composante par composante
à protection égale ou supérieure »), la ligne de verdict de `c7-dp-resultats.md`, et le
fichier `resultats/c7-dp-courbe-combinee.csv`, qui concatène sur une même colonne
`perte_utilite_points` des lignes D4 mesurées jumeau-contre-jumeau et des lignes DP mesurées
humains-ajustés-contre-jumeau (F3) : ces deux colonnes ne sont pas commensurables et la
figure qui en sortirait serait fausse.

## §9 — Pourquoi `analyses/c7_dp.py` n'a pas été modifié

Le défaut de F3 est réel (ligne 152) et la correction tient en un mot : ajuster le
générateur sur `twin60` plutôt que sur `pool_v4`, ou mesurer contre `hum40` plutôt que
`twin_x40`. Je ne l'applique pas, pour trois raisons : le script exécute un plan
préenregistré (`c7-dp-preenregistrement.md`) qui prévoit explicitement l'ajustement sur les
humains, et le corriger en silence détruirait la reproductibilité de
`c7-dp-resultats.csv` ; la correction impose une réexécution complète que quatre autres
agents travaillant en parallèle n'attendent pas ; et le remède correct n'est pas une
retouche mais un amendement au préenregistrement, qui doit dire lequel des deux objets la
DP est censée protéger. Recommandation : amender, puis réexécuter avec le mécanisme
gaussien zCDP de F4, et republier les trois composantes avec au moins 10 graines et un
intervalle (F7).

---

### Traçabilité

Fichiers lus : `analyses/c7_dp.py`, `analyses/c7_defense.py`,
`analyses/c7_reidentification.py`, `analyses/a44_commun.py`, `analyses/a2_commun.py`,
`resultats/c7-dp-resultats.csv`, `resultats/c7-defense-resultats.csv`,
`resultats/c7-defense-courbe.csv`, `resultats/c7-dp-resultats.md`,
`resultats/cout-defense-synthese-2026-09-13.md`.

Mesures nouvelles produites pour cet audit (scripts jetables hors dépôt, graine 20260913,
important les fonctions du dépôt sans les recopier) : balayage eps ∈ {0,5 ; 1 ; 3 ; 10 ;
100 ; ∞} × 5 graines pour l'architecture livrée (F2) ; le même ajusté sur le jumeau (F3) ;
marginales par segment sous composition parallèle (F4) ; mécanisme gaussien composé sous
zCDP, δ = 1e-6 (F4) ; 10 réplicats de D4 (F7) ; attaques top-1 sur trois sous-ensembles
d'items, bootstrap personnes 2 000 (F5) ; conservation du multi-ensemble intra-segment
item par item, 1 600 couples (F1) ; |corr| moyenne des 780 paires et plancher de
destruction (F8) ; écart-type inter-segments réel, tailles de `S_gra` (F7).
