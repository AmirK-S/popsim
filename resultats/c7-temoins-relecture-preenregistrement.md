# C7 — Témoins de relecture : préenregistrement écrit APRÈS coup, et qui le dit

statut: courant
mandat: T1a : reimplementer independamment les deux temoins de la relecture hostile du 13/09 (items apparies sur Twin, attaquant fort sur Argyle), appliquer le controle d'interpretabilite, rapporter mes propres chiffres avec IC bootstrap sur les personnes, et les declarer post-hoc et non preenregistres
agent: mesures / temoins de relecture (T1a), 13/09
ecriture: analyses/c7_temoins_relecture.py, resultats/c7-temoins-relecture-preenregistrement.md, resultats/c7-temoins-relecture-resultats.md, resultats/c7-temoins-relecture.csv
lecture_seule: tout le reste
interdits: appel payant, reseau, recherche web, commit sur master, fusion, ecriture hors des quatre fichiers du mandat
cout_reel_usd: 0.00

## Avertissement liminaire, à lire avant tout le reste

**Ce fichier n'est pas un préenregistrement au sens où ce dépôt emploie ce mot
partout ailleurs.** Il documente une analyse **déjà faite**. Les deux témoins qu'il
décrit ont été construits par un relecteur hostile, après lecture du PDF de soumission
et de ses résultats (`resultats/relecture-fond-2026-09-13.md`, défauts D2 et D3), puis
réimplémentés indépendamment ici. Aucun plan n'existait avant eux.

Le dépôt appelle « préenregistrement » un document écrit **avant** le premier calcul,
et il en fait un argument de crédibilité — quatorze prédictions réfutées sont tabulées
dans le manuscrit sur cette base. Il serait exactement le défaut que ce dispositif
prétend corriger que d'introduire silencieusement, dans le même article, des mesures
construites après coup sous un nom qui laisse croire le contraire.

Donc, en toutes lettres, et à reproduire partout où ces chiffres apparaissent :

> **Les deux témoins de ce fichier sont POST HOC et NON PRÉENREGISTRÉS.** Ils ont été
> conçus après avoir vu les résultats qu'ils mesurent, en réponse à une relecture
> adverse. Ils ne comptent dans aucun dénominateur de multiplicité préenregistré, ils
> ne peuvent réfuter aucune prédiction préenregistrée, et le manuscrit doit les
> présenter comme tels.

Ce que ce fichier fixe malgré tout, et qui garde une valeur : le protocole est écrit
**avant la rédaction du fichier de résultats**, les graines sont fixées dans le code,
et la règle d'arrêt (§5) est posée avant de comparer quoi que ce soit aux chiffres du
relecteur. Ce qui n'est pas protégé ici — le choix des mesures — est déclaré comme
non protégé.

Décision de publication : option (a) de la décision D2 du plan de révision
(`resultats/plan-revision-2026-09-13.md`, §5) — publier, avec la mention explicite.
Cette décision est prise ; ce fichier l'exécute.

---

## 1. Pourquoi ces deux témoins, et pourquoi les deux

La relecture a construit deux témoins que le projet n'avait jamais faits. **Ils tirent
en sens opposés :**

| témoin | ce qu'il fait à la thèse de l'article |
|---|---|
| **T1 — nombre d'items apparié** | l'**affaiblit** : le seul nombre d'items vaut plus d'un ordre de grandeur de l'amplitude de la trajectoire |
| **T2 — attaquant fort sur Argyle** | la **renforce** : même armé de l'attaquant fort, le point 2023 reste au niveau de la baseline |

**Les deux sont mesurés, les deux sont rapportés, et aucun n'est choisi.** T1,
l'affaiblissant, est rapporté **en premier** — dans le script, dans le CSV et dans le
fichier de résultats. C'est une décision prise en amont (plan de révision, R1) pour que
la rédaction ne puisse pas privilégier le témoin qui arrange, et elle est exécutée ici
sans dérogation.

---

## 2. T1 — témoin à nombre d'items apparié (Twin-2K-500)

**Question.** Le §1.1 et le §7.2 du manuscrit écrivent que « rien de ce que nous
mesurons » ne sépare « le risque a grandi avec la capacité des modèles » de « les
protocoles diffèrent ». Le nombre d'items est-il séparable, à l'intérieur d'un seul
jeu ?

