"""
a9_coherence : A11, l'incoherence au bon endroit. Structure de correlation inter items,
humains contre agents, sur Twin-2K-500.

Deux volets, imposes par ce que contient le jeu :
  - volet humain seul, sur les echelles de personnalite des vagues 1 a 3 (BFI-44 et les
    quinze autres matrices du bloc Personality). Aucune configuration LLM publiee par les
    auteurs ne simule ces items : les simulations ne portent que sur la vague 4.
  - volet humains contre agents, sur les sept batteries multi items de la vague 4, qui
    sont simulees par les treize configurations distinctes du depot.

Aucun appel de modele de langage. Sorties agregees dans resultats/, plus la figure
a9-figure-coherence en PNG et SVG.

Usage : .venv/bin/python analyses/a9_coherence.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_commun as A  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402

RES = A.RACINE / "resultats"
GRAINE = 20260907

# Palette : reprise de a2_figures pour que les figures du projet restent une seule famille.
FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
SLOT = ["#2a78d6", "#eb6834", "#1baf7a"]   # trois premieres teintes categorielles
# Rampe divergente bleu <-> rouge, point neutre gris, conforme au referentiel de palette.
DIVERGENTE = LinearSegmentedColormap.from_list(
    "bleu_rouge", ["#0d366b", "#2a78d6", "#9ec5f4", "#f0efec", "#f0a3a2", "#e34948", "#8c1f1f"])

RID287 = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]

ECHELLES_W4 = {
    "QID287_soutien_politiques": [f"QID287_{i}" for i in RID287],
    "QID288_benefice_percu": [f"QID288_{i}" for i in range(1, 5)],
    "QID289_risque_percu": [f"QID289_{i}" for i in range(1, 5)],
    "QID290_consensus_percu": [f"QID290_{i}" for i in RID287],
    "QID9_intention_achat": [f"QID9_{i}" for i in range(1, 41)],
    "QID198_appariement_1": [f"QID198_{i}" for i in range(1, 11)],
    "QID203_appariement_2": [f"QID203_{i}" for i in range(1, 7)],
}

# Paires de contenu apparie entre deux echelles : meme objet, question differente.
APPARIEMENTS = (
    [(f"QID287_{i}", f"QID290_{i}") for i in RID287]          # opinion propre / consensus percu
    + [(f"QID288_{i}", f"QID289_{i}") for i in range(1, 5)]   # benefice / risque du meme objet
)


# ---------------------------------------------------------------------------
# Outils
# ---------------------------------------------------------------------------

def cles_de_signe(corr, colonnes):
    """Signe a appliquer a chaque item pour que l'echelle soit cotee dans un seul sens.

    Le signe est celui du premier vecteur propre de la matrice de correlation humaine.
    Il est estime une fois sur les humains et applique tel quel aux agents, faute de
    quoi deux alphas ne seraient pas comparables.
    """
    m = corr.loc[colonnes, colonnes].fillna(0.0).to_numpy(dtype=float)
    vals, vecs = np.linalg.eigh(m)
    v = vecs[:, -1]
    if (v > 0).sum() < len(v) / 2:
        v = -v
    return pd.Series(np.where(v >= 0, 1.0, -1.0), index=colonnes)


def alpha_et_r_moyen(df, colonnes, cles):
    X = df[colonnes].mul(cles[colonnes], axis=1)
    a, k, n = A.alpha_cronbach(X)
    c = X.corr(min_periods=100)
    hors = c.where(~np.eye(len(c), dtype=bool)).stack()
    return a, k, n, float(hors.mean()), float(hors.std(ddof=1))


def categorie_paire(a, b, appartenance, apparies):
    if appartenance.get(a) == appartenance.get(b):
        return "intra_echelle"
    if (a, b) in apparies or (b, a) in apparies:
        return "inter_echelle_meme_objet"
    return "inter_echelle"


def concentration(delta):
    """Part de l'exces total de coherence portee par le decile de paires le plus charge."""
    d = np.sort(np.asarray([x for x in delta if x > 0], dtype=float))[::-1]
    if len(d) < 10 or d.sum() <= 0:
        return np.nan, np.nan
    k = max(1, int(round(0.10 * len(d))))
    part_decile = float(d[:k].sum() / d.sum())
    # Gini sur les exces positifs, 0 = uniforme, 1 = tout dans une paire.
    x = np.sort(d)
    n = len(x)
    gini = float((2 * np.arange(1, n + 1) - n - 1).dot(x) / (n * x.sum()))
    return part_decile, gini


