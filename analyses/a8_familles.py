"""
a8_familles : le decoupage par famille d'items, regime "question jamais posee dans ce domaine".

Repond a la limite 7 du rapport a2 : "le decoupage en blocs d'items du GSS est aleatoire,
donc un bloc secret peut contenir plusieurs items d'une meme famille tandis que ses
cousins restent dans le contexte. B2 en profite." Ici on retire la famille entiere du
contexte ET on la predit. B2 n'a plus les cousins de l'item, seulement le reste du
questionnaire. C'est le test existentiel A4 du BRAINSTORM, cote statistique.

Question a laquelle ce script repond : quand on retire toute la famille, les agents de
Stanford battent ils B2 ?

Sur Twin-2K-500 le regime est deja en place sans qu'on l'ait voulu, et c'est un fait a
verifier avant toute lecture : le contexte des vagues 1 a 3 ne contient aucun item des
blocs de la vague 4, puisque a2 retire du contexte toutes les colonnes reposees et que ces
blocs sont reposes en entier. Le script le mesure et le dit. Il ajoute donc, faute de
famille a retirer, l'ablation des blocs de contexte un a un.

Entree  : data/osf-t6g7k-stanford, data/twin2k500.
Sortie  : resultats/a8-familles-gss.csv, resultats/a8-familles-twin.csv,
          resultats/a8-familles-contexte-twin.csv.

Aucun appel de modele. Duree : environ dix minutes.

Usage : .venv/bin/python analyses/a8_familles.py
"""

import time
from collections import Counter

import numpy as np

import a8_commun as C
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, distance_hamming, en_codes,
                       encodeur_demographies, est_manquant)
import a2_baselines_gss as G
import a2_baselines_twin as T


def plancher_uniforme(y, cols):
    """Exactitude d'un tirage uniforme sur les modalites declarees, en esperance."""
    vals = []
    for j in cols:
        v = [x for x in y[:, j] if not est_manquant(x)]
        if not v:
            continue
        cpt = Counter(v)
        vals.append(sum((c / len(v)) * (1 / len(cpt)) for c in cpt.values()))
    return float(np.mean(vals)) if vals else float("nan")


def ligne(famille, methode, pred, y, cols, masque=None, extra=None):
    moy, bas, haut = C.exactitude_sur(pred, y, cols, masque)
    div = C.diversite_sur(pred, y, cols)
    d = {
        "famille": famille, "methode": methode, "n_items": len(cols),
        "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
        "part_diversite_humaine": div["part_diversite_humaine"],
        "accord_par_paires": div["accord_par_paires"],
    }
    if extra:
        d.update(extra)
    return d


# ---------------------------------------------------------------------------
# GSS
# ---------------------------------------------------------------------------

