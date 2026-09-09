"""
a6 : la double distorsion tient elle hors du GSS et hors du pipeline de Stanford ?

Statut : script d'analyse, pas du code de production. Il repond a la limite 7 de
resultats/a1-double-distorsion.md, "un seul jeu de donnees, un seul modele, une seule
equipe", en rejouant la MEME decomposition sur trois autres materiaux.

CE QUI EST REUTILISE, ET CE QUI NE L'EST PAS
--------------------------------------------
Les estimateurs a biais corrige et l'index de comptage sont IMPORTES de
analyses/a1_double_distorsion.py, qui n'est pas modifie : construire_index, compter,
decomposer, agreger, matrice_distance, silhouette, lire_nomenclature, lire_condition,
lire_demographies, normaliser, ainsi que les constantes AXES, MESURES et
ITEMS_DEMOGRAPHIQUES. Aucune formule de dispersion n'est reecrite ici.

Deux fonctions de a1 ne sont PAS importables parce qu'elles sont locales a son main() :
`recentrer`, le recentrage additif des tirages bootstrap, et `ic`, le percentile a 95
pour cent. Elles sont recopiees telles quelles ci dessous, sans changement de formule.
C'est la seule duplication, et elle est signalee dans le rapport.

LES TROIS TESTS
---------------
1. Jeux economiques et Big Five du meme paquet OSF t6g7k, memes 1052 participants,
   memes six segmentations, meme controle vague 2. La correspondance entre etiquette de
   generation et condition experimentale n'est PAS celle du GSS, elle est relue dans
   FIGURE2_PIPELINE.md et FIGURE3_PIPELINE.md a chaque execution et affichee.
2. Twin-2K-500, auteurs differents, modeles differents, jusqu'a treize configurations de
   simulation publiees. Verite humaine vague 4, controle de retest wave4_Q_wave1_3_A.
3. Sur le GSS : silhouette sur le seul sous ensemble attitudinal des items, et mediane
   item par item des ratios, les deux tests laisses ouverts par a1 sections 5 et 8.

UN POINT DE MESURE QUI N'EXISTAIT PAS DANS a1
---------------------------------------------
Les fichiers `bigfive_main` et `econ_games_main` du paquet ne contiennent PAS des items
categoriels. Ils contiennent cinq scores continus par participant : les cinq traits du
BFI, moyennes de 8 a 10 items de Likert, et les cinq mises des jeux economiques,
fractions de la dotation. Le Big Five livre n'est donc pas "entierement ordinal item par
item", il est agrege. Consequence sur la methode, et elle est assumee :
  - M3, la decomposition de variance, s'applique EXACTEMENT aux valeurs continues. Le
    codage dit "fin" attribue un code a chaque valeur distincte observee et met la valeur
    normalisee dans valeurs_ordinales : la table de contingence redonne alors, terme a
    terme, l'analyse de variance sur les valeurs brutes. Aucune approximation.
  - M1 et M2 supposent des modalites. On discretise donc en au plus cinq classes de
    quantiles, bornes estimees sur les seuls HUMAINS DE LA VAGUE 1 et appliquees telles
    quelles a toutes les conditions. Les classes vides ou confondues sont fusionnees, ce
    qui arrive sur les jeux a masse ponctuelle, et le nombre effectif de classes est
    affiche. Un seul jeu de bornes pour toutes les conditions : la discretisation ne peut
    donc pas fabriquer d'ecart entre elles.

ENTREES
-------
1. data/osf-t6g7k-stanford/figure2/data/new_analysis_summaries/{econ_games_main,
   bigfive_main}/preparation/*.csv        huit conditions, 1052 lignes, 5 colonnes
2. data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv   la segmentation
3. data/osf-t6g7k-stanford/figure2/data/new_analysis_summaries/*/analysis/
   individual_level.csv                   MAE et correlation par individu
4. data/twin2k500/llm_specs/*.csv         13 configurations + 2 references humaines,
   recuperees par analyses/a6_telecharger_twin_specs.py
5. data/twin2k500/question_catalog_and_human_response_csv/  catalogue et demographies
6. resultats/a1-ratios.csv                les points GSS deja calcules par a1, lus et non
                                          recalcules, pour le premier cadran de la figure

SORTIES, toutes dans resultats/
-------------------------------
  a6-figure-double-distorsion-multi-jeux.png et .svg
  a6-ratios-econ-games.csv, a6-ratios-bigfive.csv, a6-ratios-twin.csv
  a6-ratios-par-axe.csv
  a6-controle-permutation.csv
  a6-variantes-demographiques.csv
  a6-gss-silhouette-attitudinale.csv
  a6-gss-mediane-item.csv
  a6-twin-configurations.csv
Tous ne contiennent que des statistiques par condition. Aucune ligne individuelle.

DEPENDANCES : numpy et matplotlib du venv du depot. Aucun appel de modele de langage.
Le nombre de fils de calcul est plafonne a 4, une autre tache occupe la machine.

Usage : .venv/bin/python analyses/a6_double_distorsion_hors_gss.py
        options : --bootstrap N (defaut 600), --permutations N (defaut 30),
                  --sans-twin, --sans-gss, --rapide
"""

import os

# Plafond de parallelisme, pose AVANT l'import de numpy : un llama-server occupe la
# machine, on ne lui prend pas ses coeurs. Voir la consigne de mission.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "4")

import argparse
import csv
import json
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a1_double_distorsion import (  # noqa: E402
    AXES, MESURES, ITEMS_DEMOGRAPHIQUES,
    agreger, compter, construire_index, decomposer, lire_condition,
    lire_demographies, lire_nomenclature, matrice_distance, silhouette,
)

RACINE_OSF = "data/osf-t6g7k-stanford"
RACINE_TWIN = "data/twin2k500"


# ---------------------------------------------------------------------------
# 0. Les deux seules fonctions recopiees de a1, parce qu'elles y sont locales a main()
# ---------------------------------------------------------------------------

def recentrer(tirages, cible):
    """Ramene la moyenne des tirages bootstrap sur l'estimation ponctuelle.

    Copie litterale de la fonction interne de a1. Justification en a1 section 8 limite 3 :
    le terme inter est une composante de variance de faible valeur, un tirage bootstrap y
    ajoute une seconde couche de bruit d'echantillonnage qui s'y loge entierement, et
    laisser ce biais en place ecraserait tous les ratios vers 1. Bootstrap de base au sens
    de Davison et Hinkley : le tirage donne la FORME de la distribution, pas son centre.
    """
    v = np.asarray(tirages, dtype=float)
    fini = np.isfinite(v)
    if fini.sum() < 20:
        return v
    return v - np.mean(v[fini]) + cible


def ic(v):
    """Intervalle de percentiles a 95 pour cent. Copie litterale de a1."""
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if v.size < 20:
        return (float("nan"), float("nan"), float("nan"))
    return (float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5)), float(v.mean()))


# ---------------------------------------------------------------------------
# 1. La correspondance des etiquettes, relue dans le paquet a chaque execution
# ---------------------------------------------------------------------------
#
# a1 section 7.2 le documente : `v3` designe l'entretien pour le GSS et le DEMOGRAPHIQUE
# pour les jeux economiques et le Big Five ; `v6` designe le demographique pour le GSS et
# l'ENTRETIEN pour les jeux economiques. Transposer la table du GSS inverserait deux
# conditions sans aucun message d'erreur. On ne la transpose donc pas : on la relit.

MOTIF_CHAMP = re.compile(r"`p_wave1__([a-z0-9_]+)__[a-z]+`")


def relire_etiquettes(racine, prefixe):
    """Extrait des deux fichiers PIPELINE la correspondance condition -> etiquette.

    Les deux fichiers n'ont pas le meme nombre de colonnes : la figure 2 ecrit une ligne
    a deux cellules, condition puis champ, la figure 3 ajoute une colonne de jeu de
    donnees devant. On lit donc n'importe quelle ligne de tableau markdown :
    la cellule qui contient le champ donne l'etiquette, la cellule juste avant donne le
    nom de la condition.

    Retourne deux dictionnaires, un par figure, du type
    {"Interview-Based": "econ_games_v6", ...}. Rien n'est devine : si une ligne attendue
    est absente, elle est absente du dictionnaire et l'appelant doit le dire.
    """
    trouve = {}
    for fichier, cle in (("FIGURE2_PIPELINE.md", "figure2"),
                         ("FIGURE3_PIPELINE.md", "figure3")):
        chemin = os.path.join(racine, fichier)
        trouve[cle] = {}
        if not os.path.exists(chemin):
            continue
        for ligne in open(chemin, encoding="utf-8"):
            ligne = ligne.strip()
            if not ligne.startswith("|"):
                continue
            cellules = [c.strip() for c in ligne.strip("|").split("|")]
            for i, cellule in enumerate(cellules):
                m = MOTIF_CHAMP.fullmatch(cellule)
                if m and i > 0 and m.group(1).startswith(prefixe):
                    trouve[cle][cellules[i - 1]] = m.group(1)
    return trouve


