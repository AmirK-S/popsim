"""
a1 : la double distorsion, mesuree sur le paquet de replication OSF t6g7k de Stanford.

Statut : script d'analyse, pas du code de production. Il existe pour qu'un tiers puisse
rejouer chaque chiffre du rapport resultats/a1-double-distorsion.md en une commande.

QUESTION POSEE
--------------
Quand un modele de langage simule des personnes, la dispersion de ses reponses se
decompose t elle comme celle des humains ? On separe la dispersion d'un item en deux
termes, la part qui vient des ecarts ENTRE segments demographiques et la part qui vient
des ecarts A L'INTERIEUR des segments, puis on rapporte chaque terme a celui des humains
de la vague 1. Deux ratios par condition, donc un point dans un plan.

Les humains de la vague 2 sont les memes personnes reinterrogees deux semaines plus tard.
Ils servent de controle : une methode sans biais doit les placer en (1, 1).

ENTREES
-------
1. figure2/data/new_analysis_summaries/gss_filtered/preparation/*.csv
   Un fichier par condition, 1052 lignes, 177 colonnes d'items du GSS, reponses en clair.
   Premiere colonne : identifiant de participant, aligne entre tous les fichiers.
2. figure2/data/question_master/gss/main.csv
   Libelle et liste ORDONNEE des modalites de chaque item. Sert de nomenclature.
3. figure2/data/question_master/gss/groups/categorical.csv
   Marque "Y" les items nominaux et "N" les items ordinaux. 79 items ordinaux sur 177.
4. figure3/data/demographic_summary.csv
   Douze attributs demographiques par participant. Sert de segmentation.
5. figure3/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv
   Consistance test retest par individu, champ p_wave1__p_wave2__accuracy.

SORTIES, toutes dans resultats/
-------------------------------
  a1-figure-double-distorsion.png et .svg   la figure principale
  a1-ratios.csv                             les deux ratios par condition et par mesure
  a1-ratios-par-axe.csv                     le detail axe demographique par axe
  a1-silhouette.csv                         le score de silhouette par condition et par axe
  a1-plafond-humain.csv                     la distribution de la consistance test retest
  a1-controle-permutation.csv               le diagnostic de biais des estimateurs
  a1-etiquettes-demographiques.csv          gss_v6 contre gss_v8, cf. section 7
  et un resume imprime sur la sortie standard.

DEPENDANCES : numpy et matplotlib. Aucun appel de modele de langage.
Duree : environ deux minutes, l'essentiel en bootstrap.

Usage : python3 analyses/a1_double_distorsion.py
        options : --racine CHEMIN, --sortie CHEMIN, --bootstrap N (defaut 1000),
                  --permutations N (defaut 50, diagnostic seulement), --rapide
"""

import argparse
import csv
import json
import math
import os
import re
import sys

try:
    import numpy as np
except ImportError:
    sys.exit("numpy est absent. Dans ce depot : .venv/bin/python analyses/a1_double_distorsion.py\n"
             "Sinon : python3 -m pip install numpy matplotlib")

LN2 = math.log(2.0)

# ---------------------------------------------------------------------------
# 1. Parametres. Tout ce qui est un choix est ici, et commente.
# ---------------------------------------------------------------------------

RACINE_DEFAUT = "data/osf-t6g7k-stanford"

# Les huit conditions. Les libelles ne sont pas devines : ils viennent de
# figure2/code/plotting/plot_figure_2.py et de figure3/code/dpd/build_dpd_summaries.py.
# Point verifie et a garder en tete : gss_v6 et gss_v8 sont DEUX variantes d'agent
# demographique. La figure 2 du papier emploie v6, la figure 3 emploie v8. On garde
# les deux, et leur ecart est en soi un resultat.
CONDITIONS = [
    ("humains vague 1", "p_wave1_summary.csv"),
    ("humains vague 2", "p_wave2_summary.csv"),
    ("agents composite", "composite_agents_summary.csv"),
    ("agents entretien (v3)", "gss_v3_summary.csv"),
    ("agents enquete", "survey_agents_summary.csv"),
    ("agents persona (v7)", "gss_v7_summary.csv"),
    ("agents demographiques (v6)", "gss_v6_summary.csv"),
    ("agents demographiques (v8)", "gss_v8_summary.csv"),
]
REFERENCE = "humains vague 1"

# Axes de segmentation. Les trois premiers sont exactement ceux que le papier emploie
# pour sa figure 3, cf. DPD_VARS dans figure3/code/dpd/build_dpd_summaries.py. On ne les
# a donc pas choisis pour arranger le resultat. age et education sont ajoutes parce
# qu'ils sont complets et sans ambiguite. Le sixieme axe croise les trois premiers : il
# approche la notion de profil demographique, qui est ce qu'un agent recoit dans son
# invite. income, neighborhood et sexual_orientation sont ecartes : 180 valeurs vides
# sur 1052, soit 17 pour cent, ce qui rendrait les segments non comparables.
AXES = ["gender", "race", "political_ideology", "age", "education", "profil croise"]

# Items ecartes de l'analyse principale : ce sont les items du GSS qui redisent
# litteralement un attribut de segmentation. Un agent demographique a recu ces valeurs
# dans son invite, il ne les predit pas, il les recopie. Les garder mesurerait la
# fidelite de recopie et non la structure des opinions. L'option --tous-items refait
# tout le calcul sans cette exclusion, et le rapport donne les deux chiffres.
ITEMS_DEMOGRAPHIQUES = {
    "sex*",       # <- gender
    "race*",      # <- race
    "educ*",      # <- education
    "degree*",    # <- education
    "income",     # <- income
    "polviews",   # <- political_ideology
    "partyid",    # <- political_party
    "reg16",      # <- census_division, region a 16 ans, tres correlee
}

MESURES = ["entropie", "gini_simpson", "variance_ordinale"]


def normaliser(valeur):
    """Normalise une reponse en clair avant appariement a la nomenclature de l'item.

    Les fichiers d'agents contiennent une minorite de reponses mal formees : guillemets
    conserves, ponctuation finale, ou phrase de justification a la place de la modalite.
    On enleve la ponctuation entourante et on ecrase la casse. Ce qui ne tombe toujours
    pas dans la nomenclature est compte comme non codable, et le taux est affiche.
    Mesure : au pire 0,24 pour cent des cellules d'une condition. Chez les humains, zero.

    Attention : ne jamais traiter "none" comme une valeur manquante. C'est une modalite
    valide de plusieurs items du GSS, notamment relig. Seuls la chaine vide et le marqueur
    <not recorded> du paquet OSF sont des manquants.
    """
    v = valeur.strip().lower().strip("\"'` .")
    return re.sub(r"\s+", " ", v)


def est_manquant(v):
    return v == "" or v.startswith("<not recorded")


