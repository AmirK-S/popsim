# Audit des chiffres avant gel — 12 septembre 2026

Dernier contrôle avant gel. Objet : vérifier que chaque chiffre du manuscrit correspond à sa
source primaire (rapport ou CSV, pas seulement la synthèse), et que manuscrit et synthèse ne se
contredisent nulle part. Aucun appel d'API, aucune recherche web, aucun commit.

Fichiers modifiés : `article/manuscrit.md`, `resultats/article-synthese.md`,
`resultats/conformite-popets-2026-09-12.md`, `REPRISE-2026-09-12.md`, et ce rapport.
Non touchés : `article/latex/`, `resultats/c7-*` (agents en cours).

---

## 1. Les cinq points prioritaires

### 1.1 La fourchette « 20,7 % à 65,7 % » — **retrouvée, et requalifiée**

Les deux bornes existent et sont traçables, **mais leur assemblage en fourchette ne l'est pas**.

- **20,7 %** = top-1 en **monde fermé**, attaque **naïve**, Twin-2K-500, pool de 2 058
  (`c7-compromis-resultats.md`, `c7-echelle-resultats.md`).
- **65,7 %** = top-1 en **monde fermé**, attaque **naïve**, archive Park, condition composite,
  pool de 1 052, **mesuré par le script d'origine** (`c7-stanford-resultats.md`). La
  ré-implémentation de `c7-attaquant-fort` donne **65,51 %** pour la même condition.

L'appariement des deux vient de `c7-bits-resultats.md` §2, où il sert à une seule chose :
montrer que **le taux ne voyage pas** d'un jeu à l'autre (facteur 3,2) alors que les bits
normalisés voyagent (facteur 1,34). Ce n'est donc **ni un intervalle de confiance, ni une plage
de valeurs d'une même grandeur** : ce sont deux mesures sur deux jeux différents, à nombre
d'items, entropie par item et plafond humain tous différents.

**Où la fourchette apparaît réellement** : `article-travaux-connexes.md` l. 38 (« notre taux
(20,7 %, 65,7 %) »), `consultant-angles-morts-2026-09-12.md`, et sous la forme voisine
« 36,4 % à 65,7 % » dans `positionnement-vie-privee-2026-09-12.md` l. 18 et 79.

**Où elle n'apparaît pas** : **ni dans `article/manuscrit.md`, ni dans
`resultats/article-synthese.md`, ni dans `article/latex/main.tex`.** Vérifié par recherche
mécanique de `65[,.]7` sur les quatre fichiers. Le manuscrit ne cite 65,7 % qu'une fois
(l. 662), correctement, comme la mesure du script d'origine à côté du 65,51 % retenu.

**Verdict : aucune correction à faire dans le manuscrit, et la fourchette ne doit pas y
entrer.** Elle est doublement périmée : A6 de la synthèse **interdit explicitement** de
comparer 65,7 % et 20,7 % comme deux mesures de la même chose, et le chiffre publié pour Park
est désormais **90,40 %** sous l'attaquant fort, le 65,51 %/65,7 % n'étant plus que la mesure
d'un adversaire faible. Les trois fichiers de travail qui la portent encore sont hors de mon
périmètre d'écriture ; ils sont signalés ici.

### 1.2 Compteur de réfutations — **QUINZE**, recompté ligne à ligne

Recomptage mécanique du tableau du manuscrit (§7.1) : **17 lignes**, dont **15 « Refuted »** et
**2 « inconclusive »** (lignes 9 « call granularity » et 16 « top-1 > 5 % »).

Reconstitution de l'historique de la nuit, qui explique les trois valeurs :

| étape | compte | cause |
|---|---|---|
| départ | 16 | tableau à 16 lignes, toutes « réfutée » |
| −2 | **14** | lignes 9 et 16 requalifiées « non concluantes » : un IC bootstrap percentile sur zéro succès ne peut rendre que « [0 ; 0] », artefact arithmétique ; en Clopper-Pearson exact les seuils préenregistrés tombent **dans** l'intervalle ([0 ; 11,57 %] à n=30, [0 ; 30,85 %] à n=10) |
| +1 | **15** | ajout de la ligne 17 : T2 (pipelines réellement indépendants) testée et **réfutée** (`c7-deux-organisations-resultats.md`) |

