# C7-échelle, résultats : le top-1 décroît, le ratio à la démographie croît

Préenregistré (`c7-echelle-preenregistrement.md` + addendum du 12 septembre), calculé par
`analyses/c7_echelle.py` (graine 20260911, 20 répétitions/N, IC 95 % bootstrap). Suite à un
examen critique indépendant, ce rapport **remplace** la version précédente : plus aucune
valeur au-delà d'environ N = 4 000 n'y figure. Sorties : `c7-echelle.csv`,
`c7-echelle-diagnostic.csv`, `c7-echelle.png`.

## 1. Résultat principal : la courbe mesurée, N = 50 à 2 058
| N | JSON Persona GPT4.1 | Demographics Only | PMM k=5 (démo) | ratio riche/demo |
|---|---|---|---|---|
| 50 | 53,2 % [50,0;56,3] | 18,7 % [17,0;20,5] | 5,5 % [4,1;7,0] | 2,8 |
| 250 | 38,1 % [37,0;39,3] | 7,9 % [7,2;8,5] | 1,0 % [0,8;1,2] | 4,9 |
| 1 000 | 25,7 % [25,1;26,3] | 3,3 % [3,1;3,5] | 0,29 % [0,23;0,35] | 7,7 |
| 2 058 | 20,7 % [20,7;20,8] | 2,14 % [2,12;2,16] | 0,13 % [0,12;0,14] | **9,7** |

**Le ratio riche/démographie croît avec N** (2,8 à 9,7 sur la plage mesurée) : le signal du
persona résiste mieux au bruit de population que la démographie seule. C'est solide et
suffisant en soi, sans aucune extrapolation.

## 2. Normalisation par le plafond humain (retest vagues 1-3, même pipeline)
Plafond mesuré ici : 93,4 % à N=50, **81,6 % à N=2 058** (identique au contre-examen du 11
septembre). Pour comparaison hors Twin : 96,8 % sur Stanford/GSS (`c7-stanford-resultats.md`).
| N | riche, part du plafond | démo, part du plafond | PMM, part du plafond |
|---|---|---|---|
| 50 | 57,0 % | 20,0 % | 5,9 % |
| 1 000 | 30,4 % | 3,9 % | 0,3 % |
| 2 058 | 25,4 % | 2,6 % | 0,2 % |

## 3. Pourquoi nous n'extrapolons pas au-delà de N ≈ 4 000
Diagnostic, pas un résultat : puissance et log, ajustées sur les 6 points mesurés, sont
évaluées côte à côte à N = 4 000 (2x le plus grand N mesuré, jamais plus loin). Sur le
jumeau riche, la log gagne la CV intra-domaine mais donne déjà 13,9 % contre 18,1 % pour la
puissance (écart x1,3 à seulement 2x). Sur Demographics Only et PMM, la log **s'effondre à
zéro** dès N = 4 000 alors que la puissance donne 1,5 % et 0,07 %. **Deux formes qui
s'accordent sur 50-2 058 divergent déjà nettement, ou totalement, à 2x cette plage : six
points ne suffisent pas à choisir une loi d'échelle.** Aucune valeur au-delà n'est publiée.

## 4. Limites assumées
Le modèle de Pitman-Yor (Rocher, Hendrickx, de Montjoye, *Nat. Commun.* 2025) n'a pas été
implémenté : sa formule (fonctions digamma inverses, rapports de Gamma) n'a pas pu être
vérifiée de façon fiable dans le temps imparti. Extrapoler honnêtement demanderait soit un
pool réellement plus grand que 2 058, soit une source externe donnant la distribution des
profils en population.

## En clair
Sur les tailles qu'on peut mesurer (jusqu'à 2 058), le jumeau riche reste 2,8 à 9,7 fois plus
dangereux que la démographie seule, et ce rapport grandit avec la taille du pool. On ne sait
pas, et on ne prétend pas savoir, ce qui se passe à un million.
