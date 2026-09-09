"""
a38_commun : ce que a38 declare, et rien d'autre.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/traces/ et data/osf-t6g7k-stanford/. Aucun script existant n'est modifie. Sont
importes tels quels : a2_commun, a2_baselines_gss, a5_evaluer, a5_agents_locaux_gss,
a25_commun, a25_mesures, a28_commun, a30_commun.

a38 ferme deux points laisses ouverts par a25 et a28 :

  T1 continu. a28 construisait son score continu S2 a la main, par domaine, avec cinq
  entrees marquees [HYPOTHESE] et une couverture de 5 des 12 items sensibles. La lecture
  complete de `corpus/lecture-complete/04` etablit que l'ampleur par item existe et vit
  dans les rapports methodologiques du GSS. a38 la lit et la substitue.

  T5 par camp. Oceno 2025 etablit que le pole desirable d'un item evaluatif s'inverse
  selon le camp. a25 fixe un pole unique par item pour toute la population. a38 mesure le
  sens de l'ecart separement par bloc d'ideologie.

Ce module porte quatre declarations et aucun calcul de fond.

  1. l'assemblage du score continu d'ampleur, item par item, a partir des tables de
     data/norc-mode/ produites par a38_extraire_norc.py ;
  2. la ligne de partage comportement verifiable / attitude / auto evaluation, item par
     item, avec sa justification ;
  3. le pole d'endogroupe par camp, item par item, avec sa source, et la liste des items
     exclus faute de source ;
  4. la famille d'hypotheses, fixee avant les resultats.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Elle est ecrite ici, dans le code, et recopiee telle quelle dans le rapport. Elle prolonge
celle de a28 sans la rejouer : les 52 tests de a28 ne sont pas repris, ce sont d'autres
tests sur les memes donnees, et le rapport le dit.

  K1 (primaire, T1 continu, distance). Pour chacune des 13 methodes non humaines, la
     correlation de rang entre l'ampleur de mode MESUREE par item et la distance agent
     contre humain par item est positive. Score M1, ampleur de mode stricte. Perimetre
     150. 13 tests.
  K2 (primaire, T1 continu, dispersion). Meme chose avec le rapport d'entropie agent sur
     humain a la place de la distance ; prediction de signe NEGATIF, la simulation
     effacant plus de variete la ou l'ampleur est grande. Score M1. Perimetre 150.
     13 tests.
  K3 (secondaire, T3 comportement contre attitude). Pour chacune des 13 methodes, le
     contraste de distance sensible moins temoin est plus grand sur les comportements
     declares que sur les attitudes. Perimetre 150. 13 tests.
  K4 (secondaire, T5 par camp). Pour chacune des 13 methodes, l'ecart de desirabilite
     agent contre humain differe entre le bloc de gauche et le bloc de droite, sur les
     items pourvus d'un pole d'endogroupe documente. Perimetre 150. 13 tests.

  Famille declaree : K1 union K2 union K3 union K4, soit 52 tests. Correction principale :
  Holm sur les 52. Correction secondaire : Benjamini Hochberg sur les 52. Les corrections
  par sous famille de 13 sont aussi donnees.

  N'entrent PAS dans la famille et sont rapportes comme des descriptions : la ligne
  "humains vague 2", temoin negatif ; les scores M2 et M3, qui melangent des constructions
  differentes et servent de controle de robustesse ; le perimetre 1 052, echantillon
  emboite ; les contrastes de GROUPE, huit conditions a modele de langage contre cinq
  predicteurs statistiques, qui sont post hoc au meme titre qu'en a28 section 1.6 et
  auxquels aucune correction n'est appliquee.
===========================================================================

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NORC = os.path.join(RACINE, "data", "norc-mode")
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908

# ---------------------------------------------------------------------------
# 1. Le score continu d'ampleur
# ---------------------------------------------------------------------------
#
# Trois familles de mesures, qui ne mesurent PAS la meme chose et ne sont donc jamais
# fondues sans le dire.
#
#   "mode"       : un contraste de mode de collecte au sens strict, ou un contraste entre
#                  declaration et registre. MR099 (face a face contre web), MR021 (vote
#                  declare contre resultats), MR086 (presence d'un tiers), atlas NBER
#                  (declaration contre registre individuel). C'est la seule famille qui
#                  mesure ce que la these appelle "les humains se surveillent".
#   "conception" : MR141, la part de repondants qui prennent une modalite volontaire des
#                  qu'elle est visible. Ce n'est pas de la desirabilite, c'est de la
#                  conception d'item, et l'ampleur y est d'un ordre de grandeur au dessus.
#                  C'est un CONFONDANT de la famille "mode", pas une de ses variantes.
#   "regime"     : MR010, la part des "non" a une question absolue qui approuvent une
#                  situation concrete. C'est un changement de regime de reponse, encore
#                  autre chose.
#
# Trois scores en decoulent :
#   M1 = famille "mode" seule. C'est le score pre enregistre, celui de K1 et K2.
#   M2 = M1 union "conception". Controle de robustesse.
#   M3 = M2 union "regime". Couverture maximale, homogeneite minimale.
#
# Toutes les ampleurs sont en POINTS de pourcentage, echelle 0 a 100. Une ampleur absente
# reste absente : elle n'est jamais remplacee par zero. Zero est reserve aux domaines ou
# la litterature a cherche et n'a rien trouve, et il n'y en a aucun dans les tables NORC.

FAMILLES_AMPLEUR = {"mr099": "mode", "mr021": "mode", "mr086": "mode", "atlas": "mode",
                    "mr141": "conception", "mr010": "regime"}


def charger_ampleurs():
    """Assemble le score d'ampleur par item a partir de data/norc-mode/.

    Renvoie un DataFrame avec une ligne par mesure, colonnes : item, ampleur_points,
    famille, rapport, source. Un item peut recevoir plusieurs mesures ; le choix de celle
    qui entre dans M1, M2 et M3 est fait par score_ampleur().
    """
    lignes = []

    d = pd.read_csv(os.path.join(NORC, "mr099-depenses.csv"))
    for _, r in d.iterrows():
        if not isinstance(r.item_stanford, str) or not r.item_stanford:
            continue
        lignes.append({"item": r.item_stanford, "ampleur_points": r.ampleur_tv_points,
                       "famille": "mode", "rapport": "MR099", "source": r.source,
                       "detail": (f"face a face {r.gss_ftf_trop_peu}/{r.gss_ftf_juste}/"
                                  f"{r.gss_ftf_trop} contre web {r.knsa_web_trop_peu}/"
                                  f"{r.knsa_web_juste}/{r.knsa_web_trop} ; ampleur "
                                  f"enoncee par NORC {r.ampleur_norc_pas_trop} points")})

    d = pd.read_csv(os.path.join(NORC, "mr141-modalite-volontaire.csv"))
    for _, r in d.iterrows():
        lignes.append({"item": r.item_stanford, "ampleur_points": r.ampleur_tv_points,
                       "famille": "conception", "rapport": "MR141", "source": r.source,
                       "detail": (f"modalite volontaire « {r.modalite_volontaire} », "
                                  f"prise par {r.part_volontaire_2022_web} pour cent")})

    for fichier, rapport in [("mr010-absolu-contre-situationnel.csv", "MR010"),
                             ("mr021-vote-declare.csv", "MR021"),
                             ("mr086-presence-de-tiers.csv", "MR086")]:
        d = pd.read_csv(os.path.join(NORC, fichier))
        fam = "regime" if rapport == "MR010" else "mode"
        for _, r in d.iterrows():
            lignes.append({"item": r.item_stanford, "ampleur_points": r.ampleur_points,
                           "famille": fam, "rapport": rapport, "source": r.source,
                           "detail": r.detail})

    d = pd.read_csv(os.path.join(NORC, "atlas-nber-2025.csv"))
    for _, r in d.iterrows():
        if not isinstance(r.item_stanford, str) or not r.item_stanford:
            continue
        lignes.append({"item": r.item_stanford, "ampleur_points": r.ampleur_points,
                       "famille": "mode", "rapport": "Atlas NBER 2025",
                       "source": r.source,
                       "detail": (f"{r.etude} : reel {r.prevalence_reelle} pour cent "
                                  f"contre declare {r.prevalence_declaree}")})
    return pd.DataFrame(lignes)


# Quand deux rapports donnent une ampleur de la meme famille pour le meme item, l'ordre
# de priorite est declare ici et non decide apres coup. Le rapport propre au GSS prime sur
# la mesure etrangere : MR021 mesure la sur declaration de vote SUR LE GSS, l'atlas la
# mesure sur des registres norvegiens. Les deux valeurs sont conservees dans le tableau
# item par item, et l'ecart entre elles est un resultat en soi.
PRIORITE_RAPPORT = {"MR099": 0, "MR021": 1, "MR086": 2, "Atlas NBER 2025": 3,
                    "MR141": 4, "MR010": 5}


def score_ampleur(ampleurs, items):
    """item -> (M1, M2, M3, rapport retenu, famille retenue), NaN si non couvert."""
    a = ampleurs[ampleurs.item.isin(items)].copy()
    a["prio"] = a.rapport.map(PRIORITE_RAPPORT)
    a = a.sort_values(["item", "prio"])
    out = {}
    for it in items:
        sous = a[a.item == it]
        m1 = sous[sous.famille == "mode"]
        m2 = sous[sous.famille.isin(["mode", "conception"])]
        m3 = sous
        out[it] = {
            "m1": float(m1.ampleur_points.iloc[0]) if len(m1) else np.nan,
            "m2": float(m2.ampleur_points.iloc[0]) if len(m2) else np.nan,
            "m3": float(m3.ampleur_points.iloc[0]) if len(m3) else np.nan,
            "rapport": (m3.rapport.iloc[0] if len(m3) else ""),
            "famille": (m3.famille.iloc[0] if len(m3) else ""),
            "n_mesures": len(sous),
        }
    return out


# ---------------------------------------------------------------------------
# 2. Comportement verifiable, attitude, auto evaluation
# ---------------------------------------------------------------------------
#
# C'est la ligne de partage que la lecture complete de corpus/04 designe comme la variable
# qui explique le desaccord de la litterature, sections "ce qui se contredit" 1 et 2 : les
# etudes qui trouvent de la desirabilite disposent d'une verite terrain individuelle et
# portent sur des COMPORTEMENTS ; celles qui n'en trouvent pas portent sur des ATTITUDES.
# L'atlas NBER (L04-09) l'inscrit dans son critere d'inclusion, Smith (L04-02) le mesure
# sur le GSS lui meme, Gnambs et Kaspar (04-14) le mesurent sur les comportements honteux.
#
# Trois classes et non deux. L'auto evaluation est isolee parce que Ye, Fulton et
# Tourangeau (L04-25) proposent, sur 18 comparaisons, une explication concurrente et plus
# economique de ce qu'on y observe : le mode ne pousse pas vers le pole desirable, il
# pousse vers l'extremite POSITIVE de l'echelle. Melanger cette famille aux attitudes
# reviendrait a compter comme desirabilite un phenomene qui n'en est peut etre pas un.
#
# Regle : est un comportement declare un item qui demande au repondant de rapporter ce
# qu'il a fait, ce qu'il fait, ou un etat de fait le concernant, et dont un registre
# pourrait en principe donner la valeur. Est une auto evaluation un item qui lui demande
# de noter sa propre situation sur une echelle subjective. Tout le reste est une attitude.

COMPORTEMENT = {
    # vote et participation, verifiables au registre
    "vote16", "pres16", "if16who",
    # pratique et appartenance religieuses declarees
    "attend", "pray", "reborn", "savesoul", "jew", "relig16*", "jew16*",
    # emploi et statut d'activite
    "wrkstat", "evwork", "wrkgovt1", "wrkgovt2", "partfull", "wksub1", "wksup1",
    "union1", "unemp", "joblose",
    # menage, biographie, logement
    "divorced", "posslq/y", "mobile16", "dwelown16", "incom16", "income", "granborn",
    "uscitzn*", "fucitzn", "mnthsusa", "othlang", "spdeg*", "spjew", "spfund",
    # loisirs, equipement, exposition
    "compuse*", "webmob", "usewww*", "news", "xmovie", "owngun", "hunt1", "racwork",
}

AUTO_EVALUATION = {
    "happy", "hapmar", "satjob", "satfin", "life", "health", "class", "finalter",
    "finrela", "parsol", "kidssol", "jobfind",
}

# Tout le reste des 149 items est classe "attitude". La liste n'est pas ecrite en dur pour
# qu'un item nouveau tombe du bon cote par defaut, la classe modale.


def classe_comportement(item):
    if item in COMPORTEMENT:
        return "comportement"
    if item in AUTO_EVALUATION:
        return "auto evaluation"
    return "attitude"


JUSTIFICATIONS_CLASSE = {
    "vote16": "vote declare, valide au registre par Ansolabehere et Hersh 2012 et par "
              "Kleven 2022 ; c'est le cas d'ecole du comportement verifiable",
    "pres16": "choix de candidat declare, comparable aux resultats officiels, MR021",
    "if16who": "meme question posee autrement",
    "attend": "frequence declaree de pratique, comparee a l'observation par Presser et "
              "Stinson 1998",
    "pray": "frequence declaree de priere, aucun registre possible mais la forme de la "
            "question est celle d'un comportement",
    "reborn": "experience declaree, fait biographique",
    "savesoul": "acte declare, fait biographique",
    "news": "frequence declaree de lecture, comportement, sur declare dans la "
            "litterature de l'exposition aux medias",
    "xmovie": "acte declare, comportement stigmatise, mesure par Tourangeau et Yan 2007",
    "unemp": "chomage passe declare, comparable aux dossiers administratifs ; l'atlas "
             "NBER couvre le domaine par Dutz et al. 2021",
    "income": "revenu declare, comparable a la declaration fiscale",
    "health": "auto evaluation, pas un comportement ; MR086 mesure dessus le seul effet "
              "de presence d'un tiers qui survive aux controles",
    "happy": "auto evaluation ; Ye, Fulton et Tourangeau 2011 proposent l'extremite "
             "positive plutot que le pole desirable",
}


# ---------------------------------------------------------------------------
# 3. Le pole d'endogroupe, item par item
# ---------------------------------------------------------------------------
#
# Le probleme, pose par Oceno 2025 (L04-18) : a25 fixe un pole socialement desirable
# unique par item, valable pour toute la population. Sur l'ANES, le pole desirable d'un
# item evaluatif s'inverse selon le camp et selon l'objet ; « Republicans' positive
# emotions in 2016 mirror, in reverse, those of Democrats in 2012 ».
#
# Deux lectures concurrentes, toutes deux documentees, et le test les departage.
#
#   Lecture A, norme societale unique. Il existe un pole presentable pour tout le monde,
#   et c'est le camp dont la position sincere s'en ecarte qui se tait. Berinsky 1999 sur
#   la race, Bursztyn, Egorov et Fiorin 2020 sur l'immigration, Coffman, Coffman et
#   Ericson 2017 sur l'hostilite envers les gays, Gibson et Sutherland 2023 sur l'ampleur
#   asymetrique de l'auto censure, Valentim 2024 sur ce qui se passe quand la norme cede.
#   Prediction : le camp de droite se deplace vers le pole desirable de a25, le camp de
#   gauche ne se deplace pas.
#
#   Lecture B, norme d'endogroupe. La desirabilite est une fonction de la cible et de
#   l'approbation du groupe de reference, Crandall, Eshleman et O'Brien 2002 sur 105
#   groupes sociaux ; l'attitude declaree suit « almost exclusively » la position affichee
#   du parti, Cohen 2003 ; une etiquette ideologique code une disposition a suivre et non
#   une position, Barber et Pope 2019. Prediction : chaque camp se deplace vers SA propre
#   position typique, donc en sens opposes.
#
# Ce que a38 mesure. Le score de desirabilite reste celui de a25, inchange, et c'est le
# pole de la lecture A. Ce qui est declare ici, item par item, c'est UNIQUEMENT de quel
# cote de ce score se trouve la position typique de la droite. Un seul bit par item, ce
# qui est beaucoup moins contestable qu'un pole invente par camp. Le signe de l'ecart
# suffit alors a departager :
#
#   droite positive et gauche nulle          -> lecture A, la simulation presente la droite
#   droite negative et gauche positive       -> lecture B, chaque camp vers son pole
#   les deux du meme signe non nul           -> ni l'une ni l'autre, deplacement global
#
# "droite_bas" veut dire : la position typique de la droite americaine sur cet item se
# trouve du cote BAS du score de desirabilite de a25, celle de la gauche du cote haut.
# Un item sans source documentee est EXCLU, il n'est pas devine.

POLE_ENDOGROUPE = {
    # --- race. Le pole desirable de a25 est le pole racialement liberal.
    "racdif1": ("droite_bas", "[PROBABLE]",
                "Berinsky 1999, corpus 04-19 : l'opinion raciale liberale est sur "
                "declaree, et la sur declaration vient de ceux qui tiennent la position "
                "conservatrice ; Engelhardt 2021, L04-21, teste et ne trouve PAS de "
                "changement de desirabilite sur le ressentiment racial, reserve a porter"),
    "racdif2": ("droite_bas", "[PROBABLE]", "meme source"),
    "racdif3": ("droite_bas", "[HYPOTHESE]", "meme famille, direction moins nette"),
    "racdif4": ("droite_bas", "[PROBABLE]", "meme source"),
    "natrace/y": ("droite_bas", "[CONFIRME]",
                  "MR099 Table 3 : les depenses pour les Noirs portent la plus grande "
                  "ampleur de mode des 17 items, 13,8 points, et le clivage partisan sur "
                  "l'aide ciblee est etabli. Reserve explicite de la source : Smith et "
                  "Dennis refusent de dire que le pole pro depense est le pole desirable"),
    # --- immigration
    "letin1a": ("droite_bas", "[CONFIRME]",
                "Bursztyn, Egorov et Fiorin 2020, corpus 04-27 : l'opinion xenophobe est "
                "cachee par ceux qui la tiennent quand ils la croient minoritaire"),
    # --- hostilite envers les gays
    "homosex": ("droite_bas", "[PROBABLE]",
                "Coffman, Coffman et Ericson 2017, corpus 04-21 : la desapprobation est "
                "sous declaree en question directe, par ceux qui la tiennent"),
    "marhomo": ("droite_bas", "[PROBABLE]",
                "meme source ; reserve forte : Lax, Phillips et Stollwerk 2016, corpus "
                "04-22, ne trouvent aucune desirabilite sur le mariage entre personnes "
                "de meme sexe"),
    "spkhomo/y": ("droite_bas", "[PROBABLE]", "meme source, echelle de Stouffer"),
    "colhomo": ("droite_bas", "[PROBABLE]", "meme source"),
    "libhomo/y": ("droite_bas", "[PROBABLE]", "meme source"),
    # --- roles de genre
    "fefam": ("droite_bas", "[HYPOTHESE]",
              "l'egalitarisme de role est la norme declaree et le clivage partisan est "
              "etabli ; aucune ampleur publiee par item, la direction seule est reprise"),
    "fepresch": ("droite_bas", "[HYPOTHESE]", "meme raisonnement"),
    "fechld": ("droite_bas", "[HYPOTHESE]", "meme raisonnement"),
    "fepol": ("droite_bas", "[HYPOTHESE]",
              "meme raisonnement ; MR141 mesure sur cet item 14,1 pour cent de « ne sais "
              "pas » des que la modalite est offerte, ce qui est un confondant"),
    # --- depenses publiques. MR099 mesure l'ampleur de mode item par item, et le clivage
    #     partisan sur le niveau de depense publique est le clivage le mieux etabli de la
    #     politique americaine. Smith et Dennis refusent d'y lire de la desirabilite ;
    #     c'est justement pour cela que ces items sont les plus interessants du test : la
    #     lecture A y est explicitement recusee par la source, la lecture B non.
    **{it: ("droite_bas", "[CONFIRME]",
            "MR099 : le face a face donne moins de « trop » sur les 17 items et plus de "
            "« pas assez » sur 12 sur 17 ; Smith et Dennis refusent d'en conclure que le "
            "pole pro depense est le pole socialement desirable")
       for it in ["natspac/y", "natenvir/y", "natheal/y", "natcity/y", "natdrug/y",
                  "nateduc/y", "natfare/y", "natroad", "natsoc", "natmass", "natpark",
                  "natchld", "natsci", "natenrgy"]},
    # nataid/y et natarms/y sont ECARTES : sur l'aide etrangere et sur la defense, le
    # clivage partisan s'inverse ou disparait, et Smith et Dennis relevent eux memes qu'il
    # existe « a large anti-spending majority for foreign aid ». Aucune source ne place la
    # droite du cote bas.
    # --- tolerance politique, echelle de Stouffer. ECARTEE en entier : les items
    #     opposent la liberte d'expression a la norme visee, les deux camps y ont
    #     alternativement interet, et a25 refuse deja d'y fixer un pole pour spkrac/y,
    #     colrac et librac/y. Ne pas rouvrir sans source.
    # --- confiance dans les institutions. ECARTEE : la confiance dans la presse, dans la
    #     science et dans le pouvoir federal a change de camp au moins une fois depuis
    #     2016, ce qui est exactement le motif d'Oceno. Aucun bit stable a declarer.
    # --- religion. ECARTEE : le pole religieux est le pole desirable dans un camp et pas
    #     dans l'autre, personne ne l'a mesure, et MR145 retire une part de l'ecart de
    #     mode a la desirabilite pour l'attribuer a un stimulus differentiel.
    # --- avortement, peine de mort, armes a feu. ECARTES : a25 ne leur donne aucun pole
    #     de desirabilite, il n'y a donc pas de score a signer.
}


def items_camp(items):
    """Items pourvus d'un pole d'endogroupe declare, et raison d'exclusion pour les autres."""
    dedans = [it for it in items if it in POLE_ENDOGROUPE]
    dehors = [it for it in items if it not in POLE_ENDOGROUPE]
    return dedans, dehors


