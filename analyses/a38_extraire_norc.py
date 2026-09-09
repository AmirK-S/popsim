"""
a38_extraire_norc : transcription des tables d'ampleur par item des rapports
methodologiques du GSS et de l'atlas NBER 2025, vers data/norc-mode/.

Statut : script d'analyse jetable, aucun appel de modele de langage. Il n'ecrit que dans
data/norc-mode/, repertoire nouveau et non versionne (data/ est dans .gitignore). Il ne
lit ni ne modifie data/traces/, data/osf-t6g7k-stanford/ ni aucun script existant.

Pourquoi cette forme. Les chiffres sont transcrits ICI, dans du code versionne, avec le
rapport, la table et la page d'ou ils viennent. Les fichiers de data/norc-mode/ ne sont que
la sortie derivee de cette transcription : ils ne sont pas versionnes, et un tiers qui
telecharge les PDF peut verifier ligne a ligne ce qui suit sans avoir a nous croire.

Sources telechargees le 8 septembre 2026 depuis gss.norc.org et nber.org, empreintes dans
data/norc-mode/PROVENANCE.md :

  MR099  Smith, T. W. et Dennis, J. M. (2004), *Comparing the Knowledge Networks
         Web-Enabled Panel and the In-Person 2002 General Social Survey*, GSS
         Methodological Report No. 99. Table 3, page 15 du PDF : distributions des 17
         items de depense, don't know exclus, GSS en face a face contre panel web
         Knowledge Networks, quatre traitements A a D. Nous retenons GSS contre KNS-A,
         qui est le traitement retenu par les auteurs eux memes pour la comparaison
         principale ("the version with the closest Don't-Know levels to the GSS as well
         as the largest sample", page 6).
  MR141  Sparkman, R., Wells, B. M., Norling-Ruggles, A., Schapiro, B. et Bautista, R.
         (2024), *The Effect of Question Presentation in Web-based Surveys*, GSS
         Methodological Report No. 141. Table 4, pages 10 a 12 du PDF : distributions
         web seulement, condition sans modalite volontaire contre condition avec, 2021
         et 2022. Nous retenons 2022, l'annee de la verite terrain de Stanford.
  MR010  Smith, T. W. (1981), *Qualifications to Generalized Absolutes*, GSS
         Methodological Report No. 10, repris dans POQ 45:224-230. Page 225 du PDF :
         part des repondants disant "non" a la question absolue qui approuvent au moins
         une situation concrete.
  MR021  Smith, T. W. (s. d.), *Discrepancies in Past Presidential Vote*, GSS
         Methodological Report No. 21. Page 3 du PDF pour la participation, page 9 pour
         le choix de candidat.
  MR086  Smith, T. W. (1995), *The Impact of the Presence of Others on a Respondent's
         Answers to Questions*, GSS Methodological Report No. 86. Page 10 du PDF, seul
         chiffre par item lisible dans le corps du texte.
  MR145  Schapiro, B. (2026), *Recent Changes in GSS Questions on Religion*, GSS
         Methodological Report No. 145. Consulte, tables 2 et 3 : ne porte que sur
         RELIG, DENOM et OTHER, aucune des trois n'est dans nos 149 items. Source
         verifiee et vide, consignee comme telle.
  ATLAS  Bursztyn, L., Haaland, I. K., Rover, N. et Roth, C. (2025), "The Social
         Desirability Atlas", NBER Working Paper 33920. Appendix Table A2, page 39, et
         Appendix Table A3, page 40.

Usage :
  .venv/bin/python analyses/a38_extraire_norc.py
"""

import hashlib
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEST = os.path.join(RACINE, "data", "norc-mode")

