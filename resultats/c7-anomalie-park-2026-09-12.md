# C7-anomalie-Park : pourquoi Park fuit-il ~3x moins que Twin malgré ~3x plus d'items ?

**Écrit le 12 septembre 2026. Sections 0 à 3 (inventaire, hypothèses, préenregistrement)
rédigées avant tout calcul nouveau ; seuls des chiffres déjà publiés ailleurs dans le
dépôt sont cités en section 0-1.** Étude de risque de vie privée sur deux jeux déjà
publics (Twin-2K-500, archive Park et al./Stanford). Aucun identifiant ni appariement
individuel n'est jamais imprimé ou écrit ; seuls des taux agrégés sortent dans
`resultats/c7-anomalie-park.csv`.

## 0. L'anomalie, précisément localisée

Elle ne vient pas de `c7-stanford-resultats.md` (jumeau vs humain, où Stanford fuit
*plus* que Twin : 65,7 % contre 20,7 %). Elle vient du **canal inter-jumeaux** (un
jumeau contre les autres jumeaux de la même personne, pas contre l'humain),
documenté dans `c7-transfert-resultats.md` (Twin) et `c7-transfert-stanford-resultats.md`
(Park/Stanford), et déjà nommée dans `article-synthese.md` (lignes 44 et 85) :

| jeu | canal | items communs | top-1 | hasard (1/N) |
|---|---|---|---|---|
| Twin-2K-500 | jumeau ↔ jumeau (30 paires riches) | 60 | **36,4 %** | 0,049 % (N=2058) |
| Park/Stanford | entretien ↔ enquête (agents GSS) | 177 | **11,9-13,0 %** | 0,095 % (N=1052) |

Park a ≈3× plus d'items communs (177 vs 60) et fuit ≈3× moins (12-13 % vs 36,4 %).
Déjà écarté ailleurs dans le dépôt, cité ici sans recalcul : le nombre d'items ne
l'explique pas seul (`article-synthese.md` l.85, `c7-transfert-stanford-resultats.md` §2 :
« la relation top-1/items diffère entre jeux ») ; l'entropie par item non plus, et change
même de signe entre jeux (`c7-bits-resultats.md` §3 : r = −0,81 sur Twin, +0,57 sur
Stanford — pas une loi transportable, alors que l'information conditionnelle, elle,
garde signe et ordre de grandeur des deux côtés, r = 0,72 et 0,89).

## 1. Inventaire : qu'est-ce qui est mesurable sans appel d'API ?

Présents sur disque et exploitables localement :
- **Twin-2K-500** (`data/twin2k500/`) : réponses humaines vague 1-3 et vague 4, 8
  configurations de jumeaux dont 7 « riches », toutes rechargeables via
  `analyses/t1_commun.py` (`T1.charger()`), déjà utilisées par `c7_reidentification.py`
  et `c7_transfert.py`. **Un vrai texte de persona existe** :
  `data/twin2k500/wave_persona_chunk_001.parquet` (294 personnes sur 2058 — un seul
  chunk présent localement), colonnes `wave1_3_persona_text` et `wave1_3_persona_json` :
  mesurable directement, voir section 3.
- **Park/Stanford** (`data/osf-t6g7k-stanford/`) : réponses humaines vague 1 et vague 2,
  conditions d'agent (composite/enquête/entretien/démographique/persona) sur GSS (177
  items catégoriels), Jeux économiques et Big Five (5 items continus chacun),
  rechargeables via `analyses/c7_stanford.py` (`charger_domaine`). Déjà utilisées par
  `c7_stanford.py` et `c7_transfert_stanford.py`.
- Les deux matrices humaines (Twin v4, Stanford GSS v1) permettent de calculer une
  **matrice de corrélation/association entre items** sans aucun appel de modèle : c'est
  la donnée qui manquait aux rapports déjà écrits pour trancher l'hypothèse de
  dépendance entre items.