def gss():
    g = C.charger_gss()
    y, items, x = g["y1"], g["items"], g["x"]
    n, m = y.shape
    plis, blocs = C.grille_gss(n, m)
    codes = en_codes(y)
    index = {it: j for j, it in enumerate(items)}
    familles = {nom: [index[i] for i in membres if i in index]
                for nom, membres in G.FAMILLES.items()}
    tous = sorted({j for cols in familles.values() for j in cols})

    rng = np.random.default_rng(C.GRAINE)
    p_b0m = np.empty((n, m), dtype=object)
    p_b0t = np.empty((n, m), dtype=object)
    p_b1 = np.empty((n, m), dtype=object)
    p_b1t = np.empty((n, m), dtype=object)
    p_b2_alea = np.empty((n, m), dtype=object)
    p_b2_fam = np.empty((n, m), dtype=object)
    p_b2_fam_t = np.empty((n, m), dtype=object)

    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in tous:
            p_b0m[np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            p_b0t[np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            p_b1[np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            p_b1t[np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]
        # B2 aleatoire : le decoupage en blocs de a2, rejoue a l'identique.
        for bloc in blocs:
            contexte = np.setdiff1d(np.arange(m), bloc)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in bloc:
                if j in tous:
                    p_b2_alea[np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng)[:, None]
        # B2 famille : la famille entiere sort du contexte et sert de cible.
        for nom, cols in familles.items():
            contexte = np.setdiff1d(np.arange(m), cols)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in cols:
                p_b2_fam[np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng)[:, None]
                p_b2_fam_t[np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)

    agents = C.charger_agents_gss(items)
    lignes = []
    ensembles = list(familles.items()) + [("toutes familles reunies", tous)]
    for nom, cols in ensembles:
        extra = {"plancher_uniforme": plancher_uniforme(y, cols)}
        lignes.append(ligne(nom, "B2 famille retiree (argmax)", p_b2_fam, y, cols, extra=extra))
        lignes.append(ligne(nom, "B2 famille retiree (tirage)", p_b2_fam_t, y, cols, extra=extra))
        lignes.append(ligne(nom, "B2 blocs aleatoires (a2)", p_b2_alea, y, cols, extra=extra))
        lignes.append(ligne(nom, "B1 argmax", p_b1, y, cols, extra=extra))
        lignes.append(ligne(nom, "B1 tirage", p_b1t, y, cols, extra=extra))
        lignes.append(ligne(nom, "B0 mode", p_b0m, y, cols, extra=extra))
        lignes.append(ligne(nom, "B0 tirage", p_b0t, y, cols, extra=extra))
        for libelle, mat in agents.items():
            lignes.append(ligne(nom, libelle, mat, y, cols, extra=extra))
        lignes.append(ligne(nom, "humains reinterroges", g["y2"], y, cols, extra=extra))
    return lignes


# ---------------------------------------------------------------------------
# Twin-2K-500
# ---------------------------------------------------------------------------

BLOCS_CONTEXTE = ["Personality", "Economic preferences", "Cognitive tests", "Demographics"]


def twin():
    d0 = C.charger_twin()
    y, ctx, x = d0["y"], d0["ctx"], d0["x"]
    n, m = y.shape
    plis = C.plis_twin(n)
    masque = np.array([[not est_manquant(v) for v in l] for l in y])
    cat = d0["catalogue"]
    blocs_ctx = np.array([cat[c]["BlockName"].strip() for c in d0["contexte"]])
    blocs_cible = d0["blocs_cibles"]
    cibles = d0["cibles"]

    # Fait a verifier avant toute lecture : aucun item de contexte n'appartient a un bloc
    # de la vague 4. La famille cible est donc deja absente du contexte dans a2.
    familles_cible = set(blocs_cible.values())
    recouvrement = sorted(set(blocs_ctx) & familles_cible)
    print(f"  blocs de contexte : {sorted(set(blocs_ctx))}")
    print(f"  recouvrement entre blocs de contexte et blocs cibles : {recouvrement or 'aucun'}")

    grandes = T.FAMILLES_JAMAIS_POSEES
    index = {c: j for j, c in enumerate(cibles)}
    familles = {f: [index[c] for c in cibles if blocs_cible[c] == f] for f in grandes}
    reste = [index[c] for c in cibles if blocs_cible[c] not in grandes]
    familles["autres experiences (blocs a 1 a 6 items)"] = reste
    familles["tous les items"] = list(range(m))

    variantes = {"contexte complet": None}
    for b in BLOCS_CONTEXTE[:3]:
        variantes[f"contexte sans {b}"] = [i for i, v in enumerate(blocs_ctx) if v != b]
    variantes["contexte demographies seules"] = [i for i, v in enumerate(blocs_ctx)
                                                 if v == "Demographics"]

    rng = np.random.default_rng(C.GRAINE)
    p_b0m = np.empty((n, m), dtype=object)
    p_b0t = np.empty((n, m), dtype=object)
    p_b1 = np.empty((n, m), dtype=object)
    p_b2 = {v: np.empty((n, m), dtype=object) for v in variantes}
    p_b2_tirage = np.empty((n, m), dtype=object)

    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            p_b0m[np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            p_b0t[np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            p_b1[np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
        for nom, garde in variantes.items():
            sous = ctx if garde is None else ctx[:, garde]
            codes = en_codes(sous)
            dist = distance_hamming(codes[te], codes[tr])
            for j in range(m):
                p_b2[nom][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2, rng)[:, None]
                if garde is None:
                    p_b2_tirage[np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2,
                                                              rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)

    llm = C.charger_llm_twin(d0)
    yn = C.cible_twin_numerique(d0)
    lignes, lignes_ctx = [], []
    for nom, cols in familles.items():
        extra = {"plancher_uniforme": plancher_uniforme(y, cols)}
        lignes.append(ligne(nom, "B2 contexte complet (a2)", p_b2["contexte complet"],
                            y, cols, masque, extra))
        lignes.append(ligne(nom, "B2 contexte complet (tirage)", p_b2_tirage,
                            y, cols, masque, extra))
        lignes.append(ligne(nom, "B2 contexte demographies seules",
                            p_b2["contexte demographies seules"], y, cols, masque, extra))
        lignes.append(ligne(nom, "B1 argmax", p_b1, y, cols, masque, extra))
        lignes.append(ligne(nom, "B0 mode", p_b0m, y, cols, masque, extra))
        lignes.append(ligne(nom, "B0 tirage", p_b0t, y, cols, masque, extra))
        for libelle, spec in llm.items():
            mq = masque & spec["personnes"][:, None]
            lignes.append(ligne(nom, libelle, spec["matrice"], yn, cols, mq,
                                dict(extra, n_personnes=spec["n_personnes"])))
        lignes.append(ligne(nom, "humains retest vagues 1 a 3",
                            np.where(masque, d0["y_retest"], None), y, cols, masque, extra))
        for v in variantes:
            lignes_ctx.append(ligne(nom, f"B2 {v}", p_b2[v], y, cols, masque, extra))
    return lignes, lignes_ctx


def main():
    t0 = time.time()
    print("GSS : familles retirees du contexte et predites")
    lg = gss()
    C.ecrire_csv(lg, "a8-familles-gss.csv")

    print("\nTwin-2K-500 : familles et ablations de contexte")
    lt, lc = twin()
    C.ecrire_csv(lt, "a8-familles-twin.csv")
    C.ecrire_csv(lc, "a8-familles-contexte-twin.csv")
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
