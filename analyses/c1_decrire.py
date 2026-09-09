"""
c1_decrire : question 1 du mois 1 du programme C version menages, et les controles
bloquants C1, C2 et C4 du preenregistrement.

Decrit la structure du panel de la SCE, les variables d'anticipation retenues, les
demographies disponibles, et verifie que la chaine de lecture reproduit les comptes que la
session D1 avait mesures en lisant le XML des feuilles.

Sorties : c1-controles.csv, c1-structure-panel.csv, c1-duree-participation.csv,
c1-variables.csv, c1-demographies.csv, c1-cohortes.csv, c1-couverture-mensuelle.csv.
Aucune microdonnee.
"""

import numpy as np
import pandas as pd

import c1_commun as C1

ATTENDU_D1 = {
    "2020-2024": {"observations": 71976, "userid": 9751},
    "2025": {"observations": 10559, "userid": 2159},
    "2017-2019": {"observations": 47681, "userid": 7379},
}


def controles(df, df17):
    lignes = []
    for cle, att in ATTENDU_D1.items():
        d = df17 if cle == "2017-2019" else df[df["fichier"] == cle]
        n = len(d)
        nu = int(d["userid"].nunique())
        dbl = int(d.duplicated(["date", "userid"]).sum())
        lignes.append({"controle": f"C1 observations {cle}", "attendu": att["observations"],
                       "obtenu": n, "passe": n == att["observations"]})
        lignes.append({"controle": f"C1 userid distincts {cle}", "attendu": att["userid"],
                       "obtenu": nu, "passe": nu == att["userid"]})
        lignes.append({"controle": f"C1 doublons (date, userid) {cle}", "attendu": 0,
                       "obtenu": dbl, "passe": dbl == 0})
    # C5, ajoute apres le preenregistrement : la colonne d'amplitude des variables signees
    # est deja signee dans le fichier public. Le controle verifie que le signe observe est
    # coherent avec la direction declaree, ce qui interdit de la remultiplier par moins un.
    for cle, (c_dir, c_amp, pos, neg) in C1.SIGNEES.items():
        d = pd.to_numeric(df[c_dir], errors="coerce")
        a = pd.to_numeric(df[c_amp], errors="coerce")
        ok = d.notna() & a.notna()
        acc_pos = float((a[ok & (d == pos)] >= 0).mean())
        acc_neg = float((a[ok & (d == neg)] <= 0).mean())
        lignes.append({"controle": f"C5 signe deja porte par {c_amp}",
                       "attendu": "1.0 / 1.0",
                       "obtenu": f"{acc_pos:.4f} / {acc_neg:.4f}",
                       "passe": acc_pos > 0.999 and acc_neg > 0.999})
    # C6, ajoute apres le preenregistrement : l'extraction rapide des groupes de
    # permutation tire exactement la meme permutation que a44_commun.permuter_intra.
    rng = np.random.default_rng(C1.GRAINE)
    for n, g in ((200, 9), (5000, 300), (60000, 3000)):
        codes = rng.integers(0, g, size=n).astype(np.int32)
        ok = C1.controle_permutation(codes)
        lignes.append({"controle": f"C6 permutation identique a a44, n={n}, {g} groupes",
                       "attendu": "identique", "obtenu": "identique" if ok else "differente",
                       "passe": ok})
    return lignes