- La **taille de bassin** (N=2058 Twin, N=1052 Stanford) est déjà connue ; ce qui manque
  est un recalcul du top-1 du **canal inter-jumeaux précis** (pas jumeau-vs-humain, déjà
  fait par `c7_echelle.py`) après sous-échantillonnage du bassin Twin à N=1052.

Non mesurable sans appel d'API, constaté ici :
- **Longueur de la persona côté Park/Stanford.** Aucune transcription d'entretien brute
  n'est présente localement : `data/osf-t6g7k-stanford/figure2/data/agent_bank/` ne
  contient qu'un `participant_list_rand_order_v1.csv` (23 Ko, une liste, pas des
  entretiens) ; `FIGURE2_PIPELINE.md` documente les *sorties* d'agents (v3/v6/v7), pas
  le texte d'entrée. Le rapprochement avec la mission (persona ≈121 000 caractères
  « chez Twin » contre ≈8 000 « chez nous ») vient de `article-synthese.md` l.85-86 et
  concerne un tout autre calcul (A9/`c7-fort-resultats.md`, tentative de reproduction
  locale de la fidélité Twin avec persona tronqué), pas une mesure Park/Stanford — on ne
  peut donc chiffrer la longueur de persona Park localement, seulement celle de Twin
  (section 3).
- **Modèle générateur des jumeaux Park.** Park et al. ont produit leurs agents avec leur
  propre pipeline (mentions GPT-4o dans les métadonnées annexes) ; on ne peut ni le
  rejouer ni le faire varier sans appel payant. Confondu reconnu, non testable ici.
- **Taux de non-réponse** : déjà établi ailleurs sans recalcul nécessaire — les 60 items
  Twin utilisés sont par construction remplis à 100 % chez les deux configurations
  comparées (`items_pair`, `c7_transfert.py`) et le GSS Stanford a « quasi aucun
  manquant » (`c7-stanford-preenregistrement.md` §3). Les deux canaux comparés sont donc
  déjà à ~0 % de manquants sur les items utilisés : ce n'est pas un facteur qui peut
  différer entre les deux mesures de l'anomalie, pas besoin de recalcul.

## 2. Hypothèses concurrentes (au moins quatre, non exclusives)

| # | hypothèse | prédiction chiffrée distinctive | calcul qui départage |
|---|---|---|---|
| H1 | Longueur/format de la persona noie ou concentre le signal | Park utilise une persona nettement plus longue (ou plus courte) que Twin pour le canal en cause | **Non trancable ici** (section 1) : Twin mesurable (section 3), Park non |
| H2 | Dépendance entre items : 177 items GSS fortement corrélés ≠ 3× l'information de 60 items Twin plus hétérogènes | ratio effectif (items non redondants) ≪ ratio brut (2,95) | corrélation moyenne inter-items (Cramér's V) + items effectifs = N/(1+(N−1)·V̄), sur les réponses humaines des deux jeux |
| H3 | Taille de l'espace des candidats (N=1052 vs 2058) | un bassin plus petit **gonfle** mécaniquement le top-1 (cf. `c7-echelle-resultats.md`) ; donc N ne peut PAS expliquer un top-1 plus bas côté Park (qui a le bassin le plus petit) — au contraire, si l'hypothèse était vraie l'écart serait pire, pas résolu | recalcul du top-1 du canal inter-jumeaux Twin après sous-échantillonnage du bassin à N=1052 (20 tirages, IC bootstrap) |
| H4 | Variance entre personnes par item (fiabilité test-retest) plus faible chez Park | plafond humain test-retest de Park < celui de Twin | déjà mesuré ailleurs (81,6 % Twin N=2058 vs 96,8 % Stanford N=1052, `c7-echelle-resultats.md`/`c7-stanford-resultats.md`) — cité, pas recalculé, avec la réserve que les N diffèrent |
| H5 | Taux d'items non répondus diffère entre canaux | l'un des deux canaux montrerait un taux de remplissage < 100 % sur les items comparés | déjà établi à ~0 % des deux côtés (section 1) — pas recalculé |
| H6 | Modèle générateur des jumeaux différent (pipeline Park vs Twin) | jumeaux Park systématiquement moins fidèles/plus lissés indépendamment du contenu | **non testable localement** (section 1) — candidat pour l'expérience payante si H2/H3 ne suffisent pas |