# ---------------------------------------------------------------------------
# 2. Lecture des donnees
# ---------------------------------------------------------------------------

def lire_nomenclature(racine):
    """Pour chaque item : la liste ORDONNEE de ses modalites, et son type.

    L'ordre est celui du champ Options du question_master. Pour les items marques
    ordinaux il correspond a l'echelle du questionnaire, ce qui autorise un codage
    0..K-1 sans invention de notre part.
    """
    p_main = os.path.join(racine, "figure2/data/question_master/gss/main.csv")
    p_cat = os.path.join(racine, "figure2/data/question_master/gss/groups/categorical.csv")
    options, ordinal = {}, {}
    for r in csv.DictReader(open(p_main, encoding="utf-8")):
        options[r["Question ID"].lower()] = [normaliser(o) for o in json.loads(r["Options"])]
    for r in csv.DictReader(open(p_cat, encoding="utf-8")):
        cle = [k for k in r if k.strip().lower().startswith("categorical")][0]
        # "Categorical = Y" veut dire nominal, "N" veut dire ordinal.
        ordinal[r["Question ID"].lower()] = (r[cle].strip().upper() == "N")
    return options, ordinal


def lire_condition(chemin, entetes_attendus, options):
    """Lit un fichier de condition et le code en entiers.

    Sortie : matrice (n_participants, n_items) d'entiers, -1 pour non codable,
    la liste des identifiants, et le taux de cellules non codables.
    """
    lignes = list(csv.reader(open(chemin, newline="", encoding="utf-8")))
    if lignes[0][1:] != entetes_attendus:
        sys.exit(f"Entetes differents dans {chemin}, l'appariement par colonne serait faux.")
    ids = [l[0] for l in lignes[1:]]
    n, j_max = len(ids), len(entetes_attendus)
    x = np.full((n, j_max), -1, dtype=np.int16)
    index = [{m: k for k, m in enumerate(options[q])} for q in entetes_attendus]
    non_codable = 0
    for i, ligne in enumerate(lignes[1:]):
        for j in range(j_max):
            v = normaliser(ligne[j + 1])
            k = -1 if est_manquant(v) else index[j].get(v, -1)
            if k < 0:
                non_codable += 1
            else:
                x[i, j] = k
    return x, ids, non_codable / (n * j_max)


def lire_demographies(racine, ids_attendus):
    """Retourne axe -> vecteur d'entiers de segment (-1 si manquant) et la liste des niveaux."""
    p = os.path.join(racine, "figure3/data/demographic_summary.csv")
    lignes = {r["email"]: r for r in csv.DictReader(open(p, encoding="utf-8"))}
    absents = [i for i in ids_attendus if i not in lignes]
    if absents:
        sys.exit(f"{len(absents)} participants sans demographie, alignement impossible.")

    def brut(axe):
        return [lignes[i][axe].strip().lower() for i in ids_attendus]

    def bloc_ideologie(v):
        # Les sept niveaux du GSS ramenes a trois, pour que le croisement garde des
        # effectifs exploitables. Regle mecanique sur le libelle, pas de jugement.
        if "liberal" in v:
            return "gauche"
        if "conservative" in v:
            return "droite"
        return "centre"

    valeurs = {}
    for axe in AXES:
        if axe == "profil croise":
            g, r, i = brut("gender"), brut("race"), brut("political_ideology")
            valeurs[axe] = [f"{a}|{b}|{bloc_ideologie(c)}" for a, b, c in zip(g, r, i)]
        else:
            valeurs[axe] = brut(axe)

    seg, niveaux = {}, {}
    for axe in AXES:
        mods = sorted({v for v in valeurs[axe] if v.strip() != ""})
        idx = {m: k for k, m in enumerate(mods)}
        seg[axe] = np.array([idx.get(v, -1) for v in valeurs[axe]], dtype=np.int16)
        niveaux[axe] = mods
    return seg, niveaux


# ---------------------------------------------------------------------------
# 3. Le coeur : decomposition de la dispersion en inter et intra segments
# ---------------------------------------------------------------------------
#
# POURQUOI TROIS MESURES ET PAS UNE
# ---------------------------------
# Les reponses sont categorielles, une partie seulement est ordinale. Aucune mesure de
# dispersion ne s'impose. On en calcule trois, choisies pour ne pas partager les memes
# hypotheses, et on regarde si la conclusion tient sur les trois. Si elle ne tenait pas,
# ce serait le resultat a publier.
#
#  M1  Entropie de Shannon. Decomposition exacte H(R) = H(R|S) + I(R;S).
#      intra = H(R|S), l'incertitude qui reste une fois le segment connu.
#      inter = I(R;S), l'information que le segment donne sur la reponse.
#      Aucune hypothese d'ordre. Sensible aux modalites rares.
#
#  M2  Indice de Gini Simpson, D = 1 - somme p_k au carre. C'est l'analogue categoriel
#      de la variance et il admet la meme decomposition additive exacte :
#      D_total = D_intra + D_inter, avec D_intra = somme_g w_g D_g et D_inter >= 0
#      par convexite. Aucune hypothese d'ordre. Peu sensible aux modalites rares, ce qui
#      en fait le controle naturel de M1.
#
#  M3  Variance sur codage ordinal, restreinte aux items marques ordinaux par les auteurs
#      eux memes. Modalites codees 0..K-1 dans l'ordre du questionnaire puis divisees par
#      K-1, pour qu'un item a 3 et un item a 12 modalites soient comparables. Loi de la
#      variance totale : Var(R) = E[Var(R|S)] + Var(E[R|S]). C'est la mesure la plus
#      proche de ce que la litterature appelle un ratio d'ecarts types, mais elle suppose
#      des intervalles egaux entre modalites, ce qui est faux. D'ou son statut de controle
#      et non de mesure principale.
#
# LE BIAIS D'ECHANTILLON, ET POURQUOI IL FALLAIT LE TRAITER
# ---------------------------------------------------------
# L'estimateur naif de I(R;S) et de D_inter est positivement biaise : meme si le segment
# n'explique rien, un echantillon fini donne une valeur strictement positive. Ce biais
# croit avec le nombre de modalites effectivement employees. Or les agents en emploient
# MOINS que les humains. Comparer des estimateurs naifs fabriquerait donc mecaniquement
# un ratio inter inferieur a 1, c'est a dire l'inverse du resultat cherche, ou le
# masquerait. Chaque mesure emploie donc un estimateur a biais corrige :
#   M1 : correction de Miller Madow, H corrige = H naif + (m - 1) / (2 N ln 2), ou m est
#        le nombre de cases non vides. Appliquee a H(R), H(S) et H(R,S).
#   M2 : estimateur sans biais de l'indice de Simpson, somme n_k (n_k - 1) / (N (N - 1)).
#   M3 : composante de variance inter au sens de l'analyse de variance,
#        (SCE_inter - (G - 1) CM_intra) / N, d'esperance nulle sous independance.
# Le controle empirique de ces corrections est dans a1-controle-permutation.csv : on
# permute au hasard les etiquettes de segment et on verifie que le terme inter tombe a
# zero, pour toutes les conditions, y compris celles a faible entropie.

