# R6 — file de campagnes préparée hors ligne

État: **NO-GO — QUEUE_PREPARED, `executable=false`**. Aucune campagne, lecture authentifiée ou génération n'a été lancée pendant cette préparation. La file dérive du manifeste READY `dc7482c982df7fc80f1fd8298d1421cbe75ac0053dd5a211c2cf43c0b61028fc`. Elle exige une revue Socrates, puis un manifeste `QUEUE_READY` distinct et un GO one-shot distinct pour le seul modèle lancé.

## Ordre et portée

| Priorité | Modèle | Rôle | Fournisseur figé | Plafond modèle, pilote inclus | ETA indicative 1 250 appels |
|---:|---|---|---|---:|---:|
| 1 | `deepseek/deepseek-v4-flash` | descriptif | DigitalOcean | 0,060 USD | 134,3 min |
| 2 | `mistralai/mistral-small-2603` | descriptif | Mistral | 0,120 USD | 13,9 min |
| 3 | `qwen/qwen3.7-plus` | descriptif | Alibaba | 0,240 USD | 20,9 min |
| 4 | `z-ai/glm-5` | descriptif | StreamLake | 0,420 USD | 28,1 min |
| 5 | `anthropic/claude-haiku-4.5` | confirmatoire | Anthropic | 0,780 USD | 18,0 min |
| 6 | `x-ai/grok-4.3` | confirmatoire | xAI | 0,825 USD | 17,0 min |

Les ETA projettent la latence moyenne des 20 appels pilotes sur 1 250 appels. Elles excluent files fournisseur, limitations de débit, incidents et reprises. DeepSeek et Grok portent `non_deterministe=true` et `A4_requires_machine_floor=true`. Grok reste confirmatoire selon la revue; ces marqueurs ne rétrogradent aucune de ses autres analyses.

Chaque lancement mono-modèle enchaîne exactement F1 (894 cellules, `q4`), F2 (316, `q4gab3`) puis le plancher pré-tiré (40, `q4`). Le fournisseur, les prix maximaux, `reasoning=off`, `max_tokens=150`, les bornes de prompt, le plafond unitaire, le plafond modèle, le registre global à 4,40 USD et la réserve compte de 1,50 USD sont inscrits dans le manifeste. Les plafonds modèles totalisent 2,445 USD et incluent les coûts pilotes déjà réglés; le registre de départ totalise 0,0342335066 USD.

Kimi et Gemini sont exclus selon leurs verdicts pilotes. Llama 4 Maverick, GPT-5.6 Luna, GPT-5.4 et Claude Sonnet 5 sont exclus pour incompatibilité de la charge inchangée avec les fournisseurs disponibles du manifeste READY.

## Arrêt, reprise et rapport

`STOP-R6` ou le STOP global utilisateur lu sans modification arrête le modèle entier. Un seuil 429, une cellule non jouée, un plafond atteint ou une réservation ambiguë conserve le GO et impose la reprise exacte. L'identité stable des cellules empêche tout double achat. Le GO n'est consommé qu'après les trois traces complètes et vérifiées. Le runner publie uniquement un rapport agrégé sans réponse brute, donnée personnelle, secret ni identifiant de génération; le rôle propre à chaque modèle est conservé.

Un verrou de file interdit deux campagnes R6 simultanées. Le runner refuse aussi un modèle tant que chaque prédécesseur ne possède pas exactement 1 250 opérations `reglee`, réparties en 894 `campagne/q4`, 316 `campagne/q4gab3` et 40 `plancher/q4`. Pour chaque bloc, la séquence `(camp, identité, item)` du registre doit être exactement celle du plan source; un simple compte ou test d'unicité ne suffit pas. La même comparaison séquentielle valide les traces du modèle courant.

La commande de contrôle, sans réseau, est:

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_runner_campagnes.py \
  --file data/traces/reprise/R6-campagnes-QUEUE_PREPARED-20260910.json \
  --file-sha256 6ac75dd477659c280aed9e3a6a96c265917f29a4397419242a1149e75bde7598 \
  --modele deepseek/deepseek-v4-flash --verifier
```

Le manifeste contient, pour chacun des six modèles, le chemin attendu de son GO et l'argv futur. Il ne contient aucun GO. Le runner refuse ce manifeste préparatoire avant toute lecture de clé ou réseau.

## Vérification locale

Les quatre suites R6 passent, dont le serveur HTTP factice. Le test de campagne utilise un oracle d'ordre, de rôles et de cellules indépendant des constantes du runner. Il couvre le NO-GO, les exclusions, le GO lié au modèle et au hash, STOP-R6, la reprise sans rejeu, le fournisseur figé, le plafond incluant le pilote, ainsi que trois cas adverses à compte constant: permutation de cellules, opération non réglée et mauvaise répartition entre passes.
