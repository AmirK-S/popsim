# Préenregistrement — plan factoriel un-facteur-à-la-fois (M / G / P)

> **AVERTISSEMENT (12 septembre 2026) — rien à corriger dans ce texte, mais sa suite est
> invalidée.** Ce fichier est commité avant le premier appel payant (commit `ff90409`) —
> seul cas du dépôt à antériorité prouvée : la discipline annoncée ici a bien été tenue. Ses
> prédictions chiffrées (§4) ont été réfutées par les mesures de
> `resultats/c7-factoriel-resultats.md`, mais ces mesures se révèlent depuis non
> interprétables : le pipeline testé (bras B et ses variantes M/G/P) ne transportait aucune
> information individuelle avant toute manipulation — contre les humains réels, top-1 au
> taux du hasard — voir `resultats/c7-reconciliation-facteurs-2026-09-12.md` §3 et §7. La
> discipline du préenregistrement a donc été respectée, et elle n'a pas suffi : il manquait
> un contrôle de validité du pipeline **avant** ce préenregistrement même, contrôle que la
> réconciliation recommande désormais en §7.

Écrit le 12 septembre 2026, **avant tout appel payant**, avant `analyses/c7_factoriel.py`.
Question ouverte : l'expérience « deux organisations » (`c7-deux-organisations-resultats.md`)
a fait varier **trois facteurs à la fois** — modèle, gabarit de prompt, format de persona —
et a mesuré un effondrement du canal inter-jumeaux (top-1 B↔C = 1,76 % [0,35 ; 3,63] sur
n = 142, sous la baseline démographique 9,2 %). On ignore lequel des trois facteurs porte
ce signal. Ce préenregistrement fixe les prédictions chiffrées et la règle de décision
avant le premier appel.

## 0. Bornes de référence, déjà connues, non recalculées

- **Borne haute (intra-équipe)** : top-1 = **36,4 %** (36,38 % exact), mesuré sur 30 paires
  dirigées entre les 7 configurations riches Twin-2K-500 déjà publiées (même équipe, mêmes
  fichiers de persona sources), cf. `resultats/c7-temoin-prompt-resultats.md`. Chiffre cité
  tel quel, aucun nouvel appel ne le recalcule.
- **Borne basse (tout différent)** : top-1 B↔C = **1,76 % [0,35 ; 3,63]** sur n = 142, cf.
  `resultats/c7-deux-organisations-resultats.md` (organisation B = `deepseek/deepseek-v4-flash`
  + persona JSON + gabarit système/utilisateur « Qxx: n » ; organisation C =
  `qwen/qwen-2.5-72b-instruct` + persona narrative + gabarit une ligne « k) v »). Chiffre
  cité tel quel, aucun nouvel appel ne le recalcule.
- Demographics Only recalculée sur n = 142 dans cette même expérience : top-1 = 9,20 %
  [5,47 ; 13,40].

## 1. Ce qui est repris de `c7_deux_organisations.py`, sans une ligne recopiée

Import direct (aucune redéfinition) : `tirer_echantillon`, `GRAINE` (20260912),
`N_PERSONNES` (200), `charger_labels`, `persona_champs`, `persona_json`, `persona_narrative`,
`blocs_questions`, `SYSTEME_B`, `prompt_b`, `parser_b`, `parser_c`, `construire_banque_items`,
`MODELE_B`, `MODELE_C`, `FOURNISSEUR_B`, `FOURNISSEUR_C`, `MAX_PRICE_B`, `MAX_PRICE_C`,
`MAX_TOKENS_B`, `MAX_TOKENS_C`, `cle_api`, `entetes`, `appeler_chat`, `Arret429`, `Budget`,
`borner_codes`. Depuis `c7_reidentification.py`/`a2_commun.py` (déjà réimportés par
`c7_deux_organisations.py`, donc transitivement identiques) : `items_communs`,
`rangs_attaque`, `rang_dans_segment`, `graine_nom`, `bootstrap_personnes`,
`distance_hamming`, `REF_V4`, `REF_V13`, `DEMO`, `N_BOOTSTRAP`, `N_TIRAGES_LIENS`.

