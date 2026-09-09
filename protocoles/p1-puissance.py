"""p1. Calcul de puissance de l'experience de lecture, protocoles/01-experience-de-lecture.md.

Aucune donnee, aucun fichier lu, aucun appel de modele. Seulement scipy.stats.norm.

Cinq sections :
  1. taille par bras en plan equilibre, a effet, seuil et puissance donnes ;
  2. effet minimal detectable a taille fixee ;
  3. les effets d'Ahler et Sood 2018 convertis en d de Cohen, depuis leurs differences
     publiees, leurs intervalles de confiance et leurs effectifs ;
  4. l'effet de la condition « taux de base » du meme papier, converti de la meme facon ;
  5. l'allocation inegale a un temoin et cinq bras traites, et la taille du plan retenu.

Convention : d est un d de Cohen sur l'echelle de la mesure apres traitement, avant
ajustement de covariable ; r est la correlation entre la covariable de depart et la mesure
apres, sur la meme personne. L'ANCOVA divise l'ecart type residuel par sqrt(1 - r^2).

Rejouer : .venv/bin/python protocoles/p1-puissance.py
"""

import math

from scipy.stats import norm

ALPHA_FAM = 0.05
K_P = 3           # famille P : H1, H2, H6
K_M = 3           # famille M : H3, H4, H5
A_P = ALPHA_FAM / K_P
A_M = ALPHA_FAM / K_M
PUISS = 0.80
R = 0.45          # hypothese de travail, volontairement basse
K_TRAITES = 5     # B, C, D, E, F


def n_par_bras(d, alpha, puissance, r=0.0):
    """Taille par bras, plan equilibre a deux bras, test bilateral."""
    d_eff = d / (1.0 - r ** 2) ** 0.5
    return 2.0 * (norm.ppf(1.0 - alpha / 2.0) + norm.ppf(puissance)) ** 2 / d_eff ** 2


def emd(n, alpha, puissance, r=0.0):
    """Effet minimal detectable, en d non ajuste, a n par bras en plan equilibre."""
    d_eff = (norm.ppf(1.0 - alpha / 2.0) + norm.ppf(puissance)) * (2.0 / n) ** 0.5
    return d_eff * (1.0 - r ** 2) ** 0.5


def allocation_inegale(n_equilibre, k_traites):
    """Temoin commun a k traitements : le temoin recoit sqrt(k) fois un bras traite.

    Rend (n_traite, n_temoin, total) a precision de contraste egale au plan equilibre.
    """
    rac = math.sqrt(k_traites)
    n_t = n_equilibre * (1.0 + 1.0 / rac) / 2.0
    return n_t, rac * n_t, k_traites * n_t + rac * n_t


def d_de_deux_moyennes(m1, lo1, hi1, n1, m2, lo2, hi2, n2):
    """d de Cohen reconstruit de deux moyennes publiees avec leurs IC 95 % et leurs n."""
    sd1 = (hi1 - lo1) / 2.0 / 1.96 * math.sqrt(n1)
    sd2 = (hi2 - lo2) / 2.0 / 1.96 * math.sqrt(n2)
    sd = math.sqrt((sd1 ** 2 * (n1 - 1) + sd2 ** 2 * (n2 - 1)) / (n1 + n2 - 2))
    return m2 - m1, sd, (m2 - m1) / sd


def d_de_une_difference(diff, lo, hi, n_par_bras_source):
    """d de Cohen reconstruit d'une difference publiee avec son IC 95 % et le n par bras."""
    se = (hi - lo) / 2.0 / 1.96
    ecart_type = se / (2.0 / n_par_bras_source) ** 0.5
    return se, ecart_type, diff / ecart_type


if __name__ == "__main__":
    print("=== 1. Taille par bras, plan equilibre, puissance 0,80 ===")
    print()
    print("  d      alpha    r      n/bras   5 bras    recrutes +15 %")
    for d in (0.15, 0.20, 0.22, 0.25, 0.30, 0.35):
        for alpha in (A_M,):
            for r in (0.00, 0.30, 0.45, 0.60):
                n = n_par_bras(d, alpha, PUISS, r)
                print(f"  {d:.2f}   {alpha:.4f}   {r:.2f}   {n:6.0f}   {5 * n:6.0f}    "
                      f"{5 * n * 1.15:6.0f}")
        print()

    print("=== 2. Effet minimal detectable, plan equilibre ===")
    print()
    print("  n/bras   alpha    r      EMD en d   en points de thermometre (ET 25)")
    for n in (250, 300, 345, 400, 480, 558):
        for alpha in (A_M,):
            e = emd(n, alpha, PUISS, R)
            print(f"  {n:6d}   {alpha:.4f}   {R:.2f}   {e:8.3f}   {e * 25:6.2f}")
    print()

    print("=== 3. Ahler et Sood 2018, effets de correction convertis en d ===")
    print()
    for lib, diff, lo, hi, n_src in (
        ("extremite percue, part de placements a l'extreme", 0.066, 0.02, 0.11, 1036 / 3),
        ("thermometre, echelle 0 a 1", 0.064, 0.03, 0.10, 1036 / 3),
        ("distance sociale", 0.025, 0.00, 0.05, 821 / 3),
    ):
        se, et, d = d_de_une_difference(diff, lo, hi, n_src)
        print(f"  {lib:48s} diff={diff:.3f}  SE={se:.4f}  ET={et:.3f}  d={d:.3f}")
    print()

    print("=== 4. Ahler et Sood 2018, condition « taux de base » ===")
    print()
    print("  dyade         standard  taux de base   ecart   ET     d")
    for lib, args in (
        ("dem_black", (36.2, 31.6, 40.7, 98, 43.2, 38.3, 48.0, 95)),
        ("dem_lgb", (27.0, 21.9, 32.1, 98, 35.9, 29.5, 42.3, 95)),
        ("rep_rich", (31.5, 26.5, 36.6, 98, 39.2, 33.2, 45.3, 95)),
        ("rep_evang", (46.6, 41.1, 52.1, 98, 56.0, 50.8, 61.3, 95)),
        ("rep_old", (44.7, 40.3, 49.0, 98, 53.1, 49.1, 57.2, 95)),
    ):
        diff, sd, d = d_de_deux_moyennes(*args)
        print(f"  {lib:12s}  {args[0]:6.1f}    {args[4]:6.1f}      "
              f"{diff:+5.1f}   {sd:5.1f}  {d:.3f}")
    print()

    print("=== 5. Le plan retenu : un temoin, cinq bras traites ===")
    print()
    n_eq = n_par_bras(0.22, A_M, PUISS, R)
    n_t, n_c, total = allocation_inegale(n_eq, K_TRAITES)
    print(f"  plan equilibre equivalent : {n_eq:.0f} par bras, "
          f"{6 * n_eq:.0f} pour six bras")
    print(f"  allocation inegale        : {n_t:.0f} par bras traite, "
          f"{n_c:.0f} au temoin, total {total:.0f}")
    print(f"  verification de precision : 1/{n_t:.0f} + 1/{n_c:.0f} = "
          f"{1 / n_t + 1 / n_c:.6f}  contre  2/{n_eq:.0f} = {2 / n_eq:.6f}")
    print(f"  recrutes a +15 %          : {total * 1.15:.0f}")
    print()
    n_t9, n_c9, total9 = allocation_inegale(n_eq, 8)
    print(f"  extension E1, neuf bras   : {n_t9:.0f} par bras traite, "
          f"{n_c9:.0f} au temoin, total {total9:.0f}, recrutes {total9 * 1.15:.0f}")
