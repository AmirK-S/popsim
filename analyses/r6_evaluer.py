"""Evaluation confirmatoire R6, hors reseau et sans appel de modele.

Le script lit seulement les traces explicitement nommees dans un manifeste d'analyse.
Il reutilise les mesures et routines statistiques de ``r1_evaluer``. H1 est la regle
decisionnelle sans p du plan OSF; F2 contient H2; F3 contient H3a et H3b. Selon l'addendum
prospectif OSF kmqnw, H4 est exclusivement exploratoire : T et IC bootstrap, sans p,
Holm, significativite ni verdict confirmatoire.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

for _nom in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_nom] = "2"

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r1_evaluer as R1  # noqa: E402
import r4b_contrastes as R4  # noqa: E402
import r6_oracle_distant as CLIENT  # noqa: E402


RACINE = Path(__file__).resolve().parent.parent
RESULTATS = RACINE / "resultats"
GRAINE = 20260910
N_BOOT = 2000
N_PERM = 20000
PLANCHER_A2 = 1.009
FERMES = (
    "openai/gpt-5.6-luna",
    "google/gemini-3.8-flash",
    "anthropic/claude-haiku-4.5",
    "x-ai/grok-4.3",
    "openai/gpt-5.4",
)
SONNET = "anthropic/claude-sonnet-5"
PAIRES_H4 = (
    ("openai/gpt-5.4", "openai/gpt-5.6-luna"),
    (SONNET, "anthropic/claude-haiku-4.5"),
)
PORTEE = "DESCRIPTIF; modele, fournisseur, invite et date nommes; aucune causalite"
REFERENT_SHA256 = CLIENT.REFERENT_SHA
REFERENCE_ADDENDUM = "https://osf.io/kmqnw/overview"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for bloc in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def _cellules_plan(items, format_):
    plan = CLIENT.PLANS["f1" if format_ == "q4" else "f2"]
    choisis = items if plan["items"] == "tous" else [i for i, o in items if o]
    if plan["items"] == "tous":
        choisis = [i[0] if isinstance(i, tuple) else i for i in choisis]
    return [(camp, identite, item) for camp in plan["camps"]
            for identite in plan["identites"] for item in choisis]


def lire_manifeste(path: Path) -> list[dict]:
    try:
        m = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("manifeste d'analyse absent ou JSON invalide") from exc
    if m.get("version") != "R6-evaluation-1" or not isinstance(m.get("traces"), list):
        raise RuntimeError("manifeste d'analyse incompatible")
    return m["traces"]


def charger_traces(manifeste: Path, items_ordonnes: list[tuple[str, bool]]):
    """Charge les traces du client actuel; aucune decouverte implicite de fichier."""
    groupes = {}
    specs_vues = set()
    base = manifeste.resolve().parent
    for spec in lire_manifeste(manifeste):
        try:
            modele, format_, passe = spec["modele"], spec["format"], spec["passe"]
            suffixe, declare = spec.get("suffixe", ""), Path(spec["chemin"])
        except (KeyError, TypeError) as exc:
            raise RuntimeError("specification de trace incomplete") from exc
        if format_ not in CLIENT.FORMATS or passe not in CLIENT.PASSES_LANCEMENT:
            raise RuntimeError("format ou passe hors protocole")
        configuration_attendue = spec.get("configuration")
        if not isinstance(configuration_attendue, dict):
            raise RuntimeError("configuration attendue absente du manifeste")
        cle = CLIENT.cle_run(modele, format_, suffixe)
        path = declare if declare.is_absolute() else (base / declare)
        if path.name != f"r6-{cle}.jsonl":
            raise RuntimeError(f"nom de trace incompatible: {path.name}")
        ident_spec = (modele, format_, passe)
        if ident_spec in specs_vues:
            raise RuntimeError(f"passe dupliquee: {ident_spec}")
        specs_vues.add(ident_spec)
        attendues = (_cellules_plan(items_ordonnes, format_) if passe == "campagne" else
                     [tuple(c) for c in spec.get("cellules", [])])
        if passe != "campagne" and not attendues:
            raise RuntimeError(f"liste de cellules obligatoire pour la passe {passe}")
        rang = {cellule: i for i, cellule in enumerate(attendues)}
        vues, precedent, lignes, configuration = set(), -1, [], None
        try:
            brutes = path.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise RuntimeError(f"trace absente: {path.name}") from exc
        for numero, brut in enumerate(brutes, 1):
            if not brut.strip():
                raise RuntimeError(f"{path.name}:{numero}: ligne vide")
            try:
                d = json.loads(brut)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"{path.name}:{numero}: JSON invalide") from exc
            cellule = (d.get("camp"), d.get("identite"), d.get("item"))
            if cellule in vues:
                raise RuntimeError(f"{path.name}:{numero}: cellule dupliquee")
            # Ordre de plan strict, sauf ligne rejouee apres 429 prouve non facture
            # (amendement 429) : plus tard, jamais avant une cellule qui la precede au plan.
            rapprochement = d.get("rapprochement_429")
            rejouee = isinstance(rapprochement, dict) and rapprochement.get("statut") == "non_facture"
            if cellule not in rang or (rang[cellule] <= precedent and not rejouee):
                raise RuntimeError(f"{path.name}:{numero}: cellule hors plan ou ordre incompatible")
            exige = {
                "version_prompt": CLIENT.FORMATS[format_], "format": format_,
                "modele": modele, "cle_modele": cle, "gabarit": CLIENT.GABARIT,
                "n_tentatives": 1, "sans_relance": True, "erreur": None,
            }
            mauvais = [k for k, v in exige.items() if d.get(k) != v]
            if mauvais:
                raise RuntimeError(f"{path.name}:{numero}: configuration incompatible: {mauvais}")
            if d.get("configuration") != configuration_attendue:
                raise RuntimeError(f"{path.name}:{numero}: configuration incompatible au manifeste")
            if not d.get("fournisseur") or d.get("quantification") != d.get("fournisseur"):
                raise RuntimeError(f"{path.name}:{numero}: fournisseur absent ou incoherent")
            if configuration is None:
                configuration = d["configuration"]
            elif d["configuration"] != configuration:
                raise RuntimeError(f"{path.name}:{numero}: configuration change en cours de passe")
            vues.add(cellule)
            precedent = max(precedent, rang[cellule])
            d = dict(d)
            d["passe_r6"] = passe
            lignes.append(d)
        groupes[ident_spec] = lignes
    return groupes


def construire_tables(traces, ref, options, effectifs, sens):
    cel = R1.par_cellule(traces, ref, options, sens, effectifs)
    if not len(cel):
        return cel, pd.DataFrame(), pd.DataFrame()
    return cel, R1.par_item_ecarts(cel, ref, sens), R1.par_item_identite(cel, ref)


def _apparier(g, colonnes):
    g = g.drop_duplicates("item").set_index("item")
    return g[list(colonnes)]


def _ligne(famille, hypothese, modele, statut="REFUSE", raison="donnees absentes", **kw):
    d = {"famille": famille, "hypothese": hypothese, "modele": modele,
         "camp": "", "n_items": 0, "statut": statut, "raison_statut": raison,
         "estimateur": np.nan, "ic_bas": np.nan, "ic_haut": np.nan,
         "p": np.nan, "p_holm": np.nan, "retenu": False, "portee": PORTEE}
    d.update(kw)
    return d


def calculer_a2(ecarts, orientes, rng, n_boot):
    lignes = []
    for modele in FERMES:
        g = ecarts[(ecarts.get("modele", pd.Series(dtype=str)) == modele) &
                   (ecarts.get("identite", pd.Series(dtype=str)) == "journaliste") &
                   ecarts.get("item", pd.Series(dtype=str)).isin(orientes)] if len(ecarts) else pd.DataFrame()
        if len(g) < 3:
            lignes.append(_ligne("F1", "H1", modele))
            continue
        facteur, bas, haut, n = R1.ic_ratio_des_moyennes(
            g["gap_signe_decrit"], g["gap_signe_reel_w1"], rng, n_boot)
        lignes.append(_ligne("F1", "H1", modele, "EXECUTE", "A2 R1",
                             n_items=n, estimateur=facteur, ic_bas=bas, ic_haut=haut))
    return pd.DataFrame(lignes)


def evaluer_h1(a2):
    ok = a2[a2["statut"] == "EXECUTE"]
    if len(ok) != len(FERMES) or not np.isfinite(ok[["estimateur", "ic_bas", "ic_haut"]]).all().all():
        return {"hypothese": "H1", "famille": "F1", "statut": "INDECIDABLE",
                "satisfaite": False, "p": np.nan, "raison": "cinq fermes requis", "portee": PORTEE}
    mini, maxi = ok.loc[ok["estimateur"].idxmin()], ok.loc[ok["estimateur"].idxmax()]
    ratio = maxi["estimateur"] / mini["estimateur"] if mini["estimateur"] != 0 else np.inf
    disjoints = maxi["ic_bas"] > mini["ic_haut"] or mini["ic_bas"] > maxi["ic_haut"]
    traverse = bool((ok["ic_haut"] < PLANCHER_A2).any() and
                    (ok["ic_bas"] > PLANCHER_A2).any())
    satisfaite = bool((ratio >= 2 and disjoints) or traverse)
    return {"hypothese": "H1", "famille": "F1", "statut": "EVALUE",
            "satisfaite": satisfaite, "p": np.nan,
            "raison": f"max/min={ratio:.6f}; IC extremes disjoints={disjoints}; deux cotes={traverse}",
            "portee": PORTEE}


def planchers_machine(groupes):
    """TV moyenne campagne/plancher sur les memes cellules; absence = indefini."""
    sortie = {}
    for modele in FERMES:
        campagne = groupes.get((modele, "q4", "campagne"), [])
        plancher = groupes.get((modele, "q4", "plancher"), [])
        a = {(d["camp"], d["identite"], d["item"]): d for d in campagne
             if not d.get("rejet") and d.get("distribution")}
        distances = []
        for d in plancher:
            cle = (d["camp"], d["identite"], d["item"])
            if cle in a and not d.get("rejet") and d.get("distribution"):
                pa, pb = a[cle]["distribution"], d["distribution"]
                if set(pa) == set(pb):
                    ordre = sorted(pa)
                    distances.append(R1.tv([pa[k] for k in ordre], [pb[k] for k in ordre]))
        sortie[modele] = float(np.mean(distances)) if distances else np.nan
    return sortie


def tests_h2(identites, bruit_machine, rng, n_boot, n_perm):
    lignes = []
    for modele in FERMES:
        for camp in ("gauche", "droite"):
            g = identites[(identites.get("modele", pd.Series(dtype=str)) == modele) &
                          (identites.get("camp", pd.Series(dtype=str)) == camp)] if len(identites) else pd.DataFrame()
            if len(g) < 3:
                lignes.append(_ligne("F2", "H2", modele, camp=camp))
                continue
            a, b = g["tv_entre_identites"].to_numpy(float), g["tv_plancher_w1_w2"].to_numpy(float)
            ratio, bas, haut, n = R1.ic_ratio_des_moyennes(a, b, rng, n_boot)
            # Nulle exacte A4=2. La permutation de signe suppose les differences
            # centrees symetriques autour de zero, item par item.
            p = R1.p_permutation_signe(a - 2.0 * b, rng, n_perm)
            bm = bruit_machine.get(modele, np.nan)
            lignes.append(_ligne("F2", "H2", modele, "EXECUTE", "A4 R1 et plancher machine",
                                 camp=camp, n_items=n, estimateur=ratio, ic_bas=bas, ic_haut=haut,
                                 p=p, distance_identites=float(np.mean(a)), plancher_machine=bm))
    return lignes


def tests_h3(ecarts_f1, ecarts_f2, orientes, rng, n_boot, n_perm):
    lignes = []
    for modele in FERMES:
        filtres = []
        for table in (ecarts_f1, ecarts_f2):
            g = table[(table.get("modele", pd.Series(dtype=str)) == modele) &
                      (table.get("identite", pd.Series(dtype=str)) == "journaliste") &
                      table.get("item", pd.Series(dtype=str)).isin(orientes)] if len(table) else pd.DataFrame()
            filtres.append(_apparier(g, ("gap_signe_decrit", "gap_signe_reel_w1")) if len(g) else pd.DataFrame())
        communs = sorted(set(filtres[0].index) & set(filtres[1].index)) if all(len(x) for x in filtres) else []
        if len(communs) < 3:
            lignes.extend([_ligne("F3", h, modele) for h in ("H3a", "H3b")])
            continue
        f1, f2 = filtres[0].loc[communs], filtres[1].loc[communs]
        r1, r2 = f1["gap_signe_reel_w1"].to_numpy(float), f2["gap_signe_reel_w1"].to_numpy(float)
        if not np.allclose(r1, r2, equal_nan=True, atol=1e-12):
            lignes.extend([_ligne("F3", h, modele, raison="referent non identique")
                           for h in ("H3a", "H3b")])
            continue
        d1, d2 = f1["gap_signe_decrit"].to_numpy(float), f2["gap_signe_decrit"].to_numpy(float)
        c, bas, haut, n = R4.ic_difference_de_facteurs(d2, d1, r1, rng, n_boot)
        delta = d2 - d1
        lignes.append(_ligne("F3", "H3a", modele, "EXECUTE", "F2-F1 centre sur 0",
                             n_items=n, estimateur=c, ic_bas=bas, ic_haut=haut,
                             p=R1.p_permutation_signe(delta, rng, n_perm), seuil=0.0))
        lignes.append(_ligne("F3", "H3b", modele, "EXECUTE", "F2-F1 centre sur +0,30",
                             n_items=n, estimateur=c, ic_bas=bas, ic_haut=haut,
                             p=R1.p_permutation_signe(delta - 0.30 * r1, rng, n_perm), seuil=0.30))
    return lignes


def appliquer_holm_fixe(lignes, famille, taille):
    idx = [i for i, x in enumerate(lignes) if x["famille"] == famille]
    if len(idx) != taille:
        raise RuntimeError(f"{famille}: {taille} tests attendus, {len(idx)} construits")
    ps = [lignes[i]["p"] if lignes[i]["statut"] == "EXECUTE" and
          np.isfinite(lignes[i]["p"]) else 1.0 for i in idx]
    for i, pc in zip(idx, R1.holm(np.asarray(ps, float))):
        if lignes[i]["statut"] != "EXECUTE":
            continue
        lignes[i]["p_holm"] = float(pc)
        if famille == "F2":
            m = lignes[i]
            m["retenu"] = bool(pc < .05 and m["ic_bas"] > 2 and
                                np.isfinite(m["plancher_machine"]) and
                                m["distance_identites"] > 2 * m["plancher_machine"])
        elif famille == "F3":
            m = lignes[i]
            ic_direction = m["ic_bas"] > 0 if m["hypothese"] == "H3a" else True
            m["retenu"] = bool(pc < .05 and m["estimateur"] > m["seuil"] and ic_direction)
    return lignes


def h4_exploratoire(ecarts, orientes, rng, n_boot, modeles_joues):
    """T et IC bootstrap apparie; aucune inference confirmatoire."""
    lignes = []
    for haut, bas in PAIRES_H4:
        if haut == SONNET and haut not in modeles_joues:
            continue
        par_modele = []
        for modele in (haut, bas):
            g = ecarts[(ecarts.get("modele", pd.Series(dtype=str)) == modele) &
                       (ecarts.get("identite", pd.Series(dtype=str)) == "journaliste") &
                       ecarts.get("item", pd.Series(dtype=str)).isin(orientes)] if len(ecarts) else pd.DataFrame()
            par_modele.append(_apparier(
                g, ("gap_signe_decrit", "gap_signe_reel_w1")) if len(g) else pd.DataFrame())
        communs = (sorted(set(par_modele[0].index) & set(par_modele[1].index))
                    if all(len(g) for g in par_modele) else [])
        base = {"hypothese": "H4", "condition_haute": haut,
                "condition_economique": bas, "n_items": len(communs),
                "portee": PORTEE, "reference": REFERENCE_ADDENDUM}
        if len(communs) < 3:
            lignes.append({**base, "statut": "INDISPONIBLE", "T": np.nan,
                           "ic_bas": np.nan, "ic_haut": np.nan})
            continue
        gh, gb = (g.loc[communs] for g in par_modele)
        dh = gh["gap_signe_decrit"].to_numpy(float)
        db = gb["gap_signe_decrit"].to_numpy(float)
        rh = gh["gap_signe_reel_w1"].to_numpy(float)
        rb = gb["gap_signe_reel_w1"].to_numpy(float)
        if not np.allclose(rh, rb, equal_nan=True, atol=1e-12) or rh.mean() == 0:
            lignes.append({**base, "statut": "INDISPONIBLE", "T": np.nan,
                           "ic_bas": np.nan, "ic_haut": np.nan})
            continue
        a2h, a2b = float(dh.mean() / rh.mean()), float(db.mean() / rh.mean())
        t_obs = abs(a2h - PLANCHER_A2) - abs(a2b - PLANCHER_A2)
        idx = rng.integers(0, len(dh), size=(n_boot, len(dh)))
        den = rh[idx].mean(axis=1)
        with np.errstate(divide="ignore", invalid="ignore"):
            th = dh[idx].mean(axis=1) / den
            tb = db[idx].mean(axis=1) / den
            tirages = np.abs(th - PLANCHER_A2) - np.abs(tb - PLANCHER_A2)
        tirages = tirages[np.isfinite(tirages)]
        if not len(tirages):
            lignes.append({**base, "statut": "INDISPONIBLE", "a2_haute": a2h,
                           "a2_economique": a2b, "T": t_obs,
                           "ic_bas": np.nan, "ic_haut": np.nan})
            continue
        lignes.append({**base, "statut": "EXPLORATOIRE", "a2_haute": a2h,
                       "a2_economique": a2b, "T": t_obs,
                       "ic_bas": float(np.percentile(tirages, 2.5)),
                       "ic_haut": float(np.percentile(tirages, 97.5))})
    return pd.DataFrame(lignes)


def descriptifs(cel1, eca1, ident1, eca2, orientes, n_boot):
    """A1/A2/A4 pour tout modele present, sans p comme l'impose le plan."""
    rng = np.random.default_rng(GRAINE + 1)
    lignes = []
    ok = cel1[~cel1["rejet"].astype(bool)] if len(cel1) else pd.DataFrame()
    for (modele, camp, identite), g in (ok.groupby(
            ["modele", "camp", "identite"], sort=False) if len(ok) else []):
        v, bas, haut, n = R1.ic_ratio_des_moyennes(
            g["gs_decrit"], g["gs_reel_w1"], rng, n_boot)
        lignes.append({"quantite": "A1", "format": "q4", "modele": modele,
                       "camp": camp, "identite": identite, "n_items": n,
                       "estimateur": v, "ic_bas": bas, "ic_haut": haut, "p": np.nan,
                       "portee": PORTEE})
    for format_, table in (("q4", eca1), ("q4gab3", eca2)):
        g0 = table[table["item"].isin(orientes)] if len(table) else pd.DataFrame()
        for (modele, identite), g in (g0.groupby(["modele", "identite"], sort=False)
                                      if len(g0) else []):
            v, bas, haut, n = R1.ic_ratio_des_moyennes(
                g["gap_signe_decrit"], g["gap_signe_reel_w1"], rng, n_boot)
            lignes.append({"quantite": "A2 signe", "format": format_, "modele": modele,
                           "camp": "", "identite": identite, "n_items": n,
                           "estimateur": v, "ic_bas": bas, "ic_haut": haut, "p": np.nan,
                           "portee": PORTEE})
    for (modele, camp), g in (ident1.groupby(["modele", "camp"], sort=False)
                              if len(ident1) else []):
        v, bas, haut, n = R1.ic_ratio_des_moyennes(
            g["tv_entre_identites"], g["tv_plancher_w1_w2"], rng, n_boot)
        lignes.append({"quantite": "A4", "format": "q4", "modele": modele,
                       "camp": camp, "identite": "deux identites", "n_items": n,
                       "estimateur": v, "ic_bas": bas, "ic_haut": haut, "p": np.nan,
                       "portee": PORTEE})
    return pd.DataFrame(lignes)


