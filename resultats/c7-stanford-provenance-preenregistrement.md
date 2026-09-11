# C7 Stanford provenance, préenregistrement : le 65,7 % est-il contaminé ?

**Écrit le 12 septembre 2026, avant tout calcul.** Fait suite à `c7-stanford-resultats.md`
(top-1 = 65,7 %, condition composite) et à l'examen critique indépendant qui signale que
la provenance des agents n'a pas été auditée, contrairement à Twin
(`resultats/twin-ab-audit-provenance-2026-09-11.md`). Aucun identifiant, aucun appariement
individuel : uniquement des taux agrégés, comme dans `c7_stanford.py`.

## 1. Ce que la documentation dit déjà (avant calcul)
`FIGURE2_PIPELINE.md` §6.1 : condition « Survey-Based » = `survey_agents_summary.csv`,
construite à partir des réponses d'enquête. Le code source
(`figure2/code/source/new_analysis/analyze_gss_filtered.py`) montre que l'agent, pour
chaque condition, répond lui-même à un GSS simulé (`polished/out.csv`) — ce n'est pas une
recopie mécanique du fichier de sortie. Mais l'article (arXiv 2411.10109) décrit l'agent
« survey-based » comme alimenté par des réponses « including General Social Survey
items » : le risque est que le contexte donné à l'agent contienne déjà la réponse de vague
1 à l'item même qu'on lui fait ensuite deviner.

## 2. Test décisif : symétrie vague 1 / vague 2
Sur le bloc GSS, cellules où l'humain a changé de réponse entre vague 1 et vague 2
(`p_wave1_summary.csv` ≠ `p_wave2_summary.csv`, aucune des deux manquante). Pour chaque
condition (composite, enquête, entretien), taux d'accord de l'agent avec la vague 1 contre
la vague 2 sur ces seules cellules. IC 95 % par bootstrap sur les personnes (2000 tirages,
graine 20260912, `a2_commun.bootstrap_personnes` repris tel quel).

**Prédiction** : si la construction est propre (l'agent n'a pas vu la réponse cible), les
deux taux sont à moins de 3 points l'un de l'autre. Un écart net vers la vague 1 signale
que l'agent a vu cette réponse.

## 3. Décomposition par source et verdict
Réutilisation de `resultats/c7-stanford-reidentification.csv` (déjà calculé, pas de
recalcul) pour le top-1 par condition GSS. Vérification du chiffre entretien seul annoncé
à 44,7 %. Verdict : contamination exclue / partielle / établie selon le test 2, chiffre le
plus défendable indiqué en conséquence.
