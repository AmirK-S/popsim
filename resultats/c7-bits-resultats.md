# C7 bits : ce que la fuite coûte en vie privée par point d'exactitude gagné

Préenregistré dans `c7-bits-preenregistrement.md` (commit 7ddb1c1) et `c7-bits-preenregistrement-avenant.md` (26aaff4), calculé par `analyses/c7_bits.py` (aucun appel de modèle, lecture seule, bootstrap 2 000, graine 20260912). Sorties agrégées : `c7-bits.csv`, `c7-bits-par-item.csv`, `c7-bits-par-item-avenant.csv`, `c7-bits-regressions.csv`, `c7-bits-transport.csv`, figure `c7-bits.png`. **Aucun identifiant, aucun appariement individuel.**
Validation des estimateurs : rangs uniformes → 0,00 bit (IC contient 0) ; identification parfaite → 11,01 bits = log2(N) ; top-1 recalculés identiques aux publiés (Twin JSON 4.1 20,6 %, Stanford composite 65,6 %).

## 1. Fuite, utilité, ratio (bits d'identité = minorant, borne dyadique + Miller-Madow)

| jeu | prédicteur | bits [IC 95 %] | exactitude | gain sur la modale | bits par point |
|---|---|---|---|---|---|
| Twin (N=2 058, plafond 11,01) | retest humain v1-3 | 9,15 [9,00 ; 9,31] | 0,745 | +24,6 pp | 0,37 |
| | JSON Persona GPT4.1 | **3,55** [3,39 ; 3,72] | 0,590 | +9,1 pp | **0,39** |
| | Text Persona Gemini | 2,82 [2,68 ; 2,97] | 0,560 | +6,1 pp | 0,47 |
| | 5 autres jumeaux | 1,59 à 2,40 | 0,55 | +4,7 à +5,9 pp | 0,29 à 0,45 |
| | Demographics Only (LLM) | 0,82 [0,75 ; 0,90] | 0,494 | −0,5 pp | fuite sans gain |
| | **PMM k=10** | **0,19** [0,16 ; 0,23] | 0,475 | −2,4 pp | fuite sans gain |
| | **B1 / B2 argmax** | 0,16 / **0,08** | 0,504 / 0,511 | +0,5 / **+1,2 pp** | 0,31 / **0,068** |
| | B0 mode (validation) | −0,004 [−0,003 ; 0,002] | 0,499 | 0,0 pp | — |
| Stanford (N=1 052, plafond 10,04) | retest humain vague 2 | 9,62 [9,49 ; 9,74] | 0,812 | +21,7 pp | 0,44 |
| | composite | **7,47** [7,27 ; 7,66] | 0,712 | +11,7 pp | 0,64 |
| | entretien / enquête | 6,10 / 4,00 | 0,688 / 0,652 | +9,3 / +5,7 pp | 0,65 / 0,70 |
| | démographique | 1,23 [1,13 ; 1,36] | 0,609 | +1,4 pp | 0,92 |
| | persona | 0,34 [0,28 ; 0,42] | 0,568 | −2,7 pp | fuite sans gain |

