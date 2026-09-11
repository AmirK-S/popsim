"""Runner hors réseau vérifiable puis exécutable d'une campagne R6 mono-modèle.

Le fichier QUEUE_PREPARED livré avec ce runner est volontairement non exécutable. Une
revue doit produire un manifeste QUEUE_READY distinct et un GO one-shot propre au modèle.
Le runner ne crée aucun GO et ne retire aucun marqueur d'arrêt. À toute interruption d'une
campagne (indicateurs du résultat ou exception pendant les étapes, Ctrl-C compris), il crée
STOP-R6 s'il est absent, avec un motif horodaté, sans jamais écraser un STOP existant.

Amendement 429 : `--amendement-429 <chemin>` et `--amendement-429-sha256 <sha>` vont
ensemble. Seul le document AMENDEMENT_429_CHEMIN, d'empreinte AMENDEMENT_429_SHA256 scellée
dans ce fichier, peut l'activer ; tant que cette empreinte vaut None, l'activation est
refusée. Tout refus précède le réseau. Actif, la transaction rapproche un 429 ambigu par
deux sondes en lecture seule ; sans ces arguments, rien ne change.
"""

import argparse
from contextlib import ExitStack
import datetime
import fcntl
import hashlib
import json
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r6_oracle_distant as R6


ORDRE_MODELES = ["deepseek/deepseek-v4-flash", "mistralai/mistral-small-2603",
                 "qwen/qwen3.7-plus", "z-ai/glm-5",
                 "anthropic/claude-haiku-4.5", "x-ai/grok-4.3"]
ROLES = {model: ("confirmatoire" if model in {
    "anthropic/claude-haiku-4.5", "x-ai/grok-4.3"} else "descriptif")
    for model in ORDRE_MODELES}
NON_DETERMINISTES = {"deepseek/deepseek-v4-flash", "x-ai/grok-4.3"}
EXCLUS = {"moonshotai/kimi-k2.5", "google/gemini-3.8-flash",
          "meta-llama/llama-4-maverick", "openai/gpt-5.6-luna",
          "openai/gpt-5.4", "anthropic/claude-sonnet-5"}
ETAPES = (("f1", "campagne", "q4", 894),
          ("f2", "campagne", "q4gab3", 316),
          ("plancher", "plancher", "q4", 40))
# Amendement 429 : seul ce document, scelle par son empreinte, peut l'activer. L'empreinte
# vaut None tant que le document n'est pas finalise : l'activation est alors refusee.
# v2 (ancre stable par run, critere par variation des couts regles, persistance
# systematique de la preuve, delai avant la sonde 1 corrigeant le defaut bloquant de la
# revue adverse du 2026-09-11) remplace le point 3 de la v1 ; v1 reste figee, SHA deja
# consigne dans resultats/r6-preuve-activation-amendement-429-2026-09-11.md, jamais
# reutilisee pour signer v2. v2 activee le 2026-09-11, SHA consigne dans
# resultats/r6-preuve-activation-amendement-429-v2-2026-09-11.md.
AMENDEMENT_429_CHEMIN = os.path.join(R6.RACINE, "resultats",
                                     "r6-amendement-429-v2-2026-09-11.md")
AMENDEMENT_429_SHA256 = "c522950ad25362cd2dfde188ab1faab35ed03e71d68245311822c951b5067d9a"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def charger_file(path, empreinte):
    if not empreinte or sha256(path) != empreinte:
        raise ValueError("empreinte QUEUE_PREPARED/READY différente")
    with open(path, encoding="utf-8") as handle:
        queue = json.load(handle)
    if queue.get("version") != "R6-campaign-queue-1":
        raise ValueError("version de file inconnue")
    parent = queue.get("parent_ready", {})
    if sha256(parent.get("path", "")) != parent.get("sha256"):
        raise ValueError("manifeste READY parent absent ou modifié")
    lignes = queue.get("models")
    if not isinstance(lignes, list) or [x.get("model") for x in lignes] != ORDRE_MODELES:
        raise ValueError("ordre ou périmètre de la file différent")
    if set(queue.get("excluded_models", [])) != EXCLUS:
        raise ValueError("exclusions de la file différentes")
    if R6.dollars(queue.get("global_cap_usd")) != Decimal("4.40"):
        raise ValueError("plafond global différent")
    if R6.dollars(queue.get("account_reserve_usd")) != Decimal("1.50"):
        raise ValueError("réserve compte différente")
    if [x.get("priority") for x in lignes] != list(range(1, 7)):
        raise ValueError("priorités de la file différentes")
    if sum((R6.dollars(x.get("model_cap_usd")) for x in lignes), Decimal("0")) > Decimal("4.40"):
        raise ValueError("somme des plafonds modèles hors plafond global")
    return queue


