# Mémoire long : résultats API — llama31-8b (meta-llama/llama-3.1-8b-instruct)

Calculé le 11 septembre 2026. Trace `data/traces/memoire-long-api/ml-llama31-8b.jsonl`
(4 800/4 800 cellules, 0 rejet). Script `analyses/memoire_long_analyse.py` (corrigé, voir
`resultats/memoire-long-resultats-api.md`). IC à 95 % : bootstrap personnes, 1000 réplicats,
graine 20260911. 120 personnes, 20 items, 2 horizons.

## Table (exactitude, IC entre crochets)

| horizon | persistance | jumeau IA | mode du segment | règle combinée | IA/changées | mode/changées | AUC désaccord |
|---|---|---|---|---|---|---|---|
| +2 ans | 0,7207 [0,7001-0,7407] | 0,6079 [0,5905-0,6245] | 0,6405 [0,6185-0,6623] | 0,6928 [0,6729-0,7128] | 0,4411 [0,4054-0,4783] | 0,4766 [0,4341-0,5212] | 0,6300 [0,6046-0,6543] |
| +4 ans | 0,7153 [0,6952-0,7354] | 0,6089 [0,5937-0,6260] | 0,6443 [0,6226-0,6668] | 0,6977 [0,6808-0,7157] | 0,4266 [0,3945-0,4588] | 0,4560 [0,4136-0,4952] | 0,6351 [0,6108-0,6598] |

## Verdicts

- **P1** (persistance > IA, écart plus petit à +4 ans) : écarts +0,1128 (+2 ans) et +0,1064
  (+4 ans) — positif aux deux horizons, écart plus petit à +4 ans : forme CONFIRMÉE (à
  confirmer par les IC, chevauchants).
- **P2** (IA ne bat pas le mode du segment sur les cellules changées) : CONFIRMÉE aux deux
  horizons (0,4411 vs 0,4766 ; 0,4266 vs 0,4560).
- **P3** (AUC désaccord→changement < 0,62) : NON CONFIRMÉE aux deux horizons (0,6300 ;
  0,6351) — c'est le seul des quatre modèles au-dessus du seuil aux deux horizons.

## En clair

C'est le meilleur des quatre modèles pour se souvenir de la personne (0,61 d'accord, contre
0,72 pour la mémoire brute) et le seul dont le désaccord avec le passé est un signal un peu
plus net (AUC > 0,62 aux deux horizons) : pas assez pour rentabiliser une règle de
combinaison, mais un indice que « petit modèle » ne veut pas dire « sans aucun signal ».
