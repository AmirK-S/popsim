# Note pour le responsable du projet (avant toute décision)

Ce brouillon sert à préparer **deux** divulgations responsables — aux auteurs de
Twin-2K-500, et à l'équipe Stanford de l'archive des 1 052 agents génératifs — si et quand
le responsable du projet décide d'en envoyer une. Rien n'est envoyé par cet agent : les
deux textes anglais ci-dessous ne sont que des projets de courriel, à relire, modifier et
signer. **Tranché le 12 septembre 2026 et déjà appliqué aux deux textes : (1) signature —
Amir KELLOU SIDHOUM, chercheur indépendant sans affiliation institutionnelle,
`aboutdotblank@gmail.com` ; (2) partage du code — le dépôt public `github.com/AmirK-S/popsim`
est cité tel quel dans les deux lettres, le rapport complet étant envoyé sur demande ; aucune
pièce jointe n'est promise. Le répertoire `demandes/` n'est pas versionné et n'est donc pas
exposé ; aucune des deux lettres ne cite de chemin de fichier interne.** Restent à trancher
avant tout envoi : (3) si le délai de 30 jours
est compatible avec l'échéance PoPETs 2027.3 (30 novembre 2026), (4) si les questions
posées à chaque équipe doivent être reformulées, et (5) — spécifiquement pour Stanford —
si le ton « votre avertissement était exact, voici son ampleur mesurée » est bien respecté
avant envoi, sans aucune formulation qui sonnerait comme un reproche. **Aucun message n'a
été envoyé ni ne sera envoyé sans une décision explicite du responsable.**

**Révision du 12 septembre 2026 — ce qui a changé et pourquoi.** La nuit du 11 au 12
septembre a produit trois corrections à nos propres analyses, dont deux nous sont
défavorables :

1. **Correction d'une correction — pas de renversement.** Un témoin statistique destiné à
   tester si le « couplage » entre fidélité d'imitation et identifiabilité reflète une
   information individuelle (au-delà de la seule exactitude par personne) avait un défaut
   réel : ses cellules *fausses* évitaient la vraie réponse de la personne (`c7_disjoint.py`
   ligne 133), ce qui gonflait sa fuite mesurée d'un facteur **~1,3** (41,2 % de top-1 au
   lieu de 31,6 % une fois les valeurs fausses tirées dans la marginale de population).
   **Corrigé, ce témoin continue de reproduire le couplage** (rho 0,974, 5ᵉ–95ᵉ centiles
   [0,950 ; 0,993], sur les 12 configurations en items entiers — chiffres du manuscrit) et le
   prédicteur réel (rho 0,965) ne le dépasse pas : **la prédiction (b) reste réfutée**,
   comme l'affirmait l'analyse d'origine, et le titre de l'article **ne change pas**. Une
   version intermédiaire de cette correction avait, à tort, cru pouvoir annoncer l'inverse
   (un renversement de la prédiction (b), sur la base de cinq témoins qui, en réalité,
   appariaient l'exactitude contre une cible de substitution et non contre la vérité — ce
   qui détruisait la grandeur même que l'objection dit explicative). Un audit adverse l'a
   démontré et l'auteur l'a concédé sans réserve
   (`resultats/audit-renversement-2026-09-12.md`, `resultats/c7-nul-corrige-reponse-audit.md`
   — le rapport `c7-nul-corrige-resultats.md` porte désormais son propre avertissement de
   rétractation). **Cette annonce de renversement, et le chiffre 0,118–0,206 qui
   l'accompagnait, sont retirés des deux lettres ci-dessous.** Par ailleurs, une formulation
   de notre résumé était fausse et est ici corrigée : ce témoin corrigé **n'est pas
   dépourvu de structure individuelle** — apparié sur l'exactitude, il fuit **31,6 %** de
   top-1, contre 20,7 % (3,55 bits) pour le jumeau réel et 0,049 % pour le hasard pur ; voir
   §1 de la lettre à Twin-2K-500. *(Le couple 31,15 % / 4,63 bits qui figurait ici provient du
   rapport `c7-nul-corrige-resultats.md`, rétracté, et décrit un **autre** témoin — celui à
   cible de substitution. Le témoin dont parle la lettre est le témoin à exactitude-vérité
   appariée, remplissage marginal, mesuré à 31,62 % dans `audit-renversement-2026-09-12.md`
   et publié à 31,6 % par le manuscrit. Ne pas fusionner les deux.)*
2. **Rétractation, pas réduction.** Le témoin « deux organisations indépendantes »
   (top-1 = 1,76 % [0,35 ; 3,63] à n = 142), que nous nous apprêtions à ajouter à la lettre
   Twin-2K-500 comme une **réduction** de la menace précédemment signalée, est lui-même
   invalidé. Un arbitrage indépendant a établi que ce témoin ne prouve rien : les jumeaux
   produits par ce pipeline (B↔C) ne réidentifient la vraie personne qu'au **taux du
   hasard** (0,0 à 0,8 % contre 0,83 % attendu par hasard, même bassin de 120 personnes),
   là où les jumeaux publiés par l'équipe Twin, sur le même bassin, atteignent 20 à 39 %.
   Le dispositif ne transportait **aucune** information individuelle avant toute
   manipulation ; son résultat de 1,76 % ne montre donc pas l'absence d'un canal
   inter-organisations, il montre que ce témoin-là n'a jamais été capable d'en détecter un.
   **Formulation exacte à retenir : la question « deux organisations indépendantes » n'a
   pas été réfutée, elle n'a pas pu être testée — une limite de notre instrument, pas un
   résultat sur le monde.** L'annonce de réduction de menace est retirée de la lettre
   Twin-2K-500 ci-dessous, sans être remplacée par une annonce inverse : nous n'avons aucune
   preuve dans un sens ni dans l'autre, ce scénario est simplement **non mesuré**. Ce qui reste réellement établi y
   est dit à sa place : le canal existe et transporte une information individuelle mesurable
   **en intra-équipe**, sur les jumeaux publiés par l'équipe Twin (36,4 % de top-1, apport
   individuel +17,4 points au-delà du segment démographique, témoin de population pure à
   0,07 %) ; nous ignorons ce qu'il devient entre deux organisations indépendantes.
