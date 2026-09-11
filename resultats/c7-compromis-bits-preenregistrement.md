# C7-compromis, bits : préenregistrement du contrôle d'unification

**Écrit le 12 septembre 2026, avant tout calcul.** Concilier trois mesures : le rho de
`c7-compromis-resultats.md` (0,958, LLM et statistiques confondus), le coût en bits
d'identité par point d'exactitude de `c7-bits-resultats.md` (0,29–0,47 LLM contre 0,068
pour B2, facteur 4–7), et les générateurs statistiques de `c7-generateur-resultats.md`
plafonnés à 0,476 d'exactitude, qui ne fuient qu'à 0,22–0,25 %.

## Hypothèse
Exactitude et fidélité individuelle sont deux choses différentes. Le coût en bits **par
point d'exactitude** varie fortement entre familles (une méthode statistique gagne de
l'exactitude sans rien apprendre sur l'individu) ; le coût en bits **par unité de fidélité
individuelle** (`part_du_plancher_humain`, déjà utilisée) devrait être à peu près constant.

## Calcul, sur les 12 prédicteurs de `c7-compromis.csv`
Bits repris tels quels de `resultats/c7-bits.csv` (colonne `bits`, borne dyadique +
Miller-Madow), **aucun recalcul**. Ratio 1 = bits / gain de points au-dessus de la modale
(= colonne `ratio_bits_par_pp` déjà publiée). Ratio 2 = bits / `part_du_plancher_humain`.
Dispersion : coefficient de variation (écart-type / moyenne) des deux ratios.

## Garde-fous déclarés avant de lire les chiffres
- Ratio 1 n'est pas défini quand le gain sur la modale est négatif ou nul (`B0 tirage`,
  `PMM k=10`) : déjà le cas dans `c7-bits-resultats.md`, non contourné ici.
- Ratio 2 est instable quand le dénominateur est proche de 0 (`B0 tirage`, fidélité
  ≈ −0,001) : rapporté à part, jamais utilisé seul pour trancher.
- Régression bits ~ fidélité : ordonnée à l'origine attendue proche de 0, cohérente avec
  les jumeaux régénérés de `c7-gen-resultats.md` (0 % de fuite à fidélité quasi nulle).

## Prédictions
1. CV(ratio 2) < CV(ratio 1), d'un facteur ≥ 2, sur les points où les deux sont définis.
2. Ordonnée à l'origine de bits ~ fidélité proche de 0 (à l'échelle de l'IC, pas
   nécessairement nulle exactement).
3. Si la prédiction 1 est réfutée : un surcoût propre aux LLM reste à expliquer, résultat
   différent mais publiable, à écrire franchement.

## Limite déclarée
12 points, aucun test formel de dispersion (n trop petit) : comparaison descriptive.
