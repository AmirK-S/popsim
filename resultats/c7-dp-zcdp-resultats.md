# Confidentialité différentielle remesurée : mécanisme gaussien zCDP, référence appariée

statut: courant
mandat: Rendre opposables les cinq grandeurs que la passe T5 a refuse d'ecrire au §6.2 (0,9-1,0 ; 2,7-2,9 ; 0,1-0,3 ; 4,50-4,55 ; 0,09 %) : reconstruire la mesure DP sous mecanisme gaussien zCDP avec reference appariee, dans un script versionne, et declarer chaque valeur au registre
agent: Claude Opus 5, sous-agent correction chiffres DP opposables
ecriture: analyses/c7_dp_zcdp.py, resultats/c7-dp-zcdp.csv, resultats/c7-dp-zcdp-resultats.md, resultats/registre-chiffres.csv (lignes ajoutees)
lecture_seule: tout le reste
interdits: appel paye, reseau, commit sur master, arriere-plan, toute modification de article/manuscrit.md et resultats/article-synthese.md (deux autres agents en sont proprietaires)
cecite: n'a pas vu les scripts jetables de l'audit (hors depot, non conserves) ; n'a pas relu le manuscrit ni la synthese
cout_reel_usd: 0.00

Les cinq grandeurs que la passe T5 a refusé d'écrire au §6.2 du manuscrit — 0,9-1,0 ;
2,7-2,9 ; 0,1-0,3 ; 4,50-4,55 ; 0,09 % — venaient de scripts jetables hors dépôt
(`resultats/audit-comparaison-dp-2026-09-13.md`, §Traçabilité) et n'existaient dans aucun
CSV. **Le refus était juste.** Ce rapport les reconstruit dans le dépôt, à graine fixée,
sur 10 réplicats, par `analyses/c7_dp_zcdp.py` → `resultats/c7-dp-zcdp.csv`.

Aucune valeur du §8 n'a été recopiée. Le §8 est entré dans le script comme jeu de valeurs
**attendues**, comparé au run à la fin. Quatre des cinq grandeurs se reproduisent ; **une
est abandonnée** et **deux voient leur intervalle publiable se déplacer**.

**Ce rapport ne compare pas D4 à la confidentialité différentielle, dans aucun sens.** Il
établit une seule chose : de combien notre implémentation DP de référence
(`analyses/c7_dp.py`) était trop faible.

---

## 1. Les deux corrections, et rien d'autre

`analyses/c7_dp_zcdp.py` diffère de `analyses/c7_dp.py` sur exactement deux points.
Métriques, items, bassin, attaque et bootstrap sont importés inchangés.

**(1) Mécanisme.** Laplace avec composition séquentielle basique (`eps_item = eps/60`)
devient gaussien composé sous zCDP, δ = 1e-6. Sensibilité L2 = √2 par histogramme d'item
sous remplacement d'une personne ; ρ_total = 60·Δ₂²/(2σ²) ; conversion
ρ → (ε, δ) par la borne standard, inversée en ρ = (√(ε+ln(1/δ)) − √(ln(1/δ)))².

| ε | ρ | σ gaussien | σ effectif de `c7_dp.py` | rapport |
|---|---|---|---|---|
| 1 | 0,0175 | 58,61 | 169,71 | **2,90×** |
| 3 | 0,1473 | 20,18 | 56,57 | **2,80×** |
| 10 | 1,3530 | 6,66 | 16,97 | **2,55×** |

Le σ = 20,2 et le σ = 56,6 annoncés par l'audit se reproduisent au chiffre près
(20,185 et 56,569). Rien de ce mécanisme n'est exotique : c'est ce qu'un praticien emploie.

