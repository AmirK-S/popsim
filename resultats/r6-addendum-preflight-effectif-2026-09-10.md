# R6 — addendum prospectif corrigé du préflight financier

Statut : texte préparé après revue Euler, avant tout nouveau GO et avant toute nouvelle
tentative du pilote. Il complète la correction tarifaire `r72pj` sans modifier les
hypothèses, les invites, les cellules, le fournisseur, les critères scientifiques ni les
budgets enregistrés.

## Conditions obligatoires sur la clé

Le snapshot frais de la clé doit fournir deux nombres présents et finis : `limit = K` et
`limit_remaining = K_r`. Le préflight refuse l’appel sauf si :

`0 < K_r ≤ K ≤ 4,40 USD`.

Il exige également `limit_reset = null`, `disabled ≠ true` et
`is_management_key ≠ true`. Une valeur absente, non numérique, NaN, infinie, nulle ou
négative produit une branche de refus explicite avant réservation et avant POST.

## Plafond effectif

Pour chaque appel, sous le verrou du registre global, on définit :

- `L = 4,40 USD`, plafond global R6 ;
- `T`, somme des coûts réglés et des réservations non réconciliées du registre ;
- `C`, solde frais du compte (`total_credits − total_usage`) ;
- `R = 1,50 USD`, réserve intangible du compte ;
- `A`, somme des réservations non réconciliées ;
- `G = max(0, L − T)`, budget global restant ;
- `B = max(0, C − R − A)`, solde disponible après réserve prudente ;
- `U = min(G, B, K_r)`, plafond effectif de l’appel.

Si `b` est la réservation au pire cas de l’appel et `d` la borne dérivée de
`max_prompt_tokens`, `max_tokens` et `provider.max_price`, l’autorisation financière exige
`0 < d ≤ b ≤ U`. Pour le pilote, elle exige en plus `b ≤ 0,001 USD`, au plus vingt appels
et un cumul pilote, réservations comprises, inférieur ou égal à `0,02 USD`. Le plafond
tarifaire reste 0,11 USD/M en entrée et 0,22 USD/M en sortie. Le modèle reste
`deepseek/deepseek-v4-flash`, fournisseur DigitalOcean sans repli.

Cette formule ne demande pas de financer les 4,40 USD entiers : une clé à 4,40 USD et un
solde après réserve de 4,278549 USD donnent `U = 4,278549 USD`, ce qui couvre une
réservation de 0,001 USD.

## Réservations ambiguës et double comptage

Une réservation ambiguë entre dans `T` pour préserver le plafond global et dans `A` pour
préserver la réserve du compte. Ces déductions protègent deux contraintes distinctes.
Cependant, le snapshot de crédits peut déjà incorporer tout ou partie du coût ambigu ;
dans ce cas, `C − R − A` est volontairement conservateur et peut compter ce coût deux fois
sur la branche compte.

Ce conservatisme n’a actuellement aucun effet sur une autorisation : le client refuse tout
nouvel appel dès que `A > 0`, avant réservation et avant POST. Ainsi, toute branche
autorisée satisfait nécessairement `A = 0`. Si cette interdiction devait être retirée, la
formule du compte devrait être revue pour rapprocher la réservation du coût déjà inclus
dans le snapshot.

## Instrumentation et vérification

Chaque décision transactionnelle écrit en privé le snapshot non secret de `K`, `K_r` et
des indicateurs de clé, les valeurs `G`, `B`, `U`, `b`, `d`, et une branche stable de refus
ou `autorise`. Aucune clé ni valeur d’en-tête d’autorisation n’est conservée.

Les 220 contrôles factices hors ligne passent. Ils couvrent les valeurs absentes ou non
finies, le reset non nul, les relations `K_r > K` et `K > 4,40`, le cas
`U = 4,278549`, la limite insuffisante, l’absence de réservation et de POST après refus,
ainsi que les plafonds cumulés du pilote. Aucun réseau distant, GET authentifié, POST de
génération ou GO n’a été utilisé pour préparer et tester cette correction.
