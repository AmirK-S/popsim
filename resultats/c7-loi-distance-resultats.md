# C7 — « loi de distance » : résultats

Calculé par `analyses/c7_loi_distance.py`, préenregistré dans
`resultats/c7-loi-distance-preenregistrement.md` (écrit avant le script et avant toute
mesure de paire). Sortie chiffrée : `resultats/c7-loi-distance.csv` (75 lignes).
**Aucun appel d'API, aucune dépense, aucune recherche web, aucune génération de jumeau.**
Lecture seule sur `data/`. Aucun identifiant ni appariement individuel n'est produit.

---

## Verdict en une phrase

**Ce n'est pas une loi.** Sur Twin, une fois la fidélité des deux jumeaux contrôlée, la
distance entre pipelines n'explique **rien** (ρ partiel = **+0,003** [−0,047 ; +0,068]) ;
sur Park, trois paires seulement survivent au contrôle, ce qui interdit toute réplication.
Ma prédiction préenregistrée (Twin ρ ≈ −0,7) est **réfutée**. Ce qui reste, et qui est réel,
ce sont les **paliers par axe** — et une composition partielle entre axes, trouvée *post hoc*.

---

## 1. Ce qui est réellement exploitable

| jeu | configurations publiées | retenues avant contrôle | paires mesurées | **paires du test** |
|---|---|---|---|---|
| Twin-2K-500 | 13 | 7 | 21 | **15** |
| Park et al., bloc GSS | 6 | 5 | 10 | **3** |
| **total** | | **12** | **31** | **18** |

Bassin et items **constants dans chaque jeu**, comme exigé : Twin 2 058 personnes et
**60 items** pour les 21 paires ; Park 1 052 personnes et **20 items** pour les 10 paires.

**Il faut le dire franchement : 18 paires, mais seulement 9 configurations indépendantes
(6 + 3), et deux ateliers.** Une paire n'est pas une unité d'observation indépendante :
les 15 paires Twin sont 15 contrastes entre 6 configurations d'une même équipe partageant
les mêmes fichiers de persona et le même harnais. Le socle est mince, et il ne s'agrandit
pas en comptant les paires.

Exclusions décidées **avant** tout calcul (préenregistrement §2) : les cinq configurations
Twin non admissibles ou suspectes de `twin-ab-audit-provenance-2026-09-11.md` ;
`JSON Persona - GPT4.1-mini`, qui ne partage que 19 items avec les autres et aurait imposé
19 items à toutes les paires ; les blocs *jeux économiques* et *Big Five* de Park (5 items
chacun) ; la condition `v8` de Park, non documentée.

---

## 2. Le contrôle d'interprétabilité, et qui il a exclu

Appliqué à **chaque** configuration avant inclusion, sur le bassin et les items réellement
attaqués, baseline recalculée sur ce même bassin.

| jeu | configuration | top-1 contre les humains | baseline démographique | verdict |
|---|---|---|---|---|
| Twin | JSON Persona - GPT4.1 | 20,69 % [19,00 ; 22,40] | 2,15 % [1,59 ; 2,79] | passe |
| Twin | Text Persona - Gemini-Flash2.5 | 13,08 % [11,64 ; 14,52] | idem | passe |
| Twin | Text Persona (Reasoning) - mini | 9,33 % [8,14 ; 10,55] | idem | passe |
| Twin | Text Persona (Repeating Q.) - mini | 7,30 % [6,28 ; 8,34] | idem | passe |
| Twin | Text Persona (Default Temp.) - mini | 5,50 % [4,61 ; 6,38] | idem | passe |
| Twin | Text Persona - GPT4.1-mini | 5,45 % [4,51 ; 6,40] | idem | passe |
| Twin | **Demographics Only - GPT4.1-mini** | 2,16 % [1,60 ; 2,76] | idem | **exclue** |
| Park | composite | 18,67 % [16,59 ; 20,79] | 0,38 % [0,11 ; 0,73] | passe |
| Park | entretien | 7,36 % [6,05 ; 8,82] | idem | passe |
| Park | enquête | 6,34 % [5,15 ; 7,63] | idem | passe |
| Park | **démographique** | 0,40 % [0,14 ; 0,74] | idem | **exclue** |
| Park | **persona (`gss_v7`)** | **0,26 % [0,06 ; 0,52]** | 0,39 % [0,13 ; 0,74] | **exclue** |

