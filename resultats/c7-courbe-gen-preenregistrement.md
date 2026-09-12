# C7-courbe-gen, préenregistrement : le mystère de recette est-il un déficit de fidélité ?
**Écrit le 12 septembre 2026, avant tout calcul.** Aucun appel de modèle, lecture seule sur
`data/traces/c7-gen/` (déjà écrites) et `resultats/c7-compromis.csv`.
## Hypothèse
Nos 7 jumeaux régénérés fuient 0 à 0,83 % contre 20,7 % chez l'autre équipe, présenté comme
un mystère de recette. Hypothèse simple : pas de mystère, la fuite suit la fidélité déjà
établie sur 12 points (rho = 0,958, `c7-compromis-resultats.md`).
## Méthode
1. Fidélité : `t1_mesures.chute` (repris tel quel) sur `S_gra`, normalisée au plancher
   humain calculé sur les mêmes personnes et 60 items (ceux de la fuite), 200 permutations,
   graine 20260912.
2. Fuite : top-1 déjà dans `c7-gen-reidentification.csv` (`rangs_attaque`, non modifié).
3. Régression fuite ~ fidélité (moindres carrés) sur les 12 points de `c7-compromis.csv` ;
   intervalle de prédiction à 95 % pour nos 7 configurations, à leur fidélité mesurée.
## Prédiction chiffrée
Pour au moins 5 des 7 configurations, la fuite observée tombe dans l'intervalle de
prédiction à 95 % : question dissoute.
**Échec** : si pour ≥ 4/7 la fuite observée est nettement sous la borne basse (elles fuient
moins que ne le prédit leur fidélité), la recette compte vraiment, mystère maintenu.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
