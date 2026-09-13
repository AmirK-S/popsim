# C7 — Le nul corrigé à remplissage marginal : les réplicats, enfin en CSV

statut: courant
mandat: émettre en CSV les réplicats du nul corrigé à remplissage marginal (tableau 1, rho 0,974 [0,950 ; 0,993]), qui n'existaient dans aucun fichier du dépôt — défaut D8, tâche T1b
agent: Claude Opus 5, Anthropic
ecriture: resultats/c7-nul-corrige-marginal.csv, resultats/c7-nul-corrige-marginal.md, analyses/c7_temoin_verite_appariee.py
lecture_seule: tout le reste
interdits: appel payant sans GO, réseau, commit sur master, arrière-plan
cecite: je n'ai lu ni le manuscrit LaTeX compilé, ni `analyses/figures_article.py`, ni les travaux parallèles T1a / T2 / recensement en cours pendant cette tâche
cout_reel_usd: 0.00

---

## 1. Ce qui était cassé, et ce qui ne l'était pas

Le défaut D8 (`resultats/relecture-fond-2026-09-13.md`) est un défaut de **reproductibilité**,
pas de fond. Le couple de chiffres qui fonde la réfutation de la prédiction (b) — donc le titre
de l'article — était publié au tableau 1 sans qu'aucun CSV du dépôt ne porte les réplicats dont
il est tiré. Le script qui les produit n'écrivait que sur la sortie standard.

**Le chiffre, lui, est juste.** Il se reproduit au chiffre près (§3). C'est sa trace qui
manquait.

## 2. Le script, identifié et rejoué

`analyses/c7_temoin_verite_appariee.py` — récupéré le 12 septembre 2026 d'un scratchpad de
session (`audit_contre_nul.py`, jamais commité) et intégré sous ce nom, comme le dit son en-tête
de provenance. C'est bien lui qui produit le chiffre du tableau 1.

