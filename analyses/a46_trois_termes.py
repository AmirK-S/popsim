"""
a46_trois_termes : realite, croyance humaine de second ordre, croyance du modele.

Volet 3 de a46, celui que le matin lance. Aucun appel de modele de langage. Lecture seule
sur data/traces/. Aucun fichier existant du depot n'est modifie.

CE QU'IL FAIT, ET CE QU'IL NE FAIT PAS
--------------------------------------
Il pose les trois termes du programme A cote a cote, sur des quantites de COMPOSITION,
c'est a dire « quelle part des soutiens de ce camp appartient a ce groupe » :

  realite            la part reelle, dans deux bases declarees et jamais melangees :
                     l'ANES 2012 ponderee, qui est la base d'Ahler et Sood, et les 1 052
                     personnes du jeu de Stanford, qui est la base du run r1 ;
  croyance humaine   la perception moyenne des 1 000 adultes de l'enquete YouGov
                     d'Ahler et Sood, item par item ;
  croyance du modele deux sources, toutes deux facultatives et lues telles qu'elles sont :
                     (a) les traces r1 deja ecrites, pour les items du GSS dont la
                         modalite EST une appartenance de groupe, `union1` et `reborn` ;
                     (b) les traces du run « composition » a46, si ce run a eu lieu.

Il ne fait PAS la comparaison a trois termes sur des opinions. Les donnees publiques
d'Ahler et Sood ne contiennent aucune croyance humaine de second ordre sur une opinion
avec sa realite : le seul jeu qui en portait, l'IGS Poll et ses 25 enonces de politique
publique, n'est pas dans l'archive Dataverse. Voir `resultats/a46-appariement.csv`,
lignes de role `opinion`.

LA QUANTITE PRINCIPALE, ET POURQUOI ELLE EST SANS BASE
------------------------------------------------------
L'exageration est un rapport, `croyance / realite`. Le rapport des deux exagerations,
`exageration du modele / exageration humaine`, est donc egal a `croyance du modele /
croyance humaine` : la realite se simplifie. C'est la quantite principale, et elle a la
propriete rare de ne dependre d'aucun choix de base de realite. Un rapport superieur a 1
dit que le modele exagere plus que les humains ; inferieur a 1, qu'il exagere moins,
c'est a dire qu'il corrige. Les exagerations prises separement, elles, dependent de la
base, et le tableau porte les deux bases en colonnes distinctes.

TESTS
-----
Unite de reechantillonnage : l'item. IC bootstrap a 95 pour cent, 2 000 tirages.
Test principal : permutation de signe appariee par item sur `log(modele) - log(humain)`,
20 000 tirages, estimateur de Phipson et Smyth. Holm a l'interieur de chaque famille, une
famille par (modele, ancrage, identite). Les familles ne sont jamais fusionnees.
Seuil 0,05 apres Holm, et un seuil de materialite : un rapport dans [0,90 ; 1,11] est
declare nul en pratique. La bande est plus large qu'en r1, [0,95 ; 1,05], parce qu'il y a
au plus huit items ici contre 149 la bas.

Entree  : resultats/a46-ahler-sood-items.csv, a46-appariement.csv,
          a46-composition-gss-2024.csv   (produits par les volets 1 et 2)
          data/traces/r1-*.jsonl, data/traces/r1-distributions-reelles.csv
          data/traces/a46-composition-*.jsonl   (facultatif)
Sortie  : resultats/a46-trois-termes.csv       une ligne par terme pose
          resultats/a46-trois-termes-tests.csv les tests, par famille
          resultats/a46-couverture.csv         ce qui a ete trouve et ce qui manque

Usage : .venv/bin/python analyses/a46_trois_termes.py
"""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402

BANDE_NULLE = (0.90, 1.11)

# --------------------------------------------------------------------------------------
# Les items du GSS dont une modalite EST une appartenance de groupe au sens d'Ahler et
# Sood. C'est la porte par laquelle deux des huit items ont deja leur terme de modele,
# sans un seul appel de plus : r1 a demande la distribution complete de ces items, et la
# somme des modalites d'appartenance est exactement la part que demande Ahler et Sood.
# --------------------------------------------------------------------------------------
PONTS_R1 = {
    "dem_union": {
        "item_gss": "union1", "variante": "principale",
        "modalites": ["You belong", "You and spouse or partner belong"],
        "camp_ideologie": "gauche",
        "note": ("union1 demande l'appartenance du repondant ou de son conjoint ; on ne "
                 "somme que les deux modalites ou le repondant lui meme est syndique"),
    },
    "rep_evang": {
        "item_gss": "reborn", "variante": "principale",
        "modalites": ["Yes"],
        "camp_ideologie": "droite",
        "note": ("« ne de nouveau » est un substitut d'evangelique, pas une traduction ; "
                 "l'ecart de definition est declare et il va dans le sens d'une part plus "
                 "large que celle d'Ahler et Sood"),
    },
}


