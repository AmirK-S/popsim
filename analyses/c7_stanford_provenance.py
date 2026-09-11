"""
c7_stanford_provenance : le 65,7 % de re-identification Stanford est-il contamine ?

===========================================================================
PREENREGISTREMENT : resultats/c7-stanford-provenance-preenregistrement.md, ecrit le
12 septembre 2026, AVANT ce fichier et avant tout calcul de symetrie.

AUDIT, pas une defense du resultat. Un examen critique independant signale que la
provenance des agents Stanford (data/osf-t6g7k-stanford/) n'a pas ete auditee, a la
difference de Twin-2K-500 (resultats/twin-ab-audit-provenance-2026-09-11.md). Si les
agents ont ete construits a partir des memes reponses GSS de vague 1 que celles qu'on
utilise pour les retrouver, le 65,7 % est une recopie degradee.

ETHIQUE : aucun identifiant, aucun appariement individuel. Uniquement des taux agreges.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  c7_stanford.charger_domaine            chargement vague1/vague2/conditions, meme ordre
  c7_stanford.coder_categoriel_commun    vocabulaire commun par colonne, -1 = manquant
  a2_commun.bootstrap_personnes          IC 95 % par reechantillonnage de personnes
  resultats/c7-stanford-reidentification.csv  top-1 par condition, deja calcule par
                                          c7_stanford.py : pas recalcule ici (machine
                                          chargee, deux runs llama.cpp en cours)

CE QUI EST NOUVEAU ICI : le test de symetrie vague 1 / vague 2 sur les cellules ou
l'humain a change de reponse, condition par condition.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_stanford_provenance.py
===========================================================================
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import bootstrap_personnes  # noqa: E402
from a30_commun import ecrire  # noqa: E402
from c7_stanford import charger_domaine, coder_categoriel_commun, VAGUE1, VAGUE2  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAINE = 20260912
N_BOOTSTRAP = 2000

# Conditions GSS testees pour la symetrie : les trois qui melangent enquete et/ou
# entretien, plus demographique et persona comme temoins (n'ont vu ni l'un ni l'autre).
CONDITIONS_SYMETRIE = ["composite", "enquete", "entretien", "demographique", "persona"]


def taux_symetrie(code_agent, code_v1, code_v2):
    """Sur les cellules ou v1 != v2 (les deux renseignees), taux d'accord de l'agent
    avec v1 et avec v2, par personne (pour le bootstrap), plus le total de cellules.

    Une cellule peut ne matcher ni v1 ni v2 (troisieme reponse) : les deux taux ne sont
    pas complementaires, c'est attendu.
    """
    change = (code_v1 >= 0) & (code_v2 >= 0) & (code_v1 != code_v2)
    agent_ok = code_agent >= 0
    match_v1 = (code_agent == code_v1) & change & agent_ok
    match_v2 = (code_agent == code_v2) & change & agent_ok

    n_change_pers = change.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        r_v1 = np.where(n_change_pers > 0, match_v1.sum(axis=1) / np.maximum(n_change_pers, 1), np.nan)
        r_v2 = np.where(n_change_pers > 0, match_v2.sum(axis=1) / np.maximum(n_change_pers, 1), np.nan)
    return r_v1, r_v2, int(change.sum())


def main():
    print(__doc__.split("=" * 75)[1], flush=True)

    ordre, items, tables, typ = charger_domaine("gss")
    assert typ == "categoriel"
    codes = coder_categoriel_commun(tables, items)
    code_v1, code_v2 = codes[VAGUE1], codes[VAGUE2]

    lignes = []
    for cond in CONDITIONS_SYMETRIE:
        r_v1, r_v2, n_cellules = taux_symetrie(codes[cond], code_v1, code_v2)
        m1, b1, h1 = bootstrap_personnes(r_v1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 10])
        m2, b2, h2 = bootstrap_personnes(r_v2, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 11])
        ecart = m1 - m2
        lignes.append({
            "condition": cond, "n_cellules_changees": n_cellules,
            "taux_suit_v1": m1, "taux_suit_v1_bas": b1, "taux_suit_v1_haut": h1,
            "taux_suit_v2": m2, "taux_suit_v2_bas": b2, "taux_suit_v2_haut": h2,
            "ecart_v1_moins_v2": ecart,
            "contamine": bool(abs(ecart) > 0.03),
        })
        print(f"{cond:15s} n_change={n_cellules:6d}  suit_v1={m1:.4f} [{b1:.4f};{h1:.4f}]  "
              f"suit_v2={m2:.4f} [{b2:.4f};{h2:.4f}]  ecart={ecart:+.4f}", flush=True)

    df = pd.DataFrame(lignes)
    ecrire(df, "c7-stanford-provenance-symetrie.csv")

    # --- decomposition par source, reprise sans recalcul ---
    reident = pd.read_csv(os.path.join(RACINE, "resultats", "c7-stanford-reidentification.csv"))
    gss = reident[reident.domaine == "gss"].set_index("condition")
    print("\ntop-1 par condition GSS (repris de c7-stanford-reidentification.csv, non recalcule) :",
          flush=True)
    for cond in ["composite", "entretien", "enquete", "demographique", "persona"]:
        row = gss.loc[cond]
        print(f"  {cond:15s} top1={row.top1:.4f} [{row.top1_bas:.4f};{row.top1_haut:.4f}]", flush=True)

    print("\nverdict de symetrie (ecart > 3 points = contamine) :", flush=True)
    print(df[["condition", "n_cellules_changees", "taux_suit_v1", "taux_suit_v2",
              "ecart_v1_moins_v2", "contamine"]].to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
