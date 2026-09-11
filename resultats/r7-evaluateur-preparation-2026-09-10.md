# R7 — préparation de l'évaluateur, 10 septembre 2026

**Statut : prêt pour revue, sans exécution expérimentale R7.** Aucun modèle, GPU, réseau,
paiement ou publication n'a été utilisé.

`analyses/r7_evaluer.py` applique la définition corrigée du plan compact : `F` est un ratio
de moyennes. Un contraste A−B vaut `mean(d_A - d_B) / mean(r)` sur les items valides dans
les deux conditions. La permutation bilatérale porte sur `d_A - d_B` par item et le
bootstrap rééchantillonne les triplets appariés. Aucun ratio par item n'est calculé.

Les 25 tests prescrits sont construits avec leurs tailles fixes : F1=3, F2=3, F3=4,
F4=3, F5=12. Les orientations suivent le plan compact. H4 exige `SFT−DPO < 0` dans F1 et
`SFT−Final < 0` dans F2, avec les deux p de Holm sous 0,05. Les familles de Holm restent
séparées ; un test refusé garde sa place avec p=1. La bande [0,95 ; 1,05] ne s'applique
qu'aux ratios comparés à 1.

L'évaluateur réutilise les mesures élémentaires et fonctions statistiques de
`r1_evaluer.py`. Il exclut en plus les recopies R7 pour K>=3, conserve [43, 57] pour K=2,
apparie chaque contraste sur l'intersection des items, marque les calculs incomplets
`PARTIEL` et refuse ceux qui ont moins de trois items, un référent divergent ou un critère
de chute applicable. Les sorties portent toutes la mention
`DESCRIPTIVE checkpoints publiés; aucune causalité d'étape`.

Vérifications exécutées hors GPU :

- 8 tests de `test_r7_evaluer.py` réussis : estimateur, orientations F1/F2, tailles F1–F5,
  H4, périmètre commun, refus, recopie K>=3/K2 et compatibilité des tableaux historiques R4 ;
- contrôle numérique historique : le calcul retrouve exactement le contraste R4
  `q4base−q4nogab = −0,161004` déjà enregistré ;
- 17 tests factices de `test_r7_checkpoints.py` réussis ;
- essai de l'évaluateur sur un dossier vide : quatre sorties lisibles, 25 refus explicites,
  aucune interprétation.

Après une éventuelle collecte R7, l'ordre exécutable est :

```sh
.venv/bin/python -B analyses/r1_evaluer.py --suffixe r7 --sans-figure
.venv/bin/python -B analyses/r7_evaluer.py
```

Aucune modification supplémentaire du plan statistique n'est nécessaire après la
correction Avicenna. Il reste à faire relire le code et les tests, puis seulement à les
exécuter sur des traces R7 si une collecte distincte est décidée.
