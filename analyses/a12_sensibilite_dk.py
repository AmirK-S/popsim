"""
a12_sensibilite_dk : le "ne sait pas" est il en train de gonfler la consistance du panel ?

Statut : script d'exploration, pas du code de production. Aucun appel de modele.

Le probleme. Dans l'archive de Stanford il n'y a aucune cellule manquante : 1 052 x 177
reponses, toutes remplies. Dans le GSS de terrain il y a des "ne sait pas" (`d`), des
"pas de reponse" (`n`) et des "non pose" (`i`, ballot ou filtre). Le calcul principal de
a12 les traite tous en manquants, ce qui **retire du calcul les reponses les plus fragiles**
et tire donc la consistance du panel vers le haut. Ce script mesure de combien, en
comptant le "ne sait pas" comme une modalite a part entiere.

`i` reste un manquant dans les deux variantes : c'est une question non posee, pas une
reponse. Seuls `d` et `n` changent de statut.

Sortie : resultats/a12-sensibilite-dk.csv

Usage : .venv/bin/python analyses/a12_sensibilite_dk.py
"""

import os
import sys

import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a12_retest_delai import (MIN_ITEMS_INDIVIDU, PANEL, PANELS, SORTIE,  # noqa: E402
                              colonnes_vague, items_stanford, serie_fusionnee)

# Codes manquants etendus de Stata rencontres dans les quatre panels, releves par
# comptage direct : i, d, n, a, c, s, x, y.
#   i = inapplicable, la question n'a pas ete posee a cette personne (ballot ou filtre)
#   x, y = non disponible dans cette annee ou dans cette version du fichier
#   c = code residuel du fichier, rare, non documente dans les etiquettes de valeur
# Ces quatre la ne sont jamais des reponses : ils restent manquants dans les deux variantes.
NON_POSE = {"i", "x", "y", "c"}
#   d = ne sait pas, n = pas de reponse, a = refus, s = passe sur le web
# Ce sont des non reponses du repondant. Dans la variante haute elles deviennent une
# modalite unique "NR" : un "ne sait pas" repete deux fois compte alors comme une
# reponse stable, ce qui est la lecture la plus genereuse pour le panel.
INDECIS = {"d", "n", "a", "s"}
NR = "NR"


def charger(nom, items, compter_dk):
    cfg = PANELS[nom]
    chemin = os.path.join(PANEL, cfg["fichier"])
    _, meta = pyreadstat.read_dta(chemin, metadataonly=True, encoding="latin1")
    colonnes = {c.lower(): c for c in meta.column_names}
    besoin, plan = set(), {}
    for annee, suf in cfg["vagues"].items():
        plan[annee] = {}
        for it in items:
            cols = colonnes_vague(it, suf, colonnes)
            if cols:
                plan[annee][it] = cols
                besoin.update(colonnes[c] for c in cols)
    df, _ = pyreadstat.read_dta(chemin, usecols=sorted(besoin), encoding="latin1",
                                user_missing=True)
    df.columns = [c.lower() for c in df.columns]
    # Les codes manquants sont neutralises avant la fusion de ballot, sans quoi la fusion
    # prendrait un "non pose" pour une reponse. Tout code d'une seule lettre inconnu des
    # deux listes est traite comme manquant : c'est le choix prudent.
    def recoder(v):
        if not isinstance(v, str) or len(v) != 1:
            return v
        if compter_dk and v in INDECIS:
            return NR
        return np.nan

    df = df.map(recoder)
    mat = {}
    for annee in cfg["vagues"]:
        m = np.full((len(df), len(items)), np.nan, dtype=object)
        for j, it in enumerate(items):
            cols = plan[annee].get(it)
            if cols:
                m[:, j], _ = serie_fusionnee(df, cols)
        mat[annee] = m
    return mat


def consistance(m_a, m_b):
    ok = np.array([[not (v is None or (isinstance(v, float) and np.isnan(v)))
                    for v in ligne] for ligne in m_a])
    ok &= np.array([[not (v is None or (isinstance(v, float) and np.isnan(v)))
                     for v in ligne] for ligne in m_b])
    egal = (m_a == m_b) & ok
    n = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        pp = np.where(n >= MIN_ITEMS_INDIVIDU, egal.sum(axis=1) / np.maximum(n, 1), np.nan)
    return pp


def main():
    items = items_stanford()
    lignes = []
    for compter_dk in (False, True):
        libelle = "DK compte comme modalite" if compter_dk else "DK traite en manquant"
        for nom in PANELS:
            mat = charger(nom, items, compter_dk)
            for a, b, ecart in PANELS[nom]["paires"]:
                pp = consistance(mat[a], mat[b])
                lignes.append({"variante": libelle, "panel": nom, "paire": f"{a}-{b}",
                               "ecart_annees": ecart,
                               "n_personnes": int(np.isfinite(pp).sum()),
                               "consistance": float(np.nanmean(pp))})
    t = pd.DataFrame(lignes)
    agr = (t.groupby(["variante", "ecart_annees"])
           .apply(lambda g: pd.Series({
               "n_personnes": g["n_personnes"].sum(),
               "consistance": np.average(g["consistance"], weights=g["n_personnes"])}),
               include_groups=False).reset_index())
    t = pd.concat([t, agr.assign(panel="mise en commun", paire="-")], ignore_index=True)
    t.to_csv(os.path.join(SORTIE, "a12-sensibilite-dk.csv"), index=False)
    print(agr.to_string(index=False))


if __name__ == "__main__":
    main()
