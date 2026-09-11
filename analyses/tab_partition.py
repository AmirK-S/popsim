"""
tab_partition : la partition des 108 items de vague 4 de Twin-2K-500 en trois blocs B,
pour le tournoi A vers B (preenregistrement resultats/tab-preenregistrement.md).

===========================================================================
CE QUE CE SCRIPT LIT : les SEULES metadonnees d'items.
  data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json
  data/twin2k500/llm/wave4_formatted_to_catalog_mapping.json
Il ne lit AUCUNE reponse, humaine ou simulee, aucun masque, aucun fichier de resultats.
Il n'ecrit rien sous data/.

CE QU'IL ECRIT : resultats/tab-partition-items.csv (ou --sortie), une ligne par item,
puis affiche le SHA-256 du fichier ecrit.

LA PARTITION, regles dans cet ordre :
  1. Groupement, contrainte dure. Une unite indivisible est :
     - une experience inter sujets entiere, tous ses bras ensemble (table EXPERIENCES) ;
     - un QID matrice entier, toutes ses lignes ensemble ;
     - un lien de contenu declare (table LIENS_CONTENU) : QID288 et QID289 notent les
       quatre memes objets, en benefice puis en risque. Le script verifie au catalogue que
       leurs lignes sont identiques, et ECHOUE si deux QID des 108 ont des lignes
       identiques sans etre dans la meme unite ;
     - sinon, le QID a choix multiple seul.
  2. Tailles des trois blocs aussi egales que possible (somme des (3 t_b - 108)^2).
  3. Type : lignes de matrice par bloc (somme des (3 m_b - 40)^2).
  4. Famille d'analyse, sur les seules familles divisibles, c'est a dire portees par plus
     d'une unite (les familles indivisibles ont un ecart constant quelle que soit la
     partition) : somme sur f et b des (3 c_fb - n_f)^2.
  5. Plan : items inter sujets par bloc (somme des (3 p_b - 48)^2). Ce critere n'est pas
     dans l'arbitrage de l'orchestrateur ; il n'intervient qu'a egalite des trois
     precedents et sert la couverture des blocs.
  6. Nombre d'unites par bloc (somme des (3 u_b - U)^2), pour le bootstrap par unites.
  7. Egalites restantes : graine fixe GRAINE.

RECHERCHE EXHAUSTIVE. Les unites sont rangees en classes interchangeables pour les
criteres 2 a 6 : meme nombre d'items, de lignes de matrice, d'items inter sujets, et meme
famille si la famille est divisible. On enumere TOUTES les repartitions des effectifs de
chaque classe entre les trois blocs, on garde l'optimum lexicographique, on le rend
canonique (ordre des blocs sans signification), on departage a la graine s'il reste
plusieurs optimums, puis on tire a la graine quels membres d'une classe vont dans quel
bloc. Les blocs sont enfin numerotes dans l'ordre d'apparition de leur premier item dans
le mapping.

Usage : .venv/bin/python analyses/tab_partition.py [--sortie CHEMIN]
Aucun appel reseau, aucun modele.
===========================================================================
"""

import argparse
import csv
import hashlib
import io
import itertools
import json
import os
import sys

import numpy as np

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")
CATALOGUE = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv",
                         "question_catalog.json")
MAPPING = os.path.join(RACINE_TWIN, "llm", "wave4_formatted_to_catalog_mapping.json")
SORTIE = os.path.join(RACINE, "resultats", "tab-partition-items.csv")

GRAINE = 20260911
N_BLOCS = 3
N_ITEMS_ATTENDU = 108
N_QID_ATTENDU = 75

