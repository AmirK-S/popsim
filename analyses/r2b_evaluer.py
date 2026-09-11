"""Evaluation locale de R2b, extension adaptative portant sur 180 personnes.

Refuse une source incomplete ou ambigue. Ne modifie ni R2 ni les traces originales.
Un dossier prive neuf contient l'union ; un dossier de resultats neuf contient uniquement
les tableaux agreges. Le paquet de caches est charge une fois pour R2 et le glissement.
Les p de Holm restent ceux de R2 et ne constituent pas une confirmation independante.
"""
import argparse
import json
import math
import os
import sys
from pathlib import Path
from datetime import datetime

# Limites fixees avant tout import numerique, y compris pour les caches/statistiques.
for _nom in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
             "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS", "BLIS_NUM_THREADS"):
    os.environ[_nom] = "2"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import pandas as pd
import r2_evaluer as R2E
import a41_commun as C41
from threadpoolctl import threadpool_limits, threadpool_info

RACINE = Path(__file__).resolve().parent.parent
TRACES = RACINE / "data" / "traces"
REGISTRE = {"modele": "gpt-oss-20b", "quantification": "MXFP4", "gabarit": "harmony",
            "variante_fin": "answer", "version_prompt": "r2-p1-gptoss-answer"}


def valider_trace(chemin, personnes, items, nomenclature, condition="C3F", registre=None):
    """Exige chaque item unique, pas un compteur de lignes pouvant masquer un trou."""
    pop = personnes.set_index("pid")["pli"].to_dict()
    if len(pop) != len(personnes):
        raise ValueError("personnes dupliquees")
    attendu = set(items)
    vus = {p: set() for p in pop}
    n = 0
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            d = json.loads(ligne)
            pid, item = d["pid"], d["item"]
            if pid not in pop or item not in attendu or item in vus[pid]:
                raise ValueError("cle inconnue ou dupliquee dans la trace")
            if (d.get("condition") != condition or d.get("passe", 1) != 1
                    or d.get("pli") != pop[pid]):
                raise ValueError("condition, passe ou pli incoherent")
            if registre and any(d.get(k) != v for k, v in registre.items()):
                raise ValueError("registre modele ou prompt divergent")
            dist = d.get("distribution")
            if (not isinstance(dist, dict) or not dist
                    or set(dist) != set(nomenclature[item]["options"])
                    or not all(isinstance(v, (float, int)) and math.isfinite(v)
                               and 0 <= v <= 1 for v in dist.values())
                    or abs(sum(dist.values()) - 1) > 1e-6):
                raise ValueError("distribution invalide")
            if (d.get("rejet") or d.get("modalites_absentes")
                    or d.get("argmax") not in dist
                    or dist[d["argmax"]] < max(dist.values()) - 1e-12):
                raise ValueError("rejet, modalite absente ou argmax invalide")
            vus[pid].add(item)
            n += 1
    complets = {p for p, it in vus.items() if it == attendu}
    if len(complets) != len(pop):
        raise ValueError(f"trace incomplete : {len(complets)}/{len(pop)} personnes completes")
    return n


def valider_population(ech0, ech1, paquet):
    for ech, n, par_pli in ((ech0, 150, 30), (ech1, 30, 6)):
        if (len(ech) != n or ech.pid.nunique() != n or ech["index"].nunique() != n
                or ech.groupby("pli").size().to_dict() != {i: par_pli for i in range(5)}):
            raise ValueError("population differente des 150 + 30 prevues")
        for r in ech.itertuples(index=False):
            if paquet["ids"][r.index] != r.pid:
                raise ValueError("index et identifiant incoherents")
    if set(ech0.pid) & set(ech1.pid) or set(ech0["index"]) & set(ech1["index"]):
        raise ValueError("populations non disjointes")


def preparer_dossier(rep, ech0, ech1):
    rep.mkdir(parents=True, exist_ok=False)
    union = pd.concat([ech0, ech1], ignore_index=True).sort_values(["pli", "pid"])
    union.to_csv(rep / "a5-personnes.csv", index=False)
    trace = rep / "r2b-C3F-gptoss-180.jsonl"
    with trace.open("xb") as sortie:
        for nom in ("r2-C3F-gptoss.jsonl", "r2b-C3F-gptoss-ext.jsonl"):
            contenu = (TRACES / nom).read_bytes()
            sortie.write(contenu)
            if contenu and not contenu.endswith(b"\n"):
                sortie.write(b"\n")
    for nom in ("r2-C3-gptoss.jsonl", "a5-C3F-p1.jsonl"):
        if not (TRACES / nom).is_file():
            raise ValueError(f"trace secondaire absente : {nom}")
        (rep / nom).symlink_to(TRACES / nom)
    return union, trace


