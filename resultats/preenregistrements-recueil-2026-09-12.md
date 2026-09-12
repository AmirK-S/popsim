# Recueil des préenregistrements — dossier de dépôt tiers

## Page de garde

- **Projet** : popsim — article C7 (« le jumeau ne prédit pas, mais retrouve-t-il la personne ? »), défense contre le reproche de dragage de données (p-hacking).
- **Auteur** : Amir Kellou Sidhoum (auteur de tous les commits git cités ci-dessous ; assistance Claude Sonnet 5 / Claude Opus 5 co-autrice de plusieurs commits, voir les messages de commit).
- **Date de rédaction de ce recueil** : 12 septembre 2026.
- **Condensé du dépôt courant** (`git rev-parse HEAD`, mis à jour lors de la troisième correction
  du 12 septembre 2026, soir — voir §2.4, §3.3 et §4) :
  `8df4e685925204416baa84245b8c8e6734695f84` (« T2 requalifiée en non testable : le compteur
  tombe à 14 »). Les condensés précédents, `ee73f708456033d4f919206fa20ac47b348cb093` — condensé
  de la seconde correction —, `5c4cef48d40db4046cbb51b1bd02d1fea239573e` — condensé de la
  première correction, fin de matinée — et `23eec0072a08569837a7cf10470d7ffc5ba1f712` — condensé
  initial —, en sont tous des ancêtres (`git merge-base --is-ancestor` vérifié pour chacun contre
  le nouveau HEAD). Entre le condensé précédent et celui-ci, un arbitrage
  (`resultats/c7-reconciliation-facteurs-2026-09-12.md`, commit `5f6da6e`) a établi que les
  jumeaux des deux bras payés de la nuit — le témoin « deux organisations » et le plan factoriel —
  retrouvent la bonne personne au taux du hasard, et qu'un contrôle de validité gratuit
  (`analyses/c7_controle_interpretabilite.py`, commit `28405b2`) qui aurait dû être exigé avant
  ces deux appels payés a été écrit et testé après coup. Voir §2.4 et §3.3, révisés en
  conséquence.
- **Nombre de préenregistrements recensés** : **59** fichiers `*-preenregistrement.md` dans `resultats/` (hors `manifeste-preenregistrements.txt`, qui est un document récapitulatif antérieur, partiel, et non lui-même un préenregistrement) — 58 lors de la première rédaction, +1 (`c7-factoriel-preenregistrement.md`, §2.4 et §3.3) constaté à la seconde correction. Ce compte de fichiers ne change pas à cette troisième correction : c'est le verdict de deux d'entre eux qui est révisé, pas leur existence ni leur antériorité.

Ce recueil ne modifie aucun fichier existant. Il a été écrit en lecture seule sur tout le dépôt
à l'exception de lui-même.

---

## 1. Méthode et périmètre

Le dépôt contient deux familles de préenregistrements :

- **Tier 1 — le chantier C7** (réidentification par jumeau, l'article en cours de rédaction dans
  `article/manuscrit.md` et `resultats/article-synthese.md`) : 35 fichiers (34 à la première
  rédaction, +1 avec `c7-factoriel-preenregistrement.md` constaté à cette seconde correction),
  traités en détail ci-dessous (§3). Inclut, à la demande explicite, les deux préenregistrements
  du tournoi
  « Twin A→B » (`tab`, `tab2`), qui appartiennent à un chantier voisin mais dont le mémo de
  l'utilisateur signale qu'ils attendent aussi un dépôt OSF.
