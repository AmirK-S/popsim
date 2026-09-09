"""
i3b_figures : les trois figures du mois 1 du programme B.

  1. i3b-figure-abaque          : taille de flux contre plus petit taux detectable, une
                                  courbe par fabricant, partie extrapolee en tirets.
  2. i3b-figure-bande-deux-jeux : le plan (deficit de patrons, exces de correlation) sur
                                  le GSS et sur Twin-2K-500, avec la bande humaine et
                                  l'origine du generateur nul ; troisieme panneau, le zoom
                                  de Twin autour de la bande.
  3. i3b-figure-surface-attaque : le prix de l'invisibilite, taux de detection contre
                                  deplacement maximal non detecte de l'ecart entre camps.

Aucun calcul nouveau : le script ne lit que les CSV deja ecrits.
Usage : .venv/bin/python analyses/i3b_figures.py
"""

import json
import os
import sys

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter, NullFormatter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import i3b_commun as J
import i3_commun as I

COULEUR = {
    "agents v8": "#c0392b", "agents demographiques (v6)": "#e67e22",
    "agents composite": "#d35400", "C2": "#8e44ad", "C3": "#9b59b6",
    "PMM k=10": "#2980b9", "E2 regression contexte tirage": "#16a085",
    "IM m=10 mode des m": "#27ae60", "B0 segment": "#7f8c8d",
    "humains vague 2": "#000000",
}
ORDRE = ["agents v8", "C2", "B0 segment", "agents demographiques (v6)", "C3",
         "IM m=10 mode des m", "agents composite", "PMM k=10",
         "E2 regression contexte tirage", "humains vague 2"]


def enregistrer(fig, nom):
    for ext in ("png", "svg"):
        chemin = os.path.join(J.SORTIE, f"{nom}.{ext}")
        fig.savefig(chemin, dpi=150, bbox_inches="tight")
        print(f"ecrit {chemin}", flush=True)
    plt.close(fig)


def _axes_lineaires(ax, xticks, yticks):
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.xaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis="both", which="minor", length=2)


# ---------------------------------------------------------------------------

def figure_abaque():
    ab = pd.read_csv(os.path.join(J.SORTIE, "i3b-abaque.csv"))
    ex = pd.read_csv(os.path.join(J.SORTIE, "i3b-abaque-extrapolee.csv"))
    fig, ax = plt.subplots(figsize=(9.6, 6.4))
    for nom in ORDRE:
        d = ab[ab.source == nom]
        if not len(d):
            continue
        xs, ys = [], []
        for n in sorted(d.taille.unique()):
            v = d[d.taille == n].groupby("statistique").tau_etoile_holm3.first().values
            if np.isfinite(v).any():
                xs.append(n)
                ys.append(100.0 * np.nanmin(v))
        if not xs:
            continue
        c = COULEUR.get(nom, "#555555")
        if nom == "humains vague 2":
            ax.plot(xs, ys, "k*", ms=13, label="humains vague 2, controle")
            ax.annotate("de vraies personnes\nreinterrogees : jamais\ndetectees au dela\nde 300",
                        (xs[0], ys[0]), textcoords="offset points", xytext=(10, -46),
                        fontsize=7.5, color="#333333")
            continue
        ax.plot(xs, ys, "-", color=c, marker="o", ms=4.5, lw=1.9,
                label=I.ETIQUETTE.get(nom, nom))
        e = ex[(ex.source == nom) & ex.courbe_stable_en_N]
        if len(e):
            xe, ye = [xs[-1]], [ys[-1]]
            for n in sorted(e.taille.unique()):
                v = e[e.taille == n].tau_etoile_holm3.values
                if np.isfinite(v).any():
                    xe.append(n)
                    ye.append(100.0 * np.nanmin(v))
            if len(xe) > 1:
                ax.plot(xe, ye, "--", color=c, lw=1.3, alpha=0.85)
                ax.plot(xe[-1], ye[-1], "o", color=c, ms=4.5, mfc="white")
    ax.axhline(5.0, color="#999999", lw=0.9, ls="-.")
    ax.text(305, 5.35, "5 pour cent de contamination", fontsize=8, color="#777777")
    ax.axvline(1052, color="#bbbbbb", lw=1.0)
    ax.text(1090, 0.62, "mesure a gauche  |  extrapole a droite", fontsize=8,
            color="#888888")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(270, 6600)
    ax.set_ylim(0.55, 130)
    _axes_lineaires(ax, [300, 500, 750, 1052, 1500, 2000, 3000, 5000],
                    [1, 2, 5, 10, 20, 50, 100])
    ax.set_xlabel("taille du flux, nombre de repondants")
    ax.set_ylabel("plus petit taux de contamination detectable, pour cent\n"
                  "puissance 80 pour cent, bilateral 5 pour cent, Holm sur trois tests")
    ax.set_title("L'abaque : ce qu'un flux de 300 personnes ne peut pas voir,\n"
                 "et ce qu'un flux de 5 000 verrait", fontsize=11.5)
    ax.grid(alpha=0.25, which="major")
    ax.grid(alpha=0.10, which="minor")
    ax.legend(fontsize=8, ncol=2, loc="upper right", framealpha=0.92)
    enregistrer(fig, "i3b-figure-abaque")


