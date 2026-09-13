# Préenregistrement — existe-t-il une défense qui résiste à l'attaquant adaptatif ?

statut: courant
mandat: Chercher une défense qui tienne contre un attaquant adaptatif à un coût d'utilité acceptable, après l'effondrement de D4 ; préenregistrer les candidats, leurs attaquants dédiés, les critères de réussite et le seuil d'échec avant toute mesure
agent: Claude Opus 5, Anthropic — sous-agent défense adaptative
ecriture: analyses/c7_defense_adaptative.py, resultats/c7-defense-adaptative-preenregistrement.md, resultats/c7-defense-adaptative-resultats.md, resultats/c7-defense-adaptative.csv
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, toute modification de article/manuscrit.md (un autre agent en est propriétaire)
cecite: je n'ai pas lu article/manuscrit.md ni resultats/article-synthese.md ; je n'ai pas relu les branches non poussées d'autres agents ; je ne mesure que le jeu Twin-2K-500 et la seule configuration `JSON Persona - GPT4.1`, jamais Park et al.
cout_reel_usd: 0.00

**Ce fichier est écrit AVANT `analyses/c7_defense_adaptative.py` et avant tout calcul de
défense.** Il nomme les candidats, l'attaquant dédié de chacun, les critères, les prédictions,
et surtout le seuil en dessous duquel la conclusion publiée est « nous n'avons pas trouvé de
remède ».

---

## 1. Le trou que cette passe essaie de combler

