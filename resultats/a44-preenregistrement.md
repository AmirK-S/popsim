# a44, preenregistrement : le generateur nul conditionnellement independant de Yuan, applique a nos populations simulees

**Ecrit le 8 septembre 2026 a 15 h 46 CEST, soit 13 h 46 UTC.** Depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`, branche `chore/restauration-arborescence`.

**Etat au moment de l'ecriture.** Aucun calcul de a44 n'a ete lance. Aucun script
`analyses/a44_*.py` n'existe. Ont ete faits avant cette page, et rien d'autre : la lecture
de `MODELE-DU-MONDE.md` sections 2 et 7, de `corpus/lecture-complete/08-veille-ete-2026.md`,
du texte integral de Yuan (arXiv 2607.02368 v3, telecharge et converti dans le scratchpad),
des rapports `a1`, `a18`, `a23`, `a31`, et des scripts `a1_double_distorsion.py`,
`a18_decomposition_traces.py`, `a31_commun.py`, `a29_commun.py`, `a28_commun.py`,
`a2_commun.py`, `a35_commun.py` ; et la verification que les caches `/tmp/a25-matrices.pkl`,
`/tmp/a28-foret.npy` et `/tmp/a35-methodes.pkl` existent et contiennent les matrices
attendues, dont `PMM k=10`. Aucune mesure de a44 n'a ete regardee.

---

## 1. La question, en une phrase

Le gonflement inter de 8,16 (C2, axe ideologie) et de 5,9 (v8, six axes) et l'ecrasement
intra de 0,365 sont ils reproduits par un generateur qui n'a **aucune** structure
individuelle, c'est a dire qui tire chaque reponse independamment dans la loi de l'item a
l'interieur du segment de la personne ?

Si oui, la population simulee est un gabarit de groupe au sens exact de Yuan : chaque agent
est un tirage dans le gabarit de son segment, et la mesure ne porte pas sur la simulation
mais sur les marginales. Si non, et si l'ecart est du cote d'une structure supplementaire,
la population simulee porte quelque chose que l'etiquette seule n'a pas.

---

## 2. Ce que Yuan fait, et ce que nous transposons

**Chez Yuan (2607.02368 v3, equation 2, section 5).** Le generateur nul tire
`X_ij ~ N(mu_chapeau_{j,g}, sigma_chapeau_{j,g})`, tronque puis arrondi sur l'echelle a
cinq points, sans trait latent, sans covariance entre items, sans dependance
autoregressive. Les parametres sont estimes sur les statistiques d'item empiriques du
modele lui meme, groupe par groupe. Le faux jeu passe ensuite dans **la chaine de mesure
identique**. Resultat : 97,2 / 57,6 / 83,2 pour le nul contre 94,6 / 55,2 / 83,7 pour le
vrai GPT-4o, sous ordre fixe, ordre aleatoire et realignement.

**Chez nous.** Les reponses ne sont pas sur une echelle a cinq points comparable d'un item
a l'autre ; 149 items du GSS, nomenclatures fermees de tailles differentes, une partie
nominale. La loi normale tronquee de Yuan est donc remplacee par la **loi multinomiale
empirique de l'item a l'interieur du segment**, ce qui est la version categorielle exacte
de la meme idee : memes marginales par item et par groupe, tirages independants d'une
cellule a l'autre.

Formellement, pour une condition `M` de matrice `R` (n personnes x 149 items), une
segmentation `S` et pour chaque item `j` :

```
p_chapeau_{j,g}(k) = part des personnes du segment g, repondant a j dans M,
                     qui donnent la modalite k