- **Twin `Demographics Only`** et **Park `démographique`** sont exclues **mécaniquement** :
  elles *sont* la baseline et ne peuvent pas se dépasser elles-mêmes. C'était annoncé
  (préenregistrement §6). Leurs paires sont mesurées et consignées dans le CSV
  (`bloc = paire_hors_controle`), mais n'entrent pas dans le test.
- **Park `persona` est une exclusion réelle, et elle compte** : cet agent, à qui l'on donne
  une auto-description, réidentifie la bonne personne **moins bien que la baseline
  démographique** (0,26 % contre 0,39 % à 20 items ; 1,97 % contre 2,23 % à 177 items).
  Tout contraste bâti sur lui comparerait du bruit à du bruit. C'est exactement le
  sinistre de la nuit du 11 au 12, évité cette fois avant la mesure.

C'est ce contrôle qui fait tomber Park de 10 paires à 3, et qui rend la réplication
impossible — pas un choix d'analyse.

---

## 3. Les 15 paires Twin (bassin 2 058, 60 items, attaque symétrique)

| d | ce qui change | top-1 | IC 95 % |
|---|---|---|---|
| 1 | décodage | **81,42 %** | [79,98 ; 82,77] |
| 1 | gabarit | **67,05 %** | [65,31 ; 68,73] |
| 1 | raisonnement | **33,54 %** | [31,61 ; 35,28] |
| 1 | modèle | **17,19 %** | [15,84 ; 18,57] |
| 2 | gabarit + décodage | 56,71 % | [54,93 ; 58,51] |
| 2 | modèle + format de persona | 38,96 % | [37,11 ; 40,71] |
| 2 | gabarit + raisonnement | 35,54 % | [33,81 ; 37,22] |
| 2 | modèle + format de persona | 34,05 % | [32,23 ; 35,87] |
| 2 | décodage + raisonnement | 29,06 % | [27,37 ; 30,82] |
| 2 | modèle + raisonnement | 28,28 % | [26,62 ; 29,97] |
| 2 | modèle + gabarit | 16,83 % | [15,53 ; 18,13] |
| 2 | modèle + décodage | 13,54 % | [12,23 ; 14,75] |
| 3 | modèle + raisonnement + format | 35,56 % | [33,82 ; 37,46] |
| 3 | modèle + gabarit + format | 31,00 % | [29,30 ; 32,72] |
| 3 | modèle + décodage + format | 27,37 % | [25,72 ; 28,98] |

Hasard : 0,049 %. Toutes les paires en sont très loin ; le canal inter-jumeaux existe et
n'est pas en cause.

**Relation obtenue :**

| jeu | n paires | ρ(d, top-1) | IC 95 % | verdict préenregistré | **ρ partiel, fidélité contrôlée** |
|---|---|---|---|---|---|
| Twin-2K-500 | 15 | **−0,232** | [−0,321 ; −0,187] | INDÉCISE | **+0,003** [−0,047 ; +0,068] |
| Park (GSS) | 3 | −0,866 | [−0,866 ; −0,866] | « SOUTENUE » *(voir §4)* | +0,000 [+0,000 ; +0,000] |

**Dispersion à d fixé (test B, critère de réfutation 3) — c'est le chiffre décisif :**

| d | n | moyenne | étendue | écart-type |
|---|---|---|---|---|
| 1 | 4 | 49,80 % | **17,19 – 81,42 %** | **25,6 pts** |
| 2 | 8 | 31,62 % | 13,54 – 56,71 % | 12,6 pts |
| 3 | 3 | 31,31 % | 27,37 – 35,56 % | 3,4 pts |

À **un seul** changement de pipeline, le taux va de 17 % à 81 %. La variation *à l'intérieur*
d'un niveau de d écrase la variation *entre* niveaux. Le critère de réfutation 3 est
déclenché : même si ρ était plus négatif, d ne prédirait rien d'utile.

