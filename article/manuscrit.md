# Linkability of LLM Digital Twins: Open-World Rates, a Twin-to-Twin Channel, and a Null That Absorbs Our Own Coupling

*Submission draft, PoPETs. Body target: 12 pages. Bibliography: `article/references.bib`.*

---

## Abstract

Published LLM "digital twins" — per-respondent simulated answer vectors released alongside
survey panels — remain linkable to the humans they were built from. On the Twin-2K-500 panel
(2,058 respondents), the strongest published twin designates the correct respondent in a
closed pool of 2,058 in 23.23 % of cases [21.5 ; 25.0] under a rarity-weighted likelihood
attack whose parameters are estimated out-of-fold, against 0.049 % for chance and under
0.3 % for every non-LLM predictor we tested at comparable marginal accuracy. On the Park et al.
archive (1,052 participants) the same attack reaches **90.40 %** [88.6 ; 92.2], where a naive
agreement attack reached only 65.51 % — our first attack understated that leakage badly. The
rate is not an artifact of the closed pool: in an open world, at a false-accusation rate of 1 %,
the attacker is right 4.28 % of the time on Twin-2K-500 and 60.17 % on the Park archive
(against 3.04 % and 20.39 % for the naive attack), with the statistical baselines at roughly
0 % and a human test-retest ceiling of 54.5 % / 90.7 %. We report a channel with no direct precedent:
two independently constructed twins of the same person designate each other with no real human
answer held by the attacker — 36.4 % top-1 at 60 common items on Twin-2K-500 and 11.9–13.0 %
at 177 common items on the Park archive, against anti-artifact controls of 0.06 % and at most
0.31 %. We also report what we could not establish. We predicted, and preregistered, that the
observed coupling between imitation quality and leakage reflects an individual fingerprint; a
marginal null — 100 predictors carrying only a per-person accuracy margin and no individual
structure at all — reaches a rank correlation at least as high as ours (0.984 mean against
0.969 observed on disjoint items). Sixteen preregistered predictions were refuted; our own
twins failed to reproduce the leakage even when we paid for a frontier model and copied the
per-item call recipe; and the cross-dataset behaviour of the twin-to-twin channel is not
explained by the number of common items. Following Das, Zhang and Tramèr, we built the control
this literature was missing, and it absorbs our own effect. Finally, a 1998 mechanism (PRAM)
applied to twins reduces closed-world top-1 from 20.68 % to 0.13 % at a measured cost of 4.4
points on inter-item correlations, and holds at 0.29 % against an adaptive attacker who knows
the mechanism — while differential privacy, contrary to our own preregistered prediction, is
not dominated by it on aggregate utility.

---

## 1. Introduction

Survey research is beginning to publish *digital twins*: for each human respondent in a panel,
an LLM is conditioned on that person's profile and its simulated answers to the questionnaire
are released as a per-person record. Toubia et al. published 2,058 such twins as Twin-2K-500
[toubia2025twin]. Park et al. built generative agents for 1,052 participants and, citing
privacy, restricted access to the individual responses of those agents [park2024generative].
The privacy question these releases raise has been named — by Park et al. themselves, by
Bonagiri et al.'s normative call [bonagiri2026cognitive], and by the AAPOR task force, which
ranks synthetic response generation as the highest-privacy-risk task it evaluates and names
re-identification by linkage without ever quantifying it — but it has not been measured.

This paper measures it, and reports both what the measurement supports and what it refutes.

### 1.1 What we set out to show, and what happened

Our central hypothesis was that a twin's fidelity to *its particular person* and that twin's
identifiability are expressions of one underlying axis: make the simulation better and you
necessarily make the person more findable. We preregistered a self-refutation test for this
hypothesis. It has two parts. The first part passed: the rank correlation between imitation
quality and leakage survives measuring the two axes on completely disjoint item sets
(Spearman 0.969, 95 % CI [0.937 ; 0.993], 50 stratified random A/B splits of 60 items; 100 %
of splits above 0.7) [c7-disjoint-resultats.md §1]. The relation is therefore not an artifact
of recycled computation.

The second part failed, and it failed against us. We constructed a *marginal null*: 100
artificial predictors possessing nothing but a per-person conditional accuracy margin — no
individual fingerprint, no structure whatsoever beyond "this predictor happens to be better on
this person than on that one". The null reaches a mean Spearman of 0.984, with a 95th
percentile of 1.000 [c7-disjoint-resultats.md §2]. The observed 0.969 does not exceed its own
control; it falls below it. **The coupling is real, robust and measured, but it demonstrates no
individual specificity: a plain global-quality axis already suffices to produce it.**

We report this as a result rather than a confession. A recent line of work argues that an
attack on foundation models proves nothing until the null hypothesis is properly sampled: Das,
Zhang and Tramèr show that blind baselines routinely beat state-of-the-art membership inference
attacks [das2024blind], Duan et al. reach a compatible conclusion [duan2024membership], and a
SaTML position paper makes the methodological demand explicit [satml2025position]. The
quality-leakage coupling reported in prose by Ward et al. [ward2025synthmia] and Byun et al.
[byun2025kdd], and contested by Platzer and Reutterer [platzer2021holdout] and Adams et al.
[adams2025iscience], has never been tested against such a control. We built the control that
was missing, and it absorbs our own effect.

What survives this is not a theory of why twins leak. It is a set of five measurements that do
not depend on the coupling being individual-specific at all.

### 1.2 Contributions

We order these from the least expected to the most.

**(1) A twin-to-twin linkage channel, replicated on two datasets, with no direct precedent.**
Two twins of the same person, produced by different pipelines, designate each other when they
share enough items — while the attacker holds no real human answer of any kind. On
Twin-2K-500: 36.4 % mean top-1 over 30 pairs sharing 60 common items, against an anti-artifact
control (decoy from the same demographic segment) of 0.04 % on those pairs. On the Park
archive: 11.9 % [10.1 ; 13.8] interview→survey and 13.0 % [11.2 ; 14.9] survey→interview at
177 common items, against a control of at most 0.31 %. We never report a single number for
this channel without its common-item count, for reasons developed in §5.4. Anonymeter
[giomi2023anonymeter] formalises "linkability" differently — between two records of the *same*
original dataset, with the attacker already holding *real* attribute values — and concludes
under that definition that linkability is the weakest of the three risks it measures; our
regime is not one they tested.

**(2) A dissociation between memorization and re-identification.** The leakage we measure is
not regurgitation of training data. A model with a training cutoff preceding the panel's
publication (llama31-8b) copies nothing verbatim and leaks no more than models that do copy
[c7-gen-resultats.md]; the pipeline trains nothing on the target population, so no train/test
gap exists to exploit, unlike the setting of Yeom et al. [yeom2018privacy] and Feldman
[feldman2020memorization]; and an ablation localises the signal in the *pattern* of answers
rather than in any answer's content (§5.5). This separates our channel from the memorization
literature [carlini2021extracting] and from the free-text inference literature
[staab2024beyond, ko2026weakcues, lermen2026deanonymization].

**(3) Open-world rates with their human ceiling.** Closed-world 1-in-N rates assume the target
is always in the pool. The defensible measurement removes that assumption and reports true
detections against false accusations (§5.3, Figure 1).

**(4) A defense measured with its real cost, and held against an adaptive attacker.** Not a new
mechanism — a variant of the Post Randomisation Method of 1998 [gouweleeuw1998pram] — but
applied to LLM twins with a risk-utility curve that is measured rather than assumed, reported
with the cost component that a single averaged figure would hide, tested against an attacker who
knows exactly how the defense works, and measured on downstream analyses that a practitioner
would actually run (§6). We also report, against our own preregistered prediction, that
differential privacy is *not* dominated by it on aggregate utility (§6.2).

**(6) An attack strong enough to falsify our own first measurement.** A rarity-weighted
likelihood attack with out-of-fold parameters raises the Park archive's closed-world top-1 from
65.51 % to 90.40 % and triples its open-world rate at 1 % false accusations. We report this as a
correction of our own published figure, not as a new attack paper (§5.2, §5.3).

**(5) A bits-of-identity instrument that transports across datasets where the raw rate does
not.** Presented as a derived instrument, not a discovery: it is a case of Rényi min-entropy
leakage in the sense of Smith [smith2009foundations], in the spirit of Eckersley's surprisal
for browser fingerprints [eckersley2010browser], addressing the same transportability problem
as the κ of Rocher, Hendrickx and de Montjoye's scaling law [rocher2025scaling] by another
route (§5.6).

### 1.3 Negative results, stated in front

