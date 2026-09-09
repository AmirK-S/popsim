"""
i3b_adversaire : le fabricant qui vise la bande, construit et mesure, et la famille de
statistiques dont une partie reste en reserve.

===========================================================================
PREENREGISTREMENT : resultats/i3b-preenregistrement.md, ecrit le 8 septembre 2026 a
21 h 05 CEST, AVANT ce script et avant tout calcul de resultat.

QUESTION POSEE
--------------
i3 section 7.3 point 2 affirme qu'un fabricant qui viserait la valeur humaine des trois
statistiques ne serait pas detecte, et le classe [HYPOTHESE] : « c'est un raisonnement, pas
une mesure ». Ce script le construit, mesure s'il tombe reellement dans la bande, mesure
s'il reste vu par une statistique gardee en reserve, et mesure ce qu'il coute.

LA PARTITION, declaree au preenregistrement section 7
  H_A, 526 personnes : le fond du flux.
  H_B, 263 personnes : les microdonnees de reference de l'AUDITEUR, pour R2.
  H_C, 263 personnes : les microdonnees volees de l'ADVERSAIRE, pour A**.
Les trois sont disjointes. Le flux travaille donc a N = 526, et la reference des cinq
statistiques est prise sur 300 partitions aleatoires du meme type.

LES DEUX FAMILLES
  publiee : A, B, C, celles de i3, que l'adversaire connait et vise ;
  reserve : R1, structure de correlation a l'ordre trois, gratuite pour l'auditeur ;
            R2, distance au plus proche voisin humain, qui coute a l'auditeur de vraies
            microdonnees.

SORTIES, toutes dans resultats/
-------------------------------
  i3b-adversaire-reference.csv    la bande des cinq statistiques a N = 526
  i3b-adversaire-calibration.csv  la grille (m, rho, beta) et le point retenu
  i3b-adversaire-detection.csv    z, p de Holm et tau* des cinq statistiques

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/i3b_adversaire.py
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
N_A, N_B, N_C = 526, 263, 263
GRILLE_M = [2, 3, 5, 8, 12, 20]
GRILLE_RHO = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60]
GRILLE_BETA = [0.8, 0.9, 1.0, 1.1, 1.2]
GRILLE_RHO_MICRO = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
STATS = ["A", "B", "C", "R1", "R2"]


def cinq_statistiques(codes, seg, ctx, reference_humaine, rng, n_nul):
    """Les trois publiees et les deux de reserve, sur un flux de taille quelconque.

    R1 est publiee en exces sur le generateur nul du flux, exactement comme B. R2 ne
    depend pas du nul : c'est une distance a un echantillon humain externe.
    """
    ctxn = {**ctx, "seg": seg}
    st = I.statistiques(codes, ctxn, rng, n_nul=n_nul)
    r1_obs, n_trip = J.r1_ordre_trois(codes, seg, ctx["triplets"])
    cum, _, _ = C44.lois_par_segment(codes, seg, ctx["k_items"])
    nuls = []
    for _ in range(n_nul):
        z = C44.tirer_nul(codes, seg, cum, rng)
        nuls.append(J.r1_ordre_trois(z, seg, ctx["triplets"])[0])
    r2, r2_p10 = J.r2_plus_proche_voisin(codes, reference_humaine)
    return {"A": st["A"], "B": st["B"], "C": st["C"],
            "R1": r1_obs - float(np.mean(nuls)), "R1_brut": r1_obs,
            "R1_nul": float(np.mean(nuls)), "n_triplets": n_trip,
            "R2": r2, "R2_p10": r2_p10,
            "se_nul_A": (st["patrons_nul_et"] / np.sqrt(n_nul)
                         / max(st["patrons_nul"], 1e-9)) if n_nul > 1 else 0.0,
            "se_nul_B": st["q5_nul_et"] / np.sqrt(n_nul) if n_nul > 1 else 0.0,
            "se_nul_C": 0.0,
            "se_nul_R1": (float(np.std(nuls, ddof=1)) / np.sqrt(n_nul)
                          if n_nul > 1 else 0.0),
            "se_nul_R2": 0.0}


# ---------------------------------------------------------------------------

def tache_reference(b):
    """Une partition aleatoire du meme type que la partition declaree : 526 de fond,
    263 de reference d'auditeur. Donne la bande des cinq statistiques."""
    rng = np.random.default_rng([J.GRAINE, 401, b])
    perm = rng.permutation(G["n_total"])
    a, bb = np.sort(perm[:N_A]), np.sort(perm[N_A:N_A + N_B])
    st = cinq_statistiques(G["codes_h"][a], G["ctx"]["seg"][a], G["ctx"],
                           G["codes_h"][bb], rng, G["n_nul"])
    st["tirage"] = b
    return st


