"""
i1_previsibilite : Q-B du preenregistrement I1. Peut on predire, a partir des seules
reponses de vague 1 et des demographies, qui changera d'avis sur un item donne ?

Quatre predicteurs, trois temoins, et la quantite de verdict declaree : la chute de l'AUC
sous permutation des personnes a l'interieur du segment ideologie x age x education,
transposition de la mesure de personne de a44.

Zero appel de modele. Lecture seule sur data/. Aucun script existant modifie.

Sorties :
  resultats/i1-auc-par-item.csv
  resultats/i1-auc-synthese.csv
  resultats/i1-permutation.csv
  resultats/i1-bande-nulle.csv

Usage : .venv/bin/python analyses/i1_previsibilite.py [--items N] [--cible chg|mono]
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd
from scipy import sparse
from scipy.special import erfc
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_commun as I1

PREDICTEURS = ["P position initiale seule", "L1 logistique resumee",
               "L2 logistique complete", "V voisins k=25", "F foret"]
TEMOINS = ["T0 nul avec derive", "T0b nul a taux commun", "T1 temoin de segment"]


# ---------------------------------------------------------------------------
# 1. Construction des blocs de variables, tous lus a la vague de depart
# ---------------------------------------------------------------------------

def indicatrices_demographies(paquet):
    """Demographies de la vague de depart en indicatrices, plus l'indicatrice de panel."""
    d = paquet["demos"]
    colonnes = []
    noms = []
    for nom in I1.DEMOS:
        v = d[nom]
        niveaux = sorted({x for x in np.unique(v) if np.isfinite(x)})
        for k in niveaux:
            colonnes.append((v == k).astype(np.float32))
            noms.append(f"{nom}={k:g}")
        colonnes.append((~np.isfinite(v)).astype(np.float32))
        noms.append(f"{nom}=manquant")
    for pan in sorted(set(paquet["panel"])):
        colonnes.append((paquet["panel"] == pan).astype(np.float32))
        noms.append(f"panel={pan}")
    return sparse.csr_matrix(np.column_stack(colonnes)), noms


def indicatrices_profil(paquet):
    """Le profil complet de vague de depart en indicatrices, item par item.

    Le manquant est une modalite comme les autres : ne pas le coder reviendrait a
    donner la meme ligne a une personne qui a repondu la modalite de reference et a une
    personne qui n'a pas repondu.
    """
    ca = paquet["c_a"]
    n, p = ca.shape
    blocs, debuts, noms = [], [], []
    for j in range(p):
        k = paquet["k_par_item"][j]
        m = np.zeros((n, k + 1), dtype=np.float32)
        col = ca[:, j]
        obs = col >= 0
        m[np.flatnonzero(obs), col[obs]] = 1.0
        m[~obs, k] = 1.0
        debuts.append(sum(b.shape[1] for b in blocs))
        blocs.append(sparse.csr_matrix(m))
        noms.extend([f"{paquet['items'][j]}={c}" for c in range(k + 1)])
    return sparse.hstack(blocs, format="csr"), debuts, noms


def resumes(paquet, profs):
    """Les six resumes numeriques du profil, predicteur L1."""
    X = np.column_stack([
        profs["z_eco"], profs["z_soc"], profs["cross_pression"],
        profs["distance_patron_segment"], profs["part_rare"], profs["part_manquants"],
    ]).astype(np.float32)
    X = np.where(np.isfinite(X), X, 0.0)
    return sparse.csr_matrix(X)


# ---------------------------------------------------------------------------
# 2. Les predicteurs, un item a la fois
# ---------------------------------------------------------------------------

def _proba(modele, X):
    p = modele.predict_proba(X)
    return p[:, list(modele.classes_).index(1)] if 1 in modele.classes_ \
        else np.zeros(X.shape[0])


