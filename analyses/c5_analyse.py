"""
c5_analyse : lit les traces de c5_formulation.py et ecrit resultats/c5-resultats.md.

Statut : script d'analyse, aucun appel de modele de langage. Applique les mesures et les
criteres de `resultats/c5-preenregistrement.md`, ecrit et commis avant le premier appel.

Ce qu'il fait, pour chaque modele demande :
  1. relit l'effet humain des onze paires (recalcule par `c5_formulation.effet_humain_wave1`,
     jamais retape) ;
  2. pour chaque persona et chaque paire, l'effet simule est la difference des `too much`
     de la forme historique et de la forme Y (un appel rejete retire la paire ENTIERE pour
     ce persona, jamais une seule forme) ;
  3. moyenne cet effet sur les personas retenus, paire par paire ;
  4. mesure primaire : MAE entre effet simule et effet humain, moyennee sur les onze
     paires, IC par bootstrap sur les personas (2000 tirages, meme tirage reutilise pour
     la mesure secondaire) ;
  5. mesure secondaire : taux de fausses alertes sur les cinq paires nulles humaines
     (|effet simule| > 5 points), IC bootstrap sur le meme tirage de personas ;
  6. relit les comparateurs forts (nul a 0 sauf welfare, nul a 0 partout) et les cinq
     predictions chiffrees de la section 5 du preenregistrement ;
  7. applique le critere de la section 6 : instrument, mise en garde, ou abandon.

Avec `--suffixe`, l'analyse porte sur les traces de test (`c5-<modele>-<suffixe>.jsonl`)
et ecrit dans `resultats/c5-resultats-<suffixe>.md`, jamais dans le rapport final : c'est
la verification de l'etape 3 (20 personas, taux de parse et grammaire, aucune conclusion).

Entree  : data/traces/c5/c5-<modele>.jsonl (ou -<suffixe>.jsonl), c5-personas*.csv.
Sortie  : resultats/c5-resultats.md (ou -<suffixe>.md avec --suffixe).

Usage :
  .venv/bin/python analyses/c5_analyse.py --suffixe smoke --modele oss20   # verification
  .venv/bin/python analyses/c5_analyse.py --modele oss20,q30              # rapport final
"""

import argparse
import collections
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c5_formulation import MODELES, PAIRES, PAIRES_NULLES, TRACES, effet_humain_wave1

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTATS = os.path.join(RACINE, "resultats")

N_BOOT = 2000
GRAINE_BOOT = 20260911
SEUIL_FAUSSE_ALERTE = 5.0
SEUIL_COMPARATEUR_INSTRUMENT = 4.3
SEUIL_COMPARATEUR_MISE_EN_GARDE = 7.0


def lire_traces(cle, suffixe):
    """Lit une trace : {(pid, forme): pct_too_much ou None si l'appel est rejete}."""
    nom = f"c5-{cle}" + (f"-{suffixe}" if suffixe else "") + ".jsonl"
    chemin = os.path.join(TRACES, nom)
    if not os.path.exists(chemin):
        sys.exit(f"trace introuvable : {chemin}")
    sortie = {}
    n_lignes = n_rejets = 0
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            d = json.loads(ligne)
            n_lignes += 1
            if d["rejet"] or d["distribution"] is None:
                n_rejets += 1
                sortie[(d["pid"], d["forme"])] = None
            else:
                sortie[(d["pid"], d["forme"])] = 100.0 * d["distribution"]["too much"]
    return sortie, n_lignes, n_rejets, chemin


def effets_par_persona(trace):
    """{paire: {pid: effet}} = too_much(forme historique) - too_much(forme Y), pid retenu
    seulement si les deux formes de la paire sont presentes et non rejetees."""
    sortie = {}
    pids = sorted({pid for pid, _ in trace})
    for paire, d in PAIRES.items():
        var_h = d["hist"][0]
        var_y = d["y"][0]
        par_pid = {}
        for pid in pids:
            th = trace.get((pid, var_h))
            ty = trace.get((pid, var_y))
            if th is None or ty is None:
                continue
            par_pid[pid] = th - ty
        sortie[paire] = par_pid
    return sortie


def mae_pour_tirage(effets, humain, pids):
    """MAE moyenne sur les onze paires, pour un ensemble donne de personas (bootstrap)."""
    erreurs = []
    for paire in PAIRES:
        vals = [effets[paire][p] for p in pids if p in effets[paire]]
        if not vals:
            continue
        simule = float(np.mean(vals))
        h = humain.loc[humain["paire"] == paire, "effet_humain"].item()
        erreurs.append(abs(simule - h))
    return float(np.mean(erreurs)) if erreurs else float("nan")