Sixteen preregistered predictions were refuted (Table 3, §7.1). Our own twins identify almost
nobody, and the constructive demonstration meant to close that gap — raise fidelity with a
frontier model and watch the leakage return — **failed**: paying for `openai/gpt-4.1` and
copying Twin's per-item call recipe left fidelity at 0.1714 against their 0.708, and top-1 at
0.00 % (§5.7). We still do not know what the Twin-2K-500 recipe does differently, though the
unknown is now narrower: neither the model nor the call granularity. The twin-to-twin channel's cross-dataset behaviour contradicts its
within-dataset behaviour, and we offer no mechanism (§5.4). And the coupling that motivated
this work does not survive its own control (§5.1). We consider a reader who stops here to have
read the paper honestly.

---

## 2. Background and Related Work

### 2.1 Privacy of synthetic data

Stadler, Oprisanu and Troncoso show that generated tabular data remains linkable to its sources
[stadler2022groundhog]. Giomi et al. formalise three attacks — singling out, linkability,
inference — and conclude, on their datasets, that linkability is the weakest risk
[giomi2023anonymeter]. That conclusion is contested: Annamalai, Gadotti and Rocher
[annamalai2024linear], Ganev and De Cristofaro [ganev2025inadequacy, ganev2026rethinking] and
Ganev alone [ganev2024genlaw] show reconstruction attacks defeating distance-to-closest-record
(DCR) metrics; Yao et al. [yao2025dcr] and Meeus et al. [meeus2023achilles] generalise the
critique; Golob, Pentyala and De Cock make these attacks an emerging standard [golob2026sok].

*What distinguishes us.* This corpus concerns tabular microdata from classical generative
models (GANs, copulas, diffusion), evaluated by continuous similarity metrics. Our object is a
vector of categorical answers produced by an LLM conditioned on a person, where no similarity
metric substitutes for a direct matching attack.

### 2.2 Re-identification of real data

Narayanan and Shmatikov re-identify Netflix users [narayanan2008robust]; de Montjoye et al.
show four spatio-temporal points suffice on credit-card metadata [demontjoye2015unique];
Rocher, Hendrickx and de Montjoye model risk on incomplete samples [rocher2019estimating] and
extend it into a scaling law [rocher2025scaling]. Taub, Elliot, Pampaka and Smith ground the
statistical measurement of disclosure risk on synthetic data (CAP, TCAP) on the premise that
synthetic generation breaks the link between identity and datum [taub2018dcap].

*What distinguishes us.* These works re-identify from genuine auxiliary data. In our setting
the attack's input is never a real datum of the target: it is a model output generated from a
persona, compared against the real answers the attacker separately holds. It is precisely the
CAP/TCAP premise that we falsify, on LLM-simulated survey microdata.

### 2.3 Privacy and LLMs

Carlini et al. document memorization and regurgitation of training sequences
[carlini2021extracting]. Staab et al. infer personal attributes from innocuous free text
[staab2024beyond]. Ko et al. de-anonymise online authors by multi-cue agentic inference
[ko2026weakcues] — the closest threatening neighbour — and Lermen et al. demonstrate the same
attack at scale [lermen2026deanonymization]. Theoretically, Yeom et al. connect membership
attacks to overfitting [yeom2018privacy]; Feldman shows memorizing rare cases is necessary for
generalization [feldman2020memorization]; tracing codes [bun2014fingerprinting, dwork2015robust]
are the closest formal parent to our 1-in-N attack, bounding the worst case of an optimal
adversary recovering an individual from aggregate statistics, though in dimension far exceeding
the number of individuals.

*What distinguishes us.* Ko et al., Lermen et al., Carlini et al. and Staab et al. all start
from free text bearing direct semantic cues, aggregated by an agent reasoning over that text.
Our channel is narrower and drier: a vector of closed-choice categorical answers (buys / does
not buy), no free text, no agentic reasoning, and no memorization — established by ablation
(§5.5) and by the cutoff control (§5.7). Unlike Yeom and Feldman, our pipeline trains no model
on the target population.

*On nulls.* Das, Zhang and Tramèr [das2024blind], Duan et al. [duan2024membership] and the
SaTML position paper [satml2025position] establish the methodological precedent for our
marginal null (§5.1).

### 2.4 Respondent simulation and twins

Argyle et al. launched the use of LLMs as panel substitutes [argyle2023out]. Park et al.
restrict access to their 1,052 agents' individual responses on privacy grounds
[park2024generative] — a risk anticipated, never measured. Toubia et al. publish the 2,058-twin
panel we attack, treating neither privacy nor linkage [toubia2025twin]. Peng et al. document
group-fidelity distortions on that same panel without connection to re-identification
[peng2026funhouse]. Bonagiri et al. issue a normative call to evaluate these risks without
measuring them [bonagiri2026cognitive]. None of these works, nor the five surveyed in our
prior-art scan, measures a re-identification rate from twin outputs. That is the gap we fill.

### 2.5 Closest prior art and contradictors

Ward et al. test 13 attacks over 9 generators and 48 tabular datasets, and state in prose a
relation between quality and leakage close to ours [ward2025synthmia]; Byun et al. observe a
near-monotone frontier of the same type without a coefficient [byun2025kdd]. Three differences
separate them from our claim: their quality is *aggregate* (MMD, Jensen-Shannon divergence,
downstream AUC), never a correspondence to the right person; their risk is *membership* in a
training set, not 1-in-N identification; and they publish no coefficient — the only figure in
Synth-MIA is DCR against Max-AUC at r = 0.225, a weak correlation between two aggregate metrics.

Three contradictors hold that fidelity and risk separate: Platzer and Reutterer defend
separability [platzer2021holdout]; Adams et al. conclude a synthetic generator without formal
guarantees preserves fidelity and utility without evident privacy harm [adams2025iscience]; a
2026 preprint observes decoupling where risk grows as quality saturates [anon2026decoupling].
Our response is not that they are wrong: all three measure *aggregate* fidelity, never
individual correspondence to the right person, and — critically — none tests whether the
coupling they observe, or its absence, survives a null built without any individual
fingerprint. Ours does not (§5.1).

### 2.6 Defenses

Our D4 is not new. Shuffling answers between units of the same segment is a variant of the
Post Randomisation Method [gouweleeuw1998pram], which perturbs categorical variables through a
known transition matrix leaving margins invariant in expectation, and of data swapping, which
preserves them exactly at high aggregations — the same family as the partially synthetic data
tradition of Reiter and Drechsler, extended by Drechsler [drechsler2024synthetic] and Bowen et
al. [bowen2023synthetic]. What is new is the application to LLM twins with a measured
risk-utility curve (§6).

---

## 3. Threat Models

We distinguish three scenarios. Only the first is the classical one, and we assume its
strongest objection rather than deflecting it.

### T1 — Panel holder publishes unkeyed twins; attacker holds the real answers

A panel holder releases per-person twin records without the key linking each twin to its
respondent. An attacker who holds **the real answers to the same items** — an insider, a panel
co-owner, a leak of the source file — matches twins to respondents. This is a *linkability*
result in the sense of the Article 29 Working Party and the GDPR, not identification from
public information: the quasi-identifier required is a specific questionnaire, rarely held
outside the panel.

We state plainly what this is not. It does not show that a third party recovers a named person
from public information. And on Twin-2K-500 itself the matching is trivial without any attack —
`pid` equals `TWIN_ID`, and the twin files copy `StartDate`, `EndDate`, `Duration` and
`RecordedDate` line by line from the humans [c7-contre-examen-2026-09-11.md §4]. The result
therefore documents a generic risk for anyone releasing "anonymous" twins without that key, a
practice Twin-2K-500 does not follow.

The objection "this is not real re-identification, the attacker already holds the true answers"
is assumed, not rebutted. Our answers to it are three: the explicit model above, the open-world
measurement of §5.3 which gives the honest number, and T2, which removes the assumption
entirely.

### T2 — Two organisations publish twins of the same cohort; attacker holds nothing real

If several organisations each publish their own twins of the same panel with sufficient item
overlap, a third party cross-references them holding no human answer at all. The attacker's
input is model output on both sides. This threat model has no direct precedent in the
synthetic-data literature: Anonymeter's linkability presumes real attribute values in hand
[giomi2023anonymeter], and Guépin et al. remove the real-auxiliary-data assumption but target
membership in a single generator's training set, never matching between two independent
generations [guepin2023synthetic]. §5.4 measures T2 on two datasets.

### T3 — Pre-publication self-audit

A panel holder wishing to release twins runs the attack against their own file before
publication, to decide whether a defense is required. This is the constructive use of the
method, and the one the artifact (§9) is built to serve.

### Attacker capabilities, all models

The attacker performs no training on the target population, has no query access to the
generating model, and uses only rank-based matching over categorical vectors. Costs are
negligible; the artifact runs the full attack-and-defense loop in roughly 25 seconds on a
laptop without network access.

---

## 4. Data and Methods

### 4.1 Datasets