# ---------------------------------------------------------------------------
# Volet 1 : structure humaine des echelles de personnalite, vagues 1 a 3
# ---------------------------------------------------------------------------

def volet_personnalite(w13, catalogue):
    lignes = []
    cle_bfi = A.cle_bfi()
    corr_bfi = w13[list(cle_bfi)].corr(min_periods=100)
    for facette, items in A.BFI44.items():
        cols = [f"QID25_{abs(i)}" for i in items]
        signes = pd.Series([1.0 if i > 0 else -1.0 for i in items], index=cols)
        a, k, n, rm, rsd = alpha_et_r_moyen(w13, cols, signes)
        lignes.append(dict(echelle=f"BFI44_{facette}", source="humains_vagues1_3",
                           n_items=k, n_repondants=n, alpha=round(a, 4),
                           r_inter_items_moyen=round(rm, 4), ecart_type_r=round(rsd, 4),
                           cotation="cles canoniques du BFI-44"))
    a, k, n, rm, rsd = alpha_et_r_moyen(w13, list(cle_bfi),
                                        pd.Series({c: s for c, (f, s) in cle_bfi.items()}))
    lignes.append(dict(echelle="BFI44_total", source="humains_vagues1_3", n_items=k,
                       n_repondants=n, alpha=round(a, 4), r_inter_items_moyen=round(rm, 4),
                       ecart_type_r=round(rsd, 4), cotation="cles canoniques du BFI-44"))

    # Les autres matrices du bloc Personality : cotation alignee empiriquement.
    for q in catalogue:
        if q.get("BlockName", "").strip() != "Personality" or q["QuestionType"] != "Matrix":
            continue
        if q["QuestionID"] == "QID25":
            continue
        cols = [c for c in q["csv_columns"] if c in w13.columns]
        if len(cols) < 4:
            continue
        corr = w13[cols].corr(min_periods=100)
        signes = cles_de_signe(corr, cols)
        a, k, n, rm, rsd = alpha_et_r_moyen(w13, cols, signes)
        lignes.append(dict(echelle=f"{q['QuestionID']}_personnalite", source="humains_vagues1_3",
                           n_items=k, n_repondants=n, alpha=round(a, 4),
                           r_inter_items_moyen=round(rm, 4), ecart_type_r=round(rsd, 4),
                           cotation=f"signes alignes sur la 1re composante ; "
                                    f"{int((signes < 0).sum())} items retournes"))

    # Ou se situent les correlations du BFI : meme facette, facettes differentes,
    # items inverses ou non. C'est la reference humaine de la question A11.
    facette_de = {c: f for c, (f, s) in cle_bfi.items()}
    signe_de = {c: s for c, (f, s) in cle_bfi.items()}
    p = A.paires(corr_bfi)
    p["meme_facette"] = [facette_de[a] == facette_de[b] for a, b in zip(p.item_a, p.item_b)]
    p["meme_sens"] = [signe_de[a] == signe_de[b] for a, b in zip(p.item_a, p.item_b)]
    resume = []
    for (mf, ms), g in p.groupby(["meme_facette", "meme_sens"]):
        resume.append(dict(source="humains_vagues1_3",
                           bloc="meme facette" if mf else "facettes differentes",
                           keyage="meme sens" if ms else "sens inverses",
                           n_paires=len(g), r_moyen=round(float(g.r.mean()), 4),
                           r_absolu_moyen=round(float(g.r.abs().mean()), 4),
                           r_p10=round(float(g.r.quantile(.10)), 4),
                           r_p90=round(float(g.r.quantile(.90)), 4)))
    return pd.DataFrame(lignes), pd.DataFrame(resume)


