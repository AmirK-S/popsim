# s1. Page de plan : la croyance de second ordre sur des OPINIONS

**Horodatage d'ecriture : 2026-09-09 12:02:16 CEST (2026-09-09T10:02:16Z).**
Ecrite **avant** tout calcul de statistique de test. Aucun appel de modele de langage dans
toute la seance s1 : lecture seule de fichiers deja sur le disque.

Conventions de certitude : **[CONFIRME]** lu dans une source verifiee, **[MESURE]** calcule
ici, **[PROBABLE]** interpretation etayee, **[HYPOTHESE]** proposition a tester.

---

## 1. La question

Quand un modele de langage decrit ce que pense un ensemble de gens, ressemble t il davantage
a ce que ces gens pensent vraiment, ou a la caricature qu'un camp politique se fait de ce que
les gens pensent ? Et si c'est la caricature : celle de quel camp, et l'ecart entre les deux
caricatures est il **amplifie** ou **ecrase** par rapport aux humains ?

## 2. Pourquoi ce n'est pas la question de r1, et pourquoi r1 ne peut pas y repondre

`resultats/r1-preenregistrement.md` et `resultats/r4-preenregistrement.md` produisent le
premier terme d'une comparaison a trois termes : la croyance du modele sur les 149 items du
GSS, camp par camp, demandeur par demandeur. Le **second terme**, la croyance humaine de
second ordre sur ces memes items, n'existe sur aucun fichier de ce disque. C'est ecrit dans
la docstring de `analyses/r1_oracle_camps.py` (« exige les items de l'ANES et n'est pas
produit ici ») et etabli en detail dans `resultats/a46-second-ordre-ahler-sood.md`,
section 2. Nous le confirmons a l'inventaire, section 3. [CONFIRME]

Consequence assumee : **la comparaison a trois termes sur les 149 items du GSS reste a deux
termes**, et aucune phrase de s1 ne portera sur ces items. s1 change de jeu de donnees pour
obtenir les trois termes sur des opinions, et paie ce changement par une cible differente
(« le public » et non « le camp adverse »), declaree en section 4.3.

## 3. Inventaire honnete du second ordre disponible sur le disque

| source | quantite de second ordre | cible | realite appariee | verdict |
|---|---|---|---|---|
| `data/ahler-sood-pcomp/pcomp_yougov_data.dta` et 3 autres | part percue d'un groupe social dans un parti, 8 items | **un parti** | oui (ANES 2012 et Pew, valeurs recalculees dans `fig_1_data_actual.dta`) | **composition uniquement**, deja traite par a46 et a46b |
| `data/ahler-sood-pcomp/extremity_exp_data.dta`, `dem_per` / `rep_per` | position percue de chaque parti sur 4 enjeux (`tax`, `abortion`, `gays`, `race`), echelle a 5 ou 6 points, 1 036 personnes | **un parti** | **non**, jamais mesuree par les auteurs ; le libelle exact des 4 enonces est absent de l'archive | **inutilisable** faute de realite et de libelle |
| `pcomp_igspoll.dta` (IGS Poll, q19 et q98 : part percue de soutien democrate et republicain a 6 enonces, avec la position propre du repondant en q5) | **l'homologue exact de r1 sur des opinions** | un parti | oui, dans la meme enquete | **absent de l'archive Dataverse**, bien que cite par `readme.txt` |
| `data/anes-codebooks/` | codebooks et index SDA seuls | items de placement des partis | sans objet | **aucune microdonnee**, voir section 8 |
| `data/westwood-pnas-2025/` | repondants synthetiques purs (o4, dem, rep) | sans objet | sans objet | pas de croyance de second ordre humaine |
| `data/osf-t6g7k-stanford/` | 149 items du GSS, reponses de premier ordre | soi meme | oui | **premier ordre seulement** |
| `data/twin2k500/` bloc « False consensus » : **QID287** (soutien propre a 10 politiques publiques, Likert 5 points) et **QID290** (part du public que le repondant croit favorable a ces 10 memes politiques, curseur 0 a 100) | **le public** | **oui, la meme enquete, les memes 10 enonces, les memes 2 058 personnes**, en deux vagues | **utilisable, et c'est le seul** |
| `data/twin2k500/llm/` et `llm_specs/` | 13 configurations de jumeaux numeriques qui repondent **aux memes QID287 et QID290** | le public | idem | **le terme modele, deja calcule par les auteurs, sans un appel de plus** |

