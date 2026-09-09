"""
i3b_abaque : l'abaque du plus petit taux de contamination detectable en fonction de la
taille du flux, de 300 a 5 000 repondants, pour les neuf fabricants de i3.

===========================================================================
PREENREGISTREMENT : resultats/i3b-preenregistrement.md, ecrit le 8 septembre 2026 a
21 h 05 CEST, AVANT ce script et avant tout calcul de resultat. Empreinte SHA-256
57f921196aef0789bc17d63ef4d2ebbffa5d95c8c0bb78b5c31497d734781168.

QUESTION POSEE
--------------
i3 a mesure le detecteur a une seule taille, 1 052 personnes, et l'a ecrit dans ses limites
(point 5). Un institut recoit un flux de 300, de 800 ou de 5 000 repondants. Quel est, a
chacune de ces tailles, le plus petit taux de contamination qu'il peut detecter a puissance
80 pour cent, en bilateral, sous correction ?

SORTIES, toutes dans resultats/
-------------------------------
  i3b-controles.csv             les controles bloquants du preenregistrement section 9
  i3b-reference-par-taille.csv  la bande humaine et son bruit s0(N) a chaque taille
  i3b-abaque.csv                tau*(N) mesure, par source, statistique et taille
  i3b-abaque-extrapolee.csv     tau*(N) au dela de 1 052, loi de puissance, [PROBABLE]
  i3b-courbes-consequence.csv   polarisation et trois marginales, par source, taux, taille

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/i3b_abaque.py
===========================================================================
"""

import argparse
import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import multiprocessing as mp

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a44_commun as C44
import i3_commun as I
import i3b_commun as J

G = {}

# Les valeurs publiees par i3, tableaux 1 et 3 de resultats/i3-detecteur.md, pour le
# controle 9.7 de reproduction. Elles ne sont jamais utilisees ailleurs.
I3_PUR = {
    "humains vague 1": (-0.0686, 0.0422, 0.0272),
    "agents v8": (-0.3199, 0.0942, 0.2587),
    "agents demographiques (v6)": (-0.2279, 0.0926, 0.1216),
    "agents composite": (-0.1819, 0.0839, 0.0584),
    "IM m=10 mode des m": (-0.1208, 0.0571, 0.0508),
    "PMM k=10": (-0.0984, 0.0558, 0.0314),
    "E2 regression contexte tirage": (-0.0376, 0.0275, 0.0240),
    "B0 segment": (0.0014, -0.0003, 0.0229),
    "C2": (-0.1615, 0.0463, 0.3690),
    "C3": (-0.1378, 0.0547, 0.1537),
}
I3_S0 = {"A": 0.002919, "B": 0.000861, "C": 0.000632}


# ---------------------------------------------------------------------------

def _source_codes(nom, rng):
    if nom == "B0 segment":
        z = C44.tirer_nul(G["codes_h"], G["ctx"]["seg"], G["cum_h"], rng)
        z[G["codes_h"] < 0] = -1
        return z
    return G["src"][nom]


def _stats_a_taille(codes, seg, blocs, ctx, rng, n_nul):
    """Les trois statistiques, la polarisation et les trois marginales sur un flux deja
    restreint a sa taille."""
    ctxn = {**ctx, "seg": seg}
    st = I.statistiques(codes, ctxn, rng, n_nul=n_nul)
    pol, _, _ = I.polarisation(codes, blocs, signes=G["signes"])
    out = {k: st[k] for k in ("A", "B", "C", "C5", "patrons", "q5", "conc_nul")}
    out["polarisation"] = pol
    # Le bruit propre de la moyenne des R replicats nuls, qui entre dans A et dans B et
    # PAS dans C ni dans la polarisation. Il ne subit aucune correction de population
    # finie : c'est du bruit de mesure, pas du bruit d'echantillonnage. Voir l'ecart E1
    # declare en section 0 du rapport.
    out["se_nul_A"] = (st["patrons_nul_et"] / np.sqrt(n_nul)
                       / max(st["patrons_nul"], 1e-9)) if n_nul > 1 else 0.0
    out["se_nul_B"] = st["q5_nul_et"] / np.sqrt(n_nul) if n_nul > 1 else 0.0
    out["se_nul_C"] = 0.0
    out["se_nul_polarisation"] = 0.0
    for r, (j, mod) in enumerate(zip(G["marg_items"], G["marg_modales"])):
        out[f"marginale{r + 1}"] = J.part_modale(codes, j, mod)
    return out


