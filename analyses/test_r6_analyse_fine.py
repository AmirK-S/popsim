"""Tests entièrement synthétiques du chargeur d'analyse fine R6.

Ils n'ouvrent jamais une trace de campagne : chaque source est créée dans un répertoire
temporaire et toutes les écritures sont locales.
"""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

import r6_analyse_fine as FINE
import r6_oracle_distant as R6


def empreinte(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ecrire_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def ecrire_jsonl(path, rows):
    path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                    encoding="utf-8")


class AnalyseFineFixture:
    """Campagne complète factice : 894 F1, 316 F2, 40 plancher et pilote hors entrée."""
    def __init__(self, directory, model="fixture/deepseek", provider="fixture-provider",
                 marker=True, pilot=True, items=None):
        self.base = Path(directory)
        self.model, self.provider = model, provider
        self.marker, self.pilot = marker, pilot
        self.items = list(items) if items is not None else [f"i{i:03d}" for i in range(149)]
        self.oriented = set(self.items[:79])
        self.configuration = {"raisonnement": "off", "max_tokens": 150}
        self._sources()
        self.expected = FINE._attendus(self.items, self.oriented, self.floor_cells)
        self._ledger()
        self._traces()
        self.manifest = self._manifest()

    def _sources(self):
        orientation = self.base / "orientation.csv"
        pd.DataFrame({
            "item": self.items,
            "oriente": [item in self.oriented for item in self.items],
            "sens_codeur_A": [1 if item in self.oriented else 0 for item in self.items],
        }).to_csv(orientation, index=False)
        self.orientation = orientation

        rows = []
        for item in self.items:
            for camp, probs in (("gauche", (.62, .38)), ("centre", (.50, .50)),
                                ("droite", (.38, .62))):
                for vague in ("w1", "w2"):
                    for rank, (modalite, p) in enumerate(zip(("A", "B"), probs), 1):
                        rows.append({"item": item, "camp": camp, "vague": vague,
                                     "rang": rank, "modalite": modalite, "p": p,
                                     "n": 100, "effectif": 100})
        referent = self.base / "referent.csv"
        pd.DataFrame(rows).to_csv(referent, index=False)
        self.referent = referent

        self.floor_cells = list(R6.R1.cellules(self.items, ["gauche", "centre", "droite"],
                                                list(R6.R1.IDENTITES)))[:40]
        floor = self.base / "floor.tsv"
        with floor.open("w", encoding="utf-8") as handle:
            for camp, identity, item in self.floor_cells:
                handle.write(f"{item}\t{camp}\t{identity}\n")
        self.floor = floor

    def _ledger(self):
        rows = [{"type": "initialisation"}, {"type": "import-complet"}]
        for passe, fmt, _ in FINE.PASSES_ANALYSE:
            for camp, identity, item in self.expected[(passe, fmt)]:
                ident = R6.identite_campagne(self.model, fmt, R6.FORMATS[fmt], item, camp,
                                              identity, passe)
                rows.extend(({"type": "reservation", "identite": ident, "usd": "0.0001",
                              "empreinte_requete": self._empreinte_requete(ident),
                              "fournisseur_impose": self.provider},
                             {"type": "reconciliation", "identite": ident, "usd": "0.00001",
                              "preuve": "fixture"}))
        if self.pilot:
            ident = R6.identite_campagne(self.model, "q4", R6.FORMATS["q4"], self.items[0],
                                          "gauche", "journaliste", "essai-1")
            rows.extend(({"type": "reservation", "identite": ident, "usd": "0.001",
                          "empreinte_requete": self._empreinte_requete(ident),
                          "fournisseur_impose": self.provider},
                         {"type": "reconciliation", "identite": ident, "usd": "0.00001",
                          "preuve": "pilot fixture"}))
        ledger = self.base / "ledger.jsonl"
        ecrire_jsonl(ledger, rows)
        self.ledger = ledger

    @staticmethod
    def _empreinte_requete(ident):
        return hashlib.sha256(ident.encode("utf-8")).hexdigest()

    def _row(self, passe, fmt, cell, n):
        camp, identity, item = cell
        ident = R6.identite_campagne(self.model, fmt, R6.FORMATS[fmt], item, camp, identity,
                                     passe)
        # Le pilote a une distribution extrême mais il n'est jamais écrit dans les traces
        # admises par le manifeste d'analyse.
        shift = ((n % 7) - 3) * .01
        if camp == "gauche":
            p = [.65 + shift, .35 - shift]
        elif camp == "droite":
            p = [.35 + shift, .65 - shift]
        else:
            p = [.50 + shift, .50 - shift]
        if identity == "adversaire":
            p = [p[0] - .02, p[1] + .02]
        return {"modele": self.model, "cle_modele": f"fixture-{fmt}", "format": fmt,
                "version_prompt": R6.FORMATS[fmt], "gabarit": R6.GABARIT,
                "item": item, "camp": camp, "identite": identity,
                "famille": "famille-A" if self.items.index(item) % 2 else "famille-B",
                "n_modalites": 2, "n_tentatives": 1, "sans_relance": True,
                "erreur": None, "rejet": False, "motif_rejet": "",
                "distribution": {"A": p[0], "B": p[1]}, "fournisseur": self.provider,
                "quantification": self.provider, "fournisseur_impose": self.provider,
                "empreinte_requete": self._empreinte_requete(ident),
                "configuration": self.configuration, "passe": passe}

    def _traces(self):
        self.trace_paths = {}
        for passe, fmt, _ in FINE.PASSES_ANALYSE:
            path = self.base / f"{passe}-{fmt}.jsonl"
            ecrire_jsonl(path, [self._row(passe, fmt, c, no) for no, c in
                               enumerate(self.expected[(passe, fmt)])])
            self.trace_paths[(passe, fmt)] = path

    def _spec(self, path):
        return {"path": path.name, "sha256": empreinte(path)}

    def _manifest(self):
        model = {"model": self.model, "provider": self.provider, "terminal": "TERMINE",
                 "analysis_role": "descriptif", "non_deterministe": self.marker,
                 "floor_cells": self._spec(self.floor), "ledger": self._spec(self.ledger),
                 "traces": [dict(self._spec(self.trace_paths[(passe, fmt)]), passe=passe,
                                  format=fmt, configuration=self.configuration)
                            for passe, fmt, _ in FINE.PASSES_ANALYSE]}
        manifest = self.base / "analyse-fine.json"
        ecrire_json(manifest, {"version": "R6-analyse-fine-1",
                               "orientation": self._spec(self.orientation),
                               "referent": self._spec(self.referent), "models": [model]})
        return manifest

    def rewrite_manifest(self, value):
        ecrire_json(self.manifest, value)

    def read_manifest(self):
        return json.loads(self.manifest.read_text(encoding="utf-8"))


