# Audit d'antériorité des dix-sept prédictions préenregistrées du manuscrit — 13 septembre 2026

statut: courant
fait_foi: article/manuscrit.md à origin/agent/manuscrit/divulgation (e579124), §7.1 et annexe « The seventeen preregistered predictions » ; historique git complet (toutes refs locales)

mandat: établir, pour chacune des dix-sept prédictions du manuscrit, si l'antériorité revendiquée est prouvée par l'historique ; en déduire le compte défendable ; découper les 135 violations de P1 et les 10 de P6 entre forme, substance et faux positifs ; évaluer une déclaration post-hoc dans les portes contre une exception administrateur pour la PR #8
agent: audit / antériorité des prédictions, 13/09
ecriture: resultats/audit-anteriorite-predictions-2026-09-13.md
lecture_seule: tout le reste du dépôt, article/manuscrit.md et outils/portes/ compris
interdits: appel payant, réseau, recherche web, commit sur master, fusion, push sur agent/manuscrit/divulgation, écriture hors du fichier du mandat
cout_reel_usd: 0.00

---

## 0. Réponse courte

**Non, l'antériorité n'est pas prouvée pour les dix-sept prédictions.** Sur les dix-sept :
**11 prouvées** par l'ordre des commits, **5 non prouvées**, **1 postérieure**. **Aucune** n'a de
reçu OpenTimestamps : `git log --all --name-only | grep '\.ots$'` ne renvoie rien, et le
répertoire `preuves/` n'a jamais existé. « Prouvée » veut donc dire ici « prouvée par des dates
de commit que nous écrivons nous-mêmes ». Aucun tiers n'a horodaté quoi que ce soit.

Sur les **treize réfutations**, **9** reposent sur une antériorité prouvée par l'historique.
**3** ne sont pas prouvées (lignes 1, 12 et 13). **1 n'est pas une réfutation préenregistrée**
(ligne 4) : la prédiction telle qu'elle était préenregistrée a été **confirmée**. La
« réfutation » vient d'un découpage en sous-groupe écrit après les résultats.

Les deux portes rouges de la PR #8 ne voient **aucune** des dix-sept prédictions. Les 135 + 10
violations portent sur dix préenregistrements nouveaux de la PR, dont aucun ne figure au
Tableau 1. Les faiblesses réelles du Tableau 1 sont antérieures à la base de la PR
(`abd5752`), donc invisibles pour les portes.

## 1. Méthode

- Base de la PR : `git merge-base HEAD origin/master` = `abd5752` = `origin/master`. La PR compte
  94 commits.
- Pour chaque fichier : `git log --all --follow --diff-filter=A --format='%h %ad %cd %p'
  --date=iso-strict`. Les dates d'auteur et de commit sont comparées. Les correspondances entre
  préenregistrement, script et résultat viennent des renvois écrits dans les fichiers de
  résultats.
- Le texte de chaque prédiction est relu **au commit d'ajout** (`git show <sha>:<fichier>`),
  puis comparé à la formulation du Tableau 1.
- Réordonnancement : sur toutes les refs, aucun commit n'a une date de commit antérieure à celle
  d'un de ses parents. **12** commits ont une date d'auteur différente de leur date de commit.
  Les **6** écarts de plus de 5 minutes datent tous du 12/09 entre 22:16 et 22:24
  (`edbf900`, `a9391a8`, `d8fb2f8`, `1ae6cd6`, `e850885`, `684072c`). Ce sont des commits de
  portes et de mise en page, aucun n'est un préenregistrement ni un résultat des dix-sept. Le
  seul écart qui touche un fichier du Tableau 1 est `9de447d` : 90 secondes, sur le CSV marginal
  de la ligne 1, lui-même écrit après coup. **Aucun écart suspect sur les commits qui fondent
  l'antériorité.**
