# Note pour le responsable du projet (avant toute décision)

Ce brouillon sert à préparer **deux** divulgations responsables — aux auteurs de
Twin-2K-500, et à l'équipe Stanford de l'archive des 1 052 agents génératifs — si et quand
le responsable du projet décide d'en envoyer une. Rien n'est envoyé par cet agent : les
deux textes anglais ci-dessous ne sont que des projets de courriel, à relire, modifier et
signer. Avant tout envoi, le responsable doit trancher, pour chaque lettre : (1) qui signe
et avec quelle adresse, (2) si le code et le rapport (y compris la défense mesurée) sont
réellement prêts à être partagés en pièce jointe ou par lien, (3) si le délai de 30 jours
est compatible avec l'échéance PoPETs 2027.3 (30 novembre 2026), (4) si les questions
posées à chaque équipe doivent être reformulées, et (5) — spécifiquement pour Stanford —
si le ton « votre avertissement était exact, voici son ampleur mesurée » est bien respecté
avant envoi, sans aucune formulation qui sonnerait comme un reproche. **Aucun message n'a
été envoyé ni ne sera envoyé sans une décision explicite du responsable.**

---

## Lettre 1 — Brouillon de courriel aux auteurs de Twin-2K-500 (anglais)

**Subject:** Responsible disclosure — re-identification signal in Twin-2K-500 purchase-intent items

Dear Twin-2K-500 authors,

My name is [Name], a researcher working on privacy properties of LLM-simulated survey twins.
I am writing to disclose, ahead of any publication, a finding on your publicly released
Twin-2K-500 dataset (CC BY 4.0).

Using only the simulated responses of an LLM twin conditioned on a persona, and matching them
against the real respondents' answers to the 40 purchase-intent items, we recover the correct
respondent among 2,058 candidates in about 21% of cases, versus 2.1% for a demographic-only
twin and under 0.3% for standard statistical baselines (PMM, logistic regression) at
comparable accuracy. The signal is concentrated entirely in the block of 40 purchase items
taken jointly; opinion items carry no such signal. This assumes an attacker already holds the
true answers to those same items, so it is a linkability finding, not identification from
public information alone.

No individual respondent is named, listed, or singled out anywhere in our materials; we
report only aggregate rates across the panel. We are also releasing a measured defense
(within-segment shuffling of purchase responses) that cuts this rate from 20.7% to 0.13% at a
cost of only 1.47 points of aggregate utility, so this work is intended as a constructive
contribution, not merely a critique. Before any public posting, we would like to share our
code and full report with you for review and comment, and are happy to delay or adjust based
on your feedback. We propose a 30-day window for your response.

Two questions would help us: (1) were the twin outputs you released generated before or
after the dataset's public release, and (2) do you see any obstacle to us publishing this
analysis?

Thank you for your time and for releasing this valuable dataset.

Best regards,
[Name]

---

## Lettre 2 — Brouillon de courriel à l'équipe Stanford (Generative Agents, archive des 1 052) (anglais)

**Subject:** Responsible disclosure — measuring the re-identification risk your consent language already flagged

Dear Joon (now at Simile) and Michael,

My name is [Name], a researcher working on privacy properties of LLM-simulated agents built
from interview data. I am writing to disclose, ahead of any publication, a finding on the
publicly released archive of your 1,052-agent generative-agent study.

Using only the simulated responses of an LLM agent built from a participant's interview
transcript alone, we recover the correct participant among 1,052 in 44.7% of cases; a
composite agent (interview + survey + demographics) reaches 65.7%. We tested for
contamination via a symmetry check across conditions and found none for the composite agent
(details in our enclosed report). In a more realistic open-world setting, where the true
match may be absent from the candidate pool, the rate is 20.4% at a fixed 1% false-accusation
rate.

We want to be direct about the framing: your supplementary material's Participant Consent
section already warned participants of "a possibility that the information they provide —
such as demographic details, personal history, and political views — may be inadvertently
shared," and acknowledged that "achieving complete anonymity remains challenging." Your
warning was accurate; what we are providing is a measured estimate of the scale of the risk
you already named — not a claim that you were wrong. We recognize the substantial safeguards
you already put in place: a multi-month IRB review, pseudonymization, restricted access to
individual responses, and a 25-year retention/removal plan.

We are also releasing a measured defense (within-segment response shuffling) that sharply
reduces this identification risk at a small utility cost, and we see this as a constructive,
collaborative contribution rather than an adversarial one. Before any public posting, we
would like to share our code and full report with you for review and comment, and are happy
to delay or adjust based on your feedback. We propose a 30-day window for your response.

We would welcome your view on whether you see any obstacle to us publishing this analysis,
and whether you would like to collaborate on reviewing the methodology or the proposed
defense before anything goes public.

Thank you for your time and for this valuable, carefully consented archive.

Best regards,
[Name]

---

*(Champs [Name] à compléter par le responsable ; adresses des destinataires — Joon Sung
Park, Michael Bernstein (msb@cs.stanford.edu) — et pièces jointes non incluses dans ce
brouillon.)*