def lire_jsonl(path):
    return [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]


def sceller_ledger(fixture, rows):
    ecrire_jsonl(fixture.ledger, rows)
    manifest = fixture.read_manifest()
    manifest["models"][0]["ledger"]["sha256"] = empreinte(fixture.ledger)
    fixture.rewrite_manifest(manifest)


def sceller_trace(fixture, key, rows):
    path = fixture.trace_paths[key]
    ecrire_jsonl(path, rows)
    manifest = fixture.read_manifest()
    index = [(p, f) for p, f, _ in FINE.PASSES_ANALYSE].index(key)
    manifest["models"][0]["traces"][index]["sha256"] = empreinte(path)
    fixture.rewrite_manifest(manifest)


def identite_f1(fixture, cell):
    camp, identity, item = cell
    return R6.identite_campagne(fixture.model, "q4", R6.FORMATS["q4"], item, camp, identity)


def rejouer(rows, ident, preuves, apres=None):
    """Réservation -> annulation(s) -> réservation -> réconciliation pour une identité.

    ``apres`` : identité après la réconciliation de laquelle placer le rejeu (décalé).
    """
    i = next(n for n, r in enumerate(rows) if r.get("identite") == ident)
    reservation, reconciliation = rows[i], rows[i + 1]
    tete = [x for preuve in preuves for x in (
        dict(reservation), {"type": "annulation", "identite": ident, "usd": "0", "preuve": preuve})]
    reste = rows[:i] + tete + rows[i + 2:]
    j = (i + len(tete) if apres is None else
         next(n for n, r in enumerate(reste)
              if r.get("identite") == apres and r["type"] == "reconciliation") + 1)
    return reste[:j] + [dict(reservation), dict(reconciliation)] + reste[j:]


