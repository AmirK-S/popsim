# C7-mecanisme, preenregistrement (11 septembre 2026, avant tout calcul)

Pourquoi les 40 items d'achat (QID9, bloc *Product Preferences - Pricing*, prix fixe par
produit, identifie via `llm/wave4_formatted_to_catalog_mapping.json` + `question_catalog.json`)
portent-ils la ré-identification (33 % top-1) contre 0,25 % sur les 20 autres items communs ?
Cible : `JSON Persona - GPT4.1`. Graine `20260911`, bootstrap personnes 2000 tirages
(`a2_commun.bootstrap_personnes`), reprise telle quelle de `c7_reidentification.rangs_attaque`
et `items_communs`. Hypotheses non exclusives.
**H1, variance/entropie.** Apparier par assignation hongroise (cout = |entropie humaine
(bits) diff|) les 20 items d'achat les plus proches en entropie des 20 items d'opinion, sur
les codes humains vague 4. Comparer le top-1 restreint a ce sous ensemble d'achat vs les 20
items d'opinion. Prediction H1 : IC des deux top-1 se chevauchent ; rejet si l'ecart reste
large (IC disjoints) malgre entropie appariee.
**H2, sensibilite au prix recopiee.** Pour chaque personne, correlation de Spearman entre son
vecteur binaire achat/pas achat (40 items) et le taux moyen d'achat humain par item (proxy
d'attractivite/prix, sans prix exact). Comparer cette coherence chez les humains et chez le
jumeau, puis correler les deux series (memes personnes). Prediction H2 : correlation personne
a personne nettement positive (le jumeau retrouve le seuil propre a l'individu).
**H3, structure de matrice.** Permuter, independamment pour chaque jumeau, l'ordre des 40
reponses d'achat (items encore alignes cote humains). Recalculer le top-1 sur ce vecteur
permute. Prediction H3 : chute pres du plancher deja mesure par l'oracle du seul nombre de
« oui » (0,29 %, contre-examen section 3) : le motif exact, pris en bloc, est necessaire.
**H4, stereotypie.** Sur les 20 items d'opinion, mode du segment `S_gra` en LOO (excluant la
personne), calcule sur les humains seuls. Taux d'accord humain-propre-reponse vs ce mode LOO,
compare au taux d'accord jumeau-vs-ce-meme-mode. Prediction H4 : taux jumeau nettement
superieur si le jumeau restitue le cliche du segment plutot qu'une reponse individualisee.

Sortie : `analyses/c7_mecanisme.py` (aucun appel de modele, lecture seule `data/`, aucun
pid/appariement imprime), `resultats/c7-mecanisme-resultats.md`.
