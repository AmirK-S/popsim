# Instabilité du pilote R6 DeepSeek

## Portée

Cette analyse exploratoire porte uniquement sur les deux passes déjà présentes de dix
cellules F1 pour `deepseek/deepseek-v4-flash`, fournisseur DigitalOcean. Elle ne reclasse
aucun résultat comme confirmatoire et n'ajoute aucun test aux familles enregistrées. Les
vingt réponses sont valides au parse et les dix cellules sont appariées sans perte.

Le critère préenregistré de déterminisme échoue: 1 distribution sur 10 est identique entre
les passes, contre un minimum de 7. Le modèle doit donc rester marqué non déterministe si
la campagne est poursuivie.

## Amplitude observée

La distance de variation totale, calculée cellule par cellule entre les deux passes, a une
moyenne de **0,053**, une médiane de **0,050** et un maximum de **0,100**. Un bootstrap
exploratoire de 2 000 rééchantillonnages des dix cellules, graine 20260910, donne un IC
percentile à 95 % de **[0,033; 0,074]** pour la moyenne. Cet intervalle décrit ce petit
échantillon; ce n'est ni un test ni un intervalle confirmatoire.

Les dix cellules appartiennent aussi au contrôle local de 40 cellules. Ce contrôle donne
40 distributions identiques sur 40 et une TV moyenne et maximale de 0 entre les voies
`chat` et `completion`; sur les dix cellules appariées, la référence locale vaut donc aussi
0. Ce contrôle mesure surtout l'équivalence des voies sur un serveur local déterministe. Il
ne constitue pas une estimation indépendante de la variabilité de DeepSeek.

Le plancher humain vague 1 contre vague 2, recalculé sur les mêmes dix couples item-camp,
a une TV moyenne de **0,0282**, médiane de **0,0304** et maximale de **0,0482**. La TV du
pilote est supérieure sur 8 cellules sur 10. Le rapport des moyennes est **1,88** et la
différence appariée moyenne **+0,0248**, avec IC bootstrap exploratoire
**[+0,0040; +0,0449]**. Le plancher humain A2 de 1,009 est un rapport distinct et ne doit
pas être comparé directement à ces TV.

Six cellules ont un déplacement maximal d'au moins 5 points de pourcentage entre
modalités. Neuf sur dix dépassent un point, donc les différences ne se réduisent pas à la
seule représentation en pourcentages entiers. Les ensembles de modes sont identiques dans
5 cellules sur 10 et se recouvrent dans 7 sur 10. Le classement complet des modalités,
égalités comprises, est identique dans 4 sur 10; la médiane des corrélations de rang de
Spearman par cellule est néanmoins 0,955. La structure générale reste souvent proche, mais
plusieurs sorties changent de mode ou d'ordre de façon substantielle.

## Incidence possible sur A1 à A4

A1 pourrait varier car l'indice de Gini-Simpson change entre passes: la moyenne des valeurs
absolues de ce changement est 0,0397 et le maximum 0,1422. Les dix cellules, dispersées
entre camps et identités, ne couvrent toutefois aucun agrégat A1 complet.

A2 exige les camps gauche et droite du même item et de la même identité. A4 exige les deux
identités du même couple item-camp. Le pilote ne contient aucune paire complète de l'un ou
l'autre type; aucun A2 ou A4 pilote n'est donc calculable. A3 n'est pas une quantité R6
enregistrée. L'effet sur H1 à H4 reste indéterminé. Pour A4, le constat renforce seulement
la nécessité du plancher machine propre au modèle et de la règle de lisibilité déjà prévue.

## Options prospectives testables

| option | protocole testable | coût indicatif | validité |
|---|---|---:|---|
| Moyenne de `R` répétitions | Fixer `R` avant reprise, par exemple `R=3`, moyenner les distributions par cellule et conserver les répétitions brutes. Pour 1 210 cellules analytiques plus les 40 du plancher, cela représente 3 670 futurs appels. | Environ 0,0604 USD au coût moyen observé; plafond pire cas 3,67 USD à 0,001 USD par appel. | Estime une réponse moyenne du couple modèle-fournisseur, mais change l'estimand et le plan. Un addendum prospectif et un budget frais seraient requis. |
| Graine et fournisseur fixes | Conserver DigitalOcean, déjà imposé, ajouter une graine API fixe documentée, puis répéter un nouveau lot scellé et appliquer le même seuil 7/10. | Vingt appels: environ 0,000329 USD au coût observé, plafond 0,02 USD. | Valide seulement si l'API et le fournisseur attestent et respectent la graine. Une graine ignorée ne corrige rien. Cette option modifie la requête et exige une clarification prospective. |
| Abandon du modèle | Ne lancer ni campagne ni plancher DeepSeek. | 0 USD supplémentaire. | Évite de présenter une réponse instable comme caractéristique unique. DeepSeek étant une ligne ouverte descriptive, cet abandon ne modifie pas les familles confirmatoires H1 à H4, mais réduit la couverture descriptive. |

Les coûts sont des projections à partir des 20 appels observés, coût total 0,0003289566 USD,
et non des autorisations de dépense. La première option dépasse le pilote enregistré; la
deuxième nécessiterait elle aussi un nouveau cadre prospectif puisque les vingt appels du
pilote actuel sont déjà consommés.

## Fichiers et calculs

Sources: les deux traces `r6-deepseek-deepseek-v4-flash-q4-r6v2-essai1.jsonl` et
`essai2.jsonl`, la liste scellée `r6-essai-cellules.txt`, le contrôle local
`r6-voie-chat.md` et le référent humain déjà utilisé par R1. La TV est
`0,5 × somme |p1-p2|`; les modes sont comparés comme ensembles afin de conserver les
égalités. Le CSV joint contient les vingt distributions et tous les diagnostics par cellule.

Aucun appel réseau, modèle, GPU, GO ou nouvelle donnée R6 n'a été utilisé.
