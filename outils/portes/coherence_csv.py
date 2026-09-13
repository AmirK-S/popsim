#!/usr/bin/env python3
"""P8 — coherence chiffre <-> CSV : un nombre publie ne franchit pas sa source.

NUMEROTATION — a lire avant de citer cette porte. Le mandat l'appelait « P6 ».
P6 est deja pris (`outils/portes/horodatage.py`) et P7 aussi
(`outils/rendu_registre.py`, teste par `tests/portes/test_p7_rendu_registre.py`).
Cette porte-ci est donc **P8**, et sa jumelle de preenregistrement **P9**. Le
rapport reste `resultats/portes-p6-p7-2026-09-13.md`, nom impose par le mandat.

LE DEFAUT QU'ELLE FERME
-----------------------
Le 13/09/2026, `c7-controle-generateur-resultats.md` §3 publiait, dans la phrase
explicitement destinee au manuscrit, « ne depasse 0,15 % (Twin-2K-500) », alors
que son propre CSV porte 0,0015354713, soit **0,1535 %**. La borne annoncee etait
**franchie**, et l'arrondi allait dans le sens qui arrange. Le meme rapport
ecrivait « 0,16 % » au §1 et « 0,154 % » au §2 — justes tous les deux. Seule la
phrase la plus lue etait fausse. Aucune des six portes existantes ne pouvait le
voir : elles verifient qu'un chiffre est *declare*, jamais qu'il est *exact*.

CE QU'ELLE NE FAIT PAS, ET C'EST LE POINT
-----------------------------------------
Elle **ne lit aucune prose**. Elle ne cherche pas « ne depasse », « au plus »,
« plafonne a » dans les phrases — un tel filet retrouverait exactement la classe
d'erreurs qui a coute quatre faux positifs a P4 le 12/09 et neuf notes fausses
sur dix au filet `--indice-prose` le 13/09. Elle compare **un nombre declare a un
nombre lu dans un CSV**, et rien d'autre. Un chiffre non annote n'est pas
controle : c'est un faux negatif assume, pas un faux positif paye.

LE MARQUEUR — une valeur se RATTACHE, elle ne se devine pas
-----------------------------------------------------------
Ligne entiere, colonne 0, six champs separes par « | » :

    CHIFFRE: <valeur publiee> | <csv> | <colonne> | <selecteurs> | <echelle> | <sens>

  * `valeur publiee`  le nombre TEL QU'IL EST ECRIT dans la phrase (« 0,15 »).
                      Le nombre de decimales ecrites fixe la precision opposable.
  * `csv`             chemin depuis la racine du depot.
  * `colonne`         nom de colonne, exactement comme dans l'en-tete du CSV.
  * `selecteurs`      `cle=valeur ; cle=valeur` qui doivent designer UNE SEULE
                      ligne ; `-` si le CSV n'a qu'une ligne de donnees.
  * `echelle`         `x1`, `x100`, `x0.01`… multiplicateur applique a la valeur
                      du CSV avant comparaison (un taux 0,0015 publie en %).
  * `sens`            `exact` | `max` | `min` :
                        - `exact` : la valeur publiee est un arrondi fidele ;
                        - `max`   : elle est annoncee comme un PLAFOND
                                    (« ne depasse X ») — elle doit rester
                                    >= a la valeur reelle ;
                        - `min`   : annoncee comme un PLANCHER, <= a la reelle.

Regle d'arrondi opposable, `ulp = 10^-d` ou d est le nombre de decimales ECRITES :
  * `exact` : |publiee - reelle| < ulp. Cela accepte l'arrondi au plus proche
              COMME la troncature — les deux conventions coexistent dans ce depot
              (« 5,13 » demi-vers-le-haut de 5,125 ; « 68,7 » tronque de 68,73) et
              une porte qui en imposerait une produirait des faux positifs.
  * `max`   : publiee >= reelle  ET  publiee - reelle < ulp.
  * `min`   : publiee <= reelle  ET  reelle - publiee < ulp.

C'est `max` qui attrape le 0,15 : 0,15 < 0,1535, **la borne est franchie**. Et
c'est bien `max` et non `exact` qui doit l'attraper, car 0,15 EST l'arrondi
correct de 0,1535 a deux decimales. La faute n'est pas l'arrondi, c'est de
l'annoncer comme une borne. La porte dit cela et rien d'autre.

Pour CITER le marqueur sans le declencher — cette documentation, un rapport qui
parle des portes — l'indenter ou l'encadrer de backticks : il n'est plus a la
colonne 0. Un marqueur MAL FORME, une colonne inconnue, un selecteur qui designe
zero ou plusieurs lignes font ECHOUER la porte : une declaration irresolvable
n'est jamais ignoree en silence, sinon une faute de frappe desarmerait la regle.

DEUXIEME CONTROLE — registre <-> CSV, DORMANT jusqu'a migration
----------------------------------------------------------------
(b) Pour chaque ligne de `resultats/registre-chiffres.csv` dont la colonne
    `csv_source` porte, entre parentheses, un selecteur `colonne=<nom>` (et
    facultativement `echelle=x100`), la porte relit la cellule et verifie que
    `valeur` en est un arrondi fidele (`exact`). Au 13/09/2026 **aucune ligne du
    registre ne porte `colonne=`** : le controle (b) ne resout rien et le dit en
    note, sans rien signaler. La migration est decrite dans
    `resultats/portes-p6-p7-2026-09-13.md` ; elle ne touche que la colonne
    `csv_source`, pas la structure du registre.

Usage :
    coherence_csv.py --tous
    coherence_csv.py --depuis origin/master --mode avertissement
    coherence_csv.py --fichier resultats/x-resultats.md
    coherence_csv.py --registre-seul          # controle (b) uniquement
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import (RACINE, Constat, abandon, git_dispo, lignes,  # noqa: E402
                    masque_code)

NOM = "P8 coherence_csv"
REGISTRE = RACINE / "resultats" / "registre-chiffres.csv"

# Ligne entiere, colonne 0, mot-cle en capitales : aucune phrase francaise ne
# peut prendre cette forme. C'est ce qui rend le faux positif impossible.
RE_MARQUEUR = re.compile(r"^CHIFFRE\s*:(.*)$")
RE_ECHELLE = re.compile(r"^x(\d+(?:[.,]\d+)?)$", re.I)
SENS = ("exact", "max", "min")
RACINES_CONTROLEES = ("resultats/", "article/")


# --------------------------------------------------------------------------- #
# Nombres                                                                      #
# --------------------------------------------------------------------------- #

def lit_nombre(brut: str) -> tuple[float, int] | None:
    """« 0,1535 » -> (0.1535, 4). Rend None si ce n'est pas un nombre.

    Le second membre est le nombre de decimales ECRITES : c'est lui, et non la
    precision du flottant, qui fixe la tolerance opposable.
    """
    t = brut.strip().replace("%", "").strip()
    t = t.replace(" ", "").replace(" ", "").replace(" ", "")
    if not re.fullmatch(r"[+-]?\d+(?:[.,]\d+)?", t):
        return None
    t = t.replace(",", ".")
    decimales = len(t.split(".")[1]) if "." in t else 0
    return float(t), decimales


def lit_cellule(brut: str) -> float | None:
    """Valeur d'une cellule de CSV. Accepte la notation scientifique."""
    t = (brut or "").strip().replace(" ", "").replace(" ", "")
    if not t:
        return None
    try:
        return float(t.replace(",", "."))
    except ValueError:
        return None


