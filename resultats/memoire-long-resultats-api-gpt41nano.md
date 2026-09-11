# Mémoire long : résultats API — gpt41nano (openai/gpt-4.1-nano)

Calculé le 11 septembre 2026. Trace `data/traces/memoire-long-api/ml-gpt41nano.jsonl`
(4 800/4 800 cellules, 0 rejet). Script `analyses/memoire_long_analyse.py` (corrigé, voir
`resultats/memoire-long-resultats-api.md`). IC à 95 % : bootstrap personnes, 1000 réplicats,
graine 20260911. 120 personnes, 20 items, 2 horizons.

## Table (exactitude, IC entre crochets)

| horizon | persistance | jumeau IA | mode du segment | règle combinée | IA/changées | mode/changées | AUC désaccord |
|---|---|---|---|---|---|---|---|
| +2 ans | 0,7207 [0,7001-0,7407] | 0,6019 [0,5837-0,6214] | 0,6405 [0,6185-0,6623] | 0,6966 [0,6770-0,7156] | 0,3926 [0,3569-0,4314] | 0,4766 [0,4341-0,5212] | 0,6298 [0,6039-0,6583] |
| +4 ans | 0,7153 [0,6952-0,7354] | 0,5891 [0,5717-0,6072] | 0,6443 [0,6226-0,6668] | 0,7016 [0,6838-0,7218] | 0,3597 [0,3240-0,3967] | 0,4560 [0,4136-0,4952] | 0,6123 [0,5864-0,6377] |

## Verdicts

- **P1** (persistance > IA, écart plus petit à +4 ans) : écarts +0,1189 (+2 ans) et +0,1262
  (+4 ans) — positif aux deux horizons, mais l'écart est légèrement PLUS GRAND à +4 ans, pas
  plus petit. Forme non confirmée, direction oui.
- **P2** (IA ne bat pas le mode du segment sur les cellules changées) : CONFIRMÉE aux deux
  horizons (0,3926 vs 0,4766 ; 0,3597 vs 0,4560).
- **P3** (AUC désaccord→changement < 0,62) : NON CONFIRMÉE à +2 ans (0,6298, IC bas
  0,6039 > seuil non atteint mais point au-dessus), confirmée à +4 ans (0,6123).

## En clair

Ce petit modèle se souvient un peu de la personne (0,60 d'accord contre 0,72 pour se
souvenir simplement de sa dernière réponse) mais reste nettement moins bon que la mémoire
brute, et ne devine pas mieux les changements d'avis qu'une règle de bon sens (le choix le
plus fréquent du groupe).
