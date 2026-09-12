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
archive (1,052 participants) the same attack reaches **90.40 %** [88.6 ; 92.2] against 65.51 % for
a naive agreement attack — our first attack understated that leakage badly. The
rate is not an artifact of the closed pool: in an open world, at a false-accusation rate of 1 %,
the attacker is right 4.28 % [3.3 ; 5.6] of the time on Twin-2K-500 and 60.17 % [54.5 ; 64.4] on
the Park archive (against 3.04 % [2.0 ; 4.0] and 20.39 % [15.7 ; 24.5] for the naive attack — a
gain that is statistically clear on Park and does not survive its interval on Twin), with the
statistical baselines at roughly 0 % and a human test-retest ceiling of 54.5 % / 90.7 %.
We report a twin-to-twin channel:
within one pipeline, two twins of the same person built from the same persona source designate
each other with no real human answer held by the attacker — 36.4 % top-1 at 60 common items on
Twin-2K-500 and 11.9–13.0 % at 177 common items on the Park archive, against anti-artifact controls
of 0.06 % and at most 0.31 %. Across genuinely independent pipelines we could not test that
threat model at all: the twins our own pipeline builds designate the right human only at chance
(0.0–0.8 % top-1 against 0.83 % expected), so that arm contrasts two noise sources and bounds our
instrument rather than the world. We do not claim
an absence of prior work: in a regime it does not evaluate, we contradict Anonymeter's conclusion
that linkability is the weakest of the three risks it measures — it links two attribute partitions
of one real dataset with the attacker holding real values, where our attacker holds none.
We also report what we could not establish. We predicted, and preregistered, that the observed
coupling between imitation quality and leakage reflects an individual fingerprint; a null carrying
only a matched per-person accuracy margin — an object that is not structure-free, and that in fact
leaks more than our own twin (31.6 % top-1 against 20.7 %) — reaches a rank correlation at least
as high as ours (0.974 [0.950 ; 0.993] against 0.965 observed). Fourteen preregistered predictions were refuted, two
are inconclusive for lack of power, and one could not be tested; our own twins failed to reproduce the leakage even with a paid frontier model on the
per-item recipe; and the twin-to-twin channel's cross-dataset behaviour is explained only in part,
by item redundancy rather than item count. Following Das, Zhang and Tramèr, we built the control
this literature was missing, and it absorbs our own effect. Finally, a 1998 mechanism (PRAM)
applied to twins reduces closed-world top-1 from 20.7 % to 0.13 % at a measured cost of 4.4
points on inter-item correlations, and holds at 0.29 % against an adaptive attacker who knows
the mechanism — while differential privacy, contrary to our own preregistered prediction, is
not dominated by it on aggregate utility.

---

## 1. Introduction

Survey research is beginning to publish *digital twins*: for each human respondent in a panel,
an LLM is conditioned on that person's profile and its simulated answers to the questionnaire
are released as a per-person record. Toubia et al. published 2,058 such twins as Twin-2K-500
[toubia2025twin2k500]. Park et al. built generative agents for 1,052 participants and cited privacy
in restricting access to individual agent responses [park2024agents] — although the
replication package that is publicly posted does carry the 1,052 participants' individual
responses together with those of the agent conditions we analyse (§4.1, §8).
The privacy question these releases raise has been named — by Park et al. themselves, by
Bonagiri et al.'s normative call [bonagiri2026cognitive], and by the AAPOR task force
[aapor2026responsibleai], which ranks synthetic response generation as the most risky of the
core tasks it evaluates and names re-identification by linkage without ever quantifying it —
but it has not been measured.

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
artificial predictors matched to each person's own accuracy margin, with correct positions
drawn at random without looking at the person — an object that is not structure-free, and
that in fact leaks more than our own twin (31.6 % top-1 against 20.7 %). Adversarial review
later found a real defect in that first witness, which has since been rebuilt without changing
the verdict (§5.1). The rebuilt witness reaches mean Spearman **0.974**, 5th–95th percentiles
**[0.950 ; 0.993]**, against **0.965** observed over the 12 configurations
[audit-renversement-2026-09-12.md]; the observed value does not exceed it. The 0.969 just
quoted is that same observed quantity measured on the 50 disjoint A/B splits rather than on
whole items; each null is compared only against the observed value measured on its own plan.
**Reproducing the coupling requires nothing more than a matched per-person
accuracy and correct positions drawn at random — prediction (b) is refuted.**

We report this as a result rather than a confession. A recent line of work argues that an attack
on foundation models proves nothing until the null hypothesis is properly sampled: blind baselines
routinely beat state-of-the-art membership inference attacks [das2024blind, duan2024membership],
and a SaTML position paper makes the demand explicit [zhang2024satml]. The quality-leakage
coupling reported in prose by Ward et al. [ward2025synthmia] and Byun et al. [byun2025riskcontext], and
contested by Platzer and Reutterer [platzer2021holdout] and Adams et al. [adams2025fidelity], has
never been tested against such a control. We built the control that was missing, and it absorbs
our own effect.

What survives this is not a theory of why twins leak. It is a set of five measurements that do
not depend on the coupling being individual-specific at all.

### 1.2 Contributions

We order these from the least expected to the most.

**(1) A twin-to-twin linkage channel within a shared pipeline — and a cross-pipeline test our own
instrument turned out to be unable to carry.**
Two twins of the same person, sharing their persona source and differing only in model or output
format, designate each other when they share enough items — while the attacker holds no real
human answer of any kind. On Twin-2K-500: 36.4 % mean top-1 over 30 pairs sharing 60 common
items, against an anti-artifact control (decoy from the same demographic segment) of 0.04 % on
those pairs. On the Park archive: 11.9 % [10.1 ; 13.8] interview→survey and 13.0 % [11.2 ; 14.9]
survey→interview at 177 common items, against a control of at most 0.31 %. We never report a
single number for this channel without its common-item count (§5.4). Anonymeter's contrary
conclusion [giomi2023unified] is reached under a different definition — two records of the
*same* real dataset, the attacker holding *real* attribute values — in a regime it did not test.
Built end-to-end independently instead (T2, §3), top-1 falls to 1.8 % [0.4 ; 3.6] at n = 142 —
but that arm is **not interpretable**, its own twins identifying the real person only at chance,
so it bounds our pipeline and not the scenario (§5.4). The 36.4 % figure is not evidence for T2
either, and T2 remains untested.

**(2) The leakage is localised in the pattern of answers, not in memorised content.** An
ablation destroys the signal by permuting the order of a twin's answers while leaving their
content untouched — 33.1 % to 0.046 % top-1 (§5.5): what identifies is the dependence structure
between answers, not any answer's content, which is what a regurgitation account would require.
Structurally, the pipeline also trains nothing on the target population, so no train/test gap
exists to exploit, unlike Yeom et al. [yeom2018privacy] and Feldman [feldman2020memorization].
We state the limit of this plainly rather than let it be found: our training-cutoff control
(llama31-8b, cutoff preceding the panel's publication, copies nothing verbatim and leaks no more
than models that do [c7-gen-resultats.md]) is a control on **our own** twins, and it lives in a
regime where none of our twins identifies almost anyone (§5.7). It therefore cannot settle the
question for the published twins that carry this paper's rates, whose training data and cutoffs
we cannot probe. **We do not claim a measured dissociation between memorization and
re-identification.** The narrower claim we do make — a structural mechanism, localised by
ablation — is what separates our channel from the memorization [carlini2021extracting] and
free-text inference literatures [staab2024beyond, ko2026weakcues, lermen2026deanonymization].

