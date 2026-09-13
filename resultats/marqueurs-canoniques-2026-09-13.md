# Marqueurs canoniques de la nuit du 12 au 13 septembre 2026 — le document à relire avant de fusionner

statut: courant
mandat: Recenser les couples rapport-audité / audit-qui-l'amende produits dans la nuit, poser sur chaque affirmation amendée le marqueur canonique de la discipline du dépôt, rétablir les valeurs des CSV là où un arrondi favorable a franchi une borne, et publier la liste opposable des formulations désormais interdites avec le rapport qui les interdit. Aucun calcul nouveau, aucun appel payant, aucun réseau.
agent: Claude Opus 5, Anthropic — sous-agent marqueurs canoniques
ecriture: resultats/marqueurs-canoniques-2026-09-13.md ; et, dans les rapports amendés, l'en-tête et une section d'amendement seulement — resultats/c7-attaquant-imparfait-resultats.md, resultats/c7-equite-risque-resultats.md, resultats/c7-controle-generateur-resultats.md (plus un arrondi au §3), resultats/c7-temoins-relecture-resultats.md, resultats/c7-t1a-complements-resultats.md, resultats/c7-nul-corrige-marginal.md, resultats/revue-hostile-gel-2026-09-12.md, resultats/audit-comparateur-conditionne-2026-09-13.md (deux arrondis et une ligne de traçabilité), resultats/audit-items-banals-2026-09-13.md (ligne « statut: » rendue conforme au gabarit A2)
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, tout calcul de résultat nouveau ; **article/manuscrit.md**, **resultats/article-synthese.md**, et tout fichier des branches `agent/audit/contamination-persona`, `agent/correction/dp-chiffres-opposables`, `agent/audit/park-armement-egal`, `agent/synthese/etat-2026-09-13` — notamment `resultats/registre-chiffres.csv`, `resultats/c7-dp-resultats.md`, `resultats/retractation-dp-d4-2026-09-13.md`, `resultats/cout-defense-synthese-2026-09-13.md`, `resultats/c7-dp-courbe-combinee.csv`
cecite: je n'ai pas lu article/manuscrit.md ni resultats/article-synthese.md (propriété d'autres agents) ; je n'ai pas rejoué un seul script ; les branches `agent/audit/contamination-persona` et `agent/audit/park-armement-egal` n'étaient pas poussées et je ne les ai pas ouvertes, leurs éventuels couples ne sont donc pas recensés ici
cout_reel_usd: 0.00

---

## 0. Le défaut que ce document répare

Au matin du 13 septembre, **un seul marqueur canonique de rétractation existait dans tout le
dépôt** : celui de la comparaison avec la confidentialité différentielle, posé sur
`agent/correction/retractation-dp` sous la forme prescrite par `gabarits/entete.md` —

    RETRACTE: resultats/c7-dp-resultats.md

(cité ici indenté, pour ne pas déclencher la porte P4.)

Tout le reste de la nuit — une dizaine d'affirmations retirées, requalifiées ou rétrécies —
n'était invalidé **qu'en prose**, dans des rapports que rien n'oblige à lire. Conséquence
mécanique à la fusion : des rapports auraient publié des formulations qu'un autre rapport
interdit nommément, et **aucune porte ne l'aurait bloqué**. Le cas le plus net était le §7 de
`c7-attaquant-imparfait-resultats.md`, qui publie les trois formulations que
`audit-items-banals-2026-09-13.md` interdit.

**Discipline suivie.** Celle de `agent/correction/retractation-dp`, imitée exactement :
en-tête A2 modifié, clé qui nomme le document amendant, `fait_foi:` obligatoire, section
d'amendement en tête, **et corps d'origine conservé mot pour mot**. Rien n'est supprimé nulle
part. Trois états sont distingués :

| état | définition | clé d'en-tête posée | `statut:` |
|---|---|---|---|
| **rétracté** | l'affirmation est **fausse** | `retracte_par:` + marqueur `RETRACTE:` | `retracte_par: …` |
| **amendé** | la formulation change, **le fait tient** | `amende_par:` | `provisoire` |
| **borné** | le fait tient dans un **périmètre plus étroit**, nommé | `borne_par:` | `provisoire` |

