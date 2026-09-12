# C7-courbe-gen, résultats : le mystère de recette se dissout
Préenregistré dans `c7-courbe-gen-preenregistrement.md`, calculé par
`analyses/c7_courbe_gen.py` (fidélité : `t1_mesures.chute`, tel quel ; fuite : reprise de
`c7-gen-reidentification.csv`, produite par `rangs_attaque` non modifié). Aucun identifiant
individuel.
## 1. Fidélité et fuite de nos 7 jumeaux régénérés
| condition | fidélité (plancher humain) | exactitude | fuite top-1 | fuite prédite | IC 95 % | résidu |
|---|---|---|---|---|---|---|
| llama31-8b/R1/t0 | 0,051 | 0,394 | 0,00 % | −1,12 % | [−11,8 ; 9,6] | +0,011 |
| llama31-8b/R2/t0 | 0,055 | 0,398 | 0,00 % | −1,04 % | [−11,7 ; 9,6] | +0,010 |
| qwen37-flash/R1/t0 | 0,117 | 0,415 | 0,23 % | 0,11 % | [−10,3 ; 10,5] | +0,001 |
| qwen37-flash/R2/t0 | 0,139 | 0,412 | 0,00 % | 0,50 % | [−9,8 ; 10,8] | −0,005 |
| deepseek-v4/R1/t0 | 0,177 | 0,455 | 0,83 % | 1,19 % | [−9,0 ; 11,4] | −0,004 |
| deepseek-v4/R2/t0 | 0,163 | 0,449 | 0,50 % | 0,94 % | [−9,3 ; 11,2] | −0,004 |
| qwen37-flash/R1/t1 | 0,070 | 0,420 | 0,00 % | −0,77 % | [−11,4 ; 9,8] | +0,008 |
Régression fuite ~ fidélité, 12 points de `c7-compromis.csv` : pente 0,183, r = 0,785,
p = 0,002 (rho Spearman de référence = 0,958). Intervalle de prédiction à 95 % par point.
## 2. Verdict
**7/7 dans l'intervalle de prédiction, aucun sous la borne basse.** Seuil préenregistré
(≥ 5/7) largement atteint : **question dissoute.** Fidélité de nos jumeaux (0,05–0,18)
proche des repères statistiques naïfs (B1/B2/PMM, 0,10–0,14) et bien en deçà des jumeaux
riches de l'autre équipe (0,61–0,71) : la fuite quasi nulle est le point attendu à ce
niveau de fidélité, pas une anomalie de recette. La droite prédit une fuite négative aux
fidélités les plus basses (même artefact d'extrapolation que `B0 tirage` dans
`c7-compromis-resultats.md`), sans conséquence : les résidus restent ≤ 0,011 point.
## En clair
Nos jumeaux bon marché ne retrouvent presque personne parce qu'ils sont peu fidèles à la
personne, pas parce que leur recette serait mauvaise : au même niveau de fidélité que
n'importe quelle méthode, LLM ou statistique, on observe la même fuite quasi nulle. Le
« mystère de recette » disparaît de l'article et devient une confirmation de plus du
compromis fidélité/fuite.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
