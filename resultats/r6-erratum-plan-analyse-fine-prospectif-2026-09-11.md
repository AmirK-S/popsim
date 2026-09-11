# Erratum de portée et d’unités pour le plan d’analyse fine R6

Cet erratum complète `r6-plan-analyse-fine-prospectif.md`. Il ne modifie ni le
préenregistrement R6 `abf7y`, ni l’addendum `kmqnw`, ni les hypothèses, familles,
seuils, données, appels ou sorties confirmatoires.

## Portée enregistrée et portée exploratoire

Les seuls éléments confirmatoires enregistrés sont H1, H2 et H3 du plan R6, avec
la précision du test H2 contre 2 dans l’addendum prospectif. H4 est exclusivement
exploratoire selon `kmqnw`: T et son IC bootstrap apparié, sans p, Holm ni verdict.

Les sections 3.1 à 3.5 du plan d’analyse fine sont une procédure prospective locale
d’exploration, pas des analyses préspécifiées par `abf7y` ou `kmqnw`. Dans tout
rapport, remplacer « Hétérogénéité préspécifiée » par « Hétérogénéité exploratoire
fixée dans cette page ». Elles restent sans p, seuil, Holm, sélection de modèle ou
promotion confirmatoire.

## Corrections d’unité et de reproductibilité

1. Le contraste A2 signé et son contraste de format F2 moins F1 sont définis par
   `item × identité`, après appariement des cellules gauche et droite. Ils ne sont
   jamais calculés, affichés ou stratifiés « par camp ». Les positions décrites
   gauche et droite peuvent être montrées séparément comme composantes brutes du
   numérateur, avec le même item et la même identité, sans les appeler estimations
   A2 distinctes.

2. La stratification « famille » emploie exclusivement le champ `famille` déjà
   porté par chaque trace acceptée. La polarité emploie exclusivement la colonne
   `oriente` et le sens de `resultats/a37-orientation-items.csv`; son empreinte
   SHA-256 est publiée avec les sorties. Une valeur absente ou incompatible ne
   reçoit aucune nouvelle codification: la strate correspondante est
   `NON_INTERPRÉTABLE`.

3. Chaque sortie intermodèles porte explicitement ses clés: `format`, `camp` et
   `identité` pour les métriques de cellule ou A1; `format` et `identité` pour A2;
   `format` et `camp` pour A4. La TV intermodèles est résumée à poids égal sur les
   cellules communes de cette clé. Les corrélations de rang sont calculées sur les
   items communs de la même clé, avec rangs moyens pour les ex æquo; moins de cinq
   items ou une série constante donne `NON_INTERPRÉTABLE`.

4. Les deux passes pilote restent hors des masques, effectifs, IC et classements de
   campagne. Elles ne servent qu’au diagnostic descriptif séparé et ne peuvent ni
   compléter une cellule de campagne, ni modifier la décision de déterminisme déjà
   rendue, ni contribuer à H1–H4.

Ces précisions rendent les explorations reproductibles et évitent le double usage
des pilotes, sans créer de test supplémentaire.
