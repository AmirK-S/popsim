"""Analyse descriptive post hoc des checkpoints R7, sans appel de modele.

Lit uniquement les sorties par cellule et par item deja calculees par R1/R7 ainsi que
les metadonnees humaines A37. Les comparaisons R4/R5 utilisent une intersection unique
d'items stricts, pour l'identite journaliste. Aucun test d'hypothese n'est ajoute.
"""

from pathlib import Path
import os

for _var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_var, "2")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import spearmanr


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "resultats"
ORDER = ["olmo3base", "olmo3sft", "olmo3dpo", "olmo3rlvr"]
LABEL = {
    "olmo3base": "Base", "olmo3sft": "SFT", "olmo3dpo": "DPO",
    "olmo3rlvr": "Final", "q4": "R4 gabarit",
    "q4nogab": "R4 sans gabarit", "q4gab3": "R5 gabarit + 3 exemples",
}
TRANSITIONS = [
    ("olmo3base", "olmo3sft", "SFT - Base"),
    ("olmo3sft", "olmo3dpo", "DPO - SFT"),
    ("olmo3dpo", "olmo3rlvr", "Final - DPO"),
]


def q(x, p):
    x = pd.to_numeric(pd.Series(x), errors="coerce").dropna().to_numpy(float)
    return float(np.quantile(x, p)) if len(x) else np.nan


def distribution_row(kind, metric, identity, stratum_type, stratum, transition, values):
    x = pd.to_numeric(pd.Series(values), errors="coerce").dropna().to_numpy(float)
    if not len(x):
        return None
    eps = 1e-12
    return {
        "analyse": kind, "metrique": metric, "identite": identity,
        "strate_type": stratum_type, "strate": str(stratum),
        "contraste": transition, "n": len(x), "moyenne": x.mean(),
        "mediane": np.median(x), "q25": np.quantile(x, .25),
        "q75": np.quantile(x, .75), "moyenne_absolue": np.abs(x).mean(),
        "mediane_absolue": np.median(np.abs(x)),
        "part_positive": np.mean(x > eps), "part_negative": np.mean(x < -eps),
        "part_nulle": np.mean(np.abs(x) <= eps),
    }


def load():
    cells = pd.read_csv(OUT / "r1-par-cellule-r7.csv")
    items = pd.read_csv(OUT / "r1-par-item-ecarts-r7.csv")
    r5 = pd.read_csv(OUT / "r1-par-item-ecarts-r5.csv")
    ori = pd.read_csv(OUT / "a37-orientation-items.csv")
    human = pd.read_csv(OUT / "a37-gss-par-item.csv")
    return cells, items, r5, ori, human


def metadata(ori, human):
    m = ori[["item", "famille", "n_modalites", "oriente", "sens_codeur_A"]].merge(
        human[["item", "retenu_strict", "gs_gauche", "gs_droite"]], on="item",
        validate="one_to_one")
    m["consensus_reel_gs"] = m[["gs_gauche", "gs_droite"]].mean(axis=1)
    # GS faible = consensus fort. Les tertiles sont fixes sur les 79 items orientes.
    oriented = m["oriente"].astype(bool)
    ranks = m.loc[oriented, "consensus_reel_gs"].rank(method="first")
    m.loc[oriented, "consensus"] = pd.qcut(
        ranks, 3, labels=["fort", "intermediaire", "faible"])
    m["polarite"] = m["sens_codeur_A"].map({1: "positive", -1: "negative"})
    m["k_modalites"] = m["n_modalites"].astype(int).astype(str)
    return m


