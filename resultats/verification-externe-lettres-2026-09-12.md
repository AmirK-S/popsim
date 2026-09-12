# Vérification externe des deux lettres de divulgation responsable (12 septembre 2026)

Vérification en lecture seule (web + navigateur), sans appel de modèle payant, sans envoi ni
création de compte. Portée : les trois points que la vérification locale ne pouvait pas
trancher — citations du matériel de Park et al., statut de licence OSF / conditions NORC,
adresses des destinataires. Rien d'autre n'a été touché dans les lettres.

## Tâche 1 — Citations du matériel supplémentaire de Park et al. (arXiv 2411.10109)

Source consultée : PDF complet `https://arxiv.org/pdf/2411.10109` (86 pages, texte principal +
matériel supplémentaire dans le même document), section « Participant Consent » (page 3 du
bloc SM, immédiatement après le tableau démographique, avant la section « 2. Creating the AI
Interviewer Agent »). Texte exact de la source :

> "there is still a possibility that the information they provide—such as demographic details,
> personal history, and political views—may be inadvertently shared as researchers use the
> Agent Bank."
>
> "Despite our best efforts, participants are aware of the inherent risks involved in the
> collection of personal information, acknowledging that 'achieving complete anonymity remains
> challenging.'"
>
> "We worked with our Institutional Review Board (IRB) for over six months to ensure that
> participants maintain autonomy and provide informed consent."
>
> "despite efforts to de-identify their data by programmatically replacing all occurrences of
> their names with pseudonyms"
>
> "Requests for data removal will be honored for the first 25 years following the completion of
> the study to the best of our ability."

Verdict par élément :

| Élément cité dans la lettre 2 | Verdict | Détail |
|---|---|---|
| « a possibility that the information they provide — such as demographic details, personal history, and political views — may be inadvertently shared » | **Conforme au mot près** | Correspond exactement à la source, à l'élision de « there is still » en tête (légitime, la citation commence après) et de la fin de phrase « as researchers use the Agent Bank » (élision en fin de citation, marquée par la virgule fermante — n'altère pas le sens). |
| « achieving complete anonymity remains challenging » | **Conforme au mot près** | Citation exacte, y compris les guillemets internes de la source elle-même. |
| Revue éthique de plusieurs mois | **Conforme** | « for over six months » — « multi-month » est une paraphrase fidèle, pas une citation entre guillemets. |
| Pseudonymisation | **Conforme** | « programmatically replacing all occurrences of their names with pseudonyms » — paraphrase fidèle. |
| Accès restreint aux réponses individuelles | **Approximatif** | Aucune phrase de la source ne dit littéralement « accès restreint ». Le texte dit que l'accès aux agents/données est fourni « to the scientific community » et que les données « might become available to other researchers strictly for academic purposes », et ailleurs (hors section consentement) que seules des « aggregated responses » sont en libre accès (voir plus bas, section OSF). C'est cohérent avec « accès restreint », mais c'est une inférence, pas une citation d'un passage qui le dit explicitement — à garder non guillemetée, ce qui est déjà le cas dans la lettre. |
| Plan de rétention et de suppression à 25 ans | **Conforme** | « honored for the first 25 years following the completion of the study » — correspond exactement à « 25-year retention/removal plan ». |

Aucune des deux citations entre guillemets n'a besoin d'être corrigée ou dé-guillemetée : les
deux sont exactes au mot près, à l'élision près en début/fin de citation, ce qui est un usage
normal de la citation partielle.

## Tâche 2 — Licence OSF et conditions NORC

**OSF t6g7k.** Confirmé sur les deux sources :
- API : `https://api.osf.io/v2/nodes/t6g7k/` → `"node_license": null`, relation `license.data:
  null`.
- Page publique : `https://osf.io/t6g7k/` → champ Métadonnées « License : **No License** ».

Les deux sources concordent avec l'affirmation de la lettre : **le dépôt n'a pas de licence
déclarée**. Rien à corriger. Note en passant (hors périmètre des trois points, à ne pas
injecter dans la lettre) : le dépôt ne contient qu'un seul fichier, `replication_instructions.rar`
(3,4 Mo, ajouté le 21/04/2026 par Jonne Kamphorst) — pas de fichiers de réponses individuelles
directement navigables sur la page ; ce fichier n'a pas été téléchargé ni ouvert par cet agent
(hors périmètre, et téléchargement de fichiers tiers non demandé).