Le manuscrit portait déjà « Fifteen » en trois endroits (résumé, §1.3, titre de §7.1) — **il
était juste**. C'est la **synthèse** qui était restée à « quatorze », et `REPRISE` à
« 16 à 14, pas encore appliqué ». Les deux sont corrigées.

**Piège à ne pas confondre**, et conservé tel quel car chaque chiffre est exact : §7.3 du
manuscrit cite « 25 confirmed and 15 refuted » — c'est le **recensement de
`c7-multiplicite.md`** sur 47 tests, un objet différent dont le total coïncide par hasard avec
celui du tableau. Le texte dit déjà pourquoi les deux ne portent pas les mêmes totaux.

### 1.3 `conformite-popets-2026-09-12.md` — quatre verdicts périmés, corrigés

Le rapport déclarait « références non vérifiées » : **faux depuis cette nuit**.
`article/references-verification.md` enregistre l'audit des **45 entrées** (27 reprises d'une
vérification antérieure, 18 vérifiées à la source dans la passe du 12/09), avec deux
identifiants arXiv et deux attributions d'auteur corrigés, et un contrôle croisé confirmant que
**les 41 clés citées dans le manuscrit correspondent toutes à un travail présent dans le
`.bib`** — donc aucune référence hallucinée, qui était le motif de rejet de bureau visé.

En vérifiant ce point, trois autres verdicts du même rapport se sont révélés également périmés
et ont été corrigés dans la même passe (**ne corriger que ce qui est faux** s'applique aussi à
un rapport qui accuse à tort) :

| § | verdict avant | verdict après | preuve |
|---|---|---|---|
| 1 | Références non vérifiées, NON CONFORME | CONFORME (reste 13 clés à réorthographier) | `article/references-verification.md` |
| 2 | Longueur INCONNUE | CONFORME, 10 pages sur 12 | compilation réelle ; corps 10 055 mots |
| 3 | Section « AI use » absente | CONFORME, §10, 294 mots | `manuscrit.md` l. 1040–1068 |
| 5 | Scories `[OPEN ITEMS]` à retirer | CONFORME, retirées | `grep "OPEN ITEMS"` sans résultat |
| 7 | Cadrage IRB « manque non résolu » | CONFORME, position affirmée | §8, « Ethics review and scope » |

Les numéros de ligne cités dans les points 9 à 12 de ce rapport ont dérivé avec les réécritures
de la nuit ; leurs verdicts (tous CONFORME) restent valides, seules les références de ligne sont
approximatives.

### 1.4 `REPRISE-2026-09-12.md` — ligne de coût fausse, corrigée

Avant : « le coût réel de la nuit dépasse largement 0,55 USD ; aucun rapport lu ne donne de
total consolidé fiable — à recalculer ». Le total **a été** consolidé depuis, dans
`resultats/cout-api-2026-09-12.md` :

- **compteur du fournisseur** (deux lectures `total_usage` encadrant la période, nuit + queue
  R6) : **9,969 USD** ;
- **somme des coûts déclarés**, 6 expériences : **9,921 USD** (9,928 USD avec la queue R6) ;
- écart 0,041 USD (~0,4 %), attribué aux arrondis à 4 décimales ; recoupement indépendant par
  `GET /key` cohérent à 0,03 USD près.

Le « 0,55 USD » était `c7-deux-organisations` seul, le « 4,99 USD » `c7-fort` seul : deux
lignes, jamais un total.

### 1.5 Top-1 du témoin apparié — **31,6 %**, un seul chiffre dans les livrables

Trois valeurs circulent pour la même grandeur (top-1 du nul de marge, défaut l. 133 corrigé,
JSON Persona GPT4.1) :

