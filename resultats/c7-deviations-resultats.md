# C7, décompositions : résultats (12 septembre 2026)

Préenregistré dans `c7-deviations-preenregistrement.md`, calculé par `analyses/c7_deviations.py`
(60 items, graine 20260912). Déviation humaine de référence (vérité v4 ≠ mode) ≈ 50,1 % partout ;
hasard top-1 = 0,049 %. Régime « prévisible seul » : 0,03-0,07 % partout (≈ hasard). Régime
« écarts faux seuls » : **exactement 0,0 % pour tous**, y compris les jumeaux (voir verdict c).

| prédicteur | part écarts | justesse écarts | diversité | fuite complet | fuite écarts | écarts corrects |
|---|---|---|---|---|---|---|
| retest humain v1-3 (plafond) | 49,6 % | **68,5 %** | 0,568 | **81,6 %** | 2,34 % | 4,83 % |
| JSON Persona GPT4.1 | 47,4 % | **50,3 %** | 0,488 | **20,6 %** | 0,14 % | 0,56 % |
| JSON Persona mini | 60,4 % | 47,0 % | 0,480 | 12,1 % | 0,03 % | 0,59 % |
| Text Persona (5 variantes) | 42-61 % | 45-47 % | 0,45-0,52 | 5,5-13,1 % | 0,04-0,14 % | 0,41-0,61 % |
| Demographics Only | 67,0 % | 43,3 % | 0,405 | 2,14 % | 0,05 % | 0,29 % |
| B1 argmax | 35,7 % | 39,8 % | 0,479 | 0,31 % | 0,08 % | 0,47 % |
| B2 argmax | 26,7 % | 40,3 % | 0,383 | 0,08 % | 0,13 % | 0,27 % |
| PMM k=10 | 49,7 % | 39,1 % | 0,560 | 0,22 % | 0,08 % | 0,68 % |
| B0 tirage / mode | 50,2/0 % | 34,3 %/— | 0,569/0 | 0,15/0,03 % | 0,08/0,04 % | 0,25/0,04 % |

**(b) confirmée** : prévisible seul < 1 %, quasi hasard partout.
**(a) réfutée** : écarts seuls ne portent pas ≥ 80 % de la fuite (JSON 4.1 : 0,68 % en mixte,
2,7 % en corrects seuls) — masquer les cellules conformes réduit trop le nombre d'items
comparables ; la fuite a besoin de la réponse entière, pas des seuls écarts.
**(c) non tranchée, artefact** : un écart FAUX est par définition ≠ vérité, le vrai candidat a
donc toujours le pire accord possible sur ces cellules — la métrique ne peut mathématiquement
pas détecter de signature dans l'erreur. Le 0,0 % est un plancher de méthode, pas une preuve.
**Constat robuste non préenregistré** : à travers les 14 prédicteurs, la **justesse** des
écarts (pas leur fréquence ni la diversité) suit le classement de fuite ; PMM et B0 tirage
dévient et diversifient autant que le jumeau sans en avoir la justesse, et ne fuient pas.

**En clair** : dévier ne suffit pas, être divers non plus (PMM y arrive) ; ce qui identifie,
c'est d'avoir raison quand on dévie — et il faut la réponse entière, pas les écarts isolés.
