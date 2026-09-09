# a47. Errata appliques a la suite de la seconde relecture adverse

Chantier a47, 9 septembre 2026. Applique les corrections demandees par
`resultats/a45-relecture-adverse-2.md`, avec les recalculs qu'elles exigent.

Regle de travail : **aucun corps de rapport n'a ete reecrit**. Chaque document vise recoit
une section `## Errata du 9 septembre 2026` inseree juste apres son titre, qui cite la phrase
d'origine, donne la correction et donne la preuve. L'historique reste lisible.

Aucun appel de modele de langage. Aucun script existant n'a ete modifie. `data/` a ete lu
seulement. Les scripts `r1_*`, `r2_*` et leurs traces n'ont pas ete touches ; le
`llama-server` de la file de nuit n'a pas ete derange. Les caches `/tmp/a25-matrices.pkl`,
`/tmp/a28-foret.npy` et `/tmp/a35-methodes.pkl` ont ete relus, jamais reecrits.

**Scripts nouveaux**

| script | ce qu'il calcule | duree |
|---|---|---|
| `analyses/a47_chute_segmentations.py` | la chute d'exactitude sous permutation intra segment pour les 18 conditions, sous trois segmentations dont une sans ideologie ; le gain hongrois absolu et son plancher ; la correlation de la chute avec l'exactitude brute | 17 s, 4 coeurs |
| `analyses/a47_verifications.py` | le facteur d'amplification de a38 avant et apres permutation des personnes a l'interieur de leur camp ; la taille du contexte des deux regimes de a35 ; la lecture de `a2_baselines_gss` sur l'information de `B2` | 3 min |
| `analyses/a47_income_v6.py` | le balayage des 149 items par condition, la liste des items recopies, et la chute sous permutation sans eux | 1 min |

**Tableaux produits** : `a47-chute-deux-segmentations.csv`, `a47-plancher-reassignation.csv`,
`a47-correlation-chute-exactitude.csv`, `a47-a38-invariance-facteur.csv`,
`a47-contexte-regimes.csv`, `a47-items-recopies.csv`,
`a47-chute-hors-items-recopies.csv`.

**Reproduction**

```
.venv/bin/python analyses/a47_chute_segmentations.py --permutations 200
.venv/bin/python analyses/a47_verifications.py
.venv/bin/python analyses/a47_income_v6.py --permutations 200
```

**Controle de chaine.** Les colonnes `S_ideo` et `S_fin` de `a47-chute-deux-segmentations.csv`
reproduisent `a44-permutation.csv` au millieme sur les dix huit conditions, et les facteurs
de `a47-a38-invariance-facteur.csv` reproduisent `a38-camp.csv` au millieme. Les trois
scripts reimportent `a44_commun`, `a44_mesures`, `a28_test1_mode`, `a38_mesures`,
`a30_commun` et `a2_baselines_gss` sans une ligne de changement.

---

## 1. Les quatre resultats de mesure de ce chantier, en une page

**Un. La chute sous permutation depend de la segmentation, et le « 7 pour cent » est indexe
sur l'axe politique.** [MESURE, `a47-chute-deux-segmentations.csv`, 200 permutations par
cellule]

| condition | `S_ideo`, 7 cellules | `S_fin`, 42 cellules | **genre x race x age, 38 cellules, sans ideologie** |
|---|---|---|---|
| `agents v8` | **0,072** | 0,055 | **0,267** |
| **C2** | **0,073** | 0,074 | **0,185** |
| `B3 foret` | 0,129 | 0,082 | 0,187 |
| `agents v7` | 0,156 | 0,137 | 0,150 |
| `B1 argmax` | 0,175 | 0,117 | 0,228 |
| `agents demographiques (v6)` | 0,235 | 0,229 | 0,236 |
| `B2 argmax` | 0,357 | 0,348 | 0,424 |
| **C3** | **0,448** | 0,455 | **0,458** |
| `agents entretien (v3)` | 0,532 | 0,526 | 0,613 |
| `agents enquete` | 0,539 | 0,548 | 0,618 |
| `PMM k=10` | 0,595 | 0,573 | 0,625 |
| `agents composite` | **0,642** | 0,638 | **0,695** |
| *`B0 mode`, temoin* | *moins 0,005* | *moins 0,005* | *moins 0,005* |
| *`B0 tirage`, temoin* | *moins 0,006* | *moins 0,008* | *moins 0,008* |
| humains vague 2 | 1,000 | 1,000 | 1,000 |

