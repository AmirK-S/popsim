# R7 - résultats descriptifs des checkpoints Olmo 3

> **Erratum du 10 septembre 2026.** Dans le tableau ci-dessous, les quatre verdicts
> « fausse » se lisent « critère préenregistré non satisfait ». Aucun calcul de puissance
> ou d'équivalence n'a été préenregistré : un critère non satisfait ne démontre donc ni
> l'absence d'effet ni l'équivalence. H4 exige conjointement `SFT-DPO < 0` dans F1 et
> `SFT-Final < 0` dans F2, avec survie de chacun à Holm dans sa famille; les signes observés
> sont conformes, mais les p de Holm 0,0678 et 0,4750 ne satisfont pas cette exigence.

## Portée et exécution

Les quatre traces contiennent 894 cellules chacune, soit 3 576 sur 3 576. L'évaluation a
réutilisé les mesures R1, puis exécuté les 25 tests enregistrés: F1=3, F2=3, F3=4, F4=3 et
F5=12. Aucun test n'est partiel ou refusé. Les IC emploient 2 000 tirages bootstrap par
item et les p 20 000 permutations de signe, avec Holm séparé dans chaque famille.

Ces résultats décrivent quatre checkpoints publiés sous une invite commune. Le lineage
direct n'étant pas établi, aucune différence n'est attribuée causalement à SFT, DPO ou à
l'étape finale.

## Quantité principale et hypothèses

Sur leur périmètre valide propre parmi les 79 items orientés, les facteurs F du demandeur
journaliste sont: Base **0,455** (78 items), SFT **0,415** (76), DPO **0,630** (76) et Final
**0,526** (75). Ces quatre ratios sont significativement sous 1 dans F3 après Holm. Cette
comparaison à 1 est secondaire; elle ne valide aucune des quatre hypothèses de trajectoire.

| hypothèse préenregistrée | test décisif | résultat | verdict |
|---|---|---|---|
| H1, au moins un contraste voisin | trois tests F1 | aucun p de Holm sous 0,05 | **fausse** |
| H2, Final sous Base | Base-Final = -0,077, IC [-0,301; 0,160], p Holm 0,5280 | le signe observé est opposé et non significatif | **fausse** |
| H3, plus grande marche à Base-SFT | Base-SFT = +0,056, IC [-0,145; 0,246], p Holm 0,5871 | ce n'est ni significatif ni le plus grand contraste voisin | **fausse** |
| H4, minimum à SFT puis remontée | SFT-DPO = -0,234, p Holm 0,0678; SFT-Final = -0,119, p Holm 0,4750 | les deux signes vont dans le sens prévu, mais aucun des deux tests ne survit à Holm | **fausse** |

La trajectoire descriptive n'étaye donc pas le pari conjoint annoncé. Elle ne montre pas
non plus une trajectoire voisine significative dans F1. Chez le demandeur adversaire, la
réplication F4 donne Base-SFT = -0,384, IC [-0,661; -0,115], p Holm 0,0267, soit une
différence détectée dans le sens inverse de la petite différence principale journaliste.
Les deux autres contrastes F4 ne survivent pas à Holm. Cette divergence entre identités
reste une observation secondaire.

## Contrôles préenregistrés

- Rejets: Base 30/894 (3,36 %), SFT 57/894 (6,38 %), DPO 61/894 (6,82 %) et Final 68/894
  (7,61 %), tous sous le seuil de 25 %. Les sondes des 60 premières cellules comptent
  respectivement 4, 2, 4 et 4 rejets, toutes sous 50 %.
- Aucune recopie de l'exemple pour K supérieur ou égal à 3 n'est détectée.
- La part de distributions constantes entre camps varie de 13,3 % à 26,7 %, sous le seuil
  de 90 %.
- Le plancher humain vaut 1,008930, dans [0,85; 1,15]. Le SHA-256 du référent R1 est conforme.
- La corrélation de rang entre F et le taux de rejet vaut 0,600 en valeur absolue, sous le
  seuil préenregistré de 0,8; le critère d'artefact de conformité ne se déclenche pas.
- La validation indépendante Euler s'est terminée avec code 0: ordre, JSON, doublons,
  effectifs, rejets, empreintes, quantification et tokenisation sont conformes; aucun
  `llama-server` ne restait actif.

## Résultats secondaires

Les ratios F5 de dispersion interne chez le journaliste sont au-dessus de 1 dans les douze
cellules camp-checkpoint. Neuf survivent à Holm; les trois exceptions sont SFT-gauche,
DPO-droite et Final-droite. Ces
ratios décrivent une dispersion produite supérieure à la dispersion réelle dans plusieurs
cellules. Ils ne constituent pas une étape causale et ne changent pas les verdicts H1 à H4.

Les tableaux R1 publient aussi H2b sur les items stricts, H2a non signé, l'identité du
demandeur et les autres diagnostics annoncés. Ils restent secondaires et aucune famille
confirmatoire supplémentaire n'a été créée.

## Écart de terminaison documenté

Le script réel de collecte n'écrit pas littéralement `RUN TERMINE` et le vérificateur garde
le statut `CONTROLES_HORS_LIGNE_OK` plutôt que `TERMINE`. Une première tentative
d'évaluation s'est donc arrêtée sans analyser. Euler a ensuite établi code 0, 4 fois 894
cellules, absence de serveur et validation stricte, puis l'orchestrateur a explicitement
accepté ces preuves comme équivalentes à la garde substantielle. L'évaluation rapportée ici
n'a commencé qu'après ce GO explicite.

## Fichiers produits

- `r7-contrastes.csv`: 25 tests, estimateurs, IC, p bruts et p de Holm;
- `r7-hypotheses.csv`: verdict mécanique H1 à H4;
- `r7-controles.csv`: rejets, recopies, constance des camps, référent et diagnostic de rejet;
- `r7-evaluation.md`: restitution mécanique générée par l'évaluateur;
- sorties `r1-*-r7.csv` et `r1-resume-r7.md`: mesures R1 réutilisées et secondaires.

La suite locale de l'évaluateur passe 11 tests après l'analyse. Aucun seuil, contraste,
périmètre ou famille n'a été changé après observation.
