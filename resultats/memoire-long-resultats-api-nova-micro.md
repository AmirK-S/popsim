# Mémoire long : résultats API — nova-micro (amazon/nova-micro-v1)

Calculé le 11 septembre 2026. Trace `data/traces/memoire-long-api/ml-nova-micro.jsonl`
(4 800/4 800 cellules, 0 rejet). Script `analyses/memoire_long_analyse.py` (corrigé, voir
`resultats/memoire-long-resultats-api.md`). IC à 95 % : bootstrap personnes, 1000 réplicats,
graine 20260911. 120 personnes, 20 items, 2 horizons.

## Table (exactitude, IC entre crochets)

| horizon | persistance | jumeau IA | mode du segment | règle combinée | IA/changées | mode/changées | AUC désaccord |
|---|---|---|---|---|---|---|---|
| +2 ans | 0,7207 [0,7001-0,7407] | 0,5504 [0,5341-0,5684] | 0,6405 [0,6185-0,6623] | 0,7050 [0,6853-0,7250] | 0,4287 [0,3892-0,4689] | 0,4766 [0,4341-0,5212] | 0,5580 [0,5303-0,5844] |
| +4 ans | 0,7153 [0,6952-0,7354] | 0,5659 [0,5478-0,5838] | 0,6443 [0,6226-0,6668] | 0,7201 [0,7014-0,7395] | 0,4567 [0,4241-0,4893] | 0,4560 [0,4136-0,4952] | 0,5806 [0,5548-0,6046] |

## Verdicts

- **P1** (persistance > IA, écart plus petit à +4 ans) : écarts +0,1703 (+2 ans) et +0,1495
  (+4 ans) — positif aux deux horizons, écart plus petit à +4 ans : forme CONFIRMÉE (à
  confirmer par les IC, chevauchants).
- **P2** (IA ne bat pas le mode du segment sur les cellules changées) : confirmée à +2 ans
  (0,4287 vs 0,4766) ; à +4 ans l'IA dépasse le mode de 0,0007 (0,4567 vs 0,4560) — un écart
  minuscule, dans le bruit, donc NON CONFIRMÉE au sens strict du script mais sans portée
  pratique (quasi-égalité).
- **P3** (AUC désaccord→changement < 0,62) : CONFIRMÉE aux deux horizons (0,5580 ; 0,5806).

## En clair

Modèle intermédiaire : 0,55-0,57 d'accord avec la vérité, contre 0,72 pour se souvenir
simplement de la dernière réponse. La mémoire brute domine largement ; le seul accroc est un
écart quasi nul (0,0007) entre l'IA et le mode du groupe sur les changements à +4 ans, sans
conséquence pratique.