# ---------------------------------------------------------------------------

def _cle_courte(nom):
    return (nom.replace(" - GPT4.1-mini", " g41m").replace(" - GPT4.1", " g41")
            .replace(" - Gemini-Flash2.5", " gem")
            .replace("(500 training samples)", "500ex")
            .replace("(Predicted Output)", "(pred)")
            .replace("(Default Temperature)", "(temp)")
            .replace("(Repeating Questions)", "(repet)")
            .replace("(Reasoning)", "(raison)"))


def _panneau_bande(ax, pur, ref, titre, xlim=None, ylim=None):
    ha = float(ref[ref.statistique == "A"].valeur.iloc[0])
    hb = float(ref[ref.statistique == "B"].valeur.iloc[0])
    sa = float(ref[ref.statistique == "A"].s0.iloc[0])
    sb = float(ref[ref.statistique == "B"].s0.iloc[0])
    ax.axhline(0.0, color="#dddddd", lw=0.8)
    ax.axvline(0.0, color="#dddddd", lw=0.8)
    ax.add_patch(plt.Rectangle((ha - 8 * sa, hb - 8 * sb), 16 * sa, 16 * sb,
                               color="#f1c40f", alpha=0.30, zorder=1))
    ax.plot(0, 0, marker="P", ms=11, color="#7f8c8d", zorder=4)
    ax.plot(ha, hb, marker="*", ms=17, color="#b7950b", zorder=5)
    noms = []
    for r in pur.itertuples():
        nom = r.source
        if nom in ("humains vague 1", "humains vagues 1-3 (retest)"):
            continue
        noms.append(nom)
    noms = sorted(noms, key=lambda n: -abs(pur[pur.source == n].A.iloc[0]))
    for k, nom in enumerate(noms, start=1):
        r = pur[pur.source == nom].iloc[0]
        c = COULEUR.get(nom, "#2c3e50")
        dedans = True
        if xlim is not None:
            dedans = xlim[0] <= r.A <= xlim[1] and ylim[0] <= r.B <= ylim[1]
        if not dedans:
            continue
        ax.plot(r.A, r.B, "o", ms=13, color=c, alpha=0.9, zorder=3)
        ax.annotate(str(k), (r.A, r.B), ha="center", va="center", fontsize=7.5,
                    color="white", zorder=6, fontweight="bold")
    ax.set_xlabel("A, deficit de patrons de reponses distincts")
    ax.set_ylabel("B, exces de correlation residualisee")
    ax.set_title(titre, fontsize=10)
    ax.grid(alpha=0.2)
    if xlim:
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
    return noms