def verdict_arrondi(publiee: float, decimales: int, reelle: float,
                    sens: str) -> str | None:
    """Rend None si la valeur publiee est acceptable, sinon le constat."""
    ulp = 10.0 ** (-decimales)
    ecart = publiee - reelle
    # Garde-fou de representation : 0,15 - 0,1535 doit valoir -0,0035, pas
    # -0,0034999999999999996 compare a une borne. On arrondit l'ecart a la
    # precision publiee + 6, largement au-dela de ce qui est opposable.
    ecart = round(ecart, decimales + 6)
    if abs(ecart) >= ulp:
        return (f"valeur publiee {publiee:.{decimales}f} contre "
                f"{reelle:.10g} au CSV : ecart {ecart:+.10g}, "
                f"soit au moins un rang de la precision ecrite ({ulp:g})")
    if sens == "max" and ecart < 0:
        return (f"BORNE FRANCHIE : « au plus {publiee:.{decimales}f} » annonce "
                f"moins que la valeur reelle {reelle:.10g} (ecart {ecart:+.10g}). "
                f"L'arrondi passe du mauvais cote de la borne")
    if sens == "min" and ecart > 0:
        return (f"BORNE FRANCHIE : « au moins {publiee:.{decimales}f} » annonce "
                f"plus que la valeur reelle {reelle:.10g} (ecart {ecart:+.10g}). "
                f"L'arrondi passe du mauvais cote de la borne")
    return None


# --------------------------------------------------------------------------- #
# Lecture des CSV sources                                                      #
# --------------------------------------------------------------------------- #

_CACHE: dict[str, list[dict[str, str]] | None] = {}


def charge_csv(chemin: Path) -> list[dict[str, str]] | None:
    cle = str(chemin)
    if cle not in _CACHE:
        if not chemin.exists():
            _CACHE[cle] = None
        else:
            with chemin.open(encoding="utf-8", errors="replace", newline="") as f:
                _CACHE[cle] = list(csv.DictReader(f))
    return _CACHE[cle]