- **Tier 2 — autres chantiers du dépôt** (oracle des camps R1-R7, mémoire à long terme,
  anticipations des ménages C1, détection de population synthétique I1/I3/I3b, etc.) : 24
  fichiers, hors périmètre de l'argument anti-dragage de « notre article » C7. Listés au §6
  avec date et empreinte, sans analyse de verdict (ce n'est pas leur article qui est déposé ici).

**Avertissement sur les fichiers en cours d'écriture.** Au moment de la rédaction initiale, git
status signalait des modifications non commises sur `resultats/article-travaux-connexes.md` et
`resultats/positionnement-vie-privee-2026-09-12.md`, et de nombreux fichiers non suivis. Ce
recueil n'a pas lu le contenu courant de `article/manuscrit.md` ni d'`article-synthese.md` pour en
tirer des conclusions (ils peuvent changer sous nos pieds — au moment de cette seconde correction,
`article/manuscrit.md` porte encore des modifications non commises et cinq agents travaillent en
parallèle dessus ainsi que sur `resultats/article-synthese.md`, `resultats/moonshot-2026-09-12.md`,
`resultats/reproductibilite-chaine-2026-09-12.md`, `resultats/troisieme-jeu-2026-09-12.md` et
`demandes/`) ; il s'appuie sur les fichiers de résultats et de correction eux-mêmes, sur trois
rapports de correction datés du 12/09 (§4 — les deux déjà lus à la première rédaction, plus
`resultats/audit-chiffres-2026-09-12.md`, trouvé committé et plus complet à cette seconde
correction), ainsi que sur un audit adverse et sa réponse concédée, également du 12/09 (§3.3). Le
cas `c7-deux-organisations-*`, signalé non stabilisé à la première rédaction puis stabilisé mais
non commis à la première correction, est désormais **entièrement commis dans git**, préenregistrement
et résultat, chacun dans un commit séparé et dans le bon ordre — voir §2.3 et §3.3. Un cinquième
préenregistrement C7, `c7-factoriel-preenregistrement.md`, est apparu depuis la première
correction ; c'est le seul cas du dossier dont l'antériorité est prouvée, et non simplement
déclarée, par l'historique git — voir §2.4 et §3.3.

---

## 2. Vérification de l'antériorité — le point le plus important

Pour chaque paire préenregistrement/résultat du Tier 1, la date qui fait foi est celle de la
**première apparition du fichier dans l'historique git** (`git log --follow --diff-filter=A`),
pas la date de modification sur disque.

### 2.1 Cas normaux (24 paires)

Pour 24 des 28 paires vérifiables (tous les fichiers `c7-*` sauf les trois listés en 2.2, plus
`c7-preenregistrement.md`/`c7-resultats.md`, `a1-controle`, `c5`, `b123`), le préenregistrement
apparaît dans un commit strictement antérieur à celui du résultat, avec un écart de plusieurs
minutes à plusieurs heures. **Aucune inversion trouvée** : dans aucun de ces 24 cas le fichier de
résultats n'est apparu avant son préenregistrement.

### 2.2 Trois cas non vérifiables : préenregistrement et résultat commis ensemble

Pour **trois** paires, le préenregistrement et le fichier de résultats ont été ajoutés dans **le
même commit git** (même hash, même horodatage à la seconde) :

| Préenregistrement | Résultat | Commit unique |
|---|---|---|
| `c7-dp-preenregistrement.md` | `c7-dp-resultats.md` | `6295702a05da12c012589d3e901ab8f2b908e1a5` (12/09 07:12:13) |
| `c7-utilite-aval-preenregistrement.md` | `c7-utilite-aval-resultats.md` | `fe02537dac27d7a1431312647526c80e786c74f7` (12/09 07:09:58) |
| `c7-attaquant-fort-preenregistrement.md` | `c7-attaquant-fort-resultats.md` | `71f663ba18f47d214f3cf19e0a5718774ba2b9ce` (12/09 07:12:56) |

Dans les trois cas, le commit contient à la fois le script d'analyse (`analyses/c7_*.py`), le
préenregistrement et les résultats. **Git ne peut pas, à partir de l'historique seul, prouver que
le texte du préenregistrement a été écrit avant l'exécution du calcul** dans ces trois cas
précis : la granularité du commit ne descend pas en dessous de la seconde, et un commit unique
ne restitue aucun ordre interne entre les fichiers qu'il contient. Rien n'indique une fraude
(les messages de commit décrivent un travail cohérent avec l'ordre déclaré), mais l'argument
« antériorité prouvable par git » ne tient pas, tel quel, pour ces trois tests. C'est une faiblesse
réelle à ne pas dissimuler au moment du dépôt.

### 2.3 Mise à jour du 12/09 (fin de matinée puis correction) : quatre préenregistrements commis seuls, leurs quatre résultats désormais commis aussi

Depuis la première rédaction de ce recueil, le commit `5c4cef48d40db4046cbb51b1bd02d1fea239573e`
(12/09 11:39:23+02:00, « Preenregistrements de la nuit : horodatage separe des resultats ») a
ajouté au dépôt, **seuls et séparément de leurs fichiers de résultats** :

| Préenregistrement | Commis dans | Résultat correspondant |
|---|---|---|
| `c7-nul-corrige-preenregistrement.md` | `5c4cef4` (12/09 11:39:23+02:00) | `c7-nul-corrige-resultats.md` |
| `c7-tautologie-preenregistrement.md` | `5c4cef4` (12/09 11:39:23+02:00) | `c7-tautologie-resultats.md` |
| `c7-temoin-prompt-preenregistrement.md` | `5c4cef4` (12/09 11:39:23+02:00) | `c7-temoin-prompt-resultats.md` |

Le message de ce commit **déclare lui-même sa limite**, et ce recueil la reprend telle quelle :
« les fichiers de résultats correspondants existaient déjà sur le disque au moment de ce commit.
L'ordre des commits établit donc une antériorité faible, pas une preuve. » Autrement dit : le
texte du préenregistrement est horodaté par un commit git vérifiable et poussable, mais comme le
calcul et sa sortie existaient déjà sur le disque avant ce commit, git ne peut pas, à lui seul,
prouver que ce texte a été écrit avant l'exécution du calcul.

**Une quatrième paire, `c7-deux-organisations`, suit le même schéma, commise un peu plus tard et
seule** : le commit `24cc79d867b7944536651c21114c7629b9f496fc` (12/09 12:46:10+02:00,
« Preenregistrement du temoin deux organisations ») ajoute
`c7-deux-organisations-preenregistrement.md` seul, avec la **même limite déclarée dans son propre
message de commit**, mot pour mot : « les fichiers de résultats existaient déjà sur le disque.
L'ordre des commits établit une antériorité faible, pas une preuve. » (Ce point corrige la
première correction de ce recueil, qui affirmait que cette paire n'était « pas commise » : c'était
vrai à la première rédaction, ce ne l'était déjà plus à la première correction pour le
préenregistrement seul, et l'inspection git — pas la simple relecture du texte — était nécessaire
pour s'en rendre compte.)

**Mise à jour vérifiée à cette seconde correction : les quatre fichiers de résultats, restés
`??` à la première correction, sont maintenant eux aussi commis**, tous les quatre dans le même
commit `09b18d7e61d1af7a07b2003ccd4103fb78b37f11` (12/09 13:25:16+02:00, « Nuit du 11-12/09 :
temoin corrige, A7 detruite, article revise ») :

| Préenregistrement | Commis dans (seul) | Résultat | Commis dans |
|---|---|---|---|
| `c7-nul-corrige-preenregistrement.md` | `5c4cef4` (11:39:23) | `c7-nul-corrige-resultats.md` | `09b18d7` (13:25:16) |
| `c7-tautologie-preenregistrement.md` | `5c4cef4` (11:39:23) | `c7-tautologie-resultats.md` | `09b18d7` (13:25:16) |
| `c7-temoin-prompt-preenregistrement.md` | `5c4cef4` (11:39:23) | `c7-temoin-prompt-resultats.md` | `09b18d7` (13:25:16) |
| `c7-deux-organisations-preenregistrement.md` | `24cc79d` (12:46:10) | `c7-deux-organisations-resultats.md` (+ `c7-deux-organisations-429-rapprochement.md`, `.csv`, et le plan `c7-temoin-deux-organisations-plan.md`) | `09b18d7` (13:25:16) |

`24cc79d` est vérifié ancêtre de `09b18d7` (`git merge-base --is-ancestor` confirme). Pour les
quatre paires, l'ordre git est donc désormais **complet et correct** (préenregistrement commis
avant résultat, dans deux commits distincts), ce qui n'était vrai avant cette correction que pour
le texte des préenregistrements, pas pour leurs résultats. Cela ne change pas la nature de la
limite déclarée : les deux commits de préenregistrement (`5c4cef4`, `24cc79d`) disent eux-mêmes
que le calcul existait déjà sur le disque au moment où le texte a été commis, donc git établit ici
une **antériorité de mise en git, pas une antériorité de rédaction avant calcul**. C'est une
amélioration réelle (plus aucune des quatre paires n'a de fichier non versionné), mais ce n'est
toujours pas l'équivalent des 24 paires propres du §2.1, ni du cas §2.4 ci-dessous.

### 2.4 Un cinquième préenregistrement C7 : `c7-factoriel`, la seule antériorité prouvée par l'historique et non simplement déclarée

Une expérience factorielle un-facteur-à-la-fois a été préenregistrée et exécutée depuis la
première correction de ce recueil : `resultats/c7-factoriel-preenregistrement.md` /
`resultats/c7-factoriel-resultats.md`. Elle se distingue de toutes les paires précédentes,
propres ou faibles :

- **Préenregistrement commis seul** dans le commit `ff90409501d998ab77a36b7f0fc7a117d0d39833`
  (« C7 factoriel : préenregistrement, avant tout appel payant », 12/09 12:52:49+02:00). À ce
  commit, `analyses/c7_factoriel.py` — le script qui effectue les appels payants — **n'existe pas
  dans le dépôt** (`git show ff90409:analyses/c7_factoriel.py` échoue). `git log --follow
  --diff-filter=A -- analyses/c7_factoriel.py` confirme que sa première apparition dans tout
  l'historique du dépôt est le commit de résultats lui-même, quatre heures plus tard : le script
  n'a en tout cas jamais été **commis** avant le préenregistrement (git ne peut, ici comme
  ailleurs, rien affirmer sur une version non commise qui aurait existé sur le disque).
- **Résultat et script commis ensemble, plus tard**, dans le commit
  `ee73f708456033d4f919206fa20ac47b348cb093` (« C7 factoriel : aucun facteur isole ne porte le
  canal inter-jumeaux », 12/09 16:46:27+02:00) — commit qui est aussi le `HEAD` courant de ce
  dépôt. Deux commits séparent les deux (`git log ff90409..ee73f70` : `09b18d7`, puis `975e87f`,
  puis `ee73f70` lui-même), soit environ 4 heures d'écart, sans qu'aucun de ces commits
  intermédiaires ne touche `analyses/c7_factoriel.py` ou les fichiers `c7-factoriel-*`.
- Le préenregistrement affirme lui-même, en dernière ligne : « Aucun appel n'a encore eu lieu au
  moment où ce fichier est écrit et commité. » Le fichier de résultats confirme un coût total
  mesuré de 0,5385601250 USD sur 360 appels, cohérent avec la projection de ≈0,60 USD écrite
  **avant** le calcul dans le préenregistrement — la tenue de compte projetée correspond à la
  tenue de compte réelle, ce qui n'aurait pas de sens à démontrer si le texte avait été écrit après
  coup pour coller aux résultats.

**C'est donc le seul cas du dossier où l'antériorité est prouvée par l'historique lui-même**
(absence vérifiable du script producteur de résultats au moment du commit de préenregistrement),
**et non simplement déclarée** par le texte du message de commit comme pour les quatre paires du
§2.3, ni laissée indéterminée comme pour les trois paires du §2.2. Cela corrige directement la
faiblesse que ce recueil avait lui-même identifiée dans ses deux versions précédentes. **Ce point
reste vrai et reste le meilleur élément antériorité du dossier, indépendamment de ce qui suit** :
la discipline de préenregistrement — écrire le texte, le seuil chiffré et la règle de décision,
puis les commiter seuls, avant tout appel payant et avant même que le script producteur de
résultats existe dans le dépôt — a été intégralement respectée ici. Ce qui a fait défaut n'est pas
la discipline de préenregistrement, mais un contrôle de validité du pipeline en amont (voir
paragraphe suivant) ; ce contrôle existe désormais et est écrit et testé
(`analyses/c7_controle_interpretabilite.py`, commit `28405b2`).

**Verdict corrigé (troisième correction de ce recueil, 12/09 soir) : ce test n'a rien réfuté, car
il n'a rien testé.** Un arbitrage postérieur
(`resultats/c7-reconciliation-facteurs-2026-09-12.md`, commit `5f6da6e`, à lire en entier) a établi
que les cinq jumeaux produits par cette expérience (B, M, G, C, P) réidentifient la vraie personne,
contre les 120 humains réels du même bassin, à un taux de **0,0 à 0,8 %** — au niveau du hasard
(0,83 % attendu) et bien en dessous de Demographics Only (13,29 %), là où les jumeaux publiés par
l'équipe Twin, sur ce même bassin, atteignent 20,2 à 38,9 %. Le préenregistrement avait projeté des
top-1 d'environ 20 %, 15 % et 8 % pour les trois conditions à un facteur changé, et mesuré 0,67 %,
0,83 % et 2,65 % — un résultat lu, à tort, comme la réfutation de ces trois prédictions précises.
En réalité, un contraste entre deux jumeaux qui ne portent chacun aucune information individuelle
sur la personne (apport individuel mesuré à peu près nul, §3.3) ne peut pas trancher laquelle des
trois manipulations « porte le signal » : il n'y avait pas de signal à répartir entre les trois
conditions. **La réfutation préenregistrée est donc retirée** : un bras qui ne pouvait rien tester
ne réfute rien. Ce n'est pas une ligne de tableau à ajouter au compte du manuscrit (§4) — ni comme
réfutation, ni comme non-conclusion — puisqu'aucune des trois prédictions comparatives n'a été mise
à l'épreuve d'un pipeline capable de porter une personne. Détail complet en §3.3.

### 2.5 Conclusion sur l'antériorité

Sur 28 paires Tier 1 originales vérifiables en principe par git, plus la nouvelle paire
`c7-factoriel` (29 au total) : **24 sont propres** (ordre prouvé par simple antériorité de
commit, §2.1), **3 sont indéterminées** (même commit, §2.2), **4 ont un préenregistrement commis
seul puis un résultat commis séparément plus tard — antériorité de mise en git complète, mais
déclarée faible par les commits eux-mêmes car le calcul existait déjà sur le disque au moment du
commit de préenregistrement** (§2.3, les quatre paires y sont désormais toutes entièrement
commises), et **1 a une antériorité prouvée par l'historique, pas seulement déclarée**
(`c7-factoriel`, §2.4). Aucune inversion (résultat avant préenregistrement) n'a été trouvée nulle
part, dans aucune des 29 paires. L'argument d'antériorité tient donc pleinement pour les 24 cas
propres et pour le cas prouvé de §2.4 (25 paires sur 29) ; pour les 4 paires de §2.3, il repose sur
une déclaration du commit lui-même, pas sur une preuve indépendante ; pour les 3 paires de §2.2, il
ne tient pas du tout et doit être reconnu comme une limite.

---

## 3. Détail par préenregistrement (Tier 1)

Pour chaque fichier : première apparition git, SHA-256 du contenu actuel, question, prédictions
chiffrées, verdict.

### 3.1 Fondations

**`c7-preenregistrement.md`** — 1ʳᵉ apparition git : 2026-09-11 20:11:12+02:00. SHA-256 :
`6e1e58687a5118f4852b93cbcbbcfc6f16c2a6160db26199adb53296ab4dee31`.
Question : le jumeau retrouve-t-il la bonne personne (top-1) dans la foule, pas seulement une
réponse plausible ? Prédiction : top-1 ≥ 10 % ET ≥ 2× Demographics Only pour au moins un jumeau
riche. **Verdict : confirmée.** JSON Persona GPT-4.1 atteint 20,7 % (9,7× Demographics Only, 425×
le hasard).

**`a1-controle-preenregistrement.md`** — 2026-09-11 22:49:56+02:00. SHA-256 :
`5201d256bf38e0a969c57c4beec5eb0a72694af8fe31eba68b9007c3c105a2ff`.
Question : l'AUC 0,65 de désaccord vient-elle d'une vraie connaissance de la personne, ou de
bruit d'item/personne ? Prédictions : (i) gain < +0,01 pour les riches ; (ii) Demographics Only
≈ 0 ; (iii) seuil de « signal réel » à gain ≥ +0,02 (IC bas > 0). **Verdict : mixte.** (i)
réfutée (+0,014 à +0,020) ; (ii) à peu près confirmée (+0,009) ; (iii) atteinte par aucune
configuration (max +0,0199, juste sous la barre).

### 3.2 Baselines et robustesse méthodologique

**`c5-preenregistrement.md`** — 2026-09-11 20:12:09+02:00. SHA-256 :
`c11cd8101f7d3a4393ba91d22c1d60bfbd6329b13894d3092fe363d7a3274b8b`.
Question : onze paires de formulation du GSS reproduisent-elles l'effet humain publié (welfare,
big cities), avant tout appel de modèle ? Règle de décision à trois issues : « on fonce » / «
zone grise » / « abandon », selon MAE et faux positifs. **Verdict (au moins deux modèles
documentés dans le résultat lu)** : deepseek → **zone grise** (aucun des trois critères
rempli exactement) ; Qwen3-30B → **abandon** (MAE 4,3-7,0, au plus une fausse alerte).

