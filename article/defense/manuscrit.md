# Protecting Published LLM Digital Twins: Permutation Fails, Segment Aggregation Bounds Re-identification

<!--
statut: brouillon structuré — PAS un article fini ; aucun gabarit LaTeX, ne compile pas
origine: scission de article/manuscrit.md (branche agent/manuscrit/deux-articles, 13/09/2026), décision du responsable
contenu: (i) cadrage nouveau (titre, résumé, plan, manques) ; (ii) tout le matériel défense sorti de l'article 1, MOT POUR MOT ; (iii) journal : chaque passage de l'article 1 réécrit, dans son état d'origine
chiffres: aucun chiffre nouveau ; les renvois de registre sont ceux du registre resultats/registre-chiffres.csv, partagé avec l'article 1 ; tout chiffre du cadrage nomme son fichier source
ne_pas_toucher: le texte rapatrié ; il se réécrit en passe éditoriale, jamais en silence
-->

## Titre de travail

**Protecting Published LLM Digital Twins: Permutation Fails, Segment Aggregation Bounds
Re-identification.** Compagnon de l'article 1 (`article/manuscrit.md`), qui établit le risque ;
celui-ci porte sur ce qu'un détenteur de panel peut publier.

## Résumé provisoire

*(Brouillon. Chaque chiffre est un renvoi du registre ou nomme son fichier.)*

A companion paper shows that recent LLM digital twins can be linked back to the survey
respondents they were built from. We ask what a panel holder can publish instead. We preregistered
twenty-six defense candidates, each with an adaptive attacker written before measurement
(`resultats/c7-defense-adaptative-preenregistrement.md`). Permutation is a dead end even at its
most favourable case: a joint permutation of whole rows within a demographic segment costs
{{R:defense-permutation-jointe-cout-utilite}} points of utility and leaves adaptive top-1 at
{{R:defense-permutation-jointe-top1-adaptatif}} % {{R:defense-permutation-jointe-top1-adaptatif.ic}},
the undefended level. Our item-wise variant of the Post Randomisation Method (D4) holds the best
attacker we built to {{R:defense-d4-top1-adaptatif-s1}} % {{R:defense-d4-top1-adaptatif-s1.ic}} but
carries no formal guarantee: it republishes the within-segment histogram of
{{R:defense-d4-republication-multiensemble}} % of segment × item pairs. Aggregating by the mode over
k people of a segment is the one lever with a bound — top-1 ≤ 1/k against any attacker — observed at
{{R:defense-mode-k5-top1-adaptatif}} % {{R:defense-mode-k5-top1-adaptatif.ic}} at k = 5 and
{{R:defense-mode-k10-top1-adaptatif}} % {{R:defense-mode-k10-top1-adaptatif.ic}} at k = 10, at a price of
{{R:defense-mode-k5-cout-groupes}} and {{R:defense-mode-k10-cout-groupes}} points on between-segment
differences, against a whole twin-to-human gap of 2.17 points on that component
(`resultats/c7-defense-adaptative-resultats.md` §0). A differential-privacy generator correctly
implemented under zCDP costs the same whether noised or not, so what it measures is the cost of an
independent-per-item architecture, not of the privacy budget (`resultats/c7-dp-zcdp-resultats.md`);
we withdraw the comparison with D4 we had preregistered and claim no superiority in either
direction (`resultats/retractation-dp-d4-2026-09-13.md`).

## Plan de sections

Les renvois « → » désignent le matériel rapatrié plus bas ; « À ÉCRIRE » désigne ce qui n'existe
qu'en rapport de résultats, en français, et doit être rédigé.

1. **Introduction.** Le risque établi par l'article 1 (le citer, ne pas le redémontrer) ; la question
   du détenteur de panel ; les contributions. À ÉCRIRE.
2. **Background.** PRAM, échange de données, données partiellement synthétiques → « 2.6 Defenses » ;
   microagrégation et k-anonymat, confidentialité différentielle pour données synthétiques : À ÉCRIRE
   (voir manques).
