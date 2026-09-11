# R7 - évaluation finale non lancée, garde de terminaison absente

Le 10 septembre 2026 après la fin technique du run, les quatre traces contiennent exactement
894 lignes et `pgrep -x llama-server` ne renvoie aucun processus. La revue indépendante
Euler rapporte un code de sortie 0 et une validation stricte réussie de l'ordre, du JSON,
des doublons, des effectifs, des rejets, des empreintes et de la tokenisation.

La commande finale préparée exigeait toutefois aussi deux marqueurs locaux explicites:

- la chaîne littérale `RUN TERMINE` dans `data/traces/r7-run.log`;
- le statut global `TERMINE` dans `data/traces/r7-registre.json`.

Au contrôle suivant la revue Euler, le journal ne contenait pas cette chaîne et le registre
portait encore `CONTROLES_HORS_LIGNE_OK`. Ces deux gardes échouent. Conformément à
l'instruction de ne pas relancer et de s'arrêter si une garde échoue, ni
`r1_evaluer.py --suffixe r7 --sans-figure` ni `r7_evaluer.py` n'ont été exécutés par cette
tâche. Aucun résultat, verdict H1 à H4 ou interprétation des traces Final n'a été produit.

Ce blocage est un écart d'instrumentation de terminaison, pas un constat d'incomplétude des
quatre traces. Il appartient à l'orchestrateur de décider prospectivement quelle preuve de
fin autoritative remplace les marqueurs absents; cette tâche ne les crée pas après coup.
