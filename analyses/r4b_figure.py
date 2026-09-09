"""
r4b_figure : la figure de R4, la decomposition format contre poids.

Statut : script d'analyse jetable. Aucun appel de modele. Lecture seule sur les tableaux
de resultats/. Aucun script existant n'est modifie.

Quatre panneaux.
  (a) le facteur d'amplification signe H2b, quatre conditions, deux identites, avec IC
      bootstrap sur les items et le plancher de reinterrogation humaine ;
  (b) la decomposition : du gabarit ChatML au socle, en passant par le format seul, avec
      les IC des deux marches ;
  (c) le ratio de dispersion H1 par camp et par condition ;
  (d) la difference `TV(decrit, echantillon) - TV(decrit, national)` de H4 par condition.

Entree  : resultats/r1-h2-ecart-r4.csv, r1-h1-unanimite-r4.csv, r4b-contraste-h2b.csv,
          r4-h4-restitution.csv
Sortie  : resultats/r4b-figure-decomposition.png et .svg

Usage :
  .venv/bin/python analyses/r4b_figure.py
"""

import os

import numpy as np
import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

FOND, ENCRE, ENCRE2, GRILLE = "#fcfcfb", "#0b0b0b", "#52514e", "#e2e1dd"
COULEUR_CAMP = {"gauche": "#2a78d6", "centre": "#8a8a86", "droite": "#c8412b"}
HUMAIN = "#1f7a52"
COULEUR = {"q4": "#7a3fa8", "q4nogab": "#d18b1e", "q4base": "#0b6a8f", "q4hyb": "#a8324a"}
NOM = {
    "q4": "Instruct-2507\ngabarit ChatML\n(R1)",
    "q4nogab": "Instruct-2507\ncompletion 3 ex.",
    "q4base": "Base\ncompletion 3 ex.",
    "q4hyb": "Qwen3-4B hybride\ncompletion 3 ex.",
}
ORDRE = ("q4", "q4nogab", "q4base", "q4hyb")