# ---------------------------------------------------------------------------
# MR099, Table 3, page 15. Colonnes : + = "too little", 0 = "about right",
# - = "too much". Don't know exclus des deux cotes par les auteurs.
# ---------------------------------------------------------------------------
# (libelle du rapport, variable GSS, item Stanford,
#  GSS+, GSS0, GSS-, KNSA+, KNSA0, KNSA-)
MR099_TABLE3 = [
    ("Space",     "NATSPAC",  "natspac/y",  11.8, 50.4, 37.7, 11.5, 49.8, 38.8),
    ("Enviro.",   "NATENVIR", "natenvir/y", 60.0, 33.2,  6.8, 60.5, 29.2, 10.3),
    ("Health",    "NATHEAL",  "natheal/y",  74.9, 21.3,  3.9, 69.3, 25.1,  5.6),
    ("Cities",    "NATCITY",  "natcity/y",  45.4, 39.9, 14.8, 34.4, 44.5, 21.1),
    ("Crime",     "NATCRIME", "",           57.4, 35.8,  6.8, 51.7, 40.8,  7.4),
    ("Drugs",     "NATDRUG",  "natdrug/y",  59.1, 31.2,  9.7, 45.1, 38.2, 16.7),
    ("Educ.",     "NATEDUC",  "nateduc/y",  73.9, 20.7,  5.4, 73.5, 19.9,  6.6),
    ("Blacks",    "NATRACE",  "natrace/y",  32.7, 49.0, 18.3, 23.0, 44.9, 32.1),
    ("Defense",   "NATARMS",  "natarms/y",  31.3, 46.5, 22.3, 32.5, 44.3, 23.1),
    ("ForAffs",   "NATAID",   "nataid/y",    6.7, 27.8, 65.5,  6.1, 19.9, 74.0),
    ("Welfare",   "NATFARE",  "natfare/y",  21.2, 38.2, 40.6, 18.5, 31.2, 50.3),
    ("Hghwys.",   "NATROAD",  "natroad",    35.7, 51.7, 12.7, 35.3, 51.9, 12.8),
    ("SocSec.",   "NATSOC",   "natsoc",     60.8, 34.6,  4.6, 62.4, 32.3,  5.4),
    ("MassTrn",   "NATMASS",  "natmass",    37.0, 52.4, 10.7, 37.5, 49.3, 13.2),
    ("Parks",     "NATPARK",  "natpark",    35.0, 59.5,  5.5, 37.8, 52.8,  9.4),
    ("Childcare", "NATCHLD",  "natchld",    59.1, 33.2,  7.7, 53.3, 37.2,  9.5),
    ("Science",   "NATSCI",   "natsci",     36.4, 49.7, 13.9, 31.6, 52.4, 16.0),
]

