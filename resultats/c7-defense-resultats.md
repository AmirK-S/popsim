# C7-defense, resultats : reduire la fuite sans detruire l'utilite

Preenregistre dans `resultats/c7-defense-preenregistrement.md`, calcule par
`analyses/c7_defense.py` (graine 20260911, bootstrap personnes 2000). Defenses appliquees
uniquement aux 40 items d'achat du jumeau `JSON Persona - GPT4.1` (jamais aux humains, ni aux
20 items d'opinion). Risque = top-1 sur 2 058 humains vague 4 ; utilite = moyenne de trois
erreurs en points contre le jumeau non protege (distribution, ecarts `S_gra`, correlations).
Reference sans defense : 20,68 % [19,04 ; 22,41].

## Tableau risque-utilite (`c7-defense-courbe.csv`, figure `c7-defense-courbe.png`)

| defense | reglage | top-1 | perte d'utilite | dont distrib. / groupes / corr. |
|---|---|---|---|---|
| D1 agregation | k=2 | 3,41 % | 9,6 | 24,5 / 2,0 / 2,5 |
| **D1 agregation** | **k=10** | **0,55 %** | **3,8** | **3,5 / 2,2 / 5,6** |
| D1 agregation | k=25 | 0,24 % | 12,1 | 22,0 / 4,4 / 10,0 |
| D2 bruit | p=50 % | 1,91 % | 2,1 | 0,7 / 2,1 / 3,5 |
| D3 retrait total | - | 0,26 % | 100 (rien a publier) | - |
| D3 retrait | 20/40 gardes | 4,44 % | 2,9 | 0,8 / 4,9 / 3,0 |
| **D4 melange segment** | - | **0,13 %** | **1,5** | **0,0 / 0,0 / 4,4** |

(tableau complet des 14 reglages dans `c7-defense-resultats.csv`)

## Reglage recommande : D4, permutation intra-segment, et ce qui se perd
Top-1 = 0,13 % [0,01 ; 0,28] contre 20,68 % sans defense : la fuite disparait presque
completement. La perte d'utilite (1,47 point) vient **entierement** des correlations entre
items (4,4 points) : distribution par item et ecarts entre segments demographiques sont
**exactement** preserves (permuter dans un segment ne change ni sa moyenne ni la moyenne
globale) — la prediction preenregistree. Seuls les liens entre deux items d'achat precis
pour la MEME personne (« qui achete X achete aussi Y ») s'effacent, et ce cout (4,4 points)
reste **plus petit** que l'ecart deja present entre jumeau non protege et humains sur ce
meme indicateur (5,8 points, colonnes `_hum` de `c7-defense-resultats.csv`). D1 (k=10)
atteint aussi un top-1 sous 1 % mais coute plus cher (3,8 points, sur les trois erreurs) ;
le bruit (D2) ne descend jamais sous 1 % dans la plage testee ; retirer une partie du bloc
(D3) est soit inutile aux niveaux surs, soit ruineux en utilite au niveau total.

## Verdict
**Critere preenregistre rempli** : D4 ramene le top-1 sous 1 % avec une perte d'utilite
sous 2 points, en cassant bien specifiquement les correlations, comme predit.

**En clair** : mélanger les réponses d'achat entre personnes du même groupe démographique
supprime quasiment toute la fuite d'identité et ne change presque rien aux moyennes ou aux
écarts entre groupes publiés — seul ce qui relie deux achats précis chez une même personne
s'efface.
