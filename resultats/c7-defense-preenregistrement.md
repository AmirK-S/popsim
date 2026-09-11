# C7-defense, preenregistrement (12 septembre 2026, avant tout calcul)

Le jumeau JSON Persona - GPT4.1 retrouve 20,7 % des 2 058 humains vague 4 sur 60 items
communs (`c7-resultats.md`) ; le mecanisme tient au bloc de 40 items d'achat pris en bloc
(`c7-mecanisme-resultats.md`). Question : une defense appliquee a CE bloc seul, jamais aux
humains, peut-elle casser la fuite sans detruire l'estimation de population ?

## Cible, attaque, defenses
`JSON Persona - GPT4.1`, memes 60 items communs, meme attaque (`c7_reidentification.
rangs_attaque`, Hamming, pool = 2 058 humains vague 4). Seuls les 40 items d'achat
(`c7_mecanisme.items_achat`) sont modifies ; les 20 items d'opinion restent tels quels,
comme dans le jumeau non protege. Reference risque = 20,68 % (mesure).
- D1 agregation : mode du groupe (groupes aleatoires de taille k) a la place de la
  reponse individuelle, k = 2, 5, 10, 25.
- D2 bruit : proportion p des 40 items, tiree au hasard par personne, remplacee par un
  tirage dans la marginale du jumeau pour l'item, p = 5, 10, 25, 50 %.
- D3 retrait : (a) les 40 items marques manquants ; (b) m items gardes au hasard par
  personne, m = 5, 10, 20 (sur 40).
- D4 melange : reponse permutee entre personnes du meme segment `S_gra`, item par item.

## Mesures
Risque = top-1 (`rangs_attaque`, IC bootstrap personnes, meme graine). Utilite = trois
erreurs en points, jumeau defendu contre jumeau non protege (et rappel contre humains) :
distribution par item, ecarts entre groupes `S_gra` (ecart type inter-segment par item),
correlations entre items (paires). Utilite globale = moyenne des trois erreurs absolues.

## Prediction chiffree, critere et garde-fous
[HYPOTHESE] Il existe un reglage qui ramene le top-1 sous 1 % en degradant l'utilite
globale de moins de 2 points ; D4 casse specifiquement les correlations entre items (perte
nettement superieure aux deux autres erreurs). Reglage recommande = risque le plus bas
parmi ceux sous 2 points de perte d'utilite, sinon la meilleure utilite sous 1 % de top-1.
Graine 20260911, fonctions de `c7_reidentification.py`/`c7_mecanisme.py` reprises sans
reecriture ; aucun pid ni appariement individuel imprime ; lecture seule sur `data/`,
aucun appel de modele, aucun reseau.
