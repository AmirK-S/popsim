"""defense : rejoue la defense D4 (permutation intra-segment) de
resultats/c7-defense-resultats.md sur le bloc d'achat du jumeau "riche" fictif, et mesure
le risque et l'utilite avant / apres.

N'IMPORTE PAS DE DONNEES REELLES : importe defense_d4 et les mesures d'utilite telles
quelles depuis analyses/c7_defense.py (jamais t1_commun.charger(), qui lit data/), et
l'attaque telle quelle depuis analyses/c7_reidentification.py. Applique UNIQUEMENT au
bloc d'achat (40 items) du jumeau, jamais aux humains ni aux items d'opinion, exactement
comme dans l'etude originale.

Usage : .venv/bin/python artefact/defense.py (apres artefact/generer_donnees.py)
"""

import os
import sys

import numpy as np
import pandas as pd

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

from garde import verifier_environnement  # noqa: E402
import config as CFG  # noqa: E402
from attaque import charger_donnees_fictives, DOSSIER_RESULTATS, N_BOOTSTRAP  # noqa: E402

RACINE_REPO = os.path.dirname(ICI)
sys.path.insert(0, os.path.join(RACINE_REPO, "analyses"))

# --- import, pas de recopie : l'attaque et la defense D4 viennent telles quelles ---
from c7_reidentification import items_communs, rangs_attaque, graine_nom  # noqa: E402
from a2_commun import bootstrap_personnes  # noqa: E402
from c7_defense import defense_d4, mesurer_utilite  # noqa: E402


def risque_top1(x, pool, n, suffixe):
    rng = np.random.default_rng([CFG.GRAINE, 900, graine_nom(suffixe)])
    vrai_idx = np.arange(n)
    _, top1, _ = rangs_attaque(x, pool, vrai_idx, rng)
    return bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                graine=[CFG.GRAINE, 901, graine_nom(suffixe)])


def defendre():
    verifier_environnement()
    codes, seg, meta = charger_donnees_fictives()
    items = items_communs(codes, ["humains_v4", "humains_v13"])
    pool = codes["humains_v4"][:, items]
    n = pool.shape[0]

    # position des 40 items d'achat DANS le sous-ensemble `items` (deja restreint aux
    # items toujours renseignes) : les colonnes d'achat sont, avant filtrage, celles de
    # config.I_ACHAT (60..99). items_communs conserve leur ordre, ne les retire jamais
    # puisque le bloc d'achat est, par construction, toujours rempli.
    i_achat_abs = np.arange(CFG.N_OPINION, CFG.N_OPINION + CFG.N_ACHAT)
    achat_dans_items = np.isin(items, i_achat_abs)
    i_achat = np.flatnonzero(achat_dans_items)

    x_riche = codes["twin_riche"][:, items]
    x40 = x_riche[:, i_achat]
    hum40 = pool[:, i_achat]

    def assembler(x40_def):
        out = x_riche.copy()
        out[:, i_achat] = x40_def
        return out

    m0, b0, h0 = risque_top1(x_riche, pool, n, "avant_defense")

    x40_d4 = defense_d4(x40, seg)          # << la defense elle-meme, importee telle quelle
    x_def = assembler(x40_d4)
    m1, b1, h1 = risque_top1(x_def, pool, n, "apres_D4")

    u = mesurer_utilite(x40_d4, x40, hum40, seg, seg)

    lignes = [
        {"etape": "avant defense (jumeau riche)", "top1": m0, "top1_bas": b0, "top1_haut": h0,
         "perte_utilite": 0.0, "dont_distribution": 0.0, "dont_groupes": 0.0,
         "dont_correlations": 0.0},
        {"etape": "apres D4 (melange intra-segment sur le bloc achat)",
         "top1": m1, "top1_bas": b1, "top1_haut": h1,
         "perte_utilite": u["utilite_globale"],
         "dont_distribution": u["erreur_distribution"], "dont_groupes": u["erreur_groupes"],
         "dont_correlations": u["erreur_correlations"]},
    ]
    df = pd.DataFrame(lignes)

    print(f"avant defense : top1={m0:.4f} [{b0:.4f};{h0:.4f}]", flush=True)
    print(f"apres D4      : top1={m1:.4f} [{b1:.4f};{h1:.4f}]  "
          f"perte d'utilite={u['utilite_globale']:.2f} points "
          f"(distrib.={u['erreur_distribution']:.2f} / groupes={u['erreur_groupes']:.2f} / "
          f"corr.={u['erreur_correlations']:.2f})", flush=True)

    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)
    chemin = os.path.join(DOSSIER_RESULTATS, "defense.csv")
    df.to_csv(chemin, index=False)
    print(f"ecrit {chemin}", flush=True)
    return df


if __name__ == "__main__":
    defendre()
