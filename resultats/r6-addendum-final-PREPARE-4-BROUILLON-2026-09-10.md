# R6 — addendum technique PREPARE-4

**BROUILLON LOCAL POUR REVUE EULER — non final, non déposé, non exécutable.**

Ce texte documente des corrections instrumentales préparées après le pilote DeepSeek déjà réalisé et avant tout pilote des autres modèles ou toute campagne correspondante. Il ne doit pas être présenté comme antérieur au pilote DeepSeek. Le manifeste local est désormais `R6-campaign-readiness-PREPARE-4`. Son SHA-256 final sera ajouté après revue Euler; aucune empreinte d'une version précédente n'est présentée comme celle de PREPARE-4. Il reste `PREPARE_BLOCKED`, avec `executable=false`; `STOP-R6` reste présent et aucun GO campagne n’existe.

## Corrections instrumentales

Le client R6 conserve désormais dans un journal privé les seuls identifiants techniques non secrets utiles au rapprochement d’une erreur lorsqu’ils sont disponibles: identifiant de génération, fournisseur et identifiant de requête. La journalisation distingue les incidents de transport, les réservations non réconciliées et les réponses effectivement facturées. Elle n’enregistre ni clé, ni en-tête d’autorisation, ni réponse brute. Cette correction améliore la preuve de reprise et de coût; elle ne transforme pas un coût absent en coût nul et ne modifie aucune observation scientifique.

Un plafond cumulatif par modèle est appliqué atomiquement sous le verrou du ledger global aux vingt appels pilote, aux 1 210 cellules F1/F2 et aux 40 cellules du plancher machine, soit les 1 270 appels de la portée enregistrée. Les coûts pilote historiques déjà réconciliés sont comptés sans réécriture du ledger; toute future réservation pilote porte aussi le plafond du modèle. Le cumul est reconstruit depuis les événements persistés lors d’une reprise et refuse un changement de plafond. Il s’ajoute au plafond global R6 de 4,40 USD, à la réserve de compte de 1,50 USD, à la limite finie et non renouvelable de la clé, aux prix maximaux du fournisseur et aux réservations ambiguës déjà retenues. Il ne réalloue aucun budget entre modèles.

Le runner de pilote `analyses/r6_runner_pilotes.py` lit exclusivement le modèle, le fournisseur fixé, les prix maximaux, le plafond du modèle et la liste de cellules dans le manifeste dont l’empreinte lui est fournie. Pour chaque modèle, il impose deux passes distinctes de dix appels sur les dix mêmes cellules ordonnées, `reasoning=off` et `max_tokens=150`. Les plafonds validés sont: 0,001 USD par appel et 0,02 USD par pilote pour Mistral, Qwen, Kimi, GLM et Gemini; 0,002 USD par appel et 0,04 USD par pilote pour Haiku et Grok; 0,001 USD par appel et 0,02 USD pour DeepSeek déjà consommé, accessible en vérification locale seulement. Le fournisseur est épinglé avec repli interdit. Chaque cellule a une identité et une réservation séparées dans le ledger; une reprise saute les cellules déjà acquises et une réservation ambiguë bloque l’appel suivant. Un GO à usage unique doit nommer exactement le modèle et le hash du manifeste. Il n’est consommé qu’après vingt cellules complètes. Pour DeepSeek déjà consommé, `--verifier` lit uniquement le manifeste signé et le ledger local et retourne avant toute lecture de clé ou création de client HTTP. Toute branche d’exécution DeepSeek est refusée, même en présence d’un GO; aucune réexécution n’est possible.

Les sept couples actuellement compatibles avec la charge inchangée sont: Mistral Small 2603/Mistral, Qwen 3.7 Plus/Alibaba, Kimi K2.5/SiliconFlow, GLM-5/StreamLake, Gemini 3.8 Flash/Google AI Studio, Claude Haiku 4.5/Anthropic et Grok 4.3/xAI. Les quatre lignes incompatibles sont refusées avant lecture de clé ou requête: Llama 4 Maverick, GPT-5.6 Luna, GPT-5.4 et Claude Sonnet 5. Cette classification vient du snapshot public local déjà constitué; elle ne vaut pas nouvelle collecte au moment de ce brouillon.

| Modèle | Prix entrée USD/M | Prix sortie USD/M | Plafond modèle USD |
|---|---:|---:|---:|
| DeepSeek V4 Flash | 0,0679 | 0,168 | 0,06 |
| Mistral Small 2603 | 0,15 | 0,60 | 0,12 |
| Qwen 3.7 Plus | 0,32 | 1,28 | 0,24 |
| Kimi K2.5 | 0,45 | 2,25 | 0,345 |
| GLM-5 | 0,60 | 1,92 | 0,42 |
| Gemini 3.8 Flash | 0,375 | 1,875 | 0,585 |
| Claude Haiku 4.5 | 1 | 5 | 0,78 |
| Grok 4.3 | 1,25 | 2,50 | 0,825 |

## Vérification et portée scientifique

Les 236 contrôles factices du client passent. Ils couvrent notamment l'inclusion d'un pilote futur et d'un pilote historique dans le plafond modèle, la reprise du cumul et le refus du dépassement. Le test local du runner couvre les sept lignes compatibles, le refus des quatre autres, l’identité ordonnée des dix cellules entre passes, le fournisseur fixé, la reprise sans double achat, le coût cumulatif, STOP avant requête, le GO à usage unique et la vérification DeepSeek strictement locale. Les 16 tests de l’évaluateur passent également. Ces vérifications utilisent des mocks et un serveur loopback; elles ne constituent pas des appels aux modèles.

Ces changements n’altèrent aucune hypothèse, famille de tests, estimand, invite, cellule, ordre, parse, critère de retrait ou règle d’inférence fixés dans le plan et ses addenda substantifs. Ils rendent seulement les gardes financières et la reprise applicables aux modèles compatibles restants. La campagne demeure bloquée jusqu’à revue Euler, décision documentaire explicite et GO ultérieur distinct.

Empreintes locales associées: client `919ca5f4a3ce61033d7aac6bf65fce330ee1b2c795fb4a76bad6cfb7703a4131`; runner `3f85555931ccc7b6add91cb96571f546c25c1b1c8e7e538a253a5d4737a9cf4c`; tests client `794b1687382e78f48dcbd035720b7a19c8013e57b3a046ac3045849250c9b397`; tests runner `a6ca5665f2917c8dff8cded19c96d5105d390179a59f1bffc9714d9d8df70ed1`. Le registre global local a l’empreinte `80c7d904f3a448e2000e5f24a016bf05306639faeb0530a4b6ed392405de2ffe`; il n’a pas été réécrit par cette correction. L’identité octet pour octet entre l’addendum local de préflight et le texte archivé sous `k5qfh` n’est pas établie hors ligne; aucune équivalence exacte n’est revendiquée ici.