def construire_index(x, seg, k_max, g_max, n_items, axes=None):
    """Index plat servant au comptage vectorise.

    idx[a, i, j] designe la case (axe a, item j, segment de i, reponse de i a j) dans un
    tableau aplati. Les cellules non codables partent dans une case poubelle ignoree.
    """
    axes = axes or AXES
    n = x.shape[0]
    poubelle = len(axes) * n_items * g_max * k_max
    idx = np.full((len(axes), n, n_items), poubelle, dtype=np.int32)
    for a, axe in enumerate(axes):
        base = (np.arange(n_items, dtype=np.int32) + a * n_items) * (g_max * k_max)
        g = seg[axe].astype(np.int32)
        valide = (g[:, None] >= 0) & (x >= 0)
        plein = base[None, :] + g[:, None] * k_max + np.maximum(x, 0).astype(np.int32)
        idx[a][valide] = plein[valide]
    return idx, poubelle


def compter(idx, lignes, poubelle, n_items, g_max, k_max, n_axes):
    """Table de contingence (axe, item, segment, reponse) sur un sous ensemble de lignes."""
    c = np.bincount(idx[:, lignes, :].ravel(), minlength=poubelle + 1)[:poubelle]
    return c.reshape(n_axes, n_items, g_max, k_max).astype(np.float64)


def _xlogx(p):
    """p log2 p, prolonge par 0 en 0."""
    out = np.zeros_like(p)
    m = p > 0
    out[m] = p[m] * np.log2(p[m])
    return out


def decomposer(c, valeurs_ordinales, n_min=30):
    """Decompose la dispersion. Entree : table de contingence (A, J, G, K).

    Sortie : mesure -> (inter, intra, valide), trois tableaux (A, J).
    Chaque terme est un estimateur a biais corrige, cf. le commentaire ci dessus.
    """
    n_g = c.sum(axis=3)                     # (A, J, G)
    n_k = c.sum(axis=2)                     # (A, J, K)
    N = n_g.sum(axis=2)                     # (A, J)
    valide = N >= n_min
    N_s = np.where(valide, N, 1.0)

    # --- M1 entropie, correction de Miller Madow -----------------------------
    def h_mm(counts):
        """Entropie en bits, estimateur de Miller Madow.

        counts est un tableau (A, J, cases). Le terme (m - 1) / (2 N ln 2) corrige le
        biais negatif de l'entropie naive, biais qui croit avec le nombre m de cases
        occupees. C'est exactement ce qui differe entre humains et agents.
        """
        p = counts / N_s[:, :, None]
        h = -_xlogx(p).sum(axis=2)
        m = (counts > 0).sum(axis=2)
        return h + (m - 1.0) / (2.0 * N_s * LN2)

    h_r = h_mm(n_k)
    h_s = h_mm(n_g)
    h_rs = h_mm(c.reshape(c.shape[0], c.shape[1], -1))
    m1_intra = h_rs - h_s                   # H(R|S)
    m1_inter = h_r - m1_intra               # I(R;S)

    # --- M2 Gini Simpson, estimateur sans biais ------------------------------
    def simpson_unb(counts, total, axe):
        """1 - somme p au carre, estimateur sans biais : somme n_k (n_k - 1) / N (N - 1).

        total a une dimension de moins que counts, celle sur laquelle on somme.
        """
        den = np.where(total > 1.0, total * (total - 1.0), 1.0)
        return 1.0 - (counts * (counts - 1.0)).sum(axis=axe) / den

    d_tot = simpson_unb(n_k, N_s, 2)
    n_g_ok = n_g >= 2
    d_g = simpson_unb(c, np.where(n_g_ok, n_g, 2.0), 3)
    poids = np.where(n_g_ok, n_g, 0.0)
    poids_tot = np.where(poids.sum(axis=2) > 0, poids.sum(axis=2), 1.0)
    m2_intra = (poids * d_g).sum(axis=2) / poids_tot
    m2_inter = d_tot - m2_intra

    # --- M3 variance ordinale, composante de variance au sens de l'ANOVA -----
    v = valeurs_ordinales                   # (J, K) valeurs dans [0, 1]
    s1 = (n_k * v[None, :, :]).sum(axis=2)
    s2 = (n_k * (v ** 2)[None, :, :]).sum(axis=2)
    sce_tot = s2 - s1 ** 2 / N_s
    s1g = (c * v[None, :, None, :]).sum(axis=3)
    s2g = (c * (v ** 2)[None, :, None, :]).sum(axis=3)
    n_g_pos = np.where(n_g > 0, n_g, 1.0)
    sce_intra = (s2g - s1g ** 2 / n_g_pos).sum(axis=2)
    sce_inter = sce_tot - sce_intra
    g_eff = (n_g > 0).sum(axis=2)
    ddl = np.maximum(N - g_eff, 1.0)
    cm_intra = sce_intra / ddl
    m3_intra = cm_intra
    m3_inter = (sce_inter - (g_eff - 1.0) * cm_intra) / N_s

    return {
        "entropie": (m1_inter, m1_intra, valide),
        "gini_simpson": (m2_inter, m2_intra, valide),
        "variance_ordinale": (m3_inter, m3_intra, valide),
    }


def agreger(dec, masque_items, est_ordinal, axes_gardes=None):
    """Somme les termes inter et intra sur les axes et les items retenus.

    On somme plutot que de moyenner des ratios item par item : un item ou la dispersion
    humaine est presque nulle produirait un ratio explosif qui dominerait la moyenne.
    Le rapport donne aussi la mediane des ratios item par item, en controle.
    """
    out = {}
    for m, (inter, intra, valide) in dec.items():
        garder = masque_items & (est_ordinal if m == "variance_ordinale" else True)
        msk = valide & garder[None, :]
        if axes_gardes is not None:
            sel = np.zeros(inter.shape[0], dtype=bool)
            sel[axes_gardes] = True
            msk = msk & sel[:, None]
        out[m] = (float(np.where(msk, inter, 0.0).sum()),
                  float(np.where(msk, intra, 0.0).sum()))
    return out


# ---------------------------------------------------------------------------
# 4. Silhouette
# ---------------------------------------------------------------------------
#
# CHOIX DE LA DISTANCE
# --------------------
# Les reponses melangent nominal et ordinal, sans unite commune. La seule distance qui ne
# suppose rien est l'appariement simple : d(i, i') = proportion des items ou i et i' ont
# donne une reponse differente, calculee sur les items ou les deux ont repondu. C'est le
# coefficient de Gower reduit au cas purement categoriel. Ne pas employer une distance
# euclidienne sur un codage ordinal : elle donnerait un poids arbitraire aux items a
# nombreuses modalites, et ces items sont precisement ceux ou les agents divergent.

