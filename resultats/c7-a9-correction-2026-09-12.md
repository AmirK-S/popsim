# Correction A9 : l'IC « [0 ; 0] » est un artefact, la réfutation n° 16 n'est pas établie

Calculs reproductibles dans `analyses/c7_a9_ic.py` (`.venv/bin/python analyses/c7_a9_ic.py`).
Aucun appel de modèle, aucune modification d'un fichier existant.

## 1. Vérification à la source

Confirmé, dénominateur **exact : n = 30**, pas autre chose. Source : `c7-fort-reidentification.csv`
(colonne `n_attaques` = 30, colonne `top1` = 0.0), documenté dans `resultats/c7-fort-resultats.md`
lignes 3-4 (« 30 personnes x 60 items = 1800 appels ») et ligne 15 (tableau, `top-1 | 0,00 % [0 ; 0]`).
Repris à l'identique dans `resultats/article-synthese.md` ligne 59 (« 30 personnes × 60 items ») et
dans `article/manuscrit.md` ligne 603 (« 30 persons × 60 items »). **0 succès sur 30 tirages est
confirmé, ce n'est pas une erreur de lecture.**

Mécanisme du bug (vérifié dans le code) : `analyses/a2_commun.py`, fonction `bootstrap_personnes`
(lignes 110-123), calcule l'IC par ré-échantillonnage percentile de 2000 tirages sur le vecteur
personne-par-personne. Quand ce vecteur est composé de 30 zéros, **chaque tirage bootstrap ne peut
reproduire que des zéros** : le 2,5ᵉ et le 97,5ᵉ centile valent tous deux 0. Le résultat n'est pas un
intervalle de confiance, c'est une propriété arithmétique du ré-échantillonnage appliqué à un
événement rare avec zéro observation. Le même mécanisme est utilisé partout dans le dépôt (c'est la
convention documentée dans `analyses/c7_ic_manquants.py`, script d'un autre agent, sans lien avec ce
défaut mais qui confirme que `bootstrap_personnes` est la méthode standard) — donc chaque « 0 succès »
du dépôt produit le même « [0 ; 0] » qu'à Fort, quel que soit n.

## 2. Les trois IC corrects pour 0/30

| méthode | IC 95 % | borne haute |
|---|---|---|
| bootstrap percentile publié | [0 ; 0] | — (artefact, non un IC) |
| **Clopper-Pearson exact** | [0 % ; 11,57 %] | 11,57 % |
| Wilson (score) | [0 % ; 11,35 %] | 11,35 % |
| règle de trois (3/n) | — | ≈ 10,00 % |

**Le seuil préenregistré de 5 % est strictement à l'intérieur des trois intervalles.** La prédiction
« top-1 > 5 % » n'est donc **pas réfutée** : elle est **non concluante, faute de puissance** (n = 30
ne permet pas de distinguer un taux réel de 0 % d'un taux réel de 5 %, 8 % ou 11 %). Note : la
relecture hostile du 12/09 (`resultats/revue-hostile-finale-2026-09-12.md`, défaut F2) arrivait à la
même conclusion qualitative avec une borne approchée « ≈ 9,5 % » ; le calcul exact (Clopper-Pearson)
donne 11,57 %, un peu plus haut mais qui ne change ni le diagnostic ni le verdict.

## 3. Toutes les occurrences à corriger

### 3.1 Le défaut central (A9, n = 30) — change le verdict et le compteur

