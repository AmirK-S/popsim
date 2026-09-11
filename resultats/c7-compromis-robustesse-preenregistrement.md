# C7-compromis, robustesse : préenregistrement des 4 contrôles

**Écrit le 12 septembre 2026, avant tout calcul.** Objection reçue : deux travaux publiés
(Platzer & Reutterer, arXiv 2104.00635 ; Adams et al., iScience 2025) et un troisième plus
direct (arXiv 2605.06835) rapportent que fidélité et fuite se **découplent** (le risque croît
alors que la qualité sature). Si notre rho tient au choix des 12 points, ils ont raison.

## Ajout : un 13e point, le retest humain
`humains vagues 1-3` attaquant `humains vague 4`, même méthode, jamais calculé avant ce
texte : fidélité fixée par construction (`part_du_plancher_humain` ≈ 1,0), fuite nouvelle.
Sans lui, la plage de fidélité s'arrête à 0,71 ; avec lui, elle va jusqu'au plancher humain,
seul test possible de saturation en haut de plage.

## Prédictions
1. **Retrait par famille (LLM, statistique, humain)** : le rho survit au retrait de la
   famille statistique et du point humain. **Point faible attendu** : à l'intérieur de la
   seule famille LLM (n=8, fidélité 0,56–0,71, plage étroite), rho peut chuter sous 0,7 sans
   invalider le résultat global — prédit ici, pas garanti.
2. **Jackknife** : aucun retrait individuel ne fait tomber rho sous 0,85 ; `B0 tirage`, déjà
   signalé comme artefact d'extrapolation en section 2 du rapport, ne porte pas la relation.
3. **Forme** : prédiction risquée, à double issue. Les 4 repères statistiques (fidélité
   -0,001 à 0,136) ont une fuite dont l'IC contiendra le hasard (0,0486 %) : un palier plat
   plausible sous fidélité ≈ 0,15. Au-delà, prédiction de hausse monotone jusqu'au retest
   humain, sans second palier en haut de plage (contre le découplage de 2605.06835).
4. **Stanford** : aucune fidélité de type chute-sous-permutation n'existe pour ce jeu ici ;
   seul l'ordre de richesse d'information (composite > entretien > enquête > démographique)
   sert de proxy ordinal. Prédiction : la fuite déjà publiée (`c7-stanford-resultats.md`)
   respecte cet ordre — ce n'est pas une réplique quantitative de rho.

## Limite déclarée
13 points au mieux : aucun test de forme n'aura la puissance d'un vrai test de rupture.
Résultat exploratoire, pas une seconde confirmation indépendante.
