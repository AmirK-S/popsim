"""
memoire_long_analyse : note la trace de analyses/memoire_long_gss.py contre le protocole
de resultats/memoire-long-preenregistrement.md.

Statut : script d'analyse, pas du code de production.

Ce qu'il fait. Pour chaque horizon (+2 ans, +4 ans), compare quatre predicteurs sur les
memes cellules (personne, item) : persistance (reponse de la vague 1), mode du segment
(modalite la plus frequente a la vague 1 dans l'echantillon), le jumeau IA (trace du
modele), et la regle combinee fixee d'avance (IA seulement si elle diverge de la
persistance ET s'accorde avec le mode du segment). Rapporte l'exactitude globale, sur les
seules cellules ou la personne a change d'avis, et l'AUC du desaccord IA/passe pour
predire ce changement. IC a 95 % par bootstrap sur les PERSONNES (l'unite qui n'est pas
independante d'un item a l'autre), pas sur les cellules.

La verite (reponses de vague 1, 2 et 3) n'est PAS stockee dans la trace de collecte : ce
script la relit dans le panel, comme le fait deja analyses/a5_agents_locaux_gss.py pour
Twin-2K-500.

Entree  : data/traces/memoire-long/ml-<modele>.jsonl, ml-echantillon.csv, ml-items.csv,
          ecrits par memoire_long_gss.py. data/gss-panel/*.dta pour la verite.
Sortie  : resultats/memoire-long-<modele>.csv (table principale) et un rapport imprime.

Usage :
  .venv/bin/python analyses/memoire_long_analyse.py --modele oss20
  .venv/bin/python analyses/memoire_long_analyse.py --test      # donnees factices, aucun
                                                                 # fichier reel necessaire
"""

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memoire_long_gss import PANELS, TRACES, charger_panel_libelle  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
N_BOOTSTRAP = 1000
GRAINE_BOOTSTRAP = 20260911
HORIZONS = (2, 4)


# ---------------------------------------------------------------------------
# 1. Chargement : trace du modele + verite relue dans le panel
# ---------------------------------------------------------------------------

def charger_trace(chemin):
    """Une ligne par (panel, personne, item, horizon) : la reponse du modele, ou None
    si l'appel a ete rejete au parse."""
    lignes = []
    with open(chemin, encoding="utf-8") as fh:
        for l in fh:
            l = l.strip()
            if not l:
                continue
            d = json.loads(l)
            lignes.append({
                "panel": d["panel"], "ligne": d["ligne"], "item": d["item"],
                "horizon": d["horizon_ans"], "ia": None if d["rejet"] else d["reponse_modele"],
            })
    return pd.DataFrame(lignes)


def charger_verite(echantillon, items_cibles):
    """Recharge, panel par panel, les reponses des personnes de l'echantillon aux items
    cibles, aux trois vagues. N'a besoin d'AUCUN item de contexte : plus rapide que la
    collecte, qui doit construire le profil complet."""
    morceaux = []
    for nom_panel, sous in echantillon.groupby("panel"):
        table_p, _, _, _ = charger_panel_libelle(nom_panel, [], items_cibles)
        annees = sorted(PANELS[nom_panel]["vagues"])
        annee1 = annees[0]
        table_p = table_p[table_p["ligne"].isin(set(sous["ligne"]))]
        for it in items_cibles:
            base = table_p[["ligne", f"cible::{it}@{annee1}"]].rename(
                columns={f"cible::{it}@{annee1}": "persistance"})
            base["panel"] = nom_panel
            base["item"] = it
            for h in HORIZONS:
                col = f"cible::{it}@{annee1 + h}"
                base[f"verite_{h}"] = table_p[col].values if col in table_p.columns \
                    else None
            morceaux.append(base)
    return pd.concat(morceaux, ignore_index=True)


# ---------------------------------------------------------------------------
# 2. Le coeur du calcul : predicteurs et notation, sur un DataFrame long
#    colonnes attendues : panel, ligne, item, horizon, persistance, verite, ia
# ---------------------------------------------------------------------------

