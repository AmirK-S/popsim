"""Tests de tab_partition : determinisme, groupement, couverture des 108 items, disjonction.

Aucun appel reseau ni modele. Les tests lisent les metadonnees d'items. Le seul test qui
ouvre un fichier de reponses (test_bras_exclusifs_sur_le_masque) n'emploie que le statut
vide ou renseigne des cellules humaines de vague 4, jamais leur valeur : c'est un
comptage de structure, qui verifie la table EXPERIENCES ecrite a la main.

Usage : .venv/bin/python analyses/test_tab_partition.py
"""
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tab_partition as P  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tab_partition.py")
# Empreinte ecrite dans resultats/tab-preenregistrement.md. Si elle change, la partition
# preenregistree n'est plus celle du depot.
SHA_PREENREGISTRE = "07b3de89cdce44c9644b54fa88f09c429f9874cc2342d7c23f36a1500b183b05"
DONNEES = os.path.exists(P.CATALOGUE) and os.path.exists(P.MAPPING)


def _executer(sortie):
    r = subprocess.run([sys.executable, SCRIPT, "--sortie", sortie, "--silencieux"],
                       capture_output=True, text=True, check=False)
    return r


@unittest.skipUnless(DONNEES, "metadonnees Twin absentes")
class PartitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.chemin = os.path.join(cls.tmp.name, "partition.csv")
        cls.code = P.main(["--sortie", cls.chemin, "--silencieux"])
        cls.lignes = P.lire_csv(cls.chemin)
        with open(P.CATALOGUE, encoding="utf-8") as f:
            cls.catalogue = {q["QuestionID"]: q for q in json.load(f)}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    # -- determinisme ------------------------------------------------------
    def test_deux_executions_meme_sha(self):
        shas = []
        for k in range(2):
            sortie = os.path.join(self.tmp.name, f"run{k}.csv")
            r = _executer(sortie)
            self.assertEqual(r.returncode, 0, r.stderr)
            shas.append(r.stdout.strip().split()[-1])
            self.assertEqual(shas[-1], P.sha256_fichier(sortie))
        self.assertEqual(shas[0], shas[1])
        self.assertEqual(shas[0], P.sha256_fichier(self.chemin))

    def test_sha_egal_au_preenregistrement(self):
        self.assertEqual(P.sha256_fichier(self.chemin), SHA_PREENREGISTRE)
        if os.path.exists(P.SORTIE):
            self.assertEqual(P.sha256_fichier(P.SORTIE), SHA_PREENREGISTRE)

    # -- couverture --------------------------------------------------------
    def test_couvre_exactement_les_108_items(self):
        self.assertEqual(self.code, 0)
        attendus = [it["item"] for it in P.charger_items()]
        self.assertEqual([l["item"] for l in self.lignes], attendus)
        self.assertEqual(len(set(attendus)), 108)
        self.assertEqual(len({l["qid_parent"] for l in self.lignes}), 75)
        types = [l["type"] for l in self.lignes]
        self.assertEqual(types.count("ligne_matrice"), 40)
        self.assertEqual(types.count("MC"), 68)
        self.assertEqual(sum(l["plan"] == "inter_sujets" for l in self.lignes), 48)

    # -- disjonction -------------------------------------------------------
    def test_blocs_disjoints_et_rotations(self):
        tous = {l["item"] for l in self.lignes}
        blocs = {b: {l["item"] for l in self.lignes if l["bloc_B"] == str(b)}
                 for b in (1, 2, 3)}
        self.assertEqual(set().union(*blocs.values()), tous)
        for a in (1, 2, 3):
            for b in (1, 2, 3):
                if a < b:
                    self.assertFalse(blocs[a] & blocs[b])
            bloc_a = tous - blocs[a]
            self.assertFalse(bloc_a & blocs[a])
            self.assertEqual(bloc_a | blocs[a], tous)
        self.assertEqual([len(blocs[b]) for b in (1, 2, 3)], [36, 36, 36])

    # -- groupement --------------------------------------------------------
    def _un_seul_bloc(self, champ):
        vus = {}
        for l in self.lignes:
            if l[champ]:
                vus.setdefault(l[champ], set()).add(l["bloc_B"])
        return {k: v for k, v in vus.items() if len(v) > 1}

    def test_matrices_experiences_unites_entieres(self):
        for champ in ("qid_parent", "experience", "unite"):
            self.assertEqual(self._un_seul_bloc(champ), {}, champ)
        self.assertEqual(len({l["experience"] for l in self.lignes if l["experience"]}),
                         11)
        # Toutes les lignes de chaque matrice du catalogue sont presentes, dans un bloc.
        for qid in {l["qid_parent"] for l in self.lignes if l["type"] == "ligne_matrice"}:
            cols = [l["colonne_catalogue"] for l in self.lignes if l["qid_parent"] == qid]
            self.assertEqual(sorted(cols), sorted(self.catalogue[qid]["csv_columns"]))

    def test_lien_de_contenu_entier(self):
        for _, qids in P.LIENS_CONTENU:
            blocs = {l["bloc_B"] for l in self.lignes if l["qid_parent"] in qids}
            self.assertEqual(len(blocs), 1, qids)

    # -- echec propre ------------------------------------------------------
    def _deplacer(self, predicat):
        lignes = copy.deepcopy(self.lignes)
        cible = next(l for l in lignes if predicat(l))
        cible["bloc_B"] = "1" if cible["bloc_B"] != "1" else "2"
        return lignes

    def test_verifier_rejette_une_matrice_coupee(self):
        lignes = self._deplacer(lambda l: l["qid_parent"] == "QID198")
        with self.assertRaises(P.ErreurPartition):
            P.verifier(lignes)

    def test_verifier_rejette_un_bras_isole(self):
        lignes = self._deplacer(lambda l: l["qid_parent"] == "QID193")
        with self.assertRaises(P.ErreurPartition):
            P.verifier(lignes)

    def test_verifier_rejette_un_lien_coupe(self):
        lignes = copy.deepcopy(self.lignes)
        for l in lignes:
            if l["qid_parent"] == "QID289":
                l["bloc_B"] = "1" if l["bloc_B"] != "1" else "2"
        with self.assertRaises(P.ErreurPartition):
            P.verifier(lignes)

    def test_verifier_rejette_un_item_manquant(self):
        with self.assertRaises(P.ErreurPartition):
            P.verifier(copy.deepcopy(self.lignes)[:-1])

    def test_contenu_identique_non_groupe_echoue(self):
        with patch.object(P, "LIENS_CONTENU", []):
            items = P.charger_items()
            with self.assertRaises(P.ErreurPartition):
                P.construire_unites(items)

    def test_lien_injustifie_echoue_proprement(self):
        sortie = os.path.join(self.tmp.name, "jamais.csv")
        with patch.object(P, "LIENS_CONTENU", [("faux", ["QID287", "QID291"])]), \
                patch("sys.stderr"):
            self.assertEqual(P.main(["--sortie", sortie, "--silencieux"]), 2)
        self.assertFalse(os.path.exists(sortie))

    # -- structure des bras, statut vide ou renseigne seulement ------------
    def test_bras_exclusifs_sur_le_masque(self):
        chemin = os.path.join(P.RACINE_TWIN, "question_catalog_and_human_response_csv",
                              "wave4_response.csv")
        if not os.path.exists(chemin):
            self.skipTest("wave4_response.csv absent")
        import pandas as pd
        cols = [l["colonne_catalogue"] for l in self.lignes]
        present = pd.read_csv(chemin, usecols=cols, dtype=str).notna()
        for l in self.lignes:
            if l["plan"] == "intra_sujets":
                self.assertTrue(present[l["colonne_catalogue"]].all(), l["item"])
        for nom, bras in P.EXPERIENCES:
            vus = []
            for _, qids in bras:
                cols_bras = [l["colonne_catalogue"] for l in self.lignes
                             if l["qid_parent"] in {q for q, _ in qids}]
                m = present[cols_bras]
                # Dans un bras, les items sont vus ensemble ou pas du tout.
                self.assertTrue((m.all(axis=1) | ~m.any(axis=1)).all(), nom)
                vus.append(m.any(axis=1))
            n_bras = sum(v.astype(int) for v in vus)
            self.assertTrue((n_bras == 1).all(), nom)


if __name__ == "__main__":
    unittest.main(verbosity=2)