def conditions_osf(racine, jeu, prefixe, prep):
    """Construit la liste (libelle, fichier) pour econ_games ou bigfive.

    `jeu` est le nom du dossier, `prefixe` celui des etiquettes de generation : le paquet
    nomme le dossier `econ_games_main` mais les fichiers `econ_games_v6_summary.csv`.

    Les libelles portent l'etiquette de generation entre parentheses, parce que sans elle
    le mot "demographique" designe deux objets differents.
    """
    tab = relire_etiquettes(racine, prefixe)
    f2, f3 = tab["figure2"], tab["figure3"]
    manques = []
    conds = [("humains vague 1", "p_wave1_summary.csv"),
             ("humains vague 2", "p_wave2_summary.csv"),
             ("agents composite", "composite_agents_summary.csv"),
             ("agents enquete", "survey_agents_summary.csv")]

    def ajouter(libelle, source, cle):
        etq = source.get(cle)
        if etq is None:
            manques.append(f"{cle} absent des tables PIPELINE pour {jeu}")
            return
        fichier = f"{etq}_summary.csv"
        if not os.path.exists(os.path.join(prep, fichier)):
            manques.append(f"{fichier} annonce par le PIPELINE mais absent du dossier")
            return
        conds.append((f"{libelle} ({etq.replace(prefixe + '_', '')})", fichier))

    ajouter("agents entretien", f2, "Interview-Based")
    ajouter("agents persona", f2, "Persona-Based")
    ajouter("agents demographiques fig.2", f2, "Demographic-Based")
    ajouter("agents demographiques fig.3", f3, "Demographic Agents")
    return conds, tab, manques


# ---------------------------------------------------------------------------
# 2. Chargement : OSF continu (jeux economiques et Big Five)
# ---------------------------------------------------------------------------

def lire_continu(chemin, colonnes_attendues):
    """Lit un fichier de condition a valeurs numeriques. Retourne (n, J) float et les ids."""
    lignes = list(csv.reader(open(chemin, newline="", encoding="utf-8")))
    if lignes[0][1:] != colonnes_attendues:
        sys.exit(f"Colonnes differentes dans {chemin}, l'appariement serait faux.")
    ids = [l[0] for l in lignes[1:]]
    x = np.full((len(ids), len(colonnes_attendues)), np.nan)
    for i, ligne in enumerate(lignes[1:]):
        for j in range(len(colonnes_attendues)):
            v = ligne[j + 1].strip()
            if v != "":
                x[i, j] = float(v)
    return x, ids


def coder_fin(valeurs_par_condition):
    """Codage exact : un code par valeur distincte observee, toutes conditions confondues.

    Sortie : dict condition -> matrice d'entiers, et valeurs_ordinales (J, K) qui rend a
    decomposer la valeur numerique de chaque code. La decomposition M3 calculee sur cette
    table est alors identique, terme a terme, a l'analyse de variance sur les valeurs
    brutes : c'est un codage, pas une discretisation.
    """
    noms = list(valeurs_par_condition)
    n_items = valeurs_par_condition[noms[0]].shape[1]
    modalites = []
    for j in range(n_items):
        vals = np.concatenate([valeurs_par_condition[c][:, j] for c in noms])
        modalites.append(np.unique(vals[np.isfinite(vals)]))
    k_max = max(len(m) for m in modalites)
    val_ord = np.zeros((n_items, k_max))
    for j, m in enumerate(modalites):
        val_ord[j, :len(m)] = m
    code = {}
    for c in noms:
        x = np.full(valeurs_par_condition[c].shape, -1, dtype=np.int16)
        for j, m in enumerate(modalites):
            col = valeurs_par_condition[c][:, j]
            ok = np.isfinite(col)
            x[ok, j] = np.searchsorted(m, col[ok])
        code[c] = x
    return code, val_ord, k_max


def coder_grossier(valeurs_par_condition, reference, n_classes=5):
    """Discretisation en classes de quantiles, bornes estimees sur la seule reference.

    Un seul jeu de bornes pour toutes les conditions. Les bornes confondues sont
    fusionnees, ce qui reduit le nombre de classes la ou la distribution humaine a une
    masse ponctuelle, cas des jeux economiques. Retourne aussi le nombre effectif de
    classes par variable, qui doit figurer au rapport.
    """
    noms = list(valeurs_par_condition)
    n_items = valeurs_par_condition[noms[0]].shape[1]
    bornes, effectif = [], []
    ref = valeurs_par_condition[reference]
    for j in range(n_items):
        col = ref[:, j]
        col = col[np.isfinite(col)]
        q = np.quantile(col, np.linspace(0.0, 1.0, n_classes + 1)[1:-1])
        b = np.unique(q)
        bornes.append(b)
        effectif.append(len(b) + 1)
    k_max = max(effectif)
    val_ord = np.zeros((n_items, k_max))
    for j in range(n_items):
        if effectif[j] > 1:
            val_ord[j, :effectif[j]] = np.arange(effectif[j]) / (effectif[j] - 1)
    code = {}
    for c in noms:
        x = np.full(valeurs_par_condition[c].shape, -1, dtype=np.int16)
        for j in range(n_items):
            col = valeurs_par_condition[c][:, j]
            ok = np.isfinite(col)
            x[ok, j] = np.digitize(col[ok], bornes[j], right=False)
        code[c] = x
    return code, val_ord, k_max, effectif


def charger_osf_continu(racine, jeu, prefixe, echelle):
    """Prepare un jeu continu du paquet OSF. echelle : (mini, maxi) de l'echelle declaree.

    Les valeurs hors echelle sont ramenees aux bornes, et leur nombre est compte puis
    rapporte : c'est un fait sur les donnees, pas un nettoyage silencieux.
    """
    prep = os.path.join(racine, f"figure2/data/new_analysis_summaries/{jeu}/preparation")
    if not os.path.isdir(prep):
        return None, [f"dossier absent : {prep}"]
    conds, tab, manques = conditions_osf(racine, jeu, prefixe, prep)
    colonnes = next(csv.reader(open(os.path.join(prep, "p_wave1_summary.csv"),
                                    encoding="utf-8")))[1:]
    brut, ids_ref, hors = {}, None, {}
    for libelle, fichier in conds:
        x, ids = lire_continu(os.path.join(prep, fichier), colonnes)
        if ids_ref is None:
            ids_ref = ids
        elif ids != ids_ref:
            sys.exit(f"Identifiants desalignes dans {fichier}.")
        n_hors = int(np.nansum((x < echelle[0]) | (x > echelle[1])))
        hors[libelle] = n_hors
        x = np.clip(x, echelle[0], echelle[1])
        brut[libelle] = (x - echelle[0]) / (echelle[1] - echelle[0])

    noms = [c for c, _ in conds]
    fin, val_fin, k_fin = coder_fin(brut)
    gros, val_gros, k_gros, effectif = coder_grossier(brut, "humains vague 1")
    seg, niveaux = lire_demographies(racine, ids_ref)
    return {
        "libelle": jeu, "prefixe": prefixe,
        "noms": noms, "reference": "humains vague 1", "controle": "humains vague 2",
        "n": len(ids_ref), "items": colonnes, "n_items": len(colonnes),
        "axes": AXES, "seg": seg, "niveaux": niveaux,
        "garder": np.ones(len(colonnes), dtype=bool),
        "est_ordinal": np.ones(len(colonnes), dtype=bool),
        "principal": (gros, val_gros, k_gros),
        "ordinal": (fin, val_fin, k_fin),
        "notes": {"etiquettes": tab, "hors_echelle": hors, "classes": effectif,
                  "conditions": conds},
    }, manques


# ---------------------------------------------------------------------------
# 3. Chargement : Twin-2K-500
# ---------------------------------------------------------------------------

AXES_TWIN = ["genre", "ethnicite", "ideologie politique", "age", "education",
             "profil croise"]

# Les six axes de Twin, choisis pour etre les analogues exacts des six axes de a1.
# QID12 sexe assigne a la naissance, QID15 race ou origine, QID22 opinions politiques,
# QID13 age en quatre tranches, QID14 diplome le plus eleve. Le sixieme croise les trois
# premiers, l'ideologie etant ramenee a trois blocs comme dans a1.
DEMOS_TWIN = {"genre": "QID12", "ethnicite": "QID15", "ideologie politique": "QID22",
              "age": "QID13", "education": "QID14"}


def bloc_ideologie_twin(v):
    """Cinq niveaux ramenes a trois. Regle mecanique sur le libelle, pas de jugement."""
    v = v.lower()
    if "liberal" in v:
        return "gauche"
    if "conservative" in v:
        return "droite"
    return "centre"


def canon(v):
    """Canonicalise une cellule : les codes numeriques sont ecrits pareil partout."""
    v = (v or "").strip()
    if v == "" or v.lower() in ("nan", "na"):
        return ""
    try:
        f = float(v)
    except ValueError:
        return v
    return f"{f:.6g}"


def lire_formatte(chemin, colonnes):
    """Lit un fichier au format vague 4 : deux lignes d'entete, puis une ligne par sujet.

    La deuxieme ligne du fichier repete le libelle des questions, elle n'est pas une
    observation. Retourne un dict id -> liste de valeurs canoniques.
    """
    lignes = list(csv.reader(open(chemin, newline="", encoding="utf-8")))
    entete = lignes[0]
    pos = {c: entete.index(c) for c in colonnes if c in entete}
    if len(pos) != len(colonnes):
        sys.exit(f"{chemin} : {len(colonnes) - len(pos)} colonnes attendues absentes.")
    i_id = entete.index("TWIN_ID")
    out = {}
    for ligne in lignes[2:]:
        if not ligne or not ligne[i_id].strip().isdigit():
            continue
        out[int(ligne[i_id])] = [canon(ligne[pos[c]]) for c in colonnes]
    return out


