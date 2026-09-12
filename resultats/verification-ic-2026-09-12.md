# Vérification des intervalles publiés — 12 septembre 2026

statut: courant
mandat: établir si les intervalles publiés sont ce qu'ils prétendent être, et si des valeurs parties dans des lettres sont fausses
agent: Opus 5, Anthropic
ecriture: resultats/verification-ic-2026-09-12.md
lecture_seule: tout le reste
interdits: appel payant sans GO, réseau, commit sur master, arrière-plan
cecite: n'a pas eu accès à la boîte mail — la version réellement envoyée a été établie séparément
cout_reel_usd: 0.00

Agent de vérification, lecture seule sur tout le dépôt sauf ce fichier. Aucun appel de
modèle, aucun réseau, aucun `git commit`. Tout recalculé en avant-plan avec `.venv`.
**Je constate, je ne corrige pas.**

Périmètre : les deux anomalies signalées par la construction du registre de chiffres
(`resultats/registre-chiffres.csv`), plus un balayage des autres grandeurs à intervalle et
un relevé de ce que contiennent effectivement les lettres de divulgation.

---

## VERDICT EN DEUX LIGNES

**Anomalie 1 (Clopper-Pearson) : INEXACTE.** La méthode est implémentée deux fois dans
`analyses/`, et mes recalculs indépendants reproduisent **toutes** les valeurs publiées au
centième de point près. Rien à corriger sur le fond ni sur les chiffres.

**Anomalie 2 (bornes du 0,974) : EXACTE sur la nature des bornes, INEXACTE sur les
lettres.** `[0,950 ; 0,993]` sont bien des centiles 5/95 d'une loi nulle simulée et non un
intervalle de confiance — mais **les lettres les nomment correctement**. La confusion est
interne au manuscrit et à la synthèse, et **la conclusion ne dépend pas de ce point**.

---

## 1. Anomalie 1 — Clopper-Pearson : implémenté, et les chiffres sont justes

### 1.1 La méthode existe

L'affirmation « aucun script C7 n'implémenterait cette méthode » vient de
`resultats/socle-v2-2026-09-12.md` l. 80-82 :

> « **Aucune méthode Clopper-Pearson n'existe dans les scripts C7** (grep `clopper`,
> `beta.ppf`, `binomtest` : zéro occurrence), alors que l'article en cite. »

**Cette phrase est fausse sur ses trois termes.** Les deux premiers motifs ont des
occurrences, dans deux scripts distincts et commités :

| Fichier | Lignes | Contenu |
|---|---|---|
| `analyses/c7_a9_ic.py` | 39-49 | `def clopper_pearson(x, n, alpha=0.05)` — `stats.beta.ppf(alpha/2, x, n-x+1)` et `stats.beta.ppf(1-alpha/2, x+1, n-x)`, avec les cas limites `x=0` et `x=n` traités |
| `analyses/c7_multiplicite_globale.py` | 125-131 | même calcul, en ligne, avec les mêmes deux appels à `stats.beta.ppf` |

Le script `c7_a9_ic.py` calcule en outre Wilson (l. 52-58) et la règle de trois (l. 61-63)
comme contrôles croisés, et traite explicitement les six occurrences de « 0 succès / n,
IC [0 ; 0] » du dépôt, pas seulement A9 (l. 21-24 de sa docstring). C'est un travail plus
complet que ce que l'article en cite.