def item_table(items, cells, meta):
    g = items[items["cle_modele"].isin(ORDER)].merge(meta, on="item", validate="many_to_one")
    g = g[g["oriente"].astype(bool)].copy()
    index = ["identite", "item"]
    wide = g.pivot(index=index, columns="cle_modele", values="gap_signe_decrit")
    wide = wide.reindex(columns=ORDER).rename(columns=lambda c: f"gap_{c}").reset_index()
    refs = g.groupby(index, as_index=False)["gap_signe_reel_w1"].first()
    out = wide.merge(refs, on=index, validate="one_to_one").merge(
        meta.drop(columns=["oriente"]), on="item", validate="many_to_one")

    rejects = (cells[cells["cle_modele"].isin(ORDER)]
               .groupby(index + ["cle_modele"], as_index=False)["rejet"].agg(["sum", "mean"])
               .reset_index())
    rej_sum = rejects.pivot(index=index, columns="cle_modele", values="sum")
    rej_rate = rejects.pivot(index=index, columns="cle_modele", values="mean")
    rej_sum.columns = [f"n_rejets_{c}" for c in rej_sum.columns]
    rej_rate.columns = [f"taux_rejet_{c}" for c in rej_rate.columns]
    out = out.merge(rej_sum.reset_index(), on=index, validate="one_to_one")
    out = out.merge(rej_rate.reset_index(), on=index, validate="one_to_one")
    out["complet_4_checkpoints"] = out[[f"gap_{c}" for c in ORDER]].notna().all(axis=1)
    out["rejet_au_moins_un"] = out[[f"n_rejets_{c}" for c in ORDER]].sum(axis=1) > 0
    for a, b, label in TRANSITIONS:
        out[f"delta_{a}_{b}"] = out[f"gap_{b}"] - out[f"gap_{a}"]
    return out.sort_values(index).reset_index(drop=True)


def summaries(item_df, cells, meta):
    rows = []
    complete = item_df[item_df["complet_4_checkpoints"]].copy()
    strata = [
        ("ensemble", lambda d: [("tous", d)]),
        ("famille", lambda d: d.groupby("famille", dropna=False)),
        ("polarite", lambda d: d.groupby("polarite", dropna=False)),
        ("modalites", lambda d: d.groupby("k_modalites", dropna=False)),
        ("consensus_reel", lambda d: d.groupby("consensus", observed=True, dropna=False)),
        ("rejet", lambda d: d.groupby("rejet_au_moins_un", dropna=False)),
    ]
    for identity, d0 in complete.groupby("identite"):
        for stype, grouper in strata:
            for stratum, d in grouper(d0):
                for a, b, label in TRANSITIONS:
                    row = distribution_row(
                        "items_orientes_complets", "gap_signe_decrit", identity,
                        stype, stratum, label, d[f"delta_{a}_{b}"])
                    if row:
                        rows.append(row)

    # Trajectoires camp par camp, sur cellules valides dans les deux checkpoints.
    cm = cells.merge(meta[["item", "sens_codeur_A", "polarite",
                           "k_modalites", "consensus"]],
                     on="item", validate="many_to_one")
    cm["pos_decrit_oriente"] = cm["pos_decrit"] * cm["sens_codeur_A"]
    for identity in ("journaliste", "adversaire"):
        for camp in ("gauche", "centre", "droite"):
            dc = cm[(cm["identite"] == identity) & (cm["camp"] == camp)]
            for metric in ("pos_decrit", "pos_decrit_oriente", "gs_decrit",
                           "tv_decrit_reel"):
                w = dc.pivot(index="item", columns="cle_modele", values=metric).reindex(columns=ORDER)
                for a, b, label in TRANSITIONS:
                    row = distribution_row(
                        "cellules_appariees", metric, identity, "camp", camp,
                        label, w[b] - w[a])
                    if row:
                        rows.append(row)

    # Rejets sur les 149 items, par checkpoint, camp et identite.
    for (key, identity, camp), d in cm.groupby(["cle_modele", "identite", "camp"]):
        rows.append({
            "analyse": "rejets", "metrique": "rejet", "identite": identity,
            "strate_type": "camp", "strate": camp, "contraste": LABEL[key],
            "n": len(d), "moyenne": d["rejet"].mean(),
        })
    for stype, column in (("famille", "famille"), ("modalites", "k_modalites"),
                          ("polarite", "polarite"), ("consensus_reel", "consensus")):
        for (key, identity, level), d in cm.groupby(
                ["cle_modele", "identite", column], observed=True, dropna=False):
            rows.append({
                "analyse": "rejets", "metrique": "rejet", "identite": identity,
                "strate_type": stype, "strate": level, "contraste": LABEL[key],
                "n": len(d), "moyenne": d["rejet"].mean(),
            })
    return pd.DataFrame(rows)


