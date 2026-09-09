"""
a46_ahler_sood : ce que les humains croient de la composition des partis, item par item.

Volet 1 de a46. Aucun appel de modele de langage. Lecture seule sur data/. Aucun fichier
existant du depot n'est modifie.

Ce script produit le SECOND TERME de la comparaison a trois termes du programme A de
MOONSHOTS.md : la croyance humaine de second ordre. Il ne le compare a rien ici ; il
l'etablit, avec sa realite de reference et sa mesure d'exageration, dans les unites que
les auteurs ont employees, pour que a46_trois_termes puisse y poser le terme du modele.

Ce qu'il calcule, dans les definitions du code de replication d'Ahler et Sood :
  - la perception moyenne de chaque item, brute et ponderee, avec IC bootstrap ;
  - l'exageration en points (perception moins realite) et en rapport (perception sur
    realite), les deux, parce que les deux racontent des choses differentes sur des
    groupes dont la realite va de 2,2 a 35,7 pour cent ;
  - l'erreur relative moyenne PAR REPONDANT, `(x - reel) / reel` moyennee sur les
    personnes puis sur les items, qui est la quantite exacte des lignes 160 a 172 du
    fichier .do et celle que le papier cite ;
  - la meme chose separee par parti du repondant, ce qui donne l'ecart endogroupe
    exogroupe, colonnes 3 et 4 de leur tableau 1 ;
  - les trois replications MTurk, dont l'etude sur les explications alternatives et ses
    quatre conditions, qui est le controle qui rend le resultat difficile a attribuer a
    l'innumeratie, a l'expressivite ou a l'ignorance des taux de base.

Entree  : data/ahler-sood-pcomp/*.dta
Sortie  : resultats/a46-ahler-sood-items.csv
          resultats/a46-ahler-sood-par-repondant.csv
          resultats/a46-ahler-sood-controles.csv

Usage : .venv/bin/python analyses/a46_ahler_sood.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402


# Les colonnes de perception, etude par etude. Les quatre etudes ne nomment pas leurs
# variables de la meme facon ; les noms canoniques d'ITEMS_AS sont presents dans les trois
# jeux MTurk sous forme de variables derivees, ce qui est verifie a la lecture.
ETUDES = [
    ("YouGov", "pcomp_yougov_data.dta", "echantillon en ligne apparie, 1 000 adultes",
     "weight"),
    ("MTurk explications alternatives", "alt_exps_data.dta",
     "MTurk, quatre conditions, condition standard comprise", None),
    ("MTurk affect partisan", "affect_exp_data.dta",
     "MTurk, mesure avant traitement", None),
    ("MTurk extremite percue", "extremity_exp_data.dta",
     "MTurk, mesure avant traitement, une ligne par personne et par enjeu", None),
]

# Dans extremity_exp_data les perceptions sont prefixees d_comp_per_ / r_comp_per_ et le
# fichier est en format long, quatre lignes par personne. On repasse en une ligne par
# personne avant toute moyenne, sinon chaque repondant compte quatre fois.
RENOM_EXTREMITE = {
    "d_comp_per_black": "dem_black", "d_comp_per_union": "dem_union",
    "d_comp_per_aa": "dem_aa", "d_comp_per_lgb": "dem_lgb",
    "r_comp_per_evang": "rep_evang", "r_comp_per_rich": "rep_rich",
    "r_comp_per_young": "rep_old", "r_comp_per_south": "rep_south",
}


def perceptions(nom_etude, d, poids):
    """Extrait, pour une etude, la matrice des huit perceptions, une ligne par personne."""
    d = d.copy()
    if nom_etude == "MTurk extremite percue":
        d = d.rename(columns=RENOM_EXTREMITE)
        d = d.drop_duplicates(subset=["responseid"])
    presentes = [it for it in C.ORDRE_AS if it in d.columns]
    w = d[poids].to_numpy(dtype=float) if poids and poids in d.columns else None
    return d, presentes, w


def ligne_item(nom_etude, description, item, x, w, reel, rng):
    """Une ligne du tableau des items : perception, realite, et les deux exagerations."""
    x = np.asarray(x, dtype=float)
    m = np.isfinite(x)
    xv = x[m]
    n = int(m.sum())
    if n == 0:
        return None
    moy, bas, haut = C.ic_moyenne(xv, rng)
    wmoy = float(np.average(xv, weights=w[m])) if w is not None else float("nan")
    # Erreur relative individuelle, la quantite du fichier .do : on moyenne le rapport,
    # on ne rapporte pas les moyennes. Les deux different, et c'est la premiere que le
    # papier cite.
    err_rel = (xv - reel) / reel
    err_rel_moy, err_rel_bas, err_rel_haut = C.ic_moyenne(err_rel, rng)
    info = C.ITEMS_AS[item]
    return {
        "etude": nom_etude, "description_echantillon": description,
        "item": item, "parti_decrit": info["parti_as"], "groupe": info["groupe"],
        "question_en": info["question_en"],
        "n_repondants": n,
        "perception_moyenne": moy,
        "perception_moyenne_ponderee": wmoy,
        "perception_ic_bas": bas, "perception_ic_haut": haut,
        "perception_mediane": float(np.median(xv)),
        "perception_ecart_type": float(xv.std(ddof=1)) if n > 1 else float("nan"),
        "realite_ahler_sood": reel,
        "source_realite": info["source_realite_as"],
        "exageration_points": moy - reel,
        "exageration_ratio": moy / reel if reel else float("nan"),
        "erreur_relative_moyenne": err_rel_moy,
        "erreur_relative_ic_bas": err_rel_bas,
        "erreur_relative_ic_haut": err_rel_haut,
        "part_au_dessus_de_la_realite": float((xv > reel).mean()),
        "part_sous_estimant": float((xv < reel).mean()),
    }


def tableau_items(jeux, rng):
    lignes = []
    for (nom, fichier, description, poids), d in zip(ETUDES, jeux):
        d, presentes, w = perceptions(nom, d, poids)
        for item in presentes:
            reel = C.ITEMS_AS[item]["realite_as_arrondie"]
            l = ligne_item(nom, description, item, d[item], w, reel, rng)
            if l is not None:
                lignes.append(l)
    return pd.DataFrame(lignes)


def tableau_par_repondant(yougov, rng):
    """Colonnes 3 et 4 du tableau 1 : la perception selon le parti du repondant.

    Le repliement partisan est celui du fichier .do : les « lean » sont comptes avec le
    parti dont ils se disent proches, « Independent » seul reste independant, et « Not
    sure » sort. C'est aussi le repliement de a30, donc rien ne diverge entre les deux
    cotes de la comparaison.
    """
    d = yougov.copy()
    pid = d["pid7"].astype(str).str.strip()
    parti = pd.Series(index=d.index, dtype=object)
    parti[pid.isin(["Strong Democrat", "Not very strong Democrat",
                    "Lean Democrat"])] = "Democrate"
    parti[pid.isin(["Strong Republican", "Not very strong Republican",
                    "Lean Republican"])] = "Republicain"
    parti[pid == "Independent"] = "Independant"
    d["parti_repondant"] = parti
    w = d["weight"].to_numpy(dtype=float)

    lignes = []
    for item in C.ORDRE_AS:
        reel = C.ITEMS_AS[item]["realite_as_arrondie"]
        info = C.ITEMS_AS[item]
        for groupe_rep in ["Democrate", "Independant", "Republicain", "tous"]:
            m = (d["parti_repondant"] == groupe_rep) if groupe_rep != "tous" \
                else pd.Series(True, index=d.index)
            m = m & d[item].notna()
            if m.sum() < 5:
                continue
            x = d.loc[m, item].to_numpy(dtype=float)
            moy, bas, haut = C.ic_moyenne(x, rng)
            err_rel = (x - reel) / reel
            e, eb, eh = C.ic_moyenne(err_rel, rng)
            # Endogroupe ou exogroupe : le parti decrit est celui de l'item.
            if groupe_rep == "tous":
                position = "tous"
            elif groupe_rep == "Independant":
                position = "independant"
            elif (info["parti_as"] == "Democratic") == (groupe_rep == "Democrate"):
                position = "endogroupe"
            else:
                position = "exogroupe"
            lignes.append({
                "item": item, "parti_decrit": info["parti_as"], "groupe": info["groupe"],
                "parti_repondant": groupe_rep, "position": position,
                "n_repondants": int(m.sum()),
                "perception_moyenne": moy,
                "perception_moyenne_ponderee": float(np.average(x, weights=w[m.to_numpy()])),
                "perception_ic_bas": bas, "perception_ic_haut": haut,
                "realite_ahler_sood": reel,
                "exageration_points": moy - reel,
                "exageration_ratio": moy / reel if reel else float("nan"),
                "erreur_relative_moyenne": e,
                "erreur_relative_ic_bas": eb, "erreur_relative_ic_haut": eh,
            })
    return pd.DataFrame(lignes)


def tableau_controles(yougov, alt, affect, extremity, fig1, rng):
    """Les controles qui decident si l'exageration humaine est un artefact.

    Trois blocs, dans cet ordre :
      1. la verification que nos moyennes ponderees retombent sur fig_1_data.dta, le
         fichier produit par le code des auteurs ; si elles n'y retombent pas, tout le
         reste est faux et il faut le voir ici et pas dans le rapport ;
      2. l'erreur relative moyenne agregee, par parti du repondant, la statistique que le
         papier resume ;
      3. l'etude des explications alternatives, condition par condition : demande simple,
         somme a 100 imposee, incitation financiere, taux de base fournis.
    """
    lignes = []

    f = fig1.copy()
    f["item"] = f["Party"].str[:3].str.lower().replace({"dem": "dem", "rep": "rep"}) \
        + "_" + f["Group"].map({
            "Black": "black", "Union": "union", "Atheist/Agnostic": "aa", "LGB": "lgb",
            "Evangelical": "evang", "$250K+ Income": "rich", "Age 65+": "old",
            "Southern": "south"})
    w = yougov["weight"].to_numpy(dtype=float)
    for _, r in f.iterrows():
        item = r["item"]
        x = yougov[item].to_numpy(dtype=float)
        m = np.isfinite(x)
        nous = float(np.average(x[m], weights=w[m]))
        lignes.append({
            "bloc": "verification contre fig_1_data.dta", "cle": item,
            "quantite": "perception moyenne ponderee",
            "valeur": nous, "reference": float(r["perc_mean"]),
            "ecart": nous - float(r["perc_mean"]), "n": int(m.sum()),
            "note": ("recalcul de notre cote contre le fichier produit par le code de "
                     "replication des auteurs ; un ecart au dela de 0,01 point est un bug")})
        lignes.append({
            "bloc": "verification contre fig_1_data.dta", "cle": item,
            "quantite": "realite citee",
            "valeur": C.ITEMS_AS[item]["realite_as_arrondie"],
            "reference": float(r["true_mean"]),
            "ecart": C.ITEMS_AS[item]["realite_as_arrondie"] - float(r["true_mean"]),
            "n": np.nan,
            "note": ("la valeur arrondie est celle que les auteurs emploient dans leurs "
                     "propres calculs d'erreur relative, lignes 160 a 167 du .do")})

    d = yougov.copy()
    pid = d["pid7"].astype(str).str.strip()
    d["dem"] = pid.isin(["Strong Democrat", "Not very strong Democrat", "Lean Democrat"])
    d["rep"] = pid.isin(["Strong Republican", "Not very strong Republican",
                         "Lean Republican"])
    err = {}
    for item in C.ORDRE_AS:
        reel = C.ITEMS_AS[item]["realite_as_arrondie"]
        err[item] = (d[item].to_numpy(dtype=float) - reel) / reel
    err_dem = np.nanmean(np.vstack([err[i] for i in C.ORDRE_AS if i.startswith("dem")]), axis=0)
    err_rep = np.nanmean(np.vstack([err[i] for i in C.ORDRE_AS if i.startswith("rep")]), axis=0)
    err_all = np.nanmean(np.vstack([err[i] for i in C.ORDRE_AS]), axis=0)
    for nom, serie, masque in [
            ("erreur relative moyenne, huit items, tous repondants", err_all, None),
            ("erreur relative moyenne, items democrates, repondants democrates",
             err_dem, d["dem"].to_numpy()),
            ("erreur relative moyenne, items democrates, repondants republicains",
             err_dem, d["rep"].to_numpy()),
            ("erreur relative moyenne, items republicains, repondants republicains",
             err_rep, d["rep"].to_numpy()),
            ("erreur relative moyenne, items republicains, repondants democrates",
             err_rep, d["dem"].to_numpy())]:
        x = serie if masque is None else serie[masque]
        moy, bas, haut = C.ic_moyenne(x, rng)
        lignes.append({"bloc": "erreur relative agregee", "cle": nom,
                       "quantite": "moyenne sur les personnes puis sur les items",
                       "valeur": moy, "reference": bas, "ecart": haut,
                       "n": int(np.isfinite(x).sum()),
                       "note": "reference et ecart portent ici les bornes de l'IC a 95 pour cent"})

    for condition, g in alt.groupby("condition"):
        for item in C.ORDRE_AS:
            if item not in g.columns:
                continue
            x = g[item].to_numpy(dtype=float)
            x = x[np.isfinite(x)]
            if len(x) < 5:
                continue
            reel = C.ITEMS_AS[item]["realite_as_arrondie"]
            lignes.append({
                "bloc": "explications alternatives, par condition",
                "cle": f"{condition} | {item}",
                "quantite": "perception moyenne",
                "valeur": float(x.mean()), "reference": reel,
                "ecart": float(x.mean()) - reel, "n": len(x),
                "note": ("conditions : simpleask demande standard, complexask somme a 100 "
                         "imposee, incentive prime a l'exactitude, baserates_given taux "
                         "de base de la population fournis")})
    return pd.DataFrame(lignes)


def main():
    rng = np.random.default_rng(C.GRAINE)
    yougov, alt, affect, extremity, fig1 = C.charger_ahler_sood()
    jeux = [yougov, alt, affect, extremity]

    items = tableau_items(jeux, rng)
    par_rep = tableau_par_repondant(yougov, rng)
    ctl = tableau_controles(yougov, alt, affect, extremity, fig1, rng)

    print(C.ecrire(items, "a46-ahler-sood-items.csv"), len(items), "lignes")
    print(C.ecrire(par_rep, "a46-ahler-sood-par-repondant.csv"), len(par_rep), "lignes")
    print(C.ecrire(ctl, "a46-ahler-sood-controles.csv"), len(ctl), "lignes")

    yg = items[items["etude"] == "YouGov"].set_index("item").loc[C.ORDRE_AS]
    print("\nYouGov, 1 000 adultes, perception moyenne contre realite :")
    for item, r in yg.iterrows():
        print(f"  {item:11s} {r['perception_moyenne']:6.1f} %  contre "
              f"{r['realite_ahler_sood']:5.1f} %   "
              f"x{r['exageration_ratio']:5.2f}   "
              f"+{r['exageration_points']:5.1f} pts   "
              f"erreur relative moyenne {r['erreur_relative_moyenne']:+6.2f}")
    verif = ctl[(ctl["bloc"] == "verification contre fig_1_data.dta")
                & (ctl["quantite"] == "perception moyenne ponderee")]
    print(f"\necart maximal a fig_1_data.dta : {verif['ecart'].abs().max():.2e} point")


if __name__ == "__main__":
    main()