**(2) Référence appariée.** `c7_dp.py` ajuste le générateur sur les 2 058 **humains**
(ligne 148) et note son utilité contre le **jumeau** (ligne 152) ; il facture donc à la DP
l'écart humains↔jumeau. Ici le générateur est ajusté sur le **jumeau** — le même objet que
D4 protège — et noté contre le jumeau. L'écart humains↔jumeau que ce désappariement
facturait vaut, mesuré dans ce run : **3,118** points sur la distribution, 2,173 sur les
groupes, 5,775 sur les corrélations.

Le CSV porte, **pour chaque tirage**, la mesure appariée *et* la mesure désappariée contre
les humains. Le désappariement n'est donc pas à démontrer par raisonnement : il se lit dans
le fichier, colonne `reference`.

**Le point de contrôle ε = ∞** — même générateur, aucun bruit — est mesuré comme les
autres. Il était déjà dans `c7-dp-resultats.csv` et personne ne l'a lu avant de conclure.

---

## 2. Les trois composantes, référence appariée, 10 réplicats

Moyenne ± écart-type inter-graines, étendue [min ; max] des 10 réplicats, en points.

| ε | distribution | groupes | corrélations |
|---|---|---|---|
| 1 | 1,860 ± 0,233 [1,470 ; 2,194] | 2,678 ± 0,341 [2,157 ; 3,309] | 4,550 ± 0,068 [4,468 ; 4,684] |
| 3 | 1,039 ± 0,121 [0,854 ; 1,234] | 2,636 ± 0,347 [1,957 ; 3,140] | 4,597 ± 0,059 [4,506 ; 4,725] |
| 10 | 0,888 ± 0,073 [0,770 ; 0,969] | 2,788 ± 0,230 [2,484 ; 3,189] | 4,548 ± 0,095 [4,365 ; 4,690] |
| **∞ (aucune DP)** | **0,877 ± 0,075** | **2,637 ± 0,352** | **4,495 ± 0,072** |

Le témoin sans confidentialité est **indiscernable** de ε = 10 sur les trois composantes,
et meilleur que ε = 3 sur la distribution. Ce qui est mesuré est le coût de l'hypothèse
d'indépendance entre items (PrivBayes degré 0), pas celui du budget.

### Contribution marginale du budget — composante(ε) − composante(∞), appariée par réplicat

Même indice de réplicat des deux côtés : les tirages d'échantillonnage sont les mêmes une
fois le bruit retiré. Moyenne [min ; max] sur les 10 couples.

| ε | distribution | groupes | corrélations |
|---|---|---|---|
| 1 | +0,983 [+0,582 ; +1,324] | +0,041 [−0,641 ; +1,058] | +0,055 [−0,044 ; +0,209] |
| 3 | **+0,162** [−0,123 ; +0,454] | −0,001 [−0,938 ; +0,732] | +0,102 [−0,031 ; +0,227] |
| 10 | +0,011 [−0,197 ; +0,188] | +0,151 [−0,391 ; +0,938] | +0,054 [−0,073 ; +0,212] |

À ε = 3, la plus grande contribution marginale sur les trois composantes est **0,16 point**,
et son étendue franchit zéro. À ε = 10, aucune composante ne dépasse 0,16 et toutes les
étendues franchissent zéro. À ε = 1 seulement, la distribution paie une contribution
réelle et nettement non nulle (+0,98, étendue entièrement positive).

### Plancher de destruction des corrélations

|corr| moyenne sur les 780 paires des 40 items d'achat du jumeau : **4,317**. C'est la note
qu'obtient, par définition, tout mécanisme qui détruit toute corrélation. Le générateur DP
obtient 4,50-4,60 : il n'en préserve rien. Ce rapport ne dit rien de ce que D4 obtient.

---

## 3. Confrontation au §8 de l'audit

Le §8 n'a pas de source opposable. En cas d'écart, **ce run fait foi**. Les dix valeurs du
§8 tombent toutes dans l'étendue des 10 réplicats — mais la moyenne se déplace assez pour
changer deux des intervalles arrondis que le §6.2 doit écrire.

