"""Analyse fine R6, strictement hors réseau et réservée aux campagnes terminales.

Ce module ne calcule aucun verdict H1--H3 : ils restent dans ``r6_evaluer.py``.
Il refuse une trace active avant de l'ouvrir : le manifeste doit être scellé, le
ledger doit contenir exactement 894 F1 + 316 F2 + 40 plancher, toutes réglées,
dans l'ordre du plan. Seule exception, instrumentale : une cellule rejouée après un 429
prouvé non facturé peut apparaître plus tard, jamais plus tôt (erratum
``resultats/r6-erratum-chargeur-rejeux-429-2026-09-11.md``). Les deux passes pilote ne
sont jamais admises comme entrée.

Entrée : un manifeste JSON ``R6-analyse-fine-1`` décrivant les empreintes des
traces terminales, du ledger, du référent, d'A37 et de la liste du plancher.
Sortie : tableaux exploratoires sans p, Holm, IC ou verdict confirmatoire.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import itertools
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import r1_evaluer as R1  # noqa: E402
import r6_oracle_distant as R6  # noqa: E402


ROOT = Path(__file__).resolve().parent.parent
RESULTATS = ROOT / "resultats"
PASSES_ANALYSE = (("campagne", "q4", 894), ("campagne", "q4gab3", 316),
                  ("plancher", "q4", 40))
PASSES_PILOTE = {"essai-1", "essai-2", "ancien-pilote"}
MIN_ITEMS = 5
# Contrôle d'intégrité du chargeur seulement : preuves de non-facturation 429 admises pour
# une suite réservation -> annulation -> réservation -> réconciliation d'une même identité.
PREUVE_429_AUTOMATIQUE = "429-non-facture"  # préfixe des annulations de l'amendement 429
PREUVES_429_MANUELLES = {  # texte exact au registre de production -> seule identité admise
    "generation metadata/content GET=404 twice; credits delta from first campaign preflight "
    "matches 138 confirmed trace costs within 0.0000000581 USD; no other R6 client":
        '["deepseek/deepseek-v4-flash","q4","r1-d1","fucitzn","gauche","journaliste","campagne"]',
    "second 429: metadata/content GET=404 twice; credits and total_usage stable across probes; "
    "preflight-to-probe delta 0.002203544 USD matches 138 settled trace costs 0.0022036021 "
    "within 0.0000000581 USD":
        '["deepseek/deepseek-v4-flash","q4","r1-d1","fucitzn","gauche","journaliste","campagne"]',
    "colhomo 429 gen-1789080588-aqog8HYnALcKxZ8mPlJL: metadata/content GET=404 twice; credits "
    "and total_usage stable across probes; total_usage 149.259209016 vs expected 149.2592090606 "
    "(00:39 baseline + 82 settled cells 0.0013209756 USD), delta -4.46E-8 USD":
        '["deepseek/deepseek-v4-flash","q4","r1-d1","colhomo","gauche","adversaire","campagne"]',
}
MAX_ANNULATIONS_429 = 2


class ChargementTerminalRefuse(ValueError):
    """Une source n'est pas une campagne R6 stable et scellée."""


@dataclass
class Campagne:
    modele: str
    fournisseur: str
    role: str
    non_deterministe: bool
    traces: dict[tuple[str, str], list[dict]]
    operations_reglees: list[dict]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for bloc in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def _path(base: Path, raw: str) -> Path:
    p = Path(raw)
    return p if p.is_absolute() else (base / p).resolve()


def _json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ChargementTerminalRefuse(f"JSON absent ou invalide: {path}") from exc
    if not isinstance(value, dict):
        raise ChargementTerminalRefuse("objet JSON attendu")
    return value


def _verifier_empreinte(base: Path, spec: dict, cle: str) -> Path:
    if not isinstance(spec, dict) or not spec.get("path") or not spec.get("sha256"):
        raise ChargementTerminalRefuse(f"{cle}: chemin ou empreinte absent")
    path = _path(base, str(spec["path"]))
    if not path.is_file() or sha256(path) != spec["sha256"]:
        raise ChargementTerminalRefuse(f"{cle}: empreinte absente ou différente")
    return path


def _lire_jsonl_strict(path: Path) -> list[dict]:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ChargementTerminalRefuse(f"trace absente: {path.name}") from exc
    if not text.endswith("\n"):
        raise ChargementTerminalRefuse(f"trace non terminée: {path.name}")
    rows = []
    for no, line in enumerate(text.splitlines(), 1):
        if not line:
            raise ChargementTerminalRefuse(f"ligne vide: {path.name}:{no}")
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ChargementTerminalRefuse(f"JSONL invalide: {path.name}:{no}") from exc
        if not isinstance(row, dict):
            raise ChargementTerminalRefuse(f"ligne JSON non objet: {path.name}:{no}")
        rows.append(row)
    return rows


