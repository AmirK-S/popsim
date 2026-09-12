"""garde : garde-fou commun a tous les scripts de artefact/.

Refuse de demarrer si un chemin (argument de ligne de commande, variable
d'environnement, ou chemin supplementaire fourni par l'appelant) resout,
une fois les liens symboliques suivis et les composants '.'/'..' elimines,
vers le repertoire reel `data/` du depot -- ou vers un de ses descendants.
artefact/ ne doit JAMAIS lire quoi que ce soit sous data/ : tout son jeu de
donnees est fictif et genere sur place dans artefact/donnees_fictives/.

Principe retenu (suite a resultats/artefact-reproduction-2026-09-12.md, qui
a demontre quatre contournements d'une version anterieure fondee sur la
recherche de motifs suspects dans une chaine de caracteres -- casse,
separateur, nom de variable d'environnement, lien symbolique de nom
neutre) : on ne juge plus une chaine, on resout le chemin *reellement
atteint* par l'appel systeme qui suivrait (open, os.stat, ...), puis on
verifie sa relation d'ancestralite avec le dossier interdit -- normalisee,
absolue, et insensible a la casse (macOS et Windows le sont tous deux au
niveau du systeme de fichiers, et `os.path.realpath` ne corrige pas la
casse de lui-meme : voir les tests de artefact/test_garde.py).
"""

import os
import sys
from pathlib import Path

# Dossier interdit : data/ a la racine du depot (artefact/ est un sous-
# dossier direct de la racine). Les tests remplacent cet attribut de module
# (monkeypatch) pour s'executer dans une arborescence jetable plutot que
# sur le vrai depot.
_DONNEES_INTERDITES = (Path(__file__).resolve().parent.parent / "data").resolve()


def _resoudre(chemin):
    """Renvoie, sous forme de chaine, le chemin absolu *reellement atteint*
    si `chemin` etait ouvert maintenant : suit les liens symboliques (y
    compris en chaine), elimine les composants '.' et '..', et traite tout
    '\\' comme un separateur de repertoire meme sur un systeme POSIX -- un
    chemin ecrit avec la convention Windows doit etre juge comme s'il
    designait bien des sous-dossiers, pas comme un nom de fichier opaque.
    N'exige pas que le chemin existe : un chemin encore inexistant est juge
    sur sa seule structure, comme le ferait un appel systeme qui echouerait
    ensuite avec ENOENT plutot que de contourner le garde-fou.
    """
    brut = str(chemin).replace("\\", "/")
    return os.path.realpath(brut)


def _sous_dossier_interdit(chemin_resolu):
    """Vrai si `chemin_resolu` (deja passe par `_resoudre`) est le dossier
    interdit lui-meme ou un de ses descendants, par relation d'ancestralite
    de chemins normalises et absolus -- jamais par recherche de sous-chaine
    (un dossier "database" ou "metadata", ou un chemin qui contient "data"
    au milieu d'un autre nom, n'est pas un descendant de data/ et n'est
    donc pas suspect). La comparaison se fait en minuscules : macOS (APFS
    par defaut) et Windows sont insensibles a la casse au niveau du
    systeme de fichiers, donc `DATA/x` et `data/x` designent le meme
    fichier meme si `os.path.realpath` ne corrige pas la casse de
    lui-meme (verifie empiriquement : realpath('DATA') renvoie 'DATA',
    pas 'data', bien que ce soit le meme inode sur ce systeme).
    """
    cible = str(_DONNEES_INTERDITES).casefold()
    essai = str(chemin_resolu).casefold()
    if essai == cible:
        return True
    prefixe = cible if cible.endswith(os.sep) else cible + os.sep
    return essai.startswith(prefixe)


def _suspect(chemin):
    """Vrai si `chemin` mene reellement, une fois resolu, dans le dossier
    interdit `data/` (ou en dessous)."""
    if not chemin:
        return False
    return _sous_dossier_interdit(_resoudre(chemin))


def verifier_environnement(*chemins_supplementaires):
    """Leve SystemExit si un chemin vers data/ apparait dans argv, dans
    N'IMPORTE QUELLE variable d'environnement -- aucune liste fermee de
    noms a surveiller : toute variable peut vehiculer un chemin, sous
    n'importe quelle casse -- ou dans les chemins supplementaires passes
    par l'appelant."""
    candidats = list(sys.argv[1:]) + [c for c in chemins_supplementaires if c]
    candidats.extend(v for v in os.environ.values() if v)
    for c in candidats:
        if _suspect(c):
            print(f"REFUS : chemin suspect vers des donnees reelles detecte : {c}",
                  file=sys.stderr)
            print("artefact/ ne lit jamais data/. Tout son jeu de donnees est fictif "
                  "(artefact/donnees_fictives/).", file=sys.stderr)
            sys.exit(1)
