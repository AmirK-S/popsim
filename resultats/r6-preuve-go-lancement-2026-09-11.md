# Preuve GO-LANCEMENT R6

Date: 2026-09-11

Verdict: **GO-LANCEMENT** pour le gate de lancement R6, sous les verrous ci-dessous.

- Diff récursif READY contre PREPARED: exactement `state QUEUE_PREPARED -> QUEUE_READY` et `executable false -> true`.
- READY: `data/traces/reprise/R6-campagnes-QUEUE_READY-20260910.json`, SHA-256 `115e1b2e15b115f5926c70d47bef8a45ac46fb65315ec9f2bf7b014d14eb36e4`, permissions `0600`.
- PREPARED: SHA-256 `6ac75dd477659c280aed9e3a6a96c265917f29a4397419242a1149e75bde7598`, permissions `0600`.
- La preuve GO de préparation est conservée: `resultats/r6-preuve-go-queue-2026-09-10.md`, SHA-256 `11281eec5aec425128ebc87707d33882c85875ebe2ca8185311f8339e2714722`.
- `--verifier` du runner a passé pour les six modèles avec le chemin et le SHA READY exacts. Les sorties sont `state=QUEUE_READY`, `mode=verification-hors-reseau`, sans appel de modèle.
- `data/traces/STOP-R6` est présent; `data/traces/GO-R6` et les GO de campagne sont absents. Aucun GO modèle n’est créé par cette preuve.
- Ledger inchangé: `data/traces/reprise/r6-v2-registre-global.jsonl`, SHA-256 `197f79cb8bf8bc47ba228e652ce63a7edbb0c177dfbefa04496562a7a75a23cb`.

Ce verdict autorise le gate de lancement. Toute exécution reste conditionnée au GO individuel du modèle et à la règle STOP-R6 du runner.
