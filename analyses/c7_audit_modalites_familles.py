"""
c7_audit_modalites_familles : « famille d'items » et « nombre de modalites » sont-elles
la meme partition, et si non, laquelle porte l'effet ?

===========================================================================
PREENREGISTREMENT : resultats/audit-modalites-familles-2026-09-13.md, section 0, ecrite
et COMMITEE SEULE avant ce fichier et avant tout calcul de reidentification.

LE RECOUPEMENT. Deux rapports de la nuit du 12 au 13 septembre 2026, produits par deux
agents qui ne se sont pas parles :
  A  resultats/audit-items-banals-2026-09-13.md        le facteur est le NOMBRE DE
     MODALITES (99,8 % du gain restitue) ; 41 items binaires sur 60 ; pic a k = 40
  B  resultats/audit-contamination-persona-2026-09-13.md   tout l'effet vit dans les
     40 ITEMS D'ACHAT (33,2 %) et pas dans les 20 items d'heuristiques (0,24 %) ; le
     rapport conclut que « le mecanisme de cette concentration reste inexplique »
B publie lui-meme 2,0 modalites par item d'achat contre 5,6 par item d'heuristiques. Les
deux partitions sont peut-etre la MEME. Ce script le tranche.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucune donnee
individuelle n'est calculee, imprimee ou ecrite : taux agreges seuls, jamais un pid, une
reponse, ni un appariement.

CE QUI EST REPRIS TEL QUEL, sans une ligne reimplementee :
  c7_audit_items_banals.preparer      le bassin de 2 058 et les trois matrices
  c7_audit_items_banals.moities       le decoupage hors pli de graine fixe
  c7_audit_items_banals.n_modalites   le nombre de modalites observees par item
  c7_reidentification.rangs_attaque   l'attaque elle meme
  a2_commun.bootstrap_personnes       l'IC par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation
La regle de famille est celle de B, reprise telle quelle : un item est « achat » si et
seulement si son nom de colonne finit par _Q295.

LES DEUX PIEGES QUE CE PROJET A DEJA MANQUES TROIS FOIS, et comment ils sont fermes ici :
  - bassin : un seul, 2 058 personnes, identique dans TOUTE la partie quantitative ;
  - nombre d'items : toute comparaison de la section 3 se fait a 20 items de part et
    d'autre. Les 40 items d'achat sont ramenes a 20 par tirage, jamais compares bruts
    aux 20 items d'heuristiques.

Aucun appel de modele de langage, aucun reseau, aucune depense, aucun arriere-plan.
Lecture seule sur data/. Aucun script existant n'est modifie.

Usage : .venv/bin/python analyses/c7_audit_modalites_familles.py
===========================================================================
"""

import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import bootstrap_personnes                                # noqa: E402
from c7_reidentification import (                                        # noqa: E402
    DEMO, N_BOOTSTRAP, REF_V4, REF_V13, graine_nom, rangs_attaque,
)
from c7_audit_items_banals import moities, n_modalites, preparer         # noqa: E402
from c7_controle_interpretabilite import (                               # noqa: E402
    EchecControleInterpretabilite, controle_avant_interpretation,
)

GRAINE = 20260913
N_TIRAGES_LIENS = 5            # reduction declaree, identique aux deux branches recoupees
K_APPARIE = 20                 # nombre d'items apparie entre TOUTES les conditions de V3/V4
N_TIRAGES_ACHAT = 10           # sous-ensembles de 20 items d'achat tires au hasard
N_APPARIEMENTS = 5             # appariements deux a deux des 40 items d'achat (V4b)

SORTIE_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "resultats", "c7-audit-modalites-familles.csv")
CATALOGUE = os.path.join(T1.RACINE_TWIN, "question_catalog_and_human_response_csv",
                         "question_catalog.json")
# Les colonnes de t1_commun portent les en-tetes du CSV de reponses humaines
# (« False Cons. self _1 », « 38_Q295 »), pas les identifiants du catalogue (« QID287_1 »).
# Le pont entre les deux est le fichier de correspondance publie avec le jeu, repris tel
# quel de c7_audit_contamination -- sans lui, position et longueur de libelle sortiraient
# vides, et le volet V5 passerait sur des NaN au lieu d'etre mesure.
MAPPING_V4 = os.path.join(T1.RACINE_TWIN, "llm",
                          "wave4_formatted_to_catalog_mapping.json")