def recouvrement(df, df17):
    """Controle C2 : les identifiants sont ils stables d'un fichier a l'autre ?

    Descriptif, publie quel que soit le resultat. Deux verifications : le recouvrement des
    ensembles d'identifiants, et, sur les identifiants recoupes, la coherence des
    demographies quasi fixes, categorie d'age et diplome.
    """
    ens = {}
    for cle in ("2017-2019", "2020-2024", "2025"):
        d = df17 if cle == "2017-2019" else df[df["fichier"] == cle]
        ens[cle] = set(d["userid"].astype(np.int64))
    lignes = []
    for a, b in (("2017-2019", "2020-2024"), ("2020-2024", "2025"), ("2017-2019", "2025")):
        inter = ens[a] & ens[b]
        lignes.append({"paire": f"{a} / {b}", "n_a": len(ens[a]), "n_b": len(ens[b]),
                       "communs": len(inter),
                       "part_de_b": len(inter) / max(len(ens[b]), 1)})
    # coherence des demographies sur le raccord 2020-2024 / 2025, le seul qui compte pour
    # le perimetre primaire
    a = df[df["fichier"] == "2020-2024"]
    b = df[df["fichier"] == "2025"]
    da = a.sort_values("t").groupby("userid")[["_AGE_CAT", "_EDU_CAT"]].last()
    db = b.sort_values("t").groupby("userid")[["_AGE_CAT", "_EDU_CAT"]].first()
    j = da.join(db, how="inner", lsuffix="_a", rsuffix="_b")
    coh = {}
    for v in ("_AGE_CAT", "_EDU_CAT"):
        x, y = j[f"{v}_a"], j[f"{v}_b"]
        ok = x.notna() & y.notna()
        coh[v] = float((x[ok] == y[ok]).mean()) if ok.sum() else np.nan
    lignes.append({"paire": "2020-2024 / 2025, coherence des demographies",
                   "n_a": int(len(j)), "n_b": int(len(j)),
                   "communs": int(len(j)),
                   "part_de_b": np.nan,
                   "accord_age_cat": coh["_AGE_CAT"],
                   "accord_edu_cat": coh["_EDU_CAT"]})
    return lignes


def structure(df, df17):
    tout = pd.concat([df, df17], ignore_index=True, sort=False)
    blocs = [(c, tout[tout["fichier"] == c]) for c in ("2017-2019", "2020-2024", "2025")]
    blocs.append(("perimetre primaire 2020-2025", df))
    lignes = []
    for cle, d in blocs:
        ten = pd.to_numeric(d["tenure"], errors="coerce")
        lignes.append({
            "perimetre": cle,
            "observations": len(d),
            "menages": int(d["userid"].nunique()),
            "mois": int(d["t"].nunique()),
            "premier_mois": C1.nom_mois(int(d["t"].min())),
            "dernier_mois": C1.nom_mois(int(d["t"].max())),
            "vagues_par_menage": len(d) / max(d["userid"].nunique(), 1),
            "menages_par_mois": len(d) / max(d["t"].nunique(), 1),
            "tenure_min": float(ten.min()), "tenure_max": float(ten.max()),
            "tenure_mediane": float(ten.median()),
        })
    return lignes


def duree(df):
    """Distribution du nombre de mois de participation, dans le perimetre primaire."""
    n = df.groupby("userid")["t"].nunique()
    tab = n.value_counts().sort_index()
    return [{"mois_de_participation": int(k), "menages": int(v),
             "part": float(v / len(n))} for k, v in tab.items()]


def variables(df):
    bornes = C1.bornes_winsor(df, C1.VAR_PRIMAIRES + C1.VAR_SECONDAIRES)
    lignes = []
    for v in C1.VAR_PRIMAIRES + C1.VAR_SECONDAIRES:
        x = pd.to_numeric(df[v], errors="coerce").to_numpy(dtype=float)
        ok = np.isfinite(x)
        xv = x[ok]
        mois_ok = df.loc[ok].groupby("t")["userid"].nunique()
        lignes.append({
            "variable": v,
            "role": "primaire" if v in C1.VAR_PRIMAIRES else "secondaire",
            "libelle": C1.LIBELLE[v],
            "n_observations": int(ok.sum()),
            "n_menages": int(df.loc[ok, "userid"].nunique()),
            "part_renseignee": float(ok.mean()),
            "min": float(xv.min()) if len(xv) else np.nan,
            "p1": float(np.percentile(xv, 1)) if len(xv) else np.nan,
            "mediane": float(np.median(xv)) if len(xv) else np.nan,
            "moyenne": float(xv.mean()) if len(xv) else np.nan,
            "p99": float(np.percentile(xv, 99)) if len(xv) else np.nan,
            "max": float(xv.max()) if len(xv) else np.nan,
            "borne_winsor_basse": bornes[v][0],
            "borne_winsor_haute": bornes[v][1],
            "mois_couverts": int(len(mois_ok)),
            "mois_sous_100_menages": int((mois_ok < C1.N_MIN_MOIS).sum()),
            "C4_mois": bool((mois_ok >= C1.N_MIN_MOIS).all()) if len(mois_ok) else False,
        })
    return lignes, bornes


