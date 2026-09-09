"""
a6_telecharger_twin_specs : recupere les 13 configurations de simulation de Twin-2K-500.

Statut : script d'exploration, pas du code de production. Complement de
analyses/a2_telecharger_twin.py, qui n'avait ramene que deux configurations sur treize.

Le depot Hugging Face LLM-Digital-Twin/Twin-2K-500, licence CC BY 4.0, publie sous
LLM_simulation_results/llm_simulations_all_specifications/ un dossier par configuration
de simulation. On ne prend de chacun que le fichier de reponses simulees mis au format
de la vague 4, plus les deux fichiers de reference humains dans le meme format :
    responses_wave4_formatted.csv    verite terrain, vague 4
    responses_wave1_3_formatted.csv  memes questions, reponses donnees en vagues 1 a 3,
                                     c'est a dire le retest humain wave4_Q_wave1_3_A

Entree  : rien, hors acces reseau.
Sortie  : data/twin2k500/llm_specs/, environ 12 Mo, non versionne.

Usage : .venv/bin/python analyses/a6_telecharger_twin_specs.py
"""

import json
import os
import sys
import urllib.parse
import urllib.request

DEPOT = "LLM-Digital-Twin/Twin-2K-500"
BASE = f"https://huggingface.co/datasets/{DEPOT}/resolve/main"
API = f"https://huggingface.co/api/datasets/{DEPOT}/tree/main"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLE = os.path.join(RACINE, "data/twin2k500/llm_specs")
PREFIXE = "LLM_simulation_results/llm_simulations_all_specifications"


def nom_local(spec):
    """Nom de fichier sur : le nom de la configuration, sans espace ni ponctuation."""
    s = spec.replace(" ", "_").replace("(", "").replace(")", "").replace(".", "")
    return s.replace("/", "_").replace("-", "_").replace("__", "_").lower()


def telecharger(url, chemin):
    if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
        print(f"  deja present : {os.path.basename(chemin)}")
        return True
    try:
        urllib.request.urlretrieve(url, chemin)
        return True
    except Exception as erreur:
        print(f"  ECHEC {url}\n  {erreur}", file=sys.stderr)
        return False


def main():
    os.makedirs(CIBLE, exist_ok=True)
    url = f"{API}/{urllib.parse.quote(PREFIXE)}?recursive=false"
    try:
        arbre = json.load(urllib.request.urlopen(url))
    except Exception as erreur:
        sys.exit(f"Listage impossible : {erreur}")
    specs = [x["path"].split("/")[-1] for x in arbre if x["type"] == "directory"]
    print(f"{len(specs)} configurations listees sur le depot")

    index = []
    for spec in sorted(specs):
        distant = (f"{PREFIXE}/{spec}/csv_comparison/csv_formatted/"
                   "responses_llm_imputed_formatted.csv")
        local = os.path.join(CIBLE, f"{nom_local(spec)}.csv")
        print(f"{spec}")
        if telecharger(f"{BASE}/{urllib.parse.quote(distant)}", local):
            index.append({"configuration": spec, "fichier": os.path.basename(local)})

    # Les deux references humaines, dans le meme espace de colonnes.
    ref = "Text Persona - GPT4.1-mini"
    for distant_f, local_f in [("responses_wave4_formatted.csv", "humains_wave4.csv"),
                               ("responses_wave1_3_formatted.csv", "humains_wave1_3.csv")]:
        distant = f"{PREFIXE}/{ref}/csv_comparison/csv_formatted/{distant_f}"
        print(local_f)
        telecharger(f"{BASE}/{urllib.parse.quote(distant)}", os.path.join(CIBLE, local_f))

    with open(os.path.join(CIBLE, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=1, ensure_ascii=False)
    print(f"\ndestination : {CIBLE}")


if __name__ == "__main__":
    main()
