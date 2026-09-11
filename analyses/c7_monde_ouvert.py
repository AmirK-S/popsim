"""
c7_monde_ouvert : et si la cible n'est pas dans la base ?

===========================================================================
PREENREGISTREMENT : resultats/c7-monde-ouvert-preenregistrement.md, ecrit le
12 septembre 2026, AVANT ce fichier et avant tout calcul d'appariement.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (Twin-2K-500, archive Stanford).
c7_reidentification.py et c7_stanford.py supposent toujours la cible dans le pool
(monde ferme). Ici : deux regimes par personne attaquee, presente et retiree du pool,
un score de confiance (marge top1 - top2), une courbe ROC, le TPR a FPR fixe, et la
precision au rang 1 sous absence partielle de cible. AUCUN identifiant ni appariement
individuel n'est jamais imprime ou ecrit : seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                 les tables Twin et les demographies brutes
  a2_commun.distance_hamming        la distance de Hamming normalisee
  a2_commun.b2_voisins              le vote des k plus proches voisins (comparateur PMM)
  a2_commun.en_codes                l'encodage categoriel sans fuite
  c7_reidentification.items_communs les 60 items toujours renseignes (Twin)
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel
                                     le chargeur du bloc GSS Stanford, inchange

CE QUI EST NOUVEAU ICI : le score de marge et les deux regimes derives d'UNE SEULE
matrice d'accord (aucun recalcul pour simuler l'absence : la colonne de la vraie
personne est simplement masquee) ; le comparateur PMM k=10 (plus proche voisin sur les
demographies brutes, tirage parmi les k voisins) ; la courbe ROC exacte par tri et
recherche binaire (pas de grille arbitraire de seuils).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_monde_ouvert.py
===========================================================================
"""

import os
import sys
import zlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import distance_hamming, b2_voisins, en_codes              # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13, DEMO     # noqa: E402
import c7_stanford as CS                                                  # noqa: E402

GRAINE = 20260912
K_PMM = 10
N_TIRAGES_LIENS = 5      # tirages pour departager les ex aequo de marge (5, script leger)
FPR_CIBLES = [0.001, 0.01]
P_ABSENCE = [0.0, 0.5, 0.9]


def graine_nom(nom):
    """Entier stable pour une chaine (hash() varie selon PYTHONHASHSEED d'un
    interpreteur a l'autre : la reproductibilite l'exige, meme convention que
    c7_reidentification.graine_nom)."""
    return zlib.crc32(nom.encode("utf-8"))


# ---------------------------------------------------------------------------
# Comparateur PMM : k plus proches voisins sur les demographies brutes seules,
# tirage parmi les k voisins (convention deja en usage dans a35/a41 pour "PMM k=10").
# ---------------------------------------------------------------------------

def pmm_depuis_demo(demo_codes, pool, rng):
    """Une valeur imputee par item, k=10 plus proches voisins sur les demographies,
    la personne elle-meme exclue de la recherche (diagonale mise a l'infini)."""
    n = demo_codes.shape[0]
    dist = distance_hamming(demo_codes, demo_codes)
    np.fill_diagonal(dist, np.inf)
    out = np.zeros((n, pool.shape[1]), dtype=pool.dtype)
    for j in range(pool.shape[1]):
        out[:, j] = b2_voisins(dist, pool[:, j], K_PMM, rng, tirage=True)
    return out


# ---------------------------------------------------------------------------
# Marge top1 - top2, deux regimes (presente / retiree), meme matrice d'accord
# ---------------------------------------------------------------------------

def marges_deux_regimes(accord, vrai_idx, rng, n_tirages=N_TIRAGES_LIENS):
    """accord : (n_test, n_pool). Renvoie, moyenne sur n_tirages depart d'ex aequo :
    marge_presente, correct (top1 = vraie personne), marge_retiree (colonne vraie masquee).
    Rien n'est recalcule entre les deux regimes : la seule difference est un masquage.
    """
    n_test, n_pool = accord.shape
    marge_p = np.zeros(n_test)
    correct = np.zeros(n_test)
    marge_r = np.zeros(n_test)
    lignes = np.arange(n_test)
    for _ in range(n_tirages):
        bruit = accord + rng.random(accord.shape) * 1e-9
        a1 = np.argmax(bruit, axis=1)
        b2 = bruit.copy()
        b2[lignes, a1] = -np.inf
        a2 = np.argmax(b2, axis=1)
        marge_p += accord[lignes, a1] - accord[lignes, a2]
        correct += (a1 == vrai_idx)

        b_retire = bruit.copy()
        b_retire[lignes, vrai_idx] = -np.inf
        r1 = np.argmax(b_retire, axis=1)
        b_retire2 = b_retire.copy()
        b_retire2[lignes, r1] = -np.inf
        r2 = np.argmax(b_retire2, axis=1)
        marge_r += accord[lignes, r1] - accord[lignes, r2]
    return marge_p / n_tirages, correct / n_tirages, marge_r / n_tirages


