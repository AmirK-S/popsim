"""
i3_melanges : le detecteur non supervise de population synthetique, execute.

===========================================================================
PREENREGISTREMENT : resultats/i3-preenregistrement.md, ecrit le 8 septembre 2026 a
19 h 12 CEST, AVANT ce script et avant tout calcul. Les sources, la regle de melange, les
cinq taux, les trois statistiques, la segmentation, le mode de reechantillonnage, la
formule de puissance, la famille de tests et les sept predictions y sont figes. Ce script
ne fait que les executer.

QUESTION POSEE
--------------
Un institut recoit un fichier de reponses fermees dont une part est fabriquee. Sans
etiquette de provenance, sans exemple etiquete, sans texte libre, peut il dire qu'il y a du
synthetique, et combien ?

SORTIES, toutes dans resultats/
-------------------------------
  i3-controles.csv         les cinq controles bloquants du preenregistrement section 8
  i3-reference-humaine.csv la valeur des trois statistiques sur le flux pur, avec IC
  i3-melanges.csv          les courbes, source x taux x statistique
  i3-puissance.csv         le plus petit taux detectable et la puissance empirique
  i3-quantification.csv    l'estimateur du taux, calibration propre et calibration croisee
  i3-polarisation.csv      I4, l'ecart gauche droite en fonction du taux
  et un resume imprime sur la sortie standard.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/i3_melanges.py
===========================================================================
"""

import argparse
import os
import sys
import time

# Un thread par processus : quatre processus fils occupent les quatre coeurs.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "1"

import multiprocessing as mp

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a44_commun as C44
import i3_commun as I

G = {}   # etat partage avec les processus fils par fork


# ---------------------------------------------------------------------------
# Taches paralleles
# ---------------------------------------------------------------------------

def _source_codes(nom, rng):
    """Matrice codee de la source, deja restreinte au masque commun.

    `B0 segment` est stochastique par definition : chaque faux repondant est un tirage
    independant dans les marginales de son segment, donc la matrice est regeneree a chaque
    tirage de melange.
    """
    if nom == "B0 segment":
        z = C44.tirer_nul(G["codes_h"], G["ctx"]["seg"], G["cum_h"], rng)
        z[G["codes_h"] < 0] = -1
        return z
    return G["src"][nom]


def _id_source(nom):
    """Identifiant entier stable d'une source. hash() est randomise par processus en
    Python 3, il ne peut pas servir de graine reproductible."""
    return G["id_source"][nom]


def tache_melange(arg):
    nom, tau, tirage, n_nul = arg
    rng = np.random.default_rng([I.GRAINE, _id_source(nom), int(tau * 10000), tirage])
    src = _source_codes(nom, rng)
    f, choisies = I.flux(G["codes_h"], src, G["lignes"][nom], tau, rng)
    st = I.statistiques(f, G["ctx"], rng, n_nul=n_nul)
    pol, _, _ = I.polarisation(f, G["ctx"]["blocs"], signes=G["signes"])
    st.update({"source": nom, "taux": tau, "tirage": tirage,
               "n_remplacees": len(choisies), "polarisation": pol})
    return st


def tache_bootstrap_b(b):
    """Bootstrap classique sur les personnes pour la statistique B."""
    rng = np.random.default_rng([I.GRAINE, 71, b])
    n = G["codes_h"].shape[0]
    idx = rng.integers(0, n, size=n)
    c = G["codes_h"][idx]
    s = G["ctx"]["seg"][idx]
    q5, _ = C44.correlation_items(c, G["ctx"]["colonnes"], seg=s)
    cum, _, _ = C44.lois_par_segment(c, s, G["ctx"]["k_items"])
    nul = []
    for _ in range(G["r_boot"]):
        z = C44.tirer_nul(c, s, cum, rng)
        qn, _ = C44.correlation_items(z, G["ctx"]["colonnes"], seg=s)
        nul.append(qn)
    return q5 - float(np.mean(nul))