**Les trois déviations déclarées de l'expérience précédente sont conservées à l'identique**
(elles sont héritées automatiquement puisque les fonctions ne sont pas réécrites) :
réponse par NUMÉRO d'option (jamais l'étiquette) ; persona narrative repérée par
identifiant de champ (QID) au fil d'une phrase ; format de sortie C ancré une réponse par
ligne par son numéro brut (jamais la liste unique de nombres, qui dégénère en boucle).

**Échantillon** : le même tirage stratifié `S_gra` de 200 personnes, même graine 20260912,
obtenu en appelant `tirer_echantillon` importé (donc identique bit à bit à celui déjà
utilisé). Les 60 items cibles sont les mêmes (`construire_banque_items`, importé).

**Organisation B recyclée comme bras commun** : `data/traces/c7-deux-organisations.jsonl`
contient déjà 143 réponses B réussies, couverture 100 % (60/60 items) pour les index locaux
0 à 142 de ce même échantillon (vérifié par lecture directe de la trace avant d'écrire ce
fichier). Ces réponses B (modèle `deepseek/deepseek-v4-flash`, gabarit `prompt_b`, persona
JSON) sont **relues depuis la trace existante et réutilisées telles quelles comme un des
deux bras de chacune des trois attaques M/G/P** — aucun nouvel appel B n'est nécessaire, ce
qui réduit le nombre de pipelines à payer de 4 à 3.

## 2. Les trois conditions, une seule chose change par rapport à B

Point de départ commun (bras fixe, gratuit, relu de la trace) : **organisation B** —
`deepseek/deepseek-v4-flash`, persona JSON (`persona_json`), gabarit `prompt_b`
(système + utilisateur, sortie « Qxx: n », `parser_b`).

- **(M) modèle différent, gabarit et persona identiques à B** : rappel de `prompt_b`
  (persona JSON, gabarit système/utilisateur, sortie « Qxx: n », `parser_b`) tel quel, mais
  appelé avec le modèle `qwen/qwen-2.5-72b-instruct` (fournisseur DeepInfra, `MAX_PRICE_C`)
  au lieu de `deepseek/deepseek-v4-flash`. **Aucune nouvelle fonction de gabarit n'est
  écrite pour M** : c'est littéralement `prompt_b` rejoué avec un autre modèle.
- **(G) gabarit différent, modèle et persona identiques à B** : nouvelle fonction
  combinatoire `prompt_g`, qui reprend le style d'instructions et le format de sortie du
  gabarit C (un seul tour utilisateur, sortie une ligne par question « k) numéro »,
  `parser_c`) mais l'applique au dossier JSON (`persona_json`, la même fonction que B,
  jamais `persona_narrative`), appelée avec le modèle `deepseek/deepseek-v4-flash`
  (`MAX_PRICE_B`).
- **(P) format de persona différent, modèle et gabarit identiques à B** : nouvelle fonction
  combinatoire `prompt_p`, qui reprend le gabarit système/utilisateur de B (`SYSTEME_B`,
  sortie « Qxx: n », `parser_b`) mais l'applique à la biographie narrative
  (`persona_narrative`, la même fonction que C, jamais `persona_json`), appelée avec le
  modèle `deepseek/deepseek-v4-flash` (`MAX_PRICE_B`).

Chaque condition est donc une attaque symétrique B↔X (X = M, G ou P), mesurée avec
`rangs_attaque` + `rang_dans_segment` + `bootstrap_personnes` importés tels quels, exactement
comme B↔C dans l'expérience précédente (moyenne des deux sens de l'attaque, IC bootstrap sur
les personnes, 2000 tirages).

## 3. Effectif, choisi pour tenir dans le budget

Coût réel mesuré (pas une estimation) sur les 285 appels de l'expérience précédente,
recalculé par organisation depuis `data/traces/c7-deux-organisations.jsonl` :