def lire_orientation(path: Path) -> tuple[list[str], set[str], dict[str, float], str]:
    d = pd.read_csv(path, keep_default_na=False)
    requis = {"item", "oriente", "sens_codeur_A"}
    if not requis <= set(d.columns) or len(d) != 149 or d["item"].duplicated().any():
        raise ChargementTerminalRefuse("A37 incomplet ou non unique")
    items = d["item"].astype(str).tolist()
    marqueurs = d["oriente"].astype(str).str.strip().str.lower()
    if not marqueurs.isin({"true", "false", "1", "0"}).all():
        raise ChargementTerminalRefuse("marqueur A37 oriente invalide")
    orientes = set(d.loc[marqueurs.isin({"true", "1"}), "item"].astype(str))
    if len(orientes) != 79:
        raise ChargementTerminalRefuse("A37 doit contenir exactement 79 items orientés")
    sens = dict(zip(d["item"].astype(str), pd.to_numeric(d["sens_codeur_A"], errors="coerce")))
    if not np.isfinite(list(sens.values())).all():
        raise ChargementTerminalRefuse("sens A37 non fini")
    if any(sens[item] == 0 for item in orientes):
        raise ChargementTerminalRefuse("sens A37 nul pour un item orienté")
    return items, orientes, sens, sha256(path)


def lire_referent(path: Path) -> tuple[dict, dict, dict]:
    d = pd.read_csv(path, keep_default_na=False, na_values=[""])
    requis = {"item", "camp", "vague", "rang", "modalite", "p", "n", "effectif"}
    if not requis <= set(d.columns):
        raise ChargementTerminalRefuse("référent humain incomplet")
    for col in ("rang", "p", "n", "effectif"):
        d[col] = pd.to_numeric(d[col], errors="coerce")
    ref, options, effectifs = {}, {}, {}
    for (item, camp, vague), g in d.groupby(["item", "camp", "vague"], sort=False):
        g = g.sort_values("rang")
        p = g["p"].to_numpy(float)
        if not len(p) or not np.isfinite(p).all() or not np.isclose(p.sum(), 1.0, atol=1e-6):
            raise ChargementTerminalRefuse("distribution humaine invalide")
        ref[(str(item), str(camp), str(vague))] = p
        options[str(item)] = g["modalite"].astype(str).tolist()
        effectifs[(str(item), str(camp), str(vague))] = int(g["n"].iloc[0])
    return ref, options, effectifs


def _attendus(items: list[str], orientes: set[str], plancher: list[tuple[str, str, str]]):
    f1 = list(R6.R1.cellules(items, ["gauche", "centre", "droite"], list(R6.R1.IDENTITES)))
    f2_items = [item for item in items if item in orientes]
    f2 = list(R6.R1.cellules(f2_items, ["gauche", "droite"], list(R6.R1.IDENTITES)))
    if len(f1) != 894 or len(f2) != 316 or len(plancher) != 40:
        raise ChargementTerminalRefuse("volumes F1/F2/plancher inattendus")
    if len(set(plancher)) != 40 or not set(plancher) <= set(f1):
        raise ChargementTerminalRefuse("liste du plancher non unique ou hors F1")
    return {("campagne", "q4"): f1, ("campagne", "q4gab3"): f2,
            ("plancher", "q4"): list(plancher)}


def _lire_plancher(path: Path) -> list[tuple[str, str, str]]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
        rows = []
        for no, line in enumerate(lines, 1):
            if not line:
                raise ValueError(f"ligne vide {no}")
            item, camp, identity = line.split("\t")
            rows.append((camp, identity, item))
    except (OSError, ValueError) as exc:
        raise ChargementTerminalRefuse("liste du plancher invalide") from exc
    return rows


def _preuve_429_non_facture(ident: str, preuve) -> bool:
    if not isinstance(preuve, str):
        return False
    return preuve.startswith(PREUVE_429_AUTOMATIQUE) or PREUVES_429_MANUELLES.get(preuve) == ident


def _ordre_conforme(observees: list, attendues: list, deplacables: set) -> bool:
    """Même ensemble sans doublon ; ordre de plan strict hors cellules rejouées après 429.

    Une cellule déplaçable peut apparaître plus tard que son rang, jamais avant une cellule
    non déplaçable qui la précède dans le plan. Sans cellule déplaçable : égalité exacte.
    """
    if (len(observees) != len(attendues) or len(set(observees)) != len(observees)
            or set(observees) != set(attendues)):
        return False
    rang = {cell: i for i, cell in enumerate(attendues)}
    precedent = -1
    for cell in observees:
        if cell not in deplacables and rang[cell] <= precedent:
            return False
        precedent = max(precedent, rang[cell])
    return True


