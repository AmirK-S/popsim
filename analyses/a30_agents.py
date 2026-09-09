"""
a30_agents : la variete interne des camps chez les agents, volet 3 de a30.

La question : une population simulee reproduit elle le rapport de variete interne entre
le camp de droite et le camp de gauche mesure chez les vrais humains, et ecrase t elle
davantage le camp le plus varie ?

Ce qui est mesure, sur exactement les memes camps, les memes items et le meme estimateur
que le volet 1 :
  - le rapport droite sur gauche de chaque population simulee ;
  - l'ecrasement camp par camp, c'est a dire la dispersion interne de la population
    simulee divisee par celle des humains DANS LE MEME CAMP ;
  - la difference d'ecrasement entre les deux camps, qui dit si la simulation rabote
    plus fort la ou il y a plus a raboter.

Populations : les six conditions du paquet de Stanford, nos deux regimes locaux C2
(avec etiquette ideologique) et C3 (sans), les cinq predicteurs statistiques de a2 et
a28, la vague 2 humaine comme plancher de bruit, et du cote Twin-2K-500 les treize
configurations d'agents publiees par les auteurs, dont default et demo_only.

C2 et C3 ne couvrent que 150 personnes : toutes les lignes qui les concernent sont
recalculees en restreignant les humains et les autres conditions aux memes 150.

FAMILLE D'HYPOTHESES, ECRITE AVANT LES RESULTATS
------------------------------------------------
A1 : le rapport droite sur gauche des agents differe de celui des humains.
A2 : l'ecrasement est plus fort dans le camp de droite, le plus varie chez les humains.
A3 : la presence de l'etiquette ideologique dans l'invite change ce rapport ; comparaison
     appariee C2 contre C3 sur les memes 150 personnes, et v8 contre v6, et agents
     enquete (sans etiquette) contre agents composite.
Correction de Holm dans chaque famille de tests.

SORTIES : resultats/a30-agents-gss.csv, a30-agents-gss-150.csv, a30-agents-twin.csv,
          a30-agents-contrastes.csv

Usage : .venv/bin/python analyses/a30_agents.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
import a9_commun as T  # noqa: E402
from a28_commun import charger_tout, ORDRE_METHODES  # noqa: E402
from a25_commun import options_par_item  # noqa: E402


def mesures_camp(ind, masques, gardes, mesure="gs"):
    """Dispersion agregee de chaque camp sur un jeu d'items fixe."""
    return {c: float(C.agreger(C.mesures(ind.tables(C.poids_plein(m)))[mesure],
                               gardes)[0])
            for c, m in masques.items()}


def ligne_condition(nom, ind, masques, gardes, ref, rng, boot, perm):
    """Une ligne de resultat : dispersion par camp, rapport, ecrasement par camp."""
    v = mesures_camp(ind, masques, gardes)
    r = C.contraste(ind, masques["droite"], masques["gauche"], gardes, rng, boot, perm)
    lig = {"condition": nom, "n_items": int(gardes.sum()),
           "gs_gauche": v["gauche"], "gs_centre": v["centre"], "gs_droite": v["droite"],
           "ratio_droite_gauche": r["ratio"], "ic_bas": r["ic_bas"],
           "ic_haut": r["ic_haut"], "p_permutation": r["p"]}
    if ref is not None:
        for c in ("gauche", "centre", "droite"):
            lig["ecrasement_" + c] = v[c] / ref[c] if ref[c] else np.nan
        lig["ecrasement_droite_moins_gauche"] = (lig["ecrasement_droite"]
                                                 - lig["ecrasement_gauche"])
    return lig


# ---------------------------------------------------------------------------
# GSS
# ---------------------------------------------------------------------------