**Protocole.** Un seul jeu (Twin-2K-500), une seule équipe, un seul modèle
(`JSON Persona - GPT4.1`), une seule attaque (Hamming naïf, `rangs_attaque`), les mêmes
2 058 personnes, le même pool (`humains vague 4`). La **seule** chose qui varie d'un
point de la courbe à l'autre est **k**, le nombre d'items.

- k ∈ {12, 20, 30, 40, 60}, tirés sans remise parmi les 60 items toujours renseignés
  (`items_communs`). k = 60 est l'ensemble entier : un seul « tirage » possible.
- 30 tirages d'items indépendants par k < 60, graine fixée dans le code.
- Comparateur : `Demographics Only - GPT4.1-mini`, **mêmes** personnes, **mêmes** items
  tirés, **même** attaque — la baseline n'est jamais empruntée à un autre bassin ni à
  un autre nombre d'items (second piège de
  `resultats/controle-interpretabilite-2026-09-12.md`).

**Unités d'incertitude, séparées explicitement.** L'indicatrice top-1 de chaque
personne est moyennée sur les tirages d'items **avant** le bootstrap : l'unité de
rééchantillonnage reste la personne, jamais le tirage d'items.

1. **IC 95 % bootstrap sur les personnes** (2 000 tirages, `bootstrap_personnes`,
   graine fixée) — c'est l'intervalle demandé par le mandat.
2. **Étendue et écart-type entre tirages d'items** — rapportés **à part**, dans des
   colonnes distinctes du CSV.

Les deux ne mesurent pas la même chose et ne seront jamais présentés sous le même nom.
Les confondre est précisément le défaut D6 que la relecture reproche au §5.9.

**Sorties fixées d'avance.** top-1 et top-10 par k et par candidat ; rapport
jumeau / baseline par k ; facteur k = 12 → k = 60 pour les deux candidats ; contrôle
d'interprétabilité par k (§4).

**Réduction déclarée.** L'attaque naïve du dépôt moyenne 20 tirages de départage des
ex æquo. La courbe lance 242 attaques ; à 20 tirages elle dépasserait la demi-heure de
calcul. Elle tourne donc à **5 tirages de départage**, et elle seule ; k = 60, qui n'a
qu'un tirage d'items, garde les 20 tirages du dépôt, ce qui permet de vérifier que le
point de droite retombe bien sur les 20,694 % publiés. T2 garde 20 tirages partout.

---

## 3. T2 — l'attaquant fort appliqué à Argyle 2023

**Question.** Les deux bouts de la trajectoire publiée ne sont pas la même mesure
(défaut D2) : le bout gauche est un top-1 naïf en monde fermé, le bout droit une TPR à
1 % de FPR en monde ouvert sous l'attaquant fort. Que devient le bout gauche **dans la
métrique du bout droit** ?

**Protocole.** Jeu Argyle 2023 (`c7_argyle.charger`), 2 148 personnes complètes,
12 items. Trois jumeaux GPT-3 publiés par l'équipe Argyle, plus la baseline
démographique B-demo recalculée sur **ce** bassin (`baseline_demographique`).

Deux attaques, mêmes personnes, même pool :

- **naïve** (Hamming), pour le rappel ;
- **A-LLR hors pli** (`c7_attaquant_fort.scores_hors_pli`, importée sans
  modification) : c'est exactement la fonction qui a produit les 90,40 % de Park et les
  23,23 % de Twin.

Deux mondes :

- **monde fermé** : top-1 et top-10 (`rangs_depuis_accord`), IC bootstrap sur les
  personnes ;
- **monde ouvert** : `marges_deux_regimes` + `roc_et_taux`, inchangées — AUC,
  TPR à FPR = 1 %, TPR à FPR = 0,1 %.

**Sortie fixée d'avance.** Le gain relatif du fort sur le naïf par candidat, et la
comparaison de chaque jumeau à B-demo sous **la même** attaque.

---

## 4. Le contrôle d'interprétabilité, avant toute interprétation

C'est la leçon la plus chère du projet (`resultats/c7-reconciliation-facteurs-2026-09-12.md`).
Il est appliqué **avant** d'interpréter l'un ou l'autre témoin, et son verdict est
publié qu'il arrange ou non.

