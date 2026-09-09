"""
i1_commun : briques partagees par le jour 1 de l'idee I1, le cote humain.

Qui change d'avis dans les panels GSS entre deux vagues, et est ce previsible ?

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a12_retest_delai
(les 149 items, l'appariement des noms GSS, le chargement des panels, la definition de
consistance de Stanford), a2_commun (est_manquant, bootstrap_personnes, distance de
Hamming), a44_commun (permutation intra segment, Holm, Benjamini-Hochberg),
a30_commun (les deux axes economique et social).

LE PREENREGISTREMENT EST resultats/i1-preenregistrement.md, ECRIT AVANT CE FICHIER,
le 8 septembre 2026 a 18 h 30 CEST.

Ce module porte six choses et rien d'autre.

  1. Le noyau commun des 118 items de a12, recalcule par appel des fonctions de a12.
  2. Le codage entier des reponses du panel, un alphabet par item, partage par les
     quatre panels et les trois vagues.
  3. Les perimetres de paires de vagues declares : quatre paires a quatre ans sur des
     personnes disjointes, quatre paires a deux ans disjointes, trois panels a trois
     vagues.
  4. La regle de direction en laisse un dehors, qui classe un changement en monotone,
     contraire ou indetermine sans jamais utiliser la personne classee pour estimer la
     derive de son item.
  5. Le segment ideologie x age x education et les demographies de vague 1.
  6. Les deux axes de a30 sur les codes du panel, et le quadrant de cross pression.

Aucune microdonnee n'est ecrite par ce module ni par aucun script i1_*.
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a12_retest_delai as A12
from a2_commun import est_manquant, bootstrap_personnes  # noqa: F401
import a44_commun as C44
import a30_commun as C30

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL = os.path.join(RACINE, "data", "gss-panel")
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908
N_PERMUTATIONS = 200
N_BOOTSTRAP = 1000
N_PLIS = 5
K_VOISINS = 25
SEUIL_RARE = 0.10
MIN_ITEMS_INDIVIDU = A12.MIN_ITEMS_INDIVIDU   # 20, seuil de a12
MIN_PERSONNES_ITEM = 100                      # MIN_PAIRES_ITEM de a12
MIN_CHANGEURS_ITEM = 30
MIN_SEGMENT = 10

# --- les perimetres declares au preenregistrement, section 2 -----------------
# Les quatre echantillons de depart sont des tirages distincts du GSS : d'un panel a
# l'autre les personnes sont disjointes. A l'interieur d'un panel, en revanche, les deux
# paires a deux ans partagent les memes personnes ; le perimetre secondaire n'en retient
# donc qu'une seule par panel.
PAIRES_4ANS = [("2006-2010", 2006, 2010), ("2008-2012", 2008, 2012),
               ("2010-2014", 2010, 2014), ("2016-2020", 2016, 2020)]
PAIRES_2ANS = [("2006-2010", 2006, 2008), ("2008-2012", 2008, 2010),
               ("2010-2014", 2010, 2012), ("2016-2020", 2018, 2020)]
TROIS_VAGUES = [("2006-2010", 2006, 2008, 2010), ("2008-2012", 2008, 2010, 2012),
                ("2010-2014", 2010, 2012, 2014)]

# Colonnes demographiques, sans suffixe de vague. Elles sont lues a la vague de depart
# de la paire, jamais a la vague d'arrivee.
DEMOS = ["polviews", "partyid", "age", "sex", "race", "degree", "educ", "attend", "relig"]


# ---------------------------------------------------------------------------
# 1. Les 118 items du noyau commun, et les matrices de reponse
# ---------------------------------------------------------------------------

def charger_panels():
    """Charge les quatre panels sur les 149 items de a2, puis retient le noyau commun.

    Le noyau commun est defini exactement comme en a12 : les items mesures dans les onze
    paires de vagues a la fois, avec le meme seuil de cent personnes par item et par
    paire. Rien n'est recopie de a12, ses fonctions sont appelees.
    """
    items149 = A12.items_stanford()
    brut = {}
    for nom in A12.PANELS:
        mat, src, plan, n = A12.charger_panel(nom, items149)
        brut[nom] = {"mat": mat, "n": n}
    # comptage des paires ou l'item passe le seuil, avec la fonction de a12
    compte = {it: 0 for it in items149}
    n_paires = 0
    for nom in A12.PANELS:
        for a, b, _ in A12.PANELS[nom]["paires"]:
            n_paires += 1
            _, par_item, _, _ = A12.consistance(brut[nom]["mat"][a], brut[nom]["mat"][b])
            for j, it in enumerate(items149):
                if np.isfinite(par_item[j]):
                    compte[it] += 1
    noyau = [it for it in items149 if compte[it] == n_paires]
    idx = [items149.index(it) for it in noyau]
    for nom in brut:
        brut[nom]["mat"] = {a: m[:, idx] for a, m in brut[nom]["mat"].items()}
    return noyau, brut, n_paires


def alphabet_panel(brut, n_items):
    """Un alphabet d'entiers par item, partage par les quatre panels et les trois vagues.

    Les codes du GSS sont des nombres ; l'alphabet ne fait que les ranger dans un ordre
    stable pour rendre le calcul vectorisable. Aucune ordinalite n'est supposee : la
    regle de direction du preenregistrement travaille sur les parts de modalites.
    """
    tables = [dict() for _ in range(n_items)]
    for nom in sorted(brut):
        for a in sorted(brut[nom]["mat"]):
            m = brut[nom]["mat"][a]
            for j in range(n_items):
                t = tables[j]
                for v in m[:, j]:
                    if est_manquant(v):
                        continue
                    k = _cle(v)
                    if k not in t:
                        t[k] = len(t)
    return tables


def _cle(v):
    """Cle de modalite stable : un entier si la valeur en est un, sinon la chaine."""
    if isinstance(v, float) and float(v).is_integer():
        return int(v)
    return v


def coder(m, tables):
    """Matrice objet -> matrice d'entiers, -1 pour un manquant."""
    n, p = m.shape
    out = np.full((n, p), -1, dtype=np.int16)
    for j in range(p):
        t = tables[j]
        col = m[:, j]
        for i in range(n):
            v = col[i]
            if not est_manquant(v):
                out[i, j] = t[_cle(v)]
    return out