**`b123-preenregistrement.md`** — 2026-09-11 20:14:43+02:00. SHA-256 :
`b8e78464c96af0e00b1404b744cba52d1657d11208b02331ab1500957172d689`.
Question : une baseline gratuite (marge d'une autre cohorte/vague) égale-t-elle les métriques
vitrines citées par des vendeurs ? **Verdict : confirmée** — sur 1-MAE, 1-TV et Spearman, la
baseline gratuite égale ou dépasse chaque chiffre-vitrine cité, avec une réserve méthodologique
notable : 1-MAE (la métrique la plus citée par les vendeurs) est aussi la moins discriminante
des quatre pour distinguer une bonne baseline d'une simulation délibérément inversée.

### 3.3 Le cœur de C7 : couplage fidélité/fuite (A1) et sa remise en cause

**`c7-compromis-preenregistrement.md`** — 2026-09-12 00:37:44+02:00. SHA-256 :
`2d654195cfc04ebacf45fca9e438563c35af430ef17e7b98e203dae87b33907b`.
Prédiction : rho(fidélité, fuite) ≥ 0,70 sur 12 configurations. **Verdict : tient globalement**
(rho 0,96), mais **pas au sens strict** « à exactitude égale tout jumeau fuit plus que tout
prédicteur ».

**`c7-compromis-bits-preenregistrement.md`** (2026-09-12 00:45:58+02:00, SHA-256
`3b53c72f0c8ee35b03f05dd84d8688f37c17d004b6183971d9ece64377e8e434`) et
**`c7-compromis-robustesse-preenregistrement.md`** (2026-09-12 01:12:03+02:00, SHA-256
`5b062fb6fc9cb2c646ba5fe36ea7be71819b01f6c6bf76d2f7044d0ebbeffbb7`) : contrôles de robustesse du
même test ; leurs résultats sont publiés **dans** `c7-compromis-resultats.md` (§4, figure) plutôt
que dans des fichiers `-resultats` séparés. Robustesse confirmée contre trois références.

**`c7-disjoint-preenregistrement.md`** — 2026-09-12 01:44:59+02:00. SHA-256 :
`865d3d315bbfbedb777e6e44078e3db2067247888145ad50c44a71805a24d9d7`.
Prédictions : (a) rho survit sur items disjoints, > 0,70 ; (b) rho observé > 95ᵉ centile d'un
« nul de marge » (100 prédicteurs sans empreinte individuelle). **Verdict initial : (a)
confirmée, (b) réfutée** — le nul de marge atteint rho = 0,984, au-dessus même du rho observé
(0,969). Conclusion initiale : A1 doit être affaiblie (qualité globale, pas empreinte
individuelle spécifique). **Verdict final, après un épisode de tentative de renversement puis
d'audit adverse le 12/09 (détaillé à l'entrée `c7-nul-corrige-preenregistrement.md` juste en
dessous) : (b) reste réfutée.** Le nul de marge d'origine avait un défaut réel (ligne 133 de
`analyses/c7_disjoint.py`), mais le corriger, une fois testé rigoureusement, ne renverse pas le
verdict.