def mode_du_segment(long_df):
    """Modalite de vague 1 la plus frequente par item, sur l'echantillon entier."""
    uniques = long_df.drop_duplicates(["panel", "ligne", "item"])
    return (uniques.dropna(subset=["persistance"])
            .groupby("item")["persistance"]
            .agg(lambda s: s.value_counts().idxmax())
            .to_dict())


def ajouter_predicteurs(long_df):
    """Ajoute les colonnes b0_mode et combinee a un DataFrame deja restreint a un
    horizon. Regle combinee fixee d'avance (preenregistrement) : IA si elle diverge de
    la persistance ET s'accorde avec le mode du segment, sinon persistance."""
    modes = mode_du_segment(long_df)
    long_df = long_df.copy()
    long_df["b0_mode"] = long_df["item"].map(modes)
    diverge = long_df["ia"] != long_df["persistance"]
    accord_mode = long_df["ia"] == long_df["b0_mode"]
    long_df["combinee"] = np.where(diverge & accord_mode, long_df["ia"],
                                   long_df["persistance"])
    return long_df


def bootstrap_personnes_df(long_df, statistique, n_tirages=N_BOOTSTRAP,
                           graine=GRAINE_BOOTSTRAP):
    """IC a 95 % par bootstrap sur les personnes : on tire des personnes AVEC remise,
    pas des lignes. `statistique(df)` rend un scalaire ; None si non calculable."""
    cles = long_df[["panel", "ligne"]].drop_duplicates().values
    rng = np.random.default_rng(graine)
    point = statistique(long_df)
    if point is None or (isinstance(point, float) and np.isnan(point)):
        return float("nan"), float("nan"), float("nan")
    tirages = []
    idx_par_personne = long_df.groupby(["panel", "ligne"]).indices
    for _ in range(n_tirages):
        choix = cles[rng.integers(0, len(cles), size=len(cles))]
        lignes = np.concatenate([idx_par_personne[tuple(c)] for c in choix])
        v = statistique(long_df.iloc[lignes])
        if v is not None and not (isinstance(v, float) and np.isnan(v)):
            tirages.append(v)
    if not tirages:
        return point, float("nan"), float("nan")
    return point, float(np.percentile(tirages, 2.5)), float(np.percentile(tirages, 97.5))


def exactitude_moyenne(df, colonne, restreindre_ia=True):
    """Exactitude moyenne PAR PERSONNE (moyenne des items, puis moyenne des personnes),
    sur les cellules ou la verite et l'IA sont disponibles (cellules comparables entre
    les quatre predicteurs)."""
    d = df.dropna(subset=["verite", colonne])
    if restreindre_ia:
        d = d.dropna(subset=["ia"])
    if d.empty:
        return None
    juste = (d[colonne] == d["verite"]).astype(float)
    par_personne = juste.groupby([d["panel"], d["ligne"]]).mean()
    return float(par_personne.mean())


def auc_desaccord(df):
    """AUC du desaccord IA/persistance pour predire un vrai changement d'avis."""
    d = df.dropna(subset=["verite", "persistance", "ia"])
    if d.empty:
        return None
    change = (d["verite"] != d["persistance"]).astype(int)
    desaccord = (d["ia"] != d["persistance"]).astype(int)
    if change.nunique() < 2 or desaccord.nunique() < 2:
        return None
    return float(roc_auc_score(change, desaccord))


# ---------------------------------------------------------------------------
# 3. Rapport par horizon
# ---------------------------------------------------------------------------