# ---------------------------------------------------------------------------
# 2. Demographies
# ---------------------------------------------------------------------------

def charger_demos(nom, annee):
    """Demographies brutes d'un panel a une vague donnee, codes numeriques du GSS."""
    cfg = A12.PANELS[nom]
    suf = cfg["vagues"][annee]
    _, meta = pyreadstat.read_dta(os.path.join(PANEL, cfg["fichier"]),
                                  metadataonly=True, encoding="latin1")
    colonnes = {c.lower(): c for c in meta.column_names}
    voulu = {d: colonnes.get(d + suf) for d in DEMOS}
    presentes = [v for v in voulu.values() if v]
    df, _ = pyreadstat.read_dta(os.path.join(PANEL, cfg["fichier"]),
                                usecols=presentes, encoding="latin1")
    df.columns = [c.lower() for c in df.columns]
    out = {}
    for d in DEMOS:
        c = (d + suf)
        out[d] = df[c].values.astype(float) if c in df.columns else np.full(len(df), np.nan)
    return out


def bloc_ideologie(v):
    """polviews 1 a 7 -> trois blocs. Regle mecanique de a1 et de a44, sans jugement."""
    if not np.isfinite(v):
        return "non renseigne"
    if v <= 3:
        return "gauche"
    if v == 4:
        return "centre"
    if v <= 7:
        return "droite"
    return "non renseigne"


def bloc_age(v):
    if not np.isfinite(v) or v < 18 or v > 100:
        return "non renseigne"
    if v < 35:
        return "18-34"
    if v < 55:
        return "35-54"
    return "55+"