**Hypothèse la plus probable sur l'origine de l'anomalie** : le grep de `socle-v2` a été
lancé sur un motif de nom de fichier trop étroit (`c7-*` au lieu de `c7_*`, ou restreint
aux scripts qui écrivent un CSV — or `c7_a9_ic.py` n'écrit que sur stdout). Le fichier
`c7_a9_ic.py` est daté du 12/09 09:22 et `c7_multiplicite_globale.py` du 12/09 09:34 ; ils
existaient donc bien avant la construction du registre.

### 1.2 Recalcul indépendant

Recalculé sans lire les rapports, avec la définition standard bilatérale de
Clopper-Pearson (borne haute = quantile 97,5 % de Beta(x+1, n−x)) :

| x / n | Ma valeur recalculée | Valeur publiée | Écart |
|---|---|---|---|
| 0 / 30 | **[0 ; 11,5703 %]** | [0 ; 11,57 %] | **aucun** |
| 0 / 10 | **[0 ; 30,8497 %]** | [0 ; 30,85 %] | **aucun** |
| 0 / 40 | **[0 ; 8,8097 %]** | [0 ; 8,81 %] | **aucun** |
| 0 / 200 | **[0 ; 1,8275 %]** | [0 ; 1,83 %] | **aucun** |
| 0 / 2058 | **[0 ; 0,1791 %]** | [0 ; 0,18 %] | **aucun** |

**Les cinq valeurs concordent exactement, arrondis compris.** La convention retenue
(bilatérale à 95 %) est la convention de référence ; elle est plus conservatrice que la
borne unilatérale `1 − 0,05^(1/n)` (9,50 % à n=30) et que la règle de trois (10,0 % à
n=30), toutes deux mentionnées dans `c7_a9_ic.py` comme repères. Le choix publié est donc
le plus prudent des trois, ce qui est le bon sens pour une requalification en « non
concluante ».

### 1.3 Les valeurs sont-elles sourcées ?

**Oui.** Chaîne complète : `analyses/c7_a9_ic.py` (méthode) →
`resultats/c7-a9-correction-2026-09-12.md` (table de correction ligne à ligne, avec
l'ancienne et la nouvelle graphie pour chaque fichier et chaque numéro de ligne) →
`c7-fort-resultats.md` l. 17-23 et `c7-recette-resultats.md` l. 20-25, qui portent tous
deux un encadré « Correction du 12/09 » explicite.

**Réserve de traçabilité, déjà relevée par `autopsie-methode-2026-09-12.md` l. 263 :** les
tableaux de `c7-fort-resultats.md` (l. 15-16) et `c7-recette-resultats.md` (l. 15-16)
affichent **encore** « [0 ; 0] » dans la colonne IC ; la valeur Clopper-Pearson n'apparaît
que dans le paragraphe de correction en dessous. Le manuscrit cite ces fichiers pour des
valeurs que leurs tableaux ne portent pas. C'est un défaut de forme, pas de fond.

### 1.4 Conséquence sur le compteur 16 → 14

**Le raisonnement est valide.** Un IC bootstrap percentile sur 0 succès ne peut
arithmétiquement produire que [0 ; 0] : rééchantillonner 30 zéros avec remise ne rend
jamais autre chose que des zéros. Ce n'est pas un intervalle de confiance. Le seuil
préenregistré de 5 % tombe à l'intérieur de [0 ; 11,57 %] (n=30) et de [0 ; 30,85 %]
(n=10) ; « non concluante » est la bonne qualification, et **14** le bon compteur.

### 1.5 Un point mineur à arbitrer (n = 10 ou n = 9 ?)

`c7-recette-resultats.md` l. 16 déclare le bras « appel par item » à
**« 10 (9 complets) »** : 9 personnes complètes plus une partielle (14/60 items), le run
ayant été interrompu par un HTTP 403 de plafond de clé. L'IC publié est calculé sur
**n = 10**. Sur **n = 9**, la borne haute serait **33,63 %** au lieu de 30,85 %.

Sans conséquence sur le verdict (« non concluante » dans les deux cas, et 33,63 % est
encore plus large), mais le dénominateur retenu mérite d'être déclaré explicitement.
**Constat, pas correction.**

---

## 2. Anomalie 2 — ce que sont réellement les bornes du 0,974

### 2.1 Réponse : centiles 5/95 d'une loi nulle simulée. Pas un IC.

Preuve dans le code, `analyses/c7_temoin_verite_appariee.py` l. 86-88 :

```python
print(f"rho moyen={rhos.mean():+.4f} mediane={np.median(rhos):+.4f} p5={np.percentile(rhos,5):+.4f} "
      f"p95={np.percentile(rhos,95):+.4f} min={rhos.min():+.4f} max={rhos.max():+.4f}")
print(f"rho reel observe = 0.9650 -> le depasse-t-il ? {bool(0.965>np.percentile(rhos,95))}")
```

`rhos` est un vecteur de **N_REP réplicats du témoin** (l. 68-83) : à chaque réplicat, le
script fabrique un prédicteur nul apparié sur l'exactitude-vérité par personne, puis
calcule un Spearman sur les 12 configurations. `p5` et `p95` sont les centiles de la
distribution **de ces réplicats**.

**Ce ne sont donc ni l'un ni l'autre des candidats plausibles :**

- ce n'est **pas** un intervalle de confiance bootstrap sur les personnes — aucun
  rééchantillonnage de personnes n'a lieu ; le rééchantillonnage porte sur les tirages
  aléatoires du témoin (graines l. 73-78) ;
- c'est bien la **dispersion d'une loi nulle**, c'est-à-dire des centiles de réplicats du
  témoin. La troisième branche de l'alternative posée était la bonne.

Le tableau de `resultats/audit-renversement-2026-09-12.md` l. 99-102 le confirme en
clair : ses colonnes sont littéralement `rho moyen | médiane | **p5** | **p95** | rho réel
0,965 le dépasse ?`, avec `0,9741 | 0,9720 | 0,9500 | 0,9934 | non`.

### 2.2 Aucun CSV source — confirmé

Vérifié : le script ne contient **aucune** écriture de fichier (ni `to_csv`, ni `open(...,
"w")`, ni `savetxt`). Sa docstring l. 16 dit « Lecture seule. Écrit uniquement dans le
scratchpad », et en pratique il n'écrit que sur stdout. `registre-chiffres.csv` porte donc
justement `csv_source = ABSENT` pour la ligne `rho-nul-marge-appariee-12conf`.

**Nuance importante et à l'avantage du dossier :** le script, lui, **est commité**
(`218c955`), avec un en-tête de provenance qui documente son sauvetage depuis le
scratchpad. Le chiffre est donc **reproductible** (~130 s de calcul d'après
`audit-renversement` l. 369) même s'il n'est pas *archivé*. C'est une faiblesse de
traçabilité, pas un chiffre inventé.

### 2.3 Deux réserves supplémentaires, non signalées jusqu'ici

1. **N_REP = 20 par défaut** (l. 25). Un p5 et un p95 estimés sur 20 valeurs sont
   extrêmement grossiers : p5 est essentiellement le minimum de l'échantillon. Les bornes
   `[0,950 ; 0,993]` ne doivent pas être lues comme stables au troisième chiffre. À
   comparer aux 100 réplicats de l'ancien témoin non corrigé
   (`rho-nul-marge-items-disjoints`, 0,984 [0,965 ; 1,000]).
2. **Le registre est, lui, irréprochable sur ce point.** Sa colonne `methode_ic` porte
   `centiles 5/95 d'une loi nulle simulee (pas un IC)` et son libellé répète « Les bornes
   sont les centiles 5/95 d'une loi nulle simulée, PAS un intervalle de confiance ». C'est
   le registre qui a détecté la confusion, et il l'encode correctement.

### 2.4 La conclusion change-t-elle ? **Non — et elle ne pouvait pas changer.**

C'est le point décisif, et il va dans le sens inverse de l'inquiétude.

La prédiction (b) est réfutée parce que le prédicteur réel (rho 0,965) **ne dépasse pas**
le témoin. Le test préenregistré est littéralement, l. 88 du script :
`0.965 > np.percentile(rhos, 95)` → **False**.

**Cette comparaison exige des centiles, et serait fausse avec un intervalle de
confiance.** Comparer une statistique observée au 95ᵉ centile d'une distribution nulle est
exactement l'usage propre d'une loi nulle. Un IC, lui, décrirait l'incertitude
d'estimation du témoin et n'aurait aucun sens ici.

Autrement dit : **la nature réelle des bornes est celle que le test requiert.** L'erreur
est purement rédactionnelle — on a nommé « IC » ce qui est un témoin —, et la
requalifier correctement **renforce** la démonstration au lieu de la fragiliser. La
réfutation de (b), et donc le titre de l'article, tiennent indépendamment.

Robustesse supplémentaire : le second mode de remplissage (uniforme) donne 0,9815
[0,9580 ; 0,9930], même verdict ; et l'ancien témoin non corrigé donnait 0,984 contre
0,969, même verdict. **Trois témoins, trois fois « non dépassé ».**

### 2.5 Ce que le texte aurait dû écrire

La formulation correcte existe déjà dans le dépôt — c'est celle que l'audit s'était
lui-même prescrite (`audit-renversement-2026-09-12.md` l. 385) :

> « rho 0,974, **5ᵉ–95ᵉ centiles [0,950 ; 0,993]**, contre 0,965 observé »

Et, en anglais, `article/manuscrit.md` l. 458-459 :

> « rho 0.974, **5th–95th percentiles [0.950 ; 0.993]**, against 0.965 observed »

Formulation encore plus explicite si l'on veut clore le sujet : « rho moyen du témoin
0,974 ; **enveloppe 5ᵉ–95ᵉ centile de sa distribution sur 20 réplicats** [0,950 ; 0,993] ;
le rho observé (0,965) est **à l'intérieur** de cette enveloppe, donc ne dépasse pas le
témoin. »

**Ce qu'il ne faut pas écrire** : `0,974 [0,950 ; 0,993]` nu, ni rien qui contienne
« IC 95 % » ou « 95 % CI » accolé à ces bornes.

---

## 3. Où la confusion se propage réellement (et où elle ne se propage pas)

Le problème n'est pas que le dépôt ignore la distinction — il la connaît. Le problème est
qu'il l'applique **de façon inégale à l'intérieur d'un même document**, ce qui est le pire
des deux mondes pour un relecteur.

### 3.1 `article/manuscrit.md` — incohérent avec lui-même

| Ligne | Graphie | Statut |
|---|---|---|
| 458-459 | `rho 0.974, 5th–95th percentiles [0.950 ; 0.993]` | **correct** |
| 791 | `5th–95th percentile envelope of the corrected marginal null (mean rho 0.974)` | **correct** |
| **39** (résumé) | `as ours (0.974 [0.950 ; 0.993] against 0.965 observed)` | **ambigu** |
| **105** | `Spearman **0.974** [0.950 ; 0.993] against **0.965** observed` | **ambigu** |
| **898** (tableau 3, ligne 1) | `Null rho 0.974 [0.950 ; 0.993] against 0.965 observed` | **ambigu** |

Pourquoi « ambigu » et pas « anodin » : aux lignes **96** et **450** du *même* manuscrit,
la graphie `95 % CI [0.937 ; 0.993]` est utilisée pour le rho observé sur items disjoints
(0,969). **Deux crochets typographiquement identiques, l'un déclaré IC et l'autre non, à
quelques lignes d'écart, sur la même grandeur (un Spearman) et avec une borne haute
identique (0,993).** Un relecteur lira le second comme un IC. C'est la faute de méthode
signalée, et elle est réelle — dans le résumé et dans le tableau des résultats, c'est-à-dire
aux deux endroits les plus lus.

### 3.2 `resultats/article-synthese.md` — la propagation la plus étendue

Cinq occurrences de `0,974 [0,950 ; 0,993]` **sans aucune mention de centiles** : l. 15,
17, 23, 137, 148. La l. 17 est la plus problématique, car elle juxtapose dans une même
phrase `Spearman 0,969, IC 95 % [0,937 ; 0,993]` et `0,974 [0,950 ; 0,993]`.

**Et surtout l. 148**, qui est une consigne opérationnelle à l'agent figures :

> « Rho de Spearman observé et rho du nul en encart, l'un à côté de l'autre, **plus IC**. »

Si cette consigne est exécutée telle quelle, **la figure 2 étiquettera les centiles du
témoin comme un IC**. C'est le point le plus urgent de tout ce rapport, parce qu'il
transformerait une imprécision de texte en erreur gravée dans une figure. (La même ligne
dit par ailleurs correctement « enveloppe du nul de marge », d'où l'incohérence.)

### 3.3 Autres fichiers

- `resultats/audit-renversement-2026-09-12.md` **l. 16** (verdict en une ligne) :
  `rho 0,974 [0,950 ; 0,993] contre 0,965 observé`, non étiqueté — alors que le même
  document l'étiquette correctement l. 99-102 et l. 385.
- `resultats/autopsie-methode-2026-09-12.md` l. 126 : reprend la graphie nue.
- `resultats/c7-nul-corrige-resultats.md` l. 95 : tableau `N0 nul cassé` avec deux paires
  de bornes, en-têtes de colonnes à vérifier (ce rapport porte déjà un avertissement de
  rétractation).

### 3.4 Balayage des autres grandeurs — pas d'autre confusion du même type

J'ai balayé `resultats/*.md` et `article/*.md` à la recherche de bornes accolées à un
témoin ou à un nul. **Aucun autre cas de centiles présentés comme IC n'a été trouvé.** Les
intervalles des grandeurs observées (top-1 Twin 20,7 % [19,0 ; 22,4], Park 90,40 %
[88,6 ; 92,2], monde ouvert 60,17 % [54,5 ; 64,4], défense D4 0,13 % [0,01 ; 0,28],
témoin de population pure 0,07 % [0,04 ; 0,11]) sont tous de vrais bootstraps percentile
sur les personnes, correctement déclarés dans `registre-chiffres.csv` avec leur nombre de
réplicats et leur CSV source.

Deux réserves distinctes, déjà connues du registre et **non** du type « centile pris pour
un IC » :

1. `twin-transfert-top1-60items` (**36,4 %**) : `ic_bas`/`ic_haut`/`methode_ic` =
   **ABSENT**, avec la mention « AUCUNE agrégation d'IC n'existe : les IC du CSV sont par
   paire ». **Ce chiffre est cité sans IC dans la lettre Columbia** (voir §4.3) — c'est le
   cas de « méthode d'intervalle non déclarée » le plus proche de ce qui était cherché,
   mais il se manifeste par une *absence* d'intervalle, pas par une confusion.
2. Le doublon `twin-top1-ferme-json41-naif` : `0,2068027 [0,18960 ; 0,22427]`
   (`c7-reidentification.csv`) contre `0,2069485 [0,19072 ; 0,22457]`
   (`c7-attaquant-fort.csv`) — même condition, deux implémentations, deux IC. Écart
   négligeable (0,0001), mais à arbitrer avant soumission. Relevé par `socle-v2` §3.

---

## 4. Ce qui est effectivement parti dans les lettres

### 4.1 Les lettres nomment correctement les centiles — l'anomalie 2 se trompe sur ce point

L'anomalie signalée affirmait : « Ce chiffre est écrit dans la lettre partie à Columbia,
**présenté comme un IC à 95 %** ». **C'est faux.** Texte exact de
`resultats/divulgation-responsable-brouillon.md` :

- **l. 30-32 (note française au responsable)** : « rho 0,974, **5ᵉ–95ᵉ centiles**
  [0,950 ; 0,993] […] et le prédicteur réel (rho 0,965) ne le dépasse pas »
- **l. 162-164 (lettre anglaise à Columbia)** : « the control still reproduces the
  fidelity/leakage coupling we observe (rho = 0.974, **5th-95th percentiles**
  [0.950 ; 0.993], over the 12 configurations measured on whole items), and our real
  twins' rho (0.965) does not exceed it »

La lettre fait donc **exactement** ce que le manuscrit ne fait pas systématiquement : elle
distingue les deux objets. Elle écrit `[95% CI ...]` là où il y a un vrai IC (l. 115, 126,
233-234, 238, 245-246, 249) et `5th-95th percentiles` pour le témoin. **La lettre est plus
rigoureuse que le manuscrit qu'elle résume.**

### 4.2 Aucune version commitée n'a jamais présenté ces bornes comme un IC

Vérifié sur les six versions de l'historique git du brouillon :

| Commit | Heure (12/09) | Graphie du rho du témoin |
|---|---|---|
| `5955d12` | 00:38 | absent |
| `f09c8da` | 01:10 | **absent** (pas de rho, pas de Clopper-Pearson) |
| `09b18d7` | 13:25 | `rho 0,974–0,985` — une plage, **sans crochets**, donc sans confusion possible |
| `d11e670` | 17:08 | idem |
| `aa97d1f` | 17:44 | `5ᵉ–95ᵉ centiles [0,950 ; 0,993]` — **correct dès son apparition** |
| `8d43f1c` | 17:55 | idem (état courant, arbre propre) |

**Les bornes `[0,950 ; 0,993]` n'apparaissent dans la lettre qu'à 17:44, et elles y
apparaissent d'emblée correctement étiquetées.** Il n'existe aucune fenêtre temporelle
pendant laquelle une version de la lettre les aurait présentées comme un IC.

### 4.3 En revanche : deux points réels sur les lettres

**(a) Clopper-Pearson est délibérément hors des lettres, et c'est justifié.** La note
l. 71-79 explique que la requalification des deux prédictions en « non concluantes » n'a
**pas** été injectée dans le corps des lettres, au motif que ces deux tests internes de
méthodologie « ne portent ni sur les données Twin-2K-500 ni sur celles de Park/Stanford
spécifiquement » et ne sont pas des faits sur le risque de vie privée de leurs répondants.
Le raisonnement est défendable et la décision est documentée. **Aucune valeur
Clopper-Pearson n'est citée à Columbia ni à Stanford** — il n'y a donc, sur ce volet,
strictement rien à corriger auprès d'eux.

**(b) Le 36,4 % est cité sans intervalle.** La lettre Columbia (l. 152-158) cite
« 36.4% for the real twin-to-twin match » entouré de chiffres qui, eux, portent tous un
IC (`46.0% [45.9-46.1%]`, `+3.8 points [3.8-3.9]`, `+17.4 points [17.2-17.6]`,
`0.07% [0.04-0.11%]`). Le registre indique qu'aucun IC agrégé n'a jamais été calculé pour
cette moyenne. Ce n'est pas un chiffre faux, et ne pas afficher d'IC est plus honnête que
d'en afficher un inventé ; mais dans un paragraphe où tout le reste en porte un, l'absence
se remarque. **Imprécis, pas faux.**

### 4.4 Réserve majeure : le dépôt ne contient aucune preuve d'envoi

**Aucun fichier du dépôt n'atteste qu'une lettre ait été envoyée** (recherche sur
« envoyée ce matin », « lettres parties », « envoi effectué », « a été envoyé », « sent
this morning » : aucun résultat pertinent). Au contraire, l'en-tête du brouillon affirme
deux fois l'inverse, et jusque dans sa version courante de 17:55 :

> « Rien n'est envoyé par cet agent […] **Aucun message n'a été envoyé ni ne sera envoyé
> sans une décision explicite du responsable.** »

**Cela crée une incertitude qu'il faut lever avant toute démarche**, parce que la réponse
change complètement selon la version :

- **Si les lettres sont parties après 17:44** (état `aa97d1f`/`8d43f1c`) : elles
  contiennent la formulation correcte. **Rien à corriger sur les deux anomalies.**
- **Si elles sont parties le matin du 12/09** (état `f09c8da`, 01:10) : elles ne
  contiennent **ni** le 0,974 **ni** Clopper-Pearson — les deux anomalies sont alors sans
  objet pour les destinataires. **Mais cette version-là pose des problèmes bien plus
  graves, sans rapport avec le présent mandat :**
  - signature non renseignée (`[Name]` en placeholder, trois occurrences) — ce qui rend
    d'ailleurs un envoi en l'état peu plausible ;
  - elle annonce le **renversement** de la prédiction (b) et le chiffre **0,118–0,206**,
    tous deux **rétractés depuis** ;
  - elle annonce à Twin-2K-500 le scénario inter-organisations comme **réfuté** sur la
    foi du 1,8 % — or ce dispositif s'est révélé **non testable** ;
  - elle cite à Stanford **20,4 %** en monde ouvert, là où la mesure à jour est
    **60,17 % [54,5 ; 64,4]** : une **sous-estimation d'un facteur ~3 du risque
    communiqué**, dans une lettre de divulgation responsable ;
  - elle cite **65,7 %** (valeur courante 65,51 %) et « 21 % sur 40 items » (valeur
    courante 20,7 % [19,0 ; 22,4] sur le bloc de 60 items) ;
  - **aucun chiffre n'y porte d'IC.**

**Première chose à faire : établir laquelle des deux versions est partie, et à quelle
heure.** Cette question prime sur les deux anomelies, parce que le scénario « version du
matin » impose un correctif bien plus lourd — et de sens opposé : il faudrait annoncer à
Stanford un risque **trois fois plus élevé** que celui qu'on leur a communiqué.

---

## 5. Réponse point par point aux deux anomalies

| # | Anomalie signalée | Verdict |
|---|---|---|
| 1 | « Aucun script C7 n'implémente Clopper-Pearson » | **INEXACTE.** Deux implémentations (`c7_a9_ic.py` l. 39-49, `c7_multiplicite_globale.py` l. 125-131). La phrase de `socle-v2` l. 80-82 est fausse et devrait être retirée du socle. |
| 1b | « Les valeurs [0 ; 11,57 %] et [0 ; 30,85 %] seraient douteuses » | **INEXACTE.** Recalcul indépendant : 11,5703 % et 30,8497 %. Concordance exacte. Requalification 16 → 14 valide. |
| 1c | Traçabilité | **Partiellement fondée.** Les tableaux de `c7-fort-resultats.md` et `c7-recette-resultats.md` affichent encore « [0 ; 0] » ; la valeur corrigée n'est que dans le paragraphe en dessous. Défaut de forme. Plus : dénominateur n=10 vs n=9 à déclarer. |
| 2 | « `[0,950 ; 0,993]` sont des centiles 5/95 d'une loi nulle, pas un IC » | **EXACTE.** Prouvé par le code (l. 86-88 de `c7_temoin_verite_appariee.py`) et par le tableau de l'audit (l. 99-102). |
| 2b | « Aucun CSV source » | **EXACTE**, mais le script est commité (`218c955`) et le chiffre reproductible en ~130 s. Traçabilité faible, pas chiffre inventé. À noter aussi : N_REP = 20 seulement. |
| 2c | « Ce chiffre est dans la lettre Columbia, présenté comme un IC à 95 % » | **INEXACTE.** La lettre écrit « 5th-95th percentiles » (l. 162-164) et réserve « [95% CI …] » aux vraies estimations. Aucune version commitée n'a jamais dit autre chose. |
| 2d | « La conclusion dépend-elle de la nature des bornes ? » | **NON.** Le test est `0,965 > p95` → False. Une comparaison à un centile de loi nulle est précisément l'usage correct. La réfutation de (b) et le titre tiennent. Requalifier correctement **renforce** l'argument. |

---

## 6. Ce que je recommande — et ce que je ne recommande pas

**Je constate ; la décision appartient au responsable.** Rien n'a été modifié hors de ce
fichier.

### Faut-il écrire à Columbia et à Stanford ?

**Sur les deux anomalies signalées : non.** Aucune des deux ne produit un chiffre faux
dans les lettres. La première est inexacte (la méthode existe, les valeurs sont justes, et
elles ne sont de toute façon pas citées aux destinataires) ; la seconde porte sur une
formulation que les lettres ont, précisément, formulée correctement. **Écrire à ces deux
équipes pour corriger le 0,974 ou les intervalles Clopper-Pearson serait un correctif sans
objet** — et coûterait de la crédibilité sans rien rectifier.

**Sous une condition suspensive, toutefois** : il faut d'abord établir **quelle version
est partie** (§4.4). Si c'est la version du matin du 12/09, alors **oui, il faut écrire**,
mais pour de tout autres raisons — sous-estimation du risque en monde ouvert annoncée à
Stanford (20,4 % contre 60,17 %), et deux affirmations depuis rétractées auprès de
Twin-2K-500. Ce correctif-là serait sérieux et urgent.

### Ce qui doit être corrigé en interne, avant soumission

Par ordre d'urgence :

1. **`article-synthese.md` l. 148** — la consigne « plus IC » pour l'encart de la figure 2.
   À reformuler en « enveloppe 5ᵉ–95ᵉ centile du témoin » **avant** que l'agent figures ne
   l'exécute. C'est le seul point où l'erreur risque de devenir irréversible.
2. **`article/manuscrit.md` l. 39, 105, 898** — aligner sur la graphie déjà correcte des
   l. 458-459 et 791. Ce sont le résumé et le tableau des résultats.
3. **`article-synthese.md` l. 15, 17, 23, 137** — même alignement.
4. **`audit-renversement-2026-09-12.md` l. 16** — le verdict en une ligne, à aligner sur la
   l. 385 du même document.
5. **`socle-v2-2026-09-12.md` l. 80-82** — retirer l'affirmation « aucune méthode
   Clopper-Pearson n'existe », qui est fausse et qui a déclenché cette vérification.
6. **`c7-fort-resultats.md` et `c7-recette-resultats.md`** — porter la valeur
   Clopper-Pearson **dans** les tableaux, et déclarer le dénominateur du bras « appel par
   item » (n = 10 ou n = 9).
7. Si le temps le permet : relancer le témoin avec `NREP` nettement supérieur à 20, et
   **archiver un CSV**, pour que `registre-chiffres.csv` puisse passer la ligne
   `rho-nul-marge-appariee-12conf` de `provisoire` à `courant`.

### Une remarque pour finir

Le registre de chiffres a signalé deux anomalies ; l'une est fausse et l'autre est réelle
mais sans effet sur les conclusions — et dans les deux cas le dépôt contenait déjà, quelque
part, la bonne réponse et la bonne formulation. **Le dossier est plus solide que ses
signaux d'alerte ne le laissaient craindre ; c'est sa cohérence rédactionnelle interne,
pas sa statistique, qui est en défaut.** La seule chose réellement inquiétante trouvée au
cours de cette vérification ne figurait dans aucune des deux anomalies : l'absence de
trace de ce qui a effectivement été envoyé, et à quelle heure.
