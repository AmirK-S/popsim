# C7, tautologie : préenregistrement (12 septembre 2026)

**Écrit avant `analyses/c7_tautologie.py` et avant tout calcul.** Objection tranchée ici,
la plus dangereuse contre l'article : « un jumeau plus exact ressemble plus à la personne,
donc il est forcément plus reconnaissable ; vous n'avez mesuré que de l'exactitude
renommée en vie privée ». Le nul de marge de `c7-disjoint-resultats.md` (100 prédicteurs
Bernoulli à la seule marge d'exactitude conditionnelle, aucune structure au-delà)
**renforce** cette objection : il reproduit rho = 0,984, au-dessus même du rho observé
0,969. C'est le contrôle le plus dur qu'on ait produit contre nous-mêmes.

## 0. Question expérimentale, formulée pour pouvoir être fausse
**À exactitude par personne tenue rigoureusement constante (identique au bit près, pas
seulement en espérance comme le nul de marge Bernoulli), la fuite (top-1, top-10, rang,
bits) varie-t-elle encore selon la STRUCTURE des erreurs ?** Si non : l'exactitude
suffit à tout expliquer, l'objection de tautologie est validée sans réserve. Si oui :
une part de la fuite n'est pas déductible de la seule exactitude, et il existe un
paramètre supplémentaire (quels items sont exacts, comment les erreurs se répartissent
entre personnes) que le scalaire d'exactitude ne capture pas.

## 1. Construction (aucun appel de modèle, lecture seule sur `data/`)
Univers : les 60 items toujours renseignés (`c7_reidentification.items_communs`, importé),
les 2 058 humains de vague 4 (`REF_V4`) comme pool ET comme population attaquée (comme
`c7_reidentification`/`c7_generateur`).

**Vecteur d'exactitude k_i (nombre d'items exacts sur 60, entier, tenu constant dans les
quatre conditions)** : emprunté au jumeau réel `JSON Persona - GPT4.1` (le jumeau vedette
de l'article, exactitude 0,590, top-1 réel 20,7 %) — couverture vérifiée à 100 % sur ces
60 items, donc k_i = nombre d'items où ce jumeau égale la vague 4, sans imputation de
manquant à faire. **On n'attaque pas ce jumeau réel** : k_i sert uniquement à donner aux
quatre conditions une distribution d'exactitude réaliste et partagée. Ce qui varie entre
conditions n'est JAMAIS k_i, seulement quels items parmi les 60 portent la bonne réponse.

**Rareté d'item** : entropie de Shannon corrigée Miller-Madow par item sur les 2 058
humains (`c7_bits.entropie_item`, importée) — entropie basse = réponse concentrée sur peu
de modalités (item « fréquent »/banal), entropie haute = réponses dispersées (item
« rare »/distinctif). C'est une propriété de la POPULATION, pas de la personne.

**Quatre prédicteurs synthétiques**, un vecteur de 60 réponses par personne, avec
exactement k_i réponses égales à la vérité (le reste, une valeur tirée dans la marginale
empirique de l'item, hors la vraie modalité, par rejet) :
- **(a) hasard** : les k_i items exacts sont un sous-ensemble uniforme au hasard parmi les
  60, tiré indépendamment pour chaque personne (indépendant entre personnes).
- **(b) concentré sur les items fréquents** : les items FAUX sont les (60−k_i) items de
  plus basse entropie (les plus fréquents/banals) ; les items exacts sont donc les k_i
  items les plus rares — même classement d'entropie pour tout le monde (déterministe,
  pas de tirage).
- **(c) concentré sur les items rares** : l'inverse — les items FAUX sont les (60−k_i)
  items de plus haute entropie (les plus rares) ; les items exacts sont les k_i items les
  plus fréquents/banals — même classement, déterministe.
- **(d) erreurs corrélées entre personnes** : un ORDRE FIXE, tiré une seule fois au hasard
  (indépendant de l'entropie, graine dédiée), le même pour tout le monde. Les items exacts
  d'une personne sont les k_i derniers de cet ordre : deux personnes de même k_i ont
  exactement le même ensemble d'items exacts, et l'ensemble d'une personne à faible k_i
  est inclus dans celui d'une personne à k_i plus grand. « Mêmes items ratés par tout le
  monde », sans lien avec la rareté (contrôle contre (b)/(c)).

Le remplissage des items faux (tirage dans la marginale empirique de l'item, rejet si la
valeur tirée égale la vérité) suit le MÊME algorithme dans les quatre conditions ; seule
la RÈGLE DE CHOIX des items exacts change. C'est la seule variable manipulée.

**Garde-fou (bloquant)** : après construction, on recalcule l'exactitude réalisée par
personne dans chacune des quatre conditions et on vérifie l'égalité bit à bit avec k_i,
puis l'égalité bit à bit entre les quatre vecteurs d'exactitude réalisée eux-mêmes
(`np.array_equal`, toutes les paires). Toute inégalité fait échouer le script
(`assert` avec message explicite, arrêt immédiat, aucun résultat rapporté en cas
d'échec).

## 2. Mesures
Sur chacune des quatre conditions : top-1, top-10, rang médian
(`c7_reidentification.rangs_attaque` / `a2_commun.distance_hamming`, importées), et la
fuite en bits (borne dyadique + Miller-Madow, `c7_bits.bits_et_ic`, importée). IC 95 % par
bootstrap sur les personnes, 2 000 tirages (`a2_commun.bootstrap_personnes`, importée, et
le bootstrap interne de `bits_et_ic`, déjà fixé à 2 000). 5 réplicats de remplissage
aléatoire par condition (comme `c7_generateur`, pour lisser le bruit du tirage des valeurs
fausses ; (a) retire en plus un nouveau sous-ensemble aléatoire à chaque réplicat), 20
tirages de départage des ex æquo par réplicat. Graine fixée (20260912 + graine par nom de
condition) ; une deuxième exécution complète doit produire un CSV bit-à-bit identique.

## 3. Prédictions chiffrées **[HYPOTHÈSE]**, et pourquoi
Repères connus : hasard top-1 = 1/2 058 = 0,049 % ; JSON Persona GPT4.1 (réel, exactitude
0,590) = 20,7 % ; PMM/B2 (réel, exactitude 0,47–0,51, connus pour régresser vers le mode,
donc « corrects » surtout sur des items fréquents) = 0,07–0,3 %.

- **(c) le plus bas** : ne conserver que des items fréquents/banals revient à la
  situation de PMM/B2 (corrects surtout sur le mode) malgré une exactitude bien
  supérieure (0,59 contre 0,47–0,51). Prédiction : top-1(c) dans **[0,05 % ; 1 %]**, du
  même ordre que PMM/B2, très inférieur au jumeau réel malgré la même exactitude que lui.
- **(b) le plus haut** : ne rater que des items banals et garder les items rares est la
  répartition la plus favorable à la ré-identification à exactitude donnée (moins de
  candidats concurrents partagent par hasard la bonne réponse sur un item rare).
  Prédiction : top-1(b) **dépasse le jumeau réel (20,7 %)**, plausiblement dans
  **[30 % ; 90 %]** (intervalle large, incertitude réelle assumée).
- **(a) intermédiaire** : un sous-ensemble aléatoire d'items mélange fréquents et rares
  dans les proportions de la population. Prédiction : top-1(a) du même ordre de grandeur
  que le jumeau réel, dans **[3 % ; 25 %]**.
- **(d) l'incertitude assumée** : si SEULE la rareté des items retenus compte (et non le
  fait que le choix soit partagé entre personnes), top-1(d) doit être **proche de top-1(a)**
  (facteur < 2, IC recouvrants), parce que (d) utilise un ordre fixe tiré au hasard, donc
  en moyenne ni plus ni moins riche en items rares qu'un tirage indépendant. Si au
  contraire la corrélation des erreurs ENTRE personnes supprime en elle-même une part de
  la fuite (au-delà de la composition en rareté), top-1(d) sera **notablement inférieur**
  à top-1(a) — résultat qui serait nouveau et surprenant, à ne pas écarter a priori.

## 4. Règle de décision (ce qui réfute notre position, ce qui la confirme)
Comparaison pivot demandée par la mission : **(b) contre (d)**, à exactitude strictement
égale.

- **Réfutation de notre position, tautologie validée** : si les quatre conditions donnent
  le même top-1 aux IC 95 % près (recouvrement mutuel, écart < facteur 2 entre le plus
  haut et le plus bas), alors **l'exactitude par personne suffit à tout expliquer** ; la
  structure des erreurs (rareté des items conservés, corrélation entre personnes)
  n'ajoute rien. Phrase à écrire dans ce cas : « à exactitude par personne égale, la
  fuite ne dépend que de l'exactitude, pas de la structure des erreurs — l'objection de
  tautologie est confirmée sur ce terrain, notre résultat ne montre rien de plus que le
  nul de marge. »
- **Confirmation qu'une part de la fuite n'est pas réductible à l'exactitude** : si
  top-1(b) dépasse top-1(d) d'un facteur ≥ 3 avec IC 95 % disjoints (et, de façon
  cohérente, top-1(b) > top-1(a) > top-1(c) dans le même ordre de grandeur), alors QUELS
  items sont exacts (leur rareté dans la population) est un déterminant de la fuite non
  capturé par le scalaire d'exactitude. Phrase à écrire dans ce cas : « à exactitude par
  personne strictement égale, la fuite varie d'un facteur [X] selon que les bonnes
  réponses tombent sur des items rares ou banals : l'exactitude seule ne détermine pas la
  fuite, contrairement à ce que suppose l'objection de tautologie. »
- **Résultat mixte** (ex. b > a ≈ d > c, écart b/d réel mais < facteur 3, ou IC qui se
  recouvrent partiellement) : rapporté tel quel, sans forcer l'une ou l'autre lecture ;
  la conclusion portera alors sur l'ORDRE DE GRANDEUR (« la rareté des items comptent
  clairement, la corrélation entre personnes en elle-même n'a pas d'effet net démontré »
  ou l'inverse), pas sur une décision binaire.

Dans tous les cas, le résultat — favorable ou non — est rapporté tel quel dans
`resultats/c7-tautologie-resultats.md`, y compris s'il valide entièrement l'objection de
tautologie contre nous.

## Avenant (même jour, écrit avant tout calcul, en réaction à une alerte reçue pendant
l'écriture du script)
Une revue a signalé que `c7_disjoint.construire_nul` émet la vraie réponse `y_ref` de la
personne avec probabilité `q_i`, et qualifié cela d'« empreinte maximale » invalidant ce
témoin. Vérification demandée sur ce script-ci avant tout calcul.

**Où `y_ref` (la vérité `pool`) intervient dans les quatre conditions (a)-(d) : de façon
identique et nécessaire.** Par construction, « la personne a exactement k_i items exacts »
signifie, sur ces k_i positions, valeur du prédicteur = valeur vraie — il n'existe
mathématiquement aucune autre façon d'atteindre une exactitude EXACTE et choisie par
personne sans, sur les positions déclarées exactes, écrire la vraie valeur. Ce n'est pas
un artefact de notre code, c'est la définition même d'« exactitude ». Les quatre
conditions lisent `y_ref` de la MÊME façon (recopie sur les positions exactes, valeur
tirée dans la marginale de l'item ailleurs) ; **seule la règle qui choisit QUELLES
positions sont exactes diffère**, et c'est précisément la variable manipulée par cette
expérience. Prétendre construire un prédicteur à exactitude choisie sans jamais recopier
la vérité serait une contradiction dans les termes, pas une amélioration méthodologique.
Cela ne rend pas les quatre témoins invalides : ça les rend NÉCESSAIREMENT construits
ainsi, comme n'importe quel prédicteur réel ayant une exactitude positive (le jumeau LLM
lui-même recopie la vérité sur les items qu'il devine bien).

**Ce qui est un vrai témoin « sans lecture individuelle de la cible »** existe déjà dans
le dépôt et n'a pas besoin d'être réinventé : PMM k=10, B1, B2 (`t1_baselines.calculer`)
prédisent l'item de vague 4 à partir des vagues 1-3 et des démographies de la personne,
JAMAIS de sa propre réponse à l'item cible — leur exactitude sur les 60 items (0,47 à
0,51, `c7-contre-examen-2026-09-11.md` §1) N'EST PAS calibrée, elle tombe où elle tombe.
C'est la comparaison qui a déjà établi, avant ce script, que même à exactitude un peu plus
basse que le jumeau (0,59), ces prédicteurs sans lecture de la cible fuient 2 ordres de
grandeur en dessous (0,07-0,3 % contre 20,7 %).

**Ajout non préenregistré à l'origine, ajouté ici avant tout calcul en réponse à
l'alerte** : un cinquième témoin, `temoin_mode_global`, la modalité modale de chaque item
sur toute la population (`c7_bits.mode_item`, importée, vecteur constant, LE MÊME pour
tout le monde), rejoué dans le même pipeline. Il ne lit `y_ref` d'une personne que par sa
contribution à une statistique agrégée sur 2 058 personnes (1/2058e d'un vote de
population, convention déjà utilisée sans réserve ailleurs dans ce dépôt pour B0/B0
mode) — il ne recopie JAMAIS la réponse d'un individu pour construire SA PROPRE ligne.
Son exactitude n'est PAS calée sur k_i : elle est mesurée telle qu'elle tombe. Rapporté à
titre de repère, hors de la comparaison appariée (b)/(d) qui reste le test principal.
