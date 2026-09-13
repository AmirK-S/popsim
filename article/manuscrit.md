# Linkability of LLM Digital Twins: From Chance in 2023 to 60 % in an Open World, and the Control That Says When Not to Measure

*Submission draft, PoPETs. Body target: 12 pages. Bibliography: `article/references.bib`.*

---

## Abstract

Published LLM "digital twins" — per-respondent simulated answer vectors released alongside
survey panels — are linkable to the humans they were built from, and that risk has a
trajectory. Measured on three datasets and three generations of models, re-identification did not
beat a demographic baseline with the twins of 2023 and reaches 60 % in an open world today.
On the GPT-3 twins Argyle et al. released in 2023, the strongest twin designates the right
respondent among 2,148 in **0.14 %** [0.05 ; 0.27] of cases against 0.10 % [0.02 ; 0.23] for a
demographic baseline recomputed on that same pool — intervals that overlap — the best of the
three carrying 0.094 bits of identity against a ceiling of 11.07, at a per-item accuracy of
47.2 %, *below* the modal answer; a nearest neighbour holding the same eleven true answers
carries 3.6 times more identity bits.
On twins built with recent models that attack reaches **20.7 %** [19.0 ; 22.4] on Twin-2K-500
(2,058 respondents) and, in a rarity-weighted variant, **90.40 %** [88.6 ; 92.2] on the Park et
al. archive (1,052 participants) in a closed pool, and in an open world at 1 % false accusations,
**4.28 %** [3.3 ; 5.6] and **60.17 %** [54.5 ; 64.4], against human test-retest ceilings of
54.5 % and 90.7 %. **The three datasets differ in team, protocol, item count (12 against 60 and
177) and pool, so "the risk grew with model capability" is confounded with "the protocols
differ"; we state that confound in front rather than resolve it.**
Inside a shared pipeline we report a twin-to-twin channel: two twins of the same person designate
each other with no real human answer held by the attacker — 36.4 % top-1 at 60 common items on
Twin-2K-500 and 11.9–13.0 % at 177 common items on the Park archive, against anti-artifact
controls of 0.06 % and at most 0.31 %. What governs that channel is *which* pipeline element
differs, not how many: at a single element changed, rates run from 17.2 % (model) to 81.4 %
(decoding), and the "distance law" we preregistered is refuted by our own measurements. Whether
the channel survives between *independently built* pipelines is untested: the arm meant to decide
it is not interpretable.
Our control is not new — it is the pre-spend, gating form of Anonymeter's control baseline — and
it costs nothing: no experimental arm is interpretable until its candidate pipeline beats a
demographic baseline against the real humans. It stopped two of our own paid experiments and the
Argyle replication.
We also report what we could not establish. We predicted, and preregistered, that the observed
coupling between imitation quality and leakage reflects an individual fingerprint; a null carrying
only a matched per-person accuracy margin — not a structure-free object, and one that in fact
leaks more than our own twin (31.6 % against 20.7 %) — reaches a rank correlation as high
as ours (0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed). Thirteen preregistered predictions were
refuted and one is withdrawn, two are inconclusive for lack of power, and one could not be tested; our own twins failed
to reproduce the leakage even with a paid frontier model. Finally, a 1998 mechanism (PRAM) applied
to twins brings closed-world top-1 from 20.7 % to **0.29 %** [0.10 ; 0.53] against the best
attacker we measured — one who knows the mechanism and attacks the block it leaves untouched — at
a measured cost of 4.4 points on inter-item correlations. It carries **no formal guarantee**: it
republishes each item's within-segment histogram exactly, so its zero distribution and group
errors are that republication, not a cost avoided.

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
[argyle2023outofone]. Attacked exactly as we attack the recent panels, those twins designate the
right person among 2,148 in **0.14 %** [0.05 ; 0.27] of cases, against **0.10 %** [0.02 ; 0.23]
for a demographic baseline recomputed on that same pool: the intervals overlap. The best of the
three carries 0.094 bits of identity against a ceiling of 11.07, per-item accuracy of 47.2 % sits
*below* the modal answer, and a nearest neighbour given the same eleven true answers carries
**3.6 times more identity bits**. Three years later, twins of the same kind of panel are
re-identified at 90.40 % in a closed pool and 60.17 % in an open world at 1 % false accusations.
The risk was not measurable in the first published generation of twins; it is substantial in the
current one.

**The confound, stated before the claim rather than after it.** The three datasets differ in
team, protocol, item count (12 against 60 and 177), pool and questionnaire. "The risk grew with
model capability" is therefore confounded with "the protocols differ" — and one term of that
confound we can size. On Twin-2K-500, holding team, model and attack fixed and varying only the
item count, top-1 runs from 1.2 % [1.1 ; 1.3] at 12 items to 20.7 % [19.0 ; 22.4] at 60, a factor
of **17.0**. That factor belongs to the protocol, not the models: the demographic baseline on the
same 2,058 people gains **7.4** over the same span. More items inflate whatever attacks, so the
quantity to report is the **ratio to the baseline** — 4.3-fold for the recent twins at 12 matched
items, where the 2023 twins do not demonstrably beat theirs, leaving a 2023 → today contrast of
**8.9×** (§5.8). How much of the rest the item count absorbs, we do not measure. Nor are the two
ends in one metric: closed-world top-1 under a naive Hamming attack at the left, true detections
at 1 % false accusations under A-LLR at the right, the second **undefined** at the left end,
where its open-world AUC is indistinguishable from zero. These witnesses are post-hoc. Lifting
the confound would need the same items, the same population and several generations of models
with individually matched twins; no such resource is public (§7.4). We state the trajectory as a
measured contrast between three published corpora, never as a causal effect of model capability.

One reading must be excluded. The Argyle result is **not a refutation of our scaling law**: it is
out of domain. That law predicts the leakage of a twin that carries a person, and our
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
Spearman **0.974**, 5th–95th percentiles [0.950 ; 0.993], against **0.965** observed over the 12 configurations; the observed value does not exceed it. Each null is compared
only against the observed value measured on its own plan. **Reproducing the coupling requires
nothing more than a matched per-person accuracy and correct positions drawn at random —
prediction (b) is refuted.**

We report this as a result rather than a confession. A recent line of work argues that an attack
on foundation models proves nothing until the null hypothesis is properly sampled: blind baselines
routinely beat state-of-the-art membership inference attacks [das2024blind, duan2024membership],
and a SaTML position paper makes the demand explicit [zhang2024satml]. The quality-leakage
coupling reported in prose by Ward et al. [ward2025synthmia] and Byun et al.
[byun2025riskcontext], and contested by Platzer and Reutterer [platzer2021holdout] and Adams et
al. [adams2025fidelity], has never been tested against such a control. We built it, and it
absorbs our own effect. What survives is not a theory of why twins leak, but a set of
measurements that do not depend on the coupling being individual-specific at all.

### 1.3 Contributions