# ---------------------------------------------------------------------------
# Volet 2 : humains contre agents sur les batteries de la vague 4
# ---------------------------------------------------------------------------

def matrice_pooled(df, colonnes):
    return df[colonnes].corr(min_periods=100)


def volet_vague4(w4, configs):
    appartenance = {c: nom for nom, cols in ECHELLES_W4.items() for c in cols}
    tous = [c for c in appartenance if c in w4.columns]
    apparies = set(APPARIEMENTS)

    corr_h = matrice_pooled(w4, tous)
    cles = {}
    for nom, cols in ECHELLES_W4.items():
        cols = [c for c in cols if c in tous]
        cles[nom] = cles_de_signe(corr_h, cols)
    cle_globale = pd.concat(cles.values())

    paires_h = A.paires(corr_h)
    paires_h["categorie"] = [categorie_paire(a, b, appartenance, apparies)
                             for a, b in zip(paires_h.item_a, paires_h.item_b)]
    paires_h["echelle_a"] = paires_h.item_a.map(appartenance)
    paires_h["echelle_b"] = paires_h.item_b.map(appartenance)

    lignes_alpha, lignes_struct, lignes_cat = [], [], []
    lignes_couples, lignes_inverses = [], []
    paires_tout = {"humains": corr_h}

    def ajoute_alphas(source, df):
        for nom, cols in ECHELLES_W4.items():
            cols = [c for c in cols if c in df.columns and c in tous]
            if len(cols) < 4:
                continue
            a, k, n, rm, rsd = alpha_et_r_moyen(df, cols, cle_globale)
            lignes_alpha.append(dict(echelle=nom, source=source, n_items=k, n_repondants=n,
                                     alpha=round(a, 4) if not np.isnan(a) else "",
                                     r_inter_items_moyen=round(rm, 4),
                                     ecart_type_r=round(rsd, 4)))

    ajoute_alphas("humains_vague4", w4)

    for nomc, fichier in sorted(configs.items()):
        llm = A.charger_llm(fichier)
        cols = [c for c in tous if c in llm.columns]
        if len(cols) < len(tous) * 0.8:
            print(f"[avert] {nomc} : {len(cols)} items sur {len(tous)}")
        idx = llm.index.intersection(w4.index)
        sub = llm.loc[idx, cols]
        ajoute_alphas(nomc, sub)
        corr_a = matrice_pooled(sub, cols)
        paires_tout[nomc] = corr_a
        pa = A.paires(corr_a).set_index(["item_a", "item_b"])["r"]
        p = paires_h.copy()
        p["r_agent"] = [pa.get((a, b), np.nan) for a, b in zip(p.item_a, p.item_b)]
        p = p.dropna(subset=["r", "r_agent"])
        p["delta_abs"] = p.r_agent.abs() - p.r.abs()

        r_des_r = float(np.corrcoef(p.r, p.r_agent)[0, 1])
        rmse = float(np.sqrt(((p.r_agent - p.r) ** 2).mean()))
        part, gini = concentration(p.delta_abs.to_numpy())
        pente = float(np.polyfit(p.r, p.r_agent, 1)[0])
        lignes_struct.append(dict(configuration=nomc, n_paires=len(p),
                                  r_moyen_humain=round(float(p.r.abs().mean()), 4),
                                  r_moyen_agent=round(float(p.r_agent.abs().mean()), 4),
                                  exces_moyen=round(float(p.delta_abs.mean()), 4),
                                  correlation_des_correlations=round(r_des_r, 4),
                                  pente_agent_sur_humain=round(pente, 4),
                                  rmse=round(rmse, 4),
                                  part_exces_decile_haut=round(part, 4) if not np.isnan(part) else "",
                                  gini_exces=round(gini, 4) if not np.isnan(gini) else "",
                                  part_paires_plus_coherentes=round(float((p.delta_abs > 0).mean()), 4)))
        for cat, g in p.groupby("categorie"):
            lignes_cat.append(dict(configuration=nomc, categorie=cat, n_paires=len(g),
                                   r_absolu_humain=round(float(g.r.abs().mean()), 4),
                                   r_absolu_agent=round(float(g.r_agent.abs().mean()), 4),
                                   exces_moyen=round(float(g.delta_abs.mean()), 4)))
        # detail par couple de batteries : l'agregat par categorie est trompeur,
        # les 780 paires de la batterie de prix ecrasent les 45 paires d'attitudes.
        for (ea, eb), g in p.groupby(["echelle_a", "echelle_b"]):
            lignes_couples.append(dict(configuration=nomc, echelle_a=ea, echelle_b=eb,
                                       n_paires=len(g),
                                       r_absolu_humain=round(float(g.r.abs().mean()), 4),
                                       r_absolu_agent=round(float(g.r_agent.abs().mean()), 4),
                                       exces_moyen=round(float(g.delta_abs.mean()), 4)))
        # dans la batterie d'attitudes, les paires d'items cotes en sens inverse
        cols287 = [c for c in ECHELLES_W4["QID287_soutien_politiques"] if c in tous]
        q = p[(p.echelle_a == "QID287_soutien_politiques") &
              (p.echelle_b == "QID287_soutien_politiques")].copy()
        if len(q):
            q["meme_sens"] = [cle_globale[a] == cle_globale[b]
                              for a, b in zip(q.item_a, q.item_b)]
            for ms, g in q.groupby("meme_sens"):
                lignes_inverses.append(dict(configuration=nomc,
                                            keyage="meme sens" if ms else "sens inverses",
                                            n_paires=len(g),
                                            r_absolu_humain=round(float(g.r.abs().mean()), 4),
                                            r_absolu_agent=round(float(g.r_agent.abs().mean()), 4),
                                            exces_moyen=round(float(g.delta_abs.mean()), 4)))
        if nomc == "gpt41mini_defaut":
            g = p.sort_values("delta_abs", ascending=False)
            g.head(25)[["item_a", "item_b", "categorie", "r", "r_agent", "delta_abs"]].round(4)\
                .to_csv(RES / "a9-coherence-paires-extremes.csv", index=False)
            p.to_pickle(RES / ".a9_paires_reference.pkl")
        print(f"[info] {nomc} : exces moyen {p.delta_abs.mean():+.4f}, "
              f"r des r {r_des_r:.3f}")

    pd.DataFrame(lignes_couples).to_csv(
        RES / "a9-coherence-par-couple-echelles.csv", index=False)
    pd.DataFrame(lignes_inverses).to_csv(
        RES / "a9-coherence-items-inverses.csv", index=False)
    return (pd.DataFrame(lignes_alpha), pd.DataFrame(lignes_struct),
            pd.DataFrame(lignes_cat), corr_h, paires_tout, cle_globale)


# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------

def figure(corr_h, corr_a, paires_ref, nom_config):
    cols = [c for c in ECHELLES_W4["QID287_soutien_politiques"] if c in corr_h.columns]
    etiquettes = ["carbone", "energie 40 %", "electricite 2035", "Medicare for All",
                  "option publique", "regularisation", "conge parental", "impot 2 %",
                  "expulsions", "cheques sante"]
    fig = plt.figure(figsize=(13.5, 5.0))
    grille = fig.add_gridspec(1, 3, width_ratios=[1, 1, 1.05], wspace=0.46)

    for k, (mat, titre) in enumerate(((corr_h.loc[cols, cols], "Humains"),
                                      (corr_a.loc[cols, cols], f"Agents, {nom_config}"))):
        ax = fig.add_subplot(grille[0, k])
        m = mat.to_numpy(dtype=float).copy()
        np.fill_diagonal(m, np.nan)
        im = ax.imshow(m, cmap=DIVERGENTE, vmin=-1, vmax=1)
        ax.set_xticks(range(len(cols)))
        ax.set_yticks(range(len(cols)))
        ax.set_xticklabels(etiquettes, rotation=60, ha="right", fontsize=7.5,
                           color=ENCRE_SECONDE)
        ax.set_yticklabels(etiquettes, fontsize=7.5, color=ENCRE_SECONDE)
        for i in range(len(cols)):
            for j in range(len(cols)):
                if i == j:
                    continue
                v = m[i, j]
                ax.text(j, i, f"{v:.2f}".replace("0.", ".").replace("-.", "-."),
                        ha="center", va="center", fontsize=6,
                        color="#ffffff" if abs(v) > 0.55 else ENCRE)
        hors = mat.where(~np.eye(len(mat), dtype=bool)).stack()
        ax.set_title(f"{titre}\nr moyen en valeur absolue {hors.abs().mean():.2f}",
                     fontsize=10, color=ENCRE, pad=10)
        for cote in ax.spines.values():
            cote.set_visible(False)
        if k == 1:
            cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
            cb.set_label("correlation de Pearson", fontsize=8, color=ENCRE_SECONDE)
            cb.ax.tick_params(labelsize=7, colors=ENCRE_SECONDE)
            cb.outline.set_visible(False)

    ax = fig.add_subplot(grille[0, 2])
    ax.set_facecolor(FOND)
    ax.grid(True, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=8)
    noms = {"intra_echelle": "meme batterie",
            "inter_echelle_meme_objet": "batteries differentes, meme objet",
            "inter_echelle": "batteries differentes"}
    for i, cat in enumerate(["inter_echelle", "intra_echelle", "inter_echelle_meme_objet"]):
        g = paires_ref[paires_ref.categorie == cat]
        ax.scatter(g.r, g.r_agent, s=13 if cat != "inter_echelle" else 6,
                   c=SLOT[i], alpha=0.55 if cat == "inter_echelle" else 0.85,
                   linewidths=0.5, edgecolors=FOND, label=noms[cat], zorder=3 + i)
    lim = (-1.02, 1.02)
    ax.plot(lim, lim, color=ENCRE_SECONDE, linewidth=1.2, linestyle="--", zorder=2)
    ax.axhline(0, color=GRILLE, linewidth=1, zorder=1)
    ax.axvline(0, color=GRILLE, linewidth=1, zorder=1)
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_xlabel("correlation entre deux items, humains", fontsize=9, color=ENCRE_SECONDE)
    ax.set_ylabel(f"idem, agents ({nom_config})", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("Une paire d'items, un point\nau-dessus de la diagonale :\nagents plus coherents",
                 fontsize=10, color=ENCRE, pad=8)
    leg = ax.legend(fontsize=8, loc="upper left", frameon=False, labelcolor=ENCRE_SECONDE)
    for t in leg.get_texts():
        t.set_color(ENCRE_SECONDE)

    fig.patch.set_facecolor(FOND)
    for ext in ("png", "svg"):
        chemin = RES / f"a9-figure-coherence.{ext}"
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


# ---------------------------------------------------------------------------

def main():
    RES.mkdir(exist_ok=True)
    cat = A.charger_catalogue()
    w13 = A.charger_humains("1_3", cat)
    w4 = A.charger_humains("4", cat)

    alphas_p, struct_p = volet_personnalite(w13, cat)
    alphas_p.to_csv(RES / "a9-coherence-personnalite-humains.csv", index=False)
    struct_p.to_csv(RES / "a9-coherence-bfi-structure-humaine.csv", index=False)
    print("[ok] volet personnalite")

    configs = A.configs_llm_disponibles()
    # deux couples de fichiers sont identiques octet pour octet dans le depot
    configs.pop("gpt41mini_demo_seules_spec", None)
    configs.pop("gpt41mini_texte", None)
    alphas4, struct4, cats4, corr_h, mats, cle = volet_vague4(w4, configs)
    alphas4.to_csv(RES / "a9-coherence-alpha-vague4.csv", index=False)
    struct4.to_csv(RES / "a9-coherence-structure-vague4.csv", index=False)
    cats4.to_csv(RES / "a9-coherence-par-categorie-de-paire.csv", index=False)

    ref = "gpt41mini_defaut"
    paires_ref = pd.read_pickle(RES / ".a9_paires_reference.pkl")
    figure(corr_h, mats[ref], paires_ref, ref)
    (RES / ".a9_paires_reference.pkl").unlink(missing_ok=True)
    print("[ok] tableaux et figure ecrits dans resultats/")


if __name__ == "__main__":
    main()
