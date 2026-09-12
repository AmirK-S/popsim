# C7. Multiplicité — complément à `c7-multiplicite.md`

**Note de méthode, écrite en cours de rédaction, à ne pas cacher** : la partie la plus
coûteuse de ce chantier (bootstrap commun rejouant plusieurs analyses sur le même tirage de
personnes) a été **abandonnée avant complétion**, sur instruction explicite du
coordinateur, après deux essais interrompus (~170-200 s pour la seule étape
`t1_baselines.calculer`, incompatible avec un calcul tenu en avant-plan). La fonction est
écrite et documentée dans `analyses/c7_multiplicite_globale.py`
(`bootstrap_commun_twin()`), mais **n'est pas exécutée** (`FAIRE_BOOTSTRAP_COMMUN = False`).
Section 4 explique précisément ce qui manque de ce fait. Tout le reste de ce rapport
(inventaire, Holm/BH sur une famille confirmatoire élargie, robustesse des seuils, verdicts)
est calculé et écrit.

## 0. Préenregistrement des attentes (écrit avant les calculs de ce complément)

Avant de lancer `analyses/c7_multiplicite_globale.py`, l'attente déclarée était : (i) la
famille confirmatoire élargie contiendrait entre 15 et 25 tests convertibles en p, la
plupart avec des IC déjà très éloignés de leur seuil (donc peu de bascules attendues sous
Holm/BH) ; (ii) un bootstrap commun sur Twin montrerait une corrélation positive mais
modeste entre les réplicats de rho (A1) et de top-1 (A2/A3), avec un élargissement des IC
simultanés de l'ordre de 1,2 à 1,6× l'IC marginal ; (iii) le choix de la défense D4 resterait
robuste à un déplacement raisonnable du seuil d'utilité (1 à 3 points) ; (iv) au moins une
prédiction préenregistrée à seuil serré (candidate identifiée à l'avance : `fidélité > 0,10`
du jumeau fort, observé 0,1714) serait fragile à un déplacement de seuil plausible.
Ce qui a été recalculé confirme (i), (iii) et (iv) ; (ii) n'a pas pu être vérifié (abandon,
voir section 4). Une découverte **non anticipée** dans ce préenregistrement : deux tests à
succès nul (0 succès sur un petit n) reposaient sur un IC percentile dégénéré et doivent être
requalifiés de « réfuté » à « non concluant » — voir section 3.2, corrigé sur signal du
coordinateur pour l'un des deux (A9, top-1 du jumeau fort), étendu par moi-même par la même
logique au second (A9, recette/granularité).

## 1. Ce qui est déjà fait ailleurs, et n'est pas refait ici

`resultats/c7-multiplicite.md` : comptage de 47 tests sur trois familles (affirmations de
l'article, contrôles autonomes, branches abandonnées) et une correction de Holm sur les
**3 seuls tests à p classique** de l'article (`c7-courbe-gen` p=0,002 ; `c7-compromis` §2
p=0,008 ; `c7-compromis` §3 p=0,78). Ce fichier dit lui-même ne pas avoir recalculé les 31
autres tests (IC bootstrap contre seuil, « Holm/BH ne s'y applique pas de la même façon »).
Ce complément traite exactement cette lacune, plus la dépendance entre analyses réutilisant
les mêmes personnes, plus la robustesse des seuils choisis après coup — trois points que
`c7-multiplicite.md` liste explicitement comme non faits.

## 2. Inventaire des comparaisons chiffrées : confirmatoire vs exploratoire

Base : les 13 revendications (A1-A13) de `resultats/article-synthese.md`, section 2, plus la
section « Ce que nous ne savons pas » (A5's H1-H4 comptent sous A5, l'anomalie Stanford sous
A7/A9). **Confirmatoire** = un fichier `*-preenregistrement.md` daté existe, écrit avant le
script qui produit le chiffre, avec un seuil chiffré fixé d'avance. **Exploratoire** = chiffre
produit sans seuil fixé d'avance, ou décision prise après avoir vu un premier résultat (choix
de métrique, de sous-groupe, de comparateur).

