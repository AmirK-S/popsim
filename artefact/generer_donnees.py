"""generer_donnees : jeu de donnees FICTIF, a graine fixe, qui imite la structure de
Twin-2K-500 pour l'artefact de relecture (attaque de reidentification + defense D4).

AUCUNE DONNEE REELLE, AUCUNE PERSONNE REELLE. Tout est simule par numpy.random avec une
graine fixe (config.GRAINE). Ecrit uniquement dans artefact/donnees_fictives/.

Structure imitee (voir README.md) :
  - N personnes (config.N_PERSONNES), avec segments demographiques fictifs S_gra
    (genre x age x ethnicite).
  - 60 items "opinion" categoriels, toujours renseignes, SANS signature individuelle
    (seul un effet de segment les gouverne) : role joue par les items d'opinion de Twin.
  - 40 items "achat", matrice produits x prix (5 paliers), avec un signal individuel
    reglable (config.SIGNAL_INDIVIDUEL pour le jumeau "riche") : role joue par le bloc
    Product Preferences - Pricing de Twin, identifie dans c7-mecanisme-resultats.md comme
    le vecteur de la fuite.
  - 20 items de "contexte", avec manquants, jamais utilises par l'attaque : ils servent
    uniquement a exercer items_communs() (importee de c7_reidentification) exactement
    comme sur le vrai Twin, ou 60 des 108 items seulement sont remplis a 100 %.
  - un retest humain (v13), memes personnes, meme profil individuel mais tirage
    independant (fiabilite test-retest imparfaite, jamais 100 %).
  - deux jumeaux simules : "twin_riche" (recopie la verite avec probabilite
    SIGNAL_INDIVIDUEL sur le bloc achat -> la fuite demontrable) et "twin_demo"
    (aucune recopie individuelle, seulement le segment -> comparateur "Demographics
    Only").

Usage : .venv/bin/python artefact/generer_donnees.py
"""

import os
import sys

import numpy as np
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from garde import verifier_environnement  # noqa: E402
import config as CFG  # noqa: E402

DOSSIER_SORTIE = os.path.join(ICI, "donnees_fictives")


def _tirer_par_segment(rng, seg, n_seg, n_items, k, probs_seg):
    """Tire, pour chaque personne et chaque item, une modalite dans la loi de son segment."""
    n = len(seg)
    out = np.empty((n, n_items), dtype=np.int32)
    for g in range(n_seg):
        m = seg == g
        c = int(m.sum())
        if c == 0:
            continue
        for j in range(n_items):
            out[m, j] = rng.choice(k, size=c, p=probs_seg[g, j])
    return out


