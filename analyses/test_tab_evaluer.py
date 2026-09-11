"""Tests de tab_evaluer, entierement synthetiques.

AUCUNE reponse de Twin n'est lue. Le seul fichier du depot ouvert est la partition
resultats/tab-partition-items.csv, qui ne contient que des metadonnees d'items : les
univers factices sont construits sur ses 108 items, ses 55 unites et ses 14 familles, avec
des reponses humaines et des predictions tirees au hasard ici.

Usage : .venv/bin/python analyses/test_tab_evaluer.py
"""
import copy
import filecmp
import os
import sys
import tempfile
import unittest
from unittest import mock

_ICI = os.path.dirname(os.path.abspath(__file__))
for _p in (os.environ.get("POPSIM_ANALYSES", _ICI), _ICI):   # _ICI finit en tete
    while _p in sys.path:
        sys.path.remove(_p)
    sys.path.insert(0, _p)

import numpy as np          # noqa: E402

import tab_evaluer as E     # noqa: E402
import tab_partition as TP  # noqa: E402

PARTITION = TP.lire_csv(E.PARTITION)
ITEMS = [l["item"] for l in PARTITION]
N_PERSONNES = 900
PARAMS = E.Parametres(n_permutations=10, n_permutations_bootstrap=4, n_bootstrap=40,
                      n_bootstrap_reduit=30, pid_max_s1=600)

X = "JSON Persona - GPT4.1"               # la configuration « bien appariee »
Y = "Text Persona - GPT4.1-mini"          # le gabarit de groupe


class _Garde(Exception):
    """Levee par le faux chargeur brut : la garde a laisse passer."""


# ---------------------------------------------------------------------------
# Univers factices
# ---------------------------------------------------------------------------

