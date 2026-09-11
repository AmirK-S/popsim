"""Reprise locale d'une cellule après annulation prouvée, sans réseau externe."""

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


class Server(BaseHTTPRequestHandler):
    posts = 0

    def log_message(self, *_args):
        pass

    def do_POST(self):
        Server.posts += 1
        size = int(self.headers.get("Content-Length", "0"))
        request = json.loads(self.rfile.read(size))
        body = json.dumps({
            "id": "fixture-replayed-once", "model": request["model"],
            "provider": request["provider"]["order"][0],
            "choices": [{"message": {"content": "A: 60\nB: 40"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 10,
                      "completion_tokens_details": {"reasoning_tokens": 0}, "cost": 0.0001},
        }).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def sha(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


tmp = tempfile.mkdtemp(prefix="r6-reconcile-resume-")
server = HTTPServer(("127.0.0.1", 0), Server)
threading.Thread(target=server.serve_forever, daemon=True).start()

try:
    R6.TRACES = os.path.join(tmp, "traces")
    R6.FICHIER_ARRET_R6 = os.path.join(R6.TRACES, "STOP-R6")
    R6.FICHIER_ARRET_GLOBAL = os.path.join(R6.TRACES, "STOP")
    R6.JOURNAL = os.path.join(R6.TRACES, "run.log")
    R6.verifier_referent = lambda: None
    os.makedirs(R6.TRACES)

    old = os.path.join(tmp, "old.jsonl")
    open(old, "w").close()
    imported = os.path.join(tmp, "import.json")
    with open(imported, "w", encoding="utf-8") as fh:
        json.dump({"version": "R6-v2-import-1", "exhaustif": True,
                   "attendus": {"lignes": 0, "reponses": 0, "incidents": 0,
                                "cout_annonce_reponses_usd": "0", "borne_incidents_total_usd": "0"},
                   "cout_incidents": {"observation": "inconnu", "borne_unitaire_usd": "0",
                                      "fondement_borne": "fixture"},
                   "traces": [{"chemin": old, "passe": "ancien-pilote", "classe": "ancien-pilote",
                               "sha256": sha(old),
                               "attendus": {"lignes": 0, "reponses": 0, "incidents": 0}}]}, fh)
    inventory, _ = R6.charger_import(imported)
    ledger = os.path.join(tmp, "ledger.jsonl")
    with R6.RegistreGlobal(ledger) as reg:
        reg.initialiser_evenements(inventory, [])
        identity = R6.identite_campagne("deepseek/deepseek-v4-flash", "q4", R6.FORMATS["q4"],
                                        "fucitzn", "gauche", "journaliste", "campagne")
        reg.reserver(identity, "0.001", "10", plafond_modele_usd="0.06",
                     empreinte_requete="a" * 64, fournisseur_impose="DigitalOcean")
        reg.annuler(identity, "fixture: GET evidence proves no execution")

    marker = R6.chemin_trace("fixture-resume") + ".en-cours"
    with open(marker, "w") as fh:
        json.dump({"identite_globale": identity, "empreinte_requete": "a" * 64}, fh)
    archived = marker + ".annule"
    os.replace(marker, archived)

    go = os.path.join(tmp, "GO.json")
    open(go, "w").write("GO\n")
    key = lambda _key: {"data": {"limit": 4.4, "limit_remaining": 4.4, "limit_reset": None}}
    credits = lambda _key: {"total_credits": 10, "total_usage": 0}
    transaction = R6.TransactionPayante(ledger, inventory, "campagne", "0.001", 600,
                                         key, credits, plafond_modele="0.06", fichier_go=go)
    client = R6.ClientChat("fixture", base=f"http://127.0.0.1:{server.server_address[1]}/api/v1",
                           raisonnement="off", fournisseur="DigitalOcean",
                           max_price={"prompt": "0.11", "completion": "0.22"})
    table = {"fucitzn": {"question": "Fixture", "options": ["A", "B"]}}
    result = R6.lancer(client, "deepseek/deepseek-v4-flash", "q4", table,
                        [("gauche", "journaliste", "fucitzn")],
                        R6.Budget("0.01", 0.11 / 1_000_000, 0.22 / 1_000_000),
                        "fixture-resume", n_predict=150, transaction=transaction,
                        manifeste_import=imported)
    assert result["cellules"] == 1 and Server.posts == 1 and not os.path.exists(marker)
    with R6.RegistreGlobal(ledger) as reg:
        assert reg.operations[identity]["etat"] == "reglee"
        assert sum(e.get("type") == "annulation" for e in reg.evenements) == 1
    print("OK: annulation prouvée, marqueur archivé, une reprise locale et un seul POST fixture")
finally:
    server.shutdown()
    shutil.rmtree(tmp)
