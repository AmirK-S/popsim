# Linkability of LLM Digital Twins: From Chance in 2023 to 60 % in an Open World, and the Control That Says When Not to Measure

*Submission draft, PoPETs. Body target: 12 pages. Bibliography: `article/references.bib`.*

---

## Abstract

Published LLM "digital twins" — per-respondent simulated answer vectors released alongside
survey panels — are linkable to the humans they were built from, and that risk has a
trajectory. Measured on three datasets and three generations of models, the twins of 2023 did not
beat a demographic baseline recomputed on their own pool, and the twins of today exceed theirs.
On the GPT-3 twins Argyle et al. released in 2023, the strongest designates the right respondent
among 2,148 in **0.14 %** [0.05 ; 0.27] of cases against 0.10 % [0.02 ; 0.23] for that baseline —
intervals that overlap, at a per-item accuracy *below* the modal answer.
On twins built with recent models the same attack reaches **20.7 %** [19.0 ; 22.4] on Twin-2K-500
(2,058 respondents) in a closed pool and **4.28 %** [3.3 ; 5.6] in an open world at 1 % false
accusations, against a human test-retest ceiling of 54.5 %. **Twin-2K-500 is the dataset that
carries the claim**: armed identically on the same basin, a demographics-only comparator sits
**29.9×** below the twin, and the gap survives giving a classical comparator the twin's own
input. On the Park et al. archive the corresponding rates are **not evidence that the twin leaks
beyond demographics**: that archive's "demographics-only" condition is conditioned on **eleven**
attributes that leave almost every respondent unique in their own sample, and armed identically
it comes within a ratio of **1.06×** of the agent (§5.8). **The three datasets differ in team, protocol, item count and pool, so
"the risk grew with model capability" is confounded with "the protocols differ"; we state that
confound in front rather than resolve it.**
Inside a shared pipeline we report a twin-to-twin channel: two twins of the same person designate
each other with no real human answer held by the attacker — at 60 common items, 30 ordered pairs
of **six** configurations running from 11.9 % to 83.6 % top-1, mean 36.4 % [24.7 ; 56.5] on those
six units. The "distance law" we preregistered — leakage falling with
the number of differing elements — is refuted by our own measurements, and we claim no converse
law; whether the channel survives between *independently built* pipelines is untested.
Our control is not new — it is the pre-spend, gating form of Anonymeter's control baseline — and
it costs nothing: no experimental arm is interpretable until its candidate pipeline beats a
demographic baseline against the real humans. It stopped two of our own paid experiments and the
Argyle replication.
We also report what we could not establish. We preregistered that the observed coupling between
imitation quality and leakage reflects an individual fingerprint; a null carrying only a matched
per-person accuracy margin — which in fact leaks more than our own twin (31.6 % against 20.7 %) —
reaches a rank correlation as high as ours ({{R:rho-nul-marge-appariee-12conf-n100}}, 5th–95th percentiles {{R:rho-nul-marge-appariee-12conf-n100.ic}}, against
0.965 observed). Thirteen preregistered predictions were refuted, one is withdrawn, two are
inconclusive and one untestable; our own twins failed to reproduce the leakage even with a paid
frontier model; and the mechanism concentrating the effect on one item block stays open, though
six candidate explanations are now excluded. **The headline rate also rests on a single generation
that is not ours and whose parameters its authors have not published**: across seven
configurations {{R:variance-part-generation}} % of the observed variability is attributable to the
generation configuration and {{R:variance-part-personnes}} % to the people, so it must be read as
the rate of the most faithful configuration we hold, not of an LLM twin in general.
Finally, a 1998 mechanism (PRAM) applied to twins brings closed-world top-1 to **0.29 %**
[0.10 ; 0.53] against the best attacker we measured — one who knows the mechanism and attacks the
block it leaves untouched — at a measured cost of 4.4 points on inter-item correlations. It
carries **no formal guarantee**: it republishes each item's within-segment histogram exactly, so
its zero distribution and group errors are that republication, not a cost avoided.

---

## 1. Introduction

Survey research is beginning to publish *digital twins*: for each human respondent in a panel,
an LLM is conditioned on that person's profile and its simulated answers to the questionnaire
are released as a per-person record. Toubia et al. published 2,058 such twins as Twin-2K-500
[toubia2025twin2k500]. Park et al. built generative agents for 1,052 participants and cited privacy
in restricting access to individual agent responses [park2024agents] — although the publicly
posted replication package does carry those individual responses together with the agent
conditions we analyse (§4.1, §8). The privacy question these releases raise has been named — by
Park et al. themselves, by Bonagiri et al. [bonagiri2026cognitive], and by the AAPOR task force
[aapor2026responsibleai], which ranks synthetic response generation as the most risky of the core
tasks it evaluates and names re-identification by linkage without quantifying it — but it has not
been measured.

This paper measures it on three datasets spanning three generations of models, and reports both
what the measurement supports and what it refutes.

### 1.1 The trajectory, and the confound that comes with it

Argyle et al. published in 2023 GPT-3 twins of ANES respondents, 12 matched items per person
[argyle2023outofone]. Attacked exactly as we attack the recent panels, those twins do not
demonstrably beat a demographic baseline recomputed on their own pool of 2,148: the intervals
overlap, at a per-item accuracy *below* the modal answer, and a nearest neighbour given the same
eleven true answers carries **3.6 times more identity bits** (§5.8). Two years later, twins of the
same kind of panel are re-identified at 20.7 % in a closed pool of 2,058 and 4.28 % in an open
world at 1 % false accusations — and 29.9 times their identically armed demographic comparator
(§5.8). The risk was not measurable in the first published generation of twins; it is substantial
in the current one.

**The confound, stated before the claim rather than after it.** The three datasets differ in
team, protocol, item count (12 against 60 and 177), pool and questionnaire. "The risk grew with
model capability" is therefore confounded with "the protocols differ". At matched **effective**
information — the same independent item count on both sides, the same pool size, the same attack
and the same tie-breaking convention — the twins of 2025 exceed their own demographic baseline
while none of the three twins of 2023 exceeds theirs. Matching on the raw number of items is not
enough: twelve Twin items still carry 46 % more independent information than the twelve ANES
items, and the number of items inflates every attacker, the demographic baseline included, by a
factor of {{R:temoin-items-apparies-facteur-12-60-baseline}} between 12 and 60 items. We therefore
report a **direction, not a magnitude**: the 2023 endpoint fails our interpretability control and
is not estimable, its ratio to baseline wandering between 1.4 and 3.7 across subsamples of its own
pool, and relative to a nearest-neighbour attacker holding the same items the two ends differ by
less than we can separate from noise. Nor are they in one metric: closed-world top-1 under a naive
Hamming attack at the left, true detections at 1 % false accusations under A-LLR at the right, the
second **undefined** at the left end, where its open-world AUC is indistinguishable from zero.
These witnesses are post-hoc, and the matched-information figures are in the appendix. Lifting the
confound would need the same items, the same population and several generations of models with
individually matched twins; no such resource is public (§7.4). We state the trajectory as a
measured contrast between three published corpora, never as a causal effect of model capability.

One reading must be excluded. The Argyle result is **not a refutation of the scale trend we
report**: it is out of domain. That trend is measured on twins that carry a person (§5.9), and our
interpretability control (§4.5) establishes that these twins carry none we can demonstrate.
Taking 0.14 % for a refutation would commit, in reverse, the exact error the control exists to
prevent — concluding from a measurement taken on noise (§5.8).

### 1.2 What we set out to show, and what happened

Our central hypothesis was that a twin's fidelity to *its particular person* and that twin's
identifiability are expressions of one underlying axis. We preregistered a self-refutation test
in two parts. The first passed: the rank correlation between imitation quality and leakage
survives measuring the two axes on completely disjoint item sets (Spearman 0.969, 95 % CI
[0.937 ; 0.993], 50 stratified random A/B splits of 60 items). The
relation is not an artifact of recycled computation.

The second part failed, and against us. We constructed a *marginal null*: 100 artificial
predictors matched to each person's own accuracy margin, with correct positions drawn at random
without looking at the person — an object that is not structure-free, and that in fact leaks more
than our own twin (31.6 % top-1 against 20.7 %). Adversarial review found a real defect in that
first witness, since rebuilt without changing the verdict (§5.1). The rebuilt witness reaches mean
Spearman **{{R:rho-nul-marge-appariee-12conf-n100}}**, 5th–95th percentiles {{R:rho-nul-marge-appariee-12conf-n100.ic}}, against **0.965** observed over the 12 configurations; the observed value does not exceed it. Each null is compared
only against the observed value measured on its own plan. **Reproducing the coupling requires
nothing more than a matched per-person accuracy and correct positions drawn at random —
prediction (b) is refuted.**

We report this as a result rather than a confession. A recent line of work argues that an attack
on foundation models proves nothing until the null hypothesis is properly sampled: blind baselines
routinely beat state-of-the-art membership inference attacks [das2024blind, duan2024membership],
and a SaTML position paper makes the demand explicit [zhang2024satml]. The quality-leakage
coupling reported in prose by Ward et al. [ward2025synthmia] and Byun et al.
[byun2025riskcontext], and contested by Platzer and Reutterer [platzer2021holdout] and Adams et
al. [adams2025fidelity], has never been tested against such a control. We built it, and it absorbs
our own effect. What survives is not a theory of why twins leak, but measurements that do not
depend on the coupling being individual-specific at all.

### 1.3 Contributions

**(1) A trajectory measured across three generations of published twins.** The same attack, under
the same control, on twins released in 2023, 2024 and 2025: at their own demographic baseline
then, 29.9× above it now in the closed pool (§5.8), with the protocol confound of §1.1
forbidding any reading of it as an effect of model capability alone.

**(2) A pre-spend stop rule, and what it cost us.** The discipline is not ours: Anonymeter builds
a control baseline into its risk estimate [giomi2023unified], and blind baselines demand the same
of membership attacks [das2024blind, zhang2024satml]. What is ours is the gating form, consuming
no model call and applied before the first paid arm: **no experimental arm is interpretable until
its candidate pipeline has been shown to beat the demographic baseline in top-1 against the real
human answers** (§4.5). It stopped two of our own paid arms (§5.4), the Argyle replication
(§5.8), and the `persona` condition of the Park archive, where an agent built on a person's own
self-description re-identifies her *less* well than demographics alone.

**(3) A twin-to-twin linkage channel within a shared pipeline, whose rate is not governed by how
many pipeline elements differ.** Two twins of the same person, sharing their persona source and
differing only in model or output format, designate each other while the attacker holds no real
human answer of any kind, on both Twin-2K-500 and the Park archive and against anti-artifact
controls at or below 0.31 %; no number for this channel is reported without its common-item count.
At one pipeline element changed the rate runs from 17.2 % to 81.4 %, and the *distance law* we
preregistered — leakage falling with the number of differing components — is refuted by our own
measurements (§5.4). Anonymeter's low linkability figure is not a counter-result, for the reason
given in §2.1. Whether the channel crosses *independently built* pipelines is untested: the arm
meant to decide it is not interpretable (§5.4).

**(4) The leakage is localised in the pattern of answers, not in memorised content**, by an
ablation that permutes the order of a twin's answers while leaving their content untouched (§5.5):
what identifies is the dependence structure between answers. The pipeline trains nothing on the
target population, so no train/test gap exists to exploit, unlike Yeom et al. [yeom2018privacy]
and Feldman [feldman2020memorization]; but our training-cutoff control lives in a regime where
none of our twins identifies almost anyone (§5.7), so **we do not claim a measured dissociation
between memorization and re-identification.** That narrower claim is what separates our channel
from the memorization [carlini2021extracting] and free-text inference literatures
[staab2024beyond, ko2026weakcues, lermen2026deanonymization]. What concentrates the effect on one
item block stays open, but six candidate explanations are now excluded (§5.5).

**(5) The Narayanan–Shmatikov attack, instantiated on twins, with its human ceiling.** Both moves
are theirs [narayanan2008robust]: the rarity-weighted likelihood score, and the out-of-sample
criterion that reports true detections against false accusations (§5.3, Figure 1). New here are
the object, the pool, the human ceiling, and out-of-fold estimation of the weights. It corrects
our own published Park figure upward — and raises that archive's demographic comparator further
still, which is why Park no longer carries this paper's claim (§5.8).

**(6) Twenty-six defenses, each measured against an adaptive attacker written before the
measurement, and one of them bounded.** Permutation — the family our variant of the 1998 Post
Randomisation Method [gouweleeuw1998pram] belongs to — is a dead end even in its most favourable
case; within-segment aggregation by the mode holds adaptive top-1 under a combinatorial 1/k that
binds any attacker, at a cost in between-segment statistics that we publish beside it (§6.1).
Every rate we report other than that bound, our PRAM variant's included, is the rate of an attack
we built: it offers **no formal guarantee** and republishes the within-segment item histogram
exactly (§6). We preregistered a comparison with differential privacy and **withdraw it**; we
claim no superiority over differential privacy in either direction (§6.2).

