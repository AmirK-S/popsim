"""R7 : comparaison descriptive de quatre checkpoints publies d'Olmo 3 7B.

Ce pilote execute le plan local R7 sans convertir ni valider de poids et sans toucher a
R6. Il reutilise ``MoteurR1``, son parse et sa trace. Les quatre conditions recoivent les
memes 894 cellules et exactement les memes prompts de completion a trois exemples de R4.

La portee est descriptive : les noms Base, SFT, DPO et Final identifient des checkpoints
publies. Ils ne sont pas traites comme quatre interventions causales ni comme une chaine
d'etapes completement appariee (addendum R7 du 10 septembre 2026).

Deux modes seulement :

  --verifier  controles hors GPU/reseau et ecrit le registre de run ;
  --executer  refait les controles, puis lance un serveur local a la fois.

Le checkpoint final n'a aucun chemin implicite. ``--finale-validee`` et
``--provenance-finale`` sont obligatoires. La provenance doit porter le statut
VALIDATED_TEMPORARY, nommer exactement cette sortie et contenir son SHA-256. Le pilote ne
revalide et ne promeut pas ce fichier : ce perimetre appartient aux scripts de conversion.

Commande preparee apres la conversion finale :

  .venv/bin/python -B analyses/r7_checkpoints.py --verifier \
    --finale-validee /chemin/explicite/Olmo-3-7B-rlvr-Q8_0.partial.gguf \
    --provenance-finale /chemin/explicite/provenance.json

Puis, GPU libre, meme commande avec ``--executer --fin 07:00``.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_oracle_camps as R1
import r4_oracle_socle as R4
from r7_valider_gguf import validate as valider_gguf
from a2_baselines_gss import FAMILLES, charger
from a5_agents_locaux_gss import heure_de_fin, nomenclature, port_libre, premier_port_libre


RACINE = Path(__file__).resolve().parent.parent
TRACES = RACINE / "data/traces"
CACHE = Path.home() / "Library/Caches/popsim-modeles"
GGUF = CACHE / "gguf"
REGISTRE_DEFAUT = TRACES / "r7-registre.json"
JOURNAL = TRACES / "r7-run.log"
REFERENT = TRACES / "r1-distributions-reelles.csv"
REFERENT_SHA256 = R4.REFERENT_SHA
PLAN = RACINE / "resultats/r7-preenregistrement.md"
ADDENDUM = RACINE / "resultats/r7-addendum-reprise-2026-09-10.md"
PLAN_SHA256 = "c7c1fa35ace4c73547b299b13ec9c5ee5c53339cb6a5fb2c7f6c8a0f709933bc"
ADDENDUM_SHA256 = "e373335db2339196426bf37efeb908581355c4b8ed5071601712ba4f5ccaa5eb"
PROVENANCE_POIDS = CACHE / "PROVENANCE-r7.md"
CONVERTER_COMMIT = "c1d0e7a004015f23bc0233470b747b596f29b264"
REVISION_FINALE = "6e5971d9eba42665f5bd5a0fcf047f299ce1dccc"

VERSION_PROMPT = "r7-c3"
SUFFIXE = "r7"
GABARIT = R4.GABARIT
ARRETS = list(R4.ARRETS)
ORDRE = ["olmo3base", "olmo3sft", "olmo3dpo", "olmo3rlvr"]
SONDE = 60
SEUIL_SONDE = 0.50
SEUIL_REJET_CONDITION = 0.25
PRESSION_LIBRE_MIN_PCT = 15.0
N_ITEMS = 149
CELLULES_PAR_CONDITION = 894
CELLULES_TOTALES = 4 * CELLULES_PAR_CONDITION

# Le chemin final est remplace uniquement par l'argument explicite de la ligne de commande.
MODELES_FIXES = {
    "olmo3base": {
        "nom": "Olmo-3-1025-7B", "checkpoint": "Base publie",
        "fichier": str(GGUF / "Olmo-3-7B-base-Q8_0.gguf"),
        "tokenizer_repo": "models--allenai--Olmo-3-1025-7B",
    },
    "olmo3sft": {
        "nom": "Olmo-3-7B-Instruct-SFT", "checkpoint": "SFT publie",
        "fichier": str(GGUF / "Olmo-3-7B-sft-Q8_0.gguf"),
        "tokenizer_repo": "models--allenai--Olmo-3-7B-Instruct-SFT",
    },
    "olmo3dpo": {
        "nom": "Olmo-3-7B-Instruct-DPO", "checkpoint": "DPO publie",
        "fichier": str(GGUF / "Olmo-3-7B-dpo-Q8_0.gguf"),
        "tokenizer_repo": "models--allenai--Olmo-3-7B-Instruct-DPO",
    },
    "olmo3rlvr": {
        "nom": "Olmo-3-7B-Instruct", "checkpoint": "Final publie",
        "fichier": None,
        "tokenizer_repo": "models--allenai--Olmo-3-7B-Instruct",
    },
}


def sha256(path: Path, verifier_inactivite: bool = False) -> str:
    h = hashlib.sha256()
    prochain_controle = 0.0
    with path.open("rb") as stream:
        for bloc in iter(lambda: stream.read(1024 * 1024), b""):
            if verifier_inactivite and time.monotonic() >= prochain_controle:
                exiger_serveur_unique(None)
                prochain_controle = time.monotonic() + 1
            h.update(bloc)
    return h.hexdigest()


def modele_info(finale: Path) -> dict[str, dict]:
    """Registre R1 de R7, sans vocabulaire causal sur les contrastes."""
    sortie = {}
    for cle in ORDRE:
        src = dict(MODELES_FIXES[cle])
        if cle == "olmo3rlvr":
            src["fichier"] = str(finale.resolve())
        src.update({
            "quantification": "Q8_0", "gabarit": GABARIT,
            "coupure_publiee": "aucune", "type": "checkpoint publie",
            "portee": "comparaison descriptive de checkpoints",
        })
        sortie[cle] = src
    return sortie


def lire_provenance_finale(finale: Path, provenance: Path) -> dict:
    """Exige l'attestation de validation produite par la conversion, sans la refaire."""
    try:
        d = json.loads(provenance.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"provenance finale illisible: {exc}") from exc
    attendu = finale.resolve()
    if d.get("status") != "VALIDATED_TEMPORARY":
        raise RuntimeError("provenance finale: statut VALIDATED_TEMPORARY requis")
    if Path(d.get("output", "")).resolve() != attendu:
        raise RuntimeError("provenance finale: output different de --finale-validee")
    if not finale.is_file() or finale.stat().st_size < 1024**3:
        raise RuntimeError("--finale-validee absent ou manifestement incomplet")
    empreinte = d.get("output_sha256")
    if not isinstance(empreinte, str) or re.fullmatch(r"[0-9a-f]{64}", empreinte) is None:
        raise RuntimeError("provenance finale: output_sha256 valide absent")
    if d.get("converter_commit") != CONVERTER_COMMIT or d.get("revision") != REVISION_FINALE:
        raise RuntimeError("provenance finale: revision ou commit convertisseur incorrect")
    validation = d.get("validation", {})
    if validation.get("status") != "PASS" or Path(validation.get("path", "")).resolve() != attendu:
        raise RuntimeError("provenance finale: validation PASS de cette sortie requise")
    if validation.get("bytes") != finale.stat().st_size:
        raise RuntimeError("provenance finale: taille validee differente du fichier")
    return d