**`c7-nul-corrige-preenregistrement.md`** — commis seul le 12/09 dans
`5c4cef48d40db4046cbb51b1bd02d1fea239573e` (voir §2.3) ; son résultat
(`c7-nul-corrige-resultats.md`) est désormais commis aussi, séparément et plus tard, dans
`09b18d7` (12/09 13:25:16+02:00 — voir §2.3). SHA-256 du préenregistrement :
`9e5e44822d940fb51019be83c59e1843f2d92e53f253c2a4a8e18fe75bf9d1b6`.
Question : le « nul de marge » de `c7-disjoint` était-il défectueux (il recopiait en partie la
cible au lieu de ne porter que la marge d'exactitude) ?

**>>> Épisode complet, à signaler tel quel — un défaut réel mais non déterminant, une tentative
de renversement, un audit adverse, une concession <<<** Ce résultat renforce, plutôt qu'il
n'affaiblit, la crédibilité du recueil : une révision qui aurait arrangé l'article a été rejetée
après vérification.

1. Le défaut signalé était **réel**, mais pas exactement celui décrit dans
   `c7-nul-corrige-resultats.md`. Le vrai défaut est à la **ligne 133** de
   `analyses/c7_disjoint.py` (`faux = faux + (faux >= y_ref)`, qui évite aux cellules fausses la
   vraie réponse de la personne), pas à la ligne 134 accusée initialement (qui, elle, fait
   exactement ce qu'une empreinte individuelle par personne doit faire — écrire la vraie réponse
   sur les positions tirées comme exactes n'est pas un défaut, c'est la définition arithmétique
   d'une exactitude par personne fixée).
2. `c7-nul-corrige-resultats.md` a construit cinq témoins « corrigés » et publié, sur cette base,
   un verdict inverse : prédiction (b) **confirmée**, réfutation retirée (« issue B »). **C'est ce
   verdict-là qui ne tenait pas** : les cinq témoins corrigés apparient l'exactitude par personne
   contre une **cible de substitution** (mode de segment, vecteur d'autrui, identités permutées),
   si bien que l'exactitude qu'ils reproduisent **contre la vérité** s'effondre (0,407–0,436 contre
   0,527 pour le prédicteur réel) — précisément la grandeur que l'objection (b) met en cause. Un
   nul qui supprime la variable explicative candidate ne peut pas réfuter l'explication par cette
   variable, et la comparaison ne portait donc sur rien.
3. Ce renversement a été soumis à un **audit adverse**
   (`resultats/audit-renversement-2026-09-12.md`), qui a reconstruit le témoin manquant —
   exactitude exacte contre la vérité, positions tirées au hasard, cellules fausses tirées dans la
   marginale de population de l'item (ce qui purge spécifiquement le défaut de ligne 133) — et
   mesuré **rho 0,974 (5ᵉ–95ᵉ centiles [0,950 ; 0,993])**, contre 0,965 pour le prédicteur réel :
   le rho observé **ne dépasse pas** ce témoin correctement construit. La prédiction (b) **reste
   donc réfutée**.
4. L'auteur du renversement a répondu à cet audit
   (`resultats/c7-nul-corrige-reponse-audit.md`) et **concédé sans réserve** : « Mon renversement
   tombe. [...] La réfutation publiée **tient** [...] "Issue B / thèse soutenue" est **retiré**. »
   L'auteur a reconstruit lui-même le témoin de l'audit et retrouvé des chiffres compatibles
   (rho 0,9776 sur 10 réplicats, contre 0,9741 annoncé par l'audit).
5. Le défaut de ligne 133, une fois isolé et corrigé seul (sans changer par ailleurs la nature du
   témoin), gonflait la fuite mesurée d'un facteur **~1,3** (top-1 41,2 % contre 31,6 % une fois
   les valeurs fausses tirées dans la marginale de population) — un vrai défaut, à un vrai
   endroit, mais **qui ne fait pas basculer le verdict**.

**Verdict final : (b) reste réfutée**, comme dans `c7-disjoint-resultats.md` d'origine. Le nul de
marge d'origine avait un défaut réel (ligne 133), depuis corrigé, sans conséquence sur l'issue.
Ce préenregistrement est commis seul (§2.3), avec la limite déclarée par le commit lui-même
(antériorité faible, pas une preuve) ; son fichier de résultats est désormais commis aussi, dans
`09b18d7` (13:25:16+02:00), séparément et après le préenregistrement.

**`c7-tautologie-preenregistrement.md`** — commis seul le 12/09 dans `5c4cef4` (voir §2.3) ; son
résultat (`c7-tautologie-resultats.md`) est désormais commis aussi, dans `09b18d7`
(13:25:16+02:00). SHA-256 du préenregistrement :
`1ab405560529134736f130d962b896bb4c55524c5e7236811bae883b51d159ac`.
Question (l'objection la plus dangereuse contre l'article) : à exactitude par personne tenue
identique au bit près, la fuite varie-t-elle encore selon la structure des erreurs ? **Verdict :
mixte, tel que prévu par la règle** — écart réel mais faible (facteur 1,16), ni tautologie totale
ni structure dominante. Résultat non anticipé : les quatre témoins construits fuient TOUS plus
(27,7-32,1 %) que le jumeau réel (20,7 %) à exactitude identique.

**`c7-temoin-prompt-preenregistrement.md`** — commis seul le 12/09 dans `5c4cef4` (voir §2.3) ;
son résultat (`c7-temoin-prompt-resultats.md`) est désormais commis aussi, dans `09b18d7`
(13:25:16+02:00). SHA-256 du préenregistrement :
`24f8a150849db4e24f5e32e24eb213720796d19821c6ee9a66720ddec76b3279`.
Objection testée : le canal inter-jumeaux (A2/transfert) ne mesurerait-il que la stabilité du
gabarit de prompt, pas la personne ? **Verdict : confirmée (A2 survit)** — top-1 mode-segment
(0,07 %) très en dessous du seuil destructeur (12,13 %) ; apport individuel (17,38 pts) très
au-dessus de l'apport de segment (3,83 pts).

**`c7-deux-organisations-preenregistrement.md`** — commis seul dans `24cc79d` (12/09
12:46:10+02:00, voir §2.3). Au moment de la première rédaction de ce recueil, un autre agent
écrivait encore ce dossier et rien n'était commis ; à la première correction le préenregistrement
seul était déjà commis (ce recueil l'avait manqué) ; à cette seconde correction, **son résultat est
désormais commis aussi**, dans `09b18d7` (13:25:16+02:00), avec la même limite d'antériorité
faible que les trois paires précédentes. SHA-256 du préenregistrement :
`07e74fd088073f41195170eeb8c288a4848da73f50750aadd4d237a6edf47a79`.
Question : le canal inter-jumeaux traverse-t-il deux organisations qui ne partagent ni modèle ni
gabarit de prompt ? Résultat final (`c7-deux-organisations-resultats.md`, n = 142 sur 200
personnes prévues — un second arrêt, non rapproché cette fois, a suivi le premier arrêt à n = 82
rapproché et déclaré non facturé dans `c7-deux-organisations-429-rapprochement.md`) : top-1(B↔C) =
**1,76 % [0,35 ; 3,63]**, **inférieur** à la baseline Demographics Only (9,20 % [5,47 ; 13,40]),
IC ne recouvrant pas le leurre de segment (25,5 % [19,9 ; 31,3]). L'écart s'est creusé, pas
resserré, entre n = 82 (3,66 %) et n = 142 (1,76 %).

**Verdict corrigé (troisième correction de ce recueil, 12/09 soir) : ni soutenue ni réfutée — non
testée.** Le verdict publié d'abord dans `resultats/article-synthese.md` (« A7, menace « deux
organisations indépendantes », réfutée / détruite ») a été retiré par l'arbitrage
(`resultats/c7-reconciliation-facteurs-2026-09-12.md`, commit `5f6da6e`, à lire en entier) : les
jumeaux B et C, testés séparément contre les 120 humains réels du même bassin, ne réidentifient la
vraie personne qu'à **0,79 % et 0,29 %** — au niveau du hasard (0,83 %), très en dessous de
Demographics Only (13,29 %) et sans commune mesure avec les jumeaux publiés par l'équipe Twin sur
ce même bassin (20,2–38,9 %). Le contraste B↔C (1,76 %) n'oppose donc pas deux jumeaux porteurs
d'une personne dont on mesurerait le transfert entre deux organisations : il oppose deux
générateurs qui ne portent, chacun séparément, quasiment aucune information individuelle. Un
contraste entre deux bruits vaut le hasard quel que soit son résultat chiffré — ce n'est ni une
confirmation ni une réfutation de la menace testée, c'est une limite de cet instrument précis. Dans
le manuscrit (`article/manuscrit.md`, ligne 315, table §7.1 ligne 17), cette entrée est désormais
comptée **« non testable avec cet instrument »**, ni parmi les réfutations ni parmi les
non-conclusions (§4). Cette expérience sert malgré tout de point de départ chiffré au cinquième
préenregistrement, `c7-factoriel` (ci-dessous), qui cherche lequel des trois facteurs changés
simultanément (modèle, gabarit, persona) porte l'effondrement mesuré ici — effondrement dont on
sait maintenant qu'il préexistait, au niveau du hasard, dans le pipeline B lui-même.

**`c7-factoriel-preenregistrement.md`** — commis seul, **avant tout appel payant et avant même
l'existence du script d'analyse**, dans `ff90409` (12/09 12:52:49+02:00) ; son résultat
(`c7-factoriel-resultats.md`, avec le script `analyses/c7_factoriel.py` et
`resultats/c7-factoriel.csv`) est commis plus tard, seul lui aussi, dans `ee73f70` (12/09
16:46:27+02:00 — commit `HEAD` courant). Voir §2.4 pour le détail de la vérification
d'antériorité — c'est le seul cas du dossier où elle est prouvée, pas seulement déclarée.
Question : parmi les trois facteurs changés simultanément dans `c7-deux-organisations` (modèle,
gabarit de prompt, format de persona), lequel porte l'effondrement du canal inter-jumeaux mesuré
là-bas (1,76 %, contre 36,4 % en intra-équipe) ? Trois attaques symétriques B↔X à un seul facteur
changé par rapport au pipeline B (deepseek-v4-flash, persona JSON, gabarit système/utilisateur),
n = 120 personnes, 360 appels, 0 échec, 0 HTTP 429, coût réel 0,5386 USD (projection
préenregistrée : ≈0,60 USD). Prédictions préenregistrées : modèle seul ≈ 20 % [8 ; 35], gabarit
seul ≈ 15 % [5 ; 30], persona seule ≈ 8 % [2 ; 20] — la persona pressentie comme le facteur le
plus dégradant. Mesuré : modèle seul **0,67 % [0,00 ; 1,75]**, gabarit seul **0,83 % [0,00 ;
2,08]**, persona seule **2,65 % [0,50 ; 5,13]**, tous sous la baseline Demographics Only recalculée
sur ce pool de 120 (13,29 % [7,46 ; 19,29]) et dans la même fourchette que la configuration « tout
différent » (1,76 % [0,35 ; 3,63]). Règle de décision préenregistrée (bas_X > 3,63 % ET
top1_X ≥ 2×13,29 % = 26,58 % pour qu'un facteur « porte le signal seul ») : remplie par **aucun**
des trois. **Verdict publié d'abord : prédiction réfutée** — les trois valeurs sont bien plus
basses que prévu (aucune n'atteint le bas de son propre intervalle prédit) et **dans l'ordre
inverse** de celui prédit (c'est la persona, censée être le facteur le plus dégradant, qui préserve
le *plus* de signal ; c'est le modèle, censé protéger l'essentiel du canal, qui en préserve le
*moins*).

**Verdict corrigé (troisième correction de ce recueil, 12/09 soir) : réfutation retirée — ce test
n'a rien testé.** L'arbitrage (`resultats/c7-reconciliation-facteurs-2026-09-12.md`, §3, commis
dans `5f6da6e`) montre que les cinq jumeaux produits par cette expérience (B, M, G, C, P), testés
contre les 120 humains réels du même bassin, réidentifient la vraie personne à **0,0 à 0,8 %**,
au niveau du hasard (0,83 %) et loin en dessous de Demographics Only (13,29 %) — contre 20,2 à
38,9 % pour les jumeaux publiés par l'équipe Twin sur ce même bassin. La décomposition de l'accord
confirme un apport individuel proche de zéro (par exemple B↔M : −0,0 point). Les trois contrastes
préenregistrés (modèle seul, gabarit seul, persona seule) comparent donc chacun deux sources de
bruit, pas deux jumeaux porteurs d'une personne : un contraste entre deux bruits produit
nécessairement une valeur proche du hasard, quelle que soit la variable manipulée, et cela ne dit
rien sur laquelle des trois manipulations « porte le signal », puisqu'il n'y avait pas de signal à
répartir. **La réfutation préenregistrée est retirée** : un bras qui ne pouvait rien tester ne
réfute rien. Ce qui reste acquis et vaut d'être souligné : la discipline de préenregistrement elle-
même (texte, seuils, règle de décision commis seuls, avant tout appel payant, §2.4) a été
intégralement respectée ; elle n'a simplement pas suffi, faute d'un contrôle de validité du
pipeline en amont — contrôle qui n'existait pas au moment de l'expérience et qui existe désormais,
écrit et testé, dans `analyses/c7_controle_interpretabilite.py` (commit `28405b2`). Conclusion
correcte à retenir : **aucun des trois facteurs pris isolément, ni les trois ensemble, n'a jamais
été mis à l'épreuve d'un pipeline capable de porter une personne** — la question posée par ce
préenregistrement reste ouverte, elle n'a pas reçu de réponse dans un sens ou dans l'autre.

### 3.4 Générateurs, synthétiseur ajusté, spécificité LLM (A2)

**`c7-generateur-preenregistrement.md`** — 2026-09-12 01:01:51+02:00. SHA-256 :
`105947cfca6f620817ad180c54edcb4b558888ea5771ac7cc870807ae559de97`.
Prédiction : générateurs individualisés (G-LR, G-copule) ≥ 10 % ou ≥ moitié du jumeau, sinon très
en dessous. **Verdict : confirmée (spécificité LLM)** — top-1 des deux générateurs (0,22-0,25 %),
~85× sous le jumeau (20,7 %).

**`c7-synth-ajuste-preenregistrement.md`** — 2026-09-12 01:43:20+02:00. SHA-256 :
`ce7ea52ae6aca4b87f38130264e0736b6d5b2b9a769933c80516179cbef7336c`.
Prédiction : synthétiseur avantagé (voit le bloc cible), top-1 << 20,7 %. **Verdict : confirmée
sur le top-1** (0,00 % contre 20,7 %), avec réserve sur le top-10 (le comparateur y fuit
davantage que le jumeau).

### 3.5 Mécanisme (A5)

**`c7-mecanisme-preenregistrement.md`** — 2026-09-11 22:29:58+02:00. SHA-256 :
`b3b676e7ea3c47abaa3cc154d2ec6e1599f178fd788819bba8ecb1ea45e477fa`.
Quatre hypothèses (H1 entropie, H2 cohérence, H3 structure de matrice, H4 stéréotypie).
**Verdict : mixte** — H1 **rejetée** (l'opinion a moins d'entropie humaine, pas plus) ; H2
**soutenue partiellement** (corrélation personne à personne 0,448) ; H3 **fortement soutenue**
(permuter l'ordre des réponses fait chuter le top-1 de 33,1 % à 0,046 %) ; H4 **rejetée** (le
jumeau ne stéréotype pas plus que les humains eux-mêmes).

### 3.6 Ailleurs que sur Twin : Stanford/GSS, transfert, monde ouvert (A6, A7, A3)

**`c7-stanford-preenregistrement.md`** — 2026-09-12 00:34:22+02:00. SHA-256 :
`7fa2967b3a8e7a77da26971b098cee23e967c76529f7be45cdd73cae34ce5d8c`.
Prédiction : top-1 ≥ 10 % et ≥ 5× démographique. **Verdict : confirmée, marge plus large que
prévu** (composite 65,7 %, 29× le démographique, 691× le hasard).

**`c7-stanford-provenance-preenregistrement.md`** — 2026-09-12 00:55:10+02:00. SHA-256 :
`06f525ad15af8cb768892ea06e75cdf0082a0abb965331b06c614468fb5a229c`.
Question : le 65,7 % Stanford est-il contaminé par recopie vague1→vague2 ? **Verdict :
contamination exclue** ; chiffre le plus défendable identifié (entretien seul, 44,7 %).

**`c7-transfert-preenregistrement.md`** — 2026-09-12 00:55:09+02:00. SHA-256 :
`4a33357f5cc6c845258bdbab1d5a6d9fb0e3774033879a95de353ffe2ebeb601`.
Prédiction : volet A ≥ 15 % sur paires riches. **Verdict : mixte** — confirmée pour 30 paires à
60 items (36,4 %), **réfutée** pour 12 paires à 19 items (0,45 %) ; volet B sans objet (déclaré
infaisable avant calcul).

**`c7-transfert-stanford-preenregistrement.md`** — 2026-09-12 02:28:30+02:00. SHA-256 :
`b98dd8eba5dd93ebea0f151b160371a4a87ef99fb10c1098bd0208375d348500`.
Prédiction : top-1 GSS ≥ 20 %. **Verdict : réfutée sur le seuil principal** (11,9-13,0 %), mais
nettement au-dessus du démographique (confirmé, facteur 5-8×) ; critère d'échec préenregistré
(« ne dépasse pas nettement le démographique ») non atteint : le canal se réplique, plus
faiblement que sur Twin.

**`c7-monde-ouvert-preenregistrement.md`** — 2026-09-12 00:56:07+02:00. SHA-256 :
`5446aea4eb0e4a40cade9841ce231ed9946716b86337e47530e2959a2d877a42`.
Prédiction : TPR à FPR=1 % > 5 % (Twin) et > 30 % (Stanford). **Verdict : non confirmée, sens
pessimiste** — mesuré 3,04 % et 20,39 %, sous la barre dans les deux cas ; comparateurs restant
sous 1 % confirmés séparément. Un addendum non commis (`c7-monde-ouvert-ic-2026-09-12.md`) ajoute
des IC à ce résultat.

### 3.7 Défense D4, attaquant fort, DP, utilité aval (A3, A8, A11, A12, A13)

**`c7-defense-preenregistrement.md`** — 2026-09-12 00:33:08+02:00. SHA-256 :
`25dd2deade5d6921c048a1e6d0600b7d92ed254707541e3541bba19b0fd72f89`.
**Verdict : confirmée** — D4 ramène le top-1 sous 1 %, avec un coût réel (corrigé après relecture
hostile : 4,4 points sur les corrélations, pas 1,47).

**`c7-attaquant-fort-preenregistrement.md`** — même commit que son résultat (§2.2, non
vérifiable seul). 2026-09-12 07:12:56+02:00. SHA-256 :
`1b3f19bf7d0484cdd8601b264cf4691ae12e471db5c2a25950ebb5bfcc80af1a`.
Trois prédictions [P1] gain ≥ 20 % (Twin, Park), [P2] D4 < 1 % sous A-LLR, [P3] D4 < 1 % sous
attaquant adaptatif. **Verdict : mixte** — [P1] réfutée sur Twin (+12,2 %, sous les 20 %, mais
lu comme un renforcement du chiffre publié) / tenue sur Park (+38,0 %) ; [P2] tenue (0,24 %) ;
[P3] réfutée dans le sens favorable à la défense (0,29 %, jamais > 1 %).

**`c7-dp-preenregistrement.md`** — même commit que son résultat (§2.2). 2026-09-12
07:12:13+02:00. SHA-256 : `7213ab3f8afb0e23e29400bd44a630e2afa0be226ab981976ccd790959a69e61`.
Prédiction : DP domine D4. **Verdict : réfutée** — à eps=3 et 10, perte d'utilité (3,3-3,4 pts)
et top-1 (0,158 %, 0 %) ne sont pas meilleurs que D4 (0,126 %) ; même le témoin non privé
plafonne à 3,52 pts (plancher architectural, pas budgétaire).

**`c7-utilite-aval-preenregistrement.md`** — même commit que son résultat (§2.2). 2026-09-12
07:09:58+02:00. SHA-256 : `f364a199f3c84f90a145ee3493b2f94155e8169dbd9bc85cfd678cde751a72db`.
Quatre prédictions. **Verdict : majoritairement confirmée** — P1 et P3 confirmées ; P2 partielle
(perte de significativité, aucun changement de signe) ; P4 confirmée sur la variance, contredite
sur les loadings d'ACP.

### 3.8 Fidélité vs fuite avec un modèle fort, recette, bits, échelle (A9, A4, A8/A10)

**`c7-courbe-gen-preenregistrement.md`** — 2026-09-12 06:47:37+02:00. SHA-256 :
`99e551a719b6eb08a0cbe91c6fba8ea2546b399285948237c143b62480d4fea0`.
Prédiction : ≥ 5/7 jumeaux régénérés dans l'intervalle de prédiction. **Verdict : confirmée
largement** (7/7).

**`c7-fort-preenregistrement.md`** — 2026-09-12 06:51:29+02:00. SHA-256 :
`5b88271d27632087fd69661cc1730d298e948a07dfcb58474802bfe1b835f37d`.
Trois prédictions pour un modèle fort (GPT-4.1) : exactitude > 0,55, fidélité > 0,10, top-1 > 5 %.
**Verdict publié initialement : 1. réfutée (0,4722) ; 2. confirmée de justesse (0,1714, seuil
identifié comme fragile) ; 3. réfutée (0,00 %).**
**>>> Correction du 12/09, à signaler en évidence <<<** (`c7-a9-correction-2026-09-12.md`) :
l'IC publié « [0 % ; 0 %] » sur 0/30 est un **artefact de bootstrap percentile** (un
rééchantillonnage de 30 zéros ne peut produire que des zéros). L'IC exact (Clopper-Pearson) est
[0 % ; 11,57 %], qui **contient** le seuil préenregistré de 5 %. La prédiction 3 (top-1 > 5 %)
n'est donc **pas réfutée** : elle est **non concluante, faute de puissance** à n = 30.

**`c7-recette-preenregistrement.md`** — 2026-09-12 01:05:31+02:00. SHA-256 :
`8b24d5fd02d1d6a213042907cdac1952c291447a39ba58d884f2b659d6314856`.
Prédiction : top-1 par item ≥ 5× top-1 appel unique. **Verdict publié initialement : réfutée**
(les deux à 0,00 %, top-10 va dans le sens inverse).
**>>> Correction du 12/09, à signaler en évidence <<<** : n = 10 sur le bras « appel par item » ;
IC exact Clopper-Pearson [0 % ; 30,85 %] — le facteur ≥5 n'est **ni confirmé ni exclu**. Verdict
corrigé : **non concluante**, pas réfutée.

**`c7-gen-preenregistrement.md`** — 2026-09-12 00:51:31+02:00. SHA-256 :
`4e5a4e722e46716e432668bfd6f2d667f4849f457c957742ec41e82d72466208`.
Trois prédictions (R1, R2, R3). **Verdict : mixte** — R1 rejetée (aucun modèle n'atteint 1 %,
prédit ≥10 %) ; R2 confirmée (< 3 % partout) ; R3 confirmée mais non informative (effet de
plancher non exclu).

**`c7-bits-preenregistrement.md`** (2026-09-12 00:45:58+02:00, SHA-256
`7c84373a85b19e46d0ea09f0f741a75584459c9fdf8676ee07ca4e83a7829777`) et son avenant
**`c7-bits-preenregistrement-avenant.md`** (2026-09-12 00:54:32+02:00, SHA-256
`1ea4ae4883813eb5d87a4b96086eeffc7160bc2e351e96abc84f413030f13ad6`).
Quatre prédictions (P1-P4, bits d'identité de Miller-Madow). **Verdict : toutes confirmées** par
la règle déclarée, avec une nuance honnête signalée par les auteurs eux-mêmes : le retest humain a
un ratio bits/exactitude aussi bon ou meilleur que les jumeaux LLM face à certains comparateurs.

**`c7-echelle-preenregistrement.md`** — 2026-09-12 00:40:01+02:00. SHA-256 :
`6eb4a09405004e961aa2eb2c9cb8c94f6e0ab417d31d69d58aefdafb79b1c5d9`.
Question : le top-1 tient-il à grande échelle (N) ? **Descriptif, pas de seuil chiffré unique
préenregistré** : le ratio riche/démographie croît avec N (2,8 à 9,7 sur la plage mesurée) ;
extrapolation au-delà de N ≈ 4 000 explicitement refusée (deux lois d'échelle divergent déjà à
2× la plage mesurée).

**`c7-deviations-preenregistrement.md`** — 2026-09-12 00:49:14+02:00. SHA-256 :
`a056db00bb18dab6fab64443bd5dd5e55359f1c4a0ee79a837e049b94c382989`.
« Écarts faux seuls » : exactement 0,0 % pour tous, y compris les jumeaux, cohérent avec le
verdict déjà établi ailleurs.

### 3.9 Tournoi Twin A→B (chantier voisin, explicitement demandé)

**`tab-preenregistrement.md`** — 2026-09-11 16:14:56+02:00. SHA-256 :
`1de06cab7aaec984dbbc15f2adefc400f0f18655a0850aaa7b7559e977ef8ef6`.
Ce fichier revendique lui-même son propre mécanisme d'antériorité (« le commit public daté qui
dépose cette page remplace le dépôt OSF »), avec le hash du commit alors HEAD cité dans son texte
(`e29a53683fcf36791c3ef319112c537b4c36df3f`). Question : le choix du candidat B par diagnostic
(résidu chute~exactitude) fait-il mieux que par exactitude brute ? Quatre règles R1-R4.
**Résultat** (`tab-resultats.md`, 1ʳᵉ apparition 2026-09-11 17:27:57+02:00, soit après le
préenregistrement — ordre correct) : **Verdict : réfutée, revendication fermée.** Delta =
+0,0266, IC [+0,0026 ; +0,0412], entièrement positif (sens opposé à celui prédit). R1-R4 tous faux.

**`tab2-preenregistrement.md`** — 2026-09-11 18:18:11+02:00. SHA-256 :
`1876d2319dc3cfb9b0af26638c27a952883f7e16b5559cfbdedcc544be0b4df2`.
Deuxième version, candidats hétérogènes, cible primaire ρ_B. **Sans résultat à ce jour** : aucun
fichier `tab2-resultats*` n'existe dans le dépôt.

---

## 4. Le compte des verdicts contesté (A9 et multiplicité)

Trois rapports ont été lus intégralement (les deux premiers dès la première rédaction, le
troisième trouvé committé à cette seconde correction) :

- `resultats/c7-a9-correction-2026-09-12.md`
- `resultats/c7-multiplicite-globale-2026-09-12.md`
- `resultats/audit-chiffres-2026-09-12.md` (committé dans `09b18d7`, 12/09 13:25:16+02:00 — postérieur
  aux deux précédents, il en tire les conséquences et **recompte le tableau du manuscrit ligne à
  ligne**, ce qu'aucun des deux premiers ne faisait explicitement)

Les deux premiers rapports identifient **exactement les deux mêmes cas** à requalifier de
« réfutée » à « non concluante », tous deux causés par le même artefact (un IC bootstrap
percentile sur zéro succès ne peut rendre que « [0 ; 0] », alors que l'IC exact Clopper-Pearson
contient le seuil préenregistré) :

1. **A9, top-1 du modèle fort > 5 %** (`c7-fort-resultats.md`) : IC exact Clopper-Pearson
   [0 % ; 11,57 %] à n = 30, qui contient le seuil de 5 %.
2. **A9, recette/granularité de l'appel ≥ 5×** (`c7-recette-resultats.md`) : même défaut, n = 10,
   IC exact [0 % ; 30,85 %].

**Ce que `c7-a9-correction-2026-09-12.md` et `c7-multiplicite-globale-2026-09-12.md`, à eux
seuls, ne disaient pas** (ce recueil le signalait comme une limite à sa première rédaction) :
qu'un troisième mouvement, indépendant des deux requalifications, s'est produit la même nuit.
`resultats/audit-chiffres-2026-09-12.md` (§1.2) reconstitue les trois mouvements et **recompte
mécaniquement le tableau du manuscrit** (17 lignes au total) :

| étape | compte de réfutations | cause |
|---|---|---|
| départ | 16 | tableau à 16 lignes, toutes « Refuted » |
| −2 | 14 | les deux cas ci-dessus (A9 modèle fort, A9 recette) requalifiés « non concluant » |
| +1 | **15** | ajout d'une **17ᵉ ligne** : le témoin « deux organisations » (`c7-deux-organisations-resultats.md`, appelé T2 dans le manuscrit), testé et **réfutée** |

À l'étape `09b18d7` (13:25:16+02:00), le compte s'établissait donc à **17 lignes, 15 « Refuted »,
2 « inconclusive »** — c'était la valeur committée et vérifiée à cette date-là, et la seconde
correction de ce recueil l'avait reprise telle quelle.

**Troisième correction de ce recueil (12/09 soir) : un quatrième mouvement, postérieur aux trois
ci-dessus, change le compte une nouvelle fois — de 15 à 14, pas à 16.** L'arbitrage
(`resultats/c7-reconciliation-facteurs-2026-09-12.md`, commis dans `5f6da6e`) et le commit qui en
tire la conséquence sur le manuscrit (`8df4e68`, « T2 requalifiée en non testable : le compteur
tombe à 14 », désormais `HEAD`) établissent que le témoin « deux organisations » — la 17ᵉ ligne
ajoutée à l'étape précédente, notée T2 — ne pouvait pas être tranché « réfutée » : ses deux
jumeaux réidentifient la vraie personne au taux du hasard (0,79 % et 0,29 %, contre 0,83 % attendu),
donc son contraste B↔C oppose deux bruits, pas deux jumeaux porteurs d'une personne. La ligne 17
passe donc de « Refuted » à une troisième catégorie, **« non testable »**, distincte de
« inconclusive » (qui, elle, désigne un test valide mais sous-puissant, pas un test qui n'a rien pu
mesurer). Corrélativement, la réfutation préenregistrée du cinquième préenregistrement,
`c7-factoriel` (§2.4, §3.3), est **retirée** plutôt qu'ajoutée comme 18ᵉ ligne : ses cinq jumeaux
subissent le même défaut (0,0 à 0,8 % de réidentification réelle), donc ses trois contrastes à un
facteur ne tranchent rien non plus — ce test ne devient pas une ligne du tableau, ni comme
réfutation ni comme non-conclusion, puisqu'il n'a jamais mis à l'épreuve un pipeline capable de
porter une personne.

**Mise à jour de la table des mouvements** (complète les trois lignes déjà connues d'une
quatrième) :

| étape | compte de réfutations | cause |
|---|---|---|
| départ | 16 | tableau à 16 lignes, toutes « Refuted » |
| −2 | 14 | les deux cas A9 (modèle fort, recette) requalifiés « non concluant » |
| +1 | 15 | ajout d'une 17ᵉ ligne : le témoin « deux organisations » (T2), d'abord compté « réfutée » |
| −1, catégorie changée | **14** | T2 requalifiée « non testable » (ni réfutée ni non concluante) ; le cinquième préenregistrement `c7-factoriel` n'ajoute **aucune** ligne (réfutation retirée, pas de test valide) |

**Recompte ligne à ligne effectué par moi-même, indépendamment du commit `8df4e68`**, sur la table
actuelle du manuscrit (`article/manuscrit.md`, §7.1, lignes 907–923, 17 lignes) : Refuted aux
lignes 1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15 (**14**) ; « Not confirmed — inconclusive »
à la ligne 9 et « Not refuted — inconclusive » à la ligne 16 (**2**) ; « Not testable with this
instrument — counted as neither » à la ligne 17, T2 (**1**). 14 + 2 + 1 = **17**, le compte exact
de lignes du tableau. **Je ne trouve aucun désaccord avec le chiffre 14/2/1** annoncé par la
consigne de cette correction — au contraire, mon recomptage indépendant le confirme très
exactement, terme à terme, y compris sur l'identité des deux lignes non concluantes et de la ligne
non testable. Le texte du manuscrit (ligne 932) l'énonce lui-même dans les mêmes termes :
« Seventeen rows, fourteen refutations, two inconclusive, one untestable. »

**Ce qui reste vrai et mérite d'être mis en valeur, malgré ce recul du compte** : la discipline de
préenregistrement du bras factoriel n'a jamais été en cause. Son texte a été commis seul
(`ff90409`), avant tout appel payant et avant même que le script producteur de résultats existe
dans le dépôt (§2.4) — c'est le seul cas de tout ce recueil où l'antériorité est **prouvée** par
l'historique, et non simplement déclarée par un message de commit. Ce qui a manqué n'est pas la
rigueur du préenregistrement, mais un contrôle de validité du pipeline en amont (vérifier qu'un
jumeau réidentifie mieux que le hasard avant de lui faire porter un contraste) — contrôle qui
n'existait pas cette nuit-là et qui existe désormais, écrit et testé :
`analyses/c7_controle_interpretabilite.py` (commit `28405b2`).

**Attention à ne pas confondre deux comptages différents**, point que `audit-chiffres-2026-09-12.md`
faisait déjà (son §1.2, « piège à ne pas confondre ») et qui reste valable après cette troisième
correction : le manuscrit cite par ailleurs « 25 confirmed and 15 refuted » en §7.3 (ligne 978),
qui est le recensement de `c7-multiplicite.md` sur 47 tests convertibles en p pour Holm/BH — un
objet différent du tableau principal, dont le compte de réfutations est désormais 14, pas 15. La
coïncidence numérique qui existait à l'étape précédente (15 et 15) a donc disparu avec cette
correction ; ce recueil les distingue explicitement pour éviter que le lecteur du dépôt OSF ne les
mélange.

### Mon propre compte, au niveau des préenregistrements du Tier 1 (§3, 35 fichiers)

| Catégorie | Nombre de fichiers | Détail |
|---|---|---|
| Confirmée (toutes prédictions) | 12 | c7 (base), c7-generateur, c7-synth-ajuste (top-1), c7-stanford, c7-stanford-provenance, c7-defense, c7-courbe-gen, c7-bits, c7-temoin-prompt, b123, c7-utilite-aval (majoritaire), tab-diagnostic (au sens : hypothèse principale nettement invalidée, donc « réfutée » — voir ligne dédiée) |
| Réfutée (toutes prédictions) | 3 | c7-dp, c7-monde-ouvert, tab (tournoi A→B) |
| Mixte (au moins une confirmée et une réfutée/non concluante) | 12 | a1-controle, c7-compromis, c7-disjoint (verdict (a) confirmée / (b) réfutée — réaffirmé le 12/09 après qu'une tentative de renversement du (b) a été rejetée par un audit adverse et concédée par son auteur, voir §3.3), c7-fort, c7-gen, c7-mecanisme, c7-transfert, c7-transfert-stanford, c7-attaquant-fort, c7-tautologie, c5 (deux modèles, deux issues distinctes), c7-recette (avant correction) |
| Requalifiée réfutée→non concluante (correction du 12/09, artefact d'IC bootstrap dégénéré sur zéro succès — sans rapport avec le témoin de marge de c7-disjoint) | 2 | c7-fort (prédiction top-1), c7-recette |
| Non testable (troisième correction, 12/09 soir — contraste entre deux jumeaux qui réidentifient au taux du hasard, donc entre deux bruits ; ni soutenue ni réfutée, §3.3) | 2 | c7-deux-organisations (§2.3, entièrement commis ; verdict retiré du manuscrit — table §7.1, ligne 17, « not testable ») ; **c7-factoriel** (§2.4 — antériorité prouvée, pas seulement déclarée ; réfutation retirée, aucune ligne de tableau) |
| Descriptif (pas de seuil binaire préenregistré) | 1 | c7-echelle |
| Sans résultat à ce jour | 1 | tab2 |

Total : 12+3+12+2+2+1+1 = 33 sur 35 fichiers Tier 1 (les 2 fichiers manquants,
`c7-compromis-bits-preenregistrement.md` et `c7-compromis-robustesse-preenregistrement.md`, n'ont
pas de verdict de catégorie propre : ce sont des contrôles de robustesse dont le résultat est
publié **dans** `c7-compromis-resultats.md`, §3.2). Le total de fichiers ne change pas par
rapport à la seconde correction (toujours 33 sur 35) : seule la catégorie de deux d'entre eux a
changé, de « réfutée » à « non testable ».

Ce tableau porte sur des **fichiers**, souvent multi-prédictions ; il ne doit pas être additionné
naïvement avec le tableau du manuscrit (§7.1, 17 lignes, **14 réfutées, 2 non concluantes, 1 non
testable** après cette troisième correction), qui compte des **lignes de revendication**, pas des
fichiers (par exemple, `c7-attaquant-fort` est un seul fichier « mixte » ici mais fournit plusieurs
lignes au tableau du manuscrit). Les deux comptages restent cohérents entre eux sur le fond (aucune
divergence de verdict trouvée), seulement sur l'unité de dénombrement.

---

## 5. Récapitulatif Tier 1 (fichier, date, empreinte)

| Fichier | 1ʳᵉ apparition git | SHA-256 (abrégé) | Antériorité |
|---|---|---|---|
| c7-preenregistrement.md | 2026-09-11 20:11:12+02:00 | 6e1e5868… | OK |
| a1-controle-preenregistrement.md | 2026-09-11 22:49:56+02:00 | 5201d256… | OK |
| c5-preenregistrement.md | 2026-09-11 20:12:09+02:00 | c11cd810… | OK |
| b123-preenregistrement.md | 2026-09-11 20:14:43+02:00 | b8e78464… | OK |
| c7-compromis-preenregistrement.md | 2026-09-12 00:37:44+02:00 | 2d654195… | OK |
| c7-compromis-bits-preenregistrement.md | 2026-09-12 00:45:58+02:00 | 3b53c72f… | OK |
| c7-compromis-robustesse-preenregistrement.md | 2026-09-12 01:12:03+02:00 | 5b062fb6… | OK |
| c7-disjoint-preenregistrement.md | 2026-09-12 01:44:59+02:00 | 865d3d31… | OK |
| c7-nul-corrige-preenregistrement.md | 2026-09-12 11:39:23+02:00 (commis seul, `5c4cef4`) | 9e5e4482… | **antériorité faible** (déclarée par le commit ; résultat commis séparément dans `09b18d7`, 13:25:16) |
| c7-tautologie-preenregistrement.md | 2026-09-12 11:39:23+02:00 (commis seul, `5c4cef4`) | 1ab40556… | **antériorité faible** (déclarée par le commit ; résultat commis séparément dans `09b18d7`, 13:25:16) |
| c7-temoin-prompt-preenregistrement.md | 2026-09-12 11:39:23+02:00 (commis seul, `5c4cef4`) | 24f8a150… | **antériorité faible** (déclarée par le commit ; résultat commis séparément dans `09b18d7`, 13:25:16) |
| c7-deux-organisations-preenregistrement.md | 2026-09-12 12:46:10+02:00 (commis seul, `24cc79d`) | 07e74fd0… | **antériorité faible** (déclarée par le commit ; résultat commis séparément dans `09b18d7`, 13:25:16) |
| c7-factoriel-preenregistrement.md | 2026-09-12 12:52:49+02:00 (commis seul, `ff90409`) | 6588f6bf… | **antériorité prouvée**, pas seulement déclarée (script d'analyse absent du dépôt au moment de ce commit ; résultat commis dans `ee73f70`, 16:46:27, `HEAD` courant) |
| c7-generateur-preenregistrement.md | 2026-09-12 01:01:51+02:00 | 105947cf… | OK |
| c7-synth-ajuste-preenregistrement.md | 2026-09-12 01:43:20+02:00 | ce7ea52a… | OK |
| c7-mecanisme-preenregistrement.md | 2026-09-11 22:29:58+02:00 | b3b676e7… | OK |
| c7-stanford-preenregistrement.md | 2026-09-12 00:34:22+02:00 | 7fa2967b… | OK |
| c7-stanford-provenance-preenregistrement.md | 2026-09-12 00:55:10+02:00 | 06f525ad… | OK |
| c7-transfert-preenregistrement.md | 2026-09-12 00:55:09+02:00 | 4a33357f… | OK |
| c7-transfert-stanford-preenregistrement.md | 2026-09-12 02:28:30+02:00 | b98dd8eb… | OK |
| c7-monde-ouvert-preenregistrement.md | 2026-09-12 00:56:07+02:00 | 5446aea4… | OK |
| c7-defense-preenregistrement.md | 2026-09-12 00:33:08+02:00 | 25dd2dea… | OK |
| c7-attaquant-fort-preenregistrement.md | 2026-09-12 07:12:56+02:00 | 1b3f19bf… | **même commit que le résultat** |
| c7-dp-preenregistrement.md | 2026-09-12 07:12:13+02:00 | 7213ab3f… | **même commit que le résultat** |
| c7-utilite-aval-preenregistrement.md | 2026-09-12 07:09:58+02:00 | f364a199… | **même commit que le résultat** |
| c7-courbe-gen-preenregistrement.md | 2026-09-12 06:47:37+02:00 | 99e551a7… | OK |
| c7-fort-preenregistrement.md | 2026-09-12 06:51:29+02:00 | 5b88271d… | OK |
| c7-recette-preenregistrement.md | 2026-09-12 01:05:31+02:00 | 8b24d5fd… | OK |
| c7-gen-preenregistrement.md | 2026-09-12 00:51:31+02:00 | 4e5a4e72… | OK |
| c7-bits-preenregistrement.md | 2026-09-12 00:45:58+02:00 | 7c84373a… | OK |
| c7-bits-preenregistrement-avenant.md | 2026-09-12 00:54:32+02:00 | 1ea4ae48… | OK |
| c7-echelle-preenregistrement.md | 2026-09-12 00:40:01+02:00 | 6eb4a094… | OK |
| c7-deviations-preenregistrement.md | 2026-09-12 00:49:14+02:00 | a056db00… | OK |
| tab-preenregistrement.md | 2026-09-11 16:14:56+02:00 | 1de06cab… | OK |
| tab2-preenregistrement.md | 2026-09-11 18:18:11+02:00 | 1876d231… | OK (sans résultat) |

---

## 6. Tier 2 — autres chantiers du dépôt (hors périmètre de l'article C7)

Recensés mais **non analysés en détail** ici (verdicts, prédictions et couplage aux résultats non
vérifiés dans ce recueil) car ils appartiennent à d'autres lignes de recherche du même dépôt :
l'« oracle des camps » (R1-R7, D4), la mémoire à long terme, la détection de population
synthétique (I1, I3, I3b), la croyance de second ordre (S1), la mesure de personne répliquée
(T1, T2), la caricature de profil, et une série de préenregistrements A42-A46/C1 antérieurs au
9 septembre.

| Fichier | 1ʳᵉ apparition git | SHA-256 (abrégé) |
|---|---|---|
| a42-preenregistrement.md | 2026-09-09 12:02:14+02:00 | d08ea039… |
| a43-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 68e2007e… |
| a44-preenregistrement.md | 2026-09-09 12:02:14+02:00 | e71568fd… |
| a46-preenregistrement-composition.md | 2026-09-09 12:02:14+02:00 | 9bc201fa… |
| c1-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 14f06ab1… |
| caricature-profil-preenregistrement.md | 2026-09-11 22:26:14+02:00 | 55ae7157… |
| d4-preenregistrement.md | 2026-09-09 12:20:15+02:00 | 32e14d40… |
| echelle-preenregistrement.md (générique, distinct de c7-echelle) | 2026-09-11 22:50:21+02:00 | 4279f92d… |
| i1-preenregistrement.md | 2026-09-09 12:02:14+02:00 | e546333d… |
| i3-preenregistrement.md | 2026-09-09 12:02:14+02:00 | bde00ace… |
| i3b-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 57f92119… |
| memoire-long-preenregistrement.md | 2026-09-11 22:31:16+02:00 | 73145828… |
| r1-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 96baab6b… |
| r2-preenregistrement.md | 2026-09-09 12:02:14+02:00 | b2684f0e… |
| r2b-preenregistrement.md | 2026-09-11 16:14:56+02:00 | babd8df1… |
| r3-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 24926e0a… |
| r4-preenregistrement.md | 2026-09-09 12:02:14+02:00 | f5c6716b… |
| r5-preenregistrement.md | 2026-09-09 12:02:14+02:00 | e8592ece… |
| r6-preenregistrement.md | 2026-09-09 12:02:14+02:00 | db072973… |
| r6-preenregistrement-v2.md | 2026-09-09 13:14:58+02:00 | 4e9c90d7… |
| r7-preenregistrement.md | 2026-09-11 16:14:56+02:00 | c7c1fa35… |
| s1-preenregistrement.md | 2026-09-09 12:20:15+02:00 | 84870fa0… |
| t1-preenregistrement.md | 2026-09-09 12:02:14+02:00 | 6b8e0f83… |
| t2-preenregistrement.md | 2026-09-09 12:02:14+02:00 | b4ff2653… |

---

## 7. Marche à suivre pour l'utilisateur

1. **Ce qui restait à faire au point 1 de la version précédente de ce recueil est fait** : les
   quatre fichiers de résultats (`c7-tautologie-resultats.md`, `c7-temoin-prompt-resultats.md`,
   `c7-nul-corrige-resultats.md`, `c7-deux-organisations-resultats.md`) sont désormais tous commis,
   chacun séparément de son préenregistrement et après lui (§2.3). Il ne reste **qu'une seule
   catégorie de cas non réparable rétroactivement** : les **trois paires commises dans le même
   commit que leur résultat** (`c7-dp`, `c7-utilite-aval`, `c7-attaquant-fort`, §2.2). Pour
   celles-ci, reconnaître explicitement dans l'article que leur antériorité n'est pas prouvable
   par l'historique git seul — l'historique ne peut pas être réécrit après coup sans perdre sa
   valeur probante, donc republier un préenregistrement identique dans un nouveau commit séparé ne
   répare rien pour ces trois-là (le calcul, lui, a déjà eu lieu). C'est une limite à assumer, pas
   à corriger.
2. **Un nouveau cas, `c7-factoriel` (§2.4), montre à quoi ressemble la version réparée de ce
   problème pour toute future expérience** : préenregistrement commis seul, dans un commit qui ne
   contient ni script d'analyse ni résultat, suivi d'un commit de résultats distinct plusieurs
   heures plus tard. C'est la pratique à reproduire systématiquement pour tout test encore à
   venir, plutôt qu'une correction à appliquer aux trois cas déjà figés du point 1.
3. **Déposer ce recueil** (`resultats/preenregistrements-recueil-2026-09-12.md`) auprès d'un tiers
   horodateur indépendant : OSF (Open Science Framework, dépôt de préenregistrement avec
   horodatage public), ou à défaut un service d'horodatage de document (ex. OriginStamp, ou une
   ancre sur une blockchain publique) qui accepte un fichier texte et retourne un certificat
   vérifiable par un tiers. L'utilisateur doit effectuer ce dépôt lui-même.
4. **Alternative ou complément déjà présent dans le dépôt** : l'historique git public lui-même
   (commit `ee73f708456033d4f919206fa20ac47b348cb093`, `HEAD` courant, qui inclut tous les commits
   cités dans ce recueil et leurs parents) constitue, comme `tab-preenregistrement.md` le
   revendique explicitement pour lui-même, un horodatage tiers si le dépôt est poussé vers une
   plateforme d'hébergement (GitHub, GitLab...) avant tout calcul ultérieur — pleinement pour les
   24 paires « OK » du §2.1 et pour `c7-factoriel` (§2.4, antériorité prouvée) ; avec la limite de
   « faible antériorité » déclarée par leur propre message de commit, pour les quatre
   préenregistrements du §2.3 (leurs résultats sont désormais commis aussi, mais la déclaration de
   faiblesse reste valable) ; pas du tout pour les trois paires commises ensemble du §2.2.

**Ce que ce dépôt prouve, une fois déposé** : que le texte exact de chaque préenregistrement
(question, seuil chiffré, règle de décision) existait, sous cette forme précise, à une date
antérieure vérifiable par un tiers indépendant de l'auteur — pleinement pour les 24 paires en
ordre normal (§2.1) et pour `c7-factoriel` (§2.4, la seule antériorité **prouvée** et non
simplement déclarée par l'historique) ; avec la réserve déclarée par les commits eux-mêmes, pour
les 4 paires du §2.3 (préenregistrement commis avant résultat, mais calcul déjà présent sur le
disque au moment du commit de préenregistrement). Soit 25 paires sur 29 pleinement ou
suffisamment établies. Cela répond directement à l'objection « vous avez choisi vos seuils après
avoir vu vos résultats ».

**Ce que ce dépôt ne prouve pas** : (a) que les calculs eux-mêmes sont corrects. Une correction
publiée le 12/09 montre qu'un bug de méthode — IC bootstrap dégénéré sur zéro succès — a déjà
changé deux verdicts après coup (§4). Une tentative de correction distincte, portant sur le témoin
nul de `c7-disjoint`, a bien identifié un défaut réel (ligne 133 du générateur, §3.3) mais a
d'abord publié un verdict inversé qui ne tenait pas ; un audit adverse l'a détecté avant toute
publication dans l'article, et l'auteur du renversement l'a concédé sans réserve (§3.3). C'est une
preuve de rigueur du processus de relecture interne — une révision qui arrangeait l'article a été
rejetée après vérification — pas une garantie d'absence d'autres bugs non détectés ; (b) que les
trois paires du §2.2 (`c7-dp`, `c7-utilite-aval`, `c7-attaquant-fort`) respectent l'antériorité —
cela reste à démontrer autrement, ou à accepter comme une limite déclarée, et rien ne peut plus le
réparer rétroactivement pour ces trois-là précisément ; (c) que les Tier 2 (24 fichiers, §6), non
analysés ici, respectent les mêmes garanties — un recueil séparé serait nécessaire pour eux si un
dépôt distinct les concernant est un jour envisagé.
