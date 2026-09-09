"""
a25_commun : le croisement NORC x nos 149 items, et la definition item par item de la
modalite socialement desirable.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; tout est importe.

Ce module ne calcule rien, il declare. Il porte trois choses et rien d'autre :

  1. les trois listes de NORC (2023), *2022 GSS Cross-section, Mode Sensitivity in the
     2022 GSS, Release 1*, recopiees a l'identique du PDF officiel telecharge le
     8 septembre 2026 sur gss.norc.org. Ce sont 163 variables reparties en trois classes :
     "Likely mode sensitive" (23), "Requires further investigation" (21), "Less likely to
     be mode sensitive" (119 entrees ecrites, dont un doublon).
  2. la table de correspondance entre le nom de colonne de l'archive de Stanford et le ou
     les noms de variables du GSS. Les suffixes "/y" de Stanford fusionnent la version
     historique et la version reformulee 2021 d'une meme question, or NORC classe parfois
     les deux dans des classes differentes. Ces items sont marques "mixte" et sortent des
     deux bras du test.
  3. la modalite socialement desirable, item par item, avec sa source et son niveau de
     confiance. C'est la partie discutable du protocole et elle est ecrite ici en clair
     pour qu'un relecteur puisse la contester ligne a ligne.

Aucune microdonnee n'est ecrite par ce module.
"""

import json
import os

# ---------------------------------------------------------------------------
# 1. Les trois listes de NORC, recopiees du PDF
#    2022 GSS Mode Sensitivity Note v1, gss.norc.org, telecharge le 8 septembre 2026.
# ---------------------------------------------------------------------------

NORC_SENSIBLE = [
    "ATTEND", "CHLDIDEL", "CONEDUC", "CONLEGIS", "CONMEDIC", "IF20WHO",
    "MARBLK", "MEOVRWRK", "NATCHLD", "NATFAREY", "NATRACE", "NATRACEY",
    "NATROAD", "PARTYID", "POLABUSE", "POLATTAK", "POLMURDR", "SOCBAR",
    "SPKRAC", "VOTE16", "VOTE20", "WORDSUM", "XMARSEX",
]

NORC_INVESTIGUER = [
    "ABANY", "ABPOOR", "ABRAPE", "ADULTS", "CONARMY", "FAMDIF16",
    "FEFAM", "FEJOBAFF", "FEPRESCH", "IF16WHO", "NATCITYY", "NATCRIMY",
    "NATHEAL", "NATSPACY", "NEWS", "PILLOK", "PRAY", "REBORN",
    "RELPERSN", "SAVESOUL", "SUICIDE1",
]

# RELPERSN figure a la fois en "Requires further investigation" et en "Less likely" dans
# le PDF. C'est une incoherence de la source, signalee telle quelle. L'item n'est de toute
# facon pas dans nos 149, il est dans la liste d'exclusion de Stanford.
NORC_MOINS = [
    "ABDEFECT", "ABHLTH", "ABNOMORE", "ABSINGLE", "CAPPUN", "CHILDS",
    "COLATH", "COLRAC", "COMPUSE", "CONBUS", "CONCLERG", "CONFED",
    "CONFINAN", "CONJUDGE", "CONLABOR", "CONPRESS", "CONSCI", "CONTV",
    "DISCAFF", "DIVORCE", "DWELOWN", "EARNRS", "EQWLTH", "EVWORK",
    "FAMILY16", "FEAR", "FECHLD", "FINALTER", "FINRELA", "GOD",
    "GUNLAW", "HAPCOHAB", "HAPPY", "HEALTH", "HELPBLK", "HELPPOOR",
    "HELPSICK", "HOMOSEX", "INCOM16", "JOBFIND", "LETDIE1", "LETIN1A",
    "LIBATH", "LIBCOM", "LIFE", "MARHOMO", "NATAID", "NATAIDY",
    "NATARMS", "NATARMSY", "NATCITY", "NATCRIME", "NATDRUG", "NATDRUGY",
    "NATEDUC", "NATEDUCY", "NATENRGY", "NATENVIR", "NATENVIY", "NATFARE",
    "NATHEALY", "NATMASS", "NATPARK", "NATSCI", "NATSOC", "NATSPAC",
    "OTHLANG", "OWNGUN", "PARSOL", "PISTOL", "POLESCAP", "POLHITOK",
    "POLVIEWS", "PORNLAW", "POSSLQ", "POSSLQY", "PREMARSX", "PRES16",
    "PRES20", "RACDIF1", "RACDIF1Y", "RACDIF2", "RACDIF3", "RACDIF4",
    "RACEACS1", "RACEACS2", "RACEACS3", "RACEACS4", "RACEACS5", "RACEACS6",
    "RACEACS7", "RACEACS15", "RACEACS16", "RACLIVE", "RACWORK", "RANK",
    "REG16", "RELPERSN", "RES16", "RICHWORK", "RIFLE", "ROWNGUN",
    "SATFIN", "SATJOB", "SEXEDUC", "SHOTGUN", "SOCFREND", "SOCOMMUN",
    "SOCREL", "SPANKING", "SPKATH", "SPKLANG", "SUICIDE4", "TEENSEX",
    "UNEMP", "WIDOWED", "WRKSLF", "WRKSTAT", "WRKWAYUP",
]