def taux_fausses_alertes_pour_tirage(effets, pids, seuil=SEUIL_FAUSSE_ALERTE):
    n_alerte = 0
    for paire in PAIRES_NULLES:
        vals = [effets[paire][p] for p in pids if p in effets[paire]]
        if not vals:
            continue
        if abs(float(np.mean(vals))) > seuil:
            n_alerte += 1
    return n_alerte / len(PAIRES_NULLES)


def bootstrap(effets, humain, pids, n=N_BOOT, graine=GRAINE_BOOT):
    """Un seul tirage de personas reutilise pour le MAE et le taux de fausses alertes,
    comme prevu section 3 du preenregistrement ('meme tirage')."""
    rng = np.random.default_rng(graine)
    pids = np.array(pids)
    maes, taux = [], []
    for _ in range(n):
        tirage = rng.choice(pids, size=len(pids), replace=True)
        maes.append(mae_pour_tirage(effets, humain, tirage))
        taux.append(taux_fausses_alertes_pour_tirage(effets, tirage))
    return np.array(maes), np.array(taux)


def ic95(valeurs):
    return float(np.nanpercentile(valeurs, 2.5)), float(np.nanpercentile(valeurs, 97.5))


def effet_par_paire(effets, humain, pids):
    lignes = []
    for paire in PAIRES:
        vals = [effets[paire][p] for p in pids if p in effets[paire]]
        simule = float(np.mean(vals)) if vals else float("nan")
        h = humain.loc[humain["paire"] == paire]
        lignes.append({
            "paire": paire, "n_personas": len(vals),
            "effet_humain": h["effet_humain"].item(), "nul_humain": bool(h["nul"].item()),
            "effet_simule": round(simule, 2) if vals else None,
            "erreur_absolue": round(abs(simule - h["effet_humain"].item()), 2) if vals else None,
        })
    return pd.DataFrame(lignes)


def cellule_big_cities(trace, personas):
    """Effet signe de natcity/y par camp, pour la prediction sur 'big cities' (section 5)."""
    camp_de = {p["pid"]: p["camp"] for p in personas}
    par_camp = collections.defaultdict(list)
    for pid, camp in camp_de.items():
        th = trace.get((pid, "natcity"))
        ty = trace.get((pid, "natcityy"))
        if th is None or ty is None:
            continue
        par_camp[camp].append(th - ty)
    return {c: float(np.mean(v)) for c, v in par_camp.items() if v}


def comparateurs(humain):
    h = humain.set_index("paire")["effet_humain"]
    tout_zero_sauf_welfare = float(np.mean([abs(h[p] - (30 if p == "natfare" else 0))
                                            for p in PAIRES]))
    tout_zero = float(np.mean([abs(h[p]) for p in PAIRES]))
    return tout_zero_sauf_welfare, tout_zero


def analyser_modele(cle, suffixe, humain):
    trace, n_lignes, n_rejets, chemin = lire_traces(cle, suffixe)
    chemin_personas = os.path.join(
        TRACES, f"c5-personas{'-' + suffixe if suffixe else ''}.csv")
    personas = pd.read_csv(chemin_personas).to_dict("records")

    effets = effets_par_persona(trace)
    pids = sorted({pid for pid, _ in trace})
    tab = effet_par_paire(effets, humain, pids)
    mae = float(np.nanmean(tab["erreur_absolue"]))
    taux_fa = taux_fausses_alertes_pour_tirage(effets, pids)

    maes_boot, taux_boot = bootstrap(effets, humain, pids)
    mae_ic = ic95(maes_boot)
    taux_ic = ic95(taux_boot)

    big_cities = cellule_big_cities(trace, personas)
    welfare = tab.loc[tab["paire"] == "natfare", "effet_simule"].item()

    return {
        "cle": cle, "nom": MODELES[cle]["nom"], "trace": chemin,
        "n_lignes": n_lignes, "n_rejets": n_rejets,
        "taux_parse": 1 - n_rejets / n_lignes if n_lignes else float("nan"),
        "n_personas": len(pids), "tableau": tab, "mae": mae, "mae_ic95": mae_ic,
        "taux_fausses_alertes": taux_fa, "taux_fausses_alertes_ic95": taux_ic,
        "big_cities_par_camp": big_cities, "welfare_effet_simule": welfare,
    }


def verdict(mae, mae_ic, taux_fa):
    if mae_ic[1] < SEUIL_COMPARATEUR_INSTRUMENT:
        return "INSTRUMENT (MAE sous 4,3, IC bootstrap strictement en dessous)"
    if mae > SEUIL_COMPARATEUR_MISE_EN_GARDE and taux_fa >= 3 / 5:
        return "MISE EN GARDE (MAE au dessus de 7,0 ET au moins 3 fausses alertes sur 5)"
    if SEUIL_COMPARATEUR_INSTRUMENT <= mae <= SEUIL_COMPARATEUR_MISE_EN_GARDE and taux_fa <= 1 / 5:
        return "ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte)"
    return "ZONE GRISE (aucun des trois criteres de la section 6 n'est rempli exactement)"


