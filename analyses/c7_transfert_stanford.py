"""
c7_transfert_stanford : le canal inter-jumeaux (Twin-2K-500) se replique-t-il sur Stanford ?

===========================================================================
PREENREGISTREMENT : resultats/c7-transfert-stanford-preenregistrement.md, ecrit le
12 septembre 2026, AVANT ce fichier et avant tout calcul.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (archive Stanford, data/osf-t6g7k-
stanford/). Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant
(« participant_XXXX ») ni aucun appariement individuel : seuls des taux agreges sortent
dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  c7_stanford.charger_domaine            vague1/vague2/conditions, meme ordre par email
  c7_stanford.coder_categoriel_commun    vocabulaire commun par colonne, -1 = manquant
  c7_stanford.coder_continu_commun       valeurs numeriques brutes, memes colonnes
  c7_stanford.accord_categoriel          1 - Hamming
  c7_stanford.accord_continu             - distance euclidienne z-scoree sur le bassin
  c7_stanford.rangs_depuis_accord        rang du vrai repondant, candidats melanges
  c7_stanford.resume_taux                moyenne + IC95 par a2_commun.bootstrap_personnes
  c7_stanford.graine_domaine             entier stable a partir d'une chaine
  c7_transfert.tirer_decoys              decoy = une AUTRE personne du meme segment S_gra
  a30_commun.cellules_gss, ecrire

CE QUI EST NOUVEAU ICI : l'attaque entretien <-> enquete (au lieu de vague1 -> condition),
sur les trois domaines (gss/econ/bigfive), plus son controle anti-artefact par decoy
(au lieu de la restriction au segment utilisee dans c7_stanford.rang_dans_segment, qui
mesure autre chose : ici on garde le bassin entier et on change seulement la cible).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_transfert_stanford.py
===========================================================================
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a30_commun import cellules_gss, ecrire  # noqa: E402
from c7_stanford import (  # noqa: E402
    DOMAINES, DEMO_COND, GRAINE, DEMO_CSV,
    charger_domaine, coder_categoriel_commun, coder_continu_commun,
    accord_categoriel, accord_continu, rangs_depuis_accord, resume_taux, graine_domaine,
)
from c7_transfert import tirer_decoys  # noqa: E402

ENTRETIEN = "entretien"
ENQUETE = "enquete"


def construire_accords(nom_domaine, tables, items, typ):
    """Un accord(test, pool) par paire (source, cible) parmi entretien/enquete/demo,
    directement comparable a c7_stanford (meme fonctions, memes conventions)."""
    if typ == "categoriel":
        codes = coder_categoriel_commun(tables, items)
        def accord(src, dst):
            return accord_categoriel(codes[src], codes[dst])
    else:
        valeurs = coder_continu_commun(tables, items)
        def accord(src, dst):
            return accord_continu(valeurs[src], valeurs[dst])
    return accord


def ligne_attaque(nom_domaine, direction, src, dst, accord_fn, seg, rng_decoy, n):
    accord = accord_fn(src, dst)
    vrai = np.arange(n)
    rng = np.random.default_rng([GRAINE, graine_domaine(f"{nom_domaine}|{direction}|{src}->{dst}")])
    rang, top1, top10 = rangs_depuis_accord(accord, vrai, rng)
    m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, graine_domaine(nom_domaine + direction + "1")])
    m_t10, b_t10, h_t10 = resume_taux(top10, [GRAINE, graine_domaine(nom_domaine + direction + "10")])

    decoys = tirer_decoys(np.arange(n), np.arange(n), seg, rng_decoy)
    valide = decoys >= 0
    if valide.sum() >= 5:
        rang_c, top1_c, _ = rangs_depuis_accord(accord[valide], decoys[valide], rng)
        m_t1c, b_t1c, h_t1c = resume_taux(top1_c, [GRAINE, graine_domaine(nom_domaine + direction + "c")])
    else:
        m_t1c = b_t1c = h_t1c = np.nan

    return {
        "domaine": nom_domaine, "direction": direction, "n_items": len(items_cache[nom_domaine]),
        "n": n, "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang)), "top1_hasard": 1.0 / n,
        "top1_controle": m_t1c, "top1_controle_bas": b_t1c, "top1_controle_haut": h_t1c,
        "n_controle": int(valide.sum()),
    }


items_cache = {}


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    demo = pd.read_csv(DEMO_CSV)

    lignes = []
    for nom_domaine, spec in DOMAINES.items():
        ordre, items, tables, typ = charger_domaine(nom_domaine)
        items_cache[nom_domaine] = items
        n = len(ordre)
        d = demo.set_index("email").loc[ordre]
        seg_str = cellules_gss(d[["gender", "race", "age", "education"]].to_numpy(dtype=object),
                              ["gender", "race", "age", "education"])
        # tirer_decoys (repris de c7_transfert) attend un code entier, -1 = segment
        # inconnu ; cellules_gss renvoie des chaines (jamais manquantes ici) -> factorize.
        seg, _ = pd.factorize(seg_str)
        accord_fn = construire_accords(nom_domaine, tables, items, typ)
        rng_decoy = np.random.default_rng([GRAINE, graine_domaine(nom_domaine + "|decoy")])

        print(f"\n=== {nom_domaine} : {n} personnes, {len(items)} items ({typ}) ===", flush=True)
        paires = [
            ("entretien->enquete", ENTRETIEN, ENQUETE),
            ("enquete->entretien", ENQUETE, ENTRETIEN),
            ("demo->enquete", DEMO_COND, ENQUETE),
            ("demo->entretien", DEMO_COND, ENTRETIEN),
        ]
        for direction, src, dst in paires:
            ligne = ligne_attaque(nom_domaine, direction, src, dst, accord_fn, seg, rng_decoy, n)
            lignes.append(ligne)
            print(f"{nom_domaine:16s} {direction:20s} top1={ligne['top1']:.4f} "
                  f"[{ligne['top1_bas']:.4f};{ligne['top1_haut']:.4f}] "
                  f"top10={ligne['top10']:.4f} controle={ligne['top1_controle']:.4f} "
                  f"rang_med={ligne['rang_median']:.1f}/{n}", flush=True)

    df = pd.DataFrame(lignes)
    ecrire(df, "c7-transfert-stanford-attaque.csv")

    print("\n--- verdict preenregistre ---", flush=True)
    gss = df[df.domaine == "gss"]
    for direction in ["entretien->enquete", "enquete->entretien"]:
        row = gss[gss.direction == direction].iloc[0]
        demo_dir = "demo->enquete" if direction == "entretien->enquete" else "demo->entretien"
        demo_row = gss[gss.direction == demo_dir].iloc[0]
        print(f"GSS {direction} : top1={row.top1:.4f}, demo={demo_row.top1:.4f}, "
              f"controle={row.top1_controle:.4f}", flush=True)


if __name__ == "__main__":
    main()
