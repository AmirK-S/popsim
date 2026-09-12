# Résultats — plan factoriel un-facteur-à-la-fois (M / G / P)

> **AVERTISSEMENT (12 septembre 2026) — conclusion de ce rapport invalidée.** Les jumeaux M/G/P
> régénérés pour cette expérience ne réidentifient la personne réelle qu'au taux du hasard
> (top-1 de 0,0 à 0,8 % contre 0,83 % attendu par hasard), **avant même toute manipulation** —
> voir `resultats/c7-reconciliation-facteurs-2026-09-12.md` §3-4. Leurs contrastes B↔M/G/P
> comparent donc deux sources de bruit, pas deux jumeaux porteurs d'une personne : la
> conclusion « changer un seul facteur effondre le canal » (§4 à 6 ci-dessous) n'est pas
> réfutée, elle **n'a pas pu être testée** — limite de cet instrument, pas résultat sur le
> monde. Restent exacts et utilisables : les mesures brutes de top-1 elles-mêmes (§3) et le
> coût réel mesuré (§2). C'est leur interprétation comme preuve de fragilité du canal qui
> tombe.

Exécution de `analyses/c7_factoriel.py`, préenregistrement
`resultats/c7-factoriel-preenregistrement.md` (commité seul, avant tout appel payant,
commit `ff90409`). Sortie chiffrée : `resultats/c7-factoriel.csv`. Trace brute :
`data/traces/c7-factoriel.jsonl` (360 lignes, toutes réussies, 0 échec, 0 HTTP 429).

## 1. Ce qui a réellement tourné

- **Bras commun (relu, gratuit)** : organisation B (`deepseek/deepseek-v4-flash`, persona
  JSON, gabarit système+utilisateur, sortie « Qxx: n ») — 120 réponses relues telles
  quelles depuis `data/traces/c7-deux-organisations.jsonl` (déjà 100 % couvertes, aucun
  nouvel appel).
- **(M) modèle différent** : `prompt_b` rejoué à l'identique (persona JSON, gabarit B),
  modèle `qwen/qwen-2.5-72b-instruct` (DeepInfra) au lieu de `deepseek/deepseek-v4-flash`.
- **(G) gabarit différent** : nouvelle combinaison `prompt_g` — style d'instructions et
  format de sortie de C (un tour utilisateur, « k) n », `parser_c`) appliqué au dossier
  JSON (`persona_json`, la fonction de B), modèle `deepseek/deepseek-v4-flash`.
- **(P) persona différente** : nouvelle combinaison `prompt_p` — gabarit de B
  (`SYSTEME_B`, système+utilisateur, « Qxx: n », `parser_b`) appliqué à la biographie
  narrative (`persona_narrative`, la fonction de C), modèle `deepseek/deepseek-v4-flash`.
- 120 personnes (mêmes index locaux 0..119 du même tirage stratifié `S_gra`, graine
  20260912, que `c7_deux_organisations.py`), 60 items cibles identiques. Couverture 100 %
  (60/60 items lus) pour les trois conditions et les 120 personnes, aucune reprise
  nécessaire, aucun 429.
- Mesure : `rangs_attaque`, `rang_dans_segment`, `bootstrap_personnes` importés tels
  quels depuis `c7_reidentification.py`/`a2_commun.py`, attaque symétrique (moyenne des
  deux sens), IC bootstrap à 2000 tirages — méthode identique à `c7_deux_organisations.py`.
- Les trois déviations déclarées dans `c7_deux_organisations.py` (réponse par numéro,
  persona narrative repérée par QID, format de sortie C ancré ligne par ligne) sont
  héritées automatiquement : aucune des fonctions réutilisées n'a été réécrite.

## 2. Tenue de compte — coût réel exact

360 appels réussis (120 × 3 conditions), **0 échec, 0 HTTP 429**. Coût total mesuré (somme
exacte des `usage.cost` OpenRouter, pilote de validation à 1 personne inclus) :
**0,5385601250 USD**, sous le plafond dur de 1,00 USD et sous l'arrêt interne de 0,90 USD
(marge restante : 0,46 USD). Coût projeté au préenregistrement : ≈ 0,60 USD — le coût réel
est même légèrement inférieur à la projection.

