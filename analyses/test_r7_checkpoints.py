"""Tests factices du pilote R7: aucun serveur, GPU, reseau ni generation reelle."""
import argparse
import json
from pathlib import Path
import tempfile
import time
import unittest
from unittest.mock import patch

from tokenizers import Tokenizer, models, pre_tokenizers

import r7_checkpoints as R7


def faux_plan(n=149):
    items = [f"item{i:03d}" for i in range(n)]
    table = {i: {"question": f"Synthetic question {i}?", "options": ["Yes", "No"]}
             for i in items}
    return items, table


class FauxProc:
    pid = 424242


class FauxMoteur:
    instances = []
    reponses = []

    def __init__(self, modele, contexte, parallele, port, cache_kv_8bits):
        self.modele = modele
        self.proc = None
        self.appels = 0
        FauxMoteur.instances.append(self)

    def demarrer(self):
        self.proc = FauxProc()

    def arreter(self):
        self.proc = None

    def decrire(self, prompt, n_predict, arrets):
        self.appels += 1
        texte = self.reponses.pop(0) if self.reponses else "A: 60\nB: 40"
        return {"texte": texte, "duree_ms": 1.0, "tokens_generes": 8,
                "tokens_prompt": 300, "arret": "stop"}


class FauxMoteurEnEchec(FauxMoteur):
    def decrire(self, prompt, n_predict, arrets):
        raise RuntimeError("panne factice")


