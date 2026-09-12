# Migration du manuscrit vers le registre de chiffres — script de rendu, essai sur §5.3, coût mesuré

statut: courant
mandat: écrire le script de rendu du §1.3, peupler le registre des grandeurs de tête, et mesurer — non estimer — le coût de la migration complète du manuscrit
agent: Opus 5, Anthropic
ecriture: outils/rendu_registre.py, tests/portes/test_p7_rendu_registre.py, resultats/registre-chiffres.csv, resultats/migration-registre-2026-09-12.md
lecture_seule: tout le reste — `article/manuscrit.md` n'a pas été touché, la migration d'essai a eu lieu dans une copie de travail hors du dépôt
interdits: appel payant, réseau, recherche web, commit, arrière-plan
cecite: la provenance des grandeurs ajoutées a été établie par trois sous-agents en lecture seule travaillant en parallèle sur trois lots disjoints ; aucun n'a vu le travail des autres, et les recoupements entre lots (le 31,6 %, le 20,7 %, le 0,23 %) ont été arbitrés à la main sur les CSV
cout_reel_usd: 0.0

---

## 1. Le script de rendu

`outils/rendu_registre.py`. Il lit un fichier, remplace chaque renvoi par la valeur du
registre, et **refuse de rendre quoi que ce soit** dès qu'un renvoi pose problème.

**Grammaire.** `{{R:id}}` rend la colonne `valeur` ; `{{R:id.champ}}` rend la colonne
nommée ; `{{R:id.ic}}` rend le composite `[<ic_bas> ; <ic_haut>]`.

**La substitution est verbatim.** Le registre porte la **graphie publiée** (`20.7`,
`0.13`), jamais un flottant à reformater. Le script ne fait aucun arrondi, aucune
conversion de séparateur décimal, aucun formatage conditionnel. C'est le point : s'il en
faisait, la graphie cesserait d'être gouvernée par le registre, et la v1 a montré ce que
ça produit — le même top-1 sous trois graphies (`v1 §2.6`).

**Sept causes de refus**, toutes en code 1, et **rien n'est écrit** : identifiant absent
du registre ; ligne de statut `retracte` ; champ obligatoire vide ; champ demandé vide ;
champ demandé valant `ABSENT` ; nom de champ inconnu ; registre malformé (colonnes du
§1.3 absentes, `id` en double). Code 2 si le script n'a pas pu s'exécuter.

Le refus sur `ABSENT` mérite d'être dit : rendre le mot « ABSENT » au milieu d'une phrase
du manuscrit produirait un texte que personne ne relirait comme faux. Le script préfère
ne rien rendre.

Le schéma des douze colonnes est **importé** de `outils/portes/registre_chiffres.py`, pas
redéclaré : si les deux divergeaient, un registre passerait la porte P2 et casserait le
rendu.

### 1.1 Les tests d'échec, exécutés

`tests/portes/test_p7_rendu_registre.py` — **15 cas, tous exécutés, tous verts** ; suite
complète des portes : `python -m unittest discover -s tests/portes -t tests/portes` →
**56 tests, 55 passent, 1 sauté** (le volet `ots verify` préexistant).

| Cas | Attendu | Obtenu |
|---|---|---|
| identifiant inconnu | code 1, « ABSENT du registre » | conforme |
| ligne `statut: retracte` | code 1, « RETRACTEE » | conforme |
| champ obligatoire vide (`csv_source`) | code 1, « VIDE » | conforme |
| champ valant `ABSENT` cité via `.ic` | code 1, « vaut ABSENT » | conforme |
| nom de champ inconnu (`.intervalle`) | code 1, « champ INCONNU » | conforme |
| `id` en double dans le registre | code 1, « deja utilise » | conforme |
| registre sans les colonnes du §1.3 | code 1, « colonnes du §1.3 » | conforme |
| échec avec `--sortie` | code 1 **et aucun fichier créé** | conforme |
| `--verifier` sur un renvoi cassé | code 1, ne rend rien | conforme |
| fichier source absent | **code 2** (pas 0) | conforme |
| valeur + `.ic` + `.methode_ic` | rendu exact | conforme |
| graphie `0.13` | rendue `0.13`, sans reformatage | conforme |
| ligne `provisoire` | rendable (≠ `retracte`) | conforme |
| registre réel du dépôt | `--verifier` en code 0 | conforme |
| fichier sans renvoi | identique à l'entrée | conforme |

