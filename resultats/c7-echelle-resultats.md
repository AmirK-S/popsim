# C7-échelle, résultats : le top-1 décroît, mais reste loin devant la démographie

Préenregistré (`c7-echelle-preenregistrement.md`), calculé par `analyses/c7_echelle.py`
(graine 20260911, 20 répétitions/N, IC 95 % bootstrap). Sorties : `c7-echelle.csv`,
`c7-echelle-extrapolation.csv`, `c7-echelle.png`.

## 1. Courbe empirique (top-1, IC 95 %)
| N | JSON Persona GPT4.1 | Demographics Only | PMM k=5 (démo) |
|---|---|---|---|
| 50 | 53,2 % [50,0;56,3] | 18,7 % [17,0;20,5] | 5,5 % [4,1;7,0] |
| 250 | 38,1 % [37,0;39,3] | 7,9 % [7,2;8,5] | 1,0 % [0,8;1,2] |
| 1 000 | 25,7 % [25,1;26,3] | 3,3 % [3,1;3,5] | 0,29 % [0,23;0,35] |
| 2 058 | 20,7 % [20,7;20,8] | 2,14 % [2,12;2,16] | 0,13 % [0,12;0,14] |

PMM (nouveau ici : régression démographique par item, donneur observé parmi k=5 voisins
en probabilité prédite) reste proche du hasard (0,05 % à N=2058).
## 2. Extrapolation indicative (deux modèles déclarés, pas le Pitman-Yor de l'article)
Le modèle log gagne la validation croisée sur le jumeau riche mais **diverge vers zéro dès
N ≈ 30 000** : gagner en intra-échantillon ne garantit rien hors échantillon. On retient
la **loi puissance**, stable, jamais nulle :

| N | JSON Persona GPT4.1 | Demographics Only | PMM k=5 | ratio riche/demo |
|---|---|---|---|---|
| 10 000 | 14,3 % [13,8;14,8] | 0,89 % [0,84;0,96] | 0,030 % | 16,1 |
| 100 000 | 8,0 % [7,5;8,5] | 0,24 % [0,21;0,27] | 0,0031 % | 33,9 |
| 1 000 000 | 4,5 % [4,1;4,9] | 0,063 % [0,05;0,08] | 0,0003 % | 71,5 |
## 3. Limites
Extrapolation à 5-500x au-delà du N mesuré : **indicative, pas une preuve**. Puissance et
log s'accordent de 50 à 2 058 mais divergent radicalement au-delà ; 6 points ne tranchent
pas à 1M. Pitman-Yor (Rocher/Hendrickx/de Montjoye) non implémenté, formule non vérifiable
dans la fenêtre impartie (préenregistrement section 2).
## En clair
Même sur un panel d'un million de personnes (extrapolé, pas mesuré), un jumeau riche
resterait ~70 fois plus dangereux qu'une fiche démographique : le risque décroît, il ne
s'effondre pas.