# ---------------------------------------------------------------------------
# 2. Correspondance nom de colonne Stanford -> variables du GSS
#    Le suffixe "/y" fusionne la forme historique et la forme reformulee 2021. Le suffixe
#    "*" de Stanford n'est pas un joker, il fait partie du nom de colonne.
# ---------------------------------------------------------------------------

CORRESPONDANCE = {
    "natspac/y": ["NATSPAC", "NATSPACY"],
    "natenvir/y": ["NATENVIR", "NATENVIY"],
    "natheal/y": ["NATHEAL", "NATHEALY"],
    "natcity/y": ["NATCITY", "NATCITYY"],
    "natdrug/y": ["NATDRUG", "NATDRUGY"],
    "nateduc/y": ["NATEDUC", "NATEDUCY"],
    "natrace/y": ["NATRACE", "NATRACEY"],
    "natarms/y": ["NATARMS", "NATARMSY"],
    "nataid/y": ["NATAID", "NATAIDY"],
    "natfare/y": ["NATFARE", "NATFAREY"],
    "natroad": ["NATROAD"],
    "natsoc": ["NATSOC"],
    "natmass": ["NATMASS"],
    "natpark": ["NATPARK"],
    "natchld": ["NATCHLD"],
    "natsci": ["NATSCI"],
    "natenrgy": ["NATENRGY"],
    "posslq/y": ["POSSLQ", "POSSLQY"],
    "racdif1": ["RACDIF1", "RACDIF1Y"],
    "racdif2": ["RACDIF2"],
    "racdif3": ["RACDIF3"],
    "racdif4": ["RACDIF4"],
    "spkath/y": ["SPKATH"],
    "spkrac/y": ["SPKRAC"],
    "colath": ["COLATH"],
    "colrac": ["COLRAC"],
    "libcom/y": ["LIBCOM"],
    "polhitok/y": ["POLHITOK"],
    "polabuse/y": ["POLABUSE"],
    "polattak/y": ["POLATTAK"],
    "compuse*": ["COMPUSE"],
    # 'divorced' est le libelle Stanford de la question "avez vous deja divorce", qui est
    # DIVORCE au GSS. Correspondance deduite du libelle, pas du dictionnaire, donc
    # signalee comme incertaine dans le tableau de croisement.
    "divorced": ["DIVORCE"],
    "incom16": ["INCOM16"],
    "conarmy": ["CONARMY"], "conbus": ["CONBUS"], "conclerg": ["CONCLERG"],
    "coneduc": ["CONEDUC"], "confed": ["CONFED"], "confinan": ["CONFINAN"],
    "conjudge": ["CONJUDGE"], "conlabor": ["CONLABOR"], "conlegis": ["CONLEGIS"],
    "conmedic": ["CONMEDIC"], "conpress": ["CONPRESS"], "consci": ["CONSCI"],
    "contv": ["CONTV"],
    "abdefect": ["ABDEFECT"], "abnomore": ["ABNOMORE"], "abhlth": ["ABHLTH"],
    "abpoor": ["ABPOOR"], "abrape": ["ABRAPE"], "absingle": ["ABSINGLE"],
    "abany": ["ABANY"],
    "letdie1": ["LETDIE1"], "suicide1": ["SUICIDE1"], "suicide4": ["SUICIDE4"],
    "fechld": ["FECHLD"], "fepresch": ["FEPRESCH"], "fefam": ["FEFAM"],
    "pillok": ["PILLOK"], "xmarsex": ["XMARSEX"], "homosex": ["HOMOSEX"],
    "marhomo": ["MARHOMO"], "discaff": ["DISCAFF"], "spanking": ["SPANKING"],
    "sexeduc": ["SEXEDUC"], "pornlaw": ["PORNLAW"], "cappun": ["CAPPUN"],
    "gunlaw": ["GUNLAW"], "owngun": ["OWNGUN"], "satfin": ["SATFIN"],
    "satjob": ["SATJOB"], "happy": ["HAPPY"], "finalter": ["FINALTER"],
    "finrela": ["FINRELA"], "parsol": ["PARSOL"], "letin1a": ["LETIN1A"],
    "racwork": ["RACWORK"], "health": ["HEALTH"], "life": ["LIFE"],
    "othlang": ["OTHLANG"], "richwork": ["RICHWORK"], "unemp": ["UNEMP"],
    "evwork": ["EVWORK"], "wrkstat": ["WRKSTAT"], "jobfind": ["JOBFIND"],
    "attend": ["ATTEND"], "pray": ["PRAY"], "reborn": ["REBORN"],
    "savesoul": ["SAVESOUL"], "news": ["NEWS"], "vote16": ["VOTE16"],
    "pres16": ["PRES16"], "if16who": ["IF16WHO"],
}


