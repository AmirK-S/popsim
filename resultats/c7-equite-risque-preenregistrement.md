# C7, équité du risque : préenregistrement (13 septembre 2026)

statut: courant
mandat: Mesurer si le risque de ré-identification est réparti uniformément entre les personnes ou concentré sur une minorité, caractériser les plus exposés, et déterminer si la défense D4 (mélange intra-segment) réduit l'inégalité ou seulement le taux moyen. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_equite_risque.py, resultats/c7-equite-risque-preenregistrement.md, resultats/c7-equite-risque-resultats.md, resultats/c7-equite-risque.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_defense.py, analyses/c7_controle_interpretabilite.py, analyses/c7_stanford.py
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, réimplémentation de l'attaque, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00

**Ce document est écrit avant le premier calcul d'équité.** Rien de ce qui suit n'est
informé par un résultat de distribution individuelle : les seuls chiffres connus à
l'écriture sont les moyennes déjà publiées (20,7 % top-1 monde fermé sur Twin,
60,17 % TPR@1 % monde ouvert sur Park, 0,05 % après D4).

## 0. La question

Nous publions une moyenne. Une moyenne de 20,7 % est compatible avec deux mondes
opposés : 20,7 % de chance pour chacun, ou 21 % des personnes identifiées à coup sûr et
les autres jamais. Le second monde n'est pas la même étude : ce ne sont plus « des
données qui fuient un peu », ce sont **certaines personnes qui sont exposées**. Et si les
exposés sont ceux dont les réponses sont atypiques, alors la fuite pèse sur les
minorités de réponse. C'est la question d'équité qu'un régulateur pose.

## 1. Ce qui est repris, et ce qui est nouveau

Repris tel quel, **sans une ligne recopiée** :
`t1_commun.charger`, `c7_reidentification.items_communs / rangs_attaque / graine_nom /
REF_V4 / REF_V13 / DEMO / GRAINE`, `a2_commun.bootstrap_personnes`,
`c7_defense.defense_d4`, `c7_mecanisme.items_achat`, `c7_stanford.charger_domaine /
coder_categoriel_commun / accord_categoriel / rangs_depuis_accord / VAGUE1`,
`c7_controle_interpretabilite.controle_avant_interpretation`.

Nouveau ici, et rien d'autre : le **risque individuel à bassin constant** (§2), les
mesures de concentration (§3), les corrélats d'exposition (§4), et la décomposition de
l'effet de D4 sur l'inégalité (§5).

## 2. Le risque individuel, et le piège du bassin

Le top-1 contre le bassin entier est une variable binaire par personne : elle ne donne
pas de distribution. Pire, **le top-1 dépend mécaniquement de la taille du bassin** —
2,13 % à 2 058 personnes, 13,29 % à 120 pour la même baseline démographique. Comparer
deux sous-groupes de tailles différentes par leur top-1 intra-groupe mesurerait la taille
du groupe, pas son exposition. C'est l'erreur du moonshot, corrigée le 12/09.

**Définition retenue, préenregistrée.** Pour chaque personne attaquée `i`, l'attaque
(`rangs_attaque`, inchangée) donne le rang `R_i` de la vraie personne parmi les `N`
candidats du bassin complet. On pose `c_i = R_i − 1`, le nombre d'imposteurs qui battent
la vraie personne. Le **risque individuel à bassin B** est alors la probabilité exacte
que la vraie personne arrive première dans un bassin tiré au hasard qui la contient et
contient `B − 1` imposteurs :

`p_i(B) = C(M − c_i, B − 1) / C(M, B − 1)`, avec `M = N − 1` imposteurs.

C'est une transformation **déterministe et monotone** du rang, pas une nouvelle attaque.
Elle a trois propriétés qui la rendent seule admissible ici : elle est continue (donc
elle a des déciles), elle vaut exactement le top-1 observé quand `B = N`, et surtout
**elle est définie au même `B` pour tout le monde** — la comparaison entre sous-groupes
ne peut plus mesurer la taille du groupe. `B = 100` est fixé ici, avant tout calcul, et
`B = 1 000` sert de contrôle de sensibilité.

Cible principale : `JSON Persona - GPT4.1` contre `humains vague 4`, 60 items toujours
renseignés (le jumeau et le protocole des chiffres publiés). Comparateur :
`Demographics Only - GPT4.1-mini`, même bassin, mêmes items. Réplication : archive
Park et al., bloc GSS, condition `composite` contre `humains vague 1 (cible)`.

## 3. Prédictions — forme et concentration

**P1 (forme).** La distribution de `p_i(100)` est **fortement asymétrique** : je prédis
que le décile supérieur a un risque moyen **au moins 10 fois** celui du décile médian, et
que la médiane de `p_i(100)` est **inférieure à la moyenne** (asymétrie à droite).