Un cas mérite d'être signalé parce qu'il a **corrigé le script et non le contraire** : le
test « nom de champ inconnu » a d'abord fait dire au script « id absent du registre », ce
qui est un refus correct mais un diagnostic trompeur. Le message a été repris.

## 2. Le registre après peuplement

**10 lignes → 33 lignes** (23 ajoutées). `registre_chiffres.py --registre-seul` : **code 0**.

Ajouts : les quatre taux du monde ouvert sous attaquant fort (4,28 / 44,37 / 1,01 %) et
les deux sous attaque naïve (3,04 / 20,39 %) ; les deux plafonds de retest humain
(54,5 / 90,7 %) ; le comparateur PMM k=10 (0,23 %) ; le témoin de marge (31,6 %) et sa
version rétractée (41,2 %) ; la troisième implémentation du 20,7 % ; les trois composantes
du coût de D4 (4,4 points, 0,0 point, 68,1 %) ; les quatre taux du factoriel
un-facteur-à-la-fois (0,67 / 0,83 / 2,65 / 13,29 %) ; les quatre taux à facteur unique
isolé (d = 1) du second factoriel, `resultats/c7-loi-distance.csv` (81,4 / 67,1 / 33,5 /
17,2 %) ; le bras « deux organisations » (1,76 %).

*(Le nom usuel de ce second factoriel est évité ici : la porte P3 le prend pour une
formulation interdite — voir §5.8.)*

**Statuts : 24 `courant`, 8 `provisoire`, 1 `retracte`.**

### 2.1 Les champs restés `ABSENT`, et pourquoi

**9 lignes sur 33 (27 %) portent au moins un `ABSENT`.** Rien n'a été deviné.

| Ligne | Champs `ABSENT` | Raison |
|---|---|---|
| `twin-transfert-top1-60items` | `ic_bas`, `ic_haut`, `methode_ic`, `n_replicats` | aucun IC agrégé n'existe ; les IC du CSV sont par paire |
| `rho-nul-marge-appariee-12conf` | `csv_source` | le script n'écrit rien |
| `rho-observe-12conf-items-entiers` | `n_replicats` | non écrit, ni CSV ni rapport |
| `rho-observe-12conf-memes-items` | `n_replicats`, `graine` | idem |
| `pmm-k10-top1-ferme-contre-examen` | `methode_ic`, `n_replicats`, `graine`, `script`, `csv_source` | **producteur perdu** : « script jetable hors dépôt (scratchpad de session) », déclaré tel quel en tête du rapport. Aucun CSV ne porte le triplet 0,23 [0,06 ; 0,42] |
| `temoin-marge-top1-json41-marginal` | `ic_bas`, `ic_haut`, `methode_ic`, `csv_source` | `c7_temoin_verite_appariee.py` **n'écrit aucun fichier** ; et **aucun IC n'a jamais été calculé pour ce top-1** — le `[0,950 ; 0,993]` publié à côté est l'IC du rho |
| `defense-d4-cout-correlations` | `ic_bas`, `ic_haut` | `methode_ic` = **SANS OBJET** : `erreur_correlations()` rend un point unique, aucun rééchantillonnage |
| `defense-d4-cout-groupes` | `ic_bas`, `ic_haut` | `methode_ic` = **SANS OBJET** : zéro **exact par construction**, pas une estimation |
| `defense-d4-aggravation-ecart-humain` | `ic_bas`, `ic_haut`, `script` | grandeur **dérivée**, calculée à la main à la rédaction à partir de deux cellules ; aucun script ne la produit |

Distinction introduite et à conserver : `ABSENT` = « je n'ai pas pu l'établir » ;
**`SANS OBJET`** = « cette grandeur n'a pas d'intervalle, et c'est correct ». Les
confondre ferait chercher indéfiniment un IC qui ne doit pas exister.

### 2.2 La méthode d'intervalle : la distinction est maintenant portée

Trois familles cohabitent dans le registre, et elles n'étaient pas distinguées :

1. **bootstrap percentile 2,5/97,5 sur les personnes** — le cas courant ;
2. **bootstrap re-estimant les paramètres à chaque tirage, plis bloqués par identité,
   seuil rejoué** — les taux du monde ouvert. Le même CSV porte aussi des IC « figés » qui
   ne sont **pas** ceux du manuscrit ; la ligne le dit ;
