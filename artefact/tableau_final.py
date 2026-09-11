"""tableau_final : assemble attaque.csv et defense.csv (artefact/resultats_artefact/) en un
seul tableau, celui que le relecteur doit voir a la fin de `run.sh`.

Ne recalcule rien : lecture seule des deux CSV deja ecrits par attaque.py et defense.py.
Usage : .venv/bin/python artefact/tableau_final.py (apres attaque.py et defense.py)
"""

import os
import sys

import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIER_RESULTATS = os.path.join(ICI, "resultats_artefact")


def charger(nom):
    chemin = os.path.join(DOSSIER_RESULTATS, nom)
    if not os.path.isfile(chemin):
        print(f"Manquant : {chemin}. Lancez d'abord attaque.py puis defense.py "
              "(ou artefact/run.sh en entier).", file=sys.stderr)
        sys.exit(1)
    return pd.read_csv(chemin)


def main():
    att = charger("attaque.csv")
    dfd = charger("defense.csv")

    demo = att[att.jumeau == "twin_demo"].iloc[0]
    riche = att[att.jumeau == "twin_riche"].iloc[0]
    avant = dfd.iloc[0]
    apres = dfd.iloc[1]

    print("\n" + "=" * 78)
    print("TABLEAU FINAL - artefact de reidentification / defense (donnees FICTIVES)")
    print("=" * 78)
    print(f"{'ligne':38s} {'top-1':>10s} {'IC 95%':>18s}")
    print("-" * 78)
    print(f"{'hasard exact (1/n)':38s} {riche.top1_hasard*100:9.3f}% {'':>18s}")
    print(f"{'jumeau Demographics Only (comparateur)':38s} {demo.top1*100:9.3f}% "
          f"[{demo.top1_bas*100:.3f};{demo.top1_haut*100:.3f}]")
    print(f"{'jumeau riche, AVANT defense':38s} {avant.top1*100:9.3f}% "
          f"[{avant.top1_bas*100:.3f};{avant.top1_haut*100:.3f}]")
    print(f"{'jumeau riche, APRES D4 (melange segment)':38s} {apres.top1*100:9.3f}% "
          f"[{apres.top1_bas*100:.3f};{apres.top1_haut*100:.3f}]")
    print("-" * 78)
    reduction = (avant.top1 / apres.top1) if apres.top1 > 0 else float("inf")
    print(f"reduction du risque (avant / apres) : x{reduction:,.0f}".replace(",", " "))
    print(f"perte d'utilite de la defense : {apres.perte_utilite:.2f} points "
          f"(distribution={apres.dont_distribution:.2f} / groupes={apres.dont_groupes:.2f} / "
          f"correlations={apres.dont_correlations:.2f})")
    print("=" * 78)

    verdict_attaque = bool(riche.top1 >= 0.10 and riche.top1 >= 2 * demo.top1)
    verdict_defense = bool(apres.top1 < 0.01 and apres.perte_utilite < 2.0)
    print(f"critere 'attaque demontree' (top1 riche >= 10% ET >= 2x Demographics Only) : "
          f"{verdict_attaque}")
    print(f"critere 'defense reussie' (top1 apres D4 < 1% ET perte d'utilite < 2 points) : "
          f"{verdict_defense}")
    print("=" * 78 + "\n")

    print("Rappel : chiffres obtenus sur un jeu de donnees ENTIEREMENT FICTIF, genere par "
          "generer_donnees.py. Ils ne se substituent pas aux chiffres de l'article, mesures "
          "sur Twin-2K-500 (resultats/c7-resultats.md, resultats/c7-defense-resultats.md).")


if __name__ == "__main__":
    main()
