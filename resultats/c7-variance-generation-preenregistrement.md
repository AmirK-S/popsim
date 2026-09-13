# Variance de génération du chiffre de titre — préenregistrement

statut: courant
mandat: Établir si le taux de ré-identification publié pour Twin-2K-500 (20,7 %) est un tirage unique d'un procédé de génération dont la variabilité n'est pas bornée par nos intervalles bootstrap sur les personnes, et fixer avant tout calcul le seuil au-delà duquel ces intervalles seront déclarés trop étroits.
agent: Claude Opus 5, Anthropic — sous-agent variance de génération
ecriture: analyses/c7_variance_generation.py, resultats/c7-variance-generation-preenregistrement.md, resultats/c7-variance-generation-resultats.md, resultats/c7-variance-generation.csv
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, régénération de jumeaux, article/manuscrit.md
cecite: je n'ai pas lu article/manuscrit.md ni resultats/article-synthese.md au-delà des lignes citant « 20,7 % » ; je n'ai pas relancé c7_reidentification.py (je réutilise son CSV de sortie tel quel) ; je n'ai pas ouvert les invites réellement envoyées à l'équipe amont — elles ne sont pas observables localement (twin-ab-audit-provenance-2026-09-11.md §6.1), donc je ne peux pas vérifier que deux bras nommés différemment diffèrent bien par ce que leur nom annonce
cout_reel_usd: 0.00

---

## 0. L'aveu qui conditionne la lecture de tout ce qui suit

**Ce préenregistrement n'est pas aveugle sur les taux par bras.** Avant de l'écrire j'ai lu
`resultats/c7-reidentification.csv` en entier, colonne `top1` comprise. Toute « prédiction »
que je formulerais sur l'ampleur de la dispersion entre bras serait une rétrodiction
déguisée, et je refuse de la présenter autrement.

Ce qui est réellement préenregistré ici, et qui ne l'était pas au moment de cette lecture :

1. **le seuil de décision** (§3), fixé avant d'avoir calculé une seule étendue, un seul
   écart type entre bras, un seul partage de variance ;
2. **l'estimateur de décomposition** (§4) et ses règles d'exclusion (§2), fixés de même ;
3. **la règle d'arrêt** (§5) : ce que je m'interdis de conclure si l'inventaire est trop pauvre.

Les quantités visées par ces seuils — étendue entre bras, rapport à la largeur bootstrap,
part de variance imputable à la génération — **n'ont été calculées qu'après** l'écriture de
ce fichier. C'est le seul sens dans lequel ce document engage quelque chose.

## 1. La question, posée sans ménagement

Le chiffre de titre — **20,7 %** de ré-identification top-1 sur Twin-2K-500, bassin de
2 058 candidats — est le taux de **un** bras : `JSON Persona - GPT4.1`, un modèle, une
génération, une graine. L'intervalle publié avec lui, **[18,96 ; 22,43]**, est un bootstrap
**sur les personnes** : il répond à « et si on avait interrogé 2 058 *autres* personnes ? ».

Il ne répond pas à « et si on avait **régénéré** les jumeaux ? ». Ces deux questions n'ont
aucune raison d'avoir la même réponse.

Le dépôt a déjà payé exactement cette confusion. Le taux de 0,13 % publié pour notre défense
s'est révélé être un tirage unique en haut d'une étendue [0 ; 0,187] de moyenne 0,096 %. Le
mécanisme est identique ici, un cran plus haut dans la chaîne.

## 2. Le matériel, et les règles d'exclusion — fixées maintenant

**Source unique retenue** : `resultats/c7-reidentification.csv`, produit par
`analyses/c7_reidentification.py` sous préenregistrement (`c7-preenregistrement.md`).

Ce CSV est le seul matériel du dépôt qui satisfait la condition de bassin strictement
constant exigée par le mandat, et je l'ai vérifié dans le code avant de l'adopter
(`c7_reidentification.py`, lignes 144-175) :

