# C7-courbe-gen, préenregistrement : le mystère de recette est-il juste un déficit de fidélité ?
**Écrit le 12 septembre 2026, avant tout calcul.** Aucun appel de modèle, lecture seule sur
`data/traces/c7-gen/` (déjà écrites) et sur `resultats/c7-compromis.csv`.

## Hypothèse
Nos 7 jumeaux régénérés (`c7-gen`) fuient 0 à 0,83 % contre 20,7 % chez l'autre équipe. Nous
avons présenté l'écart comme un mystère de recette. Hypothèse simple : il n'y a pas de
mystère, la fuite suit la fidélité déjà établie sur 12 points (rho = 0,958,
`c7-compromis-resultats.md`).

## Méthode
1. Fidélité : `analyses/t1_mesures.chute` (repris tel quel), chute d'exactitude sous
   permutation intra-segment `S_gra`, normalisée au plancher humain calculé sur les MÊMES
   personnes et items (60 items communs, mêmes que la fuite), 200 permutations, graine
   20260912.
2. Fuite : top-1 déjà dans `resultats/c7-gen-reidentification.csv` (calculé par
   `c7_reidentification.rangs_attaque`, non modifié).
3. Régression fuite ~ fidélité (moindres carrés) sur les 12 points de `c7-compromis.csv` ;
   intervalle de prédiction à 95 % pour chacune de nos 7 configurations, à leur fidélité
   mesurée.

## Prédiction chiffrée
Pour au moins 5 des 7 configurations, la fuite observée tombe dans l'intervalle de
prédiction à 95 % : question dissoute, la faible fuite s'explique entièrement par la
faible fidélité.

**Échec** : si pour une majorité (≥ 4/7) la fuite observée est NETTEMENT sous la borne
basse de l'intervalle (elles fuient moins que ne le prédit leur fidélité), la recette
compte vraiment et le mystère demeure — à documenter comme résultat en soi.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