def univers(nature="succes", n=N_PERSONNES, graine=7):
    """nature :
      succes : les humains suivent le mode de leur segment S_gra a 90 % sur les items du
               bloc 1, a 50 % ailleurs. Y, gabarit pur, est le plus exact sur tout A qui
               contient le bloc 1 ; X porte la personne (vraie reponse a 65 %) et a une
               perte B plus faible que Y sur les blocs 2 et 3 : X gagne reellement sur B.
      nul    : mode a 90 % partout ; X porte toujours la personne mais perd partout.
      pmm    : comme succes, mais PMM predit la vraie reponse a 95 %.
    """
    rng = np.random.default_rng(graine)
    m = len(PARTITION)
    K = np.array([int(l["n_modalites"]) for l in PARTITION])
    est_ord = np.array([l["type"] == "ligne_matrice" for l in PARTITION])
    k_max = int(K.max())
    val_ord = np.zeros((m, k_max))
    for j in range(m):
        if est_ord[j]:
            val_ord[j, :K[j]] = np.arange(K[j]) / (K[j] - 1)
    bloc = np.array([int(l["bloc_B"]) for l in PARTITION])
    n_seg = 8
    seg = rng.integers(0, n_seg, size=n).astype(np.int32)

    observe = np.ones((n, m), dtype=bool)       # un seul bras par experience
    for exp in sorted({l["experience"] for l in PARTITION if l["experience"]}):
        bras = sorted({l["bras"] for l in PARTITION if l["experience"] == exp})
        choix = rng.integers(0, len(bras), size=n)
        for b_i, b in enumerate(bras):
            cols = [j for j, l in enumerate(PARTITION)
                    if l["experience"] == exp and l["bras"] == b]
            observe[np.ix_(choix != b_i, cols)] = False

    mode = np.stack([rng.integers(0, K) for _ in range(n_seg)])
    # Hors bloc 1, 0,6 et non 0,5 : X y reste le plus exact sans etre un point de levier
    # isole, qui ferait passer le residu maximal a la candidate la moins exacte (L2).
    part_mode = np.where(bloc == 1, 0.9, 0.6) if nature in ("succes", "pmm") \
        else np.full(m, 0.9)

    def autre(base):
        return (base + rng.integers(1, K[None, :], size=base.shape)) % K[None, :]

    mode_i = mode[seg]
    vrai = np.where(rng.random((n, m)) < part_mode[None, :], mode_i, autre(mode_i))
    verite = np.where(observe, vrai, -1).astype(np.int16)

    def gabarit(q):
        alea = rng.integers(0, K[None, :], size=(n, m))
        return np.where(rng.random((n, m)) < q, mode_i, alea).astype(np.int16)

    def personne(a):
        p = np.where(rng.random((n, m)) < a, vrai, autre(vrai))
        return np.where(observe, p, mode_i).astype(np.int16)

    configs = {
        "Demographics Only - GPT4.1-mini": gabarit(0.5),
        X: personne(0.65),
        "Text Persona (Default Temperature) - GPT4.1-mini": gabarit(0.6),
        "Text Persona (Reasoning) - GPT4.1-mini": gabarit(0.7),
        "Text Persona (Repeating Questions) - GPT4.1-mini": gabarit(0.8),
        Y: gabarit(1.0),
        "Text Persona - Gemini-Flash2.5": gabarit(0.4),
        E.JSON_MINI: gabarit(0.75),
        "Persona Summary - GPT4.1-mini": gabarit(0.6),
        "Persona Summary - JSON Persona - GPT4.1-mini": gabarit(0.6),
    }
    pids = np.arange(1, n + 1)
    configs[E.JSON_MINI][pids > PARAMS.pid_max_s1] = -1

    compte = np.stack([np.bincount(verite[observe[:, j], j], minlength=k_max)
                       for j in range(m)])
    marg = compte / compte.sum(axis=1, keepdims=True)
    # Temoin aveugle a la personne, tire une fois par cellule S_gra x item : sa chute est
    # nulle par construction, sans dependre du bruit d'echantillonnage de 900 personnes.
    tirage = np.stack([rng.choice(k_max, size=n_seg, p=marg[j]) for j in range(m)], axis=1)

    def adversaires(decalage):
        return {
            "B0 mode": np.tile(compte.argmax(axis=1), (n, 1)).astype(np.int16),
            "B0 tirage": tirage[seg].astype(np.int16),
            "B1 argmax": gabarit(0.9 - decalage),
            "B2 argmax": gabarit(0.7 - decalage),
            "PMM k=10": personne(0.95 - decalage) if nature == "pmm"
            else gabarit(0.5 - decalage),
        }

    d = {"pids": pids, "items": list(ITEMS), "verite": verite, "configs": configs,
         "adversaires": adversaires(0.0), "adversaires_s6": adversaires(0.2),
         "seg": seg, "val_ord": val_ord, "est_ordinal": est_ord,
         "partition": copy.deepcopy(PARTITION)}
    d["reference_t1"] = {nom: E._exactitude_moyenne(
        configs[nom] if nom in configs else d["adversaires"][nom], verite)
        for nom in E.CANDIDATES_PRINCIPAL + E.ADVERSAIRES}
    return d


_CACHE = {}


def resultat(nature):
    if nature not in _CACHE:
        d = univers(nature)
        _CACHE[nature] = E.executer(chargeur=lambda: d, params=PARAMS, ecrire=False)
    return _CACHE[nature]


# ---------------------------------------------------------------------------
# Regle de chute sur trois univers
# ---------------------------------------------------------------------------

