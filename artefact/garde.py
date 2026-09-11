"""garde : garde-fou commun a tous les scripts de artefact/.

Refuse de demarrer si un chemin suspect vers les donnees reelles (data/, en particulier
data/twin2k500 ou data/osf-t6g7k-stanford) est detecte dans les arguments de ligne de
commande ou dans quelques variables d'environnement plausibles. artefact/ ne doit JAMAIS
lire quoi que ce soit sous data/ : tout son jeu de donnees est fictif et genere sur place
dans artefact/donnees_fictives/.
"""

import os
import sys

_DOSSIERS_AUTORISES = ("donnees_fictives", "resultats_artefact")


def _suspect(chemin):
    """Vrai si `chemin` contient, comme composant a part entiere (pas comme simple sous-
    chaine), un dossier nomme `data` -- qu'il soit relatif ("data/twin2k500/x.csv") ou
    absolu, avec ou sans separateur de tete. Un composant "database" ou "metadata" n'est
    PAS suspect : seule une correspondance exacte du nom de dossier compte."""
    if chemin is None:
        return False
    c = os.path.normpath(str(chemin))
    if any(d in c for d in _DOSSIERS_AUTORISES):
        return False
    composants = c.split(os.sep)
    return "data" in composants


def verifier_environnement(*chemins_supplementaires):
    """Leve SystemExit si un chemin vers data/ apparait dans argv, l'environnement, ou
    les chemins supplementaires passes par l'appelant."""
    candidats = list(sys.argv[1:]) + [c for c in chemins_supplementaires if c]
    for var in ("POPSIM_DATA", "TWIN2K500", "DATA_DIR", "RACINE_TWIN"):
        v = os.environ.get(var)
        if v:
            candidats.append(v)
    for c in candidats:
        if _suspect(c):
            print(f"REFUS : chemin suspect vers des donnees reelles detecte : {c}",
                  file=sys.stderr)
            print("artefact/ ne lit jamais data/. Tout son jeu de donnees est fictif "
                  "(artefact/donnees_fictives/).", file=sys.stderr)
            sys.exit(1)