def bloc_education(v):
    """degree 0 a 4 -> trois blocs. 0 et 1 bas, 2 et 3 moyen, 4 haut."""
    if not np.isfinite(v):
        return "non renseigne"
    if v <= 1:
        return "bas"
    if v <= 3:
        return "moyen"
    if v == 4:
        return "haut"
    return "non renseigne"


def segment(demos):
    """Segment ideologie x age x education, 27 cellules au plus plus les non renseignes."""
    return np.array([f"{bloc_ideologie(i)}|{bloc_age(a)}|{bloc_education(e)}"
                     for i, a, e in zip(demos["polviews"], demos["age"], demos["degree"])],
                    dtype=object)


# ---------------------------------------------------------------------------
# 3. La regle de direction, en laisse un dehors
# ---------------------------------------------------------------------------

def classer_changement(c_a, c_b, k_par_item):
    """Classe chaque cellule en stable, monotone, contraire ou indetermine.

    Regle du preenregistrement section 3, appliquee paire par paire.

    Pour l'item j, D_j(m) = c2(m) - c1(m) est la variation d'effectif de la modalite m
    sur les personnes evaluables. Pour la personne i qui passe de a a b, la derive
    RECALCULEE SANS ELLE a pour numerateur D_j(a) + 1 sur la modalite quittee et
    D_j(b) - 1 sur la modalite prise. Le changement est monotone si la modalite prise
    gagne du terrain sans elle et la modalite quittee en perd sans elle.

    Retourne un tableau d'entiers de meme forme :
      -1 cellule non evaluable, 0 stable, 1 monotone, 2 contraire, 3 indetermine.
    """
    n, p = c_a.shape
    out = np.full((n, p), -1, dtype=np.int8)
    for j in range(p):
        a, b = c_a[:, j], c_b[:, j]
        ok = (a >= 0) & (b >= 0)
        if not ok.any():
            continue
        k = k_par_item[j]
        c1 = np.bincount(a[ok], minlength=k).astype(np.int64)
        c2 = np.bincount(b[ok], minlength=k).astype(np.int64)
        d = c2 - c1
        col = np.full(n, -1, dtype=np.int8)
        col[ok] = 0
        chg = ok & (a != b)
        if chg.any():
            aa, bb = a[chg], b[chg]
            gagne = (d[bb] - 1) > 0
            perd = (d[aa] + 1) < 0
            v = np.full(chg.sum(), 3, dtype=np.int8)
            v[gagne & perd] = 1
            v[(~gagne) & (~perd) & ((d[bb] - 1) < 0) & ((d[aa] + 1) > 0)] = 2
            col[chg] = v
        out[:, j] = col
    return out


def derive_item(c_a, c_b, k_par_item):
    """Par item : taux de changement brut, derive nette TV, n personnes evaluees."""
    n, p = c_a.shape
    taux, tv, neval = np.full(p, np.nan), np.full(p, np.nan), np.zeros(p, dtype=int)
    for j in range(p):
        a, b = c_a[:, j], c_b[:, j]
        ok = (a >= 0) & (b >= 0)
        m = int(ok.sum())
        neval[j] = m
        if m == 0:
            continue
        k = k_par_item[j]
        p1 = np.bincount(a[ok], minlength=k) / m
        p2 = np.bincount(b[ok], minlength=k) / m
        taux[j] = float((a[ok] != b[ok]).mean())
        tv[j] = float(0.5 * np.abs(p2 - p1).sum())
    return taux, tv, neval


# ---------------------------------------------------------------------------
# 4. Assemblage d'un perimetre : la table personne x item
# ---------------------------------------------------------------------------