## 3. Préenregistrement des calculs locaux (avant exécution de `analyses/c7_anomalie_park.py`)

**Priorité déclarée** : H2 (dépendance entre items) et H3 (taille du bassin) d'abord,
comme demandé — si l'une suffit, H1 (persona) devient superflue pour expliquer
l'anomalie (mais reste une inconnue en soi, non fermée par ce rapport).

**H2 — dépendance entre items.**
Données : réponses humaines Twin vague 4 sur les 60 items communs du canal inter-jumeaux
(`t1_commun.charger()` + `c7_reidentification.items_communs`) ; réponses humaines
Stanford vague 1 sur les 177 items GSS (`c7_stanford.charger_domaine("gss")`,
`coder_categoriel_commun`). Pour chaque jeu : V̄ = moyenne du V de Cramér sur toutes les
paires d'items (paires à effectif ≥ 20 réponses conjointes seulement), puis
items_effectifs = N/(1+(N−1)·V̄) (formule de taille effective sous corrélation intra-
classe constante, standard). Ratio observé = items_effectifs(GSS)/items_effectifs(Twin).
**Prédiction** : V̄(GSS) > V̄(Twin) ; verdict « fortement soutenue » si ratio effectif
< 1,2 (l'avantage brut de 2,95× disparaît presque entièrement), « soutenue » si
1,2 ≤ ratio < 2,0, « rejetée » si ratio ≥ 2,5 (redondance négligeable).

**H3 — taille du bassin.**
Canal exact : paire représentative du transfert inter-jumeaux Twin à 60 items, proche de
la moyenne des 30 paires (36,4 %) — `JSON Persona - GPT4.1` (attaquant) contre
`Text Persona - GPT4.1-mini` (bassin), top-1 publié = 37,3 % à N=2058
(`c7-transfert-voletA.csv`). Recalcul du même top-1 (mêmes fonctions
`c7_reidentification.rangs_attaque`/`resume_taux`, graine 20260912) après
sous-échantillonnage sans remise du bassin à N=1052, 20 tirages indépendants, IC 95 %
bootstrap sur les personnes (mêmes conventions que `c7_echelle.py`). Répliqué sur une
deuxième paire (`Text Persona (Default Temperature)` → `Text Persona - GPT4.1-mini`,
83,6 % à N=2058) pour vérifier que la direction ne dépend pas du niveau de départ.
**Prédiction** : top-1(N=1052) ≥ top-1(N=2058) (le bassin plus petit ne peut
qu'augmenter ou maintenir le top-1, jamais l'abaisser) ; si confirmé, H3 est **rejetée
comme explication de l'anomalie** (elle va dans le mauvais sens) — verdict inverse
seulement si top-1(N=1052) < top-1(N=2058) de façon nette (IC disjoints).

**H1, mesure descriptive seule (pas un test).** Longueur en caractères de
`wave1_3_persona_text` et `wave1_3_persona_json` sur les 294 personnes de
`wave_persona_chunk_001.parquet` : moyenne, médiane, IC bootstrap. Comparaison
possible avec Twin seulement (Park non mesurable, section 1) ; ceci documente la
donnée manquante, ne teste rien.

Sortie : `analyses/c7_anomalie_park.py` (aucun appel de modèle, lecture seule `data/`,
aucun identifiant imprimé), `resultats/c7-anomalie-park.csv`. Graine 20260912,
`.venv/bin/python`.

## 4. Résultats (calculés après la section 3, jamais avant)

Calculé par `analyses/c7_anomalie_park.py`. Sorties détaillées :
`c7-anomalie-park-h1-persona.csv`, `-h2-dependance.csv`, `-h3-bassin.csv`, et le fichier
de synthèse `c7-anomalie-park.csv` demandé par la mission.

### H1 — longueur de persona (descriptif)
Twin (`wave_persona_chunk_001.parquet`, 294 personnes sur 2 058 — un seul fragment
présent localement) : `wave1_3_persona_text` = **95 229** caractères en moyenne [IC
bootstrap 95 173;95 286], `wave1_3_persona_json` = **121 455** [121 389;121 516],
médiane 121 410 — confirme, avec une vraie mesure et non plus une seule citation, le
chiffre « ~121 000 caractères » déjà avancé dans `article-synthese.md`/`c7-fort-resultats.md`.
**Park/Stanford reste non mesurable** : aucune transcription d'entretien brute n'est
présente dans l'archive locale (section 1). H1 n'est donc **ni confirmée ni infirmée**
ici, seulement documentée d'un seul côté.

### H2 — dépendance entre items : **fortement soutenue**
| jeu | items | paires exploitables | V de Cramer moyen (point) | items effectifs (point) |
|---|---|---|---|---|
| Twin (60 items communs, humains v4) | 60 | 1 770 | 0,0834 | **10,13** |
| Park/Stanford (177 items GSS, humains v1) | 177 | 15 576 | 0,1055 | **9,05** |

Ratio brut d'items = 2,95 (177/60). **Ratio effectif = 9,05/10,13 = 0,89** : sous le
seuil de 1,2 fixé au préenregistrement pour « fortement soutenue », et même **sous 1** —
une fois la redondance retirée, les 177 items GSS transportent une information
indépendante légèrement **inférieure**, pas 3× supérieure, à celle des 60 items Twin.
L'intuition qui fonde l'énigme (plus d'items ⇒ plus d'empreinte) est directement
contredite par le calcul : Park n'a pas 3× plus d'information, il a environ la même
quantité, répartie sur 3× plus de questions corrélées entre elles.

*Note de méthode, honnêtement signalée* : un IC bootstrap (200 tirages sur les
personnes, remise) donne Twin V̄∈[0,0880 ; 0,0957] et Stanford V̄∈[0,1168 ; 0,1228] —
les DEUX décalés vers le haut par rapport au point estimé (0,0834 et 0,1055). C'est un
biais connu du bootstrap par ré-échantillonnage avec remise sur une statistique
d'association catégorielle : une ligne dupliquée s'accorde parfaitement avec elle-même
et gonfle artificiellement le chi², donc le V de Cramer. Le point estimé (sans
duplication, ci-dessus) reste la valeur retenue ; l'IC quantifie la direction et l'ordre
de grandeur de l'incertitude, pas une fourchette symétrique fiable autour du point.
Le verdict (ratio effectif ≪ ratio brut, avec inversion de sens) est de toute façon si
net que ce biais ne change aucune conclusion : même avec les V̄ hauts de l'IC, items
effectifs Stanford ≈ 8,2 contre Twin ≈ 9,3-9,7, ratio effectif encore < 1.

### H3 — taille du bassin : **rejetée comme explication, et l'écart s'aggrave après contrôle**
| paire (attaquant → bassin) | items | top-1 à N=2 058 | top-1 à N=1 052 (sous-échantillon) |
|---|---|---|---|
| JSON Persona GPT4.1 → Text Persona GPT4.1-mini | 60 | 37,3 % [35,4;39,3] | **44,1 %** [43,4;44,7] |
| Text Persona (Default Temp.) → Text Persona GPT4.1-mini | 60 | 83,5 % [82,0;85,0] | **86,9 %** [86,5;87,4] |

Sur les deux paires testées, réduire le bassin de 2 058 à 1 052 **augmente** le top-1
(IC totalement disjoints, sens confirmé pour les deux). C'est la prédiction
préenregistrée : un bassin plus petit ne peut pas expliquer un taux plus bas. Park a
justement le bassin le plus petit (1 052 contre 2 058) — si la taille du bassin jouait
un rôle, l'écart avec Twin serait **pire**, pas résolu. Concrètement : ramené à N=1 052,
le canal Twin comparable grimperait plutôt vers ~44 % (au lieu des 36,4 % moyens à
N=2 058), à comparer aux 11,9-13,0 % **réellement mesurés** sur Park à ce même N=1 052 —
l'écart corrigé pour la taille du bassin est plus grand que l'écart brut, pas plus
petit. H3 est rejetée sans ambiguïté.

## 5. Hypothèses classées après calcul

1. **H2 (dépendance entre items) — la plus étayée, et elle dissout la partie « énigme »
   de la question.** Le ratio brut de 2,95 items devient un ratio effectif de 0,89 une
   fois la corrélation inter-items retirée : Park n'a pas 3× plus d'information, il en a
   à peu près autant (voire un peu moins) que Twin, simplement répartie sur 3× plus de
   questions redondantes. L'intuition « plus d'items ⇒ plus de fuite » que l'énigme
   présuppose est fausse au niveau de l'information effective, pas seulement au niveau
   du taux observé.
2. **H3 (taille du bassin) — rejetée, et dans le mauvais sens pour « résoudre »
   l'anomalie.** Un bassin plus petit augmente le top-1 ; Park a le bassin le plus
   petit et pourtant le top-1 le plus bas : corriger pour N aggrave l'écart au lieu de
   le réduire.
3. **H5 (taux de manquants) — écartée par construction**, déjà à ~0 % des deux côtés sur
   les items comparés (section 1), sans recalcul nécessaire.
4. **H4 (variance entre personnes / fiabilité test-retest) — ne va pas dans le sens qui
   expliquerait un Park plus bas.** Le plafond humain test-retest est *plus haut* sur
   Stanford (96,8 %) que sur Twin (81,6 %), ce qui prédirait plutôt plus de fuite
   possible côté Park, pas moins (comparaison à N différents, prudence de rigueur).
5. **H1 (longueur/format de la persona) — ni confirmée ni infirmée, faute de donnée
   Park.** Twin mesuré ici pour la première fois avec un vrai chiffre (~95-121 k
   caractères selon le format) ; aucune transcription d'entretien Park n'existe
   localement pour comparer. Reste l'hypothèse la plus plausible pour le **résidu**
   (point suivant), non l'hypothèse à l'origine de l'énigme telle que formulée (H2 s'en
   charge déjà).