[MESURE et CONFIRME, verifie fichier par fichier le 2026-09-09 entre 11h00 et 12h00]

### 3.1 Ce que le bloc « False consensus » de Twin-2K-500 contient exactement

- **QID287**, matrice Likert 5 points, 10 enonces : taxe carbone ; 40 pour cent des
  investissements d'infrastructure propre vers les quartiers pauvres ; electricite sans
  carbone en 2035 ; Medicare for All ; option publique ; regularisation des sans papiers ;
  conge parental paye obligatoire ; impot de 2 pour cent sur les patrimoines de plus de
  50 millions ; augmentation des expulsions ; cheques sante pour les seniors en
  remplacement de Medicare. [CONFIRME, `question_catalog.json`]
- **QID290**, curseur 0 a 100, **exactement les 10 memes enonces**, question
  « What percentage of the public do you think supports the following policies ? ».
  [CONFIRME]
- Les deux questions sont posees **deux fois**, dans `wave1_3_response.csv` et dans
  `wave4_response.csv`, aux memes 2 058 personnes, sans aucune valeur manquante des deux
  cotes. Cette repetition est le **plancher humain de reinterrogation** demande par la
  commande. [MESURE]
- Camps disponibles pour chaque personne : `QID22` ideologie a 5 points, repliee par
  `a30_commun.TWIN_BLOC3` en 909 gauche, 582 centre, 567 droite ; `QID20` parti a
  4 modalites, repliee en 847 gauche, 609 centre, 540 droite et 62 non classables.
  [MESURE]

### 3.2 Les 13 configurations de modele, et deux pieges de nommage

Les dossiers `data/twin2k500/llm/` et `data/twin2k500/llm_specs/` contiennent 31 fichiers
CSV pour **15 contenus distincts** (empreinte MD5). Apres deduplication, les noms des deux
dossiers concordent, a deux exceptions qui doivent etre ecrites :

1. `llm/default_gpt41mini_wave4.csv` **est le fichier humain de la vague 4**, octet pour
   octet identique a `llm_specs/humains_wave4.csv`, et ses reponses QID287 coincident a
   100 pour cent avec `wave4_response.csv`. Ce n'est pas une sortie de modele. Il est exclu
   de la liste des modeles. [MESURE]
2. `llm/default_gpt41mini_llm.csv` est identique a `spec_texte_gpt41mini.csv`, c'est a dire
   a la configuration « Text Persona GPT4.1-mini ». « default » n'est pas une
   configuration de plus. [MESURE]

Il reste **13 configurations de modele**, exactement les 13 de `llm_specs/index.json`.
[MESURE]

## 4. Les quantites

Notation : `j` un enonce parmi 10, `c` un camp parmi {gauche, centre, droite}, `m` une
configuration de modele parmi 13. Toutes les quantites sont en **points de pourcentage sur
0 a 100**, la meme unite des deux cotes.

### 4.1 Les quatre termes

- **Realite**, `R(j)` : part des 2 058 humains de la vague 4 qui soutiennent l'enonce `j`,
  soit la part de QID287 en modalite 4 ou 5 (« somewhat support » ou « strongly support »),
  fois 100. C'est la definition qui colle au verbe de QID290, « supports ».
- **Croyance humaine de second ordre du camp `c`**, `H(j, c)` : moyenne de QID290 vague 4
  sur les humains du camp `c`.
- **Croyance du modele `m` sous le camp `c`**, `M(j, c, m)` : moyenne de QID290 des jumeaux
  du modele `m` dont la personne source appartient au camp `c`.
- **Plancher humain de reinterrogation**, `P(j, c)` : moyenne sur les personnes du camp `c`
  de la valeur absolue de l'ecart entre QID290 vague 1 a 3 et QID290 vague 4, pour l'enonce
  `j`. C'est ce qu'une meme personne se contredit a elle meme.

