"""
t1_placebo : l'ablation propre de l'etiquette ideologique, sur une condition dont on
controle entierement l'entree.

POURQUOI. a47 E2 montre que sur le GSS la chute sous permutation change d'un facteur 2,6 a
3,7 selon que le segment contient ou non l'ideologie, et seulement pour `agents v8` et
`C2`, les deux conditions qui recoivent l'etiquette ideologique en clair. La lecture
causale proposee est : permuter a l'interieur de la variable que la condition a recue
mesure ce qu'elle sait au dela de ce qu'on vient de fixer, donc rabote sa chute. Cette
lecture n'a jamais ete testee par une ablation, a44 E1 le dit explicitement.

Sur Twin, aucune configuration d'agent ne recoit d'etiquette ideologique explicite selon
la lecture de i3b section 4.4, et ce point n'est pas verifiable depuis data/. Mais
`B1 argmax` de t1, LUI, recoit les quatorze questions du bloc Demographics, dont `QID22`
opinions politiques et `QID20` parti. Son entree est ecrite dans t1_baselines.py, donc
elle est entierement controlee.

CE QUE FAIT CE SCRIPT. Il refait `B1 argmax` a l'identique en retirant les deux seules
colonnes politiques, `QID22` et `QID20`, et rien d'autre. C'est une ablation propre au
sens de a44 E1 : meme moteur, meme run, meme protocole, une seule chose change. Puis il
mesure la chute sous `S_ideo` et sous `S_gra` pour les deux versions.

PREDICTION, ecrite avant le calcul : si la lecture causale de a47 est juste, le rapport
`S_gra / S_ideo` doit BAISSER quand on retire l'ideologie de l'entree, et la chute sous
`S_ideo` doit MONTER.

Sortie : resultats/t1-placebo-etiquette.csv
Usage  : .venv/bin/python analyses/t1_placebo.py
"""

import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                                       # noqa: E402
from sklearn.linear_model import LogisticRegression      # noqa: E402

import t1_commun as C                                    # noqa: E402
import a44_commun as C44                                 # noqa: E402
import t1_baselines as B                                 # noqa: E402
from a2_commun import encodeur_demographies, est_manquant  # noqa: E402

POLITIQUES = ["QID22", "QID20"]


def b1(paq, colonnes):
    """B1 argmax restreint aux colonnes demographiques indiquees. Meme code que
    t1_baselines, memes plis, meme graine, seule la matrice d'entree change."""
    demo = paq["demo"]["colonnes_demo"]
    garder = [i for i, c in enumerate(demo) if c in colonnes]
    x = paq["demo"]["x"][:, garder]
    y = paq["codes"][C.REF]
    yo = B._codes_objets(y)
    n, m = y.shape
    pred = np.empty((n, m), dtype=object)
    for tr, te in B.plis(n):
        enc = encodeur_demographies(x[tr])
        Xt, Xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            col = yo[tr, j]
            obs = np.array([not est_manquant(v) for v in col])
            vus = [v for v in col if not est_manquant(v)]
            if not vus:
                continue
            classes = list(dict.fromkeys(vus))
            if len(classes) == 1:
                pred[te, j] = classes[0]
                continue
            rang = {c: i for i, c in enumerate(classes)}
            mod = LogisticRegression(max_iter=2000, C=B.FORCE)
            mod.fit(Xt[obs], np.array([rang[v] for v in np.asarray(col)[obs]]))
            pred[te, j] = [classes[i] for i in mod.predict(Xe)]
    return B._vers_codes(pred, (n, m))


def main():
    t0 = time.time()
    paq = C.charger()
    demo = paq["demo"]["colonnes_demo"]
    print(f"bloc Demographics : {len(demo)} questions, {demo}", flush=True)
    versions = {
        "B1 argmax, quatorze demographies": demo,
        "B1 argmax, sans ideologie ni parti": [c for c in demo if c not in POLITIQUES],
    }
    y_ref = paq["codes"][C.REF]
    rng = np.random.default_rng(C.GRAINE + 30)
    lignes = []
    codes = {}
    for nom, cols in versions.items():
        codes[nom] = b1(paq, cols)
        print(f"  {nom} calcule, {time.time() - t0:.0f}s", flush=True)

    plancher = {}
    for nom_seg in ("S_ideo", "S_fin", "S_gra", "S_parti"):
        s = paq["seg"][nom_seg]
        cd = paq["codes"][C.PLANCHER]
        v = float(np.nanmean(C.exactitude_codes(cd, y_ref)))
        p = np.mean([float(np.nanmean(C.exactitude_codes(
            cd[C44.permuter_intra(paq["n"], s, rng)], y_ref)))
            for _ in range(C.N_PERMUTATIONS)])
        plancher[nom_seg] = (v - p) / v

    for nom, cd in codes.items():
        for nom_seg in ("S_ideo", "S_fin", "S_gra", "S_parti"):
            s = paq["seg"][nom_seg]
            v = float(np.nanmean(C.exactitude_codes(cd, y_ref)))
            perms = np.array([float(np.nanmean(C.exactitude_codes(
                cd[C44.permuter_intra(paq["n"], s, rng)], y_ref)))
                for _ in range(C.N_PERMUTATIONS)])
            moyp = float(perms.mean())
            lignes.append({
                "condition": nom, "segmentation": nom_seg,
                "n_colonnes_demographiques": len(versions[nom]),
                "exactitude_vraie": v, "exactitude_permutee": moyp,
                "chute": v - moyp, "chute_relative": (v - moyp) / v,
                "plancher_humain_chute_relative": plancher[nom_seg],
                "part_du_plancher_humain": ((v - moyp) / v) / plancher[nom_seg]})
    C.ecrire(lignes, "t1-placebo-etiquette.csv")
    for nom in versions:
        d = {l["segmentation"]: l["part_du_plancher_humain"] for l in lignes
             if l["condition"] == nom}
        print(f"  {nom:38s} S_ideo {d['S_ideo']:.4f}  S_gra {d['S_gra']:.4f}  "
              f"facteur {d['S_gra'] / d['S_ideo']:.3f}")
    print(f"termine en {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