# ---------------------------------------------------------------------------
# MR141, Table 4, pages 10 a 12, colonnes 2022, cas web seulement.
# Chaque entree : item Stanford, mnemonique NORC, modalite volontaire, puis la liste
# (libelle de modalite, part sans modalite volontaire, part avec).
# ---------------------------------------------------------------------------
MR141_TABLE4_2022 = {
    "aged": ("AGEDV", "It depends", [
        ("A good idea", 66.9, 25.5), ("A bad idea", 33.1, 10.5),
        ("It depends", 0.0, 63.9)]),
    "courts": ("COURTSV", "About right", [
        ("Too harshly", 28.3, 9.8), ("Not harshly enough", 71.3, 49.7),
        ("About right", 0.4, 40.5)]),
    "divlaw": ("DIVLAWV", "Stay as is", [
        ("Easier", 68.0, 33.1), ("More difficult", 32.0, 12.5),
        ("Stay as is", 0.0, 54.4)]),
    "fair": ("FAIRV", "It depends", [
        ("Would take advantage", 56.5, 26.6), ("Would try to be fair", 43.3, 30.3),
        ("It depends", 0.2, 43.2)]),
    "getahead": ("GETAHEADV", "Equally important", [
        ("Hard work most important", 79.9, 50.3), ("Equally important", 0.0, 43.5),
        ("Luck more important", 20.1, 6.2)]),
    "helpful": ("HELPFULV", "It depends", [
        ("Try to be helpful", 50.5, 25.6), ("Looking out for themselves", 49.4, 29.1),
        ("It depends", 0.0, 45.2)]),
    "trust": ("TRUSTV", "It depends", [
        ("Can trust", 31.6, 16.6), ("Can't be too careful", 68.4, 44.0),
        ("It depends", 0.0, 39.3)]),
    "discaffw": ("DISCAFFWV", "Don't know", [
        ("Very likely", 25.7, 18.6), ("Somewhat likely", 45.8, 41.3),
        ("Not very likely", 19.7, 22.3), ("Very unlikely", 8.8, 10.5),
        ("Don't know", 0.0, 7.3)]),
    "fepol": ("FEPOLV", "Don't know", [
        ("Agree", 10.5, 7.8), ("Disagree", 89.5, 78.1), ("Don't know", 0.0, 14.1)]),
    "grass": ("GRASSV", "No opinion", [
        ("Should be legal", 75.4, 62.9), ("Should not be legal", 24.6, 22.0),
        ("No opinion", 0.0, 15.1)]),
    "postlife": ("POSTLIFEV", "Don't know", [
        ("Yes", 69.3, 59.2), ("No", 30.7, 14.8), ("Don't know", 0.0, 26.0)]),
    "prayer": ("PRAYERV", "No opinion", [
        ("Approve", 67.4, 52.2), ("Disapprove", 32.6, 30.2), ("No opinion", 0.0, 17.7)]),
    "uswary": ("USWARYV", "Don't know", [
        ("Yes", 54.9, 46.0), ("No", 45.1, 33.6), ("Don't know", 0.0, 20.5)]),
    "bible": ("BIBLEV", "Something else/Other", [
        ("Word of God", 21.6, 17.5), ("Inspired word", 42.9, 46.8),
        ("Ancient book", 35.4, 25.7), ("Something else/Other", 0.0, 9.9)]),
    "kidssol": ("KIDSSOLV", "No children", [
        ("Much better", 17.0, 17.8), ("Somewhat better", 29.8, 26.0),
        ("About the same", 24.9, 19.2), ("Somewhat worse", 18.8, 17.6),
        ("Much worse", 9.6, 8.3), ("No children", 0.0, 11.0)]),
    # USCITZNV : les deux dernieres modalites sont celles qui n'apparaissent que dans la
    # condition experimentale ; elles sont traitees ensemble comme "modalite volontaire".
    "uscitzn*": ("USCITZNV", "Citizen born in PR, USVI, N. Marianas", [
        ("A U.S. citizen", 59.9, 47.0), ("Not a U.S. citizen", 40.1, 49.4),
        ("Citizen born in PR, USVI, N. Marianas", 0.0, 0.4),
        ("Born outside U.S. to U.S. citizen parents", 0.0, 3.1)]),
    "fucitzn": ("FUCITZNV", "Not eligible to become a U.S. citizen", [
        ("Currently applying", 3.6, 10.3), ("Planning to apply", 46.7, 50.5),
        ("Not planning to apply", 49.7, 11.0),
        ("Not eligible to become a U.S. citizen", 0.0, 28.2)]),
}

# ---------------------------------------------------------------------------
# MR010, page 225. La question generale est POLHITOK ("Are there any situations you can
# imagine in which you would approve of a policeman striking an adult male citizen?"),
# les quatre situations sont POLABUSE (paroles vulgaires), POLMURDR (suspect de meurtre),
# POLESCAP (tentative de fuite) et POLATTAK (attaque du policier aux poings) ; l'appendice
# du rapport donne le libelle exact des cinq. La question generale sur l'homme adulte n'a
# pas d'equivalent dans nos 149 items.
# ---------------------------------------------------------------------------
MR010 = [
    ("polhitok/y", "POLHITOK", 86.0, 1.52, 1.1,
     "part des 'non' a la question absolue qui approuvent au moins une des quatre "
     "situations concretes ; 1,52 situation approuvee en moyenne ; seuls 1,1 pour cent "
     "des 'oui' n'approuvent aucune situation"),
]

# ---------------------------------------------------------------------------
# MR021, pages 3 et 9.
# ---------------------------------------------------------------------------
MR021 = [
    ("vote16", "VOTE16", 10.0,
     "la participation declaree au GSS depasse d'environ 10 points les estimations "
     "tirees des resultats officiels (page 3)"),
    ("pres16", "PRES16", 3.3,
     "ecart absolu moyen de 3,3 points entre le choix de candidat declare au GSS et les "
     "resultats ; effet de maison de 4,2 points vers le candidat democrate (page 9)"),
    ("if16who", "IF16WHO", 3.3, "meme mesure que PRES16, question posee aux non votants"),
]

