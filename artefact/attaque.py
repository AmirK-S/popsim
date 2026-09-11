"""attaque : rejoue l'attaque de reidentification de analyses/c7_reidentification.py sur
le jeu de donnees FICTIF de artefact/donnees_fictives/.

N'IMPORTE PAS DE DONNEES REELLES : sys.path est etendu jusqu'a analyses/ pour IMPORTER les
fonctions de attaque elles-memes (items_communs, rangs_attaque, rang_dans_segment,
graine_nom), pas pour recopier une ligne de leur code, et jamais pour appeler
t1_commun.charger() (qui, lui, lit data/). Voir README.md.

Calcule top-1, top-10, le rang median, et les comparateurs (hasard exact, jumeau
"Demographics Only") pour le jumeau "riche" (celui qui porte la fuite reglable de
config.SIGNAL_INDIVIDUEL) et pour le jumeau "Demographics Only" (sans fuite).

Usage : .venv/bin/python artefact/attaque.py
"""

import os
import sys

import numpy as np
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from garde import verifier_environnement  # noqa: E402
import config as CFG  # noqa: E402

RACINE_REPO = os.path.dirname(ICI)
ANALYSES = os.path.join(RACINE_REPO, "analyses")
sys.path.insert(0, ANALYSES)

# --- import, pas de recopie : la logique d'attaque vient telle quelle de c7_reidentification ---
from c7_reidentification import (  # noqa: E402
    items_communs, rangs_attaque, rang_dans_segment, graine_nom,
)
from a2_commun import bootstrap_personnes  # noqa: E402

DOSSIER_DONNEES = os.path.join(ICI, "donnees_fictives")
DOSSIER_RESULTATS = os.path.join(ICI, "resultats_artefact")
N_BOOTSTRAP = 2000


def charger_donnees_fictives():
    verifier_environnement(DOSSIER_DONNEES)
    if not os.path.isdir(DOSSIER_DONNEES):
        print("Aucune donnee fictive trouvee : lancez d'abord "
              "`.venv/bin/python artefact/generer_donnees.py`.", file=sys.stderr)
        sys.exit(1)
    meta = pd.read_csv(os.path.join(DOSSIER_DONNEES, "personnes.csv"))
    codes = {
        nom: pd.read_csv(os.path.join(DOSSIER_DONNEES, f"{nom}.csv")).values.astype(np.int32)
        for nom in ("humains_v4", "humains_v13", "twin_riche", "twin_demo")
    }
    seg = np.load(os.path.join(DOSSIER_DONNEES, "segment.npy"))
    return codes, seg, meta


def attaquer(codes, seg):
    """Meme demarche que c7_reidentification.main() : items communs, rang attaque, rang
    dans le segment, IC bootstrap sur les personnes. Chaque ligne du jumeau i correspond,
    par construction du generateur, a la personne i du pool humain (vrai_idx = arange(n))."""
    items = items_communs(codes, ["humains_v4", "humains_v13"])
    pool = codes["humains_v4"][:, items]
    n = pool.shape[0]
    vrai_idx = np.arange(n)

    lignes = []
    for nom in ("twin_demo", "twin_riche"):
        x = codes[nom][:, items]
        rng = np.random.default_rng([CFG.GRAINE, graine_nom(nom)])
        rang, top1, top10 = rangs_attaque(x, pool, vrai_idx, rng)
        _, top1_seg, taille_seg = rang_dans_segment(x, vrai_idx, pool, seg, rng)
        m_t1, b_t1, h_t1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=[CFG.GRAINE, 1])
        m_t10, b_t10, h_t10 = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP, graine=[CFG.GRAINE, 2])
        m_t1s, b_t1s, h_t1s = bootstrap_personnes(top1_seg, n_tirages=N_BOOTSTRAP, graine=[CFG.GRAINE, 3])
        lignes.append({
            "jumeau": nom, "n_attaques": n, "n_pool": n, "n_items": len(items),
            "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
            "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
            "top1_segment": m_t1s, "top1_segment_bas": b_t1s, "top1_segment_haut": h_t1s,
            "rang_median": float(np.median(rang)),
            "top1_hasard": 1.0 / n, "top10_hasard": min(10, n) / n,
            "taille_segment_mediane": float(np.median(taille_seg[taille_seg > 0]))
            if (taille_seg > 0).any() else float("nan"),
        })
        print(f"{nom} : top1={m_t1:.4f} [{b_t1:.4f};{h_t1:.4f}] (hasard={1/n:.4f}) "
              f"top10={m_t10:.4f} rang_med={np.median(rang):.1f} / {n}", flush=True)

    return pd.DataFrame(lignes), items


def main():
    print(f"{CFG.N_PERSONNES} personnes fictives, attaque sur les items toujours renseignes "
          f"(opinion + achat)", flush=True)
    codes, seg, meta = charger_donnees_fictives()
    df, items = attaquer(codes, seg)
    print(f"{len(items)} items communs (toujours renseignes, sur "
          f"{codes['humains_v4'].shape[1]} au total, dont {CFG.N_CONTEXTE} de contexte "
          f"avec manquants exclus)", flush=True)

    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)
    chemin = os.path.join(DOSSIER_RESULTATS, "attaque.csv")
    df.to_csv(chemin, index=False)
    print(f"ecrit {chemin}", flush=True)
    return df


if __name__ == "__main__":
    main()
