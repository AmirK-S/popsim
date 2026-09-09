"""
a30_commun : briques partagees par les scripts a30, « la droite est elle plus variee
que la gauche ».

Statut : script d'analyse jetable. Aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a2_baselines_gss, a25_commun,
a25_mesures, a28_commun et a9_commun sont importes tels quels.

Ce module porte cinq choses.

  1. La definition des camps, sur les deux jeux : GSS (trois blocs, sept points, parti)
     et Twin-2K-500 (trois blocs, cinq points, parti).
  2. Deux estimateurs de dispersion interne, item par item et camp par camp, identiques
     a ceux de a1 et a28 : indice de Gini Simpson sans biais et entropie de Shannon
     corrigee par Miller Madow.
  3. Un moteur de reechantillonnage unique, par poids sur les personnes, qui sert a la
     fois au bootstrap (poids multinomiaux), au test de permutation (poids 0/1 permutes),
     a la rarefaction (poids 0/1 tires sans remise) et a l'appariement demographique
     (poids 0/1 tires cellule par cellule).
  4. Le classement des 149 items du GSS en familles de sujets.
  5. Les corrections pour tests multiples, reprises de a28_commun.

Motif du moteur par poids. Toutes ces operations reviennent a recompter les modalites
d'un item sur un sous ensemble pondere de personnes. On precalcule donc une matrice
indicatrice (personnes x items x modalites) aplatie, et un jeu de B poids donne les B
tables de contingence en un seul produit matriciel. Le bootstrap sur les personnes,
exige par le cahier des charges, devient alors gratuit.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

from a28_commun import holm, benjamini_hochberg  # noqa: E402,F401

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
LN2 = np.log(2.0)

GRAINE = 20260908
N_MIN_ITEM = 30      # cellules exploitables minimales dans un camp pour qu'un item compte
N_BOOT = 1000        # tirages de bootstrap sur les personnes
N_PERM = 2000        # permutations d'etiquette de camp


# ---------------------------------------------------------------------------
# 1. Camps
# ---------------------------------------------------------------------------
#
# Trois definitions, declarees avant de regarder le moindre resultat.
#
#   bloc3    : gauche / centre / droite. C'est la partition de a1 (regle mecanique sur
#              le libelle) et celle sur laquelle porte l'hypothese principale.
#   points7  : les sept niveaux de polviews du GSS, cinq pour Twin. Sert a verifier que
#              le resultat n'est pas un artefact du repliement en trois blocs, et a
#              regarder separement les extremes, moins exposes a l'erreur de classement
#              (polviews a une fiabilite de 0,66, cf. corpus/05, 05-06).
#   parti    : identification partisane. Fiabilite 0,84 sur le GSS, donc ancrage plus
#              solide que l'ideologie declaree ; c'est le controle le plus important du
#              volet 1, parce qu'une difference qui ne survit pas au changement d'ancrage
#              n'est pas une difference entre camps mais une difference d'echelle.

GSS_BLOC3 = {
    "extremely liberal": "gauche", "liberal": "gauche", "slightly liberal": "gauche",
    "moderate": "centre",
    "slightly conservative": "droite", "conservative": "droite",
    "extremely conservative": "droite",
}
GSS_POINTS7 = ["extremely liberal", "liberal", "slightly liberal", "moderate",
               "slightly conservative", "conservative", "extremely conservative"]
# Repliement partisan standard : les « independants proches de » sont comptes avec le
# parti dont ils se disent proches, convention majoritaire en science politique
# americaine. « other party » (25 personnes) est ecarte, il ne se range d'aucun cote.
GSS_PARTI3 = {
    "strong democrat": "gauche", "not very strong democrat": "gauche",
    "independent, close to democrat": "gauche",
    "independent (neither)": "centre",
    "independent, close to republican": "droite",
    "not very strong republican": "droite", "strong republican": "droite",
}

TWIN_BLOC3 = {5: "gauche", 4: "gauche", 3: "centre", 2: "droite", 1: "droite"}
TWIN_POINTS5 = {1: "tres conservateur", 2: "conservateur", 3: "modere",
                4: "liberal", 5: "tres liberal"}
TWIN_PARTI3 = {2: "gauche", 3: "centre", 1: "droite"}  # QID20 : 1 rep, 2 dem, 3 indep


def camps_gss(x, attributs):
    """Renvoie un dictionnaire de partitions pour les 1 052 participants du GSS.

    x, attributs viennent de a2_baselines_gss.charger().
    Chaque partition est un tableau d'etiquettes de type objet, None si non classable.
    """
    col = {a: i for i, a in enumerate(attributs)}
    ideo = [str(v).strip().lower() for v in x[:, col["political_ideology"]]]
    parti = [str(v).strip().lower() for v in x[:, col["political_party"]]]
    return {
        "bloc3": np.array([GSS_BLOC3.get(v) for v in ideo], dtype=object),
        "points7": np.array([v if v in GSS_POINTS7 else None for v in ideo], dtype=object),
        "parti3": np.array([GSS_PARTI3.get(v) for v in parti], dtype=object),
    }


def camps_twin(w13):
    """Memes partitions sur Twin-2K-500, a partir de QID22 (ideologie) et QID20 (parti)."""
    ideo = w13["QID22"]
    parti = w13["QID20"]
    return {
        "bloc3": np.array([TWIN_BLOC3.get(v if v == v else None) for v in ideo], dtype=object),
        "points5": np.array([TWIN_POINTS5.get(v if v == v else None) for v in ideo], dtype=object),
        "parti3": np.array([TWIN_PARTI3.get(v if v == v else None) for v in parti], dtype=object),
    }


# ---------------------------------------------------------------------------
# 2. Indicatrice aplatie et estimateurs de dispersion
# ---------------------------------------------------------------------------

class Indicatrice:
    """Matrice indicatrice (personnes x items x modalites) aplatie en (personnes, J*K).

    codes : matrice d'entiers (n, J), -1 pour une cellule vide.
    k_par_item : nombre de modalites declarees de chaque item.
    """

    def __init__(self, codes, k_par_item):
        codes = np.asarray(codes)
        self.n, self.J = codes.shape
        self.k = int(max(k_par_item))
        self.k_par_item = np.asarray(k_par_item, dtype=int)
        oh = np.zeros((self.n, self.J * self.k), dtype=np.float32)
        li, lj = np.nonzero(codes >= 0)
        oh[li, lj * self.k + codes[li, lj]] = 1.0
        self.oh = oh

    def tables(self, poids):
        """poids : (B, n). Retourne les tables de contingence (B, J, K)."""
        p = np.asarray(poids, dtype=np.float32)
        if p.ndim == 1:
            p = p[None, :]
        return (p @ self.oh).reshape(p.shape[0], self.J, self.k)


def gini_simpson_sans_biais(c):
    """1 - somme p^2, estimateur sans biais somme n_k (n_k - 1) / (N (N - 1)).

    c : tables (B, J, K). Retourne (B, J), NaN si N < 2.
    """
    N = c.sum(axis=2)
    den = np.where(N > 1.0, N * (N - 1.0), np.nan)
    return 1.0 - (c * (c - 1.0)).sum(axis=2) / den


def entropie_miller_madow(c):
    """Entropie de Shannon en bits, correction de Miller Madow. c : (B, J, K)."""
    N = c.sum(axis=2)
    Ns = np.where(N > 0, N, np.nan)
    p = c / Ns[:, :, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        lg = np.where(p > 0, np.log2(np.maximum(p, 1e-300)), 0.0)
    h = -(p * lg).sum(axis=2)
    m = (c > 0).sum(axis=2)
    return h + (m - 1.0) / (2.0 * Ns * LN2)


def mesures(c):
    """Les deux dispersions, plus l'effectif. c : (B, J, K)."""
    return {"gs": gini_simpson_sans_biais(c),
            "h": entropie_miller_madow(c),
            "n": c.sum(axis=2)}


