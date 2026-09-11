# B123. Resultats : ce que les baselines gratuites obtiennent sur les metriques vitrines

Protocole fige dans `resultats/b123-preenregistrement.md`. Calcul : `analyses/b123_baselines_vendeurs.py`,
sorties dans `b123-gss.csv`, `b123-twin.csv`, `b123-resume.csv`. Zero appel de modele. GSS : 342
items communs aux vagues 1 des panels NORC 2008 (n=2023) et 2010 (n=2044), 2-7 modalites,
N >= 200/cohorte. Twin-2K-500 : 105/108 items categoriels, humains vagues 1-3 contre verite
vague 4 (memes 2 058 personnes, retest a deux semaines).

## Tableau : metrique x baseline x jeu, face au chiffre-vitrine

| metrique | jeu | B0 uniforme | B1 (autre cohorte / persistance) | B2 sous-groupe | chiffre-vitrine cite |
|---|---|---|---|---|---|
| 1-MAE (mediane) | GSS | 0,835 | **0,985** | 0,984 | 0,955 (Electric Twin) ; 0,945 (Kantar) |
| 1-MAE (mediane) | Twin-2K-500 | 0,907 | **0,988** | — | idem |
| Recouvrement 1-TV (mediane) | GSS | 0,738 | **0,974** | 0,974 | 0,86 (Artificial Societies) |
| Recouvrement 1-TV (mediane) | Twin-2K-500 | 0,817 | **0,982** | — | idem |
| Similarite KS (mediane, items ordinaux) | GSS | non calculee | non calculee | — | 0,85-0,88 (SSR/PyMC Labs) |
| Similarite KS (mediane, items ordinaux) | Twin-2K-500 | 0,742 | **0,980** | — | idem |
| Spearman median | GSS | n.d. | **1,0** | 1,0 | 0,90 (Aaru) |
| Spearman median | Twin-2K-500 | n.d. | **1,0** | — | idem |

Sur les quatre metriques et les deux jeux, la marge de l'autre cohorte ou vague (B1), qui ne
simule rien, egale ou depasse chaque chiffre-vitrine cite en section 1 de `idees-B-industrie-2026-09-11.md`.
Le prealable [PARI] (3/4 metriques, au moins un jeu) est depasse : 4/4, sur les deux jeux. B2
(sous-groupe) n'ajoute rien a B1 sur GSS ; omise sur Twin (memes personnes des deux cotes).

## Sensibilite : item permute et camp inverse (B1 degrade), n items GSS/Twin = 336/99

| metrique | B1 (referent) | BAD item permute | BAD camp inverse |
|---|---|---|---|
| 1-MAE, GSS | 0,985 | 0,786 | 0,762 |
| 1-MAE, Twin | 0,988 | 0,891 | 0,848 |
| 1-TV, GSS | 0,974 | 0,650 | 0,596 |
| 1-TV, Twin | 0,982 | 0,804 | 0,803 |
| KS, Twin | 0,980 | 0,714 | 0,532 |
| Spearman median, GSS | 1,0 | 0,0 | −1,0 |
| Spearman median, Twin | 1,0 | 0,8 | −1,0 |

Spearman median est le plus discriminant : effondrement a 0 sous item permute et a −1 sous camp
inverse, sur les deux jeux. KS degrade fortement sous camp inverse (0,53 sur Twin, sous le
plancher uniforme 0,74). Le 1-MAE, tel que publie, est le moins discriminant : sous camp inverse
(simulation deliberement fausse), il reste a 0,76-0,85, lisible comme « 76-85 % d'exactitude »,
proche du chiffre-vitrine (0,945-0,955) et a peine sous le plancher uniforme (GSS : 0,762 vs 0,835).

**Ce que cela ne dit pas.** KS non calculee sur le GSS (items nominaux, ordre indefini) ; SCE hors
perimetre, comme annonce. Ces chiffres portent sur nos items et nos deux jeux publics, pas sur les
items prives d'un vendeur cite.
**Verdict.** Sur 1-MAE, 1-TV et Spearman, la baseline gratuite « marge d'une autre cohorte ou
vague » egale ou depasse chaque chiffre-vitrine cite ; le 1-MAE est, des quatre, le moins capable
de separer une bonne baseline d'une simulation inversee.
