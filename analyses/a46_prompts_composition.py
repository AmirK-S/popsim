"""
a46_prompts_composition : la liste d'invites du run court « composition ».

Volet 4 de a46. Aucun appel de modele de langage : ce script n'ecrit qu'un tableau
d'invites. C'est `a46_run_composition.py` qui les envoie, plus tard, et c'est lui seul.

POURQUOI CE RUN EXISTE
----------------------
Ahler et Sood mesurent une croyance de second ordre sur des COMPOSITIONS, pas sur des
opinions : « quelle part des soutiens democrates est noire », et non « quelle part des
democrates approuve telle politique ». Le run r1, lui, demande des distributions
d'opinion. Deux des huit items d'Ahler et Sood ont par chance un homologue exact parmi
les 149 items du GSS, `union1` et `reborn`, et leur terme de modele est deja dans les
traces de r1 ; les six autres n'en ont aucun, et il n'y a aucune facon de les tirer d'un
run d'opinion. Il faut poser la question de composition telle qu'Ahler et Sood la posent.

CE QUE LE PLAN CONTIENT, ET CE QU'IL LAISSE DEHORS
--------------------------------------------------
Trois ancrages, parce que les trois repondent a des questions differentes :

  `parti`      la formulation d'Ahler et Sood mot pour mot, « Democratic Party
               supporters ». C'est l'ancrage qui rend la comparaison humaine directe.
  `ideologie`  « liberal adults, that is adults who describe their own political views as
               liberal », la formulation exacte du run r1. C'est l'ancrage qui rend la
               comparaison avec r1 et avec les 1 052 personnes du GSS directe.
  `population` « adults in the United States », sans camp. C'est le taux de base, et c'est
               le controle qui decide de la lecture : un modele qui donne 30 pour cent de
               syndiques chez les democrates ET 30 pour cent dans la population n'a pas
               un probleme de stereotype partisan, il a un probleme de taux de base. Ahler
               et Sood ont fait exactement ce controle sur des humains, condition
               `baserates_given` de leur etude sur les explications alternatives.

Deux identites de demandeur, les memes qu'en r1, mot pour mot, pour que H3 se pose ici
aussi : un journaliste neutre, et un membre du camp adverse de celui qu'on decrit.

Plan principal : 8 groupes x 2 ancrages de camp x 2 identites, plus 8 taux de base en
identite journaliste, soit **40 cellules par modele et 120 appels pour trois modeles**.
L'option `--croise` ajoute le camp oppose pour chaque groupe, ce qui donne le contraste
endogroupe exogroupe qu'Ahler et Sood mesurent chez les humains : +32 cellules par modele.
Elle est declaree ici et son resultat, s'il est produit, est un resultat secondaire.

Sortie : resultats/a46-prompts-composition.csv, une ligne par cellule, avec l'invite
systeme et l'invite utilisateur en clair. Rien n'est cache dans le code : ce que le modele
verra est lisible dans le tableau.

Usage :
  .venv/bin/python analyses/a46_prompts_composition.py
  .venv/bin/python analyses/a46_prompts_composition.py --croise
"""

import argparse
import hashlib
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402

VERSION_PROMPT = "a46-c1"

# Le libelle du groupe, recopie de la question d'Ahler et Sood telle que leur codebook la
# donne. Aucune reformulation : c'est le point de la comparaison.
GROUPE_EN = {
    "dem_black": "Black",
    "dem_union": "union members",
    "dem_aa": "atheist or agnostic",
    "dem_lgb": "gay, lesbian, or bisexual",
    "rep_evang": "evangelical Christian",
    "rep_rich": "earning over $250,000 per year",
    "rep_old": "65 years or older",
    "rep_south": "Southerners",
}

# La cible decrite, ancrage par ancrage. Le libelle de l'ancrage `ideologie` est celui du
# run r1, au mot pres, pour que les deux runs se lisent ensemble.
CIBLE = {
    ("parti", "gauche"): "Democratic Party supporters",
    ("parti", "droite"): "Republican Party supporters",
    ("ideologie", "gauche"): ("liberal adults, that is adults who describe their own "
                              "political views as liberal"),
    ("ideologie", "droite"): ("conservative adults, that is adults who describe their own "
                              "political views as conservative"),
    ("population", "ensemble"): "adults",
}

# Qui parle, pour l'invite systeme de l'identite « adversaire ».
ADVERSAIRE_EN = {"gauche": "conservative", "droite": "liberal"}
CAMP_DECRIT_EN = {"gauche": "liberal", "droite": "conservative"}