SOURCE_V4 = "wave4_Q_wave1_3_A"

# La regle de famille de l'audit B, reprise mot pour mot depuis c7_audit_contamination.
SUFFIXE_ACHAT = "_Q295"


# ---------------------------------------------------------------------------
# 1. Mesurer : candidat et baseline sur EXACTEMENT les memes colonnes et le meme pool
# ---------------------------------------------------------------------------

def mesurer(Xc, Xd, pool, etiquette):
    """top-1 du candidat et de la baseline demographique sur les matrices donnees.

    Les trois matrices sont deja restreintes aux memes colonnes (ou deja recodees) : la
    fonction ne choisit rien. La baseline n'est jamais importee d'ailleurs, elle est
    recalculee ici, sur ces memes colonnes et ce meme pool -- c'est la seule facon
    d'empecher la comparaison a la baseline d'un autre bassin.
    """
    n = Xc.shape[0]
    vrai = np.arange(n)
    out = {"n_bassin": n, "k_items": Xc.shape[1], "hasard": 1.0 / n}
    for role, X in (("cand", Xc), ("base", Xd)):
        rng = np.random.default_rng([GRAINE, graine_nom(role + "|" + etiquette)])
        _, top1, _ = rangs_attaque(X, pool, vrai, rng, n_tirages=N_TIRAGES_LIENS)
        m, b, h = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                      graine=[GRAINE, graine_nom(role + etiquette), 1])
        out[role + "_top1"] = m
        out[role + "_top1_bas"] = b
        out[role + "_top1_haut"] = h
    out["ratio_cand_base"] = (out["cand_top1"] / out["base_top1"]
                              if out["base_top1"] > 0 else np.nan)
    out["au_dessus_baseline"] = bool(out["cand_top1_bas"] > out["base_top1_haut"])
    return out


def ligne(volet, condition, res, note=""):
    d = {"volet": volet, "condition": condition, "note": note}
    d.update(res)
    print(f"  {volet:4s} {condition:44s} k={res['k_items']:3d} "
          f"cand={res['cand_top1']*100:6.2f} % "
          f"[{res['cand_top1_bas']*100:5.2f};{res['cand_top1_haut']*100:5.2f}] "
          f"base={res['base_top1']*100:5.2f} % "
          f"{'>base' if res['au_dessus_baseline'] else 'SOUS BASELINE'}", flush=True)
    return d


# ---------------------------------------------------------------------------
# 2. Les deux recodages du nombre de modalites (volet V4)
# ---------------------------------------------------------------------------