# --------------------------------------------------------------------------------------
# 1. Le terme du modele, source (a) : les traces r1 deja ecrites
# --------------------------------------------------------------------------------------

def termes_modele_depuis_r1():
    """Part de groupe impliquee par la distribution que chaque modele a decrite en r1.

    Tolerant au partiel : un modele absent, un camp non encore couvert, une cellule
    rejetee au parse, tout cela produit simplement moins de lignes, jamais une valeur
    par defaut. Le perimetre effectif est rendu a part.
    """
    lignes, manquants = [], []
    traces = C.lire_traces_r1()
    if not traces:
        return pd.DataFrame(), ["aucune trace r1 lisible"]
    for t in traces:
        for item_as, pont in PONTS_R1.items():
            if t.get("item") != pont["item_gss"]:
                continue
            if t.get("rejet") or not t.get("distribution"):
                manquants.append(f"{t.get('cle_modele')}/{t.get('camp')}/"
                                 f"{t.get('identite')}/{pont['item_gss']} : rejet au parse")
                continue
            dist = t["distribution"]
            absentes = [m for m in pont["modalites"] if m not in dist]
            if absentes:
                manquants.append(f"{t.get('cle_modele')}/{t.get('camp')} : modalites "
                                 f"absentes de la distribution decrite, {absentes}")
                continue
            part = 100.0 * float(sum(dist[m] for m in pont["modalites"]))
            lignes.append({
                "source_modele": "traces r1 (mode description, item du GSS)",
                "item_as": item_as, "cle_modele": t.get("cle_modele"),
                "modele": t.get("modele"), "ancrage": "ideologie",
                "camp": t.get("camp"), "identite": t.get("identite"),
                "item_gss": pont["item_gss"], "variante": pont["variante"],
                "croyance_modele_pourcent": part,
                "note_pont": pont["note"],
            })
    return pd.DataFrame(lignes), manquants


# --------------------------------------------------------------------------------------
# 2. Le terme du modele, source (b) : les traces du run « composition »
# --------------------------------------------------------------------------------------

def termes_modele_depuis_composition():
    """Lit data/traces/a46-composition-*.jsonl s'il existe. Rend un tableau vide sinon.

    Format attendu, celui qu'ecrira a46_run_composition : une ligne par appel, avec les
    cles `cle_modele`, `modele`, `item_as`, `ancrage`, `camp`, `identite`, `rejet` et
    `valeur` (un pourcentage entre 0 et 100).
    """
    traces = C.lire_traces_composition()
    lignes = []
    for t in traces:
        if t.get("rejet") or t.get("valeur") is None:
            continue
        lignes.append({
            "source_modele": "run composition a46 (question directe)",
            "item_as": t.get("item_as"), "cle_modele": t.get("cle_modele"),
            "modele": t.get("modele"), "ancrage": t.get("ancrage"),
            "camp": t.get("camp"), "identite": t.get("identite"),
            "item_gss": "", "variante": t.get("variante", "principale"),
            "croyance_modele_pourcent": float(t["valeur"]),
            "note_pont": "question de composition posee directement, sans passer par un item",
        })
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------------------------
# 3. Assemblage des trois termes
# --------------------------------------------------------------------------------------

