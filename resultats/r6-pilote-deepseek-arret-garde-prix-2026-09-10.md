# R6 — pilote DeepSeek arrêté par la garde de prix

Le GO reçu le 10 septembre 2026 après le dépôt de l’addendum Euler sur OSF
(`https://osf.io/kmqnw/overview`, enregistrement indiqué à 21:34 CEST, statut
« Pending approval ») autorisait uniquement le pilote
`deepseek/deepseek-v4-flash` chez DigitalOcean, en deux passes de dix appels. Il
n’autorisait aucune campagne.

Le lanceur a d’abord validé les 208 contrôles factices locaux, l’intégrité du
client, de la liste, du manifeste, du plan et du registre, ainsi que l’absence
de processus R6 et de marqueur d’arrêt. Il a ensuite effectué l’unique lecture
fraîche du catalogue autorisée avant génération.

Cette lecture a donné 0,08554 USD par million de jetons d’entrée et 0,17108 USD
par million de jetons de sortie pour le modèle fixé. Ces deux prix dépassent les
bornes enregistrées dans le client, respectivement 0,0679 et 0,168 USD par
million. La garde de prix a donc arrêté le pilote immédiatement.

Aucune lecture de solde n’a suivi, puisque la première garde distante avait déjà
échoué. Aucun POST de génération n’a été envoyé. Il n’existe donc aucune réponse,
aucun identifiant de génération, aucun incident fournisseur, aucune mesure de
parse, de raisonnement ou de déterminisme à agréger. Le coût attribuable à ce
essai est de 0 USD, établi ici par l’absence de POST. Le solde du compte n’a pas
été observé pendant cette tentative.

Le registre global est inchangé avant et après l’arrêt. Aucun fichier de trace
DeepSeek ni marqueur d’appel en cours n’a été créé. Aucun `STOP` global n’a été
touché et aucun `STOP-R6` n’a été nécessaire. Le GO a été archivé comme consommé
après l’échec de garde afin d’empêcher une relance accidentelle. Aucune campagne
n’a commencé.