def resout_cellule(csv_rel: str, colonne: str, selecteurs: dict[str, str]
                   ) -> tuple[float | None, str | None]:
    """(valeur, motif d'echec). Une declaration irresolvable est une violation."""
    chemin = RACINE / csv_rel
    table = charge_csv(chemin)
    if table is None:
        return None, f"CSV source introuvable : {csv_rel}"
    if not table:
        return None, f"CSV source vide : {csv_rel}"
    if colonne not in table[0]:
        proches = [c for c in table[0] if colonne.lower() in (c or "").lower()][:3]
        indice = f" ; colonnes proches : {proches}" if proches else ""
        return None, f"colonne « {colonne} » absente de {csv_rel}{indice}"
    retenues = [l for l in table
                if all((l.get(k) or "").strip() == v for k, v in selecteurs.items())]
    if len(retenues) != 1:
        return None, (f"les selecteurs designent {len(retenues)} ligne(s) de "
                      f"{csv_rel}, il en faut exactement une")
    valeur = lit_cellule(retenues[0].get(colonne, ""))
    if valeur is None:
        return None, (f"la cellule designee de {csv_rel} [{colonne}] "
                      f"n'est pas un nombre : « {retenues[0].get(colonne, '')[:40]} »")
    return valeur, None


def lit_selecteurs(brut: str) -> tuple[dict[str, str] | None, str | None]:
    brut = brut.strip()
    if brut in ("-", ""):
        return {}, None
    out: dict[str, str] = {}
    for morceau in brut.split(";"):
        morceau = morceau.strip()
        if not morceau:
            continue
        if "=" not in morceau:
            return None, f"selecteur « {morceau[:40]} » sans « = »"
        k, v = morceau.split("=", 1)
        out[k.strip()] = v.strip()
    return out, None


# --------------------------------------------------------------------------- #
# (a) Marqueurs CHIFFRE: dans les fichiers de sortie                           #
# --------------------------------------------------------------------------- #

MODELE = ("CHIFFRE: <valeur> | <csv> | <colonne> | <cle=valeur ; cle=valeur | -> "
          "| x1 | exact|max|min")


def controle_fichier(constat: Constat, chemin: Path, compteur: dict[str, int]) -> None:
    if not chemin.exists():
        constat.viole(chemin, 1, "fichier absent", "verifier le chemin")
        return
    src = lignes(chemin)
    en_code = masque_code(src)
    for i, brute in enumerate(src, start=1):
        if en_code[i - 1]:
            continue
        m = RE_MARQUEUR.match(brute.rstrip())
        if not m:
            continue
        compteur["marqueurs"] += 1
        champs = [c.strip() for c in m.group(1).split("|")]
        if len(champs) != 6:
            constat.viole(chemin, i,
                          f"marqueur « CHIFFRE: » a {len(champs)} champ(s) au lieu de 6",
                          f"ecrire exactement : {MODELE}")
            continue
        brut_val, csv_rel, colonne, brut_sel, brut_ech, sens = champs

        lu = lit_nombre(brut_val)
        if lu is None:
            constat.viole(chemin, i,
                          f"« {brut_val[:40]} » n'est pas un nombre",
                          "le premier champ porte la valeur publiee, telle qu'elle "
                          "est ecrite dans la phrase (« 0,15 »)")
            continue
        publiee, decimales = lu

        if not csv_rel.endswith(".csv"):
            constat.viole(chemin, i, f"« {csv_rel[:60]} » n'est pas un chemin de CSV",
                          "chemin complet depuis la racine du depot, suffixe .csv")
            continue

        selecteurs, err = lit_selecteurs(brut_sel)
        if err:
            constat.viole(chemin, i, err,
                          "selecteurs de la forme « cle=valeur ; cle=valeur », ou « - »")
            continue

        me = RE_ECHELLE.match(brut_ech)
        if not me:
            constat.viole(chemin, i, f"echelle « {brut_ech[:20]} » non reconnue",
                          "ecrire x1, x100, x0.01 … : le multiplicateur applique a "
                          "la valeur du CSV avant comparaison")
            continue
        echelle = float(me.group(1).replace(",", "."))

        if sens not in SENS:
            constat.viole(chemin, i, f"sens « {sens[:20]} » inconnu",
                          f"employer l'un de {list(SENS)} : exact = arrondi fidele, "
                          f"max = plafond annonce, min = plancher annonce")
            continue

        reelle, err = resout_cellule(csv_rel, colonne, selecteurs)
        if err:
            constat.viole(chemin, i, err,
                          "une declaration qu'on ne peut pas resoudre n'est jamais "
                          "ignoree : corriger le chemin, la colonne ou les selecteurs")
            continue

        compteur["resolus"] += 1
        constat_arrondi = verdict_arrondi(publiee, decimales, reelle * echelle, sens)
        if constat_arrondi:
            constat.viole(chemin, i, constat_arrondi,
                          f"ecrire la valeur du CSV ({reelle * echelle:.10g}) a la "
                          f"precision voulue, ou reculer la borne du bon cote")