- Corroboration partielle : le reflog local enregistre un « update by push » vers
  `origin/master` quelques secondes après chaque commit concerné (par exemple `ffe4ed8` poussé à
  00:56:09 et `020d88c` à 01:01:01). Ce reflog est local et modifiable : ce n'est pas une preuve
  tierce. Les journaux de push côté GitHub en seraient une, mais je ne les ai pas consultés
  (réseau exclu).
- Critères. **Prouvée** : préenregistrement dans un commit strictement antérieur au premier
  résultat, sans réserve déclarée, et texte de la prédiction identique au Tableau 1. **Non
  prouvée** : même commit, ou préenregistrement commis alors que les résultats existaient déjà
  sur disque (réserve déclarée dans le message de commit). **Postérieure** : la prédiction
  réfutée du Tableau 1 n'existe qu'après les résultats.

## 2. Les dix-sept, une par une

Toutes les heures sont en +02:00. Pour tous les commits cités, date d'auteur = date de commit.
Colonne OTS : aucun reçu pour aucune ligne.

| # | Verdict du Tableau 1 | Préenregistrement (commit, date) | Script (premier commit) | Premier résultat | Classement |
|---|---|---|---|---|---|
| 1 | Réfutée | `c7-disjoint-preenregistrement.md` `75362f7` 12/09 01:44:59, prédiction (b) ; protocole du nul corrigé (100 réplicats « as preregistered ») : `c7-nul-corrige-preenregistrement.md` `5c4cef4` 12/09 11:39:23 | `c7_disjoint.py` `37b58b2` 02:20:36 ; `c7_nul_corrige.py` `09b18d7` 13:25:16 | `37b58b2` (témoin défectueux) ; `09b18d7` ; CSV cité `9de447d` 13/09 03:24:31 | **Non prouvée** (voir §3.1) |
| 2 | Réfutée telle que mesurée d'abord | `c7-monde-ouvert-preenregistrement.md` `ffe4ed8` 12/09 00:56:07 (> 5 % / > 30 %) | `020d88c` 01:01:00 | `020d88c` | **Prouvée** (moitié Park de la ligne : `71f663b`, même commit) |
| 3 | Réfutée | `c7-transfert-stanford-preenregistrement.md` `08cb04d` 02:28:30 (≥ 20 %) | `da821ff` 02:31:23 | `da821ff` | **Prouvée** (écart de 3 min) |
| 4 | Réfutée (paires à 19 items) | `c7-transfert-preenregistrement.md` `9f118a9` 00:55:09 : « top-1 moyen ≥ 15 % sur les 42 paires riches » | `921635d` 01:21:30 | `921635d` : **« confirme, 26,11 % obtenu »** | **Postérieure** (voir §3.2) |
| 5 | Réfutée (H1) | `c7-mecanisme-preenregistrement.md` `0876366` 11/09 22:29:58 | `6077e45` 22:36:27 | `6077e45` | **Prouvée** |
| 6 | Réfutée (H4) | même fichier, `0876366` | `6077e45` | `6077e45` | **Prouvée** |
| 7 | Réfutée | `c7-deviations-preenregistrement.md` `21bb76b` 00:49:14 (≥ 80 %) | `ff1cb71` 01:21:49 | `ff1cb71` | **Prouvée** |
| 8 | Réfutée | `c7-gen-preenregistrement.md` `1335577` 00:51:31 (≥ 10 % sur 2 modèles sur 3) | `084e633` 00:58:05 | `084e633` | **Prouvée** |
| 9 | Non concluante | `c7-recette-preenregistrement.md` `c83a4fb` 01:05:31 | `c83a4fb` (**même commit que le préenregistrement**) | `07c2265` 01:10:56 | **Prouvée** vis-à-vis du résultat |
| 10 | Réfutée à échantillon égal | `c7-compromis-bits-preenregistrement.md` `5c1d190` 01:16:08 (« CV(ratio 2) < CV(ratio 1), facteur ≥ 2 ») | `19095cc` 01:17:31 | `19095cc` (facteur 0,70) ; ré-analyse à échantillon égal `02d8f3a` 01:46:47 (0,82) | **Prouvée** (83 s d'écart ; la correction post-relecture ne change pas le sens) |
| 11 | Réfutée | `c7-bits-preenregistrement.md` `7ddb1c1` 00:45:58 + avenant `26aaff4` 00:54:32 (« mêmes signes sur les deux jeux ») | `1e314ce` 01:06:25 | `1e314ce` | **Prouvée** |
| 12 | Réfutée sur Twin | `c7-attaquant-fort-preenregistrement.md` `71f663b` 07:12:56, [P1] | `71f663b` | `71f663b` | **Non prouvée** (un seul commit pour les trois) |
| 13 | Réfutée, pour la défense | même fichier, addendum « avant calcul » [P3], `71f663b` | `71f663b` | `71f663b` | **Non prouvée** |
| 14 | Retirée | `c7-dp-preenregistrement.md` `6295702` 07:12:13 | `6295702` | `6295702` | **Non prouvée** |
| 15 | Réfutée | `c7-fort-preenregistrement.md` `26b681b` 06:51:29 (exactitude > 0,55) | `30d3876` 06:55:43 | `4e3e32d` 07:14:21 | **Prouvée** (script lui aussi postérieur) |
| 16 | Non concluante | même fichier (top-1 > 5 %) | `30d3876` | `4e3e32d` | **Prouvée** |
| 17 | Non testable | `c7-deux-organisations-preenregistrement.md` `24cc79d` 12/09 12:46:10 | `09b18d7` 13:25:16 | `09b18d7` | **Non prouvée** : le message de `24cc79d` déclare que les résultats existaient déjà sur disque |

Effectifs : **prouvées 11** (lignes 2, 3, 5, 6, 7, 8, 9, 10, 11, 15, 16) ; **non prouvées 5**
(lignes 1, 12, 13, 14, 17) ; **postérieure 1** (ligne 4).

## 3. Les trois cas qui changent le compte

### 3.1 Ligne 1 : la prédiction est prouvée, le protocole du verdict ne l'est pas

La prédiction (b), « rho observé > 95e centile du nul », est écrite en `75362f7`, avant
`37b58b2`. Mais le verdict qui fait foi aujourd'hui (nul corrigé, 12 configurations, « 100
replicates as preregistered ») applique le protocole de `c7-nul-corrige-preenregistrement.md`.
Ce fichier est commis en `5c4cef4`, dont le message dit mot pour mot : « les fichiers de
résultats correspondants existaient deja sur le disque au moment de ce commit. L'ordre des
commits etablit donc une anteriorite faible, pas une preuve ». Le résultat suit en `09b18d7`, qui
**modifie aussi** ce préenregistrement (+10 lignes). Vérifié : l'ajout se limite au bandeau de
rétractation, les prédictions ne changent pas. Le CSV cité au Tableau 1 apparaît en `9de447d`,
le 13/09. L'intitulé du témoin qui tranche n'a donc pas d'antériorité prouvée. Une lecture
indulgente, qui ne regarderait que le texte de la prédiction, reclasserait cette ligne en
« prouvée » : on passerait à 10 sur 13. Je retiens la lecture stricte, parce que le manuscrit
revendique aussi le protocole (« as preregistered »).