def charger_twin(racine):
    """Prepare le ou les jeux Twin-2K-500.

    Retourne une LISTE de jeux, et non un seul. Raison, verifiee sur les fichiers : trois
    des treize configurations publiees ne couvrent pas les 2058 sujets.
    `JSON Persona - GPT4.1-mini` n'en couvre que 1000, `LLM Finetuning (500 training
    samples) - GPT4.1-mini` 1558, soit les 2058 moins les 500 sujets d'entrainement, et
    `JSON Persona (Predicted Output) - GPT4.1` 2050. Les melanger aux dix autres serait
    faux de deux facons : le bootstrap apparie perdrait son appariement, et le
    denominateur humain ne serait pas calcule sur les memes personnes. Chacune de ces
    trois configurations reçoit donc son propre jeu, avec les humains recalcules sur ses
    seuls sujets. C'est explicite dans les tableaux et dans la figure.
    """
    dossier = os.path.join(racine, "llm_specs")
    p_cat = os.path.join(racine, "question_catalog_and_human_response_csv",
                         "question_catalog.json")
    p_map = os.path.join(racine, "llm", "wave4_formatted_to_catalog_mapping.json")
    p_demo = os.path.join(racine, "question_catalog_and_human_response_csv",
                          "wave1_3_response_label.csv")
    manques = [c for c in (dossier, p_cat, p_map, p_demo) if not os.path.exists(c)]
    if manques:
        return [], [f"absent : {c}" for c in manques]

    catalogue = {q["QuestionID"]: q for q in json.load(open(p_cat, encoding="utf-8"))}
    mapping = json.load(open(p_map, encoding="utf-8"))
    # Cible : les seules questions categorielles de la vague 4. Les curseurs 0-100 et les
    # saisies libres sont ecartes, l'egalite exacte n'y a pas de sens. Meme choix qu'en a2.
    garder_map = [e for e in mapping
                  if catalogue[e["QuestionID"]]["QuestionType"] in ("MC", "Matrix")]
    colonnes = [e["formatted_column"] for e in garder_map]
    est_ordinal = np.array([catalogue[e["QuestionID"]]["QuestionType"] == "Matrix"
                            for e in garder_map])
    blocs = {catalogue[e["QuestionID"]]["BlockName"] for e in garder_map}
    if "Demographics" in blocs:
        return [], ["une question de la vague 4 appartient au bloc Demographics, "
                    "l'exclusion doit etre traitee avant toute mesure"]

    REF, CTRL = "humains vague 4", "humains vagues 1-3 (retest)"
    fichiers = [(REF, "humains_wave4.csv"), (CTRL, "humains_wave1_3.csv")]
    index = json.load(open(os.path.join(dossier, "index.json"), encoding="utf-8"))
    for e in index:
        fichiers.append((e["configuration"], e["fichier"]))

    tables, absents = {}, []
    for libelle, fichier in fichiers:
        chemin = os.path.join(dossier, fichier)
        if not os.path.exists(chemin):
            absents.append(fichier)
            continue
        tables[libelle] = lire_formatte(chemin, colonnes)
    if REF not in tables or CTRL not in tables:
        return [], ["les deux fichiers humains de reference de Twin sont absents"]
    noms = [l for l, _ in fichiers if l in tables]
    ids_complet = sorted(tables[REF])

    alertes = [f"twin, fichier annonce mais absent : {f}" for f in absents]
    complets, partielles = [], []
    for c in noms:
        if c in (REF, CTRL):
            continue
        if sorted(tables[c]) == ids_complet:
            complets.append(c)
        else:
            partielles.append(c)
            alertes.append(f"twin, {c} ne couvre que {len(tables[c])} des "
                           f"{len(ids_complet)} sujets : analysee a part, humains "
                           "recalcules sur ce sous ensemble")

    # Nomenclature commune a tous les jeux : union des modalites observees partout.
    n_items = len(colonnes)
    modalites = []
    for j in range(n_items):
        vus = set()
        for c in noms:
            vus.update(t[j] for t in tables[c].values())
        vus.discard("")
        try:
            mods = sorted(vus, key=float)
        except ValueError:
            mods = sorted(vus)
        modalites.append(mods)
    k_max = max(len(m) for m in modalites)
    val_ord = np.zeros((n_items, k_max))
    for j, m in enumerate(modalites):
        if est_ordinal[j] and len(m) > 1:
            val_ord[j, :len(m)] = np.arange(len(m)) / (len(m) - 1)
    idx_mod = [{m: k for k, m in enumerate(mods)} for mods in modalites]

    demo = {int(r["pid"]): r for r in csv.DictReader(open(p_demo, encoding="utf-8"))}
    inconnus = [i for i in ids_complet if i not in demo]
    if inconnus:
        return [], [f"{len(inconnus)} sujets Twin sans demographie"]

    def construire(libelle, conditions, ids):
        code = {}
        for c in conditions:
            x = np.full((len(ids), n_items), -1, dtype=np.int16)
            for i, pid in enumerate(ids):
                ligne = tables[c][pid]
                for j in range(n_items):
                    k = idx_mod[j].get(ligne[j], -1)
                    if k >= 0:
                        x[i, j] = k
            code[c] = x
        brut = {}
        for axe, qid in DEMOS_TWIN.items():
            brut[axe] = [demo[i].get(qid, "").strip() for i in ids]
        brut["profil croise"] = [f"{g}|{r}|{bloc_ideologie_twin(p)}" for g, r, p
                                 in zip(brut["genre"], brut["ethnicite"],
                                        brut["ideologie politique"])]
        seg, niveaux = {}, {}
        for axe in AXES_TWIN:
            mods = sorted({v for v in brut[axe] if v != ""})
            iv = {m: k for k, m in enumerate(mods)}
            seg[axe] = np.array([iv.get(v, -1) for v in brut[axe]], dtype=np.int16)
            niveaux[axe] = mods
        return {"libelle": libelle, "noms": conditions, "reference": REF,
                "controle": CTRL, "n": len(ids), "items": colonnes, "n_items": n_items,
                "axes": AXES_TWIN, "seg": seg, "niveaux": niveaux,
                "garder": np.ones(n_items, dtype=bool), "est_ordinal": est_ordinal,
                "principal": (code, val_ord, k_max), "ordinal": None,
                "notes": {"absents": absents, "blocs": sorted(blocs),
                          "partielles": partielles}}

    jeux = [construire("twin2k500", [REF, CTRL] + complets, ids_complet)]
    for c in partielles:
        ids = sorted(set(tables[c]) & set(ids_complet))
        jeux.append(construire(f"twin2k500 sous ensemble {len(ids)} sujets",
                               [REF, CTRL, c], ids))
    return jeux, alertes


# ---------------------------------------------------------------------------
# 4. Le moteur commun : observation, controle de permutation, bootstrap
# ---------------------------------------------------------------------------