def tache_melange(arg):
    """Un flux melange a 1 052, puis lu a chacune des tailles de la grille par sous
    echantillonnage EMBOITE. Preenregistrement section 6."""
    nom, tau, tirage, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 101, G["id_source"][nom],
                                 int(tau * 10000), tirage])
    src = _source_codes(nom, rng)
    f, choisies = I.flux(G["codes_h"], src, G["lignes"][nom], tau, rng)
    marque = np.zeros(f.shape[0], dtype=bool)
    marque[choisies] = True
    ordre = J.ordre_emboite(f.shape[0], rng)
    lignes = []
    for n in J.TAILLES_MESUREES:
        idx = np.sort(ordre[:n])
        st = _stats_a_taille(f[idx], G["ctx"]["seg"][idx], G["ctx"]["blocs"][idx],
                             G["ctx"], rng, n_nul)
        st.update({"source": nom, "taux": tau, "tirage": tirage, "taille": n,
                   "taux_realise": float(marque[idx].mean())})
        lignes.append(st)
    return lignes


def tache_reference(arg):
    """Un sous echantillon humain de taille n, sans remise, avec le meme nombre de
    replicats nuls que les flux, pour que le bruit du nul interieur entre a l'identique."""
    n, b, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 103, n, b])
    idx = np.sort(rng.choice(G["codes_h"].shape[0], size=n, replace=False))
    st = _stats_a_taille(G["codes_h"][idx], G["ctx"]["seg"][idx],
                         G["ctx"]["blocs"][idx], G["ctx"], rng, n_nul)
    st.update({"taille": n, "tirage": b})
    return st


def tache_bootstrap_remise(arg):
    """Le bootstrap AVEC remise, calcule uniquement pour publier son biais, jamais pour un
    test. Ecart E1 de i3."""
    n, b, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 107, n, b])
    idx = rng.integers(0, G["codes_h"].shape[0], size=n)
    st = _stats_a_taille(G["codes_h"][idx], G["ctx"]["seg"][idx],
                         G["ctx"]["blocs"][idx], G["ctx"], rng, n_nul)
    st.update({"taille": n, "tirage": b})
    return st


def tache_validation(arg):
    """Controle 9.6 : une population independante de taille n tiree du nul humain."""
    n, k, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 109, n, k])
    idx = np.sort(rng.choice(G["codes_h"].shape[0], size=n, replace=False))
    z = C44.tirer_nul(G["codes_h"], G["ctx"]["seg"], G["cum_h"], rng)
    z[G["codes_h"] < 0] = -1
    st = _stats_a_taille(z[idx], G["ctx"]["seg"][idx], G["ctx"]["blocs"][idx],
                         G["ctx"], rng, n_nul)
    st.update({"taille": n, "tirage": k})
    return st


def tache_validation_sous(arg):
    """Le pendant du controle 9.6 : sous echantillons d'UNE population nulle de 1 052."""
    n, b, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 113, n, b])
    idx = np.sort(rng.choice(G["z0"].shape[0], size=n, replace=False))
    st = _stats_a_taille(G["z0"][idx], G["ctx"]["seg"][idx], G["ctx"]["blocs"][idx],
                         G["ctx"], rng, n_nul)
    st.update({"taille": n, "tirage": b})
    return st


