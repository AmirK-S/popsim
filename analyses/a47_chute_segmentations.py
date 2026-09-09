"""
a47_chute_segmentations : la chute d'exactitude sous permutation intra segment, rejouee
sous une segmentation qui contient l'ideologie et sous une segmentation qui ne la contient
pas.

===========================================================================
CHANTIER a47, 9 septembre 2026. Applique l'objection 2 de
resultats/a45-relecture-adverse-2.md : a44 ne mesure la chute que sous `S_ideo` (ideologie
a sept niveaux) et `S_fin` (bloc d'ideologie x genre x age), deux segmentations qui
contiennent l'axe meme que l'invite de C2 et de v8 recoit. La permutation y mesure donc
« ce que l'agent sait au dela de ce qu'on vient de fixer » et non « l'agent porte il la
personne ».

Ce script ne modifie aucun script existant. Il importe a44_commun et a44_mesures tels
quels : meme chargement des trois caches, meme codage, meme fonction `permuter_intra`,
meme definition d'exactitude, meme reassignation hongroise. La seule chose neuve est une
troisieme segmentation, genre x race x age, construite avec la meme mecanique que `S_fin`
mais sans le bloc d'ideologie.

Aucun appel de modele de langage. Lecture seule sur data/. Les caches /tmp de a25, a28 et
a35 sont relus, jamais reecrits.

SORTIES, dans resultats/
------------------------
  a47-chute-deux-segmentations.csv   toutes les conditions x trois segmentations
  a47-plancher-reassignation.csv     le gain hongrois absolu, avec B0 tirage comme plancher
  a47-correlation-chute-exactitude.csv  la correlation de la chute avec l'exactitude brute

Usage :
  .venv/bin/python analyses/a47_chute_segmentations.py --permutations 200
===========================================================================
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import a28_commun as C28
import a44_commun as C
from a44_mesures import exactitude_codes, reassignation_codes


def segmentation_sans_ideologie(paquet):
    """genre x race x age, memes trois axes que `S_fin` mais l'ideologie remplacee par la
    race. Meme regle de construction que `a44_commun.segmentations` : normalisation par
    `a28_commun.norm`, cellule -1 pour toute personne dont un des trois attributs est
    absent, niveaux tries.
    """
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    brut = {a: [C28.norm(v) for v in paquet["x"][:, col[a]]]
            for a in ("gender", "race", "age")}
    cle = [f"{g}|{r}|{a}" for g, r, a in zip(brut["gender"], brut["race"], brut["age"])]
    mods = sorted({v for v in cle if v.strip() and "non renseigne" not in v})
    idx = {m: k for k, m in enumerate(mods)}
    return np.array([idx.get(v, -1) for v in cle], dtype=np.int32), mods


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--permutations", type=int, default=C.N_PERMUTATIONS)
    args = ap.parse_args()

    t0 = time.time()
    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    items, options = paquet["items"], paquet["options"]
    alpha = C.alphabet(items, options)
    seg_tous, _ = C.segmentations(paquet)
    seg_gra, mods_gra = segmentation_sans_ideologie(paquet)
    seg_tous["S_gra"] = seg_gra

    l150 = np.asarray(paquet["lignes150"])
    per = {"1052": np.arange(len(paquet["ids"])), "150": l150}
    conditions = [c for c in C.TOUTES if c in paquet["M"]]
    codes = {nom: C.coder(paquet["M"][nom], alpha)[0] for nom in conditions}

    print(f"{len(paquet['ids'])} personnes, {len(items)} items, "
          f"{len(conditions)} conditions", flush=True)
    for nom_seg in ("S_ideo", "S_fin", "S_gra"):
        for nom_per, lignes in per.items():
            s = seg_tous[nom_seg][lignes]
            n_cell = len({int(k) for k in np.unique(s) if k >= 0})
            print(f"  {nom_seg}, perimetre {nom_per} : {n_cell} cellules, "
                  f"{int((s < 0).sum())} personnes hors cellule", flush=True)

    # --------------------------------------------------------- la chute
    rng_p = np.random.default_rng(C.GRAINE + 2)
    brut = []
    for nom in conditions:
        nom_per = C.PERIMETRE[nom]
        lignes = per[nom_per]
        cd, y1 = codes[nom][lignes], codes["humains vague 1"][lignes]
        vraie = float(np.nanmean(exactitude_codes(cd, y1)))
        for nom_seg in ("S_ideo", "S_fin", "S_gra"):
            s = seg_tous[nom_seg][lignes]
            perms = np.array([
                float(np.nanmean(exactitude_codes(cd[C.permuter_intra(len(lignes), s,
                                                                      rng_p)], y1)))
                for _ in range(args.permutations)])
            opt = reassignation_codes(cd, y1, s)
            moy = float(perms.mean())
            brut.append({
                "condition": nom, "perimetre": nom_per, "segmentation": nom_seg,
                "n_cellules": len({int(k) for k in np.unique(s) if k >= 0}),
                "exactitude_vraie": vraie,
                "exactitude_permutee": moy,
                "permutee_bas": float(np.percentile(perms, 2.5)),
                "permutee_haut": float(np.percentile(perms, 97.5)),
                "chute": vraie - moy,
                "chute_relative": (vraie - moy) / vraie if vraie else np.nan,
                "exactitude_reassignation_optimale": opt,
                "gain_hongrois_absolu": opt - moy,
                "part_recuperee_par_reassignation":
                    ((opt - moy) / (vraie - moy)) if abs(vraie - moy) > 1e-9 else np.nan,
                "permutations": args.permutations})
        print(f"  {nom}, {time.time() - t0:.0f}s", flush=True)

    # part du plancher humain : chute relative divisee par celle des memes humains
    # reinterroges sur le meme perimetre, exactement la colonne du tableau 5 de a44.
    ref = {(l["perimetre"], l["segmentation"]): l["chute_relative"] for l in brut
           if l["condition"] in ("humains vague 2", "humains vague 2 (150)")}
    for l in brut:
        d = ref.get((l["perimetre"], l["segmentation"]))
        l["plancher_humain_chute_relative"] = d
        l["part_du_plancher_humain"] = (l["chute_relative"] / d
                                        if d and abs(d) > 1e-12 else np.nan)
    C.ecrire(brut, "a47-chute-deux-segmentations.csv")

    # ------------------------------------------- plancher de la reassignation
    plancher = []
    for l in brut:
        if l["segmentation"] != "S_ideo":
            continue
        plancher.append({
            "condition": l["condition"], "perimetre": l["perimetre"],
            "segmentation": "S_ideo",
            "gain_hongrois_absolu": l["gain_hongrois_absolu"],
            "chute_vraie": l["chute"],
            "rapport_publie_a44": l["part_recuperee_par_reassignation"],
            "au_dessus_du_plancher_B0_tirage": np.nan})
    base = [p for p in plancher if p["condition"] == "B0 tirage"]
    seuil = base[0]["gain_hongrois_absolu"] if base else np.nan
    for p in plancher:
        p["au_dessus_du_plancher_B0_tirage"] = bool(p["gain_hongrois_absolu"] > seuil)
    C.ecrire(plancher, "a47-plancher-reassignation.csv")

    # ------------------------------- correlation chute contre exactitude brute
    from scipy.stats import pearsonr, spearmanr
    lignes_cor = []
    for nom_seg in ("S_ideo", "S_fin", "S_gra"):
        for etendue, garde in (
                ("treize conditions du perimetre 1052, hors humains vague 1",
                 lambda l: l["perimetre"] == "1052"
                 and l["condition"] != "humains vague 1"),
                ("toutes conditions du perimetre 1052",
                 lambda l: l["perimetre"] == "1052")):
            sel = [l for l in brut if l["segmentation"] == nom_seg and garde(l)]
            x = np.array([l["exactitude_vraie"] for l in sel])
            y = np.array([l["chute"] for l in sel])
            lignes_cor.append({
                "segmentation": nom_seg, "etendue": etendue, "n_conditions": len(sel),
                "pearson": float(pearsonr(x, y)[0]),
                "spearman": float(spearmanr(x, y)[0]),
                "variance_partagee": float(pearsonr(x, y)[0] ** 2)})
    C.ecrire(lignes_cor, "a47-correlation-chute-exactitude.csv")

    # ------------------------------------------------------------- resume
    print("\npart du plancher humain, par segmentation")
    for nom in conditions:
        d = {l["segmentation"]: l["part_du_plancher_humain"] for l in brut
             if l["condition"] == nom}
        print(f"  {C.ETIQUETTE.get(nom, nom):>18s} : "
              f"S_ideo {d['S_ideo']:.3f}  S_fin {d['S_fin']:.3f}  "
              f"S_gra {d['S_gra']:.3f}")
    print("\ncorrelation chute contre exactitude brute")
    for l in lignes_cor:
        print(f"  {l['segmentation']} {l['etendue']} n={l['n_conditions']} : "
              f"pearson {l['pearson']:.3f}, spearman {l['spearman']:.3f}")
    print(f"\ntermine en {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