# ---------------------------------------------------------------------------
# 3. Jeux de poids
# ---------------------------------------------------------------------------

def poids_plein(masque):
    """Poids 1 sur les personnes du camp, 0 ailleurs. Forme (1, n)."""
    return np.asarray(masque, dtype=np.float32)[None, :]


def poids_bootstrap(masque, b, rng):
    """Bootstrap sur les personnes : multiplicites multinomiales dans le camp.

    Reechantillonner les personnes et non les cellules est impose par la structure des
    donnees : les 149 reponses d'un individu ne sont pas independantes.
    """
    idx = np.flatnonzero(masque)
    n = len(idx)
    if n < 2:
        return np.zeros((b, len(masque)), dtype=np.float32)
    mult = rng.multinomial(n, np.full(n, 1.0 / n), size=b).astype(np.float32)
    w = np.zeros((b, len(masque)), dtype=np.float32)
    w[:, idx] = mult
    return w


def poids_rarefaction(masque, taille, b, rng):
    """Tirage sans remise de `taille` personnes dans le camp, b fois.

    Sert a neutraliser l'effet de la taille du camp sur l'entropie de Miller Madow,
    dont la correction n'est qu'un premier ordre et depend de N. L'estimateur de Gini
    Simpson employe ici est sans biais et n'a pas besoin de ce controle ; on le calcule
    quand meme sur les memes sous echantillons, pour que les deux mesures soient lues
    sur exactement les memes personnes.
    """
    idx = np.flatnonzero(masque)
    w = np.zeros((b, len(masque)), dtype=np.float32)
    if len(idx) < taille:
        return w
    for t in range(b):
        w[t, rng.choice(idx, size=taille, replace=False)] = 1.0
    return w


