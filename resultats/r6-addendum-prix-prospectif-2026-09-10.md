# R6 addendum prospectif de prix avant POST

Ce texte complète les enregistrements OSF `abf7y` et `kmqnw`. Il est écrit avant tout POST
du pilote payant. Il fixe seulement les bornes tarifaires utilisées par les gardes du
client. Il ne modifie aucune question scientifique, hypothèse, invite, cellule, modèle,
ordre de modèle, fournisseur imposé, méthode statistique ou règle de restitution.

Les prix maximaux autorisés pour le pilote sont 0,11 USD par million de jetons en entrée et
0,22 USD par million de jetons en sortie. Avec la borne préexistante de 600 jetons en entrée
et 150 jetons en sortie, le pire coût tarifaire est :

`600 x 0,11 / 1 000 000 + 150 x 0,22 / 1 000 000 = 0,000099 USD par appel`.

Pour vingt appels, la borne tarifaire cumulée est donc 0,00198 USD. Les plafonds
opérationnels déjà annoncés restent plus conservateurs et inchangés : 0,001 USD au maximum
par appel et 0,02 USD au maximum pour les vingt appels du pilote. Le plafond global R6 reste
4,40 USD. La réserve de compte de 1,50 USD reste intacte.

Avant chaque POST, le client vérifie sous verrou le prix du fournisseur imposé, la borne du
dernier appel, le cumul R6, le plafond global et la réserve. Si le prix d'entrée dépasse
0,11 USD par million, si le prix de sortie dépasse 0,22 USD par million, ou si une borne de
coût serait franchie, l'arrêt intervient avant envoi : zéro POST et zéro nouvelle dépense.
Une réponse ambiguë sur le prix, le fournisseur, le coût ou l'identifiant de facturation
bloque également la suite selon les règles déjà déposées.

Ces nombres documentent uniquement un relèvement prospectif des bornes de prix. Ils
n'autorisent aucun appel avant le dépôt de cet addendum et ne changent pas les critères
d'arrêt scientifiques ou techniques de `abf7y` et `kmqnw`.
