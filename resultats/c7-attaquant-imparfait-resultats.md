# C7 attaquant imparfait : résultats (13 septembre 2026)

statut: courant
mandat: mesurer la reidentification C7 quand les donnees auxiliaires de l'attaquant se degradent (partielles, bruitees, items banals) et en situer le point de rupture
agent: Opus 5, Anthropic
ecriture: analyses/c7_attaquant_imparfait.py, resultats/c7-attaquant-imparfait-preenregistrement.md, resultats/c7-attaquant-imparfait-resultats.md, resultats/c7-attaquant-imparfait.csv
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0.0

Préenregistrement `resultats/c7-attaquant-imparfait-preenregistrement.md`, écrit et **commité seul
avant** le script et avant le moindre chiffre. Script `analyses/c7_attaquant_imparfait.py`, données
`resultats/c7-attaquant-imparfait.csv`. Aucun appel de modèle, aucun réseau, coût 0,00 USD. Aucun
identifiant, aucun appariement individuel : taux agrégés seuls.

**Contrôle de fidélité préalable appliqué avant toute interprétation**
(`c7_controle_interpretabilite.controle_avant_interpretation`, condition non dégradée, 2 058
personnes, 60 items) : **PASSE** — candidat 20,69 % [19,00 ; 22,40] contre baseline 2,15 %
[1,59 ; 2,79]. Ce chiffre reproduit le 20,68 % publié dans `c7-resultats.md`.

**Bassin rigoureusement constant** dans les 30 conditions : 2 058 personnes attaquées, pool de
2 058 candidats, 60 items de départ, `JSON Persona - GPT4.1`. La baseline `Demographics Only` est
recalculée **dans chaque condition, sur le pool exactement aussi dégradé**, avec le même masque et le
même bruit. Hasard : 0,0486 %.

**Réduction déclarée** (préenregistrement §9) : 5 tirages de départage des ex æquo au lieu de 20.
Coût mesuré : 20,57 % au lieu de 20,69 %, soit 0,12 point. Aucune autre réduction.

---

## 1. Le taux à chaque niveau de dégradation

Référence, données auxiliaires parfaites : **20,57 % [18,91 ; 22,27]**, baseline **2,07 %**
[1,51 ; 2,66].

### D1 — l'attaquant ne connaît qu'une fraction des items (tirage aléatoire)

| items connus | top-1 candidat | IC 95 % | baseline même dégradation | ratio | au-dessus ? |
|---|---|---|---|---|---|
| 100 % (60) | 20,57 % | [18,91 ; 22,27] | 2,07 % [1,51 ; 2,66] | 9,9 | oui |
| 75 % (45) | 12,91 % | [11,69 ; 14,55] | 1,31 % [0,67 ; 1,46] | 9,8 | oui |
| 50 % (30) | 6,04 % | [5,01 ; 6,96] | 0,77 % [0,52 ; 1,21] | 7,8 | oui |
| 25 % (15) | 1,81 % | [1,34 ; 2,33] | 0,36 % [0,15 ; 0,57] | 5,1 | oui |
| 10 % (6) | 0,35 % | [0,23 ; 0,49] | 0,16 % [0,08 ; 0,29] | 2,1 | **non — rupture** |

### D2 — une fraction des réponses connues est fausse (tous les items connus)

| erreurs | top-1 candidat | IC 95 % | baseline | ratio | au-dessus ? |
|---|---|---|---|---|---|
| 5 % | 15,05 % | [13,51 ; 16,47] | 1,65 % | 9,2 | oui |
| 10 % | 9,86 % | [8,27 ; 10,73] | 1,26 % | 7,9 | oui |
| 20 % | 4,24 % | [3,44 ; 5,13] | 0,56 % | 7,5 | oui |
| 30 % | 1,34 % | [0,86 ; 1,80] | 0,31 % | 4,4 | oui — **aucune rupture** |

### D3 — les deux combinés, la situation réelle

| items × erreurs | 10 % | 20 % | 30 % |
|---|---|---|---|
| **75 %** | 6,05 % [5,16 ; 7,08] | 2,68 % [1,86 ; 3,11] | 0,87 % [0,51 ; 1,22] |
| **50 %** | **3,25 % [2,64 ; 4,02]** | 1,45 % [1,05 ; 2,04] | 0,61 % — **rupture** |
| **25 %** | 0,98 % [0,54 ; 1,28] | 0,50 % — **rupture** | 0,26 % — rupture |

### D4 — l'attaquant ne connaît que les items les plus courants

| k items les plus banals | top-1 (entropie basse, préenregistré) | top-1 (fréquence modale, post hoc) | **D1 au même k** (aléatoire) |
|---|---|---|---|
| 45 | **30,25 % [28,37 ; 32,19]** | 31,21 % [29,40 ; 33,15] | 12,91 % |
| 30 | 20,92 % [19,22 ; 22,69] | 20,86 % [19,24 ; 22,52] | 6,04 % |
| 15 | 4,77 % [3,97 ; 5,62] | 4,58 % [3,78 ; 5,37] | 1,81 % |
| 6 | 0,30 % [0,19 ; 0,43] | 0,32 % — rupture | 0,35 % — rupture |