def poids_appariement(masque_a, masque_b, cellules, b, rng):
    """Sous echantillons apparies : meme composition demographique exacte des deux cotes.

    cellules : vecteur d'etiquettes de cellule demographique, une par personne. Pour
    chaque cellule on tire le meme nombre de personnes de chaque cote, ce nombre etant
    le minimum des deux effectifs. Le resultat est une paire de sous echantillons dont
    la distribution jointe des attributs de controle est identique par construction :
    une difference de dispersion qui survit a cette operation n'est pas une difference
    de composition.

    Retourne (poids_a, poids_b) de forme (b, n), et la taille appariee.
    """
    a = np.zeros((b, len(masque_a)), dtype=np.float32)
    bb = np.zeros((b, len(masque_b)), dtype=np.float32)
    cell = np.asarray(cellules, dtype=object)
    total = 0
    for c in sorted({v for v in cell if v is not None}, key=str):
        ia = np.flatnonzero(masque_a & (cell == c))
        ib = np.flatnonzero(masque_b & (cell == c))
        m = min(len(ia), len(ib))
        if m == 0:
            continue
        total += m
        for t in range(b):
            a[t, rng.choice(ia, size=m, replace=False)] = 1.0
            bb[t, rng.choice(ib, size=m, replace=False)] = 1.0
    return a, bb, total


def poids_permutation(masque_a, masque_b, b, rng):
    """Permutation de l'etiquette de camp entre les deux camps, effectifs conserves."""
    idx = np.flatnonzero(masque_a | masque_b)
    na = int(masque_a.sum())
    a = np.zeros((b, len(masque_a)), dtype=np.float32)
    bb = np.zeros((b, len(masque_a)), dtype=np.float32)
    for t in range(b):
        p = rng.permutation(idx)
        a[t, p[:na]] = 1.0
        bb[t, p[na:]] = 1.0
    return a, bb