**Twin-2K-500** [toubia2025twin], 2,058 respondents, public under CC BY 4.0. Target: wave 4,
60 items usable in common out of 108 (40 purchase items of the form "would you buy this product
at this price?", 20 opinion items). Attacker context where applicable: 494 context items from
waves 1–3 plus 14 demographic variables. Chance top-1 in the closed pool is 0.049 %; chance
top-10 is 0.49 %. A human test-retest condition (the same people answering waves 1–3 and wave
4) gives the empirical ceiling: 81.6 % [79.9 ; 83.2] top-1, accuracy 0.745.

**Park et al. archive** [park2024generative], 1,052 participants, 177 common items, replication
package publicly posted. Four agent conditions: composite, interview-only, survey-only,
demographic. Human retest ceiling 96.8 %.

No new data was collected. The attack uses only already-published content.

### 4.2 Methods compared

Twelve heterogeneous methods carry the quality-leakage analysis: 8 LLM twins (JSON Persona
GPT4.1, Text Persona Gemini, JSON mini, Demographics Only, and four further configurations)
and 4 statistical reference points (Demographics Only, B1 argmax over 14 demographics, B2
argmax, PMM k=10). Additional comparators appear in the targeted tests of §5.2: logistic
regression on context, a k=1 donor on context, two individualised *generators* (sampled LR,
Gaussian copula), and an explicitly advantaged k=1 donor fitted directly on the target block.
Sequential CART and a 300-tree forest were tried before that donor and abandoned at 0.45–0.53
accuracy: the retained comparator was not chosen to lose
[c7-synth-ajuste-resultats.md §1].

### 4.3 Metrics

*Attacks.* Two matching rules are used throughout, and every rate is labelled with the one that
produced it. The **naive** attack ranks candidates by Hamming-type agreement over common items.
The **strong** attack (A-LLR) ranks them by a rarity-weighted log-likelihood whose parameters are
estimated **out-of-fold over 5 folds**, so no candidate is scored with parameters fitted on
itself [c7-attaquant-fort-resultats.md]. A third variant (A-MI), weighted by measured per-item
information, scores higher still on the Park archive (93.25 %) but estimates its weights **in
sample** — an advantage declared in the preregistration — so we never report it as our result.
An **adaptive** attacker, used only against the defense (§6.1), additionally knows the defense
mechanism and which items it leaves untouched.

*Closed-world top-1 and top-10*: rank of the true target among all N candidates by the rule
stated. *Open-world*: true-positive rate against false-positive rate,
where the system may decline to accuse (§5.3). *Bits of identity*: log2 of the ratio of correct
one-shot guessing probabilities before and after conditioning on the persona — a Rényi
min-entropy leakage quantity [smith2009foundations]. *Imitation quality*: `fidelite_plancher`,
the share of the human test-retest floor attained.

All intervals are 95 % bootstrap confidence intervals unless stated.

### 4.4 Preregistration and self-refutation

Attack, defense, mechanism, Park et al. archive replication and the disjoint-item test were each
preregistered before computation. We report every refuted prediction in Table 3. The
preregistration plans are not yet third-party timestamped; see `[OPEN ITEMS]`.

### 4.5 Validity controls

*Provenance.* On Twin-2K-500, the context contains 0 wave-4 columns and 0 wave-4 QIDs; maximum
normalised mutual information between context and item is 0.16 against 0.31 for the retest on
the same item. On cells where wave 4 differs from waves 1–3, the JSON 4.1 output equals wave 4
in 37.7 % of cases and waves 1–3 in 37.9 % — symmetric, so no indication of copying. The
randomisation channel is excluded [c7-contre-examen-2026-09-11.md §2].

*Provenance, Park archive.* Over 34,915 cells where the human changed their mind, the composite
follows wave 1 in 41.6 % [40.98 ; 42.26] and wave 2 in 43.2 % [42.60 ; 43.88] — a difference of
−1.6 points, no bias. The 4.3–4.9 point wave-1 bias of the other three conditions holds for the
`demographic` condition too, so it is a shared calibration artifact, not item leakage
[c7-stanford-provenance-resultats.md].

*Empty-run validation.* Uniform ranks yield 0.00 bits; the B0 mode baseline yields
−0.004 [−0.003 ; 0.002] bits.

---

## 5. Results

### 5.1 The coupling, and the null that absorbs it

Across 12 heterogeneous methods, the ordering by imitation quality and the ordering by
re-identification rate nearly coincide: Spearman 0.958 [0.930 ; 0.993], n = 12, on the same 12
items [c7-compromis-resultats.md §1]. It is robust: restricted to LLMs over a narrow fidelity
range, rho = 0.976 [0.952 ; 1.0]; jackknife 0.958–0.986 (§4 of the same source).

The preregistered disjoint-item test measures fidelity on one half of the 60 items and leakage
on the other, over 50 stratified random A/B splits: Spearman **0.969**, median 0.972, 95 % CI
**[0.937 ; 0.993]**, with 100 % of splits above 0.7 [c7-disjoint-resultats.md §1]. Prediction
(a) confirmed — the relation is not an artifact of recycled computation.

Prediction (b) was refuted. The marginal null — 100 artificial predictors having only a
per-person conditional accuracy margin and no structure beyond it — reaches a **higher** rho:
mean **0.984**, 95th percentile **1.000** [c7-disjoint-resultats.md §2]. The observed 0.969
does not exceed the null; it is below it. The coupling demonstrates no individual specificity.
A plain global-quality axis already suffices to produce it.

We therefore do not claim, anywhere in this paper, that a twin's fidelity to its person causes
its leakage, nor that fidelity and identifiability are one axis. We also do not claim that at
equal accuracy every twin leaks more than every predictor: the residuals of the regression on
accuracy do **not** separate the families, with 3 of 7 LLM configurations falling below the
line.

One positive point remains testable outside this circularity: the human point, in raw position
(not normalised by its own value), dominates on both axes — fidelity 0.303, leakage 0.520 —
against 0.154 and 0.067 for the best twin [§3 of the same source]. There is no saturation at
the top of the range.

*Limits.* Twelve points. Raw accuracy is only a noisy proxy (r = 0.72, p = 0.008) for the right
axis. The marginal null has only 12 configurations, which makes Spearman coarse — the null
touches 1.000 through small-sample effects — so the verdict concerns the order of magnitude,
not the third decimal.

### 5.2 Closed-world rates and the comparator question

At comparable marginal accuracy, no non-LLM predictor we tested exceeds 0.3 % top-1 where the
twin reaches 20.7 % [19.1 ; 22.5] under the naive attack, and **23.23 % [21.5 ; 25.0]** under the
strong one [c7-attaquant-fort-resultats.md] — **in a closed world, with the target always present
in a pool of 2,058**. The comparator figures below are naive-attack rates, which makes the
contrast conservative. JSON Persona GPT4.1 attains that rate at accuracy 0.590. The comparators, at
accuracy 0.457–0.511: PMM k=10, 0.23 % [0.06 ; 0.42]; B2 argmax, 0.07 % [0 ; 0.19]; k=1 donor
on context alone, 0.13 %; LR on context, 0.22 % [c7-contre-examen-2026-09-11.md §1]. Two
individualised *generators* — sampled LR and Gaussian copula — give 0.25 % [0.11 ; 0.41] and
0.22 % [0.11 ; 0.36] [c7-generateur-resultats.md], answering the objection that we compare an
individualised generator against predictors that regress to the mean.

We then gave a comparator an explicit advantage: a k=1 nearest-neighbour donor fitted **directly
on the target block's answers** — seeing what the LLM twin never sees. It reaches accuracy
0.584 against the twin's 0.590, carries genuine individual signal (accuracy drops 0.142 under
within-segment permutation, 0.584 true against 0.442 permuted), and despite that advantage
obtains a top-1 of **0.00 % [0 ; 0]** [c7-synth-ajuste-resultats.md §1].

**This claim does not generalise to every leakage metric, and top-10 runs the other way.** That
same advantaged comparator reaches a top-10 of **53.2 % [51.0 ; 55.3]**, *above* the twin's
42.7 % [c7-synth-ajuste-resultats.md §2]. We flag an untested hypothesis that would reconcile
the two: a donor method copying another real person's answer vector probably places that donor
at the top of the ranking, pushing the true target into subsequent ranks — which would explain
a null top-1 alongside a high top-10 without contradicting the accuracy-matched contrast. If
confirmed, such a method would betray not the target but **the donor**: a privacy risk of a
different nature (leakage by third-party copying rather than identification of the target). We
have not tested this.

We do not claim that all individualised prediction identifies, and we do not claim strict
accuracy equality: the generators plateau at 0.476, never 0.590. Neither synthpop/CART (an R
package absent from our environment) nor CTGAN was tested.

### 5.3 Open world — the defensible measurement

