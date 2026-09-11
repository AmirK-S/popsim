# Mémoire long : résultats API — mistral-nemo (mistralai/mistral-nemo)

Calculé le 11 septembre 2026. Trace `data/traces/memoire-long-api/ml-mistral-nemo.jsonl`
(4 800/4 800 cellules, 0 rejet). Script `analyses/memoire_long_analyse.py` (corrigé, voir
`resultats/memoire-long-resultats-api.md`). IC à 95 % : bootstrap personnes, 1000 réplicats,
graine 20260911. 120 personnes, 20 items, 2 horizons.

## Table (exactitude, IC entre crochets)

| horizon | persistance | jumeau IA | mode du segment | règle combinée | IA/changées | mode/changées | AUC désaccord |
|---|---|---|---|---|---|---|---|
| +2 ans | 0,7207 [0,7001-0,7407] | 0,5280 [0,5085-0,5487] | 0,6405 [0,6185-0,6623] | 0,6829 [0,6624-0,7039] | 0,4021 [0,3632-0,4400] | 0,4766 [0,4341-0,5212] | 0,5762 [0,5467-0,6035] |
| +4 ans | 0,7153 [0,6952-0,7354] | 0,5267 [0,5067-0,5486] | 0,6443 [0,6226-0,6668] | 0,6897 [0,6694-0,7126] | 0,3915 [0,3561-0,4259] | 0,4560 [0,4136-0,4952] | 0,5816 [0,5522-0,6143] |

## Verdicts

- **P1** (persistance > IA, écart plus petit à +4 ans) : écarts +0,1927 (+2 ans) et +0,1886
  (+4 ans) — positif aux deux horizons, écart légèrement plus petit à +4 ans : forme
  CONFIRMÉE (à confirmer par les IC, chevauchants).
- **P2** (IA ne bat pas le mode du segment sur les cellules changées) : CONFIRMÉE aux deux
  horizons (0,4021 vs 0,4766 ; 0,3915 vs 0,4560).
- **P3** (AUC désaccord→changement < 0,62) : CONFIRMÉE aux deux horizons (0,5762 ; 0,5816).

## En clair

C'est le modèle le plus faible des quatre pour se souvenir de la personne : 0,53 d'accord
avec la vérité contre 0,72 pour simplement répéter la dernière réponse connue. Il confirme
les trois prédictions du préenregistrement : la mémoire brute suffit mieux que ce jumeau, et
son désaccord avec le passé ne prédit pas fiablement un vrai changement d'avis.
