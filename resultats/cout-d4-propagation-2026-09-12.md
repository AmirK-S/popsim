# Propagation du chiffre « 1,47 » (coût de D4) — audit du 12 septembre 2026

Source faisant autorité : `resultats/c7-defense-resultats.md`, section « Réglage recommandé »
(lignes 24-41 et 59-63). Trois chiffres vérifiés directement dans ce fichier avant toute
correction :

- **4,4 points** sur les seules corrélations (ligne 20, colonne « dont … corr. » de la ligne
  D4 ; répété lignes 26-32, 49-51, 62-63).
- **5,78 → 9,71** sur `erreur_correlations_hum` (jumeau vs humains réels), soit **+68 %** après
  D4 (lignes 34-41, 51, 62-63).
- **1,47** confirmé comme étant la moyenne non pondérée des trois composantes (0,0 / 0,0 / 4,4),
  explicitement qualifiée par la source elle-même de mesure trompeuse du coût (lignes 26-27,
  59-60).

Les trois chiffres se retrouvent tels quels dans la source. Rien n'a été écrit sur la base d'un
chiffre qui ne s'y retrouvait pas.

## Méthode du balayage

Recherche récursive de `1,47` et `1.47` (limites de mot) sur tout le dépôt, puis lecture du
contexte de chaque occurrence pour écarter le bruit numérique sans rapport (valeurs de tableaux
CSV, pourcentages ou coefficients d'autres analyses portant la même suite de chiffres par
coïncidence — ex. `resultats/d4-resultats.md` est une étude différente, sans rapport avec la
défense D4 de C7 ; `resultats/c5-resultats-api.md`, `resultats/t2-qui-bouge-agrege.md`,
`resultats/i3b-abaque-et-borne.md`, `resultats/a6-double-distorsion-hors-gss.md`,
`resultats/a43-r2-demoyenne.md`, `corpus/01-simulation-individus-populations.md` et les fichiers
`.csv` : aucun rapport avec le coût de D4). Une recherche complémentaire sur les formulations
« perte d'utilité globale/moyenne », « coût moyen de la défense », « moyenne des trois
composantes », « indice composite » n'a fait remonter aucun fichier supplémentaire hors de ceux
listés ci-dessous.

## Fichier corrigé (dans le périmètre d'écriture autorisé)

**`resultats/divulgation-responsable-brouillon.md`, ligne 157** (lettre à Twin-2K-500, anglais).

- Avant : « cuts the twin-vs-human rate from 20.7% to 0.13% at a cost of only 1.47 points of
  aggregate utility »
- Après : « cuts the twin-vs-human rate from 20.7% to 0.13%. The real cost falls entirely on
  inter-item correlations (4.4 points); two of the three components (per-item distribution,
  group differences) are exactly preserved by construction, so the previously used three-way
  average (1.47 points) diluted that cost by a factor of three rather than measuring it. »

Aucune autre occurrence de « 1,47 »/« 1.47 » trouvée dans les autres fichiers du périmètre
autorisé (`resultats/positionnement-vie-privee-2026-09-12.md`, `REPRISE-2026-09-12.md`,
`artefact/README.md`) : rien à corriger là.

*Point laissé de côté volontairement* : dans la même lettre (lettre 2, Stanford, ligne ~247),
« at a small utility cost » ne cite aucun chiffre et ne dit pas « moyenne » ni « global » — hors
du périmètre strict de cette tâche (pas de nombre trompeur à remplacer), donc non touché.

## Fichiers interdits en écriture — occurrences et correction proposée

Aucune correction n'est en réalité nécessaire dans les 7 fichiers interdits : les occurrences
trouvées sont déjà conformes à la formulation de référence, ou le fichier ne contient pas le
motif.

- **`article/manuscrit.md`** (lignes 768, 813, 816, 884) et **`resultats/article-synthese.md`**
  (lignes 65-66, 84, 135) : déjà corrigés. Le manuscrit retire explicitement la moyenne
  (« We therefore withdraw the summary that presented D4's cost as a single mean of 1.47
  points », l.768) et précise partout ailleurs « 1.47 is not D4's cost, which falls on a single
  component (§6) » (l.816). `article-synthese.md` porte la même règle et sa propre note de
  correction (l.66). **Aucun remplacement à proposer.**
- **`resultats/preenregistrements-recueil-2026-09-12.md`** (ligne 446) : « 4,4 points sur les
  corrélations, pas 1,47 » — déjà la formulation correcte. **Rien à changer.**
- **`resultats/c7-defense-resultats.md`** (lignes 26, 59) : c'est la source de référence
  elle-même ; elle qualifie déjà 1,47 de moyenne trompeuse. **Rien à changer.**
- **`analyses/c7_reconciliation_facteurs.py`** et **`resultats/reproductibilite-chaine-2026-09-12.md`** :
  aucune occurrence de « 1,47 »/« 1.47 » trouvée. **Rien à signaler.**

### Point de vigilance — un rapport périmé dans le dépôt