def _operations_terminales(ledger: Path, modele: str, attendus: dict) -> list[dict]:
    """Reconstruit l'état, sans importer les pilotes dans le jeu analysable."""
    rows = _lire_jsonl_strict(ledger)
    operations: dict[str, dict] = {}
    annulations: dict[str, list] = {}
    ordre: list[str] = []
    for event in rows:
        kind = event.get("type")
        if kind in {"initialisation", "import-complet"}:
            continue
        ident = event.get("identite")
        if not isinstance(ident, str):
            continue
        if kind in {"reservation", "historique", "historique-incertain"}:
            if ident in operations:
                op = operations[ident]
                if not (kind == "reservation" and op.get("type") == "reservation"
                        and op.get("etat") == "annulee"):
                    raise ChargementTerminalRefuse("opération ledger dupliquée")
                preuves = annulations.get(ident, [])
                if not preuves or not all(_preuve_429_non_facture(ident, p) for p in preuves):
                    raise ChargementTerminalRefuse("rejeu ledger sans preuve 429 de non-facturation")
                if len(preuves) > MAX_ANNULATIONS_429:
                    raise ChargementTerminalRefuse("rejeu ledger après plus de 2 annulations 429")
                if (event.get("empreinte_requete") != op.get("empreinte_requete")
                        or event.get("fournisseur_impose") != op.get("fournisseur_impose")):
                    raise ChargementTerminalRefuse("rejeu ledger d'empreinte ou de fournisseur différent")
                rejeux = op.get("rejeux_429", 0) + 1
                op.update(event)
                op.update(etat="reservation", rejeux_429=rejeux)
                # Une cellule ne compte qu'une fois, à la position de sa dernière réservation.
                ordre.remove(ident)
                ordre.append(ident)
                continue
            operations[ident] = dict(event, etat=("reglee" if kind == "historique" else kind))
            ordre.append(ident)
        elif kind == "reconciliation":
            if ident not in operations:
                raise ChargementTerminalRefuse("réconciliation sans réservation")
            operations[ident].update(event)
            operations[ident]["etat"] = "reglee"
        elif kind == "annulation":
            if ident not in operations:
                raise ChargementTerminalRefuse("annulation sans réservation")
            operations[ident]["etat"] = "annulee"
            annulations.setdefault(ident, []).append(event.get("preuve"))
        else:
            raise ChargementTerminalRefuse("événement ledger inconnu")

    cible = []
    for ident in ordre:
        op = operations[ident]
        try:
            champs = json.loads(ident)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ChargementTerminalRefuse("identité ledger invalide") from exc
        if not isinstance(champs, list) or len(champs) != 7:
            raise ChargementTerminalRefuse("identité ledger incomplète")
        if champs[0] == modele and champs[-1] in {"campagne", "plancher"}:
            cible.append(op)
    if len(cible) != 1250 or any(op.get("etat") != "reglee" for op in cible):
        raise ChargementTerminalRefuse("modèle non terminal: 1 250 opérations réglées exigées")

    expected = []
    for passe, format_, _n in PASSES_ANALYSE:
        expected.extend((passe, format_, cell) for cell in attendus[(passe, format_)])
    decoded, rejouees = [], set()
    for op in cible:
        model, fmt, version, item, camp, identity, passe = json.loads(op["identite"])
        decoded.append((passe, fmt, version, camp, identity, item))
        if op.get("rejeux_429"):
            rejouees.add(decoded[-1])
    wanted = [(passe, fmt, R6.FORMATS[fmt], camp, identity, item)
              for passe, fmt, (camp, identity, item) in expected]
    if not _ordre_conforme(decoded, wanted, rejouees):
        raise ChargementTerminalRefuse("ordre exact F1/F2/plancher du ledger différent")
    if any(not isinstance(op.get("empreinte_requete"), str) or not op["empreinte_requete"]
           or not isinstance(op.get("fournisseur_impose"), str) or not op["fournisseur_impose"]
           for op in cible):
        raise ChargementTerminalRefuse("provenance ledger incomplète")
    return cible