def assembler(modele, humain, appar, comp):
    """Une ligne par (item, modele, ancrage, camp, identite), avec les trois termes.

    Les colonnes de realite sont deux, jamais fusionnees : la base d'Ahler et Sood,
    l'ANES 2012 ponderee, et la base du run r1, les 1 052 personnes du jeu de Stanford.
    Toute exageration est calculee dans les deux bases, et le rapport des exagerations,
    lui, ne depend d'aucune des deux.
    """
    if modele.empty:
        return pd.DataFrame()
    hum = humain[humain["etude"] == "YouGov"].set_index("item")
    app = appar[(appar["role"] == "composition")
                & (appar["variante_gss"] == "principale")].set_index("item_as")

    def realite_gss(item_as, variante, ancrage, camp):
        # L'ancrage `population` des cellules de taux de base n'est pas une partition :
        # c'est l'ensemble des 1 052 personnes, que la table de composition porte sous
        # n'importe quelle partition avec le camp « ensemble ».
        partition = "parti" if ancrage == "population" else ancrage
        s = comp[(comp["item_as"] == item_as) & (comp["variante"] == variante)
                 & (comp["partition"] == partition) & (comp["camp"] == camp)]
        return float(s["part_pourcent"].iloc[0]) if len(s) else float("nan")

    lignes = []
    for _, r in modele.iterrows():
        item = r["item_as"]
        if item not in hum.index or item not in app.index:
            continue
        h = hum.loc[item]
        a = app.loc[item]
        m = float(r["croyance_modele_pourcent"])
        perc_h = float(h["perception_moyenne"])
        r_as = float(a["realite_ahler_sood_anes2012"])
        r_gss = realite_gss(item, r["variante"], r["ancrage"], r["camp"])
        lignes.append({
            "item_as": item, "groupe": h["groupe"], "parti_as": h["parti_decrit"],
            "source_modele": r["source_modele"],
            "cle_modele": r["cle_modele"], "modele": r["modele"],
            "ancrage": r["ancrage"], "camp": r["camp"], "identite": r["identite"],
            "item_gss": r["item_gss"], "variante": r["variante"],
            # Vrai quand le camp interroge est bien celui dont Ahler et Sood decrivent
            # la composition. Les cellules ou il est faux, par exemple la part de
            # syndiques attribuee au camp de droite, ne sont pas des erreurs : elles
            # completent le plan et sortent du test principal.
            "camp_est_celui_decrit_par_ahler_sood":
                bool(r["camp"] == ("gauche" if h["parti_decrit"] == "Democratic"
                                   else "droite")),
            # les trois termes
            "realite_ahler_sood_anes2012": r_as,
            "realite_gss2024": r_gss,
            "croyance_humaine": perc_h,
            "croyance_humaine_ic_bas": float(h["perception_ic_bas"]),
            "croyance_humaine_ic_haut": float(h["perception_ic_haut"]),
            "croyance_modele": m,
            # exagerations, base d'Ahler et Sood
            "exageration_humaine_ratio_as": perc_h / r_as if r_as else np.nan,
            "exageration_modele_ratio_as": m / r_as if r_as else np.nan,
            "exageration_humaine_points_as": perc_h - r_as,
            "exageration_modele_points_as": m - r_as,
            # exagerations, base GSS 2024
            "exageration_humaine_ratio_gss": perc_h / r_gss if r_gss else np.nan,
            "exageration_modele_ratio_gss": m / r_gss if r_gss else np.nan,
            "exageration_humaine_points_gss": perc_h - r_gss,
            "exageration_modele_points_gss": m - r_gss,
            # Deux facons de rapporter les deux exagerations, et elles ne disent pas la
            # meme chose.
            #  - « base propre » : chaque cote est divise par SA realite, celle de la
            #    population qu'on lui a decrite. C'est la lecture principale, parce que
            #    le modele a ete interroge sur un camp d'ideologie mesure sur les 1 052
            #    personnes du GSS, et les humains sur un parti mesure sur l'ANES 2012.
            #  - « cible commune » : le simple rapport des deux croyances. Il ne depend
            #    d'aucune base, mais il ne vaut que si l'on accepte que « liberal adults »
            #    et « Democratic Party supporters » designent la meme population, ce que
            #    rien ne garantit.
            "exageration_modele_ratio_base_propre": m / r_gss if r_gss else np.nan,
            "exageration_humaine_ratio_base_propre": perc_h / r_as if r_as else np.nan,
            "rapport_des_exagerations_base_propre":
                ((m / r_gss) / (perc_h / r_as)) if (r_gss and r_as and perc_h) else np.nan,
            "rapport_des_exagerations_cible_commune": m / perc_h if perc_h else np.nan,
            "ecart_des_exagerations_points_gss": (m - r_gss) - (perc_h - r_gss),
            "note_pont": r["note_pont"],
        })
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------------------------
# 4. Les tests
# --------------------------------------------------------------------------------------

def verdict(ratio, p_holm, seuil=0.05):
    if not np.isfinite(ratio) or not np.isfinite(p_holm):
        return "indecidable"
    if p_holm >= seuil:
        return "non significatif"
    if BANDE_NULLE[0] <= ratio <= BANDE_NULLE[1]:
        return "significatif mais nul en pratique"
    return ("le modele exagere plus que les humains" if ratio > 1
            else "le modele exagere moins que les humains, il corrige")