def volet_gss(args, rng):
    paq = charger_tout(args.cache, args.cache_foret)
    ids, items, y1, M = paq["ids"], paq["items"], paq["y1"], paq["M"]
    lignes150 = paq["lignes150"]
    options = options_par_item(C.RACINE)
    camps = C.camps_gss(paq["x"], paq["attributs"])
    masques = {c: (camps["bloc3"] == c) for c in ("gauche", "centre", "droite")}

    codes_h, ks = C.coder_gss(y1, items, options)
    ind_h = C.Indicatrice(codes_h, ks)
    gardes = C.masque_items(ind_h, masques["droite"], masques["gauche"],
                            np.ones(len(items), dtype=bool))
    ref = mesures_camp(ind_h, masques, gardes)
    print(f"humains vague 1 : {ref}", flush=True)

    lignes = [ligne_condition("humains vague 1", ind_h, masques, gardes, ref, rng,
                              args.boot, args.perm)]
    inds = {"humains vague 1": ind_h}
    for nom in ORDRE_METHODES:
        if nom not in M:
            continue
        codes, _ = C.coder_gss(np.asarray(M[nom], dtype=object), items, options)
        ind = C.Indicatrice(codes, ks)
        inds[nom] = ind
        if nom in ("C2", "C3"):
            continue  # traites separement sur les 150 personnes
        lignes.append(ligne_condition(nom, ind, masques, gardes, ref, rng,
                                      args.boot, args.perm))
    df = pd.DataFrame(lignes)
    df["p_holm"] = C.holm(df["p_permutation"].fillna(1.0).values)
    C.ecrire(df, "a30-agents-gss.csv")
    print(df[["condition", "gs_gauche", "gs_droite", "ratio_droite_gauche",
              "ic_bas", "ic_haut", "ecrasement_gauche", "ecrasement_droite"]]
          .to_string(index=False), flush=True)

    # ------------------------------------------------- restriction aux 150 personnes
    # C2 et C3 n'existent que la. Les humains et toutes les autres conditions sont
    # restreintes aux memes 150 lignes, sans quoi la comparaison melangerait un effet de
    # condition et un effet d'echantillon.
    m150 = np.zeros(len(ids), dtype=bool)
    m150[lignes150] = True
    masques150 = {c: (masques[c] & m150) for c in masques}
    print({c: int(m.sum()) for c, m in masques150.items()}, flush=True)
    gardes150 = C.masque_items(ind_h, masques150["droite"], masques150["gauche"],
                               np.ones(len(items), dtype=bool), n_min=15)
    ref150 = mesures_camp(ind_h, masques150, gardes150)
    l2 = []
    for nom, ind in inds.items():
        l2.append(ligne_condition(nom, ind, masques150, gardes150, ref150, rng,
                                  args.boot, args.perm))
    df2 = pd.DataFrame(l2)
    df2["p_holm"] = C.holm(df2["p_permutation"].fillna(1.0).values)
    C.ecrire(df2, "a30-agents-gss-150.csv")

    # ------------------------------------------------- detail par famille de sujets
    # Sert a la figure : dispersion interne par camp ET par famille, humains contre
    # agents. Le masque d'items d'une famille est fixe une fois sur les humains, pour
    # que toutes les conditions soient lues sur exactement les memes items.
    # Deux perimetres. C2 et C3 n'existent que sur 150 personnes : les lire a cote des
    # humains mesures sur 1 052 melangerait un effet de condition et un effet
    # d'echantillon, la colonne « perimetre » permet de ne jamais faire ce melange.
    fam = C.familles_gss(items)
    l3 = []
    for perim, msk, n_min in [("1052 personnes", masques, C.N_MIN_ITEM),
                              ("150 personnes", masques150, 15)]:
        masques_fam = {}
        for f in sorted(set(fam.values())):
            mf = np.array([fam[i] == f for i in items])
            masques_fam[f] = C.masque_items(ind_h, msk["droite"], msk["gauche"], mf,
                                            n_min=n_min)
        for nom, ind in inds.items():
            if perim == "1052 personnes" and nom in ("C2", "C3"):
                continue
            for f, mf in masques_fam.items():
                if mf.sum() < 3:
                    continue
                v = mesures_camp(ind, msk, mf)
                l3.append({"perimetre": perim, "condition": nom, "famille": f,
                           "n_items": int(mf.sum()), "gs_gauche": v["gauche"],
                           "gs_centre": v["centre"], "gs_droite": v["droite"],
                           "ratio_droite_gauche": v["droite"] / v["gauche"]
                           if v["gauche"] else np.nan})
    C.ecrire(pd.DataFrame(l3), "a30-agents-gss-familles.csv")
    print(df2[["condition", "n_items", "gs_gauche", "gs_droite",
               "ratio_droite_gauche", "ecrasement_gauche", "ecrasement_droite"]]
          .to_string(index=False), flush=True)
    return inds, masques, masques150, gardes, gardes150, ref, ref150