| grandeur | §8 | run (moyenne) | écart | verdict |
|---|---|---|---|---|
| distribution ε=1 | 1,754 | 1,860 | +0,106 | dans l'étendue |
| distribution ε=3 | 0,997 | 1,039 | +0,042 | dans l'étendue |
| distribution ε=10 | 0,923 | 0,888 | −0,035 | dans l'étendue |
| distribution ε=∞ | 0,837 | 0,877 | +0,040 | dans l'étendue |
| groupes ε=1 | 2,627 | 2,678 | +0,051 | dans l'étendue |
| groupes ε=3 | 2,932 | 2,636 | **−0,296** | dans l'étendue, mais déplace l'intervalle |
| groupes ε=10 | 2,673 | 2,788 | +0,115 | dans l'étendue |
| corrélations ε=1 | 4,506 | 4,550 | +0,044 | dans l'étendue |
| corrélations ε=3 | 4,549 | 4,597 | +0,048 | dans l'étendue |
| corrélations ε=10 | 4,603 | 4,548 | −0,055 | dans l'étendue |
| σ gaussien ε=3 | 20,2 | 20,185 | — | reproduit |
| σ Laplace ε=3 | 56,6 | 56,569 | — | reproduit |

**Les deux intervalles qui se déplacent, et qu'il faut donc réécrire :**

- **« 2,7 à 2,9 » sur les groupes devient « 2,6 à 2,8 »** (ε = 3 → 2,64 ; ε = 10 → 2,79).
  Le §8 avait manifestement tiré son 2,932 du haut d'une étendue large : l'écart-type
  inter-graines de cette composante vaut 0,23-0,35, soit l'ordre de grandeur de la
  différence elle-même. Cette composante ne supporte pas trois chiffres significatifs.
- **« 4,50 à 4,55 » sur les corrélations devient « 4,50 à 4,60 »** (ε = 3 → 4,597 ;
  ε = 10 → 4,548 ; ε = 1 → 4,550). L'écart est sans conséquence de fond : les trois
  valeurs restent au-dessus du plancher de destruction 4,317.

**Les deux intervalles qui tiennent :**

- **« 0,9 à 1,0 » sur la distribution** tient (ε = 10 → 0,89 ; ε = 3 → 1,04). Les deux
  bornes sont au registre à deux décimales, `dp-zcdp-distribution-eps10` et
  `dp-zcdp-distribution-eps3` ; le §6.2 cite les renvois et n'arrondit pas lui-même. Une
  troisième décimale serait du faux précis devant un écart-type inter-graines de 0,12.
- **« 0,1 à 0,3 point à ε = 3 »** ne tient pas tel quel : le run donne au plus **0,16**
  point sur les trois composantes, avec une étendue qui franchit zéro. La formulation
  publiable est **« au plus 0,2 point à ε = 3, et indiscernable de zéro à ε = 10 »**.
  C'est plus faible que le §8, et dans le sens qui renforce la conclusion : le budget de
  confidentialité contribue encore moins au coût que l'audit ne le disait.

---

## 4. La grandeur abandonnée : le « 0,09 % » du §8

**Abandonnée. Aucune ligne de registre `courant` ne la porte, et le §6.2 doit s'en passer.**

Le §8 écrit : « un attaquant qui écarte le bloc brouillé porte la fuite de D4 de 0,13 % à
0,24 %, au-dessus du générateur DP à ε = 3 (0,09 %) ». Ce 0,09 % n'est pas reproductible
comme grandeur stable, pour deux raisons cumulées.

**Première raison : c'est du hasard.** Le hasard vaut 1/2 058 = **0,049 %**. Sur 10
réplicats du générateur ajusté sur le jumeau, l'attaque naïve par accord de Hamming donne :

| ε | top-1 | hasard |
|---|---|---|
| 1 | 0,079 % [0,000 ; 0,357] | 0,049 % |
| 3 | 0,054 % [0,000 ; 0,287] | 0,049 % |
| 10 | 0,046 % [0,000 ; 0,277] | 0,049 % |
| **∞ (aucune DP)** | **0,052 %** [0,000 ; 0,272] | 0,049 % |