| Revendication | Test | Statut | Seuil préenregistré / ce qui a été regardé après coup |
|---|---|---|---|
| A1 | rho(fidélité,fuite), 12 points (`c7-compromis`) | **Confirmatoire** | ≥ 0,70 (`c7-compromis-preenregistrement.md`) |
| A1 | rho sur items disjoints (a) | **Confirmatoire** | > 0,70, moyenne sur 50 partages (`c7-disjoint-preenregistrement.md`) |
| A1 | rho observé vs nul de marge (b) | **Confirmatoire** | rho > 95e centile du nul (même fichier) |
| A1 | régression fuite~exactitude (r=0,724, p=0,008) | Exploratoire | aucun seuil préenregistré ; introduit après coup comme « proxy » |
| A1 | contrôle style (rho_style, p=0,78) | Exploratoire | idem, contrôle ad hoc |
| A2 | comparateurs statistiques (PMM, B2, donneur k=1 contexte) < 0,3 % | Exploratoire | `c7-contre-examen`, contre-examen critique post-hoc, pas de seuil préenregistré à l'origine |
| A2 | 2 générateurs individualisés (G-LR, G-copule) | **Confirmatoire** | top-1 ≥ 10 % ou ≥ moitié du jumeau, sinon << (`c7-generateur-preenregistrement.md`) |
| A2 | synthétiseur ajusté sur la cible (donneur k=1 avantagé), top-1 | **Confirmatoire** | << 20,7 % (`c7-synth-ajuste-preenregistrement.md`) |
| A2 | même comparateur, **top-10** (53,2 % > 42,7 %) | Exploratoire | métrique secondaire calculée après le top-1, jamais fixée au préenregistrement |
| A3/A11 | attaquant fort A-LLR, gain ≥ 20 % relatif, Twin et Park | **Confirmatoire** | 24,8 % (Twin), 78,9 % (Park) (`c7-attaquant-fort-preenregistrement.md` [P1]) |
| A3/A11 | D4 sous A-LLR < 1 % | **Confirmatoire** | [P2], même fichier |
| A3/A11 | attaquant adaptatif (S1-S3) < 1 % | **Confirmatoire**, non convertible en p (pas d'IC publié par stratégie au même format) | addendum du même fichier |
| A3 | monde ouvert, seuils historiques (>5 % Twin, >30 % Stanford, attaque naïve) | **Confirmatoire** | seuils de l'ancien préenregistrement C7, réfutés puis recontextualisés par l'attaquant fort |
| A5 | H1 entropie appariée (chevauchement attendu) | **Confirmatoire**, catégorique | `c7-mecanisme-preenregistrement.md` |
| A5 | H2 cohérence personne-à-personne > 0 | **Confirmatoire** | idem |
| A5 | H3 permutation du bloc → chute au plancher | **Confirmatoire**, catégorique (déjà tranché ailleurs) | idem |
| A5 | H4 stéréotypie IA nettement > humains | **Confirmatoire** | idem |
| A6 | Stanford GSS, top-1 ≥ 10 % et ≥ 5× démographique | **Confirmatoire** | `c7-stanford-preenregistrement.md` |
| A6 | contamination vague1/vague2 (écart < 3 pts) | **Confirmatoire** | `c7-stanford-provenance-preenregistrement.md` |
| A7 | transfert Twin, volet A, top-1 moyen ≥ 15 % sur 42 paires | **Confirmatoire**, mais **pooling fragile** (voir §5) | `c7-transfert-preenregistrement.md` |
| A7 | transfert Stanford, top-1 GSS ≥ 20 % | **Confirmatoire** | `c7-transfert-stanford-preenregistrement.md` |
| A7 | anomalie Stanford (3× plus d'items, 3× moins de fuite) | Exploratoire | constat fait après coup, aucun mécanisme proposé |
| A9 | courbe fidélité-fuite, régression 12 points (r=0,785, p=0,002) | **Confirmatoire** (déjà dans `c7-multiplicite.md`) | `c7-courbe-gen-preenregistrement.md` |
| A9 | 7 jumeaux régénérés dans l'IP à 95 % | **Confirmatoire** | seuil « ≥ 4/7 dedans » (échec si ≥4/7 dehors) |
| A9 | recette : granularité d'appel, top-1 ×5 | **Confirmatoire**, requalifié (§3.2) | `c7-recette-preenregistrement.md` |
| A9 | modèle fort : exactitude > 0,55 | **Confirmatoire** | `c7-fort-preenregistrement.md` |
| A9 | modèle fort : top-1 > 5 % | **Confirmatoire**, requalifié (§3.2) | idem |
| A9 | modèle fort : fidélité > 0,10 | **Confirmatoire**, **seuil fragile** (§5) | idem |
| A12 | DP vs D4, écart d'utilité ≥ 5 pts | **Confirmatoire** | `c7-dp-preenregistrement.md` |
| A13 | 4 prédictions (groupes, régression, ACP, comparaison D4 vs écart brut) | **Confirmatoire** | `c7-utilite-aval-preenregistrement.md` |
| A4, A8, A10 | bits d'identité, courbe risque-utilité D1-D4, courbe d'échelle | **Descriptif**, pas de test à seuil unique préenregistré (bornes d'ordre de grandeur seulement) | `c7-bits-`, `c7-defense-`, `c7-echelle-preenregistrement.md` |

Cet inventaire n'est pas parfaitement exhaustif (les sous-hypothèses de detail de A5/A8/A13 au-delà
de celles listées ne sont pas toutes reprises une par une), mais couvre toutes les revendications
numérotées A1-A13 et leurs préenregistrements associés.

## 3. Famille confirmatoire élargie : Holm et Benjamini-Hochberg

Calculé par `analyses/c7_multiplicite_globale.py` (fonction `famille_confirmatoire()`,
exécution en quelques secondes, aucune donnée brute rechargée — seulement les CSV déjà
publiés). Écrit dans `resultats/c7-multiplicite-globale.csv` (21 lignes : 15 convertibles en
p, 6 non convertibles listées telles quelles).

**Méthode de p, selon le cas** : classique (spearmanr/linregress) quand disponible ;
**empirique** quand la distribution de réplicats existe déjà sur disque (`c7-disjoint-nul.csv`,
`c7-disjoint-partages.csv`) ; **binomiale exacte (Clopper-Pearson)** quand l'IC publié est
dégénéré (0 succès sur un petit n) ; sinon **approximation normale (Wald)** à partir de l'IC
bootstrap publié et du seuil préenregistré (jamais un seuil choisi après coup). Convention
uniforme : p petit = forte évidence **en faveur** de la prédiction préenregistrée.

### 3.1 Table triée par p (15 tests convertibles)

| id | revendication | p brut | p (Holm) | p (BH) | Holm 0,05 | BH 0,05 |
|---|---|---|---|---|---|---|
| A2_generateur_G-LR | A2 | ~0 | ~0 | ~0 | oui | oui |
| A2_generateur_G-copule | A2 | ~0 | ~0 | ~0 | oui | oui |
| A1_disjoint_a | A1 | <1e-300 | <1e-299 | <1e-300 | oui | oui |
| A5_mecanisme_H2_coherence | A5 | 6,3e-130 | 7,6e-129 | 2,4e-129 | oui | oui |
| A11_P1_Park GSS | A11 | 4,9e-36 | 5,3e-35 | 1,5e-35 | oui | oui |
| A11_P2_D4_sous_attaquant_fort | A11 | 5,8e-12 | 5,8e-11 | 1,4e-11 | oui | oui |
| A1_primaire | A1 | 9,5e-7 | 8,6e-6 | 2,0e-6 | oui | oui |
| A9_courbe_gen_pente | A9 | 0,00247 | 0,0198 | 0,00463 | oui | oui |
| A1_disjoint_b | A1 | 0,900 | 1,000 | 1,000 | **non** | **non** |
| A11_P1_Twin | A11 | 0,961 | 1,000 | 1,000 | **non** | **non** |
| A5_mecanisme_H4_stereotypie | A5 | 0,999 | 1,000 | 1,000 | **non** | **non** |
| A9_fort_exactitude | A9 | 1,000 | 1,000 | 1,000 | **non** | **non** |
| A7_stanford_entretien→enquete | A7 | 1,000 | 1,000 | 1,000 | **non** | **non** |
| A7_stanford_enquete→entretien | A7 | 1,000 | 1,000 | 1,000 | **non** | **non** |
| A9_fort_top1 | A9 | 1,000 | 1,000 | 1,000 | **non** (voir §3.2 : non concluant, pas réfuté) |

### 3.2 Ce qui change de statut, précisément

**Aucune bascule n'est due à la correction de multiplicité elle-même.** Les 15 p sont
bimodaux : soit écrasants (p ≤ 0,0025 brut, huit tests), soit déjà proches de 1 avant toute
correction (sept tests). Il n'existe, dans cette famille élargie, **aucun test à p intermédiaire
(disons 0,01-0,05 brut)** que Holm ou BH auraient fait basculer d'un statut à l'autre — et
Holm et BH donnent ici **exactement le même verdict pour les 15 tests** (aucune divergence
entre les deux méthodes sur cette famille). C'est en soi une réponse au relecteur : la
multiplicité ne fabrique aucune fausse confirmation marginale ici, parce qu'aucune des
revendications confirmatoires ne repose sur un résultat tout juste significatif.

**Deux bascules réelles, mais dues à une correction de méthode, pas à Holm/BH** :
- **A9, top-1 du jumeau fort (> 5 %)** : l'IC percentile publié dans `c7-fort-reidentification.csv`
  est **[0 % ; 0 %]** sur k=0 succès / n=30 — un artefact : un bootstrap percentile sur une
  variable binaire à 0 succès ne peut produire que des tirages à 0, donc un IC à largeur
  nulle, quelle que soit la vraie incertitude. Le test de Clopper-Pearson exact donne
  **[0,00 % ; 11,57 %]** : le seuil préenregistré de 5 % est **à l'intérieur** de cet
  intervalle. Verdict corrigé : **NON CONCLUANT**, pas réfuté (correction reçue du
  coordinateur, incorporée telle quelle, avec le calcul reproduit dans le script).
- **A9, recette/granularité (top-1 par-item ≥ ×5 top-1 unique)** : même famille d'artefact,
  détectée par moi-même en appliquant la même logique. n=40 des deux côtés, 0/40 partout,
  Clopper-Pearson **[0 % ; 8,8 %]** pour les deux bras : les deux intervalles se recouvrent
  entièrement, aucun pouvoir statistique à ce n pour distinguer un facteur ×5 de rien du tout.
  Verdict corrigé : **NON CONCLUANT** (pas réfuté comme l'écrivait jusqu'ici l'article — la
  conclusion qualitative « la granularité n'explique pas la fuite » reste portée par ailleurs
  par le test du modèle fort et par courbe-gen, pas par ce test-ci en particulier).

**Conséquence sur le décompte global** : le nombre de prédictions préenregistrées comptées
comme « réfutées » dans le ledger de l'article diminue d'au moins un (A9 top-1 du jumeau fort),
et un second cas voisin (A9 recette/granularité) devrait recevoir la même requalification par
cohérence méthodologique, ce qui n'avait pas été signalé avant ce chantier.

### 3.3 Ce qui reste hors de cette famille (6 tests non convertibles en p)

`A9_courbe_gen_verif` (dénombrement 7/7, pas de p), `A9_fort_fidelite` (point seul sans IC
publié), `A12_dp_vs_d4` (écart de point sans IC sur l'utilité), `A13_acp_chute` (idem),
`A5_mecanisme_H1_entropie` (test d'équivalence, aucune marge préenregistrée pour en tirer un p
— tranché catégoriquement : IC disjoints d'un facteur ~46, réfuté sans ambiguïté). Ces six
lignes figurent dans le CSV avec leur description complète mais ne portent pas de p, donc pas
de correction Holm/BH — exactement le choix de méthode annoncé en préenregistrement (§0).

## 4. Réutilisation des personnes : bootstrap commun — ABANDONNÉ, ce qui manque

**Abandon assumé.** La fonction `bootstrap_commun_twin()` (dans
`analyses/c7_multiplicite_globale.py`) est écrite, documentée, et ferait ce qui suit si elle
tournait : un seul tirage de personnes par réplicat (2000 réplicats prévus), appliqué EN MÊME
TEMPS aux 12 points de `c7-compromis.csv` (recalcul de rho à chaque réplicat) et aux taux de
fuite du meilleur jumeau (JSON Persona GPT4.1), de Demographics Only et de PMM k=10, pour en
tirer une corrélation empirique entre les réplicats de rho et de top-1 (quantifiant la
dépendance introduite par la réutilisation des mêmes personnes d'une analyse à l'autre) et des
IC simultanés par la méthode du maximum studentisé (Westfall-Young).

**Pourquoi elle n'a pas tourné** : deux essais ont été lancés dans ce chantier ; le
chargement de Twin (`t1_commun.charger`, ~4-5 s) est rapide, mais le réajustement des 4
repères statistiques sur 5 plis (`t1_baselines.calculer`, nécessaire pour PMM k=10, B1, B2)
a mesuré ~164 s et ~170 s sur les deux essais, avant même d'entamer les 2000 réplicats de
bootstrap eux-mêmes. Sur instruction du coordinateur (pas de calcul en arrière-plan, tout
doit tenir en avant-plan en quelques minutes), ce calcul est abandonné ici : **aucun essai
réduit n'a été fait** (ni en réduisant le nombre de réplicats, ni en réduisant à un
sous-ensemble des 12 points), faute de temps dans cette session.

**Conséquence précise, revendication par revendication** : restent **sans IC simultané avec
quoi que ce soit d'autre**, et sans estimation quantifiée de leur dépendance mutuelle par
réutilisation de personnes :
- **A1** — rho(fidélité, fuite), les 12 points et le test sur items disjoints ;
- **A2/A3 sur Twin** — le top-1 du meilleur jumeau, de Demographics Only et de PMM k=10, en
  monde fermé ;
- par construction, **A9** (courbe-gen, modèle fort) qui repose sur la même régression à 12
  points que A1 hérite de la même lacune.

Étaient de toute façon **hors périmètre même si le bootstrap avait tourné** (dit dès la
conception, §0) : l'attaquant fort (A3/A11, A-LLR) et le monde ouvert (calibration de seuil par
réplicat, beaucoup plus coûteux) ; les bits d'identité (A4, Miller-Madow) ; toute l'archive
Park/Stanford (A6, A7-Stanford, A11-Park, substrat de personnes différent). Ces revendications
n'ont, dans ce chantier comme dans tous les précédents, aucun IC simultané publié — chacune ne
porte que son propre IC marginal, déjà cité dans `article-synthese.md`.

**Ce que cela signifie pour le relecteur** : l'énoncé « les IC sont corrects pris isolément,
l'ensemble ne l'est pas » reste, pour A1/A2/A3 sur Twin, une affirmation **non quantifiée** par
ce chantier — ni confirmée ni infirmée par un chiffre. La correction Holm/BH de la section 3
répond à la partie « multiplicité des tests », pas à la partie « dépendance par réutilisation
des personnes », qui reste ouverte pour ces trois revendications précises.

## 5. Robustesse des seuils choisis après coup

**Cas 1 — robuste : le choix de la défense D4.** Calculé sur `c7-defense-courbe.csv` (déjà
publié, aucun recalcul). Règle préenregistrée : « risque le plus bas parmi les réglages sous 2
points de perte d'utilité, sinon la meilleure utilité sous 1 % de top-1 ». D4 (top-1 0,126 %,
perte 1,467 pt) est l'unique candidat sous 2 points parmi D1 (k=2/5/10/25), D2 (p=5/10/25/50 %),
D3 (5, 10, 20/40 gardés, ou bloc entier). En déplaçant le seuil de perte d'utilité à 1, 3 ou 5
points, **D4 reste choisi dans les trois cas** (à 1 point, la règle de repli — meilleure
utilité sous 1 % top-1 — sélectionne aussi D4, seul réglage sous 0,15 % de top-1 avec la plus
faible perte parmi ceux-là ; à 3 et 5 points, D4 reste le plus bas top-1 parmi les candidats
qualifiés). **Ce choix ne tient pas à un seuil précis.**

**Cas 2 — fragile : A9, fidélité du jumeau fort > 0,10.** Observé 0,1714. Le seuil aurait pu
tout aussi bien être fixé à 0,15 (tient encore) ou à 0,18 (bascule : réfuté) — et notre propre
jumeau **le plus faible** de la courbe-gen (deepseek-v4, fidélité 0,177) est **au-dessus** de
0,1714. Un seuil fixé, avant tout calcul, au niveau de ce plancher déjà connu par ailleurs dans
le dépôt aurait fait échouer cette troisième prédiction. **Ce résultat ne tient qu'à un choix
de seuil précis, et l'article le dit déjà lui-même** (« à peine au-dessus de notre meilleur
jumeau faible »).

