"""Tests hors ligne du runner générique des pilotes R6.

Le seul serveur utilisé écoute sur 127.0.0.1. Les clés, traces, GO et STOP sont factices
et vivent dans un dossier temporaire.
"""

import hashlib
import json
import os
import shutil
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))
import r6_oracle_distant as R6
import r6_runner_pilotes as RUNNER


COMPATIBLES = [
    ("mistralai/mistral-small-2603", "Mistral", "0.15", "0.6"),
    ("qwen/qwen3.7-plus", "Alibaba", "0.32", "1.28"),
    ("moonshotai/kimi-k2.5", "SiliconFlow", "0.45", "2.25"),
    ("z-ai/glm-5", "StreamLake", "0.6", "1.92"),
    ("google/gemini-3.8-flash", "Google AI Studio", "0.375", "1.875"),
    ("anthropic/claude-haiku-4.5", "Anthropic", "1", "5"),
    ("x-ai/grok-4.3", "xAI", "2", "6"),
]
INCOMPATIBLES = [
    "meta-llama/llama-4-maverick", "openai/gpt-5.6-luna",
    "openai/gpt-5.4", "anthropic/claude-sonnet-5",
]


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
            "id": f"gen-{len(Scenario.requests)}",
            "model": payload["model"],
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
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def expect_error(label, function, fragment):
    try:
        function()
    except (ValueError, BlockingIOError) as exc:
        assert fragment in str(exc), (label, str(exc))
    else:
        raise AssertionError(label + " n'a pas été refusé")


tmp = tempfile.mkdtemp(prefix="r6-runner-test-")
server = HTTPServer(("127.0.0.1", 0), FakeServer)
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{server.server_address[1]}/api/v1"