# ---------------------------------------------------------------------------
# 4. Agregation et contraste droite / gauche
# ---------------------------------------------------------------------------

def agreger(val, items_gardes):
    """Moyenne d'une mesure sur un jeu d'items fixe.

    val : (B, J). items_gardes : masque booleen (J,), calcule une fois sur l'estimation
    ponctuelle et jamais recalcule a l'interieur d'un reechantillonnage, faute de quoi
    le denominateur bougerait d'un tirage a l'autre et le ratio ne porterait plus sur
    les memes items.
    On moyenne item par item plutot que de sommer : les familles n'ont pas le meme
    nombre d'items et un ratio de sommes serait domine par la plus grosse.
    """
    m = items_gardes[None, :] & np.isfinite(val)
    s = np.where(m, val, 0.0).sum(axis=1)
    c = m.sum(axis=1)
    return np.where(c > 0, s / np.maximum(c, 1), np.nan)


def masque_items(ind, masque_a, masque_b, items_famille, n_min=N_MIN_ITEM):
    """Items retenus : ceux de la famille, remplis a n_min au moins dans les deux camps."""
    na = ind.tables(poids_plein(masque_a)).sum(axis=2)[0]
    nb = ind.tables(poids_plein(masque_b)).sum(axis=2)[0]
    return items_famille & (na >= n_min) & (nb >= n_min)


def contraste(ind, masque_a, masque_b, items_gardes, rng,
              n_boot=N_BOOT, n_perm=N_PERM, mesure="gs"):
    """Rapport camp A sur camp B d'une dispersion agregee, avec IC et p de permutation.

    A est le numerateur (la droite dans tout le rapport), B le denominateur (la gauche).
    IC : bootstrap sur les personnes, percentiles a 2,5 et 97,5 pour cent, les deux
    camps etant reechantillonnes independamment dans le meme tirage.
    p : test de permutation de l'etiquette de camp, estimateur de Phipson et Smyth,
    statistique bilaterale sur le logarithme du rapport.
    """
    ta = ind.tables(poids_plein(masque_a))
    tb = ind.tables(poids_plein(masque_b))
    va = agreger(mesures(ta)[mesure], items_gardes)[0]
    vb = agreger(mesures(tb)[mesure], items_gardes)[0]
    r = va / vb if vb and np.isfinite(vb) else np.nan

    ic = (np.nan, np.nan)
    if n_boot:
        wa = poids_bootstrap(masque_a, n_boot, rng)
        wb = poids_bootstrap(masque_b, n_boot, rng)
        xa = agreger(mesures(ind.tables(wa))[mesure], items_gardes)
        xb = agreger(mesures(ind.tables(wb))[mesure], items_gardes)
        d = xa / xb
        d = d[np.isfinite(d)]
        if len(d) > 10:
            ic = (float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5)))

    p = np.nan
    if n_perm:
        pa, pb = poids_permutation(masque_a, masque_b, n_perm, rng)
        xa = agreger(mesures(ind.tables(pa))[mesure], items_gardes)
        xb = agreger(mesures(ind.tables(pb))[mesure], items_gardes)
        stat = xa / xb
        stat = stat[np.isfinite(stat)]
        if len(stat) > 10 and np.isfinite(r):
            ge = int((np.abs(np.log(stat)) >= abs(np.log(r)) - 1e-12).sum())
            p = (ge + 1.0) / (len(stat) + 1.0)
    return {"valeur_a": float(va), "valeur_b": float(vb), "ratio": float(r),
            "ic_bas": ic[0], "ic_haut": ic[1], "p": float(p),
            "n_items": int(items_gardes.sum())}