class RejeuxDecalesTests(unittest.TestCase):
    PREUVE_AUTO = "429-non-facture generation_id=gen-x preuve=r6-preuve-429-x.json"

    def _tables(self, manifest):
        return FINE.analyser(*FINE.charger_campagnes(manifest))

    def test_rejeux_manuels_fucitzn_colhomo_a_leur_position(self):
        items = [f"i{i:03d}" for i in range(149)]
        items[5], items[6] = "fucitzn", "colhomo"
        textes = list(FINE.PREUVES_429_MANUELLES)
        with tempfile.TemporaryDirectory() as ref_dir, tempfile.TemporaryDirectory() as directory:
            reference = AnalyseFineFixture(ref_dir, model="deepseek/deepseek-v4-flash", items=items)
            fixture = AnalyseFineFixture(directory, model="deepseek/deepseek-v4-flash", items=items)
            rows = lire_jsonl(fixture.ledger)
            fucitzn = identite_f1(fixture, ("gauche", "journaliste", "fucitzn"))
            colhomo = identite_f1(fixture, ("gauche", "adversaire", "colhomo"))
            rows = rejouer(rows, fucitzn, textes[:2])
            rows = rejouer(rows, colhomo, textes[2:])
            sceller_ledger(fixture, rows)
            campaigns, _ = FINE.charger_campagnes(fixture.manifest)
            self.assertEqual(len(campaigns[0].operations_reglees), 1250)
            self.assertEqual(len({op["identite"] for op in campaigns[0].operations_reglees}), 1250)
            attendu, obtenu = self._tables(reference.manifest), self._tables(fixture.manifest)
            self.assertEqual(set(attendu), set(obtenu))
            for name in attendu:
                pd.testing.assert_frame_equal(attendu[name], obtenu[name])

    def test_rejeu_automatique_decale_en_fin_de_passe(self):
        with tempfile.TemporaryDirectory() as ref_dir, tempfile.TemporaryDirectory() as directory:
            reference = AnalyseFineFixture(ref_dir)
            fixture = AnalyseFineFixture(directory)
            f1 = fixture.expected[("campagne", "q4")]
            rows = rejouer(lire_jsonl(fixture.ledger), identite_f1(fixture, f1[10]),
                           [self.PREUVE_AUTO], apres=identite_f1(fixture, f1[-1]))
            sceller_ledger(fixture, rows)
            trace = lire_jsonl(fixture.trace_paths[("campagne", "q4")])
            ligne = trace.pop(10)
            ligne["rapprochement_429"] = {"statut": "non_facture",
                                          "fichier_preuve": "r6-preuve-429-x.json"}
            sceller_trace(fixture, ("campagne", "q4"), trace + [ligne])
            campaigns, _ = FINE.charger_campagnes(fixture.manifest)
            self.assertEqual(len(campaigns[0].operations_reglees), 1250)
            self.assertEqual(len(campaigns[0].traces[("campagne", "q4")]), 894)
            attendu, obtenu = self._tables(reference.manifest), self._tables(fixture.manifest)
            pd.testing.assert_frame_equal(attendu["r6-analyse-fine-couverture"],
                                          obtenu["r6-analyse-fine-couverture"])
            cles = ["modele", "format", "quantite", "camp", "identite", "item"]
            a, b = (t["r6-analyse-fine-par-item"].sort_values(cles).reset_index(drop=True)
                    for t in (attendu, obtenu))
            pd.testing.assert_frame_equal(a, b, check_exact=False)

    def test_refus_rejeu_sans_preuve_429_trois_annulations_et_empreinte(self):
        cas = (
            ("sans preuve 429", ["HTTP-404-sans-generation"], None),
            # Texte manuel exact, mais sur une identité autre que celle du registre.
            ("sans preuve 429", [next(iter(FINE.PREUVES_429_MANUELLES))], None),
            ("sans preuve 429", [self.PREUVE_AUTO, "rapprochement manuel"], None),
            ("plus de 2 annulations", [self.PREUVE_AUTO] * 3, None),
            ("empreinte ou de fournisseur", [self.PREUVE_AUTO], "empreinte_requete"),
            ("empreinte ou de fournisseur", [self.PREUVE_AUTO], "fournisseur_impose"),
        )
        for motif, preuves, champ in cas:
            with self.subTest(motif=motif, preuves=preuves, champ=champ), \
                    tempfile.TemporaryDirectory() as directory:
                fixture = AnalyseFineFixture(directory)
                ident = identite_f1(fixture, fixture.expected[("campagne", "q4")][10])
                rows = rejouer(lire_jsonl(fixture.ledger), ident, preuves)
                if champ:
                    derniere = max(n for n, r in enumerate(rows)
                                   if r.get("identite") == ident and r["type"] == "reservation")
                    rows[derniere][champ] = "autre"
                sceller_ledger(fixture, rows)
                with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, motif):
                    FINE.charger_campagnes(fixture.manifest)

    def test_refus_reservation_rejouee_ouverte(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            ident = identite_f1(fixture, fixture.expected[("campagne", "q4")][10])
            rows = rejouer(lire_jsonl(fixture.ledger), ident, [self.PREUVE_AUTO])
            fin = max(n for n, r in enumerate(rows) if r.get("identite") == ident)
            self.assertEqual(rows[fin]["type"], "reconciliation")
            del rows[fin]
            sceller_ledger(fixture, rows)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "1 250 opérations"):
                FINE.charger_campagnes(fixture.manifest)

    def test_refus_cellule_plus_tot_que_son_rang(self):
        # Trace : rejeu prouvé au ledger, mais la ligne arrive avant des cellules qui la
        # précèdent dans le plan.
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            f1 = fixture.expected[("campagne", "q4")]
            rows = rejouer(lire_jsonl(fixture.ledger), identite_f1(fixture, f1[10]),
                           [self.PREUVE_AUTO], apres=identite_f1(fixture, f1[-1]))
            sceller_ledger(fixture, rows)
            trace = lire_jsonl(fixture.trace_paths[("campagne", "q4")])
            trace.insert(5, trace.pop(10))
            sceller_trace(fixture, ("campagne", "q4"), trace)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "ordre exact ou unicité"):
                FINE.charger_campagnes(fixture.manifest)

        # Ledger : toute la suite de rejeu placée avant son rang de plan.
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            f1 = fixture.expected[("campagne", "q4")]
            ident = identite_f1(fixture, f1[10])
            rows = rejouer(lire_jsonl(fixture.ledger), ident, [self.PREUVE_AUTO])
            bloc = [r for r in rows if r.get("identite") == ident]
            rows = [r for r in rows if r.get("identite") != ident]
            i = next(n for n, r in enumerate(rows) if r.get("identite") == identite_f1(fixture, f1[5]))
            sceller_ledger(fixture, rows[:i] + bloc + rows[i:])
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "ordre exact F1/F2/plancher"):
                FINE.charger_campagnes(fixture.manifest)

        # Trace décalée sans aucun rejeu au ledger : l'ordre strict s'applique.
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            trace = lire_jsonl(fixture.trace_paths[("campagne", "q4")])
            ligne = trace.pop(10)
            ligne["rapprochement_429"] = {"statut": "non_facture", "fichier_preuve": "x.json"}
            sceller_trace(fixture, ("campagne", "q4"), trace + [ligne])
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "ordre exact ou unicité"):
                FINE.charger_campagnes(fixture.manifest)


