"""
a46b_items_candidats : les items de composition disponibles pour un run elargi.

Aucun appel de modele. Lecture seule. Repond a une question et une seule : quels groupes
supplementaires le jeu de Stanford permet il de mesurer camp par camp, de sorte qu'un run
de composition elargi puisse porter assez d'items pour que le test preenregistre devienne
decidable. Chaque ligne rend la part reelle du groupe dans chaque camp, sous les deux
ancrages, avec un intervalle de Wilson, exactement comme a46_appariement le fait pour les
huit items d'Ahler et Sood.

Ce script ne propose aucun libelle d'invite et ne prejuge d'aucun stereotype : il dit ce
qui est mesurable, pas ce qu'il faut demander.

Sortie : resultats/a46b-items-candidats.csv
Usage  : .venv/bin/python analyses/a46b_items_candidats.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402


def _norm(v):
    return str(v).strip().lower() if v is not None else ""


CANDIDATS = [
    # (cle, libelle, source, colonne, regle)
    ("blanc", "blancs", "demographie", "demo_race",
     lambda d: d["demo_race"].map(_norm).str.contains("white")),
    # `hispanic` est bien un item du GSS du jeu de Stanford mais il n'est PAS dans les
    # 149 items cibles du run r1 : son terme de modele n'existe pas et coute des appels.
    ("hispanique", "hispaniques", "item du GSS, hors des 149", "hispanic",
     lambda d: d["hispanic"].map(_norm) == "hispanic"),
    ("femme", "femmes", "demographie", "demo_gender",
     lambda d: d["demo_gender"].map(_norm) == "female"),
    ("diplome", "diplomes du superieur, licence ou plus", "demographie", "demo_education",
     lambda d: d["demo_education"].map(_norm).isin({"bachelor's", "graduate"})),
    ("jeune", "moins de 30 ans", "demographie", "demo_age",
     lambda d: d["demo_age"].map(_norm).isin({"18 - 24", "25 - 34"})),
    ("rural", "habitants de zone rurale", "demographie", "demo_neighborhood",
     lambda d: d["demo_neighborhood"].map(_norm) == "rural"),
    ("urbain", "habitants de zone urbaine", "demographie", "demo_neighborhood",
     lambda d: d["demo_neighborhood"].map(_norm) == "urban"),
    ("bas_revenu", "revenu du foyer sous 25 000 dollars", "demographie", "demo_income",
     lambda d: d["demo_income"].map(_norm) == "less than $25,000"),
    ("cent_mille", "revenu du foyer a 100 000 dollars ou plus", "demographie",
     "demo_income",
     lambda d: d["demo_income"].map(_norm).isin({
         "$100,000 to $124,999", "$125,000 to $149,999", "$150,000 to $174,999",
         "$175,000 to $199,999", "$200,000 to $249,999", "$250,000 or more"})),
    ("arme", "possesseurs d'une arme a feu", "item du GSS, dans les 149", "owngun",
     lambda d: d["owngun"].map(_norm) == "yes"),
    ("fonction_publique", "employes du secteur public", "item du GSS, dans les 149",
     "wrkgovt1", lambda d: d["wrkgovt1"].map(_norm) == "yes"),
    ("chasseur", "chasseurs", "item du GSS, dans les 149", "hunt1",
     lambda d: d["hunt1"].map(_norm).isin({"you hunt", "both hunt"})),
    ("jamais_office", "n'assistant jamais a un office religieux",
     "item du GSS, dans les 149", "attend",
     lambda d: d["attend"].map(_norm) == "never"),
    ("classe_ouvriere", "se declarant de la classe ouvriere",
     "item du GSS, dans les 149", "class",
     lambda d: d["class"].map(_norm) == "working class"),
    # `jew` est ecarte a dessein : c'est un item a branchement, 740 personnes y sont
    # « inapplicable (not jewish) » mais 188 repondent « none of these » sans etre
    # juives, de sorte que le complement du « inapplicable » n'est pas la part juive.
]


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)


def main():
    d = C.charger_gss()
    partitions = {"ideologie": "camp_ideo", "parti": "camp_parti"}
    lignes = []
    for cle, libelle, source, colonne, regle in CANDIDATS:
        if colonne not in d.columns:
            lignes.append({"cle": cle, "groupe": libelle, "source": source,
                           "colonne": colonne, "partition": "", "camp": "",
                           "n_classes": 0, "n_dans_le_groupe": 0,
                           "part_pourcent": np.nan, "ic_bas": np.nan, "ic_haut": np.nan,
                           "note": "colonne absente du jeu de Stanford"})
            continue
        appartient = regle(d).fillna(False)
        for nom_part, col_camp in partitions.items():
            for camp in ["gauche", "centre", "droite", "ensemble"]:
                sous = d if camp == "ensemble" else d[d[col_camp] == camp]
                m = appartient.loc[sous.index]
                n, k = int(len(sous)), int(m.sum())
                bas, haut = wilson(k, n)
                lignes.append({
                    "cle": cle, "groupe": libelle, "source": source,
                    "colonne": colonne, "partition": nom_part, "camp": camp,
                    "n_classes": n, "n_dans_le_groupe": k,
                    "part_pourcent": 100.0 * k / n if n else np.nan,
                    "ic_bas": bas, "ic_haut": haut,
                    "note": ("aucun appel de modele n'existe pour ce groupe ; il faut "
                             "une question de composition directe"),
                })
    out = pd.DataFrame(lignes)
    print(C.ecrire(out, "a46b-items-candidats.csv"), len(out), "lignes")
    t = out[(out["camp"] != "centre")].pivot_table(
        index=["cle", "groupe", "source"], columns=["partition", "camp"],
        values="part_pourcent")
    pd.set_option("display.width", 250)
    print(t.round(1).to_string())


if __name__ == "__main__":
    main()