def p_permutation_par_item(ind, masque_a, masque_b, ratio_obs, n_perm, rng,
                           mesure="gs", morceau=2000):
    """p de permutation item par item, calcule par morceaux pour tenir en memoire.

    La statistique est la valeur absolue du logarithme du rapport, donc le test est
    bilateral et symetrique en droite / gauche. Estimateur de Phipson et Smyth :
    (b + 1) / (m + 1), jamais nul, ce qui evite d'ecrire « p = 0 » apres correction.
    """
    obs = np.asarray(ratio_obs, dtype=float)
    with np.errstate(divide="ignore", invalid="ignore"):
        stat_obs = np.abs(np.log(obs))
    compte = np.zeros(ind.J)
    total = np.zeros(ind.J)
    fait = 0
    while fait < n_perm:
        b = min(morceau, n_perm - fait)
        pa, pb = poids_permutation(masque_a, masque_b, b, rng)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = mesures(ind.tables(pa))[mesure] / mesures(ind.tables(pb))[mesure]
            s = np.abs(np.log(r))
        valide = np.isfinite(s)
        total += valide.sum(axis=0)
        compte += (valide & (s >= stat_obs[None, :] - 1e-12)).sum(axis=0)
        fait += b
    p = np.where(total >= 100, (compte + 1.0) / (total + 1.0), np.nan)
    return np.where(np.isfinite(stat_obs), p, np.nan)


# ---------------------------------------------------------------------------
# 5. Familles de sujets du GSS
# ---------------------------------------------------------------------------
#
# Les six premieres sont celles de a2_baselines_gss.FAMILLES, reprises sans changement.
# Les 91 items restants sont classes a la lecture du libelle dans question_master, en
# trois categories et pas deux : « attitude sociale », « attitude economique » et « hors
# axe ». La troisieme categorie existe parce que forcer un item comme « avez vous un
# ordinateur » dans un des deux axes fabriquerait de la variete la ou il n'y a qu'un fait
# personnel. Elle est rapportee comme les autres, jamais fondue dans les deux axes.
#
# Regle employee, ecrite avant le classement : est « economique » un item qui porte sur
# l'argent, le travail, l'impot, la redistribution ou la position materielle ; est
# « social » un item qui porte sur la morale, la famille, la religion normative, la
# race, l'ordre public, l'immigration ou les libertes ; est « hors axe » un item qui
# demande un fait biographique, un comportement, un equipement ou un etat de sante.

CLASSEMENT_RESTANTS = {
    # --- attitudes sociales -------------------------------------------------
    "prayer": "social", "courts": "social", "cappun": "social", "grass": "social",
    "gunlaw": "social", "spanking": "social", "divlaw": "social", "sexeduc": "social",
    "pillok": "social", "xmarsex": "social", "homosex": "social", "marhomo": "social",
    "pornlaw": "social", "aged": "social", "letin1a": "social", "uswary": "social",
    "polhitok/y": "social", "polabuse/y": "social", "polattak/y": "social",
    "racdif1": "social", "racdif2": "social", "racdif3": "social", "racdif4": "social",
    "discaff": "social", "discaffw": "social", "discaffm": "social",
    "bible": "social", "postlife": "social", "reborn": "social", "savesoul": "social",
    "attend": "social", "pray": "social", "wlthwhts": "social", "wlthblks": "social",
    "wlthhsps": "social",
    "fair": "social", "helpful": "social", "trust": "social",
    "vote16": "social", "pres16": "social", "if16who": "social",
    # --- attitudes economiques ----------------------------------------------
    "tax": "economique", "getahead": "economique", "class": "economique",
    "satfin": "economique", "finalter": "economique", "finrela": "economique",
    "parsol": "economique", "kidssol": "economique", "income": "economique",
    "incom16": "economique", "joblose": "economique", "jobfind": "economique",
    "satjob": "economique", "richwork": "economique", "union1": "economique",
    # --- hors axe : faits, comportements, equipement, sante -----------------
    "mobile16": "hors axe", "dwelown16": "hors axe", "divorced": "hors axe",
    "posslq/y": "hors axe", "wrkstat": "hors axe", "evwork": "hors axe",
    "wrkgovt1": "hors axe", "wrkgovt2": "hors axe", "partfull": "hors axe",
    "wksub1": "hors axe", "wksup1": "hors axe", "unemp": "hors axe",
    "happy": "hors axe", "hapmar": "hors axe", "life": "hors axe",
    "health": "hors axe", "news": "hors axe", "owngun": "hors axe",
    "hunt1": "hors axe", "racwork": "hors axe", "spdeg*": "hors axe",
    "spjew": "hors axe", "spfund": "hors axe", "jew": "hors axe",
    "relig16*": "hors axe", "jew16*": "hors axe", "granborn": "hors axe",
    "uscitzn*": "hors axe", "fucitzn": "hors axe", "mnthsusa": "hors axe",
    "othlang": "hors axe", "compuse*": "hors axe", "webmob": "hors axe",
    "usewww*": "hors axe", "xmovie": "hors axe",
}