**Aucun marqueur `RETRACTE:` n'est posé ici, et c'est délibéré.** Aucune affirmation de la
nuit n'est fausse au point d'invalider un rapport entier : les audits concluent tous à
l'affaiblissement ou au rétrécissement. Un marqueur de trop décrédibiliserait les autres. Le
seul `RETRACTE:` du dépôt reste celui de la DP.

`outils/portes/entetes.py --depuis origin/master` : **OK, aucune violation**, 17 fichiers
contrôlés. Il échouait avant cette branche, sur la ligne `statut:` de
`audit-items-banals-2026-09-13.md` (parenthèse explicative dans la valeur) — rendue conforme.

---

## 1. Les couples recensés

### 1.1 Les couples que le mandat nommait

| rapport audité | audit qui l'amende | état | marqueur posé |
|---|---|---|---|
| `c7-attaquant-imparfait-resultats.md` | `audit-items-banals-2026-09-13.md` | **amendé** | oui, §0 |
| `c7-equite-risque-resultats.md` | `audit-predictibilite-2026-09-13.md` | **amendé** | oui, §0 bis |
| `c7-controle-generateur-resultats.md` | `audit-comparateur-conditionne-2026-09-13.md` | **borné** ×2 | oui, §0 |
| `c7-temoins-relecture-resultats.md` | `c7-residu-trajectoire-resultats.md` | **borné** | oui, bandeau |
| `c7-t1a-complements-resultats.md` | `c7-residu-trajectoire-resultats.md` | **borné** | oui, bandeau |
| `c7-nul-corrige-marginal.md` (série à 20 réplicats) | `correction-t1b-2026-09-13.md` | **borné** (fichier) / **rétracté** (la désignation « la série à 20 fait foi ») | en-tête posé ; le bandeau de prose existait déjà, il ne portait pas le `statut:` |

### 1.2 Le couple que le mandat n'avait pas listé, et c'est le plus dangereux

| rapport | amendé par | état | pourquoi il est dangereux |
|---|---|---|---|
| `revue-hostile-gel-2026-09-12.md` | `correction-t1b-2026-09-13.md` | **borné** | son défaut D1 ne se contente pas de citer un chiffre périmé : il **prescrit de l'écrire dans le manuscrit** (« Remplacer l. 76 et la ligne 1 du tableau 1 par “0.974 [0.950 ; 0.993]” »). C'est une consigne exécutable par un autre agent, sur un fichier que je n'ai pas le droit de toucher. Elle est désormais bornée à sa source. |

Ce fichier n'avait **aucun en-tête A2** : il en porte un maintenant, reconstitué depuis son
propre corps, avec la mention explicite de qui l'a posé.

### 1.3 Les couples cherchés et NON trouvés

- `agent/audit/comparaison-dp` × `c7-dp-resultats.md` : couple réel, **déjà traité** par
  `agent/correction/retractation-dp`, avec le seul marqueur canonique du dépôt. Rien à faire,
  et ces fichiers appartiennent à `agent/correction/dp-chiffres-opposables`.
- `agent/mesures/nul-corrige-csv` : superséré par `agent/correction/t1b-cent-replicats`, qui
  le contient. Fusionner t1b suffit.
- `c7-residu-trajectoire-resultats.md` cite `temoins-relecture` en **confirmation**, pas en
  contradiction (le point de raccord 1,160 % à k = 12 est compatible avec le 1,2193 %
  [1,1118 ; 1,3301] mesuré indépendamment). Aucun marqueur n'est dû de ce côté-là.
- Les branches `agent/audit/contamination-persona` et `agent/audit/park-armement-egal`
  n'étaient pas poussées : leurs couples éventuels ne sont pas dans ce tableau.

---

## 2. La table des affirmations de la nuit

Aucun chiffre de ce tableau qui ne soit lu dans un CSV nommé.