**Pourquoi ρ brut est si faible.** ρ(d, fidélité) = **+0,727** : les paires à grand d sont
justement celles qui impliquent `JSON Persona - GPT4.1`, la configuration la plus fidèle
(20,7 %). La fidélité et la distance tirent en sens contraires, et une fois la fidélité
contrôlée il **ne reste rien** (ρ partiel = +0,003). **H₀ l'emporte sur H.**

---

## 4. Réplication sur Park : impossible, pas négative

Trois paires seulement passent le contrôle : enquête↔composite (d = 1) 7,70 %,
entretien↔composite (d = 1) 17,32 %, enquête↔entretien (d = 2) 2,37 %.

Le ρ de −0,866 affiché par la règle de décision **n'est pas une preuve, et je le dis plutôt
que de l'encaisser** : à n = 3 le ρ de Spearman ne peut prendre que ±1, ±0,5 ou 0, et aucun
rééchantillonnage des personnes ne renverse l'ordre — d'où un IC bootstrap **dégénéré**
([−0,866 ; −0,866]) qui ne mesure aucune incertitude. La règle préenregistrée n'avait pas
été conçue pour n = 3 ; **appliquée là, elle est vide.** Et ρ(fidélité, top-1) = **+1,000** :
les trois taux sont parfaitement ordonnés par la fidélité des conditions comparées, pas par d.

**Sensibilité post hoc à la règle d'items.** La règle préenregistrée (colonnes renseignées
à 100 % partout) ne gardait que **20 items sur 177** sur Park. Refait avec les 177 items
(manquants masqués par la distance, comme partout ailleurs dans le dépôt) : les niveaux
retrouvent les valeurs publiées (composite contre humains = 65,59 %, contre 65,7 % dans
`c7-stanford-provenance-resultats.md`), les paires montent (entretien↔composite **92,80 %**,
enquête↔composite 29,90 %, enquête↔entretien 12,41 %), **les mêmes deux conditions sont
exclues, et ρ est inchangé (−0,866, partiel +0,000)**. La règle d'items n'a donc pas
fabriqué le résultat — mais elle a coûté cher en niveau, et c'est une leçon pour la suite.

---

## 5. Post hoc, déclaré comme tel : les axes se composent partiellement

Le comptage non pondéré échoue. La question suivante, naturelle, n'était **pas**
préenregistrée : l'effet de deux changements se déduit-il de l'effet de chacun pris seul ?
Calibration sur les **seules** quatre paires à un axe (ancrées sur `Text Persona -
GPT4.1-mini`), prédiction multiplicative sur les six paires à deux axes, **aucune constante
ajustée sur les paires prédites**.

| axes combinés | prédit | observé | observé / prédit |
|---|---|---|---|
| décodage × gabarit | 54,59 % | 56,71 % | **1,04** |
| décodage × raisonnement | 27,31 % | 29,06 % | **1,06** |
| décodage × modèle | 14,00 % | 13,54 % | **0,97** |
| gabarit × modèle | 11,53 % | 16,83 % | 1,46 |
| raisonnement × gabarit | 22,49 % | 35,54 % | 1,58 |
| **raisonnement × modèle** | 5,77 % | 28,28 % | **4,90** |

Erreur absolue moyenne **7,53 pts**, ρ de rang prédit/observé **+0,714**, rapport médian
**1,26**. Trois paires sur six sont prédites à 6 % près par un modèle qui n'a vu que les
paires à un axe ; les trois autres sont **sous-estimées**, toujours dans le même sens : deux
changements dégradent **moins** que le produit de leurs effets. Les axes ne sont donc pas
indépendants — ils mordent en partie sur la même information. C'est exploratoire, sur six
points, et cela demanderait un jeu de configurations conçu pour ça.

---

## 6. Verdicts sur les prédictions préenregistrées

| prédiction (§5 du préenregistrement) | résultat |
|---|---|
| Twin ρ ≈ −0,7, IC excluant 0 | **RÉFUTÉE** : −0,232 [−0,321 ; −0,187] |
| Park ρ ≈ −0,6, IC pouvant contenir 0 | **sans objet** : 3 paires, IC dégénéré |
| Réplication (les deux jeux SOUTENUS) | **NON** |
| Inversion entre jeux (réfutation 2) | non — les deux ρ sont négatifs |
| Courbe plate sur Twin (réfutation 1, ρ > −0,20) | **non atteinte de peu** (−0,232) |
| Variance intra-niveau > inter-niveaux (réfutation 3) | **OUI, déclenchée** (25,6 pts à d = 1) |
| H au sens fort (test A : ρ partiel ≤ −0,30, IC excluant 0) | **NON** : +0,003 [−0,047 ; +0,068] |

