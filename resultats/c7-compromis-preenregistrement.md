# C7, préenregistrement : la fuite est-elle le prix de la fidélité ?

**Écrit le 12 septembre 2026, avant tout calcul de corrélation ou de régression.** Étude de
risque de vie privée, aucun identifiant individuel, uniquement des taux agrégés.

## Unités (12 points)
Les 8 configurations admissibles de `twin-ab-audit-provenance-2026-09-11.md` (déjà notées
dans `c7-reidentification.csv` et `t1-classement.csv`), plus 4 repères statistiques :
`B0 tirage`, `B1 argmax`, `B2 argmax`, `PMM k=10`.

## Axes
Fidélité (primaire) : `part_du_plancher_humain` de `t1-classement.csv`, segment `S_gra`.
Secondaire : `exactitude_vraie`. Fuite : top-1 de ré-identification, cible vague 4, 60 items
communs, méthode de `c7_reidentification.py` reprise telle quelle (`items_communs`,
`rangs_attaque`, `bootstrap_personnes`, graine 20260911). **Nouveau ici** : même calcul pour
les 4 repères, codes venant de `t1_baselines.calculer`, restreints aux 60 items communs.

## Mesure primaire
Spearman(fidélité, fuite) sur les 12 points, IC par bootstrap de personnes (2000 tirages,
graine 20260911). Puis régression fuite ~ exactitude ; signe des résidus par groupe (LLM vs
statistique) à exactitude égale.

## Prédictions
Spearman ≥ 0,7. À exactitude égale, résidus positifs pour les 8 LLM, négatifs ou nuls pour
les 4 statistiques (déjà vu pour la chute dans `t1-mesure-de-personne-twin.md`). Contrôle
style vs fidélité, 8 LLM seuls (seuls à porter `i3b_tau_etoile`) : rang(résidu, tau*) nul si
le style seul n'explique pas le résidu.
## Limites
Douze points : corrélation imprécise, IC large attendu, pas de surinterprétation d'un rho
ponctuel. Les 4 points statistiques sont un calcul neuf, jamais vu avant ce texte.
