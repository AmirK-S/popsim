# R7 — revue adverse indépendante des résultats

> **Erratum de suivi du 10 septembre 2026.** Les encadrés demandés ont été ajoutés à
> `r7-resultats.md` et `r7-evaluation.md`. Le classement exploratoire traite désormais les
> extrema non uniques dans une catégorie explicite « Ex æquo »; seul
> `r7-analyse-fine-classements.csv` a été régénéré. Aucun chiffre confirmatoire n'a changé.

## Verdict

Les calculs confirmatoires sont **reproductibles et conformes au plan** : les quatre traces
brutes régénèrent à l'identique les mesures R1, les 25 tests F1–F5, les IC, les p, Holm, les
masques et les contrôles publiés. Les verdicts mécaniques H1–H4 sont tous négatifs. Deux
corrections éditoriales sont requises avant publication : remplacer « fausse » par
« critère préenregistré non satisfait » et lever l'ambiguïté de la phrase H4 dans le rapport
mécanique. L'analyse fine est correctement post hoc, mais ses classements minimum/maximum
ne sont pas interprétables sans traitement explicite des ex æquo.

Audit exécuté hors ligne le 10 septembre 2026, sans modèle, GPU ou réseau. Aucun rapport
source ni aucune trace n'a été modifié.

## Reproduction depuis les traces brutes

Les mesures R1 ont été reconstruites dans un dossier temporaire directement depuis :

- `data/traces/r1-olmo3base-r7.jsonl`;
- `data/traces/r1-olmo3sft-r7.jsonl`;
- `data/traces/r1-olmo3dpo-r7.jsonl`;
- `data/traces/r1-olmo3rlvr-r7.jsonl`.

Les fichiers régénérés `r1-par-cellule-r7.csv`, `r1-par-item-ecarts-r7.csv`,
`r1-identite-r7.csv`, `r7-contrastes.csv`, `r7-hypotheses.csv`, `r7-controles.csv` et
`r7-evaluation.md` sont octet pour octet identiques aux fichiers publiés. Le SHA-256 de
`r7-contrastes.csv` est
`3e1059f9a5d8deebb2b043373dcff0b594813ff3bb90f6e2495b56837e9efe61`.
La suite `test_r7_evaluer.py` passe ses 11 tests. L'évaluateur réel construit bien les
**25 tests prescrits**, tous `EXECUTE`, sans test partiel ou refusé.

## Familles, masques et Holm

| famille | tests | effectifs valides |
|---|---:|---|
| F1, journaliste voisin | 3 | 75, 74, 74 |
| F2, journaliste non voisin | 3 | 74, 76, 73 |
| F3, facteur contre 1 | 4 | 78, 76, 76, 75 |
| F4, adversaire voisin | 3 | 77, 76, 77 |
| F5, dispersion par camp | 12 | 143, 146, 143, 141, 140, 140, 138, 136, 137, 139, 138, 134 |

Ces effectifs sont exactement les intersections d'items valides requises. Un rejet dans
l'une des deux conditions retire l'item des deux côtés du contraste. Les éventuelles
recopies K≥3 auraient été retirées après validation de la réponse et avant construction des
masques; aucune n'est observée. Les ratios sont des ratios de moyennes. Les bootstrap
rééchantillonnent les triplets appariés par item, et les permutations changent le signe du
numérateur apparié; le dénominateur humain commun reste fixe, ce qui est algébriquement
équivalent pour ces contrastes.

Une implémentation indépendante de Holm reproduit toutes les valeurs avec un écart maximal
de `5,1e-16`. Les tailles restent 3, 3, 4, 3 et 12; aucune famille n'est réduite après rejet.
Pour F5, le test sur les différences logarithmiques reprend exactement le test H1 de R1,
comme l'impose l'héritage des mesures R1.

## Résultats confirmatoires

- **H1** : aucun contraste voisin ne survit à Holm. SFT−DPO est détecté avant correction
  (`p=0,02260`, IC de SFT−DPO `[-0,406; -0,039]`), mais pas après Holm
  (`p_Holm=0,06780`). Le critère H1 n'est pas satisfait.
- **H2** : Base−Final vaut `−0,0768`, IC `[-0,3008; 0,1603]`,
  `p_Holm=0,5280`. Le signe ponctuel est opposé à Base>Final et le critère n'est pas
  satisfait.
- **H3** : Base−SFT vaut `+0,0563`, mais la plus grande marche voisine en valeur absolue est
  SFT−DPO (`0,2335`). Le critère n'est pas satisfait.
