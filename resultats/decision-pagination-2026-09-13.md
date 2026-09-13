# Décision de pagination — ce que compte réellement la limite de 12 pages de PoPETs, et où le corps atterrit

statut: courant
mandat: Établir depuis l'appel à communications officiel ce que la limite de 12 pages de PoPETs 2027 compte réellement, puis réduire le corps du manuscrit en conséquence sans supprimer une seule affirmation, rétractation, limite ou intervalle de confiance.
agent: Claude Opus 5, Anthropic — sous-agent pagination
ecriture: article/manuscrit.md ; resultats/registre-chiffres.csv (trois lignes passées à `retracte`, §3 du mandat) ; resultats/decision-pagination-2026-09-13.md
lecture_seule: tout le reste
interdits: appel payant, commit sur master, fusion, arrière-plan ; une seule recherche web, autorisée par le mandat pour la question du §1
cecite: je n'ai pas lu les branches d'intégration en cours de fusion ; je n'ai pas touché au titre (décision réservée au responsable) ; la compilation LaTeX de contrôle a été faite dans un répertoire de travail hors dépôt, aucun fichier de `article/latex/` n'a été modifié dans le dépôt
cout_reel_usd: 0.00  <!-- P2-exempt: cout reel lu au grand livre, pas une mesure -->

---

## 1. Ce que la limite compte — réponse établie, source citée

**La limite de 12 pages porte sur le corps seul.** Sont explicitement **hors du décompte** :
les trois sections obligatoires du gabarit 2027 (*ethical considerations*, *open science*,
*AI use*), les remerciements, la bibliographie, et **toute annexe clairement signalée**.

Source, verbatim, page officielle des auteurs PoPETs 2027
(`https://crysp.petsymposium.org/authors-2027.php`, consultée le 13/09/2026) :

> Submissions and resubmissions to PoPETs must consist of at most 12 typeset pages for the main
> body of the paper. The main body excludes the three mandatory sections per the 2027 template
> (ethical considerations, open science, and AI use) as well as any acknowledgements, the
> bibliography, and any clearly-marked appendices contained in the submission.

Trois compléments du même appel, qui changent l'arbitrage :

- **Révision : 13 pages.** « During the interactive revision process, the authors will be allowed
  one additional page for the main body of the paper (13 main-body pages in total) in order to
  address reviewer feedback. »
- **Version finale : 13 pages également**, avec un nombre illimité de pages pour les sections
  obligatoires, les remerciements, la bibliographie et les annexes signalées.
- **Mais la soumission initiale reste à 12**, et l'appel ajoute que l'article doit être
  « complete and self-contained without appendices » : une annexe sert au détail supplémentaire,
  jamais à porter une affirmation du corps.

Ceci tranche la décision **D6** laissée ouverte par `resultats/plan-revision-2026-09-13.md`
(§1072), qui supposait le cas défavorable — annexes comptées. Le cas favorable est le bon.

**Ce que cela ne dissout pas.** Le compte de 12 628 mots annoncé au mandat **excluait déjà**
les §8, §9, §10 et la bibliographie : il vaut titre + résumé + §1 à §7.4. La découverte
n'efface donc pas le dépassement, elle change la **nature du remède** — un déplacement plutôt
qu'une coupe — et elle ouvre une sortie de secours que personne n'avait vue : **13 pages sont
de droit dès la première révision.**

## 2. La contrainte technique qui a décidé du véhicule

`article/latex/md2latex.py` ne régénère que trois zones de `main.tex` : `ABSTRACT`, `BODY`
(§1 à §7) et `BACKMATTER` (§8, §9, §10). **Il n'existe aucune zone « annexe » générée.** Une
section `## Appendix A` écrite dans le manuscrit serait balayée dans `BODY`, donc **comptée dans
les 12 pages** — exactement l'inverse du but. Modifier le convertisseur était hors de mon
périmètre d'écriture.

Le matériel déplacé est donc allé en **Open Science (§9)**, que le convertisseur rend en
`\begin{openscience}`, que l'appel exclut nommément du décompte, et où le dépôt loge déjà ce
genre de matériel (les blocs « Transport failures and retries (§5.7) » et
« Differential-privacy implementation (§6.2) » y étaient avant moi). Le mandat autorisait
explicitement ce véhicule : « déplace en annexe **ou en section Open Science** ».

## 3. Ce qui a été déplacé, et ce qui ne l'a pas été

Onze blocs de détail, tous reproduits **mot pour mot** en Open Science, le corps gardant
l'affirmation et son chiffre de tête :

| corps | ce qui descend en Open Science |
|---|---|
| §4.5 | les comptes et taux des contrôles de provenance sur les trois archives |
| §5.1 | le rééchantillonnage au niveau des configurations, Fisher-z, test de permutation |
| §5.2 | la table des six comparateurs monde fermé, chacun avec son intervalle |
| §5.3 | **le recensement des seuils à FPR = 0,1 %** (défaut R9) |
| §5.4 | témoins leurres, borne démographique, décomposition, items effectifs, bras T2, les deux limites du verdict préenregistré sur la distance entre configurations (réfuté sur ses propres termes, A15, hors tableau) |
| §5.5 | H1, H4, « déviations seules », recouvrement de vocabulaire, kappas de retest |
| §5.7 | le renversement du top-10 sur le bras de granularité |
| §5.8 | **les trois conventions de départage des ex æquo** (geste 4 de R1), robustesse au choix d'items, deux conditions Park, bits du plus proche voisin, et ce qui sépare Park de Twin |
| §5.9 | les six bassins, les deux lois ajustées, la nature des intervalles |
| §6.2, §6.3 | les coûts DP budget par budget, l'erreur propre du jumeau non protégé |
| §7.3 | les p-values ajustées et le recensement complet à 47 tests |