def demographies(df):
    lignes = []
    for v in C1.DEMOS + ["Q33", "Q36", "Q47", "_STATE", "tenure", "weight"]:
        if v not in df.columns:
            lignes.append({"variable": v, "present": False})
            continue
        s = df[v] if v in C1.TEXTE else pd.to_numeric(df[v], errors="coerce")
        vc = s.value_counts(dropna=True).sort_index()
        lignes.append({
            "variable": v, "present": True,
            "type": "texte" if v in C1.TEXTE else "nombre",
            "n_renseigne": int(s.notna().sum()),
            "part_renseignee": float(s.notna().mean()),
            "n_niveaux": int(s.nunique()),
            "niveaux": ";".join(f"{k}={int(n)}" for k, n in vc.items())
            if 0 < s.nunique() <= 60 else
            (f"{s.min()} a {s.max()}" if s.notna().any() else ""),
        })
    lignes.append({"variable": "parti ou ideologie", "present": False,
                   "n_renseigne": 0, "part_renseignee": 0.0, "n_niveaux": 0,
                   "niveaux": "absent du module central, questionnaire lu en entier"})
    return lignes


def cohortes(df):
    tab = df.groupby("cohorte").agg(observations=("userid", "size"),
                                    menages=("userid", "nunique")).reset_index()
    tab = tab.sort_values("observations", ascending=False)
    tab["part_observations"] = tab["observations"] / len(df)
    return tab


def couverture(df):
    lignes = []
    for t, d in df.groupby("t"):
        ligne = {"t": int(t), "mois": C1.nom_mois(int(t)),
                 "menages": int(d["userid"].nunique()),
                 "cohortes_observees": int(d["cohorte"].nunique())}
        for v in C1.VAR_PRIMAIRES:
            ligne[f"n_{v}"] = int(pd.to_numeric(d[v], errors="coerce").notna().sum())
        lignes.append(ligne)
    return lignes


def main():
    df = C1.charger(C1.PRIMAIRE)
    df17 = C1.charger(["2017-2019"])

    ctrl = controles(df, df17)
    C1.ecrire(ctrl, "c1-controles.csv")
    for c in ctrl:
        etat = "OK" if c["passe"] else "ECHEC"
        print(f"  [{etat}] {c['controle']}: attendu {c['attendu']}, obtenu {c['obtenu']}")
    if not all(c["passe"] for c in ctrl):
        raise SystemExit("controle bloquant C1 en echec, rien n'est publie")

    C1.ecrire(recouvrement(df, df17), "c1-recouvrement-identifiants.csv")
    C1.ecrire(structure(df, df17), "c1-structure-panel.csv")
    C1.ecrire(duree(df), "c1-duree-participation.csv")
    lignes_var, _ = variables(df)
    C1.ecrire(lignes_var, "c1-variables.csv")
    C1.ecrire(demographies(df), "c1-demographies.csv")
    C1.ecrire(cohortes(df), "c1-cohortes.csv")
    C1.ecrire(couverture(df), "c1-couverture-mensuelle.csv")
    print("c1_decrire termine")


if __name__ == "__main__":
    main()