def rapport_horizon(long_df, horizon):
    d = ajouter_predicteurs(long_df[long_df["horizon"] == horizon])
    changees = d[d["verite"] != d["persistance"]]

    lignes = []
    for nom, col in (("persistance", "persistance"), ("jumeau IA", "ia"),
                     ("mode du segment", "b0_mode"), ("regle combinee", "combinee")):
        m, b, h = bootstrap_personnes_df(d, lambda x, c=col: exactitude_moyenne(x, c))
        ligne = {"horizon_ans": horizon, "predicteur": nom, "mesure": "exactitude globale",
                "valeur": m, "ic_bas": b, "ic_haut": h}
        lignes.append(ligne)
        if col in ("ia", "b0_mode"):
            m2, b2, h2 = bootstrap_personnes_df(
                changees, lambda x, c=col: exactitude_moyenne(x, c))
            lignes.append({"horizon_ans": horizon, "predicteur": nom,
                           "mesure": "exactitude sur cellules changees",
                           "valeur": m2, "ic_bas": b2, "ic_haut": h2})
    m, b, h = bootstrap_personnes_df(d, auc_desaccord)
    lignes.append({"horizon_ans": horizon, "predicteur": "jumeau IA",
                   "mesure": "AUC desaccord -> changement", "valeur": m,
                   "ic_bas": b, "ic_haut": h})
    n_personnes = d[["panel", "ligne"]].drop_duplicates().shape[0]
    n_changees = changees.dropna(subset=["ia"]).shape[0]
    n_total = d.dropna(subset=["ia"]).shape[0]
    print(f"\n--- horizon +{horizon} ans : {n_personnes} personnes, {n_total} cellules "
          f"notees, {n_changees} changees ({n_changees / max(n_total, 1):.1%}) ---")
    for l in lignes:
        if l["valeur"] is None or (isinstance(l["valeur"], float) and np.isnan(l["valeur"])):
            print(f"  {l['predicteur']:<18} {l['mesure']:<32} : n/a")
        else:
            print(f"  {l['predicteur']:<18} {l['mesure']:<32} : {l['valeur']:.4f} "
                  f"[{l['ic_bas']:.4f}-{l['ic_haut']:.4f}]")
    return lignes


def verdicts(table):
    """Confronte les trois predictions chiffrees du preenregistrement aux resultats."""
    def val(h, pred, mesure):
        r = table[(table.horizon_ans == h) & (table.predicteur == pred)
                  & (table.mesure == mesure)]
        return float(r["valeur"].iloc[0]) if len(r) and pd.notna(r["valeur"].iloc[0]) \
            else float("nan")

    print("\n=== confrontation aux predictions chiffrees ===")
    ecart2 = val(2, "persistance", "exactitude globale") - val(2, "jumeau IA", "exactitude globale")
    ecart4 = val(4, "persistance", "exactitude globale") - val(4, "jumeau IA", "exactitude globale")
    print(f"P1. persistance - IA : +2 ans {ecart2:+.4f}, +4 ans {ecart4:+.4f} "
          f"(prediction : positif aux deux, ecart plus petit a +4 qu'a +2) "
          f"-> {'a verifier au vu des IC' if ecart2 > 0 and ecart4 > 0 else 'NON CONFIRME'}")
    for h in HORIZONS:
        ia_c = val(h, "jumeau IA", "exactitude sur cellules changees")
        mode_c = val(h, "mode du segment", "exactitude sur cellules changees")
        print(f"P2 (+{h} ans). IA sur changees {ia_c:.4f} vs mode du segment {mode_c:.4f} "
              f"-> {'IA ne bat pas le mode' if ia_c <= mode_c else 'IA bat le mode : NON CONFIRME'}")
    for h in HORIZONS:
        auc = val(h, "jumeau IA", "AUC desaccord -> changement")
        print(f"P3 (+{h} ans). AUC = {auc:.4f} "
              f"-> {'sous 0.62' if auc < 0.62 else 'AU DESSUS DE 0.62 : NON CONFIRME'}")


# ---------------------------------------------------------------------------
# 4. Donnees factices, pour tester ce script SANS trace reelle ni panel
# ---------------------------------------------------------------------------

