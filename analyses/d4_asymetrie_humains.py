"""
d4_asymetrie_humains : la diversite politique d'un camp, chez les humains, en trois
quantites qui ne se reduisent pas a la position des items.

LE PREENREGISTREMENT EST resultats/d4-preenregistrement.md, ECRIT AVANT CE FICHIER,
le 2026-09-09 a 12:05 CEST. Aucune quantite, aucun perimetre, aucun critere n'est ajoute
ici.

Statut : script d'analyse jetable. Aucun appel de modele de langage, aucun serveur
d'inference, lecture seule sur data/, aucune microdonnee ecrite. Aucun script existant
n'est modifie : a30_commun, a30_structure, a37_commun, a44_commun, a2_baselines_gss,
a25_commun, a9_commun, a12_retest_delai et i1_commun sont importes tels quels.

LES TROIS QUANTITES, RAPPEL DU PREENREGISTREMENT SECTION 3
----------------------------------------------------------
  Q1  Dispersion residuelle. R(j, c) = GS_obs(j, c) - GS_pos(j, c), ou GS_pos est le
      temoin de position de a37 (loi d'entropie maximale a moyenne fixee). Publiee comme
      contraste apparie item par item, droite moins gauche. Restreinte aux items a trois
      modalites ou plus : sur un item binaire le residu est nul par identite.
  Q2  Patrons de reponses distincts, a taille egale, EN EXCES DU NUL de gabarit.
      E(c) = patrons_obs(c) - patrons_nul(c). E est negatif ; moins negatif veut dire
      moins contraint, donc plus divers.
  Q3  Dimension effective de la structure de correlation, normalisee par celle du nul.
      D_eff = (trace)^2 / ||R||_F^2 = J^2 / (J + 2 somme_{i<j} rho_ij^2), avec rho de
      Spearman. Deff_norm(c) = D_eff(c) / D_eff_nul(c).

Le nul est celui de a44 : X_ij tire independamment dans la loi empirique de l'item j A
L'INTERIEUR DU CAMP c. Il a donc exactement les memes marginales, donc exactement les
memes positions, et aucune structure. C'est le critere O du preenregistrement.

SORTIES
-------
  resultats/d4-q1-par-item.csv       le residu item par item, les deux camps, GSS
  resultats/d4-contrastes.csv        les trois quantites, toutes conditions, tous jeux
  resultats/d4-nuls.csv              observe, nul, et ecart, pour Q2 et Q3
  resultats/d4-planchers.csv         les planchers de reinterrogation
  resultats/d4-controles.csv         appariement, ancrage partisan, sensibilite a n_egal
  resultats/d4-polarite.csv          Q1 par signe de la derive, et les regressions
  resultats/d4-verdicts.csv          les criteres de la section 7, coches ou non

Usage : .venv/bin/python analyses/d4_asymetrie_humains.py [--rapide]
"""

import argparse
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C            # noqa: E402
import a37_commun as A            # noqa: E402
import a44_commun as C44          # noqa: E402
from a30_structure import apparie  # noqa: E402
from a2_baselines_gss import charger  # noqa: E402
from a25_commun import options_par_item, sans_score  # noqa: E402

RACINE = C.RACINE
SORTIE = C.SORTIE

# --- fige par le preenregistrement section 9 --------------------------------
GRAINE = 20260909
J_SOUS = 10        # items par sous ensemble, Q2
N_JEUX = 200       # sous ensembles d'items, Q2
N_TIRAGES = 20     # tirages de personnes par sous ensemble, Q2
N_NULS = 50        # replicats du generateur nul
N_BOOT = 1000      # tirages de bootstrap, tests apparies
N_DRAWS_Q3 = 200   # tirages de personnes, Q3
N_MIN_ITEM = C.N_MIN_ITEM   # 30, seuil de a30


# ===========================================================================
# 0. Briques communes aux trois jeux de donnees
# ===========================================================================

def scores_generiques_depuis_ks(ks, kmax):
    """Score 0..1 par modalite, direction arbitraire.

    Le temoin de position est invariant par retournement de l'echelle : la grille
    {0, 1/(K-1), ..., 1} est symetrique, donc la loi d'entropie maximale a la position p
    et celle a la position 1 - p sont images l'une de l'autre et ont le meme Gini
    Simpson. La direction n'a donc aucune importance pour Q1 ; elle n'en a que pour le
    controle de polarite, qui emploie l'orientation de a37.
    """
    J = len(ks)
    S = np.full((J, kmax), np.nan, dtype=np.float64)
    for j in range(J):
        K = int(ks[j])
        if K >= 2:
            S[j, :K] = np.arange(K, dtype=np.float64) / (K - 1.0)
    return S


def q1_residus(ind, masque, S):
    """R(j) = GS observe moins GS du temoin de position, item par item, un camp."""
    t = ind.tables(C.poids_plein(masque))
    gs = C.mesures(t)["gs"][0]
    tem = A.gs_temoin(t, S)[0]
    n = C.mesures(t)["n"][0]
    return gs - tem, gs, tem, n