def scores_hors_pli(j, y, plis, blocs, paquet, profs, dist_par_pli):
    """Scores hors pli des quatre predicteurs et des deux temoins, pour un item."""
    n = len(y)
    ev = np.flatnonzero(y >= 0)
    sortie = {m: np.full(n, np.nan) for m in PREDICTEURS + TEMOINS}
    debut = blocs["debuts_profil"][j]
    fin = debut + paquet["k_par_item"][j] + 1
    x_item = blocs["profil"][:, debut:fin]
    X_l1 = sparse.hstack([blocs["demo"], blocs["resume"], x_item], format="csr")
    X_l2 = sparse.hstack([blocs["demo"], blocs["profil"]], format="csr")
    X_f = blocs["foret"]
    seg = blocs["seg_codes"]

    for f in range(I1.N_PLIS):
        tr = ev[plis[ev] != f]
        te = ev[plis[ev] == f]
        if len(te) == 0 or len(tr) < 50:
            continue
        ytr = y[tr]
        taux = float(ytr.mean())
        sortie["T0 nul avec derive"][te] = taux
        sortie["T0b nul a taux commun"][te] = float(y[ev].mean())
        # T1 : taux de changement du segment, estime sur le pli d'entrainement seul
        t1 = np.full(len(te), taux)
        for s in np.unique(seg[te]):
            m_tr = tr[seg[tr] == s]
            if len(m_tr) >= I1.MIN_SEGMENT:
                t1[seg[te] == s] = float(y[m_tr].mean())
        sortie["T1 temoin de segment"][te] = t1
        # P : le taux de changement des personnes qui donnent la MEME modalite que la
        # personne a l'item j en vague de depart, estime sur le pli d'entrainement seul.
        # C'est le pendant exact de T1 avec la reponse propre a la place du segment. Il
        # isole la part du signal individuel qui n'est que le retour a la mode : une
        # modalite rare est instable, celui qui la tient change plus, et cela se sait
        # sans rien connaitre de la personne d'autre que cette reponse.
        pmod = np.full(len(te), taux)
        mod_te = paquet["c_a"][te, j]
        mod_tr = paquet["c_a"][tr, j]
        for mm in np.unique(mod_te):
            sel = tr[mod_tr == mm]
            if len(sel) >= I1.MIN_SEGMENT:
                pmod[mod_te == mm] = float(y[sel].mean())
        sortie["P position initiale seule"][te] = pmod
        if ytr.min() == ytr.max():
            for m in PREDICTEURS:
                sortie[m][te] = taux
            continue
        for nom, X in (("L1 logistique resumee", X_l1), ("L2 logistique complete", X_l2)):
            mod = LogisticRegression(max_iter=1000, C=1.0, solver="liblinear")
            mod.fit(X[tr], ytr)
            sortie[nom][te] = _proba(mod, X[te])
        mod = RandomForestClassifier(n_estimators=200, min_samples_leaf=5,
                                     max_features="sqrt", n_jobs=4,
                                     random_state=I1.GRAINE + f)
        mod.fit(X_f[tr], ytr)
        sortie["F foret"][te] = _proba(mod, X_f[te])
        # V : k plus proches voisins, item j retire de la distance
        d = dist_par_pli[f](j)          # (n_test_pli, n_train_pli) sur les evaluables
        sortie["V voisins k=25"][te] = d(tr, te, y)
    return sortie


def fabrique_distances(paquet, plis):
    """Prepare, par pli, le calcul de la distance de Hamming privee d'un item.

    A = nombre d'items ou les deux personnes repondent la meme modalite, C = nombre
    d'items renseignes chez les deux. Les deux sont calcules une seule fois par pli ;
    retirer l'item j se fait ensuite par soustraction de deux matrices de rang faible,
    ce qui evite de recalculer 118 fois une distance sur 118 items.
    """
    ca = paquet["c_a"]
    n, p = ca.shape
    obs = (ca >= 0)
    fabriques = []
    for f in range(I1.N_PLIS):
        idx_tr = np.flatnonzero(plis != f)
        idx_te = np.flatnonzero(plis == f)
        A = np.zeros((len(idx_te), len(idx_tr)), dtype=np.int16)
        C = np.zeros((len(idx_te), len(idx_tr)), dtype=np.int16)
        a_te, a_tr = ca[idx_te], ca[idx_tr]
        o_te, o_tr = obs[idx_te], obs[idx_tr]
        for j in range(p):
            both = np.logical_and(o_te[:, j][:, None], o_tr[:, j][None, :])
            C += both
            A += np.logical_and(both, a_te[:, j][:, None] == a_tr[:, j][None, :])
        pos_te = {g: k for k, g in enumerate(idx_te)}
        pos_tr = {g: k for k, g in enumerate(idx_tr)}

        def faire(j, A=A, C=C, a_te=a_te, a_tr=a_tr, o_te=o_te, o_tr=o_tr,
                  pos_te=pos_te, pos_tr=pos_tr):
            both = np.logical_and(o_te[:, j][:, None], o_tr[:, j][None, :])
            eq = np.logical_and(both, a_te[:, j][:, None] == a_tr[:, j][None, :])
            Aj = A - eq
            Cj = C - both

            def predire(tr, te, y):
                lt = np.array([pos_tr[g] for g in tr])
                le = np.array([pos_te[g] for g in te])
                sous_a = Aj[np.ix_(le, lt)].astype(np.float32)
                sous_c = Cj[np.ix_(le, lt)].astype(np.float32)
                d = np.where(sous_c > 0, 1.0 - sous_a / np.maximum(sous_c, 1), 1.0)
                k = min(I1.K_VOISINS, d.shape[1])
                ordre = np.argpartition(d, k - 1, axis=1)[:, :k]
                return y[tr][ordre].mean(axis=1)
            return predire
        fabriques.append(faire)
    return fabriques