| Fichier | Ligne | Texte actuel | Texte de remplacement |
|---|---|---|---|
| `article/manuscrit.md` | 605 | `fidelity **0.1714** against their 0.708; top-1 and top-10 **0.00 % [0 ; 0]** — below even our` | `fidelity **0.1714** against their 0.708; top-1 and top-10 **0.00 % [0 ; 11.57]** (Clopper-Pearson, n = 30) — below even our` |
| `article/manuscrit.md` | 606 | `cheap twins (0.83 % at best). **Two further preregistered predictions refuted**: accuracy > 0.55` | `cheap twins (0.83 % at best). **One further preregistered prediction refuted**: accuracy > 0.55` |
| `article/manuscrit.md` | 607 | `and top-1 > 5 %. The third (fidelity > 0.10) was confirmed at 0.1714, but barely above our best` | `; top-1 > 5 % is **not refuted** — 0/30 gives an exact 95 % CI of [0 ; 11.57 %], which contains the 5 % threshold: inconclusive for lack of power. Fidelity > 0.10 was confirmed at 0.1714, but barely above our best` |
| `article/manuscrit.md` | 796 (titre §7.1) | `### 7.1 The sixteen refuted preregistered predictions` | `### 7.1 The fifteen refuted preregistered predictions, and one inconclusive` |
| `article/manuscrit.md` | 815 (tableau 3, ligne 16) | `\| 16 \| That same twin reaches top-1 > 5 % \| **Refuted.** 0.00 % [0 ; 0], below our cheap twins \| \`c7-fort-resultats.md\` \|` | `\| 16 \| That same twin reaches top-1 > 5 % \| **Not refuted — inconclusive.** 0.00 % [0 ; 11.57] (Clopper-Pearson, n = 30); the preregistered 5 % threshold lies inside the interval \| \`c7-fort-resultats.md\` \|` |
| `article/manuscrit.md` | 894 | `frontier-model run), which is why Table 3 lists sixteen refutations where the census counts` | `frontier-model run), which is why Table 3 lists fifteen refutations where the census counts` |
| `resultats/article-synthese.md` | 59 | `Exactitude **0,4722 [0,4361 ; 0,5050]** contre 0,574 pour les jumeaux Twin ; fidélité **0,1714** contre 0,708 ; top-1 et top-10 **0,00 % [0 ; 0]**. **Deux prédictions préenregistrées réfutées** : exactitude > 0,55 (obtenu 0,4722) et top-1 > 5 % (obtenu 0,00 %, soit moins que nos propres jumeaux bon marché, 0,83 % au mieux) ; la troisième (fidélité > 0,10) est confirmée à 0,1714, mais à peine au-dessus de notre meilleur jumeau faible (deepseek-v4, 0,177) — le modèle fort n'a presque rien apporté.` | `Exactitude **0,4722 [0,4361 ; 0,5050]** contre 0,574 pour les jumeaux Twin ; fidélité **0,1714** contre 0,708 ; top-1 et top-10 **0,00 % [0 ; 11,57]** (Clopper-Pearson, n=30). **Une prédiction préenregistrée réfutée** : exactitude > 0,55 (obtenu 0,4722). Top-1 > 5 % n'est **pas réfutée** : 0/30 donne un IC exact à 95 % de [0 ; 11,57 %], qui contient le seuil de 5 % — non concluant, faute de puissance ; la troisième (fidélité > 0,10) est confirmée à 0,1714, mais à peine au-dessus de notre meilleur jumeau faible (deepseek-v4, 0,177) — le modèle fort n'a presque rien apporté.` |
| `resultats/c7-fort-resultats.md` | 15 | `\| top-1 \| 0,00 % [0 ; 0] \| 20,68 % \| 0-0,83 % \|` | `\| top-1 \| 0,00 % [0 ; 11,57] (Clopper-Pearson) \| 20,68 % \| 0-0,83 % \|` |
| `resultats/c7-fort-resultats.md` | 16 | `\| top-10 \| 0,00 % [0 ; 0] \| — \| 0-2,15 % \|` | `\| top-10 \| 0,00 % [0 ; 11,57] (Clopper-Pearson) \| — \| 0-2,15 % \|` |
| `resultats/c7-fort-resultats.md` | 26 | `3. Top-1 > 5 % : **rejetée**, et même en dessous de nos jumeaux faibles (0,83 % max) : 0 %.` | `3. Top-1 > 5 % : **non concluante**, pas rejetée — 0/30 donne un IC exact à 95 % [0 ; 11,57 %] qui contient le seuil de 5 % ; puissance insuffisante à n=30.` |
| `resultats/c7-fort-resultats.md` | 10 (en-tête tableau) | `## Résultats (IC 95 %, bootstrap personnes, pool de 2 058 humains, hasard top-1 = 0,049 %)` | `## Résultats (IC 95 % Clopper-Pearson exact pour le top-1/top-10 à zéro succès, bootstrap personnes ailleurs, pool de 2 058 humains, hasard top-1 = 0,049 %)` |

### 3.2 Même défaut ailleurs dans le dépôt (le même bug de bootstrap, mécaniquement)

