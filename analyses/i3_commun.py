"""
i3_commun : briques du detecteur non supervise de population synthetique dans un flux de
reponses fermees (idee I3 du brainstorm d'impact, jour 4).

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels a44_commun, et par lui
a28_commun, a29_commun, a31_commun, a35_commun, a2_commun, a8_commun. Le codage entier, la
segmentation, le generateur nul de Yuan, les vingt sous ensembles d'items, le comptage des
patrons distincts et la correlation residualisee viennent de a44 sans une ligne recopiee.

LE PREENREGISTREMENT EST resultats/i3-preenregistrement.md, ECRIT AVANT CE FICHIER.

Ce module porte cinq choses et rien d'autre.

  1. Le chargement du paquet et le codage entier des seize matrices, par a44_commun.

  2. La construction d'un flux melange : effectif constant a 1 052 lignes, remplacement en
     place de round(tau * N) personnes par la ligne que la source synthetique produit pour
     CETTE personne, demographies jamais touchees, masque = intersection du masque humain
     et du masque de la source (preenregistrement, section 3).

  3. Les trois statistiques non supervisees du preenregistrement section 4 :
       A  deficit relatif de patrons distincts par rapport au nul du flux lui meme,
       B  exces de correlation inter items residualisee sur le segment,
       C  concentration par segment, part du patron modal du segment.
     Chacune ne prend en entree que la matrice de reponses et la colonne d'ideologie.

  4. Le reechantillonnage de la reference humaine : bootstrap classique pour B, sous
     echantillonnage sans remise a m = N/2 remis a l'echelle pour A et C, parce qu'un
     tirage avec remise duplique des personnes et fausse ces deux la (a44, section 0).

  5. La mesure de polarisation d'I4, ecart gauche droite signe sur les rangs.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a44_commun as C44
from a28_commun import norm as _norm, _bloc_ideologie

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260909
TAUX = [0.0, 0.05, 0.10, 0.25, 0.50]
N_TIRAGES = 20            # D, tirages de melange par couple (source, taux)
N_NUL = 40                # R, replicats du generateur nul par flux
N_BOOTSTRAP = 1000        # B, reference humaine
N_VALIDATION = 60         # K, populations independantes du controle 8.4
Z_ALPHA = 1.959963985     # bilateral 5 pour cent
Z_HOLM = 3.113            # bilateral 0,05 / 27
Z_PUISSANCE = 0.8416212   # puissance 80 pour cent

# Les neuf sources du preenregistrement section 2. B0 segment est construit ici, il n'est
# pas dans le paquet ; les huit autres sont relues telles quelles.
SOURCES = [
    "agents v8", "agents demographiques (v6)", "agents composite",
    "C2", "C3",
    "PMM k=10", "E2 regression contexte tirage", "IM m=10 mode des m",
    "B0 segment",
]
FAMILLE = {
    "agents v8": "modele a etiquette",
    "agents demographiques (v6)": "modele a demographies",
    "agents composite": "modele riche",
    "C2": "modele a etiquette",
    "C3": "modele riche",
    "PMM k=10": "imputation par tirage",
    "E2 regression contexte tirage": "imputation par tirage",
    "IM m=10 mode des m": "imputation par esperance",
    "B0 segment": "tirage dans le segment",
}
# Perimetre restreint : C2 et C3 n'existent que sur 150 personnes, donc taux maximal
# 150 / 1052 = 14,3 pour cent (preenregistrement, section 3).
TAUX_SOURCE = {s: TAUX for s in SOURCES}
TAUX_SOURCE["C2"] = [0.0, 0.05, 0.10]
TAUX_SOURCE["C3"] = [0.0, 0.05, 0.10]

ETIQUETTE = {
    "agents v8": "v8, etiquette",
    "agents demographiques (v6)": "v6, demographies",
    "agents composite": "composite, riche",
    "C2": "C2, etiquette",
    "C3": "C3, sans etiquette",
    "PMM k=10": "PMM k=10",
    "E2 regression contexte tirage": "E2 regression tirage",
    "IM m=10 mode des m": "IM m=10",
    "B0 segment": "B0 segment, adversaire nul",
    "humains": "humains, controle negatif",
}


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger(cache, cache_foret, cache_a35):
    """Le paquet de a44, augmente des matrices d'imputation de a35 dont a44 ne prend que
    PMM. Rien n'est recalcule : les trois caches sont ceux deja ecrits par a25, a28 et a35.
    """
    paquet = C44.charger(cache, cache_foret, cache_a35)
    import pickle
    absentes = []
    if cache_a35 and os.path.exists(cache_a35):
        neuf = pickle.load(open(cache_a35, "rb"))
        for cle in ("E2 regression contexte tirage", "IM m=10 mode des m"):
            if cle in neuf:
                paquet["M"][cle] = np.asarray(neuf[cle], dtype=object)
            else:
                absentes.append(cle)
    else:
        absentes += ["E2 regression contexte tirage", "IM m=10 mode des m"]
    paquet["absentes"] = list(paquet.get("absentes", [])) + absentes
    return paquet


def contexte(paquet):
    """Tout ce dont les statistiques ont besoin, calcule une fois."""
    items, options = paquet["items"], paquet["options"]
    alpha = C44.alphabet(items, options)
    k_items = np.array([len(options[it]) for it in items], dtype=np.int32)
    seg_tous, niveaux = C44.segmentations(paquet)
    seg = seg_tous["S_ideo"].astype(np.int32)
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    blocs = np.array([_bloc_ideologie(_norm(v))
                      for v in paquet["x"][:, col["political_ideology"]]])
    sous_ens = C44.sous_ensembles_items(len(items))
    return {"items": items, "options": options, "alpha": alpha, "k_items": k_items,
            "seg": seg, "niveaux": niveaux["S_ideo"], "blocs": blocs,
            "colonnes": np.arange(len(items)),
            "sous_ens": sous_ens,
            "sous_ens5": [s[:5] for s in sous_ens],
            "lignes150": np.asarray(paquet["lignes150"])}


# ---------------------------------------------------------------------------
# 2. Le flux melange
# ---------------------------------------------------------------------------

def masquer_commun(codes_source, codes_humain):
    """Masque du flux : la cellule est renseignee si les deux le sont.

    Renvoie la matrice de la source restreinte au masque commun, et la part de cellules
    perdues par rapport au masque humain seul, qui est un controle bloquant.
    """
    out = codes_source.copy()
    perdu = (codes_humain >= 0) & (codes_source < 0)
    out[codes_humain < 0] = -1
    n_obs = int((codes_humain >= 0).sum())
    return out, (int(perdu.sum()) / n_obs if n_obs else np.nan)


def flux(codes_humain, codes_source_masquee, lignes_possibles, tau, rng):
    """Un flux melange, effectif constant, remplacement en place.

    lignes_possibles : indices des personnes pour lesquelles la source existe. Pour C2 et
    C3 ce sont les 150 du run local ; pour les autres, les 1 052.
    """
    n = codes_humain.shape[0]
    k = int(round(tau * n))
    out = codes_humain.copy()
    if k <= 0:
        return out, np.zeros(0, dtype=np.int64)
    if k > len(lignes_possibles):
        raise ValueError(f"taux {tau} hors de portee : {k} lignes demandees pour "
                         f"{len(lignes_possibles)} disponibles")
    choisies = rng.choice(lignes_possibles, size=k, replace=False)
    out[choisies] = codes_source_masquee[choisies]
    return out, choisies


# ---------------------------------------------------------------------------
# 3. Les trois statistiques
# ---------------------------------------------------------------------------

def concentration(codes, seg, sous_ens):
    """Statistique C : part des personnes d'un segment qui donnent le patron modal.

    Pour chaque sous ensemble d'items et chaque segment, parmi les personnes du segment
    dont les reponses du sous ensemble sont toutes renseignees, la part de celles qui
    donnent le patron le plus frequent du segment. Moyenne sur les segments ponderee par
    l'effectif complet, puis moyenne sur les sous ensembles.
    """
    valeurs = []
    niveaux = [g for g in np.unique(seg) if g >= 0]
    for cols in sous_ens:
        sub = codes[:, cols]
        complet = (sub >= 0).all(axis=1)
        num, den = 0.0, 0.0
        for g in niveaux:
            lignes = np.flatnonzero(complet & (seg == g))
            if len(lignes) < 2:
                continue
            _, comptes = np.unique(sub[lignes], axis=0, return_counts=True)
            num += float(comptes.max())
            den += float(len(lignes))
        if den > 0:
            valeurs.append(num / den)
    return float(np.mean(valeurs)) if valeurs else np.nan


def statistiques_brutes(codes, ctx):
    """Les trois quantites brutes d'un flux, avant retrait du nul."""
    patrons, n_lignes = C44.patrons_distincts(codes, ctx["sous_ens"])
    q5, n_paires = C44.correlation_items(codes, ctx["colonnes"], seg=ctx["seg"])
    q4, _ = C44.correlation_items(codes, ctx["colonnes"], seg=None)
    return {"patrons": patrons, "n_lignes_patrons": n_lignes,
            "q5": q5, "q4": q4, "n_paires": n_paires,
            "conc": concentration(codes, ctx["seg"], ctx["sous_ens"]),
            "conc5": concentration(codes, ctx["seg"], ctx["sous_ens5"])}


