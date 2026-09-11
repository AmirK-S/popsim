# R6 — audit hors ligne du non-déterminisme et du registre gelé

## État

La campagne R6 reste gelée par `data/traces/STOP-R6`. Cette analyse a utilisé seulement
les fichiers locaux; elle n'a effectué aucun appel réseau ni génération. Elle ne modifie
ni l'invite, ni le parse, ni les paramètres de génération.

## Pilote DeepSeek

Les deux passes comportent les mêmes dix cellules, dans le même ordre. Pour chacune des
dix paires, l'empreinte de requête est identique; la charge reconstruite et les messages
sont identiques. Chaque charge demandait le modèle `deepseek/deepseek-v4-flash`,
`temperature: 0.0`, `max_tokens: 150`, `reasoning: {enabled: false, exclude: true}` et
`usage.include: true`, avec `DigitalOcean` seul, sans repli et avec les bornes de prix
0,11/0,22 USD par million de jetons.

`seed`, `top_p`, `top_k` et `stop` étaient absents des vingt charges. Les vingt réponses
renvoient `DigitalOcean`, le modèle demandé, une fin `stop` et zéro jeton de raisonnement.
Le parse strict accepte 20/20 réponses, sans relance ni rejet.

Les sorties brutes diffèrent dans 10/10 paires; les distributions parsées diffèrent dans
9/10. La distance L1 par paire est comprise entre 0 et 0,20 (moyenne 0,106; médiane
0,100), soit une variation totale moyenne de 0,053. Le critère pilote de déterminisme
échoue donc: 1/10 distributions identiques, sous le seuil de 7/10.

La trace démontre que `temperature: 0.0` a été demandée dans 20/20 requêtes. Aucune
métadonnée de réponse conservée ne déclare la température ni une graine effectivement
appliquée par le fournisseur. L'hypothèse d'une température ignorée est compatible avec
les observations, mais son taux ou sa probabilité ne sont pas identifiables ici. Les
traces ne permettent pas davantage de départager une autre source interne au service.

## Registre au gel

Le registre est intègre contre son manifeste d'import. Les vingt appels pilotes sont tous
réconciliés: 0,020 USD réservés au pire cas et 0,0003289566 USD de coût établi. Les 138
réponses de campagne déjà écrites représentent 0,0022036021 USD établis. La campagne a
ensuite reçu deux 429 pour la même cellule `fucitzn`; la première réservation a été
annulée après la preuve déjà archivée. La seconde laisse une unique réservation ambiguë de
0,001 USD. Elle n'est ni un coût établi ni une annulation établie, et bloque toute reprise.

Ainsi, le total DeepSeek actuellement porté par le registre est 0,0035325587 USD, composé
de 0,0003289566 USD pilote réglé, 0,0022036021 USD campagne réglée et 0,001 USD retenu
pour l'ambiguïté. Le total R6 porté par le registre est 0,0374371087 USD; il inclut cette
seule réservation non réglée. Il ne faut pas l'annoncer comme coût final.

## Seule amélioration instrumentale proposée

Pour une expérience ultérieure autorisée séparément, conserver avant envoi un manifeste
privé de paramètres canoniques, sans invite ni secret: présence ou absence de `seed`,
`top_p`, `top_k` et `stop`, valeurs de température, raisonnement, fournisseur et bornes,
plus les empreintes des messages et de la charge. Conserver aussi, lorsqu'elle est fournie,
la seule métadonnée serveur non secrète décrivant les réglages effectivement appliqués.
Cette instrumentation ne change pas la charge et ne résout pas rétroactivement le pilote.
Ajouter une graine ou modifier un paramètre changerait le protocole; aucune telle
correction n'est proposée. La campagne reste donc arrêtée.

## Empreintes vérifiées

| artefact | SHA-256 |
|---|---|
| pilote passe 1 | `c9ac4ccbad6e25916949834cc2707a021a0d1dbdc4f4e1911ff8c740034ae8c2` |
| pilote passe 2 | `874d3a91fd4041d3f58675bcabcbea327061015a710a9f86f6eda854dd327164` |
| campagne F1, 138 lignes | `edd29d93760d96085226f05fe197529acd5364817478c68b6a7f17387bc66537` |
| registre | `1f5ae9642704319bd5798ede24909ecc714d6b9b1fbba98327057e30b7b996c0` |
| analyse privée pilote antérieure | `57df0afca7c311b219b66d9b40f1ce61d2cc315bf7be7ad567460fc1a046a39f` |
