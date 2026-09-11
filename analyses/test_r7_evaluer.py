"""Tests hors GPU/reseau de l'evaluateur R7, factices puis historiques locaux."""
import json
from pathlib import Path
import tempfile
import unittest

import numpy as np
import pandas as pd

import r7_evaluer as R7


FACTEURS = {
    "olmo3base": 1.40, "olmo3sft": 0.80,
    "olmo3dpo": 1.00, "olmo3rlvr": 1.10,
}


def tables_factices(n_orientes=79, n_total=149):
    items = [f"item{i:03d}" for i in range(n_total)]
    orientes = set(items[:n_orientes])
    ecarts, cellules = [], []
    for ci, cle in enumerate(R7.ORDRE):
        for identite in ("journaliste", "adversaire"):
            facteur = FACTEURS[cle] + (0.02 if identite == "adversaire" else 0.0)
            for i, item in enumerate(items[:n_orientes]):
                ref = 0.10 + i / 10000
                ecarts.append({
                    "cle_modele": cle, "identite": identite, "item": item,
                    "gap_signe_decrit": facteur * ref, "gap_signe_reel_w1": ref,
                })
        for camp_i, camp in enumerate(("gauche", "centre", "droite")):
            for i, item in enumerate(items):
                reel = 0.35 + (i % 17) / 100
                cellules.append({
                    "cle_modele": cle, "camp": camp, "identite": "journaliste",
                    "item": item, "rejet": False,
                    "gs_decrit": reel * (0.80 + 0.03 * ci + 0.01 * camp_i),
                    "gs_reel_w1": reel,
                })
    return {"cellules": pd.DataFrame(cellules), "ecarts": pd.DataFrame(ecarts)}, orientes