def politique_modele(queue, model):
    if model in EXCLUS:
        raise ValueError("modèle exclu de la file")
    rows = [x for x in queue["models"] if x.get("model") == model]
    if len(rows) != 1:
        raise ValueError("modèle absent ou dupliqué")
    p = rows[0]
    if p.get("analysis_role") != ROLES[model]:
        raise ValueError("rôle analytique différent")
    non_deterministe = model in NON_DETERMINISTES
    if (p.get("non_deterministe") is not non_deterministe
            or p.get("A4_requires_machine_floor") is not non_deterministe):
        raise ValueError("marqueur non-déterministe/A4 différent")
    if not p.get("provider_fixed") or p.get("reasoning") != "off":
        raise ValueError("fournisseur ou raisonnement non figé")
    if any(R6.dollars(p.get("max_price", {}).get(k)) <= 0
           for k in ("prompt", "completion")):
        raise ValueError("prix maximal absent ou nul")
    if p.get("max_tokens") != 150 or R6.dollars(p.get("call_cap_usd")) <= 0:
        raise ValueError("bornes d'appel invalides")
    if R6.dollars(p.get("model_cap_usd")) > Decimal("4.40"):
        raise ValueError("plafond modèle hors plafond global")
    steps = p.get("steps", [])
    if [(x.get("name"), x.get("pass"), x.get("format"), x.get("cells"))
            for x in steps] != list(ETAPES):
        raise ValueError("F1/F2/plancher différents du plan")
    if [x.get("max_prompt_tokens") for x in steps] != [600, 1000, 600]:
        raise ValueError("bornes de prompt différentes")
    floor = steps[2]
    if (not floor.get("cell_list")
            or sha256(floor["cell_list"]) != floor.get("cell_list_sha256")):
        raise ValueError("liste du plancher absente ou modifiée")
    caps = sum((R6.dollars(x.get("trace_cap_usd")) for x in steps), Decimal("0"))
    if caps + R6.dollars(p.get("settled_pilot_usd")) > R6.dollars(p["model_cap_usd"]):
        raise ValueError("plafonds de traces et pilote dépassent le plafond modèle")
    return p


def verifier_go(path, model, queue_sha):
    with open(path, encoding="utf-8") as handle:
        go = json.load(handle)
    attendu = {"state": "GO", "scope": "R6-campaign-one-model", "model": model,
               "queue_manifest_sha256": queue_sha, "one_shot": True,
               "socrates_reviewed": True}
    if any(go.get(k) != v for k, v in attendu.items()):
        raise ValueError("GO campagne one-shot absent, différent ou hors modèle")
    return go


def cellules_production(step, table):
    if step["name"] == "plancher":
        return R6.lire_liste(step["cell_list"])
    from a2_baselines_gss import charger
    _ids, items, _y1, _y2, _x, _attrs = charger()
    selected, camps, identities, fmt = R6.plan_cellules(step["name"], list(items))
    if fmt != step["format"]:
        raise ValueError("format du plan différent")
    return list(R6.R1.cellules(selected, camps, identities))


def cellules_rapprochees_429(evenements, model, fmt, passe):
    """Cellules (camp, identité, item) portant une annulation automatique 429-non-facture."""
    cellules = set()
    for e in evenements or []:
        if (e.get("type") != "annulation"
                or not str(e.get("preuve", "")).startswith(R6.PREUVE_NON_FACTURE_429)):
            continue
        x = json.loads(e["identite"])
        if (x[0], x[1], x[2], x[-1]) == (model, fmt, R6.FORMATS[fmt], passe):
            cellules.add((x[4], x[5], x[3]))
    return cellules