def familles_gss(items):
    """item -> famille de sujet. Les six familles thematiques, puis les trois residus."""
    from a2_baselines_gss import FAMILLES
    f = {}
    for nom, liste in FAMILLES.items():
        for it in liste:
            f[it] = nom
    out = {}
    inconnus = []
    for it in items:
        if it in f:
            out[it] = f[it]
        elif it in CLASSEMENT_RESTANTS:
            out[it] = "residu : " + CLASSEMENT_RESTANTS[it]
        else:
            inconnus.append(it)
            out[it] = "residu : hors axe"
    if inconnus:
        print(f"AVERTISSEMENT : {len(inconnus)} items non classes, ranges hors axe : "
              f"{inconnus}", flush=True)
    return out


# Axes de structure, pour la correlation social contre economique a l'interieur d'un camp.
# Reprise de corpus/05 section 5, amputee de ce qui n'existe pas dans le sous ensemble
# de 149 items de Stanford : eqwlth, helppoor, helpsick, helpblk, helpnot, premarsx et
# teensex en sont absents. L'axe economique se reduit donc a la batterie de depenses
# publiques et a l'impot, ce qui est une limite a declarer.
AXE_ECONOMIQUE = ["natspac/y", "natenvir/y", "natheal/y", "natcity/y", "natdrug/y",
                  "nateduc/y", "natrace/y", "natarms/y", "nataid/y", "natfare/y",
                  "natroad", "natsoc", "natmass", "natpark", "natchld", "natsci",
                  "natenrgy", "tax"]
AXE_SOCIAL = ["abdefect", "abnomore", "abhlth", "abpoor", "abrape", "absingle", "abany",
              "fehire", "fechld", "fepresch", "fefam", "fepol",
              "homosex", "xmarsex", "marhomo", "pillok", "pornlaw", "sexeduc",
              "divlaw", "spanking", "prayer", "bible", "cappun", "courts", "gunlaw",
              "grass"]


# ---------------------------------------------------------------------------
# 6. Cellules demographiques de controle
# ---------------------------------------------------------------------------

def cellules_gss(x, attributs):
    """Cellule demographique de controle : genre x race x age replie x education replie.

    Age et education sont replies en trois niveaux pour que les cellules gardent des
    effectifs appariables : 2 x 3 x 3 x 3 = 54 cellules pour 1 052 personnes.
    """
    col = {a: i for i, a in enumerate(attributs)}
    g = [str(v).strip().lower() for v in x[:, col["gender"]]]
    r = [str(v).strip().lower() for v in x[:, col["race"]]]
    a = [str(v).strip().lower() for v in x[:, col["age"]]]
    e = [str(v).strip().lower() for v in x[:, col["education"]]]

    def age3(v):
        if v.startswith("18") or v.startswith("25"):
            return "18-34"
        if v.startswith("35") or v.startswith("45"):
            return "35-54"
        return "55+"

    def edu3(v):
        if "less than" in v or v == "high school":
            return "bas"
        if "graduate" == v:
            return "haut"
        return "moyen"

    return np.array([f"{gg}|{rr}|{age3(aa)}|{edu3(ee)}"
                     for gg, rr, aa, ee in zip(g, r, a, e)], dtype=object)