3. **Threat model.** Attaquant adaptatif qui connaît le mécanisme ; « garanti » contre « observé » →
   paragraphe « Guaranteed and observed must not be run together » (§6.1) ; source
   `resultats/c7-defense-adaptative-resultats.md` §4.
4. **Candidates and protocol.** Les 26 candidats, le critère de protection préenregistré, les trois
   composantes d'utilité → annexe « The twenty-six defense candidates » ; source §1 et §2 du rapport.
5. **Results.**
   5.1 Permutation : D4 et permutation jointe → §6 (intro), §6.1 ;
   5.2 Agrégation par le mode, borne 1/k et prix → §6.1 ;
   5.3 Dégrader la fidélité individuelle (le λ, prédiction Q3 réfutée) : À ÉCRIRE depuis
       `resultats/c7-defense-adaptative-resultats.md` §3.3, avec ses trois réserves ;
   5.4 Confidentialité différentielle : implémentation zCDP, plancher architectural, comparaison
       retirée → §6.2 et annexe « Costs of the defense » ; source `resultats/c7-dp-zcdp-resultats.md`.
6. **What the defense costs a downstream analyst** → §6.3 et annexe « Analyst cost ».
7. **Retractions, preregistered predictions and limits.** Rétractation D4/DP
   (`resultats/retractation-dp-d4-2026-09-13.md`, `resultats/audit-comparaison-dp-2026-09-13.md`) ;
   les six prédictions Q1–Q6 (`resultats/c7-defense-adaptative-resultats.md` §5) ; lignes 13 et 14 du
   tableau 1 de l'article 1 ; limites → « *Limits.* » du §6.3. À ASSEMBLER.
8. **Discussion** : que publier selon le besoin (statistiques de population ou jumeau individuel). À
   ÉCRIRE.