def snapshots_tokeniseurs() -> dict[str, Path]:
    """Resout les quatre snapshots deja presents; aucun acces Hugging Face."""
    base = CACHE / "hf-cache/hub"
    resultat = {}
    for cle, info in MODELES_FIXES.items():
        candidats = sorted((base / info["tokenizer_repo"] / "snapshots").glob("*"))
        candidats = [p for p in candidats if (p / "tokenizer.json").is_file()]
        if len(candidats) != 1:
            raise RuntimeError(f"{cle}: un snapshot tokenizer local attendu, trouve {len(candidats)}")
        resultat[cle] = candidats[0]
    return resultat


def prompts_plan(items, table):
    """Les 894 prompts, dans l'ordre exact de R1, construits une seule fois."""
    resultat = []
    for camp, identite, item in R1.cellules(items, R1.CAMPS, R1.IDENTITES):
        sys_txt = R1.systeme(camp, identite)
        usr_txt, _ = R1.utilisateur(item, camp, table, rappel=False)
        resultat.append((item, camp, identite, R4.gabarit(GABARIT, sys_txt, usr_txt)))
    return resultat


def verifier_tokenisation(prompts, snapshots=None) -> dict:
    """Compte vraiment les jetons et publie BOS/EOS; aucune generation ni serveur."""
    try:
        from tokenizers import Tokenizer
    except ImportError as exc:
        raise RuntimeError("paquet local tokenizers absent; utiliser .venv/bin/python") from exc
    snapshots = snapshots or snapshots_tokeniseurs()
    par_modele = {}
    sequences = {}
    for cle in ORDRE:
        dossier = Path(snapshots[cle])
        tok = Tokenizer.from_file(str(dossier / "tokenizer.json"))
        config = json.loads((dossier / "tokenizer_config.json").read_text(encoding="utf-8"))
        bos = config.get("bos_token")
        eos = config.get("eos_token")
        # tokenizers.Tokenizer.encode(add_special_tokens=True) applique exactement les
        # post-processors du tokenizer.json; on conserve aussi le compte brut.
        ids_avec = [tok.encode(p[3], add_special_tokens=True).ids for p in prompts]
        ids_sans = [tok.encode(p[3], add_special_tokens=False).ids for p in prompts]
        avec = [len(ids) for ids in ids_avec]
        sans = [len(ids) for ids in ids_sans]
        sequences[cle] = ids_avec
        manifeste_ids = hashlib.sha256()
        for ids in ids_avec:
            manifeste_ids.update(json.dumps(ids, separators=(",", ":")).encode("ascii") + b"\n")
        par_modele[cle] = {
            "snapshot": str(dossier.resolve()),
            "tokenizer_sha256": sha256(dossier / "tokenizer.json"),
            "bos_token": bos, "bos_id": tok.token_to_id(bos) if isinstance(bos, str) else None,
            "eos_token": eos, "eos_id": tok.token_to_id(eos) if isinstance(eos, str) else None,
            "ajout_special": sorted(set(a - b for a, b in zip(avec, sans))),
            "ids_prompts_sha256": manifeste_ids.hexdigest(),
            "tokens_prompt_min": min(avec), "tokens_prompt_max": max(avec),
            "tokens_prompt_moyenne": round(sum(avec) / len(avec), 3),
        }
    comparaisons = []
    for i, a in enumerate(ORDRE):
        for b in ORDRE[i + 1:]:
            comptes_a = [len(ids) for ids in sequences[a]]
            comptes_b = [len(ids) for ids in sequences[b]]
            ecarts = [abs(x - y) / max(x, y) for x, y in zip(comptes_a, comptes_b)]
            ids_differents = sum(x != y for x, y in zip(sequences[a], sequences[b]))
            comparaisons.append({
                "a": a, "b": b, "ecart_relatif_max": round(max(ecarts), 6),
                "cellules_au_dela_2pct": sum(e > 0.02 for e in ecarts),
                "sequences_ids_differentes": ids_differents,
                "sequences_ids_identiques": ids_differents == 0,
                "appariement_longueur_plan": not any(e > 0.02 for e in ecarts),
                "appariement_tokenisation_strict": not any(e > 0.02 for e in ecarts),
            })
    return {"conditions": par_modele, "comparaisons": comparaisons}


