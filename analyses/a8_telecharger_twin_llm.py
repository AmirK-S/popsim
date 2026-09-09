"""
a8_telecharger_twin_llm : recupere les treize configurations de simulation de Twin-2K-500.

Statut : script d'exploration, pas du code de production. Il complete
analyses/a2_telecharger_twin.py, qui ne prenait que deux configurations sur treize. La
limite 5 du rapport a2 dit exactement cela : "un seul modele de langage sert de repere
sur Twin". Ce script leve cette limite.

Liste obtenue le 7 septembre 2026 par l'API Hugging Face
https://huggingface.co/api/datasets/LLM-Digital-Twin/Twin-2K-500?full=true
en filtrant les fichiers responses_llm_imputed_formatted.csv du dossier
LLM_simulation_results/llm_simulations_all_specifications/.

Entree  : rien, hors acces reseau.
Sortie  : data/twin2k500/llm/spec_*.csv, non versionne (data/ est dans .gitignore).

Usage : .venv/bin/python analyses/a8_telecharger_twin_llm.py
"""

import os
import sys
import urllib.parse
import urllib.request

DEPOT = "LLM-Digital-Twin/Twin-2K-500"
BASE = f"https://huggingface.co/datasets/{DEPOT}/resolve/main"
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CIBLE = os.path.join(RACINE, "data/twin2k500/llm")
PREFIXE = "LLM_simulation_results/llm_simulations_all_specifications"
SUFFIXE = "csv_comparison/csv_formatted/responses_llm_imputed_formatted.csv"

# nom de dossier distant -> nom de fichier local. Les libelles restent ceux des auteurs.
SPECIFICATIONS = {
    "Demographics Only - GPT4.1-mini": "spec_demo_only_gpt41mini.csv",
    "JSON Persona (Predicted Output) - GPT4.1-mini": "spec_json_predout_gpt41mini.csv",
    "JSON Persona (Predicted Output) - GPT4.1": "spec_json_predout_gpt41.csv",
    "JSON Persona - GPT4.1-mini": "spec_json_gpt41mini.csv",
    "JSON Persona - GPT4.1": "spec_json_gpt41.csv",
    "LLM Finetuning (500 training samples) - GPT4.1-mini": "spec_finetune500_gpt41mini.csv",
    "Persona Summary - GPT4.1-mini": "spec_resume_gpt41mini.csv",
    "Persona Summary - JSON Persona - GPT4.1-mini": "spec_resume_json_gpt41mini.csv",
    "Text Persona (Default Temperature) - GPT4.1-mini": "spec_texte_temp_defaut_gpt41mini.csv",
    "Text Persona (Reasoning) - GPT4.1-mini": "spec_texte_raisonnement_gpt41mini.csv",
    "Text Persona (Repeating Questions) - GPT4.1-mini": "spec_texte_repetition_gpt41mini.csv",
    "Text Persona - GPT4.1-mini": "spec_texte_gpt41mini.csv",
    "Text Persona - Gemini-Flash2.5": "spec_texte_gemini_flash25.csv",
}


def main():
    os.makedirs(CIBLE, exist_ok=True)
    echecs = []
    for dossier, local in SPECIFICATIONS.items():
        chemin = os.path.join(CIBLE, local)
        if os.path.exists(chemin) and os.path.getsize(chemin) > 0:
            print(f"deja present, ignore : {local}")
            continue
        url = f"{BASE}/{urllib.parse.quote(f'{PREFIXE}/{dossier}/{SUFFIXE}')}"
        print(f"telechargement : {local}", flush=True)
        try:
            urllib.request.urlretrieve(url, chemin)
        except Exception as erreur:
            # On dit pourquoi le telechargement echoue, on ne contourne pas.
            print(f"  ECHEC sur {url}\n  {erreur}", file=sys.stderr)
            echecs.append(local)
    print(f"\ndestination : {CIBLE}")
    if echecs:
        print(f"echecs : {', '.join(echecs)}", file=sys.stderr)


if __name__ == "__main__":
    main()
