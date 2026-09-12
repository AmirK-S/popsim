"""P6 vu echouer, et vu passer.

Le controle de PRESENCE du recu est operationnel et teste ici dans les deux sens.

Le controle de VERIFICATION cryptographique (`ots verify`) est teste quand le
binaire `ots` est present sur la machine (`test_verification_cryptographique`) ;
sinon il est saute avec son motif explicite — un test qui passerait en sautant
silencieusement serait precisement le controle qu'on n'a jamais vu echouer. Le
test d'argument (`test_verifier_appelle_ots_avec_moins_f_sur_le_bon_fichier`) ne
depend pas de la presence du vrai binaire : un faux `ots` sur le PATH suffit a
verifier que P6 lui donne les bons arguments, sans reseau ni calendrier.
"""

from __future__ import annotations

import os
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
        """`ots verify` sur un recu force (pas un vrai fichier de timestamp) echoue
        localement, sans reseau : c'est le format qui est rejete avant toute
        consultation d'un calendrier. Verifie que P6 relaie cet echec en code 1."""
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            (d / "preuves" / "c9-preenregistrement.md.ots").write_bytes(
                b"ceci n'est pas un recu OpenTimestamps valide")
            code, sortie = self._dans(
                d, ["--verifier", "--fichier", "resultats/c9-preenregistrement.md"])
            self.assertEchoue(code, sortie, "ots verify")

    def test_verifier_appelle_ots_avec_moins_f_sur_le_bon_fichier(self):
        """`ots verify` sans `-f` suppose le fichier horodate a cote du recu (meme
        nom, sans « .ots ») : ici le recu vit dans preuves/ et le fichier reel dans
        resultats/, dans un autre repertoire. Sans `-f`, `ots verify` echouerait
        TOUJOURS avec « Could not open target », y compris sur un recu valide.
        Ce test n'a pas besoin du vrai binaire `ots` : un faux `ots` sur le PATH
        enregistre les arguments recus, pour verifier que P6 lui donne bien
        `-f <chemin du fichier reel>` avant le chemin du recu."""
        with tempfile.TemporaryDirectory() as t:
            d, _ = self._depot(t)
            (d / "preuves" / "c9-preenregistrement.md.ots").write_bytes(b"\x00OTS")
            faux_bin = Path(t) / "faux-bin"
            faux_bin.mkdir()
            marqueur = Path(t) / "argv-recus.txt"
            faux_ots = faux_bin / "ots"
            faux_ots.write_text(
                "#!/bin/sh\n"
                "if [ \"$1\" = \"--version\" ]; then echo v0.0.0-faux; exit 0; fi\n"
                f"echo \"$@\" > {marqueur}\n"
                "exit 0\n",
                encoding="utf-8")
            faux_ots.chmod(0o755)
            env = {**os.environ, "PATH": f"{faux_bin}:{os.environ['PATH']}"}
            res = subprocess.run(
                [sys.executable, str(d / "outils" / "portes" / "horodatage.py"),
                 "--verifier", "--fichier", "resultats/c9-preenregistrement.md"],
                capture_output=True, text=True, cwd=str(d), env=env)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertTrue(marqueur.exists(), "le faux ots n'a pas ete appele pour verify")
            argv = marqueur.read_text(encoding="utf-8").split()
            self.assertIn("-f", argv)
            chemin_donne = argv[argv.index("-f") + 1]
            self.assertTrue(chemin_donne.endswith("resultats/c9-preenregistrement.md"),
                            f"attendu le chemin du fichier reel apres -f, recu : {chemin_donne}")

    def test_etat_est_declare(self):
        code, sortie = lance("horodatage", ["--etat"])
        self.assertEqual(code, 0, sortie)
        self.assertTrue("ots present" in sortie or "ots ABSENT" in sortie)


if __name__ == "__main__":
    unittest.main()