def processus_bloquants(attendu: int | None = None) -> list[dict]:
    lignes = subprocess.check_output(["ps", "-axo", "pid=,comm=,args="], text=True).splitlines()
    trouves = []
    serveur_attendu_vu = False
    for ligne in lignes:
        morceaux = ligne.strip().split(None, 2)
        if len(morceaux) != 3:
            continue
        pid, _, args = morceaux
        pid = int(pid)
        if pid == os.getpid():
            continue
        executable = Path(args.split(None, 1)[0]).name
        raison = None
        if executable == "llama-server":
            if pid == attendu:
                serveur_attendu_vu = True
            else:
                raison = "llama-server"
        elif executable.lower().startswith(("python", "pypy")):
            if any(nom in args for nom in ("r2b_extension.py", "r2_rares_apparie.py")):
                raison = "R2b"
            elif "convert_hf_to_gguf.py" in args:
                raison = "conversion"
            elif "r7_checkpoints.py" in args:
                raison = "autre pilote R7"
        if raison:
            trouves.append({"pid": pid, "raison": raison})
    if attendu is not None and not serveur_attendu_vu:
        trouves.append({"pid": attendu, "raison": "serveur R7 attendu absent"})
    return trouves


def pression_libre_pct() -> float:
    try:
        r = subprocess.run(["memory_pressure", "-Q"], capture_output=True, text=True,
                           timeout=20)
    except (OSError, subprocess.SubprocessError):
        return float("nan")
    m = re.search(r"free percentage:\s*([0-9]+)", r.stdout)
    return float(m.group(1)) if m else float("nan")