def figure_bande():
    gss = pd.read_csv(os.path.join(J.SORTIE, "i3-sources-pures.csv"))
    gref = pd.read_csv(os.path.join(J.SORTIE, "i3b-reference-par-taille.csv"))
    gref = gref[gref.taille == 1052]
    twin = pd.read_csv(os.path.join(J.SORTIE, "i3b-twin-sources-pures.csv"))
    tref = pd.read_csv(os.path.join(J.SORTIE, "i3b-twin-reference.csv"))
    tref = tref[tref.taille == tref.taille.max()]

    fig, axes = plt.subplots(1, 3, figsize=(16.4, 5.9))
    ng = _panneau_bande(axes[0], gss, gref,
                        "a. GSS, 1 052 personnes, 149 items, neuf fabricants")
    nt = _panneau_bande(axes[1], twin, tref,
                        "b. Twin-2K-500, 2 058 personnes, 108 items, treize configurations")
    _panneau_bande(axes[2], twin, tref,
                   "c. Twin, zoom autour de la bande humaine",
                   xlim=(-0.28, 0.02), ylim=(-0.005, 0.08))
    axes[0].annotate("humains de reference", (float(gref[gref.statistique == "A"]
                                                    .valeur.iloc[0]),
                                              float(gref[gref.statistique == "B"]
                                                    .valeur.iloc[0])),
                     textcoords="offset points", xytext=(8, 10), fontsize=9,
                     color="#7d6608")
    axes[0].annotate("generateur nul\n(aucune structure)", (0, 0),
                     textcoords="offset points", xytext=(-70, 14), fontsize=8,
                     color="#555555")
    axes[2].annotate("humains", (float(tref[tref.statistique == "A"].valeur.iloc[0]),
                                 float(tref[tref.statistique == "B"].valeur.iloc[0])),
                     textcoords="offset points", xytext=(8, 10), fontsize=9,
                     color="#7d6608")

    cle_g = "   ".join(f"{k}. {I.ETIQUETTE.get(n, n)}" for k, n in enumerate(ng, 1))
    cle_t = "   ".join(f"{k}. {_cle_courte(n)}" for k, n in enumerate(nt, 1))
    fig.text(0.005, -0.02, "GSS  " + cle_g, fontsize=7.4, color="#333333")
    fig.text(0.005, -0.055, "Twin  " + cle_t[:len(cle_t) // 2], fontsize=7.4,
             color="#333333")
    fig.text(0.005, -0.09, "        " + cle_t[len(cle_t) // 2:], fontsize=7.4,
             color="#333333")
    fig.suptitle("La bande a deux bords, sur deux jeux independants : de vraies personnes "
                 "ne sont ni aussi libres qu'un tirage sans structure (la croix a "
                 "l'origine),\nni aussi pauvres qu'un gabarit. La bande jaune est la "
                 "reference humaine a huit ecarts types. Sur Twin, six configurations sur "
                 "treize sont SOUS la bande sur B.", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    enregistrer(fig, "i3b-figure-bande-deux-jeux")


# ---------------------------------------------------------------------------

def figure_surface():
    s = pd.read_csv(os.path.join(J.SORTIE, "i3b-surface-attaque.csv"))
    fig, axes = plt.subplots(1, 2, figsize=(13.0, 5.6))
    for ax, taille in zip(axes, [300, 1052]):
        d = s[(s.taille == taille) & (s.source != "humains vague 2")]
        for r in d.itertuples():
            if not np.isfinite(r.taux_lu):
                continue
            c = COULEUR.get(r.source, "#2c3e50")
            x = 100.0 * r.taux_lu
            y = r.polarisation_pourcent_max
            ax.plot(x, y, "o", ms=10, color=c)
            ax.annotate(I.ETIQUETTE.get(r.source, r.source), (x, y),
                        textcoords="offset points", xytext=(9, 2), fontsize=8.5)
        ax.axhline(0.0, color="#999999", lw=0.9)
        ax.set_xscale("log")
        ax.set_xlim(1.5, 130)
        _axes_lineaires(ax, [2, 5, 10, 20, 50, 100],
                        ax.get_yticks())
        ax.set_xlabel("taux de detection, pour cent du flux (echelle logarithmique)")
        ax.set_ylabel("deplacement maximal NON DETECTE de l'ecart entre camps,\n"
                      "pour cent de la valeur humaine ; positif = gonfle, negatif = aplatit")
        ax.set_title(f"N = {taille} repondants", fontsize=10.5)
        ax.grid(alpha=0.25, which="major")
    fig.suptitle("Le prix de l'invisibilite n'est pas monotone : les deux fabricants les "
                 "plus difficiles a detecter, PMM et E2, sont des imputations par tirage\n"
                 "qui portent la personne et deplacent peu ; celui qui deplace le plus, "
                 "l'agent riche, est vu a 15,9 pour cent. Le danger est au milieu.",
                 fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.90])
    enregistrer(fig, "i3b-figure-surface-attaque")


if __name__ == "__main__":
    faites = []
    for nom, f in (("abaque", figure_abaque), ("bande", figure_bande),
                   ("surface", figure_surface)):
        try:
            f()
            faites.append(nom)
        except FileNotFoundError as e:
            print(f"figure {nom} sautee, entree absente : {e}", flush=True)
    print("figures faites :", faites, flush=True)