def statistiques(codes, ctx, rng, n_nul=N_NUL):
    """Les trois statistiques du preenregistrement, flux contre son propre nul.

    Le nul est le generateur conditionnellement independant de Yuan transpose au
    categoriel, parametre sur LE FLUX lui meme, masque conserve (a44_commun.tirer_nul).
    """
    obs = statistiques_brutes(codes, ctx)
    cum, replis, total = C44.lois_par_segment(codes, ctx["seg"], ctx["k_items"])
    p_nul, q5_nul, c_nul, c5_nul = [], [], [], []
    for _ in range(n_nul):
        z = C44.tirer_nul(codes, ctx["seg"], cum, rng)
        pn, _ = C44.patrons_distincts(z, ctx["sous_ens"])
        qn, _ = C44.correlation_items(z, ctx["colonnes"], seg=ctx["seg"])
        p_nul.append(pn)
        q5_nul.append(qn)
        c_nul.append(concentration(z, ctx["seg"], ctx["sous_ens"]))
        c5_nul.append(concentration(z, ctx["seg"], ctx["sous_ens5"]))
    p_nul = np.asarray(p_nul, dtype=float)
    q5_nul = np.asarray(q5_nul, dtype=float)
    c_nul = np.asarray(c_nul, dtype=float)
    c5_nul = np.asarray(c5_nul, dtype=float)
    return {
        "A": obs["patrons"] / p_nul.mean() - 1.0,
        "B": obs["q5"] - q5_nul.mean(),
        "C": obs["conc"],
        "C_exces": obs["conc"] - c_nul.mean(),
        "C5": obs["conc5"],
        "C5_exces": obs["conc5"] - c5_nul.mean(),
        "patrons": obs["patrons"], "patrons_nul": float(p_nul.mean()),
        "patrons_nul_et": float(p_nul.std(ddof=1)) if n_nul > 1 else np.nan,
        "q5": obs["q5"], "q5_nul": float(q5_nul.mean()),
        "q5_nul_et": float(q5_nul.std(ddof=1)) if n_nul > 1 else np.nan,
        "q4": obs["q4"],
        "conc_nul": float(c_nul.mean()),
        "conc_nul_et": float(c_nul.std(ddof=1)) if n_nul > 1 else np.nan,
        "n_lignes_patrons": obs["n_lignes_patrons"], "n_paires": obs["n_paires"],
        "replis_segment": replis / max(total, 1),
    }


