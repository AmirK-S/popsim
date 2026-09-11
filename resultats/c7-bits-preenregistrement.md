# C7 bits d'identité : préenregistrement (12 septembre 2026, AVANT tout calcul)

Écrit avant `analyses/c7_bits.py` et avant tout chiffre. Objet : remplacer le taux top-1 (qui dépend du pool, du nombre d'items et du jeu) par une quantité transportable. Aucun appel de modèle, lecture seule sur `data/`, aucun fichier existant modifié. **Quantités agrégées seulement, aucun identifiant, aucun appariement individuel imprimé.**

## 1. Définitions et estimateurs
- **Attaque** : rang du vrai répondant dans un pool de N candidats, code existant réutilisé tel quel (`c7_reidentification.rangs_attaque` sur Twin ; `c7_stanford.charger_domaine` + `accord_categoriel` + `rangs_depuis_accord` sur Stanford). Identité supposée uniforme sur le pool : H(identité) = log2(N).
- **Voie rang (principale)** : bits = log2(N) − H(R), R = rang du vrai répondant. Justification : l'ordre des candidats est une fonction de la sortie, donc H(identité | sortie) ≤ H(R) et bits est un **minorant** de I(identité ; sortie). Estimateur principal, à faible variance et conservateur : bornage dyadique H(R) ≤ H(B) + Σ_b p̂(b)·log2|b| avec bins {1},{2,3},{4..7},… (≈11 bins pour N ≈ 2 000), H(B) corrigé Miller-Madow. Estimateur secondaire rapporté à côté : plug-in sur les N rangs + Miller-Madow (biaisé vers le haut pour les bits, donc non retenu comme chiffre principal).
- **Voie appariement (secondaire, par item)** : Î(S_j ; H_j) entre réponse simulée et réponse humaine, Miller-Madow sur chaque entropie. **Déclaré d'avance : la somme sur items n'est pas une mesure d'identité** (items dépendants, redondance positive attendue) ; elle sert de budget d'information par item, pas de total.
- **Bits par item** = bits_total / n_items. **Bits normalisés** = bits_total / Σ_j H_humaine(item j) : part de l'entropie humaine convertie en information d'identité.
- IC 95 % par bootstrap sur les personnes (2 000 tirages, graine 20260912), y compris pour les bits (ré-estimation de l'entropie du rang à chaque tirage).

## 2. Utilité et ratio
- **Utilité** = exactitude du prédicteur sur les mêmes items moins l'exactitude de la modalité modale de l'item (B0 mode), en points de pourcentage. Variante rapportée : moins la modalité modale du segment (S_gra sur Twin, cellule genre×race×âge×éducation sur Stanford).
- **Ratio** = bits de fuite / point d'exactitude gagné.
- **Règle déclarée d'avance** : si le gain d'exactitude est ≤ 0 ou si son IC couvre 0, le ratio n'est pas calculé ; on écrit « fuite sans gain d'exactitude mesurable », ce qui est un résultat plus fort et non un échec.
- Prédicteurs : les 8 configurations admissibles de Twin, B0 mode, B0 tirage, B1, B2, PMM k=10 (via `t1_baselines.calculer` importé sans modification, cible restreinte aux 60 items), retest humain comme plafond. Sur Stanford : composite, enquête, entretien, démographique, persona (v8 exclu), B0 mode, retest vague 2.

## 3. Prédictions chiffrées
1. Ratio des jumeaux LLM ≥ 5 fois celui de PMM sur Twin (ou, si le gain de PMM est nul au sens ci-dessus, fuite LLM ≥ 10 fois la fuite de PMM à gain d'exactitude comparable).
2. Bits par item normalisés par l'entropie humaine : Twin et Stanford dans un facteur 2 l'un de l'autre pour la meilleure configuration de chaque jeu.
3. Plafond : le retest humain domine les jumeaux en bits ET en utilité sur les deux jeux.
4. Ordres de grandeur : B0 mode ≈ 0 bit (validation de l'estimateur, l'IC doit contenir 0) ; B1, B2, PMM < 0,5 bit au total ; JSON Persona GPT4.1 ≥ 3 bits ; Stanford composite ≥ 6 bits.

## 4. Limites déclarées
- La voie rang est un minorant : un adversaire disposant du modèle de score complet ferait au moins aussi bien.
- Les bits saturent à log2(N) : la mesure reste bornée par le pool, mais un jumeau loin du plafond est comparable entre pools, ce que le taux top-1 n'est pas. Comparaison Twin/Stanford faite sur les bits par item normalisés, pas sur les bits totaux.
- Dépendance entre items : elle interdit d'additionner les MI par item ; toute agrégation de la voie appariement est rapportée comme plafond indicatif, jamais comme le chiffre de fuite.
- Taille d'échantillon : 2 058 (Twin) et 1 052 (Stanford) personnes ; l'entropie du rang sur N bins est mal estimée en plug-in, d'où le bornage dyadique en principal.
- Si un estimateur se révèle instable (IC bootstrap plus large que l'écart mesuré), la borne la plus défendable est rapportée à la place du chiffre.
