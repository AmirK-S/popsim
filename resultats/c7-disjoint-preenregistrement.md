# C7, items disjoints : préenregistrement
Écrit le 12 septembre 2026, avant `analyses/c7_disjoint.py` et avant tout calcul. Répond à
l'objection : fidélité (chute sous permutation intra-segment, `t1_mesures.py`) et fuite
(rang de Hamming, `c7_reidentification.py`) seraient deux fonctions monotones de la même
marge par personne — une quasi-identité, pas un résultat empirique.
**Périmètre** : les 12 points de `c7-compromis-resultats.md` (8 configs LLM + 4 repères
statistiques), sur les 60 items communs de `c7_reidentification.items_communs`, segment
`S_gra`, vérité `humains vague 4`.
**Test principal, disjoint** : 50 partages aléatoires des 60 items en deux moitiés A/B,
stratifiés ordinal/non-ordinal (18/42). Sur A : chute BRUTE (exactitude vraie − exactitude
moyenne sous 40 permutations intra-`S_gra`), non normalisée par le plancher humain. Sur B :
top-1 moyen de ré-identification (Hamming, 3 tirages de départage) contre le pool des 2 058
humains v4. Spearman des 12 points par partage ; moyenne et IC 95 % (percentile) sur les 50.
**Nul de marge (contrôle décisif)** : par prédicteur, un prédicteur artificiel gardant le
masque de couverture réel et la marge d'exactitude conditionnelle par personne (Bernoulli
sur les cellules observées, faux uniforme sinon) — aucune structure au-delà du taux par
personne. 100 réplicats, items entiers (pas de partage), chaque réplicat donne un rho ; le
rho observé est comparé à cette distribution, pas à zéro.
**Prédictions chiffrées** : (a) rho disjoint moyen > 0,7 ; (b) rho observé > 95e centile du
nul de marge. Échec de l'une ou l'autre → identité de mesure, A1 retirée ou réduite à une
observation descriptive.
**Point humain** : recalculé exactement comme les 12 autres (chute brute et fuite brute sur
A/B), jamais divisé par sa propre valeur ; comparé en position brute, pas via « part du
plancher humain ».
**Éthique** : aucun identifiant, taux agrégés uniquement. Aucun script existant modifié,
aucun appel de modèle, aucun réseau pour le calcul.