---

## 7. Ce que je reproche moi-même à ce travail

- **La distance est arbitraire, et la mesure le montre.** Les poids égaux sont le point
  faible que le préenregistrement annonçait ; les quatre axes à d = 1 s'étalent de 17 % à
  81 %, soit un facteur presque 5 entre deux « unités de distance » censées valoir pareil.
  Un indice qui traite le passage de T = 0 à la température par défaut comme équivalent à
  un changement de modèle ne peut pas fonctionner, et il n'a pas fonctionné. **Je ne
  sauverais pas cette distance en la repondérant** : les poids seraient alors ajustés sur
  le taux de liaison, et la mesure deviendrait circulaire — exactement ce que la mission
  interdisait.
- **Réserve R1, non levée.** Sur Twin aucune invite n'est observable localement : les
  descripteurs viennent du **nom publié** des configurations. Si deux configurations
  diffèrent en plus sur un point non annoncé par leur nom, d est sous-estimée.
- **L'unité indépendante est la configuration, pas la paire.** 18 paires, 9 configurations,
  2 ateliers. Aucun ρ calculé ici ne mérite d'être présenté comme une régularité générale.
- **Le contrôle exclut par construction la configuration la plus éloignée de toutes les
  autres** (l'agent purement démographique). Le test porte donc sur une plage de distances
  volontairement resserrée. C'est le prix du contrôle, et il est juste : ces paires-là
  n'étaient pas interprétables.

---

## 8. Phrase que l'article a le droit d'écrire

> Le taux de liaison entre deux jumeaux publiés d'une même personne dépend fortement de
> **quel** élément du pipeline change, mais pas du **nombre** d'éléments qui changent. Sur
> les six configurations de Twin-2K-500 qui passent un contrôle de fidélité préalable
> (2 058 personnes, 60 items communs, attaque symétrique), un changement isolé donne
> 81,4 % [80,0 ; 82,8] pour le seul décodage, 67,1 % [65,3 ; 68,7] pour le seul gabarit,
> 33,5 % [31,6 ; 35,3] pour le seul raisonnement et 17,2 % [15,8 ; 18,6] pour le seul
> modèle. Une distance ordinale entre pipelines définie avant mesure comme le nombre de
> descripteurs publiés qui diffèrent ne prédit ces taux que faiblement (ρ de Spearman
> −0,23 [−0,32 ; −0,19] sur 15 paires) et **plus du tout une fois contrôlée la fidélité
> individuelle des deux jumeaux comparés** (ρ partiel +0,00 [−0,05 ; +0,07]) ; à distance
> fixée à un seul changement, les taux s'étalent de 17 % à 81 %. Sur l'archive de Park et
> al., le même contrôle n'épargne que trois paires — l'agent à auto-description y
> réidentifie la personne moins bien que la baseline démographique — de sorte qu'aucune
> réplication n'est possible. **L'hypothèse d'une loi de distance entre pipelines n'est
> donc pas soutenue ; ce qui est mesuré est un ordre de grandeur par axe, pas une loi.**

---

## 9. En clair

Deux « doubles numériques » de la même personne se ressemblent d'autant plus qu'on a moins
touché à la machine qui les fabrique — mais **compter le nombre de réglages changés ne
prédit presque rien**. Changer la température seule laisse 8 liaisons réussies sur 10 ;
changer le modèle seul en laisse moins de 2. Un seul réglage, cinq fois moins de fuite :
c'est *lequel* on change qui compte, pas *combien*. Et dès qu'on tient compte de la qualité
des deux doubles comparés, la « distance entre pipelines » n'explique plus rien du tout.
L'idée qu'on pourrait se défendre en « éloignant » les pipelines reste donc **non
démontrée** : il faudrait d'abord savoir quel axe éloigner, ce que ces deux jeux ne
suffisent pas à établir.