**(3) Open-world rates with their human ceiling.** Closed-world 1-in-N rates assume the target is
in the pool; the defensible measurement drops that assumption and reports true detections against
false accusations (§5.3, Figure 1).

**(4) A defense measured with its real cost, and held against an adaptive attacker.** Not a new
mechanism — a variant of the 1998 Post Randomisation Method [gouweleeuw1998pram] — but applied to
LLM twins with a risk-utility curve that is measured rather than assumed, reported with the cost
component a single average would hide, tested against an attacker who knows how the defense
works, and measured on analyses a practitioner would actually run (§6). Against our own
preregistered prediction, differential privacy is *not* dominated by it on aggregate utility
(§6.2).

**(5) An attack strong enough to falsify our own first measurement.** A rarity-weighted
likelihood attack with out-of-fold parameters raises the Park archive's closed-world top-1 from
65.51 % to 90.40 % and triples its open-world rate at 1 % false accusations — a correction of our
own published figure (§5.3, §5.8).

**(6) A bits-of-identity instrument that transports across datasets where the raw rate does
not.** A derived instrument, not a discovery: a case of Rényi min-entropy leakage
[smith2009foundations], in the spirit of Eckersley's surprisal [eckersley2010unique], addressing
the transportability problem of the Rocher et al. scaling law [rocher2025scaling] by another
route (§5.6).

### 1.3 Negative results, stated in front

Fourteen preregistered predictions were refuted, two are inconclusive, and one could not be
tested at all (Table 1, §7.1). Our own
twins identify almost nobody, and the constructive demonstration meant to close that gap — raise
fidelity with a frontier model and watch the leakage return — **failed**: `openai/gpt-4.1` on
Twin's per-item recipe left fidelity at 0.1714 against their 0.708 (§5.7). We still do not know
what the Twin-2K-500 recipe does differently, though the unknown is narrower: neither the model
nor the call granularity. And the coupling that motivated this work does not survive its own
control (§5.1). We consider a reader who stops here to have read the paper honestly.

---

## 2. Background and Related Work

### 2.1 Privacy of synthetic data

Stadler, Oprisanu and Troncoso show that generated tabular data remains linkable to its sources
[stadler2022groundhog]. Giomi et al. formalise three attacks — singling out, linkability,
inference — and conclude, on their datasets, that linkability is the weakest risk
[giomi2023unified]. That conclusion is contested: Annamalai, Gadotti and Rocher
[annamalai2024linear], Ganev and De Cristofaro [ganev2025inadequacy, ganev2026rethinking] and
Ganev alone [ganev2024regulatory] show reconstruction attacks defeating distance-to-closest-record
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
synthetic generation breaks the link between identity and datum [taub2018differential].

*What distinguishes us.* These works re-identify from genuine auxiliary data. Our attack's input
is never a real datum of the target: it is a model output generated from a persona, compared
against real answers the attacker separately holds. We falsify precisely the CAP/TCAP premise, on
LLM-simulated survey microdata.

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

*What distinguishes us.* Those works all start from free text bearing direct semantic cues,
aggregated by an agent reasoning over it. Our channel is narrower and drier: closed-choice
categorical answers, no free text, no agentic reasoning, and a mechanism localised in the
dependence structure rather than in memorised content — established by ablation (§5.5), the
training-cutoff control of §5.7 bearing only on our own twins. Unlike Yeom and Feldman, our pipeline trains no
model on the target population.

### 2.4 Respondent simulation and twins

Argyle et al. launched the use of LLMs as panel substitutes [argyle2023outofone]. Park et al. cite
privacy in restricting access to their 1,052 agents' individual responses
[park2024agents], while the publicly posted replication package nonetheless carries
individual participant and agent responses (§8) — a risk anticipated, never measured. Toubia et al. publish the 2,058-twin
panel we attack, treating neither privacy nor linkage [toubia2025twin2k500]. Peng et al. document
group-fidelity distortions on that same panel without connection to re-identification
[peng2026funhouse]. Bonagiri et al. issue a normative call to evaluate these risks without
measuring them [bonagiri2026cognitive]. None of these works, nor the five surveyed in our
prior-art scan, measures a re-identification rate from twin outputs. That is the gap we fill.

### 2.5 Closest prior art and contradictors

Ward et al. test 13 attacks over 9 generators and 48 tabular datasets, and state in prose a
relation between quality and leakage close to ours [ward2025synthmia]; Byun et al. observe a
near-monotone frontier of the same type without a coefficient [byun2025riskcontext]. Three differences
separate them from our claim: their quality is *aggregate* (MMD, Jensen-Shannon divergence,
downstream AUC), never a correspondence to the right person; their risk is *membership* in a
training set, not 1-in-N identification; and they publish no coefficient — the only figure in
Synth-MIA is DCR against Max-AUC at r = 0.225, a weak correlation between two aggregate metrics.

Three contradictors hold that fidelity and risk separate: Platzer and Reutterer
[platzer2021holdout]; Adams et al., for whom a generator without formal guarantees preserves
fidelity and utility without evident privacy harm [adams2025fidelity]; and Shafieinejad et al., observing decoupling as quality saturates within a single tabular
diffusion model trained longer [shafieinejad2026diffusion]. Our response is not that they are
wrong: all three measure *aggregate* fidelity, never individual correspondence to the right
person, and none tests whether the coupling they observe survives a null matched on per-person
accuracy. Ours does not (§5.1). Their decoupling is a different axis from ours: theirs unfolds
over training time within one model (quality plateau against rising membership-inference risk);
ours is a cross-sectional correlation across twelve heterogeneous methods against 1-in-N
re-identification.

### 2.6 Defenses

Our D4 is not new. Shuffling answers between units of the same segment is a variant of the
Post Randomisation Method [gouweleeuw1998pram], which perturbs categorical variables through a
known transition matrix leaving margins invariant in expectation, and of data swapping, which
preserves them exactly at high aggregations — the same family as the partially synthetic data
tradition of Reiter and Drechsler, extended by Drechsler [drechsler2024thirtyyears] and Bowen et
al. [hu2023microdata]. What is new is the application to LLM twins with a measured
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
is assumed, not rebutted. Our answers to it are two: the explicit model above, and the open-world
measurement of §5.3 which gives the honest number. A third, T2, would remove the assumption
entirely — but we did not manage to test it (§5.4), and we therefore do not count it.

### T2 — Two organisations publish twins of the same cohort; attacker holds nothing real

If several organisations each publish their own twins of the same panel with sufficient item
overlap, a third party cross-references them holding no human answer at all. This threat model
has no direct precedent in the synthetic-data literature: Anonymeter's linkability presumes real
attribute values in hand [giomi2023unified], and Guépin et al. remove the real-auxiliary-data
assumption but target membership in a single generator's training set, never matching between two
independent generations [guepin2023synthetic].

**We tried to test it directly, and could not.** §5.4's 36.4 % twin-to-twin top-1 is a same-team,
same-persona-file measurement — only the model or output format varies — and does not speak to T2
as stated. Built as T2 actually describes, two pipelines sharing nothing but the target person
give top-1 1.8 % [0.4 ; 3.6] (n = 142/200, stopped by an OpenRouter transport error). **That
number does not establish the absence of a cross-organisation channel.** Both pipelines fail a
control we should have run before spending anything: their twins designate the right human at
chance (0.0–0.8 % top-1 against 0.83 % expected in a pool of 120, where the Twin team's own twins
reach 20.2–38.9 % on that same pool) [c7-reconciliation-facteurs-2026-09-12.md §3]. A contrast
between two twins that carry no individual information returns chance whichever factor is varied.
**T2 is therefore neither supported nor refuted: it was not tested** (§5.4).