def _part_camp_constant(trace):
    groupes = {}
    for d in trace:
        if d.get("rejet") or not d.get("distribution"):
            continue
        groupes.setdefault((d.get("identite"), d.get("item")), {})[d.get("camp")] = d["distribution"]
    valeurs = []
    for g in groupes.values():
        if "gauche" in g and "droite" in g:
            valeurs.append(g["gauche"] == g["droite"])
    return float(np.mean(valeurs)) if valeurs else np.nan


def controles_entrees_bloquants(orientation, ref, effectifs, sens):
    """Invariants locaux figes avant toute analyse de modele."""
    items = orientation["item"].astype(str).tolist()
    n_items, n_orientes = len(items), int(orientation["oriente"].astype(bool).sum())
    lignes = [{"controle": "items", "valeur": n_items, "attendu": 149,
               "statut": "PASSE" if n_items == 149 and len(set(items)) == 149 else "REFUS"},
              {"controle": "items orientes", "valeur": n_orientes, "attendu": 79,
               "statut": "PASSE" if n_orientes == 79 else "REFUS"}]
    attendus = {"gauche": 417, "centre": 303, "droite": 332}
    obtenus = {}
    for camp in R1.CAMPS:
        valeurs = {n for (_item, c, vague), n in effectifs.items()
                   if c == camp and vague == "w1"}
        obtenus[camp] = max(valeurs) if valeurs else 0
    lignes.append({"controle": "effectifs", "valeur": json.dumps(obtenus, sort_keys=True),
                   "attendu": json.dumps(attendus, sort_keys=True),
                   "statut": "PASSE" if obtenus == attendus else "REFUS"})
    w1, w2 = [], []
    for item in items:
        cles = [(item, camp, vague) for camp in ("gauche", "droite")
                for vague in ("w1", "w2")]
        if not all(c in ref for c in cles):
            continue
        s = sens.get(item, np.nan)
        w1.append(R1.position(ref[(item, "droite", "w1")], s) -
                  R1.position(ref[(item, "gauche", "w1")], s))
        w2.append(R1.position(ref[(item, "droite", "w2")], s) -
                  R1.position(ref[(item, "gauche", "w2")], s))
    w1, w2 = np.asarray(w1, float), np.asarray(w2, float)
    ok = np.isfinite(w1) & np.isfinite(w2)
    plancher = float(w2[ok].mean() / w1[ok].mean()) if ok.any() and w1[ok].mean() else np.nan
    lignes.append({"controle": "plancher humain w2/w1", "valeur": plancher,
                   "attendu": "1,009 arrondi et dans [0,85;1,15]",
                   "statut": ("PASSE" if np.isfinite(plancher) and 0.85 <= plancher <= 1.15
                               and round(plancher, 3) == 1.009 else "REFUS")})
    return pd.DataFrame(lignes)


