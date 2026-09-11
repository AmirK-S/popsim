# R7 : comparaison prospective de quatre checkpoints Olmo 3 7B

**Version destinée à une registration libre OSF, revue le 10 septembre 2026 avant tout run expérimental R7.** Cette page est un plan autonome ; elle ne constitue pas une promesse que le dépôt OSF a été effectué. La mise en ligne suivra la revue. R2b est terminé sur 180 personnes et le GPU est libre. Aucun appel expérimental R7 ni publication réseau n’est déclaré à cette revue.

## Question et portée

À invite identique, comment le facteur d’écart décrit entre camps varie-t-il entre quatre checkpoints publics de la famille Olmo 3 Instruct 7B : Base, SFT, DPO et modèle final ? Les quatre points seront comparés comme **checkpoints publiés**, avec une portée descriptive. L’appariement causal direct n’est pas établi : le rapport Olmo 3 indique que Instruct-SFT démarre depuis Think-SFT et que le RL final a été essayé depuis deux candidats DPO. Le champ `base_model` des cartes ne suffit donc pas à prouver l’identité du run d’entrée. Une différence observée ne sera attribuée ni à SFT, ni à DPO, ni au RLVR pris isolément. Le nom « final » sera préféré à « RLVR » lorsque l’algorithme exact n’est pas démontré.

Hypothèses archivées, inchangées dans leur sens : H1, au moins un contraste voisin est détectable ; H2, `F(final) < F(base)` ; H3, la plus grande marche voisine est Base→SFT ; H4, `F(SFT) - F(DPO) < 0` dans F1 et `F(SFT) - F(final) < 0` dans F2, les deux contrastes devant survivre à Holm. Le pari initial est une chute à SFT suivie d’une remontée partielle. Il pourra être rejeté ; une courbe monotone ou une hausse depuis Base sera rapportée telle quelle. Ces hypothèses ne deviennent pas causales par la registration.

## Conditions, révisions et protocole

Les conditions fixes sont :

| clé | checkpoint publié | révision locale |
|---|---|---|
| `olmo3base` | `allenai/Olmo-3-1025-7B` | `a81bae42db3975be1671e27b9c9a56da1a9f980f` |
| `olmo3sft` | `allenai/Olmo-3-7B-Instruct-SFT` | `e1452fc572d51966ff4aaeb25118b891eb93e549` |
| `olmo3dpo` | `allenai/Olmo-3-7B-Instruct-DPO` | `b33130b7de49f0c2553b5c2b3bc8409ff3e627d1` |
| `olmo3rlvr` | `allenai/Olmo-3-7B-Instruct` | `6e5971d9eba42665f5bd5a0fcf047f299ce1dccc` |

La branche est Instruct ; Think et 32B sont hors périmètre et non récupérables après observation. Les quatre poids sont en Q8_0, convertis avec le même commit. Si Q8_0 ne charge pas ou passe sous 5 tokens/s, les quatre seront refaits en Q4_K_M ; aucune quantification mixte ne sera analysée. Le checkpoint final utilisable est `Olmo-3-7B-rlvr-Q8_0.partial.gguf`, validation temporaire réussie, 355 tenseurs, SHA-256 `72ff5ad987602cb8b18fe7f079600094d13b1b917f2aa4550f0504dda6fafb60`. L’ancienne cible à zéro tenseur reste intacte et n’est pas utilisée.

L’invite de completion à trois exemples est celle de R4, au caractère près, sans gabarit de conversation, avec mêmes items, paramètres et arrêts. Cela apparie le format avec le socle, au prix d’une faible validité d’usage pour les checkpoints instruits. Paramètres : `temperature=0`, `top_k=1`, `n_predict=150`, cache activé, contexte 4096, un flux, serveur local unique, arrêts `\n----`, `\nSurvey question`, `<|endoftext|>`, `<|im_end|>`, `<|im_start|>`. Le masque historique de R1 est conservé : référent humain fixe, table et construction d’invite historiques non modifiées ; aucune microdonnée ne sort de la machine.

Le plan est de 149 items × 3 camps × 2 identités de demandeur × 4 conditions = **3 576 cellules/appels**, un appel par cellule. Camps : gauche, centre, droite ; demandeurs : journaliste neutre et membre du camp adverse. Ordre : condition, camp, identité, item. Les échecs sont des rejets et ne sont jamais relancés. Une trace complète est nécessaire pour l’analyse ; une reprise reprend la première cellule manquante, vérifie les lignes déjà présentes, refuse toute ligne tronquée, tout doublon, toute configuration différente et ne rejoue aucune cellule validée.

Les critères de rejet et de diagnostic sont les suivants, conformément au plan original. (1) Une condition dépassant 25 % de rejets de format est rejetée pour interprétation, tout en publiant son taux et son dénominateur. (2) Une sonde porte sur les 60 premières cellules de chaque condition : au-delà de 0,50 de rejets, la condition est arrêtée, son taux publié, puis la suivante est traitée. (3) Si l’ordre des quatre conditions sur F est le même que celui des taux de rejet, avec |rho de Spearman| > 0,8, la courbe est publiée comme artefact possible de conformité de format et n’est pas interprétée comme une dose-réponse. (4) Pour K >= 3, une distribution égale au vecteur de l’exemple ayant K modalités est exclue comme recopie ; au-delà de 5 % des cellules d’une condition, la condition est déclarée contaminée et n’est pas interprétée. Pour K = 2, le vecteur [43, 57] est conservé et son taux est publié à côté du taux de base. (5) Si une condition produit une distribution constante d’un camp à l’autre pour plus de 90 % des items, ce fait est publié comme résultat, sans prétendre mesurer un effet de camp. (6) Le facteur du plancher humain entre vagues 1 et 2 doit être dans [0,85 ; 1,15] ; sinon le run est rejeté. (7) Toute modification du référent humain, vérifiée par SHA-256, invalide la publication. (8) Deux `llama-server` simultanés invalident le run. (9) Les quatre fichiers doivent avoir la même quantification et le même commit de conversion ; sinon le run est invalidant. (10) Un écart de tokenisation supérieur à 2 % est publié et marque le contraste concerné comme non strictement apparié. Les rejets et invalidations n’entraînent aucune relance des cellules concernées.