### T3 — Pre-publication self-audit

A panel holder runs the attack against their own file before publication, to decide whether a
defense is required — the constructive use of the method, and the one the artifact (§9) serves.

### Attacker capabilities, all models

The attacker performs no training on the target population, has no query access to the
generating model, and uses only rank-based matching over categorical vectors. Costs are
negligible (§9).

---

## 4. Data and Methods

### 4.1 Datasets

**Twin-2K-500** [toubia2025twin2k500], 2,058 respondents, public under CC BY 4.0. Target: wave 4,
60 items usable in common out of 108 (40 purchase items of the form "would you buy this product
at this price?", 20 opinion items). Attacker context where applicable: 494 context items from
waves 1–3 plus 14 demographic variables. Chance top-1 in the closed pool is 0.049 %; chance
top-10 is 0.49 %. A human test-retest condition (the same people answering waves 1–3 and wave
4) gives the empirical ceiling: 81.6 % [79.9 ; 83.2] top-1, accuracy 0.745.

**Park et al. archive** [park2024agents], 1,052 participants, 177 common items, replication
package publicly posted. The archive documents five agent conditions (persona-, demographic-,
survey-, and interview-based, and composite); we analyse four — composite, interview-only,
survey-only, demographic — and leave the persona-based condition outside our re-identification
measurement (`data/PROVENANCE.md`; `FIGURE2_PIPELINE.md`). Human retest ceiling 96.8 %.

No new data was collected. The attack uses only already-published content.

### 4.2 Methods compared

Twelve heterogeneous methods carry the quality-leakage analysis: 8 LLM twins and 4 statistical
reference points (Demographics Only, B1 argmax over 14 demographics, B2 argmax, PMM k=10).
Additional comparators appear in §5.2: logistic regression on context, a k=1 donor on context,
two individualised *generators* (sampled LR, Gaussian copula), and an explicitly advantaged k=1
donor fitted directly on the target block.
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
preregistered before computation. We report every refuted prediction in Table 1. A census of the
repository's preregistrations found **no inversion** between a plan and its result across the 28
verifiable pairs; for the large majority the ordering is provable from version-control history,
while a small number were committed alongside their results or left unversioned, which we state
as a limit rather than claim an unbroken chain. The plans are not yet third-party timestamped.

### 4.5 Validity controls

*Provenance.* On Twin-2K-500, the context contains 0 wave-4 columns and 0 wave-4 QIDs; maximum
normalised mutual information between context and item is 0.16 against 0.31 for the retest on
the same item. On cells where wave 4 differs from waves 1–3, the JSON 4.1 output equals wave 4
in 37.7 % of cases and waves 1–3 in 37.9 % — symmetric, so no indication of copying. The
randomisation channel is excluded [c7-contre-examen-2026-09-11.md §2].

*Provenance, Park archive.* Over 34,915 cells where the human changed their mind, the composite
follows wave 1 in 41.6 % and wave 2 in 43.2 % — a difference of −1.6 points, no bias. The 4.3–4.9 point wave-1 bias of the other three conditions holds for the
`demographic` condition too, so it is a shared calibration artifact, not item leakage
[c7-stanford-provenance-resultats.md].

*Empty-run validation.* Uniform ranks yield 0.00 bits; the B0 mode baseline yields
−0.004 [−0.003 ; 0.002] bits.

*Fidelity precondition, adopted after it cost us an experiment.* We state as a rule the control
whose absence invalidated two of our own arms (§5.4): **no experimental arm built on a
regenerated pipeline is interpretable until that pipeline has been shown to beat the demographic
baseline in top-1 against the real human answers.** The check consumes no model call and no
budget, since it re-uses answers already held, and it must precede the first paid contrast. A
pipeline that fails it yields twins whose contrasts oppose noise to noise and return chance
whatever is manipulated. Our own pipeline B would not have passed
[c7-reconciliation-facteurs-2026-09-12.md §7]. Baselines in this paper are always taken at the
pool size of the arm they judge, that baseline being strongly pool-dependent: 2.13 % at 2,058,
9.20 % at 200, 13.29 % at 120.

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

Prediction (b) was refuted, and the witness that refutes it has since been rebuilt to remove a
real defect without changing the verdict. The original marginal null did carry that defect: its
*wrong* cells avoided the person's true answer (`c7_disjoint.py` l. 133), which inflated its
leakage by a factor 1.3 (top-1 41.2 % against 31.6 % once wrong values are drawn from the
population marginal). With the defect corrected, the witness still reproduces the coupling —
**rho 0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed** over the 12
configurations, measured on whole items (the human retest point excluded; the 0.969 above is
the disjoint-split value of the same quantity; Figure 2) — so **prediction (b) remains
refuted**:
reproducing the correlation between imitation quality and re-identifiability requires nothing
more than a matched per-person accuracy and correct positions drawn at random.

This witness is not an information-free object, and we do not describe it as one: at matched
accuracy it leaks **more** than our twin (31.6 % top-1 against 20.7 %). Five further witnesses,
which match that accuracy against a *surrogate* target rather than against the person, fall to
chance on both axes (top-1 0.040–0.063 % against 0.049 %, 0.00 bits, accuracy against the truth
0.41–0.44 against 0.53); the observed rho exceeds them, but that margin bears on nothing, their
null distribution being that of Spearman under total absence of information at n = 12 (95th
percentiles 0.547–0.594 against 0.497 expected).

We therefore do not claim, anywhere in this paper, that a twin's fidelity to its person causes
its leakage, nor that fidelity and identifiability are one axis. We also do not claim that at
equal accuracy every twin leaks more than every predictor: the residuals of the regression on
accuracy do **not** separate the families, with 3 of 7 LLM configurations falling below the
line.

One positive point remains testable outside this circularity: the human point, in raw position,
dominates on both axes — fidelity 0.303, leakage 0.520 — against 0.154 and 0.067 for the best
twin. There is no saturation at the top of the range.

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
obtains a top-1 of **0.00 % [0 ; 0.18]** (Clopper-Pearson, n = 2,058)
[c7-synth-ajuste-resultats.md §1].

**This claim does not generalise to every leakage metric, and top-10 runs the other way.** That
same advantaged comparator reaches a top-10 of **53.2 % [51.0 ; 55.3]**, *above* the twin's
42.7 % [c7-synth-ajuste-resultats.md §2]. The direction of the whole contrast therefore depends
on the choice of k, which no principle fixes at 1.

We do not claim that all individualised prediction identifies, nor strict accuracy equality: the
generators plateau at 0.476, never 0.590. Neither synthpop/CART nor CTGAN was tested.

### 5.3 Open world — the defensible measurement

Removing the closed-world assumption gives the number we consider hardest to attack in review.

At a false-accusation rate of 1 %, the strong attack (A-LLR, parameters estimated out-of-fold over
5 folds) recovers the right person **60.17 % [54.5 ; 64.4]** of the time on the Park archive and
**4.28 % [3.3 ; 5.6]** on Twin-2K-500, under a person-level bootstrap that **re-estimates** a_j
and q_j in each resample while keeping every copy of a person in the same fold
[c7-fort-monde-ouvert-ic-2026-09-12.md §2]. At FPR = 0.1 % these fall to **44.37 % [23.3 ; 53.8]**
(Park) and **1.01 % [0.05 ; 2.82]** (Twin) — intervals this wide because the threshold there rests
on roughly **one** absolute false positive on Park and two on Twin, so we report them as very
unstable estimates, not as measured rates. Statistical comparators (Demographics Only, PMM) stay
indistinguishable from noise at both FPRs. The human ceiling at FPR = 1 % is 54.5 % [50.8 ; 57.5]
and 90.7 % [88.2 ; 93.3] [c7-monde-ouvert-ic-2026-09-12.md §1].

**These figures replace the ones we first published, and the correction runs in both directions.**
The naive attack gave 3.04 % [2.0 ; 4.0] and 20.39 % [15.7 ; 24.5] at 1 % FPR, and 0.93 %
[0.2 ; 1.6] and 8.47 % [2.5 ; 16.2] at 0.1 %. On the Park archive the strengthening is real and
statistically clear — no overlap at either FPR, and the rate **triples** (20.39 → 60.17 %). **On
Twin-2K-500 the apparent gain does not survive its interval**: 3.04 → 4.28 % and 0.93 → 1.01 %
both overlap broadly, so we do not present the strong attacker as identifying better than the
naive one here. Park's closed-world gain (65.51 → 90.40 %) is a different quantity, untouched by
this comparison.

**Our preregistered prediction was refuted, and one half of it was then reversed by a better
attack.** We announced > 5 % (Twin) and > 30 % (Park). Under the naive attack both fell below the
bar — the refutation we reported. Under the strong attack Twin (4.28 %) still falls below, while
Park (60.17 %) passes the bar it had failed. We state both, in that order.

> **Figure 1 — Open-world detection, naive and strong attack.** Two panels, one per dataset,
> false-accusation rate on a log scale against true-detection rate. Each overlays the naive
> Hamming attack as a full ROC curve with the strong A-LLR attack as **isolated diamonds**, the
> latter measured at only two thresholds (FPR = 0.1 % and 1 %): **no curve should be read into the
> diamonds.** Statistical comparators sit near zero, the human retest ceiling above. *At a glance*:
> at a tenable false-accusation rate the risk is real and far above the comparators under both
> attacks, and the strong attack lifts the Park archive close to the human ceiling. This figure
> depends on no causal reading of the quality-leakage coupling.
> Data: `resultats/c7-monde-ouvert-roc.csv`, `resultats/c7-attaquant-fort.csv`.

### 5.4 The twin-to-twin channel within one pipeline — and why our T2 test does not count

Two twins of the same person designate each other when they share enough items, with no real
data on the attacker's side. The measurements immediately below share one team and, for
Twin-2K-500, one persona source per person: they gauge the channel within a pipeline, not the
cross-organisation threat model T2 (§3), whose test at the end of this section turned out not to
be interpretable.

**Twin-2K-500, tabulated by common-item count** [c7-transfert-resultats.md]. 30 pairs sharing
60 common items: mean top-1 **36.4 %**, maximum 83.58 %. 12 pairs sharing 19 common items: mean
top-1 **0.45 %**, minimum 0.06 % (chance 0.05–0.10 %). Demographics Only against the rich twins
gives 7.76 %, clearly below 36.4 %. The anti-artifact control — a decoy from the same segment —
gives 0.04 % on the 60-item pairs (factor ~900) and 0.10 % on the 19-item pairs (factor ~4.5).

**Park archive replication** [c7-transfert-stanford-resultats.md]: 1,052 agents, 177 common
items. Interview→survey top-1 **11.9 % [10.1 ; 13.8]**; survey→interview **13.0 % [11.2 ;
14.9]**; top-10 46.4 % [43.6 ; 49.4] and 45.2 % [42.3 ; 48.1] respectively
[c7-transfert-stanford-attaque.csv]. Demographic bound 1.5–2.5 %. Anti-artifact decoy control
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

**The channel is not an artifact of a shared prompt template or of demographics.** Decomposing
agreement between two twins of the same person over the 60 common items: the floor between
*strangers* is **46.0 %**, the demographic-ideological segment adds only **3.8 points**, and the
person adds **17.4 points** — 82 % of the rise above the floor. A pure-population witness (each
twin replaced by its segment's leave-one-out modal answer) identifies the right person **0.07 %**
of the time against **36.4 %** for the real attack [c7-temoin-prompt-resultats.md].

**The cross-dataset anomaly, explained in part.** The Park archive shares 177 common items —
roughly three times the 60 of Twin-2K-500 — and leaks roughly three times *less*. Item count is
the wrong denominator: the 177 GSS items are strongly redundant (mean Cramér's V 0.1055 against
0.0834), giving **≈ 9.0 effectively independent items against ≈ 10.1** on Twin — a real ratio of
**0.89, not 2.95** [c7-anomalie-park-2026-09-12.md §4]. Pool size runs the wrong way too:
shrinking Twin's pool to 1,052 *raises* its top-1 (37.3 → 44.1 %, disjoint intervals), while Park
already has the smaller pool. **A residue of roughly 3× remains unexplained** at comparable
effective information, and we declare it: the remaining candidates — persona format and length,
and the different generating pipelines — are not testable on the material we hold.

*Limits.* The 12 low pairs are exactly those at 19 common items: the effect follows the
shared-item count, not an aberrant configuration. On the Park archive the item-rate relation does
not follow Twin's.

**T2 itself: two genuinely independent pipelines, and a test that does not count.** Two pipelines
sharing nothing but the target person — `deepseek-v4-flash` structured JSON dossiers versus
`qwen-2.5-72b` narrative biographies, different templates, different output formats — matched
head to head on the same 60 items (n = 142 of 200 planned, stopped by a second OpenRouter
transport error; a first such stop, at n = 82, was reconciled and confirmed unbilled)
[c7-deux-organisations-resultats.md]. Preregistered rule: T2 survives if the top-1 CI excludes the
segment control *and* stays at least 2× the demographic baseline. Result: top-1 1.8 %
[0.4 ; 3.6], against a demographic baseline of 9.2 % computed on the enclosing pool of 200; the
baseline matched to this arm's own pool of 142 was never computed and lies above 9.2 %, the same
baseline reaching 13.29 % at a pool of 120.

**We no longer read this as a refutation of T2.** The witness is built on the pipeline of the
paragraph below and shares its defect: neither arm produces twins that identify the real person
better than chance (0.0 % and 0.8 % top-1 against 0.83 % expected on a pool of 120, where the
Twin team's own twins reach 20.2–38.9 % on that same pool)
[c7-reconciliation-facteurs-2026-09-12.md §3]. The comparison therefore opposes two noise
sources, and would have returned chance whether or not a cross-organisation channel exists. It
measures our instrument, not the world: the honest statement is that **T2 could not be tested
here**, not that it was disproved. The 36.4 % figure above remains a same-pipeline measurement
and is not evidence for T2 either, so the threat model stands open in both directions.

**One-factor-at-a-time: arithmetically sound, not interpretable.** T2 changed model, template and
persona format together; a follow-up varies them one at a time from our own baseline pipeline B —
not from the 36.4 % intra-team configuration, which is not ours [c7-factoriel-resultats.md]:
model alone 0.67 % [0.00 ; 1.75], prompt template alone 0.83 % [0.00 ; 2.08], persona format
alone 2.65 % [0.50 ; 5.13] (n = 120, 360 calls, 0 failures; cost \$0.54; chance is 0.83 % on this
pool). The arithmetic is reproducible and correct [c7-reconciliation-facteurs-2026-09-12.md §2].
**The interpretation is not available to us**: pipeline B and all three derived conditions
identify the real person at chance (§3 of that note), so each contrast opposes two noise sources,
and no such arm can show that a factor destroys a channel it never carried. We therefore withdraw
the reading we first gave these numbers — that changing any single component collapses the
channel — and with it the refutation of the matching preregistered prediction (model ≈ 20 %,
template ≈ 15 %, persona ≈ 8 %): an arm that could test nothing refutes nothing. We also correct
a comparison of our own. These twin-to-twin rates were set against 13.29 % [7.46 ; 19.29], which
is a *twin-to-human* baseline on the same pool of 120; the homogeneous twin-to-twin baseline on
that pool is 23.69–34.42 %, so the mismatch flattered these three conditions rather than
penalising them.

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
not any answer taken in isolation.

That ablation starts from a higher rate than this paper's headline 20.7 %, and the difference is
a change of attack surface, not a discrepancy: the ablation attacks the **40 purchase items
alone**, where the headline rate uses all **60 common items**. Adding the 20 opinion items
therefore *lowers* top-1, from 33.1 % to 20.7 %. That is consistent with the rest of this
section rather than in tension with it — those items identify 46× less, and a naive Hamming rule
is diluted by uninformative items rather than helped by them — and we read it as an independent
confirmation of H1's direction, not as a loose denominator.

**Three preregistered hypotheses refuted.** H1 (entropy): opinion items carry 2.10 bits against
0.99 for purchase items and identify 46× less — top-1 0.24 % [0.07 ; 0.46] for the 20 opinion
items against 11.0 % [9.9 ; 12.3] for the purchase subset matched to them on entropy by
Hungarian assignment — a 20-item comparison, not the 40-item block above. H4 (stereotypy): 36.2 % [35.6 ; 36.8] against
37.5 % [36.9 ; 38.1] in humans. And "deviations alone carry ≥ 80 % of the leakage": 0.68 % in
the mixed condition.

We do not present "wrong deviations alone = 0.0 %" as a result: it is a floor of the method,
which cannot detect a signature there.

*Limits.* The mechanism is established on Twin's purchase block alone, and is in apparent tension
with the Park archive, where opinion items identify most. Two simple explanations are excluded: at
20 items the Park archive gives 11.7 % against 0.24 % for Twin's 20 opinion items, **at lower
per-item entropy** (1.30 against 2.10), so neither item count nor entropy accounts for it
[c7-stanford-resultats.md §6]. What remains is consistent with the block effect, which we present
as the **best-supported hypothesis, not a result**: the dedicated test (copula alone against
margins alone) is not done.

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

### 5.7 The risk depends on the recipe — and we could not reproduce it

Our own twins, produced in a single call to cheap models from a raw profile, identify almost
nobody: 0.00 % to **0.83 % [0 ; 2.15]** (deepseek-v4/R1) across 7 cells, against 2.13 % for the
other team's Demographics Only. The interval [0 ; 2.15] **contains** 2.13 %, so no precise
factor is established — only the order of magnitude, that no model reaches 1 %, is defensible
[c7-gen-resultats.md]. Any previously circulated "25× below" figure is withdrawn.

Memorization is not the explanation here: llama31-8b, with a training cutoff preceding
publication, copies nothing verbatim and leaks no more than the models that do copy. This is a
control on our own twins, in a regime where none of them identifies almost anyone; we do not
extend it to the published twins of §5.2–§5.4, whose training data we cannot probe (§1.2).

**Two further preregistered predictions refuted.** (i) R1 ≥ 10 % on at least 2 of 3 models — no
model reaches 1 %. (ii) Call granularity would explain the leakage — not confirmed
(underpowered, especially at n = 10 for the per-item arm): single call 0.00 % [0 ; 8.8] and
per-item call 0.00 % [0 ; 30.85], with top-10 running in the **opposite** direction to the
prediction (7.5 % against 0 %) [c7-recette-resultats.md].

We therefore do not claim that leakage comes from the call format, nor that the cause is
identified. **It is not.**

**We then paid to test the obvious explanation, and it failed.** Raising fidelity with a frontier
model to see whether the leakage returns was run on `openai/gpt-4.1` (Twin's own model class)
using Twin's per-item call recipe without
modification: 30 persons × 60 items = 1,800 calls, 100 % parse rate, 4.9949 USD of actual cost
[c7-fort-resultats.md]. Accuracy reached **0.4722 [0.4361 ; 0.5050]** against Twin's 0.574;
fidelity **0.1714** against their 0.708; top-1 and top-10 **0.00 % [0 ; 11.57]**
(Clopper-Pearson, n = 30) — below even our cheap twins (0.83 % at best). **One further
preregistered prediction refuted**: accuracy > 0.55; top-1 > 5 % is **not refuted** — 0/30 gives
an exact 95 % CI of [0 ; 11.57 %], which contains the 5 % threshold: inconclusive for lack of
power. Fidelity > 0.10 was confirmed at 0.1714, but barely above our best cheap twin (0.177): the
frontier model bought us almost nothing. We did not make the leakage come back, because we did
not manage to reach Twin's fidelity — and it is that fidelity gap, not the underpowered top-1,
that carries the conclusion.

**The curve is confirmed a third time, by an independent point.** At the fidelity actually
reached (0.1714), the regression over the 12 points of `c7-compromis.csv` (slope 0.1834,
r = 0.785) predicts leakage of **1.10 %, 95 % CI [−9.15 ; 11.35]**, and the observed 0.00 % falls
inside it. Coming from a new model *and* a new recipe, it is an independent check: fidelity never
rose, so the point follows the curve rather than breaking it.

**The unknown narrows instead of disappearing.** Neither the model nor the call granularity, what
remains implicated is the **format and length of the profile**: Twin's full JSON persona runs to
roughly 121,000 characters against our 8,000-character truncation. Only Twin's exact pipeline or
their complete personas would settle it.

*Limits.* n = 40 persons for the recipe arm, truncated to n = 10 on the per-item arm, and n = 30
on the paid frontier-model arm; a floor effect is not excluded. Roughly 1,490 calls first failed
with HTTP 402 from in-flight credit reservation, not lack of balance, and were retried at
decreasing concurrency without double billing.

### 5.8 Replication on a second dataset

On the Park archive, the composite agent designates the right participant among 1,052 **in a
closed world** in **90.40 % [88.6 ; 92.2]** of cases under the strong attack, with a top-10 of
97.8 % [c7-attaquant-fort-resultats.md]. The human retest ceiling is 96.8 %.

**This figure replaces the 65.51 % [62.7 ; 68.3] we first published** (measured at 65.7 %
[62.7 ; 68.6] by the original script — same condition, two implementations): a naive agreement
attack understated this archive's leakage by 38 % in relative terms. An in-sample
information-weighted variant reaches 93.25 %, which we do not claim as our result (§4.3).

The remaining conditions are **naive-attack measurements**, and the strong attack was **not**
re-run on them: interview-only **44.7 % [41.8 ; 47.5]**, survey-only 20.6 % [18.2 ; 23.0],
demographic 2.26 % [c7-stanford-resultats.md]. The interview-only figure carries zero documentary
exposure to the survey, so it is the cleanest demonstration that an agent built from a
conversation alone identifies its person — but given what the strong attack did to the composite,
**44.7 % must be read as a lower bound**.

We do not compare the Park and Twin rates as measurements of the same thing: item count (177
against 60), per-item entropy (1.30 against 0.99) and human ceilings (96.8 against 81.6) all
differ. Equalised at k = 60, Park gives 34.0 % [23.5 ; 51.5] against Twin's 20.7 % — naive attack,
20 draws, a very wide interval.

### 5.9 Scale

From N = 50 to N = 2,058, the twin/demographic ratio grows from 2.8 to 9.7: top-1 falls from
53.2 % [50.0 ; 56.3] at N = 50 to 20.7 % [20.7 ; 20.8] at N = 2,058, and the share of the human
ceiling from 57.0 % to 25.4 % [c7-echelle-resultats.md]. These are naive-attack rates; the scale
study was not re-run under the strong attack.

**We extrapolate no value beyond N ≈ 4,000**: a power law and a logarithmic law fitted on the
same 6 points already diverge at twice the range (18.1 % against 13.9 %).

> **Figure 2 — Imitation quality against leakage, with its control
> (`article/figures/fig2-couplage.png`).**
> Abscissa: individual fidelity (`fidelite_plancher`, share of the human floor, 0 to 1,
> linear). Ordinate: closed-world top-1 leakage, linear, 0 to ~0.85. Thirteen points: the LLM
> twins (filled circles), the statistical reference points (grey diamonds), Demographics Only
> broken out (triangle), and the human retest (star) at fidelity ≈ 1 / leakage 81.6 %.
> All thirteen points carry **error bars on both axes**, from a per-person bootstrap with 2,000
> resamples. **Inset**: the marginal null on a Spearman-rho axis — the 5th–95th percentile
> envelope of the corrected witness (mean rho 0.974) matched only on per-person accuracy
> (`c7-disjoint-nul.csv`) drawn as a grey band, with the observed rho (0.965) plotted as a single
> point inside that band. *What the reader should see at a glance*: the points rise
> together from left to right with no plateau at the top, **but the observed correlation sits
> inside the band that a null matched only on accuracy already produces.** An honest
> contribution: the coupling is measured, not shown to be individual-specific.
> Data: `resultats/c7-compromis.csv`, `resultats/c7-compromis-robustesse-points.csv`,
> `resultats/c7-disjoint-nul.csv`.

---

## 6. Defense

Shuffling the purchase answers between people of the same demographic segment (D4) brings
closed-world top-1 from **20.7 % [19.0 ; 22.4]** to **0.13 % [0.01 ; 0.28]**
[c7-defense-resultats.md]. Per-item distribution and between-segment differences are preserved
**exactly, by construction**, as PRAM predicts.

**The cost is not a single average.** Reported by component: 0.0 points on the per-item
distribution, 0.0 points on group differences, and **4.4 points on inter-item correlations**.
We therefore withdraw the summary that presented D4's cost *as* a single mean of 1.47 points:
that figure is the unweighted mean of the three components (`utilite_globale` in
`c7-defense-resultats.csv`, carried as `perte_utilite_points` in `c7-defense-courbe.csv`), two of
which are zero by construction, so quoting it alone divides by three an effect that falls
entirely on the third. The quantity itself is not withdrawn, only its name and its use: it is a
**composite utility index**, and it is the one form in which the comparison with differential
privacy can be made at all, since the DP mechanism's loss is measured on that same index
(§6.2). Wherever it appears below it is named as the index, never as the cost of the defense.

**The cost is worse than that summary suggests.** On that same indicator measured against the
real human answers, `erreur_correlations_hum` rises from **5.775 to 9.709** after D4, a
degradation of **68.1 %**. The defended twin moves *away* from the humans on correlations; it does not
move closer. Any framing in which the defense's cost is absorbed by an error already present
compares an increment to a level, and is incorrect.

Alternatives: D1 (k=10 aggregation) gives 0.55 % for 3.8 points spread across all three
components; D2 (noise) never descends below 1 %.

### 6.1 The defense against a strong, then an adaptive attacker

The defense figure above was measured against the naive attack, which §5.8 shows can badly
understate leakage. We
therefore re-ran it against the strong attack, recalibrated on the *defended* outputs, and then
against an attacker who knows the defense mechanism and knows which items it leaves untouched
[c7-attaquant-fort-resultats.md].

D4 holds. Top-1 goes from 0.13 % (naive) to **0.24 %** under the recalibrated strong attack, and
the **adaptive** attacker plateaus at **0.29 %** (strategy S1, leaving the 20 opinion items
intact; S1+S3 identical; segment-invariant strategy S3 alone 0.05 %). That is two orders of
magnitude below the 20.7 % undefended rate, and never above 1 %. **Attribute disclosure is not
demonstrated either**: the best strategy names the correct `S_gra` segment in **7.7 %** of cases,
against 6.8 % at chance and **12.6 %** for the trivial rule of always answering the most frequent
segment (40 segments) — the attack does worse than not attacking.

**A reservation that bounds the guarantee.** This residue comes *entirely* from the 20 opinion
items D4 does not permute. The guarantee holds for this split — 40 purchase items shuffled, 20
opinion intact — not for a design leaving a more informative block untouched. We do not present
0.29 % as a bound on the defense in general.

### 6.2 Differential privacy: our prediction refuted, and the argument that survives

We preregistered the prediction that at a moderate budget, differential privacy would be
dominated by D4 on the aggregate risk-utility table. **It is not.** With per-item marginals
perturbed by Laplace noise (L1 sensitivity 2, budget split equally over 60 items, basic
sequential composition) followed by i.i.d. per-item sampling — degree-0 PrivBayes, no joint
structure — the DP synthesiser at eps = 3 and eps = 10 loses **3.33** and **3.38** points on the
**composite utility index**, within 5 points of D4's **1.47** on that same index, while its
top-1 (**0.158 %**, **0.000 %**) is **not above** ours (0.13 %) [c7-dp-resultats.md]. The
comparison runs on the aggregate index because that is the only scale on which the two
mechanisms are commensurable. We keep it here for that reason alone, and name what it is: 1.47 is
the unweighted mean of three components of which **two are zero by construction** (0.0
distribution, 0.0 group differences, 4.4 correlations), so it divides by three an effect borne
entirely by the third. It is not D4's cost (§6).
We do not claim our defense beats DP, on either axis.

The utility floor is architectural, not budgetary: the non-private control (eps = ∞) still loses
3.52 points, only distribution error falling with epsilon (9.7 → 3.2 points).

**What survives is a theoretical point, not an empirical win.** DP protects an individual's
*membership* in the dataset used to compute a published statistic — "is Alice in the sample?".
Our attack assumes Alice is already known, since her profile is the twin's input, and asks
whether **the output conditioned on Alice** can be linked back to her: record linkage, not
membership. The DP generator escapes that attack only by **never conditioning on an individual**
— individual fidelity stays at most 0.2 points at every budget, including infinite — that is, by
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
between two answers of the same person — inter-item regression, the composition of a PCA axis.

*Limits.* Tested on a single block, of a single twin, of a single dataset (§2.6 places the
mechanism in the PRAM and data-swapping tradition).

---

## 7. Discussion and Limitations

### 7.1 The fourteen refuted preregistered predictions, two inconclusive, and one untestable

| # | Prediction (preregistered) | Outcome | Source |
|---|---|---|---|
| 1 | The quality-leakage coupling exceeds a null matched on accuracy alone | **Refuted.** Null rho 0.974 [0.950 ; 0.993] against 0.965 observed, over the 12 configurations on whole items; the original null (0.984 against 0.969, disjoint splits) carried a defect since corrected, with no change of verdict (§5.1) | `audit-renversement-2026-09-12.md` |
| 2 | Open-world > 5 % (Twin) and > 30 % (Park) at FPR = 1 % | **Refuted as first measured** (naive attack: 3.04 % and 20.39 %). Under the strong attack Twin still fails at 4.28 %, while Park **passes** at 60.17 % | `c7-monde-ouvert-resultats.md`, `c7-attaquant-fort-resultats.md` |
| 3 | Twin-to-twin top-1 ≥ 20 % on the Park archive | **Refuted.** 11.9–13.0 % at 177 common items (failure criterion not met either) | `c7-transfert-stanford-resultats.md` |
| 4 | The twin-to-twin channel leaks on the 19-common-item pairs | **Refuted.** 0.45 % mean top-1, at chance (0.05–0.10 %) | `c7-transfert-resultats.md` |
| 5 | H1: per-item entropy drives identification | **Refuted.** Opinion items 2.10 bits, identify 46× less | `c7-mecanisme-resultats.md` |
| 6 | H4: twins are more stereotyped than humans | **Refuted.** 36.2 % [35.6 ; 36.8] vs 37.5 % [36.9 ; 38.1] | `c7-mecanisme-resultats.md` |
| 7 | Deviations alone carry ≥ 80 % of the leakage | **Refuted.** 0.68 % in the mixed condition | `c7-deviations-resultats.md` |
| 8 | R1 ≥ 10 % on ≥ 2 of 3 of our own models | **Refuted.** No model reaches 1 % | `c7-gen-resultats.md` |
| 9 | Call granularity explains the leakage | **Not confirmed — inconclusive (underpowered at n = 10).** 0.00 % both arms (95 % CI [0 ; 8.8] at n=40, [0 ; 30.85] at n=10); top-10 runs opposite (7.5 % vs 0 %) | `c7-recette-resultats.md` |
| 10 | Cost per unit of individual fidelity is roughly constant | **Refuted at equal sample.** CV 0.436 vs 0.357 on the same 9 points | `c7-compromis-resultats.md` §5 |
| 11 | Per-item entropy correlates with identifying power consistently | **Refuted.** Opposite sign by dataset: r = −0.81 (Twin), +0.57 (Park) | `c7-bits-resultats.md` §3 |
| 12 | P1: a stronger attacker gains ≥ 20 % relative over the naive attack | **Refuted on Twin** (+12.2 %, 20.7 → 23.23 %); held on Park (+38.0 %, 65.51 → 90.40 %) | `c7-attaquant-fort-resultats.md` |
| 13 | P3: an adaptive attacker knowing the mechanism breaks the defense | **Refuted, in the defense's favour.** Plateaus at 0.29 %, never above 1 % | `c7-attaquant-fort-resultats.md` |
| 14 | At a moderate budget, DP is dominated by our defense on the aggregate table | **Refuted.** eps = 3/10 lose 3.33/3.38 points on the composite utility index against D4's 1.47 on that same index — a mean diluted by two components that are zero by construction, never D4's cost (§6) — top-1 0.158 % [0.012 ; 0.340] / 0.000 % [0 ; 0.18] against 0.13 % [0.01 ; 0.28] | `c7-dp-resultats.md` |
| 15 | A frontier model on Twin's per-item recipe reaches accuracy > 0.55 | **Refuted.** 0.4722 [0.4361 ; 0.5050] | `c7-fort-resultats.md` |
| 16 | That same twin reaches top-1 > 5 % | **Not refuted — inconclusive.** 0.00 % [0 ; 11.57] (Clopper-Pearson, n = 30); the preregistered 5 % threshold lies inside the interval | `c7-fort-resultats.md` |
| 17 | T2, independent pipelines: top-1 CI excludes the segment control and stays ≥ 2× the demographic baseline | **Not testable with this instrument — counted as neither.** 1.8 % [0.4 ; 3.6] at n = 142/200 (API transport error), but both arms' twins identify the real person at chance, so the contrast opposes two noise sources and decides nothing in either direction (§3, §5.4) | `c7-deux-organisations-resultats.md`, `c7-reconciliation-facteurs-2026-09-12.md` |

Rows 9 and 16 were listed as refutations until adversarial review found that a percentile
bootstrap on a zero-event sample can only return "[0 ; 0]" — an arithmetic property of the
resampling, not a confidence interval. Recomputed exactly, neither is refuted: both are
inconclusive for lack of power, and we report the reclassification rather than keep two
refutations we are not entitled to. Row 17 left the refutation count later still, and for a
different reason: its arithmetic is exact, but the pipeline that produced it carries no
individual information, so the arm decides nothing about the threat model it was built to test
(§5.4). Seventeen rows, fourteen refutations, two inconclusive, one untestable.

Three further preregistered outcomes were partial rather than refuted, and we count them as
neither confirmations nor refutations: D4 erases two publishable inter-item effects while leaving
signs unchanged, and its PCA prediction holds on variance but is contradicted on the loadings
(§6.3); the paid frontier-model run cleared its fidelity > 0.10 bar at 0.1714, barely above our
cheapest twin (§5.7). One prediction held outright under adversarial pressure: P2, that D4 stays
below 1 % against a strong attacker (§6.1).

### 7.2 What we do not know

**An excess cost in bits per unit of fidelity, real but unexplained.** On equal samples,
CV(bits/fidelity) = 0.436 against CV(bits/accuracy point) = 0.357 over the same 9 points: the
second remains less dispersed, but the gap shrinks. With so few points and no identified
mechanism, the excess **must not be attributed to "LLMs" as a family**; we describe it as
unexplained [c7-compromis-resultats.md §5].

**We did not reproduce the leakage with our own twins** (§5.7), including with a paid frontier
model on Twin's own per-item recipe — an open limit, never a mechanism, and a narrower one than
before: neither the model nor the call granularity, leaving the persona's format and length. Only
Twin's exact pipeline or their complete personas would settle it.

**Rates do not predict across datasets.** The normal-maxima model lands close on Park k = 60
(0.354 predicted, 0.340 observed) but fails both its controls (0.053 for 0.206 observed; 0.983
for 0.656): an isolated success between two failures is a coincidence, not a law
[c7-bits-resultats.md §3]. Only conditional information retains sign and order of magnitude
across datasets (r = 0.72 and 0.89).

**The twin-to-twin channel's cross-dataset rate is only partly explained** (§5.4): item count is
the wrong denominator, pool size runs the wrong way, and a residue of roughly 3× survives both
controls with no mechanism we can test on the material we hold.

### 7.3 Multiplicity

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
frontier-model run), which is why Table 1 and the census do not carry the same totals.

A second pass extended the confirmatory family to 15 tests convertible to a p-value and applied
both Holm and Benjamini-Hochberg. **Neither changes any verdict**, and the two agree on all 15:
the p-values are bimodal — eight at or below 0.0025, seven already near 1 — so no claim here rests
on a marginally significant result [c7-multiplicite-globale-2026-09-12.md §3]. It also flags three
thresholds as fragile, which we name rather than let a reviewer find: the frontier twin's
**fidelity > 0.10** bar, confirmed at 0.1714 but refuted had it been set at 0.18 — while our own
weakest known twin sits at 0.177, above the value that cleared it; the choice of k in top-k
(§5.2); and the functional form of the scale law beyond the measured range (§5.9). A common
bootstrap across analyses reusing the same 2,058 people was abandoned for cost, so the intervals
of §5.1–§5.3 on Twin are correct individually and carry no simultaneous coverage.

### 7.4 Scope, and two limits established by failure

Two datasets, one language, one questionnaire format, categorical closed-choice answers only. The
mechanism analysis and the defense both rest on a single block of a single dataset. We make no
claim about conversational agents or panels outside the two studied here. Two further limits we state with the specific resource that would lift them, because we
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

**Datasets, and the terms we are bound by.** Twin-2K-500 is public under CC BY 4.0. The Park
replication package is publicly posted on OSF (node `t6g7k`), but public posting is not a
licence: the OSF API returns `node_license: null` for that node, so **no licence is declared**
and public access carries no right to redistribute the individual responses it contains. Its
questionnaire content is a General Social Survey instrument, and **NORC's terms of use forbid
reproducing the GSS in any form without prior written consent**. We record both constraints
because an article about privacy that passes over the terms of use of its own data disqualifies
itself.

*What we do in consequence, verified rather than assumed.* We redistribute no individual
response file from either archive. We checked our own released material file by file: the
review artifact (§9) ships only code and a synthetic dataset generated at run time and reads
nothing from `data/`, which is excluded from version control; and every published table under
`resultats/` is an aggregate by condition, by item or by bootstrap replicate, carrying no
individual record and no participant identifier. Only analysis code and disclosure-reviewed
aggregates are published, with the NORC citation (Smith, Davern, Freese and Morgan, *General
Social Surveys, panel files*, Chicago: NORC) and attribution to Park et al. One limit we state
rather than resolve: NORC's published terms address reproduction of the GSS and do not speak to
derived aggregate statistics, and we found no primary source settling that case — the reading
that per-item and per-condition aggregates fall outside the prohibition is ours, not NORC's.

No new data was collected: the attack uses only already-published content (human
answers and twin outputs). A limit to note: participants did not specifically consent to a
re-identification test on the twins generated from their answers.

**No individual is identified.** No name or identifier linking a `pid`/`TWIN_ID` to a real
person is published or listed. Only rates aggregated over the full cohorts are reported; no
individual case is named or shown.

**No new harm on Twin-2K-500.** Twin-2K-500 already publishes, for each person, their
identifiers and real answers beside their twin: matching is trivial without any attack. The
result does not create new harm on this specific dataset; it documents a generic risk for
anyone releasing "anonymised" twins without that key — a practice Twin-2K-500 does not follow.

**The Park archive is a different case, and we make no such claim there.** That argument rests
on a key published beside the twins, and it does not transfer: on the Park archive no trivial
alignment makes the matching free, the rates we measure are far higher (90.40 % closed-world,
60.17 % open-world at 1 % false accusations), and the objects we attack are the very ones whose
individual release the authors treated as a privacy matter. We therefore do not argue that this
paper creates no new harm there. What limits the harm is narrower and we state only that: we
publish no individual record and no per-person result from that archive, only aggregate rates;
and the disclosure below is addressed to its authors, whose own warning this work quantifies.

**Benefit.** Several teams publish individualised LLM twin outputs without any linkage risk
analysis. This provides a first measured figure for that risk on public datasets and a
reproducible method for testing it elsewhere *before* publication.

**Responsible disclosure, and its actual state.** Letters to the Twin-2K-500 authors (Toubia et
al.) and to Park et al. are drafted, with a 30-day response window and an offer to share code
and report in advance. The tone toward Park et al. is fixed: *your warning was accurate, here is
its measured magnitude*. **As of this submission the letters have not been sent and the 30-day
window has not opened.** Sending them is a decision of the responsible investigator; it is on
the critical path and is to happen before any preprint posting or code release. We write this
plainly rather than imply a consultation that has not taken place: filing this manuscript is
itself a disclosure event, and the committee should know the window was still closed when it was
filed.

**The Park et al. case.** Their supplementary material (Participant Consent) already warned
participants that their information might be "inadvertently shared" and acknowledged that
complete anonymity remains challenging. They named the risk, obtained an ethics agreement
worked over more than six months, pseudonymised, restricted access to part of the material and
planned a 25-year withdrawal. What is nevertheless public is the replication package we analyse,
which carries the 1,052 participants' individual responses together with the agent conditions'
responses (§4.1): the protection announced in the paper does not cover the objects this attack
consumes. We flag that gap as a question for the authors rather than a finding against them —
from outside we cannot tell whether the restriction was lifted or never covered the replication
package — and it is precisely what the disclosure letter must state correctly.
No public audit had measured the magnitude of that named risk;
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
inter-item correlations, a 68.1 % worsening of the gap to human correlations (5.775 → 9.709), and the
loss of every inter-item analysis downstream (§6.3) — it holds at 0.29 % against an attacker who
knows the mechanism, but only for a split that shuffles the informative block (§6.1).
(f) Differential privacy where the published object can be a population statistic rather than a
per-person twin: it answers a different threat model, and buys its low leakage by never
conditioning on an individual (§6.2).

**Public interest.** The AAPOR report of 8 May 2026 [aapor2026responsibleai] ranks synthetic
response generation as the most risky of the core tasks it evaluates and names
re-identification by linkage without quantifying it. A risk named by practitioners and
professional bodies but never measured
justifies an independent measurement followed by responsible disclosure rather than silence.

**Ethics review and scope.** This study was not submitted to an external ethics panel such as
an IRB. It relies exclusively on secondary data already made public by their original
publishing teams — Twin-2K-500 (CC BY 4.0) and the Park et al. replication package — and no new
data was collected from any person: we surveyed no one, interviewed no one, and had no contact
with any data subject. On that basis we judged the study out of scope for human-subjects
review; §8 above records the corresponding limit (participants did not specifically consent to
a re-identification test on the twins generated from their answers).

This scoping does not extend to the released artifact, which processes no real person's data at
all (§9).

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
is never read by the artifact. Two conditions bear on obtaining it, and public availability
satisfies neither: **no licence is declared** on that OSF node (`node_license: null`), so public
access confers no redistribution right; and the GSS content it carries falls under **NORC's
terms of use, which forbid reproducing the GSS in any form without prior written consent**
(§8). Obtain both datasets from their original sources and verify current terms of use there
before any download.

**Preregistrations.** `resultats/c7-preenregistrement.md`,
`resultats/c7-defense-preenregistrement.md`, `resultats/c7-stanford-preenregistrement.md`, each
written before any computation. Third-party timestamping is pending.

**Environment.** Python 3.13.14, numpy 2.5.2, pandas 3.0.5, scikit-learn 1.9.0. No network
dependency.

---

## 10. AI Use

Large-language-model-based agents were used throughout this project: they wrote the analysis
code, ran the experiments, drafted this manuscript, and conducted adversarial review of both
the code and the text. We state this in full rather than narrowly, because an account that
understated that involvement would mislead a reader more than a plain one.

The responsible investigator directed the work throughout: set the research questions and the
falsifiable predictions in advance of each analysis, decided what to keep, discard, or redo,
authorized all paid computation, and is responsible for the accuracy and integrity of the
submission, including this section. No generative AI tool is listed as an author.

Three checks bear on how much trust the model-produced outputs warrant. First, quantitative
predictions were preregistered in writing, dated, before the corresponding analysis script was
run; the repository holds several dozen such preregistrations, one per analysis. Second, the
analysis pipeline fixes a random seed at every stochastic step, and independent reruns are
checked to reproduce identical output before a result is reported. Third, the manuscript and
code were subjected to adversarial review passes whose default posture is rejection; these
passes are how two substantive defects were found and corrected before submission: a
statistical control meant to carry only each person's accuracy margin that in fact copied
their true individual answer with the complementary probability, and a bootstrap confidence
interval reported as "[0, 0]" on a
zero-event sample — an artifact of the percentile method rather than a genuine null result,
since replaced with an exact Clopper-Pearson interval.

These checks reduce, but do not remove, the risk that a model-produced number or claim is
wrong; the responsible investigator remains accountable for every figure and statement in this
paper regardless of how it was produced.

---

## References

Bibliography maintained in `article/references.bib`. Of its 47 entries, 20 were checked directly
against their primary source in this project (18 in the main verification pass, 1 in a
supplementary pass, 1 for the AAPOR report cited above); the remaining 27 carry over an earlier
verification whose working notes were lost before this project's records began and could not be
re-audited here — not infirmed, but not auditable in this repository. One entry
(`gouweleeuw1998pram`) has no retrievable DOI and is flagged for confirmation before submission.
Full accounting in `article/references-verification.md`. Keys cited in
this manuscript, in order of
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

