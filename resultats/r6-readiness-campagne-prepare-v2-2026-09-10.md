# R6 — préparation de campagne, garde modèle et fournisseurs publics

## État

**PREPARE_BLOCKED.** Aucun appel de génération n’a été envoyé. `STOP-R6` est resté présent,
`GO-R6` absent et le manifeste privé reste explicitement non exécutable. La phase a produit
une correction instrumentale du budget, un inventaire public sans clé des endpoints et un
plan de pilotes. Quatre modèles n’ont aucun endpoint compatible avec la charge inchangée;
le client ne sait pas encore exécuter les pilotes génériques. Ces deux divergences bloquent
la readiness.

## Garde cumulative par modèle

Le client exige désormais `--plafond-modele` pour les passes `campagne` et `plancher`.
Sous le même verrou exclusif que le registre global, il :

1. reconstruit depuis les réservations du ledger le plafond déjà utilisé pour le modèle;
2. additionne les coûts réglés et les réservations F1, F2 et plancher de ce modèle;
3. refuse une borne absente, non finie, nulle, supérieure à 4,40 USD ou différente de la
   borne déjà enregistrée;
4. refuse avant création du marqueur et avant POST si `total_modèle + réservation` dépasse
   le plafond;
5. inscrit la borne dans chaque réservation avant l’envoi, afin qu’une reprise la retrouve.

Le plafond global de 4,40 USD, la réserve de 1,50 USD, le blocage de toute réservation
ambiguë et l’unicité de cellule restent inchangés. Le registre réel contient 0,0003289566
USD réglés et zéro réservation ambiguë, donc le maximum global encore engageable est
4,3996710434 USD, sous réserve du solde et de la limite de clé frais au moment d’un futur GO.

Les tests adverses couvrent deux processus concurrents sur le verrou, la reconstruction
après fermeture/réouverture, le dépassement réparti entre F1 et plancher, le changement de
plafond à la reprise, `NaN`, la double réservation et le refus avant POST lorsque le plafond
est plein.

La correction est instrumentale : elle ne modifie ni invite, ni cellule, ni parse, ni
paramètre de génération. Le client passe du SHA-256 gelé avant correction `b29f93da…` à
`b8371d8e…`; les tests passent de `6fea6468…` à `c5222532…`.

## Inventaire public des fournisseurs

Seuls les endpoints publics
`https://openrouter.ai/api/v1/models/<modèle>/endpoints` ont été lus, sans clé ni en-tête
d’autorisation. Il y a eu 17 GET publics : un premier chemin canonique périmé a répondu 404,
un GET diagnostic DeepSeek a réussi, puis les 15 modèles ont été inventoriés avec succès.
Il n’y a eu aucun GET authentifié et aucun POST.

La proposition retient un endpoint de statut 0 qui supporte simultanément `temperature`,
`max_tokens`, `reasoning` et `include_reasoning`, avec contexte suffisant et au moins 150
jetons de sortie. DeepSeek reste chez DigitalOcean conformément au pilote. Pour les autres,
le coût maximal d’une charge de 1 000 jetons d’entrée et 150 de sortie est minimisé; en cas
d’égalité, le fournisseur de l’éditeur est préféré, puis l’uptime public et le nom. Le
fournisseur est fixé sans repli et les prix observés deviennent des plafonds de routage.

| ordre | modèle | endpoints | fournisseur proposé | prix entrée/sortie USD/M | verdict |
|---:|---|---:|---|---:|---|
| 0a | Gemma 4 31B `:free` | 1 | Google AI Studio | 0 / 0 | compatible, appels gratuits suspendus |
| 0b | Nemotron Super `:free` | 1 | Nvidia | 0 / 0 | compatible, appels gratuits suspendus |
| 0c | Nemotron Ultra `:free` | 1 | Nvidia | 0 / 0 | compatible, appels gratuits suspendus |
| 1 | DeepSeek V4 Flash | 15 | DigitalOcean | 0,0679 / 0,168 | figé par le pilote |
| 2 | Mistral Small 2603 | 4 | Mistral (`mistral/zdr`) | 0,15 / 0,60 | compatible |
| 3 | Llama 4 Maverick | 5 | aucun | — | tous omettent reasoning/include_reasoning |
| 4 | Qwen 3.7 Plus | 1 | Alibaba | 0,32 / 1,28 | compatible |
| 5 | Kimi K2.5 | 6 | SiliconFlow INT4 | 0,45 / 2,25 | compatible |
| 6 | GLM-5 | 8 | StreamLake FP8 | 0,60 / 1,92 | compatible |
| 7 | GPT-5.6 Luna | 7 | aucun | — | tous omettent temperature |
| 8 | Gemini 3.8 Flash | 6 | Google AI Studio (`flex`) | 0,375 / 1,875 | compatible |
| 9 | Claude Haiku 4.5 | 8 | Anthropic | 1,00 / 5,00 | compatible |
| 10 | Grok 4.3 | 4 | xAI | 1,25 / 2,50 | compatible |
| 11 | GPT-5.4 | 7 | aucun | — | tous omettent temperature |
| 12 | Claude Sonnet 5, conditionnel | 9 | aucun | — | tous omettent temperature |

