# C7, décompositions personnelles : préenregistrement (12 septembre 2026)

Écrit avant tout calcul. Étude de mécanisme sur `c7-contre-examen-2026-09-11.md` (jumeau
20,7 % contre PMM 0,23 % et B2 0,07 %, à exactitude comparable). Zéro appel de modèle,
lecture seule sur `data/`, aucun pid ni appariement individuel imprimé : taux agrégés
seuls. Reprend `c7_reidentification.items_communs/rangs_attaque/graine_nom/CONFIGURATIONS`
et `a2_commun.distance_hamming/bootstrap_personnes` tels quels ; `t1_baselines.calculer`
fournit B0 mode/tirage, B1 argmax, B2 argmax, PMM k=10. Prédicteurs : les 8 jumeaux
admissibles, les 5 baselines, le retest humain v1-3 (plafond), sur les 60 items communs
déjà définis par `c7_reidentification`.
**Définitions.** Partie prévisible = modalité modale de l'item (une fois, sur les humains
vague 4). Écart personnel = toute cellule qui en diffère. Part d'écarts = fraction de
cellules (personne × item) qui dévient. Justesse = P(prédicteur = vérité v4 | il dévie),
comparée au taux réel de déviation humaine P(vérité ≠ mode). Diversité = distance de
Hamming moyenne entre paires de personnes simulées.
**Trois régimes d'attaque** (mêmes garde-fous que c7_reidentification, pool = humains v4) :
1) complet (réponse brute) ; 2) prévisible seul (vecteur constant = mode, identique pour
tous, plancher attendu ≈ hasard) ; 3) écarts seuls (cellules non déviantes masquées à -1
des deux côtés).
**Test décisif.** Dans le régime écarts, sous-partition le test (jamais le pool humain,
fixe) en écarts corrects (= vérité v4) et écarts faux (≠ mode et ≠ vérité), attaqués
séparément contre le même pool d'écarts humains.
**Prédictions chiffrées.** (a) fuite écarts seuls ≥ 80 % de la fuite complète, jumeaux LLM
riches ; (b) fuite prévisible seule < 1 % (hasard ≈ 0,05 %) ; (c) fuite écarts faux seuls
strictement positive et hors IC du hasard pour au moins un jumeau riche : signature
personnelle même dans l'erreur, pas seulement le prix de la fidélité.
Garde-fous : permutation des candidats, bootstrap 2000 tirages, graine 20260912. Portée :
décrire un mécanisme déjà mesuré, pas une nouvelle relance.