Les quatre valeurs sont le hasard, le témoin **sans aucune confidentialité** compris. Un
générateur qui tire chaque item indépendamment n'a aucune correspondance individuelle à
fuir : ce top-1 mesure l'architecture, jamais le budget, et ne peut soutenir aucun
classement. La suite en ε est non monotone et tous les intervalles se recouvrent.

**Seconde raison : le 0,09 % vient de l'architecture désappariée.** Témoin mesuré ici
(bloc `risque_temoin_ajuste_humains` du CSV), générateur ajusté sur les **humains** comme
dans `c7_dp.py`, attaqué contre les humains : 0,033 % à ε = 3 et 0,062 % à ε = ∞. Là encore
le hasard, et là encore non monotone. Le 0,085 % du §8 est **un tirage** d'une quantité
dont la dispersion couvre tout cet intervalle.

Conséquence pour le §6.2 : la phrase sur l'attaquant adaptatif doit citer les taux de D4,
qui sont au registre (`defense-d4-top1-adaptatif-s1`, `defense-d4-top1-opinion-naif`), et
**s'arrêter là**. Elle ne peut pas les comparer à un taux DP, puisque le taux DP est le
hasard. Formulation de remplacement au §6 ci-dessous.

---

## 5. Recherche active d'un désappariement résiduel dans cette mesure

La consigne était explicite : si la DP corrigée coûtait *encore plus cher* que D4, ce
serait le signe d'un désappariement reproduit, pas une bonne nouvelle. Trois contrôles.

**(a) Garde-fou en fin de script.** Sur le témoin ε = ∞, composante distribution : mesure
appariée **0,877** contre mesure désappariée **3,235**, pour un écart humains↔jumeau de
**3,118**. La mesure désappariée est, à 0,12 point près, l'écart de référence lui-même : le
générateur non bruité reproduit les marginales de ce sur quoi il est ajusté, et la
composante désappariée n'est *que* la facture de référence. La mesure appariée est à 28 %
de celle-là. Le désappariement de F3 est retiré, et le script échouerait bruyamment si
l'ordre s'inversait.

**(b) Les trois composantes chutent du bon facteur.** Distribution 3,11/3,21 (publié) →
1,04/0,89, division par 3,0 à 3,6. C'est l'ordre de grandeur attendu quand on retire
3,118 points de facture de référence d'une quantité de 3,2.

**(c) Ce qui ne chute pas, et pourquoi ce n'est pas un désappariement.** Les corrélations
restent à 4,50-4,60, quasi inchangées par rapport au publié (4,47-4,59). Ce n'est pas un
désappariement résiduel : l'écart humains↔jumeau sur les corrélations vaut 5,775, donc s'il
en restait quelque chose la composante appariée serait *plus haute*, pas égale. Elle est
égale parce que les deux références ont la même amplitude de corrélations à détruire
(plancher 4,317) et que le générateur les détruit toutes les deux entièrement. De même les
groupes : 2,64-2,79 apparié contre 2,55-2,65 désapparié — les deux sont proches parce que
l'écart humains↔jumeau sur cette composante est petit (2,173) et que le générateur i.i.d.
manque les écarts inter-segments dans les deux cas.

**Aucun signe de désappariement résiduel.** Le seul reste est un coût authentique : à
2 058 personnes et 40 segments de taille médiane 24, un générateur à marginales d'item
indépendantes ne reproduit pas les écarts inter-segments, quel que soit ε — le témoin ε = ∞
les manque autant que ε = 3.

---

## 6. Fiche de report pour le §6.2 — à appliquer par la passe finale

**Ce fichier ne touche pas au manuscrit.** Pour chaque valeur : l'`id` de registre à citer
sous forme de renvoi de registre, et la formulation exacte à insérer.

### 6.1 Table de report