**NORC GSS.** Page exacte : `https://gss.norc.org/us/en/gss/terms-and-conditions.html`. Texte
exact : « No part of the contents of NORC websites may be reproduced, stored, or transmitted in
any form or by any means, electronic or mechanical, in whole or in any part, without the
express written consent of NORC. » — correspond en substance à l'affirmation de la lettre
(« prohibit reproducing GSS content in any form without prior written agreement »). Les deux
formulations ne sont pas mot pour mot identiques (« express written consent » vs « prior written
agreement ») mais disent la même chose ; comme ce n'est pas mis entre guillemets dans la
lettre, aucune correction n'est nécessaire.

## Tâche 3 — Adresses des destinataires

| Personne | Adresse dans la lettre | Verdict | Source de vérification |
|---|---|---|---|
| Olivier Toubia | `ot2107@gsb.columbia.edu` | **Confirmée, à jour** | Page facultaire actuelle `https://business.columbia.edu/faculty/people/olivier-toubia` (consultée 12/09/2026, bloc Contact) ; également présente sur un CV plus récent que celui cité (`Toubia,%20Olivier%20-%20CV-071524.pdf`, màj 07/15/2024). Le doute initial (CV de 2023) est levé. |
| Tianyi Peng | `tianyi.peng@columbia.edu` | **Confirmée par deux sources auto-déclarées, mais en conflit avec l'annuaire institutionnel** | CV (01/12/2025) et page personnelle `https://tianyipeng.github.io/` indiquent tous deux cette adresse. Mais la page facultaire actuelle `https://business.columbia.edu/faculty/people/tianyi-peng` (consultée 12/09/2026) affiche **`tp2845@columbia.edu`**, une adresse différente. Les deux sont plausibles (alias personnel vs adresse d'annuaire) ; non tranché — voir note dans le brouillon. |
| Michael Bernstein | `msb@cs.stanford.edu` | **Confirmée** | Page de laboratoire personnelle `https://hci.stanford.edu/msb/` (consultée 12/09/2026). Le profil Stanford officiel (`profiles.stanford.edu`) n'affiche pas d'adresse (politique de confidentialité de l'annuaire), mais ne contredit pas cette adresse. |
| Joon Sung Park | *(aucune adresse utilisée dans la lettre)* | **Introuvable** | Vérifié sans succès sur : profil Stanford (`profiles.stanford.edu/joon-sung-park`, aucun e-mail affiché, indique désormais « Affiliate »), site personnel `joonsungpark.com` (aucun e-mail), CV personnel PDF (aucun e-mail dans le texte), site de Simile (`simile.ai` / `simile.com`, page d'accueil sans page équipe ni contact visible). La lettre ne lui attribue déjà aucune adresse — c'est la bonne posture, à conserver. |

## Corrections apportées

Dans `resultats/divulgation-responsable-brouillon.md`, seule la note de bas de page
« Destinataires et provenance des adresses » a été mise à jour (aucune autre partie des deux
lettres n'a été touchée) :
- Toubia : le doute sur le CV de 2023 est levé (confirmation sur page facultaire actuelle +
  CV 2024).
- Peng : ajout du conflit d'adresse découvert (`tianyi.peng@columbia.edu` vs
  `tp2845@columbia.edu`), avec recommandation de mise en copie ou de vérification avant envoi
  plutôt qu'un arbitrage silencieux.
- Bernstein : confirmation sourcée (page de laboratoire).
- Joon Sung Park : la lettre ne cite déjà aucune adresse pour lui ; ce constat (aucune adresse
  trouvée nulle part) est maintenant documenté explicitement plutôt que laissé comme
  « non revérifiée ».

Aucune citation, aucun chiffre, aucune formulation liée à la licence OSF ou aux conditions NORC
n'a été modifié dans le corps des lettres : les deux citations de Park et al. sont exactes, et
les affirmations sur OSF/NORC sont confirmées exactes en substance.

## Verdict

**Les deux lettres sont prêtes à partir sur ces trois points**, sous une réserve unique et
mineure : l'adresse de Tianyi Peng a une variante concurrente (`tp2845@columbia.edu`) que le
responsable peut vouloir mettre en copie par prudence avant l'envoi ; et Joon Sung Park reste
sans adresse directe vérifiable (déjà correctement non adressé dans le brouillon). Aucun des
deux points ne bloque l'envoi ; ce sont des affinages, pas des erreurs.
