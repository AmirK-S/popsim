# C7, synthétiseur ajusté sur la cible : résultats (12 septembre 2026)
Préenregistré dans `c7-synth-ajuste-preenregistrement.md`, calculé par
`analyses/c7_synth_ajuste.py`. CART séquentiel et forêt (300 arbres) testés d'abord,
plafonnent à 0,45–0,53 (sous la cible) : abandonnés, voir docstring. Méthode retenue :
**donneur plus proche voisin (k=1) sur le bloc cible lui-même**, distance = désaccord sur
les 59 autres items + poids résiduel sur l'item prédit (calibré, plateau stable à 0,584 sur
poids ∈ [0,01 ; 0,85]). Attaque `c7_reidentification.rangs_attaque`, non modifiée.

## 1. Résultat, comparé au jumeau et aux comparateurs précédents (60 items, pool 2 058)
| synthétiseur | exactitude | top-1 [IC 95 %] | top-10 | rang médian |
|---|---|---|---|---|
| retest humain (plafond) | 0,745 | 81,6 % | 91,6 % | -- |
| JSON Persona GPT4.1 (jumeau LLM) | 0,590 | **20,7 %** [19,0;22,4] | 42,7 % | 20 |
| **Donneur ajusté sur bloc cible (k=1)** | 0,584 | **0,00 %** [0;0] | **53,2 %** [51,0;55,3] | **8,5** |
| G-LR / G-copule (contexte seul) | 0,476 | 0,22–0,25 % | ~2 % | ~610 |
| PMM k=10 / B2 argmax (contexte seul) | 0,475 / 0,511 | 0,23 % / 0,07 % | 1,2–1,7 % | -- |
Fidélité (chute sous permutation intra segment S_gra) : vraie 0,584, permutée 0,442,
**chute 0,142** (24,3 % relatif) — signal propre à la personne, pas qu'un gabarit de groupe.
## 2. Deux métriques qui divergent
Top-1 tombe à 0,00 % (0/2058), **sous les comparateurs non ajustés** (0,22–0,25 %), malgré
une exactitude quasi appariée (0,584 vs 0,590) et l'accès explicite au bloc cible.
Diagnostic (indices seulement, aucun pid) : le plus proche du composite synthétique n'est
presque jamais la vraie personne (distance moyenne à soi 0,42) mais un autre candidat du
pool à 0,08 en moyenne — patchwork plausible mais générique, jamais un profil qui pointe
vers la bonne personne en tête de classement. **Mais le top-10 (53,2 %) dépasse celui du
jumeau (42,7 %)** : ce comparateur resserre le voisinage sans jamais désigner une personne
en premier. Pas de biais mécanique : 1 133 donneurs distincts servent de rang-1 sur 2 058.

## 3. Verdict : issue (b), avec une réserve sur le top-10
**Spécificité LLM confirmée sur le critère préenregistré (top-1)**, même en autorisant le
synthétiseur à voir le bloc cible, à exactitude quasi identique : 0,00 % contre 20,7 %,
écart au moins aussi net qu'avec les comparateurs non ajustés. Réserve : sur le top-10, ce
comparateur de plafond fuit *plus* que le jumeau — la spécificité LLM ne tient donc que pour
l'identification stricte (top-1), pas pour la mise en petit voisinage.

## 4. Conséquence exacte pour A2 (`resultats/article-synthese.md`)
A2 reste vraie et se renforce sur le top-1 : même un comparateur explicitement avantagé
(ajusté sur les réponses cibles) ne dépasse pas 0,3 % — il tombe à 0 %. **Ajout requis à
A2** : préciser que l'écart porte sur le top-1 ; ne pas généraliser à toute métrique (le
top-10 d'un synthétiseur ajusté sur la cible peut dépasser celui du jumeau).