- **T1** : `c7_controle_interpretabilite.controle_avant_interpretation`, la fonction
  canonique, appelée telle quelle **à chaque k**. Elle ne prend jamais de valeur de
  baseline en argument : elle la recalcule elle-même sur le même bassin et les mêmes
  items. Comme k = 12 porte la conclusion « la trajectoire survit au témoin » et que
  l'étendue entre tirages d'items y couvre un facteur ~9, le contrôle y est rejoué sur
  **5 tirages d'items indépendants** et la part de tirages qui passent est rapportée.
- **T2** : `c7_argyle.controle_avant_interpretation`, qui reprend la règle de décision
  à l'identique pour un jeu qui n'est pas Twin, sous l'attaque naïve ; puis **la même
  règle sous A-LLR**, candidat et baseline tous deux sous l'attaquant fort.

Règle de décision, inchangée : le candidat passe si la borne basse de son IC 95 % est
**strictement** supérieure à la borne haute de l'IC de la baseline démographique
recalculée sur le même bassin. Test conservateur, choisi parce que le sinistre qu'il
prévient est un **faux positif**.

---

## 5. Règle d'arrêt et traitement des écarts avec le relecteur — posée avant comparaison

Le relecteur annonce, pour T1 : 1,323 % à k = 12, 20,694 % à k = 60, facteur **15,6**,
rapport à la baseline **4,3** contre **1,5** pour Argyle. Pour T2 : 0,149 → 0,186 %,
TPR à 1 % de FPR de **0,00 %**, ROC dégénérée.

**Ces valeurs ne sont pas des cibles.** La règle, posée ici avant toute comparaison :

1. Les chiffres publiés dans le fichier de résultats sont **les miens**, issus de
   `resultats/c7-temoins-relecture.csv`, jamais recopiés du rapport de relecture.
2. Tout écart avec le relecteur est **rapporté comme écart**, avec l'hypothèse la plus
   plausible sur son origine. **Aucun paramètre, aucune graine, aucun protocole ne sera
   modifié pour réduire un écart.**
3. Seul déclencheur d'arrêt et de remontée au responsable : un **renversement de sens**
   — le facteur k = 12 → 60 tomberait sous 2, ou un jumeau Argyle passerait le contrôle
   d'interprétabilité sous A-LLR. Un tel résultat contredirait le rapport de relecture
   *et* le manuscrit ; il ne serait pas publié sans arbitrage.
4. Le point k = 60 sert de **vérification de raccordement** : s'il ne retombe pas sur
   les 20,694 % publiés à la troisième décimale près, le portage est faux et tout le
   reste est suspect.

---

## 6. Périmètre, écritures, coût

**Écrit** : `analyses/c7_temoins_relecture.py`,
`resultats/c7-temoins-relecture-preenregistrement.md`,
`resultats/c7-temoins-relecture-resultats.md`, `resultats/c7-temoins-relecture.csv`.
**Rien d'autre.** Aucun script existant modifié.

**Dérivation indépendante.** Les scripts du relecteur (`temoin_trajectoire.py`,
`temoin_argyle_fort.py`, `recalc_argyle.py`) vivent dans son scratchpad, hors dépôt.
Aucune de leurs lignes n'a été lue ni recopiée : seule la **description** de ses deux
témoins, dans `resultats/relecture-fond-2026-09-13.md`, a servi de cahier des charges.
Deux dérivations indépendantes qui convergent valent mieux qu'une seule rejouée ; c'est
le seul intérêt de refaire ce travail plutôt que de recopier ses tableaux.

**Coût.** Aucun appel de modèle de langage, aucune dépense, aucun réseau, aucune
recherche web. Lecture seule sur `data/`. Tout le calcul est local.

**Ce qui n'est PAS fait ici** : les cinq autres mesures de la tâche T1a du plan de
révision (§1c classes d'ex æquo et Clopper-Pearson, §1d FPR = 0,1 % en escalier,
§1e Spearman sur les paires, §1f bootstrap en grappes du 36,4 %, §1g baseline
démographique en monde ouvert sous A-LLR). Elles sortent du périmètre confié et ne sont
ni mesurées ni approchées.
