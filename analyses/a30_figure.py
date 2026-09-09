"""
a30_figure : la figure du rapport a30.

Ne recalcule rien. Lit les tableaux produits par a30_humains_gss.py, a30_agents.py et
a30_humains_twin.py, pour que la figure et les chiffres du rapport ne puissent pas
diverger. Aucun appel de modele.

Trois panneaux.
  A. Dispersion interne par camp et par famille de sujets, GSS, humains contre agents.
     C'est le panneau qui repond a la question posee : ou la droite est elle plus variee,
     et de combien.
  B. Rapport droite sur gauche par condition, GSS, avec intervalle de bootstrap sur les
     personnes et la valeur humaine en trait de reference.
  C. Le meme rapport sur Twin-2K-500, humains de la vague 4 contre les configurations
     d'agents des auteurs.

Entrees : resultats/a30-agents-gss-familles.csv, a30-agents-gss.csv,
          a30-agents-gss-150.csv, a30-agents-twin.csv
Sorties : resultats/a30-figure-variete-des-camps.png et .svg

Usage : .venv/bin/python analyses/a30_figure.py
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

COURT = {
    "depenses publiques (nat*)": "depenses publiques",
    "confiance dans les institutions (con*)": "confiance institutions",
    "avortement (ab*)": "avortement",
    "libertes civiles (spk/col/lib)": "libertes civiles",
    "fin de vie (suicide/letdie)": "fin de vie",
    "roles de genre (fe*)": "roles de genre",
    "residu : social": "autres, social",
    "residu : economique": "autres, economique",
    "residu : hors axe": "autres, hors axe",
}


def style(ax, axe_grille="x"):
    ax.set_facecolor(FOND)
    ax.grid(True, axis=axe_grille, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=8)


def panneau_familles(ax):
    d = pd.read_csv(os.path.join(SORTIE, "a30-agents-gss-familles.csv"))
    d = d[d["perimetre"] == "1052 personnes"]
    hum = d[d["condition"] == "humains vague 1"].set_index("famille")
    ag = d[d["condition"] == "agents composite"].set_index("famille")
    ordre = hum.sort_values("ratio_droite_gauche", ascending=True).index.tolist()
    y = np.arange(len(ordre))
    for f, (col, camp) in enumerate([(GAUCHE, "gauche"), (DROITE, "droite")]):
        ax.scatter(hum.loc[ordre, "gs_" + camp], y + (f - 0.5) * 0.22, s=42,
                   color=col, zorder=3, label=f"humains, {camp}")
        ax.scatter(ag.loc[ordre, "gs_" + camp], y + (f - 0.5) * 0.22, s=42,
                   facecolors="none", edgecolors=col, linewidths=1.4, zorder=3,
                   label=f"agents composite, {camp}")
    for i, f in enumerate(ordre):
        for k, (col, camp) in enumerate([(GAUCHE, "gauche"), (DROITE, "droite")]):
            ax.plot([ag.loc[f, "gs_" + camp], hum.loc[f, "gs_" + camp]],
                    [i + (k - 0.5) * 0.22] * 2, color=col, linewidth=1.0, alpha=0.55,
                    zorder=2)
    ax.set_yticks(y)
    ax.set_yticklabels([f"{COURT.get(f, f)}  ({int(hum.loc[f, 'n_items'])})"
                        for f in ordre], fontsize=8)
    ax.set_xlabel("dispersion interne du camp, indice de Gini Simpson sans biais",
                  fontsize=8, color=ENCRE_SECONDE)
    ax.set_title("A. Ou la droite est elle plus variee que la gauche, GSS, 1 052 personnes\n"
                 "cercle plein : vrais humains ; cercle vide : agents composite de Stanford",
                 fontsize=9.5, color=ENCRE, loc="left")
    style(ax)
    ax.legend(fontsize=7, frameon=False, loc="lower right", ncol=2)


def panneau_conditions(ax, fichier, titre, reference, ordre=None, court=None):
    d = pd.read_csv(os.path.join(SORTIE, fichier))
    if ordre is not None:
        d = d[d["condition"].isin(ordre)]
        d["_o"] = d["condition"].map({c: i for i, c in enumerate(ordre)})
        d = d.sort_values("_o")
    y = np.arange(len(d))[::-1]
    # Gris pour les references humaines, encre pour tout ce qui est produit par une
    # methode : la couleur ne code pas le resultat, seulement le statut de la ligne.
    couleurs = [NEUTRE if "humains" in c else ENCRE for c in d["condition"]]
    if "ic_bas" in d.columns:
        ax.hlines(y, d["ic_bas"], d["ic_haut"], color=NEUTRE, linewidth=1.2, zorder=2)
    ax.scatter(d["ratio_droite_gauche"], y, s=38, color=couleurs, zorder=3)
    ax.axvline(reference, color=ENCRE, linewidth=1.0, linestyle="--", zorder=1)
    ax.axvline(1.0, color=GRILLE, linewidth=1.0, zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels([(court or {}).get(c, c) for c in d["condition"]], fontsize=8)
    ax.set_xlabel("rapport de dispersion interne, droite sur gauche", fontsize=8,
                  color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=9.5, color=ENCRE, loc="left")
    style(ax)


def main():
    fig = plt.figure(figsize=(12.6, 9.4), facecolor=FOND)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.15], hspace=0.42, wspace=0.34,
                          left=0.20, right=0.98, top=0.92, bottom=0.07)

    ax_a = fig.add_subplot(gs[0, :])
    panneau_familles(ax_a)

    # La reference du panneau B est la valeur humaine SUR LES MEMES 150 PERSONNES,
    # pas celle des 1 052 : melanger les deux perimetres deplacerait le trait de trois
    # centiemes sans que rien ne le signale.
    ref_gss = pd.read_csv(os.path.join(SORTIE, "a30-agents-gss-150.csv"))
    r_hum = float(ref_gss.loc[ref_gss["condition"] == "humains vague 1",
                              "ratio_droite_gauche"].iloc[0])
    ax_b = fig.add_subplot(gs[1, 0])
    panneau_conditions(
        ax_b, "a30-agents-gss-150.csv",
        "B. GSS, les memes 150 personnes de bout en bout\n"
        "trait tirete : la valeur des vrais humains", r_hum,
        ordre=["humains vague 1", "humains vague 2", "agents composite",
               "agents entretien (v3)", "agents enquete", "agents v7",
               "agents demographiques (v6)", "agents v8", "C3", "C2",
               "B1 argmax", "B2 argmax", "B3 foret", "B0 tirage"],
        court={"agents demographiques (v6)": "agents demographiques v6, sans etiquette",
               "agents v8": "agents demographiques v8, avec etiquette",
               "C2": "C2, nos agents, avec etiquette",
               "C3": "C3, nos agents, sans etiquette",
               "B0 tirage": "B0, tirage dans la marginale",
               "B1 argmax": "B1, regression logistique",
               "B2 argmax": "B2, plus proches voisins",
               "B3 foret": "B3, foret aleatoire"})

    twin = pd.read_csv(os.path.join(SORTIE, "a30-agents-twin.csv"))
    r_twin = float(twin.loc[twin["condition"] == "humains vague 4",
                            "ratio_droite_gauche"].iloc[0])
    ax_c = fig.add_subplot(gs[1, 1])
    panneau_conditions(
        ax_c, "a30-agents-twin.csv",
        "C. Twin-2K-500, 2 058 personnes, 108 items de la vague 4\n"
        "les treize configurations publiees par les auteurs", r_twin)

    # Le titre dit l'enonce exact et non l'enonce commode : le centre n'est pas
    # distinguable de la droite, rapport 0,989 [0,973 ; 1,005], donc ce n'est pas la
    # droite qui est plus variee, c'est la gauche qui l'est moins.
    fig.suptitle("Chez les humains, la gauche est le camp le moins varie des trois ; les "
                 "populations simulees exagerent l'ecart au lieu de l'effacer",
                 fontsize=12, color=ENCRE, x=0.02, ha="left", y=0.975)
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a30-figure-variete-des-camps.{ext}")
        fig.savefig(chemin, dpi=170, facecolor=FOND)
        print(f"ecrit : {chemin}", flush=True)


if __name__ == "__main__":
    main()