## 2. Le point de rupture

Règle préenregistrée : première dégradation où la borne basse de l'IC du candidat cesse d'être
strictement au-dessus de la borne haute de l'IC de la baseline **du même bassin et de la même
dégradation**.

- **Items partiels seuls : rupture à 10 % des items (6 sur 60).** À 25 % (15 items), l'attaque tient
  encore, à 1,81 % contre 0,36 % — cinq fois la baseline et trente-sept fois le hasard.
- **Bruit seul : aucune rupture jusqu'à 30 % de réponses fausses.** À 30 % d'erreurs sur les 60
  items, le taux vaut encore 1,34 %, soit 4,4 fois la baseline.
- **Combiné : rupture à {50 % des items, 30 % d'erreurs} et à {25 %, 20 %}.** Le point réaliste
  {50 % des items, 10 % d'erreurs} **tient** : 3,25 % contre une baseline de 0,71 %.
- **Items les plus courants : aucune rupture jusqu'à 15 items**, et le taux y est **plus élevé**
  qu'avec un tirage aléatoire de même taille.

Traduction en une phrase : **il faut réduire l'attaquant à six items sur soixante, ou lui donner la
moitié des réponses avec un tiers d'erreurs, pour qu'il cesse de faire mieux que la démographie.**

## 3. Le cas « items courants seulement » : le résultat inverse de ce qui était prédit

L'attaquant restreint aux 45 items les plus ordinaires atteint **30,25 %**, contre 20,57 % avec les
60 items et 12,91 % avec 45 items tirés au hasard. Connaître **moins** de choses, mais les choses
banales, rend l'attaque **une fois et demie meilleure** que de tout connaître.

Trois vérifications avant d'accepter ce résultat :

1. **Deux opérationnalisations indépendantes de « banal » concordent.** L'entropie (préenregistrée)
   et la fréquence de la réponse modale (ajoutée **post hoc**, déclarée comme telle) sont corrélées à
   −0,956 et donnent 30,25 % et 31,21 %. Le volet préenregistré est rapporté tel quel ; le second le
   complète et ne le remplace pas. La raison de l'ajout est écrite : sur Twin, l'entropie classe
   d'abord les items par **nombre de modalités** (corrélation 0,955), pas par banalité de la réponse,
   et il fallait vérifier que le résultat ne tenait pas à ce confondant. Il n'y tient pas.
2. **Le confondant « mêmes items pour tout le monde » est écarté par un contrôle dédié** (D1b, post
   hoc). D1 tire un masque différent par candidat, D4 impose les mêmes items à tous. Avec des items
   **tirés au hasard mais identiques pour tous**, le taux à k = 45 vaut 12,52 %, indiscernable des
   12,91 % de D1. L'écart de D4 ne vient donc pas du partage des items, mais bien de **quels** items.
3. **Aucun item de Twin n'est réellement banal** : la fréquence modale maximale sur les 60 items
   vaut 0,621. Le scénario testé n'est donc pas « l'attaquant ne sait que des évidences », mais
   « l'attaquant ne dispose que d'items à peu de modalités » — ce qui est bien la forme d'une base
   commerciale, et ce qui doit être dit ainsi plutôt que surinterprété.

**Le mécanisme.** Les items écartés sont ceux à forte entropie et nombreuses modalités. Le jumeau
les reproduit mal : sur ces items, l'accord exact avec la vraie personne est presque aussi rare
qu'avec un inconnu. Ils entrent donc dans la distance de Hamming comme du bruit, et **noient** le
signal porté par les items simples. Un attaquant à données pauvres n'est pas seulement épargné : il
est **avantagé**, parce que sa pauvreté le débarrasse des items qui le desservent.

## 4. Mes prédictions préenregistrées, et ce qu'elles sont devenues

| | prédiction | mesure | verdict |
|---|---|---|---|
| P1 | D1 75 % entre 15 et 20 % | 12,91 % | **réfutée** (trop optimiste) |
| P2 | D1 50 % entre 8 et 15 % | 6,04 % | **réfutée** (trop optimiste) |
| P3 | D1 25 % entre 3 et 8 % | 1,81 % | **réfutée** (trop optimiste) |
| P4 | D1 10 % sous 2 %, IC chevauchants, rupture | 0,35 %, rupture | **confirmée** |
| P5 | D2 30 % au-dessus de 5 %, pas de rupture | 1,34 %, pas de rupture | **mi-réfutée** : la direction tient, le chiffre est 4 fois trop haut |
| P6 | D3 {50 %, 10 %} entre 5 et 12 % | 3,25 % | **réfutée** (trop optimiste) |
| P7 | D4 au moins un tiers plus bas que D1, rupture plus précoce | **une fois et demie plus haut**, rupture plus tardive | **réfutée, et de signe inverse** |
| P8 | la baseline se dégrade aussi, le ratio tient plus longtemps que l'écart absolu | baseline 2,07 % → 0,16 %, ratio 9,9 → 2,1 | **confirmée** |

Six prédictions sur huit sont fausses, et **sept des huit erreurs vont dans le même sens** : j'ai
systématiquement surestimé ce que l'attaque conserve sous dégradation. La seule erreur de signe
inverse, P7, est aussi la plus intéressante. Cela se dit, et cela pèse sur la confiance à accorder à
l'intuition dans ce chapitre : c'est la mesure qui a tranché, pas le raisonnement.

## 5. Verdict : la menace est-elle robuste ?

**Aucun des trois critères de fragilité préenregistrés (§7) ne se déclenche.**

1. Rupture dès 75 % d'items ou dès 5 % d'erreurs ? **Non** — 12,91 % et 15,05 %, neuf fois la
   baseline dans les deux cas.
2. Chute de plus de moitié entre 100 % et 75 % d'items ? **Non** — il reste 62,8 % du taux nominal.
3. D4 sous la baseline dès k = 45 ? **Non** — 30,25 % contre 5,10 %, et au-dessus du taux nominal.

**Verdict : la menace est robuste en nature, fragile en ampleur.** L'hypothèse « vraies réponses
exactes » n'est **pas** la condition de l'attaque : l'avantage sur la démographie survit à la perte
des trois quarts des items, à 30 % de réponses fausses, et à la restriction aux seuls items
ordinaires. Mais le taux **absolu** s'effondre vite — la moitié des items avec 10 % d'erreurs ne rend
plus que 3,2 %, un sixième du taux nominal. La phrase vendeuse « il suffit de connaître la moitié des
réponses, même avec 10 % d'erreurs, pour identifier six personnes sur dix » est **fausse d'un ordre
de grandeur** : c'est une personne sur trente et une, et l'article ne doit pas l'écrire.

Ce qui aggrave réellement le tableau n'est pas le taux, c'est le §3 : **la dégradation la plus
réaliste, celle d'une base commerciale, est celle qui coûte le moins — et qui peut rapporter plus que
les données parfaites.**

## 6. Limites, et ce qui n'est pas mesuré ici

- **Un seul attaquant, le plus faible.** Tout est mesuré avec l'accord de Hamming naïf. L'attaquant
  fort A-LLR de `c7-attaquant-fort-resultats.md` gagne déjà 2,5 points sur données parfaites
  (23,23 % contre 20,69 %) ; il pondère les accords par leur rareté, donc il devrait précisément
  **moins** souffrir de la dégradation. Tous les points de rupture donnés ici sont des **bornes
  optimistes pour la vie privée**, et il faudrait les recalculer sous A-LLR avant d'en faire un
  chiffre de sécurité.
- **Seul le pool est dégradé**, jamais la sortie de jumeau publiée (qui est publique par hypothèse).
- **Un seul jeu, un seul générateur** : Twin-2K-500, `JSON Persona - GPT4.1`. Rien n'est transposé à
  Park et al.
- **Le bruit est tiré dans la marginale conditionnée à être différente** de la vraie réponse. Un
  bruit uniforme, ou un bruit corrélé à la vraie réponse (une réponse périmée reste souvent proche),
  donnerait d'autres chiffres ; le choix est déclaré au préenregistrement, pas optimisé après coup.
- **D1b a une forte variance entre répétitions** (3,25 % à 8,05 % à k = 30) parce que le jeu d'items
  change d'une répétition à l'autre : sa moyenne peut tomber hors de l'IC de sa répétition médiane,
  que la règle préenregistrée impose de rapporter. C'est une limite de la règle, pas un désaccord
  entre les mesures.

## 7. La phrase que l'article devrait écrire sur son modèle d'attaquant

> Notre attaquant dispose des réponses exactes de tous les candidats. Cette hypothèse est favorable,
> mais elle n'est pas nécessaire : en dégradant ses données auxiliaires, le taux de ré-identification
> reste significativement supérieur à la baseline démographique du même bassin tant qu'il connaît un
> quart des items (1,8 % contre 0,4 %), ou jusqu'à 30 % de réponses fausses sur l'ensemble des items
> (1,3 % contre 0,3 %) ; il ne rejoint la baseline qu'à six items sur soixante. Le taux absolu, lui,
> chute vite : la moitié des items avec 10 % d'erreurs ne rend plus que 3,2 %, contre 20,6 % en
> information parfaite. Surtout, un attaquant restreint aux items les plus ordinaires — ceux que
> détient n'importe quelle base commerciale — fait **mieux**, et non moins bien, qu'avec l'ensemble
> des items (30,3 % sur les 45 items les moins entropiques), parce que les items à nombreuses
> modalités, que le jumeau reproduit mal, n'ajoutent que du bruit à l'appariement. L'hypothèse
> d'information parfaite n'est donc pas ce qui porte notre résultat.
