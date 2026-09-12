# C7, nul de marge corrigé : préenregistrement

Écrit le 12 septembre 2026, **avant** `analyses/c7_nul_corrige.py` et avant tout calcul.
Aucun chiffre de ce document n'a été regardé dans une sortie de ce nouveau script : les
seules valeurs citées comme existantes sont celles déjà publiées de `c7-disjoint-resultats.md`.

## 1. Le défaut réparé

`analyses/c7_disjoint.py`, fonction `construire_nul`, ligne 134 :

```python
out = np.where(masque, np.where(tirage_correct, y_ref, faux), -1)
```

Ce prédicteur devait ne porter **que** la marge d'exactitude par personne q_i, sans aucune
empreinte individuelle. En réalité il écrit `y_ref` — la vraie réponse de la personne — avec
probabilité q_i : c'est une copie bruitée du vecteur réel, donc l'empreinte individuelle
**maximale**. Fuite secondaire, ligne 133 : `faux = faux + (faux >= y_ref)` fait aussi
dépendre les cellules *fausses* de la vraie réponse (elles l'évitent). Le témoin ne teste
donc pas ce qu'il prétend tester, et le verdict qu'il porte (prédiction (b) réfutée, rho nul
moyen 0,984, 95e centile 1,000 contre 0,969 observé) est sans valeur probante.

## 2. Ce qui est mesuré, à l'identique de c7_disjoint

* **Périmètre** : 60 items communs (`c7_reidentification.items_communs`), vérité
  `humains vague 4`, segment `S_gra`, les 12 prédicteurs (8 configurations LLM + B0 tirage,
  B1 argmax, B2 argmax, PMM k=10). Le point humain (retest v1-3) est calculé à part et
  n'entre dans aucun rho.
* **Fidélité** = chute brute : exactitude vraie moins exactitude moyenne sous 40 permutations
  des personnes intra-`S_gra` (`a44_commun.permuter_intra`, `a44_mesures.exactitude_codes`).
* **Fuite** = top-1 moyen de ré-identification par accord de Hamming contre le pool des
  2 058 humains v4, 3 tirages de départage des ex æquo (`a2_commun.distance_hamming`).
* **rho** = Spearman des 12 points (fidélité, fuite), **sur les 60 items entiers** — pas de
  partage A/B. C'est la convention de la section 2 de `c7_disjoint.py`, celle du nul.
  Conséquence assumée et nouvelle ici : le comparateur du nul est le rho du prédicteur réel
  **mesuré sur les mêmes items entiers**, pas le rho disjoint de 0,969. `c7_disjoint.py`
  comparait un rho disjoint à un nul sur items entiers ; ce script calcule les deux sur le
  même plan et publie les deux.
* **Fuite en bits** = bits d'identité par la voie rang, borne dyadique + Miller-Madow,
  `c7_bits.bits_et_ic` et `c7_bits.rangs_tous_tirages` importées telles quelles, 20 tirages
  de départage.

## 3. Les trois constructions corrigées

Notation : `y[i]` vecteur des 60 réponses humaines v4 de la personne i ; `x[i]` sortie du
prédicteur réel ; `masque[i]` ses cellules couvertes ; q_i son exactitude conditionnelle par
personne. Tous les nuls conservent **le masque de couverture réel** et **q_i**, par
construction : q_i est précisément la seule chose que ce témoin a le droit de garder.

**N1 — cible de substitution (mode de segment, laissé-un-dehors).**
z[i] = vecteur des modes de chaque item **dans le segment `S_gra` de i, calculé en excluant
i lui-même** (repli sur le mode global hors i si le segment a moins de 2 autres membres).
Sortie : `out[i,j] = z[i,j]` avec probabilité q_i, sinon une modalité tirée uniformément
parmi les K_j − 1 autres que `z[i,j]`.
*Où `y` intervient* : (a) dans le scalaire q_i ; (b) dans z[i], qui est une statistique des
**autres** personnes du segment — la ligne i est explicitement retirée du calcul de son
propre mode. Aucune cellule de `y[i]` n'est jamais lue pour écrire `out[i]`. Le tirage des
valeurs fausses évite `z[i,j]`, jamais `y[i,j]`. Ce n'est donc pas une fuite d'identité :
deux personnes du même segment ayant le même q reçoivent des sorties échangeables.

**N2 — exactitude appariée sur le vecteur d'une autre personne.**
π = dérangement des personnes **à l'intérieur de chaque segment `S_gra`** (π(i) ≠ i garanti ;
repli sur un dérangement global pour les segments de taille 1). Sortie :
`out[i,j] = y[π(i),j]` avec probabilité q_i, sinon une modalité tirée uniformément parmi les
K_j − 1 autres que `y[π(i),j]`.
*Où `y` intervient* : dans le scalaire q_i, et dans `y[π(i)]`, le vecteur d'**une autre**
personne. Ce n'est pas une fuite sur i : l'attaquant qui retrouve la source de `out[i]`
retrouve π(i), pas i. C'est le pendant exact du nul cassé — même texture statistique, mêmes
marginales réalistes, même corrélation inter-items — avec l'identité déplacée d'un cran.