def _charger_trace(spec: dict, base: Path, modele: str, fournisseur: str,
                   expected: list[tuple[str, str, str]], passe: str, format_: str,
                   options: dict, operations: dict[str, dict]) -> list[dict]:
    path = _verifier_empreinte(base, spec, f"trace {passe}/{format_}")
    if Path(str(path) + ".en-cours").exists():
        raise ChargementTerminalRefuse("trace active marquée .en-cours")
    rows = _lire_jsonl_strict(path)
    if len(rows) != len(expected):
        raise ChargementTerminalRefuse("trace terminale de volume incorrect")
    configuration = spec.get("configuration")
    if not isinstance(configuration, dict):
        raise ChargementTerminalRefuse("configuration de trace absente du manifeste")
    cells = [(str(row.get("camp")), str(row.get("identite")), str(row.get("item")))
             for row in rows]
    rejouees = {cell for cell in expected if operations.get(R6.identite_campagne(
        modele, format_, R6.FORMATS[format_], cell[2], cell[0], cell[1], passe), {}).get("rejeux_429")}
    if not _ordre_conforme(cells, expected, rejouees):
        raise ChargementTerminalRefuse("ordre exact ou unicité de trace différent")
    for no, row in enumerate(rows, 1):
        cell = (str(row.get("camp")), str(row.get("identite")), str(row.get("item")))
        required = {
            "modele": modele, "format": format_, "version_prompt": R6.FORMATS[format_],
            "gabarit": R6.GABARIT, "n_tentatives": 1, "sans_relance": True,
            "erreur": None, "fournisseur": fournisseur,
            "quantification": fournisseur, "fournisseur_impose": fournisseur,
            "passe": passe,
        }
        bad = [key for key, value in required.items() if row.get(key) != value]
        if bad or row.get("configuration") != configuration:
            raise ChargementTerminalRefuse(f"trace {passe}/{format_} incohérente ligne {no}")
        ident = R6.identite_campagne(modele, format_, R6.FORMATS[format_], cell[2], cell[0],
                                     cell[1], passe)
        op = operations.get(ident)
        if (op is None or row.get("empreinte_requete") != op["empreinte_requete"]
                or op["fournisseur_impose"] != fournisseur):
            raise ChargementTerminalRefuse(f"provenance trace/ledger incohérente ligne {no}")
        if type(row.get("rejet")) is not bool:
            raise ChargementTerminalRefuse("marqueur de rejet non booléen")
        if row.get("n_modalites") != len(options.get(cell[2], [])):
            raise ChargementTerminalRefuse("nombre de modalités de trace incompatible")
        if not row.get("rejet"):
            distribution = row.get("distribution")
            if not isinstance(distribution, dict) or list(distribution) != options[cell[2]]:
                raise ChargementTerminalRefuse("distribution de trace incompatible au référent")
            values = np.asarray(list(distribution.values()), float)
            if not np.isfinite(values).all() or (values < 0).any() or not np.isclose(values.sum(), 1, atol=1e-6):
                raise ChargementTerminalRefuse("distribution de trace non normalisée")
    return rows


def charger_campagnes(manifeste_path: Path) -> tuple[list[Campagne], tuple]:
    """Ne lit une trace qu'après la garde terminale du ledger et les empreintes."""
    manifeste_path = manifeste_path.resolve()
    base = manifeste_path.parent
    manifeste = _json(manifeste_path)
    if manifeste.get("version") != "R6-analyse-fine-1":
        raise ChargementTerminalRefuse("version de manifeste analyse fine inconnue")
    orientation_path = _verifier_empreinte(base, manifeste.get("orientation"), "orientation")
    referent_path = _verifier_empreinte(base, manifeste.get("referent"), "référent")
    items, orientes, sens, orientation_sha = lire_orientation(orientation_path)
    ref, options, effectifs = lire_referent(referent_path)
    model_specs = manifeste.get("models")
    if not isinstance(model_specs, list):
        raise ChargementTerminalRefuse("liste des modèles absente")
    campaigns = []
    modeles_vus = set()
    for spec in model_specs:
        if not isinstance(spec, dict) or spec.get("terminal") != "TERMINE":
            raise ChargementTerminalRefuse("modèle non terminal dans le manifeste")
        modele, fournisseur = spec.get("model"), spec.get("provider")
        if not isinstance(modele, str) or not isinstance(fournisseur, str) or not fournisseur:
            raise ChargementTerminalRefuse("modèle ou fournisseur absent")
        if modele in modeles_vus:
            raise ChargementTerminalRefuse("modèle dupliqué dans le manifeste")
        modeles_vus.add(modele)
        role = spec.get("analysis_role")
        if role not in {"descriptif", "confirmatoire"}:
            raise ChargementTerminalRefuse("rôle analytique absent ou invalide")
        floor_path = _verifier_empreinte(base, spec.get("floor_cells"), "liste plancher")
        expected = _attendus(items, orientes, _lire_plancher(floor_path))
        ledger_path = _verifier_empreinte(base, spec.get("ledger"), "ledger")
        # Cette garde précède volontairement toute ouverture des trois traces de campagne.
        operations = _operations_terminales(ledger_path, modele, expected)
        operations_par_identite = {op["identite"]: op for op in operations}
        trace_specs = spec.get("traces")
        if not isinstance(trace_specs, list) or len(trace_specs) != 3:
            raise ChargementTerminalRefuse("trois traces terminales, et trois seulement, exigées")
        declared = {(x.get("passe"), x.get("format")) for x in trace_specs if isinstance(x, dict)}
        if declared != {(p, f) for p, f, _n in PASSES_ANALYSE}:
            if any(isinstance(x, dict) and x.get("passe") in PASSES_PILOTE for x in trace_specs):
                raise ChargementTerminalRefuse("passe pilote interdite dans l'analyse de campagne")
            raise ChargementTerminalRefuse("F1/F2/plancher requis, aucun pilote admis")
        traces = {}
        for trace_spec in trace_specs:
            passe, format_ = trace_spec["passe"], trace_spec["format"]
            traces[(passe, format_)] = _charger_trace(
                trace_spec, base, modele, fournisseur, expected[(passe, format_)],
                passe, format_, options, operations_par_identite)
        campaigns.append(Campagne(modele, fournisseur, role, bool(spec.get("non_deterministe")),
                                  traces, operations))
    if not campaigns:
        raise ChargementTerminalRefuse("aucun modèle terminal")
    return campaigns, (ref, options, effectifs, items, orientes, sens, orientation_sha)


