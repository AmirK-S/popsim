# C7-échelle, préenregistrement : le top-1 tient-il à grande échelle ?

**Écrit le 12 septembre 2026, avant tout calcul.** Réponse à l'objection prévisible sur
`resultats/c7-resultats.md` (top-1 = 20,7 % sur 2 058 candidats) : « à l'échelle d'un panel
national, ce taux s'effondre ». Étude de risque de vie privée sur Twin-2K-500, déjà public.
Aucune identité ni pid publié, seuls des taux agrégés.

## 1. Courbe empirique
Même attaque que C7 (`c7_reidentification.rangs_attaque`, 60 items communs, distance de
Hamming), sur trois configurations : le jumeau riche le plus fort de C7 (JSON Persona
GPT4.1), Demographics Only, et un comparateur statistique nouveau, PMM k=5 sur les
demographies (appariement sur moyenne prédite, 5 plis, régression multinomiale), faute d'un
PMM Twin déjà calculé ailleurs dans le dépôt. Pool sous-échantillonné sans remise à
N = 50, 100, 250, 500, 1 000, 2 058 (les attaqués sont les N tirés eux-mêmes, cible = eux
dans ce même sous-pool), graine 20260911, **20 répétitions par N**, IC 95 % par
`a2_commun.bootstrap_personnes` sur les 20 répétitions.

## 2. Extrapolation
[HYPOTHÈSE, méthode] Le modèle à deux paramètres de Rocher, Hendrickx et de Montjoye
(*Nature Communications* 2025) repose sur des fonctions digamma inverses et des rapports de
fonctions Gamma difficiles à extraire fiablement d'un article verrouillé dans le temps
imparti : **on ne l'implémente pas**. À la place, deux modèles déclarés à l'avance : loi
puissance κ(N) = a·N^b et loi logarithmique κ(N) = a − b·log(N), ajustés en moindres carrés
sur les 6 N mesurés, comparés par validation croisée « leave-one-out » sur ces mêmes 6
points, extrapolés à N = 10 000, 100 000, 1 000 000 avec IC par ré-échantillonnage des
points d'ancrage.

## 3. Prédiction
Le top-1 du jumeau riche décroît avec N mais reste **au moins 5 fois** celui de Demographics
Only à N = 100 000 ; l'extrapolation au-delà de N = 2 058 est déclarée **indicative**, pas
une preuve.
