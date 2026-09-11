"""Tests adverses synthétiques du filtre d'archive publique.

Ils ne lisent ni traces, ni donnees du projet. Chaque candidat est produit dans un
TemporaryDirectory et disparait a la fin du test.
"""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).with_name("verifier_paquet_public.py")
SPEC = importlib.util.spec_from_file_location("verifier_paquet_public", SCRIPT)
PUBLIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PUBLIC)


class VerifierPaquetPublicTests(unittest.TestCase):
    def _scan(self, relative, content=b"x"):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "package"
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            return {code for _, code in PUBLIC.scan(root)}

    def test_fixture_sure_est_acceptee(self):
        self.assertEqual(self._scan("README.md"), set())

    def test_categories_interdites_sont_refusees(self):
        cases = {
            "data/reponses.csv": "data-directory",
            "journal/trace.jsonl": "trace-or-ledger",
            "comptes/ledger.json": "trace-or-ledger",
            ".env": "environment-file",
            "weights/modele.gguf": "model-weight",
            "table.csv": "sensitive-tabular-header",
        }
        for relative, expected in cases.items():
            content = b"respondent_id,value\\n1,2\\n" if relative == "table.csv" else b"x"
            with self.subTest(relative=relative):
                self.assertIn(expected, self._scan(relative, content))

    def test_cle_apres_deux_mebioctets_est_refusee(self):
        fake = b"api" + b"_key=" + b"a" * 24
        self.assertIn("credential-pattern", self._scan("notes.txt", b"x" * (2 * 1024 * 1024) + fake))

    def test_repertoire_interdit_vide_et_lien_symbolique_sont_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "package"
            (root / "models").mkdir(parents=True)
            self.assertIn("model-directory", {code for _, code in PUBLIC.scan(root)})
            (root / "alias").symlink_to(root / "models", target_is_directory=True)
            self.assertIn("symlink", {code for _, code in PUBLIC.scan(root)})


if __name__ == "__main__":
    unittest.main()
