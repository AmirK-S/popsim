# C7, synthétiseur ajusté sur la cible : préenregistrement (12 septembre 2026)
**Écrit avant tout calcul.** `c7_generateur.py` a montré que des générateurs conditionnés
seulement sur le contexte (jamais les 60 items cibles) plafonnent à 0,476, loin de la cible
0,590 : la comparaison n'était donc pas appariée en exactitude. Ce script lève cette
contrainte en autorisant le synthétiseur à voir le bloc cible lui-même.

## 1. Méthode (`analyses/c7_synth_ajuste.py`)
CART séquentiel façon synthpop : `sklearn.tree.DecisionTreeClassifier`, un arbre par item
et par pli (5 plis de `t1_baselines.plis`), conditionné sur le profil (14 démographies,
`a2_commun.encodeur_demographies`) et sur les items déjà traités dans la chaîne (valeurs
vraies à l'entraînement, valeurs déjà générées hors pli en test). Tirage stochastique dans
`predict_proba`, jamais l'argmax. `synthpop`/`ctgan`/`sdv` : absents de l'environnement,
non testés, comme anticipé.

## 2. Limite déclarée à l'avance
Ce synthétiseur est **ajusté sur les réponses cibles elles-mêmes** (via les autres items du
bloc, en validation croisée hors personne) : il voit une information que ni le jumeau LLM
ni B1/B2/PMM/G-LR/G-copule n'ont. Ce n'est **pas un comparateur à information égale**, mais
un comparateur de plafond : à exactitude appariée, fuit-il autant qu'un jumeau ?

## 3. Calibration et attaque
Balayage de `min_samples_leaf` (grille ≈ 1 à 320), cible 0,590 ± 0,01 sur les 60 items.
Attaque : `c7_reidentification.rangs_attaque`, non modifiée, pool = 2 058 humains vague 4,
5 tirages finaux, IC par `bootstrap_personnes`. Fidélité individuelle : chute d'exactitude
sous `a44_commun.permuter_intra` (segment S_gra), non modifiée.

## 4. Les trois issues
- (a) top-1 proche de 20,7 % → la spécificité LLM tombe, l'article doit dire « fidélité »,
  jamais « LLM ».
- (b) top-1 << 20,7 % à exactitude égale → spécificité LLM confirmée même appariée, résultat
  fort.
- (c) cible 0,590 non atteinte malgré l'ajustement → limite à documenter, aucune conclusion.