def classe_norc(item):
    """Renvoie la classe NORC d'un item de Stanford.

    'sensible'    : toutes les variables GSS correspondantes sont "Likely mode sensitive"
    'investiguer' : toutes sont "Requires further investigation"
    'temoin'      : toutes sont "Less likely to be mode sensitive"
    'mixte'       : les variables correspondantes ne sont pas dans la meme classe, ce qui
                    arrive pour les items ou Stanford fusionne la forme historique et la
                    forme 2021 d'une question que NORC classe separement
    'non teste'   : aucune correspondance dans les 163 variables examinees par NORC
    """
    vars_gss = CORRESPONDANCE.get(item)
    if not vars_gss:
        return "non teste", []
    classes = set()
    for v in vars_gss:
        if v in NORC_SENSIBLE:
            classes.add("sensible")
        elif v in NORC_INVESTIGUER:
            classes.add("investiguer")
        elif v in NORC_MOINS:
            classes.add("temoin")
        else:
            classes.add("non teste")
    if len(classes) == 1:
        return classes.pop(), vars_gss
    return "mixte", vars_gss


# ---------------------------------------------------------------------------
# 3. La modalite socialement desirable, item par item
# ---------------------------------------------------------------------------
#
# Convention. Chaque entree vaut (regle, argument, niveau, source).
#
#   regle "ordre"    : l'argument vaut +1 si la desirabilite croit dans l'ordre des
#                      modalites tel qu'il est declare dans question_master/gss/main.csv,
#                      et -1 si elle decroit. Le score de desirabilite d'une modalite de
#                      rang r sur K est alors r/(K-1) ou 1 - r/(K-1).
#   regle "ensemble" : l'argument est l'ensemble des modalites desirables, qui recoivent
#                      le score 1 ; les autres recoivent 0.
#   regle "aucune"   : pas de pole defini. L'item entre dans les mesures d'ecart de
#                      distribution et d'exactitude, jamais dans la mesure de sens.
#
#   niveau : [CONFIRME] direction donnee explicitement par NORC dans la note de mode ;
#            [PROBABLE] direction etablie par une mesure publiee sur le meme item ou sur
#            le meme domaine ; [HYPOTHESE] direction deduite d'une norme sociale sans
#            mesure directe sur cet item.
#
# Les modalites "Inapplicable ..." ne recoivent aucun score : la part de cellules sans
# score est rapportee condition par condition dans les tableaux.