def lois_du_camp(codes, masque, ks):
    """Lois empiriques par item A L'INTERIEUR du camp, cumulees, pour le nul de a44.

    On appelle a44_commun.lois_par_segment avec un segment unique reduit au camp : le
    nul reproduit alors exactement les marginales du camp, item par item.
    """
    sous = codes[masque]
    seg = np.zeros(len(sous), dtype=np.int64)
    cumules, replis, total = C44.lois_par_segment(sous, seg, list(np.asarray(ks, int)),
                                                  n_min=1)
    return sous, seg, cumules, replis, total


def patrons_sur(codes_sous, cols, idx_pers):
    """Nombre de lignes distinctes sur cols, pour les personnes idx_pers.

    Convention de a44 : une ligne portant une cellule vide est ecartee.
    """
    sub = codes_sous[np.ix_(idx_pers, cols)]
    pleines = sub[(sub >= 0).all(axis=1)]
    if not len(pleines):
        return np.nan, 0
    return float(len(np.unique(pleines, axis=0))), int(len(pleines))


def rangs(codes_sous):
    """Rangs par item, NaN pour un manquant. Reprise exacte de a44_commun."""
    return C44.rangs_colonne(codes_sous)


def dimension_effective(r, cols, n_min=30):
    """D_eff = J^2 / ||Rho||_F^2, rho de Spearman, paires completes.

    La trace d'une matrice de correlation vaut J exactement, quelle que soit la methode
    d'estimation par paires ; le denominateur est la somme des carres de tous les
    coefficients. On evite ainsi la decomposition spectrale d'une matrice qui, estimee
    par paires completes, peut ne pas etre semi definie positive.
    """
    sub = r[:, cols]
    masque = ~np.isnan(sub)
    v = np.where(masque, sub, 0.0)
    n_obs = masque.sum(axis=0).astype(np.float64)
    garder = n_obs >= 2
    sub, masque, v = sub[:, garder], masque[:, garder], v[:, garder]
    n_obs = n_obs[garder]
    J = sub.shape[1]
    if J < 2:
        return np.nan, 0
    moyennes = v.sum(axis=0) / np.maximum(n_obs, 1.0)
    b = np.where(masque, sub - moyennes[None, :], 0.0)
    mf = masque.astype(np.float64)
    n_paire = mf.T @ mf
    cov = b.T @ b
    var = (b ** 2).T @ mf
    with np.errstate(invalid="ignore", divide="ignore"):
        rho = cov / np.sqrt(np.maximum(var * var.T, 1e-300))
    haut = np.triu_indices(J, k=1)
    val, npr = rho[haut], n_paire[haut]
    bon = np.isfinite(val) & (npr >= n_min)
    if bon.sum() < 3:
        return np.nan, 0
    # Frobenius restreint aux paires estimables, remis a l'echelle du nombre de paires
    # retenues : sans quoi un jeu avec beaucoup de paires ecartees aurait mecaniquement
    # une dimension effective plus haute.
    moy_carre = float((val[bon] ** 2).mean())
    frob = J + 2.0 * moy_carre * (J * (J - 1) / 2.0)
    return float(J * J / frob), int(bon.sum())


# ===========================================================================
# 1. Le moteur : les trois quantites sur un jeu de codes et une partition
# ===========================================================================

def q2_q3(codes, masques, cols_perimetre, ks, rng, n_egal,
          n_jeux=N_JEUX, n_tirages=N_TIRAGES, n_nuls=N_NULS,
          n_draws_q3=N_DRAWS_Q3, etiquette=""):
    """Q2 et Q3, observe et nul, camp par camp, a effectif egal.

    Retourne deux tableaux longs : un par (camp, jeu, tirage) pour Q2, un par
    (camp, tirage) pour Q3, avec la valeur observee et la valeur du nul appariee.
    """
    cols_perimetre = np.asarray(cols_perimetre)
    J = len(cols_perimetre)
    # Sous ensembles d'items tires UNE FOIS et partages par tous les camps et par le nul.
    rng_items = np.random.default_rng(GRAINE + 1)
    sous_ens = [np.sort(rng_items.choice(J, size=min(J_SOUS, J), replace=False))
                for _ in range(n_jeux)]
    # Tirages de personnes : un plan d'indices par camp, partage entre observe et nul.
    q2, q3 = [], []
    for nom, m in masques.items():
        idx_camp = np.flatnonzero(m)
        if len(idx_camp) < n_egal:
            continue
        sous = codes[idx_camp][:, cols_perimetre]
        _, seg, cumules, replis, total = lois_du_camp(
            codes[:, cols_perimetre], m, ks[cols_perimetre])
        rl = np.random.default_rng(GRAINE + abs(hash(nom)) % 10000)
        nuls = [C44.tirer_nul(sous, seg, cumules, rl) for _ in range(n_nuls)]

        # ---- Q2 -----------------------------------------------------------
        for t, cols in enumerate(sous_ens):
            for u in range(n_tirages):
                s = rl.choice(len(sous), size=n_egal, replace=False)
                po, no = patrons_sur(sous, cols, s)
                i_nul = (t * n_tirages + u) % n_nuls
                pn, nn = patrons_sur(nuls[i_nul], cols, s)
                # Controle bloquant numero 1 : un second replicat du nul, pour mesurer
                # l'ecart nul contre nul et le comparer a l'ecart observe contre nul.
                pn2, _ = patrons_sur(nuls[(i_nul + 1) % n_nuls], cols, s)
                q2.append({"jeu_de_donnees": etiquette, "camp": nom, "sous_ensemble": t,
                           "tirage": u, "patrons_obs": po, "patrons_nul": pn,
                           "patrons_nul2": pn2, "lignes_obs": no, "lignes_nul": nn,
                           "exces": po - pn if np.isfinite(po) and np.isfinite(pn)
                           else np.nan,
                           "exces_nul_contre_nul": pn2 - pn
                           if np.isfinite(pn2) and np.isfinite(pn) else np.nan})

        # ---- Q3 -----------------------------------------------------------
        cols_tous = np.arange(sous.shape[1])
        for u in range(n_draws_q3):
            s = rl.choice(len(sous), size=n_egal, replace=False)
            do, npo = dimension_effective(rangs(sous[s]), cols_tous)
            dn, npn = dimension_effective(rangs(nuls[u % n_nuls][s]), cols_tous)
            dn2, _ = dimension_effective(rangs(nuls[(u + 1) % n_nuls][s]), cols_tous)
            q3.append({"jeu_de_donnees": etiquette, "camp": nom, "tirage": u,
                       "deff_obs": do, "deff_nul": dn, "deff_nul2": dn2,
                       "deff_norm": do / dn if np.isfinite(do) and dn else np.nan,
                       "deff_norm_nul_contre_nul": dn2 / dn
                       if np.isfinite(dn2) and dn else np.nan,
                       "paires_obs": npo, "paires_nul": npn})
        print(f"  [{etiquette}] {nom:8s} n_egal {n_egal:5d} "
              f"items {J:4d} replis de loi {replis}/{total}", flush=True)
    return pd.DataFrame(q2), pd.DataFrame(q3)


