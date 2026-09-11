# R6 — addendum prospectif consolidé avant appels payants et modèles fermés

Cet addendum, validé en revue indépendante Euler, complète le préenregistrement R6 `abf7y`.
Il est écrit avant tout appel payant et avant toute collecte sur un modèle fermé. Aucun
appel concerné par cet addendum ne doit partir avant son dépôt.

## Portée des changements

Cet addendum explicite le test H2, reclasse H4 et remplace une condition technique de
lancement devenue impraticable. Il ne change ni la question, ni l’invite, ni les items, ni
les formats F1/F2, ni le panel, ni l’ordre des modèles, ni H1 ou H3. Les critères d’arrêt par
modèle, le plafond global R6 de 4,40 USD et la réserve de compte de 1,50 USD restent
inchangés. Ces décisions répondent à des problèmes définis avant observation des résultats
confirmatoires; elles ne reposent sur aucune estimation R6.

## H2 : test par inversion de signe contre le seuil 2

Pour chaque modèle fermé et chacun des camps gauche et droite, A4 reste le rapport de
moyennes défini par R1 : moyenne de la distance de variation totale entre identités divisée
par la moyenne du plancher humain apparié. Le test bilatéral par inversion de signe contre
le seuil 2 emploie par item la quantité :

`TV(identités) − 2 × TV(vague 1, vague 2)`.

Son signe est changé indépendamment par item, avec 20 000 permutations et l’estimateur de
Phipson–Smyth. Ce test suppose que, sous la nulle, les différences centrées sont
échangeables par inversion de signe, donc symétriques autour de zéro; cette hypothèse est une limite
de l’inférence. Les dix p sont corrigés ensemble par Holm dans F2. Une ligne n’est retenue
dans la direction annoncée que si la borne basse de l’IC bootstrap de A4 est supérieure à
2, si le p corrigé est inférieur à 0,05 et si la distance entre identités dépasse deux fois
le plancher machine.

Avant analyse, quatre contrôles locaux sont bloquants : exactement 149 items uniques,
exactement 79 items orientés, effectifs maximaux gauche/centre/droite égaux à 417/303/332,
et facteur humain vague 2 sur vague 1 arrondi à 1,009 et compris dans [0,85 ; 1,15].

## H4 : abandon confirmatoire et restitution exploratoire

La permutation d’étiquettes par item envisagée après le dépôt a été rejetée en revue : elle
impose une nullité d’échangeabilité plus forte que la nulle substantielle visée et peut
rendre la statistique dégénérée. Aucune permutation studentisée ni autre analyse de
remplacement n’est ajoutée. La famille confirmatoire F4 prévue est abandonnée faute de test
valide fixé avant observation. H4 reste un pari descriptif.

Pour chaque paire prévue, sur les mêmes items orientés valides dans les deux modèles et en
identité journaliste, on rapporte seulement :

`T = |A2_palier_supérieur − 1,009| − |A2_palier_économique − 1,009|`.

L’IC à 95 % est obtenu par 2 000 tirages bootstrap appariés des triplets par item
`(d_palier_supérieur, d_palier_économique, r)`, avec recalcul des deux ratios globaux A2 et
de T à chaque tirage. Aucun p, aucune significativité, aucune correction de Holm et aucun
verdict confirmatoire ne sont produits. Le signe de T et son IC sont décrits. Avec une seule
paire jouée, la restitution reste un cas unique non généralisable.

## Remplacement du gate gratuit indisponible

Le gate de dix appels sur un modèle `:free`, rendu obligatoire à l’étape 0, est abandonné
après des erreurs 502 et 429 répétées. Cette décision constate la disponibilité insuffisante
du fournisseur gratuit; elle ne constitue ni un résultat statistique ni un jugement sur la
qualité d’un modèle. Les validations déjà disponibles restent consignées : 40 cellules sur
40 concordantes pour la voie chat locale, des réponses gratuites valides obtenues lors des
pilotes techniques, et 208 tests du client réussis sur mocks et serveurs loopback.

Le gate de remplacement porte sur `deepseek/deepseek-v4-flash` : vingt appels, soit deux
passes distinctes de dix cellules sur la liste d’essai fixée. Sa borne dure totale est de
0,02 USD pour l’ensemble du pilote, avec une borne maximale de 0,001 USD par appel. Il reste
soumis aux réglages, au fournisseur imposé sans repli, au registre, à la réconciliation et
aux critères d’arrêt déjà préenregistrés : projection de coût, jetons de raisonnement,
rejets de parse, déterminisme et incidents 429. Son coût entre dans le plafond global de
4,40 USD et ne réduit jamais la réserve de 1,50 USD.

Les sorties publiques donnent les nombres d’incidents par statut et le coût agrégé
attribuable à R6 sur la clé, sans clé, en-tête, identifiant de compte, solde détaillé, chemin
privé ni réponse brute. Les anciennes réponses gratuites restent exploratoires; leur coût
annoncé nul est distingué des incidents sans coût observé, et un usage courant nul de la clé
n’est pas présenté comme preuve rétroactive.

Tant que ce projet n’est pas revu puis déposé, H4 reste `INDEFINI` dans le code et aucun gate
payant, appel de modèle fermé ou analyse exploratoire H4 n’est lancé.