def analyser(jeu, rng, n_bootstrap, n_permutations, verbeux=True):
    """Applique a un jeu la meme chaine que a1. Ne contient aucune formule de dispersion.

    Deux codages sont possibles. `principal` sert a M1 et M2, `ordinal` si present sert a
    M3. Quand `ordinal` est absent, le meme codage sert aux trois mesures, exactement
    comme dans a1 sur le GSS.
    """
    noms, axes, seg = jeu["noms"], jeu["axes"], jeu["seg"]
    n, n_items, n_axes = jeu["n"], jeu["n_items"], len(axes)
    garder, est_ordinal = jeu["garder"], jeu["est_ordinal"]
    g_max = int(max(len(jeu["niveaux"][a]) for a in axes))
    ref = jeu["reference"]

    codeP, valP, kP = jeu["principal"]
    paires = {}
    for c in noms:
        ip, pp = construire_index(codeP[c], seg, kP, g_max, n_items, axes=axes)
        paires[c] = [(ip, pp, valP, kP)]
    if jeu["ordinal"] is not None:
        codeO, valO, kO = jeu["ordinal"]
        for c in noms:
            io, po = construire_index(codeO[c], seg, kO, g_max, n_items, axes=axes)
            paires[c].append((io, po, valO, kO))

    def mesurer_index(liste, lignes):
        d = decomposer(compter(liste[0][0], lignes, liste[0][1], n_items, g_max,
                               liste[0][3], n_axes), liste[0][2])
        if len(liste) > 1:
            d2 = decomposer(compter(liste[1][0], lignes, liste[1][1], n_items, g_max,
                                    liste[1][3], n_axes), liste[1][2])
            d = dict(d)
            d["variance_ordinale"] = d2["variance_ordinale"]
        return d

    toutes = np.arange(n)
    dec = {c: mesurer_index(paires[c], toutes) for c in noms}
    observe = {c: agreger(dec[c], garder, est_ordinal) for c in noms}

    # Controle des estimateurs : sous permutation des etiquettes de segment, le terme
    # inter doit valoir zero. Ce qui subsiste est soustrait. Identique a a1.
    # Diagnostic : les memes ratios calcules sur les SEULS items ordinaux. Il existe
    # parce que M3 ne porte que sur ceux la, alors que M1 et M2 portent sur tous : sans
    # ce calcul, un desaccord entre M3 et les deux autres ne serait pas separable d'un
    # simple effet de jeu d'items. Sans intervalle : c'est un diagnostic, pas un chiffre
    # publiable tel quel.
    masque_ord = garder & est_ordinal
    observe_ord = {c: agreger(dec[c], masque_ord, est_ordinal) for c in noms}
    nul_ord = {c: {m: 0.0 for m in MESURES} for c in noms}

    nul = {c: {m: 0.0 for m in MESURES} for c in noms}
    nul_axe = {c: {a: {m: 0.0 for m in MESURES} for a in axes} for c in noms}
    if n_permutations > 0:
        for c in noms:
            vals = {m: [] for m in MESURES}
            vals_ord = {m: [] for m in MESURES}
            vals_axe = {a: {m: [] for m in MESURES} for a in axes}
            for _ in range(n_permutations):
                perm = rng.permutation(n)
                segp = {a: seg[a][perm] for a in axes}
                liste = []
                ip, pp = construire_index(codeP[c], segp, kP, g_max, n_items, axes=axes)
                liste.append((ip, pp, valP, kP))
                if jeu["ordinal"] is not None:
                    io, po = construire_index(jeu["ordinal"][0][c], segp, kO, g_max,
                                              n_items, axes=axes)
                    liste.append((io, po, valO, kO))
                d = mesurer_index(liste, toutes)
                agg = agreger(d, garder, est_ordinal)
                agg_ord = agreger(d, masque_ord, est_ordinal)
                for m in MESURES:
                    vals[m].append(agg[m][0])
                    vals_ord[m].append(agg_ord[m][0])
                for i_a, a in enumerate(axes):
                    agg_a = agreger(d, garder, est_ordinal, axes_gardes=[i_a])
                    for m in MESURES:
                        vals_axe[a][m].append(agg_a[m][0])
            nul[c] = {m: float(np.mean(vals[m])) for m in MESURES}
            nul_ord[c] = {m: float(np.mean(vals_ord[m])) for m in MESURES}
            nul_axe[c] = {a: {m: float(np.mean(vals_axe[a][m])) for m in MESURES}
                          for a in axes}

    point = {c: {m: (observe[c][m][0] - nul[c][m], observe[c][m][1]) for m in MESURES}
             for c in noms}
    base = point[ref]
    ratios = {c: {m: (point[c][m][0] / base[m][0] if base[m][0] else float("nan"),
                      point[c][m][1] / base[m][1] if base[m][1] else float("nan"))
                  for m in MESURES} for c in noms}

    brut = {c: {m: ([], []) for m in MESURES} for c in noms}
    for b in range(n_bootstrap):
        lignes = rng.integers(0, n, size=n)
        for c in noms:
            agg = agreger(mesurer_index(paires[c], lignes), garder, est_ordinal)
            for m in MESURES:
                brut[c][m][0].append(agg[m][0])
                brut[c][m][1].append(agg[m][1])
        if verbeux and n_bootstrap >= 10 and (b + 1) % max(1, n_bootstrap // 10) == 0:
            print(f"    bootstrap {b + 1}/{n_bootstrap}", flush=True)

    boot = {c: {m: (recentrer(brut[c][m][0], point[c][m][0]),
                    recentrer(brut[c][m][1], point[c][m][1])) for m in MESURES}
            for c in noms}
    ratio_boot = {c: {m: (boot[c][m][0] / boot[ref][m][0],
                          boot[c][m][1] / boot[ref][m][1]) for m in MESURES}
                  for c in noms}

    par_axe = {}
    for c in noms:
        par_axe[c] = {}
        for i_a, a in enumerate(axes):
            agg = agreger(dec[c], garder, est_ordinal, axes_gardes=[i_a])
            par_axe[c][a] = {m: (agg[m][0] - nul_axe[c][a][m], agg[m][1])
                             for m in MESURES}

    globaux = {c: {m: (point[c][m][0] + point[c][m][1]) / (base[m][0] + base[m][1])
                   for m in MESURES} for c in noms}

    point_ord = {c: {m: (observe_ord[c][m][0] - nul_ord[c][m], observe_ord[c][m][1])
                     for m in MESURES} for c in noms}
    base_ord = point_ord[ref]
    ratios_ord = {c: {m: (point_ord[c][m][0] / base_ord[m][0] if base_ord[m][0] else
                          float("nan"),
                          point_ord[c][m][1] / base_ord[m][1] if base_ord[m][1] else
                          float("nan")) for m in MESURES} for c in noms}
    return {"jeu": jeu, "dec": dec, "point": point, "ratios": ratios,
            "ratio_boot": ratio_boot, "par_axe": par_axe, "globaux": globaux,
            "nul": nul, "observe": observe, "ratios_ordinal": ratios_ord,
            "n_items_ordinal": int(masque_ord.sum())}


# ---------------------------------------------------------------------------
# 5. Ecriture des tableaux
# ---------------------------------------------------------------------------

def table_ratios(res, chemin, titre):
    jeu = res["jeu"]
    lignes = [["condition", "mesure", "ratio_inter", "inter_ic_bas", "inter_ic_haut",
               "ratio_intra", "intra_ic_bas", "intra_ic_haut", "produit",
               "ratio_dispersion_globale"]]
    print("\n" + "=" * 100)
    print(titre)
    print("=" * 100)
    for m in MESURES:
        print(f"\n--- {m} ---")
        print(f"{'condition':<40}{'ratio inter':>27}{'ratio intra':>25}"
              f"{'produit':>9}{'global':>9}")
        for c in jeu["noms"]:
            ri, ra = res["ratios"][c][m]
            i1, i2, _ = ic(res["ratio_boot"][c][m][0])
            a1_, a2_, _ = ic(res["ratio_boot"][c][m][1])
            g = res["globaux"][c][m]
            print(f"{c:<40}{ri:>9.3f} [{i1:6.3f} ; {i2:6.3f}]"
                  f"{ra:>9.3f} [{a1_:5.3f} ; {a2_:5.3f}]{ri * ra:>9.3f}{g:>9.3f}")
            lignes.append([c, m, f"{ri:.4f}", f"{i1:.4f}", f"{i2:.4f}", f"{ra:.4f}",
                           f"{a1_:.4f}", f"{a2_:.4f}", f"{ri * ra:.4f}", f"{g:.4f}"])
    with open(chemin, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


def table_diagnostic_ordinal(resultats, chemin):
    """Les memes ratios sur les seuls items ordinaux, pour separer effet de mesure et
    effet de jeu d'items. N'a de sens que si tous les items ne sont pas ordinaux."""
    lignes = [["jeu", "condition", "mesure", "ratio_inter_items_ordinaux",
               "ratio_intra_items_ordinaux", "n_items_ordinaux"]]
    imprime = False
    for res in resultats:
        jeu = res["jeu"]
        if res["n_items_ordinal"] == int(jeu["garder"].sum()):
            continue                      # tous les items sont ordinaux, rien a separer
        if not imprime:
            print("\n" + "=" * 100)
            print("DIAGNOSTIC : LES MEMES RATIOS SUR LES SEULS ITEMS ORDINAUX")
            print("M3 ne porte que sur ces items la, M1 et M2 portent sur tous. Ce tableau")
            print("dit si un desaccord entre M3 et les deux autres vient de la mesure ou du")
            print("jeu d'items. Sans intervalle de confiance : diagnostic, pas resultat.")
            print("=" * 100)
            imprime = True
        print(f"\n{jeu['libelle']}, {res['n_items_ordinal']} items ordinaux sur "
              f"{int(jeu['garder'].sum())}")
        print(f"{'condition':<48}" + "".join(f"{m[:14]:>16}" for m in MESURES)
              + "   <- ratio inter")
        for c in jeu["noms"]:
            cellules = "".join(f"{res['ratios_ordinal'][c][m][0]:>16.3f}"
                               for m in MESURES)
            print(f"{c:<48}{cellules}")
            for m in MESURES:
                lignes.append([jeu["libelle"], c, m,
                               f"{res['ratios_ordinal'][c][m][0]:.4f}",
                               f"{res['ratios_ordinal'][c][m][1]:.4f}",
                               res["n_items_ordinal"]])
        print(f"{'condition':<48}" + "".join(f"{m[:14]:>16}" for m in MESURES)
              + "   <- ratio intra")
        for c in jeu["noms"]:
            cellules = "".join(f"{res['ratios_ordinal'][c][m][1]:>16.3f}"
                               for m in MESURES)
            print(f"{c:<48}{cellules}")
    if imprime:
        with open(chemin, "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(lignes)


def table_par_axe(resultats, chemin):
    lignes = [["jeu", "condition", "axe", "mesure", "ratio_inter", "ratio_intra"]]
    for res in resultats:
        jeu = res["jeu"]
        ref = jeu["reference"]
        print("\n" + "-" * 100)
        print(f"DETAIL PAR AXE, {jeu['libelle']}, mesure entropie, ratio inter")
        print(f"{'condition':<40}" + "".join(f"{a[:15]:>15}" for a in jeu["axes"]))
        for c in jeu["noms"]:
            cellules = ""
            for a in jeu["axes"]:
                b = res["par_axe"][ref][a]
                for m in MESURES:
                    if b[m][0] > 0 and b[m][1] > 0:
                        lignes.append([jeu["libelle"], c, a, m,
                                       f"{res['par_axe'][c][a][m][0] / b[m][0]:.4f}",
                                       f"{res['par_axe'][c][a][m][1] / b[m][1]:.4f}"])
                v = (res["par_axe"][c][a]["entropie"][0] / b["entropie"][0]
                     if b["entropie"][0] > 0 else float("nan"))
                cellules += f"{v:>15.2f}"
            print(f"{c:<40}{cellules}")
    with open(chemin, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


def table_permutation(resultats, chemin):
    lignes = [["jeu", "condition", "mesure", "inter_observe", "inter_sous_permutation",
               "part"]]
    print("\n" + "=" * 100)
    print("CONTROLE DES ESTIMATEURS : terme inter obtenu sous permutation des segments,")
    print("en part du terme inter observe. Proche de zero = l'estimateur analytique suffit.")
    print("=" * 100)
    for res in resultats:
        jeu = res["jeu"]
        print(f"\n{jeu['libelle']}")
        print(f"{'condition':<40}" + "".join(f"{m[:16]:>18}" for m in MESURES))
        for c in jeu["noms"]:
            cellules = ""
            for m in MESURES:
                o = res["observe"][c][m][0]
                p = res["nul"][c][m]
                part = p / o if o else float("nan")
                cellules += f"{part:>18.3f}"
                lignes.append([jeu["libelle"], c, m, f"{o:.6f}", f"{p:.6f}",
                               f"{part:.4f}"])
            print(f"{c:<40}{cellules}")
    with open(chemin, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 6. Le test des variantes demographiques hors GSS
# ---------------------------------------------------------------------------

def variantes(racine, resultats_osf, chemin):
    """Reprend a1 section 7 sur les jeux economiques et le Big Five.

    Question : le facteur 7 entre les deux generations dites demographiques, et le facteur
    13,5 entre persona et demographique fig.3 a exactitude indistinguable, se reproduisent
    ils hors du GSS ?
    """
    lignes = [["jeu", "comparaison", "grandeur", "valeur_a", "valeur_b", "ecart_ou_facteur",
               "ic_bas", "ic_haut", "t", "conclusion"]]
    print("\n" + "=" * 100)
    print("LES DEUX GENERATIONS DITES DEMOGRAPHIQUES, HORS GSS")
    print("=" * 100)
    for res in resultats_osf:
        jeu = res["jeu"]
        nom_jeu = jeu["libelle"]
        p = os.path.join(racine, f"figure2/data/new_analysis_summaries/{nom_jeu}"
                                 "/analysis/individual_level.csv")
        # Etiquette de generation complete, du type econ_games_v8 : elle est reconstruite
        # depuis le nom de fichier de la condition, pas depuis le libelle abrege, sinon
        # la colonne p_wave1__<etiquette>__correl n'est pas trouvee.
        etq = {libelle: fichier[:-len("_summary.csv")]
               for libelle, fichier in jeu["notes"]["conditions"]}
        cibles = {}
        for c in jeu["noms"]:
            if "demographiques fig.2" in c:
                cibles["demo2"] = c
            elif "demographiques fig.3" in c:
                cibles["demo3"] = c
            elif "persona" in c:
                cibles["persona"] = c
            elif "entretien" in c:
                cibles["entretien"] = c
        print(f"\n{nom_jeu}")

        # 1. le facteur sur le ratio inter
        for a, b in (("demo2", "demo3"), ("persona", "demo3"), ("demo2", "persona")):
            if a not in cibles or b not in cibles:
                continue
            ca, cb = cibles[a], cibles[b]
            ra = res["ratios"][ca]["entropie"][0]
            rb = res["ratios"][cb]["entropie"][0]
            ia = ic(res["ratio_boot"][ca]["entropie"][0])
            ib = ic(res["ratio_boot"][cb]["entropie"][0])
            facteur = max(ra, rb) / min(ra, rb) if min(ra, rb) > 0 else float("nan")
            disjoint = (ia[1] < ib[0]) or (ib[1] < ia[0])
            print(f"  ratio inter  {ca:<34} {ra:6.3f} [{ia[0]:.3f};{ia[1]:.3f}]")
            print(f"               {cb:<34} {rb:6.3f} [{ib[0]:.3f};{ib[1]:.3f}]"
                  f"   facteur {facteur:.2f}, "
                  f"{'intervalles disjoints' if disjoint else 'intervalles qui se chevauchent'}")
            lignes.append([nom_jeu, f"{ca} vs {cb}", "ratio_inter_entropie",
                           f"{ra:.4f}", f"{rb:.4f}", f"{facteur:.4f}", "", "", "",
                           "disjoints" if disjoint else "chevauchement"])

        # 2. ce que voit la metrique du papier, correlation et MAE par individu
        if not os.path.exists(p):
            print(f"  {p} absent, test apparie non calcule.")
            lignes.append([nom_jeu, "", "individual_level.csv", "", "", "", "", "", "",
                           "fichier absent"])
            continue
        rows = list(csv.DictReader(open(p, encoding="utf-8")))

        def col(etiquette, grandeur):
            nom = f"p_wave1__{etiquette}__{grandeur}"
            if nom not in rows[0]:
                return None
            v = np.array([float(r[nom]) for r in rows])
            v[v <= -1e4] = np.nan          # sentinelle -100000 du paquet
            return v

        for grandeur in ("correl", "mae"):
            for a, b in (("demo2", "demo3"), ("persona", "demo3")):
                if a not in cibles or b not in cibles:
                    continue
                x, y = col(etq[cibles[a]], grandeur), col(etq[cibles[b]], grandeur)
                if x is None or y is None:
                    continue
                d = x - y
                d = d[np.isfinite(d)]
                se = d.std(ddof=1) / np.sqrt(d.size)
                t = d.mean() / se
                verdict = "indistinguables" if abs(t) < 1.96 else "distinguables"
                print(f"  {grandeur:<7} {etq[cibles[a]]:>16} "
                      f"{np.nanmean(x):6.3f}  contre {etq[cibles[b]]:>16} "
                      f"{np.nanmean(y):6.3f}  ecart {d.mean():+.4f} "
                      f"[{d.mean() - 1.96 * se:+.4f};{d.mean() + 1.96 * se:+.4f}] "
                      f"t={t:+.2f} -> {verdict}  (n={d.size})")
                lignes.append([nom_jeu, f"{etq[cibles[a]]} vs {etq[cibles[b]]}", grandeur,
                               f"{np.nanmean(x):.4f}", f"{np.nanmean(y):.4f}",
                               f"{d.mean():.4f}", f"{d.mean() - 1.96 * se:.4f}",
                               f"{d.mean() + 1.96 * se:.4f}", f"{t:.4f}", verdict])
    with open(chemin, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 7. Twin : exactitude par configuration, pour situer les points de la figure
# ---------------------------------------------------------------------------

def table_twin_configurations(resultats, chemin):
    """Exactitude cellule a cellule de chaque configuration contre les humains vague 4.

    Sert de contrepoint aux ratios : la question du dossier est de savoir si une
    configuration exacte peut avoir une structure fausse. Chaque configuration est
    comparee aux humains sur ses PROPRES sujets, ce qui est la raison d'etre du decoupage
    en plusieurs jeux, cf. charger_twin.
    """
    lignes = [["jeu", "configuration", "n_sujets", "exactitude_vs_humains_w4",
               "n_cellules", "accord_par_paires", "modalites_par_item"]]
    print("\n" + "=" * 100)
    print("TWIN-2K-500 : exactitude et homogeneite par configuration")
    print("Accord par paires : probabilite que deux repondants tires au hasard donnent la")
    print("meme reponse. Plus il est haut, plus la population simulee est homogene.")
    print("=" * 100)
    print(f"{'configuration':<48}{'n':>6}{'exactitude':>12}{'accord paires':>15}"
          f"{'modalites':>11}")
    vus = set()
    for res in resultats:
        jeu = res["jeu"]
        code = jeu["principal"][0]
        ref = code[jeu["reference"]]
        for c in jeu["noms"]:
            if c in vus and c != jeu["reference"]:
                continue
            if c in vus:
                continue
            vus.add(c)
            x = code[c]
            valide = (x >= 0) & (ref >= 0)
            acc = float((x[valide] == ref[valide]).mean())
            parts = []
            for j in range(jeu["n_items"]):
                col = x[:, j][x[:, j] >= 0]
                if col.size < 2:
                    continue
                n_k = np.bincount(col)
                parts.append(float((n_k * (n_k - 1)).sum()
                                   / (col.size * (col.size - 1))))
            paires = float(np.mean(parts)) if parts else float("nan")
            mods = float(np.mean([len(np.unique(x[:, j][x[:, j] >= 0]))
                                  for j in range(jeu["n_items"])]))
            print(f"{c:<48}{jeu['n']:>6}{acc:>12.4f}{paires:>15.4f}{mods:>11.2f}")
            lignes.append([jeu["libelle"], c, jeu["n"], f"{acc:.4f}",
                           int(valide.sum()), f"{paires:.4f}", f"{mods:.4f}"])
    with open(chemin, "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 8. Test 3 : le GSS revisite, sous ensemble attitudinal et mediane item par item
# ---------------------------------------------------------------------------
#
# Regle d'appartenance au sous ensemble attitudinal : elle est mecanique et porte sur le
# JEU DE MODALITES de l'item, jamais sur le texte de la question, pour qu'aucun jugement
# ne s'y glisse. Un item est attitudinal si ses modalites forment une echelle d'opinion.
# La liste est donnee ici en entier et figure au rapport.
ECHELLES_ATTITUDINALES = [
    ("too little", "about right", "too much"),
    ("a great deal", "only some", "hardly any"),
    ("strongly agree", "agree", "disagree", "strongly disagree"),
    ("strongly agree", "agree", "neither agree nor disagree", "disagree",
     "strongly disagree"),
    ("agree", "disagree"),
    ("allowed", "not allowed"),
    ("yes, allowed to speak", "not allowed"),
    ("remove", "not remove"),
    ("favor", "oppose"),
    ("approve", "disapprove"),
    ("always wrong", "almost always wrong", "sometimes wrong", "not wrong at all"),
    ("too harshly", "about right", "not harshly enough"),
    ("very likely", "somewhat likely", "somewhat unlikely", "very unlikely"),
]


def gss_tests(racine, sortie, n_bootstrap):
    prep = os.path.join(racine,
                        "figure2/data/new_analysis_summaries/gss_filtered/preparation")
    if not os.path.isdir(prep):
        print("\nGSS absent, tests 3 non faits.")
        return
    options, ordinal = lire_nomenclature(racine)
    entetes = next(csv.reader(open(os.path.join(prep, "p_wave1_summary.csv"),
                                   encoding="utf-8")))[1:]
    conditions = [("humains vague 1", "p_wave1_summary.csv"),
                  ("humains vague 2", "p_wave2_summary.csv"),
                  ("agents composite", "composite_agents_summary.csv"),
                  ("agents entretien (v3)", "gss_v3_summary.csv"),
                  ("agents enquete", "survey_agents_summary.csv"),
                  ("agents persona (v7)", "gss_v7_summary.csv"),
                  ("agents demographiques (v6)", "gss_v6_summary.csv"),
                  ("agents demographiques (v8)", "gss_v8_summary.csv")]
    donnees, ids_ref = {}, None
    for libelle, fichier in conditions:
        chemin = os.path.join(prep, fichier)
        if not os.path.exists(chemin):
            continue
        x, ids, _ = lire_condition(chemin, entetes, options)
        ids_ref = ids_ref or ids
        donnees[libelle] = x
    noms = [c for c, _ in conditions if c in donnees]
    seg, niveaux = lire_demographies(racine, ids_ref)
    n = len(ids_ref)

    garder = np.array([q not in ITEMS_DEMOGRAPHIQUES for q in entetes])
    ensembles = {tuple(e) for e in ECHELLES_ATTITUDINALES}
    attitudinal = np.array([tuple(options[q]) in ensembles for q in entetes])
    garder_att = garder & attitudinal
    print("\n" + "=" * 100)
    print("TEST 3a : SILHOUETTE SUR LE SEUL SOUS ENSEMBLE ATTITUDINAL DU GSS")
    print("=" * 100)
    print(f"{int(garder_att.sum())} items attitudinaux retenus sur {int(garder.sum())} "
          f"items non demographiques, regle mecanique sur le jeu de modalites")
    print("Items retenus : " + ", ".join(q for q, k in zip(entetes, garder_att) if k))

    rng = np.random.default_rng(20260907)
    lignes = [["sous_ensemble", "condition", "axe", "silhouette", "ic_bas", "ic_haut"]]
    for nom_sous, masque in (("attitudinal", garder_att), ("tous items non demo", garder)):
        dist = {c: matrice_distance(donnees[c], masque) for c in noms}
        point = {c: {a: silhouette(dist[c], seg[a], len(niveaux[a])) for a in AXES}
                 for c in noms}
        brut = {c: {a: [] for a in AXES} for c in noms}
        for _ in range(n_bootstrap):
            tirage = rng.integers(0, n, size=n)
            poids = np.bincount(tirage, minlength=n).astype(np.float32)
            for c in noms:
                for a in AXES:
                    brut[c][a].append(silhouette(dist[c], seg[a], len(niveaux[a]), poids))
        print(f"\n--- {nom_sous} ---")
        print(f"{'condition':<28}" + "".join(f"{a[:20]:>22}" for a in AXES))
        for c in noms:
            cellules = ""
            for a in AXES:
                s = point[c][a]
                b1, b2, _ = ic(recentrer(brut[c][a], s))
                cellules += f"{s:>7.3f} [{b1:6.3f};{b2:6.3f}]"
                lignes.append([nom_sous, c, a, f"{s:.4f}", f"{b1:.4f}", f"{b2:.4f}"])
            print(f"{c:<28}{cellules}")
    with open(os.path.join(sortie, "a6-gss-silhouette-attitudinale.csv"), "w",
              newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)

    # Test 3b : mediane des ratios item par item, limite 1 de a1.
    print("\n" + "=" * 100)
    print("TEST 3b : MEDIANE DES RATIOS ITEM PAR ITEM, GSS")
    print("=" * 100)
    est_ordinal = np.array([ordinal.get(q, False) for q in entetes])
    k_par_item = np.array([len(options[q]) for q in entetes])
    n_items = len(entetes)
    k_max = int(k_par_item.max())
    g_max = int(max(len(niveaux[a]) for a in AXES))
    val_ord = np.zeros((n_items, k_max))
    for j, q in enumerate(entetes):
        if est_ordinal[j] and k_par_item[j] > 1:
            val_ord[j, :k_par_item[j]] = np.arange(k_par_item[j]) / (k_par_item[j] - 1)
    toutes = np.arange(n)
    dec = {}
    for c in noms:
        idx, poub = construire_index(donnees[c], seg, k_max, g_max, n_items)
        dec[c] = decomposer(compter(idx, toutes, poub, n_items, g_max, k_max, len(AXES)),
                            val_ord)
    lignes = [["mesure", "sous_ensemble", "condition", "mediane_ratio_inter",
               "mediane_ratio_intra", "n_items"]]
    for m in ("entropie", "gini_simpson"):
        i_ref, a_ref, v_ref = dec["humains vague 1"][m]
        for nom_sous, masque in (("tous items non demo", garder),
                                 ("attitudinal", garder_att)):
            seuil = 0.002 if m == "entropie" else 0.001
            msk = v_ref & masque[None, :] & (i_ref > seuil)
            print(f"\n--- {m}, {nom_sous}, {int(msk.sum())} couples (axe, item) retenus ---")
            print(f"{'condition':<28}{'mediane inter':>16}{'mediane intra':>16}")
            for c in noms:
                i_c, a_c, _ = dec[c][m]
                r_i = float(np.median(i_c[msk] / i_ref[msk]))
                r_a = float(np.median(a_c[msk] / a_ref[msk]))
                print(f"{c:<28}{r_i:>16.3f}{r_a:>16.3f}")
                lignes.append([m, nom_sous, c, f"{r_i:.4f}", f"{r_a:.4f}",
                               str(int(msk.sum()))])
    with open(os.path.join(sortie, "a6-gss-mediane-item.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)


# ---------------------------------------------------------------------------
# 9. La figure
# ---------------------------------------------------------------------------

def lire_ratios_a1(chemin, mesure="entropie"):
    """Relit les points du GSS deja calcules par a1. On ne les recalcule pas."""
    if not os.path.exists(chemin):
        return None
    out = {}
    for r in csv.DictReader(open(chemin, encoding="utf-8")):
        if r["mesure"] != mesure:
            continue
        out[r["condition"]] = {
            "inter": float(r["ratio_inter"]), "intra": float(r["ratio_intra"]),
            "inter_ic": (float(r["inter_ic_bas"]), float(r["inter_ic_haut"])),
            "intra_ic": (float(r["intra_ic_bas"]), float(r["intra_ic_haut"])),
            "global": float(r["ratio_dispersion_globale"]),
        }
    return out


# Familles de conditions. Le marqueur porte la famille, pas le jeu de donnees : c'est ce
# qui permet de comparer un cadran a l'autre d'un coup d'oeil, et cela reste lisible en
# noir et blanc parce que forme et remplissage varient ensemble.
FAMILLES = [
    ("humains, reference", ("o", "white", 13)),
    ("humains, retest (controle)", ("s", "white", 9)),
    ("entretien", ("^", "black", 11)),
    ("questionnaire", ("D", "0.35", 9)),
    ("composite", ("v", "black", 11)),
    ("persona", ("P", "0.78", 13)),
    ("demographique, figure 2", ("X", "0.78", 13)),
    ("demographique, figure 3", ("*", "0.78", 17)),
    ("autre configuration", ("h", "0.55", 10)),
]
STYLE = dict(FAMILLES)


ABREGE = [("humains vague 1", "humains, ref."),
          ("humains vague 4", "humains, ref."),
          ("humains vague 2", "humains, retest"),
          ("humains vagues 1-3 (retest)", "humains, retest"),
          ("agents demographiques fig.2", "demo. fig.2"),
          ("agents demographiques fig.3", "demo. fig.3"),
          ("agents demographiques", "demo."),
          ("agents entretien", "entretien"),
          ("agents composite", "composite"),
          ("agents enquete", "enquete"),
          ("agents persona", "persona")]


def abreger(nom):
    """Etiquette courte, sur une seule ligne. La famille est deja portee par le marqueur,
    l'etiquette n'a donc a porter que ce qui distingue la condition dans son cadran."""
    for long, court in ABREGE:
        if nom.startswith(long):
            return court + nom[len(long):]
    return nom


def famille(nom):
    n = nom.lower()
    if "retest" in n or "vague 2" in n or "vagues 1-3" in n:
        return "humains, retest (controle)"
    if n.startswith("humains"):
        return "humains, reference"
    if "composite" in n:
        return "composite"
    if "entretien" in n:
        return "entretien"
    if "enquete" in n:
        return "questionnaire"
    if "demographiques fig.2" in n:
        return "demographique, figure 2"
    if "demographiques fig.3" in n or "demographics only" in n:
        return "demographique, figure 3"
    if "persona" in n and "json" not in n and "summary" not in n:
        return "persona"
    return "autre configuration"


def tracer(cadrans, sortie, mesure="entropie"):
    """Quatre cadrans, meme plan que a1 : ratio inter en abscisse, ratio intra en ordonnee.

    Chaque cadran garde ses propres bornes, sinon Twin, dont les ratios sont resserres,
    serait reduit a un amas de points au centre du cadran du GSS. Les deux reperes
    structurels sont en revanche identiques partout : le quadrant grise de la double
    distorsion et la droite du produit egal a 1. Le quatrieme cadran porte trop de
    conditions pour des etiquettes en clair : ses points sont numerotes et la legende
    numerotee est renvoyee dans le bandeau du bas, avec la legende des familles.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.patheffects as pe
        from matplotlib.lines import Line2D
    except ImportError:
        print("matplotlib absent, figure non produite.")
        return

    fig = plt.figure(figsize=(15.4, 13.6))
    # Les marges sont posees a la main : tight_layout ne sait pas traiter le bandeau
    # du bas, qui porte une legende ancree hors de ses axes.
    gs = fig.add_gridspec(3, 2, height_ratios=[1.0, 1.0, 0.46], hspace=0.34,
                          wspace=0.17, left=0.055, right=0.985, top=0.905,
                          bottom=0.015)
    axes_plot = [fig.add_subplot(gs[i // 2, i % 2]) for i in range(4)]
    ax_bas = fig.add_subplot(gs[2, :])
    ax_bas.set_axis_off()

    cle_numerotee = []
    for ax, (titre, points, numerote) in zip(axes_plot, cadrans):
        if not points:
            ax.text(0.5, 0.5, titre + "\n(non calcule)", ha="center", va="center")
            ax.set_axis_off()
            continue
        xs = [p["inter"] for p in points.values() if np.isfinite(p["inter"])]
        ys = [p["intra"] for p in points.values() if np.isfinite(p["intra"])]
        x_lo, x_hi = min(xs) * 0.45, max(xs) * 2.3
        y_lo, y_hi = min(ys) * 0.88, max(ys) * 1.26
        ax.fill_between([1.0, x_hi], y_lo, 1.0, color="0.905", zorder=0)
        t = np.geomspace(x_lo, x_hi, 400)
        ax.plot(t, 1.0 / t, color="black", lw=1.5, ls="--", zorder=2)
        ax.axhline(1.0, color="0.5", lw=0.8, zorder=1)
        ax.axvline(1.0, color="0.5", lw=0.8, zorder=1)

        numero = 0
        for nom, p in points.items():
            fam = STYLE[famille(nom)]
            mk, coul, taille = fam
            # Dans le cadran numerote, les deux points humains gardent une etiquette en
            # clair : ils se superposent en (1, 1) et deux chiffres imprimes l'un sur
            # l'autre y seraient illisibles.
            humain = famille(nom).startswith("humains")
            if numerote and not humain:
                taille = max(taille, 16)
            i1, i2 = p["inter_ic"]
            a1_, a2_ = p["intra_ic"]
            if np.isfinite(i1) and i2 > i1:
                ax.plot([max(i1, x_lo), min(i2, x_hi)], [p["intra"], p["intra"]],
                        color="black", lw=1.0, zorder=3)
                ax.plot([p["inter"], p["inter"]], [a1_, a2_], color="black", lw=1.0,
                        zorder=3)
            # Les petits marqueurs passent devant les grands, sinon ils disparaissent
            # dans l'amas du cadran d.
            ax.plot(p["inter"], p["intra"], marker=mk, ms=taille, mfc=coul,
                    mec="black", mew=1.3, ls="none", zorder=4 + (24 - taille) / 100.0)
            if numerote and not humain:
                numero += 1
                cle_numerotee.append((numero, nom, p["global"]))
                ax.annotate(str(numero), (p["inter"], p["intra"]),
                            textcoords="offset points", xytext=(0, 0),
                            ha="center", va="center", fontsize=7.5, zorder=6,
                            color="black",
                            path_effects=[pe.withStroke(linewidth=1.8,
                                                        foreground="white")])
            elif numerote:
                ax.annotate(f"{abreger(nom)}  |  {p['global']:.2f}",
                            (p["inter"], p["intra"]), textcoords="offset points",
                            xytext=(-10, 14) if "ref." in abreger(nom) else (12, 6),
                            ha="right" if "ref." in abreger(nom) else "left",
                            va="center", fontsize=8.0, zorder=5,
                            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="0.8",
                                      lw=0.5, alpha=0.92))
            else:
                ax.annotate(f"{abreger(nom)}  |  {p['global']:.2f}",
                            (p["inter"], p["intra"]), textcoords="offset points",
                            xytext=p.get("decalage", (0, 16)),
                            ha=p.get("align", "center"), va="center", fontsize=8.0,
                            zorder=5,
                            bbox=dict(boxstyle="round,pad=0.16", fc="white", ec="0.8",
                                      lw=0.5, alpha=0.92))

        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlim(x_lo, x_hi)
        ax.set_ylim(y_lo, y_hi)
        tx = [v for v in (0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2, 3, 5, 8, 12, 20, 35, 60)
              if x_lo <= v <= x_hi]
        ty = [v for v in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2)
              if y_lo <= v <= y_hi]
        ax.set_xticks(tx)
        ax.set_yticks(ty)
        ax.set_xticklabels([f"{v:g}" for v in tx])
        ax.set_yticklabels([f"{v:g}" for v in ty])
        ax.minorticks_off()
        ax.grid(True, which="major", color="0.88", lw=0.5)
        ax.set_axisbelow(True)
        ax.set_title(titre, fontsize=10.5)
        ax.set_xlabel("Ratio de dispersion ENTRE segments   (condition / humains)",
                      fontsize=9)
        ax.set_ylabel("Ratio de dispersion A L'INTERIEUR des segments", fontsize=9)

    poignees = [Line2D([], [], marker=mk, ms=min(t, 11), mfc=c, mec="black", mew=1.2,
                       ls="none", label=nom) for nom, (mk, c, t) in FAMILLES]
    poignees.append(Line2D([], [], color="black", lw=1.5, ls="--",
                           label="produit des deux ratios egal a 1 : faux deux fois,\n"
                                 "invisible sur une mesure globale de dispersion"))
    leg = ax_bas.legend(handles=poignees, loc="upper left", ncol=1, fontsize=8.0,
                        frameon=True, framealpha=0.95,
                        bbox_to_anchor=(0.0, 1.02), borderaxespad=0.0,
                        title="Familles de conditions, tous cadrans")
    leg.get_title().set_fontsize(8.5)
    if cle_numerotee:
        moitie = (len(cle_numerotee) + 1) // 2
        for k, debut in enumerate((0, moitie)):
            bloc = cle_numerotee[debut:debut + moitie]
            texte = "\n".join(f"{i}. {n}   (globale {g:.2f})" for i, n, g in bloc)
            ax_bas.text(0.335 + 0.335 * k, 0.92, texte, transform=ax_bas.transAxes,
                        fontsize=7.1, va="top", ha="left", linespacing=1.40)
        ax_bas.text(0.335, 1.02, "Cadran d, numeros des configurations Twin-2K-500",
                    transform=ax_bas.transAxes, fontsize=8.5, va="top", ha="left")

    fig.suptitle("La double distorsion hors du GSS et hors du pipeline de Stanford\n"
                 "quatre materiaux, meme decomposition par information mutuelle ; les "
                 "humains de reference sont en (1, 1) et leur retest doit y rester ;\n"
                 "zone grisee : ecarts entre groupes gonfles ET dispersion interne "
                 "ecrasee ; apres la barre verticale, ce que verrait une mesure GLOBALE "
                 "de dispersion", fontsize=12, y=0.985)
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(sortie, f"a6-figure-double-distorsion-multi-jeux.{ext}"),
                    dpi=200)
    plt.close(fig)


def points_de(res, mesure="entropie", decalages=None):
    jeu = res["jeu"]
    out = {}
    for c in jeu["noms"]:
        ri, ra = res["ratios"][c][mesure]
        i1, i2, _ = ic(res["ratio_boot"][c][mesure][0])
        a1_, a2_, _ = ic(res["ratio_boot"][c][mesure][1])
        out[c] = {"inter": ri, "intra": ra, "inter_ic": (i1, i2), "intra_ic": (a1_, a2_),
                  "global": res["globaux"][c][mesure]}
        if decalages and c in decalages:
            out[c]["decalage"], out[c]["align"] = decalages[c]
    return out


# ---------------------------------------------------------------------------
# 10. Programme principal
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine-osf", default=RACINE_OSF)
    ap.add_argument("--racine-twin", default=RACINE_TWIN)
    ap.add_argument("--sortie", default="resultats")
    ap.add_argument("--bootstrap", type=int, default=600)
    ap.add_argument("--permutations", type=int, default=30)
    ap.add_argument("--bootstrap-silhouette", type=int, default=250)
    ap.add_argument("--graine", type=int, default=20260907)
    ap.add_argument("--sans-twin", action="store_true")
    ap.add_argument("--sans-gss", action="store_true")
    ap.add_argument("--rapide", action="store_true")
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap, args.permutations, args.bootstrap_silhouette = 40, 5, 30
    os.makedirs(args.sortie, exist_ok=True)
    rng = np.random.default_rng(args.graine)

    print("=" * 100)
    print("a6 : LA DOUBLE DISTORSION HORS DU GSS ET HORS DU PIPELINE DE STANFORD")
    print("=" * 100)
    alertes = []
    resultats_osf, cadrans = [], []

    # --- cadran 1 : le GSS, relu de a1 -------------------------------------
    gss = lire_ratios_a1(os.path.join(args.sortie, "a1-ratios.csv"))
    if gss is None:
        alertes.append("resultats/a1-ratios.csv absent : le cadran GSS de la figure est vide")
        cadrans.append(("GSS, 1052 participants, 169 items (rappel de a1)", {}, False))
    else:
        pts = {c: {"inter": v["inter"], "intra": v["intra"],
                   "inter_ic": v["inter_ic"], "intra_ic": v["intra_ic"],
                   "global": v["global"]} for c, v in gss.items()}
        # Position de chaque etiquette, en points typographiques. Reglee a la main :
        # les points sont trop proches pour un placement automatique lisible.
        dec = {"humains vague 1": ((-10, 14), "right"),
               "humains vague 2": ((12, 8), "left"),
               "agents composite": ((-10, 16), "right"),
               "agents entretien (v3)": ((12, 4), "left"),
               "agents enquete": ((-10, -14), "right"),
               "agents persona (v7)": ((0, 18), "center"),
               "agents demographiques (v6)": ((0, -18), "center"),
               "agents demographiques (v8)": ((0, 18), "center")}
        for c, (d, a) in dec.items():
            if c in pts:
                pts[c]["decalage"], pts[c]["align"] = d, a
        cadrans.append(("a. General Social Survey, 1052 participants, 169 items,\n"
                        "pipeline de Stanford (chiffres de a1, non recalcules)",
                        pts, False))

    # --- cadrans 2 et 3 : jeux economiques et Big Five ---------------------
    dec_econ = {"humains vague 1": ((-8, 16), "right"),
                "humains vague 2": ((12, 8), "left"),
                "agents composite": ((6, -16), "left"),
                "agents enquete": ((6, 20), "left"),
                "agents entretien (v6)": ((-6, 20), "right"),
                "agents persona (v4)": ((4, -16), "left"),
                "agents demographiques fig.2 (v3)": ((0, -18), "center"),
                "agents demographiques fig.3 (v8)": ((-6, 18), "right")}
    dec_b5 = {"humains vague 1": ((10, 16), "left"),
              "humains vague 2": ((-8, 16), "right"),
              "agents composite": ((12, 8), "left"),
              "agents enquete": ((-4, -16), "right"),
              "agents entretien (v5)": ((-8, 16), "right"),
              "agents persona (v4)": ((0, -18), "center"),
              "agents demographiques fig.2 (v3)": ((0, -18), "center"),
              "agents demographiques fig.3 (v8)": ((0, 18), "center")}
    for jeu_nom, prefixe, echelle, titre, fichier_csv, decalages in (
            ("econ_games_main", "econ_games", (0.0, 1.0),
             "b. Jeux economiques, memes 1052 participants,\n"
             "5 mises, paquet OSF t6g7k", "a6-ratios-econ-games.csv", dec_econ),
            ("bigfive_main", "bigfive", (1.0, 5.0),
             "c. Big Five (BFI-44), memes 1052 participants,\n"
             "5 scores de trait, paquet OSF t6g7k", "a6-ratios-bigfive.csv", dec_b5)):
        jeu, manques = charger_osf_continu(args.racine_osf, jeu_nom, prefixe, echelle)
        alertes += [f"{jeu_nom} : {m}" for m in manques]
        if jeu is None:
            cadrans.append((titre, {}, False))
            continue
        print(f"\n--- {jeu_nom} : {jeu['n']} participants, {jeu['n_items']} variables, "
              f"{len(jeu['noms'])} conditions ---")
        print("Correspondance relue dans les fichiers PIPELINE du paquet :")
        for cle, tab in jeu["notes"]["etiquettes"].items():
            print(f"  {cle} : " + ", ".join(f"{k} = {v}" for k, v in sorted(tab.items())))
        print("Cellules hors echelle, ramenees aux bornes : " +
              ", ".join(f"{c} {v}" for c, v in jeu["notes"]["hors_echelle"].items()
                        if v) or "aucune")
        print("Classes effectives par variable pour M1 et M2 : "
              f"{jeu['notes']['classes']} (cible 5, fusion des bornes confondues)")
        res = analyser(jeu, rng, args.bootstrap, args.permutations)
        resultats_osf.append(res)
        table_ratios(res, os.path.join(args.sortie, fichier_csv),
                     f"LES DEUX RATIOS, {jeu_nom}, rapportes aux humains de la vague 1")
        cadrans.append((titre, points_de(res, decalages=decalages), False))

    # --- cadran 4 : Twin-2K-500 -------------------------------------------
    resultats_twin = []
    if args.sans_twin:
        cadrans.append(("d. Twin-2K-500 (non calcule)", {}, True))
    else:
        jeux_twin, alertes_twin = charger_twin(args.racine_twin)
        alertes += alertes_twin
        if not jeux_twin:
            cadrans.append(("d. Twin-2K-500 (non calcule)", {}, True))
        else:
            for k, jeu in enumerate(jeux_twin):
                print(f"\n--- {jeu['libelle']} : {jeu['n']} participants, "
                      f"{jeu['n_items']} items categoriels de la vague 4, "
                      f"{len(jeu['noms'])} conditions ---")
                if k == 0:
                    print("Segmentation : " + ", ".join(
                        f"{a} ({len(jeu['niveaux'][a])} segments)" for a in jeu["axes"]))
                    print(f"{int(jeu['est_ordinal'].sum())} items ordinaux "
                          "(matrices de Likert)")
                resultats_twin.append(
                    analyser(jeu, rng, args.bootstrap, args.permutations))
            table_ratios(resultats_twin[0],
                         os.path.join(args.sortie, "a6-ratios-twin.csv"),
                         "LES DEUX RATIOS, twin2k500, rapportes aux humains de la vague 4")
            for k, res in enumerate(resultats_twin[1:], start=1):
                table_ratios(res, os.path.join(
                    args.sortie, f"a6-ratios-twin-sous-ensemble-{k}.csv"),
                    f"LES DEUX RATIOS, {res['jeu']['libelle']}")
            table_twin_configurations(
                resultats_twin, os.path.join(args.sortie,
                                             "a6-twin-configurations.csv"))
            pts = points_de(resultats_twin[0])
            for res in resultats_twin[1:]:
                for c, v in points_de(res).items():
                    if c not in pts:
                        pts[c] = v
            cadrans.append(("d. Twin-2K-500, 2058 participants, 108 items categoriels\n"
                            "de la vague 4, auteurs et modeles differents",
                            pts, True))

    tous = resultats_osf + resultats_twin
    if tous:
        table_diagnostic_ordinal(
            tous, os.path.join(args.sortie, "a6-diagnostic-items-ordinaux.csv"))
        table_par_axe(tous, os.path.join(args.sortie, "a6-ratios-par-axe.csv"))
        table_permutation(tous, os.path.join(args.sortie, "a6-controle-permutation.csv"))
    if resultats_osf:
        variantes(args.racine_osf, resultats_osf,
                  os.path.join(args.sortie, "a6-variantes-demographiques.csv"))
    if not args.sans_gss:
        gss_tests(args.racine_osf, args.sortie, args.bootstrap_silhouette)

    tracer(cadrans, args.sortie)

    print("\n" + "=" * 100)
    if alertes:
        print("ALERTES, a reporter telles quelles dans le rapport :")
        for a in alertes:
            print("  - " + a)
    else:
        print("Aucun fichier attendu manquant, aucune correspondance d'etiquette ambigue.")
    print(f"\nEcrit dans {args.sortie}/ : a6-figure-double-distorsion-multi-jeux.png "
          "et .svg, a6-ratios-econ-games.csv, a6-ratios-bigfive.csv, a6-ratios-twin.csv,\n"
          "a6-ratios-par-axe.csv, a6-controle-permutation.csv, "
          "a6-variantes-demographiques.csv, a6-twin-configurations.csv,\n"
          "a6-gss-silhouette-attitudinale.csv, a6-gss-mediane-item.csv, "
          "a6-diagnostic-items-ordinaux.csv")


if __name__ == "__main__":
    main()
