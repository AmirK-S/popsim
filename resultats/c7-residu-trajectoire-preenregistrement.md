# C7-résidu-trajectoire : le résidu de 10× est-il réel ou un artefact ?

statut: courant
mandat: trancher si le residu de ~10x de la trajectoire 2023->2025, a nombre d'items apparie, est reel ou un artefact ; preenregistrement avant tout calcul
agent: mesures : residu de trajectoire, 13/09
ecriture: analyses/c7_residu_trajectoire.py, resultats/c7-residu-trajectoire-preenregistrement.md, resultats/c7-residu-trajectoire-resultats.md, resultats/c7-residu-trajectoire.csv
lecture_seule: tout le reste, en particulier analyses/c7_temoins_relecture.py (agent parallele)
interdits: appel d'API payant, reseau, recherche web, arriere-plan, fusion sur master
cout_reel_usd: 0.00

**Écrit le 13 septembre 2026, AVANT toute mesure d'attaque nouvelle.** Les seules
grandeurs citées en sections 0 à 2 sont (a) des chiffres déjà publiés ailleurs dans le
dépôt et (b) des statistiques calculées sur les **réponses humaines seules** de
Twin-2K-500 (aucune colonne de jumeau lue, aucun top-1 nouveau) — même discipline que
l'étape « préparation » de `analyses/c7_argyle.py`.

Étude de risque de vie privée sur deux jeux déjà publics (Twin-2K-500 ; Argyle et al.
2023, Harvard Dataverse `doi:10.7910/DVN/JPV20K`, CC0). Aucun identifiant ANES ni
Twin, aucun appariement individuel n'est imprimé ni écrit ; seuls des taux agrégés
sortent dans `resultats/c7-residu-trajectoire.csv`.

---

## 0. L'objet exact, et il est plus étroit que « la trajectoire »

`resultats/relecture-fond-2026-09-13.md` §D3 a construit le témoin qui manquait :
même jeu, même équipe, même modèle, même attaque, k items tirés au hasard parmi les 60
communs de Twin, 30 tirages.

| régime | top-1 jumeau | top-1 baseline démographique | rapport |
|---|---|---|---|
| Twin 2025, k = 60 | 20,694 % | 2,145 % | 9,6 |
| Twin 2025, k = 12 | 1,323 % (0,50–3,16 selon le tirage) | 0,309 % | **4,3** |
| Argyle 2023, 12 items | 0,135 % | 0,091 % | **1,5** |

Deux lectures coexistent dans le dépôt et il faut les séparer maintenant :

- **Le contraste brut** 0,135 % → 1,323 %, soit **≈ 10×** à nombre d'items apparié
  (contre ≈ 150× sans appariement : le nombre d'items explique un facteur 15,6).
- **Le contraste normalisé** 1,5 → 4,3, soit **≈ 2,9×** en rapport à la baseline
  démographique de chaque jeu.

C'est ce reliquat, et lui seul, que ce rapport doit trancher.

**Le fait gênant, connu avant d'écrire cette ligne, et qui doit être posé d'emblée.**
`resultats/c7-argyle-resultats.md` §4 établit que les **trois** jumeaux GPT-3 d'Argyle
**échouent au contrôle d'interprétabilité** : leurs IC bootstrap 95 % chevauchent celui
de la baseline démographique recalculée sur leur propre bassin (0,14 % [0,05;0,27]
contre 0,10 % [0,02;0,23]). Le 0,135 % qui sert de **dénominateur** au contraste de 10×
est donc un chiffre que la règle de décision n°1 du projet interdit d'interpréter.
`relecture-fond` §D2 le confirme sous l'attaquant fort (0,186 % contre baseline
0,093 %, contrôle toujours en échec) et §D9 montre que ce même chiffre est de surcroît
une **convention de départage** des ex æquo, à l'intérieur d'une plage de facteur 13
(0,0466 % à 0,6052 %).

Cela ne dispense pas de chercher les artefacts du côté Twin — c'est l'objet des
sections suivantes — mais cela fixe déjà une contrainte sur ce que la mesure pourra
autoriser à écrire, et cette contrainte est posée **avant** le calcul.

## 1. Les six artefacts candidats, et lequel est mesurable

