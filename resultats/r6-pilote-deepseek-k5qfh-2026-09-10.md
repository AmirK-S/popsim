# R6 — pilote DeepSeek enregistré sous k5qfh

La troisième tentative a été exécutée après le GO lié à l’enregistrement final archivé
`https://osf.io/k5qfh/overview`, indiqué « Pending approval ». Le périmètre était limité au
pilote `deepseek/deepseek-v4-flash`, fournisseur DigitalOcean sans repli, deux passes des
mêmes dix cellules et aucune campagne.

Les 220 contrôles factices ont passé avant le réseau. Le catalogue frais a confirmé des
prix de 0,08554 USD/M en entrée et 0,17108 USD/M en sortie, sous les plafonds 0,11/0,22.
Les vingt préflights ont accepté une clé finie plafonnée à 4,40 USD, avec
`limit_reset = null`; le plus petit plafond effectif observé était 4,278304231 USD, très
supérieur à la réservation unitaire de 0,001 USD. La réserve de compte de 1,50 USD et le
plafond global de 4,40 USD ont donc été préservés.

Chaque passe a produit dix réponses sur dix, sans cellule non jouée, incident de transport
ou rejet de parse. DigitalOcean est le fournisseur effectif des vingt réponses et le modèle
renvoyé est celui demandé. Le raisonnement facturé est nul sur les vingt réponses. Les
latences médianes sont de 7 195,7 ms puis 6 468,6 ms.

Les vingt POST ont vingt identifiants uniques. Le registre contient vingt réservations et
vingt rapprochements portant exactement ces identifiants. Les réservations au pire cas
totalisent 0,020 USD; le coût annoncé, tracé et réconcilié est 0,0001644783 USD par passe,
soit 0,0003289566 USD au total. La projection sur 1 270 cellules est 0,020888744 USD.

Les deux passes portent les mêmes dix cellules, mais une seule distribution sur dix est
strictement identique entre les deux passages. Le critère de répétabilité exige au moins
sept distributions identiques sur dix : il échoue. Le verdict pilote est donc négatif,
malgré le passage des critères de coût, transport, parse et raisonnement.

Le GO a été archivé comme consommé. Aucun `STOP` global n’a été touché, aucun `STOP-R6`
n’a été nécessaire et aucune campagne n’a été lancée. Les sorties textuelles brutes et les
identifiants individuels restent dans les traces privées.