def format_comparison(item_df, r5, meta):
    r7 = item_df[(item_df["identite"] == "journaliste") & item_df["retenu_strict"]]
    r7 = r7.set_index("item")
    old = r5[(r5["identite"] == "journaliste") &
             r5["cle_modele"].isin(["q4", "q4nogab", "q4gab3"])]
    old = old.merge(meta[["item", "retenu_strict"]], on="item", validate="many_to_one")
    old = old[old["retenu_strict"]].pivot(
        index="item", columns="cle_modele", values="gap_signe_decrit")
    common = sorted(set(r7.index) & set(old.index))
    common = [i for i in common
              if r7.loc[i, [f"gap_{c}" for c in ORDER]].notna().all()
              and old.loc[i, ["q4", "q4nogab", "q4gab3"]].notna().all()]
    r7 = r7.loc[common]
    old = old.loc[common]
    denom = float(r7["gap_signe_reel_w1"].mean())
    series = {
        "SFT - Base": r7["gap_olmo3sft"] - r7["gap_olmo3base"],
        "DPO - SFT": r7["gap_olmo3dpo"] - r7["gap_olmo3sft"],
        "Final - DPO": r7["gap_olmo3rlvr"] - r7["gap_olmo3dpo"],
        "R4 sans gabarit - gabarit": old["q4nogab"] - old["q4"],
        "R5 gabarit + exemples - gabarit": old["q4gab3"] - old["q4"],
    }
    rows = []
    for name, s in series.items():
        x = s.to_numpy(float)
        rows.append({
            "contraste": name, "n_items_communs_stricts": len(x),
            "moyenne_brute": x.mean(), "mediane_brute": np.median(x),
            "q25_brut": np.quantile(x, .25), "q75_brut": np.quantile(x, .75),
            "moyenne_absolue": np.abs(x).mean(),
            "mediane_absolue": np.median(np.abs(x)),
            "q90_absolu": np.quantile(np.abs(x), .90),
            "difference_facteur_denominateur_commun": x.mean() / denom,
            "part_positive": np.mean(x > 1e-12),
            "part_negative": np.mean(x < -1e-12),
            "part_nulle": np.mean(np.abs(x) <= 1e-12),
            "denominateur_humain_commun": denom,
        })
    return pd.DataFrame(rows), series, common


def ranking_stats(item_df):
    rows = []
    for identity, d in item_df[item_df["complet_4_checkpoints"]].groupby("identite"):
        x = d[[f"gap_{c}" for c in ORDER]]
        for i, a in enumerate(ORDER):
            for b in ORDER[i + 1:]:
                rho = spearmanr(x[f"gap_{a}"], x[f"gap_{b}"], nan_policy="omit").statistic
                rows.append({"identite": identity, "mesure": "spearman_items",
                             "a": LABEL[a], "b": LABEL[b], "valeur": rho,
                             "n": len(x)})
        # idxmin/idxmax attribuent silencieusement un ex aequo a la premiere colonne.
        # Les extrema non uniques forment donc une categorie explicite.
        etiquettes = {}
        for role, extremes in (("minimum", x.min(axis=1)), ("maximum", x.max(axis=1))):
            masque = x.eq(extremes, axis="index")
            uniques = masque.sum(axis=1).eq(1)
            valeurs = pd.Series("Ex æquo", index=x.index, dtype=object)
            colonnes = masque.loc[uniques].idxmax(axis=1)
            valeurs.loc[uniques] = colonnes.str.replace(
                "gap_", "", regex=False).map(LABEL)
            etiquettes[role] = valeurs
        for role, values in etiquettes.items():
            counts = values.value_counts()
            for checkpoint, count in counts.items():
                rows.append({"identite": identity, "mesure": role,
                             "a": checkpoint, "b": "", "valeur": count / len(x),
                             "n": int(count)})
        deltas = d[[f"delta_{a}_{b}" for a, b, _ in TRANSITIONS]].to_numpy(float)
        signs = np.sign(deltas)
        reversal = ((signs[:, :-1] * signs[:, 1:]) < 0).any(axis=1)
        rows.append({"identite": identity, "mesure": "inversion_adjacent",
                     "a": "au_moins_une", "b": "", "valeur": reversal.mean(),
                     "n": int(reversal.sum())})
    return pd.DataFrame(rows)


