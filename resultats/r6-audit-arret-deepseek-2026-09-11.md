# Audit indépendant de l’arrêt DeepSeek R6

Audit local du 11 septembre 2026, sans réseau ni lecture de distribution de campagne. Ont été
lus seulement le registre transactionnel, les diagnostics HTTP filtrés, les marqueurs
`.en-cours`, les pièces de rapprochement et le fichier d’arrêt.

## État constaté

Les diagnostics HTTP privés enregistrent trois réponses 429 DeepSeek à 00:21:15, 00:29:20 et
00:49:49 CEST. Les trois portent un `generation_id`. Les valeurs de ces identifiants ne sont
pas reproduites ici. Le journal HTTP seul ne porte ni empreinte de requête ni coût; il ne
permet donc pas, isolément, de prouver une absence de facturation.

Le ledger contient 220 opérations de campagne réconciliées et une réservation de campagne
encore ouverte, avec empreinte de requête et fournisseur imposé présents. Cette réservation
ne porte ni rapprochement, ni annulation, ni preuve de coût. La trace F1 a 220 lignes, le
marqueur `.en-cours` existe toujours, et aucune opération F2 ou plancher n’est réglée.
DeepSeek est donc non terminal : 220, et non 1 250, opérations réglées.

Les deux pièces de rapprochement précédentes ne ferment pas la troisième ambiguïté : l’une
conserve explicitement une réservation faute de preuve objective; l’autre établit seulement
la non-facturation d’une réservation antérieure et l’annule. Elles ne valent pas preuve pour
la réservation actuellement ouverte.

## Conformité au plan de contingence

La règle numérique déposée est « plus de trois erreurs 429 sur vingt appels », puis attente
d’une heure et reprise sans seconde clé. Trois incidents ne satisfont donc pas cette condition
à eux seuls : elle se déclencherait au quatrième 429, pas au troisième.

Le cas observé relève toutefois d’une garde distincte et plus stricte. Le client classe un
429 portant un `generation_id` comme coût incertain et non rejouable. Le plan exige qu’une
issue ambiguë bloque la suite; le fichier `STOP-R6` en vigueur confirme qu’aucune reprise,
aucun modèle suivant et aucune contingence ne sont permis avant rapprochement de cette
réservation et décision de protocole distincte. L’arrêt est donc justifié par l’ambiguïté de
facturation, pas par le seuil quantitatif de trois 429.

## Successeurs

**Non autorisés sous le plan actuel.** Lancer un successeur avant clôture objective de la
réservation ouverte contredirait la garde d’ambiguïté, le `STOP-R6` actif et le principe de
fournisseur sans repli. Une reprise DeepSeek ou le lancement d’un autre modèle exige d’abord
une preuve de facturation ou de non-facturation reliée à cette réservation, sa réconciliation
ou annulation dans le ledger, puis la décision de protocole distincte explicitement demandée
par le stop. Cette conclusion ne modifie ni le plan ni la campagne.
