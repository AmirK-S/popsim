"""
i3b_twin : la meme chaine de detection sur Twin-2K-500. Autre questionnaire, autres
personnes, autres auteurs, autres modeles. La bande humaine est elle la meme ?

===========================================================================
PREENREGISTREMENT : resultats/i3b-preenregistrement.md, ecrit le 8 septembre 2026 a
21 h 05 CEST, AVANT ce script et avant tout calcul de resultat.

QUESTION POSEE
--------------
i3 a mesure la bande a deux bords sur 1 052 personnes du GSS et 149 items d'attitudes, et
l'a ecrit dans ses limites (point 3) : un seul questionnaire, une seule segmentation. Si la
signature est une norme, elle doit se retrouver sur 2 058 autres personnes, 108 autres
items, treize configurations d'agents produites par une autre equipe avec GPT-4.1,
GPT-4.1-mini et Gemini-Flash-2.5.

CONVENTION DE REFERENCE, declaree au preenregistrement section 6, et qui differe de a6.
a6 prend la vague 4 comme reference et les vagues 1 a 3 comme controle. Ici c'est
l'inverse : les humains des vagues 1 a 3 sont le FOND du flux et la reference, et le
retest de la vague 4 est le CONTROLE DE FAUSSE ALARME, melange comme s'il etait un
fabricant. C'est la transposition exacte du dispositif de i3, ou le fond est la vague 1 du
GSS et le controle la vague 2.

SORTIES, toutes dans resultats/
-------------------------------
  i3b-twin-controles.csv    les controles bloquants sur ce jeu
  i3b-twin-reference.csv    la bande humaine de Twin, valeurs, IC et s0 par taille
  i3b-twin-abaque.csv       tau* par configuration, statistique et taille
  i3b-twin-sources-pures.csv les quinze conditions a taux 100 pour cent

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/i3b_twin.py
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
import a6_double_distorsion_hors_gss as A6

G = {}
FOND = "humains vagues 1-3 (retest)"      # le nom que a6 donne au fichier wave1_3
CONTROLE = "humains vague 4"
TAILLES = [1052, 2058]
TAILLES_REF = [600, 1000, 1052, 1500]


def charger_twin_commun(racine):
    """Les quinze tables de Twin dans UNE nomenclature commune, alignees sur les 2 058
    sujets de reference.

    a6.charger_twin est appelee telle quelle pour obtenir la liste des 108 colonnes
    categorielles, la segmentation ideologique et ses niveaux. a6.lire_formatte est
    appelee telle quelle pour relire chaque fichier. La seule chose reecrite ici est la
    construction de la nomenclature commune sur les QUINZE tables et l'alignement des trois
    configurations partielles sur l'index complet, que a6 ne fait pas : a6 met chaque
    configuration partielle dans un jeu separe, ce qui empeche de les melanger au meme
    flux. Cette reecriture est declaree, elle fait douze lignes et elle est verifiee par le
    controle de reproduction de a6.
    """
    import csv as _csv
    import json as _json
    jeux, alertes = A6.charger_twin(racine)
    if not jeux:
        raise SystemExit(f"twin indisponible : {alertes}")
    base = jeux[0]
    colonnes = base["items"]
    dossier = os.path.join(racine, "llm_specs")
    index = _json.load(open(os.path.join(dossier, "index.json"), encoding="utf-8"))
    fichiers = [(CONTROLE, "humains_wave4.csv"), (FOND, "humains_wave1_3.csv")] + \
               [(e["configuration"], e["fichier"]) for e in index]
    tables = {lib: A6.lire_formatte(os.path.join(dossier, f), colonnes)
              for lib, f in fichiers if os.path.exists(os.path.join(dossier, f))}
    ids = sorted(tables[CONTROLE])
    rang = {p: k for k, p in enumerate(ids)}
    n_items = len(colonnes)
    modalites = []
    for j in range(n_items):
        vus = set()
        for t in tables.values():
            vus.update(v[j] for v in t.values())
        vus.discard("")
        try:
            modalites.append(sorted(vus, key=float))
        except ValueError:
            modalites.append(sorted(vus))
    idx_mod = [{m: k for k, m in enumerate(mods)} for mods in modalites]
    codes, couverture = {}, {}
    for lib, t in tables.items():
        x = np.full((len(ids), n_items), -1, dtype=np.int16)
        for p, ligne in t.items():
            if p not in rang:
                continue
            i = rang[p]
            for j in range(n_items):
                k = idx_mod[j].get(ligne[j], -1)
                if k >= 0:
                    x[i, j] = k
        codes[lib] = x
        couverture[lib] = np.array(sorted(rang[p] for p in t if p in rang))
    seg = base["seg"]["ideologie politique"].astype(np.int32)
    niveaux = base["niveaux"]["ideologie politique"]
    blocs = np.array([A6.bloc_ideologie_twin(niveaux[k]) if k >= 0 else "inconnu"
                      for k in seg])
    k_items = np.array([max(len(m), 1) for m in modalites], dtype=np.int32)
    return {"codes": codes, "couverture": couverture, "ids": ids, "colonnes": colonnes,
            "modalites": modalites, "seg": seg, "niveaux": niveaux, "blocs": blocs,
            "k_items": k_items, "alertes": alertes, "n": len(ids),
            "configurations": [e["configuration"] for e in index]}


def contexte_twin(paq, rng):
    """Le contexte au format i3, avec les vingt sous ensembles tires parmi les seuls items
    presque toujours renseignes chez les humains de reference (preenr. section 3.1)."""
    fond = paq["codes"][FOND]
    fill = (fond >= 0).mean(axis=0)
    seuil = 0.99
    while (fill >= seuil).sum() < 20 and seuil > 0.3:
        seuil -= 0.05
    eligibles = np.flatnonzero(fill >= seuil)
    sous = [np.sort(rng.choice(eligibles, size=10, replace=False)) for _ in range(20)]
    return {"items": paq["colonnes"], "k_items": paq["k_items"], "seg": paq["seg"],
            "blocs": paq["blocs"], "colonnes": np.arange(len(paq["colonnes"])),
            "sous_ens": sous, "sous_ens5": [s[:5] for s in sous],
            "seuil_fill": seuil, "n_eligibles": int(len(eligibles))}


def _stats(codes, seg, blocs, ctx, rng, n_nul):
    ctxn = {**ctx, "seg": seg}
    st = I.statistiques(codes, ctxn, rng, n_nul=n_nul)
    pol, _, _ = I.polarisation(codes, blocs, signes=G["signes"])
    out = {k: st[k] for k in ("A", "B", "C", "C5", "patrons", "q5")}
    out["polarisation"] = pol
    # Bruit propre de la moyenne des R replicats nuls : il entre dans A et B, pas dans C
    # ni dans la polarisation, et il ne subit aucune correction de population finie.
    out["se_nul_A"] = (st["patrons_nul_et"] / np.sqrt(n_nul)
                       / max(st["patrons_nul"], 1e-9)) if n_nul > 1 else 0.0
    out["se_nul_B"] = st["q5_nul_et"] / np.sqrt(n_nul) if n_nul > 1 else 0.0
    out["se_nul_C"] = 0.0
    out["se_nul_polarisation"] = 0.0
    return out


def tache_melange(arg):
    nom, tau, tirage, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 211, G["id_source"][nom],
                                 int(tau * 10000), tirage])
    f, choisies = I.flux(G["fond"], G["codes"][nom], G["couverture"][nom], tau, rng)
    marque = np.zeros(f.shape[0], dtype=bool)
    marque[choisies] = True
    ordre = J.ordre_emboite(f.shape[0], rng)
    out = []
    for n in TAILLES:
        idx = np.sort(ordre[:n])
        st = _stats(f[idx], G["seg"][idx], G["blocs"][idx], G["ctx"], rng, n_nul)
        st.update({"source": nom, "taux": tau, "tirage": tirage, "taille": n,
                   "taux_realise": float(marque[idx].mean())})
        out.append(st)
    return out


def tache_reference(arg):
    n, b, n_nul = arg
    rng = np.random.default_rng([J.GRAINE, 213, n, b])
    idx = np.sort(rng.choice(G["fond"].shape[0], size=n, replace=False))
    st = _stats(G["fond"][idx], G["seg"][idx], G["blocs"][idx], G["ctx"], rng, n_nul)
    st.update({"taille": n, "tirage": b})
    return st


def tache_pure(nom):
    rng = np.random.default_rng([J.GRAINE, 227, G["id_source"][nom]])
    li = G["couverture"][nom]
    st = _stats(G["codes"][nom][li], G["seg"][li], G["blocs"][li], G["ctx"], rng, 40)
    return {"source": nom, "n": len(li), **{k: st[k] for k in
                                            ("A", "B", "C", "polarisation")}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default="data/twin2k500")
    ap.add_argument("--tirages", type=int, default=12)
    ap.add_argument("--nul", type=int, default=15)
    ap.add_argument("--reference", type=int, default=200)
    ap.add_argument("--procs", type=int, default=4)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    if args.smoke:
        args.tirages, args.nul, args.reference = 3, 4, 15

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = charger_twin_commun(args.racine)
    print(f"{paq['n']} sujets, {len(paq['colonnes'])} items, "
          f"{len(paq['configurations'])} configurations", flush=True)
    for a in paq["alertes"]:
        print("  alerte a6 :", a, flush=True)

    rng = np.random.default_rng([J.GRAINE, 7])
    ctx = contexte_twin(paq, rng)
    fond = paq["codes"][FOND]
    print(f"sous ensembles tires parmi {ctx['n_eligibles']} items dont le taux de "
          f"renseignement atteint {ctx['seuil_fill']:.2f}", flush=True)

    controles = [
        {"controle": "sujets, items, configurations, contre a6 section 1.4", "jeu": "twin",
         "objet": "structure", "valeur": f"{paq['n']}/{len(paq['colonnes'])}/"
                                         f"{len(paq['configurations'])}",
         "seuil": "2058/108/13",
         "passe": bool(paq["n"] == 2058 and len(paq["colonnes"]) == 108
                       and len(paq["configurations"]) == 13)},
        {"controle": "taux de cellules vides, contre a6 section 1.4", "jeu": "twin",
         "objet": CONTROLE,
         "valeur": round(float((paq["codes"][CONTROLE] < 0).mean()), 4), "seuil": "0,241",
         "passe": bool(abs(float((paq["codes"][CONTROLE] < 0).mean()) - 0.241) < 0.005)},
    ]
    cum, replis, total = C44.lois_par_segment(fond, paq["seg"], paq["k_items"])
    controles.append({"controle": "taux de repli du generateur nul, ideologie a cinq "
                                  "niveaux", "jeu": "twin", "objet": FOND,
                      "valeur": round(replis / max(total, 1), 6), "seuil": 0.0,
                      "passe": bool(replis == 0)})

    sources, couverture = {}, {}
    for nom, x in paq["codes"].items():
        if nom == FOND:
            continue
        m, perte = I.masquer_commun(x, fond)
        li = paq["couverture"][nom]
        _, p = I.masquer_commun(x[li], fond[li])
        sources[nom] = m
        couverture[nom] = li
        controles.append({"controle": "cellules perdues par l'intersection des masques",
                          "jeu": "twin", "objet": nom, "valeur": round(p, 6),
                          "seuil": 0.005, "passe": bool(p < 0.005)})

    rng0 = np.random.default_rng(J.GRAINE)
    un = paq["configurations"][0]
    f0, _ = I.flux(fond, sources[un], couverture[un], 0.0, rng0)
    controles.append({"controle": "le flux a taux 0 egale la population de fond",
                      "jeu": "twin", "objet": "toutes sources",
                      "valeur": int((f0 != fond).sum()), "seuil": 0,
                      "passe": bool(int((f0 != fond).sum()) == 0)})
    fn, _ = I.flux(fond, fond, np.arange(fond.shape[0]), 0.5,
                   np.random.default_rng(J.GRAINE + 1))
    controles.append({"controle": "controle negatif, fond melange a lui meme", "jeu":
                      "twin", "objet": "50 pour cent", "valeur": int((fn != fond).sum()),
                      "seuil": 0, "passe": bool(int((fn != fond).sum()) == 0)})

    _, signes, bon_pol = I.polarisation(fond, paq["blocs"], signes=None)
    G.update({"fond": fond, "codes": sources, "couverture": couverture,
              "seg": paq["seg"], "blocs": paq["blocs"], "ctx": ctx, "signes": signes,
              "id_source": {n: k + 1 for k, n in enumerate(sorted(sources))}})
    ctxt = mp.get_context("fork")

    print("\n--- reference humaine de Twin ---", flush=True)
    plein = _stats(fond, paq["seg"], paq["blocs"], ctx,
                   np.random.default_rng([J.GRAINE, 13]), max(args.nul * 4, 40))
    print(f"N = {paq['n']} : A = {plein['A']:+.5f}  B = {plein['B']:+.5f}  "
          f"C = {plein['C']:.5f}  P = {plein['polarisation']:+.4f}", flush=True)

    with ctxt.Pool(args.procs) as pool:
        t = time.time()
        ref = pd.DataFrame(pool.map(tache_reference,
                                    [(n, b, args.nul) for n in TAILLES_REF
                                     for b in range(args.reference)], chunksize=4))
        print(f"reference : {time.time() - t:.0f} s", flush=True)
        purs = pool.map(tache_pure, sorted(sources))

    lignes_ref, lois = [], {}
    for cle in ("A", "B", "C", "polarisation"):
        xs, ys = [], []
        for n in TAILLES_REF:
            v = ref[ref.taille == n][cle].values
            fpc = J.correction_population_finie(n, paq["n"])
            bas, haut, et = J.ic_pivote(v, centre=float(np.mean(v)))
            vn = float(np.mean(ref[ref.taille == n][f"se_nul_{cle}"].values ** 2))
            s0c = float(np.sqrt(max(et ** 2 - vn, 1e-24) * fpc ** 2 + vn))
            lignes_ref.append({"taille": n, "statistique": cle,
                               "valeur": float(np.mean(v)), "ic_bas": bas, "ic_haut": haut,
                               "ecart_type_sous_echantillon": et,
                               "facteur_population_finie": fpc,
                               "variance_du_nul_interieur": vn,
                               "s0_naif": et * fpc, "s0": s0c,
                               "n_tirages": int(len(v))})
            xs.append(np.log(n))
            ys.append(np.log(max(s0c, 1e-12)))
        pente, ordo = np.polyfit(np.array(xs), np.array(ys), 1)
        pred = ordo + pente * np.array(xs)
        r2 = 1.0 - ((np.array(ys) - pred) ** 2).sum() / max(
            ((np.array(ys) - np.mean(ys)) ** 2).sum(), 1e-30)
        lois[cle] = (float(np.exp(ordo)), float(-pente), float(r2))
        lignes_ref.append({"taille": paq["n"], "statistique": cle,
                           "valeur": float(plein[cle]), "ic_bas": np.nan,
                           "ic_haut": np.nan, "ecart_type_sous_echantillon": np.nan,
                           "facteur_population_finie": np.nan,
                           "variance_du_nul_interieur": np.nan, "s0_naif": np.nan,
                           "s0": float(np.exp(ordo) * paq["n"] ** pente), "n_tirages": 0})
    ref_df = pd.DataFrame(lignes_ref)
    ref_df["loi_c"] = ref_df.statistique.map(lambda c: lois[c][0])
    ref_df["loi_p"] = ref_df.statistique.map(lambda c: lois[c][1])
    ref_df["loi_r2"] = ref_df.statistique.map(lambda c: lois[c][2])
    J.ecrire(ref_df, "i3b-twin-reference.csv")
    J.ecrire(pd.DataFrame(purs), "i3b-twin-sources-pures.csv")

    print("\n--- melanges Twin ---", flush=True)
    taches = []
    for nom in sorted(sources):
        plafond = len(couverture[nom]) / paq["n"]
        for tau in I.TAUX:
            if tau == 0.0 or tau > plafond:
                continue
            for d in range(args.tirages):
                taches.append((nom, tau, d, args.nul))
    print(f"{len(taches)} flux x {len(TAILLES)} tailles", flush=True)
    t = time.time()
    with ctxt.Pool(args.procs) as pool:
        res = pool.map(tache_melange, taches, chunksize=2)
    print(f"melanges : {time.time() - t:.0f} s", flush=True)
    mel = pd.DataFrame([x for b in res for x in b])
    J.ecrire(mel, "i3b-twin-melanges.csv")

    refv, s0 = {}, {}
    for n in TAILLES:
        for cle in ("A", "B", "C", "polarisation"):
            if n == paq["n"]:
                refv[(n, cle)] = float(plein[cle])
            else:
                refv[(n, cle)] = float(ref[ref.taille == n][cle].mean())
            s0[(n, cle)] = float(ref_df[(ref_df.taille == n)
                                        & (ref_df.statistique == cle)].s0.iloc[0])

    lignes = []
    for nom in sorted(set(mel.source)):
        d = mel[mel.source == nom]
        for n in TAILLES:
            dn = d[d.taille == n]
            for cle in ("A", "B", "C"):
                taux = sorted(dn.taux.unique())
                moy = [float(dn[dn.taux == t][cle].mean()) for t in taux]
                ecarts = [m - refv[(n, cle)] for m in moy]
                a, b, r2 = J.ajuster_courbe([0.0] + taux, [0.0] + ecarts)
                s = s0[(n, cle)]
                for t, m in zip(taux, moy):
                    z = (m - refv[(n, cle)]) / s if s else np.nan
                    lignes.append({
                        "configuration": nom, "statistique": cle, "taille": n, "taux": t,
                        "valeur_moyenne": m, "reference_humaine": refv[(n, cle)],
                        "ecart_a_la_reference": m - refv[(n, cle)], "s0": s, "z": z,
                        "p_bilateral": J.p_bilateral(z) if np.isfinite(z) else np.nan,
                        "puissance_empirique": float(
                            (np.abs(dn[dn.taux == t][cle].values - refv[(n, cle)])
                             > J.Z_F2 * s).mean()),
                        "n_tirages": int(len(dn[dn.taux == t])),
                        "tau_etoile_holm39": J.racine_courbe(
                            a, b, (J.Z_F2 + J.Z_PUISSANCE) * s),
                        "tau_etoile_holm3": J.racine_courbe(
                            a, b, (J.Z_F1 + J.Z_PUISSANCE) * s),
                        "tau_etoile_nominal": J.racine_courbe(
                            a, b, (I.Z_ALPHA + J.Z_PUISSANCE) * s),
                        "courbe_a": a, "courbe_b": b, "courbe_r2": r2})
    ab = pd.DataFrame(lignes)
    # Holm sur la famille F2 : 3 statistiques x 13 configurations au taux 5 pour cent,
    # a la taille pleine.
    prim = ab[(ab.taux == 0.05) & (ab.taille == paq["n"])
              & (ab.configuration != CONTROLE)].copy()
    prim = prim.sort_values(["statistique", "configuration"]).reset_index(drop=True)
    prim["p_holm"] = J.holm(prim["p_bilateral"].values)
    ab = ab.merge(prim[["configuration", "statistique", "taille", "taux", "p_holm"]],
                  on=["configuration", "statistique", "taille", "taux"], how="left")
    J.ecrire(ab, "i3b-twin-abaque.csv")

    # controle 9.9 : le retest humain ne doit pas etre signale sous 25 pour cent
    faux = ab[(ab.configuration == CONTROLE) & (ab.taux <= 0.25)
              & (ab.taille == paq["n"])]
    pire = float(faux.z.abs().max()) if len(faux) else np.nan
    controles.append({"controle": "fausse alarme, retest humain vague 4 sous 25 pour cent",
                      "jeu": "twin", "objet": "|z| maximal", "valeur": round(pire, 2),
                      "seuil": f"< {J.Z_F2:.3f}", "passe": bool(pire < J.Z_F2)})
    # Le R2 n'a de sens que sur une courbe qui bouge : pour une source dont l'effet reste
    # sous un ecart type de reference, l'ajustement porte sur du bruit et son R2 est sans
    # objet. Le controle ne porte donc que sur les courbes a effet reel.
    bouge = ab[(ab.taux == 0.50) & (ab.taille == paq["n"])
               & (ab.z.abs() > 1.0)][["configuration", "statistique"]]
    cles = set(map(tuple, bouge.values))
    reelles = ab[[(c, st) in cles for c, st in
                  zip(ab.configuration, ab.statistique)]]
    pire = float(reelles.courbe_r2.min()) if len(reelles) else np.nan
    controles.append({"controle": "R2 de l'ajustement quadratique, courbes a effet reel",
                      "jeu": "twin",
                      "objet": f"minimum sur {len(cles)} courbes",
                      "valeur": round(pire, 4), "seuil": "> 0,95",
                      "passe": bool(np.isfinite(pire) and pire > 0.95)})
    ctrl = pd.DataFrame(controles)
    J.ecrire(ctrl, "i3b-twin-controles.csv")
    print(ctrl.to_string(index=False, max_colwidth=55), flush=True)
    print(f"\ntotal {time.time() - t0:.0f} s", flush=True)
    _ = bon_pol


if __name__ == "__main__":
    main()