| # | affirmation | état | fichier qui fait foi | la valeur, telle qu'elle est au CSV |
|---|---|---|---|---|
| 1 | « les 45 items les plus **banals** donnent 30,25 % » | **amendé** | `audit-items-banals-2026-09-13.md` §8 | items **binaires**, pas banals ; pic à k = 40 : 36,37 % [33,54 ; 39,19] (`c7-audit-items-banals.csv`, V2) |
| 2 | « donc notre 20,57 % **sous-estime** le risque » | **rétracté** (l'inférence est fausse) | idem §8 | le multiplicateur imputable au jumeau **tombe** : ×9,87 → ×5,96 (Hamming), ×28,18 → ×7,81 (A-LLR) — `c7-audit-items-banals.csv`, V4 |
| 3 | « une base commerciale ordinaire suffit » | **rétracté** | idem §8 | rien ne l'établit : propriété du questionnaire Twin, pas d'une base commerciale |
| 4 | « la fuite suit la **prédictibilité**, non la rareté » | **amendé** — « affaiblie et renommée », **pas retirée** | `audit-predictibilite-2026-09-13.md` §1, §7, §8 | ρ(prédictibilité hors pli, rareté moyenne) = **−0,702** : les deux ne sont pas opposables (`c7-audit-predictibilite.csv`) |
| 5 | la moitié **« rareté »** : les plus exposés ne sont pas les plus atypiques | **TIENT** — aucun marqueur | idem §6 | ρ = −0,185 [−0,228 ; −0,138] et −0,237 [−0,275 ; −0,198] **sous A-LLR pondéré par la rareté** ; la prédiction d'inversion P6 est **réfutée** |
| 6 | « aucun générateur classique ne dépasse 0,15 % (Twin) » | **borné** + **arrondi franchi corrigé** | `audit-comparateur-conditionne-2026-09-13.md` §2, §5 | `c7-controle-generateur.csv`, `meilleur_classique_top1` = **0,0015354713** = **0,1535 %** ; à entrée individuelle égale, **0,4543 %** [0,1992 ; 0,7581] (`c7-audit-comparateur-conditionne.csv`, K2a) |
| 7 | « la fidélité est la fuite » / « fuite = ce qu'implique l'exactitude » | **borné à Twin** — sur GSS le CSV **inverse** le verdict | `c7-controle-generateur.csv`, lignes `table = verdict` | Twin `lecture_memorisation` = « SE COMPORTE COMME UN COPIEUR » (eps* 0,714076 vs 0,719728) ; **Stanford = « GENERALISE : fuit MOINS qu'un copieur de meme exactitude »** (0,735202 vs 0,569910) |
| 8 | contraste 2023 → aujourd'hui à items appariés = **8,9×** | **borné**, et toute publication chiffrée interdite | `c7-residu-trajectoire-resultats.md` §9, §10 | 8,878207 (`c7-temoins-relecture.csv`, `contraste_twin_sur_argyle`) ; à information effective appariée, **2,5293** (`c7-residu-trajectoire.csv`, M2, `rapport jumeau/demo`), dénominateur non estimable |
| 9 | « la dégénérescence des ex æquo frappe **exactement** le bout gauche » | **borné** aux items bruts | `c7-residu-trajectoire-resultats.md` §7 | à M2, plage de **facteur 130** sur le bout droit (0,032 % à 4,193 % selon la convention), classe de tête à 11,5 candidats en médiane |
| 10 | nul de marge appariée : « rho moyen **0,974**, bande [0,950 ; 0,993] » | **rétracté** comme chiffre faisant foi | `correction-t1b-2026-09-13.md` | `c7-nul-corrige-marginal.csv`, agrégat `marginal` / `n_replicats = 100`, seule ligne `fait_foi_tableau1 = oui` : **0,9798947065**, p5 **0,9510489510**, p95 **0,9930069930** |
| 11 | consigne D1 : « écrire 0.974 [0.950 ; 0.993] au tableau 1 » | **borné** (le défaut tient, le chiffre prescrit est périmé) | `correction-t1b-2026-09-13.md` | idem ligne 10 ; le verdict (b) reste réfuté dans les deux séries (0,9650 sous p95) |
| 12 | « *Statistical comparators stay indistinguishable from noise at both FPRs* » | **réfuté sur Park**, **non rattaché** — voir §5 | `c7-t1a-complements-resultats.md` §1g | sous A-LLR sur Park : **85,17 %** top-1 monde fermé et **29,09 %** de TPR à 1 % de FPR, contre 2,24 % et 0,00 % sous l'attaque naïve. Sur Twin la phrase tient (0,0000 % et 0,0486 %). |

---

## 3. Les formulations désormais interdites, et le rapport qui les interdit

C'est la liste opposable. Chaque ligne nomme **qui** interdit, pour que l'interdiction ne
repose sur personne d'anonyme.

| # | formulation interdite | interdite par | à écrire à la place |
|---|---|---|---|
| I1 | les mots **« banals »** ou **« ordinaires »** pour désigner les 45 (ou 40) items | `audit-items-banals-2026-09-13.md` §8 | « items à deux modalités », « items binaires » |
| I2 | **« 30,25 % sur 45 items »** cité sans le balayage complet et sans sa baseline | idem | le pic à k = 40 avec sa baseline : 36,4 % contre 25,2 %, baseline 5,07 % contre 2,09 % |
| I3 | toute phrase du type **« une base commerciale ordinaire suffit »** | idem | rien : ce qui est testé est une propriété du questionnaire Twin |
| I4 | toute lecture du résultat D4 comme une **aggravation** de la menace | idem | le multiplicateur imputable au jumeau **baisse** sur les items binaires |
| I5 | la phrase **« la fuite suit la prédictibilité, non la rareté »** | `audit-predictibilite-2026-09-13.md` §8 | la formulation in extenso du §8 de l'audit ; et **ne jamais écrire que l'affirmation est retirée** |
| I6 | **« aucun générateur synthétique classique ajusté sur les mêmes répondants »** sans qualifier le **conditionnement** | `audit-comparateur-conditionne-2026-09-13.md` §5 | la phrase du §5 de l'audit (entrée strictement égale, 0,45 % contre 20,7 %, Demographics Only à 2,15 %) |
| I7 | **« la fidélité est la fuite »**, « fuite = ce qu'implique son exactitude », « ce n'est pas une mémorisation propre aux LLM » — **sans** la restriction à Twin et **sans** le contre-exemple GSS | `c7-controle-generateur.csv` (colonne `lecture_memorisation`) et `c7-controle-generateur-resultats.md` §0 | la même phrase, bornée à Twin-2K-500, avec le verdict GSS inverse énoncé |
| I8 | **tout facteur chiffré** entre les deux époques : « 150× », « 15× », « 10× », « 8,9× », **et y compris « 2,5× »** | `c7-residu-trajectoire-resultats.md` §10 | une **direction, pas une amplitude** : la formulation in extenso du §10 |
| I9 | présenter la dégénérescence des ex æquo comme **asymétrique** entre les deux bouts | `c7-residu-trajectoire-resultats.md` §7 | à information appariée, les deux bouts en dépendent ; publier le rapport à la baseline, pas le taux nu |
| I10 | **« 0.974 [0.950 ; 0.993] »** comme témoin faisant foi (manuscrit, résumé, tableau 1, légende de la figure 2, lettre de divulgation) | `correction-t1b-2026-09-13.md` | **0,980 [0,951 ; 0,993]**, n = 100, la série du préenregistrement |
| I11 | **« ne dépasse 0,15 % »** pour le plafond des générateurs classiques sur Twin | ce document, §4 | **0,1535 %**, valeur du CSV — ou « 0,16 % », borne que le §1 du même rapport écrivait déjà juste |
| I12 | *(rappel, déjà en vigueur)* toute revendication de supériorité de D4 sur la confidentialité différentielle | `audit-comparaison-dp-2026-09-13.md`, via `retractation-dp-d4-2026-09-13.md` | rien : aucune supériorité n'est revendiquée, dans aucun sens |

---

## 4. Les arrondis favorables trouvés, et ce qui a été rétabli

Méthode : chaque énoncé de forme « ne dépasse X / au plus X / moins de X / plafonne à X /
reste sous X » des rapports de la nuit a été confronté à la valeur du CSV qui le porte, puis
chaque phrase explicitement **destinée au manuscrit** a été relue nombre par nombre.

### 4.1 La borne franchie — corrigée

**`c7-controle-generateur-resultats.md` §3**, dans la phrase explicitement destinée au
manuscrit : « ne depasse **0,15 %** (Twin-2K-500) ». Le CSV porte **0,0015354713**, soit
**0,1535 %** (`c7-controle-generateur.csv`, ligne `Twin` / `table = verdict`, colonne
`meilleur_classique_top1`). **La borne annoncée était franchie**, et l'arrondi allait dans le
sens qui nous arrange. Rétabli : **0,1535 %**. Dans la même phrase, « 2,3 % (Park et al.) »
devient **2,27 %** (`meilleur_classique_top1` Stanford = 0,0226616).

Le défaut était **local à la phrase du manuscrit** : le §1 du même rapport écrivait « 0,16 % »
(juste) et le §2 « 0,154 % » (juste). C'est la phrase la plus lue qui était la seule fausse.

### 4.2 Le même arrondi, propagé — corrigé

**`audit-comparateur-conditionne-2026-09-13.md`** reprend le 0,15 % de la branche auditée.
Deux occurrences sont des **assertions** et sont corrigées en **0,1535 %** : la ligne
« *(rappel)* G1 marginales par segment » du tableau du §2, et la phrase « passe de 0,15 %
(segment) à 0,45 % ». Trois occurrences sont des **citations** — le mandat, le blockquote de
l'affirmation auditée au §0.1, et la prédiction préenregistrée P2 — et sont **laissées
intactes** : on ne corrige pas après coup un préenregistrement ni la citation d'un énoncé
qu'on est en train de réfuter. Une ligne `correction_posterieure:` le dit dans l'en-tête.

### 4.3 Un arrondi d'arrondi — corrigé

**`audit-comparateur-conditionne-2026-09-13.md` §2** : « 2,15 %, soit **4,8 fois** le meilleur
générateur classique nourri de la persona complète ». Le rapport exact vaut
0,021452866861 / 0,004543245870 = **4,72** (`c7-audit-comparateur-conditionne.csv`, lignes
`LLM Demographics Only` et `K2a`, `bloc_items = tous`). Le 4,8 vient d'une division de deux
valeurs **déjà arrondies** (2,15 / 0,45). Rétabli : **4,7 fois**. La phrase destinée au
manuscrit, qui dit « près de cinq fois », survit sans changement.

### 4.4 Ce qui a été vérifié et se révèle juste

Pour que la liste ci-dessus soit lisible comme une liste **complète** et non comme un
échantillon : ont été recalculés depuis les CSV et se révèlent correctement arrondis —
« plafonne à 0,154 % » et « ne depasse 0,16 % » et « ne depasse 0,055 % » en monde ouvert
(0,05475 %) et « 135 fois » / « 29 fois » et « facteur 67 et 14 » (`c7-controle-generateur`) ;
tout le §7 de `c7-equite-risque-resultats.md`, y compris « au plus 1,36 » (valeur exacte
1,35971, `c7-equite-risque.csv`, ethnicité) et « rapport exposés/reste 2,54 → 2,59 » et
« 79,8 % » et « Gini 0,816 [0,799 ; 0,832] » ; toute la formulation du §8 de
`audit-items-banals` (36,4 / 25,2 / 31,5 / 23,3 / ×9,9 / ×6,0 / ×28 / ×7,8) ; « ne dépasse
jamais 17 % du plafond humain » (16,66 % à M2) et le §10 de `c7-residu-trajectoire` ; « 8,9× »
(8,878207), « 4,26 » et « 1,79 » de `c7-temoins-relecture`.

**Une réserve, qui n'est pas un arrondi.** `c7-residu-trajectoire-resultats.md` §9 appelle
2,5× une « borne haute honnête », alors que 2,5293 est une **estimation ponctuelle** dont l'IC
monte à 3,14. Le rapport s'auto-neutralise en interdisant de publier le moindre facteur, y
compris celui-là (I8) ; aucune correction n'est donc posée, mais la lecture est signalée.

---

## 5. Les deux nuances qui avaient été déformées, et l'affirmation non rattachée

**Nuance 1 — la prédictibilité n'est pas « retirée ».** L'audit conclut, mot pour mot :
« l'affirmation ne doit pas être retirée, elle doit être **affaiblie et renommée** ». La moitié
« rareté » **tient**, et elle tient au test le plus dangereux : sous A-LLR **pondéré par la
rareté** — l'attaquant construit pour exploiter la rareté — le signe négatif ne s'inverse pas
(−0,185 [−0,228 ; −0,138]) et se **renforce** sur la rareté moyenne (−0,237 [−0,275 ; −0,198]).
Ce qui tombe, c'est l'**opposition** prédictibilité / rareté, mal posée : les deux sont
colinéaires (ρ = −0,702). Le marqueur posé au §0 bis de `c7-equite-risque-resultats.md` dit
cela et rien d'autre, et dit explicitement qu'une note présentant l'affirmation comme retirée
est fausse.

**Nuance 2 — « la fidélité est la fuite » n'est établi que sur Twin.** Le §2 de
`c7-controle-generateur-resultats.md` le disait déjà (« GSS, resultat different et il faut le
dire ») ; la **phrase destinée au manuscrit**, au §3, ne le disait pas et généralisait depuis
le seul Twin. Le CSV inverse le verdict sur GSS : `lecture_memorisation` = « GENERALISE : fuit
MOINS qu'un copieur de meme exactitude » (eps*_fuite 0,735202 contre eps*_exactitude 0,569910,
là où Twin donne 0,714076 contre 0,719728). Le fait tient sur **un** jeu, pas sur deux. Bornage
posé au §0 du rapport, interdiction I7.