DESIRABILITE = {
    # --- religion : NORC mesure une chute nette de la pratique et de la croyance sur le
    #     web, donc le pole observe est le pole religieux
    "attend": ("ordre", +1, "[CONFIRME]",
               "NORC : ATTEND chute nettement sur le web ; Presser et Stinson 1998 "
               "(corpus 04-13) : un tiers de pratique hebdomadaire en moins sans enqueteur"),
    "pray": ("ordre", -1, "[CONFIRME]",
             "NORC : PRAY chute sur le web ; modalites listees de 'plusieurs fois par jour' "
             "a 'jamais', donc la desirabilite decroit dans l'ordre"),
    "reborn": ("ensemble", {"yes"}, "[CONFIRME]",
               "NORC : REBORN chute sur le web"),
    "savesoul": ("ensemble", {"yes"}, "[CONFIRME]",
                 "NORC : SAVESOUL chute sur le web"),
    # --- confiance dans les institutions : NORC donne la direction, la confiance est plus
    #     haute en face a face
    "coneduc": ("ordre", -1, "[CONFIRME]", "NORC : CONEDUC passe de 'a great deal' en face "
                "a face a 'only some' / 'hardly any' sur le web"),
    "conlegis": ("ordre", -1, "[CONFIRME]", "NORC : idem CONLEGIS"),
    "conmedic": ("ordre", -1, "[CONFIRME]", "NORC : idem CONMEDIC"),
    "conarmy": ("ordre", -1, "[HYPOTHESE]", "meme echelle et meme pole que les trois items "
                "de confiance ou NORC donne la direction ; CONARMY est en zone grise"),
    "conbus": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "conclerg": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "confed": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "confinan": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "conjudge": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "conlabor": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "conpress": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "consci": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    "contv": ("ordre", -1, "[HYPOTHESE]", "meme echelle, meme pole, temoin"),
    # --- depenses publiques : regle uniforme, dire 'trop peu' est la reponse genereuse.
    #     NORC constate un deplacement vers un des deux poles selon le sujet mais ne donne
    #     pas la direction item par item. La regle est donc une hypothese, appliquee de
    #     facon identique aux items sensibles et aux temoins pour ne pas creer d'ecart par
    #     construction.
    **{it: ("ordre", -1, "[HYPOTHESE]",
            "regle uniforme sur les items de depense : 'too little' est le pole genereux ; "
            "NORC ne donne pas la direction item par item")
       for it in ["natspac/y", "natenvir/y", "natheal/y", "natcity/y", "natdrug/y",
                  "nateduc/y", "natrace/y", "natarms/y", "nataid/y", "natfare/y",
                  "natroad", "natsoc", "natmass", "natpark", "natchld", "natsci",
                  "natenrgy"]},
    # --- vote : la sur declaration du vote est le cas d'ecole. Attention, NORC mesure sur
    #     le GSS 2022 un vote declare PLUS eleve sur le web, soit l'inverse du sens attendu.
    "vote16": ("ensemble", {"voted"}, "[PROBABLE]",
               "Ansolabehere et Hersh 2012 (corpus 04-20) : 15,8 points d'ecart au registre, "
               "52 pour cent des non votants declarent avoir vote. Contradiction assumee : "
               "NORC mesure un vote declare plus eleve sur le web, donc sans enqueteur"),
    "pres16": ("aucune", None, "[CONFIRME]",
               "aucun pole : Enns, Lagodny et Schuldt 2017 (corpus 04-30) et AAPOR 2020 "
               "(04-31) ecartent l'electeur qui se cache comme explication"),
    "if16who": ("aucune", None, "[HYPOTHESE]", "choix de candidat, pas de pole desirable"),
    # --- moeurs et sexualite
    "xmarsex": ("ordre", -1, "[PROBABLE]",
                "Tourangeau et Yan 2007 (corpus 04-03) : les items de conduite sexuelle sont "
                "sur declares du cote de la norme ; 'always wrong' est le pole normatif"),
    "homosex": ("ordre", +1, "[PROBABLE]",
                "Coffman, Coffman et Ericson 2017 (corpus 04-21) : l'hostilite envers les gays "
                "est sous declaree en question directe, donc 'not wrong at all' est le pole "
                "declare en exces"),
    "marhomo": ("ordre", -1, "[PROBABLE]",
                "meme source ; reserve : Lax, Phillips et Stollwerk 2016 (04-22) ne trouvent "
                "aucun ecart de mode sur le mariage entre personnes de meme sexe"),
    "pillok": ("aucune", None, "[HYPOTHESE]",
               "contraception pour les 14 a 16 ans : pole normatif contesté, aucun pole retenu"),
    "sexeduc": ("ensemble", {"favor"}, "[HYPOTHESE]",
                "l'education sexuelle a l'ecole est majoritairement approuvee, le pole "
                "approbateur est le pole presentable"),
    "pornlaw": ("ordre", -1, "[HYPOTHESE]",
                "la pornographie est stigmatisee ; le pole restrictif est le pole presentable"),
    "xmovie": ("ensemble", {"no"}, "[PROBABLE]",
               "Tourangeau et Yan 2007 : conduite sexuelle sous declaree ; 'non' est le pole "
               "presentable. Item non teste par NORC"),
    # --- race
    "natrace_note": None,  # place tenue, la valeur est donnee par la regle des depenses
    "racdif1": ("ensemble", {"yes"}, "[PROBABLE]",
                "Berinsky 1999 (corpus 04-19) : l'opinion raciale liberale est sur declaree ; "
                "attribuer l'ecart a la discrimination est le pole liberal"),
    "racdif2": ("ensemble", {"no"}, "[PROBABLE]",
                "meme source ; attribuer l'ecart a une capacite innee est le pole stigmatise"),
    "racdif3": ("ensemble", {"yes"}, "[HYPOTHESE]",
                "meme famille, direction moins nette : l'explication par l'education est "
                "consideree comme structurelle"),
    "racdif4": ("ensemble", {"no"}, "[HYPOTHESE]",
                "meme famille : l'explication par le manque de volonte est le pole stigmatise"),
    "spkrac/y": ("aucune", None, "[CONFIRME]",
                 "aucun pole : deux normes s'opposent, la norme de liberte d'expression et la "
                 "norme antiraciste. NORC classe l'item sensible sans donner de direction"),
    "colrac": ("aucune", None, "[CONFIRME]", "meme raison que spkrac/y"),
    "librac/y": ("aucune", None, "[CONFIRME]", "meme raison que spkrac/y"),
    "letin1a": ("ordre", -1, "[PROBABLE]",
                "Bursztyn, Egorov et Fiorin 2020 (corpus 04-27) : l'opinion xenophobe est "
                "cachee quand elle est percue comme minoritaire, donc le pole pro immigration "
                "est le pole declare en exces"),
    "wlthblks": ("aucune", None, "[HYPOTHESE]", "perception de richesse, pas de pole normatif clair"),
    "wlthwhts": ("aucune", None, "[HYPOTHESE]", "idem"),
    "wlthhsps": ("aucune", None, "[HYPOTHESE]", "idem"),
    "racwork": ("aucune", None, "[HYPOTHESE]", "composition raciale du lieu de travail, factuel"),
    "discaff": ("aucune", None, "[HYPOTHESE]", "perception de discrimination inverse, pole contesté"),
    "discaffw": ("aucune", None, "[HYPOTHESE]", "idem"),
    "discaffm": ("aucune", None, "[HYPOTHESE]", "idem"),
    # --- tolerance politique, echelle de Stouffer
    "spkath/y": ("ensemble", {"allowed"}, "[PROBABLE]",
                 "Tourangeau et Yan 2007 : les items de tolerance sont sur declares du cote "
                 "tolerant"),
    "colath": ("ensemble", {"allowed"}, "[PROBABLE]", "idem"),
    "spkcom/y": ("ensemble", {"yes, allowed to speak"}, "[PROBABLE]", "idem"),
    "colcom/y": ("ensemble", {"not fired"}, "[PROBABLE]", "idem"),
    "libcom/y": ("ensemble", {"not remove"}, "[PROBABLE]", "idem"),
    "spkhomo/y": ("ensemble", {"yes, allowed to speak"}, "[PROBABLE]", "idem"),
    "colhomo": ("ensemble", {"allowed"}, "[PROBABLE]", "idem"),
    "libhomo/y": ("ensemble", {"not remove"}, "[PROBABLE]", "idem"),
    # --- violence policiere
    "polabuse/y": ("ensemble", {"no"}, "[HYPOTHESE]",
                   "approuver un coup porte a un citoyen qui a insulte un policier est le pole "
                   "stigmatise ; NORC classe l'item sensible sans donner de direction"),
    "polattak/y": ("aucune", None, "[HYPOTHESE]",
                   "aucun pole : le citoyen attaque le policier, approuver est ici une reponse "
                   "socialement acceptable"),
    "polhitok/y": ("ensemble", {"no"}, "[HYPOTHESE]", "meme raisonnement que polabuse/y"),
    # --- roles de genre
    "fefam": ("ordre", +1, "[PROBABLE]",
              "l'egalitarisme de role est la norme declaree ; NORC note des reponses plus "
              "extremes sur le web pour les items de femmes au travail"),
    "fepresch": ("ordre", +1, "[PROBABLE]", "idem, desapprouver est le pole egalitaire"),
    "fechld": ("ordre", -1, "[PROBABLE]",
               "l'enonce est formule a l'endroit, approuver est le pole egalitaire"),
    "fehire": ("ordre", None, "[HYPOTHESE]", "pole contesté, non retenu"),
    "fepol": ("ensemble", {"disagree"}, "[PROBABLE]", "desapprouver est le pole egalitaire"),
    # --- bien etre et statut, la famille ou le panel Pew mesure les plus gros ecarts de mode
    "happy": ("ordre", -1, "[PROBABLE]",
              "Pew 2015 (corpus 04-15) : les items de satisfaction portent les plus gros ecarts "
              "de mode, 14 a 18 points, toujours dans le sens du pole positif"),
    "satfin": ("ordre", -1, "[PROBABLE]", "idem"),
    "satjob": ("ordre", -1, "[PROBABLE]", "idem"),
    "health": ("ordre", -1, "[PROBABLE]", "idem"),
    "life": ("ordre", -1, "[PROBABLE]", "idem"),
    "hapmar": ("ordre", -1, "[PROBABLE]", "idem, item non teste par NORC"),
    "finalter": ("ordre", -1, "[HYPOTHESE]", "pole positif"),
    "finrela": ("ordre", +1, "[PROBABLE]",
                "Tourangeau et Yan 2007 : le revenu declare est sur declare vers le haut"),
    "incom16": ("ordre", +1, "[HYPOTHESE]", "meme raisonnement, revenu de la famille a 16 ans"),
    "income": ("ordre", +1, "[PROBABLE]",
               "Tourangeau et Yan 2007 : le revenu est un item sensible classique. Item non "
               "teste par NORC"),
    "parsol": ("ordre", -1, "[HYPOTHESE]", "pole positif"),
    "unemp": ("ensemble", {"no"}, "[HYPOTHESE]", "le chomage passe est un fait stigmatise"),
    "richwork": ("ensemble", {"continue to work"}, "[HYPOTHESE]",
                 "la norme de travail est le pole presentable"),
    "divorced": ("ensemble", {"no"}, "[HYPOTHESE]", "le divorce est un fait faiblement stigmatise"),
    "class": ("aucune", None, "[HYPOTHESE]", "auto classement social, pole non defini"),
    "spanking": ("ordre", +1, "[PROBABLE]",
                 "la punition corporelle est devenue un fait stigmatise ; desapprouver est le "
                 "pole presentable"),
    # --- items ou aucun pole n'est defendable
    **{it: ("aucune", None, "[HYPOTHESE]", "pole non defini")
       for it in ["abdefect", "abnomore", "abhlth", "abpoor", "abrape", "absingle", "abany",
                  "cappun", "gunlaw", "owngun", "letdie1", "suicide1", "suicide2",
                  "suicide3", "suicide4", "grass", "divlaw", "tax", "courts", "prayer",
                  "uswary", "aged", "getahead", "kidssol", "jobfind", "joblose",
                  "wrkstat", "evwork", "wrkgovt1", "wrkgovt2", "partfull", "wksub1",
                  "wksup1", "union1", "hunt1", "posslq/y", "mobile16", "dwelown16",
                  "spdeg*", "spjew", "spfund", "jew", "jew16*", "relig16*", "postlife",
                  "bible", "granborn", "uscitzn*", "fucitzn", "mnthsusa", "othlang",
                  "compuse*", "webmob", "usewww*", "trust", "fair", "helpful"]},
    # --- information
    "news": ("ordre", -1, "[PROBABLE]",
             "la consommation d'information est sur declaree ; l'ordre va de 'every day' a "
             "'never'"),
}
DESIRABILITE.pop("natrace_note", None)


