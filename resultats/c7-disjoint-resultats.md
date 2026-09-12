# C7, items disjoints : résultats

Préenregistré dans `c7-disjoint-preenregistrement.md`, calculé par `analyses/c7_disjoint.py`
(données : `c7-disjoint-partages.csv`, `c7-disjoint-nul.csv`, `c7-disjoint-resume.csv`).

## 1. Test principal, items disjoints
**Spearman = 0,969 en moyenne, médiane 0,972, IC 95 % [0,937 ; 0,993] sur 50 partages**
aléatoires des 60 items (A/B stratifiés ordinal/non-ordinal). 100 % des partages dépassent
0,7. **Prédiction (a) confirmée** : la relation ne s'effondre pas quand fidélité et fuite
sont mesurées sur des items totalement disjoints. Ce n'est donc pas la même computation
recyclée deux fois.

## 2. Nul de marge — le contrôle décisif
100 prédicteurs artificiels, gardant le masque de couverture réel et la seule marge
d'exactitude conditionnelle par personne (Bernoulli, aucune structure au-delà) : **rho nul
moyen = 0,984, 95e centile = 1,000**. **Le rho observé (0,969) NE dépasse PAS ce seuil — il
lui est même inférieur. Prédiction (b) réfutée.**

## 3. Point humain, position brute
Recalculé sans jamais le diviser par sa propre valeur : fidélité brute 0,303 et fuite brute
0,520, contre 0,154 et 0,067 pour le meilleur jumeau (JSON Persona GPT4.1). L'humain reste
devant sur les deux axes bruts : pas de saturation en haut de plage, testable et confirmée
hors normalisation circulaire.

## Verdict sur A1 : **tient en partie**
La corrélation survit à la disjonction des items (ce n'est pas l'identité arithmétique la
plus littérale visée par l'accusation), mais elle ne dépasse pas ce qu'un modèle sans
aucune structure individuelle — seulement une marge d'exactitude par personne — produit
déjà. Un simple axe de qualité globale (plus un prédicteur est précis en moyenne, plus il
fuit) suffit à expliquer la force du couplage observé, sans recours à une empreinte
individuelle distincte. **A1 doit être reformulée** : retirer l'implication « fidélité
individuelle spécifique cause la fuite » et la remplacer par « qualité globale et fuite
montent ensemble », plus faible et non réfutée par ce test. Limite : n = 12 configurations
rend Spearman grossier (le nul touche 1,000 par petits effectifs), donc ce verdict porte sur
l'ordre de grandeur, pas sur une troisième décimale.

**En clair** : le lien entre bien deviner une personne et pouvoir la retrouver dans la foule
est réel et robuste, mais rien ne montre qu'il faille deviner CETTE personne en particulier
plutôt qu'être simplement un bon prédicteur en général — la meilleure explication qui reste
debout est la plus ennuyeuse des deux.