def controles(groupes):
    lignes = []
    for (modele, format_, passe), trace in sorted(groupes.items()):
        attendues = (CLIENT.PLANS["f1" if format_ == "q4" else "f2"]["cellules"]
                     if passe == "campagne" else (40 if passe == "plancher" else 10))
        rejets = sum(bool(x.get("rejet")) for x in trace)
        rejets_courts = sum(bool(x.get("rejet")) and x.get("n_modalites") in (2, 3)
                            for x in trace)
        constante = _part_camp_constant(trace) if format_ == "q4" and passe == "campagne" else np.nan
        complet = len(trace) == attendues
        format_tenu = bool(trace and rejets / len(trace) < .01 and rejets_courts == 0)
        fournisseurs = sorted({str(x.get("fournisseur")) for x in trace if x.get("fournisseur")})
        dates = sorted({str(x.get("horodatage", ""))[:10] for x in trace if x.get("horodatage")})
        statut = ("REFUS_H1_H2" if np.isfinite(constante) and constante > .90 else
                  ("PASSE" if complet else "PARTIEL"))
        lignes.append({"modele": modele, "format": format_, "passe": passe,
                       "cellules": len(trace), "cellules_attendues": attendues,
                       "rejets": rejets, "taux_rejet": rejets / len(trace) if trace else np.nan,
                       "rejets_k2_k3": rejets_courts, "format_tenu": format_tenu,
                       "fournisseurs": ";".join(fournisseurs), "dates": ";".join(dates),
                       "part_camp_constant": constante, "statut": statut, "portee": PORTEE})
    return pd.DataFrame(lignes)


