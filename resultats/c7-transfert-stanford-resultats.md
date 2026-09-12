# C7-transfert-Stanford, résultats : le canal inter-jumeaux se réplique, plus faible

Préenregistré dans `c7-transfert-stanford-preenregistrement.md`, calculé par
`analyses/c7_transfert_stanford.py`. Table complète dans
`resultats/c7-transfert-stanford-attaque.csv`. **Aucun identifiant imprimé.**

## Attaque entretien ↔ enquête, 1 052 personnes
| domaine | items | sens | top-1 | rang médian | démo (top-1) | contrôle décoy |
|---|---|---|---|---|---|---|
| GSS | 177 | entretien→enquête | **11,9 %** [10,1;13,8] | 12/1052 | 1,5 % | 0,05 % |
| GSS | 177 | enquête→entretien | **13,0 %** [11,2;14,9] | 13/1052 | 2,5 % | 0,31 % |
| économiques | 5 | entretien↔enquête | 0,20-0,30 % | ~424/1052 | 0,08-0,24 % | ≤0,04 % |
| Big Five | 5 | entretien↔enquête | 0,19 % (2 sens) | ~252/1052 | 0,10 % | ≤0,29 % |
Hasard = 0,095 % partout (1/1052).

## Contrôle d'items et comparaison Twin
Colonnes déjà identiques entre conditions : 177 items GSS, 5 pour chaque domaine continu,
pas de sous-tirage. À 5 items le signal disparaît dans le bruit démo/décoy ; à 177 items
il domine (facteur 5-8× le démo, 40-250× le décoy). Twin : 36,4 % à 60 items, 0,45 % à 19
items, contrôle 0,06 %. Stanford GSS (177 items) plafonne à 12-13 %, **en dessous** du
36,4 % de Twin malgré 3× plus d'items : la relation top-1/items diffère entre jeux.
Stanford à 5 items (0,2 %) est du même ordre que Twin à 19 items (0,45 %).

## Verdict sur la prédiction
Top-1 GSS ≥ 20 % : **rejeté** (11,9-13,0 %). Nettement au-dessus du démographique :
**confirmé** (facteur 5-8×). Contrôle anti-artefact < 1 % : **confirmé** (≤0,31 %).
Domaines à 5 items nettement en dessous : **confirmé**. Critère d'échec préenregistré
(« ne dépasse pas nettement le démographique ») **non atteint** : le canal se réplique,
plus faible que sur Twin, sous le seuil chiffré prédit.

## Portée pour l'article
Résultat qui soutient : un organisme qui publie deux jeux de jumeaux distincts d'une
même cohorte crée à lui seul un canal de ré-identification, au-delà de Twin-2K-500.

## En clair
Comparer le double numérique « entretien » d'une personne à ses 1 052 doubles
« enquête » suffit à la retrouver environ une fois sur huit — bien au-dessus du hasard et
de la démographie seule, mais moins fort que sur l'autre jeu testé.