- Organisation B (deepseek, persona JSON, 60/60 items lus) : 0,08276 $ / 143 appels =
  **0,000579 $/appel** (entrée moy. 7 632 jetons, sortie moy. 360 jetons).
- Organisation C (qwen/DeepInfra, persona narrative, 60/60 items lus) : 0,47143 $ / 142
  appels = **0,003320 $/appel** (entrée moy. 8 833 jetons, sortie moy. 350 jetons). Ce
  chiffre confirme un prix catalogue réel de 0,36 $/1M entrée, 0,40 $/1M sortie (résout
  exactement 0,0033198 $ pour ces volumes de jetons).

Projection par condition (mêmes prix catalogue, volumes de jetons ajustés au gabarit/persona
effectivement utilisés, marge de sécurité incluse) :

| condition | modèle (prix) | persona (volume d'entrée attendu) | coût/appel projeté (marge incluse) |
|---|---|---|---|
| M | qwen/DeepInfra (0,36 $/0,40 $ par 1M) | JSON, ≈ 7 632 jetons (comme B) | ≈ 0,0035 $ |
| G | deepseek (prix B) | JSON, ≈ 7 632 jetons (comme B) | ≈ 0,0007 $ |
| P | deepseek (prix B) | narrative, ≈ 8 833 jetons (comme C) | ≈ 0,0008 $ |

**Effectif retenu : N = 120 personnes** (sous-ensemble des 143 déjà couvertes par B dans la
trace existante ; mêmes 120 premiers index locaux de l'échantillon stratifié de 200,
mêmes personnes pour les trois conditions). Coût total projeté :
120 × (0,0035 + 0,0007 + 0,0008) ≈ **0,60 $**, sous le plafond dur de 1,00 $, avec une marge
de 0,30 $ avant l'arrêt interne (`ARRET_INTERNE_USD = 0,90 $`, identique à l'expérience
précédente) et 0,40 $ avant le plafond dur. Cette marge tient compte du fait que
l'expérience précédente avait sous-estimé le prix catalogue de C d'environ deux fois avant
mesure réelle ; ici la projection part directement des prix réels mesurés, pas d'un devis a
priori, donc le risque de dépassement est plus faible qu'alors.

