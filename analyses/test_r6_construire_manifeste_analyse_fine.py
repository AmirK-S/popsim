"""Tests factices du constructeur de manifeste terminal R6."""
import json
from pathlib import Path
import tempfile
import unittest

import r6_construire_manifeste_analyse_fine as CONSTRUIRE
import r6_runner_campagnes as RUNNER
from test_r6_analyse_fine import AnalyseFineFixture, ecrire_json, empreinte


def queue_factice(base: Path, fixture: AnalyseFineFixture):
    parent = base / "parent-ready.json"
    ecrire_json(parent, {"state": "READY"})
    rows = []
    for priority, model in enumerate(RUNNER.ORDRE_MODELES, 1):
        provider = fixture.provider if model == fixture.model else f"provider-{priority}"
        nondeterministic = model in RUNNER.NON_DETERMINISTES
        rows.append({"phase": "test", "priority": priority, "model": model,
                     "analysis_role": RUNNER.ROLES[model], "provider_fixed": provider,
                     "non_deterministe": nondeterministic,
                     "A4_requires_machine_floor": nondeterministic, "reasoning": "off",
                     "max_tokens": 150, "max_price": {"prompt": "0.1", "completion": "0.2"},
                     "call_cap_usd": "0.001", "model_cap_usd": "0.50",
                     "settled_pilot_usd": "0", "steps": [
                         {"name": "f1", "pass": "campagne", "format": "q4", "cells": 894,
                          "max_prompt_tokens": 600, "trace_cap_usd": "0.30"},
                         {"name": "f2", "pass": "campagne", "format": "q4gab3", "cells": 316,
                          "max_prompt_tokens": 1000, "trace_cap_usd": "0.15"},
                         {"name": "plancher", "pass": "plancher", "format": "q4", "cells": 40,
                          "max_prompt_tokens": 600, "trace_cap_usd": "0.05",
                          "cell_list": str(fixture.floor), "cell_list_sha256": empreinte(fixture.floor)},
                     ]})
    queue = base / "queue-ready.json"
    ecrire_json(queue, {"version": "R6-campaign-queue-1", "state": "QUEUE_READY",
                        "executable": True, "parent_ready": {"path": str(parent),
                        "sha256": empreinte(parent)}, "global_cap_usd": "4.40",
                        "account_reserve_usd": "1.50", "ledger_path": str(fixture.ledger),
                        "import_manifest_path": str(base / "import.json"), "models": rows,
                        "excluded_models": sorted(RUNNER.EXCLUS)})
    return queue, empreinte(queue)


def receipt_factice(base: Path, fixture: AnalyseFineFixture, queue_sha: str):
    consumed = base / "GO.json.consomme"
    consumed.write_text("GO consume factice\n", encoding="utf-8")
    traces = []
    for passe, fmt, cells in CONSTRUIRE.PASSES:
        path = fixture.trace_paths[(passe, fmt)]
        traces.append({"passe": passe, "format": fmt, "cellules": cells, "path": str(path),
                       "sha256": empreinte(path), "configuration": fixture.configuration})
    receipt = base / "receipt.json"
    ecrire_json(receipt, {"version": CONSTRUIRE.RECEIPT_VERSION, "statut": "TERMINE",
                           "modele": fixture.model, "fournisseur": fixture.provider,
                           "analysis_role": "descriptif", "non_deterministe": True,
                           "queue_manifest_sha256": queue_sha, "go_consomme": str(consumed),
                           "ledger": {"path": str(fixture.ledger), "sha256": empreinte(fixture.ledger)},
                           "floor_cells": {"path": str(fixture.floor), "sha256": empreinte(fixture.floor)},
                           "traces": traces})
    return receipt


class ConstruireManifesteTests(unittest.TestCase):
    def test_recu_runner_terminal_ne_contient_que_les_metadonnees(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = AnalyseFineFixture(base, model="deepseek/deepseek-v4-flash", marker=True)
            queue, queue_sha = queue_factice(base, fixture)
            policy = json.loads(queue.read_text(encoding="utf-8"))["models"][0]
            consumed = base / "GO.json.consomme"
            consumed.write_text("GO factice\n", encoding="utf-8")
            traces = [{"passe": passe, "format": fmt, "cellules": cells,
                       "path": str(fixture.trace_paths[(passe, fmt)]),
                       "sha256": empreinte(fixture.trace_paths[(passe, fmt)]),
                       "configuration": fixture.configuration}
                      for passe, fmt, cells in CONSTRUIRE.PASSES]
            receipt = base / "runner-receipt.json"
            RUNNER.ecrire_recu_terminal(str(receipt), policy, queue_sha, str(fixture.ledger),
                                        str(consumed), traces)
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(data["version"], CONSTRUIRE.RECEIPT_VERSION)
            self.assertEqual(data["statut"], "TERMINE")
            self.assertNotIn("distribution", json.dumps(data))

    def test_construit_puis_relance_idempotemment_sur_recu_terminal(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = AnalyseFineFixture(base, model="deepseek/deepseek-v4-flash", marker=True)
            queue, queue_sha = queue_factice(base, fixture)
            receipt = receipt_factice(base, fixture, queue_sha)
            first = CONSTRUIRE.executer(queue, queue_sha, receipt, fixture.orientation, fixture.referent,
                                        base / "manifests", base / "analyses")
            self.assertEqual(first["statut"], "CONSTRUIT")
            self.assertEqual(first["lanceur"]["statut"], "TERMINE")
            manifest = json.loads(Path(first["manifeste"]).read_text(encoding="utf-8"))
            self.assertEqual(manifest["version"], "R6-analyse-fine-1")
            self.assertEqual(manifest["models"][0]["model"], fixture.model)
            second = CONSTRUIRE.executer(queue, queue_sha, receipt, fixture.orientation, fixture.referent,
                                         base / "manifests", base / "analyses")
            self.assertEqual(second["statut"], "DEJA_CONSTRUIT")
            self.assertEqual(second["lanceur"]["statut"], "DEJA_TERMINE")

    def test_refuse_ledger_partiel_avant_hachage_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            fixture = AnalyseFineFixture(base, model="deepseek/deepseek-v4-flash", marker=True)
            queue, queue_sha = queue_factice(base, fixture)
            receipt = receipt_factice(base, fixture, queue_sha)
            lines = fixture.ledger.read_text(encoding="utf-8").splitlines()
            del lines[-3]
            fixture.ledger.write_text("\n".join(lines) + "\n", encoding="utf-8")
            # Une trace invalide ne doit jamais être lue lorsque le ledger n'est pas terminal.
            trace = fixture.trace_paths[("campagne", "q4")]
            trace.write_text("distribution partielle interdite\n", encoding="utf-8")
            data = json.loads(receipt.read_text(encoding="utf-8"))
            data["ledger"]["sha256"] = empreinte(fixture.ledger)
            data["traces"][0]["sha256"] = empreinte(trace)
            ecrire_json(receipt, data)
            result = CONSTRUIRE.executer(queue, queue_sha, receipt, fixture.orientation, fixture.referent,
                                         base / "manifests", base / "analyses")
            self.assertEqual(result["statut"], "REFUSE")
            self.assertIn("1 250 opérations", result["raison"])
            self.assertTrue((base / "manifests" / "refus-construction.jsonl").is_file())


if __name__ == "__main__":
    unittest.main()