def sequence_conforme(observees, attendues, deplacables=frozenset()):
    """Même ensemble ; ordre strict pour toute cellule non rapprochée.

    Une cellule rapprochée (annulation 429-non-facture au registre) peut seulement être
    retardée : en fin de bloc après remise en file, ou plus loin encore après un STOP entre
    le rapprochement et le rejeu. Elle ne peut jamais précéder une cellule non rapprochée
    qui la précède dans le plan.
    """
    observees, attendues = [tuple(c) for c in observees], [tuple(c) for c in attendues]
    if (len(observees) != len(attendues) or len(set(observees)) != len(observees)
            or set(observees) != set(attendues)):
        return False
    deplacables = set(deplacables) & set(attendues)
    if ([c for c in observees if c not in deplacables]
            != [c for c in attendues if c not in deplacables]):
        return False
    rang = {c: i for i, c in enumerate(observees)}
    dernier_fixe = -1
    for c in attendues:
        if c in deplacables:
            if rang[c] < dernier_fixe:
                return False
        else:
            dernier_fixe = rang[c]
    return True


def verifier_trace(model, provider, step, trace_key, expected_cells, deplacables=frozenset()):
    rows = R6.lignes_existantes(R6.chemin_trace(trace_key))
    if len(rows) != len(expected_cells):
        raise ValueError("trace de campagne incomplète; GO conservé pour reprise exacte")
    if len({(x["version_prompt"], x["format"], x["modele"], x["item"],
             x["camp"], x["identite"]) for x in rows}) != len(expected_cells):
        raise ValueError("identités de trace dupliquées")
    if not sequence_conforme([(x.get("camp"), x.get("identite"), x.get("item")) for x in rows],
                             expected_cells, deplacables):
        raise ValueError("séquence camp/identité/item différente du plan")
    for row in rows:
        if (row.get("modele") != model or row.get("fournisseur_impose") != provider
                or row.get("format") != step["format"]
                or row.get("raisonnement") != "off"
                or row.get("configuration", {}).get("max_tokens") != 150):
            raise ValueError("identité ou configuration de trace différente")
    return rows


def verifier_operations_modele(reg, policy, cellules_par_etape=None):
    """Compare les opérations réglées aux 894 + 316 + 40 cellules dans leur ordre."""
    operations = [op for op in reg.operations_modele(policy["model"])
                  if json.loads(op["identite"])[-1] in ("campagne", "plancher")]
    if len(operations) != 1250 or any(op.get("etat") != "reglee" for op in operations):
        raise ValueError("opérations de campagne absentes, non réglées ou en surnombre")
    offset = 0
    for step in policy["steps"]:
        cells = ((cellules_par_etape or {}).get(step["name"])
                 if cellules_par_etape is not None else cellules_production(step, None))
        if cells is None or len(cells) != step["cells"]:
            raise ValueError("plan attendu indisponible ou incomplet")
        block = operations[offset:offset + len(cells)]
        decoded = [json.loads(op["identite"]) for op in block]
        if any((x[0], x[1], x[2], x[-1]) !=
               (policy["model"], step["format"], R6.FORMATS[step["format"]], step["pass"])
               for x in decoded):
            raise ValueError("répartition campagne/q4, campagne/q4gab3, plancher/q4 différente")
        deplacables = cellules_rapprochees_429(getattr(reg, "evenements", []),
                                               policy["model"], step["format"], step["pass"])
        if not sequence_conforme([(x[4], x[5], x[3]) for x in decoded], list(cells),
                                 deplacables):
            raise ValueError("séquence camp/identité/item du registre différente du plan")
        offset += len(cells)


def verifier_predecesseurs(reg, queue, policy, cellules_par_modele=None):
    """Impose l'ordre de file avec contenu, répartition et état exacts."""
    for previous in queue["models"]:
        if previous["priority"] >= policy["priority"]:
            break
        try:
            verifier_operations_modele(reg, previous,
                (cellules_par_modele or {}).get(previous["model"])
                if cellules_par_modele is not None else None)
        except ValueError as exc:
            raise ValueError(f"modèle précédent de la file invalide: {exc}") from None