def glissement_des_cellules(paquet, refs, lignes_150, lignes_180, colonnes):
    """Combien de cellules rares stables entrent et sortent quand on passe a 180 personnes.

    Le seuil de rarete est applique au PERIMETRE, definition declaree de R2 : une modalite
    a 9,8 pour cent sur 150 personnes peut passer a 10,3 pour cent sur 180 et cesser d'etre
    rare. L'ensemble des cellules jugees a 180 n'est donc pas le sur ensemble de celui a
    150, et ce n'est pas un defaut de l'extension, c'est la definition. La quantite est
    mesuree ici pour que le rapport puisse la publier au lieu de la supposer.
    """
    # Le libelle porte l'effectif REELLEMENT complet, jamais l'effectif vise : si le run a
    # ete tronque, un tableau qui annonce 180 alors qu'il en a 152 est un faux.
    out = []
    for nom, lignes in ((f"R2, {len(lignes_150)} personnes", lignes_150),
                        (f"R2b, {len(lignes_180)} personnes", lignes_180)):
        prep = R2E.preparer(paquet, lignes, refs, "perimetre")
        sel = R2E.restreindre(prep["rare_vrai"] & (prep["stab"] == 1), colonnes)
        cells = {(int(lignes[i]), int(j)) for i, j in zip(*np.nonzero(sel))}
        # a8_commun.modalites_minoritaires renvoie UNE LISTE D'ENSEMBLES, un par item :
        # le total compte donc les couples (item, modalite) declares rares, et il change
        # avec le perimetre puisque le seuil de 10 pour cent y est recalcule.
        out.append({"perimetre": nom, "personnes": len(lignes),
                    "cellules_rares_stables": len(cells),
                    "couples_item_modalite_rares": int(sum(len(s) for s in prep["mods"])),
                    "_cells": cells})
    a, b = out[0]["_cells"], out[1]["_cells"]
    commun = a & b
    detail = {
        "cellules_communes": len(commun),
        "cellules_sorties": len(a - b),
        "cellules_entrantes_hors_150": len({c for c in b - a
                                            if c[0] in set(lignes_150.tolist())}),
        "cellules_apportees_par_extension": len({c for c in b
                                                 if c[0] not in set(lignes_150.tolist())}),
    }
    for d in out:
        d.pop("_cells")
        d.update(detail)
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirages", type=int, default=4000)
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--cache-a41", default="/tmp/a41-severe.pkl")
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    ap.add_argument("--travail", type=Path, default=TRACES / "reprise" / f"evaluation-{stamp}")
    ap.add_argument("--sortie", type=Path,
                    default=RACINE / "resultats" / f"r2b-evaluation-{stamp}")
    args = ap.parse_args()
    if args.tirages != 4000 or args.permutations != 200:
        raise SystemExit("Le plan fixe 4000 tirages et 200 permutations ; aucun ajustement apres resultat")
    if args.travail.exists() or args.sortie.exists():
        raise SystemExit("Dossiers deja presents : aucune reecriture autorisee")
    for cache in (args.cache, args.cache_foret, args.cache_a35, args.cache_a41):
        if not Path(cache).is_file():
            raise SystemExit(f"cache absent, aucune reconstruction implicite : {cache}")
    with threadpool_limits(limits=2):
        paquet = C41.charger_paquet(args.cache, args.cache_foret, args.cache_a35)
        colonnes, _ = C41.colonnes_familles(paquet["items"])
        if len(colonnes) != 58:
            raise ValueError("perimetre different des 58 items")
        ech0 = pd.read_csv(TRACES / "a5-personnes.csv")
        ech1 = pd.read_csv(TRACES / "r2b-personnes-ext.csv")
        valider_population(ech0, ech1, paquet)
        table = R2E.nomenclature()
        items = [paquet["items"][j] for j in colonnes]
        n0 = valider_trace(TRACES / "r2-C3F-gptoss.jsonl", ech0, items, table, registre=REGISTRE)
        n1 = valider_trace(TRACES / "r2b-C3F-gptoss-ext.jsonl", ech1, items, table, registre=REGISTRE)
        print(f"Validation : 180 uniques completes, {n0} + {n1} appels, 58 items", flush=True)
        union, trace = preparer_dossier(args.travail, ech0, ech1)
        args.sortie.mkdir(parents=True, exist_ok=False)
        print(f"Sorties agregees : {args.sortie}", flush=True)
        print(f"Threads : {threadpool_info()}", flush=True)
        # Redirections en memoire seulement ; le fichier r2_evaluer.py reste intact.
        ancien_charger, ancien_ecrire = C41.charger_paquet, C41.ecrire
        ancien_traces, anciens_fichiers = R2E.TRACES, R2E.TRACES_R2
        ancien_dossier, ancien_argv = R2E.DOSSIER_TRACES, sys.argv
        def ecrire(df, nom):
            nom = nom.replace("r2-", "r2b-", 1) if nom.startswith("r2-") else nom
            if Path(nom).name != nom:
                raise ValueError("nom de sortie hors dossier")
            with (args.sortie / nom).open("x", encoding="utf-8", newline="") as fh:
                df.to_csv(fh, index=False)
        try:
            C41.charger_paquet = lambda *a, **kw: paquet
            C41.ecrire = ecrire
            R2E.TRACES = str(args.travail)
            R2E.TRACES_R2 = [("C3F gpt-oss-20b", trace.name, "C3F"),
                            ("C3 gpt-oss-20b", "r2-C3-gptoss.jsonl", "C3"),
                            ("C3F Qwen3-4B", "a5-C3F-p1.jsonl", "C3F")]
            sys.argv = ["r2_evaluer.py", "--tirages", str(args.tirages),
                        "--permutations", str(args.permutations), "--suffixe=-180",
                        "--racine-traces", str(args.travail),
                        "--cache", args.cache, "--cache-foret", args.cache_foret,
                        "--cache-a35", args.cache_a35, "--cache-a41", args.cache_a41]
            R2E.main()
            refs = R2E.references_population(paquet)
            index = {p: i for i, p in enumerate(paquet["ids"])}
            l150 = np.array([index[p] for p in ech0.pid])
            l180 = np.array([index[p] for p in union.pid])
            gl = glissement_des_cellules(paquet, refs, l150, l180, colonnes)
            ecrire(gl, "r2b-glissement-cellules-180.csv")
            print(gl.to_string(index=False), flush=True)
        finally:
            C41.charger_paquet, C41.ecrire = ancien_charger, ancien_ecrire
            R2E.TRACES, R2E.TRACES_R2 = ancien_traces, anciens_fichiers
            R2E.DOSSIER_TRACES, sys.argv = ancien_dossier, ancien_argv
    print("EVALUATION R2b TERMINEE", flush=True)


if __name__ == "__main__":
    main()
