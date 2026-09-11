"""
c7_stanford : le jumeau retrouve-t-il la personne, ailleurs que sur Twin-2K-500 ?

===========================================================================
PREENREGISTREMENT : resultats/c7-stanford-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce fichier et avant tout calcul d'appariement.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (archive Stanford des 1 052 agents
generatifs, data/osf-t6g7k-stanford/). Ce script ne calcule, n'imprime et n'ecrit JAMAIS
l'identifiant (« participant_XXXX ») ou l'appariement individuel d'une personne retrouvee :
seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  a2_commun.distance_hamming     la distance de Hamming normalisee (bloc GSS, categoriel)
  a2_commun.bootstrap_personnes  l'intervalle de confiance par reechantillonnage de personnes
  a2_commun.est_manquant         la definition d'une cellule non renseignee
  a30_commun.cellules_gss        la cellule demographique de controle (genre x race x age
                                  x education replies), verifiee compatible avec le format
                                  d'age et d'education de figure3/demographic_summary.csv

CE QUI EST NOUVEAU ICI : l'attaque sur trois blocs (GSS categoriel, Jeux economiques et
Big Five continus), l'accord par distance euclidienne z-scoree pour les blocs continus
(pas d'equivalent Hamming sur des scores continus, difference de methode declaree en
section 4 du preenregistrement), et le rang a l'interieur du segment demographique propre
a Stanford.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_stanford.py
===========================================================================
"""

import os
import sys
import zlib

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import distance_hamming, est_manquant, bootstrap_personnes  # noqa: E402
from a30_commun import cellules_gss, ecrire  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE = os.path.join(RACINE, "data", "osf-t6g7k-stanford")
FIG2 = os.path.join(ARCHIVE, "figure2", "data", "new_analysis_summaries")
DEMO_CSV = os.path.join(ARCHIVE, "figure3", "data", "demographic_summary.csv")

GRAINE = 20260912
N_TIRAGES_LIENS = 20    # tirages aleatoires pour departager les ex aequo de rang
N_BOOTSTRAP = 2000

VAGUE1 = "humains vague 1 (cible)"
VAGUE2 = "humains vague 2 (retest, reference humaine)"
DEMO_COND = "demographique"

# Chaque domaine : son dossier de preparation, son type d'items, et le fichier par
# condition. Les libelles « demographique », « persona », « entretien » suivent le
# tableau de FIGURE2_PIPELINE.md section 6, qui differe d'un domaine a l'autre (v3/v6/v7
# pour le GSS, v3/v4/v6 pour les jeux economiques, v3/v4/v5 pour Big Five).
DOMAINES = {
    "gss": {
        "dossier": "gss_filtered",
        "type": "categoriel",
        "conditions": {
            "composite": "composite_agents_summary.csv",
            "enquete": "survey_agents_summary.csv",
            "entretien": "gss_v3_summary.csv",
            DEMO_COND: "gss_v6_summary.csv",
            "persona": "gss_v7_summary.csv",
            "v8 (exploratoire, non documente Figure 2)": "gss_v8_summary.csv",
        },
    },
    "jeux_economiques": {
        "dossier": "econ_games_main",
        "type": "continu",
        "conditions": {
            "composite": "composite_agents_summary.csv",
            "enquete": "survey_agents_summary.csv",
            DEMO_COND: "econ_games_v3_summary.csv",
            "persona": "econ_games_v4_summary.csv",
            "entretien": "econ_games_v6_summary.csv",
            "v8 (exploratoire, non documente Figure 2)": "econ_games_v8_summary.csv",
        },
    },
    "big_five": {
        "dossier": "bigfive_main",
        "type": "continu",
        "conditions": {
            "composite": "composite_agents_summary.csv",
            "enquete": "survey_agents_summary.csv",
            DEMO_COND: "bigfive_v3_summary.csv",
            "persona": "bigfive_v4_summary.csv",
            "entretien": "bigfive_v5_summary.csv",
            "v8 (exploratoire, non documente Figure 2)": "bigfive_v8_summary.csv",
        },
    },
}


# ---------------------------------------------------------------------------
# Chargement et codage
# ---------------------------------------------------------------------------

def charger_domaine(nom_domaine):
    """Charge vague 1, vague 2 et toutes les conditions d'un domaine, alignees par email.

    La vague 1 fixe l'ordre de reference (les identifiants participant_XXXX ne sont
    jamais utilises au dela de cette jointure, et ne sont ni imprimes ni ecrits).
    """
    spec = DOMAINES[nom_domaine]
    dossier = os.path.join(FIG2, spec["dossier"], "preparation")
    p1 = pd.read_csv(os.path.join(dossier, "p_wave1_summary.csv"))
    ordre = p1["email"].tolist()
    items = [c for c in p1.columns if c != "email"]

    tables = {VAGUE1: p1.set_index("email").loc[ordre, items]}
    p2 = pd.read_csv(os.path.join(dossier, "p_wave2_summary.csv"))
    tables[VAGUE2] = p2.set_index("email").loc[ordre, items]
    for cond, fichier in spec["conditions"].items():
        d = pd.read_csv(os.path.join(dossier, fichier))
        tables[cond] = d.set_index("email").loc[ordre, items]
    return ordre, items, tables, spec["type"]