**Cas 3 — fragile par construction : A2, le choix de k dans le top-k.** Le comparateur donneur
avantagé (k=1, ajusté sur la cible) donne top-1 = 0,00 % contre 20,7 % pour le jumeau (facteur
extrême, confirme A2), mais **top-10 = 53,2 % contre 42,7 %** — le donneur dépasse le jumeau.
Le sens de toute l'affirmation « spécificité du jumeau LLM » **s'inverse** selon qu'on choisit
k=1 ou k=10, sans qu'aucun principe ne fixe k=1 comme le bon choix autrement que par convention.
Déjà signalé dans l'article (A2, réserve explicite) ; formalisé ici comme cas de seuil fragile.

**Cas 4 — fragile : A10, l'échelle au-delà de N mesuré.** Loi puissance et loi logarithmique,
ajustées sur les 6 mêmes points mesurés (N=50 à 2058), donnent déjà **18,1 % contre 13,9 %** à
2× la plage mesurée, et la loi log **s'effondre à zéro** vers N≈30 000 — deux modèles
indiscernables sur les données mesurées divergent radicalement dès qu'on extrapole. Déjà traité
dans l'article comme limite assumée (aucune valeur publiée au-delà de N≈4000) ; confirmé ici
comme un cas honnête de non-robustesse à la forme fonctionnelle choisie, pas seulement à un
seuil numérique.