### 3.2 Ligne 4 : ce n'est pas une réfutation préenregistrée

Ce qui a été préenregistré en `9f118a9` : « top-1 moyen ≥ 15 % sur les 42 paires riches ». Au
premier résultat, en `921635d`, le rapport écrit **« confirme, 26,11 % obtenu »**. Le découpage
« confirmé pour les 30 paires à 60 items, **rejeté pour les 12 paires à 19 items** » apparaît en
`02d8f3a` (12/09 01:46:47, « corrections après relecture hostile »). La formulation anglaise du
Tableau 1 (« 19-common-item pairs ») n'entre dans le manuscrit qu'en `0fb0f8f`. Le découpage est
légitime comme analyse, mais la prédiction réfutée **a été formulée après les résultats**, et la
prédiction réellement préenregistrée a été confirmée. Compter cette ligne parmi les « thirteen
preregistered predictions refuted » est inexact, quel que soit l'horodatage.

### 3.3 Lignes 12 et 13 : un seul commit

`71f663b` ajoute d'un coup le préenregistrement (avec l'addendum du volet adaptatif), le script
`analyses/c7_attaquant_fort.py`, les résultats et le CSV. Le recueil
(`preenregistrements-recueil-2026-09-12.md` §2.2) et l'autopsie (`autopsie-methode-2026-09-12.md`
§4.1) le disent déjà. Git ne restitue aucun ordre à l'intérieur d'un commit. Ces deux
réfutations sont justement les deux que le §7.1 marque « en notre faveur ». La ligne 14 (DP,
`6295702`) est dans le même cas, mais elle est retirée.