**P2 (concentration).** Le **Gini** de `p_i(100)` est **≥ 0,50**, et les **10 % les plus
exposés concentrent ≥ 35 %** du total des identifications attendues.

**P3 (validation non circulaire).** Le décile de risque estimé contre `humains vague 4`
prédit le succès mesuré contre `humains vagues 1-3 (retest)` — une cible différente :
les 10 % les plus exposés selon v4 concentrent **≥ 25 %** des top-1 réussis contre v1-3.
Ce point est ce qui empêche la concentration d'être un artefact de la mesure qui la
définit.

**P4 (corrélats).** Le risque individuel est **positivement** corrélé à l'atypicité des
réponses (distance au mode de la population sur les mêmes items), Spearman **ρ ≥ 0,20**.
Je prédis une corrélation **plus faible** (|ρ| < 0,15) avec le nombre de réponses non
manquantes et avec la cohérence interne test-retest.

**P5 (défense).** Je prédis que D4 réduit le taux moyen **davantage** qu'elle ne réduit
l'inégalité : le Gini après D4 **ne baisse pas** de plus de 0,10, alors que la moyenne
tombe de plus de deux ordres de grandeur. Autrement dit, je prédis que D4 protège
surtout ceux qui n'étaient pas menacés.

## 4. Ce qui me ferait conclure que le risque est uniforme

**Critère de réfutation, fixé ici, et qui est un livrable de pleine valeur s'il tombe.**
Je conclurai que **le risque est uniforme et que la question d'équité tombe** si les
trois conditions suivantes sont réunies sur la cible principale :

1. Gini de `p_i(100)` **< 0,20** ;
2. part des identifications attendues détenue par le décile supérieur **comprise entre
   10 % et 16 %** (l'uniformité stricte donne 10 %) ;
3. aucun corrélat de §4/P4 n'atteint **|ρ| ≥ 0,15** avec IC 95 % excluant 0.

Dans ce cas l'article écrit que la moyenne est une description fidèle du risque
individuel, que nul n'est singulièrement exposé, et la section d'équité disparaît. Ce
résultat serait **publiable tel quel** et je m'engage à l'écrire sans le requalifier.

Réfutation partielle : si (1) et (2) tombent mais pas (3), je rapporte une concentration
sans corrélat observable identifié — et je dis explicitement que je ne sais pas qui sont
les exposés.

## 5. La défense, et ce qui est décisif

D4 = `c7_defense.defense_d4`, permutation des réponses entre personnes du même segment
`S_gra`, item par item, appliquée **uniquement aux 40 items d'achat**, attaque toujours
sur les 60 items. Reprise à l'identique, mêmes graines.

Trois quantités, toutes préenregistrées :
- moyenne de `p_i(100)` avant / après ;
- Gini et part du décile supérieur avant / après ;
- **le test décisif** : le risque après D4 des personnes qui étaient dans le décile le
  plus exposé **avant** D4, rapporté au risque après D4 des 90 % restants. Si ce rapport
  reste **> 3**, la défense laisse les plus vulnérables relativement plus exposés et
  « taux moyen quasi nul » est une phrase trompeuse. Si le rapport tombe **sous 1,5**, la
  défense égalise réellement.

## 6. Garde-fous

- **Contrôle d'interprétabilité obligatoire.** `controle_avant_interpretation` est appelé
  sur le jumeau cible, sur le bassin exactement attaqué, **avant** toute lecture des
  résultats d'équité. S'il lève `EchecControleInterpretabilite`, rien n'est interprété.
  L'exception n'est pas attrapée pour continuer.
- **Aucune donnée individuelle.** Ni identifiant, ni réponse, ni segment d'une personne
  nommée, ni aucune combinaison de taille < 20. Les corrélats démographiques sont
  rapportés comme moyennes de groupe, et **aucun groupe de moins de 20 personnes n'est
  imprimé**. Publier la liste des plus exposés serait l'exacte contradiction de l'objet
  de l'article.
- **Prudence d'interprétation, écrite ici.** Une corrélation entre exposition et segment
  démographique ne dit **pas** que ce segment est visé, ni que l'attaquant utilise la
  démographie. Elle dit que les réponses de ce segment sont plus distinctives dans ce
  jeu, ce qui peut tenir à sa taille dans l'échantillon, au contenu du questionnaire, ou
  au recrutement. Aucune formulation causale ne sera écrite.
- **Intervalles** : bootstrap sur les personnes (`bootstrap_personnes`, 2 000 tirages),
  graine `20260911` et dérivées stables par `graine_nom`. Le Gini et les parts de décile
  sont ré-estimés **dans chaque tirage** (pas un IC sur la moyenne d'une statistique
  déjà agrégée).
- **Réduction déclarée** : 20 tirages de départage d'ex aequo, comme
  `c7_reidentification`. Aucune autre réduction n'est prévue ; toute réduction décidée à
  l'exécution sera écrite en tête du rapport de résultats.
