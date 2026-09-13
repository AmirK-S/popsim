"""
c7_variance_generation : le chiffre de titre est-il un tirage unique ?

===========================================================================
PREENREGISTREMENT : resultats/c7-variance-generation-preenregistrement.md, ecrit AVANT
ce fichier et AVANT tout calcul d'etendue, d'ecart type entre bras ou de partage de
variance. Les seuils S1 et S2, l'estimateur de decomposition et les regles d'exclusion
E1-E4 y sont fixes. Le preenregistrement declare en son paragraphe 0 que la colonne
top1 de c7-reidentification.csv avait deja ete lue : aucune "prediction" de ce travail
n'est aveugle, seuls les seuils le sont.

LA QUESTION. Le taux publie de 20,7 % vient d'UN bras (JSON Persona - GPT4.1), un
modele, une generation. Son intervalle [18,96 ; 22,43] est un bootstrap SUR LES
PERSONNES : il ne dit rien de la variabilite due a la generation elle-meme. Ce script
mesure la dispersion ENTRE BRAS a bassin strictement constant et la compare a cette
largeur bootstrap.

ETUDE DE RISQUE DE VIE PRIVEE. Ce script ne lit, ne calcule et n'imprime AUCUNE donnee
individuelle : il ne manipule que des taux deja agreges, lus dans des CSV de resultats.
Aucune identite, aucun TWIN_ID, aucune liste d'appariements n'entre ni ne sort.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  resultats/c7-reidentification.csv    les taux top-1 par bras, a bassin constant (2 058
                                       candidats), memes 60 items, meme attaque de
                                       Hamming, meme convention de departage des ex aequo
                                       (20 tirages), graine 20260911 -- produit par
                                       analyses/c7_reidentification.py sous son propre
                                       preenregistrement
  resultats/c7-temoins-relecture.csv   la dispersion entre 30 tirages d'items par k,
                                       utilisee comme SUBSTITUT declare (section 6 du
                                       preenregistrement)
  resultats/a6-twin-configurations.csv l'exactitude de chaque bras contre les humains
                                       vague 4, pour situer le bras de titre

CE QUI EST NOUVEAU ICI : la comparaison etendue-entre-bras contre largeur-bootstrap, la
decomposition de variance a effets aleatoires, et l'application mecanique des seuils S1
et S2.

AUCUNE REGENERATION DE JUMEAUX. Aucun appel de modele, aucune depense, aucun reseau.
c7_reidentification.py n'est PAS relance : son CSV est relu tel quel.
Usage : .venv/bin/python analyses/c7_variance_generation.py
===========================================================================
"""

import os
import sys

import numpy as np
import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTATS = os.path.join(RACINE, "resultats")

CIBLE = "humains vague 4"            # E1 : la verite terrain, jamais le retest
BRAS_TITRE = "JSON Persona - GPT4.1"
DEMO = "Demographics Only - GPT4.1-mini"
N_ATTAQUES_PLEIN = 2058              # E2 : bassin d'attaque constant

# Le couple le plus proche d'une re-generation pure (section 4 bis) : meme modele, meme
# representation de la personne, seul le reglage de decodage change.
COUPLE_DECODAGE = ("Text Persona - GPT4.1-mini",
                   "Text Persona (Default Temperature) - GPT4.1-mini")

Z95 = 1.959963984540054              # quantile normal a 95 %, pour SE = largeur / (2 z)

SEUIL_S1_GRIS = 1.0                  # E < 1 x L : rien a corriger
SEUIL_S1_TROP_ETROIT = 2.0           # E > 2 x L : intervalles publies trop etroits
SEUIL_S2_CONDITIONNEL = 0.50         # part generation > 50 % : declarer la conditionnalite
SEUIL_S2_NON_BORNANT = 0.90          # part generation > 90 % : l'IC ne borne pas


def lire(nom):
    chemin = os.path.join(RESULTATS, nom)
    if not os.path.exists(chemin):
        sys.exit(f"absent : {chemin}")
    return pd.read_csv(chemin)


def se_depuis_ic(bas, haut):
    """Erreur type deduite d'un IC bootstrap a 95 %, approximation normale.

    Preenregistre section 4. C'est une approximation : le bootstrap sur les personnes
    n'est pas exactement symetrique. Elle est utilisee de facon IDENTIQUE pour tous les
    bras, donc elle ne peut pas creer une difference entre eux.
    """
    return (haut - bas) / (2.0 * Z95)


