"""
a44_structure : la structure entre items survit elle au conditionnement le plus fin ?

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Complement DESCRIPTIF de a44_mesures, ajoute
apres lecture des resultats principaux et signale post hoc partout : il n'entre dans
aucune famille de tests declaree au preenregistrement.

POURQUOI CE COMPLEMENT
----------------------
Q5, la correlation moyenne entre items apres retrait du segment, mesure la structure qui
survit au conditionnement. Elle ne dit pas de qui est cette structure. Une correlation qui
survit au retrait de l'ideologie peut tres bien venir d'une demographie plus fine, la
race ou l'education, presente dans l'etiquette de l'agent : ce serait encore du gabarit de
groupe, simplement d'un groupe plus petit. Ce script fait varier la finesse du
conditionnement et regarde ce qui reste a chaque niveau.

Quatre niveaux, du plus grossier au plus fin :
  N0  aucun segment                                            1 cellule
  N1  ideologie politique, sept niveaux                        7 cellules
  N2  profil croise de a1, genre x race x bloc d'ideologie    18 cellules
  N3  bloc d'ideologie x genre x age                          42 cellules
  N4  bloc d'ideologie x genre x race x education             jusqu'a 90 cellules

A chaque niveau, la meme quantite est calculee sur la population et sur son generateur nul
construit au MEME niveau. L'exces au dessus du nul est ce qui ne s'explique pas par la
composition du segment. S'il tombe a zero au niveau le plus fin, la structure etait de la
demographie ; s'il survit, elle est ailleurs, et la permutation intra segment de
a44_mesures dit alors si cet ailleurs est la personne.

Entree  : caches de a25, a28 et a35, comme a44_mesures.
Sortie  : resultats/a44-structure-par-finesse.csv

Usage : .venv/bin/python analyses/a44_structure.py --replicats 50
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import a28_commun as C28
import a44_commun as C


def niveaux_de_finesse(paquet):
    """Les cinq niveaux de conditionnement, du plus grossier au plus fin."""
    col = {a: i for i, a in enumerate(paquet["attributs"])}

    def brut(a):
        return [C28.norm(v) for v in paquet["x"][:, col[a]]]

    ideo = [C._bloc_ideologie(v) for v in brut("political_ideology")]
    g, r, a, e = brut("gender"), brut("race"), brut("age"), brut("education")
    combi = {
        "N0 aucun segment": ["tout"] * len(ideo),
        "N1 ideologie": brut("political_ideology"),
        "N2 genre x race x ideologie": [f"{x}|{y}|{z}" for x, y, z in zip(g, r, ideo)],
        "N3 ideologie x genre x age": [f"{z}|{x}|{y}" for z, x, y in zip(ideo, g, a)],
        "N4 ideologie x genre x race x education":
            [f"{z}|{x}|{y}|{w}" for z, x, y, w in zip(ideo, g, r, e)],
    }
    out = {}
    for nom, valeurs in combi.items():
        mods = sorted({v for v in valeurs if v.strip() and "non renseigne" not in v})
        idx = {m: k for k, m in enumerate(mods)}
        out[nom] = (np.array([idx.get(v, -1) for v in valeurs], dtype=np.int32),
                    len(mods))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--replicats", type=int, default=50)
    args = ap.parse_args()

    t0 = time.time()
    print(__doc__.split("Usage")[0], flush=True)
    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    items, options = paquet["items"], paquet["options"]
    alpha = C.alphabet(items, options)
    k_items = np.array([len(options[it]) for it in items], dtype=np.int32)
    colonnes = np.arange(len(items))
    l150 = np.asarray(paquet["lignes150"])
    per = {"1052": np.arange(len(paquet["ids"])), "150": l150}
    niveaux = niveaux_de_finesse(paquet)
    conditions = [c for c in C.TOUTES if c in paquet["M"]]

    lignes = []
    for i_c, nom in enumerate(conditions):
        nom_per = C.PERIMETRE[nom]
        li = per[nom_per]
        cd, _ = C.coder(paquet["M"][nom], alpha)
        cd = cd[li]
        for i_s, (nom_niv, (seg_tout, n_niv)) in enumerate(niveaux.items()):
            s = seg_tout[li]
            cum, rep, tot = C.lois_par_segment(cd, s, k_items)
            q5 = C.correlation_items(cd, colonnes, s)[0]
            q4 = C.correlation_items(cd, colonnes)[0]
            a5, a4 = [], []
            for r in range(args.replicats):
                nul = C.tirer_nul(cd, s, cum,
                                  np.random.default_rng([C.GRAINE, 77, i_c, i_s, r]))
                a5.append(C.correlation_items(nul, colonnes, s)[0])
                a4.append(C.correlation_items(nul, colonnes)[0])
            lignes.append({
                "condition": nom, "perimetre": nom_per, "finesse": nom_niv,
                "cellules_declarees": n_niv,
                "cellules_effectives": int(len({int(z) for z in s if z >= 0})),
                "part_repliee": round(rep / max(tot, 1), 4),
                "Q5_reel": q5, "Q5_nul": float(np.nanmean(a5)),
                "Q5_exces": q5 - float(np.nanmean(a5)),
                "Q4_reel": q4, "Q4_nul": float(np.nanmean(a4)),
                "Q4_exces": q4 - float(np.nanmean(a4)),
                "replicats": args.replicats})
        print(f"  {nom}, {time.time() - t0:.0f}s", flush=True)

    C.ecrire(lignes, "a44-structure-par-finesse.csv")
    print(f"termine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