**Rien n'a été supprimé.** Vérification mécanique : chaque littéral numérique présent dans
`article/manuscrit.md` au commit `d712eb4` est encore présent dans le fichier après la passe —
aucune valeur n'a disparu du document. Deux chiffres que la première rédaction avait perdus en
route (le renversement du top-10 à 7,5 % du §5.7, et le couple d'entropies par item 1,30 contre  <!-- P2-exempt: chiffres cites pour documenter ce qui a ete retabli, pas une mesure nouvelle -->
0,99 qui sépare Park de Twin) ont été **rétablis** en Open Science dès que le contrôle les a  <!-- P2-exempt: idem ligne precedente -->
signalés.

**Levier 2 appliqué, sans perdre une ligne.** Le tableau des dix-sept prédictions garde ses
**dix-sept lignes**, ses dix-sept verdicts, ses dix-sept sources et tous ses chiffres ; six
cellules `Outcome` ont été resserrées. La colonne `Source` a été retirée puis **rétablie à
l'identique** : `md2latex.py` code en dur un tableau à quatre colonnes (largeurs `0.02`, `0.27`,
`0.50`, `0.135`), une version à trois colonnes ne se serait pas rendue.

**Ce qui n'a pas été touché, délibérément.** Le résumé (574 mots) : il porte les rétractations
et les limites placées en tête par discipline, et les raccourcir reviendrait à défaire la nuit
d'audits par la porte de service. Le §1.1 (le confondant énoncé avant l'affirmation), le §1.4,
le §7.2 et le §7.4 : c'est l'appareil d'honnêteté du papier, pas du détail. Le titre : décision
réservée au responsable.

## 4. Le résultat, mesuré et non estimé

Le mandat raisonnait en mots (12 628 mots, ≈ 13,2 pages à 955 mots la page). Ce modèle est
approximatif. J'ai préféré **compiler** : copie hors dépôt de `article/`, `references.bib` pris
sur `agent/biblio/anteriorites` pour que `jordon2022synthetic`, `carlini2023quantifying` et
`houssiau2022tapas` se résolvent — le convertisseur confirme *« Toutes les citations du
manuscrit ont ete reliees a une entree de references.bib »* —, puis `md2latex.py` + `pdflatex`.
**Aucun fichier de `article/latex/` du dépôt n'a été modifié.**

| | avant (`d712eb4`) | après |
|---|---|---|
| fin du corps (§7.4) | bas de la colonne **droite** de la page 13 | bas de la colonne **gauche** de la page 13 |
| corps en pages typographiées | **13** | **13** |
| document complet | 17 p. | 17 p. |
| mots du corps | 12 630 | 12 149 |

**La passe a gagné une demi-page pleine — une colonne entière — mais pas le passage à 12.**
Le corps déborde d'une colonne sur la page 13. Pour tenir 12 pages il faudrait retirer encore
une colonne entière, et il n'y reste plus de détail à déplacer : les trois catégories que le
mandat autorisait — identification des seuils, conventions de départage, tableaux de mesures
secondaires — sont épuisées. La colonne suivante se paierait en prose d'argumentation, en
nuances ou en limites. **L'interdit absolu s'applique : je rends 13 pages et je le déclare.**

## 5. Ce que le responsable a à arbitrer

1. **Soumettre à 13 pages** en l'état. Risque réel de renvoi administratif à la soumission
   initiale, mais **13 pages sont de droit dès la première révision** et pour la version
   finale : le corps actuel est déjà conforme au format d'arrivée.
2. **Faire tomber une colonne** en touchant à l'argumentation — ce que j'ai refusé de faire
   seul. Les candidats les moins destructeurs, par ordre : le résumé (574 mots, environ
   240 récupérables), les figures redondantes du §1.3 avec le §5, les légendes des figures 1
   et 2.
3. **Ouvrir une zone annexe dans `md2latex.py`** (hors de mon périmètre). Le gabarit `main.tex`
   porte déjà `\appendix` ; il ne manque que l'aiguillage. C'est le geste le plus rentable du
   lot : il rendrait la limite non contraignante, définitivement.

## 6. Portes et registre

- **P2** `registre_chiffres` sur le manuscrit : **356**, exactement la valeur d'entrée — non
  aggravée. Trois doublons de chiffres en dur introduits par les déplacements ont été retirés
  pour y revenir. Sur le registre seul : **OK, aucune violation**, 61 grandeurs déclarées.
- **P3** `interdits` : **OK**. **P4** `entetes` : **OK**. **P5** `renvois` : **OK**.
- **Registre, §3 du mandat.** Trois lignes passées de `courant` à `retracte`, **aucune
  supprimée**, chacune nommant la référence qui la remplace :
  `temoin-contraste-2023-aujourdhui-items-apparies` (8,9 — tout facteur chiffré inter-époques
  est interdit par I8 ; remplacé par une direction, pas une amplitude) ;
  `park-tpr-fpr01-fort-ouvert` (44,37 — non identifiée par les données, défaut R9 ; remplacée  <!-- P2-exempt: valeur retractee, citee parce que la retracter est l'objet de la phrase -->
  par `park-tpr-fpr1-fort-ouvert`, 60,17 % à FPR = 1 %) ; `twin-tpr-fpr01-fort-ouvert` (1,01 —  <!-- P2-exempt: valeurs retractee et remplacante, citees au titre de la retractation -->
  même défaut ; remplacée par `twin-tpr-fpr1-fort-ouvert`, 4,28 %). Le manuscrit ne citait  <!-- P2-exempt: idem : valeur retractee et sa remplacante -->
  aucune des trois et n'en cite toujours aucune.