6. **H6 (modèle générateur différent) — non testable localement**, confondu reconnu.

## 6. Ce qui résiste : un résidu, plus modeste que l'énigme de départ

**L'énigme telle que formulée (« 3× plus d'items devrait vouloir dire 3× plus
d'empreinte ») est résolue par H2** : ce n'est pas vrai au niveau de l'information
effective, donc il n'y a rien d'étonnant à ce que Park ne fuie pas plus que Twin.

Mais un **résidu plus étroit persiste, honnêtement signalé, pas caché** : à information
effective comparable (≈9-10 items indépendants des deux côtés, H2), le canal
inter-jumeaux fuit quand même environ 3× moins sur Park (11,9-13,0 %) que sur Twin
(36,4 %). H2 et H3 ne expliquent pas CE résidu-là — elles expliquent seulement pourquoi
le facteur 3 sur le nombre BRUT d'items n'est pas le bon cadre de comparaison. Deux
candidats restent pour ce résidu, ni l'un ni l'autre testable localement (section 1) :
- **H1, format/longueur de la persona.** Les deux conditions comparées côté Park
  (« entretien », probablement une longue transcription narrative, vs « enquête »,
  réponses fermées au GSS) sont des sources bien plus hétérogènes entre elles que les
  paires Twin comparées ici (toutes des reformulations d'un même persona JSON/texte
  sous-jacent) — une différence de nature des deux entrées, pas seulement de longueur,
  qu'on ne peut pas chiffrer sans les transcriptions brutes de Park.