### 4.2 Les trois distances demandees, par cellule modele x camp

Pour chaque cellule `(m, c)`, moyenne sur les 10 enonces de :

- `D_reel(m, c)` = moyenne_j | M(j, c, m) - R(j) |
- `D_endo(m, c)` = moyenne_j | M(j, c, m) - H(j, c) |, distance a la caricature du camp
  que le modele incarne
- `D_exo(m, c)` = moyenne_j | M(j, c, m) - H(j, c') |, `c'` le camp oppose, distance a la
  caricature du camp adverse
- `P(c)` = moyenne_j P(j, c), le plancher

Le centre n'a pas de camp oppose unique. Comme en r1, la cellule centre existe dans les
tableaux mais **ne sert a aucun test** portant sur `D_exo`.

### 4.3 Ce que « demandeur » devient ici, et la limite que cela coute

r1 fait varier **qui pose la question** (journaliste ou adversaire). Twin ne fait pas varier
le demandeur : la question de QID290 est la meme pour tout le monde. L'axe qui remplace le
demandeur est **le proprietaire de la caricature** : la reponse du modele sous le camp `c`
est confrontee a la caricature de `c` (endo) et a celle de `c'` (exo). C'est le meme
contraste de fond, mais du cote du referent et non du cote de l'invite.

Limite a ecrire dans tout rapport : **la cible decrite ici est « le public », pas « le camp
adverse »**. Aucune phrase de s1 ne pourra donc dire « le modele ressemble a ce que la droite
croit de la gauche ». Elle pourra dire « le modele ressemble a ce que la droite croit du
public ». La forme forte de la question exige l'IGS Poll ou l'ANES, section 8.

## 5. Hypotheses, avec la direction predite

**H1, la substitution.** Pour une majorite des 13 configurations et pour les deux camps
extremes, `D_endo < D_reel` : le modele est plus pres de la caricature de son camp que de la
realite. **Pari qui peut couter** : si `D_reel < D_endo`, le modele est un **correcteur**,
la these de l'amplification tombe, et il faut l'ecrire en tete du rapport.

**H2, l'amplification de l'ecart de perception.** Soit `G_h(j) = H(j, gauche) - H(j, droite)`
et `G_m(j, m) = M(j, gauche, m) - M(j, droite, m)`. Le rapport
`A(m) = moyenne_j |G_m(j, m)| / moyenne_j |G_h(j)|` est **superieur a 1**.
**Pari qui coute cher, et il coute contre notre propre corpus** : a1, a6, a20, t2 et a30
etablissent tous que les modeles **ecrasent** l'heterogeneite. Le corpus predit donc
`A(m) < 1`. Nous preenregistrons quand meme `A(m) > 1`, parce que la these de la caricature
l'exige. Un `A(m)` significativement inferieur a 1 **refute l'amplification** et confirme
l'ecrasement, et ce sera le titre du rapport si c'est ce qui sort.

**H3, la lentille asymetrique.** Quel que soit le camp incarne, la reponse du modele est plus
pres de `H(j, gauche)` que de `H(j, droite)`. Direction predite : **gauche**. Elle peut
couter : la direction inverse, ou l'absence d'ecart, refute la these de la lentille.

**H4, le plancher.** `D_reel(m, c) > P(c)` : l'ecart du modele a la realite depasse ce qu'une
personne se contredit a elle meme d'une vague a l'autre. Sans cela, rien n'est distinguable
du bruit et toutes les autres hypotheses sont indecidables.

**H5, controle de premier ordre.** La part de soutien **simulee** par le modele (QID287 des
jumeaux, modalites 4 ou 5) est comparee a `R(j)`. Sert a savoir si un ecart de second ordre
est un ecart de croyance sur autrui ou un simple decalage de la population simulee. Aucune
direction predite.

## 6. Tests, corrections, materialite

- **Unite de reechantillonnage principale : l'enonce.** Bootstrap sur les 10 enonces,
  10 000 tirages, graine `20260909`, intervalles de percentile a 95 pour cent. C'est la
  convention de r1 et de a46.
- **Controle : bootstrap sur les personnes**, 2 000 tirages, a l'interieur de chaque camp,
  pour `H` et `M`. Rapporte a part, jamais a la place du precedent.
- **Test apparie : permutation de signe sur les 10 enonces.** Avec 10 enonces,
  l'enumeration exacte des 1 024 patrons de signe est faite ; la plus petite p bilaterale
  atteignable est **2 / 1 024 = 0,00195**, donc **le plan a de la puissance a son propre
  seuil de 0,05**. C'est la lecon de a46, dont les 4 items rendaient tout test impossible a
  0,05, verifiee ici avant de commencer. [MESURE]
- **Familles de tests et Holm.** F1 : H1, 13 modeles x 2 camps extremes = 26 tests.
  F2 : H2, 13 tests. F3 : H3, 13 tests. F4 : H4, 26 tests. Holm a l'interieur de chaque
  famille, seuil 0,05. Les p brutes et les p corrigees sont toutes deux publiees.
- **Bande de non materialite** : un rapport dans [0,95 ; 1,05] est declare non materiel,
  meme significatif, comme en r1.
- **Aucun verdict sans intervalle.** Une cellule sans intervalle est publiee « indecidable ».

## 7. Criteres de chute, fixes d'avance

1. Plus de **10 pour cent** de valeurs non numeriques dans le bloc QID290 d'une
   configuration : la configuration sort des tests et le taux est publie.
   *Attendu deja vu a l'inventaire : `json_persona_predicted_output__gpt41_mini` est a
   31 pour cent de non parse et tombera.* [MESURE]
2. Une configuration dont QID290 est constant d'un enonce a l'autre, ou d'un camp a
   l'autre : elle est signalee, sortie de H2 et de H3.
3. Un fichier de modele identique au fichier humain : exclu, comme
   `default_gpt41mini_wave4.csv`.
4. Un camp de moins de 50 personnes dans le perimetre d'une configuration : la cellule est
   publiee « effectif insuffisant » et ne sert a aucun test.
5. Si `P(c)` depasse `moyenne_j |G_h(j)|`, c'est a dire si le bruit de reinterrogation d'une
   personne depasse l'ecart entre les camps, la question n'a pas de resolution sur ce jeu :
   tout est declare indecidable et le rapport s'arrete la.

## 8. Ce qu'ANES ajouterait, et pourquoi il n'est pas ici

Les codebooks presents (`anes_timeseries_2020`, `2024`, cumulatif, plus les index SDA)
listent les items de **placement des partis et des candidats sur des echelles d'enjeux**,
qui sont la forme forte de la croyance de second ordre sur des opinions :

- placement de soi, du parti democrate et du parti republicain sur l'echelle
  **liberal / conservateur** en 7 points ;
- meme triplet sur **depenses et services publics**, **assurance maladie publique contre
  privee**, **emploi et niveau de vie garantis par l'Etat**, **aide aux minorites
  noires**, **defense**, **immigration**, **environnement contre emploi**,
  **avortement** ;
- thermometres de sentiment envers democrates, republicains, liberaux, conservateurs, qui
  donnent l'affect, pas la croyance.

Ce que cela ajouterait, precisement, et que Twin ne donne pas : la cible devient **un camp**
et non le public, et la realite du camp est la moyenne des placements de soi des membres de
ce camp **dans la meme enquete**. La comparaison a trois termes devient exacte, et la phrase
« ce que la droite croit de la gauche » devient dicible. Les microdonnees ANES ne sont pas
redistribuables ; il faut un compte sur `electionstudies.org`, gratuit, et un
telechargement nominatif. C'est une demande a faire, pas un achat.

## 9. Regle d'arret

Le jeu de donnees est fige et ne grandira pas : 10 enonces, 2 058 personnes, 2 vagues,
13 configurations. Il n'y a donc **rien a arreter** au sens sequentiel. La regle est :
`analyses/s1_second_ordre.py` est lance **une fois**, apres cette page, et ses sorties sont
publiees telles quelles, y compris si elles refutent H1, H2 et H3. Toute analyse
supplementaire non listee ici sera etiquetee **exploratoire** dans le rapport, et ne pourra
jamais fournir le chiffre de tete.

## 10. Ce que j'ai regarde avant d'ecrire cette page, et qu'il faut declarer

L'honnetete d'une page de plan tient a ce qu'elle avoue. Avant de l'ecrire, j'ai calcule,
pour chaque fichier, le taux de non parse et **la moyenne globale de QID290, toutes personnes
et tous enonces confondus** : humains vague 4 a 54,0 ; humains vague 1 a 3 a 53,0 ; les
13 configurations entre 46,0 et 62,5. Ce chiffre ne ventile ni par camp ni par enonce, et ne
determine donc aucune des hypotheses H1 a H3, qui portent toutes sur des distances relatives
par camp. Il montre en revanche qu'aucune configuration n'est degeneree, ce qui etait la
raison de le regarder. Rien d'autre n'a ete calcule. [MESURE]

## 11. Sorties attendues

- `resultats/s1-cellules.csv` : une ligne par (modele, camp, ancrage), les trois distances,
  le plancher, les effectifs.
- `resultats/s1-par-enonce.csv` : une ligne par (modele, camp, enonce).
- `resultats/s1-termes-humains.csv` : `R(j)`, `H(j, c)`, `P(j, c)`, avec intervalles.
- `resultats/s1-tests.csv` : les quatre familles, p brutes, p de Holm, intervalles.
- `resultats/s1-amplification.csv` : `A(m)` et son intervalle.
- `resultats/s1-controles.csv` : parse, chutes, effectifs, bootstrap sur les personnes, H5.
- `resultats/s1-resultats.md` : la lecture.

---

## Ce que je n'ai pas pu verifier

1. **Que les 13 fichiers de simulation correspondent bien aux 13 libelles de
   `index.json`.** La verification faite est une verification de coherence entre deux
   dossiers telecharges par deux scripts differents, plus deux anomalies levees. Elle ne
   remonte pas au depot Hugging Face, qui n'est pas reinterroge ici.
2. **Que les jumeaux de la vague 4 aient bien vu la question QID290 dans le meme contexte
   que les humains.** Le protocole des auteurs n'est pas relu dans cette seance.
3. **Le sens exact de la modalite 3 de QID287**, « Neither oppose nor support », qui est
   comptee comme non soutien. Un autre choix, par exemple compter la moitie, changerait
   `R(j)` de quelques points. La sensibilite est prevue en controle, elle n'est pas encore
   faite.
4. **Que « le public » soit compris comme la population americaine adulte** par tous les
   repondants et par tous les modeles. Le libelle ne le precise pas.
5. **Que l'echantillon Twin-2K-500 soit representatif**, ce qu'il n'est pas au sens d'un
   sondage pondere. `R(j)` est la realite **de cet echantillon**, jamais celle des
   Etats Unis.

## Questions ouvertes pour Simon

1. `R(j)` doit il etre la part de soutien de l'echantillon Twin, ou une part exterieure
   ponderee quand elle existe ? Nous prenons l'echantillon, parce que c'est le seul choix
   qui rend le second ordre et la realite commensurables. Est ce le bon arbitrage ?
2. Le seuil de soutien a 4 ou 5 sur 5 est il celui que vous prendriez, ou faut il un seuil a
   3 ou plus, plus proche du mot « supports » entendu largement ?
3. L'axe « proprietaire de la caricature » remplace t il honnetement l'axe « demandeur » de
   r1, ou faut il refuser ce remplacement et attendre l'ANES ?
4. Avez vous acces a `pcomp_igspoll.dta` d'Ahler et Sood, ou un contact chez eux ? C'est le
   seul fichier connu qui donne le second ordre **par parti** sur des opinions avec sa
   realite dans la meme enquete.
5. Preferez vous que le chiffre de tete soit `A(m)`, l'amplification, ou le contraste
   `D_endo` contre `D_reel` ? Les deux sont preenregistres ; un seul peut etre le titre.
