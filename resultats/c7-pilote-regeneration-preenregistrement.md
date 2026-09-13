# C7 — pilote de régénération : préenregistrement

statut: courant
mandat: Pilote de regeneration payante : mesurer l'ecart entre deux executions du bras de titre
agent: agent/mesures/pilote-regeneration
ecriture: analyses/c7_pilote_regeneration.py, resultats/c7-pilote-regeneration-*
lecture_seule: tout le reste
interdits: article/manuscrit.md (autre agent), bras complet 2058, commit sur master, fusion
cout_reel_usd: 0.00

Commis **avant tout appel payant**, conformément au §4 du mandat. Aucun chiffre de résultat n'est
connu à la rédaction de ce fichier.

## 1. Pourquoi

`agent/mesures/variance-generation` a établi que **99,07 % de la variabilité du taux de
ré-identification vient de la configuration de génération et 0,93 % des personnes**, alors que les
intervalles publiés sont des bootstraps **sur les personnes**. Sept bras admissibles s'étalent de
2,1259 % à 20,6803 % (étendue 18,5544 points, contre 3,4673 points de largeur d'intervalle publié),
et **aucune condition ne possède deux exécutions** : zéro réplicat sur disque.

Le chiffre de titre — **20,6803 %**, bras `JSON Persona - GPT4.1` — est donc un **tirage unique**, et
c'est le **maximum** des huit bras admissibles. Ce pilote cherche une seule grandeur : **l'écart
entre deux exécutions de la même configuration**.

## 2. Ce qui est mesuré, et sur quel bassin

- **Bassin de personnes attaquées** : 150 personnes, tirées une seule fois, **strictement constantes
  entre les deux exécutions**. Le tirage est fait par `tirer_echantillon` sur la segmentation
  `S_gra`, graine `20260913`, et il est écrit dans le CSV de sortie avant tout appel.
- **Pool de candidats** : **invariant**, la population complète Twin-2K-500 (2 058 personnes). Il ne
  se réduit jamais au bassin attaqué. Hasard top-1 correspondant : 1/2 058 = 0,0486 %.
- **Items** : les 60 items de vague 4 toujours renseignés, tels que `c7_reidentification.items_communs`
  les détermine. Aucun choix d'items n'est fait après avoir vu un taux.
- **Mesure** : top-1 de ré-identification, jumeau contre humain de vague 4, distance de Hamming
  normalisée masquée, exactement `c7_reidentification`.

## 3. Convention de départage des ex æquo — **déclarée**

**Espérance sous départage uniforme** : la ligne de tête ex æquo compte pour 1/(taille de la classe
de tête). Implémentation retenue, identique à celle déjà publiée : 20 tirages, bruit i.i.d.
`rng.random(accord.shape) * 1e-9` ajouté aux scores, `argsort` stable, moyenne des indicatrices sur
les tirages (`c7_reidentification.rangs_attaque`). Les candidats sont mélangés avant tout calcul de
rang. **Cette convention vaut 1,32 sur Twin** au témoin de relecture-fond (k = 12 items). Les deux
conventions encadrantes (« en faveur », « contre ») ne sont pas employées ici et ne seront pas
substituées après coup.

## 4. Prédiction, et le seuil qui tranche

**Prédiction.** J'attends un écart absolu entre les deux exécutions **d'au moins 2 points de
pourcentage** sur le top-1, et je tiens pour plus probable un écart de l'ordre de 3 à 6 points que
d'un écart inférieur à 1 point. Motif : la configuration amont n'est pas documentée en température,
et les deux sources publiques disponibles se contredisent sur ce paramètre précis (voir §6).

**Seuil préenregistré.** Si l'écart absolu entre les deux exécutions dépasse **3,4673 points** — la
largeur de l'intervalle bootstrap publié pour le bras de titre — alors **les intervalles publiés sont
inutilisables comme énoncés sur le procédé** : ils seraient plus étroits que la variation d'une
simple relance à configuration identique. Ce seuil est écrit avant tout appel et ne sera pas déplacé.

Sous le seuil, la conclusion reste bornée : un seul couple d'exécutions ne donne pas un intervalle,
il donne un minorant de dispersion à deux points.

## 5. Dépense — plafonds déclarés, lus par le script

- **Plafond absolu du mandat : 60,00 USD.** Non négociable.
- **Plafond dur lu par `analyses/c7_pilote_regeneration.py` : 25,00 USD**, arrêt interne à
  **22,50 USD**, fichier `STOP` posé dès que le grand livre l'atteint.
- **Étape 0, plafond dédié : 2,00 USD** pour les cinq personnes de chiffrage.
- Coût de référence : **`usage.cost` annoncé par OpenRouter, jamais une estimation**, recoupé par la
  variation de `total_usage` sur `GET /credits` lue avant le premier appel et après le dernier.
- Le coût annoncé et le coût constaté vont tous deux au rapport, sans arrondi favorable.
- **Aucun bras complet ne sera lancé.** Ce mandat s'arrête à 150 personnes, quoi qu'il arrive.

## 6. Ce qui peut faire échouer ce pilote avant la mesure, et qui est déclaré ici

L'étape 1 du mandat exige de reconstituer la configuration du bras de titre **depuis le code et les
données**, et d'arrêter si elle n'est pas reconstituable avec certitude. Deux inconnues sont
identifiées **avant toute dépense** et sont susceptibles de déclencher cet arrêt :

1. Le paquet local ne contient **ni invite, ni message système, ni code de génération** — seulement
   des réponses formatées (`twin-ab-audit-provenance-2026-09-11.md`, §« Aucune invite n'a été lue »).
2. La correspondance entre l'étiquette `JSON Persona - GPT4.1` et une configuration amont précise
   n'est documentée nulle part, et la **température** — le paramètre qui gouverne précisément la
   grandeur cherchée ici — n'est pas établie.

Si l'étape 1 échoue, l'arrêt est le livrable, et l'étape 0 est néanmoins conduite parce que son
produit (le coût réel par personne) ne dépend pas du libellé de l'invite mais de la taille d'entrée,
du tarif et du nombre d'appels, tous trois établis indépendamment.

## 7. Clause anti-dragage

Une seule grandeur est publiée : le top-1 des deux exécutions et leur écart. Aucun sous-groupe,
aucun sous-ensemble d'items, aucune convention de départage alternative ne sera exploré après avoir
vu les taux. `analyses/c7_controle_interpretabilite.py` passe **avant** toute interprétation, et son
échec arrête le pilote sans seconde exécution. **Aucune donnée individuelle n'est imprimée** :
ni pid, ni appariement, ni extrait de prose personnelle — seulement des taux agrégés.

## 8. Ce que ce pilote ne fera pas

Il ne conclura pas en faveur de l'article par défaut. Si le procédé varie fortement d'une exécution
à l'autre, c'est le résultat, et il doit être connu avant le dépôt.