def compte_au_moins(valeurs_triees, seuils):
    idx = np.searchsorted(valeurs_triees, seuils, side="left")
    return len(valeurs_triees) - idx


def roc_et_taux(marge_p, correct, marge_r, n_test):
    """Courbe ROC exacte (tri + recherche binaire, pas de grille arbitraire), AUC,
    TPR aux FPR cibles (interpolation), abstention au seuil calibre sur FPR = 1 %."""
    seuils = np.unique(np.concatenate([marge_p, marge_r]))
    tpr_num = np.sort(marge_p[correct >= 0.5])           # marge des seules attaques "top1 correct"
    tpr = compte_au_moins(tpr_num, seuils) / n_test
    fpr = compte_au_moins(np.sort(marge_r), seuils) / n_test
    accept_p = compte_au_moins(np.sort(marge_p), seuils) / n_test   # taux d'acceptation brut (regime present)

    ordre = np.argsort(fpr)                              # FPR croissant pour l'AUC et l'interpolation
    fpr_asc, tpr_asc = fpr[ordre], tpr[ordre]
    trapz = getattr(np, "trapezoid", None) or np.trapz
    auc = float(trapz(tpr_asc, fpr_asc))
    tpr_a_fpr = {f: float(np.interp(f, fpr_asc, tpr_asc)) for f in FPR_CIBLES}

    idx_star = int(np.argmax(fpr <= 0.01)) if (fpr <= 0.01).any() else len(seuils) - 1
    abstention_1pct = 1.0 - float(accept_p[idx_star])

    return {
        "auc": auc, "tpr_fpr_0_1pct": tpr_a_fpr[0.001], "tpr_fpr_1pct": tpr_a_fpr[0.01],
        "abstention_a_fpr_1pct": abstention_1pct,
        "roc_fpr": fpr_asc.tolist(), "roc_tpr": tpr_asc.tolist(),
    }


def traiter_predicteur(nom_jeu, nom_pred, accord, vrai_idx, rng):
    n_test = accord.shape[0]
    marge_p, correct, marge_r = marges_deux_regimes(accord, vrai_idx, rng)
    top1_ferme = float(correct.mean())
    r = roc_et_taux(marge_p, correct, marge_r, n_test)
    ligne = {
        "jeu": nom_jeu, "predicteur": nom_pred, "n": n_test,
        "top1_monde_ferme": top1_ferme, "auc_ouvert": r["auc"],
        "tpr_fpr_0_1pct": r["tpr_fpr_0_1pct"], "tpr_fpr_1pct": r["tpr_fpr_1pct"],
        "abstention_a_fpr_1pct": r["abstention_a_fpr_1pct"],
    }
    for p in P_ABSENCE:
        ligne[f"precision1_p{int(p*100)}"] = (1 - p) * top1_ferme
    print(f"{nom_jeu:9s} / {nom_pred:32s} top1_ferme={top1_ferme:.4f} "
          f"AUC={r['auc']:.3f} TPR@0,1%={r['tpr_fpr_0_1pct']:.4f} "
          f"TPR@1%={r['tpr_fpr_1pct']:.4f} abstention@1%={r['abstention_a_fpr_1pct']:.3f}",
          flush=True)
    return ligne, r["roc_fpr"], r["roc_tpr"]


# ---------------------------------------------------------------------------
# Twin-2K-500
# ---------------------------------------------------------------------------

def bloc_twin():
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n = pool.shape[0]
    vrai_idx = np.arange(n)

    demo_codes = en_codes(paq["demo"]["x"])
    rng_pmm = np.random.default_rng([GRAINE, 1])
    pmm = pmm_depuis_demo(demo_codes, pool, rng_pmm)

    sondes = {
        DEMO: codes[DEMO][:, items],
        "Meilleur jumeau (JSON Persona GPT4.1)": codes["JSON Persona - GPT4.1"][:, items],
        "PMM k=10": pmm,
        "Retest humain (plafond)": codes[REF_V13][:, items],
    }
    lignes, courbes = [], []
    top1_humain = None
    for nom, x in sondes.items():
        rng = np.random.default_rng([GRAINE, 2, graine_nom(nom)])
        accord = 1.0 - distance_hamming(x, pool)
        l, fpr, tpr = traiter_predicteur("Twin", nom, accord, vrai_idx, rng)
        if nom == "Retest humain (plafond)":
            top1_humain = l["top1_monde_ferme"]
        lignes.append(l)
        courbes.append(pd.DataFrame({"jeu": "Twin", "predicteur": nom, "fpr": fpr, "tpr": tpr}))
    for l in lignes:
        if top1_humain:
            l["top1_norme_plafond_humain"] = l["top1_monde_ferme"] / top1_humain
    return pd.DataFrame(lignes), pd.concat(courbes, ignore_index=True)