### 3.4 Écart avec les documents précédents

Le recueil et l'autopsie comptaient « aucune inversion » et « 24 paires propres ». Ils avaient
raison sur l'ordre des **fichiers**. Aucun des deux ne compare le **texte** de la prédiction
réfutée au texte préenregistré : c'est ce qui laisse passer la ligne 4. Par ailleurs, l'autopsie
ne qualifie de « prouvée » que `c7-factoriel`, parce que son script était absent du dépôt au
commit de préenregistrement. Ce critère est rempli aussi par les lignes 2, 3, 5 à 8, 10, 11 et
15 : leur script apparaît, à chaque fois, dans un commit postérieur au préenregistrement
(tableau du §2). Les deux documents appliquent donc le même mot à des preuves de même nature.

## 4. Le compte, et ce que le manuscrit peut écrire

- Réfutations dont l'antériorité est prouvée par l'historique : **9 sur 13** (lignes 2, 3, 5, 6,
  7, 8, 10, 11, 15).
- Préenregistrées selon nos notes, mais commises avec leur résultat ou après son existence sur
  disque : **3** (lignes 1, 12, 13).
- Réfutation d'une prédiction formulée après les résultats : **1** (ligne 4). La prédiction
  préenregistrée correspondante est confirmée.
- Aucune des dix-sept n'a de reçu d'horodatage tiers.

Formulation défendable pour le §7.1 et le résumé (l. 43, l. 206, l. 1012) :

> Seventeen predictions are listed in Table 1; no third-party timestamp exists for any of them.
> For eleven (nine refuted, both inconclusive), git history shows the preregistration committed
> strictly before the first result. Five (rows 1, 12, 13, 14, 17) were written before computation
> according to our records but committed with, or after the on-disk existence of, their results.
> Row 4 is not a preregistered refutation.
>
> **Nine of the thirteen refutations** rest on a preregistration that git history shows
> committed strictly before the first result, with no third-party timestamp. **Three** (rows 1,
> 12, 13) were written before computation according to our records but committed with, or after
> the on-disk existence of, their results, so their precedence is not independently verifiable.
> **Row 4 is not a preregistered refutation**: the preregistered prediction was confirmed
> (26.11 % ≥ 15 %), and the refuted subgroup was defined after the results.

Conséquence mécanique : le titre « The thirteen refuted preregistered predictions » (l. 1010), la
phrase « Seventeen predictions were registered before computation » (l. 1012) et « Thirteen
preregistered predictions were refuted » (l. 43, l. 206) ne sont pas défendables tels quels.
« Registered before computation » est une affirmation sur l'ordre du calcul, que l'historique ne
prouve pour aucune ligne. Il prouve seulement l'ordre des commits, pour onze lignes. La ligne 4
doit sortir du compte des réfutations préenregistrées ou être requalifiée.

## 5. Découpe des 135 violations de P1 et des 10 de P6