| valeur | provenance | statut |
|---|---|---|
| **31,6 %** (31,62 %) | `audit-renversement-2026-09-12.md`, tableau l. 110 | **fait autorité** |
| 31,15 % | `c7-nul-corrige-reponse-audit.md` l. 50, 72 | ré-implémentation indépendante du même objet |
| 31,90 % | `c7-tautologie-resultats.md` l. 82, condition (a) | **objet différent** — témoin de tautologie, pas le nul de marge |

Le **manuscrit utilise 31,6 % aux quatre occurrences** (l. 34, 75, 396, 404) et la synthèse aussi
— **aucune correction nécessaire dans les livrables**. Deux occurrences fautives ailleurs :
`REPRISE` l. 80 portait « 31,1 % contre 20,7 % » (corrigé en 31,6 % contre 20,73 %), et la
**légende gravée dans `article/figures/fig2-couplage.png` cite « 31.15 % »** — non corrigeable
sans régénérer la figure, signalé au §3.

---

## 2. Corrections appliquées

Vingt corrections. Aucune ne change un verdict scientifique : **seize sont des erreurs de
référence interne, de compte ou de statut périmé ; quatre touchent un chiffre**, toutes dans le
sens de l'exactitude.

### `article/manuscrit.md` (10)

| # | ligne | avant | après | source qui tranche | gravité |
|---|---|---|---|---|---|
| 1 | 144 | `(Table 3, §7.1)` | `(Table 1, §7.1)` | le manuscrit ne contient **qu'un seul tableau** ; la compilation le numérote Table 1 | moyenne (renvoi faux) |
| 2 | 354 | `every refuted prediction in Table 3` | `… in Table 1` | idem | moyenne |
| 3 | 883 | `why Table 3 and the census` | `why Table 1 and the census` | idem | moyenne |
| 4 | 131 / 136 | contributions numérotées **(1)(2)(3)(4)(6)(5)** | **(1)(2)(3)(4)(5)(6)** | numérotation interne incohérente, visible au premier coup d'œil | moyenne |
| 5 | 134 | strong attack renvoyé à `(§5.2, §5.3)` | `(§5.3, §5.8)` | le passage 65,51 → 90,40 % sur Park est établi en **§5.8**, pas en §5.2 | moyenne (renvoi faux) |
| 6 | 731 | `the naive attack, which §5.2 shows to be weak` | `… which §5.8 shows can badly understate leakage` | §5.2 ne montre pas la faiblesse de l'attaque naïve (écart Twin 20,7 → 23,23 %) ; c'est §5.8 qui l'établit, sur Park | moyenne |
| 7 | 620 | `per-item call 0.00 % [0 ; 30.8]` | `[0 ; 30.85]` | valeur exacte Clopper-Pearson `preenregistrements-recueil-2026-09-12.md` l. 389/452 ; « 30.8 » **tronquait** la borne haute vers le bas | faible |
| 8 | 819 (tableau, ligne 9) | `[0 ; 30.8] at n=10` | `[0 ; 30.85] at n=10` | idem | faible |
| 9 | 569 | `identify 46× less` (ratio nu, sans IC) | ajout : `top-1 0.24 % [0.07 ; 0.46] … against 11.0 % [9.9 ; 12.3]` | `c7-mecanisme-resultats.md` l. 10-11 ; le ratio 46 n'est nulle part dans la source, il est recalculé — les deux valeurs qui le produisent portent un IC | faible |
| 10 | 507 | `top-10 approximately 45–46 %` | `46.4 % [43.6 ; 49.4]` et `45.2 % [42.3 ; 48.1]`, source corrigée vers le CSV | `c7-transfert-stanford-attaque.csv` l. 2-3 ; le rapport cité ne contient aucun top-10 | faible |
| 11 | 767 | `individual fidelity stays **under** 0.2 points` | `stays **at most** 0.2 points` | `c7-dp-resultats.md` l. 13 : la valeur à eps = ∞ est **exactement** +0,20 | faible |