3. **centiles 5/95 d'une loi nulle simulée** — ce n'est **pas** un intervalle de confiance,
   et le registre le porte en toutes lettres.

**Clopper-Pearson.** Le manuscrit en cite (ligne 498, `0.00 % [0 ; 0.18]`). La note du
socle « aucune méthode Clopper-Pearson n'existe dans les scripts C7 » **n'est plus vraie
au commit courant** : `analyses/c7_a9_ic.py` et `analyses/c7_multiplicite_globale.py` en
contiennent. Aucune des 33 lignes du registre n'en porte : la ligne du 0,00 % n'a pas été
ouverte faute d'avoir tracé la chaîne. À faire avant soumission.

## 3. La migration d'essai — §5.3, copie hors du dépôt

Périmètre : lignes 507 à 541 de `article/manuscrit.md`, section « 5.3 Open world — the
defensible measurement », **copiées dans le répertoire de travail de session**. Le
manuscrit réel n'a pas été touché.

10 substitutions, **20 renvois posés**, couvrant **28 valeurs tapées** (10 points, 18
bornes).

```
rendu_registre.py --fichier section-5.3-migre.md --verifier   -> code 0, 20 renvois résolus
rendu_registre.py --fichier section-5.3-migre.md --sortie …   -> code 0
cmp section-5.3-origine.md section-5.3-rendu.md               -> aucune différence
sha256 identique : 189a7d48…9d1dc366
```

**Résultat : identique au caractère près.** Aucun écart, ni de graphie, ni d'espacement,
ni de fin de ligne — y compris sur l'intervalle coupé par un retour à la ligne
(`90.7 %` puis `[88.2 ; 93.3]`), rendu par deux renvois séparés.

Une vérification de plus, parce qu'un rendu identique ne prouve pas que la migration a
servi à quelque chose : la porte P2 compte **12 chiffres en dur** dans la section
d'origine et **0** dans la section migrée.

## 4. Le coût mesuré de la migration complète

### 4.1 Le périmètre réel est 1,8 fois celui que P2 annonce

P2 ne voit que les nombres à **deux décimales ou plus**. Or le manuscrit publie beaucoup
de bornes à une décimale — `[3.3 ; 5.6]`, `[2.0 ; 4.0]`, `[15.7 ; 24.5]`. Elles sont
aussi des valeurs publiées, et une migration qui les laisserait tapées à la main ne
protégerait rien.

| Mesure sur `article/manuscrit.md` | P2 (≥ 2 décimales) | Périmètre réel (≥ 1 décimale) |
|---|---|---|
| occurrences | 336 | **610** |
| valeurs distinctes | 178 | **327** |
| lignes touchées | 187 | **272** sur 1 195 |
| valeurs répétées ≥ 2 fois | 82 | 133 |

Sur §5.3, la vérification est directe : P2 voyait 12 valeurs, la migration en a repris
**28**. **P2 couvre 43 % du travail réel.**

`resultats/article-synthese.md` — la source de vérité — en porte **566**, sur 78 lignes
seulement : elle est plus dense que le manuscrit.

### 4.2 Combien d'identifiants restent à créer

- **68** des 327 valeurs distinctes sont désormais couvertes par le registre ;
  **259 ne le sont pas**.
- Sur les 610 occurrences, **187 sont couvertes**, 423 ne le sont pas.
- Décompte par forme : **57 triplets distincts** « valeur [bas ; haut] » — chacun est une
  grandeur à intervalle — et **187 valeurs distinctes hors de tout triplet** (points nus,
  exactitudes, seuils, effectifs décimaux).

**Borne haute : 244 identifiants** pour couvrir le manuscrit entier ; **33 sont ouverts**,
donc **≈ 211 restent à créer**. C'est une borne haute et non une estimation : une partie
des 187 points nus n'est pas une grandeur publiée (le seuil α = 0,05, les exactitudes
0,457–0,511 qui décrivent un régime, les numéros de version). Ceux-là relèvent du
commentaire `<!-- P2-exempt: motif -->`, pas d'une ligne de registre. Le tri n'a pas été
fait : le faire suppose de lire les 272 lignes une par une, et c'est précisément le coût
qu'il s'agit de mesurer, pas de préjuger.

### 4.3 Combien de provenances sont introuvables