def make_figure(item_df, comparison, series):
    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4.7))
    colors = ["#355C7D", "#6C5B7B", "#C06C84", "#F67280"]

    d = item_df[(item_df["identite"] == "journaliste") &
                item_df["complet_4_checkpoints"]]
    vals = d[[f"gap_{c}" for c in ORDER]].to_numpy(float)
    x = np.arange(4)
    for row in vals:
        axes[0].plot(x, row, color="#9aa0a6", alpha=.18, linewidth=.7)
    axes[0].plot(x, np.mean(vals, axis=0), color="#202124", marker="o", linewidth=2,
                 label="moyenne")
    axes[0].plot(x, np.median(vals, axis=0), color="#D55E00", marker="s", linewidth=2,
                 label="médiane")
    axes[0].set_xticks(x, [LABEL[c] for c in ORDER])
    axes[0].set_ylabel("Écart signé décrit")
    axes[0].set_title(f"Trajectoires par item, journaliste (n={len(d)})")
    axes[0].legend(frameon=False)

    names = list(series)
    data = [np.asarray(series[n], float) for n in names]
    bp = axes[1].boxplot(data, patch_artist=True, showfliers=False, widths=.65)
    for patch, color in zip(bp["boxes"], colors + ["#009E73"]):
        patch.set_facecolor(color); patch.set_alpha(.75)
    axes[1].axhline(0, color="#333", linewidth=.8)
    axes[1].set_xticks(np.arange(1, len(names) + 1),
                       ["SFT-Base", "DPO-SFT", "Final-DPO", "R4 format", "R5 exemples"],
                       rotation=28, ha="right")
    axes[1].set_ylabel("Différence par item")
    axes[1].set_title(f"Périmètre strict commun (n={comparison.iloc[0, 1]})")

    c = pd.read_csv(OUT / "r1-par-cellule-r7.csv")
    rates = c.groupby(["cle_modele", "camp"])["rejet"].mean().unstack().reindex(ORDER)
    xx = np.arange(4); width = .23
    for j, camp in enumerate(["gauche", "centre", "droite"]):
        axes[2].bar(xx + (j - 1) * width, 100 * rates[camp], width, label=camp)
    axes[2].set_xticks(xx, [LABEL[k] for k in ORDER])
    axes[2].set_ylabel("Rejets (%)")
    axes[2].set_title("Rejets sur 298 cellules par camp")
    axes[2].legend(frameon=False, ncol=3, fontsize=8)

    fig.suptitle("R7, analyse descriptive post hoc", fontweight="bold")
    fig.tight_layout()
    fig.savefig(OUT / "r7-analyse-fine.png", dpi=180, bbox_inches="tight")
    fig.savefig(OUT / "r7-analyse-fine.svg", bbox_inches="tight")
    plt.close(fig)


def main():
    cells, items, r5, ori, human = load()
    meta = metadata(ori, human)
    item_df = item_table(items, cells, meta)
    summary = summaries(item_df, cells, meta)
    comparison, series, common = format_comparison(item_df, r5, meta)
    rankings = ranking_stats(item_df)
    item_df.to_csv(OUT / "r7-analyse-fine-items.csv", index=False)
    summary.to_csv(OUT / "r7-analyse-fine-strates.csv", index=False)
    comparison.to_csv(OUT / "r7-analyse-fine-comparaison-format.csv", index=False)
    rankings.to_csv(OUT / "r7-analyse-fine-classements.csv", index=False)
    make_figure(item_df, comparison, series)
    print(f"items={len(item_df)}; strict_common={len(common)}; summaries={len(summary)}")


if __name__ == "__main__":
    main()