def ecrire_rapport(path, policy, queue_sha, traces, complete):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    lines = ["# R6 — rapport agrégé de campagne", "",
             f"- Modèle: `{policy['model']}`", f"- Fournisseur figé: `{policy['provider_fixed']}`",
             f"- Rôle: **{policy['analysis_role']}**", f"- Manifeste de file: `{queue_sha}`",
             f"- Non déterministe: **{str(policy['non_deterministe']).lower()}**",
             f"- Plancher machine A4 requis: **{str(policy['A4_requires_machine_floor']).lower()}**",
             f"- État: **{'terminé' if complete else 'interrompu; reprise exacte requise'}**", ""]
    total_cost = Decimal("0")
    for name, rows in traces.items():
        cost = sum((R6.dollars(x.get("cout_annonce_usd")) for x in rows), Decimal("0"))
        total_cost += cost
        rejects = sum(bool(x.get("rejet")) for x in rows)
        incidents = sum(len(x.get("incidents_transport", [])) for x in rows)
        rapproches = sum(bool(x.get("rapprochement_429")) for x in rows)
        suffixe_429 = (f", {rapproches} 429 ambigus rapprochés non facturés puis rejoués"
                       if rapproches else "")
        lines.append(f"- {name}: {len(rows)} réponses, {rejects} rejets de parse, "
                     f"{incidents} incidents de transport{suffixe_429}, {cost} USD annoncés.")
    lines += ["", f"Coût campagne annoncé cumulé: **{total_cost} USD**. "
              "Aucun contenu brut, identifiant d'appel ou secret n'est publié.", ""]
    if policy["analysis_role"] == "descriptif":
        lines.append("Ce modèle reste descriptif; ses résultats ne deviennent pas confirmatoires.")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def ecrire_recu_terminal(path, policy, queue_sha, ledger, go_consomme, traces):
    """Scelle les seules métadonnées nécessaires à l'analyse après campagne complète."""
    if len(traces) != 3:
        raise ValueError("reçu terminal exige exactement trois traces")
    record = {
        "version": "R6-campaign-terminal-receipt-1", "statut": "TERMINE",
        "modele": policy["model"], "fournisseur": policy["provider_fixed"],
        "analysis_role": policy["analysis_role"],
        "non_deterministe": policy["non_deterministe"],
        "queue_manifest_sha256": queue_sha,
        "ledger": {"path": os.path.abspath(ledger), "sha256": sha256(ledger)},
        "go_consomme": os.path.abspath(go_consomme),
        "floor_cells": {"path": os.path.abspath(policy["steps"][2]["cell_list"]),
                        "sha256": policy["steps"][2]["cell_list_sha256"]},
        "traces": traces,
    }
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    temporary = path + ".tmp"
    with open(temporary, "w", encoding="utf-8") as handle:
        json.dump(record, handle, ensure_ascii=False, sort_keys=True, allow_nan=False, indent=2)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)


def verifier_amendement_429(chemin, empreinte):
    """Rend True si l'amendement 429 est actif ; refuse une paire incomplète ou fausse."""
    if chemin is None and empreinte is None:
        return False
    if chemin is None or empreinte is None:
        raise ValueError("--amendement-429 et --amendement-429-sha256 vont ensemble")
    if AMENDEMENT_429_SHA256 is None:
        raise ValueError("amendement 429 non scellé dans le code; activation refusée")
    if os.path.realpath(chemin) != os.path.realpath(AMENDEMENT_429_CHEMIN):
        raise ValueError("chemin de l'amendement 429 différent du chemin attendu")
    if empreinte != AMENDEMENT_429_SHA256:
        raise ValueError("empreinte de l'amendement 429 différente de l'empreinte scellée")
    if not os.path.isfile(chemin):
        raise ValueError("amendement 429 absent")
    if sha256(chemin) != empreinte:
        raise ValueError("empreinte de l'amendement 429 différente du fichier")
    return True