def _fabriquer(nom, rng, m_arch=None, rho=None, beta=None):
    """La matrice de la source sur les lignes de H_A, masque de H_A."""
    if nom == "A*":
        cum = G["cum_beta"][beta]
        return J.adversaire_archetypes(G["codes_a"], G["seg_a"], cum, m_arch, rho, rng)
    if nom == "A**":
        cum = G["cum_beta"][beta]
        return J.adversaire_microdonnees(G["codes_a"], G["seg_a"], G["seg_c"],
                                         G["codes_c"], cum, rho, rng)
    if nom == "B0 segment":
        z = C44.tirer_nul(G["codes_a"], G["seg_a"], G["cum_a"], rng)
        z[G["codes_a"] < 0] = -1
        return z
    return G["src_a"][nom]


def tache_calibration(arg):
    """Un point de la grille, population entierement fabriquee, taille N_A."""
    genre, m_arch, rho, beta, d = arg
    rng = np.random.default_rng([J.GRAINE, 403, m_arch or 0, int(rho * 100),
                                 int(beta * 100), d, 0 if genre == "A*" else 1])
    x = _fabriquer(genre, rng, m_arch=m_arch, rho=rho, beta=beta)
    ctxn = {**G["ctx"], "seg": G["seg_a"]}
    st = I.statistiques(x, ctxn, rng, n_nul=G["n_nul_cal"])
    return {"genre": genre, "m": m_arch, "rho": rho, "beta": beta, "tirage": d,
            "A": st["A"], "B": st["B"], "C": st["C"]}