3. Deux prédictions préenregistrées avaient été comptées comme « réfutées » sur la base
   d'un intervalle de confiance bootstrap dégénéré ([0 % ; 0 %] pour 0 succès sur un petit
   n) : ce sont des artefacts arithmétiques, pas des intervalles de confiance. Corrigées en
   Clopper-Pearson, les deux contiennent le seuil préenregistré : elles sont **non
   concluantes**, pas réfutées. Ceci concerne le compteur de réfutations du manuscrit
   (`article/manuscrit.md` §7.1, hors périmètre d'écriture de cet agent) et deux tests
   internes de méthodologie (test « top-1 > 5 % » avec un modèle fort, test de granularité
   de l'appel) qui ne portent ni sur les données Twin-2K-500 ni sur celles de Park/Stanford
   spécifiquement — nous ne l'avons donc **pas** injecté dans le corps des deux lettres
   (ce n'est pas un fait sur le risque de vie privée de leurs répondants), mais il est
   documenté ici par souci de transparence complète envers le responsable :
   `resultats/c7-a9-correction-2026-09-12.md`.
4. Pour la lettre à Park et Bernstein, ajout de l'explication partielle de l'anomalie
   « Park fuit ~3× moins malgré ~3× plus d'items » : leurs 177 items sont fortement
   redondants (~9,0 items effectivement indépendants contre ~10,1 chez Twin), donc le
   ratio réel est 0,89 et non 2,95 — un résidu d'environ 3× reste inexpliqué, dit sans
   détour.
5. Par souci d'exactitude (chaque chiffre cité doit porter son IC), le chiffre en monde
   ouvert cité à Park/Bernstein est mis à jour avec son intervalle de confiance et
   complété par le résultat, plus robuste, de l'attaquant renforcé
   (`resultats/c7-fort-monde-ouvert-ic-2026-09-12.md`), qui est **supérieur** à ce que la
   lettre annonçait auparavant — cette correction-ci va dans le sens d'une divulgation
   plus complète du risque, pas d'une réduction.

---

## Lettre 1 — Brouillon de courriel aux auteurs de Twin-2K-500 (anglais)

**Subject:** Responsible disclosure — re-identification signal in Twin-2K-500 purchase-intent items, and a correction on our end

**To:** Olivier Toubia <ot2107@gsb.columbia.edu>, Tianyi Peng <tianyi.peng@columbia.edu>

Dear Twin-2K-500 authors,

My name is Amir KELLOU SIDHOUM; I am an independent researcher, with no institutional
affiliation, working on privacy properties of LLM-simulated survey twins.
I am writing to disclose, ahead of any publication, a finding on your publicly released
Twin-2K-500 dataset (CC BY 4.0), and to flag two corrections we made to our own analysis
since we first drafted this note — one of which withdraws a claim we had been about to make
to you, without replacing it with a claim in the opposite direction.

**What we measured, and on what data.** Using only the simulated responses of an LLM twin
conditioned on a persona, and matching them against the real respondents' answers to the
60-item block common to wave 4 (the 40 purchase-intent items together with the 20 opinion
items), we recover the correct respondent among 2,058 candidates in 20.7% of
cases [95% CI 19.0-22.4%], versus 2.13% [1.6-2.8%] for a demographic-only twin and well under
0.3% for standard statistical baselines (e.g. predictive mean matching, 0.23% [0.06-0.42%])
at comparable accuracy. The signal is concentrated in the block of purchase items taken
jointly; opinion items carry no such signal. This assumes an attacker already holds the true
answers to those same items, so it is a linkability finding, not identification from public
information alone.

**A correction we owe you directly — not a reduction in risk.** An earlier draft of this
letter reported a broader test: whether a twin produced by one organization could be linked
to an independently produced twin of the *same* person made by a *different* organization,
using a different model, prompt template, and persona format, and described that scenario as
refuted — a twin-to-twin matching figure of 1.8% [95% CI 0.4-3.6%] at n = 142, which we read
at the time as no better than a demographics-only baseline. An independent check has since
shown that this test could not have detected a link even if one existed. Against the same 120-person pool, the twins
produced by this specific pipeline re-identify the *real* person only at chance rate (0.0-0.8%,
against 0.83% expected by chance), whereas twins your own team has published, on that same
pool, re-identify the real person 20.2-38.9% of the time. The apparatus carried no individual-level
information before any cross-organization manipulation was applied, so its 1.8% result cannot
be read as evidence for or against a cross-organization link — it reflects a generator that was
not, in fact, producing twins recognizable as anyone. We are withdrawing this claim entirely,
not softening it: the cross-organization scenario was not refuted, it was not testable with
this instrument. This is a limitation of our own test, not a finding about the world, and we
did not want to leave you with an inaccurate account of what we know.

To be clear about what we do and do not know: within a single, shared pipeline — both twins
built from the same persona files, as in the headline figure above — the channel is real and
carries measurable individual-level information. On the 60-item common block used for this
comparison, twin-to-twin agreement between strangers is 46.0% [45.9-46.1%]; the
demographic/ideological segment adds only +3.8 points [3.8-3.9]; the specific individual adds a
further +17.4 points [17.2-17.6] beyond that; and a pure-population control (segment mode only,
no individual information) succeeds only 0.07% [0.04-0.11%] of the time, against 36.4% for the
real twin-to-twin match. What we do not know, and are not claiming in either direction, is what
happens to that channel once two organizations build their twins entirely independently — we
currently have no working measurement of that scenario. To be equally direct the other way: we
are not saying the risk has grown, either. We have no evidence in either direction: the scenario
is simply unmeasured, and we will not speculate about its size until we have an instrument
capable of testing it.

**A statistical error we found in our own work, and its correction.** Separately, we ran a
control meant to test whether the rank correlation we observe, across twin configurations,
between simulation fidelity and identifiability reflects something about the specific
individual, rather than being an artifact of comparing two quantities that both simply
track per-person accuracy. We found a real flaw in that control: the cells it filled in as
"wrong" were constructed in a way that avoided the person's own true answer, which inflated
its measured leakage by a factor of about 1.3 (41.2% top-1 instead of 31.6% once wrong
cells are instead drawn from the population marginal for that item). Corrected this way —
per-person accuracy matched exactly to the ground truth, exact-answer positions placed at
random — the control still reproduces the fidelity/leakage coupling we observe (rho = 0.974,
5th-95th percentiles [0.950 ; 0.993], over the 12 configurations measured on whole items),
and our real twins' rho (0.965) does not exceed it. Prediction (b) — that this coupling reflects
something beyond per-person accuracy — therefore remains refuted, exactly as in our
original analysis; nothing here changes that conclusion. We also want to correct, on our
own initiative, an overstatement in an earlier internal summary of this control: it is not
devoid of individual structure, as we had briefly and incorrectly described it — matched to
the same per-person accuracy as our real twins, it identifies the correct respondent 31.6%
of the time, somewhat more than our real twins (20.7%, 3.55 bits of identity) and far above
chance (0.049%). If anything, this makes it a stronger synthetic adversary at matched
accuracy than our own twins, not an inert baseline — which reinforces the refutation above
rather than weakening it.

**What we have not shown.** To be explicit about scope: we have not shown that an attacker
without prior access to a respondent's true answers to these items could identify them from
twin outputs alone; we have not established that twin fidelity causally drives
identifiability (see above); and, as described above, we currently have no working
measurement of the cross-organization scenario at all — the test we ran could not
distinguish a genuine absence of signal from an instrument unable to detect one, so we
cannot bound that particular risk in either direction at this time.

No individual respondent is named, listed, or singled out anywhere in our materials; we
report only aggregate rates across the panel. We are also releasing a measured defense
(within-segment shuffling of purchase responses) that cuts the twin-vs-human rate from
20.7% to 0.13%. The real cost falls entirely on inter-item correlations (4.4 points); two of
the three components (per-item distribution, group differences) are exactly preserved by
construction, so the previously used three-way average (1.47 points) diluted that cost by a
factor of three rather than measuring it. This work is intended as a constructive
contribution, not merely a critique.

**What we are distributing, and what we are not.** To be concrete about our own materials:
we used the wave 1-4 response files and question catalog you released on Hugging Face
(`LLM-Digital-Twin/Twin-2K-500`, CC BY 4.0) to compute the rates above. We do not
redistribute those raw response files, the persona files, or any individual-level record
anywhere in our repository or in the accompanying code artifact. That artifact ships only
code, configuration, and documentation (eleven files); its demonstration runs entirely on
data it generates at runtime, and every table we publish reports rates aggregated by
condition, item, or replicate — never an individual row or identifier.

**Proposed delay and concrete ask.** Before any public posting, we would like you to be able
to check the work yourself. The code is already public and you can open it right now, at
https://github.com/AmirK-S/popsim; we are glad to send you the full report on request, and
are happy to delay or adjust based on your feedback. We propose a 30-day window for your
response, ahead of a submission
deadline we are targeting for November 30, 2026. Concretely, we would welcome: (1) whether
you see any obstacle to us publishing this analysis; (2) whether the twin outputs you
released were generated before or after the dataset's public release; and (3) any comments
on the proposed defense before we finalize it.

Thank you for your time and for releasing this valuable dataset.

Best regards,
Amir KELLOU SIDHOUM
Independent researcher (no institutional affiliation)
aboutdotblank@gmail.com

---

## Lettre 2 — Brouillon de courriel à l'équipe Stanford (Generative Agents, archive des 1 052) (anglais)

**Subject:** Responsible disclosure — measuring the re-identification risk your consent language already flagged

Dear Joon (now at Simile) and Michael,

My name is Amir KELLOU SIDHOUM; I am an independent researcher, with no institutional
affiliation, working on privacy properties of LLM-simulated agents built
from interview data. I am writing to disclose, ahead of any publication, a finding on the
publicly released archive of your 1,052-agent generative-agent study.

**What we measured, and on what data.** Using only the simulated responses of an LLM agent
built from a participant's interview transcript alone, we recover the correct participant
among 1,052 in 44.7% of cases [95% CI 41.8-47.5%]; a composite agent (interview + survey +
demographics) reaches 65.51% [95% CI 62.7-68.3%] under simple nearest-neighbor matching.
Using a strengthened, information-weighted
matching rule (evidence weighted by each item's per-item reliability and rarity, with
parameters estimated out-of-sample across five folds so the rule is never fit on the person
it is tested against), the composite agent's closed-world top-1 rises to 90.40% [95% CI
88.6-92.2%]. We did not re-run that strengthened rule on the interview-only condition, so the
44.7% above should be read as a lower bound. We tested for contamination via a symmetry check
across conditions and found none for the composite agent (details in our full report).

In a more realistic open-world setting, where the true match may be absent from the
candidate pool, at a fixed 1% false-accusation rate our strengthened matching rule recovers
the right participant 60.17% of the time [95% CI 54.5-64.4%] — clearly higher than the 20.39%
[95% CI 15.7-24.5%] we get from simple nearest-neighbor matching at the same false-accusation
rate (the two intervals do not overlap; we want to flag that our earlier estimate used the
simpler rule and understated this). At a stricter 0.1% false-accusation rate the rate is
44.37% [95% CI 23.3-53.8%], but that threshold is set by only about 1 false positive out of
1,052 people, so we consider it unstable and would not want you to anchor on it.

**An open question we investigated and want to share rather than withhold.** We noticed
that your 177-item GSS block, item for item, would suggest roughly 3x more identifying
signal than the 60-item block we use for a comparable twin-to-twin analysis on
Twin-2K-500 — yet the twin-to-twin matching rate we measure on your data (11.9-13.0%) is
about 3x *lower* than the comparable rate on Twin-2K-500 (36.4%). We looked into why, using
only your public human response data (no agent outputs). Redundancy explains the puzzle's
premise, though not the full gap: your 177 items are highly correlated with one another (mean
Cramér's V 0.1055, against 0.0834 for our 60-item Twin block), and once we account for that,
they carry the statistical equivalent of only about 9.0 independent items, against about 10.1
for our block — a real information ratio of 0.89, not the raw 2.95 the item counts alone would
suggest. That is enough to show that more raw items does not mean more identifying information
here. It does not, however, close the gap in observed rates: at this comparable effective
information, the twin-to-twin rate we measure on your data is still roughly 3x lower than on
Twin-2K-500, and we have not been able to test whether that residual comes from the format or length of the
interview transcripts used to build each agent (we do not have access to raw transcripts to
check this locally), or from a difference in the underlying generation pipeline. We wanted
you to have this analysis rather than sit on an open question.

**Framing.** We want to be direct: your supplementary material's Participant Consent section
already warned participants of "a possibility that the information they provide — such as
demographic details, personal history, and political views — may be inadvertently shared,"
and acknowledged that "achieving complete anonymity remains challenging." Your warning was
accurate; what we are providing is a measured estimate of the scale of the risk you already
named — not a claim that you were wrong. We recognize the substantial safeguards you
already put in place: a multi-month IRB review, pseudonymization, restricted access to
individual responses, and a 25-year retention/removal plan.

**What we have not shown.** To be explicit about scope: we have not shown these rates would
hold against a different attacker without access to the specific interview/survey/
demographic fields we used; we have not identified the full explanation for the residual
~3x gap described above; and our open-world estimates at the 0.1% false-accusation
threshold rest on very few absolute false positives and should be treated as unstable.

We are also releasing a measured defense (within-segment response shuffling). What we have
measured of it, we measured on Twin-2K-500, where it cuts the twin-vs-human top-1 rate from
20.7% to 0.13%; we have not run it on your archive, and we are making no claim about what it
would do to the rates above. Its cost is also not small, and should be read component by
component rather than averaged: per-item distributions and between-group differences are
preserved exactly by construction, while inter-item correlations degrade by 4.4 points, and the
gap between the defended twins and the real human correlations widens from 5.775 to 9.709, a
68.1% worsening. We offer it as a constructive, collaborative contribution rather than an
adversarial one.

**What we are distributing, and what we are not.** To be concrete about our own materials:
we used the replication package publicly posted at https://osf.io/t6g7k/ — individual
responses to the GSS, BFI-44, and economic games from your 1,052 participants across waves
1-2, plus the five agent-condition outputs — to compute the rates above. We do not
redistribute any of those raw response files or individual-level records anywhere in our
repository or in the accompanying code artifact, which ships only code, configuration, and
documentation, and whose demonstration runs entirely on data generated at runtime; every
table we publish reports rates aggregated by condition, item, or replicate, never an
individual row or identifier. Separately, we want to flag something we noticed rather than
assume an answer: querying the OSF API for this node returns no declared license
(`node_license: null` as of our check), and the GSS's own terms of use (NORC) prohibit
reproducing GSS content in any form without prior written agreement. We are treating that
as a reason to publish aggregates only and never individual-level responses from this
archive — but since it is your node, we did not want to draw that conclusion on your behalf
without asking: if you read the license status or the GSS terms differently, or if there is
a license we should be citing that the API isn't surfacing, we would welcome your view
before we finalize anything.

**Proposed delay and concrete ask.** Before any public posting, we would like you to be able
to check the work yourself. The code is already public and you can open it right now, at
https://github.com/AmirK-S/popsim; we are glad to send you the full report on request, and
are happy to delay or adjust based on your feedback. We propose a 30-day window for your
response. Concretely, we would
welcome: (1) your view on whether you see any obstacle to us publishing this analysis; (2)
any insight you can share on why the residual ~3x gap above might exist (for instance,
anything about the interview elicitation process that varies systematically from the
survey/demographic fields); and (3) whether you would like to collaborate on reviewing the
methodology or the proposed defense before anything goes public.

Thank you for your time and for this valuable, carefully consented archive.

Best regards,
Amir KELLOU SIDHOUM
Independent researcher (no institutional affiliation)
aboutdotblank@gmail.com

---

*Destinataires et provenance des adresses (12 septembre 2026 ; adresses revérifiées le même
jour sur pages institutionnelles actuelles — voir `resultats/verification-externe-lettres-2026-09-12.md`
pour le détail complet).*

* **Lettre 1, Twin-2K-500.** Ni l'article arXiv 2505.17479 (page de résumé et version HTML),
  ni la fiche Hugging Face `LLM-Digital-Twin/Twin-2K-500`, ni le dépôt de code
  `tianyipeng-lab/Digital-Twin-Simulation` ne publient d'adresse de contact.
  **Olivier Toubia, `ot2107@gsb.columbia.edu`** — **confirmée à jour** : cette adresse figure
  sur sa page facultaire actuelle `https://business.columbia.edu/faculty/people/olivier-toubia`
  (consultée le 12/09/2026, bloc « Contact ») et sur un CV plus récent que celui d'origine
  (`...CV-071524.pdf`, mis à jour 07/15/2024) — l'inquiétude initiale sur un CV vieux de trois
  ans est levée.
  **Tianyi Peng — attention, conflit non résolu.** Le CV (01/12/2025) et sa page personnelle
  (`https://tianyipeng.github.io/`) indiquent tous deux `tianyi.peng@columbia.edu` comme
  contact ; mais sa page facultaire actuelle `https://business.columbia.edu/faculty/people/tianyi-peng`
  (consultée le 12/09/2026, bloc « Contact ») affiche une adresse différente :
  `tp2845@columbia.edu`. Les deux adresses sont columbia.edu et toutes deux plausiblement
  actives (alias personnel choisi par l'intéressé lui-même sur deux sources qu'il contrôle,
  vs adresse d'annuaire institutionnel) ; **cet agent ne tranche pas entre les deux** — la
  lettre garde `tianyi.peng@columbia.edu` (son choix affiché par l'intéressé sur son propre
  CV et son propre site, la source la plus récente et la plus directement auto-déclarée), mais
  le responsable devrait envisager de mettre `tp2845@columbia.edu` en copie, ou vérifier avant
  envoi.
* **Lettre 2, Stanford.** **Michael Bernstein, `msb@cs.stanford.edu`** — confirmée sur sa
  propre page de laboratoire `https://hci.stanford.edu/msb/` (consultée le 12/09/2026).
  **Joon Sung Park — aucune adresse confirmée.** Recherche sur son profil Stanford
  (`https://profiles.stanford.edu/joon-sung-park`, pas d'e-mail affiché), son site personnel
  (`https://www.joonsungpark.com/`, aucun e-mail), son CV personnel (aucun e-mail dans le
  corps du texte), et le site de Simile (`https://simile.ai/` / `simile.com`, page d'accueil
  sans page équipe ni contact visible) : **aucune de ces sources ne publie d'adresse pour
  lui.** La lettre ne lui attribue déjà aucune adresse propre (elle l'adresse par le texte
  « Dear Joon (now at Simile) and Michael » sans ligne **To:** distincte pour lui) — c'est la
  bonne posture, à garder telle quelle plutôt que d'en inventer une ou d'en déduire une du
  domaine simile.ai.
* Pièces jointes : aucune. Les deux lettres renvoient au dépôt public
  `https://github.com/AmirK-S/popsim` et proposent le rapport complet sur demande.