CLES_STAT = ["A", "B", "C", "C_exces", "C5", "C5_exces"]
LIBELLE_STAT = {
    "A": "deficit de patrons distincts, relatif au nul du flux",
    "B": "exces de correlation inter items residualisee",
    "C": "concentration par segment, patron modal, brute",
    "C_exces": "concentration par segment, exces sur le nul",
    "C5": "concentration par segment, cinq items, brute",
    "C5_exces": "concentration par segment, cinq items, exces sur le nul",
}
# Les trois quantites primaires du preenregistrement section 4.
PRIMAIRES = ["A", "B", "C"]


# ---------------------------------------------------------------------------
# 4. La polarisation d'I4
# ---------------------------------------------------------------------------

def polarisation(codes, blocs, signes=None, n_min=30):
    """Ecart gauche droite signe, moyenne sur les items des ecarts standardises de rang.

    g_j = (moyenne des rangs a gauche - moyenne des rangs a droite) / ecart type des rangs.
    P = moyenne_j signe_j * g_j, ou signe_j vient des humains purs. Si signes est None,
    les signes sont ceux du flux lui meme et la fonction renvoie aussi le vecteur, ce qui
    sert a fixer la reference une fois pour toutes.
    """
    r = C44.rangs_colonne(codes)
    gauche = blocs == "gauche"
    droite = blocs == "droite"
    m = r.shape[1]
    g = np.full(m, np.nan)
    for j in range(m):
        col = r[:, j]
        ok = ~np.isnan(col)
        a, b = col[ok & gauche], col[ok & droite]
        if len(a) < n_min or len(b) < n_min:
            continue
        s = np.nanstd(col[ok], ddof=1)
        if not np.isfinite(s) or s <= 0:
            continue
        g[j] = (a.mean() - b.mean()) / s
    bon = np.isfinite(g)
    if signes is None:
        sg = np.where(bon, np.sign(g), 0.0)
        return float(np.nanmean(np.abs(g[bon]))) if bon.any() else np.nan, sg, bon
    # Les items retenus sont ceux que les HUMAINS purs retiennent, sinon la moyenne
    # porterait sur un ensemble d'items qui varie avec le taux de melange.
    garder = bon & (signes != 0.0)
    val = signes[garder] * g[garder]
    return (float(val.mean()) if garder.any() else np.nan), signes, garder


