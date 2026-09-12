# C7 attaquant fort, preenregistrement (12 septembre 2026, avant tout calcul)

Notre attaque C7 classe les candidats par simple accord de Hamming : un adversaire faible. Nos
taux sont une borne basse, et surtout D4 n'a ete evaluee que contre lui.

## Attaquant fort (A-LLR) et variante simple (A-MI)
Personne i, candidat c, somme sur les items j observes des deux cotes. H1 (c est i) : le jumeau
reproduit y_cj avec probabilite a_j, sinon tire dans la marginale q_j ; H0 : independance, de
marginale q_j. Score = somme_j [ accord x log(a_j/q_j(y_cj)) + desaccord x log((1-a_j)/(1-q_j(y_cj))) ].
Un accord sur une modalite RARE pese donc bien plus qu'un accord banal. Si le nombre d'items
communs varie selon le candidat, la somme est ramenee au nombre moyen. A-MI : accord pondere par
`mi_bits` de `c7-bits-par-item.csv`, normalise par la somme des poids.

## Estimation hors pli : aucune donnee de la cible
5 plis de personnes, graine 20260912. Les personnes du pli k sont attaquees ; a_j et q_j sont
estimes UNIQUEMENT sur les 4 autres plis : aucune reponse de la personne attaquee, jumeau ou
humain, n'entre dans ses propres parametres. Le pool des candidats reste la population entiere
(2 058 Twin, 1 052 Park). Declare : les poids `mi_bits` d'A-MI sont calcules sur toutes les
personnes, avantage en echantillon concede a la variante simple, jamais a A-LLR.

## Protocole, identique par ailleurs
Twin-2K-500, `JSON Persona - GPT4.1`, 60 items communs, pool humains vague 4 ; archive Park et
al., bloc GSS, condition composite, pool vague 1. `c7_reidentification.rangs_attaque` (naif),
`c7_stanford.rangs_depuis_accord`, `c7_monde_ouvert.marges_deux_regimes`/`roc_et_taux` (TPR a
0,1 % et 1 % de faux positifs) et `c7_defense.defense_d4` sont importees sans modification ;
a_j et q_j sont reestimes hors pli sur les sorties DEFENDUES. Ethique : aucun identifiant,
aucun appariement individuel, taux agreges seuls ; aucun appel de modele, aucun reseau.

## Predictions chiffrees
[P1] A-LLR augmente le top-1 d'au moins 20 % relatifs sur les deux jeux : Twin au-dessus de
24,8 % (naif 20,67 %), Park au-dessus de 78,9 % (naif 65,72 %).
[P2] D4 tient : top-1 sous 1 % meme sous A-LLR (naif 0,13 %).
[Echec de P2] Si D4 depasse 1 %, publier que notre parade ne resiste pas a un adversaire mieux arme : resultat en soi, a faire figurer dans l'article.
[Echec de P1] Si A-LLR n'apporte rien, nos taux naifs etaient deja proches du plafond atteignable : cela RENFORCE le papier, et sera dit ainsi.

---

# Addendum du 12 septembre 2026 (avant calcul) : volet 4, attaquant ADAPTATIF

Demande du coordinateur, ecrite avant tout calcul. Les volets 1 a 3 evaluent D4 contre un
adversaire qui ignore qu'une defense a ete appliquee. En securite, une parade doit resister a
un adversaire QUI LA CONNAIT.

## Modele de menace
L'attaquant SAIT : que le bloc de 40 items d'achat a ete permute entre personnes du meme
segment `S_gra`, item par item ; le mecanisme exact (`c7_defense.defense_d4`) ; quels items
sont touches et lesquels ne le sont pas ; le segment de chaque membre du pool humain, qui est
demographique et public. Il IGNORE : la permutation tiree (la graine), donc l'appariement
reel entre les 40 reponses publiees et les personnes du segment.

## Strategies, au moins deux, toutes avec A-LLR et parametres hors pli
[S1] Items non touches. Verification faite dans `c7_defense.py` : D4 ne permute que les 40
items d'achat, les 20 items d'opinion sont publies intacts. Attaque A-LLR sur ces 20 items
seuls. C'est la strategie evidente et elle doit etre mesuree.
[S2] Niveau segment. La permutation preserve exactement le multiensemble des reponses d'un
segment. L'attaquant attribue a la personne attaquee le segment du candidat de meilleur score
(agrege sur les membres du segment). Mesure : exactitude de segment contre le hasard et
contre le segment le plus frequent. Retrouver le segment sans retrouver l'identite est une
DIVULGATION D'ATTRIBUT, risque de nature differente, qui sera nomme comme tel.
[S3] Invariants. Score par appariement des modalites RARES du jumeau au multiensemble
preserve du segment du candidat, quantite qui survit par construction a la permutation,
combine aux 20 items intacts.

## Mesures et prediction
Top-1 et top-10 sous chaque strategie, contre la fuite sous attaquant naif (0,13 %) et sous
A-LLR non adaptatif.
[P3] L'attaquant adaptatif fait remonter la fuite AU-DESSUS de 1 %, sans revenir au niveau
non defendu (20,67 %).
[Issue franche] Si une strategie adaptative ramene la fuite pres de son niveau initial, notre
defense NE TIENT PAS : l'article doit le dire clairement plutot que de vanter le 0,13 %.
