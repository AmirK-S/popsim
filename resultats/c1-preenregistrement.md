# C1, preenregistrement. Les anticipations des menages americains : dispersion, plancher de reinterrogation, personne au dela de la cohorte

**Ecrit le 8 septembre 2026 a 22 h 30 CEST (20 h 30 UTC), depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant l'ecriture du premier script d'analyse et
avant tout calcul statistique.**

Ce document fige les perimetres, les variables, les definitions, les quantites de verdict, les
predictions et les controles bloquants du mois 1 du **programme C version menages**
(`MOONSHOTS.md` section 3, programme C ; `brainstorm/03-economie-entreprises.md` M4), cote
humain. Il est ecrit avant tout chiffre.

## 0. Ce qui a ete regarde avant d'ecrire ce document, et ce qui ne l'a pas ete

Honnetement : **la ligne 2 des quatre fichiers Excel, c'est a dire la liste des noms de
variables, et le questionnaire du module central en PDF, ont ete lus avant d'ecrire ce
document.** Sans eux, aucune variable ne pouvait etre nommee. Ont ete lues aussi les trois
premieres lignes d'un fichier, donc trois observations brutes, pour verifier que la ligne 1 est
la mention de source et la ligne 2 l'entete.

**Aucune statistique n'a ete calculee, aucune distribution n'a ete regardee, aucun mois n'a ete
compare a un autre, aucun identifiant n'a ete recoupe.** Le tableau de structure de
`data/sce-fed-ny/PROVENANCE.md`, ecrit par la session D1, etait deja connu : nombre
d'observations, de variables, de mois, d'identifiants distincts et de vagues par personne, par
fichier. Il est repris ici comme acquis et sera reverifie comme controle bloquant.

## 1. Les donnees

`data/sce-fed-ny/`, quatre fichiers Excel du Survey of Consumer Expectations de la Federal
Reserve Bank of New York, licence FRBNY, empreintes dans `PROVENANCE.md`. Lecture seule.
`openpyxl` 3.1.5 a ete installe dans le `.venv` le 8 septembre 2026 pour lire les `.xlsx` ;
c'est la seule modification d'environnement, elle est declaree ici.

**Perimetre primaire : `frbny-sce-public-microdata-20-24.xlsx` et
`frbny-sce-public-microdata-latest.xlsx`, soit janvier 2020 a octobre 2025, 70 mois.** C'est la
fenetre qui contient a la fois l'episode inflationniste de 2021-2022 et le choc de 2025, et
c'est celle que la mission demande.

**Perimetre secondaire, descriptif seulement : `complete-17-19.xlsx`**, janvier 2017 a decembre
2019, utilise uniquement pour situer la trajectoire d'avant 2020 sur la figure et pour tester la
stabilite des identifiants entre fichiers. Aucun verdict ne repose sur lui.

**Le fichier 13-16 n'est pas ouvert.** Il n'apporte rien a la fenetre demandee et il coute
cinquante mega-octets de lecture.

**Unite d'analyse et unite de reechantillonnage : le menage, identifie par `userid`.** Tous les
intervalles de confiance publies sont des bootstrap a 1 000 tirages **sur les menages**, jamais
sur les observations mois-menage, selon la regle de `a2_commun.bootstrap_personnes`.

## 2. Les variables d'anticipation retenues

Sept variables primaires et cinq secondaires. Le classement primaire/secondaire est fige ici.
Les codes sont ceux de l'entete des fichiers.

### 2.1 Les sept primaires

| cle | construction | nature | domaine attendu |
|---|---|---|---|
| `infl1` | `Q9_mean` | continue, moyenne de la densite subjective d'inflation a un an | non borne |
| `infl3` | `Q9c_mean` | continue, meme chose a trois ans | non borne |
| `revenu` | `Q25v2part2` signee par `Q25v2` (1 = hausse, 3 = baisse) | continue, croissance attendue du revenu du menage a un an, en pour cent | non borne |
| `depense` | `Q26v2part2` signee par `Q26v2` | continue, croissance attendue de la depense du menage | non borne |
| `logement` | `Q31v2part2` signee par `Q31v2` | continue, variation attendue du prix moyen du logement au niveau national | non borne |
| `perte_emploi` | `Q13new` | probabilite subjective de perdre son emploi principal dans douze mois | 0 a 100 |
| `chomage` | `Q4new` | probabilite subjective que le taux de chomage soit plus eleve dans douze mois | 0 a 100 |