def tache_sous_echantillon(arg):
    """Sous echantillonnage sans remise a m personnes, pour A, B et C.

    Un tirage avec remise duplique des personnes ; il fait baisser mecaniquement le
    nombre de patrons distincts (a44, section 0), monter la concentration, et monter
    l'exces de correlation, parce qu'une ligne dupliquee est une co-variation parfaite
    entre tous les items que le generateur nul detruit. Le sous echantillonnage sans
    remise n'a aucun de ces trois defauts.
    """
    b, m, source_codes = arg
    rng = np.random.default_rng([I.GRAINE, 73, b, m])
    base = G["codes_h"] if source_codes is None else G[source_codes]
    n = base.shape[0]
    idx = rng.choice(n, size=m, replace=False)
    c = base[idx]
    s = G["ctx"]["seg"][idx]
    p, _ = C44.patrons_distincts(c, G["ctx"]["sous_ens"])
    co = I.concentration(c, s, G["ctx"]["sous_ens"])
    q5, _ = C44.correlation_items(c, G["ctx"]["colonnes"], seg=s)
    cum, _, _ = C44.lois_par_segment(c, s, G["ctx"]["k_items"])
    pn, cn, qn = [], [], []
    for _ in range(G["r_boot"]):
        z = C44.tirer_nul(c, s, cum, rng)
        pn.append(C44.patrons_distincts(z, G["ctx"]["sous_ens"])[0])
        qn.append(C44.correlation_items(z, G["ctx"]["colonnes"], seg=s)[0])
    return (p / float(np.mean(pn)) - 1.0, q5 - float(np.mean(qn)), co)


def tache_validation(k):
    """Controle 8.4 : une population independante tiree du nul humain, taille 1 052."""
    rng = np.random.default_rng([I.GRAINE, 79, k])
    z = C44.tirer_nul(G["codes_h"], G["ctx"]["seg"], G["cum_h"], rng)
    z[G["codes_h"] < 0] = -1
    st = I.statistiques(z, G["ctx"], rng, n_nul=G["r_valid"])
    return st["A"], st["B"], st["C"], (z if k == 0 else None)