def fabriquer_donnees_factices(n_personnes=60, n_items=8, graine=0):
    """Simule un monde ou la persistance est correcte 70 % du temps, l'IA 55 %, et une
    petite fraction des changements est detectable par le desaccord IA/passe. Sert
    uniquement a verifier que les fonctions ci-dessus tournent sans erreur et rendent des
    nombres plausibles ; ce ne sont pas des donnees d'enquete.
    """
    rng = np.random.default_rng(graine)
    modalites = ["A", "B", "C"]
    items = [f"item{i}" for i in range(n_items)]
    lignes = []
    for p in range(n_personnes):
        panel = "2006-2010" if p % 2 == 0 else "2008-2012"
        for it in items:
            persistance = rng.choice(modalites)
            for h in HORIZONS:
                # la verite reste egale a la persistance avec une proba qui baisse un
                # peu avec l'horizon (les gens changent plus a 4 ans qu'a 2 ans).
                p_stable = 0.72 if h == 2 else 0.62
                verite = persistance if rng.random() < p_stable else rng.choice(modalites)
                a_change = verite != persistance
                # l'IA recopie souvent la persistance, se trompe parfois, et devine un
                # peu mieux que le hasard quand ca a change (signal faible et voulu).
                if rng.random() < 0.60:
                    ia = persistance
                elif a_change and rng.random() < 0.35:
                    ia = verite
                else:
                    ia = rng.choice(modalites)
                rejet = rng.random() < 0.05
                lignes.append({
                    "panel": panel, "ligne": p, "item": it, "horizon": h,
                    "persistance": persistance, "verite": verite,
                    "ia": None if rejet else ia,
                })
    return pd.DataFrame(lignes)


def executer_test():
    print("=== test sur donnees factices (aucun fichier reel lu) ===")
    long_df = fabriquer_donnees_factices()
    table = pd.DataFrame(
        [l for h in HORIZONS for l in rapport_horizon(long_df, h)])
    verdicts(table)
    assert not table.empty, "le tableau de resultats est vide"
    assert table["valeur"].notna().any(), "aucune valeur calculee"
    print("\nOK : le pipeline d'analyse tourne sans erreur sur des donnees factices.")
    return table


# ---------------------------------------------------------------------------
# 5. Programme
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="oss20", help="cle du registre MODELES (r1)")
    ap.add_argument("--suffixe", default="", help="suffixe de la trace, pour un smoke test")
    ap.add_argument("--test", action="store_true",
                    help="ignore --modele : verifie le pipeline sur des donnees factices")
    args = ap.parse_args()

    if args.test:
        executer_test()
        return

    nom = f"ml-{args.modele}" + (("-" + args.suffixe) if args.suffixe else "")
    chemin_trace = os.path.join(TRACES, nom + ".jsonl")
    chemin_ech = os.path.join(TRACES, "ml-echantillon.csv")
    chemin_items = os.path.join(TRACES, "ml-items.csv")
    for c in (chemin_trace, chemin_ech, chemin_items):
        if not os.path.exists(c):
            sys.exit(f"fichier introuvable : {c} (lancer memoire_long_gss.py d'abord)")

    echantillon = pd.read_csv(chemin_ech)
    items_cibles = pd.read_csv(chemin_items)["item"].tolist()
    print(f"{len(echantillon)} personnes, {len(items_cibles)} items cibles, "
          f"trace {chemin_trace}")

    trace = charger_trace(chemin_trace)
    verite = charger_verite(echantillon, items_cibles)

    morceaux = []
    for h in HORIZONS:
        v = verite[["panel", "ligne", "item", "persistance", f"verite_{h}"]].rename(
            columns={f"verite_{h}": "verite"})
        v["horizon"] = h
        morceaux.append(v)
    verite_longue = pd.concat(morceaux, ignore_index=True)

    long_df = verite_longue.merge(trace, on=["panel", "ligne", "item", "horizon"],
                                  how="left")
    print(f"{len(long_df)} cellules attendues, {long_df['ia'].notna().sum()} avec une "
          f"reponse IA exploitable ({long_df['ia'].notna().mean():.1%})")

    table = pd.DataFrame([l for h in HORIZONS for l in rapport_horizon(long_df, h)])
    os.makedirs(SORTIE, exist_ok=True)
    chemin_sortie = os.path.join(SORTIE, f"memoire-long-{args.modele}.csv")
    table.to_csv(chemin_sortie, index=False)
    print(f"\ntable ecrite : {chemin_sortie}")
    verdicts(table)


if __name__ == "__main__":
    main()