# Items traites comme ordinaux pour la distance de distribution. Les autres sont traites
# comme nominaux et recoivent une distance de variation totale. Un item porteur d'une
# modalite "Inapplicable" n'est jamais traite comme ordinal : cette modalite n'a pas de
# place sur l'echelle.
ORDINAUX = {
    "natspac/y", "natenvir/y", "natheal/y", "natcity/y", "natdrug/y", "nateduc/y",
    "natrace/y", "natarms/y", "nataid/y", "natfare/y", "natroad", "natsoc", "natmass",
    "natpark", "natchld", "natsci", "natenrgy",
    "courts", "discaffw", "discaffm", "discaff", "fehire", "fechld", "fepresch", "fefam",
    "incom16", "conarmy", "conbus", "conclerg", "coneduc", "confed", "confinan",
    "conjudge", "conlabor", "conlegis", "conmedic", "conpress", "consci", "contv",
    "happy", "satfin", "finalter", "finrela", "letin1a", "parsol", "spanking", "xmarsex",
    "homosex", "marhomo", "pillok", "news", "attend", "pray", "income", "health", "life",
    "wlthwhts", "wlthblks", "wlthhsps", "class", "getahead", "aged", "fair", "helpful",
    "trust", "tax", "divlaw", "pornlaw", "granborn", "bible", "mobile16",
}

