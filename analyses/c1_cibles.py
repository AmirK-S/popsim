"""
c1_cibles : question 5 du mois 1 du programme C version menages.

Le tableau des cibles qu'une population simulee de menages devra reproduire, et les
planchers qu'elle devra depasser. Ce script ne calcule aucune quantite nouvelle : il
assemble les tableaux deja ecrits, pour que la barre du run simule et les chiffres du
rapport ne puissent pas diverger.

Trois familles de nombres, dans l'ordre de la difficulte croissante pour un gabarit.

  1. A REPRODUIRE. La dispersion totale par mois, sa part inter cohortes, la part stable
     du menage. Un gabarit de cohorte reproduit la premiere, echoue sur la deuxieme par
     exces et sur la troisieme par defaut.
  2. A DEPASSER. La chute sous permutation intra cohorte de l'historique du menage, et
     celle de la persistance seule, qui est le vrai adversaire.
  3. LES PLANCHERS. T0b, qui vaut zero par construction ; T1, lu comme nul ; et D, les
     demographies seules, qui est ce qu'un gabarit de cohorte peut esperer.

Sortie : c1-cibles-jumeau.csv. Aucune microdonnee.
"""

import numpy as np
import pandas as pd

import c1_commun as C1


def main():
    mens = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-dispersion-mensuelle.csv"))
    mens = mens[mens["perimetre"] == "primaire 2020-2025"]
    ap = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-avant-apres-choc.csv"))
    stable = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-part-stable.csv"))
    retest = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-retest-par-delai.csv"))
    prev = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-previsibilite-par-variable.csv"))
    bouge = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-qui-bouge-choc.csv"))
    nul = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-nul-a-derive.csv"))

    lignes = []
    for v in C1.VAR_PRIMAIRES + ["infl1_var", "infl1_point"]:
        m = mens[mens["variable"] == v]
        s = stable[stable["variable"] == v]
        r = retest[retest["variable"] == v].set_index("delai_mois")
        p = prev[prev["variable"] == v].set_index("predicteur")
        a_p = ap[(ap["variable"] == v) & (ap["regle"].str.startswith("primaire"))]
        a_s = ap[(ap["variable"] == v) & (ap["regle"].str.startswith("secondaire"))]
        b = bouge[(bouge["variable"] == v)
                  & (bouge["regle_choc"].str.startswith("primaire"))]
        n_p = nul[(nul["variable"] == v)
                  & (nul["regle_choc"].str.startswith("primaire"))]
        b_rev = b[b["cible"] == "Y_rev"].set_index("predicteur")
        b_dir = b[b["cible"] == "Y_dir"].set_index("predicteur")

        def val(t, col, defaut=np.nan):
            return float(t[col].iloc[0]) if len(t) else defaut

        lignes.append({
            "variable": v,
            "libelle": C1.LIBELLE[v],
            "role": "primaire" if v in C1.VAR_PRIMAIRES else "secondaire",
            # 1. a reproduire
            "iqr_median_mensuel": float(m["iqr_total"].median()),
            "variance_mediane_mensuelle": float(m["variance_totale"].median()),
            "part_inter_mediane": float(m["part_inter"].median()),
            "part_inter_min": float(m["part_inter"].min()),
            "part_inter_max": float(m["part_inter"].max()),
            "part_stable": val(s, "part_stable"),
            "part_stable_ic_bas": val(s, "ic_bas"),
            "part_stable_ic_haut": val(s, "ic_haut"),
            "retest_1_mois": float(r.loc[1, "rho"]) if 1 in r.index else np.nan,
            "retest_11_mois": float(r.loc[11, "rho"]) if 11 in r.index else np.nan,
            "ratio_iqr_au_choc_primaire": val(a_p, "ratio_iqr"),
            "ratio_iqr_au_choc_secondaire": val(a_s, "ratio_iqr"),
            "delta_moyenne_au_choc_primaire": val(a_p, "delta_moyenne"),
            # 2. a depasser
            "chute_H": float(p.loc["H", "chute"]),
            "chute_H_ic_bas": float(p.loc["H", "chute_ic_bas"]),
            "chute_P": float(p.loc["P", "chute"]),
            "chute_F": float(p.loc["F", "chute"]),
            "rho_H": float(p.loc["H", "rho"]),
            "rho_P": float(p.loc["P", "rho"]),
            "chute_qui_revise_H": float(b_rev.loc["H", "chute"]) if "H" in b_rev.index
            else np.nan,
            "chute_qui_revise_V": float(b_rev.loc["V", "chute"]) if "V" in b_rev.index
            else np.nan,
            "chute_direction_H": float(b_dir.loc["H", "chute"]) if "H" in b_dir.index
            else np.nan,
            "chute_direction_L": float(b_dir.loc["L", "chute"]) if "L" in b_dir.index
            else np.nan,
            # 3. les planchers
            "plancher_T0b": float(p.loc["T0b", "chute"]),
            "plancher_T1": float(p.loc["T1", "chute"]),
            "plancher_D": float(p.loc["D", "chute"]),
            "plancher_D_qui_revise": float(b_rev.loc["D", "chute"])
            if "D" in b_rev.index else np.nan,
            # le nul a derive
            "part_dans_le_sens_observee": val(n_p, "part_dans_le_sens_observee"),
            "part_dans_le_sens_nul": val(n_p, "part_dans_le_sens_nul"),
            "ratio_ampleur_observee_sur_nul": val(n_p, "ratio_ampleur"),
        })
    tab = pd.DataFrame(lignes)
    tab["part_de_F_captee_par_P"] = tab["chute_P"] / tab["chute_F"]
    tab["part_de_H_captee_par_V_au_choc"] = (tab["chute_qui_revise_V"]
                                             / tab["chute_qui_revise_H"])
    C1.ecrire(tab, "c1-cibles-jumeau.csv")
    print("c1_cibles termine")


if __name__ == "__main__":
    main()