**Affirmation de la nuit que je n'ai PAS su rattacher à un fichier faisant foi.** La ligne 12
de la table : « *Statistical comparators stay indistinguishable from noise at both FPRs* ».
`c7-t1a-complements-resultats.md` §1g la réfute sur Park et la marque lui-même d'une
« ⚠ REMONTÉE AU RESPONSABLE », mais **le seul endroit du dépôt où cette phrase est publiée est
`article/manuscrit.md` §5.3**, que je n'ai pas le droit d'ouvrir ni de modifier. Elle reste
donc sans marqueur canonique, par construction. C'est le seul trou que je laisse, et il est
nommé ici pour que le relecteur de fusion le voie. Il appartient à l'agent propriétaire du
manuscrit.

---

## 6. La porte qui aurait bloqué ça — proposée, NON implémentée

### 6.1 En quoi elle consisterait

**P5 — porte des formulations interdites.** Un contrôle qui refuse qu'un fichier de sortie
publie une formulation figurant dans une **liste d'interdits déclarée**.

- **Déclaration.** Un fichier unique — `resultats/interdits.csv` — à trois colonnes :
  `motif` (la chaîne interdite, littérale), `interdit_par` (le rapport qui l'interdit),
  `remplacement` (le renvoi vers la formulation à écrire). Rien n'est inféré : une
  interdiction se **déclare**, exactement comme une rétractation se déclare.
- **Portée.** Le diff seulement (`--depuis origin/master`), sur les fichiers **ajoutés ou
  modifiés** de `resultats/` et `article/`. Jamais sur l'arbre entier : le dépôt contient
  321 rapports historiques qui contiennent légitimement les formulations d'avant leur propre
  correction.
- **Verdict.** Une ligne ajoutée qui contient un `motif` fait échouer la porte, en nommant
  `interdit_par` et `remplacement`. Les lignes **supprimées** ne sont jamais examinées :
  retirer une formulation interdite est précisément ce qu'on veut encourager.
- **Échappement explicite**, indispensable : une ligne indentée de quatre espaces, encadrée de
  backticks, ou marquée `CITATION:` en colonne 0 est ignorée. Sans cela, ce document-ci et
  chacun des rapports d'audit seraient bloqués par leur propre contenu — ils **citent** tous
  les formulations qu'ils interdisent.
- **Fondement.** Le §8 de chaque audit (« la formulation exacte que l'article doit employer »)
  fournit déjà, mot pour mot, la matière de `interdit_par` et de `remplacement`. Les
  douze lignes du §3 ci-dessus sont le contenu initial du CSV.

### 6.2 Pourquoi elle est dangereuse, et pourquoi je ne l'implémente pas

**Parce qu'elle cherche des motifs de prose, et que ce projet a déjà payé ce prix.** La porte
P4 a fait exactement cela jusqu'au 12/09 — un mot d'invalidation et un nom de fichier à
proximité — et a produit **quatre faux positifs en une seule journée** : un renvoi §N attribué
au mauvais fichier, un identifiant de registre CSV pris pour une déclaration, un mot et un nom
de fichier distants de 360 caractères dans un même paragraphe, et la phrase « ils ne sont pas
invalides », lue comme une invalidation faute de savoir lire une négation. Le raffinement du
vocabulaire n'a pas pu fermer cette classe d'erreurs ; l'inférence a dû être remplacée par une
**déclaration** (`gabarits/entete.md`, et l'en-tête de `outils/portes/entetes.py`).

La porte P5 ramène exactement le défaut qui a été chassé, et sous une forme **pire** :

1. **La négation reste illisible.** « Nous n'écrivons plus “items banals” » contient « items
   banals ». « Il ne s'agit pas d'une base commerciale ordinaire » contient la formulation I3.
   Une porte qui cherche des sous-chaînes bloque la phrase qui **respecte** l'interdiction.
   C'est mot pour mot le quatrième faux positif du 12/09, rejoué.
2. **Les mots interdits sont des mots ordinaires.** « banals », « ordinaires », « 0,15 % »,
   « 10× » apparaissent dans des contextes sans rapport — une légende, une citation
   bibliographique, un paramètre de script, un chiffre d'un autre jeu qui vaut réellement
   0,15 %. Un motif littéral n'a aucun moyen de distinguer l'usage de la mention.
3. **L'échappement est une porte dérobée.** Toute règle d'échappement assez large pour laisser
   passer les audits (qui citent tous ce qu'ils interdisent) est assez large pour laisser
   passer une vraie violation : il suffit d'entourer la phrase de backticks. La porte devient
   alors une formalité, et une formalité qu'on croit protectrice est **pire que rien**.
4. **Une porte à faux positifs se désarme d'elle-même.** Quatre PR bloquées à tort ont suffi,
   le 12/09, pour qu'on retire l'inférence de P4. Une P5 bruyante serait passée en
   `--mode avertissement` en une semaine, et personne ne lirait plus ses notes.

**Ce que je recommande à la place**, dans l'ordre de sûreté décroissante :

- **(a) Étendre la déclaration, pas l'inférence.** La vraie leçon de la nuit n'est pas qu'il
  manquait une porte de prose, c'est qu'il manquait un **marqueur** là où il y avait une
  rétractation. Ajouter à P4 la reconnaissance de `AMENDE:` et `BORNE:` comme marqueurs
  canoniques, sur le modèle exact de `RETRACTE:` — ligne entière, colonne 0, un fichier,
  obligation de poser `amende_par:`/`borne_par:` + `fait_foi:` **dans le même commit**. Aucune
  prose n'est lue ; le faux positif reste impossible ; et l'oubli d'aujourd'hui devient
  bloquant demain.
- **(b) Une porte de **cohérence chiffre-CSV**, qui aurait attrapé le 0,15 %.** Pour toute
  valeur d'un rapport annotée d'un renvoi `⟨csv, ligne, colonne⟩`, vérifier que l'arrondi
  publié est l'arrondi correct de la valeur lue. C'est mécanique, sans prose, sans faux
  positif possible, et c'est le défaut réel qu'on vient de trouver deux fois.
- **(c) Garder P5, mais jamais bloquante.** Sur le modèle de `--indice-prose` : des **notes** à
  l'usage du relecteur humain qui prépare la fusion, produites contre la liste du §3. Une
  détection large et bruyante est utile à un humain qui décide ; elle ne doit jamais rendre de
  verdict.

C'est (a) et (b) qui valent d'être écrites. (c) est un confort. P5 bloquante ne doit pas
exister, et ce document est le registre qu'elle aurait dû remplacer — relu par une personne,
pas par une expression régulière.