def assembler(paires, noyau, brut, tables, min_items=MIN_ITEMS_INDIVIDU):
    """Construit le perimetre : codes de vague de depart, classes de changement, segment.

    Une personne entre si elle a au moins min_items cellules evaluables dans sa paire,
    seuil MIN_ITEMS_INDIVIDU de a12. Rien n'est ecrit sur disque.
    """
    k_par_item = [max(len(t), 1) for t in tables]
    blocs = []
    for nom, a, b in paires:
        ma, mb = brut[nom]["mat"][a], brut[nom]["mat"][b]
        ca, cb = coder(ma, tables), coder(mb, tables)
        ok = (ca >= 0) & (cb >= 0)
        garde = ok.sum(axis=1) >= min_items
        ca, cb, ok = ca[garde], cb[garde], ok[garde]
        cls = classer_changement(ca, cb, k_par_item)
        dem = {d: v[garde] for d, v in charger_demos(nom, a).items()}
        blocs.append({"panel": nom, "depart": a, "arrivee": b, "c_a": ca, "c_b": cb,
                      "ok": ok, "classe": cls, "demos": dem,
                      "segment": segment(dem), "n": int(garde.sum())})
    paquet = {
        "items": noyau, "k_par_item": k_par_item, "blocs": blocs,
        "c_a": np.vstack([x["c_a"] for x in blocs]),
        "c_b": np.vstack([x["c_b"] for x in blocs]),
        "ok": np.vstack([x["ok"] for x in blocs]),
        "classe": np.vstack([x["classe"] for x in blocs]),
        "panel": np.concatenate([np.full(x["n"], x["panel"], dtype=object) for x in blocs]),
        "segment": np.concatenate([x["segment"] for x in blocs]),
        "demos": {d: np.concatenate([x["demos"][d] for x in blocs]) for d in DEMOS},
    }
    paquet["n"] = paquet["c_a"].shape[0]
    return paquet


def y_changement(paquet):
    """Cible primaire Y_chg et cible secondaire Y_mono, -1 hors perimetre evaluable."""
    cl = paquet["classe"]
    y_chg = np.where(cl < 0, -1, (cl > 0).astype(np.int8)).astype(np.int8)
    y_mono = np.where(cl < 0, -1, (cl == 1).astype(np.int8)).astype(np.int8)
    return y_chg, y_mono


# ---------------------------------------------------------------------------
# 5. Les deux axes de a30 sur les codes du panel
# ---------------------------------------------------------------------------

def scores_axes(paquet):
    """Score economique et score social par personne, methode de a30_structure.

    Premiere composante principale de chaque bloc d'items, estimee sur le perimetre
    entier et non segment par segment, manquants remplaces par la moyenne d'item, signe
    fixe par correlation positive avec polviews. Les listes d'items sont celles de
    a30_commun, restreintes a ce que le noyau commun contient.
    """
    ordre = {it: j for j, it in enumerate(paquet["items"])}
    out = {}
    ideo = paquet["demos"]["polviews"]
    for nom, liste in (("economique", C30.AXE_ECONOMIQUE), ("social", C30.AXE_SOCIAL)):
        cols = [ordre[i] for i in liste if i in ordre]
        if len(cols) < 3:
            out[nom] = np.full(paquet["n"], np.nan)
            out[nom + "_n_items"] = len(cols)
            continue
        X = paquet["c_a"][:, cols].astype(float)
        X[X < 0] = np.nan
        mu = np.nanmean(X, axis=0)
        mu = np.where(np.isfinite(mu), mu, 0.0)
        idx = np.where(np.isnan(X))
        X[idx] = np.take(mu, idx[1])
        X = X - X.mean(axis=0)
        sd = X.std(axis=0)
        X = X[:, sd > 1e-9] / sd[sd > 1e-9]
        u, s, vt = np.linalg.svd(X, full_matrices=False)
        score = u[:, 0] * s[0]
        bon = np.isfinite(ideo)
        r = np.corrcoef(score[bon], ideo[bon])[0, 1] if bon.sum() > 2 else 1.0
        score = score * (1.0 if r > 0 else -1.0)
        out[nom] = (score - score.mean()) / (score.std() + 1e-12)
        out[nom + "_n_items"] = len(cols)
    return out


def quadrant(z_eco, z_soc):
    """Hors quadrant si les deux signes different, congruent sinon. NaN si l'un manque."""
    q = np.full(len(z_eco), None, dtype=object)
    bon = np.isfinite(z_eco) & np.isfinite(z_soc)
    q[bon] = np.where(np.sign(z_eco[bon]) == np.sign(z_soc[bon]), "congruent",
                      "hors quadrant")
    return q


