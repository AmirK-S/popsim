# R6 — preuve de réconciliation DeepSeek/F1, cellule wlthhsps

La cellule wlthhsps/gauche/adversaire a reçu à 13:56:07 un HTTP 429 portant l'identifiant de
génération `gen-1789127766-JqZluHeJkA0sLSG0Bz5q`; le runner s'est arrêté sans rejeu. Deux
lectures authentifiées séparées de plus de neuf minutes (14:15:22 et 14:24:38) des métadonnées
et du contenu ont retourné 404 chacune. Aucun POST n'a été émis et aucun autre client R6 n'était actif.

Le solde lu aux deux sondes était identique: `total_usage` `149.259526975`, disponible
`5.740473025`. L'attendu est l'ancre des sondes colhomo de 13:03:55 (`149.259209016`), plus les
20 réconciliations DeepSeek campagne postérieures à l'annulation colhomo (séquence 773, jusqu'à
la réservation 814 exclue), soit `0.0003179687 USD`, ce qui donne `149.2595269847`. L'écart de
`0.0000000097 USD` est inférieur au seuil de `0.0000001 USD` et ne laisse aucune place à la borne réservée de `0.001 USD`.

La réservation a été annulée (séquence 815) et son marqueur `.en-cours` a été archivé. La cellule
reste absente de la trace principale et devra être rejouée une seule fois; `STOP-R6` est maintenu.