def tache_melange(arg):
    nom, etiquette, m_arch, rho, beta, tau, d = arg
    rng = np.random.default_rng([J.GRAINE, 409, G["id"][etiquette],
                                 int(tau * 10000), d])
    x = _fabriquer(nom, rng, m_arch=m_arch, rho=rho, beta=beta)
    f, _ = I.flux(G["codes_a"], x, np.arange(N_A), tau, rng)
    st = cinq_statistiques(f, G["seg_a"], G["ctx"], G["codes_b"], rng, G["n_nul"])
    st.update({"source": etiquette, "taux": tau, "tirage": d})
    return st


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=15)
    ap.add_argument("--nul", type=int, default=12)
    ap.add_argument("--nul-calibration", type=int, default=8)
    ap.add_argument("--calibration-tirages", type=int, default=2)
    ap.add_argument("--reference", type=int, default=300)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.tirages, args.nul, args.nul_calibration = 3, 4, 3
        args.reference, args.calibration_tirages = 15, 1

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paquet = I.charger(args.cache, args.cache_foret, args.cache_a35)
    ctx = I.contexte(paquet)
    codes_h, _ = C44.coder(paquet["M"]["humains vague 1"], ctx["alpha"])
    n = codes_h.shape[0]
    ctx["triplets"] = J.triplets(len(ctx["items"]))

    src = {}
    for nom in ("agents v8", "PMM k=10", "E2 regression contexte tirage"):
        if nom in paquet["M"]:
            brut, _ = C44.coder(paquet["M"][nom], ctx["alpha"])
            src[nom], _ = I.masquer_commun(brut, codes_h)

    # La partition declaree, tiree a la graine du projet, une fois pour toutes.
    rng = np.random.default_rng([J.GRAINE, 5])
    perm = rng.permutation(n)
    HA, HB, HC = (np.sort(perm[:N_A]), np.sort(perm[N_A:N_A + N_B]),
                  np.sort(perm[N_A + N_B:N_A + N_B + N_C]))
    print(f"partition : H_A {len(HA)}, H_B {len(HB)}, H_C {len(HC)}, "
          f"intersections {len(np.intersect1d(HA, HB))} / "
          f"{len(np.intersect1d(HA, HC))} / {len(np.intersect1d(HB, HC))}", flush=True)

    # Les marginales publiees : celles de la population entiere, ce que publie un sondage.
    cum_pub = {b: J.lois_p(codes_h, ctx["seg"], ctx["k_items"], beta=b)[0]
               for b in GRILLE_BETA}
    cum_a, _, _ = C44.lois_par_segment(codes_h[HA], ctx["seg"][HA], ctx["k_items"])

    G.update({"codes_h": codes_h, "n_total": n, "ctx": ctx, "n_nul": args.nul,
              "n_nul_cal": args.nul_calibration,
              "codes_a": codes_h[HA], "codes_b": codes_h[HB], "codes_c": codes_h[HC],
              "seg_a": ctx["seg"][HA], "seg_c": ctx["seg"][HC],
              "cum_beta": cum_pub, "cum_a": cum_a,
              "src_a": {k: v[HA] for k, v in src.items()}})
    ctxt = mp.get_context("fork")

    # --------------------------------------------------------- la bande a N = 526
    print("\n--- la bande des cinq statistiques, 300 partitions ---", flush=True)
    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        ref = pd.DataFrame(pool.map(tache_reference, range(args.reference), chunksize=4))
        print(f"reference : {time.time() - t:.0f} s", flush=True)
    fpc = J.correction_population_finie(N_A, n)
    lignes_ref, refv, s0 = [], {}, {}
    for cle in STATS:
        v = ref[cle].values
        bas, haut, et = J.ic_pivote(v, centre=float(np.mean(v)))
        vn = float(np.mean(ref[f"se_nul_{cle}"].values ** 2))
        s0c = float(np.sqrt(max(et ** 2 - vn, 1e-24) * fpc ** 2 + vn))
        refv[cle], s0[cle] = float(np.mean(v)), s0c
        lignes_ref.append({"statistique": cle, "taille": N_A,
                           "valeur": refv[cle], "ic_bas": bas, "ic_haut": haut,
                           "ecart_type_partitions": et, "facteur_population_finie": fpc,
                           "variance_du_nul_interieur": vn, "s0_naif": et * fpc,
                           "s0": s0c, "n_tirages": int(len(v))})
    ref_df = pd.DataFrame(lignes_ref)
    J.ecrire(ref_df, "i3b-adversaire-reference.csv")
    print(ref_df[["statistique", "valeur", "ic_bas", "ic_haut", "s0"]]
          .to_string(index=False), flush=True)

    # ------------------------------------------------------------ calibration
    print("\n--- calibration du fabricant qui vise la bande ---", flush=True)
    taches = [("A*", m, r, b, d) for m in GRILLE_M for r in GRILLE_RHO
              for b in GRILLE_BETA for d in range(args.calibration_tirages)]
    taches += [("A**", None, r, b, d) for r in GRILLE_RHO_MICRO for b in GRILLE_BETA
               for d in range(args.calibration_tirages)]
    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        cal = pd.DataFrame(pool.map(tache_calibration, taches, chunksize=4))
        print(f"calibration : {time.time() - t:.0f} s, {len(taches)} points", flush=True)
    g = cal.groupby(["genre", "m", "rho", "beta"], dropna=False)[["A", "B", "C"]].mean()
    g = g.reset_index()
    g["ecart_A"] = (g.A - refv["A"]).abs() / s0["A"]
    g["ecart_B"] = (g.B - refv["B"]).abs() / s0["B"]
    g["ecart_C"] = (g.C - refv["C"]).abs() / s0["C"]
    g["critere_deux_cibles"] = g[["ecart_A", "ecart_B"]].max(axis=1)
    g["critere_trois_cibles"] = g[["ecart_A", "ecart_B", "ecart_C"]].max(axis=1)
    J.ecrire(g.sort_values("critere_deux_cibles"), "i3b-adversaire-calibration.csv")

    ga = g[g.genre == "A*"]
    gm = g[g.genre == "A**"]
    p2 = ga.loc[ga.critere_deux_cibles.idxmin()]
    p3 = ga.loc[ga.critere_trois_cibles.idxmin()]
    pm = gm.loc[gm.critere_deux_cibles.idxmin()]
    for nom, p in (("A* deux cibles", p2), ("A* trois cibles", p3),
                   ("A** microdonnees", pm)):
        print(f"{nom} : m = {p.m}, rho = {p.rho}, beta = {p.beta} ; "
              f"A = {p.A:+.5f} ({p.ecart_A:.2f} s0), B = {p.B:+.5f} "
              f"({p.ecart_B:.2f} s0), C = {p.C:.5f} ({p.ecart_C:.2f} s0)", flush=True)

    # ------------------------------------------------------------- melanges
    print("\n--- melanges des adversaires ---", flush=True)
    fabricants = [
        ("A*", "A* deux cibles", int(p2.m), float(p2.rho), float(p2.beta)),
        ("A*", "A* trois cibles", int(p3.m), float(p3.rho), float(p3.beta)),
        ("A**", "A** microdonnees", None, float(pm.rho), float(pm.beta)),
        ("B0 segment", "B0 segment", None, None, 1.0),
    ]
    for nom in ("agents v8", "PMM k=10", "E2 regression contexte tirage"):
        if nom in src:
            fabricants.append((nom, nom, None, None, 1.0))
    G["id"] = {f[1]: k + 1 for k, f in enumerate(fabricants)}
    taches = [(nom, et, m, r, b, tau, d) for nom, et, m, r, b in fabricants
              for tau in I.TAUX if tau > 0 for d in range(args.tirages)]
    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        mel = pd.DataFrame(pool.map(tache_melange, taches, chunksize=2))
        print(f"melanges : {time.time() - t:.0f} s, {len(taches)} flux", flush=True)
    J.ecrire(mel, "i3b-adversaire-melanges.csv")

    lignes = []
    for nom in sorted(set(mel.source)):
        d = mel[mel.source == nom]
        for cle in STATS:
            taux = sorted(d.taux.unique())
            moy = [float(d[d.taux == t][cle].mean()) for t in taux]
            a, b, r2 = J.ajuster_courbe([0.0] + taux,
                                        [0.0] + [m - refv[cle] for m in moy])
            for t, m in zip(taux, moy):
                z = (m - refv[cle]) / s0[cle] if s0[cle] else np.nan
                lignes.append({
                    "source": nom, "statistique": cle,
                    "famille": "publiee" if cle in ("A", "B", "C") else "reserve",
                    "taux": t, "valeur_moyenne": m, "reference": refv[cle],
                    "s0": s0[cle], "z": z,
                    "p_bilateral": J.p_bilateral(z) if np.isfinite(z) else np.nan,
                    "puissance_empirique": float(
                        (np.abs(d[d.taux == t][cle].values - refv[cle])
                         > J.Z_F3 * s0[cle]).mean()),
                    "n_tirages": int((d.taux == t).sum()),
                    "tau_etoile_holm5": J.racine_courbe(
                        a, b, (J.Z_F3 + J.Z_PUISSANCE) * s0[cle]),
                    "tau_etoile_nominal": J.racine_courbe(
                        a, b, (I.Z_ALPHA + J.Z_PUISSANCE) * s0[cle]),
                    "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    det = pd.DataFrame(lignes)
    # Holm sur la famille F3, cinq tests par source au taux 5 pour cent
    for nom in sorted(set(det.source)):
        m = (det.source == nom) & (det.taux == 0.05)
        det.loc[m, "p_holm"] = J.holm(det.loc[m, "p_bilateral"].values)
    J.ecrire(det, "i3b-adversaire-detection.csv")

    print("\n=== resume, taux 5 pour cent ===", flush=True)
    print(det[det.taux == 0.05][["source", "statistique", "z", "p_holm",
                                 "tau_etoile_holm5"]]
          .round(4).to_string(index=False), flush=True)
    print(f"\ntotal {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