**(7) A bits-of-identity instrument that transports across datasets where the raw rate does
not.** A derived instrument, not a discovery: a case of Rényi min-entropy leakage
[smith2009foundations], in the spirit of Eckersley's surprisal [eckersley2010unique], addressing
the transportability problem of the Rocher et al. scaling law [rocher2025scaling] by another
route (§5.6).

### 1.4 Negative results, stated in front

Thirteen preregistered predictions were refuted and one is withdrawn, two are inconclusive, and
one could not be tested at all (Table 1, §7.1); three later verdicts — the distance law (§5.4) and the third
dataset's two predictions (§5.8) — sit outside that table for the reasons given there. Our own
twins identify almost nobody, and the constructive demonstration meant to close that gap — raise
fidelity with a frontier model and watch the leakage return — **failed**: `openai/gpt-4.1` on
Twin's per-item recipe left fidelity at 0.1714 against their 0.708 (§5.7). We still do not know
what the Twin-2K-500 recipe does differently. The coupling that motivated this work does not
survive its own control (§5.1). And **the headline rate is the rate of one generation of one
configuration** — the most faithful of the eight we measured, and also the highest — which we did
not produce and cannot re-run, its authors not having published the parameters behind it (§7.4).
We consider a reader who stops here to have read the paper honestly.

---

## 2. Background and Related Work

### 2.1 Privacy of synthetic data

Stadler, Oprisanu and Troncoso show that generated tabular data remains linkable to its sources
[stadler2022groundhog]. Giomi et al. formalise three attacks — singling out, linkability,
inference — and conclude, on their datasets, that linkability is the weakest risk
[giomi2023unified]. That conclusion is contested: Annamalai, Gadotti and Rocher
[annamalai2024linear] and Ganev and De Cristofaro [ganev2025inadequacy, ganev2026rethinking,
ganev2024regulatory] show reconstruction attacks defeating distance-to-closest-record metrics;
Yao et al. [yao2025dcr] and Meeus et al. [meeus2023achilles] generalise the critique; Golob,
Pentyala and De Cock make these attacks an emerging standard [golob2026sok]. Houssiau et al.'s
TAPAS formalises attacker knowledge and the baselines an audit must beat [houssiau2022tapas].

*What distinguishes us.* That corpus is tabular microdata from classical generators, judged by
continuous similarity metrics. Ours is a categorical answer vector produced by an LLM conditioned
on a person, where no similarity metric replaces a direct matching attack.

### 2.2 Re-identification of real data

Narayanan and Shmatikov re-identify Netflix users [narayanan2008robust]; de Montjoye et al.
show four spatio-temporal points suffice on credit-card metadata [demontjoye2015unique];
Rocher, Hendrickx and de Montjoye model risk on incomplete samples [rocher2019estimating] and
extend it into a scaling law [rocher2025scaling]. Taub et al. ground the statistical measurement
of disclosure risk on synthetic data (CAP, TCAP) on the premise that synthetic generation breaks
the link between identity and datum [taub2018differential].

*What distinguishes us.* These works re-identify from genuine auxiliary data. Our attack's input
is never a real datum of the target but a model output generated from a persona, matched against
real answers the attacker separately holds. That falsifies the CAP/TCAP premise, on LLM-simulated
survey microdata.

### 2.3 Privacy and LLMs

Carlini et al. document memorization and regurgitation of training sequences
[carlini2021extracting], and show memorization growing near log-linearly with model scale
[carlini2023quantifying] — the leakage-versus-capability precedent closest to our own
trajectory. Staab et al. infer personal attributes from innocuous free text
[staab2024beyond]. Ko et al. de-anonymise online authors by multi-cue agentic inference
[ko2026weakcues] — the closest threatening neighbour — and Lermen et al. demonstrate the same
attack at scale [lermen2026deanonymization]. Theoretically, Yeom et al. connect membership
attacks to overfitting [yeom2018privacy]; Feldman shows memorizing rare cases is necessary for
generalization [feldman2020memorization]; tracing codes [bun2014fingerprinting, dwork2015robust]
are the closest formal parent to our 1-in-N attack, bounding the worst case of an optimal
adversary recovering an individual from aggregate statistics, though in dimension far exceeding
the number of individuals.

*What distinguishes us.* Those works all start from free text bearing direct semantic cues,
aggregated by an agent reasoning over it. Our channel is narrower and drier: closed-choice
categorical answers, no free text, no agentic reasoning, a mechanism localised in the dependence
structure rather than in memorised content (§5.5). Unlike Yeom and Feldman, our pipeline trains no
model on the target population.

### 2.4 Respondent simulation and twins

Argyle et al. launched the use of LLMs as panel substitutes [argyle2023outofone]; their
Dataverse archive supplies the 2023 end of our trajectory, and our measurement does not
contradict their paper, whose study 3 compares matrices of Cramér's V — the association
structure of a sample, not individual accuracy. Park et al. cite privacy in restricting access to their 1,052 agents' individual responses
[park2024agents], while the publicly posted replication package nonetheless carries individual
participant and agent responses (§8) — a risk anticipated, never measured. Toubia et al. publish
the 2,058-twin panel we attack, treating neither privacy nor linkage [toubia2025twin2k500]. Peng
et al. document group-fidelity distortions on that same panel without connection to
re-identification [peng2026funhouse]. Bonagiri et al. issue a normative call to evaluate these
risks without measuring them [bonagiri2026cognitive]. None of these works measures a
re-identification rate from twin outputs. That is the gap we fill.

### 2.5 Closest prior art and contradictors

Ward et al. test 13 attacks over 9 generators and 48 tabular datasets, and state in prose a
relation between quality and leakage close to ours [ward2025synthmia]; Byun et al. observe a
near-monotone frontier of the same type [byun2025riskcontext]. Three differences separate them
from our claim: their quality is *aggregate* (MMD, Jensen-Shannon divergence, downstream AUC),
never a correspondence to the right person; their risk is *membership* in a training set, not
1-in-N identification; and they publish no coefficient.

Three contradictors hold that fidelity and risk separate: Platzer and Reutterer
[platzer2021holdout]; Adams et al., for whom a generator without formal guarantees preserves
fidelity and utility without evident privacy harm [adams2025fidelity]; and Shafieinejad et al.,
observing decoupling as quality saturates within a single tabular diffusion model trained longer
[shafieinejad2026diffusion]. Our response is not that they are wrong: all three measure
*aggregate* fidelity, never individual correspondence to the right person, and none tests whether
the coupling they observe survives a null matched on per-person accuracy. Ours does not (§5.1).
Their decoupling also unfolds over training time within one model, where ours is cross-sectional
across twelve heterogeneous methods against 1-in-N re-identification.

### 2.6 Defenses

Our D4 is not new. Shuffling answers between units of the same segment is a variant of the
Post Randomisation Method [gouweleeuw1998pram], which perturbs categorical variables through a
known transition matrix leaving margins invariant in expectation, and of data swapping — the same
family as the partially synthetic data tradition of Reiter and Drechsler, extended by Drechsler
[drechsler2024thirtyyears] and Bowen et al. [hu2023microdata]. What is new is the application to
LLM twins with a measured risk-utility curve (§6).

---

## 3. Threat Models

We distinguish three scenarios, assuming the first one's strongest objection rather than
deflecting it.

### T1 — Panel holder publishes unkeyed twins; attacker holds the real answers

A panel holder releases per-person twin records without the key linking each twin to its
respondent. An attacker who holds **the real answers to the same items** — an insider, a panel
co-owner, a leak of the source file — matches twins to respondents. This is a *linkability*
result in the sense of the Article 29 Working Party and the GDPR, not identification from
public information: the quasi-identifier required is a specific questionnaire, rarely held
outside the panel.

We state plainly what this is not. It does not show that a third party recovers a named person
from public information. And on Twin-2K-500 itself the matching is trivial without any attack —
`pid` equals `TWIN_ID`. The result therefore documents a generic risk for anyone releasing
"anonymous" twins without that key, a practice Twin-2K-500 does not follow. The objection "this is
not real re-identification, the attacker already holds the true answers" is assumed, not rebutted;
our answers are the explicit model above and the open-world measurement of §5.3.

### T2 — Two organisations publish twins of the same cohort; attacker holds nothing real

If several organisations each publish their own twins of the same panel with sufficient item
overlap, a third party cross-references them holding no human answer at all. This threat model is
named as an open problem by Jordon et al. [jordon2022synthetic] and covered by the A29WP
linkability definition, but never measured: Anonymeter's linkability presumes real attribute
values in hand [giomi2023unified], and Guépin et al. target membership in a single generator's
training set, never matching between two independent generations [guepin2023synthetic].

**We tried to test it directly, and could not**: §5.4's twin-to-twin measurement is same-team and
same-persona-file, and the arm built as T2 actually describes fails the interpretability control
of §4.5. **T2 is neither supported nor refuted: it was not tested** (§5.4).

### T3 — Pre-publication self-audit

A panel holder runs the attack against their own file before publication, to decide whether a
defense is required — the constructive use of the method, and the one the artifact (§9) serves.

### Attacker capabilities, all models

The attacker performs no training on the target population, has no query access to the
generating model, and uses only rank-based matching over categorical vectors.

---

## 4. Data and Methods

### 4.1 Datasets

