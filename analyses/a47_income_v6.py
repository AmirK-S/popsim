"""
a47_income_v6 : les items recopies par une condition, et ce qu'ils valent dans la chute
sous permutation de `agents demographiques (v6)`.

===========================================================================
CHANTIER a47, 9 septembre 2026. Applique l'objection 1.5 de
resultats/a45-relecture-adverse-2.md, elle meme heritee de l'objection 2.2 de a17 : `income`
figure dans les 149 items et `gss_v6` le recopie a 0,994, ce qui gonfle son exactitude et,
par voie de consequence, sa chute sous permutation.

Deux etapes, sans aucun script existant modifie, sans appel de modele, lecture seule sur
data/ et sur les caches /tmp de a25, a28 et a35 :

  1. balayage complet des 149 items x toutes les conditions : taux d'accord item par item
     avec la vague 1, et liste des items recopies a 0,95 ou plus par au moins une condition ;
  2. la chute sous permutation intra segment de a44, sous `S_ideo`, rejouee sur les items
     restants, pour `v6`, `v8`, `composite` et les humains de la vague 2.

SORTIES, dans resultats/
------------------------
  a47-items-recopies.csv          taux d'accord item par item, condition par condition
  a47-chute-hors-items-recopies.csv   la chute avec et sans les items recopies

Usage : .venv/bin/python analyses/a47_income_v6.py --permutations 200
===========================================================================
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import a44_commun as C
from a44_mesures import exactitude_codes

SEUIL_RECOPIE = 0.95


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--permutations", type=int, default=C.N_PERMUTATIONS)
    args = ap.parse_args()

    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    items = paquet["items"]
    alpha = C.alphabet(items, paquet["options"])
    seg_tous, _ = C.segmentations(paquet)
    l150 = np.asarray(paquet["lignes150"])
    per = {"1052": np.arange(len(paquet["ids"])), "150": l150}
    conditions = [c for c in C.TOUTES if c in paquet["M"]]
    codes = {nom: C.coder(paquet["M"][nom], alpha)[0] for nom in conditions}
    y1 = codes["humains vague 1"]

    # ------------------------------------------------- 1. balayage item par item
    interessantes = [c for c in conditions
                     if c not in ("humains vague 1", "humains vague 1 (150)")]
    lignes, accord = [], {}
    for nom in interessantes:
        li = per[C.PERIMETRE[nom]]
        for j, it in enumerate(items):
            v, p = y1[li, j], codes[nom][li, j]
            ok = v >= 0
            a = float((p[ok] == v[ok]).mean()) if ok.sum() else np.nan
            accord[(nom, it)] = a
            lignes.append({"condition": nom, "perimetre": C.PERIMETRE[nom], "item": it,
                           "n_observes": int(ok.sum()), "taux_accord": a})
    C.ecrire(lignes, "a47-items-recopies.csv")

    recopies = sorted({it for (nom, it), a in accord.items()
                       if a is not None and a == a and a >= SEUIL_RECOPIE})
    print(f"{len(recopies)} items recopies a {SEUIL_RECOPIE:.2f} ou plus par au moins "
          f"une condition :", flush=True)
    for it in recopies:
        par = [(C.ETIQUETTE.get(n, n), a) for (n, i), a in accord.items()
               if i == it and a == a and a >= SEUIL_RECOPIE]
        par.sort(key=lambda t: -t[1])
        print(f"  {it:<12s} " + ", ".join(f"{n} {a:.3f}" for n, a in par), flush=True)

    garde = np.array([it not in recopies for it in items])
    print(f"\n{int(garde.sum())} items conserves sur {len(items)}", flush=True)

    # ------------------------------------------------- 2. la chute, avec et sans
    rng = np.random.default_rng(C.GRAINE + 7)
    sortie = []
    for nom in conditions:
        nom_per = C.PERIMETRE[nom]
        li = per[nom_per]
        s = seg_tous["S_ideo"][li]
        for jeu, masque in (("149 items", np.ones(len(items), dtype=bool)),
                            (f"{int(garde.sum())} items, recopies retires", garde)):
            cd, vt = codes[nom][np.ix_(li, np.flatnonzero(masque))], \
                y1[np.ix_(li, np.flatnonzero(masque))]
            vraie = float(np.nanmean(exactitude_codes(cd, vt)))
            perms = np.array([
                float(np.nanmean(exactitude_codes(
                    cd[C.permuter_intra(len(li), s, rng)], vt)))
                for _ in range(args.permutations)])
            moy = float(perms.mean())
            sortie.append({"condition": nom, "perimetre": nom_per, "jeu_d_items": jeu,
                           "n_items": int(masque.sum()),
                           "exactitude_vraie": vraie, "exactitude_permutee": moy,
                           "chute": vraie - moy,
                           "chute_relative": (vraie - moy) / vraie if vraie else np.nan})
    ref = {(l["perimetre"], l["jeu_d_items"]): l["chute_relative"] for l in sortie
           if l["condition"] in ("humains vague 2", "humains vague 2 (150)")}
    for l in sortie:
        d = ref.get((l["perimetre"], l["jeu_d_items"]))
        l["part_du_plancher_humain"] = (l["chute_relative"] / d
                                        if d and abs(d) > 1e-12 else np.nan)
    C.ecrire(sortie, "a47-chute-hors-items-recopies.csv")

    print("\npart du plancher humain sous S_ideo, avant et apres retrait")
    for nom in conditions:
        v = [l for l in sortie if l["condition"] == nom]
        print(f"  {C.ETIQUETTE.get(nom, nom):>18s} : "
              f"{v[0]['part_du_plancher_humain']:.3f} -> "
              f"{v[1]['part_du_plancher_humain']:.3f}")


if __name__ == "__main__":
    main()