Le classement survit, le chiffre non. La phrase du dossier devient : **7 pour cent du
plancher humain sous la segmentation qui contient l'ideologie, 18 a 27 pour cent sous celle
qui ne la contient pas, contre 64 a 70 pour cent pour `agents composite` dans les deux.** Le
rapport entre les deux camps de conditions passe de 9 pour 1 a 2,6 pour 1. Ce n'est pas un
effet de finesse : `S_fin` a 42 cellules et donne 0,055 pour `v8`, genre x race x age en a 38
et donne 0,267. La formule **« gabarits de groupe a 93 pour cent interchangeables » est
retiree**, et sous la segmentation sans ideologie quatre conditions, `v8`, C2, `B1` et
`B3 foret`, sortent de la classe « gabarit » que a44 7.2 fixe a moins de 15 pour cent.

**Deux. Le facteur d'amplification de a38 est une quantite de gabarit.** [MESURE,
`a47-a38-invariance-facteur.csv`] Il est **exactement invariant** sous permutation des
personnes a l'interieur de leur camp, ecart `0,00e+00` sur les 27 lignes mesurees, `v8`
3,091378 avant comme apres, C2 1,616674, C3 0,523026, `composite` 1,828597, `B1` 1,208929,
`B2` 0,973468, humains vague 2 1,025092. La raison est dans le code :
`a28_test1_mode.mesurer` construit le score de desirabilite par `compte(mat, j, it)`, qui
denombre les modalites sur les lignes du camp ; c'est une fonctionnelle de la seule table
(camp, modalite). **Il mesure les marges par camp, pas les personnes.**

**Trois. Le rapport de reassignation de 4,91 n'a pas de plancher, et son plancher est dans le
fichier.** [MESURE, `a47-plancher-reassignation.csv`, `S_ideo`] Le gain hongrois absolu d'une
population sans aucun signal individuel, `B0 tirage`, vaut **0,0820** sur 1 052 personnes ;
celui de `agents v8`, sur le meme perimetre, vaut **0,0687**, donc **en dessous**. Le 4,91 ne
mesure pas que la vraie assignation est arbitraire chez `v8` : il mesure que le denominateur,
0,0139, est petit. Reserve : le 3,09 de C2 porte sur 150 personnes, ou son gain vaut 0,0393,
et le plancher a 150 personnes n'a pas ete construit.

**Quatre. La chute sous permutation partage 82 pour cent de sa variance avec l'exactitude
brute.** [MESURE, `a47-correlation-chute-exactitude.csv`] Sur les treize conditions du
perimetre 1 052, humains vague 1 exclus : Pearson **0,906**, Spearman **0,874** sous `S_ideo`
(0,894 sous `S_fin`, 0,906 sous genre x race x age). Arithmetiquement attendu, la chute etant
une composante additive de l'exactitude, mais la phrase « l'exactitude ne voit pas la
distorsion » doit etre indexee sur les conditions ou les deux divergent, `B0 mode`,
`B3 foret` et `B1`.

**Deux verifications de code, sans recalcul possible mais sans ambiguite.**

- **C2 et C3 n'echangent pas l'etiquette** [CONFIRME, `analyses/a5_agents_locaux_gss.py`] :
  `systeme_c2` lignes 164 a 177 construit une invite qui contient les onze attributs de
  `demographic_summary.csv` et rien d'autre ; `systeme_c3` lignes 180 a 196 construit une
  invite qui contient les environ 119 items de contexte, question et reponse en clair, et
  aucune demographie. Le contraste melange deux changements.
- **`B2 argmax` ne recoit aucune demographie** [CONFIRME, `analyses/a2_baselines_gss.py`] :
  ligne 178, `enc.transform` alimente `B0` et `B1` seuls ; lignes 188 a 191, `B2` est un plus
  proche voisin par `distance_hamming` sur `codes[:, contexte]`, ou `contexte` est un
  ensemble d'items.

**Deux mesures de contexte.**

- Le regime severe de a35 laisse **132 a 144 items** de contexte contre **119** au regime
  facile [MESURE, `a47-contexte-regimes.csv`] : le « cout du retrait » de 6,55 points melange
  le retrait de 5 a 17 items cousins et l'ajout de 13 a 25 items ; c'est une borne basse.
- Seize items sont recopies a 0,95 ou plus par au moins une condition ; en les retirant, la
  chute de `v6` passe de **0,235 a 0,181** du plancher humain, un quart de son signal
  individuel apparent, quand `v8` (0,072 a 0,072), C2 (0,072 a 0,072) et `composite` (0,643 a
  0,638) ne bougent pas [MESURE, `a47-chute-hors-items-recopies.csv`]. Quatre des seize sont
  recopies par `v6` seul et sont des faits d'etat civil : `income` 0,994, `othlang` 1,000,
  `divorced` 0,997, `posslq/y` 0,995.

---

## 2. Tableau des corrections appliquees

Colonne « avant » : ce qui est ecrit dans le document rendu. Colonne « apres » : ce que
l'errata etablit. Tous les errata sont inseres en tete du document concerne, sous le titre
`## Errata du 9 septembre 2026`.