# ---------------------------------------------------------------------------
# 3. Permutation intra segment, bande nulle, bootstrap
# ---------------------------------------------------------------------------

def permutation(y, score, seg_codes, rng, n=I1.N_PERMUTATIONS):
    """AUC apres permutation des scores entre personnes du meme segment, n fois.

    C'est la permutation de a44 appliquee au changement : le segment est conserve, ce
    qui distingue une personne d'une autre a l'interieur du segment ne l'est pas.
    """
    ok = np.isfinite(score) & (y >= 0)
    yy, ss, gg = y[ok], score[ok], seg_codes[ok]
    vals = np.empty(n)
    for r in range(n):
        perm = I1.permuter_intra(gg, rng)
        vals[r] = I1.auc(yy, ss[perm])
    return vals


def bande_nulle(y, rng, n=I1.N_PERMUTATIONS):
    """La bande d'echantillonnage de l'AUC en l'absence totale de signal.

    Un score tire au hasard, note contre les VRAIES etiquettes de changement, a
    l'effectif reel de l'item. C'est cette bande, et non la valeur 0,5, qui dit si une
    AUC observee est distinguable de rien. Le temoin T0 du preenregistrement, qui donne
    a chaque personne la probabilite marginale de l'item, est un score constant : son
    AUC vaut 0,5 exactement, il ne renseigne pas sur la dispersion.
    """
    yy = y[y >= 0]
    return np.array([I1.auc(yy, rng.random(len(yy))) for _ in range(n)])