def _consensus(ref: dict, item: str, camp: str) -> float:
    return float(np.max(ref[(item, camp, "w1")]))


def _polarite(item: str, orientes: set[str], sens: dict[str, float]):
    if item not in orientes:
        return np.nan
    value = sens.get(item, np.nan)
    return "positive" if value > 0 else "negative" if value < 0 else np.nan


def _terciles(values: pd.Series) -> tuple[float, float]:
    clean = values[np.isfinite(values.to_numpy(float))]
    if not len(clean):
        return np.nan, np.nan
    return float(np.quantile(clean, 1 / 3)), float(np.quantile(clean, 2 / 3))


def _etiquette_tercile(value: float, cuts: tuple[float, float]):
    if not np.isfinite(value) or not np.isfinite(cuts[0]) or not np.isfinite(cuts[1]):
        return np.nan
    return "bas" if value <= cuts[0] else ("moyen" if value <= cuts[1] else "haut")


def _metadata_cells(cel: pd.DataFrame, ref: dict, orientes: set[str], sens: dict) -> pd.DataFrame:
    d = cel.copy()
    d["consensus_humain"] = [_consensus(ref, i, c) for i, c in zip(d["item"], d["camp"])]
    d["polarite"] = [_polarite(i, orientes, sens) for i in d["item"]]
    d["ratio_gs"] = d["gs_decrit"] / d["gs_reel_w1"]
    d["s_uniforme"] = [
        R1.tv(json.loads(p), np.repeat(1 / n, n)) - R1.tv(ref[(item, camp, "w1")], np.repeat(1 / n, n))
        if not rejected else np.nan
        for p, n, item, camp, rejected in zip(d.get("p_decrit", pd.Series([None] * len(d))),
                                               d["n_modalites"], d["item"], d["camp"], d["rejet"])
    ]
    cuts = _terciles(d["consensus_humain"])
    d["consensus_tercile"] = [_etiquette_tercile(v, cuts) for v in d["consensus_humain"]]
    return d


def _metadata_items(ecarts: pd.DataFrame, cel: pd.DataFrame, ref: dict,
                    orientes: set[str], sens: dict) -> pd.DataFrame:
    rows = []
    for (_, identity, item), g in cel.groupby(["modele", "identite", "item"], sort=False):
        if {"gauche", "droite"} <= set(g["camp"]):
            fam = g["famille"].dropna().unique()
            nmod = g["n_modalites"].dropna().unique()
            rows.append({"identite": identity, "item": item,
                         "famille": fam[0] if len(fam) == 1 else np.nan,
                         "n_modalites": nmod[0] if len(nmod) == 1 else np.nan,
                         "consensus_humain": (_consensus(ref, item, "gauche") +
                                               _consensus(ref, item, "droite")) / 2,
                         "polarite": _polarite(item, orientes, sens)})
    meta = pd.DataFrame(rows).drop_duplicates(["identite", "item"])
    d = ecarts.merge(meta, on=["identite", "item"], how="left")
    cuts = _terciles(meta["consensus_humain"]) if len(meta) else (np.nan, np.nan)
    d["consensus_tercile"] = [_etiquette_tercile(v, cuts) for v in d["consensus_humain"]]
    return d