| document | objection a45 | phrase ou chiffre avant | apres | preuve |
|---|---|---|---|---|
| a29, E1, section 8 point 1 et revendication 6 | 1, D1 | « C2 contre C3 est **une ablation propre** » ; « [MESURE, **ablation** C3 contre C2, la mesure la plus propre du rapport] » | « un **contraste de conditionnement** dont les deux facteurs sont confondus » ; le 0,410 contre 0,194 reste, son attribution a l'etiquette seule tombe | `a5_agents_locaux_gss.py` `systeme_c2` et `systeme_c3` ; `a47-chute-deux-segmentations.csv` pour l'analogue `B1` contre `B2` |
| a31, E1, reponse en une ligne | 6.1, D7 | « 8,18 pour la foret aleatoire et **7,37 pour `agents v8`** », lu comme le poids du groupe | quantite de gabarit : le nul de a44 la reproduit a **7,32**, composantes a 99 et 98 pour cent ; la moitie « rarete de personne » tient, 0,241 contre 0,001 | a44 section 6, `a44-quantites.csv` |
| a34, E1, reponse en une ligne | 6.3 | « dans le tercile ou la rarete n'est PAS deductible [...] 21,8 et 20,3 pour cent contre 1,45 » | les rappels restent, **l'instrument tombe** : une partition placebo de neuf groupes aleatoires reproduit le gradient, ecart median **0,016** | a42 section 5, `a42-partitions.csv` |
| a35, E1, section 6 | 7, D5 | « `E1` perd **6,55 points** (0,7304 vers 0,6649) [...] deux fois ce que `B2` perdait » | **borne basse** : le contexte severe compte **132 a 144 items** contre **119** au facile ; la comparaison melange deux changements de signe oppose | `a47-contexte-regimes.csv` ; `a35_familles.imputer_par_famille` ligne 64 |
| a38, E1, section 4.4 lecture 4 | 1, D1 | « memes 150 personnes, memes items : **seule l'etiquette change** » | contraste de conditionnement ; la phrase contredit la ligne precedente du meme rapport | `a5_agents_locaux_gss.py` |
| a38, E2, section 4 | 3, D2 | « les quatre conditions riches de Stanford et C2 **exagerent l'ecart d'un facteur 1,6 a 3,2** » | quantite de **gabarit** : invariante a `0,00e+00` sous permutation intra camp sur 27 lignes, reproduite a 100,0 pour cent par le nul de a44 ; mesure les marges, pas les personnes | `a47-a38-invariance-facteur.csv` ; a45 section 2.1 pour le nul |
| a38, E3, section 4.4 lectures 2 et 3 | 2.3, D4 | « les trois predicteurs statistiques **qui recoivent l'etiquette** [...] `B2 argmax` a 1,01 » | **deux** predicteurs recoivent les onze attributs, a 1,03 et **1,24 excluant 1** ; `B2`, a 1,01, ne recoit aucune demographie et est l'analogue de C3 | `a2_baselines_gss.py` lignes 178 et 188 |
| a38, E4, section 4 et K4 | 4, D3 | « **les deux intervalles ne se recouvrent pas** » | ce n'est pas un test ; `p` de Holm **C2 1,0000 et C3 0,2640** ; les huit qui passent sont les six conditions de Stanford et les deux temoins `B0` | `a38-corrections.csv`, `K4 camp`, `p_holm_famille_complete` |
| a39, E1, lignes 47, 353, 448 | 1, D1 | « le seul couple ou [...] **seule l'etiquette bouge**, C2 contre C3 [...] un **fait d'ablation** » | contraste de conditionnement ; « elle se reproduit la ou elle est une ablation » perd son support | idem |
| a39, E2, meme passage | 8.1 | « moins 0,0067 [moins 0,0167 ; 0,0035], p ajuste 0,579, **c'est a dire rien** » | **non rejet** sur 150 personnes sans calcul de puissance : « nous ne pouvons ni confirmer ni infirmer l'egalite de Peng » | lecture de `a39-contrastes.csv` |
| a41, E1, section 2 et resume | 4.3, D6 | « sur les 450 cellules du **tercile non deductible** [...] 28,2 contre 13,8 » | le chiffre reste, l'instrument tombe avec a42 section 5 ; partition de remplacement, « rarete stable en vague 2 » | a42 section 5 |
| a41, E2, section 6 | 4.1 | « `agents composite` **moins 3,93 pt** » | penalite mesuree sur les **Survey Agents** ; `composite` a en plus l'entretien, donc perd moins : donner un encadrement, 0 a 3,93 points | a14 section 3.4 ; a41 applique deja la meme soustraction a `agents enquete`, ou elle est legitime |
| a42, E1, sections 2 et 6 | 1, D1 | « **l'ablation de l'etiquette**, quatrieme mesure independante » ; « C2, **le meme modele avec onze attributs demographiques** » | contraste de conditionnement ; « le meme modele conditionne sur onze attributs **au lieu** des 119 reponses » ; plus 0,1616 et plus 0,0327 inchanges | `a5_agents_locaux_gss.py` |
| a44, E1, sections 7.2 et 10 point 3 | 1, D1 | « C3, qui est **le meme modele et le meme run sans etiquette** » | contraste de conditionnement ; « le depart passe par le **conditionnement** et non par le moteur », ce que `B1` et `B3 foret` etablissent proprement | idem |
| a44, E2, sections 5.2 et 7.2 | 2 | « soit **7 pour cent du plancher humain** » ; seuil « gabarit » a 15 pour cent | **7 sous la segmentation qui contient l'ideologie, 18 a 27 sous genre x race x age, 64 a 70 pour `composite` dans les deux** ; quatre conditions sortent de la classe « gabarit » | `a47-chute-deux-segmentations.csv` |
| a44, E3, section 9.2 | 3, D2 | « **deux des six chemins** sont des quantites de gabarit » | trois lignes a ajouter, a38 **oui a 100,0 pour cent**, a37 oui par construction ; une seule quantite de personne subsiste parmi les piliers | `a47-a38-invariance-facteur.csv` |
| a44, E4, section 5.2 lecture 5 | 6 | « **4,91** [...] une reassignation arbitraire fait trois a cinq fois mieux que la vraie [...] le controle qui **leve la reserve** » | gain hongrois absolu de `v8` **0,0687**, sous le **0,0820** de `B0 tirage`, une population sans structure ; le rapport mesure un petit denominateur | `a47-plancher-reassignation.csv` |
| a44, E5, section 5.2 | 1.3 | « l'exactitude ne voit pas la distorsion », implicite depuis a1 | correlation **0,906** Pearson, **0,874** Spearman avec l'exactitude brute sur 13 conditions | `a47-correlation-chute-exactitude.csv` |
| a44, E6, section 7.2 | 1.5 | « `agents v6` \| **0,235** \| intermediaire » | **0,181** apres retrait des seize items recopies, un quart du signal apparent ; `v8`, C2 et `composite` inchanges | `a47-chute-hors-items-recopies.csv`, `a47-items-recopies.csv` |
| a44, E7, section 9.2 point 4 | D11 | « il rend **cette cellule du plan inutilisable** » (repli de `S_fin` a 150) | reserve valable pour le **nul** seulement ; la permutation n'emploie pas le nul, les lignes `S_fin` de C2 et C3 sont valides | lecture de `a44_mesures.py` lignes 397 a 428 |
| i1, E1, resume et section 4 | 10.2 | « l'exces de changement monotone est **integralement** une consequence comptable [...] il ne contient **aucune** information sur les personnes » | **non rejet a 1,35 ecart type** : nul 11,070 points, ecart type 0,498 sur 50 replicats, mesure 10,4 ; « indistinguable du nul, ecart 0,7 point pour un ecart type de 0,5 » | `i1-nul-remelange.csv` |
| i1, E2, section 4.3 | 10.1 | « cette avance ne vient pas du groupe » | l'artefact hors pli mesure sur T1, **0,0385**, vaut **28 pour cent de la chute de la foret et 43 pour cent de celle du predicteur primaire** ; reserve a porter, version corrigee non construite | `i1-auc-synthese.csv` ; `i1_previsibilite.scores_hors_pli` lignes 126 a 133. [PROBABLE] |
| i3, E1, section 2 et resume | 5, D12 | « de vraies personnes ne sont pas non plus libres : les humains ont un deficit de patrons de **moins 6,9 pour cent** et un exces de correlation de **0,042** » | ce ne sont pas des constantes humaines : sur Twin a effectif egal, **moins 2,78 pour cent et 0,0227**, rapports 2,5 et 1,9, soit **14 a 25 `s_0`** ; aucun seuil ne se transporte | `i3b-twin-reference.csv`, `i3-reference-humaine.csv`, `i3b-reference-par-taille.csv` |
| i3, E2, section 11 point 10 | 11.2, D10 | « les deux vont dans le meme sens pour v8, facteur 1,76 ici contre **1,62 en a38** » | 1,62 est celui de **C2** ; `v8` vaut **3,091** a 1 052 et **3,167** a 150 en a38 | `a47-a38-invariance-facteur.csv` |
| `MODELE-DU-MONDE.md`, E1, 10.4, 9.2, 5 | 1, D1 | « le meme modele, les memes personnes et les memes questions donnent 7 pour cent avec l'etiquette et 45 sans » ; « **l'ablation de l'etiquette : personne** » en tete de ce qui est libre | contraste de conditionnement ; la revendication de nouveaute est vide tant que R3 n'a pas rendu | `a5_agents_locaux_gss.py` ; `a47-chute-deux-segmentations.csv` |
| `MODELE-DU-MONDE.md`, E2, 10.3 et 10.4 | 2 | « 7 pour cent du plancher » ; « des gabarits de groupe **a 93 pour cent interchangeables** » | « 7 sous la segmentation qui contient l'ideologie, **18 a 27** sous celle qui ne la contient pas, 64 a 70 pour `composite` » ; le 93 pour cent est **retire** | `a47-chute-deux-segmentations.csv` |
| `MODELE-DU-MONDE.md`, E3, 10.4 | 3, D2 | « un **facteur d'amplification** de l'ecart entre camps de 1,62 contre 0,52 », cite comme pilier | quantite de gabarit ; **une seule** des quatre quantites citees comme piliers resiste au nul | `a47-a38-invariance-facteur.csv` |
| `MODELE-DU-MONDE.md`, E4, 9.1 | 4, D3 | « C2 a 1,62 contre C3 a 0,52, intervalles disjoints ; **huit tests passent Holm** » | les huit sont les six conditions de Stanford et les deux temoins ; **C2 1,0000 et C3 0,2640** | `a38-corrections.csv` |
| `MODELE-DU-MONDE.md`, E5, section 7 | 6.1, D7 | « le groupe pese jusqu'a **huit fois plus** » | quantite de gabarit, 7,37 reproduit a 7,32 ; le lift de personne resiste | a44 section 6 |
| `MODELE-DU-MONDE.md`, E6, 10.4 | 9, D9 | « deforme la loi humaine de consensus de **moins 2,2 a moins 12,4** » | pentes calculees sur **79 et 63 items** ; **moins 7,57** si la derive humaine sert d'abscisse | a37 section 3, `a37-agents-gss.csv` |
| `MODELE-DU-MONDE.md`, E7, 10.4 | 9.1 | « **83 contre 14 pour cent** de signal perdu au retrait du segment » | 83 pour un agent a etiquette seule, **76 et 77 pour une regression et une foret sur les memes attributs**, 14 pour un agent aux 119 reponses : suit le conditionnement | a43 sections 1 et 4.2 |
| `MODELE-DU-MONDE.md`, E8, 9.1 et 10.1 | 12.1, D8 | les rapports sources declares tombes | a25 et a28 n'ont **aucun errata** ; hors perimetre a47, liste en section 4 ci dessous | lecture de a25 et a28 |
| `MODELE-DU-MONDE.md`, E9, 9, 10, 10.5 | 10 | « preenregistre » | non verifiable de l'exterieur : `git ls-files` vide, aucun depot OSF ; ne pas ecrire le mot dans un preprint | a45 section 13.1 [VERIFIE par a45, non recalcule ici] |
| `ARBITRAGE.md`, E1, point 2 | 1, D1 | « la seule presence de l'etiquette fait la difference. **Six mesures independantes le disent** » | six mesures d'un **meme contraste confondu** ; le seul changement d'information vaut deja un facteur 2,0 de `B1` a `B2` | `a47-chute-deux-segmentations.csv` |
| `ARBITRAGE.md`, E2, point 2 | 2 | « il ne perd que **7 pour cent** du plancher humain » | 26,7 pour `v8` et 18,5 pour C2 sous genre x race x age | idem |
| `ARBITRAGE.md`, E3, point 3 | 3, D2 et D4 | « exagere l'ecart entre camps d'un facteur 1,6 a 3,2 **la ou toute methode statistique le reproduit fidelement** » | quantite de gabarit ; et `B1`, qui recoit les onze attributs, est a **1,24 excluant 1**, tandis que `B2` a 1,01 ne recoit aucune demographie | `a47-a38-invariance-facteur.csv` ; `a2_baselines_gss.py` |
| `ARBITRAGE.md`, E4, point 4 | 4.3, 5.1, 7 | « un sur trois contre un sur douze pour la regression » | trois reserves : comparateur faible (`PMM` ferait perdre quatre conditions sur six), asymetrie de frequence 0,109 contre 0,073, tercile non deductible invalide | `a42-stabilite.csv` ; a42 point 9 ; a42 section 5 |
| `ARBITRAGE.md`, E5, point 1 | 1.3 | « la bonne mesure d'un jumeau n'est ni sa fidelite moyenne ni sa dispersion » | la mesure qui separe partage **82 pour cent** de sa variance avec l'exactitude | `a47-correlation-chute-exactitude.csv` |
| `MOONSHOTS.md`, E1, section 4 et « ce que le dossier apporte deja » | 1 et 3, D1 et D2 | « le facteur **1,62 a modele constant sous etiquette** » ; « a38, l'ecart entre camps exagere d'un facteur 1,62 contre 0,52 » | ni « sous etiquette » (contraste de conditionnement) ni une quantite de personne (invariance exacte) ; l'argument reste valable pour un audit de **distributions** | `a5_agents_locaux_gss.py` ; `a47-a38-invariance-facteur.csv` |
| `MOONSHOTS.md`, E2, section 3, idee I3 | 5, D12 | « une signature a deux bords [...] ce qui manque est **un fichier reel contamine, pas une idee** » | ce qui manque aussi est la reference : elle varie d'un facteur 1,9 a 2,5 entre GSS et Twin a effectif egal | `i3b-twin-reference.csv` |