def coder_categoriel_commun(tables, items):
    """Encode toutes les tables d'un domaine categoriel avec un vocabulaire COMMUN par
    colonne, -1 pour manquant, afin qu'une meme modalite recoive le meme code partout."""
    noms = list(tables)
    n = len(tables[noms[0]])
    codes = {nom: np.full((n, len(items)), -1, dtype=np.int32) for nom in noms}
    for j, it in enumerate(items):
        vocab = {}
        for nom in noms:
            for v in tables[nom][it]:
                if est_manquant(v):
                    continue
                cle = str(v).strip().lower()
                if cle not in vocab:
                    vocab[cle] = len(vocab)
        for nom in noms:
            col = tables[nom][it]
            for i, v in enumerate(col):
                if est_manquant(v):
                    continue
                codes[nom][i, j] = vocab[str(v).strip().lower()]
    return codes


def accord_categoriel(codes_test, codes_pool):
    return 1.0 - distance_hamming(codes_test, codes_pool)


def coder_continu_commun(tables, items):
    """Renvoie les valeurs numeriques brutes de chaque table, memes colonnes, meme ordre."""
    return {nom: tables[nom][items].apply(pd.to_numeric, errors="coerce").to_numpy(dtype=float)
            for nom in tables}


def accord_continu(x_test, x_pool_ref):
    """- distance euclidienne, items z-scores sur la reference (vague 1).

    Seule alternative disponible a la distance de Hamming : les scores de jeux
    economiques et de Big Five sont continus, pas categoriels. Chaque colonne est
    centree-reduite par la moyenne et l'ecart type de la vague 1 (la cible), la meme
    normalisation servant au test et au pool pour ne pas introduire de fuite d'echelle.
    """
    mu = np.nanmean(x_pool_ref, axis=0)
    sd = np.nanstd(x_pool_ref, axis=0)
    sd = np.where(sd > 1e-9, sd, 1.0)
    zt = (x_test - mu) / sd
    zp = (x_pool_ref - mu) / sd
    # distance euclidienne par produit matriciel, NaN traites comme ecart nul (rare, cf.
    # preenregistrement section 0 : quasi aucun manquant sur ces deux blocs)
    zt = np.nan_to_num(zt)
    zp = np.nan_to_num(zp)
    d2 = ((zt[:, None, :] - zp[None, :, :]) ** 2).sum(axis=2)
    return -d2


# ---------------------------------------------------------------------------
# Attaque : rang du vrai repondant
# ---------------------------------------------------------------------------

def rangs_depuis_accord(accord, vrai_idx, rng, n_tirages=N_TIRAGES_LIENS):
    """Rang du vrai repondant pour chaque ligne testee contre tout le pool.

    accord : matrice (n_test, n_pool) de similarite, plus grand = plus proche. Ordre des
    candidats melange par un bruit i.i.d. avant chaque tirage de rang (garde-fou
    preenregistre, section 1 : aucun raccourci d'index ne peut imiter une identification).
    Renvoie, par personne : rang moyen (1 = meilleur), et indicatrices top-1 / top-10
    moyennees sur les tirages.
    """
    n = accord.shape[0]
    top1 = np.zeros(n)
    top10 = np.zeros(n)
    rang = np.zeros(n)
    for _ in range(n_tirages):
        bruit = rng.random(accord.shape) * 1e-9
        ordre = np.argsort(-(accord + bruit), axis=1, kind="stable")
        place = np.argsort(ordre, axis=1)
        vrai = place[np.arange(n), vrai_idx] + 1
        top1 += (vrai == 1)
        top10 += (vrai <= 10)
        rang += vrai
    return rang / n_tirages, top1 / n_tirages, top10 / n_tirages


def rang_dans_segment(accord, vrai_idx, seg, rng, n_tirages=N_TIRAGES_LIENS):
    """Meme rang, mais le pool de chaque personne est restreint a son propre segment
    demographique (genre x race x age replie x education repliee)."""
    n = accord.shape[0]
    top1 = np.zeros(n)
    rang = np.zeros(n)
    taille = np.zeros(n, dtype=int)
    seg_vrai = seg[vrai_idx]
    for g in pd.unique(seg_vrai):
        if g is None:
            continue
        membres = np.flatnonzero(seg_vrai == g)
        idx_seg = np.flatnonzero(seg == g)
        if len(idx_seg) < 2:
            continue
        sous_accord = accord[np.ix_(membres, idx_seg)]
        pos_vraie = np.searchsorted(idx_seg, vrai_idx[membres])
        r, t1, _ = rangs_depuis_accord(sous_accord, pos_vraie, rng, n_tirages)
        rang[membres] = r
        top1[membres] = t1
        taille[membres] = len(idx_seg)
    return rang, top1, taille