| condition du mandat | comment elle est tenue | ligne |
|---|---|---|
| bassin strictement constant | `pool` = les 2 058 humains, **jamais** restreint ; seules les personnes *attaquées* peuvent être un sous-ensemble | 155-156, 168 |
| mêmes items | `items = items_communs(codes, [REF_V4, REF_V13])` calculé **une seule fois**, hors de la boucle sur les bras, et depuis les **références humaines seules** — donc aucun bras ne peut déplacer le bassin d'items | 152 |
| même attaque | `distance_hamming`, identique pour tous | 94 |
| même convention de départage des ex æquo | `N_TIRAGES_LIENS = 20` tirages de bruit uniforme, pour tous les bras | 42, 99-106 |
| graine fixée | `GRAINE = 20260911`, plus `crc32(nom)` stable entre interpréteurs | 40, 133-136 |

La convention de départage n'est pas un détail : le mandat rappelle qu'elle vaut un facteur
**1,32** sur Twin, et le rapport de contrôle d'interprétabilité documente deux baselines à
120 personnes (13,25 % et 13,29 %) qui ne diffèrent que par la graine de départage. Elle est
ici **identique d'un bras à l'autre**, ce qui est précisément ce qu'il faut pour qu'une
comparaison entre bras ait un sens.

**Exclusions décidées avant calcul.**

- **E1 — cible unique.** Seules les lignes `cible = "humains vague 4"`. La vague 4 est la
  vérité terrain ; le retest vagues 1-3 est un plancher, pas une cible. Mélanger les deux
  doublerait artificiellement le nombre de points.
- **E2 — bassin d'attaque constant.** `JSON Persona - GPT4.1-mini` n'attaque que
  **1 000** personnes (pid 1-1000) là où les autres en attaquent 2 058. Le *bassin de
  candidats* reste 2 058, mais l'échantillon attaqué diffère. Ce bras est donc **écarté du
  calcul principal** et reporté à part. Ne pas l'écarter serait s'autoriser une comparaison
  que le mandat interdit.
- **E3 — familles hors périmètre.** Les 7 bras régénérés localement (`data/traces/c7-gen/`,
  3 modèles × 2 recettes + 1 température, 200 personnes) sont **exclus de toute mesure de
  variance**, non par commodité mais parce que `analyses/c7_controle_interpretabilite.py`
  les disqualifie : leurs jumeaux ré-identifient à 0,0-0,8 % contre un hasard de 0,83 %,
  très en dessous de la baseline démographique du même bassin. Un contraste entre eux
  comparerait deux générateurs de bruit. Même règle pour les 3 bras auxiliaires de
  granularité (30-40 personnes).
- **E4 — bras amont écartés par l'audit de provenance.** `JSON Persona (Predicted Output)`
  (masque d'items défaillant), `LLM Finetuning` (exposition par entraînement), les deux
  `Persona Summary` (suspects) : non mesurés par `c7_reidentification.py`, non réintroduits
  ici.

Restent donc **7 bras** au bassin d'attaque plein, dont **6 riches** et **1 démographique**.

## 3. Le seuil, fixé maintenant

Notation : `E` = étendue des taux top-1 entre bras (max − min, en points de pourcentage) ;
`L` = largeur de l'intervalle bootstrap publié pour le bras de titre, soit
22,4272 − 18,9600 = **3,4672 points**.

> **Seuil S1.** Si `E > 2 × L`, je conclus que **les intervalles publiés sont trop étroits** :
> ils décrivent une source de variabilité (les personnes) pendant qu'une autre, plus grande,
> reste non déclarée. Si `E < L`, les intervalles publiés absorbent la dispersion entre bras
> et rien n'est à corriger. Entre `L` et `2 × L`, zone grise : je publie le rapport et
> je ne tranche pas.

> **Seuil S2.** Si la part de variance imputable au bras dépasse **50 %**, l'article doit
> déclarer que son estimation est conditionnelle à une génération. Au-delà de **90 %**, la
> variabilité entre personnes devient un détail devant la variabilité du procédé, et
> l'intervalle publié doit être décrit comme **ne bornant pas** l'incertitude du chiffre.

Ces deux seuils sont écrits avant tout calcul d'étendue ou de partage de variance. Je
m'engage à les appliquer dans les deux sens, y compris si le résultat est confortable.

## 4. L'estimateur de décomposition, fixé maintenant

Pour chaque bras `a`, le CSV fournit la moyenne `p_a` et un IC bootstrap sur les personnes
`[b_a ; h_a]`. J'en tire l'erreur type intra-bras par `SE_a = (h_a − b_a) / (2 × 1,96)`,
l'approximation normale usuelle d'un IC à 95 %.

- **variance intra (personnes)** : `V_intra = moyenne(SE_a²)` sur les bras retenus ;
- **variance observée entre bras** : `V_obs = var(p_a)` (dénominateur `n − 1`) ;
- **composante de génération** : `V_gen = max(0, V_obs − V_intra)` — l'estimateur d'analyse
  de variance à effets aléatoires, qui retranche la part d'échantillonnage déjà comptée dans
  la dispersion observée ;
- **part imputable à la génération** : `V_gen / (V_gen + V_intra)`.

**Ce que cet estimateur ne dit pas, et qui doit être écrit dans le rapport.** Les bras
disponibles ne sont **pas** des répétitions du même procédé : ils diffèrent par le modèle
(GPT-4.1, GPT-4.1-mini, Gemini-Flash2.5) et par la représentation de la personne (JSON
Persona, Text Persona, Demographics Only) et par le protocole d'inférence (température par
défaut, raisonnement, questions répétées). `V_gen` mélange donc **le bruit d'une re-génération
à condition identique** et **l'effet délibéré du choix de condition**. C'est un **majorant**
de la première, pas une mesure de celle-ci. Le rapport devra le dire à chaque fois qu'il cite
le chiffre, et fournir séparément le minorant (§4 bis).