### Les douze contradictions de a45, et ou chacune est traitee

| # | traitee dans | statut |
|---|---|---|
| D1, « ablation » contre « contraste de conditionnement » | a29 E1, a38 E1, a39 E1, a42 E1, a44 E1, `ARBITRAGE` E1, `MODELE` E1, `MOONSHOTS` E1 | **appliquee** |
| D2, a38 absent du tableau des quantites de gabarit | a38 E2, a44 E3, `MODELE` E3, `MOONSHOTS` E1 | **appliquee** |
| D3, Holm juxtapose a C2 et C3 | a38 E4, `MODELE` E4 | **appliquee** |
| D4, `B2 argmax` presente comme recevant l'etiquette | a38 E3, `ARBITRAGE` E3 | **appliquee** |
| D5, regimes de a35 a tailles de contexte differentes | a35 E1 | **appliquee** |
| D6, tercile non deductible invalide par a42 | a41 E1, a34 E1 | **appliquee** |
| D7, rapport groupe sur personne reproduit par le nul | a31 E1, `MODELE` E5 | **appliquee** |
| D8, a25 et a28 sans errata | `MODELE` E8 signale ; **a25 et a28 ne sont pas dans le perimetre du chantier** | **signalee, non appliquee a la source** |
| D9, pentes de a37 sans denominateur | `MODELE` E6 ; **a37 n'est pas dans le perimetre du chantier** | **appliquee dans la synthese, pas a la source** |
| D10, i3 attribue a `v8` le facteur de C2 | i3 E2 | **appliquee** |
| D11, `S_fin` a 150 personnes | a44 E7 | **appliquee** |
| D12, la bande humaine de i3 sur Twin | i3 E1, `MOONSHOTS` E2 | **appliquee** |