def generer():
    verifier_environnement(DOSSIER_SORTIE)
    rng = np.random.default_rng(CFG.GRAINE)
    n = CFG.N_PERSONNES

    # --- demographies et segment S_gra fictifs ---
    genre = rng.choice(CFG.GENRES, size=n)
    age = rng.choice(CFG.AGES, size=n)
    ethnie = rng.choice(CFG.ETHNIES, size=n)
    cle_seg = [f"{g}|{a}|{e}" for g, a, e in zip(genre, age, ethnie)]
    niveaux = sorted(set(cle_seg))
    seg_index = {s: i for i, s in enumerate(niveaux)}
    seg = np.array([seg_index[c] for c in cle_seg], dtype=np.int32)
    n_seg = len(niveaux)

    # --- items opinion (60) : loi de segment seulement, aucune signature individuelle ---
    # alpha eleve : la loi de chaque segment reste proche de l'uniforme, pour que le
    # segment demographique seul ne devienne pas, a lui seul, une empreinte (comme dans
    # l'etude reelle, ou seul le bloc d'achat porte la fuite).
    probs_opinion = rng.dirichlet(np.full(CFG.K_OPINION, 8.0), size=(n_seg, CFG.N_OPINION))
    v4_opinion = _tirer_par_segment(rng, seg, n_seg, CFG.N_OPINION, CFG.K_OPINION, probs_opinion)
    v13_opinion = _tirer_par_segment(rng, seg, n_seg, CFG.N_OPINION, CFG.K_OPINION, probs_opinion)
    riche_opinion = _tirer_par_segment(rng, seg, n_seg, CFG.N_OPINION, CFG.K_OPINION, probs_opinion)
    demo_opinion = _tirer_par_segment(rng, seg, n_seg, CFG.N_OPINION, CFG.K_OPINION, probs_opinion)

    # --- items achat (40) : loi de segment (baseline) + profil individuel stable ---
    probs_achat_seg = rng.dirichlet(np.full(CFG.K_ACHAT, 8.0), size=(n_seg, CFG.N_ACHAT))
    profil_individuel = rng.integers(0, CFG.K_ACHAT, size=(n, CFG.N_ACHAT))  # l'"identite"

    def baseline_achat():
        return _tirer_par_segment(rng, seg, n_seg, CFG.N_ACHAT, CFG.K_ACHAT, probs_achat_seg)

    mix_v4 = rng.random((n, CFG.N_ACHAT)) < CFG.PROB_INDIVIDU_ACHAT_VERITE
    v4_achat = np.where(mix_v4, profil_individuel, baseline_achat())

    bruit_retest = rng.random((n, CFG.N_ACHAT)) < CFG.BRUIT_RETEST
    v13_achat = np.where(mix_v4 & ~bruit_retest, profil_individuel, baseline_achat())

    # jumeau "riche" : recopie la verite (v4) avec probabilite SIGNAL_INDIVIDUEL -> la fuite
    copie = rng.random((n, CFG.N_ACHAT)) < CFG.SIGNAL_INDIVIDUEL
    riche_achat = np.where(copie, v4_achat, baseline_achat())

    # jumeau "Demographics Only" : jamais de recopie individuelle
    demo_achat = baseline_achat()

    # --- items de contexte (20), avec manquants : jamais utilises dans l'attaque, servent
    #     a demontrer items_communs() sur un jeu qui n'est pas rempli a 100 % partout ---
    probs_ctx = rng.dirichlet(np.ones(CFG.K_OPINION), size=(n_seg, CFG.N_CONTEXTE))
    ctx_v4 = _tirer_par_segment(rng, seg, n_seg, CFG.N_CONTEXTE, CFG.K_OPINION, probs_ctx)
    ctx_v13 = _tirer_par_segment(rng, seg, n_seg, CFG.N_CONTEXTE, CFG.K_OPINION, probs_ctx)
    ctx_v4[rng.random(ctx_v4.shape) < CFG.PROB_MANQUANT_CONTEXTE] = -1
    ctx_v13[rng.random(ctx_v13.shape) < CFG.PROB_MANQUANT_CONTEXTE] = -1
    ctx_twin = -np.ones((n, CFG.N_CONTEXTE), dtype=np.int32)  # les jumeaux n'ont pas de contexte

    def assembler(op, ac, ctx):
        return np.concatenate([op, ac, ctx], axis=1).astype(np.int32)

    codes = {
        "humains_v4": assembler(v4_opinion, v4_achat, ctx_v4),
        "humains_v13": assembler(v13_opinion, v13_achat, ctx_v13),
        "twin_riche": assembler(riche_opinion, riche_achat, ctx_twin),
        "twin_demo": assembler(demo_opinion, demo_achat, ctx_twin),
    }

    os.makedirs(DOSSIER_SORTIE, exist_ok=True)
    meta = pd.DataFrame({"id": np.arange(n), "genre": genre, "age": age, "ethnie": ethnie,
                         "segment": cle_seg, "seg_code": seg})
    meta.to_csv(os.path.join(DOSSIER_SORTIE, "personnes.csv"), index=False)
    for nom, mat in codes.items():
        pd.DataFrame(mat).to_csv(os.path.join(DOSSIER_SORTIE, f"{nom}.csv"), index=False)
    np.save(os.path.join(DOSSIER_SORTIE, "segment.npy"), seg)

    print(f"genere : {n} personnes fictives, {n_seg} segments S_gra, "
          f"{CFG.N_OPINION} items opinion + {CFG.N_ACHAT} items achat "
          f"(signal individuel = {CFG.SIGNAL_INDIVIDUEL}) + {CFG.N_CONTEXTE} items contexte "
          f"(avec manquants) -> {DOSSIER_SORTIE}", flush=True)
    return DOSSIER_SORTIE


if __name__ == "__main__":
    generer()
