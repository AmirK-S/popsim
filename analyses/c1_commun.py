"""
c1_commun : briques partagees par le mois 1 du programme C, version menages, cote humain.

Objet : les microdonnees du Survey of Consumer Expectations de la Federal Reserve Bank of
New York, panel tournant de menages americains reinterroges jusqu'a douze mois de suite.

Statut : script d'analyse jetable, AUCUN appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels et sans une ligne
recopiee : a2_commun (bootstrap sur les unites), a44_commun (permutation des personnes a
l'interieur du segment, Holm, Benjamini-Hochberg), i1_commun (AUC de Mann-Whitney, codage
des segments en entiers).

LE PREENREGISTREMENT EST resultats/c1-preenregistrement.md, ECRIT AVANT CE FICHIER, le
8 septembre 2026 a 22 h 30 CEST, depot d536169dc5361c38edcd723d48816e2ddd06dc4f.

Ce module porte cinq choses et rien d'autre.

  1. La lecture des fichiers Excel de la SCE et leur mise en cache hors du depot. La ligne 1
     de chaque feuille est la mention de source imposee par la licence FRBNY, la ligne 2
     l'entete, les donnees commencent ligne 3.

  2. La construction des douze variables d'anticipation declarees au preenregistrement
     section 2, dont les cinq variables signees, qui n'existent pas telles quelles dans le
     fichier : la SCE stocke une direction et une amplitude positive dans deux colonnes.

  3. Les cohortes declarees section 3, age x diplome x revenu, avec la cellule des non
     renseignes tenue a part.

  4. La decomposition inter / intra cohorte de la dispersion d'une variable continue, avec
     la correction de biais d'echantillonnage fini, transposition au continu de la logique
     des estimateurs Gini-Simpson a biais corrige de a1 et a35.

  5. La winsorisation aux bornes globales declarees, calculees une fois sur les 70 mois et
     appliquees a tous les mois a l'identique.

Aucune microdonnee n'est ecrite dans resultats/.
"""

import os
import sys
import tempfile

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a44_commun as C44
import i1_commun as I1
from a2_commun import bootstrap_personnes  # noqa: F401  (reexporte pour les scripts c1_*)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONNEES = os.path.join(RACINE, "data", "sce-fed-ny")
SORTIE = os.path.join(RACINE, "resultats")

# Le cache ne va ni dans data/, qui est en lecture seule, ni dans resultats/, qui ne recoit
# aucune microdonnee. Il va dans le repertoire temporaire, ou il peut disparaitre sans
# consequence : sa reconstruction coute deux minutes de lecture Excel.
CACHE = os.environ.get("POPSIM_CACHE_C1",
                       os.path.join(tempfile.gettempdir(), "popsim-c1-cache"))

GRAINE = 20260908
N_PERMUTATIONS = 200
N_BOOTSTRAP = 1000
N_MIN_COHORTE = 5        # seuil de repli sur la marginale, N_MIN_SEGMENT de a44
N_MIN_MOIS = 100         # controle bloquant C4
N_MIN_CHOC = 300         # controle bloquant C4
WINSOR = (2.0, 98.0)     # centiles, preenregistrement section 2.3

FICHIERS = {
    "2020-2024": "frbny-sce-public-microdata-20-24.xlsx",
    "2025": "frbny-sce-public-microdata-latest.xlsx",
    "2017-2019": "frbny-sce-public-microdata-complete-17-19.xlsx",
}
PRIMAIRE = ["2020-2024", "2025"]