**Cas 5 — robuste, en contraste : A9, seuil « ≥4/7 dans l'intervalle de prédiction ».** Observé
7/7. Un tel écart (7 sur 7, contre un seuil de succès à 4) tolère de déplacer le seuil jusqu'à
7/7 sans jamais basculer : le résultat le plus robuste de tout l'inventaire aux seuils
alternatifs.

## 6. Verdict par revendication

| Revendication | Verdict |
|---|---|
| A1 | **Tient, mais requalifiée** — le couplage qualité/fuite est confirmatoirement établi (p≈0 sur trois tests indépendants : primaire, disjoint, style), mais A1 elle-même est déjà requalifiée dans l'article (nul de marge non dépassé) ; aucun IC simultané disponible avec A2/A3-Twin (abandon §4) |
| A2 | **Tient** pour le top-1 (générateurs et synthétiseur avantagé, p≈0 ou catégorique) ; **requalifiée** sur le top-10, seuil de métrique fragile (cas 3) |
| A3 | **Tient** (attaquant fort, Park confirmé p≈0 ; Twin non significatif mais déjà lu comme un renforcement, pas un échec, dans l'article) |
| A4 | Hors périmètre de ce chantier (pas de test à seuil préenregistré unique, descriptif) |
| A5 | **Tient, mixte** — H2 confirmée (p≈0), H1 et H4 réfutés catégoriquement/statistiquement (p≈1), cohérent avec le verdict déjà publié de l'article |
| A6 | Non repris ici en détail (Stanford top-1≥10 %/≥5×demo, marge écrasante déjà publiée) — pas de changement |
| A7 | **Ne tient pas** sur le seuil Stanford (≥20 %, p≈1 dans les deux sens) — déjà su ; **fragile** sur le volet Twin (pooling 42 paires, dépend du mélange 60/19 items, cf. article) |
| A8 | Hors périmètre direct de la famille Holm/BH (pas de p à ce niveau), mais **seuil de choix de défense robuste** (cas 1) |
| A9 | **Mixte, la plus retravaillée ici** : régression tient (p=0,0025→0,0198 après Holm, confirmée) ; modèle fort — exactitude réfutée (p≈1), **top-1 requalifié réfuté→non concluant** (§3.2), fidélité confirmée mais **seuil fragile** (cas 2) ; recette/granularité **requalifiée réfuté→non concluant** (§3.2) |
| A10 | **Robuste seulement dans la plage mesurée** ; extrapolation **fragile** à la forme fonctionnelle (cas 4), déjà su et assumé comme limite |
| A11 | **Tient sur Park** (p≈0 pour P1 et P2) ; **ne tient pas sur Twin** pour le gain relatif (p=0,96, déjà lu par l'article comme un renforcement plutôt qu'un échec) |
| A12 | Hors famille à p (pas d'IC sur l'utilité), mais l'écart mesuré (1,86 pt) est **loin** du seuil préenregistré (5 pts) : réfutation qualitativement nette, pas fragile |
| A13 | Hors famille à p (ratios sans IC), chute ACP observée (35,4 %) **au-delà** du seuil préenregistré (30 %) : confirmée, marge modeste (35,4 vs 30) — à surveiller mais pas dans la même famille statistique que les autres |

## 7. Fichiers produits et limites assumées

`analyses/c7_multiplicite_globale.py` (exécuté, `FAIRE_BOOTSTRAP_COMMUN=False`),
`resultats/c7-multiplicite-globale.csv` (21 lignes, toutes les colonnes de p/Holm/BH),
ce rapport. **Non fait, dit comme tel** : le bootstrap commun (section 4) ; une famille
confirmatoire strictement exhaustive de chaque sous-hypothèse de détail (A5/A8/A13 au-delà de
celles listées section 2) ; une revue des seuils fragiles au-delà des cinq cas de la section 5.
