# R6 — preuve de réconciliation DeepSeek/F1, cellule colhomo

La cellule colhomo/gauche/adversaire a reçu à 00:49:49 un HTTP 429 portant l'identifiant de
génération `gen-1789080588-aqog8HYnALcKxZ8mPlJL`; le runner s'est arrêté sans rejeu. Deux
lectures authentifiées séparées de neuf minutes (12:54 et 13:03) des métadonnées et du contenu
ont retourné 404 chacune. Aucun POST n'a été émis et aucun autre client R6 n'était actif.

Le solde lu aux deux sondes était identique: `total_usage` `149.259209016`, disponible
`5.740790984`. L'attendu est la référence des sondes de 00:39 (`149.257888085`), plus les 82
réconciliations DeepSeek campagne postérieures à la seconde annulation fucitzn (séquence 607),
soit `0.0013209756 USD`, ce qui donne `149.2592090606`. L'écart de `0.0000000446 USD` est
inférieur au seuil de `0.0000001 USD` et ne laisse aucune place à la borne réservée de `0.001 USD`.

La réservation a été annulée (séquence 773) et son marqueur `.en-cours` a été archivé. La cellule
reste absente de la trace principale et devra être rejouée une seule fois; `STOP-R6` est maintenu.
