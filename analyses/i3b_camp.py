"""
i3b_camp : la contamination concentree sur un seul camp, qui est le cas d'une operation
d'influence, contre la contamination uniforme de i3.

===========================================================================
PREENREGISTREMENT : resultats/i3b-preenregistrement.md, ecrit le 8 septembre 2026 a
21 h 05 CEST, AVANT ce script et avant tout calcul de resultat.

QUESTION POSEE
--------------
i3 melange les faux repondants uniformement sur les segments, et l'ecrit dans ses limites
(point 6) : une fraude reelle serait concentree, par exemple tous les faux repondants d'un
meme camp. Est elle plus ou moins detectable, et de combien deplace t elle l'ecart mesure
entre camps ?

DEUX LECTURES DE LA DETECTION, declarees au preenregistrement section 6
  globale : les trois statistiques sur le flux entier, ce que fait un auditeur qui ne sait
            pas ou chercher ;
  par camp : les trois statistiques sur les seules personnes du bloc vise, avec leur propre
            bruit de reference a la taille du bloc, ce que fait un auditeur averti.

SORTIES, toutes dans resultats/
-------------------------------
  i3b-camp-reference.csv     la bande humaine par bloc ideologique, avec son s0
  i3b-camp-detection.csv     z, p, puissance et tau* par source, camp, taux et lecture
  i3b-camp-polarisation.csv  l'ecart entre camps et les trois marginales

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/i3b_camp.py
===========================================================================
"""

import argparse
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
TAUX_CAMP = [0.02, 0.05, 0.10, 0.20, 0.30]
CAMP_PRIMAIRE = "droite"
# hash() est randomise par processus en Python 3 : les graines ne peuvent pas en dependre.
ID_CAMP = {"gauche": 1, "centre": 2, "droite": 3}
# Preenregistrement section 6 : le second camp est calcule pour les trois fabricants les
# plus detectables et les deux les moins detectables selon le tableau 5 de i3.
SOURCES_SECOND_CAMP = ["agents v8", "C2", "B0 segment", "PMM k=10",
                       "E2 regression contexte tirage"]
FRACTIONS_REF = [0.4, 0.6, 0.8]


def _source_codes(nom, rng):
    if nom == "B0 segment":
        z = C44.tirer_nul(G["codes_h"], G["ctx"]["seg"], G["cum_h"], rng)
        z[G["codes_h"] < 0] = -1
        return z
    return G["src"][nom]


def _mesures(codes, seg, blocs, ctx, rng, n_nul, camp):
    """Les trois statistiques en lecture globale, puis en lecture a l'interieur du camp
    vise, plus la polarisation et les trois marginales."""
    st = I.statistiques(codes, {**ctx, "seg": seg}, rng, n_nul=n_nul)
    out = {f"global_{k}": st[k] for k in ("A", "B", "C")}
    li = np.flatnonzero(blocs == camp)
    stc = I.statistiques(codes[li], {**ctx, "seg": seg[li]}, rng, n_nul=n_nul)
    out.update({f"camp_{k}": stc[k] for k in ("A", "B", "C")})
    pol, _, _ = I.polarisation(codes, blocs, signes=G["signes"])
    out["polarisation"] = pol
    for r, (j, mod) in enumerate(zip(G["marg_items"], G["marg_modales"])):
        out[f"marginale{r + 1}"] = J.part_modale(codes, j, mod)
    return out


def tache_melange(arg):
    nom, camp, tau, tirage, mode, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 301, G["id_source"][nom],
                                 ID_CAMP[camp], int(tau * 10000), tirage,
                                 0 if mode == "concentre" else 1])
    src = _source_codes(nom, rng)
    if mode == "concentre":
        f, _ = J.flux_concentre(G["codes_h"], src, G["lignes"][nom], G["ctx"]["blocs"],
                                camp, tau, rng)
    else:
        f, _ = I.flux(G["codes_h"], src, G["lignes"][nom], tau, rng)
    m = _mesures(f, G["ctx"]["seg"], G["ctx"]["blocs"], G["ctx"], rng, n_nul, camp)
    m.update({"source": nom, "camp": camp, "taux": tau, "tirage": tirage, "mode": mode})
    return m