class UniversTests(unittest.TestCase):
    def test_succes_la_regle_conclut_a_la_survie(self):
        r = resultat("succes")
        p = r["principal"]
        self.assertTrue(all(c["passe"] for c in p["controles"]),
                        [c for c in p["controles"] if not c["passe"]])
        self.assertEqual([x["c_diag"] for x in p["rotations"]], [X, X, X])
        # A_1 = B2 + B3 ne contient pas le bloc 1 : X y est aussi le plus exact.
        self.assertEqual([x["c_exa"] for x in p["rotations"]], [X, Y, Y])
        self.assertEqual(p["rotations"][0]["delta_r"], 0.0)
        dec = p["decision"]
        self.assertTrue(dec["R1"] and dec["R2"] and dec["R3"], dec)
        self.assertFalse(dec["R4_ferme"], dec)
        self.assertEqual(dec["statut"], "survit")
        self.assertLessEqual(dec["delta"], E.SEUIL_R1)
        self.assertLess(dec["ic_haut"], 0)
        self.assertEqual(len(p["familles"]), 14)
        self.assertEqual(r["S1"]["decision"]["statut"], "survit")
        self.assertEqual(r["lecture"], "survit")

    def test_nul_la_regle_ferme(self):
        dec = resultat("nul")["principal"]["decision"]
        self.assertEqual(dec["statut"], "ferme")
        self.assertFalse(dec["R1"])
        self.assertFalse(dec["R2"])
        self.assertGreater(dec["delta"], 0)

    def test_pmm_gagne_partout_R4_ferme(self):
        dec = resultat("pmm")["principal"]["decision"]
        self.assertTrue(dec["R1"] and dec["R2"], dec)
        self.assertTrue(dec["R4_ferme"])
        self.assertEqual(dec["statut"], "ferme")
        self.assertTrue(all(a <= b for a, b in zip(dec["perte_B_PMM"],
                                                   dec["perte_B_c_diag"])))

    def test_meme_choix_delta_exactement_nul_et_ferme(self):
        cand = ["a", "b", "c"]
        mes = {c: {"exa_A": np.full(3, e), "chute_A": np.full(3, ch),
                   "perte_B": np.full(3, pb), "perte_A": np.full(3, pb),
                   "exa_B": np.full(3, 1 - pb)}
               for c, e, ch, pb in (("a", 0.4, 0.0, 0.5), ("b", 0.9, 0.6, 0.1),
                                    ("c", 0.8, 0.0, 0.2))}
        delta, rot = E.calculer_delta(mes, cand)
        self.assertEqual([x["c_diag"] for x in rot], ["b"] * 3)
        self.assertEqual([x["c_exa"] for x in rot], ["b"] * 3)
        self.assertEqual(delta, 0.0)
        dec = E.regle_de_chute(delta, -0.5, {"f": {"delta": -1.0}}, [1, 1, 1], [0, 0, 0])
        self.assertFalse(dec["R1"])
        self.assertEqual(dec["statut"], "ferme")

    def test_affaibli_sans_famille_ne_ferme_pas(self):
        fam = {"f1": {"delta": -0.005}, "f2": {"delta": -0.2}}
        dec = E.regle_de_chute(-0.05, -0.01, fam, [1, 1, 1], [0, 0, 0])
        self.assertEqual(dec["statut"], "survit")
        self.assertEqual(dec["affaibli_sans"], ["f1"])
        fam["f3"] = {"delta": 0.0}
        self.assertEqual(E.regle_de_chute(-0.05, -0.01, fam, [1, 1, 1],
                                          [0, 0, 0])["statut"], "ferme")

    def test_secondaires_presentes(self):
        sec = resultat("succes")["secondaires"]
        for s in ("S2", "S3", "S4", "S5", "S6", "S7", "S8"):
            self.assertIn(s, sec)
        self.assertEqual(len(sec["S8"]), 3)
        self.assertEqual(set(sec["S7"]), set(E.DESCRIPTION_SEULE))
        self.assertNotIn("Demographics Only - GPT4.1-mini", sec["S2"]["mesures"])
        self.assertEqual(len(sec["S2"]["rotations"]), 3)


# ---------------------------------------------------------------------------
# S1, controles bloquants
# ---------------------------------------------------------------------------