# ---------------------------------------------------------------------------
# 6. Profils individuels de vague de depart
# ---------------------------------------------------------------------------

def profils(paquet):
    """Les resumes du profil de vague de depart, section 5 du preenregistrement."""
    ca, ok = paquet["c_a"], (paquet["c_a"] >= 0)
    n, p = ca.shape
    # modalites rares au seuil de 10 pour cent, sur le perimetre entier
    rare = np.zeros((n, p), dtype=bool)
    majo = np.zeros((n, p), dtype=bool)
    for j in range(p):
        col = ca[:, j]
        m = col >= 0
        if not m.any():
            continue
        cnt = np.bincount(col[m], minlength=paquet["k_par_item"][j]).astype(float)
        part = cnt / cnt.sum()
        petites = np.flatnonzero(part < SEUIL_RARE)
        grande = int(np.argmax(cnt))
        rare[m, j] = np.isin(col[m], petites)
        majo[m, j] = col[m] == grande
    n_ok = np.maximum(ok.sum(axis=1), 1)
    # distance de Hamming au patron modal du segment de la personne
    seg = paquet["segment"]
    modal = np.full((n, p), -1, dtype=np.int16)
    for s in np.unique(seg):
        lignes = np.flatnonzero(seg == s)
        for j in range(p):
            col = ca[lignes, j]
            m = col >= 0
            if m.sum() == 0:
                continue
            cnt = np.bincount(col[m], minlength=paquet["k_par_item"][j])
            modal[lignes, j] = int(np.argmax(cnt))
    distance = ((ca != modal) & ok).sum(axis=1) / n_ok
    ax = scores_axes(paquet)
    return {
        "part_rare": rare.sum(axis=1) / n_ok,
        "part_majoritaire": majo.sum(axis=1) / n_ok,
        "distance_patron_segment": distance,
        "part_manquants": 1.0 - ok.sum(axis=1) / p,
        "z_eco": ax["economique"], "z_soc": ax["social"],
        "cross_pression": np.abs(ax["economique"] - ax["social"]),
        "quadrant": quadrant(ax["economique"], ax["social"]),
        "n_items_axe_eco": ax["economique_n_items"],
        "n_items_axe_soc": ax["social_n_items"],
        "rare": rare, "majoritaire": majo,
    }


# ---------------------------------------------------------------------------
# 7. Outils
# ---------------------------------------------------------------------------

def codes_segment(seg):
    """Segment textuel -> entier, pour permuter_intra de a44."""
    niveaux = sorted(set(seg))
    idx = {s: k for k, s in enumerate(niveaux)}
    return np.array([idx[s] for s in seg], dtype=np.int32), niveaux


def auc(y, score):
    """Aire sous la courbe ROC, par les rangs de Mann Whitney. NaN si une classe manque.

    Les ex aequo recoivent le rang moyen, ce qui donne 0,5 exactement a un score
    constant : c'est ce qui rend le temoin T0 lisible.
    """
    from scipy.stats import rankdata
    y = np.asarray(y)
    s = np.asarray(score, dtype=float)
    bon = np.isfinite(s)
    y, s = y[bon], s[bon]
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return np.nan
    rangs = rankdata(s)
    return float((rangs[y == 1].sum() - n1 * (n1 + 1) / 2.0) / (n1 * n0))


def rappel_a_taux_de_base(y, score):
    """Rappel des changeurs quand on signale exactement autant de personnes qu'il y en a."""
    y = np.asarray(y)
    s = np.asarray(score, dtype=float)
    bon = np.isfinite(s)
    y, s = y[bon], s[bon]
    n1 = int(y.sum())
    if n1 == 0 or n1 == len(y):
        return np.nan
    seuil = np.argsort(-s, kind="mergesort")[:n1]
    return float(y[seuil].sum() / n1)


def permuter_intra(seg_codes, rng):
    """Permutation des personnes a l'interieur du segment, fonction de a44 reutilisee."""
    return C44.permuter_intra(len(seg_codes), seg_codes, rng)


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
