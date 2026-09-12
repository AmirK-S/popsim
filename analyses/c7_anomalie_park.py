"""
c7_anomalie_park : pourquoi le canal inter-jumeaux fuit-il ~3x moins sur Park/Stanford
(177 items GSS communs, 11,9-13,0 % top-1) que sur Twin-2K-500 (60 items communs,
36,4 % top-1), alors que Park a ~3x plus d'items communs ?

===========================================================================
PREENREGISTREMENT : resultats/c7-anomalie-park-2026-09-12.md, sections 0 a 3, ecrites
AVANT ce fichier et avant tout calcul.

ETUDE DE RISQUE DE VIE PRIVEE sur deux jeux deja publics (Twin-2K-500, archive
Park et al./Stanford). Ce script ne calcule, n'imprime et n'ecrit JAMAIS un identifiant
ou un appariement individuel : seuls des taux et statistiques agreges sortent dans
resultats/c7-anomalie-park.csv.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                          les quinze tables de Twin
  c7_reidentification.items_communs, rangs_attaque, graine_nom, resume_taux
  c7_transfert.items_pair                    items communs a une paire precise de configs
  c7_stanford.charger_domaine                 vague1/vague2/conditions Stanford, alignees
  c7_stanford.coder_categoriel_commun         vocabulaire commun par colonne, -1 = manquant
  a2_commun.bootstrap_personnes (via resume_taux)

CE QUI EST NOUVEAU ICI :
  - V de Cramer moyen entre items et "items effectifs" (H2, dependance entre items),
    sur les reponses HUMAINES des deux jeux (pas les jumeaux : la redondance d'un
    questionnaire est une propriete du questionnaire/de la population, pas du jumeau).
  - Sous-echantillonnage du bassin Twin a N=1052 sur le CANAL INTER-JUMEAUX precis qui
    montre l'anomalie (H3, taille du bassin) -- different de c7_echelle.py qui ne
    couvre que le canal jumeau-vs-humain.
  - Mesure descriptive de la longueur de persona Twin (H1, wave_persona_chunk_001.parquet).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_anomalie_park.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
from c7_reidentification import items_communs, rangs_attaque, graine_nom, resume_taux  # noqa: E402
from c7_transfert import items_pair                                        # noqa: E402
from c7_stanford import charger_domaine, coder_categoriel_commun, DOMAINES  # noqa: E402
from a2_commun import bootstrap_personnes                                  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAINE = 20260912
N_BOOTSTRAP = 2000
N_TIRAGES_N = 20
MIN_PAIRE = 20   # sous ce nombre de reponses conjointes, une paire d'items est ignoree

REF_V4 = "humains vague 4"
REF_V13 = "humains vagues 1-3 (retest)"


def ecrire(df, nom):
    p = os.path.join(RACINE, "resultats", nom)
    df.to_csv(p, index=False)
    print(f"ecrit : {p} ({len(df)} lignes)", flush=True)


# ---------------------------------------------------------------------------
# H2 : dependance entre items (V de Cramer moyen, items effectifs)
# ---------------------------------------------------------------------------

def cramers_v(a, b):
    """V de Cramer entre deux colonnes de codes entiers (-1 = manquant). np.nan si
    effectif conjoint insuffisant ou si l'une des deux colonnes est constante."""
    mask = (a >= 0) & (b >= 0)
    n = int(mask.sum())
    if n < MIN_PAIRE:
        return np.nan
    a, b = a[mask], b[mask]
    ca, cb = int(a.max()) + 1, int(b.max()) + 1
    table = np.zeros((ca, cb))
    np.add.at(table, (a, b), 1)
    lignes = table.sum(axis=1) > 0
    colonnes = table.sum(axis=0) > 0
    table = table[lignes][:, colonnes]
    r, c = table.shape
    if r < 2 or c < 2:
        return 0.0
    row_sums = table.sum(axis=1, keepdims=True)
    col_sums = table.sum(axis=0, keepdims=True)
    attendu = row_sums @ col_sums / n
    with np.errstate(divide="ignore", invalid="ignore"):
        chi2 = np.nansum(np.where(attendu > 0, (table - attendu) ** 2 / attendu, 0.0))
    denom = n * (min(r, c) - 1)
    if denom <= 0:
        return 0.0
    return float(np.sqrt(chi2 / denom))


def v_barre_matrice(codes_matrice):
    """Moyenne du V de Cramer sur toutes les paires d'items avec effectif conjoint
    suffisant (aucun bootstrap, un seul passage)."""
    n_items = codes_matrice.shape[1]
    vs = []
    for i in range(n_items):
        for j in range(i + 1, n_items):
            v = cramers_v(codes_matrice[:, i], codes_matrice[:, j])
            if not np.isnan(v):
                vs.append(v)
    return np.array(vs)