# ---------------------------------------------------------------------------
# Twin-2K-500
# ---------------------------------------------------------------------------

def volet_twin(args, rng):
    items = T.table_items()
    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    camps = C.camps_twin(w13)
    masques = {c: (camps["bloc3"] == c) for c in ("gauche", "centre", "droite")}
    pid = list(w13.index)

    configs = T.configs_llm_disponibles()
    llm = {}
    for nom, fichier in configs.items():
        d = T.charger_llm(fichier)
        llm[nom] = d.reindex(pid)
    cols = [c for c in items.index
            if c in w4.columns and items.at[c, "domaine"] != "demographies"
            and all(c in d.columns for d in llm.values())]
    print(f"Twin : {len(cols)} items communs aux humains vague 4 et aux "
          f"{len(llm)} configurations", flush=True)

    ordre = ["humains vague 4"] + list(llm.keys())
    tables = [w4.reindex(pid)] + [llm[n] for n in llm]
    codes_liste, ks = C.coder_numerique_commun(tables, cols)
    inds = {n: C.Indicatrice(c, ks) for n, c in zip(ordre, codes_liste)}

    ind_h = inds["humains vague 4"]
    gardes = C.masque_items(ind_h, masques["droite"], masques["gauche"],
                            np.ones(len(cols), dtype=bool))
    ref = mesures_camp(ind_h, masques, gardes)
    dom = np.array([items.at[c, "domaine"] for c in cols], dtype=object)

    lignes = []
    for nom, ind in inds.items():
        lig = ligne_condition(nom, ind, masques, gardes, ref, rng, args.boot, args.perm)
        for d in ("attitudes", "heuristiques_biais", "prix"):
            mf = C.masque_items(ind_h, masques["droite"], masques["gauche"], dom == d)
            v = mesures_camp(ind, masques, mf)
            lig[f"ratio_{d}"] = v["droite"] / v["gauche"] if v["gauche"] else np.nan
        lignes.append(lig)
    df = pd.DataFrame(lignes)
    df["p_holm"] = C.holm(df["p_permutation"].fillna(1.0).values)
    C.ecrire(df, "a30-agents-twin.csv")
    print(df[["condition", "gs_gauche", "gs_droite", "ratio_droite_gauche",
              "ecrasement_gauche", "ecrasement_droite", "ratio_attitudes"]]
          .to_string(index=False), flush=True)
    return inds, masques, gardes, ref


# ---------------------------------------------------------------------------
# A3 : l'etiquette ideologique
# ---------------------------------------------------------------------------

