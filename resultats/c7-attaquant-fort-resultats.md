# C7 attaquant fort : resultats (12 septembre 2026)

Preenregistrement `c7-attaquant-fort-preenregistrement.md` (+ addendum volet 4), ecrit avant tout calcul.
Script `analyses/c7_attaquant_fort.py`, donnees `c7-attaquant-fort{,-segment}.csv`. Aucun identifiant, aucun appariement individuel.

## Volets 1 et 3 : attaquant naif contre attaquant fort
| Jeu | Attaque | top-1 | top-10 | TPR@0,1 % | TPR@1 % |
|---|---|---|---|---|---|
| Twin-2K-500 | naif (Hamming) | 20,69 % [19,1;22,5] | 42,7 % | 0,93 % | 3,04 % |
| Twin-2K-500 | A-MI (information, en echantillon) | 20,85 % | 43,6 % | 1,17 % | 3,31 % |
| Twin-2K-500 | **A-LLR hors pli** | **23,23 %** [21,5;25,0] | 46,6 % | 1,01 % | 4,28 % |
| Park et al., GSS | naif (Hamming) | 65,51 % [62,7;68,3] | 90,2 % | 8,47 % | 20,39 % |
| Park et al., GSS | A-MI (information, en echantillon) | 93,25 % | 99,1 % | 48,07 % | 64,70 % |
| Park et al., GSS | **A-LLR hors pli** | **90,40 %** [88,6;92,2] | 97,8 % | 44,37 % | 60,17 % |

Plafond humain (retest) : 81,6 % Twin, 96,7 % Park. A-MI bat A-LLR sur Park, mais ses poids sont calcules en echantillon (avantage declare au preenregistrement) : le chiffre retenu est A-LLR, strictement hors pli.

## Volets 2 et 4 : la defense D4 sous les deux attaquants
| Attaque contre D4 (permutation intra-segment, 40 items d'achat) | top-1 | top-10 |
|---|---|---|
| naif (Hamming) | 0,13 % | 1,13 % |
| A-MI | 0,05 % | 1,36 % |
| A-LLR recalibre sur les sorties defendues | 0,24 % | 1,12 % |
| ADAPTATIF S1 : les 20 items d'opinion laisses intacts | **0,29 %** | 1,21 % |
| ADAPTATIF S3 : invariants de segment (multiensemble preserve) | 0,05 % | 0,52 % |
| ADAPTATIF S1+S3 | 0,29 % | 1,21 % |

Divulgation d'attribut (S2) : la meilleure strategie designe le bon segment `S_gra` dans 7,7 % des cas, contre 6,8 % au hasard et 12,6 % en repondant toujours le segment le plus frequent (40 segments).
Aucune divulgation d'attribut n'est donc demontree : la regle triviale fait mieux que l'attaque.

## Verdict
[P1] REFUTEE sur Twin, TENUE sur Park. Twin : +12,2 % relatifs (20,69 -> 23,23 %), sous les 20 % annonces ;
notre taux naif y etait deja proche de ce qu'un adversaire mieux arme obtient, ce qui RENFORCE le chiffre
publie. Park : +38,0 % relatifs (65,51 -> 90,40 %), et en monde ouvert le TPR a 1 % de faux positifs TRIPLE
(20,4 -> 60,2 %) : notre attaque naive sous-estimait gravement la fuite, l'article doit publier 90 %, pas 65 %.
[P2] TENUE. D4 reste a 0,24 % sous A-LLR recalibre sur les sorties defendues, sous la barre de 1 %.
[P3] REFUTEE, dans le sens favorable a la defense : l'attaquant adaptatif, qui connait le mecanisme et sait quels items sont intacts, plafonne a 0,29 % et ne franchit jamais 1 %.

D4 tient donc contre un adversaire mieux arme ET informe : la fuite passe de 0,13 % a 0,29 % au pire, deux ordres de grandeur sous les 20,69 % non defendus. Reserve a porter dans l'article : ce residu vient
entierement des 20 items d'opinion laisses intacts, donc la garantie vaut pour ce decoupage, pas pour un
bloc non permute plus informatif.

**En clair** : face a un attaquant qui raisonne en vraisemblance plutot qu'en simple accord, notre chiffre
Twin bouge peu (21 -> 23 %) mais celui de Park explose (66 -> 90 %), donc nous sous-estimions la fuite chez
Park ; et notre parade D4 resiste, meme face a un adversaire qui sait exactement comment elle fonctionne.