`resultats/revue-hostile-gel-2026-09-12.md` (lignes 96-113) accuse le manuscrit d'une violation
(« Le 1,47 point revient deux fois après avoir été retiré », lignes 758/826). **Ce constat est
périmé** : la version actuelle de `article/manuscrit.md` porte déjà la qualification « composite
utility index » et la clause « 1.47 is not D4's cost » aux lignes citées. L'audit plus récent
`resultats/audit-chiffres-2026-09-12.md` (lignes 210-215) confirme : « Aucune violation […] le
1,47 dans la seule comparaison à la DP, A12 ». Ne pas rouvrir cette correction sur la seule foi
de `revue-hostile-gel` — c'est exactement le mode de panne (rapport périmé) décrit dans la
consigne de cette tâche.

## Occurrences hors périmètre d'écriture (ni autorisées ni interdites nommément) — à signaler

Ces fichiers ne figurent dans aucune des deux listes ; je ne les modifie pas mais les liste avec
le remplacement que je proposerais si le responsable me donne (ou se réserve) le droit d'écrire :

- **`resultats/c7-dp-resultats.md`, ligne 15** : « perte = 1,47 pt (`c7-defense-courbe.csv`) »
  — utilisé pour comparer D4 à la DP dans le même document. **Voir section suivante (usage
  DP) : ne pas corriger d'office.** Si correction souhaitée malgré tout : ajouter la
  qualification, par ex. « perte = 1,47 pt sur l'indice composite d'utilité (moyenne non
  pondérée des trois composantes, seule base commensurable avec la DP ; le coût réel de D4 est
  de 4,4 pts, sur les seules corrélations) ».
- **`resultats/c7-dp-preenregistrement.md`, ligne 23** : « Aucun epsilon n'atteint une utilite a
  moins de 5 points de D4 (1,47) » — préenregistrement, usage DP également. Même traitement que
  ci-dessus si correction souhaitée.
- **`analyses/c7_multiplicite_globale.py`, lignes 377-379** : `ecart_min = (dp_finite.utilite_globale - 1.47).min()`
  — constante numérique utilisée pour comparer à `utilite_globale` (l'indice composite), donc
  usage DP légitime au même titre. Pas de remplacement proposé : c'est du code de comparaison,
  pas une formulation de coût.
- **`article/latex/main.tex`, lignes 353, 369, 417** : miroir exact de `article/manuscrit.md` —
  déjà correctement qualifié (« composite utility index », « 1.47 is not D4's cost »). Rien à
  proposer.
- **`resultats/revue-popets-simulee-2026-09-12.md`, ligne 10** et **`resultats/audit-chiffres-2026-09-12.md`,
  lignes 210 et 215** : documents d'audit qui identifient déjà le problème correctement
  (« Le chiffre honnête est 4,4 points sur les corrélations » ; « le 1,47 dans la seule
  comparaison à la DP »). Ce sont des constats déjà exacts, pas des erreurs à corriger.
- **`resultats/revue-hostile-gel-2026-09-12.md`** et **`resultats/revue-hostile-finale-2026-09-12.md`** :
  documents de relecture hostile qui citent le texte du manuscrit tel qu'il était au moment de
  la relecture, à titre de preuve. Ce sont des procès-verbaux historiques ; les modifier
  falsifierait le compte-rendu de la relecture. Aucun remplacement proposé — voir le point de
  vigilance ci-dessus sur leur caractère périmé.

## Passages où 1,47 sert explicitement à comparer avec la confidentialité différentielle (à trancher par le responsable, non corrigés d'office)

Conformément à la consigne : ces passages nomment 1,47 comme l'unique échelle commensurable
avec la perte d'utilité de la DP (mesurée sur ce même indice composite). Je ne les ai pas
corrigés.

1. `article/manuscrit.md` (l.813, 816, 884) et `article/latex/main.tex` (l.353, 369, 417) :
   « composite utility index […] within 5 points of D4's 1.47 on that same index […] 1.47 is
   not D4's cost, which falls on a single component (§6) ». Déjà nommé et qualifié comme demandé
   par la nuance du 12/09 — pas d'action nécessaire, juste signalé.
2. `resultats/article-synthese.md` (l.84) : « la perte d'utilité (3,33 et 3,38 pts) est à moins
   de 5 pts de D4 (1,47 pt) sur l'indice composite d'utilité (…) — seule forme sous laquelle la
   comparaison à la DP est possible ». Déjà qualifié.
3. `resultats/c7-dp-resultats.md` (l.15) et `resultats/c7-dp-preenregistrement.md` (l.23) :
   usage DP mais **sans** la qualification explicite « indice composite » présente dans les deux
   documents ci-dessus — c'est la seule zone où le nom manque encore. Signalé pour décision (pas
   dans le périmètre d'écriture de cette tâche).
4. `analyses/c7_multiplicite_globale.py` (l.377-379) : usage DP en code, littéral `1.47` comparé
   à `utilite_globale`.