| valeur du §8 | statut | `id` de registre à citer |
|---|---|---|
| 0,9 (distribution, ε=10) | reproduite | `dp-zcdp-distribution-eps10` |
| 1,0 (distribution, ε=3) | reproduite | `dp-zcdp-distribution-eps3` |
| (témoin, distribution, ε=∞) | reproduite | `dp-zcdp-distribution-epsinf` |
| 2,7-2,9 (groupes) | **déplacée → 2,6-2,8** | `dp-zcdp-groupes-eps3`, `dp-zcdp-groupes-eps10` |
| (témoin, groupes, ε=∞) | reproduite | `dp-zcdp-groupes-epsinf` |
| 4,50-4,55 (corrélations) | **déplacée → 4,50-4,60** | `dp-zcdp-correlations-eps3`, `dp-zcdp-correlations-eps10` |
| 4,32 (plancher de destruction) | reproduite | `dp-zcdp-plancher-correlations` |
| 0,1-0,3 (contribution du budget) | **affaiblie → au plus 0,2** | `dp-zcdp-contribution-budget-eps3` |
| (contribution du budget, ε=10) | reproduite | `dp-zcdp-contribution-budget-eps10` |
| 0,09 % (top-1 DP) | **ABANDONNÉE** | aucun — voir `dp-zcdp-top1-eps3` (hasard) |
| 2,8× (bruit gaussien vs Laplace) | reproduite | `dp-zcdp-rapport-bruit-eps3` |
| 3,118 (écart humains↔jumeau) | reproduite | `dp-zcdp-ecart-humains-jumeau-distribution` |

### 6.2 Texte à insérer au §6.2, en remplacement du texte du §8 de l'audit

> Nous n'avons pas comparé le coût de la confidentialité différentielle à celui de D4.
> Notre première implémentation de référence était trop faible sur deux points : elle
> employait le mécanisme de Laplace sous composition séquentielle basique, là où le
> mécanisme gaussien composé sous zCDP (δ = 1e-6) injecte {{R:dp-zcdp-rapport-bruit-eps3}}
> fois moins de bruit au même ε = 3 ; et elle ajustait le générateur sur les humains pour
> le noter contre le jumeau, lui facturant ainsi l'écart entre ces deux références, qui
> vaut à lui seul {{R:dp-zcdp-ecart-humains-jumeau-distribution}} points de distribution.
> Corrigée de ces deux points, sur ces 2 058 personnes et sur dix réplicats, un générateur
> synthétique à marginales d'item indépendantes coûte
> {{R:dp-zcdp-distribution-eps10}} à {{R:dp-zcdp-distribution-eps3}} points d'erreur de
> distribution et {{R:dp-zcdp-groupes-eps3}} à {{R:dp-zcdp-groupes-eps10}} points sur les
> écarts entre segments — qu'il soit bruité à ε = 3, à ε = 10, ou **pas bruité du tout** :
> le même générateur sans aucune confidentialité coûte
> {{R:dp-zcdp-distribution-epsinf}} et {{R:dp-zcdp-groupes-epsinf}} points. Le coût mesuré est
> celui de l'hypothèse d'indépendance entre items ; la contribution marginale du budget de
> confidentialité est d'au plus {{R:dp-zcdp-contribution-budget-eps3}} point à ε = 3 et
> indiscernable de zéro à ε = 10 ({{R:dp-zcdp-contribution-budget-eps10}}). Sur les
> corrélations, le générateur DP obtient {{R:dp-zcdp-correlations-eps10}} à
> {{R:dp-zcdp-correlations-eps3}} alors que l'amplitude à préserver vaut
> {{R:dp-zcdp-plancher-correlations}} : il n'en préserve rien. D4 n'offre, lui, aucune
> garantie formelle : il republie exactement l'histogramme de chaque item à l'intérieur de
> chaque segment ({{R:defense-d4-republication-multiensemble}} % des couples segment × item),
> de sorte qu'un adversaire connaissant les autres membres du segment reconstitue les 40
> réponses de la cible ; ses erreurs de distribution et de groupe nulles sont cette
> republication exacte, non un avantage. Enfin notre top-1 mesure un attaquant fixé : un
> attaquant qui écarte le bloc brouillé porte la fuite de D4 à
> {{R:defense-d4-top1-adaptatif-s1}} %, et ces taux correspondent à 0 à 3 personnes sur
> 2 058. **Nous ne revendiquons aucune supériorité de D4 sur la confidentialité
> différentielle**, seulement un compromis différent, sans garantie, contre l'attaque
> particulière que nous avons construite.