def _resumer_strates(records: pd.DataFrame) -> pd.DataFrame:
    lines = []
    dimensions = ("famille", "polarite", "n_modalites", "consensus_tercile")
    keys = ["modele", "format", "quantite"]
    for dimension in dimensions:
        for group_key, g in records.groupby(keys + [dimension], dropna=False, sort=False):
            *base, stratum = group_key
            values = pd.to_numeric(g["valeur"], errors="coerce").dropna()
            status = ("EXPLORATOIRE" if len(values) >= MIN_ITEMS and not pd.isna(stratum)
                      else "NON_INTERPRETABLE")
            lines.append(dict(zip(keys, base), dimension=dimension,
                              strate="ABSENTE" if pd.isna(stratum) else str(stratum),
                              n_items=int(len(values)), statut=status,
                              moyenne=float(values.mean()) if status == "EXPLORATOIRE" else np.nan,
                              mediane=float(values.median()) if status == "EXPLORATOIRE" else np.nan,
                              q25=float(values.quantile(.25)) if status == "EXPLORATOIRE" else np.nan,
                              q75=float(values.quantile(.75)) if status == "EXPLORATOIRE" else np.nan))
    return pd.DataFrame(lines)


def _leaveout(table: pd.DataFrame, keys: list[str], value: str, denom: str,
              quantity: str) -> pd.DataFrame:
    rows = []
    for key, g in table.groupby(keys, sort=False):
        g = g[np.isfinite(pd.to_numeric(g[value], errors="coerce")) &
              np.isfinite(pd.to_numeric(g[denom], errors="coerce"))].copy()
        base = dict(zip(keys, key if isinstance(key, tuple) else (key,)))
        if len(g) < MIN_ITEMS or g[denom].mean() == 0:
            rows.append({**base, "quantite": quantity, "retrait_type": "aucun",
                         "retrait": "", "n_items": len(g), "statut": "NON_INTERPRETABLE",
                         "estimateur_complet": np.nan, "estimateur_retrait": np.nan})
            continue
        full = float(g[value].mean() / g[denom].mean())
        for removal_type, column in (("item", "item"), ("famille", "famille")):
            for removal in sorted(g[column].dropna().astype(str).unique()):
                h = g[g[column].astype(str) != removal]
                estimate = (float(h[value].mean() / h[denom].mean())
                            if len(h) >= MIN_ITEMS and h[denom].mean() != 0 else np.nan)
                rows.append({**base, "quantite": quantity, "retrait_type": removal_type,
                             "retrait": removal, "n_items": len(h),
                             "statut": "EXPLORATOIRE" if np.isfinite(estimate) else "NON_INTERPRETABLE",
                             "estimateur_complet": full, "estimateur_retrait": estimate})
    return pd.DataFrame(rows)


def _safe_spearman(a: pd.Series, b: pd.Series) -> float:
    a, b = np.asarray(a, float), np.asarray(b, float)
    if len(a) < MIN_ITEMS or not np.isfinite(a).all() or not np.isfinite(b).all():
        return np.nan
    if np.ptp(a) == 0 or np.ptp(b) == 0:
        return np.nan
    return float(R1.spearman(a, b))


def _intermodel(prepared: dict[str, dict]) -> pd.DataFrame:
    rows = []
    for left, right in itertools.combinations(sorted(prepared), 2):
        a, b = prepared[left], prepared[right]
        for fmt, table_name, keys, value in (
            ("q4", "cells_f1", ["camp", "identite", "item"], "gs_decrit"),
            ("q4gab3", "cells_f2", ["camp", "identite", "item"], "gs_decrit"),
            ("q4", "a2_f1", ["identite", "item"], "gap_signe_decrit"),
            ("q4gab3", "a2_f2", ["identite", "item"], "gap_signe_decrit"),
            ("q4", "a4", ["camp", "item"], "tv_entre_identites"),
        ):
            x, y = a[table_name], b[table_name]
            if not len(x) or not len(y):
                continue
            if table_name.startswith("cells"):
                x, y = x[~x["rejet"]], y[~y["rejet"]]
            merged = x[keys + [value] + (["p_decrit"] if table_name.startswith("cells") else [])].merge(
                y[keys + [value] + (["p_decrit"] if table_name.startswith("cells") else [])],
                on=keys, suffixes=("_a", "_b"))
            group_keys = [k for k in keys if k != "item"]
            for key, g in merged.groupby(group_keys, sort=False):
                base = dict(zip(group_keys, key if isinstance(key, tuple) else (key,)))
                rho = _safe_spearman(g[f"{value}_a"], g[f"{value}_b"])
                tv_mean = np.nan
                if table_name.startswith("cells") and len(g) >= MIN_ITEMS:
                    tv_mean = float(np.mean([R1.tv(json.loads(x), json.loads(y))
                                             for x, y in zip(g["p_decrit_a"], g["p_decrit_b"])]))
                status = "EXPLORATOIRE" if len(g) >= MIN_ITEMS and np.isfinite(rho) else "NON_INTERPRETABLE"
                rows.append({"modele_a": left, "modele_b": right, "format": fmt,
                             "quantite": table_name, **base, "n_items": len(g), "statut": status,
                             "tv_intermodel_moyenne": tv_mean, "rho_spearman": rho})
    return pd.DataFrame(rows)


