# R6 — correction instrumentale et préparation du smoke test

Le client conserve désormais, dans un journal privé et sur liste blanche, les identifiants `X-Generation-Id`, fournisseur et requête présents lors d’une erreur. La capture couvre les erreurs HTTP et les réponses HTTP 200 dont le corps signale une erreur fournisseur. Aucun corps d’erreur, secret ou autre en-tête n’est conservé. L’invite, le plan, le parse, les prix, les limites et la politique de reprise sont inchangés.

La version antérieure est archivée avec SHA-256 `de748231d6e8c3fb038237161ba856809470a74e077f4d399d6683aa08d9e39b`. Les tests factices hors ligne passent intégralement, y compris l’exclusion d’un en-tête `Authorization`.

Le second incident Super est une réponse HTTP 200 portant une erreur fournisseur 502. Il ne contient aucun identifiant exploitable dans les traces antérieures. L’usage de la même clé vaut 0 USD avant la reprise, immédiatement après l’incident et lors du dernier GET en lecture seule. Le delta attribuable à cette clé est donc 0 USD; le coût individuel du 502 reste inconnu. Le marqueur demeure intact et aucun rejeu n’a été effectué.

Le catalogue public courant conserve Gemma et Ultra à prix nul. Gemma utilise actuellement Google AI Studio, statut 0 et disponibilité 30 minutes de 99,28 %. Ultra utilise Nvidia, statut 0 et 96,99 %. Après les deux erreurs fournisseur de Super, Gemma est le smoke test proposé afin de changer de fournisseur. Son ancien pilote à dix 429 reste classé exploratoire.

Commande préparée, non exécutée :

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python analyses/r6_oracle_distant.py \
  --modele google/gemma-4-31b-it:free \
  --plan f1 \
  --liste data/traces/r6-essai-cellules.txt \
  --essai 1 \
  --plafond 0.001 \
  --raisonnement off \
  --pause 3.5 \
  --suffixe r6v2-postosf-smoke-gemma \
  --manifeste-import data/traces/reprise/r6-v2-import-manifeste.json
```