### `resultats/article-synthese.md` (3)

| # | avant | après | source |
|---|---|---|---|
| 12 | « Compte de réfutations : corrigé de **seize à quatorze** », INTERDIT « seize » | « seize → quatorze → **quinze** », recomptage 17 lignes / 15 réfutées / 2 non concluantes, INTERDIT « seize » **et** « quatorze » | `c7-deux-organisations-resultats.md` (T2 réfutée) + recomptage du tableau |
| 13 | A9 `[0 ; 30,8]` | `[0 ; 30,85]` | idem correction 7 |
| 14 | spécifications des figures 1 et 2 (§5) décrivant des réglages **non livrés** | note datée : les fichiers livrés font foi, écarts listés, et défaut « 31.15 % » de fig2 signalé | inspection des deux PNG produits ; les légendes du manuscrit décrivent les figures réelles |

### `REPRISE-2026-09-12.md` (4)

| # | avant | après | source |
|---|---|---|---|
| 15 | « compteur passe de **16 à 14**, pas encore appliqué » | **quinze**, appliqué, avec les deux mouvements distingués | recomptage du tableau |
| 16 | « coût réel dépasse 0,55 USD, aucun total fiable » | **9,969 USD** au compteur / **9,921 USD** déclarés | `cout-api-2026-09-12.md` |
| 17 | « nul de marge … **31,1 %** contre 20,7 % » | **31,6 %** contre **20,73 %** | `audit-renversement-2026-09-12.md` |
| 18 | « Pas encore fait : biblio non vérifiée, AI Use absente, `[OPEN ITEMS]` à retirer, page count instable » | bloc « Fait depuis » + nouveau reste-à-faire réel | vérifications du §1.3 ci-dessus |

### `resultats/conformite-popets-2026-09-12.md` (2 blocs, 6 verdicts)

| # | contenu | source |
|---|---|---|
| 19 | §1, §2, §3, §5, §7 passés de NON CONFORME à CONFORME ; en-tête (1 087 lignes, corps 7–926) et tableau (17 lignes, Table 1) mis à jour | voir §1.3 |
| 20 | §4 « gabarit LaTeX — le manuscrit est en Markdown, NON CONFORME » → migration faite et compilée, CONFORME sous réserve, avec les trois défauts LaTeX à traiter par l'agent concerné | `article/latex/main.tex` + `main.pdf` du 12/09 ; corps rendu 10 pages sur 12 |

---

## 3. Contradictions non tranchées, ou hors de mon périmètre d'écriture

1. **`article/latex/main.tex` l. 395 : la légende du tableau annonce « The sixteen preregistered
   predictions ».** Le tableau porte 17 lignes et 15 réfutations. La chaîne est **écrite en dur
   par `md2latex.py`**, elle ne dérive pas du Markdown : mes corrections au manuscrit **ne la
   répareront pas** à la prochaine régénération. Les renvois « Table 3 » (l. 117, 203, 441) et
   l'inversion (6)/(5) (l. 111, 113) sont eux recopiés du Markdown et **seront** corrigés
   automatiquement. À traiter par l'agent LaTeX.
2. **Le tableau LaTeX est numéroté automatiquement (`\label{tab:predictions}`) mais référencé en
   dur dans le texte.** Le problème se reproduira à chaque changement de contenu tant que les
   renvois ne passeront pas par `\ref{}`. Signalé comme demandé.
3. **`c7-fort-resultats.md` et `c7-recette-resultats.md` publient encore « [0 ; 0] ».** Le
   manuscrit cite ces deux rapports pour des valeurs Clopper-Pearson qu'ils **ne contiennent
   pas** ([0 ; 11,57], [0 ; 8,8], [0 ; 30,85]) : les corrections prescrites par
   `c7-a9-correction-2026-09-12.md` §3.1–3.2 ont été appliquées au manuscrit et à la synthèse,
   **jamais aux rapports sources**. Le manuscrit est juste, sa traçabilité ne l'est pas. Fichiers
   hors périmètre.
