"""r1b. Ou le modele se trompe : par item, par modalite, et le contraste apparie des deux modes.

Aucun appel de modele. Lecture seule sur `data/traces/` et `resultats/`. Quatre coeurs.
Aucun fichier existant n'est modifie ; les sorties portent toutes le prefixe `r1b-`.

Quatre blocs.

1. **Par item.** L'erreur de description, distance de variation totale entre le portrait et
   la realite, item par item et camp par camp, avec de quoi la lire : la part de la modalite
   majoritaire reelle (le taux de base), la famille de l'item, la derive agregee de `a37`,
   et le plancher de reinterrogation du meme item.

2. **Par modalite, l'etalonnage du taux de base.** Toutes les paires
   (part reelle, part decrite) du run, rangees par decile de part reelle. C'est le test de
   generalite du signal `a46` : les syndiques valent 5 pour cent reels et Qwen3-4B en
   annonce 60 a 75. Si le modele gonfle systematiquement les modalites rares et rabote les
   modalites massives, la courbe est au dessus de la diagonale a gauche et en dessous a
   droite, et le signal des syndiques n'est qu'un cas d'une regle generale.

3. **La direction de l'effet d'identite.** H3 ne predit aucune direction et n'en mesure
   aucune : elle mesure une distance. Ce bloc regarde le signe, sur l'echelle de position
   orientee de `a37` : quand c'est un adversaire qui demande, le camp decrit est il pousse
   plus loin de l'autre camp, ou plus pres ?

4. **Le contraste apparie des deux modes**, item par item, sur les 29 items a pole declare
   de `a38`. Le facteur d'incarnation de `a38` (C2, agents etiquetes ; C3, agents nourris de
   119 reponses) est reconstruit item par item a partir de `a38-par-camp.csv` et de
   `a38-desirabilite-humaine-par-camp.csv`, puis compare item par item au facteur de
   description de r1 pour le meme modele. Le rapport des deux facteurs recoit un intervalle
   de bootstrap sur les items et un p de permutation de signe appariee.

Sorties :
  resultats/r1b-erreurs-par-item.csv
  resultats/r1b-etalonnage-taux-de-base.csv
  resultats/r1b-direction-identite.csv
  resultats/r1b-contraste-apparie-modes.csv
  resultats/r1b-figure-modes.png et .svg
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

import a25_commun as A25
import a25_mesures as A25M
import a38_commun as A38
import r1_evaluer as R1
from r1_oracle_camps import CAMPS, IDENTITES
from r1b_contraste_mode import table_desirabilite, desirabilite

RACINE, SORTIE = R1.RACINE, R1.SORTIE
GRAINE = 20260909


def charger():
    traces = R1.lire_traces("")
    ref, options, effectifs = R1.lire_referent()
    sens, oriente, strict, derive = R1.lire_a37()
    retenues = {}
    for t in traces:
        if t["rejet"] or not t.get("distribution"):
            continue
        if t.get("n_tentatives", 1) > 1 and R1.recopie_exemple(t["distribution"]):
            continue
        p = np.array([t["distribution"][o] for o in options[t["item"]]], float)
        retenues[(t["cle_modele"], t["modele"], t["identite"], t["camp"], t["item"])] = p
    familles = {t["item"]: t.get("famille") for t in traces}
    return (traces, retenues, ref, options, effectifs, sens, oriente, strict, derive,
            familles)


# ---------------------------------------------------------------------------
# 1. Erreur par item
# ---------------------------------------------------------------------------

def erreurs_par_item(retenues, ref, options, derive, sens, familles):
    lignes = []
    for (cle, modele, identite, camp, item), p in retenues.items():
        r1_ = ref[(item, camp, "w1")]
        r2_ = ref[(item, camp, "w2")]
        k = int(np.argmax(r1_))
        lignes.append({
            "modele": modele, "cle_modele": cle, "identite": identite,
            "camp": camp, "item": item, "famille": familles.get(item),
            "n_modalites": len(p),
            "tv_decrit_reel": R1.tv(p, r1_),
            "tv_plancher_w1_w2": R1.tv(r1_, r2_),
            "part_modale_reelle": float(r1_.max()),
            "modalite_modale_reelle": options[item][k],
            "part_decrite_de_cette_modalite": float(p[k]),
            "part_modale_decrite": float(p.max()),
            "gs_decrit": R1.gini_simpson(p),
            "gs_reel_w1": R1.gini_simpson(r1_),
            "pos_decrit": R1.position(p, sens.get(item, 0)),
            "pos_reel_w1": R1.position(r1_, sens.get(item, 0)),
            "derive_agregee": float(derive.get(item, np.nan)),
        })
    d = pd.DataFrame(lignes)
    d["exces_de_variete"] = d["gs_decrit"] - d["gs_reel_w1"]
    d["deficit_sur_la_modale"] = d["part_decrite_de_cette_modalite"] - d["part_modale_reelle"]
    return d.sort_values("tv_decrit_reel", ascending=False)


# ---------------------------------------------------------------------------
# 2. Etalonnage du taux de base, modalite par modalite
# ---------------------------------------------------------------------------

def etalonnage(retenues, ref, options):
    reelles, decrites, cles = [], [], []
    for (cle, modele, identite, camp, item), p in retenues.items():
        r = ref[(item, camp, "w1")]
        reelles.append(r)
        decrites.append(p)
        cles += [(modele, camp)] * len(r)
    reel = np.concatenate(reelles)
    dec = np.concatenate(decrites)
    modeles = np.array([c[0] for c in cles])

    bornes = np.array([0.0, 0.01, 0.02, 0.05, 0.10, 0.20, 0.30, 0.40,
                       0.50, 0.60, 0.75, 1.01])
    lignes = []
    for etiquette, masque in [("tous modeles", np.ones(len(reel), bool))] + \
            [(m, modeles == m) for m in sorted(set(modeles))]:
        for i in range(len(bornes) - 1):
            b, h = bornes[i], bornes[i + 1]
            sel = masque & (reel >= b) & (reel < h)
            if sel.sum() < 5:
                continue
            lignes.append({
                "perimetre": etiquette,
                "bande_part_reelle": f"[{b:.2f} ; {h:.2f}[",
                "n_modalites": int(sel.sum()),
                "part_reelle_moyenne": float(reel[sel].mean()),
                "part_decrite_moyenne": float(dec[sel].mean()),
                "rapport_decrit_sur_reel": float(dec[sel].mean() / reel[sel].mean())
                if reel[sel].mean() > 0 else np.nan,
                "ecart_en_points": float(100 * (dec[sel].mean() - reel[sel].mean())),
                "part_decrite_mediane": float(np.median(dec[sel])),
            })
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 3. Direction de l'effet d'identite
# ---------------------------------------------------------------------------

def direction_identite(retenues, ref, sens, rng):
    """Sur l'echelle orientee de a37, le portrait bouge t il vers le pole du camp decrit ?

    Convention : `pos` monte vers la droite. Pour le camp de gauche, un deplacement vers son
    propre pole est **negatif** ; pour le camp de droite, il est **positif**. La colonne
    `vers_le_pole_du_camp` porte le deplacement deja signe dans ce sens, de sorte qu'une
    valeur positive veuille toujours dire « le camp est decrit plus caricatural quand c'est
    l'adversaire qui demande ».
    """
    lignes = []
    modeles = sorted({(c, m) for c, m, _, _, _ in retenues})
    items = sorted({i for *_, i in retenues})
    for cle, modele in modeles:
        for camp in ("gauche", "droite"):
            d, garde = [], []
            for it in items:
                s = sens.get(it, 0)
                if not np.isfinite(s) or s == 0:
                    continue
                kj = (cle, modele, "journaliste", camp, it)
                ka = (cle, modele, "adversaire", camp, it)
                if kj not in retenues or ka not in retenues:
                    continue
                pj = R1.position(retenues[kj], s)
                pa = R1.position(retenues[ka], s)
                signe = 1.0 if camp == "droite" else -1.0
                d.append(signe * (pa - pj))
                garde.append(it)
            if len(d) < 3:
                continue
            d = np.array(d)
            idx = rng.integers(0, len(d), size=(2000, len(d)))
            tir = d[idx].mean(axis=1)
            lignes.append({
                "modele": modele, "cle_modele": cle, "camp": camp, "n_items": len(d),
                "vers_le_pole_du_camp": float(d.mean()),
                "ic_bas": float(np.percentile(tir, 2.5)),
                "ic_haut": float(np.percentile(tir, 97.5)),
                "part_items_vers_le_pole": float(np.mean(d > 0)),
                "p": R1.p_permutation_signe(d, rng),
            })
    return pd.DataFrame(R1.poser_holm(lignes))


# ---------------------------------------------------------------------------
# 4. Contraste apparie des deux modes, item par item
# ---------------------------------------------------------------------------

def facteurs_a38_par_item(perimetre=150):
    """Reconstruit, item par item, l'ecart entre camps simule de chaque condition de a38.

    `a38-par-camp.csv` donne `ecart_desirabilite` = desirabilite simulee moins desirabilite
    humaine, par condition, item et camp. `a38-desirabilite-humaine-par-camp.csv` donne la
    desirabilite humaine de la vague 1. La somme des deux rend la desirabilite simulee, et
    l'ecart entre camps s'en deduit. Les valeurs agregees sont ensuite verifiees contre
    `a38-camp.csv`, publie.
    """
    pc = pd.read_csv(os.path.join(SORTIE, "a38-par-camp.csv"))
    hu = pd.read_csv(os.path.join(SORTIE, "a38-desirabilite-humaine-par-camp.csv"))
    pc = pc[pc["perimetre"] == perimetre]
    hu = hu[hu["perimetre"] == perimetre]
    h = hu.pivot(index="item", columns="camp", values="desirabilite_humaine")
    gap_hum = (h["gauche"] - h["droite"]).rename("gap_humain")
    sortie = {}
    for cond, g in pc.groupby("condition"):
        e = g.pivot(index="item", columns="camp", values="ecart_desirabilite")
        gap_sim = gap_hum + (e["gauche"] - e["droite"])
        sortie[cond] = pd.DataFrame({"gap_simule": gap_sim, "gap_humain": gap_hum}).dropna()
    return sortie


def contraste_apparie(retenues, ref, options, rng):
    items29 = [it for it in sorted(A38.POLE_ENDOGROUPE) if it in options]
    table = table_desirabilite(items29, options)
    a38par = facteurs_a38_par_item(150)

    # r1, mode description : ecart de desirabilite decrit et reel, item par item
    r1gap = {}
    for cle, modele, identite, camp, it in list(retenues):
        pass
    modeles = sorted({(c, m) for c, m, _, _, _ in retenues})
    for cle, modele in modeles:
        for identite in IDENTITES:
            lignes = {}
            for it in items29:
                if it not in table:
                    continue
                vec, defini = table[it]
                kg = (cle, modele, identite, "gauche", it)
                kd = (cle, modele, identite, "droite", it)
                if kg not in retenues or kd not in retenues:
                    continue
                lignes[it] = (
                    desirabilite(retenues[kg], vec, defini)
                    - desirabilite(retenues[kd], vec, defini),
                    desirabilite(ref[(it, "gauche", "w1")], vec, defini)
                    - desirabilite(ref[(it, "droite", "w1")], vec, defini),
                )
            r1gap[(cle, identite)] = pd.DataFrame(
                lignes, index=["gap_simule", "gap_humain"]).T

    lignes = []
    for (cle, identite), dfr in sorted(r1gap.items()):
        modele = [m for c, m in modeles if c == cle][0]
        for cond in ("C2", "C3"):
            if cond not in a38par:
                continue
            dfa = a38par[cond]
            communs = sorted(set(dfr.index) & set(dfa.index))
            if len(communs) < 3:
                continue
            # facteur de chaque mode, calcule sur les memes items, contre son propre humain
            a_desc = dfr.loc[communs, "gap_simule"].to_numpy()
            b_desc = dfr.loc[communs, "gap_humain"].to_numpy()
            a_inc = dfa.loc[communs, "gap_simule"].to_numpy()
            b_inc = dfa.loc[communs, "gap_humain"].to_numpy()
            f_desc = a_desc.mean() / b_desc.mean()
            f_inc = a_inc.mean() / b_inc.mean()
            idx = rng.integers(0, len(communs), size=(4000, len(communs)))
            fd = a_desc[idx].mean(axis=1) / b_desc[idx].mean(axis=1)
            fi = a_inc[idx].mean(axis=1) / b_inc[idx].mean(axis=1)
            rap = fi / fd
            rap = rap[np.isfinite(rap)]
            # p de la difference des ecarts normalises, appariee par item
            d = a_inc / b_inc.mean() - a_desc / b_desc.mean()
            lignes.append({
                "modele_description": modele, "cle_modele": cle, "identite": identite,
                "condition_incarnation": cond,
                "modele_incarnation": "Qwen3-4B-Instruct-2507 (a38, 150 personnes)",
                "n_items": len(communs),
                "facteur_description_r1": float(f_desc),
                "facteur_incarnation_a38": float(f_inc),
                "rapport_incarnation_sur_description": float(f_inc / f_desc),
                "ic_bas": float(np.percentile(rap, 2.5)),
                "ic_haut": float(np.percentile(rap, 97.5)),
                "p_difference_appariee": R1.p_permutation_signe(d, rng),
            })
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 5. Figure
# ---------------------------------------------------------------------------

def figure(cm, etal, chemin):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.4))

    # (a) les deux modes sur la meme echelle
    ax = axes[0]
    a38c = pd.read_csv(os.path.join(SORTIE, "a38-camp.csv"))
    a38c = a38c[(a38c["perimetre"] == 150) & (a38c["condition"].isin(["C2", "C3"]))]
    reperes = []
    for cond, nom, coul in (("C2", "a38 C2, incarnation, persona etiquete", "#b2182b"),
                            ("C3", "a38 C3, incarnation, 119 reponses", "#ef8a62")):
        r = a38c[a38c["condition"] == cond].iloc[0]
        # a38 publie l'intervalle sur `difference_droite_moins_gauche` ; le facteur en est
        # une fonction affine decroissante, l'intervalle se transporte donc exactement.
        h = float(r["ecart_humain_entre_camps"])
        reperes.append((nom, float(r["facteur_amplification"]),
                        (h - float(r["ic_haut"])) / h, (h - float(r["ic_bas"])) / h, coul))
    cmj = cm[cm["identite"] == "journaliste"].sort_values("facteur")
    y, etiquettes, couleurs = [], [], []
    for nom, val, bas, haut, coul in reperes:
        y.append((nom, val, bas, haut, coul))
    for _, r in cmj.iterrows():
        y.append((f"r1 {r['modele']}, description", r["facteur"],
                  r["ic_bas"], r["ic_haut"], "#2166ac"))
    y.sort(key=lambda t: t[1])
    for i, (nom, val, bas, haut, coul) in enumerate(y):
        if np.isfinite(bas):
            ax.plot([bas, haut], [i, i], color=coul, lw=2.2, solid_capstyle="round")
        ax.plot([val], [i], "o", color=coul, ms=8, zorder=3)
        etiquettes.append(nom)
    ax.axvline(1.0, color="#444444", lw=1.2, ls="--")
    ax.text(1.03, -0.42, "plancher humain 0,98 a 1,03", fontsize=8, color="#444444")
    ax.axvspan(0.85, 1.15, color="#dddddd", alpha=0.5, zorder=0)
    ax.set_yticks(range(len(y)))
    ax.set_yticklabels(etiquettes, fontsize=8)
    ax.set_ylim(-0.8, len(y) - 0.4)
    ax.set_xlabel("facteur d'amplification de l'ecart entre camps\n"
                  "(score de desirabilite a25, 29 items a pole declare)", fontsize=9)
    ax.set_title("(a) Deux modes, une seule quantite, les memes 29 items", fontsize=10)

    # (b) etalonnage du taux de base
    ax = axes[1]
    for etiquette, coul in (("Qwen3-4B-Instruct-2507", "#2166ac"),
                            ("gpt-oss-20b", "#b2182b"),
                            ("Qwen3-30B-A3B-Instruct-2507", "#1a9850")):
        g = etal[etal["perimetre"] == etiquette]
        if not len(g):
            continue
        ax.plot(100 * g["part_reelle_moyenne"], 100 * g["part_decrite_moyenne"],
                "o-", color=coul, ms=4, lw=1.6, label=etiquette)
    lim = [0, 80]
    ax.plot(lim, lim, ls="--", color="#444444", lw=1.2, label="etalonnage parfait")
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("part reelle de la modalite, pour cent", fontsize=9)
    ax.set_ylabel("part decrite par le modele, pour cent", fontsize=9)
    ax.set_title("(b) Le taux de base : les modalites rares sont gonflees,\n"
                 "les modalites massives rabotees", fontsize=10)
    ax.legend(fontsize=7.5, loc="upper left")

    for a in axes:
        a.grid(alpha=0.25, lw=0.6)
        for c in ("top", "right"):
            a.spines[c].set_visible(False)
    fig.tight_layout()
    fig.savefig(chemin + ".png", dpi=170)
    fig.savefig(chemin + ".svg")
    print(f"  figure : {chemin}.png et .svg")


# ---------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(GRAINE)
    (traces, retenues, ref, options, effectifs, sens, oriente, strict, derive,
     familles) = charger()
    print(f"{len(traces)} cellules lues, {len(retenues)} retenues")

    err = erreurs_par_item(retenues, ref, options, derive, sens, familles)
    R1.ecrire(err, "r1b-erreurs-par-item.csv", "")

    etal = etalonnage(retenues, ref, options)
    R1.ecrire(etal, "r1b-etalonnage-taux-de-base.csv", "")

    R1.ecrire(direction_identite(retenues, ref, sens, rng),
              "r1b-direction-identite.csv", "")

    ca = contraste_apparie(retenues, ref, options, rng)
    R1.ecrire(ca, "r1b-contraste-apparie-modes.csv", "")

    cm = pd.read_csv(os.path.join(SORTIE, "r1b-contraste-mode.csv"))
    figure(cm, etal, os.path.join(SORTIE, "r1b-figure-modes"))


if __name__ == "__main__":
    main()