Reproduction locale : `preenregistrement_seul.py --depuis abd5752` renvoie **135** violations
(21 « commit seul » + 114 « PAP complet »). `horodatage.py --depuis abd5752` renvoie **10**
violations. Les dix fichiers visés sont `c7-{attaquant-imparfait, controle-generateur,
decomposition-signal, defense-adaptative, equite-risque, pilote-regeneration,
residu-trajectoire, t1a-complements, temoins-relecture, variance-generation}-preenregistrement.md`.
**Aucun n'est une des dix-sept prédictions.**

### 5.1 Les 114 violations PAP : toutes de forme

Elles portent sur 9 fichiers (`defense-adaptative` est conforme) : 11 à 13 manques par fichier.
Détail : les clés `famille`, `rang`, `commit_parent` et `horodatage_ots` (9 × 4) ; les sections
A1 n° 2, 3, 6, 7 et 8 (9 × 5) ; la section 5 (8), les sections 1 et 4 (7 chacune) ; la mention
« vu échouer » (9) ; la clause « aucun appel » (2). Toutes peuvent être ajoutées honnêtement.
Condition : écrire la vérité, c'est-à-dire la date réelle d'ajout de l'en-tête,
`horodatage_ots: absent`, et le statut post-hoc là où il s'impose (§5.3). Ajouter un en-tête ne
crée aucune antériorité et ne doit pas donner l'impression d'en créer une.

### 5.2 Les 21 violations « commit seul »

Contrôle : `git show -m --first-parent` sur chaque commit de la plage. Sur un commit de fusion, ce
diff contient toute la branche fusionnée, si bien qu'un préenregistrement correctement isolé sur
sa branche apparaît « commis avec » son script.

- **Substance, 4** : commits ordinaires (un seul parent) qui ajoutent préenregistrement, script
  et résultats ensemble.
  - `048a5d2` temoins-relecture. Le fichier se titre « préenregistrement écrit APRÈS coup, et qui
    le dit ».
  - `05ee24f` controle-generateur.
  - `9846a5f` residu-trajectoire.
  - `d0213d1` variance-generation.
- **Faux positifs de fusion, 17** : `b763533`, `47644be`, `08553d4`, `8d6df5d`, `b1e00d1`,
  `0139804`, `ea2a5d2`, `57a7c1c`, `40c56e9`, `8e65b5d`, `76ee619`, `ed4f564`, `5bd993e`,
  `fa1164b`, `93eee14`, et `dea6dad` × 2 (« 4 préenregistrements à la fois » et « touche »).
  - **7** de ces fusions **répètent** les 4 cas de substance ci-dessus (`b1e00d1`, `0139804`,
    `08553d4`, `8d6df5d`, `40c56e9`, `8e65b5d`, `fa1164b`).
  - **10** visent des préenregistrements dont le commit réel est isolé :
    - attaquant-imparfait `0bce8af` 03:19:23, résultat `ac421e7` 03:33:11 ;
    - defense-adaptative `3e3f128` 10:11:30, résultat `de1e3c6` 10:38:25 ;
    - decomposition-signal `4e0c6d4` 10:17:23, résultat `01c2af2` 10:31:46 ;
    - pilote-regeneration `4684d8e` 10:59:30, résultat `c719230` 11:05:17 ;
    - t1a-complements `d8f9388`, résultat `a788385` ;
    - equite-risque `87c46a2`, résultat `b4c3a8e`, **à la même seconde (03:28:52)** : séparation
      formelle, antériorité nulle en substance ;
    - soit 8 violations (`ed4f564`, `5bd993e`, `93eee14`, `76ee619`, `ea2a5d2`, `57a7c1c`,
      `b763533`, `47644be`), plus les 2 de `dea6dad`.
