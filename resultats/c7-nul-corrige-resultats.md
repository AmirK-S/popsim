# C7, nul de marge corrigé : résultats

> ## AVERTISSEMENT DE RÉTRACTATION — 12 septembre 2026
> **Ce rapport a été réfuté le 12 septembre 2026. Ses conclusions (renversement de la
> prédiction (b), « issue B », et les six modifications de la section 7 ci-dessous) NE
> DOIVENT PAS ÊTRE APPLIQUÉES.** Il est conservé uniquement pour la traçabilité de
> l'historique scientifique du projet — rien n'y a été effacé.
>
> Font foi, à la place de ce document : `resultats/audit-renversement-2026-09-12.md`
> (l'audit adverse) et `resultats/c7-nul-corrige-reponse-audit.md` (la concession de
> l'auteur de ce rapport lui-même : « Mon renversement tombe »).
>
> **Ce qui est vrai à la place, en trois lignes :**
> - Le témoin correct (exactitude exacte contre la **vérité**, positions au hasard, cellules
>   fausses tirées dans la marginale de population) donne rho 0,974–0,985 ; le prédicteur
>   réel à 0,965 ne le dépasse pas — la prédiction (b) **reste réfutée**, le titre de
>   l'article **ne change pas**.
> - Le témoin historique (celui que ce rapport dit « cassé ») avait néanmoins un défaut réel,
>   ligne 133, qui gonflait la fuite d'un facteur 1,3 (41,2 % au lieu de 31,6 %), **sans
>   inverser le verdict**.
> - Les témoins « corrigés » de ce rapport (§2 ci-dessous) appariaient l'exactitude contre une
>   **cible de substitution** et non contre la vérité, ce qui détruisait la grandeur même que
>   l'objection dit explicative ; ils portaient malgré tout de la structure individuelle
>   (31,15 % de top-1, 4,63 bits, contre 20,73 % / 3,56 pour le jumeau réel et 0,049 % pour le
>   hasard pur) — leur comparaison ne portait sur rien.

Préenregistré dans `c7-nul-corrige-preenregistrement.md` (écrit avant le script et avant
tout calcul), calculé par `analyses/c7_nul_corrige.py`, données `c7-nul-corrige.csv`.
**Reproductibilité : vérifiée.** Deux exécutions complètes indépendantes (3 977 s chacune,
100 réplicats, 40 permutations, bootstrap 2 000) donnent un CSV **identique bit à bit**
(md5 `e994f8f31e8c6faf389ceb3a8baa09fe` des deux côtés).

## 1. Le défaut, et l'arbitrage de l'objection conceptuelle

`c7_disjoint.construire_nul` ligne 134 écrit `np.where(tirage_correct, y_ref, faux)` : le
« nul de marge » émet **la vraie réponse de la personne** avec probabilité q_i. Ligne 133,
`faux + (faux >= y_ref)` fait en outre dépendre les cellules *fausses* de cette même vraie
réponse. Ce n'est pas un prédicteur « sans empreinte individuelle » : c'est une copie
bruitée du vecteur réel.

**L'objection de `c7_tautologie` (« apparier l'exactitude sans lire la cible est impossible,
le nul n'était donc pas cassé mais conforme à sa définition ») est à moitié fondée, et sa
conclusion est fausse.** Il faut séparer deux choses :

1. **Coïncider avec la vérité sur k_i positions.** Inévitable, en effet : « exactitude k_i »
   *signifie* coïncider k_i fois. Sur ce point l'autre agent a raison.
2. **Choisir *quelles* positions coïncident.** C'est là, et seulement là, que se loge une
   empreinte individuelle — et c'est une variable libre, pas une conséquence de (1).

La preuve que (1) ne suffit pas est dans les chiffres de l'autre agent eux-mêmes : son
témoin « mode global » coïncide avec chaque personne sur **49,9 %** des items et fuit
**0,06 %**, pour **0 bit** ; sa condition (a) coïncide sur **59 %** et fuit **31,9 %**, pour
**4,64 bits**. Dix points de coïncidence de plus ne peuvent pas produire un facteur 500 sur
le top-1. Ce qui les sépare est que le mode global coïncide là où la personne est *banale*
(les mêmes positions pour tous ses semblables, donc les leurres marquent autant qu'elle),
tandis que (a) coïncide sur un sous-ensemble *uniforme de ses items à elle*, donc y compris
ses réponses atypiques — ce qu'on ne peut écrire qu'en lisant sa ligne.

**Ce que faisait réellement le nul d'origine, code à l'appui** : il tirait les *positions*
au hasard (`rng.random(...) < q[:, None]`, indépendant de la personne) mais il y écrivait le
*contenu* `y_ref[i, j]`, c'est-à-dire les réponses rares de cette personne au même taux que
ses réponses banales. Il faisait donc (2), pas seulement (1). Un témoin ne gardant que la
marge doit produire son contenu depuis une source de population ou d'autrui ; sa coïncidence
se concentre alors mécaniquement sur le banal et ne peut pas atteindre q_i sur les items
rares. **Conclusion : « un prédicteur n'ayant que la marge d'exactitude *contre la personne*
et aucune information individuelle » est une contradiction dans les termes. L'objet construit
par `c7_disjoint` n'était pas ce nul : c'était son contraire.** La marge doit donc être
appariée contre une **cible de substitution**, ce que font N1, N2 et N3.

## 2. Les constructions et leurs contrôles

| témoin | cible de l'exactitude q_i | lit-il `y_ref[i]` ? |
|---|---|---|
| N0 nul cassé (importé tel quel) | `y_ref[i]`, la personne elle-même | **oui, c'est le défaut** |
| N1 / N1b mode de segment | mode du segment **calculé sans elle** | non (q_i seul) |
| N2 / N2b vecteur d'autrui | vrai vecteur d'**une autre** personne (dérangement intra-segment) | non (q_i seul) |
| N3 identités permutées | le vecteur réel de σ(i) | **jamais** |
| N4 mode global (plancher) | aucune marge appariée | non |

Contrôles passés : exactitude visée atteinte **exactement** pour N1/N2 (écart moyen
0,00000) et à 4·10⁻⁵ près pour N3 ; pour les variantes Bernoulli, écart standardisé moyen
**0,794–0,795** contre E|N(0,1)| = 0,798 attendu, ce qui valide l'échantillonneur. Masque de
couverture identique cellule à cellule partout sauf N3, où il suit le vecteur permuté
(conservé en multi-ensemble — déviation attendue et déclarée). Dérangement sans point fixe
garanti par construction (cycle unique), assertion bloquante.

## 3. Résultat principal : le renversement

rho = Spearman des 12 prédicteurs (fidélité = chute brute, fuite = top-1), **60 items
entiers**, 100 réplicats.

| construction | rho moyen | médiane | [p5 ; p95] | IC bootstrap personnes | rho réel > p95 ? |
|---|---|---|---|---|---|
| **prédicteur réel** | **0,9650** | — | — | **[0,9371 ; 0,9930]** | — |
| N0 nul cassé | 0,9803 | 0,9860 | [0,9507 ; **1,0000**] | [0,9301 ; 1,0000] | **non** |
| N1 mode de segment | 0,1681 | 0,1589 | [−0,3009 ; 0,5695] | [−0,0735 ; 0,7426] | **oui** |
| N1b mode de segment (Bernoulli) | 0,2058 | 0,2401 | [−0,2284 ; 0,5936] | [−0,0338 ; 0,7502] | **oui** |
| N2 vecteur d'autrui | 0,1342 | 0,1572 | [−0,4220 ; 0,5911] | [−0,4150 ; 0,4213] | **oui** |
| N2b vecteur d'autrui (Bernoulli) | 0,1176 | 0,1118 | [−0,4203 ; 0,5750] | [−0,1606 ; 0,6161] | **oui** |
| N3 identités permutées | 0,1387 | 0,1393 | [−0,3154 ; 0,5468] | [−0,2894 ; 0,6382] | **oui** |
| N4 mode global (plancher) | −0,1334 | — | — | [−0,4935 ; 0,5058] | **oui** |

**Le nul cassé reproduisait rho (0,980, 95e centile 1,000) ; les cinq nuls corrigés ne le
reproduisent pas (0,118–0,206, 95es centiles 0,547–0,594), et le rho observé 0,965 dépasse
les cinq, à l'unanimité.** Issue B du préenregistrement.

Fuite et fidélité sous les nuls corrigés : **top-1 moyen 0,040–0,063 % contre un hasard de
0,049 %** (1/2 058) — exactement le plancher — et **bits 0,000–0,008**, indiscernables de
zéro ; chute de fidélité −0,0013 à −0,0018, soit zéro. Les deux axes s'effondrent ensemble,
comme prévu au §6 du préenregistrement.

## 4. Top-1 par configuration, prédicteur réel — le tableau qui manquait à l'article

Calculé puis jeté par la boucle des lignes 221-235 de `c7_disjoint.py` ; ici enregistré.
60 items entiers, pool de 2 058, IC bootstrap 2 000 sur les personnes.

| configuration | exactitude | chute | top-1 [IC 95 %] | bits | δ |
|---|---|---|---|---|---|
| retest humain v1-3 (plafond) | 0,745 | 0,303 | **81,50 %** [79,79 ; 83,11] | 9,15 | 0,313 |
| JSON Persona - GPT4.1 | 0,590 | 0,154 | **20,73 %** [19,03 ; 22,48] | 3,56 | 0,159 |
| Text Persona - Gemini-Flash2.5 | 0,560 | 0,141 | 13,12 % [11,74 ; 14,51] | 2,82 | 0,146 |
| JSON Persona - GPT4.1-mini | 0,550 | 0,128 | 12,10 % [10,23 ; 14,03] | 2,41 | 0,135 |
| Text Persona (Reasoning) - mini | 0,546 | 0,122 | 9,23 % [8,00 ; 10,51] | 2,09 | 0,126 |
| Text Persona (Repeating Q.) - mini | 0,557 | 0,120 | 7,29 % [6,24 ; 8,37] | 2,04 | 0,124 |
| Text Persona (Default Temp.) - mini | 0,552 | 0,109 | 5,43 % [4,50 ; 6,41] | 1,59 | 0,113 |
| Text Persona - GPT4.1-mini | 0,558 | 0,114 | 5,33 % [4,36 ; 6,33] | 1,73 | 0,119 |
| Demographics Only - mini | 0,494 | 0,079 | 2,17 % [1,60 ; 2,83] | 0,82 | 0,083 |
| B1 argmax | 0,504 | 0,032 | 0,275 % [0,08 ; 0,52] | 0,16 | 0,048 |
| PMM k=10 | 0,475 | 0,033 | 0,211 % [0,05 ; 0,42] | 0,19 | 0,039 |
| B2 argmax | 0,511 | 0,034 | 0,081 % [0,00 ; 0,21] | 0,08 | 0,039 |
| B0 tirage | 0,432 | 0,001 | 0,065 % [0,00 ; 0,18] | 0,00 | 0,001 |

## 5. Le fait embarrassant, quantifié : pourquoi le vrai jumeau fuit moins que le faux

À **exactitude identique** (a = 0,5904 réel contre 0,5894 pour le nul cassé bâti sur sa
propre marge), le jumeau réel fuit **deux fois moins** :

| | a (coïncidence avec la vraie personne) | c (coïncidence avec un candidat au hasard) | δ = a − c | top-1 | bits |
|---|---|---|---|---|---|
| JSON Persona GPT4.1 **réel** | 0,5904 | **0,4319** | **0,1585** | 20,73 % | 3,56 |
| N0 nul cassé, même marge | 0,5894 | **0,4093** | **0,1800** | **41,18 %** | 5,22 |

**L'explication tient dans la colonne c.** Le jumeau réel et le faux coïncident autant avec
la vraie personne ; mais les **erreurs** du jumeau réel tombent sur des réponses de
population, si bien qu'elles coïncident *aussi* avec les leurres (c = 0,432 contre 0,409).
L'excès de coïncidence δ, qui est ce sur quoi l'attaque trie, passe de 0,180 à 0,159, et le
top-1 de 41,2 % à 20,7 %. Le jumeau converge vers la moyenne là où il se trompe, ce qui
réduit sa distinctivité. **Confirmation indépendante du résultat de `c7_tautologie`**, avec
un chiffre plus haut que le sien (41,2 % contre 31,9 %) parce que ses valeurs fausses sont
tirées dans la marginale de l'item quand les miennes sont uniformes — une erreur uniforme
est plus distinctive, donc fuit davantage. **Dans les deux cas, le témoin artificiel dépasse
le jumeau réel : à exactitude égale, nos jumeaux sont un MINORANT de ce que la fuite peut
atteindre, pas un maximum.**

## 6. Verdict, règle préenregistrée §7, et sa réserve

**Issue B, à l'unanimité des cinq témoins corrigés.** La réfutation publiée dans
`c7-disjoint-resultats.md` §2 et reprise dans l'article **tombe** : elle reposait sur un
témoin qui copiait la cible. La prédiction (b) du préenregistrement `c7-disjoint` («  le rho
observé dépasse le 95e centile du nul ») est, après correction, **confirmée**.

**Réserve, écrite au §8 du préenregistrement avant de voir les chiffres, et qui s'applique
pleinement ici.** Un témoin correct détruit les deux axes à la fois — c'est sa définition —
donc les dépasser était *presque* acquis d'avance et ne prouve pas la causalité. Ce qui est
établi est exactement : **le couplage n'est pas produit par un taux d'exactitude par personne
seul**. Ce qui ne l'est pas : que la fidélité *à cette personne-là* en soit le mécanisme. Le
§5 pousse même dans l'autre sens — un hasard calé sur la même exactitude fuit deux fois plus
que le jumeau réel. Et n = 12 rend le Spearman grossier : aucune troisième décimale n'est
interprétée (les 100 réplicats ont tous un rho défini, 0 axe constant, mais les
distributions nulles sont larges, p5 ≈ −0,42 à −0,23).

**Réponse en un mot : soutenue — faiblement.** Non pas « démontrée » : la thèse cesse d'être
réfutée et redevient défendable, sans que sa version causale forte soit établie.

**Divergence entre les cinq constructions** : 0,118 à 0,206 de rho moyen, soit un écart réel
mais sans conséquence — les cinq 95es centiles (0,547–0,594) sont du même ordre et les cinq
donnent le même verdict. L'écart vient du résidu d'information non individuelle que chaque
cible de substitution laisse passer : le mode de segment porte encore un peu de signal de
segment (N1 : bits 0,008, δ 0,0067), le vecteur d'autrui n'en porte presque aucun (N2 :
bits −0,001, δ 0,0016). **Mesure de référence recommandée pour l'article : N2 (vecteur
d'autrui)** — c'est la plus stricte (marge appariée exactement, marginales et corrélations
inter-items réalistes puisqu'elle recopie un vrai humain, δ le plus bas). Publier la
fourchette 0,118–0,206 en note, pas un chiffre unique.

## 7. Ce que l'article doit changer

> **RÉTRACTÉ — NE PAS APPLIQUER.** Les six modifications ci-dessous reposent sur le
> renversement réfuté (voir l'avertissement en tête de fichier). Elles sont conservées mot
> pour mot pour la trace, chacune marquée `[NE PAS APPLIQUER]` ; aucune ne doit être portée
> sur `article/manuscrit.md` ni ailleurs.

Six endroits, plus le script de figure. Aucun n'est modifié par ce script.

1. **[NE PAS APPLIQUER] Titre** (`article/manuscrit.md` l. 1) — « and a Null That Absorbs Our Own Coupling » est
   faux. Remplacer par : *« Linkability of LLM Digital Twins: Open-World Rates, a
   Twin-to-Twin Channel, and a Fingerprint-Free Null That Does Not Absorb the Coupling »*.
2. **[NE PAS APPLIQUER] Résumé** (l. 24-32) — remplacer les phrases sur le « marginal null » par : *« We
   preregistered that the coupling between imitation quality and leakage reflects an
   individual fingerprint, and first reported it refuted by a marginal null. That null was
   defective: it emitted each person's own answer with probability q_i, making it a noisy
   copy of the vector it was meant to exclude. Five corrected witnesses, matching the same
   per-person accuracy against a surrogate target, reach Spearman 0.118–0.206 (95th
   percentiles 0.547–0.594) against 0.965 observed, and leak at chance (top-1 0.04–0.06 %
   against 0.049 %, 0.00 bits). The refutation is withdrawn; the coupling is not produced by
   a per-person accuracy rate alone. At equal accuracy, however, a calibrated noisy copy
   leaks twice as much as the real twin (41.2 % vs 20.7 %): our twins are a lower bound. »*
3. **[NE PAS APPLIQUER] §1.1** (l. 65-71) — remplacer « The second part failed, and it failed against us… » par
   le même constat : le second volet **passe** une fois le témoin réparé, avec la réserve du
   §6 ci-dessus et le renvoi à `c7-nul-corrige-resultats.md` §3.
4. **[NE PAS APPLIQUER] §5.1** (l. 389-393) — remplacer « Prediction (b) was refuted… » par la ligne « prédiction
   (b) confirmée après correction du témoin », tableau du §3 ci-dessus, et conserver le
   paragraphe de prudence (l. 395-399) qui reste exact.
5. **[NE PAS APPLIQUER] Figure 2** — légende (l. 671-686) : la bande grise n'est plus « the marginal null »
   mais « the defective null (shown as the artefact it is) » et la bande à tracer est celle
   des témoins corrigés, que le rho observé **dépasse**. Données : dans
   `analyses/figures_article.py`, l. 277 `rho_obs` vient de `c7-disjoint-resume.csv` et
   l. 278 `bas5, haut95 = np.percentile(nul["rho_nul"], [5, 95])` vient de
   `c7-disjoint-nul.csv` ; les deux doivent lire `resultats/c7-nul-corrige.csv` (lignes
   `type == "rho_replicat"`, `construction == "N2 vecteur d'autrui"` pour la bande, et
   `type == "rho_resume"`, `construction == "reel"` pour le point), l'`axhspan` de la l. 285
   passant alors sous le point au lieu de le recouvrir.
6. **[NE PAS APPLIQUER] Tableau 3, ligne 1** (l. 800) — remplacer *« Refuted. Null rho 0.984 mean, 95th pct
   1.000, against 0.969 observed »* par : *« **Confirmed after the witness was repaired.**
   The original null copied the target; five corrected nulls reach 0.118–0.206 (95th pct
   0.547–0.594) against 0.965 observed. Witness defect and correction:
   `c7-nul-corrige-resultats.md` »*. Le décompte « sixteen refuted predictions » du titre de
   §7.1 devient **quinze**.

**[NE PAS APPLIQUER]** `resultats/article-synthese.md` porte la même affirmation aux lignes
11, 13, 19, 20, 103, 112, 114 et 134 : à corriger par qui en a la charge, pas par ce script.

## 8. Déviations déclarées

1. Le préenregistrement demandait un tirage de Bernoulli **et** un écart maximal à q_i
   < 0,08 : incompatibles (l'écart type binomial à 60 cellules vaut 0,065, son maximum sur
   2 058 personnes le dépasse nécessairement). N1/N2 tirent donc un **effectif exact**
   (exigence « même exactitude par personne » atteinte exactement), et N1b/N2b exécutent la
   règle préenregistrée telle quelle. Les deux familles donnent le même verdict.
2. Le seuil bloquant d'écart standardisé, fixé à 5 au préenregistrement, était la **même
   erreur de calibrage répétée** : il compare un maximum sur 2,36 millions d'écarts à une
   borne pensée pour un seul tirage. Il a fait échouer une première exécution complète
   (N1b, z max 5,20). Remplacé par le maximum attendu `sqrt(2 ln M) + 2` = 7,42, dérivé du
   nombre d'écarts et non des valeurs observées, complété par un contrôle de **loi** (écart
   standardisé moyen contre E|N(0,1)| = 0,798) qui est le test réellement informatif.
3. N3 ne conserve le masque qu'en multi-ensemble (il suit le vecteur permuté), et conserve
   la **distribution** des q, pas leur appariement personne par personne.

**Éthique** : aucun identifiant, aucun pid, aucun appariement individuel écrit ou imprimé ;
taux agrégés uniquement. Aucun appel de modèle, aucun réseau, lecture seule sur `data/`.
Aucun script existant modifié.