class AnalyseFineTests(unittest.TestCase):
    def test_chargeur_terminal_exclut_pilote_et_sorties_restent_exploratoires(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory, model="fixture/deepseek", marker=True, pilot=True)
            campaigns, context = FINE.charger_campagnes(fixture.manifest)
            self.assertEqual(len(campaigns), 1)
            self.assertEqual(len(campaigns[0].operations_reglees), 1250)
            self.assertTrue(campaigns[0].non_deterministe)
            tables = FINE.analyser(campaigns, context)
            coverage = tables["r6-analyse-fine-couverture"]
            self.assertEqual(coverage["cellules"].sum(), 1250)
            self.assertTrue((coverage["pilotes_inclus"] == 0).all())
            self.assertTrue((coverage["operations_reglees_campagne"] == 1250).all())
            self.assertNotIn("centre", {r["camp"] for r in campaigns[0].traces[("campagne", "q4gab3")]})
            self.assertTrue(tables["r6-analyse-fine-stabilite"].iloc[0]["non_deterministe"])
            for table in tables.values():
                self.assertFalse(any(c in table.columns for c in ("p", "p_holm", "ic_bas", "ic_haut", "verdict")))

    def test_garde_ledger_refuse_incomplet_avant_ouverture_trace(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            rows = fixture.ledger.read_text(encoding="utf-8").splitlines()
            # La dernière opération de campagne devient ambiguë ; les deux lignes pilote
            # restent afin de prouver qu'elles ne servent pas à compléter la campagne.
            del rows[-3]
            fixture.ledger.write_text("\n".join(rows) + "\n", encoding="utf-8")
            # Une trace invalide avec une empreinte mise à jour ne doit pas être ouverte :
            # l'échec terminal du ledger a nécessairement priorité.
            target = fixture.trace_paths[("campagne", "q4")]
            target.write_text("pas-du-json\n", encoding="utf-8")
            manifest = fixture.read_manifest()
            model = manifest["models"][0]
            model["ledger"]["sha256"] = empreinte(fixture.ledger)
            model["traces"][0]["sha256"] = empreinte(target)
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "1 250 opérations"):
                FINE.charger_campagnes(fixture.manifest)

    def test_ordre_ledger_et_trace_f2_sans_centre_sont_bloquants(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            rows = [json.loads(x) for x in fixture.ledger.read_text(encoding="utf-8").splitlines()]
            # Échange deux opérations F1 complètes : même volume, ordre protocolaire faux.
            rows[2:4], rows[4:6] = rows[4:6], rows[2:4]
            ecrire_jsonl(fixture.ledger, rows)
            manifest = fixture.read_manifest()
            manifest["models"][0]["ledger"]["sha256"] = empreinte(fixture.ledger)
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "ordre exact"):
                FINE.charger_campagnes(fixture.manifest)

        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            path = fixture.trace_paths[("campagne", "q4gab3")]
            rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
            rows[0]["camp"] = "centre"
            ecrire_jsonl(path, rows)
            manifest = fixture.read_manifest()
            manifest["models"][0]["traces"][1]["sha256"] = empreinte(path)
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "ordre exact"):
                FINE.charger_campagnes(fixture.manifest)

    def test_pilote_dans_manifeste_est_refuse(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            manifest = fixture.read_manifest()
            manifest["models"][0]["traces"][2]["passe"] = "essai-1"
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "pilote interdite"):
                FINE.charger_campagnes(fixture.manifest)

    def test_pilote_cache_et_provenance_incomplete_sont_refuses(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            path = fixture.trace_paths[("campagne", "q4")]
            rows = [json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]
            rows[0]["passe"] = "essai-1"
            ecrire_jsonl(path, rows)
            manifest = fixture.read_manifest()
            manifest["models"][0]["traces"][0]["sha256"] = empreinte(path)
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "trace campagne/q4 incohérente"):
                FINE.charger_campagnes(fixture.manifest)

        with tempfile.TemporaryDirectory() as directory:
            fixture = AnalyseFineFixture(directory)
            rows = [json.loads(x) for x in fixture.ledger.read_text(encoding="utf-8").splitlines()]
            del rows[2]["empreinte_requete"]
            ecrire_jsonl(fixture.ledger, rows)
            manifest = fixture.read_manifest()
            manifest["models"][0]["ledger"]["sha256"] = empreinte(fixture.ledger)
            fixture.rewrite_manifest(manifest)
            with self.assertRaisesRegex(FINE.ChargementTerminalRefuse, "provenance ledger"):
                FINE.charger_campagnes(fixture.manifest)

    def test_leave_one_item_et_leave_one_family(self):
        table = pd.DataFrame({"modele": ["m"] * 12, "format": ["q4"] * 12,
                              "identite": ["journaliste"] * 12,
                              "item": [f"i{i}" for i in range(12)],
                              "famille": ["A"] * 6 + ["B"] * 6,
                              "num": np.arange(1, 13, dtype=float),
                              "den": np.ones(12)})
        result = FINE._leaveout(table, ["modele", "format", "identite"], "num", "den", "A2")
        self.assertEqual(set(result["retrait_type"]), {"item", "famille"})
        self.assertEqual(len(result[result["retrait_type"] == "item"]), 12)
        self.assertEqual(len(result[result["retrait_type"] == "famille"]), 2)
        self.assertTrue((result["statut"] == "EXPLORATOIRE").all())

    def test_non_interpretable_strate_et_intermodele_constant(self):
        records = pd.DataFrame({"modele": ["m"] * 4, "format": ["q4"] * 4,
                                "quantite": ["A1"] * 4, "famille": ["A"] * 4,
                                "polarite": [np.nan] * 4, "n_modalites": [2] * 4,
                                "consensus_tercile": ["bas"] * 4,
                                "valeur": [.1, .2, .3, .4]})
        strata = FINE._resumer_strates(records)
        self.assertTrue((strata["statut"] == "NON_INTERPRETABLE").all())
        self.assertTrue(strata["moyenne"].isna().all())
        constant = pd.DataFrame({"camp": ["gauche"] * 5, "identite": ["journaliste"] * 5,
                                 "item": [f"i{i}" for i in range(5)], "rejet": [False] * 5,
                                 "gs_decrit": [.5] * 5, "p_decrit": ["[0.5, 0.5]"] * 5})
        empty = pd.DataFrame(columns=["identite", "item", "gap_signe_decrit"])
        a4 = pd.DataFrame(columns=["camp", "item", "tv_entre_identites"])
        prepared = {name: {"cells_f1": constant.copy(), "cells_f2": constant.copy(),
                           "a2_f1": empty.copy(), "a2_f2": empty.copy(), "a4": a4.copy()}
                    for name in ("deepseek", "grok")}
        inter = FINE._intermodel(prepared)
        self.assertTrue((inter["statut"] == "NON_INTERPRETABLE").all())

    def test_marqueurs_deepseek_et_grok_sont_explicitement_conserves(self):
        f1 = pd.DataFrame({"camp": ["gauche"] * 5, "identite": ["journaliste"] * 5,
                           "item": [f"i{i}" for i in range(5)], "rejet": [False] * 5,
                           "p_decrit": ["[0.5, 0.5]"] * 5, "gs_decrit": [.5] * 5})
        floor = f1.copy()
        for model in ("deepseek/deepseek-v4-flash", "x-ai/grok-4"):
            campaign = FINE.Campagne(model, "provider", "descriptif", True, {}, [])
            result = FINE._stabilite(campaign, f1, floor)
            self.assertTrue(result.iloc[0]["non_deterministe"])
            self.assertEqual(result.iloc[0]["statut"], "EXPLORATOIRE")


if __name__ == "__main__":
    unittest.main()
