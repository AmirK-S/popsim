# C7 Stanford, résultats : le jumeau retrouve la personne, ailleurs aussi

Préenregistré dans `resultats/c7-stanford-preenregistrement.md`, calculé par
`analyses/c7_stanford.py` (1 052 personnes, 20 tirages de départ pour les ex aequo,
bootstrap 2000, graine 20260912), sur l'archive Stanford des agents génératifs, déjà
publique. **Aucun identifiant n'est imprimé ici** : tout est un taux agrégé sur
`resultats/c7-stanford-reidentification.csv`, `-par-bloc.csv`, `-courbe-items.csv` et
`-entropie.csv`.
## 1. Ré-identification, cible = humains de vague 1, 1 052 candidats

| bloc | condition | top-1 | IC 95 % | top-10 | rang médian |
|---|---|---|---|---|---|
| GSS (177 items) | composite (enquête + entretien) | **65,7 %** | [62,7 ; 68,6] | 90,2 % | 1 |
| GSS | entretien seul | 44,7 % | [41,8 ; 47,5] | 80,2 % | 2 |
| GSS | enquête seule | 20,6 % | [18,2 ; 23,0] | 53,1 % | 8,9 |
| GSS | démographique seul | 2,26 % | [1,44 ; 3,16] | 14,7 % | 96 |
| GSS | humains vague 2 (retest) | 96,8 % | [95,7 ; 97,7] | 98,4 % | 1 |
| Jeux économiques (5 scores) | meilleur agent (enquête) | 0,20 % | [0,0 ; 0,5] | 1,2 % | 497 |
| Big Five (5 traits) | meilleur agent (entretien) | 1,05 % | [0,5 ; 1,7] | 5,1 % | 202 |

Hasard : top-1 = 0,095 %, top-10 = 0,95 %.
## 2. Comparateurs et verdict
Critère préenregistré : top-1 ≥ 10 % ET ≥ 5 fois le démographique seul, pour au moins une
condition riche. **Rempli très largement** : composite atteint 65,7 %, soit 29 fois le
démographique (2,26 %) et 691 fois le hasard. Trois des quatre conditions riches du GSS
dépassent 10 %. **On fonce confirmé, marge bien plus large que prévu.**
## 3. Quel bloc porte l'identification
Le GSS (bloc catégoriel riche, 177 items) porte presque toute l'identification ; jeux
économiques et Big Five (5 dimensions continues chacun) restent au ras du hasard, même
pour la condition composite. Il faut un bloc large et catégoriel pour qu'un motif de
réponses serve d'empreinte — items d'achat sur Twin, items GSS ici.

## 4. Contrôle demandé : l'écart avec Twin vient-il du nombre d'items ?
Twin n'utilise que 60 des 108 items communs ; Stanford GSS en a 177. Courbe top-1 de la
condition composite, k items GSS tirés au hasard sans remise, 20 tirages par k (IC =
2,5ᵉ/97,5ᵉ centile des tirages) :

| k items | top-1 moyen | IC (dispersion inter-tirages) |
|---|---|---|
| 10 | 5,2 % | [1,6 ; 17,4] |
| 20 | 11,7 % | [3,9 ; 26,8] |
| 40 | 22,1 % | [13,1 ; 31,6] |
| **60** | **34,0 %** | **[23,5 ; 51,5]** |
| 100 | 49,9 % | [40,6 ; 59,4] |
| 177 (bloc entier) | 65,5 % | — |

**Point comparable à Twin, k = 60 : Stanford 34,0 % contre Twin (JSON Persona GPT4.1)
20,7 %.** Le nombre d'items explique une partie de l'écart brut (65,7 % à 177 items tombe
à 34,0 % à 60 items égalisés), mais pas tout : à k égal, Stanford reste 1,6 fois au-dessus
de Twin, IC large vu seulement 20 tirages. Questionnaires et populations différent :
comparaison à nombre d'items égal, pas une réplique exacte.

## 5. Contrôle d'entropie
Entropie de Shannon médiane par item, humains, même estimateur des deux côtés (bits) :
Stanford GSS (177 items) = **1,30**, Twin (60 items communs C7) = **0,99**. Stanford est
un peu plus informatif par item, ce qui explique une part supplémentaire, mais modeste, de
l'écart résiduel de la section 4 : l'écart d'entropie (+31 %) est bien plus petit que
l'écart de top-1 à k égal (+64 %).

## 6. Les deux jeux sont-ils compatibles ? GSS Stanford contre opinion Twin
Sur Twin (`resultats/c7-mecanisme-resultats.md`), les 20 items d'opinion, pourtant plus
riches en entropie (2,10 bits médian) que le GSS Stanford (1,30), n'identifiaient presque
personne : top-1 = 0,24 %. Sur Stanford, 20 items GSS tirés au hasard, moins informatifs
par item, atteignent 11,7 % — environ 49 fois plus, à effectif d'items égal et entropie
par item inférieure. **Ni le nombre d'items ni l'entropie par item ne peuvent donc
expliquer pourquoi les items d'opinion Twin échouent alors que les items GSS Stanford
réussissent.** Hypothèse la mieux étayée, à confirmer par une réplique dédiée : les items
GSS forment un bloc cohérent d'attitudes corrélées entre elles (mêmes familles de sujets,
mêmes axes idéologiques), qui compose une empreinte multi-item stable, alors que les 20
items d'opinion Twin sont un échantillon plus étroit et plus hétérogène de sujets, sans
cet effet de bloc — cohérent avec le résultat H3 de `c7-mecanisme-resultats.md` (Twin) :
c'est la structure du motif pris en bloc qui identifie, pas le contenu informationnel item
par item.

## 7. Comparaison à Twin-2K-500
Réplication confirmée sur un second jeu, une seconde tâche (opinions, pas achats) et un
mécanisme de génération d'agent différent. Le taux brut est plus élevé ici (65,7 % contre
20,7 %), mais la section 4 montre qu'une bonne partie de cet écart vient du nombre d'items
(177 contre 60) et, dans une moindre mesure, de l'entropie par item (section 5) ; à
nombre d'items égal l'écart résiduel (34,0 % contre 20,7 %) reste net mais nettement plus
modeste que l'écart brut.

## 8. En clair
Un agent construit à partir des réponses d'une personne à un sondage d'opinion suffit,
dans deux tiers des cas, à la retrouver parmi mille inconnus rien qu'à son style de
réponses. Une bonne part de l'écart avec Twin vient du nombre de questions utilisées, pas
d'une fuite radicalement différente ; mais à nombre de questions égal, les questions
d'opinion du GSS restent bien plus identifiantes que celles de Twin — un souci d'écriture
des questions, pas seulement de quantité.
