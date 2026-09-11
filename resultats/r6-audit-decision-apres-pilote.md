# R6 — audit de décision après le pilote DeepSeek

## Périmètre et limite de preuve

Cet audit est strictement hors ligne. Il lit le plan v2, le texte autonome du plan, les
addenda locaux reliés aux registrations `kmqnw`, `r72pj` et `k5qfh`, les archives de GO et
les rapports du pilote. Il ne vérifie pas le contenu d’OSF par réseau et ne lance aucun
appel.

La correspondance documentaire est établie ainsi : `kmqnw` est relié au dépôt de
l’addendum consolidé par la preuve locale et par le premier GO pilote; `r72pj` est cité
directement par l’addendum tarifaire et son GO; `k5qfh` est cité par le GO final, le rapport
et la réconciliation du pilote. Une limite subsiste : le gel final consigne pour
`r6-addendum-preflight-effectif-2026-09-10.md` le SHA-256 `8b550e7d…`, tandis que le fichier
local actuel vaut `eeaa445c…`. La preuve locale ne permet donc pas d’affirmer que ce fichier
est octet pour octet la narrative archivée sous `k5qfh`. Son contenu actuel et le gel
s’accordent toutefois sur les conditions utiles ici : clé finie, `limit_reset = null`,
`0 < d`, plafond effectif, vingt appels et plafonds financiers. La règle scientifique de
déterminisme vient du plan v2 antérieur et n’est modifiée par aucun de ces addenda.

## Clauses exactes du gate deux fois dix

Le plan autonome dit : « Pour chaque payant, l’essai de dix cellules envoyé deux fois
applique exactement ces règles » (`r6-plan-depot-2026-09-10.md`, lignes 99–102). Les
conséquences sont ensuite individualisées :

- coût projeté supérieur à 1,5 fois la ligne v2 : une correction, nouvel essai, puis
  « retrait du modèle » au second dépassement (lignes 103–104);
- moyenne de raisonnement supérieure à 50 : « même correction puis retrait » (ligne 105);
- plus de deux rejets de parse sur dix : « retrait, sans reformulation de l’invite »
  (ligne 106);
- moins de sept distributions identiques : « modèle marqué non déterministe, A4 lisible
  seulement avec le plancher machine » (lignes 107–108);
- plus de trois erreurs 429 sur vingt : attente d’une heure puis reprise sans seconde clé
  (lignes 109–110).

La version longue est encore plus explicite. Le tableau intitule sa dernière colonne
« seuil d’arrêt pour ce modèle », mais les trois premières lignes emploient le mot
« retrait », tandis que la ligne de déterminisme prescrit seulement : « le modèle est
marqué “non déterministe” et A4 n’y est lisible qu’à travers le plancher machine des 40
cellules » (`r6-preenregistrement-v2.md`, lignes 300–310). Le plan prévoit par ailleurs ce
plancher sur chaque modèle payant et fixe la lisibilité de A4 à une distance entre identités
supérieure à deux fois la distance entre passes (`r6-plan-depot-2026-09-10.md`, lignes
50–55).

L’addendum consolidé `kmqnw` remplace le gate gratuit par DeepSeek : « vingt appels, soit
deux passes distinctes de dix cellules », borne totale 0,02 USD et borne unitaire 0,001 USD.
Il le soumet aux critères déjà préenregistrés, qu’il énumère comme coût, raisonnement,
parse, déterminisme et 429 (`r6-addendum-prospectif-consolide-2026-09-10.md`, lignes 56–71).
Il dit aussi que « les critères d’arrêt par modèle […] restent inchangés » (lignes 9–13).

L’addendum tarifaire `r72pj` relève seulement les prix maximaux à 0,11/0,22 USD/M et affirme
qu’il « ne change pas les critères d’arrêt scientifiques ou techniques »
(`r6-addendum-prix-prospectif-2026-09-10.md`, lignes 3–28). L’addendum de préflight associé
à la préparation finale fixe les conditions financières et répète qu’il ne modifie pas les
critères scientifiques (`r6-addendum-preflight-effectif-2026-09-10.md`, lignes 3–37).

