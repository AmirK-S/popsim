"""
a30_resin_twin : densite du sous graphe partisan a la ResIN, sur Twin-2K-500.

Ajout demande en cours de chantier a30. Repond a une question differente de celle des
autres scripts a30 : non plus « combien de variete a l'interieur d'un camp », mais
« a quel point les attitudes d'un camp sont elles reliees entre elles ». Les deux ne
disent pas la meme chose, et rien n'oblige a ce qu'elles aillent dans le meme sens : un
camp peut etre disperse et fortement structure.

METHODE, recopiee de resultats/a32-papier-diversite-droite.md section 2 et 5.3
-------------------------------------------------------------------------------
Noeud = une modalite de reponse a un item, pas un item. QID287, matrice de dix items sur
la meme echelle a cinq points, donne 50 noeuds.
Arete = coefficient phi entre les deux colonnes indicatrices, c'est a dire la
correlation de Pearson entre deux binaires. Les paires de modalites du meme item sont
exclues, elles sont mutuellement exclusives. Les phi negatifs sont ramenes a zero,
comme dans le notebook des auteurs.
Camp d'un noeud : la modalite est affectee au camp qui l'endosse le plus souvent, taux
d'endossement rapporte a l'effectif du camp, pour que le desequilibre 847 contre 540 ne
decide pas de l'affectation.
Densite d'un sous graphe : moyenne des poids d'arete sur les paires de noeuds du camp
appartenant a des items differents. Le nombre de noeuds du camp et le nombre de
modalites reellement employees sont rapportes a cote, faute de quoi une densite qui
bouge parce qu'un agent n'emploie jamais une modalite serait lue comme un resultat.

CE QUI N'EST PAS FAIT ICI, ET POURQUOI
--------------------------------------
Ni disposition a ressorts, ni ACP de rotation, ni figure de reseau. Le placement
Fruchterman Reingold ne sert dans les papiers d'origine qu'a produire l'image dont
l'asymetrie est constatee a l'oeil ; il n'entre dans aucune quantite mesuree. Le
reproduire ajouterait une source de variation aleatoire sans ajouter de mesure.

FAMILLE D'HYPOTHESES, ECRITE AVANT LES RESULTATS
------------------------------------------------
R1 : chez les humains, la densite du sous graphe republicain depasse celle du sous graphe
     democrate, ratio D/G > 1. C'est ce que Chen et ses coauteurs trouvent sur l'ANES de
     2000 a 2020, sauf en 2020.
R2 : la forme est stable dans le temps, le ratio de la vague 4 reproduit celui des
     vagues 1 a 3 sur les memes personnes.
R3 : les configurations d'agents ramenent ce ratio vers 1, c'est a dire effacent la
     difference de geometrie entre camps.
Trois tests, correction de Holm dans une famille de trois pour R1 et R2 ; R3 est lu sur
des intervalles apparies et non sur un p.

Le controle qui manque aux papiers d'origine est fait ici : les deux camps sont ramenes
au meme effectif avant toute comparaison de densite.

SORTIES : resultats/a30-resin-twin-densites.csv, a30-resin-twin-noeuds.csv

Usage : .venv/bin/python analyses/a30_resin_twin.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
import a9_commun as T  # noqa: E402

ITEMS = ["QID287_1", "QID287_2", "QID287_3", "QID287_4", "QID287_5", "QID287_6",
         "QID287_7", "QID287_10", "QID287_11", "QID287_12"]
MODALITES = [1, 2, 3, 4, 5]   # 1 Strongly oppose ... 5 Strongly support
NEUTRE = 3


def disjonctif(df):
    """Encodage disjonctif : une colonne binaire par couple (item, modalite).

    Retourne la matrice binaire (personnes x 50), l'item de chaque noeud et sa modalite.
    Une cellule manquante donne zero partout pour cet item, ce qui retire la personne du
    numerateur de toutes les modalites de cet item sans la retirer du reseau entier.
    """
    cols, item_de, mod_de = [], [], []
    for it in ITEMS:
        v = pd.to_numeric(df[it], errors="coerce").to_numpy(dtype=float)
        for m in MODALITES:
            cols.append((v == m).astype(np.float64))
            item_de.append(it)
            mod_de.append(m)
    return np.column_stack(cols), np.array(item_de), np.array(mod_de)


def reseau(X, item_de):
    """Matrice de phi, negatifs ramenes a zero, paires du meme item annulees.

    phi entre deux binaires est exactement la correlation de Pearson entre les deux
    colonnes ; on la calcule donc en une seule operation matricielle.
    """
    n = X.shape[0]
    mu = X.mean(axis=0)
    sd = X.std(axis=0)
    ok = sd > 1e-12
    Z = np.zeros_like(X)
    Z[:, ok] = (X[:, ok] - mu[ok]) / sd[ok]
    W = (Z.T @ Z) / n
    W[~np.isfinite(W)] = 0.0
    W = np.maximum(W, 0.0)
    meme = item_de[:, None] == item_de[None, :]
    W[meme] = 0.0
    return W, ok


def affecter_noeuds(X, masque_a, masque_b):
    """Camp de chaque noeud : celui dont le taux d'endossement est le plus eleve.

    On compare P(modalite | droite) a P(modalite | gauche), et non les effectifs bruts :
    avec 847 democrates contre 540 republicains, comparer des effectifs affecterait
    presque tous les noeuds au camp le plus nombreux.
    """
    pa = X[masque_a].mean(axis=0)
    pb = X[masque_b].mean(axis=0)
    return np.where(pa >= pb, "droite", "gauche"), pa, pb


def densite(W, noeuds, item_de):
    """Moyenne des poids d'arete sur les paires de noeuds d'items differents."""
    idx = np.flatnonzero(noeuds)
    if len(idx) < 2:
        return np.nan, 0, 0
    sub = W[np.ix_(idx, idx)]
    eligible = item_de[idx][:, None] != item_de[idx][None, :]
    n_paires = int(eligible.sum()) // 2
    if n_paires == 0:
        return np.nan, len(idx), 0
    return float(sub[eligible].sum() / eligible.sum()), len(idx), n_paires


def mesurer(X, item_de, noeuds_d, noeuds_g, lignes):
    """Densites des deux sous graphes, sur un sous ensemble de personnes donne."""
    sel = np.zeros(X.shape[0], dtype=bool)
    sel[lignes] = True
    W, employe = reseau(X[sel], item_de)
    dd, nd, _ = densite(W, noeuds_d, item_de)
    dg, ng, _ = densite(W, noeuds_g, item_de)
    return {"densite_droite": dd, "densite_gauche": dg,
            "ratio_droite_gauche": dd / dg if dg else np.nan,
            "noeuds_droite": nd, "noeuds_gauche": ng,
            "modalites_employees": int(employe.sum())}


def lignes_appariees(masque_a, masque_b, taille, rng):
    """Un tirage sans remise de meme effectif dans les deux camps."""
    ia = rng.choice(np.flatnonzero(masque_a), size=taille, replace=False)
    ib = rng.choice(np.flatnonzero(masque_b), size=taille, replace=False)
    return np.concatenate([ia, ib])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirages", type=int, default=200)
    args = ap.parse_args()
    rng = np.random.default_rng(C.GRAINE)

    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    pid = list(w13.index)
    camps = C.camps_twin(w13)
    ma = camps["parti3"] == "droite"      # republicains
    mb = camps["parti3"] == "gauche"      # democrates
    print(f"parti : {int(ma.sum())} republicains, {int(mb.sum())} democrates", flush=True)
    taille = int(min(ma.sum(), mb.sum()))

    # Le partage des noeuds entre les deux camps est fixe une fois pour toutes sur les
    # humains des vagues 1 a 3. Toutes les conditions sont ensuite lues sur EXACTEMENT
    # les memes deux ensembles de noeuds : sinon un agent qui deplace une modalite d'un
    # camp a l'autre changerait la densite des deux sous graphes a la fois, et le ratio
    # ne serait plus comparable d'une ligne a l'autre.
    X0, item_de, mod_de = disjonctif(w13)
    camp_noeud, pa, pb = affecter_noeuds(X0, ma, mb)
    C.ecrire(pd.DataFrame({"item": item_de, "modalite": mod_de, "camp": camp_noeud,
                           "taux_droite": pa, "taux_gauche": pb,
                           "neutre": mod_de == NEUTRE}), "a30-resin-twin-noeuds.csv")
    n_neutres_droite = int(((mod_de == NEUTRE) & (camp_noeud == "droite")).sum())
    print(f"noeuds : {int((camp_noeud == 'droite').sum())} a droite, "
          f"{int((camp_noeud == 'gauche').sum())} a gauche ; "
          f"{n_neutres_droite} des 10 modalites neutres tombent a droite", flush=True)

    # Trois partages de noeuds, parce que la densite moyenne d'un sous graphe depend du
    # nombre de noeuds qu'on y met, et que le partage brut est tres desequilibre.
    #   « brut »        : tel que la regle d'endossement le donne, 33 contre 17.
    #   « egalise »     : les K noeuds les plus caracteristiques de chaque camp, K etant
    #                     le minimum des deux effectifs, pour que les deux sous graphes
    #                     aient exactement la meme taille.
    #   « sans neutre » : le partage brut prive des dix modalites « ni l'un ni l'autre »,
    #                     qui tombent presque toutes du meme cote et gonflent ce cote.
    ecart = pa - pb
    nd_brut, ng_brut = camp_noeud == "droite", camp_noeud == "gauche"
    k = int(min(nd_brut.sum(), ng_brut.sum()))
    ordre_d = np.argsort(-ecart)
    ordre_g = np.argsort(ecart)
    nd_eg = np.zeros(len(ecart), dtype=bool); nd_eg[ordre_d[:k]] = True
    ng_eg = np.zeros(len(ecart), dtype=bool); ng_eg[ordre_g[:k]] = True
    pas_neutre = mod_de != NEUTRE
    PARTAGES = {
        "brut": (nd_brut, ng_brut),
        "egalise": (nd_eg, ng_eg),
        "sans neutre": (nd_brut & pas_neutre, ng_brut & pas_neutre),
    }
    for nom, (a, b) in PARTAGES.items():
        print(f"partage {nom} : {int(a.sum())} noeuds a droite, {int(b.sum())} a gauche",
              flush=True)

    conditions = {"humains vagues 1 a 3": w13,
                  "humains vague 4": w4.reindex(pid)}
    for nom, fichier in T.configs_llm_disponibles().items():
        if not nom.startswith("gpt41mini"):
            continue
        conditions[nom] = T.charger_llm(fichier).reindex(pid)

    lignes = []
    for nom, df in conditions.items():
        manquantes = [c for c in ITEMS if c not in df.columns]
        if manquantes:
            print(f"  {nom} : items absents, ignore", flush=True)
            continue
        X, _, _ = disjonctif(df)
        # Un seul jeu de tirages a effectifs egaux, partage par les trois partages de
        # noeuds : les trois lignes d'une meme condition portent ainsi sur exactement
        # les memes personnes.
        tirs = [lignes_appariees(ma, mb, taille, rng) for _ in range(args.tirages)]
        for partage, (a, b) in PARTAGES.items():
            base = mesurer(X, item_de, a, b, np.flatnonzero(ma | mb))
            tir = [mesurer(X, item_de, a, b, t) for t in tirs]
            r = np.array([t["ratio_droite_gauche"] for t in tir], dtype=float)
            r = r[np.isfinite(r)]
            lignes.append({
                "condition": nom, "partage_des_noeuds": partage, **base,
                "ratio_effectifs_egaux": float(np.mean(r)) if len(r) else np.nan,
                "ic_bas": float(np.percentile(r, 2.5)) if len(r) else np.nan,
                "ic_haut": float(np.percentile(r, 97.5)) if len(r) else np.nan,
                "densite_droite_effectifs_egaux":
                    float(np.mean([t["densite_droite"] for t in tir])),
                "densite_gauche_effectifs_egaux":
                    float(np.mean([t["densite_gauche"] for t in tir])),
                "taille_par_camp": taille, "tirages": args.tirages,
            })
            print(f"{nom:30s} {partage:12s} ratio "
                  f"{lignes[-1]['ratio_effectifs_egaux']:.4f} "
                  f"[{lignes[-1]['ic_bas']:.4f} ; {lignes[-1]['ic_haut']:.4f}] "
                  f"densites {lignes[-1]['densite_droite_effectifs_egaux']:.4f} / "
                  f"{lignes[-1]['densite_gauche_effectifs_egaux']:.4f} "
                  f"modalites {base['modalites_employees']}/50", flush=True)

    df = pd.DataFrame(lignes)
    C.ecrire(df, "a30-resin-twin-densites.csv")


if __name__ == "__main__":
    main()