---

## 3. Convention de lecture proposee pour tout tableau du dossier

Trois classes, a nommer explicitement a cote de chaque chiffre publie.

1. **Quantite de gabarit** : fonctionnelle de la table (segment ou camp) x modalite,
   invariante sous permutation des personnes a l'interieur du segment. Ratio inter et ratio
   intra de a1, lifts de segment et rapport groupe sur personne de a31, facteur
   d'amplification de a38, unanimite et Gini Simpson de a30, pente de consensus de a37. Toutes
   sont reproduites par un generateur sans structure individuelle.
2. **Quantite de personne** : chute d'exactitude sous permutation intra segment (a44),
   correlation par personne de a29, exces sur les raretes stables de a42, lift de personne de
   a31. Le generateur nul echoue dessus.
3. **Quantite mixte ou non testee** : a28 test 3, a33, la reassignation hongroise tant que son
   plancher n'est pas publie a cote.

**Regle.** Une quantite de gabarit ne se publie jamais seule ; elle se publie a cote d'une
quantite de personne et du plancher humain. C'est la formulation que `MODELE-DU-MONDE.md`
10.4 adopte deja pour le gonflement et l'ecrasement, et qu'il faut etendre au facteur
d'amplification.

---

## 4. Les passages a reecrire au matin, et de quoi ils dependent