# ---------------------------------------------------------------------------
# 5. Reechantillonnage de la reference humaine
# ---------------------------------------------------------------------------

def ic_percentile(tirages, centre=None, echelle=1.0):
    """IC a 95 pour cent par percentiles, avec mise a l'echelle facultative.

    echelle = racine(m / N) pour un sous echantillonnage a m personnes. Le pivot est la
    MOYENNE des tirages et non la valeur de reference : la loi du sous echantillon est
    decalee par rapport a la valeur pleine, parce que le nombre de patrons distincts et la
    concentration dependent de l'effectif. Prendre la valeur de reference comme pivot
    produirait un intervalle qui ne contient pas cette valeur, ce qui est le defaut que ce
    correctif supprime.
    """
    t = np.asarray([x for x in tirages if np.isfinite(x)], dtype=float)
    if not len(t):
        return np.nan, np.nan, np.nan
    bas, haut = np.percentile(t, 2.5), np.percentile(t, 97.5)
    moy = float(t.mean())
    et = float(t.std(ddof=1))
    if centre is None:
        centre = moy
    bas = centre - (moy - bas) * echelle
    haut = centre + (haut - moy) * echelle
    et = et * echelle
    return float(bas), float(haut), et


def holm(p):
    return C44.holm(p)


def benjamini_hochberg(p):
    return C44.benjamini_hochberg(p)


def ecrire(lignes, nom):
    chemin = os.path.join(SORTIE, nom)
    df = lignes if isinstance(lignes, pd.DataFrame) else pd.DataFrame(lignes)
    df.to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(df)} lignes", flush=True)
    return chemin


def p_bilateral_normale(z):
    """p bilateral d'un z, sans scipy."""
    from math import erfc, sqrt
    return float(erfc(abs(z) / sqrt(2.0)))


def ajuster_courbe(taux, ecarts):
    """Ajustement de degre 2 sans terme constant de l'ecart a la reference sur le taux.

    Renvoie (a, b, R2) pour ecart(tau) = a * tau + b * tau^2, moindres carres ordinaires.
    """
    t = np.asarray(taux, dtype=float)
    y = np.asarray(ecarts, dtype=float)
    bon = np.isfinite(t) & np.isfinite(y)
    t, y = t[bon], y[bon]
    if len(t) < 2:
        return np.nan, np.nan, np.nan
    X = np.column_stack([t, t ** 2])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    sse = float(((y - pred) ** 2).sum())
    sst = float((y ** 2).sum())
    r2 = 1.0 - sse / sst if sst > 0 else np.nan
    return float(coef[0]), float(coef[1]), r2


def racine_courbe(a, b, cible):
    """Plus petite racine positive de |a t + b t^2| = cible, bornee a 1.

    Renvoie NaN si la courbe n'atteint jamais la cible sur [0 ; 1].
    """
    if not np.isfinite(a) or not np.isfinite(b) or not np.isfinite(cible) or cible <= 0:
        return np.nan
    grille = np.linspace(0.0, 1.0, 20001)
    val = np.abs(a * grille + b * grille ** 2)
    ok = np.flatnonzero(val >= cible)
    if not len(ok):
        return np.nan
    return float(grille[ok[0]])


def inverser_courbe(a, b, ecart):
    """tau tel que a t + b t^2 = ecart, plus proche point de la grille sur [0 ; 1]."""
    if not np.isfinite(a) or not np.isfinite(b) or not np.isfinite(ecart):
        return np.nan
    grille = np.linspace(0.0, 1.0, 20001)
    val = a * grille + b * grille ** 2
    return float(grille[int(np.argmin(np.abs(val - ecart)))])