def style(ax):
    ax.set_facecolor(FOND)
    ax.grid(True, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(ENCRE2)
    ax.tick_params(colors=ENCRE2, labelsize=8)


def main():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    h2 = pd.read_csv(os.path.join(SORTIE, "r1-h2-ecart-r4.csv"))
    h1 = pd.read_csv(os.path.join(SORTIE, "r1-h1-unanimite-r4.csv"))
    ct = pd.read_csv(os.path.join(SORTIE, "r4b-contraste-h2b.csv"))
    h4 = pd.read_csv(os.path.join(SORTIE, "r4-h4-restitution.csv"))

    h2b = h2[(h2["hypothese"].str.startswith("H2b"))
             & (h2["perimetre"] == "79 items orientes")]

    fig, axes = plt.subplots(2, 2, figsize=(11.4, 8.4), facecolor=FOND)

    # (a) facteur H2b
    ax = axes[0][0]
    style(ax)
    largeur = 0.36
    for j, identite in enumerate(("journaliste", "adversaire")):
        xs, ys, bas, haut = [], [], [], []
        for i, cle in enumerate(ORDRE):
            r = h2b[(h2b["cle_modele"] == cle) & (h2b["identite"] == identite)]
            if not len(r):
                continue
            r = r.iloc[0]
            xs.append(i + (j - 0.5) * largeur)
            ys.append(r["facteur"])
            bas.append(r["facteur"] - r["ic_bas"])
            haut.append(r["ic_haut"] - r["facteur"])
        ax.bar(xs, ys, width=largeur * 0.92,
               color=[COULEUR[c] for c in ORDRE], alpha=1.0 if j == 0 else 0.45,
               edgecolor=ENCRE, linewidth=0.4, zorder=3,
               label="journaliste" if j == 0 else "adversaire")
        ax.errorbar(xs, ys, yerr=[bas, haut], fmt="none", ecolor=ENCRE,
                    elinewidth=1.0, capsize=3, zorder=4)
    ax.axhline(1.0, color=HUMAIN, linewidth=1.4, zorder=5)
    ax.text(3.42, 1.02, "plancher humain 1,01", color=HUMAIN, fontsize=7.5, ha="right")
    ax.set_xticks(range(len(ORDRE)))
    ax.set_xticklabels([NOM[c] for c in ORDRE], fontsize=7.5, color=ENCRE)
    ax.set_ylabel("ecart entre camps decrit, en part du reel", fontsize=8.5, color=ENCRE)
    ax.set_title("(a) H2b, 79 items orientes : le meme fichier de poids passe de 0,25 a 0,73\n"
                 "quand on retire le gabarit de conversation",
                 fontsize=9, color=ENCRE, loc="left")
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    ax.set_ylim(0, 1.35)

    # (b) decomposition
    ax = axes[0][1]
    style(ax)
    c = ct[(ct["perimetre"] == "79 items orientes") & (ct["identite"] == "journaliste")]
    f_q4 = float(c[c["condition_b"] == "q4"].iloc[0]["facteur_b"])
    fmt = c[(c["condition_a"] == "q4nogab") & (c["condition_b"] == "q4")].iloc[0]
    poids = c[(c["condition_a"] == "q4base") & (c["condition_b"] == "q4nogab")].iloc[0]
    niveaux = [("gabarit ChatML\n(R1, q4)", f_q4, None),
               ("+ format\ncompletion 3 ex.", f_q4 + fmt["difference_de_facteurs"], fmt),
               ("+ poids du socle\n(q4base)",
                f_q4 + fmt["difference_de_facteurs"] + poids["difference_de_facteurs"], poids)]
    xs = np.arange(3)
    ax.plot(xs, [n[1] for n in niveaux], color=ENCRE, linewidth=1.2, zorder=3,
            marker="o", markersize=7,
            markerfacecolor=[COULEUR["q4"], COULEUR["q4nogab"], COULEUR["q4base"]][0])
    for i, (nom, v, ct_r) in enumerate(niveaux):
        ax.plot([i], [v], marker="o", markersize=9, zorder=5,
                color=[COULEUR["q4"], COULEUR["q4nogab"], COULEUR["q4base"]][i])
        ax.annotate(f"{v:.3f}".replace(".", ","), (i, v), textcoords="offset points",
                    xytext=(0, 12), ha="center", fontsize=8.5, color=ENCRE)
        if ct_r is not None:
            d = ct_r["difference_de_facteurs"]
            ax.annotate(f"{d:+.3f}".replace(".", ",")
                        + f"\n[{ct_r['ic_bas']:+.3f} ; {ct_r['ic_haut']:+.3f}]".replace(".", ","),
                        (i - 0.5, (v + niveaux[i - 1][1]) / 2), ha="center", va="center",
                        fontsize=7.5, color=ENCRE2,
                        bbox=dict(boxstyle="round,pad=0.25", facecolor=FOND,
                                  edgecolor=GRILLE, linewidth=0.6))
    ax.axhline(1.0, color=HUMAIN, linewidth=1.4, zorder=2)
    ax.axhline(float(h2b[(h2b["cle_modele"] == "q4hyb")
                         & (h2b["identite"] == "journaliste")].iloc[0]["facteur"]),
               color=COULEUR["q4hyb"], linewidth=1.1, linestyle="--", zorder=2)
    ax.text(2.45, 0.275, "Qwen3-4B hybride, meme format : 0,262",
            color=COULEUR["q4hyb"], fontsize=7.5, ha="right")
    ax.text(2.45, 1.02, "plancher humain 1,01", color=HUMAIN, fontsize=7.5, ha="right")
    ax.set_xticks(xs)
    ax.set_xticklabels([n[0] for n in niveaux], fontsize=8, color=ENCRE)
    ax.set_xlim(-0.55, 2.55)
    ax.set_ylim(0, 1.2)
    ax.set_ylabel("ecart entre camps decrit, en part du reel", fontsize=8.5, color=ENCRE)
    ax.set_title("(b) la marche du format est plus grande que l'ecart total :\n"
                 "les poids du socle ramenent vers le bas, pas vers le haut",
                 fontsize=9, color=ENCRE, loc="left")

    # (c) H1 par camp
    ax = axes[1][0]
    style(ax)
    g = h1[h1["identite"] == "journaliste"]
    largeur = 0.2
    for j, camp in enumerate(("gauche", "centre", "droite")):
        xs, ys, bas, haut = [], [], [], []
        for i, cle in enumerate(ORDRE):
            r = g[(g["cle_modele"] == cle) & (g["camp"] == camp)]
            if not len(r):
                continue
            r = r.iloc[0]
            xs.append(i + (j - 1) * largeur)
            ys.append(r["ratio"])
            bas.append(r["ratio"] - r["ic_bas"])
            haut.append(r["ic_haut"] - r["ratio"])
        ax.bar(xs, ys, width=largeur * 0.88, color=COULEUR_CAMP[camp],
               edgecolor=ENCRE, linewidth=0.4, zorder=3, label=camp)
        ax.errorbar(xs, ys, yerr=[bas, haut], fmt="none", ecolor=ENCRE,
                    elinewidth=0.9, capsize=2.5, zorder=4)
    ax.axhline(1.0, color=HUMAIN, linewidth=1.4, zorder=5)
    ax.set_xticks(range(len(ORDRE)))
    ax.set_xticklabels([NOM[c] for c in ORDRE], fontsize=7.5, color=ENCRE)
    ax.set_ylim(0.9, 1.42)
    ax.set_ylabel("dispersion decrite / dispersion reelle", fontsize=8.5, color=ENCRE)
    ax.legend(fontsize=7.5, frameon=False, ncol=3, loc="upper left")
    ax.set_title("(c) H1 : les quatre conditions sur decrivent la variete interne.\n"
                 "Le socle n'est pas plus proche de 1 que l'instruit",
                 fontsize=9, color=ENCRE, loc="left")

    # (d) H4
    ax = axes[1][1]
    style(ax)
    largeur = 0.36
    for j, identite in enumerate(("journaliste", "adversaire")):
        xs, ys, bas, haut = [], [], [], []
        for i, cle in enumerate(ORDRE):
            r = h4[(h4["cle_modele"] == cle) & (h4["identite"] == identite)]
            if not len(r):
                continue
            r = r.iloc[0]
            xs.append(i + (j - 0.5) * largeur)
            ys.append(r["difference_moyenne"])
            bas.append(r["difference_moyenne"] - r["ic_bas"])
            haut.append(r["ic_haut"] - r["difference_moyenne"])
        ax.bar(xs, ys, width=largeur * 0.92, color=[COULEUR[c] for c in ORDRE],
               alpha=1.0 if j == 0 else 0.45, edgecolor=ENCRE, linewidth=0.4, zorder=3,
               label="journaliste" if j == 0 else "adversaire")
        ax.errorbar(xs, ys, yerr=[bas, haut], fmt="none", ecolor=ENCRE,
                    elinewidth=1.0, capsize=3, zorder=4)
    ax.axhline(0.0, color=ENCRE, linewidth=1.0, zorder=5)
    ax.set_xticks(range(len(ORDRE)))
    ax.set_xticklabels([NOM[c] for c in ORDRE], fontsize=7.5, color=ENCRE)
    ax.set_ylabel("TV(decrit, echantillon) - TV(decrit, national)", fontsize=8.5, color=ENCRE)
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    ax.set_title("(d) H4 : l'attraction vers les marginales nationales est portee\n"
                 "par le gabarit, pas par les poids",
                 fontsize=9, color=ENCRE, loc="left")

    fig.suptitle("r4. Le socle contre l'instruit : le format d'invite porte plus que "
                 "les poids sur l'ecart entre camps decrit",
                 fontsize=11.5, color=ENCRE, y=0.985)
    fig.text(0.5, 0.008,
             "149 items du GSS, 3 camps, 2 identites, 894 cellules par condition, "
             "temperature 0. IC 95 % bootstrap sur les items, 2 000 tirages.\n"
             "Le contraste socle contre instruit-2507 est declare non apparie ; "
             "la paire appariee du socle est Qwen3-4B hybride (a27, 4.4).",
             ha="center", fontsize=7.5, color=ENCRE2)
    fig.tight_layout(rect=[0, 0.042, 1, 0.955])
    base = os.path.join(SORTIE, "r4b-figure-decomposition")
    for ext in ("png", "svg"):
        fig.savefig(f"{base}.{ext}", dpi=200, facecolor=FOND)
    plt.close(fig)
    print(f"ecrit {base}.png et .svg")


if __name__ == "__main__":
    main()