| # | artefact | mesurable localement ? | comment |
|---|---|---|---|
| A1 | **items effectifs** (et non leur nombre brut) | **oui** | V̄ de Cramér et n_eff calculés sur chaque sous-ensemble Twin tiré ; appariement à n_eff(Argyle) = 4,31 |
| A2 | **taille du bassin** | **oui, partiellement** | sous-échantillonnage du bassin Argyle 2 148 → 2 058 et des deux bassins → 1 500, 20 tirages |
| A3 | **plafond de fiabilité humaine** (test-retest) | **non des deux côtés** | Twin oui (vagues 1-3 contre vague 4) ; ANES 2016 n'a **pas** de remesure des mêmes items — substitut B-oracle, déclaré comme substitut |
| A4 | **nature des items** (modalités, entropie) | **oui** | entropie humaine par item et totale, nombre de modalités, des deux côtés ; appariement en bits |
| A5 | **non-réponse et couverture** | **oui** | taux de manquants sur les items réellement utilisés |
| A6 | **la population elle-même** (ANES 2016 vs Twin) | **non** | confondu irréductible, nommé, non neutralisé |

Entrées déjà en main, côté humains seuls (aucune colonne de jumeau lue) :

| grandeur (humains seuls) | Twin, 60 items communs | Argyle, 12 items |
|---|---|---|
| bassin | 2 058 | 2 148 |
| manquants sur les items utilisés | **0,0000 %** | 0 % par construction (bassin = lignes pleines) |
| modalités par item (médiane / max) | 2 / 7 | à recalculer (l'âge en compte 73) |
| entropie moyenne par item | **1,349 bit** | 1,775 bit (21,30 / 12, `c7-argyle-resultats.md` §6) |
| entropie humaine totale | **80,91 bits** | **21,30 bits** |
| V̄ de Cramér | 0,0834 | **0,1620** |
| items effectifs | 10,13 | **4,31** |
| accord test-retest humain | **74,47 %** | **non mesurable** (pas de remesure ANES) |

## 2. Trois régimes d'appariement, et ils ne pointent pas dans le même sens

Apparier le **nombre brut** d'items (k = 12) n'apparie ni l'information indépendante ni
l'information totale. Trois appariements distincts sont possibles et seront tous les
trois calculés, précisément parce qu'ils ne donnent pas le même k :

- **M1 — items bruts appariés**, k = 12. Le témoin déjà construit ; refait ici avec un
  IC, qu'il n'avait pas (sa dispersion 0,50–3,16 % entre tirages est sa faiblesse
  principale).
- **M2 — items effectifs appariés**, n_eff = 4,31. Avec V̄(Twin) = 0,0834, la formule
  n_eff = k/(1+(k−1)·V̄) donne **k ≈ 6**. C'est l'appariement demandé par la mission ;
  il va dans le sens de **moins** d'items Twin.
- **M3 — information effective en bits appariée**, n_eff × H̄ = 4,31 × 1,775 =
  **7,65 bits** effectifs. Côté Twin, 7,65 / 1,349 = 5,67 items effectifs →
  **k ≈ 8**. Régime intermédiaire qui apparie A1 et A4 **simultanément**.

Pour mémoire, un quatrième appariement, l'**entropie humaine brute** (21,30 bits), irait
dans le sens **inverse** — k ≈ 16 items Twin. Il sera reporté pour l'honnêteté de la
fourchette, mais il n'apparie ni la redondance ni la taille du bassin et n'est pas la
mesure retenue pour le verdict.

Pour chaque k, n_eff et H seront **recalculés sur le sous-ensemble réellement tiré**,
jamais extrapolés par la formule : l'interpolation sur (n_eff observé, top-1 observé)
donnera la valeur au point d'appariement exact.

## 3. Prédiction chiffrée, préenregistrée

Écrite avant exécution. Intervalles de prédiction, pas des IC.

| grandeur à M2 (n_eff = 4,31, k ≈ 6, bassin 2 058) | prédiction | intervalle |
|---|---|---|
| top-1 jumeau `JSON Persona - GPT4.1` | **0,55 %** | [0,25 ; 1,20] |
| top-1 baseline `Demographics Only` | **0,20 %** | [0,08 ; 0,45] |
| rapport à la baseline | **2,7** | [1,3 ; 5,0] |
| contrôle d'interprétabilité à M2 | **ÉCHEC attendu** (IC chevauchants) | — |
| rapport à la baseline à M3 (k ≈ 8) | **3,2** | [1,6 ; 5,5] |
| invariance du rapport à la taille du bassin (A2) | rapport stable à ±20 % entre N = 2 058 et N = 1 500 | — |

**Je prédis donc que le résidu s'amenuise mais ne disparaît pas en valeur ponctuelle,
et qu'il cesse en revanche d'être interprétable** — parce que le contrôle
d'interprétabilité tombe des deux côtés une fois l'information effective appariée. Si
c'est ce qui se produit, la bonne conclusion n'est pas « le résidu est réel » mais
« à information appariée, aucun des deux bouts ne porte de personne démontrable ».

## 4. Règle de décision, et surtout : ce qui me ferait conclure à l'artefact

Appliquée dans cet ordre, sans exception.

**R0 — le contrôle avant toute interprétation.** `controle_avant_interpretation` est
appelé à chaque régime, des deux côtés, avec la baseline **recalculée sur le bassin et
les items exactement attaqués** (la fonction n'accepte aucune valeur de baseline en
argument). Un top-1 dont le contrôle échoue n'est **jamais** utilisé comme numérateur ni
comme dénominateur d'un rapport publié.

**R1 — le résidu est un ARTEFACT** si l'une des conditions suivantes est remplie :
- (a) à M2 **ou** à M3, le jumeau Twin **échoue** son propre contrôle d'interprétabilité
  (IC chevauchant celui de sa baseline sur le même bassin et les mêmes items) — le
  résidu est alors fabriqué par l'excédent d'information effective de Twin, pas par
  l'époque ;
- (b) l'IC 95 % du rapport à la baseline de Twin à M2 **contient 1,5** (la valeur
  d'Argyle) ;
- (c) le rapport se révèle fortement dépendant de la taille du bassin (variation > 2×
  entre N = 2 058 et N = 1 500), auquel cas A2 seul suffit à produire le contraste.

**R2 — le résidu est RÉEL** seulement si **toutes** les conditions suivantes tiennent :
- le jumeau Twin **passe** le contrôle à M2 **et** à M3 ;
- l'IC 95 % de son rapport à la baseline **exclut 1,5** aux deux régimes ;
- le rapport est stable sous variation du bassin (A2) ;
- et la conclusion est explicitement bornée par A3 et A6, non neutralisables.

**R3 — le résidu est INDÉCIDABLE EN AMPLITUDE, quel que soit le reste.** Le dénominateur
du contraste de 10× (0,135 %, Argyle) échoue son propre contrôle (§0) et dépend d'une
convention de départage sur une plage de facteur 13. Aucun chiffre calculé ici ne peut
rendre défini un rapport dont le dénominateur est du bruit. **Cette clause s'applique
même si R2 est entièrement satisfaite** : dans ce cas la seule chose qui survit est
l'**asymétrie qualitative** — un bout passe le contrôle, l'autre ne le passe pas — et
non son amplitude.

**R4 — non neutralisables, à déclarer quoi qu'il arrive** : A3 côté ANES (pas de
test-retest) et A6 (deux populations, deux époques). Si l'un des deux suffit à
expliquer le résidu et qu'il n'est pas mesurable, la réponse est « indécidable », pas
« réel ».

