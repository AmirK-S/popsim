# C7 monde ouvert, préenregistrement : et si la cible n'est pas dans la base ?

**Écrit le 12 septembre 2026, avant tout calcul.** `c7_reidentification.py` et
`c7_stanford.py` supposent la cible toujours dans le pool (monde fermé) : la métrique la
plus flatteuse. Sans taux de fausses accusations, un relecteur PoPETs/USENIX démonte le
résultat. Ce plan ajoute le monde ouvert, calculé dans `analyses/c7_monde_ouvert.py`.

## 1. Protocole
Un seul calcul d'accord par prédicteur (`a2_commun.distance_hamming`, repris tel quel)
donne les deux régimes sans recalcul : **présente** = meilleur (top1) et deuxième
meilleur candidat sur le pool entier ; **retirée** = mêmes valeurs, colonne de la vraie
personne masquée. Score de confiance = écart top1 − top2 (accord), dans chaque régime.

## 2. Mesures
ROC (TPR contre FPR en faisant varier le seuil de confiance), AUC, **TPR à FPR = 0,1 % et
1 %** (interpolation sur la courbe), taux d'abstention au seuil calibré sur FPR = 1 %.
Précision au rang 1 (meilleur candidat, sans seuil) pour p = 0, 50, 90 % de cibles
absentes : formule analytique (1 − p) × top1 monde fermé, car une cible absente ne peut
jamais donner un rang 1 correct par définition.

## 3. Prédicteurs
Twin (2 058, 60 items communs) : meilleur jumeau riche = JSON Persona GPT4.1 ; Demographics
Only - GPT4.1-mini ; **PMM k=10 nouveau** (plus proche voisin sur les 14 questions
démographiques brutes, `a2_commun.b2_voisins` repris tel quel, tirage parmi les k voisins,
convention déjà en usage dans `a35`/`a41`) ; retest humain (vagues 1-3) comme plafond.
Stanford (bloc GSS, loader de `c7_stanford.py` réutilisé sans modification) : condition
composite (meilleure), démographique seule, PMM k=10 (mêmes 4 colonnes de
`demographic_summary.csv`), retest humain vague 2.

## 4. Prédiction chiffrée
TPR à FPR = 1 % **> 5 %** pour le meilleur jumeau riche sur Twin, **> 30 %** sur Stanford
composite ; Demographics Only et PMM restent **< 1 %** sur les deux jeux.

## 5. Garde-fous
Aucun pid ni identité imprimés. Ordre des candidats non permuté ici (le score de marge,
symétrique, ne dépend pas d'un raccourci d'index). Aucun fichier existant modifié, lecture
seule sur `data/`, aucun appel de modèle.