def _stabilite(campagne: Campagne, f1: pd.DataFrame, floor: pd.DataFrame) -> pd.DataFrame:
    keys = ["camp", "identite", "item"]
    a = f1[~f1["rejet"]].copy()
    b = floor[~floor["rejet"]].copy()
    g = a[keys + ["p_decrit", "gs_decrit"]].merge(
        b[keys + ["p_decrit", "gs_decrit"]], on=keys, suffixes=("_campagne", "_plancher"))
    if len(g) < MIN_ITEMS:
        return pd.DataFrame([{"modele": campagne.modele, "non_deterministe": campagne.non_deterministe,
                              "n_cellules": len(g), "statut": "NON_INTERPRETABLE",
                              "tv_moyenne": np.nan, "tv_mediane": np.nan, "tv_max": np.nan,
                              "variation_gs_moyenne": np.nan}])
    tvs = np.asarray([R1.tv(json.loads(x), json.loads(y))
                      for x, y in zip(g["p_decrit_campagne"], g["p_decrit_plancher"])])
    dgs = np.abs(g["gs_decrit_campagne"].to_numpy(float) - g["gs_decrit_plancher"].to_numpy(float))
    return pd.DataFrame([{"modele": campagne.modele, "non_deterministe": campagne.non_deterministe,
                          "n_cellules": len(g), "statut": "EXPLORATOIRE",
                          "tv_moyenne": float(tvs.mean()), "tv_mediane": float(np.median(tvs)),
                          "tv_max": float(tvs.max()), "variation_gs_moyenne": float(dgs.mean())}])


