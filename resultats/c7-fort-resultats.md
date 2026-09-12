# C7-fort, résultats : modèle fort + appel par item ne suffisent pas à faire revenir la fuite
Préenregistré dans `c7-fort-preenregistrement.md`. Modèle `openai/gpt-4.1` (classe Twin),
recette « appel par item » de `c7_recette` reprise sans modification, 30 personnes x 60
items = 1800 appels, mêmes personnes/items que C7 (graine 20260912). Coût réel
**4,9949 USD** sur 5,00 autorisés (calibrage 5 appels compris). Taux de parse **100 %**.
Trois relances à concurrence décroissante (8→4→2→1) ont été nécessaires : ~1490 appels
ont d'abord échoué en HTTP 402 « in_flight_budget_exhausted » (réservation de crédit en
vol de la clé, pas un manque de solde réel — le solde restait > 3 USD à chaque fois) ;
les échecs à coût 0 ont été retirés de la trace puis réessayés, sans dépasser le plafond.
## Résultats (IC 95 %, bootstrap personnes, pool de 2 058 humains, hasard top-1 = 0,049 %)
| mesure | C7-fort (n=30) | Twin JSON Persona GPT-4.1 | nos jumeaux faibles |
|---|---|---|---|
| exactitude | 0,4722 [0,4361 ; 0,5050] | 0,574 | 0,394-0,455 |
| fidélité (part du plancher humain) | 0,1714 | 0,708 | 0,051-0,177 |
| top-1 | 0,00 % [0 ; 0] | 20,68 % | 0-0,83 % |
| top-10 | 0,00 % [0 ; 0] | — | 0-2,15 % |
## Position sur la courbe fidélité → fuite
Régression des 12 points de `c7-compromis.csv` (pente 0,1834, r=0,7854, `c7-courbe-gen`) :
à fidélité 0,1714, fuite prédite = 1,10 % IC95 % = [-9,15 ; 11,35]. Observé (0,00 %)
**tombe dans l'intervalle de prédiction**, loin au-dessus de la borne basse : le point ne
contredit PAS la courbe, il la confirme (8e point conforme, cf. les 7 de `c7-courbe-gen`).
## Verdict sur les trois prédictions
1. Exactitude > 0,55 : **rejetée** (0,4722, à peine au-dessus de nos jumeaux faibles).
2. Fidélité > 0,10 : **confirmée** (0,1714), mais à peine au-dessus de notre meilleur
   jumeau faible (deepseek-v4, 0,177) : le modèle fort n'a presque rien apporté ici.
3. Top-1 > 5 % : **rejetée**, et même en dessous de nos jumeaux faibles (0,83 % max) : 0 %.
## Exigence : la fuite ne revient pas — et cela NE contredit PAS la courbe
Un modèle bien plus fort (GPT-4.1 complet, ~5x le prix de mini) et la même granularité
d'appel que Twin ne font remonter ni la fidélité ni la fuite : la fidélité plafonne près
de celle de nos jumeaux les moins chers (~0,17 contre 0,71 chez Twin) et la fuite reste à
zéro. Ce n'est PAS le résultat majeur et contradictoire que l'hypothèse annonçait, car la
fidélité elle-même n'est jamais montée : le point suit la courbe, il ne la brise pas.
## En clair
Payer un modèle beaucoup plus cher et appeler item par item, comme Twin, ne suffit pas :
sans le format de persona complet de Twin (JSON entier, ~121 000 caractères, contre notre
texte tronqué à 8 000), la fidélité reste basse et la fuite reste nulle. Le facteur
limitant n'est donc ni le modèle ni la granularité d'appel, mais probablement le format
et la longueur du persona — et la fuite continue de suivre fidèlement la fidélité,
confirmant une fois de plus le compromis fidélité/fuite plutôt que la recette Twin.
Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
