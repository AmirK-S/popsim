# R6 — correction instrumentale du préflight financier

## Diagnostic

L’ancienne garde calculait d’abord le budget interne restant, soit le minimum du
plafond global et du solde après réserve. Elle refusait ensuite lorsque
`limit_remaining` était supérieur à ce budget. Cette comparaison inversait le
rôle de la limite de clé : une capacité externe plus élevée devenait un motif
d’échec.

Avec les valeurs de l’incident, le solde après réserve vaut 5,778549 − 1,50 =
4,278549 USD. Sous l’état de clé attendu à 4,40 USD, l’ancienne condition
comparait 4,40 à 4,278549 et s’arrêtait avant même d’évaluer la réservation de
0,001 USD. Elle exigeait donc, dans ce cas, que le compte puisse financer tout
le plafond restant de la clé plutôt que le seul pire appel envisagé.

## Correction

Le préflight calcule maintenant :

`plafond effectif = min(budget global restant, solde − réserve − réservations ambiguës, limit_remaining si fini)`.

Il autorise uniquement lorsque la réservation du pire appel couvre la borne
dérivée des jetons et prix maximaux et reste inférieure ou égale à ce plafond
effectif. Les limites de 4,40 USD globales, 1,50 USD de réserve, 0,001 USD par
appel pilote, 0,02 USD et vingt appels pour le pilote restent inchangées. Une
réservation ambiguë continue de bloquer tout appel suivant.

Chaque préflight transactionnel conserve désormais, dans une trace privée, les
champs non secrets de limite de clé, les composantes global/compte/clé, le
minimum effectif, la borne demandée et une branche stable telle que
`autorise`, `plafond_effectif_insuffisant` ou `reservation_non_reconciliee`.
Aucune clé, aucun en-tête d’autorisation et aucun corps de requête n’y figurent.

## Vérification hors ligne

Les 211 contrôles factices passent. Ils couvrent notamment le cas observé, qui
autorise une réservation de 0,001 USD sous un plafond effectif de 4,278549 USD;
une limite de clé supérieure au budget interne; une clé sans limite finie; et
un plafond effectif de 0,0005 USD, qui produit la branche exacte
`plafond_effectif_insuffisant` avant réservation et avant POST. Aucun réseau
distant, GET authentifié, POST de génération ou `GO-R6` n’a été utilisé.

## Statut d’enregistrement

Cette correction ne change ni hypothèse, ni invite, ni échantillon, ni seuil
scientifique, ni budget autorisé. Elle change toutefois la règle opérationnelle
qui décide si un appel peut partir. D’après la description disponible, `r72pj`
couvre les nouveaux plafonds tarifaires mais pas cette anomalie de préflight,
découverte après son dépôt et après une tentative d’exécution. Un court addendum
OSF prospectif distinct décrivant l’ancienne condition, la formule corrigée et
les tests est recommandé avant un nouveau GO pilote.