# ---------------------------------------------------------------------------
# MR086, page 10. Seul chiffre par item lisible dans le corps du texte : la sante auto
# declaree. Les tables 2, 4 et 5 du rapport ne donnent que des niveaux de probabilite, et
# la mise en page du PDF numerise ne permet pas de les rattacher a coup sur a leur ligne.
# ---------------------------------------------------------------------------
MR086 = [
    ("health", "HEALTH", 5.0,
     "29 pour cent d'« excellente » quand quelqu'un est present contre 34 pour cent "
     "seul ; 35, 31 et 23,5 pour cent pour 0, 1 et 2 personnes et plus (page 10). "
     "Seule association survivant aux controles"),
]

# ---------------------------------------------------------------------------
# Atlas NBER 2025, Appendix Table A2 page 39 et Appendix Table A3 page 40. Le critere
# d'inclusion de l'atlas est severe : uniquement les etudes qui apparient declaration et
# registre au niveau de l'individu. Il ne couvre donc que des COMPORTEMENTS verifiables,
# et deux de nos 149 items seulement tombent dans un de ses six domaines.
# ---------------------------------------------------------------------------
ATLAS = [
    ("vote16", "voting", "Kleven (2022), non-voting Norway 1969-2021, N = 26 333",
     14.0, 11.0, 3.0, 96.0, 26.0, 1.0),
    ("unemp", "economic outcomes",
     "Dutz et al. (2021), applied for unemployment insurance, N = 1 700",
     9.0, 8.0, 1.0, 98.0, float("nan"), float("nan")),
]
# Valeurs de l'atlas non appariables a un de nos items, conservees pour memoire dans le
# fichier de sortie : elles servent a montrer que le domaine du comportement verifiable
# est presque vide sur le GSS attitudinal.
ATLAS_HORS_PERIMETRE = [
    ("Completion of Tertiary Education", "education", 37.0, 43.0, 6.0),
    ("Covid Vaccinated", "health behaviors", 67.0, 69.0, 2.0),
    ("Current Smoker (Female Soldiers)", "health behaviors", 26.0, 19.0, 7.0),
    ("Smoking During Pregnancy", "health behaviors", 15.0, 13.0, 2.0),
    ("Business Tax Evasion in Uganda", "criminal behavior", float("nan"),
     float("nan"), float("nan")),
    ("Return Erroneously Received Money", "moral behavior", 32.0, 65.0, 33.0),
]


def tv(a, b):
    """Distance de variation totale entre deux distributions donnees en pourcentages.

    Les deux vecteurs sont renormalises avant comparaison : les tables des rapports sont
    arrondies au dixieme et ne somment pas toujours exactement a 100. Le resultat est
    rendu en POINTS de pourcentage, echelle 0 a 100, pour rester homogene avec les
    ampleurs que les rapports enoncent en points.
    """
    sa, sb = sum(a), sum(b)
    pa = [v / sa for v in a]
    pb = [v / sb for v in b]
    return 50.0 * sum(abs(u - v) for u, v in zip(pa, pb))