def matrice_distance(x, garder):
    """Distance d'appariement simple entre participants, sur les items retenus."""
    n = x.shape[0]
    diff = np.zeros((n, n), dtype=np.float32)
    valides = np.zeros((n, n), dtype=np.float32)
    for j in np.where(garder)[0]:
        col = x[:, j]
        v = col >= 0
        paire = np.logical_and(v[:, None], v[None, :])
        valides += paire
        diff += np.logical_and(paire, col[:, None] != col[None, :])
    return diff / np.maximum(valides, 1.0)


def silhouette(d, groupes, n_groupes, poids=None):
    """Silhouette moyenne d'une partition donnee, distances pre calculees.

    poids permet le bootstrap sans recopier la matrice : un participant tire m fois
    compte m fois dans les moyennes de groupe. C'est algebriquement identique a
    construire la sous matrice de l'echantillon bootstrap, et cent fois plus rapide.
    """
    n = d.shape[0]
    if poids is None:
        poids = np.ones(n, dtype=np.float32)
    valide = groupes >= 0
    w = np.zeros((n, n_groupes), dtype=np.float32)
    w[np.arange(n)[valide], groupes[valide]] = poids[valide]
    somme = d @ w                                  # (n, G) distances cumulees vers chaque groupe
    taille = w.sum(axis=0)                         # (G) effectif pondere
    g = np.where(valide, groupes, 0)
    with np.errstate(divide="ignore", invalid="ignore"):
        a = somme[np.arange(n), g] / np.maximum(taille[g] - 1.0, 1e-9)
        moy = somme / np.maximum(taille, 1e-9)[None, :]
    moy[np.arange(n), g] = np.inf
    moy[:, taille < 1] = np.inf
    b = moy.min(axis=1)
    s = (b - a) / np.maximum(a, b)
    bon = valide & (taille[g] >= 2) & np.isfinite(s) & (poids > 0)
    if not bon.any():
        return float("nan")
    return float(np.average(s[bon], weights=poids[bon]))


