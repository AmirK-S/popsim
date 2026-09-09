"""
a2_figures : trace les figures du rapport a2 a partir des JSON produits par les baselines.

Statut : script d'exploration, pas du code de production. Il ne recalcule rien, il lit
les resultats deja ecrits pour que la figure et le tableau du rapport ne puissent pas
diverger.

Entree  : resultats/a2_gss_resultats.json et resultats/a2_twin_resultats.json.
Sortie  : dans resultats/, en PNG et en SVG,
            a2-courbe-croisement-gss   exactitude selon le nombre de repondants
            a2-courbe-croisement-twin  idem sur Twin-2K-500
            a2-exactitude-diversite    le couple exactitude et diversite preservee
          Axes, titres et legendes en francais.

Aucun appel de modele. Duree : quelques secondes.

Usage : python3 analyses/a2_figures.py
"""

import json
import os

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Palette validee : trois teintes categorielles, fond clair, encres de texte separees
# des teintes de serie. Les series portent aussi une etiquette posee directement au
# bout de la courbe, ce qui rend la lecture possible sans distinguer les couleurs.
FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
SERIES = {"B0": "#2a78d6", "B1": "#eb6834", "B2": "#1baf7a"}
REFERENCE = "#4a3aa7"


def style(ax):
    """Grille et axes recessifs, fond neutre, pas de cadre superflu."""
    ax.set_facecolor(FOND)
    ax.grid(True, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def enregistrer(fig, nom):
    for extension in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"{nom}.{extension}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


def courbe_croisement(res, nom_fichier, titre, sous_titre, references):
    """Exactitude de chaque baseline selon le nombre de personnes servant a l'entrainer.

    Une seule echelle verticale, l'exactitude. Les points de repere, humains et modeles
    de langage, sont des horizontales : ils ne dependent pas de la taille du corpus
    d'entrainement puisque rien n'y est entraine.
    """
    points = res["courbe"]
    x = [p["n_entrainement"] for p in points]
    fig, ax = plt.subplots(figsize=(8.2, 5.2))
    style(ax)
    bouts = []

    libelles = {
        "B0 mode": "B0, modalite majoritaire",
        "B1 argmax": "B1, regression sur demographies",
        "B2 argmax": "B2, plus proches voisins",
    }
    for cle, couleur in (("B0 mode", SERIES["B0"]), ("B1 argmax", SERIES["B1"]),
                         ("B2 argmax", SERIES["B2"])):
        y = [p[cle] for p in points]
        ecart = [p[cle + " ecart"] for p in points]
        ax.plot(x, y, color=couleur, linewidth=2, marker="o", markersize=5,
                markeredgecolor=FOND, markeredgewidth=1.2, zorder=3, label=libelles[cle])
        ax.fill_between(x, [a - b for a, b in zip(y, ecart)],
                        [a + b for a, b in zip(y, ecart)],
                        color=couleur, alpha=0.12, linewidth=0, zorder=2)
        bouts.append((y[-1], f"{libelles[cle]}  {y[-1]:.3f}"))

    # Une horizontale de reference qui traverse le nuage voit son etiquette passer
    # sous la ligne, sinon elle se superpose a la courbe la plus basse.
    plancher = max(p["B0 mode"] for p in points)
    for etiquette, valeur in references:
        ax.axhline(valeur, color=REFERENCE, linewidth=1, linestyle=(0, (4, 3)), zorder=1)
        ax.annotate(f"{etiquette}  {valeur:.3f}", (x[0], valeur),
                    textcoords="offset points",
                    xytext=(0, -12 if valeur < plancher else 4), fontsize=8.5,
                    color=REFERENCE)

    # Etiquettes directes au bout des courbes : la lecture ne repose pas sur la couleur.
    # Elles sont ecartees verticalement quand deux courbes finissent au meme niveau.
    bas, haut = ax.get_ylim()
    hauteur_pt = ax.get_position().height * fig.get_figheight() * 72
    minimum = 11 * (haut - bas) / hauteur_pt
    voulu = None
    for valeur, texte in sorted(bouts, reverse=True):
        voulu = valeur if voulu is None else min(valeur, voulu - minimum)
        ax.annotate(texte, (x[-1], valeur), textcoords="offset points",
                    xytext=(8, (voulu - valeur) / (haut - bas) * hauteur_pt),
                    va="center", fontsize=8.5, color=ENCRE_SECONDE)

    ax.set_xscale("log")
    ax.set_xticks(x)
    ax.set_xticklabels([str(v) for v in x])
    ax.set_xlabel("nombre de repondants reels servant a entrainer", fontsize=10,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("exactitude par personne sur les questions tenues secretes",
                  fontsize=10, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=13, color=ENCRE, loc="left", pad=18)
    ax.text(0, 1.02, sous_titre, transform=ax.transAxes, fontsize=9.5,
            color=ENCRE_SECONDE, va="bottom")
    ax.legend(loc="upper right", frameon=False, fontsize=9, labelcolor=ENCRE_SECONDE,
              bbox_to_anchor=(1.0, 0.94))
    ax.set_xlim(min(x) * 0.85, max(x) * 2.6)
    ax.tick_params(axis="x", which="minor", bottom=False)
    ax.xaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    fig.patch.set_facecolor(FOND)
    enregistrer(fig, nom_fichier)


def exactitude_diversite(gss, twin):
    """Le couple exactitude et diversite preservee, un panneau par jeu de donnees.

    Deux familles seulement, donc deux teintes : les baselines sans modele et les
    simulations par modele de langage. Chaque point porte son nom, la couleur ne
    supporte aucune information a elle seule. Les humains reinterroges sont en (1, 1)
    par construction et servent de coin ideal.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.6))
    for ax, res, titre in zip(axes, (gss, twin),
                              ("GSS, archive OSF t6g7k, 1 052 personnes, 149 items",
                               "Twin-2K-500, 2 058 personnes, 108 items de la vague 4")):
        style(ax)
        # Placement des etiquettes de points : on essaie quatre positions autour du
        # marqueur et on garde la premiere qui ne chevauche aucune etiquette deja posee.
        # Sans cela deux baselines de meme exactitude se recouvrent et deviennent
        # illisibles, et une etiquette poussee trop loin cesse de designer son point.
        largeur_pt = ax.get_position().width * fig.get_figwidth() * 72
        hauteur_pt = ax.get_position().height * fig.get_figheight() * 72
        occupees, a_poser = [], []
        for serie, couleur, marqueur in ((res["baselines"], SERIES["B0"], "o"),
                                         (res.get("references_llm", []), SERIES["B1"], "s")):
            for l in serie:
                nom = l.get("baseline") or l.get("condition")
                px, py = l["part_diversite_humaine"], l["exactitude"]
                ax.scatter(px, py, s=70, color=couleur, marker=marqueur,
                           edgecolor=FOND, linewidth=1.2, zorder=3)
                a_poser.append((py, px, nom))

        bas_y, haut_y = min(p[0] for p in a_poser), max(p[0] for p in a_poser)
        # Les marqueurs eux memes sont des zones occupees : une etiquette ne doit pas
        # passer par dessus le point d'une autre baseline.
        for py, px, _ in a_poser:
            occupees.append((px - 0.02, px + 0.02, py))
        for py, px, nom in sorted(a_poser, reverse=True):
            largeur = len(nom) * 4.4 + 8
            for dx, dy, ha in ((7, -3, "left"), (7, 9, "left"), (7, -15, "left"),
                               (-7, -3, "right"), (-7, 9, "right"), (-7, -15, "right")):
                gauche = px + (dx if ha == "left" else dx - largeur) / largeur_pt * 1.4
                droite = gauche + largeur / largeur_pt * 1.4
                milieu = py + dy / hauteur_pt * (haut_y - bas_y) * 1.35
                if not any(gauche < d and g < droite and abs(milieu - m) < 0.028 * (haut_y - bas_y)
                           for g, d, m in occupees):
                    break
            occupees.append((gauche, droite, milieu))
            ax.annotate(nom, (px, py), textcoords="offset points", xytext=(dx, dy),
                        ha=ha, fontsize=8, color=ENCRE_SECONDE)

        retest = res["test_retest_humain"]["exactitude"]
        ax.axhline(retest, color=REFERENCE, linewidth=1, linestyle=(0, (4, 3)), zorder=1)
        ax.annotate(f"plafond humain, test retest  {retest:.3f}", (0.02, retest),
                    textcoords="offset points", xytext=(0, 4), fontsize=8.5,
                    color=REFERENCE)
        ax.axvline(1.0, color=GRILLE, linewidth=1, zorder=1)
        ax.set_xlabel("diversite de reponse conservee, part de celle des humains",
                      fontsize=10, color=ENCRE_SECONDE)
        ax.set_ylabel("exactitude par personne", fontsize=10, color=ENCRE_SECONDE)
        ax.set_title(titre, fontsize=10.5, color=ENCRE, loc="left")
        ax.set_xlim(-0.05, 1.35)
    axes[0].scatter([], [], s=70, color=SERIES["B0"], marker="o",
                    label="baselines sans modele de langage")
    axes[0].scatter([], [], s=70, color=SERIES["B1"], marker="s",
                    label="simulations par modele de langage")
    axes[0].legend(loc="upper left", frameon=False, fontsize=9, labelcolor=ENCRE_SECONDE,
                   bbox_to_anchor=(0.0, 0.93))
    fig.suptitle("Une bonne exactitude s'achete en detruisant la dispersion",
                 fontsize=13, color=ENCRE, x=0.09, ha="left", y=1.0)
    fig.patch.set_facecolor(FOND)
    fig.tight_layout()
    enregistrer(fig, "a2-exactitude-diversite")


def main():
    gss = json.load(open(os.path.join(SORTIE, "a2_gss_resultats.json"), encoding="utf-8"))
    twin = json.load(open(os.path.join(SORTIE, "a2_twin_resultats.json"), encoding="utf-8"))

    ref_gss = [("humains reinterroges", gss["test_retest_humain"]["exactitude"])]
    for r in gss.get("references_llm", []):
        if r["condition"] in ("agents composite", "agents demographiques (v6)"):
            ref_gss.append((r["condition"], r["exactitude"]))
    courbe_croisement(
        gss, "a2-courbe-croisement-gss",
        "Courbe de croisement, GSS",
        "a partir de combien de repondants reels une methode statistique classique "
        "rattrape puis depasse un agent de langage",
        ref_gss)

    ref_twin = [("humains reinterroges", twin["test_retest_humain"]["exactitude"])]
    for r in twin.get("references_llm", []):
        ref_twin.append((r["condition"], r["exactitude"]))
    courbe_croisement(
        twin, "a2-courbe-croisement-twin",
        "Courbe de croisement, Twin-2K-500",
        "meme protocole, cible de la vague 4, contexte des vagues 1 a 3 hors questions "
        "reposees",
        ref_twin)

    exactitude_diversite(gss, twin)


if __name__ == "__main__":
    main()