# --------------------------------------------------------------------------- #
# (b) Registre <-> CSV — dormant tant que `colonne=` n'est pas declaree        #
# --------------------------------------------------------------------------- #

RE_CSV_DANS_SOURCE = re.compile(r"([A-Za-z0-9_./-]+\.csv)")
RE_PARENTHESE = re.compile(r"\(([^)]*)\)")


def controle_registre(constat: Constat, chemin: Path, compteur: dict[str, int]) -> None:
    if not chemin.exists():
        constat.viole(chemin, 1, "registre absent",
                      "resultats/registre-chiffres.csv est la source des grandeurs")
        return
    with chemin.open(encoding="utf-8", newline="") as f:
        for n, ligne in enumerate(csv.DictReader(f), start=2):
            ident = (ligne.get("id") or "").strip()
            if not ident or ident.startswith("#"):
                continue
            if (ligne.get("statut") or "").strip() == "retracte":
                continue
            source = (ligne.get("csv_source") or "").strip()
            par = RE_PARENTHESE.search(source)
            selecteurs = {}
            if par:
                selecteurs, err = lit_selecteurs(par.group(1).replace(",", ";"))
                if err:
                    selecteurs = {}
            colonne = selecteurs.pop("colonne", None)
            echelle_txt = selecteurs.pop("echelle", "x1")
            if not colonne:
                compteur["registre_non_resolu"] += 1
                continue
            mcsv = RE_CSV_DANS_SOURCE.search(source)
            if not mcsv:
                constat.viole(chemin, n,
                              f"« {ident} » declare colonne={colonne} mais aucun "
                              f"chemin .csv dans csv_source",
                              "csv_source doit commencer par le chemin du CSV")
                continue
            me = RE_ECHELLE.match(echelle_txt)
            echelle = float(me.group(1).replace(",", ".")) if me else 1.0
            reelle, err = resout_cellule(mcsv.group(1), colonne, selecteurs)
            if err:
                constat.viole(chemin, n, f"« {ident} » : {err}",
                              "corriger le selecteur de csv_source")
                continue
            lu = lit_nombre(ligne.get("valeur") or "")
            if lu is None:
                compteur["registre_non_resolu"] += 1
                continue
            compteur["registre_resolu"] += 1
            c = verdict_arrondi(lu[0], lu[1], reelle * echelle, "exact")
            if c:
                constat.viole(chemin, n, f"« {ident} » : {c}",
                              "la graphie du registre doit etre un arrondi fidele "
                              "de la cellule qu'il declare (v2 §1.3)")


# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--depuis")
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--registre", default=str(REGISTRE))
    ap.add_argument("--registre-seul", action="store_true", help="controle (b) seul")
    ap.add_argument("--sans-registre", action="store_true", help="controle (a) seul")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)
    compteur = {"marqueurs": 0, "resolus": 0,
                "registre_resolu": 0, "registre_non_resolu": 0}

    if not a.sans_registre:
        chemin_reg = Path(a.registre)
        if not chemin_reg.is_absolute():
            chemin_reg = RACINE / chemin_reg
        controle_registre(constat, chemin_reg, compteur)
        constat.note(f"(b) registre : {compteur['registre_resolu']} ligne(s) "
                     f"rattachee(s) a une cellule, {compteur['registre_non_resolu']} "
                     f"sans selecteur « colonne= » (non controlees ; voir la "
                     f"procedure de migration du rapport P8/P9)")
    if a.registre_seul:
        return constat.conclure()

    cibles: list[Path] = []
    if a.fichier:
        cibles = [Path(f) if Path(f).is_absolute() else RACINE / f for f in a.fichier]
    elif a.depuis:
        if not git_dispo():
            return abandon(NOM, "git indisponible")
        from commun import fichiers_modifies
        for f in fichiers_modifies(a.depuis):
            p = RACINE / f
            if p.exists() and p.suffix in (".md", ".tex") \
                    and f.startswith(RACINES_CONTROLEES):
                cibles.append(p)
    elif a.tous:
        for r in RACINES_CONTROLEES:
            d = RACINE / r
            if d.is_dir():
                cibles += sorted(d.rglob("*.md")) + sorted(d.rglob("*.tex"))

    for c in cibles:
        controle_fichier(constat, c, compteur)
    constat.note(f"(a) {len(cibles)} fichier(s) lus ; {compteur['marqueurs']} "
                 f"marqueur(s) « CHIFFRE: », {compteur['resolus']} resolu(s) "
                 f"jusqu'a la cellule")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