def contrastes_etiquette(inds_gss, masques150, gardes150, inds_twin, masques_twin,
                         gardes_twin, rng, boot):
    """Couples avec etiquette contre sans etiquette, sur le rapport droite / gauche.

    Le rapport est une quantite de population, pas une quantite individuelle : le
    bootstrap porte donc sur les personnes, les deux conditions du couple etant
    recalculees sur EXACTEMENT le meme tirage de personnes, ce qui apparie le contraste.
    """
    # Les deux premiers couples sont des contrastes d'etiquette au sens strict : meme
    # modele, memes personnes, memes questions, la seule difference documentee etant la
    # presence de l'ideologie declaree dans l'invite. Le troisieme n'en est pas un, c'est
    # un contraste de richesse d'information (entretien plus questionnaire contre
    # questionnaire seul) ; il figure ici comme temoin et ne doit pas etre lu comme un
    # effet d'etiquette.
    couples = [
        ("GSS 150", "C2 (avec etiquette ideologique)", "C2",
         "C3 (sans etiquette)", "C3"),
        ("GSS 150", "agents v8 (avec etiquette)", "agents v8",
         "agents demographiques v6 (sans)", "agents demographiques (v6)"),
        ("GSS 150", "TEMOIN, pas une etiquette : agents composite", "agents composite",
         "agents enquete", "agents enquete"),
    ]
    lignes = []
    for jeu, na, ka, nb, kb in couples:
        if ka not in inds_gss or kb not in inds_gss:
            continue
        ia, ib = inds_gss[ka], inds_gss[kb]
        wa = C.poids_bootstrap(masques150["droite"], boot, rng)
        wg = C.poids_bootstrap(masques150["gauche"], boot, rng)
        with np.errstate(divide="ignore", invalid="ignore"):
            ra = (C.agreger(C.mesures(ia.tables(wa))["gs"], gardes150)
                  / C.agreger(C.mesures(ia.tables(wg))["gs"], gardes150))
            rb = (C.agreger(C.mesures(ib.tables(wa))["gs"], gardes150)
                  / C.agreger(C.mesures(ib.tables(wg))["gs"], gardes150))
        d = ra - rb
        d = d[np.isfinite(d)]
        p_a = mesures_camp(ia, masques150, gardes150)
        p_b = mesures_camp(ib, masques150, gardes150)
        lignes.append({"jeu": jeu, "avec_etiquette": na, "sans_etiquette": nb,
                       "ratio_avec": p_a["droite"] / p_a["gauche"],
                       "ratio_sans": p_b["droite"] / p_b["gauche"],
                       "ecart": float(np.mean(d)),
                       "ic_bas": float(np.percentile(d, 2.5)),
                       "ic_haut": float(np.percentile(d, 97.5))})
    for na, nb in [("gpt41mini_defaut", "gpt41mini_demo_seules")]:
        if na not in inds_twin or nb not in inds_twin:
            continue
        ia, ib = inds_twin[na], inds_twin[nb]
        wa = C.poids_bootstrap(masques_twin["droite"], boot, rng)
        wg = C.poids_bootstrap(masques_twin["gauche"], boot, rng)
        with np.errstate(divide="ignore", invalid="ignore"):
            ra = (C.agreger(C.mesures(ia.tables(wa))["gs"], gardes_twin)
                  / C.agreger(C.mesures(ia.tables(wg))["gs"], gardes_twin))
            rb = (C.agreger(C.mesures(ib.tables(wa))["gs"], gardes_twin)
                  / C.agreger(C.mesures(ib.tables(wg))["gs"], gardes_twin))
        d = ra - rb
        d = d[np.isfinite(d)]
        p_a = mesures_camp(ia, masques_twin, gardes_twin)
        p_b = mesures_camp(ib, masques_twin, gardes_twin)
        lignes.append({"jeu": "Twin vague 4", "avec_etiquette": na,
                       "sans_etiquette": nb,
                       "ratio_avec": p_a["droite"] / p_a["gauche"],
                       "ratio_sans": p_b["droite"] / p_b["gauche"],
                       "ecart": float(np.mean(d)),
                       "ic_bas": float(np.percentile(d, 2.5)),
                       "ic_haut": float(np.percentile(d, 97.5))})
    df = pd.DataFrame(lignes)
    C.ecrire(df, "a30-agents-contrastes.csv")
    print(df.to_string(index=False), flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", dest="cache_foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--boot", type=int, default=C.N_BOOT)
    ap.add_argument("--perm", type=int, default=C.N_PERM)
    args = ap.parse_args()
    rng = np.random.default_rng(C.GRAINE)

    inds_gss, masques, masques150, gardes, gardes150, ref, ref150 = volet_gss(args, rng)
    inds_twin, masques_twin, gardes_twin, ref_twin = volet_twin(args, rng)
    contrastes_etiquette(inds_gss, masques150, gardes150, inds_twin, masques_twin,
                         gardes_twin, rng, args.boot)


if __name__ == "__main__":
    main()