class PerimetreControlesTests(unittest.TestCase):
    def test_s1_premieres_personnes_huit_configurations(self):
        r = resultat("succes")
        self.assertEqual(r["principal"]["n"], N_PERSONNES)
        self.assertEqual(r["S1"]["n"], PARAMS.pid_max_s1)
        self.assertEqual(r["S1"]["candidates"], E.CANDIDATES_S1)
        self.assertIn(E.JSON_MINI, r["S1"]["candidates"])
        self.assertNotIn(E.JSON_MINI, r["principal"]["candidates"])
        np.testing.assert_array_equal(r["S1"]["T"]["lignes"], np.arange(PARAMS.pid_max_s1))
        self.assertEqual(E.PID_MAX_S1, 1000)

    def test_c1_couverture_insuffisante_non_concluant(self):
        d = univers("succes")
        d["configs"]["Text Persona - Gemini-Flash2.5"][: int(0.8 * N_PERSONNES), 0] = -1
        r = E.executer(chargeur=lambda: d, params=PARAMS, ecrire=False)
        self.assertEqual(r["principal"]["decision"]["statut"], "non concluant")
        echecs = {c["controle"] for c in r["principal"]["controles"] if not c["passe"]}
        self.assertIn("C1 couverture minimale d'un item", echecs)
        self.assertNotIn("mesures", r["principal"])          # aucune perte calculee
        self.assertEqual(r["secondaires"], {})

    def test_temoin_qui_chute_non_concluant(self):
        d = univers("succes")
        d["adversaires"]["B0 tirage"] = np.where(d["verite"] >= 0, d["verite"],
                                                 0).astype(np.int16)
        r = E.executer(chargeur=lambda: d, params=PARAMS, ecrire=False)
        self.assertEqual(r["principal"]["decision"]["statut"], "non concluant")
        self.assertTrue(any(c["controle"].startswith("T ") and not c["passe"]
                            for c in r["principal"]["controles"]))

    def test_reproduction_t1_ecart_non_concluant(self):
        d = univers("succes")
        d["reference_t1"][X] += 1e-9
        r = E.executer(chargeur=lambda: d, params=PARAMS, ecrire=False)
        self.assertEqual(r["principal"]["decision"]["statut"], "non concluant")
        ctrl_r = [c for c in r["principal"]["controles"] if c["controle"].startswith("R ")]
        self.assertEqual(len(ctrl_r), 1)
        self.assertFalse(ctrl_r[0]["passe"])
        self.assertEqual(ctrl_r[0]["valeur"], "")            # jamais la valeur


# ---------------------------------------------------------------------------
# Mesures elementaires
# ---------------------------------------------------------------------------

class MesuresTests(unittest.TestCase):
    def test_perte_ordinale_binaire_absente(self):
        val_ord = np.array([[0, 0.5, 1.0], [0, 0, 0]])
        est_ord = np.array([True, False])
        V = np.array([[0, 1], [2, 1]])
        M = np.array([[True, True], [True, False]])
        np.testing.assert_allclose(
            E.matrice_perte(np.array([[2, 2], [-1, 1]]), V, M, est_ord, val_ord),
            [[1.0, 1.0], [1.0, 0.0]])
        np.testing.assert_allclose(
            E.matrice_perte(np.array([[1, 1], [2, 0]]), V, M, est_ord, val_ord),
            [[0.5, 0.0], [0.0, 0.0]])

    def test_exactitude_A_convention_t1(self):
        r = resultat("succes")["principal"]
        T = r["T"]
        struct = E.structure_partition(PARTITION, ITEMS)
        cA, _ = E.colonnes_rotations(struct, np.ones(len(ITEMS), dtype=int))[1]
        attendu = np.nanmean(E.C.exactitude_codes(T["preds"][Y][:, cA], T["Vm"][:, cA]))
        self.assertEqual(r["mesures"][Y]["exa_A"][1], attendu)

    def test_permutation_identites_distinctes(self):
        rng = np.random.default_rng(3)
        seg = np.array([0, 0, 0, 1, 1, 1, 2])
        lignes = np.array([0, 0, 1, 2, 3, 3, 3, 6, 4])
        for p in E.permutations_identites(lignes, seg, 30, rng):
            src = {}
            for copie, s in zip(lignes, p):
                self.assertEqual(src.setdefault(copie, s), s)   # copies identiques
                self.assertEqual(seg[copie], seg[s])            # meme cellule S_gra
            self.assertEqual(sorted(src.values()), sorted(src))  # bijection des distincts
        p0 = E.permutations_identites(np.arange(7), seg, 1, np.random.default_rng(5))[0]
        np.testing.assert_array_equal(
            p0, E.C44.permuter_intra(7, seg, np.random.default_rng(5)))


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------

class BootstrapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.d = univers("succes")
        cls.struct = E.structure_partition(cls.d["partition"], cls.d["items"],
                                           cls.d["est_ordinal"])
        cls.T = E.preparer_tournoi(cls.d, np.arange(N_PERSONNES), E.CANDIDATES_PRINCIPAL,
                                   {})

    def test_chaque_replicat_refait_la_selection(self):
        p = E.Parametres(n_permutations_bootstrap=3, n_bootstrap=6)
        with mock.patch.object(E, "selectionner", wraps=E.selectionner) as espion:
            b = E.bootstrap(self.T, self.struct, E.CANDIDATES_PRINCIPAL, p, "t")
        self.assertEqual(espion.call_count, 6 * 3)
        rng = np.random.default_rng(p.graine_bootstrap)
        tirages = []
        for k in range(3):
            lignes, poids, perms = E.tirer_replicat(rng, self.T, self.struct, 3)
            tirages.append(lignes)
            mes = E.mesurer(self.T, lignes, E.colonnes_rotations(self.struct, poids),
                            E.CANDIDATES_PRINCIPAL, perms)
            delta, rot = E.calculer_delta(mes, E.CANDIDATES_PRINCIPAL)
            self.assertEqual(b["replicats"][k]["delta"], delta)
            for x in rot:
                self.assertEqual(b["replicats"][k][f"c_exa_{x['rotation']}"], x["c_exa"])
                self.assertEqual(b["replicats"][k][f"c_diag_{x['rotation']}"], x["c_diag"])
            for bl in (1, 2, 3):          # autant d'unites que le bloc, et seulement les siennes
                us = self.struct["unites_bloc"][bl]
                self.assertEqual(sum(int(poids[self.struct["unite"] == u][0]) for u in us),
                                 len(us))
        self.assertFalse(np.array_equal(tirages[0], tirages[1]))
        self.assertLess(len(np.unique(tirages[0])), N_PERSONNES)

    def test_selection_suit_les_quantites_du_replicat(self):
        mes = {c: {"exa_A": np.full(3, 0.5), "chute_A": np.zeros(3),
                   "perte_B": np.full(3, 0.5), "perte_A": np.full(3, 0.5),
                   "exa_B": np.full(3, 0.5)} for c in E.CANDIDATES_PRINCIPAL}
        mes[X]["exa_A"] = np.array([0.6, 0.4, 0.5])
        _, rot = E.calculer_delta(mes, E.CANDIDATES_PRINCIPAL)
        self.assertEqual(rot[0]["c_exa"], X)
        self.assertEqual(rot[1]["c_exa"], E.CANDIDATES_PRINCIPAL[0])   # departage §2
        self.assertEqual(rot[2]["c_exa"], E.CANDIDATES_PRINCIPAL[0])

    def test_regle_de_cout(self):
        horloge = iter(np.arange(0, 1e9, 1e5)).__next__
        p = E.Parametres(n_permutations_bootstrap=1, n_bootstrap=24, n_bootstrap_reduit=21,
                         n_replicats_projection=20)
        b = E.bootstrap(self.T, self.struct, E.CANDIDATES_PRINCIPAL, p, "t", horloge)
        self.assertTrue(b["reduit"])
        self.assertEqual(len(b["replicats"]), 21)
        b2 = E.bootstrap(self.T, self.struct, E.CANDIDATES_PRINCIPAL, p, "t")
        self.assertFalse(b2["reduit"])
        self.assertEqual(len(b2["replicats"]), 24)
        self.assertEqual(b["replicats"][5]["delta"], b2["replicats"][5]["delta"])


# ---------------------------------------------------------------------------
# Determinisme, garde, fuite
# ---------------------------------------------------------------------------