def tests(trois, rng):
    """Un test par (modele, ancrage, identite, camp) et par quantite, sur les items dispo.

    Deux quantites, declarees toutes les deux, jamais l'une sans l'autre :

      `base_propre`    log(exageration du modele) moins log(exageration humaine), chaque
                       exageration calculee contre la realite de la population qui a ete
                       decrite a ce cote la. C'est la lecture principale.
      `cible_commune`  log(croyance du modele) moins log(croyance humaine). Elle ne depend
                       d'aucune base de realite, mais elle suppose que le camp d'ideologie
                       decrit au modele et le parti decrit aux humains sont la meme
                       population. Ils ne le sont pas exactement ; c'est une lecture de
                       controle, pas un resultat.

    Le test ne porte que sur le camp qu'Ahler et Sood decrivent. On teste sur le
    logarithme et non sur le rapport brut : les huit items ont des realites qui vont de
    2,2 a 35,7 pour cent, et une moyenne de rapports bruts serait dominee par rep_rich.
    """
    if trois.empty:
        return pd.DataFrame()
    quantites = [
        ("base_propre", "exageration_modele_ratio_base_propre",
         "exageration_humaine_ratio_base_propre"),
        ("cible_commune", "croyance_modele", "croyance_humaine"),
    ]
    lignes = []
    # La source du terme de modele entre dans la cle de famille. Deux instruments
    # differents mesurent parfois le meme item, `dem_union` par exemple, qui vient a la
    # fois du pont r1 sur `union1` et de la question de composition directe : les melanger
    # dans un meme test compterait deux fois le meme item et retrecirait faussement l'IC.
    for (source, cle, ancrage, identite, camp), g0 in trois.groupby(
            ["source_modele", "cle_modele", "ancrage", "identite", "camp"], sort=False):
        # Le test ne porte que sur le camp qu'Ahler et Sood decrivent : la croyance
        # humaine mesuree porte sur les democrates pour les items dem_*, et lui opposer
        # ce que le modele dit du camp de droite serait comparer deux questions
        # differentes. Les autres cellules restent dans a46-trois-termes.csv.
        g = g0[g0["camp_est_celui_decrit_par_ahler_sood"]].reset_index(drop=True)
        if g.empty:
            continue
        for nom_quantite, col_a, col_b in quantites:
            a = g[col_a].to_numpy(dtype=float)
            b = g[col_b].to_numpy(dtype=float)
            m = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
            aa, bb = a[m], b[m]
            if len(aa) == 0:
                continue
            dlog = np.log(aa) - np.log(bb)
            rapport, bas, haut, _ = C.ic_ratio_des_moyennes(aa, bb, rng)
            p = C.p_permutation_signe(dlog, rng) if len(dlog) >= 3 else float("nan")
            lignes.append({
                "quantite": nom_quantite,
                "source_modele": source,
                "famille": f"{nom_quantite} | {source} | {cle} | {ancrage} | {identite}",
                "cle_modele": cle, "modele": g["modele"].iloc[0],
                "ancrage": ancrage, "identite": identite, "camp": camp,
                "n_items": int(len(aa)),
                "items": ",".join(sorted(g.loc[m, "item_as"].tolist())),
                "cote_modele_moyenne": float(aa.mean()),
                "cote_humain_moyenne": float(bb.mean()),
                "rapport_des_moyennes": rapport,
                "rapport_ic_bas": bas, "rapport_ic_haut": haut,
                "rapport_geometrique": float(np.exp(dlog.mean())),
                "p_permutation": p,
            })
    df = pd.DataFrame(lignes)
    if df.empty:
        return df
    # Holm a l'interieur de chaque famille, jamais entre familles.
    sortie = []
    for _, g in df.groupby("famille", sort=False):
        sous = g.to_dict("records")
        C.poser_holm(sous, cle_p="p_permutation", cle_sortie="p_holm")
        for l in sous:
            l["taille_famille"] = int(len(sous))
            l["verdict"] = verdict(l["rapport_des_moyennes"], l["p_holm"])
        sortie += sous
    return pd.DataFrame(sortie)


# --------------------------------------------------------------------------------------
# 5. Couverture
# --------------------------------------------------------------------------------------