- **Le commit de fusion temporaire de GitHub.** Il ne fait **pas** partie des 135 locales : il n'y
  a pas de commit synthétique en local. J'en ai simulé un (`git commit-tree` sur
  `merge-tree origin/master HEAD`, objet `e8a6334`, aucune ref créée) : il ajoute **exactement 2**
  violations (« 10 préenregistrements à la fois » et « touche »), soit 137. Si la CI affiche 135,
  ou bien sa plage diffère de `abd5752..HEAD`, ou bien les « 2 suspectes » sont en fait la paire
  de `dea6dad`, une vraie fusion d'intégration, mais un artefact du même mécanisme. Impossible à
  trancher sans le journal de la CI (réseau exclu).

**Découpe de P1** : **forme 114** ; **substance 4** ; **faux positifs 17**, dont 7 doublons de la
substance et 10 fusions sur des fichiers isolés. Le synthétique GitHub, lui, est absent du compte
local. Si l'on compte l'antériorité **par fichier** et non par violation, il s'ajoute 1 cas de
substance que P1 ne voit pas (equite-risque, même seconde) et 1 fichier post-hoc déclaré, que P1
voit seulement sur ses fusions (t1a-complements, « Les cinq volets décrits ici sont POST HOC et
NON PRÉENREGISTRÉS »).

### 5.3 Recoupement avec les 10 de P6

Les 10 violations de P6 visent exactement les mêmes 10 fichiers. Par fichier :

- **Antériorité non prouvable, 5** : temoins-relecture (même commit, post-hoc déclaré),
  controle-generateur, residu-trajectoire, variance-generation (même commit), equite-risque
  (même seconde).
- **Post-hoc déclaré, commit isolé, 1** : t1a-complements.
- **Ordre prouvé par l'historique, 4** : attaquant-imparfait, defense-adaptative,
  decomposition-signal, pilote-regeneration. Le manuscrit (l. 1547) cite defense-adaptative
  comme « committed before any measurement ». C'est cohérent avec `3e3f128` antérieur à
  `de1e3c6`.

Aucun des 10 n'a de `.ots`, pas plus que les ~70 autres préenregistrements du dépôt. P6 ne
contrôle que les fichiers touchés : lancée avec `--tous`, elle échouerait sur tous. Pour les 4
fichiers bien ordonnés, P6 est une dette d'outillage. Pour les 6 autres, un `.ots` posé
aujourd'hui horodaterait le 13/09 **après** les résultats, et ne prouverait rien de plus.

## 6. Les deux issues

### (a) Déclaration post-hoc dans P1 et P6

Principe : un préenregistrement portant `statut: post-hoc` (avec `commit_resultats:` et un motif)
passe P1 (a) et P6 ; un préenregistrement non déclaré bloque toujours.

Ce qui le rendrait impossible à abuser :
1. **La porte déduit le statut de git, elle ne le lit pas seulement.** Si le commit ordinaire
   (hors fusion, `git log --no-merges --diff-filter=A`) qui introduit le préenregistrement
   introduit aussi un script ou un résultat du même préfixe, ou si le premier résultat suit à
   moins de N secondes, alors `statut: post-hoc` est **obligatoire**. Une déclaration
   « préenregistré » contredite par git bloque. Cette règle couvre le cas equite-risque (même
   seconde, deux commits), que le contrôle actuel laisse passer.
2. **Déclaration irréversible.** P1 lit l'historique de la clé : un `statut: post-hoc` ne peut
   jamais redevenir « préenregistré ».
3. **Couplage au manuscrit (le point décisif).** Une porte du type P5/P9 refuse `preregistered`,
   `registered before computation` ou `préenregistré` à moins de N lignes d'un renvoi vers un
   fichier post-hoc, et impose l'étiquette `exploratory`. Le Tableau 1 prend une colonne
   « antériorité : horodatée / ordre git / déclarée / post-hoc », calculée par la porte à partir
   de git, non saisie à la main. Sans ce couplage, la déclaration post-hoc reste un contournement
   discret.
4. **Correction du faux positif de fusion** : ne juger que les commits ordinaires. Sinon, un
   préenregistrement correctement isolé est bloqué, et la déclaration post-hoc devient la sortie
   de secours utilisée même quand elle est fausse, ce qui serait un abus dans l'autre sens.