def contraste_q1(ind, mg, md, S, cols, rng, etiquette="", condition=""):
    """Contraste apparie item par item du residu de position, droite moins gauche."""
    Rg, gsg, temg, ng = q1_residus(ind, mg, S)
    Rd, gsd, temd, nd = q1_residus(ind, md, S)
    ok = np.zeros(ind.J, dtype=bool)
    ok[cols] = True
    ok &= np.isfinite(Rg) & np.isfinite(Rd) & (ng >= N_MIN_ITEM) & (nd >= N_MIN_ITEM)
    if ok.sum() < 3:
        return None, None
    d, lo, hi, p = apparie(Rd[ok], Rg[ok], N_BOOT, rng)
    ligne = {"jeu_de_donnees": etiquette, "condition": condition, "quantite": "Q1",
             "valeur_gauche": float(np.mean(Rg[ok])), "valeur_droite": float(np.mean(Rd[ok])),
             "contraste": d, "ic_bas": lo, "ic_haut": hi, "p": p,
             "n_unites": int(ok.sum()), "unite": "item"}
    detail = pd.DataFrame({"item_index": np.flatnonzero(ok),
                           "gs_gauche": gsg[ok], "temoin_gauche": temg[ok],
                           "residu_gauche": Rg[ok],
                           "gs_droite": gsd[ok], "temoin_droite": temd[ok],
                           "residu_droite": Rd[ok],
                           "n_gauche": ng[ok], "n_droite": nd[ok]})
    return ligne, detail


def contraste_apparie_long(df, colonne, camp_a, camp_b, cles, rng,
                           etiquette="", condition="", quantite=""):
    """Contraste apparie entre deux camps sur un tableau long, apparie sur cles."""
    a = df[df["camp"] == camp_a].set_index(cles)[colonne]
    b = df[df["camp"] == camp_b].set_index(cles)[colonne]
    j = pd.concat([a.rename("a"), b.rename("b")], axis=1).dropna()
    if len(j) < 5:
        return None
    d, lo, hi, p = apparie(j["a"].values, j["b"].values, N_BOOT, rng)
    return {"jeu_de_donnees": etiquette, "condition": condition, "quantite": quantite,
            "valeur_gauche": float(j["b"].mean()), "valeur_droite": float(j["a"].mean()),
            "contraste": d, "ic_bas": lo, "ic_haut": hi, "p": p,
            "n_unites": int(len(j)), "unite": "tirage"}


# ===========================================================================
# 2. GSS de Stanford
# ===========================================================================

def charger_gss():
    ids, items, y1, y2, x, attributs = charger()
    options = options_par_item(RACINE)
    codes1, ks = C.coder_gss(y1, items, options)
    codes2, _ = C.coder_gss(y2, items, options)
    camps = C.camps_gss(x, attributs)
    cellules = C.cellules_gss(x, attributs)
    S_ori, oriente, sens, niveaux, _ = A.scores_gss(items, options)
    # Items dont une modalite est « inapplicable » : la position n'a pas de sens.
    inapplicable = np.array([any(sans_score(o) for o in options[it]) for it in items])
    return dict(items=items, options=options, codes1=codes1, codes2=codes2, ks=ks,
                camps=camps, cellules=cellules, S_ori=S_ori, oriente=oriente,
                inapplicable=inapplicable, x=x, attributs=attributs)


