"""Tests legers de r6_evaluer: donnees factices temporaires et sorties R4 locales."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

import r6_evaluer as R6


class R6StatistiquesTests(unittest.TestCase):
    def test_h1_est_une_regle_sans_p(self):
        valeurs = [0.40, 0.80, 1.00, 1.10, 1.30]
        lignes = []
        for modele, v in zip(R6.FERMES, valeurs):
            lignes.append(R6._ligne("F1", "H1", modele, "EXECUTE", "factice",
                                     n_items=79, estimateur=v, ic_bas=v-.05, ic_haut=v+.05))
        r = R6.evaluer_h1(pd.DataFrame(lignes))
        self.assertEqual(r["statut"], "EVALUE")
        self.assertTrue(r["satisfaite"])
        self.assertTrue(np.isnan(r["p"]))

    def test_h3b_teste_reellement_le_seuil_plus_030(self):
        items = [f"i{i}" for i in range(8)]
        def table(mult):
            return pd.DataFrame({"modele": [R6.FERMES[0]] * 8,
                                 "identite": ["journaliste"] * 8, "item": items,
                                 "gap_signe_decrit": np.arange(1, 9) * .1 * mult,
                                 "gap_signe_reel_w1": np.arange(1, 9) * .1})
        vus = []
        def permutation(d, _rng, _n):
            vus.append(np.asarray(d, float))
            return .5
        with patch.object(R6.R1, "p_permutation_signe", side_effect=permutation):
            lignes = R6.tests_h3(table(1.0), table(1.35), set(items),
                                 np.random.default_rng(2), 80, 199)
        h3b = next(x for x in lignes if x["hypothese"] == "H3b")
        self.assertAlmostEqual(h3b["estimateur"], .35)
        self.assertEqual(h3b["seuil"], .30)
        r = np.arange(1, 9) * .1
        np.testing.assert_allclose(vus[0], .35 * r)
        np.testing.assert_allclose(vus[1], .35 * r - .30 * r)

    def test_h2_exige_ic_et_plancher_machine(self):
        modele = R6.FERMES[0]
        ident = pd.DataFrame({"modele": [modele] * 6, "camp": ["gauche"] * 6,
                              "item": range(6), "tv_entre_identites": [.30] * 6,
                              "tv_plancher_w1_w2": [.10] * 6})
        lignes = R6.tests_h2(ident, {modele: .20}, np.random.default_rng(3), 60, 99)
        g = next(x for x in lignes if x["modele"] == modele and x["camp"] == "gauche")
        self.assertGreater(g["ic_bas"], 2)
        tests = R6.appliquer_holm_fixe(lignes, "F2", 10)
        self.assertFalse(next(x for x in tests if x is g)["retenu"])

    def test_h2_permute_numerateur_moins_deux_denominateurs(self):
        modele = R6.FERMES[0]
        ident = pd.DataFrame({"modele": [modele] * 3, "camp": ["gauche"] * 3,
                              "item": range(3), "tv_entre_identites": [.3, .4, .5],
                              "tv_plancher_w1_w2": [.1, .15, .2]})
        vus = []
        with patch.object(R6.R1, "p_permutation_signe",
                          side_effect=lambda d, _rng, _n: vus.append(np.asarray(d)) or .5):
            R6.tests_h2(ident, {modele: .01}, np.random.default_rng(5), 30, 19)
        np.testing.assert_allclose(vus[0], [.1, .1, .1])

    def test_h4_exploratoire_rapporte_t_et_ic_sans_inference(self):
        items = [f"i{i}" for i in range(8)]
        haut, bas = R6.PAIRES_H4[0]
        lignes = []
        for modele, facteur in ((haut, 1.0), (bas, .5)):
            for i, item in enumerate(items, 1):
                lignes.append({"modele": modele, "identite": "journaliste", "item": item,
                               "gap_signe_decrit": facteur * i / 10,
                               "gap_signe_reel_w1": i / 10})
        d = R6.h4_exploratoire(pd.DataFrame(lignes), set(items),
                               np.random.default_rng(6), 80, set(R6.FERMES))
        self.assertEqual(d.iloc[0]["statut"], "EXPLORATOIRE")
        self.assertAlmostEqual(d.iloc[0]["a2_haute"], 1.0)
        self.assertAlmostEqual(d.iloc[0]["a2_economique"], .5)
        self.assertAlmostEqual(d.iloc[0]["T"], abs(1.0 - 1.009) - abs(.5 - 1.009))
        self.assertLessEqual(d.iloc[0]["ic_bas"], d.iloc[0]["ic_haut"])
        self.assertEqual(d.iloc[0]["reference"], R6.REFERENCE_ADDENDUM)
        self.assertNotIn("p", d.columns)
        self.assertNotIn("p_holm", d.columns)
        self.assertNotIn("significatif", d.columns)
        self.assertNotIn("verdict", d.columns)

    def test_h4_perimetre_asymetrique_compte_seulement_les_items_communs(self):
        haut, bas = R6.PAIRES_H4[0]
        lignes = []
        for modele, items in ((haut, range(8)), (bas, range(3, 8))):
            for i in items:
                lignes.append({"modele": modele, "identite": "journaliste", "item": f"i{i}",
                               "gap_signe_decrit": (i + 1) / 10,
                               "gap_signe_reel_w1": (i + 1) / 10})
        d = R6.h4_exploratoire(pd.DataFrame(lignes), {f"i{i}" for i in range(8)},
                               np.random.default_rng(7), 40, set(R6.FERMES))
        self.assertEqual(d.iloc[0]["n_items"], 5)

    def test_h4_est_reproductible_a_graine_identique(self):
        haut, bas = R6.PAIRES_H4[0]
        lignes = [{"modele": modele, "identite": "journaliste", "item": f"i{i}",
                   "gap_signe_decrit": facteur * (i + 1) / 10,
                   "gap_signe_reel_w1": (i + 1) / 10}
                  for modele, facteur in ((haut, 1.1), (bas, .7)) for i in range(8)]
        args = (pd.DataFrame(lignes), {f"i{i}" for i in range(8)})
        a = R6.h4_exploratoire(*args, np.random.default_rng(8), 80, set(R6.FERMES))
        b = R6.h4_exploratoire(*args, np.random.default_rng(8), 80, set(R6.FERMES))
        pd.testing.assert_frame_equal(a, b)

    def test_h4_deuxieme_paire_seulement_si_sonnet_est_joue(self):
        lignes = []
        for modele, facteur in ((haut, facteur) for (haut, _bas), facteur in
                                zip(R6.PAIRES_H4, (1.0, 1.1))):
            for i in range(4):
                lignes.append({"modele": modele, "identite": "journaliste", "item": f"i{i}",
                               "gap_signe_decrit": facteur * (i + 1) / 10,
                               "gap_signe_reel_w1": (i + 1) / 10})
        for modele in (R6.PAIRES_H4[0][1], R6.PAIRES_H4[1][1]):
            for i in range(4):
                lignes.append({"modele": modele, "identite": "journaliste", "item": f"i{i}",
                               "gap_signe_decrit": .8 * (i + 1) / 10,
                               "gap_signe_reel_w1": (i + 1) / 10})
        e = pd.DataFrame(lignes)
        sans = R6.h4_exploratoire(e, {f"i{i}" for i in range(4)},
                                     np.random.default_rng(9), 30, set(R6.FERMES))
        avec = R6.h4_exploratoire(e, {f"i{i}" for i in range(4)},
                                     np.random.default_rng(9), 30,
                                     set(R6.FERMES) | {R6.SONNET})
        self.assertEqual(len(sans), 1)
        self.assertEqual(len(avec), 2)
        self.assertEqual(avec.iloc[1]["condition_haute"], R6.SONNET)

    def test_h4_sans_tirage_fini_ne_calcule_pas_de_percentile(self):
        class TiragesDenominateurNul:
            def integers(self, _low, _high, size):
                return np.tile([0, 1, 0, 1], (size[0], 1))
        haut, bas = R6.PAIRES_H4[0]
        reels = [1., -1., 1., 1.]
        lignes = [{"modele": modele, "identite": "journaliste", "item": f"i{i}",
                   "gap_signe_decrit": facteur * reels[i], "gap_signe_reel_w1": reels[i]}
                  for modele, facteur in ((haut, 1.0), (bas, .5)) for i in range(4)]
        d = R6.h4_exploratoire(pd.DataFrame(lignes), {f"i{i}" for i in range(4)},
                               TiragesDenominateurNul(), 20, set(R6.FERMES))
        self.assertEqual(d.iloc[0]["statut"], "INDISPONIBLE")
        self.assertTrue(np.isnan(d.iloc[0]["ic_bas"]))
        self.assertTrue(np.isnan(d.iloc[0]["ic_haut"]))

    def test_descriptifs_ouverts_restent_sans_p(self):
        cel = pd.DataFrame({"modele": ["modele-ouvert"] * 3, "camp": ["gauche"] * 3,
                            "identite": ["journaliste"] * 3, "rejet": [False] * 3,
                            "gs_decrit": [.2, .3, .4], "gs_reel_w1": [.1, .2, .3]})
        d = R6.descriptifs(cel, pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), set(), 40)
        self.assertEqual(d.iloc[0]["modele"], "modele-ouvert")
        self.assertTrue(d["p"].isna().all())


class R6ChargementTests(unittest.TestCase):
    def _ligne(self, modele, cle, item="i0"):
        return {"version_prompt": R6.CLIENT.FORMATS["q4"], "format": "q4",
                "modele": modele, "cle_modele": cle, "gabarit": R6.CLIENT.GABARIT,
                "item": item, "camp": "gauche", "identite": "journaliste",
                "n_tentatives": 1, "sans_relance": True, "erreur": None,
                "rejet": False, "distribution": {"A": .5, "B": .5},
                "fournisseur": "mock", "quantification": "mock",
                "configuration": {"raisonnement": "off", "max_tokens": 150}}

    def _ecrire(self, base, lignes, suffixe="test"):
        modele = R6.FERMES[0]
        cle = R6.CLIENT.cle_run(modele, "q4", suffixe)
        trace = base / f"r6-{cle}.jsonl"
        trace.write_text("\n".join(json.dumps(x) for x in lignes) + "\n", encoding="utf-8")
        manifeste = base / "analyse.json"
        manifeste.write_text(json.dumps({"version": "R6-evaluation-1", "traces": [{
            "modele": modele, "format": "q4", "passe": "campagne",
            "suffixe": suffixe, "chemin": trace.name,
            "configuration": {"raisonnement": "off", "max_tokens": 150}}]}),
            encoding="utf-8")
        return manifeste, modele, cle, trace

    def test_chargeur_accepte_un_sous_plan_ordonne(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            modele = R6.FERMES[0]
            cle = R6.CLIENT.cle_run(modele, "q4", "test")
            manifeste, _, _, _ = self._ecrire(base, [self._ligne(modele, cle)])
            groupes = R6.charger_traces(manifeste, [("i0", True), ("i1", True)])
            self.assertEqual(len(groupes[(modele, "q4", "campagne")]), 1)

    def test_chargeur_refuse_json_doublon_configuration_et_nom(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            modele = R6.FERMES[0]
            cle = R6.CLIENT.cle_run(modele, "q4", "test")
            ligne = self._ligne(modele, cle)
            manifeste, _, _, trace = self._ecrire(base, [ligne, ligne])
            with self.assertRaisesRegex(RuntimeError, "dupliquee"):
                R6.charger_traces(manifeste, [("i0", True)])
            trace.write_text('{"x":', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "JSON invalide"):
                R6.charger_traces(manifeste, [("i0", True)])
            mauvaise = dict(ligne, gabarit="autre")
            trace.write_text(json.dumps(mauvaise) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "configuration incompatible"):
                R6.charger_traces(manifeste, [("i0", True)])
            mauvaise = dict(ligne, configuration={"raisonnement": "low", "max_tokens": 150})
            trace.write_text(json.dumps(mauvaise) + "\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "configuration incompatible au manifeste"):
                R6.charger_traces(manifeste, [("i0", True)])
            contenu = json.loads(manifeste.read_text())
            contenu["traces"][0]["suffixe"] = "autre"
            manifeste.write_text(json.dumps(contenu), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "nom de trace incompatible"):
                R6.charger_traces(manifeste, [("i0", True)])

    def test_rejeu_429_prouve_peut_venir_plus_tard_jamais_plus_tot(self):
        modele = R6.FERMES[0]
        cle = R6.CLIENT.cle_run(modele, "q4", "test")
        plan = [("i0", True), ("i1", True), ("i2", True)]
        marque = {"statut": "non_facture", "fichier_preuve": "r6-preuve-429-x.json"}

        def ligne(item, rapprochement=None):
            d = self._ligne(modele, cle, item)
            if rapprochement is not None:
                d["rapprochement_429"] = rapprochement
            return d

        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            # Rejeu automatique décalé en fin de passe : accepté, chaque cellule une fois.
            manifeste, _, _, _ = self._ecrire(base, [ligne("i1"), ligne("i2"), ligne("i0", marque)])
            groupes = R6.charger_traces(manifeste, plan)
            self.assertEqual([x["item"] for x in groupes[(modele, "q4", "campagne")]],
                             ["i1", "i2", "i0"])
            refus = (
                [ligne("i1"), ligne("i2"), ligne("i0")],                     # sans marqueur
                [ligne("i1"), ligne("i2"), ligne("i0", {"statut": "autre"})],  # marqueur invalide
                [ligne("i2", marque), ligne("i0"), ligne("i1")],              # plus tôt que son rang
                [ligne("i1"), ligne("i0", marque), ligne("i0", marque)],      # cellule dupliquée
            )
            for lignes in refus:
                with self.subTest(items=[x["item"] for x in lignes]):
                    manifeste, _, _, _ = self._ecrire(base, lignes)
                    with self.assertRaisesRegex(RuntimeError, "ordre incompatible|dupliquee"):
                        R6.charger_traces(manifeste, plan)

    def test_controle_connait_les_quotites_des_passes(self):
        modele = R6.FERMES[0]
        groupes = {(modele, "q4", "plancher"): [{}],
                   (modele, "q4", "essai-1"): [{}] * 10}
        d = R6.controles(groupes).set_index("passe")
        self.assertEqual(d.at["plancher", "cellules_attendues"], 40)
        self.assertEqual(d.at["plancher", "statut"], "PARTIEL")
        self.assertEqual(d.at["essai-1", "cellules_attendues"], 10)
        self.assertEqual(d.at["essai-1", "statut"], "PASSE")

    def test_camp_ignore_declenche_le_refus_prescrit(self):
        trace = []
        for i in range(5):
            for camp in ("gauche", "droite"):
                trace.append({"item": f"i{i}", "camp": camp, "identite": "journaliste",
                              "rejet": False, "n_modalites": 2,
                              "distribution": {"A": .4, "B": .6}})
        modele = R6.FERMES[0]
        d = R6.controles({(modele, "q4", "campagne"): trace}).iloc[0]
        self.assertEqual(d["part_camp_constant"], 1.0)
        self.assertEqual(d["statut"], "REFUS_H1_H2")


class R6HistoriqueLocalTests(unittest.TestCase):
    def test_estimateur_r1_retrouve_une_ligne_r4(self):
        racine = Path(__file__).resolve().parent.parent
        e = pd.read_csv(racine / "resultats/r1-par-item-ecarts-r4.csv")
        o = pd.read_csv(racine / "resultats/a37-orientation-items.csv")
        items = set(o.loc[o["oriente"].astype(bool), "item"])
        g = e[(e["cle_modele"] == "q4") & (e["identite"] == "journaliste") &
              e["item"].isin(items)]
        facteur, *_ = R6.R1.ic_ratio_des_moyennes(
            g["gap_signe_decrit"], g["gap_signe_reel_w1"], np.random.default_rng(4), 40)
        publie = pd.read_csv(racine / "resultats/r1-h2-ecart-r4.csv")
        r = publie[(publie["cle_modele"] == "q4") &
                   (publie["identite"] == "journaliste") &
                   (publie["perimetre"] == "79 items orientes")].iloc[0]
        self.assertAlmostEqual(facteur, r["facteur"], places=12)

    def test_controles_bloquants_passent_sur_referent_historique(self):
        orientation = pd.read_csv(R6.RESULTATS / "a37-orientation-items.csv")
        ref, _options, effectifs = R6.R1.lire_referent()
        sens = dict(zip(orientation["item"], orientation["sens_codeur_A"]))
        d = R6.controles_entrees_bloquants(orientation, ref, effectifs, sens)
        self.assertEqual(d["controle"].tolist(),
                         ["items", "items orientes", "effectifs", "plancher humain w2/w1"])
        self.assertTrue(d["statut"].eq("PASSE").all())


if __name__ == "__main__":
    unittest.main()
