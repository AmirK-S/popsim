# C7-mecanisme, resultats : pourquoi les items d'achat identifient-ils ?
Preenregistre dans `resultats/c7-mecanisme-preenregistrement.md`, calcule par
`analyses/c7_mecanisme.py` (graine 20260911, bootstrap personnes 2000). Cible :
`JSON Persona - GPT4.1`, 2 058 personnes, 40 items d'achat (QID9, bloc *Product Preferences
- Pricing*) vs 20 items d'opinion, sur les 60 items communs de C7.
## H1, variance/entropie : **rejetee**
Les items d'opinion ont MOINS d'entropie humaine, pas plus... en fait l'inverse de ce que H1
predit sans corriger : entropie mediane opinion 2,10 bits contre 0,99 pour l'achat (achat
quasi binaire, opinion plus riche). Malgre cela, le sous-ensemble d'achat le plus proche en
entropie des 20 items d'opinion (appariement hongrois) garde un top-1 de **11,0 % [9,9 ; 12,3]**
contre **0,24 % [0,07 ; 0,46]** pour l'opinion : IC disjoints. Plus d'entropie sur l'opinion,
moins d'identification : la variance par item n'explique pas l'ecart.
## H2, sensibilite au prix recopiee : **soutenue (partiellement)**
Coherence de seuil (correlation de Spearman personne par personne entre son vecteur d'achat
et le taux d'achat moyen humain par item) : niveau moyen faible chez les humains (0,023) et
nul chez le jumeau (-0,003), mais **correlation personne a personne entre les deux series =
0,448 [0,409 ; 0,482]** sur 1 991 personnes. Le jumeau ne devient pas plus coherent en
moyenne, mais SA coherence varie d'une personne a l'autre comme celle du vrai repondant.
## H3, structure de matrice : **fortement soutenue**
Permuter, independamment par jumeau, l'ordre des 40 reponses d'achat (items encore alignes
cote humain) fait chuter le top-1 de **33,1 % [31,2 ; 35,2] a 0,046 % [0 ; 0,11]**, sous le
plancher hasard (0,049 %) et sous l'oracle du seul compte de « oui » du contre-examen
(0,29 %). Le motif exact, pris comme un bloc de 40 reponses alignees sur les bons produits,
est necessaire : aucun resume (compte, moyenne) ne le remplace.
## H4, stereotypie sur l'opinion : **rejetee**
Taux d'accord avec le mode du segment `S_gra` (LOO) sur les 20 items d'opinion : humains
37,5 % [36,9 ; 38,1], jumeau 36,2 % [35,6 ; 36,8]. Le jumeau ne colle PAS plus au cliche de
segment que les humains eux-memes ; si difference il y a, elle va dans l'autre sens. La
faible identification sur l'opinion ne vient pas d'un exces de stereotypie du modele.
## Explication la plus probable
Le jumeau capture, item par item sur les 40 questions d'achat, une correlation propre a la
personne avec sa vraie tendance a acheter (H2), et cette information n'est exploitable que
prise comme motif complet aligne sur les bons produits (H3) : casser soit l'alignement, soit
n'en garder qu'un resume detruit la fuite. Ni le volume d'information par item (H1) ni un
biais de cliche du modele sur l'opinion (H4) n'expliquent l'ecart entre achat et opinion.
**En clair** : le jumeau retrouve la personne parce qu'il devine correctement, produit par
produit, si CETTE personne precise achete ou non — pas parce que les questions d'achat sont
plus riches, ni parce que le modele repond au hasard des cliches sur les questions d'opinion.