def cellules_twin(w13):
    """Meme controle sur Twin : QID12 genre x QID15 ethnicite x QID13 age x QID14 educ."""
    def edu3(v):
        if v != v:
            return None
        return {1: "bas", 2: "bas", 3: "moyen", 4: "moyen", 5: "haut", 6: "haut"}.get(int(v))

    out = []
    for g, r, a, e in zip(w13["QID12"], w13["QID15"], w13["QID13"], w13["QID14"]):
        if any(v != v for v in (g, r, a, e)):
            out.append(None)
        else:
            out.append(f"{int(g)}|{int(r)}|{int(a)}|{edu3(e)}")
    return np.array(out, dtype=object)


# ---------------------------------------------------------------------------
# 7. Codage
# ---------------------------------------------------------------------------

def coder_gss(matrice, items, options):
    """Reponses en clair -> entiers, dans l'ordre de question_master. -1 pour vide."""
    from a2_commun import est_manquant
    n, m = matrice.shape
    codes = np.full((n, m), -1, dtype=np.int32)
    for j, it in enumerate(items):
        index = {o: k for k, o in enumerate(options[it])}
        for i in range(n):
            v = matrice[i, j]
            if v is None or est_manquant(v):
                continue
            k = index.get(str(v).lower().strip())
            if k is not None:
                codes[i, j] = k
    return codes, np.array([len(options[it]) for it in items], dtype=int)


def coder_numerique(df, colonnes):
    """DataFrame de codes numeriques -> entiers 0..K-1 par colonne, -1 pour NaN."""
    n, m = len(df), len(colonnes)
    codes = np.full((n, m), -1, dtype=np.int32)
    ks = np.zeros(m, dtype=int)
    for j, c in enumerate(colonnes):
        v = pd.to_numeric(df[c], errors="coerce").to_numpy(dtype=float)
        ok = ~np.isnan(v)
        if ok.sum() == 0:
            ks[j] = 1
            continue
        mods = np.unique(v[ok])
        table = {m_: i for i, m_ in enumerate(mods)}
        codes[ok, j] = [table[m_] for m_ in v[ok]]
        ks[j] = len(mods)
    return codes, np.maximum(ks, 1)


def coder_numerique_commun(dfs, colonnes):
    """Code plusieurs tableaux avec une table de modalites COMMUNE, colonne par colonne.

    Indispensable pour comparer humains et agents : si chaque tableau construisait sa
    propre table, une modalite absente chez l'agent decalerait tous les codes suivants
    et l'entropie ne porterait plus sur le meme alphabet.
    """
    m = len(colonnes)
    ks = np.zeros(m, dtype=int)
    tables = []
    for j, c in enumerate(colonnes):
        vals = []
        for d in dfs:
            v = pd.to_numeric(d[c], errors="coerce").to_numpy(dtype=float)
            vals.append(v[~np.isnan(v)])
        mods = np.unique(np.concatenate(vals)) if vals else np.array([])
        tables.append({m_: i for i, m_ in enumerate(mods)})
        ks[j] = max(len(mods), 1)
    sorties = []
    for d in dfs:
        codes = np.full((len(d), m), -1, dtype=np.int32)
        for j, c in enumerate(colonnes):
            v = pd.to_numeric(d[c], errors="coerce").to_numpy(dtype=float)
            ok = ~np.isnan(v)
            if ok.sum():
                codes[ok, j] = [tables[j][x] for x in v[ok]]
        sorties.append(codes)
    return sorties, ks


def ecrire(df, nom):
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, nom)
    df.to_csv(chemin, index=False, float_format="%.6f")
    print(f"ecrit : {chemin}", flush=True)
    return chemin
