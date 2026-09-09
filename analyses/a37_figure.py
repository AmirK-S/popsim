"""
a37_figure : la figure du rapport a37.

Ne recalcule rien. Lit les tableaux produits par a37_humains.py et a37_agents.py, pour que
la figure et les chiffres du rapport ne puissent pas diverger. Aucun appel de modele.

Quatre panneaux.
  A. Humains du GSS : rapport de dispersion droite sur gauche de chaque item contre la
     derive agregee de cet item, avec la droite de regression. C'est le test direct du
     modele generatif de Brandt et Sleegers.
  B. Deux conditions d'agents sur les memes 1 052 personnes et les memes items : la
     condition demographique de Stanford qui porte l'etiquette ideologique (v8) et la
     condition enquete qui ne la porte pas.
  C. Nos deux conditions locales sur les memes 150 personnes : C2 avec etiquette et C3
     sans. Les items ou le camp de gauche simule est devenu unanime sont portes en
     triangles au bord haut : le rapport y est infini et le point n'a pas d'ordonnee.
  D. La pente de chaque condition, avec son intervalle de bootstrap sur les personnes.

Entrees : resultats/a37-gss-par-item.csv, a37-agents-par-item.csv, a37-agents-gss.csv,
          a37-agents-gss-150.csv, a37-regressions-humains.csv
Sorties : resultats/a37-figure-consensus.png et .svg

Usage : .venv/bin/python analyses/a37_figure.py
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
GAUCHE = "#2a78d6"
DROITE = "#c8412b"
NEUTRE = "#8d8b86"
HUMAIN = "#3f3d39"

COURT = {
    "humains vague 1": "humains",
    "agents v8": "agents v8, avec etiquette",
    "agents enquete": "agents enquete, sans etiquette",
    "agents demographiques (v6)": "agents v6, sans etiquette",
    "C2": "C2, avec etiquette",
    "C3": "C3, sans etiquette",
    "agents entretien (v3)": "agents entretien v3",
    "agents composite": "agents composite",
    "agents v7": "agents persona v7",
    "humains vague 2": "humains vague 2",
    "B0 tirage": "B0, tirage dans la marginale",
    "B1 argmax": "B1, regression logistique",
    "B2 argmax": "B2, plus proches voisins",
    "B3 foret": "B3, foret aleatoire",
    "B0 mode": "B0, mode",
}


def style(ax, axe_grille="both"):
    ax.set_facecolor(FOND)
    ax.grid(True, axis=axe_grille, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=8)


def droite_reg(ax, x, y, couleur, etiquette=None, tirets=None):
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return np.nan
    p = np.polyfit(x[ok], y[ok], 1)
    xs = np.linspace(np.nanmin(x[ok]), np.nanmax(x[ok]), 50)
    ax.plot(xs, np.polyval(p, xs), color=couleur, linewidth=1.8, zorder=4,
            label=etiquette, linestyle=tirets or "-")
    return p[0]


def nuage(ax, x, y, couleur, etiquette, plein=True, taille=30):
    ok = np.isfinite(x) & np.isfinite(y)
    if plein:
        ax.scatter(x[ok], y[ok], s=taille, color=couleur, alpha=0.75, zorder=3,
                   linewidths=0, label=etiquette)
    else:
        ax.scatter(x[ok], y[ok], s=taille, facecolors="none", edgecolors=couleur,
                   linewidths=1.1, zorder=3, label=etiquette)


def censures(ax, x, y, couleur, haut):
    """Items ou le rapport est infini : le camp de gauche simule est unanime."""
    m = np.isfinite(x) & ~np.isfinite(y)
    if m.sum():
        ax.scatter(x[m], np.full(m.sum(), haut), s=44, marker="^", color=couleur,
                   zorder=5, linewidths=0)
    return int(m.sum())


def panneau_humains(ax):
    d = pd.read_csv(os.path.join(SORTIE, "a37-gss-par-item.csv"))
    d = d[d["retenu"]]
    x = d["derive_agregee"].to_numpy()
    y = d["log_ratio"].to_numpy()
    ax.axhline(0.0, color=NEUTRE, linewidth=1.0, zorder=1)
    ax.axvline(0.0, color=NEUTRE, linewidth=1.0, zorder=1)
    fam_ab = d["famille"].str.startswith("avortement").to_numpy()
    fam_lib = d["famille"].str.startswith("libertes").to_numpy()
    nuage(ax, x[~(fam_ab | fam_lib)], y[~(fam_ab | fam_lib)], HUMAIN,
          "autres items orientes")
    nuage(ax, x[fam_lib], y[fam_lib], GAUCHE, "libertes civiles")
    nuage(ax, x[fam_ab], y[fam_ab], DROITE, "avortement")
    pente = droite_reg(ax, x, y, ENCRE, None)
    reg = pd.read_csv(os.path.join(SORTIE, "a37-regressions-humains.csv"))
    r = reg[reg["test"].str.startswith("H1")].iloc[0]
    ax.set_xlabel("derive agregee de l'item, negative a gauche et positive a droite",
                  fontsize=8, color=ENCRE_SECONDE)
    ax.set_ylabel("log du rapport de dispersion, droite sur gauche", fontsize=8,
                  color=ENCRE_SECONDE)
    ax.set_title(f"A. Humains du GSS, {int(r['n_items'])} items orientes\n"
                 f"pente {r['pente']:.2f} [{r['pente_ic_bas']:.2f} ; "
                 f"{r['pente_ic_haut']:.2f}], R2 {r['r2']:.2f}\n ",
                 fontsize=8.5, color=ENCRE, loc="left")
    style(ax)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    return pente


def panneau_agents(ax, perimetre, conditions, titre, fichier_reg):
    d = pd.read_csv(os.path.join(SORTIE, "a37-agents-par-item.csv"))
    d = d[d["perimetre"] == perimetre]
    reg = pd.read_csv(os.path.join(SORTIE, fichier_reg))
    reg = reg[reg["perimetre"] == perimetre].set_index("condition")

    hum = d[d["condition"] == "humains vague 1"]
    ax.axhline(0.0, color=NEUTRE, linewidth=1.0, zorder=1)
    ax.axvline(0.0, color=NEUTRE, linewidth=1.0, zorder=1)
    nuage(ax, hum["derive_propre"].to_numpy(), hum["log_ratio"].to_numpy(), NEUTRE,
          "humains", taille=18)
    droite_reg(ax, hum["derive_propre"].to_numpy(), hum["log_ratio"].to_numpy(),
               HUMAIN, "humains, regression", tirets="--")
    haut = np.nanmax(np.abs(d["log_ratio"].replace([np.inf, -np.inf], np.nan))) * 1.05
    sous_titres = []
    for nom, couleur in conditions:
        s = d[d["condition"] == nom]
        if not len(s):
            continue
        x = s["derive_propre"].to_numpy()
        y = s["log_ratio"].to_numpy()
        nuage(ax, x, y, couleur, COURT.get(nom, nom), plein=False)
        droite_reg(ax, x, y, couleur, None)
        nc = censures(ax, x, y, couleur, haut)
        p = reg.loc[nom]
        sous_titres.append(f"{COURT.get(nom, nom)} : pente {p['pente']:.2f}"
                           + (f", {nc} item{'s' if nc > 1 else ''} censure"
                              f"{'s' if nc > 1 else ''}" if nc else ""))
    ax.set_ylim(-haut * 1.08, haut * 1.14)
    ax.set_xlabel("derive agregee de l'item, mesuree dans la population consideree",
                  fontsize=8, color=ENCRE_SECONDE)
    ax.set_ylabel("log du rapport de dispersion, droite sur gauche", fontsize=8,
                  color=ENCRE_SECONDE)
    ax.set_title(titre + "\n" + "\n".join(sous_titres), fontsize=8.5, color=ENCRE,
                 loc="left")
    style(ax)
    ax.legend(fontsize=7, frameon=False, loc="lower left")


def panneau_pentes(ax):
    a = pd.read_csv(os.path.join(SORTIE, "a37-agents-gss.csv"))
    b = pd.read_csv(os.path.join(SORTIE, "a37-agents-gss-150.csv"))
    ordre = [("1052 personnes", "humains vague 1"),
             ("1052 personnes", "humains vague 2"),
             ("1052 personnes", "agents v7"),
             ("1052 personnes", "agents demographiques (v6)"),
             ("1052 personnes", "agents composite"),
             ("1052 personnes", "agents enquete"),
             ("1052 personnes", "agents entretien (v3)"),
             ("1052 personnes", "agents v8"),
             ("150 personnes", "C3"),
             ("150 personnes", "C2")]
    tab = pd.concat([a, b])
    lignes = []
    for per, nom in ordre:
        s = tab[(tab["perimetre"] == per) & (tab["condition"] == nom)]
        if len(s):
            lignes.append((per, nom, s.iloc[0]))
    y = np.arange(len(lignes))[::-1]
    for i, (per, nom, r) in enumerate(lignes):
        yy = y[i]
        coul = HUMAIN if "humains" in nom else (
            DROITE if nom in ("agents v8", "C2") else ENCRE)
        ax.hlines(yy, r["pente_ic_bas"], r["pente_ic_haut"], color=NEUTRE,
                  linewidth=1.2, zorder=2)
        ax.scatter(r["pente"], yy, s=40, color=coul, zorder=3)
        if r["n_items_perdus_log"] > 0:
            ax.annotate(f"{int(r['n_items_perdus_log'])} censures",
                        (r["pente"], yy), textcoords="offset points",
                        xytext=(9, 7), fontsize=6.5, color=DROITE)
    ref = [r for per, nom, r in lignes if nom == "humains vague 1"][0]
    ax.axvline(ref["pente"], color=HUMAIN, linewidth=1.0, linestyle="--", zorder=1)
    ax.axvline(0.0, color=GRILLE, linewidth=1.0, zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{COURT.get(n, n)}  ({p.split()[0]})" for p, n, _ in lignes],
                       fontsize=8)
    ax.set_xlabel("pente de log(rapport de dispersion) sur la derive agregee",
                  fontsize=8, color=ENCRE_SECONDE)
    ax.set_title("D. La pente par condition, intervalle de bootstrap sur les\n"
                 "personnes ; trait tirete : la pente des vrais humains\n ",
                 fontsize=8.5, color=ENCRE, loc="left")
    style(ax, axe_grille="x")


def main():
    fig = plt.figure(figsize=(13.2, 10.4), facecolor=FOND)
    gs = fig.add_gridspec(2, 2, hspace=0.46, wspace=0.26,
                          left=0.07, right=0.985, top=0.875, bottom=0.055)

    panneau_humains(fig.add_subplot(gs[0, 0]))
    panneau_agents(fig.add_subplot(gs[0, 1]), "1052 personnes",
                   [("agents v8", DROITE), ("agents enquete", GAUCHE)],
                   "B. Conditions de Stanford, deux montrees, 1 052 personnes",
                   "a37-agents-gss.csv")
    panneau_agents(fig.add_subplot(gs[1, 0]), "150 personnes",
                   [("C2", DROITE), ("C3", GAUCHE)],
                   "C. Nos agents locaux, les memes 150 personnes",
                   "a37-agents-gss-150.csv")
    panneau_pentes(fig.add_subplot(gs[1, 1]))

    fig.suptitle("Le 1,12 est l'effet de consensus liberal : la variete relative d'un "
                 "camp suit la derive agregee de l'item ;\nl'etiquette ideologique dans "
                 "l'invite ne l'efface pas, elle la caricature jusqu'a l'unanimite",
                 fontsize=12.5, color=ENCRE, x=0.015, ha="left", y=0.985)
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a37-figure-consensus.{ext}")
        fig.savefig(chemin, dpi=170, facecolor=FOND)
        print(f"ecrit : {chemin}", flush=True)


if __name__ == "__main__":
    main()
