# C7-DP, resultats (12 septembre 2026)

## Mecanisme, ce qu'il garantit vraiment
Marginales par item bruitees (Laplace, sensibilite L1 = 2, budget reparti a parts egales sur 60 items, composition sequentielle basique) puis tirage i.i.d. par item (PrivBayes degre 0, aucune structure jointe). Epsilon-DP prouve pour la publication des histogrammes sur les 2 058 humains vague 4 ; le synthetique en herite par post-traitement. NON garanti : correlations et ecarts de segment S_gra (tires independamment, quel que soit epsilon) ; S_gra traite comme covariable publique non protegee (comme D1/D4) ; aucune composition avec les autres analyses du depot ; ni PrivBayes complet ni bibliotheque de reference (ecrit a la main, `analyses/c7_dp.py`).

## Tableau par epsilon (reference d'utilite = jumeau JSON Persona GPT4.1 non protege)
| epsilon | top1 [IC95%] | perte utilite (pts) | fidelite indiv. (pts) |
|---|---|---|---|
| 0,5 | 0,012 % [0 ; 0,036] | 5,61 | +0,02 |
| 1 | 0,080 % [0 ; 0,216] | 4,01 | +0,09 |
| 3 | 0,158 % [0,012 ; 0,340] | 3,33 | +0,12 |
| 10 | 0,000 % [0 ; 0] | 3,38 | +0,04 |
| infini (non prive) | 0,024 % [0 ; 0,073] | 3,52 | +0,20 |

D4 (permutation intra-segment, notre meilleure defense) : top1 = 0,126 % [0,012 ; 0,284], perte = 1,47 pt (`c7-defense-courbe.csv`). **Ce 1,47 est une moyenne de trois composantes d'erreur (distribution, ecarts de segment, correlations), dont deux sont nulles par construction pour D4** (la permutation intra-segment preserve exactement la distribution par item et les ecarts de segment) ; le cout reel de D4 ne porte que sur les correlations inter-items et vaut **4,4 points** (`c7-defense-resultats.csv`, ligne `D4_melange` : erreur_correlations = 4,3999..., utilite_globale = 1,4666... = 4,4/3). La comparaison a un epsilon DP scalaire au tableau ci-dessus reste valide, mais 1,47 sous-estime le cout de D4 d'un facteur 3 par construction, pas par un choix de mesure equivalent chez la DP. Fidelite DP quasi nulle partout (< 0,2 pt) : aucun conditionnement par personne, meme pas par segment.

## Superposition, verdict chiffre (critere preenregistre)
Prediction dementie : a eps = 3 et 10, la perte d'utilite (3,3-3,4 pts) est a moins de 5 pts de D4, et le top-1 (0,158 %, 0 %) n'est pas superieur au notre (0,126 %) — l'issue inverse annoncee. Meme le temoin non prive (eps = infini) plafonne a 3,52 pts : le plancher vient de l'architecture (erreur_groupes ~2,3-2,9 et erreur_correlations ~4,4-4,6 quasi constantes sur toute la plage), pas du budget ; seule erreur_distribution baisse avec epsilon (9,7 a 3,2 pts).

## La reponse theorique (le coeur de la question du relecteur)
Non, la DP ne repond pas a notre modele de menace. Elle protege l'APPARTENANCE d'un individu au jeu utilise pour calculer une statistique publiee — « Alice est-elle dans l'echantillon ? ». Notre attaque suppose Alice deja connue (son profil est l'entree du jumeau) et demande si LA SORTIE conditionnee sur Alice peut lui etre reliee : une liaison d'attribut/enregistrement, pas un probleme de membership. Le generateur DP ne « resout » ce probleme qu'en refusant la tache du jumeau : il ne conditionne jamais sur un individu (fidelite ~0 a tout epsilon), donc il ne peut pas se substituer a une personne precise en recherche. Sa faible fuite est un sous-produit de cette incapacite, pas du budget choisi.

## En clair
La DP la plus simple defendable egale ou bat nos defenses sur ce tableau agrege, mais elle y arrive en ne repondant jamais a la question de l'attaque : elle ne remplace jamais une personne, elle ne publie que des statistiques de population.