**Twin-2K-500** [toubia2025twin2k500], 2,058 respondents, public under CC BY 4.0. Target: wave 4,
60 items usable in common out of 108 (40 purchase items of the form "would you buy this product
at this price?", 20 opinion items). Attacker context where applicable: 494 context items from
waves 1–3 plus 14 demographic variables. Chance top-1 in the closed pool is 0.049 %. A human
test-retest condition gives the empirical ceiling: 81.6 % [79.9 ; 83.2] top-1, accuracy 0.745.
**We generated none of these twins.** Every Twin-2K-500 arm we attack, the headline `JSON Persona
- GPT4.1` included, is taken from that release as published; our repository holds neither the
prompt nor the generating code. **The exact generation parameters of the headline arm are not
published by its authors**: the upstream repository releases thirteen sets of outputs but a single
configuration file, and that file describes a different arm — a `gpt-4.1-mini` model, a persona
rendered as *text* rather than JSON, at temperature 0.0. **We therefore state no model setting,
temperature or prompt for the arm this paper reports**, and §7.4 draws the consequence.

**Park et al. archive** [park2024agents], 1,052 participants, 177 common items, replication
package publicly posted. Of its five agent conditions we analyse four — composite,
interview-only, survey-only, demographic — the `persona` condition being excluded by the
interpretability control (§4.5). Human retest ceiling 96.8 %.

**Argyle et al. archive** [argyle2023outofone], Harvard Dataverse, **CC0 1.0**: 4,270 ANES 2016
respondents, of whom **2,148** answer all **12** matched items; chance top-1 is 0.047 %. Each
twin column is a GPT-3 (`davinci`) prediction produced while holding that item out and supplying
the person's eleven other **true** answers, so these twins are *better* informed than our persona
twins, not worse: that confound runs against us. Its three twin versions vary decoding, not epoch,
and we never present them as survey waves.

No new data was collected. The attack uses only already-published content.

### 4.2 Methods compared

Twelve heterogeneous methods carry the quality-leakage analysis: 8 LLM twins and 4 statistical
reference points (Demographics Only, B1 argmax over 14 demographics, B2 argmax, PMM k=10).
Additional comparators appear in §5.2: logistic regression on context, a k=1 donor on context,
two individualised *generators* (sampled LR, Gaussian copula), and an explicitly advantaged k=1
donor fitted directly on the target block. Sequential CART and a 300-tree forest were tried
before that donor and abandoned at 0.45–0.53 accuracy: the retained comparator was not chosen to
lose. On the Argyle archive the comparators are **B-demo**, a leave-one-out imputer on the four
demographic items, and **B-oracle**, the same imputer given the person's eleven other true
answers — the comparator matched to that archive's own conditioning.

### 4.3 Metrics

*Attacks.* Two matching rules are used throughout, and every rate is labelled with the one that
produced it. The **naive** attack ranks candidates by Hamming-type agreement over common items.
The **strong** attack (A-LLR) instantiates the Narayanan–Shmatikov rarity-weighted
log-likelihood [narayanan2008robust], whose parameters we estimate **out-of-fold over 5 folds**.
A third variant (A-MI) scores higher still on the Park archive but estimates its weights **in
sample**, an advantage declared in the preregistration, so we never report it as our result. An
**adaptive** attacker, used only against the defense (§6.1), additionally knows the mechanism and
which items it leaves untouched.

*Closed-world top-1 and top-10*: rank of the true target among all N candidates by the rule
stated. *Open-world*: true-positive rate against false-positive rate, where the system may decline
to accuse (§5.3). *Bits of identity*: log2 of the ratio of correct one-shot guessing probabilities
before and after conditioning on the persona — a Rényi min-entropy leakage quantity
[smith2009foundations]. *Imitation quality*: the share of the human test-retest floor attained.

Unless stated, intervals are 95 % bootstrap confidence intervals resampling persons, not methods:
an interval on a quantity computed across the twelve methods is conditional on those twelve and
does not generalise beyond them. Intervals that resample something else — sub-pool or
tie-breaking draws, nulls — are not confidence intervals on the rate, and are labelled where they
appear.

### 4.4 Preregistration and self-refutation

Attack, defense, mechanism, the two archive replications, the disjoint-item test and the
distance law were each preregistered before computation, and we report every refuted prediction
in Table 1. A census found **no inversion** between a plan and its result across the 28
verifiable pairs; for the large majority the ordering is provable from version-control history,
while a small number were committed alongside their results or left unversioned; we state this
as a limit rather than claim an unbroken chain. The plans are not yet third-party timestamped.

### 4.5 Validity controls

*Provenance.* On all three archives we verified that the attacker's context cannot contain the
attacked answers and that no twin copies an earlier wave. Counts, rates and the argument for each
archive: the appendix.

*Empty-run validation.* Uniform ranks yield 0.00 bits; the B0 mode baseline yields
−0.004 [−0.003 ; 0.002] bits.

*Interpretability control, adopted after it cost us an experiment.* We state as a rule the control
whose absence invalidated two of our own arms (§5.4): **no experimental arm is interpretable until
its candidate pipeline has been shown to beat the demographic baseline in top-1 against the real
human answers**, on the pool and items actually attacked, with the baseline recomputed on those
same rows rather than carried over as a constant. The check consumes no model call and must
precede the first paid contrast; a pipeline that fails it yields twins whose contrasts oppose
noise to noise and return chance whatever is manipulated. It has since excluded our own pipeline
B, all three GPT-3 twins of the Argyle archive (§5.8), and the Park archive's `persona` condition
(§1.3). Baselines are always taken at the pool size of the arm they judge, being strongly
pool-dependent (§5.4); **and a baseline is only as weak as the attributes it is given** — the Park
archive's is not, in that sense, a demographic baseline at all (§5.8).

---

## 5. Results

### 5.1 The coupling, and the null that absorbs it

Across 12 heterogeneous methods, the ordering by imitation quality and the ordering by
re-identification rate nearly coincide. Three rank correlations appear for that statement, and
they are three measurement plans, not three estimates of one number: raw accuracy on whole items,
the preregistered disjoint-item test over 50 stratified A/B splits of the 60 items — **0.969**
[0.937 ; 0.993], 100 % of splits above 0.7, **prediction (a) confirmed**, the relation is not an
artifact of recycled computation — and **0.965** on Figure 2's axis (`fidelite_plancher`), the
value the null below is compared against. All these intervals resample **people within each
configuration** and hold the 12 configurations fixed; they are conditional on this set of methods
and do not generalise. Resampling the **configurations** — the unit the claim is about — widens
the interval substantially without changing its sign, and a permutation test rejects independence;
these witnesses are post-hoc, and are reported in full in the appendix.

Prediction (b) was refuted, and the witness that refutes it has since been rebuilt to remove a
real defect without changing the verdict: its *wrong* cells avoided the person's true answer
(`c7_disjoint.py` l. 133), inflating its leakage by a factor 1.3 (41.2 % against 31.6 % once
wrong values are drawn from the population marginal). Corrected, it still reproduces the coupling
— **rho {{R:rho-nul-marge-appariee-12conf-n100}}, 5th–95th percentiles {{R:rho-nul-marge-appariee-12conf-n100.ic}}, against 0.965 observed** over the 12
configurations, 100 replicates as preregistered (Figure 2) — so
**prediction (b) remains refuted**. It is not an information-free object, and we do not describe
it as one: at matched accuracy it leaks **more** than our twin (31.6 % top-1 against 20.7 %).

We therefore do not claim, anywhere in this paper, that a twin's fidelity to its person causes
its leakage, nor that fidelity and identifiability are one axis, nor that at equal accuracy every
twin leaks more than every predictor: the residuals of the regression on accuracy do **not**
separate the families, 3 of 7 LLM configurations falling below the line. One positive point
remains testable outside this circularity: the human retest dominates the best twin on both axes
— 0.303 against 0.154 and 0.520 against 0.067 on the disjoint-split scale, 81.6 % against 20.7 %
of closed-world top-1 on Figure 2's — so there is no saturation at the top of the range. The two
scales are not interchangeable and nothing here mixes them.

*Limits.* Raw accuracy is only a noisy proxy (r = 0.72, p = 0.008) for the right axis, and
Spearman is coarse at n = 12 — the null touches 1.000 through small-sample effects — so the
verdict concerns the order of magnitude, not the third decimal.

### 5.2 Closed-world rates and the comparator question

At comparable marginal accuracy, no non-LLM predictor we tested comes near the twin: the
strongest of them reaches **0.45 %** top-1 (the persona-conditioned comparator of the next
paragraph) where the
twin reaches {{R:twin-top1-ferme-json41-naif}} % {{R:twin-top1-ferme-json41-naif.ic}} under the naive attack and **{{R:twin-top1-ferme-json41-fort}} % {{R:twin-top1-ferme-json41-fort.ic}}** under the
strong one — **in a closed world, with the target always present in a pool of 2,058**. The
comparator figures are naive-attack rates, which makes the contrast conservative. JSON Persona
GPT4.1 attains that rate at accuracy 0.590; the six comparators, at comparable accuracy, all sit
at or below **0.25 %** top-1 — among them two individualised *generators*, which answers the
objection that we oppose an individualised generator to predictors that regress to the mean. Each
rate with its interval: the appendix.

**At strictly equal input information the gap holds, and that is the form of the claim we
defend.** Given the 634 wave-1–3 columns the persona is made of — from which the 60 attacked
items are absent — the best classical generator conditioned on the individual reaches **0.45 %**
[0.20 ; 0.76] against **{{R:twin-top1-ferme-json41-naif-audit-comparateur}} %** {{R:twin-top1-ferme-json41-naif-audit-comparateur.ic}} for the LLM twin, both terms from one run. A twin conditioned on the
**demographic segment alone**, not on her past answers, still reaches **2.15 %**
[1.57 ; 2.77] — **4.7 times** that best classical comparator, itself fed the individual. The gap
is therefore not attributable to the input information. *(Post-hoc, not preregistered.)*

**Is any of it individual? Three levels, one run.** The standing objection is that a realistic
answer vector identifies by its structure alone. A **real human** answer vector borrowed from
another person — realistic inter-item dependence, no information about the target — re-identifies
{{R:decomposition-vecteur-humain-top1}} % of people and does not separate its target from another
member of the same segment (AUC {{R:decomposition-plancher-auc-intra-segment}}
{{R:decomposition-plancher-auc-intra-segment.ic}}, where 0.5 is no trace); forcing it into the
**right** segment takes it only to {{R:decomposition-vecteur-humain-segment-top1}} %
{{R:decomposition-vecteur-humain-segment-top1.ic}}, an interval still containing zero. The twin
reaches {{R:decomposition-persona-top1}} % {{R:decomposition-persona-top1.ic}} in that same run and
keeps its advantage **with the segment held constant**: AUC
{{R:decomposition-persona-auc-intra-segment}} {{R:decomposition-persona-auc-intra-segment.ic}}.
Crediting the non-individual level with the whole 2.15 % — too generous, those **fourteen**
demographic questions taking {{R:demographics-only-cellules-distinctes}} distinct joint values
across the panel, a quasi-identifier and not a group — the person's share of the rate is
{{R:decomposition-part-personne-taux}} %; on the bits-of-identity scale the same attribution gives
{{R:decomposition-part-personne-bits}} %, the non-individual level there weighing *more* than the
person. **We publish both, because a share of this kind is meaningless without its scale.**
*(Post-hoc, not preregistered.)*

We then gave a comparator an explicit advantage: a k=1 nearest-neighbour donor fitted **directly
on the target block's answers**, seeing what the LLM twin never sees. It carries genuine individual
signal and, despite that, obtains a top-1 of **0.00 % [0 ; 0.18]** (Clopper-Pearson, n = 2,058).
**This claim does not generalise to every leakage metric, and top-10 runs the other way**: that
same advantaged comparator reaches a top-10 of **53.2 % [51.0 ; 55.3]**, *above* the twin's
42.7 %, so the direction of the whole contrast depends on the choice of k, which no principle
fixes at 1. We claim neither that all individualised prediction identifies nor strict accuracy
equality — the generators plateau at 0.476. Neither synthpop/CART nor CTGAN was tested. The
donor's accuracy and its within-segment permutation witness: the appendix.

### 5.3 Open world — the defensible measurement

Removing the closed-world assumption gives the number we consider hardest to attack in review. At
a false-accusation rate of 1 %, the strong attack (A-LLR, parameters estimated out-of-fold over
5 folds) recovers the right person **{{R:twin-tpr-fpr1-fort-ouvert}} % {{R:twin-tpr-fpr1-fort-ouvert.ic}}** of the time on Twin-2K-500, the dataset that carries the
claim, and **{{R:park-tpr-fpr1-fort-ouvert}} % {{R:park-tpr-fpr1-fort-ouvert.ic}}** on the Park archive, under a person-level bootstrap that **re-estimates** its
parameters in each resample, every copy of a person staying in one fold. At FPR = 0.1 % the
quantity is **not identified by the data** — the threshold there rests on one or two absolute
false positives, and hundreds of admissible thresholds span almost the whole range of attainable
detection rates — so **we report no point estimate at that FPR**. At FPR = 1 % the same
construction is stable, and **the headline figures are the ones at 1 % FPR**; the threshold census
establishing both statements is in the appendix. The human ceiling at FPR = 1 % is {{R:plafond-humain-twin-tpr-fpr1}} % {{R:plafond-humain-twin-tpr-fpr1.ic}} on Twin and {{R:plafond-humain-park-tpr-fpr1}} % {{R:plafond-humain-park-tpr-fpr1.ic}} on Park.

**Statistical comparators stay indistinguishable from noise at both FPRs on Twin-2K-500 — and
only there.** Replayed under the same strong attack as the target, Twin's demographic comparator
gives 0.00 % TPR at 0.1 % FPR and **0.0486 %**, one person, at 1 % FPR, below its own naive
value, so the 4.28 % stands clear of it; PMM k=10 stays at 0.00 % on both archives under both
attacks. On the Park archive the demographic comparator is **not** at noise once armed with the
same attack — 29.09 % at 1 % FPR — which is why that archive no longer carries this paper's claim
(§5.8). These witnesses are post-hoc.

**These figures replace the ones we first published, and the correction runs in both directions.**
The naive attack gave {{R:twin-tpr-fpr1-naif-ouvert}} % and {{R:park-tpr-fpr1-naif-ouvert}} % at 1 % FPR. On Park the
strengthening is statistically clear at that FPR — no overlap, the rate **triples**. **On
Twin-2K-500 the apparent gain does not survive its interval**: 3.04 → 4.28 % overlaps broadly, so
we do not present the strong attacker as identifying better than the naive one here.

**Our preregistered prediction was refuted, and one half of it then reversed by a better attack**
(> 5 % Twin, > 30 % Park; Table 1, row 2).

> **Figure 1 — Open-world detection, naive and strong attack
> (`article/figures/fig1-monde-ouvert.png`).** Two panels, one per dataset,
> false-accusation rate on a log scale against true-detection rate. Each overlays the naive
> Hamming attack as a full ROC curve with the strong A-LLR attack as **isolated diamonds** at two
> thresholds only (FPR = 0.1 % and 1 %): **no curve should be read into the diamonds.**
> On Twin-2K-500 comparators sit near zero; on the Park archive the armed demographic comparator
> does not (§5.3). The human retest ceiling sits above.

### 5.4 The twin-to-twin channel within one pipeline, what governs it, and why our T2 test does not count

Two twins of the same person designate each other when they share enough items, with no real data
on the attacker's side. The measurements below share one team and, for Twin-2K-500, one persona
source per person: they gauge the channel inside a pipeline, not T2 (§3).

**Twin-2K-500, tabulated by common-item count**. At 60 common items the channel is large and its
size badly determined: **six** configurations give **30** ordered pairs running from **11.9 %** to
**83.6 %** top-1, mean **36.4 %**, 95 % CI **[24.7 ; 56.5]** clustered by configuration — the
independent unit is the configuration, not the pair, as elsewhere here, so the interval rests on
**six** units and spans a factor above two. **We never give that mean without its range and its
six units, and never as a typical value.** 12 pairs sharing 19 common items: mean top-1
**0.45 %**. The anti-artifact control, a decoy from the same segment, stays at or below **0.10 %**
on both item regimes (the appendix).

**Park archive replication**: 1,052 agents, 177 common items, top-1 **11.9 % [10.1 ; 13.8]** and
**13.0 %** in the two directions, against a decoy control **at most 0.31 %**. **Preregistered
prediction refuted**: we set a threshold of at least 20 % top-1 there and 11.9–13.0 % does not
reach it, though the preregistered *failure* criterion is not met either (the appendix).

**We never report a single figure for this channel without its common-item count**; a previously
circulated average of 26.11 % pooled the two item regimes and is withdrawn. Nor do we claim
leakage crosses waves: that arm is infeasible, with 0 items in common.

**The channel is not an artifact of a shared prompt template or of demographics.** Decomposing
agreement between two twins of one person over the 60 common items, the person contributes
**82 %** of the rise above the floor between *strangers*, the demographic-ideological segment the
rest; a pure-population witness identifies the right person **0.07 %** of the time (the appendix).

**The cross-dataset anomaly, explained in part.** Park shares three times Twin's items and leaks
roughly three times *less*, and neither item count nor pool size accounts for it: the 177 GSS
items are strongly redundant, and shrinking Twin's pool to Park's *raises* its top-1 rather than
lowering it. **A residue of roughly 3× remains unexplained**, the remaining candidates — persona
format and length, and the generating pipelines — not testable on what we hold. The same
denominator places the third dataset far below both (§5.8; the appendix).

*Limits.* The 12 low pairs are exactly those at 19 common items, so the effect follows the
shared-item count rather than an aberrant configuration. On Park the item-rate relation does not
follow Twin's.

**T2 itself: two genuinely independent pipelines, and a test that does not count.** Two pipelines
sharing nothing but the target person — JSON dossiers against narrative biographies, distinct
models — were matched on the same 60 items (n = 142, stopped by a transport error), giving top-1
{{R:deux-organisations-BC-top1}} % {{R:deux-organisations-BC-top1.ic}} against a demographic
baseline of 9.2 %. **We no longer read this as a refutation.** Neither arm produces twins that
identify the real person better than chance on that pool, where the Twin team's own twins reach
20.2–38.9 % (the appendix), so the comparison opposes two noise sources: it measures our
instrument, not the world. The 36.4 % above, a same-pipeline measurement, is not evidence for T2
either, so T2 stands open both ways.

**Which element differs, not how many — and a preregistered law our own measurements refute.**
Among the six Twin-2K-500 configurations that pass the interpretability control, changing a single
published pipeline descriptor gives **{{R:loi-distance-decodage-top1-d1}} %** for decoding alone, **{{R:loi-distance-gabarit-top1-d1}} %** for the prompt template, **{{R:loi-distance-raisonnement-top1-d1}} %**
for reasoning and **{{R:loi-distance-modele-top1-d1}} %** for the model. We preregistered a
*distance law* — leakage falling with the number of published descriptors that differ — and our
own measurements refute it: Spearman **−0.232** [−0.321 ; −0.187] over 15 pairs, **+0.003**
[−0.047 ; +0.068] once the two twins' individual fidelity is controlled, against the −0.7
predicted. At a distance of one, rates span 17 % to 81 %: the spread *within* a level dwarfs the
spread *between* levels. Counting changed components predicts nothing useful; that *naming* them
would, four one-off contrasts cannot establish.
On Park the same control leaves three pairs, so no replication is possible. Two limits bound this
verdict — arbitrary distance weights, and a small number of independent configurations — and are
stated in the appendix.

**One-factor-at-a-time from our own pipeline is arithmetically sound but not interpretable.**
Pipeline B and all three conditions derived from it identify the real person at chance, so each
contrast opposes two noise sources: we withdraw both the reading we first gave those rates — that
changing any single component collapses the channel — and the refutation of the matching
preregistered prediction.

### 5.5 Mechanism: being right while deviating — and three refuted hypotheses

What identifies is neither the frequency of departures from the modal answer nor answer
diversity, but their **correctness** — and the whole response vector is required. Correctness of
deviations ranks the four objects exactly as leakage does, from 68.5 % for the human retest down
to 39.1 % for PMM, which deviates and diversifies as much as the twin without leaking. The four
values with their leakage rates: the appendix.

The ablation is the strongest evidence: permuting the order of each twin's 40 purchase answers
drops closed-world top-1 from **{{R:twin-top1-achat40-ablation-avant}} % {{R:twin-top1-achat40-ablation-avant.ic}} to 0.046 % [0 ; 0.11]**, below chance, and
an oracle given only the count of "yes" answers gives 0.29 %. What identifies is the dependence
structure between answers, not any answer in isolation. That ablation starts above this paper's
headline 20.7 % because it attacks the **40 purchase items alone** where the headline uses all
**60**: the 20 opinion items identify 46× less and dilute a naive Hamming rule rather than help
it. That is a change of attack surface, not a discrepancy.

**Three preregistered hypotheses refuted** — H1 (per-item entropy drives identification), H4
(twins are more stereotyped than humans) and "deviations alone carry ≥ 80 % of the leakage":
Table 1, rows 5–7, with each comparison and its interval in the appendix. We do not present
"wrong deviations alone = 0.0 %" as a result: it is a floor of the method.

**The effect is concentrated, and three convenient explanations are now excluded.** The gap is
carried entirely by the 40 purchase items: the twin re-identifies **{{R:twin-top1-achat40-audit-comparateur}} %** {{R:twin-top1-achat40-audit-comparateur.ic}} of
people there, against **0.08 %** [0.00 ; 0.20] for the best classical comparator explicitly fed
the persona columns bearing on consumption and price; on the 20 heuristics-and-biases items the
twin (0.24 %) does not exceed **that same persona-conditioned classical generator** (0.51 %) —
against the demographic baseline recomputed on those same 20 columns (0.00 %) it is above, and
**the two statements name different comparators**. This concentration is **not a content effect** —
the persona names none of the 40 brands and none of the 40 products, and overlaps the purchase
block's vocabulary *less* than the heuristics block's — and it is **not explained by instability
of the heuristics items**, which remain reliable in humans: normalised by the top-1 a human
answering the same items twice achieves, the twin reaches **44 %** of that rate on the purchase
items and **1.5 %** of it on the heuristics items. **That pair is a ratio between two
re-identification rates, not a decomposition of identity information**: it shows the block gap
survives dividing by the human ceiling, and names no quantity the twin carries — the mechanism
below stays a named residue. Token overlaps and test-retest kappas: the appendix.

**The mechanism is open, but bounded — six explanations are excluded by matched tests rather than
by argument.** Item family and modality count cover almost the same partition of the 60 items
(Cramér's V 0.96), so we separated them by manipulation. Dichotomised to two modalities, the 20
heuristics items re-identify {{R:heuristiques-binarises-top1}} %
{{R:heuristiques-binarises-top1.ic}}, against {{R:achat20-apparie-top1}} % for 20 purchase items
matched on item count, modality count **and** entropy; symmetrically, the 40 purchase items
recomposed into 20 four-modality items, at exactly preserved information, still reach
{{R:achat-composites-4modalites-top1}} %. Modality count therefore has a real but second-order
effect, running the wrong way to explain anything. **The six excluded**: semantic contamination of
the persona, leakage of the spending level alone, response noise in the heuristics items, modality
count, per-item entropy, and position in the questionnaire ({{R:achat20-apparie-position-top1}} %
for purchase items matched on position). What stays open is the wording length, the test-retest
kappa, and the content of the questions; we propose no mechanism, and we do not offer the item
family as one — it is the name of the residue. *(Post-hoc, not preregistered.)*

*Limits.* The mechanism is established on Twin's purchase block alone and is in apparent tension
with the Park archive, where opinion items identify most, **at lower per-item entropy** (the
appendix). What remains is the block effect, the **best-supported hypothesis, not a result**.

### 5.6 Bits of identity: the instrument travels between our two datasets, the rate does not

An LLM twin costs about 0.4 bits of identity per point of accuracy gained, against 0.068 for the
best useful statistical comparator: Twin JSON 4.1 carries **3.55 bits [3.39 ; 3.72]** of a
log2 N = 11.01 ceiling and the Park composite **7.47 [7.27 ; 7.66]** of 10.04 (the other objects:
the appendix). Transportability is the point. Bits normalised by human entropy give 0.0439 (Twin)
against 0.0327 (Park) — a factor of **1.34** — where top-1 varies by a factor of **3.2**.
Demographics Only and PMM leak with **no accuracy gain at all**, a case a ratio alone would mask.
The instrument's validity is bounded on the other side by the third dataset, where a twin carrying
no demonstrable individual information has no ratio worth transporting (§5.8).

**A nuance against our own hypothesis.** The human retest has a ratio of 0.37 (Twin) and 0.44
(Park), as good as or better than the twins: the excess cost exists relative to statistical
predictors, **not relative to a human answering twice**.

*Limits.* The bits are a **lower bound** (dyadic bound plus Miller-Madow). The sum of per-item
mutual information is unusable as a total, as preregistered (the appendix).

### 5.7 The risk depends on the recipe — and we could not reproduce it

Our own twins, produced in a single call to cheap models from a raw profile, identify almost
nobody: 0.00 % to **0.83 % [0 ; 2.15]** across 7 cells, against 2.13 % for the other team's
Demographics Only. That interval **contains** 2.13 %, so no precise factor is established — only
the order of magnitude, that no model reaches 1 %. Any previously circulated "25× below" figure is
withdrawn. Memorization is not the explanation: llama31-8b, with a training cutoff preceding
publication, copies nothing verbatim and leaks no more than the models that do copy — a control on
our own twins, in a regime where none identifies almost anyone, which we do not extend to the
published twins of §5.2–§5.4 (§1.3).

**Two further preregistered predictions refuted** (Table 1, rows 8–9): R1 ≥ 10 % on at least 2 of
3 models, where no model reaches 1 %; and call granularity as the explanation, which is not
confirmed and is underpowered, with top-10 running **opposite** to the prediction. We claim
neither that leakage comes from the call format nor that the cause is identified. **It is not.**

**We then paid to test the obvious explanation, and it failed.** `openai/gpt-4.1` (Twin's own
model class) on Twin's per-item recipe without modification, 30 persons: accuracy **0.4722
[0.4361 ; 0.5050]** against Twin's 0.574; fidelity **0.1714** against their 0.708; top-1 and
top-10 **0.00 % [0 ; 11.57]** (Clopper-Pearson, n = 30). **One further preregistered prediction
refuted**: accuracy > 0.55; top-1 > 5 % is **not refuted**, its interval containing the threshold
— inconclusive for lack of power. We did not make the leakage come back because we did not reach
Twin's fidelity, and it is that gap, not the underpowered top-1, that carries the conclusion: at
the fidelity reached, the regression over the 12 points of `c7-compromis.csv` predicts **1.10 %**
[−9.15 ; 11.35], and the observed 0.00 % falls inside it.

**The unknown narrows instead of disappearing, and our failure to reproduce is explained rather
than informative.** Neither the model nor the call granularity: what remains implicated is the
**format and length of the profile**. Twin's full JSON persona runs to roughly 121,000 characters —
about 44,348 input tokens, sent whole in a single call — against our **8,000-character truncation**,
a ratio above fifteen in the information supplied. **Our locally regenerated arms were therefore
never an attempt to reproduce the upstream pipeline; they were a different experiment**, with their
own prompts, three distinct open models and a plain-text output. Their failing the interpretability
control says nothing about the reproducibility of the published arm, and **we do not present it as
a property of the procedure.**

*Limits.* n = 40 persons for the recipe arm, truncated to n = 10 on the per-item arm, and n = 30
on the paid frontier-model arm; a floor effect is not excluded. Transport failures and retries:
Open Science.

### 5.8 A second dataset, and a third at the other end of the trajectory

On the Park archive, the composite agent designates the right participant among 1,052 **in a
closed world** in **{{R:park-top1-ferme-fort-allr}} % {{R:park-top1-ferme-fort-allr.ic}}** of cases under the strong attack, top-10 97.8 %,
against a human retest ceiling of 96.8 %. **This replaces the 65.51 % [62.7 ; 68.3] we first
published**: a naive agreement attack understated this archive's leakage by 38 % in relative
terms. An in-sample information-weighted variant reaches 93.25 %, which we do not claim (§4.3).

**These Park figures are not evidence that the LLM twin leaks beyond demographics.** Armed with
the same rarity-weighted likelihood attacker on the same basin, the demographics-only comparator
reaches **85.17 %** [82.89 ; 87.26] closed-world and **29.09 %** TPR at 1 % FPR: a
target-to-comparator ratio of **1.06×** [1.030 ; 1.097] closed-world — a paired gap of **+5.2
points** [+2.7 ; +8.1], statistically resolved but 27 times smaller than the 29× obtained under
the naive attack — and **2.07×** at 1 % FPR. The reason is that the Park "demographics-only"
condition is conditioned on **eleven** attributes that leave **98.86 %** of the 1,052 respondents
unique in their own sample — a quasi-identifier block, not a demographic baseline — which a
rarity-weighted attacker converts into identity from the items: the same comparator reaches
3.84 % at 20 items and 22.74 % at 60.

**Twin-2K-500 carries the claim — and not because its comparator is thinner.** We armed Twin's
comparator exactly as Park's was and **tried to reproduce the collapse on the other dataset; we
failed, and that is the strong form of the result.** Twin publishes **fourteen** demographic
questions against Park's eleven, leaving {{R:twin-bloc-demo-unicite}} % of its 2,058 respondents
unique in their own cell against Park's figure above: a quasi-identifier block at least as identifying,
and **we do not claim Twin has none**. What differs is whether the attacked items **decode** it —
the same attacker realises {{R:park-items-part-plafond}} % of the attainable cell ceiling on Park
and {{R:twin-items-part-plafond}} % on Twin. Arming does not close that gap: seven enriched
comparators all land *below* the published Demographics Only condition (the appendix), which
therefore remains the strongest demographics-only comparator we can build here, so the published
ratio is **conservative**:
{{R:twin-rapport-cible-comparateur-le-plus-fort}}× {{R:twin-rapport-cible-comparateur-le-plus-fort.ic}}
closed-world, {{R:twin-top1-ferme-json41-fort}} % against {{R:twin-comparateur-demo-top1-fort}} %,
sixteen people; and {{R:twin-tpr-fpr1-fort-ouvert}} % against **one person** out of 2,058 at 1 %
FPR. **Nor is item count the sole reason Park collapses and Twin does not**, the narrower
attribution our own Park audit first drew: at 60 items and equal arming Park's comparator reaches
the same 22.7 % quoted above against Twin's {{R:twin-comparateur-demo-top1-fort}} %, a factor of
29, the second reason being the demographic loading of the items. **At 1 % FPR we publish no ratio** —
we had written 88× — by the rule this section applies to Argyle below: under 1 % the rate is fixed
by the tie-breaking convention, not by the data. We defend the paired gap there. We do not
withdraw Park, we requalify it: it demonstrates that linkage risk exists
**without an LLM twin at all**, as soon as a quasi-identifier block and enough items are
published together. A rate on this kind of corpus is therefore not comparable across studies
without declaring the number **and** the identity of the items, and the tie-breaking convention.
*(Post-hoc, not preregistered; audit of 13 September 2026.)*

The remaining conditions are **naive-attack measurements**, the strong attack not having been
re-run on them; the highest, interview-only at **44.7 % [41.8 ; 47.5]**, carries zero documentary
exposure to the survey, so it is the cleanest demonstration that an agent built from a
conversation alone identifies its person — and given what the strong attack did to the composite,
**it is a lower bound**. The other two conditions: the appendix.

We do not compare the Park and Twin rates as measurements of the same thing: item count, per-item
entropy and human ceilings all differ. The rates equalised at k = 60: the appendix.

**The third dataset, and the analysis that stops before it starts.** On the Argyle archive the
interpretability control **fails for all three GPT-3 twins**, and the preregistered decision rule
halts the analysis there: top-1 0.14 % [0.05 ; 0.27], 0.11 % [0.04 ; 0.20] and 0.09 %
[0.02 ; 0.22] against a demographic baseline of **0.10 %** [0.02 ; 0.23] recomputed on that same
pool of 2,148, all intervals overlapping. No contrast is interpreted, and the anchor-pool draws
were never computed: they would have interpreted noise. The verdict rests on no choice of items,
and the reason is visible per item: mean exact accuracy **47.2 %**, below the demographic
imputer's 51.5 % and below the modal answer on nine items of twelve. In bits the best of the three
sits at the level of Twin's *weakest* statistical comparator. The item-choice robustness, the bits
and their ceiling, and the paired comparison with a nearest neighbour given the same eleven true
answers: the appendix.

**Below 1 %, the rate is fixed by the tie-breaking convention, not by the data**: across the three
conventions the same twin ranges from exactly chance to more than four times the value we report,
and at **matched effective information both ends of the trajectory depend on that choice**. This
is why §1.1 reports a ratio to baseline and not a bare rate. Nor does the verdict rest on a weak
attacker: re-running the A-LLR attack that carries this paper's headline figures takes the best of
the three to **{{R:temoin-argyle-fort-top1-principale}} %** and its baseline to
**{{R:temoin-argyle-fort-top1-bdemo}} %** — still overlapping, still failing the control, the whole
gain **three** people out of 2,148. In the open-world metric that twin detects **one** person at
1 % false accusations and none at ten times that severity, at an AUC indistinguishable from zero:
the metric has no shape here, which is why the left end is read closed-world. These witnesses are
post-hoc, and the three conventions with their intervals are in the appendix.

**Two preregistered predictions were missed, and we count them as neither.** We had announced
top-1 2.5 % [1.0 ; 6.0] and normalised bits [0.020 ; 0.070] from our measured item and pool
curves; the observations, 0.14 % and 0.0044, fall far outside both. Neither the scale trend of
§5.9 nor the transportability claim is refuted by this, because neither is testable here: both
presuppose a twin that carries individual information. **We cannot distinguish "the trend
overstates leakage at a low effective item count" from "this twin is at the noise level", and we
do not pretend to.** Both rows sit outside Table 1's count, like the distance law of §5.4 — three verdicts
reached after the census of §7.1 was closed.

### 5.9 Scale: an observation on six pools, and no law

From N = 50 to N = 2,058, the twin/demographic ratio grows from **2.8 to 9.7** while top-1 falls
from 53.2 % to 20.7 % — naive-attack rates, the scale study not having been re-run under the
strong attack, and on intervals that span the sub-pool draws rather than the persons of §4.3.
**Six points do not carry a law: this is a measured trend, and we extrapolate to no pool size at
all** — not even the N ≈ 4,000 an earlier draft allowed itself. The power law and the logarithmic
law we fitted are reported only as the reason for that refusal: on those same 6 points they
already diverge at twice the measured range. The six pools, their rates and the two fits: the
appendix.

> **Figure 2 — Imitation quality against leakage, with its control
> (`article/figures/fig2-couplage.png`).**
> Abscissa: individual fidelity (`fidelite_plancher`, share of the human floor). Ordinate:
> closed-world top-1 leakage. Thirteen points — LLM twins, statistical reference points,
> Demographics Only, and the human retest at fidelity ≈ 1 / leakage 81.6 % — all with **error
> bars on both axes** from a per-person bootstrap of 2,000 resamples. **Inset**: the 5th–95th
> percentile envelope of the corrected marginal null (mean rho {{R:rho-nul-marge-appariee-12conf-n100}}, 100 replicates) as a grey band, with the
> observed rho (0.965) inside it: **the observed correlation sits inside the band that a null
> matched only on accuracy already produces** — the coupling is measured, not shown to be
> individual-specific.

---

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

---

## 7. Discussion and Limitations

### 7.1 The thirteen refuted preregistered predictions, one withdrawn, two inconclusive, and one untestable

Seventeen predictions were registered before computation; **thirteen are refuted.** Table 1, in
the appendix, gives each as written with its verdict and source. Eleven are also stated where they
were measured (§5.1, §5.3, §5.4, §5.5, §5.7, §6.1), so this count reads without the table. The
other two belong here: **per-item entropy does not rank items with a consistent sign across the
two datasets**, and **the cost per unit of individual fidelity, predicted roughly constant, is
not** (§7.2).

**Two of the thirteen went in our favour, and we mark them rather than bank them**: a stronger
attacker gains less than the 20 % relative we predicted on Twin-2K-500, and an adaptive attacker
knowing the mechanism fails to break the defense. A prediction refuted in the direction one hoped
for is worth less than one refuted against.

**Four verdicts left the count after they were written, each costing us a refutation.** That call
granularity explains the leakage, and that the frontier twin identifies more than 5 % of its
cohort, were first recorded as refuted on zero-event samples, where the exact intervals contain
the thresholds they were said to exclude: **inconclusive and underpowered** (§5.7). That two
organisations' independent pipelines leak into one another is arithmetically answered (§5.4), but
twins on both arms identify the real person at chance, so the contrast decides nothing: **not
testable, counted as neither.** That our defense dominates differential privacy at a moderate
budget is **withdrawn, not decided** — the comparison behind it was retracted (§6.2).

**The census: thirteen refutations, one withdrawn, two inconclusive, one untestable.** Three
further outcomes were partial and count as neither (§5.7, §6.3); one held outright, P2 (§6.1);
three verdicts reached after it closed are reported in place (§5.4, §5.8).

### 7.2 What we do not know

**An excess cost in bits per unit of fidelity, real but unexplained** (the appendix). With so few
points and no mechanism, it **must not be attributed to "LLMs" as a family**.

**We did not reproduce the leakage with our own twins** (§5.7), including with a paid frontier
model on Twin's own per-item recipe — an open limit, never a mechanism, and a narrower one than
before: neither the model nor the call granularity, leaving the persona's format and length. **Nor
can we reproduce the published arm itself**, whose generation parameters its authors have not
released (§4.1, §7.4).

**Whether the twin-to-twin channel crosses independent pipelines.** Everything we report on it is
measured inside a shared pipeline, and the arm built to decide the cross-pipeline case fails the
control of §4.5: **T2 is untested, not refuted** (§5.4).

**Why the effect concentrates on one block.** On Twin-2K-500 the whole gap lives in the 40
purchase items. **The mechanism is open, and we offer no candidate — but it is bounded**: six
explanations, semantic contamination and modality count among them, are excluded by matched tests
(§5.5).

**Rates do not predict across datasets.** The normal-maxima model lands close on Park k = 60 but
fails both its controls (the appendix): an isolated success between two failures is a coincidence,
not a law. Only conditional information retains sign and order of magnitude
across datasets (r = 0.72 and 0.89). The twin-to-twin channel's cross-dataset rate is likewise
only partly explained, a residue of roughly 3× surviving both controls (§5.4). And nothing we
hold separates the trajectory of §5.8 from the protocols that differ along it (§1.1).

### 7.3 Multiplicity

Most of this paper's central results are bootstrap confidence intervals around a descriptive
measure — re-identification rate, rank correlation, bits of identity — not classical hypothesis
tests; of the 34 **adjudicated tests** underpinning those claims at the time of the census (not
the 17 preregistered predictions — the appendix sets the three counts side by side), 11 were
refuted and 3 judged inconclusive, roughly one third, the opposite of the signature of data
dredging. **That rate controls the auxiliary family, not the headline**: none of 20.7 %, 90.40 %
and 60.17 % is a preregistered threshold — each is descriptive, chosen among competing metrics.
Holm and Benjamini-Hochberg were both applied to the 15 tests convertible to a p-value.
**Neither changes any verdict**, and the two agree on all 15: the p-values are bimodal, so no
claim here rests on a marginally significant result. The intervals carrying the other claims must
be read as measurements, each with its own margin, not as independent rejections of a common
null. The adjusted p-values, the full 47-test census across three families, and why it and
Table 1 do not carry the same totals: the appendix.

Three thresholds are fragile, and we name them rather than let a reviewer find them: the frontier
twin's
**fidelity > 0.10** bar, confirmed at 0.1714 but refuted had it been set at 0.18 — while our own
weakest known twin sits at 0.177; the choice of k in top-k (§5.2); and the functional form fitted
to the six scale points, which is why §5.9 extrapolates beyond them to nothing at all. A common
bootstrap across analyses reusing the same
2,058 people was abandoned for cost, so the intervals of §5.1–§5.3 on Twin carry no simultaneous
coverage.

### 7.4 Scope, a single generation, and two limits established by failure

**The headline rate rests on one generation, that generation is not ours, and it is not
reproducible as things stand.** The twins we attack were produced **once**, by the upstream team,
and **no replicate of that condition exists**. Worse for us, **the condition itself is not
identified**: the upstream repository publishes thirteen sets of outputs and one configuration
file describing a different arm (§4.1), so we can state neither model setting, temperature nor
prompt behind the rate we report. **Re-running the headline arm is therefore not something we can
price, only something the upstream prompt would unblock**; a paid pilot stopped there (the
appendix). The published interval [18.96 ; 22.43] is a bootstrap over *people*.
At strictly constant basin, items, attack and tie-breaking convention, the seven twin
configurations available at full sample span **2.13 %** to **20.68 %**, a range of
{{R:variance-etendue-bras}} points against {{R:variance-largeur-ic-titre}} points of interval
width, and {{R:variance-part-generation}} % of the observed variability is attributable to the
**configuration** against {{R:variance-part-personnes}} % to the people: our intervals measure that
hundredth with care and say nothing about the other ninety-nine. The arm we report is the
**maximum** of the eight measured and also the **most faithful** of them (accuracy
{{R:variance-bras-titre-exactitude}}, rank 1 of 8), which makes that maximum expected rather than
suspect; both facts belong together. **This figure must therefore be read as the rate of the most
faithful configuration we hold, not the rate of an LLM twin in general.** We do not claim the
generation variability is small: we did not measure it, and the decomposition above is a
**majorant** of it.

Three datasets, one language, one questionnaire format, categorical closed-choice answers only.
The mechanism analysis and the defense both rest on a single block of a single dataset, and we
make no claim about conversational agents or panels outside the three studied here. Two further
limits, each stated with the resource that would lift it.

**Generality beyond American attitude instruments, and the audit bottleneck.** All three datasets
are American survey panels built on neighbouring instrument families, so we cannot say whether
this channel is a property of that family — nor, as §1.1 states, separate the trajectory from the
protocols that differ along it. The obstacle is that the matched file — row-by-row, not by
demographic cell — is almost never redistributed: we verified three such datasets at the source and
ran no census, so no upper bound is established, and **on a typology of four cases and on no rate,
the risk appears to be created faster than it becomes auditable.** The four cases, and the
resource that would lift this: the appendix.

**Free-text outputs.** We measure nothing about free text, because **none of the three archives
publishes twin text** (the appendix, with the resource that would lift this). Every rate here
concerns closed-choice categorical answers, and we extrapolate in neither direction: the free-text
inference literature [staab2024beyond, ko2026weakcues] attacks a richer signal, so our figures are
no upper bound there.

---

## 8. Ethics Considerations

**Datasets, and the terms we are bound by.** Twin-2K-500 is public under CC BY 4.0 and the Argyle
archive under CC0 1.0. The Park replication package is publicly posted on OSF (node `t6g7k`), but
public posting is not a licence: the OSF API returns `node_license: null` for that node, so **no
licence is declared** and public access carries no right to redistribute the individual responses
it contains. Its questionnaire content is a General Social Survey instrument, and **NORC's terms
of use forbid reproducing the GSS in any form without prior written consent**. We record these
constraints because an article about privacy that passes over the terms of use of its own data
disqualifies itself.

*What we do in consequence, verified rather than assumed.* We redistribute no individual
response file from any of the three archives. We checked our own released material file by file:
the review artifact (§9) ships only code and a synthetic dataset generated at run time and reads
nothing from `data/`, which is excluded from version control; every published table under
`resultats/` is an aggregate by condition, by item or by bootstrap replicate; and the Argyle
analysis prints and writes no ANES case identifier and no individual match. Only analysis code
and disclosure-reviewed aggregates are published, with the NORC citation and attribution to Park
et al. Two limits we state rather than resolve: NORC's published terms address reproduction of the
GSS and do not speak to derived aggregate statistics, the reading that per-item aggregates fall
outside the prohibition being ours and not NORC's; and the ANES clause covering the public
variables the Argyle archive carries was not verified at its own source, the Dataverse deposit
itself being CC0.

No new data was collected: the attack uses only already-published content (human
answers and twin outputs). A limit to note: participants did not specifically consent to a
re-identification test on the twins generated from their answers.

**No individual is identified.** No identifier linking a record to a real person is published or
listed; only rates aggregated over the full cohorts are reported.

**No new harm on Twin-2K-500.** It already publishes, for each person, their identifiers and real
answers beside their twin: matching is trivial without any attack. The result documents a generic
risk for anyone releasing "anonymised" twins without that key — a practice Twin-2K-500 does not
follow.

**The Park archive is a different case, and we make no such claim there.** That argument rests
on a key published beside the twins and does not transfer: no trivial alignment makes the matching
free there, the rates are far higher, and the objects we attack are the very ones whose individual
release the authors treated as a privacy matter. What limits the harm is narrower: we publish no
individual record and no per-person result from that archive, only aggregate rates, and the
disclosure below is addressed to its authors, whose own warning this work quantifies.

**Benefit.** Several teams publish individualised LLM twin outputs without any linkage risk
analysis. This provides a first measured figure for that risk on public datasets, and a
reproducible method — attack plus interpretability control — for testing it *before* publication.

**Responsible disclosure, and its actual state.** Letters to the Twin-2K-500 authors and to Park
et al. are drafted, with a 30-day response window and an offer to share code and report in
advance. The tone toward Park et al. is fixed: *your warning was accurate, here is its measured
magnitude*. **As of this submission the letters have not been sent and the 30-day window has not
opened.** Sending them is on the critical path and is to happen before any preprint posting or
code release. We write this plainly rather than imply a consultation that has not taken place:
the committee should know the window was still closed when this manuscript was filed.

**The Park et al. case.** Their supplementary material already warned participants that their
information might be "inadvertently shared" and acknowledged that complete anonymity remains
challenging. They named the risk, obtained an ethics agreement worked over more than six months,
pseudonymised, restricted access to part of the material and planned a 25-year withdrawal. What
is nevertheless public is the replication package we analyse, which carries the 1,052
participants' individual responses together with the agent conditions' responses (§4.1): the
protection announced in the paper does not cover the objects this attack consumes. We flag that
gap as a question for the authors rather than a finding against them — from outside we cannot
tell whether the restriction was lifted or never covered the replication package — and it is
precisely what the disclosure letter must state correctly. No public audit had measured the
magnitude of that named risk; our figures (90.40 % closed-world, 60.17 % open-world at 1 % false
accusations, and 44.7 % from the interview alone, a lower bound) are, to our knowledge, its first
quantification — with the qualification established in §5.8, that an identically armed
demographics-only comparator reaches 85.17 % on this archive, so what is quantified is the
linkage risk the release carries and not a margin the LLM agent adds — and our own first
measurement understated it.

**Publishing the attack code.** *For*: replicability, and enabling other panel holders to test
their twins before publication. *Against*: it lowers the cost for an attacker already holding a
third-party panel's real answers and a corresponding twin file. *Our resolution*: publish,
because the code only acts if the attacker already holds real answers to the same items, and the
countermeasure is straightforward once the risk is known.

**Recommended defenses.** (a) Do not publish twin outputs item by item for blocks with high
inter-person specificity; publish aggregates or calibrated noise. (b) Break the person-twin
alignment in public files. (c) Publish regenerated twins without copying wave metadata
(`StartDate`/`EndDate`/`Duration`/`RecordedDate`). (d) Run a minimal linkage test, and the
interpretability control of §4.5, before any twin release: both are free, and the second says
whether the first can be interpreted at all. (e) Within-segment shuffling (§6), with its real
cost stated: {{R:defense-d4-cout-correlations}} points on inter-item correlations — a single permutation draw, and above the
{{R:dp-zcdp-plancher-correlations}} points of amplitude there was to destroy, so the component is destroyed in full (§6) —
a {{R:defense-d4-aggravation-ecart-humain}} % worsening of the gap to human
correlations (5.775 → 9.709), and the loss of every inter-item analysis downstream (§6.3) — and
with what it does not provide: **no formal guarantee**, and exact republication of each item's
within-segment histogram, so an adversary who knows a segment's other members recovers the
target's answers. It holds at 0.29 % against an attacker who knows the mechanism, but only for a
split that shuffles the informative block (§6.1). (f) Differential privacy where the published
object can be a population statistic rather than a per-person twin; we make no claim about its
cost relative to (e), having withdrawn the comparison we preregistered (§6.2).

**Public interest.** The AAPOR report of 8 May 2026 [aapor2026responsibleai] ranks synthetic
response generation as the most risky of the core tasks it evaluates and names re-identification
by linkage without quantifying it. A risk named by professional bodies but never measured
justifies an independent measurement followed by responsible disclosure rather than silence.

**Ethics review and scope.** This study was not submitted to an external ethics panel such as
an IRB. It relies exclusively on secondary data already made public by their original publishing
teams, and no new data was collected from any person: we surveyed no one, interviewed no one, and
had no contact with any data subject. On that basis we judged the study out of scope for
human-subjects review, with the limit recorded above — participants did not specifically consent
to a re-identification test on the twins generated from their answers. The scoping does not
extend to the released artifact, which processes no real person's data at all (§9).

---

## 9. Availability

**Review artifact.** `artefact/` replays the re-identification attack and its D4 defense in a
single command (`./artefact/run.sh`), **with no real data and no real person**, in about 25
seconds on a laptop, without GPU, network, or any language model call. It runs on a fictional
dataset of 600 synthetic persons at fixed seed with a tunable individual-signal dial,
structurally comparable to the real data (categorical items, product × price matrix block,
demographic segments, retest) but with different sample sizes and signal strength. It demonstrates
that the two mechanics are the ones running in the paper: `attaque.py` and `defense.py` import
their functions directly from `analyses/c7_reidentification.py` and `analyses/c7_defense.py`,
nothing is copied, the only function that reads real data is never called, and a guard refuses to
start if a path to `data/` is detected.

**No artifact figure is a result of this study.** The artifact's outputs (on fictional data:
21.9 % before defense, 0.842 % after D4) illustrate the mechanics and must never be cited as
study results.

**Underlying analyses.** Every quantitative claim in this paper corresponds to a dated analysis
script and result file under `resultats/` in this repository, organised to mirror the paper's own
section numbering. Individual file names are cited where a reader needs them to retrace a number:
in the Source column of Table 1, in the appendix entry giving each figure's data sources, and at
the few points in §5.1 and §5.7 where a specific script line is at issue; elsewhere they are
omitted to keep the manuscript readable.

**Bibliographic verification.** Of our 50 references, 23 carry an auditable source-verification
trace in the artifact; the remaining 27 were verified in an earlier pass whose record did not
survive. We state this as a limit rather than claim a fully audited bibliography. Full accounting
in `article/references-verification.md`.

**Transport failures and retries (§5.7).** Roughly 1,490 calls first failed with HTTP 402 from
in-flight credit reservation, not lack of balance, and were retried at decreasing concurrency
without double billing.

**What we cannot release about the headline arm's generation (§4.1, §7.4).** The Twin-2K-500 twins
we attack were downloaded as published; we hold no prompt, no configuration file and no generating
code for them, and none of ours reconstructs the headline arm. A paid pilot written to measure the
run-to-run variability of that arm stopped at this obstacle by its preregistered rule, having spent
under one dollar on input sizing alone, and its ledger, projection and stopping argument are
published in full. Its recommendation stands unchanged in this paper: the release that would lift
the limit is the upstream team's prompt and configuration, not a larger budget of ours.

**Differential-privacy implementation (§6.2).** The synthesiser was written by hand rather than
with a reference library, and is not full PrivBayes: per-item marginals perturbed by Laplace noise
(L1 sensitivity 2, budget split over 60 items, basic sequential composition) then sampled i.i.d.
per item, that is degree-0 PrivBayes with no joint structure. It was fitted on the human answers
and scored against the twin. Epsilon covers only the published histograms, with no composition
across the repository's other analyses, and correlations, between-segment differences and the
`S_gra` covariate are not protected. These are reasons the comparison of §6.2 is withdrawn rather than
corrected here; the corrected design — refitting on the twin, a composed Gaussian mechanism under
zCDP, and at least ten seeds with intervals — is specified in
`resultats/audit-comparaison-dp-2026-09-13.md`, section 9, and **has since been run**
(`analyses/c7_dp_zcdp.py`, `resultats/c7-dp-zcdp.csv`, ten replicates per budget): it is that run,
not the one described in this paragraph, that supplies every figure of §6.2. The withdrawal stands
regardless, and for a reason the rerun does not lift: what the corrected run measures is the cost
of our own reference implementation's independence assumption, which is not a ranking of the two
mechanisms in either direction.

**Obtaining the real data.** Twin-2K-500: Hugging Face repository `LLM-Digital-Twin/Twin-2K-500`,
CC BY 4.0. Argyle et al.: Harvard Dataverse `doi:10.7910/DVN/JPV20K`, CC0 1.0. Park replication
archive: OSF `https://osf.io/t6g7k/`, which carries real individual responses, is not
redistributed here, and is never read by the artifact — and whose two obstacles public
availability does not lift: no declared licence, and NORC's terms on the GSS content (§8). Obtain
all three from their original sources and verify current terms of use before any download.

**Preregistrations.** `resultats/c7-preenregistrement.md`,
`resultats/c7-defense-preenregistrement.md`, `resultats/c7-stanford-preenregistrement.md`,
`resultats/c7-argyle-preenregistrement.md` and `resultats/c7-loi-distance-preenregistrement.md`,
each written before any computation. Third-party timestamping is pending.

**Environment.** Python 3.13.14, numpy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0. No network
dependency.

---

## 10. AI Use

Large-language-model-based agents were used throughout this project: they wrote the analysis
code, ran the experiments, drafted this manuscript, and conducted adversarial review of both
the code and the text. We state this in full rather than narrowly, because an account that
understated that involvement would mislead a reader more than a plain one. The responsible
investigator directed the work throughout: set the research questions and the falsifiable
predictions in advance of each analysis, decided what to keep, discard, or redo, authorized all
paid computation, and is responsible for the accuracy and integrity of the submission. No
generative AI tool is listed as an author.

Three checks bear on how much trust the model-produced outputs warrant. First, quantitative
predictions were preregistered in writing, dated, before the corresponding analysis script was
run. Second, the analysis pipeline fixes a random seed at every stochastic step, and independent
reruns are checked to reproduce identical output before a result is reported. Third, the
manuscript and code were subjected to adversarial review passes whose default posture is
rejection; these passes are how two substantive defects were found and corrected before
submission: a statistical control meant to carry only each person's accuracy margin that in fact
copied their true individual answer with the complementary probability, and a bootstrap
confidence interval reported as "[0, 0]" on a zero-event sample, since replaced with an exact
Clopper-Pearson interval. These checks reduce, but do not remove, the risk that a model-produced
number or claim is wrong; the responsible investigator remains accountable for every figure and
statement in this paper regardless of how it was produced.

---

## Appendix

## Provenance and validity controls

**Provenance controls (§4.5).** On Twin-2K-500, the context contains 0 wave-4 columns and 0
wave-4 QIDs; maximum normalised mutual information between context and item is 0.16 against 0.31
for the retest on the same item. On cells where wave 4 differs from waves 1–3, the JSON 4.1 output
equals wave 4 in 37.7 % of cases and waves 1–3 in 37.9 % — symmetric, so no indication of copying.
On the Park archive, over 34,915 cells where the human changed their mind, the composite follows
wave 1 in 41.6 % and wave 2 in 43.2 %, and the 4.3–4.9 point wave-1 bias of the other three
conditions holds for the `demographic` condition too, so it is a shared calibration artifact, not
item leakage. On the Argyle archive each twin column is generated with its own item held out, so
no tautology exists on either side; the same holds for B-demo and B-oracle, whose target item is
removed from their context.

## Secondary measurements behind the results

**Why no archive permits a free-text measurement, and what would (§7.4).** The Park archive
publishes no transcripts, none of the 13 Twin configurations produces text, and the Argyle twins
are single recoded tokens. The missing resource is Park's complete transcripts, or a run of the
Twin pipeline that generates text.

**The audit-bottleneck typology, its four cases, and the resource that would lift it (§7.4).** Two
teams withhold their matched file (editorial choice or silence); a third is barred by its source
licence (SOEP); and one inverse case exists, synthetic outputs with no matched humans. The
resource that would lift the limit is a matched individual dataset outside GSS and Big Five whose
twins were built by a third-party team, under a licence permitting local computation and
publication of an aggregate rate; and, for the trajectory of §5.8, several model generations over
the same items and the same population.

**Park and Twin equalised at k = 60 (§5.8).** Park gives 34.0 % [23.5 ; 51.5] against Twin's
20.7 %, on 20 draws of a naive attack.

**How to read the two figures at a glance.** Figure 1: at a tenable false-accusation rate the risk
is real and, on Twin-2K-500, far above the comparators under both attacks, while on Park the
strong attack lifts the agent and its own comparator together. Figure 2: the points rise together
with no plateau at the top, but the observed correlation sits inside the null band.

**Figure data sources.** Figure 1: `resultats/c7-monde-ouvert-roc.csv`,
`resultats/c7-attaquant-fort.csv`. Figure 2: `resultats/c7-compromis.csv`,
`resultats/c7-compromis-robustesse-points.csv`, `resultats/c7-nul-corrige-marginal.csv` (inset
band: `variante=marginal`, `n_replicats=100`), `resultats/c7-nul-corrige.csv` (inset point, row
`rho_resume`/`reel`).

**The excess cost in bits per unit of fidelity (§7.2).** On equal samples, CV(bits/fidelity) =
0.436 against CV(bits/accuracy point) = 0.357 over the same 9 points.

**Cross-dataset prediction of rates (§7.2).** The normal-maxima model predicts 0.354 against
0.340 observed on Park k = 60, but 0.053 for 0.206 observed and 0.983 for 0.656 on its two
controls.

**The trajectory at matched effective information (§1.1).** At 4.3 independent items on both
sides, the same pool size, the same attack and the same tie-breaking convention, the twins of 2025
reach 0.34 % [0.29 ; 0.40] against 0.13 % [0.11 ; 0.16] for their own demographic baseline, while
none of the three twins of 2023 exceeds theirs. A second study of the item-count inflation factor
between 12 and 60 items puts it at 8.7 rather than the value quoted in §1.1. Relative to a
nearest-neighbour attacker holding the same items, the 2025 twin gains 1.26 where the 2023 twin
gains 0.96 — a difference we cannot separate from noise.

**Rank correlations, the first measurement plan (§5.1).** Fidelity taken as raw accuracy on whole
items gives {{R:rho-observe-12conf-memes-items}} {{R:rho-observe-12conf-memes-items.ic}}; the
other two plans are quoted in §5.1 itself.

**Bits of identity, the remaining objects (§5.6).** PMM carries 0.19 [0.16 ; 0.23] bits and B2
0.08. Demographics Only and PMM leak with an accuracy gain of −0.5 and −2.4 points. The sum of
per-item mutual information reaches 58.7 bits against a ceiling of 10.04 on the Park archive,
which is why it is unusable as a total.

**Defense, secondary values (§6, §6.1).** D4 leaves the within-segment multiset of each item
identical on 1,560 of 1,560 segment × item pairs. Against the adaptive attacker, segment-invariant
strategy S3 alone gives 0.05 %; naming the correct `S_gra` segment is at 6.8 % by chance.

**The twin-to-twin channel, further values (§5.4).** Individual pairs at 60 common items have an
SD of 18.6 points; chance at 19 common items is 0.05–0.10 %. The preregistered *failure* criterion
on the Park replication is not met either, the rate sitting at 5–8× the demographic bound. The 177
GSS items give ≈ 9.0 effectively independent items against ≈ 10.1 on Twin. The T2 arm used
`deepseek-v4-flash` JSON dossiers against `qwen-2.5-72b` narrative biographies, n = 142 of 200
planned. The paid frontier-model arm of §5.7 is 30 persons × 60 items = 1,800 calls at a 100 %
parse rate.

**Rank correlations, the configuration-level resampling (§5.1).** Resampling the **configurations**
— the unit the claim is about — gives **[0.749 ; 1.000]** for the first correlation, with 13.9 % of
draws at exactly 1.000, and a Fisher-z approximation gives [0.848 ; 0.989]; a permutation test
rejects independence at p < 10⁻⁴. These witnesses are post-hoc.

**One quantity, several runs (§5.2, §5.5).** Three rates in the body are the same quantity
measured in different runs, differing by the tie-breaking draw alone, and each is quoted beside
the term it is compared with so that both come from one run: closed-world top-1 of JSON 4.1 over
the 60 items, {{R:twin-top1-ferme-json41-naif}} % canonically and {{R:twin-top1-ferme-json41-naif-audit-comparateur}} % in the comparator audit of §5.2 (and
20.6 % in the deviations run whose bracketed rates §5.5 quotes); and top-1 over the 40 purchase
items, {{R:twin-top1-achat40-ablation-avant}} % {{R:twin-top1-achat40-ablation-avant.ic}} in the ablation of §5.5 against {{R:twin-top1-achat40-audit-comparateur}} %
{{R:twin-top1-achat40-audit-comparateur.ic}} in that same audit. None is substituted for another;
the registry carries one identifier per run.

**Three counts, and what each counts (§7.1, §7.3).** **17** preregistered predictions, the unit of
Table 1 and §7.1, of which thirteen are refuted; **34** adjudicated tests bearing on this
article's claims, of which 11 are refuted and 3 inconclusive; **47** adjudicated tests across
three families, of which those 34 are the first family. A preregistered prediction is written
before computation to be able to fail; an adjudicated test is any verdict the census could settle.
The refutation rates of the first two are therefore not comparable.

**Closed-world comparators (§5.2).** The six comparators of §5.2, in order: PMM k=10,
{{R:pmm-k10-top1-ferme-contre-examen}} % {{R:pmm-k10-top1-ferme-contre-examen.ic}}; B2 argmax,
0.07 % [0 ; 0.19]; k=1 donor on context alone, 0.13 %; LR on context, 0.22 %. The two
individualised *generators*, sampled LR and Gaussian copula, give 0.25 % [0.11 ; 0.41] and 0.22 %
[0.11 ; 0.36].

**Threshold census at FPR = 0.1 % (§5.3).** The threshold rests on a single absolute false
positive on Park and two on Twin, and on Park **538 distinct thresholds** sit within 1.5 false
positives of the target with TPRs spanning **0.10 % to 50.95 %**. The conservative step-function
value — the largest TPR whose FPR stays at or below the target — is **50.19 %** on Park and
**1.26 %** on Twin; we report no point estimate at this FPR. At FPR = 1 % the same construction is
stable: 10 and 20 absolute false positives, spans of 0.38 and 0.05 point.

**Twin-to-twin channel, secondary tables (§5.4).** Demographics Only against the rich twins gives
7.76 %. The anti-artifact decoy control gives 0.04 % on the 60-item pairs and 0.10 % on the
19-item pairs. On the Park archive, top-10 is 45–46 % and the demographic bound 1.5–2.5 %.
Decomposing agreement over the 60 common items: the floor between *strangers* is **46.0 %**, the
demographic-ideological segment adds **3.8 points**, the person adds **17.4**. On the cross-dataset
anomaly, the 177 GSS items give a real ratio of effective items of **0.89, not 2.95**, and
shrinking Twin's pool to 1,052 moves top-1 from 37.3 % to 44.1 %; the same denominator places the
Argyle archive at **4.31** effective items for 12 raw ones. In the T2 arm the two pipelines' own
twins reach 0.0 % and 0.8 % top-1 against 0.83 % expected on a pool of 120. Two limits bound the
distance-law verdict: the distance weights are arbitrary, and refitting them on the linkage rate
would make the measure circular; and the independent unit is the configuration — 18 pairs, 9
configurations, two teams.

**Mechanism, the three refuted hypotheses and the concentration controls (§5.5).** H1 (entropy):
opinion items carry 2.10 bits against 0.99 for purchase items and identify 46× less — top-1
0.24 % [0.07 ; 0.46] against 11.0 % [9.9 ; 12.3] for the purchase subset matched to them on
entropy, a 20-item comparison. H4 (stereotypy): 36.2 % [35.6 ; 36.8] against 37.5 %
[36.9 ; 38.1] in humans. "Deviations alone carry ≥ 80 % of the leakage": 0.68 % in the mixed
condition. On the concentration, the persona's vocabulary overlaps the purchase block *less*
(5.8 % of its distinctive tokens) than the heuristics block (38 %), and the heuristics items remain
reliable in humans (median test-retest kappa 0.365, no item below 0.25, against 0.672 on the
purchase items).

**Recipe arm, the top-10 reversal (§5.7).** On the call-granularity arm, top-10 runs **opposite**
to the prediction: 7.5 % for the single call against 0 % for the per-item call, where top-1 is
zero on both arms (Table 1, row 9).

**What separates the Park and Twin rates (§5.8).** The two archives differ in item count (177
against 60), in per-item entropy (1.30 against 0.99) and in human ceiling (96.8 against 81.6),
which is why we do not read their rates as measurements of the same thing.

**Scale, the six pools (§5.9).** The share of the human ceiling falls from 57.0 % to 25.4 % between
N = 50 and N = 2,058. The intervals are **not** the person-level bootstrap of §4.3: they span the
sub-pool draws, and at N = 2,058 no sub-pool is left to draw, so that row carries none. A power law
and a logarithmic law fitted on the same 6 points diverge at twice the range: 18.1 % against
13.9 %.

**Tie-breaking conventions and item-choice robustness on the Argyle archive (§5.8).** Ties resolved
in the attacker's favour give 0.61 % [0.33 ; 0.98], the uniform-draw expectation we report gives
0.135 % [0.045 ; 0.269], and ties resolved against the attacker give 0.047 % [0.000 ; 0.140] —
exactly chance for a pool of 2,148; the leading tie class holds 13 people, median 3 candidates.
Dropping age gives 0.08–0.13 % and the eight attitude items alone 0.09–0.11 %. The nearest
neighbour given the same eleven true answers carries 0.342 [0.301 ; 0.389] bits and a top-1 of
0.140 % [0.075 ; 0.218], against 0.135 % [0.045 ; 0.269] for the twin — a paired difference of
−0.005 points [−0.131 ; +0.137]. In bits the best of the three twins carries **0.094**
[0.074 ; 0.118] of an 11.07 ceiling, so the nearest neighbour carries 3.6 times more. On the Park
archive the two conditions not cited in §5.8 are survey-only, 20.6 % [18.2 ; 23.0], and
demographic, 2.26 %, both naive-attack measurements.

**The Park `persona` condition, stopped by the control (§1.3, §4.5).** It re-identifies 0.26 % of
participants against 0.39 % for demographics alone on the same pool.

**The Park tension on item families (§5.5).** At 20 items the Park archive gives 11.7 % against
0.24 % for Twin's 20 opinion items, at a per-item entropy of 1.30 against 2.10.

**Correctness of deviations, the four values (§5.5).** 68.5 % for the human retest (leakage
81.6 %), 50.3 % for JSON 4.1 (20.6 %), 43.3 % for Demographics Only (2.14 %), 39.1 % for PMM
(0.22 %).

**The advantaged donor comparator (§5.2).** The k=1 nearest-neighbour donor fitted on the target
block reaches accuracy 0.584 against the twin's 0.590, and carries genuine individual signal:
0.584 true against 0.442 under within-segment permutation.

## Detail behind the five audits of 13 September 2026

Each of the five audits below is published with its preregistration, its script and its result CSV;
this section gives the reasoning and the reservations, and the named files carry the tables.

**Three levels of signal, one run (§5.2)** — `resultats/c7-decomposition-signal.csv`. All
conditions share basin, items, attack and tie-breaking convention. Top-1 is reported under the
repository's convention, random tie-breaking averaged over 20 draws at a fixed seed, while the
**AUC with the segment held constant** counts ties as one half and depends on no draw, no seed and
no convention: that is why it, and not top-1, carries the verdict. The Demographics Only twin
discriminates even against each person's *nearest demographic neighbour*, who shares eleven of the
fourteen answers in median, where all three structure-only floors stay at chance — which is what
makes it a quasi-identifier rather than a segment. Under the more defensible reading of the segment
level, the borrowed human vector of the same segment, the two scales agree instead of diverging;
we publish the least favourable attribution. *What we could not verify*: the archive publishes this
configuration's outputs, not its prompt template, so we cannot assert that the fourteen
Demographics questions are exactly those passed to it. The weaker claim suffices — whatever its
prompt, this twin discriminates *inside* both of the repository's segmentations, so its input is
strictly finer than a demographic segment.

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

**Arming Twin's comparator (§5.8)** — `resultats/c7-audit-twin-comparateur.csv`. The fourteen
Demographics questions are QID11–QID24, none of them re-asked in wave 4. Restricted to the eleven
attributes homologous to Park's they leave slightly fewer Twin respondents unique than Park's block
does; at fourteen they pass it. The mechanism is measurable on the items themselves: Twin's
fourteen attributes shift the majority-response share of the attacked items over same-size random
groups by about a quarter of the shift Park's eleven produce. For the ratio to fall to the
collapse threshold of 2.0×, Twin's comparator would have to reach almost fifteen times the
published comparator.

**Separating item family from modality count (§5.5)** — `resultats/c7-audit-modalites-familles.csv`
and `resultats/c7-audit-contamination.csv`. The two descriptions cover almost the same partition:
all 40 purchase items have two modalities and one of the 20 heuristics items does. The dichotomised
conditions **do not pass the interpretability control** and are therefore not read as risk
measurements: they establish an absence of rise, which requires only that the comparison be
matched, and it is. The heuristics items are not response noise — none falls below a test-retest
kappa of 0.25, and they carry about twice the information per item of the purchase items, a
stability ratio far too small to produce the gap observed on the fraction of ceiling recovered.
Semantic contamination is excluded by a comparator fed the related persona predictors, which stays
near zero where the twin identifies a third of the block and the positive witness of the same
apparatus identifies most of it; the weak form — leakage of the spending level alone — falls with
it, since destroying the *pattern* of a twin's "yes" answers while conserving their *count* per
person collapses the rate. We do not present these two audits as independent confirmations: they
bear on the same columns, 39 items out of 40.

**Generation variance (§7.4)** — `resultats/c7-variance-generation.csv`. Of the 13 configurations
the upstream team published, 8 pass our provenance audit; 7 of those attack the full basin and
enter the variance computation, the eighth attacking a smaller sample and being reported for
information only. The arm we report is the maximum of all eight and of the seven. Both preregistered
thresholds are crossed — the range-to-interval ratio against a threshold of 2, the configuration
share of variance against a threshold of 90 % — and the verdict is unchanged when the periphery is
restricted to the six rich configurations. A substitute estimate built from item draws rather than
regenerations is reported there too; none of it measures re-generation variability at constant
condition.

**Why that variability is not merely unmeasured but unpriceable (§4.1, §7.4)** —
`resultats/c7-pilote-regeneration-resultats.md`. A paid pilot was run to measure it and **stopped
before the measurement**, by its own preregistered rule: the headline arm's configuration could
not be established from our repository or from the upstream sources, and the missing parameter is
the one that governs the quantity sought — at temperature 0 two runs are nominally identical, at a
higher temperature they genuinely differ, and the upstream configuration file and the upstream
paper do not agree, the file describing a different arm. Measuring the gap without that parameter
would have produced an interval on a pipeline of our own invention wearing the appearance of a
measurement of theirs. The pilot's full cost accounting is published with it, reconciled by two
independent methods. The cheapest way to lift this limit is not money: it is the upstream prompt.

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

## Multiplicity: adjusted p-values and the full census

**Multiplicity, the adjusted p-values and the full census (§7.3).** Of the 3 tests carrying a
classical p-value in the first pass, a Holm correction leaves the two smallest standing (0.002 and
0.008, adjusted to 0.006 and 0.016) and confirms the non-significance of the third. The second
pass extended the confirmatory family to 15 tests convertible to a p-value and applied both Holm
and Benjamini-Hochberg: the p-values are bimodal, eight at or below 0.0025 and seven already near
1. The full census covers 47 adjudicated tests across three families — the article's claims, the
standalone controls, the abandoned branches — with 25 confirmed and 15 refuted; its first family,
the article's claims, holds 34 of those tests, 20 confirmed, 11 refuted, 3 inconclusive. **None of
these three totals is the count of preregistered predictions**, which is seventeen (Table 1): an
adjudicated test is any verdict the census could settle, a preregistered prediction is one written
before computation to be able to fail. The census was written over the 15 `c7-*` sub-studies
existing at the time and excludes the verdicts added since, which is the second reason Table 1
and the census do not carry the same totals.

## The seventeen preregistered predictions, one by one

| # | Prediction (preregistered) | Outcome | Source |
|---|---|---|---|
| 1 | The quality-leakage coupling exceeds a null matched on accuracy alone | **Refuted.** Null rho {{R:rho-nul-marge-appariee-12conf-n100}} {{R:rho-nul-marge-appariee-12conf-n100.ic}} vs 0.965 observed, 12 configurations, 100 replicates as preregistered; the original null's defect is corrected, verdict unchanged (§5.1) | `c7-nul-corrige-marginal.csv` |
| 2 | Open-world > 5 % (Twin) and > 30 % (Park) at FPR = 1 % | **Refuted as first measured** (3.04 % and 20.39 %). Under the strong attack Twin still fails at 4.28 %, Park **passes** at 60.17 % — but that attack also takes Park's demographic comparator to 29.09 % (§5.8). Half refuted, half confirmed, one row | `c7-attaquant-fort-resultats.md` |
| 3 | Twin-to-twin top-1 ≥ 20 % on the Park archive | **Refuted.** 11.9–13.0 % at 177 common items (failure criterion not met either) | `c7-transfert-stanford-resultats.md` |
| 4 | The twin-to-twin channel leaks on the 19-common-item pairs | **Refuted.** 0.45 % mean top-1, at chance (0.05–0.10 %) | `c7-transfert-resultats.md` |
| 5 | H1: per-item entropy drives identification | **Refuted.** Opinion items 2.10 bits, identify 46× less | `c7-mecanisme-resultats.md` |
| 6 | H4: twins are more stereotyped than humans | **Refuted.** 36.2 % [35.6 ; 36.8] vs 37.5 % [36.9 ; 38.1] | `c7-mecanisme-resultats.md` |
| 7 | Deviations alone carry ≥ 80 % of the leakage | **Refuted.** 0.68 % in the mixed condition | `c7-deviations-resultats.md` |
| 8 | R1 ≥ 10 % on ≥ 2 of 3 of our own models | **Refuted.** No model reaches 1 % | `c7-gen-resultats.md` |
| 9 | Call granularity explains the leakage | **Inconclusive, underpowered.** 0.00 % both arms ([0 ; 8.8] at n=40, [0 ; 30.85] at n=10); top-10 runs opposite | `c7-recette-resultats.md` |
| 10 | Cost per unit of individual fidelity is roughly constant | **Refuted at equal sample.** CV 0.436 vs 0.357 on the same 9 points | `c7-compromis-resultats.md` §5 |
| 11 | Per-item entropy correlates with identifying power consistently | **Refuted.** Opposite sign by dataset: r = −0.81 (Twin), +0.57 (Park) | `c7-bits-resultats.md` §3 |
| 12 | P1: a stronger attacker gains ≥ 20 % relative over the naive attack | **Refuted on Twin** (+12.2 %, 20.7 → 23.23 %); held on Park (+38.0 %, 65.51 → 90.40 %) | `c7-attaquant-fort-resultats.md` |
| 13 | P3: an adaptive attacker knowing the mechanism breaks the defense | **Refuted, for the defense.** Plateaus at 0.29 %, never above 1 % | `c7-attaquant-fort-resultats.md` |
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Withdrawn, not decided.** The comparison is retracted: the DP generator was fitted on the humans and scored against the twin, and at eps = ∞ — no privacy — the cost was already the same (§6.2) | `audit-comparaison-dp-2026-09-13.md` |
| 15 | A frontier model on Twin's per-item recipe reaches accuracy > 0.55 | **Refuted.** 0.4722 [0.4361 ; 0.5050] | `c7-fort-resultats.md` |
| 16 | That same twin reaches top-1 > 5 % | **Inconclusive.** 0.00 % [0 ; 11.57] (Clopper-Pearson, n = 30); the 5 % threshold lies inside it | `c7-fort-resultats.md` |
| 17 | T2, independent pipelines: top-1 CI excludes the segment control and stays ≥ 2× the demographic baseline | **Not testable — counted as neither.** {{R:deux-organisations-BC-top1}} % {{R:deux-organisations-BC-top1.ic}} at n = 142/200, but both arms' twins identify the real person at chance: the contrast decides nothing (§5.4) | `c7-deux-organisations-resultats.md` |

---

## References

Bibliography maintained in `article/references.bib`; its verification status is stated in Open
Science (§9). Keys cited here, in order of
first appearance: `toubia2025twin2k500`, `park2024agents`, `bonagiri2026cognitive`,
`das2024blind`, `duan2024membership`, `zhang2024satml`, `ward2025synthmia`, `byun2025riskcontext`,
`platzer2021holdout`, `adams2025fidelity`, `giomi2023unified`, `gouweleeuw1998pram`,
`smith2009foundations`, `eckersley2010unique`, `rocher2025scaling`, `stadler2022groundhog`,
`annamalai2024linear`, `ganev2025inadequacy`, `ganev2026rethinking`, `ganev2024regulatory`,
`yao2025dcr`, `meeus2023achilles`, `golob2026sok`, `narayanan2008robust`,
`demontjoye2015unique`, `rocher2019estimating`, `taub2018differential`, `carlini2021extracting`,
`staab2024beyond`, `ko2026weakcues`, `lermen2026deanonymization`, `yeom2018privacy`,
`feldman2020memorization`, `bun2014fingerprinting`, `dwork2015robust`, `argyle2023outofone`,
`peng2026funhouse`, `guepin2023synthetic`, `shafieinejad2026diffusion`, `drechsler2024thirtyyears`,
`hu2023microdata`, `aapor2026responsibleai`.

