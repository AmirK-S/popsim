# Mémoire long : résultats API — résumé (4 modèles)

Bug corrigé (2026-09-11) : la vérité relue dans le panel gardait la casse/le libellé brut
(« too little », « fired ») alors que l'IA écrit déjà la nomenclature officielle
(« Too little », « Yes, fired ») — comparaison jamais égale, IA à 0,0000 partout. Fix dans
`analyses/memoire_long_analyse.py`, chargement seulement (canonicalisation de la vérité +
garde d'échec si >5 % de cellules IA manquantes). Traces complètes : 4 800/4 800 cellules ×
4 modèles, 0 rejet, coût total 1,79 $. **Écarts au plan** : 120 personnes (plancher prévu :
200) ; modèles réduits (nano/8B/micro), choisis pour tenir le plafond de 2 $.
## Table (exactitude, IC 95 %)
| modèle | horizon | persistance | jumeau IA | IA/mode (changées) | AUC désaccord |
|---|---|---|---|---|---|
| gpt41nano | +2/+4 | 0,721/0,715 | 0,602 [0,584-0,621] / 0,589 [0,572-0,607] | 0,39/0,48 | 0,63/0,61 |
| mistral-nemo | +2/+4 | 0,721/0,715 | 0,528 [0,509-0,549] / 0,527 [0,507-0,549] | 0,40/0,48 | 0,58/0,58 |
| llama31-8b | +2/+4 | 0,721/0,715 | 0,608 [0,591-0,625] / 0,609 [0,594-0,626] | 0,44/0,48 | 0,63/0,64 |
| nova-micro | +2/+4 | 0,721/0,715 | 0,550 [0,534-0,568] / 0,566 [0,548-0,584] | 0,43/0,48 | 0,56/0,58 |
Détail par modèle (IC de l'AUC) : `resultats/memoire-long-resultats-api-<clé>.md`.
## Verdicts et en clair
- **P1** (persistance > IA) : confirmée aux 2 horizons, 4 modèles ; écart plus petit à
  +4 ans pour 3/4 (pas gpt41nano).
- **P2** (IA ne bat pas le mode) : confirmée 7/8 cas ; 1 quasi-égalité sans portée pratique
  (nova-micro +4 ans, écart 0,0007).
- **P3** (AUC < 0,62) : confirmée pour mistral-nemo et nova-micro ; llama31-8b au-dessus aux
  2 horizons ; gpt41nano au-dessus à +2 ans.
- **En clair** : se souvenir de la dernière réponse bat le jumeau IA chez les 4 modèles ; le
  jumeau capte un signal réel mais modeste sur qui va changer d'avis, jamais suffisant pour
  remplacer la mémoire brute.
