# Contrôle A1 : item ou personne derrière l'AUC 0,65 ?

Écrit le 11 septembre 2026, avant tout calcul. Doute (`idees-A-atouts-2026-09-11.md` idée 1,
`tri-idees-2026-09-11.md` contrôle A1) : vague 4 = retest à 2 semaines, Demographics Only
atteint déjà 0,607 d'AUC ; le signal de P3 (désaccord jumeau/passé → changement) pourrait
n'être que volatilité d'item et propension personne, pas une connaissance individuelle.

Données et cellules : identiques à `memoire_twin.py` (8 configurations admissibles, périmètre
propre à chacune). Cible `changée` = code vagues 1-3 ≠ code vague 4. Prédicteur testé
`désaccord` = jumeau ≠ code vagues 1-3.

Référence : régression logistique de `changée` sur effets fixes d'item (indicatrices, communes
à tous les plis) + propension individuelle au changement par personne, en excluant l'item
courant (leave-one-item-out) — pas d'effet fixe personne, qui ne se généralise pas à une
personne inédite. Modèle testé : référence + `désaccord`.

Validation croisée : 5 plis par personne (aucune coupée entre plis), graine 20260909. Mesure
primaire : gain d'AUC hors échantillon (prédictions out-of-fold empilées), IC par bootstrap
personnes × items apparié (mêmes poids pour les deux modèles), 1000 réplicats, même graine.

Prédictions : gain < +0,01 pour les 7 jumeaux à persona riche ; gain ≈ 0 pour Demographics
Only. Seuil « signal réel » : gain ≥ +0,02 avec borne basse d'IC > 0. Sous ce seuil, P3 est
confondue avec la volatilité déjà connue (item + personne), pas un signal de connaissance
individuelle.
