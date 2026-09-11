# R6 — seconde tentative pilote arrêtée au préflight

Le GO reçu après le dépôt de l’addendum tarifaire prospectif sur OSF
(`https://osf.io/r72pj/overview`, enregistrement indiqué à 21:43 CEST, statut
« Pending approval ») autorisait uniquement deux passes de dix appels de
`deepseek/deepseek-v4-flash` chez DigitalOcean. Les limites étaient de vingt
POST et 0,02 USD pour le pilote, 0,001 USD par appel, 4,40 USD au registre
global et une réserve de compte de 1,50 USD. Aucune campagne n’était autorisée.

Les 208 contrôles factices locaux ont passé. Le catalogue frais a confirmé le
modèle à 0,08554 USD par million de jetons d’entrée et 0,17108 USD par million
de jetons de sortie, sous les nouveaux plafonds de 0,11 et 0,22 USD par
million. La lecture fraîche du solde a également abouti.

Avant le premier envoi, le client a relu sous verrou l’état de la clé et le
solde. La garde combinant limite de clé, budget global et réserve de compte a
refusé le préflight avec le diagnostic « limit_remaining hors budget autorisé
restant ». Le client actuel ne conserve pas le snapshot non secret de limite de
clé ni la branche précise de cette condition composée. Cette sous-condition
reste donc indéterminée; elle n’a pas été reconstruite après coup par une
nouvelle lecture.

L’arrêt est intervenu avant réservation et avant génération. Le bilan est de
zéro POST, zéro réponse, zéro identifiant de génération, zéro incident
fournisseur et zéro coût attribuable. Le parse, le raisonnement et le
déterminisme n’ont pas été observés. Le fichier de première passe existe mais
est vide; il est conservé comme marqueur matériel de l’arrêt. Le registre
global est inchangé.

Aucun `STOP` global n’a été touché et aucun `STOP-R6` n’a été nécessaire. Le GO
a été archivé comme consommé, sans relance. Aucune seconde passe et aucune
campagne n’ont commencé.