- **H4** : SFT−DPO et SFT−Final ont tous deux le signe prévu (`−0,2335` et `−0,1188`), mais
  leurs p de Holm sont `0,0678` et `0,4750`; la conjonction n'est pas satisfaite.

Les quatre F3 sont sous 1 après Holm. En F4, Base−SFT chez l'adversaire est le seul contraste
voisin significatif (`−0,3839`, IC `[-0,6609; -0,1150]`, `p_Holm=0,0267`). Neuf des douze
F5 survivent à Holm; les exceptions publiées sont exactes.

## Rejets et critères de chute

Les traces comptent exactement 894 cellules chacune. Les rejets sont 30, 57, 61 et 68,
soit 3,36 %, 6,38 %, 6,82 % et 7,61 %. Les sondes des 60 premières cellules comptent 4, 2,
4 et 4 rejets. Aucun seuil de 25 % ou de 50 % n'est approché; aucune recopie K≥3 n'est
présente. Les parts constantes gauche–droite sont 23,4 %, 26,7 %, 13,3 % et 21,3 %, sous
90 %. Le plancher humain vaut 1,008930 et le rho F/rejets vaut 0,600 en valeur absolue. Les
contrôles n'imposent donc aucun masque ou refus supplémentaire.

## Puissance et portée des résultats négatifs

Aucune analyse de puissance, taille d'effet minimale détectable ou hypothèse de variance
n'a été préenregistrée ou publiée pour R7. Il n'existe donc pas de valeur de puissance à
« reproduire » sans ajouter une analyse post hoc. Les six IC F1/F2 ont des largeurs comprises
entre 0,310 et 0,484 en unités de facteur; ils restent compatibles avec des effets
substantiels dans plusieurs directions. Les verdicts négatifs signifient que les critères
préenregistrés ne sont pas satisfaits. Ils ne démontrent ni équivalence ni absence d'effet.

Dans `r7-resultats.md`, remplacer les quatre occurrences de verdict **« fausse »** par
**« critère préenregistré non satisfait »**. Le texte explicatif peut conserver les signes,
IC et p qui justifient chaque décision. Dans `r7-evaluation.md`, remplacer :

> les deux survivant à Holm

par :

> les deux devant survivre à Holm pour satisfaire H4

La formulation actuelle peut être lue comme l'affirmation erronée que les deux tests ont
survécu, alors que le tableau montre le contraire.

## Analyse fine exploratoire

Les quatre CSV de `r7-analyse-fine*` ont été régénérés dans un dossier temporaire et sont
octet pour octet identiques. Le script est explicitement intitulé « analyse descriptive
post hoc », ne calcule aucun nouveau p et ne modifie aucune famille confirmatoire. Les
comparaisons avec R4/R5 utilisent une intersection commune de 58 items stricts et doivent
rester présentées comme comparaisons exploratoires entre expériences et formats distincts.

Le tableau de classements emploie toutefois `idxmin` et `idxmax`. Pandas attribue alors tout
ex æquo au premier checkpoint dans l'ordre Base, SFT, DPO, Final. Les données comportent :

| identité | items complets | ex æquo au minimum | ex æquo au maximum |
|---|---:|---:|---:|
| journaliste | 72 | 13 | 12 |
| adversaire | 76 | 10 | 16 |

Les proportions publiées de checkpoint « minimum » ou « maximum » favorisent donc les
checkpoints placés tôt, particulièrement Base. Avant toute interprétation de ces colonnes,
il faut soit publier une catégorie « ex æquo », soit partager chaque item entre ses extrema,
soit exclure les ex æquo avec le dénominateur correspondant. Les tertiles de consensus
emploient également `rank(method="first")`; les égalités proches des coupures sont réparties
selon l'ordre des lignes et cette convention doit être indiquée. Ces deux points sont
exploratoires et ne changent aucun résultat H1–H4.

## Séparation finale

**Confirmatoire enregistré :** 25 tests F1–F5, Holm séparé, quatre verdicts mécaniques,
contrôles de rejet/sonde/recopie/constance, plancher humain et diagnostic F/rejets.

**Secondaire enregistré :** F3, F4, F5 et les tableaux R1 annoncés, sans promotion vers les
hypothèses de trajectoire.

**Exploratoire post hoc :** strates, classements, trajectoires par item, comparaison aux
effets de format R4/R5 et figure `r7-analyse-fine`. Ces sorties peuvent être publiées si
leur statut post hoc et les règles d'ex æquo sont visibles.
