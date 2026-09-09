"""
a46_appariement : quels items d'Ahler et Sood ont un homologue dans le GSS, et lequel.

Volet 2 de a46. Aucun appel de modele de langage. Lecture seule sur data/. Aucun fichier
existant du depot n'est modifie.

Ce script fait deux choses et les separe soigneusement.

1. Il calcule la REALITE CONTEMPORAINE de chacun des huit groupes d'Ahler et Sood dans le
   jeu GSS de Stanford, camp par camp, sous les deux ancrages du dossier : l'ideologie
   declaree, qui est l'ancrage du run r1, et le parti declare, qui est l'ancrage d'Ahler
   et Sood. Les deux, parce que la comparaison a trois termes se casse en silence si on
   met un terme mesure par parti en face d'un terme mesure par ideologie.

2. Il construit l'appariement item par item, avec pour chaque ligne le degre de confiance,
   l'ecart declare entre la definition du GSS et celle d'Ahler et Sood, et surtout la
   colonne qui decide de ce que le matin peut faire : `dispo_terme_modele_r1`, vrai
   seulement quand le run r1 a deja demande cet item aux modeles.

Un avertissement porte par les tableaux eux memes. Les 1 052 personnes du jeu de Stanford
ne sont pas un echantillon representatif des Etats Unis : 40,5 pour cent y declarent
n'avoir aucune religion, contre environ 28 pour cent dans les enquetes nationales. La
composition calculee ici est celle de CET echantillon. Elle est le bon referent pour le
run r1, qui decrit ces camps la, et elle n'est pas le referent d'Ahler et Sood, qui est
l'ANES 2012 ponderee. Les deux realites figurent cote a cote et ne doivent jamais etre
melangees dans un meme rapport.

Entree  : data/osf-t6g7k-stanford (vague 1, demographies)
          registre et definitions de a46_commun
Sortie  : resultats/a46-composition-gss-2024.csv
          resultats/a46-appariement.csv

Usage : .venv/bin/python analyses/a46_appariement.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402


# Les 149 items que r1 interroge. Lus par la meme fonction que r1, pour qu'aucune liste
# recopiee ne puisse diverger.
def items_r1():
    from a2_baselines_gss import charger
    _, items, _, _, _, _ = charger()
    return set(items)


# --------------------------------------------------------------------------------------
# 1. La composition reelle, camp par camp
# --------------------------------------------------------------------------------------

def composition(d, items_du_run):
    """Part de chaque groupe dans chaque camp, sous les deux ancrages, avec IC de Wilson.

    Le denominateur exclut les personnes dont l'information de groupe est absente, meme
    convention qu'en a2 et a30. Le nombre de manquants est rendu dans sa propre colonne :
    sur l'orientation sexuelle il monte a 18 pour cent, et une part calculee sur 82 pour
    cent des gens n'est pas la meme chose qu'une part calculee sur tout le monde.
    """
    lignes = []
    for item in C.ORDRE_AS:
        for defn in C.DEFS_GSS[item]:
            colonne = defn["colonne"]
            if colonne not in d.columns:
                continue
            appartient = defn["regle"](d)
            renseigne = d[colonne].notna() & (d[colonne].astype(str).str.strip() != "")
            if item == "dem_aa" and defn["variante"] == "stricte":
                renseigne = renseigne & d["attend"].notna()
            if item == "rep_evang" and defn["variante"] == "stricte":
                renseigne = renseigne & d["relig*"].notna()
            for partition, colonne_camp in (("ideologie", "camp_ideo"),
                                            ("parti", "camp_parti")):
                for camp in ["gauche", "centre", "droite", "ensemble"]:
                    m = renseigne & ((d[colonne_camp] == camp) if camp != "ensemble"
                                     else pd.Series(True, index=d.index))
                    n = int(m.sum())
                    k = int((appartient & m).sum())
                    p, bas, haut = C.wilson(k, n)
                    lignes.append({
                        "item_as": item,
                        "groupe": C.ITEMS_AS[item]["groupe"],
                        "variante": defn["variante"],
                        "source_gss": defn["source"],
                        "colonne_gss": colonne,
                        "dans_les_149_items": colonne in items_du_run,
                        "partition": partition, "camp": camp,
                        "n_classes": n,
                        "n_non_renseigne": int(((d[colonne_camp] == camp)
                                                if camp != "ensemble"
                                                else pd.Series(True, index=d.index)).sum() - n),
                        "n_dans_le_groupe": k,
                        "part_pourcent": p,
                        "ic_bas": bas, "ic_haut": haut,
                        "confiance_appariement": defn["confiance"],
                        "ecart_a_ahler_sood": defn["ecart"],
                    })
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------------------------
# 2. L'appariement
# --------------------------------------------------------------------------------------

# Le camp du GSS qui tient lieu du parti decrit par Ahler et Sood. Sous l'ancrage parti,
# c'est direct ; sous l'ancrage ideologie, c'est une substitution, et elle est declaree.
CAMP_POUR_PARTI = {"Democratic": "gauche", "Republican": "droite"}


def appariement(comp, items_du_run):
    """Une ligne par (item d'Ahler et Sood, variante), avec ce que chaque terme vaut."""
    lignes = []
    for item in C.ORDRE_AS:
        info = C.ITEMS_AS[item]
        camp = CAMP_POUR_PARTI[info["parti_as"]]
        for defn in C.DEFS_GSS[item]:
            sel = comp[(comp["item_as"] == item)
                       & (comp["variante"] == defn["variante"])]
            def val(partition, camp_, colonne="part_pourcent"):
                s = sel[(sel["partition"] == partition) & (sel["camp"] == camp_)]
                return float(s[colonne].iloc[0]) if len(s) else float("nan")
            lignes.append({
                "role": "composition",
                "item_as": item, "groupe_as": info["groupe"],
                "parti_as": info["parti_as"],
                "question_as": info["question_en"],
                "variante_gss": defn["variante"],
                "source_gss": defn["source"],
                "colonne_gss": defn["colonne"],
                "camp_gss_ideologie": camp,
                "camp_gss_parti": camp,
                "confiance": defn["confiance"],
                "dispo_terme_modele_r1": bool(defn["dispo_r1"]
                                              and defn["colonne"] in items_du_run),
                "dispo_terme_modele_run_composition": True,
                "realite_ahler_sood_anes2012": info["realite_as_arrondie"],
                "realite_gss2024_parti": val("parti", camp),
                "realite_gss2024_parti_ic_bas": val("parti", camp, "ic_bas"),
                "realite_gss2024_parti_ic_haut": val("parti", camp, "ic_haut"),
                "realite_gss2024_ideologie": val("ideologie", camp),
                "realite_gss2024_ensemble": val("parti", "ensemble"),
                "note": defn["ecart"],
            })

    # Le volet opinion, celui qui manque. Il est ecrit ici pour que son absence soit un
    # element du tableau et non un oubli qu'on redecouvre au mois 3.
    opinion = [
        ("IGS Poll, 25 enonces de politique publique",
         "q19_1 a q19_6 et q98_1 a q98_6, part percue de democrates et de republicains "
         "soutenant chaque enonce, six enonces tires au hasard par repondant sur 25",
         "absent du depot public",
         ("C'est le SEUL endroit ou Ahler et Sood mesurent une croyance de second ordre "
          "sur des OPINIONS, avec pour referent les reponses de la meme enquete. C'est "
          "l'homologue exact de la quantite de r1. Le fichier pcomp_igspoll.dta n'est pas "
          "dans l'archive Dataverse, le readme le cite pourtant. Sans lui, la comparaison "
          "a trois termes sur des opinions n'a pas de terme humain."),
         "faible" ),
        ("Etude d'extremite percue, 4 enjeux",
         "dem_per et rep_per, part percue de chaque parti soutenant l'enjeu, sur tax, "
         "abortion, gays et race ; d_ext_per_* et r_ext_per_* pour le placement",
         "present, mais sans verite terrain ni libelle",
         ("Les variables de perception sont dans extremity_exp_data.dta et sont bien des "
          "croyances de second ordre sur des opinions. Deux choses manquent : le libelle "
          "exact des quatre enonces, absent de l'archive, et la distribution reelle des "
          "partis sur ces enonces, que les auteurs n'ont jamais mesuree. Sans realite, "
          "pas d'exageration, donc pas de second terme."),
         "faible"),
    ]
    for source, variables, statut, note, confiance in opinion:
        lignes.append({
            "role": "opinion", "item_as": source, "groupe_as": "", "parti_as": "",
            "question_as": variables, "variante_gss": "", "source_gss": statut,
            "colonne_gss": "", "camp_gss_ideologie": "", "camp_gss_parti": "",
            "confiance": confiance,
            "dispo_terme_modele_r1": True,
            "dispo_terme_modele_run_composition": False,
            "realite_ahler_sood_anes2012": float("nan"),
            "realite_gss2024_parti": float("nan"),
            "realite_gss2024_parti_ic_bas": float("nan"),
            "realite_gss2024_parti_ic_haut": float("nan"),
            "realite_gss2024_ideologie": float("nan"),
            "realite_gss2024_ensemble": float("nan"),
            "note": note,
        })
    return pd.DataFrame(lignes)


def main():
    d = C.charger_gss()
    items_du_run = items_r1()
    comp = composition(d, items_du_run)
    app = appariement(comp, items_du_run)

    print(C.ecrire(comp, "a46-composition-gss-2024.csv"), len(comp), "lignes")
    print(C.ecrire(app, "a46-appariement.csv"), len(app), "lignes")

    print(f"\ncamps, ancrage ideologie : "
          f"{(d['camp_ideo'] == 'gauche').sum()} gauche, "
          f"{(d['camp_ideo'] == 'centre').sum()} centre, "
          f"{(d['camp_ideo'] == 'droite').sum()} droite")
    print(f"camps, ancrage parti    : "
          f"{(d['camp_parti'] == 'gauche').sum()} gauche, "
          f"{(d['camp_parti'] == 'centre').sum()} centre, "
          f"{(d['camp_parti'] == 'droite').sum()} droite, "
          f"{d['camp_parti'].isna().sum()} non classables")

    print("\nrealite du camp decrit, ancrage parti, variante principale :")
    p = app[(app["role"] == "composition") & (app["variante_gss"] == "principale")]
    for _, r in p.iterrows():
        print(f"  {r['item_as']:11s} {r['groupe_as']:17s} "
              f"Ahler et Sood {r['realite_ahler_sood_anes2012']:5.1f} %   "
              f"GSS 2024 parti {r['realite_gss2024_parti']:5.1f} % "
              f"[{r['realite_gss2024_parti_ic_bas']:4.1f} ; {r['realite_gss2024_parti_ic_haut']:4.1f}]   "
              f"ideologie {r['realite_gss2024_ideologie']:5.1f} %   "
              f"terme modele r1 : {'oui' if r['dispo_terme_modele_r1'] else 'non'}")


if __name__ == "__main__":
    main()
