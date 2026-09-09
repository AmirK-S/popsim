"""
a12_telecharger_panel : recuperation des panels GSS de NORC, et rien d'autre.

Statut : script d'exploration, pas du code de production.

Ce que fait ce script : il telecharge les quatre fichiers de panel du GSS depuis
gss.norc.org, les decompresse dans data/gss-panel/, verifie les tailles et les
empreintes, et ecrit data/gss-panel/PROVENANCE.md.

Ce qu'il ne fait pas : aucun calcul, aucun appel de modele, aucune ecriture hors de
data/gss-panel/. Les fichiers telecharges sont des microdonnees sous conditions NORC :
ils ne sortent jamais de data/, qui est dans le .gitignore, et ils ne sont jamais
redistribues.

Usage : .venv/bin/python analyses/a12_telecharger_panel.py
"""

import hashlib
import os
import subprocess
import sys
import urllib.request
import zipfile
from datetime import date

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RACINE, "data", "gss-panel")
BASE = "https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/"

# Les quatre panels du GSS, tels que listes sur
# https://gss.norc.org/us/en/gss/get-the-data/stata.html
# Cle : nom court utilise dans tout le reste de a12.
PANELS = {
    "2006-2010": ("GSS_2006_Panel_Stata.zip", "GSS_panel06w123_R6a - Stata.dta"),
    "2008-2012": ("GSS_2008_Panel_stata.zip", "GSS_panel08w123_R6 - stata.dta"),
    "2010-2014": ("GSS_2010_Panel_stata.zip", "GSS_panel2010w123_R6 - stata.dta"),
    "2016-2020": ("GSS_2020_panel_stata_1a.zip", "gss2020panel_r1a.dta"),
}


def empreinte(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


def telecharger(nom_zip):
    cible = os.path.join(DEST, nom_zip)
    if os.path.exists(cible):
        print(f"deja present : {nom_zip} ({os.path.getsize(cible)} octets)")
        return cible
    url = BASE + nom_zip
    print(f"telechargement : {url}")
    urllib.request.urlretrieve(url, cible)
    print(f"  ecrit : {cible} ({os.path.getsize(cible)} octets)")
    return cible


def main():
    os.makedirs(DEST, exist_ok=True)
    lignes = []
    for nom, (zip_nom, dta_nom) in PANELS.items():
        chemin = telecharger(zip_nom)
        with zipfile.ZipFile(chemin) as z:
            contenu = z.namelist()
            for membre in contenu:
                if not os.path.exists(os.path.join(DEST, membre)):
                    z.extract(membre, DEST)
        taille_dta = os.path.getsize(os.path.join(DEST, dta_nom))
        lignes.append({
            "panel": nom, "zip": zip_nom, "octets_zip": os.path.getsize(chemin),
            "sha256_zip": empreinte(chemin), "dta": dta_nom, "octets_dta": taille_dta,
            "contenu": contenu,
        })

    provenance = os.path.join(DEST, "PROVENANCE.md")
    with open(provenance, "w") as f:
        f.write("# Provenance des panels GSS\n\n")
        f.write(f"Ecrit par `analyses/a12_telecharger_panel.py` le {date.today().isoformat()}.\n\n")
        f.write("## Source\n\n")
        f.write("Page d'index : https://gss.norc.org/us/en/gss/get-the-data/stata.html\n\n")
        f.write("Telechargement direct par URL, sans compte, sans formulaire, sans jeton.\n")
        f.write("Verifie par requete HEAD : HTTP 200 et `content-type: application/zip`.\n\n")
        f.write("## Conditions d'usage\n\n")
        f.write("Conditions generales NORC, https://gss.norc.org/us/en/gss/terms-and-conditions.html :\n")
        f.write('> "No part of the contents of NORC websites may be reproduced, stored, or\n')
        f.write('> transmitted in any form or by any means, electronic or mechanical, in whole\n')
        f.write('> or in any part, without the express written consent of NORC."\n\n')
        f.write("Consequence operationnelle pour popsim : le telechargement et l'analyse locale\n")
        f.write("sont possibles sans demarche, la **redistribution ne l'est pas**. Ces fichiers\n")
        f.write("restent dans `data/`, qui est dans le `.gitignore`. Aucune microdonnee, aucun\n")
        f.write("extrait de ligne individuelle ne sort de ce dossier. Les tableaux produits par\n")
        f.write("a12 sont des agregats par item et par decile, jamais des enregistrements.\n\n")
        f.write("## Fichiers\n\n")
        f.write("| panel | archive | octets | sha256 | fichier Stata | octets |\n")
        f.write("|---|---|---|---|---|---|\n")
        for l in lignes:
            f.write(f"| {l['panel']} | {l['zip']} | {l['octets_zip']} | `{l['sha256_zip'][:16]}...` "
                    f"| {l['dta']} | {l['octets_dta']} |\n")
        f.write("\nEmpreintes completes :\n\n```\n")
        for l in lignes:
            f.write(f"{l['sha256_zip']}  {l['zip']}\n")
        f.write("```\n\n")
        f.write("## Citation demandee par NORC\n\n")
        f.write("Smith, Tom W., Davern, Michael, Freese, Jeremy, and Morgan, Stephen L.,\n")
        f.write("General Social Surveys, panel files. Chicago: NORC.\n")
    print(f"\nprovenance ecrite : {provenance}")


if __name__ == "__main__":
    main()
