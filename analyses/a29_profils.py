"""
a29_profils : qui sont les personnes minoritaires, et qui chaque methode designe comme
telles.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a29_commun, et par lui a28_commun, a25_commun,
a8_commun et a2_commun, sont importes tels quels.

TOUT CE QUE CE SCRIPT PRODUIT EST DESCRIPTIF et n'entre dans aucune famille
d'hypotheses. Il ne porte aucun p corrige, et aucune de ses lignes ne doit etre lue comme
un test : ce sont des profils, avec leurs intervalles bootstrap sur les personnes, poses
cote a cote. La raison est ecrite ici pour ne pas etre oubliee a la relecture : les
comparaisons possibles se comptent en centaines, six axes fois quatorze conditions, et
aucune n'a ete declaree avant de voir les chiffres.

Trois questions, dans cet ordre.

  1. Qui donne beaucoup de reponses rares dans la vraie population ? Taux de reponses
     rares par personne, moyenne par niveau demographique, plus la fidelite test retest de
     la personne, c'est a dire la part d'items ou elle redonne la meme reponse deux
     semaines plus tard. Une personne qui repond souvent la modalite rare est elle une
     personne instable ou une personne stable et minoritaire ?
  2. Qui chaque methode designe t elle comme rare ? Meme profil, calcule sur le taux de
     reponses rares PREDITES. Une methode qui aurait un stereotype de "personne
     marginale" produirait un profil plus contraste que la realite sur l'axe qui porte le
     stereotype, et un profil plat ailleurs.
  3. Le profil predit ressemble t il au profil reel ? Correlation, a travers les niveaux
     demographiques, entre le taux reel moyen et le taux predit moyen, et rapport
     d'amplitude entre le niveau le plus rare et le moins rare.

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, caches de a25 et de a28.
Sortie  : resultats/a29-profils-niveaux.csv, a29-profils-correlation.csv,
          a29-profils-quintiles.csv, a29-profils-fidelite.csv.

Usage :
  .venv/bin/python analyses/a29_profils.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 2000
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a29_commun as C
from a8_commun import modalites_minoritaires

SEUIL = 0.10


def moyenne_par_niveau(valeurs, seg, n_niveaux, idx_boot=None):
    """Moyenne d'un vecteur par niveau de segment, avec intervalle bootstrap."""
    out = []
    for k in range(n_niveaux):
        m = seg == k
        v = valeurs[m]
        v = v[~np.isnan(v)]
        if len(v) == 0:
            out.append((k, 0, np.nan, np.nan, np.nan))
            continue
        if idx_boot is None:
            out.append((k, len(v), float(v.mean()), np.nan, np.nan))
            continue
        tir = np.array([np.nanmean(valeurs[i][seg[i] == k])
                        if (seg[i] == k).any() else np.nan for i in idx_boot])
        tir = tir[~np.isnan(tir)]
        out.append((k, len(v), float(v.mean()),
                    float(np.percentile(tir, 2.5)) if len(tir) else np.nan,
                    float(np.percentile(tir, 97.5)) if len(tir) else np.nan))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--graine", type=int, default=C.GRAINE)
    args = ap.parse_args()

    t0 = time.time()
    paquet = C.charger(args.cache, args.cache_foret)
    rng = np.random.default_rng(args.graine)
    per = C.perimetres(paquet)
    seg_tous, niveaux = C.segments_et_niveaux(paquet)

    niveaux_lignes, corr_lignes, quint_lignes, fid_lignes = [], [], [], []

    for nom_per, lignes in per.items():
        methodes = C.methodes_du_perimetre(paquet, nom_per)
        verite = paquet["y1"][lignes]
        mods = modalites_minoritaires(verite, SEUIL)
        idx_boot = C.tirages_bootstrap(len(lignes), args.tirages, rng)

        # taux reel de reponses rares, et fidelite test retest, par personne
        c_ref = C.compter(verite, verite, mods)
        u_reel = c_ref["n_rare_vrai"] / np.where(c_ref["n_eval"] > 0,
                                                 c_ref["n_eval"], np.nan)
        fid = C.fidelite_test_retest(paquet["y1"], paquet["y2"], lignes)

        taux_predits = {}
        for nom in methodes:
            c = C.compter(paquet["M"][nom][lignes], verite, mods)
            _, v = C.taux(c)
            taux_predits[nom] = v

        # --------------------------------------------------------- 1 et 2, profils
        for axe in C.AXES:
            seg = seg_tous[axe][lignes]
            noms_niveaux = niveaux[axe]
            base = moyenne_par_niveau(u_reel, seg, len(noms_niveaux), idx_boot)
            reel = {k: m for k, _, m, _, _ in base}
            for k, n, m, b, h in base:
                niveaux_lignes.append({
                    "perimetre": nom_per, "axe": axe, "niveau": noms_niveaux[k],
                    "condition": "reel, vague 1", "personnes": n, "taux_rares": m,
                    "ic_bas": b, "ic_haut": h})
            for nom in methodes:
                for k, n, m, b, h in moyenne_par_niveau(taux_predits[nom], seg,
                                                        len(noms_niveaux), idx_boot):
                    niveaux_lignes.append({
                        "perimetre": nom_per, "axe": axe, "niveau": noms_niveaux[k],
                        "condition": nom, "personnes": n, "taux_rares": m,
                        "ic_bas": b, "ic_haut": h})
                pred = {k: m for k, _, m, _, _ in
                        moyenne_par_niveau(taux_predits[nom], seg, len(noms_niveaux))}
                ks = [k for k in reel if not np.isnan(reel[k]) and not np.isnan(pred[k])]
                a = np.array([reel[k] for k in ks])
                b2 = np.array([pred[k] for k in ks])
                corr_lignes.append({
                    "perimetre": nom_per, "axe": axe, "condition": nom,
                    "niveaux": len(ks),
                    "rho_profil": C.spearman(a, b2),
                    "r_profil": C.pearson(a, b2),
                    "amplitude_reelle": float(a.max() / a.min()) if len(a) and a.min() > 0
                    else np.nan,
                    "amplitude_predite": float(b2.max() / b2.min())
                    if len(b2) and b2.min() > 0 else np.nan,
                    "niveau_le_plus_rare_reel": noms_niveaux[ks[int(np.argmax(a))]]
                    if len(ks) else "",
                    "niveau_le_plus_rare_predit": noms_niveaux[ks[int(np.argmax(b2))]]
                    if len(ks) else "",
                })

        # ------------------------------------------------- 3, quintiles de personnes
        ok = ~np.isnan(u_reel)
        rangs = np.full(len(u_reel), -1)
        vals = u_reel[ok]
        bornes = np.quantile(vals, [0.2, 0.4, 0.6, 0.8])
        rangs[ok] = np.searchsorted(bornes, vals, side="right")
        for q in range(5):
            m = rangs == q
            ligne = {"perimetre": nom_per, "quintile": q + 1,
                     "personnes": int(m.sum()),
                     "taux_rares_reel": float(np.nanmean(u_reel[m])),
                     "fidelite_test_retest": float(np.nanmean(fid[m]))}
            for nom in methodes:
                ligne[nom] = float(np.nanmean(taux_predits[nom][m]))
            quint_lignes.append(ligne)

        # ------------------------------------- fidelite test retest et rarete predite
        fid_lignes.append({
            "perimetre": nom_per, "condition": "reel, vague 1",
            "rho_avec_fidelite": C.spearman(u_reel, fid),
            "rho_avec_taux_reel": 1.0})
        for nom in methodes:
            fid_lignes.append({
                "perimetre": nom_per, "condition": nom,
                "rho_avec_fidelite": C.spearman(taux_predits[nom], fid),
                "rho_avec_taux_reel": C.spearman(taux_predits[nom], u_reel)})
        print(f"  perimetre {nom_per} : fait ({time.time() - t0:.0f} s)", flush=True)

    niv = pd.DataFrame(niveaux_lignes)
    cor = pd.DataFrame(corr_lignes)
    qui = pd.DataFrame(quint_lignes)
    fdl = pd.DataFrame(fid_lignes)

    C.ecrire(niv, "a29-profils-niveaux.csv")
    C.ecrire(cor, "a29-profils-correlation.csv")
    C.ecrire(qui, "a29-profils-quintiles.csv")
    C.ecrire(fdl, "a29-profils-fidelite.csv")

    pd.set_option("display.width", 260)
    ordre = {c: i for i, c in enumerate(C.ORDRE_METHODES)}

    print("\n" + "=" * 140)
    print("Qui donne des reponses rares, perimetre 1 052, axe ideologie et axe education")
    print("=" * 140)
    for axe in ("political_ideology", "education", "race", "age", "gender"):
        s = niv[(niv.perimetre == "1052") & (niv.axe == axe)
                & (niv.condition == "reel, vague 1")]
        print(f"\n-- {axe}")
        print(s[["niveau", "personnes", "taux_rares", "ic_bas",
                 "ic_haut"]].round(4).to_string(index=False))

    print("\n" + "=" * 140)
    print("Profil predit contre profil reel, perimetre 1 052")
    print("=" * 140)
    s = cor[cor.perimetre == "1052"].copy()
    s["o"] = s.condition.map(ordre)
    piv = s.pivot_table(index=["condition"], columns="axe", values="rho_profil")
    print(piv.reindex([c for c in C.ORDRE_METHODES if c in piv.index]).round(3).to_string())

    print("\n" + "=" * 140)
    print("Amplitude du profil sur l'axe ideologie, perimetre 1 052")
    print("=" * 140)
    s = cor[(cor.perimetre == "1052") & (cor.axe == "political_ideology")].copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values("o")[["condition", "amplitude_reelle", "amplitude_predite",
                              "niveau_le_plus_rare_reel", "niveau_le_plus_rare_predit",
                              "rho_profil"]].round(3).to_string(index=False))

    print("\n" + "=" * 140)
    print("Quintiles de personnes par taux de reponses rares reelles")
    print("=" * 140)
    for nom_per in ("1052", "150"):
        print(f"\n-- perimetre {nom_per}")
        print(qui[qui.perimetre == nom_per].round(4).to_string(index=False))

    print("\n" + "=" * 140)
    print("Rarete predite et fidelite test retest de la personne")
    print("=" * 140)
    s = fdl.copy()
    s["o"] = s.condition.map(lambda c: ordre.get(c, -1))
    print(s.sort_values(["perimetre", "o"])[
        ["perimetre", "condition", "rho_avec_fidelite",
         "rho_avec_taux_reel"]].round(4).to_string(index=False))

    print(f"\nduree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
