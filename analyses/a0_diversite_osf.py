"""
a0 : premiere mesure de la diversite preservee, sur les donnees publiques de Stanford.

Statut : script d'exploration, pas du code de production. Il existe pour que le premier
chiffre du projet soit rejouable par un tiers en une commande.

Entree  : paquet de replication OSF t6g7k, dossier
          figure2/data/new_analysis_summaries/gss_filtered/preparation/
          Un fichier par condition, une ligne par participant, une colonne par item du GSS,
          valeurs en clair du type "too little" / "about right" / "too much".
Sortie  : entropie de reponse moyenne par condition, rapportee a celle des humains,
          et probabilite que deux repondants tires au hasard donnent la meme reponse.

Aucun appel de modele. Duree : moins d'une seconde.

Usage : python3 analyses/a0_diversite_osf.py [chemin_du_dossier_preparation]
"""

import csv, math, os, sys
from collections import Counter

DEFAUT = ("data/osf-t6g7k-stanford/figure2/data/new_analysis_summaries/"
          "gss_filtered/preparation")

# Valeurs a exclure du calcul : non reponses et cellules vides.
MANQUANT = {"", "<not recorded>", "nan", "NA"}

CONDITIONS = {
    "humains vague 1": "p_wave1_summary.csv",
    "humains vague 2": "p_wave2_summary.csv",
    "agents enquete": "survey_agents_summary.csv",
    "agents composite": "composite_agents_summary.csv",
    "agents v3": "gss_v3_summary.csv",
    "agents v6": "gss_v6_summary.csv",
    "agents v7": "gss_v7_summary.csv",
    "agents v8": "gss_v8_summary.csv",
}


def charger(chemin):
    with open(chemin, newline="", encoding="utf-8") as fh:
        lignes = list(csv.reader(fh))
    entetes = lignes[0][1:]           # la premiere colonne est l'identifiant
    donnees = [l[1:] for l in lignes[1:] if len(l) > 1]
    return entetes, donnees


def entropie(valeurs):
    """Entropie de Shannon en bits de la distribution des reponses a un item."""
    valeurs = [v for v in valeurs if v not in MANQUANT]
    if not valeurs:
        return None
    n = len(valeurs)
    return -sum((k / n) * math.log2(k / n) for k in Counter(valeurs).values())


def accord_par_paires(valeurs):
    """Probabilite que deux repondants tires sans remise donnent la meme reponse.

    C'est l'indice de Simpson. Il se lit directement : 50 pour cent veut dire qu'une
    paire au hasard est d'accord une fois sur deux. Plus il est haut, plus la
    population est homogene.
    """
    valeurs = [v for v in valeurs if v not in MANQUANT]
    n = len(valeurs)
    if n < 50:
        return None
    return sum(k * (k - 1) for k in Counter(valeurs).values()) / (n * (n - 1))


def colonne(donnees, j):
    return [l[j] for l in donnees if j < len(l)]


def main():
    base = sys.argv[1] if len(sys.argv) > 1 else DEFAUT
    if not os.path.isdir(base):
        sys.exit(f"Dossier introuvable : {base}\n"
                 "Telecharger le paquet OSF : curl -L -o r.rar https://osf.io/download/s2u7c/")

    charge = {}
    for libelle, fichier in CONDITIONS.items():
        chemin = os.path.join(base, fichier)
        if os.path.exists(chemin):
            charge[libelle] = charger(chemin)
        else:
            print(f"absent, ignore : {fichier}")

    reference = charge["humains vague 1"]
    n_items = len(reference[0])
    entropies_humaines = [entropie(colonne(reference[1], j)) for j in range(n_items)]

    print(f"\n{n_items} items du GSS, {len(reference[1])} participants\n")
    print(f"{'condition':<20}{'entropie moyenne':>18}{'part de la diversite humaine':>32}")
    for libelle, (entetes, donnees) in charge.items():
        paires = []
        for j in range(min(n_items, len(entetes))):
            e = entropie(colonne(donnees, j))
            if e is not None and entropies_humaines[j] is not None:
                paires.append((e, entropies_humaines[j]))
        moyenne = sum(a for a, _ in paires) / len(paires)
        part = sum(a for a, _ in paires) / sum(b for _, b in paires)
        print(f"{libelle:<20}{moyenne:>18.4f}{part * 100:>31.1f}%")

    print("\nProbabilite que deux repondants tires au hasard donnent la meme reponse")
    for libelle, (entetes, donnees) in charge.items():
        valeurs = [accord_par_paires(colonne(donnees, j))
                   for j in range(min(n_items, len(entetes)))]
        valeurs = [v for v in valeurs if v is not None]
        print(f"  {libelle:<20}{sum(valeurs) / len(valeurs) * 100:>7.1f}%")


if __name__ == "__main__":
    main()