Estimateur plug-in secondaire (biaisé vers le haut pour les bits) : 2,97 au lieu de 3,55 pour JSON 4.1, −0,69 pour B0 — il échoue la validation à vide, le chiffre principal reste la borne dyadique. Voie appariement : la somme des MI par item donne 7,2 bits (Twin) et **58,7** (Stanford, contre un plafond d'identité de 10,04) — la dépendance entre items la rend inutilisable comme total, comme préenregistré ; elle ne sert qu'item par item.

## 2. Verdicts préenregistrés
- **P4 (ordres de grandeur) : rempli.** B0 ≈ 0 (IC contient 0), statistiques < 0,5 bit, JSON 4.1 ≥ 3, composite ≥ 6.
- **P1 : rempli par la règle de repli déclarée.** PMM a un gain d'exactitude **négatif** (−2,4 pp) : le ratio n'est pas calculable, on compare à fuite égale. À exactitude inférieure, PMM fuit 0,19 bit contre 3,55 pour JSON 4.1, **facteur 19**. Sur le seul comparateur statistique à gain positif (B2, +1,2 pp), le ratio vaut 0,068 contre 0,29-0,47 pour les jumeaux : **les jumeaux LLM paient 4 à 7 fois plus de vie privée par point d'exactitude**.
- **Nuance honnête, contre l'hypothèse** : le retest humain a un ratio de 0,37 (Twin) et 0,44 (Stanford), donc **aussi bon ou meilleur que les jumeaux**. Le surcoût de vie privée des jumeaux existe face aux prédicteurs statistiques, pas face à un humain qui répond deux fois.
- **P2 (transportabilité) : rempli.** Bits normalisés par l'entropie humaine : 0,0439 (Twin) contre 0,0327 (Stanford), **facteur 1,34** ; bits par item 0,059 contre 0,042 (facteur 1,4). Le top-1, lui, varie d'un facteur 3,2 (20,7 % contre 65,7 %) entre les mêmes jeux. **La mesure voyage, le taux non.**
- **P3 (plafond humain) : rempli** sur les deux jeux, en bits et en utilité.

## 3. Avenant : pourquoi l'entropie d'un item ne prédit pas l'identification
Pouvoir d'identification d'un item : δ_j = a_j − c_j (coïncidence avec la vraie personne moins coïncidence avec un candidat au hasard).
- **Anomalie expliquée (prédiction 5 : remplie).** Twin, items d'achat : δ médian 0,209, entropie 0,99 bit. Items d'opinion : δ médian **0,029** (7 fois moins) pour une entropie **2,11 bits** (deux fois plus), et une information conditionnelle médiane **nulle** (−0,002 bit). Sur ces items le jumeau ne dit rien de la personne au-delà du démographique : haute entropie, zéro identification.
- **Régression (δ ~ entropie + MI conditionnelle vraie, poids standardisés).** Twin : entropie −0,66 [−0,84 ; −0,49], MI conditionnelle **+0,53** [0,40 ; 0,68]. Stanford : entropie +0,03 [−0,06 ; 0,12], MI conditionnelle **+0,87** [0,80 ; 0,94]. **Prédictions 1 et 3 remplies** (poids de l'information conditionnelle ≥ 0,5 des deux côtés, rapport 1,64 ≤ 2). **Prédiction 2 réfutée telle qu'écrite** : l'entropie corrèle fortement avec δ (r = −0,81 sur Twin, +0,57 sur Stanford) — mais **en sens opposé selon le jeu**, donc elle ne peut pas être une loi ; l'information conditionnelle, elle, garde le même signe et le même ordre de grandeur (r = 0,72 et 0,89). Le substitut par différence (MI jumeau − MI démographique) est instable (poids de 0,25 à 0,77 selon le jeu) : la conclusion repose sur la MI conditionnelle vraie, comme prévu par la règle d'instabilité.
- **Prédiction 4 (top-1 de Stanford à k=60) : le chiffre tombe juste, mais je ne le revendique pas.** Modèle normal des maxima, φ = 1,22 transporté de Twin : **0,354 prédit contre 0,340 observé**. Or le même modèle échoue à ses deux contrôles : il donne 0,053 pour Twin (observé 0,206, facteur 4 en dessous) et 0,983 pour Stanford à k=177 (observé 0,656). Cause diagnostiquée : le modèle ignore l'hétérogénéité entre personnes (certaines sont bien mieux modélisées que la moyenne et gagnent le tri). **Un succès isolé entre deux échecs est une coïncidence, pas une loi** : la prédiction de taux entre jeux reste hors de portée, ce qui confirme la section 2 par l'autre bout — les bits se transportent, les taux non.

## 4. Ce que la mesure permet de dire, que le taux ne permettait pas
Le taux top-1 ne compare ni deux jeux, ni deux prédicteurs d'exactitude différente. Les bits d'identité le font : ils sont bornés par log2(N), validés à vide, comparables une fois normalisés par l'entropie humaine, et ils s'assemblent avec l'utilité en un prix — bits de vie privée par point d'exactitude. Ils montrent aussi que PMM et Demographics Only fuient **sans rien gagner**, cas qu'un ratio seul aurait masqué.

## 5. En clair
Un jumeau LLM fait payer environ **0,4 bit d'identité par point d'exactitude gagné**, contre **0,07 pour le meilleur prédicteur statistique utile** : cinq fois plus cher, pour la même chose. Et ce qui identifie n'est pas la question la plus riche, c'est celle où le jumeau sait de vous quelque chose que votre profil démographique ne dit pas.
