# C7-utilite-aval, preenregistrement (12 septembre 2026, avant tout calcul)

Question du relecteur : que casse D4 (melange intra-segment S_gra) dans une analyse
concrete de chercheur, sur les 40 items d'achat de `JSON Persona - GPT4.1` (2 058
personnes) ? Calcule par `analyses/c7_utilite_aval.py`, sur humains v4, jumeau brut, D4.

## Trois analyses (items de `c7_mecanisme.items_achat`, binaires)
A. Comparaison de groupes : ecart de proportion Hommes-Femmes sur l'item `1_Q295`, IC
   bootstrap personnes (2000 tirages, graine 20260912).
B. Regression MCO : `5_Q295` ~ genre (Homme=1) + age 65+ (dummy) + `1_Q295` + `2_Q295`.
C. ACP sur les 40 items d'achat : part de variance des deux premiers axes.
Genre/age viennent du segment `S_gra` deja charge, jamais recalcule.

## Mesures
Signe et significativite (|t|>1,96 ou IC hors zero) par analyse/condition ; % de
coefficients qui changent entre conditions ; ecart humains-brut vs brut-D4.

## Predictions chiffrees (issue inverse en regard)
1. Groupes : 0 % de signe/valeur different entre brut et D4 (identite mathematique) —
   inverse : la moindre difference refute.
2. Regression : les 2 coefficients demographiques gardent signe/significativite brut->D4 ;
   au moins 1 des 2 coefficients d'item change de signe ou perd sa significativite —
   inverse : les deux resistent aussi bien que les demographiques.
3. ACP : part de variance des 2 premiers axes chute d'au moins 30 % (relatif) brut->D4 —
   inverse : chute sous 10 %.
4. Point crucial : la degradation ajoutee par D4 (brut->D4, ACP) est plus PETITE que
   l'ecart deja present humains->brut — inverse : D4 aggrave au-dela de cet ecart.

Aucun pid, aucun appariement individuel. Lecture seule sur `data/`, aucun appel de modele.
