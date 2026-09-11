# R7 - préflight hors ligne de l'évaluateur

## Statut

Préflight réalisé sans modèle, GPU, réseau ni analyse de la trace Final en cours. Le plan
et ses seuils n'ont pas été modifiés. Les traces Base, SFT et DPO, chacune complète à 894
lignes, ont servi uniquement à vérifier le schéma, l'ordre, la configuration, les sommes
des distributions et la construction des périmètres.

## Matrice figée

| famille | quantité et périmètre | tests | rôle dans H1 à H4 |
|---|---|---:|---|
| F1 | F principal, journaliste, intersection des 79 items orientés | Base-SFT, SFT-DPO, DPO-Final | H1: au moins un test significatif; H3: Base-SFT positif et plus grand en valeur absolue; première branche de H4: SFT-DPO négatif et significatif |
| F2 | F principal, journaliste, même périmètre apparié | Base-Final, Base-DPO, SFT-Final | H2: Base-Final positif et significatif; seconde branche de H4: SFT-Final négatif et significatif |
| F3 | F principal, journaliste, 79 items orientés | quatre checkpoints contre 1 | secondaire, sans nouveau rôle dans H1 à H4 |
| F4 | F principal, demandeur adversaire, intersection des 79 items orientés | les trois voisins de F1 | réplication secondaire |
| F5 | ratio de dispersion interne de R1, journaliste, 149 items par camp | 4 checkpoints par 3 camps contre 1 | secondaire; le nom historique « H1 » de R1 est distinct de H1 de R7 |

Les tailles Holm restent exactement F1=3, F2=3, F3=4, F4=3 et F5=12, soit 25 tests.
Chaque famille est corrigée séparément. Un test inexécutable conserve sa place avec p=1.
La bande [0,95; 1,05] s'applique seulement à F3 et F5.

Le contraste A-B est `(moyenne(d_A)-moyenne(d_B))/moyenne(r)` sur les items communs. Le
bootstrap rééchantillonne les triplets appariés `(d_A,d_B,r)`, 2 000 fois. La permutation
bilatérale change le signe de `d_A-d_B` par item, 20 000 fois, avec correction de
Phipson-Smyth. F3 emploie le test compatible avec le ratio contre 1, `d-r`. F5 réutilise
la méthode R1: ratio des moyennes et permutation des différences logarithmiques finies.

Les sorties secondaires sur les 65 items stricts, H2a et l'erreur TV restent produites par
`r1_evaluer.py`; elles ne sont pas promues dans F1 à F5 par `r7_evaluer.py`.

## Correction démontrée

Avant correction, trois lignes appariées dont deux valeurs de référent étaient NaN
pouvaient laisser un contraste marqué `EXECUTE`. L'IC éliminait ces lignes, tandis que la
permutation pouvait encore employer un autre périmètre. Le même statut erroné était possible
dans F3 et F5 lorsque moins de trois paires numériques subsistaient.

`r7_evaluer.py` construit maintenant explicitement le masque fini commun avant l'IC et la
permutation. Il refuse le test si moins de trois triplets finis restent. Pour la permutation
logarithmique F5, au moins trois paires strictement positives sont aussi exigées. Aucun
estimateur, seuil, contraste ou ordre de famille n'a changé.

Un test factice reproduit le défaut et vérifie les trois refus. Un second test vérifie que
bootstrap, permutations et Holm sont identiques bit à bit avec la même graine. La suite
locale compte 11 tests réussis. Un passage séparé sur Base/SFT/DPO a validé 894 lignes par
condition, les distributions finies normalisées, la matrice de 25 tests et la
reproductibilité, avec Final absent du bac de test.

## Commande finale préparée, non exécutée

À lancer seulement après le marqueur de fin autoritatif du run, 894 lignes Final, statut
global `TERMINE` dans `r7-registre.json`, puis validation Euler:

```sh
grep -q 'RUN TERMINE' data/traces/r7-run.log
test "$(wc -l < data/traces/r1-olmo3rlvr-r7.jsonl)" -eq 894
.venv/bin/python -B -c 'import json; assert json.load(open("data/traces/r7-registre.json"))["statut"] == "TERMINE"'
.venv/bin/python -B analyses/r1_evaluer.py --suffixe r7 --sans-figure
.venv/bin/python -B analyses/r7_evaluer.py
```

Cette commande n'a pas été exécutée pendant ce préflight. Toutes les sorties de
`r7_evaluer.py` conservent la portée `DESCRIPTIVE checkpoints publiés; aucune causalité
d'étape`.