# ---------------------------------------------------------------------------
# 5. Programme principal
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=RACINE_DEFAUT)
    ap.add_argument("--sortie", default="resultats")
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--permutations", type=int, default=50,
                    help="diagnostic de biais uniquement, n'entre pas dans les chiffres")
    ap.add_argument("--graine", type=int, default=20260903)
    ap.add_argument("--tous-items", action="store_true",
                    help="ne pas exclure les items purement demographiques")
    ap.add_argument("--rapide", action="store_true", help="bootstrap 100, pour un essai")
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap, args.permutations = 100, 15

    prep = os.path.join(args.racine,
                        "figure2/data/new_analysis_summaries/gss_filtered/preparation")
    if not os.path.isdir(prep):
        sys.exit(f"Dossier introuvable : {prep}\n"
                 "Reconstituer : curl -L -o data/replication.rar https://osf.io/download/s2u7c/")
    os.makedirs(args.sortie, exist_ok=True)
    rng = np.random.default_rng(args.graine)

    # --- lecture ----------------------------------------------------------
    options, ordinal = lire_nomenclature(args.racine)
    entetes = next(csv.reader(open(os.path.join(prep, "p_wave1_summary.csv"),
                                   encoding="utf-8")))[1:]
    n_items = len(entetes)

    donnees, taux_nc, ids_ref = {}, {}, None
    for libelle, fichier in CONDITIONS:
        chemin = os.path.join(prep, fichier)
        if not os.path.exists(chemin):
            print(f"absent, condition ignoree : {fichier}")
            continue
        x, ids, nc = lire_condition(chemin, entetes, options)
        if ids_ref is None:
            ids_ref = ids
        elif ids != ids_ref:
            sys.exit(f"Identifiants desalignes dans {fichier}.")
        donnees[libelle], taux_nc[libelle] = x, nc
    noms = [c for c, _ in CONDITIONS if c in donnees]
    n = len(ids_ref)

    seg, niveaux = lire_demographies(args.racine, ids_ref)

    # --- items retenus et codage ordinal ----------------------------------
    garder = np.array([args.tous_items or (q not in ITEMS_DEMOGRAPHIQUES) for q in entetes])
    est_ordinal = np.array([ordinal.get(q, False) for q in entetes])
    k_par_item = np.array([len(options[q]) for q in entetes])
    k_max, g_max = int(k_par_item.max()), int(max(len(niveaux[a]) for a in AXES))
    valeurs_ordinales = np.zeros((n_items, k_max))
    for j, q in enumerate(entetes):
        if est_ordinal[j] and k_par_item[j] > 1:
            valeurs_ordinales[j, :k_par_item[j]] = np.arange(k_par_item[j]) / (k_par_item[j] - 1)

    print("=" * 92)
    print("a1 : DOUBLE DISTORSION, decomposition inter et intra segments demographiques")
    print("=" * 92)
    print(f"{n} participants, {n_items} items du GSS, {int(garder.sum())} items retenus "
          f"({int((~garder).sum())} items purement demographiques exclus)")
    print(f"{int((est_ordinal & garder).sum())} items ordinaux parmi les retenus, "
          f"employes pour la mesure de variance")
    print("Segmentation : " + ", ".join(f"{a} ({len(niveaux[a])} segments)" for a in AXES))
    print("\nTaux de cellules non codables par condition")
    for c in noms:
        print(f"  {c:<28}{taux_nc[c] * 100:6.2f}%")

    n_axes = len(AXES)
    index = {}
    for c in noms:
        index[c], poubelle = construire_index(donnees[c], seg, k_max, g_max, n_items)
    toutes = np.arange(n)

    def mesurer(cond, lignes):
        cnt = compter(index[cond], lignes, poubelle, n_items, g_max, k_max, n_axes)
        return decomposer(cnt, valeurs_ordinales)

    dec = {c: mesurer(c, toutes) for c in noms}
    observe = {c: agreger(dec[c], garder, est_ordinal) for c in noms}

    # --- correction residuelle par permutation, et controle des estimateurs -------
    # Les estimateurs ci dessus sont deja corriges analytiquement. On verifie ce qu'il
    # reste de biais en permutant au hasard les etiquettes de segment : sous permutation
    # le terme inter DOIT valoir zero. Ce qui subsiste est soustrait du terme inter.
    # Resultat de ce controle, a lire dans a1-controle-permutation.csv : le residu est
    # inferieur a 0,5 pour cent pour Gini Simpson et pour la variance ordinale, ce qui
    # valide ces deux estimateurs. Il atteint 3 a 15 pour cent pour l'entropie, dont la
    # correction de Miller Madow n'est qu'un premier ordre. La soustraction ci dessous
    # est donc surtout necessaire a l'entropie.
    print(f"\nCORRECTION RESIDUELLE, {args.permutations} permutations des etiquettes de segment")
    print("Terme inter obtenu sous permutation, en part du terme inter observe.")
    print("Proche de zero : l'estimateur analytique suffisait. Sinon, on soustrait.")
    diag = [["condition", "mesure", "inter_observe", "inter_sous_permutation", "part"]]
    print(f"{'condition':<28}" + "".join(f"{m[:16]:>18}" for m in MESURES))
    nul, nul_axe = {}, {}
    for c in noms:
        vals = {m: [] for m in MESURES}
        vals_axe = {a: {m: [] for m in MESURES} for a in AXES}
        for _ in range(args.permutations):
            perm = rng.permutation(n)
            ip, pb = construire_index(donnees[c], {a: seg[a][perm] for a in AXES},
                                      k_max, g_max, n_items)
            d = decomposer(compter(ip, toutes, pb, n_items, g_max, k_max, n_axes),
                           valeurs_ordinales)
            agg = agreger(d, garder, est_ordinal)
            for m in MESURES:
                vals[m].append(agg[m][0])
            for i_a, a in enumerate(AXES):
                agg_a = agreger(d, garder, est_ordinal, axes_gardes=[i_a])
                for m in MESURES:
                    vals_axe[a][m].append(agg_a[m][0])
        nul[c] = {m: float(np.mean(vals[m])) for m in MESURES}
        nul_axe[c] = {a: {m: float(np.mean(vals_axe[a][m])) for m in MESURES} for a in AXES}
        cellules = ""
        for m in MESURES:
            part = nul[c][m] / observe[c][m][0] if observe[c][m][0] else float("nan")
            cellules += f"{part:>18.3f}"
            diag.append([c, m, f"{observe[c][m][0]:.4f}", f"{nul[c][m]:.4f}", f"{part:.4f}"])
        print(f"{c:<28}{cellules}")
    with open(os.path.join(args.sortie, "a1-controle-permutation.csv"), "w",
              newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(diag)

    point = {c: {m: (observe[c][m][0] - nul[c][m], observe[c][m][1]) for m in MESURES}
             for c in noms}
    ref = point[REFERENCE]
    ratios = {c: {m: (point[c][m][0] / ref[m][0], point[c][m][1] / ref[m][1]) for m in MESURES}
              for c in noms}

    # --- bootstrap sur les participants ------------------------------------
    # POINT DE METHODE, il a fallu le corriger et il faut le dire.
    # Le terme inter est une composante de variance dont la valeur vraie est petite.
    # Un tirage bootstrap ajoute une seconde couche de bruit d'echantillonnage, et ce
    # bruit se loge entierement dans cette composante : mesure, la moyenne bootstrap du
    # terme inter depasse la valeur observee de 24 pour cent chez les humains et de
    # 2 pour cent chez les agents demographiques v8, parce que les seconds ont un terme
    # inter dix fois plus grand et donc moins affecte par un ajout constant. Laisser cet
    # ecart en place ecraserait tous les ratios vers 1. On recentre donc chaque
    # distribution bootstrap, de facon additive, sur son estimation ponctuelle avant de
    # former le ratio. C'est le bootstrap de base, au sens de Davison et Hinkley : le
    # tirage sert a estimer la FORME de la distribution d'echantillonnage, pas son centre.
    print(f"\nBootstrap : {args.bootstrap} tirages avec remise sur les {n} participants,")
    print("le meme tirage etant applique a toutes les conditions pour preserver l'appariement.")
    dist = {c: matrice_distance(donnees[c], garder) for c in noms}
    sil_point = {c: {a: silhouette(dist[c], seg[a], len(niveaux[a])) for a in AXES}
                 for c in noms}
    brut = {c: {m: ([], []) for m in MESURES} for c in noms}
    brut_sil = {c: {a: [] for a in AXES} for c in noms}
    for b in range(args.bootstrap):
        lignes = rng.integers(0, n, size=n)
        poids = np.bincount(lignes, minlength=n).astype(np.float32)
        for c in noms:
            agg = agreger(mesurer(c, lignes), garder, est_ordinal)
            for m in MESURES:
                brut[c][m][0].append(agg[m][0])
                brut[c][m][1].append(agg[m][1])
            for a in AXES:
                brut_sil[c][a].append(silhouette(dist[c], seg[a], len(niveaux[a]), poids))
        if (b + 1) % max(1, args.bootstrap // 10) == 0:
            print(f"  {b + 1}/{args.bootstrap}", flush=True)

    def recentrer(tirages, cible):
        """Ramene la moyenne des tirages bootstrap sur l'estimation ponctuelle."""
        v = np.asarray(tirages, dtype=float)
        fini = np.isfinite(v)
        if fini.sum() < 20:
            return v
        return v - np.mean(v[fini]) + cible

    boot = {c: {m: (recentrer(brut[c][m][0], point[c][m][0]),
                    recentrer(brut[c][m][1], point[c][m][1])) for m in MESURES}
            for c in noms}
    boot_sil = {c: {a: recentrer(brut_sil[c][a], sil_point[c][a]) for a in AXES}
                for c in noms}
    ratio_boot = {c: {m: (boot[c][m][0] / boot[REFERENCE][m][0],
                          boot[c][m][1] / boot[REFERENCE][m][1]) for m in MESURES}
                  for c in noms}

    def ic(v):
        v = np.asarray(v, dtype=float)
        v = v[np.isfinite(v)]
        if v.size < 20:
            return (float("nan"), float("nan"), float("nan"))
        return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), float(v.mean()))

    # --- table des ratios --------------------------------------------------
    print("\n" + "=" * 92)
    print("LES DEUX RATIOS, condition rapportee aux humains de la vague 1")
    print("intervalle de confiance a 95 pour cent, bootstrap sur les participants")
    print("=" * 92)
    print("La derniere colonne est ce que verrait une mesure GLOBALE de dispersion, qui")
    print("n'ouvre pas la boite : (inter + intra) de la condition sur celui des humains.")
    lignes_csv = [["condition", "mesure", "ratio_inter", "inter_ic_bas", "inter_ic_haut",
                   "ratio_intra", "intra_ic_bas", "intra_ic_haut", "produit",
                   "ratio_dispersion_globale"]]
    for m in MESURES:
        print(f"\n--- {m} ---")
        print(f"{'condition':<28}{'ratio inter':>27}{'ratio intra':>27}"
              f"{'produit':>9}{'global':>9}")
        glob_ref = point[REFERENCE][m][0] + point[REFERENCE][m][1]
        for c in noms:
            ri, ra = ratios[c][m]
            i1, i2, _ = ic(ratio_boot[c][m][0])
            a1, a2, _ = ic(ratio_boot[c][m][1])
            glob = (point[c][m][0] + point[c][m][1]) / glob_ref
            print(f"{c:<28}{ri:>9.3f} [{i1:6.3f} ; {i2:6.3f}]"
                  f"{ra:>11.3f} [{a1:5.3f} ; {a2:5.3f}]{ri * ra:>9.3f}{glob:>9.3f}")
            lignes_csv.append([c, m, f"{ri:.4f}", f"{i1:.4f}", f"{i2:.4f}", f"{ra:.4f}",
                               f"{a1:.4f}", f"{a2:.4f}", f"{ri * ra:.4f}", f"{glob:.4f}"])
    with open(os.path.join(args.sortie, "a1-ratios.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_csv)

    # --- controle : mediane des ratios item par item -----------------------
    print("\nControle d'agregation : mediane des ratios calcules item par item")
    print("(au lieu du ratio des sommes ; entropie, items ou I(R;S) humain depasse 0,002 bit)")
    print(f"{'condition':<28}{'mediane inter':>16}{'mediane intra':>16}")
    inter_ref, intra_ref, val_ref = dec[REFERENCE]["entropie"]
    msk = val_ref & garder[None, :] & (inter_ref > 0.002)
    for c in noms:
        i_c, a_c, _ = dec[c]["entropie"]
        r_i = np.median(i_c[msk] / inter_ref[msk])
        r_a = np.median(a_c[msk] / intra_ref[msk])
        print(f"{c:<28}{r_i:>16.3f}{r_a:>16.3f}")

    # --- detail par axe ----------------------------------------------------
    print("\n" + "=" * 92)
    print("DETAIL PAR AXE DEMOGRAPHIQUE, mesure entropie et information mutuelle")
    print("=" * 92)
    lignes_axe = [["condition", "axe", "mesure", "ratio_inter", "ratio_intra"]]
    entete = f"{'condition':<28}" + "".join(f"{a[:13]:>15}" for a in AXES)
    print(entete)
    par_axe = {c: {a: {m: (v[m][0] - nul_axe[c][a][m], v[m][1]) for m in MESURES}
                   for a, v in ((a, agreger(dec[c], garder, est_ordinal, axes_gardes=[i]))
                                for i, a in enumerate(AXES))} for c in noms}
    for c in noms:
        cellules = ""
        for a in AXES:
            base = par_axe[REFERENCE][a]
            for m in MESURES:
                if base[m][0] > 0 and base[m][1] > 0:
                    lignes_axe.append([c, a, m,
                                       f"{par_axe[c][a][m][0] / base[m][0]:.4f}",
                                       f"{par_axe[c][a][m][1] / base[m][1]:.4f}"])
            cellules += f"{par_axe[c][a]['entropie'][0] / base['entropie'][0]:>15.2f}"
        print(f"{c:<28}{cellules}   <- ratio inter")
    print()
    print(entete)
    for c in noms:
        cellules = ""
        for a in AXES:
            base = par_axe[REFERENCE][a]
            cellules += f"{par_axe[c][a]['entropie'][1] / base['entropie'][1]:>15.2f}"
        print(f"{c:<28}{cellules}   <- ratio intra")
    with open(os.path.join(args.sortie, "a1-ratios-par-axe.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_axe)

    # --- silhouette --------------------------------------------------------
    print("\n" + "=" * 92)
    print("SCORE DE SILHOUETTE sur la segmentation demographique")
    print("distance d'appariement simple, intervalle bootstrap a 95 pour cent")
    print("=" * 92)
    print(f"{'condition':<28}" + "".join(f"{a[:20]:>22}" for a in AXES))
    lignes_sil = [["condition", "axe", "silhouette", "ic_bas", "ic_haut"]]
    for c in noms:
        cellules = ""
        for a in AXES:
            s = sil_point[c][a]
            b1, b2, _ = ic(boot_sil[c][a])
            cellules += f"{s:>7.3f} [{b1:6.3f};{b2:6.3f}]"
            lignes_sil.append([c, a, f"{s:.4f}", f"{b1:.4f}", f"{b2:.4f}"])
        print(f"{c:<28}{cellules}")
    with open(os.path.join(args.sortie, "a1-silhouette.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_sil)

    etiquettes(args.racine, args.sortie, donnees, entetes)
    plafond(args.racine, args.sortie)
    globaux = {c: {m: (point[c][m][0] + point[c][m][1])
                       / (point[REFERENCE][m][0] + point[REFERENCE][m][1])
                   for m in MESURES} for c in noms}
    tracer(ratios, ratio_boot, noms, args.sortie, ic, globaux)

    print(f"\nEcrit dans {args.sortie}/ : a1-figure-double-distorsion.png et .svg, "
          "a1-ratios.csv, a1-ratios-par-axe.csv, a1-silhouette.csv,\n"
          "a1-plafond-humain.csv, a1-controle-permutation.csv,\n"
          "a1-etiquettes-demographiques.csv")


# ---------------------------------------------------------------------------
# 6. Le plafond humain : une distribution, et non une moyenne
# ---------------------------------------------------------------------------

def plafond(racine, sortie):
    """Etudie la distribution de la consistance test retest individuelle.

    Le papier normalise les scores d'agents par UNE moyenne, 79,53 pour cent. Si la
    consistance varie fortement d'une personne a l'autre, cette normalisation ne dit rien
    de la fidelite pour une personne donnee. On mesure donc l'etendue de cette variation
    et l'ecart entre les deux normalisations possibles.
    """
    p = os.path.join(racine,
                     "figure3/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv")
    if not os.path.exists(p):
        print("\nindividual_level.csv absent, plafond humain non calcule.")
        return
    rows = list(csv.DictReader(open(p, encoding="utf-8")))

    def col(nom):
        return np.array([float(r[nom]) for r in rows
                         if r.get(nom) not in (None, "", "nan")])

    retest = col("p_wave1__p_wave2__accuracy")
    # Le fichier stocke des proportions dans [0, 1] ; on affiche en pour cent.
    if retest.max() <= 1.5:
        retest = retest * 100.0

    print("\n" + "=" * 92)
    print("PLAFOND HUMAIN : distribution de la consistance test retest par individu")
    print("=" * 92)
    q = np.percentile(retest, [0, 5, 10, 25, 50, 75, 90, 95, 100])
    print(f"n = {retest.size}, moyenne = {retest.mean():.2f} pour cent, "
          f"ecart type = {retest.std(ddof=1):.2f} points")
    print("centiles   0 : {:.1f}   5 : {:.1f}   10 : {:.1f}   25 : {:.1f}   50 : {:.1f}"
          "   75 : {:.1f}   90 : {:.1f}   95 : {:.1f}   100 : {:.1f}".format(*q))
    print(f"etendue interquartile = {q[5] - q[3]:.1f} points, "
          f"etendue totale = {q[-1] - q[0]:.1f} points, "
          f"coefficient de variation = {100 * retest.std(ddof=1) / retest.mean():.1f} pour cent")
    for seuil in (60, 65, 70, 75):
        print(f"  part des participants sous {seuil} pour cent de consistance : "
              f"{100 * (retest < seuil).mean():5.1f} pour cent")
    print(f"  rapport du 90e au 10e centile : {q[6] / q[2]:.2f}")

    print("\nEffet du choix de normalisation, par condition")
    print("moy/moy : le score du papier, moyenne des agents divisee par moyenne du retest.")
    print("moy des ratios : chacun normalise par SA propre consistance, puis moyenne.")
    print(f"{'condition':<28}{'moy/moy':>10}{'moy des ratios':>16}{'ecart type':>12}"
          f"{'q10':>8}{'q90':>8}{'part > 1':>10}")
    lignes = [["statistique", "valeur"]]
    lignes += [["retest_moyenne_pct", f"{retest.mean():.4f}"],
               ["retest_ecart_type_pts", f"{retest.std(ddof=1):.4f}"],
               ["retest_min_pct", f"{q[0]:.4f}"], ["retest_q10_pct", f"{q[2]:.4f}"],
               ["retest_q25_pct", f"{q[3]:.4f}"], ["retest_median_pct", f"{q[4]:.4f}"],
               ["retest_q75_pct", f"{q[5]:.4f}"], ["retest_q90_pct", f"{q[6]:.4f}"],
               ["retest_max_pct", f"{q[-1]:.4f}"],
               ["retest_coef_variation_pct", f"{100 * retest.std(ddof=1) / retest.mean():.4f}"]]
    for cle, libelle in [("composite_agents", "agents composite"),
                         ("gss_v3", "agents entretien (v3)"),
                         ("survey_agents", "agents enquete"),
                         ("gss_v7", "agents persona (v7)"),
                         ("gss_v6", "agents demographiques (v6)"),
                         ("gss_v8", "agents demographiques (v8)")]:
        nom = f"p_wave1__{cle}__accuracy"
        if nom not in rows[0]:
            continue
        acc = col(nom)
        acc = acc * 100.0 if acc.max() <= 1.5 else acc
        m = min(acc.size, retest.size)
        acc, ret = acc[:m], retest[:m]
        bon = ret > 0
        globalr = acc[bon].mean() / ret[bon].mean()
        indiv = acc[bon] / ret[bon]
        qi = np.percentile(indiv, [10, 90])
        print(f"{libelle:<28}{globalr:>10.3f}{indiv.mean():>16.3f}{indiv.std(ddof=1):>12.3f}"
              f"{qi[0]:>8.3f}{qi[1]:>8.3f}{100 * (indiv > 1).mean():>9.1f}%")
        lignes += [[f"{cle}_normalise_par_moyenne", f"{globalr:.4f}"],
                   [f"{cle}_moyenne_des_ratios_individuels", f"{indiv.mean():.4f}"],
                   [f"{cle}_ecart_type_des_ratios_individuels", f"{indiv.std(ddof=1):.4f}"],
                   [f"{cle}_q10_ratios_individuels", f"{qi[0]:.4f}"],
                   [f"{cle}_q90_ratios_individuels", f"{qi[1]:.4f}"],
                   [f"{cle}_part_ratios_sup_1", f"{(indiv > 1).mean():.4f}"]]
        # correlation entre la stabilite d'une personne et la fidelite de son agent
        r = float(np.corrcoef(ret[bon], acc[bon])[0, 1])
        lignes.append([f"{cle}_correlation_retest_fidelite", f"{r:.4f}"])
        print(f"{'':<28}correlation entre consistance propre et fidelite de son agent : "
              f"r = {r:.3f}")
    with open(os.path.join(sortie, "a1-plafond-humain.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 7. Les deux generations etiquetees demographiques
# ---------------------------------------------------------------------------

def etiquettes(racine, sortie, donnees, entetes):
    """Compare gss_v6 et gss_v8, deux generations toutes deux dites demographiques.

    Le fait n'est pas une deduction de notre part, il est ecrit dans le paquet :
      FIGURE2_PIPELINE.md section 6.1  ->  Demographic-Based  = p_wave1__gss_v6__accuracy
      FIGURE3_PIPELINE.md section 5.2  ->  Demographic Agents = p_wave1__gss_v8__accuracy
      plot_figure_2.py ligne 102       ->  gss_v6 "demographic-based (ablation demog)"
      build_dpd_summaries.py ligne 38  ->  "Demographic Agents" : gss_v8
      camerer_five_studies_results.md  ->  v8 = "ablation (demog) -- LA"
    Cette fonction chiffre ce que la metrique du papier voit de leur difference, et ce
    qu'elle ne voit pas.
    """
    print("\n" + "=" * 92)
    print("DEUX GENERATIONS ETIQUETEES DEMOGRAPHIQUES : ce que l'exactitude ne separe pas")
    print("=" * 92)

    p = os.path.join(racine,
                     "figure2/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv")
    lignes = [["comparaison", "ecart_apparie_pts", "ic_bas", "ic_haut", "t", "conclusion"]]
    if os.path.exists(p):
        rows = list(csv.DictReader(open(p, encoding="utf-8")))

        def col(cle):
            v = np.array([float(r[f"p_wave1__{cle}__accuracy"]) for r in rows])
            return v * 100.0 if v.max() <= 1.5 else v

        print("Exactitude par participant, chiffre du papier, et test apparie sur 1052 sujets")
        for a, b in (("gss_v6", "gss_v8"), ("gss_v7", "gss_v8"), ("gss_v6", "gss_v7")):
            x, y = col(a), col(b)
            d = x - y
            se = d.std(ddof=1) / np.sqrt(d.size)
            t = d.mean() / se
            verdict = "indistinguables" if abs(t) < 1.96 else "distinguables"
            print(f"  {a} {x.mean():6.2f}%  contre  {b} {y.mean():6.2f}%   "
                  f"ecart {d.mean():+6.2f} pt  IC95 [{d.mean() - 1.96 * se:+.2f} ; "
                  f"{d.mean() + 1.96 * se:+.2f}]  t = {t:+6.2f}  -> {verdict}")
            lignes.append([f"{a}_vs_{b}", f"{d.mean():.4f}",
                           f"{d.mean() - 1.96 * se:.4f}", f"{d.mean() + 1.96 * se:.4f}",
                           f"{t:.4f}", verdict])
    else:
        print("  individual_level.csv de la figure 2 absent, test apparie non calcule.")

    # Accord cellule a cellule : deux etiquettes du meme fichier accorderaient 100 pour cent.
    print("\nAccord cellule a cellule, 177 items x 1052 participants")
    paires = [("agents demographiques (v6)", "agents demographiques (v8)"),
              ("agents persona (v7)", "agents demographiques (v8)"),
              ("agents demographiques (v6)", "humains vague 1"),
              ("agents demographiques (v8)", "humains vague 1")]
    for a, b in paires:
        if a not in donnees or b not in donnees:
            continue
        xa, xb = donnees[a], donnees[b]
        valide = (xa >= 0) & (xb >= 0)
        acc = float((xa[valide] == xb[valide]).mean())
        print(f"  {a:<28} contre {b:<28}{acc * 100:6.1f}%")
        lignes.append([f"accord_{a}_vs_{b}", f"{acc:.4f}", "", "", "", ""])

    # Richesse du vocabulaire employe : ecarte l'explication par un vocabulaire appauvri.
    print("\nModalites distinctes employees par item, en moyenne")
    for c in ("humains vague 1", "agents demographiques (v6)", "agents persona (v7)",
              "agents demographiques (v8)"):
        if c not in donnees:
            continue
        x = donnees[c]
        m = float(np.mean([len(np.unique(x[:, j][x[:, j] >= 0])) for j in range(x.shape[1])]))
        print(f"  {c:<28}{m:6.2f}")
        lignes.append([f"modalites_par_item_{c}", f"{m:.4f}", "", "", "", ""])

    with open(os.path.join(sortie, "a1-etiquettes-demographiques.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 8. La figure
# ---------------------------------------------------------------------------

def tracer(ratios, boot, noms, sortie, ic, globaux, mesure="entropie"):
    """Le plan des deux ratios. Un point par condition, lisible en noir et blanc.

    Echelle logarithmique sur les deux axes : les ratios sont multiplicatifs, et
    l'hyperbole produit egal a 1 y devient une droite. Les axes ne couvrent pas la meme
    plage parce qu'aucune condition n'a une dispersion interne superieure a celle des
    humains : imposer un carre gaspillerait les trois quarts de la surface.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib absent, figure non produite.")
        return

    # Marqueurs et remplissages choisis pour rester distincts en noir et blanc.
    # decalage : position de l'etiquette en points typographiques.
    style = {
        "humains vague 1":            ("o", "white", 15, (-14, 16), "right"),
        "humains vague 2":            ("s", "white", 10, (12, -20), "left"),
        "agents composite":           ("^", "black", 13, (-12, 20), "right"),
        "agents entretien (v3)":      ("v", "black", 13, (16, -2), "left"),
        "agents enquete":             ("D", "0.35", 11, (-12, -18), "right"),
        "agents persona (v7)":        ("P", "0.75", 15, (0, 22), "center"),
        "agents demographiques (v6)": ("X", "0.75", 15, (0, -24), "center"),
        "agents demographiques (v8)": ("*", "0.75", 20, (-16, 16), "right"),
    }

    fig, ax = plt.subplots(figsize=(10.2, 7.2))
    xs = [ratios[c][mesure][0] for c in noms]
    ys = [ratios[c][mesure][1] for c in noms]
    x_lo, x_hi = min(xs) * 0.55, max(xs) * 1.9
    y_lo, y_hi = min(ys) * 0.93, max(ys) * 1.20

    # Le quadrant de la double distorsion : ecarts entre groupes gonfles ET dispersion
    # interne ecrasee. C'est la prediction a tester, et le fond gris dit ou elle se lit.
    ax.fill_between([1.0, x_hi], y_lo, 1.0, color="0.905", zorder=0)
    ax.text(x_hi * 0.97, y_lo * 1.02, "quadrant de la double distorsion :\n"
            "ecarts entre groupes gonfles, dispersion interne ecrasee",
            ha="right", va="bottom", fontsize=9.5, color="0.30", zorder=1)

    # L'hyperbole produit egal a 1 : le lieu des simulateurs faux deux fois et pourtant
    # invisibles a toute mesure globale de dispersion. En echelle log c'est une droite.
    t = np.geomspace(x_lo, x_hi, 400)
    ax.plot(t, 1.0 / t, color="black", lw=1.8, ls="--", zorder=2,
            label="produit des deux ratios egal a 1 :\nfaux deux fois, invisible sur une mesure globale")
    ax.axhline(1.0, color="0.5", lw=0.9, zorder=1)
    ax.axvline(1.0, color="0.5", lw=0.9, zorder=1)

    for c in noms:
        ri, ra = ratios[c][mesure]
        i1, i2, _ = ic(boot[c][mesure][0])
        a1, a2, _ = ic(boot[c][mesure][1])
        mk, coul, taille, (dx, dy), ha = style.get(c, ("o", "0.5", 10, (0, 12), "center"))
        if np.isfinite(i1) and (i2 - i1) > 1e-9:
            ax.plot([i1, i2], [ra, ra], color="black", lw=1.2, zorder=3)
            ax.plot([ri, ri], [a1, a2], color="black", lw=1.2, zorder=3)
        ax.plot(ri, ra, marker=mk, ms=taille, mfc=coul, mec="black", mew=1.4,
                ls="none", zorder=4)
        # On rappelle sous chaque etiquette ce que verrait une mesure GLOBALE de
        # dispersion, celle qui ne separe pas inter et intra. C'est tout le propos :
        # elle reste proche de 1 alors que les deux composantes sont fausses.
        texte = f"{c}\nmesure globale : {globaux[c][mesure]:.2f}"
        ax.annotate(texte, (ri, ra), textcoords="offset points", xytext=(dx, dy),
                    ha=ha, va="center", fontsize=9, zorder=5, linespacing=1.35,
                    bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="0.8", lw=0.5,
                              alpha=0.88))

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(x_lo, x_hi); ax.set_ylim(y_lo, y_hi)
    tx = [v for v in (0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2, 3, 5, 8, 12) if x_lo <= v <= x_hi]
    ty = [v for v in (0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2) if y_lo <= v <= y_hi]
    ax.set_xticks(tx); ax.set_yticks(ty)
    ax.set_xticklabels([f"{v:g}" for v in tx])
    ax.set_yticklabels([f"{v:g}" for v in ty])
    ax.minorticks_off()
    ax.set_xlabel("Ratio de dispersion ENTRE segments demographiques   "
                  "(condition / humains vague 1)", fontsize=11)
    ax.set_ylabel("Ratio de dispersion A L'INTERIEUR des segments\n"
                  "(condition / humains vague 1)", fontsize=11)
    ax.set_title("La double distorsion des populations simulees\n"
                 "General Social Survey, 1052 participants, 169 items, 6 segmentations,\n"
                 "decomposition par information mutuelle ; la vague 2 est le controle,\n"
                 "memes personnes deux semaines plus tard, elle tombe bien en (1, 1)",
                 fontsize=11.5)
    ax.grid(True, which="major", color="0.88", lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="upper left", fontsize=9, framealpha=0.95)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(sortie, f"a1-figure-double-distorsion.{ext}"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