INAPPLICABLE = ("inapplicable", "i have no children", "neither belongs", "neither hunt",
                "works alone")


def sans_score(modalite):
    """Vrai si la modalite ne doit recevoir aucun score de desirabilite."""
    m = str(modalite).lower().strip()
    return any(m.startswith(p) for p in INAPPLICABLE)


def scores_desirabilite(item, options):
    """Score de desirabilite par modalite, dans [0, 1], ou None si aucun pole n'est defini.

    options est la liste ordonnee des modalites telle qu'elle figure dans
    question_master/gss/main.csv, en minuscules.
    """
    entree = DESIRABILITE.get(item)
    if entree is None:
        return None, "[HYPOTHESE]", "item absent de la table de desirabilite"
    regle, arg, niveau, source = entree
    if regle == "aucune" or arg is None:
        return None, niveau, source
    utiles = [o for o in options if not sans_score(o)]
    if regle == "ordre":
        k = len(utiles)
        if k < 2:
            return None, niveau, source
        scores = {}
        for r, o in enumerate(utiles):
            v = r / (k - 1)
            scores[o] = v if arg > 0 else 1.0 - v
        return scores, niveau, source
    if regle == "ensemble":
        inconnues = set(arg) - set(utiles)
        assert not inconnues, f"{item} : modalites desirables absentes des options {inconnues}"
        return {o: (1.0 if o in arg else 0.0) for o in utiles}, niveau, source
    raise ValueError(regle)