**Puissance attendue** : à n = 142, l'IC bootstrap du top-1 B↔C (≈ 1,8 %) avait une
demi-largeur d'environ 1,6 point. À n = 120, avec des taux de top-1 plausiblement plus élevés
(10–30 %, cf. prédictions ci-dessous), la variance de rang est plus grande et l'IC sera
proportionnellement plus large (demi-largeur attendue de l'ordre de 6 à 9 points pour un
top-1 autour de 15–20 %). Cet effectif est **suffisant pour distinguer un effet large** (un
facteur qui restaure, à lui seul, un top-1 net au-dessus de la borne basse [0,35 % ; 3,63 %]
et de 2× la baseline démographique — un écart d'au moins un facteur 3 à 5) mais **insuffisant
pour distinguer des effets modérés et proches entre eux** (par exemple 12 % vs 18 % entre
deux conditions) : si les trois conditions atterrissent dans une fourchette resserrée
(disons 8–20 %), l'expérience ne pourra pas dire lequel des trois facteurs domine, seulement
qu'aucun ne les distingue avec les données récoltées — c'est explicitement couvert par la
règle « rien montré » en section 5. C'est le compromis assumé : tester trois facteurs à un
effectif qui résout un effet large, plutôt que viser une résolution fine hors budget.

## 4. Prédictions chiffrées, écrites avant tout appel

- **(M) modèle différent** : point central top-1 ≈ **0,20** (20 %), intervalle plausible a
  priori [0,08 ; 0,35]. Raisonnement : persona et gabarit strictement identiques à B : seule
  change la capacité du modèle à exploiter un dossier JSON riche pour produire des réponses
  spécifiques à l'individu. Les deux modèles (deepseek-v4-flash, qwen-2.5-72b-instruct) sont
  des LLM instruct de capacité comparable ; j'attends une perte partielle mais pas totale du
  canal.
- **(G) gabarit différent** : point central top-1 ≈ **0,15** (15 %), intervalle plausible
  [0,05 ; 0,30]. Raisonnement : même modèle, même persona JSON ; seule la mise en forme des
  instructions et du format de sortie change. L'information individuelle portée par le
  dossier reste intacte ; je m'attends à une perte modérée, principalement due au changement
  de structure du tour de conversation (système+utilisateur vs utilisateur seul).
- **(P) format de persona différent** : point central top-1 ≈ **0,08** (8 %), intervalle
  plausible [0,02 ; 0,20]. Raisonnement : c'est le changement le plus susceptible de
  dégrader le canal individuel — 494 champs hétérogènes compressés en une seule phrase au
  fil, sans séparation visuelle claire entre champs, contre un objet JSON strictement
  structuré. Je prédis que **c'est ce facteur qui porte l'essentiel de l'effondrement
  observé dans l'expérience « deux organisations »**.

## 5. Règles de décision, fixées avant tout appel

Pour chaque condition X ∈ {M, G, P}, avec IC bootstrap à 95 % [bas_X ; haut_X] sur les
n = 120 (ou moins en cas d'arrêt anticipé) personnes couvertes :

- **X porte le signal (seul)** si bas_X > 3,63 % (borne haute de l'IC de la borne « tout
  différent ») **ET** top1_X ≥ 2 × Demographics Only recalculée sur ce même pool de 120. Les
  deux conditions doivent être remplies : sortir du bruit de la borne basse ne suffit pas
  si le chiffre reste comparable à un devin démographique.
- **Aucun facteur ne porte le signal seul (effet d'interaction)** si, pour les **trois**
  conditions M, G, P, bas_X ≤ 3,63 % **OU** top1_X < 2 × Demographics Only — c'est-à-dire
  qu'aucune des trois ne se distingue individuellement de la borne « tout différent ». Dans
  ce cas, l'effondrement mesuré dans l'expérience « deux organisations » exige la
  combinaison des trois changements ; aucun célibataire n'y suffit.
- **Un facteur domine les deux autres** (sans nécessairement atteindre la borne intra-équipe)
  si une seule condition remplit le critère « porte le signal » ci-dessus alors que les deux
  autres ne le remplissent pas, ou si les IC des trois conditions sont mutuellement disjoints
  avec un ordre nettement tranché.
- **L'expérience n'a rien montré** (résultat nul, à déclarer comme tel, pas maquillé) si les
  IC des trois conditions M, G, P se recouvrent **à la fois** avec l'IC de la borne basse
  [0,35 % ; 3,63 %] **et** avec un chiffre franchement au-dessus de 2× Demographics Only sans
  qu'aucune paire de conditions ne soit statistiquement distinguable l'une de l'autre —
  autrement dit si les trois nuages de confiance se chevauchent tous en un magma indistinct
  qui ne permet ni de dire qu'un facteur domine, ni de dire qu'aucun ne domine avec
  confiance. Dans ce cas le rapport final dira explicitement : « ce plan factoriel, à cet
  effectif, ne distingue pas les trois facteurs » — et ne choisira pas une conclusion parmi
  les trois plus haut par défaut.

Aucun autre seuil n'est ajouté après coup. Le résultat rapporté est celui réellement obtenu,
quel qu'il soit, y compris s'il contredit les prédictions de la section 4.

## 6. Tenue de compte

Plafond strict de la tâche : 1,00 $ USD (déjà partiellement engagé par l'expérience
précédente sur ce même projet, mais cette tâche-ci repart avec son propre plafond dédié tel
que fixé par la mission). Coût projeté ici : ≈ 0,60 $. Arrêt interne du script si le cumul
mesuré (`usage.cost` annoncé par OpenRouter, jamais une estimation) dépasse 0,90 $. Un HTTP
429 porteur d'un identifiant de génération arrête le script immédiatement, sans relance
improvisée ; l'identifiant est rapporté, pas rapproché ici (hors périmètre de cette tâche).

Aucun appel n'a encore eu lieu au moment où ce fichier est écrit et commité.