## 3. Résultat mesuré

n = 120 pour les quatre lignes (les trois attaques symétriques B↔X et la baseline
Demographics Only recalculée sur ce même pool de 120).

| condition | top1 | IC 95 % | top1_segment (contrôle) | IC 95 % |
|---|---|---|---|---|
| **B↔M** (modèle différent) | **0,67 %** | [0,00 ; 1,75] | 19,13 % | [13,33 ; 24,98] |
| **B↔G** (gabarit différent) | **0,83 %** | [0,00 ; 2,08] | 16,63 % | [11,21 ; 22,19] |
| **B↔P** (persona différente) | **2,65 %** | [0,50 ; 5,13] | 22,33 % | [16,25 ; 28,96] |
| Demographics Only (pool=120, recalculée) | 13,29 % | [7,46 ; 19,29] | 38,21 % | [29,75 ; 46,67] |

Bornes de référence citées telles quelles, non recalculées :

| borne | top1 | IC 95 % |
|---|---|---|
| Intra-équipe (7 configurations riches, 30 paires, même équipe) | **36,4 %** | — (cf. `c7-temoin-prompt-resultats.md`) |
| Tout différent (B↔C, n = 142, expérience précédente) | **1,76 %** | [0,35 ; 3,63] |

(top10 : M = 10,4 % [6,0 ; 15,3] ; G = 12,6 % [7,8 ; 17,8] ; P = 15,0 % [9,5 ; 21,0].
Hasard top1 = 1/120 = 0,83 %.)

## 4. Application de la règle de décision préenregistrée (section 5)