## Mesures et inférence

La quantité principale est `F`, facteur H2b. Pour une condition `c`, `F_c = mean_i(d_ci) / mean_i(r_i)`, où `d_ci` est l’écart signé décrit pour l’item `i`, `position(droite) - position(gauche)`, et `r_i` l’écart réel correspondant. Un contraste entre les conditions A et B est `mean_i(d_Ai - d_Bi) / mean_i(r_i)`. Ce sont des ratios de moyennes ; aucun ratio par item n’est calculé. Le périmètre est celui des 79 items orientés, demandeur journaliste. Les secondaires publiées sont H2b chez le demandeur adverse, H2b sur les 65 items `retenu_strict`, H2a non signé sur les 149 items, H1 de dispersion interne par camp, erreur TV par rapport au réel avec le plancher humain, taux de rejet et statistiques de sonde.

L’unité de rééchantillonnage est l’item. Les IC à 95 % sont obtenus par bootstrap de tuples `(d_ci, d_bi, r_i)` appariés, avec 2 000 tirages et percentiles 2,5 à 97,5. Les contrastes utilisent une permutation bilatérale des signes de `d_Ai - d_Bi`, appariée par item, avec 20 000 tirages et p de Phipson-Smyth `(b+1)/(m+1)`. Un item rejeté dans l’une des deux conditions sort du contraste des deux conditions. Aucun choix de sous-ensemble après coup n’est permis.

Holm est appliqué séparément, seuil 0,05 : F1, `Base−SFT`, `SFT−DPO` et `DPO−Final` sur F ; F2, `Base−Final`, `Base−DPO` et `SFT−Final` sur F ; F3, quatre comparaisons de F à 1 ; F4, les trois contrastes voisins chez le demandeur adverse ; F5, 12 ratios de dispersion (3 camps × 4 conditions). H4 est une conjonction : `SFT−DPO < 0` dans F1 et `SFT−Final < 0` dans F2 doivent tous deux survivre à Holm. La bande [0,95 ; 1,05] de nullité pratique s’applique uniquement aux ratios comparés à 1, jamais aux différences ou aux contrastes entre conditions. Le comptage de contamination éventuel sur corpus voisin reste exploratoire, hors des familles F1 à F5, et ne prouve jamais qu’Olmo 3 a vu ou non un item.

## État préalable et antériorité honnête

Le plan original était un brouillon local non déposé ; son ancienne affirmation de quatre conversions/chargements réussis et d’absence totale d’appels doit être corrigée. La revue constate trois completions techniques historiques de huit tokens (Base/SFT/DPO), aucune cellule expérimentale R7, trois GGUF structurellement valides et un GGUF final désormais reconverti et validé temporairement avec 355 tenseurs. Ces essais ne sont ni des résultats R7 ni un benchmark. Le validateur et les tests hors GPU restent préparatoires ; le code retour global antérieur du validateur était attendu à 1 parce que l’ancienne cible finale échouait. Aucune inférence R7 n’est déclarée faite.

Le résultat décrira quatre checkpoints publics de la même famille, sous invite et quantification communes, avec les réserves de lineage ci-dessus. Il ne dira pas que l’alignement « censure », ne séparera pas algorithme et corpus, et ne généralisera pas au 32B. La page pourra être déposée après revue dans une registration OSF libre ; jusque-là son statut reste « plan écrit avant le run, non déposé ».

## Empreintes SHA-256 des fichiers concernés

Les empreintes sont celles contrôlées le 10 septembre 2026 ; elles permettent d’identifier exactement le plan, l’addendum et les entrées immuables réutilisées. Les scripts restent identifiés par leur nom et leur rôle, sans SHA-256 figé avant la revue technique indépendante. Aucun contenu de référent individuel n’est reproduit ici.

| fichier | SHA-256 |
|---|---|
| `resultats/r7-preenregistrement.md` | `c7c1fa35ace4c73547b299b13ec9c5ee5c53339cb6a5fb2c7f6c8a0f709933bc` |
| `resultats/r7-addendum-reprise-2026-09-10.md` | `e373335db2339196426bf37efeb908581355c4b8ed5071601712ba4f5ccaa5eb` |
| `data/traces/r1-distributions-reelles.csv` | `ea7cd93e8eb3b34d279171ac9a202a0451554afc3d34c7a142dfce761391c811` |
| `resultats/a37-orientation-items.csv` | `019653bd94a8fda496e962082ee46745f2eb6d720c55f787ac33e4ef18edce62` |

Le pilote `analyses/r7_checkpoints.py` et les sources analytiques réutilisées sont ceux présents dans le projet au moment de la revue ; leur empreinte pourra être figée après une revue technique indépendante si nécessaire.