def tache_pure(nom):
    """Controle 9.7 : la source pure, taux 100 pour cent, contre les valeurs publiees."""
    rng = np.random.default_rng([J.GRAINE, 127, G["id_source"][nom]])
    src = _source_codes(nom, rng)
    lignes = G["lignes"][nom]
    ctxn = {**G["ctx"], "seg": G["ctx"]["seg"][lignes]}
    st = I.statistiques(src[lignes], ctxn, rng, n_nul=40)
    return {"source": nom, "n": len(lignes),
            "A": st["A"], "B": st["B"], "C": st["C"]}


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=12)
    ap.add_argument("--nul", type=int, default=15)
    ap.add_argument("--reference", type=int, default=300)
    ap.add_argument("--validation", type=int, default=40)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--reutiliser-melanges", action="store_true",
                    help="relit resultats/i3b-melanges-par-taille.csv au lieu de "
                         "recalculer les 432 flux ; sert quand seule la reference change")
    args = ap.parse_args()
    if args.smoke:
        args.tirages, args.nul, args.reference, args.validation = 3, 4, 20, 6

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paquet = I.charger(args.cache, args.cache_foret, args.cache_a35)
    ctx = I.contexte(paquet)
    print(f"{paquet['x'].shape[0]} personnes, {len(ctx['items'])} items ; "
          f"absentes : {paquet['absentes'] or 'aucune'}", flush=True)

    controles = []
    codes_h, hors_h = C44.coder(paquet["M"]["humains vague 1"], ctx["alpha"])
    controles.append({"controle": "part de cellules hors nomenclature", "jeu": "gss",
                      "objet": "humains vague 1", "valeur": round(hors_h, 6),
                      "seuil": 0.005, "passe": bool(hors_h < 0.005)})

    src, lignes = {}, {}
    for nom in I.SOURCES + ["humains vague 2"]:
        if nom == "B0 segment":
            lignes[nom] = np.arange(codes_h.shape[0])
            continue
        if nom not in paquet["M"]:
            print(f"source absente, ignoree : {nom}", flush=True)
            continue
        brut, hors = C44.coder(paquet["M"][nom], ctx["alpha"])
        controles.append({"controle": "part de cellules hors nomenclature", "jeu": "gss",
                          "objet": nom, "valeur": round(hors, 6), "seuil": 0.005,
                          "passe": bool(hors < 0.005)})
        lignes[nom] = (ctx["lignes150"] if nom in ("C2", "C3")
                       else np.arange(codes_h.shape[0]))
        m, _ = I.masquer_commun(brut, codes_h)
        src[nom] = m
        li = lignes[nom]
        _, p = I.masquer_commun(brut[li], codes_h[li])
        controles.append({"controle": "cellules perdues par l'intersection des masques",
                          "jeu": "gss", "objet": nom, "valeur": round(p, 6),
                          "seuil": 0.005, "passe": bool(p < 0.005)})

    sources = [s for s in I.SOURCES if s == "B0 segment" or s in src]
    cum_h, replis_h, total_h = C44.lois_par_segment(codes_h, ctx["seg"], ctx["k_items"])
    controles.append({"controle": "taux de repli du generateur nul, S_ideo", "jeu": "gss",
                      "objet": "humains vague 1",
                      "valeur": round(replis_h / max(total_h, 1), 6), "seuil": 0.0,
                      "passe": bool(replis_h == 0)})

    rng0 = np.random.default_rng(J.GRAINE)
    f0, _ = I.flux(codes_h, src["agents v8"], lignes["agents v8"], 0.0, rng0)
    controles.append({"controle": "le flux a taux 0 egale la population de fond",
                      "jeu": "gss", "objet": "toutes sources",
                      "valeur": int((f0 != codes_h).sum()), "seuil": 0,
                      "passe": bool(int((f0 != codes_h).sum()) == 0)})
    ecart_neg = 0
    for tau in I.TAUX:
        fn, _ = I.flux(codes_h, codes_h, np.arange(codes_h.shape[0]), tau,
                       np.random.default_rng(J.GRAINE + 1))
        ecart_neg = max(ecart_neg, int((fn != codes_h).sum()))
    controles.append({"controle": "controle negatif, fond melange a lui meme", "jeu": "gss",
                      "objet": "cinq taux", "valeur": ecart_neg, "seuil": 0,
                      "passe": bool(ecart_neg == 0)})

    _, signes, bon_pol = I.polarisation(codes_h, ctx["blocs"], signes=None)
    marg_items, marg_modales, marg_ecarts = J.choisir_marginales(codes_h, ctx["blocs"])
    print("trois marginales declarees, regle mecanique :", flush=True)
    for r, (j, mod, e) in enumerate(zip(marg_items, marg_modales, marg_ecarts)):
        print(f"  {r + 1}. item {ctx['items'][j]}, modalite modale humaine "
              f"'{ctx['options'][ctx['items'][j]][mod]}', ecart entre camps {e:+.3f}",
              flush=True)

    toutes = I.SOURCES + ["humains vague 2", "humains"]
    G["id_source"] = {n: k + 1 for k, n in enumerate(toutes)}
    G.update({"codes_h": codes_h, "src": src, "lignes": lignes, "ctx": ctx,
              "cum_h": cum_h, "signes": signes, "marg_items": marg_items,
              "marg_modales": marg_modales})
    ctxt = mp.get_context("fork")

    # ---------------------------------------------------- reference par taille
    print("\n--- reference humaine par taille ---", flush=True)
    plein = _stats_a_taille(codes_h, ctx["seg"], ctx["blocs"], ctx,
                            np.random.default_rng([J.GRAINE, 11]), max(args.nul * 4, 40))
    print(f"N = 1052 : A = {plein['A']:+.5f}  B = {plein['B']:+.5f}  "
          f"C = {plein['C']:.5f}  P = {plein['polarisation']:+.4f}", flush=True)

    petites = [n for n in J.TAILLES_MESUREES if n < codes_h.shape[0]]
    taches_ref = [(n, b, args.nul) for n in petites for b in range(args.reference)]
    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        ref_brut = pool.map(tache_reference, taches_ref, chunksize=4)
        print(f"reference : {time.time() - t:.0f} s", flush=True)
        t = time.time()
        boot = pool.map(tache_bootstrap_remise,
                        [(1052, b, args.nul) for b in range(args.reference)], chunksize=4)
        print(f"bootstrap avec remise, pour son biais : {time.time() - t:.0f} s",
              flush=True)
        t = time.time()
        val_dir = pool.map(tache_validation,
                           [(n, k, args.nul) for n in petites
                            for k in range(args.validation)], chunksize=2)
        print(f"controle 9.6, populations nulles independantes : {time.time() - t:.0f} s",
              flush=True)
    refd = pd.DataFrame(ref_brut)

    z0rng = np.random.default_rng([J.GRAINE, 131])
    z0 = C44.tirer_nul(codes_h, ctx["seg"], cum_h, z0rng)
    z0[codes_h < 0] = -1
    G["z0"] = z0
    with ctxt.Pool(args.procs) as pool:
        val_sous = pool.map(tache_validation_sous,
                            [(n, b, args.nul) for n in petites
                             for b in range(args.validation * 3)], chunksize=4)
    vd, vs = pd.DataFrame(val_dir), pd.DataFrame(val_sous)

    lignes_ref = []
    for n in J.TAILLES_MESUREES:
        for cle in ("A", "B", "C", "polarisation"):
            if n == codes_h.shape[0]:
                lignes_ref.append({"taille": n, "statistique": cle,
                                   "valeur": plein[cle], "ic_bas": np.nan,
                                   "ic_haut": np.nan, "ecart_type_sous_echantillon":
                                       np.nan, "facteur_population_finie": np.nan,
                                   "variance_du_nul_interieur": np.nan,
                                   "s0_naif": np.nan,
                                   "s0": np.nan, "n_tirages": 0,
                                   "mode": "population entiere, s0 par loi de puissance"})
                continue
            v = refd[refd.taille == n][cle].values
            fpc = J.correction_population_finie(n, codes_h.shape[0])
            bas, haut, et = J.ic_pivote(v, centre=float(np.mean(v)))
            vn = float(np.mean(refd[refd.taille == n][f"se_nul_{cle}"].values ** 2))
            s0c = float(np.sqrt(max(et ** 2 - vn, 1e-24) * fpc ** 2 + vn))
            lignes_ref.append({
                "taille": n, "statistique": cle, "valeur": float(np.mean(v)),
                "ic_bas": bas, "ic_haut": haut, "ecart_type_sous_echantillon": et,
                "facteur_population_finie": fpc, "variance_du_nul_interieur": vn,
                "s0_naif": et * fpc, "s0": s0c, "n_tirages": int(len(v)),
                "mode": "sous echantillonnage sans remise, pivote, correction de "
                        "population finie sur la seule part d'echantillonnage"})
    ref_df = pd.DataFrame(lignes_ref)

    # loi de puissance s0 = c N^-p sur les trois tailles mesurees, puis s0(1052)
    lois = {}
    for cle in ("A", "B", "C", "polarisation"):
        d = ref_df[(ref_df.statistique == cle) & ref_df.s0.notna()]
        x, y = np.log(d.taille.values.astype(float)), np.log(d.s0.values)
        pente, ordonnee = np.polyfit(x, y, 1)
        pred = ordonnee + pente * x
        r2 = 1.0 - ((y - pred) ** 2).sum() / max(((y - y.mean()) ** 2).sum(), 1e-30)
        lois[cle] = (float(np.exp(ordonnee)), float(-pente), float(r2))
        ref_df.loc[(ref_df.statistique == cle) & (ref_df.taille == codes_h.shape[0]),
                   "s0"] = float(np.exp(ordonnee) * codes_h.shape[0] ** pente)
    ref_df["loi_c"] = ref_df.statistique.map(lambda c: lois[c][0])
    ref_df["loi_p"] = ref_df.statistique.map(lambda c: lois[c][1])
    ref_df["loi_r2"] = ref_df.statistique.map(lambda c: lois[c][2])

    for cle in ("A", "B", "C"):
        s = float(ref_df[(ref_df.statistique == cle)
                         & (ref_df.taille == 1052)].s0.iloc[0])
        d = abs(s - I3_S0[cle]) / I3_S0[cle]
        # Non bloquant, et il faut dire pourquoi : i3 prend son s0 par sous echantillonnage
        # a m = 526 avec trois replicats nuls seulement, i3b par loi de puissance sur trois
        # tailles avec quinze. Les deux estimateurs ne sont pas le meme estimateur, l'ecart
        # est publie tel quel et discute dans le rapport.
        controles.append({"controle": "s0(1052) par loi de puissance contre i3, ecart "
                                      "relatif", "jeu": "gss", "objet": cle,
                          "valeur": round(d, 4), "seuil": "publie, non bloquant",
                          "passe": True})

    # biais du bootstrap avec remise, publie sans jamais servir
    bd = pd.DataFrame(boot)
    for cle in ("A", "B", "C"):
        biais = float(bd[cle].mean() - plein[cle])
        s = float(ref_df[(ref_df.statistique == cle)
                         & (ref_df.taille == 1052)].s0.iloc[0])
        controles.append({"controle": "biais du bootstrap avec remise, en s0",
                          "jeu": "gss", "objet": cle,
                          "valeur": round(biais / s if s else np.nan, 2),
                          "seuil": "publie, non bloquant", "passe": True})

    # controle 9.6 : validite de la mise a l'echelle
    for n in petites:
        fpc = J.correction_population_finie(n, codes_h.shape[0])
        for cle in ("A", "B", "C"):
            direct = vd[vd.taille == n][cle].values
            brut = vs[vs.taille == n][cle].values
            sd_d = float(np.std(direct, ddof=1))
            sd_s = float(np.std(brut, ddof=1))
            vn = float(np.mean(vs[vs.taille == n][f"se_nul_{cle}"].values ** 2))
            corrige = float(np.sqrt(max(sd_s ** 2 - vn, 1e-24) * fpc ** 2 + vn))
            for lib, val in (("naif", sd_s * fpc), ("corrige", corrige)):
                r = val / sd_d if sd_d > 0 else np.nan
                controles.append({
                    "controle": f"validite de la mise a l'echelle, {lib}, N = {n}",
                    "jeu": "gss", "objet": cle, "valeur": round(r, 3),
                    "seuil": "entre 0,7 et 1,4" if lib == "corrige"
                    else "publie pour comparaison",
                    "passe": bool(np.isfinite(r) and 0.7 <= r <= 1.4)
                    if lib == "corrige" else True})

    # controle 9.7 : reproduction de i3 sur les sources pures
    with ctxt.Pool(args.procs) as pool:
        purs = pool.map(tache_pure, sources)
    purs.append({"source": "humains vague 1", "n": codes_h.shape[0],
                 "A": plein["A"], "B": plein["B"], "C": plein["C"]})
    for p in purs:
        if p["source"] in I3_PUR:
            a, b, c = I3_PUR[p["source"]]
            d = max(abs(p["A"] - a), abs(p["B"] - b), abs(p["C"] - c))
            controles.append({"controle": "reproduction de i3, sources pures", "jeu": "gss",
                              "objet": p["source"], "valeur": round(d, 5), "seuil": 0.005,
                              "passe": bool(d < 0.005)})

    J.ecrire(ref_df, "i3b-reference-par-taille.csv")

    # ------------------------------------------------------------- melanges
    print("\n--- melanges, quatre tailles par flux ---", flush=True)
    taches = []
    for nom in sources + (["humains vague 2"] if "humains vague 2" in src else []):
        taux = I.TAUX_SOURCE.get(nom, I.TAUX)
        for tau in taux:
            if tau == 0.0:
                continue
            for d in range(args.tirages):
                taches.append((nom, tau, d, args.nul))
    chemin_mel = os.path.join(J.SORTIE, "i3b-melanges-par-taille.csv")
    if args.reutiliser_melanges and os.path.exists(chemin_mel):
        mel = pd.read_csv(chemin_mel)
        mel = mel[mel.source != "tous"].copy()
        print(f"melanges relus de {chemin_mel}, {len(mel)} lignes", flush=True)
    else:
        print(f"{len(taches)} flux x {len(J.TAILLES_MESUREES)} tailles", flush=True)
        t = time.time()
        with ctxt.Pool(args.procs) as pool:
            res = pool.map(tache_melange, taches, chunksize=2)
        print(f"melanges : {time.time() - t:.0f} s", flush=True)
        mel = pd.DataFrame([x for bloc in res for x in bloc])

    # la ligne taux 0 par taille : c'est la reference elle meme
    zero = []
    for n in J.TAILLES_MESUREES:
        if n == codes_h.shape[0]:
            zero.append({**plein, "source": "tous", "taux": 0.0, "tirage": -1,
                         "taille": n, "taux_realise": 0.0})
        else:
            d = refd[refd.taille == n]
            zero.append({**{c: float(d[c].mean()) for c in d.columns
                            if c not in ("taille", "tirage")},
                         "source": "tous", "taux": 0.0, "tirage": -1, "taille": n,
                         "taux_realise": 0.0})
    mel = pd.concat([pd.DataFrame(zero), mel], ignore_index=True)
    J.ecrire(mel, "i3b-melanges-par-taille.csv")

    # ------------------------------------------------------- abaque
    print("\n--- abaque ---", flush=True)
    refv = {(r.taille, r.statistique): r.valeur for r in ref_df.itertuples()}
    s0 = {(r.taille, r.statistique): r.s0 for r in ref_df.itertuples()}
    lignes_ab, courbes = [], {}
    for nom in sorted(set(mel.source) - {"tous"}):
        d = mel[mel.source == nom]
        for n in J.TAILLES_MESUREES:
            dn = d[d.taille == n]
            for cle in ("A", "B", "C"):
                taux = sorted(dn.taux.unique())
                moy = [float(dn[dn.taux == t][cle].mean()) for t in taux]
                ecarts = [m - refv[(n, cle)] for m in moy]
                a, b, r2 = J.ajuster_courbe([0.0] + taux, [0.0] + ecarts)
                courbes[(cle, nom, n)] = (a, b, r2)
                s = s0[(n, cle)]
                tau_f1 = J.racine_courbe(a, b, (J.Z_F1 + J.Z_PUISSANCE) * s)
                tau_i3 = J.racine_courbe(a, b, (J.Z_I3 + J.Z_PUISSANCE) * s)
                tau_nom = J.racine_courbe(a, b, (I.Z_ALPHA + J.Z_PUISSANCE) * s)
                for t, m in zip(taux, moy):
                    sd = dn[dn.taux == t][cle]
                    z = (m - refv[(n, cle)]) / s if s and np.isfinite(s) else np.nan
                    lignes_ab.append({
                        "source": nom, "famille": I.FAMILLE.get(nom, "humain"),
                        "statistique": cle, "taille": n, "taux": t,
                        "taux_realise_moyen": float(dn[dn.taux == t].taux_realise.mean()),
                        "valeur_moyenne": m, "ecart_a_la_reference": m - refv[(n, cle)],
                        "s0": s, "z": z,
                        "p_bilateral": J.p_bilateral(z) if np.isfinite(z) else np.nan,
                        "puissance_empirique": float(
                            (np.abs(sd.values - refv[(n, cle)]) > J.Z_F1 * s).mean())
                        if s and np.isfinite(s) else np.nan,
                        "n_tirages": int(len(sd)),
                        "tau_etoile_holm3": tau_f1, "tau_etoile_holm27": tau_i3,
                        "tau_etoile_nominal": tau_nom,
                        "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    ab = pd.DataFrame(lignes_ab)
    J.ecrire(ab, "i3b-abaque.csv")

    # ------------------------------------------------- extrapolation au dela de 1 052
    print("\n--- extrapolation ---", flush=True)
    lignes_ex = []
    for nom in sorted(set(mel.source) - {"tous"}):
        for cle in ("A", "B", "C"):
            a3 = courbes.get((cle, nom, 300))
            a10 = courbes.get((cle, nom, 1052))
            if a3 is None or a10 is None:
                continue
            # stabilite en N de la courbe d'effet, lue a 10 pour cent de contamination
            e3 = a3[0] * 0.10 + a3[1] * 0.01
            e10 = a10[0] * 0.10 + a10[1] * 0.01
            rap = e3 / e10 if e10 else np.nan
            stable = bool(np.isfinite(rap) and 0.8 <= rap <= 1.25)
            c, p, r2loi = lois[cle]
            for n in J.TAILLES_EXTRAPOLEES:
                s = c * n ** (-p)
                tau = (J.racine_courbe(a10[0], a10[1], (J.Z_F1 + J.Z_PUISSANCE) * s)
                       if stable else np.nan)
                lignes_ex.append({
                    "source": nom, "famille": I.FAMILLE.get(nom, "humain"),
                    "statistique": cle, "taille": n, "s0_extrapole": s,
                    "loi_c": c, "loi_p": p, "loi_r2": r2loi,
                    "rapport_effet_300_sur_1052": rap,
                    "courbe_stable_en_N": stable,
                    "tau_etoile_holm3": tau,
                    "statut": "[PROBABLE], extrapolation" if stable
                    else "exige une seconde population"})
    ex = pd.DataFrame(lignes_ex)
    J.ecrire(ex, "i3b-abaque-extrapolee.csv")

    # -------------------------------------------- courbes de consequence
    cons = []
    quantites = ["polarisation", "marginale1", "marginale2", "marginale3"]
    for nom in sorted(set(mel.source) - {"tous"}):
        d = mel[mel.source == nom]
        for n in J.TAILLES_MESUREES:
            dn = d[d.taille == n]
            for q in quantites:
                base = float(plein[q]) if n == codes_h.shape[0] \
                    else float(refd[refd.taille == n][q].mean())
                taux = sorted(dn.taux.unique())
                moy = [float(dn[dn.taux == t][q].mean()) for t in taux]
                a, b, r2 = J.ajuster_courbe([0.0] + taux, [0.0] + [m - base for m in moy])
                for t, m in zip(taux, moy):
                    cons.append({"source": nom, "quantite": q, "taille": n, "taux": t,
                                 "valeur_humaine": base, "valeur": m,
                                 "ecart": m - base,
                                 "facteur": m / base if base else np.nan,
                                 "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    J.ecrire(pd.DataFrame(cons), "i3b-courbes-consequence.csv")

    meta = {"marginales": [{"rang": r + 1, "item": ctx["items"][j],
                            "modalite_modale_humaine":
                                ctx["options"][ctx["items"][j]][m],
                            "ecart_entre_camps_humain": e}
                           for r, (j, m, e) in
                           enumerate(zip(marg_items, marg_modales, marg_ecarts))],
            "z_holm3": J.Z_F1, "z_holm27": J.Z_I3, "z_holm39": J.Z_F2,
            "z_holm5": J.Z_F3,
            "n_items_polarisation": int(bon_pol.sum()),
            "tirages": args.tirages, "nul": args.nul, "reference": args.reference}
    open(os.path.join(J.SORTIE, "i3b-meta.json"), "w").write(json.dumps(meta, indent=1))

    ctrl = pd.DataFrame(controles)
    J.ecrire(ctrl, "i3b-controles.csv")
    print(ctrl.to_string(index=False, max_colwidth=55), flush=True)
    if not ctrl["passe"].all():
        print("\n*** au moins un controle ne passe pas ***", flush=True)
    print(f"\ntotal {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