**N3 — permutation des identités.**
σ = permutation des personnes intra-`S_gra` ; `out = x[σ]`. Les vecteurs réels sont conservés
intégralement, seul le lien personne↔vecteur est rompu ; le profil des q est préservé en
population mais réaffecté.
*Où `y` intervient* : nulle part. `out[i]` ne dépend que de la personne σ(i).
Réserve déclarée : ici l'exactitude par personne mesurée contre `y[i]` n'est plus q_i mais
q_{σ(i)} ; N3 conserve la **distribution** des q, pas l'appariement. C'est la contrepartie de
sa pureté (aucune lecture de `y`).

**N0 — nul cassé d'origine**, recalculé à l'identique et nommé « nul cassé » partout, comme
comparateur historique. Il n'a valeur que de repère.

## 4. Contrôles bloquants (échec bruyant, arrêt du script)

1. **Exactitude visée atteinte** : pour N1, |exactitude(out[i], z[i]) − q_i| ; pour N2,
   |exactitude(out[i], y[π(i)]) − q_i| ; pour N3, |exactitude(out[i], y[σ(i)]) − q_{σ(i)}|.
   Critère : écart absolu **moyen < 0,01** et écart **maximal < 0,08** sur les personnes
   couvertes (la borne max tient compte du bruit binomial à 60 cellules, dont l'écart type
   vaut au plus 0,065). Échec ⇒ `sys.exit`.
2. **Masque identique** : `(out >= 0) == (x >= 0)` cellule à cellule, sinon `sys.exit`.
3. **Non-lecture de la cible** : pour N2 et N3, π(i) ≠ i et σ(i) ≠ i pour toute personne d'un
   segment d'au moins 2 membres ; part de points fixes rapportée et exigée nulle hors
   segments singletons.
4. **Reproduction du nul cassé** : le rho moyen recalculé de N0 doit retomber à
   0,984 ± 0,010 et son 95e centile à 1,000. Sinon le portage est faux et rien n'est publié.

## 5. Paramètres figés

Graine `20260912` (celle de `c7_disjoint.py`), 100 réplicats par construction, 40
permutations pour la chute, 3 tirages de départage pour le top-1, 20 pour les bits, 3
réplicats seulement pour les bits (coût), 2 000 tirages de bootstrap sur les personnes.
Le script est exécuté **deux fois** et l'identité octet à octet du CSV est vérifiée.

**Bootstrap sur les personnes pour rho** : on conserve, par configuration, les trois vecteurs
par personne (exactitude, exactitude moyenne sous permutation, indicatrice top-1) ; un tirage
rééchantillonne les personnes, recalcule les 12 chutes et les 12 fuites, puis le Spearman.
C'est exactement la même statistique que le calcul direct quand le tirage est l'identité
(la chute est une moyenne par personne), le pool des candidats restant la population entière.

## 6. Prédictions chiffrées, écrites avant exécution

