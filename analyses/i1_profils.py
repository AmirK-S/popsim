"""
i1_profils : Q-C du preenregistrement I1, volet humain d'I2. Qui bouge ?

Position initiale, incoherence initiale, cross pressures au sens de a30, et bruit de
reponse propre a la personne estime hors des items evalues. Les personnes incoherentes en
vague 1 sont elles celles qui bougent ?

Zero appel de modele. Lecture seule sur data/. Aucun script existant modifie.

Sorties :
  resultats/i1-cross-pressions.csv
  resultats/i1-profil-changeurs.csv
  resultats/i1-position-initiale.csv
  resultats/i1-deciles-cross-pression.csv

Usage : .venv/bin/python analyses/i1_profils.py
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import rankdata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_commun as I1
from a2_commun import bootstrap_personnes


def spearman(a, b):
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 10:
        return np.nan
    return float(np.corrcoef(rankdata(a[ok]), rankdata(b[ok]))[0, 1])


def contraste_bootstrap(valeurs, groupe, cible_a, cible_b, n=I1.N_BOOTSTRAP,
                        graine=I1.GRAINE):
    """Ecart de moyenne entre deux groupes de personnes, IC bootstrap sur les personnes."""
    ia = np.flatnonzero((groupe == cible_a) & np.isfinite(valeurs))
    ib = np.flatnonzero((groupe == cible_b) & np.isfinite(valeurs))
    if len(ia) < 10 or len(ib) < 10:
        return np.nan, np.nan, np.nan, np.nan, np.nan, len(ia), len(ib)
    rng = np.random.default_rng(graine)
    obs = float(valeurs[ia].mean() - valeurs[ib].mean())
    t = np.empty(n)
    for r in range(n):
        t[r] = (valeurs[rng.choice(ia, len(ia), replace=True)].mean()
                - valeurs[rng.choice(ib, len(ib), replace=True)].mean())
    p = float(min(1.0, 2 * min((t <= 0).mean(), (t >= 0).mean())))
    return (obs, float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5)), p,
            float(valeurs[ia].mean()), len(ia), len(ib))


def permutation_intra_segment(valeurs, groupe, seg_codes, cible_a, cible_b,
                              n=I1.N_PERMUTATIONS, graine=I1.GRAINE):
    """L'ecart survit il quand l'etiquette de groupe est brassee dans le segment ?

    Si l'ecart entre hors quadrant et congruents disparait sous permutation des
    etiquettes a l'interieur du segment ideologie x age x education, alors la cross
    pression n'est qu'un autre nom du segment. C'est la permutation de a44 appliquee a
    une etiquette de personne au lieu d'une matrice de reponses.
    """
    rng = np.random.default_rng(graine)
    bon = np.isfinite(valeurs) & np.isin(groupe, [cible_a, cible_b])
    v, g, s = valeurs[bon], groupe[bon], seg_codes[bon]
    obs = float(v[g == cible_a].mean() - v[g == cible_b].mean())
    t = np.empty(n)
    for r in range(n):
        perm = I1.permuter_intra(s, rng)
        gp = g[perm]
        t[r] = float(v[gp == cible_a].mean() - v[gp == cible_b].mean())
    p = (1 + int((np.abs(t) >= abs(obs)).sum())) / (1 + n)
    return obs, float(np.mean(t)), float(np.percentile(t, 2.5)), \
        float(np.percentile(t, 97.5)), p


def taux_personne(classe, colonnes=None):
    """Taux de changement brut et taux de changement monotone, par personne."""
    c = classe if colonnes is None else classe[:, colonnes]
    ok = c >= 0
    d = np.maximum(ok.sum(axis=1), 1)
    return (c > 0).sum(axis=1) / d, (c == 1).sum(axis=1) / d, ok.sum(axis=1)


def bruit_propre(noyau, brut, tables, moities, graine=I1.GRAINE):
    """Taux d'aller retour par personne sur les trois panels a trois vagues.

    Il est calcule sur une moitie des items et confronte au changement monotone mesure
    sur l'AUTRE moitie, puis l'inverse : sans ce croisement, la quantite predite et la
    quantite predictive partageraient les memes cellules et la correlation serait un
    artefact d'algebre.
    """
    k = [max(len(t), 1) for t in tables]
    out = []
    for nom, a, b, c in I1.TROIS_VAGUES:
        ca = I1.coder(brut[nom]["mat"][a], tables)
        cb = I1.coder(brut[nom]["mat"][b], tables)
        cc = I1.coder(brut[nom]["mat"][c], tables)
        ok = (ca >= 0) & (cb >= 0) & (cc >= 0)
        garde = ok.sum(axis=1) >= I1.MIN_ITEMS_INDIVIDU
        ca, cb, cc, ok = ca[garde], cb[garde], cc[garde], ok[garde]
        ar = ok & (ca == cc) & (cb != ca)
        cls = I1.classer_changement(ca, cc, k)
        for m, autre in ((moities[0], moities[1]), (moities[1], moities[0])):
            d1 = np.maximum(ok[:, m].sum(axis=1), 1)
            d2 = np.maximum((cls[:, autre] >= 0).sum(axis=1), 1)
            out.append(pd.DataFrame({
                "panel": nom, "moitie": "A" if m is moities[0] else "B",
                "aller_retour": ar[:, m].sum(axis=1) / d1,
                "monotone_autre_moitie": (cls[:, autre] == 1).sum(axis=1) / d2,
                "changement_autre_moitie": (cls[:, autre] > 0).sum(axis=1) / d2,
            }))
    return pd.concat(out, ignore_index=True)


def main():
    rng = np.random.default_rng(I1.GRAINE)
    noyau, brut, n_paires = I1.charger_panels()
    tables = I1.alphabet_panel(brut, len(noyau))
    paquet = I1.assembler(I1.PAIRES_4ANS, noyau, brut, tables)
    profs = I1.profils(paquet)
    seg_codes, niveaux = I1.codes_segment(paquet["segment"])
    cls = paquet["classe"]
    print(f"{paquet['n']} personnes, axes economique {profs['n_items_axe_eco']} items, "
          f"social {profs['n_items_axe_soc']} items", flush=True)

    t_chg, t_mono, n_items_pers = taux_personne(cls)
    q = profs["quadrant"]
    print("quadrants :", pd.Series(q).value_counts(dropna=False).to_dict(), flush=True)

    # ------------------------------------------------------------ 1. quadrants
    lignes = []
    for nom_cible, val in (("changement brut", t_chg), ("changement monotone", t_mono)):
        (obs, bas, haut, p, moy_a, na, nb) = contraste_bootstrap(
            val, q, "hors quadrant", "congruent")
        o2, moy_perm, pbas, phaut, pperm = permutation_intra_segment(
            val, q, seg_codes, "hors quadrant", "congruent")
        lignes.append({
            "cible": nom_cible, "contraste": "hors quadrant moins congruent",
            "n_hors_quadrant": na, "n_congruent": nb,
            "moyenne_hors_quadrant": moy_a, "moyenne_congruent": moy_a - obs,
            "ecart": obs, "ic_bas": bas, "ic_haut": haut, "p_bootstrap": p,
            "ecart_sous_permutation_intra_segment": moy_perm,
            "perm_ic_bas": pbas, "perm_ic_haut": phaut, "p_permutation": pperm,
        })
    t_q = pd.DataFrame(lignes)
    t_q["p_holm"] = I1.holm(t_q["p_permutation"].values)
    I1.ecrire(t_q, "i1-cross-pressions.csv")
    print(t_q.to_string(index=False), flush=True)

    # ------------------------------------ 2. correlations avec les profils de vague 1
    variables = {
        "cross pression |z_eco - z_soc|": profs["cross_pression"],
        "distance au patron modal du segment": profs["distance_patron_segment"],
        "part de modalites rares tenues": profs["part_rare"],
        "part de modalites majoritaires tenues": profs["part_majoritaire"],
        "score economique z": profs["z_eco"],
        "score social z": profs["z_soc"],
        "|position ideologique - centre|": np.abs(
            np.where(np.isfinite(paquet["demos"]["polviews"]),
                     paquet["demos"]["polviews"], np.nan) - 4.0),
        "age": paquet["demos"]["age"],
        "annees d'etudes": paquet["demos"]["educ"],
        "part de cellules manquantes": profs["part_manquants"],
    }
    lignes = []
    rng2 = np.random.default_rng(I1.GRAINE)
    for nom, v in variables.items():
        for cible, y in (("changement brut", t_chg), ("changement monotone", t_mono)):
            r = spearman(v, y)
            ok = np.flatnonzero(np.isfinite(v) & np.isfinite(y))
            tir = np.empty(400)
            for b in range(400):
                s = rng2.choice(ok, len(ok), replace=True)
                tir[b] = spearman(v[s], y[s])
            p = float(min(1.0, 2 * min((tir <= 0).mean(), (tir >= 0).mean())))
            # la meme correlation apres permutation des personnes dans le segment
            perms = np.empty(I1.N_PERMUTATIONS)
            for b in range(I1.N_PERMUTATIONS):
                perm = I1.permuter_intra(seg_codes, rng2)
                perms[b] = spearman(v, y[perm])
            lignes.append({"variable": nom, "cible": cible, "n": len(ok),
                           "rho_spearman": r,
                           "ic_bas": float(np.percentile(tir, 2.5)),
                           "ic_haut": float(np.percentile(tir, 97.5)),
                           "p_bootstrap": p,
                           "rho_sous_permutation_intra_segment": float(perms.mean()),
                           "chute": r - float(perms.mean()),
                           "p_permutation": (1 + int((np.abs(perms) >= abs(r)).sum()))
                           / (1 + I1.N_PERMUTATIONS)})
    t_p = pd.DataFrame(lignes)
    for cible in t_p["cible"].unique():
        s = t_p["cible"] == cible
        t_p.loc[s, "p_holm"] = I1.holm(t_p.loc[s, "p_permutation"].values)
        t_p.loc[s, "p_bh"] = I1.benjamini_hochberg(t_p.loc[s, "p_permutation"].values)
    I1.ecrire(t_p, "i1-profil-changeurs.csv")
    print(t_p[t_p.cible == "changement monotone"].to_string(index=False), flush=True)

    # ---------------------------------------- 3. position initiale, item par item
    lignes = []
    rare, majo = profs["rare"], profs["majoritaire"]
    for j, it in enumerate(noyau):
        c = cls[:, j]
        ev = c >= 0
        if ev.sum() < I1.MIN_PERSONNES_ITEM:
            continue
        for etiquette, m in (("modalite rare, moins de 10 pour cent", rare[:, j]),
                             ("modalite majoritaire", majo[:, j])):
            a = ev & m
            b = ev & ~m
            if a.sum() < 30 or b.sum() < 30:
                continue
            lignes.append({
                "item": it, "position_initiale": etiquette,
                "n_porteurs": int(a.sum()), "n_autres": int(b.sum()),
                "taux_changement_porteurs": float((c[a] > 0).mean()),
                "taux_changement_autres": float((c[b] > 0).mean()),
                "taux_monotone_porteurs": float((c[a] == 1).mean()),
                "taux_monotone_autres": float((c[b] == 1).mean()),
            })
    t_pos = pd.DataFrame(lignes)
    I1.ecrire(t_pos, "i1-position-initiale.csv")
    for etq, d in t_pos.groupby("position_initiale"):
        w = d["n_porteurs"] + d["n_autres"]
        print(f"{etq} : changement {np.average(d.taux_changement_porteurs, weights=w):.4f} "
              f"contre {np.average(d.taux_changement_autres, weights=w):.4f}, "
              f"monotone {np.average(d.taux_monotone_porteurs, weights=w):.4f} "
              f"contre {np.average(d.taux_monotone_autres, weights=w):.4f} "
              f"sur {len(d)} items", flush=True)

    # ------------------------------------------- 4. deciles de cross pression
    lignes = []
    for nom, v in (("cross pression", profs["cross_pression"]),
                   ("distance au patron modal du segment",
                    profs["distance_patron_segment"])):
        ok = np.isfinite(v)
        bornes = np.percentile(v[ok], np.arange(0, 101, 10))
        idx = np.clip(np.searchsorted(bornes, v, side="right") - 1, 0, 9)
        for d in range(10):
            m = ok & (idx == d)
            if m.sum() < 30:
                continue
            lignes.append({"variable": nom, "decile": d + 1, "n": int(m.sum()),
                           "valeur_moyenne": float(v[m].mean()),
                           "taux_changement": float(t_chg[m].mean()),
                           "taux_monotone": float(t_mono[m].mean())})
    I1.ecrire(pd.DataFrame(lignes), "i1-deciles-cross-pression.csv")

    # ------------------------------- 5. le bruit propre de la personne, trois vagues
    ordre = rng.permutation(len(noyau))
    moities = [np.sort(ordre[:len(noyau) // 2]), np.sort(ordre[len(noyau) // 2:])]
    b = bruit_propre(noyau, brut, tables, moities)
    lignes = []
    for cible in ("monotone_autre_moitie", "changement_autre_moitie"):
        r = spearman(b["aller_retour"].values, b[cible].values)
        tir = np.empty(400)
        idx = np.arange(len(b))
        for t in range(400):
            s = rng.choice(idx, len(idx), replace=True)
            tir[t] = spearman(b["aller_retour"].values[s], b[cible].values[s])
        lignes.append({"quantite": "rho entre aller retour d'une moitie d'items et "
                       + cible.replace("_", " "),
                       "n_personnes": len(b) // 2, "rho_spearman": r,
                       "ic_bas": float(np.percentile(tir, 2.5)),
                       "ic_haut": float(np.percentile(tir, 97.5))})
    t_b = pd.DataFrame(lignes)
    I1.ecrire(t_b, "i1-bruit-propre.csv")
    print(t_b.to_string(index=False), flush=True)
    print("\ni1_profils termine", flush=True)


if __name__ == "__main__":
    main()
