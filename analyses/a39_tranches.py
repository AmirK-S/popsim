"""
a39_tranches : la mesure de queue de Peng et al., rejouee sur nos donnees.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a2_baselines_gss, a5_evaluer,
a5_agents_locaux_gss, a25_commun, a25_mesures et a28_commun sont importes tels quels,
memes graines, memes plis, memes 149 items, memes personnes. La foret aleatoire
`B3 foret` est relue du cache de a28, elle n'est pas redefinie.

Ce que fait ce script : pour chaque methode et pour chaque tranche de la vraie valeur
humaine, il calcule l'exactitude et son intervalle, il classe les methodes par tranche, il
teste quatre familles de contrastes declarees ci dessous, et il ajoute leur rapport
d'ecarts types par resultat sur les items ordinaux.

===============================================================================
LE PROTOCOLE, ECRIT AVANT LES RESULTATS
===============================================================================

**Perimetre declare** : le perimetre naturel de chaque methode, soit les 1 052 personnes
pour les onze methodes qui les couvrent, et les 150 personnes du run local pour C2 et C3.
Sur le perimetre 150, la reference de rarete et le tri des tranches sont recalcules sur
ces 150 personnes, comme en a28 et a29.

**Deux definitions de tranche**, toutes deux fondees sur la vraie reponse humaine de la
vague 1 et donc identiques cellule par cellule pour les quatorze conditions.

  - **rarete**, sur les 149 items, seule transposition possible du tri de Peng et al. a
    une reponse nominale : bas = la vraie modalite est donnee par moins de 5 pour cent des
    repondants de l'item ; haut = la vraie modalite est la modalite majoritaire et cette
    modalite depasse 95 pour cent des repondants ; milieu = le reste. L'exactitude est la
    concordance exacte.
  - **ordinale**, sur les items ordinaux de a25, qui est leur definition mot pour mot :
    les repondants sont tries par leur vraie valeur, les 5 pour cent du bas et les 5 pour
    cent du haut sont pris par rang, le reste est le milieu. L'exactitude est la leur,
    `1 - |predit - vrai| / etendue`, les valeurs etant les rangs normalises dans [0, 1].

**Un temoin de plus que a28 et a29, et il est indispensable.** Leur `random_benchmark`
est un tirage UNIFORME sur l'etendue du resultat. Notre `B0 tirage` est un tirage dans la
MARGINALE observee de l'item : il connait la distribution de la population et se concentre
donc sur la modalite majoritaire. Les deux ne sont pas la meme chose, et la ligne de leur
tableau qui dit que le hasard bat l'etiquette sur les 5 pour cent du bas n'a d'equivalent
chez nous que contre un tirage uniforme. Ce script ajoute donc `B0 uniforme`, qui tire
uniformement parmi les modalites declarees de l'item, et le declare comme quatorzieme
methode non humaine. Il est defini dans a39_commun, aucun script existant n'est touche.
[Ajout signale : il a ete introduit apres un premier passage a 300 tirages qui a montre
que `B0 tirage` n'etait pas leur temoin. La structure des familles ci dessous n'a pas
change, seul le nombre de methodes est passe de 13 a 14.]

**Famille primaire declaree, 52 tests.** Pour chacune des 13 methodes non humaines autres
que le temoin lui meme, pour chacune des deux definitions, et pour chacune des deux
tranches qui portent la these, bas et milieu : la difference d'exactitude entre la methode
et `B0 uniforme`, sur la meme tranche et la meme definition, differe de zero. Bilateral.
13 x 2 x 2 = 52.
Prediction de la these et de leur depot : sur le milieu, toutes les conditions a modele de
langage sont nettement au dessus du tirage ; sur le bas, l'ecart se resserre voire
s'inverse pour les conditions a etiquette seule.

**Famille secondaire declaree, 56 tests.** Les memes 56 contrastes, contre
`humains vague 2`, c'est a dire contre le plancher de bruit que donnent les memes humains
reinterroges deux semaines plus tard.

**Famille « replique Peng » declaree, 16 tests, corrigee separement.** Les quatre
comparaisons de leur tableau, rejouees sur deux definitions de tranche :
  (a) etiquette seule contre condition riche, tranche milieu ;
  (b) etiquette seule contre condition riche, tranche bas ;
  (c) etiquette seule contre tirage uniforme, tranche bas ;
  (d) condition riche contre tirage uniforme, tranche bas.
Le couple etiquette contre riche vaut `agents v8` contre `agents composite` sur les
1 052 personnes, et `C2` contre `C3` sur les 150. 4 x 2 definitions x 2 couples = 16.
Prediction : (a) nulle, (b) negative, (c) negative, (d) positive.

**Famille « dispersion » declaree, 14 tests, corrigee separement.** Pour chacune des 14
methodes non humaines, le rapport d'ecarts types moyen sur les items ordinaux differe de
celui de `humains vague 2`.

Les quatre familles sont corrigees **separement** par **Holm**, valide sans hypothese sur
la dependance, ce qui est necessaire puisque les contrastes portent sur les memes
personnes et les memes items. **Benjamini Hochberg** est rapporte a cote. Tous les p sont
des p de bootstrap apparie sur les personnes, 4 000 tirages, lus sur la position de zero
dans la distribution ; ils ne descendent jamais sous 1 / 4 000 = 0,00025.

**N'entrent dans aucune famille**, et sont des descriptions : la tranche haute, qui ne
porte presque aucune cellule sur le GSS ; la variante « extremes de l'echelle », qui
remplace le tri par rang par l'appartenance au bout de l'echelle ; le perimetre 150 pour
les onze methodes qui disposent du 1 052, echantillon emboite ; le classement par
tranche ; le detail par item ; la comparaison chiffre a chiffre avec leurs valeurs
publiees, qui porte sur un autre jeu, un autre modele et une autre mesure d'exactitude ;
l'echelle de dispersion « vide, etiquette, persona complete », qui est une lecture d'ordre
et non un test ; et la decomposition du rapport d'ecarts types en un terme inter segments
et un terme intra segment sur l'axe ideologique, qui est ajoutee pour montrer ce que leur
rapport total confond, avec des intervalles bootstrap sur 1 000 tirages et aucun test.

Entree  : /tmp/a25-matrices.pkl, /tmp/a28-foret.npy, data/osf-t6g7k-stanford,
          data/traces. Non versionnes.
Sortie  : resultats/a39-tranches.csv, a39-classement.csv, a39-contrastes.csv,
          a39-ecarts-types.csv, a39-ecarts-types-items.csv,
          a39-ecarts-types-decomposition.csv, a39-definition-tranches.csv,
          a39-comparaison-peng.csv

Usage :
  .venv/bin/python analyses/a39_tranches.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 4000
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a39_commun as A
import a28_commun as C28
from a2_commun import est_manquant

PAIRES_PENG = [
    # (perimetre, etiquette seule, condition riche)
    ("1052", "agents v8", "agents composite"),
    ("150", "C2", "C3"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=4000)
    ap.add_argument("--graine", type=int, default=A.GRAINE)
    args = ap.parse_args()

    rng = np.random.default_rng(args.graine)
    paquet = A.charger(args.cache, args.cache_foret)
    items, y1, M, options = (paquet["items"], paquet["y1"], paquet["M"],
                             paquet["options"])
    per = A.perimetres(paquet)

    M[A.UNIFORME] = A.baseline_uniforme(items, options, len(paquet["ids"]),
                                        graine=args.graine)

    ord_items = A.items_ordinaux(items, options)
    col_ord = [items.index(it) for it in ord_items]
    rangs = A.table_de_rang(items, options)
    print(f"{len(paquet['ids'])} personnes, {len(items)} items, "
          f"{len(ord_items)} items ordinaux, {len(per['150'])} personnes du run local",
          flush=True)

    ok_total = A.observe(y1)
    scores_vrais_ord_total = A.matrice_scores(y1, col_ord, items, rangs)

    # -----------------------------------------------------------------------
    # 1. Les tranches, une construction par perimetre et par definition
    # -----------------------------------------------------------------------
    contexte = {}
    lignes_def = []
    for nom_per, lignes in per.items():
        y = y1[lignes]
        tr_rar, detail_rar = A.tranches_rarete(y)
        sv = scores_vrais_ord_total[lignes]
        tr_ord, detail_ord = A.tranches_ordinales(sv, graine=args.graine)
        tr_ext = A.tranches_extremes_echelle(sv)
        contexte[nom_per] = {
            "lignes": lignes, "y": y, "ok": ok_total[lignes],
            "sv": sv, "tr": {"rarete": tr_rar, "ordinale": tr_ord,
                             "ordinale extremes": tr_ext},
        }
        n_haut_items = int((detail_rar["part_modale"] > A.SEUIL_HAUT).sum())
        for nom_d, tr in contexte[nom_per]["tr"].items():
            n_items_d = len(items) if nom_d == "rarete" else len(ord_items)
            for k, nom_t in enumerate(A.TRANCHES):
                lignes_def.append({
                    "perimetre": nom_per, "definition": nom_d, "tranche": nom_t,
                    "n_cellules": int((tr == k).sum()),
                    "part_des_cellules": float((tr == k).sum() / max((tr >= 0).sum(), 1)),
                    "n_items": n_items_d,
                    "items_a_modale_sup_95": n_haut_items if nom_d == "rarete" else -1,
                })
    definition = pd.DataFrame(lignes_def)
    A.ecrire(definition, "a39-definition-tranches.csv")

    # -----------------------------------------------------------------------
    # 2. Exactitude par tranche, avec bootstrap sur les personnes
    # -----------------------------------------------------------------------
    idx_boot = {nom: A.tirages_bootstrap(len(l), args.tirages, rng)
                for nom, l in per.items()}

    # comptes[(perimetre, definition, condition)][tranche] = (num, den)
    comptes, tirages, valeurs = {}, {}, {}
    lignes_table = []
    for nom_per, lignes in per.items():
        ctx = contexte[nom_per]
        conds = A.methodes_du_perimetre(paquet, nom_per)
        # le denominateur ne depend que de la tranche : la tranche est definie par la
        # verite humaine et le masque d'evaluation aussi
        den_boot = {}
        for nom_d, tr in ctx["tr"].items():
            for k, nom_t in enumerate(A.TRANCHES + ["ensemble"]):
                masque = (tr == k) if nom_t != "ensemble" else (tr >= 0)
                den = masque.sum(axis=1).astype(float)
                den_boot[(nom_d, nom_t)] = (den,
                                            den[idx_boot[nom_per]].sum(axis=1))
        for cond in conds:
            mat = M[cond][lignes]
            n_refus = int(sum(1 for l in mat for v in l if v is None or est_manquant(v)))
            sc_rar = A.scores_exactitude_categorielle(mat, ctx["y"], ctx["ok"])
            sp = A.matrice_scores(M[cond], col_ord, items, rangs)[lignes]
            sc_ord = A.scores_exactitude_ordinale(sp, ctx["sv"])
            paquets_scores = {"rarete": sc_rar, "ordinale": sc_ord,
                              "ordinale extremes": sc_ord}
            for nom_d, tr in ctx["tr"].items():
                sc = paquets_scores[nom_d]
                for k, nom_t in enumerate(A.TRANCHES + ["ensemble"]):
                    masque = (tr == k) if nom_t != "ensemble" else (tr >= 0)
                    num = np.where(masque, np.nan_to_num(sc), 0.0).sum(axis=1)
                    den, db = den_boot[(nom_d, nom_t)]
                    d = den.sum()
                    val = float(num.sum() / d) if d > 0 else np.nan
                    with np.errstate(invalid="ignore", divide="ignore"):
                        tb = np.where(db > 0,
                                      num[idx_boot[nom_per]].sum(axis=1)
                                      / np.maximum(db, 1e-12), np.nan)
                    cle = (nom_per, nom_d, cond, nom_t)
                    valeurs[cle] = val
                    tirages[cle] = tb
                    comptes[cle] = (num, den)
                    lo, hi = A.ic(tb)
                    lignes_table.append({
                        "perimetre": nom_per, "definition": nom_d, "condition": cond,
                        "famille_condition": A.FAMILLE_CONDITION.get(cond, ""),
                        "tranche": nom_t, "exactitude": val, "ic_bas": lo,
                        "ic_haut": hi, "n_cellules": int(d),
                        "n_personnes": int(len(lignes)),
                        "taux_refus": n_refus / max(int(ctx["ok"].sum()), 1),
                    })
            print(f"  {nom_per} : {cond} termine", flush=True)
    table = pd.DataFrame(lignes_table)
    A.ecrire(table, "a39-tranches.csv")

    # -- controle de protocole, execute avant toute lecture ------------------
    # La colonne "ensemble" de la definition rarete est, par construction, l'exactitude
    # globale par cellule sur les 149 items. Elle doit reproduire au chiffre pres les
    # valeurs publiees par a2 dans resultats/a2_gss_resultats.json. Si elle ne les
    # reproduit pas, la chaine a bouge et rien de ce qui suit n'est lisible.
    reference_a2 = {
        "agents composite": 0.683932, "agents entretien (v3)": 0.656493,
        "agents enquete": 0.650988, "agents demographiques (v6)": 0.581787,
        "B0 mode": 0.593386, "B0 tirage": 0.491828, "B1 argmax": 0.620856,
        "B2 argmax": 0.671709, "humains vague 2": 0.795002,
    }
    print("\n--- controle de protocole : exactitude globale contre a2 ---")
    ecart_max = 0.0
    for cond, attendu in reference_a2.items():
        obtenu = valeurs[("1052", "rarete", cond, "ensemble")]
        ecart_max = max(ecart_max, abs(obtenu - attendu))
        print(f"  {cond:<28} {obtenu:.6f} contre {attendu:.6f}  "
              f"ecart {obtenu - attendu:+.6f}")
    print(f"  ecart maximal {ecart_max:.6f}")
    assert ecart_max < 1e-4, "la chaine a bouge, les chiffres de a2 ne se reproduisent pas"

    # -----------------------------------------------------------------------
    # 3. Classement par tranche
    # -----------------------------------------------------------------------
    cl = []
    for (nom_per, nom_d, nom_t), g in table.groupby(["perimetre", "definition",
                                                     "tranche"]):
        g = g.sort_values("exactitude", ascending=False).reset_index(drop=True)
        for r, row in g.iterrows():
            cl.append({"perimetre": nom_per, "definition": nom_d, "tranche": nom_t,
                       "rang": r + 1, "condition": row.condition,
                       "exactitude": row.exactitude})
    A.ecrire(pd.DataFrame(cl), "a39-classement.csv")

    # -----------------------------------------------------------------------
    # 4. Les quatre familles de contrastes
    # -----------------------------------------------------------------------
    def contraste(cle_a, cle_b):
        ta, tb = tirages[cle_a], tirages[cle_b]
        d = ta - tb
        obs = valeurs[cle_a] - valeurs[cle_b]
        lo, hi = A.ic(d)
        return obs, lo, hi, A.p_bilateral(d)

    familles = {}

    # -- famille primaire et famille secondaire ------------------------------
    for nom_famille, reference in (("primaire, contre B0 uniforme", A.UNIFORME),
                                   ("secondaire, contre humains vague 2",
                                    "humains vague 2")):
        lignes_f = []
        for nom_per in ("1052", "150"):
            conds = [c for c in A.methodes_du_perimetre(paquet, nom_per)
                     if c != "humains vague 2"]
            if nom_per == "1052":
                conds = [c for c in conds if c not in ("C2", "C3")]
            else:
                conds = ["C2", "C3"]
            for nom_d in ("rarete", "ordinale"):
                for nom_t in ("bas", "milieu"):
                    for cond in conds:
                        if cond == reference:
                            continue
                        o, lo, hi, p = contraste((nom_per, nom_d, cond, nom_t),
                                                 (nom_per, nom_d, reference, nom_t))
                        lignes_f.append({
                            "famille": nom_famille, "perimetre": nom_per,
                            "definition": nom_d, "tranche": nom_t, "A": cond,
                            "B": reference, "difference": o, "ic_bas": lo,
                            "ic_haut": hi, "p_brut": p})
        familles[nom_famille] = pd.DataFrame(lignes_f)

    # -- famille replique Peng ----------------------------------------------
    lignes_f = []
    for nom_per, etiquette, riche in PAIRES_PENG:
        for nom_d in ("rarete", "ordinale"):
            for libelle, a, b, t in (
                    ("a. etiquette contre riche, milieu", etiquette, riche, "milieu"),
                    ("b. etiquette contre riche, bas", etiquette, riche, "bas"),
                    ("c. etiquette contre uniforme, bas", etiquette, A.UNIFORME, "bas"),
                    ("d. riche contre uniforme, bas", riche, A.UNIFORME, "bas")):
                o, lo, hi, p = contraste((nom_per, nom_d, a, t),
                                         (nom_per, nom_d, b, t))
                lignes_f.append({"famille": "replique Peng", "perimetre": nom_per,
                                 "definition": nom_d, "tranche": t, "A": a, "B": b,
                                 "contraste": libelle, "difference": o, "ic_bas": lo,
                                 "ic_haut": hi, "p_brut": p})
    familles["replique Peng"] = pd.DataFrame(lignes_f)

    # -----------------------------------------------------------------------
    # 5. Rapport d'ecarts types par resultat, sur les items ordinaux
    # -----------------------------------------------------------------------
    lignes_sd, lignes_sd_items, tir_sd = [], [], {}
    for nom_per, lignes in per.items():
        ctx = contexte[nom_per]
        for cond in A.methodes_du_perimetre(paquet, nom_per):
            sp = A.matrice_scores(M[cond], col_ord, items, rangs)
            d = A.rapport_ecarts_types(sp, scores_vrais_ord_total, lignes)
            d.insert(0, "item", ord_items)
            d.insert(0, "condition", cond)
            d.insert(0, "perimetre", nom_per)
            lignes_sd_items.append(d)
            tb = A.bootstrap_moyenne_ratio(sp, scores_vrais_ord_total, lignes,
                                           idx_boot[nom_per])
            tir_sd[(nom_per, cond)] = tb
            lo, hi = A.ic(tb)
            r = d["ratio"].to_numpy()
            lignes_sd.append({
                "perimetre": nom_per, "condition": cond,
                "famille_condition": A.FAMILLE_CONDITION.get(cond, ""),
                "ratio_moyen": float(np.nanmean(r)),
                "ic_bas": lo, "ic_haut": hi,
                "ratio_median": float(np.nanmedian(r)),
                "items_sous_1": int(np.nansum(r < 1.0)),
                "n_items": int(np.isfinite(r).sum()),
            })
            print(f"  ecarts types {nom_per} : {cond} termine", flush=True)
    A.ecrire(pd.DataFrame(lignes_sd), "a39-ecarts-types.csv")

    # -- decomposition du rapport, hors famille, descriptive -----------------
    # Leur rapport est TOTAL, il melange en un seul nombre ce que a1 separe en un terme
    # inter segments et un terme intra segment. La decomposition est ajoutee ici pour que
    # l'echelle "la dispersion croit avec l'information" soit lisible des deux cotes.
    seg, niveaux = C28.segments(paquet["x"], paquet["attributs"])
    axe = "political_ideology"
    idx_dec = idx_boot["1052"][:1000]
    lignes_dec = []
    for cond in A.methodes_du_perimetre(paquet, "1052"):
        sp = A.matrice_scores(M[cond], col_ord, items, rangs)
        res, _ = A.decomposition_dispersion(sp, scores_vrais_ord_total, seg[axe],
                                            per["1052"], len(niveaux[axe]),
                                            idx_boot=idx_dec)
        ligne = {"perimetre": "1052", "condition": cond,
                 "famille_condition": A.FAMILLE_CONDITION.get(cond, "")}
        for nom in ("total", "inter", "intra"):
            ligne[f"ratio_{nom}"] = res[nom]["moyenne"]
            ligne[f"ratio_{nom}_ic_bas"] = res[nom].get("ic_bas", np.nan)
            ligne[f"ratio_{nom}_ic_haut"] = res[nom].get("ic_haut", np.nan)
            ligne[f"ratio_{nom}_median"] = res[nom]["mediane"]
        lignes_dec.append(ligne)
        print(f"  decomposition 1052 : {cond} termine", flush=True)
    for cond in ("C2", "C3", "humains vague 2"):
        sp = A.matrice_scores(M[cond], col_ord, items, rangs)
        res, _ = A.decomposition_dispersion(sp, scores_vrais_ord_total, seg[axe],
                                            per["150"], len(niveaux[axe]),
                                            idx_boot=idx_boot["150"][:1000])
        ligne = {"perimetre": "150", "condition": cond,
                 "famille_condition": A.FAMILLE_CONDITION.get(cond, "")}
        for nom in ("total", "inter", "intra"):
            ligne[f"ratio_{nom}"] = res[nom]["moyenne"]
            ligne[f"ratio_{nom}_ic_bas"] = res[nom].get("ic_bas", np.nan)
            ligne[f"ratio_{nom}_ic_haut"] = res[nom].get("ic_haut", np.nan)
            ligne[f"ratio_{nom}_median"] = res[nom]["mediane"]
        lignes_dec.append(ligne)
        print(f"  decomposition 150 : {cond} termine", flush=True)
    decomposition = pd.DataFrame(lignes_dec)
    A.ecrire(decomposition, "a39-ecarts-types-decomposition.csv")
    A.ecrire(pd.concat(lignes_sd_items, ignore_index=True),
             "a39-ecarts-types-items.csv")

    lignes_f = []
    for nom_per in ("1052", "150"):
        conds = [c for c in A.methodes_du_perimetre(paquet, nom_per)
                 if c != "humains vague 2"]
        conds = ([c for c in conds if c not in ("C2", "C3")] if nom_per == "1052"
                 else ["C2", "C3"])
        for cond in conds:
            d = tir_sd[(nom_per, cond)] - tir_sd[(nom_per, "humains vague 2")]
            obs = (float(np.nanmean(tir_sd[(nom_per, cond)]))
                   - float(np.nanmean(tir_sd[(nom_per, "humains vague 2")])))
            lo, hi = A.ic(d)
            lignes_f.append({"famille": "dispersion", "perimetre": nom_per,
                             "definition": "ordinale", "tranche": "sans objet",
                             "A": cond, "B": "humains vague 2", "difference": obs,
                             "ic_bas": lo, "ic_haut": hi, "p_brut": A.p_bilateral(d)})
    familles["dispersion"] = pd.DataFrame(lignes_f)

    # -----------------------------------------------------------------------
    # 6. Corrections, chaque famille separement
    # -----------------------------------------------------------------------
    sorties = []
    for nom_famille, d in familles.items():
        d = d.copy()
        d["p_holm"] = A.holm(d["p_brut"].to_numpy())
        d["p_bh"] = A.benjamini_hochberg(d["p_brut"].to_numpy())
        d["n_tests_famille"] = len(d)
        sorties.append(d)
        print(f"\nfamille « {nom_famille} » : {len(d)} tests, "
              f"{int((d['p_holm'] < 0.05).sum())} passent Holm a 0,05")
    contrastes = pd.concat(sorties, ignore_index=True)
    A.ecrire(contrastes, "a39-contrastes.csv")

    # -----------------------------------------------------------------------
    # 7. Comparaison chiffre a chiffre avec leurs valeurs publiees
    # -----------------------------------------------------------------------
    corres = [
        ("full_persona_without_reasoning", "agents composite", "1052",
         "condition riche la plus forte de Stanford"),
        ("full_persona_without_reasoning", "C3", "150",
         "notre condition sans etiquette, meme modele que C2"),
        ("demographics_only", "agents v8", "1052",
         "etiquette ideologie, parti, race, genre"),
        ("demographics_only", "agents demographiques (v6)", "1052",
         "etiquette demographique sans ideologie"),
        ("demographics_only", "C2", "150", "onze attributs demographiques"),
        ("random_benchmark", A.UNIFORME, "1052",
         "tirage uniforme sur la nomenclature, le seul temoin comparable au leur"),
        ("random_benchmark", "B0 tirage", "1052",
         "tirage dans la marginale observee, temoin plus fort que le leur"),
    ]
    lignes_c = []
    for spec, cond, nom_per, note in corres:
        for nom_d in ("rarete", "ordinale"):
            for nom_t in A.TRANCHES:
                cle = (nom_per, nom_d, cond, nom_t)
                if cle not in valeurs:
                    continue
                lignes_c.append({
                    "specification_peng": spec, "valeur_peng": A.PENG_TRANCHES[spec][nom_t],
                    "notre_condition": cond, "perimetre": nom_per,
                    "definition": nom_d, "tranche": nom_t,
                    "notre_valeur": valeurs[cle], "correspondance": note})
    A.ecrire(pd.DataFrame(lignes_c), "a39-comparaison-peng.csv")

    # -----------------------------------------------------------------------
    # 8. Sortie lisible
    # -----------------------------------------------------------------------
    for nom_d in ("rarete", "ordinale", "ordinale extremes"):
        for nom_per in ("1052", "150"):
            print("\n" + "=" * 92)
            print(f"EXACTITUDE PAR TRANCHE, definition {nom_d}, perimetre {nom_per}")
            print("=" * 92)
            g = table[(table.definition == nom_d) & (table.perimetre == nom_per)]
            piv = g.pivot(index="condition", columns="tranche", values="exactitude")
            piv = piv.reindex([c for c in A.ORDRE_METHODES if c in piv.index])
            print(piv[["bas", "milieu", "haut", "ensemble"]].to_string(
                float_format=lambda v: f"{v:.4f}"))

    print("\n" + "=" * 92)
    print("RAPPORT D'ECARTS TYPES PAR RESULTAT, items ordinaux")
    print("=" * 92)
    sd = pd.DataFrame(lignes_sd)
    print(sd.to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    print("\n" + "=" * 92)
    print("DECOMPOSITION DU RAPPORT, axe ideologie, hors famille")
    print("=" * 92)
    print(decomposition[["perimetre", "condition", "famille_condition", "ratio_total",
                         "ratio_inter", "ratio_intra"]].to_string(
        index=False, float_format=lambda v: f"{v:.4f}"))

    print("\n" + "=" * 92)
    print("CONTRASTES QUI PASSENT HOLM A 0,05")
    print("=" * 92)
    q = contrastes[contrastes.p_holm < 0.05]
    print(q.to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