**Ces documents n'ont recu qu'un errata en tete ; leur corps n'a pas ete touche.**
L'orchestrateur s'en charge, avec les resultats des runs de la nuit. Les numeros de ligne
sont ceux des fichiers au 9 septembre 2026, **avant** l'insertion des errata de ce chantier,
c'est a dire tels que a45 les cite.

### MODELE-DU-MONDE.md

| passage | ce qu'il faut ecrire | depend de |
|---|---|---|
| 10.4, « le meme modele, les memes personnes et les memes questions donnent 7 pour cent du plancher avec l'etiquette et 45 pour cent sans » | « un agent conditionne sur onze attributs dont l'etiquette est a 7 pour cent du plancher sous la segmentation ideologique et 18 sous une segmentation qui ne la contient pas ; un agent conditionne sur les 119 reponses de la personne est a 45 ; **les deux facteurs sont confondus** » | **run R3** pour la part propre de l'etiquette ; le reste est ecrit et mesure |
| 10.4, « un facteur d'amplification de l'ecart entre camps de 1,62 contre 0,52 » | a deplacer dans la phrase des quantites de gabarit, avec le gonflement et l'ecrasement | rien, mesure |
| 10.3, « des gabarits de groupe a 93 pour cent interchangeables » | **a supprimer** | rien, mesure |
| 10.3, « v8 et C2 perdent 2,5 et 2,4, soit 7 pour cent du plancher » | ajouter « sous la segmentation ideologique ; 18 a 27 pour cent sous genre x race x age » | rien, mesure |
| 10.3, « une reassignation arbitraire fait 4,9 fois mieux que la vraie chez v8 » | « le gain de l'appariement optimal chez v8, 0,069, est au niveau du gain obtenu sur une population sans structure, 0,082 » | rien, mesure |
| 9.1, « huit tests passent Holm sur la famille de 52 » | « les huit qui passent sont les six conditions de Stanford et les deux temoins ; C2 et C3 sont a 1,00 et 0,26 » | rien, mesure |
| 10.4, « moins 2,2 a moins 12,4 » | ajouter les denominateurs, 79 et 63 items, et la variante a derive humaine, moins 7,57 | rien, lu dans a37 |
| 10.4, « 83 contre 14 pour cent de signal perdu » | ajouter « 76 et 77 pour une regression et une foret sur les memes attributs » | rien, lu dans a43 |
| section 7, « le groupe pese jusqu'a huit fois plus » | ajouter « quantite de gabarit, reproduite a 7,32 par un generateur sans structure » | rien, lu dans a44 |
| section 5, « l'ablation de l'etiquette [...] : personne » | « le placebo d'etiquette : personne, **nous compris jusqu'au run R3** » | **run R3** |
| 10.5, verrou deux | le placebo d'etiquette passe **verrou numero un**, avant la comparaison appariee des minorites | decision de redaction |
| toutes les mentions de « preenregistre » dans un texte destine a l'exterieur | a retirer tant que rien n'est depose sur OSF ni committe | **depot OSF ou commit de `resultats/`** |

