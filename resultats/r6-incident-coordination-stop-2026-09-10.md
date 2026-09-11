# R6 — incident de coordination STOP et correction

## Incident

À 20:57:21 CEST, pendant l’exécution R6, `data/traces/STOP` a été créé pour empêcher le client R6 de poursuivre après les 429. Ce marqueur était global et partagé avec R7; il a donc arrêté Euler par effet de bord. Le parent a ensuite fait reprendre Euler. Cette interaction était une erreur de coordination R6. Aucun fichier STOP global n’a été créé, supprimé ou modifié pendant la correction décrite ci-dessous.

## Avant

Le client R6 ne connaissait que le STOP global hérité de R1. En outre, après quatre 429 et une cellule classée non jouée, il passait à la cellule suivante. L’arrêt manuel global a masqué cette seconde lacune et affecté R7. La version est archivée sous SHA-256 `dbe56d02619162c562175a99b53813bf68aa4bfd87873847707df55436aa88fa`.

## Après

R6 reconnaît désormais `data/traces/STOP-R6` comme marqueur dédié. Il continue de reconnaître `data/traces/STOP` comme ordre global utilisateur, en lecture seule. Le client ne crée ni ne supprime aucun de ces marqueurs. Selon le critère figé « plus de trois erreurs 429 sur vingt appels », la quatrième 429 arrête maintenant le run entier après consignation de la cellule courante; aucune cellule suivante n’est appelée.

Les tests factices vérifient que trois 429 restent dans le seuil, que la quatrième arrête avant la cellule suivante, que `STOP-R6` bloque le CLI avant réseau, qu’il ne modifie pas un témoin R7 et que le STOP global reste pris en charge sans modification. Les 197 contrôles passent. Aucun appel modèle, changement de clé, fournisseur, prix, plafond, réserve, invite, parse ou plan n’a été effectué. La collecte gratuite reste suspendue jusqu’à un nouveau GO.
