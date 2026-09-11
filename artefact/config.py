"""config : parametres du jeu de donnees fictif et de l'attaque/defense de demonstration.

Aucune donnee reelle, aucune personne reelle. Tous les nombres ci-dessous pilotent une
simulation a graine fixe (voir generer_donnees.py) qui imite la STRUCTURE de Twin-2K-500
(items categoriels, bloc matrice produits x prix, segments demographiques, retest), avec
un signal individuel reglable dans le bloc d'achat : SIGNAL_INDIVIDUEL.
"""

GRAINE = 20260912

N_PERSONNES = 600           # << 2 058 humains reels de Twin, pour rester sous 5 minutes

# --- items "opinion" : jamais de signature individuelle, seulement un effet de segment ---
N_OPINION = 60
K_OPINION = 5                # modalites par item

# --- bloc "achat" : matrice produits x prix, signature individuelle reglable ---
N_ACHAT = 40
K_ACHAT = 5                  # 5 paliers de prix

# --- items de "contexte" : avec manquants, jamais utilises dans l'attaque, servent
#     uniquement a demontrer items_communs() (repris de c7_reidentification) sur un
#     jeu qui n'est pas rempli a 100 % partout, comme le vrai Twin-2K-500 ---
N_CONTEXTE = 20
PROB_MANQUANT_CONTEXTE = 0.30

# --- segments demographiques S_gra (genre x age x ethnicite), fictifs ---
GENRES = ["F", "H"]
AGES = ["18-29", "30-44", "45-59", "60+"]
ETHNIES = ["A", "B", "C"]

# --- signal individuel dans le bloc d'achat ---
# part de la reponse d'achat "verite terrain" (v4) qui vient du profil individuel stable
# plutot que de la seule moyenne de segment : c'est ce qui rend une personne identifiable
# en principe, avant meme tout jumeau.
PROB_INDIVIDU_ACHAT_VERITE = 0.70

# probabilite qu'une reponse d'achat du retest (v13) diverge malgre le meme profil
# individuel (fiabilite test-retest humaine imparfaite).
BRUIT_RETEST = 0.15

# LE CADRAN A REGLER : probabilite qu'un item d'achat du jumeau "riche" recopie
# exactement la vraie reponse de la personne (le mecanisme de fuite d'identite reproduit
# ici). 0.0 = aucune fuite (equivaut au jumeau "Demographics Only"). Plus haut = fuite
# plus forte et attaque plus efficace.
SIGNAL_INDIVIDUEL = 0.25

# decoupage des colonnes dans les matrices assemblees (opinion, achat, contexte) --
# ordre fixe, partage par generer_donnees.py, attaque.py et defense.py.
I_OPINION = slice(0, N_OPINION)
I_ACHAT = slice(N_OPINION, N_OPINION + N_ACHAT)
I_CONTEXTE = slice(N_OPINION + N_ACHAT, N_OPINION + N_ACHAT + N_CONTEXTE)