5. **P6** : exiger le `.ots` pour tout statut autre que post-hoc, **dans le commit du
   préenregistrement** (ou juste après, avant le premier résultat), et non « avant fusion sur
   master ». Aujourd'hui la règle accepte un reçu posé après les résultats.

Ce qu'elle protège : l'historique reste vrai, le travail honnête n'est pas bloqué, et l'étiquette
suit la preuve jusque dans l'article. Ce qu'elle laisse passer : un préenregistrement écrit
**après** le calcul puis commis seul avant le résultat. C'est exactement le cas `5c4cef4` /
`24cc79d`, et seul un horodatage tiers pris **au moment de l'écriture** le fermerait. Elle ne
touche pas non plus aux dix-sept, antérieures à la base de toute PR future, sauf à lancer une
fois le contrôle sur tout l'historique. Relecteur PoPETs lisant l'historique : il voit des portes
qui ont rattrapé le problème et une étiquette qui descend jusqu'au texte. C'est crédible, **à
condition** que le Tableau 1 soit corrigé en même temps. Sinon il verra une porte assouplie la
veille de la soumission.

### (b) Exception documentée pour la PR #8, fusion administrateur

Ce qu'elle protège : l'historique (rien n'est réécrit) et la règle pour les PR suivantes. Ce
qu'elle laisse passer : les 4 commits de substance, equite-risque, les 2 post-hoc déclarés, 114
en-têtes incomplets, 10 préenregistrements sans reçu, et surtout **tout le Tableau 1**, que P1 et
P6 ne regardent pas. L'exception règle le symptôme de la CI sans rien dire des lignes 1, 4, 12, 13
et 17. Relecteur PoPETs lisant l'historique : il voit une fusion administrateur contournant la
porte d'antériorité **sur la PR même qui porte le manuscrit**, dont la crédibilité repose sur
l'antériorité. La lecture la plus probable est défavorable, même si la note d'exception est
exacte. Elle ne devient neutre que si la note énumère les fichiers, leur statut réel et les
corrections du manuscrit qui l'accompagnent.

### Constat commun aux deux issues

Aucune ne corrige le manuscrit. Les deux problèmes sont indépendants : le rouge de la CI concerne
10 fichiers hors Tableau 1, tandis que la sur-affirmation concerne le Tableau 1 et les lignes 43,
206, 1010 et 1012. L'issue (a) peut les relier (point 3). L'issue (b) les laisse disjoints.

## 7. Traçabilité

Commits cités, tous vérifiés dans l'arbre `/tmp/wt-anteriorite` (branche
`agent/audit/anteriorite-predictions`, créée depuis `origin/agent/manuscrit/divulgation` à
`e579124`) : `75362f7`, `37b58b2`, `5c4cef4`, `09b18d7`, `9de447d`, `ffe4ed8`, `020d88c`,
`08cb04d`, `da821ff`, `9f118a9`, `921635d`, `02d8f3a`, `0fb0f8f`, `0876366`, `6077e45`,
`21bb76b`, `ff1cb71`, `1335577`, `084e633`, `c83a4fb`, `07c2265`, `5c1d190`, `19095cc`,
`7ddb1c1`, `26aaff4`, `1e314ce`, `71f663b`, `6295702`, `26b681b`, `30d3876`, `4e3e32d`,
`24cc79d`, `abd5752`, et pour la PR `048a5d2`, `05ee24f`, `9846a5f`, `d0213d1`, `0bce8af`,
`ac421e7`, `3e3f128`, `de1e3c6`, `4e0c6d4`, `01c2af2`, `4684d8e`, `c719230`, `d8f9388`,
`a788385`, `87c46a2`, `b4c3a8e`, `dea6dad`. Objet de fusion simulé `e8a6334` : non référencé, il
sera supprimé par le ramasse-miettes de git.