def tache_pure(nom):
    """Controle 8.1 : la source pure, taux 100 pour cent, contre a44."""
    rng = np.random.default_rng([I.GRAINE, 83, _id_source(nom)])
    src = _source_codes(nom, rng)
    lignes = G["lignes"][nom]
    st = I.statistiques(src[lignes], G["ctx_par_perimetre"][len(lignes)], rng,
                        n_nul=G["r_pur"])
    st["source"] = nom
    st["n"] = len(lignes)
    return st


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=I.N_TIRAGES)
    ap.add_argument("--nul", type=int, default=I.N_NUL)
    ap.add_argument("--bootstrap", type=int, default=I.N_BOOTSTRAP)
    ap.add_argument("--r-boot", type=int, default=3)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.tirages, args.nul, args.bootstrap, args.r_boot = 3, 5, 30, 2

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paquet = I.charger(args.cache, args.cache_foret, args.cache_a35)
    ctx = I.contexte(paquet)
    print(f"{paquet['x'].shape[0]} personnes, {len(ctx['items'])} items ; "
          f"absentes : {paquet['absentes'] or 'aucune'}", flush=True)

    controles = []

    # ------------------------------------------------------- codage des sources
    codes_h, hors_h = C44.coder(paquet["M"]["humains vague 1"], ctx["alpha"])
    controles.append({"controle": "part de cellules hors nomenclature", "objet":
                      "humains vague 1", "valeur": round(hors_h, 6), "seuil": 0.005,
                      "passe": bool(hors_h < 0.005)})
    src, lignes, perte = {}, {}, {}
    for nom in I.SOURCES + ["humains vague 2"]:
        if nom == "B0 segment":
            lignes[nom] = np.arange(codes_h.shape[0])
            perte[nom] = 0.0
            continue
        if nom not in paquet["M"]:
            print(f"source absente, ignoree : {nom}", flush=True)
            continue
        brut, hors = C44.coder(paquet["M"][nom], ctx["alpha"])
        controles.append({"controle": "part de cellules hors nomenclature", "objet": nom,
                          "valeur": round(hors, 6), "seuil": 0.005,
                          "passe": bool(hors < 0.005)})
        lignes[nom] = (ctx["lignes150"] if nom in ("C2", "C3")
                       else np.arange(codes_h.shape[0]))
        m, _ = I.masquer_commun(brut, codes_h)
        src[nom] = m
        # La perte de cellules est lue sur les seules lignes ou la source existe : pour
        # C2 et C3, les 902 personnes hors du run local sont vides par construction et
        # ne sont jamais tirees dans un flux.
        li = lignes[nom]
        _, p = I.masquer_commun(brut[li], codes_h[li])
        perte[nom] = p
        controles.append({"controle": "cellules perdues par l'intersection des masques",
                          "objet": nom, "valeur": round(p, 6), "seuil": 0.005,
                          "passe": bool(p < 0.005)})

    sources = [s for s in I.SOURCES if s == "B0 segment" or s in src]
    cum_h, replis_h, total_h = C44.lois_par_segment(codes_h, ctx["seg"], ctx["k_items"])
    controles.append({"controle": "taux de repli du generateur nul, S_ideo",
                      "objet": "humains vague 1",
                      "valeur": round(replis_h / max(total_h, 1), 6), "seuil": 0.0,
                      "passe": bool(replis_h == 0)})

    # controle 8.2 : le flux a taux 0 est exactement la population humaine
    rng0 = np.random.default_rng(I.GRAINE)
    f0, _ = I.flux(codes_h, src.get("agents v8", codes_h), lignes["agents v8"], 0.0, rng0)
    ecart0 = int((f0 != codes_h).sum())
    controles.append({"controle": "le flux a taux 0 egale la population humaine",
                      "objet": "toutes sources", "valeur": ecart0, "seuil": 0,
                      "passe": bool(ecart0 == 0)})

    # controle 8.5 : melange des humains avec eux memes, a tous les taux
    ecart_neg = 0
    for tau in I.TAUX:
        fn, _ = I.flux(codes_h, codes_h, np.arange(codes_h.shape[0]), tau,
                       np.random.default_rng(I.GRAINE + 1))
        ecart_neg = max(ecart_neg, int((fn != codes_h).sum()))
    controles.append({"controle": "controle negatif, humains melanges a eux memes",
                      "objet": "cinq taux", "valeur": ecart_neg, "seuil": 0,
                      "passe": bool(ecart_neg == 0)})

    # --------------------------------------------------------------- etat partage
    _, signes, bon_pol = I.polarisation(codes_h, ctx["blocs"], signes=None)
    ctx150 = dict(ctx)
    ctx150 = {**ctx, "seg": ctx["seg"][ctx["lignes150"]]}
    toutes_sources = I.SOURCES + ["humains vague 2", "humains"]
    G["id_source"] = {nom: k + 1 for k, nom in enumerate(toutes_sources)}
    G.update({"codes_h": codes_h, "src": src, "lignes": lignes, "ctx": ctx,
              "cum_h": cum_h, "signes": signes, "r_boot": args.r_boot,
              "r_valid": args.nul, "r_pur": max(args.nul, 40),
              "ctx_par_perimetre": {codes_h.shape[0]: ctx,
                                    len(ctx["lignes150"]): ctx150}})
    ctxt = mp.get_context("fork")

    # ------------------------------------------------- reference humaine, taux 0
    print("\n--- reference humaine, flux pur ---", flush=True)
    ref = I.statistiques(codes_h, ctx, np.random.default_rng([I.GRAINE, 11]),
                         n_nul=max(args.nul * 5, 40))
    pol_ref, _, _ = I.polarisation(codes_h, ctx["blocs"], signes=signes)
    print(f"A = {ref['A']:+.4f}   B = {ref['B']:+.4f}   C = {ref['C']:.5f}   "
          f"P = {pol_ref:+.4f}", flush=True)

    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        b_boot = pool.map(tache_bootstrap_b, range(args.bootstrap), chunksize=8)
        print(f"bootstrap B : {time.time() - t:.0f} s", flush=True)
        m = codes_h.shape[0] // 2
        t = time.time()
        sous = pool.map(tache_sous_echantillon,
                        [(b, m, None) for b in range(args.bootstrap)], chunksize=8)
        print(f"sous echantillonnage A et C : {time.time() - t:.0f} s", flush=True)
        t = time.time()
        valid = pool.map(tache_validation, range(I.N_VALIDATION if not args.smoke else 8))
        print(f"controle 8.4 : {time.time() - t:.0f} s", flush=True)
        t = time.time()
        purs = pool.map(tache_pure, sources)
        print(f"controle 8.1, sources pures : {time.time() - t:.0f} s", flush=True)

    a_sous = np.array([x[0] for x in sous])
    b_sous = np.array([x[1] for x in sous])
    c_sous = np.array([x[2] for x in sous])
    echelle = np.sqrt(m / codes_h.shape[0])

    # bruit du nul interieur, ajoute en quadrature : la moyenne de R replicats nuls est
    # elle meme bruitee, et elle entre dans A et dans C_exces.
    se_nul_a = (ref["patrons_nul_et"] / np.sqrt(max(args.nul * 5, 40))
                / max(ref["patrons_nul"], 1e-9))
    se_nul_b = ref["q5_nul_et"] / np.sqrt(max(args.nul * 5, 40))

    # ECART E1 AU PREENREGISTREMENT, section 5. Le preenregistrement reservait le
    # bootstrap avec remise a la statistique B, en pensant que seules A et C etaient
    # sensibles aux doublons. La mesure montre que B l'est aussi, et fortement : une ligne
    # dupliquee est une co-variation parfaite entre tous les items, que le nul detruit.
    # Les trois references sont donc prises par sous echantillonnage sans remise a
    # m = N / 2, remis a l'echelle. La valeur du bootstrap avec remise est publiee a cote,
    # avec son biais mesure, parce que c'est elle qui etait preenregistree.
    biais_bootstrap = float(np.mean(b_boot)) - ref["B"]
    controles.append({"controle": "biais du bootstrap avec remise sur la statistique B",
                      "objet": "1 000 tirages", "valeur": round(biais_bootstrap, 6),
                      "seuil": "publie, non bloquant", "passe": True})

    reference = []
    for cle, tirages, ech, extra in (
            ("A", a_sous, echelle, se_nul_a),
            ("B", b_sous, echelle, se_nul_b),
            ("C", c_sous, echelle, 0.0)):
        bas, haut, et = I.ic_percentile(tirages, centre=ref[cle], echelle=ech)
        s0 = float(np.sqrt(et ** 2 + extra ** 2))
        reference.append({
            "statistique": cle, "libelle": I.LIBELLE_STAT[cle],
            "valeur": ref[cle], "ic_bas": bas, "ic_haut": haut,
            "ecart_type_reechantillonnage": et,
            "ecart_type_du_nul_interieur": extra,
            "s0": s0,
            "mode": "sous echantillonnage sans remise m = %d, remis a l'echelle" % m,
            "n_tirages": len(tirages),
            "valeur_bootstrap_avec_remise": (float(np.mean(b_boot)) if cle == "B"
                                             else np.nan),
            "biais_du_bootstrap_avec_remise": (biais_bootstrap if cle == "B"
                                               else np.nan)})
    ref_df = pd.DataFrame(reference)
    I.ecrire(ref_df, "i3-reference-humaine.csv")
    s0 = {r["statistique"]: r["s0"] for r in reference}
    ref_val = {r["statistique"]: r["valeur"] for r in reference}
    ic = {r["statistique"]: (r["ic_bas"], r["ic_haut"]) for r in reference}

    # ---- controle 8.4, validite de la mise a l'echelle
    a_val = np.array([v[0] for v in valid])
    b_val = np.array([v[1] for v in valid])
    c_val = np.array([v[2] for v in valid])
    z0 = [v[3] for v in valid if v[3] is not None][0]
    G["z0"] = z0
    with ctxt.Pool(args.procs) as pool:
        sous_z = pool.map(tache_sous_echantillon,
                          [(b, m, "z0") for b in range(200 if not args.smoke else 20)],
                          chunksize=4)
    a_sz = np.array([x[0] for x in sous_z]) * echelle
    b_sz = np.array([x[1] for x in sous_z]) * echelle
    c_sz = np.array([x[2] for x in sous_z]) * echelle
    for cle, direct, sousech in (("A", a_val, a_sz), ("B", b_val, b_sz),
                                 ("C", c_val, c_sz)):
        r = float(sousech.std(ddof=1) / direct.std(ddof=1)) if direct.std(ddof=1) > 0 \
            else np.nan
        controles.append({
            "controle": f"validite de la mise a l'echelle du sous echantillonnage, {cle}",
            "objet": f"K = {len(direct)} populations nulles independantes",
            "valeur": round(r, 4), "seuil": "entre 0,7 et 1,4",
            "passe": bool(np.isfinite(r) and 0.7 <= r <= 1.4)})

    # ---- controle 8.1, reproduction de a44 sur les sources pures
    a44_patrons = {"agents v8": -0.321, "agents demographiques (v6)": -0.230,
                   "agents composite": -0.182, "PMM k=10": -0.098,
                   "C2": -0.162, "C3": -0.138}
    a44_q5 = {"agents v8": 0.0942, "agents demographiques (v6)": 0.0926,
              "agents composite": 0.0838, "PMM k=10": 0.0558,
              "C2": 0.0467, "C3": 0.0546}
    for p in purs:
        nom = p["source"]
        if nom in a44_patrons:
            d = abs(p["A"] - a44_patrons[nom])
            controles.append({"controle": "reproduction de a44, tableau 3, deficit de "
                                          "patrons", "objet": nom,
                              "valeur": round(d, 5), "seuil": 0.005,
                              "passe": bool(d < 0.005)})
        if nom in a44_q5:
            d = abs(p["B"] - a44_q5[nom])
            controles.append({"controle": "reproduction de a44, tableau 4, exces de "
                                          "correlation", "objet": nom,
                              "valeur": round(d, 5), "seuil": 0.005,
                              "passe": bool(d < 0.005)})
    pur_df = pd.DataFrame([{**{k: v for k, v in p.items()}, } for p in purs])

    ctrl_df = pd.DataFrame(controles)
    I.ecrire(ctrl_df, "i3-controles.csv")
    print("\ncontroles :", flush=True)
    print(ctrl_df.to_string(index=False, max_colwidth=60), flush=True)
    if not ctrl_df["passe"].all():
        print("\n*** au moins un controle ne passe pas ; le rapport doit le dire en "
              "premier ***", flush=True)

    # ------------------------------------------------------------- les melanges
    print("\n--- melanges ---", flush=True)
    taches = []
    for nom in sources:
        for tau in I.TAUX_SOURCE[nom]:
            if tau == 0.0:
                continue
            for d in range(args.tirages):
                taches.append((nom, tau, d, args.nul))
    # controle descriptif ajoute : la vague 2, de vraies personnes, comme fausse source
    if "humains vague 2" in src:
        for tau in I.TAUX:
            if tau == 0.0:
                continue
            for d in range(args.tirages):
                taches.append(("humains vague 2", tau, d, args.nul))
        lignes["humains vague 2"] = np.arange(codes_h.shape[0])
        G["lignes"] = lignes
    print(f"{len(taches)} flux a calculer", flush=True)
    t = time.time()
    with ctxt.Pool(args.procs) as pool:
        res = pool.map(tache_melange, taches, chunksize=2)
    print(f"melanges : {time.time() - t:.0f} s", flush=True)
    mel = pd.DataFrame(res)

    # la ligne taux 0, commune a toutes les sources
    ligne0 = {"source": "tous", "taux": 0.0, "tirage": -1, "n_remplacees": 0,
              "polarisation": pol_ref,
              **{k: ref[k] for k in ref if k in
                 ("A", "B", "C", "C_exces", "C5", "C5_exces", "patrons", "patrons_nul",
                  "q5", "q5_nul", "q4", "conc_nul", "n_lignes_patrons", "n_paires")}}
    mel = pd.concat([pd.DataFrame([ligne0]), mel], ignore_index=True)
    I.ecrire(mel, "i3-melanges.csv")

    # ------------------------------------------------------- puissance et taux*
    print("\n--- puissance ---", flush=True)
    lignes_p = []
    courbes = {}
    for nom in sorted(set(mel.source) - {"tous"}):
        d = mel[mel.source == nom]
        for cle in I.CLES_STAT:
            if cle not in ("A", "B", "C"):
                continue
            taux = sorted(d.taux.unique())
            moyennes = [float(d[d.taux == t][cle].mean()) for t in taux]
            ecarts = [mu - ref_val[cle] for mu in moyennes]
            a, b, r2 = I.ajuster_courbe([0.0] + taux, [0.0] + ecarts)
            courbes[(cle, nom)] = (a, b, r2)
            cible_nom = (I.Z_ALPHA + I.Z_PUISSANCE) * s0[cle]
            cible_holm = (I.Z_HOLM + I.Z_PUISSANCE) * s0[cle]
            for t, mu in zip(taux, moyennes):
                sd = d[d.taux == t][cle]
                puissance = float(((sd < ic[cle][0]) | (sd > ic[cle][1])).mean())
                z = (mu - ref_val[cle]) / s0[cle] if s0[cle] > 0 else np.nan
                lignes_p.append({
                    "source": nom, "famille": I.FAMILLE.get(nom, "humain"),
                    "statistique": cle, "taux": t,
                    "valeur_moyenne": mu, "ecart_a_la_reference": mu - ref_val[cle],
                    "z": z, "p_bilateral": I.p_bilateral_normale(z)
                    if np.isfinite(z) else np.nan,
                    "puissance_empirique": puissance,
                    "n_tirages": int(len(sd)),
                    "taux_detectable_alpha5": I.racine_courbe(a, b, cible_nom),
                    "taux_detectable_holm27": I.racine_courbe(a, b, cible_holm),
                    "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    puis = pd.DataFrame(lignes_p)

    # correction de Holm sur la famille primaire : 3 statistiques x sources, taux 5 %
    prim = puis[(puis.taux == 0.05) & (puis.source.isin(sources))].copy()
    prim = prim.sort_values(["statistique", "source"]).reset_index(drop=True)
    prim["p_holm"] = I.holm(prim["p_bilateral"].values)
    puis = puis.merge(prim[["source", "statistique", "taux", "p_holm"]],
                      on=["source", "statistique", "taux"], how="left")
    I.ecrire(puis, "i3-puissance.csv")

    # ---------------------------------------------------------- quantification
    print("\n--- quantification ---", flush=True)
    lignes_q = []
    llm = [s for s in sources if I.FAMILLE.get(s, "").startswith("modele")]
    for cle in ("A", "B", "C"):
        agn = [courbes[(cle, s)] for s in llm if (cle, s) in courbes]
        a_agn = float(np.mean([c[0] for c in agn])) if agn else np.nan
        b_agn = float(np.mean([c[1] for c in agn])) if agn else np.nan
        for nom in sorted(set(mel.source) - {"tous"}):
            d = mel[mel.source == nom]
            calibrations = [("propre", nom)] + \
                           [("croisee", s) for s in sorted(set(mel.source) - {"tous", nom})]
            for genre, cal in calibrations:
                if (cle, cal) not in courbes:
                    continue
                a, b, _ = courbes[(cle, cal)]
                err = []
                for t in sorted(d.taux.unique()):
                    v = d[d.taux == t][cle].values
                    est = np.array([I.inverser_courbe(a, b, x - ref_val[cle]) for x in v])
                    err.append((t, est))
                for t, est in err:
                    lignes_q.append({
                        "statistique": cle, "source_evaluee": nom,
                        "calibration": genre, "source_calibration": cal,
                        "taux_vrai": t, "taux_estime_median": float(np.median(est)),
                        "erreur_absolue_mediane": float(np.median(np.abs(est - t))),
                        "erreur_quadratique_moyenne":
                            float(np.sqrt(np.mean((est - t) ** 2))),
                        "n_tirages": int(len(est))})
            if np.isfinite(a_agn):
                for t in sorted(d.taux.unique()):
                    v = d[d.taux == t][cle].values
                    est = np.array([I.inverser_courbe(a_agn, b_agn, x - ref_val[cle])
                                    for x in v])
                    lignes_q.append({
                        "statistique": cle, "source_evaluee": nom,
                        "calibration": "agnostique", "source_calibration":
                            "moyenne des sources a modele de langage",
                        "taux_vrai": t, "taux_estime_median": float(np.median(est)),
                        "erreur_absolue_mediane": float(np.median(np.abs(est - t))),
                        "erreur_quadratique_moyenne":
                            float(np.sqrt(np.mean((est - t) ** 2))),
                        "n_tirages": int(len(est))})
    quant = pd.DataFrame(lignes_q)
    I.ecrire(quant, "i3-quantification.csv")

    # ------------------------------------------------------------------- I4
    print("\n--- I4, polarisation ---", flush=True)
    with ctxt.Pool(args.procs) as pool:
        pol_boot = pool.map(tache_polarisation_bootstrap,
                            range(400 if not args.smoke else 30), chunksize=4)
    pb = np.asarray(pol_boot)
    pol_bas, pol_haut = float(np.percentile(pb, 2.5)), float(np.percentile(pb, 97.5))
    lignes_i4 = [{"source": "humains purs", "famille": "humain", "taux": 0.0,
                  "polarisation": pol_ref, "facteur": 1.0,
                  "ic_bas": pol_bas, "ic_haut": pol_haut, "n_tirages": len(pb),
                  "n_items_retenus": int(bon_pol.sum())}]
    for nom in sorted(set(mel.source) - {"tous"}):
        d = mel[mel.source == nom]
        for t in sorted(d.taux.unique()):
            v = d[d.taux == t]["polarisation"].values
            lignes_i4.append({
                "source": nom, "famille": I.FAMILLE.get(nom, "humain"), "taux": t,
                "polarisation": float(np.mean(v)),
                "facteur": float(np.mean(v)) / pol_ref if pol_ref else np.nan,
                "ic_bas": float(np.percentile(v, 2.5)),
                "ic_haut": float(np.percentile(v, 97.5)),
                "n_tirages": int(len(v)),
                "n_items_retenus": int(bon_pol.sum())})
    i4 = pd.DataFrame(lignes_i4)
    I.ecrire(i4, "i3-polarisation.csv")
    I.ecrire(pur_df, "i3-sources-pures.csv")

    # --------------------------------------------------------------- resume
    print("\n=== resume ===", flush=True)
    print(ref_df[["statistique", "valeur", "ic_bas", "ic_haut", "s0"]]
          .round(5).to_string(index=False), flush=True)
    for cle in ("A", "B", "C"):
        print(f"\n{cle} : {I.LIBELLE_STAT[cle]}", flush=True)
        piv = puis[puis.statistique == cle].pivot_table(
            index="source", columns="taux", values="valeur_moyenne")
        print(piv.round(4).to_string(), flush=True)
        tt = puis[(puis.statistique == cle)].groupby("source")[
            ["taux_detectable_alpha5", "taux_detectable_holm27"]].first()
        print(tt.round(4).to_string(), flush=True)
    print(f"\ntotal {time.time() - t0:.0f} s", flush=True)


def tache_polarisation_bootstrap(b):
    rng = np.random.default_rng([I.GRAINE, 91, b])
    n = G["codes_h"].shape[0]
    idx = rng.integers(0, n, size=n)
    p, _, _ = I.polarisation(G["codes_h"][idx], G["ctx"]["blocs"][idx],
                             signes=G["signes"])
    return p


if __name__ == "__main__":
    main()
