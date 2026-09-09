"""
t2_agrege : volet 1 de T2. La part de personnes qui changent par item et par groupe,
et sa previsibilite contre le nul a derive.

Preenregistrement : resultats/t2-preenregistrement.md, sections 2 et 3.

Dispositif : cinq coupures 50 / 50 des personnes, stratifiees par panel. Les six modeles
sont ajustes sur la moitie A, la cible est observee sur la moitie B. Rien ne traverse.

Sorties : t2-controles.csv, t2-groupes.csv, t2-modeles.csv, t2-contrastes.csv,
t2-variance-inter-groupes.csv, t2-erreur-par-item.csv, t2-par-groupe-item.csv.
Aucune microdonnee.

Usage : .venv/bin/python analyses/t2_agrege.py
"""

import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t2_commun as T2
import i1_commun as I1

MODELES = ["M0", "M1", "M2", "M3", "M4", "M5"]
LIBELLES = {
    "M0": "nul a derive (item seul)",
    "M1": "segment (groupe seul)",
    "M2": "additif item + groupe",
    "M3": "P agrege (vague 1, transitions)",
    "M4": "P agrege + decalage de groupe",
    "M5": "oracle empirique de cellule",
}
CIBLES = [("tau", "taux de changement, points"),
          ("pi", "deplacement projete sur la derive, points"),
          ("mu", "deplacement ordinal, points d'echelle")]


def _corr(a, b):
    """Correlation de Pearson entre deux tableaux de cellules, NaN ignores.

    Sur les cellules (groupe, item), a est l'ecart du groupe a la moyenne d'item dans la
    moitie A et b le meme ecart dans la moitie B. Sous un decoupage sans contenu elle
    vaut zero en esperance : c'est la mesure directe de « les groupes different ils de
    facon reproductible ».
    """
    a = np.asarray(a, dtype=float).ravel()
    b = np.asarray(b, dtype=float).ravel()
    m = np.isfinite(a) & np.isfinite(b)
    if m.sum() < 10:
        return np.nan
    a, b = a[m] - a[m].mean(), b[m] - b[m].mean()
    d = np.sqrt((a ** 2).sum() * (b ** 2).sum())
    return float((a * b).sum() / d) if d > 0 else np.nan


def _moy(masque, X, OK):
    """Moyenne par item sur les personnes du masque. Retourne (moyenne, effectif)."""
    w = masque.astype(np.float32)
    num = w @ np.nan_to_num(X, nan=0.0).astype(np.float32)
    den = w @ OK
    return np.where(den > 0, num / np.maximum(den, 1e-9), np.nan), den