- **H6, pipeline générateur différent** (Park et al. vs Twin-2K-500), déjà signalé comme
  confondu non testable dans `resultats/c7-troisieme-jeu-inventaire-2026-09-12.md`.

## 7. Expérience payante minimale, si l'orchestrateur veut trancher le résidu (NON exécutée)

Objectif : tester si un **grand écart de format/longueur entre les deux sources
utilisées pour produire deux jumeaux indépendants de la même personne** (analogue à
« entretien » vs « enquête » côté Park) dégrade la **cohérence inter-jumeaux** (pas la
fidélité à l'humain, déjà testée par `c7-fort-resultats.md`), à information effective
égale par ailleurs.

- **Protocole** : reprendre exactement la recette « appel par item » de
  `analyses/c7_recette.py`/`c7_fort.py` (déjà validée, ne pas la modifier), sur les
  mêmes N=30 personnes et 60 items que `c7-fort-resultats.md` (comparabilité directe,
  coût connu). Produire **deux** jumeaux indépendants par personne : (A) persona JSON
  complet, ~121 000 caractères (mesuré en section 4, aucune troncature) ; (B) même
  persona tronqué à 8 000 caractères (règle déjà en vigueur dans `c7_gen`/`c7_recette`).
  Modèle `gpt-4.1-mini` (tenir le modèle constant, coût maîtrisé — la question posée est
  le format, pas le modèle, déjà écarté par `c7-fort-resultats.md`).
- **Mesure nouvelle** : top-1 **inter-jumeaux** A↔B sur les mêmes 60 items (même
  fonction `rangs_attaque`, même contrôle décoy que `c7_transfert.py`), comparé au
  top-1 A-vs-humain et B-vs-humain déjà mesurables sans coût additionnel.
- **Taille** : 30 personnes × 60 items × 2 conditions = 3 600 appels (le double de
  `c7-fort`, qui n'en produisait qu'une).
- **Coût estimé** : au tarif réellement observé pour `gpt-4.1` dans `c7-fort-resultats.md`
  (4,9949 USD / 1 800 appels ≈ 0,00278 USD/appel), 3 600 appels ≈ **10 USD** ; `gpt-4.1-mini`
  coûte typiquement plusieurs fois moins cher par jeton, donc une fourchette réaliste de
  **3 à 10 USD** selon le modèle finalement choisi. Budget proposé : **10 USD**, en
  incluant une marge d'échecs/relances comme celles déjà rencontrées dans `c7-fort`.
- **Prédiction falsifiable** : si H1 explique le résidu, top-1(A↔B) sera nettement plus
  bas que le top-1 obtenu entre deux configurations Twin déjà proches par construction
  (36,4 % moyen), en particulier plus proche des 11,9-13,0 % mesurés sur Park.

**Non exécutée. L'orchestrateur décide.**

## En clair

L'énigme posée (Park a 3× plus d'items et fuit 3× moins) n'en est plus une une fois
qu'on compte l'information effective plutôt que le nombre de questions : les 177
questions du GSS sont si corrélées entre elles qu'elles ne valent, une fois la
redondance retirée, pas plus qu'une dizaine de questions vraiment indépendantes — à peu
près autant, pas plus, que les 60 questions de Twin. La taille du bassin ne peut pas non
plus expliquer l'écart : elle va dans le sens inverse (un bassin plus petit, comme celui
de Park, devrait plutôt AUGMENTER le taux, pas le réduire). Un écart plus modeste
persiste malgré tout à information comparable, et il reste ouvert : la forme du persona
utilisé pour fabriquer chaque jumeau, ou le fait que les deux jumeaux Park proviennent de
sources bien plus différentes l'une de l'autre que les jumeaux Twin comparés ici. Le
trancher demanderait soit les transcriptions d'entretien brutes de Park (absentes du
disque), soit une expérience payante d'environ 10 USD décrite en section 7, non
exécutée.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>

