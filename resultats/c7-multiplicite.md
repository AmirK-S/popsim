# C7. La multiplicité, traitée honnêtement
Recensement sur trois familles : `article-synthese.md` (A1-A10, 15 sous-études `c7-*`), les contrôles autonomes (`a1-*`, `b123-*`), les branches abandonnées (`c5-*`, `memoire-*`, `caricature-profil-*`, `echelle-*`, `tab-*`/Twin A→B). Chaque verdict est recopié du tableau ou de la section « Verdict » du rapport cité, jamais recalculé ; sans p ni IC, c'est écrit tel quel.

## 1. Comptage par famille
| famille | tests tranchés | confirmés | réfutés | partiels/non concluants |
|---|---|---|---|---|
| affirmations de l'article (15 sous-études c7) | 34 | 20 | 11 | 3 |
| contrôles autonomes (a1, b123) | 2 | 1 | 1 | 0 |
| branches abandonnées (c5, mémoire, caricature, échelle, tab) | 11 | 4 | 3 | 4 (c5) |
| **total** | **47** | **25** | **15** | **7** |

Réfutations de l'article (11) : c7-disjoint (b) ; c7-bits prédiction 2 (loi d'entropie, signe opposé Twin/Stanford) ; c7-compromis (coût en bits/fidélité non constant) ; c7-monde-ouvert (seuils Twin >5 %, Stanford >30 %) ; c7-mecanisme H1 et H4 ; c7-transfert (volet 19 items) ; c7-transfert-stanford (seuil ≥20 %) ; c7-recette (granularité de l'appel) ; c7-deviations (a) ; c7-gen R1 (≥10 % sur 2/3 modèles). Abandonnées : `memoire-resultats.md` P3, `caricature-profil-resultats.md` (rejetée, sens inverse), `tab-resultats.md` (R1-R4 tous faux) ; `c5-resultats.md` (deux modèles, aucun des trois critères atteint, zone grise, ni confirmé ni réfuté).

## 2. Correction de multiplicité, affirmations de l'article
Sur les 34 tests, **seuls 3 rapportent un p classique** (les autres sont des IC bootstrap sur un seuil préenregistré, §3) : p=0,002 (`c7-courbe-gen`, r=0,785, confirme la courbe fidélité-fuite, A9) ; p=0,008 (`c7-compromis` §2, r=0,724, exactitude comme proxy) ; p=0,78 (`c7-compromis` §3, style propre vs fidélité, n=8, déjà non concluant). **Holm** (FWER, n=3, chaque test soutient une affirmation centrale) : trié 0,002<0,008<0,78 → ajustés 0,006 ; 0,016 ; 0,78. **Survivent à α=0,05 : p=0,002 et p=0,008.** Le troisième ne survit pas, mais n'a jamais été dit significatif.

## 3. Ce que la correction ne couvre pas
Les 31 autres tests sont des **mesures avec IC bootstrap** comparées à un seuil fixé d'avance (top-1 de ré-identification, rho, bits d'identité), pas des tests indépendants avec un p propre : Holm/BH ne s'y applique pas de la même façon, faute de p commensurable. Recalculer à un niveau ajusté (ex. 99,7 % pour 15-20 comparaisons) exigerait de refaire chaque bootstrap, non fait ici.

## 4. Ce que nous ne prétendons pas
- Pas un plan d'expérience unique corrigé globalement : trois familles, trois logiques d'échec.
- Les IC bootstrap n'équivalent pas à des p corrigés : seuls 3 tests le permettent.
- 25 confirmations sur 47 ne valident pas la thèse en bloc : 11 des 15 réfutations portent sur des affirmations que l'article retient quand même, sous forme corrigée ou amoindrie (A1, A3, A7, A9), pas balayées sous le tapis.
- Ce recensement n'est pas exhaustif à chaque sous-hypothèse descriptive ; il compte les verdicts que chaque rapport se donne lui-même.

## Paragraphe pour la section Limitations
*La plupart des résultats centraux de cet article reposent sur des intervalles de confiance bootstrap autour d'une mesure descriptive — taux de ré-identification, corrélation de rang, bits d'identité — non sur des tests d'hypothèse classiques ; sur les 34 prédictions préenregistrées qui sous-tendent ces affirmations, 11 ont été réfutées et 3 jugées non concluantes, un taux d'environ un tiers, l'inverse de la signature d'un dragage de données. Sur les 3 tests disposant d'un p classique, une correction de Holm laisse subsister les deux plus petits (0,002 et 0,008, ajustés à 0,006 et 0,016) et confirme la non-signification du troisième (0,78), déjà lu comme tel avant correction ; les intervalles de confiance qui portent les autres affirmations ne se corrigent pas de la même manière et doivent être lus comme des mesures, chacune avec sa propre marge, non comme des rejets indépendants d'une hypothèse nulle commune.*