class R7Tests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.traces = self.base / "traces"
        self.traces.mkdir()
        self.items, self.table = faux_plan()
        self.modeles = R7.modele_info(self.base / "final.gguf")
        self.registre = {
            "modeles": self.modeles,
            "conditions": {c: {"trace": str(self.traces / f"r1-{c}-r7.jsonl")}
                           for c in R7.ORDRE},
        }
        self.args = argparse.Namespace(port=0, depot_plan="osf:test-depot")
        FauxMoteur.instances = []
        FauxMoteur.reponses = []
        self.patches = [
            patch.object(R7, "TRACES", self.traces),
            patch.object(R7.R1, "TRACES", str(self.traces)),
            patch.object(R7.R1, "FICHIER_ARRET", str(self.traces / "STOP")),
            patch.object(R7, "JOURNAL", self.traces / "r7-run-factice.log"),
            patch.object(R7, "exiger_serveur_unique", return_value=None),
            patch.object(R7, "premier_port_libre", return_value=39001),
            patch.object(R7, "port_libre", return_value=True),
        ]
        for p in self.patches:
            p.start()

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def run_fake(self):
        return R7.executer(
            self.registre, self.items, self.table, {}, time.time() + 3600,
            R7.dt.datetime.now() + R7.dt.timedelta(hours=1), self.args,
            self.base / "registre.json", moteur_cls=FauxMoteur)

    def test_plan_compte_quatre_fois_894_et_prompts_r4(self):
        prompts = R7.prompts_plan(self.items, self.table)
        self.assertEqual(len(prompts), 894)
        self.assertEqual(4 * len(prompts), 3576)
        for item, camp, identite, prompt in prompts:
            sys_txt = R7.R1.systeme(camp, identite)
            usr_txt, _ = R7.R1.utilisateur(item, camp, self.table, rappel=False)
            self.assertEqual(prompt, R7.R4.gabarit(R7.GABARIT, sys_txt, usr_txt))
            self.assertEqual(prompt, R7.R1.gabarit(R7.GABARIT, sys_txt, usr_txt))
            self.assertTrue(prompt.endswith("\n\n"))
        self.assertEqual(R7.ARRETS, R7.R4.ARRETS)

    def test_finale_explicite_exige_provenance_validee_correspondante(self):
        finale = self.base / "final.gguf"
        with finale.open("wb") as f:
            f.truncate(2 * 1024**3)
        prov = self.base / "provenance.json"
        bon = {"status": "VALIDATED_TEMPORARY", "output": str(finale),
               "output_sha256": "a" * 64,
               "converter_commit": R7.CONVERTER_COMMIT,
               "revision": R7.REVISION_FINALE,
               "validation": {"status": "PASS", "path": str(finale),
                              "bytes": finale.stat().st_size}}
        prov.write_text(json.dumps(bon))
        self.assertEqual(R7.lire_provenance_finale(finale, prov)["status"],
                         "VALIDATED_TEMPORARY")
        bon["output"] = str(self.base / "autre.gguf")
        prov.write_text(json.dumps(bon))
        with self.assertRaisesRegex(RuntimeError, "different"):
            R7.lire_provenance_finale(finale, prov)

    def test_provenance_refuse_commit_taille_et_hash_malformes(self):
        finale = self.base / "final.gguf"
        with finale.open("wb") as f:
            f.truncate(2 * 1024**3)
        prov = self.base / "provenance.json"
        bon = {"status": "VALIDATED_TEMPORARY", "output": str(finale),
               "output_sha256": "a" * 64, "converter_commit": R7.CONVERTER_COMMIT,
               "revision": R7.REVISION_FINALE,
               "validation": {"status": "PASS", "path": str(finale),
                              "bytes": finale.stat().st_size}}
        for mutation, motif in (({"output_sha256": "z" * 64}, "output_sha256"),
                                ({"converter_commit": "autre"}, "commit"),
                                ({"validation": {**bon["validation"], "bytes": 1}}, "taille")):
            d = {**bon, **mutation}
            prov.write_text(json.dumps(d))
            with self.assertRaisesRegex(RuntimeError, motif):
                R7.lire_provenance_finale(finale, prov)

    def test_tokeniseurs_publient_egalite_exacte_des_ids(self):
        snapshots = {}
        for i, cle in enumerate(R7.ORDRE):
            dossier = self.base / cle
            dossier.mkdir()
            vocab = {"[UNK]": 0, "alpha": 1, "beta": 2}
            if i == 1:
                vocab = {"[UNK]": 0, "alpha": 2, "beta": 1}
            tok = Tokenizer(models.WordLevel(vocab=vocab, unk_token="[UNK]"))
            tok.pre_tokenizer = pre_tokenizers.Whitespace()
            tok.save(str(dossier / "tokenizer.json"))
            (dossier / "tokenizer_config.json").write_text(
                json.dumps({"bos_token": None, "eos_token": None}))
            snapshots[cle] = dossier
        resultat = R7.verifier_tokenisation(
            [("i1", "gauche", "journaliste", "alpha beta")], snapshots)
        comp = {(d["a"], d["b"]): d for d in resultat["comparaisons"]}
        self.assertEqual(comp[("olmo3base", "olmo3sft")]["cellules_au_dela_2pct"], 0)
        self.assertEqual(comp[("olmo3base", "olmo3sft")]["sequences_ids_differentes"], 1)
        self.assertFalse(comp[("olmo3base", "olmo3sft")]["sequences_ids_identiques"])
        self.assertTrue(comp[("olmo3base", "olmo3dpo")]["sequences_ids_identiques"])

    def test_sonde_rejet_arrete_a_60_et_passe_condition_suivante(self):
        FauxMoteur.reponses = ["illisible"] * 60
        self.run_fake()
        trace = self.traces / "r1-olmo3base-r7.jsonl"
        self.assertEqual(len(trace.read_text().splitlines()), 60)
        self.assertEqual(self.registre["conditions"]["olmo3base"]["statut"], "ARRET_SONDE")
        self.assertEqual(FauxMoteur.instances[0].appels, 60)
        # Les conditions suivantes restent jouables et ne partagent jamais leur serveur.
        self.assertEqual(len(FauxMoteur.instances), 4)
        self.assertEqual(sum(m.appels for m in FauxMoteur.instances), 60 + 3 * 894)

    def test_seuil_sonde_est_strictement_superieur_a_moitie(self):
        lignes = [{"rejet": i < 30} for i in range(60)]
        self.assertTrue(R7.bilan_sonde(lignes)["passe"])
        lignes[30]["rejet"] = True
        self.assertFalse(R7.bilan_sonde(lignes)["passe"])

    def test_rejets_finaux_superieurs_a_25pct_marquent_condition(self):
        FauxMoteur.reponses = (["A: 60\nB: 40"] * 60 + ["illisible"] * 224)
        self.run_fake()
        etat = self.registre["conditions"]["olmo3base"]
        self.assertEqual(etat["statut"], "REJET_FORMAT")
        self.assertEqual(etat["bilan"]["rejets"], 224)
        self.assertFalse(etat["bilan"]["passe"])
        self.assertEqual(self.registre["statut"], "TERMINE")

    def test_reprise_complete_la_sonde_sans_rejouer_les_20_premieres(self):
        info = self.modeles["olmo3base"]
        moteur = FauxMoteur("x", 4096, 1, 1, True)
        moteur.demarrer()
        R7.R1.VERSION_PROMPT = R7.VERSION_PROMPT
        R7.R1.lancer(moteur, "olmo3base", info, self.items, self.table, {},
                     R7.R1.CAMPS, R7.R1.IDENTITES, time.time() + 100, R7.SUFFIXE,
                     limite=20, sans_relance=True)
        avant = (self.traces / "r1-olmo3base-r7.jsonl").read_bytes()
        self.run_fake()
        lignes = (self.traces / "r1-olmo3base-r7.jsonl").read_bytes()
        self.assertTrue(lignes.startswith(avant))
        self.assertEqual(len(lignes.splitlines()), 894)
        # 874 seulement pour la condition reprise, puis 894 pour chacune des trois autres.
        self.assertEqual(sum(m.appels for m in FauxMoteur.instances[1:]), 874 + 3 * 894)
        traces = [json.loads(x) for x in lignes.decode().splitlines()]
        self.assertTrue(all(x["n_tentatives"] == 1 and x["sans_relance"] for x in traces))

    def test_stop_present_ne_lance_aucun_serveur(self):
        (self.traces / "STOP").touch()
        self.run_fake()
        self.assertEqual(FauxMoteur.instances, [])
        self.assertEqual(self.registre["statut"], "INTERROMPU_REPRENABLE")

    def test_fin_dure_atteinte_ne_lance_aucun_serveur(self):
        R7.executer(self.registre, self.items, self.table, {}, time.time() - 1,
                    R7.dt.datetime.now(), self.args, self.base / "registre.json",
                    moteur_cls=FauxMoteur)
        self.assertEqual(FauxMoteur.instances, [])
        self.assertEqual(self.registre["statut"], "INTERROMPU_REPRENABLE")

    def test_exclusivite_detecte_r2b_sans_serveur(self):
        ps = ("111 /opt/python /opt/python analyses/r2b_extension.py --heures 3\n"
              "222 /usr/bin/llama-server llama-server -m autre.gguf\n")
        with patch.object(R7.subprocess, "check_output", return_value=ps):
            trouves = R7.processus_bloquants()
        self.assertEqual({x["raison"] for x in trouves}, {"R2b", "llama-server"})

    def test_exclusivite_refuse_si_serveur_attendu_a_disparu(self):
        with patch.object(R7.subprocess, "check_output", return_value=""):
            self.assertEqual(R7.processus_bloquants(424242),
                             [{"pid": 424242, "raison": "serveur R7 attendu absent"}])

    def test_panne_technique_bloque_les_conditions_suivantes(self):
        with self.assertRaisesRegex(RuntimeError, "echec technique"):
            R7.executer(self.registre, self.items, self.table, {}, time.time() + 3600,
                        R7.dt.datetime.now() + R7.dt.timedelta(hours=1), self.args,
                        self.base / "registre.json", moteur_cls=FauxMoteurEnEchec)
        self.assertEqual(len(FauxMoteur.instances), 1)
        self.assertEqual(self.registre["conditions"]["olmo3base"]["statut"],
                         "INTERROMPU_REPRENABLE")
        self.assertEqual(self.registre["statut"], "INTERROMPU_REPRENABLE")

    def test_garde_memoire_refuse_sonde_illisible_ou_sous_15pct(self):
        for sortie, motif in (("garbage", "illisible"),
                              ("System-wide memory free percentage: 14%", "sous le seuil")):
            faux = type("R", (), {"stdout": sortie})()
            with patch.object(R7.subprocess, "run", return_value=faux):
                with self.assertRaisesRegex(RuntimeError, motif):
                    R7.exiger_memoire_disponible()
        faux = type("R", (), {"stdout": "System-wide memory free percentage: 15%"})()
        with patch.object(R7.subprocess, "run", return_value=faux):
            self.assertEqual(R7.exiger_memoire_disponible(), 15.0)

    def test_trace_tronquee_bloque_reprise(self):
        path = self.traces / "r1-olmo3base-r7.jsonl"
        path.write_text('{"version_prompt":"r7-c3"')
        with self.assertRaisesRegex(RuntimeError, "tronquee"):
            R7.auditer_trace("olmo3base", self.modeles["olmo3base"], self.items)

    def test_execution_refuse_sans_depot_plan(self):
        self.args.depot_plan = None
        with self.assertRaisesRegex(RuntimeError, "depot-plan"):
            self.run_fake()
        self.assertEqual(FauxMoteur.instances, [])

    def test_un_rejet_ne_declenche_jamais_deuxieme_tentative(self):
        info = self.modeles["olmo3base"]
        FauxMoteur.reponses = ["illisible"]
        moteur = FauxMoteur("x", 4096, 1, 1, True)
        moteur.demarrer()
        R7.R1.VERSION_PROMPT = R7.VERSION_PROMPT
        resultat = R7.R1.lancer(
            moteur, "olmo3base", info, self.items[:1], self.table, {}, ["gauche"],
            ["journaliste"], time.time() + 100, R7.SUFFIXE, sans_relance=True)
        ligne = json.loads((self.traces / "r1-olmo3base-r7.jsonl").read_text())
        self.assertEqual(moteur.appels, 1)
        self.assertEqual(resultat["rejets"], 1)
        self.assertEqual(ligne["n_tentatives"], 1)


if __name__ == "__main__":
    unittest.main()