Ces occurrences portent le même « [0 ; 0] » impossible, produit par le même mécanisme
(`bootstrap_personnes` ré-échantillonnant des zéros). Contrairement à A9, **aucune ne change le
verdict de fond** (les bornes hautes exactes restent très en dessous des seuils comparés), mais ce
sont des occurrences supplémentaires du même défaut de notation à corriger, et pour `c7-recette`
(§3.2, ligne « Table 3 rang 9 ») le verdict lui-même doit être requalifié.

| Fichier | Ligne | Texte actuel | Texte de remplacement | Effet sur le verdict |
|---|---|---|---|---|
| `resultats/article-synthese.md` | 22 | `tombe à **0,00 % [0 ; 0]** en top-1. »` | `tombe à **0,00 % [0 ; 0,18]** (Clopper-Pearson, n=2058) en top-1. »` | Aucun — A2 tient (borne haute 0,18 % ≪ 20,7 %). |
| `resultats/article-synthese.md` | 22 | `un top-1 de **0,00 % [0 ; 0]** contre 20,7 % pour le jumeau.` | `un top-1 de **0,00 % [0 ; 0,18]** contre 20,7 % pour le jumeau.` | Aucun. |
| `resultats/c7-synth-ajuste-resultats.md` | 14 | `\| **Donneur ajusté sur bloc cible (k=1)** \| 0,584 \| **0,00 %** [0;0] \| **53,2 %** [51,0;55,3] \| **8,5** \|` | `\| **Donneur ajusté sur bloc cible (k=1)** \| 0,584 \| **0,00 %** [0 ; 0,18] (Clopper-Pearson) \| **53,2 %** [51,0;55,3] \| **8,5** \|` | Aucun. |
| `article/manuscrit.md` | 428 | `obtains a top-1 of **0.00 % [0 ; 0]** [c7-synth-ajuste-resultats.md §1].` | `obtains a top-1 of **0.00 % [0 ; 0.18]** (Clopper-Pearson, n = 2,058) [c7-synth-ajuste-resultats.md §1].` | Aucun. |
| `article/manuscrit.md` | 808 (tableau 3, ligne 9) | `\| 9 \| Call granularity explains the leakage \| **Refuted.** 0.00 % both arms; top-10 runs opposite (7.5 % vs 0 %) \| \`c7-recette-resultats.md\` \|` | `\| 9 \| Call granularity explains the leakage \| **Not confirmed (underpowered at n = 10).** 0.00 % both arms (95 % CI [0 ; 8.8] at n=40, [0 ; 30.8] at n=10); top-10 runs opposite (7.5 % vs 0 %) \| \`c7-recette-resultats.md\` \|` | **Change** : la prédiction était un ratio (« item ≥ 5× unique ») ; à n=10 la borne haute (30,8 %) ne permet ni de confirmer ni d'exclure ce ratio. « Réfutée » devient « non confirmée / non concluante ». Fait déjà chuter le compte de réfutations à 14 si appliqué avec le point 3.1. |
| `resultats/article-synthese.md` | 58 | `(ii) la granularité de l'appel expliquerait la fuite — appel unique 0,00 % et appel par item 0,00 %, le top-10 allant dans le sens **inverse** du prédit (7,5 % contre 0 %) (\`c7-recette-resultats.md\`).` | `(ii) la granularité de l'appel expliquerait la fuite — non confirmée, pas réfutée : appel unique 0,00 % [0 ; 8,8] (n=40), appel par item 0,00 % [0 ; 30,8] (n=10, sous-puissant), le top-10 allant dans le sens **inverse** du prédit (7,5 % contre 0 %) (\`c7-recette-resultats.md\`).` | Idem. |
| `resultats/c7-recette-resultats.md` | 15 | `\| Appel unique (60 items, 1 appel/pers.) \| 40 \| 0,00 % \| [0 ; 0] \| 7,50 % \| 852,9 \|` | `\| Appel unique (60 items, 1 appel/pers.) \| 40 \| 0,00 % \| [0 ; 8,81] (Clopper-Pearson) \| 7,50 % \| 852,9 \|` | Aucun en soi. |
| `resultats/c7-recette-resultats.md` | 16 | `\| Appel par item (1 appel/question) \| 10 (9 complets) \| 0,00 % \| [0 ; 0] \| 0,00 % \| 834,8 \|` | `\| Appel par item (1 appel/question) \| 10 (9 complets) \| 0,00 % \| [0 ; 30,85] (Clopper-Pearson) \| 0,00 % \| 834,8 \|` | Voir ci-dessous. |
| `resultats/c7-recette-resultats.md` | 20 | `**Rejetee.** Predit : item >= 5x unique en top-1. Les deux sont a 0,00 % (facteur non` | `**Non concluante, pas rejetee.** Predit : item >= 5x unique en top-1. Les deux sont a 0,00 % observe (facteur non` | Requalification. |
| `article/manuscrit.md` | 592-593 | `(ii) Call granularity would explain the leakage — single call 0.00 % and per-item call 0.00 %, with top-10 running in the **opposite** direction to the prediction` | `(ii) Call granularity would explain the leakage — not confirmed (underpowered, especially at n=10 for the per-item arm): single call 0.00 % [0 ; 8.8] and per-item call 0.00 % [0 ; 30.8], with top-10 running in the **opposite** direction to the prediction` | Idem. |