# Les onze experiences inter sujets. Source : audit
# resultats/twin-ab-audit-provenance-2026-09-11.md section 3.1, ou les bras ont ete
# etablis sur la structure des masques humains (bras mutuellement exclusifs, union a
# 100 pour cent). Ici la table est une constante de metadonnees ; le libelle de bloc
# attendu au catalogue est verifie pour chaque QID, et test_tab_partition.py reverifie
# l'exclusivite des bras sur le seul statut vide ou renseigne des cellules.
EXPERIENCES = [
    ("Disease", [("loss", [("QID158", "Disease-loss")]),
                 ("gain", [("QID157", "Disease - gain")])]),
    ("Linda", [("conjunction", [("QID160", "Linda-conjunction")]),
               ("no conjunction", [("QID159", "Linda -no conjunction")])]),
    ("Outcome bias", [("failure", [("QID162", "Outcome bias - failure")]),
                      ("success", [("QID161", "Outcome bias - success")])]),
    ("Anchoring African", [("low", [("QID163", "Anchoring - African countries low")]),
                           ("high", [("QID165", "Anchoring - African countries high")])]),
    ("Anchoring redwood", [("low", [("QID167", "Anchoring - redwood low")]),
                           ("high", [("QID169", "Anchoring - redwood high")])]),
    ("Less is More + Proportion dominance", [
        ("A", [("QID171", "Less is More Gamble A"), ("QID174", "Proportion dominance 1A"),
               ("QID177", "Proportion dominance 2A")]),
        ("B", [("QID172", "Less is More Gamble B"), ("QID175", "Proportion dominance 1B"),
               ("QID178", "Proportion dominance 2B")]),
        ("C", [("QID173", "Less is More Gamble C"), ("QID176", "Proportion dominance 1C"),
               ("QID179", "Proportion dominance 2C")])]),
    ("Absolute vs. relative", [
        ("calculator", [("QID183", "Absolute vs. relative - calculator")]),
        ("jacket", [("QID184", "Absolute vs. relative - jacket")])]),
    ("WTA/WTP Thaler", [
        ("WTP certainty", [("QID189", "WTA/WTP Thaler problem - WTP certainty")]),
        ("WTA certainty", [("QID190", "WTA/WTP Thaler problem - WTA certainty")]),
        ("WTP noncertainty", [("QID191", "WTA/WTP Thaler - WTP noncertainty")])]),
    ("Allais", [("Form 1", [("QID192", "Allais Form 1")]),
                ("Form 2", [("QID193", "Allais Form 2")])]),
    ("Myside", [("Ford", [("QID194", "Myside Ford")]),
                ("German", [("QID195", "Myside German")])]),
    ("Probability matching", [
        ("Problem 1", [("QID198", "Probability matching vs. maximizing - Problem 1")]),
        ("Problem 2", [("QID203", "Probability matching vs. maximizing - Problem 2")])]),
]

# Liens de contenu hors experiences et hors matrices : QID distincts qui portent le meme
# contenu. Verifie au catalogue (lignes identiques).
LIENS_CONTENU = [
    ("Nonseparability benefice et risque", ["QID288", "QID289"]),
]

COLONNES_CSV = ["item", "colonne_catalogue", "qid_parent", "type", "selecteur",
                "n_modalites", "famille", "famille_analyse", "experience", "bras", "plan",
                "unite", "bloc_B"]


class ErreurPartition(Exception):
    """Une contrainte de groupement ou de structure est violee."""


# ---------------------------------------------------------------------------
# 1. Metadonnees
# ---------------------------------------------------------------------------

