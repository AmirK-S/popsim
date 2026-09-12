# C7-transfert-Stanford, préenregistrement : le canal inter-jumeaux se réplique-t-il ?

**Écrit le 12 septembre 2026, avant tout calcul.** Réplique `c7-transfert-resultats.md`
(Twin-2K-500 : 36,4 % top-1 à 60 items, 0,45 % à 19 items, contrôle 0,06 %) sur l'archive
Stanford, où les mêmes 1 052 personnes ont un agent « entretien » et un agent « enquête »
(gss/econ/bigfive, cf. `c7-stanford-provenance-resultats.md`).

## Attaque
Chaque agent entretien classe les 1 052 agents enquête par accord sur les items communs
(Hamming pour GSS catégoriel, distance euclidienne z-scorée pour econ/bigfive continus),
ordre mélangé, aucun identifiant ; puis l'inverse. `c7_transfert_stanford.py` réutilise
`c7_stanford.rangs_depuis_accord`/`resume_taux` et `c7_transfert.tirer_decoys`.

## Comparateurs et contrôle
Hasard = 1/1052. Agent démographique, mêmes bassins, deux sens. Contrôle anti-artefact :
décoy (autre personne, même segment démographique GSS), même bassin, même matrice.

## Contrôle d'items
Colonnes déjà identiques entre conditions : 177 items GSS, 5 économiques, 5 Big Five —
ces trois tailles font office de courbe par nombre d'items (comparable au 60/19 de Twin).

## Prédiction
Top-1 GSS (177 items) ≥ 20 % dans au moins un sens, bien au-dessus du démographique ;
contrôle anti-artefact < 1 %. Domaines à 5 items : top-1 net en dessous.

## Échec
Si le top-1 ne dépasse pas nettement le démographique, le canal ne se réplique pas hors
Twin et doit être présenté comme propre à ce jeu.

Graine 20260912. `.venv/bin/python`, aucun appel réseau ni de modèle.