**(1) A trajectory measured across three generations of published twins.** The same attack, under
the same control, on twins released in 2023, 2025 and 2026: below the demographic baseline then,
60.17 % in an open world now (§5.8), with the protocol confound of §1.1 forbidding any reading of
it as an effect of model capability alone.

**(2) A pre-spend stop rule, and what it cost us.** The discipline is not ours: Anonymeter builds
a control baseline into its risk estimate [giomi2023unified], and blind baselines demand the same
of membership attacks [das2024blind, zhang2024satml]. What is ours is the gating form, consuming
no model call and applied before the first paid arm: **no experimental arm is interpretable until
its candidate pipeline has been shown to beat the demographic baseline in top-1 against the real
human answers** (§4.5). It stopped two of our own paid arms (§5.4), the Argyle replication
(§5.8), and the `persona` condition of the Park archive — an agent built on a person's own
self-description re-identifies her *less* well than demographics alone, 0.26 % [0.06 ; 0.52]
against a baseline of 0.39 %.

**(3) A twin-to-twin linkage channel within a shared pipeline, governed by which element differs,
not how many.**
Two twins of the same person, sharing their persona source and differing only in model or output
format, designate each other while the attacker holds no real
human answer of any kind. On Twin-2K-500: 36.4 % mean top-1 over 30 pairs sharing 60 common
items, against an anti-artifact control of 0.04 %. On the Park archive: 11.9 % [10.1 ; 13.8] and
13.0 % [11.2 ; 14.9] in the two directions at 177 common items, against a control of at most
0.31 %; no number for this channel is reported without its common-item count. At one
pipeline element changed, the rate runs from 17.2 % (model) to 81.4 % (decoding), and the
*distance law* we preregistered — leakage falling with the number of differing components — is
refuted by our own measurements (§5.4). Anonymeter's low linkability figure is not a
counter-result: it is an excess over a control, measured on aggregate tabular releases whose
records stand in no one-to-one relation to individuals, where a twin release is one record per
person by construction [giomi2023unified] (§2.1). Built end-to-end independently instead (T2, §3),
top-1 falls to 1.8 % [0.4 ; 3.6] — but that arm is **not interpretable**, its own twins
identifying the real person only at chance, so T2 remains untested.

**(4) The leakage is localised in the pattern of answers, not in memorised content.** An
ablation destroys the signal by permuting the order of a twin's answers while leaving their
content untouched — 33.1 % to 0.046 % top-1 (§5.5): what identifies is the dependence structure
between answers, not any answer's content.
The pipeline also trains nothing on the target population, so no train/test gap exists to exploit,
unlike Yeom et al. [yeom2018privacy] and Feldman [feldman2020memorization]. Our training-cutoff
control lives in a regime where none of our twins identifies almost
anyone (§5.7), so **we do not claim a measured dissociation between memorization and
re-identification.** That narrower claim — a structural mechanism, localised by
ablation — is what separates our channel from the memorization [carlini2021extracting] and
free-text inference literatures [staab2024beyond, ko2026weakcues, lermen2026deanonymization].

**(5) The Narayanan–Shmatikov attack, instantiated on twins, with its human ceiling.** Both moves
are theirs [narayanan2008robust]: the rarity-weighted likelihood score, and the out-of-sample
criterion that drops the closed-world assumption that the target is in the pool and reports true
detections against false accusations (§5.3, Figure 1). New here are the object, the pool, the
human ceiling, and out-of-fold estimation of the weights. So instantiated, the attack raises the
Park archive's closed-world top-1 from 65.51 % to 90.40 % and triples its open-world rate at 1 %
false accusations — a correction of our own published figure (§5.3, §5.8).

**(6) A defense measured with its real cost, and held against an adaptive attacker.** Not a new
mechanism — a variant of the 1998 Post Randomisation Method [gouweleeuw1998pram] — but applied to
LLM twins with a risk-utility curve that is measured rather than assumed, tested against an
attacker who knows how the defense works, and reported with what it does *not* protect: it offers
**no formal guarantee**, and republishes the within-segment item histogram exactly (§6). We
preregistered a comparison with differential privacy and **withdraw it**: our DP implementation
was a straw man scored against a mismatched reference, and at eps = ∞ — no privacy at all — the
cost was already the same. We claim no superiority over differential privacy (§6.2).

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
what the Twin-2K-500 recipe does differently. And the coupling that motivated this work does not
survive its own control (§5.1). We consider a reader who stops here to have read the paper
honestly.

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

*What distinguishes us.* This corpus concerns tabular microdata from classical generative
models, evaluated by continuous similarity metrics. Our object is a vector of categorical answers
produced by an LLM conditioned on a person, where no similarity metric substitutes for a direct
matching attack.

### 2.2 Re-identification of real data

Narayanan and Shmatikov re-identify Netflix users [narayanan2008robust]; de Montjoye et al.
show four spatio-temporal points suffice on credit-card metadata [demontjoye2015unique];
Rocher, Hendrickx and de Montjoye model risk on incomplete samples [rocher2019estimating] and
extend it into a scaling law [rocher2025scaling]. Taub et al. ground the statistical measurement
of disclosure risk on synthetic data (CAP, TCAP) on the premise that synthetic generation breaks
the link between identity and datum [taub2018differential].

*What distinguishes us.* These works re-identify from genuine auxiliary data. Our attack's input
is never a real datum of the target: it is a model output generated from a persona, compared
against real answers the attacker separately holds. We falsify precisely the CAP/TCAP premise, on
LLM-simulated survey microdata.

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
categorical answers, no free text, no agentic reasoning, and a mechanism localised in the
dependence structure rather than in memorised content (§5.5). Unlike Yeom and Feldman, our
pipeline trains no model on the target population.

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
near-monotone frontier of the same type without a coefficient [byun2025riskcontext]. Three differences
separate them from our claim: their quality is *aggregate* (MMD, Jensen-Shannon divergence,
downstream AUC), never a correspondence to the right person; their risk is *membership* in a
training set, not 1-in-N identification; and they publish no coefficient.

Three contradictors hold that fidelity and risk separate: Platzer and Reutterer
[platzer2021holdout]; Adams et al., for whom a generator without formal guarantees preserves
fidelity and utility without evident privacy harm [adams2025fidelity]; and Shafieinejad et al.,
observing decoupling as quality saturates within a single tabular diffusion model trained longer
[shafieinejad2026diffusion]. Our response is not that they are wrong: all three measure
*aggregate* fidelity, never individual correspondence to the right person, and none tests whether
the coupling they observe survives a null matched on per-person accuracy. Ours does not (§5.1).
Their decoupling also unfolds over training time within one model, where ours is a cross-sectional
correlation across twelve heterogeneous methods against 1-in-N re-identification.

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
`pid` equals `TWIN_ID`, and the twin files copy wave metadata line by line from the humans. The result therefore documents a generic risk for anyone
releasing "anonymous" twins without that key, a practice Twin-2K-500 does not follow. The
objection "this is not real re-identification, the attacker already holds the true answers" is
assumed, not rebutted; our answers are the explicit model above and the open-world measurement of
§5.3. A third, T2, would remove the assumption entirely — but we did not manage to test it.