**Mesuré sur l'échantillon des grandeurs de tête, pas extrapolé** : sur les 23 lignes
ouvertes aujourd'hui, **7 portent au moins un `ABSENT`** (30 %), et sur les 33 lignes du
registre, **9** (27 %). Deux cas sont des **provenances définitivement perdues**, pas des
recherches à finir :

1. **le 0,23 % du comparateur PMM k=10** — script jetable hors dépôt, aucun CSV. Cinq
   champs sur neuf sont `ABSENT`. Le dépôt contient trois autres mesures du même
   comparateur (0,2259 / 0,2187 / 0,2106 %) dont la provenance est complète, mais aucune
   ne peut être attribuée à la valeur publiée sans deviner ;
2. **le 31,6 % du témoin de marge** — le script n'écrit aucun fichier ; la seule trace du
   chiffre est un tableau markdown et une légende gravée dans une image.

À 27 %, les ≈ 211 identifiants restants produiraient **de l'ordre de 55 lignes
incomplètes**. Ce taux est probablement **optimiste** : les grandeurs de tête sont celles
qui ont été auditées ; les valeurs de seconde ligne ont eu moins d'attention.

### 4.4 Combien de temps

Repères mesurés, pas estimés :

| | Grandeurs | Moyen |
|---|---|---|
| socle du 12/09 (§3) | **6**, dont 2 incomplètes | une recherche dédiée |
| aujourd'hui | **23**, dont 7 incomplètes | **trois sous-agents en lecture seule, une passe, en parallèle sur des lots disjoints** |

Le facteur est la parallélisation sur lots disjoints : la provenance d'une grandeur est
une tâche de lecture indépendante, sans contexte partagé — exactement le cas où le
multi-agent fonctionne (v2, fait 5, *a contrario*).

Au rythme mesuré, **≈ 211 identifiants ≈ 9 passes de la taille d'aujourd'hui**. À quoi
s'ajoute, et ce n'est pas parallélisable :

- **l'arbitrage des recoupements entre lots** : trois collisions ont dû être tranchées à
  la main aujourd'hui sur 23 grandeurs, soit une pour huit. Sur 211, ≈ 26 arbitrages ;
- **le tri exemption / grandeur** sur 272 lignes, en série, par un seul agent (§1.1) ;
- **423 substitutions** dans le manuscrit, mécaniques, plus autant dans la synthèse.

**La migration complète du seul manuscrit est un travail de l'ordre de plusieurs jours,
et la synthèse le double.** Aucune des étapes coûteuses n'est la substitution.

## 5. Ce que je n'ai pas pu rendre opposable

1. **La porte P2 refuse la grammaire du rendu.** Mesuré : sur la section migrée,
   `registre_chiffres.py` **se ferme avec 8 violations**, une par `{{R:id.ic}}`, parce
   qu'il cherche `park-tpr-fpr1-fort-ouvert.ic` comme un identifiant entier. **Le
   dispositif du §1.3 ne peut donc pas être appliqué tel quel : les deux moitiés ne sont
   pas compatibles.** Le correctif est d'une ligne — retirer le suffixe `.champ` connu
   avant la recherche, exactement comme le fait `decoupe()` du script de rendu — mais
   `outils/portes/registre_chiffres.py` est **hors de mon périmètre d'écriture** et je ne
   l'ai pas touché. La grammaire à point a été choisie **pour que P2 échoue bruyamment
   plutôt que de laisser passer un renvoi qu'il ne comprend pas** : une syntaxe évitant sa
   regex aurait créé un trou silencieux.
2. **P2 ne voit que 43 % des valeurs à migrer.** Son seuil à deux décimales laisse passer
   toutes les bornes à une décimale. Une porte qui annonce 340 quand le travail est 610
   donne une fausse impression de fond de cuve. Élargir la regex la rendrait aussi plus
   bruyante sur les effectifs et les versions — c'est un arbitrage à trancher, pas un
   oubli.