def tache_reference_camp(arg):
    """Reference du bloc : sous echantillon des seules personnes du bloc, sans remise."""
    camp, m, b, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 303, ID_CAMP[camp], m, b])
    li = np.flatnonzero(G["ctx"]["blocs"] == camp)
    idx = np.sort(rng.choice(li, size=m, replace=False))
    st = I.statistiques(G["codes_h"][idx], {**G["ctx"], "seg": G["ctx"]["seg"][idx]},
                        rng, n_nul=n_nul)
    return {"camp": camp, "taille": m, "tirage": b,
            "se_nul_A": (st["patrons_nul_et"] / np.sqrt(n_nul)
                         / max(st["patrons_nul"], 1e-9)) if n_nul > 1 else 0.0,
            "se_nul_B": st["q5_nul_et"] / np.sqrt(n_nul) if n_nul > 1 else 0.0,
            "se_nul_C": 0.0,
            **{k: st[k] for k in ("A", "B", "C")}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=10)
    ap.add_argument("--nul", type=int, default=12)
    ap.add_argument("--reference", type=int, default=200)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.tirages, args.nul, args.reference = 3, 4, 15

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paquet = I.charger(args.cache, args.cache_foret, args.cache_a35)
    ctx = I.contexte(paquet)
    codes_h, _ = C44.coder(paquet["M"]["humains vague 1"], ctx["alpha"])
    src, lignes = {}, {}
    for nom in I.SOURCES + ["humains vague 2"]:
        if nom == "B0 segment":
            lignes[nom] = np.arange(codes_h.shape[0])
            continue
        if nom not in paquet["M"]:
            continue
        brut, _ = C44.coder(paquet["M"][nom], ctx["alpha"])
        lignes[nom] = (ctx["lignes150"] if nom in ("C2", "C3")
                       else np.arange(codes_h.shape[0]))
        src[nom], _ = I.masquer_commun(brut, codes_h)
    sources = [s for s in I.SOURCES if s == "B0 segment" or s in src]
    cum_h, _, _ = C44.lois_par_segment(codes_h, ctx["seg"], ctx["k_items"])
    _, signes, _ = I.polarisation(codes_h, ctx["blocs"], signes=None)
    marg_items, marg_modales, _ = J.choisir_marginales(codes_h, ctx["blocs"])

    effectifs = {c: int((ctx["blocs"] == c).sum()) for c in ("gauche", "centre", "droite")}
    print("effectifs par bloc :", effectifs, flush=True)

    G.update({"codes_h": codes_h, "src": src, "lignes": lignes, "ctx": ctx,
              "cum_h": cum_h, "signes": signes, "marg_items": marg_items,
              "marg_modales": marg_modales,
              "id_source": {n: k + 1 for k, n in
                            enumerate(I.SOURCES + ["humains vague 2"])}})
    ctxt = mp.get_context("fork")

    # ------------------------------------------------- reference par bloc
    print("\n--- reference par bloc ---", flush=True)
    taches_ref = []
    for camp in ("gauche", "droite"):
        for fr in FRACTIONS_REF:
            m = int(round(fr * effectifs[camp]))
            for b in range(args.reference):
                taches_ref.append((camp, m, b, args.nul))
    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        refc = pd.DataFrame(pool.map(tache_reference_camp, taches_ref, chunksize=8))
        print(f"reference par bloc : {time.time() - t:.0f} s", flush=True)

    # valeur pleine du bloc, et s0 au plein effectif par loi de puissance
    lignes_ref, s0_camp, ref_camp = [], {}, {}
    for camp in ("gauche", "droite"):
        li = np.flatnonzero(ctx["blocs"] == camp)
        plein = I.statistiques(codes_h[li], {**ctx, "seg": ctx["seg"][li]},
                               np.random.default_rng([J.GRAINE, 17]), n_nul=40)
        for cle in ("A", "B", "C"):
            xs, ys = [], []
            for fr in FRACTIONS_REF:
                m = int(round(fr * effectifs[camp]))
                dsub = refc[(refc.camp == camp) & (refc.taille == m)]
                v = dsub[cle].values
                fpc = J.correction_population_finie(m, effectifs[camp])
                bas, haut, et = J.ic_pivote(v, centre=float(np.mean(v)))
                vn = float(np.mean(dsub[f"se_nul_{cle}"].values ** 2))
                s0c = float(np.sqrt(max(et ** 2 - vn, 1e-24) * fpc ** 2 + vn))
                lignes_ref.append({"camp": camp, "taille": m, "statistique": cle,
                                   "valeur": float(np.mean(v)), "ic_bas": bas,
                                   "ic_haut": haut, "facteur_population_finie": fpc,
                                   "variance_du_nul_interieur": vn,
                                   "s0_naif": et * fpc, "s0": s0c,
                                   "n_tirages": int(len(v))})
                xs.append(np.log(m))
                ys.append(np.log(max(s0c, 1e-12)))
            pente, ordo = np.polyfit(np.array(xs), np.array(ys), 1)
            s0_camp[(camp, cle)] = float(np.exp(ordo) * effectifs[camp] ** pente)
            ref_camp[(camp, cle)] = float(plein[cle])
            lignes_ref.append({"camp": camp, "taille": effectifs[camp],
                               "statistique": cle, "valeur": float(plein[cle]),
                               "ic_bas": np.nan, "ic_haut": np.nan,
                               "facteur_population_finie": np.nan,
                               "variance_du_nul_interieur": np.nan, "s0_naif": np.nan,
                               "s0": s0_camp[(camp, cle)], "n_tirages": 0})
    J.ecrire(pd.DataFrame(lignes_ref), "i3b-camp-reference.csv")

    # reference globale a 1 052, relue du fichier de l'abaque
    chemin = os.path.join(J.SORTIE, "i3b-reference-par-taille.csv")
    if not os.path.exists(chemin):
        sys.exit("i3b-reference-par-taille.csv absent : lancer i3b_abaque.py d'abord.")
    rg = pd.read_csv(chemin)
    rg = rg[rg.taille == codes_h.shape[0]]
    s0_glob = {r.statistique: r.s0 for r in rg.itertuples()}
    ref_glob = {r.statistique: r.valeur for r in rg.itertuples()}

    # ------------------------------------------------------------- melanges
    print("\n--- melanges concentres et uniformes ---", flush=True)
    taches = []
    for nom in sources + (["humains vague 2"] if "humains vague 2" in src else []):
        for camp in ("droite", "gauche"):
            if camp == "gauche" and nom not in SOURCES_SECOND_CAMP:
                continue
            dispo = len(np.intersect1d(lignes[nom],
                                       np.flatnonzero(ctx["blocs"] == camp)))
            for tau in TAUX_CAMP:
                if int(round(tau * codes_h.shape[0])) > dispo:
                    continue
                for d in range(args.tirages):
                    taches.append((nom, camp, tau, d, "concentre", args.nul))
        for tau in TAUX_CAMP:
            if int(round(tau * codes_h.shape[0])) > len(lignes[nom]):
                continue
            for d in range(args.tirages):
                taches.append((nom, CAMP_PRIMAIRE, tau, d, "uniforme", args.nul))
    print(f"{len(taches)} flux", flush=True)
    t = time.time()
    with ctxt.Pool(args.procs) as pool:
        mel = pd.DataFrame(pool.map(tache_melange, taches, chunksize=2))
    print(f"melanges : {time.time() - t:.0f} s", flush=True)
    J.ecrire(mel, "i3b-camp-melanges.csv")

    # ------------------------------------------------------------- detection
    lignes_det = []
    for (nom, camp, mode), d in mel.groupby(["source", "camp", "mode"]):
        for lecture in ("global", "camp"):
            for cle in ("A", "B", "C"):
                col = f"{lecture}_{cle}"
                base = ref_glob[cle] if lecture == "global" else ref_camp[(camp, cle)]
                s = s0_glob[cle] if lecture == "global" else s0_camp[(camp, cle)]
                taux = sorted(d.taux.unique())
                moy = [float(d[d.taux == t][col].mean()) for t in taux]
                a, b, r2 = J.ajuster_courbe([0.0] + taux, [0.0] + [m - base for m in moy])
                for t, m in zip(taux, moy):
                    z = (m - base) / s if s else np.nan
                    lignes_det.append({
                        "source": nom, "camp": camp, "mode": mode, "lecture": lecture,
                        "statistique": cle, "taux_total": t, "valeur_moyenne": m,
                        "reference": base, "s0": s, "z": z,
                        "p_bilateral": J.p_bilateral(z) if np.isfinite(z) else np.nan,
                        "puissance_empirique": float(
                            (np.abs(d[d.taux == t][col].values - base) > J.Z_F1 * s).mean()),
                        "n_tirages": int((d.taux == t).sum()),
                        "tau_etoile_holm3": J.racine_courbe(
                            a, b, (J.Z_F1 + J.Z_PUISSANCE) * s),
                        "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    det = pd.DataFrame(lignes_det)
    J.ecrire(det, "i3b-camp-detection.csv")

    # --------------------------------------------------------- consequence
    lignes_c = []
    base_pol = float(pd.read_csv(chemin).query("taille == 1052 and "
                                               "statistique == 'polarisation'")
                     .valeur.iloc[0])
    bases = {"polarisation": base_pol}
    for r, (j, mod) in enumerate(zip(marg_items, marg_modales)):
        bases[f"marginale{r + 1}"] = J.part_modale(codes_h, j, mod)
    for (nom, camp, mode), d in mel.groupby(["source", "camp", "mode"]):
        for q, base in bases.items():
            taux = sorted(d.taux.unique())
            for t in taux:
                v = d[d.taux == t][q].values
                lignes_c.append({"source": nom, "camp": camp, "mode": mode,
                                 "quantite": q, "taux_total": t,
                                 "valeur_humaine": base, "valeur": float(v.mean()),
                                 "ecart": float(v.mean()) - base,
                                 "facteur": float(v.mean()) / base if base else np.nan,
                                 "ic_bas": float(np.percentile(v, 2.5)),
                                 "ic_haut": float(np.percentile(v, 97.5)),
                                 "n_tirages": int(len(v))})
    J.ecrire(pd.DataFrame(lignes_c), "i3b-camp-polarisation.csv")
    print(f"\ntotal {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
