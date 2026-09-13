# Coût de D4 (mélange intra-segment) sur des tâches en aval, synthèse

statut: courant
mandat: Repondre a la question du responsable : le melange intra-segment (D4) qui fait tomber la re-identification abime-t-il la qualite des reponses, chiffres a l'appui (taches en aval, courbe de reglage, comparaison DP)
agent: Claude Sonnet 5, sous-agent synthese cout-defense
ecriture: resultats/cout-defense-synthese-2026-09-13.md uniquement
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0.00

Question du responsable : le mélange intra-segment qui fait tomber la ré-identification
à 0,05 % (en réalité 0,126 % [0,012 ; 0,284], top-1, `resultats/c7-defense-resultats.csv`
ligne `D4_melange`) abîme-t-il la qualité des réponses, et de combien, précisément ?

Sources vérifiées ligne à ligne : `resultats/c7-defense-resultats.csv`,
`resultats/c7-defense-courbe.csv`, `resultats/c7-utilite-aval-resume.json` (+ ses trois
CSV `A-groupes`/`B-regression`/`C-acp`), `resultats/c7-dp-resultats.csv`. Tous les chiffres
d'écart humains cités ici sont confirmés dans ces fichiers.

## 1. Ce qui a été mesuré comme dégâts « en abstrait » (rappel vérifié)

`c7-defense-resultats.csv`, ligne `D4_melange` : `erreur_distribution=0.0`,
`erreur_groupes=0.0` (exacts par construction — permuter dans un segment ne change ni sa
moyenne ni la moyenne globale), `erreur_correlations=4.399958990777788`,
`utilite_globale=1.4666529969259292` (= moyenne des trois, **trompeuse**, retirée des
documents). Mesuré contre les humains (colonnes `_hum`) : `erreur_correlations_hum` passe
de `5.7754464636422895` (sans défense) à `9.708521960510733` (D4), soit **+68,08 %**
(9.708521960510733 / 5.7754464636422895 = 1,6808). Ces chiffres sont confirmés tels quels.

## 2. Les tâches en aval mesurées (`analyses/c7_utilite_aval.py`, `c7-utilite-aval-*`)

Trois analyses rejouées sur humains v4 / jumeau brut / jumeau D4 (2 058 personnes, items
d'achat binaires de `c7_mecanisme.items_achat`, segment `S_gra` chargé tel quel, jamais
recalculé) :

- **A. Comparaison de groupes** : écart de proportion Hommes−Femmes sur l'item d'achat
  `1_Q295`, IC bootstrap personnes (2000 tirages). Usage type : « les hommes achètent-ils
  plus tel produit que les femmes ? »
- **B. Régression MCO** : `5_Q295` ~ genre (Homme=1) + âge 65+ (dummy) + `1_Q295` +
  `2_Q295`. Usage type : expliquer un achat par la démographie et deux autres achats.
- **C. ACP** sur les 40 items d'achat : part de variance des deux premiers axes + part des
  loadings de l'axe 1 inversés vs humains. Usage type : détection de segments/structure
  latente d'achat.

## 3. Coût mesuré sur chacune, avec son intervalle — et où il est gratuit vs cher

**A — gratuit, exactement.** `c7-utilite-aval-A-groupes.csv` : écart H-F identique à 16
décimales entre `jumeau_brut` (0.010020630710285916, IC [-0.0327;0.0524]) et `jumeau_D4`
(0.010020630710285916, IC [-0.0334;0.0508]) : coût de D4 = 0. Mais attention, cela ne
veut pas dire que l'analyse est fiable : le jumeau (brut comme D4) se trompe déjà de
signe face aux humains (humains : -0,047, **significatif** ; jumeau : +0,010, non
significatif) — une erreur préexistante à D4, pas causée par lui.

**B — gratuit sur les coefficients démographiques, cher sur les coefficients d'achat.**
`c7-utilite-aval-B-regression.csv` : `genre_H` et `age_65+` restent non significatifs et
de même signe dans les trois conditions (coût D4 = 0 sur ces deux variables). Les
coefficients d'achat, eux, passent de significatifs chez le jumeau brut
(`achat_1_Q295` : coef 0,060, t=2,73, p<.01 ; `achat_2_Q295` : coef 0,073, t=3,26,
p<.001) à non significatifs après D4 (`achat_1_Q295` : coef 0,016, t=0,74, n.s. ;
`achat_2_Q295` : coef 0,015, t=0,66, n.s.). Coût concret : **2 coefficients sur 4 perdent
leur significativité**, exactement ceux qui reliaient deux achats d'une même personne.