Closed-world rates assume the target is in the pool. Removing that assumption gives the number
we consider hardest to attack in review.

At a false-accusation rate of 1 %, the best twin recovers the right person **4.28 %** of the time
on Twin-2K-500 and **60.17 %** on the Park archive under the strong attack. At FPR = 0.1 %:
**1.01 %** and **44.37 %** [c7-attaquant-fort-resultats.md]. Statistical comparators
(Demographics Only, PMM) sit at approximately 0 %. The human ceiling at the same FPR is 54.5 %
and 90.7 % [c7-monde-ouvert-resultats.md].

**These figures replace the ones we first published, and the correction runs against us.** The
naive attack gave 3.04 % and 20.39 % at 1 % FPR, and 0.93 % and 8.47 % at 0.1 %. On Twin-2K-500
the revision is small (3.04 → 4.28 %). On the Park archive the open-world rate **triples**
(20.39 → 60.17 %): our first attack understated that leakage badly, and any reader holding the
earlier number holds a figure we no longer defend.

**Our preregistered prediction was refuted, and one half of it was then reversed by a better
attack.** We announced > 5 % (Twin) and > 30 % (Park). Measured with the naive attack, both fell
below the bar — the refutation we reported. Under the strong attack, Twin (4.28 %) still falls
below, while the Park archive (60.17 %) passes the bar it had failed. We state both, in that
order, rather than quietly reporting whichever version flatters the claim.

> **Figure 1 — Open-world detection, naive attack and strong attack
> (`article/figures/fig1-monde-ouvert.png`).**
> Two stacked panels, one per dataset (Twin-2K-500 above, titled "Twin-2K-500 (2,058
> respondents)"; the Park archive below, titled "Park et al. (1,052 agents)"). Abscissa:
> false-accusation rate (FPR) on
> a **log scale**, spanning roughly 4·10⁻⁴ to 1. Ordinate: true-detection rate (TPR), 0 to 1.
> Each panel overlays **two attacks** on the best twin/agent of that dataset: the naive
> Hamming-agreement attack, drawn as a full ROC curve (dashed line) built from every threshold in
> `resultats/c7-monde-ouvert-roc.csv`; and the strong A-LLR (likelihood-ratio) attack, drawn as
> **isolated filled diamonds with no connecting line and no error bars**, because
> `resultats/c7-attaquant-fort.csv` measures only **two thresholds**, FPR = 0.1 % and FPR = 1 %.
> The naive curve reads 8.47 % and 20.39 % on the Park archive at those two thresholds and 3.04 %
> on Twin-2K-500 at FPR = 1 %; the strong-attack points read 44.37 % and 60.17 % on Park and
> 4.28 % on Twin at FPR = 1 %. Also shown: the statistical comparators (Demographics Only, PMM
> k=10) flattened near zero, and the human test-retest ceiling (dash-dotted) above. Dotted
> vertical reference lines at FPR = 0.1 % and FPR = 1 %. **A reader should not read a curve into
> the diamonds**: with only two measured points, no shape, slope, or intermediate value for the
> strong attack is known, and none is implied by the figure. *What the reader should see at a
> glance*: at a tenable false-accusation rate the risk is real and far above the comparators
> under both attacks, and the strong attack raises the Park archive close to the human ceiling —
> a floor, not a full account of that attack's ROC. This figure depends on no causal reading of
> the quality-leakage coupling.
> Data: `resultats/c7-monde-ouvert-roc.csv`, `resultats/c7-attaquant-fort.csv`.

### 5.4 The twin-to-twin channel (T2), replicated — and an unexplained anomaly

Two twins of the same person, built differently, designate each other when they share enough
items, with no real data on the attacker's side.

**Twin-2K-500, tabulated by common-item count** [c7-transfert-resultats.md]. 30 pairs sharing
60 common items: mean top-1 **36.4 %**, maximum 83.58 %. 12 pairs sharing 19 common items: mean
top-1 **0.45 %**, minimum 0.06 % (chance 0.05–0.10 %). Demographics Only against the rich twins
gives 7.76 %, clearly below 36.4 %. The anti-artifact control — a decoy from the same segment —
gives 0.04 % on the 60-item pairs (factor ~900) and 0.10 % on the 19-item pairs (factor ~4.5).

**Park archive replication** [c7-transfert-stanford-resultats.md]: 1,052 agents, 177 common
items. Interview→survey top-1 **11.9 % [10.1 ; 13.8]**; survey→interview **13.0 % [11.2 ;
14.9]**; top-10 approximately 45–46 %. Demographic bound 1.5–2.5 %. Anti-artifact decoy control
**at most 0.31 %**.

**We never report a single figure for this channel without its common-item count**, within or
across datasets. A previously circulated average of 26.11 % pooled the two item regimes and is
withdrawn. Nor do we claim leakage crosses waves: that arm is infeasible, with 0 items in common
between the 108 wave-4 items and the 494 context items.

**Preregistered prediction refuted.** We set a threshold of at least 20 % top-1 on the Park
archive; the observed 11.9–13.0 % does not reach it. The preregistered *failure* criterion
("does not clearly exceed the demographic bound") is however not met either, at a factor of
5–8×: the channel replicates, more weakly than on Twin-2K-500, below the numeric threshold we
predicted.

**Unexplained anomaly.** The Park archive shares 177 common items — roughly three times the 60
of Twin-2K-500 — and leaks roughly three times *less* (11.9–13.0 % against 36.4 %). The number
of common items therefore does not by itself explain the cross-dataset leakage rate, contrary to
what the within-Twin comparison suggested (60 items → 36.4 %, 19 items → 0.45 %). We state this
as a fact and propose no mechanism.

*Limits.* The 12 low pairs are exactly those at 19 common items (6 of them with a pool of 1,000
rather than 2,058): the effect follows the shared-item count, not an aberrant configuration. On
the Park archive the item-rate relation does not follow Twin's.

### 5.5 Mechanism: being right while deviating — and three refuted hypotheses

What identifies is neither the frequency of departures from the modal answer nor answer
diversity, but their **correctness** — and the whole response vector is required.

Correctness of deviations: 68.5 % for the human retest (leakage 81.6 %), 50.3 % for JSON 4.1
(20.6 %), 43.3 % for Demographics Only (2.14 %), 39.1 % for PMM (0.22 %). PMM deviates (49.7 %)
and diversifies (0.560) as much as the twin without leaking [c7-deviations-resultats.md].

The ablation is the strongest evidence: permuting the order of each twin's 40 purchase answers
drops closed-world top-1 from **33.1 % [31.2 ; 35.2] to 0.046 % [0 ; 0.11]**, below chance. An
oracle given only the count of "yes" answers gives 0.29 % [c7-mecanisme-resultats.md H3]. The
identifying quantity is the dependence structure between answers, carried by the conditioning —
not any answer taken in isolation. This is also what rules out memorization as the mechanism.

**Three preregistered hypotheses refuted.** H1 (entropy): opinion items carry 2.10 bits against
0.99 for purchase items and identify 46× less. H4 (stereotypy): 36.2 % [35.6 ; 36.8] against
37.5 % [36.9 ; 38.1] in humans. And "deviations alone carry ≥ 80 % of the leakage": 0.68 % in
the mixed condition.

We do not present "wrong deviations alone = 0.0 %" as a result: it is a floor of the method, as
the metric cannot mathematically detect a signature there.

*Limits.* The mechanism is established on Twin's purchase block alone, and is in apparent
tension with the Park archive (objection O2, §7.3).

### 5.6 Bits of identity: the instrument transports, the rate does not

An LLM twin costs approximately 0.4 bits of identity per point of accuracy gained, against
0.068 for the best useful statistical comparator. Twin JSON 4.1: **3.55 bits [3.39 ; 3.72]**
against a ceiling of log2 N = 11.01. Park composite: **7.47 [7.27 ; 7.66]** against a ceiling
of 10.04. PMM: 0.19 [0.16 ; 0.23]. B2: 0.08 [c7-bits-resultats.md §1–2].

Transportability is the point. Bits normalised by human entropy give 0.0439 (Twin) against
0.0327 (Park) — a factor of **1.34** — where top-1 varies by a factor of **3.2**. Demographics
Only and PMM leak with **no accuracy gain at all** (−0.5 and −2.4 points), a case that a ratio
alone would mask.

**A nuance against our own hypothesis.** The human retest has a ratio of 0.37 (Twin) and 0.44
(Park) — as good as or better than the twins. The excess cost exists relative to statistical
predictors, **not relative to a human answering twice**. We therefore do not claim that LLM
twins leak more than anything else.

*Limits.* The bits are a **lower bound** (dyadic bound plus Miller-Madow). The sum of per-item
mutual information is unusable as a total: 58.7 bits against a ceiling of 10.04 on the Park
archive, as preregistered.