### T2 — Two organisations publish twins of the same cohort; attacker holds nothing real

If several organisations each publish their own twins of the same panel with sufficient item
overlap, a third party cross-references them holding no human answer at all. This threat model is
named as an open problem by Jordon et al. [jordon2022synthetic] and covered by the A29WP
linkability definition, but never measured: Anonymeter's linkability presumes real
attribute values in hand [giomi2023unified], and Guépin et al. remove the real-auxiliary-data
assumption but target membership in a single generator's training set, never matching between two
independent generations [guepin2023synthetic].

**We tried to test it directly, and could not.** §5.4's 36.4 % twin-to-twin top-1 is a same-team,
same-persona-file measurement and does not speak to T2 as stated. Built as T2 actually describes,
two pipelines sharing nothing but the target person give top-1 1.8 % [0.4 ; 3.6] — but both fail
the interpretability control of §4.5, so the contrast opposes two noise sources. **T2 is neither
supported nor refuted: it was not tested** (§5.4).

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

**Park et al. archive** [park2024agents], 1,052 participants, 177 common items, replication
package publicly posted. Of its five agent conditions we analyse four — composite,
interview-only, survey-only, demographic — the `persona` condition being excluded by the
interpretability control (§4.5). Human retest ceiling 96.8 %.

**Argyle et al. archive** [argyle2023outofone], Harvard Dataverse, **CC0 1.0**: 4,270 ANES 2016
respondents, of whom **2,148** answer all **12** matched items; chance top-1 is 0.047 %. Each
twin column is a GPT-3 (`davinci`) prediction produced while holding that item out and supplying
the person's eleven other **true** answers, so these twins are *better* informed than our persona
twins, not worse: that confound runs against us. Three twin versions of the same people exist
(main decoding, temperature 0.01 and 1.0); they vary decoding, not epoch, and we never present
them as survey waves.

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
A third variant (A-MI)
scores higher still on the Park archive (93.25 %) but estimates its weights **in sample**, an
advantage declared in the preregistration, so we never report it as our result. An **adaptive**
attacker, used only against the defense (§6.1), additionally knows the mechanism and which items
it leaves untouched.

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

*Provenance.* On Twin-2K-500, the context contains 0 wave-4 columns and 0 wave-4 QIDs; maximum
normalised mutual information between context and item is 0.16 against 0.31 for the retest on
the same item. On cells where wave 4 differs from waves 1–3, the JSON 4.1 output equals wave 4
in 37.7 % of cases and waves 1–3 in 37.9 % — symmetric, so no indication of copying. On the Park archive, over 34,915 cells where the human
changed their mind, the composite follows wave 1 in 41.6 % and wave 2 in 43.2 %, and the
4.3–4.9 point wave-1 bias of the other three conditions holds for the `demographic` condition
too, so it is a shared calibration artifact, not item leakage. On the Argyle archive each twin column is generated with
its own item held out, so no tautology exists on either side; the same holds for B-demo and
B-oracle, whose target item is removed from their context.

*Empty-run validation.* Uniform ranks yield 0.00 bits; the B0 mode baseline yields
−0.004 [−0.003 ; 0.002] bits.

*Interpretability control, adopted after it cost us an experiment.* We state as a rule the control
whose absence invalidated two of our own arms (§5.4): **no experimental arm is interpretable until
its candidate pipeline has been shown to beat the demographic baseline in top-1 against the real
human answers**, on the pool and items actually attacked, with the baseline recomputed on those
same rows rather than carried over as a constant. The check consumes no model call and must
precede the first paid contrast; a pipeline that fails it yields twins whose contrasts oppose
noise to noise and return chance whatever is manipulated. It has since excluded our own pipeline
B, all three GPT-3 twins of the Argyle archive (§5.8), and the Park archive's `persona` condition,
whose agent — built on the person's own self-description — re-identifies her at 0.26 %
[0.06 ; 0.52] against a demographic baseline of 0.39 %. Baselines are always taken at the pool
size of the arm they judge, being strongly pool-dependent (§5.4).

---

## 5. Results

### 5.1 The coupling, and the null that absorbs it

Across 12 heterogeneous methods, the ordering by imitation quality and the ordering by
re-identification rate nearly coincide. Three rank correlations appear for that statement, and
they are three measurement plans, not three estimates of one number. **0.958** [0.930 ; 0.993],
fidelity taken as raw accuracy on whole items, robust to restriction to LLMs over a narrow
fidelity range (rho = 0.976) and to jackknife (0.958–0.986). **0.969** [0.937 ; 0.993], the
preregistered disjoint-item test over 50 stratified A/B splits of the 60 items, 100 % of them
above 0.7 — prediction (a) confirmed, the relation is not an artifact of recycled computation.
**0.965**, fidelity on Figure 2's axis (`fidelite_plancher`), the value the null below is
compared against. Both intervals resample **persons inside the 12 fixed methods**: they are
conditional on those methods and do not cover the sampling of methods, which is the dominant
source and the one "across 12 heterogeneous methods" appeals to.

Prediction (b) was refuted, and the witness that refutes it has since been rebuilt to remove a
real defect without changing the verdict: its *wrong* cells avoided the person's true answer
(`c7_disjoint.py` l. 133), inflating its leakage by a factor 1.3 (41.2 % against 31.6 % once
wrong values are drawn from the population marginal). Corrected, it still reproduces the coupling
— **rho 0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed** (Figure 2) — so
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

At comparable marginal accuracy, no non-LLM predictor we tested exceeds 0.3 % top-1 where the
twin reaches 20.7 % [19.0 ; 22.4] under the naive attack and **23.23 % [21.5 ; 25.0]** under the
strong one — **in a closed world, with the target always present in a pool of 2,058**. The
comparator figures are naive-attack rates, which makes the contrast conservative. JSON Persona
GPT4.1 attains that rate at accuracy 0.590; the comparators, at accuracy 0.457–0.511: PMM k=10,
0.23 % [0.06 ; 0.42]; B2 argmax, 0.07 % [0 ; 0.19]; k=1 donor on context alone, 0.13 %; LR on
context, 0.22 %. Two individualised *generators* — sampled LR and Gaussian copula — give 0.25 %
[0.11 ; 0.41] and 0.22 % [0.11 ; 0.36], answering the objection that we oppose an individualised
generator to predictors that regress to the mean.

We then gave a comparator an explicit advantage: a k=1 nearest-neighbour donor fitted **directly
on the target block's answers**, seeing what the LLM twin never sees. It reaches accuracy 0.584
against the twin's 0.590, carries genuine individual signal (0.584 true against 0.442 under
within-segment permutation), and despite that obtains a top-1 of **0.00 % [0 ; 0.18]**
(Clopper-Pearson, n = 2,058).

**This claim does not generalise to every leakage metric, and top-10 runs the other way.** That
same advantaged comparator reaches a top-10 of **53.2 % [51.0 ; 55.3]**, *above* the twin's
42.7 %: the direction of the whole contrast depends on the choice of k, which no principle fixes
at 1. We claim neither that all individualised prediction identifies nor strict accuracy equality
— the generators plateau at 0.476. Neither synthpop/CART nor CTGAN was tested.