def v_moyen_et_items_effectifs(codes_matrice, nom, n_bootstrap_v=200):
    """codes_matrice : (n_personnes, n_items), -1 = manquant. Moyenne du V de Cramer sur
    toutes les paires d'items avec effectif conjoint suffisant, puis items effectifs
    = N/(1+(N-1) V_barre) (taille effective sous correlation intra-classe constante).
    IC 95% par bootstrap sur les PERSONNES (reechantillonnage des lignes, n_bootstrap_v
    repetitions -- moins que N_BOOTSTRAP=2000 des autres mesures de ce script car chaque
    repetition recalcule toutes les paires d'items, cout domine par le nombre de paires)."""
    n_items = codes_matrice.shape[1]
    n_personnes = codes_matrice.shape[0]
    t0 = time.time()
    vs = v_barre_matrice(codes_matrice)
    v_barre = float(np.mean(vs))
    v_median = float(np.median(vs))
    items_eff = n_items / (1.0 + (n_items - 1) * v_barre)

    rng = np.random.default_rng([GRAINE, graine_nom(nom)])
    v_barre_boot = np.empty(n_bootstrap_v)
    items_eff_boot = np.empty(n_bootstrap_v)
    for b in range(n_bootstrap_v):
        idx = rng.choice(n_personnes, size=n_personnes, replace=True)
        vb = v_barre_matrice(codes_matrice[idx])
        v_barre_boot[b] = np.mean(vb)
        items_eff_boot[b] = n_items / (1.0 + (n_items - 1) * v_barre_boot[b])
    v_bas, v_haut = np.percentile(v_barre_boot, [2.5, 97.5])
    eff_bas, eff_haut = np.percentile(items_eff_boot, [2.5, 97.5])

    print(f"{nom} : {n_items} items, {len(vs)} paires exploitables, "
          f"V_barre={v_barre:.4f} [{v_bas:.4f};{v_haut:.4f}], V_median={v_median:.4f}, "
          f"items_effectifs={items_eff:.2f} [{eff_bas:.2f};{eff_haut:.2f}] "
          f"({time.time()-t0:.1f}s, {n_bootstrap_v} tirages bootstrap)", flush=True)
    return {"jeu": nom, "n_items": n_items, "n_paires": len(vs),
            "v_cramer_moyen": v_barre, "v_cramer_moyen_bas": float(v_bas),
            "v_cramer_moyen_haut": float(v_haut), "v_cramer_median": v_median,
            "items_effectifs": items_eff, "items_effectifs_bas": float(eff_bas),
            "items_effectifs_haut": float(eff_haut)}


