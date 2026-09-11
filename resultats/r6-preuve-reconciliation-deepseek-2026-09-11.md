# R6 — preuve de réconciliation DeepSeek/F1

Une cellule F1 a reçu un HTTP 429 avec un identifiant de génération et a donc été bloquée
sans rejeu. Deux lectures authentifiées séparées des métadonnées et du contenu de génération
ont retourné 404; aucun contenu exact n'était récupérable.

Le solde frais a été lu deux fois et était identique. Depuis le premier préflight de la
campagne, sa baisse est de `0.002203544 USD`; les 138 réponses F1 réglées totalisent
`0.0022036021 USD`. L'écart de `0.0000000581 USD` est inférieur à l'arrondi affiché et ne
laisse aucune place à la borne réservée de `0.001 USD`. Aucun autre client R6 n'était actif.

La réservation a donc été annulée avec cette preuve, tandis que son marqueur `.en-cours` a
été archivé. La cellule demeure absente de la trace principale et doit être rejouée une seule
fois au prochain run, sans être présentée comme une réponse déjà observée.

Les tests locaux confirment les deux propriétés: un 429 ambigu interdit tout second POST; une
annulation prouvée permet ensuite exactement un POST fixture, avec nouvelle écriture de trace
et réconciliation. Aucun appel de génération réel n'a été fait pendant ces tests.
