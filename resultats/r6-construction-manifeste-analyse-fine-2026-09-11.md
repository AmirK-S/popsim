# Construction du manifeste d’analyse fine R6

`analyses/r6_construire_manifeste_analyse_fine.py` reçoit une file `QUEUE_READY`, son
SHA-256, un reçu terminal JSON de `r6_runner_campagnes`, A37 et le référent humain. Il refuse
avant toute lecture ou empreinte de trace lorsque le reçu n’est pas terminal, que le GO
consommé manque, ou que le ledger ne reconstruit pas exactement 894 F1, 316 F2 et 40 plancher
réglés dans l’ordre. Il écrit alors uniquement `refus-construction.jsonl`.

Après cette garde, il vérifie les empreintes des trois traces, construit un manifeste
`R6-analyse-fine-1` à un seul modèle avec chemins absolus et empreintes exactes, puis appelle
le lanceur idempotent. Il ne crée aucune requête, sous-processus, signal, GO ou modification
de file. Les sorties restent séparées par modèle et empreinte source.

Commande, à n’employer seulement après reçu terminal :

```sh
.venv/bin/python analyses/r6_construire_manifeste_analyse_fine.py \
  --queue data/traces/reprise/R6-campagnes-QUEUE_READY-20260910.json \
  --queue-sha256 SHA_QUEUE_READY \
  --recu resultats/r6-campagne-MODELE-recu-terminal.json \
  --orientation resultats/a37-orientation-items.csv \
  --referent data/traces/r1-distributions-reelles.csv
```

Le reçu est désormais écrit par `r6_runner_campagnes` après validation des trois traces et
consommation du GO ; il contient seulement les métadonnées, configurations, chemins et
empreintes requis, jamais les distributions ou contenus bruts.