Il construit le **nul à exactitude-vérité appariée** : pour chaque personne, exactement le même
nombre de cellules exactes **contre la vérité** que le prédicteur réel, mais les **positions**
tirées au hasard. C'est le nul qui répond à l'objection testée (« les deux axes sont deux
fonctions monotones de la même marge d'exactitude »), parce qu'il **conserve** la grandeur dont
l'objection affirme qu'elle explique tout, et ne détruit que le choix des positions exactes.

Dépendance : le cache `C7_NUL_CACHE` (défaut `/tmp/c7-nul-corrige-baselines-60.pkl`), construit
par `analyses/c7_nul_corrige.py`. Il était présent ; aucun recalcul de baseline n'a été
nécessaire.

**Rejeu à l'identique, script non modifié, `NREP=20` :**

```
=== NUL A EXACTITUDE-VERITE APPARIEE, remplissage marginal (20 replicats) ===
rho moyen=+0.9741 mediane=+0.9720 p5=+0.9500 p95=+0.9934 min=+0.9301 max=+1.0000
rho reel observe = 0.9650 -> le depasse-t-il ? False
```

Le tableau par configuration se reproduit lui aussi ligne pour ligne (JSON Persona - GPT4.1 :
exactitude 0,5904, chute +0,16116, top-1 31,624 % ; B0 tirage : 0,4323, +0,01035, 0,154 %),
identique à `resultats/audit-renversement-2026-09-12.md` §1.3. Coût : 159 s, aucun appel payant.

## 3. Le critère d'arrêt est satisfait — exactement

| grandeur | tableau 1 / audit | rejeu | verdict |
|---|---|---|---|
| rho moyen | 0,9741 | **0,9741** | identique |
| médiane | 0,9720 | **0,9720** | identique |
| 5ᵉ centile de la loi nulle | 0,9500 | **0,9500** | identique |
| 95ᵉ centile de la loi nulle | 0,9934 | **0,9934** | identique |
| rho réel observé le dépasse ? | non | **non** | identique |

**Aucun écart, à aucune décimale.** Le chiffre parti dans la lettre à Columbia tient. La
réfutation de la prédiction (b) tient, et le titre de l'article avec elle.

## 4. Réserve sur le nombre de réplicats — à lire avant toute republication

La tâche T1b du plan prescrit `NREP=100` **et** attend rho moyen ≈ 0,9741. **Les deux sont
incompatibles.** Le chiffre publié vient d'un run à **20** réplicats, pas 100.

J'ai fait tourner les deux. La série à 20 réplicats est un **préfixe bit-exact** de la série à
100 (les graines sont indexées par réplicat, `[GRAINE,999,r,graine_nom(nom),0|1]`, donc les 20
premiers réplicats sont les mêmes objets) — vérifié, écart maximal 0,0. Mais les agrégats
diffèrent :

| variante | n | rho moyen | médiane | centile 5 | centile 95 |
|---|---|---|---|---|---|
| **marginal** | **20** | **0,9741** | 0,9720 | **0,9500** | **0,9934** |
| marginal | 100 | 0,9799 | 0,9816 | 0,9510 | 0,9930 |
| uniforme | 20 | 0,9815 | 0,9860 | 0,9580 | 0,9930 |

La bande survit au passage à 100 (elle arrondit à [0,951 ; 0,993] au lieu de [0,950 ; 0,993]).
**La moyenne, non** : 0,974 devient **0,980**, un écart à la 3ᵉ décimale.

Et 0,980 est précisément le nombre-piège de cette tâche. Un agent qui suivrait T1b à la lettre
publierait 0,980 en croyant confirmer 0,974, et ce 0,980-là serait **encore un troisième
0,980**, distinct des deux autres du dépôt. Le critère d'arrêt de T1b est mal calibré, pas le
résultat. **Ce qui fait foi pour le tableau 1 est la série à 20 réplicats**, et elle seule : le
CSV la marque `fait_foi_tableau1=oui`. Les trois séries sont dans le fichier pour que la
distinction soit vérifiable, pas pour laisser le choix.

Décision à porter au responsable, hors de mon périmètre : soit le tableau 1 garde 0,974 en
déclarant n = 20, soit il passe à 100 réplicats et **le chiffre change**. Je n'ai touché à rien.

## 5. Les trois nuls du dépôt, à ne jamais confondre

C'est le cœur du piège. Trois séries voisines, quatre nombres commençant par 0,98, une seule qui
fait foi.

| série | fichier | construction | n | rho moyen | centiles 5-95 |
|---|---|---|---|---|---|
| **nul corrigé, remplissage marginal** | **`resultats/c7-nul-corrige-marginal.csv`** (ce travail) | exactitude-vérité appariée ; cellules fausses tirées dans la **marginale de population par item**, valeur de la personne exclue | **20** | **0,9741** | **[0,9500 ; 0,9934]** |
| nul corrigé, remplissage uniforme | `resultats/c7-nul-corrige-marginal.csv` (même fichier, `variante=uniforme`) | idem, mais cellules fausses **uniformes sur les modalités** | 20 | 0,9815 | [0,9580 ; 0,9930] |
| « N0 nul casse » | `resultats/c7-nul-corrige.csv`, ligne `rho_resume` / `N0 nul casse` | témoin de marge historique importé tel quel de `c7_disjoint` | 100 | 0,9803 | [0,9507 ; 1,0000] |
| nul **non** corrigé | `resultats/c7-disjoint-nul.csv` | témoin de marge d'origine, défaut l. 133 non réparé | 100 | 0,9844 | [0,9650 ; 1,0000] |

**Ce qui fait foi pour le tableau 1 : la première ligne, et elle seule.** Pourquoi : c'est la
seule des quatre qui conserve l'exactitude **contre la vérité** par personne — la grandeur que
l'objection invoque — tout en étant purgée du défaut réel de `c7_disjoint.py` l. 133 (les
cellules fausses y évitaient la vraie réponse de la personne, ce qui gonflait la fuite du témoin
d'un facteur ~1,3). Le remplissage **marginal** est le bon parce qu'il tire les valeurs fausses
dans la distribution de population, sans information sur la personne ; le remplissage
**uniforme** est une variante de robustesse, publiée pour montrer que le verdict n'en dépend pas.

Dans les deux variantes, le rho observé (0,9650) tombe **à l'intérieur** de la loi nulle. Le
verdict ne dépend pas du choix. Mais le **chiffre publié**, si.

## 6. Nature des bornes — ce ne sont pas des intervalles de confiance

`[0,950 ; 0,993]` sont les **5ᵉ et 95ᵉ centiles d'une loi nulle** : la dispersion des rho
produits par 20 tirages du témoin. Ce n'est **pas** un intervalle de confiance autour du rho
observé, et cela ne se lit pas comme tel — la question posée est « le 0,965 observé sort-il de
cette distribution ? » (réponse : non), pas « quelle est la précision de 0,974 ? ».

La correction est déjà appliquée au manuscrit ; le CSV la porte dans ses **noms de colonnes** :
`rho_nul_centile5_loi_nulle`, `rho_nul_centile95_loi_nulle`, plus une colonne
`nature_des_bornes` qui l'écrit en toutes lettres sur chaque ligne. Il n'existe dans ce fichier
aucune colonne nommée « ic », « borne_basse » ou « intervalle ».

## 7. Le CSV

`resultats/c7-nul-corrige-marginal.csv` — 143 lignes de données : une par réplicat (20 marginal,
20 uniforme, 100 marginal) plus une ligne d'agrégat par série.

| colonne | contenu |
|---|---|
| `ligne` | `replicat` ou `agregat` |
| `variante` | **`marginal`** ou `uniforme` — la distinction critique |
| `remplissage_cellules_fausses` | la construction en toutes lettres |
| `fait_foi_tableau1` | `oui` sur la seule série qui fonde le tableau 1 |
| `n_replicats`, `graine` | 20 ou 100 ; graine 20260912 |
| `n_permutations`, `n_tirages_top1`, `n_points_spearman` | 40, 3, 12 |
| `replicat`, `rho_nul` | index et rho du réplicat (lignes `replicat`) |
| `rho_nul_moyen`, `rho_nul_median`, `rho_nul_min`, `rho_nul_max` | agrégats |
| `rho_nul_centile5_loi_nulle`, `rho_nul_centile95_loi_nulle` | les bornes, nommées pour ce qu'elles sont |
| `rho_reel_observe`, `rho_reel_depasse_centile95_loi_nulle` | 0,9650 ; `false` partout |
| `nature_des_bornes`, `script`, `cache` | provenance |

## 8. Ce que la légende de la figure 2 devra citer

**Je n'ai touché ni au manuscrit, ni à la figure 2, ni à `analyses/figures_article.py`.** Pour
l'agent qui corrigera la légende :

- **Remplacer** `resultats/c7-disjoint-nul.csv` (qui porte le nul **non** corrigé, 0,9844
  [0,9650 ; 1,0000] — ce ne sont pas les valeurs de la figure) **par**
  `resultats/c7-nul-corrige-marginal.csv`.
- Les lignes à citer sont celles où **`variante = marginal` et `n_replicats = 20`**
  (`fait_foi_tableau1 = oui`). Préciser le filtre dans la légende : sans lui, le même fichier
  contient aussi 0,9815 et 0,9799.
- Les colonnes qui portent la bande tracée : **`rho_nul_centile5_loi_nulle`** et
  **`rho_nul_centile95_loi_nulle`** ; la moyenne : `rho_nul_moyen` ; l'observé :
  `rho_reel_observe`.
- La formulation « 5th–95th percentile envelope of the corrected marginal null (mean rho
  0.974) » est **exacte** et n'a pas à changer. Seule la ligne `Data:` est fausse.
- Les deux autres sources de la légende (`c7-compromis.csv`,
  `c7-compromis-robustesse-points.csv`) n'ont pas été examinées ici.

## 9. Modification apportée au script

`analyses/c7_temoin_verite_appariee.py` : **le code de calcul n'a pas bougé d'une ligne.** Deux
ajouts, tous deux après le calcul :

1. accumulation des rho déjà calculés dans un dictionnaire `RESUME`, puis écriture CSV si
   `C7_MARGINAL_CSV` est posé (sans cette variable, le script se comporte exactement comme
   avant) ;
2. une variable `MODES` qui restreint les variantes parcourues. Elle ne change aucun résultat :
   la graine de chaque réplicat est `[GRAINE,999,r,graine_nom(nom),0|1]`, indépendante de l'ordre
   d'itération.

**Preuve que rien n'a bougé** : le run avec sortie CSV réimprime `rho moyen=+0.9741
mediane=+0.9720 p5=+0.9500 p95=+0.9934 min=+0.9301 max=+1.0000`, identique au run du script
non modifié effectué avant toute édition.

## 10. Reste ouvert

- La décision n = 20 contre n = 100 du §4, à trancher par le responsable.
- La correction de la légende de la figure 2 (agent dédié).
- Le `cecite:` ci-dessus : je n'ai pas relu le manuscrit et ne peux pas garantir que 0,974
  n'apparaît pas ailleurs avec une autre provenance déclarée.
