# R6 — runner générique des pilotes, préparation locale

Date : 10 septembre 2026. État : **PREPARE_BLOCKED**, `executable=false`.

Cette correction est instrumentale. Elle ne change ni les invites, ni l'ordre des cellules, ni le parse, ni les critères, ni les règles de retrait. Aucun appel modèle, GET authentifié ou GET public n'a été effectué pour cette correction. Le marqueur `data/traces/STOP-R6` est resté présent; aucun `GO-R6` n'a été créé et le STOP global n'a pas été touché.

## Comportement obtenu

`analyses/r6_runner_pilotes.py` charge exclusivement une politique depuis le manifeste readiness dont le SHA-256 est fourni en argument. Une ligne exécutable doit fixer un modèle unique, un fournisseur compatible, les deux prix maximaux, le plafond du modèle, une réservation de 0,001 USD par appel, un plafond pilote de 0,02 USD, `reasoning=off`, `max_tokens=150`, et la liste hashée de dix cellules. Le runner impose deux passes nommées `essai-1` et `essai-2` sur ces dix mêmes cellules.

Chaque cellule conserve une réservation distincte dans le ledger global scellé. Le cumul du pilote est isolé par modèle et reconstruit depuis le journal append-only lors d'une reprise. Les coûts pilote, historiques comme futurs, entrent aussi dans le plafond cumulatif du modèle avec F1, F2 et le plancher, soit la portée complète des 1 270 appels. Une trace déjà écrite n'est pas rachetée. Une réservation ambiguë continue de bloquer tout appel suivant. Le fournisseur est fixé avec `allow_fallbacks=false`, et le fournisseur renvoyé doit être identique.

L'exécution exige un fichier GO JSON propre au modèle, lié au hash exact du manifeste et déclaré `one_shot=true`. Le GO reste en place pendant une interruption et n'est déplacé vers `.consomme` qu'après les vingt cellules complètes et la vérification de l'identité ordonnée des deux passes. DeepSeek, dont le pilote est déjà consommé, est accessible uniquement par `--verifier`: cette branche lit le manifeste et le ledger locaux puis rend son diagnostic avant toute lecture de clé, tout client HTTP et toute vérification de GO. La branche d'exécution DeepSeek est refusée sans condition; elle ne peut donc pas réexécuter le pilote.

Le runner autorise seulement les sept lignes compatibles préparées :

| Modèle | Fournisseur fixé | Plafond modèle USD |
|---|---|---:|
| `mistralai/mistral-small-2603` | Mistral | 0.12 |
| `qwen/qwen3.7-plus` | Alibaba | 0.24 |
| `moonshotai/kimi-k2.5` | SiliconFlow | 0.345 |
| `z-ai/glm-5` | StreamLake | 0.42 |
| `google/gemini-3.8-flash` | Google AI Studio | 0.585 |
| `anthropic/claude-haiku-4.5` | Anthropic | 0.78 |
| `x-ai/grok-4.3` | xAI | 0.825 |

Les quatre lignes incompatibles sont refusées avant lecture de clé ou accès réseau : `meta-llama/llama-4-maverick`, `openai/gpt-5.6-luna`, `openai/gpt-5.4` et `anthropic/claude-sonnet-5`.

## Vérification locale

Le test factice utilise uniquement un serveur HTTP sur `127.0.0.1`, un ledger temporaire et des marqueurs temporaires. Il vérifie les sept politiques autorisées, les quatre refus, le pinning fournisseur, l'identité des dix cellules, le cumul par modèle, le STOP avant requête, la reprise 15+5 sans double achat, le GO consommable une seule fois et le refus d'exécuter DeepSeek déjà engagé. Le cumul factice final est de 0,0020 USD pour vingt réponses de 0,0001 USD; la réservation maximale reste 0,02 USD.

Résultats : 236 contrôles du client R6 passent, le test du runner passe, et les 16 tests de l'évaluateur passent. Le manifeste privé `data/traces/reprise/GO-R6-campagne-PREPARE-20260910.json` est en version `R6-campaign-readiness-PREPARE-4`, reste non exécutable, et référence le ledger et le manifeste d'import canoniques. Les blocages restants sont documentaires ou opérationnels : incompatibilité de quatre fournisseurs, appels gratuits suspendus, absence de GO campagne, présence de STOP-R6 et identité byte-à-byte de l'addendum k5qfh non établie hors ligne.