# ---------------------------------------------------------------------------
# 1. Les variables declarees au preenregistrement section 2
# ---------------------------------------------------------------------------
#
# ECART AU PREENREGISTREMENT, section 2.1. Le questionnaire decrit cinq variables stockees
# en deux colonnes, une direction ordinale et une amplitude presentee comme positive
# (« increase by ___ % » / « decrease by ___ % »). Le preenregistrement en a deduit qu'il
# fallait reconstruire le signe. VERIFICATION FAITE SUR LES DONNEES : la colonne part2 du
# fichier public est DEJA SIGNEE. Pour une direction 1, toutes les valeurs sont positives
# ou nulles ; pour une direction 3 ou 2, de 85 a 99 pour cent des valeurs sont strictement
# negatives et le reste vaut exactement zero. Multiplier par moins un aurait retourne les
# valeurs et rendu toute la mesure fausse. La colonne est donc prise telle quelle, et
# l'accord entre la direction declaree et le signe observe est publie comme controle.

SIGNEES = {
    "revenu":       ("Q25v2", "Q25v2part2", 1, 3),
    "depense":      ("Q26v2", "Q26v2part2", 1, 3),
    "logement":     ("Q31v2", "Q31v2part2", 1, 3),
    "infl1_point":  ("Q8v2", "Q8v2part2", 1, 2),
    "revenus_trav": ("Q23v2", "Q23v2part2", 1, 3),
}

DIRECTES = {
    "infl1": "Q9_mean",
    "infl3": "Q9c_mean",
    "perte_emploi": "Q13new",
    "chomage": "Q4new",
    "infl1_var": "Q9_var",
    "infl1_iqr": "Q9_iqr",
    "fin_avant": "Q1",
    "fin_apres": "Q2",
}

VAR_PRIMAIRES = ["infl1", "infl3", "revenu", "depense", "logement",
                 "perte_emploi", "chomage"]
VAR_SECONDAIRES = ["infl1_var", "infl1_iqr", "infl1_point", "fin_avant", "fin_apres"]
VAR_ORDINALES = ["fin_avant", "fin_apres"]
VAR_BORNEES = ["perte_emploi", "chomage"]   # 0 a 100 par construction, non winsorisees

LIBELLE = {
    "infl1": "inflation a un an, moyenne de la densite",
    "infl3": "inflation a trois ans, moyenne de la densite",
    "revenu": "croissance attendue du revenu du menage",
    "depense": "croissance attendue de la depense du menage",
    "logement": "variation attendue du prix du logement",
    "perte_emploi": "probabilite de perdre son emploi",
    "chomage": "probabilite que le chomage augmente",
    "infl1_var": "incertitude d'inflation, variance de la densite",
    "infl1_iqr": "incertitude d'inflation, ecart interquartile de la densite",
    "infl1_point": "prevision ponctuelle d'inflation a un an",
    "fin_avant": "situation financiere comparee a douze mois plus tot",
    "fin_apres": "situation financiere attendue dans douze mois",
    "revenus_trav": "croissance attendue des revenus du travail",
}

DEMOS = ["_AGE_CAT", "_EDU_CAT", "_HH_INC_CAT", "_REGION_CAT", "_NUM_CAT"]

# Les colonnes de la SCE qui portent du texte et non des nombres. La chaine vide y tient
# lieu de manquant. Les convertir en nombres les detruirait silencieusement.
TEXTE = set(DEMOS) | {"_STATE", "survey_date"}

COLONNES = (["date", "userid", "tenure", "weight", "survey_date"]
            + DEMOS
            + sorted({c for c in DIRECTES.values()}
                     | {a for a, b, _, _ in SIGNEES.values()}
                     | {b for a, b, _, _ in SIGNEES.values()}
                     | {"Q11", "Q12new", "Q33", "Q36", "Q47", "_STATE"}))


# ---------------------------------------------------------------------------
# 2. Lecture des fichiers Excel et cache
# ---------------------------------------------------------------------------