def exiger_memoire_disponible() -> float:
    libre = pression_libre_pct()
    if not math.isfinite(libre):
        raise RuntimeError("garde memoire illisible; lancement refuse")
    if libre < PRESSION_LIBRE_MIN_PCT:
        raise RuntimeError(f"memoire libre {libre:.0f}%, sous le seuil {PRESSION_LIBRE_MIN_PCT:.0f}%")
    return libre


def exiger_serveur_unique(attendu: int | None) -> None:
    trouves = processus_bloquants(attendu)
    if trouves:
        raise RuntimeError(f"exclusivite GPU/memoire violee: {trouves}")


class MoteurR7(R1.MoteurR1):
    """Moteur R1 intact, avec controle d'exclusivite avant chaque cellule."""

    def demarrer(self):
        exiger_memoire_disponible()
        super().demarrer()
        exiger_memoire_disponible()
        self._prochain_controle_memoire = time.monotonic() + 60

    def decrire(self, prompt, n_predict, arrets):
        if self.proc is None:
            raise RuntimeError("serveur R7 absent")
        exiger_serveur_unique(self.proc.pid)
        if time.monotonic() >= self._prochain_controle_memoire:
            exiger_memoire_disponible()
            self._prochain_controle_memoire = time.monotonic() + 60
        return super().decrire(prompt, n_predict, arrets)


def chemin_trace(cle: str) -> Path:
    return TRACES / f"r1-{cle}-{SUFFIXE}.jsonl"


def auditer_trace(cle, info, items) -> list[dict]:
    """Reprise stricte: JSON complet, configuration figee, sans doublon ni trou."""
    path = chemin_trace(cle)
    if not path.exists():
        return []
    attendues = list(R1.cellules(items, R1.CAMPS, R1.IDENTITES))
    lignes = []
    for numero, brut in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not brut.strip():
            continue
        try:
            d = json.loads(brut)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"{path}:{numero}: ligne tronquee/invalide; reprise refusee") from exc
        if len(lignes) >= len(attendues):
            raise RuntimeError(f"{path}: plus de {len(attendues)} cellules")
        camp, identite, item = attendues[len(lignes)]
        exige = {
            "version_prompt": VERSION_PROMPT, "cle_modele": cle,
            "modele": info["nom"], "quantification": "Q8_0", "gabarit": GABARIT,
            "item": item, "camp": camp, "identite": identite,
            "sans_relance": True, "n_tentatives": 1,
        }
        mauvais = {k: (d.get(k), v) for k, v in exige.items() if d.get(k) != v}
        if mauvais:
            raise RuntimeError(f"{path}:{numero}: trace incompatible {mauvais}")
        lignes.append(d)
    return lignes


def bilan_sonde(lignes: list[dict]) -> dict | None:
    if len(lignes) < SONDE:
        return None
    premieres = lignes[:SONDE]
    rejets = sum(bool(d.get("rejet")) for d in premieres)
    taux = rejets / SONDE
    return {"cellules": SONDE, "rejets": rejets, "taux_rejet": taux,
            "passe": taux <= SEUIL_SONDE}