def calculer():
    t0 = time.time()
    paquet = T2.charger("4ans")
    items = paquet["items"]
    P = len(items)
    est_ord = T2.items_ordinaux(items)
    garde_ord, V = T2.valeurs_ordinales(paquet, est_ord)
    grp, ax = T2.groupes(paquet)
    OK = paquet["ok"].astype(np.float32)
    OKO = (paquet["ok"] & garde_ord[None, :]).astype(np.float32)
    rng = np.random.default_rng(T2.GRAINE)

    cons, n_noyau = T2.controle_consistance()
    controles = [
        {"controle": "consistance a deux ans, noyau commun, valeur de a12",
         "attendu": 0.695267, "obtenu": round(cons[2], 6),
         "passe": round(cons[2], 6) == 0.695267},
        {"controle": "consistance a quatre ans, noyau commun, valeur de a12",
         "attendu": 0.674471, "obtenu": round(cons[4], 6),
         "passe": round(cons[4], 6) == 0.674471},
        {"controle": "nombre d'items du noyau commun", "attendu": 118, "obtenu": P,
         "passe": P == 118},
        {"controle": "personnes, perimetre a quatre ans", "attendu": 4683,
         "obtenu": paquet["n"], "passe": paquet["n"] == 4683},
        {"controle": "items marques ordinaux par le question_master", "attendu": "",
         "obtenu": int(est_ord.sum()), "passe": True},
        {"controle": "items ordinaux retenus (codes numeriques distincts)", "attendu": "",
         "obtenu": int(garde_ord.sum()), "passe": True},
        {"controle": "groupes retenus au seuil de 200 personnes", "attendu": "",
         "obtenu": len(grp), "passe": True},
    ]

    # tableau descriptif des groupes
    T2.ecrire([{"axe": g["axe"], "groupe": g["groupe"], "n_personnes": g["n"],
                "part_du_perimetre": g["n"] / paquet["n"]} for g in grp], "t2-groupes.csv")

    # accumulateurs
    acc_err = {c: {m: [] for m in MODELES} for c, _ in CIBLES}      # erreurs par cellule
    acc_boot = {c: {m: [] for m in MODELES} for c, _ in CIBLES}     # MAE bootstrap
    acc_r2 = {c: {m: [] for m in MODELES} for c, _ in CIBLES}
    acc_r2_axe = []
    acc_plafond = []
    acc_perm = []
    err_item = {c: {m: np.zeros((P, 2)) for m in MODELES} for c, _ in CIBLES}
    lignes_cellules = []
    coupures_ok = True
    min_cell = []

    for rep in range(T2.N_REPETITIONS):
        A = T2.coupure(paquet, rep)
        B = ~A
        if (A & B).any() or A.sum() + B.sum() != paquet["n"]:
            coupures_ok = False
        tr = T2.transitions(paquet, A, V, garde_ord)
        # valeurs par personne et par item, dans l'ordre des cibles
        obs = {"tau": tr["chg"], "pi": tr["proj_obs"], "mu": tr["ord_obs"]}
        pred = {"tau": tr["pchg"], "pi": tr["proj_pred"], "mu": tr["ord_pred"]}
        masques = {"tau": OK, "pi": OK, "mu": OKO}
        ech = {"tau": 100.0, "pi": 100.0, "mu": 1.0}

        # --- cote A : les agregats qui servent aux modeles ---------------------
        glob_A = {}
        for c, _ in CIBLES:
            glob_A[c] = _moy(A, obs[c], masques[c])[0] * ech[c]
        cell_A, nA, m3_A = {}, {}, {}
        for c, _ in CIBLES:
            cell_A[c] = np.full((len(grp), P), np.nan)
            m3_A[c] = np.full((len(grp), P), np.nan)
        for gi, g in enumerate(grp):
            ma = g["masque"] & A
            for c, _ in CIBLES:
                v, d = _moy(ma, obs[c], masques[c])
                cell_A[c][gi] = v * ech[c]
                if c == "tau":
                    nA[gi] = d
                m3_A[c][gi] = _moy(ma, pred[c], masques[c])[0] * ech[c]

        # --- cote B : cibles et predictions, avec bootstrap sur les personnes ---
        idxB = np.flatnonzero(B)
        W = T2.poids_bootstrap(len(idxB), T2.N_BOOTSTRAP, rng)   # (nb+1, nB)
        Xobs = {c: np.nan_to_num(obs[c][idxB], nan=0.0).astype(np.float32) for c, _ in CIBLES}
        Xpred = {c: np.nan_to_num(pred[c][idxB], nan=0.0).astype(np.float32) for c, _ in CIBLES}
        Mk = {c: masques[c][idxB] for c, _ in CIBLES}

        cible_B = {c: np.full((T2.N_BOOTSTRAP + 1, len(grp), P), np.nan, dtype=np.float32)
                   for c, _ in CIBLES}
        m3_B = {c: np.full((T2.N_BOOTSTRAP + 1, len(grp), P), np.nan, dtype=np.float32)
                for c, _ in CIBLES}
        nB = np.zeros((len(grp), P))
        for gi, g in enumerate(grp):
            mg = g["masque"][idxB].astype(np.float32)
            Wg = W * mg[None, :]
            for c, _ in CIBLES:
                den = Wg @ Mk[c]
                cible_B[c][:, gi, :] = np.where(den > 0, (Wg @ Xobs[c]) / np.maximum(den, 1e-9),
                                                np.nan) * ech[c]
                m3_B[c][:, gi, :] = np.where(den > 0, (Wg @ Xpred[c]) / np.maximum(den, 1e-9),
                                             np.nan) * ech[c]
                if c == "tau":
                    nB[gi] = den[0]

        # --- retention des cellules -------------------------------------------
        garde = np.zeros((len(grp), P), dtype=bool)
        for gi in range(len(grp)):
            garde[gi] = (nA[gi] >= T2.MIN_CELLULE) & (nB[gi] >= T2.MIN_CELLULE)
        min_cell.append(float(min(nA[gi][garde[gi]].min() if garde[gi].any() else np.inf
                                  for gi in range(len(grp)))))

        # --- les six modeles ---------------------------------------------------
        for c, _ in CIBLES:
            gardec = garde & np.isfinite(cible_B[c][0]) & np.isfinite(cell_A[c])
            if c == "mu":
                gardec = gardec & garde_ord[None, :]
            gj = np.flatnonzero(gardec.any(axis=0))
            # moyennes par groupe et globale sur A, en moyenne d'items
            moy_item_glob = np.nanmean(glob_A[c][gj])
            moy_item_grp = np.array([np.nanmean(cell_A[c][gi][gardec[gi]])
                                     if gardec[gi].any() else np.nan
                                     for gi in range(len(grp))])
            dec_M4 = np.array([np.nanmean((cell_A[c][gi] - m3_A[c][gi])[gardec[gi]])
                               if gardec[gi].any() else 0.0 for gi in range(len(grp))])
            pr = {}
            pr["M0"] = np.tile(glob_A[c], (len(grp), 1))
            pr["M1"] = np.tile(moy_item_grp[:, None], (1, P))
            pr["M2"] = pr["M0"] + (moy_item_grp - moy_item_glob)[:, None]
            pr["M3"] = m3_B[c][0]
            pr["M4"] = pr["M3"] + dec_M4[:, None]
            pr["M5"] = cell_A[c]
            # predictions bootstrap : seuls M3 et M4 dependent des personnes de B
            prb = {m: (np.broadcast_to(pr[m], (T2.N_BOOTSTRAP + 1, len(grp), P))
                       if m not in ("M3", "M4")
                       else (m3_B[c] if m == "M3"
                             else m3_B[c] + dec_M4[None, :, None]))
                   for m in MODELES}
            y = cible_B[c]
            sel = gardec
            for m in MODELES:
                e = np.abs(prb[m] - y)
                mae = np.array([np.nanmean(e[b][sel]) for b in range(T2.N_BOOTSTRAP + 1)])
                acc_boot[c][m].append(mae)
                acc_err[c][m].append(float(mae[0]))
                # R2 relatif au nul, par tirage
                sse = np.array([np.nansum(((prb[m][b] - y[b]) ** 2)[sel])
                                for b in range(T2.N_BOOTSTRAP + 1)])
                sse0 = np.array([np.nansum(((prb["M0"][b] - y[b]) ** 2)[sel])
                                 for b in range(T2.N_BOOTSTRAP + 1)])
                acc_r2[c][m].append(1.0 - sse / np.maximum(sse0, 1e-12))
                # erreur par item
                ei = np.where(sel, np.abs(pr[m] - y[0]), np.nan)
                with np.errstate(invalid="ignore"):
                    err_item[c][m][:, 0] += np.nan_to_num(np.nanmean(ei, axis=0), nan=0.0)
                    err_item[c][m][:, 1] += np.isfinite(ei).any(axis=0).astype(float)
            # R2 par axe
            for a in sorted({g["axe"] for g in grp}):
                ga = np.array([g["axe"] == a for g in grp])
                s = sel & ga[:, None]
                if s.sum() < 20:
                    continue
                for m in MODELES:
                    sse = np.nansum(((pr[m] - y[0]) ** 2)[s])
                    sse0 = np.nansum(((pr["M0"] - y[0]) ** 2)[s])
                    acc_r2_axe.append({"repetition": rep, "cible": c, "axe": a,
                                       "modele": m, "n_cellules": int(s.sum()),
                                       "r2": 1.0 - sse / max(sse0, 1e-12)})
            # --- le plafond de fidelite : quelle part de la variance inter groupes
            # observee sur B est du signal et non du bruit d'echantillonnage.
            # Les deux moities ont le meme effectif, donc le bruit de la cellule y est
            # de meme variance ; E[(devA - devB)^2] = 2 sigma^2 sous l'hypothese que la
            # vraie valeur de la cellule est la meme des deux cotes.
            globB = np.nanmean(np.where(sel, y[0], np.nan), axis=0)
            devA = np.where(sel, pr["M5"] - glob_A[c][None, :], np.nan)
            devB = np.where(sel, y[0] - globB[None, :], np.nan)
            sigma2 = 0.5 * np.nanmean((devA - devB) ** 2)
            denom = np.nanmean((pr["M0"] - y[0])[sel] ** 2)
            acc_plafond.append({"repetition": rep, "cible": c, "axe": "tous",
                                "n_cellules": int(sel.sum()),
                                "variance_totale_inter_groupes": float(denom),
                                "variance_de_bruit": float(sigma2),
                                "r2_plafond": float(1.0 - sigma2 / max(denom, 1e-12)),
                                "part_de_bruit": float(sigma2 / max(denom, 1e-12)),
                                "correlation_moities": _corr(devA, devB)})
            for a in sorted({g["axe"] for g in grp}):
                ga = np.array([g["axe"] == a for g in grp])
                s = sel & ga[:, None]
                if s.sum() < 20:
                    continue
                dA = np.where(s, pr["M5"] - glob_A[c][None, :], np.nan)
                dB = np.where(s, y[0] - globB[None, :], np.nan)
                s2 = 0.5 * np.nanmean((dA - dB) ** 2)
                dn = np.nanmean((pr["M0"] - y[0])[s] ** 2)
                acc_plafond.append({"repetition": rep, "cible": c, "axe": a,
                                    "n_cellules": int(s.sum()),
                                    "variance_totale_inter_groupes": float(dn),
                                    "variance_de_bruit": float(s2),
                                    "r2_plafond": float(1.0 - s2 / max(dn, 1e-12)),
                                    "part_de_bruit": float(s2 / max(dn, 1e-12)),
                                    "correlation_moities": _corr(dA, dB)})

            # tableau descriptif des cellules, repetition 0 seulement
            if rep == 0:
                for gi in range(len(grp)):
                    for j in np.flatnonzero(sel[gi]):
                        lignes_cellules.append({
                            "cible": c, "axe": grp[gi]["axe"], "groupe": grp[gi]["groupe"],
                            "item": items[j], "n_A": int(nA[gi][j]), "n_B": int(nB[gi][j]),
                            "observe_B": float(y[0, gi, j]), "observe_A": float(cell_A[c][gi, j]),
                            "M0": float(pr["M0"][gi, j]), "M3": float(pr["M3"][gi, j]),
                            "M5": float(pr["M5"][gi, j])})
        # --- bande de permutation de l'etiquette de groupe ---------------------
        # Les etiquettes d'un axe sont permutees entre les personnes du meme panel.
        # Le decoupage garde ses effectifs et perd son contenu ; ce que M5 obtient
        # alors est ce qu'un groupement sans contenu produit.
        rngp = np.random.default_rng(T2.GRAINE + 7 * rep)
        blocs_panel = [np.flatnonzero(paquet["panel"] == p) for p in np.unique(paquet["panel"])]
        for c in ("tau", "pi", "mu"):
            for a in T2.AXES_SIMPLES:
                lab = ax[a]
                niveaux = [g for g in sorted(set(lab)) if (lab == g).sum() >= T2.MIN_GROUPE]
                if len(niveaux) < 2:
                    continue
                for perm in range(T2.N_PERMUTATIONS):
                    lp = lab.copy()
                    for bl in blocs_panel:
                        lp[bl] = lab[bl][rngp.permutation(len(bl))]
                    cA, cB, kA, kB = [], [], [], []
                    for g in niveaux:
                        m = lp == g
                        v, d = _moy(m & A, obs[c], masques[c])
                        cA.append(v * ech[c])
                        kA.append(d)
                        v, d = _moy(m & B, obs[c], masques[c])
                        cB.append(v * ech[c])
                        kB.append(d)
                    cA, cB = np.array(cA), np.array(cB)
                    s = (np.array(kA) >= T2.MIN_CELLULE) & (np.array(kB) >= T2.MIN_CELLULE)
                    s = s & np.isfinite(cA) & np.isfinite(cB)
                    if s.sum() < 20:
                        continue
                    g0 = np.tile(glob_A[c], (len(niveaux), 1))
                    sse0 = np.nansum(((g0 - cB) ** 2)[s])
                    gB = np.nanmean(np.where(s, cB, np.nan), axis=0)
                    dA = np.where(s, cA - glob_A[c][None, :], np.nan)
                    dB = np.where(s, cB - gB[None, :], np.nan)
                    acc_perm.append({
                        "repetition": rep, "cible": c, "axe": a, "permutation": perm,
                        "r2_M5": 1.0 - np.nansum(((cA - cB) ** 2)[s]) / max(sse0, 1e-12),
                        "correlation_moities": _corr(dA, dB)})
        print(f"  repetition {rep} faite, {time.time() - t0:.0f} s", flush=True)

    controles.append({"controle": "coupures 50/50 disjointes", "attendu": "oui",
                      "obtenu": "oui" if coupures_ok else "non", "passe": coupures_ok})
    controles.append({"controle": "effectif minimal d'une cellule retenue, cote A",
                      "attendu": ">= 50", "obtenu": int(min(min_cell)),
                      "passe": min(min_cell) >= T2.MIN_CELLULE})

    # ---- synthese des modeles -------------------------------------------------
    lignes = []
    contrastes = []
    for c, lib in CIBLES:
        for m in MODELES:
            mae = np.mean(np.vstack(acc_boot[c][m]), axis=0)
            r2 = np.mean(np.vstack(acc_r2[c][m]), axis=0)
            lo, hi = T2.ic(mae[1:])
            r2lo, r2hi = T2.ic(r2[1:])
            lignes.append({"cible": c, "unite": lib, "modele": m, "libelle": LIBELLES[m],
                           "erreur_absolue_moyenne": mae[0],
                           "ic_percentile_bas": lo, "ic_percentile_haut": hi,
                           "ic_pivotal_bas": 2 * mae[0] - hi, "ic_pivotal_haut": 2 * mae[0] - lo,
                           "ecart_type_bootstrap": float(np.std(mae[1:])),
                           "r2_inter_groupes": r2[0], "r2_ic_bas": r2lo, "r2_ic_haut": r2hi})
            if m == "M0":
                continue
            mae0 = np.mean(np.vstack(acc_boot[c]["M0"]), axis=0)
            d = mae0 - mae      # positif = le modele fait mieux que le nul
            lo, hi = T2.ic(d[1:])
            contrastes.append({"cible": c, "modele": m, "libelle": LIBELLES[m],
                               "gain_sur_le_nul_points": d[0],
                               "ic_percentile_bas": lo, "ic_percentile_haut": hi,
                               "ic_pivotal_bas": 2 * d[0] - hi, "ic_pivotal_haut": 2 * d[0] - lo,
                               "ecart_type_bootstrap": float(np.std(d[1:])),
                               "p_bootstrap": T2.p_bootstrap(d[1:])})
    df_c = pd.DataFrame(contrastes)
    for c, _ in CIBLES:
        s = df_c["cible"] == c
        df_c.loc[s, "p_holm"] = T2.holm(df_c.loc[s, "p_bootstrap"].values)
    T2.ecrire(lignes, "t2-modeles.csv")
    T2.ecrire(df_c, "t2-contrastes.csv")

    dfa = pd.DataFrame(acc_r2_axe)
    T2.ecrire(dfa.groupby(["cible", "axe", "modele"], as_index=False)
              .agg(n_cellules=("n_cellules", "mean"), r2=("r2", "mean")),
              "t2-variance-inter-groupes.csv")

    lignes_item = []
    for c, _ in CIBLES:
        for j in range(P):
            d = {"cible": c, "item": items[j], "ordinal": bool(garde_ord[j])}
            n = err_item[c]["M0"][j, 1]
            if n == 0:
                continue
            for m in MODELES:
                d["erreur_" + m] = err_item[c][m][j, 0] / n
            lignes_item.append(d)
    dfp = pd.DataFrame(acc_plafond)
    T2.ecrire(dfp.groupby(["cible", "axe"], as_index=False)
              .agg(n_cellules=("n_cellules", "mean"),
                   variance_totale_inter_groupes=("variance_totale_inter_groupes", "mean"),
                   variance_de_bruit=("variance_de_bruit", "mean"),
                   part_de_bruit=("part_de_bruit", "mean"),
                   r2_plafond=("r2_plafond", "mean"),
                   correlation_moities=("correlation_moities", "mean")), "t2-plafond.csv")

    dfq = pd.DataFrame(acc_perm)
    obs_m5 = (dfa[dfa["modele"] == "M5"].groupby(["cible", "axe"], as_index=False)
              .agg(r2_observe=("r2", "mean")))
    obs_r = (dfp.groupby(["cible", "axe"], as_index=False)
             .agg(correlation_observee=("correlation_moities", "mean")))
    band = (dfq.groupby(["cible", "axe"], as_index=False)
            .agg(r2_permute_moyen=("r2_M5", "mean"),
                 r2_permute_p05=("r2_M5", lambda s: float(np.percentile(s, 5))),
                 r2_permute_p95=("r2_M5", lambda s: float(np.percentile(s, 95))),
                 correlation_permutee_moyenne=("correlation_moities", "mean"),
                 correlation_permutee_p95=("correlation_moities",
                                           lambda s: float(np.percentile(s, 95))),
                 n_permutations=("r2_M5", "size")))
    band = band.merge(obs_m5, on=["cible", "axe"], how="left")
    band = band.merge(obs_r, on=["cible", "axe"], how="left")
    pr2, pco = [], []
    for r in band.itertuples():
        sub = dfq[(dfq["cible"] == r.cible) & (dfq["axe"] == r.axe)]
        pr2.append(float((sub["r2_M5"] >= r.r2_observe).mean())
                   if np.isfinite(r.r2_observe) else np.nan)
        pco.append(float((sub["correlation_moities"] >= r.correlation_observee).mean())
                   if np.isfinite(r.correlation_observee) else np.nan)
    band["p_permutation_r2"] = pr2
    band["p_permutation_correlation"] = pco
    band["p_holm_correlation"] = T2.holm(np.array(pco))
    T2.ecrire(band, "t2-permutation-groupes.csv")

    T2.ecrire(lignes_item, "t2-erreur-par-item.csv")
    T2.ecrire(lignes_cellules, "t2-par-groupe-item.csv")
    T2.ecrire(controles, "t2-controles-volet1.csv")
    print(f"volet 1 termine en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    calculer()
