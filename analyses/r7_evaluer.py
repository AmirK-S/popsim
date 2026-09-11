"""R7 : contrastes descriptifs entre quatre checkpoints publies d'Olmo 3.

Ce script ne lance aucun modele. Il prolonge les estimations ecrites par
``r1_evaluer.py --suffixe r7 --sans-figure`` et ne recopie ni ses mesures ni ses tests
contre le referent humain. Les contrastes F1--F5 suivent le plan R7 et son addendum du
10 septembre 2026. Leur portee est exclusivement descriptive : le lineage direct des
quatre checkpoints n'est pas etabli et aucune difference n'est attribuee causalement a
une etape d'entrainement.

Entrees principales :
  resultats/r1-par-cellule-r7.csv
  resultats/r1-par-item-ecarts-r7.csv
  data/traces/r1-<condition>-r7.jsonl (controles et completude)

Sorties : resultats/r7-contrastes.csv, r7-hypotheses.csv, r7-controles.csv,
          r7-evaluation.md

Le script accepte une collecte interrompue seulement si son fichier est un prefixe
valide du plan. Toute corruption, repetition, permutation ou configuration incompatible
est refusee. Un contraste avec moins de trois items valides communs est refuse ; le
statut PARTIEL depend de la completude de la collecte (894 tentatives), pas du nombre
d'items restant apres les rejets. Pour ne pas rendre Holm plus favorable quand un test
manque, les tests refuses occupent leur place avec p=1 dans leur famille figee.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r1_evaluer as R1  # noqa: E402


RACINE = Path(__file__).resolve().parent.parent
RESULTATS = RACINE / "resultats"
TRACES = RACINE / "data/traces"
GRAINE = 20260910
N_BOOT = 2000
N_PERM = 20000
PORTEE = "DESCRIPTIVE checkpoints publies; aucune causalite d'etape"
REFERENT_SHA256 = "ea7cd93e8eb3b34d279171ac9a202a0451554afc3d34c7a142dfce761391c811"

ORDRE = ("olmo3base", "olmo3sft", "olmo3dpo", "olmo3rlvr")
N_ORIENTES = 79
VERSION_PROMPT = "r7-c3"
GABARIT = "completion-3ex"
NOMS_MODELES = {
    "olmo3base": "Olmo-3-1025-7B",
    "olmo3sft": "Olmo-3-7B-Instruct-SFT",
    "olmo3dpo": "Olmo-3-7B-Instruct-DPO",
    "olmo3rlvr": "Olmo-3-7B-Instruct",
}
PAIRES = {
    # Orientation litterale du plan compact corrige. H4 lit deux de ces lignes < 0.
    "F1": (("olmo3base", "olmo3sft"), ("olmo3sft", "olmo3dpo"),
           ("olmo3dpo", "olmo3rlvr")),
    "F2": (("olmo3base", "olmo3rlvr"), ("olmo3base", "olmo3dpo"),
           ("olmo3sft", "olmo3rlvr")),
    "F4": (("olmo3base", "olmo3sft"), ("olmo3sft", "olmo3dpo"),
           ("olmo3dpo", "olmo3rlvr")),
}
TAILLES_FAMILLES = {"F1": 3, "F2": 3, "F3": 4, "F4": 3, "F5": 12}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for bloc in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def lire_csv(path: Path, colonnes: set[str]) -> tuple[pd.DataFrame, str | None]:
    if not path.is_file():
        return pd.DataFrame(), f"entree absente: {path.name}"
    try:
        table = pd.read_csv(path)
    except Exception as exc:
        return pd.DataFrame(), f"entree illisible: {path.name}: {type(exc).__name__}"
    manque = sorted(colonnes - set(table.columns))
    if manque:
        return pd.DataFrame(), f"colonnes absentes dans {path.name}: {', '.join(manque)}"
    return table, None


def lire_entrees(resultats: Path) -> tuple[dict[str, pd.DataFrame], list[str]]:
    specs = {
        "cellules": ("r1-par-cellule-r7.csv", {"cle_modele", "camp", "identite", "item",
                                                   "rejet", "gs_decrit", "gs_reel_w1"}),
        "ecarts": ("r1-par-item-ecarts-r7.csv", {"cle_modele", "identite", "item",
                                                      "gap_signe_decrit", "gap_signe_reel_w1"}),
    }
    tables, erreurs = {}, []
    for cle, (nom, colonnes) in specs.items():
        tables[cle], erreur = lire_csv(resultats / nom, colonnes)
        if erreur:
            erreurs.append(erreur)
    return tables, erreurs


def lire_perimetres(resultats: Path) -> tuple[set[str], set[str]]:
    orientation, erreur_o = lire_csv(resultats / "a37-orientation-items.csv", {"item", "oriente"})
    strict, erreur_s = lire_csv(resultats / "a37-gss-par-item.csv", {"item", "retenu_strict"})
    if erreur_o or erreur_s:
        return set(), set()
    return (set(orientation.loc[orientation["oriente"].astype(bool), "item"]),
            set(strict.loc[strict["retenu_strict"].astype(bool), "item"]))


def lire_items_plan(resultats: Path) -> list[str]:
    """Ordre des 149 items utilisé par le pilote, conservé par la table a37."""
    table, erreur = lire_csv(resultats / "a37-orientation-items.csv", {"item"})
    if erreur:
        return []
    items = table["item"].astype(str).tolist()
    return items if len(items) == 149 and len(set(items)) == 149 else []


def _nombre(x) -> float:
    try:
        v = float(x)
        return v if math.isfinite(v) else float("nan")
    except (TypeError, ValueError):
        return float("nan")


def ic_difference_facteurs(a, b, ref, rng, n=N_BOOT):
    """Difference de deux rapports de moyennes, sur les memes items et le meme referent."""
    a, b, ref = (np.asarray(x, dtype=float) for x in (a, b, ref))
    ok = np.isfinite(a) & np.isfinite(b) & np.isfinite(ref)
    a, b, ref = a[ok], b[ok], ref[ok]
    if len(a) < 3 or not np.isfinite(ref.mean()) or ref.mean() == 0:
        return (float("nan"),) * 5 + (int(len(a)),)
    fa, fb = float(a.mean() / ref.mean()), float(b.mean() / ref.mean())
    difference = fa - fb
    idx = rng.integers(0, len(a), size=(n, len(a)))
    den = ref[idx].mean(axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        tirages = (a[idx].mean(axis=1) - b[idx].mean(axis=1)) / den
    tirages = tirages[np.isfinite(tirages)]
    if len(tirages) < 10:
        return fa, fb, difference, float("nan"), float("nan"), int(len(a))
    return (fa, fb, difference, float(np.percentile(tirages, 2.5)),
            float(np.percentile(tirages, 97.5)), int(len(a)))


def ligne_refusee(famille, test, identite="journaliste", camp="", raison="entree absente"):
    return {
        "famille": famille, "test": test, "identite": identite, "camp": camp,
        "condition_a": "", "condition_b": "", "n_items": 0, "n_items_attendus": 0,
        "statut": "REFUSE", "raison_statut": raison, "estimateur_a": np.nan,
        "estimateur_b": np.nan, "difference": np.nan, "ic_bas": np.nan,
        "ic_haut": np.nan, "p": np.nan, "p_holm": np.nan, "significatif": False,
        "portee": PORTEE,
    }


def contrastes_paires(ecarts, orientes, famille, identite, rng, n_boot, n_perm):
    lignes = []
    g = ecarts[(ecarts["identite"] == identite) & ecarts["item"].isin(orientes)]
    attendu = N_ORIENTES
    for a, b in PAIRES[famille]:
        test = f"{a} - {b}"
        ga = g[g["cle_modele"] == a].drop_duplicates("item").set_index("item")
        gb = g[g["cle_modele"] == b].drop_duplicates("item").set_index("item")
        communs = sorted(set(ga.index) & set(gb.index))
        if len(communs) < 3:
            ligne = ligne_refusee(famille, test, identite, raison="moins de 3 items apparies")
            ligne.update({"condition_a": a, "condition_b": b, "n_items": len(communs),
                          "n_items_attendus": attendu})
            lignes.append(ligne)
            continue
        va = ga.loc[communs, "gap_signe_decrit"].to_numpy(float)
        vb = gb.loc[communs, "gap_signe_decrit"].to_numpy(float)
        refa = ga.loc[communs, "gap_signe_reel_w1"].to_numpy(float)
        refb = gb.loc[communs, "gap_signe_reel_w1"].to_numpy(float)
        finis = np.isfinite(va) & np.isfinite(vb) & np.isfinite(refa) & np.isfinite(refb)
        va, vb, refa, refb = va[finis], vb[finis], refa[finis], refb[finis]
        if len(va) < 3:
            ligne = ligne_refusee(
                famille, test, identite, raison="moins de 3 triplets apparies finis")
            ligne.update({"condition_a": a, "condition_b": b, "n_items": len(va),
                          "n_items_attendus": attendu})
            lignes.append(ligne)
            continue
        # Le referent doit etre identique des deux cotes sur le perimetre apparie.
        if not np.allclose(refa, refb, atol=1e-12):
            ligne = ligne_refusee(famille, test, identite, raison="referent non identique entre conditions")
            ligne.update({"condition_a": a, "condition_b": b, "n_items": len(va),
                          "n_items_attendus": attendu})
            lignes.append(ligne)
            continue
        fa, fb, dif, bas, haut, n = ic_difference_facteurs(va, vb, refa, rng, n_boot)
        p = R1.p_permutation_signe(va - vb, rng, n_perm)
        lignes.append({
            "famille": famille, "test": test, "identite": identite, "camp": "",
            "condition_a": a, "condition_b": b, "n_items": n,
            "n_items_attendus": attendu, "statut": "EXECUTE",
            "raison_statut": "items valides dans les deux conditions",
            "estimateur_a": fa, "estimateur_b": fb, "difference": dif,
            "ic_bas": bas, "ic_haut": haut, "p": p, "p_holm": np.nan,
            "significatif": False, "portee": PORTEE,
        })
    return lignes


def tests_contre_un(cellules, ecarts, orientes, rng, n_boot, n_perm):
    """F3/F5 par les mesures elementaires R1, avec exactement ses estimateurs."""
    lignes = []
    attendu_f3 = N_ORIENTES
    h2p = (ecarts[(ecarts["identite"] == "journaliste") & ecarts["item"].isin(orientes)]
           if len(ecarts) else pd.DataFrame())
    for cle in ORDRE:
        g = (h2p[h2p["cle_modele"] == cle] if len(h2p) else pd.DataFrame())
        g = g.drop_duplicates("item")
        if len(g) < 3:
            ligne = ligne_refusee("F3", f"{cle} contre 1", raison="moins de 3 estimations R1 par item")
            ligne.update({"condition_a": cle, "n_items_attendus": attendu_f3})
            lignes.append(ligne)
            continue
        a = g["gap_signe_decrit"].to_numpy(float)
        b = g["gap_signe_reel_w1"].to_numpy(float)
        finis = np.isfinite(a) & np.isfinite(b)
        a, b = a[finis], b[finis]
        if len(a) < 3:
            ligne = ligne_refusee("F3", f"{cle} contre 1",
                                  raison="moins de 3 paires finies")
            ligne.update({"condition_a": cle, "condition_b": "1",
                          "n_items": len(a), "n_items_attendus": attendu_f3})
            lignes.append(ligne)
            continue
        facteur, bas, haut, n = R1.ic_ratio_des_moyennes(a, b, rng, n_boot)
        p = R1.p_permutation_signe(a - b, rng, n_perm)
        statut = "EXECUTE"
        lignes.append({
            "famille": "F3", "test": f"{cle} contre 1", "identite": "journaliste",
            "camp": "", "condition_a": cle, "condition_b": "1", "n_items": n,
            "n_items_attendus": attendu_f3, "statut": statut,
            "raison_statut": "estimation R1 reutilisee" if statut != "REFUSE" else "moins de 3 items",
            "estimateur_a": facteur, "estimateur_b": 1.0,
            "difference": facteur - 1.0, "ic_bas": bas,
            "ic_haut": haut, "p": p,
            "p_holm": np.nan, "significatif": False, "portee": PORTEE,
        })

    h1p = (cellules[(~cellules["rejet"].astype(bool)) &
                    (cellules["identite"] == "journaliste")]
           if len(cellules) else pd.DataFrame())
    for cle in ORDRE:
        for camp in R1.CAMPS:
            g = (h1p[(h1p["cle_modele"] == cle) & (h1p["camp"] == camp)]
                 if len(h1p) else pd.DataFrame())
            g = g.drop_duplicates("item")
            if len(g) < 3:
                ligne = ligne_refusee("F5", f"{cle}/{camp} contre 1", camp=camp,
                                      raison="moins de 3 estimations R1 par item")
                ligne.update({"condition_a": cle, "n_items_attendus": 149})
                lignes.append(ligne)
                continue
            a = g["gs_decrit"].to_numpy(float)
            b = g["gs_reel_w1"].to_numpy(float)
            finis = np.isfinite(a) & np.isfinite(b)
            a, b = a[finis], b[finis]
            positifs = (a > 0) & (b > 0)
            if len(a) < 3 or int(positifs.sum()) < 3:
                ligne = ligne_refusee(
                    "F5", f"{cle}/{camp} contre 1", camp=camp,
                    raison="moins de 3 paires finies et strictement positives")
                ligne.update({"condition_a": cle, "condition_b": "1",
                              "n_items": int(positifs.sum()), "n_items_attendus": 149})
                lignes.append(ligne)
                continue
            ratio, bas, haut, n = R1.ic_ratio_des_moyennes(a, b, rng, n_boot)
            with np.errstate(divide="ignore", invalid="ignore"):
                dlog = np.log(np.where(a > 0, a, np.nan)) - np.log(np.where(b > 0, b, np.nan))
            p = R1.p_permutation_signe(dlog, rng, n_perm)
            statut = "EXECUTE"
            lignes.append({
                "famille": "F5", "test": f"{cle}/{camp} contre 1", "identite": "journaliste",
                "camp": camp, "condition_a": cle, "condition_b": "1", "n_items": n,
                "n_items_attendus": 149, "statut": statut,
                "raison_statut": "estimation R1 reutilisee" if statut != "REFUSE" else "moins de 3 items",
                "estimateur_a": ratio, "estimateur_b": 1.0,
                "difference": ratio - 1.0, "ic_bas": bas,
                "ic_haut": haut, "p": p,
                "p_holm": np.nan, "significatif": False, "portee": PORTEE,
            })
    return lignes


def appliquer_holm_fixe(lignes):
    """Holm par famille figee ; un test non executable conserve sa place avec p=1."""
    for famille, taille in TAILLES_FAMILLES.items():
        idx = [i for i, ligne in enumerate(lignes) if ligne["famille"] == famille]
        if len(idx) != taille:
            raise RuntimeError(f"{famille}: {taille} tests prescrits, {len(idx)} construits")
        ps = [lignes[i]["p"] if np.isfinite(lignes[i]["p"]) and
              lignes[i]["statut"] != "REFUSE" else 1.0 for i in idx]
        corriges = R1.holm(np.asarray(ps, dtype=float))
        for i, p_holm in zip(idx, corriges):
            if lignes[i]["statut"] != "REFUSE":
                lignes[i]["p_holm"] = float(p_holm)
                lignes[i]["significatif"] = bool(p_holm < 0.05)
                if p_holm >= 0.05:
                    lignes[i]["verdict"] = "non significatif"
                elif famille in ("F3", "F5") and 0.95 <= lignes[i]["estimateur_a"] <= 1.05:
                    lignes[i]["verdict"] = "significatif mais nul en pratique"
                elif famille in ("F3", "F5"):
                    lignes[i]["verdict"] = "au-dessus de 1" if lignes[i]["estimateur_a"] > 1 else "sous 1"
                else:
                    lignes[i]["verdict"] = "difference positive" if lignes[i]["difference"] > 0 else "difference negative"
            else:
                lignes[i]["verdict"] = "indecidable"
    return lignes


def lire_traces(traces_dir: Path, items: list[str]):
    """Lit uniquement un préfixe strict du plan R7; toute corruption refuse la trace."""
    par_condition = {}
    for cle in ORDRE:
        path = traces_dir / f"r1-{cle}-r7.jsonl"
        lignes = []
        if path.is_file():
            if not items:
                raise RuntimeError(f"{path.name}: ordre des 149 items indisponible")
            attendues = [(camp, identite, item) for camp in R1.CAMPS
                         for identite in R1.IDENTITES for item in items]
            cles_vues = set()
            for numero, brut in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if not brut.strip():
                    raise RuntimeError(f"{path.name}:{numero}: ligne vide; trace refusee")
                try:
                    ligne = json.loads(brut)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        f"{path.name}:{numero}: JSON invalide; trace refusee") from exc
                if not isinstance(ligne, dict):
                    raise RuntimeError(f"{path.name}:{numero}: objet JSON attendu; trace refusee")
                cle_cellule = (ligne.get("camp"), ligne.get("identite"), ligne.get("item"))
                if cle_cellule in cles_vues:
                    raise RuntimeError(f"{path.name}:{numero}: cellule en doublon; trace refusee")
                if len(lignes) >= len(attendues):
                    raise RuntimeError(f"{path.name}:{numero}: cellule en trop; trace refusee")
                camp, identite, item = attendues[len(lignes)]
                exige = {
                    "version_prompt": VERSION_PROMPT,
                    "cle_modele": cle,
                    "modele": NOMS_MODELES[cle],
                    "quantification": "Q8_0",
                    "gabarit": GABARIT,
                    "item": item,
                    "camp": camp,
                    "identite": identite,
                    "sans_relance": True,
                    "n_tentatives": 1,
                }
                mauvais = {k: (ligne.get(k), valeur) for k, valeur in exige.items()
                            if ligne.get(k) != valeur}
                if mauvais:
                    raise RuntimeError(
                        f"{path.name}:{numero}: ordre/configuration incompatible {mauvais}")
                cles_vues.add(cle_cellule)
                lignes.append(ligne)
        par_condition[cle] = lignes
    return par_condition


def exclure_recopies_r7(tables, traces):
    """Retire des estimations R1 les recopies K>=3, y compris sans relance.

    R1 ne retire une recopie que lorsqu'elle suit une relance. R7 n'a aucune relance et
    sa regle 2 bis retire toute recopie de l'exemple pour K>=3. Les mesures elementaires
    restent celles de R1 ; ce filtre ne change que leur perimetre.
    """
    copies = set()
    for cle, lignes in traces.items():
        for t in lignes:
            distribution = t.get("distribution")
            k = int(t.get("n_modalites", len(distribution or {})))
            if (not t.get("rejet") and distribution and k >= 3 and
                    R1.recopie_exemple(distribution)):
                copies.add((cle, t.get("camp"), t.get("identite"), t.get("item")))
    sortie = {cle: table.copy() for cle, table in tables.items()}
    cel = sortie["cellules"]
    if len(cel) and copies:
        masque = [
            (r.cle_modele, r.camp, r.identite, r.item) not in copies
            for r in cel.itertuples(index=False)
        ]
        sortie["cellules"] = cel[np.asarray(masque, dtype=bool)].copy()
    eca = sortie["ecarts"]
    if len(eca) and copies:
        # H2b n'emploie que gauche et droite : une copie d'un cote retire l'item des deux.
        interdits = {(cle, identite, item) for cle, camp, identite, item in copies
                     if camp in ("gauche", "droite")}
        masque = [(r.cle_modele, r.identite, r.item) not in interdits
                  for r in eca.itertuples(index=False)]
        sortie["ecarts"] = eca[np.asarray(masque, dtype=bool)].copy()
    return sortie, copies


def controles_traces(traces, cellules, referent: Path):
    lignes = []
    for cle in ORDRE:
        ts = traces.get(cle, [])
        n, rejets = len(ts), sum(bool(t.get("rejet")) for t in ts)
        copies3 = copies2 = 0
        for t in ts:
            if t.get("rejet") or not t.get("distribution"):
                continue
            k = int(t.get("n_modalites", len(t["distribution"])))
            copie = R1.recopie_exemple(t["distribution"])
            copies3 += int(copie and k >= 3)
            copies2 += int(copie and k == 2)
        taux = rejets / n if n else np.nan
        g = cellules[(cellules.get("cle_modele", pd.Series(dtype=str)) == cle)] if len(cellules) else pd.DataFrame()
        identiques = total = 0
        if len(g) and "p_decrit" in g.columns:
            ok = g[~g["rejet"].astype(bool)]
            for (_, _), gg in ok.groupby(["identite", "item"], sort=False):
                pres = dict(zip(gg["camp"], gg["p_decrit"].astype(str)))
                if "gauche" in pres and "droite" in pres:
                    total += 1
                    identiques += int(pres["gauche"] == pres["droite"])
        # r1-par-cellule supprime p_decrit : reconstitution minimale depuis les traces.
        if not total:
            groupes = {}
            for t in ts:
                if not t.get("rejet") and t.get("distribution"):
                    groupes.setdefault((t.get("identite"), t.get("item")), {})[t.get("camp")] = t["distribution"]
            for pres in groupes.values():
                if "gauche" in pres and "droite" in pres:
                    total += 1
                    identiques += int(pres["gauche"] == pres["droite"])
        part_constante = identiques / total if total else np.nan
        motif = []
        if n < 894:
            motif.append("trace incomplete")
        if np.isfinite(taux) and taux > 0.25:
            motif.append("rejets > 25 %")
        if n >= 60 and sum(bool(t.get("rejet")) for t in ts[:60]) / 60 > 0.50:
            motif.append("sonde > 50 %")
        if n and copies3 / n > 0.05:
            motif.append("recopie K>=3 > 5 %")
        if np.isfinite(part_constante) and part_constante > 0.90:
            motif.append("camp ignore > 90 %")
        lignes.append({
            "condition": cle, "cellules": n, "cellules_attendues": 894,
            "rejets": rejets, "taux_rejet": taux, "recopies_k_ge_3": copies3,
            "taux_recopie_k_ge_3": copies3 / n if n else np.nan,
            "recopies_k_2_informatif": copies2, "items_comparables_camps": total,
            "part_constante_camps": part_constante,
            "statut": "A_LIRE" if motif else "PASSE",
            "detail": "; ".join(motif) if motif else "controles disponibles passes",
            "portee": PORTEE,
        })
    ref_ok = referent.is_file() and sha256(referent) == REFERENT_SHA256
    lignes.append({
        "condition": "referent humain", "cellules": np.nan, "cellules_attendues": np.nan,
        "rejets": np.nan, "taux_rejet": np.nan, "recopies_k_ge_3": np.nan,
        "taux_recopie_k_ge_3": np.nan, "recopies_k_2_informatif": np.nan,
        "items_comparables_camps": np.nan, "part_constante_camps": np.nan,
        "statut": "PASSE" if ref_ok else "REFUS_GLOBAL",
        "detail": "SHA-256 R1 conforme" if ref_ok else "referent absent ou modifie",
        "portee": PORTEE,
    })
    return pd.DataFrame(lignes)


def ajouter_controles_analyse(controles, contrastes, ecarts):
    """Ajoute le plancher humain et le diagnostic F/taux de rejet du plan R7."""
    lignes = []
    if len(ecarts) and {"gap_signe_reel_w1", "gap_signe_reel_w2"} <= set(ecarts.columns):
        e = ecarts.drop_duplicates("item")
        den = e["gap_signe_reel_w1"].mean()
        facteur = e["gap_signe_reel_w2"].mean() / den if den else np.nan
    else:
        facteur = np.nan
    lignes.append({
        "condition": "plancher humain", "cellules": np.nan, "cellules_attendues": np.nan,
        "rejets": np.nan, "taux_rejet": np.nan, "recopies_k_ge_3": np.nan,
        "taux_recopie_k_ge_3": np.nan, "recopies_k_2_informatif": np.nan,
        "items_comparables_camps": np.nan, "part_constante_camps": np.nan,
        "statut": ("PASSE" if np.isfinite(facteur) and 0.85 <= facteur <= 1.15 else
                   "REFUS_GLOBAL"),
        "detail": (f"facteur w2/w1={facteur:.6f}" if np.isfinite(facteur) else
                   "facteur w2/w1 indisponible"), "portee": PORTEE,
    })

    f3 = contrastes[contrastes["famille"] == "F3"].set_index("condition_a")
    rej = controles[controles["condition"].isin(ORDRE)].set_index("condition")
    rho = np.nan
    if set(ORDRE) <= set(f3.index) and set(ORDRE) <= set(rej.index):
        fv = np.array([f3.at[c, "estimateur_a"] for c in ORDRE], float)
        rv = np.array([rej.at[c, "taux_rejet"] for c in ORDRE], float)
        if np.isfinite(fv).all() and np.isfinite(rv).all():
            rho = float(pd.Series(fv).rank().corr(pd.Series(rv).rank()))
    lignes.append({
        "condition": "F contre taux de rejet", "cellules": np.nan,
        "cellules_attendues": np.nan, "rejets": np.nan, "taux_rejet": np.nan,
        "recopies_k_ge_3": np.nan, "taux_recopie_k_ge_3": np.nan,
        "recopies_k_2_informatif": np.nan, "items_comparables_camps": np.nan,
        "part_constante_camps": rho,
        "statut": "A_LIRE" if np.isfinite(rho) and abs(rho) > 0.8 else
                  ("PASSE" if np.isfinite(rho) else "INDECIDABLE"),
        "detail": (f"rho={rho:.6f}; artefact possible de conformite" if
                   np.isfinite(rho) and abs(rho) > 0.8 else
                   (f"rho={rho:.6f}" if np.isfinite(rho) else "rho indisponible")),
        "portee": PORTEE,
    })
    return pd.concat([controles, pd.DataFrame(lignes)], ignore_index=True)


def appliquer_refus_controles(lignes, controles):
    mauvais = set(controles.loc[
        controles["condition"].isin(ORDRE) & controles["detail"].str.contains(
            "rejets >|sonde >|recopie K>=3", regex=True, na=False), "condition"])
    camps_ignores = set(controles.loc[
        controles["condition"].isin(ORDRE) &
        controles["detail"].str.contains("camp ignore", regex=False, na=False), "condition"])
    incompletes = set(controles.loc[
        controles["condition"].isin(ORDRE) &
        controles["detail"].str.contains("trace incomplete", regex=False, na=False), "condition"])
    raisons_globales = controles.loc[controles["statut"] == "REFUS_GLOBAL", "detail"].tolist()
    for ligne in lignes:
        impliques = {ligne.get("condition_a"), ligne.get("condition_b")} & set(ORDRE)
        causes = sorted(impliques & mauvais)
        causes_camp = sorted(impliques & camps_ignores) if ligne["famille"] != "F5" else []
        if raisons_globales or causes or causes_camp:
            ligne["statut"] = "REFUSE"
            if raisons_globales:
                ligne["raison_statut"] = "refus global: " + "; ".join(raisons_globales)
            else:
                ligne["raison_statut"] = "critere de chute: " + ", ".join(causes + causes_camp)
            ligne["p_holm"] = np.nan
            ligne["significatif"] = False
        elif ligne["statut"] == "EXECUTE" and impliques & incompletes:
            ligne["statut"] = "PARTIEL"
            ligne["raison_statut"] = "trace incomplete: estimation descriptive seulement"
    return lignes


def evaluer_hypotheses(contrastes):
    """Lecture mecanique H1--H4 ; aucun vocabulaire causal."""
    def prendre(famille, test):
        g = contrastes[(contrastes["famille"] == famille) & (contrastes["test"] == test)]
        return None if len(g) != 1 else g.iloc[0]

    f1 = contrastes[contrastes["famille"] == "F1"]
    decidable_f1 = len(f1) == 3 and f1["statut"].eq("EXECUTE").all()
    h1 = bool(decidable_f1 and f1["significatif"].any())

    h2r = prendre("F2", "olmo3base - olmo3rlvr")
    h2_dec = h2r is not None and h2r["statut"] == "EXECUTE" and np.isfinite(h2r["difference"])
    h2 = bool(h2_dec and h2r["significatif"] and h2r["difference"] > 0)

    marche = prendre("F1", "olmo3base - olmo3sft")
    h3_dec = decidable_f1 and np.isfinite(f1["difference"]).all()
    h3 = bool(h3_dec and marche is not None and marche["difference"] > 0 and
              abs(marche["difference"]) == f1["difference"].abs().max())

    h4a = prendre("F1", "olmo3sft - olmo3dpo")
    h4b = prendre("F2", "olmo3sft - olmo3rlvr")
    h4_dec = all(r is not None and r["statut"] == "EXECUTE" and
                 np.isfinite(r["difference"]) for r in (h4a, h4b))
    h4 = bool(h4_dec and h4a["significatif"] and h4b["significatif"] and
              h4a["difference"] < 0 and h4b["difference"] < 0)

    return pd.DataFrame([
        {"hypothese": "H1", "critere": "au moins un contraste F1 significatif",
         "statut": "EVALUE" if decidable_f1 else "INDECIDABLE", "satisfaite": h1,
         "portee": PORTEE},
        {"hypothese": "H2", "critere": "Base-Final > 0 et significatif dans F2",
         "statut": "EVALUE" if h2_dec else "INDECIDABLE", "satisfaite": h2,
         "portee": PORTEE},
        {"hypothese": "H3", "critere": "Base-SFT > 0 et plus grand contraste F1 en valeur absolue",
         "statut": "EVALUE" if h3_dec else "INDECIDABLE", "satisfaite": h3,
         "portee": PORTEE},
        {"hypothese": "H4", "critere": "SFT-DPO < 0 (F1) et SFT-Final < 0 (F2), deux p Holm < 0,05",
         "statut": "EVALUE" if h4_dec else "INDECIDABLE", "satisfaite": h4,
         "portee": PORTEE},
    ])


def construire(tables, orientes, rng, n_boot=N_BOOT, n_perm=N_PERM):
    if not len(tables["ecarts"]):
        lignes = []
        for famille in ("F1", "F2", "F4"):
            identite = "adversaire" if famille == "F4" else "journaliste"
            for a, b in PAIRES[famille]:
                ligne = ligne_refusee(famille, f"{a} - {b}", identite,
                                      raison="r1-par-item-ecarts-r7.csv indisponible")
                ligne.update({"condition_a": a, "condition_b": b,
                              "n_items_attendus": N_ORIENTES})
                lignes.append(ligne)
    else:
        lignes = contrastes_paires(tables["ecarts"], orientes, "F1", "journaliste",
                                    rng, n_boot, n_perm)
        lignes += contrastes_paires(tables["ecarts"], orientes, "F2", "journaliste",
                                     rng, n_boot, n_perm)
        lignes += contrastes_paires(tables["ecarts"], orientes, "F4", "adversaire",
                                     rng, n_boot, n_perm)
    lignes += tests_contre_un(tables["cellules"], tables["ecarts"], orientes,
                              rng, n_boot, n_perm)
    return lignes


def fmt(v, n=3):
    return "n.d." if not np.isfinite(_nombre(v)) else f"{float(v):.{n}f}".replace(".", ",")


def ecrire_rapport(path, contrastes, hypotheses, controles, erreurs):
    n_exec = int(contrastes["statut"].eq("EXECUTE").sum())
    n_part = int(contrastes["statut"].eq("PARTIEL").sum())
    n_refus = int(contrastes["statut"].eq("REFUSE").sum())
    lignes = [
        "# R7 — evaluation descriptive des checkpoints", "",
        "**Portee : DESCRIPTIVE checkpoints publies.** Le lineage direct n'est pas etabli ; "
        "aucun contraste n'autorise une attribution causale a SFT, DPO ou a l'etape finale.", "",
        f"Tests prescrits : **25**. Executes complets : **{n_exec}** ; partiels : "
        f"**{n_part}** ; refuses : **{n_refus}**. Holm est applique separement dans F1--F5 "
        "en conservant la taille preenregistree de chaque famille.", "",
        "H4 est code dans l'orientation des familles : `SFT-DPO < 0` dans F1 et "
        "`SFT-Final < 0` dans F2, les deux survivant a Holm.", "",
    ]
    if erreurs:
        lignes += ["Entrees ou traces a revoir : " + " ; ".join(erreurs) + ".", ""]
    lignes += ["| famille | contraste | n | statut | difference | p Holm |",
               "|---|---|---:|---|---:|---:|"]
    for _, r in contrastes.iterrows():
        lignes.append(f"| {r['famille']} | {r['test']} | {int(r['n_items'])} | "
                      f"{r['statut']} | {fmt(r['difference'])} | {fmt(r['p_holm'], 4)} |")
    lignes += ["", "## Hypotheses", "", "| hypothese | statut | satisfaite |",
               "|---|---|---|"]
    for _, r in hypotheses.iterrows():
        valeur = "oui" if r["satisfaite"] else "non"
        lignes.append(f"| {r['hypothese']} | {r['statut']} | {valeur} |")
    lignes += ["", "## Controles", "",
               "| condition | cellules | rejets | copies K>=3 | camp constant | statut |",
               "|---|---:|---:|---:|---:|---|"]
    for _, r in controles.iterrows():
        cellules = "n.d." if pd.isna(r["cellules"]) else str(int(r["cellules"]))
        rejets = "n.d." if pd.isna(r["rejets"]) else str(int(r["rejets"]))
        copies = "n.d." if pd.isna(r["recopies_k_ge_3"]) else str(int(r["recopies_k_ge_3"]))
        lignes.append(f"| {r['condition']} | {cellules} | {rejets} | {copies} | "
                      f"{fmt(r['part_constante_camps'])} | {r['statut']} |")
    lignes += ["", "Aucune interpretation de nouvelle donnee n'est produite par ce script.", ""]
    path.write_text("\n".join(lignes), encoding="utf-8")


def evaluer(resultats=RESULTATS, traces_dir=TRACES, n_boot=N_BOOT, n_perm=N_PERM):
    tables, erreurs = lire_entrees(resultats)
    orientes, _ = lire_perimetres(resultats)
    if len(orientes) != N_ORIENTES:
        erreurs.append(f"perimetre oriente: {len(orientes)} items, {N_ORIENTES} attendus")
    items = lire_items_plan(resultats)
    traces = lire_traces(traces_dir, items)
    controles = controles_traces(traces, tables["cellules"], traces_dir / "r1-distributions-reelles.csv")
    tables, _ = exclure_recopies_r7(tables, traces)
    rng = np.random.default_rng(GRAINE)
    lignes = construire(tables, orientes, rng, n_boot, n_perm)
    controles = ajouter_controles_analyse(controles, pd.DataFrame(lignes), tables["ecarts"])
    lignes = appliquer_refus_controles(lignes, controles)
    lignes = appliquer_holm_fixe(lignes)
    contrastes = pd.DataFrame(lignes)
    hypotheses = evaluer_hypotheses(contrastes)
    return contrastes, hypotheses, controles, erreurs


def parser_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--resultats", type=Path, default=RESULTATS)
    ap.add_argument("--traces", type=Path, default=TRACES)
    ap.add_argument("--tirages-bootstrap", type=int, default=N_BOOT)
    ap.add_argument("--permutations", type=int, default=N_PERM)
    return ap.parse_args(argv)


def main(argv=None):
    args = parser_args(argv)
    args.resultats.mkdir(parents=True, exist_ok=True)
    contrastes, hypotheses, controles, erreurs = evaluer(
        args.resultats, args.traces, args.tirages_bootstrap, args.permutations)
    contrastes.to_csv(args.resultats / "r7-contrastes.csv", index=False)
    hypotheses.to_csv(args.resultats / "r7-hypotheses.csv", index=False)
    controles.to_csv(args.resultats / "r7-controles.csv", index=False)
    ecrire_rapport(args.resultats / "r7-evaluation.md", contrastes, hypotheses,
                   controles, erreurs)
    print(json.dumps({"tests": len(contrastes),
                      "executes": int(contrastes["statut"].eq("EXECUTE").sum()),
                      "partiels": int(contrastes["statut"].eq("PARTIEL").sum()),
                      "refuses": int(contrastes["statut"].eq("REFUSE").sum()),
                      "portee": PORTEE, "erreurs": erreurs}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
