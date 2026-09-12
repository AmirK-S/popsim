"""
c7_attaquant_fort : nos taux venaient-ils d'un adversaire faible, et la defense tient-elle ?

===========================================================================
PREENREGISTREMENT : resultats/c7-attaquant-fort-preenregistrement.md (et son addendum
volet 4, attaquant adaptatif), ecrits le 12 septembre 2026, AVANT ce fichier et avant
tout calcul de score.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (Twin-2K-500, archive Park et al.).
Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant d'une personne retrouvee ni
aucun appariement individuel : seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                   les tables Twin et l'ecriture des CSV
  a2_commun.bootstrap_personnes                 IC par reechantillonnage de personnes
  c7_reidentification.items_communs/rangs_attaque/graine_nom/REF_V4/REF_V13
                                                l'attaquant NAIF et ses garde-fous, importe
                                                sans modification pour la comparaison
  c7_stanford.charger_domaine/coder_categoriel_commun/accord_categoriel/rangs_depuis_accord
                                                le bloc GSS de Park et al. et le rang a
                                                partir d'une matrice de score precalculee
  c7_monde_ouvert.marges_deux_regimes/roc_et_taux  le protocole de monde ouvert, inchange
  c7_defense.defense_d4                         la defense D4 telle qu'implementee
  c7_mecanisme.items_achat                      les 40 indices du bloc d'achat

CE QUI EST NOUVEAU ICI : l'attaquant fort A-LLR (rapport de vraisemblance pondere par la
rarete de la modalite et la fiabilite de l'item), son estimation HORS PLI, la variante
simple A-MI (poids = information de l'item deja publiee), et le volet 4 : les trois
strategies d'un attaquant ADAPTATIF qui connait la defense D4.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_attaquant_fort.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from a2_commun import bootstrap_personnes                            # noqa: E402
from c7_reidentification import (                                    # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
import c7_stanford as CS                                             # noqa: E402
from c7_monde_ouvert import marges_deux_regimes, roc_et_taux         # noqa: E402
from c7_defense import defense_d4                                    # noqa: E402
from c7_mecanisme import items_achat                                 # noqa: E402

GRAINE = 20260912
N_PLIS = 5
N_BOOTSTRAP = 2000
N_TIRAGES_LIENS = 20
CIBLE_TWIN = "JSON Persona - GPT4.1"
CIBLE_STAN = "composite"
BITS_CSV = "c7-bits-par-item.csv"


# ---------------------------------------------------------------------------
# 1. Parametres de l'attaquant fort, estimes sur des personnes d'entrainement
# ---------------------------------------------------------------------------

def parametres(x_entr, y_entr):
    """a_j et q_j a partir des SEULES personnes d'entrainement.

    a_j  = probabilite que le jumeau reproduise la reponse de la vraie personne sur l'item j
           (accord apparie, estime sur les paires vraies des personnes d'entrainement).
    q_j  = marginale du jumeau sur l'item j (probabilite d'emettre chaque modalite).
    Lissage de Laplace pour qu'aucune modalite n'ait une probabilite nulle (le log
    diverge sinon), et bornage de a_j loin de 0 et de 1 pour la meme raison.
    """
    n_items = x_entr.shape[1]
    a = np.zeros(n_items)
    q = []
    for j in range(n_items):
        xj, yj = x_entr[:, j], y_entr[:, j]
        ok = (xj >= 0) & (yj >= 0)
        a[j] = float((xj[ok] == yj[ok]).mean()) if ok.sum() >= 5 else 0.5
        vals = xj[xj >= 0]
        n_mod = int(max(xj.max(), yj.max(), 0)) + 1
        comptes = np.bincount(vals, minlength=n_mod).astype(float) if len(vals) \
            else np.zeros(n_mod)
        q.append((comptes + 1.0) / (comptes.sum() + n_mod))
    return np.clip(a, 1e-4, 1 - 1e-4), q


def score_llr(x_test, y_pool, a, q):
    """Score de vraisemblance (n_test, n_pool), somme sur les items observes des deux cotes.

    Accord sur l'item j : log(a_j / q_j(y_cj)) — un accord sur une modalite RARE vaut
    beaucoup plus qu'un accord sur une modalite banale.
    Desaccord : log((1 - a_j) / (1 - q_j(y_cj))) — ne pas reproduire une reponse rare
    penalise peu, ne pas reproduire une reponse banale penalise.
    Si le nombre d'items communs varie d'un candidat a l'autre, la somme est ramenee au
    nombre moyen d'items communs (preenregistrement), pour que les candidats restent
    comparables.
    """
    n_t, n_items = x_test.shape
    n_p = y_pool.shape[0]
    s = np.zeros((n_t, n_p))
    nc = np.zeros((n_t, n_p))
    log_a, log_1a = np.log(a), np.log(1.0 - a)
    for j in range(n_items):
        yj = y_pool[:, j]
        ok_y = yj >= 0
        qy = np.where(ok_y, q[j][np.clip(yj, 0, len(q[j]) - 1)], 0.5)
        qy = np.clip(qy, 1e-9, 1 - 1e-9)
        u = log_1a[j] - np.log(1.0 - qy)          # contribution de desaccord, par candidat
        w = (log_a[j] - np.log(qy)) - u           # bonus d'accord, par candidat
        xj = x_test[:, j]
        valide = (xj >= 0)[:, None] & ok_y[None, :]
        accord = (xj[:, None] == yj[None, :]) & valide
        s += np.where(valide, u[None, :], 0.0) + accord * w[None, :]
        nc += valide
    if (nc <= 0).any():
        print(f"  {int((nc <= 0).sum())} paires sans item commun, score plancher", flush=True)
    nbar = float(nc[nc > 0].mean()) if (nc > 0).any() else 1.0
    s = np.where(nc > 0, s * (nbar / np.maximum(nc, 1)), -np.inf)
    if np.isneginf(s).any():
        s[np.isneginf(s)] = s[np.isfinite(s)].min() - 1.0
    return s


def score_mi(x_test, y_pool, poids):
    """Variante simple A-MI : accord pondere par l'information de l'item, normalise.

    Les poids viennent de resultats/c7-bits-par-item.csv, calcules sur TOUTES les personnes :
    avantage en echantillon, au niveau agrege de l'item, concede a cette variante simple et
    declare au preenregistrement. A-LLR, lui, reste strictement hors pli.
    """
    n_t, n_items = x_test.shape
    n_p = y_pool.shape[0]
    s = np.zeros((n_t, n_p))
    d = np.zeros((n_t, n_p))
    for j in range(n_items):
        if poids[j] <= 0:
            continue
        yj = y_pool[:, j]
        ok_y = yj >= 0
        xj = x_test[:, j]
        valide = (xj >= 0)[:, None] & ok_y[None, :]
        accord = (xj[:, None] == yj[None, :]) & valide
        s += accord * poids[j]
        d += valide * poids[j]
    return np.where(d > 0, s / np.maximum(d, 1e-12), 0.0)


def plis(n, graine_suffixe):
    rng = np.random.default_rng([GRAINE, 7, graine_suffixe])
    return np.array_split(rng.permutation(n), N_PLIS)


def scores_hors_pli(x, y_pool, vrai_idx, etiquette, colonnes=None):
    """Matrice de score A-LLR (n_attaques, n_pool), parametres estimes HORS PLI.

    Les personnes du pli k sont les personnes attaquees ; a_j et q_j sont estimes
    uniquement sur les personnes des quatre autres plis. Aucune reponse de la personne
    attaquee, ni du jumeau ni de l'humain, n'entre dans ses propres parametres. Le pool
    des candidats reste la population entiere.
    """
    if colonnes is not None:
        x = x[:, colonnes]
        y_pool = y_pool[:, colonnes]
    n_att = x.shape[0]
    s = np.zeros((n_att, y_pool.shape[0]))
    for pli in plis(n_att, graine_nom(etiquette)):
        entr = np.setdiff1d(np.arange(n_att), pli)
        a, q = parametres(x[entr], y_pool[vrai_idx[entr]])
        s[pli] = score_llr(x[pli], y_pool, a, q)
    return s


# ---------------------------------------------------------------------------
# 2. Mesures communes : monde ferme (top-1, top-10) et monde ouvert (TPR a FPR fixe)
# ---------------------------------------------------------------------------

def mesurer(nom_jeu, nom_attaque, score, vrai_idx, ouvert=True):
    rng = np.random.default_rng([GRAINE, 11, graine_nom(nom_jeu + "|" + nom_attaque)])
    _, top1, top10 = CS.rangs_depuis_accord(score, vrai_idx, rng, N_TIRAGES_LIENS)
    m1, b1, h1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, 12])
    m10, b10, h10 = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, 13])
    ligne = {"jeu": nom_jeu, "attaque": nom_attaque, "n": score.shape[0],
             "n_pool": score.shape[1], "top1": m1, "top1_bas": b1, "top1_haut": h1,
             "top10": m10, "top10_bas": b10, "top10_haut": h10}
    if ouvert:
        rng_o = np.random.default_rng([GRAINE, 14, graine_nom(nom_attaque)])
        mp, correct, mr = marges_deux_regimes(score, vrai_idx, rng_o)
        r = roc_et_taux(mp, correct, mr, score.shape[0])
        ligne.update({"auc_ouvert": r["auc"], "tpr_fpr_0_1pct": r["tpr_fpr_0_1pct"],
                      "tpr_fpr_1pct": r["tpr_fpr_1pct"]})
    print(f"  {nom_jeu:9s} / {nom_attaque:34s} top1={m1:.4f} [{b1:.4f};{h1:.4f}] "
          f"top10={m10:.4f}" + (f" TPR@0,1%={ligne['tpr_fpr_0_1pct']:.4f} "
          f"TPR@1%={ligne['tpr_fpr_1pct']:.4f}" if ouvert else ""), flush=True)
    return ligne


def mesurer_naif_twin(x, pool, vrai_idx, nom_attaque, ouvert=True):
    """Attaquant naif sur Twin : rangs_attaque importee sans modification."""
    rng = np.random.default_rng([GRAINE, 15, graine_nom(nom_attaque)])
    _, top1, top10 = rangs_attaque(x, pool, vrai_idx, rng)
    m1, b1, h1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, 12])
    m10, b10, h10 = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, 13])
    ligne = {"jeu": "Twin", "attaque": nom_attaque, "n": x.shape[0], "n_pool": pool.shape[0],
             "top1": m1, "top1_bas": b1, "top1_haut": h1,
             "top10": m10, "top10_bas": b10, "top10_haut": h10}
    if ouvert:
        from a2_commun import distance_hamming
        accord = 1.0 - distance_hamming(x, pool)
        rng_o = np.random.default_rng([GRAINE, 14, graine_nom(nom_attaque)])
        mp, correct, mr = marges_deux_regimes(accord, vrai_idx, rng_o)
        r = roc_et_taux(mp, correct, mr, x.shape[0])
        ligne.update({"auc_ouvert": r["auc"], "tpr_fpr_0_1pct": r["tpr_fpr_0_1pct"],
                      "tpr_fpr_1pct": r["tpr_fpr_1pct"]})
    print(f"  Twin      / {nom_attaque:34s} top1={m1:.4f} [{b1:.4f};{h1:.4f}] "
          f"top10={m10:.4f}" + (f" TPR@0,1%={ligne['tpr_fpr_0_1pct']:.4f} "
          f"TPR@1%={ligne['tpr_fpr_1pct']:.4f}" if ouvert else ""), flush=True)
    return ligne


def poids_mi(jeu, predicteur, n_items):
    d = pd.read_csv(os.path.join(T1.SORTIE, BITS_CSV))
    d = d[(d.jeu == jeu) & (d.predicteur == predicteur)].sort_values("item")
    w = np.clip(d.mi_bits.to_numpy(dtype=float), 0.0, None)
    if len(w) != n_items:
        raise SystemExit(f"poids MI : {len(w)} valeurs pour {n_items} items ({jeu}/{predicteur})")
    return np.nan_to_num(w)


# ---------------------------------------------------------------------------
# 3. Volets 1 et 3 : attaquant fort, monde ferme et monde ouvert, deux jeux
# ---------------------------------------------------------------------------

def bloc_twin(lignes):
    print("\n=== Twin-2K-500 : volets 1 et 3 ===", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    x = codes[CIBLE_TWIN][:, items]
    couverts = np.flatnonzero((codes[CIBLE_TWIN] >= 0).any(axis=1))
    xc = x[couverts]
    print(f"{pool.shape[0]} personnes, {len(items)} items communs, "
          f"{len(couverts)} jumeaux couverts", flush=True)

    lignes.append(mesurer_naif_twin(xc, pool, couverts, "naif (Hamming)"))
    s_mi = score_mi(xc, pool, poids_mi("Twin-2K-500", CIBLE_TWIN, len(items)))
    lignes.append(mesurer("Twin", "A-MI (poids information)", s_mi, couverts))
    s_llr = scores_hors_pli(xc, pool, couverts, "twin|llr")
    lignes.append(mesurer("Twin", "A-LLR (vraisemblance, hors pli)", s_llr, couverts))
    return paq, codes, items, pool, couverts


def bloc_stanford(lignes):
    print("\n=== Archive Park et al., bloc GSS : volets 1 et 3 ===", flush=True)
    _, items, tables, _ = CS.charger_domaine("gss")
    codes = CS.coder_categoriel_commun(tables, items)
    pool = codes[CS.VAGUE1]
    x = codes[CIBLE_STAN]
    n = pool.shape[0]
    vrai_idx = np.arange(n)
    print(f"{n} personnes, {len(items)} items (condition {CIBLE_STAN})", flush=True)

    rng = np.random.default_rng([GRAINE, 16])
    _, top1, top10 = CS.rangs_depuis_accord(CS.accord_categoriel(x, pool), vrai_idx, rng,
                                             N_TIRAGES_LIENS)
    m1, b1, h1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, 12])
    m10, b10, h10 = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, 13])
    rng_o = np.random.default_rng([GRAINE, 14, graine_nom("stan|naif")])
    mp, correct, mr = marges_deux_regimes(CS.accord_categoriel(x, pool), vrai_idx, rng_o)
    r = roc_et_taux(mp, correct, mr, n)
    lignes.append({"jeu": "Park GSS", "attaque": "naif (Hamming)", "n": n, "n_pool": n,
                   "top1": m1, "top1_bas": b1, "top1_haut": h1,
                   "top10": m10, "top10_bas": b10, "top10_haut": h10,
                   "auc_ouvert": r["auc"], "tpr_fpr_0_1pct": r["tpr_fpr_0_1pct"],
                   "tpr_fpr_1pct": r["tpr_fpr_1pct"]})
    print(f"  Park GSS  / {'naif (Hamming)':34s} top1={m1:.4f} [{b1:.4f};{h1:.4f}] "
          f"top10={m10:.4f} TPR@0,1%={r['tpr_fpr_0_1pct']:.4f} "
          f"TPR@1%={r['tpr_fpr_1pct']:.4f}", flush=True)

    s_mi = score_mi(x, pool, poids_mi("Stanford GSS", CIBLE_STAN, len(items)))
    lignes.append(mesurer("Park GSS", "A-MI (poids information)", s_mi, vrai_idx))
    s_llr = scores_hors_pli(x, pool, vrai_idx, "stan|llr")
    lignes.append(mesurer("Park GSS", "A-LLR (vraisemblance, hors pli)", s_llr, vrai_idx))


# ---------------------------------------------------------------------------
# 4. Volet 2 : la defense D4 sous l'attaquant fort
# ---------------------------------------------------------------------------

def bloc_defense(lignes, paq, codes, items, pool, couverts):
    print("\n=== Volet 2 : defense D4 sous l'attaquant fort ===", flush=True)
    seg_gra = paq["seg"]["S_gra"]
    seg_c = seg_gra[couverts]
    achat_mask = np.isin(items, items_achat(paq))
    i_achat = np.flatnonzero(achat_mask)
    i_opinion = np.flatnonzero(~achat_mask)
    print(f"{len(i_achat)} items d'achat permutes par D4, {len(i_opinion)} items "
          f"d'opinion INTACTS", flush=True)

    xc = codes[CIBLE_TWIN][:, items][couverts]
    x40_def = defense_d4(xc[:, i_achat], seg_c)
    x_def = np.empty_like(xc)
    x_def[:, i_achat] = x40_def
    x_def[:, i_opinion] = xc[:, i_opinion]

    lignes.append(mesurer_naif_twin(x_def, pool, couverts, "D4 / naif (Hamming)"))
    s_mi = score_mi(x_def, pool, poids_mi("Twin-2K-500", CIBLE_TWIN, len(items)))
    lignes.append(mesurer("Twin", "D4 / A-MI", s_mi, couverts))
    s_llr = scores_hors_pli(x_def, pool, couverts, "twin|d4|llr")
    lignes.append(mesurer("Twin", "D4 / A-LLR (recalibre sur D4)", s_llr, couverts))
    return x_def, i_achat, i_opinion, seg_c, seg_gra


# ---------------------------------------------------------------------------
# 5. Volet 4 : l'attaquant ADAPTATIF, qui connait D4
# ---------------------------------------------------------------------------

def score_invariant(x40_def, x40_test, seg_c, seg_pool, a, q, i_achat):
    """S3 : appariement des modalites RARES au multiensemble preserve du segment.

    D4 permute les reponses A L'INTERIEUR d'un segment : l'ensemble des modalites presentes
    dans un segment, item par item, est donc EXACTEMENT preserve. C'est une quantite
    invariante que l'attaquant peut exploiter sans connaitre la permutation tiree. Le score
    d'un candidat c vaut, sur les 40 items d'achat, la somme des raretes -log q_j(x_ij) des
    modalites du jumeau qui figurent dans le multiensemble du segment de c.
    """
    n_t = x40_test.shape[0]
    n_p = len(seg_pool)
    segments = np.unique(seg_c[seg_c >= 0])
    s = np.zeros((n_t, n_p))
    for j in range(x40_test.shape[1]):
        n_mod = len(q[j])
        presence = {}
        for g in segments:
            vals = x40_def[(seg_c == g), j]
            marque = np.zeros(n_mod, dtype=bool)
            v = vals[(vals >= 0) & (vals < n_mod)]
            marque[v] = True
            presence[g] = marque
        xj = x40_test[:, j]
        rarete = np.where(xj >= 0, -np.log(q[j][np.clip(xj, 0, n_mod - 1)]), 0.0)
        for g in segments:
            colonnes = np.flatnonzero(seg_pool == g)
            if not len(colonnes):
                continue
            dedans = np.zeros(n_t, dtype=bool)
            ok = xj >= 0
            dedans[ok] = presence[g][np.clip(xj[ok], 0, n_mod - 1)]
            s[:, colonnes] += (dedans * rarete)[:, None]
    return s


def exactitude_segment(score, vrai_idx, seg_pool, seg_vrai, etiquette):
    """S2 : l'attaquant designe un SEGMENT, pas une personne.

    Deux lectures : le segment du meilleur candidat, et le segment dont les membres ont le
    meilleur score moyen. Comparees au hasard (tirage d'un candidat au hasard) et au
    segment le plus frequent. Retrouver le segment sans retrouver l'identite reste une
    DIVULGATION D'ATTRIBUT, d'une autre nature que la reidentification.
    """
    segments = np.unique(seg_pool[seg_pool >= 0])
    pred_argmax = seg_pool[np.argmax(score, axis=1)]
    moyennes = np.column_stack([score[:, seg_pool == g].mean(axis=1) for g in segments])
    pred_moyenne = segments[np.argmax(moyennes, axis=1)]
    parts = np.array([(seg_pool == g).mean() for g in segments])
    ok = seg_vrai >= 0
    return {"strategie": etiquette,
            "exactitude_segment_meilleur_candidat": float((pred_argmax[ok] == seg_vrai[ok]).mean()),
            "exactitude_segment_score_moyen": float((pred_moyenne[ok] == seg_vrai[ok]).mean()),
            "hasard_tirage_candidat": float((parts ** 2).sum()),
            "segment_le_plus_frequent": float(parts.max()),
            "n_segments": int(len(segments))}


def bloc_adaptatif(lignes, lignes_seg, x_def, pool, couverts, i_achat, i_opinion,
                   seg_c, seg_gra):
    print("\n=== Volet 4 : attaquant ADAPTATIF, qui connait D4 ===", flush=True)

    # [S1] les items non touches : D4 ne permute que les 40 items d'achat.
    s1 = scores_hors_pli(x_def, pool, couverts, "twin|s1", colonnes=i_opinion)
    l1 = mesurer("Twin", "D4 / S1 : 20 items intacts", s1, couverts)
    l1["strategie"] = "S1 items non touches"
    lignes.append(l1)

    # [S3] invariants : multiensemble du segment, preserve par construction.
    n_att = x_def.shape[0]
    s3 = np.zeros((n_att, pool.shape[0]))
    for pli in plis(n_att, graine_nom("twin|s3")):
        entr = np.setdiff1d(np.arange(n_att), pli)
        a, q = parametres(x_def[entr][:, i_achat], pool[couverts[entr]][:, i_achat])
        s3[pli] = score_invariant(x_def[:, i_achat], x_def[pli][:, i_achat], seg_c,
                                  seg_gra, a, q, i_achat)
    l3 = mesurer("Twin", "D4 / S3 : invariants de segment", s3, couverts)
    l3["strategie"] = "S3 invariants seuls"
    lignes.append(l3)

    s13 = s1 + s3
    l13 = mesurer("Twin", "D4 / S1+S3 combinees", s13, couverts)
    l13["strategie"] = "S1+S3 combinees"
    lignes.append(l13)

    # [S2] divulgation d'attribut : le segment, pas l'identite.
    seg_vrai = seg_gra[couverts]
    for etiq, sc in (("S1 items non touches", s1), ("S3 invariants seuls", s3),
                     ("S1+S3 combinees", s13)):
        d = exactitude_segment(sc, couverts, seg_gra, seg_vrai, etiq)
        lignes_seg.append(d)
        print(f"  S2 segment / {etiq:28s} exactitude={d['exactitude_segment_score_moyen']:.4f} "
              f"(meilleur candidat {d['exactitude_segment_meilleur_candidat']:.4f}) "
              f"hasard={d['hasard_tirage_candidat']:.4f} "
              f"plus frequent={d['segment_le_plus_frequent']:.4f}", flush=True)


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes, lignes_seg = [], []

    paq, codes, items, pool, couverts = bloc_twin(lignes)
    bloc_stanford(lignes)
    x_def, i_achat, i_opinion, seg_c, seg_gra = bloc_defense(
        lignes, paq, codes, items, pool, couverts)
    bloc_adaptatif(lignes, lignes_seg, x_def, pool, couverts, i_achat, i_opinion,
                   seg_c, seg_gra)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-attaquant-fort.csv")
    T1.ecrire(pd.DataFrame(lignes_seg), "c7-attaquant-fort-segment.csv")

    # --- verdict sur les predictions preenregistrees ---
    print("\n--- verdict ---", flush=True)

    def top1(jeu, attaque):
        r = df[(df.jeu == jeu) & (df.attaque == attaque)]
        return float(r.top1.iloc[0]) if len(r) else np.nan

    for jeu, naif, fort in (("Twin", "naif (Hamming)", "A-LLR (vraisemblance, hors pli)"),
                            ("Park GSS", "naif (Hamming)", "A-LLR (vraisemblance, hors pli)")):
        tn, tf = top1(jeu, naif), top1(jeu, fort)
        rel = (tf - tn) / tn * 100 if tn else np.nan
        print(f"[P1] {jeu} : naif={tn:.4f} fort={tf:.4f} soit {rel:+.1f} % relatifs "
              f"-> P1 {'tenue' if rel >= 20 else 'REFUTEE'}", flush=True)

    t_d4 = top1("Twin", "D4 / A-LLR (recalibre sur D4)")
    print(f"[P2] D4 sous A-LLR non adaptatif : top1={t_d4:.4f} "
          f"-> P2 {'tenue' if t_d4 < 0.01 else 'REFUTEE'}", flush=True)

    pires = df[df.attaque.str.startswith("D4 / S")]
    if len(pires):
        pire = pires.loc[pires.top1.idxmax()]
        t_nd = top1("Twin", "naif (Hamming)")
        print(f"[P3] meilleure strategie adaptative : {pire.attaque}, top1={pire.top1:.4f} "
              f"(non defendu {t_nd:.4f}) -> P3 "
              f"{'tenue' if 0.01 < pire.top1 < t_nd else 'REFUTEE'}", flush=True)
        if pire.top1 >= 0.5 * t_nd:
            print("      ISSUE FRANCHE : la fuite revient pres de son niveau initial, "
                  "D4 NE TIENT PAS.", flush=True)


if __name__ == "__main__":
    main()