def calculer_h2():
    print("\n--- H2 : dependance entre items ---", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    items_twin = items_communs(codes, [REF_V4, REF_V13])
    mat_twin = codes[REF_V4][:, items_twin]
    ligne_twin = v_moyen_et_items_effectifs(mat_twin, "Twin (60 items communs, humains v4)")

    ordre, items_gss, tables, _ = charger_domaine("gss")
    codes_gss = coder_categoriel_commun(tables, items_gss)
    mat_gss = codes_gss["humains vague 1 (cible)"]
    ligne_gss = v_moyen_et_items_effectifs(mat_gss, "Park/Stanford (177 items GSS, humains v1)")

    ratio_brut = ligne_gss["n_items"] / ligne_twin["n_items"]
    ratio_effectif = ligne_gss["items_effectifs"] / ligne_twin["items_effectifs"]
    if ratio_effectif < 1.2:
        verdict = "fortement soutenue"
    elif ratio_effectif < 2.0:
        verdict = "soutenue"
    elif ratio_effectif >= 2.5:
        verdict = "rejetee"
    else:
        verdict = "ambigue"
    print(f"ratio brut items = {ratio_brut:.2f}, ratio effectif = {ratio_effectif:.2f} "
          f"-> H2 {verdict}", flush=True)
    df = pd.DataFrame([ligne_twin, ligne_gss])
    df["ratio_brut_items"] = ratio_brut
    df["ratio_effectif_items"] = ratio_effectif
    df["verdict_h2"] = verdict
    return df


# ---------------------------------------------------------------------------
# H3 : taille du bassin, canal inter-jumeaux precis (pas jumeau-vs-humain)
# ---------------------------------------------------------------------------

def sous_echantillon_top1(vec_test, pool_full, n_cible, n_tirages, graine_base):
    """Top-1 moyen (+ IC bootstrap sur les personnes) apres n_tirages sous-echantillonnages
    sans remise du bassin (et des memes personnes attaquees, restreintes au sous-tirage)
    a n_cible individus. Meme logique que c7_echelle.py (sous-pool = attaques = memes
    personnes), transposee au canal inter-jumeaux au lieu du canal jumeau-vs-humain."""
    n_total = vec_test.shape[0]
    graine_liste = list(graine_base) if isinstance(graine_base, (list, tuple)) else [graine_base]
    tous_top1 = []
    for t in range(n_tirages):
        rng_tirage = np.random.default_rng(graine_liste + [1000 + t])
        sous_idx = rng_tirage.choice(n_total, size=n_cible, replace=False)
        vt = vec_test[sous_idx]
        pf = pool_full[sous_idx]
        vrai = np.arange(n_cible)
        rng_rang = np.random.default_rng(graine_liste + [2000 + t])
        _, top1, _ = rangs_attaque(vt, pf, vrai, rng_rang)
        tous_top1.append(top1)
    tous_top1 = np.concatenate(tous_top1)
    m, bas, haut = bootstrap_personnes(tous_top1, n_tirages=N_BOOTSTRAP, graine=graine_liste)
    return m, bas, haut


def calculer_h3():
    print("\n--- H3 : taille du bassin, canal inter-jumeaux ---", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    n_total = codes[REF_V4].shape[0]

    paires = [
        ("JSON Persona - GPT4.1", "Text Persona - GPT4.1-mini"),
        ("Text Persona (Default Temperature) - GPT4.1-mini", "Text Persona - GPT4.1-mini"),
    ]
    lignes = []
    for x_nom, y_nom in paires:
        attaques_idx = np.arange(n_total)
        pool_idx = np.arange(n_total)
        items = items_pair(codes, x_nom, y_nom, attaques_idx, pool_idx)
        vec_test = codes[x_nom][:, items]
        pool_full = codes[y_nom][:, items]

        rng_full = np.random.default_rng([GRAINE, graine_nom(x_nom + "|" + y_nom)])
        _, top1_full, _ = rangs_attaque(vec_test, pool_full, np.arange(n_total), rng_full)
        m_full, b_full, h_full = resume_taux(top1_full, [GRAINE, graine_nom(x_nom + y_nom + "full")])

        m_sub, b_sub, h_sub = sous_echantillon_top1(
            vec_test, pool_full, 1052, N_TIRAGES_N,
            [GRAINE, graine_nom(x_nom + "|" + y_nom + "|sous1052")])

        sens = "top1(N=1052) >= top1(N=2058)" if m_sub >= m_full else "top1(N=1052) < top1(N=2058)"
        print(f"{x_nom} -> {y_nom} ({len(items)} items) : "
              f"N=2058 top1={m_full:.4f} [{b_full:.4f};{h_full:.4f}] ; "
              f"N=1052 top1={m_sub:.4f} [{b_sub:.4f};{h_sub:.4f}] -- {sens}", flush=True)
        lignes.append({
            "config_x": x_nom, "config_y": y_nom, "n_items": len(items),
            "top1_N2058": m_full, "top1_N2058_bas": b_full, "top1_N2058_haut": h_full,
            "top1_N1052": m_sub, "top1_N1052_bas": b_sub, "top1_N1052_haut": h_sub,
            "sens": sens,
        })
    df = pd.DataFrame(lignes)
    toutes_augmentent = bool((df["top1_N1052"] >= df["top1_N2058_bas"]).all())
    verdict = ("H3 rejetee comme explication (le bassin plus petit ne fait pas baisser "
               "le top-1, donc ne peut pas expliquer un top-1 plus bas cote Park)"
               if toutes_augmentent else
               "surprise : le top-1 baisse avec un bassin plus petit -- a examiner")
    print(f"verdict H3 : {verdict}", flush=True)
    df["verdict_h3"] = verdict
    return df


# ---------------------------------------------------------------------------
# H1 : mesure descriptive de la longueur de persona Twin (Park non mesurable, voir texte)
# ---------------------------------------------------------------------------

def calculer_h1():
    print("\n--- H1 : longueur de persona (descriptif, Twin seulement) ---", flush=True)
    p = os.path.join(RACINE, "data", "twin2k500", "wave_persona_chunk_001.parquet")
    d = pd.read_parquet(p)
    lignes = []
    for col in ["wave1_3_persona_text", "wave1_3_persona_json"]:
        longueurs = d[col].dropna().str.len().to_numpy(dtype=float)
        m, bas, haut = bootstrap_personnes(longueurs, n_tirages=N_BOOTSTRAP, graine=GRAINE)
        mediane = float(np.median(longueurs))
        print(f"{col} : n={len(longueurs)}, moyenne={m:.0f} [{bas:.0f};{haut:.0f}] "
              f"caracteres, mediane={mediane:.0f}", flush=True)
        lignes.append({"colonne": col, "n_personnes": len(longueurs),
                        "longueur_moyenne_caracteres": m,
                        "longueur_moyenne_bas": bas, "longueur_moyenne_haut": haut,
                        "longueur_mediane_caracteres": mediane})
    return pd.DataFrame(lignes)


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    df_h1 = calculer_h1()
    df_h2 = calculer_h2()
    df_h3 = calculer_h3()

    # Seul fichier de sortie autorise par la mission : un unique csv de synthese
    # (pas de fichier intermediaire par hypothese, pour rester dans le perimetre
    # d'ecriture accorde).
    resume = pd.concat([
        df_h1.assign(hypothese="H1_persona"),
        df_h2.assign(hypothese="H2_dependance"),
        df_h3.assign(hypothese="H3_bassin"),
    ], ignore_index=True)
    ecrire(resume, "c7-anomalie-park.csv")


if __name__ == "__main__":
    main()
