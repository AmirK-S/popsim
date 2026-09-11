"""caricature_profil : la caricature ideologique gonfle-t-elle moins quand le profil donne
a l'IA est plus riche, sur Twin-2K-500 ?

PREENREGISTREMENT : resultats/caricature-profil-preenregistrement.md, ecrit AVANT ce fichier
et avant tout calcul. Aucun appel de modele : les 13 configurations d'agents Twin-2K-500 sont
deja calculees par une autre equipe ; seules les 8 configurations admissibles de
`resultats/twin-ab-audit-provenance-2026-09-11.md` sont utilisees ici. Lecture seule sur
data/. Camp = `i3b_twin.charger_twin_commun`["blocs"] (gauche/droite, derive de l'ideologie
QID22 par `a6_double_distorsion_hors_gss.bloc_ideologie_twin`), seule variable partisane
locale disponible ; personnes "centre" exclues.

Mesure primaire (facteur d'exageration) et secondaire (compression) : voir le
preenregistrement pour la definition exacte. Bootstrap : nested person-within-unit puis
unit-resampling, tous deux avec remise, graine fixe -- l'implementation resample les
personnes de chaque item DANS leur propre camp (B tirages independants par item), colonne
par colonne du tableau (n_unites x B) obtenu, puis tire des unites (item, config) avec
remise pour chaque replicat ; c'est la lecture retenue de "personnes ET items
reechantillonnes avec remise conjointement" du preenregistrement.
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "4"

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i3b_twin as T3  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")

GRAINE = 20260911
B = 2000
SEUIL_ECART_HUM = 0.02
PLANCHER_TVD = 1e-3
MIN_GROUPE = 10

# Les 8 configurations admissibles (audit de provenance), par niveau de richesse.
NIVEAUX = {
    "Demographics Only": ["Demographics Only - GPT4.1-mini"],
    "JSON Persona": ["JSON Persona - GPT4.1", "JSON Persona - GPT4.1-mini"],
    "Text Persona": ["Text Persona (Default Temperature) - GPT4.1-mini",
                      "Text Persona (Reasoning) - GPT4.1-mini",
                      "Text Persona (Repeating Questions) - GPT4.1-mini",
                      "Text Persona - GPT4.1-mini",
                      "Text Persona - Gemini-Flash2.5"],
}


def tvd(p, q):
    return 0.5 * float(np.sum(np.abs(p - q)))


def gini_simpson(p):
    return 1.0 - float(np.sum(p * p))


def dist(codes_col, idx, k):
    c = codes_col[idx]
    c = c[c >= 0]
    if len(c) == 0:
        return None
    return np.bincount(c, minlength=k).astype(float) / len(c)


def compter_2d(cat_mat, k):
    """cat_mat : (B, n) valeurs 0..k-1 -> (B, k) proportions."""
    b_, n_ = cat_mat.shape
    out = np.zeros((b_, k))
    rows = np.repeat(np.arange(b_), n_)
    np.add.at(out, (rows, cat_mat.ravel()), 1)
    return out / n_


def main():
    print("chargement Twin-2K-500 ...", flush=True)
    paq = T3.charger_twin_commun(RACINE_TWIN)
    codes, blocs, modalites = paq["codes"], paq["blocs"], paq["modalites"]
    codes_h = codes[T3.CONTROLE]
    n_items = codes_h.shape[1]

    idx_g_all = np.where(blocs == "gauche")[0]
    idx_d_all = np.where(blocs == "droite")[0]
    print(f"camp gauche {len(idx_g_all)}, camp droite {len(idx_d_all)}", flush=True)

    unites, lignes_config = [], []
    for niveau, membres in NIVEAUX.items():
        for c in membres:
            codes_c = codes[c]
            facteurs, compressions = [], []
            for j in range(n_items):
                k = len(modalites[j])
                if k < 2:
                    continue
                vg = idx_g_all[(codes_h[idx_g_all, j] >= 0) & (codes_c[idx_g_all, j] >= 0)]
                vd = idx_d_all[(codes_h[idx_d_all, j] >= 0) & (codes_c[idx_d_all, j] >= 0)]
                if len(vg) < MIN_GROUPE or len(vd) < MIN_GROUPE:
                    continue
                dh_g, dh_d = dist(codes_h[:, j], vg, k), dist(codes_h[:, j], vd, k)
                di_g, di_d = dist(codes_c[:, j], vg, k), dist(codes_c[:, j], vd, k)
                tvd_h, tvd_i = tvd(dh_g, dh_d), tvd(di_g, di_d)
                if tvd_h < SEUIL_ECART_HUM:
                    continue
                facteur = tvd_i / tvd_h
                cv = []
                for dh, di in ((dh_g, di_g), (dh_d, di_d)):
                    disp_h = gini_simpson(dh)
                    if disp_h > 0:
                        cv.append(gini_simpson(di) / disp_h)
                compression = float(np.mean(cv)) if cv else np.nan
                facteurs.append(facteur)
                if not np.isnan(compression):
                    compressions.append(compression)
                unites.append({"niveau": niveau, "config": c, "item": j,
                               "vg": vg, "vd": vd, "k": k, "facteur": facteur,
                               "compression": compression})
            lignes_config.append({
                "niveau": niveau, "config": c, "n_items_retenus": len(facteurs),
                "facteur_mediane": float(np.median(facteurs)) if facteurs else np.nan,
                "compression_mediane": float(np.median(compressions)) if compressions else np.nan,
            })
            print(f"  {c} : {len(facteurs)} items retenus, "
                  f"facteur median {lignes_config[-1]['facteur_mediane']:.2f}", flush=True)

    df_config = pd.DataFrame(lignes_config)
    df_config.to_csv(os.path.join(SORTIE, "caricature-profil-configs.csv"), index=False)

    # ---- bootstrap : un vecteur de B facteurs par unite (item, config) --------------
    print(f"bootstrap, {len(unites)} unites x {B} replicats ...", flush=True)
    rng = np.random.default_rng(GRAINE)
    for u in unites:
        vg, vd, j, k, c = u["vg"], u["vd"], u["item"], u["k"], u["config"]
        col_h, col_i = codes_h[:, j], codes[c][:, j]
        ng, nd = len(vg), len(vd)
        rg = rng.integers(0, ng, size=(B, ng))
        rd = rng.integers(0, nd, size=(B, nd))
        dh_g = compter_2d(col_h[vg][rg], k)
        dh_d = compter_2d(col_h[vd][rd], k)
        di_g = compter_2d(col_i[vg][rg], k)
        di_d = compter_2d(col_i[vd][rd], k)
        tvd_h_b = np.maximum(0.5 * np.abs(dh_g - dh_d).sum(axis=1), PLANCHER_TVD)
        tvd_i_b = 0.5 * np.abs(di_g - di_d).sum(axis=1)
        u["facteur_boot"] = tvd_i_b / tvd_h_b

    def bootstrap_niveau(noms_niveaux, rng_local):
        us = [u for u in unites if u["niveau"] in noms_niveaux]
        mat = np.stack([u["facteur_boot"] for u in us])  # (n_unites, B)
        n_u = mat.shape[0]
        tirage = rng_local.integers(0, n_u, size=(B, n_u))
        vals = mat[tirage, np.arange(B)[:, None]]  # (B, n_u)
        return np.median(vals, axis=1), n_u

    boot_demo, n_demo = bootstrap_niveau(["Demographics Only"], rng)
    boot_json, n_json = bootstrap_niveau(["JSON Persona"], rng)
    boot_text, n_text = bootstrap_niveau(["Text Persona"], rng)
    boot_complets, n_complets = bootstrap_niveau(["JSON Persona", "Text Persona"], rng)
    ratio_boot = boot_demo / boot_complets

    def resume(nom, obs_med, boot, n_u):
        return {"niveau": nom, "n_unites": n_u,
                "facteur_mediane": obs_med,
                "ic95_bas": float(np.percentile(boot, 2.5)),
                "ic95_haut": float(np.percentile(boot, 97.5))}

    obs = {niveau: np.median([u["facteur"] for u in unites if u["niveau"] == niveau])
           for niveau in NIVEAUX}
    obs_complets = np.median([u["facteur"] for u in unites
                              if u["niveau"] in ("JSON Persona", "Text Persona")])

    lignes_niveau = [
        resume("Demographics Only", obs["Demographics Only"], boot_demo, n_demo),
        resume("JSON Persona", obs["JSON Persona"], boot_json, n_json),
        resume("Text Persona", obs["Text Persona"], boot_text, n_text),
        resume("Profils complets (JSON+Text)", obs_complets, boot_complets, n_complets),
    ]
    df_niveau = pd.DataFrame(lignes_niveau)
    df_niveau.to_csv(os.path.join(SORTIE, "caricature-profil-niveaux.csv"), index=False)

    ratio_obs = obs["Demographics Only"] / obs_complets
    verdict = pd.DataFrame([{
        "ratio_demo_sur_complets": ratio_obs,
        "ratio_ic95_bas": float(np.percentile(ratio_boot, 2.5)),
        "ratio_ic95_haut": float(np.percentile(ratio_boot, 97.5)),
        "prediction_ratio_1_5": bool(ratio_obs >= 1.5),
        "facteur_complets": obs_complets,
        "complets_ic95_bas": float(np.percentile(boot_complets, 2.5)),
        "prediction_complets_sup_1": bool(obs_complets > 1.0),
    }])
    verdict.to_csv(os.path.join(SORTIE, "caricature-profil-verdict.csv"), index=False)

    print(df_niveau.to_string(index=False), flush=True)
    print(verdict.to_string(index=False), flush=True)
    print("termine", flush=True)


if __name__ == "__main__":
    main()