**C — coût réel mais plus petit que l'écart de départ sur la variance ; coût structurel
plus grand sur la composition.** `c7-utilite-aval-resume.json` : part de variance PC1+PC2
— humains 15,03 %, brut 9,78 %, D4 6,31 %. Écart brut→D4 = **3,46 points**
(`C_ecart_points_D4_vs_brut`), plus petit que l'écart humains→brut = **5,25 points**
(`C_ecart_points_brut_vs_hum`) : sur la seule variance expliquée, D4 ajoute moins que
l'erreur déjà présente. Mais les **loadings** de l'axe 1 : 0 % inversés brut vs humains,
**45 % inversés** D4 vs brut (`C_pct_loadings_pc1_inversees_D4_vs_brut`) : D4 change quels
items composent l'axe, un coût que la variance seule ne montre pas.

**Verdict usage par usage** : gratuit pour une comparaison de groupes démographiques ou
des coefficients démographiques de régression ; cher (perte de significativité ou
recomposition de l'axe) pour tout ce qui repose sur le lien entre deux achats d'une même
personne (régression inter-items, ACP multi-items).

## 4. La courbe de réglage (`c7-defense-courbe.csv`) — trois points, taux vs coût

| réglage | top-1 (IC95%) | perte d'utilité moyenne (pts) | détail dist./groupes/corr. |
|---|---|---|---|
| D2_bruit, p=50% | 1,91 % [1,35 ; 2,48] | 2,10 | 0,70 / 2,08 / 3,51 |
| D1_agregation, k=10 | 0,55 % [0,29 ; 0,87] | 3,77 | 3,53 / 2,15 / 5,62 |
| D4_melange (recommandé) | 0,13 % [0,01 ; 0,28] | 1,47 (moyenne trompeuse ; coût réel 4,4 sur la seule composante corrélations) | 0,0 / 0,0 / 4,40 |

Compromis lisible : D2 p=50% est moins protecteur (top-1 quinze fois plus haut que D4 :
1,91 % contre 0,13 %) et coûte quand même plus cher en moyenne nominale (2,10 > 1,47), et
il touche les groupes (2,08) là où D4 y est à 0,0 — donc D2 n'est pas le compromis
« moins protecteur mais moins cher » qu'on pourrait espérer. D1 k=10 descend sous 1 %
comme D4 mais coûte plus cher **sur chaque composante**, y compris les corrélations
(5,62 > 4,40). Sur ce tableau, aucun réglage testé ne bat D4 à la fois sur la protection
et sur le coût par composante : D4 reste la meilleure combinaison des quatorze réglages
mesurés, une fois le coût lu composante par composante plutôt qu'en moyenne.

## 5. Comparaison à la confidentialité différentielle — SECTION RÉTRACTÉE le 13/09/2026

**Cette section entière est retirée.** Elle affirmait qu'« à protection comparable, la DP
coûte plus cher que D4 sur chacune des trois composantes » et que « D4 domine la DP
composante par composante ». Les deux moitiés de cette affirmation sont fausses :
la « protection comparable » n'en est pas une, et le « coût de la DP » n'est pas un coût
de la DP. Le texte d'origine est conservé ci-dessous, barré, et ne doit plus être cité.
Fait foi : `resultats/audit-comparaison-dp-2026-09-13.md` (§F1 à §F8, formulation de
remplacement au §8) ; fiche de report vers le manuscrit :
`resultats/retractation-dp-d4-2026-09-13.md`. Le reste de ce rapport (sections 1 à 4 et 6,
tâches en aval et courbe de réglage) ne dépend pas de la DP et n'est pas retiré.

Les quatre motifs, tous vérifiés par recalcul :

1. **La DP est ajustée sur les humains et notée contre le jumeau** (`analyses/c7_dp.py`,
   l. 148 contre l. 152). Elle se voit facturer l'écart humains↔jumeau, qui vaut
   3,118 points — soit exactement le « coût » de 3,1-3,2 publié ici. Ajusté sur le jumeau,
   le même générateur tombe à 0,92 point à eps = 10.
2. **Le budget de confidentialité ne contribue à rien.** À eps = infini, c'est-à-dire sans
   aucune confidentialité, le coût est déjà le même (3,52, pire qu'à eps = 10). La
   contribution marginale du budget est de 0,0 à 0,3 point : ce qui est mesuré est le coût
   de l'hypothèse d'indépendance entre items.
3. **Les `0,0` de D4 ne sont pas un coût nul, ils sont la republication.** `defense_d4`
   permute item par item à l'intérieur du segment : le multi-ensemble intra-segment est
   conservé à l'identique sur 1 560 couples segment × item sur 1 560
   (`resultats/c7-d4-adaptatif.csv`). D4 republie exactement l'histogramme que la DP, elle,
   protège. Comparer les deux sur l'exactitude de cet histogramme est circulaire.
4. **L'ordre s'inverse sous un attaquant qui choisit ses colonnes.** D4 ne touche pas les
   20 items d'opinion : un attaquant qui écarte le bloc brouillé obtient 0,29 %
   (`c7-attaquant-fort.csv`, stratégie S1) contre 0,085 % pour la DP à eps = 3. Et ces
   taux valent 0 à 3 personnes sur 2 058, avec des intervalles qui se recouvrent tous :
   aucun classement des deux mécanismes n'est soutenable, dans aucun sens.

Ce qui survit de la nuance conceptuelle, et qui ne dépend d'aucun chiffre du tableau :
la DP protège l'appartenance à l'échantillon, pas la liaison attribut-personne visée par
notre attaque ; sa faible fuite vient de ce qu'elle ne conditionne jamais sur un individu
(fidélité individuelle < 0,2 pt à tout epsilon), pas du budget choisi. Les deux mécanismes
ne répondent pas à la même menace — et c'est tout ce que l'on peut en dire ici.

<!-- TEXTE D'ORIGINE, RETIRÉ LE 13/09/2026, CONSERVÉ POUR LA TRAÇABILITÉ, NE PLUS CITER :

| epsilon | top-1 (IC95%) | erreur_distribution | erreur_groupes | erreur_correlations | moyenne (trompeuse) |
|---|---|---|---|---|---|
| 3 | 0,158 % [0,012 ; 0,340] | 3,11 | 2,40 | 4,47 | 3,33 |
| 10 | 0,000 % [0 ; 0] | 3,21 | 2,33 | 4,59 | 3,38 |
| D4 | 0,126 % [0,012 ; 0,284] | 0,0 | 0,0 | 4,40 | 1,47 |

À protection comparable (top-1 ≈ 0,13-0,16 %, voire 0 % à eps=10), la DP coûte plus
cher que D4 sur chacune des trois composantes : distribution (3,1-3,2 contre 0,0),
écarts de groupe (2,3-2,4 contre 0,0), et même sur les corrélations, où la DP est
légèrement plus chère (4,47-4,59 contre 4,40) — alors que la comparaison naïve des
moyennes (3,33-3,38 contre 1,47) suggérait à tort que la DP coûtait deux fois plus, ce qui
sous-estimait encore l'écart réel en faveur de D4. Nuance conceptuelle
(`c7-dp-resultats.md`) : la DP protège l'appartenance à l'échantillon, pas la liaison
attribut-personne visée par notre attaque — sa faible fuite vient de ce qu'elle ne
conditionne jamais sur un individu (fidélité individuelle < 0,2 pt à tout epsilon), pas
du budget choisi. Les deux mécanismes ne répondent donc pas exactement à la même menace,
mais sur le tableau chiffré, D4 domine la DP composante par composante à protection egale
ou supérieure.
-->

### 5 bis. Ce qui doit être dit à la place de la section 4 sur D4

La ligne « D4_melange (recommandé) … 0,0 / 0,0 / 4,40 » de la section 4 reste exacte comme
lecture de `c7-defense-resultats.csv`, mais sa lecture **change** : les deux `0,0` ne sont
pas un coût évité, ils sont la republication exacte de la statistique (motif 3 ci-dessus).
Et le `0,13 %` de la même ligne est le taux sous attaque naïve contrainte aux 60 items ;
le taux de D4 à publier est **0,29 % [0,10 ; 0,53]**, celui de l'attaquant adaptatif S1.
D4 reste le meilleur des quatorze réglages mesurés **sur ce banc**, sans aucune garantie
formelle et contre les seules attaques que nous avons construites.

## 6. Ce qui manque pour répondre plus loin, sans l'estimer

Aucune tâche en aval mesurée en dehors des trois de `c7_utilite_aval.py` (A/B/C) : pas de
prédiction hors échantillon, pas de tâche de classification/segmentation ciblée, pas de
mesure sur les 20 items d'opinion (la défense ne leur est jamais appliquée, donc aucun
coût n'est mesuré ni attendu là-dessus — non testé, pas nul par hypothèse). Un seul jumeau
(`JSON Persona - GPT4.1`) et un seul réglage D4 (« permutation intra-segment », pas de
variante de granularité de segment testée) : aucune donnée sur un mélange inter-segments
plus large ou plus étroit. Ne pas généraliser au-delà de ces trois tâches et de ce réglage
sans nouveau calcul.
