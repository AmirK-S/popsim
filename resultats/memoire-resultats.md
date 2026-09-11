# Mémoire : résultats

Calculé le 11 septembre 2026, après `resultats/memoire-predictions.md`. Script :
`analyses/memoire_twin.py`. IC à 95 % : bootstrap personnes × items, 1000 réplicats, graine
20260909. 108 items répétés, 8 configurations admissibles, chacune sur son propre périmètre
(2 058 personnes sauf JSON Persona mini, 1 000).

## Table principale (exactitude, IC entre crochets)

| configuration | persistance | jumeau | B0 mode | PMM k=10 | jumeau/changées | B0/changées | AUC désaccord |
|---|---|---|---|---|---|---|---|
| Demographics Only | 0,712 [0,678-0,741] | 0,500 [0,465-0,533] | 0,522 | 0,491 | 0,353 | 0,373 | 0,607 [0,595-0,619] |
| JSON Persona GPT4.1 | 0,712 [0,678-0,741] | **0,574** [0,531-0,611] | 0,522 | 0,491 | 0,366 | 0,373 | **0,649** [0,636-0,660] |
| JSON Persona mini | 0,706 [0,675-0,737] | 0,545 [0,508-0,579] | 0,518 | 0,491 | 0,369 | 0,375 | 0,630 [0,616-0,641] |
| Text défaut | 0,712 [0,678-0,741] | 0,548 [0,509-0,583] | 0,522 | 0,491 | 0,361 | 0,373 | 0,634 [0,624-0,643] |
| Text raisonnement | 0,712 [0,678-0,741] | 0,544 [0,507-0,577] | 0,522 | 0,491 | 0,367 | 0,373 | 0,630 [0,620-0,639] |
| Text répétition | 0,712 [0,678-0,741] | 0,549 [0,511-0,585] | 0,522 | 0,491 | 0,364 | 0,373 | 0,633 [0,622-0,643] |
| Text Persona mini | 0,712 [0,678-0,741] | 0,553 [0,514-0,588] | 0,522 | 0,491 | 0,365 | 0,373 | 0,635 [0,626-0,644] |
| Text Persona Gemini | 0,712 [0,678-0,741] | 0,551 [0,513-0,586] | 0,522 | 0,491 | 0,350 | 0,373 | 0,644 [0,634-0,653] |

Taux de changement humain : 48 632 cellules sur 168 768 (28,8 %), 2 058 personnes, 108
items ; l'audit citait 3 448 sur 294 personnes et 75 QID (22,1 %) — même ordre de grandeur,
écart attribuable au nombre de personnes et à la granularité (matrice comptée par ligne).

Règle combinée (P4, 8 admissibles, 1 000 personnes, 81 879 cellules) : persistance
0,706 [0,675-0,737], combinée 0,612 [0,578-0,645], gain **-0,094** (31,3 % basculées).

## Verdicts

- **P1 CONFIRMÉE.** Écart persistance - meilleur jumeau (JSON Persona GPT4.1) = 0,712 -
  0,574 = **13,8 points**, IC disjoints, largement au-delà des 10 points prédits.
- **P2 CONFIRMÉE.** Sur les cellules changées, le meilleur jumeau fait 0,366, B0 mode 0,373 :
  écart -0,8 point, dans la marge de 2 points, et dans le sens « pas mieux ».
- **P3 RÉFUTÉE.** AUC(désaccord jumeau/passé → changement) = 0,649 [0,636-0,660] pour le
  meilleur jumeau, et entre 0,607 et 0,649 pour les huit. Toutes les bornes basses dépassent
  0,60 : le désaccord est un signal faible mais réel, pas du bruit.
- **P4 CONFIRMÉE**, mais pas comme prévu. La règle combinée ne gagne pas un point : elle en
  perd 9,4. Le vote à 5 sur 8 bascule trop de cellules (31 %) avec une precision insuffisante
  pour rentabiliser le signal pourtant réel de P3. Une règle mieux calibrée n'est pas exclue,
  mais celle-ci, fixée avant calcul, nuit.

## Ce que ça veut dire

Sur ce jeu de données, la mémoire suffit et le jumeau ne la remplace pas : la persistance
gagne de 14 points, et aucun jumeau ne bat la modalité la plus fréquente sur les changements
d'avis. Mais le jumeau n'est pas aveugle au changement : son désaccord avec la réponse passée
le prédit un peu mieux que le hasard, sans qu'une règle simple sache en tirer parti ici.
Limites : un seul jeu de données, pas de trajectoire longue (deux points dans le temps),
déséquilibre d'information assumé (le jumeau n'a pas vu la réponse passée), une seule règle
de combinaison testée parmi d'autres possibles.
