# C7-transfert, preenregistrement : la fuite traverse-t-elle les configurations et les vagues ?

**Ecrit le 12 septembre 2026, avant tout calcul.** Prolonge `resultats/c7-resultats.md`
(20,68 % top-1 jumeau JSON Persona GPT4.1 contre humains v4, 2 058 candidats, 60 items,
hasard 0,0486 %). Meme cadre ethique : aucun pid ni appariement individuel publie, seuls
des taux agreges. `analyses/c7_transfert.py` importe `rangs_attaque`, `graine_nom`,
`resume_taux` de `analyses/c7_reidentification.py` sans le modifier.

## Volet A — transfert entre les 8 configurations admissibles
Pour chaque paire ordonnee (X attaquant, Y bassin) parmi les 8 configs : top-1, top-10,
rang median, IC 95 % (bootstrap personnes, meme methode), sur les items remplis a 100 %
chez les attaques (X∩Y) et chez tout le bassin Y. 56 paires dirigees. Comparateurs
obligatoires : hasard = 1/n_bassin ; **Demographics Only** contre les 7 configs riches
(les deux sens), qui borne ce que la seule demographie explique.

## Volet B — transfert vers les humains de vagues 1-3, items differents
Verifie AVANT tout calcul : `humains_wave1_3.csv` (via `i3b_twin.charger_twin_commun`) est
un **retest des 108 items de vague 4 eux-memes**, pas des items disjoints. Les vrais items
non reposes existent (`t1_commun.demographies_brutes`, colonne `contexte`, ~494 items) mais
sont **disjoints par construction** de tout ce que le jumeau a jamais repondu : intersection
= 0, aucune distance calculable. **Volet B infaisable ici** : pas un manque d'effectif, une
absence structurelle d'items communs. Aucun calcul force.

## Predictions chiffrees
Volet A : top-1 moyen ≥ 15 % sur les 42 paires riches (hors Demographics), au-dessus des
20,7 % humains-v4 pas attendu sur chaque paire mais sur la moyenne. Demographics Only :
top-1 net en dessous des paires riches.

## Controle anti-artefact
Deux jumeaux d'un meme profil riche peuvent se ressembler par le segment demographique
seul. Controle : pour chaque personne attaquee, tirer un **decoy** — une AUTRE personne du
meme segment `S_gra`, presente dans le bassin Y — et relancer le meme rang avec ce decoy
comme cible. Le top-1 reel doit depasser nettement celui du decoy (proche du hasard sans artefact).

Graine 20260911. `.venv/bin/python`, aucun appel reseau ni de modele.