4. **Deux sources mesurent la même grandeur et ne s'accordent pas : 31,62 % contre 31,15 %.**
   `audit-renversement` fait autorité (et note que son 31,6 % « recoupe indépendamment les
   31,9 % de `c7_tautologie` »), mais `c7-nul-corrige-reponse-audit` est une ré-implémentation
   indépendante du **même** objet qui mesure 31,15 %, soit un demi-point d'écart, et **rien dans
   le dépôt ne réconcilie les deux implémentations**. Je ne tranche pas : je constate que
   l'écart est sans effet sur le verdict (le témoin fuit plus que le jumeau réel à 20,73 %
   quelle que soit la valeur retenue), et que la valeur désignée comme faisant autorité est bien
   celle qui figure partout dans les livrables.
5. **La légende gravée dans `article/figures/fig2-couplage.png` cite « 31.15 % ».** Elle
   contredit le texte du manuscrit (31,6 %) sur la même page. Non corrigeable sans régénérer la
   figure — hors de mon périmètre (`analyses/`), signalé dans la synthèse et dans `REPRISE`.

---

## 4. Contrôles passés sans correction

- **Formulations interdites** : recherche mécanique des interdits de la synthèse sur le
  manuscrit (« 25× », « 93.25 » comme résultat, « 26.11 », moyenne de 1,47 comme coût, minorant
  appliqué à nos jumeaux, causalité fidélité→fuite, « un seul axe », fuite traversant les
  vagues, défense supérieure à la DP, témoin « sans structure individuelle »). **Aucune
  violation.** Les six occurrences trouvées sont toutes des **retraits explicites** (« is
  withdrawn », « we do not claim ») ou des usages autorisés par la synthèse elle-même (les bits
  comme minorant, A4 ; le 44,7 % comme minorant, A6 ; le 1,47 dans la seule comparaison à la DP,
  A12).
- **Gain de l'attaquant fort sur Twin** : jamais présenté comme établi. Résumé, §5.3 et la
  légende de la figure 1 portent tous la réserve d'IC chevauchants
  (`c7-fort-monde-ouvert-ic-2026-09-12.md` §4).
- **36,4 % entre organisations indépendantes** : jamais présenté comme tel. Résumé,
  contribution (1), T2 (§3) et §5.4 le qualifient tous d'intra-pipeline, avec le 1,8 % en regard.
- **44,37 % à FPR = 0,1 %** : présenté comme « very unstable estimates, not as measured rates »,
  avec son IC et la mention d'« environ **un** faux positif absolu sur Park et deux sur Twin »
  (§5.3). Conforme à la réserve obligatoire de A3.
- **Le témoin n'est nulle part dit dépourvu de structure individuelle** : « not structure-free »
  au résumé et en §5.1, avec le 31,6 % contre 20,73 % qui le démontre.
- **Renvois internes** : les 60 renvois `§N.M`, les 3 renvois de tableau et les 3 renvois de
  figure ont été vérifiés un à un contre leur cible. Trois étaient faux (corrections 1-3, 5, 6) ;
  les autres pointent juste.
- **Vérification numérique de §5.4 à §6.3** : environ 110 valeurs remontées jusqu'à leur rapport
  ou leur CSV source. **Aucune erreur de valeur ni d'arrondi** hors les quatre corrigées
  ci-dessus.

---

## 5. Solde en mots

| | mots |
|---|---|
| corps avant cette passe (résumé + §1–§7) | 10 021 |
| corps après | **10 055** |
| **solde net** | **+34** |

Les +34 mots sont entièrement dus aux trois ajouts d'exactitude demandés par la consigne
(intervalles de confiance sur H1, sur le top-10 Stanford, et la reformulation du renvoi §5.8) ;
les corrections de renvois et de numérotation sont neutres. La contrainte de longueur ayant été
levée en cours de mission (10 pages sur 12, ~1 005 mots/page, ~2 pages de marge), ce solde est
donné pour la trace et non comme un plafond respecté.
