# Audit de l'affirmation « les 45 items les plus banals donnent 30,25 % » (13 septembre 2026)

statut: preenregistrement (section 0 ecrite et commitee AVANT tout calcul)
mandat: attaquer l'affirmation D4 de la branche agent/mesures/attaquant-imparfait — selection post hoc, balayage cache, mecanisme, baseline, dependance a l'attaquant, controle d'interpretabilite
agent: Opus 5, Anthropic
ecriture: resultats/audit-items-banals-2026-09-13.md, analyses/c7_audit_items_banals.py, resultats/c7-audit-items-banals.csv
lecture_seule: tout le reste, y compris article/manuscrit.md et la branche auditee
interdits: appel paye, reseau, recherche web, commit sur master, fusion, arriere-plan
cout_reel_usd: 0.0

---

## 0. Préenregistrement, écrit avant le script et avant le moindre chiffre nouveau

### 0.1 Ce qui est audité

La branche `agent/mesures/attaquant-imparfait` établit, volet D4 :

> attaquant restreint aux 45 items les plus ordinaires → **30,25 %** [28,37 ; 32,19] de
> ré-identification top-1, contre **20,57 %** [18,91 ; 22,27] avec les 60 items et **12,91 %**
> avec 45 items tirés au hasard ; deux mesures de banalité concordent (r = −0,956) ; le
> confondant « mêmes items pour tous » est écarté (D1b, 12,52 %).

Cette affirmation arrange l'article (elle rend la menace plus réaliste et fait du 20,57 %
publié une sous-estimation). Elle est donc attaquée, pas confirmée.

### 0.2 Le défaut structurel suspecté

Dans `c7_attaquant_imparfait.py`, le critère de banalité (`entropies_items`, `frequences_modales`)
est calculé sur `pool` — **exactement la matrice des humains vague 4 qui sert ensuite de bassin de
candidats et de vérité pour mesurer le taux**. Les 45 items sont donc choisis sur les mêmes
personnes que celles sur lesquelles le taux est mesuré. Le volet D4 tourne en outre à
`repetitions = 1` : aucune variabilité n'est échantillonnée. Le seul test propre est **hors pli**.

### 0.3 Protocole (bassin rigoureusement constant, graine fixée)

Bassin de départ identique à celui audité : `preparer()` de la branche, 2 058 personnes,
60 items toujours renseignés, candidat `JSON Persona - GPT4.1`, baseline `Demographics Only -
GPT4.1-mini` **recalculée dans chaque condition sur exactement le même sous-ensemble d'items et
le même pool**. Réduction déclarée, identique à celle de la branche auditée : 5 tirages de
départage des ex æquo au lieu de 20 ; bootstrap 2 000.

- **V1 — hors pli.** Les 2 058 personnes sont coupées en deux moitiés A et B (permutation de
  graine fixe). Le classement de banalité est estimé sur les **réponses humaines de A seulement**,
  et le taux est mesuré **sur B seulement** (personnes attaquées = B, pool de candidats = B).
  Symétrique (B → A), les deux plis moyennés. Conditions mesurées sur le **même demi-bassin**,
  donc à taille de bassin constante : (a) 45 items banals choisis hors pli, (b) 45 items banals
  choisis **dans** le pli (réplique du défaut, pour isoler l'effet de la sélection), (c) 45 items
  aléatoires communs, (d) les 60 items.
- **V2 — balayage.** k ∈ {6, 10, 15, 20, 30, 40, 45, 50, 55, 60}, hors pli, critère entropie.
  Profil complet publié, pic identifié s'il existe.
- **V3 — nombre de modalités.** Même balayage, classement par **nombre de modalités croissant**
  (égalités départagées par une permutation de graine fixe, jamais par l'entropie), estimé hors
  pli lui aussi.
- **V4 — A-LLR.** Condition centrale (45 banals / 45 aléatoires communs / 60 items) rejouée sous
  l'attaquant fort A-LLR de `c7_attaquant_fort.scores_hors_pli`, importé sans réimplémentation,
  sur le bassin complet de 2 058. Baseline démographique également sous A-LLR.
- **V5 — contrôle d'interprétabilité.** `c7_controle_interpretabilite.controle_avant_interpretation`
  appliqué à la condition « 45 items banals » avant toute interprétation.

Aucune donnée individuelle n'est calculée, imprimée ou écrite : taux agrégés seuls.

### 0.4 Prédictions, et ce qui les réfute

| | prédiction | réfutée si |
|---|---|---|
| **P1** | L'entropie d'un item est une statistique de population très stable ; à n ≈ 1 029 par moitié, le classement hors pli sera presque identique au classement dans le pli. Le taux hors pli à k = 45 sera **à moins de 3 points** du taux dans le pli, et restera **au-dessus** du taux à 60 items sur le même demi-bassin. | écart hors pli / dans le pli > 3 points, **ou** le taux hors pli à k = 45 cesse d'être strictement au-dessus du taux à 60 items (IC bootstrap) |
| **P2** | Il **existe un pic** strictement à l'intérieur de la plage : le taux monte de k = 6 à un maximum situé entre k = 40 et k = 55, puis redescend vers 60. Publier la valeur du pic sans dire qu'on a balayé serait une sélection déguisée. | le profil est monotone croissant jusqu'à 60 (pas de pic), **ou** le maximum est atteint à k = 60 |
| **P3** | Le nombre de modalités est le vrai facteur : le classement par nombre de modalités croissant restitue **au moins 80 %** du gain (taux à k = 45 ≥ 27 % si le gain entropie vaut 30 %). | le classement par nombre de modalités restitue moins de 50 % du gain |
| **P4** | La baseline démographique **monte plus que proportionnellement** sur les items banals. Lecture (non une prédiction) du CSV audité : ratio candidat/baseline 5,93 à k = 45 banals contre 9,94 à 60 items et 9,84 à 45 aléatoires. Je prédis que ce **renversement de ratio survit hors pli** : ratio(45 banals) < ratio(60 items). | ratio(45 banals) ≥ ratio(60 items) hors pli |
| **P5** | A-LLR pondère les accords par leur rareté : il exploite déjà ce que Hamming gaspille. Je prédis que le gain des items banals **s'effondre** sous A-LLR : gain(45 banals − 60 items) sous A-LLR **inférieur à la moitié** du gain sous Hamming. | le gain sous A-LLR vaut au moins la moitié du gain sous Hamming |
| **P6** | Le contrôle d'interprétabilité **passe** à 45 items banals (30 % contre ~5 %, IC très écartés). | le contrôle échoue |

### 0.5 Critère de verdict, fixé d'avance

- **À retirer** si P1 est réfutée du côté « la sélection fait le résultat » (le gain disparaît hors
  pli), **ou** si sous A-LLR les 45 items banals ne font pas mieux que les 60 items.
- **À affaiblir**, avec reformulation obligatoire, si P1 tient mais qu'au moins une de ces choses
  est vraie : un pic existe dans le balayage (P2 confirmée → c'est un réglage), le ratio à la
  baseline se dégrade (P4 confirmée → l'avantage propre au jumeau rétrécit), ou le nombre de
  modalités suffit (P3 confirmée → l'énoncé « items banals » est faux, il faut écrire « items à
  peu de modalités »).
- **Publiable tel quel** seulement si : P1 tient, P2 réfutée (pas de pic), P4 réfutée (le ratio
  tient), P5 réfutée (le gain survit à A-LLR), P6 confirmée.

Je note d'avance que trois de mes six prédictions vont **contre** l'article et trois seulement
décrivent une stabilité technique. Les résultats de la section 1 et suivantes sont écrits après
exécution, sans modification de la présente section 0.
