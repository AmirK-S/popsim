"""
a2_telecharger_twin : recupere les fichiers utiles de Twin-2K-500 depuis Hugging Face.

Statut : script d'exploration, pas du code de production. Il existe pour qu'un tiers
reconstitue le jeu de donnees en une commande, sans que rien ne soit versionne.

Identifiant du depot verifie le 3 septembre 2026 par l'API :
    https://huggingface.co/api/datasets/LLM-Digital-Twin/Twin-2K-500
    private: false, gated: false, disabled: false, license: cc-by-4.0
Il n'y a donc ni jeton ni acceptation de conditions a fournir. Le depot complet pese
plusieurs gigaoctets, on ne prend que ce qui sert : les reponses humaines mises au propre,
le catalogue de questions, et deux simulations publiees servant de points de repere.

Entree  : rien, hors acces reseau.
Sortie  : data/twin2k500/, environ 40 Mo, non versionne (data/ est dans .gitignore).

Usage : python3 analyses/a2_telecharger_twin.py
"""

import os
import sys
import urllib.parse
import urllib.request

DEPOT = "LLM-Digital-Twin/Twin-2K-500"
BASE = f"https://huggingface.co/datasets/{DEPOT}/resolve/main"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLE = os.path.join(RACINE, "data/twin2k500")

# chemin distant -> chemin local
FICHIERS = {
    "README.md": "README.md",
    "question_catalog_and_human_response_csv/question_catalog.json":
        "question_catalog_and_human_response_csv/question_catalog.json",
    "question_catalog_and_human_response_csv/question_catalog_README.md":
        "question_catalog_and_human_response_csv/question_catalog_README.md",
    "question_catalog_and_human_response_csv/generate_catalog_and_csvs.py":
        "question_catalog_and_human_response_csv/generate_catalog_and_csvs.py",
    "question_catalog_and_human_response_csv/wave1_3_response.csv":
        "question_catalog_and_human_response_csv/wave1_3_response.csv",
    "question_catalog_and_human_response_csv/wave1_3_response_label.csv":
        "question_catalog_and_human_response_csv/wave1_3_response_label.csv",
    "question_catalog_and_human_response_csv/wave4_response.csv":
        "question_catalog_and_human_response_csv/wave4_response.csv",
    "question_catalog_and_human_response_csv/wave4_response_label.csv":
        "question_catalog_and_human_response_csv/wave4_response_label.csv",
    "LLM_simulation_results/wave4_formatted_to_catalog_mapping.json":
        "llm/wave4_formatted_to_catalog_mapping.json",
    "LLM_simulation_results/wave4_formatted_to_catalog_mapping_README.md":
        "llm/README_mapping.md",
    "LLM_simulation_results/GPT4.1-mini-simulation-llm-vs-human/"
    "responses_llm_imputed_formatted.csv": "llm/default_gpt41mini_llm.csv",
    "LLM_simulation_results/GPT4.1-mini-simulation-llm-vs-human/"
    "responses_wave4_formatted.csv": "llm/default_gpt41mini_wave4.csv",
    "LLM_simulation_results/llm_simulations_all_specifications/Demographics Only - "
    "GPT4.1-mini/csv_comparison/csv_formatted/responses_llm_imputed_formatted.csv":
        "llm/demo_only_gpt41mini_llm.csv",
    # Un seul fragment du wave_split, 27 Mo, uniquement pour verifier que le persona des
    # vagues 1 a 3 ne contient pas les questions de la vague 4. Voir rapport section 2.2.
    "wave_split/chunks/wave_persona_chunk_001.parquet":
        "wave_persona_chunk_001.parquet",
}


def main():
    for distant, local in FICHIERS.items():
        chemin = os.path.join(CIBLE, local)
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
            print(f"deja present, ignore : {local}")
            continue
        url = f"{BASE}/{urllib.parse.quote(distant)}"
        print(f"telechargement : {local}", flush=True)
        try:
            urllib.request.urlretrieve(url, chemin)
        except Exception as erreur:
            # On dit pourquoi le telechargement echoue, on ne contourne pas.
            print(f"  ECHEC sur {url}\n  {erreur}", file=sys.stderr)
    print(f"\ndestination : {CIBLE}")


if __name__ == "__main__":
    main()