def main():
    os.makedirs(DEST, exist_ok=True)
    ecrits = []

    # ---------------------------------------------------------------- MR099
    lignes = []
    for lib, var, item, gp, gz, gm, kp, kz, km in MR099_TABLE3:
        lignes.append({
            "item_stanford": item, "variable_gss": var, "libelle_mr099": lib,
            "gss_ftf_trop_peu": gp, "gss_ftf_juste": gz, "gss_ftf_trop": gm,
            "knsa_web_trop_peu": kp, "knsa_web_juste": kz, "knsa_web_trop": km,
            # l'ampleur que NORC enonce lui meme dans le corps du texte, page 6 :
            # "% not too much on GSS moins % not too much in KNS"
            "ampleur_norc_pas_trop": round((100.0 - gm) - (100.0 - km), 1),
            "ampleur_tv_points": round(tv([gp, gz, gm], [kp, kz, km]), 2),
            "signe_vers_depense": round((gp - kp), 1),
            "source": "MR099 Table 3 page 15, GSS face a face contre KNS-A web, DK exclus",
        })
    d = pd.DataFrame(lignes)
    d.to_csv(os.path.join(DEST, "mr099-depenses.csv"), index=False)
    ecrits.append(("mr099-depenses.csv", len(d)))

    # ---------------------------------------------------------------- MR141
    lignes = []
    for item, (mnem, vol, mods) in MR141_TABLE4_2022.items():
        sans = [m[1] for m in mods]
        avec = [m[2] for m in mods]
        # part de la condition experimentale qui prend la ou les modalites que la
        # condition de controle n'offrait pas, c'est a dire celles dont la part est nulle
        # ou quasi nulle sans modalite volontaire
        part_vol = sum(m[2] for m in mods if m[1] <= 0.5)
        lignes.append({
            "item_stanford": item, "mnemonique_norc": mnem,
            "modalite_volontaire": vol,
            "part_volontaire_2022_web": round(part_vol, 1),
            "ampleur_tv_points": round(tv(sans, avec), 2),
            "n_modalites": len(mods),
            "detail": " | ".join(f"{m[0]}={m[1]}/{m[2]}" for m in mods),
            "source": "MR141 Table 4 pages 10 a 12, colonnes 2022, cas web seulement",
        })
    d = pd.DataFrame(lignes)
    d.to_csv(os.path.join(DEST, "mr141-modalite-volontaire.csv"), index=False)
    ecrits.append(("mr141-modalite-volontaire.csv", len(d)))

    # ------------------------------------------------- MR010, MR021, MR086, atlas
    d = pd.DataFrame(
        [{"item_stanford": i, "variable_gss": v, "ampleur_points": a,
          "situations_approuvees_moyenne": m, "faux_positifs_pourcent": f,
          "source": "MR010 page 225", "detail": s} for i, v, a, m, f, s in MR010])
    d.to_csv(os.path.join(DEST, "mr010-absolu-contre-situationnel.csv"), index=False)
    ecrits.append(("mr010-absolu-contre-situationnel.csv", len(d)))

    d = pd.DataFrame(
        [{"item_stanford": i, "variable_gss": v, "ampleur_points": a,
          "source": "MR021 pages 3 et 9", "detail": s} for i, v, a, s in MR021])
    d.to_csv(os.path.join(DEST, "mr021-vote-declare.csv"), index=False)
    ecrits.append(("mr021-vote-declare.csv", len(d)))

    d = pd.DataFrame(
        [{"item_stanford": i, "variable_gss": v, "ampleur_points": a,
          "source": "MR086 page 10", "detail": s} for i, v, a, s in MR086])
    d.to_csv(os.path.join(DEST, "mr086-presence-de-tiers.csv"), index=False)
    ecrits.append(("mr086-presence-de-tiers.csv", len(d)))

    lignes = [{"item_stanford": i, "domaine": dom, "etude": et,
               "prevalence_reelle": vr, "prevalence_declaree": vd,
               "ampleur_points": amp, "exactitude": ex,
               "faux_positifs": fp, "faux_negatifs": fn,
               "source": "Atlas NBER 33920, Appendix Table A2 page 39 et A3 page 40"}
              for i, dom, et, vr, vd, amp, ex, fp, fn in ATLAS]
    lignes += [{"item_stanford": "", "domaine": dom, "etude": nom,
                "prevalence_reelle": vr, "prevalence_declaree": vd,
                "ampleur_points": amp, "exactitude": float("nan"),
                "faux_positifs": float("nan"), "faux_negatifs": float("nan"),
                "source": "Atlas NBER 33920, Appendix Table A2 page 39, hors de nos items"}
               for nom, dom, vr, vd, amp in ATLAS_HORS_PERIMETRE]
    d = pd.DataFrame(lignes)
    d.to_csv(os.path.join(DEST, "atlas-nber-2025.csv"), index=False)
    ecrits.append(("atlas-nber-2025.csv", len(d)))

    # ---------------------------------------------------------------- provenance
    prov = f"""# Provenance des ampleurs de mode par item, data/norc-mode/

Repertoire NON VERSIONNE (`data/` est dans `.gitignore`). Il est integralement
regenere par `analyses/a38_extraire_norc.py`, ou les chiffres sont transcrits a la
main du PDF avec leur table et leur page. Le code est la source, ce repertoire est la
sortie.

Telechargements du 8 septembre 2026.

| fichier | rapport | table et page | items couverts |
|---|---|---|---|
| `mr099-depenses.csv` | GSS Methodological Report No. 99, Smith et Dennis 2004 | Table 3, page 15 | 17 items de depense, dont 16 dans nos 149 |
| `mr141-modalite-volontaire.csv` | GSS Methodological Report No. 141, Sparkman et al. 2024 | Table 4, pages 10 a 12, colonnes 2022 web | 19 items, dont 17 dans nos 149 |
| `mr010-absolu-contre-situationnel.csv` | GSS Methodological Report No. 10, Smith 1981 | page 225 | 1 item |
| `mr021-vote-declare.csv` | GSS Methodological Report No. 21, Smith | pages 3 et 9 | 3 items |
| `mr086-presence-de-tiers.csv` | GSS Methodological Report No. 86, Smith 1995 | page 10 | 1 item |
| `atlas-nber-2025.csv` | NBER Working Paper 33920, Bursztyn, Haaland, Rover et Roth 2025 | Appendix Table A2 page 39, Appendix Table A3 page 40 | 2 items, plus 6 lignes hors perimetre |

URL exactes :

- MR099 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR99%20Comparing%20the%20Knowledge%20Networks%20Web-Enabled%20Panel%20and%20the%20In-Person%202002%20GSS.pdf
- MR141 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR141%20Grid%20And%20Volunteered%20Response%20Experiments.pdf
- MR010 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR010.pdf
- MR021 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR021.pdf
- MR086 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/MR086.pdf
- MR145 : https://gss.norc.org/content/dam/gss/get-documentation/pdf/reports/methodological-reports/GSS%20MR145%20Recent%20Religion%20Question%20Changes.pdf
- Atlas : https://www.nber.org/system/files/working_papers/w33920/w33920.pdf

Sources verifiees et vides, consignees pour qu'on ne les rouvre pas :

- **MR145** (religion, mars 2026) donne bien un ecart de mode par modalite, 2022 face a
  face contre web : protestants 45,4 contre 36,1 pour cent, sans religion 24,3 contre
  32,7, catholiques 20,9 contre 21,4. Mais il ne porte que sur RELIG, DENOM et OTHER,
  aucune des trois n'etant dans nos 149 items ; `relig16*` et `jew16*` sont la religion
  a 16 ans, une autre variable. Ampleur inutilisable ici.
- **MR086** ne publie, item par item, que des niveaux de probabilite dans des tables dont
  la numerisation ne permet pas de rattacher a coup sur une valeur a sa ligne. Seul le
  chiffre de la sante auto declaree figure dans le corps du texte, il est repris.
- **L'atlas NBER** n'inclut que des etudes appariant declaration et registre au niveau de
  l'individu, donc uniquement des comportements verifiables. Sur 149 items du GSS
  attitudinal, deux seulement tombent dans un de ses six domaines.

Empreintes SHA-256 des PDF :

"""
    scratch = os.environ.get("A38_PDF_DIR", "")
    if scratch and os.path.isdir(scratch):
        for nom in sorted(os.listdir(scratch)):
            if nom.lower().endswith(".pdf"):
                h = hashlib.sha256(open(os.path.join(scratch, nom), "rb").read())
                prov += f"- `{nom}` : `{h.hexdigest()}`\n"
    else:
        prov += ("- non calculees : le repertoire des PDF n'a pas ete passe par la "
                 "variable d'environnement `A38_PDF_DIR`.\n")

    open(os.path.join(DEST, "PROVENANCE.md"), "w").write(prov)
    ecrits.append(("PROVENANCE.md", 0))

    print(f"ecrit dans {DEST} :")
    for nom, n in ecrits:
        print(f"  {nom:<42} {n if n else ''}")


if __name__ == "__main__":
    main()
