# C7, compromis : la fuite est-elle le prix de la fidélité ?

Préenregistré dans `resultats/c7-compromis-preenregistrement.md`, calculé par
`analyses/c7_compromis.py` (figure : `analyses/c7_compromis_figure.py`). 12 points : les 8
configurations admissibles de Twin-2K-500 plus 4 repères statistiques (`B0 tirage`,
`B1 argmax`, `B2 argmax`, `PMM k=10`), dont le top-1 de ré-identification est calculé ici
pour la première fois. Aucun identifiant individuel, taux agrégés seulement.

## 1. Corrélation fidélité / fuite
**Spearman = 0,958, IC 95 % [0,930 ; 0,993] (bootstrap joint, 2000 tirages, graine
20260911).** Prédiction (≥ 0,7) largement dépassée. L'ordre des 12 points par fidélité
(`part_du_plancher_humain`, `S_gra`) et par fuite (top-1) coïncide presque partout : les 4
statistiques occupent les 4 places les plus basses des deux côtés, `Demographics Only` la
5e, et les 7 jumeaux riches suivent dans le même ordre à deux inversions mineures près.

## 2. Fuite résiduelle à exactitude égale
Régression fuite ~ exactitude : pente 1,32, r = 0,724, p = 0,008, plus bruitée que le lien
avec la fidélité. **Les résidus ne se séparent pas proprement par groupe** : 3 des 4
statistiques sont sous la droite (`B2` −0,066, `B1` −0,047, `PMM` −0,012) mais `B0 tirage`
est au-dessus (+0,050), artefact d'extrapolation : sa fuite réelle (0,09 %) reste au niveau
du hasard, la droite prédit une valeur négative impossible à son exactitude la plus basse
(0,443). Côté LLM, 3 des 7 jumeaux sont sous la droite, 4 au-dessus. En moyenne, résidu LLM
+0,011, résidu statistique −0,019 : la direction prédite tient, pas la séparation annoncée.

## 3. Style idiosyncratique vs fidélité
Spearman(résidu, `i3b_tau_etoile`) sur les 8 LLM seuls = −0,119 (p = 0,78, n = 8) : aucun
lien détectable, mais n = 8 est trop petit pour trancher entre fidélité et style propre.

## Verdict
**Le compromis tient à l'échelle globale, mais pas au sens strict « à exactitude égale, tout
jumeau fuit plus que tout prédicteur ».** La fidélité individuelle prédit la fuite presque
parfaitement (rho 0,96) sur les 12 configurations, LLM et statistiques confondus : un seul
axe, la correspondance à la bonne personne, organise la quasi-totalité de l'ordre.
L'exactitude brute est un proxy plus faible et plus bruité, dont le résidu ne sépare pas
proprement les deux familles.

**En clair** : plus une méthode retrouve la bonne réponse de la bonne personne (pas
seulement une réponse plausible), plus elle permet de la retrouver dans la foule, que ce
soit un jumeau de langage ou un simple modèle statistique. Ce n'est pas un défaut propre aux
jumeaux LLM, c'est le prix de toute méthode qui vise l'individu plutôt que le groupe.

## 4. Robustesse (préenregistré dans `c7-compromis-robustesse-preenregistrement.md`,
calculé par `analyses/c7_compromis_robustesse.py`, figure `c7-compromis-robustesse.png`)

**Objection reçue** : Platzer & Reutterer (arXiv 2104.00635) et Adams et al. (iScience
2025) montrent que fidélité et risque peuvent être rendus séparables ; arXiv 2605.06835
rapporte un découplage direct, le risque qui continue de croître quand la qualité sature.
Quatre contrôles, plus un 13e point jamais calculé avant ce texte : le retest humain
(vagues 1-3 attaquant la vague 4) donne une fuite de **81,6 % [79,9 ; 83,2]**, fidélité 1
par construction.

- **Retrait par famille** : sans les statistiques (n=9, LLM+humain) rho = 0,983
  [0,967 ; 1,0] ; sans le retest humain (n=12, l'analyse d'origine) rho = 0,958
  [0,930 ; 0,993] ; **à l'intérieur de la seule famille LLM (n=8, fidélité 0,56–0,71,
  plage étroite)** rho = **0,976 [0,952 ; 1,0]** — tient, contrairement à ce qu'une plage
  étroite laissait craindre. Seul le retrait total des LLM (n=5, 4 statistiques + humain)
  fait chuter rho à 0,50 [0,10 ; 0,90], non significatif : les 4 statistiques, tassées près
  du hasard, n'ont pas d'ordre interne fiable entre elles à si petit effectif.
