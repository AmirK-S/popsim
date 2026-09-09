"""
r4b_diagnostic : les rejets de R4, leur mecanisme, et la sensibilite des mesures.

Statut : script d'analyse jetable. Aucun appel de modele. Lecture seule sur
data/traces/r1-*-r4.jsonl et sur les tableaux de resultats/. Aucun script existant
n'est modifie.

Ce qu'il etablit :
  1. Le decompte des rejets par condition, par motif, par nombre de modalites K, et la
     part des relances qui rattrapent.
  2. Le mecanisme des rejets de q4hyb : les marqueurs de reconstruction de tour de
     conversation dans la sortie brute, comptes de la meme facon dans les quatre
     conditions, y compris celles qui ne rejettent pas.
  3. Le critere de chute 2 bis, recopie des exemples a trois coups, et son taux de base
     dans la condition sous gabarit.
  4. La sensibilite : les quantites principales recalculees en gardant les cellules
     relancees, puis sur le seul perimetre commun aux quatre conditions.

Entree  : data/traces/r1-{q4,q4base,q4nogab,q4hyb}-r4.jsonl,
          resultats/r1-par-item-ecarts-r4.csv, resultats/r1-par-cellule-r4.csv
Sortie  : resultats/r4b-rejets.csv, r4b-marqueurs-gabarit.csv, r4b-2bis.csv

Usage :
  .venv/bin/python analyses/r4b_diagnostic.py
"""

import collections
import json
import os

import numpy as np
import pandas as pd

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data", "traces")

CONDITIONS = ("q4", "q4nogab", "q4base", "q4hyb")

# Marqueurs de reconstruction d'un tour de conversation dans une invite de completion.
# Ils sont cherches a l'identique dans les quatre conditions, y compris sous gabarit,
# pour qu'aucun ne soit un artefact de la condition ou on l'a d'abord vu.
MARQUEURS = {
    "separateur d'exemple ----": ("----",),
    "annonce d'une question nouvelle": ("Now, here's the actual", "Now, the actual",
                                        "Now here's the actual", "the actual question"),
    "en tete d'exemple recopie": ("Survey question, Millbrook",),
    "auto correction en cours de reponse": ("Wait,", "But the example", "So, the answer is",
                                            "The final answer", "That adds up"),
    "balise de reponse mathematique": ("\\boxed",),
    "texte apres la derniere ligne chiffree": (),   # calcule a part
}

EXEMPLES = {3: [17, 46, 37], 6: [22, 9, 14, 11, 27, 17], 2: [43, 57]}


