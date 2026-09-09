"""
a41_regime_severe : le regime severe, mesure avec des intervalles et une correction.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a2_baselines_gss, a8_commun,
a28_commun, a29_commun, a31_commun, a33_commun, a34_commun, a35_commun et a35_familles
sont importes tels quels, memes graines, memes plis, memes 149 items, memes personnes,
memes 58 items de famille, memes 60 personnes de la trace C3F.

La question, posee par a35 section 11 point 1 et par a35 question 3 pour Simon : le regime
severe "porte maintenant l'essentiel de la these et il est le moins bien mesure du
rapport". Ses chiffres sont des estimations ponctuelles, sans bootstrap et sans
correction. L'ecart de 1,3 point entre `agents composite` et `E1 famille retiree` n'est
pas teste. a41 le teste, et il pose en meme temps la question que a8 errata E1 rend
inevitable : la comparaison n'est pas appariee, puisque les agents de Stanford gardent
les items cousins dans leur invite.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT L'EXECUTION
===========================================================================

CE RAPPORT NE REVENDIQUE PAS LE PRE ENREGISTREMENT, ET C'EST LE PREMIER CHIFFRE
DESAGREABLE. Les estimations ponctuelles du regime severe ont deja ete lues : elles sont
publiees dans a35 section 6 et dans a8 section 3.2, et elles ont oriente le choix des
contrastes ci dessous. `agents composite` a 0,6775, `agents enquete` a 0,6711,
`E1 famille retiree` a 0,6649, `B2 famille retiree` a 0,6621 sont connus. Les p qui
suivent sont des p de CONFIRMATION FAIBLE : ils disent si un ecart deja vu survit a un
reechantillonnage des personnes, ils ne disent pas qu'une hypothese aveugle a ete
soumise a l'epreuve. Le fait est repete dans le rapport et aucune formulation ne doit
laisser croire l'inverse.

PERIMETRE DECLARE : les 1 052 personnes de a2 et les 58 items des six familles
thematiques de a2_baselines_gss. Regime severe = protocole de a8 section 3.1 : la famille
thematique entiere sort du contexte du predicteur ET sert de cible. Les six conditions de
Stanford ne sont PAS replacees dans ce regime, elles ne peuvent pas l'etre sans relancer
leurs agents, et elles gardent donc les items cousins dans leur invite. Ce defaut
d'appariement est la raison d'etre des sections de comparaison honnete ; il est signale
sur chaque ligne de chaque tableau par la colonne "famille retiree".

MESURE DE DISPERSION DECLAREE : indice de Gini Simpson, estimateur sans biais de a1, tel
que a28_commun.dispersion_item le calcule. Segmentation : l'ideologie politique.
SEUIL DE MINORITE DECLARE : 10 pour cent, reference calculee sur les 1 052 personnes.
PARTITION DE DEDUCTIBILITE DECLAREE : D_seg de a34, terciles dont les bornes sont
recalculees sur les cellules minoritaires des 58 items.

CRITERE DE STRUCTURE DECLARE : l'ecart ABSOLU a 1 du ratio intra, et non le ratio lui
meme. Un ratio de 1 veut dire que la methode laisse les gens d'un meme segment aussi
differents qu'ils le sont vraiment ; 1,05 n'est pas meilleur que 0,95. Le choix est ecrit
ici parce qu'il change le sens de plusieurs contrastes.

  | | enonce | nombre de tests |
  |---|---|---|
  | F1 primaire | pour chacune des 9 methodes statistiques du regime severe, le contraste `agents composite` moins la methode, sur 3 quantites : exactitude, ecart absolu a 1 du ratio intra, rappel des cellules minoritaires ; bilateral | 27 |
  | F2 secondaire | (a) `agents composite` et `agents enquete` contre `E1 famille retiree`, sur 4 quantites : exactitude, diversite conservee, ratio intra, ratio inter ; (b) les memes deux conditions APPARIEES au sens de a8 errata E1, contre `E1 famille retiree` et contre `B2 famille retiree (argmax)`, sur l'exactitude seule | 8 + 4 = 12 |
  | F3 tertiaire | sur les 60 personnes et les 58 items de la trace C3F, C3F contre chacune des 6 methodes statistiques du regime severe, sur l'exactitude ; bilateral | 6 |

SIGNES ATTENDUS, ECRITS AVANT EXECUTION. Pour F1 : positif sur l'exactitude et sur le
rappel minoritaire, negatif sur l'ecart absolu a 1 du ratio intra, c'est a dire l'agent
plus proche de 1 que la methode statistique. Un signe inverse est un resultat contre la
prediction et il est signale comme tel. Pour F2 (a) : positif sur l'exactitude et la
diversite conservee, positif sur le ratio intra, positif sur le ratio inter, ce dernier
etant un DEFAUT de l'agent et non un avantage. Pour F2 (b) : le signe est inconnu, c'est
tout l'objet du test. Pour F3 : negatif, a33 ayant deja mesure que notre agent local de
4 milliards de parametres perd contre `B2 famille retiree` de 12,5 points sur ce
perimetre.

CORRECTION : Holm sur chaque famille separement, valide sans hypothese sur la dependance,
ce qui est necessaire puisque tous les contrastes portent sur les memes personnes et les
memes items. Benjamini Hochberg est rapporte a cote. Tous les p sont des p de bootstrap
APPARIE SUR LES PERSONNES, lus sur la position de zero dans la distribution ; ils ne
descendent jamais sous 1 divise par le nombre de tirages. Avec 2 000 tirages sur les
1 052 personnes le plancher vaut 0,0005, soit 0,0135 apres Holm sur 27 tests ; avec
4 000 tirages sur les 60 personnes de C3F il vaut 0,00025, soit 0,0015 apres Holm sur 6.

N'ENTRENT DANS AUCUNE FAMILLE, et sont rapportes comme des descriptions : le tableau a
quatre cases lui meme, ligne par ligne ; le ratio de dispersion totale ; l'accord par
paires ; la precision minoritaire ; le rappel du tercile T1 non deductible, dont le
denominateur est trop petit sur 58 items pour porter un test declare, et qui est publie
avec son intervalle ; les lignes du regime facile, qui servent a lire ce que le retrait de
la famille coute ; les cinq conditions de Stanford autres que `agents composite` dans F1 ;
la sensibilite de la condition appariee a l'ampleur du decalage ; le decalage d'exactitude
qui rendrait la comparaison indecidable ; et les quantites de structure sur les 60
personnes de C3F, dont a33 section 4 a etabli qu'elles ne sont pas identifiables sur ce
perimetre.

CE QUE CE PROTOCOLE NE PEUT PAS FAIRE, ecrit ici et non a la fin : il ne peut pas replacer
les agents de Stanford dans le regime severe. La condition appariee de F2 (b) est une
TRANSPOSITION d'un chiffre publie par le papier sur un autre perimetre, pas une mesure.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, cache de matrices de a25, cache de la
          foret de a28, cache des methodes de a35.
Sortie  : resultats/a41-controles.csv, a41-tableau-quatre-cases.csv, a41-contrastes-f1.csv,
          a41-contrastes-f2.csv, a41-c3f-60-personnes.csv, a41-terciles.csv,
          a41-condition-appariee.csv, a41-verification-mesures.csv, a41-cout-du-retrait.csv.

Usage :
  .venv/bin/python analyses/a41_regime_severe.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl \
      --cache-a41 /tmp/a41-severe.pkl --tirages 2000 --tirages-c3f 4000
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a29_commun as C29
import a33_commun as C33
import a41_commun as C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--cache-a41", default="/tmp/a41-severe.pkl")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--tirages-c3f", type=int, default=4000)
    ap.add_argument("--graine", type=int, default=C.GRAINE_A41)
    args = ap.parse_args()

    t_debut = time.time()
    print(__doc__.split("=" * 75)[1])

    controles = []

    # ------------------------------------------------------------------ 1. chargement
    paquet = C.charger_paquet(args.cache, args.cache_foret, args.cache_a35)
    C.construire_severe(paquet, cache=args.cache_a41)
    y1, items, options = paquet["y1"], paquet["items"], paquet["options"]
    n, m = y1.shape
    cols, familles = C.colonnes_familles(items)
    print(f"\n{len(familles)} familles thematiques, {len(cols)} items, {n} personnes")

    lignes = np.arange(n)
    seg_tous, _ = C28.segments(paquet["x"], paquet["attributs"])
    seg = seg_tous[C.AXE_PRINCIPAL]
    k_items = [len(options[it]) for it in items]
    k_max_nom = max(k_items)

    methodes = C.methodes_disponibles(paquet, avec_facile=True, avec_locales=False)
    print(f"{len(methodes)} conditions sur le perimetre 1 052")

    # ------------------------------------------------- 2. controles avant toute lecture
    print("\ncontroles de protocole, avant toute lecture")
    for nom, cible in (("B2 famille retiree (argmax)", 0.662105),
                       ("agents composite", 0.677527),
                       ("agents enquete", 0.671103),
                       ("agents entretien (v3)", 0.633572),
                       ("B2 argmax", 0.695572),
                       ("B0 mode", 0.616379),
                       ("humains vague 2", 0.785597)):
        v = float(np.nanmean(C.exactitude(paquet["M"][nom], y1, lignes, cols)))
        controles.append({"controle": f"exactitude {nom} sur les 58 items",
                          "valeur": v, "reference": cible,
                          "source": "a8-familles-gss.csv",
                          "ecart": abs(v - cible)})
        print(f"  {nom:<32} {v:.6f} contre {cible:.6f}")
    for nom, cible in (("E1 famille retiree (argmax)", 0.6649),
                       ("IM m=10 mode, famille retiree", 0.6501),
                       ("PMM k=10 famille retiree", 0.6280),
                       ("E2 famille retiree (tirage)", 0.5937),
                       ("E1 regression contexte argmax", 0.7304),
                       ("PMM k=10", 0.6942)):
        v = float(np.nanmean(C.exactitude(paquet["M"][nom], y1, lignes, cols)))
        controles.append({"controle": f"exactitude {nom} sur les 58 items",
                          "valeur": v, "reference": cible,
                          "source": "a35-familles-regime-severe.csv",
                          "ecart": abs(v - cible)})
        print(f"  {nom:<32} {v:.6f} contre {cible:.4f}")
    v = float(np.nanmean(C.exactitude(paquet["M"]["B2 famille retiree (tirage)"],
                                      y1, lignes, cols)))
    controles.append({"controle": "exactitude B2 famille retiree tirage, 58 items",
                      "valeur": v, "reference": 0.583552,
                      "source": "a8-familles-gss.csv, IC [0,5777 ; 0,5892]",
                      "ecart": abs(v - 0.583552)})
    print(f"  B2 famille retiree (tirage)      {v:.6f} contre 0,583552 "
          f"[0,5777 ; 0,5892], flux aleatoire different")

    plafond = float(np.nanmean(C.exactitude(paquet["M"]["humains vague 2"],
                                            y1, lignes, cols)))

    # ------------------------------------------- 3. codage, deductibilite, verifications
    print("\ncodage des matrices")
    codes_nom = {"_humains": C28.coder(y1, lignes, items, options)}
    for nom in methodes:
        codes_nom[nom] = C28.coder(paquet["M"][nom], lignes, items, options)
    brut = {"_humains": y1}
    brut.update({nom: paquet["M"][nom] for nom in methodes})
    codes_lib, k_max_lib = C.codes_libres(brut, cols)

    print("verification des versions vectorisees contre les implementations de reference")
    ver = []
    for nom in ("_humains", "E1 famille retiree (argmax)", "PMM k=10 famille retiree",
                "agents composite", "B2 famille retiree (argmax)"):
        a = C.sommes_dispersion(codes_nom[nom], seg, k_items, cols)
        b = C.sommes_dispersion_rapide(codes_nom[nom], seg, k_max_nom, cols)
        hh, _ = C.entropie_accord_rapide(codes_lib["_humains"], cols, k_max_lib)
        hp, ap = C.entropie_accord_rapide(codes_lib[nom], cols, k_max_lib)
        div_r, acc_r = C.diversite_rapide(hp, ap, hh)
        mat = y1 if nom == "_humains" else paquet["M"][nom]
        ref = C.diversite(mat, y1, lignes, cols)
        ver.append({"matrice": nom,
                    "ecart_dispersion_total": abs(a["total"] - b["total"]),
                    "ecart_dispersion_intra": abs(a["intra"] - b["intra"]),
                    "ecart_dispersion_inter": abs(a["inter"] - b["inter"]),
                    "ecart_diversite": abs(div_r - ref["part_diversite_humaine"]),
                    "ecart_accord": abs(acc_r - ref["accord_par_paires"])})
    ver = pd.DataFrame(ver)
    C.ecrire(ver, "a41-verification-mesures.csv")
    emax = float(ver.drop(columns=["matrice"]).values.max())
    print(f"  ecart maximal entre les deux implementations : {emax:.2e}")
    controles.append({"controle": "ecart maximal versions vectorisees contre reference",
                      "valeur": emax, "reference": 0.0, "source": "interne",
                      "ecart": emax})

    print("\nscore de deductibilite par segment, definition de a34")
    ded = C.deductibilite_segment(paquet, cols)
    b1, b2 = ded["bornes"]
    n_rare = int(ded["rare_vrai"].sum())
    n_t1 = int((ded["rare_vrai"] & (ded["tercile"] == 0)).sum())
    n_t2 = int((ded["rare_vrai"] & (ded["tercile"] == 1)).sum())
    n_t3 = int((ded["rare_vrai"] & (ded["tercile"] == 2)).sum())
    couverture = float((~np.isnan(ded["d_seg"][ded["rare_vrai"]])).mean())
    porte = int(sum(1 for s in ded["mods"] if s))
    print(f"  {n_rare} cellules minoritaires sur les 58 items, {porte} items en portent")
    print(f"  bornes D_seg {b1:.4f} et {b2:.4f} ; T1 {n_t1}, T2 {n_t2}, T3 {n_t3}, "
          f"couverture {couverture:.3f}")
    C.ecrire(pd.DataFrame([{
        "perimetre": "1052 personnes, 58 items", "seuil": C.SEUIL_MINORITE,
        "items_portant_une_minorite": porte, "cellules_minoritaires": n_rare,
        "borne_t1_t2": b1, "borne_t2_t3": b2, "n_t1": n_t1, "n_t2": n_t2, "n_t3": n_t3,
        "couverture_d_seg": couverture, "cases_de_segment": ded["n_segments"]}]),
        "a41-terciles.csv")
    controles.append({"controle": "couverture de D_seg sur les cellules minoritaires",
                      "valeur": couverture, "reference": 0.896,
                      "source": "a34 section 0.2, perimetre 149 items",
                      "ecart": abs(couverture - 0.896)})

    comptes = {nom: C.comptes_minorites(paquet["M"][nom], y1, cols, ded)
               for nom in methodes}

    # --------------------------------------------------- 4. le tableau a quatre cases
    print("\ntableau a quatre cases du regime severe")
    rng = np.random.default_rng(args.graine)
    idx_boot = C.tirages(n, args.tirages, rng)

    hum_nom = C.sommes_dispersion(codes_nom["_humains"], seg, k_items, cols)
    hh_lib, _ = C.entropie_accord_rapide(codes_lib["_humains"], cols, k_max_lib)

    lignes_tab = []
    for nom in methodes:
        acc = C.exactitude(paquet["M"][nom], y1, lignes, cols)
        with np.errstate(invalid="ignore"):
            tir = np.nanmean(acc[idx_boot], axis=1)
        s = C.sommes_dispersion(codes_nom[nom], seg, k_items, cols)
        div = C.diversite(paquet["M"][nom], y1, lignes, cols)
        c = comptes[nom]
        lignes_tab.append({
            "methode": nom, "regime": C.REGIME[nom],
            "famille_retiree": C.FAMILLE_RETIREE[nom],
            "conditionnement": C.CONDITIONNEMENT[nom],
            "n_items": len(cols),
            "exactitude": float(np.nanmean(acc)),
            "exactitude_ic_bas": float(np.percentile(tir, 2.5)),
            "exactitude_ic_haut": float(np.percentile(tir, 97.5)),
            "exactitude_normalisee": float(np.nanmean(acc)) / plafond,
            "ratio_intra_ideologie": s["intra"] / hum_nom["intra"],
            "ratio_inter_ideologie": s["inter"] / hum_nom["inter"],
            "ratio_total_ideologie": s["total"] / hum_nom["total"],
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
            "cellules_minoritaires": float(c["n_rare_vrai"].sum()),
            "raretes_osees": float(c["n_rare_pred"].sum()),
            "rappel_minoritaire": C.taux(c["n_juste"], c["n_rare_vrai"]),
            "precision_minoritaire": C.taux(c["n_juste"], c["n_rare_pred"]),
            "rappel_t1_non_deductible": C.taux(c["n_juste_t1"], c["n_rare_vrai_t1"]),
            "cellules_t1": float(c["n_rare_vrai_t1"].sum()),
        })
        print(f"  {nom:<34} exa {lignes_tab[-1]['exactitude']:.4f} "
              f"intra {lignes_tab[-1]['ratio_intra_ideologie']:.3f} "
              f"inter {lignes_tab[-1]['ratio_inter_ideologie']:.3f} "
              f"div {lignes_tab[-1]['part_diversite_humaine']:.3f} "
              f"rap {lignes_tab[-1]['rappel_minoritaire']:.4f}", flush=True)

    # ----------------------------------------------------------- 5. le bootstrap partage
    decalage_pt = C.ECART_NORMALISE_APPARIE * plafond
    print(f"\ndecalage de la condition appariee : {C.ECART_NORMALISE_APPARIE} de score "
          f"normalise x {plafond:.4f} de plafond = {decalage_pt:.4f} d'exactitude brute")
    appariees = {}
    for nom in ("agents composite", "agents enquete", "agents entretien (v3)"):
        appariees[nom + " [appariee]"] = nom
    for court, source in appariees.items():
        paquet["M"][court] = paquet["M"][source]
        codes_nom[court] = codes_nom[source]
        codes_lib[court] = codes_lib[source]
        comptes[court] = comptes[source]
        C.REGIME[court] = "modele de langage, exactitude decalee"
        C.FAMILLE_RETIREE[court] = "transposee, a8 errata E1"
        C.CONDITIONNEMENT[court] = C.CONDITIONNEMENT[source]

    methodes_boot = methodes + list(appariees)
    decalage = {court: decalage_pt for court in appariees}

    print(f"\nbootstrap apparie sur les 1 052 personnes, {args.tirages} tirages, "
          f"{len(methodes_boot)} conditions")
    dist = C.bootstrap_quantites(paquet, lignes, cols, codes_nom, codes_lib, seg,
                                 k_max_nom, k_max_lib, idx_boot, methodes_boot,
                                 comptes, decalage=decalage)

    # intervalles bootstrap des quantites de structure et de minorite, pour le tableau
    tab = pd.DataFrame(lignes_tab)
    for cle, prefixe in (("intra", "ratio_intra"), ("inter", "ratio_inter"),
                         ("diversite", "part_diversite_humaine"),
                         ("rappel", "rappel_minoritaire"),
                         ("rappel_t1", "rappel_t1_non_deductible")):
        bas, haut = [], []
        for nom in tab.methode:
            d = dist[nom][cle]
            d = d[~np.isnan(d)]
            bas.append(float(np.percentile(d, 2.5)) if len(d) else np.nan)
            haut.append(float(np.percentile(d, 97.5)) if len(d) else np.nan)
        tab[prefixe + "_ic_bas"] = bas
        tab[prefixe + "_ic_haut"] = haut
    C.ecrire(tab, "a41-tableau-quatre-cases.csv")

    # ---------------------------------------------------------------- 6. F1, primaire
    print("\nF1 primaire : 27 contrastes, agents composite contre neuf methodes")
    f1 = []
    attendu = {"exactitude": "agent plus haut",
               "proximite_intra": "agent plus proche de 1",
               "rappel": "agent plus haut"}
    for adv in C.ADVERSAIRES_F1:
        for cle in ("exactitude", "proximite_intra", "rappel"):
            if cle == "proximite_intra":
                d, lo, hi, p = C.contraste_proximite(dist, "agents composite", adv)
            else:
                d, lo, hi, p = C.contraste(dist, "agents composite", adv, cle)
            conforme = (d < 0) if cle == "proximite_intra" else (d > 0)
            f1.append({"famille": "F1 primaire", "condition": "agents composite",
                       "adversaire": adv, "regime_adversaire": C.REGIME[adv],
                       "quantite": cle, "difference_agent_moins_adversaire": d,
                       "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p,
                       "signe_attendu": attendu[cle], "conforme": bool(conforme)})
    f1 = pd.DataFrame(f1)
    f1["p_holm"] = C.holm(f1.p_bootstrap.values)
    f1["p_bh"] = C.benjamini_hochberg(f1.p_bootstrap.values)
    f1["decidable"] = f1.p_holm < 0.05
    C.ecrire(f1, "a41-contrastes-f1.csv")
    print(f"  {int(f1.decidable.sum())} des 27 tests passent Holm a 5 pour cent, "
          f"{int((f1.decidable & f1.conforme).sum())} avec le signe attendu")

    # ---------------------------------------------------------------- 7. F2, secondaire
    print("\nF2 secondaire : 12 contrastes")
    f2 = []
    attendu2 = {"exactitude": "agent plus haut", "diversite": "agent plus haut",
                "intra": "agent plus haut", "inter": "agent plus haut, et c'est un defaut"}
    for cond in ("agents composite", "agents enquete"):
        for cle in ("exactitude", "diversite", "intra", "inter"):
            d, lo, hi, p = C.contraste(dist, cond, "E1 famille retiree (argmax)", cle)
            f2.append({"famille": "F2 secondaire (a)", "condition": cond,
                       "reference": "E1 famille retiree (argmax)", "quantite": cle,
                       "difference": d, "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p,
                       "signe_attendu": attendu2[cle], "conforme": bool(d > 0)})
    for cond in ("agents composite", "agents enquete"):
        for ref in ("E1 famille retiree (argmax)", "B2 famille retiree (argmax)"):
            d, lo, hi, p = C.contraste(dist, cond + " [appariee]", ref, "exactitude")
            f2.append({"famille": "F2 secondaire (b), condition appariee",
                       "condition": cond + " [appariee]", "reference": ref,
                       "quantite": "exactitude", "difference": d, "ic_bas": lo,
                       "ic_haut": hi, "p_bootstrap": p,
                       "signe_attendu": "inconnu, c'est l'objet du test",
                       "conforme": bool(d > 0)})
    f2 = pd.DataFrame(f2)
    f2["p_holm"] = C.holm(f2.p_bootstrap.values)
    f2["p_bh"] = C.benjamini_hochberg(f2.p_bootstrap.values)
    f2["decidable"] = f2.p_holm < 0.05
    C.ecrire(f2, "a41-contrastes-f2.csv")
    print(f"  {int(f2.decidable.sum())} des 12 tests passent Holm a 5 pour cent")

    # --------------------------------- 8. sensibilite du decalage de la condition appariee
    print("\nsensibilite de la condition appariee, hors famille")
    sens = []
    for cond in ("agents composite", "agents enquete", "agents entretien (v3)"):
        base = float(tab.loc[tab.methode == cond, "exactitude"].iloc[0])
        for ref in ("E1 famille retiree (argmax)", "B2 famille retiree (argmax)",
                    "IM m=10 mode, famille retiree", "PMM k=10 famille retiree"):
            vref = float(tab.loc[tab.methode == ref, "exactitude"].iloc[0])
            d0, lo0, hi0, _ = C.contraste(dist, cond, ref, "exactitude")
            for pts in (0.0, 0.01, 0.02, decalage_pt, 0.05):
                sens.append({"condition": cond, "reference": ref,
                             "decalage_applique": pts,
                             "exactitude_condition": base - pts,
                             "exactitude_reference": vref,
                             "difference": d0 - pts,
                             "ic_bas": lo0 - pts, "ic_haut": hi0 - pts,
                             "avantage_survit": bool((lo0 - pts) > 0),
                             "est_le_decalage_de_a8": bool(abs(pts - decalage_pt) < 1e-9),
                             "decalage_de_bascule_point_estime": d0,
                             "decalage_de_bascule_borne_basse": lo0})
    C.ecrire(pd.DataFrame(sens), "a41-condition-appariee.csv")

    # ------------------------------------------------------- 9. le cout du retrait
    print("\ncout du retrait de la famille, hors famille d'hypotheses")
    cout = []
    for facile, severe in (("E1 regression contexte argmax", "E1 famille retiree (argmax)"),
                           ("E2 regression contexte tirage", "E2 famille retiree (tirage)"),
                           ("PMM k=10", "PMM k=10 famille retiree"),
                           ("IM m=10 mode des m", "IM m=10 mode, famille retiree"),
                           ("B2 argmax", "B2 famille retiree (argmax)"),
                           ("B2 tirage", "B2 famille retiree (tirage)")):
        for cle in ("exactitude", "intra", "inter", "diversite", "rappel"):
            d, lo, hi, p = C.contraste(dist, severe, facile, cle)
            cout.append({"methode_facile": facile, "methode_severe": severe,
                         "quantite": cle, "difference_severe_moins_facile": d,
                         "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})
    C.ecrire(pd.DataFrame(cout), "a41-cout-du-retrait.csv")

    # ------------------------------------------------------- 10. F3, les 60 de C3F
    print("\nF3 tertiaire : les 60 personnes de la trace C3F")
    c3f = C33.matrice_c3f(paquet)
    paquet["M"]["C3F"] = c3f["matrice"]
    lignes60 = np.asarray(c3f["lignes"])
    controles.append({"controle": "personnes completes dans la trace C3F",
                      "valeur": float(len(lignes60)), "reference": 60.0,
                      "source": "a33 section 0.1", "ecart": abs(len(lignes60) - 60.0)})
    controles.append({"controle": "personnes partielles ecartees de C3F",
                      "valeur": float(c3f["partielles"]), "reference": 1.0,
                      "source": "a33 section 0.1", "ecart": abs(c3f["partielles"] - 1.0)})

    methodes60 = (["humains vague 2", "C3F", "C3"] + C.SEVERE
                  + ["B3 foret", "B0 mode", "B0 tirage"])
    methodes60 = [x for x in methodes60 if x in paquet["M"]]
    for nom in ("C3F", "C3"):
        if nom in paquet["M"] and nom not in codes_nom:
            codes_nom[nom] = C28.coder(paquet["M"][nom], lignes, items, options)
    brut60 = {"_humains": y1}
    brut60.update({nom: paquet["M"][nom] for nom in methodes60})
    codes_lib60, k_lib60 = C.codes_libres(brut60, cols)
    comptes60 = {nom: C.comptes_minorites(paquet["M"][nom], y1, cols, ded)
                 for nom in methodes60}

    rng60 = np.random.default_rng(args.graine + 1)
    idx60 = C.tirages(len(lignes60), args.tirages_c3f, rng60)
    print(f"  bootstrap apparie sur les 60 personnes, {args.tirages_c3f} tirages")
    dist60 = C.bootstrap_quantites(paquet, lignes60, cols, codes_nom, codes_lib60, seg,
                                   k_max_nom, k_lib60, idx60, methodes60, comptes60,
                                   pas_de_trace=1000)

    plafond60 = float(np.nanmean(C.exactitude(paquet["M"]["humains vague 2"],
                                              y1, lignes60, cols)))
    l60 = []
    for nom in methodes60:
        acc = C.exactitude(paquet["M"][nom], y1, lignes60, cols)
        s = C.sommes_dispersion(codes_nom[nom][lignes60], seg[lignes60], k_items, cols)
        h = C.sommes_dispersion(codes_nom["_humains"][lignes60], seg[lignes60],
                                k_items, cols)
        div = C.diversite(paquet["M"][nom], y1, lignes60, cols)
        d = dist60[nom]["exactitude"]
        l60.append({"methode": nom, "regime": C.REGIME[nom],
                    "famille_retiree": C.FAMILLE_RETIREE[nom],
                    "n_personnes": len(lignes60), "n_items": len(cols),
                    "exactitude": float(np.nanmean(acc)),
                    "exactitude_ic_bas": float(np.percentile(d, 2.5)),
                    "exactitude_ic_haut": float(np.percentile(d, 97.5)),
                    "exactitude_normalisee": float(np.nanmean(acc)) / plafond60,
                    "ratio_intra_ideologie": s["intra"] / h["intra"] if h["intra"] else np.nan,
                    "ratio_inter_ideologie": s["inter"] / h["inter"] if h["inter"] else np.nan,
                    "part_diversite_humaine": div["part_diversite_humaine"],
                    "accord_par_paires": div["accord_par_paires"]})
    t60 = pd.DataFrame(l60)
    controles.append({"controle": "exactitude C3F sur 60 personnes et 58 items",
                      "valeur": float(t60.loc[t60.methode == "C3F", "exactitude"].iloc[0]),
                      "reference": 0.5572, "source": "a33 section 2",
                      "ecart": abs(float(t60.loc[t60.methode == "C3F",
                                                 "exactitude"].iloc[0]) - 0.5572)})
    controles.append({"controle": "exactitude B2 famille retiree sur les 60",
                      "valeur": float(t60.loc[t60.methode == "B2 famille retiree (argmax)",
                                              "exactitude"].iloc[0]),
                      "reference": 0.6822, "source": "a33 section 7",
                      "ecart": abs(float(t60.loc[t60.methode ==
                                                 "B2 famille retiree (argmax)",
                                                 "exactitude"].iloc[0]) - 0.6822)})

    f3 = []
    for adv in C.SEVERE:
        d, lo, hi, p = C.contraste(dist60, "C3F", adv, "exactitude")
        f3.append({"famille": "F3 tertiaire", "condition": "C3F", "adversaire": adv,
                   "regime_adversaire": C.REGIME[adv], "quantite": "exactitude",
                   "difference_c3f_moins_adversaire": d, "ic_bas": lo, "ic_haut": hi,
                   "p_bootstrap": p, "signe_attendu": "C3F plus bas",
                   "conforme": bool(d < 0)})
    f3 = pd.DataFrame(f3)
    f3["p_holm"] = C.holm(f3.p_bootstrap.values)
    f3["p_bh"] = C.benjamini_hochberg(f3.p_bootstrap.values)
    f3["decidable"] = f3.p_holm < 0.05
    C.ecrire(t60, "a41-c3f-60-personnes.csv")
    C.ecrire(f3, "a41-contrastes-f3.csv")
    print(t60[["methode", "exactitude", "part_diversite_humaine",
               "ratio_intra_ideologie"]].to_string(index=False))
    print(f3[["adversaire", "difference_c3f_moins_adversaire", "ic_bas", "ic_haut",
              "p_holm"]].to_string(index=False))

    C.ecrire(pd.DataFrame(controles), "a41-controles.csv")
    print(f"\nduree totale {time.time() - t_debut:.0f} s")


if __name__ == "__main__":
    main()