### 5.3 Open world — the defensible measurement

Removing the closed-world assumption gives the number we consider hardest to attack in review. At
a false-accusation rate of 1 %, the strong attack (A-LLR, parameters estimated out-of-fold over
5 folds) recovers the right person **60.17 % [54.5 ; 64.4]** of the time on the Park archive and
**4.28 % [3.3 ; 5.6]** on Twin-2K-500, under a person-level bootstrap that **re-estimates** its
parameters in each resample, every copy of a person staying in one fold. At FPR = 0.1 % these fall to **44.37 % [23.3 ; 53.8]**
(Park) and **1.01 % [0.05 ; 2.82]** (Twin). Those two are not imprecise estimates: **the quantity
is not identified by the data at that FPR**, the threshold resting on roughly **one** absolute
false positive on Park and two on Twin, with hundreds of candidate thresholds within a false
positive of it giving widely different true detections. We draw no conclusion from them; the
FPR = 1 % pair is the measurement. Statistical comparators stay indistinguishable from noise at
both FPRs — under the naive attack, the only one they have been run under, so that comparison is
not on the twin's footing. The human ceiling at FPR = 1 % is 54.5 % [50.8 ; 57.5] and 90.7 %
[88.2 ; 93.3].

**These figures replace the ones we first published, and the correction runs in both directions.**
The naive attack gave 3.04 % [2.0 ; 4.0] and 20.39 % [15.7 ; 24.5] at 1 % FPR. On Park the
strengthening is statistically clear at that FPR — no overlap, the rate **triples**. **On
Twin-2K-500 the apparent gain does not survive its interval**: 3.04 → 4.28 % overlaps broadly, so
we do not present the strong attacker as identifying better than the naive one here.

**Our preregistered prediction was refuted, and one half of it then reversed by a better attack.**
We announced > 5 % (Twin) and > 30 % (Park); under the naive attack both fell below the bar. Under
the strong attack Twin (4.28 %) still falls below, while Park (60.17 %) passes the bar it had
failed.

> **Figure 1 — Open-world detection, naive and strong attack.** Two panels, one per dataset,
> false-accusation rate on a log scale against true-detection rate. Each overlays the naive
> Hamming attack as a full ROC curve with the strong A-LLR attack as **isolated diamonds** at two
> thresholds only (FPR = 0.1 % and 1 %): **no curve should be read into the diamonds.**
> Comparators sit near zero, the human retest ceiling above. *At a glance*: at a tenable
> false-accusation rate the risk is real and far above the comparators under both attacks, and the
> strong attack lifts the Park archive close to the human ceiling.
> Data: `resultats/c7-monde-ouvert-roc.csv`, `resultats/c7-attaquant-fort.csv`.

### 5.4 The twin-to-twin channel within one pipeline, what governs it, and why our T2 test does not count

Two twins of the same person designate each other when they share enough items, with no real data
on the attacker's side. The measurements below share one team and, for Twin-2K-500, one persona
source per person: they gauge the channel inside a pipeline, not T2 (§3).

**Twin-2K-500, tabulated by common-item count**. 30 pairs sharing 60 common items: mean top-1
**36.4 %**, individual pairs running from **11.9 %** to **83.6 %** — a mean over that spread is
not a typical pair's rate, and those 30 pairs come from 6 configurations, so the independent unit
is again the configuration. 12 pairs sharing 19 common items: mean top-1 **0.45 %** (chance
0.05–0.10 %). Demographics Only against the rich twins gives 7.76 %. The anti-artifact control, a
decoy from the same segment, gives 0.04 % on the 60-item pairs and 0.10 % on the 19-item pairs.

**Park archive replication**: 1,052 agents, 177 common items. Interview→survey top-1 **11.9 %
[10.1 ; 13.8]**; survey→interview **13.0 % [11.2 ; 14.9]**; top-10 45–46 %. Demographic bound
1.5–2.5 %, decoy control **at most 0.31 %**. **Preregistered prediction refuted**: we set a
threshold of at least 20 % top-1 there and 11.9–13.0 % does not reach it, though the preregistered
*failure* criterion is not met either, at 5–8× the demographic bound.

**We never report a single figure for this channel without its common-item count**; a previously
circulated average of 26.11 % pooled the two item regimes and is withdrawn. Nor do we claim
leakage crosses waves: that arm is infeasible, with 0 items in common.

**The channel is not an artifact of a shared prompt template or of demographics.** Decomposing
agreement between two twins of one person over the 60 common items: the floor between *strangers*
is **46.0 %**, the demographic-ideological segment adds **3.8 points**, the person adds **17.4**
— 82 % of the rise above the floor. A pure-population witness identifies the right person
**0.07 %** of the time against **36.4 %** for the real attack.

**The cross-dataset anomaly, explained in part.** Park shares three times Twin's items and leaks
roughly three times *less*. Item count is the wrong denominator: the 177 GSS items are strongly
redundant, giving **≈ 9.0 effectively independent items against ≈ 10.1** on Twin, a real ratio of
**0.89, not 2.95**. Pool size runs the wrong way too: shrinking Twin's pool to 1,052 *raises* its
top-1 (37.3 → 44.1 %). **A residue of roughly 3× remains unexplained**, the remaining candidates
— persona format and length, and the generating pipelines — not testable on what we hold. The
same denominator places the third dataset far below both, at **4.31** effective items for 12 raw
ones (§5.8).

*Limits.* The 12 low pairs are exactly those at 19 common items, so the effect follows the
shared-item count rather than an aberrant configuration. On Park the item-rate relation does not
follow Twin's.