def lire(cle):
    lignes = []
    with open(os.path.join(TRACES, f"r1-{cle}-r4.jsonl"), encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if ligne:
                lignes.append(json.loads(ligne))
    return lignes


def rejets():
    out = []
    for cle in CONDITIONS:
        tr = lire(cle)
        rej = [d for d in tr if d["rejet"]]
        relances = [d for d in tr if d["n_tentatives"] > 1]
        rattrapees = [d for d in relances if not d["rejet"]]
        motifs = collections.Counter(d["motif_rejet"].split(" : ")[0] for d in rej)
        par_k = collections.Counter(d["n_modalites"] for d in rej)
        # taux de rejet de la premiere tentative, avant relance
        premiere = sum(1 for d in tr if d["tentatives"][0]["motif_rejet"])
        out.append({
            "cle_modele": cle, "cellules": len(tr),
            "echecs_premiere_tentative": premiere,
            "taux_echec_premiere": premiere / len(tr),
            "relances": len(relances),
            "relances_rattrapees": len(rattrapees),
            "part_relances_rattrapees": len(rattrapees) / len(relances) if relances else float("nan"),
            "rejets_apres_relance": len(rej),
            "taux_rejet_apres_relance": len(rej) / len(tr),
            "rejets_K_sup_4": sum(v for k, v in par_k.items() if k >= 5),
            "K_median_des_rejets": float(np.median([d["n_modalites"] for d in rej])) if rej else float("nan"),
            "motifs": "; ".join(f"{m} x{n}" for m, n in motifs.most_common()),
            "K_des_rejets": "; ".join(f"K={k} x{n}" for k, n in sorted(par_k.items())),
        })
    return pd.DataFrame(out)


def marqueurs():
    """Les marqueurs de reconstruction de tour, comptes dans toutes les sorties brutes."""
    out = []
    for cle in CONDITIONS:
        tr = lire(cle)
        n_sorties = sum(len(d["tentatives"]) for d in tr)
        n_relances = sum(1 for d in tr for t in d["tentatives"] if t["rappel"])
        compte = collections.Counter()
        compte_relance = collections.Counter()
        for d in tr:
            for t in d["tentatives"]:
                s = t["sortie_brute"]
                for nom, mots in MARQUEURS.items():
                    if mots and any(m in s for m in mots):
                        compte[nom] += 1
                        if t["rappel"]:
                            compte_relance[nom] += 1
        for nom in MARQUEURS:
            if not MARQUEURS[nom]:
                continue
            out.append({
                "cle_modele": cle, "marqueur": nom,
                "n_sorties": n_sorties, "n_sorties_de_relance": n_relances,
                "sorties_touchees": compte[nom],
                "part_des_sorties": compte[nom] / n_sorties,
                "dont_relances": compte_relance[nom],
                "part_des_relances": compte_relance[nom] / n_relances if n_relances else float("nan"),
            })
    return pd.DataFrame(out)


def critere_2bis():
    """Recopie d'un exemple a trois coups, et son taux de base sous gabarit."""
    out = []
    for cle in CONDITIONS:
        tr = lire(cle)
        par_k = collections.Counter()
        cells_k = collections.Counter()
        for d in tr:
            k = d["n_modalites"]
            cells_k[k] += 1
            if d["rejet"] or k not in EXEMPLES:
                continue
            p = np.array(list(d["distribution"].values()), float)
            ex = np.array(EXEMPLES[k], float)
            ex = ex / ex.sum()
            if len(p) == len(ex) and np.allclose(p, ex, atol=1e-6):
                par_k[k] += 1
        for k in sorted(EXEMPLES):
            out.append({
                "cle_modele": cle, "K": k, "cellules_de_ce_K": cells_k[k],
                "recopies_exactes": par_k[k],
                "taux": par_k[k] / cells_k[k] if cells_k[k] else float("nan"),
                "retire_des_mesures": k >= 3,
            })
    return pd.DataFrame(out)


def indifference():
    """Part d'items ou les camps gauche et droite recoivent la meme distribution,
    et part d'items ou la distribution decrite est celle de l'item precedent."""
    eca = pd.read_csv(os.path.join(SORTIE, "r1-par-item-ecarts-r4.csv"))
    out = []
    for cle in CONDITIONS:
        for identite in ("journaliste", "adversaire"):
            g = eca[(eca["cle_modele"] == cle) & (eca["identite"] == identite)]
            out.append({
                "cle_modele": cle, "identite": identite, "n_items": len(g),
                "part_items_camps_identiques": float((g["tv_camps_decrit"] < 1e-9).mean()),
                "tv_camps_decrit_moyen": float(g["tv_camps_decrit"].mean()),
            })
    # repetition d'une meme distribution d'un item a l'autre, a K egal
    for cle in CONDITIONS:
        tr = [d for d in lire(cle) if not d["rejet"]]
        par_cle = collections.defaultdict(list)
        for d in tr:
            par_cle[(d["camp"], d["identite"], d["n_modalites"])].append(
                tuple(round(v, 6) for v in d["distribution"].values()))
        rep = tot = 0
        for _, v in par_cle.items():
            if len(v) < 2:
                continue
            c = collections.Counter(v)
            tot += len(v)
            rep += len(v) - len(c)
        out.append({"cle_modele": cle, "identite": "les deux",
                    "n_items": tot,
                    "part_items_camps_identiques": float("nan"),
                    "tv_camps_decrit_moyen": float("nan"),
                    "part_distributions_repetees_entre_items": rep / tot if tot else float("nan")})
    return pd.DataFrame(out)


def alpha_uniforme():
    """Coefficient de retrecissement vers l'uniforme, `p_decrit = a p_reel + (1 - a) u`.

    Quantite declaree apres coup, dans l'esprit de r1 section 3.3 : ajustement au sens des
    moindres carres sans constante sur les ecarts a l'uniforme, cellule par cellule, puis
    mediane. a = 1 est la fidelite, a = 0 est l'uniforme.
    """
    d = pd.read_csv(os.path.join(TRACES, "r1-distributions-reelles.csv"),
                    keep_default_na=False, na_values=[""])
    for col in ("rang", "n", "effectif", "p"):
        d[col] = pd.to_numeric(d[col], errors="coerce")
    ref = {}
    for (item, camp, vague), g in d.groupby(["item", "camp", "vague"], sort=False):
        g = g.sort_values("rang")
        ref[(item, camp, vague)] = (list(g["modalite"]), g["p"].to_numpy(float))
    out = []
    for cle in CONDITIONS:
        for identite in ("journaliste", "adversaire"):
            a = []
            for o in lire(cle):
                if o["rejet"] or o["identite"] != identite:
                    continue
                k = (o["item"], o["camp"], "w1")
                if k not in ref:
                    continue
                mods, pr = ref[k]
                pdd = np.array([o["distribution"].get(m, 0.0) for m in mods], float)
                if len(pdd) != len(pr):
                    continue
                u = np.ones(len(pr)) / len(pr)
                x, y = pr - u, pdd - u
                if float(x @ x) < 1e-12:
                    continue
                a.append(float((x @ y) / (x @ x)))
            out.append({"cle_modele": cle, "identite": identite, "n_cellules": len(a),
                        "alpha_median": float(np.median(a)) if a else float("nan"),
                        "alpha_moyen": float(np.mean(a)) if a else float("nan")})
    return pd.DataFrame(out)


def main():
    r = rejets()
    m = marqueurs()
    b = critere_2bis()
    i = indifference()
    al = alpha_uniforme()
    for df, nom in ((r, "r4b-rejets"), (m, "r4b-marqueurs-gabarit"),
                    (b, "r4b-2bis"), (i, "r4b-indifference"),
                    (al, "r4b-alpha-uniforme")):
        chemin = os.path.join(SORTIE, f"{nom}.csv")
        df.to_csv(chemin, index=False)
        print(f"ecrit {chemin}  {len(df)} lignes")
    pd.set_option("display.width", 220, "display.max_columns", 40)
    print("\n--- rejets ---")
    print(r.to_string(index=False))
    print("\n--- marqueurs de reconstruction de tour ---")
    print(m.to_string(index=False))
    print("\n--- critere 2 bis ---")
    print(b.to_string(index=False))
    print("\n--- indifference au camp et repetition ---")
    print(i.to_string(index=False))
    print("\n--- retrecissement vers l'uniforme ---")
    print(al.to_string(index=False))


if __name__ == "__main__":
    main()