class R7EvaluateurFacticeTests(unittest.TestCase):
    def construire(self, tables=None, orientes=None):
        if tables is None:
            tables, orientes = tables_factices()
        rng = np.random.default_rng(R7.GRAINE)
        lignes = R7.construire(tables, orientes, rng, n_boot=120, n_perm=199)
        return pd.DataFrame(R7.appliquer_holm_fixe(lignes))

    def test_familles_et_orientations_exactes(self):
        d = self.construire()
        self.assertEqual(d.groupby("famille").size().to_dict(), R7.TAILLES_FAMILLES)
        f1 = d[d["famille"] == "F1"].set_index("test")
        self.assertAlmostEqual(f1.loc["olmo3base - olmo3sft", "difference"], 0.60, places=10)
        self.assertAlmostEqual(f1.loc["olmo3sft - olmo3dpo", "difference"], -0.20, places=10)
        self.assertAlmostEqual(f1.loc["olmo3dpo - olmo3rlvr", "difference"], -0.10, places=10)
        f2 = d[d["famille"] == "F2"].set_index("test")
        self.assertAlmostEqual(f2.loc["olmo3base - olmo3rlvr", "difference"], 0.30, places=10)
        self.assertAlmostEqual(f2.loc["olmo3base - olmo3dpo", "difference"], 0.40, places=10)
        self.assertAlmostEqual(f2.loc["olmo3sft - olmo3rlvr", "difference"], -0.30, places=10)

    def test_estimateur_ratio_de_moyennes_pas_moyenne_de_ratios(self):
        rng = np.random.default_rng(1)
        a, b, ref = np.array([1., 9., 2.]), np.array([0., 3., 1.]), np.array([1., 10., 2.])
        fa, fb, difference, *_ = R7.ic_difference_facteurs(a, b, ref, rng, n=50)
        self.assertAlmostEqual(fa, a.mean() / ref.mean())
        self.assertAlmostEqual(fb, b.mean() / ref.mean())
        self.assertAlmostEqual(difference, (a.mean() - b.mean()) / ref.mean())
        self.assertNotAlmostEqual(fa, np.mean(a / ref))

    def test_meme_graine_reproduit_bootstrap_permutations_et_holm(self):
        a = self.construire().sort_values(["famille", "test"]).reset_index(drop=True)
        b = self.construire().sort_values(["famille", "test"]).reset_index(drop=True)
        colonnes = ["estimateur_a", "estimateur_b", "difference", "ic_bas", "ic_haut",
                    "p", "p_holm", "significatif"]
        pd.testing.assert_frame_equal(a[colonnes], b[colonnes], check_exact=True)

    def test_rejets_reduisent_le_perimetre_sans_rendre_collecte_complete_partielle(self):
        tables, orientes = tables_factices()
        item = sorted(orientes)[0]
        e = tables["ecarts"]
        tables["ecarts"] = e[~((e["cle_modele"] == "olmo3sft") &
                                (e["identite"] == "journaliste") & (e["item"] == item))]
        c = tables["cellules"]
        tables["cellules"] = c[~((c["cle_modele"] == "olmo3sft") &
                                  (c["camp"] == "gauche") & (c["item"] == item))]
        d = self.construire(tables, orientes)
        r = d[(d["famille"] == "F1") &
              (d["test"] == "olmo3base - olmo3sft")].iloc[0]
        self.assertEqual(r["n_items"], 78)
        self.assertEqual(r["statut"], "EXECUTE")
        f3 = d[(d["famille"] == "F3") &
               (d["condition_a"] == "olmo3sft")].iloc[0]
        self.assertEqual(f3["n_items"], 78)
        self.assertEqual(f3["statut"], "EXECUTE")
        f5 = d[(d["famille"] == "F5") & (d["condition_a"] == "olmo3sft") &
               (d["camp"] == "gauche")].iloc[0]
        self.assertEqual(f5["n_items"], 148)
        self.assertEqual(f5["statut"], "EXECUTE")

        controles = pd.DataFrame([
            {"condition": cle, "cellules": 894, "statut": "PASSE", "detail": "passe"}
            for cle in R7.ORDRE
        ])
        lignes = R7.appliquer_refus_controles(d.to_dict("records"), controles)
        r = next(x for x in lignes if x["famille"] == "F1" and
                 x["test"] == "olmo3base - olmo3sft")
        self.assertEqual(r["statut"], "EXECUTE")
        self.assertEqual(next(x for x in lignes if x["famille"] == "F3" and
                              x["condition_a"] == "olmo3sft")["statut"], "EXECUTE")
        self.assertEqual(next(x for x in lignes if x["famille"] == "F5" and
                              x["condition_a"] == "olmo3sft" and
                              x["camp"] == "gauche")["statut"], "EXECUTE")

        controles.loc[controles["condition"] == "olmo3sft", "detail"] = "trace incomplete"
        lignes = R7.appliquer_refus_controles(d.to_dict("records"), controles)
        r = next(x for x in lignes if x["famille"] == "F1" and
                 x["test"] == "olmo3base - olmo3sft")
        self.assertEqual(r["statut"], "PARTIEL")

    def test_referent_different_refuse_le_contraste(self):
        tables, orientes = tables_factices()
        e = tables["ecarts"]
        m = ((e["cle_modele"] == "olmo3sft") & (e["identite"] == "journaliste") &
             (e["item"] == sorted(orientes)[0]))
        tables["ecarts"].loc[m, "gap_signe_reel_w1"] += 0.01
        d = self.construire(tables, orientes)
        r = d[(d["famille"] == "F1") &
              (d["test"] == "olmo3base - olmo3sft")].iloc[0]
        self.assertEqual(r["statut"], "REFUSE")
        self.assertIn("referent non identique", r["raison_statut"])

    def test_nan_ne_cree_pas_un_test_sur_des_perimetres_differents(self):
        tables, orientes = tables_factices(n_orientes=3, n_total=3)
        e = tables["ecarts"]
        masque = ((e["cle_modele"] == "olmo3sft") &
                  (e["identite"] == "journaliste") &
                  e["item"].isin(["item000", "item001"]))
        tables["ecarts"].loc[masque, "gap_signe_reel_w1"] = np.nan
        lignes = R7.construire(tables, orientes, np.random.default_rng(3), 20, 19)
        r = next(x for x in lignes if x["famille"] == "F1" and
                 x["test"] == "olmo3base - olmo3sft")
        self.assertEqual(r["statut"], "REFUSE")
        self.assertEqual(r["n_items"], 1)
        self.assertIn("triplets apparies finis", r["raison_statut"])
        f3 = next(x for x in lignes if x["famille"] == "F3" and
                  x["condition_a"] == "olmo3sft")
        self.assertEqual(f3["statut"], "REFUSE")
        self.assertEqual(f3["n_items"], 1)

        c = tables["cellules"]
        masque = ((c["cle_modele"] == "olmo3sft") & (c["camp"] == "gauche") &
                  c["item"].isin(["item000", "item001"]))
        tables["cellules"].loc[masque, "gs_decrit"] = np.nan
        lignes = R7.construire(tables, orientes, np.random.default_rng(3), 20, 19)
        f5 = next(x for x in lignes if x["famille"] == "F5" and
                  x["condition_a"] == "olmo3sft" and x["camp"] == "gauche")
        self.assertEqual(f5["statut"], "REFUSE")
        self.assertEqual(f5["n_items"], 1)

    def test_h4_utilise_deux_signes_negatifs_dans_f1_et_f2(self):
        h = R7.evaluer_hypotheses(self.construire())
        r = h[h["hypothese"] == "H4"].iloc[0]
        self.assertEqual(r["statut"], "EVALUE")
        self.assertTrue(r["satisfaite"])
        self.assertIn("SFT-DPO < 0", r["critere"])

    def test_recopie_k3_exclue_k2_conservee(self):
        tables, _ = tables_factices()
        k3, k2 = R7.R1.repartition_exemple(3), R7.R1.repartition_exemple(2)
        traces = {c: [] for c in R7.ORDRE}
        traces["olmo3base"] = [
            {"camp": "gauche", "identite": "journaliste", "item": "item000",
             "n_modalites": 3, "rejet": False,
             "distribution": {str(i): v / sum(k3) for i, v in enumerate(k3)}},
            {"camp": "gauche", "identite": "journaliste", "item": "item001",
             "n_modalites": 2, "rejet": False,
             "distribution": {str(i): v / sum(k2) for i, v in enumerate(k2)}},
        ]
        filtres, copies = R7.exclure_recopies_r7(tables, traces)
        self.assertIn(("olmo3base", "gauche", "journaliste", "item000"), copies)
        self.assertNotIn(("olmo3base", "gauche", "journaliste", "item001"), copies)
        g = filtres["cellules"]
        self.assertFalse(((g["cle_modele"] == "olmo3base") &
                          (g["camp"] == "gauche") & (g["item"] == "item000")).any())
        self.assertTrue(((g["cle_modele"] == "olmo3base") &
                         (g["camp"] == "gauche") & (g["item"] == "item001")).any())

    def test_sortie_refuse_proprement_sans_entrees(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            contrastes, hypotheses, controles, erreurs = R7.evaluer(
                base / "resultats", base / "traces", n_boot=20, n_perm=19)
            self.assertEqual(len(contrastes), 25)
            self.assertTrue(contrastes["statut"].eq("REFUSE").all())
            self.assertTrue(hypotheses["statut"].eq("INDECIDABLE").all())
            self.assertTrue((controles["statut"] == "REFUS_GLOBAL").any())
            self.assertTrue(erreurs)

    def test_json_corrompu_doublon_desordre_et_configuration_sont_refuses(self):
        items = ["item000", "item001"]
        def ligne(item):
            return {
                "version_prompt": R7.VERSION_PROMPT, "cle_modele": "olmo3base",
                "modele": R7.NOMS_MODELES["olmo3base"], "quantification": "Q8_0",
                "gabarit": R7.GABARIT, "item": item, "camp": "gauche",
                "identite": "journaliste", "sans_relance": True, "n_tentatives": 1,
                "rejet": False, "n_modalites": 2, "distribution": {"A": .5, "B": .5},
            }
        with tempfile.TemporaryDirectory() as d:
            traces = Path(d)
            path = traces / "r1-olmo3base-r7.jsonl"

            path.write_text(json.dumps(ligne("item000")) + "\n", encoding="utf-8")
            self.assertEqual(len(R7.lire_traces(traces, items)["olmo3base"]), 1)

            path.write_text('{"version_prompt":', encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "JSON invalide"):
                R7.lire_traces(traces, items)

            path.write_text("\n".join([json.dumps(ligne("item000")),
                                       json.dumps(ligne("item000"))]), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "doublon"):
                R7.lire_traces(traces, items)

            path.write_text(json.dumps(ligne("item001")), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "ordre/configuration incompatible"):
                R7.lire_traces(traces, items)

            mauvaise = ligne("item000")
            mauvaise["quantification"] = "Q4_K_M"
            path.write_text(json.dumps(mauvaise), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "ordre/configuration incompatible"):
                R7.lire_traces(traces, items)


class R7HistoriqueLocalTests(unittest.TestCase):
    def test_sorties_r1_r4_sont_compatibles_sans_les_modifier(self):
        racine = Path(__file__).resolve().parent.parent
        e = pd.read_csv(racine / "resultats/r1-par-item-ecarts-r4.csv")
        c = pd.read_csv(racine / "resultats/r1-par-cellule-r4.csv")
        self.assertTrue({"cle_modele", "identite", "item", "gap_signe_decrit",
                         "gap_signe_reel_w1"} <= set(e.columns))
        self.assertTrue({"cle_modele", "camp", "identite", "item", "rejet",
                         "gs_decrit", "gs_reel_w1"} <= set(c.columns))
        mapping = {"q4base": "olmo3base", "q4nogab": "olmo3sft",
                   "q4hyb": "olmo3dpo", "q4": "olmo3rlvr"}
        e = e[e["cle_modele"].isin(mapping)].copy()
        e["cle_modele"] = e["cle_modele"].map(mapping)
        o = pd.read_csv(racine / "resultats/a37-orientation-items.csv")
        orientes = set(o.loc[o["oriente"].astype(bool), "item"])
        lignes = R7.contrastes_paires(e, orientes, "F1", "journaliste",
                                      np.random.default_rng(7), 40, 39)
        self.assertEqual(len(lignes), 3)
        self.assertTrue(all(3 <= r["n_items"] <= 79 for r in lignes))

        # Controle numerique contre l'estimation R4 deja publiee, sans la recalculer
        # depuis les traces : q4base - q4nogab vaut -0,161004 sur les 79 items.
        brut = pd.read_csv(racine / "resultats/r1-par-item-ecarts-r4.csv")
        g = brut[(brut["identite"] == "journaliste") & brut["item"].isin(orientes)]
        a = g[g["cle_modele"] == "q4base"].set_index("item")
        b = g[g["cle_modele"] == "q4nogab"].set_index("item")
        communs = sorted(set(a.index) & set(b.index))
        fa, fb, dif, *_ = R7.ic_difference_facteurs(
            a.loc[communs, "gap_signe_decrit"], b.loc[communs, "gap_signe_decrit"],
            a.loc[communs, "gap_signe_reel_w1"], np.random.default_rng(8), n=40)
        publie = pd.read_csv(racine / "resultats/r4b-contraste-h2b.csv")
        r = publie[(publie["condition_a"] == "q4base") &
                   (publie["condition_b"] == "q4nogab") &
                   (publie["identite"] == "journaliste") &
                   (publie["perimetre"] == "79 items orientes")].iloc[0]
        self.assertAlmostEqual(fa, r["facteur_a"], places=12)
        self.assertAlmostEqual(fb, r["facteur_b"], places=12)
        self.assertAlmostEqual(dif, r["difference_de_facteurs"], places=12)


if __name__ == "__main__":
    unittest.main()