def bilan_condition(lignes: list[dict]) -> dict | None:
    if len(lignes) != CELLULES_PAR_CONDITION:
        return None
    rejets = sum(bool(d.get("rejet")) for d in lignes)
    taux = rejets / CELLULES_PAR_CONDITION
    return {"cellules": CELLULES_PAR_CONDITION, "rejets": rejets, "taux_rejet": taux,
            "passe": taux <= SEUIL_REJET_CONDITION}


def ecrire_json_atomique(path: Path, contenu: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporaire = path.with_name(path.name + f".tmp-{os.getpid()}")
    temporaire.write_text(json.dumps(contenu, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(temporaire, path)


def controle_hors_ligne(finale, provenance, items, table, registre_path) -> dict:
    """Tous les controles qui precedent un serveur; hash complet de la finale compris."""
    prov = lire_provenance_finale(finale, provenance)
    if sha256(finale, verifier_inactivite=True) != prov["output_sha256"]:
        raise RuntimeError("provenance finale: SHA-256 du fichier different")
    if sha256(PLAN) != PLAN_SHA256 or sha256(ADDENDUM) != ADDENDUM_SHA256:
        raise RuntimeError("plan R7 ou addendum modifie depuis la revue")
    try:
        provenance_poids = PROVENANCE_POIDS.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"provenance des poids illisible: {exc}") from exc
    if CONVERTER_COMMIT not in provenance_poids or "--outtype q8_0" not in provenance_poids:
        raise RuntimeError("provenance des trois GGUF fixes incompatible avec le plan")
    modeles = modele_info(finale)
    if len(items) != N_ITEMS:
        raise RuntimeError(f"plan R7: {N_ITEMS} items attendus, trouve {len(items)}")
    prompts = prompts_plan(items, table)
    if len(prompts) != CELLULES_PAR_CONDITION or len(ORDRE) * len(prompts) != CELLULES_TOTALES:
        raise RuntimeError("plan R7: attendu 4 * 894 = 3576 cellules")
    if len({hashlib.sha256(p[3].encode()).hexdigest() for p in prompts}) != len(prompts):
        raise RuntimeError("deux cellules produisent un prompt identique")
    manifeste_prompts = hashlib.sha256()
    for item, camp, identite, prompt in prompts:
        manifeste_prompts.update(
            json.dumps([item, camp, identite, prompt], ensure_ascii=False,
                       separators=(",", ":")).encode("utf-8") + b"\n")
    if not REFERENT.is_file() or sha256(REFERENT) != REFERENT_SHA256:
        raise RuntimeError("referent humain R1 absent ou modifie")
    validations = {}
    for cle in ORDRE:
        path = Path(modeles[cle]["fichier"])
        if not path.is_file() or path.stat().st_size < 1024**3:
            raise RuntimeError(f"{cle}: GGUF absent ou manifestement incomplet: {path}")
        validations[cle] = valider_gguf(path)
        if validations[cle].get("status") != "PASS":
            raise RuntimeError(f"{cle}: validation GGUF echouee: {validations[cle].get('error')}")
    tokenisation = verifier_tokenisation(prompts)
    registre = {
        "schema": "popsim-r7-registre-v1", "statut": "CONTROLES_HORS_LIGNE_OK",
        "portee": "comparaison descriptive de checkpoints publies; aucune causalite d'etape",
        "version_prompt": VERSION_PROMPT, "gabarit": GABARIT, "sans_relance": True,
        "arrets": ARRETS, "sonde": {"cellules": SONDE, "seuil_rejet": SEUIL_SONDE},
        "seuil_rejet_condition": SEUIL_REJET_CONDITION,
        "documents_plan": {"plan": str(PLAN), "plan_sha256": PLAN_SHA256,
                           "addendum": str(ADDENDUM), "addendum_sha256": ADDENDUM_SHA256},
        "provenance_poids": {"chemin": str(PROVENANCE_POIDS),
                             "sha256": sha256(PROVENANCE_POIDS),
                             "converter_commit": CONVERTER_COMMIT},
        "plan": {"items": len(items), "camps": list(R1.CAMPS),
                 "identites": list(R1.IDENTITES), "cellules_par_condition": len(prompts),
                 "conditions": len(ORDRE), "cellules_total": CELLULES_TOTALES,
                 "prompts_communs_sha256": manifeste_prompts.hexdigest()},
        "modeles": modeles,
        "finale": {"chemin_explicite": str(finale.resolve()),
                   "provenance": str(provenance.resolve()),
                   "validation_status": prov["validation"]["status"],
                   "output_sha256": prov["output_sha256"]},
        "tokenisation": tokenisation,
        "validation_gguf": validations,
        "conditions": {},
    }
    for cle in ORDRE:
        lignes = auditer_trace(cle, modeles[cle], items)
        registre["conditions"][cle] = {"trace": str(chemin_trace(cle)),
                                        "cellules_tracees": len(lignes),
                                        "sonde": bilan_sonde(lignes),
                                        "bilan": bilan_condition(lignes)}
    ecrire_json_atomique(registre_path, registre)
    return registre


def _fusionner(a, b):
    c = dict(b)
    for champ in ("cellules", "rejets", "relances", "relances_reussies", "secondes"):
        c[champ] = a.get(champ, 0) + b.get(champ, 0)
    c["taux_rejet"] = round(c["rejets"] / c["cellules"], 4) if c["cellules"] else 0.0
    c["arret_demande"] = bool(a.get("arret_demande") or b.get("arret_demande"))
    return c


def executer(registre, items, table, familles, fin_ts, fin_dt, args, registre_path,
             moteur_cls=MoteurR7):
    """Sonde puis reprise sur les memes cellules, avec un unique serveur local."""
    if not isinstance(getattr(args, "depot_plan", None), str) or not args.depot_plan.strip():
        raise RuntimeError("--depot-plan est requis avant toute inference experimentale R7")
    registre["depot_plan_amende"] = args.depot_plan.strip()
    modeles = registre["modeles"]
    R1.VERSION_PROMPT = VERSION_PROMPT
    R1.JOURNAL_RUN = str(JOURNAL)
    resumes = []
    for cle in ORDRE:
        if R1.arret_demande() or time.time() >= fin_ts:
            break
        lignes = auditer_trace(cle, modeles[cle], items)
        sonde = bilan_sonde(lignes)
        if sonde is not None and not sonde["passe"]:
            registre["conditions"][cle].update({"statut": "ARRET_SONDE", "sonde": sonde})
            ecrire_json_atomique(registre_path, registre)
            continue
        if len(lignes) == CELLULES_PAR_CONDITION:
            bilan = bilan_condition(lignes)
            registre["conditions"][cle].update({
                "bilan": bilan,
                "statut": "TERMINE" if bilan["passe"] else "REJET_FORMAT",
            })
            continue
        exiger_serveur_unique(None)
        port = args.port or premier_port_libre()
        if not port_libre(port):
            raise RuntimeError(f"port {port} occupe")
        moteur = moteur_cls(modeles[cle]["fichier"], contexte=4096, parallele=1,
                            port=port, cache_kv_8bits=True)
        erreur = None
        try:
            moteur.demarrer()
            exiger_serveur_unique(moteur.proc.pid)
            total_nouveau = None
            if len(lignes) < SONDE:
                manque = SONDE - len(lignes)
                total_nouveau = R1.lancer(
                    moteur, cle, modeles[cle], items, table, familles, R1.CAMPS,
                    R1.IDENTITES, fin_ts, SUFFIXE, limite=manque,
                    n_predict=R1.N_PREDICT, sans_relance=True)
                lignes = auditer_trace(cle, modeles[cle], items)
                sonde = bilan_sonde(lignes)
                registre["conditions"][cle]["sonde"] = sonde
                if sonde is None or R1.arret_demande() or time.time() >= fin_ts:
                    resumes.append(total_nouveau)
                    continue
                if not sonde["passe"]:
                    registre["conditions"][cle]["statut"] = "ARRET_SONDE"
                    resumes.append(total_nouveau)
                    continue
            reste = R1.lancer(
                moteur, cle, modeles[cle], items, table, familles, R1.CAMPS,
                R1.IDENTITES, fin_ts, SUFFIXE, limite=None,
                n_predict=R1.N_PREDICT, sans_relance=True)
            resumes.append(_fusionner(total_nouveau, reste) if total_nouveau else reste)
        except Exception as exc:
            registre["conditions"][cle]["erreur"] = f"{type(exc).__name__}: {exc}"
            resumes.append({"cle_modele": cle, "echec": str(exc), "cellules": 0})
            erreur = exc
        finally:
            erreur_nettoyage = None
            try:
                moteur.arreter()
                exiger_serveur_unique(None)
            except Exception as exc:
                erreur_nettoyage = exc
            lignes = auditer_trace(cle, modeles[cle], items)
            etat = registre["conditions"][cle]
            etat["cellules_tracees"] = len(lignes)
            etat["sonde"] = bilan_sonde(lignes)
            etat["bilan"] = bilan_condition(lignes)
            if len(lignes) == CELLULES_PAR_CONDITION:
                etat["statut"] = "TERMINE" if etat["bilan"]["passe"] else "REJET_FORMAT"
            elif etat.get("statut") != "ARRET_SONDE":
                etat["statut"] = "INTERROMPU_REPRENABLE"
            ecrire_json_atomique(registre_path, registre)
            if erreur_nettoyage is not None:
                registre["statut"] = "INTERROMPU_REPRENABLE"
                ecrire_json_atomique(registre_path, registre)
                raise RuntimeError(f"{cle}: nettoyage/exclusivite apres serveur en echec") from erreur_nettoyage
        if erreur is not None:
            registre["statut"] = "INTERROMPU_REPRENABLE"
            ecrire_json_atomique(registre_path, registre)
            raise RuntimeError(f"{cle}: echec technique; reprise requise") from erreur
        if R1.arret_demande():
            break
    registre["statut"] = ("TERMINE" if all(registre["conditions"][c].get("statut") in
                                             ("TERMINE", "ARRET_SONDE", "REJET_FORMAT")
                                             for c in ORDRE)
                           else "INTERROMPU_REPRENABLE")
    registre["fin_locale"] = dt.datetime.now().isoformat()
    registre["fin_dure"] = fin_dt.isoformat()
    ecrire_json_atomique(registre_path, registre)
    return resumes


def parser_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--verifier", action="store_true", help="controles seulement, aucun serveur")
    mode.add_argument("--executer", action="store_true", help="controles puis run local")
    ap.add_argument("--finale-validee", required=True, type=Path,
                    help="chemin explicite de la sortie finale validee, jamais devine")
    ap.add_argument("--provenance-finale", required=True, type=Path,
                    help="provenance VALIDATED_TEMPORARY correspondant exactement a la finale")
    ap.add_argument("--registre", type=Path, default=REGISTRE_DEFAUT)
    ap.add_argument("--depot-plan",
                    help="identifiant/URL du depot du plan et de son addendum; requis avec --executer")
    ap.add_argument("--fin", default="07:00", help="fin dure locale du run")
    ap.add_argument("--port", type=int, default=0, help="0 choisit un port libre")
    return ap.parse_args(argv)


def main(argv=None):
    args = parser_args(argv)
    if args.executer and not args.depot_plan:
        raise SystemExit("--depot-plan est requis avec --executer; aucun appel n'a ete fait")
    # Le hash integral du final est une lecture lourde: ne pas meme commencer pendant R2b,
    # un serveur, une conversion ou un autre pilote R7.
    exiger_serveur_unique(None)
    if args.executer:
        exiger_memoire_disponible()
    TRACES.mkdir(parents=True, exist_ok=True)
    table = nomenclature()
    _, items, *_ = charger()
    familles = {it: nom for nom, membres in FAMILLES.items() for it in membres}
    # Importer R4 installe le gabarit trois exemples dans R1; R7 fixe ensuite sa version.
    R1.VERSION_PROMPT = VERSION_PROMPT
    registre = controle_hors_ligne(args.finale_validee, args.provenance_finale,
                                   items, table, args.registre)
    print(json.dumps({"registre": str(args.registre.resolve()), "statut": registre["statut"],
                      "plan": registre["plan"],
                      "tokenisation": registre["tokenisation"]}, ensure_ascii=False, indent=2))
    if args.verifier:
        return 0
    fin_ts, fin_dt = heure_de_fin(args.fin)
    executer(registre, items, table, familles, fin_ts, fin_dt, args, args.registre)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