try:
    R6.TRACES = os.path.join(tmp, "traces")
    os.makedirs(os.path.join(R6.TRACES, "reprise"))
    R6.JOURNAL = os.path.join(R6.TRACES, "r6-run.log")
    R6.FICHIER_ARRET_GLOBAL = os.path.join(R6.TRACES, "STOP")
    R6.FICHIER_ARRET_R6 = os.path.join(R6.TRACES, "STOP-R6")
    R6.verifier_referent = lambda: None
    Scenario.stop_path = R6.FICHIER_ARRET_R6

    cell_path = os.path.join(tmp, "pilot-cells.txt")
    cells = [(f"item_{i}", "gauche", "journaliste") for i in range(10)]
    with open(cell_path, "w", encoding="utf-8") as handle:
        for item, camp, identity in cells:
            handle.write(f"{item}\t{camp}\t{identity}\n")
    table = {item: {"question": item, "options": ["A", "B"]}
             for item, _camp, _identity in cells}

    empty_trace = os.path.join(tmp, "old.jsonl")
    open(empty_trace, "w").close()
    import_path = os.path.join(tmp, "import.json")
    write_json(import_path, {
        "version": "R6-v2-import-1", "exhaustif": True,
        "attendus": {"lignes": 0, "reponses": 0, "incidents": 0,
                    "cout_annonce_reponses_usd": "0",
                    "borne_incidents_total_usd": "0"},
        "cout_incidents": {"observation": "inconnu", "borne_unitaire_usd": "0",
                           "fondement_borne": "fixture sans incident"},
        "traces": [{"chemin": empty_trace, "passe": "ancien-pilote",
                    "classe": "ancien-pilote", "sha256": sha(empty_trace),
                    "attendus": {"lignes": 0, "reponses": 0, "incidents": 0}}],
    })
    inventory, _events = R6.charger_import(import_path)

    panel = []
    for model, provider, prompt, completion in COMPATIBLES:
        panel.append({
            "model": model, "provider_fixed": provider,
            "prepared_model_spend_cap_usd": "0.50",
            "provider_proposal": {"provider_name": provider,
                                  "required_payload_parameters_supported": True},
            "pilot_plan": {"required": True, "passes": ["essai-1", "essai-2"],
                           "cells_per_pass": 10, "cell_list": cell_path,
                           "cell_list_sha256": sha(cell_path), "max_tokens": 150,
                           "max_prompt_tokens": 600, "reasoning": "off",
                           "max_price_prompt_usd_per_million": prompt,
                           "max_price_completion_usd_per_million": completion,
                           "reserved_call_usd": "0.001",
                           "pilot_total_cap_usd": "0.02"},
        })
    for model in INCOMPATIBLES:
        panel.append({"model": model, "provider_fixed": None,
                      "provider_proposal": None,
                      "pilot_plan": {"required": True, "blocked": "incompatible"}})
    manifest_path = os.path.join(tmp, "ready.json")
    runner_guard = {"ledger_path": os.path.join(tmp, "unused-ledger.jsonl"),
                    "import_manifest_path": import_path}
    write_json(manifest_path, {"version": "R6-campaign-readiness-TEST",
                               "state": "READY", "executable": True, "panel": panel,
                               "pilot_runner_guard": runner_guard})
    manifest_sha = sha(manifest_path)

    # Les sept seules lignes compatibles se chargent depuis le manifeste signé.
    manifest, _ = RUNNER.charger_manifeste(manifest_path, manifest_sha)
    for model, provider, _prompt, _completion in COMPATIBLES:
        assert RUNNER.politique_modele(manifest, model)["provider"] == provider
    for model in INCOMPATIBLES:
        expect_error("incompatible " + model,
                     lambda model=model: RUNNER.politique_modele(manifest, model),
                     "non compatible")

    def fresh_ledger(name):
        path = os.path.join(tmp, name)
        with R6.RegistreGlobal(path) as ledger:
            ledger.initialiser_evenements(inventory, [])
        return path

    key_snapshot = lambda _key: {"data": {"limit": 4.4, "limit_remaining": 4.4,
                                             "limit_reset": None}}
    credit_snapshot = lambda _key: {"total_credits": 10, "total_usage": 0}

    # STOP précède toute requête et reste présent.
    ledger_stop = fresh_ledger("ledger-stop.jsonl")
    go_stop = os.path.join(tmp, "go-stop.json")
    write_json(go_stop, {"state": "GO", "scope": "R6-pilot-one-model",
                         "model": COMPATIBLES[0][0],
                         "prepare_manifest_sha256": manifest_sha, "one_shot": True})
    open(R6.FICHIER_ARRET_R6, "w").close()
    before = len(Scenario.requests)
    expect_error("STOP", lambda: RUNNER.executer(
        manifest_path, manifest_sha, COMPATIBLES[0][0], go_stop, False,
        ledger_stop, import_path, base, "fake", key_snapshot, credit_snapshot, table),
        "STOP present")
    assert len(Scenario.requests) == before and os.path.exists(R6.FICHIER_ARRET_R6)
    os.remove(R6.FICHIER_ARRET_R6)

    # Une interruption après 15 réponses conserve le GO; la reprise n'achète que 5 cellules.
    model, provider, _prompt, _completion = COMPATIBLES[1]
    ledger = fresh_ledger("ledger.jsonl")
    go = os.path.join(tmp, "go.json")
    write_json(go, {"state": "GO", "scope": "R6-pilot-one-model", "model": model,
                    "prepare_manifest_sha256": manifest_sha, "one_shot": True})
    Scenario.requests.clear()
    Scenario.stop_after = 15
    expect_error("reprise", lambda: RUNNER.executer(
        manifest_path, manifest_sha, model, go, False, ledger, import_path, base,
        "fake", key_snapshot, credit_snapshot, table), "GO conserve")
    assert len(Scenario.requests) == 15 and os.path.exists(go)
    os.remove(R6.FICHIER_ARRET_R6)
    Scenario.stop_after = None
    result = RUNNER.executer(manifest_path, manifest_sha, model, go, False, ledger,
                            import_path, base, "fake", key_snapshot, credit_snapshot, table)
    assert result["completed"] and len(Scenario.requests) == 20
    assert not os.path.exists(go) and os.path.exists(go + ".consomme")
    assert all(req["provider"] == {"order": [provider], "allow_fallbacks": False,
                                    "max_price": {"prompt": 0.32,
                                                  "completion": 1.28}}
               for req in Scenario.requests)
    first = Scenario.requests[:10]
    second = Scenario.requests[10:]
    assert [x["messages"] for x in first] == [x["messages"] for x in second]
    with R6.RegistreGlobal(ledger) as registry:
        assert len(registry.operations_pilote(model)) == 20
        assert registry.total_pilote(model) == R6.Decimal("0.0020")
        assert registry.total_modele(model) == R6.Decimal("0.0020")
        assert registry.plafond_pilote_enregistre(model) == R6.Decimal("0.02")
        assert registry.plafond_modele_enregistre(model) == R6.Decimal("0.50")
    expect_error("GO one-shot", lambda: RUNNER.executer(
        manifest_path, manifest_sha, model, go, False, ledger, import_path, base,
        "fake", key_snapshot, credit_snapshot, table), "deja consomme")

    # DeepSeek déjà engagé reste consultable, mais ne peut jamais repartir.
    deep_ledger = fresh_ledger("ledger-deepseek.jsonl")
    deep_policy = dict(R6.politique_pilote_legacy())
    with R6.RegistreGlobal(deep_ledger) as registry:
        identity = R6.identite_campagne(R6.MODELE_PILOTE, "q4", R6.FORMATS["q4"],
                                        "item_0", "gauche", "journaliste", "essai-1")
        registry.reserver(identity, "0.001", "10", empreinte_requete="a" * 64,
                          fournisseur_impose=R6.FOURNISSEUR_PILOTE,
                          plafond_pilote_usd="0.02", appels_pilote_max=20,
                          borne_pilote_max_usd="0.001")
        registry.reconcilier(identity, "0.0001", "gen-deepseek")
    deep_row = {
        "model": R6.MODELE_PILOTE, "provider_fixed": R6.FOURNISSEUR_PILOTE,
        "prepared_model_spend_cap_usd": "0.50",
        "pilot_complete": True,
        "provider_proposal": {"provider_name": R6.FOURNISSEUR_PILOTE,
                              "required_payload_parameters_supported": True},
        "pilot_plan": {"required": False, "verification_only": True,
                       "passes": ["essai-1", "essai-2"],
                       "cells_per_pass": 10, "cell_list": cell_path,
                       "cell_list_sha256": sha(cell_path), "max_tokens": 150,
                       "max_prompt_tokens": 600, "reasoning": "off",
                       "max_price_prompt_usd_per_million": "0.11",
                       "max_price_completion_usd_per_million": "0.22",
                       "reserved_call_usd": "0.001", "pilot_total_cap_usd": "0.02"},
    }
    write_json(manifest_path, {"version": "R6-campaign-readiness-TEST",
                               "state": "READY", "executable": True,
                               "panel": panel + [deep_row],
                               "pilot_runner_guard": runner_guard})
    deep_sha = sha(manifest_path)
    requests_before_deepseek = len(Scenario.requests)
    diagnostic_deepseek = RUNNER.executer(
        manifest_path, deep_sha, R6.MODELE_PILOTE, verifier=True,
        registre=deep_ledger, import_path=import_path)
    assert diagnostic_deepseek["pilot_operations"] == 1
    assert diagnostic_deepseek["mode"] == "verification-hors-reseau"
    assert len(Scenario.requests) == requests_before_deepseek
    deep_go = os.path.join(tmp, "go-deep.json")
    write_json(deep_go, {"state": "GO", "scope": "R6-pilot-one-model",
                         "model": R6.MODELE_PILOTE,
                         "prepare_manifest_sha256": deep_sha, "one_shot": True})
    expect_error("DeepSeek consommé", lambda: RUNNER.executer(
        manifest_path, deep_sha, R6.MODELE_PILOTE, deep_go, False, deep_ledger,
        import_path, base, "fake",
        lambda _key: (_ for _ in ()).throw(AssertionError("lecture cle interdite")),
        lambda _key: (_ for _ in ()).throw(AssertionError("lecture solde interdite")),
        table),
        "verification hors reseau seulement")
    assert len(Scenario.requests) == requests_before_deepseek

    print("TOUT PASSE: 7 compatibles, 4 incompatibles, STOP, reprise, GO one-shot, ledger")
finally:
    server.shutdown()
    shutil.rmtree(tmp, ignore_errors=True)