def sha256_fichier(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as f:
        for bloc in iter(lambda: f.read(1 << 16), b""):
            h.update(bloc)
    return h.hexdigest()


def charger_items(catalogue=CATALOGUE, mapping=MAPPING):
    """Les 108 items categoriels de vague 4, dans l'ordre du mapping (celui de a6 et t1),
    avec leurs seules metadonnees."""
    with open(catalogue, encoding="utf-8") as f:
        cat = {q["QuestionID"]: q for q in json.load(f)}
    with open(mapping, encoding="utf-8") as f:
        mp = json.load(f)
    exp_de, bras_de, bloc_attendu = {}, {}, {}
    for nom, bras in EXPERIENCES:
        if len(bras) < 2:
            raise ErreurPartition(f"experience {nom} : moins de deux bras")
        for b, qids in bras:
            for qid, libelle in qids:
                if qid in exp_de:
                    raise ErreurPartition(f"{qid} figure dans deux experiences")
                exp_de[qid], bras_de[qid], bloc_attendu[qid] = nom, b, libelle
    items = []
    for e in mp:
        q = cat.get(e["QuestionID"])
        if q is None:
            raise ErreurPartition(f"{e['QuestionID']} absent du catalogue")
        if q["QuestionType"] not in ("MC", "Matrix"):
            continue
        qid = e["QuestionID"]
        famille = q["BlockName"].strip()
        if qid in bloc_attendu and famille != bloc_attendu[qid]:
            raise ErreurPartition(f"{qid} : bloc {famille!r} au catalogue, "
                                  f"{bloc_attendu[qid]!r} attendu")
        n_mod = len(q.get("Columns") or []) if q["QuestionType"] == "Matrix" \
            else len(q.get("Options") or [])
        items.append({
            "item": e["formatted_column"], "colonne_catalogue": e["catalog_csv_column"],
            "qid_parent": qid,
            "type": "ligne_matrice" if q["QuestionType"] == "Matrix" else "MC",
            "selecteur": q.get("Settings", {}).get("Selector", ""),
            "n_modalites": n_mod, "famille": famille,
            "famille_analyse": exp_de.get(qid, famille),
            "experience": exp_de.get(qid, ""), "bras": bras_de.get(qid, ""),
            "plan": "inter_sujets" if qid in exp_de else "intra_sujets",
            "_lignes": tuple(q.get("Rows") or ()),
        })
    if len(items) != N_ITEMS_ATTENDU:
        raise ErreurPartition(f"{len(items)} items categoriels, {N_ITEMS_ATTENDU} attendus")
    if len({it["item"] for it in items}) != len(items):
        raise ErreurPartition("noms d'items dupliques")
    qids = {it["qid_parent"] for it in items}
    if len(qids) != N_QID_ATTENDU:
        raise ErreurPartition(f"{len(qids)} QID, {N_QID_ATTENDU} attendus")
    manquants = set(exp_de) - qids
    if manquants:
        raise ErreurPartition(f"QID d'experience hors des 108 : {sorted(manquants)}")
    return items


def construire_unites(items):
    """Chaque item recoit une unite indivisible. Renvoie la liste des unites, dans
    l'ordre d'apparition de leur premier item."""
    parent = {}                                  # QID -> cle d'unite
    for nom, bras in EXPERIENCES:
        for _, qids in bras:
            for qid, _ in qids:
                parent[qid] = ("experience", nom)
    for nom, qids in LIENS_CONTENU:
        lignes = set()
        for qid in qids:
            if qid in parent:
                raise ErreurPartition(f"{qid} est a la fois dans une experience et dans "
                                      f"le lien {nom}")
            parent[qid] = ("lien", nom)
            lignes.add(next(it["_lignes"] for it in items if it["qid_parent"] == qid))
        if len(lignes) != 1 or not next(iter(lignes)):
            raise ErreurPartition(f"lien {nom} : lignes differentes au catalogue, le lien "
                                  "n'est pas justifie")
    for it in items:
        parent.setdefault(it["qid_parent"], ("qid", it["qid_parent"]))

    # Garde-fou : deux QID de lignes identiques doivent partager une unite.
    par_lignes = {}
    for it in items:
        if it["_lignes"]:
            par_lignes.setdefault(it["_lignes"], set()).add(it["qid_parent"])
    for groupe in par_lignes.values():
        if len({parent[q] for q in groupe}) > 1:
            raise ErreurPartition(f"QID de contenu identique dans des unites differentes : "
                                  f"{sorted(groupe)}")

    ordre, unites = {}, []
    for j, it in enumerate(items):
        cle = parent[it["qid_parent"]]
        if cle not in ordre:
            ordre[cle] = len(unites)
            unites.append({"cle": cle, "items": []})
        unites[ordre[cle]]["items"].append(j)
        it["_unite"] = ordre[cle]
    for k, u in enumerate(unites):
        u["id"] = f"U{k + 1:02d}"
        its = [items[j] for j in u["items"]]
        u["n"] = len(its)
        u["n_mx"] = sum(it["type"] == "ligne_matrice" for it in its)
        u["n_part"] = sum(it["plan"] == "inter_sujets" for it in its)
        fams = {it["famille_analyse"] for it in its}
        if len(fams) != 1:
            raise ErreurPartition(f"unite {u['cle']} a cheval sur plusieurs familles "
                                  f"d'analyse : {sorted(fams)}")
        u["famille"] = fams.pop()
    return unites


# ---------------------------------------------------------------------------
# 2. Recherche exhaustive
# ---------------------------------------------------------------------------

def _compositions(m, k=N_BLOCS):
    out = [c for c in itertools.product(range(m + 1), repeat=k) if sum(c) == m]
    return np.array(out, dtype=np.int64)


def classes_interchangeables(unites):
    unites_par_fam = {}
    for u in unites:
        unites_par_fam.setdefault(u["famille"], []).append(u)
    divisibles = sorted(f for f, us in unites_par_fam.items() if len(us) > 1)
    classes = {}
    for k, u in enumerate(unites):
        sig = (u["n"], u["n_mx"], u["n_part"],
               u["famille"] if u["famille"] in divisibles else None)
        classes.setdefault(sig, []).append(k)
    liste = sorted(classes.items(), key=lambda kv: kv[1][0])
    return [{"sig": s, "membres": m} for s, m in liste], divisibles


def _cles(total, n_mx, n_part, n_u, fam, n_fam):
    """Les cinq criteres, en entiers, pour des agregats par bloc (..., 3)."""
    t, mx, pt = total.sum(-1)[..., None], n_mx.sum(-1)[..., None], n_part.sum(-1)[..., None]
    u = n_u.sum(-1)[..., None]
    k1 = ((3 * total - t) ** 2).sum(-1)
    k2 = ((3 * n_mx - mx) ** 2).sum(-1)
    k3 = np.zeros_like(k1)
    for f, nf in n_fam.items():
        k3 = k3 + ((3 * fam[f] - nf) ** 2).sum(-1)
    k4 = ((3 * n_part - pt) ** 2).sum(-1)
    k5 = ((3 * n_u - u) ** 2).sum(-1)
    return np.stack([k1, k2, k3, k4, k5], axis=-1)


def rechercher(unites):
    """Toutes les repartitions d'effectifs par classe ; renvoie les optimums
    lexicographiques canoniques, le vecteur de criteres optimal et le nombre de
    repartitions examinees."""
    classes, divisibles = classes_interchangeables(unites)
    comps = [_compositions(len(c["membres"])) for c in classes]
    externe = int(np.argmax([len(c) for c in comps]))
    internes = [i for i in range(len(classes)) if i != externe]
    n_fam = {f: sum(u["n"] for u in unites if u["famille"] == f) for f in divisibles}

    # Produit cartesien des classes internes : effectifs (N, n_internes, 3).
    idx = np.array(list(itertools.product(*[range(len(comps[i])) for i in internes])),
                   dtype=np.int64)
    cnt = np.stack([comps[i][idx[:, a]] for a, i in enumerate(internes)], axis=1)

    def agreger(cnt_cl, cls):
        s = {"n": 0, "mx": 0, "pt": 0, "u": 0}
        fam = {f: 0 for f in divisibles}
        for a, i in enumerate(cls):
            n, mx, pt, f = classes[i]["sig"]
            c = cnt_cl[..., a, :]
            s["n"] = s["n"] + c * n
            s["mx"] = s["mx"] + c * mx
            s["pt"] = s["pt"] + c * pt
            s["u"] = s["u"] + c
            if f is not None:
                fam[f] = fam[f] + c * n
        return s, fam

    s_in, fam_in = agreger(cnt, internes)
    meilleur, optimums, n_examinees = None, [], 0
    for o, comp_ext in enumerate(comps[externe]):
        s_ex, fam_ex = agreger(comp_ext[None, None, :], [externe])
        cles = _cles(s_in["n"] + s_ex["n"], s_in["mx"] + s_ex["mx"],
                     s_in["pt"] + s_ex["pt"], s_in["u"] + s_ex["u"],
                     {f: fam_in[f] + fam_ex[f] for f in divisibles}, n_fam)
        n_examinees += len(cles)
        garde = np.arange(len(cles))
        for k in range(cles.shape[1]):
            v = cles[garde, k]
            garde = garde[v == v.min()]
        tuple_min = tuple(int(x) for x in cles[garde[0]])
        if meilleur is None or tuple_min < meilleur:
            meilleur, optimums = tuple_min, []
        if tuple_min == meilleur:
            for g in garde:
                mat = np.zeros((len(classes), N_BLOCS), dtype=np.int64)
                mat[internes] = cnt[g]
                mat[externe] = comp_ext
                optimums.append(mat)

    canon = set()
    for mat in optimums:
        colonnes = sorted((tuple(mat[:, b]) for b in range(N_BLOCS)), reverse=True)
        canon.add(tuple(colonnes))
    canon = sorted(canon)
    return classes, canon, meilleur, n_examinees


def partitionner(items, unites, graine=GRAINE):
    classes, canon, meilleur, n_examinees = rechercher(unites)
    rng = np.random.default_rng(graine)
    choix = int(rng.integers(len(canon))) if len(canon) > 1 else 0
    colonnes = canon[choix]
    bloc_unite = np.full(len(unites), -1, dtype=int)
    for c, cl in enumerate(classes):
        membres = sorted(cl["membres"])
        perm = [membres[i] for i in rng.permutation(len(membres))]
        pos = 0
        for b in range(N_BLOCS):
            for u in perm[pos:pos + colonnes[b][c]]:
                bloc_unite[u] = b
            pos += colonnes[b][c]
    if (bloc_unite < 0).any():
        raise ErreurPartition("une unite n'a pas recu de bloc")
    # Numerotation canonique : ordre d'apparition du premier item dans le mapping.
    renum = {}
    for it in items:
        b = bloc_unite[it["_unite"]]
        if b not in renum:
            renum[b] = len(renum) + 1
    for it in items:
        it["unite"] = unites[it["_unite"]]["id"]
        it["bloc_B"] = renum[bloc_unite[it["_unite"]]]
    return {"criteres": meilleur, "n_optimums_canoniques": len(canon),
            "indice_optimum_retenu": choix, "n_repartitions": n_examinees,
            "n_classes": len(classes), "n_unites": len(unites)}


# ---------------------------------------------------------------------------
# 3. Verification, ecriture
# ---------------------------------------------------------------------------

def verifier(lignes):
    """Echoue proprement si la partition ecrite viole une contrainte."""
    if len(lignes) != N_ITEMS_ATTENDU:
        raise ErreurPartition(f"{len(lignes)} lignes, {N_ITEMS_ATTENDU} attendues")
    if len({l["item"] for l in lignes}) != len(lignes):
        raise ErreurPartition("un item apparait deux fois")
    blocs = {int(l["bloc_B"]) for l in lignes}
    if blocs != set(range(1, N_BLOCS + 1)):
        raise ErreurPartition(f"blocs {sorted(blocs)}, attendus 1 a {N_BLOCS}")
    lien_de = {q: nom for nom, qids in LIENS_CONTENU for q in qids}
    for champ, libelle in (("qid_parent", "QID"), ("experience", "experience"),
                           ("unite", "unite"), ("_lien", "lien de contenu")):
        vus = {}
        for l in lignes:
            cle = lien_de.get(l["qid_parent"], "") if champ == "_lien" else l[champ]
            if not cle:
                continue
            vus.setdefault(cle, set()).add(int(l["bloc_B"]))
        coupes = {k: sorted(v) for k, v in vus.items() if len(v) > 1}
        if coupes:
            raise ErreurPartition(f"{libelle} coupe entre blocs : {coupes}")
    tailles = [sum(int(l["bloc_B"]) == b for l in lignes) for b in range(1, N_BLOCS + 1)]
    if max(tailles) - min(tailles) > 0 and N_ITEMS_ATTENDU % N_BLOCS == 0:
        # L'egalite exacte est atteignable avec les 42 unites d'un item ; un ecart
        # signalerait une recherche fausse.
        raise ErreurPartition(f"tailles {tailles} inegales")
    return tailles


def ecrire_csv(items, chemin):
    tampon = io.StringIO()
    w = csv.DictWriter(tampon, fieldnames=COLONNES_CSV, lineterminator="\n",
                       quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for it in items:
        w.writerow({k: it[k] for k in COLONNES_CSV})
    os.makedirs(os.path.dirname(os.path.abspath(chemin)), exist_ok=True)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        f.write(tampon.getvalue())
    return sha256_fichier(chemin)


def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def resume(items):
    lignes = []
    for b in range(1, N_BLOCS + 1):
        its = [it for it in items if it["bloc_B"] == b]
        fams = sorted({it["famille_analyse"] for it in its})
        lignes.append({
            "bloc": b, "items": len(its),
            "lignes_matrice": sum(it["type"] == "ligne_matrice" for it in its),
            "MC": sum(it["type"] == "MC" for it in its),
            "inter_sujets": sum(it["plan"] == "inter_sujets" for it in its),
            "unites": len({it["unite"] for it in its}),
            "familles_analyse": len(fams),
            "detail": {f: sum(it["famille_analyse"] == f for it in its) for f in fams}})
    return lignes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--sortie", default=SORTIE)
    ap.add_argument("--silencieux", action="store_true")
    args = ap.parse_args(argv)
    try:
        items = charger_items()
        unites = construire_unites(items)
        info = partitionner(items, unites)
        sha = ecrire_csv(items, args.sortie)
        verifier(lire_csv(args.sortie))
    except ErreurPartition as e:
        print(f"ECHEC de la partition : {e}", file=sys.stderr)
        return 2
    if not args.silencieux:
        print(f"catalogue  sha256 {sha256_fichier(CATALOGUE)}")
        print(f"mapping    sha256 {sha256_fichier(MAPPING)}")
        print(f"graine {GRAINE} ; {info['n_unites']} unites, {info['n_classes']} classes ; "
              f"{info['n_repartitions']} repartitions examinees ; criteres optimaux "
              f"{info['criteres']} ; {info['n_optimums_canoniques']} optimum(s) "
              f"canonique(s), indice retenu {info['indice_optimum_retenu']}")
        for r in resume(items):
            print(f"bloc B{r['bloc']} : {r['items']} items, {r['lignes_matrice']} lignes "
                  f"de matrice, {r['MC']} MC, {r['inter_sujets']} inter sujets, "
                  f"{r['unites']} unites, {r['familles_analyse']} familles d'analyse")
            for f, n in r["detail"].items():
                print(f"    {n:3d}  {f}")
        print(f"ecrit {args.sortie}")
    print(f"SHA-256 {sha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