def analyser(campagnes: list[Campagne], contexte: tuple) -> dict[str, pd.DataFrame]:
    ref, options, effectifs, _items, orientes, sens, orientation_sha = contexte
    prepared: dict[str, dict] = {}
    coverage, cell_records, item_records, leaveouts, stability = [], [], [], [], []
    for campagne in campagnes:
        rows_f1 = campagne.traces[("campagne", "q4")]
        rows_f2 = campagne.traces[("campagne", "q4gab3")]
        rows_floor = campagne.traces[("plancher", "q4")]
        cells_f1 = _metadata_cells(R1.par_cellule(rows_f1, ref, options, sens, effectifs), ref, orientes, sens)
        cells_f2 = _metadata_cells(R1.par_cellule(rows_f2, ref, options, sens, effectifs), ref, orientes, sens)
        cells_floor = _metadata_cells(R1.par_cellule(rows_floor, ref, options, sens, effectifs), ref, orientes, sens)
        a2_f1 = _metadata_items(R1.par_item_ecarts(cells_f1, ref, sens), cells_f1, ref, orientes, sens)
        a2_f2 = _metadata_items(R1.par_item_ecarts(cells_f2, ref, sens), cells_f2, ref, orientes, sens)
        a4 = R1.par_item_identite(cells_f1, ref)
        a4 = a4.merge(cells_f1[["camp", "item", "famille", "n_modalites", "consensus_humain",
                                 "polarite", "consensus_tercile"]].drop_duplicates(["camp", "item"]),
                      on=["camp", "item"], how="left")
        a2_f1["format"] = "q4"
        a2_f2["format"] = "q4gab3"
        a4["format"] = "q4"
        delta = a2_f1.merge(a2_f2, on=["identite", "item"], suffixes=("_f1", "_f2"))
        delta["format"] = "F2-F1"
        delta["delta_gap"] = delta["gap_signe_decrit_f2"] - delta["gap_signe_decrit_f1"]
        delta["gap_signe_reel_w1"] = delta["gap_signe_reel_w1_f1"]
        delta["famille"] = delta["famille_f1"]

        for format_, cells in (("q4", cells_f1), ("q4gab3", cells_f2)):
            cells = cells.copy()
            cells["format"] = format_
            for metric in ("ratio_gs", "tv_decrit_reel", "s_uniforme"):
                z = cells[["modele", "format", "camp", "identite", "item", "famille", "polarite",
                           "n_modalites", "consensus_tercile", metric]].rename(columns={metric: "valeur"})
                z["quantite"] = metric
                cell_records.append(z)
        for format_, table in (("q4", a2_f1), ("q4gab3", a2_f2)):
            z = table[["modele", "format", "identite", "item", "famille", "polarite", "n_modalites",
                       "consensus_tercile", "gap_signe_decrit"]].rename(columns={"gap_signe_decrit": "valeur"})
            z["camp"] = ""
            z["quantite"] = "gap_signe_decrit"
            item_records.append(z)
        z = a4[["modele", "format", "camp", "item", "famille", "polarite", "n_modalites",
                "consensus_tercile", "tv_entre_identites"]].rename(columns={"tv_entre_identites": "valeur"})
        z["identite"] = "deux identites"
        z["quantite"] = "tv_entre_identites"
        item_records.append(z)
        z = delta[["modele_f1", "format", "identite", "item", "famille", "polarite_f1", "n_modalites_f1",
                   "consensus_tercile_f1", "delta_gap"]].rename(columns={"modele_f1": "modele",
                     "polarite_f1": "polarite", "n_modalites_f1": "n_modalites",
                     "consensus_tercile_f1": "consensus_tercile", "delta_gap": "valeur"})
        z["camp"] = ""
        z["quantite"] = "delta_gap_F2_moins_F1"
        item_records.append(z)

        leaveouts.extend([
            _leaveout(cells_f1, ["modele", "camp", "identite"], "gs_decrit", "gs_reel_w1", "A1"),
            _leaveout(a2_f1[a2_f1["item"].isin(orientes)], ["modele", "format", "identite"],
                       "gap_signe_decrit", "gap_signe_reel_w1", "A2_signe_F1"),
            _leaveout(a2_f2[a2_f2["item"].isin(orientes)], ["modele", "format", "identite"],
                       "gap_signe_decrit", "gap_signe_reel_w1", "A2_signe_F2"),
            _leaveout(a4, ["modele", "format", "camp"], "tv_entre_identites", "tv_plancher_w1_w2", "A4"),
            _leaveout(delta, ["modele_f1", "format", "identite"], "delta_gap", "gap_signe_reel_w1", "F2_moins_F1"),
        ])
        stability.append(_stabilite(campagne, cells_f1, cells_floor))
        for passe, fmt, count in PASSES_ANALYSE:
            rows = campagne.traces[(passe, fmt)]
            coverage.append({"modele": campagne.modele, "fournisseur": campagne.fournisseur,
                             "role": campagne.role, "non_deterministe": campagne.non_deterministe,
                             "passe": passe, "format": fmt, "cellules": len(rows),
                             "attendues": count, "rejets": sum(bool(x.get("rejet")) for x in rows),
                             "pilotes_inclus": 0, "operations_reglees_campagne": len(campagne.operations_reglees),
                             "orientation_sha256": orientation_sha, "statut": "EXPLORATOIRE"})
        prepared[campagne.modele] = {"cells_f1": cells_f1, "cells_f2": cells_f2,
                                     "a2_f1": a2_f1, "a2_f2": a2_f2, "a4": a4}
    long = pd.concat(cell_records + item_records, ignore_index=True, sort=False)
    strata = _resumer_strates(long)
    leave = pd.concat(leaveouts, ignore_index=True, sort=False)
    return {
        "r6-analyse-fine-couverture": pd.DataFrame(coverage),
        "r6-analyse-fine-par-item": long,
        "r6-analyse-fine-strates": strata,
        "r6-analyse-fine-intermodeles": _intermodel(prepared),
        "r6-analyse-fine-uniforme": long[long["quantite"] == "s_uniforme"].copy(),
        "r6-analyse-fine-leaveout": leave,
        "r6-analyse-fine-stabilite": pd.concat(stability, ignore_index=True),
        "r6-analyse-fine-portee": pd.DataFrame([
            {"bloc": "H1-H3", "statut": "HORS_DE_CE_SCRIPT", "detail": "r6_evaluer.py seul calcule le confirmatoire"},
            {"bloc": "analyse fine", "statut": "EXPLORATOIRE", "detail": "aucun p, Holm, IC ou verdict"},
        ]),
    }


def ecrire(sortie: Path, tables: dict[str, pd.DataFrame]) -> None:
    sortie.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(sortie / f"{name}.csv", index=False)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifeste", type=Path, required=True)
    parser.add_argument("--sortie", type=Path, required=True)
    args = parser.parse_args(argv)
    campagnes, contexte = charger_campagnes(args.manifeste)
    ecrire(args.sortie, analyser(campagnes, contexte))
    print(json.dumps({"statut": "termine", "reseau": False,
                      "modeles": [c.modele for c in campagnes],
                      "confirmatoire": "hors de ce script"}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