def decomposer(p, se):
    """Partage de variance a effets aleatoires (preenregistre section 4).

    V_obs  : variance observee des taux entre bras (denominateur n - 1)
    V_intra: variance d'echantillonnage moyenne, deja comptee dans V_obs
    V_gen  : ce qui reste, majorant de la variabilite de re-generation
    """
    v_obs = float(np.var(p, ddof=1))
    v_intra = float(np.mean(se ** 2))
    v_gen = max(0.0, v_obs - v_intra)
    part = v_gen / (v_gen + v_intra) if (v_gen + v_intra) > 0 else float("nan")
    return v_obs, v_intra, v_gen, part


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []

    # ---------------------------------------------------------------- 1. inventaire
    reid = lire("c7-reidentification.csv")
    cfg = lire("a6-twin-configurations.csv")
    exact = dict(zip(cfg["configuration"], cfg["exactitude_vs_humains_w4"]))

    d = reid[reid["cible"] == CIBLE].copy()                       # E1
    d["se"] = se_depuis_ic(d["top1_bas"], d["top1_haut"])
    d["largeur_ic"] = d["top1_haut"] - d["top1_bas"]
    d["exactitude"] = d["configuration"].map(exact)
    d = d.sort_values("top1", ascending=False).reset_index(drop=True)

    print(f"\n=== 1. INVENTAIRE : {len(d)} bras mesures, cible = {CIBLE} ===")
    print(f"{'bras':<50}{'n_att':>7}{'top1':>9}{'IC bootstrap':>22}{'exact.':>9}")
    for _, r in d.iterrows():
        marque = " <- TITRE" if r["configuration"] == BRAS_TITRE else ""
        ic = f"[{100*r['top1_bas']:.2f};{100*r['top1_haut']:.2f}]"
        ex = f"{r['exactitude']:.4f}" if pd.notna(r["exactitude"]) else "-"
        print(f"{r['configuration']:<50}{int(r['n_attaques']):>7}"
              f"{100*r['top1']:>8.4f}%{ic:>22}{ex:>9}{marque}")
        lignes.append({
            "table": "inventaire", "bras": r["configuration"],
            "n_attaques": int(r["n_attaques"]), "n_pool": int(r["n_pool"]),
            "top1": r["top1"], "top1_bas": r["top1_bas"], "top1_haut": r["top1_haut"],
            "se_personnes": r["se"], "largeur_ic": r["largeur_ic"],
            "exactitude_vs_w4": r["exactitude"],
            "bassin_attaque_plein": int(r["n_attaques"]) == N_ATTAQUES_PLEIN,
            "note": "bras du chiffre de titre" if r["configuration"] == BRAS_TITRE else "",
        })

    # E2 : seuls les bras au bassin d'attaque plein entrent dans le calcul principal
    plein = d[d["n_attaques"] == N_ATTAQUES_PLEIN].copy()
    ecarte = d[d["n_attaques"] != N_ATTAQUES_PLEIN]
    for _, r in ecarte.iterrows():
        print(f"\nE2 : {r['configuration']} ecarte du calcul principal "
              f"({int(r['n_attaques'])} personnes attaquees, pas {N_ATTAQUES_PLEIN}) "
              f"-- top1 = {100*r['top1']:.4f} %, reporte a part")

    riches = plein[plein["configuration"] != DEMO].copy()   # sans la baseline demographique

    titre = d[d["configuration"] == BRAS_TITRE].iloc[0]
    L = float(titre["largeur_ic"])
    print(f"\nbras de titre : {BRAS_TITRE}")
    print(f"  top1 = {100*titre['top1']:.4f} %  IC = [{100*titre['top1_bas']:.4f} ; "
          f"{100*titre['top1_haut']:.4f}]  largeur L = {100*L:.4f} points")
    rang = int((d["top1"] > titre["top1"]).sum()) + 1
    print(f"  rang du bras de titre parmi les {len(d)} bras mesures : {rang}"
          f"{'  (c est le MAXIMUM)' if rang == 1 else ''}")
    rang_ex = int((d["exactitude"] > titre["exactitude"]).sum()) + 1
    print(f"  rang en exactitude : {rang_ex} sur {d['exactitude'].notna().sum()}")

    # -------------------------------------------------- 2. dispersion entre bras / S1
    print("\n=== 2. DISPERSION ENTRE BRAS contre INTERVALLE BOOTSTRAP (seuil S1) ===")
    for nom, sous in (("7 bras (avec la baseline demographique)", plein),
                      ("6 bras riches (sans la baseline demographique)", riches)):
        p = sous["top1"].to_numpy()
        E = float(p.max() - p.min())
        rapport = E / L
        if rapport > SEUIL_S1_TROP_ETROIT:
            verdict = "S1 FRANCHI : intervalles publies TROP ETROITS"
        elif rapport < SEUIL_S1_GRIS:
            verdict = "S1 non franchi : les IC absorbent la dispersion"
        else:
            verdict = "zone grise : ne pas trancher"
        print(f"\n  {nom}  (n = {len(sous)})")
        print(f"    etendue E        = {100*E:.4f} points "
              f"({100*p.min():.4f} % a {100*p.max():.4f} %)")
        print(f"    largeur IC L     = {100*L:.4f} points")
        print(f"    rapport E / L    = {rapport:.4f}")
        print(f"    ecart type inter = {100*np.std(p, ddof=1):.4f} points")
        print(f"    -> {verdict}")
        lignes.append({
            "table": "dispersion", "bras": nom, "n_bras": len(sous),
            "etendue_points": E, "min": float(p.min()), "max": float(p.max()),
            "largeur_ic_titre": L, "rapport_E_sur_L": rapport,
            "ecart_type_inter_bras": float(np.std(p, ddof=1)),
            "seuil_S1_franchi": bool(rapport > SEUIL_S1_TROP_ETROIT), "note": verdict,
        })

    # ------------------------------------------- 3. decomposition de variance / S2
    print("\n=== 3. DECOMPOSITION DE LA VARIABILITE (seuil S2) ===")
    for nom, sous in (("7 bras (avec la baseline demographique)", plein),
                      ("6 bras riches (sans la baseline demographique)", riches)):
        p = sous["top1"].to_numpy()
        se = sous["se"].to_numpy()
        v_obs, v_intra, v_gen, part = decomposer(p, se)
        if part > SEUIL_S2_NON_BORNANT:
            verdict = "S2 : l'IC publie NE BORNE PAS l'incertitude du chiffre"
        elif part > SEUIL_S2_CONDITIONNEL:
            verdict = "S2 : l'article doit declarer la conditionnalite a une generation"
        else:
            verdict = "S2 non franchi"
        print(f"\n  {nom}  (n = {len(sous)})")
        print(f"    variance observee entre bras V_obs   = {v_obs:.8f}")
        print(f"    variance d'echantillonnage  V_intra  = {v_intra:.8f}  "
              f"(personnes, deja dans V_obs)")
        print(f"    composante de generation    V_gen    = {v_gen:.8f}")
        print(f"    part imputable a la generation       = {100*part:.2f} %")
        print(f"    part imputable aux personnes         = {100*(1-part):.2f} %")
        print(f"    -> {verdict}")
        lignes.append({
            "table": "decomposition", "bras": nom, "n_bras": len(sous),
            "v_obs": v_obs, "v_intra_personnes": v_intra, "v_gen": v_gen,
            "part_generation": part, "part_personnes": 1.0 - part,
            "seuil_S2_franchi": bool(part > SEUIL_S2_CONDITIONNEL), "note": verdict,
        })

    # ------------------------------------------------ 4. le minorant : decodage seul
    print("\n=== 4. MINORANT : le seul contraste proche d'une re-generation pure ===")
    a, b = COUPLE_DECODAGE
    ra = d[d["configuration"] == a]
    rb = d[d["configuration"] == b]
    if len(ra) and len(rb):
        ra, rb = ra.iloc[0], rb.iloc[0]
        ecart = abs(float(ra["top1"]) - float(rb["top1"]))
        recouvre = not (ra["top1_haut"] < rb["top1_bas"] or rb["top1_haut"] < ra["top1_bas"])
        print(f"  {a:<50}{100*ra['top1']:>8.4f} %  "
              f"[{100*ra['top1_bas']:.4f};{100*ra['top1_haut']:.4f}]")
        print(f"  {b:<50}{100*rb['top1']:>8.4f} %  "
              f"[{100*rb['top1_bas']:.4f};{100*rb['top1_haut']:.4f}]")
        print(f"  ecart = {100*ecart:.4f} points "
              f"({100*ecart/float(ra['top1']):.2f} % en relatif)")
        print(f"  IC {'qui se recouvrent' if recouvre else 'disjoints'}")
        print("  ATTENTION : meme modele, meme representation de la personne, seul le\n"
              "  reglage de decodage change. C'est un MINORANT de l'instabilite de\n"
              "  generation, et il ne porte pas sur le bras de titre.")
        lignes.append({
            "table": "minorant_decodage", "bras": f"{a} vs {b}",
            "top1": ra["top1"], "top1_autre": rb["top1"], "ecart_points": ecart,
            "ecart_relatif": ecart / float(ra["top1"]), "ic_recouvrent": bool(recouvre),
            "note": "minorant : decodage seul, pas le bras de titre",
        })

    # protocole d'inference a modele et representation constants (Text Persona mini)
    famille = d[d["configuration"].str.startswith("Text Persona")
                & d["configuration"].str.contains("GPT4.1-mini")]
    if len(famille) > 1:
        p = famille["top1"].to_numpy()
        print(f"\n  Famille Text Persona - GPT4.1-mini ({len(famille)} protocoles "
              f"d'inference, modele et representation constants) :")
        print(f"    {100*p.min():.4f} % a {100*p.max():.4f} %  -- etendue "
              f"{100*(p.max()-p.min()):.4f} points, soit "
              f"{100*(p.max()-p.min())/p.min():.2f} % en relatif du plus bas")
        lignes.append({
            "table": "protocole_inference", "bras": "Text Persona - GPT4.1-mini (4 protocoles)",
            "n_bras": len(famille), "min": float(p.min()), "max": float(p.max()),
            "etendue_points": float(p.max() - p.min()),
            "ecart_relatif": float((p.max() - p.min()) / p.min()),
            "note": "modele et representation constants, protocole d'inference variable",
        })

    # --------------------------------------- 5. substitut : tirages d'items declares
    print("\n=== 5. SUBSTITUT DECLARE : dispersion entre tirages d'items ===")
    print("  Ce n'est PAS la mesure demandee. C'est ce que le choix du sous-ensemble")
    print("  d'items fait bouger, pas ce que la re-generation ferait bouger.")
    tem = lire("c7-temoins-relecture.csv")
    t = tem[(tem["mesure"] == "top1") & (tem["candidat"] == BRAS_TITRE)
            & tem["tirages_ecart_type"].notna()].copy()
    for _, r in t.sort_values("k_items").iterrows():
        rel = float(r["tirages_ecart_type"]) / float(r["valeur"])
        etendue = float(r["tirages_max"]) - float(r["tirages_min"])
        print(f"    k = {int(r['k_items']):>2} items, {int(r['n_tirages_items'])} tirages : "
              f"moyenne {100*float(r['valeur']):.4f} % "
              f"[{100*float(r['tirages_min']):.4f} ; {100*float(r['tirages_max']):.4f}] "
              f"ecart type {100*float(r['tirages_ecart_type']):.4f} pt "
              f"({100*rel:.2f} % en relatif)")
        lignes.append({
            "table": "substitut_items", "bras": BRAS_TITRE, "k_items": int(r["k_items"]),
            "n_tirages_items": int(r["n_tirages_items"]), "top1": float(r["valeur"]),
            "min": float(r["tirages_min"]), "max": float(r["tirages_max"]),
            "etendue_points": etendue,
            "ecart_type_tirages": float(r["tirages_ecart_type"]),
            "ecart_relatif": rel,
            "note": "SUBSTITUT : variabilite entre tirages d'items, pas de generation",
        })
    print(f"\n  Pour memoire, la largeur relative de l'IC bootstrap du bras de titre a")
    print(f"  k = 60 (tous les items, aucun tirage) : {100*L/float(titre['top1']):.2f} %.")

    # ---------------------------------------------------- 6. ce qui n'existe PAS
    print("\n=== 6. CE QUI N'EXISTE PAS SUR DISQUE, ET QUI SEUL REPONDRAIT ===")
    print("  Aucune condition, dans aucune famille, n'a deux executions. Le bras de")
    print("  titre (JSON Persona - GPT4.1) n'a AUCUN replicat : ni autre graine, ni")
    print("  autre execution, ni autre temperature. La variabilite de re-generation a")
    print("  condition constante n'est donc PAS mesuree par ce travail, et ne peut pas")
    print("  l'etre sans depense (regle R1 du preenregistrement).")
    lignes.append({
        "table": "lacune", "bras": BRAS_TITRE, "n_bras": 1,
        "note": "aucun replicat a condition constante sur disque, dans aucune famille ; "
                "la variabilite de re-generation n'est pas mesuree et ne peut l'etre sans depense",
    })

    df = pd.DataFrame(lignes)
    sortie = os.path.join(RESULTATS, "c7-variance-generation.csv")
    df.to_csv(sortie, index=False)
    print(f"\necrit : {sortie}  ({len(df)} lignes)")


if __name__ == "__main__":
    main()
