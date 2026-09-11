"""Tests synthétiques du lanceur idempotent d'analyse fine R6."""
import json
from pathlib import Path
import tempfile
import unittest

import r6_lancer_analyse_fine as LANCER
from test_r6_analyse_fine import AnalyseFineFixture, empreinte


class LancerAnalyseFineTests(unittest.TestCase):
    def test_termine_puis_est_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            output = Path(directory) / "sorties"
            first = LANCER.executer(fixture.manifest, fixture.model, output)
            self.assertEqual(first["statut"], "TERMINE")
            receipt = Path(first["sortie"]) / "execution.json"
            self.assertTrue(receipt.is_file())
            data = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual(len(data["fichiers"]), 8)
            second = LANCER.executer(fixture.manifest, fixture.model, output)
            self.assertEqual(second["statut"], "DEJA_TERMINE")
            self.assertEqual(second["sortie"], first["sortie"])

    def test_partiel_est_refuse_et_journalise_avant_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            ledger_lines = fixture.ledger.read_text(encoding="utf-8").splitlines()
            del ledger_lines[-3]
            fixture.ledger.write_text("\n".join(ledger_lines) + "\n", encoding="utf-8")
            # Si le lanceur lisait la trace avant le ledger, ce JSON invalide changerait le refus.
            trace = fixture.trace_paths[("campagne", "q4")]
            trace.write_text("invalide\n", encoding="utf-8")
            manifest = fixture.read_manifest()
            model = manifest["models"][0]
            model["ledger"]["sha256"] = empreinte(fixture.ledger)
            model["traces"][0]["sha256"] = empreinte(trace)
            fixture.rewrite_manifest(manifest)
            output = Path(directory) / "sorties"
            result = LANCER.executer(fixture.manifest, fixture.model, output)
            self.assertEqual(result["statut"], "REFUSE")
            self.assertIn("1 250 opérations", result["raison"])
            journal = output / "refus.jsonl"
            self.assertTrue(journal.is_file())
            self.assertIn("1 250 opérations", journal.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
