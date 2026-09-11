"""Tests hors ligne de la file de campagnes R6 avec serveur HTTP factice local."""

import hashlib
import json
import os
import shutil
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analyses"))
import r6_oracle_distant as R6
import r6_runner_campagnes as RUN


# Oracle du test écrit explicitement: il ne réutilise ni ordre, ni rôles du runner.
EXPECTED_ORDER = ["deepseek/deepseek-v4-flash", "mistralai/mistral-small-2603",
                  "qwen/qwen3.7-plus", "z-ai/glm-5",
                  "anthropic/claude-haiku-4.5", "x-ai/grok-4.3"]
EXPECTED_ROLES = ["descriptif", "descriptif", "descriptif", "descriptif",
                  "confirmatoire", "confirmatoire"]


class Scenario:
    requests = []
    stop_after = None
    stop_path = None


class FakeServer(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_POST(self):
        size = int(self.headers.get("Content-Length", "0"))
        payload = json.loads(self.rfile.read(size))
        Scenario.requests.append(payload)
        if Scenario.stop_after == len(Scenario.requests):
            open(Scenario.stop_path, "w").close()
        provider = payload["provider"]["order"][0]
        body = json.dumps({
            "id": f"fake-{len(Scenario.requests)}", "model": payload["model"],
            "provider": provider,
            "choices": [{"message": {"content": "A: 60\nB: 40"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 10,
                      "completion_tokens_details": {"reasoning_tokens": 0},
                      "cost": 0.0001},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def write_json(path, value):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(value, fh, ensure_ascii=False, indent=2)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def expect_error(label, fn, fragment):
    try:
        fn()
    except (ValueError, BlockingIOError) as exc:
        assert fragment in str(exc), (label, str(exc))
    else:
        raise AssertionError(label + " non refusé")


tmp = tempfile.mkdtemp(prefix="r6-campaign-runner-")
server = HTTPServer(("127.0.0.1", 0), FakeServer)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_address[1]}/api/v1"

try:
    R6.TRACES = os.path.join(tmp, "traces")
    R6.SORTIE = os.path.join(tmp, "results")
    os.makedirs(os.path.join(R6.TRACES, "reprise"))
    R6.JOURNAL = os.path.join(R6.TRACES, "run.log")
    R6.FICHIER_ARRET_GLOBAL = os.path.join(R6.TRACES, "STOP")
    R6.FICHIER_ARRET_R6 = os.path.join(R6.TRACES, "STOP-R6")
    R6.verifier_referent = lambda: None
    Scenario.stop_path = R6.FICHIER_ARRET_R6

    old = os.path.join(tmp, "old.jsonl")
    open(old, "w").close()
    imported = os.path.join(tmp, "import.json")
    write_json(imported, {
        "version": "R6-v2-import-1", "exhaustif": True,
        "attendus": {"lignes": 0, "reponses": 0, "incidents": 0,
                    "cout_annonce_reponses_usd": "0", "borne_incidents_total_usd": "0"},
        "cout_incidents": {"observation": "inconnu", "borne_unitaire_usd": "0",
                           "fondement_borne": "fixture"},
        "traces": [{"chemin": old, "passe": "ancien-pilote", "classe": "ancien-pilote",
                    "sha256": sha(old),
                    "attendus": {"lignes": 0, "reponses": 0, "incidents": 0}}],
    })
    inventory, _ = R6.charger_import(imported)
    ledger = os.path.join(tmp, "ledger.jsonl")
    with R6.RegistreGlobal(ledger) as reg:
        reg.initialiser_evenements(inventory, [])

    parent = os.path.join(tmp, "parent.json")
    write_json(parent, {"state": "READY"})
    floor = os.path.join(tmp, "floor.txt")
    with open(floor, "w") as fh:
        for i in range(40):
            fh.write(f"floor_{i}\tgauche\tjournaliste\n")
    model_rows = []
    for priority, (model, role) in enumerate(zip(EXPECTED_ORDER, EXPECTED_ROLES), 1):
            nondeterministic = model in {"deepseek/deepseek-v4-flash", "x-ai/grok-4.3"}
            model_rows.append({
                "phase": role, "priority": priority, "model": model,
                "analysis_role": role, "provider_fixed": "FakeProvider",
                "non_deterministe": nondeterministic,
                "A4_requires_machine_floor": nondeterministic,
                "reasoning": "off", "max_tokens": 150,
                "max_price": {"prompt": "0.1", "completion": "0.2"},
                "call_cap_usd": "0.001", "model_cap_usd": "0.50",
                "settled_pilot_usd": "0",
                "steps": [
                    {"name": "f1", "pass": "campagne", "format": "q4", "cells": 894,
                     "max_prompt_tokens": 600, "trace_cap_usd": "0.30"},
                    {"name": "f2", "pass": "campagne", "format": "q4gab3", "cells": 316,
                     "max_prompt_tokens": 1000, "trace_cap_usd": "0.15"},
                    {"name": "plancher", "pass": "plancher", "format": "q4", "cells": 40,
                     "max_prompt_tokens": 600, "trace_cap_usd": "0.05",
                     "cell_list": floor, "cell_list_sha256": sha(floor)},
                ],
            })
    queue_path = os.path.join(tmp, "queue.json")

    def make_queue(state="QUEUE_PREPARED", executable=False):
        write_json(queue_path, {
            "version": "R6-campaign-queue-1", "state": state, "executable": executable,
            "parent_ready": {"path": parent, "sha256": sha(parent)},
            "global_cap_usd": "4.40", "account_reserve_usd": "1.50",
            "ledger_path": ledger, "import_manifest_path": imported,
            "models": model_rows, "excluded_models": sorted(RUN.EXCLUS),
        })
        return sha(queue_path)

    model = EXPECTED_ORDER[0]
    prepared_sha = make_queue()
    before = len(Scenario.requests)
    expect_error("QUEUE_PREPARED", lambda: RUN.executer(
        queue_path, prepared_sha, model), "non exécutable")
    assert len(Scenario.requests) == before
    expect_error("excluded", lambda: RUN.politique_modele(
        RUN.charger_file(queue_path, prepared_sha), "moonshotai/kimi-k2.5"), "exclu")
    altered_rows = list(model_rows)
    altered_rows[0], altered_rows[1] = altered_rows[1], altered_rows[0]
    original_rows = model_rows
    model_rows = altered_rows
    altered_sha = make_queue()
    expect_error("ordre explicite", lambda: RUN.charger_file(queue_path, altered_sha),
                 "ordre")
    model_rows = original_rows

    # Vingt cellules pilote réglées à coût annoncé nul: le plafond campagne les inclut.
    with R6.RegistreGlobal(ledger) as reg:
        for i in range(20):
            pilot_pass = "essai-1" if i < 10 else "essai-2"
            identity = R6.identite_campagne(model, "q4", R6.FORMATS["q4"],
                                             f"pilot_{i % 10}", "gauche",
                                             "journaliste", pilot_pass)
            reg.reserver(identity, "0.001", "10", plafond_modele_usd="0.50",
                         empreinte_requete=str(i).zfill(64),
                         fournisseur_impose="FakeProvider",
                         plafond_pilote_usd="0.02", appels_pilote_max=20,
                         borne_pilote_max_usd="0.001")
            reg.reconcilier(identity, "0", f"pilot-{i}")

    ready_sha = make_queue("QUEUE_READY", True)
    loaded_ready = RUN.charger_file(queue_path, ready_sha)

    # Oracle indépendant des constantes du runner pour les 894 + 316 + 40 identités.
    from a2_baselines_gss import charger
    import pandas as pd
    _ids, all_items, _y1, _y2, _x, _attrs = charger()
    orientation = pd.read_csv(os.path.join(ROOT, "resultats", "a37-orientation-items.csv"))
    oriented = {str(item) for item, yes in zip(orientation["item"],
                                               orientation["oriente"].astype(bool)) if yes}
    f1_cells = list(R6.R1.cellules(list(all_items), ["gauche", "centre", "droite"],
                                   ["journaliste", "adversaire"]))
    f2_cells = list(R6.R1.cellules([x for x in all_items if x in oriented],
                                   ["gauche", "droite"],
                                   ["journaliste", "adversaire"]))
    oracle_steps = [
        ("campagne", "q4", f1_cells),
        ("campagne", "q4gab3", f2_cells),
        ("plancher", "q4", R6.lire_liste(floor)),
    ]
    assert [len(x[2]) for x in oracle_steps] == [894, 316, 40]

    def settled_operations(target_model):
        answer = []
        for pass_name, fmt, cells in oracle_steps:
            for camp, identity, item in cells:
                answer.append({"etat": "reglee", "identite": R6.identite_campagne(
                    target_model, fmt, R6.FORMATS[fmt], item, camp, identity, pass_name)})
        return answer

    class FakeRegistry:
        def __init__(self, operations):
            self.operations = operations

        def operations_modele(self, _model):
            return self.operations

    target_policy = RUN.politique_modele(loaded_ready, EXPECTED_ORDER[1])
    valid_ops = settled_operations(EXPECTED_ORDER[0])
    oracle_by_model = {EXPECTED_ORDER[0]: {
        "f1": oracle_steps[0][2], "f2": oracle_steps[1][2],
        "plancher": oracle_steps[2][2]}}
    RUN.verifier_predecesseurs(FakeRegistry(valid_ops), loaded_ready, target_policy,
                               oracle_by_model)
    swapped = list(valid_ops)
    swapped[0], swapped[1] = swapped[1], swapped[0]
    expect_error("séquence permutée", lambda: RUN.verifier_predecesseurs(
        FakeRegistry(swapped), loaded_ready, target_policy, oracle_by_model), "séquence")
    unsettled = [dict(x) for x in valid_ops]
    unsettled[17]["etat"] = "reservation"
    expect_error("non réglée", lambda: RUN.verifier_predecesseurs(
        FakeRegistry(unsettled), loaded_ready, target_policy, oracle_by_model), "non réglées")
    wrong_partition = [dict(x) for x in valid_ops]
    fields = json.loads(wrong_partition[894]["identite"])
    fields[-1] = "plancher"
    wrong_partition[894]["identite"] = json.dumps(fields, separators=(",", ":"))
    expect_error("répartition", lambda: RUN.verifier_predecesseurs(
        FakeRegistry(wrong_partition), loaded_ready, target_policy, oracle_by_model),
        "répartition")
    go = os.path.join(tmp, "GO.json")
    write_json(go, {"state": "GO", "scope": "R6-campaign-one-model", "model": model,
                    "queue_manifest_sha256": ready_sha, "one_shot": True,
                    "socrates_reviewed": True})
    wrong_go = os.path.join(tmp, "wrong-GO.json")
    write_json(wrong_go, {"state": "GO", "scope": "R6-campaign-one-model",
                          "model": EXPECTED_ORDER[1],
                          "queue_manifest_sha256": ready_sha, "one_shot": True,
                          "socrates_reviewed": True})
    expect_error("GO model", lambda: RUN.executer(
        queue_path, ready_sha, model, wrong_go), "hors modèle")
    assert len(Scenario.requests) == before

    key = lambda _secret: {"data": {"limit": 4.4, "limit_remaining": 4.4,
                                      "limit_reset": None}}
    credits = lambda _secret: {"total_credits": 10, "total_usage": 0}
    table = {"item_a": {"question": "Question", "options": ["A", "B"]},
             "item_b": {"question": "Question", "options": ["A", "B"]},
             "item_c": {"question": "Question", "options": ["A", "B"]}}
    overrides = {"f1": [("gauche", "journaliste", "item_a")],
                 "f2": [("gauche", "journaliste", "item_b")],
                 "plancher": [("droite", "adversaire", "item_c")]}

    Scenario.requests.clear()
    Scenario.stop_after = 2
    expect_error("resume", lambda: RUN.executer(
        queue_path, ready_sha, model, go, registre=ledger, import_path=imported,
        client_base=base, cle="fake", snapshot_cle=key, snapshot_solde=credits,
        table=table, cellules_override=overrides), "GO conservé")
    assert len(Scenario.requests) == 2 and os.path.exists(go)
    assert os.path.exists(R6.FICHIER_ARRET_R6)
    os.remove(R6.FICHIER_ARRET_R6)
    Scenario.stop_after = None
    report = os.path.join(tmp, "report.md")
    receipt = os.path.join(tmp, "terminal-receipt.json")
    result = RUN.executer(queue_path, ready_sha, model, go, registre=ledger,
                          import_path=imported, client_base=base, cle="fake",
                          snapshot_cle=key, snapshot_solde=credits, table=table,
                          cellules_override=overrides, rapport_path=report, recu_path=receipt)
    assert result["completed"] and len(Scenario.requests) == 3
    assert result["receipt"] == receipt and json.load(open(receipt, encoding="utf-8"))["statut"] == "TERMINE"
    assert not os.path.exists(go) and os.path.exists(go + ".consomme")
    assert all(x["provider"]["order"] == ["FakeProvider"] for x in Scenario.requests)
    with R6.RegistreGlobal(ledger) as reg:
        assert len(reg.operations_pilote(model)) == 20
        assert len(reg.operations_modele(model)) == 23
        assert reg.total_modele(model) == R6.Decimal("0.0003")
        assert reg.plafond_modele_enregistre(model) == R6.Decimal("0.50")

    descriptive = RUN.politique_modele(RUN.charger_file(queue_path, ready_sha),
                                       EXPECTED_ORDER[0])
    descriptive_report = os.path.join(tmp, "descriptive.md")
    RUN.ecrire_rapport(descriptive_report, descriptive, ready_sha, {}, True)
    assert "reste descriptif" in open(descriptive_report, encoding="utf-8").read()
    grok = RUN.politique_modele(loaded_ready, EXPECTED_ORDER[-1])
    grok_report = os.path.join(tmp, "grok.md")
    RUN.ecrire_rapport(grok_report, grok, ready_sha, {}, True)
    grok_text = open(grok_report, encoding="utf-8").read()
    assert "Rôle: **confirmatoire**" in grok_text
    assert "Non déterministe: **true**" in grok_text
    assert "reste descriptif" not in grok_text
    sequence_key = "adverse-sequence"
    sequence_path = R6.chemin_trace(sequence_key)
    expected_sequence = [("gauche", "journaliste", "item_a"),
                         ("droite", "adversaire", "item_b")]
    sequence_rows = [{"version_prompt": R6.FORMATS["q4"], "format": "q4",
                      "modele": model, "item": item, "camp": camp,
                      "identite": identity, "fournisseur_impose": "FakeProvider",
                      "raisonnement": "off", "configuration": {"max_tokens": 150}}
                     for camp, identity, item in reversed(expected_sequence)]
    with open(sequence_path, "w", encoding="utf-8") as fh:
        for row in sequence_rows:
            fh.write(json.dumps(row) + "\n")
    expect_error("trace permutée", lambda: RUN.verifier_trace(
        model, "FakeProvider", {"format": "q4"}, sequence_key, expected_sequence),
        "séquence")
    for model_name, expected_role in zip(EXPECTED_ORDER, EXPECTED_ROLES):
        policy = RUN.politique_modele(loaded_ready, model_name)
        assert policy["analysis_role"] == expected_role
        expected_marker = model_name in {EXPECTED_ORDER[0], EXPECTED_ORDER[-1]}
        assert policy["non_deterministe"] is expected_marker
        assert policy["A4_requires_machine_floor"] is expected_marker
    print("OK: ordre/roles, séquences adverses, GO, STOP-R6, reprise, provider, ledger")
finally:
    server.shutdown()
    shutil.rmtree(tmp)
