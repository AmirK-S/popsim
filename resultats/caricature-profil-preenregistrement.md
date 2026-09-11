# Caricature x richesse du profil, preenregistrement, avant tout calcul

Ecrit le 11 septembre 2026, avant l'execution de `analyses/caricature_profil.py`. Aucun appel
de modele : les 8 configurations admissibles de `twin-ab-audit-provenance-2026-09-11.md` sont
deja calculees. Camp = `blocs` de `i3b_twin.charger_twin_commun` (gauche/droite, ideologie
QID22), seule variable partisane locale ; personnes « centre »/« inconnu » exclues. Trois
niveaux de richesse : Demographics Only (1 config), JSON Persona (2), Text Persona (5).

**Mesure primaire, facteur d'exageration.** Par item categoriel j et par config c, sur les
personnes ayant un code valide (IA et humain v4) et un camp gauche/droite : ecart_IA(j) =
distance de variation totale (TVD, moitie de la somme des |p_k| des deux distributions de
modalites) entre gauche et droite chez l'IA ; ecart_hum(j) idem chez les humains v4, memes
personnes. facteur(j) = ecart_IA(j) / ecart_hum(j), item retenu seulement si ecart_hum(j) >=
0,02 (sinon exclu, compte rapporte). Facteur d'une config = mediane des facteur(j) sur les
items retenus. Facteur d'un niveau de richesse = mediane des facteur(j) sur tous les items de
toutes les configs du niveau, poolés.

**Mesure secondaire, compression.** Par item et par camp, dispersion = indice de
Gini-Simpson (1 - somme p_k^2) de la distribution de modalites, IA et humains, memes
personnes. compression(j) = moyenne sur les deux camps de disp_IA/disp_hum. Rapportee en
mediane sur les items, par config et par niveau. < 1 = l'IA est moins dispersee que l'humain
a l'interieur du camp.

**Prediction, dans le sens de la these.** Facteur(Demographics Only) >= 1,5 x
facteur(profils complets = JSON Persona + Text Persona poolés). Facteur(profils complets) >
1 (caricature reduite, non nulle).

**Intervalles.** Bootstrap a 2 000 replicats, personnes ET items reechantillonnes avec
remise conjointement (memes personnes gardent leur camp), graine 20260911. IC95 par
percentile sur le facteur de chaque niveau et sur leur ratio.
