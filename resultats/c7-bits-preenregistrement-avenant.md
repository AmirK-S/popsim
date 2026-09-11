# C7 bits, avenant au préenregistrement (12 septembre 2026, AVANT tout calcul de cette partie)

Demande du coordinateur après la courbe par nombre d'items de `c7-stanford-resultats.md` : l'entropie par item ne prédit pas le pouvoir d'identification (20 items d'opinion Twin à 2,10 bits identifient 0,24 %, 20 items GSS à 1,30 bit identifient 11,7 %). Le fichier principal `c7-bits-preenregistrement.md` (commit 7ddb1c1) reste inchangé ; cet avenant ajoute quatre points, écrits avant leur calcul. La partie 1 (bits d'identité, ratio, transportabilité) était déjà lancée : les résultats déjà obtenus ne sont pas modifiés par cet avenant.

## 5. Décomposition de l'information par item
Par item j, sur chaque jeu, trois quantités, toutes en bits et corrigées Miller-Madow :
- **H_j** : entropie humaine de l'item (déjà définie).
- **I_j** = Î(S_j ; H_j) : information mutuelle entre la sortie du jumeau et la réponse humaine.
- **I_cond_j** : information conditionnelle, c'est-à-dire ce que le jumeau apporte au-delà du démographique. Mesure principale, déclarée comme un **substitut par différence** et non comme une information conditionnelle formelle : I_cond_j = Î(S_j ; H_j) − Î(D_j ; H_j), où D est le prédicteur démographique du jeu (B1 argmax sur Twin, condition « démographique » sur Stanford). Contrôle de robustesse : information conditionnelle vraie Î(S_j ; H_j | cellule genre × âge), segment grossier (≤ 12 cellules) pour que les cellules restent peuplées ; si les deux divergent en signe ou d'un facteur 2, c'est signalé et la conclusion est suspendue.

## 6. Pouvoir d'identification d'un item et régression
- **Pouvoir d'identification** de l'item j : δ_j = a_j − c_j, où a_j = P(sortie du jumeau = réponse de la vraie personne) et c_j = Σ_c q_j(c)·p_j(c) = probabilité que la sortie coïncide avec la réponse d'un candidat pris au hasard. δ_j est l'excès de coïncidence sur lequel l'attaque de Hamming trie les candidats : c'est la grandeur mécaniquement responsable du rang, et elle est nulle pour un item où le jumeau ne fait que reproduire la marginale, quelle que soit son entropie.
- **Régression au niveau des items**, poids standardisés, IC bootstrap sur les items : δ_j ~ H_j + I_cond_j + a_j. Déclaré d'avance : δ_j = a_j − c_j est algébriquement lié à a_j, donc le modèle à trois régresseurs est rapporté pour mémoire et **la comparaison qui tranche est H_j contre I_cond_j** (régression à deux régresseurs, plus corrélations simples et partielles).
- Règle d'instabilité : si les IC des poids se recouvrent au point de ne pas ordonner les régresseurs, on rapporte les corrélations et le contraste descriptif achat/opinion, pas la régression.

## 7. Transport et mise à l'épreuve
- **Transport** : mêmes régressions sur Twin et sur Stanford ; on compare signes et amplitudes des poids standardisés.
- **Prédiction hors échantillon du top-1 de Stanford à k = 60**, sans utiliser aucun rang de Stanford. Modèle : le score d'accord de la vraie personne est une moyenne de k indicatrices de moyenne ā, celui d'un leurre de moyenne c̄ ; top-1 = P(la vraie dépasse les N−1 leurres), calculé par intégration normale des maxima. Un seul paramètre est **transporté depuis Twin** : le facteur d'inflation de variance φ = (écart type observé des scores de leurres) / (écart type binomial), qui encaisse la dépendance entre items. ā et c̄ sont ceux de Stanford, mesurés par item, sans attaque. Comparaison à la valeur observée de 34,0 %.

## 8. Prédictions chiffrées
1. Poids standardisé de I_cond_j sur δ_j ≥ 0,5 sur les deux jeux ; celui de H_j ≤ 0,2 en valeur absolue, IC couvrant 0.
2. Corrélation simple |r(H_j, δ_j)| ≤ 0,3 ; r(I_cond_j, δ_j) ≥ 0,6.
3. Transport : mêmes signes sur les deux jeux, rapport des poids de I_cond ≤ 2.
4. Prédiction du top-1 de Stanford à k = 60 dans ±10 points de 34,0 % (intervalle déclaré [24 ; 44]).
5. Anomalie Twin : δ médian des 20 items d'opinion ≤ 1/3 de celui des 40 items d'achat, malgré une entropie environ deux fois plus élevée.

## 9. Limites déclarées
Dépendance entre items non modélisée hors du facteur φ ; substitut par différence pour I_cond ; δ_j est la bonne grandeur pour une attaque par accord de Hamming et pour elle seule ; 60 et 177 items font de petits échantillons de régression (IC bootstrap sur les items rapportés partout) ; une prédiction réussie à ±10 points ne valide que l'ordre de grandeur du modèle, pas sa forme exacte.