**T2 itself: two genuinely independent pipelines, and a test that does not count.** Two pipelines
sharing nothing but the target person — `deepseek-v4-flash` JSON dossiers against `qwen-2.5-72b`
narrative biographies — were matched on the same 60 items (n = 142 of 200 planned, stopped by a
transport error). Preregistered rule: T2 survives if the top-1 CI excludes the segment control
*and* stays at least 2× the demographic baseline. Result: top-1 1.8 % [0.4 ; 3.6] against a
demographic baseline of 9.2 %. **We no longer read this as a refutation.** Neither arm produces
twins that identify the real person better than chance (0.0 % and 0.8 % top-1 against 0.83 %
expected on a pool of 120, where the Twin team's own twins reach 20.2–38.9 % on that pool), so
the comparison opposes two noise sources and would have returned chance whether or not a
cross-organisation channel exists: it measures our instrument, not the world. The 36.4 % above,
a same-pipeline measurement, is not evidence for T2 either, so T2 stands open in both directions.

**Which element differs, not how many — and a preregistered law our own measurements refute.**
Among the six Twin-2K-500 configurations that pass the interpretability control (2,058 people, 60
common items, symmetric attack), changing a single published pipeline descriptor gives **81.4 %**
[80.0 ; 82.8] for decoding alone, **67.1 %** [65.3 ; 68.7] for the prompt template, **33.5 %**
[31.6 ; 35.3] for reasoning and **17.2 %** [15.8 ; 18.6] for the model. We preregistered a
*distance law* — leakage falling with the number of published descriptors that differ — and our
own measurements refute it: Spearman **−0.232** [−0.321 ; −0.187] over 15 pairs, **+0.003**
[−0.047 ; +0.068] once the two twins' individual fidelity is controlled, against the −0.7
predicted. At a distance of one, rates span 17 % to 81 %: the spread *within* a level dwarfs the
spread *between* levels. Counting changed components predicts nothing useful; naming them does.
On Park the same control leaves three pairs, so no replication is possible. Two limits: the
distance weights are arbitrary, and refitting them on the linkage rate would make the measure
circular; and the independent unit is the configuration — 18 pairs, 9 configurations, two teams.

**One-factor-at-a-time from our own pipeline: arithmetically sound, not interpretable.** Varying
model, template and persona format one at a time from pipeline B gives 0.67 %, 0.83 % and 2.65 %
(n = 120, chance 0.83 %). B and all three derived conditions identify the real person at chance,
so each contrast opposes two noise sources: we withdraw the reading we first gave these numbers —
that changing any single component collapses the channel — and with it the refutation of the
matching preregistered prediction. We also correct a comparison of our own: these rates were set
against 13.29 %, a *twin-to-human* baseline, where the twin-to-twin one is 23.69–34.42 %.

### 5.5 Mechanism: being right while deviating — and three refuted hypotheses

What identifies is neither the frequency of departures from the modal answer nor answer
diversity, but their **correctness** — and the whole response vector is required. Correctness of
deviations: 68.5 % for the human retest (leakage 81.6 %), 50.3 % for JSON 4.1 (20.6 %), 43.3 %
for Demographics Only (2.14 %), 39.1 % for PMM (0.22 %) — PMM deviating and diversifying as much
as the twin without leaking.

The ablation is the strongest evidence: permuting the order of each twin's 40 purchase answers
drops closed-world top-1 from **33.1 % [31.2 ; 35.2] to 0.046 % [0 ; 0.11]**, below chance, and
an oracle given only the count of "yes" answers gives 0.29 %. What identifies is the dependence
structure between answers, not any answer in isolation. That ablation starts above this paper's
headline 20.7 % because it attacks the **40 purchase items alone** where the headline uses all
**60**: the 20 opinion items identify 46× less and dilute a naive Hamming rule rather than help
it. That is a change of attack surface, not a discrepancy.

**Three preregistered hypotheses refuted.** H1 (entropy): opinion items carry 2.10 bits against
0.99 for purchase items and identify 46× less — top-1 0.24 % [0.07 ; 0.46] against 11.0 %
[9.9 ; 12.3] for the purchase subset matched to them on entropy, a 20-item comparison. H4
(stereotypy): 36.2 % [35.6 ; 36.8] against 37.5 % [36.9 ; 38.1] in humans. And "deviations alone
carry ≥ 80 % of the leakage": 0.68 % in the mixed condition. We do not present "wrong deviations
alone = 0.0 %" as a result: it is a floor of the method.

*Limits.* The mechanism is established on Twin's purchase block alone and is in apparent tension
with the Park archive, where opinion items identify most: at 20 items Park gives 11.7 % against
0.24 % for Twin's 20 opinion items, **at lower per-item entropy** (1.30 against 2.10). What
remains is the block effect, the **best-supported hypothesis, not a result**.

### 5.6 Bits of identity: the instrument transports, the rate does not

An LLM twin costs about 0.4 bits of identity per point of accuracy gained, against 0.068 for the
best useful statistical comparator. Twin JSON 4.1: **3.55 bits [3.39 ; 3.72]** of a log2 N = 11.01
ceiling. Park composite: **7.47 [7.27 ; 7.66]** of 10.04. PMM: 0.19 [0.16 ; 0.23]. B2: 0.08.

Transportability is the point. Bits normalised by human entropy give 0.0439 (Twin) against
0.0327 (Park) — a factor of **1.34** — where top-1 varies by a factor of **3.2**. Demographics
Only and PMM leak with **no accuracy gain at all** (−0.5 and −2.4 points), a case a ratio alone
would mask. The instrument's validity is bounded on the other side by the third dataset, where a
twin carrying no demonstrable individual information has no ratio worth transporting (§5.8).

**A nuance against our own hypothesis.** The human retest has a ratio of 0.37 (Twin) and 0.44
(Park), as good as or better than the twins: the excess cost exists relative to statistical
predictors, **not relative to a human answering twice**.

*Limits.* The bits are a **lower bound** (dyadic bound plus Miller-Madow). The sum of per-item
mutual information is unusable as a total: 58.7 bits against a ceiling of 10.04 on the Park
archive, as preregistered.

### 5.7 The risk depends on the recipe — and we could not reproduce it

Our own twins, produced in a single call to cheap models from a raw profile, identify almost
nobody: 0.00 % to **0.83 % [0 ; 2.15]** (deepseek-v4/R1) across 7 cells, against 2.13 % for the
other team's Demographics Only. That interval **contains** 2.13 %, so no precise factor is
established — only the order of magnitude, that no model reaches 1 %. Any previously circulated
"25× below" figure is withdrawn. Memorization is not the explanation: llama31-8b, with a training
cutoff preceding publication, copies nothing verbatim and leaks no more than the models that do
copy — a control on our own twins, in a regime where none identifies almost anyone, which we do
not extend to the published twins of §5.2–§5.4 (§1.3).

**Two further preregistered predictions refuted.** (i) R1 ≥ 10 % on at least 2 of 3 models — no
model reaches 1 %. (ii) Call granularity would explain the leakage — not confirmed and
underpowered (n = 10 on the per-item arm): single call 0.00 % [0 ; 8.8] and per-item call 0.00 %
[0 ; 30.85], top-10 running **opposite** to the prediction (7.5 % against 0 %). We claim neither
that leakage comes from the call format nor that the cause is identified. **It is not.**

**We then paid to test the obvious explanation, and it failed.** `openai/gpt-4.1` (Twin's own
model class) on Twin's per-item recipe without modification, 30 persons × 60 items = 1,800 calls,
100 % parse rate: accuracy **0.4722 [0.4361 ; 0.5050]** against Twin's 0.574; fidelity **0.1714**
against their 0.708; top-1 and top-10 **0.00 % [0 ; 11.57]** (Clopper-Pearson, n = 30). **One
further preregistered prediction refuted**: accuracy > 0.55; top-1 > 5 % is **not refuted**, its
interval containing the threshold — inconclusive for lack of power. Fidelity > 0.10 held at
0.1714, barely above our best cheap twin (0.177). We did not make the leakage come back because
we did not reach Twin's fidelity, and it is that gap, not the underpowered top-1, that carries
the conclusion: at the fidelity reached, the regression over the 12 points of `c7-compromis.csv`
(slope 0.1834, r = 0.785) predicts **1.10 %** [−9.15 ; 11.35], and the observed 0.00 % falls
inside it — from a new model *and* a new recipe, the point follows the curve.

**The unknown narrows instead of disappearing.** Neither the model nor the call granularity, what
remains implicated is the **format and length of the profile**: Twin's full JSON persona runs to
roughly 121,000 characters against our 8,000-character truncation.

*Limits.* n = 40 persons for the recipe arm, truncated to n = 10 on the per-item arm, and n = 30
on the paid frontier-model arm; a floor effect is not excluded. Transport failures and retries:
Open Science.

### 5.8 A second dataset, and a third at the other end of the trajectory

On the Park archive, the composite agent designates the right participant among 1,052 **in a
closed world** in **90.40 % [88.6 ; 92.2]** of cases under the strong attack, top-10 97.8 %,
against a human retest ceiling of 96.8 %. **This replaces the 65.51 % [62.7 ; 68.3] we first
published**: a naive agreement attack understated this archive's leakage by 38 % in relative
terms. An in-sample information-weighted variant reaches 93.25 %, which we do not claim (§4.3).

The remaining conditions are **naive-attack measurements**, the strong attack not having been
re-run on them: interview-only **44.7 % [41.8 ; 47.5]**, survey-only 20.6 % [18.2 ; 23.0],
demographic 2.26 %. The interview-only figure carries zero documentary exposure to the survey, so
it is the cleanest demonstration that an agent built from a conversation alone identifies its
person — and given what the strong attack did to the composite, **it is a lower bound**.

We do not compare the Park and Twin rates as measurements of the same thing: item count (177
against 60), per-item entropy (1.30 against 0.99) and human ceilings (96.8 against 81.6) all
differ. Equalised at k = 60, Park gives 34.0 % [23.5 ; 51.5] against Twin's 20.7 %, on 20 draws
of a naive attack.

**The third dataset, and the analysis that stops before it starts.** On the Argyle archive the
interpretability control **fails for all three GPT-3 twins**, and the preregistered decision rule
halts the analysis there: top-1 0.14 % [0.05 ; 0.27], 0.11 % [0.04 ; 0.20] and 0.09 %
[0.02 ; 0.22] against a demographic baseline of **0.10 %** [0.02 ; 0.23] recomputed on that same
pool of 2,148, all intervals overlapping. No contrast is interpreted, and the anchor-pool draws
were never computed: they would have interpreted noise. The verdict rests on no choice of items —
dropping age gives 0.08–0.13 %, the eight attitude items alone 0.09–0.11 %. The reason is visible
per item: mean exact accuracy **47.2 %**, below the demographic imputer's 51.5 % and below the
modal answer on nine items of twelve. In bits, the best of the three carries **0.094**
[0.074 ; 0.118] of an 11.07 ceiling — the level of Twin's *weakest* statistical comparator — while
a nearest neighbour given exactly the same eleven true answers carries 0.342 [0.301 ; 0.389],
**3.6 times more**.

Nor does it rest on a weak attacker. Re-running the A-LLR attack that carries this paper's
headline figures takes the best of the three to **0.23 %** and its baseline to **0.09 %** — still
overlapping, still failing the control, the whole gain four people out of 2,148. In the
open-world metric of the trajectory's other end that twin detects **one** person at 1 % false
accusations and none at ten times that severity, at an AUC indistinguishable from zero: the
metric has no shape here, which is why the left end is read closed-world. Both witnesses are
post-hoc.

**Two preregistered predictions were missed, and we count them as neither.** We had announced
top-1 2.5 % [1.0 ; 6.0] and normalised bits [0.020 ; 0.070] from our measured item and pool
curves; the observations, 0.14 % and 0.0044, fall far outside both. Neither our scaling law nor
the transportability claim is refuted by this, because neither is testable here: both presuppose
a twin that carries individual information. **We cannot distinguish "our law overstates leakage
at a low effective item count" from "this twin is at the noise level", and we do not pretend
to.** Both rows sit outside Table 1's count, like the distance law of §5.4 — three verdicts
reached after the census of §7.1 was closed.

### 5.9 Scale

From N = 50 to N = 2,058, the twin/demographic ratio grows from 2.8 to 9.7: top-1 falls from
53.2 % [50.0 ; 56.3] to 20.7 %, and the share of the human ceiling from 57.0 % to
25.4 % — naive-attack rates, the scale study not having been re-run
under the strong attack. The intervals here are **not** the person-level bootstrap of §4.3: they
span the sub-pool draws, and at N = 2,058 no sub-pool is left to draw, so that row carries none. **We extrapolate no value beyond N ≈ 4,000**: a power law and a
logarithmic law fitted on the same 6 points already diverge at twice the range (18.1 % against
13.9 %).

> **Figure 2 — Imitation quality against leakage, with its control
> (`article/figures/fig2-couplage.png`).**
> Abscissa: individual fidelity (`fidelite_plancher`, share of the human floor). Ordinate:
> closed-world top-1 leakage. Thirteen points — LLM twins, statistical reference points,
> Demographics Only, and the human retest at fidelity ≈ 1 / leakage 81.6 % — all with **error
> bars on both axes** from a per-person bootstrap of 2,000 resamples. **Inset**: the 5th–95th
> percentile envelope of the corrected marginal null (mean rho 0.974) as a grey band, with the
> observed rho (0.965) inside it. *At a glance*: the points rise together with no plateau at the
> top, **but the observed correlation sits inside the band that a null matched only on accuracy
> already produces** — the coupling is measured, not shown to be individual-specific.
> Data: `resultats/c7-compromis.csv`, `resultats/c7-compromis-robustesse-points.csv`,
> `resultats/c7-nul-corrige-marginal.csv`.

---

## 6. Defense

Shuffling the purchase answers between people of the same demographic segment (D4) brings
closed-world top-1 from **20.7 % [19.0 ; 22.4]** to **0.13 %** against the naive, non-adaptive
attack, and to **0.29 % [0.10 ; 0.53]** against the best attacker we measured
(§6.1) — the figure we report as the defense's rate. Per-item distribution and between-segment
differences are preserved **exactly, by construction**, as PRAM predicts, and that exactness is
also the mechanism's central limitation: shuffling item by item within a segment leaves the
within-segment multiset of each item identical (1,560 of 1,560 segment × item pairs), so D4
republishes each item's within-segment histogram without noise, and an adversary who knows a
segment's other members recovers the target's 40 answers by difference. **D4 offers no formal
privacy guarantee.**

**The cost is not a single average.** By component: **0.0 points on the per-item distribution and
0.0 on group differences — which is that republication, not a cost avoided** — and **4.4 points on
inter-item correlations** (4.373 ± 0.058 over ten seeds; the amplitude to be destroyed is 4.317,
so this component is destroyed in full). We therefore withdraw the summary that presented D4's
cost *as* a single mean of 1.47 points: two of the three components are zero by construction, so
that mean divides by three an effect falling entirely on the third. And that cost is worse than
the summary suggested: against the real human answers `erreur_correlations_hum` rises from **5.775
to 9.709**, a degradation of **68.1 %** — the defended twin moves *away* from the humans on
correlations, so no framing in which the cost is absorbed by an error already present is correct.

Alternatives: D1 (k=10 aggregation) gives 0.55 % for 3.8 points across all three components; D2
(noise) never descends below 1 %.

### 6.1 The defense against a strong, then an adaptive attacker

The figure above was measured against the naive attack, which §5.8 shows can badly understate
leakage. We re-ran it against the strong attack recalibrated on the *defended* outputs, then
against an attacker who knows the mechanism and which items it leaves untouched. D4 holds: top-1
goes from 0.13 % (naive) to **0.24 %** under the recalibrated strong attack, and the **adaptive**
attacker plateaus at **0.29 %** (strategy S1, leaving the 20 opinion items intact;
segment-invariant strategy S3 alone 0.05 %) — two orders of magnitude below the 20.7 %
undefended rate, and never above 1 %. **Attribute disclosure is not demonstrated either**: the
best strategy names the correct `S_gra` segment in **7.7 %** of cases, against 6.8 % at chance and
**12.6 %** for always answering the most frequent segment — the attack does worse than not
attacking.

**A reservation that bounds the guarantee.** This residue comes *entirely* from the 20 opinion
items D4 does not permute: the guarantee holds for this split, not for a design leaving a more
informative block untouched. On those 20 items alone the defended and the **undefended** twin are
indistinguishable — 0.245 % [0.073 ; 0.471] against 0.260 %, on intervals that almost
coincide — so the residue is not a residue of the defense but the part of the publication it never
touches. None of these rates is a bound on the defense; they are the rates of the attacks we
built.

### 6.2 Differential privacy: a comparison we withdraw

We preregistered that at a moderate budget differential privacy would be dominated by D4, and
reported that prediction as refuted. **We withdraw the comparison and its verdict: we did not
compare the cost of differential privacy to D4's.** Our generator was fitted on the humans and
scored against the twin, so part of its error is a mismatch of reference, not a price of privacy;
at **eps = ∞, with no privacy at all**, it already costs as much as at eps = 3 or eps = 10, so
what we measured is the cost of an independent-per-item architecture to which the budget
contributes almost nothing; on correlations D4 and the DP generator alike sit at or above the
amplitude there is to destroy (§6), the score of any mechanism that destroys all of it; and the
top-1 rates we set against each other are 0 to 3 people out of 2,058. **We claim no
superiority of D4 over differential privacy** — only a different trade-off, carrying no guarantee,
against the particular attack we built. The corrected measurement is not reported here; the audit
establishing the faults is cited in Table 1, and the implementation's limits in Open Science.

**What survives is architectural, and a theoretical point.** The floor is not budgetary: the
non-private control pays the same price, so a per-item independent synthesiser cannot carry this
questionnaire's joint structure at any epsilon. And DP protects an individual's *membership*
behind a published statistic, whereas our attack assumes the person is already known — her profile
being the twin's input — and asks whether **the output conditioned on her** can be linked back:
record linkage, not membership. The DP generator escapes it only by **never conditioning on an
individual** (individual fidelity stays at most 0.2 points at every budget, including infinite),
that is, by refusing the twin's task. A panel holder who needs population statistics should use
DP; one who needs a per-person twin cannot get one here at any epsilon.

### 6.3 What the defense costs a downstream analyst

A defense is usable only if the analyses people actually run survive it. We measured three on the
same 2,058 persons. **Preserved exactly**: group comparisons are **identical to 16 decimal
places** between raw and defended twin, and demographic regression coefficients keep their sign
and significance. **Destroyed**: purchase-item coefficients significant in the raw twin become
non-significant after D4, and on a PCA of the 40 purchase items **45 % of the first component's
loadings are inverted** relative to humans, against **0 %** for the raw twin.

**The honest comparison.** The unprotected twin was already wrong — it inverts the sign of the
male-female gap (+0.010 against −0.047 in humans) and loses 5.3 points of PC1+PC2 variance — and
D4 adds **3.5 points**, less than the error already present; but the axis inversion is **D4's own
doing**, changing *which* items compose the structure more than its strength. With a D4-defended
twin, group analyses and predominantly demographic regressions remain reliable; anything resting
on the link between two answers of the same person becomes unusable.

*Limits.* Tested on a single block, of a single twin, of a single dataset.

---

## 7. Discussion and Limitations

### 7.1 The thirteen refuted preregistered predictions, one withdrawn, two inconclusive, and one untestable

| # | Prediction (preregistered) | Outcome | Source |
|---|---|---|---|
| 1 | The quality-leakage coupling exceeds a null matched on accuracy alone | **Refuted.** Null rho 0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed over the 12 configurations; original null carried a defect, since corrected, verdict unchanged (§5.1) | `audit-renversement-2026-09-12.md` |
| 2 | Open-world > 5 % (Twin) and > 30 % (Park) at FPR = 1 % | **Refuted as first measured** (3.04 % and 20.39 %). Under the strong attack Twin still fails at 4.28 %, Park **passes** at 60.17 %: one half refuted, the other confirmed, counted here as a single row | `c7-attaquant-fort-resultats.md` |
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
| 13 | P3: an adaptive attacker knowing the mechanism breaks the defense | **Refuted, in the defense's favour.** Plateaus at 0.29 %, never above 1 % | `c7-attaquant-fort-resultats.md` |
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Withdrawn, not decided.** The comparison behind this verdict is retracted: the DP generator was fitted on the humans and scored against the twin, and at eps = ∞ — no privacy — the cost was already the same. No verdict (§6.2) | `audit-comparaison-dp-2026-09-13.md` |
| 15 | A frontier model on Twin's per-item recipe reaches accuracy > 0.55 | **Refuted.** 0.4722 [0.4361 ; 0.5050] | `c7-fort-resultats.md` |
| 16 | That same twin reaches top-1 > 5 % | **Inconclusive.** 0.00 % [0 ; 11.57] (Clopper-Pearson, n = 30), the 5 % threshold lying inside the interval | `c7-fort-resultats.md` |
| 17 | T2, independent pipelines: top-1 CI excludes the segment control and stays ≥ 2× the demographic baseline | **Not testable with this instrument — counted as neither.** 1.8 % [0.4 ; 3.6] at n = 142/200, but both arms' twins identify the real person at chance, so the contrast decides nothing either way (§5.4) | `c7-deux-organisations-resultats.md` |

Four rows left the refutation count after they were first written: rows 9 and 16, once a
percentile bootstrap on a zero-event sample was recognised as unable to return anything but
"[0 ; 0]"; row 17, whose arithmetic is exact but whose pipeline carries no individual information
(§5.4); and row 14, when the comparison behind its verdict was retracted (§6.2). **Seventeen rows,
thirteen refutations, one withdrawn, two inconclusive, one untestable.** Three further outcomes
were partial and count as neither (§6.3, §5.7); one held outright, P2 (§6.1); three verdicts
reached after this table closed are reported in place, not counted in it (§5.4, §5.8).

### 7.2 What we do not know

**An excess cost in bits per unit of fidelity, real but unexplained.** On equal samples,
CV(bits/fidelity) = 0.436 against CV(bits/accuracy point) = 0.357 over the same 9 points. With so
few points and no identified mechanism, the excess **must not be attributed to "LLMs" as a
family**.

**We did not reproduce the leakage with our own twins** (§5.7), including with a paid frontier
model on Twin's own per-item recipe — an open limit, never a mechanism, and a narrower one than
before: neither the model nor the call granularity, leaving the persona's format and length.

**Whether the twin-to-twin channel crosses independent pipelines.** Everything we report on that
channel is measured inside a shared pipeline. The arm built to decide the cross-pipeline case
returns 1.8 % [0.4 ; 3.6] but fails the control of §4.5, so it decides nothing either way (§5.4,
row 17): **T2 is untested, not refuted**, and the channel is a within-pipeline result.

**Rates do not predict across datasets.** The normal-maxima model lands close on Park k = 60
(0.354 predicted, 0.340 observed) but fails both its controls (0.053 for 0.206 observed; 0.983
for 0.656): an isolated success between two failures is a coincidence, not a law. Only conditional information retains sign and order of magnitude
across datasets (r = 0.72 and 0.89). The twin-to-twin channel's cross-dataset rate is likewise
only partly explained, a residue of roughly 3× surviving both controls (§5.4). And nothing we
hold separates the trajectory of §5.8 from the protocols that differ along it (§1.1).

### 7.3 Multiplicity

Most of this paper's central results are bootstrap confidence intervals around a descriptive
measure — re-identification rate, rank correlation, bits of identity — not classical hypothesis
tests; of the 34 preregistered predictions underpinning those claims at the time of the census,
11 were refuted and 3 judged inconclusive, roughly one third, the opposite of the signature of
data dredging. **That rate controls the auxiliary family, not the headline**: the preregistered
predictions concern mechanism, defense, recipe and distance law, while none of 20.7 %, 90.40 %
and 60.17 % is a preregistered threshold — each is descriptive, chosen among competing metrics
(top-1 or top-10, naive or strong, closed or open world, the choice of k). Of the 3 tests carrying a classical p-value, a Holm correction leaves the two
smallest standing (0.002 and 0.008, adjusted to 0.006 and 0.016) and confirms the
non-significance of the third; the intervals carrying the other claims must be read as
measurements, each with its own margin, not as independent rejections of a common null.

The full census covers 47 adjudicated tests across three families — the article's claims, the
standalone controls, the abandoned branches — with 25 confirmed and 15 refuted. It was written
over the 15 `c7-*` sub-studies existing at the time and excludes the verdicts added since, which
is why Table 1 and the census do not carry the same totals.

A second pass extended the confirmatory family to 15 tests convertible to a p-value and applied
both Holm and Benjamini-Hochberg. **Neither changes any verdict**, and the two agree on all 15:
the p-values are bimodal — eight at or below 0.0025, seven already near 1 — so no claim here rests
on a marginally significant result. It also flags three
thresholds as fragile, which we name rather than let a reviewer find: the frontier twin's
**fidelity > 0.10** bar, confirmed at 0.1714 but refuted had it been set at 0.18 — while our own
weakest known twin sits at 0.177; the choice of k in top-k (§5.2); and the functional form of the
scale law beyond the measured range (§5.9). A common bootstrap across analyses reusing the same
2,058 people was abandoned for cost, so the intervals of §5.1–§5.3 on Twin carry no simultaneous
coverage.

### 7.4 Scope, and two limits established by failure

Three datasets, one language, one questionnaire format, categorical closed-choice answers only.
The mechanism analysis and the defense both rest on a single block of a single dataset. We make no
claim about conversational agents or panels outside the three studied here. Two further limits we
state with the resource that would lift them, because we looked for it and did not find it.

**Generality beyond American attitude instruments, and the audit bottleneck.** All three datasets
are American survey panels built on neighbouring instrument families, so we cannot say whether
this channel is a property of that family — nor, as §1.1 states, separate the trajectory from the
protocols that differ along it. The obstacle is not that the method is rare, but that the matched
file — row-by-row, not by demographic cell — is almost never redistributed. We verified three such
datasets at the source; we ran no systematic census, so no upper bound is established. **Not a
count, a typology**: two teams withhold their file (editorial choice or silence); a third is
barred by its source licence (SOEP); and one inverse case exists, synthetic outputs with no
matched humans. **On that typology of four cases, and on no census, the risk appears to be created
faster than it becomes auditable** — a reading of four cases, not a rate. The resource that would
lift our limit is a matched individual dataset from a domain distinct from GSS and Big Five for
which twins produced by a **third-party team** already exist for the same respondents, under a
licence permitting local computation and publication of an
aggregate rate; and, for the trajectory of §5.8, several model generations over the same items and
the same population.

**Free-text outputs.** We measure nothing about free text, because no dataset here permits it:
the Park archive publishes **no transcripts**, **none of the 13 Twin configurations** produces
text, and the Argyle twins are single recoded tokens. Every rate in this paper therefore concerns
closed-choice categorical answers, and we extrapolate them to free-text outputs in neither
direction — the free-text inference literature [staab2024beyond, ko2026weakcues] attacks a richer
signal than ours, so our figures are not an upper bound there. The missing resource is Park's
complete transcripts, or a run of the Twin pipeline that generates text.

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
quantification, and our own first measurement understated it.

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
cost stated: 4.4 points on inter-item correlations, a 68.1 % worsening of the gap to human
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
in the Source column of Table 1, in the `Data:` line of each figure caption, and at the few points
in §5.1 and §5.7 where a specific script line is at issue; elsewhere they are omitted to keep the
manuscript readable.

**Bibliographic verification.** Of our 47 references, 20 carry an auditable source-verification
trace in the artifact; the remaining 27 were verified in an earlier pass whose record did not
survive. We state this as a limit rather than claim a fully audited bibliography. Full accounting
in `article/references-verification.md`.

**Transport failures and retries (§5.7).** Roughly 1,490 calls first failed with HTTP 402 from
in-flight credit reservation, not lack of balance, and were retried at decreasing concurrency
without double billing.

**Differential-privacy implementation (§6.2).** The synthesiser was written by hand rather than
with a reference library, and is not full PrivBayes: per-item marginals perturbed by Laplace noise
(L1 sensitivity 2, budget split over 60 items, basic sequential composition) then sampled i.i.d.
per item, that is degree-0 PrivBayes with no joint structure. It was fitted on the human answers
and scored against the twin. Epsilon covers only the published histograms, with no composition
across the repository's other analyses, and correlations, between-segment differences and the
`S_gra` covariate are not protected. These are reasons the comparison of §6.2 is withdrawn rather than
corrected here; the corrected design — refitting on the twin, a composed Gaussian mechanism under
zCDP, and at least ten seeds with intervals — is specified in
`resultats/audit-comparaison-dp-2026-09-13.md` §9 and has not been run.

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