`perte_emploi` n'est posee qu'aux salaries non independants ayant au moins un emploi
(`Q10` dans 1, 2, 4, 5 et `Q12new` different de « independant » et `Q11 > 0`). Son perimetre est
donc un sous ensemble, et **il est declare ici que ce sous ensemble est conditionne sur une
variable qui bouge elle meme avec le cycle** ; c'est une reserve, pas un defaut corrigeable.

### 2.2 Les cinq secondaires

| cle | construction | nature |
|---|---|---|
| `infl1_var` | `Q9_var` | incertitude individuelle, variance de la densite subjective a un an |
| `infl1_iqr` | `Q9_iqr` | incertitude individuelle, ecart interquartile de la densite |
| `infl1_point` | `Q8v2part2` signee par `Q8v2` (1 = inflation, 2 = deflation) | prevision ponctuelle d'inflation a un an |
| `fin_avant` | `Q1` | ordinale a cinq modalites, situation financiere comparee a douze mois plus tot |
| `fin_apres` | `Q2` | ordinale a cinq modalites, situation financiere attendue dans douze mois |

`fin_avant` et `fin_apres` sont les deux seules variables ordinales du lot ; elles servent au
volet « variables ordinales » de la mission et sont traitees par les mesures robustes et par le
Gini-Simpson de `a44_commun`, jamais par la variance.

### 2.3 Traitement des valeurs extremes, declare avant de les voir

Les variables de pourcentage de la SCE sont saisies en clair et contiennent des valeurs
aberrantes connues de la litterature. La regle est figee ici :

1. **Aucune troncature pour les mesures robustes.** Ecart interquartile, ecart median absolu et
   quantiles sont calcules sur les valeurs brutes. Ce sont eux qui portent la lecture.
2. **Pour la variance et pour toute regression, winsorisation aux 2e et 98e centiles de la
   distribution mise en commun sur les 70 mois du perimetre primaire**, bornes calculees une
   seule fois par variable et appliquees a l'identique a tous les mois. Les bornes sont
   publiees dans `c1-variables.csv`. Une winsorisation par mois ferait bouger la definition avec
   la quantite mesuree.
3. Les probabilites `perte_emploi` et `chomage` sont bornees a 0 et 100 par construction, elles
   ne sont pas winsorisees.
4. Les valeurs manquantes arrivent en `None` et sont exclues ; aucune imputation.

### 2.4 Ce qui n'existe pas et qu'il faudra dire

**Le module central de la SCE ne contient ni parti, ni ideologie, ni intention de vote.** Le
questionnaire a ete lu en entier ; les seules demographies sont l'age, le sexe, l'origine
hispanique, la race, le diplome, la situation matrimoniale, la composition du menage, l'Etat,
la zone d'emploi, le revenu du menage et la numeratie. La segmentation par camp politique, qui
porte tout le reste du dossier, **est impossible ici**, et le rapport le dira dans la section
descriptive et non en note.

## 3. Les cohortes

**Cohorte primaire : `_AGE_CAT` x `_EDU_CAT` x `_HH_INC_CAT`**, exactement les trois variables
que la mission nomme, telles que la FRBNY les code. Les menages dont l'une des trois est
manquante forment une cellule « non renseigne » a part, jamais fusionnee avec une autre. C'est
le pendant du segment `ideologie x age x education` de i1, avec l'ideologie remplacee par le
revenu faute de mieux, et la meme convention : **une cohorte de moins de cinq menages dans un
mois donne est repliee sur la marginale du mois** pour toute estimation de moyenne de cohorte,
seuil `N_MIN_SEGMENT = 5` de `a44_commun`.

