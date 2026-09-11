# Note pour le responsable du projet (avant toute décision)

Ce brouillon sert à préparer une divulgation responsable aux auteurs de Twin-2K-500, si et
quand le responsable du projet décide d'en envoyer une. Rien n'est envoyé par cet agent : le
texte anglais ci-dessous n'est qu'un projet de courriel, à relire, modifier et signer.
Avant tout envoi, le responsable doit trancher : (1) qui signe et avec quelle adresse, (2) si
le code et le rapport complet sont réellement prêts à être partagés en pièce jointe ou par
lien, (3) si le délai de 30 jours est compatible avec l'échéance PoPETs 2027.3 (30 novembre
2026), et (4) si les deux questions posées aux auteurs (antériorité des jumeaux publiés,
obstacle perçu à la publication) doivent être reformulées. **Aucun message n'a été envoyé ni
ne sera envoyé sans une décision explicite du responsable.**

---

## Brouillon de courriel (anglais, à l'attention des auteurs de Twin-2K-500)

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
report only aggregate rates across the panel. Before any public posting, we would like to
share our code and full report with you for review and comment, and are happy to delay or
adjust based on your feedback. We propose a 30-day window for your response.

Two questions would help us: (1) were the twin outputs you released generated before or
after the dataset's public release, and (2) do you see any obstacle to us publishing this
analysis?

Thank you for your time and for releasing this valuable dataset.

Best regards,
[Name]

---

*(~235 mots hors objet et formules de politesse. Champs [Name] à compléter par le
responsable ; adresse des destinataires et pièces jointes non incluses dans ce brouillon.)*