def raisons_interruption(result):
    noms = (("reconciliation_requise", "reconciliation_requise"),
            ("non_jouees", "non_jouees"), ("arret_seuil_429", "seuil 429"),
            ("plafond_atteint", "plafond"), ("arret_demande", "arrêt demandé"))
    return [libelle for cle, libelle in noms if result.get(cle)]


def creer_stop_interruption(model, raisons):
    """Crée STOP-R6 s'il est absent ; un STOP existant n'est jamais écrasé."""
    chemin = R6.FICHIER_ARRET_R6
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    motif = (f"{datetime.datetime.now().astimezone().isoformat(timespec='seconds')} "
             f"r6_runner_campagnes: campagne interrompue; modele={model}; "
             f"raison={', '.join(raisons) or 'inconnue'}\n")
    try:
        fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        return False
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(motif)
        fh.flush()
        os.fsync(fh.fileno())
    return True


def executer(queue_path, queue_sha, model, go_path=None, verifier=False, registre=None,
             import_path=None, client_base=None, cle=None, snapshot_cle=None,
             snapshot_solde=None, table=None, cellules_override=None, rapport_path=None,
             recu_path=None, amendement_429=None, amendement_429_sha256=None):
    amendement_actif = verifier_amendement_429(amendement_429, amendement_429_sha256)
    queue = charger_file(queue_path, queue_sha)
    p = politique_modele(queue, model)
    diagnostic = {"mode": "verification-hors-reseau", "state": queue.get("state"),
                  "executable": False, "model": model,
                  "analysis_role": p["analysis_role"], "provider": p["provider_fixed"],
                  "non_deterministe": p["non_deterministe"],
                  "A4_requires_machine_floor": p["A4_requires_machine_floor"],
                  "queue_manifest_sha256": queue_sha,
                  "amendement_429_actif": amendement_actif}
    if amendement_actif:
        diagnostic["amendement_429"] = {"path": os.path.abspath(amendement_429),
                                        "sha256": amendement_429_sha256}
    if verifier:
        return diagnostic
    if queue.get("state") != "QUEUE_READY" or queue.get("executable") is not True:
        raise ValueError("file QUEUE_PREPARED non exécutable; revue Socrates requise")
    if R6.arret_demande():
        raise ValueError("STOP présent; aucune campagne")
    if not go_path or not os.path.exists(go_path):
        raise ValueError("GO campagne one-shot modèle absent")
    registre = registre or queue["ledger_path"]
    import_path = import_path or queue["import_manifest_path"]
    inventory, _events = R6.charger_import(import_path)
    with ExitStack() as stack:
        queue_lock = stack.enter_context(open(queue_path + ".run.lock", "a"))
        fcntl.flock(queue_lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        lock = stack.enter_context(open(go_path + ".lock", "a"))
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        verifier_go(go_path, model, queue_sha)
        if R6.arret_demande():
            raise ValueError("STOP présent; aucune campagne")
        with R6.RegistreGlobal(registre) as reg:
            reg.verifier_integrite(inventory)
            if (len(reg.operations_pilote(model)) != 20
                    or reg.total_pilote(model) != R6.dollars(p["settled_pilot_usd"])):
                raise ValueError("pilote réglé différent du manifeste de file")
            verifier_predecesseurs(reg, queue, p)
        table = table or R6.nomenclature()
        api_key = cle if cle is not None else R6.cle_api()
        client = R6.ClientChat(api_key, base=client_base or R6.BASE, raisonnement="off",
                               fournisseur=p["provider_fixed"], max_price=p["max_price"])
        traces = {}
        traces_terminales = []
        report = rapport_path or os.path.join(R6.SORTIE, "r6-campagne-" +
            model.replace("/", "-").replace(":", "-") + "-rapport.md")
        try:
            for step in p["steps"]:
                if R6.arret_demande():
                    raise ValueError("STOP présent entre les étapes; GO conservé")
                cells = ((cellules_override or {}).get(step["name"])
                         if cellules_override is not None else cellules_production(step, table))
                if cells is None:
                    raise ValueError("cellules d'étape absentes")
                expected_count = len(cells) if cellules_override is not None else step["cells"]
                if len(cells) != expected_count:
                    raise ValueError("comptage de cellules différent")
                suffix = ("r6v2-plancher" if step["name"] == "plancher"
                          else "r6v2-campagne-" + step["name"])
                trace_key = R6.cle_run(model, step["format"], suffix)
                transaction = R6.TransactionPayante(
                    registre, inventory, step["pass"], p["call_cap_usd"],
                    step["max_prompt_tokens"], snapshot_cle or R6.statut_cle,
                    snapshot_solde or R6.solde, plafond_modele=p["model_cap_usd"],
                    fichier_go=go_path, rapprochement_429=amendement_actif)
                budget = R6.Budget(step["trace_cap_usd"],
                                   float(R6.dollars(p["max_price"]["prompt"])) / 1_000_000,
                                   float(R6.dollars(p["max_price"]["completion"])) / 1_000_000,
                                   R6.JETONS_ESTIMES[step["format"]])
                result = R6.lancer(client, model, step["format"], table, cells, budget,
                                   trace_key, n_predict=150, transaction=transaction,
                                   manifeste_import=import_path)
                if (result.get("reconciliation_requise") or result.get("arret_demande")
                        or result.get("arret_seuil_429") or result.get("non_jouees")
                        or result.get("plafond_atteint")):
                    # STOP posé AVANT le rapport : un échec d'écriture ne peut pas l'omettre.
                    creer_stop_interruption(model, raisons_interruption(result))
                    traces[step["name"]] = R6.lignes_existantes(R6.chemin_trace(trace_key))
                    ecrire_rapport(report, p, queue_sha, traces, False)
                    raise ValueError("campagne interrompue; GO conservé pour reprise exacte")
                with R6.RegistreGlobal(registre) as reg:
                    deplacables = cellules_rapprochees_429(reg.evenements, model,
                                                           step["format"], step["pass"])
                traces[step["name"]] = verifier_trace(model, p["provider_fixed"], step,
                                                        trace_key, list(cells), deplacables)
                traces_terminales.append({
                    "passe": step["pass"], "format": step["format"], "cellules": len(cells),
                    "path": os.path.abspath(R6.chemin_trace(trace_key)),
                    "sha256": sha256(R6.chemin_trace(trace_key)),
                    "configuration": traces[step["name"]][0]["configuration"],
                })
        except BaseException as exc:
            # Toute sortie anormale pendant les étapes (fournisseur différent, OSError sur
            # /credits, ErreurPreflight, Ctrl-C pendant l'attente des sondes...) pose STOP-R6
            # sans jamais écraser un STOP existant, puis relance l'exception d'origine.
            try:
                creer_stop_interruption(model, [f"exception {type(exc).__name__}"])
            except Exception as stop_exc:
                print(f"STOP-R6 non posé: {type(stop_exc).__name__}", file=sys.stderr)
            raise
        consumed = go_path + ".consomme"
        if os.path.exists(consumed):
            raise ValueError("archive GO déjà présente")
        os.replace(go_path, consumed)
        ecrire_rapport(report, p, queue_sha, traces, True)
        receipt = recu_path or os.path.join(R6.SORTIE, "r6-campagne-" +
            model.replace("/", "-").replace(":", "-") + "-recu-terminal.json")
        ecrire_recu_terminal(receipt, p, queue_sha, registre, consumed, traces_terminales)
        return dict(diagnostic, mode="campagne", executable=True, completed=True,
                    go_consumed_to=consumed, report=report,
                    receipt=receipt, traces={k: len(v) for k, v in traces.items()})


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True)
    parser.add_argument("--file-sha256", required=True)
    parser.add_argument("--modele", required=True)
    parser.add_argument("--go")
    parser.add_argument("--verifier", action="store_true")
    parser.add_argument("--amendement-429")
    parser.add_argument("--amendement-429-sha256")
    args = parser.parse_args(argv)
    print(json.dumps(executer(args.file, args.file_sha256, args.modele, args.go,
                              args.verifier, amendement_429=args.amendement_429,
                              amendement_429_sha256=args.amendement_429_sha256),
                     ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