X_ij ~ Multinomiale(p_chapeau_{j, g(i)}),  independamment sur i et sur j
```

**Regles fixees d'avance.**

1. **Masque conserve.** Une cellule vide ou refusee dans `M` reste vide dans le nul. Le
   nombre de cellules exploitables par item et par personne est donc identique entre la
   population et son nul, ce qui interdit qu'un ecart vienne d'un effectif different.
2. **Segments a effectif insuffisant.** Un segment de moins de 5 repondants observes sur un
   item voit sa loi remplacee par la loi de l'item sur toute la condition. La regle est
   posee avant execution ; sa sensibilite (seuil 2 et seuil 10) est declaree descriptive.
3. **Deux segmentations, declarees a l'avance.**
   - `S_fin` : ideologie politique x genre x age, le segment le plus fin que l'invite
     demographique porte reellement.
   - `S_ideo` : ideologie politique seule, l'axe que a1 section 4 et a23 designent comme le
     seul qui porte le gonflement.
4. **Nombre de replicats du nul : R = 200**, graine `20260908`. La valeur publiee pour le
   nul est la moyenne sur les 200 replicats ; la bande est le percentile 2,5 a 97,5 sur les
   replicats.
5. **Le nul n'est pas re-normalise.** Ses ratios inter et intra sont rapportes au meme
   denominateur que ceux de la population reelle, les humains de la vague 1 sur le meme
   perimetre, comme a1 le fait.

---

## 3. Conditions, perimetres, items

**Cadre de mesure : celui de a25 / a28 / a29, 1 052 personnes x 149 items**, matrices
relues du cache `/tmp/a25-matrices.pkl` et `/tmp/a28-foret.npy`, plus `PMM k=10` relu de
`/tmp/a35-methodes.pkl`. Rien n'est recalcule, aucun script existant n'est modifie, aucun
appel de modele.

| condition | perimetre naturel | role |
|---|---|---|
| humains vague 1 | 1 052 | reference et denominateur |
| humains vague 2 | 1 052 | plancher, les memes personnes reinterrogees |
| agents composite | 1 052 | Stanford, riche |
| agents entretien (v3) | 1 052 | Stanford, riche |
| agents enquete | 1 052 | Stanford, riche |
| agents demographiques (v6) | 1 052 | Stanford, etiquette |
| agents v7 | 1 052 | Stanford, persona |
| agents v8 | 1 052 | Stanford, etiquette, le 5,9 de a1 |
| C2 | 150 | notre agent a etiquette, le 8,16 de a23 |
| C3 | 150 | notre agent sans etiquette |
| B1 argmax | 1 052 | regression sur demographies |
| B2 argmax | 1 052 | plus proches voisins sur contexte |
| PMM k=10 | 1 052 | appariement sur moyenne predite |

`B0 mode`, `B0 tirage` et `B3 foret` sont mesurees **en descriptif**, hors de toute famille
de tests : `B0 tirage` est deja un generateur nul non conditionne, et sa distance a son
propre nul conditionne est un controle de lecture, pas une hypothese.

Les mesures a 1 052 et a 150 ne sont **jamais** comparees entre elles dans un test ; C2 et
C3 sont compares entre eux et a la vague 2 restreinte aux memes 150 personnes.

---

## 4. Les quantites mesurees, sur la population et sur son nul

| | quantite | definition | ou elle vient |
|---|---|---|---|
| **Q1** | ratio inter | somme sur items du terme inter de Gini Simpson sans biais, divisee par celle des humains vague 1 | a1, `decomposer` / `sommes_dispersion_rapide` |
| **Q2** | ratio intra | idem, terme intra | a1 |
| **Q3** | patrons distincts | nombre moyen de lignes distinctes sur 20 sous ensembles de 10 items tires une fois, graine fixe, partages par toutes les conditions | nouveau, motive par les 19 patrons sur 929 de Wang et al. |
| **Q4** | correlation inter items brute | moyenne des \|rho de Spearman\| sur les paires d'items ordinaux | nouveau, transposition de la matrice de correlation de Yuan |
| **Q5** | correlation inter items residualisee | idem apres retrait, item par item, de la moyenne de rang du segment de la personne | **quantite primaire du verdict** |
| **Q6** | rapport groupe sur personne | lift de rarete de segment divise par lift de rarete de personne, sur les fausses raretes | a31, H2b sur H1b |
| **Q7** | rappel des cellules rares | rappel minoritaire au seuil de 10 pour cent | a29 |

**Q5 est la quantite primaire du verdict**, et c'est un choix de methode a declarer :
le generateur nul tire les items independamment **a l'interieur du segment**, donc son
esperance sur Q5 est nulle a l'erreur d'echantillonnage pres, alors que sa Q4 reproduit
exactement la part de correlation que le segment induit. Q5 est donc la transposition
directe du critere de Yuan, « une structure interne a un seul jeu de reponses que le gabarit
de groupe ne peut pas produire ». Q1, Q2, Q3, Q6 et Q7 sont secondaires et servent a dire
**quelles** de nos quantites publiees sont des quantites de gabarit.

**Codage de Q4 et Q5.** Items marques ordinaux par les auteurs de Stanford
(`a25_commun.ORDINAUX`), codes 0..K-1 dans l'ordre de la nomenclature, rangs calcules sur
les personnes observees de l'item. Paires retenues : celles ou au moins 30 personnes
repondent aux deux items. Moyenne des valeurs absolues, pour qu'un item inverse ne compense
pas un item direct.

---

## 5. La distance au nul, et son intervalle

Pour chaque condition `M`, chaque segmentation et chaque quantite `Q` :

```
d(M, Q) = Q(M) - moyenne sur les 200 replicats de Q(nul de M)
z(M, Q) = d(M, Q) / ecart type des 200 replicats
```

**Intervalle de confiance a 95 pour cent par bootstrap sur les personnes, 1 000 tirages**,
le meme tirage etant applique a la population et a ses replicats nuls, ce qui rend le
contraste apparie. Le bootstrap porte sur les personnes et jamais sur les cellules : deux
reponses d'une meme personne ne sont pas independantes.

**Verdict declare, quantite primaire Q5, segmentation `S_fin` :**

- **gabarit de groupe** si l'intervalle de `d` contient zero ;
- **porteur de personne** si l'intervalle exclut zero **par le haut** ;
- **anti structure** si l'intervalle exclut zero par le bas, cas non prevu, a signaler tel
  quel s'il survient.

**Famille de tests primaire declaree** : `d(M, Q5)` sous `S_fin` pour les 13 conditions du
tableau de la section 3, soit **13 tests**, corriges par **Holm**, valide sans hypothese sur
la dependance. Benjamini Hochberg rapporte a cote. Les `p` sont bilateraux, lus sur la
position de zero dans la distribution bootstrap ; ils ne descendent pas sous 1/1 000.

**N'entrent dans aucune famille et sont des descriptions** : la segmentation `S_ideo` ;
Q1, Q2, Q3, Q4, Q6, Q7 ; les trois conditions descriptives `B0 mode`, `B0 tirage`,
`B3 foret` ; les sensibilites de seuil de segment ; les valeurs `z` ; la figure.

---

## 6. Les trois proprietes de Yuan, transposees

**Ce qui n'est pas possible, et il faut le dire d'entree.** Yuan perturbe **l'ordre de
presentation des items** dans le contexte de chaque instance. Chez nous, permuter l'ordre
des items dans l'invite de C2 ou de C3 **demanderait de relancer 22 350 appels par
condition**. Nos traces sont a ordre fixe, et il n'existe aucune facon de reconstruire une
trace a ordre aleatoire a partir d'une trace a ordre fixe. Le test d'ordre de Yuan est donc
**hors de portee de a44**, il reste ce que la veille section 4.1 chiffre a une nuit courte
d'appels. a44 ne le fera pas et ne pretendra pas l'avoir fait.

**Ce qui le remplace : la permutation des personnes a l'interieur du segment.** Le
raisonnement est le meme que celui de Yuan, applique a l'autre axe de la matrice. Si les
agents sont des gabarits de groupe, alors a l'interieur d'un segment les reponses sont
echangeables entre personnes, et permuter qui recoit quelle reponse simulee **ne change
rien** a l'exactitude. Si les agents portent la personne, l'exactitude chute.

Trois termes, dans l'ordre de Yuan :

| terme de Yuan | notre terme | ce qu'on mesure |
|---|---|---|
| **FO**, ordre fixe partage | **assignation vraie** | exactitude par personne, telle que a2 la mesure |
| **RO**, ordre propre a chaque instance | **permutation intra segment** | exactitude moyenne sur 200 permutations aleatoires des personnes a l'interieur de leur segment |
| **RO-BTSP**, realignement sur un ordre partage | **reassignation optimale intra segment** | exactitude sous l'appariement hongrois qui maximise l'accord a l'interieur de chaque segment |

Le troisieme terme est **le maillon faible de la transposition** et il est declare
descriptif : le realignement de Yuan est tire au hasard 2 000 fois et n'exploite pas les
donnees, alors que l'appariement hongrois les exploite ; il borne donc par le haut ce qu'un
gabarit de groupe peut atteindre en choisissant son alignement apres coup, il ne l'estime
pas. Il est publie avec cette reserve ecrite a cote et ne fonde aucun verdict.

**Reference : les humains de la vague 2**, dont la chute sous permutation intra segment est
le plancher humain de cette mesure.

**Un fait arithmetique a verifier numeriquement et non a supposer** : le ratio inter de a1
est **exactement invariant** sous permutation des personnes a l'interieur d'un segment,
puisque la table de contingence (segment, modalite) ne bouge pas. Le script le verifie et
s'arrete si l'ecart depasse `1e-12`. C'est le point de Yuan sous sa forme la plus nue : la
quantite qui porte notre resultat le plus fort ne peut pas, par construction, distinguer une
personne d'une autre a l'interieur de son segment.

**Segmentation de la permutation** : `S_fin` en principal, `S_ideo` en descriptif.

---

## 7. Predictions ecrites avant le calcul

Ce sont des paris, ils sont la pour etre perdus.

| | prediction | statut si elle tombe |
|---|---|---|
| **P1** | C2 et v8 sont indistinguables de leur generateur nul sur Q1 et Q2 : le 8,16 et le 5,9 sont reproduits a l'interieur de la bande du nul | notre gonflement est une quantite de marginales, pas de simulation |
| **P2** | Les conditions riches, composite et entretien, s'ecartent du nul sur Q5 par le haut, avec un intervalle excluant zero | elles portent une structure individuelle que l'etiquette n'a pas |
| **P3** | C2 ne s'ecarte pas du nul sur Q5 ; C3 s'en ecarte | l'etiquette est ce qui reduit l'agent au gabarit |
| **P4** | Les humains de la vague 1 et de la vague 2 s'ecartent tres largement du nul sur Q5 | le critere separe bien, la mesure n'est pas creuse |
| **P5** | La chute d'exactitude sous permutation intra segment est proche de zero pour C2 et v8, et nettement positive pour les humains vague 2 et pour les conditions riches | l'agent a etiquette est un gabarit au sens operationnel |
| **P6** | Q3, le nombre de patrons distincts, est **plus grand** dans le nul que dans la population simulee | l'agent est moins varie que le tirage independant dans son propre gabarit, ce qui serait un ecart au nul dans la direction opposee a la structure |

**P6 merite d'etre lue avant les resultats** : si elle se realise, le verdict « gabarit de
groupe » est trop genereux pour nos agents a etiquette, qui seraient alors **en deca** du
generateur nul, c'est a dire plus pauvres qu'un tirage sans aucune structure. Yuan n'a pas
ce cas parce que son generateur reproduit ses ecarts types d'item ; le notre reproduit les
marginales exactes, donc l'ecart ne peut venir que de la dependance entre items.

---

## 8. Ce qui est fige avant execution

- Graine unique `20260908`, employee pour les replicats nuls, les permutations, le
  bootstrap et le tirage des sous ensembles d'items de Q3.
- `R = 200` replicats nuls, `B = 1 000` tirages bootstrap, `P = 200` permutations.
- Quatre coeurs, variables `OMP_NUM_THREADS` et suivantes posees avant l'import de numpy.
- Lecture seule sur `data/`. Aucun fichier existant modifie. Sorties uniquement dans
  `analyses/a44_*.py`, `resultats/a44-*.csv`, `resultats/a44-figure-generateur-nul.png`
  et `.svg`, `resultats/a44-generateur-nul.md`.
- Deux controles bloquants, executes a chaque lancement :
  1. le generateur nul alimente par une condition et re-mesure sur les **marginales par
     item et par segment** doit redonner ces marginales a l'erreur d'echantillonnage pres,
     ecart moyen inferieur a 0,01 sur les 200 replicats ;
  2. le ratio inter sous permutation intra segment doit etre egal au ratio inter vrai a
     `1e-12` pres.
  Le script s'arrete si l'un des deux echoue.

---

## 9. Ce que a44 ne pourra pas dire

- Rien sur l'ordre des items, cf. section 6.
- Rien sur Twin-2K-500 ni sur les jeux hors GSS : le perimetre est celui de a25 / a28.
- Rien sur la cause de l'ecart au nul quand il existe : Q5 dit qu'il y a de la structure,
  pas d'ou elle vient.
- Rien qui compare une condition a 1 052 personnes a une condition a 150.
