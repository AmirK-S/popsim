# R6 — preuve locale de QUEUE_READY

Source immuable: `data/traces/reprise/R6-campagnes-QUEUE_PREPARED-20260910.json`, SHA-256 `6ac75dd477659c280aed9e3a6a96c265917f29a4397419242a1149e75bde7598`.

Fichier dérivé: `data/traces/reprise/R6-campagnes-QUEUE_READY-20260910.json`, SHA-256 `115e1b2e15b115f5926c70d47bef8a45ac46fb65315ec9f2bf7b014d14eb36e4`.

Le diff JSON complet ne contient que deux changements de premier niveau:

- `state`: `QUEUE_PREPARED` → `QUEUE_READY`;
- `executable`: `false` → `true`.

Le manifeste est JSON valide et reste privé (`0600`). Aucun GO mono-modèle ni `data/traces/GO-R6` n'existe. `data/traces/STOP-R6` demeure présent, SHA-256 `20078c67237a96d084354bda917a09d48bed219a9c8e416a5e2313dde6cbc707`. Aucun appel réseau n'a été effectué.