Le client envoie toujours `temperature=0.0` et `reasoning={enabled:false, exclude:true}`.
Retirer l’un de ces champs pour rendre un endpoint éligible changerait la charge. La
readiness conserve donc ces quatre modèles comme bloqués au lieu de supposer que le routeur
ignore ou transforme un paramètre non annoncé.

Le snapshot privé complet est
`data/traces/reprise/r6-endpoints-publics-20260910.json`, SHA-256
`ea1313cfef2a363fb7af094e61272db68a16c379aec1f34fc1ab9b9bd1e9bb77`.

## Pilotes préparés

Tous les pilotes gardent les mêmes dix cellules scellées, SHA-256
`0898b5e171e0825a3784a058c1dd490c22d73ff00f4dd3505bb80f3ff69710c5`, deux passes
`essai-1` et `essai-2`, température 0, `max_tokens=150`, raisonnement désactivé, fournisseur
unique et aucun repli. Les bornes ci-dessous couvrent 600 jetons d’entrée et 150 de sortie;
le plafond pilote vaut vingt fois la réservation unitaire.

| modèle restant compatible | fournisseur | borne dérivée/appel | réservation/appel | plafond 20 appels |
|---|---|---:|---:|---:|
| Mistral Small 2603 | Mistral | 0,00018000 | 0,001 | 0,02 |
| Qwen 3.7 Plus | Alibaba | 0,00038400 | 0,001 | 0,02 |
| Kimi K2.5 | SiliconFlow | 0,00060750 | 0,001 | 0,02 |
| GLM-5 | StreamLake | 0,00064800 | 0,001 | 0,02 |
| Gemini 3.8 Flash | Google AI Studio | 0,00050625 | 0,001 | 0,02 |
| Claude Haiku 4.5 | Anthropic | 0,00135000 | 0,002 | 0,04 |
| Grok 4.3 | xAI | 0,00112500 | 0,002 | 0,04 |

Les tableaux d’arguments exacts des deux passes de chaque modèle sont dans le manifeste
privé. Ils restent non exécutables : la garde pilote actuelle impose encore
DeepSeek/DigitalOcean et compte globalement les vingt appels DeepSeek déjà consommés. Elle
doit devenir une garde par modèle avant qu’un autre pilote puisse partir. Les quatre modèles
sans endpoint compatible n’ont volontairement aucune commande.

Pour la campagne DeepSeek déjà pilotée, les commandes préparées antérieurement doivent
désormais ajouter `--plafond-modele 0.06`; la garde nouvelle partage alors cette borne entre
F1, F2 et plancher. Aucun autre paramètre scientifique ne change.

## Vérification et blocages restants

`analyses/test_r6_client.py` passe **231 contrôles** et `analyses/test_r6_evaluer.py` passe
**16 tests**. La compilation Python et `git diff --check` passent également.

La readiness reste bloquée par :

- l’incompatibilité documentée de la charge inchangée pour Maverick, Luna, GPT-5.4 et
  Sonnet 5;
- la garde pilote codée uniquement pour DeepSeek, alors que sept autres payants compatibles
  exigent leur propre pilote;
- la suspension persistante des nouveaux appels gratuits;
- l’absence de GO de campagne et la présence intentionnelle de `STOP-R6`;
- la divergence déjà signalée entre le hash local actuel de l’addendum préflight et le hash
  inscrit dans le gel `k5qfh`.

Le manifeste `GO-R6-campagne-PREPARE-20260910.json` ne doit pas être renommé, copié ou
interprété comme `data/traces/GO-R6`.