### 3.3 Occurrences sans effet sur le fond (n grand, notation seule)

| Fichier | Ligne | Texte actuel | Texte de remplacement |
|---|---|---|---|
| `resultats/c7-gen-resultats.md` | 10 | `\| llama31-8b \| R1 \| 0 \| 0,00 % \| [0 ; 0] \| 1,38 % \| 39,4 % \|` | `\| llama31-8b \| R1 \| 0 \| 0,00 % \| [0 ; 1,83] (Clopper-Pearson) \| 1,38 % \| 39,4 % \|` |
| `resultats/c7-gen-resultats.md` | 11 | `\| llama31-8b \| R2 \| 0 \| 0,00 % \| [0 ; 0] \| 0,45 % \| 39,8 % \|` | `\| llama31-8b \| R2 \| 0 \| 0,00 % \| [0 ; 1,83] (Clopper-Pearson) \| 0,45 % \| 39,8 % \|` |
| `resultats/c7-gen-resultats.md` | 13 | `\| qwen37-flash \| R2 \| 0 \| 0,00 % \| [0 ; 0] \| 0,00 % \| 41,2 % \|` | `\| qwen37-flash \| R2 \| 0 \| 0,00 % \| [0 ; 1,83] (Clopper-Pearson) \| 0,00 % \| 41,2 % \|` |
| `resultats/c7-gen-resultats.md` | 16 | `\| qwen37-flash \| R1 \| 1 \| 0,00 % \| [0 ; 0] \| 0,00 % \| 42,0 % \|` | `\| qwen37-flash \| R1 \| 1 \| 0,00 % \| [0 ; 1,83] (Clopper-Pearson) \| 0,00 % \| 42,0 % \|` |
| `resultats/c7-dp-resultats.md` | 12 | `\| 10 \| 0,000 % [0 ; 0] \| 3,38 \| +0,04 \|` | `\| 10 \| 0,000 % [0 ; 0,18] (Clopper-Pearson) \| 3,38 \| +0,04 \|` |
| `article/manuscrit.md` | 813 (tableau 3, ligne 14) | `top-1 0.158 %/0.000 % against 0.126 %` | `top-1 0.158 % [0.012 ; 0.340] / 0.000 % [0 ; 0.18] against 0.126 % [0.012 ; 0.284]` |

### 3.4 Formulations « nul / zéro » à nuancer (pas un IC, mais présente le point estimé comme
une certitude d'absence)

| Fichier | Ligne | Texte actuel | Texte de remplacement |
|---|---|---|---|
| `resultats/c7-fort-resultats.md` | 30-31 | `de celle de nos jumeaux les moins chers (~0,17 contre 0,71 chez Twin) et la fuite reste à\nzéro.` | `de celle de nos jumeaux les moins chers (~0,17 contre 0,71 chez Twin) et la fuite observée reste à zéro, sans que l'IC (borne haute 11,6 % à n=30) permette d'exclure un taux de quelques points de pourcent.` |
| `resultats/c7-fort-resultats.md` | 36 | `texte tronqué à 8 000), la fidélité reste basse et la fuite reste nulle.` | `texte tronqué à 8 000), la fidélité reste basse et la fuite observée reste nulle (mesure non concluante à n=30, voir Verdict).` |

