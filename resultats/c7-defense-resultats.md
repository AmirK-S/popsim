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
completement. **Le cout ne se lit pas en moyenne des trois erreurs (1,47 point) : cette
moyenne divise par trois un effet qui ne porte que sur une seule composante.** Par
composante : distribution par item (0,0 point) et ecarts entre segments demographiques
(0,0 point) sont **exactement** preserves (permuter dans un segment ne change ni sa
moyenne ni la moyenne globale) — la prediction preenregistree ; correlations entre items
(4,4 points) : seuls les liens entre deux items d'achat precis pour la MEME personne
(« qui achete X achete aussi Y ») s'effacent.

**Effet sur l'ecart aux reponses humaines.** `erreur_correlations_hum` (meme indicateur,
mesure contre les vraies reponses humaines) passe de **5,78** sans defense a **9,71**
apres D4 (`c7-defense-resultats.csv`, colonnes `_hum`) : le jumeau defendu est **68 % plus
loin des humains** sur les correlations que le jumeau non protege. Comparer un increment
(le cout de 4,4 points, mesure contre le jumeau non defendu) a un niveau (l'ecart
jumeau/humains) serait une erreur : les deux ne se soustraient pas. Le bon enonce est que
D4 supprime la fuite d'identite au prix d'une degradation reelle et notable de la
correlation aux reponses humaines, pas d'un cout negligeable au regard de cet ecart.

D1 (k=10) atteint aussi un top-1 sous 1 % mais coute plus cher (3,8 points, sur les trois
erreurs) ; le bruit (D2) ne descend jamais sous 1 % dans la plage testee ; retirer une
partie du bloc (D3) est soit inutile aux niveaux surs, soit ruineux en utilite au niveau
total.

## Verdict
**Critere preenregistre rempli** : D4 ramene le top-1 sous 1 %, en cassant bien
specifiquement les correlations (4,4 points), comme predit — au prix d'une degradation de
68 % de l'ecart aux reponses humaines sur ce meme indicateur (5,78 → 9,71 points).

**En clair** : mélanger les réponses d'achat entre personnes du même groupe démographique
supprime quasiment toute la fuite d'identité et ne change presque rien aux moyennes ou aux
écarts entre groupes publiés — seul ce qui relie deux achats précis chez une même personne
s'efface. Mais ce lien perdu n'est pas gratuit : sur cet indicateur précis, le jumeau
défendu ressemble 68 % moins aux vraies réponses humaines qu'avant défense.

*Corrigé après relecture hostile du 12/09 : la moyenne des trois erreurs (1,47 point)
noyait un coût réel de 4,4 points sur les seules corrélations, et l'ancienne comparaison
« ce coût reste sous l'écart déjà présent entre jumeau et humains (5,8 pts) » comparait un
incrément à un niveau ; la colonne `erreur_correlations_hum` du CSV source montre que cet
écart passe en réalité de 5,78 à 9,71 après D4.*