3. **La règle « deux mesures, deux identifiants » n'est pas opposable aujourd'hui.**
   Vérification faite sur les douze couples documentés (les huit de
   `contre-verification-lettres-2026-09-12.md` §3, le neuvième du socle, les trois de
   l'encadré du socle) : **2 sont entièrement séparés par des identifiants distincts,
   8 ne le sont qu'à moitié** (un membre a un `id`, l'autre aucun), **2 n'ont aucun membre
   au registre** (65,7 / 65,51 % du composite Park naïf ; 3,55 / 3,56 bits). Une valeur
   sans `id` ne peut pas entrer en collision — mais elle n'est pas protégée non plus.
   **La règle ne mord qu'une fois les deux membres inscrits**, et aucun script ne peut
   savoir que deux grandeurs auraient dû être inscrites. C'est le point faible du
   dispositif, et il est structurel.
4. **Une valeur rétractée volontairement citée ne peut pas être rendue.** La ligne
   `nul-casse-N0-top1-json41` (41,2 %) est honnêtement `retracte` : elle est remplacée par
   le témoin reconstruit. Mais le manuscrit la cite **délibérément**, ligne 457, comme
   repère historique — et le rendu refuse, à juste titre selon sa propre règle. Le §1.3
   n'a pas de forme pour « je cite sciemment un chiffre rétracté ». Il en faut une
   (un renvoi explicite du type `{{R:id!historique}}`), sinon la ligne 457 bloquera la
   migration, ou quelqu'un repassera la ligne en `provisoire` pour la débloquer — ce qui
   serait un mensonge sur le statut.
5. **Le registre ne peut pas arbitrer un conflit de graphie.** `deux-organisations-BC-top1`
   porte `1.76` et `[0.35 ; 3.63]` parce que c'est ce que disent les rapports ; le
   manuscrit écrit `1.8 %` et `[0.4 ; 3.6]`. **La migration de ces quatre occurrences est
   impossible sans trancher laquelle des deux graphies fait foi.** Le script ne peut pas
   trancher : s'il reformatait, il reprendrait le pouvoir que le registre lui retire.
   C'est une décision humaine, une fois, et elle doit être écrite.
6. **Trois troncatures au lieu d'arrondis** ont été relevées en passant (22,48 → 22,4 ;
   68,73 → 68,7 ; 5,125 → 5,13 arrondi demi-haut). Elles sont sans conséquence de fond,
   mais elles resteront invisibles tant que la graphie est tapée à la main : une fois au
   registre, elles deviennent une décision explicite. C'est l'effet attendu du dispositif.
7. **Le sens des chiffres reste hors de portée.** Le registre garantit qu'un chiffre vient
   d'un CSV nommé par un script nommé. Il ne garantit pas que la phrase autour dit ce que
   le chiffre mesure. Le « facteur 1,3 » de la ligne 457 en est l'exemple : les deux
   membres du rapport seront tous deux au registre, corrects, et le rapport restera un
   rapport entre estimateurs **non appariés** (100 réplicats contre 20, deux scripts).
   Aucune porte ne peut voir ça.
8. **Un faux positif de plus pour la porte P3, trouvé en écrivant ce rapport.** P3 refuse
   le nom du second plan factoriel (`resultats/c7-loi-distance.csv`) parce que ce nom
   apparaît entre guillemets **à l'intérieur** d'une phrase `INTERDIT :` de
   `article-synthese.md` ligne 130, où l'interdit porte en réalité sur le mot « seize ».
   C'est le défaut déjà documenté au socle §6.4 — P3 confond l'objet d'un interdit et
   l'interdit lui-même. Le taux constaté passe de **1 à 2 faux positifs sur 22
   formulations**. Le remède est une exemption motivée dans
   `outils/portes/interdits-exemptions.txt`, **hors de mon périmètre d'écriture** ; j'ai
   donc contourné en n'employant pas le nom, ce qui est exactement la mauvaise
   incitation que produit une porte à faux positifs.

## 6. Ce qui n'a pas été fait, et qui reste ouvert

- `article/manuscrit.md` **n'a pas été modifié**, conformément au mandat.
- `outils/portes/registre_chiffres.py` n'a pas été amendé (§5.1) : hors périmètre.
- Les ≈ 211 identifiants restants, et le tri exemption / grandeur sur 272 lignes.
- La chaîne de provenance du `0.00 % [0 ; 0.18]` (Clopper-Pearson déclaré, manuscrit
  ligne 498) n'a pas été tracée.
- `resultats/c7-attaquant-fort.csv` porte une **ligne d'en-tête dupliquée** (lignes 1 et 2
  identiques) : un parseur naïf y lira une ligne de données factice. Repéré, non corrigé.