def bloc_gss(g, args, rng, lignes, nuls_q2, nuls_q3, detail_q1, polarite, planchers,
             controles):
    items, ks = g["items"], g["ks"]
    J = len(items)
    kmax = int(ks.max())
    S_gen = scores_generiques_depuis_ks(ks, kmax)
    ind1 = C.Indicatrice(g["codes1"], ks)
    ind2 = C.Indicatrice(g["codes2"], ks)
    b3 = g["camps"]["bloc3"]
    mg, mc, md = b3 == "gauche", b3 == "centre", b3 == "droite"

    P1 = np.flatnonzero(g["oriente"] & ~g["inapplicable"])
    P0 = np.flatnonzero(~g["oriente"] & ~g["inapplicable"])
    P1_q1 = np.array([j for j in P1 if ks[j] > 2])
    P0_q1 = np.array([j for j in P0 if ks[j] > 2])
    print(f"GSS Stanford : {J} items, P1 {len(P1)} (Q1 {len(P1_q1)}), "
          f"P0 {len(P0)} (Q1 {len(P0_q1)}), inapplicables {int(g['inapplicable'].sum())}",
          flush=True)
    print(f"  camps bloc3 : gauche {mg.sum()}, centre {mc.sum()}, droite {md.sum()}",
          flush=True)

    n_egal_dc = int(min(mg.sum(), md.sum()))
    n_egal_3 = int(min(mg.sum(), mc.sum(), md.sum()))

    # ---------------------------------------------------------------- Q1, P1
    for nom_per, cols in (("P1", P1_q1), ("P0", P0_q1)):
        for vague, ind in (("vague1", ind1), ("vague2", ind2)):
            l, det = contraste_q1(ind, mg, md, S_gen, cols, rng,
                                  etiquette="GSS Stanford",
                                  condition=f"{nom_per} bloc3 {vague}")
            if l:
                lignes.append(l)
                if nom_per == "P1" and vague == "vague1":
                    det["item"] = [items[i] for i in det["item_index"]]
                    detail_q1.append(det)
        # centre, publie hors famille
        for cible, nom in ((mc, "centre moins gauche"), ):
            l, _ = contraste_q1(ind1, mg, cible, S_gen, cols, rng,
                                etiquette="GSS Stanford",
                                condition=f"{nom_per} {nom} vague1")
            if l:
                l["quantite"] = "Q1"
                lignes.append(l)

    # -------------------------------------------- Q1, controle de polarite
    D = A.derive(ind1.tables(C.poids_plein(np.ones(len(g["codes1"]), bool))),
                 g["S_ori"])[0]
    Rg, _, _, ng = q1_residus(ind1, mg, S_gen)
    Rd, _, _, nd = q1_residus(ind1, md, S_gen)
    ok = np.zeros(J, bool)
    ok[P1_q1] = True
    ok &= np.isfinite(Rg) & np.isfinite(Rd) & np.isfinite(D) & \
        (ng >= N_MIN_ITEM) & (nd >= N_MIN_ITEM)
    y = (Rd - Rg)[ok]
    d = D[ok]
    for nom, masque_sous in (("derive negative", d < 0), ("derive positive", d > 0)):
        if masque_sous.sum() >= 3:
            m, lo, hi, p = apparie(Rd[ok][masque_sous], Rg[ok][masque_sous], N_BOOT, rng)
            polarite.append({"jeu_de_donnees": "GSS Stanford", "sous_ensemble": nom,
                             "n_items": int(masque_sous.sum()), "contraste_q1": m,
                             "ic_bas": lo, "ic_haut": hi, "p": p,
                             "derive_moyenne": float(d[masque_sous].mean())})
    X = np.column_stack([np.ones(len(d)), d, np.abs(d)])
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ coef
    r2 = 1.0 - resid.var() / y.var() if y.var() > 0 else np.nan
    polarite.append({"jeu_de_donnees": "GSS Stanford",
                     "sous_ensemble": "regression sur derive et valeur absolue",
                     "n_items": int(len(d)), "contraste_q1": float(coef[0]),
                     "ic_bas": np.nan, "ic_haut": np.nan, "p": np.nan,
                     "derive_moyenne": float(d.mean()),
                     "pente_derive": float(coef[1]), "pente_abs_derive": float(coef[2]),
                     "r2": float(r2)})

    # ---------------------------------------------------------- Q2 et Q3, P1
    for nom_per, cols in (("P1", P1), ("P0", P0)):
        for vague, codes in (("vague1", g["codes1"]), ("vague2", g["codes2"])):
            if nom_per == "P0" and vague == "vague2":
                continue
            q2, q3 = q2_q3(codes, {"gauche": mg, "centre": mc, "droite": md},
                           cols, ks, rng, n_egal_3,
                           n_jeux=args.jeux, n_tirages=args.tirages,
                           n_nuls=args.nuls, n_draws_q3=args.draws,
                           etiquette=f"GSS Stanford {nom_per} {vague}")
            q2["condition"] = f"{nom_per} bloc3 {vague}"
            q3["condition"] = f"{nom_per} bloc3 {vague}"
            nuls_q2.append(q2)
            nuls_q3.append(q3)
            for a_camp, b_camp, nom in (("droite", "gauche", "bloc3"),
                                        ("centre", "gauche", "centre moins gauche")):
                l = contraste_apparie_long(q2, "exces", a_camp, b_camp,
                                           ["sous_ensemble", "tirage"], rng,
                                           "GSS Stanford", f"{nom_per} {nom} {vague}", "Q2")
                if l:
                    lignes.append(l)
                l = contraste_apparie_long(q3, "deff_norm", a_camp, b_camp,
                                           ["tirage"], rng,
                                           "GSS Stanford", f"{nom_per} {nom} {vague}", "Q3")
                if l:
                    lignes.append(l)

    # ------------------------------------------------- controles bloquants
    # 3. appariement demographique exact
    wa, wb, taille = C.poids_appariement(md, mg, g["cellules"], 1, rng)
    ma = wa[0] > 0
    mb = wb[0] > 0
    l, _ = contraste_q1(ind1, mb, ma, S_gen, P1_q1, rng, "GSS Stanford",
                        "P1 appariement demographique")
    if l:
        lignes.append(l)
        controles.append({"controle": "appariement demographique exact",
                          "taille_appariee": int(taille), **l})
    q2a, q3a = q2_q3(g["codes1"], {"gauche": mb, "droite": ma}, P1, ks, rng,
                     int(min(ma.sum(), mb.sum())), n_jeux=max(args.jeux // 2, 20),
                     n_tirages=args.tirages, n_nuls=args.nuls,
                     n_draws_q3=max(args.draws // 2, 20),
                     etiquette="GSS Stanford P1 apparie")
    for df_, col, q in ((q2a, "exces", "Q2"), (q3a, "deff_norm", "Q3")):
        cles = ["sous_ensemble", "tirage"] if q == "Q2" else ["tirage"]
        l = contraste_apparie_long(df_, col, "droite", "gauche", cles, rng,
                                   "GSS Stanford", "P1 appariement demographique", q)
        if l:
            lignes.append(l)
            controles.append({"controle": "appariement demographique exact",
                              "taille_appariee": int(taille), **l})

    # 4. ancrage partisan
    p3 = g["camps"]["parti3"]
    mgp, mdp = p3 == "gauche", p3 == "droite"
    l, _ = contraste_q1(ind1, mgp, mdp, S_gen, P1_q1, rng, "GSS Stanford",
                        "P1 ancrage partisan")
    if l:
        lignes.append(l)
        controles.append({"controle": "ancrage partisan partyid",
                          "taille_appariee": np.nan, **l})
    n_p = int(min(mgp.sum(), mdp.sum()))
    q2p, q3p = q2_q3(g["codes1"], {"gauche": mgp, "droite": mdp}, P1, ks, rng, n_p,
                     n_jeux=max(args.jeux // 2, 20), n_tirages=args.tirages,
                     n_nuls=args.nuls, n_draws_q3=max(args.draws // 2, 20),
                     etiquette="GSS Stanford P1 partyid")
    for df_, col, q in ((q2p, "exces", "Q2"), (q3p, "deff_norm", "Q3")):
        cles = ["sous_ensemble", "tirage"] if q == "Q2" else ["tirage"]
        l = contraste_apparie_long(df_, col, "droite", "gauche", cles, rng,
                                   "GSS Stanford", "P1 ancrage partisan", q)
        if l:
            lignes.append(l)
            controles.append({"controle": "ancrage partisan partyid",
                              "taille_appariee": np.nan, **l})

    # 2. sensibilite a n_egal, trois valeurs
    for frac in (0.5, 0.75, 1.0):
        n_e = max(int(n_egal_dc * frac), 60)
        q2s, q3s = q2_q3(g["codes1"], {"gauche": mg, "droite": md}, P1, ks, rng, n_e,
                         n_jeux=max(args.jeux // 4, 20), n_tirages=args.tirages,
                         n_nuls=args.nuls, n_draws_q3=max(args.draws // 4, 20),
                         etiquette=f"GSS Stanford P1 n{n_e}")
        for df_, col, q in ((q2s, "exces", "Q2"), (q3s, "deff_norm", "Q3")):
            cles = ["sous_ensemble", "tirage"] if q == "Q2" else ["tirage"]
            l = contraste_apparie_long(df_, col, "droite", "gauche", cles, rng,
                                       "GSS Stanford", f"P1 n_egal {n_e}", q)
            if l:
                lignes.append(l)
                controles.append({"controle": f"sensibilite n_egal {n_e}",
                                  "taille_appariee": n_e, **l})
    return n_egal_3, n_egal_dc


# ===========================================================================
# 3. Twin-2K-500
# ===========================================================================

def bloc_twin(args, rng, lignes, nuls_q2, nuls_q3, planchers):
    import a9_commun as T
    items = T.table_items()
    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    cols_tous = [c for c in items.index
                 if c in w13.columns and items.at[c, "domaine"] != "demographies"]
    camps = C.camps_twin(w13)
    codes, ks = C.coder_numerique(w13, cols_tous)
    ks = np.asarray(ks)
    kmax = int(ks.max())
    S_gen = scores_generiques_depuis_ks(ks, kmax)
    ind = C.Indicatrice(codes, ks)
    dom = np.array([items.at[c, "domaine"] for c in cols_tous], dtype=object)
    P1 = np.flatnonzero(dom == "attitudes")
    P0 = np.flatnonzero(dom == "personnalite")
    P1_q1 = np.array([j for j in P1 if ks[j] > 2])
    P0_q1 = np.array([j for j in P0 if ks[j] > 2])
    b3 = camps["bloc3"]
    mg, mc, md = b3 == "gauche", b3 == "centre", b3 == "droite"
    n_egal = int(min(mg.sum(), mc.sum(), md.sum()))
    print(f"Twin : {len(cols_tous)} items, P1 attitudes {len(P1)} (Q1 {len(P1_q1)}), "
          f"P0 personnalite {len(P0)} (Q1 {len(P0_q1)}), n_egal {n_egal}", flush=True)

    for nom_per, cq1, cq in (("P1", P1_q1, P1), ("P0", P0_q1, P0)):
        l, _ = contraste_q1(ind, mg, md, S_gen, cq1, rng, "Twin-2K-500",
                            f"{nom_per} bloc3 vagues 1-3")
        if l:
            lignes.append(l)
        q2, q3 = q2_q3(codes, {"gauche": mg, "centre": mc, "droite": md}, cq, ks, rng,
                       n_egal, n_jeux=max(args.jeux // 2, 20), n_tirages=args.tirages,
                       n_nuls=args.nuls, n_draws_q3=max(args.draws // 2, 20),
                       etiquette=f"Twin {nom_per}")
        q2["condition"] = f"{nom_per} bloc3 vagues 1-3"
        q3["condition"] = f"{nom_per} bloc3 vagues 1-3"
        nuls_q2.append(q2)
        nuls_q3.append(q3)
        for q_, col, nom in ((q2, "exces", "Q2"), (q3, "deff_norm", "Q3")):
            cles = ["sous_ensemble", "tirage"] if nom == "Q2" else ["tirage"]
            l = contraste_apparie_long(q_, col, "droite", "gauche", cles, rng,
                                       "Twin-2K-500", f"{nom_per} bloc3 vagues 1-3", nom)
            if l:
                lignes.append(l)

    # plancher de bruit : les 108 items reposes en vague 4
    cols4 = [c for c in cols_tous if c in w4.columns]
    if len(cols4) >= 20:
        idx4 = [cols_tous.index(c) for c in cols4]
        (c13, c4), ks4 = C.coder_numerique_commun([w13[cols4], w4[cols4]], cols4)
        ks4 = np.asarray(ks4)
        S4 = scores_generiques_depuis_ks(ks4, int(ks4.max()))
        ind13 = C.Indicatrice(c13, ks4)
        ind4 = C.Indicatrice(c4, ks4)
        cols_q1 = np.array([j for j in range(len(cols4)) if ks4[j] > 2])
        for nom, ind_ in (("vagues 1-3", ind13), ("vague 4", ind4)):
            l, _ = contraste_q1(ind_, mg, md, S4, cols_q1, rng, "Twin-2K-500",
                                f"plancher items reposes {nom}")
            if l:
                lignes.append(l)
                planchers.append({"jeu_de_donnees": "Twin-2K-500", "quantite": "Q1",
                                  "condition": nom, "contraste": l["contraste"],
                                  "ic_bas": l["ic_bas"], "ic_haut": l["ic_haut"]})


# ===========================================================================
# 4. Panels NORC
# ===========================================================================

def bloc_panels(args, rng, lignes, nuls_q2, nuls_q3, planchers):
    import i1_commun as I
    noyau, brut, n_paires = I.charger_panels()
    ori = A.ORIENTATION
    est_ori = np.array([it in ori for it in noyau])
    print(f"Panels NORC : noyau {len(noyau)} items, dont orientes {int(est_ori.sum())}",
          flush=True)
    par_panel = []
    for nom_panel, cfg in (("2006-2010", 2006), ("2008-2012", 2008),
                           ("2010-2014", 2010), ("2016-2020", 2016)):
        mat = brut[nom_panel]["mat"][cfg]
        demos = I.charger_demos(nom_panel, cfg)
        bloc = np.array([I.bloc_ideologie(v) for v in demos["polviews"]], dtype=object)
        # codage ordinal propre : les modalites du GSS sont des entiers ordonnes.
        n, m = mat.shape
        codes = np.full((n, m), -1, dtype=np.int32)
        ks = np.ones(m, dtype=int)
        for j in range(m):
            col = mat[:, j]
            vals = np.array([v for v in col
                             if not (isinstance(v, float) and v != v) and v is not None],
                            dtype=float) if n else np.array([])
            if len(vals) == 0:
                continue
            mods = np.unique(vals)
            table = {v: i for i, v in enumerate(mods)}
            ks[j] = len(mods)
            for i in range(n):
                v = col[i]
                if v is None or (isinstance(v, float) and v != v):
                    continue
                codes[i, j] = table[float(v)]
        kmax = int(ks.max())
        S_gen = scores_generiques_depuis_ks(ks, kmax)
        ind = C.Indicatrice(codes, ks)
        mg, mc, md = bloc == "gauche", bloc == "centre", bloc == "droite"
        P1 = np.flatnonzero(est_ori)
        P0 = np.flatnonzero(~est_ori)
        P1_q1 = np.array([j for j in P1 if ks[j] > 2])
        P0_q1 = np.array([j for j in P0 if ks[j] > 2])
        n_egal = int(min(mg.sum(), mc.sum(), md.sum()))
        print(f"  {nom_panel} vague {cfg} : gauche {mg.sum()}, centre {mc.sum()}, "
              f"droite {md.sum()}, n_egal {n_egal}, P1 {len(P1)} (Q1 {len(P1_q1)})",
              flush=True)
        for nom_per, cq1, cq in (("P1", P1_q1, P1), ("P0", P0_q1, P0)):
            l, _ = contraste_q1(ind, mg, md, S_gen, cq1, rng, f"panel {nom_panel}",
                                f"{nom_per} bloc3 {cfg}")
            if l:
                lignes.append(l)
                par_panel.append(l)
            q2, q3 = q2_q3(codes, {"gauche": mg, "centre": mc, "droite": md}, cq, ks,
                           rng, n_egal, n_jeux=max(args.jeux // 4, 20),
                           n_tirages=max(args.tirages // 2, 5), n_nuls=args.nuls,
                           n_draws_q3=max(args.draws // 4, 20),
                           etiquette=f"panel {nom_panel} {nom_per}")
            q2["condition"] = f"{nom_per} bloc3 {cfg}"
            q3["condition"] = f"{nom_per} bloc3 {cfg}"
            nuls_q2.append(q2)
            nuls_q3.append(q3)
            for q_, col, nomq in ((q2, "exces", "Q2"), (q3, "deff_norm", "Q3")):
                cles = ["sous_ensemble", "tirage"] if nomq == "Q2" else ["tirage"]
                l = contraste_apparie_long(q_, col, "droite", "gauche", cles, rng,
                                           f"panel {nom_panel}",
                                           f"{nom_per} bloc3 {cfg}", nomq)
                if l:
                    lignes.append(l)
                    par_panel.append(l)

        # plancher : la meme mesure a la vague suivante, memes personnes
        annees = sorted(brut[nom_panel]["mat"].keys())
        if len(annees) >= 2:
            mat2 = brut[nom_panel]["mat"][annees[-1]]
            codes2 = np.full((n, m), -1, dtype=np.int32)
            for j in range(m):
                col = mat2[:, j]
                vals = np.array([v for v in col
                                 if not (isinstance(v, float) and v != v) and v is not None],
                                dtype=float)
                if len(vals) == 0:
                    continue
                mods = np.unique(vals)
                table = {v: i for i, v in enumerate(mods)}
                if len(mods) != ks[j]:
                    continue
                for i in range(n):
                    v = col[i]
                    if v is None or (isinstance(v, float) and v != v):
                        continue
                    codes2[i, j] = table[float(v)]
            ind2 = C.Indicatrice(codes2, ks)
            l, _ = contraste_q1(ind2, mg, md, S_gen, P1_q1, rng, f"panel {nom_panel}",
                                f"P1 plancher {annees[-1]}")
            if l:
                lignes.append(l)
                planchers.append({"jeu_de_donnees": f"panel {nom_panel}", "quantite": "Q1",
                                  "condition": f"vague {annees[-1]} contre {cfg}",
                                  "contraste": l["contraste"], "ic_bas": l["ic_bas"],
                                  "ic_haut": l["ic_haut"]})
    return par_panel


# ===========================================================================
# 5. Verdicts
# ===========================================================================

def verdicts(df, planchers_df):
    """Applique mot pour mot les criteres de la section 7 du preenregistrement."""
    out = []
    fam = df[(df["jeu_de_donnees"] == "GSS Stanford") &
             (df["condition"] == "P1 bloc3 vague1")].copy()
    fam = fam.set_index("quantite").reindex(["Q1", "Q2", "Q3"]).dropna(subset=["p"])
    if len(fam):
        fam["p_holm"] = C.holm(fam["p"].values)
    plancher = {}
    for q in ("Q1", "Q2", "Q3"):
        v1 = df[(df["jeu_de_donnees"] == "GSS Stanford") &
                (df["condition"] == "P1 bloc3 vague1") & (df["quantite"] == q)]
        v2 = df[(df["jeu_de_donnees"] == "GSS Stanford") &
                (df["condition"] == "P1 bloc3 vague2") & (df["quantite"] == q)]
        if len(v1) and len(v2):
            plancher[q] = abs(float(v1["contraste"].iloc[0]) -
                              float(v2["contraste"].iloc[0]))
    for q in ("Q1", "Q2", "Q3"):
        if q not in fam.index:
            continue
        r = fam.loc[q]
        signe_ok = bool(r["contraste"] > 0)
        ic_ok = bool(r["ic_bas"] > 0 or r["ic_haut"] < 0)
        holm_ok = bool(r["p_holm"] < 0.05)
        pl = plancher.get(q, np.nan)
        pl_ok = bool(np.isfinite(pl) and abs(r["contraste"]) > pl)
        p0 = df[(df["jeu_de_donnees"] == "GSS Stanford") &
                (df["condition"] == "P0 bloc3 vague1") & (df["quantite"] == q)]
        p0v = float(p0["contraste"].iloc[0]) if len(p0) else np.nan
        p0_ok = bool(not np.isfinite(p0v) or
                     abs(p0v) < 0.5 * abs(float(r["contraste"])))
        rep = df[(df["jeu_de_donnees"] != "GSS Stanford") & (df["quantite"] == q) &
                 (df["condition"].str.startswith("P1 bloc3"))]
        rep_ok = bool(len(rep) and
                      ((rep["contraste"] > 0) & (rep["ic_bas"] > 0)).any())
        # Refutation numero 3 : signe inverse avec intervalles disjoints.
        inverse = bool(len(rep) and
                       ((rep["contraste"] < 0) & (rep["ic_haut"] < 0) &
                        (float(r["ic_bas"]) > 0)).any())
        out.append({"quantite": q, "contraste": float(r["contraste"]),
                    "ic_bas": float(r["ic_bas"]), "ic_haut": float(r["ic_haut"]),
                    "p": float(r["p"]), "p_holm": float(r["p_holm"]),
                    "plancher_vague2": pl, "contraste_P0": p0v,
                    "n_replications_meme_signe":
                        int(((rep["contraste"] > 0) & (rep["ic_bas"] > 0)).sum()),
                    "n_replications_signe_inverse":
                        int(((rep["contraste"] < 0) & (rep["ic_haut"] < 0)).sum()),
                    "c1_signe_et_holm": signe_ok and ic_ok and holm_ok,
                    "c2_au_dessus_du_plancher": pl_ok,
                    "c3_replication_meme_signe": rep_ok,
                    "c4_P0_ne_reproduit_pas": p0_ok,
                    "refutation_3_inversion": inverse,
                    "les_quatre": signe_ok and ic_ok and holm_ok and pl_ok and rep_ok
                    and p0_ok})
    return pd.DataFrame(out)


# ===========================================================================
# 6. Main
# ===========================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--jeux", type=int, default=N_JEUX)
    ap.add_argument("--tirages", type=int, default=N_TIRAGES)
    ap.add_argument("--nuls", type=int, default=N_NULS)
    ap.add_argument("--draws", type=int, default=N_DRAWS_Q3)
    ap.add_argument("--rapide", action="store_true")
    ap.add_argument("--sans-panels", action="store_true", dest="sans_panels")
    args = ap.parse_args()
    if args.rapide:
        args.jeux, args.tirages, args.nuls, args.draws = 20, 4, 10, 20
    rng = np.random.default_rng(GRAINE)

    lignes, nuls_q2, nuls_q3, detail_q1 = [], [], [], []
    polarite, planchers, controles = [], [], []

    g = charger_gss()
    bloc_gss(g, args, rng, lignes, nuls_q2, nuls_q3, detail_q1, polarite, planchers,
             controles)
    bloc_twin(args, rng, lignes, nuls_q2, nuls_q3, planchers)
    if not args.sans_panels:
        bloc_panels(args, rng, lignes, nuls_q2, nuls_q3, planchers)

    df = pd.DataFrame(lignes)
    # Holm dans chaque famille, jamais entre familles.
    df["p_holm"] = np.nan
    for (jeu, cond), sous in df.groupby(["jeu_de_donnees", "condition"]):
        if len(sous) and sous["p"].notna().all():
            df.loc[sous.index, "p_holm"] = C.holm(sous["p"].values)
    C.ecrire(df, "d4-contrastes.csv")

    q2all = pd.concat(nuls_q2, ignore_index=True)
    q3all = pd.concat(nuls_q3, ignore_index=True)
    res_nul = []
    for (jeu, cond, camp), s in q2all.groupby(["jeu_de_donnees", "condition", "camp"]):
        res_nul.append({"jeu_de_donnees": jeu, "condition": cond, "camp": camp,
                        "quantite": "Q2", "observe": s["patrons_obs"].mean(),
                        "nul": s["patrons_nul"].mean(), "exces": s["exces"].mean(),
                        "exces_nul_contre_nul": s["exces_nul_contre_nul"].mean(),
                        "ecart_type_nul_contre_nul": s["exces_nul_contre_nul"].std(),
                        "n_tirages": len(s)})
    for (jeu, cond, camp), s in q3all.groupby(["jeu_de_donnees", "condition", "camp"]):
        res_nul.append({"jeu_de_donnees": jeu, "condition": cond, "camp": camp,
                        "quantite": "Q3", "observe": s["deff_obs"].mean(),
                        "nul": s["deff_nul"].mean(), "exces": s["deff_norm"].mean(),
                        "exces_nul_contre_nul": s["deff_norm_nul_contre_nul"].mean(),
                        "ecart_type_nul_contre_nul":
                            s["deff_norm_nul_contre_nul"].std(),
                        "n_tirages": len(s)})
    C.ecrire(pd.DataFrame(res_nul), "d4-nuls.csv")

    if detail_q1:
        C.ecrire(pd.concat(detail_q1, ignore_index=True), "d4-q1-par-item.csv")
    C.ecrire(pd.DataFrame(polarite), "d4-polarite.csv")
    C.ecrire(pd.DataFrame(planchers), "d4-planchers.csv")
    C.ecrire(pd.DataFrame(controles), "d4-controles.csv")
    C.ecrire(verdicts(df, pd.DataFrame(planchers)), "d4-verdicts.csv")

    print("\n--- contrastes principaux, GSS Stanford, P1 vague 1 ---", flush=True)
    p = df[(df["jeu_de_donnees"] == "GSS Stanford") &
           (df["condition"] == "P1 bloc3 vague1")]
    print(p[["quantite", "valeur_gauche", "valeur_droite", "contraste",
             "ic_bas", "ic_haut", "p", "p_holm"]].to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
