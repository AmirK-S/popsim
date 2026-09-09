"""
a28_test3_stereotype : test decisif de l'idee de rang 3, "le modele efface par le
stereotype et non par la moyenne".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a8_commun est importe tel quel pour la
definition des modalites minoritaires, celle de a8 section 6.

Le profil d'erreur, cellule par cellule. Pour chaque methode, chaque axe de segmentation
et chaque cellule (personne, item) :

  m_pop   : la modalite majoritaire de la POPULATION humaine sur cet item ;
  m_seg   : la modalite majoritaire du SEGMENT de la personne sur cet item.

Les deux sont calcules sur les humains de la vague 1, en laissant de cote la personne
elle meme : sans cette precaution, une personne contribuerait a la definition du
stereotype auquel on compare sa propre prediction, ce qui gonflerait mecaniquement la
part stereotype des methodes qui recopient bien.

Les cellules ou m_pop et m_seg coincident sont EXCLUES : elles ne separent rien, et elles
sont la majorite. Parmi les cellules restantes, on ne garde que les erreurs, c'est a dire
les cellules ou la prediction differe de la vraie reponse, et on les repartit :

  erreur vers la moyenne    : la prediction vaut m_pop ;
  erreur vers le stereotype : la prediction vaut m_seg ;
  erreur ailleurs           : ni l'un ni l'autre.

La quantite rapportee est la part stereotype parmi les deux premieres,
n_stereotype / (n_stereotype + n_moyenne), avec un intervalle bootstrap sur les personnes.

Prediction de la these : les baselines se trompent vers la moyenne, les agents a etiquette
se trompent vers le stereotype de leur segment, C3, qui ne recoit aucune etiquette, se
place entre les deux.

Avertissement porte dans le rapport et repete ici : deux methodes sont tautologiques sur
cette mesure. `B0 mode` predit m_pop par construction, sa part stereotype ne peut etre que
proche de zero. `B1 argmax` maximise la probabilite conditionnelle a l'etiquette, elle
predit tres souvent m_seg. Ces deux lignes sont des ancres de lecture, pas des resultats.
Les comparaisons informatives sont entre conditions a modele de langage, et entre elles et
B2, qui ne voit pas les demographies, et la foret, qui ne voit qu'elles.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
  H7  Pour chacune des huit conditions a modele de langage, la part stereotype est plus
      haute que celle de `B0 mode` sur le meme axe et le meme perimetre. Axe declare :
      l'ideologie politique, celui dont a1 et a23 etablissent qu'il porte l'effet.
      Perimetre 150. 8 tests, par bootstrap apparie sur les personnes.
  H8  La part stereotype de C3, condition sans aucune etiquette, est plus basse que celle
      de C2, meme modele et memes personnes avec etiquette demographique. 1 test.

  Famille declaree : H7 union H8, soit 9 tests. Correction principale : Holm.
  Correction secondaire : Benjamini Hochberg.
  N'entrent PAS dans la famille : les autres axes, le perimetre 1 052, et le rappel des
  cellules minoritaires, qui est une description reliee a la part minoritaire.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl.
Sortie  : resultats/a28-t3-profil-erreur.csv, a28-t3-minorites.csv.

Usage :
  .venv/bin/python analyses/a28_test3_stereotype.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 2000
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C

AXES_T3 = ["political_ideology", "gender", "age", "education", "profil croise"]
SEUILS_MINORITE = [0.10, 0.20]


def modes_laissant_de_cote(codes_h, seg, k):
    """m_pop et m_seg par cellule, calcules sans la personne concernee.

    codes_h : (n, m) codes de reponse des humains, -1 si vide.
    seg     : (n,) segment de chaque personne, -1 si inconnu.
    k       : (m,) nombre de modalites declarees de chaque item.
    Renvoie deux matrices (n, m) de codes, -1 quand la modalite n'est pas definie.
    En cas d'egalite, la modalite de plus petit rang dans la nomenclature l'emporte :
    la regle est deterministe et sans effet sur les comparaisons entre methodes, qui
    partagent la meme definition.
    """
    n, m = codes_h.shape
    m_pop = np.full((n, m), -1, dtype=np.int32)
    m_seg = np.full((n, m), -1, dtype=np.int32)
    g = int(seg.max()) + 1 if seg.max() >= 0 else 0
    for j in range(m):
        col = codes_h[:, j]
        kk = k[j]
        tot = np.zeros(kk)
        for v in col[col >= 0]:
            tot[v] += 1
        par_seg = np.zeros((max(g, 1), kk))
        for i in range(n):
            if col[i] >= 0 and seg[i] >= 0:
                par_seg[seg[i], col[i]] += 1
        for i in range(n):
            t = tot.copy()
            if col[i] >= 0:
                t[col[i]] -= 1
            if t.sum() > 0:
                m_pop[i, j] = int(np.argmax(t))
            if seg[i] >= 0:
                s = par_seg[seg[i]].copy()
                if col[i] >= 0:
                    s[col[i]] -= 1
                if s.sum() > 0:
                    m_seg[i, j] = int(np.argmax(s))
    return m_pop, m_seg


def profil(paquet, lignes, conditions, axe, tirages, rng):
    """Part stereotype par methode, avec intervalle bootstrap sur les personnes."""
    items, options = paquet["items"], paquet["options"]
    k = np.array([len(options[it]) for it in items])
    seg_tous, _ = C.segments(paquet["x"], paquet["attributs"])
    seg = seg_tous[axe][lignes]
    codes_h = C.coder(paquet["y1"], lignes, items, options)
    m_pop, m_seg = modes_laissant_de_cote(codes_h, seg, k)

    # Cellules qui separent : vraie reponse connue, les deux modes definis et differents.
    separe = (codes_h >= 0) & (m_pop >= 0) & (m_seg >= 0) & (m_pop != m_seg)
    n = len(lignes)
    idx_boot = rng.integers(0, n, (tirages, n))

    out, par_personne = [], {}
    for cond in conditions:
        codes = C.coder(paquet["M"][cond], lignes, items, options)
        dispo = separe & (codes >= 0)
        erreur = dispo & (codes != codes_h)
        vers_moyenne = erreur & (codes == m_pop)
        vers_stereo = erreur & (codes == m_seg)
        s = vers_stereo.sum(axis=1).astype(float)
        mo = vers_moyenne.sum(axis=1).astype(float)
        par_personne[cond] = (s, mo)
        den = s.sum() + mo.sum()
        part = s.sum() / den if den > 0 else np.nan
        tir = np.array([
            (s[i].sum() / (s[i].sum() + mo[i].sum()))
            if (s[i].sum() + mo[i].sum()) > 0 else np.nan for i in idx_boot])
        out.append({
            "axe": axe, "condition": cond,
            "cellules_separantes": int(dispo.sum()),
            "erreurs": int(erreur.sum()),
            "erreurs_vers_stereotype": int(vers_stereo.sum()),
            "erreurs_vers_moyenne": int(vers_moyenne.sum()),
            "erreurs_ailleurs": int((erreur & ~vers_stereo & ~vers_moyenne).sum()),
            "part_stereotype": float(part),
            "ic_bas": float(np.nanpercentile(tir, 2.5)),
            "ic_haut": float(np.nanpercentile(tir, 97.5)),
            "part_erreurs_expliquees": float((vers_stereo.sum() + vers_moyenne.sum())
                                             / erreur.sum()) if erreur.sum() else np.nan,
            "exactitude_sur_cellules_separantes": float(
                (dispo & (codes == codes_h)).sum() / dispo.sum()) if dispo.sum() else np.nan,
        })
    return pd.DataFrame(out), par_personne, idx_boot


def contraste_apparie(par_personne, a, b, idx_boot):
    """Difference de part stereotype entre deux methodes, memes personnes tirees."""
    sa, ma = par_personne[a]
    sb, mb = par_personne[b]

    def part(s, m, i):
        d = s[i].sum() + m[i].sum()
        return s[i].sum() / d if d > 0 else np.nan

    obs = (sa.sum() / (sa.sum() + ma.sum())) - (sb.sum() / (sb.sum() + mb.sum()))
    tir = np.array([part(sa, ma, i) - part(sb, mb, i) for i in idx_boot])
    tir = tir[~np.isnan(tir)]
    # p bilateral a partir de la position de zero dans la distribution bootstrap
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return (float(obs), float(np.percentile(tir, 2.5)),
            float(np.percentile(tir, 97.5)), float(min(max(p, 1.0 / len(tir)), 1.0)))


def minorites(paquet, lignes, conditions):
    """Rappel des cellules minoritaires, definition de a8 section 6, memes lignes."""
    from a8_commun import mesures_minorites, modalites_minoritaires
    items = paquet["items"]
    y = paquet["y1"][lignes][:, :len(items)]
    seuils = {s: modalites_minoritaires(y, s) for s in SEUILS_MINORITE}
    out = []
    for cond in conditions:
        p = paquet["M"][cond][lignes][:, :len(items)]
        for s, mods in seuils.items():
            r = mesures_minorites(p, y, mods)
            out.append({"condition": cond, "seuil": s, **r})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    paquet = C.charger_tout(args.cache, args.cache_foret)
    rng = np.random.default_rng(args.graine)
    print(__doc__.split("=" * 75)[1])

    toutes = [c for c in C.ORDRE_METHODES if c in paquet["M"]]
    perimetres = {"150": paquet["lignes150"],
                  "1052": np.arange(len(paquet["ids"]))}

    tables, contrastes = [], []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        for axe in AXES_T3:
            d, pp, idx = profil(paquet, lignes, conds, axe, args.tirages, rng)
            d["perimetre"] = nom_per
            tables.append(d)
            if axe == "political_ideology":
                for cond in conds:
                    if cond in ("B0 mode", "humains vague 2"):
                        continue
                    o, b, h, p = contraste_apparie(pp, cond, "B0 mode", idx)
                    contrastes.append({
                        "perimetre": nom_per, "axe": axe, "hypothese": "H7 contre B0 mode",
                        "condition": cond, "difference": o, "ic_bas": b, "ic_haut": h,
                        "p_bootstrap": p})
                if "C2" in conds and "C3" in conds:
                    o, b, h, p = contraste_apparie(pp, "C3", "C2", idx)
                    contrastes.append({
                        "perimetre": nom_per, "axe": axe, "hypothese": "H8 C3 contre C2",
                        "condition": "C3 moins C2", "difference": o, "ic_bas": b,
                        "ic_haut": h, "p_bootstrap": p})
        print(f"  perimetre {nom_per} : fait", flush=True)

    prof = pd.concat(tables, ignore_index=True)
    ct = pd.DataFrame(contrastes)

    # correction sur la famille declaree : perimetre 150, axe ideologie, huit conditions
    # a modele de langage pour H7, plus H8
    m = ((ct.perimetre == "150") & (ct.axe == "political_ideology")
         & ((ct.condition.isin(C.LLM)) | (ct.condition == "C3 moins C2")))
    idx = ct[m].index
    ct["p_holm"] = np.nan
    ct["p_bh"] = np.nan
    ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
    ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)

    prof = prof.merge(ct[ct.hypothese == "H7 contre B0 mode"][
        ["perimetre", "axe", "condition", "difference", "ic_bas", "ic_haut",
         "p_bootstrap", "p_holm", "p_bh"]].rename(columns={
            "difference": "h7_difference", "ic_bas": "h7_ic_bas",
            "ic_haut": "h7_ic_haut", "p_bootstrap": "h7_p", "p_holm": "h7_p_holm",
            "p_bh": "h7_p_bh"}),
        on=["perimetre", "axe", "condition"], how="left")
    C.ecrire(prof, "a28-t3-profil-erreur.csv")
    C.ecrire(ct, "a28-t3-contrastes.csv")

    # --------------------------------------------------------------- minorites
    mn = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        d = minorites(paquet, lignes, conds)
        d["perimetre"] = nom_per
        mn.append(d)
    minor = pd.concat(mn, ignore_index=True)
    C.ecrire(minor, "a28-t3-minorites.csv")

    # ------------------------------------------------------------------ affichage
    pd.set_option("display.width", 240)
    for nom_per in ["150", "1052"]:
        print("\n" + "=" * 126)
        print(f"Profil d'erreur, perimetre {nom_per}, axe ideologie politique")
        print("=" * 126)
        s = prof[(prof.perimetre == nom_per)
                 & (prof.axe == "political_ideology")].copy()
        s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
        print(s.sort_values("ordre")[
            ["condition", "cellules_separantes", "erreurs", "erreurs_vers_stereotype",
             "erreurs_vers_moyenne", "part_stereotype", "ic_bas", "ic_haut",
             "part_erreurs_expliquees", "h7_p_holm"]].to_string(index=False))

    print("\n" + "=" * 126)
    print("Part stereotype par axe, perimetre 150")
    print("=" * 126)
    piv = prof[prof.perimetre == "150"].pivot(
        index="condition", columns="axe", values="part_stereotype")
    print(piv.reindex([c for c in C.ORDRE_METHODES if c in piv.index]).round(4).to_string())

    print("\n" + "=" * 126)
    print("H8 et H7, contrastes apparies sur les personnes, perimetre 150, ideologie")
    print("=" * 126)
    s = ct[(ct.perimetre == "150") & (ct.axe == "political_ideology")].copy()
    s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
    print(s.sort_values(["hypothese", "ordre"])[
        ["hypothese", "condition", "difference", "ic_bas", "ic_haut", "p_bootstrap",
         "p_holm", "p_bh"]].to_string(index=False))

    print("\n" + "=" * 126)
    print("Rappel des cellules minoritaires, definition de a8 section 6, perimetre 150")
    print("=" * 126)
    s = minor[(minor.perimetre == "150")].copy()
    s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
    print(s.sort_values(["seuil", "ordre"]).to_string(index=False))


if __name__ == "__main__":
    main()
