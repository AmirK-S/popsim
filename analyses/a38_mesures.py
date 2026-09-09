"""
a38_mesures : l'ecart agent contre humain par item, en population entiere et camp par camp.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a2_baselines_gss, a5_evaluer, a5_agents_locaux_gss, a25_commun, a25_mesures, a28_commun,
a28_test1_mode et a30_commun. En particulier, la fonction de mesure par item est
`a28_test1_mode.mesurer`, reprise sans une ligne de changement : c'est ce qui garantit que
les chiffres de a38 en population entiere sont exactement ceux de a28.

Trois mesures par couple condition et item, et par camp :
  - distance de distribution agent contre humain, Wasserstein sur les rangs pour les items
    ordinaux, variation totale pour les nominaux ;
  - rapport d'entropie agent sur humain, entropie corrigee par Miller Madow ;
  - ecart de desirabilite, score de a25, positif si la masse simulee se deplace vers le
    pole desirable.

Camps : la partition `bloc3` de a30_commun, gauche / centre / droite, regle mecanique sur
le libelle de `political_ideology`. Aucune autre partition n'est employee ici ; le controle
par identification partisane est signale comme non fait dans le rapport.

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl.
Sortie  : resultats/a38-par-item-condition.csv, resultats/a38-par-camp.csv.

Usage :
  .venv/bin/python analyses/a38_mesures.py --cache /tmp/a25-matrices.pkl \\
      --cache-foret /tmp/a28-foret.npy
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a38_commun as A38
from a2_commun import est_manquant
from a25_commun import ORDINAUX, classe_norc, sans_score, scores_desirabilite
from a25_mesures import desirabilite_moyenne
from a28_test1_mode import mesurer
from a30_commun import camps_gss


def desirabilite_humaine(paquet, lignes):
    """Score moyen de desirabilite de la population humaine de la vague 1, par item.

    Meme score que a25, meme renormalisation sur les seules modalites pourvues d'un
    score. Il sert d'echelle de reference au test par camp : l'ecart humain entre le bloc
    de gauche et le bloc de droite est ce qu'une simulation fidele devrait reproduire.
    """
    items, y1, options = paquet["items"], paquet["y1"], paquet["options"]
    out = {}
    for j, it in enumerate(items):
        opts = options[it]
        sc, _, _ = scores_desirabilite(it, opts)
        if not sc:
            continue
        index = {o: k for k, o in enumerate(opts)}
        vec = np.zeros(len(opts))
        defini = np.zeros(len(opts))
        for o, v in sc.items():
            vec[index[o]] = v
            defini[index[o]] = 1.0
        c = np.zeros(len(opts))
        for v in y1[lignes, j]:
            if v is None or est_manquant(v):
                continue
            k = index.get(C28.norm(v))
            if k is not None:
                c[k] += 1
        if c.sum() == 0:
            continue
        d, _ = desirabilite_moyenne((c / c.sum())[None, :], vec, defini)
        out[it] = float(d[0])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    args = ap.parse_args()

    paquet = C28.charger_tout(args.cache, args.cache_foret)
    items = paquet["items"]
    classes = {it: classe_norc(it)[0] for it in items}
    types = {it: C28.type_item(it, paquet["options"]) for it in items}

    toutes = [c for c in C28.ORDRE_METHODES if c in paquet["M"]]
    perimetres = {"150": np.asarray(paquet["lignes150"]),
                  "1052": np.arange(len(paquet["ids"]))}

    # ------------------------------------------------- population entiere
    par_item = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        d = mesurer(paquet, lignes, conds)
        d["perimetre"] = nom_per
        d["camp"] = "tous"
        d["n_personnes"] = len(lignes)
        par_item.append(d)
        print(f"  perimetre {nom_per}, tous camps : {len(d)} couples", flush=True)

    # ------------------------------------------------- camp par camp
    camps = camps_gss(paquet["x"], paquet["attributs"])["bloc3"]
    par_camp = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        for camp in A38.CAMPS:
            sel = np.array([i for i in lignes if camps[i] == camp], dtype=int)
            if len(sel) < 20:
                print(f"  perimetre {nom_per}, camp {camp} : {len(sel)} personnes, "
                      "trop peu, ecarte")
                continue
            d = mesurer(paquet, sel, conds)
            d["perimetre"] = nom_per
            d["camp"] = camp
            d["n_personnes"] = len(sel)
            par_camp.append(d)
            print(f"  perimetre {nom_per}, camp {camp} : {len(sel)} personnes, "
                  f"{len(d)} couples", flush=True)

    tout = pd.concat(par_item, ignore_index=True)
    tout["classe_norc"] = tout.item.map(classes)
    tout["type"] = tout.item.map(types)
    tout["classe_comportement"] = tout.item.map(A38.classe_comportement)
    A38.ecrire(tout, "a38-par-item-condition.csv")

    # ------------------------------------------------- reference humaine par camp
    ref_hum = []
    for nom_per, lignes in perimetres.items():
        for camp in A38.CAMPS:
            sel = np.array([i for i in lignes if camps[i] == camp], dtype=int)
            if len(sel) < 20:
                continue
            for it, v in desirabilite_humaine(paquet, sel).items():
                ref_hum.append({"perimetre": nom_per, "camp": camp, "item": it,
                                "desirabilite_humaine": v, "n_personnes": len(sel)})
        for it, v in desirabilite_humaine(paquet, lignes).items():
            ref_hum.append({"perimetre": nom_per, "camp": "tous", "item": it,
                            "desirabilite_humaine": v, "n_personnes": len(lignes)})
    hum = pd.DataFrame(ref_hum)
    hum["pole_endogroupe"] = hum.item.map(
        lambda it: A38.POLE_ENDOGROUPE[it][0] if it in A38.POLE_ENDOGROUPE else "")
    A38.ecrire(hum, "a38-desirabilite-humaine-par-camp.csv")

    camp = pd.concat(par_camp, ignore_index=True)
    camp["classe_norc"] = camp.item.map(classes)
    camp["type"] = camp.item.map(types)
    camp["classe_comportement"] = camp.item.map(A38.classe_comportement)
    camp["pole_endogroupe"] = camp.item.map(
        lambda it: A38.POLE_ENDOGROUPE[it][0] if it in A38.POLE_ENDOGROUPE else "")
    A38.ecrire(camp, "a38-par-camp.csv")

    # controle : les chiffres en population entiere doivent reproduire a28
    ref = os.path.join(A38.SORTIE, "a28-t1-par-item.csv")
    if os.path.exists(ref):
        a = pd.read_csv(ref)
        a["perimetre"] = a.perimetre.astype(str)
        b = tout[tout.camp == "tous"].copy()
        b["perimetre"] = b.perimetre.astype(str)
        f = a.merge(b, on=["perimetre", "condition", "item"], suffixes=("_a28", "_a38"))
        ecart = np.nanmax(np.abs(f.distance_a28.values - f.distance_a38.values))
        print(f"\ncontrole de reproduction de a28 sur {len(f)} couples : "
              f"ecart maximal de distance = {ecart:.2e}")


if __name__ == "__main__":
    main()