9. Sections obligatoires PoPETs (éthique, disponibilité, usage d'IA) : reprendre et réduire celles de
   l'article 1. À ÉCRIRE.

## Ce qui manque pour en faire un article

**Littérature à citer** (aucune entrée ajoutée à `article/references.bib` ; chaque référence reste à
trouver et vérifier à la source) :

- microagrégation et k-anonymat, dont l'agrégation par le mode est un cas : Sweeney ; Domingo-Ferrer
  et Mateo-Sanz ;
- divulgation d'attribut au niveau du groupe, que la borne 1/k ne couvre pas : l-diversité,
  t-proximité ;
- échange de données (data swapping) : Dalenius et Reiss ; la littérature du contrôle de la
  divulgation statistique (Hundepool et al.) ;
- confidentialité différentielle pour données synthétiques avec structure jointe : PrivBayes, MST,
  AIM ; la zCDP (Bun et Steinke) ; les évaluations de générateurs DP (compétitions NIST) ;
- attaques contre les données synthétiques déjà citées par l'article 1 et à reprendre :
  `stadler2022groundhog`, `annamalai2024linear`, `giomi2023unified`, `gouweleeuw1998pram`,
  `drechsler2024thirtyyears`, `hu2023microdata`.

**Expériences à ajouter** (aucune n'est lancée ; chacune exige un préenregistrement avant tout
calcul) :

- l'attaque « par différence » contre D4 — l'adversaire qui connaît les autres membres du segment —
  est énoncée mais **jamais mesurée** ;
- la divulgation d'attribut de groupe sous agrégation par le mode, que 1/k ne borne pas ;
- un générateur DP **à structure jointe** (PrivBayes de degré supérieur à 0, MST ou AIM), seul moyen
  de savoir si le plancher mesuré tient à l'architecture indépendante par item ou à la DP ;
- le coût de D4 sur les corrélations **en plusieurs tirages avec intervalle** (la valeur publiée est
  un tirage unique, marqué provisoire au registre) ;
- des intervalles et plusieurs graines sur les coûts d'utilité de l'agrégation et du λ ;
- la défense sur les **autres configurations de jumeaux** publiées de Twin-2K-500, et sur d'autres
  blocs que les items d'achat : elle est testée sur un seul bloc, d'un seul jumeau, d'un seul jeu
  (§6.3, *Limits*) ;
- un attaquant plus fort que le meilleur mesuré : aucun taux observé n'est une borne.

**Autres jeux de données** :

- l'archive Park et al. (items GSS), où l'article 1 montre que le comparateur démographique armé
  également rejoint l'agent : la défense y protège-t-elle d'un risque démographique plutôt que
  jumeau ? ;
- les jumeaux Argyle et al. (2023), au niveau de leur baseline : témoin négatif, la défense ne doit
  rien y changer ;
- tout panel qui publierait jumeaux et réponses appariées ligne à ligne (l'article 1, §7.4, n'en
  trouve pas d'autre) ;
- le réglage d'un gabarit et d'une cible de publication : **aucun gabarit**, donc aucune compilation
  LaTeX pour l'instant.

**Portes du dépôt** : `registre_chiffres.py` (P2), `interdits.py` (P3) et `renvois.py` (P5) n'ont
été conçues que pour `article/manuscrit.md` et `resultats/` ; leur lecture de `article/defense/`
reste à établir avant toute passe éditoriale.

---

## Matériel rapatrié de l'article 1, mot pour mot

*Texte recopié tel qu'il figurait dans `article/manuscrit.md` au commit de départ de la scission
(`e579124`). Les numéros de section et les renvois §N sont ceux de l'article 1 d'origine.*


### 2.6 Defenses

Our D4 is not new. Shuffling answers between units of the same segment is a variant of the
Post Randomisation Method [gouweleeuw1998pram], which perturbs categorical variables through a
known transition matrix leaving margins invariant in expectation, and of data swapping — the same
family as the partially synthetic data tradition of Reiter and Drechsler, extended by Drechsler
[drechsler2024thirtyyears] and Bowen et al. [hu2023microdata]. What is new is the application to
LLM twins with a measured risk-utility curve (§6).

## 6. Defense

Shuffling the purchase answers between people of the same demographic segment (D4) brings
closed-world top-1 from **{{R:twin-top1-ferme-json41-naif-ref-defense}} % {{R:twin-top1-ferme-json41-naif-ref-defense.ic}}** to **{{R:twin-d4-top1-residuel}} %** against the naive, non-adaptive
attack, and to **{{R:defense-d4-top1-adaptatif-s1}} % {{R:defense-d4-top1-adaptatif-s1.ic}}** against the best attacker we measured
(§6.1) — the figure we report as the defense's rate. Per-item distribution and between-segment
differences are preserved **exactly, by construction**, as PRAM predicts, and that exactness is
also the mechanism's central limitation: shuffling item by item within a segment leaves each
item's within-segment multiset identical, so D4 republishes that histogram without noise, and an
adversary who knows a segment's other members recovers the target's 40 answers by difference.
**D4 offers no formal privacy guarantee.**

**The cost is not a single average.** By component: **0.0 points on the per-item distribution and
0.0 on group differences — which is that republication, not a cost avoided** — and **{{R:defense-d4-cout-correlations}} points on
inter-item correlations** — a **single permutation draw, not a ten-seed average**, the highest of
ten, kept as published and marked provisional. The ten-draw mean also exceeds the
{{R:dp-zcdp-plancher-correlations}} points of amplitude there was to destroy, so the component is
destroyed in full either way. We therefore withdraw the summary presenting D4's cost *as* a single
mean of 1.47 points: two of the three components are zero by construction, so that mean divides by
three an effect falling entirely on the third. And the cost is worse than that summary suggested:
against the real human answers `erreur_correlations_hum` degrades by
**{{R:defense-d4-aggravation-ecart-humain}} %** — the defended twin moves *away* from the humans on
correlations, so no framing in which the cost is absorbed by an error already present is correct.

Alternatives: D1 (k=10 aggregation) gives 0.55 % for 3.8 points across all three components; D2
(noise) never descends below 1 %.

### 6.1 The defense against a strong, then an adaptive attacker

The figure above was measured against the naive attack, which §5.8 shows can badly understate
leakage. We re-ran it against the strong attack recalibrated on the *defended* outputs, then
against an attacker who knows the mechanism and which items it leaves untouched. D4 holds: top-1
goes from 0.13 % (naive) to **0.24 %** under the recalibrated strong attack, and the **adaptive**
attacker plateaus at **{{R:defense-d4-top1-adaptatif-s1}} %** (strategy S1, leaving the 20 opinion
items intact) — two orders of magnitude below the 20.7 % undefended rate, and never above 1 %.
**Attribute disclosure is not demonstrated either**: the best strategy names the correct `S_gra`
segment in **7.7 %** of cases, against **12.6 %** for always answering the most frequent segment —
the attack does worse than not attacking.

**A reservation that bounds the guarantee.** This residue comes *entirely* from the 20 opinion
items D4 does not permute: the guarantee holds for this split, not for a design leaving a more
informative block untouched. On those 20 items alone the defended and the **undefended** twin are
indistinguishable — {{R:defense-d4-top1-opinion-naif}} % {{R:defense-d4-top1-opinion-naif.ic}} against 0.260 %, on intervals that almost
coincide — so the residue is not a residue of the defense but the part of the publication it never
touches. None of these rates is a bound on the defense; they are the rates of the attacks we
built.

**Shuffling is a dead end, shown at the case most favourable to it; aggregation is the lever, and
it carries a bound.** We preregistered twenty-six defense candidates, each with its adaptive
attacker written before measurement. A **joint** permutation of whole rows within a segment — the
best case for the family D4 belongs to — costs
{{R:defense-permutation-jointe-cout-utilite}} points on all three utility components at once and
leaves adaptive top-1 at {{R:defense-permutation-jointe-top1-adaptatif}} %
{{R:defense-permutation-jointe-top1-adaptatif.ic}}, the undefended level: a permutation hides the
**index**, never the **content**, and our attacker never used the index. The one candidate that
passes and carries a guarantee is **within-segment aggregation by the mode over k people**:
adaptive top-1 {{R:defense-mode-k5-top1-adaptatif}} % {{R:defense-mode-k5-top1-adaptatif.ic}} at
k = 5 and {{R:defense-mode-k10-top1-adaptatif}} % {{R:defense-mode-k10-top1-adaptatif.ic}} at
k = 10, under the combinatorial bound **top-1 ≤ 1/k, against any attacker, with no assumption** —
the k published rows of a group being identical, at most one of its k members can rank first.
**The price is announced with it**: {{R:defense-mode-k5-cout-groupes}} and
{{R:defense-mode-k10-cout-groupes}} points of error on between-segment differences, where the
whole gap between the twin and the humans on that component is 2.17 points; the aggregation
destroys the group statistics it was meant to save. **Guaranteed and observed must not be run
together.** Only top-1 ≤ 1/k is a bound, and it bounds **re-identification, not privacy**:
publishing a group's mode discloses that mode, which 1/k does not cover. Every other rate here,
D4's included, is the rate of an attack we built against a mechanism we built, and the best
attacker measured is not the best attacker possible. **We claim no superiority of any empirical
mechanism over differential privacy, in either direction** (§6.2). *(Preregistered before
measurement; audit of 13 September 2026.)*

### 6.2 Differential privacy: a comparison we withdraw

We preregistered that at a moderate budget differential privacy would be dominated by D4, and
reported that prediction as refuted. **We withdraw the comparison and its verdict: we did not
compare the cost of differential privacy to D4's.** Our reference implementation was too weak on
two counts: it used the Laplace mechanism under basic sequential composition, where the Gaussian
mechanism composed under zCDP (delta = 1e-6) injects **{{R:dp-zcdp-rapport-bruit-eps3}} times less
noise** at the same eps = 3; and it fitted the generator on the humans while scoring it against
the twin, charging it the gap between those two references, worth
**{{R:dp-zcdp-ecart-humains-jumeau-distribution}} points** of distribution error on its own.

Corrected on both counts, over these 2,058 people and ten replicates, a synthetic generator with
independent per-item marginals costs the same on distribution error and on between-segment
differences whether noised at eps = 3, at eps = 10, or **not noised at all**. What we measured is
therefore the cost of the independent-per-item architecture; the marginal contribution of the
privacy budget is **at most {{R:dp-zcdp-contribution-budget-eps3}} point** at eps = 3 and
indistinguishable from zero at eps = 10. On correlations the DP generator preserves **none** of
the amplitude to be preserved. Every figure, budget by budget, is in the appendix. D4 for its part
carries **no formal guarantee** — it republishes each item's within-segment histogram exactly
(**{{R:defense-d4-republication-multiensemble}} %** of segment × item pairs, §6) — and its zero
distribution and group errors are that republication, not an advantage. **We set no top-1 rate of the two
mechanisms against each other**: ours measures one fixed attacker, and the DP generator's is at
chance. **We claim no superiority of D4 over differential privacy** — only a different trade-off,
carrying no guarantee, against the particular attack we built.

**What survives is architectural, and a theoretical point.** The floor is not budgetary: the
non-private control pays the same price, so a per-item independent synthesiser cannot carry this
questionnaire's joint structure at any epsilon. And DP protects an individual's *membership*
behind a published statistic, where our attack assumes the person already known — her profile
being the twin's input — and asks whether **the output conditioned on her** links back: record
linkage, not membership. The DP generator escapes it only by **never conditioning on an
individual**, that is by refusing the twin's task (its individual fidelity stays at most 0.2 points
at every budget, including infinite). A panel holder who needs population statistics should use DP;
one who needs a per-person twin cannot get one here at any epsilon.

### 6.3 What the defense costs a downstream analyst

A defense is usable only if the analyses people actually run survive it. We measured three on the
same 2,058 persons. **Identical — and that identity is the artifact, not a utility preserved**:
group comparisons are the exact republication of the within-segment histogram that makes D4's
distribution and group costs zero (§6). Demographic regression coefficients keep their sign and
significance. **Destroyed**: purchase-item coefficients significant in the raw twin become
non-significant after D4, and the first principal component of the 40 purchase items has a large
share of its loadings **inverted** relative to humans, against none for the raw twin (the
appendix). **The honest comparison.** The unprotected twin was already wrong — it inverts the sign
of the male-female gap and loses PC1+PC2 variance (the appendix) — and D4 adds **3.5 points**,
less than the error already present; but the axis inversion is **D4's own doing**, changing *which*
items compose the structure more than its strength. Under D4, group comparisons are unchanged
*because they are republished unchanged*, predominantly demographic regressions remain reliable,
and anything resting on the link between two answers of the same person becomes unusable.

*Limits.* Tested on a single block, of a single twin, of a single dataset.

### Appendices moved with the defense

**Defense, secondary values (§6, §6.1).** D4 leaves the within-segment multiset of each item
identical on 1,560 of 1,560 segment × item pairs. Against the adaptive attacker, segment-invariant
strategy S3 alone gives 0.05 %; naming the correct `S_gra` segment is at 6.8 % by chance.

**The twenty-six defense candidates (§6.1)** — `resultats/c7-defense-adaptative.csv`, with
`resultats/c7-defense-adaptative-preenregistrement.md` committed before any measurement. Each
candidate was published with its adaptive attacker *before* measurement, and each is scored against
the same preregistered protection criterion, the lower bound of the demographic baseline. Against
the joint whole-row permutation the naive Hamming attacker and a recalibrated A-LLR both return
near-zero, which is precisely why neither is the rate to publish: only the content-linking attacker,
which never consults the index, reveals that the published tables are identical **as sets** to the
undefended ones. Mode aggregation also costs distribution error and correlation error beside the
between-segment figures quoted in §6.1, and both costs grow with k. The bound top-1 ≤ 1/k follows
from the mode being a symmetric function of the group's multiset: the k published rows are
identical, so any attacker assigns the same ranking of humans to all k members.

## Costs of the defense

**Differential-privacy costs, budget by budget (§6.2).** The generator costs
**{{R:dp-zcdp-distribution-eps10}} to {{R:dp-zcdp-distribution-eps3}}** points of distribution
error and **{{R:dp-zcdp-groupes-eps3}} to {{R:dp-zcdp-groupes-eps10}}** points on between-segment
differences; with no privacy at all it costs {{R:dp-zcdp-distribution-epsinf}} and
{{R:dp-zcdp-groupes-epsinf}} points. The marginal contribution of the budget at eps = 10 is
{{R:dp-zcdp-contribution-budget-eps10}}. On correlations the DP generator scores
**{{R:dp-zcdp-correlations-eps10}} to {{R:dp-zcdp-correlations-eps3}}** where the amplitude to be
preserved is **{{R:dp-zcdp-plancher-correlations}}**.

**Analyst cost, the raw twin's own error (§6.3).** The unprotected twin inverts the sign of the
male-female gap (+0.010 against −0.047 in humans) and loses 5.3 points of PC1+PC2 variance. Group
comparisons match to 16 decimal places between the raw and the defended twin, which is the same
exact republication of the within-segment histogram that makes D4's distribution and group costs
zero; on a PCA of the 40 purchase items, 45 % of the first component's loadings are inverted
relative to humans after D4, against 0 % for the raw twin.

---

## Journal de la scission : passages de l'article 1 réécrits, dans leur état d'origine

*Chaque entrée donne le lieu, le texte d'origine puis le texte qui le remplace dans l'article 1.
Les blocs sont en code pour qu'aucune porte ni aucun rendu ne les prenne pour du texte courant.*

**Titre (ligne 1)**

Avant :

```text
# Linkability of LLM Digital Twins: From Chance in 2023 to 60 % in an Open World, and the Control That Says When Not to Measure
```

Après :

```text
# Linkability of LLM Digital Twins: Recent Twins Re-identify the People They Were Built From, Where 2023 Twins Stay at Their Demographic Baseline and Classical Generators Do Not
```

**Résumé, dernière phrase (lignes 51-55)**

Avant :

```text
Finally, a 1998 mechanism (PRAM) applied to twins brings closed-world top-1 to **0.29 %**
[0.10 ; 0.53] against the best attacker we measured — one who knows the mechanism and attacks the
block it leaves untouched — at a measured cost of 4.4 points on inter-item correlations. It
carries **no formal guarantee**: it republishes each item's within-segment histogram exactly, so
its zero distribution and group errors are that republication, not a cost avoided.
```

Après :

```text
Finally, permuting a twin's answers within a demographic segment does not protect against an
adaptive attacker, whereas aggregating a segment's twins by groups of k bounds top-1 by 1/k
against any attacker, at a cost we state (§6); we withdraw our preregistered comparison with
differential privacy.
```

**§1.3, contribution (6) (lignes 188-196)**

Avant :

```text
**(6) Twenty-six defenses, each measured against an adaptive attacker written before the
measurement, and one of them bounded.** Permutation — the family our variant of the 1998 Post
Randomisation Method [gouweleeuw1998pram] belongs to — is a dead end even in its most favourable
case; within-segment aggregation by the mode holds adaptive top-1 under a combinatorial 1/k that
binds any attacker, at a cost in between-segment statistics that we publish beside it (§6.1).
Every rate we report other than that bound, our PRAM variant's included, is the rate of an attack
we built: it offers **no formal guarantee** and republishes the within-segment item histogram
exactly (§6). We preregistered a comparison with differential privacy and **withdraw it**; we
claim no superiority over differential privacy in either direction (§6.2).
```

Après :

```text
**(6) Consequences for publication, developed in a companion paper.** Permutation does not
protect, even in its most favourable case; within-segment aggregation by the mode bounds top-1
by 1/k against any attacker, at a cost in between-segment statistics that we publish beside it;
our variant of the 1998 Post Randomisation Method carries **no formal guarantee**; and we
withdraw our preregistered comparison with differential privacy (§6).
```

**§2.6 Defenses (lignes 306-313)**

Avant :

```text
(sorti en entier : voir « Matériel rapatrié », §2.6)
```

Après :

```text
(supprimé de l'article 1)
```

**§6 entier (lignes 882-1004)**

Avant :

```text
(sorti en entier : voir « Matériel rapatrié », §6)
```

Après :

```text
## 6. Consequences for Publication

Defenses are developed in a companion paper; we state here only what a panel holder needs, and
what we withdraw. **Permuting answers does not protect.** A joint permutation of whole rows
within a demographic segment — the case most favourable to the family of the Post Randomisation
Method [gouweleeuw1998pram] — costs {{R:defense-permutation-jointe-cout-utilite}} points of
utility and leaves top-1 against an adaptive attacker at
{{R:defense-permutation-jointe-top1-adaptatif}} % {{R:defense-permutation-jointe-top1-adaptatif.ic}},
the undefended level: a permutation hides the index, never the content. Our item-wise variant,
D4, stays at 0.24 % under the strong attack recalibrated on its outputs and at
{{R:defense-d4-top1-adaptatif-s1}} % {{R:defense-d4-top1-adaptatif-s1.ic}} against an adaptive
attacker, but it offers **no formal guarantee**: it republishes each item's within-segment
histogram exactly ({{R:defense-d4-republication-multiensemble}} % of segment × item pairs), so
its zero distribution and group costs are that republication, not a cost avoided, and we
withdraw the summary that gave its cost as a single mean of 1.47 points. **Aggregating by the
mode over k people of the same segment protects, with a bound**: adaptive top-1 falls to
{{R:defense-mode-k5-top1-adaptatif}} % {{R:defense-mode-k5-top1-adaptatif.ic}} at k = 5 and
{{R:defense-mode-k10-top1-adaptatif}} % {{R:defense-mode-k10-top1-adaptatif.ic}} at k = 10, under
top-1 ≤ 1/k against any attacker — a bound on re-identification, not on privacy, since the
published mode is itself disclosed. The price is {{R:defense-mode-k5-cout-groupes}} and
{{R:defense-mode-k10-cout-groupes}} points of error on between-segment differences, where the
whole gap between the twin and the humans on that component is 2.17 points. **We withdraw the
comparison with differential privacy that we preregistered and first reported** (Table 1, row
14): our reference generator was fitted on the humans but scored against the twin, and we claim
no superiority of any mechanism over differential privacy, in either direction.
```

**§4.3, renvoi (ligne 414)**

Avant :

```text
**adaptive** attacker, used only against the defense (§6.1), additionally knows the mechanism and
```

Après :

```text
**adaptive** attacker, used only against the defense (§6), additionally knows the mechanism and
```

**§7.1, renvoi (ligne 1014)**

Avant :

```text
were measured (§5.1, §5.3, §5.4, §5.5, §5.7, §6.1), so this count reads without the table. The
```

Après :

```text
were measured (§5.1, §5.3, §5.4, §5.5, §5.7, §6), so this count reads without the table. The
```

**§7.1, renvoi (ligne 1031)**

Avant :

```text
budget is **withdrawn, not decided** — the comparison behind it was retracted (§6.2).
```

Après :

```text
budget is **withdrawn, not decided** — the comparison behind it was retracted (§6).
```

**§7.1, renvois (ligne 1034)**

Avant :

```text
further outcomes were partial and count as neither (§5.7, §6.3); one held outright, P2 (§6.1);
```

Après :

```text
further outcomes were partial and count as neither (§5.7, §6); one held outright, P2 (§6);
```

**§8, renvoi (ligne 1226)**

Avant :

```text
correlations (5.775 → 9.709), and the loss of every inter-item analysis downstream (§6.3) — and
```

Après :

```text
correlations (5.775 → 9.709), and the loss of every inter-item analysis downstream (§6) — and
```

**§8, renvoi (ligne 1230)**

Avant :

```text
split that shuffles the informative block (§6.1). (f) Differential privacy where the published
```

Après :

```text
split that shuffles the informative block (§6). (f) Differential privacy where the published
```

**§8, renvoi (ligne 1232)**

Avant :

```text
cost relative to (e), having withdrawn the comparison we preregistered (§6.2).
```

Après :

```text
cost relative to (e), having withdrawn the comparison we preregistered (§6).
```

**§9, renvoi (ligne 1290)**

Avant :

```text
**Differential-privacy implementation (§6.2).** The synthesiser was written by hand rather than
```

Après :

```text
**Differential-privacy implementation (§6).** The synthesiser was written by hand rather than
```

**§9, renvoi (ligne 1296)**

Avant :

```text
`S_gra` covariate are not protected. These are reasons the comparison of §6.2 is withdrawn rather than
```

Après :

```text
`S_gra` covariate are not protected. These are reasons the comparison of §6 is withdrawn rather than
```

**§9, renvoi (ligne 1301)**

Avant :

```text
not the one described in this paragraph, that supplies every figure of §6.2. The withdrawal stands
```

Après :

```text
not the one described in this paragraph, that supplies every differential-privacy figure of the companion paper (§6). The withdrawal stands
```

**Annexe, « Defense, secondary values » (lignes 1417-1419)**

Avant :

```text
(sorti en entier : voir « Matériel rapatrié », annexes)
```

Après :

```text
(supprimé de l'article 1)
```

**Annexe, titre (ligne 1526)**

Avant :

```text
## Detail behind the five audits of 13 September 2026
```

Après :

```text
## Detail behind the four audits of 13 September 2026
```

**Annexe, phrase d'ouverture (ligne 1528)**

Avant :

```text
Each of the five audits below is published with its preregistration, its script and its result CSV;
```

Après :

```text
Each of the four audits below (a fifth, on the defense candidates, moved to the companion paper) is published with its preregistration, its script and its result CSV;
```

**Annexe, « The twenty-six defense candidates » (lignes 1546-1556)**

Avant :

```text
(sorti en entier : voir « Matériel rapatrié », annexes)
```

Après :

```text
(supprimé de l'article 1)
```

**Annexe « Costs of the defense » (lignes 1603-1619)**

Avant :

```text
(sorti en entier : voir « Matériel rapatrié », annexes)
```

Après :

```text
(supprimé de l'article 1)
```

**Tableau 1, ligne 14, renvoi (ligne 1654)**

Avant :

```text
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Withdrawn, not decided.** The comparison is retracted: the DP generator was fitted on the humans and scored against the twin, and at eps = ∞ — no privacy — the cost was already the same (§6.2) | `audit-comparaison-dp-2026-09-13.md` |
```

Après :

```text
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Withdrawn, not decided.** The comparison is retracted: the DP generator was fitted on the humans and scored against the twin, and at eps = ∞ — no privacy — the cost was already the same (§6) | `audit-comparaison-dp-2026-09-13.md` |
```

**Références, clé plus citée (ligne 1674)**

Avant :

```text
`peng2026funhouse`, `guepin2023synthetic`, `shafieinejad2026diffusion`, `drechsler2024thirtyyears`,
```

Après :

```text
`peng2026funhouse`, `guepin2023synthetic`, `shafieinejad2026diffusion`,
```

**Références, clé plus citée (ligne 1675)**

Avant :

```text
`hu2023microdata`, `aapor2026responsibleai`.
```

Après :

```text
`aapor2026responsibleai`.
```
