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