## 4. Compte total de lignes à corriger

Décompte des tableaux 3.1 à 3.4 ci-dessus (chaque ligne de tableau = un correctif distinct ;
la ligne 22 d'`article-synthese.md` porte deux correctifs séparés, comptés ici deux fois) :

- **`article/manuscrit.md` : 10** correctifs — lignes 605, 606, 607, 796, 815, 894 (défaut
  central A9) ; 428, 592-593 (bloc), 808, 813 (même défaut ailleurs).
- **`resultats/article-synthese.md` : 4** correctifs — ligne 59 (A9), ligne 22 ×2 (A2), ligne 58
  (granularité de l'appel).
- **`resultats/c7-fort-resultats.md` : 6** correctifs — lignes 10, 15, 16, 26, 30-31, 36.
- **`resultats/c7-synth-ajuste-resultats.md` : 1** correctif — ligne 14.
- **`resultats/c7-recette-resultats.md` : 3** correctifs — lignes 15, 16, 20.
- **`resultats/c7-gen-resultats.md` : 4** correctifs — lignes 10, 11, 13, 16.
- **`resultats/c7-dp-resultats.md` : 1** correctif — ligne 12.

**Total : 29 correctifs** répartis sur 7 fichiers. Un seul (ligne 9 du tableau 3 / granularité de
l'appel, §5) change un verdict en plus de A9 ; les 27 autres ne corrigent que la notation de l'IC
sans changer aucune conclusion.

## 5. Autre défaut du même type, plus grave que prévu

Le point le plus utile de cette mission : **la ligne 9 du tableau 3** (`c7-recette-resultats.md`,
granularité de l'appel) souffre du même défaut ET change de verdict, comme A9. La prédiction
préenregistrée était un **ratio** (« item ≥ 5× unique en top-1 »). Avec le vrai dénominateur (n=10
sur le bras « appel par item », 9 personnes complètes), la borne haute exacte est **30,85 %** :
le facteur ≥5 n'est ni confirmé ni exclu — le texte source le reconnaît déjà à demi-mot (« facteur
non calculable sur un plancher nul », « n=10, la puissance est faible ») mais le tableau 3 du
manuscrit tranche quand même par « **Refuted** ». C'est exactement l'erreur de A9, sur une
prédiction différente. Si l'orchestrateur applique aussi cette correction, **le compte de
réfutations tombe à 14, pas 15** (A9 retirée, granularité de l'appel requalifiée).

Les autres candidats identifiés (A2/`c7-synth-ajuste`, n=2058 ; `c7-gen`, n=200 par cellule ;
`c7-dp` eps=10, n=2058) portent le même bug de notation mais **ne changent aucun verdict** : leurs
bornes hautes exactes (0,18 %, 1,83 %, 0,18 % respectivement) restent très en dessous des seuils
auxquels elles sont comparées.

## 6. Formulation de remplacement pour A9 (top-1 > 5 %)

**Ce que l'observation autorise à dire :** *« Sur ce bras payant (30 personnes, GPT-4.1, recette
Twin sans modification), le top-1 observé est 0/30. Un intervalle de confiance exact à 95 %
(Clopper-Pearson) donne [0 % ; 11,6 %] : le seuil préenregistré de 5 % se situe à l'intérieur de
cet intervalle. La prédiction "top-1 > 5 %" n'est donc pas réfutée — elle est non concluante,
faute de puissance statistique à ce dénominateur. Ce que l'expérience établit malgré tout : le
top-1 observé (0 %) est inférieur à celui de nos propres jumeaux bon marché (jusqu'à 0,83 %), et
la fidélité individuelle atteinte (0,1714) reste très en dessous de celle de l'équipe Twin (0,708)
— c'est cette dernière mesure, pas le top-1, qui explique pourquoi la fuite n'est pas revenue. »*

Cette formulation conserve tout ce que le bras payant établit réellement (l'échec à atteindre la
fidélité de Twin, donc l'échec à faire revenir la fuite comme mécanisme causal testé) sans
transformer une observation sous-puissante en réfutation d'un seuil numérique précis.
