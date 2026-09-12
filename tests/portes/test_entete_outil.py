"""Tests pour outils/entete.py — poser et verifier l'en-tete A2.

Regle G0.5 (Methode v1) : « un controle qu'on n'a jamais vu echouer n'est pas
un controle ». Cas d'echec executes ici : fichier deja pourvu d'un en-tete,
champ obligatoire manquant, fichier inexistant — en plus des cas de passage.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
OUTIL = RACINE / "outils" / "entete.py"

TITRE = "# Rapport jouet\n\nCorps du rapport.\n"


def lance(argv: list[str]) -> tuple[int, str]:
    res = subprocess.run([sys.executable, str(OUTIL), *argv],
                         capture_output=True, text=True)
    return res.returncode, res.stdout + res.stderr


class TestEnteteOutilPoser(unittest.TestCase):

    def _fichier(self, tmp, texte: str = TITRE, nom: str = "r.md") -> Path:
        p = Path(tmp) / nom
        p.write_text(texte, encoding="utf-8")
        return p

    # --- cas d'echec ---------------------------------------------------------

    def test_echec_fichier_inexistant(self):
        with tempfile.TemporaryDirectory() as t:
            cible = Path(t) / "absent.md"
            code, sortie = lance([
                "--poser", str(cible), "--mandat", "m", "--agent", "a",
                "--ecriture", "e", "--cout-reel-usd", "0.00",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("introuvable", sortie)

    def test_echec_champ_obligatoire_manquant(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            # --mandat absent : ne doit pas inventer de valeur, doit echouer bruyamment
            code, sortie = lance([
                "--poser", str(p), "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("--mandat", sortie)
            # le fichier n'a pas ete touche
            self.assertEqual(p.read_text(encoding="utf-8"), TITRE)

    def test_echec_cout_reel_usd_manquant(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            code, sortie = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("--cout-reel-usd", sortie)
            self.assertEqual(p.read_text(encoding="utf-8"), TITRE)

    def test_echec_entete_deja_present(self):
        with tempfile.TemporaryDirectory() as t:
            deja = TITRE.replace(
                "Corps du rapport.",
                "statut: courant\nmandat: x\nagent: x\nCorps du rapport.")
            p = self._fichier(t, deja)
            avant = p.read_text(encoding="utf-8")
            code, sortie = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("deja", sortie.lower())
            # refus de dupliquer : le fichier reste inchange
            self.assertEqual(p.read_text(encoding="utf-8"), avant)

    def test_echec_sans_titre(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t, "Pas de titre ici.\n")
            code, sortie = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("titre", sortie.lower())

    def test_echec_retracte_sans_fait_foi(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            code, sortie = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00", "--statut", "retracte_par: resultats/audit.md",
            ])
            self.assertNotEqual(code, 0)
            self.assertIn("fait_foi", sortie.lower())

    # --- cas de passage --------------------------------------------------------

    def test_passage_pose_entete(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            code, sortie = lance([
                "--poser", str(p), "--mandat", "trancher si la porte se ferme",
                "--agent", "Opus 5, Anthropic", "--ecriture", "r.md",
                "--cout-reel-usd", "0.00",
            ])
            self.assertEqual(code, 0, sortie)
            texte = p.read_text(encoding="utf-8")
            self.assertTrue(texte.startswith("# Rapport jouet\n\nstatut: courant\n"))
            self.assertIn("mandat: trancher si la porte se ferme", texte)
            self.assertIn("agent: Opus 5, Anthropic", texte)
            self.assertIn("ecriture: r.md", texte)
            self.assertIn("lecture_seule: tout le reste", texte)
            self.assertIn("interdits: appel payant sans GO", texte)
            self.assertIn("cout_reel_usd: 0.00", texte)
            self.assertIn("Corps du rapport.", texte)

            # une deuxieme pose sur le meme fichier est refusee (pas de doublon)
            code2, sortie2 = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00",
            ])
            self.assertNotEqual(code2, 0)

    def test_passage_retracte_avec_fait_foi(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            code, sortie = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00", "--statut", "retracte_par: resultats/audit.md",
                "--fait-foi", "resultats/audit.md",
            ])
            self.assertEqual(code, 0, sortie)
            texte = p.read_text(encoding="utf-8")
            self.assertIn("retracte_par: resultats/audit.md", texte)
            self.assertIn("fait_foi: resultats/audit.md", texte)


class TestEnteteOutilVerifier(unittest.TestCase):

    def _fichier(self, tmp, texte: str = TITRE, nom: str = "r.md") -> Path:
        p = Path(tmp) / nom
        p.write_text(texte, encoding="utf-8")
        return p

    def test_echec_verifier_fichier_inexistant(self):
        with tempfile.TemporaryDirectory() as t:
            code, sortie = lance(["--verifier", str(Path(t) / "absent.md")])
            self.assertNotEqual(code, 0)
            self.assertIn("introuvable", sortie)

    def test_echec_verifier_absent(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            avant = p.read_text(encoding="utf-8")
            code, sortie = lance(["--verifier", str(p)])
            self.assertNotEqual(code, 0)
            # --verifier ne modifie jamais le fichier
            self.assertEqual(p.read_text(encoding="utf-8"), avant)

    def test_echec_verifier_incomplet(self):
        with tempfile.TemporaryDirectory() as t:
            incomplet = TITRE.replace(
                "Corps du rapport.",
                "statut: courant\nmandat: m\nCorps du rapport.")
            p = self._fichier(t, incomplet)
            code, sortie = lance(["--verifier", str(p)])
            self.assertNotEqual(code, 0)
            self.assertIn("agent", sortie)

    def test_passage_verifier_complet(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(t)
            code_pose, _ = lance([
                "--poser", str(p), "--mandat", "m", "--agent", "a", "--ecriture", "e",
                "--cout-reel-usd", "0.00",
            ])
            self.assertEqual(code_pose, 0)
            code, sortie = lance(["--verifier", str(p)])
            self.assertEqual(code, 0, sortie)


if __name__ == "__main__":
    unittest.main()
