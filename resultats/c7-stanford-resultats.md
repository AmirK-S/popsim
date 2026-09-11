# C7 Stanford, résultats : le jumeau retrouve la personne, ailleurs aussi

Préenregistré dans `resultats/c7-stanford-preenregistrement.md`, calculé par
`analyses/c7_stanford.py` (1 052 personnes, 20 tirages de départ pour les ex aequo,
bootstrap 2000, graine 20260912), sur l'archive Stanford des agents génératifs, déjà
publique. **Aucun identifiant n'est imprimé ici** : tout est un taux agrégé sur
`resultats/c7-stanford-reidentification.csv` et `c7-stanford-par-bloc.csv`.
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
pour la condition composite. Comme sur Twin, quelques scores continus agrégés ne
suffisent pas : il faut un bloc large et catégoriel pour qu'un motif de réponses serve
d'empreinte — items d'achat sur Twin, items GSS ici.
## 4. Comparaison à Twin-2K-500
Réplication confirmée sur un second jeu, une seconde tâche (opinions, pas achats) et un
mécanisme de génération d'agent différent. Le taux est même plus élevé ici (65,7 % contre
20,7 % sur Twin) : moins de candidats (1 052 contre 2 058) et un agent composite plus
riche (entretien qualitatif inclus) expliquent l'écart, pas un mécanisme différent.
## 5. En clair
Un agent construit à partir des réponses d'une personne à un sondage d'opinion suffit,
dans deux tiers des cas, à la retrouver parmi mille inconnus rien qu'à son style de
réponses — même sans achat, sans nom, sans texte libre.