**§4 bis — le minorant.** Le contraste le plus proche d'une re-génération pure disponible
dans la famille amont est `Text Persona - GPT4.1-mini` contre
`Text Persona (Default Temperature) - GPT4.1-mini` : même modèle, même représentation de la
personne, seul le réglage de décodage change. L'écart entre ces deux bras est reporté comme
**minorant** de l'instabilité de génération. Aucun des deux encadrements ne remplace la
mesure demandée, qui exigerait deux exécutions de la **même** condition — et le §5 constate
qu'il n'en existe aucune sur disque.

## 5. La règle d'arrêt, et le refus de conclure en notre faveur

Le mandat prévoit qu'un inventaire trop pauvre est un livrable de pleine valeur. Je fixe donc
ce que je m'interdis :

- **R1.** Je ne déclarerai **en aucun cas** que la variabilité de génération est « faible »
  ou « bornée » sur la foi des bras disponibles. Aucun d'eux n'est un réplicat du bras de
  titre : la variabilité de re-génération à condition constante n'est **pas mesurée** par
  ce travail, et ne peut pas l'être sans dépense.
- **R2.** Si le bras de titre se révèle être le **maximum** des bras disponibles, je l'écris,
  quelle qu'en soit l'explication — y compris si c'est aussi le bras le plus fidèle et que
  le couplage fidélité-fuite le rend attendu.
- **R3.** Je n'arrondis aucune valeur dans le sens qui nous arrange. Les valeurs des CSV sont
  reportées telles quelles, à quatre décimales, et toute borne énoncée sous forme « ne
  dépasse pas X » prend la valeur du CSV, pas sa version arrondie.
- **R4.** Je respecte les treize formulations interdites de
  `resultats/marqueurs-canoniques-2026-09-13.md` §3 — en particulier **I8** (aucun facteur
  chiffré entre époques), **I6** (le comparateur conditionné ne se cite pas sans son
  conditionnement) et **I11** (0,1535 %, pas « 0,15 % »).
- **R5.** Aucune donnée individuelle n'est imprimée, ni identité, ni `TWIN_ID`, ni liste
  d'appariements : ce travail ne manipule que des taux déjà agrégés.

## 6. Le substitut par sous-échantillonnage d'items

Si — et le §5 anticipe que ce sera le cas — les bras de génération ne permettent pas de
mesurer la variabilité demandée, la variabilité entre **tirages d'items** déjà mesurée
(30 tirages par `k`, `resultats/c7-temoins-relecture.csv`) est reportée comme **borne
inférieure de l'instabilité de la mesure**. Elle est explicitement **un substitut** : elle
décrit ce que le choix du sous-ensemble d'items fait bouger, pas ce que la re-génération
ferait bouger. Elle est reportée parce qu'elle est ce que nous avons, et étiquetée comme
telle partout où elle apparaît.