# ---------------------------------------------------------------------------
# 4. Outils
# ---------------------------------------------------------------------------

CAMPS = ["gauche", "centre", "droite"]


def ecrire(df, nom):
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, nom)
    df.to_csv(chemin, index=False, float_format="%.6f")
    print(f"ecrit : {chemin}")
    return chemin


def bootstrap_moyenne(v, tirages, rng):
    """Moyenne et intervalle a 95 pour cent, unites reechantillonnees."""
    v = np.asarray(v, float)
    v = v[~np.isnan(v)]
    if len(v) < 2:
        return np.nan, np.nan, np.nan
    t = v[rng.integers(0, len(v), (tirages, len(v)))].mean(axis=1)
    return float(v.mean()), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def p_permutation_correlation(u, v, tirages, rng):
    """p bilateral de la correlation de rang, par permutation d'un des deux vecteurs.

    Version vectorisee. Les deux vecteurs sont ranges une fois pour toutes, la correlation
    de Spearman devient une correlation de Pearson sur les rangs, et la permutation porte
    sur le vecteur de rangs deja calcule. Les ex aequo sont traites par rangs moyens, ce
    qui compte ici : le score M1 porte des valeurs egales, les 3,3 points de MR021 par
    exemple. Estimateur de Phipson et Smyth, (b + 1) / (m + 1).
    """
    from scipy.stats import rankdata
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    u, v = u[ok], v[ok]
    n = len(u)
    if n < 6 or len(np.unique(u)) < 2 or len(np.unique(v)) < 2:
        return np.nan, np.nan, n
    ru = rankdata(u) - (n + 1) / 2.0
    rv = rankdata(v) - (n + 1) / 2.0
    den = np.sqrt((ru ** 2).sum() * (rv ** 2).sum())
    obs = float((ru * rv).sum() / den)
    idx = np.argsort(rng.random((tirages, n)), axis=1)
    stat = (rv[idx] * ru[None, :]).sum(axis=1) / den
    p = ((np.abs(stat) >= abs(obs) - 1e-12).sum() + 1.0) / (tirages + 1.0)
    return obs, float(p), n


def correlation_sure(u, v, tirages_boot, rng):
    """Spearman avec intervalle bootstrap sur les items, jamais d'exception.

    C28.bootstrap_correlation echoue quand tous les tirages sont degeneres, ce qui arrive
    des qu'un des deux vecteurs est constant sur un sous ensemble d'items. Ici le cas est
    intercepte et rendu comme une absence de mesure.
    """
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    u, v = u[ok], v[ok]
    if len(u) < 6 or len(np.unique(u)) < 2 or len(np.unique(v)) < 2:
        return np.nan, np.nan, np.nan, len(u)
    return C28.bootstrap_correlation(u, v, tirages_boot, rng)