### 6.3 Les trois écarts au §8 que la passe finale doit connaître

1. **Ne pas écrire « 2,7 à 2,9 »** sur les groupes : écrire les deux renvois de registre,
   qui valent 2,64 et 2,79. La valeur 2,932 du §8 n'est pas reproduite.
2. **Ne pas écrire « 4,50 à 4,55 »** sur les corrélations : la borne haute reproduite est
   4,60.
3. **Ne pas écrire « 0,09 % »** pour le générateur DP, ni aucune phrase qui compare le
   top-1 de D4 à un top-1 DP. Le top-1 du générateur DP est le hasard (§4), y compris sans
   aucune confidentialité. La phrase de remplacement, ci-dessus, s'arrête au taux de D4.
4. **Ne pas écrire « 0,1 à 0,3 »** : écrire « au plus 0,2 point à ε = 3 ».

---

## 7. Limites de ce travail

- **Le mécanisme reste PrivBayes degré 0.** Aucune structure jointe n'est apprise, donc
  aucune corrélation ni écart inter-segments ne peut survivre, quel que soit ε. Un
  générateur DP qui apprendrait un graphe de dépendances n'a pas été testé ici ; il
  paierait son apprentissage en budget mais pourrait préserver de la structure. Ce rapport
  ne dit donc pas ce que « la DP » coûte, seulement ce que **cette architecture** coûte.
- **Aucune bibliothèque de référence n'est installée** : la comptabilité zCDP est écrite à
  la main dans `rho_depuis_eps_delta` / `sigma_gaussien`, documentée ligne à ligne, et
  reproduit les σ annoncés par l'audit. Elle n'a pas été confrontée à une implémentation
  tierce.
- **La borne zCDP → (ε, δ) employée est la borne standard**, pas la plus fine connue. Une
  conversion plus fine donnerait *moins* de bruit encore, donc un coût encore plus bas :
  toutes les valeurs de ce rapport sont conservatrices dans le sens défavorable à la DP.
- **Les marginales par segment** (composition parallèle, gratuite en ε) n'ont pas été
  reproduites ici ; l'audit les a testées et écartées (elles aggravent l'erreur de
  groupes). Ce rapport ne les source donc pas, et le §6.2 ne doit pas les citer.
- **10 réplicats** pour l'utilité comme pour le risque. L'écart-type inter-graines de la
  composante groupes (0,23-0,35) reste du même ordre que les différences entre ε : cette
  composante ne supporte pas mieux que deux chiffres significatifs.

---

## 8. Reproduction

    .venv/bin/python analyses/c7_dp_zcdp.py

Graine 20260913, 10 réplicats, bassin constant (les 2 058 personnes couvertes par
`JSON Persona - GPT4.1`), 60 items communs dont 40 d'achat. Durée observée : 7 min 28 s
sur la machine de développement, dont environ 6 min pour les 44 attaques top-1 (bootstrap
2 000 personnes chacune). Aucune donnée individuelle n'est imprimée ni écrite ; aucun appel
de modèle de langage ; aucun accès réseau.

Sortie : `resultats/c7-dp-zcdp.csv`, 177 lignes, blocs `replicat`, `resume`,
`contribution_marginale_budget`, `reference`, `mecanisme`, `risque`,
`risque_temoin_ajuste_humains`.