def graine_domaine(nom):
    """Un entier stable pour une chaine, contrairement a hash() qui varie d'un
    interpreteur a l'autre (PYTHONHASHSEED) : la reproductibilite l'exige."""
    return zlib.crc32(nom.encode("utf-8"))


def resume_taux(indic, graine):
    return bootstrap_personnes(indic, n_tirages=N_BOOTSTRAP, graine=graine)


# ---------------------------------------------------------------------------
# Un domaine
# ---------------------------------------------------------------------------

def traiter_domaine(nom_domaine, seg):
    ordre, items, tables, typ = charger_domaine(nom_domaine)
    n = len(ordre)
    print(f"\n=== {nom_domaine} : {n} personnes, {len(items)} items ({typ}) ===", flush=True)

    if typ == "categoriel":
        codes = coder_categoriel_commun(tables, items)
        pool = codes[VAGUE1]
        def accord_contre_pool(nom):
            return accord_categoriel(codes[nom], pool)
    else:
        valeurs = coder_continu_commun(tables, items)
        pool_ref = valeurs[VAGUE1]
        def accord_contre_pool(nom):
            return accord_continu(valeurs[nom], pool_ref)

    vrai_idx = np.arange(n)  # meme ordre partout : la ligne i est toujours la meme personne
    lignes = []
    for nom in [VAGUE2] + list(DOMAINES[nom_domaine]["conditions"]):
        rng = np.random.default_rng([GRAINE, graine_domaine(nom_domaine + "|" + nom)])
        accord = accord_contre_pool(nom)
        rang, top1, top10 = rangs_depuis_accord(accord, vrai_idx, rng)
        rang_seg, top1_seg, taille_seg = rang_dans_segment(accord, vrai_idx, seg, rng)
        m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, 1])
        m_t10, b_t10, h_t10 = resume_taux(top10, [GRAINE, 2])
        m_t1s, b_t1s, h_t1s = resume_taux(top1_seg, [GRAINE, 3])
        lignes.append({
            "domaine": nom_domaine, "condition": nom, "n_attaques": n, "n_pool": n,
            "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
            "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
            "rang_median": float(np.median(rang)),
            "top1_hasard": 1.0 / n, "top10_hasard": min(10, n) / n,
            "top1_segment": m_t1s, "top1_segment_bas": b_t1s, "top1_segment_haut": h_t1s,
            "rang_segment_median": float(np.median(rang_seg)),
            "taille_segment_mediane": float(np.median(taille_seg[taille_seg > 0]))
            if (taille_seg > 0).any() else np.nan,
        })
        print(f"{nom_domaine:18s} / {nom:45s} top1={m_t1:.4f} [{b_t1:.4f};{h_t1:.4f}] "
              f"top10={m_t10:.4f} rang_med={np.median(rang):.1f} / {n}", flush=True)
    return pd.DataFrame(lignes)


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    demo = pd.read_csv(DEMO_CSV)

    dfs = []
    for nom_domaine in DOMAINES:
        # Le segment demographique est reconstruit pour l'ordre exact du domaine, au cas
        # ou une future variante du paquet reordonnerait les identifiants.
        ordre = pd.read_csv(os.path.join(FIG2, DOMAINES[nom_domaine]["dossier"],
                                         "preparation", "p_wave1_summary.csv"))["email"].tolist()
        d = demo.set_index("email").loc[ordre]
        seg = cellules_gss(d[["gender", "race", "age", "education"]].to_numpy(dtype=object),
                           ["gender", "race", "age", "education"])
        dfs.append(traiter_domaine(nom_domaine, seg))

    df = pd.concat(dfs, ignore_index=True)
    ecrire(df, "c7-stanford-reidentification.csv")

    # --- verdict, critere preenregistre section 4 : GSS, condition riche contre demographique ---
    gss = df[df.domaine == "gss"]
    demo_top1 = float(gss.loc[gss.condition == DEMO_COND, "top1"].iloc[0])
    riches = gss[(gss.condition != DEMO_COND) & (~gss.condition.str.startswith("v8"))
                & (gss.condition != VAGUE2)]
    meilleur = riches.loc[riches.top1.idxmax()]
    on_fonce = bool(meilleur.top1 >= 0.10 and meilleur.top1 >= 5 * demo_top1)
    print(f"\nmeilleur bloc GSS : {meilleur.condition}, top1={meilleur.top1:.4f} "
          f"vs demographique={demo_top1:.4f} -> on fonce = {on_fonce}", flush=True)

    # --- par bloc : quelle famille d'items porte l'identification ? ---
    par_bloc = (df[~df.condition.isin([VAGUE2]) & (~df.condition.str.startswith("v8"))]
                .groupby("domaine")["top1"].max().rename("meilleur_top1_condition_riche"))
    print("\nmeilleur top-1 par bloc (hors v8, hors reference humaine) :", flush=True)
    print(par_bloc.to_string(), flush=True)
    ecrire(par_bloc.reset_index(), "c7-stanford-par-bloc.csv")


if __name__ == "__main__":
    main()