def analyser(groupes, ref, options, effectifs, sens, orientes, n_boot=N_BOOT, n_perm=N_PERM):
    rng = np.random.default_rng(GRAINE)
    f1 = [d for (m, f, p), xs in groupes.items() if f == "q4" and p == "campagne" for d in xs]
    f2 = [d for (m, f, p), xs in groupes.items() if f == "q4gab3" and p == "campagne" for d in xs]
    cel1, eca1, ident1 = construire_tables(f1, ref, options, effectifs, sens)
    _cel2, eca2, _ident2 = construire_tables(f2, ref, options, effectifs, sens)
    desc = descriptifs(cel1, eca1, ident1, eca2, orientes, n_boot)
    a2 = calculer_a2(eca1, orientes, rng, n_boot)
    tests = tests_h2(ident1, planchers_machine(groupes), rng, n_boot, n_perm)
    tests += tests_h3(eca1, eca2, orientes, rng, n_boot, n_perm)
    complet = {}
    camps_ignores = set()
    for modele in FERMES:
        complet[(modele, "f1")] = len(groupes.get((modele, "q4", "campagne"), [])) == 894
        complet[(modele, "f2")] = len(groupes.get((modele, "q4gab3", "campagne"), [])) == 316
        complet[(modele, "plancher")] = len(groupes.get((modele, "q4", "plancher"), [])) == 40
        if _part_camp_constant(groupes.get((modele, "q4", "campagne"), [])) > .90:
            camps_ignores.add(modele)
    for ligne in a2.to_dict("records"):
        if ligne["statut"] == "EXECUTE" and ligne["modele"] in camps_ignores:
            a2.loc[a2["modele"] == ligne["modele"], ["statut", "raison_statut"]] = [
                "REFUSE", "camp ignore dans plus de 90 % des items"]
        elif ligne["statut"] == "EXECUTE" and not complet[(ligne["modele"], "f1")]:
            a2.loc[a2["modele"] == ligne["modele"], ["statut", "raison_statut"]] = [
                "PARTIEL", "collecte F1 incomplete"]
    h1 = evaluer_h1(a2)
    for ligne in tests:
        requis = (("f1", "plancher") if ligne["famille"] == "F2" else ("f1", "f2"))
        if ligne["famille"] == "F2" and ligne["modele"] in camps_ignores:
            ligne["statut"] = "REFUSE"
            ligne["raison_statut"] = "camp ignore dans plus de 90 % des items"
        elif ligne["statut"] == "EXECUTE" and not all(complet[(ligne["modele"], r)] for r in requis):
            ligne["statut"] = "PARTIEL"
            ligne["raison_statut"] = "collecte source incomplete"
    appliquer_holm_fixe(tests, "F2", 10)
    appliquer_holm_fixe(tests, "F3", 10)
    modeles = {m for m, _f, p in groupes if p == "campagne"}
    # L'addendum fixe 2 000 tirages pour H4, independamment des options de test CLI.
    h4 = h4_exploratoire(eca1, orientes, np.random.default_rng(GRAINE + 2),
                         N_BOOT, modeles)
    hypotheses = [h1]
    for h, minimum in (("H2", 4), ("H3a", 3), ("H3b", 3)):
        g = [x for x in tests if x["hypothese"] == h]
        par_modele = {
            m: (all(x["retenu"] for x in g if x["modele"] == m)
                if h == "H2" else any(x["retenu"] for x in g if x["modele"] == m))
            for m in FERMES
        }
        hypotheses.append({"hypothese": h, "famille": "F2" if h == "H2" else "F3",
                           "statut": "EVALUE" if all(any(x["statut"] == "EXECUTE" for x in g if x["modele"] == m)
                                                       for m in FERMES) else "INDECIDABLE",
                           "satisfaite": sum(par_modele.values()) >= minimum,
                           "p": np.nan, "raison": f"{sum(par_modele.values())}/5 modeles retenus",
                           "portee": PORTEE})
    hypotheses.append({"hypothese": "H4", "famille": "hors famille",
                       "statut": "EXPLORATOIRE", "satisfaite": np.nan, "p": np.nan,
                       "raison": "T et IC descriptifs; aucun verdict confirmatoire",
                       "portee": PORTEE})
    return desc, a2, pd.DataFrame(tests), pd.DataFrame(hypotheses), controles(groupes), h4


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifeste", type=Path, required=True)
    ap.add_argument("--sortie", type=Path, default=RESULTATS)
    ap.add_argument("--tirages-bootstrap", type=int, default=N_BOOT)
    ap.add_argument("--permutations", type=int, default=N_PERM)
    args = ap.parse_args(argv)
    orientation = pd.read_csv(RESULTATS / "a37-orientation-items.csv")
    items = list(zip(orientation["item"].astype(str), orientation["oriente"].astype(bool)))
    groupes = charger_traces(args.manifeste, items)
    referent = Path(CLIENT.REFERENT)
    if not referent.is_file() or sha256(referent) != REFERENT_SHA256:
        raise RuntimeError("referent humain absent ou empreinte incompatible")
    ref, options, effectifs = R1.lire_referent()
    sens = dict(zip(orientation["item"], orientation["sens_codeur_A"]))
    orientes = set(orientation.loc[orientation["oriente"].astype(bool), "item"])
    entrees = controles_entrees_bloquants(orientation, ref, effectifs, sens)
    if not entrees["statut"].eq("PASSE").all():
        raise RuntimeError("controle bloquant des entrees locales refuse")
    desc, a2, tests, hypotheses, ctl, h4 = analyser(
        groupes, ref, options, effectifs, sens, orientes,
        args.tirages_bootstrap, args.permutations)
    args.sortie.mkdir(parents=True, exist_ok=True)
    desc.to_csv(args.sortie / "r6-descriptifs.csv", index=False)
    a2.to_csv(args.sortie / "r6-a2-fermes.csv", index=False)
    tests.to_csv(args.sortie / "r6-tests-confirmatoires.csv", index=False)
    hypotheses.to_csv(args.sortie / "r6-hypotheses.csv", index=False)
    h4.to_csv(args.sortie / "r6-h4-exploratoire.csv", index=False)
    ctl["controle"] = "trace"
    pd.concat([entrees, ctl], ignore_index=True, sort=False).to_csv(
        args.sortie / "r6-controles-evaluation.csv", index=False)
    print(json.dumps({"statut": "termine", "tests": len(tests),
                      "h4": "EXPLORATOIRE sans p ni verdict confirmatoire",
                      "reference_h4": REFERENCE_ADDENDUM, "reseau": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