def options_par_item(racine):
    """Lit question_master/gss/main.csv et renvoie item -> liste ordonnee de modalites."""
    import pandas as pd
    chemin = os.path.join(racine, "data/osf-t6g7k-stanford/figure2/data/"
                                  "question_master/gss/main.csv")
    qm = pd.read_csv(chemin)
    return {k.lower(): [o.lower().strip() for o in json.loads(v)]
            for k, v in zip(qm["Question ID"], qm["Options"])}


# ---------------------------------------------------------------------------
# 4. Second decoupage, celui de la litterature, pour le cas ou le croisement NORC serait
#    juge trop etroit. Domaines sensibles listes par Tourangeau et Yan 2007 (corpus 04-03)
#    et repris dans la synthese de corpus/04 : religion, sexualite, drogues, revenu, vote,
#    race. Ce decoupage est plus large et moins bien fonde que celui de NORC, il ne sert
#    que de controle de robustesse.
# ---------------------------------------------------------------------------

LITTERATURE_SENSIBLE = {
    # religion
    "attend", "pray", "reborn", "savesoul", "postlife", "bible",
    # sexualite
    "xmarsex", "homosex", "marhomo", "xmovie", "spkhomo/y", "colhomo", "libhomo/y",
    "pillok", "sexeduc", "pornlaw",
    # drogues
    "grass",
    # revenu
    "income", "finrela", "incom16",
    # vote
    "vote16", "pres16", "if16who",
    # race
    "natrace/y", "racdif1", "racdif2", "racdif3", "racdif4", "spkrac/y", "colrac",
    "librac/y", "racwork", "wlthblks", "wlthwhts", "wlthhsps", "discaff", "discaffw",
    "discaffm", "letin1a",
}