def recoder_mode(pool_regle, X):
    """Dichotomisation « mode contre non-mode ».

    La modalite modale de chaque item est estimee sur les REPONSES HUMAINES de
    `pool_regle`, puis la meme regle est appliquee a l'identique au jumeau, a la baseline
    et au pool : 1 si la reponse est la modale, 0 sinon. Les manquants (-1) le restent.
    Une regle estimee sur les humains et appliquee aux trois matrices ne peut pas
    avantager l'une d'elles.
    """
    out = np.full(X.shape, -1, dtype=np.int32)
    for j in range(pool_regle.shape[1]):
        col = pool_regle[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            continue
        vals, cnt = np.unique(col, return_counts=True)
        mode = vals[np.argmax(cnt)]
        pres = X[:, j] >= 0
        out[pres, j] = (X[pres, j] == mode).astype(np.int32)
    return out


def recoder_mediane(pool_regle, X, est_ordinal_j):
    """Coupure a la mediane pour les items ordinaux, regle du mode pour les autres.

    La mediane est estimee sur les reponses humaines de `pool_regle`. Un item ordinal dont
    la mediane tombe sur une borne (toutes les reponses du meme cote) retombe sur la regle
    du mode, faute de quoi la colonne serait constante et ne porterait plus rien.
    """
    out = np.full(X.shape, -1, dtype=np.int32)
    for j in range(pool_regle.shape[1]):
        col = pool_regle[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            continue
        pres = X[:, j] >= 0
        if est_ordinal_j[j]:
            med = np.median(col)
            bas = (col <= med).mean()
            if 0.02 < bas < 0.98:
                out[pres, j] = (X[pres, j] > med).astype(np.int32)
                continue
        vals, cnt = np.unique(col, return_counts=True)
        mode = vals[np.argmax(cnt)]
        out[pres, j] = (X[pres, j] == mode).astype(np.int32)
    return out


def composer_paires(X, paires, k_mod):
    """Apparie les colonnes deux a deux en items composites, SANS fabriquer de donnee.

    Le couple de reponses observees (a, b) devient la modalite unique a * k_mod + b. La
    transformation est BIJECTIVE : l'information est exactement conservee, seul le GRAIN
    DE LA METRIQUE change -- un desaccord sur un seul des deux sous-items coute desormais
    autant qu'un desaccord sur les deux. C'est la manipulation du nombre de modalites a
    information constante, symetrique de la dichotomisation.
    """
    out = np.full((X.shape[0], len(paires)), -1, dtype=np.int32)
    for c, (j1, j2) in enumerate(paires):
        pres = (X[:, j1] >= 0) & (X[:, j2] >= 0)
        out[pres, c] = X[pres, j1] * k_mod + X[pres, j2]
    return out


# ---------------------------------------------------------------------------
# 3. Descriptifs par item, pour les confondants du volet V5
# ---------------------------------------------------------------------------

def entropie_items(bloc):
    h = np.zeros(bloc.shape[1])
    for j in range(bloc.shape[1]):
        col = bloc[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            continue
        _, cnt = np.unique(col, return_counts=True)
        p = cnt / cnt.sum()
        h[j] = float(-(p * np.log2(p)).sum())
    return h


def kappa_item(a, b):
    """Kappa de Cohen entre deux vecteurs de codes, manquants exclus. Correction du
    hasard indispensable ici : elle seule rend comparables un item a 2 modalites et un
    item a 7."""
    m = (a >= 0) & (b >= 0)
    if m.sum() < 10:
        return np.nan
    a, b = a[m], b[m]
    po = float((a == b).mean())
    mods = np.union1d(np.unique(a), np.unique(b))
    pe = float(sum((a == v).mean() * (b == v).mean() for v in mods))
    return (po - pe) / (1 - pe) if pe < 1 else np.nan


def gain_normalise_items(X, pool):
    """Par item : (exactitude du generateur - taux modal humain) / (1 - taux modal).

    Mesure par item, donc INSENSIBLE a la non-linearite du top-1 vis-a-vis du nombre
    d'items -- c'est ce qui la rend utilisable pour chercher un confondant a l'interieur
    d'un bloc, la ou le top-1 ne peut rien dire.
    """
    g = np.full(X.shape[1], np.nan)
    for j in range(X.shape[1]):
        m = (X[:, j] >= 0) & (pool[:, j] >= 0)
        if m.sum() < 10:
            continue
        acc = float((X[m, j] == pool[m, j]).mean())
        vals, cnt = np.unique(pool[m, j], return_counts=True)
        modal = float(cnt.max() / cnt.sum())
        g[j] = (acc - modal) / (1 - modal) if modal < 1 else np.nan
    return g


def descripteurs_catalogue(noms):
    """Position au catalogue et longueur du libelle, par colonne attaquee.

    Les deux sont des proprietes du QUESTIONNAIRE PUBLIC, pas des repondants : aucune
    donnee individuelle n'entre ici.
    """
    cat = json.load(open(CATALOGUE))
    mapping = {x["formatted_column"]: x["QuestionID"]
               for x in json.load(open(MAPPING_V4))}
    rang_qid, longueur_qid = {}, {}
    for r, e in enumerate(cat):
        if e["source"] != SOURCE_V4:
            continue
        rang_qid[e["QuestionID"]] = r
        longueur_qid[e["QuestionID"]] = len(" ".join((e.get("QuestionText") or "").split()))
    pos = np.array([rang_qid.get(mapping.get(c, ""), np.nan) for c in noms], dtype=float)
    lon = np.array([longueur_qid.get(mapping.get(c, ""), np.nan) for c in noms],
                   dtype=float)
    manquants = int(np.isnan(pos).sum())
    if manquants:
        raise RuntimeError(
            f"{manquants} des {len(noms)} items attaques n'ont pas ete raccordes au "
            "catalogue : position et longueur de libelle seraient des NaN, et le volet "
            "V5 conclurait « aucun confondant » sur des colonnes vides. Corriger la "
            "correspondance avant d'interpreter quoi que ce soit.")
    return pos, lon


# ---------------------------------------------------------------------------
# 4. Le programme
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes, desc_lignes, resume = [], [], {}

    paq, bassin, items, pool, X_cand, X_demo = preparer()
    noms = [paq["colonnes"][j] for j in items]
    est_achat = np.array([c.endswith(SUFFIXE_ACHAT) for c in noms])
    nmod = n_modalites(pool).astype(int)
    n = len(bassin)
    print(f"bassin {n} personnes, {len(items)} items, "
          f"{int(est_achat.sum())} d'achat et {int((~est_achat).sum())} d'heuristiques",
          flush=True)

    i_achat = np.flatnonzero(est_achat)
    i_heur = np.flatnonzero(~est_achat)

    # ---- V1 : le tableau croise -------------------------------------------------
    print("\n[V1] tableau croise famille x nombre de modalites", flush=True)
    croise = pd.crosstab(pd.Series(np.where(est_achat, "achat", "heuristiques"),
                                   name="famille"),
                         pd.Series(nmod, name="n_modalites"))
    print(croise.to_string(), flush=True)
    chi2 = 0.0
    tot = croise.values.sum()
    for i in range(croise.shape[0]):
        for j in range(croise.shape[1]):
            att = croise.values[i].sum() * croise.values[:, j].sum() / tot
            chi2 += (croise.values[i, j] - att) ** 2 / att if att > 0 else 0.0
    v_cramer = float(np.sqrt(chi2 / (tot * (min(croise.shape) - 1))))
    n_heur_bin = int(((~est_achat) & (nmod == 2)).sum())
    n_achat_nonbin = int((est_achat & (nmod != 2)).sum())
    print(f"V de Cramer = {v_cramer:.4f} ; items d'heuristiques binaires = {n_heur_bin} ; "
          f"items d'achat non binaires = {n_achat_nonbin}", flush=True)
    resume["v_cramer"] = v_cramer
    resume["n_heur_binaires"] = n_heur_bin
    resume["n_achat_non_binaires"] = n_achat_nonbin
    for j in np.flatnonzero((~est_achat) & (nmod == 2)):
        print(f"  hors diagonale, item d'heuristiques binaire : {noms[j]}", flush=True)
        resume["item_hors_diagonale"] = noms[j]

    # ---- V2 : les deux rapports mesurent-ils le meme ensemble ? -----------------
    print("\n[V2] recouvrement entre le classement de A et la partition de B", flush=True)
    rng_eg = np.random.default_rng([GRAINE, 4242])
    brouillage = rng_eg.permutation(len(nmod))
    ordre_mod = np.lexsort((brouillage, nmod.astype(float)))
    top40_A = set(ordre_mod[:40].tolist())
    rec = len(top40_A & set(i_achat.tolist()))
    print(f"  |{{40 items a plus faible nombre de modalites}} INTER {{40 items d'achat}}| "
          f"= {rec} / 40", flush=True)
    resume["recouvrement_A_B_sur_40"] = rec

    # ---- descripteurs par item (V5, partie descriptive) ------------------------
    pool_v13 = paq["codes"][REF_V13][bassin][:, items]
    ent = entropie_items(pool)
    kap = np.array([kappa_item(pool_v13[:, j], pool[:, j]) for j in range(len(items))])
    gain_llm = gain_normalise_items(X_cand, pool)
    gain_h = gain_normalise_items(pool_v13, pool)
    taux_nr = np.array([float((pool[:, j] < 0).mean()) for j in range(len(items))])
    position, longueur = descripteurs_catalogue(noms)
    for j in range(len(items)):
        desc_lignes.append({
            "item_rang": j, "famille": "achat" if est_achat[j] else "heuristiques",
            "n_modalites": int(nmod[j]), "entropie_bits": float(ent[j]),
            "kappa_retest": float(kap[j]), "gain_normalise_jumeau": float(gain_llm[j]),
            "gain_normalise_retest_humain": float(gain_h[j]),
            "taux_non_reponse": float(taux_nr[j]),
            "position_catalogue": float(position[j]),
            "longueur_libelle": float(longueur[j]),
        })
    print("\n[V5] descripteurs par famille (moyennes)", flush=True)
    dd = pd.DataFrame(desc_lignes)
    print(dd.groupby("famille")[["n_modalites", "entropie_bits", "kappa_retest",
                                 "gain_normalise_jumeau", "taux_non_reponse",
                                 "position_catalogue", "longueur_libelle"]]
          .mean().to_string(), flush=True)

    # correlations A L'INTERIEUR du bloc d'achat : le seul endroit ou famille et nombre
    # de modalites sont tous deux constants, donc le seul ou un autre confondant peut
    # parler seul.
    dda = dd[dd.famille == "achat"]
    print("\n[V5] correlation au gain normalise du jumeau, A L'INTERIEUR du bloc d'achat "
          f"(n = {len(dda)} items, famille et nombre de modalites constants)", flush=True)
    for v in ("entropie_bits", "kappa_retest", "taux_non_reponse", "position_catalogue",
              "longueur_libelle"):
        x = dda[v].values.astype(float)
        y = dda["gain_normalise_jumeau"].values.astype(float)
        m = np.isfinite(x) & np.isfinite(y)
        r = float(np.corrcoef(x[m], y[m])[0, 1]) if m.sum() > 3 and x[m].std() > 0 else np.nan
        print(f"    r({v:22s}, gain) = {r:+.3f}", flush=True)
        resume[f"r_interne_achat_{v}"] = r

    # La meme correlation A L'INTERIEUR du bloc d'heuristiques, et l'etendue des positions
    # par famille : une variable qui ne SEPARE pas les deux familles ne peut pas expliquer
    # l'ecart entre elles, quelle que soit sa force a l'interieur d'un bloc.
    ddh = dd[dd.famille == "heuristiques"]
    for v in ("entropie_bits", "kappa_retest", "position_catalogue", "longueur_libelle"):
        x = ddh[v].values.astype(float)
        y = ddh["gain_normalise_jumeau"].values.astype(float)
        m = np.isfinite(x) & np.isfinite(y)
        r = float(np.corrcoef(x[m], y[m])[0, 1]) if m.sum() > 3 and x[m].std() > 0 else np.nan
        resume[f"r_interne_heur_{v}"] = r
    for fam, sous in (("achat", dda), ("heuristiques", ddh)):
        print(f"    position au catalogue, {fam:12s} : "
              f"{sous.position_catalogue.min():.0f} - {sous.position_catalogue.max():.0f}",
              flush=True)
        resume[f"position_min_{fam}"] = float(sous.position_catalogue.min())
        resume[f"position_max_{fam}"] = float(sous.position_catalogue.max())

    # ---- V3 / V4 : les conditions, TOUTES a 20 items ---------------------------
    print(f"\n[V3/V4] conditions a nombre d'items apparie (k = {K_APPARIE} partout)",
          flush=True)

    # reference non appariee, pour raccorder aux chiffres publies de A et de B
    lignes.append(ligne("V3", "40 items d'achat, natifs (reference de B)",
                        mesurer(X_cand[:, i_achat], X_demo[:, i_achat], pool[:, i_achat],
                                "achat40"), "non apparie : 40 items"))
    lignes.append(ligne("V3", "60 items, natifs (reference publiee)",
                        mesurer(X_cand, X_demo, pool, "tous60"),
                        "non apparie : 60 items"))

    # (a) 20 items d'heuristiques natifs
    res_h_natif = mesurer(X_cand[:, i_heur], X_demo[:, i_heur], pool[:, i_heur], "heur20")
    lignes.append(ligne("V3", "20 items d'heuristiques, natifs (5,6 modalites)",
                        res_h_natif))

    # (b) 20 items d'achat tires au hasard, N tirages
    rng_t = np.random.default_rng([GRAINE, 77])
    taux_a20 = []
    for t in range(N_TIRAGES_ACHAT):
        sel = i_achat[rng_t.choice(len(i_achat), K_APPARIE, replace=False)]
        r = mesurer(X_cand[:, sel], X_demo[:, sel], pool[:, sel], f"achat20|{t}")
        taux_a20.append(r["cand_top1"])
        lignes.append(ligne("V3", f"20 items d'achat, tirage {t + 1}/{N_TIRAGES_ACHAT}", r,
                            "binaires"))
    m_a20 = float(np.mean(taux_a20))
    print(f"  --> 20 items d'achat : moyenne {m_a20 * 100:.2f} % "
          f"(etendue {min(taux_a20) * 100:.2f} - {max(taux_a20) * 100:.2f})", flush=True)
    resume["achat20_moyen"] = m_a20
    resume["heur20_natif"] = res_h_natif["cand_top1"]

    # (b bis) 20 items d'achat APPARIES EN POSITION sur les 20 items d'heuristiques.
    # La position au catalogue est le seul confondant que V5 trouve actif A L'INTERIEUR
    # du bloc d'achat ; ce tirage-ci le neutralise entre les deux familles au lieu de le
    # laisser au hasard. Appariement par plus proche voisin sans remise.
    libres = list(i_achat)
    sel_pos = []
    for j in sorted(i_heur, key=lambda u: position[u]):
        k = min(libres, key=lambda u: abs(position[u] - position[j]))
        libres.remove(k)
        sel_pos.append(k)
    sel_pos = np.array(sel_pos)
    ecart_med = float(np.median([abs(position[a] - position[h]) for a, h in
                                 zip(sel_pos, sorted(i_heur, key=lambda u: position[u]))]))
    r = mesurer(X_cand[:, sel_pos], X_demo[:, sel_pos], pool[:, sel_pos], "achat20pos")
    lignes.append(ligne("V3", "20 items d'achat APPARIES EN POSITION", r,
                        f"ecart median de position {ecart_med:.0f} rangs"))
    resume["achat20_apparie_position"] = r["cand_top1"]

    # (c) V4a : les 20 items d'heuristiques DICHOTOMISES, deux regles
    est_ord = np.array([bool(paq["est_ordinal"][j]) for j in items])
    for nom_regle, fonc in (("mode contre non-mode", "mode"), ("coupure a la mediane", "med")):
        if fonc == "mode":
            Pr = recoder_mode(pool[:, i_heur], pool[:, i_heur])
            Cr = recoder_mode(pool[:, i_heur], X_cand[:, i_heur])
            Dr = recoder_mode(pool[:, i_heur], X_demo[:, i_heur])
        else:
            eo = est_ord[i_heur]
            Pr = recoder_mediane(pool[:, i_heur], pool[:, i_heur], eo)
            Cr = recoder_mediane(pool[:, i_heur], X_cand[:, i_heur], eo)
            Dr = recoder_mediane(pool[:, i_heur], X_demo[:, i_heur], eo)
        ent_r = float(entropie_items(Pr).mean())
        r = mesurer(Cr, Dr, Pr, f"heurbin|{fonc}")
        r["entropie_moyenne"] = ent_r
        lignes.append(ligne("V4a", f"20 items d'heuristiques BINARISES ({nom_regle})", r,
                            f"entropie moyenne {ent_r:.3f} bit"))
        resume[f"heur20_bin_{fonc}"] = r["cand_top1"]
        resume[f"heur20_bin_{fonc}_bas"] = r["cand_top1_bas"]
        resume[f"heur20_bin_{fonc}_base_haut"] = r["base_top1_haut"]
        resume[f"heur20_bin_{fonc}_passe"] = r["au_dessus_baseline"]
        resume[f"heur20_bin_{fonc}_entropie"] = ent_r

    # V4a hors pli : regle estimee sur une moitie, taux mesure sur l'autre
    mA, mB = moities(n)
    taux_hp = []
    for nom_pli, i_regle, i_mes in (("A->B", mA, mB), ("B->A", mB, mA)):
        Pr = recoder_mode(pool[i_regle][:, i_heur], pool[i_mes][:, i_heur])
        Cr = recoder_mode(pool[i_regle][:, i_heur], X_cand[i_mes][:, i_heur])
        Dr = recoder_mode(pool[i_regle][:, i_heur], X_demo[i_mes][:, i_heur])
        r = mesurer(Cr, Dr, Pr, f"heurbinhp|{nom_pli}")
        taux_hp.append(r["cand_top1"])
        lignes.append(ligne("V4a", f"20 items d'heuristiques BINARISES, hors pli {nom_pli}",
                            r, "bassin reduit de moitie : non comparable au bassin entier"))
    # temoin du meme demi-bassin : 20 items d'heuristiques natifs, hors pli
    for nom_pli, i_mes in (("A->B", mB), ("B->A", mA)):
        r = mesurer(X_cand[i_mes][:, i_heur], X_demo[i_mes][:, i_heur],
                    pool[i_mes][:, i_heur], f"heurnatifhp|{nom_pli}")
        lignes.append(ligne("V4a", f"20 items d'heuristiques natifs, demi-bassin {nom_pli}",
                            r, "temoin de meme bassin pour la ligne binarisee"))
    resume["heur20_bin_horspli"] = float(np.mean(taux_hp))

    # (d) V4b : les 40 items d'achat DEGRADES en 20 composites a 4 modalites
    taux_comp = []
    rng_p = np.random.default_rng([GRAINE, 909])
    for t in range(N_APPARIEMENTS):
        perm = rng_p.permutation(len(i_achat))
        paires = [(i_achat[perm[2 * u]], i_achat[perm[2 * u + 1]])
                  for u in range(len(i_achat) // 2)]
        Pc = composer_paires(pool, paires, 2)
        Cc = composer_paires(X_cand, paires, 2)
        Dc = composer_paires(X_demo, paires, 2)
        r = mesurer(Cc, Dc, Pc, f"comp|{t}")
        taux_comp.append(r["cand_top1"])
        lignes.append(ligne("V4b", f"20 composites d'achat a 4 modalites, appariement "
                                   f"{t + 1}/{N_APPARIEMENTS}", r,
                            "information des 40 items exactement conservee"))
    m_comp = float(np.mean(taux_comp))
    ref40 = lignes[0]["cand_top1"]
    print(f"  --> composites : moyenne {m_comp * 100:.2f} % contre {ref40 * 100:.2f} % "
          f"pour les 40 items natifs, meme information "
          f"(chute relative {100 * (ref40 - m_comp) / ref40:.1f} %)", flush=True)
    resume["composites_moyen"] = m_comp
    resume["achat40_natif"] = ref40
    resume["chute_relative_composites"] = float((ref40 - m_comp) / ref40)

    # ---- V6 : le controle d'interpretabilite -----------------------------------
    print("\n[V6] controle d'interpretabilite, sur les colonnes natives reellement en jeu",
          flush=True)
    for etiq, sel in (("20 items d'heuristiques", i_heur),
                      ("40 items d'achat", i_achat),
                      ("les 60 items", np.arange(len(items)))):
        cols = items[sel]
        try:
            d = controle_avant_interpretation(bassin, cols, X_cand[:, sel],
                                              f"JSON Persona GPT4.1 | {etiq}", paq=paq)
            verdict = "PASSE"
        except EchecControleInterpretabilite as exc:
            d = exc.diagnostic
            verdict = "ECHOUE"
        print(f"  {etiq:24s} {verdict} : candidat {d['candidat_top1']*100:.2f} % "
              f"[{d['candidat_ic'][0]*100:.2f} ; {d['candidat_ic'][1]*100:.2f}] "
              f"contre baseline {d['baseline_top1']*100:.2f} %", flush=True)
        lignes.append({"volet": "V6", "condition": f"controle | {etiq}",
                       "note": verdict, "n_bassin": d["bassin"], "k_items": d["n_items"],
                       "cand_top1": d["candidat_top1"],
                       "cand_top1_bas": d["candidat_ic"][0],
                       "cand_top1_haut": d["candidat_ic"][1],
                       "base_top1": d["baseline_top1"], "hasard": d["hasard"],
                       "au_dessus_baseline": bool(d["passe"])})
        resume[f"controle_{etiq}"] = verdict

    # ---- verdicts preenregistres ----------------------------------------------
    print("\n=== verdicts sur les predictions preenregistrees ===", flush=True)
    p1 = (n_achat_nonbin == 0) and (n_heur_bin <= 2) and (v_cramer > 0.90)
    p2 = rec >= 39
    # P3 se lit sur le croise REPLIE en 2 x 2 (binaire / non binaire) x (achat /
    # heuristiques) : c'est la partition dont l'article parle. Une case a moins de
    # 5 items ne permet aucun contraste a nombre d'items apparie.
    c22 = np.array([[int((est_achat & (nmod == 2)).sum()),
                     int((est_achat & (nmod != 2)).sum())],
                    [int(((~est_achat) & (nmod == 2)).sum()),
                     int(((~est_achat) & (nmod != 2)).sum())]])
    print(f"  croise replie 2x2 [[achat-bin, achat-nonbin], [heur-bin, heur-nonbin]] = "
          f"{c22.tolist()}", flush=True)
    resume["croise_2x2"] = c22.tolist()
    p3 = bool((c22 < 5).any())
    seuil_p4 = 10 * res_h_natif["cand_top1"]
    meilleur_bin = max(resume["heur20_bin_mode"], resume["heur20_bin_med"])
    passe_bin = resume["heur20_bin_mode_passe"] or resume["heur20_bin_med_passe"]
    p4 = bool(meilleur_bin >= max(seuil_p4, 0.024) and passe_bin)
    p5 = bool(resume["chute_relative_composites"] >= 0.30)
    # P6 n'est declaree confirmee que si les variables ont REELLEMENT ete mesurees :
    # une correlation NaN (colonne vide) ne vaut pas « aucun confondant ». Le taux de
    # non-reponse est le seul NaN legitime, parce qu'il est constant a zero par
    # construction -- les 60 items sont choisis comme toujours renseignes.
    cles_r = [k for k in resume if k.startswith("r_interne_achat_")]
    mesurees = [k for k in cles_r if np.isfinite(resume[k])]
    attendu_nan = ["r_interne_achat_taux_non_reponse"]
    non_mesurees = [k for k in cles_r if k not in mesurees and k not in attendu_nan]
    if non_mesurees:
        raise RuntimeError(f"confondants non mesures (correlation NaN) : {non_mesurees}. "
                           "P6 ne peut pas etre declaree confirmee sur des NaN.")
    p6 = bool(float(taux_nr.max()) == 0.0
              and max(abs(resume[k]) for k in mesurees) <= 0.40)
    p7 = (resume["controle_40 items d'achat"] == "PASSE"
          and resume["controle_20 items d'heuristiques"] == "ECHOUE")
    for nom, v in (("P1 croise quasi diagonal", p1), ("P2 recouvrement >= 39/40", p2),
                   ("P3 indecidable observationnellement", p3),
                   ("P4 la binarisation fait monter les heuristiques", p4),
                   ("P5 les composites chutent de >= 30 %", p5),
                   ("P6 aucun confondant interne au bloc d'achat", p6),
                   ("P7 controle : achat PASSE, heuristiques ECHOUE", p7)):
        print(f"  {nom:52s} {'CONFIRMEE' if v else 'REFUTEE'}", flush=True)
        resume[nom.split()[0]] = "confirmee" if v else "refutee"

    if p4:
        issue = "B : le nombre de modalites"
    elif p5:
        issue = ("mixte : ajouter des modalites nuit, en retirer ne repare pas "
                 "-- ni B ni C")
    else:
        issue = "C : la famille d'items"
    print(f"\nISSUE REALISEE : {issue}", flush=True)
    resume["issue"] = issue

    # ---- ecriture --------------------------------------------------------------
    df = pd.DataFrame(lignes)
    dd["volet"] = "V5-descripteurs"
    dr = pd.DataFrame([{"volet": "resume", "condition": k, "note": str(v)}
                       for k, v in resume.items()])
    pd.concat([df, dd, dr], ignore_index=True).to_csv(SORTIE_CSV, index=False)
    print(f"\necrit : {SORTIE_CSV}", flush=True)


if __name__ == "__main__":
    main()