## 5. Protocole exact

Script : `analyses/c7_residu_trajectoire.py`. Graine **20260913**. `.venv/bin/python`.
Aucun appel de modèle, aucune dépense, aucun réseau. Lecture seule sur `data/`.

Repris tel quel, sans une ligne recopiée :
`t1_commun.charger` ; `c7_reidentification.{items_communs, rangs_attaque, resume_taux,
graine_nom, REF_V4, REF_V13, DEMO, N_BOOTSTRAP}` ; `a2_commun.distance_hamming` ;
`c7_bits.entropie_item` ; `c7_argyle.{charger, baseline_demographique, baseline_oracle,
cramer_v, items_effectifs, attaquer, controle_avant_interpretation}` ;
`c7_controle_interpretabilite.controle_avant_interpretation` côté Twin.

Nouveau ici, et rien d'autre : le tirage de sous-ensembles d'items avec **mesure** de
n_eff et de l'entropie sur le sous-ensemble tiré, l'interpolation au point
d'appariement, et la mise en regard des deux jeux à information appariée.

Jumeau Twin retenu : **`JSON Persona - GPT4.1`**, le même que le témoin de
`relecture-fond` §D3, pour comparabilité directe. Baseline Twin :
`Demographics Only - GPT4.1-mini`, recalculée sur les mêmes items à chaque régime.
Jumeau Argyle retenu : les trois versions, la température principale en tête.

Tirages : 30 sous-ensembles par k, k ∈ {4, 6, 8, 10, 12, 16, 20, 30, 40, 60}.
IC : bootstrap 95 % sur les personnes, 2 000 tirages, agrégé **sur l'ensemble des
tirages d'items** (l'incertitude publiée doit inclure la variance du tirage d'items,
que le témoin de `relecture-fond` ne publiait pas).

Sorties : `resultats/c7-residu-trajectoire.csv`,
`resultats/c7-residu-trajectoire-resultats.md`.

**Réduction déclarée d'avance** : si le temps de calcul de la baseline `_imputer_loo`
d'Argyle (O(n²) par item) ou du bootstrap dépasse le raisonnable en avant-plan, le
nombre de tirages d'items sera réduit de 30 à 10 et le nombre de sous-échantillons de
bassin de 20 à 10 ; la réduction sera écrite dans le rapport de résultats, avec le
chiffre exact.
