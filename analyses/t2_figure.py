"""
t2_figure : la figure de T2, trois panneaux.

Preenregistrement : resultats/t2-preenregistrement.md, section 6.

  A. Erreur absolue du predicteur de groupe contre celle du nul a derive, item par item,
     sur le taux de changement et sur le deplacement projete.
  B. Rapport reel sur nul par panel et par delai, avec la valeur du SCE en reference.
  C. Correlation des profils de groupe entre deux moities de l'echantillon, par cible et
     par axe, avec la bande de permutation de l'etiquette de groupe.

Sorties : resultats/t2-figure-qui-bouge-agrege.png et .svg.

Usage : .venv/bin/python analyses/t2_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t2_commun as T2

R = T2.SORTIE
BLEU, ROUGE, GRIS, VERT = "#1f4e79", "#b03a2e", "#7f7f7f", "#1e7a52"


def tracer():
    plt.rcParams.update({"font.size": 8.5, "axes.titlesize": 9.5,
                         "axes.labelsize": 8.5, "figure.dpi": 150})
    fig = plt.figure(figsize=(13.2, 4.5))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.05, 1.25], wspace=0.30)

    # ---- A : erreur par item, groupe contre nul ----------------------------
    ax = fig.add_subplot(gs[0, 0])
    ei = pd.read_csv(os.path.join(R, "t2-erreur-par-item.csv"))
    for cible, coul, lab, mk in (("tau", BLEU, "taux de changement", "o"),
                                 ("pi", ROUGE, "deplacement projete", "^")):
        d = ei[ei.cible == cible]
        ax.scatter(d.erreur_M0, d.erreur_M4, s=13, alpha=0.62, c=coul, label=lab,
                   marker=mk, linewidths=0)
    lim = [0, max(ei.erreur_M0.max(), ei.erreur_M4.max()) * 1.05]
    ax.plot(lim, lim, color="black", lw=0.9, ls="--", zorder=0)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("erreur du nul a derive M0, points")
    ax.set_ylabel("erreur du predicteur de groupe M4, points")
    ax.set_title("A. Un item, un point. Sous la diagonale,\nle groupe apporte quelque chose",
                 loc="left")
    ax.legend(frameon=False, loc="upper left", fontsize=7.5)
    ax.grid(alpha=0.25, lw=0.5)

    # ---- B : rapport reel sur nul -------------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    am = pd.read_csv(os.path.join(R, "t2-amplitude.csv"))
    d = am[(am.decoupe == "panel") & (am.variante.str.startswith("N1"))].copy()
    d = d.sort_values(["quantite", "perimetre", "cle"])
    etiquettes, y, yl, yh, coul = [], [], [], [], []
    for q, c in (("nombre d'items changes", BLEU), ("distance ordinale", VERT)):
        for per, marq in (("4ans", "4 ans"), ("2ans", "2 ans")):
            s = d[(d.quantite == q) & (d.perimetre == per)]
            for r in s.itertuples():
                etiquettes.append(f"{r.cle}, {marq}")
                y.append(r.rapport)
                yl.append(r.rapport - r.ic_bas)
                yh.append(r.ic_haut - r.rapport)
                coul.append(c)
    pos = np.arange(len(y))
    ax.errorbar(y, pos, xerr=[yl, yh], fmt="none", ecolor=GRIS, lw=1.0, capsize=2)
    ax.scatter(y, pos, c=coul, s=22, zorder=3)
    ax.set_yticks(pos)
    ax.set_yticklabels(etiquettes, fontsize=6.4)
    ax.invert_yaxis()
    ens = am[(am.decoupe == "ensemble") & (am.variante.str.startswith("N1"))
             & (am.perimetre == "4ans") & (am.quantite == "nombre d'items changes")]
    ax.axvline(float(ens.rapport.iloc[0]), color=BLEU, lw=1.1, ls="-",
               label=f"GSS, ensemble a quatre ans : {float(ens.rapport.iloc[0]):.3f}")
    ax.axvline(0.43, color=ROUGE, lw=1.1, ls="--", label="SCE, menages, C1 : 0,43")
    ax.axvline(1.0, color="black", lw=0.8, ls=":", label="egalite reel et nul")
    ax.set_xlim(0.40, 1.06)
    ax.set_xlabel("rapport reel sur nul de l'amplitude")
    ax.set_title("B. Une population sans personnes bouge trop.\nBleu, items changes ; "
                 "vert, distance ordinale", loc="left")
    ax.legend(frameon=False, loc="upper right", fontsize=6.6)
    ax.grid(axis="x", alpha=0.25, lw=0.5)

    # ---- C : correlation des profils de groupe entre deux moities -----------
    ax = fig.add_subplot(gs[0, 2])
    bp = pd.read_csv(os.path.join(R, "t2-permutation-groupes.csv"))
    noms = {"tau": "qui change", "pi": "sens du deplacement",
            "mu": "deplacement ordinal"}
    coulc = {"tau": BLEU, "pi": ROUGE, "mu": VERT}
    axes_ordre = ["camp", "age", "education", "genre"]
    largeur = 0.26
    base = np.arange(len(axes_ordre))
    for k, c in enumerate(["tau", "pi", "mu"]):
        s = bp[bp.cible == c].set_index("axe")
        v = [float(s.loc[a, "correlation_observee"]) if a in s.index else np.nan
             for a in axes_ordre]
        b95 = [float(s.loc[a, "correlation_permutee_p95"]) if a in s.index else np.nan
               for a in axes_ordre]
        x = base + (k - 1) * largeur
        ax.bar(x, v, width=largeur * 0.9, color=coulc[c], label=noms[c], alpha=0.88)
        ax.plot(np.repeat(x, 3).reshape(-1, 3).T[[0, 0]] +
                np.array([[-largeur * 0.45], [largeur * 0.45]]),
                np.array([b95, b95]), color="black", lw=1.0)
    ax.set_xticks(base)
    ax.set_xticklabels(axes_ordre)
    ax.axhline(0, color="black", lw=0.7)
    ax.set_ylabel("correlation des profils de groupe,\ndeux moities de l'echantillon")
    ax.set_title("C. Les groupes different ils de facon reproductible ?\n"
                 "Trait noir, 95e centile de la permutation d'etiquette", loc="left")
    ax.legend(frameon=False, loc="upper right", fontsize=7.2)
    ax.grid(axis="y", alpha=0.25, lw=0.5)

    fig.suptitle("T2. Qui bouge, version agregee : le groupe se predit sur le taux de "
                 "changement, jamais sur le sens ; et le nul a derive bouge trop",
                 x=0.008, ha="left", fontsize=10.5, y=1.005)
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    for ext in ("png", "svg"):
        chemin = os.path.join(R, f"t2-figure-qui-bouge-agrege.{ext}")
        fig.savefig(chemin, bbox_inches="tight")
        print("ecrit", chemin, flush=True)


if __name__ == "__main__":
    tracer()