Pour chaque condition X, « X porte le signal seul » exige **à la fois** :
bas_X > 3,63 % (borne haute de l'IC « tout différent ») **et** top1_X ≥ 2 × 13,29 % = 26,58 %.

- **M** : bas = 0,00 % ≤ 3,63 % → critère non rempli.
- **G** : bas = 0,00 % ≤ 3,63 % → critère non rempli.
- **P** : bas = 0,50 % ≤ 3,63 % (chevauche même l'IC « tout différent ») → critère non
  rempli, et de loin (top1 = 2,65 % contre 26,58 % requis).

**Aucun des trois facteurs ne porte le signal seul.** Les trois conditions restent, chacune,
sous la baseline démographique elle-même (13,29 %) — pas seulement sous son double — et deux
d'entre elles (M, G) ont même un IC dont la borne haute reste sous 2,1 %, à peine plus haut
que la borne « tout différent » (1,76 % [0,35 ; 3,63]). Ce n'est pas le résultat nul défini en
section 5 du préenregistrement (les trois IC ne se recouvrent pas simultanément avec un
chiffre franchement au-dessus de 2× la baseline démographique — au contraire, les trois sont
nettement, unanimement, en dessous) : c'est un résultat destructeur net et concordant.

Vérification du garde-fou « rien montré » : il exigeait que les trois IC se recouvrent à la
fois avec la borne basse **et** avec une valeur franchement supérieure à 2× Demographics Only
(26,58 %). Aucune des trois conditions n'approche cette valeur (haut IC maximal = 5,13 % pour
P) : le garde-fou n'est pas déclenché, le résultat est bien informatif, pas un artefact de
sous-puissance.

## 5. Ma prédiction préenregistrée est réfutée

J'avais prédit (section 4 du préenregistrement) : M ≈ 20 % [8 ; 35], G ≈ 15 % [5 ; 30],
P ≈ 8 % [2 ; 20] — dans cet ordre, avec P le plus dégradé. Le résultat mesuré est à la fois
**bien plus bas que prévu pour les trois conditions** (aucune des trois n'atteint même le
bas de son propre intervalle prédit) et **dans l'ordre inverse de celui prédit** : c'est P
(persona différente) qui préserve le *plus* de signal (2,65 %), pas le moins, et M
(modèle différent) qui en préserve le *moins* (0,67 %), pas le plus. Mon raisonnement — que
conserver le même modèle et le même gabarit protégerait l'essentiel du canal individuel
porté par un dossier JSON riche — ne tient pas : changer une seule pièce du pipeline
(n'importe laquelle des trois) suffit à effondrer le canal presque aussi complètement que
changer les trois à la fois.

## 6. Ce que ce résultat dit

Aucun des trois facteurs prise isolément n'explique, à lui seul, l'effondrement mesuré dans
l'expérience « deux organisations ». Les trois conditions à un seul facteur changé
atterrissent toutes dans la même fourchette basse que la configuration où les trois facteurs
changent ensemble (0,67–2,65 % contre 1,76 % pour « tout différent »), très en dessous de la
borne intra-équipe (36,4 %) et même en dessous de la baseline démographique recalculée sur
le même pool (13,29 %). Le canal inter-jumeaux mesuré par A7 n'est donc pas simplement
fragile à la combinaison complète des trois changements : il est déjà fragile à **n'importe
lequel** des trois pris seul, dans cette réalisation (un modèle B fixe, changé sur un seul
axe à la fois). Il n'a pas été possible d'identifier un facteur « protecteur » — le résultat
est négatif sur les trois facteurs testés, pas indéterminé.

## 7. Limites honnêtes

- Effectif n = 120 par condition : suffisant pour distinguer un effet large (n'importe
  laquelle des trois conditions dépassant nettement la borne « tout différent » et 2× la
  baseline), ce qui s'est produit ici dans le sens négatif (aucune ne la dépasse). L'effectif
  reste, comme annoncé au préenregistrement, insuffisant pour trancher entre des effets
  modérés et proches (les IC de M, G et P se chevauchent tous les uns les autres : on ne peut
  pas affirmer avec confiance que P préserve statistiquement plus de signal que M ou G,
  seulement que les trois sont, ensemble, très en dessous du seuil de signal).
- Un seul point de départ (le pipeline B, modèle deepseek-v4-flash / persona JSON / gabarit
  système-utilisateur) a servi de bras fixe pour les trois comparaisons. Un plan qui
  partirait d'un autre pipeline de référence, ou qui testerait le facteur inverse (repartir
  de C et changer un seul facteur vers B), pourrait en principe donner un ordre différent ;
  ce script ne teste que la direction B → {M, G, P}.
- La baseline Demographics Only recalculée sur ce pool de 120 (13,29 %) est nettement plus
  haute que celle recalculée sur le pool de 200 dans l'expérience précédente (9,20 %) : les
  120 personnes ne sont pas un sous-tirage stratifié indépendant, mais les 120 premiers index
  (par pid croissant) du tirage stratifié de 200 — même convention que les runs partiels
  précédents (n = 82, n = 142), mais qui peut légèrement déformer la composition par segment
  par rapport à un re-tirage propre à 120.

## 8. Phrase que l'article peut désormais écrire

> Un plan factoriel un-facteur-à-la-fois (n = 120, trois conditions dérivées d'un pipeline
> de référence en ne changeant que le modèle, que le gabarit de prompt, ou que le format de
> persona) montre qu'aucun des trois facteurs pris isolément ne suffit à préserver le canal
> inter-jumeaux mesuré en intra-équipe (36,4 %) : changer le modèle seul donne un top-1 de
> 0,7 % [0,0 ; 1,8], changer le gabarit de prompt seul donne 0,8 % [0,0 ; 2,1], changer le
> format de persona seul donne 2,7 % [0,5 ; 5,1] — les trois restent sous la baseline
> démographique recalculée sur le même échantillon (13,3 % [7,5 ; 19,3]) et dans le même
> ordre de grandeur que la configuration où les trois facteurs changent simultanément
> (1,8 % [0,4 ; 3,6]). Le canal jumeau-contre-jumeau qui atteint 36 % en intra-équipe ne
> survit à aucun changement isolé de pipeline testé ici ; sa fragilité n'est pas seulement
> une propriété de la combinaison complète modèle+gabarit+persona, mais de chacun de ces trois
> axes pris séparément — un praticien ne peut donc pas se fier à un seul de ces trois choix
> pour préserver ou casser délibérément ce canal, il faudrait les contrôler conjointement.
