# C7-DP, preenregistrement (12 septembre 2026, avant tout calcul)

Question du relecteur : pourquoi pas la DP plutot que nos defenses empiriques (D1-D4,
`c7-defense-courbe.csv`) ? Ce chantier construit le remede standard et le situe sur le
meme graphique risque-utilite.

## Mecanisme
Generateur le plus simple defendable : histogramme par item sur les 2 058 humains
vague 4 (memes 60 items communs que l'attaque C7), bruit de Laplace independant par
item (sensibilite L1 = 2, remplacement d'une personne), budget reparti a parts egales
sur les 60 items (composition sequentielle basique). Tirage i.i.d. par item apres
normalisation (PrivBayes degre 0, aucune structure de dependance, aucun segment). Le
jeu synthetique herite de la garantie epsilon-DP des histogrammes par post-traitement.
Epsilon in {0,5 ; 1 ; 3 ; 10 ; infini (temoin non prive, meme architecture)}.

## Mesures (reprises sans modification)
Risque = top-1 (`c7_reidentification.rangs_attaque`, IC bootstrap). Utilite = les
trois erreurs de `c7_defense.mesurer_utilite` (distribution, ecarts S_gra,
correlations) contre le jumeau JSON Persona GPT4.1, 40 items d'achat. Fidelite
individuelle = exactitude (`a44_mesures.exactitude_codes`), appariement reel moins
permute intra-segment (`a44_commun.permuter_intra`).
## Prediction chiffree
[HYPOTHESE] Aucun epsilon n'atteint une utilite a moins de 5 points de D4 (1,47) :
l'echantillonnage independant detruit par construction ecarts entre segments et
correlations, quel que soit epsilon (plancher d'architecture, pas le budget) ; top-1
restera pres du hasard (~0,05 %) partout. Donc DP dominee par D4, pas sur la frontiere.
Issue inverse : un epsilon a moins de 5 points de D4 avec top-1 non superieur au notre
impliquerait de reconsiderer DP comme alternative serieuse a D4.

Graine 20260912. Lecture seule sur `data/`, aucun appel de modele, aucun reseau.
