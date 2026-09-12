# Mémoire long, run local gpt-oss-20b : résultats sur trace complète

Trace complète : 15 960/15 960 cellules notées (100 %, 0 rejet). Écart au plan : 120
cellules manquantes sur les 16 080 attendues, soit 3 personnes (133 au lieu de 134 par
panel) perdues à l'échantillonnage, pas d'appels manqués côté modèle. Aucun déséquilibre :
798 cellules par item, 7 980 par horizon, 5 320 par panel.

## Table principale (399 personnes, IC 95 % bootstrap sur les personnes)
| horizon | persistance | jumeau IA | mode du segment | AUC désaccord→changement |
|---|---|---|---|---|
| +2 ans | 0,7325 [0,7227-0,7434] | 0,5715 [0,5602-0,5830] | 0,6320 [0,6225-0,6418] | 0,5960 [0,5798-0,6116] |
| +4 ans | 0,7140 [0,7034-0,7253] | 0,5634 [0,5526-0,5755] | 0,6238 [0,6144-0,6326] | 0,5866 [0,5711-0,6023] |

Exactitude sur cellules changées : jumeau IA 0,3726 [0,3517-0,3931] (+2) / 0,3723
[0,3526-0,3921] (+4), contre mode du segment 0,4754 [0,4546-0,4972] / 0,4531 [0,4345-0,4729].

## Confrontation aux trois prédictions préenregistrées
- **P1** (persistance > IA, écart plus petit à +4 qu'à +2) : **confirmée**. Écart
  +0,1610 à +2 ans, +0,1507 à +4 ans — positif aux deux, et plus petit à +4 ans.
- **P2** (IA ne bat pas le mode du segment sur les cellules changées) : **confirmée**
  aux deux horizons (0,3726 < 0,4754 ; 0,3723 < 0,4531).
- **P3** (AUC < 0,62 aux deux horizons) : **confirmée** (0,5960 et 0,5866). Les trois
  prédictions tiennent, sans exception.

## Comparaison aux 4 modèles API (`memoire-long-resultats-api.md`)
La taille change-t-elle quelque chose ? **Non.** Écart persistance − IA : API 0,119 à
0,193 (11 à 19 points) ; local (3× plus gros) 0,161/0,151 — dans la même fourchette, pas
au-dessus. Sur cellules changées, l'IA locale (0,373/0,372) est **sous** les 4 modèles API
(0,39 à 0,48) : pas d'avantage, plutôt l'inverse. AUC local (0,587-0,596) se situe au
milieu de la fourchette API (0,56-0,64), ni meilleur ni pire.

**En clair** : même avec un modèle trois fois plus gros et un horizon de deux à quatre
ans, recopier la dernière réponse reste bien meilleur que le jumeau IA — la taille du
modèle ne comble pas l'écart.

## Écart avec l'analyse antérieure
Aucun écart : le CSV déjà présent (`memoire-long-oss20.csv`, commit `0b4137b`) avait déjà
été calculé sur la trace complète — le rejouer produit un fichier identique au bit près
(`git diff` vide). La mention d'une analyse déclenchée sur trace partielle ne s'applique
plus à l'état actuel du dépôt : rien à corriger cette fois.