*Framing.* This is a derived instrument, not a discovery: a case of Rényi min-entropy leakage —
the probability of guessing right in one shot [smith2009foundations] — in the spirit of
Eckersley's surprisal [eckersley2010browser], addressing the same transportability problem as
the κ of the Rocher et al. scaling law [rocher2025scaling] by another route.

### 5.7 The risk depends on the recipe — and we could not reproduce it

Our own twins, produced in a single call to cheap models from a raw profile, identify almost
nobody: 0.00 % to **0.83 % [0 ; 2.15]** (deepseek-v4/R1) across 7 cells, against 2.13 % for the
other team's Demographics Only. The interval [0 ; 2.15] **contains** 2.13 %, so no precise
factor is established — only the order of magnitude, that no model reaches 1 %, is defensible
[c7-gen-resultats.md]. Any previously circulated "25× below" figure is withdrawn.

Memorization is excluded as the explanation: llama31-8b, with a training cutoff preceding
publication, copies nothing verbatim and leaks no more than the models that do copy.

**Two further preregistered predictions refuted.** (i) R1 ≥ 10 % on at least 2 of 3 models — no
model reaches 1 %. (ii) Call granularity would explain the leakage — single call 0.00 % and
per-item call 0.00 %, with top-10 running in the **opposite** direction to the prediction
(7.5 % against 0 %) [c7-recette-resultats.md].

We therefore do not claim that leakage comes from the call format, and we do not claim the cause
is identified. **It is not.** We do not know what the Twin-2K-500 recipe does differently —
finetuning, exact persona format, or full GPT4.1 rather than mini. This is an open limit.

