"""
a38_tests : les quatre hypotheses de a38, corrigees sur la famille declaree.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a25_commun, a28_commun et a38_commun sont
importes tels quels. Ce script ne lit que des tableaux de resultats deja ecrits par
a38_ampleurs.py et a38_mesures.py.

La famille d'hypotheses est celle declaree dans l'entete de a38_commun.py, K1 a K4, 52
tests, correction principale de Holm et correction secondaire de Benjamini Hochberg.

  K1  correlation de rang entre l'ampleur de mode MESUREE et la distance, par item.
  K2  la meme avec le rapport d'entropie, prediction de signe negatif.
  K3  le contraste sensible moins temoin est plus grand sur les comportements declares
      que sur les attitudes.
  K4  l'ecart de desirabilite differe entre le bloc de gauche et le bloc de droite.

Sortie : resultats/a38-continu.csv, a38-comportement.csv, a38-camp.csv,
         a38-corrections.csv, a38-contraste-de-groupe.csv, a38-robustesse.csv.

Usage :
  .venv/bin/python analyses/a38_tests.py --tirages 20000
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a38_commun as A38


# ---------------------------------------------------------------------------

def contraste_permute(a, b, tirages, rng):
    """Difference de moyennes, intervalle bootstrap sur les items, p de permutation."""
    _, bas, haut = C28.bootstrap_items(a, b, min(tirages, 10000), rng)
    obs, p = C28.permutation(a, b, tirages, rng)
    return obs, bas, haut, p


def difference_de_contrastes(d, tirages, rng):
    """Contraste sensible moins temoin dans chaque classe d'item, et sa difference.

    d porte les colonnes classe_norc, classe_comportement, distance. La statistique
    testee est (contraste chez les comportements) moins (contraste chez les attitudes).
    Le p vient d'une permutation des etiquettes sensible et temoin A L'INTERIEUR de
    chaque classe, ce qui preserve la composition des classes et ne teste que ce qui est
    en jeu.
    """
    def bras(cl):
        s = d[d.classe_comportement == cl]
        return (s.loc[s.classe_norc == "sensible", "distance"].values,
                s.loc[s.classe_norc == "temoin", "distance"].values)

    ac, tc = bras("comportement")
    aa, ta = bras("attitude")
    if len(ac) < 1 or len(tc) < 2 or len(aa) < 2 or len(ta) < 2:
        return {k: np.nan for k in
                ["contraste_comportement", "contraste_attitude", "difference",
                 "ic_bas", "ic_haut", "p_permutation"]} | {
                "n_sensible_comportement": len(ac), "n_temoin_comportement": len(tc),
                "n_sensible_attitude": len(aa), "n_temoin_attitude": len(ta)}
    cc = float(np.nanmean(ac) - np.nanmean(tc))
    ca = float(np.nanmean(aa) - np.nanmean(ta))
    obs = cc - ca

    poolc = np.concatenate([ac, tc])
    poola = np.concatenate([aa, ta])
    nc, na = len(ac), len(aa)
    pc = poolc[np.argsort(rng.random((tirages, len(poolc))), axis=1)]
    pa = poola[np.argsort(rng.random((tirages, len(poola))), axis=1)]
    tir = ((pc[:, :nc].mean(axis=1) - pc[:, nc:].mean(axis=1))
           - (pa[:, :na].mean(axis=1) - pa[:, na:].mean(axis=1)))
    p = ((np.abs(tir) >= abs(obs) - 1e-12).sum() + 1.0) / (tirages + 1.0)

    # intervalle bootstrap sur les items, les quatre groupes reechantillonnes separement
    b = min(tirages, 10000)
    def tirs(v):
        v = np.asarray(v, float)
        v = v[~np.isnan(v)]
        return v[rng.integers(0, len(v), (b, len(v)))].mean(axis=1)
    dd = (tirs(ac) - tirs(tc)) - (tirs(aa) - tirs(ta))
    return {"contraste_comportement": cc, "contraste_attitude": ca, "difference": obs,
            "ic_bas": float(np.percentile(dd, 2.5)),
            "ic_haut": float(np.percentile(dd, 97.5)), "p_permutation": p,
            "n_sensible_comportement": len(ac), "n_temoin_comportement": len(tc),
            "n_sensible_attitude": len(aa), "n_temoin_attitude": len(ta)}


def test_camp(dg, dd, tirages, rng):
    """Compare l'ecart de desirabilite du bloc de gauche et du bloc de droite.

    dg et dd sont deux series indexees par item, l'ecart de desirabilite agent contre
    humain mesure dans chaque camp. Le test est apparie item par item : la statistique
    est la moyenne de (droite moins gauche), et le p vient d'une permutation de signe,
    qui est le test exact de l'hypothese "les deux camps se deplacent pareil".
    """
    commun = dg.index.intersection(dd.index)
    g = dg.loc[commun].values.astype(float)
    d = dd.loc[commun].values.astype(float)
    ok = ~np.isnan(g) & ~np.isnan(d)
    g, d = g[ok], d[ok]
    if len(g) < 4:
        return None
    delta = d - g
    obs = float(delta.mean())
    signes = rng.choice([-1.0, 1.0], size=(tirages, len(delta)))
    tir = (signes * delta).mean(axis=1)
    p = ((np.abs(tir) >= abs(obs) - 1e-12).sum() + 1.0) / (tirages + 1.0)
    b = min(tirages, 10000)
    idx = rng.integers(0, len(delta), (b, len(delta)))
    tb = delta[idx].mean(axis=1)
    return {"n_items": int(len(g)),
            "ecart_gauche": float(g.mean()), "ecart_droite": float(d.mean()),
            "difference_droite_moins_gauche": obs,
            "ic_bas": float(np.percentile(tb, 2.5)),
            "ic_haut": float(np.percentile(tb, 97.5)),
            "p_permutation": p}


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirages", type=int, default=20000)
    ap.add_argument("--graine", type=int, default=A38.GRAINE)
    args = ap.parse_args()
    rng = np.random.default_rng(args.graine)

    print(__doc__.split("La famille")[1].split("Sortie")[0])

    amp = pd.read_csv(os.path.join(A38.SORTIE, "a38-ampleurs-items.csv"))
    par_item = pd.read_csv(os.path.join(A38.SORTIE, "a38-par-item-condition.csv"))
    par_camp = pd.read_csv(os.path.join(A38.SORTIE, "a38-par-camp.csv"))
    par_item["perimetre"] = par_item.perimetre.astype(str)
    par_camp["perimetre"] = par_camp.perimetre.astype(str)

    a = amp.set_index("item")
    toutes = [c for c in C28.ORDRE_METHODES if c in set(par_item.condition)]

    # =========================================================== K1 et K2, T1 continu
    lignes = []
    for per, dper in par_item.groupby("perimetre"):
        for cond, d in dper.groupby("condition"):
            d = d.set_index("item")
            for nom_s, col in [("M1 mode", "m1_mode"),
                               ("M2 mode plus conception", "m2_mode_plus_conception"),
                               ("M3 toutes sources", "m3_toutes_sources")]:
                u = a.loc[d.index, col].values
                for hyp, metrique in [("K1 distance", "distance"),
                                      ("K2 dispersion", "ratio_entropie")]:
                    v = d[metrique].values
                    r, bas, haut, n = A38.correlation_sure(u, v, 2000, rng)
                    _, p, _ = A38.p_permutation_correlation(u, v, args.tirages, rng)
                    lignes.append({
                        "perimetre": per, "hypothese": hyp, "condition": cond,
                        "score": nom_s, "metrique": metrique, "rho_spearman": r,
                        "ic_items_bas": bas, "ic_items_haut": haut, "n_items": n,
                        "p_permutation": p})
    continu = pd.DataFrame(lignes)
    A38.ecrire(continu, "a38-continu.csv")

    # =========================================================== K3, comportement
    lignes = []
    for per, dper in par_item.groupby("perimetre"):
        for cond, d in dper.groupby("condition"):
            r = difference_de_contrastes(d, args.tirages, rng)
            lignes.append({"perimetre": per, "condition": cond, **r})
            # detail par classe, en description
            for cl in ["comportement", "attitude", "auto evaluation"]:
                s = d[d.classe_comportement == cl]
                aa = s.loc[s.classe_norc == "sensible", "distance"].values
                tt = s.loc[s.classe_norc == "temoin", "distance"].values
                if len(aa) and len(tt):
                    obs, bas, haut, p = contraste_permute(aa, tt, args.tirages, rng)
                else:
                    obs = bas = haut = p = np.nan
                lignes[-1][f"contraste_{cl.replace(' ', '_')}"] = obs
                lignes[-1][f"p_{cl.replace(' ', '_')}"] = p
                lignes[-1][f"n_sensible_{cl.replace(' ', '_')}"] = len(aa)
                lignes[-1][f"n_temoin_{cl.replace(' ', '_')}"] = len(tt)
    comportement = pd.DataFrame(lignes)
    A38.ecrire(comportement, "a38-comportement.csv")

    # =========================================================== K4, par camp
    #
    # L'echelle de lecture est donnee par les humains eux memes. Soit ecart_humain, item
    # par item, le score de desirabilite du bloc de gauche moins celui du bloc de droite
    # dans la population humaine de la vague 1. Alors :
    #
    #   difference droite moins gauche = ecart_humain moins ecart_simule
    #
    # ce qui donne trois reperes exacts et non arbitraires :
    #   difference = +ecart_humain  -> la methode ignore completement le camp
    #   difference = 0              -> la methode reproduit exactement l'ecart humain
    #   difference < 0              -> la methode EXAGERE l'ecart entre camps
    #
    # Le facteur d'amplification, ecart_simule sur ecart_humain, vaut donc 0 quand la
    # methode ignore le camp, 1 quand elle est fidele, plus de 1 quand elle caricature.
    hum = pd.read_csv(os.path.join(A38.SORTIE,
                                   "a38-desirabilite-humaine-par-camp.csv"))
    hum["perimetre"] = hum.perimetre.astype(str)
    items_camp = [it for it in a.index if it in A38.POLE_ENDOGROUPE]

    # controle prealable : le bit declare item par item dit que la position typique de la
    # droite se trouve du cote bas du score de desirabilite. Les humains le confirment ils ?
    verif = []
    for per, h in hum[hum.item.isin(items_camp)].groupby("perimetre"):
        piv = h.pivot_table(index="item", columns="camp", values="desirabilite_humaine")
        if not {"gauche", "droite"}.issubset(piv.columns):
            continue
        for it in piv.index:
            attendu = A38.POLE_ENDOGROUPE[it][0]
            gap = float(piv.loc[it, "gauche"] - piv.loc[it, "droite"])
            verif.append({"perimetre": per, "item": it,
                          "pole_endogroupe_declare": attendu,
                          "desirabilite_gauche": float(piv.loc[it, "gauche"]),
                          "desirabilite_droite": float(piv.loc[it, "droite"]),
                          "ecart_humain_gauche_moins_droite": gap,
                          "declaration_confirmee": bool(
                              (gap > 0) == (attendu == "droite_bas"))})
    verif = pd.DataFrame(verif)
    A38.ecrire(verif, "a38-verification-pole-endogroupe.csv")

    lignes = []
    for per, dper in par_camp.groupby("perimetre"):
        h = hum[hum.perimetre == per].pivot_table(
            index="item", columns="camp", values="desirabilite_humaine")
        gap_hum = (h["gauche"] - h["droite"]).reindex(items_camp)
        for cond, d in dper.groupby("condition"):
            d = d[d.item.isin(items_camp)]
            piv = d.pivot_table(index="item", columns="camp",
                                values="ecart_desirabilite")
            if not {"gauche", "droite"}.issubset(piv.columns):
                continue
            r = test_camp(piv["gauche"], piv["droite"], args.tirages, rng)
            if r is None:
                continue
            # deplacement vers le pole d'endogroupe : le score de desirabilite de a25 est
            # oriente vers le pole progressiste, donc pour un item "droite_bas" le pole
            # d'endogroupe de la droite est le pole BAS et celui de la gauche le pole haut.
            signe = np.array([-1.0 if A38.POLE_ENDOGROUPE[it][0] == "droite_bas" else 1.0
                              for it in piv.index])
            endo_d = float(np.nanmean(signe * piv["droite"].values))
            endo_g = float(np.nanmean(-signe * piv["gauche"].values))
            centre = (float(np.nanmean(piv["centre"].values))
                      if "centre" in piv.columns else np.nan)
            gh = float(np.nanmean(gap_hum.loc[piv.index].values))
            gs = gh - r["difference_droite_moins_gauche"]
            lignes.append({"perimetre": per, "condition": cond, **r,
                           "ecart_centre": centre,
                           "vers_endogroupe_droite": endo_d,
                           "vers_endogroupe_gauche": endo_g,
                           "ecart_humain_entre_camps": gh,
                           "ecart_simule_entre_camps": gs,
                           "facteur_amplification": (gs / gh if abs(gh) > 1e-9
                                                     else np.nan)})
    camp = pd.DataFrame(lignes)
    A38.ecrire(camp, "a38-camp.csv")

    # ---- robustesse de K4 au sous ensemble d'items, hors famille
    #
    # Quinze des 29 items sont des items de depense publique, ou Smith et Dennis refusent
    # explicitement de lire le pole pro depense comme le pole socialement desirable. Le
    # test est donc rejoue sans eux. `natroad` est retire a part : c'est le seul item dont
    # les humains contredisent le bit declare, l'ecart entre camps y valant moins 0,009.
    depenses_camp = [it for it in items_camp if it.startswith("nat")]
    sous_ensembles = [
        ("tous les items a pole declare", items_camp),
        ("sans les items de depense", [it for it in items_camp
                                       if it not in depenses_camp]),
        ("sans natroad", [it for it in items_camp if it != "natroad"]),
        ("items de depense seuls", depenses_camp),
    ]
    lignes = []
    for per, dper in par_camp.groupby("perimetre"):
        h = hum[hum.perimetre == per].pivot_table(
            index="item", columns="camp", values="desirabilite_humaine")
        for nom_se, sel in sous_ensembles:
            gap_hum = (h["gauche"] - h["droite"]).reindex(sel)
            for cond, d in dper.groupby("condition"):
                d = d[d.item.isin(sel)]
                piv = d.pivot_table(index="item", columns="camp",
                                    values="ecart_desirabilite")
                if not {"gauche", "droite"}.issubset(piv.columns):
                    continue
                r = test_camp(piv["gauche"], piv["droite"], 10000, rng)
                if r is None:
                    continue
                gh = float(np.nanmean(gap_hum.loc[piv.index].values))
                gs = gh - r["difference_droite_moins_gauche"]
                lignes.append({"perimetre": per, "sous_ensemble": nom_se,
                               "condition": cond, **r,
                               "ecart_humain_entre_camps": gh,
                               "facteur_amplification": (gs / gh if abs(gh) > 1e-9
                                                         else np.nan)})
    camp_rob = pd.DataFrame(lignes)
    A38.ecrire(camp_rob, "a38-camp-robustesse.csv")

    # =========================================================== corrections
    famille = []
    for _, r in continu[(continu.perimetre == "150") & (continu.score == "M1 mode")
                        & (continu.condition != "humains vague 2")].iterrows():
        famille.append({"hypothese": r.hypothese, "condition": r.condition,
                        "statistique": r.rho_spearman, "p": r.p_permutation})
    for _, r in comportement[(comportement.perimetre == "150")
                             & (comportement.condition != "humains vague 2")].iterrows():
        famille.append({"hypothese": "K3 comportement", "condition": r.condition,
                        "statistique": r.difference, "p": r.p_permutation})
    for _, r in camp[(camp.perimetre == "150")
                     & (camp.condition != "humains vague 2")].iterrows():
        famille.append({"hypothese": "K4 camp", "condition": r.condition,
                        "statistique": r.difference_droite_moins_gauche,
                        "p": r.p_permutation})
    fam = pd.DataFrame(famille)
    fam = fam[fam.p.notna()].reset_index(drop=True)
    fam["p_holm_famille_complete"] = C28.holm(fam.p.values)
    fam["p_bh_famille_complete"] = C28.benjamini_hochberg(fam.p.values)
    fam["p_holm_sous_famille"] = np.nan
    fam["p_bh_sous_famille"] = np.nan
    for h, idx in fam.groupby("hypothese").groups.items():
        idx = list(idx)
        fam.loc[idx, "p_holm_sous_famille"] = C28.holm(fam.loc[idx, "p"].values)
        fam.loc[idx, "p_bh_sous_famille"] = C28.benjamini_hochberg(fam.loc[idx, "p"].values)
    A38.ecrire(fam, "a38-corrections.csv")

    # =========================================================== contraste de groupe
    #
    # Post hoc, exactement comme en a28 section 1.6, et hors de toute correction : la
    # revendication du projet ne porte pas sur une condition mais sur un motif, huit
    # conditions a modele de langage d'un cote et cinq predicteurs statistiques de
    # l'autre. Le p vient d'une permutation des etiquettes de METHODE, et il se lit comme
    # la probabilite qu'un decoupage au hasard de 13 methodes en 8 et 5 produise un ecart
    # aussi grand. Les 13 methodes ne sont pas des unites echangeables, la limite est la
    # meme qu'en a28 et elle est rappelee dans le rapport.
    lignes = []
    def groupe(source, col, filtre, nom):
        s = source[filtre]
        aa = s[s.condition.isin(C28.LLM)][col].values
        bb = s[s.condition.isin(C28.STAT)][col].values
        if len(aa) < 2 or len(bb) < 2:
            return
        obs, p = C28.permutation(aa, bb, args.tirages, rng)
        lignes.append({"quantite": nom, "moyenne_llm": float(np.nanmean(aa)),
                       "moyenne_statistique": float(np.nanmean(bb)),
                       "difference": obs, "p_permutation_methodes": p,
                       "n_llm": len(aa), "n_stat": len(bb)})

    for nom_s in ["M1 mode", "M2 mode plus conception", "M3 toutes sources"]:
        for hyp in ["K1 distance", "K2 dispersion"]:
            groupe(continu, "rho_spearman",
                   (continu.perimetre == "150") & (continu.score == nom_s)
                   & (continu.hypothese == hyp), f"{hyp}, {nom_s}, perimetre 150")
            groupe(continu, "rho_spearman",
                   (continu.perimetre == "1052") & (continu.score == nom_s)
                   & (continu.hypothese == hyp), f"{hyp}, {nom_s}, perimetre 1052")
    groupe(comportement, "difference", comportement.perimetre == "150",
           "K3 comportement moins attitude, perimetre 150")
    groupe(comportement, "contraste_comportement", comportement.perimetre == "150",
           "K3 contraste sur les comportements seuls, perimetre 150")
    groupe(comportement, "contraste_attitude", comportement.perimetre == "150",
           "K3 contraste sur les attitudes seules, perimetre 150")
    groupe(camp, "difference_droite_moins_gauche", camp.perimetre == "150",
           "K4 droite moins gauche, perimetre 150")
    groupe(camp, "ecart_droite", camp.perimetre == "150",
           "K4 ecart de desirabilite du bloc de droite, perimetre 150")
    groupe(camp, "ecart_gauche", camp.perimetre == "150",
           "K4 ecart de desirabilite du bloc de gauche, perimetre 150")
    groupe(camp, "difference_droite_moins_gauche", camp.perimetre == "1052",
           "K4 droite moins gauche, perimetre 1052")
    groupe(camp, "facteur_amplification", camp.perimetre == "150",
           "K4 facteur d'amplification de l'ecart entre camps, perimetre 150")
    groupe(camp, "facteur_amplification", camp.perimetre == "1052",
           "K4 facteur d'amplification de l'ecart entre camps, perimetre 1052")
    groupes = pd.DataFrame(lignes)
    A38.ecrire(groupes, "a38-contraste-de-groupe.csv")

    # =========================================================== robustesse
    #
    # Trois controles, tous conditionnels et hors famille.
    #   (i)   le confondant de conception seul : la correlation entre la part de modalite
    #         volontaire de MR141 et l'ecart agent contre humain, sur les 17 items communs.
    #         Si elle est forte, une part de l'ecart que a25 attribue au modele vient de ce
    #         que l'humain disposait d'une echappatoire que l'agent n'a jamais eue.
    #   (ii)  la correlation M1 sur les seules attitudes, pour verifier que le resultat
    #         n'est pas porte par les deux comportements du jeu ;
    #   (iii) la correlation M1 sans les items de depense, qui forment 16 des 21 items
    #         couverts et pourraient a eux seuls porter le motif.
    depense = [it for it in a.index if it.startswith("nat")]
    lignes = []
    for per, dper in par_item.groupby("perimetre"):
        for cond, d in dper.groupby("condition"):
            d = d.set_index("item")
            for nom_r, sel, col in [
                    ("conception seule, MR141", a.famille_retenue == "conception",
                     "m3_toutes_sources"),
                    ("M1 attitudes seules", a.classe_comportement == "attitude", "m1_mode"),
                    ("M1 sans les items de depense",
                     ~a.index.isin(depense), "m1_mode")]:
                idx = a.index[sel]
                sous = d[d.index.isin(idx)]
                if len(sous) < 6:
                    continue
                u = a.loc[sous.index, col].values
                for hyp, metrique in [("K1 distance", "distance"),
                                      ("K2 dispersion", "ratio_entropie")]:
                    v = sous[metrique].values
                    r, bas, haut, n = A38.correlation_sure(u, v, 2000, rng)
                    _, p, _ = A38.p_permutation_correlation(u, v, 10000, rng)
                    lignes.append({"perimetre": per, "condition": cond,
                                   "controle": nom_r, "hypothese": hyp,
                                   "rho_spearman": r, "ic_items_bas": bas,
                                   "ic_items_haut": haut, "n_items": n,
                                   "p_permutation": p})
    robustesse = pd.DataFrame(lignes)
    A38.ecrire(robustesse, "a38-robustesse.csv")

    # =========================================================== affichage
    pd.set_option("display.width", 240)
    ordre = {c: i for i, c in enumerate(C28.ORDRE_METHODES)}

    for hyp in ["K1 distance", "K2 dispersion"]:
        print("\n" + "=" * 118)
        print(f"{hyp}, perimetre 150, correlation de rang ampleur x mesure")
        print("=" * 118)
        s = continu[(continu.perimetre == "150") & (continu.hypothese == hyp)].copy()
        piv = s.pivot(index="condition", columns="score", values="rho_spearman")
        piv = piv.reindex([c for c in C28.ORDRE_METHODES if c in piv.index])
        pp = s[s.score == "M1 mode"].set_index("condition")
        piv["p brut M1"] = pp.p_permutation
        piv["IC M1"] = [f"[{b:+.3f} ; {h:+.3f}]" for b, h in
                        zip(pp.reindex(piv.index).ic_items_bas,
                            pp.reindex(piv.index).ic_items_haut)]
        print(piv.round(4).to_string())

    print("\n" + "=" * 118)
    print("K3, comportements declares contre attitudes, perimetre 150")
    print("=" * 118)
    s = comportement[comportement.perimetre == "150"].copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values("o")[
        ["condition", "contraste_comportement", "contraste_attitude",
         "contraste_auto_evaluation", "difference", "ic_bas", "ic_haut",
         "p_permutation"]].round(4).to_string(index=False))
    print(f"\nnombre d'items par case : sensibles comportement "
          f"{int(s.n_sensible_comportement.iloc[0])}, temoins comportement "
          f"{int(s.n_temoin_comportement.iloc[0])}, sensibles attitude "
          f"{int(s.n_sensible_attitude.iloc[0])}, temoins attitude "
          f"{int(s.n_temoin_attitude.iloc[0])}")

    for per in ["150", "1052"]:
        print("\n" + "=" * 118)
        print(f"K4, ecart de desirabilite par camp, perimetre {per}, "
              f"{len(items_camp)} items a pole d'endogroupe declare")
        print("=" * 118)
        s = camp[camp.perimetre == per].copy()
        if not len(s):
            continue
        s["o"] = s.condition.map(ordre)
        print(s.sort_values("o")[
            ["condition", "n_items", "ecart_gauche", "ecart_centre", "ecart_droite",
             "difference_droite_moins_gauche", "ic_bas", "ic_haut", "p_permutation",
             "ecart_simule_entre_camps", "facteur_amplification"]].round(4).to_string(
            index=False))
        print(f"  ecart humain entre camps, echelle de reference : "
              f"{s.ecart_humain_entre_camps.iloc[0]:+.4f} point de score de "
              f"desirabilite ; facteur 0 = la methode ignore le camp, 1 = elle le "
              f"reproduit, plus de 1 = elle le caricature")

    print("\n" + "=" * 118)
    print("Contraste de groupe, post hoc, huit conditions a modele de langage contre "
          "cinq predicteurs statistiques")
    print("=" * 118)
    print(groupes.round(4).to_string(index=False))

    print("\n" + "=" * 118)
    print("Corrections pour tests multiples, famille de "
          f"{len(fam)} tests declaree avant les resultats")
    print("=" * 118)
    f = fam.sort_values("p")
    print(f.head(20).round(4).to_string(index=False))
    for col, nom in [("p_holm_famille_complete", "Holm 52"),
                     ("p_bh_famille_complete", "Benjamini Hochberg 52"),
                     ("p_holm_sous_famille", "Holm par sous famille de 13"),
                     ("p_bh_sous_famille", "BH par sous famille de 13")]:
        n = int((fam[col] < 0.05).sum())
        print(f"  {nom:<32} : {n} test(s) sous 0,05, meilleur p ajuste "
              f"{fam[col].min():.4f}")

    print("\n" + "=" * 118)
    print("K4, robustesse au sous ensemble d'items, facteur d'amplification, "
          "perimetre 150")
    print("=" * 118)
    s = camp_rob[camp_rob.perimetre == "150"]
    piv = s.pivot(index="condition", columns="sous_ensemble",
                  values="facteur_amplification")
    piv = piv.reindex([c for c in C28.ORDRE_METHODES if c in piv.index])
    print(piv.round(3).to_string())
    print("\nnombre d'items par sous ensemble :")
    print(s.groupby("sous_ensemble").n_items.first().to_string())

    print("\n" + "=" * 118)
    print("Robustesse, perimetre 150")
    print("=" * 118)
    s = robustesse[(robustesse.perimetre == "150")
                   & (robustesse.hypothese == "K1 distance")].copy()
    piv = s.pivot(index="condition", columns="controle", values="rho_spearman")
    piv = piv.reindex([c for c in C28.ORDRE_METHODES if c in piv.index])
    print(piv.round(4).to_string())
    print("\nnombre d'items par controle :")
    print(s.groupby("controle").n_items.first().to_string())


if __name__ == "__main__":
    main()