- **Jackknife** : rho varie seulement de 0,958 à 0,986 selon le point retiré un par un ;
  sans `B0 tirage` (l'artefact d'extrapolation signalé en section 2), rho = 0,972. Aucun
  point isolé ne porte la relation.
- **Forme** : 3 des 4 statistiques (`B0`, `B2`, `PMM`) ont un IC de fuite qui contient le
  hasard (0,049 %) ; `B1 argmax` est légèrement au-dessus. Un modèle à deux régimes
  (plancher puis droite) réduit la somme des carrés de 98 % (0,318 → 0,006) par rapport à
  une droite unique : la relation est plate près du hasard, puis monte. **Et surtout, en
  haut de plage, pas de second palier** : le retest humain (fidélité ≈ 1) fuit 3,95 fois
  plus que le meilleur jumeau (81,6 % contre 20,7 %) — la qualité ne sature pas avant que
  le risque s'arrête, ils montent ensemble jusqu'au bout. Sur Stanford
  (`c7-stanford-resultats.md`, lecture seule, pas de fidélité chute-sous-permutation
  disponible pour ce jeu) : composite 65,7 % > entretien 44,7 % > enquête 20,6 % >
  démographique 2,3 %, l'ordre attendu, et le retest humain (96,8 %) dépasse là aussi
  largement la meilleure condition riche — même absence de saturation en haut.
- **Verdict robustesse** : contre les trois références, **le couplage tient sur nos
  données** : il survit au retrait de chaque famille prise séparément (sauf en écartant les
  LLM, où il ne reste plus assez de variance utile), à aucun point isolé, et surtout il ne
  sature pas en haut de plage — l'inverse du découplage rapporté par arXiv 2605.06835.

## 5. Bits d'identité par unité de fidélité (préenregistré dans
`c7-compromis-bits-preenregistrement.md`, calculé par `analyses/c7_compromis_bits.py`,
bits repris tels quels de `c7-bits.csv`)

**Hypothèse testée, et réfutée** : le coût en bits par point d'exactitude varie fortement
entre familles (0,29–0,47 LLM contre 0,068 pour B2, déjà publié) ; celui par unité de
fidélité individuelle devrait, lui, être à peu près constant.

**Comparaison corrigée, à échantillon égal.** La comparaison publiée auparavant —
CV(bits/fidélité) = 0,507 sur 12 points contre CV(bits/point d'exactitude) = 0,357 sur les
9 points où ce second ratio est défini — opposait deux dispersions calculées sur deux
échantillons différents, ce qui n'est pas valide. En restreignant CV(bits/fidélité) aux
9 points où les deux ratios sont définis (mêmes 9 prédicteurs, `analyses/c7_compromis_bits.py`,
écart-type d'échantillon comme dans le script) : **CV(bits/fidélité) = 0,436** contre
**CV(bits/point d'exactitude) = 0,357**. La conclusion (le ratio bits/fidélité reste plus
dispersé) survit, mais l'écart fond : facteur 0,82 (contre 0,70 annoncé sur les échantillons
disparates), soit un ratio 22 % plus dispersé et non 42 %.

La régression bits ~ fidélité passe raisonnablement près de l'origine (ordonnée −0,31 sur les
12 points, −1,13 avec le retest humain ajouté ; `B0 tirage` lui-même est quasi à l'origine,
bits ≈ −0,002 pour fidélité ≈ −0,001), donc « pas de fidélité, pas de fuite » tient. **Mais
la loi d'un coût constant par unité de fidélité ne tient pas** : ce ratio va de 1,47
(Demographics Only) à 5,02 (JSON Persona GPT4.1) chez les configurations issues de LLM,
contre 0,68–1,53 pour les 3 statistiques définies. La corrélation de rang (section 1)
survit à tous les contrôles, et un surcoût en bits par unité de fidélité, déjà documenté par
`c7-bits-resultats.md` en points d'exactitude, reste réel sur cet échantillon — mais avec
n=7 configurations LLM contre 3 statistiques définies, et sans mécanisme identifié, il ne
doit **pas être attribué aux « LLM » comme famille** : il reste, en l'état, **un surcoût non
expliqué**, à ne pas confondre avec une propriété démontrée de cette famille de modèles.

*Corrigé après relecture hostile du 12/09 : la comparaison 0,507 (n=12) vs 0,357 (n=9)
comparait deux échantillons différents ; recalculée sur les mêmes 9 points, elle donne
0,436 contre 0,357 (facteur 0,82, pas 0,70) — la conclusion tient, l'écart est plus faible
qu'annoncé, et le surcoût n'est plus attribué aux « LLM » mais décrit comme non expliqué.*