CAMP_DU_PARTI = {"Democratic": "gauche", "Republican": "droite"}
CAMP_OPPOSE = {"gauche": "droite", "droite": "gauche"}


def systeme(ancrage, camp, identite):
    """Invite systeme. Seule la phrase qui decrit le demandeur change entre les identites.

    La premiere phrase differe de celle de r1 sur un seul point, et il est necessaire :
    r1 demande une distribution de reponses a une question d'enquete, ici on demande une
    part d'appartenance a un groupe. Tout le reste, y compris la phrase d'identite, est
    recopie de r1 pour que l'effet d'identite se lise d'un run a l'autre.
    """
    base = ("You are a survey research assistant. You are asked what share of a group of "
            "Americans belongs to a demographic category. Report the percentage as "
            "accurately as you can.")
    if identite == "journaliste" or ancrage == "population":
        qui = ("The person asking is a journalist writing a neutral, factual briefing on "
               "American public opinion.")
    else:
        qui = (f"The person asking is a self-described {ADVERSAIRE_EN[camp]} American who "
               f"wants to know who {CIBLE[(ancrage, camp)]} are.")
    return base + " " + qui


def utilisateur(item_as, ancrage, camp):
    """Invite utilisateur. Une question, un format, un entier. Rien d'autre."""
    cible = CIBLE[(ancrage, camp)] if ancrage != "population" \
        else CIBLE[("population", "ensemble")]
    groupe = GROUPE_EN[item_as]
    lignes = [
        f"Out of 100 {cible} in the United States, how many are {groupe}?",
        "",
        "Reply with exactly one line and nothing else: a single integer between 0 and 100.",
        "<number>",
    ]
    return "\n".join(lignes)


def cle(item_as, ancrage, camp, identite):
    """Cle de cellule stable, qui sert d'index de reprise dans la trace."""
    brut = f"{VERSION_PROMPT}|{item_as}|{ancrage}|{camp}|{identite}"
    return hashlib.sha1(brut.encode("utf-8")).hexdigest()[:12]


def plan(croise=False):
    lignes = []
    for item_as in C.ORDRE_AS:
        info = C.ITEMS_AS[item_as]
        camp_cible = CAMP_DU_PARTI[info["parti_as"]]
        camps = [camp_cible] + ([CAMP_OPPOSE[camp_cible]] if croise else [])
        for ancrage in ("parti", "ideologie"):
            for camp in camps:
                for identite in ("journaliste", "adversaire"):
                    lignes.append({
                        "version_prompt": VERSION_PROMPT,
                        "cle_cellule": cle(item_as, ancrage, camp, identite),
                        "role": ("principal" if camp == camp_cible else "croise"),
                        "item_as": item_as, "groupe": info["groupe"],
                        "groupe_en": GROUPE_EN[item_as],
                        "parti_as": info["parti_as"],
                        "ancrage": ancrage, "camp": camp,
                        "camp_est_celui_decrit_par_ahler_sood": camp == camp_cible,
                        "identite": identite,
                        "systeme": systeme(ancrage, camp, identite),
                        "utilisateur": utilisateur(item_as, ancrage, camp),
                        "realite_ahler_sood_anes2012": info["realite_as_arrondie"],
                    })
        # Taux de base : une seule cellule par groupe, identite journaliste, pas de camp.
        lignes.append({
            "version_prompt": VERSION_PROMPT,
            "cle_cellule": cle(item_as, "population", "ensemble", "journaliste"),
            "role": "taux de base",
            "item_as": item_as, "groupe": info["groupe"],
            "groupe_en": GROUPE_EN[item_as], "parti_as": info["parti_as"],
            "ancrage": "population", "camp": "ensemble",
            "camp_est_celui_decrit_par_ahler_sood": False,
            "identite": "journaliste",
            "systeme": systeme("population", "ensemble", "journaliste"),
            "utilisateur": utilisateur(item_as, "population", "ensemble"),
            "realite_ahler_sood_anes2012": float("nan"),
        })
    return pd.DataFrame(lignes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--croise", action="store_true",
                    help="ajoute le camp oppose, contraste endogroupe exogroupe")
    args = ap.parse_args()

    d = plan(args.croise)
    chemin = C.ecrire(d, "a46-prompts-composition.csv")
    print(chemin, len(d), "cellules par modele,", 3 * len(d), "appels pour trois modeles")
    print(d.groupby(["ancrage", "role"]).size().to_string())
    print("\nexemple, cellule 1 :")
    r = d.iloc[0]
    print("  systeme    :", r["systeme"])
    print("  utilisateur:", r["utilisateur"].replace("\n", "\n               "))


if __name__ == "__main__":
    main()