**Cohortes secondaires**, publiees a cote pour la sensibilite : `_AGE_CAT` seul,
`_EDU_CAT x _HH_INC_CAT`, et `_REGION_CAT`. Aucun verdict ne repose sur elles.

Le nombre de niveaux de chaque variable n'a pas ete regarde ; il sera publie tel quel.

## 4. Les quantites

### 4.1 Dispersion mensuelle et sa decomposition (question 2)

Pour chaque variable et chaque mois `t`, sur les menages renseignes :

- **Dispersion totale** : variance sur les valeurs winsorisees, et ecart interquartile sur les
  valeurs brutes. Les deux sont publiees cote a cote.
- **Decomposition inter/intra cohorte, estimateur sans biais.** Avec `G` cohortes d'effectifs
  `n_g`, de moyennes `m_g` et de variances intra `s_g^2` :
  - intra = somme ponderee `sum_g (n_g - 1) s_g^2 / (N - G)` ;
  - inter brute = variance ponderee des `m_g` autour de la moyenne generale ;
  - **inter corrigee = inter brute moins l'esperance de sa part de bruit**, `sum_g w_g (1 - w_g)
    s_g^2 / n_g` avec `w_g = n_g / N`, qui est le terme que l'echantillonnage fini ajoute
    mecaniquement. C'est la meme logique de correction que les estimateurs Gini-Simpson a biais
    corrige de a1 et a35, transposee au continu. **La correction peut rendre la part inter
    negative ; elle est alors publiee negative et lue comme nulle.**
  - **quantite publiee : `part_inter = inter corrigee / (inter corrigee + intra)`**, la part de
    la dispersion inter menages qui est de la difference entre cohortes.
- **Version robuste** : ecart interquartile total du mois, mediane des ecarts interquartiles
  intra cohorte, et ecart interquartile des medianes de cohorte. Aucune decomposition additive
  n'est revendiquee pour la version robuste ; les trois nombres sont publies tels quels.
- **Pour les deux variables ordinales**, la dispersion est le Gini-Simpson a biais corrige de
  `a44_commun.dispersion`, deja utilise par a1, a35 et a44, avec ses ratios inter et intra. Rien
  n'est reimplemente.

Trajectoire : les 70 mois, plus les 36 mois de 2017-2019 en descriptif.

### 4.2 Le choc de 2025, defini depuis les donnees par une regle ecrite d'avance

**Regle primaire.** Le mois du choc `t*` est le mois de la fenetre **janvier 2025 a octobre
2025** qui maximise `|moyenne(infl1, t) - moyenne(infl1, t-1)|`, moyenne calculee sur les
menages renseignes du mois, sans ponderation. Un seul mois est retenu.

**Regle secondaire, publiee a cote et jamais substituee** : le mois de la meme fenetre qui
maximise le saut de la **dispersion** de `infl1`, ecart interquartile.

**Prediction ecrite ici : `t*` sera avril ou mai 2025**, parce que l'annonce tarifaire
americaine du 2 avril 2025 est l'evenement macroeconomique majeur de la fenetre. Si `t*` tombe
ailleurs, la prediction est fausse et le rapport le dira.

**Avant et apres.** Fenetre avant = les trois mois `t*-3, t*-2, t*-1` ; fenetre apres =
`t*, t*+1, t*+2`. Trois mois de chaque cote, declares maintenant, pour que les effectifs de
menages presents des deux cotes soient suffisants et parce que le fichier `latest` s'arrete en
octobre 2025.

### 4.3 Le plancher de reinterrogation (question 3)

Pour chaque variable primaire :

- **Correlation de retest a delai `k`**, `k` de 1 a 11 mois : correlation de Spearman entre
  `x(i, t)` et `x(i, t+k)` sur les couples menage-mois disponibles, **apres retrait de la
  moyenne du mois** de chaque cote, pour que la derive agregee n'alimente pas la correlation.
  Publiee comme courbe, `k` en abscisse. C'est le pendant direct de `a12_retest_delai` sur des
  variables continues.
- **Part stable, decomposition menage / residu.** Sur les menages ayant au moins **trois**
  observations dans le perimetre, apres retrait de la moyenne du mois, decomposition d'analyse
  de variance a un facteur aleatoire :
  `sigma_entre^2` estimee sans biais par `(MS_entre - MS_intra) / n_0` avec `n_0` le nombre
  effectif d'observations par menage, `sigma_intra^2 = MS_intra`.
  **Quantite publiee : `part_stable = sigma_entre^2 / (sigma_entre^2 + sigma_intra^2)`**, la
  part de la dispersion inter menages qui est de la vraie heterogeneite. Elle peut sortir
  negative sur un estimateur sans biais ; elle est alors publiee negative.
- **Verification non circulaire** : la meme part estimee par la correlation de Spearman entre la
  moyenne du menage sur les mois **impairs** et sa moyenne sur les mois **pairs**. Les deux
  estimateurs sont publies ; s'ils divergent de plus de 0,10, le rapport le signale.

### 4.4 La personne au dela de la cohorte (question 4)

**Cible primaire** : `x(i, t+1)`, l'anticipation du menage au mois suivant, pour chaque variable
primaire, sur tous les couples `(i, t)` ou les deux mois sont renseignes.

**Sept predicteurs et temoins**, tous ajustes **hors pli**, cinq plis decoupes **sur les
menages** et non sur les observations :

- `T0b`, **temoin constant** : la moyenne du mois `t+1` calculee sur tout le perimetre, donc
  rigoureusement constante a l'interieur d'un mois. Sa chute doit valoir zero exactement ; c'est
  la verification d'implementation de la permutation, lecon E3 de i1.
- `T1`, **temoin de cohorte** : la moyenne de la cohorte au mois `t+1`, estimee sur le pli
  d'entrainement, repliee sur la marginale du mois sous cinq menages. **Sa chute est attendue
  nulle ou legerement negative**, et sera lue comme nulle, convention explicitement heritee de
  la section 4.3 de i1.
- `P`, **persistance seule** : `x(i, t)`. Zero appel, une ligne. C'est l'adversaire que i1
  designe comme le vrai adversaire, transpose au continu.
- `D`, **demographies seules** : regression ridge sur les indicatrices de `_AGE_CAT`,
  `_EDU_CAT`, `_HH_INC_CAT`, `_REGION_CAT`, `_NUM_CAT`, plus `tenure` et le mois.
- `H`, **historique du menage** : ridge sur `x(i, t)`, `x(i, t-1)` quand elle existe, la moyenne
  et l'ecart type du menage sur ses mois passes, le nombre de mois passes, plus le mois.
- `HD`, **historique et demographies**.
- `F`, **foret**, 200 arbres, sur l'union des variables de `H` et de `D`.

**Score de performance** : correlation de Spearman hors pli entre la prediction et la valeur
realisee, calculee **par mois cible** puis moyennee en ponderant par l'effectif du mois. Le
Spearman est prefere au R2 parce que les queues des variables de pourcentage rendraient un R2
illisible.

**Quantite de verdict declaree : la chute sous permutation des menages a l'interieur de leur
cohorte**, `a44_commun.permuter_intra` reutilise sans retouche, **200 permutations par variable
et par predicteur**, la permutation etant appliquee au vecteur de scores a l'interieur du mois
cible et de la cohorte. Elle vaut zero si le predicteur ne porte que de la cohorte, elle est
positive s'il porte du menage.

**Intervalles** : bootstrap a 1 000 tirages sur les menages, chute recalculee avec une
permutation fraiche a chaque tirage, comme `i1_previsibilite.bootstrap_synthese`.

**Correction pour tests multiples** : famille des sept variables primaires fois sept
predicteurs, `p` de permutation par approximation normale de la loi de permutation, correction
de Holm sur la famille, Benjamini-Hochberg publie a cote. **La lecon E4 de i1 est appliquee
d'avance** : 200 permutations planchent le `p` empirique a 1/201, ce qui rend Holm inapplicable
sur une grande famille ; c'est l'approximation normale qui porte la correction, et les deux
sont publiees.

### 4.5 Qui bouge au choc (question 4, second volet)

Sur les menages presents dans la fenetre avant **et** dans la fenetre apres :

- **Revision** `R(i) = moyenne(x, fenetre apres) - moyenne(x, fenetre avant)`.
- **Cible binaire `Y_rev`** : `1` si `|R(i)|` depasse la mediane de `|R|` sur le perimetre.
  C'est la transposition continue de « qui bouge » de i1.
- Les memes predicteurs, restreints a ce que l'on peut savoir **avant** le choc : historique du
  menage jusqu'a `t*-1` contre demographies seules. Metrique : AUC de `i1_commun.auc`, chute
  sous permutation intra cohorte, meme correction.
- **Nul a derive**, transpose de la section 3.5 de i1 : un temoin qui **conserve la distribution
  des valeurs avant et la distribution des valeurs apres a l'interieur de chaque cohorte, et
  detruit l'appariement**, c'est a dire qui remelange les valeurs de la fenetre apres entre les
  menages de la meme cohorte. Il conserve donc la derive agregee et la derive par cohorte, et il
  ne conserve rien de la personne. **La part de revisions dans le sens de la derive agregee est
  publiee, observee contre nul a derive**, exactement comme i1 l'a fait pour le changement
  monotone.
- **Direction contre ampleur** : la meme mesure est refaite avec `Y_dir = 1{R(i) > 0}`. i1 dit
  que la direction est comptable ; la prediction ci dessous parie que cela se reproduit ici.

### 4.6 Le tableau des cibles pour un jumeau (question 5)

Aucune quantite nouvelle. Le tableau reprend, pour chaque variable primaire : la dispersion
totale et sa part inter cohorte au mois median du perimetre et dans les fenetres avant et apres
le choc ; la part stable ; la chute sous permutation du meilleur predicteur et celle de `P` ;
et les planchers, `T0b` a zero et `T1` lu comme nul. Une population simulee devra reproduire les
trois premieres et **depasser** les deux dernieres.

## 5. Six predictions, ecrites avant tout calcul

| | prediction |
|---|---|
| **P1** | La part inter cohorte de la dispersion de `infl1` est **inferieure a 0,15** a tous les mois du perimetre : l'essentiel du desaccord est a l'interieur des cohortes d'age, de diplome et de revenu, pas entre elles. C'est la prediction qui porte l'enonce du programme C. |
| **P2** | Le mois du choc `t*` tombe en **avril ou mai 2025**. |
| **P3** | Au choc, la **dispersion** de `infl1` augmente d'au moins 10 pour cent en ecart interquartile entre la fenetre avant et la fenetre apres, et elle augmente **plus** que la part inter cohorte, c'est a dire que le desaccord monte surtout a l'interieur des cohortes. |
| **P4** | La **part stable** de `infl1` est comprise entre **0,25 et 0,55**. En dessous de 0,25, la dispersion inter menages serait presque tout du bruit et le programme C perdrait son objet ; au dessus de 0,55, elle serait un trait de menage presque fixe. |
| **P5** | Sur la cible `x(i, t+1)`, la **chute sous permutation de `H` depasse celle de `D`** d'au moins 0,05 point de Spearman, et **`P` seule capte au moins 70 pour cent de la chute de `F`**, c'est a dire la meme structure que i1 : un signal individuel reel, presque entierement fait de la reponse precedente. |
| **P6** | Sur `Y_dir`, la direction de la revision au choc, **la chute sous permutation n'est pas distinguable de zero apres correction**, et la part de revisions dans le sens de la derive agregee est reproduite par le nul a derive a moins de trois points pres. C'est le transport du resultat central de i1 aux anticipations continues. |

## 6. Quatre controles bloquants, executes avant toute lecture de resultat

| | controle | condition de passage |
|---|---|---|
| **C1** | **Reproduction de la structure mesuree par D1** : 71 976 observations utiles et 9 751 `userid` distincts sur 2020-2024, 10 559 observations et 2 159 `userid` sur 2025, aucun couple `(date, userid)` en double. | Les quatre nombres a l'unite pres. Si un seul echoue, la chaine de lecture est fausse et rien n'est publie. |
| **C2** | **Stabilite des identifiants entre fichiers**, le point d'ombre de `PROVENANCE.md` et de la lettre 02. Recouvrement des `userid` entre 17-19, 20-24 et `latest`, et coherence des demographies fixes d'un menage recoupe. | Aucun seuil : le controle est **descriptif et publie quel que soit son resultat**. Il decide seulement si un menage peut etre suivi de 2019 a 2025. Toute analyse du perimetre primaire reste valide dans les deux cas, puisque 20-24 et `latest` sont deux fichiers differents et que le raccord de janvier 2025 depend de ce controle. |
| **C3** | **Verification d'implementation de la permutation** : le temoin `T0b`, constant par mois, doit donner une chute **exactement nulle**. | `|chute| < 1e-9`. Lecon E3 de i1. |
| **C4** | **Puissance minimale** : chaque variable primaire doit avoir au moins **100 menages** dans chaque mois retenu et au moins **300 menages** presents des deux cotes du choc. | Une variable qui echoue est publiee comme non evaluable sur la partie concernee, elle n'est pas retiree du descriptif. |

## 7. Les regles de decision

1. **Si la part inter cohorte de `infl1` depasse 0,40 a tous les mois**, l'enonce du programme C
   version menages est faux tel qu'il est ecrit : le desaccord serait surtout entre cohortes, et
   un gabarit qui reproduit les moyennes de cohorte donnerait a une banque centrale l'essentiel
   de ce qu'elle cherche. Le rapport le dira en premiere ligne.
2. **Si la part stable est inferieure a 0,10**, la dispersion inter menages est du bruit de
   mesure et il n'y a pas de personne a reproduire ; le programme C version menages se replie
   sur la seule trajectoire agregee de la dispersion, et le run simule de la nuit suivante est
   annule.
3. **Si la chute sous permutation de `H` n'est pas distinguable de zero apres correction sur
   toutes les variables primaires**, il n'y a rien qui appartienne au menage au dela de sa
   cohorte, et la barre du run simule devient triviale ; le rapport le dira et le run est
   annule.
4. **Sinon**, la barre du run simule est la chute de `H` et celle de `P`, ecrites dans le
   tableau des cibles, et le run de la nuit suivante est declare avec elles.

## 8. Ce qui n'est pas fait, et qui est declare comme non fait

- **Aucune ponderation.** Les champs `weight` existent et ne sont pas utilises. Toutes les
  quantites publiees sont des quantites d'echantillon, jamais des quantites de population
  americaine. Meme convention que i1 section 9.7.
- **Aucune correction d'attrition.** Le panel est tournant, un menage qui disparait n'est pas
  remplace par son semblable, et les mesures de stabilite portent mecaniquement sur les menages
  qui restent.
- **Aucun appel de modele de langage.** Aucune microdonnee ecrite dans `resultats/`. Aucun
  fichier existant modifie. Quatre coeurs.
- **Aucune donnee externe.** Ni serie officielle d'inflation, ni indice de prix, ni chronologie
  d'evenements ; le choc est defini depuis les donnees par la regle de la section 4.2, et sa
  lecture politique est une hypothese, pas une mesure.

## 9. Les sorties prevues

Scripts `analyses/c1_commun.py`, `c1_decrire.py`, `c1_dispersion.py`, `c1_stabilite.py`,
`c1_previsibilite.py`, `c1_figures.py`. Tableaux `resultats/c1-*.csv`. Figures
`resultats/c1-figure-dispersion-mensuelle.{png,svg}` et
`resultats/c1-figure-chute-permutation.{png,svg}`. Rapport
`resultats/c1-anticipations-sce.md`.

Tout ecart a ce document sera publie dans une section « ecarts au preenregistrement » du
rapport, avec sa raison, selon la forme de i1 section 7.
