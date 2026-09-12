"""P6 vu echouer, et vu passer.

Le controle de PRESENCE du recu est operationnel et teste ici dans les deux sens.
Le controle de VERIFICATION cryptographique (`ots verify`) n'est PAS teste : le
binaire `ots` est absent de la machine et sa verification exige un acces reseau a
un calendrier, exclu du mandat. Un test qui passerait en sautant silencieusement
serait precisement le controle qu'on n'a jamais vu echouer — il est donc marque
`skip` avec son motif, et P6 se declare non operationnel sur ce volet.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, commit, depot_jetable, lance

GABARIT = RACINE / "gabarits" / "preenregistrement.md"


class TestP6(CasDePorte):

    def _depot(self, t):
        d = depot_jetable(Path(t))
        (d / "resultats").mkdir()
        (d / "preuves").mkdir()
        shutil.copy(GABARIT, d / "resultats" / "c9-preenregistrement.md")
        base = commit(d, "base")
        copie = d / "outils" / "portes"
        copie.mkdir(parents=True)
        for nom in ("commun.py", "horodatage.py"):
            shutil.copy(RACINE / "outils" / "portes" / nom, copie / nom)
        return d, base

    def _dans(self, d: Path, argv: list[str]):
        res = subprocess.run(
            [sys.executable, str(d / "outils" / "portes" / "horodatage.py"), *argv],
            capture_output=True, text=True, cwd=str(d))
        return res.returncode, res.stdout + res.stderr

    def test_echec_recu_absent(self):
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            code, sortie = self._dans(
                d, ["--fichier", "resultats/c9-preenregistrement.md"])
            self.assertEchoue(code, sortie, "aucun recu d'horodatage")
            self.assertIn("ots stamp", sortie)

    def test_echec_recu_vide(self):
        """Un recu vide atteste d'une date fausse : pire que pas de recu."""
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            (d / "preuves" / "c9-preenregistrement.md.ots").write_bytes(b"")
            code, sortie = self._dans(
                d, ["--fichier", "resultats/c9-preenregistrement.md"])
            self.assertEchoue(code, sortie, "recu d'horodatage vide")

    def test_passage_recu_present(self):
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            (d / "preuves" / "c9-preenregistrement.md.ots").write_bytes(b"\x00OTS")
            code, sortie = self._dans(
                d, ["--fichier", "resultats/c9-preenregistrement.md"])
            self.assertPasse(code, sortie)
            self.assertIn("NON OPERATIONNEL", sortie,
                          "P6 doit declarer que la verification cryptographique "
                          "n'a pas eu lieu")

    def test_exiger_ots_abandonne_si_binaire_absent(self):
        """--exiger-ots doit sortir en code 2, jamais en 0, si `ots` manque."""
        if shutil.which("ots"):
            self.skipTest("ots est installe : ce cas ne s'applique pas")
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            code, sortie = self._dans(
                d, ["--exiger-ots", "--fichier", "resultats/c9-preenregistrement.md"])
            self.assertEqual(code, 2, sortie)
            self.assertIn("pip install opentimestamps-client", sortie)

    @unittest.skipIf(shutil.which("ots") is None,
                     "binaire `ots` absent : le volet verification de P6 est NON "
                     "OPERATIONNEL, il n'est pas teste et ne doit pas etre presume actif")
    def test_verification_cryptographique(self):
        self.fail("a ecrire le jour ou `ots` est installe : forger un recu invalide "
                  "et verifier que `ots verify` fait sortir P6 en code 1")

    def test_etat_est_declare(self):
        code, sortie = lance("horodatage", ["--etat"])
        self.assertEqual(code, 0, sortie)
        self.assertTrue("ots present" in sortie or "ots ABSENT" in sortie)


if __name__ == "__main__":
    unittest.main()