class GardeFuiteDeterminismeTests(unittest.TestCase):
    def test_determinisme_a_graine_fixe(self):
        with tempfile.TemporaryDirectory() as t:
            dossiers = []
            for k in range(2):
                s = os.path.join(t, f"run{k}")
                E.executer(chargeur=lambda: univers("succes"), params=PARAMS, sortie=s)
                dossiers.append(s)
            noms = sorted(os.listdir(dossiers[0]))
            self.assertEqual(noms, ["tab-bootstrap.csv", "tab-controles.csv",
                                    "tab-familles.csv", "tab-rotations.csv",
                                    "tab-secondaires.csv"])
            _, diff, err = filecmp.cmpfiles(dossiers[0], dossiers[1], noms, shallow=False)
            self.assertEqual((diff, err), ([], []))

    def test_refus_sans_go_tab(self):
        with tempfile.TemporaryDirectory() as t, \
                mock.patch.object(E, "_charger_twin_brut") as brut:
            with self.assertRaises(E.ErreurGarde):
                E.charger_reel(chemin_go=os.path.join(t, "GO-TAB"))
            with mock.patch.object(E, "GO_TAB", os.path.join(t, "GO-TAB")), \
                    self.assertRaises(E.ErreurGarde):
                E.executer(sortie=t)
            brut.assert_not_called()

    def test_refus_sha_de_partition_faux(self):
        with tempfile.TemporaryDirectory() as t, \
                mock.patch.object(E, "_charger_twin_brut") as brut:
            go = os.path.join(t, "GO-TAB")
            open(go, "w").close()
            faux = os.path.join(t, "partition.csv")
            with open(E.PARTITION, encoding="utf-8") as f:
                contenu = f.read()
            self.assertIn("U55,2", contenu)
            with open(faux, "w", encoding="utf-8") as f:
                f.write(contenu.replace("U55,2", "U55,3"))
            with self.assertRaises(E.ErreurGarde):
                E.charger_reel(chemin_go=go, chemin_partition=faux)
            brut.assert_not_called()

    def test_garde_passe_avec_go_et_bon_sha(self):
        with tempfile.TemporaryDirectory() as t, \
                mock.patch.object(E, "_charger_twin_brut", side_effect=_Garde):
            go = os.path.join(t, "GO-TAB")
            open(go, "w").close()
            with self.assertRaises(_Garde):
                E.charger_reel(chemin_go=go)

    def test_refus_parametres_alleges_et_sortie_sous_data(self):
        with mock.patch.object(E, "charger_reel") as reel:
            with self.assertRaises(E.ErreurGarde):
                E.executer(params=PARAMS, sortie=tempfile.gettempdir())
            with self.assertRaises(E.ErreurGarde):
                E.executer(chargeur=univers, params=PARAMS,
                           sortie=os.path.join(E.RACINE, "data", "tab"))
            reel.assert_not_called()

    def test_fuite_item_de_B_dans_A_refusee(self):
        d = univers("succes")
        fuite = dict(next(l for l in d["partition"] if l["bloc_B"] == "1"))
        fuite["bloc_B"] = "2"
        d["partition"].append(fuite)                     # meme item, dans B1 et dans B2
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(E.ErreurFuite):
                E.executer(chargeur=lambda: d, params=PARAMS, sortie=t)
            self.assertEqual(os.listdir(t), [])

    def test_fuite_unite_coupee_refusee(self):
        part = copy.deepcopy(PARTITION)
        next(l for l in part if l["unite"] == "U01")["bloc_B"] = "2"
        with self.assertRaises(E.ErreurFuite):
            E.structure_partition(part, ITEMS)

    def test_verifier_rotation_refuse_un_chevauchement(self):
        with self.assertRaises(E.ErreurFuite):
            E.verifier_rotation([1, 1, 0], [0, 1, 1])
        E.verifier_rotation([1, 1, 0], [0, 0, 1])


if __name__ == "__main__":
    unittest.main(verbosity=2)
