"""
a46b_figure : la figure du rapport a46, exageration du modele contre exageration humaine.

Ne recalcule rien : lit resultats/a46b-par-item.csv et a46b-taux-de-base.csv, pour que la
figure et les chiffres du rapport ne puissent pas diverger. Aucun appel de modele.

Trois panneaux.
  A. Le rapport des exagerations, echelle logarithmique sur les deux axes. En abscisse
     l'exageration humaine, perception YouGov divisee par la realite d'Ahler et Sood ; en
     ordonnee l'exageration du modele, croyance divisee par la realite du GSS 2024 de la
     population qui lui a ete decrite, c'est a dire la lecture « base propre » de la page
     de plan. La diagonale est l'egalite. Au dessus, le modele exagere plus que les
     humains ; au dessous, il corrige. Le point est la moyenne des quatre cellules de
     protocole, deux ancrages et deux identites ; la barre en est l'etendue.
  B. Le meme fait en POINTS, contre la realite d'Ahler et Sood, seule echelle ou une
     reponse zero se represente. Aucun item n'y est retire.
  C. Le taux de base : ce que le modele donne pour la population entiere contre la part
     reelle dans les 1 052 personnes du jeu de Stanford. C'est le controle H4.

Entrees : resultats/a46b-par-item.csv, resultats/a46b-taux-de-base.csv
Sorties : resultats/a46b-figure-trois-termes.png et .svg

Usage : .venv/bin/python analyses/a46b_figure.py
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
NEUTRE = "#8d8b86"

# Trois series, trois emplacements categoriels valides toutes paires en mode clair
# (validate_palette.js, ecart CVD 9,2 et vision normale 24,0). Forme de marqueur en
# encodage secondaire : l'identite n'est jamais portee par la couleur seule.
COULEUR = {"q4": "#2a78d6", "oss20": "#eb6834", "q30": "#1baf7a"}
MARQUEUR = {"q4": "o", "oss20": "s", "q30": "^"}
NOM = {"q4": "Qwen3-4B", "oss20": "gpt-oss-20b", "q30": "Qwen3-30B-A3B"}
ORDRE_MODELE = ["q4", "oss20", "q30"]

ORDRE = ["dem_black", "dem_union", "dem_aa", "dem_lgb",
         "rep_evang", "rep_rich", "rep_old", "rep_south"]
COURT = {"dem_black": "noirs, dem.", "dem_union": "syndiques, dem.",
         "dem_aa": "athees, dem.", "dem_lgb": "LGB, dem.",
         "rep_evang": "evangeliques, rep.", "rep_rich": "> 250 k$, rep.",
         "rep_old": "65 ans et +, rep.", "rep_south": "sudistes, rep."}
PLANCHER = 0.017  # ou l'on epingle les couples dont les quatre cellules valent zero


def style(ax, grille="both"):
    ax.set_facecolor(FOND)
    ax.grid(True, axis=grille, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=8.5, length=3)


def panneau_a(ax, d):
    ax.set_xscale("log")
    ax.set_yscale("log")
    limx, limy = (0.92, 24.0), (0.0135, 19.0)
    ax.plot([limx[0], limx[1]], [limx[0], limx[1]], color=NEUTRE, linewidth=1.4,
            linestyle=(0, (5, 3)), zorder=1)
    ax.axhline(1.0, color=GRILLE, linewidth=1.0, zorder=1)
    xx = np.geomspace(limx[0], limx[1], 200)
    ax.fill_between(xx, xx, limy[1], color="#e34948", alpha=0.035, zorder=0)

    for cle in ORDRE_MODELE:
        g = d[d["cle_modele"] == cle]
        x = g["exag_humaine"].to_numpy(float)
        y = g["exag_modele_moy"].to_numpy(float)
        bas = g["exag_modele_min"].to_numpy(float)
        haut = g["exag_modele_max"].to_numpy(float)
        nul = g["n_zero"].to_numpy(int) > 0
        yv = np.where(y > 0, y, PLANCHER)
        for i in range(len(x)):
            if bas[i] > 0 and haut[i] > 0 and haut[i] > bas[i]:
                ax.plot([x[i], x[i]], [bas[i], haut[i]], color=COULEUR[cle],
                        linewidth=2.0, alpha=0.45, solid_capstyle="round", zorder=2)
        ax.scatter(x[~nul], yv[~nul], s=64, marker=MARQUEUR[cle], color=COULEUR[cle],
                   edgecolors=FOND, linewidths=2.0, zorder=3, label=NOM[cle])
        if nul.any():
            ax.scatter(x[nul], yv[nul], s=64, marker=MARQUEUR[cle], facecolors="none",
                       edgecolors=COULEUR[cle], linewidths=1.8, zorder=3,
                       label=("au moins une cellule a reponse 0" if cle == "oss20"
                              else None))

    # Etiquettes directes des items, une seule fois, sur le modele mediane q30.
    ref = d[d["cle_modele"] == "q30"]
    for _, r in ref.iterrows():
        yv = r["exag_modele_moy"] if r["exag_modele_moy"] > 0 else PLANCHER
        ax.annotate(COURT[r["item_as"]], (r["exag_humaine"], yv),
                    textcoords="offset points", xytext=(9, -3), fontsize=7.6,
                    color=ENCRE_SECONDE, zorder=4)

    for _, r in d[d["exag_modele_moy"] <= 0].iterrows():
        droite = r["exag_humaine"] > 5
        ax.annotate(f"{COURT[r['item_as']]} : gpt-oss-20b repond 0\naux quatre cellules, "
                    f"rapport indefini",
                    (r["exag_humaine"], PLANCHER), textcoords="offset points",
                    xytext=(-11 if droite else 11, 5), fontsize=7.4,
                    ha="right" if droite else "left",
                    color=ENCRE_SECONDE, zorder=4)
    ax.text(4.6, 14.0, "le modele exagere PLUS que les humains", fontsize=8.8,
            color="#c8412b", style="italic")
    ax.text(1.02, 0.033, "le modele exagere MOINS que les humains : il corrige",
            fontsize=8.8, color=ENCRE_SECONDE, style="italic")
    ax.set_xlim(*limx)
    ax.set_ylim(*limy)
    ax.set_xlabel("exageration humaine, perception YouGov / realite ANES 2012 (log)",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_ylabel("exageration du modele, croyance / realite GSS 2024 (log)",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("A. Le rapport des exagerations, base propre, moyenne des quatre "
                 "cellules de protocole",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    style(ax)
    leg = ax.legend(frameon=False, fontsize=8.8, loc="upper left",
                    handletextpad=0.4, borderpad=0.2)
    for t in leg.get_texts():
        t.set_color(ENCRE_SECONDE)


def panneau_b(ax, d):
    y = np.arange(len(ORDRE))[::-1]
    pos = {k: v for k, v in zip(ORDRE, y)}
    ax.axvline(0.0, color=NEUTRE, linewidth=1.4, zorder=1)
    hum = d.drop_duplicates("item_as").set_index("item_as")
    for item in ORDRE:
        h = float(hum.loc[item, "ecart_humain_points"])
        ax.plot([0, h], [pos[item] + 0.30, pos[item] + 0.30], color=NEUTRE,
                linewidth=2.0, solid_capstyle="round", zorder=2)
        ax.scatter([h], [pos[item] + 0.30], s=58, marker="D", color=ENCRE_SECONDE,
                   edgecolors=FOND, linewidths=1.6, zorder=3,
                   label="humains, YouGov" if item == ORDRE[0] else None)
    dec = {"q4": 0.02, "oss20": -0.20, "q30": -0.42}
    for cle in ORDRE_MODELE:
        g = d[d["cle_modele"] == cle].set_index("item_as")
        for item in ORDRE:
            m = float(g.loc[item, "ecart_modele_points_moy"])
            lo = float(g.loc[item, "ecart_modele_points_min"])
            hi = float(g.loc[item, "ecart_modele_points_max"])
            yy = pos[item] + dec[cle]
            ax.plot([lo, hi], [yy, yy], color=COULEUR[cle], linewidth=2.0, alpha=0.45,
                    solid_capstyle="round", zorder=2)
            ax.scatter([m], [yy], s=52, marker=MARQUEUR[cle], color=COULEUR[cle],
                       edgecolors=FOND, linewidths=1.6, zorder=3,
                       label=NOM[cle] if item == ORDRE[0] else None)
    ax.set_yticks(y)
    ax.set_yticklabels([COURT[i] for i in ORDRE], fontsize=8.6, color=ENCRE)
    ax.set_ylim(-0.8, len(ORDRE) - 0.35)
    ax.set_xlabel("ecart a la realite d'Ahler et Sood, en points de pourcentage",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("B. Le meme fait en points : aucune cellule retiree, zeros compris",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    style(ax, grille="x")
    leg = ax.legend(frameon=False, fontsize=8.2, loc="upper right", ncol=1,
                    handletextpad=0.4, borderpad=0.2)
    for t in leg.get_texts():
        t.set_color(ENCRE_SECONDE)


def panneau_c(ax, tb):
    ax.plot([0, 55], [0, 55], color=NEUTRE, linewidth=1.4, linestyle=(0, (5, 3)),
            zorder=1)
    b = tb.drop_duplicates(["item_as", "cle_modele"])
    for cle in ORDRE_MODELE:
        g = b[b["cle_modele"] == cle]
        ax.scatter(g["reel_population_gss"], g["modele_population"], s=64,
                   marker=MARQUEUR[cle], color=COULEUR[cle], edgecolors=FOND,
                   linewidths=2.0, zorder=3, label=NOM[cle])
    ref = b[b["cle_modele"] == "q30"]
    for _, r in ref.iterrows():
        ax.annotate(COURT[r["item_as"]], (r["reel_population_gss"],
                                          r["modele_population"]),
                    textcoords="offset points", xytext=(8, -3), fontsize=7.4,
                    color=ENCRE_SECONDE, zorder=4)
    ax.set_xlim(0, 55)
    ax.set_ylim(0, 55)
    ax.set_xlabel("part reelle dans les 1 052 personnes du GSS 2024, en %",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_ylabel("part donnee par le modele pour la population entiere, en %",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("C. Le taux de base, controle H4 : huit cellules sans camp",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    style(ax)
    leg = ax.legend(frameon=False, fontsize=8.6, loc="upper left",
                    handletextpad=0.4, borderpad=0.2)
    for t in leg.get_texts():
        t.set_color(ENCRE_SECONDE)


def main():
    p = pd.read_csv(os.path.join(SORTIE, "a46b-par-item.csv"))
    tb = pd.read_csv(os.path.join(SORTIE, "a46b-taux-de-base.csv"))

    lignes = []
    for (item, cle), g in p.groupby(["item_as", "cle_modele"]):
        r = g["exageration_modele_ratio_gss"].to_numpy(float)
        pos = r[r > 0]
        lignes.append({
            "item_as": item, "cle_modele": cle,
            "exag_humaine": float(g["exageration_humaine_ratio_as"].iloc[0]),
            "exag_modele_moy": float(pos.mean()) if len(pos) else 0.0,
            "exag_modele_min": float(pos.min()) if len(pos) else np.nan,
            "exag_modele_max": float(pos.max()) if len(pos) else np.nan,
            "n_zero": int((r <= 0).sum()),
            "ecart_humain_points": float(g["ecart_humain_moins_reel_as_points"].iloc[0]),
            "ecart_modele_points_moy": float(g["ecart_modele_moins_reel_as_points"].mean()),
            "ecart_modele_points_min": float(g["ecart_modele_moins_reel_as_points"].min()),
            "ecart_modele_points_max": float(g["ecart_modele_moins_reel_as_points"].max()),
        })
    d = pd.DataFrame(lignes)
    d["ordre"] = d["item_as"].map({k: i for i, k in enumerate(ORDRE)})
    d = d.sort_values(["ordre", "cle_modele"])

    fig = plt.figure(figsize=(13.6, 10.9), facecolor=FOND)
    gs = fig.add_gridspec(2, 2, height_ratios=[0.94, 1.0], hspace=0.30, wspace=0.22,
                          left=0.108, right=0.978, top=0.905, bottom=0.072)
    panneau_a(fig.add_subplot(gs[0, :]), d)
    panneau_b(fig.add_subplot(gs[1, 0]), d)
    panneau_c(fig.add_subplot(gs[1, 1]), tb)

    fig.suptitle("a46. Exageration du modele contre exageration humaine sur les huit "
                 "compositions d'Ahler et Sood",
                 fontsize=13.5, color=ENCRE, x=0.045, ha="left", y=0.972)
    fig.text(0.045, 0.940,
             "Trois modeles ouverts, 40 cellules chacun, temperature 0. Referent humain : "
             "1 000 adultes YouGov, Ahler et Sood 2018. Le point est la moyenne des "
             "quatre cellules de protocole, la barre leur etendue.",
             fontsize=9, color=ENCRE_SECONDE, ha="left")

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a46b-figure-trois-termes.{ext}")
        fig.savefig(chemin, dpi=170 if ext == "png" else None, facecolor=FOND)
        print(chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