`resultats/audit-comparaison-dp-2026-09-13.md` et `resultats/retractation-dp-d4-2026-09-13.md`
ont établi que D4 (permutation intra-segment, item par item, sur les 40 items d'achat) a deux
défauts nommés :

- **F1** — elle permute item par item, donc republie à l'identique le multi-ensemble
  intra-segment : 1 560 couples segment × item sur 1 560. Son « coût nul » sur la distribution
  et sur les écarts entre groupes **est** cette republication.
- **F5** — elle laisse intacts les 20 items d'opinion. Sur ce bloc seul, protégé et non protégé
  sont indiscernables (0,245 % contre 0,260 %). Le taux de tête sous attaquant adaptatif est
  **0,29 % [0,10 ; 0,53]**.

L'article mesure donc un risque et laisse le praticien sans recours. La question de cette
passe : **existe-t-il une défense qui résiste à l'attaquant adaptatif, à un coût d'utilité
acceptable ?**

## 2. Le bassin, les items, les graines — fixés ici

- **Bassin constant** entre toutes les conditions : les 2 058 personnes couvertes par
  `JSON Persona - GPT4.1`, pool d'attaque = les 2 058 humains vague 4 (monde fermé).
- **Items** : les 60 items communs de `c7_reidentification.items_communs` (40 d'achat,
  20 d'opinion). **Tous les candidats nouveaux s'appliquent aux 60 items**, jamais aux seuls
  40 — c'est le premier des deux défauts de D4 et il se corrige par construction. D4 telle
  qu'elle est publiée reste mesurée, comme référence du défaut.
- **Graine** : `GRAINE = 20260913`, dérivée par nom de condition via
  `c7_reidentification.graine_nom` (crc32), comme partout dans le dépôt.
- **Aucune donnée individuelle** n'est imprimée ni écrite : uniquement des taux agrégés, des
  coûts en points et des réglages de mécanisme.
- `c7_controle_interpretabilite.controle_avant_interpretation` est appelé **avant toute
  interprétation**, sur le bassin exactement attaqué, baseline `Demographics Only` recalculée
  par ce module sur ce même bassin.

## 3. Les candidats, et pourquoi chacun est là

| code | famille | mécanisme | piste du mandat |
|---|---|---|---|
| **A0** | — | aucune défense, jumeau tel que publié | référence haute |
| **D4tq** | permutation | D4 telle qu'elle est publiée : item par item, intra-segment, 40 items d'achat seuls | référence du défaut |
| **E1** | permutation | D4 **étendue aux 60 items**, toujours item par item | piste 1, moitié « tous les items » |
| **E2(B)** | permutation | permutation **jointe** par blocs d'items corrélés, intra-segment, 60 items ; B ∈ {1, 2, 5, 10} blocs, B = 1 étant la ligne entière | piste 1, moitié « jointe » |
| **E3a(k)** | agrégation | groupes de taille ≤ k formés **à l'intérieur de chaque segment** ; chaque membre reçoit le **mode par item** du groupe ; k ∈ {2, 5, 10, 25} | piste 2 |
| **E3b(k)** | agrégation | mêmes groupes ; chaque membre reçoit la ligne **d'un membre tiré au hasard** dans le groupe ; k ∈ {2, 5, 10, 25} | piste 2 |
| **E4(λ)** | fidélité | permutation intra-segment item par item d'une **fraction λ des cellules** seulement ; λ ∈ {0,25 ; 0,50 ; 0,75} (λ = 1 est E1) | piste 3 |
| **E5** | DP | générateur synthétique sous confidentialité différentielle, mécanisme **gaussien composé sous zCDP** (δ = 1e-6), repris de `analyses/c7_dp_zcdp.py` ; deux architectures — marginales d'item, et marginales **conditionnées au segment** — à eps ∈ {1, 3, 10, ∞} | piste 4 |

**Pourquoi l'architecture conditionnée au segment est ajoutée.** Sous remplacement d'une ligne,
une personne ne contribue qu'à **un** segment par item : la sensibilité L2 de l'histogramme
conditionné vaut √2, exactement celle de l'histogramme marginal. Conditionner sur le segment,
covariable publique, **ne coûte donc rien au budget**. Si le plancher d'architecture établi par
`c7-dp-zcdp-resultats.md` (2,6 points sur les écarts entre groupes, à eps = 3 comme à eps = ∞)
vient bien de l'indépendance au segment et non du bruit, cette variante doit l'effacer. C'est
une prédiction, elle est au §6.

## 4. L'attaquant adaptatif, défense par défense — écrit avant la mesure

**Règle.** Un candidat sans attaquant adaptatif dédié ne compte pas. Le taux publié pour chaque
candidat est le **maximum** sur les stratégies ci-dessous, et la stratégie qui l'atteint est
nommée dans le CSV. Chaque candidat est aussi mesuré sous l'attaque naïve, pour que l'écart
naïf → adaptatif soit lisible — c'est précisément l'écart qui a coûté D4.

| stratégie | ce qu'elle exploite | candidats visés |
|---|---|---|
| **N** — naïf (Hamming) | rien ; accord brut sur les 60 items | tous (référence) |
| **L** — A-LLR **recalibré sur la sortie défendue**, hors pli | l'accord apparié et la rareté des modalités, **ré-estimés sur la publication défendue** : c'est ce qui rend cet attaquant adaptatif au sens strict | tous |
| **S1** — colonnes intactes | un bloc d'items que la défense ne touche pas | D4tq seule (les autres couvrent les 60 items) |
| **S3** — invariants de segment | le multi-ensemble intra-segment, conservé à l'identique par toute permutation intra-segment | D4tq, E1, E4 |
| **C** — **lien par le contenu** (nouveau ici) | une permutation ne cache que l'**indice**, jamais le **contenu** : si un bloc d'items d'une personne est republié verbatim quelque part dans la publication, l'attaquant le retrouve en le comparant au dossier humain de la cible, sans jamais avoir besoin de savoir à quelle ligne il a atterri | E2, E3b |

**La stratégie C est celle qui décide de la piste 1**, et elle est écrite ici avant de mesurer :
une permutation jointe d'un bloc à l'intérieur d'un segment laisse le contenu du bloc **intact**
et ne fait que le déplacer. Un attaquant qui apparie par le contenu — et l'attaquant de ce
dépôt apparie par le contenu, jamais par l'indice — ne perd rien. Opérationnellement, la mesure
de C pour un bloc donné est le top-1 obtenu en attaquant les colonnes de ce bloc sur le contenu
**d'origine** : la permutation jointe ne le change pas. Le taux de C est le **maximum sur les
blocs** ; la ligne « au moins un bloc » est aussi portée au CSV.

Pour E3a, la stratégie C n'existe pas (le mode d'un groupe n'est la ligne de personne) et la
**garantie combinatoire** du §5 prend sa place.

## 5. Ce qui sera déclaré GARANTI, et ce qui ne sera déclaré qu'OBSERVÉ

Cette distinction est portée colonne par colonne au CSV (`nature_de_la_protection`).

**Garanti** — trois énoncés seulement, et aucun autre :

1. **E3a(k)** : les k membres d'un groupe reçoivent la **même ligne publiée** (le mode est une
   fonction symétrique du multi-ensemble des membres). Le score attribué par n'importe quel
   attaquant à un humain candidat est donc **identique** pour les k membres, et un seul humain
   peut être classé premier. Donc **au plus 1 des k membres a son humain au rang 1** :
   `top-1 ≤ 1/k`, pour tout attaquant, sans hypothèse. C'est une garantie combinatoire, pas une
   garantie formelle de confidentialité différentielle, et elle ne borne **que** la
   réidentification — jamais la divulgation d'attribut au niveau du groupe.
2. **E3b(k)** : la ligne publiée est celle d'**un** membre tiré uniformément ; par symétrie
   d'échange, `top-1 ≤ top-1(A0)/k`. Contrepartie **à publier avec** : le membre tiré est
   republié **verbatim**, sa divulgation d'attribut est totale. La protection est une moyenne,
   pas un plancher — c'est une inégalité entre personnes, au sens de
   `resultats/c7-equite-risque-resultats.md`.
3. **E5** : (eps, δ)-DP pour la publication des histogrammes, δ = 1e-6, sous remplacement d'une
   ligne, avec immunité au post-traitement pour le jeu synthétique. C'est la **seule garantie
   formelle** de tout ce tableau.

**Observé, et rien de plus** — tout le reste : E1, E2, E4, D4tq. Leurs taux sont ceux des
attaques que nous avons construites, contre des mécanismes sans garantie. Le meilleur attaquant
mesuré n'est pas le meilleur attaquant possible. **Aucun de ces taux n'est une borne.**

**Interdiction reprise de `resultats/marqueurs-canoniques-2026-09-13.md` (I12).** Aucune
revendication de supériorité, dans aucun sens, d'un mécanisme empirique sur la confidentialité
différentielle. Une garantie formelle et une mesure empirique ne se comparent pas sur le seul
coût. Les coûts de E5 sont publiés à côté des autres et ne les classent pas.

## 6. Les critères, fixés avant de voir un chiffre

### 6.1 Protection

**Critère principal (P).** La borne **haute** de l'IC bootstrap à 95 % du top-1 sous attaquant
adaptatif est **strictement inférieure** à la borne **basse** de l'IC de la baseline
`Demographics Only - GPT4.1-mini`, recalculée par `c7_controle_interpretabilite` sur ce même
bassin (≈ 2,15 %). En clair : **publier le jumeau défendu n'identifie pas plus que les
démographies publiques n'identifient déjà**. Le critère est symétrique de celui du contrôle
d'interprétabilité, et il n'est pas arbitraire : il est lu dans le dépôt.

**Critère secondaire (P1%).** top-1 adaptatif < 1,0 %, le seuil déjà tracé sur
`resultats/c7-defense-courbe.png`. Reporté pour continuité, jamais employé seul.

### 6.2 Utilité — les trois tâches en aval de `analyses/c7_utilite_aval.py`

Les trois analyses A, B, C sont rejouées **sans une ligne réécrite**, sur les 40 items d'achat
de chaque publication défendue, et comparées à la publication **non protégée** (A0).

- **T-A** (comparaison de groupes, écart H − F) : préservée si **même signe et même
  significativité** que A0.
- **T-B** (régression MCO, 4 coefficients hors constante) : préservée si **au plus 1 des 4**
  change de signe ou de significativité par rapport à A0.
- **T-C** (ACP) : préservée si |Δ part des deux premiers axes| ≤ 5 points **et** ≤ 20 % des
  40 charges de l'axe 1 inversées, par rapport à A0.

Les **trois composantes abstraites** de `c7_defense` (erreur de distribution, erreur sur les
écarts entre segments, erreur sur les corrélations) sont portées au CSV pour chaque candidat,
avec le **plancher de destruction des corrélations (4,317)** en regard — sans lui, un coût de
4,5 se lit comme un coût alors que c'est le plancher.

### 6.3 Verdict d'utilisabilité

- **Utilisable** = passe **P** **et** préserve **au moins une** des trois tâches.
- **Pleinement utilisable** = passe **P** et préserve **les trois**.
- Toute défense qui passe P en ne préservant **aucune** tâche est déclarée **protectrice et
  inutile**, et ne compte pas comme remède.

### 6.4 LE SEUIL D'ÉCHEC — la clause qui donne sa valeur au reste

**Si aucun candidat ne passe simultanément P et au moins une des trois tâches, alors la
conclusion publiée est : « nous n'avons pas trouvé de remède ».** Pas de repli sur le candidat
le moins mauvais, pas de seuil desserré après coup, pas de tâche redéfinie. C'est un livrable
de pleine valeur, et probablement plus honnête que d'en vendre un mauvais.

Précision qui ferme la porte de sortie : E5 (DP) passera vraisemblablement P **par
architecture** — un générateur qui tire chaque item indépendamment n'a aucune correspondance
un-à-un à fuir, et `registre-chiffres.csv / dp-zcdp-top1-eps3` établit déjà que son top-1 est
le hasard (0,054 % contre 1/2058 = 0,0486 %). **Ce passage ne compte comme remède que si une
tâche au moins survit.** Un mécanisme qui protège parce qu'il ne publie plus rien d'individuel
n'est un remède que s'il reste utile à quelque chose de nommé.

## 7. Les prédictions, écrites avant la mesure

| # | prédiction | ce qui la réfuterait |
|---|---|---|
| **Q1** | **Gagnant attendu : E3a(k), agrégation intra-segment par le mode, à k ≥ 10.** C'est le seul candidat non-DP à porter une garantie, et l'agrégation intra-segment devrait préserver les écarts entre segments (tâche T-A). Prédiction jointe : il **ne** préservera **pas** T-C. | E3a ne passe pas P à k = 25, ou ne préserve aucune tâche |
| **Q2** | **La piste 1 est un cul-de-sac : E2 (permutation jointe) sera réfutée comme réparation de D4.** À bloc large, la stratégie C ramène le taux au niveau non protégé (≈ 20,7 %) alors que le coût d'utilité tombe à zéro. Le « coût nul » de E2(1) est, encore plus que celui de D4, la fuite elle-même. | E2 passe P à un B quelconque |
| **Q3** | **E4 ne donne pas de courbe exploitable :** la protection n'arrive qu'une fois les corrélations détruites (λ → 1). Aucun λ intermédiaire ne passe P en préservant T-C. | un λ ∈ {0,25 ; 0,50 ; 0,75} passe P avec T-C préservée |
| **Q4** | **E5 passe P à tout eps, y compris eps = ∞** — parce que c'est l'architecture et non le budget qui supprime le lien un-à-un. **L'architecture conditionnée au segment préserve T-A là où l'architecture marginale échoue**, et **aucune** des deux ne préserve T-C à aucun eps. | le top-1 de E5 dépasse la baseline démographique ; ou l'architecture conditionnée n'améliore pas les écarts entre groupes |
| **Q5** | **E1 (D4 étendue aux 60 items) protège mieux que D4tq** — elle ferme S1 — **mais ne passe pas le critère de coût** : elle détruit les corrélations comme D4, sur 60 items au lieu de 40. | E1 préserve T-C |
| **Q6** | **Au moins un candidat sera utilisable**, au sens du §6.3. Si Q6 est réfutée, le §6.4 s'applique intégralement. | aucun candidat ne passe P avec une tâche |

## 8. Réductions déclarées d'avance

Contrainte de temps, local seulement, aucun appel payant. Les réductions sont **déclarées ici
avant de mesurer**, jamais choisies après avoir vu un résultat.

- **E5 (DP), mesure de risque : 2 réplicats de générateur** au lieu des 10 de
  `c7_dp_zcdp.py`. Motif : le top-1 d'un générateur synthétique est le hasard et sa dispersion
  inter-graines est sans enjeu pour la question posée. La mesure d'**utilité** de E5 garde
  **5 réplicats**. Aucune de ces deux dispersions n'est un bootstrap sur les personnes ;
  l'étendue publiée est une étendue, jamais un IC.
- **Une seule graine de permutation** par réglage de E1, E2, E4 (pas les 10 réplicats de
  `c7_d4_adaptatif.py`). Motif : `retractation-dp-d4-2026-09-13.md` a mesuré que la dispersion
  inter-tirages de D4 vaut 0,05 à 0,09 point, très en deçà des écarts que nous cherchons. Une
  conclusion qui tiendrait à moins de 0,1 point ne serait pas publiée de toute façon.
- **A-LLR : 5 plis**, valeur de `c7_attaquant_fort.py`, inchangée.
- **Bootstrap : 2 000 tirages de personnes**, valeur du dépôt, inchangée.
- **Un seul jeu (Twin-2K-500) et une seule configuration de jumeau.** Rien de ce qui suit ne
  doit être lu comme valant pour Park et al. ni pour une autre configuration.

## 9. Ce que cette passe ne mesure pas, et ne conclura donc pas

- Aucun **adversaire à connaissance latérale** (qui connaîtrait les |g| − 1 autres membres d'un
  segment). C'est une conséquence par construction, pas une mesure ; elle reste hors de portée
  ici, exactement comme dans `retractation-dp-d4-2026-09-13.md` §3.
- Aucune **composition** entre les publications successives du dépôt.
- Aucune **divulgation d'attribut** mesurée finement, hors les deux constats structurels portés
  au §5 (E3b expose verbatim 1/k des personnes ; E3a divulgue au niveau du groupe).
- Aucun **monde ouvert** : tous les taux sont en monde fermé, comme les 0,29 % et 20,7 %
  auxquels ils doivent rester comparables.