### ARBITRAGE.md

| passage | ce qu'il faut ecrire | depend de |
|---|---|---|
| point 2, « la seule presence de l'etiquette fait la difference. Six mesures independantes le disent » | « remplacer les 119 reponses de la personne par onze attributs dont l'etiquette fait la difference ; six mesures **du meme contraste**, dont les deux facteurs sont confondus » | **run R3** |
| point 2, « il ne perd que 7 pour cent du plancher humain » | ajouter la segmentation, et le 18 a 27 sous genre x race x age | rien, mesure |
| point 3, « il exagere l'ecart entre camps d'un facteur 1,6 a 3,2 la ou toute methode statistique le reproduit fidelement » | « il exagere les **marges par camp** d'un facteur 1,6 a 3,2, quantite de gabarit ; la regression sur les memes attributs est deja a 1,24, intervalle excluant 1 » | rien, mesure |
| point 3, « C'est l'etiquette ideologique, pas l'etiquette demographique, qui le fait » | tenable sur `v6` et `v7`, qui ont l'etiquette demographique sans l'ideologie et sous reproduisent l'ecart ; a garder **avec** cette justification et non avec le couple C2 contre C3 | rien, lu dans a38 section 4 |
| point 4, « un sur trois contre un sur douze pour la regression » | mettre `PMM k=10` en comparateur principal et nommer les quatre conditions qui perdent | **verrou cinq**, zero appel, non fait |
| point 1, « la bonne mesure n'est ni la fidelite moyenne ni la dispersion » | ajouter « la mesure qui separe partage 82 pour cent de sa variance avec l'exactitude ; ce qui separe est le lieu ou elles divergent » | rien, mesure |
| « Mon avis », ordre des nuits | le placebo d'etiquette passe avant la comparaison appariee sur les gens rares | decision d'arbitrage |

### Rapports hors perimetre du chantier a47

Trois errata restent a ecrire et **n'ont pas ete inseres**, faute de mandat sur ces fichiers.

| rapport | errata attendu | source |
|---|---|---|
| `a25-items-sensibles-au-mode.md` et `a28-trois-tests-decisifs.md` | trois lignes en tete renvoyant a a38 sections 2 et 3 : la these « la simulation devie la ou les humains se surveillent » est tombee, et le seul effet distinguable de a25 etait C2, une condition sur treize dans une famille non corrigee | a45 section 12.1, contradiction D8 |
| `a37-consensus-liberal-et-simulation.md` | le nombre d'items a cote de chaque pente, 79 chez les humains, 63 chez `v8`, 46 chez C2, et la variante `pente_sur_derive_humaine` a moins 7,57 ; ne jamais comparer un compte d'unanimite entre 150 et 1 052 personnes ; et le Gini Simpson est une quantite de gabarit | a45 sections 7.1 et 7.2, contradiction D9 |
| `a30-variete-interne-des-camps.md` | l'unanimite est une fonctionnelle de la table (camp, modalite), reconnue par a44 9.2 mais non portee par a30 | a45 section 7.2 |

---

## 5. Ce que je n'ai pas pu verifier