def _lire_xlsx(chemin, colonnes):
    """Lit une feuille SCE et retourne un DataFrame des seules colonnes demandees.

    openpyxl en mode lecture seule, ligne a ligne : les fichiers font jusqu'a 75 Mo et une
    lecture complete en memoire par pandas coute plusieurs gigaoctets.

    Ligne 1 = mention de source imposee par la licence FRBNY. Ligne 2 = entete.
    Donnees a partir de la ligne 3. Le fichier 20-24 contient des lignes vides en fin de
    feuille, sans date ni userid ; elles sont ecartees ici, ce qui reproduit le compte de
    PROVENANCE.md.
    """
    import openpyxl
    wb = openpyxl.load_workbook(chemin, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    it = ws.iter_rows(values_only=True)
    next(it)                       # mention de source
    entete = list(next(it))
    idx = {nom: k for k, nom in enumerate(entete) if nom is not None}
    garde = [c for c in colonnes if c in idx]
    positions = [idx[c] for c in garde]
    i_date, i_user = idx["date"], idx["userid"]
    lignes = []
    for r in it:
        if r[i_date] is None or r[i_user] is None:
            continue           # ligne vide de fin de feuille
        lignes.append([r[p] for p in positions])
    wb.close()
    df = pd.DataFrame(lignes, columns=garde)
    for c in garde:
        if c in TEXTE:
            df[c] = df[c].astype(str).str.strip().replace({"": None, "None": None,
                                                           "nan": None, "NaT": None})
        else:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    df["_manquantes"] = ",".join(sorted(set(colonnes) - set(garde)))
    return df


def charger(cles=PRIMAIRE, forcer=False):
    """Les fichiers demandes, concatenes, avec les variables construites et les cohortes.

    Le resultat est mis en cache en parquet hors du depot ; la reconstruction est
    deterministe et ne depend d'aucune graine.
    """
    os.makedirs(CACHE, exist_ok=True)
    morceaux = []
    for cle in cles:
        chemin_cache = os.path.join(CACHE, f"sce-{cle}.parquet")
        if os.path.exists(chemin_cache) and not forcer:
            d = pd.read_parquet(chemin_cache)
        else:
            print(f"lecture de {FICHIERS[cle]} ...", flush=True)
            d = _lire_xlsx(os.path.join(DONNEES, FICHIERS[cle]), COLONNES)
            d.to_parquet(chemin_cache, index=False)
            print(f"  {len(d)} lignes, cache {chemin_cache}", flush=True)
        d["fichier"] = cle
        morceaux.append(d)
    df = pd.concat(morceaux, ignore_index=True, sort=False)
    return construire(df)


def construire(df):
    """Ajoute les variables declarees, le mois en entier ordinal et les cohortes."""
    df = df.copy()
    df["date"] = df["date"].astype(int)
    df["annee"] = df["date"] // 100
    df["mois_annee"] = df["date"] % 100
    # index de mois continu, 0 = janvier 2013, pour les decalages temporels
    df["t"] = (df["annee"] - 2013) * 12 + (df["mois_annee"] - 1)

    for cle, col in DIRECTES.items():
        df[cle] = pd.to_numeric(df[col], errors="coerce") if col in df.columns else np.nan

    for cle, (c_dir, c_amp, pos, neg) in SIGNEES.items():
        if c_dir in df.columns and c_amp in df.columns:
            a = pd.to_numeric(df[c_amp], errors="coerce")
            df[cle] = a.to_numpy(dtype=float)   # deja signee, cf. commentaire ci dessus
        else:
            df[cle] = np.nan

    df["cohorte"] = cohorte(df)
    df["cohorte_code"] = pd.factorize(df["cohorte"])[0].astype(np.int32)
    return df


# ---------------------------------------------------------------------------
# 3. Les cohortes, preenregistrement section 3
# ---------------------------------------------------------------------------

def _cat(s):
    """Une categorie de la SCE en chaine, avec une cellule NR tenue a part et jamais fusionnee.

    Les variables `_*_CAT` de la SCE sont du texte, 'Over 60', 'High School', '50k to 100k'.
    La chaine vide y tient lieu de manquant.
    """
    v = pd.Series(s).astype(object).where(pd.notna(pd.Series(s)), "NR")
    v = v.map(lambda x: str(x).strip())
    return np.where(v.isin(["", "None", "nan", "NaT", "<NA>", "NR"]), "NR", v)


def cohorte(df, variables=("_AGE_CAT", "_EDU_CAT", "_HH_INC_CAT")):
    """Cohorte primaire age x diplome x revenu. Toute cellule manquante donne 'NR'."""
    parts = []
    for v in variables:
        parts.append(_cat(df[v]) if v in df.columns else np.array(["NR"] * len(df)))
    return pd.Series(["|".join(p) for p in zip(*parts)], index=df.index)


# ---------------------------------------------------------------------------
# 4. Winsorisation, preenregistrement section 2.3
# ---------------------------------------------------------------------------

def bornes_winsor(df, variables, centiles=WINSOR):
    """Bornes globales par variable, calculees une fois sur tout le perimetre.

    Les variables bornees par construction, les probabilites de 0 a 100, ne sont pas
    winsorisees : leur borne est leur domaine.
    """
    out = {}
    for v in variables:
        x = pd.to_numeric(df[v], errors="coerce").to_numpy(dtype=float)
        x = x[np.isfinite(x)]
        if v in VAR_BORNEES or len(x) == 0:
            out[v] = (0.0, 100.0) if v in VAR_BORNEES else (np.nan, np.nan)
        else:
            out[v] = (float(np.percentile(x, centiles[0])),
                      float(np.percentile(x, centiles[1])))
    return out


def winsoriser(x, bornes):
    b, h = bornes
    if not np.isfinite(b) or not np.isfinite(h):
        return np.asarray(x, dtype=float)
    return np.clip(np.asarray(x, dtype=float), b, h)


# ---------------------------------------------------------------------------
# 5. Dispersion et decomposition inter / intra cohorte
# ---------------------------------------------------------------------------

def decomposition(x, g, n_min=N_MIN_COHORTE):
    """Decompose la dispersion d'une variable continue en inter et intra cohorte.

    x : valeurs, g : code entier de cohorte. Les cellules de moins de n_min menages sont
    regroupees dans une cohorte residuelle unique plutot que jetees : les jeter biaiserait
    la part inter vers le haut en ne gardant que les grosses cohortes.

    intra  = somme_g (n_g - 1) s_g^2 / (N - G), variance intra ponderee sans biais.
    inter  = variance ponderee des moyennes de cohorte, MOINS le terme que
             l'echantillonnage fini ajoute mecaniquement, somme_g w_g (1 - w_g) s_g^2 / n_g.
             C'est la correction de biais ; elle peut rendre la part inter negative, auquel
             cas elle est publiee negative et lue comme nulle.

    Retourne aussi la version brute, non corrigee, pour que l'ampleur de la correction soit
    visible.
    """
    x = np.asarray(x, dtype=float)
    g = np.asarray(g)
    ok = np.isfinite(x)
    x, g = x[ok], g[ok]
    n = len(x)
    if n < 3:
        return {"n": n, "n_cohortes": 0, "total": np.nan, "intra": np.nan,
                "inter": np.nan, "inter_brut": np.nan, "part_inter": np.nan}
    cles, inv = np.unique(g, return_inverse=True)
    eff = np.bincount(inv, minlength=len(cles))
    petites = eff < n_min
    if petites.any():
        # cohorte residuelle unique, code -1
        gg = np.where(petites[inv], -1, inv)
        cles, inv = np.unique(gg, return_inverse=True)
        eff = np.bincount(inv, minlength=len(cles))
    utiles = eff >= 2
    if utiles.sum() < 2:
        tot = float(np.var(x, ddof=1))
        return {"n": n, "n_cohortes": int(len(cles)), "total": tot, "intra": tot,
                "inter": 0.0, "inter_brut": 0.0, "part_inter": 0.0}
    sommes = np.bincount(inv, weights=x, minlength=len(cles))
    moyennes = sommes / eff
    carres = np.bincount(inv, weights=(x - moyennes[inv]) ** 2, minlength=len(cles))
    with np.errstate(invalid="ignore", divide="ignore"):
        var_g = np.where(eff > 1, carres / np.maximum(eff - 1, 1), np.nan)
    G = int(utiles.sum())
    intra = float(np.nansum(carres[utiles]) / max(n - G, 1))
    w = eff / n
    m_gen = float(np.sum(w * moyennes))
    inter_brut = float(np.sum(w * (moyennes - m_gen) ** 2))
    biais = float(np.nansum(w[utiles] * (1 - w[utiles]) * var_g[utiles] / eff[utiles]))
    inter = inter_brut - biais
    denom = inter + intra
    return {"n": n, "n_cohortes": G, "total": float(np.var(x, ddof=1)),
            "intra": intra, "inter": inter, "inter_brut": inter_brut,
            "part_inter": float(inter / denom) if denom > 0 else np.nan}


def robustes(x, g, n_min=N_MIN_COHORTE):
    """Version robuste : ecart interquartile total, mediane des IQR intra, IQR des medianes.

    Aucune decomposition additive n'est revendiquee, les trois nombres sont publies tels
    quels, comme le preenregistrement le declare.
    """
    x = np.asarray(x, dtype=float)
    g = np.asarray(g)
    ok = np.isfinite(x)
    x, g = x[ok], g[ok]
    if len(x) < 3:
        return {"iqr_total": np.nan, "iqr_intra_median": np.nan,
                "iqr_medianes": np.nan, "mad_total": np.nan}
    q75, q25 = np.percentile(x, [75, 25])
    med = float(np.median(x))
    cles, inv = np.unique(g, return_inverse=True)
    eff = np.bincount(inv, minlength=len(cles))
    iqrs, medianes = [], []
    for k in range(len(cles)):
        if eff[k] < max(n_min, 4):
            continue
        xi = x[inv == k]
        a, b = np.percentile(xi, [75, 25])
        iqrs.append(a - b)
        medianes.append(float(np.median(xi)))
    return {
        "iqr_total": float(q75 - q25),
        "iqr_intra_median": float(np.median(iqrs)) if iqrs else np.nan,
        "iqr_medianes": float(np.percentile(medianes, 75) - np.percentile(medianes, 25))
        if len(medianes) >= 4 else np.nan,
        "mad_total": float(np.median(np.abs(x - med))),
    }


# ---------------------------------------------------------------------------
# 6. Outils repris tels quels
# ---------------------------------------------------------------------------

def permuter_intra(codes, rng):
    """Permutation des menages a l'interieur de la cohorte, fonction de a44 reutilisee."""
    return C44.permuter_intra(len(codes), np.asarray(codes), rng)


def preparer_groupes(codes):
    """Les indices de chaque groupe de permutation, calcules une seule fois.

    a44_commun.permuter_intra balaie tout le vecteur pour chaque groupe, ce qui coute le
    produit du nombre de groupes par la taille du vecteur. Ici les groupes sont (mois,
    cohorte) et il y en a plusieurs milliers, ce qui rendait chaque permutation cent fois
    plus chere que le calcul qu'elle sert. Les groupes sont donc extraits une fois par tri
    stable ; l'ORDRE des groupes et l'ORDRE des indices a l'interieur d'un groupe sont
    identiques a ceux de a44, ce qui garantit que la permutation tiree est exactement la
    meme a graine egale. Le controle C6 le verifie.
    """
    codes = np.asarray(codes)
    ordre = np.argsort(codes, kind="mergesort")
    s = codes[ordre]
    coupures = np.flatnonzero(np.r_[True, s[1:] != s[:-1], True])
    return [ordre[a:b] for a, b in zip(coupures[:-1], coupures[1:]) if b - a > 1]


def permuter_prepare(n, groupes, rng):
    """La permutation de a44, avec les groupes deja extraits. Meme tirage a graine egale."""
    perm = np.arange(n)
    for lignes in groupes:
        perm[lignes] = rng.permutation(lignes)
    return perm


def controle_permutation(codes, graine=GRAINE):
    """Controle C6 : les deux implementations donnent la meme permutation, a graine egale."""
    a = C44.permuter_intra(len(codes), np.asarray(codes),
                           np.random.default_rng(graine))
    b = permuter_prepare(len(codes), preparer_groupes(codes),
                         np.random.default_rng(graine))
    return bool(np.array_equal(a, b))


def auc(y, score):
    """AUC de Mann-Whitney, fonction de i1 reutilisee sans retouche."""
    return I1.auc(y, score)


def holm(p):
    return C44.holm(p)


def benjamini_hochberg(p):
    return C44.benjamini_hochberg(p)


def rangs(x):
    """Rangs moyens des ex aequo, vectorises. Equivalent de scipy.stats.rankdata.

    Ecrit ici et non importe a chaque appel : la permutation et le bootstrap appellent
    cette fonction des centaines de milliers de fois, et l'import repete de scipy coutait
    plus que le calcul.
    """
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n == 0:
        return x
    ordre = np.argsort(x, kind="mergesort")
    xs = x[ordre]
    debut = np.empty(n, dtype=bool)
    debut[0] = True
    np.not_equal(xs[1:], xs[:-1], out=debut[1:])
    groupe = np.cumsum(debut) - 1
    debuts = np.flatnonzero(debut)
    fins = np.append(debuts[1:], n)
    moyen = (debuts + fins + 1) / 2.0
    r = np.empty(n, dtype=float)
    r[ordre] = moyen[groupe]
    return r


def spearman(a, b):
    """Correlation de Spearman, NaN si l'un des deux vecteurs est constant."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    ok = np.isfinite(a) & np.isfinite(b)
    if ok.sum() < 10:
        return np.nan
    ra, rb = rangs(a[ok]), rangs(b[ok])
    if ra.std() == 0 or rb.std() == 0:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def p_normal(observe, tirages):
    """p bilateral par approximation normale de la loi de permutation.

    Lecon E4 de i1 : avec 200 permutations le p empirique est plancher a 1/201 et aucune
    correction de Holm sur une grande famille ne peut retenir quoi que ce soit.
    L'approximation normale de la loi de permutation redonne la resolution ; les deux p
    sont publies cote a cote.
    """
    from scipy.stats import norm
    t = np.asarray([v for v in tirages if np.isfinite(v)], dtype=float)
    if len(t) < 5 or not np.isfinite(observe):
        return np.nan
    s = t.std(ddof=1)
    if s <= 0:
        return 1.0 if abs(observe - t.mean()) < 1e-12 else 0.0
    return float(2 * norm.sf(abs(observe - t.mean()) / s))


def p_empirique(observe, tirages):
    t = np.asarray([v for v in tirages if np.isfinite(v)], dtype=float)
    if len(t) == 0 or not np.isfinite(observe):
        return np.nan
    return float((np.sum(np.abs(t - t.mean()) >= abs(observe - t.mean())) + 1) / (len(t) + 1))


def ic(tirages):
    t = np.asarray([v for v in tirages if np.isfinite(v)], dtype=float)
    if len(t) == 0:
        return np.nan, np.nan
    return float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def ecrire(lignes, nom):
    chemin = os.path.join(SORTIE, nom)
    df = lignes if isinstance(lignes, pd.DataFrame) else pd.DataFrame(lignes)
    df.to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(df)} lignes", flush=True)
    return chemin


def nom_mois(t):
    """Index de mois continu -> 'AAAA-MM'."""
    a, m = 2013 + t // 12, t % 12 + 1
    return f"{a:04d}-{m:02d}"
