# R6 — analyse instrumentale hors ligne du pilote k5qfh

## Gel

La campagne reste gelée après le verdict pilote négatif. `GO-R6` est absent. Aucun appel
réseau ou modèle n’a été effectué pour cette analyse. Un arrêt R6 dédié est posé après
l’analyse; le STOP global reste absent.

## Requêtes

Les vingt empreintes enregistrées se reconstruisent exactement à partir du client gelé et
des cellules tracées. Les dix paires inter-passes ont les mêmes messages, la même charge
canonique et la même empreinte. Les paramètres reconstruits sont : modèle
`deepseek/deepseek-v4-flash`, `temperature = 0.0`, `max_tokens = 150`, raisonnement
désactivé (`enabled = false`, `exclude = true`), comptage d’usage demandé, DigitalOcean
seul sans repli, et prix maximaux 0,11/0,22 USD/M. Aucun champ `seed`, `top_p`, `top_k` ou
`stop` n’a été envoyé.

## Réponses et parse

DigitalOcean est le fournisseur renvoyé pour les vingt réponses; le modèle renvoyé est le
modèle demandé et les vingt fins sont `stop`. Les vingt identifiants sont uniques. Le
raisonnement compté vaut zéro partout. Le même parse strict a accepté 20/20 réponses sans
relance ni rejet.

Aucune des dix paires de sorties textuelles brutes n’est strictement identique. Une seule
des dix distributions parsées est identique. Sur les distributions, la distance L1 moyenne
est 0,106, la médiane 0,100 et l’étendue 0 à 0,200; la variation totale moyenne vaut 0,053.
Les traces sont scellées par SHA-256 dans la preuve privée.

## Température effective

Le fait démontré est que `temperature = 0.0` figure dans 20/20 charges reconstruites et que
les dix paires de charges sont identiques. En revanche, aucune réponse conservée ne rapporte
la température ou le seed effectivement appliqué côté fournisseur. Les variations observées
sont compatibles avec une température ignorée, mais elles ne prouvent pas cette cause et ne
permettent pas d’en estimer la probabilité. Les traces ne distinguent pas non plus d’autres
sources internes au service. L’analyse s’arrête à cette limite documentaire.

## Registre

Le registre final contient vingt réservations et vingt rapprochements, tous réglés avec les
vingt identifiants des traces. La borne réservée totalise 0,020 USD et le coût réconcilié
0,0003289566 USD. Aucune réservation ambiguë ne subsiste.

## Seule correction instrumentale sans changement de protocole

Pour une éventuelle expérience future faisant l’objet d’une autorisation distincte, le
client pourrait conserver la charge canonique non secrète ainsi que des en-têtes ou
métadonnées de succès strictement autorisés lorsqu’ils déclarent les réglages
échantillonnage effectivement appliqués. Cette instrumentation ne peut pas compléter
rétroactivement le pilote achevé. Ajouter un `seed` modifierait la charge expérimentale et
ne constitue donc pas une correction instrumentale de ce protocole. En l’absence de
métadonnée serveur supplémentaire, aucune autre correction hors ligne ne peut départager
les causes; la campagne reste arrêtée.