1. **Je n'ai relance aucun script existant en entier.** Les trois scripts de a47 reimportent
   `a44_commun`, `a44_mesures`, `a28_test1_mode`, `a38_mesures`, `a30_commun` et
   `a2_baselines_gss` et reproduisent leurs chiffres publies au millieme, ce qui valide la
   chaine ; mais `a44_mesures.py`, `a38_tests.py` et `a35_imputation.py` n'ont pas ete
   rejoues, donc je n'ai pas verifie que tous leurs CSV publies correspondent a la derniere
   version de leurs scripts.

2. **Le generateur nul de a44 n'a pas ete repasse sur a38 par moi.** J'ai etabli l'invariance
   exacte sous permutation intra camp, `0,00e+00` sur 27 lignes, ce qui suffit a classer le
   facteur d'amplification en quantite de gabarit. La reproduction a 100,0 pour cent par le
   nul est celle de a45 section 2.1, 30 replicats, que je cite sans l'avoir recalculee. Le
   nul est un test plus fort que l'invariance et il devrait etre passe sur a38, a37 et a30
   dans le meme script que a44.

3. **Aucune segmentation intermediaire n'a ete essayee.** J'ai mesure trois segmentations,
   deux qui contiennent l'ideologie et une qui ne la contient pas. a45 en a mesure neuf. La
   question « a partir de quelle part d'information ideologique le chiffre bascule » n'est pas
   traitee, et il n'existe pas de segmentation qui contienne l'ideologie **sans** contenir
   l'axe de l'invite, puisque c'est le meme.

4. **La chute sous permutation n'a pas d'intervalle dans mes tableaux.** a45 en publie un,
   300 tirages bootstrap apparies, et conclut que les intervalles sont etroits et qu'aucune
   conclusion ne bouge, y compris sur les 150 personnes. Je n'ai pas reproduit ce calcul :
   il reste a faire avant publication, y compris sous la segmentation sans ideologie.

5. **La liste des items recopies n'est pas identique a celle de a45.** Mon balayage porte sur
   toutes les conditions, retest humain compris, et remonte seize items a 0,95 ou plus ; a45
   en remonte onze sur dix conditions. Les quatre items d'etat civil recopies par `v6` seul
   sont les memes, et l'effet sur `v6` est du meme ordre, 0,235 vers 0,181 chez moi contre
   0,235 vers 0,177 chez a45. La difference vient du perimetre de la liste, pas d'un
   desaccord.

6. **Le plancher de la reassignation hongroise n'existe pas sur 150 personnes.** `B0 tirage`
   n'a ete calcule qu'a 1 052. La comparaison « gain de v8 sous le gain d'une population sans
   structure » n'est donc etablie que pour `v8` ; pour C2 elle est plausible et non mesuree.

7. **Je n'ai pas construit `C2 tirage` ni `C3 tirage`.** L'objection 3.4 de a45, le regime de
   decodage, reste entiere : toutes les conditions a modele de langage sont evaluees en
   argmax, et le passage argmax vers tirage fait tomber le ratio inter de `B1` de 1,48 chez
   les couples statistiques de a35. Les traces contiennent les distributions, le test coute
   zero appel de modele, il n'a pas ete fait ici.

8. **Je n'ai pas borne l'artefact hors pli de i1 sur `L2` et sur `F`.** L'errata E2 de i1
   porte le mecanisme et l'ordre de grandeur, 28 et 43 pour cent des chutes concernees ; la
   version corrigee demande de refaire les cinq plis avec un estimateur different et n'a pas
   ete construite. L'errata est marque [PROBABLE].

9. **La penalite propre de `agents composite` sous retrait de bloc n'est pas mesurable ici.**
   L'errata E2 de a41 porte sur l'attribution de la penalite, pas sur un chiffre de rechange.
   Il faudrait chercher dans le paquet OSF un fichier de la condition « retrait par bloc » ;
   a17 le signalait deja, ce n'est toujours pas fait.

10. **Rien sur Twin par mes propres calculs.** Les chiffres de l'errata E1 de i3 sont lus dans
    `i3b-twin-reference.csv` et `i3b-reference-par-taille.csv`, pas recalcules sur les donnees
    brutes de Twin. La replication de la chute sous permutation sur Twin, verrou trois de
    `MODELE-DU-MONDE.md` 10.5 a zero appel, n'existe toujours pas, et c'est ce qu'un relecteur
    demandera apres avoir lu la section 1 ci dessus : si le chiffre depend de la segmentation
    sur le GSS, il faut savoir s'il depend aussi du jeu.

11. **Je n'ai pas verifie l'horodatage des preenregistrements.** L'errata E9 de
    `MODELE-DU-MONDE.md` reprend le constat de a45 section 13.1 sans le refaire ; je n'ai
    execute ni `git ls-files` ni `stat` sur les cinq fichiers.

12. **Je n'ai pas ouvert les papiers tiers.** Yuan, Peng, Ahn, van Buuren, Rennard, von der
    Heyde : je prends pour exactes les citations des rapports. Mes corrections portent sur ce
    que le dossier fait de ces lectures, jamais sur leur fidelite.