Le résultat observé est 1 distribution identique sur 10, donc inférieur à 7; coût,
transport, parse et raisonnement passent (`r6-pilote-deepseek-k5qfh-2026-09-10.md`, lignes
15–28). La réconciliation confirme 20 POST, 0 rejet, 0 incident, 0 jeton de raisonnement et
un coût réel de 0,0003289566 USD. Elle classe le seuil de déterminisme comme échoué.

## Quatre décisions qui ne doivent pas être confondues

**Arrêt du modèle.** La formule générale « arrête sur chacune » et l’en-tête « seuil
d’arrêt pour ce modèle » créent une ambiguïté de rédaction. La conséquence spécifique de
la ligne de déterminisme la résout : l’échec produit une étiquette et une restriction de
lecture de A4, sans ordre de retrait. Le rapport exploratoire confirme cette lecture en
écrivant que DeepSeek « doit donc rester marqué non déterministe si la campagne est
poursuivie ». Présenter 1/10 comme une règle enregistrée d’arrêt définitif du modèle serait
donc inexact.

**Arrêt de la campagne.** La campagne est néanmoins arrêtée dans l’état opérationnel
présent. Le GO `k5qfh` avait pour champ exact « pilote uniquement; aucune campagne » et il a
été archivé comme consommé. `GO-R6` est absent et `STOP-R6` est présent. Cet arrêt vient de
la portée du GO et du gel de coordination; il ne transforme pas la ligne de déterminisme en
retrait préenregistré.

**Retrait.** Dans le texte enregistré, le retrait est la conséquence explicite d’un second
dépassement de coût après correction, d’un second dépassement de raisonnement après
correction, ou de plus de deux rejets de parse. Aucun de ces faits n’est observé. DeepSeek
n’est donc pas retiré par une clause enregistrée. Un abandon volontaire reste possible,
mais doit être rapporté comme décision post-pilote et non comme application rétroactive du
seuil 7/10.

**Redesign.** Ajouter un seed, changer de fournisseur, répéter chaque cellule puis moyenner,
changer le seuil 7/10 ou remplacer l’égalité exacte par une tolérance modifie la requête,
le couple modèle-fournisseur, l’estimand ou la règle de décision. Ce sont des redesigns.
Ils ne peuvent ni réparer rétroactivement le pilote ni être introduits sous les dépôts
actuels. La revue adverse relève en outre que, pour une moyenne de trois répétitions, le
plancher doit viser le même estimand : 3 × (1 210 + 40) = 3 750 appels, pas 3 670.

## Conclusion opérationnelle unique

**Aucun appel ni lancement de campagne n’est autorisé maintenant.** Le seul GO applicable
était limité au pilote et est consommé; le marqueur `STOP-R6` maintient le gel.

Sans nouveau dépôt OSF, il est conforme de terminer et publier la documentation du pilote,
de conserver DeepSeek comme « non déterministe », d’appliquer le plancher machine à A4, ou
d’abandonner sa ligne descriptive en déclarant honnêtement une attrition post-pilote. Le
protocole déposé permet aussi, sur le fond, la campagne DeepSeek inchangée à une réponse par
cellule chez DigitalOcean : l’échec 1/10 n’est pas une clause de retrait. Cette campagne ne
pourrait toutefois partir qu’après un **nouveau GO explicite de campagne**, la levée
explicite de `STOP-R6` et les mêmes gardes opérationnelles; ces actes d’exécution ne sont pas
un nouveau dépôt.

Un nouveau dépôt prospectif est requis avant tout redesign : seed, autre fournisseur,
répétitions agrégées, nouveau pilote, modification du seuil ou de la métrique de
déterminisme, ou nouvelle règle faisant de 1/10 un retrait. Tant qu’aucun de ces choix n’est
déposé et qu’aucun nouveau GO de campagne n’est donné, le gel actuel est la seule décision
opérationnelle conforme.
