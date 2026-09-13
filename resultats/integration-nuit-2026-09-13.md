# Intégration de la nuit du 12 au 13 septembre 2026 : branche `integration/nuit-2026-09-13`

statut: courant
mandat: construire et vérifier une branche d'intégration portant les branches de mesures, d'audits, de corrections et de portes de la nuit, sans toucher à master ni aux branches de manuscrit, et rendre au responsable une intégration dont chaque porte, chaque marqueur et chaque grandeur ont été contrôlés un par un
agent: Claude Opus 5, Anthropic — sous-agent intégration
ecriture: resultats/integration-nuit-2026-09-13.md ; resultats/registre-chiffres.csv (résolution de conflit, union) ; retrait de deux liens symboliques versionnés par mégarde (.venv, data)
lecture_seule: tout le reste du dépôt
interdits: appel payant, réseau, recherche web, arrière-plan, tout calcul nouveau, commit ou bascule sur master, fusion des branches de manuscrit, écriture dans article/manuscrit.md
cecite: aucun script d'analyse n'a été rejoué ; aucun chiffre n'a été recalculé ; article/manuscrit.md n'a été ni lu pour écriture ni modifié (il appartient à un autre agent) ; les branches agent/manuscrit/* et agent/latex/*, agent/biblio/anteriorites, agent/orchestrateur/*, agent/portes/entete-outil, agent/portes/g31-marqueur, agent/redaction/renvois-internes n'ont pas été ouvertes
cout_reel_usd: 0.00

Travail conduit **exclusivement** dans un `git worktree` isolé (`/tmp/wt-integration`).
`master` n'a été ni fusionné, ni poussé, ni réinitialisé, ni même basculé : le dépôt principal
est resté sur `master` sans qu'une seule commande d'écriture ne l'atteigne.

---

## 1. En dix lignes

**Dix-sept branches sont intégrées**, aucune écartée sauf `agent/mesures/nul-corrige-csv`,
dont le caractère périmé a été **vérifié et non présumé** (§4). Le registre de chiffres compte
**53 grandeurs** — pas 37 : la synthèse ne connaissait pas encore les seize lignes de
`agent/correction/dp-chiffres-opposables`. **Un seul conflit** s'est produit, sur
`resultats/registre-chiffres.csv`, résolu en **union stricte** par un script vérifiable, sans
qu'aucune ligne ne soit remplacée ni perdue.

**Les treize affirmations marquées ont toutes survécu** : les huit rapports amendés ou bornés
portent leur clé d'en-tête et leur `fait_foi:`, l'unique marqueur canonique de rétractation du
dépôt pointe toujours sur une cible existante, et **aucune cible de `fait_foi:` ne pend dans le
vide**. Le nul de marge vaut **0,980**, statut `courant` ; le 0,974 est `retracte`. Aucune
grandeur rétractée n'est redevenue `courant`.

**Les tests passent : 129, dont 1 ignoré** (78 avant : les deux portes neuves en apportent 51).
**Trois portes restent fermées en mode diff**, pour des dettes que les branches portaient
**déjà séparément** — ce n'est pas la fusion qui les crée, et le §6 le démontre branche par
branche. **Deux d'entre elles doivent être traitées avant le report sur `master`.**

---

## 2. Ce qui est intégré, et dans quel ordre

Ordre effectivement exécuté, conforme à celui du mandat et de
`resultats/etat-des-lieux-2026-09-13.md`.

**Groupe A — la rétractation d'abord, pour que rien ne pointe dans le vide.**

| # | branche | résultat |
|---|---|---|
| 1 | `agent/audit/comparaison-dp` | propre — c'est la cible du `fait_foi:` de la suivante |
| 2 | `agent/correction/retractation-dp` | propre (mais voir §5, deux liens symboliques) |
| 3 | `agent/correction/dp-chiffres-opposables` | propre — **+16 lignes de registre** |

**Groupe B — additions.**

| # | branche | résultat |
|---|---|---|
| 4 | `agent/mesures/residu-trajectoire` | propre |
| 5 | `agent/mesures/equite-risque` | propre |
| 6 | `agent/audit/predictibilite` | propre — après (5), dont il attaque la phrase |
| 7 | `agent/mesures/controle-generateur` | propre |
| 8 | `agent/audit/comparateur-conditionne` | propre — **après (7)**, dont il amende la conclusion |
| 9 | `agent/audit/contamination-persona` | propre |
| 10 | `agent/mesures/attaquant-imparfait` | propre |
| 11 | `agent/audit/items-banals` | propre |
| 12 | `agent/mesures/temoins-relecture` | propre |
| 13 | `agent/mesures/t1a-complements` | propre |
| 14 | `agent/audit/park-armement-egal` | propre |

**Groupe C.**

| # | branche | résultat |
|---|---|---|
| 15 | `agent/correction/marqueurs-canoniques` | **conflit unique**, résolu en union (§3) |
| 16 | `agent/portes/coherence-chiffres` | propre — apporte les portes P8 et P9 |
| 17 | `agent/correction/t1b-cent-replicats` | **déjà intégrée** — voir ci-dessous |

**La contrainte de porte annoncée n'a pas eu à être levée à la main.** La synthèse prévoyait
que `agent/audit/items-banals` fermerait P4 sur une ligne `statut:` non conforme et exigeait
une réparation avant fusion. Cette réparation est **déjà portée par
`agent/correction/marqueurs-canoniques`**, qui remet la valeur à `courant`. L'ordre du mandat
plaçant `marqueurs-canoniques` après `items-banals`, la porte est momentanément fermée entre
(11) et (15) puis rouverte : elle est **ouverte à l'état final**, seul état qui compte.

### `t1b-cent-replicats` n'a pas eu à être fusionnée séparément

`git merge` répond **« Déjà à jour »** : la branche est un **ancêtre** de
`agent/correction/marqueurs-canoniques`, qui avait déjà fusionné dans sa propre histoire neuf
branches de la nuit, dont `t1b`. C'est la raison pour laquelle **le conflit de registre annoncé
pour `t1b` est apparu au moment de fusionner `marqueurs-canoniques`** : c'est bien le même
conflit, entre les mêmes deux apports, porté par une autre référence. Vérifié explicitement :

    git merge-base --is-ancestor origin/agent/correction/t1b-cent-replicats HEAD   → vrai

---

## 3. Le conflit, et comment il est résolu

**Fichier** : `resultats/registre-chiffres.csv`. **Unique conflit de toute l'intégration.**

Analyse des trois états, par identifiant, avant toute décision :

| état | lignes | contenu |
|---|---|---|
| base commune | 33 | le registre de `master` |
| notre côté (groupes A+B) | 52 | +3 de `retractation-dp`, +16 de `dp-chiffres-opposables` |
| leur côté (`marqueurs-canoniques`) | 34 | +1 ligne, +1 ligne modifiée |

**Aucune suppression d'aucun côté. Aucune ligne modifiée des deux côtés à la fois.** Ce n'est
donc pas un arbitrage : c'est une **union**, et elle est mécanique.

- les 19 lignes que seul notre côté ajoute sont conservées ;
- la ligne que seul leur côté ajoute, `rho-nul-marge-appariee-12conf-n100`, est insérée **à sa
  place** (juste après la ligne qu'elle remplace, comme chez eux) ;
- la seule ligne modifiée d'un seul côté, `rho-nul-marge-appariee-12conf`, prend **la version
  rétractante** : `statut` passe de `provisoire` à `retracte`, et `csv_source` cesse d'être
  `ABSENT` pour nommer sa cellule.

**Total : 53 grandeurs, identifiants uniques vérifiés.** La résolution n'a pas été faite à la
main : un script de fusion refuse de produire un résultat si une ligne disparaît, si une ligne
est modifiée des deux côtés différemment, ou si un identifiant se duplique. Les en-têtes des
trois versions sont identiques (mêmes douze colonnes), ce qui a été vérifié avant l'union.

Le compte de 37 annoncé par la synthèse **n'est pas une erreur de sa part** : il vaut
33 + 3 + 1, et il ignore les seize lignes `dp-zcdp-*` et `dp-s8-*` apportées depuis par
`agent/correction/dp-chiffres-opposables`. **Compté, non présumé : 53.**

---

## 4. La branche écartée, et la vérification qui l'écarte

`agent/mesures/nul-corrige-csv` — **écartée**. La consigne demandait de vérifier cette
affirmation plutôt que de la reprendre. Elle est vérifiée, et elle est **exacte**.

Les deux branches livrent `resultats/c7-nul-corrige-marginal.csv` avec **exactement 143 lignes
de part et d'autre**, et **la même répartition** : 101 lignes à 100 réplicats, 42 à 20. La
série à 100 réplicats est donc **déjà présente** dans la version écartée : elle n'apporte
aucune donnée que `t1b` n'ait.

La seule différence de fond est la **désignation de ce qui fait foi** :

| | `nul-corrige-csv` | `t1b-cent-replicats` |
|---|---|---|
| `fait_foi_tableau1 = oui` porté par | la série à **20** réplicats | la série à **100** réplicats |

Et dans `analyses/c7_temoin_verite_appariee.py`, l'unique écart est la condition
`N_REP == 20` au lieu de `N_REP == 100`, `t1b` portant en plus le commentaire qui explique que
le préenregistrement prescrivait 100. **La fusionner ferait donc exactement ce que la synthèse
annonçait : rebasculer silencieusement le témoin sur la série hors protocole.** Rien d'unique
n'a été trouvé. Elle est écartée sans réserve, et il n'y a rien à en récupérer.

Écartées également, conformément au mandat et **sans avoir été ouvertes** : les branches de
manuscrit `agent/manuscrit/t3`, `t4`, `t5`, `final`, `pagination`. Vérifié : aucune n'est
ancêtre de la branche d'intégration, et `article/manuscrit.md` est **identique à `master`,
octet pour octet**.

---

## 5. Un défaut trouvé au passage : deux liens symboliques versionnés par mégarde

Le commit `f1c1416` de `agent/correction/retractation-dp` versionne deux liens symboliques
vers des chemins **absolus** de la machine de l'auteur :

    .venv -> /Users/…/popsim/.venv
    data  -> /Users/…/popsim/data

Les deux chemins sont **déjà déclarés dans `.gitignore`** (lignes 4, 20 et 45). C'est un
accident d'arbre de travail, pas un apport de la branche : sur toute autre machine ils pointent
dans le vide, et un `.venv` à la racine expose les parcours d'arbre des portes à un répertoire
d'environnement.

**Traitement** : les deux liens sont retirés dans un commit **isolé et distinct de toute
fusion**, pour que le responsable puisse le révoquer seul s'il juge ces liens volontaires.
Aucun contenu scientifique n'est touché. Les 129 tests passent avant comme après.

---

## 6. L'état de chaque porte, avant et après

### 6.1 Sur le dépôt entier

| porte | avant (`master`) | après | lecture |
|---|---|---|---|
| P1 `preenregistrement_seul` | 858 violations | 934 | dette historique, +76 par les nouveaux préenregistrements |
| P2 `registre_chiffres` (intégrité) | **OK**, 33 grandeurs | **OK**, 53 grandeurs | reste ouverte |
| P3 `interdits` | **OK** | **OK** | reste ouverte |
| P4 `entetes` | 366 violations | **363** | **améliorée** : trois en-têtes posés malgré ~30 fichiers neufs |
| P5 `renvois` | 13 violations | 15 | +2, analysés en 6.3 |
| P6 `horodatage` | 61 violations | 67 | +6 préenregistrements neufs sans reçu `.ots` |
| P8 `coherence_csv` | *n'existait pas* | **OK** — 357 fichiers lus, **zéro faux positif** | porte neuve, exigence tenue |
| P9 `conformite_preenregistrement` | *n'existait pas* | **OK** (inerte tant que les deux colonnes manquent) | porte neuve |

**L'exigence portant sur P8 est tenue** : sur le dépôt entier, 357 fichiers lus, un marqueur
`CHIFFRE:` résolu jusqu'à sa cellule, **aucune violation et aucun faux positif**.

### 6.2 En mode diff — ce que la CI contrôle réellement

Le fichier `.github/workflows/portes.yml` fait foi sur ce qui bloque. Résultats contre
`origin/master`, dans l'ordre des étapes de la CI :

| étape CI | verdict |
|---|---|
| tests des portes | **OK — 129 tests** (1 ignoré) |
| P1 `--depuis` | **FERMÉE — 90 violations** |
| P2 `--registre-seul` | **OK** — 53 grandeurs |
| P2 `--depuis --mode avertissement` | avertissement, 3 464 nombres en dur — **non bloquant par conception** |
| P3 (dépôt entier) | **OK** |
| P4 `--depuis` | **OK** |
| P4 `--retractation --depuis` | **OK** — c'est la porte de la discipline des marqueurs |
| P5 `--depuis` | **FERMÉE — 3 violations** |
| P6 `--etat` puis `--depuis` | **FERMÉE — 6 violations** |

Les 3 464 nombres en dur de P2 **ne sont pas une régression** : la CI lance délibérément cette
étape en mode avertissement (« DETTE : 340 valeurs en dur dans le manuscrit ; mode avertissement
jusqu'à la migration »). Mesuré : `agent/audit/comparaison-dp` **seule**, non fusionnée, en
produit déjà 101.

### 6.3 Les trois portes fermées : la fusion en est-elle la cause ?

Question posée parce qu'elle est la seule qui compte. Réponse obtenue en rejouant les portes
sur les branches **isolées**, dans des arbres jetables.

- **P1 (90) et P6 (6)** — **dettes de branche, antérieures à toute fusion.**
  `agent/mesures/attaquant-imparfait` seule, contre `origin/master`, ferme déjà P1 (11
  violations) et P6 (1). Chaque branche a commis son préenregistrement avec ses résultats au
  lieu de le commettre seul, et sans reçu d'horodatage. La fusion **additionne** ces dettes,
  elle n'en crée aucune.

- **P5 (3)** — **une seule des trois naît de la fusion, et c'est la seule intéressante.**

  | # | renvoi fautif | origine |
  |---|---|---|
  | 1 | `audit-comparaison-dp-2026-09-13.md:6` renvoie à une section 9 de lui-même, qui n'existe pas | **dette de branche** : `comparaison-dp` seule ferme déjà P5 |
  | 2 | `retractation-dp-d4-2026-09-13.md:231` renvoie à une section 8 de l'audit DP, qui n'en a pas | **née de la fusion** : `retractation-dp` seule passe P5, parce que le fichier cible n'existe pas encore et que la porte ne peut pas vérifier un renvoi vers un fichier absent |
  | 3 | `revue-hostile-gel-2026-09-12.md:103` renvoie à une section 5.1 de `audit-renversement`, qui n'en a pas | **défaut préexistant sur `master`** (il y figurait déjà, ligne 69) : il devient visible en mode diff parce que `marqueurs-canoniques` a touché le fichier pour y poser un en-tête |

  Le cas 2 est exactement la classe de faute que la nuit a traquée : **un renvoi qu'aucune
  porte ne pouvait contrôler tant que les deux branches vivaient séparément.** Il ne devient
  vérifiable qu'à la fusion, et il est faux.

**Aucune de ces trois corrections n'a été faite ici.** Ce sont des corrections de numéro de
section dans des documents d'audit dont je ne suis pas l'auteur ; les trancher au jugé
reviendrait à réécrire la prose d'un audit sans savoir quelle section était visée. Elles sont
signalées au §8 comme le travail restant.

---

## 7. Les marqueurs ont-ils survécu ? Vérification une par une

C'est le risque que la fusion faisait courir, et c'est le cœur du mandat.
`resultats/marqueurs-canoniques-2026-09-13.md` recense treize affirmations. Contrôle après
fusion, fichier par fichier :

| rapport amendé | `statut:` | clé posée | `fait_foi:` | cible existe |
|---|---|---|---|---|
| `c7-attaquant-imparfait-resultats.md` | `provisoire` | `amende_par:` | oui | oui |
| `c7-equite-risque-resultats.md` | `provisoire` | `amende_par:` | oui | oui |
| `c7-controle-generateur-resultats.md` | `provisoire` | `borne_par:` | oui | oui |
| `c7-temoins-relecture-resultats.md` | `provisoire` | `borne_par:` | oui | oui |
| `c7-t1a-complements-resultats.md` | `provisoire` | `borne_par:` | oui | oui |
| `c7-nul-corrige-marginal.md` | `provisoire` | `borne_par:` | oui | oui |
| `audit-renversement-2026-09-12.md` | `provisoire` | `borne_par:` | oui | oui |
| `revue-hostile-gel-2026-09-12.md` | `provisoire` | `borne_par:` | oui | oui |
| `c7-dp-resultats.md` | `retracte_par: …` | — | oui | oui |

**Les huit rapports amendés ou bornés portent tous leur clé et leur `fait_foi:`. Aucun n'a
perdu son marqueur à la fusion.**

**L'unique marqueur canonique de rétractation du dépôt est intact** : une seule ligne en
colonne 0 dans tout `resultats/`, à la ligne 11 de `retractation-dp-d4-2026-09-13.md`,
nommant `c7-dp-resultats.md` — dont l'en-tête porte bien `retracte_par:` et `fait_foi:`. La
porte `P4 --retractation`, celle qui vérifie que l'audité est marqué **dans le même commit**,
**passe**.

**Aucune cible de `fait_foi:` ne pend dans le vide** : les neuf cibles distinctes déclarées
dans `resultats/` existent toutes après fusion. Et les quatorze fichiers qui font foi pour les
treize affirmations — les trois audits, les six CSV de mesure, `correction-t1b`,
`c7-residu-trajectoire-resultats.md`, `c7-t1a-complements-resultats.md` — sont tous présents.

**Le seul trou est celui que le document nommait déjà lui-même**, et la fusion ne le referme
pas : l'affirmation « *Statistical comparators stay indistinguishable from noise at both FPRs* »
n'est publiée qu'au manuscrit, hors de portée de cette intégration comme de l'agent qui a posé
les marqueurs. **Elle reste sans marqueur canonique, et elle appartient à l'agent propriétaire
du manuscrit.** C'est le point à ne pas perdre au report.

**Ce que la fusion ne protège toujours pas**, et qui ne peut pas l'être par une porte : la
section 7 de `c7-attaquant-imparfait-resultats.md` emploie des formulations qu'un autre rapport
interdit. Le fichier porte désormais `amende_par:` et une section d'amendement en tête, ce qui
rend le lien **machine-lisible** — c'est le gain réel de `marqueurs-canoniques` — mais le corps
d'origine est conservé mot pour mot, par discipline. Un relecteur qui ne lit que la section 7
lira encore la formulation interdite.

---

## 8. Ce que le responsable doit trancher avant de reporter

Par ordre décroissant de gravité. **Aucun de ces points n'a été tranché ici.**

1. **P5, renvoi né de la fusion** — `retractation-dp-d4-2026-09-13.md:231` renvoie à une
   section 8 d'un audit qui n'en a pas. Corriger le numéro, ou le titre visé dans l'audit.
   Bloquant en CI.
2. **P5, dette de branche** — `audit-comparaison-dp-2026-09-13.md:6` renvoie à une section 9
   de lui-même, absente. Bloquant en CI.
3. **P1 (90) et P6 (6)** — préenregistrements commis avec leurs résultats et sans reçu
   d'horodatage, sur la quasi-totalité des branches de mesure. Bloquant en CI, mais
   **rigoureusement antérieur à cette intégration** : c'est une décision de discipline, pas une
   correction d'intégration.
4. **Le retrait des deux liens symboliques** (§5) — à confirmer ou à révoquer ; le commit est
   isolé pour cela.
5. **L'affirmation non rattachée du manuscrit** (§7) — à transmettre à l'agent propriétaire de
   `article/manuscrit.md`, qui est le seul à pouvoir poser ce marqueur.

---

## 9. La commande de report sur `master`

**À lancer par le responsable, et par personne d'autre.** Rien ici n'a touché `master` ; c'est
la première commande de tout ce document qui l'écrit.

Relecture d'abord, sans rien modifier :

    git fetch origin
    git log --oneline --graph origin/master..integration/nuit-2026-09-13
    git diff --stat origin/master integration/nuit-2026-09-13

Report, une fois les points du §8 tranchés :

    git switch master
    git merge --no-ff integration/nuit-2026-09-13 \
        -m "Integration de la nuit du 12 au 13 septembre 2026 (17 branches)"
    git push origin master

**Avant de pousser**, rejouer la séquence de la CI depuis l'arbre fusionné :

    python -m unittest discover -s tests/portes -t tests/portes -p "test_*.py"
    python outils/portes/registre_chiffres.py --registre-seul
    python outils/portes/interdits.py
    python outils/portes/entetes.py --depuis origin/master
    python outils/portes/entetes.py --retractation --depuis origin/master
    python outils/portes/coherence_csv.py --tous

Ces six contrôles **passent** sur la branche d'intégration telle qu'elle est livrée. Les trois
autres étapes de la CI — P1, P5 et P6 en mode diff — **échouent**, pour les motifs disséqués au
§6.3 ; le report ne doit pas être poussé avant que les points 1 à 3 du §8 soient tranchés.

**`agent/mesures/nul-corrige-csv` ne doit pas être fusionnée**, ni avant ni après, pour le
motif établi au §4. Les branches de manuscrit forment une chaîne linéaire qui se fusionnera
d'un seul tenant, **après** le travail de l'agent qui détient `article/manuscrit.md`.