# ---------------------------------------------------------------------------
# Stanford (bloc GSS), loader de c7_stanford reutilise sans modification
# ---------------------------------------------------------------------------

def bloc_stanford():
    ordre, items, tables, _ = CS.charger_domaine("gss")
    codes_gss = CS.coder_categoriel_commun(tables, items)
    pool = codes_gss[CS.VAGUE1]
    n = pool.shape[0]
    vrai_idx = np.arange(n)

    demo = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    demo_arr = demo[["gender", "race", "age", "education"]].astype(str).to_numpy(dtype=object)
    demo_codes = en_codes(demo_arr)
    rng_pmm = np.random.default_rng([GRAINE, 3])
    pmm = pmm_depuis_demo(demo_codes, pool, rng_pmm)

    sondes = {
        "démographique": codes_gss[CS.DEMO_COND],
        "Meilleur agent (composite)": codes_gss["composite"],
        "PMM k=10": pmm,
        "Retest humain (plafond)": codes_gss[CS.VAGUE2],
    }
    lignes, courbes = [], []
    top1_humain = None
    for nom, x in sondes.items():
        rng = np.random.default_rng([GRAINE, 4, graine_nom(nom)])
        accord = CS.accord_categoriel(x, pool)
        l, fpr, tpr = traiter_predicteur("Stanford", nom, accord, vrai_idx, rng)
        if nom == "Retest humain (plafond)":
            top1_humain = l["top1_monde_ferme"]
        lignes.append(l)
        courbes.append(pd.DataFrame({"jeu": "Stanford", "predicteur": nom, "fpr": fpr, "tpr": tpr}))
    for l in lignes:
        if top1_humain:
            l["top1_norme_plafond_humain"] = l["top1_monde_ferme"] / top1_humain
    return pd.DataFrame(lignes), pd.concat(courbes, ignore_index=True)


# ---------------------------------------------------------------------------
# Figure ROC
# ---------------------------------------------------------------------------

def figure_roc(courbes, chemin):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib absent, figure non produite", flush=True)
        return
    fig, ax = plt.subplots(figsize=(7, 5.5))
    for (jeu, pred), g in courbes.groupby(["jeu", "predicteur"]):
        style = "-" if "jumeau" in pred or "agent" in pred or "PMM" in pred else "--"
        ax.plot(np.clip(g["fpr"], 1e-4, 1), g["tpr"], style,
                label=f"{jeu} / {pred}", linewidth=1.4, alpha=0.85)
    ax.set_xscale("log")
    ax.axvline(0.001, color="gray", linestyle=":", linewidth=0.8)
    ax.axvline(0.01, color="gray", linestyle=":", linewidth=0.8)
    ax.set_xlabel("FPR (taux de fausses accusations), échelle log")
    ax.set_ylabel("TPR (identifications correctes)")
    ax.set_title("C7 monde ouvert : ROC par prédicteur et par jeu")
    ax.legend(fontsize=7, loc="lower right")
    ax.set_xlim(1e-4, 1)
    ax.set_ylim(0, 1)
    fig.tight_layout()
    fig.savefig(chemin, dpi=150)
    print(f"figure ecrite : {chemin}", flush=True)


def main():
    print(__doc__.split("=" * 75)[1], flush=True)

    print("\n=== Twin-2K-500 ===", flush=True)
    df_twin, courbes_twin = bloc_twin()

    print("\n=== Stanford (bloc GSS) ===", flush=True)
    df_stanford, courbes_stanford = bloc_stanford()

    df = pd.concat([df_twin, df_stanford], ignore_index=True)
    T1.ecrire(df, "c7-monde-ouvert.csv")

    courbes = pd.concat([courbes_twin, courbes_stanford], ignore_index=True)
    T1.ecrire(courbes, "c7-monde-ouvert-roc.csv")

    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    figure_roc(courbes, os.path.join(racine, "resultats", "c7-monde-ouvert-roc.png"))

    print("\n--- verdict par rapport a la prediction preenregistree ---", flush=True)
    for jeu, pred_riche in [("Twin", "Meilleur jumeau (JSON Persona GPT4.1)"),
                            ("Stanford", "Meilleur agent (composite)")]:
        row = df[(df.jeu == jeu) & (df.predicteur == pred_riche)].iloc[0]
        print(f"{jeu} / {pred_riche} : TPR@FPR=1%={row.tpr_fpr_1pct:.4f}", flush=True)
    for jeu in ["Twin", "Stanford"]:
        for pred in (["Demographics Only - GPT4.1-mini", "PMM k=10"] if jeu == "Twin"
                     else ["démographique", "PMM k=10"]):
            row = df[(df.jeu == jeu) & (df.predicteur == pred)]
            if len(row):
                print(f"{jeu} / {pred} : TPR@FPR=1%={row.iloc[0].tpr_fpr_1pct:.4f}", flush=True)


if __name__ == "__main__":
    main()