**We then paid to test the obvious explanation, and it failed.** The constructive demonstration
this section calls for — raise fidelity with a frontier model and check that the leakage returns
— was run on `openai/gpt-4.1` (Twin's own model class) using Twin's per-item call recipe without
modification: 30 persons × 60 items = 1,800 calls, 100 % parse rate, 4.9949 USD of actual cost
[c7-fort-resultats.md]. Accuracy reached **0.4722 [0.4361 ; 0.5050]** against Twin's 0.574;
fidelity **0.1714** against their 0.708; top-1 and top-10 **0.00 % [0 ; 0]** — below even our
cheap twins (0.83 % at best). **Two further preregistered predictions refuted**: accuracy > 0.55
and top-1 > 5 %. The third (fidelity > 0.10) was confirmed at 0.1714, but barely above our best
cheap twin (0.177): the frontier model bought us almost nothing. We did not make the leakage come
back, because we did not manage to reach Twin's fidelity.

**The curve is confirmed a third time, by an independent point.** At the fidelity actually
reached (0.1714), the regression over the 12 points of `c7-compromis.csv` (slope 0.1834,
r = 0.785) predicts leakage of **1.10 %, 95 % CI [−9.15 ; 11.35]**, and the observed 0.00 % falls
inside that interval. This point comes from an entirely new model *and* an entirely new recipe,
so it is an independent check additional to the seven regenerated twins of §5.7. It does not
contradict the curve: fidelity never rose, so the point follows the curve rather than breaking
it.

**The unknown narrows instead of disappearing.** It is neither the model nor the call
granularity. What remains implicated is the **format and length of the profile** handed to the
model: Twin's full JSON persona runs to roughly 121,000 characters against our text truncated at
8,000. The resource that would settle it is Twin's exact pipeline, or their complete personas.

*Method note.* Roughly 1,490 calls first failed with HTTP 402 "in_flight_budget_exhausted" — an
artifact of in-flight credit reservation on the key, not a lack of balance (which stayed above
3 USD). Zero-cost failures were removed from the trace and retried at decreasing concurrency
(8→4→2→1), without exceeding the cap and without double billing.

*Limits.* n = 40 persons for the recipe arm, truncated to n = 10 on the per-item arm, and n = 30
on the paid frontier-model arm; a floor effect is not excluded.

### 5.8 Replication on a second dataset

On the Park archive, the composite agent designates the right participant among 1,052 **in a
closed world** in **90.40 % [88.6 ; 92.2]** of cases under the strong attack, with a top-10 of
97.8 % [c7-attaquant-fort-resultats.md]. The human retest ceiling is 96.8 %.

**This figure replaces the 65.51 % [62.7 ; 68.3] we first published** (measured at 65.7 %
[62.7 ; 68.6] by the original script — same condition, two implementations). The gap is the
point: a naive agreement attack understated the leakage of this archive by 38 % in relative
terms, and a reader who wants the honest number needs the stronger attacker. Under that attack
an in-sample information-weighted variant reaches 93.25 %, which we do not claim as our result
(§4.3).

The remaining conditions are **naive-attack measurements**, and the strong attack was **not**
re-run on them: interview-only **44.7 % [41.8 ; 47.5]**, survey-only 20.6 % [18.2 ; 23.0],
demographic 2.26 % [c7-stanford-resultats.md]. The interview-only figure is the one carrying zero
documentary exposure to the survey, and it is therefore the cleanest demonstration that an agent
built from a conversation alone identifies its person — but given what the strong attack did to
the composite, **44.7 % must be read as a lower bound**, and we make no claim about what it would
become under the stronger attacker.

We do not compare the Park rates and the Twin rate of 20.7 % as two measurements of the same
thing: neither the item count (177 against 60), nor the per-item entropy (1.30 against 0.99), nor
the human ceilings (96.8 against 81.6) are equal. With item count equalised at k = 60, the Park
archive gives 34.0 % [23.5 ; 51.5] against Twin's 20.7 % — naive attack, on 20 draws, with a very
wide interval.

### 5.9 Scale

From N = 50 to N = 2,058, the twin/demographic ratio grows from 2.8 to 9.7: top-1 falls from
53.2 % [50.0 ; 56.3] at N = 50 to 20.7 % [20.7 ; 20.8] at N = 2,058, and the share of the human
ceiling from 57.0 % to 25.4 % [c7-echelle-resultats.md]. These are naive-attack rates; the scale
study was not re-run under the strong attack.

**We extrapolate no value beyond N ≈ 4,000.** A power law and a logarithmic law fitted on the
same 6 points already diverge at twice the range (18.1 % against 13.9 %), and the logarithmic
form collapses to zero on the comparators. The Pitman-Yor model of Rocher et al.
[rocher2025scaling] was not implemented, its formula not having been reliably verifiable.

> **Figure 2 — Imitation quality against leakage, with its control
> (`article/figures/fig2-couplage.png`).**
> Abscissa: individual fidelity (`fidelite_plancher`, share of the human floor, 0 to 1,
> linear). Ordinate: closed-world top-1 leakage, linear, 0 to ~0.85. Thirteen points: the LLM
> twins (filled circles), the statistical reference points (grey diamonds), Demographics Only
> broken out (triangle), and the human retest (star) at fidelity ≈ 1 / leakage 81.6 %.
> All thirteen points carry **error bars on both axes**, from a per-person bootstrap with 2,000
> resamples. **Inset**: the marginal null on a Spearman-rho axis — the 5th–95th percentile
> envelope of the 100 predictors carrying no individual fingerprint (`c7-disjoint-nul.csv`) drawn
> as a grey band, with the observed disjoint-item rho (0.969) plotted as a single point inside
> that band, at its lower edge. *What the reader should see at a glance*: the points rise
> together from left to right with no plateau at the top, **but the observed correlation sits
> inside the band that a fingerprint-free null already produces.** An honest contribution — the
> coupling exists and is measured — not a claim that it is individual-specific.
> Data: `resultats/c7-compromis.csv`, `resultats/c7-compromis-robustesse-points.csv`,
> `resultats/c7-disjoint-nul.csv`.

---

## 6. Defense

Shuffling the purchase answers between people of the same demographic segment (D4) brings
closed-world top-1 from **20.68 % [19.04 ; 22.41]** to **0.13 % [0.01 ; 0.28]**
[c7-defense-resultats.md]. Per-item distribution and between-segment differences are preserved
**exactly, by construction**, as PRAM predicts.

**The cost is not a single average.** Reported by component: 0.0 points on the per-item
distribution, 0.0 points on group differences, and **4.4 points on inter-item correlations**.
A previously circulated mean of 1.47 points divided by three an effect that falls entirely on
one component, and is withdrawn.

**The cost is worse than that summary suggests.** On that same indicator measured against the
real human answers, `erreur_correlations_hum` rises from **5.78 to 9.71** after D4, a
degradation of 68 %. The defended twin moves *away* from the humans on correlations; it does not
move closer. Any framing in which the defense's cost is absorbed by an error already present
compares an increment to a level, and is incorrect.

Alternatives: D1 (k=10 aggregation) gives 0.55 % for 3.8 points spread across all three
components; D2 (noise) never descends below 1 %.

### 6.1 The defense against a strong, then an adaptive attacker

The defense figure above was measured against the naive attack, which §5.2 shows to be weak. We
therefore re-ran it against the strong attack, recalibrated on the *defended* outputs, and then
against an attacker who knows the defense mechanism and knows which items it leaves untouched
[c7-attaquant-fort-resultats.md].

D4 holds. Top-1 goes from 0.13 % (naive) to **0.24 %** under the recalibrated strong attack, and
the **adaptive** attacker plateaus at **0.29 %** (strategy S1, leaving the 20 opinion items
intact; S1+S3 identical; segment-invariant strategy S3 alone 0.05 %). That is two orders of
magnitude below the 20.69 % undefended rate, and never above 1 %. **Attribute disclosure is not
demonstrated either**: the best strategy names the correct `S_gra` segment in **7.7 %** of cases,
against 6.8 % at chance and **12.6 %** for the trivial rule of always answering the most frequent
segment (40 segments) — the attack does worse than not attacking.

**A reservation we must state, because it bounds the guarantee.** This residue comes *entirely*
from the 20 opinion items that D4 does not permute. The guarantee therefore holds for this
particular split — 40 purchase items shuffled, 20 opinion items intact — and not for a design
that leaves a more informative block untouched. We do not present 0.29 % as a bound on the
defense in general.

### 6.2 Differential privacy: our prediction refuted, and the argument that survives

We preregistered the prediction that at a moderate budget, differential privacy would be
dominated by D4 on the aggregate risk-utility table. **It is not.** With per-item marginals
perturbed by Laplace noise (L1 sensitivity 2, budget split equally over 60 items, basic
sequential composition) followed by i.i.d. per-item sampling — degree-0 PrivBayes, no joint
structure — the DP synthesiser at eps = 3 and eps = 10 loses **3.33** and **3.38** points of
utility, within 5 points of D4's 1.47, while its top-1 (**0.158 %**, **0.000 %**) is **not above**
ours (0.126 %) [c7-dp-resultats.md]. We do not claim our defense beats DP, on either axis.

The utility floor is architectural, not budgetary: the non-private control (eps = ∞) still loses
3.52 points, with group error ~2.3–2.9 and correlation error ~4.4–4.6 near-constant across the
whole range; only distribution error falls with epsilon (9.7 → 3.2 points).

**What survives is a theoretical point, not an empirical win.** DP protects an individual's
*membership* in the dataset used to compute a published statistic — "is Alice in the sample?".
Our attack assumes Alice is already known, since her profile is the twin's input, and asks
whether **the output conditioned on Alice** can be linked back to her: record linkage, not
membership. The DP generator escapes that attack only by **never conditioning on an individual**
— individual fidelity stays under 0.2 points at every budget, including infinite — that is, by
refusing the twin's task altogether. Its low leakage is a by-product of that incapacity, not of
the budget chosen. A panel holder who needs population statistics should use DP; one who needs a
per-person twin cannot obtain one from this mechanism at any epsilon.

*Limits.* Written by hand rather than with a reference library, and not full PrivBayes; epsilon
covers only the published histograms, with no composition across the other analyses in this
repository; correlations, between-segment differences and the `S_gra` covariate are not
protected.

### 6.3 What the defense costs a downstream analyst

A defense is only usable if the analyses people actually run survive it. We measured three on the
same 2,058 persons [c7-utilite-aval-resultats.md].

**Preserved exactly.** Group comparisons are **identical to 16 decimal places** between the raw
and defended twin — shuffling within `S_gra` moves no group mean — and demographic regression
coefficients (gender, age) keep their sign and significance.

**Destroyed.** Purchase-item coefficients that were significant in the raw twin (p < 0.01 and
p < 0.001) become non-significant after D4. On a PCA of the 40 purchase items, **45 % of the
first component's loadings are inverted** relative to humans, against **0 %** for the raw twin.

**The honest comparison.** The unprotected twin was already wrong: it inverts the sign of the
male-female gap (+0.010 against −0.047 in humans) and already loses 5.3 points of PC1+PC2
variance (15.0 % → 9.8 %). D4 adds **3.5 points** (9.8 % → 6.3 %), less than the error already
present — but the axis inversion is **D4's own doing**. It changes *which* items compose the
structure more than it changes the structure's strength.

**Practical recommendation.** With a D4-defended twin, group analyses and predominantly
demographic regressions remain reliable. What becomes unusable is anything resting on the link
between two answers of the same person — inter-item regression, the composition of a PCA axis —
even when total explained variance does not collapse further than the twin's own starting error.

**This mechanism is not new.** It is a variant of the Post Randomisation Method
[gouweleeuw1998pram] and of data swapping, in the Reiter/Drechsler tradition
[drechsler2024synthetic, bowen2023synthetic]. What is new is its application to LLM twins with a
risk-utility curve that is *measured* rather than assumed.

*Limits.* Tested on a single block, of a single twin, of a single dataset.

---

## 7. Discussion and Limitations

### 7.1 The sixteen refuted preregistered predictions

| # | Prediction (preregistered) | Outcome | Source |
|---|---|---|---|
| 1 | The quality-leakage coupling exceeds a null without individual fingerprint | **Refuted.** Null rho 0.984 mean, 95th pct 1.000, against 0.969 observed | `c7-disjoint-resultats.md` §2 |
| 2 | Open-world > 5 % (Twin) and > 30 % (Park) at FPR = 1 % | **Refuted as first measured** (naive attack: 3.04 % and 20.39 %). Under the strong attack Twin still fails at 4.28 %, while Park **passes** at 60.17 % | `c7-monde-ouvert-resultats.md`, `c7-attaquant-fort-resultats.md` |
| 3 | Twin-to-twin top-1 ≥ 20 % on the Park archive | **Refuted.** 11.9–13.0 % at 177 common items (failure criterion not met either) | `c7-transfert-stanford-resultats.md` |
| 4 | The twin-to-twin channel leaks on the 19-common-item pairs | **Refuted.** 0.45 % mean top-1, at chance (0.05–0.10 %) | `c7-transfert-resultats.md` |
| 5 | H1: per-item entropy drives identification | **Refuted.** Opinion items 2.10 bits, identify 46× less | `c7-mecanisme-resultats.md` |
| 6 | H4: twins are more stereotyped than humans | **Refuted.** 36.2 % [35.6 ; 36.8] vs 37.5 % [36.9 ; 38.1] | `c7-mecanisme-resultats.md` |
| 7 | Deviations alone carry ≥ 80 % of the leakage | **Refuted.** 0.68 % in the mixed condition | `c7-deviations-resultats.md` |
| 8 | R1 ≥ 10 % on ≥ 2 of 3 of our own models | **Refuted.** No model reaches 1 % | `c7-gen-resultats.md` |
| 9 | Call granularity explains the leakage | **Refuted.** 0.00 % both arms; top-10 runs opposite (7.5 % vs 0 %) | `c7-recette-resultats.md` |
| 10 | Cost per unit of individual fidelity is roughly constant | **Refuted at equal sample.** CV 0.436 vs 0.357 on the same 9 points | `c7-compromis-resultats.md` §5 |
| 11 | Per-item entropy correlates with identifying power consistently | **Refuted.** Opposite sign by dataset: r = −0.81 (Twin), +0.57 (Park) | `c7-bits-resultats.md` §3 |
| 12 | P1: a stronger attacker gains ≥ 20 % relative over the naive attack | **Refuted on Twin** (+12.2 %, 20.69 → 23.23 %); held on Park (+38.0 %, 65.51 → 90.40 %) | `c7-attaquant-fort-resultats.md` |
| 13 | P3: an adaptive attacker knowing the mechanism breaks the defense | **Refuted, in the defense's favour.** Plateaus at 0.29 %, never above 1 % | `c7-attaquant-fort-resultats.md` |
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Refuted.** eps = 3/10 lose 3.33/3.38 points against D4's 1.47, top-1 0.158 %/0.000 % against 0.126 % | `c7-dp-resultats.md` |
| 15 | A frontier model on Twin's per-item recipe reaches accuracy > 0.55 | **Refuted.** 0.4722 [0.4361 ; 0.5050] | `c7-fort-resultats.md` |
| 16 | That same twin reaches top-1 > 5 % | **Refuted.** 0.00 % [0 ; 0], below our cheap twins | `c7-fort-resultats.md` |

Three further preregistered outcomes were partial rather than refuted, and we count them as
neither confirmations nor refutations: D4 erases two publishable inter-item effects while leaving
signs unchanged, and its PCA prediction holds on variance but is contradicted on the loadings
(§6.3); the paid frontier-model run cleared its fidelity > 0.10 bar at 0.1714, barely above our
cheapest twin (§5.7). One prediction held outright under adversarial pressure: P2, that D4 stays
below 1 % against a strong attacker (§6.1).

### 7.2 What we do not know

**An excess cost in bits per unit of fidelity, real but unexplained.** Recomputed on equal
samples: CV(bits/fidelity) = 0.436 against CV(bits/accuracy point) = 0.357 on the same 9 points
— the second remains less dispersed, but the gap shrinks (factor 0.82, not 0.70). The ratio runs
from 1.47 to 5.02 for the 7 LLM-derived configurations against 0.68–1.53 for the 3 defined
statistical ones. The excess is real on this sample, but with so few points and no identified
mechanism it **must not be attributed to "LLMs" as a family**: we describe it as unexplained
[c7-compromis-resultats.md §5].

**We did not reproduce the leakage with our own twins** (§5.7), including with a paid frontier
model on Twin's own per-item recipe. We therefore do not know what the Twin-2K-500 recipe does.
This is an open limit, never a mechanism — but a narrower one than before: it is neither the
model nor the call granularity, and what remains implicated is the format and length of the
persona (roughly 121,000 characters in Twin's full JSON against our 8,000-character truncation).
The resource that would settle it is Twin's exact pipeline or their complete personas; we name it
rather than speculate further.

**Rates do not predict across datasets.** The normal-maxima model lands close on Park k = 60
(0.354 predicted, 0.340 observed) but fails both its controls (0.053 for 0.206 observed; 0.983
for 0.656): an isolated success between two failures is a coincidence, not a law
[c7-bits-resultats.md §3]. Only conditional information retains sign and order of magnitude
across datasets (r = 0.72 and 0.89).

**The twin-to-twin channel's cross-dataset rate is not explained by common-item count** (§5.4).

### 7.3 The three most dangerous objections

**O1 — "Tautology: a model faithful to the individual identifies, obviously."** *Not dismissed.*
What holds: nothing predicted the form or the strength of the relation before measuring it on 12
heterogeneous methods, and it survives complete disjunction of the items used for each axis
(rho 0.969 [0.937 ; 0.993]). What no longer holds: a marginal null with no individual structure
reproduces the coupling's strength (0.984). The correlation alone does not distinguish an
individual fingerprint from a global-quality effect. What remains defensible independently is
§5.2, where two methods at near-identical accuracy leak two orders of magnitude apart —
reinforced by the two sampled generators at 0.22–0.25 %.

**O2 — "Twin and the Park archive contradict each other: opinion does not identify here and
identifies most there; your mechanism is a block-size artifact."** The control is done and
excludes both simple explanations. At 20 items, the Park archive gives 11.7 % against 0.24 % for
Twin's 20 opinion items, **at lower per-item entropy** (1.30 against 2.10): neither item count
nor entropy explains it [c7-stanford-resultats.md §6]. What remains is consistent with the block
effect — the dependence structure between items of one family. **We present this as the
best-supported hypothesis, not as a result**: the dedicated test (one attacker receiving the
copula alone against another receiving the margins alone) is not done.

**O3 — "This is not re-identification: the attacker already holds the real answers."** Assumed;
it is the paper's framing (§3, T1). Our answers: the explicit threat model, the open-world
measurement that gives the honest number (§5.3), and T2 (§5.4), which *widens* the threat — a
third party crossing two twin files of the same panel needs no human answer at all. What is
missing is the curve "how many items must the attacker hold", of which we have only two isolated
points (30 items → 7.6 %; waves 1–3 as target → 19.1 %).

### 7.4 Multiplicity

Most of this paper's central results are bootstrap confidence intervals around a descriptive
measure — re-identification rate, rank correlation, bits of identity — not classical hypothesis
tests; of the 34 preregistered predictions underpinning those claims at the time of the census,
11 were refuted and 3 judged inconclusive, a rate of roughly one third, the opposite of the
signature of data dredging. Of the 3 tests carrying a classical p-value, a Holm correction leaves
the two smallest standing (0.002 and 0.008, adjusted to 0.006 and 0.016) and confirms the
non-significance of the third (0.78), already read as such before correction; the confidence
intervals carrying the other claims do not correct the same way and must be read as measurements,
each with its own margin, not as independent rejections of a common null hypothesis
[c7-multiplicite.md].

The full census covers 47 adjudicated tests across three families — the article's claims, the
standalone controls, and the abandoned branches — with 25 confirmed and 15 refuted. It was
written over the 15 `c7-*` sub-studies existing at the time and does not include the four
verdicts added the same day (the strong attacker, DP, downstream utility, and the paid
frontier-model run), which is why Table 3 lists sixteen refutations where the census counts
eleven.

### 7.5 Scope, and two limits established by failure

Two datasets, one language, one questionnaire format, categorical closed-choice answers only.
The mechanism analysis rests on a single block of a single dataset. The defense is tested on that
same block. We make no claim about conversational agents or about panels outside the two studied
here. Two further limits we state with the specific resource that would lift them, because we
looked for that resource and did not find it.

**Generality beyond GSS and Big Five instruments.** Both our datasets are American survey panels
built on the same instrument family, so we cannot say whether this channel is a property of that
family. We searched our holdings for a third dataset of a different nature carrying both real
answers and simulated outputs for the same people, and found none usable
[c7-troisieme-jeu-inventaire-2026-09-12.md]: the GSS panel is the very instrument a reviewer
would object to; the Westwood PNAS 2025 material has no matched human file; NORC mode data and
the ANES codebooks hold no individual microdata. Two candidates are genuinely different in nature
and publishable in aggregate — the NY Fed Survey of Consumer Expectations (82,535 observations,
stable `userid`) and Ahler-Sood (YouGov, CC0) — but **neither has existing simulated outputs** for
its respondents. Generating them ourselves would introduce a new confound, our own generation
method and models, and would test a different question. The missing resource is an individual
dataset from a domain distinct from GSS and Big Five — health, consumption, elections — for which
LLM twins produced by a **third-party team** already exist for the same respondents, under a
licence permitting local computation and publication of an aggregate rate.

**Free-text outputs.** We measure nothing about free text, and the reason is that neither dataset
permits it: the Park archive publishes **no transcripts**, and **none of the 13 Twin
configurations** produces text. Every rate in this paper therefore concerns closed-choice
categorical answers. The missing resource is Park's complete transcripts, or a run of the Twin
pipeline that generates text. We extrapolate our rates to free-text outputs in neither
direction — note that the free-text inference literature [staab2024beyond, ko2026weakcues]
attacks a richer signal than ours, so our figures are not an upper bound on that setting.

---

## 8. Ethics Considerations

**Datasets.** Twin-2K-500 is public under CC BY 4.0; the Park replication package is publicly
posted. No new data was collected: the attack uses only already-published content (human
answers and twin outputs). A limit to note: participants did not specifically consent to a
re-identification test on the twins generated from their answers.

**No individual is identified.** No name or identifier linking a `pid`/`TWIN_ID` to a real
person is published or listed. Only rates aggregated over the full cohorts are reported; no
individual case is named or shown.

**No new harm on these datasets.** Twin-2K-500 already publishes, for each person, their
identifiers and real answers beside their twin: matching is trivial without any attack. The
result does not create new harm on this specific dataset; it documents a generic risk for
anyone releasing "anonymised" twins without that key — a practice Twin-2K-500 does not follow.

**Benefit.** Several teams publish individualised LLM twin outputs without any linkage risk
analysis. This provides a first measured figure for that risk on public datasets and a
reproducible method for testing it elsewhere *before* publication.

**Responsible disclosure.** Planned with the Twin-2K-500 authors (Toubia et al.) and with Park
et al. before any preprint posting or code release, with a 30-day response window and an offer
to share code and report in advance. The tone toward Park et al. is fixed: *your warning was
accurate, here is its measured magnitude*. **These letters have not yet been sent; see
`[OPEN ITEMS]`.**

**The Park et al. case.** Their supplementary material (Participant Consent) already warned
participants that their information might be "inadvertently shared" and acknowledged that
complete anonymity remains challenging. They named the risk, obtained an ethics agreement
worked over more than six months, pseudonymised, restricted access to individual responses and
planned a 25-year withdrawal. No public audit had measured the magnitude of that named risk;
our figures (90.40 % for the composite agent among 1,052 in a closed world, 60.17 % in an open
world at 1 % false accusations, and 44.7 % — a lower bound, the strong attack not re-run on the
interview-only condition — from the interview alone) are,
to our knowledge, its first quantification. We note for the disclosure letter that our own first
measurement, 65.51 % closed-world and 20.39 % open-world, understated the magnitude of the risk
they had named.

**Publishing the attack code, for and against.** *For*: replicability, and enabling other panel
holders to test their twins before publication — standard security practice. *Against*: it
lowers the cost for an attacker already holding a third-party panel's real answers and a
corresponding twin file. *Our resolution*: publish, because the code only acts if the attacker
already holds real answers to the same items (rare outside the panel holder), and the
countermeasure is straightforward once the risk is known.

**Recommended defenses.** (a) Do not publish twin outputs item by item for blocks with high
inter-person specificity; publish aggregates or calibrated noise. (b) Break the person-twin
alignment in public files. (c) Publish regenerated twins without copying wave metadata
(`StartDate`/`EndDate`/`Duration`/`RecordedDate`). (d) Document a minimal linkage test before
any twin release. (e) Within-segment shuffling (§6), with its real cost stated: 4.4 points on
inter-item correlations, a 68 % worsening of the gap to human correlations (5.78 → 9.71), and the
loss of every inter-item analysis downstream (§6.3) — it holds at 0.29 % against an attacker who
knows the mechanism, but only for a split that shuffles the informative block (§6.1).
(f) Differential privacy where the published object can be a population statistic rather than a
per-person twin: it answers a different threat model, and buys its low leakage by never
conditioning on an individual (§6.2).

**Public interest.** The AAPOR report of 8 May 2026 ranks synthetic response generation as the
highest privacy-risk task it evaluates and names re-identification by linkage without
quantifying it. A risk named by practitioners and professional bodies but never measured
justifies an independent measurement followed by responsible disclosure rather than silence.

**IRB determination: a declared gap.** This work has **no ethics exemption or approval
determination of its own**. Only Park et al.'s IRB is referenced, for their own collection, not
for the present re-identification. PoPETs expects an explicit sentence naming an institution,
even to conclude that the work falls outside human-subjects research. Until that determination
is obtained and cited here, this is a real gap in the submission dossier, distinct from the
data-licence verification conducted separately.

---

## 9. Availability

**Review artifact.** `artefact/` replays the re-identification attack and its D4 defense in a
single command (`./artefact/run.sh`), **with no real data and no real person**, in approximately
25 seconds on a laptop, without GPU, without network, and without any language model call. It
runs on a fictional dataset of 600 synthetic persons generated at fixed seed
(`config.GRAINE = 20260912`) with a tunable individual-signal dial
(`config.SIGNAL_INDIVIDUEL = 0.25`), structurally comparable to the real data (categorical
items, product × price matrix block, demographic segments, retest) but with different sample
sizes and signal strength.

The artifact demonstrates that the two mechanics are the ones running in the paper: `attaque.py`
imports `items_communs`, `rangs_attaque`, `rang_dans_segment` and `graine_nom` from
`analyses/c7_reidentification.py`, and `defense.py` imports `defense_d4` and `mesurer_utilite`
from `analyses/c7_defense.py`. Nothing is copied; the only function that reads real data
(`t1_commun.charger()`) is never called, and a guard (`garde.py`) refuses to start if a path to
`data/` is detected.

**No artifact figure is a result of this study.** The artifact's outputs (on fictional data:
21.9 % before defense, 0.842 % after D4) illustrate the mechanics and must never be cited as
study results. The study's figures are those of §5 and §6, measured on Twin-2K-500 and the Park
archive.

**Obtaining the real data.** Twin-2K-500: Hugging Face repository `LLM-Digital-Twin/Twin-2K-500`,
CC BY 4.0. Park replication archive: publicly posted on OSF at `https://osf.io/t6g7k/`; it
contains real individual responses from 1,052 human participants, is not redistributed here, and
is never read by the artifact. Verify current terms of use on the OSF page before any download.

**Preregistrations.** `resultats/c7-preenregistrement.md`,
`resultats/c7-defense-preenregistrement.md`, `resultats/c7-stanford-preenregistrement.md`, each
written before any computation. Third-party timestamping is pending; see `[OPEN ITEMS]`.

**Environment.** Python 3.13.14, numpy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0. No network
dependency.

---

## References

Bibliography maintained in `article/references.bib`. Keys cited in this manuscript, in order of
first appearance: `toubia2025twin`, `park2024generative`, `bonagiri2026cognitive`,
`das2024blind`, `duan2024membership`, `satml2025position`, `ward2025synthmia`, `byun2025kdd`,
`platzer2021holdout`, `adams2025iscience`, `giomi2023anonymeter`, `gouweleeuw1998pram`,
`smith2009foundations`, `eckersley2010browser`, `rocher2025scaling`, `stadler2022groundhog`,
`annamalai2024linear`, `ganev2025inadequacy`, `ganev2026rethinking`, `ganev2024genlaw`,
`yao2025dcr`, `meeus2023achilles`, `golob2026sok`, `narayanan2008robust`,
`demontjoye2015unique`, `rocher2019estimating`, `taub2018dcap`, `carlini2021extracting`,
`staab2024beyond`, `ko2026weakcues`, `lermen2026deanonymization`, `yeom2018privacy`,
`feldman2020memorization`, `bun2014fingerprinting`, `dwork2015robust`, `argyle2023out`,
`peng2026funhouse`, `guepin2023synthetic`, `anon2026decoupling`, `drechsler2024synthetic`,
`bowen2023synthetic`.

---

## [OPEN ITEMS]

Blocking or unresolved at the time of writing. Items marked **[decision]** depend on the
responsible investigator, not on any agent.

1. **[decision] Disclosure letters not sent.** Drafts ready in
   `divulgation-responsable-brouillon.md` for the Twin-2K-500 team (Toubia et al.) and Park et
   al. The 30-day response window is on the critical path and must open **before any preprint
   posting**. §8 currently states these as "planned"; that sentence must be updated to a date
   once sent.
2. **[decision] Timestamped OSF deposit with DOI** of the C7 preregistration plans. Without
   third-party timestamping, the word "preregistered" — used throughout §5 and Table 3 — is not
   attestable, and no external co-signer will commit.
3. **[decision] IRB / exemption determination for this study itself.** §8 declares this gap
   explicitly. PoPETs expects a named institution, even to conclude the work is out of scope for
   human-subjects research.
4. **Bibliography keys are provisional, and the file does not yet exist.**
   `article/references.bib` was **absent** from the repository when this manuscript was written
   (another agent is completing it). Every key listed in References
   above is a conventional author-year guess and must be reconciled against the finished file
   before submission. Two entries additionally carry "confirm before deposit" markers:
   Adams et al. (iScience 2025) DOI, and the stable URL for PRAM (Gouweleeuw et al. 1998).
   Further identifiers flagged as unconfirmed in the related-work source: Eckersley (PETS 2010)
   exact reference, Yeom et al. (arXiv 1709.01604), Feldman (arXiv 1906.05271), Bun et al.
   (arXiv 1311.3158), Dwork et al. (arXiv 1502.02486).
5. **Bibliographic verification 1 — Anonymeter's formal definition.** Re-read Giomi et al.
   (PoPETs 2023) linkability definition on the original PDF, to confirm the characterisation
   used in §1.2, §2.1 and §3 (T2): link between two records of the *same* original dataset, the
   attacker already holding *real* attribute values.
6. **Bibliographic verification 2 — ZAK-MIA (PoPETs 2024).** Content never verified; extraction
   failed during the prior-art scan. It is not currently cited; confirm it does not constitute
   closer prior art to §5.4 before submission.
7. **[decision] Recipe question: the paid run happened and did not settle it.** The authorised
   top-up was spent — 4.9949 USD of 5.00 on `openai/gpt-4.1` with Twin's per-item recipe — and
   the leakage did not return (§5.7). It rules out the model and the call granularity, leaving
   the persona format and length. Decide: fund a further pass with a full-length persona **if**
   the Twin team supplies its pipeline, or publish the question as an assumed limit. The second
   reproducibility pass on regenerated twins (top-1 per pass, agreement on the designated
   identity) remains undone.
8. **Positioning file not yet available.** `resultats/positionnement-vie-privee-2026-09-12.md`
   did not exist when this manuscript was written. §8 must be re-read against it once delivered,
   as the ethics draft itself flags that dependency.
9. **Two computable figures still unpublished**, local, no API calls: the size of rank-1 tie
    classes per configuration (is top-1 a measurement or a tie-breaking convention?), and the
    Park k = 60 point written to a CSV rather than printed to screen only.
10. **Two tests that would close objections O2 and O3** (§7.3), both local, no API calls: the
    copula-alone against margins-alone test, which would turn the block-effect hypothesis into a
    result (one day); and the "number of items held by the attacker" curve (1, 5, 10, 20, 40,
    60, crossed with recoding noise), which closes O3 (half a day).
11. **External replication of the critical path.** Counter-examination, hostile review and
    provenance audit are all internal to the agent apparatus: this is internal control, not
    independence.
12. **Artifact re-read against final figures.** Verify that no artifact number can be read as a
    study result (§9 states this explicitly; confirm after the figures are final).
