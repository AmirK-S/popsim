"""
a37_densite : la correction demandee sur la densite de sous graphe partisan de a30.

Volet 3 de a37. Aucun calcul nouveau sur les microdonnees : ce script lit les deux
tableaux deja produits par `analyses/a30_resin_twin.py` et les remet en forme pour que
les deux variantes, sans egalisation du nombre de noeuds et avec, soient lues cote a
cote. Il ajoute la composition des sous graphes, qui est ce qui explique l'ecart entre
les deux variantes. Aucun fichier existant n'est modifie.

POURQUOI CETTE CORRECTION
-------------------------
`a30` section 6.2 conclut, en reprenant `a32`, que « toute densite de sous graphe partisan
publiee sans nombre de noeuds egalise est ininterpretable », et en fait son interdiction
numero 8. La lecture integrale du depot de code de Chen et de ses coauteurs, rapportee
dans `corpus/lecture-complete/05`, oblige a corriger ce diagnostic sur un point de fond :
leur `get_density_weighted` divise la somme des poids d'arete par le nombre de paires de
noeuds DU SOUS GRAPHE LUI MEME issues d'items differents. Le denominateur suit donc deja
la taille du sous graphe, et notre propre `a30_resin_twin.densite` fait exactement la meme
chose (moyenne des poids d'arete sur les paires eligibles du sous graphe).

La dependance residuelle au nombre de noeuds n'est donc pas un artefact de denominateur.
C'est un effet de composition : les seize modalites que le camp de droite detient en plus
sont en majorite des modalites neutres et peu endossees, et une modalite peu endossee a un
phi faible avec presque tout. Or l'absorption des positions neutres par le camp
republicain est le phenomene decrit par Luders et par Chen, pas un biais qui le masque.

Les deux variantes repondent donc a deux questions differentes, et aucune ne remplace
l'autre :
  brut     : « le stock de positions que ce camp detient effectivement est il serre ? »
  egalise  : « les positions les plus caracteristiques de ce camp, a nombre egal, sont
              elles serrees ? »
L'interdiction numero 8 de `a30` doit etre remplacee par une obligation : publier les deux,
avec le nombre de noeuds et le nombre de modalites employees a cote.

SORTIES : resultats/a37-densite-deux-variantes.csv,
          resultats/a37-densite-composition.csv

Usage : .venv/bin/python analyses/a37_densite.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402

NEUTRE = 3
QUESTION = {
    "brut": "le stock de positions que ce camp detient effectivement est il serre",
    "egalise": "les positions les plus caracteristiques de ce camp, a nombre egal de "
               "noeuds, sont elles serrees",
    "sans neutre": "les positions non neutres que ce camp detient sont elles serrees",
}


def partages(noeuds):
    """Reconstruit les trois partages de noeuds de a30_resin_twin, par arithmetique pure.

    brut        : le noeud va au camp qui l'endosse le plus, taux rapporte a l'effectif.
    egalise     : les K noeuds les plus caracteristiques de chaque camp, K etant le
                  minimum des deux effectifs bruts.
    sans neutre : le partage brut prive des dix modalites « ni l'un ni l'autre ».
    """
    ecart = (noeuds["taux_droite"] - noeuds["taux_gauche"]).to_numpy()
    droite = noeuds["camp"].to_numpy() == "droite"
    gauche = ~droite
    k = int(min(droite.sum(), gauche.sum()))
    od = np.argsort(-ecart)
    og = np.argsort(ecart)
    d_eg = np.zeros(len(ecart), dtype=bool); d_eg[od[:k]] = True
    g_eg = np.zeros(len(ecart), dtype=bool); g_eg[og[:k]] = True
    pas_neutre = noeuds["modalite"].to_numpy() != NEUTRE
    return {"brut": (droite, gauche),
            "egalise": (d_eg, g_eg),
            "sans neutre": (droite & pas_neutre, gauche & pas_neutre)}


def main():
    dens = pd.read_csv(os.path.join(C.SORTIE, "a30-resin-twin-densites.csv"))
    noeuds = pd.read_csv(os.path.join(C.SORTIE, "a30-resin-twin-noeuds.csv"))

    # ------------------------------------------------------- composition des partages
    lignes = []
    for nom, (d, g) in partages(noeuds).items():
        for camp, m in (("droite", d), ("gauche", g)):
            taux = noeuds["taux_droite" if camp == "droite" else "taux_gauche"].to_numpy()
            lignes.append({
                "partage_des_noeuds": nom, "camp": camp,
                "n_noeuds": int(m.sum()),
                "n_noeuds_neutres": int((m & (noeuds["modalite"].to_numpy() == NEUTRE)).sum()),
                "taux_endossement_moyen": float(taux[m].mean()),
                "taux_endossement_median": float(np.median(taux[m])),
                "n_noeuds_endosses_sous_10_pour_cent": int((taux[m] < 0.10).sum()),
                "ce_que_la_densite_mesure": QUESTION[nom],
            })
    comp = pd.DataFrame(lignes)
    C.ecrire(comp, "a37-densite-composition.csv")
    print(comp.to_string(index=False), flush=True)

    # ------------------------------------------------------- les deux variantes cote a cote
    pivot = []
    for cond in dens["condition"].unique():
        d = dens[dens["condition"] == cond].set_index("partage_des_noeuds")
        lig = {"condition": cond,
               "modalites_employees_sur_50": int(d["modalites_employees"].iloc[0]),
               "taille_par_camp": int(d["taille_par_camp"].iloc[0])}
        for nom in ("brut", "egalise", "sans neutre"):
            if nom not in d.index:
                continue
            r = d.loc[nom]
            cle = nom.replace(" ", "_")
            lig[f"noeuds_droite_{cle}"] = int(r["noeuds_droite"])
            lig[f"noeuds_gauche_{cle}"] = int(r["noeuds_gauche"])
            lig[f"densite_droite_{cle}"] = float(r["densite_droite_effectifs_egaux"])
            lig[f"densite_gauche_{cle}"] = float(r["densite_gauche_effectifs_egaux"])
            lig[f"ratio_{cle}"] = float(r["ratio_effectifs_egaux"])
            lig[f"ic_bas_{cle}"] = float(r["ic_bas"])
            lig[f"ic_haut_{cle}"] = float(r["ic_haut"])
        pivot.append(lig)
    tab = pd.DataFrame(pivot)

    # L'ecart entre les deux variantes, qui est la quantite dont a30 disait qu'elle
    # rendait la variante brute ininterpretable, et qui est en fait la mesure de
    # l'absorption des modalites neutres par le camp de droite.
    tab["ecart_egalise_moins_brut"] = tab["ratio_egalise"] - tab["ratio_brut"]
    ref = tab.loc[tab["condition"] == "humains vagues 1 a 3"].iloc[0]
    v4 = tab.loc[tab["condition"] == "humains vague 4"].iloc[0]
    plancher = abs(float(v4["ratio_egalise"]) - float(ref["ratio_egalise"]))
    tab["ecart_aux_humains_egalise"] = tab["ratio_egalise"] - float(ref["ratio_egalise"])
    tab["ecart_aux_humains_brut"] = tab["ratio_brut"] - float(ref["ratio_brut"])
    tab["depasse_le_plancher_de_bruit"] = \
        tab["ecart_aux_humains_egalise"].abs() > plancher
    tab["plancher_de_bruit_vague4"] = plancher
    C.ecrire(tab, "a37-densite-deux-variantes.csv")

    cols = ["condition", "noeuds_droite_brut", "noeuds_gauche_brut", "ratio_brut",
            "ratio_egalise", "ratio_sans_neutre", "ecart_egalise_moins_brut",
            "modalites_employees_sur_50", "depasse_le_plancher_de_bruit"]
    print(tab[cols].to_string(index=False), flush=True)
    print(f"\nplancher de bruit entre vagues, variante egalisee : {plancher:.4f}",
          flush=True)


if __name__ == "__main__":
    main()