def ecrire_rapport(resultats, humain, chemin, suffixe):
    tz_welfare, tz_zero = comparateurs(humain)
    lignes = []
    titre = "# C5, resultats" + (f" (verification, suffixe {suffixe})" if suffixe else "")
    lignes.append(titre)
    lignes.append("")
    if suffixe:
        lignes.append("**Traces de test, 20 personas exclues de l'echantillon de 300. "
                       "Aucune conclusion du preenregistrement ne s'applique ici : ce "
                       "fichier verifie le taux de parse et la grammaire de sortie, pas "
                       "l'hypothese.**")
        lignes.append("")
    lignes.append(f"Comparateurs forts (preenregistrement section 4) : nul tout a 0 sauf "
                   f"welfare = {tz_welfare:.2f} points, nul tout a 0 = {tz_zero:.2f} "
                   f"points.")
    lignes.append("")
    for r in resultats:
        lignes.append(f"## {r['nom']} (`{r['cle']}`)")
        lignes.append("")
        lignes.append(f"Trace `{r['trace']}`, {r['n_lignes']} lignes, {r['n_rejets']} "
                       f"rejets, taux de parse {r['taux_parse']:.4f}, {r['n_personas']} "
                       f"personas avec au moins un appel.")
        lignes.append("")
        lignes.append(f"MAE = **{r['mae']:.2f}** points, IC95 bootstrap "
                       f"[{r['mae_ic95'][0]:.2f} ; {r['mae_ic95'][1]:.2f}].")
        lignes.append(f"Taux de fausses alertes (5 paires nulles, seuil "
                       f"{SEUIL_FAUSSE_ALERTE:.0f} points) = "
                       f"**{r['taux_fausses_alertes']:.2f}**, IC95 bootstrap "
                       f"[{r['taux_fausses_alertes_ic95'][0]:.2f} ; "
                       f"{r['taux_fausses_alertes_ic95'][1]:.2f}].")
        lignes.append("")
        lignes.append("| paire | effet humain | nul ? | effet simule | erreur absolue |")
        lignes.append("|---|---|---|---|---|")
        for _, row in r["tableau"].iterrows():
            lignes.append(f"| {row['paire']} | {row['effet_humain']:.2f} | "
                           f"{'oui' if row['nul_humain'] else 'non'} | "
                           f"{row['effet_simule']:.2f} | {row['erreur_absolue']:.2f} |")
        lignes.append("")
        signe_ok = "bon signe" if r["welfare_effet_simule"] > 0 else "signe oppose"
        amplitude_ok = "> 20 points" if r["welfare_effet_simule"] > 20 else "<= 20 points"
        lignes.append(f"Prediction welfare : effet simule {r['welfare_effet_simule']:.2f} "
                       f"points, {signe_ok}, {amplitude_ok} (predit : bon signe et > 20 "
                       f"points, 95 %).")
        bc = r["big_cities_par_camp"]
        bons = sum(1 for v in bc.values() if v < 0)
        lignes.append(f"Prediction big cities : signe correct (effet negatif) dans "
                       f"{bons}/{len(bc)} cellules camp x modele "
                       f"({', '.join(f'{c}={v:.2f}' for c, v in bc.items())}), predit au "
                       f"plus la moitie.")
        lignes.append("")
        lignes.append(f"**Verdict (section 6) : {verdict(r['mae'], r['mae_ic95'], r['taux_fausses_alertes'])}.**")
        lignes.append("")
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lignes) + "\n")
    return chemin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="oss20,q30")
    ap.add_argument("--suffixe", default="",
                    help="suffixe des traces de test ; ecrit alors dans "
                         "resultats/c5-resultats-<suffixe>.md, jamais le rapport final")
    args = ap.parse_args()

    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in MODELES:
            sys.exit(f"modele inconnu : {c}")

    humain = effet_humain_wave1()
    resultats = [analyser_modele(c, args.suffixe, humain) for c in cles]

    nom_rapport = "c5-resultats" + (f"-{args.suffixe}" if args.suffixe else "") + ".md"
    chemin = os.path.join(RESULTATS, nom_rapport)
    ecrire_rapport(resultats, humain, chemin, args.suffixe)
    print(f"rapport ecrit : {chemin}")
    for r in resultats:
        print(f"{r['cle']} : MAE {r['mae']:.2f} (IC {r['mae_ic95']}), "
              f"fausses alertes {r['taux_fausses_alertes']:.2f}")


if __name__ == "__main__":
    main()