| Quantité | Prédiction |
|---|---|
| rho du prédicteur **réel**, 60 items entiers | 0,97 ; intervalle déclaré [0,90 ; 1,00] |
| rho du **nul cassé** (N0) | 0,984 ± 0,010 en moyenne, 95e centile 1,000 |
| rho **N1**, moyenne sur 100 réplicats | proche de 0 ; \|moyenne\| < 0,50 ; 95e centile < 0,95 |
| rho **N2**, moyenne | proche de 0 ; \|moyenne\| < 0,50 ; 95e centile < 0,95 |
| rho **N3**, moyenne | proche de 0 ; \|moyenne\| < 0,50 ; 95e centile < 0,95 |
| chute (fidélité) des nuls corrigés, toutes configs | \|chute\| < 0,02 |
| top-1 des nuls corrigés, toutes configs | < 0,010 (hasard = 1/2058 = 0,00049) |
| top-1 du nul cassé, meilleure config | > 0,10, c'est-à-dire du même ordre ou au-dessus du réel |
| bits des nuls corrigés | < 0,50 bit |
| bits du nul cassé, meilleure config | > 3 bits |

Raison de ces prédictions : un prédicteur dont le contenu ne dépend pas de la personne ne
peut être ni fidèle à elle (la chute tombe à zéro, les sorties sont échangeables intra
segment) ni permettre de la retrouver (le top-1 tombe au hasard). Les deux axes s'effondrent
**ensemble**, et le Spearman de 12 points quasi constants devient du bruit centré sur zéro.

## 7. Règle de décision, les deux issues écrites d'avance

Soit rho_reel le rho du prédicteur réel sur items entiers, et P95(N) le 95e centile de la
distribution des 100 rho d'une construction N.

* **Issue A — la réfutation tient.** Si pour **toutes** les constructions corrigées
  rho_reel ≤ P95(N) : une simple marge d'exactitude par personne suffit à reproduire le
  couplage. Le nul cassé avait, par chance, la bonne conclusion. La thèse « la fidélité d'un
  jumeau est ce qui le rend identifiable » **reste réfutée**, le titre, le résumé, §1.1, §5.1,
  la figure 2 et la ligne 1 du tableau 3 sont maintenus **mais** leur source devient ce
  témoin-ci, et le texte doit dire que le premier témoin était défectueux.
* **Issue B — la réfutation tombe.** Si pour **toutes** les constructions corrigées
  rho_reel > P95(N) : la marge seule ne reproduit pas le couplage, la prédiction (b) du
  préenregistrement `c7-disjoint` devient **confirmée**, la réfutation publiée est retirée, et
  la thèse initiale redevient soutenable — dans la limite exacte de la réserve du §8.
* **Issue C — divergence.** Si les constructions ne donnent pas le même verdict, le résultat
  est rapporté tel quel, sans arbitrage : « indécidable, deux témoins licites désaccordés ».

## 8. Réserve déclarée d'avance, valable surtout sous l'issue B

Un nul correct détruit **les deux** axes à la fois : c'est sa définition. Dépasser un tel nul
prouve seulement que le couplage **n'est pas produit par un taux d'exactitude par personne
seul** ; cela n'établit ni causalité, ni que la fidélité *à cette personne-là* soit le
mécanisme. Un nul dont les deux axes sont dégénérés rend d'ailleurs le dépassement presque
automatique : on publie donc, comme diagnostic obligatoire, le niveau des deux axes sous
chaque nul, le nombre de réplicats où un axe est constant (Spearman non défini) et la part
d'ex æquo. Si plus de la moitié des réplicats ont un axe dégénéré, l'issue B est déclarée
**faiblement informative** et rapportée comme telle. n = 12 configurations rend par ailleurs
le Spearman grossier : aucune troisième décimale n'est interprétée.

## 9. Sorties

`resultats/c7-nul-corrige.csv` — une ligne par (construction, configuration) : chute, top-1
**enregistré par configuration**, ce que la boucle des lignes 221-235 de `c7_disjoint.py`
calculait et jetait, bits, et les IC bootstrap ; plus une ligne par (construction, réplicat)
pour les rho. `resultats/c7-nul-corrige-resultats.md` — la lecture.

**Éthique** : étude de risque sur un jeu déjà public, aucun identifiant, aucun pid, aucun
appariement individuel écrit ou imprimé ; taux agrégés uniquement. Aucun appel de modèle,
aucun réseau, lecture seule sur `data/`. Aucun script existant modifié.