def bootstrap_synthese(Y, idx_item, items_ok, scores, evaluables, seg_codes, n_boot, rng):
    """IC a 95 pour cent des deux quantites agregees, reechantillonnage sur les PERSONNES.

    L'unite de tirage est la personne et non la cellule : deux items d'une meme personne
    ne sont pas independants, un bootstrap sur les cellules donnerait un intervalle
    faussement etroit. C'est la regle de a2_commun.bootstrap_personnes, transposee a une
    quantite qui se calcule item par item avant d'etre moyennee.

    A chaque tirage la chute est recalculee avec une permutation intra segment FRAICHE :
    l'intervalle publie contient donc a la fois l'incertitude d'echantillonnage sur les
    personnes et celle de la permutation.
    """
    n = Y.shape[0]
    lignes = {m: {"auc": [], "chute": []} for m in PREDICTEURS + TEMOINS}
    for b in range(n_boot):
        tirage = rng.integers(0, n, size=n)
        acc = {m: [[], [], []] for m in PREDICTEURS + TEMOINS}
        for it in items_ok:
            j = idx_item[it]
            sel = tirage[evaluables[it][tirage]]
            if len(sel) < 50:
                continue
            y = Y[sel, j]
            if y.min() == y.max():
                continue
            perm = I1.permuter_intra(seg_codes[sel], rng)
            for m in PREDICTEURS + TEMOINS:
                s_m = scores[it][m][sel]
                a = I1.auc(y, s_m)
                if not np.isfinite(a):
                    continue
                acc[m][0].append(a)
                acc[m][1].append(a - I1.auc(y, s_m[perm]))
                acc[m][2].append(len(sel))
        for m in PREDICTEURS + TEMOINS:
            if acc[m][0]:
                w = np.array(acc[m][2], dtype=float)
                lignes[m]["auc"].append(float(np.average(acc[m][0], weights=w)))
                lignes[m]["chute"].append(float(np.average(acc[m][1], weights=w)))
        if (b + 1) % 50 == 0:
            print(f"  tirage {b + 1}/{n_boot}", flush=True)
    out = []
    for m in PREDICTEURS + TEMOINS:
        a = np.array(lignes[m]["auc"])
        c = np.array(lignes[m]["chute"])
        out.append({"predicteur": m,
                    "auc_ic_bas": float(np.percentile(a, 2.5)) if len(a) else np.nan,
                    "auc_ic_haut": float(np.percentile(a, 97.5)) if len(a) else np.nan,
                    "chute_ic_bas": float(np.percentile(c, 2.5)) if len(c) else np.nan,
                    "chute_ic_haut": float(np.percentile(c, 97.5)) if len(c) else np.nan,
                    "chute_p_bootstrap": float(min(1.0, 2 * min((c <= 0).mean(),
                                                                (c >= 0).mean())))
                    if len(c) else np.nan,
                    "n_tirages": len(c)})
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# 4. Programme
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", type=int, default=0, help="0 = tous")
    ap.add_argument("--cible", default="chg", choices=["chg", "mono"])
    ap.add_argument("--boot", type=int, default=I1.N_BOOTSTRAP)
    args = ap.parse_args()
    rng = np.random.default_rng(I1.GRAINE)

    noyau, brut, n_paires = I1.charger_panels()
    tables = I1.alphabet_panel(brut, len(noyau))
    paquet = I1.assembler(I1.PAIRES_4ANS, noyau, brut, tables)
    profs = I1.profils(paquet)
    y_chg, y_mono = I1.y_changement(paquet)
    Y = y_chg if args.cible == "chg" else y_mono
    print(f"{paquet['n']} personnes, {len(noyau)} items, cible {args.cible}", flush=True)

    seg_codes, niveaux = I1.codes_segment(paquet["segment"])
    print(f"{len(niveaux)} segments, effectif median "
          f"{np.median(np.bincount(seg_codes)):.0f}", flush=True)

    plis = rng.permutation(paquet["n"]) % I1.N_PLIS      # decoupe sur les personnes
    demo, noms_demo = indicatrices_demographies(paquet)
    profil, debuts, noms_profil = indicatrices_profil(paquet)
    foret = np.column_stack(
        [paquet["c_a"].astype(np.float32)]
        + [np.where(np.isfinite(paquet["demos"][d]), paquet["demos"][d], -1.0)
           for d in I1.DEMOS]).astype(np.float32)
    blocs = {"demo": demo, "profil": profil, "debuts_profil": debuts,
             "resume": resumes(paquet, profs), "foret": foret, "seg_codes": seg_codes}
    print(f"{demo.shape[1]} indicatrices demographiques, "
          f"{profil.shape[1]} indicatrices de profil", flush=True)

    dist = fabrique_distances(paquet, plis)

    items = range(len(noyau)) if not args.items else range(min(args.items, len(noyau)))
    lignes, perm_lignes, bande = [], [], []
    scores_gardes, evaluables = {}, {}
    for j in items:
        y = Y[:, j]
        ev = y >= 0
        n_ev, n_pos = int(ev.sum()), int((y == 1).sum())
        if n_ev < I1.MIN_PERSONNES_ITEM or n_pos < I1.MIN_CHANGEURS_ITEM \
                or n_pos == n_ev:
            continue
        sc = scores_hors_pli(j, y, plis, blocs, paquet, profs, dist)
        scores_gardes[noyau[j]] = {m: sc[m].astype(np.float32) for m in sc}
        evaluables[noyau[j]] = ev
        alea = bande_nulle(y, rng, n=I1.N_PERMUTATIONS)
        bande.append({"item": noyau[j], "n_personnes": n_ev, "n_changeurs": n_pos,
                      "auc_alea_moyenne": float(alea.mean()),
                      "auc_alea_p2_5": float(np.percentile(alea, 2.5)),
                      "auc_alea_p97_5": float(np.percentile(alea, 97.5))})
        for m in PREDICTEURS + TEMOINS:
            s = sc[m]
            a_obs = I1.auc(y[ev], s[ev])
            r_obs = I1.rappel_a_taux_de_base(y[ev], s[ev])
            vals = permutation(y, s, seg_codes, rng)
            p = (1 + int((vals >= a_obs).sum())) / (1 + len(vals))
            # p empirique et p par approximation normale de la distribution de
            # permutation. Le p empirique est plancher a 1 / (1 + 200) = 0,004975 ; sur
            # 118 items, Holm exige moins de 0,05 / 118 = 0,000424 pour retenir quoi que
            # ce soit. Le plancher rend donc Holm structurellement incapable de retenir
            # un item, quel que soit le resultat. L'approximation normale, licite parce
            # que l'AUC est une statistique de rang moyennee sur toutes les paires et
            # que sa loi de permutation est symetrique et unimodale, redonne la
            # resolution ; les deux sont publies.
            sd = float(np.std(vals, ddof=1))
            z = (a_obs - float(np.mean(vals))) / sd if sd > 0 else np.nan
            p_z = float(erfc(z / np.sqrt(2.0)) / 2.0) if np.isfinite(z) else np.nan
            lignes.append({
                "item": noyau[j], "cible": args.cible, "predicteur": m,
                "n_personnes": n_ev, "n_changeurs": n_pos,
                "taux_de_base": n_pos / n_ev,
                "auc": a_obs, "rappel": r_obs,
                "auc_permutee": float(np.mean(vals)),
                "auc_permutee_p2_5": float(np.percentile(vals, 2.5)),
                "auc_permutee_p97_5": float(np.percentile(vals, 97.5)),
                "auc_permutee_ecart_type": sd, "z_permutation": z,
                "chute": a_obs - float(np.mean(vals)), "p_permutation": p,
                "p_permutation_normale": p_z,
            })
        perm_lignes.append({"item": noyau[j], "n_personnes": n_ev})
        if (j + 1) % 10 == 0:
            print(f"  item {j + 1}/{len(noyau)}", flush=True)

    t = pd.DataFrame(lignes)
    # correction pour tests multiples, sur le predicteur primaire puis sur les autres
    t["p_holm"] = np.nan
    t["p_bh"] = np.nan
    for m in PREDICTEURS + TEMOINS:
        s = t["predicteur"] == m
        t.loc[s, "p_holm"] = I1.holm(t.loc[s, "p_permutation"].values)
        t.loc[s, "p_bh"] = I1.benjamini_hochberg(t.loc[s, "p_permutation"].values)
        pz = np.nan_to_num(t.loc[s, "p_permutation_normale"].values, nan=1.0)
        t.loc[s, "p_holm_normale"] = I1.holm(pz)
        t.loc[s, "p_bh_normale"] = I1.benjamini_hochberg(pz)
    I1.ecrire(t, f"i1-auc-par-item{'' if args.cible == 'chg' else '-mono'}.csv")
    I1.ecrire(pd.DataFrame(bande),
              f"i1-bande-nulle{'' if args.cible == 'chg' else '-mono'}.csv")

    # --- synthese, avec bootstrap sur les personnes
    syn = []
    items_ok = sorted(t["item"].unique())
    idx_item = {noyau[j]: j for j in range(len(noyau))}
    scores_cache = {}
    for m in PREDICTEURS + TEMOINS:
        d = t[t["predicteur"] == m]
        w = d["n_personnes"].values.astype(float)
        syn.append({
            "predicteur": m, "cible": args.cible, "n_items": len(d),
            "auc_moyenne_ponderee": float(np.average(d["auc"], weights=w)),
            "auc_mediane": float(d["auc"].median()),
            "auc_permutee_moyenne": float(np.average(d["auc_permutee"], weights=w)),
            "chute_moyenne_ponderee": float(np.average(d["chute"], weights=w)),
            "chute_mediane": float(d["chute"].median()),
            "rappel_moyen_pondere": float(np.average(d["rappel"].fillna(0), weights=w)),
            "taux_de_base_moyen": float(np.average(d["taux_de_base"], weights=w)),
            "n_items_holm_retenus": int((d["p_holm"] < 0.05).sum()),
            "n_items_bh_retenus": int((d["p_bh"] < 0.05).sum()),
            "n_items_holm_normale_retenus": int((d["p_holm_normale"] < 0.05).sum()),
            "n_items_bh_normale_retenus": int((d["p_bh_normale"] < 0.05).sum()),
            "z_permutation_median": float(d["z_permutation"].median()),
        })
    # bootstrap sur les personnes : une personne tiree entre avec toutes ses lignes item
    print(f"\nbootstrap sur les personnes, {args.boot} tirages", flush=True)
    ic = bootstrap_synthese(Y, idx_item, items_ok, scores_gardes, evaluables,
                            seg_codes, args.boot, rng)
    syn = pd.DataFrame(syn).merge(ic, on="predicteur", how="left")
    I1.ecrire(syn, f"i1-auc-synthese{'' if args.cible == 'chg' else '-mono'}.csv")
    print(pd.DataFrame(syn).to_string(index=False), flush=True)
    np.save(os.path.join("/tmp", f"i1-plis-{args.cible}.npy"), plis)
    print("\ni1_previsibilite termine", flush=True)


if __name__ == "__main__":
    main()
