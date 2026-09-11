# C7 monde ouvert, résultats : et si la cible n'est pas dans la base ?

Préenregistré dans `resultats/c7-monde-ouvert-preenregistrement.md`, calculé par
`analyses/c7_monde_ouvert.py` (marge top1 − top2, deux régimes dérivés d'une seule
matrice d'accord, 5 tirages de départage, graine 20260912). Sanity check : les taux monde
fermé retrouvés ici (Twin JSON Persona GPT4.1 20,64 %, Demographics Only 2,15 %, Stanford
composite 65,61 %, retest humain 81,6 % / 96,7 %) collent aux résultats déjà publiés.

## 1. Tableau (voir aussi `c7-monde-ouvert.csv` et la figure `c7-monde-ouvert-roc.png`)

| jeu | prédicteur | TPR à FPR=0,1 % | TPR à FPR=1 % | précision@1, 0/50/90 % absents | % du plafond humain (FPR=1 %) |
|---|---|---|---|---|---|
| Twin | Meilleur jumeau (JSON Persona GPT4.1) | 0,93 % | **3,04 %** | 20,6 / 10,3 / 2,1 % | 5,6 % |
| Twin | Demographics Only | 0,10 % | 0,20 % | 2,1 / 1,1 / 0,2 % | 0,4 % |
| Twin | PMM k=10 | 0,00 % | 0,00 % | 0,06 / 0,03 / 0,006 % | 0,0 % |
| Twin | Retest humain (plafond) | 36,9 % | 54,5 % | 81,6 / 40,8 / 8,2 % | 100 % |
| Stanford | Meilleur agent (composite) | 8,47 % | **20,39 %** | 65,6 / 32,8 / 6,6 % | 22,5 % |
| Stanford | démographique | 0,00 % | 0,00 % | 2,3 / 1,2 / 0,2 % | 0,0 % |
| Stanford | PMM k=10 | 0,00 % | 0,00 % | 0,5 / 0,3 / 0,05 % | 0,0 % |
| Stanford | Retest humain (plafond) | 63,5 % | 90,7 % | 96,7 / 48,4 / 9,7 % | 100 % |

## 2. Verdict contre la prédiction préenregistrée

**Non confirmée, dans le sens pessimiste.** La prédiction écrite avant calcul demandait
TPR à FPR=1 % > 5 % (Twin) et > 30 % (Stanford) : les valeurs mesurées sont **3,04 %** et
**20,39 %**, toutes deux sous la barre. Les comparateurs (Demographics Only, PMM) restent
bien sous 1 %, ce volet-là est confirmé. PMM (k plus proches voisins sur les seules
démographies) est même pire que Demographics Only : un simple vote de voisins ne capture
rien, c'est le raisonnement du modèle sur les démographies qui porte le peu de signal
mesuré à ce niveau.

## 3. Ce que le monde ouvert change

Le monde fermé racontait une découverte dans un cinquième des cas (Twin) ou deux tiers des
cas (Stanford). Le monde ouvert, seule mesure défendable en relecture, montre qu'à un
niveau de fausses accusations tenable (1 %), l'attaquant a raison **3 fois sur 100** (Twin)
ou **20 fois sur 100** (Stanford) — et qu'à 0,1 % de fausses accusations, quasiment plus
rien ne dépasse le bruit sur Twin (0,93 %). Rapporté au plafond humain (un vrai retest ne
fait pas mieux que 54,5 % / 90,7 % à ce même FPR), le meilleur jumeau Twin n'atteint que
5,6 % de la performance humaine, et le meilleur agent Stanford 22,5 %.

## 4. En clair

Si un attaquant s'engage à ne se tromper que 1 fois sur 100, un jumeau IA retrouve la vraie
personne dans son questionnaire d'achat 3 fois sur 100 (Twin) ou dans son sondage
d'opinion 20 fois sur 100 (Stanford) — loin des 20 % et 66 % annoncés en monde fermé, mais
loin d'être nul : le risque de vie privée est réel, juste plus modeste et plus honnête que
la version flatteuse.