def couverture(trois, modele_r1, modele_comp, manquants):
    """Ce qui a ete trouve et ce qui manque, item par item. C'est le tableau a lire d'abord."""
    lignes = []
    for item in C.ORDRE_AS:
        info = C.ITEMS_AS[item]
        r1 = modele_r1[modele_r1["item_as"] == item] if not modele_r1.empty \
            else pd.DataFrame()
        cp = modele_comp[modele_comp["item_as"] == item] if not modele_comp.empty \
            else pd.DataFrame()
        lignes.append({
            "item_as": item, "groupe": info["groupe"], "parti_as": info["parti_as"],
            "terme_realite": "oui, deux bases",
            "terme_humain": "oui, YouGov 1 000 adultes",
            "terme_modele_via_r1": int(len(r1)),
            "terme_modele_via_run_composition": int(len(cp)),
            "modeles_couverts": ",".join(sorted(set(
                (list(r1["cle_modele"]) if len(r1) else [])
                + (list(cp["cle_modele"]) if len(cp) else [])))),
            "comparaison_a_trois_termes_possible": bool(len(r1) or len(cp)),
            "ce_qui_manque": "" if (len(r1) or len(cp))
                else ("aucun item du GSS ne porte cette appartenance dans les 149 du run "
                      "r1 ; il faut le run composition"),
        })
    d = pd.DataFrame(lignes)
    rejets = pd.DataFrame([{"item_as": "", "groupe": "rejets et anomalies", "parti_as": "",
                            "terme_realite": "", "terme_humain": "",
                            "terme_modele_via_r1": np.nan,
                            "terme_modele_via_run_composition": np.nan,
                            "modeles_couverts": "",
                            "comparaison_a_trois_termes_possible": False,
                            "ce_qui_manque": m} for m in sorted(set(manquants))])
    return pd.concat([d, rejets], ignore_index=True) if len(rejets) else d


def main():
    rng = np.random.default_rng(C.GRAINE)

    for nom in ("a46-ahler-sood-items.csv", "a46-appariement.csv",
                "a46-composition-gss-2024.csv"):
        if not os.path.exists(os.path.join(C.SORTIE, nom)):
            sys.exit(f"{nom} absent. Lancer d'abord a46_ahler_sood.py puis "
                     f"a46_appariement.py")
    humain = pd.read_csv(os.path.join(C.SORTIE, "a46-ahler-sood-items.csv"))
    appar = pd.read_csv(os.path.join(C.SORTIE, "a46-appariement.csv"))
    comp = pd.read_csv(os.path.join(C.SORTIE, "a46-composition-gss-2024.csv"))

    modele_r1, manquants = termes_modele_depuis_r1()
    modele_comp = termes_modele_depuis_composition()
    modele = pd.concat([m for m in (modele_r1, modele_comp) if not m.empty],
                       ignore_index=True) if (not modele_r1.empty
                                              or not modele_comp.empty) else pd.DataFrame()

    trois = assembler(modele, humain, appar, comp)
    tst = tests(trois, rng)
    cov = couverture(trois, modele_r1, modele_comp, manquants)

    print(C.ecrire(trois, "a46-trois-termes.csv"), len(trois), "lignes")
    print(C.ecrire(tst, "a46-trois-termes-tests.csv"), len(tst), "lignes")
    print(C.ecrire(cov, "a46-couverture.csv"), len(cov), "lignes")

    if trois.empty:
        print("\nAucun terme de modele disponible. Le tableau des trois termes est vide, "
              "ce qui est le comportement attendu tant que le run r1 n'a pas atteint "
              "union1 et reborn et que le run composition n'a pas eu lieu.")
        return
    print("\ntrois termes, cellules disponibles :")
    for _, r in trois.iterrows():
        print(f"  {r['item_as']:10s} {r['cle_modele']:6s} {r['ancrage']:10s} "
              f"{r['camp']:7s} {r['identite']:11s} "
              f"reel GSS {r['realite_gss2024']:5.1f} %  "
              f"humain {r['croyance_humaine']:5.1f} %  "
              f"modele {r['croyance_modele']:5.1f} %  "
              f"exag. modele {r['exageration_modele_ratio_base_propre']:5.2f} contre "
              f"humaine {r['exageration_humaine_ratio_base_propre']:5.2f}  "
              f"rapport {r['rapport_des_exagerations_base_propre']:5.2f}")
    if not tst.empty:
        print("\ntests :")
        for _, r in tst.iterrows():
            print(f"  {r['famille']:46s} camp {r['camp']:7s} n={r['n_items']} "
                  f"rapport {r['rapport_des_moyennes']:5.2f} "
                  f"[{r['rapport_ic_bas']:.2f} ; {r['rapport_ic_haut']:.2f}] "
                  f"p_holm {r['p_holm']:.3f}  {r['verdict']}")


if __name__ == "__main__":
    main()
